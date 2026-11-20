#!/usr/bin/env python3
"""Fail fast when run-level artifacts leak into the formal papers library."""
from __future__ import annotations

import argparse
from pathlib import Path


FORBIDDEN_FILES = {
    "catalog.jsonl",
    "discovery.md",
    "dedup-report.md",
}
FORBIDDEN_DIRS = {"runs", "logs", "tmp"}


def validate(papers_root: Path) -> list[str]:
    if not papers_root.exists():
        return []
    errors: list[str] = []
    for entry in sorted(papers_root.iterdir()):
        if entry.is_file():
            if entry.name in FORBIDDEN_FILES or entry.name == ".DS_Store" or entry.suffix in {".yaml", ".yml", ".log"}:
                errors.append(f"papers 根目录禁止运行产物: {entry}")
            elif entry.name != "README.md":
                errors.append(f"papers 根目录只能保留 README.md，发现文件: {entry}")
        elif entry.name in FORBIDDEN_DIRS:
            errors.append(f"papers 根目录禁止运行目录: {entry}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("papers", nargs="?", type=Path, default=Path("docs/papers"))
    args = parser.parse_args()
    errors = validate(args.papers)
    if errors:
        print("\n".join(errors))
        return 1
    print(f"layout ok: {args.papers}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
