from unittest.mock import patch

from vitruvius.concepts import run_canonicalize_concept_one


def test_generated_concept_has_placeholder_status(tmp_path):
    with patch("vitruvius.concepts.get_repo_root", return_value=tmp_path):
        rc = run_canonicalize_concept_one(concept_name="New Concept For Test")
    assert rc == 0

    target = tmp_path / "003_Canonical-Knowledge-Layer" / "shared" / "concepts" / "new-concept-for-test.md"
    assert target.exists()

    content = target.read_text(encoding="utf-8")
    assert "canonical_status: placeholder" in content
    assert "concept_status: placeholder" in content
    assert "page_type: concept" in content
