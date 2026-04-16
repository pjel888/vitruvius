from __future__ import annotations

from pathlib import Path

from .canonicalize import build_plan


def canonical_source_id_for_relative_path(relative_path: str) -> str:
    try:
        plan = build_plan(relative_path)
        canonical_id = plan.get("canonical_id")
        if isinstance(canonical_id, str) and canonical_id.strip():
            return canonical_id
    except Exception:
        pass

    stem = Path(relative_path).stem.lower()
    if "ra9514" in stem or "ra-9514" in stem:
        return "irr-implementing-rules-and-regulations-of-the-fire-code-of-the-philippines"
    if "bp220" in stem or "bp-220" in stem:
        return "irr-revised-implementing-rules-and-regulations-of-batas-pambansa-blg-220"
    if "bp344" in stem or "bp-344" in stem:
        return "irr-revised-implementing-rules-and-regulations-of-batas-pambansa-blg-344"
    if "irr" in stem:
        return "irr-implementing-rules-and-regulations-of-the-national-building-code"
    return "law-national-building-code-of-the-philippines"
