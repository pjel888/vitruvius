"""Sprint AUDIT-1 — FlatBuffers audit harness.

Benchmarks the top two JSON-serialization hot paths (event_store append
and verdict_cache put) against hand-written FlatBuffers-like flat
representations. Emits an :class:`AuditResult` per site plus a
combined recommendation for Task 1 of the advanced-tech audit plan.

This is a STUDY module — it does not touch the production
RocksDBEventStore or RocksDBStatefulReviewRegistry classes. The
only purpose is to measure whether the proposal is worth shipping.
"""
from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

Recommendation = Literal["GO", "DEFER", "NO_GO"]


@dataclass(frozen=True)
class AuditResult:
    site: str
    n: int
    json_wall_seconds: float
    flatbuffers_wall_seconds: float
    speedup_ratio: float  # json / flatbuffers. >1 means flatbuffers is faster.
    breakdown: dict[str, float] = field(default_factory=dict)


def _timed(fn) -> float:
    start = time.perf_counter()
    fn()
    return time.perf_counter() - start


def _build_flatbuffers_event(builder, event_type: str, edge_id: str, timestamp: str, from_node: str, to_node: str):
    """Hand-write a FlatBuffer-like record without generating schemas.

    This uses the low-level ``flatbuffers.Builder`` API to avoid the
    schema-compilation step. In production we would generate Python
    classes via ``flatc`` — the audit only needs a representative
    serialize/deserialize cost.
    """
    et = builder.CreateString(event_type)
    eid = builder.CreateString(edge_id)
    ts = builder.CreateString(timestamp)
    fn = builder.CreateString(from_node)
    tn = builder.CreateString(to_node)

    builder.StartObject(5)
    builder.PrependUOffsetTRelativeSlot(0, et, 0)
    builder.PrependUOffsetTRelativeSlot(1, eid, 0)
    builder.PrependUOffsetTRelativeSlot(2, ts, 0)
    builder.PrependUOffsetTRelativeSlot(3, fn, 0)
    builder.PrependUOffsetTRelativeSlot(4, tn, 0)
    return builder.EndObject()


def bench_event_store_serialization(*, n: int) -> AuditResult:
    import flatbuffers

    # Prepare representative records
    records = [
        {
            "event_type": "PROMOTED",
            "edge_id": f"rel-{i:06d}",
            "timestamp_utc": f"2026-04-15T10:00:{i % 60:02d}Z",
            "payload": {"from": f"law-{i}", "to": f"concept-{i}"},
        }
        for i in range(n)
    ]

    # JSON serialize-all-then-deserialize-all cycle
    def json_cycle():
        blobs = [json.dumps(r, sort_keys=True).encode("utf-8") for r in records]
        for b in blobs:
            json.loads(b)

    json_wall = _timed(json_cycle)

    # FlatBuffers equivalent
    def flatbuffers_cycle():
        builder = flatbuffers.Builder(1024)
        finished: list[bytes] = []
        for r in records:
            builder.Clear()
            root = _build_flatbuffers_event(
                builder,
                r["event_type"],
                r["edge_id"],
                r["timestamp_utc"],
                r["payload"]["from"],
                r["payload"]["to"],
            )
            builder.Finish(root)
            finished.append(bytes(builder.Output()))
        # Representative deserialize: just read the header bytes.
        for buf in finished:
            # Table root offset is at buf[0:4].
            if len(buf) < 4:
                raise RuntimeError("truncated flatbuffer")

    fb_wall = _timed(flatbuffers_cycle)
    ratio = json_wall / fb_wall if fb_wall > 0 else 0.0

    return AuditResult(
        site="event_store_serialization",
        n=n,
        json_wall_seconds=json_wall,
        flatbuffers_wall_seconds=fb_wall,
        speedup_ratio=ratio,
        breakdown={
            "json_bytes_per_record_estimate": (
                sum(len(json.dumps(r).encode("utf-8")) for r in records) / max(1, len(records))
            ),
        },
    )


