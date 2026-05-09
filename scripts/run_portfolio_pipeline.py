from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path

import yaml

from pipeline.db import SQLiteStore
from pipeline.llm_processor import LLMProcessor
from pipeline.models import ProcessedItem, TaskStatus
from pipeline.notifier import Notifier
from pipeline.scraper import Scraper

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "sources.yaml"
CST = dt.timezone(dt.timedelta(hours=8))


def load_config() -> dict:
    with CONFIG.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default="", help="Run date in YYYY-MM-DD (CST)")
    args = parser.parse_args()
    run_date = dt.datetime.strptime(args.date, "%Y-%m-%d").date() if args.date else dt.datetime.now(CST).date()

    cfg = load_config()
    gh_pat = os.getenv("GH_PAT", "").strip() or os.getenv("GITHUB_TOKEN", "").strip()
    primary_llm = os.getenv("OPENAI_API_KEY", "").strip()
    backup_llm = os.getenv("BACKUP_OPENAI_API_KEY", "").strip()

    store = SQLiteStore(ROOT / "data" / "portfolio_pipeline.db")
    task_id = store.add_task_status(
        TaskStatus(task_name="portfolio_daily_pipeline", status="running", started_at=dt.datetime.now(dt.timezone.utc))
    )

    try:
        scraper = Scraper(github_token=gh_pat, timeout_sec=20, max_retries=3)
        llm = LLMProcessor(primary_api_key=primary_llm, backup_api_key=backup_llm)
        notifier = Notifier(ROOT / "digests")

        repos = cfg.get("ai_cli_repos", []) + [cfg.get("openclaw_primary_repo", "")] + cfg.get("openclaw_compare_repos", [])
        repos = [r for r in repos if r]

        raw_items = scraper.fetch_repo_activity_24h(repos)
        raw_items.extend(scraper.fetch_hn_ai_top30())

        processed: list[ProcessedItem] = []
        for raw in raw_items:
            # Dedupe by source + external id + run_date to prevent duplicate pushes.
            # 按 source + external_id + 日期去重，避免重复发布。
            if store.has_processed(raw.source, raw.external_id, run_date):
                continue
            insight = llm.process(raw)
            processed.append(ProcessedItem(raw=raw, insight=insight, run_date=run_date, status="processed"))

        store.save_many(processed)
        outputs = notifier.write_daily_files(run_date, processed)

        meta = {
            "date": run_date.isoformat(),
            "digest_dir": str(outputs["dir"].as_posix()),
            "issue_title": f"AI Portfolio Daily Report - {run_date.isoformat()}",
            "issue_body_file": str(outputs["issue_body"].as_posix()),
            "new_records": len(processed),
        }
        (ROOT / "digests" / "latest_daily_meta.json").write_text(
            json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        store.update_task_status(task_id, "success", f"processed={len(processed)}")
        print(json.dumps(meta, ensure_ascii=False))
    except Exception as ex:
        store.update_task_status(task_id, "failed", str(ex))
        raise


if __name__ == "__main__":
    main()
