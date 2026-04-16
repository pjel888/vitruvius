from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from ..promotion_validator import (
    build_canonical_index,
    load_registry,
    validate_promotion_record,
)
from ..utils import utc_now_stamp


@dataclass
class AuditEntry:
    batch_id: str
    record_id: str
    action: str  # "created" | "merged" | "rejected" | "rolled_back"
    path: str
    detail: str


def append_audit_entry(log_path: Path, entry: AuditEntry) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    stamp = utc_now_stamp()
    line = (
        f"{stamp}\t{entry.batch_id}\t{entry.action}\t{entry.record_id}\t"
        f"{entry.path}\t{entry.detail}\n"
    )
    with log_path.open("a", encoding="utf-8") as f:
        f.write(line)


_SLUG_NON_ALNUM = re.compile(r"[^a-z0-9]+")


def slugify(value: str) -> str:
    value = value.lower()
    value = _SLUG_NON_ALNUM.sub("-", value)
    value = re.sub(r"-+", "-", value)
    return value.strip("-")


def short_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:8]


def build_relationship_id(from_entity: str, predicate: str, to_entity: str) -> str:
    slug = slugify(f"{from_entity}-{predicate}-{to_entity}")
    return f"rel-{slug}"


def build_promotion_batch_id() -> str:
    stamp = utc_now_stamp()
    return f"{stamp}_{short_hash(stamp)}"


def evidence_fingerprint(evidence_entry: dict) -> str:
    key = "|".join([
        str(evidence_entry.get("source_id", "")),
        str(evidence_entry.get("source_section_id", "")),
        short_hash(str(evidence_entry.get("evidence_snippet", ""))),
    ])
    return key


def merge_evidence(existing: list[dict], new: list[dict]) -> list[dict]:
    seen = {evidence_fingerprint(e): e for e in existing}
    for entry in new:
        fp = evidence_fingerprint(entry)
        if fp not in seen:
            seen[fp] = entry
    return list(seen.values())


def min_confidence(evidence: list[dict]) -> float:
    scores = [float(e.get("reviewer_confidence", 0.0)) for e in evidence]
    return min(scores) if scores else 0.0


def _render_frontmatter(record: dict) -> str:
    """Render the record as YAML frontmatter with stable key ordering.

    Uses yaml.safe_dump rather than a hand-rolled emitter so the output is
    strict-round-trip-safe: load→render→load yields identical strings.
    """
    ordered_keys = [
        "id", "title", "page_type", "relationship_type",
        "from_entity", "to_entity", "trust_level", "canonical_status",
        "confidence_score", "promotion_batch_id", "promotion_audit_log_ref",
        "last_promoted_utc",
    ]
    ordered: dict = {}
    for k in ordered_keys:
        if k in record:
            ordered[k] = record[k]
    ordered["evidence"] = record.get("evidence", [])

    body = yaml.safe_dump(
        ordered,
        sort_keys=False,
        default_flow_style=False,
        allow_unicode=True,
        width=1000000,  # no line wrapping — keep snippets on one logical line
    )
    return "---\n" + body.rstrip() + "\n---"


def _render_body(record: dict) -> str:
    lines = []
    lines.append(f"# {record.get('title', record.get('id', ''))}")
    lines.append("")
    lines.append("## Relationship Summary")
    lines.append("")
    lines.append(f"Promoted relationship of type `{record.get('relationship_type')}` "
                 f"from `{record.get('from_entity')}` to `{record.get('to_entity')}`.")
    lines.append("")
    lines.append("## Evidence")
    lines.append("")
    for idx, ev in enumerate(record.get("evidence", []), 1):
        lines.append(f"### Evidence {idx} - `{ev.get('source_id')}` §{ev.get('source_section_id')}")
        lines.append("")
        snippet = ev.get("evidence_snippet", "")
        lines.append(f"> {snippet}")
        lines.append("")
        lines.append(
            f"- Reviewer: `{ev.get('reviewer_model')}` · "
            f"Decision: `{ev.get('review_decision')}` · "
            f"Confidence: `{ev.get('reviewer_confidence')}`"
        )
        if ev.get("reviewed_at_utc"):
            lines.append(f"- Reviewed: {ev['reviewed_at_utc']}")
        lines.append(f"- Batch: `{record.get('promotion_batch_id')}`")
        lines.append("")
    return "\n".join(lines)


