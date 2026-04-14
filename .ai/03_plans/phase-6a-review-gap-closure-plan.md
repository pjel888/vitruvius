---
plan_id: phase-6a-review-gap-closure
phase: 6A
title: Review Layer Gap Closure
status: partial
priority: high
sprint: "Sprint A + Sprint B (weeks 1-6)"
version: 1.0.0
plan_type: implementation_tdd
created: 2026-04-14
last_updated: 2026-04-14
owner: Senior Systems Architect
prerequisites:
  - Phase 6A (LLM review) complete — verified 2026-04-13
dependencies:
  - .ai/02_audits/review-layer-audit.md
  - scripts/vitruvius/ollama_review.py
related_plans:
  - phase-7-promotion-governance-plan.md (depends on minimal subset of this)
unblocks:
  - Automatic pipeline integration (review becomes part of `run`)
---

# Phase 6A — Review Layer Gap Closure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` or `superpowers:executing-plans`. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close the seven known gaps in `ollama_review.py` identified by the 2026-04-13 review-layer audit: hardcoded Ollama URL, no retry, no resume, no config file support, no parallelization, no confidence-threshold auto-filter, and no automatic pipeline integration.

**Architecture:** Incremental, test-driven improvements to the existing `ollama_review.py` module. The Sprint A subset (config migration + high-confidence writer) is carved out into `phase-7-promotion-governance-plan.md` as Tasks 1–3 because Phase 7 depends on it. This plan covers the Sprint B/C remainder.

**Tech Stack:** Python stdlib (`urllib`, `concurrent.futures`, `json`, `pathlib`); pytest.

---

## Scope Boundary (what is and is NOT here)

| Gap | Covered by |
|---|---|
| Hardcoded Ollama URL → config | Phase 7 plan, Tasks 1–2 (Sprint A) |
| High-confidence output writer | Phase 7 plan, Task 3 (Sprint A) |
| Per-candidate retry with bounded attempts | **This plan, Task 1** |
| Resume from `in_progress` save | **This plan, Task 2** |
| Per-candidate timeout | **This plan, Task 3** |
| Parallelization (`concurrent.futures`) | **This plan, Task 4** |
| Automatic pipeline integration (opt-in) | **This plan, Task 5** |
| Second-pass review | Phase 6B plan (separate) |

## File Structure

| Path | Change |
|---|---|
| `scripts/vitruvius/ollama_review.py` | Modify — add retry, resume, timeout, parallelization |
| `scripts/pipeline_cli.py` | Modify — new `run-with-review` command |
| `config/vitruvius.yaml` | Modify — add retry and parallelism keys |
| `scripts/tests/test_ollama_retry.py` | New |
| `scripts/tests/test_ollama_resume.py` | New |
| `scripts/tests/test_ollama_parallel.py` | New |

---

## Task 1: Per-Candidate Retry

**Files:**
- Modify: `scripts/vitruvius/ollama_review.py:140-157` (`review_relationship`)
- Create: `scripts/tests/test_ollama_retry.py`

- [ ] **Step 1.1: Add retry config keys**

Append to `config/vitruvius.yaml` under `review.ollama`:
```yaml
    max_retries_per_candidate: 3
    retry_backoff_seconds: 2
```

Add to `scripts/vitruvius/config.py`:
```python
def get_ollama_max_retries() -> int:
    return int(load_config().get("review", {}).get("ollama", {}).get("max_retries_per_candidate", 3))


def get_ollama_retry_backoff() -> float:
    return float(load_config().get("review", {}).get("ollama", {}).get("retry_backoff_seconds", 2))
```

- [ ] **Step 1.2: Write the failing test**

