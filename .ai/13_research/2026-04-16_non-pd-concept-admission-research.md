# Research Pack — Non-PD Concept Admission Slice

## Purpose
Identify the smallest law-specific concept additions likely to improve truthful relationship extraction for `BP-344` and `BP-220` after source admission and M2B stage wiring are already complete.

## Fresh evidence
Current post-M2B official state:
- `PD-1096` → covered
- `RA-9514` → covered
- `BP-344` → partial
- `BP-220` → partial

Blocking evidence already logged:
- `/.ai/05_logs/2026-04-16_non-pd-concept-gap-validation.md`

## Phrase-frequency evidence from refined markdown
### BP-344
Observed phrase counts in the refined markdown:
- `accessible ramps` → 10
- `toilets and baths` → 3
- `signage` → 35
- `handrails` → 33
- `ramps` → 43

### BP-220
Observed phrase counts in the refined markdown:
- `socialized housing projects` → 27
- `economic and socialized housing projects` → 20
- `open spaces` → 12
- `community facilities` → 15
- `parks and playgrounds` → 16
- `circulation system` → 5
- `lot planning` → 3

## Interpretation
The current shared concept set is still PD-1096-centric. Non-PD laws are being extracted against concepts that are either too generic or semantically wrong.

A minimal next slice should therefore add only a very small number of law-appropriate placeholder concepts, then rerun dataset-safe extraction with a concept whitelist to avoid interference from unrelated PD-1096 concepts.

## Recommended first concept additions
### BP-344
- `accessible ramps`
- optionally later: `handrails`

Reason:
- very strong repetition in the source text
- high chance of yielding source→concept governs candidates
- simpler than adding multiple overlapping accessibility concepts at once

### BP-220
- `socialized housing projects`
- optionally later: `community facilities` or `open spaces`

Reason:
- strong repetition
- aligns directly with the document’s core subject matter
- likely to yield source→concept governs candidates if extracted in isolation

## Recommended execution rule
Do not add a large concept family at once.
Add one concept per law first, then rerun dataset-safe extraction/review before widening.
