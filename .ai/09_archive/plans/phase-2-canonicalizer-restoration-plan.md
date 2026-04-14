---
plan_id: phase-2-canonicalizer-restoration
phase: 2
title: Canonicalizer Restoration — Structured Section Generation
status: planned
priority: medium
sprint: "Sprint C (weeks 7-12)"
version: 1.0.0
plan_type: implementation_tdd
created: 2026-04-14
last_updated: 2026-04-14
owner: Senior Systems Architect
prerequisites:
  - Phase 1C Centralized Normalization (refined Markdown is the input)
  - Phase 2 current skeleton (rules engine + ID system) — verified complete
dependencies:
  - .ai/06_specs/source-schema.md
  - scripts/vitruvius/canonicalize.py (existing skeleton)
  - 003_Canonical-Knowledge-Layer/shared/sources/ (hand-curated golden set)
related_plans:
  - phase-3-concept-enrichment-plan.md (runs after this)
unblocks:
  - Phase 3C concept enrichment (needs structural sections to extract definitions)
---

# Phase 2 — Canonicalizer Restoration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` or `superpowers:executing-plans`.

**Goal:** Restore structured-section generation in `canonicalize.py` so canonical source files match the shape in `/.ai/06_specs/source-schema.md` §5 (Overview, Coverage, Key Points, Referenced Concepts) rather than the current frontmatter-only regression (RI-011).

**Architecture:** Extend `canonicalize.py` with a `build_structured_body()` function that reads the refined Markdown, extracts section candidates via header detection, pulls key points from numbered/bulleted lists, and resolves referenced concepts against `003/shared/concepts/`. Add diff-before-write protection so existing hand-curated files are never overwritten silently. Add a batch mode.

**Tech Stack:** Python stdlib only. PyYAML for frontmatter parsing.

---

## Why This Is a "Restoration"
The 2026-04-13 codebase audit found hand-curated canonical files with richer structure (Overview / Coverage / Key Points / Referenced Concepts) than what `canonicalize.py` currently generates. The audit concluded *"this suggests the current script is a regression or a simplified replacement for a tool that is no longer in the repo."* We rebuild rather than revert because the old tool is gone.

## File Structure

| Path | Change |
|---|---|
| `scripts/vitruvius/canonicalize.py` | Modify — add `build_structured_body`, `extract_key_points`, `resolve_referenced_concepts`, `run_canonicalize` (batch) |
| `scripts/vitruvius/canonical_diff.py` | New — diff-before-write protection |
| `scripts/pipeline_cli.py` | Modify — add `canonicalize` batch command |
| `scripts/tests/test_canonicalize_body.py` | New |
| `scripts/tests/test_canonical_diff.py` | New |
| `scripts/tests/fixtures/refined_pd_1096_sample.md` | New — small synthetic refined document |

---

## Task 1: Header & Key-Point Extractor

- [ ] **Step 1.1: Create the fixture**

Create `scripts/tests/fixtures/refined_pd_1096_sample.md`:
```markdown
# National Building Code of the Philippines

## Section 101 — Title

This Decree shall be known as the "National Building Code of the Philippines"...

## Section 102 — Declaration of Policy

It is hereby declared to be the policy of the State to safeguard life, health,
property, and public welfare...

## Section 301 — Building Permits

No person, firm, or corporation, including any agency or instrumentality of the
government shall erect, construct, alter, repair, move, convert or demolish
any building or structure without first obtaining a building permit...

## Section 701 — Occupancy Classified

Every building shall be classified in accordance with its use or occupancy.
Occupancy classification determines the applicable fire-resistive requirements.
```

- [ ] **Step 1.2: Write failing tests**

