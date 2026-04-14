"""Diff-before-write protection for the canonical layer.

Canonicalizer regenerates files from refined markdown, but users may have
manually edited enriched or verified records. This guard ensures the
canonicalizer never overwrites those silently — it either skips the write
entirely (if content is unchanged) or rejects it (if status is protected).
"""

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
