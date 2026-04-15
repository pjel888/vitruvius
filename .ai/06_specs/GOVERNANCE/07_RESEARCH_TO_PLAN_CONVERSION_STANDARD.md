# Vitruvius Research-to-Plan Conversion Standard

## Purpose
This document defines how exploratory research becomes implementation-ready planning in Vitruvius.

Vitruvius produces rich research artifacts. That is a strength only if those artifacts are translated into executable plans without collapsing exploration into premature implementation. This standard preserves the distinction between:
- possibility
- recommendation
- approved execution

## Core Principle
Research is not code.  
Research informs audits.  
Audits constrain plans.  
Plans govern implementation.

## Scope
This standard applies to:
- conceptual architecture research
- technical surveys
- tradeoff documents
- design-space explorations
- external references gathered for future implementation
- consolidated research documents
- subsystem research used to derive implementation work

---

## Section 1 — Research Document Status

All research documents must be treated as exploratory unless explicitly promoted into a different status artifact.

### Research Characteristics
A research document may contain:
- conceptual proposals
- alternatives
- tradeoffs
- comparative surveys
- open questions
- preferred directions
- risks
- technical possibilities

### Research Does Not Automatically Authorize
- direct coding
- architectural finality
- dependency adoption
- policy change
- truth-governance change

### Rule
Research informs planning. It does not replace planning.

---

## Section 2 — Conversion Pipeline

The required pipeline is:

1. Research review
2. Research extraction summary
3. Audit against current repo reality
4. Gap identification
5. Implementation plan derivation
6. Plan critique
7. Execution checklist
8. Validation plan

This is how a conceptual document becomes executable work.

---

## Section 3 — Research Review Requirements

Before deriving a plan from research, identify:

- what the document is proposing
- what the document is prescribing
- what parts are exploratory only
- what assumptions depend on missing infrastructure
- what open questions remain unresolved
- what areas conflict with current architecture or roadmap
- what parts belong to future phases rather than current work

### Rule
Do not derive implementation directly from inspirational language without extracting precise claims.

---

## Section 4 — Research Extraction Summary

For every research document used to drive work, create a concise extraction summary that answers:

- Proposed subsystem(s)
- Recommended technologies
- Required boundaries
- Key risks
- Open questions
- Claimed benefits
- Dependencies
- Suggested sequence
- Unresolved assumptions

This summary becomes the bridge between research and audit.

---

## Section 5 — Audit Against Repo Reality

Once research claims are summarized, compare them to the actual repo.

### Required Audit Questions
- What already exists?
- What is partially implemented?
- What is missing?
- What conflicts with current architecture?
- What parts of the research are already obsolete?
- What parts require prerequisite work not yet done?
- What roadmap phase does this belong to?
- What state files or decisions already constrain it?

### Rule
A plan derived from research must be grounded in current implementation reality, not in aspiration.

---

## Section 6 — Deriving the Implementation Plan

The implementation plan should include only work that is:
- in scope
- phase-appropriate
- bounded
- architecture-compatible
- testable
- realistically executable

### The Plan Must Convert
- concepts into modules
- goals into tasks
- tradeoffs into explicit decisions
- open questions into stop conditions or deferred items
- technical claims into validation requirements

### The Plan Must Not
- preserve all alternatives indefinitely
- pretend unresolved research questions are already solved
- collapse future-phase ideas into current-phase work without approval

---

## Section 7 — Plan Critique Requirements

Every research-derived plan must critique itself.

### Critique Questions
- Which assumptions from the research are still unproven?
- Which recommended technologies are risky or premature?
- Which pieces are phase-inappropriate?
- What hidden dependencies exist?
- What performance or correctness claims require benchmarks?
- What boundary violations are possible?
- Which parts should be deferred instead of implemented now?

### Rule
Research often sounds more complete than it is. Critique is what prevents enthusiasm from becoming architecture drift.

---

## Section 8 — Separation of Exploration and Commitment

Vitruvius should explicitly separate:
- research recommendation
- audited feasibility
- approved plan
- executed implementation

Suggested language:
- “research suggests”
- “audit confirms”
- “plan proposes”
- “implementation completes”

This prevents status confusion.

---

## Section 9 — Research Confidence and Maturity

Not all research is equally mature.

### Suggested Maturity Labels
- exploratory
- promising
- phase-ready
- blocked by prerequisites
- deferred
- superseded

### Rule
A research idea should not become a plan unless it is mature enough for the current phase.

---

## Section 10 — Open Questions Handling

Research documents often contain open questions.

### Options for Open Questions
- resolve before planning
- preserve as explicit plan risks
- defer to future phase
- mark as stop condition
- create spike or experiment task

### Rule
Open questions must not be silently buried in implementation.

---

## Section 11 — Research-Derived Plan Template

### Research Source
- file:
- version/date:
- author/source:

### Summary
- subsystem:
- thesis:
- recommended stack:
- key benefits:
- key risks:
- open questions:

### Audit Alignment
- current implementation:
- conflicts:
- prerequisites:
- roadmap phase:
- state alignment:

### Plan Derivation
- in-scope work:
- deferred work:
- blocked work:
- validation requirements:
- benchmark requirements:
- doc updates required:

### Plan Critique
- weak assumptions:
- likely failure points:
- unresolved questions:
- why this is still acceptable or not acceptable now:

---

## Section 12 — Agent Rules

Agents must not:
- treat research language as direct instruction to code
- skip the audit stage because research is detailed
- import entire conceptual stacks without phase control
- hide unresolved research questions

Agents must:
- convert research into bounded planning artifacts
- identify what is now vs later
- preserve open questions honestly
- update plans when research is superseded or clarified

---

## Final Principle
Research expands possibility.  
Planning narrows possibility into execution.  
Vitruvius must preserve that discipline if it wants to remain coherent.
