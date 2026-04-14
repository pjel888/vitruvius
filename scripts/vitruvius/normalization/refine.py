"""The `refine` pipeline stage — Phase 1C CLI entry point.

Consumes a raw markdown file under
`002_Raw-Conversion-Layer/<category>/raw_markdown/<...>/<stem>.md` and
produces a cleaned counterpart under
`002_Raw-Conversion-Layer/<category>/refined_markdown/<...>/<stem>.md`
with a sibling `.refined.json` manifest recording every rule applied.

This is the scoped minimum-viable Phase 1C. Tier C semantic rules, full
semantic chunking, and the destructive-guard rollback are not yet wired
in — they are tracked in the Phase 1C plan for a later pass.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from ..paths import get_repo_root
from ..utils import utc_now_stamp
from .engine import NormalizationEngine
from .rules_tier_a import TIER_A_RULES
from .rules_tier_b import TIER_B_RULES


def _build_default_engine() -> NormalizationEngine:
    engine = NormalizationEngine()
    for rule in TIER_A_RULES:
        engine.register(rule)
    for rule in TIER_B_RULES:
        engine.register(rule)
    return engine


def build_refined_paths(relative_markdown_path: str) -> tuple[Path, Path]:
    """Given `001-Laws/raw_markdown/PD-1096/foo.md`, return
    (`001-Laws/refined_markdown/PD-1096/foo.md`,
     `001-Laws/refined_markdown/PD-1096/foo.refined.json`).
    """
    src = Path(relative_markdown_path)
    parts = list(src.parts)
    if "raw_markdown" not in parts:
        raise ValueError(
            f"Expected 'raw_markdown' in source path, got: {relative_markdown_path}"
        )
    idx = parts.index("raw_markdown")
    parts[idx] = "refined_markdown"
    refined = Path(*parts)
    manifest = refined.with_suffix(".refined.json")
    return refined, manifest


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def refine_one_inner(
    *,
    repo_root: Path,
    relative_markdown_path: str,
) -> int:
    conversion_root = repo_root / "002_Raw-Conversion-Layer"
    source_path = conversion_root / relative_markdown_path
    if not source_path.exists():
        print(f"ERROR: Source not found: {source_path}")
        return 1

    raw_text = source_path.read_text(encoding="utf-8")

    engine = _build_default_engine()
    refined_text, audit = engine.run(raw_text, scope="document_text")

    refined_rel, manifest_rel = build_refined_paths(relative_markdown_path)
    refined_path = conversion_root / refined_rel
    manifest_path = conversion_root / manifest_rel

    refined_path.parent.mkdir(parents=True, exist_ok=True)
    refined_path.write_text(refined_text, encoding="utf-8")

    manifest = {
        "schema_version": "1.0.0",
        "generated_at_utc": utc_now_stamp(),
        "source_relative_path": relative_markdown_path,
        "refined_relative_path": refined_rel.as_posix(),
        "source_hash": _sha256(raw_text),
        "output_hash": _sha256(refined_text),
        "chars_before": len(raw_text),
        "chars_after": len(refined_text),
        "chars_delta": len(refined_text) - len(raw_text),
        "rules_count": len(audit),
        "rules_applied": [entry["rule"] for entry in audit],
        "rules_changed_text": [entry["rule"] for entry in audit if entry["changed"]],
        "audit": audit,
        "manual_review": False,
        "manual_review_reason": None,
    }
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    return 0


def run_refine_one(*, relative_markdown_path: str) -> int:
    return refine_one_inner(
        repo_root=get_repo_root(),
        relative_markdown_path=relative_markdown_path,
    )


def run_refine() -> int:
    """Batch-refine every `raw_markdown` file under 002_Raw-Conversion-Layer."""
    repo_root = get_repo_root()
    conversion_root = repo_root / "002_Raw-Conversion-Layer"
    if not conversion_root.exists():
        print("No conversion layer found.")
        return 0

    processed = 0
    failed = 0
    for md_path in sorted(conversion_root.rglob("*.md")):
        rel = md_path.relative_to(conversion_root).as_posix()
        if "raw_markdown" not in Path(rel).parts:
            continue
        rc = refine_one_inner(
            repo_root=repo_root,
            relative_markdown_path=rel,
        )
        if rc == 0:
            processed += 1
        else:
            failed += 1

    print(f"refine (batch) complete. Processed: {processed}, Failed: {failed}")
    return 0 if failed == 0 else 1
