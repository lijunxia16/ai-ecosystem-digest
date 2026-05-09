from __future__ import annotations

import datetime as dt
import random
import time
from typing import Dict, Iterable, List

import requests

from .models import RawItem

UTC = dt.timezone.utc


class Scraper:
    """
    Multi-source scraper with anti-bot and retry strategies.
    多源抓取器，包含反爬处理（UA轮换、抖动）和超时重试逻辑。
    """

    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Version/17.0 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36",
    ]

    def __init__(self, github_token: str = "", timeout_sec: int = 20, max_retries: int = 3) -> None:
        self.github_token = github_token.strip()
        self.timeout_sec = timeout_sec
        self.max_retries = max_retries

    def _request(self, url: str, headers: Dict[str, str] | None = None, params: Dict | None = None) -> requests.Response:
        base_headers = {
            "User-Agent": random.choice(self.USER_AGENTS),
            "Accept": "application/json",
        }
        if self.github_token and "api.github.com" in url:
            base_headers["Authorization"] = f"Bearer {self.github_token}"
            base_headers["Accept"] = "application/vnd.github+json"
        if headers:
            base_headers.update(headers)

        for attempt in range(self.max_retries + 1):
            try:
                # Random sleep helps reduce burst patterns.
                # 随机抖动可降低连续请求触发风控的概率。
                time.sleep(random.uniform(0.2, 1.1))
                res = requests.get(url, headers=base_headers, params=params or {}, timeout=self.timeout_sec)
                if res.status_code in (429, 500, 502, 503, 504):
                    if attempt < self.max_retries:
                        time.sleep(2 ** attempt)
                        continue
                return res
            except requests.RequestException:
                if attempt >= self.max_retries:
                    raise
                time.sleep(2 ** attempt)
        raise RuntimeError(f"Unreachable retry branch for {url}")

    def fetch_repo_activity_24h(self, repos: Iterable[str]) -> List[RawItem]:
        since = dt.datetime.now(UTC) - dt.timedelta(hours=24)
        items: List[RawItem] = []
        for repo in repos:
            base = f"https://api.github.com/repos/{repo}"
            for endpoint, kind in [("/issues", "issue"), ("/pulls", "pr"), ("/releases", "release")]:
                try:
                    res = self._request(
                        f"{base}{endpoint}",
                        params={"state": "all", "per_page": 50, "sort": "updated", "direction": "desc"},
                    )
                except requests.RequestException:
                    continue
                if res.status_code != 200:
                    continue
                for obj in res.json():
                    created = obj.get("created_at") or obj.get("published_at") or obj.get("updated_at")
                    if not created:
                        continue
                    created_at = dt.datetime.fromisoformat(created.replace("Z", "+00:00")).astimezone(UTC)
                    if created_at < since:
                        continue
                    title = obj.get("title") or obj.get("name") or f"{repo} {kind}"
                    html = obj.get("html_url") or f"https://github.com/{repo}"
                    body = obj.get("body") or ""
                    items.append(
                        RawItem(
                            source="github",
                            external_id=f"{repo}:{kind}:{obj.get('id', obj.get('node_id', title))}",
                            title=title,
                            url=html,
                            content=body[:3000],
                            created_at=created_at,
                            metadata={"repo": repo, "kind": kind},
                        )
                    )
        return items

    def fetch_hn_ai_top30(self) -> List[RawItem]:
        now = int(dt.datetime.now(UTC).timestamp())
        since = now - 24 * 3600
        try:
            res = self._request(
                "https://hn.algolia.com/api/v1/search_by_date",
                params={"query": "ai", "tags": "story", "numericFilters": f"created_at_i>{since}", "hitsPerPage": 100},
            )
        except requests.RequestException:
            return []
        if res.status_code != 200:
            return []
        hits = sorted(res.json().get("hits", []), key=lambda x: x.get("points") or 0, reverse=True)[:30]
        rows = []
        for hit in hits:
            url = hit.get("url") or f"https://news.ycombinator.com/item?id={hit.get('objectID')}"
            created_at = dt.datetime.fromisoformat(hit["created_at"].replace("Z", "+00:00")).astimezone(UTC)
            rows.append(
                RawItem(
                    source="hn",
                    external_id=f"hn:{hit.get('objectID')}",
                    title=hit.get("title") or "(no title)",
                    url=url,
                    content=(hit.get("story_text") or "")[:2000],
                    created_at=created_at,
                    metadata={"points": hit.get("points", 0), "comments": hit.get("num_comments", 0)},
                )
            )
        return rows
