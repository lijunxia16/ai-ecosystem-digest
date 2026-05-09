"""
Renders the five portfolio Markdown files (ai-cli / ai-agents / ai-web / ai-trending / ai-hn).
生成五份专题 Markdown，结构与面试展示用大纲一致。
"""

from __future__ import annotations

import datetime as dt
from pathlib import Path
from typing import Any, Dict, List

from .scraper_extended import classify_anthropic_url, classify_openai_url, categorize_hn_post

UTC = dt.timezone.utc


def _link(title: str, url: str) -> str:
    return f"[{title}]({url})"


def _issue_line(it: Dict[str, Any]) -> str:
    return f"- {_link(it.get('title', '')[:100], it.get('html_url', '#'))}"


def _pr_line(pr: Dict[str, Any]) -> str:
    return f"- #{pr.get('number')} {_link(pr.get('title', '')[:90], pr.get('html_url', '#'))}"


def _rel_line(r: Dict[str, Any]) -> str:
    return f"- **{r.get('name', '')}** — {_link('Release', r.get('html_url', '#'))}"


def _meta_table_row(name: str, bundle: Dict[str, Any]) -> str:
    m = bundle.get("meta") or {}
    if not m:
        return f"| {name} | — | — | — | — |"
    return (
        f"| {name} | {m.get('stargazers_count', 0):,} | {m.get('forks_count', 0):,} | "
        f"{m.get('open_issues_count', 0):,} | {m.get('updated_at', '—')[:10]} |"
    )


