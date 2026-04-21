---
task: ollama-review-runtime-wiring
phase: "03"
created: 2026-04-21
author: PLANNER
supersedes: null
status: ACCEPTED
---

# Research Pack — Ollama Review Runtime Wiring

## 01 — Discover

### Task surface

- Primary runtime module: `scripts/vitruvius/ollama_review.py`
- Live CLI entrypoint surface: `scripts/pipeline_cli.py`
- Dataset-pipeline integration surface: `scripts/vitruvius/dataset_pipeline.py`
- Existing state/log context: `.ai/10_state/active_context.md`, `.ai/00_system/pipeline-overview.md`

### Existing documentation touching this surface

- `.ai/00_system/pipeline-overview.md`
- `.ai/00_system/architecture.md`
- `.ai/02_audits/2026-04-16_architecture-and-boundary-audit.md`
- `.ai/02_audits/review-layer-audit.md`
- `.ai/10_state/decisions.md`

## 02 — Baseline

### Operational baseline before edits

- Tier-1 review exists and is callable through `review-relationships-ollama`.
- Documentation already downgrades stateful registry wiring from “live default” to “shipped infrastructure / follow-on wiring”.
- No code change has yet been made in this lane.

## 03 — Evidence gathered so far

### Code graph / impact evidence

- `code-review-graph_get_minimal_context_tool(...)` summary: repo-wide planning context is stable enough to continue.
- `code-review-graph_get_impact_radius_tool(...)` on likely runtime files reports **high blast radius** (`89` impacted files within two hops), so implementation must remain narrow and validation-heavy.

### Repo documentation evidence

1. `.ai/00_system/pipeline-overview.md`
   - states that the stateful registry infrastructure ships, but `review_with_cache()` is still a follow-on wiring path rather than the default live review loop.

2. `.ai/10_state/decisions.md`
   - records:
     - `select_review_model()` as a shipped flag-gated hook
     - `review_with_cache()` as a shipped flag-gated hook
   - confirms these helpers exist as infrastructure, not necessarily as the live default runtime path.

3. `.ai/02_audits/2026-04-16_architecture-and-boundary-audit.md`
   - flags `_call_llm()` in `ollama_review.py` as a `NotImplementedError` path in the cache-wrapper flow and describes the stateful cache boundary as present but not clearly wired into the live review loop.

4. `.ai/02_audits/review-layer-audit.md`
   - documents the Tier-1 review surface as primary and notes runtime/default-path ambiguity that must be checked directly in code.

## 04 — Working hypotheses to verify in audit

1. The production review loop still calls the direct live review path instead of `review_with_cache(...)`.
2. `_call_llm()` is not yet implemented as the production adapter required by `review_with_cache(...)`.
3. `select_review_model()` may exist and be tested, but still not drive the live model-selection path.
4. The narrowest safe validation path will likely begin with review-layer unit tests before CLI-connected tests.

## 05 — Open questions pending active code search

- Exact production call site(s) where the live review loop bypasses `review_with_cache(...)`
- Whether `dataset_pipeline.py` and CLI flow share the same internal review call path
- Which tests already assert cache/routing behavior strongly enough to guard a narrow change
- Whether feature-flag semantics require preserving the direct live path as fallback

## 06 — Next required artifact

- `.ai/02_audits/ollama-review-runtime-wiring-audit.md`
