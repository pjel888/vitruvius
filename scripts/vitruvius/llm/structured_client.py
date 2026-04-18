"""Structured LLM client for the Knowledge Graph transition.

Wraps local (Ollama) and optional cloud LLM calls with Pydantic v2
schema validation, retry logic, and failure logging.

This is the canonical extraction gate: no free-form LLM output may
mutate the graph without passing through here first.
"""

from __future__ import annotations

import json
import logging
import time
from pathlib import Path
from typing import Any, TypeVar

from pydantic import BaseModel, ValidationError

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class StructuredLLMClient:
    """Client that enforces schema-constrained LLM outputs.

    Supports two backends:
    - ``ollama`` (default): local Ollama via HTTP POST to /api/generate
    - ``openai`` (optional): cloud OpenAI-compatible API

    All outputs are validated against the provided Pydantic model.
    Invalid outputs are retried up to ``max_retries`` times.
    """

    def __init__(
        self,
        backend: str = "ollama",
        ollama_url: str = "http://127.0.0.1:11434",
        ollama_model: str = "gemma4:31b",
        openai_api_key: str | None = None,
        openai_model: str = "gpt-4o",
        max_retries: int = 3,
        retry_backoff_seconds: float = 2.0,
        timeout_seconds: int = 600,
        temperature: float = 0.0,
    ) -> None:
        self.backend = backend
        self.ollama_url = ollama_url.rstrip("/")
        self.ollama_model = ollama_model
        self.openai_api_key = openai_api_key
        self.openai_model = openai_model
        self.max_retries = max_retries
        self.retry_backoff_seconds = retry_backoff_seconds
        self.timeout_seconds = timeout_seconds
        self.temperature = temperature

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def extract(self, prompt: str, model_cls: type[T], **kwargs: Any) -> T | None:
        """Call the LLM and validate the response against *model_cls*.

        Returns the validated model instance, or ``None`` if all retries
        are exhausted. Parse failures are logged to
        ``006_System-Manifests/runs/llm_parse_failures/``.
        """
        for attempt in range(1, self.max_retries + 1):
            raw = self._call(prompt, **kwargs)
            if raw is None:
                logger.warning("Attempt %d/%d: LLM returned None", attempt, self.max_retries)
                self._backoff(attempt)
                continue

            parsed = self._parse_raw(raw, model_cls)
            if parsed is not None:
                return parsed

            self._log_failure(prompt, raw, model_cls.__name__, attempt)
            self._backoff(attempt)

        logger.error("All %d retries exhausted for model %s", self.max_retries, model_cls.__name__)
        return None

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _call(self, prompt: str, **kwargs: Any) -> str | None:
        if self.backend == "ollama":
            return self._call_ollama(prompt, **kwargs)
        if self.backend == "openai":
            return self._call_openai(prompt, **kwargs)
        raise ValueError(f"Unknown backend: {self.backend}")

    def _call_ollama(self, prompt: str, **kwargs: Any) -> str | None:
        import urllib.request

        body = json.dumps(
            {
                "model": kwargs.get("model", self.ollama_model),
                "prompt": prompt,
                "format": "json",
                "stream": False,
                "options": {
                    "temperature": self.temperature,
                    "num_predict": kwargs.get("num_predict", 300),
                },
            }
        ).encode("utf-8")

        req = urllib.request.Request(
            f"{self.ollama_url}/api/generate",
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=self.timeout_seconds) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data.get("response", "")
        except Exception as exc:
            logger.warning("Ollama call failed: %s", exc)
            return None

    def _call_openai(self, prompt: str, **kwargs: Any) -> str | None:
        try:
            import openai
        except ImportError:
            logger.error("openai package not installed; cannot use cloud backend")
            return None

        client = openai.OpenAI(api_key=self.openai_api_key)
        try:
            resp = client.chat.completions.create(
                model=kwargs.get("model", self.openai_model),
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature,
                response_format={"type": "json_object"},
            )
            return resp.choices[0].message.content or ""
        except Exception as exc:
            logger.warning("OpenAI call failed: %s", exc)
            return None

    def _parse_raw(self, raw: str, model_cls: type[T]) -> T | None:
        # Strip markdown fences if present
        text = raw.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()

        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            logger.debug("JSON parse error: %s", exc)
            return None

        try:
            return model_cls.model_validate(data)
        except ValidationError as exc:
            logger.debug("Pydantic validation error: %s", exc)
            return None

    def _backoff(self, attempt: int) -> None:
        delay = self.retry_backoff_seconds * attempt
        logger.debug("Backing off %.1fs after attempt %d", delay, attempt)
        time.sleep(delay)

    def _log_failure(
        self,
        prompt: str,
        raw: str,
        model_name: str,
        attempt: int,
    ) -> None:
        from vitruvius.paths import get_repo_root

        fail_dir = get_repo_root() / "006_System-Manifests" / "runs" / "llm_parse_failures"
        fail_dir.mkdir(parents=True, exist_ok=True)

        timestamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
        path = fail_dir / f"{timestamp}_{model_name}_attempt{attempt}.json"
        payload = {
            "prompt_preview": prompt[:500],
            "raw_output": raw,
            "model": model_name,
            "attempt": attempt,
        }
        try:
            path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        except OSError as exc:
            logger.warning("Could not write parse failure log: %s", exc)
