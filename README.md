# AI Ecosystem Auto Briefing

这个项目用于自动生成并发布 AI 生态多维日报（GitHub Issues + Markdown）：

- 每天 08:00 CST 生成日报（GitHub Issues + Markdown）
- 支持手动触发与定时任务

## 覆盖内容

- 追踪仓库 24h Issues/PR/Releases
- Claude Code Skills 热度榜（按参与度）
- OpenClaw 深度报告 + 10 项目横向对比
- Anthropic/OpenAI Sitemap 增量检测
- GitHub Trending + 6 个 AI 标签趋势信号
- Hacker News 24h AI Top 30 + 情绪快照

## 文件结构

- `config/sources.yaml`: 跟踪仓库、主题、资讯源配置
- `scripts/generate_digest.py`: 每日简报生成脚本
- `scripts/run_portfolio_pipeline.py`: 面试作品集版主流程（模块化）
- `scripts/pipeline/scraper.py`: 多源抓取层（反爬 + 重试）
- `scripts/pipeline/llm_processor.py`: AI 过滤层（主备模型 + 关键词兜底）
- `scripts/pipeline/db.py`: SQLite 结构化存储（去重 + 任务状态）
- `scripts/pipeline/notifier.py`: 通知层（Markdown 与 Issue 索引）
- `scripts/pipeline/models.py`: pydantic 数据模型与校验
- `scripts/generate_summary.py`: 周报/月报汇总脚本（可选）
- `.github/workflows/*.yml`: GitHub Actions 工作流
- `digests/YYYY-MM-DD/`: 每日专题文件
  - `ai-cli.md`
  - `ai-agents.md`
  - `ai-web.md`
  - `ai-trending.md`
  - `ai-hn.md`

## GitHub Actions 定时

GitHub Actions 使用 UTC 时区，已转换为北京时间（CST, UTC+8）：

- 日报：`0 0 * * *` -> 每天 08:00 CST
- 周报：`10 0 * * 1` -> 每周一 08:10 CST
- 月报：`20 0 1 * *` -> 每月 1 日 08:20 CST

## 使用与配置

1. 按需编辑 `config/sources.yaml`（仓库、主题、新闻源）
2. 在仓库 `Settings -> Secrets and variables -> Actions` 中配置：
   - `GH_PAT`（可提高公开 API 限额；未配置时回退为 `GITHUB_TOKEN`）
   - `OPENAI_API_KEY`（主模型，可选）
   - `BACKUP_OPENAI_API_KEY`（备用模型，可选）
3. 若两个 LLM Key 都不可用，系统会自动启用规则兜底，不会中断。
3. 推送到 GitHub 后，工作流会按计划自动运行；也可手动 `Run workflow`

## 本地调试

```bash
pip install -r requirements.txt
python scripts/generate_digest.py
python scripts/generate_summary.py --mode weekly
python scripts/generate_summary.py --mode monthly
```
