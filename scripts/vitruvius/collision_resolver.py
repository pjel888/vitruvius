"""Sprint CLEANUP-1 Stream C1.2 — hash-disambiguated slug collision resolver.

Protects Principle P6 (Immutable canonical IDs): once a source path has
been assigned a canonical ID, that mapping is permanent. If a new source
path would produce a colliding ID, the resolver appends a short MD5 hash
of the source path and records the mapping in `slug_alias_registry.yaml`.

Re-resolving the same source path returns the previously-assigned ID
(idempotency). The registry is YAML so a human can audit it.

Gated behind `p1c_slug_collision_policy`. When the flag is off, the
resolver is bypassed and canonicalize.py falls back to the current
`build_canonical_id()` behavior (silent overwrite).

Perf call: pure string / dict ops, above the Rust Line (AD-036).
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Optional, Set

import yaml


_HASH_LEN = 6  # first 6 hex chars of md5(source_path) — ~16M disambiguations


@dataclass
class SlugAliasRegistry:
    path: Path
    entries: Dict[str, str] = field(default_factory=dict)

    @classmethod
    def load(cls, path: Path) -> "SlugAliasRegistry":
        if not path.exists():
            return cls(path=path, entries={})
        raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        entries = dict(raw.get("collisions") or {})
        return cls(path=path, entries=entries)

    def get(self, source_path: str) -> Optional[str]:
        return self.entries.get(source_path)

    def record(self, source_path: str, resolved_id: str) -> None:
        # Append-only per P6; never overwrite an existing entry
        if source_path in self.entries and self.entries[source_path] != resolved_id:
            raise ValueError(
                f"SlugAliasRegistry: refusing to overwrite existing entry "
                f"{source_path!r} (was {self.entries[source_path]!r}, "
                f"attempted {resolved_id!r}). Principle P6."
            )
        self.entries[source_path] = resolved_id

    def save(self) -> None:
        self.path.write_text(
            yaml.safe_dump({"collisions": self.entries}, sort_keys=True),
            encoding="utf-8",
        )


def _short_hash(source_path: str) -> str:
    return hashlib.md5(source_path.encode("utf-8")).hexdigest()[:_HASH_LEN]


def resolve_canonical_id(
    *,
    prefix: str,
    slug: str,
    source_path: str,
    existing_ids: Set[str],
    registry: SlugAliasRegistry,
) -> str:
    """Return a canonical id that does not collide with existing_ids.

    1. If the source_path already has a registry entry, return it (idempotency).
    2. Otherwise compute `{prefix}-{slug}`.
    3. If that id is not in existing_ids, return it unchanged.
    4. Otherwise append `-{_short_hash(source_path)}`, record in registry,
       return the disambiguated id.
    """
    existing_entry = registry.get(source_path)
    if existing_entry is not None:
        return existing_entry

    base = f"{prefix}-{slug}"
    if base not in existing_ids:
        return base

    disambiguated = f"{base}-{_short_hash(source_path)}"
    registry.record(source_path, disambiguated)
    return disambiguated
