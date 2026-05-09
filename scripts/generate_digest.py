import argparse
import datetime as dt
import json
import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List

import requests
import yaml
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "sources.yaml"
DIGEST_ROOT = ROOT / "digests"
STATE_DIR = DIGEST_ROOT / "state"

UTC = dt.timezone.utc
CST = dt.timezone(dt.timedelta(hours=8))


def load_config() -> Dict:
    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def gh_get(url: str, token: str = "", params: Dict | None = None) -> requests.Response:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "ai-ecosystem-digest-bot",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return requests.get(url, headers=headers, params=params or {}, timeout=40)


def iso_now() -> dt.datetime:
    return dt.datetime.now(UTC)


def parse_iso(text: str) -> dt.datetime:
    return dt.datetime.fromisoformat(text.replace("Z", "+00:00")).astimezone(UTC)


def fetch_repo_meta(repo: str, token: str = "") -> Dict:
    res = gh_get(f"https://api.github.com/repos/{repo}", token=token)
    if res.status_code == 200:
        return res.json()
    return {}


def fetch_repo_24h_activity(repo: str, since_iso: str, token: str = "") -> Dict:
    issues, prs, releases = [], [], []

    issues_res = gh_get(
        f"https://api.github.com/repos/{repo}/issues",
        token=token,
        params={"state": "all", "since": since_iso, "per_page": 100},
    )
    if issues_res.status_code == 200:
        for item in issues_res.json():
            if "pull_request" not in item:
                issues.append(item)

    prs_res = gh_get(
        f"https://api.github.com/repos/{repo}/pulls",
        token=token,
        params={"state": "all", "sort": "updated", "direction": "desc", "per_page": 100},
    )
    if prs_res.status_code == 200:
        for pr in prs_res.json():
            if parse_iso(pr.get("updated_at", "1970-01-01T00:00:00Z")) >= parse_iso(since_iso):
                prs.append(pr)

    rel_res = gh_get(f"https://api.github.com/repos/{repo}/releases", token=token, params={"per_page": 50})
    if rel_res.status_code == 200:
        for rel in rel_res.json():
            published_at = rel.get("published_at")
            if published_at and parse_iso(published_at) >= parse_iso(since_iso):
                releases.append(rel)

    return {"issues": issues, "prs": prs, "releases": releases}


def md_link(title: str, url: str) -> str:
    return f"[{title}]({url})"


def short(text: str, max_len: int = 120) -> str:
    t = " ".join((text or "").split())
    if len(t) <= max_len:
        return t
    return t[: max_len - 3] + "..."


def render_cli_digest(report_date: dt.date, config: Dict, token: str) -> str:
    since_iso = (dt.datetime.now(UTC) - dt.timedelta(hours=24)).replace(microsecond=0).isoformat()
    lines = [
        f"# AI CLI Daily ({report_date.isoformat()})",
        "",
        "Brief intro: 24h Issues/PRs/Releases updates for tracked CLI repos,",
        "plus side-by-side tool comparison.",
        "",
    ]
    table_rows = []
    for repo in config.get("ai_cli_repos", []):
        meta = fetch_repo_meta(repo, token=token)
        act = fetch_repo_24h_activity(repo, since_iso, token=token)
        stars = meta.get("stargazers_count", 0)
        table_rows.append(
            f"| {repo} | {stars} | {len(act['issues'])} | {len(act['prs'])} | {len(act['releases'])} |"
        )

        lines.extend([f"## {repo}", ""])
        lines.append(
            f"- Repo: {md_link(repo, f'https://github.com/{repo}')} | "
            f"Stars: {stars} | Updated: {meta.get('updated_at', '-')}"
        )
        lines.append(f"- 24h stats: Issues {len(act['issues'])}, PRs {len(act['prs'])}, Releases {len(act['releases'])}")
        lines.append("- Highlights:")
        items = act["issues"][:2] + act["prs"][:2] + act["releases"][:1]
        if not items:
            lines.append("- No notable public updates in the last 24h.")
        for it in items:
            title = short(it.get("title") or it.get("name") or "(no title)")
            url = it.get("html_url", "")
            lines.append(f"- {title} ({url})")
        lines.append("")

    lines.extend(
        [
            "## Cross-tool comparison",
            "",
            "| Repository | Stars | Issues(24h) | PRs(24h) | Releases(24h) |",
            "|---|---:|---:|---:|---:|",
            *table_rows,
        ]
    )
    return "\n".join(lines) + "\n"


