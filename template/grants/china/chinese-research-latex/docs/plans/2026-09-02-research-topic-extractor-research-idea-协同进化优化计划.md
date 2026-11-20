# research-topic-extractor × research-idea 协同进化实施计划

> 状态：仅计划，尚未修改任何源代码、Skill 文档或配置。
>
> 目标：让两个 Skill 从“提取主题、生成候选、逐个查新、重复审查”升级为一条可追溯的科学发现链：理解用户需求 → 定位大/中/小领域 → 找到经典、同行轨迹与近期前沿 → 建立文献和引用网络 → 攻击网络寻找真实缺口 → 形成可证伪的研究问题 → 以证据和启发式方式成稿。

## 通俗解释：究竟发生了什么

- **一句话说明：** 现在的两个 Skill 能把资料变成几个研究问题，却还没有把“这个小领域如何发展到今天、哪里断了、为什么值得做”系统地重建出来。
- **生活类比：** 可以把 `research-topic-extractor` 看成“接待和导航台”，把 `research-idea` 看成“研究侦察队”。导航台目前只递给侦察队一张写着地点、关键词和几个问题的便签；侦察队随后分别查每个问题，却没有共同的地图、档案目录和道路关系图。本计划要让导航台交付一份可核对的区域简报，让侦察队先建档案馆和发展地图，再从地图中的断路、冲突和未连接区域寻找值得验证的问题。
- **对应到本问题：** 区域是大/中/小研究领域；档案是带 DOI、作者、查询来源和摘要定位的文献证据；道路关系图是引用、作者轨迹、方法继承和冲突关系；断路是研究空白、边界条件或机制链缺口；侦察队的不同成员是按证据域分工的只读 Agent，最后由一个综合主体形成候选和报告。
- **改变前后：** 现在输入“某现象在某技术中的应用”会直接得到 3–7 个问题和固定 3×3 审查意见；改进后先得到“领域层级、相邻领域、经典→转折→前沿时间线、关键同行及其可核验轨迹、纳排文献库和引用拓扑”，然后每个候选都能回答“缺口落在哪个节点/边、已有研究覆盖到哪里、什么观察会推翻它、在用户资源内是否值得做”。

## 专业判断：问题在哪里

### 当前现象

1. `skills/research-topic-extractor/SKILL.md` 只承诺 `topic`、`keywords`、`core_questions` 三项输出；没有用户约束、领域层级、检索面、经典/近期种子、来源锚点或不确定性。
2. `skills/research-idea/SKILL.md` 的主流程是“资料 → 3–7 个候选 → 每个候选调用 Premium 查新 → 固定 3 轮、每轮 3 个独立审查 → 选择最佳方案”。Agent 目前共享同一类 Prompt，缺少领域侦察、反例、方法、可行性等证据域分工。
3. `research-literature-review` 已有 5–25 条多查询、去重、标题/摘要评分和证据卡能力，但其默认目标是 80–150 篇、10k–15k 字、PDF/Word 的规范综述；现有论文转换和证据卡没有完整作者 ID、引用边、被引关系和版本信息。
4. 当前查新结论只有“未研究 / 部分研究但关键缺口存在 / 已充分研究”，缺少“哪篇论文支持、哪条引用边或时间转折暴露了缺口”的结构化证据。当前仓库也没有可直接调用的 `openalex_citation_chase.py`，不能把未来的引用追踪当作现成能力。

### 影响范围

- 用户得到的可能是“换词后的旧问题”，而不是由领域演进和冲突证据推导出的研究机会。
- 只追高被引或模型记忆中的“大牛”会放大声望偏差，遗漏小同行、负结果、相邻领域和不符合主流叙事的工作。
- 把题目/摘要中的语义相似误写成引用、机制或因果关系，会导致新颖性判断和正式引用不可靠。
- 如果直接把两个 Skill 互相调用，会形成循环依赖；如果让 `research-idea` 伪装成完整综述，又会把灵感探索拖入不必要的篇幅、排版和导出成本。

### 已知原因与待验证假设

- **已知事实：** 当前上游只交付三字段，当前下游没有统一的证据注册表和科研网络契约；现有检索契约要求多查询并 fail-closed。
- **已知事实：** 标题/摘要可以承担第一轮筛选，但不能独立证明机制、等价假设或“该问题从未被研究”。
- **待验证假设：** 现有 OpenAlex/Semantic Scholar/Crossref 适配器能够在不破坏旧字段的前提下补充作者/机构 ID、引用列表、被引数和版本信息；缺失字段必须允许显式 `unknown`。
- **待验证假设：** 一个轻量 `discovery/evidence_only` profile 可以复用 `research-literature-review` 的多查询与评分实现，而不改变标准综述默认行为；未来 `research-literature-search` 可通过同一契约插入。

