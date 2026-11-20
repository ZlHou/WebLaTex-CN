# research-literature-review 中间文件隔离优化计划

## 通俗解释：究竟发生了什么

- **一句话说明：** 这次运行把“后厨加工区”和“交给用户的文件架”当成了同一个目录，所以检索证据、字数预算和最终 PDF/Word 一起出现在正式交付目录中。
- **具体场景：** 综述流水线会先产生候选文献、评分结果、证据卡和字数预算，最后才生成 PDF/Word。当前 `work_dir` 既承担流水线工作区，又被当作交付目录；只要调用方把 `--work-dir` 指向正式目录，任何阶段写出的文件都会在那里留下。
- **对应到本问题：** 截图中的 `evidence_cards_*.jsonl`、`selected_papers_enriched_*.jsonl` 和 `word_budget_final.csv` 是后厨文件；`*_review.pdf`、`*_review.docx` 才是最稳定的最终成品。`*_工作条件.md`、`*_验证报告.md`、`.tex`、`.bib` 是否对外提供，应由发布策略决定，而不应与流水线临时文件混在一起。
- **改变前后：** 现在运行结束后需要人工辨认哪些文件能交付；改进后，运行目录只保存内部状态和中间产物，发布目录由程序按白名单复制支持的交付文件，根部出现未授权文件会在导出前被拦截。

## 专业判断：问题在哪里