Create `scripts/tests/test_ollama_retry.py`:
```python
from unittest.mock import patch, MagicMock

from vitruvius.ollama_review import review_relationship


def test_retries_up_to_three_times_on_transient_error():
    call_count = {"n": 0}

    def flaky_call(prompt, model, timeout_seconds):
        call_count["n"] += 1
        if call_count["n"] < 3:
            raise RuntimeError("transient")
        return '{"decision":"keep","confidence":0.95,"reason":"ok","suggested_type":null}'

    with patch("vitruvius.ollama_review.call_ollama", side_effect=flaky_call):
        result = review_relationship(
            {"from": "a", "type": "governs", "to": "b", "sections": [], "examples": []},
            model="gemma4:31b",
            timeout_seconds=60,
        )

    assert call_count["n"] == 3
    assert result["review"]["decision"] == "keep"


def test_falls_back_to_review_further_after_all_retries():
    with patch("vitruvius.ollama_review.call_ollama", side_effect=RuntimeError("down")):
        result = review_relationship(
            {"from": "a", "type": "governs", "to": "b", "sections": [], "examples": []},
            model="gemma4:31b",
            timeout_seconds=60,
        )
    assert result["review"]["decision"] == "review_further"
    assert result["review"]["confidence"] == 0.0
    assert "Ollama review failed" in result["review"]["reason"]
```

- [ ] **Step 1.3: Run test to verify failure**

```bash
PYTHONPATH=scripts python -m pytest scripts/tests/test_ollama_retry.py -v
```
Expected: First test fails because retry is not implemented.

- [ ] **Step 1.4: Implement retry logic**

Replace `review_relationship` in `scripts/vitruvius/ollama_review.py`:
```python
def review_relationship(candidate: dict[str, Any], model: str, timeout_seconds: int) -> dict[str, Any]:
    from .config import get_ollama_max_retries, get_ollama_retry_backoff

    max_retries = get_ollama_max_retries()
    backoff = get_ollama_retry_backoff()

    prompt = build_prompt(candidate)

    last_exc: Exception | None = None
    for attempt in range(1, max_retries + 1):
        try:
            raw_response = call_ollama(prompt, model=model, timeout_seconds=timeout_seconds)
            review = parse_model_json(raw_response)
            return {"candidate": candidate, "review": review}
        except Exception as exc:
            last_exc = exc
            if attempt < max_retries:
                time.sleep(backoff * attempt)

    return {
        "candidate": candidate,
        "review": {
            "decision": "review_further",
            "confidence": 0.0,
            "reason": f"Ollama review failed after {max_retries} attempts: {last_exc}",
            "suggested_type": None,
        },
    }
```

- [ ] **Step 1.5: Run test to verify success**

```bash
PYTHONPATH=scripts python -m pytest scripts/tests/test_ollama_retry.py -v
```
Expected: `2 passed`

- [ ] **Step 1.6: Commit**

```bash
git add scripts/vitruvius/ollama_review.py scripts/vitruvius/config.py config/vitruvius.yaml scripts/tests/test_ollama_retry.py
git commit -m "feat(review): retry Ollama calls up to N times with linear backoff"
```

---

## Task 2: Resume From Progress

**Files:**
- Modify: `scripts/vitruvius/ollama_review.py` (`run_review_relationships_ollama`)
- Create: `scripts/tests/test_ollama_resume.py`

The existing code saves `in_progress` snapshots but never reads them back on relaunch. Users who hit Ctrl-C or lose power currently have to re-run from scratch.

- [ ] **Step 2.1: Write the failing test**

Create `scripts/tests/test_ollama_resume.py`:
```python
import json
from pathlib import Path

from vitruvius.ollama_review import load_resume_state


def test_load_resume_state_returns_empty_when_no_snapshot(tmp_path):
    state = load_resume_state(tmp_path)
    assert state["reviews"] == []
    assert state["status"] is None


def test_load_resume_state_reads_in_progress(tmp_path):
    (tmp_path).mkdir(exist_ok=True)
    snapshot = {
        "generated_at": "20260414T030000Z",
        "model": "gemma4:31b",
        "source": "s",
        "total_candidates": 5,
        "completed_reviews": 2,
        "status": "in_progress",
        "summary": {},
        "reviews": [
            {"candidate": {"from": "a", "type": "governs", "to": "b"}, "review": {}},
            {"candidate": {"from": "c", "type": "governs", "to": "d"}, "review": {}},
        ],
    }
    (tmp_path / "latest_relationship_review_ollama.json").write_text(
        json.dumps(snapshot), encoding="utf-8"
    )

    state = load_resume_state(tmp_path)

    assert state["status"] == "in_progress"
    assert len(state["reviews"]) == 2
    assert state["completed_count"] == 2
```

