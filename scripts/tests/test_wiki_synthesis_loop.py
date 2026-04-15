"""Sprint WIKI Stream WIKI.2 — synthesis-loop tests (mocked LLM).

Policy: these tests MUST NOT make live Ollama calls. The
synthesis loop consumes any object conforming to
:class:`vitruvius.wiki.llm_client.LLMClient`, so we inject a tiny
``_MockLLM`` that returns canned responses. Running these tests
with ``OLLAMA_HOST=unreachable`` (or no network at all) must still
pass.
"""

from __future__ import annotations

import pydantic
import pytest

from vitruvius.wiki.synthesis_loop import (
    WikiPageProposal,
    synthesize_wiki_page,
)


class _MockLLM:
    """Canned-response LLM client for synthesis-loop tests."""

    def __init__(self, response: str) -> None:
        self.response = response
        self.prompts: list[str] = []

    def complete(self, prompt: str) -> str:
        self.prompts.append(prompt)
        return self.response


def test_synthesis_happy_path() -> None:
    canned = (
        '{"page_id": "concept-egress-width", '
        '"title": "Egress Width", '
        '"body_markdown": "Minimum 1.2 m per PD 1096.", '
        '"linked_entities": ["source-pd-1096"], '
        '"source_citations": ["PD 1096 §3.4"]}'
    )
    llm = _MockLLM(canned)

    proposal = synthesize_wiki_page(
        raw_markdown="# PD 1096\nMinimum egress width 1.2 m.",
        llm_client=llm,
        source_id="pd-1096-national-building-code",
    )

    assert isinstance(proposal, WikiPageProposal)
    assert proposal.page_id == "concept-egress-width"
    assert proposal.title == "Egress Width"
    assert proposal.body_markdown == "Minimum 1.2 m per PD 1096."
    assert proposal.linked_entities == ["source-pd-1096"]
    assert proposal.source_citations == ["PD 1096 §3.4"]
    # The prompt must mention the source_id so the LLM can cite it.
    assert len(llm.prompts) == 1
    assert "pd-1096-national-building-code" in llm.prompts[0]


def test_synthesis_invalid_page_id_raises() -> None:
    canned = (
        '{"page_id": "building-permit", '  # missing concept|source|relationship prefix
        '"title": "Building Permit", '
        '"body_markdown": "body"}'
    )
    llm = _MockLLM(canned)

    with pytest.raises(pydantic.ValidationError) as excinfo:
        synthesize_wiki_page(
            raw_markdown="raw",
            llm_client=llm,
            source_id="pd-1096",
        )
    assert "page_id" in str(excinfo.value)


def test_synthesis_malformed_json_raises() -> None:
    llm = _MockLLM("not json")

    with pytest.raises(pydantic.ValidationError):
        synthesize_wiki_page(
            raw_markdown="raw",
            llm_client=llm,
            source_id="pd-1096",
        )
