"""WIKI Ollama LLM client — production implementation of LLMClient.

Wraps Ollama's ``/api/generate`` endpoint with ``format="json"`` so the
LLM is forced to emit strict JSON. The adapter is **synchronous**
(matches the :class:`vitruvius.wiki.llm_client.LLMClient` Protocol) and
does a blocking :class:`httpx.Client` POST under the hood.

Usage::

    from vitruvius.wiki.ollama_client import OllamaLLMClient

    client = OllamaLLMClient(model="gemma4:e4b")
    raw = client.complete("Return JSON …")

Tests mock ``httpx.Client.post`` so no live Ollama traffic is generated.
Live use happens in operator scripts only — there is **no**
auto-instantiation in any auto-loaded module, keeping ``pytest``
completely offline.
"""

from __future__ import annotations

from typing import Any, Final

import httpx

from vitruvius.config import get_ollama_url

__all__ = ["OllamaClientError", "OllamaLLMClient"]


_DEFAULT_MODEL: Final[str] = "gemma4:e4b"
_DEFAULT_TIMEOUT_SECONDS: Final[float] = 600.0


class OllamaClientError(RuntimeError):
    """Raised when the Ollama adapter cannot return a valid response.

    Used to distinguish transport/protocol failures (HTTP errors, empty
    ``response`` field, malformed JSON envelope) from downstream
    ``pydantic.ValidationError`` raised by :mod:`vitruvius.wiki.synthesis_loop`
    when the returned JSON body does not conform to
    :class:`WikiPageProposal`.
    """


class OllamaLLMClient:
    """Synchronous LLM client backed by a local Ollama server.

    Implements the :class:`vitruvius.wiki.llm_client.LLMClient` Protocol,
    so instances are drop-in for the existing WIKI.2 synthesis loop and
    WIKI.4.2 ego-graph linter. No auto-instantiation — operators build
    one explicitly and inject it into
    :func:`vitruvius.wiki.synthesis_loop.synthesize_wiki_page` /
    :func:`vitruvius.wiki.ego_linter.lint_ego_graph`.
    """

    def __init__(
        self,
        *,
        model: str = _DEFAULT_MODEL,
        base_url: str | None = None,
        timeout_seconds: float = _DEFAULT_TIMEOUT_SECONDS,
    ) -> None:
        self._model = model
        self._base_url = (base_url or get_ollama_url()).rstrip("/")
        self._timeout_seconds = float(timeout_seconds)

    @property
    def model(self) -> str:
        return self._model

    @property
    def base_url(self) -> str:
        return self._base_url

    def complete(self, prompt: str) -> str:
        """Send ``prompt`` to Ollama and return the raw text response.

        Forces ``format="json"`` and ``stream=False`` so the upstream
        consumers can call :func:`pydantic.TypeAdapter.validate_json`
        directly on the returned string. ``temperature=0`` makes the
        synthesis/linter outputs deterministic for a given prompt.

        Raises:
            OllamaClientError: if the HTTP call fails, the JSON
                envelope is malformed, or the ``response`` field is
                missing or empty.
        """
        endpoint = f"{self._base_url}/api/generate"
        payload: dict[str, Any] = {
            "model": self._model,
            "prompt": prompt,
            "format": "json",
            "stream": False,
            "options": {"temperature": 0},
        }

        try:
            with httpx.Client(timeout=self._timeout_seconds) as client:
                resp = client.post(endpoint, json=payload)
                resp.raise_for_status()
                data = resp.json()
        except (httpx.HTTPError, ValueError, KeyError) as exc:
            raise OllamaClientError(
                f"Ollama request to {endpoint} failed: {exc}"
            ) from exc

        if not isinstance(data, dict):
            raise OllamaClientError(
                f"Ollama returned non-dict envelope from {endpoint}: "
                f"{type(data).__name__}"
            )

        response = data.get("response")
        if not isinstance(response, str) or not response:
            raise OllamaClientError(
                "Ollama returned an empty or missing 'response' field "
                f"from {endpoint}"
            )

        return response
