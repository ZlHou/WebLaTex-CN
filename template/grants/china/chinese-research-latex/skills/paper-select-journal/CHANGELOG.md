## [Unreleased]

### Changed
- 加强工作区边界约束：`shortlist_journals.py`、`fetch_pubmed_recent.py`、`render_report.py` 现在会拒绝读取 run 目录之外的关键 JSON，并确保生成文件始终写回当前 workspace，避免中间产物和最终报告越界散落
- `fetch_pubmed_recent.py` 修正 PubMed 文本月份解析，`Mar` 等月份缩写现在会归一化为 `YYYY-MM-DD`，避免近期论文按字符串排序时出现日期错序
- `shortlist_journals.py` 对非正数 `limit` 改为显式报错，不再默默接受 `0` 或负数造成候选截断异常
- `scripts/common.py` 删除上一版语义打分遗留的无效 token 工具函数，并补充工作区路径校验辅助函数，减少“文档已改、底层工具仍保留旧设计”的漂移
- `config.yaml` 补充 `directories.plans/tests` 与 `reports.manuscript_profile/scope_review/final_json`，将测试目录和关键工作文件路径进一步集中化，并将技能版本号 `0.3.0 → 0.3.1`
- `SKILL.md` 与 `README.md` 同步补充 run 目录内 JSON/报告路径约束，以及低 IF 人工例外的使用边界，避免说明与脚本行为不一致
- 将 Set1 从“硬编码语义打分 shortlist”调整为“最小硬过滤候选池 + 宿主模型自主规划”：`shortlist_journals.py` 不再依赖固定关键词/字段权重，而是只保留 IF、排除名单、分区、OA 比例等确定性整理；Set2/Set3 的语义去留继续交给当前 Claude Code / Codex 会话判断
- `config.yaml` 删除已不再需要的 `matching.*` 语义打分配置，并将技能版本号 `0.2.2 → 0.3.0`
- `templates/manuscript_profile.template.json`、`references/manuscript-profile.md`、`SKILL.md` 与 `README.md` 改为鼓励使用简洁自然语言画像，不再要求为了脚本打分而拆很多 `field_hints / method_terms / application_terms`
- `tests/unit/test_shortlist_journals.py` 改为验证最小硬过滤、显式排除与人工例外行为，不再绑定旧的语义打分公式

## [0.2.2] - 2026-04-05

### Changed
- 压缩 `SKILL.md` 与 `references/*.md` 的工作型 Markdown 表达，去掉重复铺垫，保留触发语义、Set1→Set3 流程、关键命令、输出文件名与 Step 4b 必须由当前宿主模型原生完成的边界

## [0.2.1] - 2026-04-05

### Changed
- `SKILL.md` 与 `README.md` 明确 Step 4b 的 AI 评定必须由当前宿主环境中的模型原生完成，也就是 Claude Code / Codex 当前会话自身承担规划与语义判断
- `plans/v20260405190757.md` 同步补充“AI 算力来自 skill 工作环境、不额外调用外部 AI API”的设计边界，避免把 Step 4b 误解为需要另起模型服务

## [0.2.0] - 2026-04-05

### Added
- 新增 `paper-select-journal` skill：支持从 manuscript 生成语义画像、基于内置 `2023IF.xlsx` 进行 Set1 初筛、对 Set2 期刊批量抓取最近 3 个月 PubMed 论文，并把最终推荐渲染成单一 Markdown 报告

### Changed
- `render_report.py` 的最终推荐数量上限改为读取 `config.yaml:screening.default_set3_limit`，不再硬编码 `10`
- `SKILL.md` 与 `README.md` 的脚本示例统一改为 `<skill_root>/scripts/...` 口径，避免系统级安装后路径误导
- `fetch_pubmed_recent.py` 的中间 Markdown 标题从“Set3”修正为“Set2 PubMed 近 3 个月论文证据”，与实际阶段一致

### Fixed
- 修复 PubMed 批量检索在单刊失败时会中断整批流程的问题，改为逐刊记录 `error` 并继续
- 修复 `shortlist_journals.py` 中 manual exception 评分未复用主 profile、去重逻辑可能覆盖更优候选的问题
- 修复最终报告未过滤空期刊名的问题，并补充对应单元测试
- 清理 `.DS_Store`、`__pycache__` 与 fixture 隐藏工作区运行产物，并在 `.gitignore` 中新增 `paper-select-journal` fixture 隐藏工作区忽略规则

### Added
- 新增 `templates/set3_similarity_review.template.json`，用于承载 AI 对 Set2→Set3 的语义相似性评估结果

### Changed
- `fetch_pubmed_recent.py` 不再使用硬编码 token 重叠公式计算相似度，改为只抓取和整理 PubMed 原始论文证据，并按发表日期降序输出
- `SKILL.md` 的 Step 4 拆分为 4a（脚本抓取原始 PubMed 证据）和 4b（AI 语义评定 Set3），并新增 `set3_similarity_review.json` 工作流说明
- `final_recommendations.template.json`、`render_report.py` 与 `report-schema.md` 改为展示每篇证据论文的 AI `relevance`，不再依赖脚本分数
- `README.md` 同步更新为“脚本抓取 + AI 语义判断”的新流程说明
- `config.yaml` 删除不再需要的 PubMed 硬编码相似度权重，并新增 `reports.set3_similarity_review`

## [0.1.0] - 2026-04-05

### Added
- 初始版本：新增 `SKILL.md`、`README.md`、`config.yaml`、`assets/journal_catalog/2023IF.xlsx`
- 新增 `scripts/init_workspace.py`、`scripts/shortlist_journals.py`、`scripts/fetch_pubmed_recent.py`、`scripts/render_report.py`
- 新增 `templates/*.json` 与 `references/*.md`，用于稳定输出 `manuscript_profile.json`、`set2_scope_review.json` 与 `final_recommendations.json`
- 新增 `tests/unit/` 单元测试与 `tests/paper-select-journal/` 轻量测试夹具
