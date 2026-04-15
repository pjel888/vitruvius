# Rust Style and Implementation Rules

## Purpose
This document defines implementation preferences and style rules for Rust code in Vitruvius.

## Design Preferences
- prefer explicitness over cleverness
- prefer small focused modules over giant abstractions
- prefer pure functions where possible
- prefer simple data over ornate APIs
- prefer measurable optimization over speculative optimization
- prefer stable interfaces over fast-changing ones

---

## Naming
- use descriptive names
- avoid overly short geometry names except conventional math locals inside tight scope
- suffix numeric unit-bearing variables clearly where ambiguity is possible
- keep public API names boring and obvious

## Module Design
- one strong idea per module
- separate reference implementations from optimized implementations where useful
- separate tests cleanly
- isolate FFI-facing code from core kernel code

## Struct Design
- keep hot-path structs lean
- do not mix metadata with compute fields
- avoid dumping many unrelated fields into one struct
- document invariants near the struct definition

## Function Design
- keep functions single-purpose
- define preconditions clearly
- return structured results when error context matters
- minimize hidden side effects

## Memory Rules
- avoid allocation in hot loops
- avoid unnecessary `clone`
- pass by reference where appropriate
- use stack-friendly shapes when practical
- justify heap-heavy design

## Numeric Rules
- default to `f64` unless documented reason exists otherwise
- centralize epsilon and tolerance policy
- avoid copy-pasted threshold constants
- document whether boundary equality is inclusive or exclusive

## Error Rules
- no silent swallowing of meaningful failure
- no panic for expected user or data conditions
- error messages should help diagnosis, not just say “invalid input”

## Comment Rules
- comment invariants and non-obvious math
- do not comment the obvious
- explain why, not only what
- note references for known algorithms when useful

## Unsafe Rules
- avoid unless absolutely necessary
- isolate unsafe blocks
- document safety invariants directly above the block
- surround with tests and review

## Benchmark Rules
- benchmark before and after optimization
- keep benchmark inputs representative
- do not claim speed from intuition alone

## FFI Rules
- keep conversions shallow
- avoid exposing internal complexity
- keep FFI types stable and explicit

## Final Rule
Readable, testable, auditable Rust is preferred over clever Rust that only its author understands.
