"""RSS feed crawl for latest TOC, filtered by query keywords."""
from __future__ import annotations

import xml.etree.ElementTree as ET

from .base import SESSION, paper_dict, query_relevance, throttle, year_from_date_parts

NS = {"atom": "http://www.w3.org/2005/Atom", "dc": "http://purl.org/dc/elements/1.1/"}


def search_rss_recent(
    journal: dict,
    query: str,
    max_results: int,
    min_year: int,
) -> list[dict]:
    rss_url = journal.get("crawl_config", {}).get("rss_url")
    if not rss_url:
        return []

    throttle()
    resp = SESSION.get(rss_url, timeout=30)
    resp.raise_for_status()
    root = ET.fromstring(resp.content)

    papers = []
    for entry in root.findall("atom:entry", NS) + root.findall("entry"):
        title_el = entry.find("atom:title", NS) or entry.find("title")
        link_el = entry.find("atom:link", NS) or entry.find("link")
        date_el = entry.find("atom:published", NS) or entry.find("published") or entry.find("dc:date", NS)
        if title_el is None:
            continue
        title = (title_el.text or "").strip()
        url = link_el.get("href", "") if link_el is not None else ""
        if link_el is not None and not url:
            url = link_el.text or ""
        published = (date_el.text or "")[:10] if date_el is not None else ""
        year = int(published[:4]) if len(published) >= 4 else None
        if year and year < min_year:
            continue
        score = query_relevance(query, title)
        if score <= 0:
            continue
        p = paper_dict(
            title=title,
            authors=[],
            year=year,
            journal=journal["display_name"],
            journal_id=journal["id"],
            url=url,
            source=f"rss:{rss_url}",
            published=published,
        )
        p["relevance_score"] = score
        papers.append(p)
        if len(papers) >= max_results:
            break
    return papers
