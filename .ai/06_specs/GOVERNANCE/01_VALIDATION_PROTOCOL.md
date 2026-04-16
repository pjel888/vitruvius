# Vitruvius Validation Protocol

## Purpose
This document defines the mandatory validation regime for work performed in the Vitruvius repository. It exists to ensure that no code, configuration, rule, schema, workflow, or architecture-affecting change is treated as complete without appropriate proof.

Validation is not decorative. It is the mechanism by which Vitruvius prevents incorrect, unstable, unbounded, or unverified work from surviving into the product.

## Scope
This protocol applies to:
- Python code
- Rust code
- TypeScript or Node.js code
- configuration changes
- schema changes
- rule extraction and promotion logic
- pipeline behavior
- performance-sensitive changes
- documentation that affects execution or governance
- any change that can alter truth, trust, determinism, or auditability

## Core Principle
A change is not validated because it appears reasonable.  
A change is validated only when evidence appropriate to its risk level has been produced and reviewed.

## Validation Objectives
Every validated change should answer the following:
- Did the intended behavior actually occur?
- Did any existing behavior break?
- Is the output deterministic where required?
- Is the result traceable and explainable?
- Is performance still acceptable?
- Are all affected docs and state artifacts updated?
- Are known limitations surfaced honestly?

## Validation Layers
Vitruvius uses layered validation:

1. Static validation
2. Contract validation
3. Deterministic functional validation
4. Edge-case validation
5. Differential or oracle validation
6. Integration validation
7. Performance validation
8. Truth and provenance validation
9. State and documentation validation

No single layer is sufficient on its own for serious work.

---

## Section 1 — Static Validation

### Purpose
Catch obvious structural issues before dynamic execution.

### Examples
- formatting
- linting
- type checks where applicable
- dependency integrity
- dead code or unused import detection where useful
- schema shape validation
- syntax-level config validation

### Minimum Expectations by Language

#### Python
- formatter passes if formatter is in use
- lints or equivalent checks where configured
- import integrity checked
- type checking if module participates in typed subsystem or contract-sensitive path

#### Rust
- `cargo fmt --all`
- `cargo clippy --all-targets --all-features -- -D warnings`
- `cargo test --all-targets`

#### TypeScript / Node
- formatter where applicable
- linting where configured
- type check
- tests for touched modules

### Failure Rule
Static validation failure blocks completion.

---

## Section 2 — Contract Validation

### Purpose
Ensure explicit interfaces remain correct.

### Applies To
- API boundaries
- function signatures with defined behavior
- schema-bound payloads
- AST serialization
- RocksDB payload structures
- PyO3 boundaries
- Wasm boundaries
- config files
- rule formats
- canonical frontmatter or metadata formats

### Required Questions
- Are input and output shapes still correct?
- Are required fields present?
- Are units or data types preserved?
- Are default assumptions still valid?
- Are invalid states rejected or explicitly handled?

### Examples
- JSON schema validation for extracted rule payloads
- AST node validation before compilation
- canonical metadata validation before promotion
- FFI payload validation before entering Rust

### Failure Rule
If a contract exists, it must be validated.

---

## Section 3 — Deterministic Functional Validation

### Purpose
Verify that intended behavior works in ordinary cases.

### Required
Every non-trivial implementation must include deterministic tests for:
- expected success cases
- expected failure cases
- threshold behaviors where relevant
- representative business or pipeline logic for the changed area

### Examples
- pipeline stage emits expected files
- canonicalization produces expected frontmatter
- relationship extraction emits expected candidate structure
- Z3 compiler encodes expected arithmetic logic
- Rust kernel returns expected numeric result for canonical cases

### Rule
If the expected output can be known, it should be asserted.

---

## Section 4 — Edge-Case Validation

### Purpose
Prevent shallow success masking fragile behavior.

### Required Triggers
Edge-case validation is mandatory when a change touches:
- parsing
- normalization
- geometry
- numerical computation
- thresholds
- rule interpretation
- truth promotion
- routing logic
- temporal logic
- multi-step orchestration

### Edge-Case Categories
- empty inputs
- missing fields
- duplicate IDs
- near-threshold values
- contradictory rules
- stale registry references
- zero-length geometry
- very large coordinates
- near-parallel segments
- conflicting document authority
- inconsistent timestamps or temporality windows

### Rule
Known edge cases must be tested or explicitly deferred and documented.

---

## Section 5 — Differential or Oracle Validation

### Purpose
Compare a new or optimized implementation against a trusted reference.

### When Required
- optimized math kernels
- extracted rule ASTs
- canonicalization transformations
- normalization engines
- refactors with high truth risk
- batch pipelines where prior outputs serve as reference
- performance rewrites

### Acceptable Oracles
- a simpler reference implementation
- an older verified implementation
- mathematically derived expected values
- golden files
- reviewed snapshots
- human-reviewed sample set

### Rule
If a new implementation is more complex or more optimized, it should be checked against something simpler and trusted.

---

## Section 6 — Integration Validation

### Purpose
Verify that system components still work together.

### Required For
- cross-module refactors
- pipeline stage changes
- AST-to-Z3 compilation
- Python-to-Rust boundaries
- extraction-to-review-to-promotion chains
- cache or stateful workflow changes
- feature-flagged routing or model selection logic

