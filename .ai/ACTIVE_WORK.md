# Active Work

**Updated:** 2026-04-21  
**Scope:** only active and incomplete work belongs here

## NOW

### 1. AEC execution-readiness decision
- **Status:** planned
- **Why it matters:** AEC is the only major remaining implementation family still represented as potentially live.
- **Evidence:** `/.ai/03_plans/AEC_ENGINE_MASTER_IMPLEMENTATION_PLAN.md`, `/.ai/IMPLEMENTATION_MATRIX.md`
- **Next concrete action:** decide whether to open a real execution lane or demote the family to long-term reference until runtime roots exist.
- **Dependency / blocker:** runtime implementation roots and a reduced execution packet are not yet verified.

### 2. Verification refresh for unverified claims
- **Status:** planned
- **Why it matters:** some success claims are log-backed but not freshly rerun.
- **Evidence:** `/.ai/05_logs/2026-04-20_full-test-suite-green-validation.md`, `/.ai/IMPLEMENTATION_MATRIX.md`
- **Next concrete action:** rerun targeted verification before making fresh “green” claims after future implementation changes.
- **Dependency / blocker:** none; triggered by future code changes.

## NEXT

### 3. Skills / agents consolidation
- **Status:** planned
- **Why it matters:** duplicated skill and agent layers create ambiguity about what is active.
- **Evidence:** `/.ai/11_skills/`, `/.ai/skills/`, `/.ai/12_agents/`
- **Next concrete action:** choose one canonical skill layer and demote imported/unrelated packs to archive/reference.
- **Dependency / blocker:** not blocking the core operating surface.

### 4. Historical transcript demotion
- **Status:** planned
- **Why it matters:** transcripts are useful history but not active planning state.
- **Evidence:** `/.ai/chatGPT-Conversations/`
- **Next concrete action:** move or formally demote transcript material into archive/reference navigation.
- **Dependency / blocker:** reference impact should be mapped before moving files.
