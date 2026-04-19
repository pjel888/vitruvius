"""CanonicalStore — file-native JSONL persistence for Phase 3 output.

Stores canonical nodes, placement assertions, and merge assertions in
a single JSONL file with a deterministic SHA-256 checksum sidecar.

Usage::

    from vitruvius.kg.canonical_store import CanonicalStore
    store = CanonicalStore(base_dir=Path("006_System-Manifests/runs/kg_canonical"))
    path = store.save(nodes, placements, merges, run_id="run-001")
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .schemas import CanonicalNode, MergeAssertion, PlacementAssertion


class CanonicalStore:
    """Write and read canonicalization artifacts as JSONL."""

    DEFAULT_BASE_DIR = Path("006_System-Manifests/runs/kg_canonical")

    def __init__(self, base_dir: Path | None = None) -> None:
        self.base_dir = Path(base_dir) if base_dir else self.DEFAULT_BASE_DIR
        self.base_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # Write
    # ------------------------------------------------------------------

    def save(
        self,
        nodes: list[CanonicalNode],
        placements: list[PlacementAssertion],
        merges: list[MergeAssertion],
        run_id: str | None = None,
    ) -> Path:
        """Write canonicalization artifacts to JSONL and return the path."""
        if run_id is None:
            run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

        path = self.base_dir / f"{run_id}_kg_canonical.jsonl"

        with path.open("w", encoding="utf-8") as fh:
            # Header record
            fh.write(
                json.dumps(
                    {"_meta": True, "run_id": run_id, "version": "3.0.0", "record_types": ["node", "placement", "merge"]},
                    ensure_ascii=False,
                    sort_keys=True,
                )
                + "\n"
            )
            for node in nodes:
                fh.write(
                    json.dumps(
                        {"type": "node", "data": node.model_dump(mode="json")},
                        ensure_ascii=False,
                        sort_keys=True,
                    )
                    + "\n"
                )
            for placement in placements:
                fh.write(
                    json.dumps(
                        {"type": "placement", "data": placement.model_dump(mode="json")},
                        ensure_ascii=False,
                        sort_keys=True,
                    )
                    + "\n"
                )
            for merge in merges:
                fh.write(
                    json.dumps(
                        {"type": "merge", "data": merge.model_dump(mode="json")},
                        ensure_ascii=False,
                        sort_keys=True,
                    )
                    + "\n"
                )

        # Sidecar checksum
        checksum = self.checksum(path)
        (path.parent / f"{path.name}.sha256").write_text(checksum, encoding="utf-8")
        return path

    # ------------------------------------------------------------------
    # Read
    # ------------------------------------------------------------------

    def load(
        self, path: Path
    ) -> tuple[list[CanonicalNode], list[PlacementAssertion], list[MergeAssertion]]:
        """Round-trip load from JSONL."""
        nodes: list[CanonicalNode] = []
        placements: list[PlacementAssertion] = []
        merges: list[MergeAssertion] = []

        with path.open("r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                record = json.loads(line)
                if record.get("_meta"):
                    continue
                rec_type = record.get("type")
                data = record.get("data", {})
                if rec_type == "node":
                    nodes.append(CanonicalNode.model_validate(data))
                elif rec_type == "placement":
                    placements.append(PlacementAssertion.model_validate(data))
                elif rec_type == "merge":
                    merges.append(MergeAssertion.model_validate(data))

        return nodes, placements, merges

    # ------------------------------------------------------------------
    # Checksum
    # ------------------------------------------------------------------

    @staticmethod
    def checksum(path: Path) -> str:
        """Return SHA-256 hex digest of *path* contents."""
        h = hashlib.sha256()
        with path.open("rb") as fh:
            for chunk in iter(lambda: fh.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()
