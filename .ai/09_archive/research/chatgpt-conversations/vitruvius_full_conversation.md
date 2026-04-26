# Full Vitruvius Development Conversation (Structured Transcript)

This document captures a detailed, step-by-step reconstruction of the development process of the Vitruvius pipeline, preserving intent, decisions, errors, and system evolution.

---

## 1. Initial Goal

Build a local-first AI-powered knowledge system for architecture:

- ingest PDFs, Word, Excel
- convert to markdown
- build canonical knowledge layer
- extract relationships
- eventually power a “second brain” / wiki system

---

## 2. Data Pipeline Established

Directory structure:

001_Raw-Source-Layer  
002_Raw-Conversion-Layer  
003_Canonical-Knowledge-Layer  
006_System-Manifests  

Pipeline capabilities:

- convert documents to markdown
- reconcile outputs
- track runs via manifests

---

## 3. Canonicalization Phase

Key commands built:

- canonicalize-plan-one
- canonicalize-one

Key decision:

Do NOT hardcode logic  
→ introduced canonical_rules.yaml

---

## 4. ID System Enforcement

Standard enforced:

- law-*
- irr-*
- concept-*

Migration system created:

- migrate-ids-plan
- migrate-ids-apply

Result:

All IDs normalized and consistent  
→ critical milestone

---

## 5. Concept Layer Creation

Command:

canonicalize-concept-one

Initial issue:

CLI mismatch (name vs concept_name)  
→ fixed by enforcing keyword-only arguments

---

## 6. Core Concept Expansion (PD 1096)

Created ~20 key concepts:

- occupancy classification
- occupancy load
- means of egress
- fire-resistive construction
- building permit
- certificate of occupancy
- light and ventilation
- setbacks
- etc.

Impact:

Extraction quality increased significantly

---

## 7. Relationship Extraction Evolution

### V1
- line-based
- result: 0 relationships

### V2
- window-based
- still weak

### V3
- aggregation
- deduplication
- improved concept matching

Result: usable structure

---

## 8. Section-Aware Extraction (Major Breakthrough)

Parsed 63 sections from PD 1096

Output:

- section-level relationships
- occurrences count
- traceable legal references

Result:

23 unique relationships extracted

---

## 9. Problem Identified

Even with improvements:

- noise present
- incorrect relationships
- overly aggressive pattern matching

Conclusion:

Extraction alone is not enough

---

## 10. Architectural Shift

New pipeline:

RAW → STRUCTURED → REVIEWED

Instead of:

RAW → FINAL TRUTH

---

## 11. LLM Integration (Ollama)

Model:

gemma4:31b

Role:

NOT generator  
→ reviewer

---

## 12. Review Layer Design

Command:

review-relationships-ollama

Input:

candidate relationships

Output:

- decision: keep / review_further / reject
- confidence
- reasoning
- optional suggested type

---

## 13. Key System Philosophy

1. Deterministic first
2. LLM validates, not invents
3. Human review only for edge cases
4. Concepts drive knowledge graph
5. Sections are fundamental for legal parsing

---

## 14. Current State

System now has:

- ingestion pipeline
- canonicalization engine
- concept layer
- relationship extraction (section-aware)
- LLM review layer

This is already a full knowledge pipeline.

---

## 15. Next Direction

- relationship promotion system
- canonical graph writing
- query engine
- expansion to more laws
- AI-assisted enrichment

---

## Timestamp
Generated: 2026-04-13T09:18:30.662375