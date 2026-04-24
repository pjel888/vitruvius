from vitruvius.relationships_sections import build_text_windows, extract_section_relationships, split_sections


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


def test_split_sections_handles_lettered_sections() -> None:
    text = (
        'Section A : Brief History\n\n'
        'Town history text.\n\n'
        'Section B. Human Resource\n\n'
        'Population text.\n'
    )
    sections = split_sections(text)
    assert [section['section_id'] for section in sections] == ['section-a', 'section-b']
    assert sections[0]['title'] == 'Brief History'
    assert 'Town history text.' in ' '.join(sections[0]['lines'])


def test_build_text_windows_splits_paragraphs_and_sentences() -> None:
    windows = build_text_windows([
        "Accessible ramps shall comply with the slope rule. Handrails shall be required.",
        "",
        "Short",
        "Means of egress shall comply with lighting requirements.",
    ])
    assert any("Accessible ramps shall comply" in window for window in windows)
    assert any("Means of egress shall comply" in window for window in windows)


def test_extract_section_relationships_uses_local_windows_not_whole_section() -> None:
    section = {
        "section_id": "section-1",
        "title": "Sample",
        "lines": [
            "Accessible ramps shall comply with accessibility requirements.",
            "",
            "This unrelated paragraph mentions stairs without a relation trigger.",
        ],
    }
    concept_map = {
        "accessible ramps": "concept-accessible-ramps",
        "stairs": "concept-stairs",
    }
    rels = extract_section_relationships(
        section,
        concept_map,
        source_id="irr-revised-implementing-rules-and-regulations-of-batas-pambansa-blg-344",
    )
    assert rels == [
        {
            "from": "irr-revised-implementing-rules-and-regulations-of-batas-pambansa-blg-344",
            "type": "governs",
            "to": "concept-accessible-ramps",
            "section": "section-1",
            "section_title": "Sample",
            "source_text": "Accessible ramps shall comply with accessibility requirements.",
        }
    ]


def test_extract_section_relationships_does_not_emit_concept_defines_concept() -> None:
    section = {
        "section_id": "section-1",
        "title": "Sample",
        "lines": [
            "Means of egress shall be stairs for this sample sentence.",
        ],
    }
    concept_map = {
        "means of egress": "concept-means-of-egress",
        "stairs": "concept-stairs",
    }
    rels = extract_section_relationships(
        section,
        concept_map,
        source_id="irr-revised-implementing-rules-and-regulations-of-batas-pambansa-blg-220",
    )
    assert rels == []
