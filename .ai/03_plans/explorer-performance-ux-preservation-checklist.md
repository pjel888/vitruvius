# Explorer Performance UX Preservation Checklist

Scope: Explorer performance optimization for the file-backed AEC-MEPFS graph source `20260430T094129Z`.

Must remain visually and behaviorally preserved:

- Routes: current Explorer route flow and graph perspective selection remain unchanged.
- Layout: Explorer rail, graph canvas, bottom/preview affordances, and upper toolbar remain in their current positions.
- Styling: Tailwind-based visual language, dark graph canvas, node colors, selected-neighbor emphasis, source-clearance display, and panel typography remain unchanged.
- Search: command/search input, debounce behavior, default learner-facing results, alias resolution, and server fallback behavior remain unchanged.
- Selection: node click selects the clicked node; selected parent highlighting remains selected node plus visible direct-edge neighborhood unless a separate state is explicitly surfaced.
- Pan mode and select mode: toolbar behavior and keyboard shortcuts remain unchanged.
- Preview: node preview and source-clearance fields remain human-readable; no raw source-rights enums or protected-source labels are promoted to concepts.
- Filtering: learner-facing default graph excludes source/provenance/internal-only records.
- Bad-label safety: `Local raw-source filename metadata for TOA tropical architecture PDF` and related source/provenance process labels must not appear in learner-facing graph output.
- Renderer: `react-vis-network-graph` / `vis-network` remains the active renderer; no renderer migration is part of this phase.
- State/data flow: Zustand scene state and TanStack Query data fetching remain in use.
- Graph source: UI/API runtime remains pinned to the current clean file-backed shadow staging artifact or a newer validated clean successor.
- Loading/error/empty states: current user-facing states are preserved.

Permitted performance changes in this phase:

- Build faster indexes under the existing graph-engine contract.
- Cache visible subgraph generation and repeated searches by graph fingerprint/query.
- Keep expensive query work in the existing worker/fallback graph-engine layer.
- Add diagnostics/benchmarks/tests that do not alter the product UI.

Changes intentionally not made:

- No visual redesign.
- No UX redesign.
- No renderer replacement.
- No Rust/WASM graph engine unless benchmarks prove a TypeScript-worker compute bottleneck.
- No graph content changes.
