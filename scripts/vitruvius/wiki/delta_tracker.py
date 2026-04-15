"""Sprint WIKI Stream WIKI.4.1 — SHA-256 delta tracking for wiki pages.

Sits on top of the Sprint HP.1 Merkle primitive but works at the
per-file granularity that the WIKI synthesis loop needs. Callers
snapshot a wiki directory into a manifest file, then later re-walk
the directory and get a :class:`DeltaReport` naming the new, changed,
and removed pages since the snapshot.

The manifest is JSON so it can be git-tracked alongside the wiki
itself. Operators that want to "start fresh" simply delete the
manifest file.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping


@dataclass(frozen=True)
class PageDigest:
    relative_path: str
    sha256: str


@dataclass(frozen=True)
class DeltaReport:
    new: list[str]
    changed: list[str]
    removed: list[str]


def _hash_file(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


class DeltaTracker:
    """Snapshot + diff a wiki directory by per-file SHA-256."""

    def __init__(self, *, manifest_path: Path) -> None:
        self._manifest_path = Path(manifest_path)

    def _load_manifest(self) -> Mapping[str, str]:
        if not self._manifest_path.exists():
            return {}
        try:
            raw = json.loads(self._manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
        if not isinstance(raw, dict):
            return {}
        return {str(k): str(v) for k, v in raw.items()}

    def _save_manifest(self, digests: Mapping[str, str]) -> None:
        self._manifest_path.parent.mkdir(parents=True, exist_ok=True)
        self._manifest_path.write_text(
            json.dumps(dict(sorted(digests.items())), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    def _walk_digests(self, wiki_root: Path) -> dict[str, str]:
        wiki_root = Path(wiki_root)
        out: dict[str, str] = {}
        for path in sorted(wiki_root.rglob("*.md")):
            if not path.is_file() or path.is_symlink():
                continue
            rel = path.relative_to(wiki_root).as_posix()
            out[rel] = _hash_file(path)
        return out

    def commit_snapshot(self, wiki_root: Path) -> None:
        """Walk ``wiki_root`` and persist its per-file digest map."""
        digests = self._walk_digests(wiki_root)
        self._save_manifest(digests)

    def compute_delta(self, wiki_root: Path) -> DeltaReport:
        """Compare the current state of ``wiki_root`` against the last
        committed manifest.

        Returns sorted lists of ``new``, ``changed``, and ``removed``
        relative paths. Does NOT update the manifest — callers that
        want to advance the snapshot follow a compute_delta call with
        :meth:`commit_snapshot`.
        """
        previous = self._load_manifest()
        current = self._walk_digests(wiki_root)

        prev_keys = set(previous.keys())
        curr_keys = set(current.keys())

        new_paths = sorted(curr_keys - prev_keys)
        removed_paths = sorted(prev_keys - curr_keys)
        changed_paths = sorted(
            path
            for path in (curr_keys & prev_keys)
            if previous[path] != current[path]
        )

        return DeltaReport(
            new=new_paths,
            changed=changed_paths,
            removed=removed_paths,
        )