def render_ai_cli_md(run_date: dt.date, ctx: Dict[str, Any]) -> str:
    tools: List[Dict[str, Any]] = ctx.get("cli_tools_bundles", [])
    skills: List[Dict[str, Any]] = ctx.get("claude_skills", [])

    lines: List[str] = [
        f"# AI CLI Landscape | AI 命令行工具全景 · {run_date.isoformat()}",
        "",
        "*Data: GitHub API (24h activity) + GitHub Search (Claude-related skills).*",
        "*数据：GitHub API（近 24h 动态）+ GitHub Search（Claude 生态 Skills）。*",
        "",
        "## 横向对比 | Cross-tool comparison",
        "",
        "### 生态全景 | Ecosystem overview",
        "- **EN:** Compare terminal-native AI assistants by activity, community signals, and release cadence.",
        "- **中文：** 从活跃度、社区信号与发布节奏对比终端侧 AI 助手生态。",
        "",
        "### 活跃度对比表 | Activity snapshot",
        "",
        "| Tool | Stars | Forks | Open issues | Last update |",
        "|------|------:|------:|-------------:|:-------------|",
    ]
    for b in tools:
        lines.append(_meta_table_row(b.get("display_name", b.get("repo", "?")), b))
    lines.extend(
        [
            "",
            "### 共同需求 | Shared needs",
            "- **EN:** Reliable auth, plugin/MCP ecosystem, low-latency UX, reproducible workflows.",
            "- **中文：** 稳定鉴权、插件或 MCP 生态、低延迟体验、可复现工作流。",
            "",
            "### 差异定位 | Differentiation",
            "- **EN:** Vendor-backed CLIs vs community-first harnesses; different model defaults and skill marketplaces.",
        ]
    )
    lines.extend(
        [
            "- **中文：** 厂商背书 CLI 与社区驱动 harness 并存；默认模型与 Skills 市场形态各异。",
            "",
            "### 趋势信号 | Trend signals",
            "- **EN:** Watch for cross-tool skill portability, local-first runners, and governance around agent permissions.",
            "- **中文：** 关注 Skills 跨工具迁移、本地优先运行时、以及对 Agent 权限的治理演进。",
            "",
            "## 各工具详细报告 | Per-tool deep dives",
            "",
        ]
    )

    for b in tools:
        name = b.get("display_name", "Tool")
        repo = b.get("repo") or ""
        lines.append(f"<details>")
        lines.append(f"<summary><strong>{name}</strong>")
        if repo:
            lines.append(f" — <code>{repo}</code>")
        if name.strip().lower() == "claude code":
            lines.append(" — *Claude Code Skills 社区热点 | Claude Code Skills community heat*")
        lines.append("</summary>")
        lines.append("")
        if not repo:
            lines.extend(
                [
                    "*未配置 GitHub 仓库。请在 `config/sources.yaml` → `cli_tools` 中为该工具填写 `repo`。*",
                    "*No GitHub repo configured. Set `repo` under `cli_tools` in `config/sources.yaml`.*",
                    "",
                ]
            )
            lines.append("</details>")
            lines.append("")
            continue

        if name.strip().lower() == "claude code":
            lines.extend(
                [
                    "#### 热门 Skills 排行 | Top skills (by engagement)",
                    "",
                ]
            )
            if skills:
                for i, sk in enumerate(skills[:10], 1):
                    eng = sk.get("_engagement", 0)
                    lines.append(
                        f"{i}. {_link(sk.get('full_name', ''), sk.get('html_url', '#'))} "
                        f"— ⭐ {sk.get('stargazers_count', 0):,} · engagement **{eng}**"
                    )
            else:
                lines.append("*暂无搜索结果（检查 Token 限额或搜索词）。* / *No search results.*")
            lines.extend(
                [
                    "",
                    "#### 社区需求趋势 | Community demand",
                    "- **EN:** High engagement repos often bundle prompts, eval harnesses, and security guardrails.",
                    "- **中文：** 高参与度仓库常捆绑提示词、评测与安全护栏，反映「可落地」诉求。",
                    "",
                    "#### 高潜力待合并 Skills | Promising skills to watch",
                    "- **EN:** Watch newly starred repos with fast issue velocity; good candidates to upstream or fork.",
                    "- **中文：** 关注星标增长快、Issue 活跃的新仓库，适合评估是否合并或二次开发。",
                    "",
                    "---",
                    "",
                ]
            )

        lines.extend(["#### 今日速览 | Today", ""])
        issues, prs, rels = b.get("issues", []), b.get("prs", []), b.get("releases", [])
        lines.append(f"- Issues (24h window): **{len(issues)}** | PRs: **{len(prs)}** | Releases: **{len(rels)}**")
        lines.append("")
        lines.append("##### 热点 Issues | Hot issues")
        lines.extend([_issue_line(x) for x in issues[:8]] or ["*None in window.*"])
        lines.append("")
        lines.append("##### PR 进展 | Pull requests")
        lines.extend([_pr_line(x) for x in prs[:8]] or ["*None in window.*"])
        lines.append("")
        lines.append("##### 版本与发布 | Releases")
        lines.extend([_rel_line(x) for x in rels[:6]] or ["*None in window.*"])
        lines.append("")
        lines.append("##### 趋势 | Trend")
        lines.append(
            "- **EN:** Combine release notes + merged PR themes to infer product direction for the next week."
        )
        lines.append("- **中文：** 结合 Release 说明与已合并 PR 主题，推断未来一周产品方向。")
        lines.append("")
        lines.append("</details>")
        lines.append("")

    return "\n".join(lines) + "\n"


