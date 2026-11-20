#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from typing import Any

from common import (
    compact_text,
    load_config,
    read_json,
    resolve_path,
    resolve_path_within,
    workspace_output_path,
    write_json,
    write_text,
)


MONTH_MAP = {
    "1": "01",
    "01": "01",
    "jan": "01",
    "january": "01",
    "2": "02",
    "02": "02",
    "feb": "02",
    "february": "02",
    "3": "03",
    "03": "03",
    "mar": "03",
    "march": "03",
    "4": "04",
    "04": "04",
    "apr": "04",
    "april": "04",
    "5": "05",
    "05": "05",
    "may": "05",
    "6": "06",
    "06": "06",
    "jun": "06",
    "june": "06",
    "7": "07",
    "07": "07",
    "jul": "07",
    "july": "07",
    "8": "08",
    "08": "08",
    "aug": "08",
    "august": "08",
    "9": "09",
    "09": "09",
    "sep": "09",
    "sept": "09",
    "september": "09",
    "10": "10",
    "oct": "10",
    "october": "10",
    "11": "11",
    "nov": "11",
    "november": "11",
    "12": "12",
    "dec": "12",
    "december": "12",
}


def build_esearch_url(config: dict[str, Any], journal_name: str, start_date: dt.date, end_date: dt.date) -> str:
    params = {
        "db": "pubmed",
        "retmode": "json",
        "retmax": str(config["pubmed"]["retmax"]),
        "sort": "pub_date",
        "tool": config["pubmed"]["tool_name"],
        "term": f'"{journal_name}"[Journal] AND ("{start_date:%Y/%m/%d}"[Date - Publication] : "{end_date:%Y/%m/%d}"[Date - Publication])',
    }
    return config["pubmed"]["esearch_url"] + "?" + urllib.parse.urlencode(params)


def build_efetch_url(config: dict[str, Any], ids: list[str]) -> str:
    params = {
        "db": "pubmed",
        "retmode": "xml",
        "tool": config["pubmed"]["tool_name"],
        "id": ",".join(ids),
    }
    return config["pubmed"]["efetch_url"] + "?" + urllib.parse.urlencode(params)


def http_get(url: str, timeout: int) -> str:
    with urllib.request.urlopen(url, timeout=timeout) as response:
        return response.read().decode("utf-8")


def search_pubmed_ids(config: dict[str, Any], journal_name: str, start_date: dt.date, end_date: dt.date) -> list[str]:
    payload = json.loads(http_get(build_esearch_url(config, journal_name, start_date, end_date), int(config["pubmed"]["timeout_seconds"])))
    return payload.get("esearchresult", {}).get("idlist", [])


def _normalize_month(value: str | None) -> str:
    text = str(value or "").strip().lower()
    if not text:
        return "01"
    return MONTH_MAP.get(text, "01")


def _extract_pub_date(article: ET.Element) -> str:
    article_date = article.find(".//Article/ArticleDate")
    if article_date is not None:
        year = article_date.findtext("Year", default="1900")
        month = _normalize_month(article_date.findtext("Month", default="01"))
        day = article_date.findtext("Day", default="01")
        return f"{year}-{month.zfill(2)}-{day.zfill(2)}"

    pub_date = article.find(".//JournalIssue/PubDate")
    if pub_date is None:
        return ""
    year = pub_date.findtext("Year", default="1900")
    month = _normalize_month(pub_date.findtext("Month", default="01"))
    day = pub_date.findtext("Day", default="01")
    return f"{year}-{month.zfill(2)}-{day.zfill(2)}"


def parse_pubmed_articles(xml_payload: str) -> list[dict[str, Any]]:
    root = ET.fromstring(xml_payload)
    articles: list[dict[str, Any]] = []
    for article in root.findall(".//PubmedArticle"):
        title_node = article.find(".//ArticleTitle")
        title = "".join(title_node.itertext()).strip() if title_node is not None else ""
        pmid = article.findtext(".//PMID", default="").strip()
        abstract_parts: list[str] = []
        for node in article.findall(".//Abstract/AbstractText"):
            label = node.attrib.get("Label", "").strip()
            text = "".join(node.itertext()).strip()
            if not text:
                continue
            abstract_parts.append(f"{label}: {text}" if label else text)
        abstract = " ".join(abstract_parts).strip()
        articles.append(
            {
                "pmid": pmid,
                "title": title,
                "abstract": abstract,
                "journal": article.findtext(".//Journal/Title", default="").strip(),
                "publication_date": _extract_pub_date(article),
                "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else "",
            }
        )
    return articles


