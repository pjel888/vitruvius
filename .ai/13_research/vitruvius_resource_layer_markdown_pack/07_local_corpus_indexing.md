# 07 — Local Corpus Indexing Plan

## Why local corpus matters

Local files are often the most valuable references in Vitruvius because they can be stable, indexed deeply, page referenced, project-specific, available offline, connected to internal workflows, and used for evidence/procedure/document nodes.

A local source with a page reference and good rationale can be more useful than a generic online URL.

## Target file types

Start with PDF, EPUB, DOCX, HTML, TXT, and Markdown.

Optional later: images with OCR only when necessary, scanned PDFs, CAD/BIM documents if text metadata is extractable, and spreadsheets if they contain source/register data.

## Suggested folder discovery

Inspect repository for existing source folders. If none exist, recommend:

```text
/resources/local/
/resources/local/books/
/resources/local/pdfs/
/resources/local/standards/
/resources/local/manuals/
/resources/local/internal/
```

Do not move user files without permission or repo convention. Index them where they are.

## Local resource metadata extraction

For each file, extract path, file name, extension, size, hash, modified date, PDF metadata title/author where available, title from first pages if metadata missing, page count, table of contents if available, text extraction status, possible resource type, discipline/taxonomy hints, and access type.

## Hashing

Use SHA-256 or equivalent stable file hash. Hash supports duplicate detection, changed-file detection, stable local resource IDs, and verification.

## Chunking

Chunk local documents by table of contents sections, headings, page ranges, or fallback token/character chunks. For sidebar references, page-level chunks are often ideal.

Suggested chunk size: 500–1,200 tokens for semantic search. Keep short text previews only and avoid storing long copyrighted excerpts in output surfaces.

## Indexing fields

For each chunk:

- resource ID,
- page start/end,
- section title,
- heading path,
- keywords,
- short preview,
- embedding ID if embeddings exist,
- matched node candidates.

## Node matching for local chunks

Use hybrid matching:

```text
score =
  0.25 * canonical name exact/near match
+ 0.20 * alias match
+ 0.20 * taxonomy context match
+ 0.20 * semantic similarity
+ 0.10 * heading/title match
+ 0.05 * source authority/local corpus priority
```

Raise score when the node name appears in a heading, multiple aliases appear, parent topic terms appear, related nodes appear nearby, or source is already known/trusted. Lower score when the term appears only in bibliography/index, appears in unrelated context, the document is too broad, or extraction is poor.

## Local resource linking examples

### Node: Load Path

```text
relationship: explains
pageRefs: ["pp. 12-16"]
rationale: Explains how building loads are transferred through slabs, beams, columns, and foundations.
```

### Node: Site Grading

```text
relationship: provides_design_guidance
pageRefs: ["pp. 45-52"]
rationale: Discusses grading decisions that affect drainage, access, and building elevation.
```

### Node: Concrete Curing Procedure

```text
relationship: provides_procedure
pageRefs: ["Section 6.4"]
rationale: Provides construction-stage curing procedure and inspection considerations.
```

## Verification for local files

Required checks: file exists, hash computed, title not empty, text extraction attempted, page count available for PDFs where possible, resource card does not expose restricted content beyond allowed metadata/preview, and path stored in safe application format.

## UI access cautions

Do not expose server filesystem paths publicly in a web deployment unless explicitly designed and secured. Use a secure library viewer, sanitized file names, and permission checks.

## Minimum viable local index

```json
{
  "resourceId": "local_pdf_sha256_xxx",
  "title": "Foundation Design Guide",
  "resourceType": "local_pdf",
  "localPath": "resources/local/foundation-design-guide.pdf",
  "localFileHash": "...",
  "pageCount": 180,
  "verificationStatus": "local_file_verified",
  "keywords": ["foundation", "bearing capacity", "settlement"]
}
```