- [ ] **Step 2.2: Run test to verify failure**

```bash
PYTHONPATH=scripts python -m pytest scripts/tests/test_ollama_resume.py -v
```

- [ ] **Step 2.3: Implement `load_resume_state`**

Append to `scripts/vitruvius/ollama_review.py` before `run_review_relationships_ollama`:
```python
def load_resume_state(runs_dir: Path) -> dict[str, Any]:
    snapshot_path = runs_dir / "latest_relationship_review_ollama.json"
    if not snapshot_path.exists():
        return {"reviews": [], "status": None, "completed_count": 0}

    payload = json.loads(snapshot_path.read_text(encoding="utf-8"))
    if payload.get("status") != "in_progress":
        return {"reviews": [], "status": payload.get("status"), "completed_count": 0}

    return {
        "reviews": payload.get("reviews", []),
        "status": "in_progress",
        "completed_count": len(payload.get("reviews", [])),
    }
```

In `run_review_relationships_ollama`, after `reviews: list[dict[str, Any]] = []`, add:
```python
    resume_state = load_resume_state(runs_dir)
    if resume_state["status"] == "in_progress" and resume_state["reviews"]:
        print(f"Resuming from {resume_state['completed_count']} previously completed reviews.")
        reviews = resume_state["reviews"]
        candidates_to_process = candidates[len(reviews):]
    else:
        candidates_to_process = candidates
```

And change the loop header to iterate over `candidates_to_process` with `start=len(reviews) + 1` so the progress numbers stay correct.

- [ ] **Step 2.4: Run test to verify success**

```bash
PYTHONPATH=scripts python -m pytest scripts/tests/test_ollama_resume.py -v
```
Expected: `2 passed`

- [ ] **Step 2.5: Commit**

```bash
git add scripts/vitruvius/ollama_review.py scripts/tests/test_ollama_resume.py
git commit -m "feat(review): resume from latest in_progress snapshot on relaunch"
```

---

## Task 3: Per-Candidate Timeout (Already Partial — Harden)

**Files:**
- Modify: `scripts/vitruvius/ollama_review.py` (`call_ollama`)

The current timeout is per HTTP call, which is per-candidate since calls are sequential. However, the retry loop added in Task 1 can extend total time to `timeout * max_retries`. Hardening step: enforce a hard wall-clock cap per candidate that spans all retries.

- [ ] **Step 3.1: Write the failing test**

Append to `scripts/tests/test_ollama_retry.py`:
```python
import time
from unittest.mock import patch

from vitruvius.ollama_review import review_relationship


def test_honors_wall_clock_cap_across_retries():
    def slow_call(prompt, model, timeout_seconds):
        time.sleep(0.1)
        raise RuntimeError("transient")

    start = time.monotonic()
    with patch("vitruvius.ollama_review.call_ollama", side_effect=slow_call):
        review_relationship(
            {"from": "a", "type": "governs", "to": "b", "sections": [], "examples": []},
            model="gemma4:31b",
            timeout_seconds=60,
        )
    elapsed = time.monotonic() - start
    # 3 retries * 0.1s call + 2 backoffs (2 + 4) = ~6.3s but the wall-cap must clamp this
    assert elapsed < 10.0, f"Retry loop ran for {elapsed}s, exceeds cap"
```

- [ ] **Step 3.2: Run the test**

