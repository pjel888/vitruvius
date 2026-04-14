import warnings

from vitruvius.utils import normalize_filename, normalize_text


def test_normalize_text_matches_historical_behavior():
    # Legacy contract was " ".join(text.split()): collapse whitespace.
    # Suppress the DeprecationWarning here — this test is specifically
    # verifying the legacy behavior, not whether the deprecation fires.
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        assert normalize_text("hello    world") == "hello world"


def test_normalize_text_emits_deprecation_warning():
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        normalize_text("abc")
        messages = [str(w.message) for w in caught if issubclass(w.category, DeprecationWarning)]
    assert any("normalize_text" in m for m in messages)


def test_normalize_filename_emits_deprecation_warning():
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        normalize_filename("Foo-Bar.PDF")
        messages = [str(w.message) for w in caught if issubclass(w.category, DeprecationWarning)]
    assert any("normalize_filename" in m for m in messages)


def test_normalize_filename_still_lowercases_and_strips_nonalnum():
    # Preserved signature and behavior.
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        assert normalize_filename("Foo-Bar.PDF") == "foobar.pdf"
