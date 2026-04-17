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


def test_build_plan_matches_ra_9266_irr_rule() -> None:
    plan = build_plan(
        '001-Laws/refined_markdown/RA-9266/RA-9266 IRR Architecture Act of 2004.md'
    )
    assert plan['title'] == 'Implementing Rules and Regulations of the Architecture Act of 2004'
    assert plan['prefix'] == 'irr'
    assert plan['source_type'] == 'irr'
    assert plan['trust'] == 'primary'


def test_build_plan_matches_pd_9514_file_to_ra_9514_irr_rule() -> None:
    plan = build_plan(
        '001-Laws/refined_markdown/PD-9514/PD 9514 - Fire Code of the Philippines.md'
    )
    assert plan['title'] == 'Implementing Rules and Regulations of the Fire Code of the Philippines'
    assert plan['prefix'] == 'irr'
    assert plan['source_type'] == 'irr'
    assert plan['trust'] == 'primary'


def test_build_plan_matches_eo_72_law_rule() -> None:
    plan = build_plan('001-Laws/refined_markdown/EO/EO 72 Comprehensive Land use.md')
    assert plan['title'] == 'Executive Order No. 72 on Comprehensive Land Use Plans'
    assert plan['prefix'] == 'law'
    assert plan['source_type'] == 'law'
    assert plan['trust'] == 'primary'


def test_build_plan_matches_eo_90_law_rule() -> None:
    plan = build_plan('001-Laws/refined_markdown/EO/EO 90 NGO for Shelter Program.md')
    assert plan['title'] == 'Executive Order No. 90 on the National Shelter Program'
    assert plan['prefix'] == 'law'
    assert plan['source_type'] == 'law'
    assert plan['trust'] == 'primary'


def test_build_plan_matches_eo_648_law_rule() -> None:
    plan = build_plan('001-Laws/refined_markdown/EO/EO 648 Chapter of the Human Settlements Regulatory Commissio.md')
    assert plan['title'] == 'Executive Order No. 648 Reorganizing the Human Settlements Regulatory Commission'
    assert plan['prefix'] == 'law'
    assert plan['source_type'] == 'law'
    assert plan['trust'] == 'primary'


def test_build_plan_matches_dhsud_open_space_guidelines_rule() -> None:
    plan = build_plan('001-Laws/refined_markdown/HLURB-DHSUD/Open Space Development Guidelines.md')
    assert plan['title'] == 'Open Space Development Guidelines'
    assert plan['prefix'] == 'handout'
    assert plan['source_type'] == 'handout'
    assert plan['trust'] == 'primary'


def test_build_plan_matches_dhsud_resilient_urban_guidelines_rule() -> None:
    plan = build_plan('001-Laws/refined_markdown/HLURB-DHSUD/Resilient Urban Design and Development Guidelines.md')
    assert plan['title'] == 'Resilient Urban Design and Development Guidelines'
    assert plan['prefix'] == 'handout'
    assert plan['source_type'] == 'handout'
    assert plan['trust'] == 'primary'


def test_build_plan_matches_ched_architecture_curriculum_standards_rule() -> None:
    plan = build_plan('001-Laws/refined_markdown/CHED/CHED CMO 61 Series 2017 - BS Architecture Curriculum Standards.md')
    assert plan['title'] == 'CMO 61 Series 2017 BS Architecture Curriculum Standards'
    assert plan['prefix'] == 'handout'
    assert plan['source_type'] == 'handout'
    assert plan['trust'] == 'primary'


def test_build_plan_matches_ciap_document_102_rule() -> None:
    plan = build_plan('001-Laws/refined_markdown/CIAP/CIAP-Document-102-Private-Constn-Contract.md')
    assert plan['title'] == 'CIAP Document 102 Uniform General Conditions of Contract for Private Construction'
    assert plan['prefix'] == 'handout'
    assert plan['source_type'] == 'handout'
    assert plan['trust'] == 'primary'


def test_build_plan_matches_uap_code_of_ethics_rule() -> None:
    plan = build_plan('001-Laws/refined_markdown/UAP/UAP Document Code of Ethics.md')
    assert plan['title'] == 'UAP Document Code of Ethics'
    assert plan['prefix'] == 'handout'
    assert plan['source_type'] == 'handout'
    assert plan['trust'] == 'primary'


def test_build_plan_matches_uap_spp_rule() -> None:
    plan = build_plan('001-Laws/refined_markdown/UAP/UAP Document Standards of Professional Practice.md')
    assert plan['title'] == 'UAP Document Standards of Professional Practice'
    assert plan['prefix'] == 'handout'
    assert plan['source_type'] == 'handout'
    assert plan['trust'] == 'primary'


