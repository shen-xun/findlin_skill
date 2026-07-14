# 使用示例

## 示例 A：句法 idea（自动触发）

**用户输入：**
> 我有一个 idea：汉语把字句在生成派框架下怎么分析？帮我看看有没有相关研究。

**Agent 解析：**
- 子领域：syntax
- 框架：generative
- 英文检索词：`Mandarin ba construction syntactic analysis`

**命令（默认爬全部 23 本）：**
```powershell
python "$env:USERPROFILE\.agents\skills\linguistics-journal-research\scripts\linguistics_search.py" `
  "Mandarin ba construction syntactic analysis" `
  --max-per-journal 3 --years 8 -o results.json
```

综合摘要时优先深入：LI, NLLT, Syntax, Language（见 reference.md），但 `crawl_log` 应显示全部 23 本。

---

## 示例 B：语义 idea（显式触发）

**用户输入：**
> /linguistics-journal-research already vs still 的语义对比

**检索词：** `already still scalar particles semantics`

**命令：** 同上，不传 `--journals`。

---

## 示例 C：功能主义类型学（中文 idea）

**用户输入：**
> 作格配列和信息结构之间有什么互动？

**检索词：** `ergativity information structure interaction`

**命令：** 爬全部 23 本；综述时重点看 Studies in Language, Functions of Language。

---

## 示例 D：结果过少时的放宽策略

若全部 23 本检索后仍不足：

1. `--years 30`（扩大时间窗口）
2. 换用更宽泛检索词
3. 启用 `enrich_abstracts.py` 补全摘要
