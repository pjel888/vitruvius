"""Sprint RUST-MIG-1 Task 1 — Python baseline harness for migration candidates.

Measures per-candidate wall time + peak RSS for each of the 8 GO/MAYBE
migration candidates identified in the Rust migration audit. The output
JSON at ``.ai/10_state/audit_rust_migration_baseline_2026-04-15.json``
is the gate that decides which candidates earn a Rust port in Phases A/B/C.

Design
------
Each candidate runs in its own Python subprocess under ``/usr/bin/time -l``
(macOS), using the same pattern proven in ``bench_rust_pdf_audit.py``
(AD-033 — Sprint RUST-PDF-1). Subprocess isolation is critical because:

* Peak RSS should reflect only the candidate's own memory footprint,
  not the harness driver's own import graph or the other candidates'.
* A hung candidate can be killed via ``subprocess.TimeoutExpired``
  without crashing the whole bench.

The harness is orchestration + subprocess dispatch + JSON I/O — which
sits **above the Rust Line** per AD-036 (perf-first directive). Python
is the correct tool for this layer: the hot work lives inside the child
processes where it will be measured, not in this file.

The verdict threshold is deliberately simple and baked into module
constants so the gate is auditable without re-reading the plan:

* ``wall_ms > 25`` OR ``peak_rss_mb > 10`` → ``"hot"`` (eligible for port)
* otherwise → ``"cold"`` (stay in Python — port would be a distraction)
* subprocess timeout or crash → ``"aborted"`` (investigate, do not port)

Platform note: this module hard-codes ``/usr/bin/time -l`` (macOS). The
dev machine is an 8 GB M2. On Linux the invocation would need ``-v``
and the RSS units would change (KB instead of bytes). Ship the macOS
path; document the Linux delta here.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Callable


# Verdict thresholds — record as module-level constants so the gate is
# auditable without re-reading the sprint plan. See AD-038 for the
# justification of these specific numbers (25 ms / 10 MB).
VERDICT_THRESHOLD_WALL_MS: int = 25
VERDICT_THRESHOLD_RSS_MB: int = 10

# Default per-candidate subprocess timeout. If a candidate hasn't
# finished in 30 s the verdict column is ``"aborted"`` and the record
# captures the timeout so the follow-up task can investigate.
DEFAULT_SUBPROCESS_TIMEOUT_S: float = 30.0

# Pin the Python interpreter so the bench is reproducible across
# developer machines. Matches the interpreter used by AD-033.
PYTHON_INTERPRETER = "/opt/homebrew/opt/python@3.11/bin/python3.11"

# Deterministic RNG seed — same seed = same numbers = same bench across
# runs. Use ``numpy.random.default_rng(SEED)`` in the child scripts,
# NOT the legacy ``numpy.random.seed``.
RNG_SEED: int = 42


# --------------------------------------------------------------------------- #
# Candidate spec — one entry per GO/MAYBE row from the audit                  #
# --------------------------------------------------------------------------- #


def _spec_s1_adjacency_edges(n: int) -> str:
    """Generate ``n`` synthetic spatial boxes and call
    ``build_spatial_adjacency_edges``. The function walks every pair
    (O(n^2)) so 2000 boxes exercise ~2M pair tests.
    """
    return f"""
import sys
import numpy as np
from dataclasses import dataclass

from vitruvius.spatial.spatial_edge_builder import (
    SpatialPoint,
    build_spatial_adjacency_edges,
)


@dataclass(frozen=True)
class _AABB:
    min_xyz: tuple
    max_xyz: tuple


def _main() -> None:
    rng = np.random.default_rng({RNG_SEED})
    n = {n}
    mins = rng.uniform(0.0, 100.0, size=(n, 3))
    sizes = rng.uniform(0.1, 2.0, size=(n, 3))
    maxs = mins + sizes
    points = [
        SpatialPoint(
            id=f"inst-{{i}}",
            aabb=_AABB(
                min_xyz=(float(mins[i, 0]), float(mins[i, 1]), float(mins[i, 2])),
                max_xyz=(float(maxs[i, 0]), float(maxs[i, 1]), float(maxs[i, 2])),
            ),
        )
        for i in range(n)
    ]
    edges = build_spatial_adjacency_edges(points)
    print(f"OUT_N={{len(edges)}}", file=sys.stderr)


