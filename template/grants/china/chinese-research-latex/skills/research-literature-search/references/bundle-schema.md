# 检索 Bundle 契约

`manifest.json` 是 bundle 唯一入口。artifact 的 `path` 必须是相对 manifest 目录的安全路径，并附 SHA-256。review 只接受 `status=success` 或 `partial_success`。

最小字段：

```text
contract_version / candidate_schema_version / search_skill_version / search_run_id
topic / domain / topic_hash
query_plan {source, sha256, requested_count, accepted_count, items[]}
filters / provider_policy / attempts
counts {raw, normalized, deduped, failed, empty_records, invalid_records, normalization_failed, dropped}
truncation / dedupe / abstract_enrichment
artifacts / status / failure_code / warnings / created_at / cache
```

`candidates_deduped.jsonl` 是 canonical 候选池；`provenance.jsonl` 能回答 provider、query、原始 rank 及合并来源；`dedupe_map.json` 记录 canonical 选择与合并边。