def render_ai_agents_md(run_date: dt.date, ctx: Dict[str, Any]) -> str:
    oc = ctx.get("openclaw_bundle", {})
    peers: List[Dict[str, Any]] = ctx.get("peer_bundles", [])
    ni, np, nc = ctx.get("agents_issue_total", 0), ctx.get("agents_pr_total", 0), ctx.get("agents_project_count", 0)

    lines = [
        f"# AI Agents & OpenClaw | 智能体与 OpenClaw · {run_date.isoformat()}",
        "",
        f"**Issues:** {ni} &nbsp;|&nbsp; **PRs:** {np} &nbsp;|&nbsp; **覆盖项目 | Projects covered:** {nc}",
        "",
        "## OpenClaw 项目深度报告 | OpenClaw deep report",
        "",
    ]
    lines.extend(_openclaw_sections(oc, is_primary=True))
    lines.extend(
        [
            "## 横向生态对比 | Ecosystem comparison",
            "",
            "### 生态全景 | Landscape",
            "- **EN:** Agent harnesses span coding agents, browser automation, and multi-agent orchestration.",
            "- **中文：** 智能体 harness 覆盖编程代理、浏览器自动化与多智能体编排。",
            "",
            "### 活跃度对比表 | Activity table",
            "",
            "| Project | Stars | Forks | Issues(24h) | PRs(24h) | Releases |",
            "|---------|------:|------:|-------------:|---------:|---------|",
        ]
    )
    rows = []
    if oc.get("repo"):
        m = oc.get("meta") or {}
        rows.append(
            f"| OpenClaw | {m.get('stargazers_count', 0):,} | {m.get('forks_count', 0):,} | "
            f"{len(oc.get('issues', []))} | {len(oc.get('prs', []))} | {len(oc.get('releases', []))} |"
        )
    for p in peers:
        m = p.get("meta") or {}
        label = p.get("display_name", p.get("repo", "?"))
        rows.append(
            f"| {label} | {m.get('stargazers_count', 0):,} | {m.get('forks_count', 0):,} | "
            f"{len(p.get('issues', []))} | {len(p.get('prs', []))} | {len(p.get('releases', []))} |"
        )
    lines.extend(rows or ["| — | — | — | — | — | — |"])
    lines.extend(
        [
            "",
            "### OpenClaw 定位分析 | Positioning",
            "- **EN:** Position against peers by integration breadth (channels), plugin model, and operational maturity.",
            "- **中文：** 从接入广度（渠道）、插件模型与运维成熟度对比 OpenClaw 定位。",
            "",
            "### 共同技术方向 | Shared technical directions",
            "- **EN:** Tool calling, durable sessions, sandboxing, observability, and cost controls.",
            "- **中文：** 工具调用、持久会话、沙箱、可观测性与成本控制。",
            "",
            "### 差异化定位 | Differentiation",
            "- **EN:** Some projects optimize for IDE embedding; others for headless automation or multi-tenant SaaS.",
            "- **中文：** 有的偏 IDE 嵌入，有的偏无头自动化或多租户 SaaS。",
            "",
            "### 社区热度与成熟度 | Heat & maturity",
            "- **EN:** Use stars/forks as weak proxies; prioritize issue/PR recency for momentum.",
            "- **中文：** Star/Fork 仅作弱信号，更看 Issue/PR 的时效性判断动能。",
            "",
            "### 趋势信号 | Signals",
            "- **EN:** Multi-agent delegation, safer defaults, and cross-runtime portability are recurring themes.",
            "- **中文：** 多智能体委派、更安全的默认配置与跨运行时迁移是反复出现的主题。",
            "",
            "## 同赛道项目详细报告 | Peer project reports",
            "",
        ]
    )

    for p in peers:
        nm = p.get("display_name", "Peer")
        lines.append("<details>")
        lines.append(f"<summary><strong>{nm}</strong></summary>")
        lines.append("")
        if not p.get("repo"):
            lines.append("*请在 `config/sources.yaml` → `openclaw_peers` 配置 `repo`。* / *Configure `repo` in YAML.*")
            lines.append("")
            lines.append("</details>")
            lines.append("")
            continue
        lines.extend(
            [
                "#### 今日速览 | Today",
                f"- Issues / PRs / Releases (window): **{len(p.get('issues', []))}** / **{len(p.get('prs', []))}** / **{len(p.get('releases', []))}**",
                "",
                "#### 版本发布 | Releases",
                *[ _rel_line(x) for x in p.get("releases", [])[:6] ] or ["*None.*"],
                "",
                "#### 项目进展 | Progress",
                *[ _pr_line(x) for x in p.get("prs", [])[:6] ] or ["*None.*"],
                "",
                "#### 社区热点 | Community",
                *[ _issue_line(x) for x in p.get("issues", [])[:6] ] or ["*None.*"],
                "",
                "#### Bug / 稳定性 | Bugs & stability",
                "- **EN:** Track `bug`/`regression` labels in issues when available; triage by recency.",
                "- **中文：** 在 Issue 中关注 `bug`/`regression` 等标签并按时间排序。",
                "",
                "#### 功能请求 | Feature requests",
                "- **EN:** Cluster enhancement issues to infer roadmap pressure.",
                "- **中文：** 聚合 enhancement 类 Issue 推断路线图压力。",
                "",
                "#### 用户反馈 | User feedback",
                "- **EN:** High-comment issues often surface UX pain points.",
                "- **中文：** 高评论 Issue 常暴露体验痛点。",
                "",
                "#### 待处理积压 | Backlog",
                "- **EN:** Use open issue count + age as a coarse backlog signal.",
                "- **中文：** 用 Open Issue 数量与龄期粗看积压。",
                "",
            ]
        )
        lines.append("</details>")
        lines.append("")

    return "\n".join(lines) + "\n"


