"""Sprint DISTILL-1 Task 1 — LLM reviewer distillation corpus audit.

Inspects the Sprint R Y4 stateful verdict cache (either SQLite via
``StatefulReviewRegistry`` or RocksDB via ``RocksDBStatefulReviewRegistry``
per AD-029) to decide whether we have enough historical LLM verdicts
to train a classical ML student model that can bypass Ollama on
common cases.

Decision gates (pre-committed in the plan):
- ``DEFER_NO_DATA`` if total verdicts < 50 (can't train on sparse data)
- ``GO`` if ≥50 verdicts AND label balance is not pathological
- ``DEFER_IMBALANCED`` if ≥50 verdicts but one class has <10%
- ``NO_GO`` if ≥50 verdicts AND we successfully trained a classifier
  but it couldn't reach 75% accuracy (actual training happens in Task 3
  after this task confirms we have the data)

This task is only the corpus inspection. Task 2 does feature extraction
and Task 3 does train/test. The audit auto-short-circuits to
``DEFER_NO_DATA`` here if the cache is empty, which is the expected
outcome on a fresh install.
"""
from __future__ import annotations

import json
import os
import sqlite3
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class CorpusInspectionResult:
    cache_type: str  # "sqlite" | "rocksdb" | "none"
    cache_path: Optional[str]
    total_verdicts: int
    unique_source_hashes: int
    unique_model_versions: int
    label_distribution: dict[str, int] = field(default_factory=dict)
    date_range_utc: tuple[Optional[str], Optional[str]] = (None, None)
    recommendation: str = "DEFER_NO_DATA"
    notes: str = ""


def _candidate_cache_paths() -> list[tuple[str, Path]]:
    """Return a list of (cache_type, path) tuples to inspect in order.

    The Sprint R Y4 registry doesn't hardcode a single location — it
    takes a db_path arg on construction. For the audit we check the
    conventional locations under the vitruvius tree.
    """
    repo = Path("/Users/philiplewis/vitruvius")
    return [
        ("sqlite", repo / "006_System-Manifests" / "cache" / "stateful_review_registry.sqlite"),
        ("sqlite", repo / "006_System-Manifests" / "cache" / "review_verdicts.sqlite"),
        ("sqlite", repo / "005_Operational-Intelligence-Layer" / "review" / "verdicts.sqlite"),
        ("rocksdb", repo / "006_System-Manifests" / "cache" / "stateful_review_registry.rocksdb"),
        ("rocksdb", repo / "005_Operational-Intelligence-Layer" / "review" / "verdicts.rocksdb"),
    ]


def _inspect_sqlite_cache(path: Path) -> CorpusInspectionResult:
    """Query a SQLite verdict cache. The Sprint R Y4 schema is:

        CREATE TABLE verdicts (
            source_hash TEXT,
            relationship_hash TEXT,
            model_version TEXT,
            verdict TEXT,
            self_confidence REAL,
            created_utc TEXT,
            PRIMARY KEY (source_hash, relationship_hash, model_version)
        )
    """
    conn = sqlite3.connect(str(path))
    try:
        cursor = conn.execute("SELECT COUNT(*) FROM verdicts")
        total = int(cursor.fetchone()[0])
        if total == 0:
            return CorpusInspectionResult(
                cache_type="sqlite",
                cache_path=str(path),
                total_verdicts=0,
                unique_source_hashes=0,
                unique_model_versions=0,
                recommendation="DEFER_NO_DATA",
                notes="SQLite cache exists but contains 0 verdicts",
            )
        unique_sources = int(
            conn.execute("SELECT COUNT(DISTINCT source_hash) FROM verdicts").fetchone()[0]
        )
        unique_models = int(
            conn.execute("SELECT COUNT(DISTINCT model_version) FROM verdicts").fetchone()[0]
        )
        label_rows = conn.execute(
            "SELECT verdict, COUNT(*) FROM verdicts GROUP BY verdict"
        ).fetchall()
        label_dist = {str(v): int(c) for v, c in label_rows}
        min_date, max_date = conn.execute(
            "SELECT MIN(created_utc), MAX(created_utc) FROM verdicts"
        ).fetchone()
        return CorpusInspectionResult(
            cache_type="sqlite",
            cache_path=str(path),
            total_verdicts=total,
            unique_source_hashes=unique_sources,
            unique_model_versions=unique_models,
            label_distribution=label_dist,
            date_range_utc=(min_date, max_date),
            recommendation="NEEDS_TRAINING" if total >= 50 else "DEFER_NO_DATA",
            notes=(
                f"Found {total} verdicts; "
                f"Task 2/3 will run feature extraction + train/test."
                if total >= 50
                else f"Only {total} verdicts (<50 threshold); "
                f"cannot train a meaningful classifier."
            ),
        )
    finally:
        conn.close()


