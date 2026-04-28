# Explorer UI/UX Optimization Plan Critique

```yaml
status: CRITIQUE_READY
created: 2026-04-28
branch: main
plan_under_review: .ai/03_plans/AEC-MEPFS-Backbone/2026-04-28_explorer_ui_ux_optimization_readiness_and_implementation_plan.md
```

## 1. Verdict

The plan is directionally correct and should proceed as the next Explorer UX
slice. The immediate zoom/spread/physics changes are low-risk and directly match
observed user pain. The larger density strategy is necessary before document and
evidence relationships are default-visible.

## 2. Risks to control

### Risk 1 — More spread can reduce context

More spacing will make the graph less cramped, but too much spread can make users
lose the whole-system picture. The implementation should pair larger spread with
fit, minimap, zoom slider, and density presets rather than only raising the max.

### Risk 2 — A zoom slider must stay synchronized

If mouse-wheel zoom, zoom buttons, fit, minimap center, and the slider disagree,
the control will feel broken. Slider implementation must subscribe to actual
network zoom events or viewport snapshots.

### Risk 3 — Auto-pausing physics could surprise users

Auto-pause is desirable for spread changes, but the UI needs visible state and a
clear Resume action. Do not silently pause without making the state obvious.

### Risk 4 — Semantic zoom can hide information if poorly messaged

Automatic label/detail hiding must not make users think nodes disappeared. Keep
manual label toggles and show the current label/detail level.

### Risk 5 — Future document edges require separate acceptance criteria

The plan should not claim that document interrelationships are solved by spacing.
They need edge type filters, focus modes, and performance evidence.

### Risk 6 — Minimap must be treated as a control surface

The minimap is not just decoration; for a dense graph it is a primary recovery
and orientation control. The first implementation slice should harden minimap
snapshot/viewport synchronization, not only add tests later.

## 3. Required acceptance gates for the first implementation slice

- `git diff --check` passes.
- Focused Explorer component/graph tests pass.
- Full Explorer test suite passes.
- Explorer lint passes.
- Explorer build passes.
- Minimap updates are verified after filters/layout/zoom where practical.
- No API, Neo4j, KG, taxonomy fixture, protected content, or resolver behavior is
  touched.
- Manual/browser smoke should be run if the in-app browser or local dev server is
  available.

## 4. Recommendation

Proceed with Phase 1 as the next code slice:

1. zoom slider/readout;
2. expanded spread range/default;
3. auto-pause physics on user spread changes;
4. store/controller spread clamping;
5. focused tests and performance evidence.
