# Canonicalization Automation Workflow

## Purpose

Define a safe, controlled system to convert raw extracted content into
structured canonical knowledge.

Automation produces **drafts only**. Human review determines truth.

------------------------------------------------------------------------

## Core Principle

Raw Conversion Layer = Evidence\
Canonical Layer = Trusted Knowledge

Automation must never bypass validation, structure, or traceability.

------------------------------------------------------------------------

## Commands

### canonicalize-plan-one

Generates a plan only. No files are written.

### canonicalize-one

Generates draft canonical files based on an approved plan.

### canonicalize-batch

Processes multiple inputs. Only used after validation of single-file
workflow.

------------------------------------------------------------------------

## Workflow Stages

### Stage 1: Input Selection

Input is a raw markdown file from: 002_Raw-Conversion-Layer

------------------------------------------------------------------------

### Stage 2: Source Classification

Classify into: - law - irr - official manual - textbook - reviewer -
handout - spreadsheet support - unknown

Determines trust level and behavior.

------------------------------------------------------------------------

### Stage 3: Metadata Normalization

Extract and normalize: - title - aliases - category - trust level -
relationships - lineage

------------------------------------------------------------------------

### Stage 4: Structural Parsing

Detect: - headings - sections - rules - lists - definitions - OCR noise

Clean without altering meaning.

------------------------------------------------------------------------

### Stage 5: Canonical Target Planning

Decide: - create source page (yes/no) - create concept pages (yes/no) -
create glossary entries (yes/no) - create relationship pages (yes/no)

------------------------------------------------------------------------

### Stage 6: Draft Generation

Create: - YAML frontmatter - structured page content - canonical format

Status must be: draft

------------------------------------------------------------------------

### Stage 7: Reporting

Write reports to: 006_System-Manifests/runs/

Examples: - latest_canonicalize_plan_one.json -
latest_canonicalize_one.json

------------------------------------------------------------------------

## Rules

1.  Never overwrite approved pages
2.  Never merge distinct authorities automatically
3.  Higher trust overrides lower trust
4.  Do not guess on ambiguity
5.  Every statement must trace to a source
6.  Prefer under-generation over over-generation

------------------------------------------------------------------------

## Trust Hierarchy

1.  Primary (laws, official codes)
2.  Secondary (manuals, institutional)
3.  Educational (textbooks)
4.  Study aids (handouts)
5.  Derived content

------------------------------------------------------------------------

## Outputs

### canonicalize-plan-one

Returns: - classification - trust level - proposed outputs - warnings

### canonicalize-one

Creates: - source page draft - optional concept drafts - report file

------------------------------------------------------------------------

## File Locations

Outputs must go to:

-   shared/sources/
-   shared/concepts/
-   shared/glossary/
-   shared/relationships/

------------------------------------------------------------------------

## Safety Model

-   All outputs = draft
-   Human review required
-   No auto-approval
-   No silent overwrites

------------------------------------------------------------------------

## Version 1 Scope

v1 should only: - process one file - generate one source page - produce
a plan report

------------------------------------------------------------------------

## Non-Negotiable Rule

If content cannot be traced back to a source, it does not belong in the
Canonical Layer.
