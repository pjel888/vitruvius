> ⚠️ **HISTORICAL SNAPSHOT — SUPERSEDED 2026-04-15**
>
> This audit was written on 2026-04-13 against a pre-Sprint-A baseline. It is retained here as a frozen historical record of what the codebase looked like before Sprints A + B + C + D + Q + R + PHYS + H + GEOM + WIKI + GT + HP + Z + HP.3-R shipped. Almost every "weakness" or "missing feature" flagged below has since been addressed.
>
> **For the current state of the codebase, read these instead:**
> - `/.ai/10_state/active_context.md` — current session state
> - `/.ai/10_state/decisions.md` — architecture decisions AD-001 through AD-029
> - `/.ai/01_roadmap/current-phase.md` — current sprint / phase
> - `/.ai/00_system/architecture.md` — current package layout (including post-Sprint-D additions)
> - `/.ai/00_system/pipeline-overview.md` — current execution flow

---

# Review Layer Audit — Vitruvius

**Audit Date:** 2026-04-13
**Target:** Review and Validation Layer (Ollama-based relationship review)
**Codebase Scope:** Full repository — all Python files
**Status:** COMPLETE

---

## Section 1: Repository Map

### Python Files (25 total)

| File | Purpose | Review Relevance |
|------|---------|-----------------|
| `pipeline_cli.py` | CLI entrypoint | **HIGH** — review command registered here |
| `vitruvius/ollama_review.py` | Main review module | **PRIMARY** — 345 lines |
| `vitruvius/relationships_sections.py` | Relationship extraction | HIGH — provides candidates |
| `vitruvius/relationships.py` | Relationship extraction (regex) | MEDIUM |
| `vitruvius/reports.py` | JSON/TXT report writing | HIGH — output storage |
| `vitruvius/paths.py` | Path resolution | MEDIUM |
| `vitruvius/utils.py` | Timestamps, utilities | LOW |
| Other modules | Various pipeline stages | LOW |

---

## Section 2: Entrypoints and Review Triggers

### CLI Entrypoint

**File:** `scripts/pipeline_cli.py`

**Registration (lines 77-79):**
```python
review_parser = subparsers.add_parser("review-relationships-ollama")
review_parser.add_argument("--model", default="gemma4:31b")
review_parser.add_argument("--timeout-seconds", type=int, default=600)
```

**Execution (lines 163-167):**
```python
if args.command == "review-relationships-ollama":
    return run_review_relationships_ollama(
        model=args.model,
        timeout_seconds=args.timeout_seconds,
    )
```

### Key Finding: MANUAL TRIGGER ONLY

The review layer is **NOT** automatically invoked in the pipeline. It requires explicit command:

```bash
python scripts/pipeline_cli.py review-relationships-ollama
python scripts/pipeline_cli.py review-relationships-ollama --model llama3.2 --timeout-seconds 300
```

**Pipeline flow does NOT include review stage.** Users must manually run the review command after relationship extraction.

---

## Section 3: Import Graph

### Module Dependencies

**`ollama_review.py` imports:**
```python
from .paths import get_repo_root          # Path resolution
from .reports import write_json, write_text # Output storage
from .utils import utc_now_stamp         # Timestamps
```

**`pipeline_cli.py` imports:**
```python
from vitruvius.ollama_review import run_review_relationships_ollama
```

### Dependency Chain

```
pipeline_cli.py
    └── ollama_review.py
            ├── paths.py (get_repo_root)
            ├── reports.py (write_json, write_text)
            └── utils.py (utc_now_stamp)
```

### No External LLM Libraries

**Key Finding:** Uses only standard library `urllib` for Ollama HTTP API calls. No `ollama-python` or similar library.

---

## Section 4: Review Execution Trace

### Step-by-Step Flow

1. **CLI invocation:** `review-relationships-ollama` command
2. **Load candidates:** `load_relationship_report()` reads from `006_System-Manifests/runs/latest_relationship_extraction_sections.json`
3. **For each candidate:**
   - `build_prompt()` — constructs JSON prompt with candidate data
   - `call_ollama()` — sends HTTP request to Ollama
   - `parse_model_json()` — parses and validates response
   - `review_relationship()` — wraps the flow, handles errors
