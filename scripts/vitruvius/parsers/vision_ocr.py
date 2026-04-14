"""Stream Y5.1 — Ollama vision-model fallback for PDF table extraction.

Called ONLY when Stream B's ``table_graph_extractor`` cannot produce a
CSV / XLSX interpretation of a page (e.g. the page is a rasterised
image, not an extractable text layer). Gated behind
``features.y_vision_ocr`` plus a ``ple-vision-probe`` (Y5.3) pre-flight.

The call is stateless — no temporary files outside the caller's
``tmp_path``, no caching. Image pixel count is checked pre-call so a
single page cannot blow the 8 GB RAM budget.

Also hosts the Y5.3 ``ple-vision-probe`` hardware checker and the CLI
handler that wires it into ``pipeline_cli.py``.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional


@dataclass(frozen=True)
class VisionExtractedTable:
    rows: list[list[str]]
    caption: str
    source_image: Path


def _pixel_count(path: Path) -> int:
    """Inspect an image's pixel count without fully decoding it."""
    from PIL import Image  # lazy import

    with Image.open(path) as im:
        w, h = im.size
    return int(w) * int(h)


def _call_ollama_vision(image_path: Path, *, model: str, prompt: str) -> str:
    """Invoke Ollama's vision API. Thin wrapper so tests can patch
    a single symbol without stubbing httpx internals.
    """
    import base64

    import httpx

    with Path(image_path).open("rb") as fh:
        b64 = base64.b64encode(fh.read()).decode("ascii")

    payload: dict[str, Any] = {
        "model": model,
        "prompt": prompt,
        "images": [b64],
        "stream": False,
    }
    resp = httpx.post(
        "http://localhost:11434/api/generate",
        json=payload,
        timeout=120.0,
    )
    resp.raise_for_status()
    data = resp.json()
    return str(data.get("response", ""))


_PROMPT = (
    "You are extracting a table from a page image. "
    "Return STRICT JSON with keys 'rows' (list of lists of strings) "
    "and 'caption' (string). "
    "Do NOT wrap the JSON in markdown. Do NOT include any explanation."
)


def extract_table_from_image(
    image_path: Path,
    *,
    model: str,
    max_pixels: int = 2_000_000,
) -> Optional[VisionExtractedTable]:
    """Extract a structured table from a rendered PDF page image.

    Returns ``None`` if the vision model produced an empty or
    unparseable response. Raises ``ValueError`` if the image exceeds
    ``max_pixels`` so the caller can rescale before retrying.
    """
    image_path = Path(image_path)
    if _pixel_count(image_path) > max_pixels:
        raise ValueError(
            f"{image_path.name} exceeds max_image_pixels ({max_pixels}) — "
            "rescale first"
        )

    raw = _call_ollama_vision(image_path, model=model, prompt=_PROMPT)
    if not raw.strip():
        return None

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return None

    rows = payload.get("rows")
    if not isinstance(rows, list) or not all(isinstance(r, list) for r in rows):
        return None

    return VisionExtractedTable(
        rows=[[str(c) for c in row] for row in rows],
        caption=str(payload.get("caption", "")),
        source_image=image_path,
    )


# ---------------------------------------------------------------------------
# Stream Y5.3 — ple-vision-probe hardware pre-flight
# ---------------------------------------------------------------------------
def _free_ram_gb() -> float:
    """Return free RAM in GB. Falls back to -1.0 when psutil is not
    installed (probe then reports "cannot measure" and fails safe).
    """
    try:
        import psutil  # type: ignore

        return psutil.virtual_memory().available / (1024 ** 3)
    except ImportError:
        return -1.0


def _ollama_model_available(name: str) -> bool:
    """Query ``/api/tags`` on the local Ollama server and check whether
    ``name``'s family (e.g. ``moondream``) is present. Returns ``False``
    on any connection error so the probe fails safe rather than falsely
    reporting the model exists.
    """
    try:
        import httpx

        r = httpx.get("http://localhost:11434/api/tags", timeout=5.0)
        r.raise_for_status()
        tags = r.json().get("models", [])
        family = name.split(":")[0]
        return any(str(m.get("name", "")).startswith(family) for m in tags)
    except Exception:
        return False


def run_ple_vision_probe(
    *,
    required_free_gb: float = 3.5,
    model: str = "moondream:latest",
) -> int:
    """Stream Y5.3 — CLI handler for ``ple-vision-probe``.

    Exit codes:
      * ``0`` — probe PASS (enough RAM, model pulled)
      * ``1`` — not enough free RAM
      * ``2`` — vision model not pulled on the local Ollama
      * ``3`` — psutil is not installed so RAM cannot be measured
    """
    free = _free_ram_gb()
    if free < 0:
        print("FAIL: psutil not installed — install with `pip install psutil`")
        return 3
    if free < required_free_gb:
        print(f"FAIL: only {free:.2f} GB free (need {required_free_gb:.2f})")
        return 1
    if not _ollama_model_available(model):
        print(
            f"FAIL: vision model '{model}' not pulled. "
            f"Run: ollama pull {model}"
        )
        return 2
    print(f"PASS: {free:.2f} GB free, {model} available")
    return 0
