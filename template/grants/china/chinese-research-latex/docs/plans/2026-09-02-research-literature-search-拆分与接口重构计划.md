# research-literature-search 拆分与接口重构实施计划

> 状态：实施中（已完成 search skill 骨架、manifest/candidate 契约、review resolver 与阶段 1/2 适配；当前继续补齐安全门禁、兼容 wrapper 和回归验证）。
>
> 目标：从现有 `research-literature-review` 中抽出可独立复用的文献检索能力，新增 `research-literature-search` skill；`research-literature-review` 的名称、用户入口和综述功能保持不变，但强制通过新检索 skill 获取候选文献。

## 通俗解释：究竟发生了什么

- **一句话说明：** 现在“找文献”和“写综述”共用一条流水线，其他任务想只找文献时必须加载整套综述流程；本次要把找文献做成一个有固定交接单的独立环节。
- **生活类比或具体场景：** 把检索 skill 看成仓库的“配货中心”，把综述 skill 看成“组装车间”。配货中心负责从多个供应商找货、核对编号、去掉重复货物并附上来源单；组装车间只接收符合格式的货物，负责分拣、组装和出厂。以前这些工作挤在同一间车间里，其他车间想取货只能连整条生产线一起借用。
- **对应到本问题：** “货物”是候选论文，“来源单”是查询、provider、排名、时间和去重记录；`manifest.json` 是交接单，规定文件在哪里、数量是多少、是否有截断或失败，以及下游能否安全使用。
- **改变前后：** 现在综述阶段 1/2 直接调用内部检索和去重脚本；改造后，综述阶段先调用 `research-literature-search`，校验 manifest 和候选池，再继续使用原有评分、选文、字数预算、写作、验证和 PDF/Word 导出链路。用户仍可用 `research-literature-review` 原名和旧 CLI；需要只搜文献的用户可以直接调用新 skill。

## 专业判断：问题在哪里

### 当前现象

当前综述流水线把检索分布在多个位置：阶段 1 由 `multi_query_search.py` 负责多查询、provider 降级和搜索日志，阶段 2 再由 `dedupe_papers.py` 做一次更深的去重；摘要补全又在选文后由 `multi_source_abstract.py` 完成。`pipeline_runner.py` 还直接管理查询文件、状态字段、旧目录兼容和后续阶段的文件名。

现有实现已有可复用能力，但交接协议不完整：不同 provider 的字段不完全一致，简易去重与深度去重存在两套逻辑，Search Log 缺少部分复现和截断信息，且 `mcp`/`duckduckgo` 在纯 Python runner 中实际上需要宿主工具而不是本地实现。

### 影响范围

- 想只获得候选文献池、做研究选题或为 NSFC 准备证据的调用方，必须理解综述 skill 的写作和导出流程。
- 综述 skill 若继续内嵌 provider 和去重实现，检索规则被复用到不同场景时容易发生复制、漂移和行为不一致。
- 如果直接替换现有文件而没有版本化交接协议，旧的 `pipeline_state.json`、`papers*.jsonl`、Search Log 和 resume 流程可能无法恢复。

### 已知事实与待验证假设

- **已知事实：** 当前多查询输入契约已经规定有效查询默认 5–25 条、fail-closed、查询文件 SHA-256 和 Search Log 审计字段；该契约应被外提继承，而不是重新发明第二套格式。
- **已知事实：** 综述下游读取 `title/doi/abstract/venue/year/url/authors/authorships/source` 等旧字段；新规范必须提供兼容映射或保留兼容视图。
- **已知事实：** 当前默认摘要补全在选文后执行；本次不能把它改成对全量候选强制补全，否则会改变耗时、请求量和可能的选文结果。
- **待验证假设：** 独立安装环境能否稳定发现新 skill，需要通过本地项目路径、显式参数、环境变量和用户 skill 根目录逐级解析，并用离线测试覆盖。