## 要达到什么目标

### 完成后的变化

1. `research-topic-extractor` 保留默认 `topic_only`，新增显式 `scientist` 和 `candidate` 模式，输出版本化 `research-brief/v1`；旧的三字段 JSON/YAML 仍可被标准综述消费。
2. `research-brief/v1` 结构化保存用户需求、资源/时间边界、大中小领域和邻域、术语与排除词、查询族、经典/同行/近期种子以及不确定性和来源。
3. `research-idea` 成为唯一编排者：先共享一份不可变研究简报，再构建 `evidence-registry/v1` 和 `research-network/v1`，之后才进行 gap attack、候选定向查新和价值红队。
4. 文献库同时保存纳入项、排除项、矛盾/负证据、摘要缺失和筛选理由；正式引用只能从有 DOI/URL、provider、访问时间和 claim locator 的注册表记录产生。
5. 科研网络区分 API 事实边和 Agent 推断边，按时间切片叙述从经典工作到当前前沿的演进；每个 gap 必须绑定 evidence ID 以及图节点/边。
6. 多 Agent 按证据域分工、独立只读、分批汇总并受预算和饱和停止条件约束；不会把同质多数票当作科学共识。
7. 最终报告新增领域地图、同行轨迹、时间线/引用拓扑、文献筛选、网络攻击、正式参考文献和“本地思维碰撞/待验证线索”章节，同时保留现有候选、可证伪、查新和风险内容。

### 不在本次处理范围

- 本轮只交付计划，不修改任何源代码、Skill、配置、测试或安装文件。
- 不删除 `topic_only`、旧 `theme.json`、旧 `Research-Idea_*.md`、旧 `run_pipeline.py` 参数、旧别名或历史工作区。
- 不把 `research-idea` 变成完整系统综述；标准 `research-literature-review` 的 5–25 查询、Premium 综述、PDF/Word 和默认选文逻辑保持不变。
- 不在第一阶段实现无限深度 citation chasing、全文下载、社交媒体采集或新的真实 provider；未来 `research-literature-search` 只先定义可插拔接口。
- 不把模型记忆、引用量、共同作者关系或 Agent brainstorming 当作正式证据；不自动生成不存在的引用边。
- 不修改系统级 `~/.codex/skills/`、`~/.claude/skills/` 或用户凭据；测试不在仓库根目录产生中间文件。

## 改进方向

### 方向一：建立向后兼容的研究简报契约

在 `research-topic-extractor` 中新增版本化 `research-brief/v1`，默认仍输出旧三字段，只有用户或下游显式请求 `mode: scientist` 时才生成科学家模式的完整简报；`mode: candidate` 只针对一个已有 `gap_id` 生成增量查询。`research-topic-extractor` 只负责理解资料和生成简报，不依赖 `research-idea`，避免循环调用。

简报至少包含：

- `user_need`：目标、研究对象、应用/决策语境、时间窗、可用数据/设备/样本/技能、伦理或风险边界、未决澄清项。
- `domain_map`：`field`、`subfield`、`niche`、`adjacent_fields`；每层允许多个候选、理由、置信度和输入出处，不把扁平关键词分类器当成最终领域结论。
- `terms`：规范术语、同义词、方法词、对象/结果词、排除词、多语言变体及来源。
- `questions`：描述性、机制性、边界条件、争议/反例问题；保留 `core_questions` 作为兼容别名。
- `query_plan`：`broad_scope`、`seminal`、`authority`、`recent_frontier`、`direct_relevance`、`adjacent_negative`、`contradiction`、`gap` 等查询族，每条带目的、时间范围、语言、rationale 和预期证据域；最终能转换为现有 5–25 条 `queries.json`。
- `seed_landmarks`：经典论文、研究者/实验室、期刊/会议和近期工作仅作为待验证种子，带标识/URL、选择理由、来源和置信度，禁止凭模型记忆补人名。
- `scope`、`inclusion_exclusion`、`uncertainties`、`provenance`、`schema_version` 和输入内容 hash。

