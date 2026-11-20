#!/usr/bin/env python3
"""查询输入契约：统一文件 stem、JSON schema、数量边界与内容指纹。"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


class QueryInputError(ValueError):
    """查询输入不满足公开契约。"""


@dataclass(frozen=True)
class QueryPlan:
    queries: list[dict[str, str]]
    requested_count: int

    @property
    def accepted_count(self) -> int:
        return len(self.queries)


def normalize_output_stem(raw: str) -> str:
    """生成 runner 与 wrapper 共用的稳定输出 stem。"""
    stem = re.sub(r'[\\/:*?"<>|]+', "", str(raw or "").strip())
    stem = re.sub(r"\s+", "-", stem)
    return stem[:80] or "topic"


def legacy_output_stems(raw: str) -> list[str]:
    """返回只读兼容探测用的历史 stem；新文件不得使用这些名称。"""
    value = str(raw or "").strip()
    old_runner = re.sub(r'[\\/:*?"<>|]+', "", value)
    old_runner = re.sub(r"\\s+", "-", old_runner)[:80] or "topic"
    canonical = normalize_output_stem(value)
    return [stem for stem in dict.fromkeys([old_runner]) if stem != canonical]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _normalize_item(item: Any, index: int) -> dict[str, str] | None:
    if isinstance(item, str):
        query = item.strip()
        return {"query": query, "rationale": ""} if query else None
    if isinstance(item, dict):
        query = str(item.get("query") or "").strip()
        if not query:
            return None
        rationale = str(item.get("rationale") or "").strip()
        return {"query": query, "rationale": rationale}
    raise QueryInputError(
        f"查询 JSON 第 {index} 项格式错误：只支持字符串或含 query/rationale 的对象"
    )


def normalize_query_payload(
    data: Any,
    *,
    min_queries: int = 5,
    max_queries: int = 25,
    source: str = "查询输入",
) -> QueryPlan:
    """规范化已解析的查询 JSON，并应用数量边界。"""
    if min_queries < 1 or max_queries < min_queries:
        raise QueryInputError(
            f"查询数量配置无效：min_queries={min_queries}, max_queries={max_queries}"
        )

    if isinstance(data, dict):
        if "queries" not in data:
            raise QueryInputError('查询 JSON 对象必须包含 "queries" 数组')
        items = data["queries"]
    else:
        items = data
    if not isinstance(items, list):
        raise QueryInputError("查询 JSON 必须是数组，或包含 queries 数组的对象")

    queries: list[dict[str, str]] = []
    for index, item in enumerate(items, 1):
        normalized = _normalize_item(item, index)
        if normalized is not None:
            queries.append(normalized)

    accepted = len(queries)
    if accepted < min_queries:
        raise QueryInputError(
            f"{source} 的有效查询至少需要 {min_queries} 条，空查询剔除后仅 {accepted} 条"
        )
    if accepted > max_queries:
        raise QueryInputError(f"{source} 的有效查询至多允许 {max_queries} 条，当前 {accepted} 条")
    return QueryPlan(queries=queries, requested_count=len(items))


def load_query_plan(path: Path, *, min_queries: int = 5, max_queries: int = 25) -> QueryPlan:
    """读取并严格校验公开的多查询 JSON 契约。"""
    source = Path(path).expanduser().resolve()
    if not source.exists():
        raise QueryInputError(f"查询文件不存在：{source}")
    if not source.is_file():
        raise QueryInputError(f"查询路径不是普通文件：{source}")

    try:
        data = json.loads(source.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise QueryInputError(f"无法解析查询 JSON：{source}（{exc}）") from exc
    return normalize_query_payload(
        data,
        min_queries=min_queries,
        max_queries=max_queries,
        source=str(source),
    )
