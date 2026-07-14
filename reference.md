# 纯语言学期刊参考手册

本文件为 [SKILL.md](SKILL.md) 的补充参考，含 23 本期刊的选刊指南与已知局限。

## 选刊决策树

### 按子领域

| 子领域 | 首选期刊 | 次选期刊 |
|--------|----------|----------|
| syntax（句法） | Syntax, Linguistic Inquiry, NLLT | Language, Journal of Linguistics |
| semantics（语义） | Journal of Semantics, Natural Language Semantics | Linguistics & Philosophy, NLLT |
| phonology（音系） | Phonology | Language, Journal of Linguistics |
| corpus（语料库） | Corpus Linguistics & Linguistic Theory | Lingua, Glossa, 中文信息学报 |
| computational / NLP（计算语言学） | 中文信息学报 | Lingua, Languages |
| typology（类型学） | Studies in Language | Functions of Language, Lingua |
| philosophy（语言哲学） | Linguistics & Philosophy, Language Sciences | Journal of Semantics |
| review（综述） | Annual Review of Linguistics | — |
| general（综合） | Language, Journal of Linguistics | Glossa, Lingua |

### 按理论框架

| 框架 | 推荐期刊 |
|------|----------|
| generative（生成派） | NLLT, Linguistic Inquiry, The Linguistic Review | Language, Syntax |
| functional（功能派） | Functions of Language, Studies in Language | Theoretical Linguistics, Lingua |
| formal（形式主义） | Syntax, Journal of Semantics, Phonology | NLLT, Natural Language Semantics |
| 不限 | Language, Journal of Linguistics, Glossa | Lingua, Theoretical Linguistics |

### 特殊定位

| 需求 | 期刊 |
|------|------|
| 亚太理论语言学 | Language & Linguistics |
| 跨学科 / 偏应用 | Languages, Lingua, 中文信息学报 |
| 中文 NLP / 信息处理 | 中文信息学报 | Language & Linguistics, Lingua |
| 高发文量、覆盖面广 | Glossa |
| 顶刊、高影响力 | Language |

### 选刊数量建议

- 窄领域 idea（如纯音系）：3–5 本专刊 + 1–2 本综合刊
- 宽领域 idea（如语言与认知接口）：5–8 本，覆盖多个子领域
- 理论框架明确时：至少 2 本匹配该框架的刊

## 期刊完整列表

详见 [journals.json](journals.json)。23 本期刊按 priority 排序：

- **priority 1**：子领域顶刊 / 综合顶刊（Language, LI, NLLT, JoL, JoS, NLS, Syntax, Phonology）
- **priority 2**：重要但覆盖面较窄或周期较长的刊（含 *中文信息学报*）
- **priority 3**：哲学取向或跨学科取向的刊

## 已知局限

1. **API 滞后**：OpenAlex 对最新录用论文可能滞后 6–18 个月，慢刊（*Linguistics*、*Theoretical Linguistics*）尤其明显
2. **摘要缺失**：约 30–40% 论文在 OpenAlex 中无摘要，可启用 `enrich_abstracts.py` 补全
3. **Annual Review**：仅邀稿综述，检索到的是他人已写的 review，不宜评估 idea 原创性
4. **付费墙**：脚本仅获取元数据和摘要，无法验证全文论证细节
5. **期刊名歧义**：`Linguistics`（De Gruyter）已通过 ISSN `0024-3949` 消歧；`Languages`（MDPI）通过 ISSN `2226-471X` 消歧；`中文信息学报` 通过 ISSN `1003-0077` 标识
6. **中文信息学报**：OpenAlex 论文元数据以英文标题为主，中文摘要覆盖率较低；idea 检索建议同时使用中英文关键词

## 安装后配置

首次使用前，在 `scripts/` 目录下的脚本中将 `MAILTO` 替换为你的邮箱（进入 OpenAlex polite pool，提高速率限制）：

```python
MAILTO = "your-email@example.com"
```

然后运行一次性 ID 解析：

```bash
pip install -r scripts/requirements.txt
python scripts/resolve_journal_ids.py
```