对普通用户而言，这意味着“提取主题”仍然快捷；对 `research-idea` 而言，交接的是一份可以逐项核对的研究地图起点。

### 方向二：把检索结果变成证据注册表，而不是一堆高分论文

为 `research-literature-review` 增加显式 `discovery/evidence_only` 适配层，复用现有查询契约、多源检索、去重、摘要补全和题目/摘要评分，但不强制 10k–15k 字、80–150 篇和 PDF/Word 发布。未来 `research-literature-search` 只要能消费同一 `query_plan`、输出同一 bundle，即可作为可选提供方。

`evidence-registry/v1` 的记录要包含稳定 `paper_id`、完整作者与作者/机构 ID、题目、摘要、年份/版本、venue、DOI/URL、provider、query/facet、`screening_label`（direct/adjacent/background/contradiction/negative/excluded）、相关性和筛选置信度、纳排理由、设计/发现/局限/适用边界、claims、`formal_citation_eligible`、provenance 和缺失原因。保留排除项和低分项，避免只见入选文献。

选文不再单纯按高分排序，而是按经典、近五年、直接相关、相邻桥接、矛盾/负证据等 facet 设置可配置的最低覆盖；citation count 只作发现信号。题目/摘要只产生 `provisional` 机制判断，关键等价假设和“已充分研究”必须走定向检索，并在必要时要求全文或人工核验。

### 方向三：确定性构图，再让 Agent 解释拓扑

扩展 provider 规范化层，尽可能保留 `referenced_works`、`cited_by_count`、`primary_topic/concepts`、作者/机构 ID、出版类型和版本关系；缺失时记录 `null` 与缺失原因。新增确定性 graph builder 或 enricher，生成 `research-network/v1`：

- 节点：`paper`、`author`、`lab/institution`、`concept/term`、`question`，带年份、角色、证据 ID 和置信度。
- 边：来源事实 `cites`、`coauthor`、版本关系，以及有摘要证据的 `supports`、`contradicts`、`reuses_method`；每条边带 source、locator、confidence 和 `edge_kind=fact|inference`。
- 时间线：基线/定义、方法转折、应用扩展、争议或失败、当前前沿；每个里程碑链接论文和用户问题。
- `communities`、`bridges`、`isolates`、`missing_links`：只作为可解释的发现线索，不能把中心性直接等同于重要性。

引用方向必须来自 provider 事实或明确来源；共同作者、时间先后和语义相似不能自动升级为思想继承或因果影响。网络不完整时报告 coverage 和 `unknown`，不补造边。

### 方向四：用证据域分工替换重复的固定 3×3 审查

主 Agent 负责状态机、用户边界、不可变输入快照、预算和唯一正式写入；评估 Agent 只读取分配的快照/公共原始索引，写各自 `workspace/RESULT.md`；每批至少两个独立评估后，恰好一个只读汇总 Agent 合并；真正实现阶段只允许一个执行主体，复杂跨模块变更由主 Agent 落地。

建议的默认链路如下，实际线程数按证据增益动态缩减：

1. **需求/边界闸门**：主 Agent 提炼目标、资源、时间和伦理边界；必要时最多一个只读澄清评估。信息不足时暂停检索，不急于生成 idea。
2. **领域侦察（3 个评估 + 1 个汇总）**：`domain-cartographer` 负责大/中/小领域和邻域；`canonical-trajectory-scout` 负责经典工作、同行/实验室轨迹；`frontier-recall-scout` 负责近 3–5 年、小同行、非主流、跨语言和负证据。汇总器生成 field map 和 query plan。
3. **文献筛选（2 个评估 + 1 个 adjudicator）**：保守路线核对直接性和等价假设；召回路线寻找相邻、矛盾、负结果和小同行；adjudicator 只处理分歧，不改写原始记录。
4. **图谱与 gap attack（4 个评估 + 1 个汇总）**：`contradiction-hunter`、`missing-link-hunter`、`mechanism-causal-hunter`、`boundary-feasibility-hunter`；高风险领域可增加 `taste-critic`，但不默认启动。每个 gap 至少关联两条独立证据，只有一条证据时标为 `speculative`。
5. **候选定向查新**：主 Agent 从攻击汇总生成 3–7 个完整候选，通过 `candidate` mode 生成增量查询；每候选最多一次有界重构，全部淘汰后交付负结果和覆盖限制，不无限循环。
6. **价值红队（3 个评估 + 1 个汇总）**：`importance/taste`、`novelty/equivalent-prior-art`、`falsifiability/feasibility` 分别评分；输出 `importance`、`novelty`、`explanatory_gain`、`falsifiability`、`feasibility`、`tractability`、`risk` 与独立的 `evidence_confidence`，不以多数票掩盖分歧。
7. **成稿与验证**：唯一写作主体读取所有汇总和 registry，写启发式报告、正式参考文献和隔离的 brainstorming；确定性 validator 通过后由主 Agent 做引用、网络和用户边界复验。