_main()
"""


def _spec_s2_weight_by_distance(n: int) -> str:
    """Generate ``n`` synthetic seed centroids + a fixed focal point and
    call ``weight_by_distance`` once. Pure-math math.sqrt + math.exp
    per seed — the migration candidate is the inner loop.
    """
    return f"""
import sys
import numpy as np

from vitruvius.spatial.proximity_jump import weight_by_distance


def _main() -> None:
    rng = np.random.default_rng({RNG_SEED})
    n = {n}
    coords = rng.uniform(-50.0, 50.0, size=(n, 3))
    seeds = {{
        f"inst-{{i}}": (
            float(coords[i, 0]),
            float(coords[i, 1]),
            float(coords[i, 2]),
        )
        for i in range(n)
    }}
    focal = (0.0, 0.0, 0.0)
    weights = weight_by_distance(seeds, focal_xyz=focal, lambda_decay=0.05)
    print(f"OUT_N={{len(weights)}}", file=sys.stderr)


_main()
"""


def _spec_n1_wasserstein(n: int) -> str:
    """Two ``n``-element random 1-D arrays through ``wasserstein_merge_decision``.

    The module expects 2-D ``(n, d)`` arrays — reshape the 1-D floats
    to ``(n, 1)`` so the caller contract is satisfied. The hot work is
    inside ``ot.dist`` + ``ot.emd2``, which is the migration candidate.
    """
    return f"""
import sys
import numpy as np

from vitruvius.graph.wasserstein_merge import wasserstein_merge_decision


def _main() -> None:
    rng = np.random.default_rng({RNG_SEED})
    n = {n}
    a = rng.standard_normal(n).reshape(n, 1)
    b = (rng.standard_normal(n) + 0.2).reshape(n, 1)
    decision = wasserstein_merge_decision(a, b)
    print(f"OUT_N={{decision.verdict}}", file=sys.stderr)


_main()
"""


def _spec_n4_mahalanobis(n: int) -> str:
    """Fit outlier model on ``n`` 64-dim embeddings, then score each
    one via ``mahalanobis_distance``. Measures the hot scoring loop
    directly (``score_chunks`` is just the same loop wrapped around
    ``EmbeddedChunk``, which would drag in sentence-transformers).

    Perf note (review fix): the embeddings stay as a 2-D numpy array
    end-to-end. The previous version called ``.tolist()`` and then
    iterated a Python list-of-lists, which added list-materialization
    and float-boxing noise on top of the real Mahalanobis cost — the
    exact thing a Rust port would target. Keeping numpy avoids that
    measurement noise; ``fit_outlier_model`` accepts any 2-D array,
    and ``mahalanobis_distance`` accepts a numpy row vector.
    """
    return f"""
import sys
import numpy as np

from vitruvius.normalization.outlier_detector import (
    fit_outlier_model,
    mahalanobis_distance,
)


def _main() -> None:
    rng = np.random.default_rng({RNG_SEED})
    n = {n}
    dim = 64
    # Stay in numpy: no .tolist() round-trip, no list-of-lists box step.
    embeddings_np = rng.standard_normal((n, dim))
    model = fit_outlier_model(embeddings_np)
    total = 0.0
    for row in embeddings_np:
        total += mahalanobis_distance(row, model)
    print(f"OUT_N={{total:.4f}}", file=sys.stderr)


_main()
"""


def _spec_s10_bloom(n: int) -> str:
    """Add ``n`` random keys to a ``BloomFilter`` then do ``n``
    membership checks. Exercises the blake2b hash + bitset path —
    the migration candidate is the bitset layer.
    """
    return f"""
import sys
import numpy as np

from vitruvius.foraging.bloom_filter import BloomFilter