- **当前现象：** 技能文本要求中间文件进入 `.bensz-api/...`，但同一份技能又要求最终交付物直接放在 `work_dir` 根部，并把字数预算列为“默认交付”。这使“正式交付目录”的边界从定义上就不清楚（见 [`SKILL.md`](../../skills/research-literature-review/SKILL.md#L39)、[`SKILL.md`](../../skills/research-literature-review/SKILL.md#L67)）。
- **路径契约已经分叉：** [`config.yaml`](../../skills/research-literature-review/config.yaml#L284) 把隐藏目录配置为 `output`；[`pipeline_runner.py`](../../skills/research-literature-review/scripts/pipeline_runner.py#L178) 遵循该配置，但 [`organize_run_dir.py`](../../skills/research-literature-review/scripts/organize_run_dir.py#L24)、[`reconcile_state_from_outputs.py`](../../skills/research-literature-review/scripts/reconcile_state_from_outputs.py#L88) 以及工作条件骨架仍写死 `.systematic-literature-review`。整理和恢复因此可能检查错误的目录。
- **工作目录与发布目录耦合：** [`_output_path`](../../skills/research-literature-review/scripts/pipeline_runner.py#L282) 把所有声明为 output 的文件直接写到 `work_dir`；[`run_pipeline.py`](../../skills/research-literature-review/scripts/run_pipeline.py#L28) 默认使用 `runs/<主题>`，显式 `--work-dir` 也没有禁止指向用户正式目录。
- **整理不是可靠门禁：** 自动整理只扫描工作目录根部的有限命名模式，且只按旧目录名移动（见 [`organize_run_dir.py`](../../skills/research-literature-review/scripts/organize_run_dir.py#L41)）；整理失败在 runner 中被标记为“非致命”（见 [`pipeline_runner.py`](../../skills/research-literature-review/scripts/pipeline_runner.py#L915)）。因此“运行成功”不等于“目录干净”。
- **人工交接缺少类别校验：** 评分和写作阶段要求 AI 手动保存文件（见 [`pipeline_runner.py`](../../skills/research-literature-review/scripts/pipeline_runner.py#L489)、[`pipeline_runner.py`](../../skills/research-literature-review/scripts/pipeline_runner.py#L668)），现有路径隔离只限制“不出 work_dir”，没有进一步限制“中间产物必须进 artifacts、可发布文件必须进 deliverables”。

## 要达到什么目标

- **完成后的变化：** 一次运行有唯一的内部工作区和明确的发布目录；所有候选库、评分、选文、摘要补齐、证据卡、字数预算、校验 JSON、状态和日志都只能进入内部目录；发布目录只出现约定的交付文件。
- **兼容性要求：** 旧的 `.systematic-literature-review/` 运行结果仍可显式 resume、整理或迁移；已有 `--work-dir` 用户不应被静默删除或覆盖文件。
- **不在本次处理范围：** 不改变检索源、评分算法、选文策略、综述正文质量规则或 PDF/Word 内容；不自动删除历史运行目录；不把所有审计材料强行丢弃。

## 改进方向

### 方向一：建立布局单一真相，并拆开内部运行与对外发布

以 `config.yaml:layout` 为唯一布局来源，定义 `workspace_root`、`artifacts`、`reference`、`cache`、`scripts`、`state` 和 `deliverables` 的职责；runner、整理器、状态恢复器、成本追踪和各脚本都通过同一解析函数取路径，不再出现字符串形式的 `.systematic-literature-review`。内部运行目录默认由 `run_pipeline.py` 创建在当前任务的 `.bensz-api/task-.../research-literature-review/<run-id>/` 下，避免把用户指定的正式目录直接当作 `work_dir`。

新增显式 `--publish-dir`（或等价配置）作为发布目标。导出阶段先在内部 `deliverables/` 生成文件，再将白名单文件原子复制到发布目录：默认至少包含 PDF/Word；`.tex`、`.bib`、工作条件和验证报告作为可选“源码/审计包”按现有兼容承诺提供，但不再与中间产物共用根目录。这样既保留可复核材料，又不会让证据包伪装成最终交付物。

### 方向二：把路径分类变成可执行门禁，而不是事后整理

为每个阶段提供统一的路径工厂和文件类别（`artifact`、`reference`、`state`、`log`、`deliverable`）。阶段 3 的评分文件、阶段 4 的选文与 rationale、阶段 4.5 的三次预算和 final、阶段 5 的 enriched/evidence cards、阶段 6 的 counts JSON 均只能写入内部目录；只有经过验证的 `.tex`、`.bib`、PDF、DOCX 及被允许的报告才能进入 `deliverables/`。

将人工交接提示改成“给出绝对目标路径 + 写入后立即校验”，对越级写入直接报错并提示正确路径。导出前运行严格的根目录检查，检查失败则停止发布；导出后的整理器只作为旧运行迁移工具，不再承担保证正确性的主职责。整理器应读取配置、递归发现已知泄漏文件、显式报告冲突，不能静默跳过；恢复脚本也必须同时支持新布局和显式 legacy 模式。

### 方向三：同步契约、迁移工具和用户说明

统一 `SKILL.md`、`README.md`、配置注释、工作条件骨架路径、CHANGELOG 和维护者命令：明确“内部工作区”“交付目录”“支持性审计包”三种概念，并删除仍指向 `runs/<主题>` 或旧隐藏目录的默认示例。为历史实例提供 dry-run/`--apply` 迁移命令，迁移前生成清单和冲突报告，迁移后保留原文件不覆盖已有目标。

## 实施范围与顺序

1. 先实现布局解析器、路径工厂和 `workspace_root`/`publish_dir` 数据模型，更新 `pipeline_runner.py` 与 `run_pipeline.py` 的默认路径和 CLI；这是后续阶段都必须依赖的边界。
2. 再把所有阶段输出改接到分类路径，加入导出前严格清洁门禁和导出后白名单发布；同时改造 `organize_run_dir.py`、`reconcile_state_from_outputs.py`、`pipeline_cost.py` 使用同一配置，并保留显式 legacy 读取。
3. 最后同步技能文档、示例、CHANGELOG 与迁移说明，补齐自动化回归和一份包含截图中三类文件的泄漏样例；确认默认运行和显式发布运行都遵循同一规则。

## 如何确认完成

- **布局一致性：** 在临时运行中读取配置后，runner、整理器、恢复器和成本脚本解析出的内部目录完全相同；代码与文档不再出现未经说明的硬编码旧目录。
- **泄漏拦截：** 故意把 `evidence_cards_*.jsonl`、`selected_papers_enriched_*.jsonl` 或 `word_budget_final.csv` 写到发布目录，严格门禁必须失败并给出目标路径；把它们写到内部 artifacts 后，运行通过。
- **发布白名单：** 成功运行后，发布目录只包含约定的 PDF/Word 及用户选择的源码/审计包；`papers*.jsonl`、评分、选文、证据卡、预算 CSV 和状态文件不出现。
- **流程回归：** 覆盖全新运行、阶段 3/5 人工交接、`--resume-from`、PDF/Word 导出失败、重复发布目录、旧 `.systematic-literature-review` 迁移和已有文件冲突；任何发布失败都不能返回成功状态。
- **目录清洁：** 使用 [`validate_workdir_cleanliness.py`](../../skills/research-literature-review/scripts/validate_workdir_cleanliness.py) 的严格模式验证内部/发布目录，并将测试产物放在 `tests/` 子目录而非仓库根目录。

## 风险与待确认事项

- 需要确认“默认正式交付”是否仍包含 `.tex`、`.bib`、工作条件和验证报告。计划建议保留它们作为可选支持包，默认把 PDF/Word 作为发布根部的核心文件，以兼容现有用户对可复核材料的需求。
- 用户显式指定的发布目录可能已有同名文件；默认应拒绝覆盖并报告冲突，只有显式 `--force`（并记录清单）才允许替换。
- 旧运行目录的路径和状态字段可能混用相对路径；迁移/恢复必须先解析并校验路径，再写入新 state，不能通过空 state 覆盖历史进度。