每个 Agent 输出必须包含角色、输入指纹、结论、证据 ID、推荐变化、未覆盖域、风险和验证点；失败或超预算的线程不能被静默视为成功。

### 方向五：硬隔离正式证据与本地思维碰撞

`evidence_registry.jsonl` 是唯一 BibTeX/正文引用来源，正式记录必须有 DOI/URL、provider、检索时间和 claim locator。`brainstorm_notes.jsonl` 单独保存 Agent 的类比、未核验专家线索、会议/社交媒体推测、冲突解释和假说草图，强制字段为 `citation_allowed: false`、`origin: agent`、`status: unverified` 和关联 evidence IDs。

报告单列“本地思维碰撞/待验证线索”，只能用启发性或待核验措辞，不生成 `\cite`、BibTeX 或“已有研究证明”。网络节点、gap 和候选必须能通过 evidence ID 回到正式记录；不能回链的内容降级为 brainstorming 或删除。

### 方向六：把领域拓扑和证据闭环纳入报告质量门

扩展 `skills/research-idea/references/report-template.md` 和 `validate_report.py`，新增以下章节和校验：用户需求与边界、领域分层与相邻领域、同行/经典/近期轨迹、文献库纳排与证据等级、时间线/引用拓扑、网络攻击得到的 gap、正式参考文献、本地 brainstorming、候选问题/假设/预测/反证、最佳方案和风险下一步。

校验器除保留现有候选数量、可证伪词、Premium 和隐藏路径检查外，还要检查：schema 版本；证据 ID → registry → DOI/Bib 闭环；网络边端点、方向和年份；经典/近期/直接/相邻/矛盾 facet coverage；每个 gap 的节点/边和 evidence；正式引用与 brainstorming 的分离；未验证/摘要缺失/作者待核实的显式标记。

## 实施范围与顺序

按依赖顺序推进；每阶段通过出口门后才进入下一阶段。实现时正式变更仍应保持单点落地，不让多个 Agent 并行修改同一源文件。

| 阶段 | 目标与主要源码范围 | 文档/配置同步 | 出口门与最小验证 |
| --- | --- | --- | --- |
| P0 基线与契约冻结 | 只读保存当前 `topic_only`、`research-idea` 报告、review 查询/评分/选文和输出行为；设计三个 JSON Schema 与 hash/版本规则。 | 在计划评审中确认旧字段、旧目录、5–25 查询和 Premium 约束不可变。 | 形成脱敏 fixture；旧输入可解析，新 schema 的坏版本/坏类型/缺字段 fail-closed。 |
| P1 研究简报 | 修改 `skills/research-topic-extractor/` 的 `SKILL.md`、`config.yaml`、`references/`、README/CHANGELOG，并新增 schema/校验脚本；修改 `research-idea` 的依赖解析和 theme adapter。 | 明确 `topic_only/scientist/candidate`、`research-brief/v1` 和旧 `theme.json` 兼容；必要时同步 `skills/README.md`。 | 旧三字段不变；scientist 输出含领域层级、查询族、种子和 provenance；candidate round-trip 查询指纹稳定。 |
| P2 发现检索与证据注册表 | 在 `skills/research-literature-review/` 增加 `discovery/evidence_only` adapter；扩展 provider 规范化、去重、证据卡和 `evidence_registry`；不删除旧脚本入口。 | 更新 review 的必需/可选依赖、未来 `research-literature-search` capability contract、查询/来源/摘要缺失说明。 | mock provider 验证 5/25/空/重复/超限查询、DOI/作者/版本去重、facet 配额、纳排理由、摘要缺失和 partial/failed 状态。 |
| P3 科研网络 | 新增确定性 citation/author/method graph builder 或 enricher，生成 `research-network/v1`、时间切片、coverage 和缺边报告；只在 provider 有依据时生成事实边。 | 新增网络 schema 和图谱叙事规则，说明 fact/inference 边与 `unknown`。 | 合成金样验证 DAG 方向、端点、版本合并、断边和跨 provider 冲突；语义相似不能通过 citation 边校验。 |
| P4 `research-idea` 编排与 gap attack | 重写 `research-idea` 的主流程、agent prompt、状态/manifest 和输入快照：领域侦察→筛选→构图→攻击→候选查新→红队→成稿；每批独立 workspace、恰好一个汇总器。 | 在 `config.yaml` 写角色、预算、停止/降级、feature flag 和未来 search resolver；同步 README/CHANGELOG。 | fake adapter dry-run 检查调用顺序、角色数量、隔离、失败恢复、预算停止、gap 证据绑定和无第二执行主体。 |
| P5 报告与质量门 | 扩展 `report-template.md`、`validate_report.py`，必要时增加 registry/network validator；保留旧报告兼容或显式版本标识。 | 同步两个 Skill、`skills/README.md`、根 `README.md`/`CHANGELOG.md`（仅实际接口变化处）。 | 正/反例报告验证：无拓扑、无 provenance、brainstorm 被引用、候选不足、隐藏路径泄露和错误 schema 均失败；旧报告按兼容规则不被误判。 |
| P6 现实 smoke 与人工验收 | 前述离线验证通过后，用公开主题运行固定 5–8 query、有限一跳/重点二跳图；不把网络失败解释为“未研究”。 | 记录 provider、查询 hash、成本、时间、覆盖限制和回滚点，不上传私密输入。 | 科学家盲评能回答领域层级、关键同行、经典如何到前沿、gap 所在边和可推翻实验；任一项失败则回滚到对应阶段。 |

