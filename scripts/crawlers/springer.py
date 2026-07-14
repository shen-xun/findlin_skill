"""Direct crawl of Springer Link journal search pages."""
from __future__ import annotations

import re

from bs4 import BeautifulSoup

from .base import SESSION, paper_dict, query_relevance, throttle, year_from_date_parts

SPRINGER_SEARCH = "https://link.springer.com/search"


def search_springer(
    journal: dict,
    query: str,
    max_results: int,
    min_year: int,
) -> list[dict]:
    journal_id = journal.get("crawl_config", {}).get("springer_journal_id")
    if not journal_id:
        return []

    params = {
        "query": query,
        "facet-content-type": "Article",
        "facet-journal-id": journal_id,
        "sortBy": "newestFirst",
    }
    throttle()
    resp = SESSION.get(SPRINGER_SEARCH, params=params, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    papers = []
    seen: set[str] = set()
    for link in soup.select("h2 a, h3 a, a.title"):
        title = link.get_text(strip=True)
        if len(title) < 12 or title in seen:
            continue
        href = link.get("href", "")
        if not href.startswith("http"):
            href = "https://link.springer.com" + href
        seen.add(title)

        year = None
        parent = link.find_parent("li") or link.find_parent("div")
        if parent:
            m = re.search(r"(20\d{2})", parent.get_text(" ", strip=True))
            if m:
                year = int(m.group(1))
        if year and year < min_year:
            continue

        p = paper_dict(
            title=title,
            authors=[],
            year=year,
            journal=journal["display_name"],
            journal_id=journal["id"],
            url=href,
            source=f"springer:{journal.get('homepage', '')}",
        )
        p["relevance_score"] = query_relevance(query, p["title"])
        papers.append(p)
        if len(papers) >= max_results:
            break
    return papers
