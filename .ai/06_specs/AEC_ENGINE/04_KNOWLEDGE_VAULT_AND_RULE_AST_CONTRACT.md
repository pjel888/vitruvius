# Knowledge Vault and Rule AST Contract

## Purpose
This file defines the mandatory schema, data contracts, and ingestion discipline for the RocksDB knowledge vault — the single source of truth for laws, standards, jurisdictional parameters, and pricing in the Vitruvius AEC engine. It is the governing document for every byte that ever reaches the vault and every byte that ever leaves it. Other files in this pack cite this one; when those files disagree with this one on a vault-shaped question, this file wins. The vault is the legal memory of the system, and legal memory is only ever JSON.

## Scope
- RocksDB key schema for rules, costs, terrain, assets, and persisted ECS state
- The four-block JSON payload — Metadata, Temporality, Governance, Physics AST
- The three enforcement levels — `statutory_law`, `industry_standard`, `optimization_heuristic`
- AST composability rules across domains and jurisdictions
- LLM ingestion discipline and schema-constrained generation
- Confidence thresholds and human-in-the-loop promotion
- International modular rule packages and the jurisdiction-as-namespace rule
- Rule conflict resolution metadata and orchestrator responsibility
- The absolute "no code in the database" rule and its enforcement surface

## Core Principle
Rules are data, not code. The knowledge vault holds JSON forever — it never, under any circumstance, stores executable code. Rust owns physics, Python owns translation, RocksDB owns law, and the three roles are non-transferable.

## Why RocksDB, Not SQL
- The dominant access pattern is a prefix scan over hierarchical keys ("give me every rule that applies to a concrete beam in Manila"), which RocksDB serves natively via its log-structured merge-tree and prefix iterator. SQL would need indexes and joins to match it.
- Append-only write semantics align with the temporal-graph requirement — rules are versioned, never overwritten, never deleted.
- RocksDB runs embedded, with no separate server process, which matters for local-first development and for reproducible CI runs.
- The `rust-rocksdb` binding is mature, actively maintained, and owned by the C++ RocksDB team.
- RocksDB compression (Snappy, Zstd, LZ4) makes storing large legal corpora practical without a bespoke compaction layer.
- Browser deployment is a known constraint — RocksDB does not run in the browser. A Wasm target MUST either preload the required subset of the vault into memory at session start, use a `sled` or IndexedDB-backed adapter, or fall back to a server-side vault service. The choice MUST be documented by an AD before shipping any Wasm binary that claims vault access.

## RocksDB Key Schema Rules

### 1. Canonical Hierarchy
- Every rule key MUST follow the form: `rule:[jurisdiction]:[domain]:[target_entity]:[rule_id]`.
- Canonical examples:
  - `rule:ph:architectural:setback_front:pd1096_sec804`
  - `rule:ph:electrical:voltage_drop:pec_sec210`
  - `rule:ph:structural:beam_deflection:nscp_sec409`
  - `rule:sg:fire:sprinkler_coverage:scdf_ch4`
  - `rule:intl:structural:steel_deflection:aisc_360`

### 2. Extended Key Namespaces
Non-rule data uses the same colon hierarchy under reserved top-level namespaces:
- `cost:material:{material_code}` → price per unit in a documented currency
- `cost:labor:{trade}_{level}` → crew-day rate in a documented currency
- `terrain:{site_id}:{resolution}` → heightmap blob for a specific site and resolution
- `asset:{asset_id}` → JSON metadata for a catalog asset (HVAC unit, fixture, etc.)
- `entity:{building_id}:{entity_id}` → serialized ECS entity state when persistence is enabled

Pricing data details are governed by `09_PARETO_OPTIMIZATION_AND_FINANCIAL_LAYER_RULES.md`. This file only specifies that prices live under the `cost:` prefix.

### 3. Key Formation Rules
- All keys MUST use colon separators. No slashes, no dots, no hyphens as separators.
- All jurisdiction codes MUST use ISO-style prefixes (`ph`, `sg`, `us`, `hk`, `my`, `vn`, `id`, `intl`).
- All domains MUST come from a controlled vocabulary (`architectural`, `structural`, `mechanical`, `electrical`, `plumbing`, `fire`, `accessibility`, `civil`, `zoning`, `environmental`).
- Custom top-level namespaces (anything not in `{rule, cost, terrain, asset, entity}`) MUST NOT be introduced without an AD.
- Keys MUST be lowercase ASCII. Unicode in keys is forbidden.
- Keys MUST be stable — once issued, a rule ID becomes part of the supersedes chain and cannot be repurposed.

## The Four-Block JSON Payload

Every vault write under the `rule:` prefix MUST contain exactly four top-level blocks, in this order, conforming to the AST JSON Schema. Payloads with missing blocks, extra blocks, or reordered blocks MUST be rejected at write time.

