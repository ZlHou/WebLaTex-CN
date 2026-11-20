#!/usr/bin/env python3
"""Optional, bounded abstract enrichment command."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from search_runner import enrich_abstracts


def main() -> int:
    parser = argparse.ArgumentParser(description="Enrich selected paper abstracts")
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
