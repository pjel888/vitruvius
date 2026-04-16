# Vitruvius Truth Governance and Promotion Contract

## Purpose
This document defines how Vitruvius treats candidate knowledge, reviewed outputs, provenance, confidence, and canonical promotion.

Vitruvius is not a casual content generator. Its value depends on defensible, traceable, governed truth. Therefore truth must be admitted through controlled gates rather than inferred informally.

## Core Principle
Truth is not generated.  
Truth is admitted.

## Scope
This contract applies to:
- rule ingestion
- canonicalization affecting truth-bearing content
- concept generation and enrichment
- relationship extraction
- review systems
- promotion to trusted layers
- temporal versions of truth
- provenance, evidence, and confidence metadata
- conflict and supersession logic

---

## Section 1 — Trust Levels

Vitruvius should conceptually separate at least four trust levels.

### Level 0 — Raw Evidence
Original source material. Immutable. Not trusted as structured output, but trusted as primary evidence.

Examples:
- original PDFs
- scans
- raw office documents
- survey files

### Level 1 — Processed Material
Converted or normalized material that is machine-usable but not yet trusted as canonical truth.

Examples:
- raw markdown
- OCR outputs
- parsed JSON sidecars
- refined text

### Level 2 — Candidate Knowledge
Structured outputs proposed by deterministic logic, LLM extraction, heuristics, or review systems.

Examples:
- extracted concepts
- candidate relationships
- parsed ASTs
- inferred metadata
- provisional review outputs

### Level 3 — Canonical Truth
Admitted, evidence-backed, schema-valid, provenance-preserving records approved to power trusted system behavior.

Examples:
- canonical sources
- verified concepts
- promoted relationships
- reviewed and accepted rules
- admitted temporal rule versions

### Rule
Candidate and canonical data must not be conflated.

---

## Section 2 — Truth Requirements

No truth-bearing record should exist without answering:
- What is this claim?
- Where exactly did it come from?
- Why do we believe it?
- Under what rule, review, or validation regime was it admitted?
- What is its confidence and status?
- When is it valid?
- What supersedes it, if anything?

If the system cannot answer these questions, the record is not mature enough for canonical truth.

---

## Section 3 — Required Truth Metadata

For truth-bearing records, require as applicable:
- stable ID
- source document identity
- source section or clause ID
- evidence snippet
- provenance path
- extraction method or origin
- review status
- review actor or model
- confidence score
- timestamp
- temporal validity window
- supersession reference where applicable
- schema version
- promotion batch or audit reference where applicable

### Rule
A truth-bearing record without provenance is incomplete.

---

## Section 4 — Candidate Creation Rules

Candidate knowledge may be produced by:
- deterministic extraction
- rules engines
- LLM schema-constrained extraction
- review models
- enrichment pipelines
- manual curation

### But
Candidate creation does not imply truth.

### Candidate Requirements
Candidates must:
- conform to schema
- preserve provenance
- carry status fields
- avoid silent auto-promotion
- remain separable from admitted truth

---

## Section 5 — Review and Confidence Rules

### Review Status Categories
Suggested categories:
- unreviewed
- draft
- machine-reviewed
- escalated
- human-reviewed
- accepted
- rejected
- superseded

### Confidence Policy
Confidence is a signal, not authority.

#### High Confidence
May permit lighter manual review, but should still preserve provenance and validation requirements.

#### Medium Confidence
Requires stronger review before promotion.

#### Low Confidence
Should usually remain candidate-only or be rejected.

### Rule
Confidence alone must never substitute for provenance or schema validity.

---

## Section 6 — Promotion Gates

Before any record becomes canonical truth, verify:

1. Schema validity
2. Required provenance fields present
3. Source reference valid
4. Evidence snippet present where required
5. ID policy satisfied
6. Conflict checks performed
7. Review status satisfies promotion policy
8. Confidence threshold satisfied where applicable
9. Temporal validity is coherent
10. Promotion action is logged

### Rule
Promotion is an explicit event, not an accidental byproduct of extraction.

---

## Section 7 — Promotion Logging

Every promotion event should be traceable.

### Promotion Log Should Capture
- promoted record IDs
- promotion time
- promotion batch or run reference
- actor or system performing promotion
- validation outcome
- source references
- any caveats or conflict notes

This supports:
- auditability
- rollback analysis
- dispute handling
- temporal forensics

### Dataset-Scoped Graph Truth Rule
When Vitruvius is used to prove a graph for a bounded dataset or pilot bundle:
- the graph must still be built from **canonical/promoted truth-bearing inputs**
- raw folders are only **scope anchors**, not direct graph truth
- scoped graph proofs must not silently reuse global `latest_relationship_*` or global latest graph artifacts
- if a pilot needs dataset-selected approved relationship inputs, that selection must be explicit in manifest/staging data, not hidden in code branches

Truthfulness requirement:
- a pilot graph may be **bounded**
- it may be **gated**
- but it must never pretend to be generic all-dataset support if the implementation is still tied to one pilot bundle

---

## Section 8 — Conflict Handling

Truth-bearing records can conflict.

### Common Conflict Types
- duplicate IDs
- contradictory numeric values
- overlapping temporal windows
- conflicting rule interpretations
- conflicting relationships
- source mismatch
- outdated truth not marked superseded

### Required Response
Conflicts must not be silently overwritten.

### Conflict Options
- reject new record
- supersede old record
- keep both with temporal separation
- escalate for review
- create explicit conflict record

### Rule
Conflicts must be visible.

---

## Section 9 — Supersession and Temporality

Truth changes over time. Vitruvius must represent that explicitly.

### Required Temporal Fields As Applicable
- effective start
- effective end
- supersedes reference
- superseded by reference if maintained
- version or revision identity

### Rule
Old truth should usually be preserved historically, not deleted casually.

This enables:
- retroactive compliance checks
- historical audit
- forensic analysis
- version-aware reasoning

---

## Section 10 — Truth Exposure Rules

When user-facing or downstream systems consume truth:
- expose provenance when possible
- expose uncertainty where relevant
- avoid claiming more confidence than the record justifies
- avoid hiding candidate status as if it were canonical

### Rule
Presentation must not overstate trust.

---

## Section 11 — Truth Rejection Policy

Reject or hold records that:
- lack provenance
- fail schema
- lack evidence snippet where required
- conflict without resolution
- fall below promotion threshold
- have incoherent temporality
- derive from ambiguous source segmentation
- are produced by methods not approved for the record class

### Rule
Reject by default when evidence is inadequate.

---

## Section 12 — Manual Review Triggers

Manual review should be required or strongly considered when:
- high-impact legal rules are extracted
- evidence is ambiguous
- confidence is borderline
- conflicts exist
- temporal interpretation is unclear
- promotion would materially affect compliance output
- deterministic and machine-review layers disagree

---

## Section 13 — Truth Artifact Lifecycle

A practical lifecycle might be:

1. raw evidence
2. processed material
3. candidate extraction
4. machine review
5. human or escalation review where needed
6. promotion
7. supersession or archival when later displaced

### Rule
Each stage should be explicit in status metadata.

---

## Section 14 — Agent Rules

Agents must not:
- treat candidate data as canonical
- silently overwrite verified records
- remove provenance for convenience
- invent evidence snippets
- weaken truth requirements to simplify coding
- claim “verified” without satisfying the promotion gates

Agents must:
- preserve traceability
- surface ambiguity
- escalate when unsure
- update truth-governance docs when policy changes

---

## Final Principle
Vitruvius earns trust by making wrong truth hard to admit and easy to trace.  
That discipline is part of the product, not overhead.
