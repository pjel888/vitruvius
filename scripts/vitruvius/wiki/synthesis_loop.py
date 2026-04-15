"""Sprint WIKI Stream WIKI.2 — LLM-driven wiki synthesis loop.

This module feeds freshly-ingested Markdown to an LLM (behind the
:class:`~vitruvius.wiki.llm_client.LLMClient` Protocol) and asks it
to return a strictly-shaped JSON object describing a single wiki
page. The response is parsed and validated in one step via
:class:`pydantic.TypeAdapter`, so malformed output surfaces as a
:class:`pydantic.ValidationError` that the caller can either retry
on or escalate.

Scope:
  * Hard-enforces ``page_id`` naming (``^(concept|source|relationship)-[a-z0-9-]+$``).
  * Produces a :class:`WikiPageProposal` that the next pipeline stage
    (cosine-similarity bidirectional linker, out of scope here) can
    ingest.
  * Never makes network calls directly — everything goes through the
    injected ``LLMClient``. Tests stub the client with a canned mock.

The bidirectional cosine-similarity linker mentioned in the
phase-14 plan is deferred; this stream only names the linked
entities that the LLM proposes.
"""

from __future__ import annotations

import re

import pydantic

from vitruvius.wiki.llm_client import LLMClient

# Page IDs are namespaced by kind so downstream Kuzu queries can
# filter by prefix without a separate column. The three kinds come
# from phase-14 §WIKI.2: concept nodes, source nodes, and
# relationship nodes.
PAGE_ID_PATTERN = re.compile(r"^(concept|source|relationship)-[a-z0-9-]+$")


class WikiPageProposal(pydantic.BaseModel):
    """Strict schema for one LLM-proposed wiki page.

    The synthesis loop asks the LLM to return a JSON object with
    exactly these fields. The ``page_id`` field is validated against
    :data:`PAGE_ID_PATTERN` so a malformed ID causes
    :class:`pydantic.ValidationError`, not silent downstream garbage.
    """

    model_config = pydantic.ConfigDict(frozen=True, extra="forbid")

    page_id: str
    title: str
    body_markdown: str
    linked_entities: list[str] = pydantic.Field(default_factory=list)
    source_citations: list[str] = pydantic.Field(default_factory=list)

    @pydantic.field_validator("page_id")
    @classmethod
    def _validate_page_id(cls, value: str) -> str:
        if not PAGE_ID_PATTERN.match(value):
            raise ValueError(
                f"page_id {value!r} must match "
                f"{PAGE_ID_PATTERN.pattern!r}"
            )
        return value


_PROPOSAL_ADAPTER: pydantic.TypeAdapter[WikiPageProposal] = pydantic.TypeAdapter(
    WikiPageProposal
)


_SYNTHESIS_PROMPT_TEMPLATE = """\
You are a domain-expert knowledge-graph author. Read the raw Markdown
below (converted from a primary source with source_id={source_id!r})
and propose exactly ONE wiki page describing the most salient
concept, source, or relationship it introduces.

Respond with a single JSON object — no prose, no code fences — whose
keys are exactly:

  page_id          (string, matching ^(concept|source|relationship)-[a-z0-9-]+$)
  title            (string)
  body_markdown    (string, Markdown body with inline citations)
  linked_entities  (array of strings — other wiki page_ids to link)
  source_citations (array of strings — source anchors used)

Raw Markdown:
---
{raw_markdown}
---
"""


def _build_synthesis_prompt(*, raw_markdown: str, source_id: str) -> str:
    """Compose the strict-JSON synthesis prompt.

    Kept as a private helper so a future Ollama adapter can reuse it
    or pin it for reproducibility.
    """
    return _SYNTHESIS_PROMPT_TEMPLATE.format(
        raw_markdown=raw_markdown,
        source_id=source_id,
    )


def synthesize_wiki_page(
    *,
    raw_markdown: str,
    llm_client: LLMClient,
    source_id: str,
) -> WikiPageProposal:
    """Run the WIKI.2 synthesis loop once.

    Parameters
    ----------
    raw_markdown
        Markdown previously converted from a primary source by
        :func:`vitruvius.wiki.docling_parser.convert_pdf_to_markdown`.
    llm_client
        Any object conforming to the :class:`LLMClient` Protocol —
        tests pass a mock; production passes the real Ollama client.
    source_id
        Stable identifier for the primary source (e.g.
        ``"pd-1096-national-building-code"``) so the LLM can reference
        it in citations.

    Returns
    -------
    WikiPageProposal
        A validated proposal. The caller is free to enqueue it into
        Kuzu via :class:`vitruvius.wiki.kuzu_store.KuzuWikiStore`.

    Raises
    ------
    pydantic.ValidationError
        If the LLM returns JSON that does not match the
        :class:`WikiPageProposal` schema — including an invalid
        ``page_id`` prefix or a body that omits required fields.
        Also raised (wrapping the underlying parse error) when the
        LLM returns text that is not valid JSON at all.
    """
    prompt = _build_synthesis_prompt(
        raw_markdown=raw_markdown, source_id=source_id
    )
    raw_response = llm_client.complete(prompt)
    return _PROPOSAL_ADAPTER.validate_json(raw_response)


__all__ = [
    "PAGE_ID_PATTERN",
    "WikiPageProposal",
    "synthesize_wiki_page",
]
