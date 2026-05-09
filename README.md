# AI Ecosystem Digest | AI 生态情报日报

每日定时抓取多源信号，经 AI 分类与摘要后，输出**一份中英对照、分板块排版**的 Markdown，并可选发布为 GitHub Issue。

---

## 当前主流程（推荐）

| 能力 | 说明 |
|------|------|
| 定时运行 | GitHub Actions：每天 **08:00 CST**（`cron: 0 0 * * *` UTC） |
| 手动触发 | 同一 Workflow 支持 `workflow_dispatch` |
| 产出位置 | `digests/YYYY-MM-DD/daily-digest.md`（**单文件**，内含 5 个板块） |
| Issue | `digests/latest_issue_body.md` 作为 Issue 正文索引，指向当日完整报告 |

**架构（模块化）**

- `scripts/run_portfolio_pipeline.py` — 编排入口  
- `scripts/pipeline/scraper.py` — 多源抓取（UA 轮换、超时、重试）  
- `scripts/pipeline/llm_processor.py` — 分类与双语摘要（主模型 → 备用模型 → **本地摘要**，读者侧不出现技术用语）  
- `scripts/pipeline/db.py` — SQLite：去重、任务状态  
- `scripts/pipeline/notifier.py` — 生成 Markdown 与 Issue 索引  
- `scripts/pipeline/models.py` — Pydantic 校验  

**配置**

- `config/sources.yaml` — 追踪的 GitHub 仓库等  

**Secrets（`Settings → Secrets and variables → Actions`）**

- `GH_PAT` — 建议配置，提升 GitHub API 限额（未配置时使用 `GITHUB_TOKEN`）  
- `OPENAI_API_KEY` — 主模型（可选）  
- `BACKUP_OPENAI_API_KEY` — 备用模型（可选）  
- 未配置 LLM 时，仍会用**基于标题与关键词的本地摘要**生成可读正文，流水线不中断  

**本地运行**

```bash
pip install -r requirements.txt
python scripts/run_portfolio_pipeline.py
# 指定日期（按 CST 日历日）
python scripts/run_portfolio_pipeline.py --date 2026-05-12
```

**数据文件**

- `data/portfolio_pipeline.db` — SQLite（处理记录与任务状态；勿将含密钥的日志提交入库）

---

## 日报结构（`daily-digest.md`）

单文件内 **5 个板块**（中英标题对照）：

1. **AI CLI** — 命令行工具相关仓库动态  
2. **AI Agents** — 智能体 / OpenClaw 赛道等  
3. **AI Web** — 官网与公开资讯类信号（由分类器归入）  
4. **AI Trending** — 趋势与主题类信号  
5. **AI HN** — Hacker News 社区热点  

排版以**要点列表 + 双语一句摘要 + 原文链接**为主；必要时辅以简短表格，避免整篇表格堆砌。

---

## 其他脚本（历史 / 扩展）

- `scripts/generate_digest.py` — 早期「多功能单脚本」版本（Trending、Sitemap、多段报告等），与当前 **portfolio 主流程并行存在**，便于对比或二次裁剪。  
- `scripts/generate_summary.py` — 周报 / 月报汇总（读取 `reports/daily`，若你仍保留旧目录可使用）。  
- `.github/workflows/weekly-ai-summary.yml`、`monthly-ai-summary.yml` — 周 / 月汇总（如目录结构有变需自行对齐）。

---