## 要达到什么目标

### 完成后的变化

1. 新增 `research-literature-search`，能独立完成“查询输入 → 多源检索 → 规范化 → 去重 → 审计输出”，并能被其它 skill 复用。
2. 新 skill 对外提供版本化、可校验、可追溯的 manifest 和候选文献契约；下游不再猜测文件名或 provider 字段。
3. `research-literature-review` 保留原名、原有用户入口和全部综述功能，且阶段 1/2 强制消费新检索契约。
4. 旧的 `--query-file`、单查询显式后备、旧输出文件名、旧 checkpoint/resume 和直接脚本入口保持兼容；兼容路径必须可审计，不能静默改变检索模式。
5. 在固定离线夹具上，新旧综述链路的评分输入、选文、BibTeX、PDF/Word 和验证结果保持功能等价；允许新增来源审计字段和更明确的 warning，但不能无说明地改变候选集合。

### 不在本次处理范围

- 不更改 `research-literature-review` 的名称，不移除旧名 `systematic-literature-review` 的 prompt 兼容，不迁移历史 `.systematic-literature-review/` 目录。
- 不在本次重构中新增 arXiv、IEEE Xplore 或其它 provider；新契约应允许未来添加这些 provider，但 provider 扩展另做计划。
- 不把 AI 相关性评分、纳入/排除判断、子主题分组、参考文献配额、字数预算、综述写作、BibTeX 生成和 PDF/Word 导出放入 search skill。
- 不把 search skill 产物直接改造成正式发布物；检索产物是供下游消费的内部证据包，正式综述交付规则继续由 review skill 管理。
- 不修改系统级 `~/.codex/skills/` 或 `~/.claude/skills/` 中的已安装文件；上游安装器和技能清单只作为发布同步项处理。

## 改进方向

### 方向一：建立唯一的检索 skill 和版本化交接契约

新增 `research-literature-search`，让它成为检索实现的唯一归属。它负责查询契约、provider 适配、分页、限流、缓存、来源降级、元数据规范化、预印本识别、去重、可选摘要补全和审计；代码只保留一份，旧脚本改为薄 wrapper 或兼容入口。

新 skill 的默认截断点是“去重后的 canonical 候选池”。它不决定哪些论文最终进入综述，也不生成选文理由或正文。

拆分首个稳定版本时增加“行为锁定模式”：默认复现当前 `multi_query_search.py` 的 provider 选择和结果合并语义——OpenAlex 为主力，结果不足时按现有规则做 Semantic Scholar 补充，Crossref 作为降级，MCP/`duckduckgo` 在纯 Python 环境中仍显式 skipped；不把拆分顺手改成所有 provider 结果的无条件 union。未来若要引入 union 或新的召回策略，必须另设 provider policy/版本并单独做结果变更评估。

#### 对外输入契约

新 skill 提供稳定的 `run` 命令（具体脚本名在实现阶段确定，但 CLI 语义固定），至少接受：

- `topic`、可选 `domain`；
- 显式 `query-file`（别名 `queries`），继续支持当前三种 JSON 形态：`{"queries": [...]}`、对象数组、字符串数组；
- 查询数量默认 5–25，空项剔除后不足或超限直接失败；
- `filters`：年份、文献类型、语言、开放获取和预印本策略等；
- `provider policy`：请求顺序、允许的 provider、降级开关和每查询/总结果上限；
- 输出目录和任务级 scope root；不得允许路径穿越或把结果写到工作区之外；
- 可选缓存、礼貌延迟和摘要补全模式。

查询在内部规范化为带稳定 `query_id`、顺序号、查询文本和 rationale 的 QueryPlan。查询文件 SHA-256、规范化数量和来源写入 manifest；不得仅凭“返回结果很多”推断多查询成功。

#### 对外输出契约

每次 `run` 生成一个独立的检索输出目录，至少包含：

