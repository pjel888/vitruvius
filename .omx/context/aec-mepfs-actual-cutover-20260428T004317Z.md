# AEC-MEPFS Actual Cutover Context Snapshot

- Task statement: continue the project-owner authorized AEC-MEPFS actual implementation/cutover work.
- Desired outcome: implement every locally safe AEC-MEPFS lane, and classify remaining lanes only as implemented or hard-blocked with an exact reason.
- Known facts/evidence: branch `main` is synced to `origin/main` at `94966e5f`; Explorer was already made the prelaunch AEC-MEPFS default; the current dirty tree makes `/v2/resolve*` default-on with an explicit rollback disable flag and updates route inventory/runtime threshold evidence code.
- Constraints: no Gemini; no secrets; protected content admission still requires valid rights/steward/legal authority; production Neo4j promotion still requires credentials, target identity, backup, restore proof, rollback transcript, and fresh safety gates.
- Unknowns/open questions: Kimi/Spark availability must be probed safely; production Neo4j credentials and protected-source legal authority are not assumed.
- Likely codebase touchpoints: `api/`, `explorer/`, `scripts/vitruvius/kg/`, `scripts/tests/`, `.ai/03_plans/AEC-MEPFS-Backbone/`, `.ai/05_logs/`, and `006_System-Manifests/aec-mepfs-backbone/`.
