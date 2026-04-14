from __future__ import annotations

import warnings
from datetime import datetime, timezone


def utc_now_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def iso_utc_from_timestamp(ts: float) -> str:
    return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()


def normalize_filename(name: str) -> str:
    """DEPRECATED: use direct slugify logic or Path operations.

    Preserved for backward compatibility with pre-Phase-1C callers.
    Behavior unchanged: lowercase the stem, strip non-alphanumerics,
    append the lowercased suffix.
    """
    warnings.warn(
        "normalize_filename is deprecated; migrate callers to direct slugify "
        "logic or to vitruvius.normalization when a general text pipeline is needed.",
        DeprecationWarning,
        stacklevel=2,
    )
    from pathlib import Path

    path = Path(name)
    stem = "".join(ch.lower() for ch in path.stem if ch.isalnum())
    ext = path.suffix.lower()
    return f"{stem}{ext}"


def normalize_text(text: str) -> str:
    """DEPRECATED: use vitruvius.normalization.NormalizationEngine instead.

    Preserved for backward compatibility with pre-Phase-1C callers. Behavior
    matches the historical " ".join(text.split()) — whitespace-collapse only.
    """
    warnings.warn(
        "utils.normalize_text is deprecated; use "
        "vitruvius.normalization.NormalizationEngine for document text.",
        DeprecationWarning,
        stacklevel=2,
    )
    return " ".join(text.split())


def safe_name_for_report(name: str) -> str:
    return "".join(ch if ch.isalnum() else "_" for ch in name)
