#!/usr/bin/env python3
"""Discover and validate the required research-literature-search skill."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable


REQUIRED_CONTRACT = "rls.v1"


def candidate_roots(*, explicit: Path | None = None, project_root: Path | None = None) -> Iterable[Path]:
    if explicit is not None:
        yield Path(explicit).expanduser().resolve()
    if project_root is not None:
        yield (Path(project_root).resolve() / "skills" / "research-literature-search").resolve()
    env_root = os.environ.get("RESEARCH_LITERATURE_SEARCH_ROOT") or os.environ.get("RLS_SEARCH_SKILL_ROOT")
    if env_root:
        yield Path(env_root).expanduser().resolve()
    for root in (Path.home() / ".codex" / "skills", Path.home() / ".claude" / "skills"):
        yield (root / "research-literature-search").resolve()


def resolve_search_skill_root(*, explicit: Path | None = None, project_root: Path | None = None) -> Path:
    checked: list[str] = []
    if explicit is not None:
        root = Path(explicit).expanduser().resolve()
        checked.append(str(root))
        if (root / "SKILL.md").is_file() and (root / "config.yaml").is_file():
            return root
        raise FileNotFoundError(
            "显式指定的 research-literature-search 依赖不存在或不完整："
            f"{root}；请修正 --search-skill-root 或移除该参数。"
        )
    for root in candidate_roots(explicit=explicit, project_root=project_root):
        checked.append(str(root))
        if (root / "SKILL.md").is_file() and (root / "config.yaml").is_file():
            return root
    raise FileNotFoundError(
        "research-literature-search 依赖未找到。请安装该 Skill，或传 --search-skill-root <path>；"
        f"已检查：{', '.join(dict.fromkeys(checked))}"
    )


def read_metadata(root: Path) -> tuple[str, str]:
    import yaml

    try:
        config = yaml.safe_load((Path(root) / "config.yaml").read_text(encoding="utf-8")) or {}
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        raise RuntimeError(f"无法读取 research-literature-search 配置：{Path(root) / 'config.yaml'} ({exc})") from exc
    if not isinstance(config, dict):
        raise RuntimeError("research-literature-search config.yaml 必须是对象")
    info = config.get("skill_info") if isinstance(config, dict) else {}
    contract = config.get("contract") if isinstance(config, dict) else {}
    return str((info or {}).get("version") or ""), str((contract or {}).get("version") or "")


def assert_compatible(root: Path, *, required_contract: str = REQUIRED_CONTRACT, minimum_version: str = "1.0.0") -> tuple[str, str]:
    root = Path(root).expanduser().resolve()
    if not (root / "scripts" / "search_runner.py").is_file() or not (root / "scripts" / "validate_bundle.py").is_file():
        raise RuntimeError(f"research-literature-search 缺少稳定脚本入口：{root / 'scripts'}")
    version, contract = read_metadata(root)
    if contract != required_contract:
        raise RuntimeError(f"research-literature-search contract 不兼容：需要 {required_contract}，发现 {contract or '(缺失)'}")
    def version_tuple(value: str) -> tuple[int, int, int]:
        import re
        match = re.fullmatch(r"v?(\d+)\.(\d+)\.(\d+)", value.strip())
        if not match:
            raise RuntimeError(f"research-literature-search 版本无效：{value or '(缺失)'}")
        return tuple(int(part) for part in match.groups())
    if version_tuple(version) < version_tuple(minimum_version):
        raise RuntimeError(f"research-literature-search 版本过低：需要 >= {minimum_version}，发现 {version}")
    return version, contract
