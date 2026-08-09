# Reproducible Research System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Pretvoriti repozitorij `rektorova-studentski-izbori-2026 (grupni rad)` u fail-closed reproducibilni istraživački sustav u kojem zaključani podatci i rezultati hrane rad i web, a CI automatski zaustavlja drift.

**Architecture:** Sustav ima jasno odvojene slojeve: zaključani podatci → analitički snapshot → registar tvrdnji i release metadata → manifest → paper/web prikazi → jedinstveni validator → GitHub Actions. `release.json`, `claims.json` i `analysis/results_snapshot.json` su strojni izvori istine; Word i HTML ostaju downstream prikazi i ne smiju postati autoritativni izvori zaključanih brojki.

**Tech Stack:** Python 3.11, pytest, jsonschema, python-docx, BeautifulSoup4, standardna biblioteka (`json`, `hashlib`, `pathlib`, `zipfile`, `csv`, `re`), statični HTML/CSS/JS i GitHub Actions.

## Global Constraints

- Projektni naslov je `rektorova-studentski-izbori-2026 (grupni rad)`.
- Kanonski GitHub repo je `danielrisavi77-create/rektorova-studentski-izbori-2026-grupni-rad-`.
- Zaključani podatci se ne mijenjaju ručno; svaka stvarna promjena podataka zahtijeva novi lock cycle i novi release.
- `release.json` je jedini autoritativni izvor release-level metapodataka.
- `claims.json` je jedini autoritativni Claim-to-Evidence registar.
- `analysis/results_snapshot.json` je jedini strojni izvor zaključanih brojčanih rezultata analiza.
- Sampling funnel mora svugdje biti identičan: `180 → 178 → 175`.
- H2 mora svugdje razlikovati `34` statusna zapisa od `11/34` numerički verificiranih nazivnika za mjesta.
- H4' i H4b moraju ostati označeni kao eksplorativni.
- H3 se ne smije prikazivati kao potvrđena hipoteza.
- H2 se ne smije prikazivati kao potpuno potvrđena kauzalna hipoteza.
- Validator je read-only i vraća non-zero exit code pri drifta; ne popravlja podatke automatski.
- Službeni dokumenti se ne redistribuiraju ako prava distribucije nisu jasna; tada se čuvaju metapodatci, poveznice, arhivski trag i dokazna napomena.
- `MANIFEST.json` ne smije imati samoreferencijalnu hash petlju; manifest ne hashira samoga sebe niti Git commit SHA koji se mijenja kao posljedica manifest commita.
- Trenutni baseline release ostaje `UNIZG-SZ-2017-2025-sync1`, dataset version `v7`, web companion `v8-sync`, lock cycle `5`, službeni test count `237`.
- Sinkronizacijski testovi moraju se voditi odvojeno od povijesnog službenog testnog paketa sve dok formalno ne postanu njegov dio.

---

## Repository File Map

Datoteke koje plan stvara ili standardizira:

```text
README.md                              javni ulaz u projekt i reproducibility upute
CITATION.cff                           strojno čitljiv način citiranja
LICENSE                                licenca za kod i dokumentaciju
DATA_LICENSE.md                        status/licenca podataka i izvornih dokumenata
MANIFEST.json                          generirani SHA-256 manifest zaključanih artefakata
release.json                           kanonski release metadata
claims.json                            kanonski Claim-to-Evidence registar
requirements.txt                       fiksirani runtime/test dependencies

paper/Rad_REKTOROVA_v7_SYNC.docx       glavni urednički artefakt rada
paper/PAPER_EVIDENCE_SYNC.md           opis Paper ↔ Evidence sloja
paper/sync_map.json                    sigurne paper-anchor definicije

web/izvori.html                        glavni dokazni web companion
web/data/release.json                  build-kopija release metadata za web
web/data/claims.json                   build-kopija claim registra za web
web/data/results_snapshot.json         build-kopija rezultata za web

data/final/panel_wide.csv              zaključani široki panel
data/final/panel_long.csv              zaključani dugi panel
data/final/sources.csv                 strukturirani registry izvora
data/README.md                          definicija zaključavanja i strukture podataka

evidence/provenance.json               provenijencija izvora
evidence/DECISIONS.md                  decision log

analysis/results_snapshot.json          zaključani brojčani izlaz analiza
analysis/scripts/                       analitičke skripte korištene za snapshot
analysis/replication/provjera.sps       PSPP sintaksa za neovisnu računsku reprodukciju
analysis/replication/usporedba.csv      usporedba 10/10 ključnih vrijednosti

schemas/release.schema.json             JSON Schema za release
schemas/claims.schema.json              JSON Schema za claims
schemas/results_snapshot.schema.json    minimalni schema guard za snapshot

scripts/research_io.py                  zajednički loaderi i schema validation
scripts/build_manifest.py               deterministički manifest builder
scripts/build_web_data.py               kopira/generira web data layer
scripts/sync_paper.py                    sigurno verificira/ažurira označena Word polja
scripts/validate_sync.py                 jedinstveni fail-closed validator
scripts/package_release.py               gradi release ZIP i checksums

tests/test_release_schema.py            release schema tests
tests/test_claims_schema.py             claims schema i semantic tests
tests/test_dataset_integrity.py          panel i sampling funnel tests
tests/test_results_snapshot.py           snapshot key/value guards
tests/test_manifest.py                   hash/manifest tests
tests/test_web_sync.py                   HTML ↔ kanonski artefakti tests
tests/test_paper_sync.py                 DOCX ↔ kanonski artefakti tests
tests/test_validate_sync.py              end-to-end validator tests
tests/test_package_release.py            release package tests

.github/workflows/reproducibility.yml    CI za PR/push/manual run
```

