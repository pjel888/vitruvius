"""Source-evidence refinement stage — Phase 1C CLI entry point.

Consumes extraction-staging markdown under
`002_Raw-Conversion-Layer/<category>/raw_markdown/<...>/<stem>.md` and
produces a cleaned source-evidence counterpart under
`002_Raw-Conversion-Layer/<category>/refined_markdown/<...>/<stem>.md`
with a sibling `.refined.json` manifest recording every rule applied.

Under the KG-first AEC-MEPFS direction this remains compatibility and evidence
preparation infrastructure. It preserves layer paths and provenance contracts;
it is not a raw-source rewrite, KG rebuild/reset, or authored-backbone cutover.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from ..paths import get_repo_root
from ..utils import utc_now_stamp
from .contract_validator import validate_sidecar_json
from .engine import NormalizationEngine
from .rules_tier_a import TIER_A_RULES
from .rules_tier_b import TIER_B_RULES

# Sprint CLEANUP-1 Stream C1.1 — feature-flag key for the Phase 1B → 1C
# contract validator. Bypass entirely when the flag is off so flag-OFF =
# pre-CLEANUP-1 behavior byte-identical (AD-016 non-breaking contract).
_CONTRACT_VALIDATOR_FLAG = "p1c_contract_validator"


def _sidecar_path_for(markdown_path: Path) -> Path | None:
    """Derive the expected Phase 1B sidecar JSON path for a raw_markdown file.

    Maps ``.../raw_markdown/<sub>/<stem>.md`` →
    ``.../sidecar_json/<sub>/<stem>.json``. Returns None if the input
    path does not contain a ``raw_markdown`` component.
    """
    parts = list(markdown_path.parts)
    if "raw_markdown" not in parts:
        return None
    idx = parts.index("raw_markdown")
    parts[idx] = "sidecar_json"
    return Path(*parts).with_suffix(".json")


def _validate_sidecar_if_enabled(source_path: Path) -> None:
    """Flag-gated, warn-only contract validation of the Phase 1B sidecar.

    Called from ``refine_one_inner`` at document-entry. When
    ``p1c_contract_validator`` is OFF the function is a no-op. When ON,
    a malformed or missing-field sidecar prints a WARNING but does NOT
    abort the refine run — per AD-016 the validator is a
    boundary-sentinel, not a hard gate.

    Perf call: pure dict traversal + JSON parse; cold path (once per
    document); above the Rust Line per AD-036.
    """
    # Import lazily so the flag-OFF fast path does not pay the yaml
    # load cost; also avoids a circular-import risk with the wider
    # vitruvius package at module-import time.
    from vitruvius.spatial._feature_gate import _load_features_cached

    try:
        features = _load_features_cached()
    except Exception:  # pragma: no cover — defensive: feature load must never break refine
        return
    if not features.is_enabled(_CONTRACT_VALIDATOR_FLAG):
        return

    sidecar_path = _sidecar_path_for(source_path)
    if sidecar_path is None or not sidecar_path.exists():
        return

    report = validate_sidecar_json(sidecar_path)
    if report.ok:
        return

    details: list[str] = []
    if report.missing_fields:
        details.append(f"missing_fields={list(report.missing_fields)}")
    if report.nested_errors:
        details.append(f"nested_errors={list(report.nested_errors)}")
    print(
        f"WARNING: Phase 1B sidecar contract check failed for {sidecar_path}: "
        + "; ".join(details)
    )


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

    # Sprint CLEANUP-1 Stream C1.1 — validate Phase 1B sidecar against
    # the v2.0.0 contract. Flag-gated, warn-only (AD-016 non-breaking).
    _validate_sidecar_if_enabled(source_path)

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