def _openclaw_sections(bundle: Dict[str, Any], is_primary: bool) -> List[str]:
    if not bundle.get("repo"):
        return ["*OpenClaw 仓库未配置。* / *OpenClaw repo missing in config.*", ""]
    issues, prs, rels = bundle.get("issues", []), bundle.get("prs", []), bundle.get("releases", [])
    tag = "OpenClaw" if is_primary else bundle.get("display_name", "Project")
    return [
        f"*{tag} — Issues: {len(issues)} · PRs: {len(prs)} · Releases: {len(rels)}*",
        "",
        "### 今日速览 | Today",
        *[ _issue_line(x) for x in issues[:5] ] or ["*No issues in window.*"],
        "",
        "### 版本发布 | Releases",
        *[ _rel_line(x) for x in rels[:6] ] or ["*None.*"],
        "",
        "### 项目进展 | Progress",
        *[ _pr_line(x) for x in prs[:8] ] or ["*None.*"],
        "",
        "### 社区热点 | Community",
        *[ _issue_line(x) for x in issues[5:12] ] or ["*—*"],
        "",
        "### Bug / 稳定性 | Stability",
        "- **EN:** Monitor crash reports, flaky CI, and security advisories in releases.",
        "- **中文：** 关注崩溃报告、不稳定 CI 与 Release 中的安全通告。",
        "",
        "### 功能请求 | Feature requests",
        "- **EN:** Group enhancement issues to see demand concentration.",
        "- **中文：** 归类 enhancement 需求看集中度。",
        "",
        "### 用户反馈 | Feedback",
        "- **EN:** Look for repeated complaints in long threads.",
        "- **中文：** 在长讨论中识别重复抱怨点。",
        "",
        "### 待处理积压 | Backlog",
        "- **EN:** Track oldest open issues with high 👍 reactions when available.",
        "- **中文：** 若有 👍 反应数据，可结合最早未关闭 Issue 观察积压。",
        "",
    ]


