"""Crossref adapter used as DOI-aware fallback."""

from __future__ import annotations

from typing import Any


def search(query: str, *, max_results: int = 50, timeout: float = 30, mailto: str | None = None, session: Any = None, **_: Any) -> list[dict[str, Any]]:
    import requests

    params = {"query": query, "rows": max(1, min(int(max_results), 100))}
    headers = {"User-Agent": "research-literature-search/1.0" + (f" (mailto:{mailto})" if mailto else "")}
    client = session or requests
    response = client.get("https://api.crossref.org/works", params=params, headers=headers, timeout=timeout)
    response.raise_for_status()
    return list((response.json().get("message") or {}).get("items") or [])[: int(max_results)]
