from __future__ import annotations

import json
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _validate(data: dict, schema_name: str) -> None:
    schema = load_json(SCHEMAS / schema_name)
    Draft202012Validator(schema).validate(data)


def validate_release(data: dict) -> None:
    _validate(data, "release.schema.json")


def validate_claims(data: dict) -> None:
    _validate(data, "claims.schema.json")


def validate_results_snapshot(data: dict) -> None:
    _validate(data, "results_snapshot.schema.json")
