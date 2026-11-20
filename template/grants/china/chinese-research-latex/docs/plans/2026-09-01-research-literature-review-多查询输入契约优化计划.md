# research-literature-review 多查询输入契约优化计划

## 结论与问题边界

本次异常应按技能设计缺陷处理。阶段 1 当前只有一个未公开的精确文件约定：`output/artifacts/queries_{file_stem}.json`。找不到该文件时，`pipeline_runner.py` 会直接调用单查询 `openalex_search.py`，并把阶段标记为成功；CLI 没有查询文件参数，`SKILL.md` 也没有规定查询文件的生成时机、路径和传递方式。因而即使 AI 已经生成了多查询 JSON，只要路径或命名稍有偏差，多查询意图就会被成功但无感地丢失。

另有一个可复现的命名风险：`PipelineRunner._sanitize_topic_for_filename()` 的空白正则写法错误，含空格主题不会按预期转成连字符；`run_pipeline.py` 又使用了另一套 slug 逻辑，可能进一步造成文件名不一致。

本计划只修复“查询输入交接与降级可见性”，不改变检索供应商、评分、选文和写作策略。

## 目标

1. 让 AI 或用户能够通过显式参数稳定传入查询文件，不依赖猜测内部文件名。
2. 保证查询文件缺失、为空或格式错误时不会无感地降级为单查询。
3. 保留单查询能力，但改为明确授权、可审计的后备模式。
4. 统一主题 slug/文件 stem，兼容历史运行目录和旧文件名。
5. 在状态文件与 Search Log 中记录实际搜索模式、查询来源、查询数量和降级原因。

## 实施步骤

### 1. 建立查询输入契约

- 为 `run_pipeline.py` 和 `pipeline_runner.py` 增加 `--query-file`（别名 `--queries`）参数；必要时提供受控的 `--query-list`。
- 明确 JSON 规范：支持 `{"queries": [{"query": "...", "rationale": "..."}]}`、对象数组和字符串数组；空查询剔除后必须至少保留配置要求的最小数量（默认 5），上限默认 25。
- 显式参数优先于自动发现；参数路径通过现有 `path_scope` 校验，并在启动时解析为绝对路径。
- 查询文件进入当前 run 的 `input` 或 `output/artifacts` 后再使用，或以只读引用方式使用并记录来源；不得跨 run 猜路径。

### 2. 改造阶段 0/1 的编排与失败策略

- 在阶段 0 生成查询计划模板和待填充路径，文档化“先生成并保存查询 JSON，再启动阶段 1”的顺序；如需要交互暂停，增加 `--prepare-only`/`--resume` 的轻量入口，而不让一次命令在未准备输入时直接检索。
- 阶段 1 按以下优先级取源：显式 `--query-file` → 当前 run `input/queries.json` 或 `input/queries_{stem}.json` → 当前 run `output/artifacts/queries_{stem}.json` → 明确标注的历史兼容路径。
- 发现多个候选文件时停止并报告冲突；发现文件但内容无效时停止并给出 schema/路径修复提示。
- 默认改为 fail-closed：无有效多查询输入时阶段 1 失败，不得自动执行单查询。保留 `--allow-single-query-fallback`（或同等命名）作为显式后备开关，并要求在状态与日志中记录授权人机来源、原因和主题。
- 单查询后备只调用一次并使用独立的 `search_mode=single_query` 标记；多查询路径标记为 `search_mode=multi_query`。

### 3. 统一命名与状态审计

- 抽取一个共享的 slug/stem 函数供两个入口使用，修正空白正则（源代码应使用 `r"\s+"`），并为旧文件名提供兼容探测而不再生成新的不一致名称。
- `pipeline_state.json` 增加查询来源、规范化查询数、查询文件 SHA-256（或等价内容指纹）、搜索模式和 fallback 原因字段；resume 时验证输入仍存在且指纹一致，缺失/变更时暂停并要求确认。
- `search_log_*.json` 增加 `search_mode`、`query_source`、`requested_query_count`、`accepted_query_count`、`fallback_reason`，让“499 条来自单查询”一眼可见。
- 阶段完成条件应包含：搜索模式和查询输入已写入日志；若是显式单查询后备，日志必须带警告而不能仅以成功退出码表示正常多查询完成。

### 4. 同步技能说明与配置

- 更新 `skills/research-literature-review/SKILL.md`：给出生成查询 JSON 的确切时机、路径/参数、schema、数量范围和失败处理；删除“AI 自定检索词”但没有落盘协议的歧义。
- 更新 `README.md`、`config.yaml`（查询输入目录、最小/最大查询数、默认是否允许单查询后备）和 `CHANGELOG.md`。
- 按项目指令检查根级 `README.md`、`skills/README.md`、`AGENTS.md`/相关迁移文档中的命令口径；不修改系统级已安装 skill。

### 5. 回归测试与验收

在 `skills/research-literature-review/tests/` 增加不依赖联网的测试夹具，并覆盖：

- 显式 `--query-file` 被读取，且不会调用单查询分支。
- 从 `input/` 与 artifacts 目录自动发现的每种兼容路径均可用。
- 文件名含空格、斜杠、中文和显式 `--output-stem` 时，runner 与生成文件使用同一 stem。
- 缺失、空文件、非法 JSON、零有效查询、少于最小数量、多候选冲突均 fail-closed，并给出可操作错误。
- 未传查询文件时默认不产生单查询结果；带显式 fallback 开关时才运行单查询，并在 state/log 中记录原因。
- resume 能保留查询来源和模式；输入文件被删除或指纹变化时不会静默改跑另一种模式。
- 使用 mock provider 的集成测试验证多查询合并、查询数和 Search Log 字段；固定断言单查询不会得到“伪装成多查询”的成功状态。

验收命令至少包括：

```bash
python -m unittest discover -s skills/research-literature-review/tests -p 'test_*.py'
python -m py_compile skills/research-literature-review/scripts/pipeline_runner.py skills/research-literature-review/scripts/run_pipeline.py skills/research-literature-review/scripts/multi_query_search.py
```

再用一个 3-query mock fixture 做一次完整阶段 0–2 dry run，确认日志明确显示 `multi_query`；用无查询 fixture 验证默认退出并且没有 `papers*.jsonl` 被写成单查询结果。

## 兼容与回滚

- 旧运行目录只在显式 `--resume` 或检测到唯一历史文件时兼容读取；不改变已有论文结果。
- 第一阶段可先以“新增显式参数 + fail-closed 警告 + 日志字段”上线，第二阶段再移除默认自动发现中的旧路径，避免一次升级破坏可恢复运行。
- 若新契约导致外部编排器暂时无法传参，可临时使用显式 `--allow-single-query-fallback`，但该开关必须出现在运行命令和审计日志中。

## 完成定义

- 用户无需猜测 `queries_{file_stem}.json` 的内部命名即可稳定运行多查询。
- 任何多查询输入未被读取的情况都会在阶段 1 阻断或以显眼、可追踪的显式后备记录呈现。
- 测试能证明多查询与单查询两条路径不会互相伪装，且主题命名变化不会导致输入丢失。
- 文档、配置、脚本、测试和变更日志的版本口径一致。