---

### Task 1: Bootstrap repository and import the approved synchronized baseline

**Files:**
- Create: `README.md`
- Create: `requirements.txt`
- Create: `release.json`
- Create: `claims.json`
- Create: `paper/PAPER_EVIDENCE_SYNC.md`
- Create: `web/izvori.html`
- Create binary: `paper/Rad_REKTOROVA_v7_SYNC.docx`
- Create: `tests/test_bootstrap.py`

**Interfaces:**
- Consumes: approved local bundle `PAPER_EVIDENCE_SYNC1_BUNDLE.zip` containing `Rad_REKTOROVA_v7_SYNC.docx`, `izvori_v8_SYNC.html`, `release.json`, `claims.json`, `PAPER_EVIDENCE_SYNC.md`.
- Produces: repository baseline whose canonical metadata exactly match release `UNIZG-SZ-2017-2025-sync1`.

- [ ] **Step 1: Write the failing bootstrap test**

```python
# tests/test_bootstrap.py
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
```

- [ ] **Step 2: Run the test and verify RED**

Run: `python -m pytest tests/test_bootstrap.py -v`

Expected: FAIL because baseline files do not yet all exist in the repository.

- [ ] **Step 3: Import the five text artefacts and the DOCX binary from the approved bundle**

Use the exact current synchronized artefacts; do not regenerate their scientific content during bootstrap. Store the DOCX as binary Git content and the other files as UTF-8.

Create `requirements.txt`:

```text
beautifulsoup4==4.13.4
jsonschema==4.25.0
python-docx==1.2.0
pytest==8.4.1
```

Create an initial `README.md` that identifies the project, states `FINAL_DATA_LOCK`, and explicitly says the repository is in reproducibility-system bootstrap until all canonical analytical artefacts pass CI.

- [ ] **Step 4: Run bootstrap tests and verify GREEN**

Run: `python -m pytest tests/test_bootstrap.py -v`

Expected: `2 passed`.

- [ ] **Step 5: Commit**

```bash
git add README.md requirements.txt release.json claims.json paper/ web/ tests/test_bootstrap.py
git commit -m "chore: import synchronized research baseline"
```

---

### Task 2: Add machine-readable schemas and canonical loaders

**Files:**
- Create: `schemas/release.schema.json`
- Create: `schemas/claims.schema.json`
- Create: `schemas/results_snapshot.schema.json`
- Create: `scripts/research_io.py`
- Create: `tests/test_release_schema.py`
- Create: `tests/test_claims_schema.py`

**Interfaces:**
- Consumes: `release.json`, `claims.json`, future `analysis/results_snapshot.json`.
- Produces: `load_json(path: Path) -> dict`, `validate_release(data: dict) -> None`, `validate_claims(data: dict) -> None`, `validate_results_snapshot(data: dict) -> None`.

- [ ] **Step 1: Write failing schema tests**

```python
# tests/test_release_schema.py
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
```

```python
# tests/test_claims_schema.py
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
```

- [ ] **Step 2: Run tests and verify RED**

Run: `python -m pytest tests/test_release_schema.py tests/test_claims_schema.py -v`

Expected: FAIL because `scripts.research_io` and schemas do not exist.

- [ ] **Step 3: Implement strict schemas and loaders**

`release.schema.json` must require: `schema_version`, `release_id`, `release_date`, `dataset_version`, `web_companion_version`, `data_lock_status`, `lock_cycle`, `tests_passed`, `universe`, `source_registry`, `h2_seat_coverage`, `canonical_artifacts`, `integrity`.

`claims.schema.json` must require each claim to have at minimum: `id`, `hypothesis`, `class`, `title`, `claim`, `status`, `paper`, `web_anchor`; `id` pattern must be `^CLAIM-[A-Z0-9'-]+` and `class` must be one of `confirmatory`, `confirmatory-partial`, `exploratory`.

`scripts/research_io.py`:

```python
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
```

- [ ] **Step 4: Run tests and verify GREEN**

Run: `python -m pytest tests/test_release_schema.py tests/test_claims_schema.py -v`

Expected: all tests PASS.

- [ ] **Step 5: Commit**

```bash
git add schemas/ scripts/research_io.py tests/test_release_schema.py tests/test_claims_schema.py
git commit -m "feat: validate canonical research metadata"
```

---

### Task 3: Import and lock the canonical analytical artefacts

**Files:**
- Create/import: `data/final/panel_wide.csv`
- Create/import: `data/final/panel_long.csv`
- Create/import: `data/final/sources.csv`
- Create/import: `analysis/results_snapshot.json`
- Create/import: `evidence/provenance.json`
- Create/import: `evidence/DECISIONS.md`
- Create/import: `analysis/replication/provjera.sps`
- Create/import: `analysis/replication/usporedba.csv`
- Create: `data/README.md`
- Create: `tests/test_dataset_integrity.py`
- Create: `tests/test_results_snapshot.py`

