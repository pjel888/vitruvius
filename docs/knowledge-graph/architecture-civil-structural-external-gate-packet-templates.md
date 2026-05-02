# Architecture Civil Structural External Gate Packet Templates

Date: 2026-05-01

These are schema templates for future externally supplied packets. They are not admitted graph truth by themselves. The gated-review runner validates structure and evidence references, writes dry-run reports under `006_System-Manifests`, and keeps all mutation/admission boundaries false unless a later purpose-built admission workflow is implemented and separately validated.

## Steward duplicate decision packet

Required fields:

- `packet_id`
- `steward`
- `decision_date`
- `authority_record_id`
- `rationale`
- `evidence_paths`
- either:
  - `decision_scope: all_current_duplicate_candidates` plus `default_action` of `preserve_contextual_duplicate` or `add_display_disambiguation`, or
  - `decisions[]` with `normalized_label`, `action`, `rationale`, and evidence.

Merge-like actions also require `survivor_node_id`, `source_rights_ids`, and `migration_evidence_paths`. The current runner only emits `steward-duplicate-apply-plan-dry-run.json`; it does not mutate labels, apply aliases, retire nodes, or write migrations.

## Project or AHJ numeric criteria packet

Required fields:

- `packet_id`
- `project_id`
- `jurisdiction_id`
- `ahj_authority`
- `steward_approval_id`
- `adopted_sources`
- `criteria[]` with `criterion_name`, `concept_path_code`, `value`, `units`, `source_id`, `adopted_edition`, `ahj_basis`, `effective_date`, and `source_rights_clearance_state`.

`source_rights_clearance_state` must be `cleared_for_declared_use`, and `protected_payload_included` must be false. Validation remains `validated_not_admitted`; no numeric graph write is performed.

## External authority ledger

Required fields per `authority_records[]`:

- `authority_id`
- `authority_type`
- `scope`
- `decision_status`
- `steward`
- `decision_date`
- `evidence_paths`

Approved or admitted records also require `source_rights_ids`. The runner validates authority ledger shape and evidence paths only; it does not authorize admission.

## Protected payload manifest

Required fields:

- `manifest_id`
- `steward`
- `decision_date`
- `authority_record_ids`
- `evidence_paths`
- `payloads[]` with `payload_id`, `source_id`, `source_rights_id`, `content_sha256`, `admitted_use`, and `exposure_policy`.

Allowed exposure policies are `hash_only`, `metadata_only`, and `non_public_internal_reference`. Payload text, quotes, standard text, table text, raw-source paths, secrets, and token/password-like fields are rejected by the payload-leak audit.

## Live promotion plan

Required fields:

- `plan_id`
- `approved_by`
- `approved_at`
- `target_environment: production`
- `backup_artifact_path`
- `restore_test_artifact_path`
- `rollback_transcript_path`

The environment must also provide production Neo4j credential names. The runner reports only missing credential names, never credential values, and remains dry-run only: no Neo4j connection or write is attempted.

## Generated readiness skeletons

Every gated-review run now writes draft-only operator skeletons beside the report:

- `steward-preserve-packet-skeleton.json`
- `criteria-packet-skeleton.json`
- `authority-ledger-skeleton.json`
- `protected-payload-manifest-skeleton.json`
- `live-promotion-plan-skeleton.json`
- `external-gate-readiness-bundle.json`

These files are generated from repo-known facts and schema requirements only. They intentionally leave steward, AHJ, source-rights, payload hash, credential, backup, restore-test, and rollback evidence fields empty. They are not authority records, do not admit graph truth, do not apply duplicate decisions, and do not authorize live promotion.

`external-gate-readiness-bundle.json` aggregates current gate statuses, skeleton paths, missing external inputs, and explicit operations not performed. It exists to make the remaining hard blockers mechanically visible without fabricating credentials, legal rights, AHJ criteria, protected content, or steward decisions.