def fetch_articles_for_journal(
    *,
    config: dict[str, Any],
    journal_name: str,
    start_date: dt.date,
    end_date: dt.date,
) -> list[dict[str, Any]]:
    ids = search_pubmed_ids(config, journal_name, start_date, end_date)
    if not ids:
        return []
    xml_payload = http_get(build_efetch_url(config, ids), int(config["pubmed"]["timeout_seconds"]))
    articles = parse_pubmed_articles(xml_payload)
    articles.sort(key=lambda item: item.get("publication_date") or "", reverse=True)
    return articles[: int(config["pubmed"]["top_articles_per_journal"])]


def normalize_scope_review(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, dict):
        journals = payload.get("journals", [])
    else:
        journals = payload
    return [journal for journal in journals if journal.get("include_in_set2", True)]


def build_pubmed_summary(
    *,
    config: dict[str, Any],
    scope_review: list[dict[str, Any]],
    end_date: dt.date,
) -> dict[str, Any]:
    start_date = end_date - dt.timedelta(days=int(config["pubmed"]["lookback_days"]))
    journals_output: list[dict[str, Any]] = []
    for index, journal in enumerate(scope_review):
        journal_name = str(journal.get("journal_name") or "").strip()
        entry = {
            "journal_name": journal_name,
            "scope_fit_summary": journal.get("scope_fit_summary", ""),
            "official_website": journal.get("official_website", ""),
            "articles": [],
        }
        if not journal_name:
            entry["error"] = "缺少 journal_name，已跳过"
            journals_output.append(entry)
            continue
        try:
            entry["articles"] = fetch_articles_for_journal(
                config=config,
                journal_name=journal_name,
                start_date=start_date,
                end_date=end_date,
            )
        except Exception as exc:
            entry["error"] = f"{type(exc).__name__}: {exc}"
        journals_output.append(entry)
        if index < len(scope_review) - 1:
            time.sleep(float(config["pubmed"]["delay_seconds_between_requests"]))
    return {
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "journals": journals_output,
    }


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# Set2 PubMed 近 3 个月论文证据",
        "",
        f"- 生成时间：{summary['generated_at']}",
        f"- 检索时间窗：{summary['start_date']} 至 {summary['end_date']}",
        "",
    ]
    for journal in summary["journals"]:
        lines.append(f"## {journal['journal_name']}")
        lines.append("")
        if journal.get("error"):
            lines.append(f"- 检索失败：{journal['error']}")
            lines.append("")
            continue
        if not journal["articles"]:
            lines.append("- PubMed 最近 3 个月未检索到可用论文，或该刊在 PubMed 收录不足。")
            lines.append("")
            continue
        lines.append("| 日期 | 标题 | 摘要 | PMID |")
        lines.append("| --- | --- | --- | --- |")
        for article in journal["articles"]:
            lines.append(
                "| {date} | {title} | {abstract} | [PMID {pmid}]({url}) |".format(
                    date=article["publication_date"] or "未知",
                    title=compact_text(article["title"], 100).replace("|", "/"),
                    abstract=compact_text(article.get("abstract", ""), 140).replace("|", "/"),
                    pmid=article["pmid"] or "N/A",
                    url=article["url"] or "https://pubmed.ncbi.nlm.nih.gov/",
                )
            )
        lines.append("")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="抓取 Set2 期刊最近 3 个月 PubMed 论文")
    parser.add_argument("--workspace", required=True, help="隐藏工作区 run 根目录")
    parser.add_argument("--profile", required=True, help="manuscript_profile.json 路径")
    parser.add_argument("--scope-review", required=True, help="set2_scope_review.json 路径")
    parser.add_argument("--today", default="", help="覆盖今天日期，格式 YYYY-MM-DD")
    args = parser.parse_args()

    config = load_config()
    workspace = resolve_path(args.workspace)
    _ = read_json(resolve_path_within(args.profile, parent=workspace, label="profile"))
    scope_review = normalize_scope_review(
        read_json(resolve_path_within(args.scope_review, parent=workspace, label="scope-review"))
    )
    end_date = dt.date.fromisoformat(args.today) if args.today else dt.date.today()
    payload = build_pubmed_summary(
        config=config,
        scope_review=scope_review,
        end_date=end_date,
    )
    json_path = workspace_output_path(workspace, config["reports"]["pubmed_json"])
    markdown_path = workspace_output_path(workspace, config["reports"]["pubmed_markdown"])
    write_json(json_path, payload)
    write_text(markdown_path, render_markdown(payload))
    print(f"pubmed_json={json_path}")
    print(f"pubmed_markdown={markdown_path}")


if __name__ == "__main__":
    main()