**Interfaces:**
- Consumes: original final artefacts from the research project. Search the user's available files/library by the exact target names and by the release identifiers `UNIZG-SZ-2017-2025`, `panel_wide`, `results_snapshot`, `provenance`, `DECISIONS`, `provjera.sps`, `usporedba.csv`.
- Produces: complete canonical analytical tree referenced by `release.json`.

**Fail-closed rule:** if an original artefact cannot be found, do not synthesize it from the Word or HTML. Stop this task and report the exact missing path; Tasks 4–12 must not claim full reproducibility until the canonical artefact is supplied.

- [ ] **Step 1: Write failing dataset integrity tests**

```python
# tests/test_dataset_integrity.py
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def rows(path: str):
    with (ROOT / path).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def test_wide_panel_has_178_rows():
    assert len(rows("data/final/panel_wide.csv")) == 178


def test_complete_turnout_count_is_175():
    data = rows("data/final/panel_wide.csv")
    turnout_candidates = ["turnout", "turnout_pct", "izlaznost", "izlaznost_pct"]
    field = next(name for name in turnout_candidates if name in data[0])
    complete = [r for r in data if str(r[field]).strip() not in {"", "NA", "NaN", "nan"}]
    assert len(complete) == 175
```

```python
# tests/test_results_snapshot.py
from pathlib import Path
from scripts.research_io import load_json, validate_results_snapshot

ROOT = Path(__file__).resolve().parents[1]


def test_results_snapshot_is_schema_valid():
    validate_results_snapshot(load_json(ROOT / "analysis/results_snapshot.json"))


def test_replication_comparison_has_ten_matching_values():
    text = (ROOT / "analysis/replication/usporedba.csv").read_text(encoding="utf-8-sig")
    lines = [line for line in text.splitlines() if line.strip()]
    assert len(lines) >= 11
```

- [ ] **Step 2: Run tests and verify RED**

Run: `python -m pytest tests/test_dataset_integrity.py tests/test_results_snapshot.py -v`

Expected: FAIL because canonical analytical artefacts are not yet imported.

- [ ] **Step 3: Import original artefacts without scientific transformation**

Copy the original bytes/text into the exact target paths. Update only path metadata in `release.json` so all paths become repo-relative and resolve from repository root, for example:

```json
"canonical_artifacts": {
  "panel_wide": "data/final/panel_wide.csv",
  "panel_long": "data/final/panel_long.csv",
  "results_snapshot": "analysis/results_snapshot.json",
  "manifest": "MANIFEST.json",
  "provenance": "evidence/provenance.json",
  "claims": "claims.json",
  "release": "release.json",
  "decisions": "evidence/DECISIONS.md",
  "pspp_syntax": "analysis/replication/provjera.sps",
  "pspp_comparison": "analysis/replication/usporedba.csv"
}
```

`data/README.md` must state that the data are `FINAL_DATA_LOCK`, lock cycle `5`, and that missing/unavailable official values remain missing rather than imputed.

- [ ] **Step 4: Adapt column-name-only test selectors to the real locked schema**

Do not rename analytical columns merely to satisfy tests. The tests may be adjusted to the actual existing column names, but expected row counts and scientific values remain fixed.

- [ ] **Step 5: Run tests and verify GREEN**

Run: `python -m pytest tests/test_dataset_integrity.py tests/test_results_snapshot.py tests/test_release_schema.py -v`

Expected: all PASS.

- [ ] **Step 6: Commit**

```bash
git add data/ analysis/ evidence/ release.json tests/test_dataset_integrity.py tests/test_results_snapshot.py
git commit -m "data: import final locked analytical artefacts"
```

---

### Task 4: Bind every claim to a machine result and enforce scientific semantics

**Files:**
- Modify: `claims.json`
- Modify: `schemas/claims.schema.json`
- Create: `scripts/claim_validation.py`
- Modify: `tests/test_claims_schema.py`
- Create: `tests/test_claim_semantics.py`

**Interfaces:**
- Consumes: parsed `claims.json`, parsed `analysis/results_snapshot.json`.
- Produces: `validate_claim_bindings(claims: dict, snapshot: dict) -> list[str]` returning an empty list on success and human-readable errors otherwise.

- [ ] **Step 1: Write failing semantic tests**

```python
# tests/test_claim_semantics.py
from pathlib import Path
from scripts.research_io import load_json
from scripts.claim_validation import validate_claim_bindings

ROOT = Path(__file__).resolve().parents[1]


def test_all_claims_bind_to_snapshot():
    claims = load_json(ROOT / "claims.json")
    snapshot = load_json(ROOT / "analysis/results_snapshot.json")
    assert validate_claim_bindings(claims, snapshot) == []


def test_h2_coverage_is_explicit():
    claims = {c["id"]: c for c in load_json(ROOT / "claims.json")["claims"]}
    h2 = claims["CLAIM-H2-CANDIDATES"]
    assert h2["seat_status_records_n"] == 34
    assert h2["seat_numeric_verified_n"] == 11
    assert h2["ratio_n"] == 11
    assert h2["class"] == "confirmatory-partial"


def test_h3_is_not_confirmed():
    claims = {c["id"]: c for c in load_json(ROOT / "claims.json")["claims"]}
    assert "potvr" not in claims["CLAIM-H3-FIELD"]["status"].lower()
```

