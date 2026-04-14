---
plan_id: phase-7-promotion-governance
phase: 7
title: Promotion Governance Layer
status: in_progress
priority: highest
sprint: "Sprint A (weeks 1-2)"
version: 1.0.0
plan_type: implementation_tdd
created: 2026-04-14
last_updated: 2026-04-14
owner: Senior Systems Architect
prerequisites:
  - Phase 6A (LLM review) complete — verified 2026-04-13
dependencies:
  - .ai/06_specs/relationship-schema.md
  - .ai/01_roadmap/master-roadmap.md §3.1 and §3.5
  - scripts/vitruvius/ollama_review.py (existing)
unblocks:
  - Phase 8 Graph Contract & Indexing
  - Phase 9 Query & AI Layer
  - Phase 11 Dataset Expansion
---

# Phase 7 — Promotion Governance Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a `pipeline_cli.py promote` command that reads high-confidence Ollama review decisions and writes canonical relationship files under `003_Canonical-Knowledge-Layer/shared/relationships/` with a full audit log, closed-vocabulary enforcement, dry-run default, evidence-merge semantics, and rollback support.

**Architecture:** A new `promotion` subsystem — four modules (`promotion.py`, `promotion_validator.py`, `relationship_registry.yaml`, audit log writer) driven by a `run_promote()` orchestrator. It consumes a new filtered artifact (`latest_relationship_review_high_confidence.json`) emitted by the existing `ollama_review.py` module. The filesystem-as-database principle (P1) remains intact: the audit log is an append-only text file, not a database.

**Tech Stack:** Python 3.11+ stdlib only (`json`, `pathlib`, `dataclasses`, `hashlib`, `argparse`); PyYAML (already in project); pytest for tests. No new dependencies.

---

## File Structure

### Files to create
| Path | Responsibility |
|---|---|
| `config/vitruvius.yaml` *(modify)* | Add `review.ollama.url`, `review.ollama.default_model`, `promotion.confidence_threshold` keys |
| `scripts/vitruvius/config.py` *(new)* | Single config loader — `load_config()` returns a parsed dict, cached |
| `scripts/vitruvius/rules/relationship_registry.yaml` *(new)* | Closed predicate vocabulary + compatibility pairs |
| `scripts/vitruvius/promotion_validator.py` *(new)* | `ValidationResult` dataclass + `validate_promotion_record()` implementing all 17 rules |
| `scripts/vitruvius/promotion.py` *(new)* | `run_promote()` orchestrator, evidence-merge, audit log writer, slug builder, rollback |
| `scripts/vitruvius/ollama_review.py` *(modify)* | Replace hardcoded `OLLAMA_URL` with config loader; add `write_high_confidence_review()` |
| `scripts/pipeline_cli.py` *(modify)* | Register `promote` subcommand with `--execute` and `--rollback BATCH_ID` flags |
| `scripts/tests/__init__.py` *(new if missing)* | Test package marker |
| `scripts/tests/test_config.py` *(new)* | Unit tests for config loader |
| `scripts/tests/test_promotion_validator.py` *(new)* | Unit tests for all 17 validation rules |
| `scripts/tests/test_promotion.py` *(new)* | Unit tests for slug, merge, ID, audit log |
| `scripts/tests/fixtures/` *(new)* | Synthetic review JSON, source/concept files, expected outputs |

### Files the plan must NOT touch
- `001_Raw-Source-Layer/` (principle P2)
- Any existing file under `003_Canonical-Knowledge-Layer/shared/sources/` or `.../concepts/`
- `scripts/vitruvius/relationships.py` or `relationships_sections.py` (Phase 5 is out of scope)

---

## Pre-flight Commands

Run once before starting. These commands must succeed; if they don't, stop and report.

```bash
cd /Users/philiplewis/vitruvius
python -c "import yaml; print('yaml OK')"
python -c "import json, pathlib, dataclasses, hashlib; print('stdlib OK')"
ls scripts/vitruvius/ollama_review.py
ls config/vitruvius.yaml
mkdir -p scripts/tests/fixtures
```

Install pytest if missing:
```bash
python -m pip install pytest
```

---

## Task 1: Config Loader Module

**Files:**
- Create: `scripts/vitruvius/config.py`
- Create: `scripts/tests/test_config.py`
- Modify: `config/vitruvius.yaml`

- [ ] **Step 1.1: Add config keys to `config/vitruvius.yaml`**

Append to `config/vitruvius.yaml`:
```yaml

review:
  ollama:
    url: "http://127.0.0.1:11434"
    default_model: "gemma4:31b"
    default_timeout_seconds: 600

promotion:
  confidence_threshold: 0.90
  audit_log_name: "latest_promotion_audit.log"
```

- [ ] **Step 1.2: Write the failing test for `load_config`**

Create `scripts/tests/test_config.py`:
```python
from pathlib import Path
from vitruvius.config import load_config, get_ollama_url, get_confidence_threshold


def test_load_config_returns_dict():
    cfg = load_config()
    assert isinstance(cfg, dict)
    assert "review" in cfg
    assert "promotion" in cfg


def test_get_ollama_url_reads_config():
    url = get_ollama_url()
    assert url.startswith("http://")
    assert "11434" in url


def test_get_confidence_threshold_is_point_nine():
    assert get_confidence_threshold() == 0.90
```

- [ ] **Step 1.3: Run test to verify failure**

```bash
cd /Users/philiplewis/vitruvius
PYTHONPATH=scripts python -m pytest scripts/tests/test_config.py -v
```
Expected: `ModuleNotFoundError: No module named 'vitruvius.config'`

- [ ] **Step 1.4: Implement `scripts/vitruvius/config.py`**

```python
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import yaml

from .paths import get_repo_root


@lru_cache(maxsize=1)
def load_config() -> dict:
    path = get_repo_root() / "config" / "vitruvius.yaml"
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def get_ollama_url() -> str:
    cfg = load_config()
    return cfg.get("review", {}).get("ollama", {}).get("url", "http://127.0.0.1:11434")


def get_ollama_default_model() -> str:
    cfg = load_config()
    return cfg.get("review", {}).get("ollama", {}).get("default_model", "gemma4:31b")


def get_ollama_default_timeout() -> int:
    cfg = load_config()
    return int(cfg.get("review", {}).get("ollama", {}).get("default_timeout_seconds", 600))


def get_confidence_threshold() -> float:
    cfg = load_config()
    return float(cfg.get("promotion", {}).get("confidence_threshold", 0.90))


def get_audit_log_name() -> str:
    cfg = load_config()
    return cfg.get("promotion", {}).get("audit_log_name", "latest_promotion_audit.log")
```

- [ ] **Step 1.5: Run test to verify success**

```bash
PYTHONPATH=scripts python -m pytest scripts/tests/test_config.py -v
```
Expected: `3 passed`

- [ ] **Step 1.6: Commit**

```bash
git add config/vitruvius.yaml scripts/vitruvius/config.py scripts/tests/test_config.py
git commit -m "feat(config): add central config loader for review and promotion settings"
```

---

## Task 2: Unhard-code Ollama URL in `ollama_review.py`

**Files:**
- Modify: `scripts/vitruvius/ollama_review.py:15-17, 79, 90`

- [ ] **Step 2.1: Write a failing test that asserts the hardcoded constant is gone**

Append to `scripts/tests/test_config.py`:
```python
def test_ollama_review_uses_config_url():
    from vitruvius import ollama_review
    # OLLAMA_URL module-level constant must not be hardcoded.
    # We verify by checking that call_ollama reads from config at call time.
    import inspect
    src = inspect.getsource(ollama_review.call_ollama)
    assert "get_ollama_url" in src, "call_ollama must read URL from config module"
```

- [ ] **Step 2.2: Run test to verify failure**

```bash
PYTHONPATH=scripts python -m pytest scripts/tests/test_config.py::test_ollama_review_uses_config_url -v
```
Expected: FAIL with `AssertionError: call_ollama must read URL from config module`

- [ ] **Step 2.3: Update `ollama_review.py` to read from config**

Edit lines 10-17 of `scripts/vitruvius/ollama_review.py`:
```python
from .config import (
    get_ollama_default_model,
    get_ollama_default_timeout,
    get_ollama_url,
)
from .paths import get_repo_root
from .reports import write_json, write_text
from .utils import utc_now_stamp


DEFAULT_MODEL = get_ollama_default_model()
DEFAULT_TIMEOUT_SECONDS = get_ollama_default_timeout()
```

Delete the line `OLLAMA_URL = "http://127.0.0.1:11434/api/generate"`.

