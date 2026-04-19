"""Diff-before-write protection for the canonical layer.

Canonicalizer regenerates files from refined markdown, but users may have
manually edited enriched or verified records. This guard ensures the
canonicalizer never overwrites those silently — it either skips the write
entirely (if content is unchanged after stripping volatile fields) or
rejects it (if status is protected).
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass
class WriteDecision:
    allowed: bool
    reason: str


PROTECTED_STATUSES = {"enriched", "verified", "superseded"}

# Frontmatter fields that change on every regeneration without affecting
# the semantic payload. Strip them before comparing content so that
# timestamp-only diffs count as unchanged.
VOLATILE_FIELDS = (
    "last_canonicalized_utc",
    "enriched_at_utc",
    "reviewed_at_utc",
    "promotion_batch_id",
    "last_promoted_utc",
    "promotion_audit_log_ref",
)

# Compiled once — used by _strip_volatile_frontmatter.
_VOLATILE_FIELD_PATTERNS = [
    re.compile(rf"^{re.escape(field)}:.*$", re.MULTILINE)
    for field in VOLATILE_FIELDS
]


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


def _strip_volatile_frontmatter(text: str) -> str:
    """Remove volatile YAML frontmatter fields so timestamp-only diffs count
    as unchanged. Operates line-by-line inside the frontmatter block; leaves
    the markdown body untouched.
    """
    if not text.startswith("---"):
        return text
    end = text.find("\n---", 3)
    if end == -1:
        return text

    header = text[:end]
    rest = text[end:]

    cleaned_header = header
    for pattern in _VOLATILE_FIELD_PATTERNS:
        cleaned_header = pattern.sub("", cleaned_header)

    # Collapse any blank lines that the stripping left behind.
    cleaned_header = re.sub(r"\n{2,}", "\n", cleaned_header)
    return cleaned_header + rest


def should_overwrite(path: Path, new_body: str, force: bool = False) -> WriteDecision:
    if not path.exists():
        return WriteDecision(allowed=True, reason="new_file")

    existing = path.read_text(encoding="utf-8")

    # Compare with volatile fields stripped so timestamp-only diffs don't
    # cause a rewrite (AD-012-equivalent pattern for the canonical layer).
    if not force and _strip_volatile_frontmatter(existing) == _strip_volatile_frontmatter(new_body):
        return WriteDecision(allowed=False, reason="unchanged")

    fm = _parse_frontmatter(existing)
    status = fm.get("canonical_status", "unknown")

    if status in PROTECTED_STATUSES:
        return WriteDecision(allowed=False, reason=f"{status}_protected")
    return WriteDecision(allowed=True, reason=status or "unknown")
