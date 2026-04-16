---
task: readme-investor-mermaid-diagram
phase: "05"
created: 2026-04-16
author: IMPLEMENTER
supersedes: null
status: archived
archive_status: complete
archived_at: 2026-04-16T00:11:22Z
---

# README Investor Mermaid Diagram Plan — 2026-04-16

## Objective
Add a Mermaid diagram to `README.md` that explains Vitruvius from source-document intake through current outputs and future product direction in language that is readable to investors and non-technical stakeholders.

## In scope
- `README.md`
- table of contents update if needed
- one Mermaid diagram section
- short supporting explanation below the diagram
- validation log for the README change

## Out of scope
- broad README rewrite
- roadmap/status corrections outside what is necessary for the diagram section
- product-claim expansion beyond current repo truth
- code changes

## Design choice
Add a new section after `## Vitruvius in plain English`.

Why there:
- the reader has just received the human explanation
- the diagram can translate that explanation into a memorable visual flow
- the technical architecture diagram can remain later for deeper readers

## Diagram design
The Mermaid diagram should show:
1. **source documents**
2. **conversion to machine-readable text**
3. **refinement / normalization**
4. **canonical knowledge creation**
5. **review / validation**
6. **auditable graph / queryable knowledge outputs**
7. **planned next product layer**

## Wording rules
- use business-readable labels, not internal-only jargon
- use one clearly marked `planned` / `future` node or subgraph
- describe current value in terms of:
  - auditable knowledge
  - traceable answers
  - reusable rule assets
- describe future value in terms of:
  - compliance workflows
  - scenario analysis
  - AEC decision support

## Plan Critique
### C001 — overclaim risk
If the diagram makes future AEC solving look fully shipped, README truth drifts.
- **Mitigation:** explicitly label the roadmap/future node as planned.

### C002 — under-explaining current value
If the diagram focuses only on internal stages, it still reads like developer plumbing.
- **Mitigation:** include a current-value node that names the investor-visible outcome.

### C003 — too much complexity
A diagram with too many implementation branches will overwhelm non-technical readers.
- **Mitigation:** use one simple end-to-end line with limited branching.

### C004 — contradiction with existing README framing
If the new section sounds radically different from the rest of the README, it creates narrative whiplash.
- **Mitigation:** position the new section as the high-level explainer, while preserving the existing deeper technical sections below.

## Execution Checklist
- [ ] G001 — add audit artifact
- [ ] G002 — insert new Mermaid explainer section into `README.md`
- [ ] G003 — update README table of contents
- [ ] G004 — keep claims aligned with roadmap and current status
- [ ] G005 — validate Mermaid block renders structurally and README remains coherent
- [ ] G006 — architect-review the final wording for truthfulness
- [ ] G007 — write validation log
