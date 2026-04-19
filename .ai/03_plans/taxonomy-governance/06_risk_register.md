# 06 — Risk Register: Taxonomy Governance Build

> **Scope:** Identified risks, triggers, early warnings, contingencies, and rollback thresholds for the taxonomy governance build.
> **Date:** 2026-04-19
> **Authority:** `00_locked_decisions.md`, `03_implementation_plan.md`, `05_pr_sequence.md`

---

## Risk Legend

| Severity | Color | Meaning |
|----------|-------|---------|
| 🔴 Critical | Red | Will block release or cause data loss if realized |
| 🟠 High | Orange | Will significantly delay release or degrade quality |
| 🟡 Medium | Yellow | Will cause localized issues, manageable with planning |
| 🟢 Low | Green | Minor impact, easily mitigated |

| Probability | Meaning |
|-------------|---------|
| High | >50% chance of realization |
| Medium | 20–50% chance |
| Low | <20% chance |

---

## R01: Changing Canonical IDs Breaks Graph References

| Field | Value |
|-------|-------|
| **Severity** | 🔴 Critical |
| **Probability** | Medium |
| **Stage** | Phase 2 (ID Migration), PR-05, PR-06 |
| **Description** | Opaque `VTN-*` IDs replace semantic slugs. Any runtime reference (API, UI URLs, graph edges, frontmatter arrays) that still uses old IDs will break. |
| **Trigger** | PR-05 merges and `canonical_id` properties are written to Neo4j without full redirect table coverage. |
| **Early Warning Signal** | Parity check script reports <100% match for node lookups. Unit tests for redirect resolution fail. |
| **Mitigation** | 1. `id_redirect` table must be 100% populated before any write. 2. All v1 endpoints return `canonical_id` additively. 3. 308 redirect handler routes old URLs. 4. Parity check must pass before PR-06 merges. |
| **Contingency** | Revert PR-05 and PR-06. Restore old IDs from Git backup. |
| **Contingency Owner** | Data Engineer |
| **Time-to-Rollback Threshold** | 15 minutes (id_redirect table truncation + property removal) |
| **Monitoring** | Parity check CI job, redirect hit rate in logs |

---

## R02: Explorer UI Breaks If Node Types Change

| Field | Value |
|-------|-------|
| **Severity** | 🔴 Critical |
| **Probability** | High |
| **Stage** | Phase 7 (Explorer Updates), PR-12 |
| **Description** | Explorer hardcodes 8 node types and 7 edge types. New facet-based types will not render correctly. |
| **Trigger** | PR-12 merges with dynamic type rendering without sufficient fallback handling. |
| **Early Warning Signal** | Explorer build fails or shows blank nodes/edges. E2E tests fail on taxonomy tree rendering. |
| **Mitigation** | 1. Keep hardcoded lists as fallback aliases. 2. Dynamic rendering only activates when `k_taxonomy_v2 = true`. 3. Add `unknown` type handler with default styling. 4. All changes behind feature flag. |
| **Contingency** | Toggle `k_taxonomy_v2 = false`. Revert to static type lists. |
| **Contingency Owner** | Frontend Engineer |
| **Time-to-Rollback Threshold** | 5 minutes (feature flag toggle) |
| **Monitoring** | E2E test suite, error tracking (Sentry or equivalent) |

---

## R03: Philippine Rules Do Not Generalize

| Field | Value |
|-------|-------|
| **Severity** | 🟠 High |
| **Probability** | Medium |
| **Stage** | Phase 4 (Jurisdiction Packs), PR-08 |
| **Description** | `canonical_rules.yaml` is 1,186 lines of Philippine-specific rules. Extracting to a generic jurisdiction pack may lose nuance or introduce errors. |
| **Trigger** | PR-08 merges with incorrect rule extraction or missing edge cases. |
| **Early Warning Signal** | Validation script reports missing rules. Applicability rule tests fail for edge cases (e.g., LGU-specific overrides). |
| **Mitigation** | 1. Extract rules incrementally (national first, LGU second). 2. Rule-by-rule review by subject matter expert. 3. Maintain `canonical_rules.yaml` as reference until PR-08 is validated. 4. Add rule coverage tests. |
| **Contingency** | Revert PR-08. Restore `regulatory_basis` in concept frontmatter. Keep `canonical_rules.yaml` active. |
| **Contingency Owner** | Domain Expert (Philippine regulatory) |
| **Time-to-Rollback Threshold** | 30 minutes (restore frontmatter + rules file) |
| **Monitoring** | Rule coverage metrics, applicability rule test results |

---

## R04: Search Regression Without Index

