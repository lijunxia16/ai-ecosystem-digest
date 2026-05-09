from __future__ import annotations

import datetime as dt
from typing import List, Literal

from pydantic import BaseModel, Field, HttpUrl


class RawItem(BaseModel):
    """Raw content fetched by scrapers / 抓取层输出的原始数据."""

    source: str = Field(description="Data source name, e.g. github|hn|web")
    external_id: str = Field(description="Stable ID in source system")
    title: str = Field(min_length=1)
    url: HttpUrl
    content: str = ""
    created_at: dt.datetime
    metadata: dict = Field(default_factory=dict)


class AIInsight(BaseModel):
    """Normalized AI output with strict schema / 结构化 AI 输出."""

    category: Literal[
        "ai_cli",
        "ai_agents",
        "ai_web",
        "ai_trending",
        "ai_hn",
        "other",
    ]
    summary_zh: str = Field(min_length=1, max_length=240)
    summary_en: str = Field(min_length=1, max_length=240)
    sentiment: Literal["positive", "neutral", "negative"]
    confidence: float = Field(ge=0.0, le=1.0)
    tags: List[str] = Field(default_factory=list, max_length=8)
    source_url: HttpUrl


class ProcessedItem(BaseModel):
    """A complete processed record / 完整处理结果记录."""

    raw: RawItem
    insight: AIInsight
    run_date: dt.date
    status: Literal["processed", "failed"] = "processed"
    error: str = ""


class TaskStatus(BaseModel):
    """Task execution status row / 任务状态记录."""

    task_name: str
    status: Literal["running", "success", "failed"]
    started_at: dt.datetime
    finished_at: dt.datetime | None = None
    message: str = ""
