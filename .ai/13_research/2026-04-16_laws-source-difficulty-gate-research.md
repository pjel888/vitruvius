# Research Pack — Laws Source Difficulty / Extraction Trust Gate

## Purpose
Add checks and balances for difficult source files so low-quality OCR/extraction does not silently degrade canonical summaries or graph truth.

## Current truth
The pipeline already has some parser/detection quality checks, but the bounded laws lane still lacks a clear per-source trust report that answers:
- is this refined file structurally usable?
- does it look OCR-noisy?
- should it be treated as cautionary for canonical summarization?

## Smallest safe first slice
Do not add a hard fail gate yet.
First add a **dataset-local source quality signal** to the bounded source→graph lane.

Suggested metrics:
- total non-empty lines
- image line count
- table line count
- heading count
- structural heading count
- useful text line count
- useful-text ratio
- obvious noise signals (ISBN, GOVPH, URL, TOC, OCR fragments)

## Why this helps
It creates evidence for:
- which source pages are hard to trust
- where OCR / alternate-source fallback is needed
- whether summary quality is a source problem or a code problem

## Future direction
Once benchmarked, these signals can become a real blocking gate for low-trust sources.
