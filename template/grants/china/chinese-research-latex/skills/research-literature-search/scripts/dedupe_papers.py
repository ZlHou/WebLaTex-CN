#!/usr/bin/env python3
"""Deterministic DOI/title-year deduplication for canonical candidates."""

from __future__ import annotations

import argparse
import json
import re
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

from candidate_schema import normalize_doi, normalize_record, normalize_year, validate_candidates


STOPWORDS = {"a", "an", "the", "and", "or", "of", "for", "in", "on", "to", "with", "from", "by", "via"}


def normalize_title(title: Any) -> str:
    text = re.sub(r"[\u3000\s]+", " ", str(title or "").strip().lower())
    text = re.sub(r"[\"'“”‘’]", "", text)
    text = re.sub(r"[^\w\s-]", " ", text, flags=re.UNICODE)
    text = re.sub(r"[-_]+", " ", text)
    return " ".join(token for token in re.sub(r"\s+", " ", text).strip().split() if token not in STOPWORDS)


def token_jaccard(left: str, right: str) -> float:
    a, b = set(left.split()), set(right.split())
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def is_preprint(record: dict[str, Any]) -> bool:
    pub = record.get("publication") if isinstance(record.get("publication"), dict) else {}
    if pub.get("is_preprint") is True:
        return True
    probe = f"{record.get('venue') or ''} {record.get('url') or ''}".lower()
    return any(token in probe for token in ("arxiv", "biorxiv", "medrxiv", "preprint"))