| Field | Value |
|-------|-------|
| **Severity** | 🟠 High |
| **Probability** | Medium |
| **Stage** | Phase 6 (API v2 + Search), PR-10, PR-11 |
| **Description** | Current search is Cypher `CONTAINS`. Adding FTS + facet filtering may introduce latency or incorrect result sets. |
| **Trigger** | PR-11 merges with FTS query that is slower or less accurate than `CONTAINS`. |
| **Early Warning Signal** | Search latency >200ms. Result count diverges from v1 for identical queries. User complaints about missing results. |
| **Mitigation** | 1. Benchmark FTS before PR-11 merges (<200ms target). 2. Maintain v1 search as fallback during shadow read. 3. Gradual rollout: 10% → 50% → 100% of search traffic. 4. Search result diff monitoring. |
| **Contingency** | Toggle `k_taxonomy_v2 = false`. Revert to `CONTAINS` fallback. |
| **Contingency Owner** | Backend Engineer |
| **Time-to-Rollback Threshold** | 5 minutes (feature flag toggle) |
| **Monitoring** | Search latency metrics, result diff rate, user feedback |

---

## R05: Governance Gap — No Backbone Change Process

| Field | Value |
|-------|-------|
| **Severity** | 🟠 High |
| **Probability** | High |
| **Stage** | Phase 1 (Backbone), Phase 10 (Governance), PR-01, PR-15 |
| **Description** | Without a documented change process, backbone drift is inevitable. AI may modify L1–L2. Stewards may conflict. |
| **Trigger** | Multiple PRs attempt to modify backbone without steward approval. AI tool proposes L1–L2 changes. |
| **Early Warning Signal** | Git history shows backbone files modified without PR reference. Steward roster has unassigned domains. Review queue has unapproved proposals. |
| **Mitigation** | 1. `steward_runbook.md` committed before Phase 1 begins. 2. CI check: backbone file changes require steward approval. 3. AI policy explicitly prohibits L1–L2 AI modification. 4. Backbone tagged with semver; changes require version bump. |
| **Contingency** | Freeze backbone changes. Convene stewards to resolve conflicts. Revert unauthorized changes. |
| **Contingency Owner** | Governance Lead |
| **Time-to-Rollback Threshold** | 1 hour (revert commits + steward review) |
| **Monitoring** | Git history audit, PR approval labels, steward activity log |

---

## R06: Data Loss If Old Nodes Deleted

| Field | Value |
|-------|-------|
| **Severity** | 🟠 High |
| **Probability** | Low |
| **Stage** | Phase 8 (Migration), Phase 9 (Shadow Graph), PR-13, PR-14 |
| **Description** | Migration or shadow graph build may accidentally delete or overwrite existing Neo4j nodes. |
| **Trigger** | Migration script uses `MERGE` incorrectly. Shadow graph build overwrites primary labels. |
| **Early Warning Signal** | Node count drops unexpectedly. Parity check reports missing nodes. Neo4j backup size decreases. |
| **Mitigation** | 1. Migration script never deletes nodes (only creates new ones + redirects). 2. Shadow graph uses distinct labels (`__shadow__`). 3. Neo4j backup taken before every migration. 4. Parity check runs before and after migration. 5. Rollback script restores from backup. |
| **Contingency** | Restore Neo4j from backup. Re-run migration from clean state. |
| **Contingency Owner** | Data Engineer |
| **Time-to-Rollback Threshold** | 30 minutes (Neo4j restore from backup) |
| **Monitoring** | Neo4j node count metrics, backup integrity checks, parity check results |

---

## R07: AI Corrupts Backbone

| Field | Value |
|-------|-------|
| **Severity** | 🟠 High |
| **Probability** | Medium |
| **Stage** | Phase 1 (Backbone), Phase 3 (Facets), Phase 10 (Governance) |
| **Description** | AI-assisted classification or proposal may introduce incorrect facets, wrong domain assignments, or invalid backbone nodes. |
| **Trigger** | AI batch job runs without human review. Review queue bypassed. Confidence threshold too low. |
| **Early Warning Signal** | `validate_facets.py` reports errors after AI batch. Steward review queue has >50% rejection rate. Backbone validation fails. |
| **Mitigation** | 1. AI policy: L1–L2 are human-only. L3–L4 AI proposals require steward review. 2. Confidence threshold: 0.85 minimum for facet proposals. 3. Batch jobs create proposals, not direct commits. 4. Validation script runs before any proposal is applied. |
| **Contingency** | Revert AI batch commits. Restore from pre-batch backup. Review and re-classify manually. |
| **Contingency Owner** | Data Engineer + Steward |
| **Time-to-Rollback Threshold** | 1 hour (revert commits + validation) |
| **Monitoring** | AI proposal acceptance rate, validation error rate, steward review time |

