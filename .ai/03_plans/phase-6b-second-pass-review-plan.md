---
plan_id: phase-6b-second-pass-review
phase: 6B
title: Second-Pass Review (Two-Stage Adjudication)
status: planned
priority: medium
sprint: "Sprint C (weeks 7-12)"
version: 1.0.0
plan_type: implementation_design_spec
created: 2026-04-14
last_updated: 2026-04-14
owner: Senior Systems Architect
prerequisites:
  - Phase 6A gap closure (retry, resume, parallelization) complete
  - Phase 7 Promotion Layer shipping (consumes only high-confidence keep)
dependencies:
  - .ai/08_prompts/qwen-second-pass.txt (design reference)
  - .ai/07_experiments/model-comparison.md (winner selection methodology)
related_plans:
  - phase-6a-review-gap-closure-plan.md
  - phase-7-promotion-governance-plan.md
unblocks:
  - Lower human-escalation rate
  - Better calibration on borderline candidates
---

# Phase 6B — Second-Pass Review Implementation Plan

**Goal:** Add a Tier-2 adjudicator that re-reviews only the uncertain subset of Tier-1 (Gemma) decisions and produces a merged adjudication report with an agreement matrix, reducing the `review_further` queue by ≥70% before human review.

**Architecture:** New module `scripts/vitruvius/ollama_review_second_pass.py`, new CLI command `review-relationships-ollama-second-pass`, and a new run artifact `latest_relationship_review_merged.json`. The Tier-2 model runs only on candidates filtered from Tier-1 output using the entry criteria in `/.ai/08_prompts/qwen-second-pass.txt`. Agreement and escalation computation follow the decision table in the same file.

**Tech Stack:** Python stdlib + existing Ollama HTTP client pattern from `ollama_review.py`. No new dependencies.

---

## Scope Boundary

**In scope:** Tier-2 prompt construction, HTTP call, filter logic, merged report, agreement matrix, human-escalation worklist, CLI integration.

