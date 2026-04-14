---
plan_id: phase-3-concept-enrichment
phase: 3C
title: Concept Enrichment — Placeholder to Knowledge Node
status: planned
priority: medium
sprint: "Post-Sprint-C (after Phase 2 restoration)"
version: 1.0.0
plan_type: implementation_design_spec
created: 2026-04-14
last_updated: 2026-04-14
owner: Senior Systems Architect
prerequisites:
  - Phase 2 canonicalizer restoration (structured sections)
  - Phase 1C normalization (refined markdown is enrichment input)
dependencies:
  - .ai/06_specs/concept-schema.md
  - scripts/vitruvius/concepts.py (existing placeholder generator)
  - 003_Canonical-Knowledge-Layer/shared/concepts/ (20 placeholders)
related_plans:
  - phase-2-canonicalizer-restoration-plan.md
unblocks:
  - Phase 5E LLM-assisted relationship extraction (needs real definitions)
  - Higher Phase 6A confidence on concept-to-concept edges
---

# Phase 3C — Concept Enrichment Implementation Plan

**Goal:** Move all 20 seeded PD 1096 concepts from `canonical_status: placeholder` to `canonical_status: enriched` by extracting definitions from source sections, populating the `regulatory_basis` field, filling an `aliases` registry, and adding `related_concepts` cross-references.

**Architecture:** Three new modules build the enrichment pipeline: (1) `concept_definitions.py` extracts candidate definitions from canonical source bodies using regex anchors ("...means...", "...shall mean...", "...refers to..."); (2) `concept_aliases.py` mines alias candidates from document headers and body text; (3) `concepts.py` is extended with `enrich_concept_one` and `enrich_concepts` batch mode that compose the first two. Each enrichment call is **additive** — it never overwrites manually curated content.

**Tech Stack:** Python stdlib only for text extraction. PyYAML for frontmatter. Optional: local LLM via existing `ollama_review.py` pattern for Tier-2 definition quality checks (deferred to a sub-task).

---

## Scope Boundary

**In scope:**
- Extracting definitions from canonical source bodies.
- Populating `regulatory_basis: [{source_id, section_id, evidence_snippet}]`.
- Populating `aliases[]` from document headers and abbreviation patterns.
- Detecting `related_concepts[]` via co-occurrence within the same section.
- Additive updates that preserve manually-edited content.
- A CLI command `enrich-concept-one` and batch `enrich-concepts`.

**Out of scope:**
- Creating new concept files (use `canonicalize-concept-one` for that).
- Machine-generated free-text descriptions beyond the evidence snippet.
- Phase 5E LLM-assisted relationship extraction (a different plan).
- Cross-document concept disambiguation / merging.

## File Structure

| Path | Change |
|---|---|
| `scripts/vitruvius/concept_definitions.py` | New — regex-anchored definition extractor |
| `scripts/vitruvius/concept_aliases.py` | New — alias and abbreviation miner |
| `scripts/vitruvius/concepts.py` | Modify — add `enrich_concept_one`, `enrich_concepts`, diff-before-write |
| `scripts/pipeline_cli.py` | Modify — register `enrich-concept-one` and `enrich-concepts` commands |
| `scripts/tests/test_concept_definitions.py` | New |
| `scripts/tests/test_concept_aliases.py` | New |
| `scripts/tests/test_concept_enrichment.py` | New — integration |

---

## Task 1: Definition Extractor

The extractor scans canonical source bodies for sentences that match definition anchors:

- `"X means Y"`
- `"X shall mean Y"`
- `"X refers to Y"`
- `"'X' is defined as Y"`
- `"X is the Y"` (weakest anchor, lowest confidence)

Each match emits a `DefinitionCandidate` with `(concept_slug, source_section_id, snippet, confidence)`.

### Data model
```python
@dataclass
class DefinitionCandidate:
    concept_slug: str      # e.g., "occupancy-classification"
    source_id: str         # e.g., "law-national-building-code-of-the-philippines"
    source_section_id: str # e.g., "sec-701"
    snippet: str           # verbatim from the source
    confidence: float      # anchor strength, 0.0–1.0
```

### Key functions
```python
def extract_definitions_from_source(source_path: Path, known_slugs: set[str]) -> list[DefinitionCandidate]:
    """Walk a canonical source file, find definition anchors, emit candidates."""

def pick_best_definition(candidates: list[DefinitionCandidate]) -> DefinitionCandidate | None:
    """Prefer higher confidence; on tie, prefer earliest section."""
```

### Confidence ladder (used by the picker)
| Anchor | Confidence |
|---|---|
| `... shall mean ...` | 0.95 |
| `... is defined as ...` | 0.93 |
| `... means ...` | 0.90 |
| `... refers to ...` | 0.85 |
| `<Term> is the ...` | 0.70 |
| `<Term> is a ...` | 0.65 |

### Test coverage (write these first)
- One match per anchor pattern.
- Multiple matches for the same concept → picker returns the highest-confidence one.
- No matches → picker returns `None`.
- Only matches concepts in `known_slugs` (avoids noise from arbitrary capitalized terms).

---

## Task 2: Alias Miner

Input: canonical source files and raw refined markdown. Output: a list of alias candidates per concept.

