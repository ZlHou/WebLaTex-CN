#!/usr/bin/env python3
"""Normalize provider envelopes into the versioned paper schema."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Iterable

from candidate_schema import normalize_record, validate_candidates


def read_records(path: Path) -> list[Any]:
    text = path.read_text(encoding="utf-8", errors="replace")
    if path.suffix.lower() == ".jsonl":
        return [json.loads(line) for line in text.splitlines() if line.strip()]
    data = json.loads(text)
    if isinstance(data, list):
        return list(data)
    if isinstance(data, dict) and isinstance(data.get("records"), list):
        return list(data["records"])
    raise ValueError("input must be JSON list or JSONL")


def normalize_records(
    records: Iterable[Any],
    *,
    provider: str,
    query_id: str | None = None,
    issues: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for index, record in enumerate(records, 1):
        if record is None:
            if issues is not None:
                issues.append({"index": index, "code": "empty_record"})
            continue
        if not isinstance(record, dict):
            if issues is not None:
                issues.append({"index": index, "code": "invalid_record_type", "type": type(record).__name__})
            continue
        raw = dict(record)
        # Provider-specific aliases are resolved once at the boundary.
        if provider == "semantic_scholar":
            ext = raw.get("externalIds") if isinstance(raw.get("externalIds"), dict) else {}
            raw.setdefault("doi", ext.get("DOI"))
            raw.setdefault("pmid", ext.get("PubMed"))
            raw.setdefault("arxiv", ext.get("ArXiv"))
            raw.setdefault("venue", raw.get("venue"))
        elif provider == "crossref":
            titles = raw.get("title")
            if isinstance(titles, list):
                raw["title"] = titles[0] if titles else ""
            dates = raw.get("published") or raw.get("published-print") or raw.get("issued")
            if isinstance(dates, dict) and isinstance(dates.get("date-parts"), list) and dates["date-parts"]:
                parts = dates["date-parts"][0]
                if parts:
                    raw.setdefault("year", parts[0])
                    raw.setdefault("published_date", "-".join(str(item) for item in parts))
            authors = raw.get("author")
            if isinstance(authors, list):
                raw["authors"] = [" ".join(str(item) for item in (author.get("given"), author.get("family")) if item) for author in authors if isinstance(author, dict)]
        try:
            output.append(normalize_record(raw, provider=provider, query_id=query_id, rank=index, fallback_index=index))
        except ValueError as exc:
            if issues is not None:
                code = getattr(exc, "code", "normalization_failed")
                issues.append({"index": index, "code": code, "message": str(exc)[:200]})
    return output


def write_jsonl(path: Path, records: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize provider records into rls.paper.v1 JSONL")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--provider", default="legacy")
    parser.add_argument("--query-id")
    args = parser.parse_args()
    issues: list[dict[str, Any]] = []
    records = normalize_records(read_records(args.input), provider=args.provider, query_id=args.query_id, issues=issues)
    _, errors = validate_candidates(records)
    if errors:
        parser.error("normalized candidates invalid: " + "; ".join(errors[:5]))
    if issues:
        print(f"skipped {len(issues)} invalid candidate record(s): " + ", ".join(sorted({str(item['code']) for item in issues})), file=sys.stderr)
    write_jsonl(args.output, records)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
