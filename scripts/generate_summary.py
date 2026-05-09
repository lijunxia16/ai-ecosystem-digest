import argparse
import datetime as dt
from pathlib import Path
from typing import List


ROOT = Path(__file__).resolve().parents[1]
DAILY_DIR = ROOT / "reports" / "daily"
WEEKLY_DIR = ROOT / "reports" / "weekly"
MONTHLY_DIR = ROOT / "reports" / "monthly"

CST = dt.timezone(dt.timedelta(hours=8))


def parse_date_from_name(path: Path) -> dt.date:
    return dt.datetime.strptime(path.stem, "%Y-%m-%d").date()


def collect_files(start: dt.date, end: dt.date) -> List[Path]:
    files = []
    for p in DAILY_DIR.glob("*.md"):
        try:
            d = parse_date_from_name(p)
        except ValueError:
            continue
        if start <= d <= end:
            files.append(p)
    return sorted(files)


def build_summary(period_name: str, start: dt.date, end: dt.date, files: List[Path]) -> str:
    zh_files = "\n".join(f"- {p.name}" for p in files) if files else "- （无日报）"
    en_files = "\n".join(f"- {p.name}" for p in files) if files else "- (no daily reports)"
    return f"""# {period_name} AI Summary | AI 汇总

## 中文版
- 时间范围：{start.isoformat()} ~ {end.isoformat()}
- 覆盖日报数量：{len(files)}

### 包含的日报文件
{zh_files}

### 建议人工补充
- 本周/本月关键里程碑
- 最具影响力仓库与资讯变化
- 下阶段关注方向

---

## English Version
- Time window: {start.isoformat()} ~ {end.isoformat()}
- Number of daily reports included: {len(files)}

### Included Daily Files
{en_files}

### Suggested Manual Highlights
- Major milestones in this week/month
- Most impactful repo/news movement
- Focus items for next period
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["weekly", "monthly"], required=True)
    args = parser.parse_args()

    today = dt.datetime.now(CST).date()

    if args.mode == "weekly":
        end = today
        start = today - dt.timedelta(days=6)
        period_name = f"Weekly ({start.isoformat()} to {end.isoformat()})"
        out_dir = WEEKLY_DIR
        out_file = out_dir / f"{end.isoformat()}.md"
    else:
        first_day = today.replace(day=1)
        end = today
        start = first_day
        period_name = f"Monthly ({start.isoformat()} to {end.isoformat()})"
        out_dir = MONTHLY_DIR
        out_file = out_dir / f"{today.strftime('%Y-%m')}.md"

    files = collect_files(start, end)
    content = build_summary(period_name, start, end, files)

    out_dir.mkdir(parents=True, exist_ok=True)
    out_file.write_text(content, encoding="utf-8")
    print(out_file.as_posix())


if __name__ == "__main__":
    main()