Create `scripts/tests/test_canonicalize_body.py`:
```python
from pathlib import Path

from vitruvius.canonicalize import (
    extract_section_headers,
    extract_key_points,
    build_overview_paragraph,
)


FIXTURE = Path(__file__).parent / "fixtures" / "refined_pd_1096_sample.md"


def test_extract_section_headers_returns_coverage_items():
    text = FIXTURE.read_text(encoding="utf-8")
    headers = extract_section_headers(text)
    assert len(headers) == 4
    assert headers[0]["level"] == 2
    assert "Title" in headers[0]["title"]


def test_extract_key_points_returns_top_n_sentences():
    text = FIXTURE.read_text(encoding="utf-8")
    key_points = extract_key_points(text, limit=3)
    assert 1 <= len(key_points) <= 3
    assert all(len(kp) < 300 for kp in key_points)


def test_build_overview_paragraph_returns_first_non_header_para():
    text = FIXTURE.read_text(encoding="utf-8")
    overview = build_overview_paragraph(text)
    assert "National Building Code" in overview
    assert not overview.startswith("#")
```

- [ ] **Step 1.3: Implement the three extractors**

Append to `scripts/vitruvius/canonicalize.py`:
```python
def extract_section_headers(markdown_text: str) -> list[dict]:
    headers = []
    for line in markdown_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("## "):
            headers.append({"level": 2, "title": stripped[3:].strip()})
        elif stripped.startswith("### "):
            headers.append({"level": 3, "title": stripped[4:].strip()})
    return headers


def extract_key_points(markdown_text: str, *, limit: int = 5) -> list[str]:
    """Pick short, standalone assertions: first sentence after each H2 that is
    not itself a header, trimmed to 300 chars."""
    points: list[str] = []
    current: list[str] = []
    collecting = False

    for line in markdown_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("## "):
            if current:
                sentence = " ".join(current).split(". ")[0].strip()
                if sentence:
                    points.append(sentence[:300].rstrip(".") + ".")
            current = []
            collecting = True
            continue
        if collecting and stripped and not stripped.startswith("#"):
            current.append(stripped)

    if current:
        sentence = " ".join(current).split(". ")[0].strip()
        if sentence:
            points.append(sentence[:300].rstrip(".") + ".")

    return points[:limit]


def build_overview_paragraph(markdown_text: str) -> str:
    for line in markdown_text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        return stripped[:500]
    return ""
```

- [ ] **Step 1.4: Run tests**

```bash
PYTHONPATH=scripts python -m pytest scripts/tests/test_canonicalize_body.py -v
```
Expected: `3 passed`

- [ ] **Step 1.5: Commit**

```bash
git add scripts/vitruvius/canonicalize.py scripts/tests/test_canonicalize_body.py scripts/tests/fixtures/refined_pd_1096_sample.md
git commit -m "feat(canonicalize): extract section headers, key points, and overview paragraph"
```

---

## Task 2: Referenced Concept Resolver

- [ ] **Step 2.1: Write the failing test**

Append to `scripts/tests/test_canonicalize_body.py`:
```python
from vitruvius.canonicalize import resolve_referenced_concepts


def test_resolve_referenced_concepts_from_text(tmp_path):
    concepts_dir = tmp_path / "003_Canonical-Knowledge-Layer" / "shared" / "concepts"
    concepts_dir.mkdir(parents=True)
    for slug in ("occupancy-classification", "fire-resistive-construction", "building-permit"):
        (concepts_dir / f"{slug}.md").write_text(
            f"---\nid: concept-{slug}\ntitle: {slug}\npage_type: concept\n"
            "canonical_status: placeholder\n"
            "last_canonicalized_utc: 2026-04-14T00:00:00Z\n---\n",
            encoding="utf-8",
        )

    body = (
        "Every building shall be classified by occupancy classification. "
        "Fire-resistive construction is determined by occupancy. "
        "A building permit must be obtained before construction."
    )
    resolved = resolve_referenced_concepts(body, repo_root=tmp_path)
    assert "concept-occupancy-classification" in resolved
    assert "concept-fire-resistive-construction" in resolved
    assert "concept-building-permit" in resolved
```

- [ ] **Step 2.2: Run test to verify failure**

