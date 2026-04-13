---
name: componentize-ui
description: Extracts repeated or large UI blocks into focused, reusable components and consolidates TypeScript interfaces. Use when a page/layout exceeds ~200 lines or the same JSX pattern appears in multiple places in Cerebro.
---

# Componentize UI

## When to Use

- A page or layout exceeds ~200 lines
- The same JSX pattern appears in multiple files
- A section has a clear single responsibility (e.g. summary stats, question row, nav item)

## Instructions

### 1. Placement

- **Feature-specific**: `src/components/{feature}/` (e.g. quiz, dashboard, analytics).
- **Shared / design system**: `src/components/ui/` or `src/components/shared/`.

### 2. Types

- Define props interfaces in the component file, or in `src/types/` (e.g. `src/types/dashboard.ts`, `src/types/app.ts`, or `src/types/quiz-config.ts`) when shared across features.
- No `any`; use existing types from `src/types/` and Supabase where applicable.

### 3. Design

- Prefer composition (children, slots) over large prop lists.
- Naming: PascalCase, descriptive of responsibility (e.g. `SessionSummaryStats`, `QuestionResultRow`, `SidebarNavItem`).

### 4. Extraction steps

1. Identify the block to extract (single responsibility).
2. Choose the target directory (feature vs shared).
3. Define the component and its props (and shared types if needed).
4. Replace the inline JSX with the new component; pass props or children.
5. Ensure no behavior change (same data, same events).
