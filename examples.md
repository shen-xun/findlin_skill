# 使用示例

## 示例 A：句法 idea（自动触发）

**用户输入：**
> 我有一个 idea：汉语把字句在生成派框架下怎么分析？帮我看看有没有相关研究。

**Agent 解析：**
- 子领域：syntax
- 框架：generative
- 英文检索词：`Mandarin ba construction syntactic analysis`

**选刊：**
`linguistic-inquiry`, `nllt`, `syntax`, `language`, `journal-of-linguistics`

**命令：**
```bash
python skills/linguistics-journal-research/scripts/linguistics_search.py \
  "Mandarin ba construction syntactic analysis" \
  --journals linguistic-inquiry,nllt,syntax,language,journal-of-linguistics \
  --max-per-journal 5 --years 25
```

---

## 示例 B：语义 idea（显式触发）

**用户输入：**
> /linguistics-journal-research already vs still 的语义对比

**Agent 解析：**
- 子领域：semantics
- 英文检索词：`already still scalar particles semantics`

**选刊：**
`journal-of-semantics`, `natural-language-semantics`, `linguistics-philosophy`, `nllt`

---

## 示例 C：功能主义类型学（中文 idea）

**用户输入：**
> 作格配列和信息结构之间有什么互动？想做功能主义角度的研究。

**Agent 解析：**
- 子领域：typology
- 框架：functional
- 英文检索词：`ergativity information structure interaction`

**选刊：**
`studies-in-language`, `functions-of-language`, `lingua`, `language`

**注意：** 不选 `syntax` 或 `nllt`（生成派专刊，与功能主义框架不匹配）。

---

## 示例 D：结果过少时的放宽策略

若首次检索仅返回 1 篇：

1. `--years 30`（扩大时间窗口）
2. 追加综合刊：`glossa`, `lingua`, `linguistics-de-gruyter`
3. 换用更宽泛的检索词（如 `ba construction` 替代 `Mandarin ba construction left periphery`）
4. 启用 `enrich_abstracts.py` 补全摘要后再综合