def _main() -> None:
    rng = np.random.default_rng({RNG_SEED})
    n = {n}
    # Rule-of-thumb size: 10 bits per element, 4 hashes -> FPR ~2%.
    bf = BloomFilter(size=n * 10, hash_count=4)
    keys = [f"key-{{int(x)}}" for x in rng.integers(0, 10**9, size=n)]
    for k in keys:
        bf.add(k)
    hits = 0
    for k in keys:
        if bf.contains(k):
            hits += 1
    print(f"OUT_N={{hits}}", file=sys.stderr)


_main()
"""


def _spec_g2_duplicate_detector(n: int) -> str:
    """Write ``n`` synthetic content files to a tmpdir then run
    ``find_duplicate`` against an incoming blob. The corpus walk hashes
    every file, which is the migration candidate.
    """
    return f"""
import sys
import tempfile
from pathlib import Path
import numpy as np

from vitruvius.foraging.duplicate_detector import find_duplicate


def _main() -> None:
    rng = np.random.default_rng({RNG_SEED})
    n = {n}
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        paths = []
        for i in range(n):
            payload = bytes(rng.integers(0, 256, size=256, dtype=np.uint8))
            p = root / f"doc-{{i:06d}}.bin"
            p.write_bytes(payload)
            paths.append(p)
        incoming = bytes(rng.integers(0, 256, size=256, dtype=np.uint8))
        report = find_duplicate(incoming, paths)
        print(f"OUT_N={{report.is_duplicate}}", file=sys.stderr)


_main()
"""


def _spec_p9_scanner_sha256(n: int) -> str:
    """Hash ``n`` synthetic 1 MiB files via ``_sha256_of_file``. The
    streaming reader + hashlib.sha256 update loop is the migration
    candidate.
    """
    return f"""
import sys
import tempfile
from pathlib import Path
import numpy as np

from vitruvius.scanner import _sha256_of_file


def _main() -> None:
    rng = np.random.default_rng({RNG_SEED})
    n = {n}
    size_bytes = 1 << 20
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        digests = []
        for i in range(n):
            p = root / f"file-{{i:04d}}.bin"
            # One random seed blob per file, tiled to 1 MiB, so file
            # contents differ across files but the RNG cost is O(1).
            seed_blob = bytes(rng.integers(0, 256, size=4096, dtype=np.uint8))
            reps = size_bytes // len(seed_blob)
            p.write_bytes(seed_blob * reps)
            digests.append(_sha256_of_file(p))
        print(f"OUT_N={{len(digests)}}", file=sys.stderr)


_main()
"""


def _spec_p10_merkle_fs(n: int) -> str:
    """Build a synthetic tree of ``n`` files and call
    ``calculate_directory_hash``. Exercises the recursive walk + sort +
    per-file sha256 + root-digest aggregator — the full migration
    candidate.
    """
    return f"""
import sys
import tempfile
from pathlib import Path
import numpy as np

from vitruvius.merkle_fs import calculate_directory_hash


def _main() -> None:
    rng = np.random.default_rng({RNG_SEED})
    n = {n}
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        for i in range(n):
            sub = root / f"dir-{{i // 10:03d}}"
            sub.mkdir(parents=True, exist_ok=True)
            payload = bytes(rng.integers(0, 256, size=4096, dtype=np.uint8))
            (sub / f"file-{{i:04d}}.bin").write_bytes(payload)
        result = calculate_directory_hash(root)
        print(f"OUT_N={{result.file_count}}", file=sys.stderr)