```bash
PYTHONPATH=scripts python -m pytest scripts/tests/test_canonicalize_body.py::test_resolve_referenced_concepts_from_text -v
```

- [ ] **Step 2.3: Implement the resolver**

Append to `scripts/vitruvius/canonicalize.py`:
```python
def _concept_title_from_slug(slug: str) -> str:
    return slug.replace("-", " ")


def resolve_referenced_concepts(body: str, *, repo_root: Path) -> list[str]:
    concepts_dir = Path(repo_root) / "003_Canonical-Knowledge-Layer" / "shared" / "concepts"
    if not concepts_dir.exists():
        return []

    body_lower = body.lower()
    found: list[str] = []
    for md in sorted(concepts_dir.glob("*.md")):
        slug = md.stem
        title = _concept_title_from_slug(slug)
        if title in body_lower or title.replace(" ", "-") in body_lower:
            found.append(f"concept-{slug}")

    return found
```

- [ ] **Step 2.4: Run test and commit**

```bash
PYTHONPATH=scripts python -m pytest scripts/tests/test_canonicalize_body.py -v
git add scripts/vitruvius/canonicalize.py scripts/tests/test_canonicalize_body.py
git commit -m "feat(canonicalize): resolve referenced concepts from body against shared/concepts"
```

---

## Task 3: Diff-Before-Write Protection

**Files:**
- Create: `scripts/vitruvius/canonical_diff.py`
- Create: `scripts/tests/test_canonical_diff.py`

- [ ] **Step 3.1: Write the failing test**

Create `scripts/tests/test_canonical_diff.py`:
```python
from pathlib import Path

from vitruvius.canonical_diff import should_overwrite, WriteDecision


def test_draft_files_can_be_overwritten(tmp_path):
    p = tmp_path / "pd-1096.md"
    p.write_text(
        "---\nid: law-pd-1096\npage_type: source\ncanonical_status: draft\n---\n# X\n",
        encoding="utf-8",
    )
    decision = should_overwrite(p, new_body="newer content")
    assert decision.allowed
    assert decision.reason == "draft"


def test_enriched_files_are_protected(tmp_path):
    p = tmp_path / "pd-1096.md"
    p.write_text(
        "---\nid: law-pd-1096\npage_type: source\ncanonical_status: enriched\n---\n# X\n",
        encoding="utf-8",
    )
    decision = should_overwrite(p, new_body="newer content")
    assert not decision.allowed
    assert "enriched" in decision.reason


def test_nonexistent_files_can_be_written(tmp_path):
    p = tmp_path / "new.md"
    decision = should_overwrite(p, new_body="")
    assert decision.allowed
    assert decision.reason == "new_file"


def test_identical_content_is_noop(tmp_path):
    p = tmp_path / "pd-1096.md"
    content = (
        "---\nid: law-pd-1096\npage_type: source\ncanonical_status: draft\n---\n# X\n"
    )
    p.write_text(content, encoding="utf-8")
    decision = should_overwrite(p, new_body=content)
    assert not decision.allowed
    assert decision.reason == "unchanged"
```

- [ ] **Step 3.2: Run test to verify failure**

```bash
PYTHONPATH=scripts python -m pytest scripts/tests/test_canonical_diff.py -v
```

- [ ] **Step 3.3: Implement `canonical_diff.py`**

```python
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass
class WriteDecision:
    allowed: bool
    reason: str


PROTECTED_STATUSES = {"enriched", "verified", "superseded"}


def _parse_frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    try:
        return yaml.safe_load(text[3:end].strip()) or {}
    except yaml.YAMLError:
        return {}


def should_overwrite(path: Path, new_body: str) -> WriteDecision:
    if not path.exists():
        return WriteDecision(allowed=True, reason="new_file")

    existing = path.read_text(encoding="utf-8")
    if existing == new_body:
        return WriteDecision(allowed=False, reason="unchanged")

    fm = _parse_frontmatter(existing)
    status = fm.get("canonical_status", "unknown")

    if status in PROTECTED_STATUSES:
        return WriteDecision(allowed=False, reason=f"{status}_protected")
    return WriteDecision(allowed=True, reason=status or "unknown")
```

