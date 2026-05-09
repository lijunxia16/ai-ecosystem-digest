from __future__ import annotations

import json
import re
from typing import List

import requests

from .models import AIInsight, RawItem


class LLMProcessor:
    """
    AI classification/summarization with robust fallback chain.
    AI 分类与摘要层，失败时自动降级：
    1) primary model -> 2) backup model -> 3) heuristic keywords
    """

    def __init__(
        self,
        primary_api_key: str = "",
        backup_api_key: str = "",
        primary_model: str = "gpt-4o-mini",
        backup_model: str = "gpt-4.1-mini",
    ) -> None:
        self.primary_api_key = primary_api_key.strip()
        self.backup_api_key = backup_api_key.strip()
        self.primary_model = primary_model
        self.backup_model = backup_model

    def process(self, item: RawItem) -> AIInsight:
        # Try primary model first.
        insight = self._call_model(item, self.primary_api_key, self.primary_model)
        if insight:
            return insight

        # Automatic backup model switch when primary fails.
        # 主模型失败后自动切到备用模型，保证流程不中断。
        insight = self._call_model(item, self.backup_api_key, self.backup_model)
        if insight:
            return insight

        # Final safety net: heuristic rule-based output.
        # 最终兜底：关键词启发式，确保永远有合法结构化输出。
        return self._heuristic_fallback(item)

    def _call_model(self, item: RawItem, api_key: str, model: str) -> AIInsight | None:
        if not api_key:
            return None
        prompt = self._build_prompt(item)
        try:
            res = requests.post(
                "https://api.openai.com/v1/chat/completions",
                timeout=25,
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                json={
                    "model": model,
                    "messages": [{"role": "system", "content": "Return only valid JSON."}, {"role": "user", "content": prompt}],
                    "temperature": 0.2,
                },
            )
        except requests.RequestException:
            return None
        if res.status_code != 200:
            return None
        try:
            text = res.json()["choices"][0]["message"]["content"]
            payload = json.loads(text)
            payload["source_url"] = str(item.url)
            return AIInsight.model_validate(payload)
        except Exception:
            return None

    def _build_prompt(self, item: RawItem) -> str:
        return (
            "Analyze this AI ecosystem item and return JSON with fields: "
            "category, summary_zh, summary_en, sentiment, confidence, tags.\n"
            f"title: {item.title}\n"
            f"content: {item.content[:1000]}\n"
            f"metadata: {item.metadata}\n"
        )

    def _heuristic_fallback(self, item: RawItem) -> AIInsight:
        text = f"{item.title} {item.content}".lower()
        if item.source == "hn":
            category = "ai_hn"
        elif any(k in text for k in ["release", "tag", "version"]):
            category = "ai_cli"
        elif any(k in text for k in ["agent", "workflow", "openclaw", "skill"]):
            category = "ai_agents"
        elif any(k in text for k in ["anthropic", "openai", "research", "news"]):
            category = "ai_web"
        else:
            category = "other"

        sentiment = "neutral"
        if re.search(r"\b(success|launch|improve|faster)\b", text):
            sentiment = "positive"
        if re.search(r"\b(risk|bug|issue|failure|ban)\b", text):
            sentiment = "negative"

        return AIInsight(
            category=category,  # type: ignore[arg-type]
            summary_zh=f"【规则兜底】{item.title[:70]}，来源 {item.source}，建议人工复核细节。",
            summary_en=f"[Heuristic fallback] {item.title[:90]} from {item.source}. Manual review recommended.",
            sentiment=sentiment,  # type: ignore[arg-type]
            confidence=0.45,
            tags=self._extract_tags(text),
            source_url=item.url,
        )

    def _extract_tags(self, text: str) -> List[str]:
        candidates = ["cli", "agent", "openclaw", "release", "issue", "pr", "hn", "model", "security", "benchmark"]
        tags = [c for c in candidates if c in text]
        return tags[:8]
