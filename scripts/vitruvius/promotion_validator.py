from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime
from functools import lru_cache
from pathlib import Path

import yaml

from .paths import get_repo_root


REL_ID_PATTERN = re.compile(r"^rel-[a-z][a-z0-9-]*$")
ALLOWED_TRUST = ("primary", "secondary", "tertiary", "unverified")
TRUST_RANK = {"primary": 0, "secondary": 1, "tertiary": 2, "unverified": 3}


def normalize_relationship_trust(value: object) -> str:
    """Return a relationship-schema trust level for source frontmatter values."""
    if isinstance(value, str) and value in ALLOWED_TRUST:
        return value
    return "unverified"


@dataclass
class ValidationResult:
    passed: bool
    errors: list[str] = field(default_factory=list)
    record_id: str = ""


def _parse_iso8601(value) -> bool:
    # PyYAML auto-parses ISO timestamps into datetime objects.
    if isinstance(value, datetime):
        return True
    if not isinstance(value, str) or not value:
        return False
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
        return True
    except ValueError:
        return False


def validate_promotion_record(
    record: dict,
    registry: dict,
    canonical_index: dict,
) -> ValidationResult:
    errors: list[str] = []
    record_id = record.get("id", "<missing-id>") if isinstance(record, dict) else "<missing-id>"

    # Rule 1: frontmatter present (the record dict itself counts as parsed)
    if not isinstance(record, dict):
        return ValidationResult(False, ["Record is not a parseable mapping."], record_id)

    # Rule 2: id format
    rid = record.get("id")
    if not isinstance(rid, str) or not REL_ID_PATTERN.match(rid):
        errors.append(f"Rule 2 (id format): id '{rid}' must match ^rel-[a-z][a-z0-9-]*$")

    # Rule 3: page_type
    if record.get("page_type") != "relationship":
        errors.append(f"Rule 3 (page_type): expected 'relationship', got {record.get('page_type')!r}")

    # Rule 4: predicate in registry
    predicate = record.get("relationship_type")
    predicates = registry.get("predicates", {})
    if predicate not in predicates:
        errors.append(f"Rule 4 (predicate): unknown predicate '{predicate}' - not in registry")

    # Rule 5: from/to exist
    from_entity = record.get("from_entity")
    to_entity = record.get("to_entity")
    if from_entity not in canonical_index:
        errors.append(f"Rule 5 (from_entity): '{from_entity}' not in canonical index")
    if to_entity not in canonical_index:
        errors.append(f"Rule 5 (to_entity): '{to_entity}' not in canonical index")

    # Rule 6: evidence non-empty
    evidence = record.get("evidence") or []
    if not evidence:
        errors.append("Rule 6 (evidence): array must be non-empty")

    # Rule 7: (from_type, to_type) compatibility
    if predicate in predicates and from_entity in canonical_index and to_entity in canonical_index:
        from_type = canonical_index[from_entity]["type"]
        to_type = canonical_index[to_entity]["type"]
        allowed = predicates[predicate].get("allowed_pairs", [])
        if not any(p.get("subject_type") == from_type and p.get("object_type") == to_type for p in allowed):
            errors.append(
                f"Rule 7 (compatibility): ({from_type}, {to_type}) not an allowed pair for '{predicate}'"
            )

    # Rules 8-12: evidence integrity
    for idx, ev in enumerate(evidence):
        prefix = f"Rule 8-12 (evidence[{idx}])"
        if not ev.get("source_section_id"):
            errors.append(f"{prefix}: missing source_section_id (Rule 8)")
        snippet = ev.get("evidence_snippet")
        if not isinstance(snippet, str) or not snippet.strip():
            errors.append(f"{prefix}: empty evidence_snippet (Rule 9)")
        src_id = ev.get("source_id")
        if src_id not in canonical_index:
            errors.append(f"{prefix}: source_id '{src_id}' not in canonical index (Rule 10)")
        conf = ev.get("reviewer_confidence")
        try:
            confval = float(conf)
            if confval < 0.0 or confval > 1.0:
                errors.append(f"{prefix}: reviewer_confidence {confval} outside [0, 1] (Rule 11)")
        except (TypeError, ValueError):
            errors.append(f"{prefix}: reviewer_confidence not a float (Rule 11)")
        decision = ev.get("review_decision")
        if decision != "keep":
            errors.append(f"{prefix}: review_decision '{decision}' must be 'keep' (Rule 12)")

    # Rule 13: promotion threshold
    try:
        score = float(record.get("confidence_score", 0.0))
        if score < 0.90:
            errors.append(f"Rule 13 (threshold): confidence_score {score} below 0.90")
    except (TypeError, ValueError):
        errors.append("Rule 13 (threshold): confidence_score not a float")

    # Rule 14: trust propagation
    declared_trust = record.get("trust_level")
    evidence_trusts = [canonical_index[e["source_id"]]["trust_level"]
                       for e in evidence if e.get("source_id") in canonical_index]
    evidence_trusts = [t for t in evidence_trusts if t in TRUST_RANK]
    if evidence_trusts:
        min_trust = max(evidence_trusts, key=lambda t: TRUST_RANK[t])
        if declared_trust != min_trust:
            errors.append(
                f"Rule 14 (trust): declared {declared_trust!r} must equal worst evidence trust {min_trust!r}"
            )
    if declared_trust not in ALLOWED_TRUST:
        errors.append(f"Rule 14 (trust): '{declared_trust}' not in {ALLOWED_TRUST}")

    # Rules 15-16: audit fields
    if not record.get("promotion_batch_id"):
        errors.append("Rule 15: promotion_batch_id is required")
    if not _parse_iso8601(record.get("last_promoted_utc", "")):
        errors.append("Rule 16: last_promoted_utc must be ISO-8601")

    # Rule 17: endpoint canonical_status
    if record.get("canonical_status") == "promoted":
        for endpoint_field in ("from_entity", "to_entity"):
            eid = record.get(endpoint_field)
            if eid in canonical_index:
                cs = canonical_index[eid]["canonical_status"]
                if cs in ("placeholder", "superseded"):
                    errors.append(
                        f"Rule 17: {endpoint_field} '{eid}' is in '{cs}' status; cannot promote"
                    )

    return ValidationResult(passed=not errors, errors=errors, record_id=record_id)