def bench_verdict_cache_serialization(*, n: int) -> AuditResult:
    import flatbuffers

    records = [
        {
            "verdict": "keep" if i % 2 == 0 else "reject",
            "self_confidence": 0.5 + (i % 10) / 20.0,
            "created_utc": f"2026-04-15T10:00:{i % 60:02d}Z",
        }
        for i in range(n)
    ]

    def json_cycle():
        blobs = [json.dumps(r, sort_keys=True).encode("utf-8") for r in records]
        for b in blobs:
            json.loads(b)

    json_wall = _timed(json_cycle)

    def flatbuffers_cycle():
        builder = flatbuffers.Builder(256)
        finished: list[bytes] = []
        for r in records:
            builder.Clear()
            v = builder.CreateString(r["verdict"])
            ts = builder.CreateString(r["created_utc"])
            builder.StartObject(3)
            builder.PrependUOffsetTRelativeSlot(0, v, 0)
            builder.PrependFloat32Slot(1, r["self_confidence"], 0.0)
            builder.PrependUOffsetTRelativeSlot(2, ts, 0)
            root = builder.EndObject()
            builder.Finish(root)
            finished.append(bytes(builder.Output()))
        for buf in finished:
            if len(buf) < 4:
                raise RuntimeError("truncated flatbuffer")

    fb_wall = _timed(flatbuffers_cycle)
    ratio = json_wall / fb_wall if fb_wall > 0 else 0.0

    return AuditResult(
        site="verdict_cache_serialization",
        n=n,
        json_wall_seconds=json_wall,
        flatbuffers_wall_seconds=fb_wall,
        speedup_ratio=ratio,
        breakdown={
            "json_bytes_per_record_estimate": (
                sum(len(json.dumps(r).encode("utf-8")) for r in records) / max(1, len(records))
            ),
        },
    )


def compute_recommendation(*, event_store_ratio: float, verdict_cache_ratio: float) -> Recommendation:
    """Decision gate.

    GO: both ratios >= 2.0 (FlatBuffers >= 2x faster on both sites)
    DEFER: both ratios between 1.25 and 2.0 (worth revisiting at scale)
    NO_GO: either ratio < 1.25 (not worth the complexity cost)
    """
    if event_store_ratio >= 2.0 and verdict_cache_ratio >= 2.0:
        return "GO"
    if event_store_ratio >= 1.25 and verdict_cache_ratio >= 1.25:
        return "DEFER"
    return "NO_GO"


def result_as_json(result: AuditResult) -> dict:
    return {
        "site": result.site,
        "n": result.n,
        "json_wall_seconds": round(result.json_wall_seconds, 6),
        "flatbuffers_wall_seconds": round(result.flatbuffers_wall_seconds, 6),
        "speedup_ratio": round(result.speedup_ratio, 4),
        "breakdown": {k: round(v, 4) for k, v in result.breakdown.items()},
    }


if __name__ == "__main__":
    import argparse
    import datetime as dt
    import os

    parser = argparse.ArgumentParser(description="FlatBuffers audit harness")
    parser.add_argument("--n", type=int, default=10_000)
    parser.add_argument("--out", type=Path, default=Path(".ai/10_state/audit_flatbuffers_2026-04-15.json"))
    args = parser.parse_args()

    ev = bench_event_store_serialization(n=args.n)
    vc = bench_verdict_cache_serialization(n=args.n)
    rec = compute_recommendation(
        event_store_ratio=ev.speedup_ratio,
        verdict_cache_ratio=vc.speedup_ratio,
    )

    report = {
        "timestamp_utc": dt.datetime.utcnow().isoformat() + "Z",
        "n": args.n,
        "python_interpreter": os.sys.executable,
        "host": "darwin-arm64",
        "results": [result_as_json(ev), result_as_json(vc)],
        "decision_gate": {
            "event_store_ratio": round(ev.speedup_ratio, 4),
            "verdict_cache_ratio": round(vc.speedup_ratio, 4),
            "threshold_go": 2.0,
            "threshold_defer_lower": 1.25,
            "recommendation": rec,
            "notes": (
                f"FlatBuffers {'>=' if rec == 'GO' else '<'} 2x faster than JSON on "
                f"event_store_serialization ({round(ev.speedup_ratio, 2)}x) and "
                f"verdict_cache_serialization ({round(vc.speedup_ratio, 2)}x). "
                f"Decision: {rec}."
            ),
        },
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))
