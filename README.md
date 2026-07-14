# Linguistics Journal Research Skill

直接爬取 23 本语言学期刊**官网及出版商搜索页**，按发表时间倒序检索最新相关论文，生成结构化中文文献综述。

## 安装

```powershell
pip install -r scripts/requirements.txt
```

## 爬取哪些网站？

每本期刊的 `homepage` 和 `search_page` 配置在 [journals.json](journals.json)，完整列表见 [reference.md](reference.md)。

| 爬取方式 | 覆盖 |
|----------|------|
| CrossRef（出版商元数据，按 ISSN 最新排序） | 全部 23 本 |
| Springer Link 直爬 | NLLT、NLS、L&P |
| RSS 最新目录 | Glossa、Languages |
| 中文信息学报官网 | jcip.cipsc.org.cn |

## 使用

```powershell
python scripts/linguistics_search.py `
  "Mandarin tone sandhi" `
  --max-per-journal 3 `
  --years 8 `
  -o results.json
```

默认爬取全部 23 本期刊；仅当需要缩小范围时传 `--journals id1,id2`。

## 与旧版（OpenAlex）的区别

| | 旧版 | 新版 |
|---|---|---|
| 数据源 | OpenAlex 第三方索引 | 期刊官网 + 出版商搜索页 |
| 时效性 | 可能滞后 6–18 个月 | 按 `published` 倒序，优先最新 |
| 透明度 | 不透明 | `crawl_log` 记录爬了哪些网站 |

## 部署

```powershell
# 克隆
git clone https://github.com/shen-xun/findlin_skill.git

# 复制到 Cursor skills 目录
Copy-Item -Recurse findlin_skill "$env:USERPROFILE\.agents\skills\linguistics-journal-research"
```
