from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path

from .utils import utc_now_stamp


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


def _yaml_scalar(value) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    s = str(value)
    if any(c in s for c in ':#"\'\n') or s == "":
        return '"' + s.replace('"', '\\"') + '"'
    return s


def _render_frontmatter(record: dict) -> str:
    ordered_keys = [
        "id", "title", "page_type", "relationship_type",
        "from_entity", "to_entity", "trust_level", "canonical_status",
        "confidence_score", "promotion_batch_id", "promotion_audit_log_ref",
        "last_promoted_utc",
    ]
    lines = ["---"]
    for k in ordered_keys:
        if k in record:
            lines.append(f"{k}: {_yaml_scalar(record[k])}")
    lines.append("evidence:")
    for entry in record.get("evidence", []):
        lines.append("  -")
        for ek, ev in entry.items():
            lines.append(f"    {ek}: {_yaml_scalar(ev)}")
    lines.append("---")
    return "\n".join(lines)


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
