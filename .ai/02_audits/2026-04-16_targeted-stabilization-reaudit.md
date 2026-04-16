---
task: vitruvius-targeted-stabilization-reaudit
phase: 04
created: 2026-04-16
author: AUDITOR
supersedes: null
status: ACCEPTED
---

# 2026-04-16 Targeted Stabilization Re-Audit

## 1. Summary

PASS 2 **materially improved** Vitruvius. The fixes were real: silent graph-integrity failure is now loud, query provenance is evidence-backed, Rust static gates are green again, and the live state/docs are much more truthful than they were in PASS 1.

Confidence level: **moderate-high** for the touched surfaces.

However, the system is **not yet stable enough for broad new feature work** because one previously-high issue remains unresolved at the underlying data layer: the duplicate canonical source ID still exists, and `build-graph` still fails on it. PASS 2 changed this from a silent false-green to an explicit blocking error, which is a good fix — but it is not the same thing as eliminating the root problem.

## 2. Fix Verification Results

### Issue: Fresh runtime truth was not centralized across state/docs
- **Expected fix:** live state docs, roadmap snapshots, and README should reflect current `main`-branch reality rather than the stale feature-branch snapshot.
- **Actual behavior:** mostly fixed.
- **Evidence:**
  - `/.ai/01_roadmap/current-phase.md` now states `main`, PASS 2 completed with caveats, and names the duplicate-ID caveat explicitly.
  - `/.ai/10_state/active_context.md` now reports `main`, Python `1569 passed / 1 skipped`, TypeScript `21 passed`, Rust `33` passing, Rust static gates green, and the duplicate-ID caveat.
  - `README.md` now reports the same 2026-04-16 validation baseline.
  - `/.ai/00_system/principles.md` updates the monotonic test baseline to `1569 passed / 1 skipped`.
- **Result:** **PARTIAL**
- **Why partial:** one active governance spec still points to `.ai/10_state/current-phase.md` / `.ai/10_state/milestone-tracker.md`, and some non-authoritative archival artifacts still carry the old path.

### Issue: Path authority conflict for `current-phase` / `milestone-tracker`
- **Expected fix:** the live authority stack should consistently use `/.ai/01_roadmap/current-phase.md` and `/.ai/01_roadmap/milestone-tracker.md`.
- **Actual behavior:** fixed in the live authority stack, but not everywhere.
- **Evidence:**
  - `AGENTS.md`, `current-phase.md`, and `master-roadmap.md` all point to `/.ai/01_roadmap/*`.
  - Local verification confirmed `.ai/10_state/current-phase.md` and `.ai/10_state/milestone-tracker.md` do not exist.
  - `/.ai/06_specs/GOVERNANCE/02_DOCUMENT_AUTHORITY_AND_UPDATE_POLICY.md` still references the stale `.ai/10_state/*` paths.
- **Result:** **PARTIAL**

### Issue: Duplicate canonical IDs entered the graph silently
- **Expected fix:** graph integrity should detect duplicate node IDs instead of passing silently.
- **Actual behavior:** fixed.
- **Evidence:**
  - `python3 scripts/pipeline_cli.py build-graph` now exits non-zero and reports:
    - `code: duplicate_node_id`
    - `node_id: irr-implementing-rules-and-regulations-of-the-national-building-code`
  - `scripts/tests/test_graph_integrity.py` includes a duplicate-node failure test.
- **Result:** **FIXED**
- **Important caveat:** the *detection* is fixed, but the *underlying duplicate canonical source ID* remains unresolved.

### Issue: Query citations were synthetic / placeholder-based
- **Expected fix:** query citations should come from real relationship evidence.
- **Actual behavior:** fixed.
- **Evidence:**
  - `python3 scripts/pipeline_cli.py query-structured --function what_governs --subject concept-means-of-egress`
  - `python3 scripts/pipeline_cli.py query "What governs means of egress?"`
  - both now show:
    - real `source_section_id` (`section-irr-general`)
    - real `evidence_snippet`
    - reviewer-confidence-based `0.95`
  - `query-graph` now returns edge payloads carrying `evidence_source_id`, `evidence_source_section_id`, `evidence_snippet`, and `reviewer_confidence`.