4. **Save progress:** `save_progress_report()` writes JSON and TXT reports
5. **Summary:** `summarize_reviews()` aggregates decision counts

### Function Call Chain

```
run_review_relationships_ollama()
    ├── load_relationship_report()
    │   └── json.loads(path.read_text())
    ├── for each candidate:
    │   ├── review_relationship()
    │   │   ├── build_prompt()
    │   │   ├── call_ollama()
    │   │   │   └── urllib.request.urlopen()
    │   │   └── parse_model_json()
    │   └── save_progress_report()
    │       ├── summarize_reviews()
    │       └── write_json() / write_text()
```

### Candidate Input Format

**Source file:** `006_System-Manifests/runs/latest_relationship_extraction_sections.json`

**Expected structure:**
```json
{
  "source": "path/to/source.md",
  "relationships": [
    {
      "from": "concept-A",
      "type": "relates_to",
      "to": "concept-B",
      "occurrences": 5,
      "sections": ["Section 1.1", "Section 2.3"],
      "examples": ["example text 1", "example text 2"]
    }
  ]
}
```

---

## Section 5: LLM Integration Details

### Ollama Configuration

**Endpoint:** `http://127.0.0.1:11434/api/generate`

**Default model:** `gemma4:31b` (configurable via `--model`)

**Default timeout:** 600 seconds (configurable via `--timeout-seconds`)

### HTTP Request Construction

**File:** `ollama_review.py`, lines 65-98

```python
def call_ollama(prompt: str, model: str, timeout_seconds: int) -> str:
    body = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "options": {
            "temperature": 0,
            "num_predict": 300,
        },
    }
    data = json.dumps(body).encode("utf-8")
    request = urllib.request.Request(
        OLLAMA_URL,  # "http://127.0.0.1:11434/api/generate"
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
```

### Prompt Construction

**File:** `ollama_review.py`, lines 33-62

```python
def build_prompt(candidate: dict[str, Any]) -> str:
    payload = {
        "task": "Review candidate legal relationship",
        "allowed_decisions": ["keep", "review_further", "reject"],
        "candidate": {
            "from": candidate["from"],
            "type": candidate["type"],
            "to": candidate["to"],
            "occurrences": candidate.get("occurrences", 0),
            "sections": candidate.get("sections", []),
            "examples": candidate.get("examples", []),
        },
        "instructions": [...],
        "output_schema": {
            "decision": "keep|review_further|reject",
            "confidence": "number from 0.0 to 1.0",
            "reason": "short explanation",
            "suggested_type": "string or null"
        }
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)
```

### Error Handling

**File:** `ollama_review.py`, lines 85-92

```python
try:
    with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
        raw = response.read().decode("utf-8")
except urllib.error.URLError as exc:
    raise RuntimeError(
        "Failed to reach Ollama at http://127.0.0.1:11434. "
        "Make sure Ollama is running and the model is available."
    ) from exc
```

### Key Findings: LLM Integration

| Aspect | Finding |
|--------|---------|
| **Library** | Standard library `urllib` only — no external dependencies |
| **API** | `/api/generate` endpoint (non-chat) |
| **Model** | Configurable via CLI arg |
| **Temperature** | Hardcoded to 0 (deterministic) |
| **Max tokens** | Hardcoded to 300 |
| **Format** | JSON request, JSON response expected |
| **Error handling** | Raises RuntimeError on connection failure |
| **Other LLM support** | NOT IMPLEMENTED — Ollama only |

---

## Section 6: Review Decision Structure

### Decision Types

**Allowed decisions:** `keep`, `review_further`, `reject`

**File:** `ollama_review.py`, lines 36, 116

```python
"allowed_decisions": ["keep", "review_further", "reject"],

if decision not in {"keep", "review_further", "reject"}:
    raise ValueError(f"Invalid decision from model: {decision}")
```

### Output Schema

```json
{
  "decision": "keep|review_further|reject",
  "confidence": 0.85,
  "reason": "The evidence clearly shows...",
  "suggested_type": "depends_on"  // optional
}
```

