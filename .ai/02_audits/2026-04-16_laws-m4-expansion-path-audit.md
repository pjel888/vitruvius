# Audit — Laws M4 Expansion Path

## Core finding
The bounded pilot is already successful, so M4 is no longer about proving the graph lane works.
It is about making expansion safe and repeatable.

## Audit verdict
Proceed with M4 as **model/spec work first**, then only implement the smallest additive runtime support justified by those specs.

## Why that is the lowest-risk path
- avoids widening into generic Phase 11 expansion by momentum
- keeps the current successful bounded pilot stable
- lets future law additions follow a repeatable law-unit contract
- reduces the risk of silently inventing section or merge semantics in code before they are governed

## Specific audit conclusions
### Per-law repetition
Safe to formalize now.
It reuses existing manifest/report machinery and mostly needs a clearer contract.

### Per-section graphing
Safe as an evidence-filtered snapshot model.
Unsafe to jump directly to canonical section nodes without a separate truth-admission policy.

### Merged graph rules
Safe to specify now.
Unsafe to implement broad merge orchestration before collision/provenance rules are frozen.

## Recommended M4 execution order
1. formalize per-law repetition model
2. formalize per-section evidence-scoped graph model
3. formalize merged-graph collision/provenance rules
4. only then add minimal runtime/schema support where needed
