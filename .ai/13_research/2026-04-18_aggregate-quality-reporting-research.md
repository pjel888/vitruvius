---
task: aggregate-quality-reporting
created: 2026-04-18
status: complete
---

# Research — Aggregate quality reporting

## Goal
Make the combined ready-family graph easier to harden by exposing a compact structured summary of its warnings and partial-coverage hotspots.

## Current state
- build reports already contain integrity findings and per-folder coverage
- source-to-graph reports already contain source-quality summaries
- there is no short operator surface that rolls those into one actionable warning summary

## Minimal useful step
Add a command that reads a dataset build report and emits:
- warning counts by code
- top orphan nodes
- top duplicate edges
- partial coverage folders
- counts of covered vs partial folders
