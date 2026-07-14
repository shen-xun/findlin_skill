# Linguistics Journal Research Skill

在 23 本语言学及相关期刊中自动检索与用户 research idea 相关的论文，并生成结构化中文文献综述。

## 安装

```bash
pip install -r scripts/requirements.txt
python scripts/resolve_journal_ids.py   # 首次使用：解析 OpenAlex 期刊 ID
```

建议将 `scripts/` 中的 `MAILTO` 替换为你的真实邮箱（OpenAlex polite pool）。

## 在 Cursor 中使用

### 方式一：自动触发

在对话中描述语言学 research idea，Agent 会自动加载本 skill。例如：

> 我想研究汉语话题化结构的左缘语层，有相关文献吗？

### 方式二：显式调用

> /linguistics-journal-research 空主语参数的跨语言对比

或：

> 用 linguistics-journal-research skill 帮我调研这个 idea：……

## 手动检索

```bash
python scripts/linguistics_search.py \
  "pro-drop parameter" \
  --journals nllt,language,syntax \
  --max-per-journal 5
```

## 文件结构

```
linguistics-journal-research/
├── SKILL.md              # Agent 主工作流
├── reference.md          # 选刊决策树
├── journals.json         # 23 本期刊注册表
├── examples.md           # 使用示例
└── scripts/
    ├── linguistics_search.py
    ├── resolve_journal_ids.py
    ├── enrich_abstracts.py
    └── requirements.txt
```

## 期刊覆盖

23 本语言学及相关期刊，涵盖句法、语义、音系、语料库、类型学、语言哲学、中文信息处理等子领域。详见 [reference.md](reference.md)。

## 局限

- 基于 OpenAlex 元数据，不阅读全文
- 最新录用论文可能有 6–18 个月滞后
- 约 30–40% 论文摘要缺失（可用 `enrich_abstracts.py` 部分补全）

## 部署到 Cursor

克隆本仓库后，将 `linguistics-journal-research/` 目录：

- 复制到 `~/.cursor/skills/`（个人全局），或
- 保留在项目中，并在 Cursor Rules 中注明 skill 路径
