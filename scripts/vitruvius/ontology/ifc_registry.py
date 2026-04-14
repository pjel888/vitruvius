"""Stream M.1 — static concept → IfcClass + Pset registry loader."""
from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Mapping

import yaml


logger = logging.getLogger(__name__)


DEFAULT_IFC_MAPPING_PATH = Path(__file__).parent / "ifc_mapping.yaml"


@dataclass(frozen=True)
class IfcMapping:
    concept_id: str
    ifc_class: str
    psets: tuple[str, ...]
    notes: str


def load_ifc_mapping(
    path: Path = DEFAULT_IFC_MAPPING_PATH,
) -> Mapping[str, IfcMapping]:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if raw is None:
        raw = []
    if not isinstance(raw, list):
        raise ValueError(
            f"ifc_mapping.yaml root must be a list (got {type(raw).__name__})"
        )
    collected: dict[str, IfcMapping] = {}
    for idx, row in enumerate(raw):
        if not isinstance(row, dict):
            logger.warning("ifc_mapping[%d] is not a mapping; skipping", idx)
            continue
        concept_id = row.get("concept_id")
        ifc_class = row.get("ifc_class")
        psets_raw = row.get("psets", [])
        notes = row.get("notes", "")
        if not isinstance(concept_id, str) or not concept_id.startswith("concept-"):
            logger.warning(
                "ifc_mapping[%d] missing or invalid concept_id; skipping",
                idx,
            )
            continue
        if not isinstance(ifc_class, str) or not ifc_class.startswith("Ifc"):
            logger.warning(
                "ifc_mapping[%d] missing or invalid ifc_class for %s; skipping",
                idx,
                concept_id,
            )
            continue
        if not isinstance(psets_raw, (list, tuple)):
            logger.warning(
                "ifc_mapping[%d] psets must be list for %s; skipping",
                idx,
                concept_id,
            )
            continue
        psets = tuple(str(p) for p in psets_raw)
        if concept_id in collected:
            raise ValueError(f"duplicate concept_id {concept_id!r} in ifc_mapping")
        collected[concept_id] = IfcMapping(
            concept_id=concept_id,
            ifc_class=ifc_class,
            psets=psets,
            notes=str(notes) if notes is not None else "",
        )
    sorted_items = dict(sorted(collected.items(), key=lambda kv: kv[0]))
    return MappingProxyType(sorted_items)


def lookup_ifc_class(
    concept_id: str,
    *,
    mapping: Mapping[str, IfcMapping] | None = None,
) -> IfcMapping | None:
    registry = mapping if mapping is not None else load_ifc_mapping()
    return registry.get(concept_id)
