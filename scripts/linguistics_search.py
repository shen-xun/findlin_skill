#!/usr/bin/env python3
"""Search linguistics journals by crawling official publisher sites."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

from crawlers import search_crossref, search_jcip, search_rss_recent, search_springer

SKILL_DIR = Path(__file__).resolve().parent.parent
JOURNALS_PATH = SKILL_DIR / "journals.json"

CRAWLERS = {
    "crossref": search_crossref,
    "springer": search_springer,
    "rss": search_rss_recent,
    "jcip": search_jcip,
}


def load_journals(journal_ids: list[str] | None) -> list[dict]:
    journals = json.loads(JOURNALS_PATH.read_text(encoding="utf-8"))
    if journal_ids:
        id_set = set(journal_ids)
        journals = [j for j in journals if j["id"] in id_set]
    return journals


def crawl_journal(
    journal: dict,
    query: str,
    max_results: int,
    min_year: int,
) -> list[dict]:
    methods = journal.get("crawl_methods", ["crossref"])
    papers: list[dict] = []
    seen: set[str] = set()

    for method in methods:
        fn = CRAWLERS.get(method)
        if not fn:
            continue
        try:
            batch = fn(journal, query, max_results, min_year)
        except Exception as exc:
            print(f"WARN: {journal['display_name']} [{method}]: {exc}", file=sys.stderr)
            continue
        for p in batch:
            key = p.get("doi") or p["title"].lower().strip()
            if key and key not in seen:
                seen.add(key)
                papers.append(p)

    papers.sort(key=lambda p: (p.get("relevance_score", 0), p.get("year") or 0), reverse=True)
    return papers[:max_results]


def deduplicate(papers: list[dict]) -> list[dict]:
    seen: set[str] = set()
    unique = []
    for p in papers:
        key = p.get("doi") or p["title"].lower().strip()
        if key and key not in seen:
            seen.add(key)
            unique.append(p)
    return unique


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Crawl official journal sites for latest research"
    )
    parser.add_argument("query", help="Search query (English or Chinese keywords)")
    parser.add_argument(
        "--journals",
        help="Comma-separated journal IDs (default: all 23 journals)",
    )
    parser.add_argument("--max-per-journal", type=int, default=3)
    parser.add_argument("--years", type=int, default=10, help="Look back N years (default 10 for latest)")
    parser.add_argument("--max-total", type=int, default=60, help="Cap total results after dedup")
    parser.add_argument("-o", "--output", help="Write JSON results to file")
    args = parser.parse_args()

    min_year = datetime.now().year - args.years
    journal_ids = [j.strip() for j in args.journals.split(",")] if args.journals else None
    journals = load_journals(journal_ids)

    if not journals:
        print(json.dumps({"error": "No matching journals found"}, ensure_ascii=False))
        sys.exit(1)

    all_papers: list[dict] = []
    crawl_log: list[dict] = []
    for j in journals:
        papers = crawl_journal(j, args.query, args.max_per_journal, min_year)
        all_papers.extend(papers)
        crawl_log.append({
            "journal_id": j["id"],
            "journal": j["display_name"],
            "homepage": j.get("homepage", ""),
            "methods": j.get("crawl_methods", []),
            "hits": len(papers),
        })

    all_papers = deduplicate(all_papers)
    all_papers.sort(
        key=lambda p: (p.get("relevance_score", 0), p.get("year") or 0),
        reverse=True,
    )
    all_papers = all_papers[: args.max_total]

    result = {
        "query": args.query,
        "min_year": min_year,
        "strategy": "direct_site_crawl",
        "journals_crawled": len(journals),
        "total": len(all_papers),
        "crawl_log": crawl_log,
        "papers": all_papers,
    }
    output = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(output + "\n", encoding="utf-8")
    else:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        print(output)


if __name__ == "__main__":
    main()
