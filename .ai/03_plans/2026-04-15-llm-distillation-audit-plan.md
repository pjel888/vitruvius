---
plan_id: llm-reviewer-distillation-audit
phase: meta
title: "LLM Reviewer Distillation Audit (low-spec investigation)"
status: active
priority: high
sprint: "Sprint DISTILL-1"
version: 1.0.0
plan_type: audit_then_conditional_implementation
created: 2026-04-15
last_updated: 2026-04-15
owner: Senior Systems Architect
prerequisites:
  - Sprint R closed (tag `sprint-r-closed`) — Stream Y4 stateful verdict cache exists and holds historical review decisions
  - Low-spec directive from user: "run Vitruvius on even a low spec machine"
related_plans:
  - ../09_archive/plans/2026-04-15-rust-pdf-audit-plan.md (AD-033 pattern reference)
  - ../09_archive/plans/per-layer-embeddings-agentic-upgrade-plan.md (Sprint R — source of the verdict cache)
---

# LLM Reviewer Distillation Audit

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Decide — with measured evidence — whether a small classical ML classifier (scikit-learn `GradientBoostingClassifier` or `lightgbm`) trained on historical LLM review verdicts can handle **60-80% of relationship-review decisions without calling Ollama at all**, freeing the ~4 GB of RAM the local LLM holds while warm. The Tier-1 LLM stays as the adjudicator on uncertain cases (gated by conformal prediction), so quality doesn't regress.

**Architecture:** Three evaluation phases:

1. **Data readiness audit** — inspect the Sprint R Y4 stateful verdict cache (`StatefulReviewRegistry` / `RocksDBStatefulReviewRegistry`). Count verdicts, check label balance, extract candidate features (source_hash → candidate text shape, model_version, self_confidence, verdict). Decide whether the corpus is large enough to train a useful classifier.
2. **Train + test a classical model** — train a `GradientBoostingClassifier` (stdlib-ish — scikit-learn is 50 MB with numpy) on 80% of the verdict corpus, test on 20%. Record accuracy, F1, and the "high-confidence subset" that would bypass the LLM.
3. **Decision gate** — GO if the student model achieves ≥85% accuracy AND the high-confidence subset covers ≥60% of decisions AND the model + inference footprint is <100 MB. DEFER otherwise.

**Tech Stack:**
- `scikit-learn` — check if installed; if not, audit the install cost vs benefit. A single `GradientBoostingClassifier` at 100 estimators runs in <20 MB RAM for inference and serializes to <10 MB on disk.
- `lightgbm` — secondary candidate if scikit-learn's implementation is slow on our workload. Smaller model files, faster training. Pure Python install, no native CUDA needed.
- Existing Sprint R `StatefulReviewRegistry` — source of historical verdicts. Keys on `(source_hash, relationship_hash, model_version)` → `(verdict, self_confidence, created_utc)`.
- Existing Sprint Q W2 `pre_review_filter.py` — the NB prefilter is the closest thing we have to a student model today. The distilled model is its sophisticated cousin.

---

## Scope & Non-Goals

### In scope (audit only)

1. **Task 1** — Verdict cache inspection + corpus count. Read every verdict in the Sprint R Y4 stateful registry, report the count, label balance, and covered `model_version` values. If the cache has <50 verdicts, the audit auto-emits `DEFER_NO_DATA` and writes AD-035 explaining that we need to run more corpus through the LLM before distillation is meaningful.
2. **Task 2** — Feature extraction from verdicts. For each verdict, synthesize a small feature vector: `[candidate_text_length, endpoint_type_pair_hash, self_confidence, model_version_index, hour_of_day]`. Avoid using the candidate text itself as a feature (no embedding requirement at audit time — keep it classical).
3. **Task 3** — Train + test a `GradientBoostingClassifier` with 80/20 split. Record accuracy, precision, recall, F1, high-confidence coverage (percent of predictions with max-class-prob ≥ 0.95).
4. **Task 4** — Decision gate + AD-035. Emit `GO` / `DEFER` / `NO_GO` based on measured numbers against pre-committed thresholds. Archive this plan.

### Out of scope

- **Actual wiring of the student model into `ollama_review.py`.** That's a separate Tranche 3-equivalent implementation plan that this audit either unblocks or doesn't.
- **Neural student models.** GBT/GBM are classical and sufficient at our scale. A neural student would add ~500 MB of inference overhead, defeating the point.
- **Active learning loop.** Deferred — Sprint D Stream J already had this queued.
- **Cross-model distillation** (learn from multiple LLM backends). The Sprint R Y4 registry already scopes by `model_version`, so we can train a per-model student if needed.