---

## R08: Performance — Jurisdiction Resolution

| Field | Value |
|-------|-------|
| **Severity** | 🟡 Medium |
| **Probability** | Medium |
| **Stage** | Phase 4 (Jurisdiction), Phase 6 (API v2), PR-02b, PR-11 |
| **Description** | Jurisdiction precedence resolver (`local > regional > national`) may introduce latency for complex queries. |
| **Trigger** | `POST /v2/resolve` latency >500ms for multi-jurisdiction queries. |
| **Early Warning Signal** | API latency metrics exceed target. Neo4j query plan shows full graph scan. |
| **Mitigation** | 1. Precompute jurisdiction chains at ingestion time. 2. Add Neo4j index on `Jurisdiction.code`. 3. Cache resolved contexts in PostgreSQL. 4. Benchmark before PR-11 merges. |
| **Contingency** | Disable jurisdiction resolution for non-critical queries. Return national-level defaults. |
| **Contingency Owner** | Backend Engineer |
| **Time-to-Rollback Threshold** | 5 minutes (feature flag toggle for jurisdiction resolution) |
| **Monitoring** | API latency metrics, Neo4j query plan analysis, cache hit rate |

---

## R09: Operational Complexity of Jurisdiction Packs

| Field | Value |
|-------|-------|
| **Severity** | 🟡 Medium |
| **Probability** | Medium |
| **Stage** | Phase 4 (Jurisdiction), PR-08 |
| **Description** | Each jurisdiction pack is a YAML file + Neo4j subgraph + PostgreSQL rows. Managing multiple packs increases operational overhead. |
| **Trigger** | Second jurisdiction pack (e.g., US-IBC) is attempted and conflicts with PH pack. |
| **Early Warning Signal** | Jurisdiction pack validation fails. Neo4j label collision. PostgreSQL foreign key conflicts. |
| **Mitigation** | 1. Jurisdiction packs are namespaced by code prefix. 2. Validation script checks for collisions before import. 3. Each pack is independently versioned. 4. Pack import is idempotent. |
| **Contingency** | Remove conflicting pack. Fix validation errors. Re-import. |
| **Contingency Owner** | Backend Engineer |
| **Time-to-Rollback Threshold** | 30 minutes (pack removal + re-import) |
| **Monitoring** | Pack validation results, import success rate, namespace collision reports |

---

## R10: Standards Mapping Ambiguity

| Field | Value |
|-------|-------|
| **Severity** | 🟡 Medium |
| **Probability** | High |
| **Stage** | Phase 5 (Standards), PR-04, PR-09 |
| **Description** | Mapping canonical concepts to external standards (OmniClass, IFC, etc.) is inherently ambiguous. Low-confidence mappings may mislead users. |
| **Trigger** | PR-09 merges with unreviewed mappings. Users report incorrect standard codes. |
| **Early Warning Signal** | Mapping confidence scores are low (<0.7). User feedback reports mismatches. Coverage gaps for critical concepts. |
| **Mitigation** | 1. All mappings have `confidence` field. 2. Default filter: `confidence >= 0.7`. 3. Mappings reviewed by domain expert before commit. 4. Mapping provenance tracked (`mapped_by`, `mapped_at`). 5. Users can flag incorrect mappings. |
| **Contingency** | Hide low-confidence mappings. Revert to no-mapping state for affected concepts. |
| **Contingency Owner** | Domain Expert |
| **Time-to-Rollback Threshold** | 15 minutes (filter toggle + mapping removal) |
| **Monitoring** | Mapping confidence distribution, user flag rate, coverage metrics |

---

## R11: Shadow Graph Parity Failure

| Field | Value |
|-------|-------|
| **Severity** | 🟠 High |
| **Probability** | Medium |
| **Stage** | Phase 9 (Shadow Graph), PR-14 |
| **Description** | Shadow graph does not produce identical results to primary graph for all v1 query patterns. |
| **Trigger** | PR-14 merges without passing parity check. Shadow read enabled despite <100% parity. |
| **Early Warning Signal** | Parity check reports <100% match. Diff shows missing nodes, wrong properties, or incorrect edges. |
| **Mitigation** | 1. Parity check is gate: no merge without 100% match. 2. Shadow read only enabled after 1-week observation. 3. Real-time parity monitoring during observation. 4. Automated alert if parity drops. |
| **Contingency** | Disable shadow read. Fix shadow graph builder. Rebuild and recheck parity. |
| **Contingency Owner** | Backend Engineer |
| **Time-to-Rollback Threshold** | 5 minutes (feature flag toggle) |
| **Monitoring** | Parity check CI job, shadow read error rate, diff metrics |

