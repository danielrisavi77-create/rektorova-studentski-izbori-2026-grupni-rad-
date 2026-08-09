from pathlib import Path
from scripts.research_io import load_json, validate_claims

ROOT = Path(__file__).resolve().parents[1]


def test_claims_schema_accepts_baseline():
    validate_claims(load_json(ROOT / "claims.json"))


def test_claim_ids_are_unique():
    claims = load_json(ROOT / "claims.json")["claims"]
    ids = [claim["id"] for claim in claims]
    assert len(ids) == len(set(ids))


def test_exploratory_claims_remain_exploratory():
    claims = {c["id"]: c for c in load_json(ROOT / "claims.json")["claims"]}
    assert claims["CLAIM-H4P-VALID"]["class"] == "exploratory"
    assert claims["CLAIM-H4B-GRADIENT"]["class"] == "exploratory"
