"""Small OpenAlex adapter; provider responses stay outside the paper contract."""

from __future__ import annotations

from typing import Any


def search(query: str, *, max_results: int = 50, min_year: int | None = None, max_year: int | None = None, mailto: str | None = None, timeout: float = 30, session: Any = None, **_: Any) -> list[dict[str, Any]]:
    import requests

    params: dict[str, Any] = {"search": query, "per-page": max(1, min(int(max_results), 200))}
    filters: list[str] = []
    if min_year is not None:
        filters.append(f"from_publication_date:{int(min_year)}-01-01")
    if max_year is not None:
        filters.append(f"to_publication_date:{int(max_year)}-12-31")
    if filters:
        params["filter"] = ",".join(filters)
    if mailto:
        params["mailto"] = mailto
    client = session or requests
    response = client.get("https://api.openalex.org/works", params=params, timeout=timeout)
    response.raise_for_status()
    data = response.json()
    return list(data.get("results") or [])[: int(max_results)]
