from vitruvius.normalization import NormalizationEngine, NormalizationRule


class _NoopA:
    name = "noop-a"
    tier = "A"
    phase = 1
    scope = ["document_text"]
    gated_by: list[str] = []
    is_deterministic = True

    def apply(self, text: str) -> str:
        return text


class _UpperCaseA:
    name = "upper-a"
    tier = "A"
    phase = 1
    scope = ["document_text"]
    gated_by: list[str] = []
    is_deterministic = True

    def apply(self, text: str) -> str:
        return text.upper()


def test_engine_registers_and_lists_rules():
    engine = NormalizationEngine()
    engine.register(_NoopA())
    engine.register(_UpperCaseA())
    names = [r.name for r in engine.rules]
    assert "noop-a" in names
    assert "upper-a" in names


def test_engine_applies_rules_in_phase_order():
    engine = NormalizationEngine()
    engine.register(_UpperCaseA())
    result, audit = engine.run("hello world", scope="document_text")
    assert result == "HELLO WORLD"
    assert len(audit) == 1
    assert audit[0]["rule"] == "upper-a"


def test_engine_skips_rules_outside_scope():
    engine = NormalizationEngine()
    engine.register(_UpperCaseA())
    result, audit = engine.run("hello", scope="filename")
    assert result == "hello"  # unchanged
    assert audit == []


def test_engine_is_idempotent_for_deterministic_rules():
    engine = NormalizationEngine()
    engine.register(_UpperCaseA())
    once, _ = engine.run("hello", scope="document_text")
    twice, _ = engine.run(once, scope="document_text")
    assert once == twice