_main()
"""


#: Map from candidate id -> (default_n, script_builder).
#:
#: Default ``n`` values match the task spec so the aggregated report
#: matches the audit's blast-radius expectations. Script builders are
#: plain functions, not lambdas, so the module is introspectable.
CANDIDATE_SPECS: dict[str, tuple[int, Callable[[int], str]]] = {
    "s1_adjacency_edges": (2000, _spec_s1_adjacency_edges),
    "s2_weight_by_distance": (10000, _spec_s2_weight_by_distance),
    "n1_wasserstein": (500, _spec_n1_wasserstein),
    "n4_mahalanobis": (1000, _spec_n4_mahalanobis),
    "s10_bloom": (10000, _spec_s10_bloom),
    "g2_duplicate_detector": (1000, _spec_g2_duplicate_detector),
    "p9_scanner_sha256": (100, _spec_p9_scanner_sha256),
    "p10_merkle_fs": (100, _spec_p10_merkle_fs),
}


# --------------------------------------------------------------------------- #
# Measurement                                                                 #
# --------------------------------------------------------------------------- #


def _parse_time_output(stderr: str) -> tuple[float, float]:
    """Parse ``/usr/bin/time -l`` output into ``(wall_seconds, peak_rss_bytes)``.

    Matches the parser in ``bench_rust_pdf_audit.py`` line-for-line so
    the two benches stay consistent — if a future macOS ``time -l``
    output format change breaks one, it'll break both, and the fix
    lands in one place.
    """
    wall_seconds = 0.0
    peak_rss_bytes = 0.0
    for line in stderr.splitlines():
        stripped = line.strip()
        if " real " in line and " user " in line:
            m = re.match(r"\s*([\d.]+)\s+real", line)
            if m:
                wall_seconds = float(m.group(1))
        elif "maximum resident set size" in stripped:
            m = re.match(r"\s*(\d+)\s+maximum resident set size", line)
            if m:
                peak_rss_bytes = float(m.group(1))
    return wall_seconds, peak_rss_bytes


def classify_verdict(*, wall_ms: float | None, peak_rss_mb: float | None) -> str:
    """Return ``"hot"`` if the measurement exceeds either threshold.

    Both ``None`` → ``"aborted"`` (caller is responsible for recording
    the error detail alongside the verdict). ``"hot"`` = ``wall_ms > 25``
    OR ``peak_rss_mb > 10`` — strict greater-than so the thresholds
    themselves are ``"cold"`` (reproducible boundary).
    """
    if wall_ms is None or peak_rss_mb is None:
        return "aborted"
    if wall_ms > VERDICT_THRESHOLD_WALL_MS:
        return "hot"
    if peak_rss_mb > VERDICT_THRESHOLD_RSS_MB:
        return "hot"
    return "cold"


def _run_candidate_subprocess(
    candidate_id: str,
    *,
    n: int,
    timeout_s: float = DEFAULT_SUBPROCESS_TIMEOUT_S,
) -> dict[str, Any]:
    """Run one candidate in an isolated subprocess and capture wall+RSS.

    The returned dict has the exact shape the JSON report records:
    ``{"wall_ms", "peak_rss_mb", "n", "verdict"}`` with an optional
    ``"error"`` field when the run was aborted.
    """
    default_n, builder = CANDIDATE_SPECS[candidate_id]
    # Default n is the task spec's canonical size; callers may override
    # for a quick smoke bench, but the on-disk report always records
    # the actual n that ran.
    script = builder(n)

    # Pass the repo's scripts/ path on PYTHONPATH so the child can
    # ``from vitruvius.spatial... import ...`` without installing.
    repo_root = Path(__file__).resolve().parents[3]
    scripts_dir = repo_root / "scripts"
    env = os.environ.copy()
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = (
        f"{scripts_dir}{os.pathsep}{existing}" if existing else str(scripts_dir)
    )

    try:
        completed = subprocess.run(
            ["/usr/bin/time", "-l", PYTHON_INTERPRETER, "-c", script],
            capture_output=True,
            timeout=timeout_s,
            check=False,
            env=env,
        )
    except subprocess.TimeoutExpired:
        return {
            "wall_ms": None,
            "peak_rss_mb": None,
            "n": n,
            "verdict": "aborted",
            "error": f"subprocess timed out after {timeout_s}s",
        }
    except FileNotFoundError as exc:
        return {
            "wall_ms": None,
            "peak_rss_mb": None,
            "n": n,
            "verdict": "aborted",
            "error": f"could not spawn subprocess: {exc}",
        }

    stderr = (completed.stderr or b"").decode("utf-8", errors="replace")

    if completed.returncode != 0:
        return {
            "wall_ms": None,
            "peak_rss_mb": None,
            "n": n,
            "verdict": "aborted",
            "error": (
                f"candidate subprocess exited {completed.returncode}. "
                f"stderr_tail={stderr[-500:]}"
            ),
        }

    wall_seconds, peak_rss_bytes = _parse_time_output(stderr)
    wall_ms = round(wall_seconds * 1000.0, 3)
    peak_rss_mb = round(peak_rss_bytes / (1024.0 * 1024.0), 3)
    verdict = classify_verdict(wall_ms=wall_ms, peak_rss_mb=peak_rss_mb)

    return {
        "wall_ms": wall_ms,
        "peak_rss_mb": peak_rss_mb,
        "n": n,
        "verdict": verdict,
    }


# --------------------------------------------------------------------------- #
# Orchestration                                                               #
# --------------------------------------------------------------------------- #


def run_baseline(
    out_path: Path,
    *,
    timeout_s: float = DEFAULT_SUBPROCESS_TIMEOUT_S,
    overrides: dict[str, int] | None = None,
) -> dict[str, Any]:
    """Run every migration candidate, write the JSON report, return it.

    Parameters
    ----------
    out_path:
        Where to write the aggregated report. Parent directories are
        created if missing.
    timeout_s:
        Per-candidate subprocess timeout. A candidate that hasn't
        finished in ``timeout_s`` seconds is recorded as ``"aborted"``.
    overrides:
        Optional ``{candidate_id: n}`` map. Useful for smoke runs
        ("run the bench with n=10 everywhere") — production runs should
        pass ``None`` so every candidate uses its spec-defined ``n``.
    """
    # Pre-flight: fail loudly if the pinned interpreter is missing.
    # Without this guard every candidate would hit ``FileNotFoundError``
    # inside ``subprocess.run`` and silently record ``"aborted"``,
    # producing a report that looks like a timeout sweep rather than a
    # configuration error. Fail fast instead.
    interpreter = Path(PYTHON_INTERPRETER)
    if not interpreter.exists():
        raise RuntimeError(
            f"PYTHON_INTERPRETER not found at {PYTHON_INTERPRETER}. "
            f"Set PYTHON_INTERPRETER to a valid Python 3.11 executable or install "
            f"python3.11 at the expected path. The subprocess harness cannot run "
            f"without a real interpreter path."
        )

    candidates: dict[str, dict[str, Any]] = {}
    for cid, (default_n, _builder) in CANDIDATE_SPECS.items():
        n = (overrides or {}).get(cid, default_n)
        result = _run_candidate_subprocess(cid, n=n, timeout_s=timeout_s)
        candidates[cid] = result
        status = result.get("verdict", "?")
        wall_ms = result.get("wall_ms")
        rss_mb = result.get("peak_rss_mb")
        print(
            f"[{cid}] n={n} wall={wall_ms} ms, "
            f"rss={rss_mb} MB → {status}",
            flush=True,
        )

    report: dict[str, Any] = {
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "python_interpreter": PYTHON_INTERPRETER,
        "host": "darwin-arm64 / 8 GB M2",
        "threshold_wall_ms": VERDICT_THRESHOLD_WALL_MS,
        "threshold_peak_rss_mb": VERDICT_THRESHOLD_RSS_MB,
        "rng_seed": RNG_SEED,
        "candidates": candidates,
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2) + "\n")
    return report


def _main() -> int:
    parser = argparse.ArgumentParser(
        description="Sprint RUST-MIG-1 Task 1 — Python baseline harness",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path(".ai/10_state/audit_rust_migration_baseline_2026-04-15.json"),
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_SUBPROCESS_TIMEOUT_S,
        help="Per-candidate subprocess timeout in seconds.",
    )
    args = parser.parse_args()

    report = run_baseline(args.out, timeout_s=args.timeout)

    print()
    print("Verdict summary:")
    for cid, entry in report["candidates"].items():
        print(f"  {cid:30s} {entry['verdict']}")
    print(f"\nFull report: {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(_main())