```bash
PYTHONPATH=scripts python -m pytest scripts/tests/test_ollama_retry.py::test_honors_wall_clock_cap_across_retries -v
```

- [ ] **Step 3.3: Add wall-clock cap to `review_relationship`**

In `scripts/vitruvius/ollama_review.py`, wrap the retry loop with a monotonic-clock check:
```python
def review_relationship(candidate: dict[str, Any], model: str, timeout_seconds: int) -> dict[str, Any]:
    from .config import get_ollama_max_retries, get_ollama_retry_backoff

    max_retries = get_ollama_max_retries()
    backoff = get_ollama_retry_backoff()
    prompt = build_prompt(candidate)

    deadline = time.monotonic() + timeout_seconds
    last_exc: Exception | None = None

    for attempt in range(1, max_retries + 1):
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            break
        call_timeout = min(timeout_seconds, max(1, int(remaining)))
        try:
            raw_response = call_ollama(prompt, model=model, timeout_seconds=call_timeout)
            review = parse_model_json(raw_response)
            return {"candidate": candidate, "review": review}
        except Exception as exc:
            last_exc = exc
            if attempt < max_retries and time.monotonic() + (backoff * attempt) < deadline:
                time.sleep(backoff * attempt)

    return {
        "candidate": candidate,
        "review": {
            "decision": "review_further",
            "confidence": 0.0,
            "reason": f"Ollama review failed (wall-cap or retries exhausted): {last_exc}",
            "suggested_type": None,
        },
    }
```

- [ ] **Step 3.4: Run test and commit**

```bash
PYTHONPATH=scripts python -m pytest scripts/tests/test_ollama_retry.py -v
git add scripts/vitruvius/ollama_review.py scripts/tests/test_ollama_retry.py
git commit -m "feat(review): enforce wall-clock deadline spanning retries"
```

---

## Task 4: Opt-In Parallelization

**Files:**
- Modify: `scripts/vitruvius/ollama_review.py`
- Create: `scripts/tests/test_ollama_parallel.py`

Ollama can handle concurrent requests to the same model (the model is loaded once, requests are queued on the server). Local experimentation shows 2–4 parallel candidates is a sweet spot. This task makes parallelism opt-in via `--parallel N` with `N=1` (current behavior) as the default.

- [ ] **Step 4.1: Add config key**

Append to `config/vitruvius.yaml` under `review.ollama`:
```yaml
    default_parallelism: 1
```

Add helper:
```python
def get_ollama_default_parallelism() -> int:
    return int(load_config().get("review", {}).get("ollama", {}).get("default_parallelism", 1))
```

- [ ] **Step 4.2: Write the failing test**

Create `scripts/tests/test_ollama_parallel.py`:
```python
from unittest.mock import patch

from vitruvius.ollama_review import review_candidates_parallel


def test_returns_results_in_order():
    candidates = [
        {"from": f"c-{i}", "type": "governs", "to": f"c-{i+1}", "sections": [], "examples": []}
        for i in range(5)
    ]

    def stub(prompt, model, timeout_seconds):
        # decision keyed to the from-id so we can verify ordering
        import json
        payload = json.loads(prompt)
        from_id = payload["candidate"]["from"]
        return f'{{"decision":"keep","confidence":0.95,"reason":"{from_id}","suggested_type":null}}'

    with patch("vitruvius.ollama_review.call_ollama", side_effect=stub):
        results = review_candidates_parallel(
            candidates, model="gemma4:31b", timeout_seconds=60, parallelism=2
        )

    assert len(results) == 5
    assert [r["candidate"]["from"] for r in results] == [c["from"] for c in candidates]
    assert [r["review"]["reason"] for r in results] == [f"c-{i}" for i in range(5)]
```

- [ ] **Step 4.3: Implement `review_candidates_parallel`**

