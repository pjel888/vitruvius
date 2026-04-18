from __future__ import annotations

from pathlib import Path

from vitruvius.concept_candidate_suggestions import (
    extract_definition_style_terms,
    suggest_concept_candidates,
)


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')


def test_extract_definition_style_terms_captures_quoted_and_bare_means() -> None:
    text = '''
- (a) "Arbitration" means a voluntary dispute resolution process.
- (b) Chemical mixture means any combination of two or more chemical substances.
- SECTION 3. Definition of Terms.
'''
    assert extract_definition_style_terms(text) == ['Arbitration', 'Chemical mixture']


def test_suggest_concept_candidates_reports_matched_and_unmatched(tmp_path: Path) -> None:
    concepts = tmp_path / '003_Canonical-Knowledge-Layer' / 'shared' / 'concepts'
    _write(
        concepts / 'arbitration.md',
        '---\n'
        'title: Arbitration\n'
        'aliases:\n'
        '  - arbitration\n'
        '---\n',
    )
    refined = tmp_path / '002_Raw-Conversion-Layer' / '001-Laws' / 'refined_markdown' / 'RA-9285' / 'RA_9285.md'
    _write(
        refined,
        '\n'.join([
            '- (a) "Arbitration" means a voluntary dispute resolution process.',
            '- (b) "Mediator" means a person who conducts mediation.',
        ]),
    )
    payload = suggest_concept_candidates(
        repo_root=tmp_path,
        refined_markdown_path='001-Laws/refined_markdown/RA-9285/RA_9285.md',
    )
    assert payload['matched_existing_count'] == 1
    assert payload['unmatched_candidate_count'] == 1
    assert payload['matched_existing'][0]['concept_id'] == 'concept-arbitration'
    assert payload['unmatched_candidates'][0]['suggested_concept_id'] == 'concept-mediator'
