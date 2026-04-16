from pathlib import Path

from vitruvius.canonicalize import (
    extract_section_headers,
    extract_key_points,
    build_overview_paragraph,
)


FIXTURE = Path(__file__).parent / "fixtures" / "refined_pd_1096_sample.md"


def test_extract_section_headers_returns_coverage_items():
    text = FIXTURE.read_text(encoding="utf-8")
    headers = extract_section_headers(text)
    assert len(headers) == 4
    assert headers[0]["level"] == 2
    assert "Title" in headers[0]["title"]


def test_extract_key_points_returns_top_n_sentences():
    text = FIXTURE.read_text(encoding="utf-8")
    key_points = extract_key_points(text, limit=3)
    assert 1 <= len(key_points) <= 3
    assert all(len(kp) < 300 for kp in key_points)


def test_build_overview_paragraph_returns_first_non_header_para():
    text = FIXTURE.read_text(encoding="utf-8")
    overview = build_overview_paragraph(text)
    assert "National Building Code" in overview or "Decree" in overview
    assert not overview.startswith("#")


def test_build_overview_paragraph_skips_images_and_short_noise() -> None:
    text = (
        "![image 1](foo.png)\n"
        "\n"
        "Short line\n"
        "|Preface|\n"
        "This is the first substantial paragraph with enough words to be useful.\n"
    )
    overview = build_overview_paragraph(text)
    assert overview == "This is the first substantial paragraph with enough words to be useful."


def test_extract_section_headers_skips_tiny_noise_headers() -> None:
    text = "## M\n## Real Header\n### T\n### Another Real Header\n"
    headers = extract_section_headers(text)
    assert headers == [
        {"level": 2, "title": "Real Header"},
        {"level": 3, "title": "Another Real Header"},
    ]


def test_resolve_referenced_concepts_from_text(tmp_path):
    from vitruvius.canonicalize import resolve_referenced_concepts

    concepts_dir = tmp_path / "003_Canonical-Knowledge-Layer" / "shared" / "concepts"
    concepts_dir.mkdir(parents=True)
    for slug in ("occupancy-classification", "fire-resistive-construction", "building-permit"):
        (concepts_dir / f"{slug}.md").write_text(
            f"---\nid: concept-{slug}\ntitle: {slug}\npage_type: concept\n"
            "canonical_status: placeholder\n"
            "last_canonicalized_utc: 2026-04-14T00:00:00Z\n---\n",
            encoding="utf-8",
        )

    body = (
        "Every building shall be classified by occupancy classification. "
        "Fire-resistive construction is determined by occupancy. "
        "A building permit must be obtained before construction."
    )
    resolved = resolve_referenced_concepts(body, repo_root=tmp_path)
    assert "concept-occupancy-classification" in resolved
    assert "concept-fire-resistive-construction" in resolved
    assert "concept-building-permit" in resolved


def test_build_overview_paragraph_skips_isbn_url_and_toc_noise() -> None:
    text = (
        'ISBN 978-1-23-456789-0\n'
        'https://example.com/file.pdf\n'
        'TABLE OF CONTENTS\n'
        'This is the first substantial paragraph with enough words to be useful.\n'
    )
    overview = build_overview_paragraph(text)
    assert overview == 'This is the first substantial paragraph with enough words to be useful.'


def test_extract_key_points_skips_noise_lines() -> None:
    text = (
        '## Overview\n\n'
        'ISBN 978-1-23-456789-0\n'
        'GOVPH https://example.com\n'
        'This paragraph contains the actual meaningful sentence for the canonical source.\n'
    )
    key_points = extract_key_points(text, limit=2)
    assert key_points == ['This paragraph contains the actual meaningful sentence for the canonical source.']


def test_extract_section_headers_accepts_deeper_markdown_headings() -> None:
    text = '#### RULE I General Provisions\n##### Section 1. Scope of Application\n'
    headers = extract_section_headers(text)
    assert headers == [
        {"level": 4, "title": "RULE I General Provisions"},
        {"level": 5, "title": "Section 1. Scope of Application"},
    ]


def test_build_overview_paragraph_cleans_leading_ocr_fragment() -> None:
    text = 'n a country where tragic fires leave people devastated but not resolute in preventing them.\n'
    overview = build_overview_paragraph(text)
    assert overview == 'a country where tragic fires leave people devastated but not resolute in preventing them.'


def test_extract_key_points_cleans_leading_ocr_fragment() -> None:
    text = '## Message\n\ny heartfelt greetings to the Bureau of Fire Protection for the successful revision.\n'
    key_points = extract_key_points(text, limit=1)
    assert key_points == ['heartfelt greetings to the Bureau of Fire Protection for the successful revision.']


def test_extract_section_headers_skips_noise_heading_titles() -> None:
    text = '### GOVPH https://example.com\n#### EDUARDO M. ANO\n### Rule I General Provisions\n'
    headers = extract_section_headers(text)
    assert headers == [{"level": 3, "title": "Rule I General Provisions"}]


