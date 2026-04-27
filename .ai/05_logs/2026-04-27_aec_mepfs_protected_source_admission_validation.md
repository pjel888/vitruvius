# AEC-MEPFS Protected Source Admission Validation

```yaml
date: 2026-04-27
lane: protected-source-admission
classification: GREEN_METADATA_ONLY_ZERO_CONTENT_PROOF
starting_commit: a2590084
ending_commit: pending
branch: main
packet: .ai/03_plans/AEC-MEPFS-Backbone/2026-04-27_protected_source_admission_packet.md
```

## Scope

This lane completes protected-source admission work to the repo-actionable, metadata-only boundary. It does not ingest protected standards, legal clauses, tables, figures, datasets, local caches, or canonical source content.

## Files inspected

- `.ai/03_plans/AEC-MEPFS-Backbone/standards-legal-source-pack.md`
- `.ai/03_plans/AEC-MEPFS-Backbone/legal-and-steward-admission-record.md`
- `.ai/03_plans/AEC-MEPFS-Backbone/canonical-source-admission-packet.md`
- `.ai/03_plans/AEC-MEPFS-Backbone/registry-candidates/source-rights-registry.json`
- `006_System-Manifests/aec-mepfs-backbone/source-currentness/20260425T140712Z/source-currentness-report.json`
- `006_System-Manifests/aec-mepfs-backbone/source-currentness/20260425T144600Z/manual-currentness-resolution-report.json`
- `scripts/vitruvius/kg/backbone_contracts.py`

## Files changed

- `.ai/03_plans/AEC-MEPFS-Backbone/2026-04-27_protected_source_admission_packet.md`
- `.ai/05_logs/2026-04-27_aec_mepfs_protected_source_admission_validation.md`
- `scripts/vitruvius/kg/backbone_source_admission.py`
- `scripts/tests/test_kg_backbone_source_admission.py`
- `006_System-Manifests/aec-mepfs-backbone/source-admission/20260427T121648Z/source-admission-report.json`

## Implementation summary

- Added a protected-source admission packet that admits metadata/reference evidence only and keeps protected content ingest externally blocked.
- Added a file-backed source admission preflight reporter.
- The reporter validates the existing 29 source-rights rows against currentness evidence and manual currentness exception rows.
- The reporter fails closed on:
  - `content_ingest` intent in `source_rights_class`, `allowed_use_class`, `intended_use`, or `max_admitted_use`.
  - non-metadata/reference source-rights classes.
  - missing currentness coverage.
  - protected payload keys and known aliases such as `clauseText`, `source_payload`, and nested `text`.
  - unsafe run IDs and output/source paths.
- After Spark review, the report no longer claims API/Explorer/Neo4j/KG runtime surfaces were exercised by this metadata-only preflight.

## Generated artifact

- `006_System-Manifests/aec-mepfs-backbone/source-admission/20260427T121648Z/source-admission-report.json`

Key artifact facts:

- `ok: true`
- `source_rights_rows: 29`
- `metadata_only_rows: 29`
- `content_ingest_rows: 0`
- `protected_payload_key_hits: 0`
- `missing_currentness_rows: 0`
- `protectedContentIngestAuthorized: false`
- `canonicalContentAdmissionAuthorized: false`
- `contentIngestExternalBlocked: true`
- `runtimeSurfaceClaimsMade: false`

## Commands and results

```bash
python3 -m compileall -q scripts/vitruvius/kg/backbone_source_admission.py
# pass

PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_source_admission.py -q
# 9 passed

PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_source_admission.py scripts/tests/test_kg_backbone_contracts.py scripts/tests/test_kg_backbone_shadow_report_reader.py -q
# 82 passed

PYTHONPATH=scripts python3 -m vitruvius.kg.backbone_source_admission --run-id 20260427T121648Z
# ok true; report generated

git diff --check
# pass
```

## Spark review

Attempted with `codex exec -m gpt-5.3-codex-spark -s read-only`.

Initial findings:

1. High: content-ingest intent was detected only from `source_rights_class` and could miss `allowed_use_class`, `intended_use`, or `max_admitted_use`.
2. Medium: protected-payload check was key-name-only and missed aliases such as `protectedContent`, `source_payload`, and generic payload/text fields.
3. Medium: report status overclaimed runtime-surface safety for API/Explorer/Neo4j/KG even though the preflight is file-backed metadata validation.

Disposition:

- Accepted all three findings.
- Added content-ingest alias-field detection and fail-closed tests.
- Added protected payload aliases and fail-closed tests.
- Reworded report status to `runtimeSurfaceClaimsMade=false` and added `runtime_surface_scope` clarifying API/Explorer/Neo4j/KG checks are not performed here.
- Spark fixed-diff review found no remaining actionable issues.

## Kimi review

Kimi/Moonshot was attempted twice:

- Full fixed-diff review via `kimi --quiet` timed out with no final output.
- Short summary review via `kimi --quiet -p ...` also timed out with no final output.

Earlier non-quiet Kimi invocation echoed the diff through the terminal UI but did not produce actionable final findings. Missing Kimi output is documented as non-blocking per the four-lane directive.

## Safety invariants

Confirmed for this lane:

- broad/global `LIVE_RUNTIME_AUTHORIZED`: not introduced.
- protected content ingest: not authorized and not performed.
- canonical source content admission: not authorized and not performed.
- local protected payload/cache: not introduced.
- source payload exposure: not authorized.
- Neo4j/KG mutation: no code path added and no mutation command run.
- API/Explorer runtime behavior: not changed by this lane.

## Residual risks / next boundary

Protected content ingest remains `EXTERNAL_BLOCKED`. A future content admission packet must name exact source rows, payload fields, legal/licensing/steward authority, retention policy, exposure policy, and rollback/removal procedure before any protected text/table/figure/dataset/clause can be ingested.