```text
manifest.json              # 唯一入口和交接单
candidates_raw.jsonl       # provider 原始命中，供审计，不供下游直接消费
candidates_normalized.jsonl
candidates_deduped.jsonl   # canonical 候选池，下游默认读取
provenance.jsonl            # 原始命中到 canonical 的来源/查询/排名映射
dedupe_map.json             # 合并边与 canonical 选择理由
search_log.json             # 面向人阅读的兼容日志
```

`candidates_deduped.jsonl` 每行遵守版本化 paper schema。第一版建议使用 `rls.paper.v1`，包含以下语义：

`candidates_raw.jsonl` 不要求保存完整 API 原始响应；可以保存经过脱敏的最小原始命中信封（provider、provider record id、query id、rank 和原始字段快照）。这样既保持 `cache.mode=minimal` 的磁盘策略，也让规范化和去重过程有可定位的输入证据。

- `record_type`、`schema_version`、稳定 `record_id`；
- 非空 `title`；`authors` 为字符串数组，允许保留原始 `authorships` 扩展；
- `identifiers` 对象，至少规范化 `doi`，并为 `pmid/arxiv/openalex/semantic_scholar` 等保留可空位置；
- `venue`、`year`、可选的 `published_date/online_date`、`url`；缺失使用 `null` 或 `[]`，不使用虚构占位文本；
- `abstract` 和 `abstract_status`；若补全过，写入 `abstract_provenance`（来源、方法、时间、尝试次数）；
- `publication` 对象，包含 `publication_type`、`is_preprint`、`preprint_server`、`peer_reviewed` 和版本信息（未知值允许为 `null`）；
- `sources`/`provenance`，记录 provider、provider record id、首次命中时间、对应 query id、原始排名和来源 URL；
- `query_matches`、`quality_warnings` 等可审计扩展。

为保证现有下游稳定，规范候选同时提供兼容的扁平字段视图（`doi/abstract/venue/year/url/authors/source` 等）；规范字段是新代码的唯一读取口径，兼容字段只由边界适配器和旧 wrapper 使用。OpenAlex 也必须补出统一的 provider 标识，不能因 provider 差异让 `source` 有时缺失。

canonical candidate validator 必须严格检查 `rls.paper.v1`；旧 `papers*.jsonl` 或旧 checkpoint 中只有 `title/year/id` 等最小字段的记录，必须经过明确的 legacy adapter 补齐为 `null/[]` 后再消费，并保留 `legacy_adapted` 警告，不能把宽松旧记录冒充新契约。

`manifest.json` 至少包含：

- `contract_version`、`candidate_schema_version`、`search_skill_version`、`search_run_id`；
- topic/domain（必要时附 topic hash）、规范化 query plan、query file SHA-256、请求数/接受数；
- 生效的 filters、provider 顺序、provider 配置指纹（去除密钥）、每查询/每 provider 的 attempts；
- `counts.raw/normalized/deduped`、各阶段失败数、截断是否发生及 `dropped_count`；
- 去重参数、`dedupe_map` 路径和 canonical 选择统计；
- 摘要补全模式、尝试数、成功数、失败数和缺失摘要警告；
- 所有产物相对于 manifest 的安全相对路径；
- `status`、`failure_code`、`warnings`、`created_at`、缓存模式和可复现性信息。

状态语义固定为：

- `success`：契约有效并生成完整 canonical 候选池；
- `partial_success`：至少有可用候选，但存在 provider 失败、跳过、截断或字段缺失，所有问题都在 manifest 中列出；
- `failed`：输入契约错误、路径违规、所有 provider 不可用或没有可消费候选。

`failure_code` 细分 `contract_invalid/no_provider/path_violation/manifest_invalid` 等。综述 skill 只接受 `success` 或 `partial_success`，并要求 manifest、canonical 候选和 hash 校验全部通过。

