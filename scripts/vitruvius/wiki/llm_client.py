"""Sprint WIKI — shared ``LLMClient`` Protocol.

WIKI.2 (Synthesis Loop) and WIKI.4.2 (Ego-Graph Linter) both call an
LLM to extract structured JSON from free-text prompts. Rather than
hard-code a network client into each module, they depend on the
minimal :class:`LLMClient` Protocol declared here. Tests pass a tiny
mock object that conforms to the protocol; the real Ollama wiring
lives in a future ``wiki/ollama_client.py`` that is out of scope for
this task.

The protocol is deliberately thin: a single synchronous
:meth:`LLMClient.complete` that takes a prompt and returns the raw
text response. Structured-output validation is the caller's
responsibility (via :func:`pydantic.TypeAdapter.validate_json`).
"""

from __future__ import annotations

from typing import Protocol


class LLMClient(Protocol):
    """Minimal LLM client interface used by WIKI.2 / WIKI.4.2.

    Implementers only have to provide :meth:`complete`. A real Ollama
    adapter will wrap ``httpx.post('/api/generate', json={...})`` and
    return ``response['response']``; tests supply a canned-response
    mock. See ``scripts/tests/test_wiki_synthesis_loop.py`` and
    ``scripts/tests/test_wiki_ego_linter.py`` for the mock pattern.
    """

    def complete(self, prompt: str) -> str:
        """Return the LLM's text response for ``prompt``.

        Synchronous on purpose so that the synthesis/linter call sites
        stay linear and easy to reason about. Implementations may
        still do network I/O under the hood.
        """
        ...
