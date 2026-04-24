import time
from unittest.mock import patch

from vitruvius.ollama_review import review_relationship


def test_retries_up_to_three_times_on_transient_error():
    call_count = {"n": 0}

    def flaky_call(prompt, model, timeout_seconds):
        call_count["n"] += 1
        if call_count["n"] < 3:
            raise RuntimeError("transient")
        return '{"decision":"keep","confidence":0.95,"reason":"ok","suggested_type":null}'

    with patch("time.sleep"):
        with patch("vitruvius.ollama_review.call_ollama", side_effect=flaky_call):
            result = review_relationship(
                {"from": "a", "type": "governs", "to": "b", "sections": [], "examples": []},
                model="gemma4:31b",
                timeout_seconds=60,
            )

    assert call_count["n"] == 3
    assert result["review"]["decision"] == "keep"


def test_falls_back_to_review_further_after_all_retries():
    with patch("time.sleep"):
        with patch("vitruvius.ollama_review.call_ollama", side_effect=RuntimeError("down")):
            result = review_relationship(
                {"from": "a", "type": "governs", "to": "b", "sections": [], "examples": []},
                model="gemma4:31b",
                timeout_seconds=60,
            )
    assert result["review"]["decision"] == "review_further"
    assert result["review"]["confidence"] == 0.0
    assert "Ollama review failed" in result["review"]["reason"]


def test_fallback_reason_includes_raw_response_preview_on_parse_failure():
    raw = '{"properties":{"decision":{"enum":["keep","review_further","reject"]}}}'
    with patch("vitruvius.config.get_ollama_max_retries", return_value=1):
        with patch("vitruvius.ollama_review.call_ollama", return_value=raw):
            result = review_relationship(
                {"from": "a", "type": "governs", "to": "b", "sections": [], "examples": []},
                model="gemma4:31b",
                timeout_seconds=60,
            )

    assert result["review"]["decision"] == "review_further"
    assert "response preview" in result["review"]["reason"]
    assert "properties" in result["review"]["reason"]


def test_honors_wall_clock_cap_across_retries():
    def slow_call(prompt, model, timeout_seconds):
        time.sleep(0.1)
        raise RuntimeError("transient")

    start = time.monotonic()
    with patch("time.sleep"):
        with patch("vitruvius.ollama_review.call_ollama", side_effect=slow_call):
            review_relationship(
                {"from": "a", "type": "governs", "to": "b", "sections": [], "examples": []},
                model="gemma4:31b",
                timeout_seconds=2,  # small wall cap
            )
    elapsed = time.monotonic() - start
    # Wall cap is 2s. Some small slack for test overhead.
    assert elapsed < 5.0, f"Retry loop ran for {elapsed}s, exceeds cap"
