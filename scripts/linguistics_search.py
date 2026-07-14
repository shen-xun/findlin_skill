#!/usr/bin/env python3
"""Search linguistics journals via OpenAlex API."""
import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path

import requests

SKILL_DIR = Path(__file__).resolve().parent.parent
JOURNALS_PATH = SKILL_DIR / "journals.json"
OPENALEX_WORKS = "https://api.openalex.org/works"
MAILTO = "linguistics-skill@openalex.local"


def load_journals(journal_ids: list[str] | None) -> list[dict]:
    journals = json.loads(JOURNALS_PATH.read_text(encoding="utf-8"))
    if journal_ids:
        id_set = set(journal_ids)
        journals = [j for j in journals if j["id"] in id_set]
    return [j for j in journals if j.get("openalex_source_id")]


def reconstruct_abstract(inverted_index: dict | None) -> str:
    if not inverted_index:
        return ""
    max_pos = max(pos for positions in inverted_index.values() for pos in positions)
    words = [""] * (max_pos + 1)
    for word, positions in inverted_index.items():
        for pos in positions:
            words[pos] = word
    return " ".join(words).strip()


def search_journal(
    journal: dict, query: str, max_results: int, min_year: int
) -> list[dict]:
    params = {
        "search": query,
        "filter": (
            f"primary_location.source.id:{journal['openalex_source_id']},"
            f"publication_year:>{min_year - 1}"
        ),
        "sort": "relevance_score:desc",
        "per_page": max_results,
        "mailto": MAILTO,
    }
    resp = requests.get(OPENALEX_WORKS, params=params, timeout=30)
    resp.raise_for_status()
    papers = []
    for w in resp.json().get("results", []):
        papers.append({
            "title": w.get("title") or "",
            "authors": [
                a.get("author", {}).get("display_name", "")
                for a in w.get("authorships", [])
            ],
            "year": w.get("publication_year"),
            "journal": journal["display_name"],
            "journal_id": journal["id"],
            "doi": (w.get("doi") or "").replace("https://doi.org/", ""),
            "cited_by_count": w.get("cited_by_count") or 0,
            "abstract": reconstruct_abstract(w.get("abstract_inverted_index")),
            "openalex_id": (w.get("id") or "").split("/")[-1],
            "relevance_score": w.get("relevance_score") or 0,
        })
    return papers


def deduplicate(papers: list[dict]) -> list[dict]:
    seen: set[str] = set()
    unique = []
    for p in papers:
        key = p["doi"] or p["title"].lower().strip()
        if key and key not in seen:
            seen.add(key)
            unique.append(p)
    return unique


def main() -> None:
    parser = argparse.ArgumentParser(description="Search linguistics journals")
    parser.add_argument("query", help="Search query (English keywords)")
    parser.add_argument("--journals", help="Comma-separated journal IDs")
    parser.add_argument("--max-per-journal", type=int, default=5)
    parser.add_argument("--years", type=int, default=15, help="Look back N years")
    parser.add_argument("--min-citations", type=int, default=0)
    parser.add_argument("--max-total", type=int, default=30, help="Cap total results")
    parser.add_argument("-o", "--output", help="Write JSON to file (avoids Windows console encoding issues)")
    args = parser.parse_args()

    min_year = datetime.now().year - args.years
    journal_ids = [j.strip() for j in args.journals.split(",")] if args.journals else None
    journals = load_journals(journal_ids)

    if not journals:
        print(json.dumps({"error": "No journals with resolved OpenAlex IDs"}, ensure_ascii=False))
        sys.exit(1)

    all_papers: list[dict] = []
    for j in journals:
        try:
            papers = search_journal(j, args.query, args.max_per_journal, min_year)
            all_papers.extend(papers)
            time.sleep(0.15)
        except requests.RequestException as e:
            print(f"WARN: {j['display_name']}: {e}", file=sys.stderr)

    all_papers = deduplicate(all_papers)
    all_papers = [p for p in all_papers if p["cited_by_count"] >= args.min_citations]
    all_papers.sort(
        key=lambda p: (p["relevance_score"], p["cited_by_count"]), reverse=True
    )
    all_papers = all_papers[: args.max_total]

    result = {"query": args.query, "total": len(all_papers), "papers": all_papers}
    output = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(output + "\n", encoding="utf-8")
    else:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        print(output)


if __name__ == "__main__":
    main()
