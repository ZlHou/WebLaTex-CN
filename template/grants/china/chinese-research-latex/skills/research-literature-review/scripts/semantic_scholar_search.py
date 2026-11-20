#!/usr/bin/env python3
"""Deprecated Semantic Scholar wrapper."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

SEARCH_ROOT = Path(os.environ.get("RESEARCH_LITERATURE_SEARCH_ROOT", str(Path(__file__).resolve().parents[2] / "research-literature-search"))).expanduser().resolve() / "scripts"
sys.path.insert(0, str(SEARCH_ROOT))
from providers.semantic_scholar import search as search_semantic_scholar  # noqa: E402


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Deprecated Semantic Scholar compatibility wrapper")
    parser.add_argument("--query", required=True)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--max-results", type=int, default=50)
    args = parser.parse_args()
    try:
        rows = search_semantic_scholar(args.query, max_results=args.max_results)
    except Exception as exc:  # noqa: BLE001
        print(f"✗ Semantic Scholar 检索失败：{exc}", file=sys.stderr)
        return 1
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
