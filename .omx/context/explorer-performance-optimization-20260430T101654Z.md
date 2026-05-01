# Explorer performance optimization context snapshot

- task statement: Optimize Vitruvius Explorer performance for the architecture / AEC / LEA-ALE knowledge graph while preserving current UX/UI and rights-safe learner-facing graph boundaries.
- desired outcome: Measured baseline, real repository optimizations to loading/index/search/highlight/neighborhood/render workload, regression tests, validation report, Kimi advisory/final audit, no UX redesign.
- known facts/evidence: Current graph reported about 9,834 nodes and 12,970 relationships; source-rights rows about 105; current API/Explorer source pinned to file-backed shadow staging; learner-facing bad-label hits previously 0; no protected source payloads; no Neo4j/live promotion or KG rebuild/reset authorized.
- constraints: Preserve React/Vite/Tailwind/Zustand/React Query/vis-network UX; do not migrate renderer without evidence; do not use Codex Spark; use Kimi for advisory architecture review and final audit; do not perform destructive graph operations or protected-source ingestion; Windows-safe generated filenames.
- unknowns/open questions: Actual current graph artifact path/size, Explorer load/query hot paths, whether worker/index exists, feasible browser tooling, Kimi CLI syntax, current uncommitted user changes in overlapping files.
- likely codebase touchpoints: explorer/src, api graph endpoints/tests, 006_System-Manifests/aec-mepfs-backbone/shadow-staging, package scripts, Explorer tests and benchmarks.
