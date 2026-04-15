"""Sprint WIKI — :mod:`vitruvius.wiki.ollama_client` unit tests.

Policy: these tests MUST NOT make live Ollama calls. Another agent
may be running bench work against ``http://127.0.0.1:11434``
concurrently, so every case patches :meth:`httpx.Client.post` before
instantiating :class:`OllamaLLMClient`. Live smoke of ``gemma4:e4b``
is the operator's job and is guarded behind a skipped integration
test at the bottom of this file.
"""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock, patch

import httpx
import pytest

from vitruvius.wiki.ollama_client import OllamaClientError, OllamaLLMClient


def _fake_response(
    *,
    json_payload: dict[str, Any] | None = None,
    raise_for_status_exc: Exception | None = None,
) -> MagicMock:
    """Build a MagicMock that looks enough like :class:`httpx.Response`
    for :meth:`OllamaLLMClient.complete` to introspect.
    """
    response = MagicMock(name="httpx.Response")
    if raise_for_status_exc is not None:
        response.raise_for_status.side_effect = raise_for_status_exc
    else:
        response.raise_for_status.return_value = None
    response.json.return_value = json_payload or {}
    return response


def test_complete_returns_response_field() -> None:
    """Happy path: the ``response`` field is surfaced verbatim."""
    fake = _fake_response(json_payload={"response": "hello"})

    with patch.object(httpx.Client, "post", return_value=fake) as mock_post:
        client = OllamaLLMClient(base_url="http://127.0.0.1:11434")
        out = client.complete("anything")

    assert out == "hello"
    assert mock_post.call_count == 1


def test_complete_sends_format_json() -> None:
    """The POST body must force ``format="json"`` and ``stream=False``
    so upstream pydantic validation has a strict JSON string to chew on.
    """
    fake = _fake_response(json_payload={"response": "{}"})

    with patch.object(httpx.Client, "post", return_value=fake) as mock_post:
        client = OllamaLLMClient(base_url="http://127.0.0.1:11434")
        client.complete("prompt here")

    # httpx.Client.post was called as a bound method, so args[0] is
    # the endpoint URL and kwargs carry the JSON payload.
    assert mock_post.call_count == 1
    _, call_args, call_kwargs = mock_post.mock_calls[0]
    # Endpoint is the first positional arg after self (removed by
    # MagicMock since we patched at the class level — so args[0] is
    # the URL).
    url = call_args[0]
    payload = call_kwargs["json"]

    assert url.endswith("/api/generate")
    assert payload["format"] == "json"
    assert payload["stream"] is False
    assert payload["prompt"] == "prompt here"
    assert payload["options"] == {"temperature": 0}


def test_complete_uses_configured_model() -> None:
    """Custom model names must flow through to the POST body."""
    fake = _fake_response(json_payload={"response": "{}"})

    with patch.object(httpx.Client, "post", return_value=fake) as mock_post:
        client = OllamaLLMClient(
            model="custom:1b",
            base_url="http://127.0.0.1:11434",
        )
        client.complete("any prompt")

    _, _, call_kwargs = mock_post.mock_calls[0]
    assert call_kwargs["json"]["model"] == "custom:1b"


def test_complete_raises_on_http_error() -> None:
    """HTTP errors must be wrapped in :class:`OllamaClientError` so
    callers can distinguish transport failures from pydantic validation
    errors on otherwise-valid JSON payloads.
    """
    http_err = httpx.HTTPStatusError(
        "500 Internal Server Error",
        request=MagicMock(name="httpx.Request"),
        response=MagicMock(name="httpx.Response", status_code=500),
    )
    fake = _fake_response(raise_for_status_exc=http_err)

    with patch.object(httpx.Client, "post", return_value=fake):
        client = OllamaLLMClient(base_url="http://127.0.0.1:11434")
        with pytest.raises(OllamaClientError) as excinfo:
            client.complete("anything")

    assert "500" in str(excinfo.value) or "Internal Server Error" in str(excinfo.value)


def test_complete_raises_on_empty_response() -> None:
    """An empty ``response`` field is treated as an adapter failure —
    synthesis_loop / ego_linter would otherwise blow up inside pydantic
    with a confusing validation trace.
    """
    fake = _fake_response(json_payload={"response": ""})

    with patch.object(httpx.Client, "post", return_value=fake):
        client = OllamaLLMClient(base_url="http://127.0.0.1:11434")
        with pytest.raises(OllamaClientError) as excinfo:
            client.complete("anything")

    assert "empty" in str(excinfo.value).lower() or "missing" in str(excinfo.value).lower()


def test_complete_raises_on_missing_response_field() -> None:
    """Belt-and-braces: a well-formed JSON envelope without a
    ``response`` key should also raise ``OllamaClientError`` so we never
    leak ``None`` through the LLMClient contract.
    """
    fake = _fake_response(json_payload={"model": "gemma4:e4b"})  # no response

    with patch.object(httpx.Client, "post", return_value=fake):
        client = OllamaLLMClient(base_url="http://127.0.0.1:11434")
        with pytest.raises(OllamaClientError):
            client.complete("anything")


def test_base_url_default_strips_trailing_slash() -> None:
    """A base_url passed with a trailing slash must still produce a
    clean ``/api/generate`` endpoint (no doubled slash).
    """
    fake = _fake_response(json_payload={"response": "ok"})

    with patch.object(httpx.Client, "post", return_value=fake) as mock_post:
        client = OllamaLLMClient(base_url="http://127.0.0.1:11434/")
        client.complete("hello")

    _, call_args, _ = mock_post.mock_calls[0]
    assert call_args[0] == "http://127.0.0.1:11434/api/generate"


@pytest.mark.skip(reason="live integration smoke; run manually")
def test_complete_live_gemma_smoke() -> None:  # pragma: no cover
    """Operator-run smoke test — expects ``ollama serve`` + ``gemma4:e4b``."""
    client = OllamaLLMClient(model="gemma4:e4b")
    out = client.complete(
        'Return strict JSON of the form {"ping": "pong"} and nothing else.'
    )
    assert '"ping"' in out
