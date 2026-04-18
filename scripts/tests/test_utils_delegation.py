import warnings

import pytest

from vitruvius.utils import assert_windows_safe_path, normalize_filename, normalize_text


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


def test_assert_windows_safe_path_accepts_safe_segments():
    assert str(assert_windows_safe_path("004_Derived-Content-Layer/graph-visualizations/demo/run.html")) == (
        "004_Derived-Content-Layer/graph-visualizations/demo/run.html"
    )


def test_assert_windows_safe_path_rejects_forbidden_segment_chars():
    with pytest.raises(ValueError, match="Windows-forbidden filename characters"):
        assert_windows_safe_path('004_Derived-Content-Layer/graph-visualizations/demo:bad/run.html')