## 如何确认完成

### 自动化验证矩阵

- **契约兼容：** 旧 `topic/keywords/core_questions` 可只读迁移；未知 schema、字段类型错误、越界路径和 hash 改变会 fail-closed；`topic_only` 的标准综述调用行为不变。
- **领域地图：** 固定主题 fixture 输出大/中/小领域、相邻领域、每层证据/置信度、查询族和待核实种子；冲突时保留多个候选，不静默覆盖。
- **证据注册表：** mock OpenAlex/Semantic Scholar/Crossref 覆盖 DOI、作者/机构 ID、引用字段、预印本—正式版重复、摘要缺失、direct/adjacent/contradiction/negative/excluded 标签及纳排理由；registry 能生成可回链的 Bib 元数据。
- **网络完整性：** 所有边端点存在；`cites` 方向和时间关系可解释；节点/边无重复 ID；时间线和 coverage 可重现；断边、跨 provider ID 冲突和缺字段被标记而不是补造。
- **Agent 协议：** 每批至少两个相互独立的只读评估和恰好一个汇总；汇总输入覆盖全部有效结果；没有第二执行主体；线程失败、超预算和降级状态可追溯；所有中间产物留在任务级隐藏工作区。
- **Gap 与候选：** 每个 gap 具备 evidence IDs、网络节点/边、置信度、未覆盖预测和资源边界；候选始终有科学问题、可证伪假设、关键预测、反证路径、查新状态和风险；全部淘汰最多一次重构后安全退出。
- **正式报告：** 含领域分层、同行/经典/近期轨迹、时间线/拓扑、文献库纳排、网络攻击、正式参考文献和明确的 brainstorming 非正式标记；citation key→registry→Bib 闭环通过；不泄露隐藏路径、Prompt、凭据或私密原文。

实现阶段的离线验证应放在 `tests/research-topic-extractor/`、`tests/research-idea/` 及已有 review 测试子目录，不在仓库根目录生成产物。建议命令由实现阶段按真实入口确定，至少覆盖各 Skill 的 Python 语法检查、schema/validator 单元测试、fake-provider dry-run 和旧接口回归；真实联网 smoke 只能作为最后的补充证据。

### 运行时停止与降级

- 每个查询 facet 达到最低覆盖，且连续两轮新增查询带来的独立高相关文献低于阈值后停止；保存 query fingerprint、结果数、去重率和停止原因。
- 一跳引用扩展及重点节点二跳达到节点/边/API 预算，且连续两轮没有新增关键节点或社区后停止；图谱缺失降级为 coverage warning。
- 两个筛选 Agent 达到一致性阈值才自动接受；不一致交 adjudicator；摘要缺失或元数据冲突不能自动升级为强证据。
- gap taxonomy 连续两轮不再新增类别，或新增 gap 都只有单一/未验证来源时停止；保留“未发现更多”的理由。
- 任何 provider、作者身份、全文或引用字段不可用时，结论使用“在本检索范围未发现/待核验”，可继续本地 brainstorming，但不得提升正式证据等级。