### Integration Questions
- Does the full workflow still complete?
- Do intermediate artifacts remain valid?
- Are manifests and reports still written correctly?
- Are downstream consumers still compatible?
- Do feature flags preserve byte-identical behavior when disabled, if that is a requirement?

### Rule
A change that spans multiple modules or layers is not validated by unit tests alone.

### Dataset-Scoped Graph Proof Validation
For any future mini dataset→graph implementation, validation must explicitly cover both the **micro pilot** and the **macro codebase impact**.

Minimum required checks:
- **Path audit evidence** — the full source→graph path and blast radius are documented before implementation
- **Leakage check** — only manifest-allowed canonical pages / relationship records enter the scoped graph
- **Artifact isolation check** — dataset outputs land only under dataset-specific roots and do not mutate global `latest_*`
- **Scoped integrity check** — zero duplicate node IDs, zero dangling edges, warning count recorded
- **Scoped query check** — seeded questions against the scoped snapshot return evidence-bearing answers
- **Determinism/replay check** — rerunning the same manifest yields stable outputs
- **Macro-compatibility check** — the dataset-scoped mechanism still preserves the current default/global path when dataset mode is unused
- **Anti-special-case check** — reject implementations that hardcode the pilot dataset instead of using manifest data

---

## Section 7 — Performance Validation

### Purpose
Protect product-critical performance characteristics.

### Performance Is Mandatory To Validate When
- a hot path is modified
- Rust kernel behavior changes
- a heavy loop changes
- data shape or memory layout changes
- broad pipeline operations are refactored
- feature flags introduce latent cost
- model routing or graph operations change computational profile

### Required Performance Evidence
- benchmark target
- benchmark method
- baseline
- current result
- acceptable threshold
- interpretation

### Example Metrics
- wall-clock latency
- throughput
- memory usage
- allocation count
- cache or serialization overhead
- startup or warmup cost
- index rebuild time

### Failure Rule
Performance claims without measurement are not evidence.

---

## Section 8 — Truth and Provenance Validation

### Purpose
Protect Vitruvius from incorrect claims entering trusted layers.

### Required For
- extraction systems
- canonicalization affecting truth-bearing content
- rule ingestion
- relationship extraction
- review logic
- promotion logic
- temporal versions
- confidence thresholds
- provenance metadata

### Required Checks
- source identity present
- section or clause identity present where required
- evidence snippet present where required
- schema valid
- confidence and review fields present
- canonical ID rules preserved
- conflict handling explicit
- temporality windows valid
- no silent overwrite of verified truth

### Rule
No truth-bearing output is valid without provenance.

---

## Section 9 — State and Documentation Validation

### Purpose
Ensure the repo’s memory reflects reality.

### Required
After non-trivial work:
- current plan status updated
- validation report created or updated
- state files updated if execution status changed
- milestone tracker updated where scope or status changed
- decisions log updated if architecture changed
- authoritative docs updated if behavior changed

### Failure Rule
A code change without corresponding repo-memory updates is incomplete.

---

## Section 10 — Validation by Task Class

### Trivial Task
Minimum:
- local correctness check
- focused test if applicable
- no state drift introduced

### Moderate Task
Minimum:
- targeted tests
- contract validation where relevant
- state update if required

### Major Task
Minimum:
- full execution loop
- targeted and integration tests
- validation report
- state reconciliation

### Architecture-Affecting Task
Minimum:
- full execution loop
- architecture review
- decision log update
- integration and regression validation

### Rust-Critical Task
Minimum:
- full Rust protocol
- edge-case tests
- property tests where applicable
- benchmarks for hot paths
- validation report

### Truth-Critical Task
Minimum:
- provenance checks
- schema validation
- oracle or reviewed sample validation
- promotion gating review

### Performance-Critical Task
Minimum:
- benchmark baseline
- benchmark after change
- interpretation of regression or improvement
- rejection if budget exceeded without explicit approval

---

## Section 11 — Validation Artifacts

### Expected Artifact Types
- test output logs
- benchmark results
- validation report markdown
- updated plan checklist
- updated state docs
- diff notes or regression summaries
- reviewed sample outputs
- schema validation output

### Required Storage
Validation artifacts should be stored in locations already used by repo conventions, such as:
- `.ai/05_logs/`
- `.ai/10_state/`
- `006_System-Manifests/runs/`
- test or benchmark directories within the affected subsystem

---

## Section 12 — Validation Report Template

## Validation Report
- Task:
- Date:
- Scope:
- Risk class:
- Related audit:
- Related plan:

### Static Validation
- checks run:
- outcome:

### Functional Validation
- tests run:
- outcome:

### Edge-Case Validation
- cases covered:
- remaining weak spots:

### Integration Validation
- workflows exercised:
- outcome:

### Performance Validation
- benchmark path:
- baseline:
- current:
- threshold:
- interpretation:

### Truth / Provenance Validation
- schema/provenance checks:
- outcome:

### State and Docs Validation
- updated files:
- outcome:

### Final Judgment
- accepted / accepted with caveats / rejected

### Known Limitations
- list clearly

---

## Section 13 — Failure Policy

If validation fails:
- do not mark task complete
- document what failed
- document what remains risky
- either fix or explicitly defer with a recorded reason

Partial completion is allowed. Silent completion is not.

## Final Principle
Validation is the price of trust.  
If validation is skipped, trust is forfeited.
