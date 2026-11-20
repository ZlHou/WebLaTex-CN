#!/usr/bin/env python3
from __future__ import annotations

import argparse
from typing import Any

from common import (
    compact_text,
    load_config,
    read_json,
    resolve_path,
    resolve_path_within,
    workspace_output_path,
    write_text,
)


def normalize_final_payload(payload: Any, limit: int = 10) -> dict[str, Any]:
    if isinstance(payload, dict):
        journals = payload.get("journals", [])
        title = payload.get("manuscript_title", "")
        notes = payload.get("summary", "")
    else:
        journals = payload
        title = ""
        notes = ""
    journals = [item for item in journals if str(item.get("journal_name") or "").strip()]
    journals = sorted(
        journals,
        key=lambda item: (
            -(item.get("recommendation_score") or item.get("rank_score") or 0.0),
            item.get("rank", 999),
        ),
    )[:limit]
    return {
        "manuscript_title": title,
        "summary": notes,
        "journals": journals,
    }


def render_markdown(payload: dict[str, Any]) -> str:
    lines = ["# 期刊投稿推荐报告", ""]
    if payload["manuscript_title"]:
        lines.append(f"- 稿件题目：{payload['manuscript_title']}")
    if payload["summary"]:
        lines.append(f"- 总结：{payload['summary']}")
    if len(lines) > 2:
        lines.append("")

    for index, journal in enumerate(payload["journals"], start=1):
        lines.append(f"# {index}. {journal.get('journal_name', '未命名期刊')}")
        lines.append("")
        lines.append("## 核心信息")
        lines.append("")
        lines.append(f"- 影响因子：{journal.get('impact_factor', journal.get('jif', '待补充'))}")
        lines.append(
            "- 中科院小类及其分区：{value}".format(
                value=journal.get("cas_small_category_quartile", journal.get("cas_quartile", "待联网核验"))
            )
        )
        lines.append(f"- 业内认可度：{journal.get('recognition', '待联网核验')}")
        official_website = journal.get("official_website", "")
        if official_website:
            lines.append(f"- 官方网站：[{official_website}]({official_website})")
        else:
            lines.append("- 官方网站：待联网核验")
        lines.append("")
        lines.append("## 为什么推荐这个杂志")
        lines.append("")
        reasons = journal.get("recommendation_reasons", [])
        if reasons:
            for reason in reasons:
                lines.append(f"- {reason}")
        else:
            lines.append("- 待补充推荐理由")
        scope_fit = journal.get("scope_fit_summary", "")
        if scope_fit:
            lines.append(f"- Scope 匹配摘要：{scope_fit}")
        lines.append("")
        lines.append("## 最近 3 个月类似主题论文")
        lines.append("")
        lines.append("| 发表日期 | 标题 | 摘要 | 相关性说明 | PMID / 链接 |")
        lines.append("| --- | --- | --- | --- | --- |")
        articles = journal.get("recent_articles", [])
        if not articles:
            lines.append("| 暂无 | 暂无 | 暂无 | 暂无 | 暂无 |")
        for article in articles:
            url = article.get("url") or ""
            pmid = article.get("pmid") or "无"
            if url:
                link = f"[PMID {pmid}]({url})"
            else:
                link = pmid
            lines.append(
                "| {date} | {title} | {abstract} | {relevance} | {link} |".format(
                    date=article.get("publication_date", "未知"),
                    title=compact_text(article.get("title", ""), 90).replace("|", "/"),
                    abstract=compact_text(article.get("abstract", ""), 140).replace("|", "/"),
                    relevance=compact_text(article.get("relevance", "待 AI 补充"), 120).replace("|", "/"),
                    link=link,
                )
            )
        lines.append("")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="把最终推荐 JSON 渲染成 Markdown 报告")
    parser.add_argument("--workspace", required=True, help="隐藏工作区 run 根目录")
    parser.add_argument("--final-json", required=True, help="final_recommendations.json 路径")
    parser.add_argument("--output", default="", help="覆盖默认输出路径")
    args = parser.parse_args()

    config = load_config()
    workspace = resolve_path(args.workspace)
    payload = normalize_final_payload(
        read_json(resolve_path_within(args.final_json, parent=workspace, label="final-json")),
        limit=int(config["screening"]["default_set3_limit"]),
    )
    output_path = (
        resolve_path_within(args.output, parent=workspace, label="output", base=workspace)
        if args.output
        else workspace_output_path(workspace, config["reports"]["final_report"])
    )
    write_text(output_path, render_markdown(payload))
    print(f"report_markdown={output_path}")


if __name__ == "__main__":
    main()