def render_ai_web_md(run_date: dt.date, ctx: Dict[str, Any]) -> str:
    new_a = ctx.get("web_new_anthropic", [])
    new_o = ctx.get("web_new_openai", [])
    na, no = len(new_a), len(new_o)
    first = ctx.get("web_first_full", False)

    lines = [
        f"# AI Web Pulse | 官网情报 · {run_date.isoformat()}",
        "",
        f"**数据来源 | Sources:** **anthropic.com** ({na} new URLs) + **openai.com** ({no} new URLs) *（Sitemap 增量）*",
        "",
        "## 今日速览 | Today",
        "- **EN:** Incremental URLs discovered since last successful run; classify by path for quick scanning.",
        "- **中文：** 相对上次运行新增的 URL；按路径粗分为新闻 / 研究 / 工程等。",
        "",
        "## Anthropic / Claude 内容精选 | Anthropic picks",
        "",
    ]
    lines.extend(_web_bucket(new_a, classify_anthropic_url))
    lines.extend(["", "## OpenAI 内容精选 | OpenAI picks", ""])
    lines.extend(_web_bucket(new_o, classify_openai_url))
    lines.extend(
        [
            "",
            "## 战略信号解读 | Strategic read",
            "- **EN:** Cluster announcements around safety, enterprise adoption, and model capability jumps.",
            "- **中文：** 将公告按安全、企业采用与能力跃迁聚类解读。",
            "",
            "## 值得关注的细节 | Notable details",
            "- **EN:** Prefer URLs with fresh `lastmod` and non-generic paths (news/research).",
            "- **中文：** 优先 `lastmod` 较新且路径非泛化首页的条目。",
            "",
        ]
    )
    if first:
        lines.extend(
            [
                "## 内容格局总览 | Full snapshot (first run)",
                "- **EN:** First run seeds the sitemap cache; subsequent runs show deltas only.",
                "- **中文：** 首次运行写入缓存，此后仅展示增量。",
                "",
            ]
        )
    return "\n".join(lines) + "\n"


def _web_bucket(rows: List[Dict[str, str]], classifier) -> List[str]:
    buckets: Dict[str, List[str]] = {"news": [], "research": [], "engineering": [], "learn": [], "release": [], "company": [], "safety": [], "other": []}
    for row in rows[:35]:
        loc = row.get("loc", "")
        cat = classifier(loc)
        line = f"- {_link(loc.split('/')[-1][:80], loc)} · `{row.get('lastmod', '')[:10]}`"
        if cat in buckets:
            buckets[cat].append(line)
        else:
            buckets["other"].append(line)
    out: List[str] = []
    for key, title in [
        ("news", "news"),
        ("research", "research"),
        ("engineering", "engineering / product"),
        ("learn", "learn"),
        ("release", "release / blog"),
        ("company", "company"),
        ("safety", "safety"),
        ("other", "other"),
    ]:
        if buckets[key]:
            out.append(f"### {title}")
            out.extend(buckets[key][:12])
            out.append("")
    if not out:
        out.append("*No new URLs in this run.*")
    return out


def render_ai_trending_md(run_date: dt.date, ctx: Dict[str, Any]) -> str:
    trending = ctx.get("trending_repos", [])
    dims = ctx.get("trending_dimensions", [])

    lines = [
        f"# AI Trending | GitHub 趋势 · {run_date.isoformat()}",
        "",
        "**数据来源 | Sources:** GitHub Trending (HTML) + GitHub Search API",
        "",
        "## 今日速览 | Today",
        "- **EN:** Blend editorial trending with topic-scoped search to reduce single-metric bias.",
        "- **中文：** 将 Trending 与主题检索结合，降低单一指标偏差。",
        "",
        "## 各维度热门项目 | Hot repos by dimension",
        "",
    ]
    for d in dims:
        emoji = d.get("emoji", "•")
        tzh = d.get("title_zh", "")
        ten = d.get("title_en", "")
        repos = d.get("repos", [])
        lines.append(f"### {emoji} {tzh} — *{ten}*")
        lines.append("")
        for r in repos[:8]:
            lines.append(
                f"- {_link(r.get('full_name', ''), r.get('html_url', '#'))} — ⭐ {r.get('stargazers_count', 0):,} · "
                f"{(r.get('description') or '')[:120]}"
            )
        if not repos:
            lines.append("*No results (quota or query).*")
        lines.append("")

    lines.extend(
        [
            "### GitHub Trending (daily) | 今日 Trending",
            "",
        ]
    )
    for t in trending[:12]:
        lines.append(f"- {_link(t['name'], t['url'])} — {t.get('desc', '')[:100]} · stars **{t.get('stars', '-')}**")
    lines.extend(
        [
            "",
            "## 趋势信号分析 | Signal analysis",
            "- **EN:** When multiple dimensions converge on the same repo family, treat it as a stronger signal.",
            "- **中文：** 多个维度指向同一仓库家族时，信号权重更高。",
            "",
            "## 社区关注热点 | Community focus",
            "- **EN:** Cross-check trending names with HN front-page topics when overlap appears.",
            "- **中文：** 与 HN 头条交叉验证可提高可信度。",
            "",
        ]
    )
    return "\n".join(lines) + "\n"