- [ ] **Step 3.4: Run test and commit**

```bash
PYTHONPATH=scripts python -m pytest scripts/tests/test_canonical_diff.py -v
git add scripts/vitruvius/canonical_diff.py scripts/tests/test_canonical_diff.py
git commit -m "feat(canonicalize): add diff-before-write protection for enriched+ files"
```

---

## Task 4: Integrate Structured Body into `run_canonicalize_one`

- [ ] **Step 4.1: Replace `run_canonicalize_one`**

Edit `scripts/vitruvius/canonicalize.py` — replace `run_canonicalize_one` with:
```python
from .canonical_diff import should_overwrite


def build_structured_source_file(
    *,
    repo_root: Path,
    relative_markdown_path: str,
) -> tuple[Path, str]:
    source_path = repo_root / CONVERSION_LAYER_NAME / relative_markdown_path
    if not source_path.exists():
        raise FileNotFoundError(f"Refined markdown not found: {source_path}")

    refined_text = source_path.read_text(encoding="utf-8")
    plan = build_plan(relative_markdown_path)

    headers = extract_section_headers(refined_text)
    key_points = extract_key_points(refined_text, limit=5)
    overview = build_overview_paragraph(refined_text)
    referenced = resolve_referenced_concepts(refined_text, repo_root=repo_root)

    lines = [
        "---",
        f"id: {plan['canonical_id']}",
        f"title: {plan['title']}",
        "page_type: source",
        f"trust_level: {plan['trust']}",
        "canonical_status: draft",
        f"last_canonicalized_utc: {datetime.now(timezone.utc).isoformat()}",
    ]
    if plan["aliases"]:
        lines.append("aliases:")
        for a in plan["aliases"]:
            lines.append(f"  - {a}")
    lines.append("---")
    lines.append("")
    lines.append(f"# {plan['title']}")
    lines.append("")
    lines.append("## Overview")
    lines.append("")
    lines.append(overview or f"{plan['title']} is a canonical source within the Vitruvius system.")
    lines.append("")
    lines.append("## Coverage")
    lines.append("")
    for h in headers:
        lines.append(f"- {h['title']}")
    if not headers:
        lines.append("- (no headers detected in refined source)")
    lines.append("")
    lines.append("## Key Points")
    lines.append("")
    for kp in key_points:
        lines.append(f"- {kp}")
    if not key_points:
        lines.append("- (no key points extracted)")
    lines.append("")
    lines.append("## Referenced Concepts")
    lines.append("")
    for ref in referenced:
        lines.append(f"- {ref}")
    if not referenced:
        lines.append("- (none resolved against shared/concepts)")
    lines.append("")

    target = repo_root / "003_Canonical-Knowledge-Layer" / "shared" / "sources"
    target.mkdir(parents=True, exist_ok=True)
    filename = f"{slugify(plan['title'])}.md"
    target_file = target / filename
    return target_file, "\n".join(lines)


def run_canonicalize_one(*, relative_markdown_path: str) -> int:
    repo_root = get_repo_root()
    try:
        target_file, content = build_structured_source_file(
            repo_root=repo_root,
            relative_markdown_path=relative_markdown_path,
        )
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}")
        return 1

    decision = should_overwrite(target_file, content)
    if not decision.allowed:
        print(f"SKIP ({decision.reason}): {target_file}")
        return 0

    target_file.write_text(content, encoding="utf-8")
    print(f"canonicalize-one complete. Wrote: {target_file}")
    return 0
```

- [ ] **Step 4.2: Write an integration test**

