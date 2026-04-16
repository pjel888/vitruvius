# Vitruvius MVP Data Acquisition and Source Strategy Brief
**Purpose:** Comprehensive strategic brief for Codex and future implementation agents on how Vitruvius should handle weak source documents, scanned-image PDFs, internet-sourced legal texts, AI-assisted correction, provenance, and MVP-stage engineering tradeoffs.

**Status:** Founder-level MVP strategy brief
**Audience:** Codex, implementation agents, auditors, future maintainers, and product decision-makers
**Primary Goal:** Make Vitruvius work reliably enough for an MVP by prioritizing trustworthy structure and usable legal/AEC knowledge over unnecessary engineering purity.

---

# 1. Executive Summary

Vitruvius is not being built as a research toy or a purity-driven parsing exercise. It is being built as an MVP by a founder who needs the system to work. That means the system should not be forced to depend only on poor-quality scanned PDFs when cleaner, more reliable, or more structured legal sources are available elsewhere.

Many source PDFs in the target dataset are not true digital text documents. They are effectively scanned photographs or scan-like reproductions. This makes OCR unreliable, inconsistent, and expensive in terms of engineering effort, especially when the goal is to produce a working MVP quickly. Because the product is now hyper-focused on architecture, building regulations, laws, standards, and related AEC knowledge, there is no reason to remain doctrinaire about source purity or insist that the entire system must reconstruct truth from the worst available source.

The correct MVP strategy is:

1. **Use the best available source for each law or document**
2. **Allow multiple sources to compound and reinforce one another**
3. **Use internet retrieval where it improves reliability**
4. **Use AI as a bounded corrective and reconciliation layer**
5. **Track provenance, confidence, and source hierarchy clearly**
6. **Keep the system practical, explainable, and founder-efficient**

This is not cheating. It is smart product engineering.

---

# 2. Foundational Position

## 2.1 The goal is not parser purity

At this stage, Vitruvius should not optimize for:

- being perfectly offline
- being fully OCR-dependent
- being purely deterministic from scanned PDFs
- being ideologically “clean” from a software-engineering purist perspective

Those are secondary concerns.

The real objective is:

```text
Can Vitruvius produce accurate, traceable, useful AEC/legal structure and knowledge quickly enough to validate the product?
```

That is the correct founder framing.

## 2.2 A founder building an MVP must optimize for working leverage

A founder’s job is not to worship elegance at the expense of traction.

If:
- scanned PDFs are weak
- OCR is unreliable
- internet sources contain better versions
- AI can reconcile structure
- the product can become more reliable faster by using multiple source types

then the system should absolutely be allowed to do that.

This is not a violation of sound architecture. It is a correct prioritization of product velocity and usable truth.

---

# 3. The Source Quality Problem

## 3.1 Why scanned PDFs are a real issue

Many legal and regulatory documents are distributed as:
- scanned images
- photocopies turned into PDF
- rasterized pages with poor contrast
- low-quality OCR exports
- non-uniform formatting
- misaligned or degraded text

This creates major issues for an extraction pipeline:
- text is missing or malformed
- headings are lost
- numbering is broken
- line segmentation becomes unreliable
- section boundaries blur
- OCR introduces spelling and formatting errors
- hierarchy reconstruction becomes brittle

If Vitruvius tries to treat these weak PDFs as the sole authority for structure extraction, the system will waste a huge amount of time fighting the wrong problem.

## 3.2 Why this matters more for laws and AEC documents

AEC/legal knowledge graphs depend heavily on:
- exact headings
- section numbering
- rule/chapter hierarchy
- definitions
- exceptions
- references to other provisions
- applicability scope
- semantic structure of requirements and prohibitions

Weak OCR directly damages those features.

So even if OCR recovers “some text,” it may still fail at what matters most: structure.

---

# 4. The Correct MVP Strategy: Source Hierarchy

Vitruvius should not treat all sources equally. It should rank them and prefer the highest-quality, most trustworthy version available.

## 4.1 Recommended source hierarchy

### Tier 1 — Authoritative machine-readable legal text
Best case. These are clean web pages, structured legal databases, official government text publications, or well-maintained text versions of laws and regulations.

