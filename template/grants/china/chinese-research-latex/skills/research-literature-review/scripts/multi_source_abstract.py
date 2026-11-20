#!/usr/bin/env python3
"""Deprecated abstract enrichment wrapper for research-literature-search."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SEARCH_ROOT = Path(__file__).resolve().parents[2] / "research-literature-search" / "scripts"
sys.path.insert(0, str(SEARCH_ROOT))
from search_runner import enrich_abstracts  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Deprecated abstract enrichment wrapper")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--topic", default="")
    parser.add_argument("--timeout", type=int, default=3)
    parser.add_argument("--max-papers", type=int, default=200)
    parser.add_argument("--min-abstract-chars", type=int, default=80)
    parser.add_argument("--cache-dir", type=Path)
    parser.add_argument("--cache-ttl-seconds", type=int, default=86400)
    args = parser.parse_args()
    print(json.dumps(enrich_abstracts(args.input, args.output, max_papers=args.max_papers, min_chars=args.min_abstract_chars, timeout=args.timeout), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
