# Vitruvius Spatial Daemon

> **Purpose:** Consume raw CAD exports (SketchUp JSON, glTF, OBJ) and emit
> JSON manifests into `../001B_Spatial-Source-Layer/` that conform to the
> Vitruvius Spatial Contract v1.0.0
> (see `../.ai/06_specs/spatial-schema.md`).
>
> **Isolation:** This daemon is a sibling subproject. It has its own
> `package.json`, its own dependencies, and does not share a process
> with the Python pipeline. The Python pipeline only reads files the
> daemon writes — there is no RPC, no shared memory, no coupled runtime.

## Install

```bash
cd spatial-daemon
npm install
```

## Build

```bash
npm run build
```

## Test

```bash
npm test
```

## Run

```bash
npx vitruvius-spatial \
    --input path/to/sketchup_export.json \
    --output ../001B_Spatial-Source-Layer/
```

## Architecture

1. `src/types.ts` — type definitions mirroring the Python contract.
2. `src/aabb.ts` — axis-aligned bounding box computation.
3. `src/gjk.ts` — GJK intersection for convex hulls.
4. `src/contract_writer.ts` — emits JSON conforming to schema v1.0.0.
5. `src/cli.ts` — command-line entry point.

Every module is pure: no `fs`-side effects outside the contract writer.
