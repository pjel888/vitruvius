# Continuous Vitruvius Next Actions

Last updated: 2026-05-02T02:20:03Z

1. Implement Resource Layer standards-context cleanup workflow for ASCE 7 and ACI 318 without inventing edition/version/scope values.
2. Add per-P1-packet ontology review status (`unreviewed`, `kimi_reviewed`, `human_review_needed`, `human_reviewed`, `rejected`, `deferred`) and UI filters without auto-approval.
3. Improve P0 Concrete/Reinforced Concrete approval packet clarity and admission preview while keeping both groups proposed until truthful approval exists.
4. Add a bootstrap/coverage plan for custody-critical files that do not yet have transaction manifests, especially Resource Layer registry files.
5. If a real packet HMAC key is configured, regenerate P1 packets so signature status becomes `valid` instead of unsigned.
