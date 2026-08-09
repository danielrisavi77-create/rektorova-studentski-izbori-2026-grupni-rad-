from pathlib import Path
from scripts.research_io import load_json, validate_release

ROOT = Path(__file__).resolve().parents[1]


def test_release_schema_accepts_baseline():
    validate_release(load_json(ROOT / "release.json"))


def test_release_sampling_funnel_is_exact():
    release = load_json(ROOT / "release.json")
    u = release["universe"]
    assert u == {
        "components": 36,
        "cycles": 5,
        "theoretical_component_cycles": 180,
        "not_in_panel": 2,
        "panel_rows": 178,
        "missing_turnout_denominator": 3,
        "complete_turnout_rows": 175,
    }