- [ ] **Step 2: Run and verify RED**

Run: `python -m pytest tests/test_claim_semantics.py -v`

Expected: FAIL until every claim has a stable `result_key` or an explicitly documented non-numeric procedural binding.

- [ ] **Step 3: Normalize claim bindings**

For numerical claims add exact `result_key` values that resolve in the imported snapshot. For procedural H4, use a structured `evidence_binding` pointing to the paired-comparison count object in snapshot rather than inventing a scalar estimate. Preserve all currently approved estimates: H1 `-4.45`, H2 candidate count `+0.37`, H2 ratio `+10.16`, H3 `+8.74`, H4' `+1.25`, H4b `-0.47`, and cycle effects as stored in the original snapshot.

Implement a dotted-path resolver:

```python
def resolve_path(data: dict, dotted: str):
    current = data
    for part in dotted.split("."):
        current = current[part]
    return current
```

`validate_claim_bindings` must report missing paths, release ID mismatch, illegal class/status combinations, H2 coverage drift, and exploratory-label drift.

- [ ] **Step 4: Run and verify GREEN**

Run: `python -m pytest tests/test_claims_schema.py tests/test_claim_semantics.py -v`

Expected: all PASS.

- [ ] **Step 5: Commit**

```bash
git add claims.json schemas/claims.schema.json scripts/claim_validation.py tests/test_claims_schema.py tests/test_claim_semantics.py
git commit -m "feat: bind research claims to canonical results"
```

---

### Task 5: Build deterministic SHA-256 manifest and lock enforcement

**Files:**
- Create: `scripts/build_manifest.py`
- Create: `tests/test_manifest.py`
- Generate: `MANIFEST.json`

**Interfaces:**
- Consumes: explicit allowlist of canonical and generated artefacts.
- Produces: `sha256_file(path: Path) -> str`, `build_manifest(root: Path, release_id: str) -> dict`, deterministic `MANIFEST.json`.

- [ ] **Step 1: Write failing manifest tests**

```python
# tests/test_manifest.py
import json
from pathlib import Path
from scripts.build_manifest import build_manifest

ROOT = Path(__file__).resolve().parents[1]


def test_manifest_is_deterministic():
    a = build_manifest(ROOT, "UNIZG-SZ-2017-2025-sync1")
    b = build_manifest(ROOT, "UNIZG-SZ-2017-2025-sync1")
    assert a == b


def test_manifest_does_not_hash_itself():
    manifest = build_manifest(ROOT, "UNIZG-SZ-2017-2025-sync1")
    paths = {item["path"] for item in manifest["artifacts"]}
    assert "MANIFEST.json" not in paths


def test_manifest_contains_locked_panel():
    manifest = build_manifest(ROOT, "UNIZG-SZ-2017-2025-sync1")
    paths = {item["path"] for item in manifest["artifacts"]}
    assert "data/final/panel_wide.csv" in paths
```

- [ ] **Step 2: Run and verify RED**

Run: `python -m pytest tests/test_manifest.py -v`

Expected: FAIL because builder does not exist.

- [ ] **Step 3: Implement deterministic builder**

Every artifact entry must contain exactly:

```json
{
  "path": "data/final/panel_wide.csv",
  "sha256": "<64 lowercase hex chars>",
  "size_bytes": 123,
  "role": "canonical-data",
  "release_id": "UNIZG-SZ-2017-2025-sync1",
  "kind": "canonical"
}
```

Sort entries lexicographically by path. Hash file bytes, not normalized text. Exclude `.git/`, caches, `MANIFEST.json`, temporary Office files, release ZIPs and validation reports.

- [ ] **Step 4: Generate manifest and compare the locked panel prefix**

Run: `python scripts/build_manifest.py --write`

Expected: `MANIFEST.json` created; full SHA-256 of `data/final/panel_wide.csv` begins with release baseline prefix `13f8b3f1e50b9711`. If it does not, stop: the imported panel is not the locked panel described by the approved release.

- [ ] **Step 5: Run tests and verify GREEN**

Run: `python -m pytest tests/test_manifest.py -v`

Expected: all PASS.

- [ ] **Step 6: Commit**

```bash
git add scripts/build_manifest.py tests/test_manifest.py MANIFEST.json
git commit -m "feat: add deterministic research manifest"
```

---

### Task 6: Convert the web companion to consume canonical build data

**Files:**
- Create: `scripts/build_web_data.py`
- Create: `web/data/release.json`
- Create: `web/data/claims.json`
- Create: `web/data/results_snapshot.json`
- Modify: `web/izvori.html`
- Create: `tests/test_web_sync.py`

**Interfaces:**
- Consumes: root `release.json`, `claims.json`, `analysis/results_snapshot.json`.
- Produces: deterministic copies under `web/data/`; HTML anchors and UI values that are validated against canonical JSON.

