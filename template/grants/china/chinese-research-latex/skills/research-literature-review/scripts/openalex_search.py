#!/usr/bin/env python3
"""Deprecated OpenAlex wrapper; implementation lives in research-literature-search."""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

SEARCH_ROOT = Path(os.environ.get("RESEARCH_LITERATURE_SEARCH_ROOT", str(Path(__file__).resolve().parents[2] / "research-literature-search"))).expanduser().resolve() / "scripts"
sys.path.insert(0, str(SEARCH_ROOT))
from providers.openalex import search as search_openalex  # noqa: E402


def _work_to_paper(work: dict[str, Any]) -> dict[str, Any]:
    return work


def main() -> int:
    parser = argparse.ArgumentParser(description="Deprecated OpenAlex compatibility wrapper")
    parser.add_argument("--query", required=True)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--max-results", type=int, default=50)
    parser.add_argument("--min-year", type=int)
    parser.add_argument("--max-year", type=int)
    parser.add_argument("--mailto")
    parser.add_argument("--cache-dir", type=Path)
    args = parser.parse_args()
    try:
        rows = search_openalex(args.query, max_results=args.max_results, min_year=args.min_year, max_year=args.max_year, mailto=args.mailto)
    except Exception as exc:  # noqa: BLE001
        print(f"✗ OpenAlex 检索失败：{exc}", file=sys.stderr)
        return 1
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(_work_to_paper(row), ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