输出必须使用 UTF-8、稳定 JSON 序列化和确定性排序（例如首次命中顺序再加 `record_id`），使相同夹具和配置可比较。`provenance.jsonl` 要能回答“这篇论文来自哪个 provider、哪个 query、原始排名多少、是否与另一条记录合并”。

### 方向二：把摘要补全和检索扩展做成可选子命令，不污染主边界

新 skill 提供独立的 `enrich-abstracts` 能力，复用当前 Crossref → Semantic Scholar → PubMed → OpenAlex-by-DOI 的顺序和统计，但默认 `run` 不对全量候选做强制补全。综述 skill 在选文后继续调用该能力，保持当前 `post_selection` 时机、上限、重试和缺失摘要 warning 不变。

未来的 citation chasing、arXiv/bioRxiv/medRxiv 补充和全文获取也应通过独立、可审计的扩展模式接入，不改变 `run` 的基础候选 schema。全文下载和版权边界不在本次计划内。

### 方向三：让 review skill 成为新检索 skill 的强制消费者

`research-literature-review` 继续使用原名，但在依赖元数据和执行门禁中声明 `research-literature-search` 为必需依赖，并校验兼容的 contract version。

#### Review 的新消费方式

1. 阶段 0 继续提供原有主题、档位和查询模板体验；查询契约的实现归属 search skill，review 只保留兼容转发。
2. 阶段 1 不再直接拥有 provider 逻辑，调用 search skill 的 `run`，接收 manifest 和候选产物。
3. 阶段 1 将 search 输出的 manifest、canonical 候选和必要的 provenance 以只读输入包形式放入当前任务的 review `input/`，同时把源路径、文件 hash 和 contract version 写入 `pipeline_state.json`。
4. 阶段 2 保留 `2_dedupe` 阶段名称和 checkpoint 语义，但只做 manifest/候选完整性验证及旧文件名映射，不再次执行另一套去重。对新运行不得出现二次 canonical 变化。
5. 阶段 3 以后通过适配器读取规范候选，并继续生成原有 `scored_papers.jsonl`、`selected_papers.jsonl`、`references.bib`、工作条件、字数预算、正文、验证报告、PDF 和 Word。
6. 阶段 5 选文后仍调用 search skill 的 `enrich-abstracts`（或同一实现的兼容 wrapper），保持当前摘要补全时机和写作证据卡行为。
7. `Search Plan`、`Search Log` 和工作条件中的检索统计由 manifest/适配器自动填充；AI 不再手写 provider 次数、候选数量或去重结论，避免审计字段遗漏。

#### Search skill 的发现与失败策略

为支持独立安装，review 优先按以下顺序寻找 search skill：显式 `--search-skill-root` → 项目内 `skills/research-literature-search` → 显式环境变量 → 用户 skill 根目录。发现不到 skill、版本不兼容、manifest 无效或 hash 不一致时必须 fail-closed，并给出安装/修复指引。

迁移期间可保留显式的 `--legacy-local-search` 诊断开关，仅用于旧环境或回滚演练；该路径必须写入 `search_mode/provider/contract_version` 警告，不能成为默认隐式 fallback。旧 checkpoint 若已有合法候选和可验证的旧 Search Log，可通过 legacy adapter 继续恢复；一旦需要重新检索，应走新 search skill。

#### 任务工作区边界

一次协作任务只使用一个 `.bensz-api/task-*` 根目录。search 和 review 各自有独立 skill 子目录；review 不直接读取另一个 run 的任意文件，而是接收 search 生成的 manifest bundle，并在自己的 `input/search-contract/` 中保留只读副本或受控引用和来源说明。这样既保持 skill 边界，也使 resume、审查和清理可追溯。

### 方向四：以兼容 wrapper 和适配器保住现有用户入口