- [ ] **Step 1: Write failing web synchronization tests**

```python
# tests/test_web_sync.py
import json
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]


def test_web_has_anchor_for_every_claim():
    claims = json.loads((ROOT / "claims.json").read_text(encoding="utf-8"))["claims"]
    soup = BeautifulSoup((ROOT / "web/izvori.html").read_text(encoding="utf-8"), "html.parser")
    ids = {node.get("id") for node in soup.find_all(id=True)}
    missing = [c["web_anchor"].lstrip("#") for c in claims if c["web_anchor"].lstrip("#") not in ids]
    assert missing == []


def test_web_data_equals_canonical_json():
    for name, source in {
        "release.json": "release.json",
        "claims.json": "claims.json",
        "results_snapshot.json": "analysis/results_snapshot.json",
    }.items():
        assert json.loads((ROOT / "web/data" / name).read_text(encoding="utf-8")) == json.loads((ROOT / source).read_text(encoding="utf-8"))
```

- [ ] **Step 2: Run and verify RED**

Run: `python -m pytest tests/test_web_sync.py -v`

Expected: FAIL because `web/data/` build layer is absent and/or some anchors differ.

- [ ] **Step 3: Implement `build_web_data.py`**

The script must copy canonical JSON through parse-and-canonical-dump rather than byte-copy, using UTF-8 and stable indentation. It must never calculate new scientific results.

```python
def write_canonical_json(source: Path, target: Path) -> None:
    data = json.loads(source.read_text(encoding="utf-8"))
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
```

- [ ] **Step 4: Align HTML claim anchors and add a data provenance declaration**

Ensure each card uses the exact anchor from `claims.json`: `#claim-h1`, `#claim-h2`, `#claim-h3`, `#claim-h4`, `#claim-h4p`, `#claim-h4b`, and the H5 anchor stored in the registry. Add a visible note in the reproducibility section: “Zaključane brojke dolaze iz kanonskog `results_snapshot.json`; web ih ne računa ponovno.”

Do not remove the existing accessibility features, search/filter UI, evidence matrix, component dossiers, graph interactions, or bibliography.

- [ ] **Step 5: Build and test**

Run:

```bash
python scripts/build_web_data.py
python -m pytest tests/test_web_sync.py -v
```

Expected: all PASS.

- [ ] **Step 6: Commit**

```bash
git add scripts/build_web_data.py web/ tests/test_web_sync.py
git commit -m "feat: bind evidence website to canonical research data"
```

---

### Task 7: Add safe Word synchronization and paper drift detection

**Files:**
- Create: `paper/sync_map.json`
- Create: `scripts/sync_paper.py`
- Create: `tests/fixtures/minimal_paper.docx`
- Create: `tests/test_paper_sync.py`
- Modify binary only when safe: `paper/Rad_REKTOROVA_v7_SYNC.docx`

**Interfaces:**
- Consumes: DOCX, `release.json`, `claims.json`, `paper/sync_map.json`.
- Produces: `inspect_paper(docx_path: Path) -> list[str]`, `sync_paper(source: Path, target: Path) -> None`.

**Safety boundary:** automated sync may only replace uniquely anchored synchronization fields. It must not rewrite tables, figures, bibliography, body paragraphs or styles globally.

- [ ] **Step 1: Write failing DOCX tests**

```python
# tests/test_paper_sync.py
from pathlib import Path
from scripts.sync_paper import inspect_paper

ROOT = Path(__file__).resolve().parents[1]


def test_real_paper_has_no_sync_drift():
    errors = inspect_paper(ROOT / "paper/Rad_REKTOROVA_v7_SYNC.docx")
    assert errors == []
```

Add fixture tests proving that changing `178` to `179`, removing `FINAL_DATA_LOCK`, or relabeling H4' from exploratory to confirmatory creates a deterministic validation error.

- [ ] **Step 2: Run and verify RED**

Run: `python -m pytest tests/test_paper_sync.py -v`

Expected: FAIL because sync inspector does not exist.

- [ ] **Step 3: Define exact sync anchors**

`paper/sync_map.json` stores each unique human-readable prefix plus expected source path, for example:

```json
{
  "release_id": {"prefix": "Research release:", "source": "release.release_id"},
  "lock_cycle": {"prefix": "Lock cycle:", "source": "release.lock_cycle"},
  "sampling_funnel": {"prefix": "Analitički slijed:", "literal": "180 → 178 → 175"},
  "h2_coverage": {"prefix": "H2 pokrivenost mjesta:", "literal": "34 statusna zapisa; 11/34 numerički verificirano"}
}
```

Use actual unique labels already present in the synchronized Word where possible. If an anchor is absent, add one controlled paragraph in the reproducibility appendix rather than altering scientific body text.

- [ ] **Step 4: Implement inspection first, then safe update mode**

`inspect_paper` reads all paragraph and table-cell text and checks exact anchored values. `sync_paper` must copy the DOCX to a new target, update only the text following configured anchors, reopen the target, and verify that paragraph count, table count, section count and embedded media count are unchanged.

If uniqueness is violated or structural counts change, raise `PaperSyncError` and leave the source untouched.

