---
task: aec-mepfs-backbone
phase: source-currentness-evidence
created: 2026-04-25
author: CODEX
status: EVIDENCE-COLLECTED-MANUAL-REVIEW-REQUIRED
---

# Source Currentness Evidence Pack

## Purpose

Record official-source accessibility and currentness evidence for the S6
source-rights registry candidates.

This is evidence, not legal clearance and not canonical admission.

## Generated Report

Report:
`006_System-Manifests/aec-mepfs-backbone/source-currentness/20260425T140712Z/source-currentness-report.json`

Summary:

- source rows checked: 29
- official URLs checked: 31
- URLs accessible by curl with default TLS verification: 26
- source rows with all declared URLs accessible: 24
- source rows with no declared URL accessible by curl: 5
- source rows with partial accessibility: 0

The earlier Python `urllib` attempt failed because the local Python certificate
store rejected otherwise reachable HTTPS endpoints. The retained S7 evidence
uses `curl` with default TLS verification instead.

## Rows Requiring Manual Review

| Source ID | Source family | Reported issue | Current disposition |
|---|---|---|---|
| `SRC-PH-BFP-RA9514-RIRR` | RA 9514 Fire Code RIRR | BFP URL returned HTTP 403 to curl | manual currentness review required |
| `SRC-PH-DHSUD-BP220` | BP 220 economic/socialized housing | DHSUD PDF returned HTTP 403 to curl | manual currentness review required |
| `SRC-PH-PHIVOLCS-HAZARD-MAPS` | PHIVOLCS hazard maps | PHIVOLCS page produced malformed header handling in curl after redirect | manual currentness review required |
| `SRC-PH-DENR-MGB-GEOHAZARD` | DENR-MGB geohazard maps | MGB URL returned HTTP 403 to curl | manual currentness review required |
| `SRC-PH-PSA-PSGC` | PSGC administrative geography | PSA URL returned HTTP 403 to curl | manual currentness review required |

## External Evidence Notes

- Neo4j and database rollback evidence are handled in
  `neo4j-rollback-rehearsal-evidence.md`, not this source pack.
- PHIVOLCS and MGB hazard sources remain contextual hazard overlays, not legal
  obligations unless a later legal overlay says otherwise.
- BFP, DHSUD, PHIVOLCS, MGB, and PSA rows should not be rejected solely because
  curl could not fetch them; they should be reviewed manually in a browser and
  assigned an admission-time currentness decision.

## Admission Rule

Rows with `manual currentness review required` may remain in the planning
candidate registry, but they cannot be used to claim current authority, seed
canonical source content, or support legal overlay extraction until a human
reviewer records a currentness decision.

All rows remain within their declared source-rights class. No row is cleared for
content ingest by this evidence pack.
