# AEC-MEPFS Protected Source Admission Packet

```yaml
status: BOUNDARY_APPROVED_METADATA_ONLY
created: 2026-04-27
authority: project-owner-directive-four-gated-lanes
lane: protected-source-admission
classification: GREEN_METADATA_ONLY_ZERO_CONTENT_PROOF
baseline_commit: a2590084
protected_content_ingest_authorized: false
canonical_content_admission_authorized: false
```

## 1. Purpose

Complete all repo-actionable protected-source admission preparation while
preserving the no-ingest boundary for protected standards, legal clauses,
tables, figures, datasets, and local protected caches.

This packet admits only metadata/reference evidence that is already represented
in the source-rights registry and currentness artifacts. It does not admit source
text or canonical legal/source content.

## 2. Authority and baseline

- Umbrella packet: `2026-04-27_four_gated_lanes_reopen_packet.md`.
- Source baseline: `standards-legal-source-pack.md`.
- Existing source-rights candidate registry:
  `.ai/03_plans/AEC-MEPFS-Backbone/registry-candidates/source-rights-registry.json`.
- Currentness evidence:
  `006_System-Manifests/aec-mepfs-backbone/source-currentness/20260425T140712Z/source-currentness-report.json`.
- Manual exception resolution:
  `006_System-Manifests/aec-mepfs-backbone/source-currentness/20260425T144600Z/manual-currentness-resolution-report.json`.
- Legal/steward record: `legal-and-steward-admission-record.md`.
- Canonical admission record: `canonical-source-admission-packet.md`.

## 3. Allowed scope in this packet

- Validate source-rights rows as metadata/reference only.
- Cross-check currentness rows cover every source-rights row.
- Preserve manual exception resolutions as reference/metadata evidence only.
- Generate a zero-content-ingest proof report under
  `006_System-Manifests/aec-mepfs-backbone/source-admission/<RUN_ID>/`.
- Add tests proving content-ingest rows and protected payload keys fail closed.

## 4. Explicitly blocked scope

- Protected standards text/table/figure/clause ingestion.
- Government legal clause extraction into canonical content.
- Local caching of protected datasets or source payloads.
- Treating URL reachability as legal clearance.
- Canonical source content admission.
- Neo4j/KG mutation.
- Explorer/API exposure of protected payloads.
- Broad/global `LIVE_RUNTIME_AUTHORIZED`.

## 5. Admission status

| Admission surface | Status | Reason |
|---|---|---|
| Metadata/reference source-family rows | prepared and validated | Existing 29 candidate rows are reference/crosswalk only. |
| Currentness evidence | prepared for declared use | Currentness evidence exists, with manual exception caveats. |
| Protected content ingest | blocked | No valid legal/source-rights record authorizes content ingest. |
| Canonical source content | blocked | Canonical admission remains zero-content metadata staging only. |
| Runtime source payload exposure | blocked | API/Explorer source preview remains sanitized metadata only. |

## 6. Verification plan

```bash
python3 -m compileall -q scripts/vitruvius/kg/backbone_source_admission.py
PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_source_admission.py -q
PYTHONPATH=scripts python3 -m vitruvius.kg.backbone_source_admission --run-id <RUN_ID>
git diff --check
```

## 7. Evidence artifacts

- Source admission report:
  `006_System-Manifests/aec-mepfs-backbone/source-admission/<RUN_ID>/source-admission-report.json`
- Validation log:
  `.ai/05_logs/2026-04-27_aec_mepfs_protected_source_admission_validation.md`

## 8. Completion criteria

- Report confirms all registry rows are metadata/reference only.
- Report confirms no `content_ingest` intent in any supported rights/intended-use
  field and no protected payload keys or known payload-key aliases.
- Report confirms currentness evidence covers every registry row.
- Content ingest remains `EXTERNAL_BLOCKED` unless a later source-rights/legal
  packet records valid authority for exact fields and payloads.
- No API, Explorer, Neo4j, KG rebuild, or protected source cache behavior changes
  are made by this packet. This preflight does not claim to exercise those
  runtime surfaces; they remain covered by their dedicated packets and tests.

## 9. Next boundary

Protected source content admission remains `EXTERNAL_BLOCKED`. A future content
admission packet must name the exact source row, payload fields, legal/licensing
record, retention policy, exposure policy, and rollback/removal procedure before
any protected source text, table, figure, dataset, or clause is ingested.
