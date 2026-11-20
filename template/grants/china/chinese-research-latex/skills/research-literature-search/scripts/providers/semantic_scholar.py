"""Semantic Scholar adapter."""

from __future__ import annotations

from typing import Any


def search(query: str, *, max_results: int = 50, timeout: float = 30, session: Any = None, **_: Any) -> list[dict[str, Any]]:
    import requests

    params = {"query": query, "limit": max(1, min(int(max_results), 100)), "fields": "title,abstract,authors,year,venue,externalIds,url,publicationTypes"}
    client = session or requests
    response = client.get("https://api.semanticscholar.org/graph/v1/paper/search", params=params, timeout=timeout)
    response.raise_for_status()
    return list(response.json().get("data") or [])[: int(max_results)]