### Block 1 — Metadata (Identity)
- `rule_id` — stable string, matches the trailing segment of the key
- `source_document` — canonical name of the statute, standard, or code section
- `human_text` — the original natural-language text of the rule, verbatim
- Provenance is load-bearing. User-facing citations quote `human_text` directly. Rust never sees this block.

```json
"metadata": {
  "rule_id": "ph_pd1096_sec804",
  "source_document": "National Building Code of the Philippines",
  "human_text": "Front setback for R-1 zoning shall not be less than 4.5 meters."
}
```

### Block 2 — Temporality
- `version` — short version tag (e.g. `v2005_irr`, `v2019_irr`, `v2024_nscp`)
- `effective_date_start` — ISO-8601 date, inclusive
- `effective_date_end` — ISO-8601 date or `null` if the rule is still active
- `supersedes_id` — rule ID of the immediately prior version, or `null` if this is the original
- Rules are NEVER deleted. Amendments append a new rule whose `supersedes_id` points backward.
- The `supersedes_id` chain forms a backward linked list of historical versions. RocksDB thereby becomes an Append-Only Temporal Graph.

```json
"temporality": {
  "version": "v2005_irr",
  "effective_date_start": "2005-04-30",
  "effective_date_end": null,
  "supersedes_id": "ph_pd1096_sec804_v1977"
}
```

### Block 3 — Governance
- `enforcement_level` — exactly one of `statutory_law`, `industry_standard`, `optimization_heuristic` (see next section)
- `stringency_weight` — float in `[0, 1]` for fine-grained tuning by the optimizer
- `waiver_possible` — boolean recording whether administrative variances are permitted
- `source_authority` — short token identifying the promulgating body (used in conflict resolution)
- `conflict_resolution_hint` — optional structured hint for the orchestrator when two rules collide

```json
"governance": {
  "enforcement_level": "statutory_law",
  "stringency_weight": 1.0,
  "waiver_possible": false,
  "source_authority": "dpwh_ph",
  "conflict_resolution_hint": null
}
```

### Block 4 — Physics AST
- `node_id` — stable identifier for this AST node within its rule
- `domain` — same controlled vocabulary as the key
- `component_target` — the ECS component type this AST binds to
- `constraint_type` — controlled vocabulary (`minimum_clearance`, `maximum_deflection`, `maximum_velocity`, `minimum_ventilation_rate`, etc.)
- `formula_ast` — tree-structured expression with `operator` and `operands` / `left` / `right`
- `confidence` — float in `[0, 1]` from the LLM extraction pipeline

```json
"physics_ast": {
  "node_id": "rule_nscp_sec_409",
  "domain": "structural",
  "component_target": "concrete_beam",
  "constraint_type": "maximum_deflection",
  "formula_ast": {
    "operator": "divide",
    "left": "span_length",
    "right": 360
  },
  "confidence": 0.98
}
```

## The Three Enforcement Levels

The `governance.enforcement_level` field dictates how downstream layers treat the AST. It is the only field that controls whether a violation is fatal, expensive, or merely suboptimal.

### 1. `statutory_law`
- HARD boundary. Violations are not negotiable.
- Z3 returns `unsat` on a violation; the orchestrator refuses to generate or commit the configuration.
- No override is possible at the engine level. Waivers are an administrative process outside the engine.
- Examples: PD 1096 setbacks, fire egress minimums, structural safety factors.
- `stringency_weight` MUST be `1.0`. `waiver_possible` MAY be `true` only to record that a human-driven variance process exists — the engine still refuses.

### 2. `industry_standard`
- SOFT boundary. Violations are permitted only when adhering would force a cascade into a `statutory_law` violation elsewhere.
- The optimizer penalizes violations heavily via `stringency_weight`, preferring conformant layouts but not destroying them.
- Examples: ASHRAE duct velocity guidelines, ACI recommended cover for non-critical elements, NEC advisories that are not adopted as law in the current jurisdiction.
- The orchestrator MUST log every soft-boundary violation for audit review.

### 3. `optimization_heuristic`
- No compliance implications whatsoever.
- Consumed exclusively by the Pareto / financial / topological optimizer (see `09_PARETO_OPTIMIZATION_AND_FINANCIAL_LAYER_RULES.md`).
- Examples: "keep plumbing runs as straight as possible", "prefer standard stock lengths", "minimize duct bends".
- Heuristics MUST NOT be handed to Z3. Z3 is for verification, not for taste.