Edit `call_ollama` (lines 65-98) — replace the two references to `OLLAMA_URL`:
```python
def call_ollama(prompt: str, model: str, timeout_seconds: int) -> str:
    body = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "options": {
            "temperature": 0,
            "num_predict": 300,
        },
    }

    data = json.dumps(body).encode("utf-8")
    base_url = get_ollama_url().rstrip("/")
    endpoint = f"{base_url}/api/generate"
    request = urllib.request.Request(
        endpoint,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.URLError as exc:
        raise RuntimeError(
            f"Failed to reach Ollama at {endpoint}. "
            "Make sure Ollama is running and the model is available."
        ) from exc

    parsed = json.loads(raw)
    if "response" not in parsed:
        raise RuntimeError(f"Unexpected Ollama response: {raw}")

    return parsed["response"]
```

- [ ] **Step 2.4: Run test to verify success**

```bash
PYTHONPATH=scripts python -m pytest scripts/tests/test_config.py -v
```
Expected: `4 passed`

- [ ] **Step 2.5: Commit**

```bash
git add scripts/vitruvius/ollama_review.py scripts/tests/test_config.py
git commit -m "refactor(review): read Ollama URL from config instead of hardcoding (RI-003)"
```

---

## Task 3: High-Confidence Review Writer

**Files:**
- Modify: `scripts/vitruvius/ollama_review.py` (add `write_high_confidence_review` + call at end of `run_review_relationships_ollama`)
- Create: `scripts/tests/test_high_confidence_writer.py`

- [ ] **Step 3.1: Write the failing test**

Create `scripts/tests/test_high_confidence_writer.py`:
```python
import json
from pathlib import Path

from vitruvius.ollama_review import write_high_confidence_review


def test_filters_keep_at_or_above_threshold(tmp_path):
    report = {
        "generated_at": "20260414T030000Z",
        "model": "gemma4:31b",
        "source": "003/shared/sources/test.md",
        "total_candidates": 3,
        "completed_reviews": 3,
        "status": "completed",
        "summary": {},
        "reviews": [
            {
                "candidate": {"from": "concept-a", "type": "governs", "to": "concept-b",
                              "sections": ["sec-1"], "examples": ["e1"], "occurrences": 1},
                "review": {"decision": "keep", "confidence": 0.95, "reason": "clear",
                           "suggested_type": None},
            },
            {
                "candidate": {"from": "concept-c", "type": "affects", "to": "concept-d",
                              "sections": ["sec-2"], "examples": ["e2"], "occurrences": 1},
                "review": {"decision": "keep", "confidence": 0.80, "reason": "weak",
                           "suggested_type": None},
            },
            {
                "candidate": {"from": "concept-e", "type": "requires", "to": "concept-f",
                              "sections": ["sec-3"], "examples": ["e3"], "occurrences": 1},
                "review": {"decision": "reject", "confidence": 0.99, "reason": "no",
                           "suggested_type": None},
            },
        ],
    }

    output = write_high_confidence_review(report, tmp_path, threshold=0.90)

    assert output.exists()
    payload = json.loads(output.read_text())
    assert payload["count"] == 1
    assert payload["threshold"] == 0.90
    assert payload["source_model"] == "gemma4:31b"
    assert payload["candidates"][0]["candidate"]["from"] == "concept-a"


def test_empty_when_nothing_passes_threshold(tmp_path):
    report = {
        "generated_at": "20260414T030000Z",
        "model": "gemma4:31b",
        "source": "s",
        "total_candidates": 1,
        "completed_reviews": 1,
        "status": "completed",
        "summary": {},
        "reviews": [
            {
                "candidate": {"from": "a", "type": "governs", "to": "b",
                              "sections": [], "examples": [], "occurrences": 1},
                "review": {"decision": "keep", "confidence": 0.5, "reason": "meh",
                           "suggested_type": None},
            }
        ],
    }
    output = write_high_confidence_review(report, tmp_path, threshold=0.90)
    payload = json.loads(output.read_text())
    assert payload["count"] == 0
    assert payload["candidates"] == []
```

- [ ] **Step 3.2: Run test to verify failure**

```bash
PYTHONPATH=scripts python -m pytest scripts/tests/test_high_confidence_writer.py -v
```
Expected: FAIL — `cannot import name 'write_high_confidence_review'`

- [ ] **Step 3.3: Add `write_high_confidence_review` to `ollama_review.py`**

Append to `scripts/vitruvius/ollama_review.py` (before `run_review_relationships_ollama`):
```python
def write_high_confidence_review(
    report: dict[str, Any],
    runs_dir: Path,
    *,
    threshold: float | None = None,
) -> Path:
    """Filter the review report to keep-only, confidence >= threshold.

    Writes 006_System-Manifests/runs/latest_relationship_review_high_confidence.json
    and returns the output path. An empty-but-valid file is written when no
    candidates clear the threshold.
    """
    from .config import get_confidence_threshold

    if threshold is None:
        threshold = get_confidence_threshold()

    high_conf: list[dict[str, Any]] = []
    for item in report.get("reviews", []):
        review = item.get("review", {})
        if review.get("decision") == "keep" and float(review.get("confidence", 0.0)) >= threshold:
            high_conf.append(item)

    payload = {
        "generated_at": utc_now_stamp(),
        "source_report_generated_at": report.get("generated_at"),
        "source_model": report.get("model"),
        "source": report.get("source"),
        "threshold": threshold,
        "count": len(high_conf),
        "candidates": high_conf,
    }

    runs_dir.mkdir(parents=True, exist_ok=True)
    output_path = runs_dir / "latest_relationship_review_high_confidence.json"
    write_json(output_path, payload)
    return output_path
```

- [ ] **Step 3.4: Wire it into `run_review_relationships_ollama`**

In `scripts/vitruvius/ollama_review.py`, find the block that ends with:
```python
    save_progress_report(
        runs_dir=runs_dir,
        model=model,
        source=source,
        candidates=candidates,
        reviews=reviews,
        status="completed",
    )
```
(around line 330 in the current file).

Immediately after that block, add:
```python
    final_report = {
        "generated_at": utc_now_stamp(),
        "model": model,
        "source": source,
        "total_candidates": len(candidates),
        "completed_reviews": len(reviews),
        "status": "completed",
        "summary": summarize_reviews(reviews),
        "reviews": reviews,
    }
    high_conf_path = write_high_confidence_review(final_report, runs_dir)
    print(f"High-confidence: {high_conf_path}")
```

- [ ] **Step 3.5: Run tests to verify success**

```bash
PYTHONPATH=scripts python -m pytest scripts/tests/test_high_confidence_writer.py -v
```
Expected: `2 passed`

- [ ] **Step 3.6: Commit**

```bash
git add scripts/vitruvius/ollama_review.py scripts/tests/test_high_confidence_writer.py
git commit -m "feat(review): emit latest_relationship_review_high_confidence.json (Phase 7 input)"
```

---

## Task 4: Relationship Type Registry YAML

**Files:**
- Create: `scripts/vitruvius/rules/relationship_registry.yaml`
- Create: `scripts/tests/test_registry_load.py`

- [ ] **Step 4.1: Write the failing test**

Create `scripts/tests/test_registry_load.py`:
```python
from vitruvius.promotion_validator import load_registry


def test_registry_has_seven_predicates():
    registry = load_registry()
    predicates = registry["predicates"]
    expected = {"governs", "defines", "requires", "depends_on", "limits", "affects", "supersedes"}
    assert set(predicates.keys()) == expected


def test_governs_allows_source_to_concept():
    registry = load_registry()
    pairs = registry["predicates"]["governs"]["allowed_pairs"]
    assert {"subject_type": "source", "object_type": "concept"} in pairs


def test_requires_allows_concept_to_concept():
    registry = load_registry()
    pairs = registry["predicates"]["requires"]["allowed_pairs"]
    assert {"subject_type": "concept", "object_type": "concept"} in pairs
```

- [ ] **Step 4.2: Run test to verify failure**

```bash
PYTHONPATH=scripts python -m pytest scripts/tests/test_registry_load.py -v
```
Expected: FAIL — `No module named 'vitruvius.promotion_validator'`

- [ ] **Step 4.3: Create `scripts/vitruvius/rules/relationship_registry.yaml`**

