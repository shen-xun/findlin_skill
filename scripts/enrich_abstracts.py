#!/usr/bin/env python3
"""Enrich paper abstracts from Semantic Scholar when OpenAlex has none."""
import json
import sys
import time

import requests

S2_API = "https://api.semanticscholar.org/graph/v1/paper"
DELAY = 1.0  # respect rate limits


def enrich_from_s2(paper: dict) -> dict:
    if paper.get("abstract") or not paper.get("doi"):
        return paper
    url = f"{S2_API}/DOI:{paper['doi']}"
    try:
        resp = requests.get(url, params={"fields": "abstract"}, timeout=15)
        if resp.status_code == 200:
            paper["abstract"] = resp.json().get("abstract") or ""
        elif resp.status_code == 429:
            time.sleep(5)
    except requests.RequestException:
        pass
    return paper


def main() -> None:
    data = json.load(sys.stdin)
    papers = data.get("papers", [])
    enriched = 0
    for p in papers:
        before = bool(p.get("abstract"))
        enrich_from_s2(p)
        if not before and p.get("abstract"):
            enriched += 1
        time.sleep(DELAY)
    data["abstracts_enriched"] = enriched
    output = json.dumps(data, ensure_ascii=False, indent=2)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