- **Result:** **FIXED**

### Issue: Query confidence semantics were shallow/binary
- **Expected fix:** confidence should reflect evidence quality where available.
- **Actual behavior:** mostly fixed.
- **Evidence:**
  - query outputs now use reviewer confidence when relationship evidence provides it.
  - targeted query aggregate tests pass.
- **Result:** **FIXED** for evidence-bearing paths
- **Caveat:** legacy/no-evidence paths still fall back to simpler confidence behavior.

### Issue: Query route could imply stronger NL behavior than actually existed
- **Expected fix:** user-facing query behavior should be truthful.
- **Actual behavior:** improved but still limited.
- **Evidence:**
  - query output is now provenance-faithful and exposes the actual structured query trace.
  - `scripts/vitruvius/query/nl_translator.py` still defaults to regex fallback unless an LLM caller is injected.
- **Result:** **PARTIAL**

### Issue: Advanced-boundary claims were overstated
- **Expected fix:** prove live runtime callers or downgrade the wording.
- **Actual behavior:** partially fixed.
- **Evidence:**
  - `pipeline-overview.md` now downgrades the stateful registry from live-default review path to shipped infrastructure / follow-on wiring.
  - `pipeline-overview.md` and `architecture.md` now downgrade the Datalog bridge to experimental / scaffolding wording where live audited wiring was absent.
  - `README.md` now labels Wasm/browser/React Three Fiber as experimental/directional rather than current shipped UI.
- **Result:** **PARTIAL**
- **Why partial:** some active governance/reference docs still contain stale or overstated wording, and no new runtime proof was added for the unresolved advanced claims.

### Issue: Phase 1B parallelism was overstated
- **Expected fix:** docs should stop claiming shipped `ProcessPoolExecutor` fan-out if the implementation is sequential.
- **Actual behavior:** only partly fixed.
- **Evidence:**
  - `milestone-tracker.md` top section now says the scaling/governance slice is partial and the shipped API is sequential compatibility-only.
  - `master-roadmap.md` phase deliverable wording now describes a batch/resource-allocation API with a future upgrade path.
  - But one lower milestone bullet still says `ProcessPoolExecutor` parallelism shipped.
- **Result:** **PARTIAL**

### Issue: Rust static hygiene was red
- **Expected fix:** fmt + clippy + Rust tests should be green.
- **Actual behavior:** fixed.
- **Evidence:**
  - `cargo fmt --all --check` passes in `engine_rs` and `datalog_rs`
  - `cargo clippy --workspace --all-targets -- -D warnings` passes in both Rust roots
  - `cargo test --quiet` passes in both Rust roots
- **Result:** **FIXED**

## 3. Regression Findings

No new functional regressions were found in the touched surfaces.

### Regression check results
- Python suite: `1569 passed, 1 skipped`
- TypeScript suite: `21 passed`
- Rust unit tests: `33 passed`
- Rust fmt/clippy: green
- Targeted graph/query suites: green
- `pipeline_cli.py run`: clean on the current raw corpus baseline (`350` files, `0` new, `0` changed, `0` missing)

### Non-regression caveat
- `build-graph` is now red. This is **not** a new accidental regression; it is the intentional exposure of a pre-existing silent integrity defect.

## 4. Subsystem Health

### Frontend
- **Status:** N/A / no live frontend to re-audit.
- **Evidence:** no `web/`, `app/`, `frontend/`, or active browser/dashboard route tree exists in the repo.
- **Health:** truthful enough after PASS 2 doc cleanup, but future/browser language still requires discipline.

### Backend
- **Status:** improved.
- **Health:** graph/query backend is more trustworthy, but not fully healthy because the duplicate canonical source ID still blocks a green integrity pass.

### Routes
- **Status:** CLI/operator routes only.
- **Health:** improved on the query side; query/structured/query-graph now behave more truthfully.

### Admin
- **Status:** N/A / no live admin surface.

### State management
- **Status:** improved.
- **Health:** live authority stack is much closer to reality, but one active governance spec remains stale and one milestone bullet remains misleading.

### Compute layer
- **Status:** improved.
- **Health:** Python↔Rust touched surfaces are stable; Rust static and dynamic checks are green again.

## 5. Boundary Integrity