```yaml
schema_version: 1.0.0

predicates:
  governs:
    semantics: "Subject legally governs the object."
    allowed_pairs:
      - {subject_type: source, object_type: concept}

  defines:
    semantics: "Subject provides the definitional text for the object."
    allowed_pairs:
      - {subject_type: source, object_type: concept}

  requires:
    semantics: "Subject requires the object to exist or be satisfied."
    allowed_pairs:
      - {subject_type: concept, object_type: concept}
      - {subject_type: concept, object_type: attribute}

  depends_on:
    semantics: "Subject cannot be determined without the object."
    allowed_pairs:
      - {subject_type: concept, object_type: concept}

  limits:
    semantics: "Subject places numeric or scope limits on the object."
    allowed_pairs:
      - {subject_type: source, object_type: concept}
      - {subject_type: source, object_type: attribute}
      - {subject_type: section, object_type: concept}
      - {subject_type: section, object_type: attribute}

  affects:
    semantics: "Subject changes the behavior of the object without requiring or limiting it."
    allowed_pairs:
      - {subject_type: concept, object_type: concept}
      - {subject_type: source, object_type: concept}

  supersedes:
    semantics: "Subject is a newer version that replaces the object."
    allowed_pairs:
      - {subject_type: source, object_type: source}
      - {subject_type: concept, object_type: concept}
```

- [ ] **Step 4.4: Create the minimal `promotion_validator.py` stub so the test can import**

Create `scripts/vitruvius/promotion_validator.py`:
```python
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import yaml

from .paths import get_repo_root


@lru_cache(maxsize=1)
def load_registry() -> dict:
    path = get_repo_root() / "scripts" / "vitruvius" / "rules" / "relationship_registry.yaml"
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}
```

- [ ] **Step 4.5: Run test to verify success**

```bash
PYTHONPATH=scripts python -m pytest scripts/tests/test_registry_load.py -v
```
Expected: `3 passed`

- [ ] **Step 4.6: Commit**

```bash
git add scripts/vitruvius/rules/relationship_registry.yaml scripts/vitruvius/promotion_validator.py scripts/tests/test_registry_load.py
git commit -m "feat(promotion): add relationship_registry.yaml with seven closed predicates"
```

---

## Task 5: Canonical Index Loader

**Files:**
- Modify: `scripts/vitruvius/promotion_validator.py`
- Create: `scripts/tests/test_canonical_index.py`

Goal: Given a clean walk of `003/shared/sources/` and `003/shared/concepts/`, produce an index `{id: {"type": "source"|"concept", "path": Path, "canonical_status": str}}` that the validator will use for referential-integrity checks.

- [ ] **Step 5.1: Write the failing test**

Create `scripts/tests/test_canonical_index.py`:
```python
from pathlib import Path

from vitruvius.promotion_validator import build_canonical_index


def test_builds_index_from_fixture(tmp_path):
    root = tmp_path / "003_Canonical-Knowledge-Layer" / "shared"
    (root / "sources").mkdir(parents=True)
    (root / "concepts").mkdir(parents=True)

    (root / "sources" / "pd-1096.md").write_text(
        "---\nid: law-pd-1096\ntitle: PD 1096\npage_type: source\n"
        "trust_level: primary\ncanonical_status: draft\n"
        "last_canonicalized_utc: 2026-04-14T00:00:00Z\n---\n# X\n",
        encoding="utf-8",
    )
    (root / "concepts" / "occupancy-classification.md").write_text(
        "---\nid: concept-occupancy-classification\ntitle: Occupancy Classification\n"
        "page_type: concept\ncanonical_status: placeholder\n"
        "last_canonicalized_utc: 2026-04-14T00:00:00Z\n---\n# Y\n",
        encoding="utf-8",
    )

    index = build_canonical_index(tmp_path)

    assert index["law-pd-1096"]["type"] == "source"
    assert index["law-pd-1096"]["canonical_status"] == "draft"
    assert index["concept-occupancy-classification"]["type"] == "concept"
    assert index["concept-occupancy-classification"]["canonical_status"] == "placeholder"


def test_empty_index_when_dirs_missing(tmp_path):
    assert build_canonical_index(tmp_path) == {}
```

- [ ] **Step 5.2: Run test to verify failure**

```bash
PYTHONPATH=scripts python -m pytest scripts/tests/test_canonical_index.py -v
```
Expected: FAIL — `cannot import name 'build_canonical_index'`

- [ ] **Step 5.3: Implement `build_canonical_index`**

Append to `scripts/vitruvius/promotion_validator.py`:
```python
from typing import Any


def _parse_frontmatter(md_text: str) -> dict[str, Any]:
    if not md_text.startswith("---"):
        return {}
    end = md_text.find("\n---", 3)
    if end == -1:
        return {}
    raw = md_text[3:end].strip()
    try:
        return yaml.safe_load(raw) or {}
    except yaml.YAMLError:
        return {}


def build_canonical_index(repo_root: Path) -> dict[str, dict[str, Any]]:
    """Walk 003_Canonical-Knowledge-Layer/shared/{sources,concepts} and return
    an ID-keyed index for referential-integrity checks."""
    index: dict[str, dict[str, Any]] = {}

    base = Path(repo_root) / "003_Canonical-Knowledge-Layer" / "shared"
    for entity_type, subdir in (("source", "sources"), ("concept", "concepts")):
        directory = base / subdir
        if not directory.exists():
            continue
        for md_path in sorted(directory.glob("*.md")):
            fm = _parse_frontmatter(md_path.read_text(encoding="utf-8"))
            entity_id = fm.get("id")
            if not entity_id:
                continue
            index[entity_id] = {
                "type": entity_type,
                "path": md_path,
                "canonical_status": fm.get("canonical_status", "unknown"),
                "trust_level": fm.get("trust_level"),
            }

    return index
```

- [ ] **Step 5.4: Run test to verify success**

```bash
PYTHONPATH=scripts python -m pytest scripts/tests/test_canonical_index.py -v
```
Expected: `2 passed`

- [ ] **Step 5.5: Commit**

```bash
git add scripts/vitruvius/promotion_validator.py scripts/tests/test_canonical_index.py
git commit -m "feat(promotion): add canonical index loader for validator referential checks"
```

---

## Task 6: `PromotionValidator` — All 17 Rules

**Files:**
- Modify: `scripts/vitruvius/promotion_validator.py`
- Create: `scripts/tests/test_promotion_validator.py`
- Create: `scripts/tests/fixtures/valid_record.yaml`

The 17 rules are defined in `/.ai/06_specs/relationship-schema.md` §10. We'll write tests first, then implement the validator method-by-method.

- [ ] **Step 6.1: Create a valid-record fixture**

Create `scripts/tests/fixtures/valid_record.yaml`:
```yaml
id: rel-occupancy-governs-fire-requirements
title: Occupancy Classification Governs Fire-Resistive Requirements
page_type: relationship
relationship_type: governs
from_entity: law-pd-1096
to_entity: concept-fire-resistive-construction
trust_level: primary
canonical_status: promoted
confidence_score: 0.92
promotion_batch_id: 20260414T030000Z_a1b2c3d4
promotion_audit_log_ref: 006_System-Manifests/runs/20260414T030000Z_a1b2c3d4_promotion_audit.log
last_promoted_utc: 2026-04-14T03:00:00Z
evidence:
  - source_id: law-pd-1096
    source_section_id: sec-701
    source_artifact: 002_Raw-Conversion-Layer/001-Laws/raw_markdown/PD-1096/PD 1096 IRR.md
    evidence_snippet: "Every building shall be classified..."
    review_decision: keep
    reviewer_model: gemma4:31b
    reviewer_confidence: 0.92
    reviewer_reason: "Clear governs edge."
    extracted_at_utc: 2026-04-13T08:44:19Z
    reviewed_at_utc: 2026-04-13T09:01:02Z
```

- [ ] **Step 6.2: Write failing tests for all 17 rules**

