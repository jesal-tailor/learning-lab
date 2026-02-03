import os
import csv
import sys
from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()


def is_number(value: str) -> bool:
    try:
        float(value)
        return True
    except ValueError:
        return False


def summarise_csv(csv_path: Path) -> str:
    if not csv_path.exists():
        raise FileNotFoundError(f"File not found: {csv_path}")

    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        return "CSV is empty.\n"

    headers = rows[0].keys()
    numeric_cols = [h for h in headers if all(is_number(r[h]) for r in rows if r[h] != "")]

    lines = []
    lines.append(f"File: {csv_path.name}")
    lines.append(f"Rows: {len(rows)}")
    lines.append(f"Columns: {len(list(headers))}")
    lines.append("")

    if numeric_cols:
        lines.append("Numeric column summary (min / max / avg):")
        for col in numeric_cols:
            nums = [float(r[col]) for r in rows if r[col] != ""]
            mn = min(nums)
            mx = max(nums)
            avg = sum(nums) / len(nums)
            lines.append(f"- {col}: {mn:.2f} / {mx:.2f} / {avg:.2f}")
    else:
        lines.append("No fully-numeric columns found.")

    lines.append("")
    lines.append("Preview (first 5 rows):")
    for i, r in enumerate(rows[:5], start=1):
        lines.append(f"{i}. {r}")

    return "\n".join(lines) + "\n"


def main():
    if len(sys.argv) < 2:
        print("Usage: python summarise_csv.py <path-to-csv>")
        sys.exit(1)

    csv_path = Path(sys.argv[1]).expanduser().resolve()
    report = summarise_csv(csv_path)

    out_path = csv_path.with_suffix(".report.txt")
    out_path.write_text(report, encoding="utf-8")

    logging.info("\n" + report)
    logging.info("Report written to: %s", out_path)


if __name__ == "__main__":
    main()
