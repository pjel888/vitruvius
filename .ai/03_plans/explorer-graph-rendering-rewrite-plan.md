---
task: explorer-graph-rendering-rewrite
phase: "05"
status: complete
created: 2026-04-16
---

# Explorer Graph Rendering — Rewrite Plan

## Status: Current State is Broken

After iterative reactive patching, the graph at `/explore` renders nothing. The user is rightfully frustrated. We need to stop, plan, and rebuild properly.

---

## Root Cause Analysis

### 1. Sigma.js v3 + React = Inherently Fragile
- Sigma.js is a WebGL imperative library. React is declarative. The impedance mismatch causes constant subtle bugs.
- `@react-sigma/core` v4 has lifecycle issues (double-mount under StrictMode, stale closures on `useSigma()`).
- Raw Sigma without React wrappers works better but still has edge cases (attribute name collisions, event handler ordering).

### 2. Attribute Name Collisions
- Sigma reserves `type` for node program selection, `hidden` for visibility, `zIndex` for layering.
- Our knowledge graph nodes use `type` for "concept", "rule", etc. → crashes Sigma with "could not find program for node type X".
- We renamed to `nodeType`/`edgeType` but this is a band-aid that could break again.

### 3. No Error Boundaries
- One graphology exception (duplicate edge ID) crashes the entire React tree.
- No fallback UI. No graceful degradation.

### 4. Race Conditions
- `useEffect` in GraphScene polls for controller readiness with `setTimeout` loops.
- React 19 can run effects twice in development. Parallel `loadPerspective` calls cause duplicate node/edge errors.
- No single source of truth for "is graph initialized?"

### 5. Build vs Dev Server Confusion
- `bun run build` produces static files in `dist/`.
- API serves `dist/` at `localhost:3000`.
- Vite dev server runs at `localhost:5173` with HMR.
- Changes to source files should reflect immediately at `localhost:5173` via HMR, but HMR can fail silently after many rapid edits.

---

## Option A: Fix Raw Sigma (Incremental)

Keep the current raw Sigma approach but fix the structural issues.

**Pros**: Fastest path to working. We already have the code.
**Cons**: Still fighting React/Sigma impedance mismatch. Will keep having edge cases.

**Changes needed**:
1. **Add React Error Boundary** around `<SigmaHost>` so one graph crash doesn't kill the whole app.
2. **Serialize graph initialization** — use a `graphReady` promise instead of polling loops.
3. **Prefix ALL Sigma attributes** — use `__nodeType`, `__edgeType` instead of `nodeType`/`edgeType` to avoid any future collisions.
4. **Remove drag for now** — it's the most recent addition and likely the source of the current blank page (event handler conflicts).
5. **Test ONE thing at a time** — load graph → see nodes → add hover → add drag → add filters.

---

## Option B: Use @react-sigma/core Properly

Go back to `@react-sigma/core` but use it correctly:
- `SigmaContainer` + `useLoadGraph` + `useSetSettings` + `useRegisterEvents`
- All graph mutations happen inside `useEffect` with proper cleanup
- No imperative controller refs

**Pros**: The "official" React integration. Cleaner declarative code.
**Cons**: We already tried this and it had stale closure issues. The library may not be mature enough for Sigma v3 beta.

---

## Option C: Replace Sigma with D3-Force + SVG/Canvas

Use D3's force simulation with SVG or Canvas rendering. D3 is more predictable, has better React integration patterns, and doesn't use WebGL (so no shader program crashes).

**Pros**: Mature, well-documented, no attribute collisions, easy to debug.
**Cons**: Slower for >1000 nodes. No built-in labels. Would need more custom rendering code.

**For 200-500 nodes, D3-force + SVG is perfectly adequate.**

---

## Option D: Use the Working Legacy HTML Approach

The legacy `vitruvius-graph.html` renders correctly. It uses raw Sigma v2 (or v3?) without React. We could:
- Port that exact working code into a React component
- Wrap it minimally — just mount the Sigma instance and expose a few methods

**Pros**: Proven working code. Minimal changes.
**Cons**: Still imperative. Still has React integration issues, but smaller surface area.

---

## Recommendation

**Option A (Fix Raw Sigma) + Option D (reference legacy)** as the immediate fix.

**Then Option C (D3 migration)** as the medium-term architecture if we keep hitting Sigma issues.

### Immediate Fix Steps (Option A)

1. **Strip to bare minimum** — remove drag, remove hover reducers, remove filters. Just: load graph + render.
2. **Verify nodes appear**.
3. **Add back hover** (dim non-connected nodes, highlight edges).
4. **Add back filters** (node/edge type toggles).
5. **Add back drag** (if needed — but pan/zoom may be enough).
6. **Add color schemes and size scaling**.

### If Option A still fails after step 1

Switch to Option D — copy the exact working Sigma configuration from `vitruvius-graph.html` into a React wrapper with zero additional features.

---

## Testing Protocol

After EACH step:
1. `bun run build` must pass
2. Refresh browser at `http://localhost:5173/explore`
3. Check console for errors
4. Verify the specific feature works
5. Only then proceed to next step

**No skipping steps. No bundling multiple changes.**

---

## Files to Modify

| File | Action |
|------|--------|
| `explorer/src/components/graph/SigmaHost.tsx` | Rewrite with minimal approach |
| `explorer/src/components/GraphScene.tsx` | Remove debug overlay, simplify controller sync |
| `explorer/src/components/ErrorBoundary.tsx` | NEW — catch graph crashes |

## Files to Reference

| File | Why |
|------|-----|
| `vitruvius-graph.html` | Working Sigma config to copy |