def write_relationship_file(path: Path, record: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    content = _render_frontmatter(record) + "\n\n" + _render_body(record) + "\n"
    path.write_text(content, encoding="utf-8")


def _load_high_confidence(repo_root: Path, input_path: Path | None = None) -> list[dict]:
    path = input_path or (
        repo_root / "006_System-Manifests" / "runs" / "latest_relationship_review_high_confidence.json"
    )
    if not path.is_absolute():
        path = repo_root / path
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload.get("candidates", [])


def _candidate_to_record(
    candidate_envelope: dict,
    *,
    canonical_index: dict,
    batch_id: str,
    audit_log_ref: str,
) -> dict | None:
    candidate = candidate_envelope["candidate"]
    review = candidate_envelope["review"]

    from_entity = candidate["from"]
    to_entity = candidate["to"]
    predicate = candidate["type"]
    rel_id = build_relationship_id(from_entity, predicate, to_entity)

    # Pull the first section and first example as the initial evidence entry.
    section_id = (candidate.get("sections") or [None])[0]
    snippet = (candidate.get("examples") or [""])[0]

    # The evidence source_id must match an entity in the canonical index.
    # Prefer the from_entity if it is a source; otherwise use it anyway (Rule 10
    # will fail loudly if the ID is bad).
    evidence_source = from_entity
    trust_level = canonical_index.get(evidence_source, {}).get("trust_level")

    evidence_entry = {
        "source_id": evidence_source,
        "source_section_id": section_id,
        "evidence_snippet": snippet,
        "review_decision": review["decision"],
        "reviewer_model": "gemma4:31b",
        "reviewer_confidence": float(review["confidence"]),
        "reviewer_reason": review.get("reason", ""),
        "extracted_at_utc": utc_now_stamp(),
        "reviewed_at_utc": utc_now_stamp(),
    }

    record = {
        "id": rel_id,
        "title": f"{from_entity} {predicate} {to_entity}",
        "page_type": "relationship",
        "relationship_type": predicate,
        "from_entity": from_entity,
        "to_entity": to_entity,
        "trust_level": trust_level or "unverified",
        "canonical_status": "promoted",
        "confidence_score": float(review["confidence"]),
        "promotion_batch_id": batch_id,
        "promotion_audit_log_ref": audit_log_ref,
        "last_promoted_utc": utc_now_stamp(),
        "evidence": [evidence_entry],
    }
    return record


def _load_existing_record(path: Path) -> dict | None:
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    return yaml.safe_load(text[3:end].strip()) or None


def run_promote_inner(
    *,
    repo_root: Path,
    execute: bool,
    rollback_batch_id: str | None,
    high_confidence_input_path: Path | None = None,
    relationships_output_dir: Path | None = None,
    audit_log_path: Path | None = None,
) -> dict:
    if rollback_batch_id is not None:
        return _run_rollback(repo_root, rollback_batch_id)

    canonical_index = build_canonical_index(repo_root)
    registry = load_registry()

    rels_dir = relationships_output_dir or (
        repo_root / "003_Canonical-Knowledge-Layer" / "shared" / "relationships"
    )
    if not rels_dir.is_absolute():
        rels_dir = repo_root / rels_dir
    runs_dir = repo_root / "006_System-Manifests" / "runs"
    audit_log = audit_log_path or (runs_dir / "latest_promotion_audit.log")
    if not audit_log.is_absolute():
        audit_log = repo_root / audit_log

    candidates = _load_high_confidence(repo_root, high_confidence_input_path)
    batch_id = build_promotion_batch_id()

    result: dict[str, Any] = {
        "batch_id": batch_id,
        "total_candidates": len(candidates),
        "created": 0, "merged": 0, "skipped": 0, "rejected": 0,
        "would_create": 0, "would_merge": 0, "would_skip": 0, "would_reject": 0,
        "errors": [],
    }

    for envelope in candidates:
        record = _candidate_to_record(
            envelope,
            canonical_index=canonical_index,
            batch_id=batch_id,
            audit_log_ref=str(audit_log.relative_to(repo_root)),
        )
        if record is None:
            result["rejected"] += 1
            continue

        target_path = rels_dir / f"{record['id']}.md"
        existing = _load_existing_record(target_path)
        is_merge = existing is not None
        is_noop = False

        if is_merge:
            existing_evidence = existing.get("evidence", []) or []
            merged = merge_evidence(existing_evidence, record["evidence"])
            if len(merged) == len(existing_evidence):
                # No new fingerprints — the candidate adds nothing.
                is_noop = True
                record = existing
            else:
                existing["evidence"] = merged
                existing["confidence_score"] = min_confidence(merged)
                existing["promotion_batch_id"] = batch_id
                existing["last_promoted_utc"] = utc_now_stamp()
                existing["promotion_audit_log_ref"] = str(audit_log.relative_to(repo_root))
                record = existing

        if is_noop:
            if execute:
                result["skipped"] += 1
            else:
                result["would_skip"] += 1
            continue

        validation = validate_promotion_record(record, registry, canonical_index)
        if not validation.passed:
            if execute:
                result["rejected"] += 1
            else:
                result["would_reject"] += 1
            result["errors"].append({"record_id": record["id"], "errors": validation.errors})
            if execute:
                append_audit_entry(audit_log, AuditEntry(
                    batch_id=batch_id,
                    record_id=record["id"],
                    action="rejected",
                    path=str(target_path),
                    detail="; ".join(validation.errors),
                ))
            continue

        if not execute:
            if is_merge:
                result["would_merge"] += 1
            else:
                result["would_create"] += 1
            continue

        write_relationship_file(target_path, record)
        action = "merged" if is_merge else "created"
        result[action] += 1
        append_audit_entry(audit_log, AuditEntry(
            batch_id=batch_id,
            record_id=record["id"],
            action=action,
            path=str(target_path),
            detail=f"evidence_count={len(record['evidence'])}",
        ))

    return result


def _run_rollback(repo_root: Path, batch_id: str) -> dict:
    runs_dir = repo_root / "006_System-Manifests" / "runs"
    audit_log = runs_dir / "latest_promotion_audit.log"
    if not audit_log.exists():
        return {"rolled_back": 0, "errors": ["no audit log found"]}

    rolled_back = 0

    for line in audit_log.read_text(encoding="utf-8").splitlines():
        parts = line.split("\t")
        if len(parts) < 5:
            continue
        _stamp, bid, action, rid, path_str = parts[:5]
        if bid != batch_id or action != "created":
            continue
        target = Path(path_str)
        if not target.is_absolute():
            target = repo_root / target
        if target.exists():
            target.unlink()
            rolled_back += 1
            append_audit_entry(audit_log, AuditEntry(
                batch_id=batch_id,
                record_id=rid,
                action="rolled_back",
                path=str(target),
                detail="reversal",
            ))

    return {"rolled_back": rolled_back, "batch_id": batch_id}


def _concept_stringency_vector(concept_id: str) -> str:
    """Stream W3.3 — read the ``stringency_vector`` field from a concept
    file's frontmatter. Returns ``"qualitative"`` (the safe default)
    whenever the file is missing, unparseable, or the field is absent.
    """
    from ..paths import get_repo_root
    slug = concept_id.removeprefix("concept-")
    path = (
        get_repo_root()
        / "003_Canonical-Knowledge-Layer"
        / "shared"
        / "concepts"
        / f"{slug}.md"
    )
    if not path.exists():
        return "qualitative"
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return "qualitative"
    end = text.find("\n---", 3)
    if end == -1:
        return "qualitative"
    try:
        fm = yaml.safe_load(text[3:end].strip())
    except yaml.YAMLError:
        return "qualitative"
    if isinstance(fm, dict):
        vector = fm.get("stringency_vector", "qualitative")
        if vector in {"maximize", "minimize", "qualitative"}:
            return vector
    return "qualitative"


def _maybe_resolve_stringency_conflict(
    edge_a: Any,
    edge_b: Any,
) -> dict[str, object] | None:
    """Stream W3.3 — consult ``resolve_stringency`` when two promoted edges
    target the same concept and the feature flag is on.

    Returns:
      - ``None`` when ``features.w_promotion_stringency_gate`` is false
      - ``None`` when the resolver returns ``unresolved`` (e.g. both
        numeric_values are None under a qualitative vector) — the
        caller keeps both edges without a governing tag
      - A dict with ``winner_edge_id`` / ``loser_edge_id`` /
        ``is_governing_standard=True`` / ``reason`` when the resolver
        picks a winner
    """
    from ..config import _features_block
    from .stringency_resolver import resolve_stringency
    if not _features_block().get("w_promotion_stringency_gate", False):
        return None
    vector = _concept_stringency_vector(edge_a.to_entity)
    try:
        verdict = resolve_stringency(edge_a, edge_b, stringency_vector=vector)
    except ValueError:
        return None
    if verdict.unresolved or verdict.winner_edge_id is None:
        return None
    return {
        "winner_edge_id": verdict.winner_edge_id,
        "loser_edge_id": verdict.loser_edge_id,
        "is_governing_standard": True,
        "reason": verdict.reason,
    }


def run_promote(
    *,
    execute: bool = False,
    rollback_batch_id: str | None = None,
    high_confidence_input_path: Path | None = None,
    relationships_output_dir: Path | None = None,
    audit_log_path: Path | None = None,
) -> int:
    # Resolve via the shared helper so the repo root stays correct after
    # promotion became a subpackage — the previous hardcoded
    # `parent.parent.parent` walk only worked when promotion was a flat
    # module (one level shallower).
    from ..paths import get_repo_root

    repo_root = get_repo_root()
    result = run_promote_inner(
        repo_root=repo_root,
        execute=execute,
        rollback_batch_id=rollback_batch_id,
        high_confidence_input_path=high_confidence_input_path,
        relationships_output_dir=relationships_output_dir,
        audit_log_path=audit_log_path,
    )
    print(json.dumps(result, indent=2, default=str))
    return 0
