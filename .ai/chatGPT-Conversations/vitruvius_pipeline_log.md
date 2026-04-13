# Vitruvius Pipeline Development Log

## Overview
This document summarizes the step-by-step development of the Vitruvius knowledge pipeline, including ingestion, canonicalization, relationship extraction, and LLM-based validation.

---

## Phase 1: Data Ingestion
- Built pipeline for converting PDFs, Word, Excel into markdown
- Established folder structure:
  - 001_Raw-Source-Layer
  - 002_Raw-Conversion-Layer
  - 003_Canonical-Knowledge-Layer

---

## Phase 2: Canonicalization
- Implemented canonicalize-one and canonicalize-plan-one
- Introduced strict ID system:
  - law-*
  - concept-*
  - irr-*
- Created canonical_rules.yaml to avoid hardcoding

---

## Phase 3: Concept Layer
- Built canonicalize-concept-one
- Generated core PD 1096 concept set (~20 concepts)
- Enabled concept detection in extraction

---

## Phase 4: Relationship Extraction
### V1
- Line-based extraction
- Result: 0 relationships

### V2
- Window-based extraction
- Result: minimal relationships

### V3
- Added:
  - aggregation
  - deduplication
  - concept matching improvements
- Result: structured relationships

---

## Phase 5: Section-Aware Extraction
- Parsed 63 sections from PD 1096
- Extracted relationships per section
- Output included:
  - occurrences
  - section references
- Result: 23 unique relationships

---

## Phase 6: Problem Identified
- Extraction quality improved
- But noise present:
  - incorrect relationships
  - overly broad matches

---

## Phase 7: LLM Review Layer (Ollama)
- Integrated gemma4:31b via Ollama
- Built review-relationships-ollama command
- Model classifies relationships:
  - keep
  - review_further
  - reject
- Outputs:
  - confidence
  - reasoning
  - suggested type

---

## Architecture Summary

Raw Data
→ Conversion
→ Canonicalization
→ Concept Layer
→ Relationship Extraction
→ Section-Aware Structuring
→ LLM Review (Gemma 4)
→ Human Spot Check (minimal)

---

## Key Insights

1. Deterministic extraction must come first
2. Concepts drive relationship discovery
3. Section-aware parsing is critical for legal texts
4. LLM should validate, not generate truth
5. Manual review must be minimized and targeted

---

## Current Status

- Pipeline operational end-to-end
- Extraction producing meaningful graph structure
- LLM review layer implemented
- Ready for:
  - relationship promotion
  - graph construction
  - query layer

---

## Next Steps

- Build relationship promotion system
- Write approved relationships into canonical layer
- Introduce graph database (optional)
- Expand dataset beyond PD 1096
- Add AI-assisted concept enrichment

---

## Timestamp
Generated: 2026-04-13T09:17:56.916944