Preferred because:
- better text quality
- better heading fidelity
- lower OCR burden
- easier parsing
- often closer to true legal structure

### Tier 2 — High-quality digital PDFs
These are PDFs with embedded text and reasonably clean formatting.

Useful because:
- close to official layout
- often retain numbering and headings
- easier to extract deterministically

### Tier 3 — Messy but partially extractable PDFs
These may have embedded text but poor formatting, layout issues, or partial OCR.

Useful as fallback or corroboration source.

### Tier 4 — Scanned-image PDFs requiring OCR
These should not be the default preferred source if better sources exist.

Use when:
- no cleaner source exists
- original official appearance matters
- source comparison is needed
- OCR can provide partial recovery

### Tier 5 — AI-assisted recovery and reconciliation
AI should sit above or beside source extraction, not replace it blindly.

Use AI to:
- compare multiple extracted versions
- classify ambiguous text blocks
- repair hierarchy proposals
- resolve conflicts between weak sources
- fill structural gaps cautiously

## 4.2 Core principle

The question should not be:
“Can we force this scanned PDF to work?”

The question should be:
“What is the best available representation of this law, and how do we combine sources responsibly?”

---

# 5. It Is Acceptable to Compound the Dataset with Internet Sources

## 5.1 Yes, this is acceptable

Vitruvius should be allowed to enrich or compound its dataset with trustworthy internet sources, especially when the base PDFs are weak.

This means:
- looking for better text versions online
- finding structured legal pages
- checking multiple sources for the same law
- comparing official and unofficial text copies
- choosing the most usable and trustworthy version for parsing
- using web sources to validate OCR or recover missing structure

This is strategically correct for an MVP.

## 5.2 Why this is not a problem

This is not “corrupting” the dataset.
This is not “polluting” the truth.
This is not “taking shortcuts” in a bad way.

It is simply recognizing that:
- some source artifacts are poor containers of legal text
- the product needs reliable structure
- internet-accessible legal text may be better than the scanned PDF
- the job of the system is to recover truth, not to romanticize bad inputs

## 5.3 The condition: provenance must be preserved

If Vitruvius compounds its source data using internet sources, it must preserve:

- source URL
- source type
- retrieval timestamp
- extraction method
- confidence score
- whether the source is official, quasi-official, or secondary
- whether structure came from raw source, OCR, or AI-assisted reconciliation
- whether multiple sources were compared
- whether conflicts were detected

That is the key discipline that keeps the MVP credible.

---

# 6. AI and Internet Use Are Correct for MVP

## 6.1 AI should be allowed to help repair weak source structure

If the system has:
- a poor scanned PDF
- a weak OCR output
- a cleaner web copy
- some ambiguity in section boundaries or heading types

then AI may absolutely be used to:
- compare sources
- classify blocks
- repair structure proposals
- decide likely parent-child relationships
- flag uncertainty
- reconcile layout damage

This is appropriate.

## 6.2 AI should not become unbounded truth generation

Even though AI is allowed, it should not be allowed to:
- invent law structure with no source grounding
- silently rewrite provisions
- fabricate missing references
- hide uncertainty
- produce final structure with no validation or provenance

The correct rule is:

```text
AI may reinforce and reconcile.
AI may not become an untraceable replacement for source-grounded structure.
```

## 6.3 This is founder-efficient engineering

For MVP, the winning move is not purity.
The winning move is:
- get reliable structure quickly
- stay transparent about source quality
- track provenance
- keep a path to later hardening

That is exactly the kind of leverage a founder should use.

---

# 7. The Pipeline Should Shift to Multi-Source Ingestion

The current thinking of:

```text
PDF → parse → graph
```

is too weak for the realities of the dataset.

The correct MVP pipeline is:

```text
law/document identifier
→ gather candidate sources
→ rank and score sources
→ extract text/structure from best source(s)
→ compare and reconcile versions
→ validate structure
→ produce canonical representation
→ graph
```

## 7.1 What this changes

Vitruvius should no longer treat a PDF file as the sole truth container.
Instead, it should treat the PDF as one candidate source among several possible representations of the same law.

## 7.2 Benefits