## AST Composability Rules
- Multiple ASTs MAY be fetched and composed into a single Z3 query by Python.
- Composition is an orchestrator responsibility. Rust never composes ASTs. Rust never sees an AST at all — it sees the compiled numerics produced by the Z3 Inequality Compiler (see `06_FORMAL_VERIFICATION_AND_Z3_PROTOCOL.md`).
- Variable namespacing is mandatory. Every variable in a `formula_ast` MUST be interpreted under its parent rule's namespace. A raw `length` in one rule MUST NOT alias `length` in another rule.
- The translation layer disambiguates variables at composition time. Name collisions MUST be resolved explicitly; silent coercion is forbidden.
- Composed ASTs MUST preserve the provenance chain. When a Z3 unsat core cites a constraint, Python MUST be able to trace the constraint back to the original rule IDs.
- Composition across jurisdictions is only allowed inside a Python orchestration context that has an explicit jurisdictional binding. Cross-jurisdiction AST composition without that binding is a red-line condition.

## The No-Code-In-Database Rule
- The vault MUST NEVER store Python scripts, Rust functions, JavaScript, WebAssembly binaries, shell commands, lambdas, pickles, regexes that will be compiled at runtime, grammars that will be executed, or any other executable artifact.
- Every rule in the vault MUST be inspectable as JSON without executing anything.
- `eval()` (and every language-level equivalent) against vault content is FORBIDDEN.
- The `formula_ast` block is a data tree, not a program. It is walked by the Z3 Inequality Compiler, which produces Z3 expressions — Python never interprets the tree as code.
- Any proposal to extend the schema with an "executable" field, a "script" field, a "plugin" field, or anything that would invite code-in-data is an immediate escalation. No exceptions.
- Rationale, canonical: a code-in-database pattern destroys auditability, destroys reproducibility, destroys security, and kills performance. The day a rule becomes code is the day the system becomes unauditable.

## LLM Ingestion Discipline

### 1. Schema-Constrained Generation Is Mandatory
- Every LLM that writes to the vault MUST emit JSON through schema-constrained decoding. Free-form JSON prompting is forbidden for vault ingestion.
- Acceptable constraint mechanisms:
  - Anthropic tool use with a strict tool schema
  - OpenAI structured outputs with a JSON Schema
  - Outlines (Python) with regex- or grammar-constrained decoding
  - llama.cpp GBNF grammars for local models
  - Guidance or equivalent constraint frameworks
- The LLM's job is strictly to *map unstructured text into the schema*. It MUST NOT compute, judge, or reason about physics while ingesting.
- Prompts MUST NOT grant the LLM a "free text" escape hatch. Any extraction that cannot be expressed in the AST schema is rejected, not stashed in a text field.

### 2. Pipeline Shape
1. Provide the LLM with the JSON Schema for the four-block payload.
2. Provide the source text (a bounded section of the law or standard).
3. Instruct the LLM to emit JSON conforming to the schema.
4. Validate the emitted JSON against the schema with a loud, failing validator.
5. On validation failure, issue a corrective retry with a bounded attempt count.
6. On success, attach the model's confidence score to `physics_ast.confidence` and route through the human-review gate below.
7. Only then is the JSON eligible for a vault write.

### 3. Confidence Thresholds
- `confidence > 0.95` — auto-accept into the vault; flag for sample review.
- `0.7 <= confidence <= 0.95` — queue for human review before promotion. The rule MUST NOT be queryable by the orchestrator until a human promotes it.
- `confidence < 0.7` — reject outright; flag for manual extraction by a domain expert.
- Every rule whose `enforcement_level` is `statutory_law` MUST be seen by a human at least once, regardless of confidence score. The LLM may do the heavy lifting of extraction; it never gets the last word on the law.

### 4. Retry Policy
- Schema validation failures MUST trigger a bounded corrective retry (typical bound: 3 attempts).
- Uncorrectable rules MUST be rejected and logged, NEVER force-promoted.
- A rule that fails validation three times is a manual extraction job, not a retry-forever job.
- Retry attempts and their diffs MUST be logged in the ingestion audit trail.

## International Modular Rule Packages
- Each jurisdiction lives under its own top-level namespace inside the `rule:` prefix (`ph`, `sg`, `us`, `hk`, `my`, `vn`, `id`, `intl`, etc.).
- The Rust data plane MUST remain completely blind to geography. Rust does not know what "PD 1096" or the "International Building Code" is. It understands abstract AEC physics and nothing more.
- Context injection is a Python responsibility. When a user selects a project location, the Python orchestrator binds the jurisdiction and queries the matching namespace. Rust never learns the jurisdiction name.
- Adding a new country means ingesting new JSON, not recompiling Rust. The engine is a legal cartridge swapper.
- Jurisdictional corpora MUST go through the same ingestion pipeline, the same schema, and the same confidence gating as every other jurisdiction. A new country does not get a relaxed bar.
- Cross-jurisdiction rule injection (e.g. pulling a Singapore rule into a Philippines project) without an explicit Python context-layer binding is a red-line condition.
- Pricing data under `cost:` is jurisdictional by convention — `cost:material:pvc_50mm:ph` and `cost:material:pvc_50mm:sg` coexist. The orchestrator MUST bind a jurisdiction before reading `cost:`.

