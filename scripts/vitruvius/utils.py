from __future__ import annotations

from datetime import datetime, timezone


def utc_now_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def iso_utc_from_timestamp(ts: float) -> str:
    return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()


def normalize_filename(name: str) -> str:
    from pathlib import Path

    path = Path(name)
    stem = "".join(ch.lower() for ch in path.stem if ch.isalnum())
    ext = path.suffix.lower()
    return f"{stem}{ext}"


def normalize_text(text: str) -> str:
    return " ".join(text.split())


def safe_name_for_report(name: str) -> str:
    return "".join(ch if ch.isalnum() else "_" for ch in name)