---

## R12: Migration Runner Corruption

| Field | Value |
|-------|-------|
| **Severity** | 🔴 Critical |
| **Probability** | Low |
| **Stage** | Phase 8 (Migration), PR-13 |
| **Description** | Migration runner corrupts canonical Markdown files (invalid frontmatter, lost content, wrong IDs). |
| **Trigger** | Migration script has bug in frontmatter parsing or writing. Human review misses error in diff. |
| **Early Warning Signal** | `validate_post_migration.py` fails. Git diff shows unexpected content changes. Frontmatter YAML parsing errors. |
| **Mitigation** | 1. Generate → diff → review → apply flow. 2. No direct in-place mutation. 3. Staging directory for review. 4. Validation script runs before apply. 5. Git backup branch before apply. 6. Steward reviews diff for all content changes. |
| **Contingency** | Run `rollback.py`. Restore from Git backup branch. Fix migration script. Re-run. |
| **Contingency Owner** | Data Engineer |
| **Time-to-Rollback Threshold** | 30 minutes (rollback script + Git restore) |
| **Monitoring** | Validation script results, Git diff size metrics, steward review time |

---

## R13: API v2 Contract Instability

| Field | Value |
|-------|-------|
| **Severity** | 🟠 High |
| **Probability** | Medium |
| **Stage** | Phase 6 (API v2), PR-11 |
| **Description** | v2 endpoints change after external consumers begin integration. |
| **Trigger** | PRs modify v2 response shapes after PR-11 merges. |
| **Early Warning Signal** | Contract tests fail. OpenAPI spec changes without version bump. Consumer complaints. |
| **Mitigation** | 1. v2 API versioned in path (`/v2/`). 2. Contract tests are CI gate. 3. Response shapes additive-only within major version. 4. Breaking changes require `/v3/` path. 5. API changelog maintained. |
| **Contingency** | Revert breaking PR. Maintain v2 contract. Defer changes to v3. |
| **Contingency Owner** | Backend Engineer |
| **Time-to-Rollback Threshold** | 15 minutes (PR revert) |
| **Monitoring** | Contract test pass rate, OpenAPI diff, consumer feedback |

---

## Risk Rollout Stage Mapping

| Rollout Stage | Active Risks | Primary Mitigation |
|--------------|-------------|-------------------|
| **Phase 0–1: Schema + Backbone** | R05, R07 | Steward runbook, AI policy, CI checks |
| **Phase 2: ID Migration** | R01, R06, R12 | Redirect table, backup, parity check, diff review |
| **Phase 3: Facets** | R07, R10 | Confidence thresholds, validation scripts, steward review |
| **Phase 4: Jurisdiction** | R03, R08, R09 | Rule coverage tests, benchmarking, pack validation |
| **Phase 5: Standards** | R10 | Confidence filtering, domain expert review |
| **Phase 6: API v2 + Search** | R04, R08, R13 | Benchmarks, feature flags, contract tests, gradual rollout |
| **Phase 7: Explorer** | R02 | Feature flags, fallback rendering, E2E tests |
| **Phase 8: Migration** | R06, R12 | Backup, staging, validation, rollback script |
| **Phase 9: Shadow Graph** | R11, R06 | Parity check, observation period, monitoring |
| **Phase 10: Governance** | R05, R07 | Steward runbook, AI policy, review queue |

---

## Risk Dashboard (Monitoring Checklist)

| Risk | Metric | Threshold | Alert Channel |
|------|--------|-----------|---------------|
| R01 | Parity check match rate | <100% | CI failure |
| R02 | Explorer E2E pass rate | <100% | CI failure |
| R03 | Rule coverage | <95% | Slack/Email |
| R04 | Search latency p99 | >200ms | Slack/Email |
| R05 | Unapproved backbone changes | >0 | CI failure + Slack |
| R06 | Neo4j node count delta | <-1% | Slack/Email |
| R07 | AI proposal rejection rate | >50% | Slack/Email |
| R08 | Jurisdiction resolve latency p99 | >500ms | Slack/Email |
| R09 | Pack validation failures | >0 | CI failure |
| R10 | Mapping confidence <0.7 | >20% of mappings | Slack/Email |
| R11 | Shadow parity match rate | <100% | CI failure |
| R12 | Post-migration validation errors | >0 | CI failure |
| R13 | Contract test failures | >0 | CI failure |
