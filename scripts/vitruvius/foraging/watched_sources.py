"""Stream O.1 — YAML loader for the watched-sources registry.

The registry declares which external sources the pipeline *will*
monitor once a fetcher ships. The loader validates every row against
the Sprint H non-negotiable rules — HTTPS URL, known frequency,
unique source name — so malformed YAML fails loudly at load time.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import yaml


class WatchedSourcesError(ValueError):
    """Raised when a watched-sources YAML file is malformed."""


_ALLOWED_FREQUENCIES = frozenset({"daily", "weekly", "monthly"})


@dataclass(frozen=True)
class WatchedSource:
    name: str
    url: str
    category: str
    subcategory: Optional[str]
    frequency: str


def load_watched_sources(yaml_path: Path) -> list[WatchedSource]:
    """Parse ``yaml_path`` and return a list of :class:`WatchedSource`.

    The expected top-level shape is a mapping with a ``sources`` key
    holding a list of per-source dicts. An empty or missing list
    returns ``[]``. Any validation failure raises
    :class:`WatchedSourcesError` with an index-qualified message so
    operators can pinpoint the offending row.
    """
    raw = yaml.safe_load(Path(yaml_path).read_text(encoding="utf-8")) or {}
    rows = raw.get("sources", [])
    out: list[WatchedSource] = []
    seen: set[str] = set()
    for idx, row in enumerate(rows):
        if not isinstance(row, dict):
            raise WatchedSourcesError(f"sources[{idx}] must be a mapping")
        name = row.get("name")
        url = row.get("url")
        category = row.get("category")
        frequency = row.get("frequency")
        subcategory = row.get("subcategory")
        if not isinstance(name, str) or not name:
            raise WatchedSourcesError(f"sources[{idx}].name missing or empty")
        if name in seen:
            raise WatchedSourcesError(f"duplicate source name {name!r}")
        seen.add(name)
        if not isinstance(url, str) or not url.startswith("https://"):
            raise WatchedSourcesError(
                f"sources[{idx}].url must start with 'https://' (got {url!r})"
            )
        if not isinstance(category, str) or not category:
            raise WatchedSourcesError(f"sources[{idx}].category must be a string")
        if frequency not in _ALLOWED_FREQUENCIES:
            raise WatchedSourcesError(
                f"sources[{idx}].frequency {frequency!r} not in "
                f"{sorted(_ALLOWED_FREQUENCIES)}"
            )
        out.append(
            WatchedSource(
                name=name,
                url=url,
                category=category,
                subcategory=subcategory if isinstance(subcategory, str) else None,
                frequency=frequency,
            )
        )
    return out
