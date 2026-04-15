"""Sprint AUDIT-1 Task 5B — integrity-verified reader for spatial contract files.

Closes the MEDIUM admission-gate gap surfaced by the Sprint AUDIT-1 Task 2
integrity audit: the TypeScript spatial-daemon writes canonical JSON that
Python consumers previously read without any integrity check. A silent
truncation or corruption would propagate wrong spatial results downstream.

The spatial-daemon `contract_writer.ts` now appends a SHA-256 footer of
the form::

    <pretty-printed JSON body>\\n
    # sha256: <64 hex digest>\\n

This module parses such files, verifies the footer matches the body
hash, and raises :class:`IntegrityError` on mismatch.

Backward compatibility: files without a footer (legacy contract files
from before Task 5B) remain parseable via ``parse_contract(...,
require_footer=False)``. The default is ``require_footer=False`` so
this module can be dropped into existing call sites (walker.py) without
breaking the many already-on-disk fixtures that lack footers. Call
sites that want a hard guarantee can pass ``require_footer=True``.

Perf call: SHA-256 via Python's hashlib (stdlib, hardware-accelerated on
Apple Silicon via ARMv8 crypto extensions). Benchmarked 1.5-2.5x faster
than BLAKE3 in :mod:`vitruvius.bench.bench_integrity_audit` so we stay
with the stdlib path. This sits squarely ABOVE the Rust Line — hashing a
~1-10 KB spatial contract on read is cheap enough that porting is
pointless, and hashlib is already native C.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

INTEGRITY_FOOTER_PREFIX = "# sha256: "


class IntegrityError(ValueError):
    """Raised when a spatial contract file fails its integrity check."""


@dataclass(frozen=True)
class ContractParseResult:
    """Structured result of parsing a contract file."""

    payload: dict[str, Any]
    """The decoded JSON body."""

    body: str
    """The raw JSON body (everything before the footer, including trailing newline)."""

    digest_expected: str | None
    """The footer's digest, or None if the file had no footer."""

    digest_actual: str
    """The SHA-256 hex digest of ``body`` as computed at parse time."""

    has_footer: bool
    """True if the file carried a ``# sha256:`` footer."""


def compute_body_sha256(body: str) -> str:
    """Compute the SHA-256 hex digest of a contract body.

    The body is the exact pretty-printed JSON bytes (including the
    trailing newline) as written to disk by ``contract_writer.ts``.
    """
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def split_body_and_footer(raw: str) -> tuple[str, str | None]:
    """Split raw file contents into (body, digest-or-None).

    If the file carries an integrity footer, returns the body (ending
    in a newline) and the hex digest. Otherwise returns the raw content
    unchanged and ``None``.
    """
    marker = "\n" + INTEGRITY_FOOTER_PREFIX
    footer_idx = raw.rfind(marker)
    if footer_idx < 0:
        return raw, None
    body = raw[: footer_idx + 1]  # keep the trailing newline
    footer_line = raw[footer_idx + 1 :].rstrip("\n")
    if not footer_line.startswith(INTEGRITY_FOOTER_PREFIX):
        return raw, None
    digest = footer_line[len(INTEGRITY_FOOTER_PREFIX) :].strip()
    if len(digest) != 64:
        return raw, None
    return body, digest


def parse_contract(path: Path | str, *, require_footer: bool = False) -> ContractParseResult:
    """Parse and verify a spatial contract file.

    Args:
        path: path to a contract JSON file written by the spatial-daemon.
        require_footer: if True, raises :class:`IntegrityError` when the
            file lacks a footer. Default False for backward compatibility.

    Raises:
        IntegrityError: if ``require_footer`` and the footer is missing,
            or if the footer digest does not match the body's SHA-256.
        json.JSONDecodeError: if the body is not valid JSON.
    """
    p = Path(path)
    raw = p.read_text(encoding="utf-8")
    body, expected = split_body_and_footer(raw)
    actual = compute_body_sha256(body)

    if expected is None:
        if require_footer:
            raise IntegrityError(
                f"spatial contract {p} has no integrity footer (expected '# sha256: ...')"
            )
        payload = json.loads(body)
        return ContractParseResult(
            payload=payload,
            body=body,
            digest_expected=None,
            digest_actual=actual,
            has_footer=False,
        )

    if expected != actual:
        raise IntegrityError(
            f"spatial contract {p} integrity failure: "
            f"footer digest {expected} does not match recomputed body digest {actual}"
        )

    payload = json.loads(body)
    return ContractParseResult(
        payload=payload,
        body=body,
        digest_expected=expected,
        digest_actual=actual,
        has_footer=True,
    )
