# 最终报告字段说明

`analysis/final_recommendations.json` 至少包含：

- `manuscript_title`
- `summary`
- `journals`

每个 journal 建议包含：

- `rank`
- `recommendation_score`
- `journal_name`
- `impact_factor`
- `cas_small_category_quartile`
- `recognition`
- `official_website`
- `scope_fit_summary`
- `recommendation_reasons`
- `recent_articles`

`recent_articles` 每条建议包含：

- `publication_date`
- `title`
- `abstract`
- `relevance`
- `pmid`
- `url`