- [ ] **Step 5: Run paper tests and visual smoke check**

Run: `python -m pytest tests/test_paper_sync.py -v`

Expected: all PASS.

Then render the synchronized DOCX using the available document-rendering workflow and visually inspect at minimum: title page, methodology sampling funnel, H2 results table/paragraph, reproducibility appendix, Claim-to-Evidence appendix and final page. No pagination-breaking edit is accepted without review.

- [ ] **Step 6: Commit**

```bash
git add paper/sync_map.json scripts/sync_paper.py tests/test_paper_sync.py tests/fixtures/minimal_paper.docx paper/Rad_REKTOROVA_v7_SYNC.docx
git commit -m "feat: add safe paper synchronization guards"
```

---

### Task 8: Implement the unified fail-closed synchronization validator

**Files:**
- Create: `scripts/validate_sync.py`
- Create: `tests/test_validate_sync.py`
- Preserve/import: prior `validate_paper_evidence_sync.py` under `archive/sync1/` for audit history if useful; do not use it as the new canonical validator.

**Interfaces:**
- Consumes: all canonical metadata, snapshot, manifest, DOCX and HTML.
- Produces: `run_validation(root: Path) -> ValidationReport`; CLI exit `0` only when every required check passes.

- [ ] **Step 1: Write failing end-to-end validator tests**

```python
# tests/test_validate_sync.py
from pathlib import Path
from scripts.validate_sync import run_validation

ROOT = Path(__file__).resolve().parents[1]


def test_repository_validation_passes():
    report = run_validation(ROOT)
    assert report.failed == 0
    assert report.passed >= 15


def test_validation_report_has_named_checks():
    report = run_validation(ROOT)
    names = {check.name for check in report.checks}
    assert {
        "release-schema",
        "claims-schema",
        "claim-bindings",
        "dataset-funnel",
        "h2-coverage",
        "manifest-hashes",
        "paper-sync",
        "web-sync",
    }.issubset(names)
```

- [ ] **Step 2: Run and verify RED**

Run: `python -m pytest tests/test_validate_sync.py -v`

Expected: FAIL because validator does not exist.

- [ ] **Step 3: Implement typed validation report**

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class CheckResult:
    name: str
    passed: bool
    detail: str

@dataclass(frozen=True)
class ValidationReport:
    checks: tuple[CheckResult, ...]

    @property
    def passed(self) -> int:
        return sum(c.passed for c in self.checks)

    @property
    def failed(self) -> int:
        return sum(not c.passed for c in self.checks)
```

Implement at least the 15 checks from the approved design: release schema, claims schema, unique claim IDs, claim→snapshot bindings, paper→release, paper→claims, web→release, web→claims, sampling funnel, H2 34/11 semantics, H3 non-confirmed status, H4'/H4b exploratory status, test-count/lock-cycle consistency, manifest hashes, inner web anchors/canonical artefact existence.

- [ ] **Step 4: Add CLI behavior**

Run: `python scripts/validate_sync.py`

Expected output pattern:

```text
PASS release-schema — valid
PASS claims-schema — valid
...
SUMMARY: <N> passed, 0 failed
```

Exit code must be `1` when any required check fails.

- [ ] **Step 5: Run full validator tests**

Run: `python -m pytest tests/test_validate_sync.py -v && python scripts/validate_sync.py`

Expected: all PASS and exit code `0`.

- [ ] **Step 6: Commit**

```bash
git add scripts/validate_sync.py tests/test_validate_sync.py archive/
git commit -m "feat: add fail-closed paper evidence validator"
```

---

### Task 9: Add GitHub Actions reproducibility CI

**Files:**
- Create: `.github/workflows/reproducibility.yml`
- Create: `tests/test_workflow_contract.py`

**Interfaces:**
- Consumes: repository on PR/push/manual dispatch.
- Produces: a required CI job named `reproducibility` that installs dependencies, runs the full test suite, rebuilds deterministic derived data, verifies no drift, validates manifest and uploads a validation report artifact.

- [ ] **Step 1: Write failing workflow contract test**

```python
# tests/test_workflow_contract.py
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_workflow_runs_required_commands():
    text = (ROOT / ".github/workflows/reproducibility.yml").read_text(encoding="utf-8")
    for required in [
        "python -m pytest",
        "python scripts/build_web_data.py",
        "python scripts/build_manifest.py --check",
        "python scripts/validate_sync.py",
    ]:
        assert required in text
