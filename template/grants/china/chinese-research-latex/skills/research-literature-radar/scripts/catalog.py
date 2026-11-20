#!/usr/bin/env python3
"""Lightweight, offline helpers for research-literature-radar catalogues."""
from __future__ import annotations
import argparse, hashlib, json, re, unicodedata
from pathlib import Path

def normalize_title(title: str) -> str:
    text = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode().lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()

def slug(value: str, limit: int = 64) -> str:
    value = normalize_title(value).replace(" ", "-")
    return value[:limit].strip("-") or "untitled"


# Short, recognizable names keep the human-facing ID useful without making it
# a duplicate of the full title.  The fallback remains deterministic for new
# papers whose method name is not in this table.
KEYWORD_ALIASES = (
    ("efficient estimation of word representations", "word2vec"),
    ("very deep convolutional networks", "vgg"),
    ("sequence to sequence learning", "seq2seq"),
    ("going deeper with convolutions", "inception"),
    ("dropout", "dropout"),
    ("adam", "adam"),
    ("generative adversarial", "gan"),
    ("batch normalization", "batchnorm"),
    ("deep residual learning", "resnet"),
    ("attention is all you need", "transformer"),
    ("neural ordinary differential", "neural-ode"),
    ("bert", "bert"),
    ("scaling laws", "scaling-laws"),
    ("simple framework for contrastive", "simclr"),
    ("language models are few shot", "gpt3"),
    ("denoising diffusion", "ddpm"),
    ("an image is worth", "vit"),
    ("score based generative", "score-sde"),
    ("transferable visual models", "clip"),
    ("swin transformer", "swin-transformer"),
    ("lora", "lora"),
    ("masked autoencoders", "mae"),
    ("chain of thought", "chain-of-thought"),
    ("follow instructions with human feedback", "rlhf"),
    ("flashattention", "flashattention"),
    ("react", "react"),
    ("dinov2", "dinov2"),
    ("tree of thoughts", "tree-of-thoughts"),
    ("mamba", "mamba"),
    ("deepseek r1", "deepseek-r1"),
)


def keyword_slug(title: str) -> str:
    normalized = normalize_title(title)
    for phrase, keyword in KEYWORD_ALIASES:
        if phrase in normalized:
            return keyword
    # Keep a useful, bounded fallback for papers without a known short name.
    return slug(title, 32)


def friendly_id(paper: dict) -> str:
    """Build a human-readable, stable ID from author, year and a short keyword."""
    authors = paper.get("authors") or ["unknown"]
    author = slug(str(authors[0]), 40)
    year = str(paper.get("year", "undated"))
    keyword = slug(str(paper.get("keyword") or keyword_slug(paper.get("title", "untitled"))), 40)
    return f"{author}-{year}-{keyword}"


def make_id(paper: dict, existing_ids: set[str] | None = None) -> str:
    """Return a friendly ID, adding a stable suffix only on collision."""
    candidate = friendly_id(paper)
    if existing_ids and candidate in existing_ids:
        digest = hashlib.sha1(normalize_title(paper.get("title", "")).encode()).hexdigest()[:8]
        candidate = f"{candidate}-{digest}"
    return candidate

def load_catalog(path: Path) -> list[dict]:
    if not path.exists(): return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip(): rows.append(json.loads(line))
    return rows

def duplicate_of(paper: dict, rows: list[dict]) -> tuple[str|None, str|None]:
    ids = paper.get("identifiers") or {}
    for row in rows:
        rid = row.get("identifiers") or {}
        for key in ("doi", "arxiv", "openreview"):
            left = str(ids.get(key, "")).lower().strip()
            right = str(rid.get(key, "")).lower().strip()
            if key == "arxiv":
                left = re.sub(r"v\d+$", "", left.removeprefix("arxiv:"))
                right = re.sub(r"v\d+$", "", right.removeprefix("arxiv:"))
            if left and right and left == right:
                return row.get("id"), key
        paper_title = normalize_title(paper.get("title", ""))
        row_title = normalize_title(row.get("title", ""))
        paper_authors = paper.get("authors") or []
        row_authors = row.get("authors") or []
        if paper_title and row_title and paper_authors and row_authors and paper_title == row_title:
            pa = str(paper_authors[0]).split()[-1].lower()
            ra = str(row_authors[0]).split()[-1].lower()
            if pa and pa == ra and str(paper.get("year", "")) == str(row.get("year", "")):
                return row.get("id"), "title-author-year"
    return None, None

def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("id"); p.add_argument("json")
    p = sub.add_parser("dedupe"); p.add_argument("catalog"); p.add_argument("paper")
    args = parser.parse_args()
    if args.cmd == "id": print(make_id(json.loads(Path(args.json).read_text())))
    else:
        rows = load_catalog(Path(args.catalog)); paper = json.loads(Path(args.paper).read_text())
        rid, reason = duplicate_of(paper, rows)
        print(json.dumps({"duplicate_of": rid, "reason": reason}, ensure_ascii=False))

if __name__ == "__main__": main()
