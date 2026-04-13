# Canonical ID Standard (Vitruvius)

## ID Format

All canonical IDs must follow:

`<page_type>`{=html}-`<slug>`{=html}

## Page Type Prefixes

-   law
-   irr
-   concept
-   glossary
-   relationship
-   handout
-   reviewer
-   law-section
-   source

## Slug Rules

-   lowercase only
-   words separated by hyphens
-   no underscores
-   no special characters
-   no duplicate hyphens
-   no trailing hyphens

## Title vs ID

-   Title: human-readable
-   ID: machine-stable

Example: - Title: National Building Code of the Philippines - ID:
law-national-building-code-of-the-philippines

## Legal Metadata (Future)

-   common_reference
-   formal_citation

## Relationship Rules

All references must use canonical IDs.

Example: - implements: law-national-building-code-of-the-philippines

## Migration Rules

-   no duplicate IDs
-   no legacy prefixes (laws-, etc.)
-   all relationships updated to new IDs
-   verify referential integrity after migration

## Notes

This document defines the canonical identity system for all entities in
Vitruvius.