- 保留 `run_pipeline.py` 的现有 CLI（包括 `--query-file/--queries`、显式单查询后备、`--resume`、`--resume-from`、发布目录参数等），只改变其内部阶段 1 的实现。
- `multi_query_search.py`、`openalex_search.py`、`dedupe_papers.py` 等直接调用入口改成薄 wrapper，继续接受旧参数、返回码和主要文件名，但内部委托新 search 实现；不复制 provider 或去重逻辑。
- 继续生成或受控映射旧文件名：`papers_{stem}.jsonl`、`papers_deduped_{stem}.jsonl`、`search_log_{stem}.json`、`dedupe_map_{stem}.json`，并在 manifest 中说明它们对应 raw/normalized/canonical 哪一层。
- 旧 `papers_{stem}.jsonl` 固定映射为“provider 合并后、深度模糊去重前”的 normalized 视图（保留当前阶段 1 的早期精确去重语义）；旧 `papers_deduped_{stem}.jsonl` 固定映射为 search 输出的 canonical deduped 视图。review 的新阶段 2 只验证后者，旧 standalone `dedupe_papers.py` 对 legacy 调用保持幂等。
- 旧 `pipeline_state.json` 字段 `search_mode/query_source/requested_query_count/accepted_query_count/query_file_sha256/fallback_reason` 必须继续可读；新状态增加 `search_manifest`、`search_contract_version`、`search_manifest_sha256` 和候选 hash 等字段。
- 兼容 `search_log_{stem}.json` 顶层至少继续提供现有的 `search_mode/query_source/requested_query_count/accepted_query_count/fallback_reason`；这些字段由 manifest 单向生成，避免新旧日志出现两套事实。
- 旧 `.systematic-literature-review` checkpoint 和历史 stem 仅用于显式 resume/兼容读取，不生成新的旧目录或旧命名。

### 方向五：明确实现归属，避免“拆成两份”

目标目录只表达职责，不要求一次提交机械搬运所有文件；实现时应先抽取共享核心，再让旧入口转调：

```text
skills/research-literature-search/
├── SKILL.md / README.md / config.yaml / CHANGELOG.md / requirements.txt
├── references/
│   ├── paper-schema.md
│   ├── bundle-schema.md
│   └── provider-guide.md
├── scripts/
│   ├── search_runner.py          # run / enrich-abstracts / validate 的编排
│   ├── query_contract.py         # QueryPlan、stem、输入 hash
│   ├── candidate_schema.py       # candidate 与 manifest validator
│   ├── normalize_papers.py       # provider → canonical record
│   ├── providers/                # OpenAlex/Semantic Scholar/Crossref/MCP adapter
│   ├── dedupe_papers.py          # DOI、标题年份、预印本 canonical
│   ├── multi_source_abstract.py  # 可选摘要补全
│   └── manifest.py / validate_bundle.py
└── tests/fixtures/               # 离线 provider、坏输入和 golden bundle
```

`research-literature-review/scripts/` 中现有同名检索、去重和摘要脚本在过渡期保留为 deprecated wrapper；它们只负责旧参数解析、调用新 CLI、生成旧文件别名和返回旧退出码，不得继续承载独立业务逻辑。评分、选文、字数、写作、导出脚本继续留在 review skill。

## 实施范围与顺序

### 1. 冻结基线，先把接口写成可测试的规范

先以当前测试夹具和一个代表性综述运行记录建立 golden baseline，记录候选计数、去重映射、评分输入、选文集合、BibTeX key、字数预算和最终 PDF/Word 的可观察结果。同步确认 2026-09-01 多查询输入契约作为前置设计被继承。

然后实现独立的 schema/manifest validator 和版本兼容判断；先验证坏字段、坏类型、缺文件、数量越界、hash 改变、路径越界和重复 `record_id` 都能在下游消费前阻断。

基线对比必须按层记录：query plan、provider attempts、raw/normalized/deduped 的 paper id 顺序、dedupe canonical 与合并边、review 评分输入、selected id、BibTeX key、字数预算和最终导出。允许新 bundle 多出 provenance/manifest 字段，但在默认行为锁定模式下不允许候选或排序无说明地变化。

