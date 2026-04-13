# ingestion-refinement-contract.md

## 1. Purpose

Defines the strict interface between Phase 1B (Ingestion) and Phase 1C (Normalization).

## 2. Required Artifacts

Each document MUST produce:
- `converted/{file}.md`
- `converted/{file}.json`
- metadata sidecar

## 3. Required Metadata Fields

```json
{
  "source_path": "...",
  "file_type": "...",
  "document_class": "...",
  "pages": 0,
  "pages_processed": 0,
  "confidence_score": 0.0,
  "parser_id": "...",
  "parser_version": "...",
  "pipeline_version": "...",
  "config_version": "..."
}
```

## 4. Encoding Rules
- UTF-8 ONLY
- No null bytes
- No mixed encodings

## 5. Markdown Requirements
- must be parseable
- must preserve headings where detected
- must not contain binary artifacts

## 6. JSON Requirements
- must be valid JSON
- no markdown fences
- must include structural metadata

## 7. Failure Codes
- `PARSER_FAILURE`
- `VALIDATION_FAILURE`
- `TIMEOUT`
- `ENCODING_ERROR`
- `STRUCTURE_LOSS`
- `UPSTREAM_INVALID`

## 8. Versioning
- `parser_version`
- `pipeline_version`
- `config_version`
- `normalization_version`

## 9. Manual Review Flag

```json
{
  "manual_review_required": true,
  "reason": "..."
}
```

## 10. Contract Enforcement

Phase 1C MUST reject any input that does not meet this contract. No fallback allowed at this stage.