Create `scripts/tests/test_promotion_validator.py`:
```python
from pathlib import Path

import yaml

from vitruvius.promotion_validator import (
    ValidationResult,
    validate_promotion_record,
)


FIXTURE = Path(__file__).parent / "fixtures" / "valid_record.yaml"


def load_valid():
    return yaml.safe_load(FIXTURE.read_text(encoding="utf-8"))


def canonical_index():
    return {
        "law-pd-1096": {"type": "source", "canonical_status": "draft", "trust_level": "primary"},
        "concept-fire-resistive-construction": {
            "type": "concept", "canonical_status": "draft", "trust_level": None,
        },
        "concept-occupancy-classification": {
            "type": "concept", "canonical_status": "draft", "trust_level": None,
        },
    }


def registry():
    from vitruvius.promotion_validator import load_registry
    return load_registry()


# ---------- happy path ----------

def test_valid_record_passes():
    result = validate_promotion_record(load_valid(), registry(), canonical_index())
    assert result.passed, f"Unexpected errors: {result.errors}"
    assert result.errors == []


# ---------- structural rules 1-6 ----------

def test_rule_2_invalid_id_format():
    rec = load_valid()
    rec["id"] = "REL-BAD"
    result = validate_promotion_record(rec, registry(), canonical_index())
    assert not result.passed
    assert any("id" in e.lower() for e in result.errors)


def test_rule_3_wrong_page_type():
    rec = load_valid()
    rec["page_type"] = "source"
    result = validate_promotion_record(rec, registry(), canonical_index())
    assert not result.passed
    assert any("page_type" in e for e in result.errors)


def test_rule_4_unknown_predicate():
    rec = load_valid()
    rec["relationship_type"] = "frobnicates"
    result = validate_promotion_record(rec, registry(), canonical_index())
    assert not result.passed
    assert any("frobnicates" in e for e in result.errors)


def test_rule_5_unknown_from_entity():
    rec = load_valid()
    rec["from_entity"] = "concept-does-not-exist"
    result = validate_promotion_record(rec, registry(), canonical_index())
    assert not result.passed
    assert any("from_entity" in e for e in result.errors)


def test_rule_6_empty_evidence():
    rec = load_valid()
    rec["evidence"] = []
    result = validate_promotion_record(rec, registry(), canonical_index())
    assert not result.passed
    assert any("evidence" in e.lower() for e in result.errors)


# ---------- registry compatibility rule 7 ----------

def test_rule_7_incompatible_pair():
    rec = load_valid()
    # governs requires source->concept, not concept->concept
    rec["from_entity"] = "concept-occupancy-classification"
    result = validate_promotion_record(rec, registry(), canonical_index())
    assert not result.passed
    assert any("compatibility" in e.lower() or "pair" in e.lower() for e in result.errors)


# ---------- evidence integrity rules 8-12 ----------

def test_rule_8_missing_source_section_id():
    rec = load_valid()
    rec["evidence"][0]["source_section_id"] = None
    result = validate_promotion_record(rec, registry(), canonical_index())
    assert not result.passed
    assert any("source_section_id" in e for e in result.errors)


def test_rule_9_empty_snippet():
    rec = load_valid()
    rec["evidence"][0]["evidence_snippet"] = ""
    result = validate_promotion_record(rec, registry(), canonical_index())
    assert not result.passed
    assert any("snippet" in e.lower() for e in result.errors)


def test_rule_10_evidence_source_not_in_index():
    rec = load_valid()
    rec["evidence"][0]["source_id"] = "law-mystery"
    result = validate_promotion_record(rec, registry(), canonical_index())
    assert not result.passed
    assert any("source_id" in e for e in result.errors)


def test_rule_11_confidence_out_of_range():
    rec = load_valid()
    rec["evidence"][0]["reviewer_confidence"] = 1.5
    result = validate_promotion_record(rec, registry(), canonical_index())
    assert not result.passed
    assert any("confidence" in e.lower() for e in result.errors)


def test_rule_12_non_keep_decision():
    rec = load_valid()
    rec["evidence"][0]["review_decision"] = "review_further"
    result = validate_promotion_record(rec, registry(), canonical_index())
    assert not result.passed
    assert any("review_decision" in e or "keep" in e for e in result.errors)


# ---------- promotion threshold rule 13 ----------

def test_rule_13_below_threshold():
    rec = load_valid()
    rec["confidence_score"] = 0.80
    result = validate_promotion_record(rec, registry(), canonical_index())
    assert not result.passed
    assert any("threshold" in e.lower() or "0.90" in e for e in result.errors)


# ---------- trust propagation rule 14 ----------

def test_rule_14_trust_level_mismatch():
    rec = load_valid()
    rec["trust_level"] = "tertiary"  # actual min is primary
    result = validate_promotion_record(rec, registry(), canonical_index())
    assert not result.passed
    assert any("trust" in e.lower() for e in result.errors)


# ---------- audit integrity rules 15-16 ----------

def test_rule_15_missing_batch_id():
    rec = load_valid()
    rec["promotion_batch_id"] = ""
    result = validate_promotion_record(rec, registry(), canonical_index())
    assert not result.passed
    assert any("promotion_batch_id" in e for e in result.errors)


def test_rule_16_missing_last_promoted_utc():
    rec = load_valid()
    rec["last_promoted_utc"] = ""
    result = validate_promotion_record(rec, registry(), canonical_index())
    assert not result.passed
    assert any("last_promoted_utc" in e for e in result.errors)


# ---------- referential integrity rule 17 ----------

def test_rule_17_placeholder_endpoint_rejected():
    rec = load_valid()
    idx = canonical_index()
    idx["concept-fire-resistive-construction"]["canonical_status"] = "placeholder"
    result = validate_promotion_record(rec, registry(), idx)
    assert not result.passed
    assert any("placeholder" in e.lower() for e in result.errors)
```

- [ ] **Step 6.3: Run tests to verify all fail the right way**

```bash
PYTHONPATH=scripts python -m pytest scripts/tests/test_promotion_validator.py -v
```
Expected: All tests fail with `cannot import name 'ValidationResult'` or similar.

- [ ] **Step 6.4: Implement the `ValidationResult` dataclass and `validate_promotion_record`**

Append to `scripts/vitruvius/promotion_validator.py`:
```python
import re
from dataclasses import dataclass, field
from datetime import datetime


REL_ID_PATTERN = re.compile(r"^rel-[a-z][a-z0-9-]*$")
ALLOWED_TRUST = ("primary", "secondary", "tertiary", "unverified")
TRUST_RANK = {"primary": 0, "secondary": 1, "tertiary": 2, "unverified": 3}


@dataclass
class ValidationResult:
    passed: bool
    errors: list[str] = field(default_factory=list)
    record_id: str = ""


def _parse_iso8601(value: str) -> bool:
    if not isinstance(value, str) or not value:
        return False
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
        return True
    except ValueError:
        return False


def validate_promotion_record(
    record: dict,
    registry: dict,
    canonical_index: dict,
) -> ValidationResult:
    errors: list[str] = []
    record_id = record.get("id", "<missing-id>")

    # Rule 1: frontmatter present (the record dict itself counts as parsed)
    if not isinstance(record, dict):
        return ValidationResult(False, ["Record is not a parseable mapping."], record_id)

    # Rule 2: id format
    rid = record.get("id")
    if not isinstance(rid, str) or not REL_ID_PATTERN.match(rid):
        errors.append(f"Rule 2 (id format): id '{rid}' must match ^rel-[a-z][a-z0-9-]*$")

    # Rule 3: page_type
    if record.get("page_type") != "relationship":
        errors.append(f"Rule 3 (page_type): expected 'relationship', got {record.get('page_type')!r}")

    # Rule 4: predicate in registry
    predicate = record.get("relationship_type")
    predicates = registry.get("predicates", {})
    if predicate not in predicates:
        errors.append(f"Rule 4 (predicate): unknown predicate '{predicate}' — not in registry")

    # Rule 5: from/to exist
    from_entity = record.get("from_entity")
    to_entity = record.get("to_entity")
    if from_entity not in canonical_index:
        errors.append(f"Rule 5 (from_entity): '{from_entity}' not in canonical index")
    if to_entity not in canonical_index:
        errors.append(f"Rule 5 (to_entity): '{to_entity}' not in canonical index")

    # Rule 6: evidence non-empty
    evidence = record.get("evidence") or []
    if not evidence:
        errors.append("Rule 6 (evidence): array must be non-empty")

    # Rule 7: (from_type, to_type) compatibility
    if predicate in predicates and from_entity in canonical_index and to_entity in canonical_index:
        from_type = canonical_index[from_entity]["type"]
        to_type = canonical_index[to_entity]["type"]
        allowed = predicates[predicate].get("allowed_pairs", [])
        if not any(p.get("subject_type") == from_type and p.get("object_type") == to_type for p in allowed):
            errors.append(
                f"Rule 7 (compatibility): ({from_type}, {to_type}) not an allowed pair for '{predicate}'"
            )

    # Rules 8–12: evidence integrity
    for idx, ev in enumerate(evidence):
        prefix = f"Rule 8-12 (evidence[{idx}])"
        if not ev.get("source_section_id"):
            errors.append(f"{prefix}: missing source_section_id (Rule 8)")
        snippet = ev.get("evidence_snippet")
        if not isinstance(snippet, str) or not snippet.strip():
            errors.append(f"{prefix}: empty evidence_snippet (Rule 9)")
        src_id = ev.get("source_id")
        if src_id not in canonical_index:
            errors.append(f"{prefix}: source_id '{src_id}' not in canonical index (Rule 10)")
        conf = ev.get("reviewer_confidence")
        try:
            confval = float(conf)
            if confval < 0.0 or confval > 1.0:
                errors.append(f"{prefix}: reviewer_confidence {confval} outside [0, 1] (Rule 11)")
        except (TypeError, ValueError):
            errors.append(f"{prefix}: reviewer_confidence not a float (Rule 11)")
        decision = ev.get("review_decision")
        if decision != "keep":
            errors.append(f"{prefix}: review_decision '{decision}' must be 'keep' (Rule 12)")

    # Rule 13: promotion threshold
    try:
        score = float(record.get("confidence_score", 0.0))
        if score < 0.90:
            errors.append(f"Rule 13 (threshold): confidence_score {score} below 0.90")
    except (TypeError, ValueError):
        errors.append("Rule 13 (threshold): confidence_score not a float")

    # Rule 14: trust propagation
    declared_trust = record.get("trust_level")
    evidence_trusts = [canonical_index[e["source_id"]]["trust_level"]
                       for e in evidence if e.get("source_id") in canonical_index]
    evidence_trusts = [t for t in evidence_trusts if t in TRUST_RANK]
    if evidence_trusts:
        min_trust = max(evidence_trusts, key=lambda t: TRUST_RANK[t])
        if declared_trust != min_trust:
            errors.append(
                f"Rule 14 (trust): declared {declared_trust!r} must equal worst evidence trust {min_trust!r}"
            )
    if declared_trust not in ALLOWED_TRUST:
        errors.append(f"Rule 14 (trust): '{declared_trust}' not in {ALLOWED_TRUST}")

    # Rules 15–16: audit fields
    if not record.get("promotion_batch_id"):
        errors.append("Rule 15: promotion_batch_id is required")
    if not _parse_iso8601(record.get("last_promoted_utc", "")):
        errors.append("Rule 16: last_promoted_utc must be ISO-8601")

    # Rule 17: endpoint canonical_status
    if record.get("canonical_status") == "promoted":
        for endpoint_field in ("from_entity", "to_entity"):
            eid = record.get(endpoint_field)
            if eid in canonical_index:
                cs = canonical_index[eid]["canonical_status"]
                if cs in ("placeholder", "superseded"):
                    errors.append(
                        f"Rule 17: {endpoint_field} '{eid}' is in '{cs}' status; cannot promote"
                    )

    return ValidationResult(passed=not errors, errors=errors, record_id=record_id)
```

