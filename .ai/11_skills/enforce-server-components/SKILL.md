---
name: enforce-server-components
description: >
  Enforces Next.js 16 and React 19 patterns in Cerebro: Server Components by default,
  client at leaf nodes, and no useEffect for initial data fetching. Use when adding or
  refactoring pages, layouts, or data-dependent UI.
---

# Enforce Server Components

## When to Use

- Adding or refactoring a page or layout
- Introducing or moving data fetching
- Reviewing client/server boundaries

## Instructions

### 1. Default: Server Components

- Do not add `'use client'` unless the component needs client-only behavior.
- Fetch data in RSC with async/await; pass data as props to children.

### 2. When to add `'use client'`

Only when the component (or a child) needs:

- `useState`, `useEffect` (for non-fetch: timers, DOM sync, subscriptions)
- `useCallback`, `useMemo`
- Event handlers (onClick, onChange, etc.)
- Browser APIs (`window`, `localStorage`, `document`)
- React context consumption

Push `'use client'` to the **smallest subtree** (leaf wrapper) so the rest of the tree stays server-rendered.

### 3. Data fetching

- **Initial load**: Prefer RSC async or Server Actions; pass `initialData` (e.g. `initialQuestions`, `initialCursor`) from page to client component.
- **Client-driven fetch** (e.g. infinite scroll, refresh): Use Server Actions called from client; do not use `useEffect` for the *initial* load when the page can preload.
- Prefer `use()` for reading promises in client components where appropriate; use Suspense boundaries when needed.

### 4. Verification

- Grep for `useEffect` and confirm none are used **solely** for initial data fetch; refactor to RSC + client wrapper when they are.
- Keep `useEffect` for: timers, focus/DOM sync, localStorage, context side effects, or "load more" triggered by user/scroll (after initial data came from props).
