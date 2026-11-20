#!/usr/bin/env python3
"""Promote a fully audited paper corpus to complete status atomically."""
from __future__ import annotations

import argparse
import json
import os
import re
import tempfile
from pathlib import Path


def atomic_write(path: Path, data: bytes) -> None:
    fd, name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(name, path)
    finally:
        Path(name).unlink(missing_ok=True)


def ids_from_file(path: Path) -> list[str]:
    return [line[2:].strip() for line in path.read_text(encoding="utf-8").splitlines() if line.startswith("- ")]


def summary_is_unanimous(summary: str, expected: int) -> bool:
    """Accept common human summaries without tying promotion to one run size."""
    compact = re.sub(r"\s+", "", summary)
    ratios = re.findall(r"PASS(?:[:：]|=)?(\d+)/(\d+)", compact, re.IGNORECASE)
    pass_counts = [int(value) for value in re.findall(r"PASS(?:[:：]|=)?(\d+)", compact, re.IGNORECASE)]
    fail_counts = [int(value) for value in re.findall(r"FAIL(?:[:：]|=)?(\d+)", compact, re.IGNORECASE)]
    if len(set(pass_counts)) > 1 or len(set(fail_counts)) > 1:
        return False
    if not fail_counts or any(value != 0 for value in fail_counts):
        return False
    if ratios:
        return all(passed == expected and total == expected for passed, total in ratios)
    return bool(pass_counts) and all(value == expected for value in pass_counts)


def render_promoted_note(path: Path) -> bytes:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "\n---\n" not in text:
        raise ValueError(f"invalid frontmatter: {path}")
    head, body = text.split("\n---\n", 1)
    status_rows = [line for line in head.splitlines() if re.fullmatch(r"status\s*:.*", line)]
    if len(status_rows) > 1:
        raise ValueError(f"duplicate status keys: {path}")
    lines = ["status: complete" if re.fullmatch(r"status\s*:.*", line) else line for line in head.splitlines()]
    if not any(line == "status: complete" for line in lines):
        lines.append("status: complete")
    return ("\n".join(lines) + "\n---\n" + body).encode("utf-8")


def promote_note(path: Path) -> None:
    atomic_write(path, render_promoted_note(path))


def render_promoted_notes(paths: list[Path]) -> dict[Path, bytes]:
    """Validate every note before the caller writes any of them."""
    return {path: render_promoted_note(path) for path in paths}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--papers", type=Path, default=Path("docs/papers"))
    parser.add_argument("--ids-file", type=Path, required=True)
    parser.add_argument("--catalog", type=Path, default=Path(".bensz-api/research-literature-radar/catalog.jsonl"))
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--run-id", default="manual")
    args = parser.parse_args()
    summary = args.summary.read_text(encoding="utf-8")
    ids = ids_from_file(args.ids_file)
    if not ids:
        raise SystemExit("refusing promotion: ids file is empty")
    if len(ids) != len(set(ids)):
        raise SystemExit("refusing promotion: ids file contains duplicates")
    if not summary_is_unanimous(summary, len(ids)):
        raise SystemExit(f"refusing promotion: summary is not unanimous PASS for {len(ids)} ids")
    rows = []
    for line in args.catalog.read_text(encoding="utf-8").splitlines():
        if line.strip(): rows.append(json.loads(line))
    catalog_ids = {row.get("id") for row in rows}
    if not set(ids) <= catalog_ids:
        raise SystemExit("refusing promotion: ids missing from catalog")
    selected = {row["id"]: row for row in rows if row.get("id") in ids}
    if len(selected) != len(ids):
        raise SystemExit("refusing promotion: ids missing from catalog")
    note_paths = [args.papers / paper_id / f"{paper_id}.md" for paper_id in ids]
    missing = [str(path) for path in note_paths if not path.is_file()]
    if missing:
        raise SystemExit("refusing promotion: missing note paths: " + ", ".join(missing))
    promoted_notes = render_promoted_notes(note_paths)
    for path, data in promoted_notes.items():
        atomic_write(path, data)
    for row in rows:
        if row.get("id") not in selected:
            continue
        row["status"] = "complete"
        history = row.setdefault("history", [])
        action = f"interpretation-complete-{args.run_id}"
        if not any(event.get("action") == action for event in history):
            history.append({"run": args.run_id, "action": action})
    data = ("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n").encode("utf-8")
    atomic_write(args.catalog, data)
    print(f"promoted {len(ids)} audited notes; catalog rows={len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
