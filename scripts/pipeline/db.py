from __future__ import annotations

import datetime as dt
import json
import sqlite3
from pathlib import Path
from typing import Iterable, List

from .models import ProcessedItem, TaskStatus


class SQLiteStore:
    """
    SQLite store for dedupe + task state.
    SQLite 存储层：用于去重与任务状态管理。
    """

    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_tables()

    def _conn(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _init_tables(self) -> None:
        with self._conn() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS processed_items (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  source TEXT NOT NULL,
                  external_id TEXT NOT NULL,
                  run_date TEXT NOT NULL,
                  payload_json TEXT NOT NULL,
                  status TEXT NOT NULL,
                  created_at TEXT NOT NULL,
                  UNIQUE(source, external_id, run_date)
                );
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS task_runs (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  task_name TEXT NOT NULL,
                  status TEXT NOT NULL,
                  started_at TEXT NOT NULL,
                  finished_at TEXT,
                  message TEXT
                );
                """
            )
            conn.commit()

    def has_processed(self, source: str, external_id: str, run_date: dt.date) -> bool:
        with self._conn() as conn:
            row = conn.execute(
                """
                SELECT 1
                FROM processed_items
                WHERE source=? AND external_id=? AND run_date=?
                LIMIT 1
                """,
                (source, external_id, run_date.isoformat()),
            ).fetchone()
            return row is not None

    def save_processed(self, item: ProcessedItem) -> None:
        with self._conn() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO processed_items
                (source, external_id, run_date, payload_json, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    item.raw.source,
                    item.raw.external_id,
                    item.run_date.isoformat(),
                    json.dumps(item.model_dump(mode="json"), ensure_ascii=False),
                    item.status,
                    dt.datetime.now(dt.timezone.utc).isoformat(),
                ),
            )
            conn.commit()

    def save_many(self, items: Iterable[ProcessedItem]) -> None:
        for item in items:
            self.save_processed(item)

    def list_by_date(self, run_date: dt.date) -> List[ProcessedItem]:
        rows: List[ProcessedItem] = []
        with self._conn() as conn:
            for payload_json, in conn.execute(
                "SELECT payload_json FROM processed_items WHERE run_date=? ORDER BY id ASC",
                (run_date.isoformat(),),
            ).fetchall():
                rows.append(ProcessedItem.model_validate_json(payload_json))
        return rows

    def add_task_status(self, status: TaskStatus) -> int:
        with self._conn() as conn:
            cursor = conn.execute(
                """
                INSERT INTO task_runs (task_name, status, started_at, finished_at, message)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    status.task_name,
                    status.status,
                    status.started_at.isoformat(),
                    status.finished_at.isoformat() if status.finished_at else None,
                    status.message,
                ),
            )
            conn.commit()
            return int(cursor.lastrowid)

    def update_task_status(self, task_id: int, status: str, message: str = "") -> None:
        with self._conn() as conn:
            conn.execute(
                """
                UPDATE task_runs
                SET status=?, finished_at=?, message=?
                WHERE id=?
                """,
                (status, dt.datetime.now(dt.timezone.utc).isoformat(), message, task_id),
            )
            conn.commit()