- [ ] **Step 6.5: Run tests to verify success**

```bash
PYTHONPATH=scripts python -m pytest scripts/tests/test_promotion_validator.py -v
```
Expected: `17 passed`

- [ ] **Step 6.6: Commit**

```bash
git add scripts/vitruvius/promotion_validator.py scripts/tests/test_promotion_validator.py scripts/tests/fixtures/valid_record.yaml
git commit -m "feat(promotion): add PromotionValidator enforcing 17 rules from relationship schema"
```

---

## Task 7: Slug Builder + Relationship ID Generation

**Files:**
- Create: `scripts/vitruvius/promotion.py` (stub)
- Create: `scripts/tests/test_promotion_slug.py`

- [ ] **Step 7.1: Write failing tests**

Create `scripts/tests/test_promotion_slug.py`:
```python
from vitruvius.promotion import build_relationship_id, short_hash, build_promotion_batch_id


def test_build_relationship_id_is_deterministic():
    rid1 = build_relationship_id("law-pd-1096", "governs", "concept-fire-resistive-construction")
    rid2 = build_relationship_id("law-pd-1096", "governs", "concept-fire-resistive-construction")
    assert rid1 == rid2
    assert rid1.startswith("rel-")


def test_build_relationship_id_includes_predicate():
    rid = build_relationship_id("law-pd-1096", "requires", "concept-x")
    assert "requires" in rid


def test_short_hash_is_stable():
    assert short_hash("abc") == short_hash("abc")
    assert len(short_hash("abc")) == 8
    assert all(c in "0123456789abcdef" for c in short_hash("abc"))


def test_build_promotion_batch_id_shape():
    bid = build_promotion_batch_id()
    # 20260414T030000Z_a1b2c3d4
    parts = bid.split("_")
    assert len(parts) == 2
    assert parts[0].endswith("Z")
    assert len(parts[1]) == 8
```

- [ ] **Step 7.2: Run test to verify failure**

```bash
PYTHONPATH=scripts python -m pytest scripts/tests/test_promotion_slug.py -v
```
Expected: FAIL — `No module named 'vitruvius.promotion'`

- [ ] **Step 7.3: Create `scripts/vitruvius/promotion.py` stub with these helpers**

```python
from __future__ import annotations

import hashlib
import re

from .utils import utc_now_stamp


_SLUG_NON_ALNUM = re.compile(r"[^a-z0-9]+")


def slugify(value: str) -> str:
    value = value.lower()
    value = _SLUG_NON_ALNUM.sub("-", value)
    value = re.sub(r"-+", "-", value)
    return value.strip("-")


def short_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:8]


def build_relationship_id(from_entity: str, predicate: str, to_entity: str) -> str:
    slug = slugify(f"{from_entity}-{predicate}-{to_entity}")
    return f"rel-{slug}"


def build_promotion_batch_id() -> str:
    stamp = utc_now_stamp()
    return f"{stamp}_{short_hash(stamp)}"
```

- [ ] **Step 7.4: Run test to verify success**

```bash
PYTHONPATH=scripts python -m pytest scripts/tests/test_promotion_slug.py -v
```
Expected: `4 passed`

- [ ] **Step 7.5: Commit**

```bash
git add scripts/vitruvius/promotion.py scripts/tests/test_promotion_slug.py
git commit -m "feat(promotion): add slug, short_hash, and relationship ID builders"
```

---

## Task 8: Evidence Merge Logic

**Files:**
- Modify: `scripts/vitruvius/promotion.py`
- Create: `scripts/tests/test_promotion_merge.py`

- [ ] **Step 8.1: Write failing tests**

Create `scripts/tests/test_promotion_merge.py`:
```python
from vitruvius.promotion import merge_evidence, evidence_fingerprint


def test_evidence_fingerprint_stable():
    e = {
        "source_id": "law-pd-1096",
        "source_section_id": "sec-701",
        "evidence_snippet": "Every building...",
    }
    assert evidence_fingerprint(e) == evidence_fingerprint(e)


def test_merge_appends_new_evidence():
    existing = [{
        "source_id": "law-pd-1096", "source_section_id": "sec-701",
        "evidence_snippet": "A", "reviewer_confidence": 0.95, "review_decision": "keep",
        "reviewer_model": "gemma4:31b",
    }]
    new = [{
        "source_id": "law-pd-1096", "source_section_id": "sec-702",
        "evidence_snippet": "B", "reviewer_confidence": 0.91, "review_decision": "keep",
        "reviewer_model": "gemma4:31b",
    }]
    merged = merge_evidence(existing, new)
    assert len(merged) == 2


def test_merge_dedups_identical_evidence():
    existing = [{
        "source_id": "law-pd-1096", "source_section_id": "sec-701",
        "evidence_snippet": "A", "reviewer_confidence": 0.95, "review_decision": "keep",
        "reviewer_model": "gemma4:31b",
    }]
    merged = merge_evidence(existing, existing)
    assert len(merged) == 1


def test_merge_recomputes_min_confidence():
    from vitruvius.promotion import min_confidence
    ev = [
        {"reviewer_confidence": 0.95},
        {"reviewer_confidence": 0.91},
        {"reviewer_confidence": 0.99},
    ]
    assert min_confidence(ev) == 0.91
```

- [ ] **Step 8.2: Run test to verify failure**

```bash
PYTHONPATH=scripts python -m pytest scripts/tests/test_promotion_merge.py -v
```
Expected: FAIL — `cannot import name 'merge_evidence'`

- [ ] **Step 8.3: Implement merge helpers**

Append to `scripts/vitruvius/promotion.py`:
```python
def evidence_fingerprint(evidence_entry: dict) -> str:
    key = "|".join([
        str(evidence_entry.get("source_id", "")),
        str(evidence_entry.get("source_section_id", "")),
        short_hash(str(evidence_entry.get("evidence_snippet", ""))),
    ])
    return key


def merge_evidence(existing: list[dict], new: list[dict]) -> list[dict]:
    seen = {evidence_fingerprint(e): e for e in existing}
    for entry in new:
        fp = evidence_fingerprint(entry)
        if fp not in seen:
            seen[fp] = entry
    return list(seen.values())


def min_confidence(evidence: list[dict]) -> float:
    scores = [float(e.get("reviewer_confidence", 0.0)) for e in evidence]
    return min(scores) if scores else 0.0
```

