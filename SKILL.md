---
name: linguistics-journal-research
description: >-
  Crawls 23 linguistics journal official websites and publisher search pages for
  the latest research related to a user's idea, then synthesizes a structured
  literature summary in Chinese. Use when the user asks about a linguistics
  research idea, wants related papers from top linguistics journals, needs a
  literature review, mentions 语言学 research, 文献综述, idea 可行性, or invokes
  /linguistics-journal-research.
---

# Linguistics Journal Research

直接爬取 23 本期刊官网及出版商搜索页，按发表时间倒序检索**最新**相关论文，并输出结构化中文文献综述。

## 触发方式

- **自动**：用户描述语言学 research idea、询问文献综述时自动加载
- **显式**：`/linguistics-journal-research` 或「帮我调研这个语言学 idea」

## 工作流

```
- [ ] Step 1: 解析用户 idea
- [ ] Step 2: 选择期刊（参考 reference.md）
- [ ] Step 3: 爬取官网检索最新论文
- [ ] Step 4: 综合摘要
- [ ] Step 5: 研究空白与建议
```

### Step 1: 解析用户 idea

提取：核心问题、子领域、理论框架、检索词 3–5 个（中英文均可）。

### Step 2: 选择期刊

从 [journals.json](journals.json) 选 5–10 本，说明理由。每本期刊的官网见 [reference.md](reference.md)。

### Step 3: 爬取官网检索

Skill 目录：`~/.agents/skills/linguistics-journal-research/`

```powershell
pip install -r "$env:USERPROFILE\.agents\skills\linguistics-journal-research\scripts\requirements.txt"

python "$env:USERPROFILE\.agents\skills\linguistics-journal-research\scripts\linguistics_search.py" `
  "dialect tone change" `
  --journals language,phonology,journal-of-chinese-information-processing `
  --max-per-journal 5 `
  --years 8 `
  -o results.json
```

**爬取逻辑**（按期刊 `crawl_methods` 配置）：
- 所有期刊：`crossref`（出版商元数据，按 ISSN + 发表日期倒序）
- Springer 刊：`springer` 官网搜索页直爬
- Glossa / Languages：`rss` 最新目录
- 中文信息学报：`jcip` 官网关键词检索

输出 JSON 含 `crawl_log`（记录了爬了哪些网站、命中多少）和 `papers`（含 `source`、`url`、`published`）。

**结果不足**：扩大 `--years`、增加期刊、换更宽泛检索词。

**摘要缺失**：`enrich_abstracts.py` 通过 DOI 从 Semantic Scholar 补全。

### Step 4–5

阅读 `papers` 中的 title + abstract，按模板输出综述。**不得编造**。

## 输出模板

```markdown
# [Idea 标题] 文献调研

## 检索概况
- **核心问题**：[...]
- **检索词**：[...]
- **爬取网站**：[列出 homepage + 命中数，来自 crawl_log]
- **命中论文**：N 篇

## 研究现状摘要
### 主要发现
1. **[主题]**：(Author, Year, Journal) ...

## 与用户 idea 的关系
- **支持点** / **潜在挑战** / **差异化方向**

## 局限说明
- 基于官网元数据/摘要，未阅读全文
```

## 附加资源

- [reference.md](reference.md) — 23 本期刊官网与爬取策略
- [examples.md](examples.md) — 使用示例
