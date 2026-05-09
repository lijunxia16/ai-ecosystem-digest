"""
Extended scraping for structured digest reports (CLI / agents / web / trending / HN).
扩展抓取：为五份专题 Markdown 提供结构化数据。
"""

from __future__ import annotations

import datetime as dt
import json
import random
import re
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Dict, List, Tuple

import requests
from bs4 import BeautifulSoup

UTC = dt.timezone.utc


def _parse_github_dt(s: str) -> dt.datetime:
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(UTC)


class GitHubClient:
    """Minimal GitHub REST client with retries (shared pattern with Scraper)."""

    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Version/17.0 Safari/605.1.15",
    ]

    def __init__(self, token: str, timeout: int = 25, max_retries: int = 3) -> None:
        self.token = (token or "").strip()
        self.timeout = timeout
        self.max_retries = max_retries

    def get(self, url: str, params: Dict[str, Any] | None = None) -> requests.Response | None:
        headers = {
            "User-Agent": random.choice(self.USER_AGENTS),
            "Accept": "application/vnd.github+json",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        for attempt in range(self.max_retries + 1):
            try:
                time.sleep(random.uniform(0.15, 0.9))
                r = requests.get(url, headers=headers, params=params or {}, timeout=self.timeout)
                if r.status_code in (429, 500, 502, 503, 504) and attempt < self.max_retries:
                    time.sleep(2**attempt)
                    continue
                return r
            except requests.RequestException:
                if attempt >= self.max_retries:
                    return None
                time.sleep(2**attempt)
        return None

    def json_or_none(self, url: str, params: Dict[str, Any] | None = None) -> Any:
        r = self.get(url, params)
        if not r or r.status_code != 200:
            return None
        try:
            return r.json()
        except ValueError:
            return None


def fetch_repo_bundle(gh: GitHubClient, repo: str, since: dt.datetime) -> Dict[str, Any]:
    """Issues (non-PR), PRs, releases updated in last 24h-ish window."""
    if not repo or "/" not in repo:
        return {"repo": repo, "meta": None, "issues": [], "prs": [], "releases": []}

    meta = gh.json_or_none(f"https://api.github.com/repos/{repo}")
    since_iso = since.replace(microsecond=0).isoformat().replace("+00:00", "Z")

    issues_raw = gh.json_or_none(
        f"https://api.github.com/repos/{repo}/issues",
        {"state": "all", "since": since_iso, "per_page": 50},
    )
    issues: List[Dict[str, Any]] = []
    if isinstance(issues_raw, list):
        for it in issues_raw:
            if "pull_request" in it:
                continue
            issues.append(it)

    prs_raw = gh.json_or_none(
        f"https://api.github.com/repos/{repo}/pulls",
        {"state": "all", "sort": "updated", "direction": "desc", "per_page": 50},
    )
    prs: List[Dict[str, Any]] = []
    if isinstance(prs_raw, list):
        for pr in prs_raw:
            u = pr.get("updated_at") or pr.get("created_at")
            if u and _parse_github_dt(u) >= since:
                prs.append(pr)

    rel_raw = gh.json_or_none(f"https://api.github.com/repos/{repo}/releases", {"per_page": 30})
    releases: List[Dict[str, Any]] = []
    if isinstance(rel_raw, list):
        for rel in rel_raw:
            pub = rel.get("published_at")
            if pub and _parse_github_dt(pub) >= since:
                releases.append(rel)

    return {"repo": repo, "meta": meta, "issues": issues, "prs": prs, "releases": releases}


def search_repositories(gh: GitHubClient, q: str, per_page: int = 8) -> List[Dict[str, Any]]:
    data = gh.json_or_none(
        "https://api.github.com/search/repositories",
        {"q": q, "sort": "stars", "order": "desc", "per_page": per_page},
    )
    if not data or "items" not in data:
        return []
    return list(data["items"])


def fetch_claude_skills(gh: GitHubClient, query: str, limit: int = 12) -> List[Dict[str, Any]]:
    q = f"{query} in:name,description,readme stars:>=30 archived:false"
    items = search_repositories(gh, q, per_page=limit)
    for it in items:
        eng = (it.get("stargazers_count") or 0) + 2 * (it.get("forks_count") or 0) + (it.get("open_issues_count") or 0)
        it["_engagement"] = eng
    items.sort(key=lambda x: x.get("_engagement", 0), reverse=True)
    return items


def fetch_trending_page(url: str, limit: int = 15) -> List[Dict[str, str]]:
    try:
        r = requests.get(url, timeout=25, headers={"User-Agent": "ai-ecosystem-digest/1.0"})
    except requests.RequestException:
        return []
    if r.status_code != 200:
        return []
    soup = BeautifulSoup(r.text, "html.parser")
    out: List[Dict[str, str]] = []
    for article in soup.select("article.Box-row")[:limit]:
        a = article.select_one("h2 a")
        p = article.select_one("p")
        st = article.select_one("a[href$='/stargazers']")
        if not a:
            continue
        name = " ".join(a.get_text(strip=True).split()).replace(" / ", "/").replace(" ", "")
        out.append(
            {
                "name": name,
                "url": f"https://github.com/{name}",
                "desc": (p.get_text(" ", strip=True) if p else "")[:200],
                "stars": st.get_text(strip=True) if st else "-",
            }
        )
    return out


def parse_sitemap_urls(sitemap_url: str) -> List[Dict[str, str]]:
    try:
        r = requests.get(sitemap_url, timeout=30, headers={"User-Agent": "ai-ecosystem-digest/1.0"})
        if r.status_code != 200:
            return []
        root = ET.fromstring(r.text)
    except Exception:
        return []
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    rows: List[Dict[str, str]] = []
    for node in root.findall(".//sm:url", ns):
        loc = node.findtext("sm:loc", default="", namespaces=ns)
        lm = node.findtext("sm:lastmod", default="", namespaces=ns)
        if loc:
            rows.append({"loc": loc.strip(), "lastmod": lm.strip()})
    return rows


def web_incremental(
    sitemap_sources: Dict[str, List[str]],
    state_path: Path,
) -> Tuple[Dict[str, List[Dict[str, str]]], Dict[str, int], bool]:
    """
    Return (new_by_site, total_counts_this_run, is_first_full_snapshot).
    """
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state: Dict[str, List[str]] = {}
    if state_path.exists():
        try:
            state = json.loads(state_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            state = {}

    new_by_site: Dict[str, List[Dict[str, str]]] = {}
    totals: Dict[str, int] = {}
    first_full = not bool(state)

    for site, urls in sitemap_sources.items():
        seen = set(state.get(site, []))
        all_urls: Dict[str, Dict[str, str]] = {}
        for sm in urls:
            for row in parse_sitemap_urls(sm):
                all_urls[row["loc"]] = row
        totals[site] = len(all_urls)
        fresh = [v for k, v in all_urls.items() if k not in seen]
        fresh.sort(key=lambda x: x.get("lastmod", ""), reverse=True)
        new_by_site[site] = fresh[:40]
        state[site] = list(all_urls.keys())[:8000]

    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    return new_by_site, totals, first_full


def fetch_hn_top30() -> List[Dict[str, Any]]:
    now = int(dt.datetime.now(UTC).timestamp())
    since = now - 24 * 3600
    merged: Dict[str, Dict[str, Any]] = {}
    for q in ("ai", "llm", "agent", "openai", "anthropic", "claude"):
        try:
            r = requests.get(
                "https://hn.algolia.com/api/v1/search_by_date",
                params={"query": q, "tags": "story", "numericFilters": f"created_at_i>{since}", "hitsPerPage": 80},
                timeout=25,
            )
        except requests.RequestException:
            continue
        if r.status_code != 200:
            continue
        for hit in r.json().get("hits", []):
            oid = hit.get("objectID")
            if not oid:
                continue
            pts = hit.get("points") or 0
            prev = merged.get(oid)
            if not prev or pts > (prev.get("points") or 0):
                merged[oid] = hit
    posts = sorted(merged.values(), key=lambda x: x.get("points") or 0, reverse=True)[:30]
    return posts


def categorize_hn_post(hit: Dict[str, Any]) -> str:
    t = (hit.get("title") or "").lower()
    if "ask hn" in t:
        return "opinion"
    if "show hn" in t:
        return "tools"
    if any(k in t for k in ("paper", "model", "benchmark", "gpt", "llm", "arxiv")):
        return "research"
    if any(k in t for k in ("funding", "ipo", "company", "layoff", "acquire", "startup")):
        return "business"
    if any(k in t for k in ("github", "open source", "release", "framework", "library")):
        return "tools"
    return "opinion"


def classify_anthropic_url(loc: str) -> str:
    loc_l = loc.lower()
    if "/research/" in loc_l:
        return "research"
    if "/news/" in loc_l:
        return "news"
    if "/engineering" in loc_l or "/product" in loc_l:
        return "engineering"
    if "/learn" in loc_l:
        return "learn"
    return "other"


def classify_openai_url(loc: str) -> str:
    loc_l = loc.lower()
    if "/research" in loc_l:
        return "research"
    if "/index/" in loc_l or "blog" in loc_l:
        return "release"
    if "/safety" in loc_l:
        return "safety"
    if "/company" in loc_l or "/about" in loc_l:
        return "company"
    return "other"
