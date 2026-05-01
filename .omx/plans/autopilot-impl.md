# Autopilot Implementation Plan: AEC-BB-S4

1. Ground state and impact evidence.
   - Confirm worktree state and keep unrelated `explorer/package.json`
     unstaged.
   - Run GitNexus impact for the new/edited symbols before code edits where
     possible.

2. Implement the file-backed parity runner.
   - Add `scripts/vitruvius/kg/backbone_parity_runner.py`.
   - Read and validate the S3 fixture through `validate_backbone_contract_file`.
   - Extract `integration_parity_runner_plan`.
   - Resolve `RUN_ID` in report paths.
   - Execute commands with a bounded subprocess adapter.
   - Write deterministic JSON reports.

3. Add focused tests.
   - Validate successful report generation.
   - Validate missing/invalid plan failure.
   - Validate failed command blocks readiness.
   - Validate safe run-id/report-path behavior.

4. Update readiness artifacts.
   - Add fourth bounded implementation packet.
   - Update scorecard, README, acceptance record, active state, and validation log.
   - Keep full runtime readiness blocked where blockers are external/runtime.

5. Verify, review, commit, push.
   - Run focused Python tests, API tests, Explorer tests, static checks, and
     GitNexus evidence.
   - Run architect/security/quality review.
   - Commit/push with Lore trailers.
