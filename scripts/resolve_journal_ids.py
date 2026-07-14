#!/usr/bin/env python3
"""Resolve OpenAlex source IDs for journals in journals.json."""
import json
import sys
import time
from pathlib import Path

import requests

JOURNALS_PATH = Path(__file__).resolve().parent.parent / "journals.json"
OPENALEX = "https://api.openalex.org/sources"
MAILTO = "linguistics-skill@openalex.local"

# ISSN 在 OpenAlex 中缺失时的手工映射（经样本论文验证）
MANUAL_OVERRIDES: dict[str, str] = {
    "syntax": "S44683723",
    "phonology": "S23261261",
    "linguistics-vanguard": "S4210237318",
    "language-and-linguistics": "S39669439",
}


def resolve_journal(journal: dict) -> str | None:
    if journal["id"] in MANUAL_OVERRIDES:
        return MANUAL_OVERRIDES[journal["id"]]
    """Resolve OpenAlex source ID via ISSN first, then name search."""
    params: dict = {"mailto": MAILTO, "per_page": 5}

    if journal.get("issn"):
        params["filter"] = f"issn:{journal['issn'][0]}"
        resp = requests.get(OPENALEX, params=params, timeout=30)
        resp.raise_for_status()
        results = resp.json().get("results", [])
        if results:
            return results[0]["id"].split("/")[-1]

    params = {
        "search": journal.get("search_aliases", [journal["display_name"]])[0],
        "filter": "type:journal",
        "mailto": MAILTO,
        "per_page": 10,
    }
    resp = requests.get(OPENALEX, params=params, timeout=30)
    resp.raise_for_status()
    target = journal["display_name"].lower()
    for r in resp.json().get("results", []):
        name = r["display_name"].lower()
        if target in name or name in target:
            return r["id"].split("/")[-1]
    return None


def main() -> None:
    journals = json.loads(JOURNALS_PATH.read_text(encoding="utf-8"))
    for j in journals:
        if j.get("openalex_source_id"):
            print(f"SKIP {j['display_name']}: {j['openalex_source_id']}")
            continue
        sid = resolve_journal(j)
        j["openalex_source_id"] = sid or ""
        print(f"{j['display_name']}: {sid or 'NOT FOUND'}")
        time.sleep(0.2)

    JOURNALS_PATH.write_text(
        json.dumps(journals, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    missing = [j["display_name"] for j in journals if not j["openalex_source_id"]]
    if missing:
        print(f"\nWARNING: unresolved: {missing}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
