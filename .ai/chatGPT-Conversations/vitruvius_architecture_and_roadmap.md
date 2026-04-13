# Vitruvius System Architecture & Roadmap

## Overview
This document defines the full architecture, current progress, and roadmap of the Vitruvius knowledge system.

---

# PART 1: SYSTEM ARCHITECTURE

## 1. Core Philosophy
- Deterministic pipeline first
- AI as validator, not source of truth
- Structured knowledge over raw text
- Legal-document-aware parsing (section-based)

---

## 2. Data Flow

RAW DATA  
→ Conversion Layer  
→ Canonicalization Layer  
→ Concept Layer  
→ Relationship Extraction  
→ Section Structuring  
→ LLM Review Layer  
→ (Future) Canonical Graph  

---

## 3. Folder Architecture

```
001_Raw-Source-Layer/
002_Raw-Conversion-Layer/
003_Canonical-Knowledge-Layer/
    shared/
        concepts/
        sources/
006_System-Manifests/
    runs/
    migrations/
```

---

## 4. Core Modules

### Ingestion
- convert
- convert-one
- convert-spreadsheet-one

### Canonicalization
- canonicalize-plan-one
- canonicalize-one

### Concepts
- canonicalize-concept-one

### Relationships
- extract-relationships-one
- extract-relationships-sections-one

### LLM Review
- review-relationships-ollama (Gemma 4)

---

## 5. Data Structures

### Concept
```
id: concept-*
title: *
page_type: concept
```

### Source
```
id: law-* / irr-*
title: *
relationships: []
```

### Relationship (current)
```
from
type
to
occurrences
sections
examples
```

---

# PART 2: CURRENT PROGRESS

## Completed

✔ Data ingestion pipeline  
✔ Canonicalization system  
✔ ID normalization  
✔ Concept generation system  
✔ Relationship extraction (V3)  
✔ Section-aware extraction  
✔ LLM review layer (Gemma 4)  

## Current Capability

- Extract structured relationships from legal documents
- Trace relationships to specific sections
- Automatically review relationship quality using local AI

---

# PART 3: CURRENT LIMITATIONS

## 1. Relationship Noise
- Over-detection of weak relationships
- Pattern-based extraction still crude

## 2. Concept Coverage
- Only partial concept set defined
- Missing many domain-specific concepts

## 3. No Promotion Layer
- Relationships are not yet written into canonical knowledge

## 4. No Query Layer
- Cannot yet "ask questions" to the system

---

# PART 4: ROADMAP

## Phase 1 — Foundation (DONE)
- ingestion
- canonicalization
- ID system
- concept layer

STATUS: COMPLETE

---

## Phase 2 — Extraction (DONE)
- relationship extraction V1 → V3
- section-aware parsing

STATUS: COMPLETE

---

## Phase 3 — Validation (CURRENT)
- LLM review via Ollama (Gemma 4)
- classification: keep / review / reject

STATUS: IN PROGRESS

---

## Phase 4 — Promotion Layer (NEXT)

Goal:
Write approved relationships into canonical layer

Tasks:
- build promotion system
- only accept high-confidence "keep"
- version relationships

---

## Phase 5 — Knowledge Graph

Goal:
Turn system into a queryable graph

Tasks:
- connect concepts ↔ concepts
- connect sources ↔ concepts
- optional graph DB (Neo4j or similar)

---

## Phase 6 — Query Engine

Goal:
Enable:

- "What governs occupancy classification?"
- "Which sections affect building permits?"

Tasks:
- graph traversal
- API layer

---

## Phase 7 — AI Augmentation

Goal:
- AI-assisted concept expansion
- semantic relationship detection
- intelligent summarization

---

# PART 5: DISTANCE TO GO

## You are here:

[██████████░░░░░░░░░░] ~45%

## Remaining work:

- relationship promotion layer
- graph construction
- query interface
- large-scale dataset expansion

---

# PART 6: STRATEGIC INSIGHT

You are no longer building a script.

You are building:

→ a structured legal knowledge engine  
→ a domain-specific reasoning system  

This is closer to:

- a legal AI backend
- a knowledge graph engine
- a computational architecture assistant

---

# TIMESTAMP
Generated: 2026-04-13T09:20:50.617290