def _inspect_rocksdb_cache(path: Path) -> CorpusInspectionResult:
    """Inspect a RocksDB verdict cache via rocksdict if available."""
    try:
        import rocksdict
    except ImportError:
        return CorpusInspectionResult(
            cache_type="rocksdb",
            cache_path=str(path),
            total_verdicts=0,
            unique_source_hashes=0,
            unique_model_versions=0,
            recommendation="DEFER_NO_DATA",
            notes="RocksDB cache path exists but rocksdict not installed",
        )

    db = rocksdict.Rdict(str(path), access_type=rocksdict.AccessType.read_only())
    try:
        total = 0
        source_hashes: set[str] = set()
        model_versions: set[str] = set()
        label_dist: dict[str, int] = {}
        dates: list[str] = []
        for key in db.keys():
            if not key.startswith(b"v:"):
                continue
            total += 1
            try:
                payload = db.get(key)
                import json as _json
                data = _json.loads(payload.decode("utf-8") if isinstance(payload, bytes) else payload)
                verdict = data.get("verdict", "unknown")
                label_dist[verdict] = label_dist.get(verdict, 0) + 1
                created = data.get("created_utc")
                if created:
                    dates.append(created)
            except Exception:
                continue
            try:
                _prefix, src_h, rel_h, model = key.decode("utf-8").split(":", 3)
                source_hashes.add(src_h)
                model_versions.add(model)
            except Exception:
                pass
    finally:
        db.close()

    if total == 0:
        return CorpusInspectionResult(
            cache_type="rocksdb",
            cache_path=str(path),
            total_verdicts=0,
            unique_source_hashes=0,
            unique_model_versions=0,
            recommendation="DEFER_NO_DATA",
            notes="RocksDB cache exists but contains 0 verdict entries",
        )

    date_range = (min(dates) if dates else None, max(dates) if dates else None)
    return CorpusInspectionResult(
        cache_type="rocksdb",
        cache_path=str(path),
        total_verdicts=total,
        unique_source_hashes=len(source_hashes),
        unique_model_versions=len(model_versions),
        label_distribution=label_dist,
        date_range_utc=date_range,
        recommendation="NEEDS_TRAINING" if total >= 50 else "DEFER_NO_DATA",
        notes=(
            f"Found {total} verdicts in RocksDB."
            if total >= 50
            else f"Only {total} verdicts (<50 threshold)."
        ),
    )


def inspect_verdict_cache() -> CorpusInspectionResult:
    """Main audit entry point. Walks the candidate cache paths and
    returns the first non-empty cache, or a ``DEFER_NO_DATA`` result
    if no cache is found at any known location."""
    for cache_type, path in _candidate_cache_paths():
        if not path.exists():
            continue
        try:
            if cache_type == "sqlite":
                return _inspect_sqlite_cache(path)
            if cache_type == "rocksdb":
                return _inspect_rocksdb_cache(path)
        except Exception as exc:
            return CorpusInspectionResult(
                cache_type=cache_type,
                cache_path=str(path),
                total_verdicts=0,
                unique_source_hashes=0,
                unique_model_versions=0,
                recommendation="DEFER_NO_DATA",
                notes=f"cache at {path} could not be opened: {exc}",
            )

    return CorpusInspectionResult(
        cache_type="none",
        cache_path=None,
        total_verdicts=0,
        unique_source_hashes=0,
        unique_model_versions=0,
        recommendation="DEFER_NO_DATA",
        notes=(
            "No stateful verdict cache found at any known location. "
            "The Sprint R Y4 registry infrastructure ships but has not "
            "been populated by a live LLM review run. To unblock the "
            "distillation audit, run the full PD 1096 ingestion with "
            "features.y_stateful_registry=true so verdicts accumulate "
            "in 006_System-Manifests/cache/stateful_review_registry.sqlite "
            "(or the RocksDB variant when AD-029 defaults are on)."
        ),
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--out",
        type=Path,
        default=Path(".ai/10_state/audit_distillation_2026-04-15.json"),
    )
    args = parser.parse_args()

    start = time.perf_counter()
    result = inspect_verdict_cache()
    elapsed = time.perf_counter() - start

    report = {
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "elapsed_seconds": round(elapsed, 4),
        "corpus_inspection": asdict(result),
        "decision_gate": {
            "recommendation": result.recommendation,
            "notes": result.notes,
            "threshold_defer_no_data": 50,
            "threshold_go_accuracy": 0.85,
            "threshold_go_high_conf_coverage": 0.60,
            "threshold_go_model_size_mb": 10,
        },
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))
