# Active Work

**Updated:** 2026-04-21  
**Scope:** only active and incomplete work belongs here

## NOW

### 1. Plan-family slimming
- **Status:** in_progress
- **Why it matters:** the active plan surface is still larger than the true live work surface.
- **Evidence:** `/.ai/03_plans/INDEX.md`, `/.ai/archive/ARCHIVE_INDEX.md`
- **Next concrete action:** keep only the dispatcher + minimal AEC execution packet in the active index and classify the remaining AEC planning burst as reference-only.
- **Dependency / blocker:** historical AEC and laws-wave plan bursts still occupy the live plans directory.

### 2. Active-doc reference integrity
- **Status:** in_progress
- **Why it matters:** active docs must not point to stale `/docs` paths or non-existent aggregate viewer artifacts.
- **Evidence:** `/.ai/10_state/laws-wave-status.json`, `/.ai/03_plans/laws-wave/LAWS_WAVE_ARTIFACT_INDEX.md`
- **Next concrete action:** keep active-doc references constrained to existing `.ai/` and repo paths, and remove any invalid plan filename references from the live index.
- **Dependency / blocker:** older reference docs still carry legacy path patterns.

## NEXT

### 3. AEC execution-readiness decision
- **Status:** planned
- **Why it matters:** AEC is the only major remaining implementation family still represented as potentially live.
- **Evidence:** `/.ai/03_plans/AEC_ENGINE_MASTER_IMPLEMENTATION_PLAN.md`, `/.ai/IMPLEMENTATION_MATRIX.md`
- **Next concrete action:** decide whether to open a real execution lane or demote the family to long-term reference until runtime roots exist.
- **Dependency / blocker:** runtime implementation roots and a reduced execution packet are not yet verified.

### 4. Verification refresh for unverified claims
- **Status:** planned
- **Why it matters:** some success claims are log-backed but not freshly rerun.
- **Evidence:** `/.ai/05_logs/2026-04-20_full-test-suite-green-validation.md`, `/.ai/IMPLEMENTATION_MATRIX.md`
- **Next concrete action:** rerun targeted verification before making fresh “green” claims after future implementation changes.
- **Dependency / blocker:** none; triggered by future code changes.

## LATER

### 5. Skills / agents consolidation
- **Status:** planned
- **Why it matters:** duplicated skill and agent layers create ambiguity about what is active.
- **Evidence:** `/.ai/11_skills/`, `/.ai/skills/`, `/.ai/12_agents/`
- **Next concrete action:** choose one canonical skill layer and demote imported/unrelated packs to archive/reference.
- **Dependency / blocker:** not blocking the core operating surface.

### 6. Historical transcript demotion
- **Status:** planned
- **Why it matters:** transcripts are useful history but not active planning state.
- **Evidence:** `/.ai/chatGPT-Conversations/`
- **Next concrete action:** move or formally demote transcript material into archive/reference navigation.
- **Dependency / blocker:** reference impact should be mapped before moving files.
