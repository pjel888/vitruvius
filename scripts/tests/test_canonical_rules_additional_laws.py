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


def test_build_plan_matches_pd_1067_law_rule() -> None:
    plan = build_plan(
        '001-Laws/refined_markdown/PD-1067/PD 1067 - Water Code of the Philippines.md'
    )
    assert plan['title'] == 'Water Code of the Philippines'
    assert plan['prefix'] == 'law'
    assert plan['source_type'] == 'law'
    assert plan['trust'] == 'primary'


def test_build_plan_matches_pd_1067_amended_irr_rule() -> None:
    plan = build_plan(
        '001-Laws/refined_markdown/PD-1067/Water Code of PH IRR 2005.md'
    )
    assert plan['title'] == 'Amended Implementing Rules and Regulations of the Water Code of the Philippines'
    assert plan['prefix'] == 'irr'
    assert plan['source_type'] == 'irr'
    assert plan['trust'] == 'primary'


def test_build_plan_matches_pd_1151_law_rule() -> None:
    plan = build_plan(
        '001-Laws/refined_markdown/PD-1151/PD 1151 - PD 1152 Environmental Code.md'
    )
    assert plan['title'] == 'Philippine Environmental Policy'
    assert plan['prefix'] == 'law'
    assert plan['source_type'] == 'law'
    assert plan['trust'] == 'primary'


def test_build_plan_matches_ra_9003_law_rule() -> None:
    plan = build_plan(
        '001-Laws/refined_markdown/RA-9003/RA 9003 Ecological Solid Waste Management Act 2000.md'
    )
    assert plan['title'] == 'Ecological Solid Waste Management Act of 2000'
    assert plan['prefix'] == 'law'
    assert plan['source_type'] == 'law'
    assert plan['trust'] == 'primary'


def test_build_plan_matches_pd_1517_irr_rule() -> None:
    plan = build_plan(
        '001-Laws/refined_markdown/PD-1517/PD 1517_Urban Land Reform.md'
    )
    assert plan['title'] == 'Implementing Rules and Regulations of the Urban Land Reform Act'
    assert plan['prefix'] == 'irr'
    assert plan['source_type'] == 'irr'
    assert plan['trust'] == 'primary'


def test_build_plan_matches_ra_6969_law_rule() -> None:
    plan = build_plan(
        '001-Laws/refined_markdown/RA-6969/RA 6969 Toxic Substances and Hazardouse Nuclear Wastes Control Act 1990.md'
    )
    assert plan['title'] == 'Toxic Substances and Hazardous and Nuclear Wastes Control Act of 1990'
    assert plan['prefix'] == 'law'
    assert plan['source_type'] == 'law'
    assert plan['trust'] == 'primary'


def test_build_plan_matches_ra_10066_law_rule() -> None:
    plan = build_plan(
        '001-Laws/refined_markdown/RA-10066/ra 10066.md'
    )
    assert plan['title'] == 'National Cultural Heritage Act of 2009'
    assert plan['prefix'] == 'law'
    assert plan['source_type'] == 'law'
    assert plan['trust'] == 'primary'


def test_build_plan_matches_pd_856_law_rule() -> None:
    plan = build_plan(
        '001-Laws/refined_markdown/PD-856/phi201040.md'
    )
    assert plan['title'] == 'Code on Sanitation of the Philippines'
    assert plan['prefix'] == 'law'
    assert plan['source_type'] == 'law'
    assert plan['trust'] == 'primary'


def test_build_plan_matches_pd_856_food_establishments_irr_rule() -> None:
    plan = build_plan(
        '001-Laws/refined_markdown/PD-856/DOH Food Establishments.md'
    )
    assert plan['title'] == 'Implementing Rules and Regulations of Chapter III of the Code on Sanitation of the Philippines'
    assert plan['prefix'] == 'irr'
    assert plan['source_type'] == 'irr'
    assert plan['trust'] == 'primary'


def test_build_plan_matches_ra_7160_law_rule() -> None:
    plan = build_plan(
        '001-Laws/refined_markdown/RA-7160/RA 7160 The Local Government Code.md'
    )
    assert plan['title'] == 'Local Government Code of 1991'
    assert plan['prefix'] == 'law'
    assert plan['source_type'] == 'law'
    assert plan['trust'] == 'primary'


def test_build_plan_matches_ra_9275_law_rule_from_ra_9257_folder_file() -> None:
    plan = build_plan(
        '001-Laws/refined_markdown/RA-9257/RA 9275 PH Clean Water Act.md'
    )
    assert plan['title'] == 'Philippine Clean Water Act of 2004'
    assert plan['prefix'] == 'law'
    assert plan['source_type'] == 'law'
    assert plan['trust'] == 'primary'


def test_build_plan_matches_ra_4566_law_rule() -> None:
    plan = build_plan(
        '001-Laws/refined_markdown/RA-4566/RA_4566.md'
    )
    assert plan['title'] == "Contractors' License Law"
    assert plan['prefix'] == 'law'
    assert plan['source_type'] == 'law'
    assert plan['trust'] == 'primary'