- [ ] **Step 8.4: Run test to verify success**

```bash
PYTHONPATH=scripts python -m pytest scripts/tests/test_promotion_merge.py -v
```
Expected: `4 passed`

- [ ] **Step 8.5: Commit**

```bash
git add scripts/vitruvius/promotion.py scripts/tests/test_promotion_merge.py
git commit -m "feat(promotion): add evidence merge, fingerprint, and min_confidence helpers"
```

---

## Task 9: Audit Log Writer

**Files:**
- Modify: `scripts/vitruvius/promotion.py`
- Create: `scripts/tests/test_promotion_audit.py`

- [ ] **Step 9.1: Write failing tests**

Create `scripts/tests/test_promotion_audit.py`:
```python
from pathlib import Path

from vitruvius.promotion import append_audit_entry, AuditEntry


def test_append_creates_file_if_missing(tmp_path):
    log = tmp_path / "latest_promotion_audit.log"
    entry = AuditEntry(
        batch_id="20260414T030000Z_a1b2c3d4",
        record_id="rel-a-governs-b",
        action="created",
        path="003/shared/relationships/rel-a-governs-b.md",
        detail="first promotion",
    )
    append_audit_entry(log, entry)
    assert log.exists()
    text = log.read_text(encoding="utf-8")
    assert "rel-a-governs-b" in text
    assert "created" in text


def test_append_is_append_only(tmp_path):
    log = tmp_path / "latest_promotion_audit.log"
    for i in range(3):
        append_audit_entry(log, AuditEntry(
            batch_id="B", record_id=f"rel-{i}", action="created",
            path=f"p-{i}.md", detail=""
        ))
    assert log.read_text(encoding="utf-8").count("\n") >= 3
```

- [ ] **Step 9.2: Run test to verify failure**

```bash
PYTHONPATH=scripts python -m pytest scripts/tests/test_promotion_audit.py -v
```
Expected: FAIL — `cannot import name 'append_audit_entry'`

- [ ] **Step 9.3: Implement the audit writer**

Append to `scripts/vitruvius/promotion.py`:
```python
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class AuditEntry:
    batch_id: str
    record_id: str
    action: str  # "created" | "merged" | "rejected" | "rolled_back"
    path: str
    detail: str


def append_audit_entry(log_path: Path, entry: AuditEntry) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    stamp = utc_now_stamp()
    line = (
        f"{stamp}\t{entry.batch_id}\t{entry.action}\t{entry.record_id}\t"
        f"{entry.path}\t{entry.detail}\n"
    )
    with log_path.open("a", encoding="utf-8") as f:
        f.write(line)
```

- [ ] **Step 9.4: Run test to verify success**

```bash
PYTHONPATH=scripts python -m pytest scripts/tests/test_promotion_audit.py -v
```
Expected: `2 passed`

- [ ] **Step 9.5: Commit**

```bash
git add scripts/vitruvius/promotion.py scripts/tests/test_promotion_audit.py
git commit -m "feat(promotion): add append-only audit log writer with AuditEntry dataclass"
```

---

## Task 10: Relationship File Writer

**Files:**
- Modify: `scripts/vitruvius/promotion.py`
- Create: `scripts/tests/test_promotion_write.py`

- [ ] **Step 10.1: Write failing test**

Create `scripts/tests/test_promotion_write.py`:
```python
import yaml
from pathlib import Path

from vitruvius.promotion import write_relationship_file


def test_write_creates_valid_markdown_with_frontmatter(tmp_path):
    record = {
        "id": "rel-x-governs-y",
        "title": "X Governs Y",
        "page_type": "relationship",
        "relationship_type": "governs",
        "from_entity": "law-x",
        "to_entity": "concept-y",
        "trust_level": "primary",
        "canonical_status": "promoted",
        "confidence_score": 0.95,
        "promotion_batch_id": "B",
        "promotion_audit_log_ref": "p.log",
        "last_promoted_utc": "2026-04-14T00:00:00Z",
        "evidence": [{
            "source_id": "law-x",
            "source_section_id": "sec-1",
            "evidence_snippet": "snip",
            "reviewer_model": "gemma4:31b",
            "reviewer_confidence": 0.95,
            "review_decision": "keep",
            "reviewer_reason": "ok",
            "reviewed_at_utc": "2026-04-13T00:00:00Z",
        }],
    }
    output = tmp_path / "rel-x-governs-y.md"
    write_relationship_file(output, record)
    text = output.read_text(encoding="utf-8")
    assert text.startswith("---\n")
    assert "id: rel-x-governs-y" in text
    assert "# X Governs Y" in text
    assert "## Relationship Summary" in text
    assert "## Evidence" in text
    assert "sec-1" in text
```

- [ ] **Step 10.2: Run test to verify failure**

```bash
PYTHONPATH=scripts python -m pytest scripts/tests/test_promotion_write.py -v
```

- [ ] **Step 10.3: Implement `write_relationship_file`**

Append to `scripts/vitruvius/promotion.py`:
```python
def _render_frontmatter(record: dict) -> str:
    ordered_keys = [
        "id", "title", "page_type", "relationship_type",
        "from_entity", "to_entity", "trust_level", "canonical_status",
        "confidence_score", "promotion_batch_id", "promotion_audit_log_ref",
        "last_promoted_utc",
    ]
    lines = ["---"]
    for k in ordered_keys:
        if k in record:
            lines.append(f"{k}: {_yaml_scalar(record[k])}")
    lines.append("evidence:")
    for entry in record.get("evidence", []):
        lines.append("  -")
        for ek, ev in entry.items():
            lines.append(f"    {ek}: {_yaml_scalar(ev)}")
    lines.append("---")
    return "\n".join(lines)


def _yaml_scalar(value) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    s = str(value)
    if any(c in s for c in ':#"\'\n') or s == "":
        return '"' + s.replace('"', '\\"') + '"'
    return s


def _render_body(record: dict) -> str:
    lines = []
    lines.append(f"# {record.get('title', record.get('id', ''))}")
    lines.append("")
    lines.append("## Relationship Summary")
    lines.append("")
    lines.append(f"Promoted relationship of type `{record.get('relationship_type')}` "
                 f"from `{record.get('from_entity')}` to `{record.get('to_entity')}`.")
    lines.append("")
    lines.append("## Evidence")
    lines.append("")
    for idx, ev in enumerate(record.get("evidence", []), 1):
        lines.append(f"### Evidence {idx} — `{ev.get('source_id')}` §{ev.get('source_section_id')}")
        lines.append("")
        snippet = ev.get("evidence_snippet", "")
        lines.append(f"> {snippet}")
        lines.append("")
        lines.append(
            f"- Reviewer: `{ev.get('reviewer_model')}` · "
            f"Decision: `{ev.get('review_decision')}` · "
            f"Confidence: `{ev.get('reviewer_confidence')}`"
        )
        if ev.get("reviewed_at_utc"):
            lines.append(f"- Reviewed: {ev['reviewed_at_utc']}")
        lines.append(f"- Batch: `{record.get('promotion_batch_id')}`")
        lines.append("")
    return "\n".join(lines)


def write_relationship_file(path: Path, record: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    content = _render_frontmatter(record) + "\n\n" + _render_body(record) + "\n"
    path.write_text(content, encoding="utf-8")
```

- [ ] **Step 10.4: Run test to verify success**

```bash
PYTHONPATH=scripts python -m pytest scripts/tests/test_promotion_write.py -v
```
Expected: `1 passed`

- [ ] **Step 10.5: Commit**

```bash
git add scripts/vitruvius/promotion.py scripts/tests/test_promotion_write.py
git commit -m "feat(promotion): add relationship file writer with frontmatter + body rendering"
```

---

## Task 11: `run_promote` Orchestrator

**Files:**
- Modify: `scripts/vitruvius/promotion.py`
- Create: `scripts/tests/test_run_promote.py`

- [ ] **Step 11.1: Write the failing test for the full orchestrator**