### 2. 创建新 skill 骨架并外提唯一实现

新增 `skills/research-literature-search/` 的 `SKILL.md`、`README.md`、`config.yaml`、`CHANGELOG.md`、最小 `requirements.txt`、scripts、references 和 tests。将查询契约、provider adapters、限流/缓存、规范化、去重、来源追踪和摘要补全整理到新 skill；review 侧不保留第二份实现。

新 skill 至少提供 `run` 和 `enrich-abstracts` 两个稳定入口，并让 provider 配置区分“检索来源”和“摘要补全来源”。对当前 `mcp/duckduckgo` 的宿主依赖、实际跳过和 warning 语义如实记录。

### 3. 实现 manifest bundle 和兼容输出

实现 raw → normalized → deduped 三层产物、canonical `record_id`、预印本—正式版合并、provenance、dedupe map、确定性排序、截断统计和完整 Search Log。加入旧字段兼容视图，但新下游只读规范字段。

摘要补全默认保持可选；实现 `enrich-abstracts` 后，验证它能生成与当前 selected 后补全等价的 `abstract_status/quality_warnings` 和统计信息。

### 4. 改造 review 的依赖解析和阶段适配

在 review 中加入 search skill resolver、manifest validator 和 contract adapter。阶段 1 只调用新 search `run`；阶段 2 改为验证和映射，不重复去重；阶段 3–7 的业务逻辑尽量不动。对旧 checkpoint、旧文件名和旧 standalone CLI 提供只读 adapter/wrapper。

把新 search 的 manifest hash、候选 hash、contract version 和 source path 写回 review state，并在 resume 时拒绝缺失、篡改或版本不兼容的输入。缺 search 时默认明确失败，不以旧内联逻辑静默替代。

依赖元数据可沿仓库已有 `metadata.dependencies.required` 风格声明：依赖名为 `research-literature-search`，同时声明最小兼容 contract（而不只绑定某个脚本文件版本）。review 启动时先做依赖发现和版本检查，再准备阶段 0/1；失败应在真正发起检索前返回可操作的安装提示。

### 5. 同步文档、版本和安装说明

更新新 skill 自身文档；更新 `research-literature-review` 的 SKILL/README/config/CHANGELOG，说明必需依赖、接口消费方式、旧命令兼容和 fail-closed 策略。同步检查根 `README.md`、`skills/README.md`、根 `CHANGELOG.md`、技能依赖图和推荐工作流。

检查 `research-topic-extractor`、`research-idea`、`research-citation-check`、`nsfc-justification-writer` 等对综述产物或旧 marker 的引用：只在实际依赖边界发生变化处更新，不把 search 产物强行接入不相关的渲染或只读检测流程。外部 `install-bensz-skills`/上游技能清单列为发布同步项，确保 search 能被独立安装且 review 的必需依赖会一并安装。

### 6. 分阶段启用、回归和稳定化

先允许新 search skill 独立运行并通过离线契约测试；再让 review 默认消费新 manifest；最后在一个弃用周期后评估是否移除旧内联实现。迁移期间保留显式 legacy 开关和 wrapper，不删除用户已有文件，不覆盖旧 checkpoint。

若发现结果差异，优先比较 raw/normalized/deduped、manifest、provenance 和 dedupe map，定位是 provider、规范化、去重还是适配器变化；不能用“重新检索一次”掩盖差异。

## 技术补充（接口与验收细节）

### 生产者—消费者接口摘要

