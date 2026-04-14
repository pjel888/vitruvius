"""Sprint HP Stream HP.1 — Merkle directory hash for zero-RAM status.

Replaces ``O(N)`` full-directory content walks with a single
``O(log N)`` Merkle-tree digest. The tree is rebuilt lazily (hash of
every file's SHA-256 concatenated in stable order) and stored in the
System Manifests so subsequent ``run_status`` invocations can short-
circuit unchanged subtrees.

HP.1 delivers the pure-Python primitives:
  * :func:`calculate_directory_hash` — walks a directory tree and
    returns a :class:`DirectoryHash` with the root digest + recursive
    file count.
  * :func:`dir_has_changed` — idempotent check against a previously
    persisted digest.

Wiring the digest into ``scanner.py`` and ``run_status`` (the HP.1.2
and HP.1.3 tasks) is a follow-on that touches the existing scanner
call path; this module is the pure primitive the follow-on builds on.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path


_CHUNK_SIZE = 1 << 20  # 1 MiB streaming reads


@dataclass(frozen=True)
class DirectoryHash:
    """Result of :func:`calculate_directory_hash`.

    ``digest`` is a hex-encoded SHA-256 over (relative_path, file_digest)
    pairs sorted by relative path. ``file_count`` is the total number
    of regular files under the root (recursive).
    """

    digest: str
    file_count: int


def _hash_file(path: Path) -> str:
    """Streaming SHA-256 of a single file."""
    hasher = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(_CHUNK_SIZE), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def calculate_directory_hash(root: Path) -> DirectoryHash:
    """Compute a Merkle-style root hash for the directory tree at ``root``.

    Walk is stable: files are visited in lexicographically sorted
    order of their path relative to ``root``. Each file contributes
    ``<rel_path>\\t<file_sha256>\\n`` to the root hasher, so either
    renaming or mutating any file changes the root digest.

    Symlinks and non-file entries are skipped so the hash stays a
    pure content fingerprint of the regular-file subtree.
    """
    root = Path(root)
    if not root.exists():
        return DirectoryHash(
            digest=hashlib.sha256(b"").hexdigest(),
            file_count=0,
        )

    entries: list[tuple[str, str]] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.is_symlink():
            continue
        rel = path.relative_to(root).as_posix()
        entries.append((rel, _hash_file(path)))

    hasher = hashlib.sha256()
    for rel, file_hash in entries:
        hasher.update(rel.encode("utf-8"))
        hasher.update(b"\t")
        hasher.update(file_hash.encode("ascii"))
        hasher.update(b"\n")

    return DirectoryHash(digest=hasher.hexdigest(), file_count=len(entries))


def dir_has_changed(root: Path, *, previous_digest: str) -> bool:
    """Return ``True`` when ``root``'s current Merkle digest differs
    from ``previous_digest``.

    The caller owns the ``previous_digest`` store (e.g. a manifest
    file under ``006_System-Manifests/``). This helper is pure — it
    does not read or write that store.
    """
    current = calculate_directory_hash(root)
    return current.digest != previous_digest
