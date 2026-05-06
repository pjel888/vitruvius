# Full Autopilot Global Inventory

Date: 2026-05-07 local

Baseline verified against terminal output and validators during the full autopilot loop.

## Current Counts

| Item | Count |
|---|---:|
| Resources | 10 |
| nodeResourceLinks | 12 |
| accepted nodeResourceLinks | 9 |
| needs_review nodeResourceLinks | 2 |
| rejected nodeResourceLinks | 1 |
| External metadata candidates | 15 |
| Admitted graph relationships | 266 |
| Base graph edges | 13,670 |
| Effective graph edges | 13,936 |
| `CROSS_DOMAIN_EQUIVALENT` | 0 |
| `CROSS_DOMAIN_ALIGNMENT` | 22 |

## Candidate Work

| Category | Items | Current blocker or action |
|---|---:|---|
| `duplicate_candidate` | 2 | ASCE 7 and FHWA external candidates duplicate existing Resources; no promotion from these candidates. |
| `ready_for_promotion_review` | 3 | buildingSMART IFC, WBDG Fire Protection, and Uniclass already have promoted reviewer-only Resources and accepted links; candidate status reconciliation may be needed, but no duplicate Resource should be created. |
| `needs_review` source-family candidates | 10 | Exact official source locator, custody, and rights/access review still required before Resource-only or Resource-and-link promotion. |
| standards context incomplete | 2 Resources / 3 standard-like link warnings | ASCE 7 and ACI 318 remain blocked from accepted-link/learner-trust advancement without real edition/version/scope context. |

No candidate is safe to promote without further official locator/custody review except already-promoted duplicate-safe records.

## Resource Work

| Category | Items | Current blocker or action |
|---|---|---|
| accepted public-web Resources with standardized metadata-only caveats | U.S. Access Board Accessible Routes Ch. 4; WBDG Wind Safety Building Envelope; WBDG Seismic Design Principles; ICE Structural Load Paths; FHWA Earth Retaining Structures | No further metadata-only correction needed unless a later source check discovers a safer exact locator or caveat. |
| reviewer-only accepted Resources | buildingSMART IFC, WBDG Fire Protection, Uniclass | Metadata-only custody checked and accepted links exist; do not claim source truth or governing status. |
| standards Resources missing context | ASCE 7; ACI 318 | Blocked by missing edition/version/scope context; no current/governing/compliance/AHJ claim is safe. |

## nodeResourceLink Work

| Category | Items | Current blocker or action |
|---|---:|---|
| accepted links | 9 | Learner eligibility is computed by Resource Layer logic. |
| `needs_review` links | 2 | ASCE standard-like wind/seismic links remain blocked by standards context. |
| rejected links | 1 | ACI 318 / Structural Column remains rejected or not learner-trusted. |
| possible accepted-link candidate | 0 immediate | FHWA retaining wall link was accepted in this unit; no other non-standard `needs_review` link remains. |

## Graph Work

| Category | Current status |
|---|---|
| Previously admitted Resource-backed graph edges | `BIM Schemas INFORMS IFC Exchange`; `Structural Wind Load INFORMS Load Path`. |
| Newly accepted FHWA link graph potential | Needs a separate graph packet; likely Resource Layer-only unless a precise existing endpoint and relation pass gates. |
| WBDG Fire Protection and Uniclass graph potential | Prior packets found Resource Layer-only boundaries due duplicate/overclaim risk. |
| Standards-backed graph potential | Blocked until standards context is complete. |

No graph edge may be admitted without source/context gate, relation vocabulary gate, delegated review, dry-run, transaction manifest, rollback plan, Explorer verification, and tests.

## Explorer/UI Work

Safe visual improvement candidates remain:

- Correct `unverified` badge tone in Resource evidence UI where string matching can treat `unverified` as verified. Completed in `/.ai/13_research/full_autopilot_visual_graph_improvements.md`.
- Surface accepted Resource caveats more clearly in learner Resource cards without changing eligibility logic.
- Add targeted regression coverage for accepted `INFORMS` edge visibility and evidence badges.

No current evidence indicates learner overexposure.

## Tooling Caveats

- `morph` codebase search returned HTTP 429 during early exploration.
- ChunkHound deep research lacked an LLM configuration, and one parallel search attempt hit a DuckDB lock; GitNexus CLI and local validators remained usable.
- Code intelligence refresh completed with known ChunkHound timeout/embedding warnings and code-review-graph `tree-sitter-yaml` / embedding context warnings.

## Next Highest-Value Unblocked Actions

1. Commit the FHWA metadata and accepted-link unit after scoped staging and git sync verification.
2. Surface accepted Resource caveats more clearly in learner Resource cards without changing eligibility logic, if focused inspection finds a real display gap.
3. Continue official locator discovery for the ten remaining source-family candidates.
4. Continue standards-context review for ASCE 7 / ACI 318 only if real public metadata is available without protected-content ingestion.