| 项目 | `research-literature-search`（生产者） | `research-literature-review`（消费者） |
| --- | --- | --- |
| 输入 | topic、QueryPlan、filters、provider policy、输出目录 | 用户主题/档位/查询文件；search skill root 或 resolver 配置 |
| 主要动作 | 检索、规范化、去重、来源追踪、可选摘要补全 | manifest 校验、评分、选文、证据整合、写作和导出 |
| 主交接物 | `manifest.json` + `candidates_deduped.jsonl` + provenance/map | review `input/search-contract/` 中的只读 bundle 与 hash |
| 成功门槛 | contract 有效、候选可读、状态为 success/partial_success | contract 兼容、manifest/hash/候选通过校验 |
| 禁止承担 | AI 相关性判断、最终选文、Bib/正文/PDF | 私自调用 provider、二次改变 canonical 去重结果 |
| 失败策略 | `failed` + failure_code + attempts/warnings，非零退出 | 缺依赖/版本/hash/产物时 fail-closed；仅显式 legacy 模式可回退 |

### 建议的 manifest 最小结构

```text
contract_version
candidate_schema_version
search_skill_version
search_run_id
topic / domain / topic_hash
query_plan {source, sha256, requested_count, accepted_count, items[]}
filters
provider_policy {requested_order, effective_order, config_fingerprint}
attempts[]
counts {raw, normalized, deduped, failed, dropped}
truncation {applied, limit, dropped_count}
dedupe {parameters, map_path, cross_doi_preprint_merges}
abstract_enrichment {mode, attempted, filled, missing, warnings}
artifacts {candidates_raw, candidates_normalized, candidates_deduped, provenance, dedupe_map, search_log}
status / failure_code / warnings
created_at / cache
```

manifest 中的 artifact 路径必须是相对自身目录的安全路径；review 解析后再把它们复制到自己的输入边界，不能信任 manifest 提供的任意绝对路径。

### 验收矩阵

#### Search-only

- 正常 5–25 查询生成完整 manifest、canonical candidates、provenance 和 dedupe map；JSON schema、稳定排序和 hash 校验通过。
- OpenAlex 成功、OpenAlex 结果不足触发 Semantic Scholar/Crossref、MCP/`duckduckgo` 不可用时显式 skipped；provider attempts 完整可追溯。
- 单 provider 全失败返回 `failed/no_provider`；部分 provider 失败但仍有候选返回 `partial_success`，不能伪装为全成功。
- 缺字段、坏类型、非法 DOI/年份、重复 `record_id`、查询数量越界、候选路径越界和 manifest 不匹配均 fail-closed。
- 同 DOI、标题+年份模糊重复、预印本—正式版重复能生成 canonical 和合并边；canonical 选择理由可解释。
- 年份/文献类型/预印本策略/总量上限生效；截断的 dropped count、排序和 warning 可重现。
- 摘要 enrichment 的关闭、全候选有限补全和 selected 后补全三种模式都有清晰状态和来源标记。

#### Review end-to-end

- review 阶段 1 只调用新 search；阶段 2 不再调用旧 dedupe，仍保留 `1_search/2_dedupe` checkpoint 语义。
- 在 mock provider 和 golden fixture 上，评分输入、选文集合、BibTeX key、字数预算、工作条件、验证报告、PDF/Word 与基线等价。
- review 缺 search、manifest contract 不兼容、候选/hash 被删除或篡改时明确失败；不会静默回到旧内联 provider。
- 旧 `run_pipeline.py` 参数、旧输出文件名、旧 standalone wrappers、旧 `.systematic-literature-review` checkpoint 和显式单查询后备仍可验证。
- 现有摘要补全仍在选文后发生，缺摘要 warning 和 evidence cards 行为不发生无说明变化。

#### 安全、复现和发布

- scope-root/path traversal、外部 publish 目录冲突、绝对 artifact 路径和跨 run 猜测全部被阻断。
- 查询 hash、配置指纹、provider attempts、cache 模式、生成时间、版本和 manifest hash 可供 resume 审计。
- 新 search 可按最小依赖独立安装；review 缺少依赖时给出安装指引；外部安装器/上游清单完成同步检查。
- 所有测试产物位于 `skills/research-literature-search/tests/` 或 `skills/research-literature-review/tests/` 的计划子目录及本轮 `.bensz-api` 工作区，不在仓库根目录生成临时文件。