def fetch_claude_skills(token: str, query: str, limit: int = 20) -> List[Dict]:
    q = f"{query} in:name,description,readme stars:>=20 archived:false"
    res = gh_get(
        "https://api.github.com/search/repositories",
        token=token,
        params={"q": q, "sort": "stars", "order": "desc", "per_page": limit},
    )
    if res.status_code != 200:
        return []
    repos = []
    for item in res.json().get("items", []):
        engagement = item.get("stargazers_count", 0) + item.get("forks_count", 0) * 2 + item.get("open_issues_count", 0)
        item["engagement"] = engagement
        repos.append(item)
    repos.sort(key=lambda x: x.get("engagement", 0), reverse=True)
    return repos


def render_agents_digest(report_date: dt.date, config: Dict, token: str) -> str:
    since_iso = (dt.datetime.now(UTC) - dt.timedelta(hours=24)).replace(microsecond=0).isoformat()
    lines = [
        f"# AI Agents & OpenClaw ({report_date.isoformat()})",
        "",
        "Brief intro: OpenClaw deep report, 10-project benchmark, and Claude Code Skills ranking by engagement.",
        "",
    ]
    primary = config.get("openclaw_primary_repo")
    compare_repos = config.get("openclaw_compare_repos", [])
    all_repos = [primary] + compare_repos
    rows = []
    for repo in all_repos:
        meta = fetch_repo_meta(repo, token=token)
        act = fetch_repo_24h_activity(repo, since_iso, token=token)
        rows.append(
            "| {repo} | {stars} | {forks} | {issues} | {prs} | {rels} | {updated} |".format(
                repo=repo,
                stars=meta.get("stargazers_count", 0),
                forks=meta.get("forks_count", 0),
                issues=len(act["issues"]),
                prs=len(act["prs"]),
                rels=len(act["releases"]),
                updated=meta.get("updated_at", "-"),
            )
        )

    lines.extend(
        [
            "## OpenClaw deep report",
            "",
            f"- Primary repo: {md_link(primary, f'https://github.com/{primary}')}",
            "- Dimensions: stars, forks, last-24h Issues/PRs/Releases, last update.",
            "",
            "## OpenClaw vs 10 peers",
            "",
            "| Repo | Stars | Forks | Issues(24h) | PRs(24h) | Releases(24h) | Updated |",
            "|---|---:|---:|---:|---:|---:|---|",
            *rows,
            "",
        ]
    )

    skills = fetch_claude_skills(token=token, query=config.get("claude_skills_search_query", "claude code skill"), limit=15)
    lines.extend(
        [
            "## Hot Claude Code Skills (by engagement)",
            "",
            "| Repo | Engagement | Stars | Forks | Open issues | Link |",
            "|---|---:|---:|---:|---:|---|",
        ]
    )
    if skills:
        for s in skills:
            lines.append(
                f"| {s.get('full_name')} | {s.get('engagement', 0)} | {s.get('stargazers_count', 0)} | "
                f"{s.get('forks_count', 0)} | {s.get('open_issues_count', 0)} | {md_link('source', s.get('html_url', ''))} |"
            )
    else:
        lines.append("| N/A | 0 | 0 | 0 | 0 | N/A |")
    return "\n".join(lines) + "\n"


def extract_sitemap_urls(url: str) -> List[Dict]:
    try:
        res = requests.get(url, timeout=40, headers={"User-Agent": "ai-ecosystem-digest-bot"})
        if res.status_code != 200:
            return []
        root = ET.fromstring(res.text)
    except Exception:
        return []

    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = []
    for node in root.findall(".//sm:url", ns):
        loc = node.findtext("sm:loc", default="", namespaces=ns)
        lastmod = node.findtext("sm:lastmod", default="", namespaces=ns)
        if loc:
            urls.append({"loc": loc, "lastmod": lastmod})
    return urls