## Rule Conflict Resolution
- Two rules from different sources MAY genuinely contradict one another — the Plumbing Code says X mm minimum, the Building Code says Y mm minimum, and both claim authority.
- The `governance` block MUST carry enough conflict-resolution metadata to let the orchestrator decide: `enforcement_level`, `stringency_weight`, `source_authority`, and (optionally) `conflict_resolution_hint`.
- The conflict-resolution policy itself is an orchestrator responsibility, not a kernel responsibility. Python reads the metadata, applies the configured policy (most-restrictive wins, most-recent wins, highest-authority wins), and logs the decision in the audit trail.
- Unresolved conflicts MUST block compliance verification. The orchestrator MUST NOT guess. A conflict that has no resolution policy is a red-line condition that halts generation until a human configures the policy.
- Rust MUST NOT be asked to resolve a conflict. Rust sees a single compiled constraint set — the orchestrator has already decided.

## Temporal Audit Rules (Cross-Reference)
- Retroactive compliance audits inject a historical clock into the orchestrator. The orchestrator reads `temporality.effective_date_start` and `temporality.effective_date_end` and selects only the rules that were in effect at the audit clock.
- The temporality block is what makes retroactive audits possible — heritage assessments, insurance disputes, forensic engineering, legal proceedings.
- Full determinism, temporal clock, and audit-log rules are governed by `08_DETERMINISM_TEMPORALITY_AND_AUDIT_RULES.md`. This file only specifies the vault-side schema that makes those rules expressible.
- The temporal clock MUST be a Python concept. Rust MUST NOT read a system clock in any code path that crosses the boundary.

## Red-Line Conditions
The Agent MUST stop and escalate if any of the following occur:
- a proposed vault write contains executable code in any field or any form
- a proposed ingestion accepts LLM output without schema-constrained generation
- a proposed ingestion bypasses the confidence gate or promotes a sub-threshold rule
- a proposed schema change introduces a new top-level namespace without an AD
- a proposed amendment deletes a rule instead of superseding it
- a proposed Rust change asks Rust to read RocksDB directly
- a proposed Rust change asks Rust to interpret legal text or parse an AST
- a proposed orchestration step performs cross-jurisdiction AST composition without an explicit Python context-layer binding
- a proposed conflict between two rules reaches the solver without resolution metadata
- a proposed vault row lacks any of the four required blocks, or includes a fifth block
- a proposed `statutory_law` rule has never been seen by a human reviewer
- any proposal to add an "executable", "script", "plugin", "eval", or "code" field to the AST schema
- any proposal to store unicode, binary blobs, or non-JSON payloads under the `rule:` prefix

Escalation means stop, write the conflict down, and request an AD. It does not mean "work around it".

## Cross-References
- **Research paper** (`/.ai/13_research/AEC-ECS-SC_RESEARCH.md`):
  - §4 — The Knowledge Vault (RocksDB) — full section
  - §4.1 Why RocksDB, not SQL
  - §4.2 The Smart Key Schema
  - §4.3 The Four-Block JSON Payload
  - §4.4 The Absolute Rule — No Code in the Database
  - §4.5 LinkML, SHACL, and JSON Schema for Rule Serialization
  - §4.6 The LLM Ingestion Pipeline
  - §4.7 Confidence and Human Review
  - §11 International Modular Rule Packages — full section
  - §11.3 Retroactive Compliance Audits
- **Companion AEC_ENGINE files:**
  - `01_COMPOUND_AI_OPERATING_CONTRACT.md` — the five-layer contract that this vault lives inside
  - `05_MULTI_DISCIPLINARY_COORDINATION_RULES.md` — hierarchy of precedence across domains
  - `06_FORMAL_VERIFICATION_AND_Z3_PROTOCOL.md` — Z3 Inequality Compiler (consumes the Physics AST block)
  - `08_DETERMINISM_TEMPORALITY_AND_AUDIT_RULES.md` — temporal clock and audit-log semantics
  - `09_PARETO_OPTIMIZATION_AND_FINANCIAL_LAYER_RULES.md` — pricing data under `cost:` prefix
- **Related RUST / GOVERNANCE pack files:**
  - `.ai/06_specs/RUST/04_RUST_ARCHITECTURE_AND_BOUNDARY_RULES.md` — Rust MUST NOT read RocksDB
  - `.ai/06_specs/GOVERNANCE/05_TRUTH_GOVERNANCE_AND_PROMOTION_CONTRACT.md` — promotion discipline that this file's confidence gate plugs into

## Final Rule
A rule in the vault is JSON, now and forever. The day a rule becomes code is the day the system becomes unauditable.