## 技术补充（按需阅读）

### 生产者—消费者关系

| 生产者 | 消费者 | 交接物 | 禁止越界 |
| --- | --- | --- | --- |
| `research-topic-extractor` | `research-idea`、标准 review | `research-brief/v1`；兼容 `theme.json` 三字段 | extractor 不调用 idea，不判断候选价值，不生成正式引用 |
| `research-literature-review` discovery adapter（未来可换 `research-literature-search`） | `research-idea` | `evidence-registry/v1`、查询日志、来源和筛选证据 | provider 不决定最终 idea，不把完整综述正文当灵感报告 |
| registry/确定性 graph builder | gap attack 与报告 | `research-network/v1`、timeline、coverage | graph builder 不把语义相似当 citation，不创造无来源边 |
| gap attack/红队汇总 | 唯一成稿主体 | 带证据的 gap、候选、评分向量、分歧和未验证线索 | Agent 不改原始 registry、别的 thread 结果或正式项目文件 |

### 最小字段契约

`research-brief/v1`：`schema_version`、`mode`、`topic`、`keywords`、`core_questions`、`user_need`、`domain_map`、`terms`、`questions`、`query_plan`、`seed_landmarks`、`scope`、`inclusion_exclusion`、`uncertainties`、`provenance`。

`evidence-registry/v1`：`paper_id`、`identifiers`、`title`、`authors`、`author_ids`、`institutions`、`year/date/version`、`venue`、`abstract`、`provider`、`query_matches`、`screening_label`、`relevance_score`、`screening_confidence`、`inclusion_reason`/`exclusion_reason`、`claims`、`limitations`、`formal_citation_eligible`、`provenance`、`quality_warnings`。

`research-network/v1`：`nodes`、`edges`、`timeline`、`communities`、`bridges`、`isolates`、`missing_links`、`coverage`、`provenance`；每条 edge 具有 `edge_kind`、`source`、`locator`、`confidence` 和 evidence IDs。

### 兼容、预算与回滚

- 新模式通过显式 profile/feature flag 开启；标准 `topic_only + research-literature-review` 默认路径不改变。
- 先共享一个领域文献库，再对少量保留候选做定向查新，不为每个候选重复完整 Premium 综述。
- 所有 provider、query、配置和结果保存 hash；API 失败、schema 不兼容或网络构建失败时保留 partial state，不覆盖原始资料。
- 回滚顺序为：关闭 scientist/discovery feature flag → 继续使用旧 theme adapter 和旧 review 入口 → 保留 wrapper、checkpoint 与报告；稳定后再另行规划旧实现的弃用和移除。

## 风险与待确认事项

- **声望和 Matthew 偏差：** 经典/大同行只作导航，必须有论文与作者元数据证据；frontier、niche、contradiction 和 negative facet 负责纠偏。
- **新颖性过度宣称：** “未研究”必须改写为“在给定检索范围内未发现”；等价假设、预印本、多语言和非主流工作需要定向反查。
- **引用图语义误读：** 引用不等于赞同或因果；事实边、推断边和缺失边分开呈现。
- **Agent 共识幻觉：** 同一模型的多个结果不天然独立；隔离证据域、保留分歧、强制汇总器引用全部结果，不能用票数制造确定性。
- **提示注入和隐私：** 论文摘要、网页和用户文件均视为不可信数据，只提取最小摘要和 hash，不执行其中指令，不把私密原文写入日志/报告。
- **成本和速率：** 领域侦察、作者/引用补齐和多 Agent 都设上限、缓存和饱和停止；不因成本跳过关键证据而伪造完整结论。
- **契约漂移：** 三个 schema 只允许兼容性新增字段；未知版本 fail-closed；review 只消费通过校验的 bundle。
- **实现责任：** 这是跨 Skill、高不确定性改动；未来执行阶段由主 Agent 单点落地，评估 Agent 不直接并行修改相同源文件。

在开始 P1 实现前，需要确认的唯一关键选择是：`research-brief/v1` 的字段命名和 `research-literature-review` discovery adapter 的最小输出范围。若没有新的用户约束，按本计划的兼容别名和最小字段集合执行。