def render_ai_hn_md(run_date: dt.date, ctx: Dict[str, Any]) -> str:
    posts: List[Dict[str, Any]] = ctx.get("hn_posts", [])
    buckets: Dict[str, List[Dict[str, Any]]] = {"research": [], "tools": [], "business": [], "opinion": []}
    for h in posts:
        buckets[categorize_hn_post(h)].append(h)

    lines = [
        f"# Hacker News AI | 社区脉搏 · {run_date.isoformat()}",
        "",
        "**数据来源 | Source:** Hacker News — **top 30** AI-related stories (last 24h, Algolia API)",
        "",
        "## 今日速览 | Today",
        f"- **EN:** {len(posts)} stories ranked by points; grouped for faster reading.",
        f"- **中文：** 共 {len(posts)} 条，按分数排序并分组速读。",
        "",
        "## 热门新闻与讨论 | Hot stories",
        "",
        "### 🔬 模型与研究 | Models & research",
        "",
    ]
    lines.extend(_hn_list(buckets["research"][:10]))
    lines.extend(["", "### 🛠️ 工具与工程 | Tools & engineering", ""])
    lines.extend(_hn_list(buckets["tools"][:10]))
    lines.extend(["", "### 🏢 产业动态 | Industry", ""])
    lines.extend(_hn_list(buckets["business"][:8]))
    lines.extend(["", "### 💬 观点与争议 | Opinions & debates", ""])
    lines.extend(_hn_list(buckets["opinion"][:12]))

    pos = sum(1 for h in posts if (h.get("points") or 0) >= 50)
    lines.extend(
        [
            "",
            "## 社区情绪信号 | Sentiment",
            f"- **EN:** High-score threads ({pos} with ≥50 pts) often anchor the day's narrative.",
            f"- **中文：** 高分帖（≥50 分共 **{pos}** 条）常构成当日叙事主轴。",
            "",
            "## 值得深读 | Worth a deep read",
            "",
        ]
    )
    for h in posts[:5]:
        url = h.get("url") or f"https://news.ycombinator.com/item?id={h.get('objectID')}"
        lines.append(f"- {_link(h.get('title', '')[:90], url)} — **{h.get('points', 0)}** pts · {h.get('num_comments', 0)} comments")
    lines.append("")
    return "\n".join(lines) + "\n"


def _hn_list(items: List[Dict[str, Any]]) -> List[str]:
    if not items:
        return ["*Empty.*"]
    lines = []
    for h in items:
        url = h.get("url") or f"https://news.ycombinator.com/item?id={h.get('objectID')}"
        lines.append(f"- {_link(h.get('title', '')[:100], url)} — **{h.get('points', 0)}** pts")
    return lines


def write_all_digest_files(day_dir: Path, run_date: dt.date, ctx: Dict[str, Any]) -> Dict[str, Path]:
    day_dir.mkdir(parents=True, exist_ok=True)
    mapping = {
        "ai-cli.md": render_ai_cli_md(run_date, ctx),
        "ai-agents.md": render_ai_agents_md(run_date, ctx),
        "ai-web.md": render_ai_web_md(run_date, ctx),
        "ai-trending.md": render_ai_trending_md(run_date, ctx),
        "ai-hn.md": render_ai_hn_md(run_date, ctx),
    }
    paths = {}
    for name, body in mapping.items():
        p = day_dir / name
        p.write_text(body, encoding="utf-8")
        paths[name] = p
    return paths
