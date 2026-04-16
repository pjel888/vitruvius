from vitruvius.relationships_sections import split_sections


def test_split_sections_handles_markdown_heading_prefixes() -> None:
    text = (
        '### RULE I GENERAL PROVISIONS\n\n'
        '### Section 1. Scope of Application\n\n'
        'These rules apply.\n\n'
        '### Section 2. Declaration of Policies\n\n'
        'These policies apply.\n'
    )
    sections = split_sections(text)
    assert [section['section_id'] for section in sections] == ['section-1', 'section-2']
    assert sections[0]['title'] == 'Scope of Application'
    assert 'These rules apply.' in ' '.join(sections[0]['lines'])


def test_split_sections_skips_toc_entries_and_uses_real_heading() -> None:
    text = (
        '- Section 1. Scope of Application 1\n'
        '- Section 2. Declaration of Policies 2\n\n'
        '### Section 1. Scope of Application\n\n'
        'Actual section body.\n'
    )
    sections = split_sections(text)
    assert len(sections) == 1
    assert sections[0]['section_id'] == 'section-1'
    assert 'Actual section body.' in ' '.join(sections[0]['lines'])


def test_split_sections_handles_numbered_all_caps_heading() -> None:
    text = '1. GENERAL PROVISIONS\n\nAccessibility text.\n'
    sections = split_sections(text)
    assert len(sections) == 1
    assert sections[0]['section_id'] == 'section-1'
    assert sections[0]['title'] == 'GENERAL PROVISIONS'