def load_state() -> Dict:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    state_path = STATE_DIR / "web_seen.json"
    if not state_path.exists():
        return {}
    try:
        return json.loads(state_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def save_state(state: Dict) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    (STATE_DIR / "web_seen.json").write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def render_web_digest(report_date: dt.date, config: Dict) -> str:
    state = load_state()
    sources = config.get("sitemap_sources", {})
    lines = [
        f"# AI Web Sources ({report_date.isoformat()})",
        "",
        "Brief intro: sitemap-based incremental detection for Anthropic and OpenAI pages.",
        "",
    ]
    for site, sitemap_urls in sources.items():
        seen = set(state.get(site, []))
        latest = []
        for sm_url in sitemap_urls:
            latest.extend(extract_sitemap_urls(sm_url))
        unique_latest = {x["loc"]: x for x in latest}
        fresh = [v for k, v in unique_latest.items() if k not in seen]
        fresh.sort(key=lambda x: x.get("lastmod", ""), reverse=True)

        lines.extend([f"## {site.title()}", "", f"- Sources: {', '.join(sitemap_urls)}", "- New pages detected:", ""])
        if not fresh:
            lines.append("- No new pages detected from sitemap delta.")
        for row in fresh[:25]:
            title = row["loc"].rstrip("/").split("/")[-1].replace("-", " ") or row["loc"]
            lines.append(f"- {title}: {row['loc']} (lastmod: {row.get('lastmod', '-')})")
        lines.append("")
        state[site] = list(unique_latest.keys())[:5000]

    save_state(state)
    return "\n".join(lines) + "\n"


def fetch_trending_repos(url: str, limit: int = 20) -> List[Dict]:
    res = requests.get(url, timeout=40, headers={"User-Agent": "ai-ecosystem-digest-bot"})
    if res.status_code != 200:
        return []
    soup = BeautifulSoup(res.text, "html.parser")
    repos = []
    for article in soup.select("article.Box-row")[:limit]:
        a = article.select_one("h2 a")
        desc = article.select_one("p")
        stars = article.select_one("a[href$='/stargazers']")
        if not a:
            continue
        name = " ".join(a.get_text(strip=True).split()).replace(" / ", "/").replace(" ", "")
        repos.append(
            {
                "name": name,
                "url": f"https://github.com/{name}",
                "desc": short(desc.get_text(" ", strip=True) if desc else ""),
                "stars_today": (stars.get_text(strip=True) if stars else "-"),
            }
        )
    return repos


def topic_dimension(topic: str) -> str:
    mapping = {
        "ai-agent": "Agentic Apps",
        "code-assistant": "Dev Productivity",
        "llm": "Foundation Models",
        "multimodal": "Multimodal UX",
        "rag": "Knowledge & Retrieval",
        "mcp": "Tooling Protocols",
    }
    return mapping.get(topic, "General AI")


def search_topic_repos(topic: str, token: str, limit: int = 8) -> List[Dict]:
    q = f"topic:{topic} stars:>=100 archived:false"
    res = gh_get(
        "https://api.github.com/search/repositories",
        token=token,
        params={"q": q, "sort": "stars", "order": "desc", "per_page": limit},
    )
    if res.status_code != 200:
        return []
    return res.json().get("items", [])


def render_trending_digest(report_date: dt.date, config: Dict, token: str) -> str:
    trending = fetch_trending_repos(config.get("github_trending_url", ""), limit=20)
    topics = config.get("topic_labels", [])[:6]
    lines = [
        f"# AI Trending Signals ({report_date.isoformat()})",
        "",
        "Brief intro: combines GitHub Trending and six topic-tag searches, grouped by dimensions.",
        "",
        "## GitHub Trending (daily)",
        "",
    ]
    for t in trending[:15]:
        lines.append(f"- {md_link(t['name'], t['url'])}: {t['desc']} (stars today: {t['stars_today']})")
    lines.append("")

    lines.extend(["## Topic-based scan (6 tags)", ""])
    signals = []
    for topic in topics:
        rows = search_topic_repos(topic, token=token, limit=6)
        dim = topic_dimension(topic)
        stars = [r.get("stargazers_count", 0) for r in rows]
        avg_stars = int(sum(stars) / len(stars)) if stars else 0
        signals.append((topic, dim, len(rows), avg_stars))
        lines.append(f"### #{topic} ({dim})")
        for r in rows:
            lines.append(
                f"- {md_link(r.get('full_name', ''), r.get('html_url', ''))}: "
                f"{short(r.get('description', ''))} (stars: {r.get('stargazers_count', 0)})"
            )
        if not rows:
            lines.append("- No qualified repositories found.")
        lines.append("")

    lines.extend(["## Trend signals", "", "| Tag | Dimension | Result count | Avg stars |", "|---|---|---:|---:|"])
    for topic, dim, count, avg in signals:
        lines.append(f"| #{topic} | {dim} | {count} | {avg} |")
    return "\n".join(lines) + "\n"


def fetch_hn_ai_posts(last_24h_epoch: int, limit: int = 30) -> List[Dict]:
    queries = ["ai", "llm", "agent", "openai", "anthropic", "claude"]
    merged = {}
    for q in queries:
        url = "https://hn.algolia.com/api/v1/search_by_date"
        params = {"query": q, "tags": "story", "numericFilters": f"created_at_i>{last_24h_epoch}", "hitsPerPage": 100}
        try:
            res = requests.get(url, params=params, timeout=40)
        except requests.RequestException:
            continue
        if res.status_code != 200:
            continue
        for hit in res.json().get("hits", []):
            obj_id = hit.get("objectID")
            if not obj_id:
                continue
            pts = hit.get("points") or 0
            prev = merged.get(obj_id)
            if not prev or pts > (prev.get("points") or 0):
                merged[obj_id] = hit
    posts = list(merged.values())
    posts.sort(key=lambda x: x.get("points") or 0, reverse=True)
    return posts[:limit]


def sentiment_score(title: str) -> str:
    t = title.lower()
    pos = len(re.findall(r"\b(breakthrough|launch|improve|success|faster|open source)\b", t))
    neg = len(re.findall(r"\b(risk|lawsuit|ban|problem|fail|unsafe|concern)\b", t))
    if pos > neg:
        return "Positive"
    if neg > pos:
        return "Negative"
    return "Neutral"


def render_hn_digest(report_date: dt.date) -> str:
    now = dt.datetime.now(UTC)
    posts = fetch_hn_ai_posts(int((now - dt.timedelta(hours=24)).timestamp()), limit=30)
    lines = [
        f"# Hacker News AI Pulse ({report_date.isoformat()})",
        "",
        "Brief intro: top 30 AI-related HN posts in last 24h sorted by score, with lightweight sentiment cues.",
        "",
        "| Rank | Title | Score | Comments | Sentiment | Link |",
        "|---:|---|---:|---:|---|---|",
    ]
    sentiment_counter = {"Positive": 0, "Neutral": 0, "Negative": 0}
    for idx, p in enumerate(posts, start=1):
        title = short(p.get("title") or "(no title)", max_len=90)
        score = p.get("points") or 0
        comments = p.get("num_comments") or 0
        sent = sentiment_score(title)
        sentiment_counter[sent] += 1
        url = p.get("url") or f"https://news.ycombinator.com/item?id={p.get('objectID')}"
        lines.append(f"| {idx} | {title} | {score} | {comments} | {sent} | {md_link('source', url)} |")

    lines.extend(
        [
            "",
            "## Community sentiment snapshot",
            "",
            f"- Positive: {sentiment_counter['Positive']}",
            f"- Neutral: {sentiment_counter['Neutral']}",
            f"- Negative: {sentiment_counter['Negative']}",
        ]
    )
    return "\n".join(lines) + "\n"


def write_digest_files(report_date: dt.date, sections: Dict[str, str]) -> Dict[str, str]:
    day_dir = DIGEST_ROOT / report_date.isoformat()
    day_dir.mkdir(parents=True, exist_ok=True)
    out_paths = {}
    for name, content in sections.items():
        path = day_dir / f"{name}.md"
        path.write_text(content, encoding="utf-8")
        out_paths[name] = str(path.as_posix())
    return out_paths


def build_issue_body(report_date: dt.date, out_paths: Dict[str, str]) -> str:
    rel = lambda p: p.replace(str(ROOT).replace("\\", "/") + "/", "")
    lines = [
        f"# AI Daily Multi-Report ({report_date.isoformat()})",
        "",
        "Daily report bundle generated by GitHub Actions. Includes links and source references.",
        "",
        "## Files",
        "",
        f"- `ai-cli.md`: `{rel(out_paths['ai-cli'])}`",
        f"- `ai-agents.md`: `{rel(out_paths['ai-agents'])}`",
        f"- `ai-web.md`: `{rel(out_paths['ai-web'])}`",
        f"- `ai-trending.md`: `{rel(out_paths['ai-trending'])}`",
        f"- `ai-hn.md`: `{rel(out_paths['ai-hn'])}`",
        "",
        "## Notes",
        "",
        "- Time window for repo/HN scans: last 24 hours.",
        "- Web updates are sitemap-based incremental detections.",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default="", help="Date in YYYY-MM-DD (CST)")
    args = parser.parse_args()

    config = load_config()
    token = os.getenv("GH_PAT", "").strip() or os.getenv("GITHUB_TOKEN", "").strip()
    report_date = (
        dt.datetime.strptime(args.date, "%Y-%m-%d").date() if args.date else dt.datetime.now(CST).date()
    )

    sections = {
        "ai-cli": render_cli_digest(report_date, config, token),
        "ai-agents": render_agents_digest(report_date, config, token),
        "ai-web": render_web_digest(report_date, config),
        "ai-trending": render_trending_digest(report_date, config, token),
        "ai-hn": render_hn_digest(report_date),
    }
    out_paths = write_digest_files(report_date, sections)

    issue_title = f"AI Daily Multi-Report - {report_date.isoformat()}"
    issue_body = build_issue_body(report_date, out_paths)
    issue_body_path = DIGEST_ROOT / "latest_issue_body.md"
    issue_body_path.write_text(issue_body, encoding="utf-8")

    meta = {
        "date": report_date.isoformat(),
        "digest_dir": str((DIGEST_ROOT / report_date.isoformat()).as_posix()),
        "issue_title": issue_title,
        "issue_body_file": str(issue_body_path.as_posix()),
    }
    (DIGEST_ROOT / "latest_daily_meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(meta, ensure_ascii=False))


if __name__ == "__main__":
    main()