def test_build_plan_matches_ra_386_law_rule() -> None:
    plan = build_plan(
        '001-Laws/refined_markdown/RA-386/RA-386 Civil Code.md'
    )
    assert plan['title'] == 'Civil Code of the Philippines'
    assert plan['prefix'] == 'law'
    assert plan['source_type'] == 'law'
    assert plan['trust'] == 'primary'


def test_build_plan_matches_ra_9184_law_rule() -> None:
    plan = build_plan(
        '001-Laws/refined_markdown/RA-9184/RA 9184 IRR - Government Procurement IRR.md'
    )
    assert plan['title'] == 'Government Procurement Reform Act'
    assert plan['prefix'] == 'law'
    assert plan['source_type'] == 'law'
    assert plan['trust'] == 'primary'


def test_build_plan_matches_ra_9184_updated_2016_irr_rule() -> None:
    plan = build_plan(
        '001-Laws/refined_markdown/RA-9184/Updated 2016 IRR_31 March 2021.md'
    )
    assert plan['title'] == 'Updated 2016 Revised Implementing Rules and Regulations of the Government Procurement Reform Act'
    assert plan['prefix'] == 'irr'
    assert plan['source_type'] == 'irr'
    assert plan['trust'] == 'primary'


def test_build_plan_matches_ra_1378_law_rule() -> None:
    plan = build_plan(
        '001-Laws/refined_markdown/RA-1378/MASTER PLUMBING LAW.md'
    )
    assert plan['title'] == 'Plumbing Law'
    assert plan['prefix'] == 'law'
    assert plan['source_type'] == 'law'
    assert plan['trust'] == 'primary'


def test_build_plan_matches_ra_9285_law_rule() -> None:
    plan = build_plan(
        '001-Laws/refined_markdown/RA-9285/RA_9285.md'
    )
    assert plan['title'] == 'Alternative Dispute Resolution Act of 2004'
    assert plan['prefix'] == 'law'
    assert plan['source_type'] == 'law'
    assert plan['trust'] == 'primary'


def test_build_plan_matches_ra_11201_law_rule() -> None:
    plan = build_plan(
        '001-Laws/refined_markdown/RA-11201/RA 11201 - DHSUD Act of 2019.md'
    )
    assert plan['title'] == 'Department of Human Settlements and Urban Development Act'
    assert plan['prefix'] == 'law'
    assert plan['source_type'] == 'law'
    assert plan['trust'] == 'primary'


def test_build_plan_matches_ra_11201_irr_rule() -> None:
    plan = build_plan(
        '001-Laws/refined_markdown/RA-11201/RA 11201 IRR - DHSUD Act Implementing Rules.md'
    )
    assert plan['title'] == 'Implementing Rules and Regulations of the Department of Human Settlements and Urban Development Act'
    assert plan['prefix'] == 'irr'
    assert plan['source_type'] == 'irr'
    assert plan['trust'] == 'primary'


def test_build_plan_matches_ra_11285_law_rule() -> None:
    plan = build_plan(
        '001-Laws/refined_markdown/RA-11285/RA 11285 - Energy Efficiency and Conservation Act 2019.md'
    )
    assert plan['title'] == 'Energy Efficiency and Conservation Act'
    assert plan['prefix'] == 'law'
    assert plan['source_type'] == 'law'
    assert plan['trust'] == 'primary'


def test_build_plan_matches_denr_dao_2003_30_irr_rule() -> None:
    plan = build_plan(
        '001-Laws/refined_markdown/DENR/DENR DAO 2003-30 - EIS System Implementing Rules.md'
    )
    assert plan['title'] == 'Implementing Rules and Regulations for the Philippine Environmental Impact Statement System'
    assert plan['prefix'] == 'irr'
    assert plan['source_type'] == 'irr'
    assert plan['trust'] == 'primary'


def test_build_plan_matches_doe_energy_conserving_design_guidelines_rule() -> None:
    plan = build_plan(
        '001-Laws/refined_markdown/DOE/DOE Guidelines on Energy Conserving Design on Buildings v2008.md'
    )
    assert plan['title'] == 'Guidelines on Energy Conserving Design of Buildings'
    assert plan['prefix'] == 'handout'
    assert plan['source_type'] == 'handout'
    assert plan['trust'] == 'primary'


def test_build_plan_matches_dpwh_do037_accessibility_order_rule() -> None:
    plan = build_plan(
        '001-Laws/refined_markdown/DPWH/DPWH DO037 Enforcement of BP344 along National Roads.md'
    )
    assert plan['title'] == 'Department Order No. 37 on Enforcement of the Accessibility Law Along National Roads'
    assert plan['prefix'] == 'handout'
    assert plan['source_type'] == 'handout'
    assert plan['trust'] == 'primary'
