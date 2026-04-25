# api

To install dependencies:

```bash
bun install
```

To run:

```bash
bun run index.ts
```

To test:

```bash
bun test
```

The API fronts Neo4j for explorer workflows and now persists saved scenes in `api/.data/scenes.json`.

## Shadow Backbone Route

`GET /v2/backbone` is an additive, read-only shadow route. It reads the
file-backed AEC-MEPFS Backbone consumer report and returns a compact summary
only. It does not read or write Neo4j, does not expose registry rows or protected
source content, and is not used by Explorer by default.

This project was created using `bun init` in bun v1.3.12. [Bun](https://bun.com) is a fast all-in-one JavaScript runtime.