def test_build_overview_paragraph_prefers_sentence_over_all_caps_banner() -> None:
    text = (
        'REVISED RULES AND STANDARDS FOR ECONOMIC AND SOCIALIZED HOUSING PROJECTS\n'
        'Pursuant to Section 3 of BP 220, the Housing and Land Use Regulatory Board is authorized to establish and promulgate standards.\n'
    )
    overview = build_overview_paragraph(text)
    assert overview == 'Pursuant to Section 3 of BP 220, the Housing and Land Use Regulatory Board is authorized to establish and promulgate standards.'


def test_extract_section_headers_accepts_plain_section_lines_and_skips_toc_entries() -> None:
    text = (
        '- Section 1. Scope of Application 1\n'
        'Section 1. Scope of Application\n'
        'RULE II GENERAL PROVISIONS\n'
    )
    headers = extract_section_headers(text)
    assert headers == [
        {"level": 2, "title": "Section 1. Scope of Application"},
        {"level": 2, "title": "RULE II GENERAL PROVISIONS"},
    ]


def test_extract_section_headers_skips_named_message_headings() -> None:
    text = '###### EDUARDO M. AÑO\n###### SECRETARY EDUARDO M. AÑO\n#### DIVISION 4. COMMAND\n'
    headers = extract_section_headers(text)
    assert headers == [{"level": 4, "title": "DIVISION 4. COMMAND"}]


def test_extract_section_headers_skips_numbered_sentences() -> None:
    text = '1. Accessible Ramps\n1. For accessible ramps 3000 mm or more in width, provide intermediate handrails at the center.\n'
    headers = extract_section_headers(text)
    assert headers == [{"level": 2, "title": "1. Accessible Ramps"}]


def test_build_overview_paragraph_skips_headingish_bullets() -> None:
    text = (
        '- Section 3. Compliance with Standards and Guidelines 1\n'
        'Pursuant to Section 3 of BP 220, the Housing and Land Use Regulatory Board is authorized to establish and promulgate standards.\n'
    )
    overview = build_overview_paragraph(text)
    assert overview == 'Pursuant to Section 3 of BP 220, the Housing and Land Use Regulatory Board is authorized to establish and promulgate standards.'


def test_build_overview_paragraph_skips_bullet_table_lines() -> None:
    text = (
        '- Table 1 Parks and Playground Allocation 5\n'
        'Pursuant to Section 3 of BP 220, the Housing and Land Use Regulatory Board is authorized to establish and promulgate standards.\n'
    )
    overview = build_overview_paragraph(text)
    assert overview == 'Pursuant to Section 3 of BP 220, the Housing and Land Use Regulatory Board is authorized to establish and promulgate standards.'


def test_build_overview_paragraph_skips_bulleted_cover_inventory() -> None:
    text = (
        'INCLUDES\n'
        '- • NBCDO MEMORANDUM CIRCULAR NO. 1, s. 2004\n'
        'TABLE OF CONTENTS\n'
        'This implementing rules document governs building permits and occupancy classifications across the code.\n'
    )
    overview = build_overview_paragraph(text)
    assert overview == 'This implementing rules document governs building permits and occupancy classifications across the code.'


def test_build_overview_paragraph_skips_dot_leader_toc_lines() -> None:
    text = (
        'Foreword…………………………………………………………………….... vii\n'
        'Acknowledgement…………………………………………………………… viii\n'
        'This implementing rules document governs building permits and occupancy classifications across the code.\n'
    )
    overview = build_overview_paragraph(text)
    assert overview == 'This implementing rules document governs building permits and occupancy classifications across the code.'


def test_build_overview_paragraph_skips_all_caps_page_range_toc_lines() -> None:
    text = (
        'NEW SCHEDULE OF FEES AND OTHER CHARGES 254 - 270 NBC FORMS 272 - 341\n'
        'This implementing rules document governs building permits and occupancy classifications across the code.\n'
    )
    overview = build_overview_paragraph(text)
    assert overview == 'This implementing rules document governs building permits and occupancy classifications across the code.'


def test_extract_section_headers_skips_domain_noise_titles() -> None:
    text = '### National Council on Disability Affairs\n### Pambansang Sanggunian Ukol sa Ugnayang Pangmaykapansanan\n### Rule I General Provisions\n'
    headers = extract_section_headers(text)
    assert headers == [{"level": 3, "title": "Rule I General Provisions"}]


def test_extract_section_headers_skips_preface_before_first_structural_heading() -> None:
    text = (
        '### Revised Implementing Rules and Regulations\n'
        '### GOVPH\n'
        '### Rule I General Provisions\n'
        '### Section 1. Scope of Application\n'
    )
    headers = extract_section_headers(text)
    assert headers == [
        {"level": 3, "title": "Rule I General Provisions"},
        {"level": 3, "title": "Section 1. Scope of Application"},
    ]