### Alias sources
1. **Existing frontmatter aliases** in the source file (already present for PD 1096).
2. **Abbreviation patterns** in body text: `"National Building Code (NBC)"` → `nbc` is an alias for `national-building-code`.
3. **"also known as" phrases**: `"Occupancy Classification, also known as use group"`.
4. **Definition anchor consequents**: when `extract_definitions_from_source` finds `"Building Permit means a written authorization..."`, the `Y` tail can yield noun-phrase aliases in rare cases.

### Key functions
```python
def mine_aliases_for_concept(source_text: str, concept_title: str) -> list[str]:
    """Return deduplicated, lowercased alias strings."""

def parenthetical_abbreviations(text: str) -> list[tuple[str, str]]:
    """Return [(long_form, short_form)] pairs from 'Long Form (LF)' patterns."""
```

### Validation rules
- Drop aliases that are identical to the concept slug.
- Drop single-word stopwords (`the`, `and`, `of`).
- Cap at 5 aliases per concept to prevent sprawl.

---

## Task 3: Enrichment Orchestrator

### `enrich_concept_one(concept_slug: str) -> int`
Steps:
1. Load the concept file from `003_Canonical-Knowledge-Layer/shared/concepts/<slug>.md`.
2. Parse frontmatter. If `canonical_status in {"enriched", "verified"}`, **skip** unless `--force`.
3. Walk `003_Canonical-Knowledge-Layer/shared/sources/*.md` and collect candidate definitions for the concept (Task 1).
4. Pick the best definition. If none, write the concept back with `concept_status: draft` but no body change, and return 0.
5. Mine aliases (Task 2) from the matched source.
6. Detect co-occurring concepts in the same section → `related_concepts`.
7. Render the enriched body:
   ```markdown
   # <Title>

   ## Definition
   <paragraph from best definition candidate>

   ## Regulatory Basis
   - **[<Source Title>](<source-id>)** — Section <section_id>: "<snippet>"

   ## Related Concepts
   - `concept-<other>` — <one-line co-occurrence rationale>
   ```
8. Update frontmatter: set `canonical_status: enriched`, `concept_status: enriched`, `enriched_at_utc: <now>`, `aliases: [...]`, `regulatory_basis: [...]`, `related_concepts: [...]`.
9. Use the same `should_overwrite` helper from `canonical_diff.py` (Phase 2 plan) to avoid clobbering manually-curated files.

### `enrich_concepts() -> int` (batch)
Walk every `.md` under `003_Canonical-Knowledge-Layer/shared/concepts/`, call `enrich_concept_one` for each, tally success/skip/fail counts, print a summary.

---

## Task 4: CLI Wiring

Add to `scripts/pipeline_cli.py`:
```python
    enrich_parser = subparsers.add_parser("enrich-concept-one")
    enrich_parser.add_argument("concept_slug")
    enrich_parser.add_argument("--force", action="store_true")

    subparsers.add_parser("enrich-concepts")
```

Dispatch:
```python
    if args.command == "enrich-concept-one":
        return enrich_concept_one(concept_slug=args.concept_slug, force=args.force)
    if args.command == "enrich-concepts":
        return enrich_concepts()
```

---

## Task 5: Golden Path Verification

1. Run `enrich-concepts` on the 20 seeded PD 1096 concepts.
2. Verify that at least 15/20 transition to `canonical_status: enriched`.
3. Spot-check 3 concepts by eye: the definition should read as a coherent sentence, the regulatory basis should cite a real section, and the aliases should be sane.
4. For any concepts that fail to enrich, add a note to `/.ai/10_state/known_issues.md` under RI-010 and curate manually.

## Gating Metrics
- **Enrichment rate:** ≥75% of placeholder concepts transition to enriched.
- **Regulatory basis coverage:** ≥90% of enriched concepts have ≥1 source pointer.
- **False-alias rate:** ≤5% of generated aliases are nonsense (human spot-check).
- **Protection:** 0 manually-edited files silently overwritten (measured by `canonical_diff`).

## Non-Goals
- Per `/.ai/06_specs/concept-schema.md` §11, concept merging and splitting are out of scope for this plan. They require a formal migration in `decisions.md`.
- Creating concepts that do not already exist. Use `canonicalize-concept-one` for new concepts.
- Running a local LLM on definition quality (deferred; the regex anchors are deterministic and auditable).

## Risks
| Risk | Mitigation |
|---|---|
| Regex anchors miss Filipino / code-switched text | Phase 11 adds Filipino-specific anchors when that corpus lands. |
| Definitions in IRR contradict definitions in the base law | Prefer the law (primary) over the IRR (secondary) by trust_level. |
| Free-text drift in definitions | Every definition is pinned to a verbatim evidence snippet and section_id. |

## Self-Review Checklist
- Every required field in `/.ai/06_specs/concept-schema.md` §3 + §4 is produced by the orchestrator.
- Every lifecycle rule in §3.1 is honored (placeholder → draft → enriched).
- Diff-before-write protection is shared with Phase 2 (DRY).

## Execution Handoff
Recommended: Subagent-driven. Each of the 20 concepts can be enriched independently; the batch mode is parallelizable if it becomes slow.
