"""CrossRef: publisher-indexed metadata, sorted by latest publication date."""
from __future__ import annotations

from .base import SESSION, paper_dict, query_relevance, throttle, year_from_date_parts

CROSSREF_API = "https://api.crossref.org/works"


def _extract_abstract(item: dict) -> str:
    abs_val = item.get("abstract")
    if not abs_val:
        return ""
    import re
    return re.sub(r"<[^>]+>", "", abs_val).strip()


def search_crossref(
    journal: dict,
    query: str,
    max_results: int,
    min_year: int,
) -> list[dict]:
    issn = journal["issn"][0]
    params = {
        "query": query,
        "filter": f"issn:{issn},from-pub-date:{min_year}",
        "sort": "published",
        "order": "desc",
        "rows": max_results,
    }
    throttle()
    resp = SESSION.get(CROSSREF_API, params=params, timeout=30)
    resp.raise_for_status()
    items = resp.json().get("message", {}).get("items", [])

    papers = []
    for item in items:
        title = (item.get("title") or [""])[0]
        authors = [
            " ".join(filter(None, [
                (a.get("given") or ""),
                (a.get("family") or ""),
            ])).strip()
            for a in item.get("author", [])
        ]
        pub = item.get("published-print") or item.get("published-online") or item.get("created") or {}
        year = year_from_date_parts(pub.get("date-parts"))
        doi = item.get("DOI", "")
        abstract = _extract_abstract(item)
        url = item.get("URL") or (f"https://doi.org/{doi}" if doi else journal.get("homepage", ""))
        published = "-".join(str(x) for x in (pub.get("date-parts") or [[""]])[0][:3] if x)

        p = paper_dict(
            title=title,
            authors=authors,
            year=year,
            journal=journal["display_name"],
            journal_id=journal["id"],
            doi=doi,
            abstract=abstract,
            url=url,
            source=f"crossref:{journal.get('homepage', issn)}",
            published=published,
        )
        p["relevance_score"] = query_relevance(query, p["title"], p["abstract"])
        papers.append(p)
    return papers
