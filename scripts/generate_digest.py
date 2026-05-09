import argparse
import datetime as dt
import json
import os
from pathlib import Path
from typing import Dict, List, Tuple

import feedparser
import requests
import yaml
from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "sources.yaml"
REPORTS_DAILY_DIR = ROOT / "reports" / "daily"

UTC = dt.timezone.utc
CST = dt.timezone(dt.timedelta(hours=8))


def load_config() -> Dict:
    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def gh_get(url: str, token: str = "") -> requests.Response:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "ai-ecosystem-digest-bot",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return requests.get(url, headers=headers, timeout=30)


def fetch_repo_events(repo: str, token: str = "", limit: int = 3) -> List[str]:
    url = f"https://api.github.com/repos/{repo}/events"
    res = gh_get(url, token)
    if res.status_code != 200:
        return fetch_repo_activity_fallback(repo, token=token, limit=limit, code=res.status_code)

    items = []
    for event in res.json()[:limit]:
        etype = event.get("type", "UnknownEvent")
        actor = event.get("actor", {}).get("login", "unknown")
        created = event.get("created_at", "")
        items.append(f"{repo}: {etype} by @{actor} at {created}")
    return items or [f"{repo}: no recent public events"]


def fetch_repo_activity_fallback(
    repo: str, token: str = "", limit: int = 3, code: int = 0
) -> List[str]:
    lines: List[str] = []

    repo_meta_url = f"https://api.github.com/repos/{repo}"
    meta_res = gh_get(repo_meta_url, token)
    if meta_res.status_code == 200:
        meta = meta_res.json()
        lines.append(
            f"{repo}: fallback(meta) ⭐ {meta.get('stargazers_count', 0)} "
            f"| updated {meta.get('updated_at', '-')}"
        )

    commits_feed = f"https://github.com/{repo}/commits.atom"
    commit_items = fetch_feed_items(commits_feed, limit=limit)
    if commit_items:
        for title, link in commit_items:
            lines.append(f"{repo}: fallback(commit) {title} ({link})")

    if not lines:
        lines.append(f"{repo}: unavailable from API/feed (last code {code})")
    else:
        lines.append(f"{repo}: note API events unavailable ({code}), used fallback sources")
    return lines


def fetch_topic_repos(topic: str, token: str = "", limit: int = 5) -> List[str]:
    q = f"topic:{topic} stars:>=50 archived:false"
    url = (
        "https://api.github.com/search/repositories"
        f"?q={q}&sort=updated&order=desc&per_page={limit}"
    )
    res = gh_get(url, token)
    if res.status_code != 200:
        return [f"topic:{topic}: unavailable ({res.status_code})"]
    lines = []
    for repo in res.json().get("items", []):
        lines.append(
            f"{repo.get('full_name')}: ⭐ {repo.get('stargazers_count', 0)} "
            f"| updated {repo.get('updated_at', '-')}"
        )
    return lines or [f"topic:{topic}: no repositories found"]


def fetch_feed_items(url: str, limit: int = 5) -> List[Tuple[str, str]]:
    parsed = feedparser.parse(url)
    items = []
    for entry in parsed.entries[:limit]:
        title = entry.get("title", "(no title)")
        link = entry.get("link", "")
        items.append((title, link))
    return items


def fetch_news(feed_urls: List[str], limit: int = 5) -> List[Tuple[str, str]]:
    for url in feed_urls:
        items = fetch_feed_items(url, limit=limit)
        if items:
            return items
    return [("No feed update found", "")]


def fetch_trending(url: str, limit: int = 10) -> List[str]:
    res = requests.get(url, timeout=30, headers={"User-Agent": "digest-bot"})
    if res.status_code != 200:
        return [f"Failed to fetch trending page ({res.status_code})"]

    soup = BeautifulSoup(res.text, "html.parser")
    repos = []
    for article in soup.select("article.Box-row")[:limit]:
        name_tag = article.select_one("h2 a")
        desc_tag = article.select_one("p")
        star_tag = article.select_one("a[href$='/stargazers']")

        if not name_tag:
            continue

        repo_name = " ".join(name_tag.get_text(strip=True).split())
        repo_name = repo_name.replace(" / ", "/").replace(" ", "")
        desc = desc_tag.get_text(" ", strip=True) if desc_tag else ""
        stars = star_tag.get_text(strip=True) if star_tag else "-"
        repos.append(f"{repo_name}: {desc} | stars {stars}")

    return repos or ["No trending repositories parsed"]