**Out of scope:** Model benchmarking (covered by `/.ai/07_experiments/model-comparison.md`), Tier-3 human review UI (that's a separate product effort), changing the closed predicate vocabulary, re-running Tier-1 (Tier-2 is additive, not a replacement).

## File Structure

| Path | Change |
|---|---|
| `scripts/vitruvius/ollama_review_second_pass.py` | New — `run_second_pass()` orchestrator |
| `scripts/vitruvius/review_routing.py` | New — decision-table router (Tier 1 + Tier 2 → action) |
| `scripts/pipeline_cli.py` | Modify — register new command |
| `config/vitruvius.yaml` | Modify — add `review.second_pass.model`, `.timeout_seconds` keys |
| `scripts/tests/test_review_routing.py` | New — decision table coverage |
| `scripts/tests/test_second_pass_orchestrator.py` | New |
| `006_System-Manifests/runs/latest_relationship_review_merged.json` | New artifact (generated) |
| `006_System-Manifests/runs/latest_human_escalation_worklist.json` | New artifact (generated) |

---

## Phase 1 — Routing Logic (Tasks 1–2)

### Task 1: Entry Criteria Filter

Goal: From a Tier-1 review report, extract the candidates that need Tier 2.

- [ ] **Step 1.1: Write failing tests**

Create `scripts/tests/test_review_routing.py` with tests covering all entry criteria in `/.ai/08_prompts/qwen-second-pass.txt` "ENTRY CRITERIA":
```python
from vitruvius.review_routing import select_for_second_pass


def _t1(decision, confidence, suggested_type=None):
    return {
        "candidate": {"from": "a", "type": "governs", "to": "b"},
        "review": {
            "decision": decision, "confidence": confidence,
            "reason": "r", "suggested_type": suggested_type,
        },
    }


def test_skips_high_confidence_keep():
    assert select_for_second_pass([_t1("keep", 0.95)]) == []


def test_skips_high_confidence_reject():
    assert select_for_second_pass([_t1("reject", 0.95)]) == []


def test_routes_all_review_further():
    items = [_t1("review_further", 0.5), _t1("review_further", 0.95)]
    assert len(select_for_second_pass(items)) == 2


def test_routes_low_confidence_keep():
    assert len(select_for_second_pass([_t1("keep", 0.85)])) == 1


def test_routes_low_confidence_reject():
    assert len(select_for_second_pass([_t1("reject", 0.85)])) == 1


def test_routes_predicate_disagreement():
    items = [_t1("keep", 0.99, suggested_type="affects")]
    assert len(select_for_second_pass(items)) == 1
```

- [ ] **Step 1.2: Run test to verify failure**

```bash
PYTHONPATH=scripts python -m pytest scripts/tests/test_review_routing.py -v
```

- [ ] **Step 1.3: Implement `select_for_second_pass`**

Create `scripts/vitruvius/review_routing.py`:
```python
from __future__ import annotations

from typing import Any


CONFIDENCE_CUTOFF = 0.90


def select_for_second_pass(tier_one_items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    for item in tier_one_items:
        review = item["review"]
        decision = review["decision"]
        confidence = float(review["confidence"])
        suggested = review.get("suggested_type")
        candidate_type = item["candidate"]["type"]

        if decision == "review_further":
            selected.append(item)
            continue

        if decision == "keep" and confidence < CONFIDENCE_CUTOFF:
            selected.append(item)
            continue

        if decision == "reject" and confidence < CONFIDENCE_CUTOFF:
            selected.append(item)
            continue

        if suggested is not None and suggested != candidate_type:
            selected.append(item)
            continue

    return selected
```

- [ ] **Step 1.4: Commit**

```bash
PYTHONPATH=scripts python -m pytest scripts/tests/test_review_routing.py -v
git add scripts/vitruvius/review_routing.py scripts/tests/test_review_routing.py
git commit -m "feat(review): add Tier-2 entry-criteria filter"
```

### Task 2: Post-Tier-2 Decision Router

Goal: Given a Tier-1 + Tier-2 pair, decide the final action (`auto_promote`, `suppress`, `human_review`).

- [ ] **Step 2.1: Test the full decision table**

Append to `scripts/tests/test_review_routing.py` (one test per row of the decision table in `/.ai/08_prompts/qwen-second-pass.txt`):
```python
from vitruvius.review_routing import route_adjudication


def _pair(t1_decision, t1_conf, t2_decision, t2_conf):
    return {
        "tier_one": {"decision": t1_decision, "confidence": t1_conf},
        "tier_two": {"decision": t2_decision, "confidence": t2_conf},
    }


def test_t1_keep_high_skipped():
    # High confidence Tier 1 keep should never reach Tier 2. Router handles the
    # case anyway for safety.
    assert route_adjudication(_pair("keep", 0.95, None, None)) == "auto_promote"


def test_t1_keep_low_t2_keep_high():
    assert route_adjudication(_pair("keep", 0.85, "keep", 0.95)) == "auto_promote"


def test_t1_keep_low_t2_keep_low():
    assert route_adjudication(_pair("keep", 0.85, "keep", 0.85)) == "human_review"


def test_t1_keep_low_t2_reject():
    assert route_adjudication(_pair("keep", 0.85, "reject", 0.95)) == "human_review"


def test_t1_reject_low_t2_reject_high():
    assert route_adjudication(_pair("reject", 0.85, "reject", 0.95)) == "suppress"


def test_t1_reject_low_t2_keep():
    assert route_adjudication(_pair("reject", 0.85, "keep", 0.95)) == "human_review"


def test_t1_review_further_t2_keep_high():
    assert route_adjudication(_pair("review_further", 0.5, "keep", 0.95)) == "human_review"


def test_t1_review_further_t2_reject_high():
    assert route_adjudication(_pair("review_further", 0.5, "reject", 0.95)) == "suppress"


def test_t2_parse_error_defaults_to_human_review():
    assert route_adjudication(_pair("keep", 0.85, None, None)) == "human_review"
```

- [ ] **Step 2.2: Implement `route_adjudication`**

Append to `scripts/vitruvius/review_routing.py`:
```python
def route_adjudication(pair: dict[str, Any]) -> str:
    t1 = pair["tier_one"]
    t2 = pair["tier_two"]

    t1_dec = t1["decision"]
    t1_conf = float(t1.get("confidence") or 0.0)
    t2_dec = t2.get("decision") if t2 else None
    t2_conf = float(t2.get("confidence") or 0.0) if t2 else 0.0

    if t1_dec == "keep" and t1_conf >= CONFIDENCE_CUTOFF:
        return "auto_promote"

    if t2_dec is None:
        if t1_dec == "keep" and t1_conf < CONFIDENCE_CUTOFF:
            return "human_review"
        if t1_dec == "reject" and t1_conf < CONFIDENCE_CUTOFF:
            return "human_review"
        return "human_review"

    if t1_dec == "keep":
        if t2_dec == "keep" and t2_conf >= CONFIDENCE_CUTOFF:
            return "auto_promote"
        return "human_review"

    if t1_dec == "reject":
        if t2_dec == "reject" and t2_conf >= CONFIDENCE_CUTOFF:
            return "suppress"
        return "human_review"

    if t1_dec == "review_further":
        if t2_dec == "reject" and t2_conf >= CONFIDENCE_CUTOFF:
            return "suppress"
        return "human_review"

    return "human_review"
```

- [ ] **Step 2.3: Run tests and commit**

```bash
PYTHONPATH=scripts python -m pytest scripts/tests/test_review_routing.py -v
git add scripts/vitruvius/review_routing.py scripts/tests/test_review_routing.py
git commit -m "feat(review): add Tier-1+Tier-2 decision router per qwen-second-pass.txt"
```

---

## Phase 2 — Tier-2 Orchestrator (Tasks 3–5)

### Task 3: Tier-2 Prompt Builder

- [ ] **Step 3.1: Write failing test**

Create `scripts/tests/test_second_pass_orchestrator.py`:
```python
import json

from vitruvius.ollama_review_second_pass import build_second_pass_prompt


def test_prompt_includes_tier_one_decision():
    candidate = {
        "from": "concept-a", "type": "governs", "to": "concept-b",
        "occurrences": 1, "sections": ["sec-1"], "examples": ["e"],
    }
    t1 = {"decision": "review_further", "confidence": 0.4, "reason": "unclear", "suggested_type": None}

    prompt_text = build_second_pass_prompt(candidate, t1, model_name="gemma4:31b")
    prompt = json.loads(prompt_text)

    assert prompt["tier_one_decision"]["decision"] == "review_further"
    assert prompt["tier_one_decision"]["model"] == "gemma4:31b"
    assert "agrees_with_tier_one" in prompt["output_schema"]
```

- [ ] **Step 3.2: Implement the builder**

Create `scripts/vitruvius/ollama_review_second_pass.py`:
```python
from __future__ import annotations

import json
from typing import Any


def build_second_pass_prompt(
    candidate: dict[str, Any],
    tier_one: dict[str, Any],
    *,
    model_name: str,
) -> str:
    payload = {
        "task": "Second-pass adjudication of a legal relationship candidate",
        "allowed_decisions": ["keep", "review_further", "reject"],
        "candidate": {
            "from": candidate["from"],
            "type": candidate["type"],
            "to": candidate["to"],
            "occurrences": candidate.get("occurrences", 0),
            "sections": candidate.get("sections", []),
            "examples": candidate.get("examples", []),
        },
        "tier_one_decision": {
            "model": model_name,
            "decision": tier_one["decision"],
            "confidence": tier_one["confidence"],
            "reason": tier_one.get("reason", ""),
            "suggested_type": tier_one.get("suggested_type"),
        },
        "instructions": [
            "You are a second-pass adjudicator. A different model has already reviewed this candidate.",
            "Independently assess the candidate using only the supplied evidence examples.",
            "Consider but do not blindly defer to the Tier 1 decision.",
            "If you disagree with Tier 1, say so explicitly in your reason.",
            "If the evidence clearly supports the candidate and the predicate, choose keep with high confidence.",
            "If the predicate is wrong but the endpoints are right, choose review_further and set suggested_type.",
            "If the evidence is irrelevant, weak, or contradicts the claim, choose reject.",
            "Do not invent facts. Do not propose new subjects or objects.",
            "Return valid JSON only with no markdown fences.",
        ],
        "output_schema": {
            "decision": "keep|review_further|reject",
            "confidence": "number from 0.0 to 1.0",
            "reason": "short explanation",
            "suggested_type": "string or null",
            "agrees_with_tier_one": "boolean",
        },
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)
```

- [ ] **Step 3.3: Run test and commit**

```bash
PYTHONPATH=scripts python -m pytest scripts/tests/test_second_pass_orchestrator.py -v
git add scripts/vitruvius/ollama_review_second_pass.py scripts/tests/test_second_pass_orchestrator.py
git commit -m "feat(review): add Tier-2 prompt builder per qwen-second-pass.txt spec"
```

### Task 4: Run Tier-2 Against Tier-1 Output

- [ ] **Step 4.1: Add config keys**

Append to `config/vitruvius.yaml`:
```yaml
  second_pass:
    model: "qwen3:30b"
    timeout_seconds: 600
```

Add helpers in `scripts/vitruvius/config.py`:
```python
def get_second_pass_model() -> str:
    return load_config().get("review", {}).get("second_pass", {}).get("model", "qwen3:30b")


def get_second_pass_timeout() -> int:
    return int(load_config().get("review", {}).get("second_pass", {}).get("timeout_seconds", 600))
```

- [ ] **Step 4.2: Implement `run_second_pass`**

Append to `scripts/vitruvius/ollama_review_second_pass.py`:
```python
from pathlib import Path

from .config import get_second_pass_model, get_second_pass_timeout
from .ollama_review import call_ollama, parse_model_json
from .paths import get_repo_root
from .reports import write_json
from .review_routing import route_adjudication, select_for_second_pass
from .utils import utc_now_stamp


def _load_tier_one_report() -> dict[str, Any]:
    path = get_repo_root() / "006_System-Manifests" / "runs" / "latest_relationship_review_ollama.json"
    if not path.exists():
        raise FileNotFoundError(
            f"Tier 1 review report not found: {path}. Run review-relationships-ollama first."
        )
    return json.loads(path.read_text(encoding="utf-8"))


def _adjudicate_one(item: dict[str, Any], *, model: str, timeout: int) -> dict[str, Any]:
    candidate = item["candidate"]
    tier_one = item["review"]

    prompt = build_second_pass_prompt(candidate, tier_one, model_name=model)
    try:
        raw = call_ollama(prompt, model=model, timeout_seconds=timeout)
        tier_two = parse_model_json(raw)
        tier_two["agrees_with_tier_one"] = (
            tier_two["decision"] == tier_one["decision"]
            and (tier_two.get("suggested_type") or None) == (tier_one.get("suggested_type") or None)
        )
    except Exception as exc:
        tier_two = {
            "decision": "review_further",
            "confidence": 0.0,
            "reason": f"Qwen second pass failed: {exc}",
            "suggested_type": None,
            "agrees_with_tier_one": False,
        }

    return {
        "candidate": candidate,
        "tier_one": tier_one,
        "tier_two": tier_two,
        "action": route_adjudication({"tier_one": tier_one, "tier_two": tier_two}),
    }


def run_second_pass(*, model: str | None = None, timeout_seconds: int | None = None) -> int:
    model = model or get_second_pass_model()
    timeout_seconds = timeout_seconds or get_second_pass_timeout()

    repo_root = get_repo_root()
    runs_dir = repo_root / "006_System-Manifests" / "runs"
    runs_dir.mkdir(parents=True, exist_ok=True)

    tier_one_report = _load_tier_one_report()
    selected = select_for_second_pass(tier_one_report.get("reviews", []))

    print(f"Tier 2 ({model}) adjudicating {len(selected)} uncertain candidates...")

    adjudicated: list[dict[str, Any]] = []
    for idx, item in enumerate(selected, start=1):
        print(f"[{idx}/{len(selected)}] {item['candidate']['from']} -> {item['candidate']['to']}")
        adjudicated.append(_adjudicate_one(item, model=model, timeout=timeout_seconds))

    # aggregate counts
    action_counts: dict[str, int] = {"auto_promote": 0, "suppress": 0, "human_review": 0}
    disagreement = 0
    for a in adjudicated:
        action_counts[a["action"]] += 1
        if not a["tier_two"]["agrees_with_tier_one"]:
            disagreement += 1

    merged_report = {
        "generated_at": utc_now_stamp(),
        "tier_one_model": tier_one_report.get("model"),
        "tier_two_model": model,
        "total_tier_one": len(tier_one_report.get("reviews", [])),
        "total_second_pass": len(selected),
        "disagreement_rate": (disagreement / len(adjudicated)) if adjudicated else 0.0,
        "actions": action_counts,
        "items": adjudicated,
    }

    write_json(runs_dir / "latest_relationship_review_merged.json", merged_report)

    # Human escalation worklist
    worklist = [a for a in adjudicated if a["action"] == "human_review"]
    write_json(
        runs_dir / "latest_human_escalation_worklist.json",
        {
            "generated_at": utc_now_stamp(),
            "count": len(worklist),
            "items": worklist,
        },
    )

    print(f"Tier 2 complete. auto_promote={action_counts['auto_promote']} "
          f"suppress={action_counts['suppress']} human_review={action_counts['human_review']}")
    return 0
```

### Task 5: CLI Wiring

- [ ] **Step 5.1: Register the command**

In `scripts/pipeline_cli.py`:
```python
from vitruvius.ollama_review_second_pass import run_second_pass
```

```python
    second_pass_parser = subparsers.add_parser("review-relationships-ollama-second-pass")
    second_pass_parser.add_argument("--model", default=None)
    second_pass_parser.add_argument("--timeout-seconds", type=int, default=None)
```

```python
    if args.command == "review-relationships-ollama-second-pass":
        return run_second_pass(model=args.model, timeout_seconds=args.timeout_seconds)
```

- [ ] **Step 5.2: Commit**

```bash
git add scripts/pipeline_cli.py scripts/vitruvius/ollama_review_second_pass.py scripts/vitruvius/config.py config/vitruvius.yaml
git commit -m "feat(cli): add review-relationships-ollama-second-pass composite command"
```

---

## Phase 3 — Metrics & Observability (Task 6)

### Task 6: Agreement Matrix in Merged Report

Expand the merged report to include a full agreement matrix:

| | Tier 2 keep | Tier 2 review_further | Tier 2 reject |
|---|---|---|---|
| Tier 1 keep | ... | ... | ... |
| Tier 1 review_further | ... | ... | ... |
| Tier 1 reject | ... | ... | ... |

- [ ] **Step 6.1: Write the test**

```python
def test_agreement_matrix_shape():
    from vitruvius.ollama_review_second_pass import compute_agreement_matrix

    items = [
        {"tier_one": {"decision": "keep"}, "tier_two": {"decision": "keep"}},
        {"tier_one": {"decision": "keep"}, "tier_two": {"decision": "reject"}},
        {"tier_one": {"decision": "review_further"}, "tier_two": {"decision": "keep"}},
    ]
    m = compute_agreement_matrix(items)
    assert m["keep"]["keep"] == 1
    assert m["keep"]["reject"] == 1
    assert m["review_further"]["keep"] == 1
```

- [ ] **Step 6.2: Implement `compute_agreement_matrix`**

Append to `scripts/vitruvius/ollama_review_second_pass.py`:
```python
def compute_agreement_matrix(items: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    axes = ("keep", "review_further", "reject")
    matrix = {a: {b: 0 for b in axes} for a in axes}
    for item in items:
        t1 = item["tier_one"]["decision"]
        t2 = item["tier_two"]["decision"]
        if t1 in matrix and t2 in matrix[t1]:
            matrix[t1][t2] += 1
    return matrix
```

Wire it into `run_second_pass` by adding `"agreement_matrix": compute_agreement_matrix(adjudicated)` to `merged_report`.

- [ ] **Step 6.3: Commit**

```bash
git add scripts/vitruvius/ollama_review_second_pass.py scripts/tests/test_second_pass_orchestrator.py
git commit -m "feat(review): add agreement matrix to Tier 2 merged report"
```

---

## Self-Review Checklist

- **Decision table coverage:** Every row from `/.ai/08_prompts/qwen-second-pass.txt` "DECISION TABLE" has a test in `test_review_routing.py`.
- **Prompt fidelity:** `build_second_pass_prompt` matches the EXACT PROMPT PAYLOAD from `qwen-second-pass.txt` §"EXACT PROMPT PAYLOAD".
- **Graceful degradation:** Parse/HTTP errors default to `review_further` with `agrees_with_tier_one: false`, same convention as Tier 1.
- **No placeholders:** All steps are actionable with complete code or commands.

## Execution Handoff

Recommended: Subagent-driven. Tasks 1–2 and Tasks 3–5 form two natural sub-phases.
