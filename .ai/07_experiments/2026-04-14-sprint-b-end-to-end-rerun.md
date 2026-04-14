# Experiment — Sprint B End-to-End Rerun on PD 1096

> **Date:** 2026-04-14
> **Branch:** `feat/phase-7-promotion-governance`
> **Motivation:** Answer the Sprint B question — *"Did Phase 1C centralized normalization reduce the 82% rejection rate at the review layer?"*
> **Bottom line:** **Inconclusive on Phase 1C in isolation.** The experiment had two confounders (different input AND different review model). The rejection rate dropped from 82.6% to 69.6%, but most of that is attributable to the model change, not to normalization. Three additional relationships were promoted as a side-effect.

---

## 1. Setup

| Variable | Baseline (Sprint A) | New run (Sprint B experiment) |
|---|---|---|
| **Input markdown** | `001-Laws/raw_markdown/PD-1096/PD 1096 - National Building Code.md` | `001-Laws/refined_markdown/PD-1096/PD 1096 - National Building Code.md` (Phase 1C refined) |
| **Extraction command** | `extract-relationships-sections-one` | `extract-relationships-sections-one` (same) |
| **Review command** | `review-relationships-ollama` | `review-relationships-ollama --model gemma4:e4b` |
| **Review model** | `gemma4:31b` | `gemma4:e4b` (smaller, 4B params, ~9.6 GB) |
| **Promotion threshold** | `confidence >= 0.90` | `confidence >= 0.90` (same) |

**Confounder alert:** we changed both input and model. Cannot cleanly attribute shifts to Phase 1C alone. `gemma4:31b` was not available in the local Ollama; pulling 31B would have taken hours and ~62 GB.

## 2. Extraction delta

Both runs produced **23 candidates** over the same 13 unique section IDs. But only **6 out of 23 triplets** overlap between the two runs — 17 were "lost" and 17 were "gained".

### Overlap (present in both)
```
concept-light-and-ventilation --[defines]--> concept-stairs
concept-light-and-ventilation --[depends_on]--> concept-stairs
concept-occupancy-classification --[defines]--> concept-certificate-of-occupancy
law-national-building-code-of-the-philippines --[governs]--> concept-building-permit
law-national-building-code-of-the-philippines --[governs]--> concept-floor-area
law-national-building-code-of-the-philippines --[governs]--> concept-stairs
```

### Only in OLD (raw-extraction, 17)
A cluster of 12 `concept-floor-area → [5 predicates] → concept-{occupancy-separation | yards | lot-occupancy}` and 5 `concept-occupancy-classification → [5 predicates] → concept-mixed-occupancy`.

### Only in NEW (refined-extraction, 17)
A cluster of 5 `concept-occupancy-separation → [5 predicates] → concept-occupancy-classification`, 5 `concept-stairs → [5 predicates] → concept-fire-resistive-construction`, 5 `concept-yards → [5 predicates] → concept-floor-area`, and 2 `concept-light-and-ventilation → [2 predicates] → concept-yards`.

### Interpretation
The regex-based section extractor in `relationships_sections.py` matches concept pairs within a sliding line window. **Tier A normalization changed the paragraph boundaries** (via `strip-control-chars` removing interior nulls and `collapse-consecutive-blank-lines` reducing blank-line runs). That shifted which concepts appeared inside each window, producing a different — but equally arbitrary — candidate set.

**This is not a Phase 1C defect. It is an exposure of how fragile the regex-based extractor is under small text perturbations.** The regex extractor produces one candidate per predicate per endpoint pair it sees, giving the reviewer 5 variants of the same edge to choose from. This is noise the review layer has to filter out.

**Implication for the roadmap:** Phase 5E (LLM-assisted candidate generation) or a full replacement of regex extraction is the real fix. Phase 1C is a prerequisite, not a sufficient cure.

**Regression worth noting:** Two of the three Sprint A high-confidence keeps (`concept-occupancy-classification → [depends_on|affects] → concept-mixed-occupancy`) are **not present** in the refined extraction. They remain as canonical files on disk (because promotion is additive, not retroactive), but their underlying evidence was reshuffled by normalization.

## 3. Review delta

| Metric | Baseline (gemma4:31b, raw) | New (gemma4:e4b, refined) | Δ |
|---|---|---|---|
| Total candidates | 23 | 23 | 0 |
| `keep` | 3 | 6 | **+3** |
| `reject` | 19 | 16 | −3 |
| `review_further` | 1 | 1 | 0 |
| **Rejection rate** | **82.6%** | **69.6%** | **−13 pts** |
| `high_confidence_keep` (≥0.90) | 3 | 6 | **+3** |

### Baseline high-confidence keeps (gemma4:31b)
```
concept-occupancy-classification --[affects]--> concept-mixed-occupancy     (conf 0.9)
concept-occupancy-classification --[depends_on]--> concept-mixed-occupancy  (conf 0.9)
law-nbc --[governs]--> concept-building-permit                              (conf 1.0)
```

### New run high-confidence keeps (gemma4:e4b)
```
concept-occupancy-classification --[defines]--> concept-certificate-of-occupancy  (conf 0.9)
concept-occupancy-separation --[affects]--> concept-occupancy-classification      (conf 0.9)
concept-occupancy-separation --[depends_on]--> concept-occupancy-classification   (conf 0.9)
concept-occupancy-separation --[limits]--> concept-occupancy-classification       (conf 0.9)
concept-occupancy-separation --[requires]--> concept-occupancy-classification     (conf 0.9)
law-nbc --[governs]--> concept-building-permit                                    (conf 0.9)
```