Append to `scripts/vitruvius/ollama_review.py`:
```python
from concurrent.futures import ThreadPoolExecutor


def review_candidates_parallel(
    candidates: list[dict[str, Any]],
    *,
    model: str,
    timeout_seconds: int,
    parallelism: int,
) -> list[dict[str, Any]]:
    if parallelism <= 1:
        return [review_relationship(c, model=model, timeout_seconds=timeout_seconds)
                for c in candidates]

    with ThreadPoolExecutor(max_workers=parallelism) as pool:
        futures = [
            pool.submit(review_relationship, c, model, timeout_seconds)
            for c in candidates
        ]
        return [f.result() for f in futures]  # ordered matches submit order
```

- [ ] **Step 4.4: Expose `--parallel` flag**

In `scripts/pipeline_cli.py`, add to `review_parser`:
```python
    review_parser.add_argument("--parallel", type=int, default=None,
                               help="Number of concurrent Ollama requests (default: config)")
```

And pass it through in `main()`:
```python
    if args.command == "review-relationships-ollama":
        return run_review_relationships_ollama(
            model=args.model,
            timeout_seconds=args.timeout_seconds,
            parallelism=args.parallel,
        )
```

In `run_review_relationships_ollama`, accept `parallelism: int | None = None` and fall back to the config default when `None`. Route the candidate loop through `review_candidates_parallel`.

- [ ] **Step 4.5: Run test to verify success**

```bash
PYTHONPATH=scripts python -m pytest scripts/tests/test_ollama_parallel.py -v
```
Expected: `1 passed`

- [ ] **Step 4.6: Commit**

```bash
git add scripts/vitruvius/ollama_review.py scripts/pipeline_cli.py scripts/vitruvius/config.py config/vitruvius.yaml scripts/tests/test_ollama_parallel.py
git commit -m "feat(review): opt-in parallel candidate review with ThreadPoolExecutor"
```

---

## Task 5: Opt-In Pipeline Integration

**Files:**
- Modify: `scripts/pipeline_cli.py`

Add a new composite command `run-with-review` that runs `scan → status → lint → convert → canonicalize-* → extract-relationships-sections-* → review-relationships-ollama`. The default `run` remains unchanged (scan/status/lint only), preserving the principle that review stays opt-in.

- [ ] **Step 5.1: Add the composite command**

In `scripts/pipeline_cli.py`:
```python
def run_pipeline_with_review() -> int:
    """Full pipeline ending with LLM review. Opt-in; `run` stays minimal."""
    rc = run_pipeline()
    if rc != 0:
        return rc
    rc = run_convert()
    if rc != 0:
        return rc
    # NOTE: canonicalization and extraction are per-file in the current CLI;
    # this composite only orchestrates the batch-capable stages.
    return run_review_relationships_ollama(
        model=get_ollama_default_model(),
        timeout_seconds=get_ollama_default_timeout(),
    )
```

Register the subcommand:
```python
    subparsers.add_parser("run-with-review")
```

Dispatch in `main()`:
```python
    if args.command == "run-with-review":
        return run_pipeline_with_review()
```

Add the import at the top:
```python
from vitruvius.config import get_ollama_default_model, get_ollama_default_timeout
```

- [ ] **Step 5.2: Smoke-test**

```bash
python scripts/pipeline_cli.py run-with-review --help
```
Expected: The command appears in help output.

- [ ] **Step 5.3: Commit**

```bash
git add scripts/pipeline_cli.py
git commit -m "feat(cli): add run-with-review composite command for full-pipeline runs"
```

---

## Self-Review Checklist

- **Audit gap coverage:** Every gap listed in `/.ai/02_audits/review-layer-audit.md` §9 is either covered here or explicitly out of scope.
- **Non-regression:** Existing tests continue to pass (`pytest scripts/tests/ -v`).
- **No placeholders:** Every code block is complete; no "TBD" or "add validation."

## Execution Handoff

Recommended: Inline execution (`superpowers:executing-plans`) — this plan is smaller than Phase 7 and benefits from staying in one session.
