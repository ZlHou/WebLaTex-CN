#!/usr/bin/env python3
"""Deprecated compatibility wrapper for ``research-literature-search``.

New code must call ``skills/research-literature-search/scripts/search_runner.py``.
The legacy CLI and its flat output names remain available for existing runners.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import tempfile
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Optional

# Bootstrap the explicit override before importing the producer modules.  This
# keeps the deprecated wrapper usable when review/search are installed apart.
for _index, _arg in enumerate(sys.argv[:-1]):
    if _arg == "--search-skill-root":
        os.environ["RESEARCH_LITERATURE_SEARCH_ROOT"] = str(Path(sys.argv[_index + 1]).expanduser().resolve())

SEARCH_ROOT = Path(os.environ.get("RESEARCH_LITERATURE_SEARCH_ROOT", str(Path(__file__).resolve().parents[2] / "research-literature-search"))).expanduser().resolve() / "scripts"
sys.path.insert(0, str(SEARCH_ROOT))
from providers import search_crossref, search_openalex, search_semantic_scholar  # noqa: E402
from query_contract import QueryInputError, QueryPlan, load_query_plan, normalize_query_payload  # noqa: E402
from search_runner import run_search  # noqa: E402


@dataclass
class SearchLog:
    query: str
    rationale: str
    returned: int
    unique: int
    notes: str = ""
    provider_used: str = ""
    attempts: list[dict[str, Any]] | None = None


def _load_query_plan(queries_path: Optional[Path], query_list: Optional[str], *, min_queries: int, max_queries: int) -> QueryPlan:
    if queries_path is not None and query_list:
        raise QueryInputError("--queries 与 --query-list 不能同时使用")
    if queries_path is not None:
        return load_query_plan(queries_path, min_queries=min_queries, max_queries=max_queries)
    if query_list:
        try:
            data = json.loads(query_list)
        except json.JSONDecodeError as exc:
            raise QueryInputError(f"无法解析 --query-list JSON：{exc}") from exc
        return normalize_query_payload(data, min_queries=min_queries, max_queries=max_queries, source="--query-list")
    raise QueryInputError("未提供 --queries/--query-list 或 --query-file")


def _load_queries(queries_path: Optional[Path], query_list: Optional[str]) -> list[dict[str, str]]:
    try:
        return _load_query_plan(queries_path, query_list, min_queries=1, max_queries=25).queries
    except QueryInputError:
        return []


def _legacy_key(record: dict[str, Any]) -> str:
    return str(record.get("doi") or f"{record.get('title', '').strip().lower()}::{record.get('year')}")


def multi_search(queries: list[dict[str, str]], max_results_per_query: int, mailto: Optional[str], min_year: Optional[int], max_year: Optional[int], polite_delay: tuple[float, float] = (0.0, 0.0), cache_dir: Optional[Path] = None) -> tuple[list[dict[str, Any]], list[SearchLog], dict[str, Any], dict[str, Any]]:
    """In-process compatibility API backed by the canonical search runner."""
    payload = {"queries": queries}
    functions = {"openalex": search_openalex, "semantic_scholar": search_semantic_scholar, "crossref": search_crossref}
    with tempfile.TemporaryDirectory(prefix="rls-legacy-") as tmp:
        root = Path(tmp)
        query_file = root / "queries.json"
        query_file.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        manifest = run_search(
            topic="",
            query_file=query_file,
            output_dir=root / "bundle",
            scope_root=root,
            provider_order=["openalex", "semantic_scholar", "crossref"],
            max_results_per_query=max_results_per_query,
            filters={"min_year": min_year, "max_year": max_year},
            provider_functions=functions,
            provider_options={"min_queries": 1, "max_queries": 25, "mailto": mailto},
        )
        bundle = root / "bundle"
        papers = _read_jsonl(bundle / "candidates_deduped.jsonl") if (bundle / "candidates_deduped.jsonl").exists() else []
        log_data = json.loads((bundle / "search_log.json").read_text(encoding="utf-8")) if (bundle / "search_log.json").exists() else {}
        logs = []
        for index, item in enumerate(log_data.get("queries") or [], 1):
            attempts = item.get("attempts") or []
            used = next((str(attempt.get("provider")) for attempt in attempts if attempt.get("status") == "success"), "")
            query_id = f"q{index:02d}"
            unique = sum(1 for row in papers if query_id in (row.get("query_matches") or []))
            logs.append(SearchLog(query=item.get("query", ""), rationale=item.get("rationale", ""), returned=int(item.get("returned", 0) or 0), unique=unique, provider_used=used, attempts=attempts))
        return papers, logs, manifest, {"enabled": False}


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Deprecated multi-query wrapper")
    parser.add_argument("--queries", type=Path)
    parser.add_argument("--query-list")
    parser.add_argument("--min-queries", type=int, default=5)
    parser.add_argument("--max-queries", type=int, default=25)
    parser.add_argument("--query-source", default="direct_cli")
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--search-log", type=Path, default=Path("search_log_multi_query.json"))
    parser.add_argument("--bundle-dir", type=Path, help="new search bundle directory")
    parser.add_argument("--topic", default="")
    parser.add_argument("--max-results-per-query", type=int, default=50)
    parser.add_argument("--max-total", type=int, default=500)
    parser.add_argument("--mailto")
    parser.add_argument("--min-year", type=int)
    parser.add_argument("--max-year", type=int)
    parser.add_argument("--cache-dir", type=Path)
    parser.add_argument("--scope-root", type=Path)
    parser.add_argument("--search-skill-root", type=Path, help="research-literature-search Skill 根目录")
    parser.add_argument("--provider-order", "--providers")
    parser.add_argument("--no-fallback", action="store_true")
    args = parser.parse_args()
    if args.search_skill_root is not None:
        # The parent runner normally exports this before spawning us.  Keep a
        # clear CLI-compatible override for direct legacy invocations; imports
        # above still use the environment when available.
        os.environ["RESEARCH_LITERATURE_SEARCH_ROOT"] = str(args.search_skill_root.expanduser().resolve())
    try:
        plan = _load_query_plan(args.queries, args.query_list, min_queries=args.min_queries, max_queries=args.max_queries)
    except QueryInputError as exc:
        print(f"✗ 查询输入错误：{exc}", file=sys.stderr)
        return 1
    if args.bundle_dir:
        provider_order = [item.strip() for item in args.provider_order.split(",") if item.strip()] if args.provider_order else None
        manifest = run_search(topic=args.topic, query_file=args.queries or Path("queries.json"), output_dir=args.bundle_dir, filters={"min_year": args.min_year, "max_year": args.max_year}, provider_order=provider_order, max_results_per_query=args.max_results_per_query, max_total=args.max_total, fallback_enabled=not args.no_fallback, scope_root=args.scope_root, query_source=args.query_source, provider_options={"min_queries": args.min_queries, "max_queries": args.max_queries})
        bundle = args.bundle_dir.resolve()
        normalized = bundle / "candidates_normalized.jsonl"
        log = bundle / "search_log.json"
        if normalized.exists():
            shutil.copy2(normalized, args.output)
        if log.exists():
            shutil.copy2(log, args.search_log)
        return 0 if manifest.get("status") in {"success", "partial_success"} else 1
    papers, logs, _, _ = multi_search(plan.queries, args.max_results_per_query, args.mailto, args.min_year, args.max_year, cache_dir=args.cache_dir)
    papers = papers[: args.max_total] if args.max_total > 0 else papers
    _write_jsonl(args.output, papers)
    payload = {"search_mode": "multi_query", "query_source": args.query_source, "requested_query_count": plan.requested_count, "accepted_query_count": plan.accepted_count, "fallback_reason": "", "total_returned": sum(item.returned for item in logs), "total_unique": len(papers), "queries": [asdict(item) for item in logs]}
    args.search_log.parent.mkdir(parents=True, exist_ok=True)
    args.search_log.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