### Confidence Scoring

**Range:** 0.0 to 1.0 (clamped)

**File:** `ollama_review.py`, lines 119-124

```python
try:
    confidence = float(confidence)
except (TypeError, ValueError) as exc:
    raise ValueError(f"Invalid confidence from model: {confidence}") from exc

confidence = max(0.0, min(1.0, confidence))
```

### High Confidence Thresholds

**File:** `ollama_review.py`, lines 176-180

```python
if decision == "keep" and confidence >= 0.85:
    summary["high_confidence_keep"] += 1

if decision == "reject" and confidence >= 0.85:
    summary["high_confidence_reject"] += 1
```

---

## Section 7: Output and Storage

### Output Files

**Location:** `006_System-Manifests/runs/`

| File | Format | Contents |
|------|-------|----------|
| `latest_relationship_review_ollama.json` | JSON | Full report with all reviews |
| `latest_relationship_review_ollama.txt` | TXT | Human-readable report |

### JSON Report Structure

**File:** `ollama_review.py`, lines 224-233

```python
report = {
    "generated_at": "20260413T054443Z",
    "model": "gemma4:31b",
    "source": "path/to/source.md",
    "total_candidates": 10,
    "completed_reviews": 10,
    "status": "completed",
    "summary": {
        "keep": 5,
        "review_further": 3,
        "reject": 2,
        "high_confidence_keep": 3,
        "high_confidence_reject": 1
    },
    "reviews": [
        {
            "candidate": {...},
            "review": {...}
        }
    ]
}
```

### Text Report Sample

**File:** `ollama_review.py`, lines 185-212

```
Ollama Relationship Review Report

Model: gemma4:31b
Source: 003_Canonical-Knowledge-Layer/shared/relationships/legal-relationships.md
Candidates reviewed: 10
Keep: 5
Review Further: 3
Reject: 2

A -> relates_to -> B
  decision=keep confidence=0.92
  reason=The evidence clearly shows...
  suggested_type=depends_on
```

---

## Section 8: Progress and Control

### Progress Tracking

**File:** `ollama_review.py`, lines 307-314

After each candidate review:
```python
save_progress_report(
    runs_dir=runs_dir,
    model=model,
    source=source,
    candidates=candidates,
    reviews=reviews,
    status="in_progress" if idx < len(candidates) else "completed",
)
```

### Status Values

| Status | When Set |
|--------|----------|
| `in_progress` | After each review (before final) |
| `completed` | After all reviews finish |
| `interrupted` | After KeyboardInterrupt |

### Logging to Console

**File:** `ollama_review.py`, lines 285-305

```
[1/10] Reviewing: concept-A -> relates_to -> concept-B (occurrences=5)
    Done in 45.2s | decision=keep confidence=0.92
```

### Interruption Handling

**File:** `ollama_review.py`, lines 316-328

```python
except KeyboardInterrupt:
    print("")
    print("Interrupted by user. Saving partial review results...")
    save_progress_report(
        runs_dir=runs_dir,
        model=model,
        source=source,
        candidates=candidates,
        reviews=reviews,
        status="interrupted",
    )
    print("Partial results saved.")
    return 130
```

**Key Finding: INTERRUPTION SAFETY IMPLEMENTED.** Partial results are saved on interrupt.

---

## Section 9: Failure and Gap Analysis

### Identified Gaps

| Gap | Status | Evidence |
|-----|--------|----------|
| **No automatic pipeline integration** | CONFIRMED | Review not in `run_pipeline()` |
| **No second-pass review** | NOT IMPLEMENTED | No code for re-review |
| **No confidence threshold enforcement** | NOT IMPLEMENTED | Only counts, no filtering |
| **No batch parallelization** | NOT IMPLEMENTED | Sequential processing |
| **No retry logic for individual candidates** | NOT IMPLEMENTED | Single attempt only |
| **No model fallback** | NOT IMPLEMENTED | Single model per run |
| **No progress resume capability** | PARTIAL | Partial saves, but no resume |

### Inconsistent Logic