def test_extract_section_headers_skips_sentence_like_definition_headers() -> None:
    text = '### Self-Closing Fire Doors (or Self-Closing Fire-Resistive Doors). Automatic closing doors that are\n### RULE 4. AUTHORITY OF THE CHIEF, BUREAU OF FIRE PROTECTION\n'
    headers = extract_section_headers(text)
    assert headers == [{"level": 3, "title": "RULE 4. AUTHORITY OF THE CHIEF, BUREAU OF FIRE PROTECTION"}]


def test_extract_section_headers_skips_table_caption_like_headings() -> None:
    text = '### Viewing Distance (m) Size of Symbol (mm)\n### 10. Stairs\n'
    headers = extract_section_headers(text)
    assert headers == [{"level": 3, "title": "10. Stairs"}]


def test_build_structured_source_file_prefers_structural_headers(tmp_path, monkeypatch) -> None:
    import vitruvius.canonicalize as canonicalize_mod

    refined = tmp_path / '002_Raw-Conversion-Layer' / 'sample.md'
    refined.parent.mkdir(parents=True)
    refined.write_text(
        '### Revised Implementing Rules and Regulations\n'
        '### RULE I GENERAL PROVISIONS\n'
        '### Section 1. Scope of Application\n'
        '### Viewing Distance (m) Size of Symbol (mm)\n',
        encoding='utf-8',
    )

    monkeypatch.setattr(canonicalize_mod, 'build_plan', lambda _p: {
        'title': 'Sample Source',
        'canonical_id': 'source-sample-source',
        'trust': 'primary',
        'aliases': [],
    })

    _target, content = canonicalize_mod.build_structured_source_file(
        repo_root=tmp_path,
        relative_markdown_path='sample.md',
    )
    assert '- RULE I GENERAL PROVISIONS' in content
    assert '- Section 1. Scope of Application' in content
    assert 'Viewing Distance (m) Size of Symbol (mm)' not in content
    assert 'Revised Implementing Rules and Regulations' not in content


def test_build_structured_source_file_keeps_medium_severity_overview(tmp_path, monkeypatch) -> None:
    import vitruvius.canonicalize as canonicalize_mod

    refined = tmp_path / '002_Raw-Conversion-Layer' / 'sample-medium.md'
    refined.parent.mkdir(parents=True)
    refined.write_text(
        'TABLE OF CONTENTS\n'
        + '\n'.join('| table row |' for _ in range(120))
        + '\nThis implementing rules document governs building permits and occupancy classifications across the code.\n'
        + '\n'.join('This section provides additional operative text for the medium-severity sample.' for _ in range(220))
        + '\n'
        + '## Section 1. Permit Requirements\n\nAll buildings must have permits.\n',
        encoding='utf-8',
    )

    monkeypatch.setattr(canonicalize_mod, 'build_plan', lambda _p: {
        'title': 'Sample Source',
        'canonical_id': 'source-sample-source',
        'trust': 'primary',
        'aliases': [],
    })

    _target, content = canonicalize_mod.build_structured_source_file(
        repo_root=tmp_path,
        relative_markdown_path='sample-medium.md',
    )
    assert 'This implementing rules document governs building permits and occupancy classifications across the code.' in content
    assert 'Automated summary withheld for Sample Source' not in content


def test_build_structured_source_file_withholds_high_severity_overview(tmp_path, monkeypatch) -> None:
    import vitruvius.canonicalize as canonicalize_mod

    refined = tmp_path / '002_Raw-Conversion-Layer' / 'sample-high.md'
    refined.parent.mkdir(parents=True)
    refined.write_text(
        'TABLE OF CONTENTS\n'
        + '\n'.join('| table row |' for _ in range(900))
        + '\nThis implementing rules document governs building permits and occupancy classifications across the code.\n'
        + '## Section 1. Permit Requirements\n\nAll buildings must have permits.\n',
        encoding='utf-8',
    )

    monkeypatch.setattr(canonicalize_mod, 'build_plan', lambda _p: {
        'title': 'Sample Source',
        'canonical_id': 'source-sample-source',
        'trust': 'primary',
        'aliases': [],
    })

    _target, content = canonicalize_mod.build_structured_source_file(
        repo_root=tmp_path,
        relative_markdown_path='sample-high.md',
    )
    assert 'Automated summary withheld for Sample Source' in content
    assert '(automated key points withheld because source-summary trust is low; review operative sections directly)' in content


def test_extract_section_headers_cleans_merged_heading_words() -> None:
    text = '###### SECTION 5.0.1.2 SOURCESThe Technical Staff may be drawn from the following:\n'
    headers = extract_section_headers(text)
    assert headers == [{"level": 6, "title": "SECTION 5.0.1.2 SOURCES The Technical Staff may be drawn from the following:"}]
