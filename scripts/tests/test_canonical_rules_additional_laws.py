from vitruvius.canonicalize import build_plan


def test_build_plan_matches_ra_9514_rirr_rule() -> None:
    plan = build_plan('001-Laws/raw_markdown/RA-9514/RA9514-RIRR-rev-2019.md')
    assert plan['title'] == 'Implementing Rules and Regulations of the Fire Code of the Philippines'
    assert plan['prefix'] == 'irr'
    assert plan['source_type'] == 'irr'
    assert plan['trust'] == 'primary'


def test_build_plan_matches_bp_220_rirr_rule() -> None:
    plan = build_plan('001-Laws/raw_markdown/BP-220/Revised_IRR_BP220_2008.md')
    assert plan['title'] == 'Revised Implementing Rules and Regulations of Batas Pambansa Blg. 220'
    assert plan['prefix'] == 'irr'
    assert plan['source_type'] == 'irr'
    assert plan['trust'] == 'primary'


def test_build_plan_matches_bp_344_primary_variant_rule() -> None:
    plan = build_plan(
        '001-Laws/raw_markdown/BP-344/2024 Revised Implementing Rules and Regulations Batas Pambansa Blg. 344 _ National Council on Disability Affairs.md'
    )
    assert plan['title'] == 'Revised Implementing Rules and Regulations of Batas Pambansa Blg. 344'
    assert plan['prefix'] == 'irr'
    assert plan['source_type'] == 'irr'
    assert plan['trust'] == 'primary'


def test_build_plan_matches_pd_957_irr_rule() -> None:
    plan = build_plan(
        '001-Laws/refined_markdown/PD-957/PD 957 IRR - Subdivision and Condominium IRR.md'
    )
    assert plan['title'] == 'Revised Implementing Rules and Regulations for PD 957'
    assert plan['prefix'] == 'irr'
    assert plan['source_type'] == 'irr'
    assert plan['trust'] == 'primary'


def test_build_plan_matches_pd_1185_law_rule() -> None:
    plan = build_plan(
        '001-Laws/refined_markdown/PD-1185/PD 1185 - Fire Code of the Philippines 1977.md'
    )
    assert plan['title'] == 'Fire Code of the Philippines'
    assert plan['prefix'] == 'law'
    assert plan['source_type'] == 'law'
    assert plan['trust'] == 'primary'


def test_build_plan_matches_pd_1216_law_rule() -> None:
    plan = build_plan(
        '001-Laws/refined_markdown/PD-1216/PD 1216 - Open Space Requirements in Subdivisions.md'
    )
    assert plan['title'] == 'Open Space Requirements in Residential Subdivisions'
    assert plan['prefix'] == 'law'
    assert plan['source_type'] == 'law'
    assert plan['trust'] == 'primary'


def test_build_plan_matches_ra_7279_law_rule() -> None:
    plan = build_plan(
        '001-Laws/refined_markdown/RA-7279/RA 7279 Urban Development and Housing Act 2009.md'
    )
    assert plan['title'] == 'Urban Development and Housing Act'
    assert plan['prefix'] == 'law'
    assert plan['source_type'] == 'law'
    assert plan['trust'] == 'primary'


def test_build_plan_matches_ra_4726_law_rule() -> None:
    plan = build_plan(
        '001-Laws/refined_markdown/RA-4726/RA 4726 Condominium Act.md'
    )
    assert plan['title'] == 'Condominium Act'
    assert plan['prefix'] == 'law'
    assert plan['source_type'] == 'law'
    assert plan['trust'] == 'primary'


def test_build_plan_matches_ra_7899_law_rule() -> None:
    plan = build_plan(
        '001-Laws/refined_markdown/RA-7899/RA 7899 Amendments to RA 4726.md'
    )
    assert plan['title'] == 'Amendments to the Condominium Act'
    assert plan['prefix'] == 'law'
    assert plan['source_type'] == 'law'
    assert plan['trust'] == 'primary'
