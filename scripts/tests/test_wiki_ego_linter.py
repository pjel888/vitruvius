"""Sprint WIKI Stream WIKI.4.2 — ego-graph linter tests (mocked LLM).

Policy: zero live Ollama calls. These tests feed canned JSON
responses through a tiny ``_MockLLM`` object that conforms to
:class:`vitruvius.wiki.llm_client.LLMClient`. The ``empty_neighbors``
case additionally asserts that the LLM is never invoked, matching
the short-circuit contract in
:func:`vitruvius.wiki.ego_linter.lint_ego_graph`.
"""

from __future__ import annotations

from vitruvius.wiki.ego_linter import ContradictionReport, lint_ego_graph
from vitruvius.wiki.kuzu_store import WikiPageRow


class _MockLLM:
    """Canned-response LLM client for ego-linter tests."""

    def __init__(self, response: str) -> None:
        self.response = response
        self.call_count = 0

    def complete(self, prompt: str) -> str:
        self.call_count += 1
        return self.response


def _row(
    page_id: str,
    *,
    title: str = "T",
    tags: tuple[str, ...] = (),
    linked: tuple[str, ...] = (),
) -> WikiPageRow:
    return WikiPageRow(
        page_id=page_id,
        title=title,
        source_id="pd-1096",
        tags=tags,
        linked_entities=linked,
    )


def test_lint_reports_contradiction() -> None:
    canned = (
        '{"contradictions": ['
        '{"neighbor_id": "concept-egress-width-legacy", '
        '"reason": "claims 0.9 m but focal says 1.2 m"}'
        ']}'
    )
    llm = _MockLLM(canned)
    focal = _row("concept-egress-width", title="Egress Width")
    neighbors = [_row("concept-egress-width-legacy", title="Legacy Egress")]

    report = lint_ego_graph(
        focal_page=focal,
        neighbors=neighbors,
        llm_client=llm,
    )

    assert isinstance(report, ContradictionReport)
    assert report.focal_page_id == "concept-egress-width"
    assert report.contradicting_neighbor_ids == ("concept-egress-width-legacy",)
    assert "0.9 m" in report.reason
    assert llm.call_count == 1


def test_lint_returns_none_when_clean() -> None:
    llm = _MockLLM('{"contradictions": []}')
    focal = _row("concept-foo")
    neighbors = [_row("concept-bar"), _row("concept-baz")]

    result = lint_ego_graph(
        focal_page=focal,
        neighbors=neighbors,
        llm_client=llm,
    )

    assert result is None
    assert llm.call_count == 1


def test_lint_handles_empty_neighbors() -> None:
    llm = _MockLLM("this should never be parsed")
    focal = _row("concept-orphan")

    result = lint_ego_graph(
        focal_page=focal,
        neighbors=[],
        llm_client=llm,
    )

    assert result is None
    assert llm.call_count == 0