### Python ↔ Rust
- **Status:** healthy for the touched PASS 2 surfaces.
- **Evidence:** Rust static gates and tests passed after the PASS 2 changes; no Python test regressions were introduced.

### Python ↔ API / CLI
- **Status:** improved.
- **Evidence:** CLI graph/query flows now surface real evidence and a truthful integrity error when graph identity is broken.

### UI ↔ API
- **Status:** not applicable.
- **Evidence:** no live UI/API app boundary exists in the current repo.

### Data-flow correctness
- **Status:** improved.
- **Evidence:** relationship evidence now flows into graph edges, then into query citations, then into user-visible CLI output.

## 6. Performance Observations

- No performance regression was observed in the touched surfaces.
- No new benchmark claim was introduced in PASS 2.
- The raw-layer pipeline baseline is cleaner than PASS 1 (`0` new / `0` changed / `0` missing files after `pipeline_cli.py run`).
- No suspicious slowdown was observed in graph/query or Rust validation paths.

## 7. Docs and State Accuracy

### Pre-audit conflict note
- The user brief required `.ai/10_state/current-phase.md` and `.ai/10_state/milestone-tracker.md`, but those files do not exist.
- Following the repo’s actual authority stack, this re-audit used `/.ai/01_roadmap/current-phase.md` and `/.ai/01_roadmap/milestone-tracker.md` instead.
- This path conflict is itself part of the remaining docs/state risk surface.

### Verified accurate
- `/.ai/01_roadmap/current-phase.md`
- `/.ai/10_state/active_context.md`
- `README.md` validation snapshot sections
- `/.ai/01_roadmap/master-roadmap.md` historical/live distinction
- `/.ai/00_system/principles.md` test baseline

### Still mismatched or stale
- `/.ai/06_specs/GOVERNANCE/02_DOCUMENT_AUTHORITY_AND_UPDATE_POLICY.md` still references the nonexistent `.ai/10_state/current-phase.md` and `.ai/10_state/milestone-tracker.md`
- `/.ai/01_roadmap/milestone-tracker.md` still contains one stale `ProcessPoolExecutor` “shipped” bullet lower in the file
- Non-authoritative archival/research artifacts still carry the old `.ai/10_state/*` path references

## 8. Remaining Issues

1. **Duplicate canonical source ID remains unresolved at the corpus layer**
   - Now surfaced correctly
   - Still blocks a green `build-graph`
   - Needs a dedicated migration/curation decision

2. **NL query routing remains only partially fixed**
   - Output is more truthful
   - Translator is still regex-fallback based without injected LLM routing

3. **Some secondary docs remain stale**
   - Not enough to invalidate the live authority stack
   - Still enough to block a clean “fully truthful” claim

## 9. Critical Risks (if any)

### Must-fix before proceeding broadly
- The duplicate canonical source ID is still a high-severity unresolved issue.
- As long as `build-graph` fails on live canonical data, graph-adjacent feature work remains risky.

## 10. Final Verdict

**NOT READY — REQUIRES ADDITIONAL FIX PASS**

### Why
The PASS 2 fixes **did work** in the important sense:
- they restored truthfulness in the live state/docs stack,
- they replaced fake query evidence with real provenance,
- they restored Rust hygiene,
- and they turned a silent graph-integrity defect into an explicit blocking error.

But the system is **not yet stable enough to move forward with new feature work in general** because:
1. the underlying duplicate canonical source ID still exists,
2. graph integrity is still red on the live corpus,
3. the query route is still only partially “fixed” at the NL translation layer,
4. and a few active/secondary docs still lag reality.

### Direct answer
**The audit fixes mostly worked, but they did not finish stabilization. Vitruvius is safer and more truthful now, but it still needs one additional focused fix pass before it is truly ready for new feature development.**

## Follow-On Resolution Note — 2026-04-16
- The additional focused fix pass was completed after this re-audit.
- The duplicate live IRR source page was removed while preserving the canonical ID on the retained page, and `build-graph` now passes with warnings only.
- See `.ai/03_plans/2026-04-16_duplicate-canonical-source-id-remediation-plan.md` and `.ai/05_logs/2026-04-16_duplicate-canonical-source-id-remediation-validation.md`.