1. **High confidence not used for filtering:** Results are counted but not used to auto-accept/reject
2. **No distinction between LLM failure and human review:** Both result in `review_further`
3. **Ollama URL hardcoded:** No configuration file support

### Performance Risks

| Risk | Severity | Description |
|------|----------|-------------|
| Sequential processing | HIGH | 10 candidates × 600s = 100 minutes max |
| No timeout per-candidate | MEDIUM | Global timeout only |
| Model loading per call | MEDIUM | Each request may reload model |

---

## Section 10: Input Preparation for LLM

### Candidate Data Required

The review expects candidates with these fields:
```python
{
    "from": str,        # Source concept ID
    "type": str,       # Relationship type
    "to": str,         # Target concept ID
    "occurrences": int, # Count of mentions
    "sections": list,  # Source sections
    "examples": list   # Example text snippets
}
```

### Source: Relationship Extraction Output

**File:** `relationships_sections.py` produces candidates from markdown content.

**Output location:** `006_System-Manifests/runs/latest_relationship_extraction_sections.json`

---

## Section 11: Output Parsing and Validation

### JSON Parsing

**File:** `ollama_review.py`, lines 101-137

```python
def parse_model_json(text: str) -> dict[str, Any]:
    cleaned = text.strip()

    # Strip markdown fences
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`").strip()
        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:].strip()

    result = json.loads(cleaned)
    # ... validation ...
```

### Validation Steps

1. Decision must be one of: `keep`, `review_further`, `reject`
2. Confidence must be convertible to float, clamped 0.0-1.0
3. Reason must be non-empty string
4. `suggested_type` must be string or null

### Error Handling

**File:** `ollama_review.py`, lines 146-152

```python
except Exception as exc:
    review = {
        "decision": "review_further",
        "confidence": 0.0,
        "reason": f"Ollama review failed: {exc}",
        "suggested_type": None,
    }
```

**Key Finding: GRACEFUL DEGRADATION.** LLM failures default to `review_further` with 0.0 confidence.

---

## Section 12: Second-Pass Review

**Status:** NOT IMPLEMENTED

There is no code for:
- Re-reviewing candidates marked `review_further`
- Human-in-the-loop review
- Batch escalation
- Confidence-based routing

---

## Section 13: Review Result Storage Artifacts

### Files Produced

| Artifact | Path | Purpose |
|----------|------|---------|
| JSON report | `006_System-Manifests/runs/latest_relationship_review_olluma.json` | Machine consumption |
| TXT report | `006_System-Manifests/runs/latest_relationship_review_olluma.txt` | Human review |
| Timestamp copies | `006_System-Manifests/runs/<timestamp>_relationship_review_ollama.*` | Audit trail |

### No Upstream Integration

**Key Finding:** Review results are NOT automatically consumed by any downstream pipeline stage. Results are end-of-line reports only.

---

## Section 14: Code-Ground Summary

### What IS Implemented

- [x] Ollama-based LLM review for candidate relationships
- [x] CLI command `review-relationships-ollama`
- [x] Three decision types: keep, review_further, reject
- [x] Confidence scoring (0.0-1.0)
- [x] Reason generation
- [x] Suggested type hint
- [x] JSON and TXT output reports
- [x] Progress tracking (in_progress, completed, interrupted)
- [x] Interruption handling with partial saves
- [x] Configurable model and timeout
- [x] Markdown fence stripping in responses

### What is NOT Implemented

- [ ] Automatic pipeline integration (manual trigger only)
- [ ] Second-pass review
- [ ] Confidence threshold auto-filtering
- [ ] Batch parallelization
- [ ] Retry logic for failed candidates
- [ ] Model fallback
- [ ] Progress resume capability
- [ ] Configuration file support (hardcoded Ollama URL)
- [ ] Other LLM providers (Ollama only)

---

## Audit Conclusion

The review layer is **IMPLEMENTED** as a standalone, manually-triggered Ollama-based relationship reviewer. It is **NOT integrated** into the automatic pipeline and lacks second-pass review, confidence-based filtering, and parallelization.

**Governance Status:** The review layer exists but is not enforced in the pipeline. It requires manual invocation and manual consumption of results.

---

*End of Review Layer Audit*