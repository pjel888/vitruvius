"""Tests for StructuredLLMClient.

Tests use mocked HTTP responses so no running LLM server is required.
"""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import pytest
from pydantic import BaseModel

from vitruvius.llm.structured_client import StructuredLLMClient


class FakeOutput(BaseModel):
    name: str
    confidence: float


def test_parse_raw_valid_json() -> None:
    client = StructuredLLMClient(backend="ollama")
    raw = '{"name": "test", "confidence": 0.95}'
    result = client._parse_raw(raw, FakeOutput)
    assert result is not None
    assert result.name == "test"
    assert result.confidence == 0.95


def test_parse_raw_with_markdown_fences() -> None:
    client = StructuredLLMClient(backend="ollama")
    raw = '```json\n{"name": "test", "confidence": 0.95}\n```'
    result = client._parse_raw(raw, FakeOutput)
    assert result is not None
    assert result.name == "test"


def test_parse_raw_invalid_json() -> None:
    client = StructuredLLMClient(backend="ollama")
    raw = "not json"
    result = client._parse_raw(raw, FakeOutput)
    assert result is None


def test_parse_raw_validation_error() -> None:
    client = StructuredLLMClient(backend="ollama")
    raw = '{"name": "test", "confidence": "not_a_number"}'
    result = client._parse_raw(raw, FakeOutput)
    assert result is None


def test_extract_with_mocked_ollama() -> None:
    client = StructuredLLMClient(backend="ollama", max_retries=2)
    fake_response = json.dumps({"name": "mocked", "confidence": 0.99})

    with patch("urllib.request.urlopen") as mock_urlopen:
        mock_resp = MagicMock()
        mock_resp.read.return_value = json.dumps({"response": fake_response}).encode()
        mock_urlopen.return_value.__enter__.return_value = mock_resp

        result = client.extract("test prompt", FakeOutput)
        assert result is not None
        assert result.name == "mocked"


def test_extract_retries_on_failure() -> None:
    client = StructuredLLMClient(backend="ollama", max_retries=2, retry_backoff_seconds=0.1)

    with patch("urllib.request.urlopen") as mock_urlopen:
        mock_resp = MagicMock()
        # First call returns invalid JSON, second call returns valid
        mock_resp.read.side_effect = [
            json.dumps({"response": "bad json"}).encode(),
            json.dumps({"response": '{"name": "recovered", "confidence": 0.8}'}).encode(),
        ]
        mock_urlopen.return_value.__enter__.return_value = mock_resp

        result = client.extract("test prompt", FakeOutput)
        assert result is not None
        assert result.name == "recovered"


def test_extract_returns_none_after_all_retries() -> None:
    client = StructuredLLMClient(backend="ollama", max_retries=2, retry_backoff_seconds=0.1)

    with patch("urllib.request.urlopen") as mock_urlopen:
        mock_resp = MagicMock()
        mock_resp.read.return_value = json.dumps({"response": "always bad"}).encode()
        mock_urlopen.return_value.__enter__.return_value = mock_resp

        result = client.extract("test prompt", FakeOutput)
        assert result is None
