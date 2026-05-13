# Research Pack - ChunkHound Embedding Hygiene

## Question

What causes ChunkHound's remaining embedding errors and timeout noise?

## Evidence

ChunkHound run output:

- OpenAI-compatible embedding error: input length exceeds context length.
- Follow-on ChunkHound async batch logging errors: `_Task.elapsed`.
- 95 timeout-skipped large files under `003_Canonical-Knowledge-Layer/shared/sources/`.

Database inspection:

```sql
select f.path, count(*) as missing_count, max(length(c.code)) as max_chars, sum(length(c.code)) as total_chars
from chunks c
join files f on f.id=c.file_id
left join embeddings_768 e on e.chunk_id=c.id
where e.chunk_id is null
group by f.path
order by max_chars desc, missing_count desc;
```

Result:

- `config/vitruvius.yaml`
- 100 missing `embeddings_768`
- max chunk length: 11,361 chars
- largest symbol: `features`

## Root Cause

After YAML parser support was added, ChunkHound began parsing `config/vitruvius.yaml` deeply enough to create a very large YAML block chunk. That chunk exceeds the context limit of the configured local embedding model. The canonical source timeout files are separate: they are large document payloads, not code, and are expensive/noisy for a code-intelligence index.

## Recommendation

1. Set `--config-file-size-threshold-kb 10` in `scripts/chunkhound_analyze.sh` so large structured config files are skipped by ChunkHound instead of producing oversized embedding chunks.
2. Explicitly exclude `config/vitruvius.yaml` so stale oversized chunks are cleaned up.
3. Exclude `003_Canonical-Knowledge-Layer/shared/sources/**` in `.chunkhound.json` because those files are source-document custody payloads, not codebase structure.
4. Exclude `003_Canonical-Knowledge-Layer/shared/relationships/**` because a dry-run showed large canonical relationship payloads, also not codebase structure.
