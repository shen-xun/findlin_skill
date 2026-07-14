"""Direct crawl of 中文信息学报官网检索与当期目录。"""
from __future__ import annotations

import re

import requests
from bs4 import BeautifulSoup

from .base import SESSION, paper_dict, query_relevance, throttle

JCIP_SEARCH = "https://jcip.cipsc.org.cn/CN/article/showArticleByKeyword.do"
JCIP_CURRENT = "https://jcip.cipsc.org.cn/CN/current"


def _parse_jcip_articles(html: str, journal: dict, query: str, min_year: int, max_results: int, source: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    papers = []
    seen: set[str] = set()

    for row in soup.select("table tr, .article-list li, .noselectrow"):
        text = row.get_text(" ", strip=True)
        if len(text) < 10:
            continue
        link = row.find("a", href=True)
        if not link:
            continue
        title = link.get_text(strip=True)
        if len(title) < 6 or title in seen:
            continue
        href = link["href"]
        if not href.startswith("http"):
            href = "https://jcip.cipsc.org.cn" + href
        year = None
        ym = re.search(r"(20\d{2})", text)
        if ym:
            year = int(ym.group(1))
        if year and year < min_year:
            continue
        score = query_relevance(query, title, text)
        if score <= 0 and query:
            continue
        seen.add(title)
        p = paper_dict(
            title=title,
            authors=[],
            year=year,
            journal=journal["display_name"],
            journal_id=journal["id"],
            url=href,
            source=source,
        )
        p["relevance_score"] = score
        papers.append(p)
        if len(papers) >= max_results:
            break
    return papers


def search_jcip(
    journal: dict,
    query: str,
    max_results: int,
    min_year: int,
) -> list[dict]:
    papers: list[dict] = []

    # Keyword search on official site
    try:
        throttle()
        resp = SESSION.get(
            JCIP_SEARCH,
            params={"keyword": query},
            timeout=20,
        )
        if resp.status_code == 200:
            papers.extend(_parse_jcip_articles(
                resp.text, journal, query, min_year, max_results,
                source=f"jcip:{JCIP_SEARCH}",
            ))
    except requests.RequestException:
        pass

    # Fallback: current issue TOC
    if len(papers) < max_results:
        try:
            throttle()
            resp = SESSION.get(JCIP_CURRENT, timeout=20)
            if resp.status_code == 200:
                toc = _parse_jcip_articles(
                    resp.text, journal, query, min_year, max_results - len(papers),
                    source=f"jcip:{JCIP_CURRENT}",
                )
                seen = {p["title"] for p in papers}
                for p in toc:
                    if p["title"] not in seen:
                        papers.append(p)
        except requests.RequestException:
            pass

    return papers[:max_results]