def quality_score(record: dict[str, Any]) -> int:
    score = 0
    if normalize_doi(record.get("doi") or (record.get("identifiers") or {}).get("doi")):
        score += 10
    if not is_preprint(record):
        score += 4
    if record.get("venue"):
        score += 2
    if normalize_year(record.get("year")):
        score += 1
    if isinstance(record.get("abstract"), str):
        score += min(2, len(record["abstract"]) // 400)
    return score


def merge_records(canonical: dict[str, Any], other: dict[str, Any]) -> dict[str, Any]:
    merged = dict(canonical)
    for key in ("title", "venue", "year", "published_date", "online_date", "url", "abstract"):
        if merged.get(key) in (None, "", []):
            if other.get(key) not in (None, "", []):
                merged[key] = other[key]
    if not merged.get("authors") and other.get("authors"):
        merged["authors"] = list(other["authors"])
    # Keep identifiers discovered by either provider.  A provisional preprint
    # can be merged before its published DOI-bearing record arrives.
    left_ids = canonical.get("identifiers") if isinstance(canonical.get("identifiers"), dict) else {}
    right_ids = other.get("identifiers") if isinstance(other.get("identifiers"), dict) else {}
    identifiers = {
        key: (left_ids.get(key) or right_ids.get(key))
        for key in ("doi", "pmid", "arxiv", "openalex", "semantic_scholar")
    }
    identifiers["doi"] = normalize_doi(identifiers.get("doi"))
    merged["identifiers"] = identifiers
    merged["sources"] = list({json.dumps(item, ensure_ascii=False, sort_keys=True): item for item in [*(merged.get("sources") or []), *(other.get("sources") or [])]}.values())
    merged["query_matches"] = sorted(set(merged.get("query_matches") or []) | set(other.get("query_matches") or []))
    merged["quality_warnings"] = sorted(set(merged.get("quality_warnings") or []) | set(other.get("quality_warnings") or []))
    merged["record_id"] = canonical.get("record_id") or other.get("record_id")
    # Keep flat compatibility fields aligned with canonical identifiers.
    ids = merged.get("identifiers") if isinstance(merged.get("identifiers"), dict) else {}
    merged["doi"] = normalize_doi(ids.get("doi") or merged.get("doi"))
    for key, flat in (("pmid", "pmid"), ("openalex", "openalex_id"), ("semantic_scholar", "semantic_scholar_id"), ("arxiv", "arxiv_id")):
        merged[flat] = ids.get(key) or merged.get(flat)
    return merged


def dedupe_records(records: list[dict[str, Any]], *, title_similarity: float = .92, token_threshold: float = .80, year_window: int = 1) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    canonical: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    doi_index: dict[str, int] = {}
    for source_index, record in enumerate(records):
        title = normalize_title(record.get("title"))
        year = normalize_year(record.get("year"))
        identifiers = record.get("identifiers") if isinstance(record.get("identifiers"), dict) else {}
        doi = normalize_doi(record.get("doi") or identifiers.get("doi"))
        match_index: int | None = doi_index.get(doi) if doi else None
        best: tuple[float, float, int, str] | None = None
        if match_index is None and title:
            for index, existing in enumerate(canonical):
                existing_title = normalize_title(existing.get("title"))
                existing_year = normalize_year(existing.get("year"))
                if year is not None and existing_year is not None and abs(year - existing_year) > year_window:
                    continue
                similarity = SequenceMatcher(None, title, existing_title).ratio()
                jaccard = token_jaccard(title, existing_title)
                existing_doi = normalize_doi(existing.get("doi") or (existing.get("identifiers") or {}).get("doi"))
                cross_version = bool((doi and not existing_doi and is_preprint(existing)) or (existing_doi and not doi and is_preprint(record)))
                cross_doi = bool(doi and existing_doi and doi != existing_doi)
                if (cross_doi or cross_version) and not (is_preprint(record) or is_preprint(existing)):
                    continue
                required_similarity = .97 if (cross_doi or cross_version) else title_similarity
                if similarity >= required_similarity and jaccard >= token_threshold:
                    reason = "cross_doi_preprint_to_published" if (cross_doi or cross_version) else "fuzzy_title_year"
                    candidate = (similarity, jaccard, index, reason)
                    if best is None or candidate[:2] > best[:2]:
                        best = candidate
            if best is not None:
                _, _, match_index, reason = best
            else:
                reason = ""
        if match_index is None:
            match_index = len(canonical)
            canonical.append(record)
            if doi:
                doi_index[doi] = match_index
            continue
        existing = canonical[match_index]
        existing_id = existing.get("record_id")
        incoming_id = record.get("record_id")
        incoming_wins = quality_score(record) > quality_score(existing)
        if incoming_wins:
            canonical[match_index] = merge_records(record, existing)
            canonical[match_index]["record_id"] = incoming_id or existing_id
        else:
            canonical[match_index] = merge_records(existing, record)
        chosen = canonical[match_index]
        chosen_doi = normalize_doi(chosen.get("doi") or (chosen.get("identifiers") or {}).get("doi"))
        if chosen_doi:
            doi_index[chosen_doi] = match_index
        edges.append({
            "canonical_record_id": chosen.get("record_id"),
            "merged_record_id": existing_id if incoming_wins else incoming_id,
            "reason": "same_doi" if doi and normalize_doi(existing.get("doi") or (existing.get("identifiers") or {}).get("doi")) == doi else (reason or "fuzzy_title_year"),
            "source_index": source_index,
            "similarity": 1.0 if doi and normalize_doi(existing.get("doi") or (existing.get("identifiers") or {}).get("doi")) == doi else (best[0] if best else 0.0),
            "jaccard": 1.0 if doi and normalize_doi(existing.get("doi") or (existing.get("identifiers") or {}).get("doi")) == doi else (best[1] if best else 0.0),
        })
    return canonical, edges


def read_jsonl(path: Path) -> list[Any]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(item, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n" for item in records), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Deduplicate rls.paper.v1 candidates")
    parser.add_argument("--input", "-i", required=True, type=Path)
    parser.add_argument("--output", "-o", required=True, type=Path)
    parser.add_argument("--map", required=True, type=Path)
    parser.add_argument("--title-sim", type=float, default=.92)
    parser.add_argument("--token-jaccard", type=float, default=.80)
    parser.add_argument("--year-window", type=int, default=1)
    args = parser.parse_args()
    raw = read_jsonl(args.input)
    candidates: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    for index, item in enumerate(raw, 1):
        if item is None:
            skipped.append({"index": index, "code": "empty_record"})
            continue
        if not isinstance(item, dict):
            skipped.append({"index": index, "code": "invalid_record_type", "type": type(item).__name__})
            continue
        candidates.append(normalize_record(item, provider=str(item.get("source") or "legacy"), fallback_index=index))
    _, errors = validate_candidates(candidates)
    if errors:
        parser.error("invalid candidates: " + "; ".join(errors[:5]))
    result, edges = dedupe_records(candidates, title_similarity=args.title_sim, token_threshold=args.token_jaccard, year_window=args.year_window)
    write_jsonl(args.output, result)
    args.map.parent.mkdir(parents=True, exist_ok=True)
    args.map.write_text(json.dumps({"schema_version": "rls.dedupe.v1", "input_count": len(raw), "valid_input_count": len(candidates), "skipped_records": skipped, "output_count": len(result), "merged_count": len(edges), "cross_doi_preprint_merges": sum(1 for edge in edges if edge["reason"] == "cross_doi_preprint_to_published"), "params": {"title_similarity_threshold": args.title_sim, "token_jaccard_threshold": args.token_jaccard, "year_window": args.year_window}, "edges": edges}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