```

- [ ] **Step 2: Run and verify RED**

Run: `python -m pytest tests/test_workflow_contract.py -v`

Expected: FAIL because workflow is absent.

- [ ] **Step 3: Create CI workflow**

Use `ubuntu-latest`, Python `3.11`, dependency caching, `pip install -r requirements.txt`, and these ordered gates:

```text
1. pytest
2. build_web_data.py
3. git diff --exit-code web/data
4. build_manifest.py --check
5. validate_sync.py
6. package validation report artifact
```

Trigger on `pull_request`, `push` to `main`, and `workflow_dispatch`.

- [ ] **Step 4: Run workflow contract and local CI equivalent**

Run:

```bash
python -m pytest -q
python scripts/build_web_data.py
git diff --exit-code -- web/data
python scripts/build_manifest.py --check
python scripts/validate_sync.py
```

Expected: all commands exit `0`.

- [ ] **Step 5: Commit**

```bash
git add .github/workflows/reproducibility.yml tests/test_workflow_contract.py
git commit -m "ci: enforce research reproducibility gates"
```

---

### Task 10: Add citation, licensing and complete project documentation

**Files:**
- Modify: `README.md`
- Create: `CITATION.cff`
- Create: `LICENSE`
- Create: `DATA_LICENSE.md`
- Create: `docs/REPRODUCIBILITY.md`
- Create: `docs/CLAIM_TO_EVIDENCE.md`
- Create: `tests/test_documentation_contract.py`

**Interfaces:**
- Consumes: authors/title from the approved paper, release metadata and repository structure.
- Produces: a third party can understand what is public, what is locked, what can be redistributed, how to reproduce validation, and how to cite the work.

- [ ] **Step 1: Write failing documentation contract test**

```python
# tests/test_documentation_contract.py
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_readme_explains_reproduction_path():
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    for phrase in [
        "180 → 178 → 175",
        "FINAL_DATA_LOCK",
        "python scripts/validate_sync.py",
        "34 statusna zapisa",
        "11/34",
    ]:
        assert phrase in text


def test_citation_file_exists():
    assert (ROOT / "CITATION.cff").exists()
```

- [ ] **Step 2: Run and verify RED**

Run: `python -m pytest tests/test_documentation_contract.py -v`

Expected: FAIL until documentation is complete.

- [ ] **Step 3: Write README as the research entry point**

README sections must be: project title and authors, research question, key findings with scientific-status labels, 180→178→175 funnel, H2 34/11 note, repository map, one-command validation, reproducibility boundaries, data/source rights, release/version status, citation instructions.

Do not claim that a third party can recreate unavailable official documents. Reproducibility refers to the locked research package and calculations from the archived/registered evidence available in the project.

- [ ] **Step 4: Add licensing files**

Use a permissive software/documentation license only for material authored by the project team. `DATA_LICENSE.md` must explicitly separate: project-authored metadata/code, transformed/derived datasets where publication is permitted, and third-party official source documents whose copyright remains with the original institutions.

Do not put an unverified blanket open-data license over third-party official documents.

- [ ] **Step 5: Add citation metadata**

`CITATION.cff` must use the paper's full nine-author list and the paper title “Determinante izlaznosti na sveučilišnim studentskim izborima: analiza sastavnica Sveučilišta u Zagrebu, 2017. do 2025.” Release version must resolve from current baseline `UNIZG-SZ-2017-2025-sync1`; DOI is omitted until an actual DOI exists.

- [ ] **Step 6: Run and verify GREEN**

Run: `python -m pytest tests/test_documentation_contract.py -v`

Expected: all PASS.

- [ ] **Step 7: Commit**

```bash
git add README.md CITATION.cff LICENSE DATA_LICENSE.md docs/ tests/test_documentation_contract.py
git commit -m "docs: document reproducibility citation and licensing"
```

---

### Task 11: Build deterministic release packaging

**Files:**
- Create: `scripts/package_release.py`
- Create: `tests/test_package_release.py`
- Generate locally/CI only: `dist/UNIZG-SZ-2017-2025-sync1.zip`
- Generate locally/CI only: `dist/SHA256SUMS.txt`
- Modify: `.gitignore`

**Interfaces:**
- Consumes: validated repository and `MANIFEST.json`.
- Produces: a release ZIP containing exactly the intended public/reproducibility artefacts plus `SHA256SUMS.txt`.

- [ ] **Step 1: Write failing package tests**

```python
# tests/test_package_release.py
from pathlib import Path
from zipfile import ZipFile
from scripts.package_release import package_release

ROOT = Path(__file__).resolve().parents[1]


def test_release_zip_contains_core_artifacts(tmp_path):
    archive = package_release(ROOT, tmp_path)
    with ZipFile(archive) as zf:
        names = set(zf.namelist())
    for required in [
        "release.json",
        "claims.json",
        "MANIFEST.json",
        "paper/Rad_REKTOROVA_v7_SYNC.docx",
        "web/izvori.html",
        "analysis/results_snapshot.json",
        "data/final/panel_wide.csv",
    ]:
        assert required in names