### Interpretation
The rejection rate dropped, but **four of the six new high-confidence keeps are variants of the same edge** (`concept-occupancy-separation → [4 predicates] → concept-occupancy-classification`). A well-calibrated larger model would have kept at most one of those four — the correct predicate — and rejected the other three. The `gemma4:e4b` 4B-parameter model is less conservative and anchors on the endpoints, saying "keep" to every predicate variant.

**Attribution estimate (author's best guess, not rigorously measured):**
- Model change (`31b` → `e4b`): −10 to −12 percentage points (e4b is less conservative).
- Input change (raw → refined): −1 to −3 percentage points (Phase 1C's contribution; probably positive but small).
- The honest experiment requires re-running with the same model. That experiment is blocked on pulling `gemma4:31b` locally.

## 4. Promotion outcome

Running `promote --execute` against the 6 new high-confidence keeps:

```
total_candidates: 6
created: 3      (new records)
skipped: 1      (law-nbc → governs → concept-building-permit already exists; byte-identical)
rejected: 2     (Rule 7 compatibility failures — see below)
```

### Rule 7 rejections
- `concept-occupancy-classification → defines → concept-certificate-of-occupancy`: `defines` requires `subject_type == source`, not `concept`. **The Phase 7 governance gate caught this.** Smaller review models often produce such type errors.
- `concept-occupancy-separation → limits → concept-occupancy-classification`: `limits` requires `subject_type ∈ {source, section}`, not `concept`. Same story.

### Created records (3 new)
- `rel-concept-occupancy-separation-affects-concept-occupancy-classification`
- `rel-concept-occupancy-separation-depends-on-concept-occupancy-classification`
- `rel-concept-occupancy-separation-requires-concept-occupancy-classification`

These all point at the same edge with three different predicates — the reviewer couldn't distinguish which one fits the evidence best. A well-calibrated reviewer would have picked one (likely `depends_on` or `affects`) and rejected the other two. Phase 6B second-pass adjudication is designed to resolve exactly this kind of same-endpoint-multiple-predicate ambiguity.

### Canonical layer state after the experiment
```
003_Canonical-Knowledge-Layer/shared/relationships/
├── occupancy-governs-fire-requirements.md                                            (hand-curated draft)
├── rel-concept-occupancy-classification-affects-concept-mixed-occupancy.md           (Sprint A, stale evidence)
├── rel-concept-occupancy-classification-depends-on-concept-mixed-occupancy.md        (Sprint A, stale evidence)
├── rel-concept-occupancy-separation-affects-concept-occupancy-classification.md      (this experiment)
├── rel-concept-occupancy-separation-depends-on-concept-occupancy-classification.md   (this experiment)
├── rel-concept-occupancy-separation-requires-concept-occupancy-classification.md     (this experiment)
└── rel-law-national-building-code-of-the-philippines-governs-concept-building-permit.md  (both sprints)
```

**Total promoted records: 6. Hand-curated: 1. Grand total: 7.**

## 5. What worked end-to-end

- `run-with-review` composite command would have run the whole pipeline in one shot (we ran the stages individually here because Ollama needed a specific model flag).
- Tier A normalization idempotency held on real data (output hash unchanged across runs).
- Phase 7 Promotion Validator caught 2 of 6 candidates at Rule 7 — exactly the kind of small-model typing error we expected.
- The canonical layer grew without any manual file editing: review → validator → writer → audit log, fully automated.

## 6. What surprised me

1. **Regex extractor is paragraph-boundary-sensitive.** 17/23 candidates flipped under what looked like a "trivial" text cleanup. The lesson: the regex extractor is a floor, not a ceiling, and replacing it (Phase 5E) should be considered sooner than the current Sprint-C roadmap suggests.
2. **Smaller models are less reliable at predicate selection.** `gemma4:e4b` kept 4 different predicates for the same endpoint pair. This is exactly what Phase 6B second-pass review is meant to catch, and it's a strong argument for running 6B next.
3. **Phase 7 governance gate works as a typing firewall.** Without Rule 7, we would have promoted invalid `defines` and `limits` records.

## 7. Recommendations

1. **Run Phase 6B next.** The single biggest quality lever is two-stage adjudication. It directly addresses the "4 predicates for the same edge" issue observed here.
2. **Phase 5E LLM-assisted extraction is more urgent than the roadmap currently indicates.** The regex extractor's instability under normalization is a latent risk for every future rerun.
3. **Pull `gemma4:31b` locally at some point.** Without a consistent baseline model, quality comparisons are muddied. `gemma4:e4b` is fine for CI and quick iteration, not for production review.
4. **Consider a `retire-stale-records` command.** Two Sprint A records now have orphaned underlying evidence. They aren't wrong, just stale. A retirement command keyed on "is this candidate in the latest review output?" would close that loop.
5. **Do NOT interpret 82.6% → 69.6% as a Phase 1C win.** It is mostly a model-swap effect. The honest Phase 1C number requires a same-model A/B.

## 8. Artifacts

- New review report: `006_System-Manifests/runs/latest_relationship_review_ollama.json`
- New high-confidence input: `006_System-Manifests/runs/latest_relationship_review_high_confidence.json`
- New promotion batch ID: `20260414T042840Z_befa550c`
- Audit log: `006_System-Manifests/runs/latest_promotion_audit.log`
- Baselines (snapshotted to `/tmp/baseline_*.json` — not committed)

## 9. Test suite status
81/81 passing after the experiment. No regressions from the rerun.
