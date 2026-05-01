# AEC-MEPFS Actual Implementation Context

## Task statement
Project owner directive: move from prep/rehearsal/closure into actual AEC-MEPFS implementation/cutover where locally implementable; final lane statuses must be implemented or hard-blocked with exact reason.

## Desired outcome
Implement runtime resolver mounting/default policy, Explorer default adoption, runtime threshold adoption for implemented runtime surfaces, and produce hard blockers for Neo4j live promotion/protected content where credentials/legal authority are absent. Commit and push verified evidence.

## Known constraints
No Gemini. Use Kimi if available. Use Spark/native subagents for focused parallel work if useful. Do not print secrets/env values. No unsafe production mutation without backup/restore/rollback proof. Protected content requires valid legal/steward/source-rights authority. Team runtime not auto-launched because this session is outside tmux.

## Likely touchpoints
.ai/03_plans/AEC-MEPFS-Backbone, .ai/05_logs, 006_System-Manifests/aec-mepfs-backbone, api/index.ts, api/v2Resolver.test.ts, api/v2Backbone.test.ts, explorer, scripts/vitruvius/kg, scripts/tests.
