# AI Ecosystem Auto Briefing

这个项目用于自动生成并发布中英双语 AI 生态简报：

- 每天 08:00 CST 生成日报（GitHub Issues + Markdown）
- 每周自动生成周报（GitHub Issues + Markdown）
- 每月自动生成月报（GitHub Issues + Markdown）

## 覆盖内容

- 主流 AI CLI 工具的 GitHub 动态
- OpenClaw 及其同赛道项目生态活动
- Anthropic 与 OpenAI 官网资讯（RSS 优先）
- GitHub AI 热门仓库每日趋势

## 文件结构

- `config/sources.yaml`: 跟踪仓库、主题、资讯源配置
- `scripts/generate_digest.py`: 每日简报生成脚本
- `scripts/generate_summary.py`: 周报/月报汇总脚本
- `.github/workflows/*.yml`: GitHub Actions 工作流
- `reports/daily`: 每日简报
- `reports/weekly`: 每周汇总
- `reports/monthly`: 每月汇总

## GitHub Actions 定时

GitHub Actions 使用 UTC 时区，已转换为北京时间（CST, UTC+8）：

- 日报：`0 0 * * *` -> 每天 08:00 CST
- 周报：`10 0 * * 1` -> 每周一 08:10 CST
- 月报：`20 0 1 * *` -> 每月 1 日 08:20 CST

## 使用与配置

1. 按需编辑 `config/sources.yaml`（仓库、主题、新闻源）
2. 在仓库 `Settings -> Secrets and variables -> Actions` 中可选配置：
   - `GH_PAT`（可提高公开 API 限额；未配置时回退为 `GITHUB_TOKEN`）
3. 推送到 GitHub 后，工作流会按计划自动运行；也可手动 `Run workflow`

## 本地调试

```bash
pip install -r requirements.txt
python scripts/generate_digest.py
python scripts/generate_summary.py --mode weekly
python scripts/generate_summary.py --mode monthly
```
