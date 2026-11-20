#!/usr/bin/env python3
"""统一解析 research-literature-review 的运行目录布局。"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping


@dataclass(frozen=True)
class LayoutPaths:
    work_dir: Path
    hidden_dir: Path
    artifacts_dir: Path
    reference_dir: Path
    cache_dir: Path
    scripts_dir: Path
    deliverables_dir: Path
    supporting_dir: Path

    @classmethod
    def from_config(cls, work_dir: Path, config: Mapping[str, Any] | None = None) -> "LayoutPaths":
        root = Path(work_dir).expanduser().resolve()
        layout = (config or {}).get("layout", {}) if isinstance(config, Mapping) else {}
        hidden_name = str(layout.get("hidden_dir_name", ".systematic-literature-review"))
        artifacts_name = str(layout.get("artifacts_dir_name", "artifacts"))
        reference_name = str(layout.get("reference_dir_name", "reference"))
        cache_name = str(layout.get("cache_dir_name", "cache"))
        scripts_name = str(layout.get("scripts_dir_name", "scripts"))
        deliverables_name = str(layout.get("deliverables_dir_name", "deliverables"))
        supporting_name = str(layout.get("supporting_dir_name", "supporting"))
        hidden = root / hidden_name
        return cls(
            work_dir=root,
            hidden_dir=hidden,
            artifacts_dir=hidden / artifacts_name,
            reference_dir=hidden / reference_name,
            cache_dir=hidden / cache_name,
            scripts_dir=hidden / scripts_name,
            deliverables_dir=hidden / deliverables_name,
            supporting_dir=hidden / deliverables_name / supporting_name,
        )

    @property
    def state_file(self) -> Path:
        return self.hidden_dir / "pipeline_state.json"

    def ensure(self, cache_enabled: bool = False) -> None:
        for directory in (
            self.work_dir / "input",
            self.work_dir / "log",
            self.hidden_dir,
            self.artifacts_dir,
            self.reference_dir,
            self.scripts_dir,
            self.deliverables_dir,
            self.supporting_dir,
        ):
            directory.mkdir(parents=True, exist_ok=True)
        if cache_enabled:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