Create `scripts/tests/test_canonicalize_integration.py`:
```python
from pathlib import Path
from unittest.mock import patch

from vitruvius.canonicalize import build_structured_source_file


def test_builds_file_with_all_four_sections(tmp_path):
    # Seed a refined markdown file
    refined = tmp_path / "002_Raw-Conversion-Layer" / "001-Laws" / "raw_markdown"
    refined.mkdir(parents=True)
    (refined / "sample.md").write_text(
        "# Sample Law\n\nThis law governs buildings.\n\n"
        "## Section 1\n\nAll buildings must have permits.\n\n"
        "## Section 2\n\nFire safety is mandatory.\n",
        encoding="utf-8",
    )
    (tmp_path / "003_Canonical-Knowledge-Layer" / "shared" / "concepts").mkdir(parents=True)

    with patch("vitruvius.canonicalize.get_repo_root", return_value=tmp_path):
        with patch("vitruvius.canonicalize.load_rules", return_value={"rules": []}):
            target, content = build_structured_source_file(
                repo_root=tmp_path,
                relative_markdown_path="001-Laws/raw_markdown/sample.md",
            )

    assert "## Overview" in content
    assert "## Coverage" in content
    assert "## Key Points" in content
    assert "## Referenced Concepts" in content
    assert "Section 1" in content  # header should appear in Coverage
```

- [ ] **Step 4.3: Run all canonicalize tests**

```bash
PYTHONPATH=scripts python -m pytest scripts/tests/test_canonicalize_body.py scripts/tests/test_canonical_diff.py scripts/tests/test_canonicalize_integration.py -v
```

- [ ] **Step 4.4: Commit**

```bash
git add scripts/vitruvius/canonicalize.py scripts/tests/test_canonicalize_integration.py
git commit -m "feat(canonicalize): emit Overview/Coverage/Key Points/Referenced Concepts sections"
```

---

## Task 5: Batch Mode

- [ ] **Step 5.1: Add `run_canonicalize_batch`**

Append to `scripts/vitruvius/canonicalize.py`:
```python
def run_canonicalize() -> int:
    """Walk 002_Raw-Conversion-Layer/*/raw_markdown and canonicalize each file."""
    repo_root = get_repo_root()
    conversion_root = repo_root / CONVERSION_LAYER_NAME
    if not conversion_root.exists():
        print("No conversion layer found.")
        return 0

    processed = 0
    skipped = 0
    for md_path in sorted(conversion_root.rglob("raw_markdown/**/*.md")):
        rel = md_path.relative_to(conversion_root).as_posix()
        rc = run_canonicalize_one(relative_markdown_path=rel)
        if rc == 0:
            processed += 1
        else:
            skipped += 1

    print(f"canonicalize (batch) complete. Processed: {processed}, Skipped: {skipped}")
    return 0
```

- [ ] **Step 5.2: Register CLI command**

In `scripts/pipeline_cli.py`:
```python
from vitruvius.canonicalize import run_canonicalize, run_canonicalize_one, run_canonicalize_plan_one
```
Add subcommand:
```python
    subparsers.add_parser("canonicalize")
```
Dispatch:
```python
    if args.command == "canonicalize":
        return run_canonicalize()
```

- [ ] **Step 5.3: Smoke-test and commit**

```bash
python scripts/pipeline_cli.py canonicalize --help
python scripts/pipeline_cli.py canonicalize
git add scripts/vitruvius/canonicalize.py scripts/pipeline_cli.py
git commit -m "feat(canonicalize): add batch run_canonicalize command"
```

---

## Self-Review Checklist

- **Schema coverage:** All four required body sections from `/.ai/06_specs/source-schema.md` §5 are generated.
- **Protection:** `enriched` / `verified` / `superseded` files are never overwritten silently.
- **Non-regression:** `canonicalize-plan-one` remains intact; only `canonicalize-one` is rewritten.
- **No placeholders:** Every code block complete; no TBD.

## Execution Handoff

Recommended: Subagent-driven. Task 4 is large and benefits from a fresh context.