This improves:
- reliability
- structural fidelity
- robustness to degraded scans
- parser success rate
- graph richness
- founder velocity

---

# 8. Recommended Source Handling Model

## 8.1 Candidate source collection

For each law or document, the system should be able to collect possible source representations such as:
- official PDF
- digital text PDF
- structured web page
- legal database copy
- archived text page
- OCR output from scanned PDF
- manual ingestion copy if needed

## 8.2 Source ranking

Each source should be scored using factors such as:
- officialness / authority
- text cleanliness
- heading fidelity
- completeness
- machine readability
- consistency with other sources
- extraction confidence

## 8.3 Source comparison

If multiple sources exist, the system should compare:
- titles
- section numbering
- heading sequence
- number of detected sections
- reference patterns
- text completeness
- structural consistency

## 8.4 Reconciliation

Reconciliation may include:
- selecting the strongest source as primary
- using secondary sources to fill gaps
- using OCR only to confirm missing spans
- using AI to reconcile ambiguous differences
- flagging unresolved conflicts instead of hiding them

---

# 9. Provenance Must Become a First-Class System Feature

If Vitruvius uses compounded data, provenance is not optional. It is part of the product’s integrity.

## 9.1 Minimum provenance fields

For every canonical node or extracted structure segment, store:

- canonical document ID
- source document ID
- source URL or file path
- source tier
- source authority classification
- retrieval timestamp
- extraction method
- parser version
- whether OCR was used
- whether AI-assisted repair was used
- confidence score
- conflict flag if applicable

## 9.2 Why provenance matters

Provenance allows the system to:
- defend its outputs
- debug source conflicts
- explain why a structure exists
- reprocess when better sources appear
- avoid black-box behavior
- increase trust for users and founders alike

---

# 10. Deterministic + Internet + AI Is the Right Hybrid

## 10.1 Correct architecture

The right architecture is not:
- pure OCR
- pure Rust
- pure deterministic parser from bad scans
- pure AI extraction

The right architecture is:

```text
multi-source acquisition
+ deterministic parsing
+ internet-assisted source improvement
+ AI-assisted reconciliation
+ validation
+ provenance tracking
```

## 10.2 Deterministic code still matters

Even if internet and AI are used aggressively, deterministic code still needs to handle:
- source ranking
- text extraction pipelines
- section detection
- numbering analysis
- structural schema generation
- validation
- provenance storage
- graph assembly

The system should remain explainable and testable.

## 10.3 Why pure Rust is not the priority

At this stage:
- source quality and parser logic are more important than raw runtime speed
- Python has broader ecosystem support for document handling, web retrieval, OCR orchestration, text processing, and rapid iteration
- the main bottleneck is not performance, it is input chaos

Therefore:
- a pure Rust mindset is not useful for MVP
- a hybrid or Python-first approach is more sensible
- Rust can be introduced later only for proven bottlenecks

---

# 11. What Codex Should Understand

Codex should be explicitly instructed that Vitruvius is allowed and expected to:

- search for better sources online
- compare multiple representations of the same law
- prefer cleaner data over poor scans
- use OCR as fallback, not dogma
- use AI to resolve ambiguity and reinforce structure
- maintain provenance and confidence
- optimize for MVP reliability, not engineering purity

Codex should **not** behave as if:
- only local raw PDFs matter
- offline extraction purity is sacred
- using the internet is a design failure
- the MVP should avoid practical corrective measures

That would be the wrong mindset.

---

# 12. Correct Founder-Level Product Philosophy

## 12.1 Product reality over ideological engineering

The founder is not building a parsing dissertation.
The founder is building a product.

That means the correct priorities are:
1. make the product useful
2. make the outputs reliable enough to trust
3. move fast enough to validate the market
4. leave room for later hardening

## 12.2 MVPs are allowed to be strategically impure

As long as the system is:
- traceable
- defensible
- improvable
- source-aware
- bounded in AI usage

it is entirely acceptable for the MVP to use:
- internet retrieval
- multiple source forms
- AI-assisted reconciliation
- pragmatic source substitution

This is not a flaw. It is intelligent prioritization.

---

# 13. Recommended Changes to the Existing Strategic Brief

The existing Vitruvius architecture brief should be mentally updated with these additions:

