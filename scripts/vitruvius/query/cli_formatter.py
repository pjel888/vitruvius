from __future__ import annotations

from .result import QueryCitation, QueryResult


_NO_EVIDENCE = "No supporting evidence found"


def _escape(text: str) -> str:
    return text.replace("\r", " ").replace("\n", " ")


def _format_citation(index: int, citation: QueryCitation) -> list[str]:
    snippet = _escape(citation.evidence_snippet).strip() or "(no snippet)"
    section = citation.source_section_id or "(no section)"
    source_label = citation.source_id
    if citation.source_title and citation.source_title.strip() and citation.source_title != citation.source_id:
        source_label = f"{citation.source_title} [{citation.source_id}]"
    lines = [
        f"  [{index}] {source_label} {section}",
        f"      \"{snippet}\"",
        f"      Confidence: {citation.confidence:.2f}",
    ]
    return lines


def _format_arguments(arguments) -> str:
    if not arguments:
        return "{}"
    parts = [f"{k}={v}" for k, v in sorted(arguments.items())]
    return "{" + ", ".join(parts) + "}"


def render_query_result(result: QueryResult) -> str:
    lines: list[str] = []
    lines.append(f"Question: {_escape(result.question)}")
    lines.append("")
    if result.has_evidence:
        display = result.answer_display_entities or result.answer_entities
        answer = ", ".join(display) if display else "(no entities)"
        lines.append(f"Answer: {answer}")
        lines.append("")
        lines.append(f"Confidence: {result.aggregate_confidence:.2f}")
        lines.append("")
        lines.append("Supporting Evidence:")
        for idx, citation in enumerate(result.citations, start=1):
            lines.extend(_format_citation(idx, citation))
    else:
        lines.append(f"Answer: {_NO_EVIDENCE}")
        lines.append("")
        lines.append("Confidence: 0.00")
    lines.append("")
    lines.append("Query trace:")
    lines.append(f"  function: {result.query_function}")
    lines.append(f"  arguments: {_format_arguments(result.arguments)}")
    return "\n".join(lines) + "\n"
