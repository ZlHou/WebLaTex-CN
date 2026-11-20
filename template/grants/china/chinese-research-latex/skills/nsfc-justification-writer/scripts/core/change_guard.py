#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""与 LaTeX 语法无关的预览/写入范围检查。"""

from __future__ import annotations

import difflib
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List


STRUCTURE_COMMAND_RE = re.compile(
    r"\\(?:part|chapter|section|subsection|subsubsection|paragraph|input|include|begin|end|label|newcommand|renewcommand|documentclass|usepackage)\b"
)


@dataclass(frozen=True)
class ChangeGuardResult:
    ok: bool
    changed_lines: int
    structural_hits: List[str]
    diff: str


def inspect_proposal(*, original: str, proposed: str, target_path: Path, project_root: Path) -> ChangeGuardResult:
    """生成 diff，并提示新增/删除行是否触碰结构或配置命令。"""
    root = Path(project_root).resolve()
    target = Path(target_path).resolve()
    target.relative_to(root)  # 越界时抛出 ValueError，由 CLI 转成安全错误
    diff_lines = list(
        difflib.unified_diff(
            (original or "").splitlines(),
            (proposed or "").splitlines(),
            fromfile=str(target),
            tofile=str(target),
            lineterm="",
        )
    )
    changed = [line[1:] for line in diff_lines if line.startswith(("+", "-")) and not line.startswith(("+++", "---"))]
    hits = sorted({m.group(0) for line in changed for m in STRUCTURE_COMMAND_RE.finditer(line)})
    return ChangeGuardResult(ok=not hits, changed_lines=len(changed), structural_hits=hits, diff="\n".join(diff_lines) + ("\n" if diff_lines else ""))
