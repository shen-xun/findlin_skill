#!/usr/bin/env python3
"""One-time migration: add website crawl metadata to journals.json."""
import json
from pathlib import Path

JOURNALS_PATH = Path(__file__).resolve().parent.parent / "journals.json"

SITE_META: dict[str, dict] = {
    "annual-review-linguistics": {
        "homepage": "https://www.annualreviews.org/journal/linguistics",
        "search_page": "https://www.annualreviews.org/action/doSearch?AllField={query}&SeriesKey=linguistics",
        "crawl_methods": ["crossref"],
        "publisher": "Annual Reviews",
    },
    "language": {
        "homepage": "https://www.linguisticsociety.org/language",
        "search_page": "https://www.linguisticsociety.org/page/language-issues",
        "crawl_methods": ["crossref"],
        "publisher": "LSA / Wiley",
    },
    "linguistic-inquiry": {
        "homepage": "https://direct.mit.edu/ling",
        "search_page": "https://direct.mit.edu/ling/search-results?q={query}",
        "crawl_methods": ["crossref"],
        "publisher": "MIT Press",
    },
    "corpus-linguistics-theory": {
        "homepage": "https://www.degruyter.com/journal/key/cllt/html",
        "search_page": "https://www.degruyter.com/search?query={query}&documentVisibility=all&subjectFacet=CLLT",
        "crawl_methods": ["crossref"],
        "publisher": "De Gruyter",
    },
    "nllt": {
        "homepage": "https://link.springer.com/journal/11049",
        "search_page": "https://link.springer.com/search?query={query}&facet-journal-id=11049",
        "crawl_methods": ["crossref", "springer"],
        "publisher": "Springer",
        "crawl_config": {"springer_journal_id": "11049"},
    },
    "journal-of-linguistics": {
        "homepage": "https://www.cambridge.org/core/journals/journal-of-linguistics",
        "search_page": "https://www.cambridge.org/core/search?q={query}&journalCode=LIN",
        "crawl_methods": ["crossref"],
        "publisher": "Cambridge",
    },
    "linguistics-de-gruyter": {
        "homepage": "https://www.degruyter.com/journal/key/ling/html",
        "search_page": "https://www.degruyter.com/search?query={query}&subjectFacet=LING",
        "crawl_methods": ["crossref"],
        "publisher": "De Gruyter",
    },
    "lingua": {
        "homepage": "https://www.sciencedirect.com/journal/lingua",
        "search_page": "https://www.sciencedirect.com/search?qs={query}&pub=lingua",
        "crawl_methods": ["crossref"],
        "publisher": "Elsevier",
    },
    "glossa": {
        "homepage": "https://www.glossa-journal.org",
        "search_page": "https://www.glossa-journal.org/search/?q={query}",
        "crawl_methods": ["crossref", "rss"],
        "publisher": "Open Library of Humanities",
        "crawl_config": {"rss_url": "https://www.glossa-journal.org/rss/current.xml"},
    },
    "journal-of-semantics": {
        "homepage": "https://academic.oup.com/jos",
        "search_page": "https://academic.oup.com/jos/search-results?q={query}",
        "crawl_methods": ["crossref"],
        "publisher": "Oxford University Press",
    },
    "natural-language-semantics": {
        "homepage": "https://link.springer.com/journal/11050",
        "search_page": "https://link.springer.com/search?query={query}&facet-journal-id=11050",
        "crawl_methods": ["crossref", "springer"],
        "publisher": "Springer",
        "crawl_config": {"springer_journal_id": "11050"},
    },
    "syntax": {
        "homepage": "https://www.journals.uchicago.edu/journals/syntax",
        "search_page": "https://www.journals.uchicago.edu/action/doSearch?AllField={query}&SeriesKey=syntax",
        "crawl_methods": ["crossref"],
        "publisher": "University of Chicago Press",
    },
    "phonology": {
        "homepage": "https://www.cambridge.org/core/journals/phonology",
        "search_page": "https://www.cambridge.org/core/search?q={query}&journalCode=PHO",
        "crawl_methods": ["crossref"],
        "publisher": "Cambridge",
    },
    "theoretical-linguistics": {
        "homepage": "https://www.degruyter.com/journal/key/thli/html",
        "search_page": "https://www.degruyter.com/search?query={query}&subjectFacet=THLI",
        "crawl_methods": ["crossref"],
        "publisher": "De Gruyter",
    },
    "linguistics-vanguard": {
        "homepage": "https://www.degruyter.com/journal/key/lingvan/html",
        "search_page": "https://www.degruyter.com/search?query={query}&subjectFacet=lingvan",
        "crawl_methods": ["crossref"],
        "publisher": "De Gruyter",
    },
    "linguistics-philosophy": {
        "homepage": "https://link.springer.com/journal/11051",
        "search_page": "https://link.springer.com/search?query={query}&facet-journal-id=11051",
        "crawl_methods": ["crossref", "springer"],
        "publisher": "Springer",
        "crawl_config": {"springer_journal_id": "11051"},
    },
    "language-sciences": {
        "homepage": "https://www.sciencedirect.com/journal/language-sciences",
        "search_page": "https://www.sciencedirect.com/search?qs={query}&pub=language-sciences",
        "crawl_methods": ["crossref"],
        "publisher": "Elsevier",
    },
    "functions-of-language": {
        "homepage": "https://benjamins.com/catalog/fol",
        "search_page": "https://benjamins.com/catalog?query={query}&f%5B0%5D=imprint%3A3",
        "crawl_methods": ["crossref"],
        "publisher": "John Benjamins",
    },
    "studies-in-language": {
        "homepage": "https://benjamins.com/catalog/sl",
        "search_page": "https://benjamins.com/catalog?query={query}&f%5B0%5D=imprint%3A3",
        "crawl_methods": ["crossref"],
        "publisher": "John Benjamins",
    },
    "linguistic-review": {
        "homepage": "https://www.degruyter.com/journal/key/tlir/html",
        "search_page": "https://www.degruyter.com/search?query={query}&subjectFacet=TLIR",
        "crawl_methods": ["crossref"],
        "publisher": "De Gruyter",
    },
    "language-and-linguistics": {
        "homepage": "https://www.degruyter.com/journal/key/lali/html",
        "search_page": "https://www.degruyter.com/search?query={query}&subjectFacet=LALI",
        "crawl_methods": ["crossref"],
        "publisher": "De Gruyter",
    },
    "languages-mdpi": {
        "homepage": "https://www.mdpi.com/journal/languages",
        "search_page": "https://www.mdpi.com/search?q={query}&journal=languages",
        "crawl_methods": ["crossref", "rss"],
        "publisher": "MDPI",
        "crawl_config": {"rss_url": "https://www.mdpi.com/rss/journal/languages"},
    },
    "journal-of-chinese-information-processing": {
        "homepage": "https://jcip.cipsc.org.cn",
        "search_page": "https://jcip.cipsc.org.cn/CN/article/showArticleByKeyword.do?keyword={query}",
        "crawl_methods": ["crossref", "jcip"],
        "publisher": "中国中文信息学会",
    },
}


def main() -> None:
    journals = json.loads(JOURNALS_PATH.read_text(encoding="utf-8"))
    for j in journals:
        meta = SITE_META.get(j["id"], {})
        j["homepage"] = meta.get("homepage", "")
        j["search_page"] = meta.get("search_page", "")
        j["crawl_methods"] = meta.get("crawl_methods", ["crossref"])
        j["publisher"] = meta.get("publisher", "")
        if "crawl_config" in meta:
            j["crawl_config"] = meta["crawl_config"]
        elif "crawl_config" in j:
            del j["crawl_config"]
    JOURNALS_PATH.write_text(json.dumps(journals, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Updated {len(journals)} journals")


if __name__ == "__main__":
    main()
