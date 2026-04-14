"""Ollama env config helper — version-gated env var emission (Task F.7)."""

from __future__ import annotations

import re
from dataclasses import dataclass


KV_CACHE_MIN_VERSION = (0, 4, 0)
FLASH_ATTENTION_MIN_VERSION = (0, 4, 0)
SPECULATIVE_DECODE_MIN_VERSION = (0, 6, 0)

_VERSION_PATTERN = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")


@dataclass(frozen=True)
class OllamaEnvConfig:
    num_parallel: int = 4
    kv_cache_type: str = "q8_0"
    flash_attention: bool = True
    speculative_decoding: bool = False
    draft_model: str | None = None


@dataclass(frozen=True)
class EnvExport:
    env_vars: dict[str, str]
    notes: tuple[str, ...]


def parse_ollama_version(raw: str) -> tuple[int, int, int]:
    match = _VERSION_PATTERN.match(raw.strip())
    if match is None:
        raise ValueError(f"invalid ollama version: {raw!r}")
    return (int(match.group(1)), int(match.group(2)), int(match.group(3)))


def _meets(version: tuple[int, int, int] | None, minimum: tuple[int, int, int]) -> bool:
    if version is None:
        return True
    return version >= minimum


def build_ollama_env(
    config: OllamaEnvConfig,
    *,
    ollama_version: str | None = None,
) -> EnvExport:
    parsed: tuple[int, int, int] | None = None
    if ollama_version is not None:
        parsed = parse_ollama_version(ollama_version)

    env: dict[str, str] = {}
    notes: list[str] = []

    env["OLLAMA_NUM_PARALLEL"] = str(config.num_parallel)

    if _meets(parsed, KV_CACHE_MIN_VERSION):
        env["OLLAMA_KV_CACHE_TYPE"] = config.kv_cache_type
    else:
        notes.append(
            f"skipped OLLAMA_KV_CACHE_TYPE: requires Ollama >= "
            f"{'.'.join(str(n) for n in KV_CACHE_MIN_VERSION)}, detected {ollama_version}"
        )

    if config.flash_attention and _meets(parsed, FLASH_ATTENTION_MIN_VERSION):
        env["OLLAMA_FLASH_ATTENTION"] = "1"
    elif config.flash_attention:
        notes.append(
            f"skipped OLLAMA_FLASH_ATTENTION: requires Ollama >= "
            f"{'.'.join(str(n) for n in FLASH_ATTENTION_MIN_VERSION)}, detected {ollama_version}"
        )

    if config.speculative_decoding:
        if config.draft_model is None:
            notes.append("skipped OLLAMA_SPEC_DECODE: no draft_model configured")
        elif not _meets(parsed, SPECULATIVE_DECODE_MIN_VERSION):
            notes.append(
                f"skipped OLLAMA_SPEC_DECODE: requires Ollama >= "
                f"{'.'.join(str(n) for n in SPECULATIVE_DECODE_MIN_VERSION)}, detected {ollama_version}"
            )
        else:
            env["OLLAMA_SPEC_DECODE"] = "1"
            env["OLLAMA_DRAFT_MODEL"] = config.draft_model

    return EnvExport(env_vars=env, notes=tuple(notes))