```

- [ ] **Step 2: Run and verify RED**

Run: `python -m pytest tests/test_package_release.py -v`

Expected: FAIL because packaging code is absent.

- [ ] **Step 3: Implement packaging only after validation passes**

`package_release` must call or import `run_validation`; if `failed > 0`, raise and do not create a ZIP. ZIP entries must use stable relative paths; package must exclude `.git`, caches, test fixtures, temporary Office files and private/nonredistributable source documents.

- [ ] **Step 4: Generate package and checksums**

Run: `python scripts/package_release.py`

Expected: `dist/UNIZG-SZ-2017-2025-sync1.zip` and `dist/SHA256SUMS.txt`.

- [ ] **Step 5: Run tests and verify GREEN**

Run: `python -m pytest tests/test_package_release.py -v`

Expected: all PASS.

- [ ] **Step 6: Commit code, not generated distribution files**

```bash
git add scripts/package_release.py tests/test_package_release.py .gitignore
git commit -m "feat: add validated research release packaging"
```

---

### Task 12: Final end-to-end verification and baseline release readiness

**Files:**
- Modify if needed: `release.json` only for non-scientific repository path corrections already justified by the migration
- Regenerate: `MANIFEST.json`
- Create: `docs/BASELINE_VERIFICATION.md`

**Interfaces:**
- Consumes: complete repository from Tasks 1–11.
- Produces: evidence that the migrated reproducibility system is internally consistent and ready for the first GitHub release/tag without changing the locked analysis.

- [ ] **Step 1: Run the complete local gate from a clean checkout**

Run:

```bash
python -m pip install -r requirements.txt
python -m pytest -q
python scripts/build_web_data.py
python scripts/build_manifest.py --check
python scripts/validate_sync.py
python scripts/package_release.py
```

Expected: every command exits `0`; no tracked-file drift after builders.

- [ ] **Step 2: Verify scientific invariants explicitly**

Run a small Python assertion script or pytest selection confirming:

```text
release_id = UNIZG-SZ-2017-2025-sync1
lock_cycle = 5
official tests = 237
sampling funnel = 180 → 178 → 175
H2 = 34 status records / 11 numeric verified
H1 estimate = -4.45 pp
H2 candidate effect = +0.37 pp
H2 ratio effect = +10.16 pp
H3 estimate = +8.74 pp and not confirmed
H4 original = not confirmed
H4' = +1.25 pp and exploratory
H4b = -0.47 pp and exploratory
```

The exact H5 cycle values must be read from and compared to `analysis/results_snapshot.json`; do not hard-code values not present in that canonical artefact.

- [ ] **Step 3: Verify the Word visually after all repository-level changes**

Render the DOCX and inspect: title page, contents, list of tables/figures, methodology, main results, Table 8/9/10, limitations, Appendix D, Appendix F renamed as neovisna računska/softverska reprodukcija where approved, Appendix G Claim-to-Evidence, and final page. Record the observed page count and any benign pagination change in `docs/BASELINE_VERIFICATION.md`.

- [ ] **Step 4: Verify web behavior**

Open `web/izvori.html` and verify keyboard navigation, theme control, search/filter, component dossier dialog, evidence matrix, four interactive graphs, claim anchors, downloads/reproducibility section, and no broken internal links.

- [ ] **Step 5: Check GitHub Actions status**

Push the final branch/commit and confirm the `reproducibility` workflow is green. If GitHub branch protection is available, configure the `reproducibility` job as a required check before merge to `main`.

- [ ] **Step 6: Write baseline verification record**

`docs/BASELINE_VERIFICATION.md` must include commit SHA, release ID, manifest panel SHA-256, total pytest count, validator pass/fail count, CI run status, package SHA-256, and a statement that the migration changed no locked scientific result.

- [ ] **Step 7: Final commit**

```bash
git add MANIFEST.json docs/BASELINE_VERIFICATION.md release.json
git commit -m "chore: verify reproducible research baseline"
```

- [ ] **Step 8: Release readiness decision**

Only after the final commit is green may the repository be tagged/released as the first reproducibility-system baseline. A future Zenodo/OSF deposit and DOI must point to that immutable release, not to a moving `main` branch.

---

## Definition of Done

Implementation is complete only when all of the following are true:

1. Original locked analytical artefacts exist under the documented canonical paths.
2. `release.json`, `claims.json` and `analysis/results_snapshot.json` validate against schemas.
3. Every claim has a valid machine/evidence binding.
4. The panel hash matches the approved `13f8b3f1e50b9711…` baseline.
5. `MANIFEST.json` is deterministic and all hashes pass.
6. Sampling funnel `180 → 178 → 175` is identical in release, tests, paper and web.
7. H2 `34` versus `11/34` is unambiguous everywhere.
8. H3 is not represented as confirmed; H4' and H4b remain exploratory.
9. Paper inspection returns zero drift errors and preserves document structure.
10. Web claim anchors and canonical web-data copies pass.
11. `python scripts/validate_sync.py` exits `0`.
12. `python -m pytest -q` is fully green.
13. GitHub Actions `reproducibility` job is green.
14. Release packaging refuses to run on invalid state and succeeds on the validated state.
15. README, citation and licensing accurately describe what can and cannot be reproduced or redistributed.
16. `docs/BASELINE_VERIFICATION.md` records the final immutable verification evidence.

## Self-review result

- **Spec coverage:** all approved architecture sections are mapped to Tasks 1–12: canonical artefacts, 180→178→175, H2 34/11, Claim-to-Evidence, provenance, manifest, paper/web sync, validator, TDD, CI, licensing/citation and release packaging.
- **Placeholder scan:** no `TBD`, `TODO`, “implement later” or unspecified test steps are permitted in this plan.
- **Type consistency:** shared interfaces are fixed as `load_json`, schema validators, `validate_claim_bindings`, `build_manifest`, `inspect_paper`, `sync_paper`, `run_validation` and `package_release` and are referenced consistently by later tasks.
- **Scope:** this is one coherent reproducibility pipeline; tasks are independently reviewable but converge on a single fail-closed release gate.
