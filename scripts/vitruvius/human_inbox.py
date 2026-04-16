from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

Decision = Literal["approve", "reject", "defer"]
_ALLOWED_DECISIONS = {"approve", "reject", "defer"}


class HumanInboxParseError(ValueError):
    pass


@dataclass(frozen=True)
class HumanInboxItem:
    item_id: str
    fields: dict[str, str]
    your_decision: Decision
    your_notes: str


@dataclass(frozen=True)
class HumanInboxAnswer:
    packet_id: str
    status: str
    reviewer: str
    overall_notes: str
    machine_intent: str
    items: tuple[HumanInboxItem, ...]
    inferred_answer_complete: bool


_TOP_LEVEL_KEYS = {
    "STATUS",
    "REVIEWER",
    "OVERALL_NOTES",
    "MACHINE_INTENT",
}

_ITEM_KEYS = {
    "HUMAN_READABLE_QUESTION",
    "RELATIONSHIP_ID",
    "AGENT_DEFAULT",
    "WHY_AGENT_HESITATED",
    "WHAT_APPROVE_MEANS",
    "WHAT_REJECT_MEANS",
    "EVIDENCE_FILE",
    "YOUR_DECISION",
    "YOUR_NOTES",
}


def _strip_placeholder(value: str) -> str:
    value = value.strip()
    if value.startswith("<") and value.endswith(">"):
        return ""
    return value


def _parse_key_value(line: str) -> tuple[str, str]:
    if ":" not in line:
        raise HumanInboxParseError(f"expected KEY: value line, got: {line!r}")
    key, value = line.split(":", 1)
    return key.strip(), value.strip()


def parse_human_inbox_answer(path: Path) -> HumanInboxAnswer:
    lines = path.read_text(encoding="utf-8").splitlines()
    packet_id = ""
    top_level: dict[str, str] = {}
    items: list[HumanInboxItem] = []
    current_item_id: str | None = None
    current_fields: dict[str, str] = {}
    current_top_level_key: str | None = None
    current_item_key: str | None = None

    def flush_item() -> None:
        nonlocal current_item_id, current_fields, current_item_key
        if current_item_id is None:
            return
        decision = _strip_placeholder(current_fields.get("YOUR_DECISION", "")).lower()
        notes = _strip_placeholder(current_fields.get("YOUR_NOTES", ""))
        if decision and decision not in _ALLOWED_DECISIONS:
            raise HumanInboxParseError(
                f"item {current_item_id!r} has invalid YOUR_DECISION {decision!r}"
            )
        items.append(
            HumanInboxItem(
                item_id=current_item_id,
                fields=dict(current_fields),
                your_decision=decision if decision in _ALLOWED_DECISIONS else "defer",
                your_notes=notes,
            )
        )
        current_item_id = None
        current_fields = {}
        current_item_key = None

    for raw_line in lines:
        line = raw_line.strip()
        if line.startswith("## Packet:"):
            flush_item()
            packet_id = line.split(":", 1)[1].strip()
            current_top_level_key = None
            continue
        if line.startswith("### Item "):
            flush_item()
            current_item_id = line[len("### Item ") :].strip()
            current_top_level_key = None
            continue
        if not line:
            if current_item_id is not None and current_item_key == "YOUR_NOTES":
                current_fields[current_item_key] = current_fields[current_item_key] + "\n"
            elif current_item_id is None and current_top_level_key == "OVERALL_NOTES":
                top_level[current_top_level_key] = top_level.get(current_top_level_key, "") + "\n"
            continue
        if line.startswith("#") or line == "---":
            continue
        if current_item_id is not None and current_item_key == "YOUR_NOTES":
            if ":" in line:
                key, value = _parse_key_value(line)
                if key not in _ITEM_KEYS:
                    current_fields[current_item_key] = (
                        current_fields[current_item_key] + "\n" + line.strip()
                    )
                    continue
        if ":" not in line:
            if current_item_id is not None and current_item_key is not None:
                current_fields[current_item_key] = (
                    current_fields[current_item_key] + "\n" + line.strip()
                )
                continue
            if current_item_id is None and current_top_level_key is not None:
                top_level[current_top_level_key] = (
                    top_level.get(current_top_level_key, "") + "\n" + line.strip()
                ).strip()
                continue
            continue
        key, value = _parse_key_value(line)
        if current_item_id is None:
            if key in _TOP_LEVEL_KEYS:
                top_level[key] = _strip_placeholder(value)
                current_top_level_key = key
            continue
        current_fields[key] = value
        current_item_key = key
    flush_item()

    if not packet_id:
        raise HumanInboxParseError("missing packet header")
    status = _strip_placeholder(top_level.get("STATUS", ""))
    if not status:
        raise HumanInboxParseError("missing STATUS value")
    reviewer = _strip_placeholder(top_level.get("REVIEWER", ""))
    overall_notes = _strip_placeholder(top_level.get("OVERALL_NOTES", ""))
    machine_intent = _strip_placeholder(top_level.get("MACHINE_INTENT", ""))
    inferred_answer_complete = bool(reviewer) and bool(items) and all(
        item.your_decision in _ALLOWED_DECISIONS and item.your_notes
        for item in items
    )

    if status == "answered":
        if not reviewer:
            raise HumanInboxParseError("answered file is missing REVIEWER")
        if not items:
            raise HumanInboxParseError("answered file has no items")
        for item in items:
            if item.your_decision not in _ALLOWED_DECISIONS:
                raise HumanInboxParseError(
                    f"answered file item {item.item_id!r} is missing YOUR_DECISION"
                )
            if not item.your_notes:
                raise HumanInboxParseError(
                    f"answered file item {item.item_id!r} is missing YOUR_NOTES"
                )

    return HumanInboxAnswer(
        packet_id=packet_id,
        status=status,
        reviewer=reviewer,
        overall_notes=overall_notes,
        machine_intent=machine_intent,
        items=tuple(items),
        inferred_answer_complete=inferred_answer_complete,
    )