from typing import Any


@lru_cache(maxsize=1)
def load_registry() -> dict:
    path = get_repo_root() / "scripts" / "vitruvius" / "rules" / "relationship_registry.yaml"
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _parse_frontmatter(md_text: str) -> dict[str, Any]:
    if not md_text.startswith("---"):
        return {}
    end = md_text.find("\n---", 3)
    if end == -1:
        return {}
    raw = md_text[3:end].strip()
    try:
        return yaml.safe_load(raw) or {}
    except yaml.YAMLError:
        return {}


def build_canonical_index(repo_root: Path) -> dict[str, dict[str, Any]]:
    """Walk 003_Canonical-Knowledge-Layer/shared/{sources,concepts} and return
    an ID-keyed index for referential-integrity checks."""
    index: dict[str, dict[str, Any]] = {}

    base = Path(repo_root) / "003_Canonical-Knowledge-Layer" / "shared"
    for entity_type, subdir in (("source", "sources"), ("concept", "concepts")):
        directory = base / subdir
        if not directory.exists():
            continue
        for md_path in sorted(directory.glob("*.md")):
            fm = _parse_frontmatter(md_path.read_text(encoding="utf-8"))
            entity_id = fm.get("id")
            if not entity_id:
                continue
            index[entity_id] = {
                "type": entity_type,
                "path": md_path,
                "canonical_status": fm.get("canonical_status", "unknown"),
                "trust_level": normalize_relationship_trust(fm.get("trust_level")),
            }

    return index