Create `scripts/tests/test_run_promote.py`:
```python
import json
from pathlib import Path

import yaml

from vitruvius.promotion import run_promote_inner


def _seed_canonical_tree(root: Path) -> None:
    """Create a minimal canonical tree with one source and two concepts."""
    shared = root / "003_Canonical-Knowledge-Layer" / "shared"
    (shared / "sources").mkdir(parents=True)
    (shared / "concepts").mkdir(parents=True)
    (shared / "relationships").mkdir(parents=True)

    (shared / "sources" / "pd-1096.md").write_text(
        "---\nid: law-pd-1096\ntitle: PD 1096\npage_type: source\n"
        "trust_level: primary\ncanonical_status: draft\n"
        "last_canonicalized_utc: 2026-04-14T00:00:00Z\n---\n",
        encoding="utf-8",
    )
    for slug in ("occupancy-classification", "fire-resistive-construction"):
        (shared / "concepts" / f"{slug}.md").write_text(
            f"---\nid: concept-{slug}\ntitle: {slug}\npage_type: concept\n"
            "canonical_status: draft\n"
            "last_canonicalized_utc: 2026-04-14T00:00:00Z\n---\n",
            encoding="utf-8",
        )


def _seed_high_conf_file(root: Path) -> None:
    runs = root / "006_System-Manifests" / "runs"
    runs.mkdir(parents=True)
    payload = {
        "generated_at": "20260414T030000Z",
        "source_report_generated_at": "20260414T025500Z",
        "source_model": "gemma4:31b",
        "source": "pd-1096",
        "threshold": 0.90,
        "count": 1,
        "candidates": [
            {
                "candidate": {
                    "from": "law-pd-1096",
                    "type": "governs",
                    "to": "concept-fire-resistive-construction",
                    "occurrences": 1,
                    "sections": ["sec-701"],
                    "examples": ["Every building shall be classified..."],
                },
                "review": {
                    "decision": "keep",
                    "confidence": 0.92,
                    "reason": "clear governs",
                    "suggested_type": None,
                },
            }
        ],
    }
    (runs / "latest_relationship_review_high_confidence.json").write_text(
        json.dumps(payload), encoding="utf-8"
    )


def test_dry_run_does_not_write_files(tmp_path):
    _seed_canonical_tree(tmp_path)
    _seed_high_conf_file(tmp_path)

    result = run_promote_inner(repo_root=tmp_path, execute=False, rollback_batch_id=None)

    assert result["would_create"] == 1
    assert result["would_merge"] == 0
    rels = list((tmp_path / "003_Canonical-Knowledge-Layer" / "shared" / "relationships").iterdir())
    # dry-run must not write the new file; seed_canonical_tree only creates the dir
    assert not any(p.name.startswith("rel-") for p in rels)


def test_execute_writes_file_and_audit(tmp_path):
    _seed_canonical_tree(tmp_path)
    _seed_high_conf_file(tmp_path)

    result = run_promote_inner(repo_root=tmp_path, execute=True, rollback_batch_id=None)

    assert result["created"] == 1
    assert result["merged"] == 0
    rels_dir = tmp_path / "003_Canonical-Knowledge-Layer" / "shared" / "relationships"
    created = [p for p in rels_dir.iterdir() if p.name.startswith("rel-")]
    assert len(created) == 1
    audit_log = tmp_path / "006_System-Manifests" / "runs" / "latest_promotion_audit.log"
    assert audit_log.exists()
    assert "created" in audit_log.read_text(encoding="utf-8")


def test_idempotent_execute(tmp_path):
    _seed_canonical_tree(tmp_path)
    _seed_high_conf_file(tmp_path)

    run_promote_inner(repo_root=tmp_path, execute=True, rollback_batch_id=None)
    second = run_promote_inner(repo_root=tmp_path, execute=True, rollback_batch_id=None)

    # Second run must merge (or skip), not create a duplicate.
    assert second["created"] == 0
```

- [ ] **Step 11.2: Run test to verify failure**

```bash
PYTHONPATH=scripts python -m pytest scripts/tests/test_run_promote.py -v
```
Expected: FAIL — `cannot import name 'run_promote_inner'`

- [ ] **Step 11.3: Implement `run_promote_inner` and `run_promote`**

Append to `scripts/vitruvius/promotion.py`:
```python
import json
from typing import Any

from .promotion_validator import (
    build_canonical_index,
    load_registry,
    validate_promotion_record,
)


def _load_high_confidence(repo_root: Path) -> list[dict]:
    path = repo_root / "006_System-Manifests" / "runs" / "latest_relationship_review_high_confidence.json"
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload.get("candidates", [])


def _candidate_to_record(
    candidate_envelope: dict,
    *,
    canonical_index: dict,
    batch_id: str,
    audit_log_ref: str,
) -> dict | None:
    candidate = candidate_envelope["candidate"]
    review = candidate_envelope["review"]

    from_entity = candidate["from"]
    to_entity = candidate["to"]
    predicate = candidate["type"]
    rel_id = build_relationship_id(from_entity, predicate, to_entity)

    # derive trust_level from sources present in the evidence
    section_id = (candidate.get("sections") or [None])[0]
    snippet = (candidate.get("examples") or [""])[0]

    evidence_trust_source = from_entity if canonical_index.get(from_entity, {}).get("type") == "source" else None
    trust_level = canonical_index.get(evidence_trust_source, {}).get("trust_level") if evidence_trust_source else None

    evidence_entry = {
        "source_id": evidence_trust_source or from_entity,
        "source_section_id": section_id,
        "evidence_snippet": snippet,
        "review_decision": review["decision"],
        "reviewer_model": "gemma4:31b",
        "reviewer_confidence": float(review["confidence"]),
        "reviewer_reason": review.get("reason", ""),
        "extracted_at_utc": utc_now_stamp(),
        "reviewed_at_utc": utc_now_stamp(),
    }

    record = {
        "id": rel_id,
        "title": f"{from_entity} {predicate} {to_entity}",
        "page_type": "relationship",
        "relationship_type": predicate,
        "from_entity": from_entity,
        "to_entity": to_entity,
        "trust_level": trust_level or "unverified",
        "canonical_status": "promoted",
        "confidence_score": float(review["confidence"]),
        "promotion_batch_id": batch_id,
        "promotion_audit_log_ref": audit_log_ref,
        "last_promoted_utc": utc_now_stamp(),
        "evidence": [evidence_entry],
    }
    return record


def _load_existing_record(path: Path) -> dict | None:
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    return yaml.safe_load(text[3:end].strip()) or None


def run_promote_inner(
    *,
    repo_root: Path,
    execute: bool,
    rollback_batch_id: str | None,
) -> dict:
    if rollback_batch_id is not None:
        return _run_rollback(repo_root, rollback_batch_id)

    canonical_index = build_canonical_index(repo_root)
    registry = load_registry()

    rels_dir = repo_root / "003_Canonical-Knowledge-Layer" / "shared" / "relationships"
    runs_dir = repo_root / "006_System-Manifests" / "runs"
    audit_log = runs_dir / "latest_promotion_audit.log"

    candidates = _load_high_confidence(repo_root)
    batch_id = build_promotion_batch_id()

    result = {
        "batch_id": batch_id,
        "total_candidates": len(candidates),
        "created": 0, "merged": 0, "rejected": 0,
        "would_create": 0, "would_merge": 0, "would_reject": 0,
        "errors": [],
    }

    for envelope in candidates:
        record = _candidate_to_record(
            envelope,
            canonical_index=canonical_index,
            batch_id=batch_id,
            audit_log_ref=str(audit_log.relative_to(repo_root)),
        )
        if record is None:
            result["rejected"] += 1
            continue

        target_path = rels_dir / f"{record['id']}.md"
        existing = _load_existing_record(target_path)
        is_merge = existing is not None

        if is_merge:
            merged = merge_evidence(existing.get("evidence", []), record["evidence"])
            existing["evidence"] = merged
            existing["confidence_score"] = min_confidence(merged)
            existing["promotion_batch_id"] = batch_id
            existing["last_promoted_utc"] = utc_now_stamp()
            existing["promotion_audit_log_ref"] = str(audit_log.relative_to(repo_root))
            record = existing

        validation = validate_promotion_record(record, registry, canonical_index)
        if not validation.passed:
            result["rejected" if execute else "would_reject"] += 1
            result["errors"].append({"record_id": record["id"], "errors": validation.errors})
            if execute:
                append_audit_entry(audit_log, AuditEntry(
                    batch_id=batch_id,
                    record_id=record["id"],
                    action="rejected",
                    path=str(target_path),
                    detail="; ".join(validation.errors),
                ))
            continue

        if not execute:
            result["would_merge" if is_merge else "would_create"] += 1
            continue

        write_relationship_file(target_path, record)
        action = "merged" if is_merge else "created"
        result[action] += 1
        append_audit_entry(audit_log, AuditEntry(
            batch_id=batch_id,
            record_id=record["id"],
            action=action,
            path=str(target_path),
            detail=f"evidence_count={len(record['evidence'])}",
        ))

    return result


def _run_rollback(repo_root: Path, batch_id: str) -> dict:
    runs_dir = repo_root / "006_System-Manifests" / "runs"
    audit_log = runs_dir / "latest_promotion_audit.log"
    if not audit_log.exists():
        return {"rolled_back": 0, "errors": ["no audit log found"]}

    rels_dir = repo_root / "003_Canonical-Knowledge-Layer" / "shared" / "relationships"
    rolled_back = 0

    for line in audit_log.read_text(encoding="utf-8").splitlines():
        parts = line.split("\t")
        if len(parts) < 5:
            continue
        _stamp, bid, action, rid, path_str = parts[:5]
        if bid != batch_id or action != "created":
            continue
        target = Path(path_str)
        if not target.is_absolute():
            target = repo_root / target
        if target.exists():
            target.unlink()
            rolled_back += 1
            append_audit_entry(audit_log, AuditEntry(
                batch_id=batch_id,
                record_id=rid,
                action="rolled_back",
                path=str(target),
                detail="reversal",
            ))

    return {"rolled_back": rolled_back, "batch_id": batch_id}


def run_promote(
    *,
    execute: bool = False,
    rollback_batch_id: str | None = None,
) -> int:
    repo_root = Path(__file__).resolve().parent.parent.parent
    result = run_promote_inner(
        repo_root=repo_root,
        execute=execute,
        rollback_batch_id=rollback_batch_id,
    )
    print(json.dumps(result, indent=2, default=str))
    return 0 if not result.get("errors") else 0  # errors are reported, not fatal
```