## 13.1 Source acquisition layer should become explicit
Add a front-end layer to the pipeline for:
- candidate source discovery
- internet retrieval
- source ranking
- source comparison
- provenance capture

## 13.2 OCR should be demoted to fallback status
OCR should remain important, but not privileged if cleaner sources exist.

## 13.3 Benchmarking should include source quality scenarios
Evals should test:
- clean web sources
- text PDFs
- messy PDFs
- scanned-image PDFs
- multi-source reconciliation cases

## 13.4 Provenance should be part of schema
The intermediate representation should include source metadata and extraction lineage.

---

# 14. Proposed MVP Pipeline for Vitruvius

```text
law identifier / target document
→ source discovery
→ candidate source collection
→ source authority + quality scoring
→ select primary + secondary sources
→ extract text / structure
→ compare and reconcile
→ deterministic structural parsing
→ AI-assisted repair for ambiguities
→ validation
→ canonical representation with provenance
→ knowledge graph
→ UI / downstream outputs
```

---

# 15. What to Optimize for Right Now

## 15.1 Optimize for:
- reliable structure
- cleaner source acquisition
- quick founder leverage
- explainable provenance
- multi-source robustness
- pragmatic MVP usefulness

## 15.2 Do not optimize for:
- pure offline operation
- OCR purity
- premature Rust optimization
- theoretical parser elegance at the expense of product speed
- rigid source dogmatism

---

# 16. Risks and Guardrails

## 16.1 Main risks of this strategy
- hidden source conflicts
- AI overreach
- accidental drift from authoritative text
- source inconsistency across websites
- silent provenance loss
- overconfidence in secondary sources

## 16.2 Guardrails
- always track source metadata
- always prefer authoritative sources when available
- compare multiple sources when feasible
- flag conflicts instead of hiding them
- keep validation deterministic
- log when AI influenced structure
- separate primary source text from repaired or reconciled structure

---

# 17. Non-Negotiable Rules

1. Vitruvius is allowed to use internet sources to improve reliability.
2. Vitruvius is allowed to compound weak local data with stronger online data.
3. OCR is a fallback and corroboration tool, not a sacred first principle.
4. AI may be used for correction, comparison, reconciliation, and ambiguity handling.
5. AI must remain bounded, source-grounded, and traceable.
6. Provenance must be captured for every source and every repaired structure segment.
7. The MVP should optimize for useful, trustworthy outputs rather than engineering purity.
8. Python-first or hybrid implementation is acceptable and preferable for MVP velocity.
9. Pure Rust is not the current priority.
10. The system must remain explainable enough to harden later.

---

# 18. Direct Instructions for Codex

When Codex is given this brief, it should understand the following:

- scanned-image PDFs are a known weakness in the dataset
- source quality is a central product issue
- Vitruvius should support multi-source law ingestion
- cleaner web sources are allowed and encouraged for MVP
- internet-assisted correction is part of the strategy
- provenance and confidence tracking are mandatory
- AI is allowed as a bounded corrective layer
- OCR should not dominate the system design
- parser purity is not the objective
- founder leverage and MVP usefulness are the objective

Codex should then:
- audit current source ingestion assumptions
- design or improve a source acquisition layer
- propose source ranking and provenance tracking
- integrate internet-assisted candidate source selection
- keep deterministic parsing and validation strong
- avoid ideological resistance to practical data improvement

---

# 19. Final Position

The correct Vitruvius MVP philosophy is:

```text
Use the best available source.
Compound weak source data with stronger source data.
Use the internet when it materially improves reliability.
Use AI to reconcile and repair where appropriate.
Track provenance.
Stay practical.
Build the product.
```

This is the right founder decision.

It is not less serious.
It is more serious, because it focuses on what actually makes the product work.

---

# 20. End State for This Brief

This document should be used as a strategic context file for:
- source acquisition redesign
- Codex audit prompts
- MVP data pipeline planning
- provenance schema design
- web retrieval and reconciliation plans
- AI-assisted correction boundaries
- implementation roadmaps focused on real product leverage

It is not a final engineering specification.
It is a founder-level directive on how Vitruvius should handle source reality during MVP stage.