def test_build_plan_matches_uap_document_301_rule() -> None:
    plan = build_plan('001-Laws/refined_markdown/UAP/UAP Document 301.md')
    assert plan['title'] == 'UAP Document 301 General Conditions'
    assert plan['prefix'] == 'handout'
    assert plan['source_type'] == 'handout'
    assert plan['trust'] == 'primary'


def test_build_plan_matches_doh_guidelines_for_health_facilities_rule() -> None:
    plan = build_plan('001-Laws/refined_markdown/DOH/DOH Guidelines for Health Facilities 20004.md')
    assert plan['title'] == 'DOH Guidelines for Health Facilities'
    assert plan['prefix'] == 'handout'
    assert plan['source_type'] == 'handout'
    assert plan['trust'] == 'primary'


def test_build_plan_matches_deped_drrr_manual_rule() -> None:
    plan = build_plan('001-Laws/refined_markdown/DEPED/DepEd DRRR Manual Philippines.md')
    assert plan['title'] == 'DepEd Disaster Risk Reduction Resource Manual'
    assert plan['prefix'] == 'handout'
    assert plan['source_type'] == 'handout'
    assert plan['trust'] == 'primary'


def test_build_plan_matches_san_mateo_zoning_ordinance_rule() -> None:
    plan = build_plan('001-Laws/refined_markdown/LGU/794216046-San-Mateo-Zoning-Ordinance.md')
    assert plan['title'] == 'Zoning Ordinance of the Municipality of San Mateo'
    assert plan['prefix'] == 'law'
    assert plan['source_type'] == 'law'
    assert plan['trust'] == 'primary'


def test_build_plan_matches_san_mateo_clup_rule() -> None:
    plan = build_plan('001-Laws/refined_markdown/LGU/844057380-Copy-of-San-Mateo-Rizal-clup.md')
    assert plan['title'] == 'San Mateo Comprehensive Land Use Plan 2021-2031'
    assert plan['prefix'] == 'handout'
    assert plan['source_type'] == 'handout'
    assert plan['trust'] == 'primary'


def test_build_plan_matches_dagupan_zoning_ordinance_rule() -> None:
    plan = build_plan('001-Laws/refined_markdown/LGU/756628009-Dagupan-City-Ordinance-no-2061-2016.md')
    assert plan['title'] == 'Comprehensive Zoning Ordinance of Dagupan City'
    assert plan['prefix'] == 'law'
    assert plan['source_type'] == 'law'
    assert plan['trust'] == 'primary'


def test_build_plan_matches_malolos_zoning_ordinance_rule() -> None:
    plan = build_plan('001-Laws/refined_markdown/LGU/700996086-Malolos-City-Zoning-Ordinance.md')
    assert plan['title'] == 'Zoning Ordinance of the City of Malolos'
    assert plan['prefix'] == 'law'
    assert plan['source_type'] == 'law'
    assert plan['trust'] == 'primary'


def test_build_plan_matches_meycauayan_zoning_ordinance_rule() -> None:
    plan = build_plan('001-Laws/refined_markdown/LGU/622896675-275447696-Zoning-Ordinances-Meycauayan-Bulacan.md')
    assert plan['title'] == 'Comprehensive Zoning Ordinance of the Municipality of Meycauayan'
    assert plan['prefix'] == 'law'
    assert plan['source_type'] == 'law'
    assert plan['trust'] == 'primary'


def test_build_plan_matches_davao_clup_rule() -> None:
    plan = build_plan('001-Laws/refined_markdown/LGU/253090760-Zoning-Davao-City.md')
    assert plan['title'] == 'Davao City Comprehensive Land Use Plan'
    assert plan['prefix'] == 'handout'
    assert plan['source_type'] == 'handout'
    assert plan['trust'] == 'primary'


def test_build_plan_matches_tarlac_zoning_ordinance_rule() -> None:
    plan = build_plan('001-Laws/refined_markdown/LGU/289088479-Tarlac-Zoning-Ordinances.md')
    assert plan['title'] == 'Comprehensive Zoning Ordinance of the City of Tarlac'
    assert plan['prefix'] == 'law'
    assert plan['source_type'] == 'law'
    assert plan['trust'] == 'primary'


def test_build_plan_matches_qc_cbd_zoning_ordinance_rule() -> None:
    plan = build_plan('001-Laws/refined_markdown/LGU/437459910-Ordinance-No-2117.md')
    assert plan['title'] == 'Quezon City Central Business District Zoning Ordinance'
    assert plan['prefix'] == 'law'
    assert plan['source_type'] == 'law'
    assert plan['trust'] == 'primary'
