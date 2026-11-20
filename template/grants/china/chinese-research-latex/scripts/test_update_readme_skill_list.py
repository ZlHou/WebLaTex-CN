from pathlib import Path
import sys

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts import update_readme_skill_list as updater


def write_config(skill_dir: Path, version) -> None:
    """在临时技能目录写入指定版本号的 config.yaml。version 为原始 YAML 字面量。"""
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "config.yaml").write_text(
        f"skill_info:\n  name: {skill_dir.name}\n  version: {version}\n",
        encoding="utf-8",
    )


def test_derive_status_follows_semver_rule():
    assert updater.derive_status("1.0.0") == "✅ 稳定"
    assert updater.derive_status("2.1.0") == "✅ 稳定"
    assert updater.derive_status("0.9.9") == "🚧 开发中"
    assert updater.derive_status("0.0.1") == "🚧 开发中"


def test_load_skill_version_accepts_three_segment_string(tmp_path):
    write_config(tmp_path / "demo-skill", "1.2.3")
    assert updater.load_skill_version(tmp_path / "demo-skill") == "1.2.3"


@pytest.mark.parametrize(
    "version",
    ["1.10", 1.0, '"1.0"', "abc", None],
)
def test_load_skill_version_rejects_non_three_segment(tmp_path, version):
    write_config(tmp_path / "demo-skill", version)
    with pytest.raises(RuntimeError, match="x.y.z"):
        updater.load_skill_version(tmp_path / "demo-skill")


def test_validate_registry_rejects_unregistered_configured_skill(tmp_path):
    write_config(tmp_path / "known-skill", "1.0.0")
    write_config(tmp_path / "ghost-skill", "1.0.0")

    with pytest.raises(RuntimeError, match="ghost-skill"):
        updater.validate_registry(tmp_path, {"known-skill"})


def test_validate_registry_rejects_missing_registered_skill(tmp_path):
    write_config(tmp_path / "known-skill", "1.0.0")

    with pytest.raises(RuntimeError, match="vanished-skill"):
        updater.validate_registry(tmp_path, {"known-skill", "vanished-skill"})


def test_validate_registry_skips_unconfigured_dir_with_warning(tmp_path, capsys):
    write_config(tmp_path / "known-skill", "1.0.0")
    (tmp_path / "legacy-dir").mkdir()
    (tmp_path / "legacy-dir" / "tests").mkdir()

    versions = updater.validate_registry(tmp_path, {"known-skill"})

    assert versions == {"known-skill": "1.0.0"}
    assert "legacy-dir" in capsys.readouterr().out


def test_render_skill_table_covers_all_registered_specs():
    versions = {spec.name: "1.0.0" for spec in updater.SKILL_SPECS}
    table = updater.render_skill_table(versions)

    assert "| 技能 | 阶段 | 版本 | 功能 | 状态 |" in table
    for spec in updater.SKILL_SPECS:
        assert f"[{spec.name}](skills/{spec.name}/)" in table
        assert spec.summary in table
    assert table.count("\n") == len(updater.SKILL_SPECS) + 2


def test_render_skill_table_marks_dev_version_as_in_progress():
    versions = {spec.name: "0.1.0" for spec in updater.SKILL_SPECS}
    table = updater.render_skill_table(versions)

    assert "🚧 开发中" in table
    assert "✅ 稳定" not in table


def test_replace_marked_block_requires_both_markers(tmp_path):
    with pytest.raises(RuntimeError, match="SKILL-LIST"):
        updater.replace_marked_block("no markers here", "table")


def test_update_readme_is_idempotent(tmp_path):
    skills_dir = tmp_path / "skills"
    for spec in updater.SKILL_SPECS:
        write_config(skills_dir / spec.name, "1.0.0")
    readme_path = tmp_path / "README.md"
    readme_path.write_text(
        "<!-- SKILL-LIST:START -->\nold content\n<!-- SKILL-LIST:END -->\n",
        encoding="utf-8",
    )

    assert updater.update_readme(readme_path, skills_dir) is True
    first_pass = readme_path.read_text(encoding="utf-8")
    assert "old content" not in first_pass

    assert updater.update_readme(readme_path, skills_dir) is False
    assert readme_path.read_text(encoding="utf-8") == first_pass
