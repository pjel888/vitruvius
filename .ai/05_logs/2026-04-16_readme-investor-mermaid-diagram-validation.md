---
task: readme-investor-mermaid-diagram
phase: "09"
created: 2026-04-16
author: REVIEWER
supersedes: null
status: DRAFT
---

# README Investor Mermaid Diagram Validation — 2026-04-16

## Validation scope
Validate that the README upgrade:
1. adds an investor-readable Mermaid diagram
2. accurately explains what Vitruvius does today from source documents through governed knowledge outputs
3. clearly separates current capability from roadmap direction
4. does not overclaim unshipped AEC/compliance product layers as present-tense reality

## Environment notes
- Repo root: `/Users/philiplewis/vitruvius`
- This task is documentation-only; no code paths, builds, or runtime behavior changed.
- Validation therefore focused on README structure, wording truthfulness, diagram presence, and artifact completeness.

## Artifact validation
### Command
```bash
git status --short README.md \
  .ai/02_audits/2026-04-16_readme-investor-mermaid-diagram-audit.md \
  .ai/03_plans/2026-04-16_readme-investor-mermaid-diagram-plan.md \
  .ai/05_logs/2026-04-16_readme-investor-mermaid-diagram-validation.md
```

### Result
- `README.md` modified
- audit artifact present
- plan artifact present
- validation artifact present

### Meaning
The scoped README task files exist and are available for bounded review and commit.

## README structure validation
### Command
```bash
rg -n 'From source documents to investor value|```mermaid|Roadmap direction|Value today' README.md
```

### Result
Confirmed:
- table-of-contents entry exists
- section header exists
- Mermaid block exists
- current-value node (`Value today`) exists
- roadmap node (`Roadmap direction`) exists

### Meaning
The new explainer section is discoverable from the README table of contents and contains the expected investor-oriented visual structure.

## Content-truth validation
### Checks performed
- verified the section headline and one-line investor summary are present
- verified the diagram describes the current pipeline as: source documents → conversion → refinement → canonical knowledge → governance → value today
- verified the future/product-direction claim is visually separated with a dashed planned-next-layer edge
- verified the explanatory bullets explicitly say the dashed roadmap box is direction, not a fully shipped product surface in the repo yet

### Result
- **PASS**

### Meaning
The diagram communicates the current product truth while still showing the strategic direction. It does not collapse roadmap items into present-tense shipped capability.

## Architect verification
### Result
- Architect review verdict: **APPROVED**

### Concise findings
- investor-readable narrative is clear
- current capability vs. roadmap direction is correctly separated
- supporting bullets reinforce provenance/trust language instead of vague AI claims
- no must-fix issues were raised in architect review

## Ralph deslop pass — scoped follow-up
### Scope
- `README.md`
- `.ai/02_audits/2026-04-16_readme-investor-mermaid-diagram-audit.md`
- `.ai/03_plans/2026-04-16_readme-investor-mermaid-diagram-plan.md`

### Cleanup intent
Run the mandatory Ralph cleanup pass strictly on the README investor-diagram documentation edits, preserving truthfulness, investor readability, and roadmap-vs-current-state separation.

### Cleanup result
- inspected the scoped files for duplication, overclaiming, unnecessary jargon, and diagram-label noise
- **no cleanup edits were warranted** after architect approval

## Post-deslop verification
### Commands
```bash
git diff --check -- README.md \
  .ai/02_audits/2026-04-16_readme-investor-mermaid-diagram-audit.md \
  .ai/03_plans/2026-04-16_readme-investor-mermaid-diagram-plan.md \
  .ai/05_logs/2026-04-16_readme-investor-mermaid-diagram-validation.md
python3 - <<'PY'
from pathlib import Path
readme = Path('README.md').read_text()
validation = Path('.ai/05_logs/2026-04-16_readme-investor-mermaid-diagram-validation.md').read_text()
checks = {
    'toc_entry': '- [From source documents to investor value](#from-source-documents-to-investor-value)' in readme,
    'section_header': '## From source documents to investor value' in readme,
    'mermaid_block_count_is_1': readme.count('```mermaid') == 1,
    'current_value_node': '6. Value today' in readme,
    'roadmap_node': '7. Roadmap direction' in readme,
    'planned_edge': 'planned next layer' in readme,
    'explicit_direction_not_shipped': 'direction, not as a fully shipped product' in readme,
    'validation_log_created': 'README Investor Mermaid Diagram Validation' in validation,
    'deslop_section_created': 'Ralph deslop pass' in validation,
}
failed = [k for k,v in checks.items() if not v]
print('overall:', 'PASS' if not failed else 'FAIL')
PY
```

### Results
- `git diff --check`: PASS
- structural README truth/readability check: PASS

## Caveats
1. The README as a whole still contains stronger top-of-file AEC product framing than the current shipped state, but this task materially improves truthfulness for the specific investor explainer section.
2. Mermaid validation here is structural/readability validation inside the Markdown source; no separate external renderer was introduced for this docs-only task.

## Validation verdict
**PASS**

The README now contains a human-readable Mermaid diagram that explains what Vitruvius does today and what it is building toward, while keeping roadmap claims clearly marked as future direction.

## Architect verification
- Verdict: **APPROVED**
- Conclusion: the new README section truthfully presents Vitruvius as a document-to-knowledge pipeline today and a compliance / AEC decision-support direction next, without overclaiming the roadmap as shipped.

## Ralph deslop pass
- Scope:
  - `README.md`
  - `.ai/02_audits/2026-04-16_readme-investor-mermaid-diagram-audit.md`
  - `.ai/03_plans/2026-04-16_readme-investor-mermaid-diagram-plan.md`
  - `.ai/05_logs/2026-04-16_readme-investor-mermaid-diagram-validation.md`
- Result: no cleanup edits were warranted after bounded inspection.
- Post-deslop verification: PASS.

## Final top-of-README truth-alignment pass
### Change made
Softened the README opening so it now presents Vitruvius first as an **auditable document-to-knowledge pipeline today**, and only then frames the AEC constraint-solver as the **strategic direction**.

### Fresh verification
- `git diff --check -- README.md` → PASS
- Architect follow-up verdict on revised opening language → **APPROVED**

### Meaning
The top of the README now matches the new investor Mermaid section instead of competing with it. The document leads with current shipped truth and preserves the larger AEC vision as roadmap context.
