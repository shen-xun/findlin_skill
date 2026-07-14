"""Shared types and HTTP helpers for journal crawlers."""
from __future__ import annotations

import re
import time
from typing import Any

import requests

USER_AGENT = "findlin-skill/1.0 (mailto:linguistics-skill@openalex.local)"
SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": USER_AGENT,
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8",
})

REQUEST_DELAY = 0.4


def throttle() -> None:
    time.sleep(REQUEST_DELAY)


def normalize_title(title: str) -> str:
    title = re.sub(r"<[^>]+>", "", title)
    return re.sub(r"\s+", " ", title).strip()


def paper_dict(
    *,
    title: str,
    authors: list[str],
    year: int | None,
    journal: str,
    journal_id: str,
    doi: str = "",
    abstract: str = "",
    url: str = "",
    source: str = "",
    published: str = "",
) -> dict[str, Any]:
    return {
        "title": normalize_title(title),
        "authors": authors,
        "year": year,
        "journal": journal,
        "journal_id": journal_id,
        "doi": doi.replace("https://doi.org/", "") if doi.startswith("http") else doi,
        "abstract": abstract.strip(),
        "url": url,
        "source": source,
        "published": published,
        "cited_by_count": 0,
        "relevance_score": 0.0,
    }


def year_from_date_parts(parts: list | None) -> int | None:
    if parts and isinstance(parts, list) and parts and isinstance(parts[0], list):
        return int(parts[0][0])
    return None


def query_relevance(query: str, title: str, abstract: str = "") -> float:
    """Simple keyword overlap score for ranking."""
    q_tokens = {t for t in re.findall(r"[a-z0-9\u4e00-\u9fff]+", query.lower()) if len(t) > 2}
    if not q_tokens:
        return 0.0
    text = f"{title} {abstract}".lower()
    hits = sum(1 for t in q_tokens if t in text)
    return hits / len(q_tokens)
