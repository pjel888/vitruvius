# Explorer Shell Layout Cleanup Plan

**Date:** 2026-04-24
**Audit:** `.ai/02_audits/2026-04-24_explorer_shell_layout_ux_audit.md`

## Objective

Improve the Explorer shell layout without changing the graph rendering. The work should make the header, right inspector rail, and sidebar controls feel grid-aligned, intentional, and reliable.

## Implementation Steps

1. Fix inspector auto-open behavior.
   - Auto-open the inspector only when a new node/edge selection appears.
   - Preserve the user's explicit minimize action while the same selection remains active.

2. Rework the inspector header cell.
   - Keep the open cell at `w-96` and collapsed cell at `w-10`.
   - Put graph summary on the left.
   - Put API status pill and minimize/maximize button in a horizontal right-side group with a clear gap.

3. Reinforce the design mandate.
   - Add spacing guidance for compact, grouped, and region-level UI.
   - Capture that sidebar state controls should remain in the sidebar-aligned header cell.

4. Lock behavior with tests.
   - Extend the Explorer integration test to prove minimize stays minimized for the same selection.
   - Prove a new selection reopens the inspector.

5. Verify.
   - Run targeted lint for touched Explorer files.
   - Run relevant Explorer interaction/integration tests.
   - Run production build.
   - Run `design.md` lint for the mandate file.
   - Run `git diff --check`.
