#!/usr/bin/env python3
"""整理旧运行目录根部泄漏的已知中间产物。"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Mapping

import yaml

try:
    from layout_paths import LayoutPaths
except ModuleNotFoundError:  # 允许被 qa 动态加载
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from layout_paths import LayoutPaths


FINAL_SUFFIXES = (
    "_工作条件.md",
    "_review.tex",
    "_参考文献.bib",
    "_review.pdf",
    "_review.docx",
    "_验证报告.md",
)


def is_final_output(path: Path) -> bool:
    return any(path.name.endswith(suffix) for suffix in FINAL_SUFFIXES)


def iter_candidates(work_dir: Path) -> list[Path]:
    globs = [
        "pipeline_state.json",
        "checkpoint_*.json",
        "search_plan*.json",
        "search_log_openalex.json",
        "papers*.jsonl",
        "extended_papers*.jsonl",
        "supplemented_papers*.jsonl",
        "expanded_keywords.json",
        "quality_report*.json",
        "evidence_sufficiency*.json",
        "evidence_cards*.jsonl",
        "dedupe_map*.json",
        "supplement_search_history*.json",
        "sentinel_*",
        "selected_*",
        "selection_rationale*.yaml",
        "word_budget*.csv",
        "non_cited_budget.csv",
        "doi_to_bibkey.json",
        "bibtex_report.json",
        "ccs_append*.bib",
        "data_extraction_table.md",
        "degraded_outline*.md",
        "temp_*.py",
        "debug_*.py",
        "analysis_*.py",
    ]
    seen: set[Path] = set()
    result: list[Path] = []
    for pattern in globs:
        for path in sorted(work_dir.glob(pattern)):
            if path not in seen:
                seen.add(path)
                result.append(path)
    return result


def organize_run_dir(
    work_dir: Path,
    config: Mapping[str, Any] | None = None,
    *,
    apply: bool = False,
) -> list[str]:
    """整理根部泄漏文件，返回已计划/移动的文件名。"""
    work_dir = Path(work_dir).expanduser().resolve()
    if not work_dir.is_dir():
        raise ValueError(f"work_dir not found or not a directory: {work_dir}")

    paths = LayoutPaths.from_config(work_dir, config)
    checkpoints = paths.hidden_dir / "checkpoints"
    moves: list[tuple[Path, Path]] = []
    for path in iter_candidates(work_dir):
        if not path.is_file() or is_final_output(path):
            continue
        if path.name.startswith("checkpoint_"):
            target_dir = checkpoints
        elif path.name == "pipeline_state.json":
            target_dir = paths.hidden_dir
        elif path.suffix == ".py":
            target_dir = paths.scripts_dir
        else:
            target_dir = paths.artifacts_dir
        destination = target_dir / path.name
        if destination.exists():
            raise ValueError(f"整理目标已存在，拒绝覆盖：{destination}")
        moves.append((path, destination))

    if apply:
        for _, destination in moves:
            destination.parent.mkdir(parents=True, exist_ok=True)
        for source, destination in moves:
            source.replace(destination)
    return [source.name for source, _ in moves]


def main() -> int:
    parser = argparse.ArgumentParser(description="Organize a research-literature-review run directory layout.")
    parser.add_argument("--work-dir", required=True, type=Path, help="Run directory")
    parser.add_argument("--apply", action="store_true", help="Apply changes; default is dry-run")
    parser.add_argument("--config", type=Path, default=Path(__file__).parent.parent / "config.yaml")
    args = parser.parse_args()

    try:
        config = yaml.safe_load(args.config.read_text(encoding="utf-8")) or {}
        paths = LayoutPaths.from_config(args.work_dir, config)
        planned = organize_run_dir(args.work_dir, config, apply=args.apply)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        raise SystemExit(str(exc))

    if not planned:
        print("✓ no moves needed")
        return 0
    print(f"work_dir: {Path(args.work_dir).expanduser().resolve()}")
    print(f"hidden:   {paths.hidden_dir}")
    print(f"mode:     {'apply' if args.apply else 'dry-run'}")
    for name in planned:
        print(f"- {name}")
    if args.apply:
        print(f"✓ moved {len(planned)} files into {paths.hidden_dir}/")
    else:
        print("(dry-run) add --apply to move files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