建议的离线验证命令（实现后执行，计划阶段不执行源代码修改）：

```bash
python -m unittest discover -s skills/research-literature-search/tests -p 'test_*.py'
python -m unittest discover -s skills/research-literature-review/tests -p 'test_*.py'
python -m unittest discover -s skills/research-literature-review/qa -p 'test_*.py'
python -m py_compile skills/research-literature-search/scripts/*.py
python -m py_compile skills/research-literature-review/scripts/pipeline_runner.py skills/research-literature-review/scripts/run_pipeline.py
```

正式验收还需使用 mock provider 完成一次 review 阶段 0–7 dry run，并使用一份真实但已脱敏的历史输出做 PDF/Word 和候选集合回归；联网检索失败时不得声称已完成真实 provider 验证。

## 风险与待确认事项

- **契约设计过度复杂：** 先固定 `rls.v1` 的必需字段和 manifest 最小集合，扩展字段只允许向后兼容增加；不要把全文、评分和写作字段塞进 paper schema。
- **双重去重导致结果变化：** 新 search 输出 canonical 后，review 阶段 2 必须是验证/映射 no-op；旧 dedupe 只作为 wrapper 或 legacy adapter。
- **独立安装路径不稳定：** resolver 必须有显式 override、版本检查和清晰失败信息；不能依赖某个当前机器上的固定绝对路径。
- **旧脚本用户受影响：** 先保留 wrapper、参数和旧文件名，完成 golden 回归后再安排弃用；不直接删除或重命名旧入口。
- **摘要补全成本上升：** 默认继续 post-selection；manifest 明确 enrichment mode，避免 search run 对全量候选重复请求。
- **provider 字段质量不一致：** 规范化时统一 DOI、日期、来源和缺失值语义；保留 raw/provenance，不能用 `journal/source` 互相猜填。
- **部分成功被误认为完整成功：** status、failure_code、attempts、truncation 和 warnings 必须成为 review 的硬门槛输入。
- **外部安装器不同步：** 本仓库没有安装器源码时，把上游/外部安装器同步列为发布前阻断项，而不是在本仓库伪造修改已安装 skill 的步骤。

### 回滚方案

1. 在切换 review 默认消费者前保留基线、旧 wrappers、旧 checkpoint 适配器和 feature flag。
2. 新 search 仅新增不覆盖；review 出现回归时可显式切回 `--legacy-local-search`，并在日志标记 legacy 模式、原因和结果来源。
3. 旧运行目录只读恢复；迁移脚本必须幂等，不删除、不覆盖用户文件。
4. 稳定后再单独发布旧内联实现的弃用公告和移除计划，不能把“拆分完成”与“立即删除兼容层”绑定在同一个不可逆提交中。

## 完成定义

- `research-literature-search` 可独立运行并输出通过 validator 的版本化 manifest bundle；任何候选论文都能追溯到 provider、query、排名和去重决策。
- `research-literature-review` 的依赖元数据和执行门禁明确要求新 search；阶段 1/2 完全对接该契约，不私自重复检索或去重。
- 综述 skill 的原名、旧 CLI、旧 checkpoint/resume、选文/写作/验证/PDF/Word 功能均保持可用，golden fixture 证明结果等价。
- 缺少 search、契约不兼容、manifest/hash 损坏、provider 全失败和路径越界都会可见地失败，而不是静默降级。
- 新增 skill、综述 skill、根 README/skills README、CHANGELOG、依赖图、安装说明和测试矩阵的版本口径一致；外部安装器同步项已列入发布检查。
- 计划中的所有测试与真实构建验证均在实现阶段完成并留存可审计日志；本轮只交付本计划，不修改源代码。
