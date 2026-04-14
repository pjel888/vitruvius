from unittest.mock import patch

from vitruvius.ollama_review import warmup_model


def test_warmup_sends_one_generate_call():
    with patch("vitruvius.ollama_review.call_ollama") as mock_call:
        mock_call.return_value = '{"decision":"keep","confidence":0.1,"reason":"warmup","suggested_type":null}'
        result = warmup_model(model="gemma4:e4b", timeout_seconds=60)
        assert mock_call.call_count == 1
        args, kwargs = mock_call.call_args
        prompt = args[0] if args else kwargs.get("prompt")
        assert "warmup" in prompt.lower() or "ping" in prompt.lower()
        assert result is True


def test_warmup_returns_false_on_failure_but_does_not_raise():
    with patch("vitruvius.ollama_review.call_ollama", side_effect=RuntimeError("ollama down")):
        result = warmup_model(model="gemma4:e4b", timeout_seconds=60)
        assert result is False
