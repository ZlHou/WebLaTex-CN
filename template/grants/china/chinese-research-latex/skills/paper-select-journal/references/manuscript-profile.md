# Manuscript Profile 指南

`analysis/manuscript_profile.json` 是后续筛刊的语义起点，先理解 manuscript 再写。

## 最低字段

- `title`
- `abstract`
- `keywords`
- `manuscript_summary`

## 推荐写法

- `keywords` 保留稿件原生关键词即可，不必为了脚本打分额外凑词。
- `manuscript_summary` 用 `2-4` 句概括研究问题、主要方法、核心贡献和目标读者。
- 如果用户已经说明投稿偏好，把它们写进 `target_journal_brief` 或 `notes`，让宿主模型在后续步骤自主规划。
- 不需要为了 Set1 人工拆出一长串 `field_hints / method_terms / application_terms`；除非它们确实能帮助人类复核，否则宁可少写。

## `excluded_journals` 何时填写

- 用户明确说“不投某刊”
- 已知合作/伦理/版面费等原因需要回避某刊
- 需要提前排除曾拒稿且不想重复尝试的期刊
