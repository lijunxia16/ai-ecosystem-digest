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
                # Keep output fixed to 5 files for portfolio requirement.
                # 为满足作品集要求，未知类别统一归入 ai_trending，保证输出文件恒定。
                grouped["ai_trending"].append(it)

        mapping = {
            "ai_cli": "ai-cli.md",
            "ai_agents": "ai-agents.md",
            "ai_web": "ai-web.md",
            "ai_trending": "ai-trending.md",
            "ai_hn": "ai-hn.md",
        }
        out = {}
        for category, filename in mapping.items():
            content = self._render_category(run_date, category, grouped.get(category, []))
            path = day_dir / filename
            path.write_text(content, encoding="utf-8")
            out[category] = path

        issue = self._render_issue_index(run_date, out)
        issue_path = self.digest_root / "latest_issue_body.md"
        issue_path.write_text(issue, encoding="utf-8")
        return {"dir": day_dir, "issue_body": issue_path}

    def _render_category(self, run_date: dt.date, category: str, items: list[ProcessedItem]) -> str:
        lines = [
            f"# {category} ({run_date.isoformat()})",
            "",
            "Brief intro: curated updates with bilingual AI summaries and source links.",
            "",
        ]
        if not items:
            lines.append("- No items today.")
            return "\n".join(lines) + "\n"
        lines.extend(["| Title | Summary(ZH) | Summary(EN) | Sentiment | Source |", "|---|---|---|---|---|"])
        for it in items:
            lines.append(
                f"| {it.raw.title[:80]} | {it.insight.summary_zh[:120]} | {it.insight.summary_en[:120]} | "
                f"{it.insight.sentiment} | [link]({it.raw.url}) |"
            )
        return "\n".join(lines) + "\n"

    def _render_issue_index(self, run_date: dt.date, paths: dict) -> str:
        day = run_date.isoformat()
        lines = [
            f"# AI Daily Digest Bundle ({day})",
            "",
            "Generated files:",
            "",
            f"- `digests/{day}/ai-cli.md`",
            f"- `digests/{day}/ai-agents.md`",
            f"- `digests/{day}/ai-web.md`",
            f"- `digests/{day}/ai-trending.md`",
            f"- `digests/{day}/ai-hn.md`",
        ]
        return "\n".join(lines) + "\n"
