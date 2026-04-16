---
task: laws-source-difficulty-gate
phase: 05
created: 2026-04-16
author: CODER
status: ACCEPTED
---

# 2026-04-16 Laws Source Difficulty Gate Plan

## Goal
Give the bounded source→graph pipeline explicit visibility into source difficulty and extraction trust.

## First implementation slice
1. compute lightweight refined-markdown quality signals
2. attach them to `run-dataset-source-to-graph` stage reports
3. keep the slice non-blocking until thresholds are benchmarked

## Success criteria
- every bounded stage report includes source quality signals
- difficult sources become visible and auditable
- no graph truth is changed solely by this reporting slice