def to_bilingual_markdown(
    report_date: dt.date,
    ai_cli_events: List[str],
    openclaw_events: List[str],
    openclaw_topics: List[str],
    anthropic_news: List[Tuple[str, str]],
    openai_news: List[Tuple[str, str]],
    trending: List[str],
) -> str:
    zh_date = report_date.strftime("%Y-%m-%d")
    en_date = report_date.strftime("%Y-%m-%d")

    def render_news(news: List[Tuple[str, str]]) -> str:
        lines = []
        for title, link in news:
            if link:
                lines.append(f"- {title} ({link})")
            else:
                lines.append(f"- {title}")
        return "\n".join(lines)

    content = f"""# AI Daily Brief | AI 每日简报 ({zh_date})

## 中文版

### 1) 主流 AI CLI 工具 GitHub 动态
{chr(10).join(f"- {x}" for x in ai_cli_events)}

### 2) OpenClaw 与同赛道生态活动
#### 仓库动态
{chr(10).join(f"- {x}" for x in openclaw_events)}

#### 赛道主题热度
{chr(10).join(f"- {x}" for x in openclaw_topics)}

### 3) Anthropic & OpenAI 官网最新资讯
#### Anthropic
{render_news(anthropic_news)}

#### OpenAI
{render_news(openai_news)}

### 4) GitHub AI 热门仓库趋势（每日）
{chr(10).join(f"- {x}" for x in trending)}

---

## English Version

### 1) GitHub Updates of Mainstream AI CLI Tools
{chr(10).join(f"- {x}" for x in ai_cli_events)}

### 2) OpenClaw and Adjacent Ecosystem Activity
#### Repository Activity
{chr(10).join(f"- {x}" for x in openclaw_events)}

#### Theme/Topic Momentum
{chr(10).join(f"- {x}" for x in openclaw_topics)}

### 3) Latest News from Anthropic and OpenAI
#### Anthropic
{render_news(anthropic_news)}

#### OpenAI
{render_news(openai_news)}

### 4) Daily Trending AI Repositories on GitHub
{chr(10).join(f"- {x}" for x in trending)}

---

Generated at: {dt.datetime.now(UTC).isoformat()} UTC | {dt.datetime.now(CST).isoformat()} CST
"""
    return content


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default="", help="Date in YYYY-MM-DD (CST)")
    args = parser.parse_args()

    config = load_config()
    token = os.getenv("GH_PAT", "").strip() or os.getenv("GITHUB_TOKEN", "").strip()

    if args.date:
        report_date = dt.datetime.strptime(args.date, "%Y-%m-%d").date()
    else:
        report_date = dt.datetime.now(CST).date()

    ai_cli_events: List[str] = []
    for repo in config.get("ai_cli_repos", []):
        ai_cli_events.extend(fetch_repo_events(repo, token=token, limit=2))

    openclaw_events: List[str] = []
    for repo in config.get("openclaw_track_repos", []):
        openclaw_events.extend(fetch_repo_events(repo, token=token, limit=2))

    openclaw_topics: List[str] = []
    for topic in config.get("openclaw_track_topics", []):
        openclaw_topics.extend(fetch_topic_repos(topic, token=token, limit=3))

    news_cfg = config.get("news_feeds", {})
    anthropic_news = fetch_news(news_cfg.get("anthropic", []), limit=5)
    openai_news = fetch_news(news_cfg.get("openai", []), limit=5)
    trending = fetch_trending(config.get("github_trending_url"), limit=10)

    markdown = to_bilingual_markdown(
        report_date=report_date,
        ai_cli_events=ai_cli_events,
        openclaw_events=openclaw_events,
        openclaw_topics=openclaw_topics,
        anthropic_news=anthropic_news,
        openai_news=openai_news,
        trending=trending,
    )

    REPORTS_DAILY_DIR.mkdir(parents=True, exist_ok=True)
    out_file = REPORTS_DAILY_DIR / f"{report_date.isoformat()}.md"
    out_file.write_text(markdown, encoding="utf-8")

    issue_title = f"AI Daily Brief / AI 每日简报 - {report_date.isoformat()}"
    issue_body_path = ROOT / "reports" / "latest_issue_body.md"
    issue_body_path.write_text(markdown, encoding="utf-8")

    meta = {
        "date": report_date.isoformat(),
        "daily_file": str(out_file.as_posix()),
        "issue_title": issue_title,
        "issue_body_file": str(issue_body_path.as_posix()),
    }
    (ROOT / "reports" / "latest_daily_meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(meta, ensure_ascii=False))


if __name__ == "__main__":
    main()