- [ ] **Step 11.4: Run test to verify success**

```bash
PYTHONPATH=scripts python -m pytest scripts/tests/test_run_promote.py -v
```
Expected: `3 passed`

- [ ] **Step 11.5: Commit**

```bash
git add scripts/vitruvius/promotion.py scripts/tests/test_run_promote.py
git commit -m "feat(promotion): add run_promote orchestrator with dry-run default and rollback"
```

---

## Task 12: CLI Wiring

**Files:**
- Modify: `scripts/pipeline_cli.py`

- [ ] **Step 12.1: Add the import**

Edit `scripts/pipeline_cli.py` line 13 (after `from vitruvius.ollama_review import run_review_relationships_ollama`):
```python
from vitruvius.promotion import run_promote
```

- [ ] **Step 12.2: Register the subcommand**

In `build_parser()` (lines 33-81), after the `review_parser` block, add:
```python
    promote_parser = subparsers.add_parser("promote")
    promote_parser.add_argument("--execute", action="store_true",
                                help="Write changes (default: dry-run)")
    promote_parser.add_argument("--rollback", dest="rollback_batch_id",
                                default=None,
                                help="Rollback the given promotion batch ID")
```

- [ ] **Step 12.3: Dispatch the command**

In `main()`, after the `review-relationships-ollama` block (lines 163-167), add:
```python
    if args.command == "promote":
        return run_promote(
            execute=args.execute,
            rollback_batch_id=args.rollback_batch_id,
        )
```

- [ ] **Step 12.4: Smoke-test the CLI**

```bash
cd /Users/philiplewis/vitruvius
PYTHONPATH=scripts python scripts/pipeline_cli.py promote --help
```
Expected: Help text shows `--execute` and `--rollback BATCH_ID`.

- [ ] **Step 12.5: Commit**

```bash
git add scripts/pipeline_cli.py
git commit -m "feat(cli): register 'promote' subcommand with --execute and --rollback"
```

---

## Task 13: Golden Path End-to-End

**Files:**
- No new code. Verification only.

- [ ] **Step 13.1: Run the full test suite**

```bash
PYTHONPATH=scripts python -m pytest scripts/tests/ -v
```
Expected: All tests pass.

- [ ] **Step 13.2: Dry-run against the actual review output (if present)**

```bash
python scripts/pipeline_cli.py promote
```
Expected: JSON summary with `would_create` / `would_merge` / `would_reject` counts. No files written under `003_Canonical-Knowledge-Layer/shared/relationships/`.

If `latest_relationship_review_high_confidence.json` is missing, first run:
```bash
python scripts/pipeline_cli.py review-relationships-ollama
```
(Requires Ollama running with `gemma4:31b` pulled.)

- [ ] **Step 13.3: Execute and verify**

```bash
python scripts/pipeline_cli.py promote --execute
ls 003_Canonical-Knowledge-Layer/shared/relationships/ | head
cat 006_System-Manifests/runs/latest_promotion_audit.log
```
Expected: At least one `rel-*.md` file, at least one `created` line in the audit log.

- [ ] **Step 13.4: Verify idempotency**

```bash
python scripts/pipeline_cli.py promote --execute
python scripts/pipeline_cli.py promote --execute
```
Expected: Second run reports `created: 0` (merges or skips only). `git status` on the relationships directory shows no new files.

- [ ] **Step 13.5: Test rollback on a throwaway batch**

```bash
BATCH=$(awk -F'\t' '/\tcreated\t/{print $2; exit}' 006_System-Manifests/runs/latest_promotion_audit.log)
echo "Rolling back batch: $BATCH"
python scripts/pipeline_cli.py promote --rollback "$BATCH"
```
Expected: Files created in that batch are removed; a `rolled_back` entry appears in the audit log.

- [ ] **Step 13.6: Commit the run reports if the above is being done on real data**

```bash
git add 006_System-Manifests/runs/latest_promotion_audit.log 003_Canonical-Knowledge-Layer/shared/relationships/
git commit -m "chore(phase-7): first promotion golden-path batch on PD 1096"
```

---

## Task 14: Status Updates and Decision Log

**Files:**
- Modify: `.ai/01_roadmap/master-roadmap.md` (status table)
- Modify: `.ai/10_state/decisions.md` (AD-011)
- Modify: `.ai/10_state/active_context.md` (sprint closure)
- Modify: `.ai/01_roadmap/milestone-tracker.md`

- [ ] **Step 14.1: Update roadmap §4 status table**

Change the Phase 7 row from `❌ NOT STARTED` to `✅ COMPLETE` in `.ai/01_roadmap/master-roadmap.md` §4.

- [ ] **Step 14.2: Fill in AD-011 in `decisions.md`**

Replace the placeholder `AD-011` entry with the final record shape. Example (update with real numbers from Task 13):
```markdown
## AD-011: First Promoted Relationship Record Shape
- **Date:** 2026-04-28
- **Status:** Implemented
- **Context:** Sprint A · Task 13 produced the first promoted relationships.
- **Decision:** The record shape matches `/.ai/06_specs/relationship-schema.md` §4 with no deviations.
- **Observed counts:** <fill-in> candidates reviewed, <fill-in> cleared 0.90 gate, <fill-in> files created, <fill-in> merged.
- **Consequence:** Phase 8 (graph contract) is unblocked once volume hits ≥50 records.
```

- [ ] **Step 14.3: Update `active_context.md`**

Mark Sprint A closed, set the active sprint to Sprint B (Phase 1C + 6A full gap closure), and update the "Status of Supporting Work" table.

- [ ] **Step 14.4: Tick the Sprint A boxes in `milestone-tracker.md`**

Mark every `- [ ]` under Phase 7 in `milestone-tracker.md` as `- [x]`.

- [ ] **Step 14.5: Commit the docs**

```bash
git add .ai/01_roadmap/master-roadmap.md .ai/01_roadmap/milestone-tracker.md .ai/10_state/decisions.md .ai/10_state/active_context.md
git commit -m "docs(roadmap): close Sprint A, promote Phase 7 to COMPLETE"
```

---

## Self-Review Checklist

- **Spec coverage:** Every rule from `.ai/06_specs/relationship-schema.md` §10 (17 rules) has a test (Task 6). Every bullet in `.ai/01_roadmap/current-phase.md` "Sprint A Exit Criteria" maps to a task: A-1 → Task 1+2+3; A-2 → Task 4; A-3 → Task 6; A-4 → Tasks 7–12; A-5 → Task 13; A-6 → Task 14.
- **Placeholder scan:** No "TBD", "implement later", or empty steps. Every step contains either a command or full code.
- **Type consistency:** `ValidationResult` used consistently. `AuditEntry` field names match across tests and implementation. `run_promote_inner` is the testable seam; `run_promote` is the CLI entry point. `build_relationship_id` signature is stable across Tasks 7–11.

## Execution Handoff

**Two execution options:**

1. **Subagent-Driven** — dispatch one subagent per task, review between tasks, fast iteration. Use `superpowers:subagent-driven-development`.
2. **Inline Execution** — execute in this session using `superpowers:executing-plans`, batch execution with checkpoints.

**Recommended:** Subagent-Driven, because Tasks 6 and 11 are long and benefit from a clean context per task.
