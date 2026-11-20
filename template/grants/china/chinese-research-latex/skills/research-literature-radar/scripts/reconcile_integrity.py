#!/usr/bin/env python3
"""Check or rebuild paper manifests without changing review state."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path


MANIFEST_NAME = "manifest.json"


@dataclass(frozen=True)
class PlannedPaper:
    paper_id: str
    manifest_path: Path
    manifest: dict
    manifest_bytes: bytes


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_json(data: object) -> bytes:
    return json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")


def load_catalog(path: Path) -> list[dict]:
    rows: list[dict] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"catalog line {number}: {exc}") from exc
    ids = [row.get("id") for row in rows]
    if any(not paper_id for paper_id in ids):
        raise ValueError("catalog contains an empty id")
    if len(ids) != len(set(ids)):
        raise ValueError("catalog contains duplicate ids")
    return rows


def managed_files(raw_dir: Path) -> list[Path]:
    files: list[Path] = []
    for path in sorted(raw_dir.iterdir(), key=lambda item: item.name):
        if path.name == MANIFEST_NAME or path.name.startswith(".") or path.name.endswith(".tmp"):
            continue
        if path.is_symlink():
            raise ValueError(f"symlink is not allowed in raw: {path}")
        if path.is_file():
            files.append(path)
    return files


def plan(papers_root: Path, catalog_path: Path) -> tuple[list[PlannedPaper], list[dict], bytes]:
    rows = load_catalog(catalog_path)
    planned: list[PlannedPaper] = []
    updated_rows: list[dict] = []
    for row in rows:
        paper_id = row["id"]
        paper_dir = papers_root / paper_id
        raw_dir = paper_dir / "raw"
        note_path = paper_dir / f"{paper_id}.md"
        metadata_path = raw_dir / "metadata.json"
        manifest_path = raw_dir / MANIFEST_NAME
        for required in (paper_dir, raw_dir, note_path, metadata_path):
            if not required.exists():
                raise ValueError(f"missing required path for {paper_id}: {required}")

        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        if metadata.get("id") != paper_id:
            raise ValueError(f"metadata id mismatch for {paper_id}")
        if manifest_path.exists():
            current_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            retrieved = current_manifest.get("retrieved") or metadata.get("retrieved")
        else:
            retrieved = metadata.get("retrieved")

        entries = []
        for path in managed_files(raw_dir):
            entries.append(
                {
                    "path": path.relative_to(paper_dir).as_posix(),
                    "sha256": file_sha256(path),
                    "bytes": path.stat().st_size,
                }
            )
        manifest = {"id": paper_id, "files": entries, "retrieved": retrieved}
        planned.append(
            PlannedPaper(
                paper_id=paper_id,
                manifest_path=manifest_path,
                manifest=manifest,
                manifest_bytes=canonical_json(manifest),
            )
        )

        updated = dict(row)
        updated["files"] = dict(row.get("files") or {})
        updated["files"]["raw"] = [entry["path"] for entry in entries] + ["raw/manifest.json"]
        updated_rows.append(updated)

    catalog_bytes = (
        "\n".join(json.dumps(row, ensure_ascii=False) for row in updated_rows) + "\n"
    ).encode("utf-8")
    return planned, updated_rows, catalog_bytes


def manifest_errors(item: PlannedPaper) -> list[str]:
    if not item.manifest_path.exists():
        return [f"{item.paper_id}: missing raw/manifest.json"]
    try:
        current = json.loads(item.manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{item.paper_id}: invalid manifest JSON: {exc}"]

    errors: list[str] = []
    if current.get("id") != item.paper_id:
        errors.append(f"{item.paper_id}: manifest id mismatch")
    current_entries = {entry.get("path"): entry for entry in current.get("files", [])}
    expected_entries = {entry["path"]: entry for entry in item.manifest["files"]}
    if set(current_entries) != set(expected_entries):
        errors.append(
            f"{item.paper_id}: manifest paths differ; "
            f"expected={sorted(expected_entries)} actual={sorted(current_entries)}"
        )
    for path, expected in expected_entries.items():
        actual = current_entries.get(path)
        if actual is None:
            continue
        fields = []
        if actual.get("sha256") != expected["sha256"]:
            fields.append("sha256")
        if actual.get("bytes") != expected["bytes"]:
            fields.append("bytes")
        if fields:
            errors.append(f"{item.paper_id}: {path} mismatch ({', '.join(fields)})")
    return errors


def check(papers_root: Path, catalog_path: Path) -> list[str]:
    planned, updated_rows, _ = plan(papers_root, catalog_path)
    errors: list[str] = []
    for item in planned:
        errors.extend(manifest_errors(item))
    current_rows = load_catalog(catalog_path)
    if len(current_rows) != len(updated_rows):
        errors.append(
            f"catalog row count mismatch: expected={len(updated_rows)} actual={len(current_rows)}"
        )
    for current, expected in zip(current_rows, updated_rows):
        if (current.get("files") or {}).get("raw") != expected["files"]["raw"]:
            errors.append(f"{current['id']}: catalog files.raw mismatch")
    return errors


def atomic_write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    temporary_path = Path(temporary)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, path)
    finally:
        temporary_path.unlink(missing_ok=True)


def write(papers_root: Path, catalog_path: Path) -> int:
    planned, _, catalog_bytes = plan(papers_root, catalog_path)
    for item in planned:
        if not item.manifest_path.exists() or item.manifest_path.read_bytes() != item.manifest_bytes:
            atomic_write(item.manifest_path, item.manifest_bytes)
    if catalog_path.read_bytes() != catalog_bytes:
        atomic_write(catalog_path, catalog_bytes)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--check", action="store_true")
    action.add_argument("--write", action="store_true")
    parser.add_argument("--papers", type=Path, default=Path("docs/papers"))
    parser.add_argument("--catalog", type=Path, default=Path(".bensz-api/research-literature-radar/catalog.jsonl"))
    args = parser.parse_args()
    try:
        if args.write:
            return write(args.papers, args.catalog)
        errors = check(args.papers, args.catalog)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"integrity error: {exc}")
        return 1
    if errors:
        print("\n".join(errors))
        return 1
    print(f"integrity ok: {len(load_catalog(args.catalog))} papers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
