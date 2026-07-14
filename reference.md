# 期刊官网爬取参考

本 skill **不再使用 OpenAlex**，改为直接访问各期刊官网及其出版商搜索页，按**发表时间倒序**检索最新研究。

## 爬取策略

| 方法 | 说明 | 适用期刊 |
|------|------|----------|
| `crossref` | 通过 CrossRef 获取出版商提交的元数据，按 ISSN + 发表日期排序 | **全部 23 本**（默认） |
| `springer` | 直接爬取 Springer Link 搜索页 | NLLT、Natural Language Semantics、Linguistics & Philosophy |
| `rss` | 抓取期刊 RSS 最新目录，按关键词过滤 | Glossa、Languages (MDPI) |
| `jcip` | 直接爬取《中文信息学报》官网检索与当期目录 | 中文信息学报 |

默认 `--years 10`，优先返回近十年内**最新发表**的论文。

## 选刊决策树

### 按子领域

| 子领域 | 首选期刊 | 次选期刊 |
|--------|----------|----------|
| syntax（句法） | Syntax, Linguistic Inquiry, NLLT | Language, Journal of Linguistics |
| semantics（语义） | Journal of Semantics, Natural Language Semantics | Linguistics & Philosophy, NLLT |
| phonology（音系） | Phonology | Language, Journal of Linguistics |
| corpus（语料库） | Corpus Linguistics & Linguistic Theory | Lingua, Glossa, 中文信息学报 |
| computational / NLP | 中文信息学报 | Lingua, Languages |
| typology（类型学） | Studies in Language | Functions of Language, Lingua |
| philosophy（语言哲学） | Linguistics & Philosophy, Language Sciences | Journal of Semantics |
| review（综述） | Annual Review of Linguistics | — |
| general（综合） | Language, Journal of Linguistics | Glossa, Lingua |

### 特殊定位

| 需求 | 期刊 |
|------|------|
| 亚太理论语言学 | Language & Linguistics |
| 跨学科 / 偏应用 | Languages, Lingua, 中文信息学报 |
| 中文 NLP / 信息处理 | 中文信息学报 |
| 最新发文（OA） | Glossa, Languages |

## 23 本期刊官网一览

| 期刊 | 官网 | 出版商 |
|------|------|--------|
| Annual Review of Linguistics | https://www.annualreviews.org/journal/linguistics | Annual Reviews |
| Language | https://www.linguisticsociety.org/language | LSA |
| Linguistic Inquiry | https://direct.mit.edu/ling | MIT Press |
| Corpus Linguistics & Linguistic Theory | https://www.degruyter.com/journal/key/cllt/html | De Gruyter |
| Natural Language & Linguistic Theory | https://link.springer.com/journal/11049 | Springer |
| Journal of Linguistics | https://www.cambridge.org/core/journals/journal-of-linguistics | Cambridge |
| Linguistics | https://www.degruyter.com/journal/key/ling/html | De Gruyter |
| Lingua | https://www.sciencedirect.com/journal/lingua | Elsevier |
| Glossa | https://www.glossa-journal.org | OLH |
| Journal of Semantics | https://academic.oup.com/jos | OUP |
| Natural Language Semantics | https://link.springer.com/journal/11050 | Springer |
| Syntax | https://www.journals.uchicago.edu/journals/syntax | Chicago |
| Phonology | https://www.cambridge.org/core/journals/phonology | Cambridge |
| Theoretical Linguistics | https://www.degruyter.com/journal/key/thli/html | De Gruyter |
| Linguistics Vanguard | https://www.degruyter.com/journal/key/lingvan/html | De Gruyter |
| Linguistics & Philosophy | https://link.springer.com/journal/11051 | Springer |
| Language Sciences | https://www.sciencedirect.com/journal/language-sciences | Elsevier |
| Functions of Language | https://benjamins.com/catalog/fol | Benjamins |
| Studies in Language | https://benjamins.com/catalog/sl | Benjamins |
| The Linguistic Review | https://www.degruyter.com/journal/key/tlir/html | De Gruyter |
| Language & Linguistics | https://www.degruyter.com/journal/key/lali/html | De Gruyter |
| Languages | https://www.mdpi.com/journal/languages | MDPI |
| 中文信息学报 | https://jcip.cipsc.org.cn | 中国中文信息学会 |

完整爬取配置见 [journals.json](journals.json) 中的 `homepage`、`search_page`、`crawl_methods`。

## 已知局限

1. **付费墙**：多数出版商网站只返回标题/摘要，无法获取全文
2. **反爬限制**：Elsevier、OUP、MIT Press 等站点可能拦截自动化请求，此时回退到 CrossRef 元数据
3. **中文信息学报**：官网爬取受网络环境影响，失败时仍可通过 CrossRef ISSN 检索
4. **RSS 过滤**：RSS 仅提供最新目录，需关键词匹配，可能漏掉相关但标题不明显的论文
5. **礼貌爬取**：脚本内置请求间隔（~0.4s），请勿并发大量请求
