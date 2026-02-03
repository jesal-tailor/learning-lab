from pathlib import Path
from learning_lab.summarise_csv import summarise_csv


def test_summarise_csv_creates_expected_summary(tmp_path: Path):
    csv_content = """name,age,score
Jesal,39,88
Poonam,40,91
Riaan,0,100
Amiah,0,99
"""
    csv_file = tmp_path / "sample.csv"
    csv_file.write_text(csv_content, encoding="utf-8")

    report = summarise_csv(csv_file)

    assert "Rows: 4" in report
    assert "Columns: 3" in report
    assert "age:" in report
    assert "score:" in report
    assert "Preview" in report
