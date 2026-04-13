# Vitruvius Canonicalization Rules

## Purpose

The Canonical Knowledge Layer represents **trusted, normalized
knowledge** derived from raw source materials.

It is not a dump of extracted markdown.\
It is a curated, structured, and governed knowledge system.

------------------------------------------------------------------------

## Core Principle

Raw Conversion Layer = Evidence\
Canonical Layer = Trusted Knowledge

No content enters the Canonical Layer without passing through
normalization, validation, and structuring rules.

------------------------------------------------------------------------

## Canonical Page Types

### 1. Source Page

Represents a source document as an authority.

Purpose: - identify the source - define its scope and authority - link
to derived concepts

Location: shared/sources/

------------------------------------------------------------------------

### 2. Concept Page

Represents a topic, rule, or idea.

Purpose: - structured explanation - normalized terminology -
cross-references

Location: shared/concepts/

------------------------------------------------------------------------

### 3. Glossary Page

Represents a term definition.

Purpose: - concise definition - alias tracking - classification

Location: shared/glossary/

------------------------------------------------------------------------

### 4. Relationship Page

Represents structured relationships between entities.

Purpose: - governance mapping - dependencies - cross-references

Location: shared/relationships/

------------------------------------------------------------------------

### 5. Category Topic Page

Represents curated knowledge within a category.

Location example: 001-Laws/

------------------------------------------------------------------------

## Frontmatter Standard

All canonical pages must include YAML frontmatter.

### Required Fields

id: title: page_type: category: topic_tags: aliases: source_documents:
source_artifacts: trust_level: canonical_status: last_canonicalized_utc:
relationships:

------------------------------------------------------------------------

## Canonical Status Values

-   draft
-   reviewed
-   approved
-   deprecated
-   superseded

------------------------------------------------------------------------

## Trust Hierarchy

### Level 1: Primary Authority

-   laws
-   official codes
-   government issuances

### Level 2: Official Secondary Authority

-   official manuals
-   institutional references

### Level 3: Strong Educational References

-   textbooks
-   formal reviewers

### Level 4: Study Aids

-   lecture notes
-   handouts

### Level 5: Derived Content

-   generated explanations
-   internal summaries

Higher trust overrides lower trust.

------------------------------------------------------------------------

## Canonicalization Rules

### Rule 1

Do not alter meaning of source content.

### Rule 2

Remove extraction noise only: - headers - footers - OCR artifacts -
duplicated content

### Rule 3

Prefer higher-trust sources when conflicts exist.

### Rule 4

Keep source pages and concept pages separate.

### Rule 5

Every statement must be traceable to a source.

### Rule 6

Preserve conflicts when unresolved.

### Rule 7

Structure takes priority over writing style.

------------------------------------------------------------------------

## Canonical Page Structure

### Source Page

# Title

## Overview

## Source Identity

## Coverage

## Key Canonical Points

## Related Concepts

## Source Lineage

## Notes

------------------------------------------------------------------------

### Concept Page

# Title

## Definition

## Why It Matters

## Canonical Explanation

## Rules / Conditions / Exceptions

## Related Sources

## Related Concepts

## Notes

------------------------------------------------------------------------

## Spreadsheet Handling

Spreadsheets are not directly converted into canonical prose.

They contribute through: - structured data - mappings -
cross-references - glossary seeding - relationship extraction

------------------------------------------------------------------------

## Canonicalization Pipeline Stages

1.  Source Classification\
2.  Cleaning\
3.  Structural Parsing\
4.  Canonical Target Planning\
5.  Page Generation\
6.  Review and Approval

------------------------------------------------------------------------

## Non-Negotiable Rule

If content cannot be traced back to a source, it does not belong in the
Canonical Layer.
