from __future__ import annotations

from pathlib import Path

import pytest

from vitruvius.human_inbox import HumanInboxParseError, parse_human_inbox_answer


def _write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def test_parse_pending_answer_file_accepts_placeholders() -> None:
    path = Path("/tmp/human_inbox_pending.md")
    _write(
        path,
        """# Human Inbox — Current Pending Decisions

## Packet: demo-packet
STATUS: pending
REVIEWER: <your name here>
OVERALL_NOTES: <optional summary>
MACHINE_INTENT: I am deciding whether to admit a staged relationship.

### Item item-1
HUMAN_READABLE_QUESTION: Is this okay?
RELATIONSHIP_ID: rel-1
AGENT_DEFAULT: reject
WHY_AGENT_HESITATED: not enough evidence
WHAT_APPROVE_MEANS: admit it
WHAT_REJECT_MEANS: keep it out
EVIDENCE_FILE: path/to/file.md
YOUR_DECISION: <approve|reject|defer>
YOUR_NOTES: <type your notes here>
""",
    )
    parsed = parse_human_inbox_answer(path)
    assert parsed.packet_id == "demo-packet"
    assert parsed.status == "pending"
    assert parsed.reviewer == ""
    assert parsed.machine_intent == "I am deciding whether to admit a staged relationship."
    assert parsed.items[0].fields["HUMAN_READABLE_QUESTION"] == "Is this okay?"
    assert parsed.inferred_answer_complete is False


def test_parse_answered_file_requires_reviewer_and_notes() -> None:
    path = Path("/tmp/human_inbox_answered.md")
    _write(
        path,
        """# Human Inbox — Current Pending Decisions

## Packet: demo-packet
STATUS: answered
REVIEWER: Phil
OVERALL_NOTES: looks good overall
MACHINE_INTENT: Decide whether to admit the relationship.

### Item item-1
HUMAN_READABLE_QUESTION: Is this okay?
RELATIONSHIP_ID: rel-1
AGENT_DEFAULT: reject
WHY_AGENT_HESITATED: not enough evidence
WHAT_APPROVE_MEANS: admit it
WHAT_REJECT_MEANS: keep it out
EVIDENCE_FILE: path/to/file.md
YOUR_DECISION: reject
YOUR_NOTES: The evidence is too weak.
""",
    )
    parsed = parse_human_inbox_answer(path)
    assert parsed.status == "answered"
    assert parsed.reviewer == "Phil"
    assert parsed.items[0].your_decision == "reject"
    assert parsed.inferred_answer_complete is True


def test_parse_answered_file_rejects_missing_notes() -> None:
    path = Path("/tmp/human_inbox_bad.md")
    _write(
        path,
        """# Human Inbox — Current Pending Decisions

## Packet: demo-packet
STATUS: answered
REVIEWER: Phil
OVERALL_NOTES: done
MACHINE_INTENT: Decide whether to admit the relationship.

### Item item-1
HUMAN_READABLE_QUESTION: Is this okay?
RELATIONSHIP_ID: rel-1
AGENT_DEFAULT: reject
WHY_AGENT_HESITATED: not enough evidence
WHAT_APPROVE_MEANS: admit it
WHAT_REJECT_MEANS: keep it out
EVIDENCE_FILE: path/to/file.md
YOUR_DECISION: approve
YOUR_NOTES: <type your notes here>
""",
    )
    with pytest.raises(HumanInboxParseError):
        parse_human_inbox_answer(path)


def test_parse_pending_file_supports_multiline_human_notes_and_infers_completion() -> None:
    path = Path("/tmp/human_inbox_multiline.md")
    _write(
        path,
        """# Human Inbox — Current Pending Decisions

## Packet: demo-packet
STATUS: pending
REVIEWER: Phil
OVERALL_NOTES: looks okay
MACHINE_INTENT: Decide whether to admit the relationship.

### Item item-1
HUMAN_READABLE_QUESTION: Is this okay?
RELATIONSHIP_ID: rel-1
AGENT_DEFAULT: reject
WHY_AGENT_HESITATED: not enough evidence
WHAT_APPROVE_MEANS: admit it
WHAT_REJECT_MEANS: keep it out
EVIDENCE_FILE: path/to/file.md
YOUR_DECISION: defer
YOUR_NOTES: First line.
Second line.
Third line.
""",
    )
    parsed = parse_human_inbox_answer(path)
    assert parsed.status == "pending"
    assert parsed.inferred_answer_complete is True
    assert parsed.items[0].your_notes == "First line.\nSecond line.\nThird line."


def test_parse_pending_file_preserves_blank_lines_in_human_notes() -> None:
    path = Path("/tmp/human_inbox_blank_lines.md")
    _write(
        path,
        """# Human Inbox — Current Pending Decisions

## Packet: demo-packet
STATUS: pending
REVIEWER: Phil
OVERALL_NOTES: summary
MACHINE_INTENT: Decide whether to admit the relationship.

### Item item-1
HUMAN_READABLE_QUESTION: Is this okay?
RELATIONSHIP_ID: rel-1
AGENT_DEFAULT: reject
WHY_AGENT_HESITATED: not enough evidence
WHAT_APPROVE_MEANS: admit it
WHAT_REJECT_MEANS: keep it out
EVIDENCE_FILE: path/to/file.md
YOUR_DECISION: defer
YOUR_NOTES: First line.

Second line after blank line.
Third line.
""",
    )
    parsed = parse_human_inbox_answer(path)
    assert parsed.items[0].your_notes == "First line.\n\nSecond line after blank line.\nThird line."
