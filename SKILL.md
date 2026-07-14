---
name: linguistics-journal-research
description: >-
  Searches 23 linguistics and Chinese language science journals for research related to a user's idea,
  then synthesizes a structured literature summary in Chinese. Use when the user
  asks about a linguistics research idea, wants related papers from top
  linguistics journals, needs a literature review for syntax/semantics/phonology,
  mentions 语言学 research, 文献综述, idea 可行性, or explicitly invokes
  /linguistics-journal-research.
---

# Linguistics Journal Research

在 23 本语言学及相关期刊中检索与用户 idea 相关的论文，并输出结构化中文文献综述。

## 触发方式

- **自动**：用户描述语言学 research idea、询问文献综述、评估 idea 可行性时自动加载
- **显式**：用户输入 `/linguistics-journal-research` 或「帮我调研这个语言学 idea」

## 工作流

```
Task Progress:
- [ ] Step 1: 解析用户 idea
- [ ] Step 2: 选择期刊
- [ ] Step 3: 执行检索
- [ ] Step 4: 综合摘要
- [ ] Step 5: 研究空白与建议
```

### Step 1: 解析用户 idea

从用户输入提取：

1. **核心问题**（一句话）
2. **子领域**：syntax / semantics / phonology / corpus / typology / philosophy / general
3. **理论框架**（若提及）：generative / functional / formal / 不限
4. **英文检索词** 3–5 个（中文 idea 必须翻译为英文学术术语）

### Step 2: 选择期刊

读取 [reference.md](reference.md) 选刊决策树，从 [journals.json](journals.json) 选出 5–10 本最相关期刊，并简述选择理由。

优先级：子领域专刊 > 综合刊；理论框架匹配 > 不匹配；priority=1 优先。

### Step 3: 执行检索

Skill 根目录：`skills/linguistics-journal-research/`（相对于工作区或克隆的 GitHub 仓库根目录）。

```bash
pip install -r skills/linguistics-journal-research/scripts/requirements.txt
python skills/linguistics-journal-research/scripts/linguistics_search.py \
  "YOUR ENGLISH KEYWORDS" \
  --journals id1,id2,id3 \
  --max-per-journal 5 \
  --years 20 \
  -o /tmp/linguistics_results.json
```

Windows 用户建议加 `-o results.json` 避免终端编码问题，然后读取该 JSON 文件综合摘要。

**结果不足（< 3 篇）**：放宽 `--years 30`、减少 `--min-citations 0`、扩大期刊列表。

**摘要缺失较多**：管道补全（注意 Semantic Scholar 限速）：

```bash
python skills/linguistics-journal-research/scripts/linguistics_search.py \
  "query" --journals id1,id2 | \
  python skills/linguistics-journal-research/scripts/enrich_abstracts.py
```

**首次使用**：若 `journals.json` 中 `openalex_source_id` 为空，先运行：

```bash
python skills/linguistics-journal-research/scripts/resolve_journal_ids.py
```

### Step 4: 综合摘要

阅读脚本返回的 title + abstract，按下方模板输出。**不得编造**未在结果中出现的论文、作者或观点。

### Step 5: 研究空白与建议

指出已有共识、争议点、空白，以及对用户 idea 的可行性评估。

## 输出模板

```markdown
# [Idea 标题] 文献调研

## 检索概况
- **核心问题**：[...]
- **检索词**：[...]
- **检索期刊**（N 本）：[...]
- **命中论文**：N 篇（去重后）

## 研究现状摘要

### 主要发现
1. **[主题 A]**：[2–3 句，附引用 (Author, Year, Journal)]
2. **[主题 B]**：[...]

### 理论分歧（如有）
- [...]

### 高引核心文献
| 论文 | 期刊 | 年份 | 引用 | 与 idea 的关联 |
|------|------|------|------|----------------|
| ... | ... | ... | ... | ... |

## 与用户 idea 的关系
- **支持点**：[...]
- **潜在挑战**：[...]
- **差异化方向**：[...]

## 局限说明
- 本摘要基于 OpenAlex 元数据，未阅读全文
- [未覆盖的期刊/年份范围]
```

## 附加资源

- 期刊元数据与选刊指南：[reference.md](reference.md)
- 端到端示例：[examples.md](examples.md)