---

## File Structure

### New files

| Path | Purpose |
|---|---|
| `scripts/vitruvius/bench/distillation_audit.py` | Inspection + feature extraction + train/test harness |
| `scripts/tests/test_distillation_audit.py` | Smoke test (gated on scikit-learn availability + non-empty verdict cache) |
| `.ai/10_state/audit_distillation_2026-04-15.json` | Audit output with decision gate |

### Modified files

| Path | Reason |
|---|---|
| `.ai/10_state/decisions.md` | AD-035 |
| `.ai/03_plans/INDEX.md` | Add row |

---

## Pre-Audit Ground Truth

- **Current LLM RAM cost:** Ollama runs `gemma4:e4b` at INT4 → ~4 GB resident when warm. Can be unloaded, but then the next call pays cold-start latency.
- **Current verdict cache size:** unknown; Task 1 is the first audit step. Sprint R Y4 ships the infrastructure but the cache may be empty in the current session's working directory.
- **Target decision gate:**
  - `GO` — accuracy ≥ 0.85 AND high-confidence coverage ≥ 60% AND model file < 10 MB
  - `DEFER` — accuracy ≥ 0.75 but coverage < 60% (the model is learning but needs more data or more features)
  - `DEFER_NO_DATA` — verdict cache has < 50 usable records (sparse-data auto-defer)
  - `NO_GO` — accuracy < 0.75 (classical ML can't learn the LLM's decisions at the feature set we're providing; distillation isn't the right pattern for this workload)

---

## Tasks (condensed — full TDD expansion follows the Rust-PDF-audit plan pattern)

### Task 1 — Corpus inspection

Write `scripts/vitruvius/bench/distillation_audit.py` with `inspect_verdict_cache(db_path)` that opens the stateful registry (via `make_stateful_registry` factory), iterates all keys, returns a `CorpusInspectionResult` dataclass with: `total_verdicts`, `unique_source_hashes`, `unique_model_versions`, `label_distribution: dict[verdict, count]`, `date_range: (oldest, newest)`, `verdict_cache_is_empty: bool`.

Emit the result to `.ai/10_state/audit_distillation_2026-04-15.json::corpus_inspection`.

**Early exit:** if `total_verdicts < 50`, write `recommendation: "DEFER_NO_DATA"` and STOP. No point training on 5 examples.

### Task 2 — Feature extraction

Extend `distillation_audit.py` with `extract_features(verdicts) -> (X, y)` that produces a numpy array of per-verdict feature vectors. Features: `[candidate_length_scaled, endpoint_type_pair_onehot, self_confidence, model_version_index, created_hour_of_day]`.

Document in the plan exactly what counts as "candidate text" and how we derive it from the verdict's `source_hash` + `relationship_hash` — this is the trickiest part because the Sprint R registry stores the verdict *output*, not the candidate *input*. If the full candidate text isn't reconstructable from the cache alone, fall back to a feature vector that uses only the confidence, hour-of-day, and model version — and document the quality limitation clearly.

### Task 3 — Train + test

Import `scikit-learn` (auto-skip test if not installed). Check `pip show scikit-learn` first; if not installed, run `pip install scikit-learn` inside the task (~50 MB disk, ~100 MB intermediate download). STOP if disk headroom < 1 GB.

```python
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
clf = GradientBoostingClassifier(n_estimators=100, max_depth=3)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
y_proba = clf.predict_proba(X_test)
max_proba = y_proba.max(axis=1)

accuracy = accuracy_score(y_test, y_pred)
high_conf_mask = max_proba >= 0.95
high_conf_coverage = high_conf_mask.mean()
report = classification_report(y_test, y_pred, output_dict=True)
```

Record accuracy, per-class F1, high_conf_coverage, serialized model size (via `joblib.dump(clf, fp)` + `os.path.getsize`).

### Task 4 — Decision gate + AD-035

Apply the thresholds from Pre-Audit Ground Truth. Write `decision_gate.recommendation` into the JSON. Write AD-035 with the measured numbers + the recommended next step (conditional implementation plan for ship, or hold for more data).

---

## Execution Handoff

Plan saved. Executable when user approves. This audit is fast (~10 min end-to-end) once scikit-learn is available. Output feeds a conditional implementation plan that would ship the student model behind a feature flag.
