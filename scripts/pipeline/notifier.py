from __future__ import annotations

import datetime as dt
from collections import defaultdict
from pathlib import Path
from typing import Iterable

from .models import ProcessedItem


class Notifier:
    """
    Output markdown files and issue body.
    输出 Markdown 及 Issue 正文，作为通知层（可对接 GitHub API）。
    """

    def __init__(self, digest_root: Path) -> None:
        self.digest_root = digest_root

    def write_daily_files(self, run_date: dt.date, items: Iterable[ProcessedItem]) -> dict:
        day_dir = self.digest_root / run_date.isoformat()
        day_dir.mkdir(parents=True, exist_ok=True)
        grouped = defaultdict(list)
        for it in items:
            if it.insight.category in {"ai_cli", "ai_agents", "ai_web", "ai_trending", "ai_hn"}:
                grouped[it.insight.category].append(it)
            else:
                # Uncategorized items go to Trending so five sections stay populated.
                # 未分类条目归入「趋势」板块，保证五大板块结构稳定。
                grouped["ai_trending"].append(it)

        # Single beautiful digest file with 5 sections.
        # 单文件日报（五大板块），便于展示和面试讲解。
        digest_path = day_dir / "daily-digest.md"
        digest_content = self._render_single_digest(run_date, grouped)
        digest_path.write_text(digest_content, encoding="utf-8")

        issue = self._render_issue_index(run_date, digest_path)
        issue_path = self.digest_root / "latest_issue_body.md"
        issue_path.write_text(issue, encoding="utf-8")
        return {"dir": day_dir, "issue_body": issue_path, "digest_file": digest_path}

    def _render_single_digest(self, run_date: dt.date, grouped: dict) -> str:
        total = sum(len(v) for v in grouped.values())
        lines = [
            f"# AI Ecosystem Daily Digest | AI 生态每日报告 · {run_date.isoformat()}",
            "",
            "**English** — Daily curated signals across CLI tools, agents, the open web, trending repos, and Hacker News. "
            "Each item includes a one-line bilingual takeaway and a primary link.",
            "",
            "**中文** — 每日汇总 CLI 工具、智能体生态、公开网络信号、仓库趋势与 Hacker News 热点；每条含中英一句要点与原文链接。",
            "",
            f"**Today | 今日** — {total} item(s) in this run.",
            "",
            "## 0) At a glance | 今日速览",
            "",
            self._glance_lines(grouped),
            "",
        ]

        lines.extend(self._render_section("1) AI CLI", "AI CLI 工具动态", grouped.get("ai_cli", []), "release/pr/issue updates"))
        lines.extend(self._render_section("2) AI Agents", "智能体与 OpenClaw 赛道", grouped.get("ai_agents", []), "ecosystem collaboration and skills"))
        lines.extend(self._render_section("3) AI Web", "官网资讯与研究更新", grouped.get("ai_web", []), "official websites and research"))
        lines.extend(self._render_section("4) AI Trending", "趋势信号与主题标签", grouped.get("ai_trending", []), "GitHub trending and topics"))
        lines.extend(self._render_section("5) AI HN", "Hacker News 社区脉搏", grouped.get("ai_hn", []), "community hot discussions"))
        lines.append("")
        lines.append("---")
        lines.append("*— End of digest | 报告结束 —*")
        return "\n".join(lines) + "\n"

    def _glance_lines(self, grouped: dict) -> str:
        parts = []
        labels = [
            ("ai_cli", "CLI", "命令行工具"),
            ("ai_agents", "Agents", "智能体"),
            ("ai_web", "Web", "官网与资讯"),
            ("ai_trending", "Trending", "趋势"),
            ("ai_hn", "HN", "社区"),
        ]
        for key, en, zh in labels:
            n = len(grouped.get(key, []))
            parts.append(f"- **{en} / {zh}**: {n}")
        return "\n".join(parts)

    def _render_section(self, en_title: str, zh_title: str, items: list[ProcessedItem], note: str) -> list[str]:
        lines = [
            f"## {en_title} | {zh_title}",
            "",
            f"*EN — {note}.*",
            f"*中文 — {self._zh_note(note)}。*",
            "",
        ]

        if not items:
            lines.extend(["*No items in this section today. | 本板块今日无条目。*", ""])
            return lines

        lines.append("### Highlights | 重点速览")
        for idx, it in enumerate(items[:5], start=1):
            mood_en = {"positive": "Positive tone", "neutral": "Neutral", "negative": "Critical / cautious"}.get(
                it.insight.sentiment, it.insight.sentiment
            )
            mood_zh = {"positive": "偏积极", "neutral": "中性", "negative": "偏谨慎 / 批评"}.get(
                it.insight.sentiment, it.insight.sentiment
            )
            lines.append(
                f"{idx}. **{it.raw.title.strip()[:100]}**  \n"
                f"   - **EN:** {it.insight.summary_en.strip()[:200]}  \n"
                f"   - **中文：** {it.insight.summary_zh.strip()[:200]}  \n"
                f"   - **Link | 原文：** [{it.raw.url}]({it.raw.url})  \n"
                f"   - **Tone | 语气:** {mood_en} / {mood_zh}"
            )
            lines.append("")

        if len(items) > 5:
            lines.append("### More | 更多条目")
            for it in items[5:12]:
                lines.append(
                    f"- [{it.raw.title.strip()[:70]}]({it.raw.url}) — *{it.insight.summary_zh.strip()[:80]}* / "
                    f"*{it.insight.summary_en.strip()[:80]}*"
                )
            lines.append("")
        return lines

    def _zh_note(self, note: str) -> str:
        mapping = {
            "release/pr/issue updates": "围绕发布、PR 和 Issue 的活跃变化",
            "ecosystem collaboration and skills": "关注生态协作、项目演进与 Skills 热度",
            "official websites and research": "聚合官网公告、研究和产品页面更新",
            "GitHub trending and topics": "结合 Trending 与主题标签提炼信号",
            "community hot discussions": "提取社区高热讨论并观察情绪",
        }
        return mapping.get(note, "关键更新摘要")

    def _render_issue_index(self, run_date: dt.date, digest_path: Path) -> str:
        day = run_date.isoformat()
        rel_path = f"digests/{day}/daily-digest.md"
        lines = [
            f"# Daily digest published | 日报已生成 · {day}",
            "",
            "**English** — Full bilingual report for this date is in the repository at the path below.",
            "",
            "**中文** — 当日完整中英对照报告已写入仓库，路径如下。",
            "",
            f"- **File | 文件:** `{rel_path}`",
            f"- **Open | 打开:** [daily-digest.md](./{rel_path})",
            "",
            "**Sections | 板块:** CLI · Agents · Web · Trending · Hacker News",
        ]
        return "\n".join(lines) + "\n"
