#!/usr/bin/env python3
"""Fail-closed validator for a research-literature-search manifest bundle."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from candidate_schema import SCHEMA_VERSION, validate_candidates
from manifest import ARTIFACT_NAMES, sha256_file
from rls_contract import CONTRACT_VERSION


def _read_jsonl(path: Path) -> list[Any]:
    records: list[Any] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path.name}:{line_no}: invalid JSON ({exc})") from exc
    return records


def validate_bundle(bundle_dir: Path, *, require_candidates: bool = True) -> list[str]:
    root = Path(bundle_dir).expanduser().resolve()
    manifest_path = root / "manifest.json"
    errors: list[str] = []
    if not manifest_path.exists() or not manifest_path.is_file():
        return [f"manifest.json missing in {root}"]
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return [f"manifest unreadable: {exc}"]
    if not isinstance(manifest, dict):
        return ["manifest must be an object"]
    if manifest.get("contract_version") != CONTRACT_VERSION:
        errors.append(f"unsupported contract_version: {manifest.get('contract_version')!r}")
    if manifest.get("candidate_schema_version") != SCHEMA_VERSION:
        errors.append(f"unsupported candidate_schema_version: {manifest.get('candidate_schema_version')!r}")
    if manifest.get("status") not in {"success", "partial_success"}:
        errors.append(f"bundle status is not consumable: {manifest.get('status')!r}")
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, dict):
        return errors + ["manifest.artifacts must be an object"]
    paths: dict[str, Path] = {}
    for name in ARTIFACT_NAMES:
        entry = artifacts.get(name)
        if entry is None:
            errors.append(f"artifact missing from manifest: {name}")
            continue
        if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
            errors.append(f"artifact entry invalid: {name}")
            continue
        relative = Path(entry["path"])
        if relative.is_absolute() or ".." in relative.parts:
            errors.append(f"artifact path is unsafe: {name}={entry['path']!r}")
            continue
        path = (root / relative).resolve()
        try:
            path.relative_to(root)
        except ValueError:
            errors.append(f"artifact path escapes bundle: {name}")
            continue
        paths[name] = path
        if not path.exists() or not path.is_file():
            errors.append(f"artifact file missing: {name} ({relative})")
            continue
        expected = entry.get("sha256")
        if not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected):
            errors.append(f"artifact sha256 missing or invalid: {name}")
        elif sha256_file(path) != expected:
            errors.append(f"artifact hash mismatch: {name}")
        expected_bytes = entry.get("bytes")
        if expected_bytes is not None and (not isinstance(expected_bytes, int) or expected_bytes != path.stat().st_size):
            errors.append(f"artifact byte count mismatch: {name}")

    candidate_path = paths.get("candidates_deduped")
    if candidate_path and candidate_path.exists():
        try:
            candidates = _read_jsonl(candidate_path)
            _, candidate_errors = validate_candidates(candidates)
            errors.extend([f"candidates_deduped: {item}" for item in candidate_errors])
            expected_count = (manifest.get("counts") or {}).get("deduped")
            if expected_count is not None:
                try:
                    count_value = int(expected_count)
                except (TypeError, ValueError):
                    errors.append(f"deduped count is invalid: {expected_count!r}")
                else:
                    if count_value != len(candidates):
                        errors.append(f"deduped count mismatch: manifest={expected_count}, file={len(candidates)}")
            if require_candidates and not candidates:
                errors.append("candidates_deduped is empty")
        except (OSError, UnicodeError, ValueError) as exc:
            errors.append(f"cannot validate candidates_deduped: {exc}")
    elif require_candidates:
        errors.append("candidates_deduped is unavailable")

    query_plan = manifest.get("query_plan")
    accepted_count = None
    if isinstance(query_plan, dict):
        try:
            accepted_count = int(query_plan.get("accepted_count", 0) or 0)
        except (TypeError, ValueError):
            accepted_count = None
    if not isinstance(query_plan, dict) or accepted_count is None or accepted_count < 1:
        errors.append("query_plan.accepted_count must be positive")
    elif not isinstance(query_plan.get("items"), list) or len(query_plan["items"]) != accepted_count:
        errors.append("query_plan.items/count mismatch")
    else:
        ids = [item.get("query_id") for item in query_plan["items"] if isinstance(item, dict)]
        if len(ids) != len(query_plan["items"]) or len(set(ids)) != len(ids):
            errors.append("query_plan items must have unique query_id values")
    counts = manifest.get("counts")
    if not isinstance(counts, dict) or any(isinstance(counts.get(key, 0), bool) or not isinstance(counts.get(key, 0), int) or counts.get(key, 0) < 0 for key in ("raw", "normalized", "deduped", "failed", "dropped")):
        errors.append("manifest.counts must contain non-negative integers")
    warnings = manifest.get("warnings")
    if not isinstance(warnings, list) or any(not isinstance(item, str) for item in warnings):
        errors.append("manifest.warnings must be a string array")
    if manifest.get("status") == "success" and isinstance(warnings, list) and warnings:
        errors.append("success bundle cannot contain warnings; use partial_success")
    if manifest.get("status") == "success" and isinstance(counts, dict) and (counts.get("failed", 0) or (manifest.get("truncation") or {}).get("applied")):
        errors.append("success bundle cannot contain failed attempts or truncation")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate research-literature-search manifest bundle")
    parser.add_argument("bundle", type=Path)
    args = parser.parse_args()
    errors = validate_bundle(args.bundle)
    if errors:
        for error in errors:
            print(f"✗ {error}")
        return 1
    print(json.dumps({"status": "valid", "bundle": str(args.bundle.resolve())}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
