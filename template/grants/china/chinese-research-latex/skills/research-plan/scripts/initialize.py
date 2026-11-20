#!/usr/bin/env python3
"""
Make Research Plan - 初始化脚本

创建项目工作目录结构。
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Optional


def _slug(value: str) -> str:
    value = re.sub(r"[^0-9A-Za-z\u4e00-\u9fff_-]+", "-", value.strip())
    return value.strip("-_") or "research-plan"


def create_work_directory(work_dir: Optional[str] = None, task_label: Optional[str] = None) -> dict:
    """
    创建工作目录结构。

    Args:
        work_dir: 工作目录路径，默认为当前目录

    Returns:
        包含目录路径和创建结果的字典

    Raises:
        PermissionError: 目录不可写
        NotADirectoryError: 路径不是目录
    """
    if work_dir is None:
        work_dir = os.getcwd()

    work_path = Path(work_dir).resolve()
    base_path = Path.cwd().resolve()

    # 安全性验证：确保解析后的路径在允许的范围内（防御符号链接攻击）
    try:
        work_path.relative_to(base_path)
    except ValueError:
        raise PermissionError(f"路径超出允许范围: {work_path}")

    # 验证目录
    if not work_path.exists():
        raise NotADirectoryError(f"目录不存在: {work_path}")
    if not work_path.is_dir():
        raise NotADirectoryError(f"路径不是目录: {work_path}")
    if not os.access(work_path, os.W_OK):
        raise PermissionError(f"目录不可写: {work_path}")

    # 创建任务级工作目录；旧 .make-research-plan 仅作显式兼容读取。
    timestamp = datetime.now().strftime("%Y%m%d-%H%M")
    label = _slug(task_label or "research-plan")
    task_base = work_path / ".bensz-api"
    task_base.mkdir(parents=True, exist_ok=True)
    task_root = task_base / f"task-{timestamp}-{label}"
    if task_root.exists():
        for index in range(2, 100):
            candidate = task_base / f"task-{timestamp}-{label}-{index:02d}"
            if not candidate.exists():
                task_root = candidate
                break
        else:
            raise RuntimeError("无法分配唯一任务工作区")
    hidden_dir = task_root / "research-plan"

    # 目录结构
    directories = [
        task_root / "shared" / "input",
        task_root / "shared" / "output",
        task_root / "shared" / "log",
        hidden_dir / "input" / "papers",
        hidden_dir / "input" / "metadata",
        hidden_dir / "output" / "extracted",
        hidden_dir / "output",
        hidden_dir / "log",
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

    # 创建初始化元数据
    init_meta = {
        "created_at": datetime.now().isoformat(),
        "work_directory": str(work_path),
        "task_root": str(task_root),
        "skill_directory": str(hidden_dir),
        "project_name": work_path.name,
        "version": "0.1.0"
    }

    meta_file = hidden_dir / "input" / "metadata" / "init.json"
    with open(meta_file, "w", encoding="utf-8") as f:
        json.dump(init_meta, f, indent=2, ensure_ascii=False)

    return {
        "status": "created",
        "work_directory": str(hidden_dir),
        "structure": {
            "papers": str(hidden_dir / "input" / "papers"),
            "metadata": str(hidden_dir / "input" / "metadata"),
            "extracted": str(hidden_dir / "output" / "extracted"),
        },
        "message": f"已创建工作目录: {hidden_dir}"
    }


if __name__ == "__main__":
    import sys

    work_dir = sys.argv[1] if len(sys.argv) > 1 else None

    try:
        result = create_work_directory(work_dir)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e)}, indent=2), file=sys.stderr)
        sys.exit(1)
