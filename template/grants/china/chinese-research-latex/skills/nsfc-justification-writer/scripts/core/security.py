#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, List, Mapping, Optional

import re

from .config_access import get_mapping, get_seq_str
from .config_loader import DEFAULT_CONFIG


@dataclass(frozen=True)
class WritePolicy:
    allowed_relpaths: List[str]
    forbidden_relpaths: List[str]
    forbidden_globs: List[str]


def build_write_policy(config: Mapping[str, Any]) -> WritePolicy:
    guard = get_mapping(config, "guardrails")
    if not guard:
        # 兜底：即使上层未通过 config_loader.load_config() 加载，也不允许“空策略”导致任意写入
        guard = get_mapping(DEFAULT_CONFIG, "guardrails")
    return WritePolicy(
        allowed_relpaths=list(get_seq_str(guard, "allowed_write_files")) or ["extraTex/1.1.立项依据.tex"],
        forbidden_relpaths=list(get_seq_str(guard, "forbidden_write_files")) or ["main.tex", "extraTex/@config.tex"],
        forbidden_globs=list(get_seq_str(guard, "forbidden_write_globs")) or ["**/*.cls", "**/*.sty"],
    )


def _matches_any_glob(path: Path, globs: Iterable[str]) -> bool:
    for pat in globs:
        if path.match(pat):
            return True
    return False


def validate_write_target(
    *,
    project_root: Path,
    target_path: Path,
    policy: WritePolicy,
) -> None:
    project_root = project_root.resolve()
    target_path = target_path.resolve()
    try:
        rel = target_path.relative_to(project_root)
    except ValueError as e:
        raise RuntimeError(f"写入目标不在 project_root 内：{target_path}") from e

    rel_str = rel.as_posix()

    if policy.forbidden_relpaths and rel_str in set(policy.forbidden_relpaths):
        raise RuntimeError(f"禁止写入文件：{rel_str}")

    if policy.forbidden_globs and _matches_any_glob(rel, policy.forbidden_globs):
        raise RuntimeError(f"禁止写入路径（glob 命中）：{rel_str}")

    if policy.allowed_relpaths:
        if rel_str not in set(policy.allowed_relpaths):
            raise RuntimeError(
                f"写入目标不在白名单：{rel_str}；如这是项目正文目标，请将该相对路径精确加入 guardrails.allowed_write_files"
            )


def resolve_target_path(project_root: Path, relpath: str) -> Path:
    return (project_root / relpath).resolve()


def discover_target_candidates(project_root: Path) -> List[str]:
    """只读追踪 main.tex 的 input/include 候选；不在多个候选中猜测。"""
    root = Path(project_root).resolve()
    main = root / "main.tex"
    if not main.is_file():
        return []
    text = main.read_text(encoding="utf-8", errors="ignore")
    candidates: List[str] = []
    for match in re.finditer(r"\\(?:input|include)\s*\{([^{}]+)\}", text):
        raw = match.group(1).strip()
        if not raw:
            continue
        rel = raw if raw.endswith(".tex") else raw + ".tex"
        p = (root / rel).resolve()
        try:
            p.relative_to(root)
        except ValueError:
            continue
        if p.is_file() and p not in {root / "main.tex"}:
            candidates.append(p.relative_to(root).as_posix())
    return sorted(set(candidates))


def discover_target_relpath(project_root: Path) -> Optional[str]:
    candidates = discover_target_candidates(project_root)
    return candidates[0] if len(candidates) == 1 else None


def choose_target_relpath(project_root: Path, candidates: Optional[List[str]] = None) -> str:
    """为全自动流程确定正文目标，不向用户发起候选确认。"""
    root = Path(project_root).resolve()
    items = list(candidates if candidates is not None else discover_target_candidates(root))
    if not items:
        return "extraTex/1.1.立项依据.tex"

    def rank(rel: str) -> tuple[int, int, str]:
        name = Path(rel).stem.lower()
        preferred = ("立项依据", "justification", "justif", "proposal", "basis")
        hit = 0 if any(token in name for token in preferred) else 1
        depth = len(Path(rel).parts)
        return hit, depth, rel

    return min(items, key=rank)


def validate_target_file(*, project_root: Path, target_path: Path, require_exists: bool = True) -> Path:
    """统一规范化目标路径，拒绝越出项目根目录的绝对路径和符号链接。"""
    root = Path(project_root).resolve()
    target = Path(target_path).resolve()
    try:
        target.relative_to(root)
    except ValueError as exc:
        raise RuntimeError(f"目标路径越出 project_root：{target}") from exc
    if require_exists and (not target.is_file()):
        raise RuntimeError(f"目标文件不存在或不是普通文件：{target}")
    return target
