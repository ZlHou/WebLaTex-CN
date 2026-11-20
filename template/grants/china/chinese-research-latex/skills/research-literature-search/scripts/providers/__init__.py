"""Provider adapters used by research-literature-search."""

from .crossref import search as search_crossref
from .openalex import search as search_openalex
from .semantic_scholar import search as search_semantic_scholar

__all__ = ["search_openalex", "search_semantic_scholar", "search_crossref"]
