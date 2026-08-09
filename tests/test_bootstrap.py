import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_required_baseline_files_exist():
    required = [
        "release.json",
        "claims.json",
        "paper/Rad_REKTOROVA_v7_SYNC.docx",
        "paper/PAPER_EVIDENCE_SYNC.md",
        "web/izvori.html",
    ]
    assert all((ROOT / path).exists() for path in required)


def test_baseline_release_identity():
    release = json.loads((ROOT / "release.json").read_text(encoding="utf-8"))
    assert release["release_id"] == "UNIZG-SZ-2017-2025-sync1"
    assert release["dataset_version"] == "v7"
    assert release["web_companion_version"] == "v8-sync"
    assert release["lock_cycle"] == 5
    assert release["tests_passed"] == 237
