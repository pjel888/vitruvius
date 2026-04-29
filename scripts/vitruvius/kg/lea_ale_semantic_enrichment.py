
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

GENERATION_METHOD = (
    "steward_governed_lea_ale_semantic_enrichment_from_kimi_guided_public_"
    "philippine_architecture_licensure_sources"
)
OWNER = "Philip Lewis"
RELEASE_VERSION = "0.7.0"
SCOPE_NOTE = (
    "Kimi-guided Philippine LEA/ALE semantic enrichment using official/public source-family "
    "metadata, raw-source filename inventory signals, and steward-authored original summaries; "
    "metadata only, no protected source payloads, exam questions, answer keys, clauses, tables, "
    "figures, diagrams, reviewer text, or code provisions stored."
)
RAW_SOURCE_RIGHTS_CLASSIFICATION = [
    {
        "path": "001_Raw-Source-Layer/001-Laws/test/ALE - Building Laws Cross-Reference Table (Pedro Santos Jr).xlsx",
        "classification": "private_or_third_party_exam_prep_reference",
        "allowed_use": "filename metadata and high-level topic signal only; no spreadsheet payload ingest",
        "source_id": "SRC-RAW-ALE-BUILDING-LAWS-XLSX",
    },
    {
        "path": "001_Raw-Source-Layer/004-Technology/ALE BT REVIEWER.pdf",
        "classification": "private_or_third_party_reviewer_pdf",
        "allowed_use": "filename metadata and high-level topic signal only; no reviewer text, questions, answer keys, diagrams, or tables ingested",
        "source_id": "SRC-RAW-ALE-BT-REVIEWER-PDF",
    },
    {
        "path": "001_Raw-Source-Layer/004-Technology/Building Technology June 2010 ALE.pdf",
        "classification": "private_or_third_party_exam_or_reviewer_pdf",
        "allowed_use": "filename metadata and high-level topic signal only; no exam payload, reviewer text, questions, answer keys, diagrams, or tables ingested",
        "source_id": "SRC-RAW-ALE-BT-JUNE-2010-PDF",
    },
]

SOURCE_REFERENCES: list[dict[str, str]] = [
    {"source_id": "SRC-PRC-ARCHITECTURE-BOARD", "source_family": "PRC Professional Regulatory Board of Architecture public information", "publisher_authority": "Professional Regulation Commission", "official_url": "https://www.prc.gov.ph/profession/architecture", "intended_vitruvius_use": "metadata-only architecture board, licensure, registration, and professional practice source-family reference"},
    {"source_id": "SRC-PRC-ALE-TOS", "source_family": "PRC Architecture Licensure Examination table of specifications and official exam framing metadata", "publisher_authority": "Professional Regulation Commission / Professional Regulatory Board of Architecture", "official_url": "https://www.prc.gov.ph/profession/architecture", "intended_vitruvius_use": "metadata-only ALE/BLEA/LEA subject framing, exam authority, and licensure-domain crosswalks"},
    {"source_id": "SRC-RA-9266-ARCHITECTURE-ACT", "source_family": "Republic Act No. 9266 Architecture Act of 2004", "publisher_authority": "Republic of the Philippines / LawPhil", "official_url": "https://lawphil.net/statutes/repacts/ra2004/ra_9266_2004.html", "intended_vitruvius_use": "metadata-only architecture practice, examination, registration, scope, signing/sealing, and professional responsibility crosswalks"},
    {"source_id": "SRC-RA-9266-IRR-METADATA", "source_family": "Implementing Rules and Regulations of R.A. 9266", "publisher_authority": "Professional Regulation Commission / Professional Regulatory Board of Architecture", "official_url": "https://www.prc.gov.ph/uploaded/documents/ARCHITECTURE%20LAW.PDF", "intended_vitruvius_use": "metadata-only IRR source-family reference for architecture practice and documentation topics"},
    {"source_id": "SRC-CHED-CMO-61-2017-BS-ARCH", "source_family": "CHED CMO No. 61 series 2017 Policies Standards and Guidelines for BS Architecture", "publisher_authority": "Commission on Higher Education", "official_url": "https://ched.gov.ph/wp-content/uploads/2017/10/CMO-61-s.-2017.pdf", "intended_vitruvius_use": "metadata-only architecture curriculum, education, and licensure-preparation topic crosswalks"},
    {"source_id": "SRC-PD-1096-NBCP", "source_family": "Presidential Decree No. 1096 National Building Code of the Philippines", "publisher_authority": "Republic of the Philippines / LawPhil", "official_url": "https://lawphil.net/statutes/presdecs/pd1977/pd_1096_1977.html", "intended_vitruvius_use": "metadata-only building code administration, permits, occupancy, construction type, site controls, and building planning crosswalks"},
    {"source_id": "SRC-PD-1096-REVISED-IRR-METADATA", "source_family": "2004 Revised IRR of P.D. 1096 and DPWH NBCDO public metadata", "publisher_authority": "Department of Public Works and Highways", "official_url": "https://dpwh.architectureboard.com.ph/documents/", "intended_vitruvius_use": "metadata-only National Building Code IRR and referral-code crosswalks; no code tables or clauses stored"},
    {"source_id": "SRC-RA-9514-FIRE-CODE", "source_family": "Republic Act No. 9514 Revised Fire Code of the Philippines of 2008", "publisher_authority": "Republic of the Philippines / LawPhil", "official_url": "https://lawphil.net/statutes/repacts/ra2008/ra_9514_2008.html", "intended_vitruvius_use": "metadata-only fire prevention, suppression, BFP approval, fire safety inspection, and life-safety topic crosswalks"},
    {"source_id": "SRC-BP-344-ACCESSIBILITY-LAW", "source_family": "Batas Pambansa Blg. 344 Accessibility Law and NCDA public IRR metadata", "publisher_authority": "Republic of the Philippines / National Council on Disability Affairs", "official_url": "https://lawphil.net/statutes/bataspam/bp1983/bp_344_1983.html; https://ncda.gov.ph/disability-laws/implementing-rules-and-regulations-irr/irr-of-bp-344/", "intended_vitruvius_use": "metadata-only accessibility, barrier-free route, ramp, parking, toilet, signage, and public-building compliance crosswalks"},
    {"source_id": "SRC-PD-1067-WATER-CODE", "source_family": "Presidential Decree No. 1067 Water Code of the Philippines", "publisher_authority": "Republic of the Philippines / LawPhil", "official_url": "https://lawphil.net/statutes/presdecs/pd1976/pd_1067_1976.html", "intended_vitruvius_use": "metadata-only water rights, drainage, easements, waterways, flood constraints, and site-planning crosswalks"},
    {"source_id": "SRC-PD-856-SANITATION-CODE", "source_family": "Presidential Decree No. 856 Code on Sanitation of the Philippines", "publisher_authority": "Republic of the Philippines / LawPhil", "official_url": "https://lawphil.net/statutes/presdecs/pd1975/pd_856_1975.html", "intended_vitruvius_use": "metadata-only sanitation, public health, ventilation, toilets, solid waste, water supply, and building health crosswalks"},
    {"source_id": "SRC-RA-7160-LOCAL-GOVERNMENT-CODE", "source_family": "Republic Act No. 7160 Local Government Code of 1991", "publisher_authority": "Republic of the Philippines / LawPhil", "official_url": "https://lawphil.net/statutes/repacts/ra1991/ra_7160_1991.html", "intended_vitruvius_use": "metadata-only local code adoption, zoning, land-use, locational-clearance, and LGU permitting crosswalks"},
    {"source_id": "SRC-DHSUD-HLURB-CLUP-GUIDEBOOKS", "source_family": "DHSUD/HLURB Comprehensive Land Use Plan and Zoning Ordinance guidebooks", "publisher_authority": "Department of Human Settlements and Urban Development / former HLURB", "official_url": "https://dhsud.gov.ph/wp-content/uploads/Publication/Guidebooks/HLURB_CLUP_Vol_1.pdf; https://www.dhsud.gov.ph/wp-content/uploads/Publication/Guidebooks/HLURB_CLUP_Vol_2.pdf; https://www.dhsud.gov.ph/wp-content/uploads/Publication/Guidebooks/HLURB_CLUP_Vol_3.pdf", "intended_vitruvius_use": "metadata-only CLUP, zoning ordinance, development control, and land-use planning crosswalks"},
    {"source_id": "SRC-RA-10066-HERITAGE-ACT", "source_family": "Republic Act No. 10066 National Cultural Heritage Act of 2009", "publisher_authority": "Republic of the Philippines / LawPhil", "official_url": "https://lawphil.net/statutes/repacts/ra2010/ra_10066_2010.html", "intended_vitruvius_use": "metadata-only built heritage, conservation, adaptive reuse, heritage zones, and Philippine architecture history crosswalks"},
    {"source_id": "SRC-NCCA-NATIONAL-ARTISTS-ARCHITECTURE", "source_family": "NCCA National Artists for Architecture and Allied Arts public metadata", "publisher_authority": "National Commission for Culture and the Arts", "official_url": "https://ncca.gov.ph/about-culture-and-arts/culture-profile/national-artists-of-the-philippines/", "intended_vitruvius_use": "metadata-only Filipino architect, national artist, work, and movement crosswalks"},
    {"source_id": "SRC-UAP-SPP-CODE-ETHICS-METADATA", "source_family": "UAP Standards of Professional Practice and Code of Ethics public metadata", "publisher_authority": "United Architects of the Philippines / IAPOA context", "official_url": "https://www.united-architects.org/", "intended_vitruvius_use": "metadata-only professional practice, ethics, services, and agreement topic crosswalks; no protected SPP payload stored"},
    {"source_id": "SRC-CIAP-DOCUMENT-102", "source_family": "CIAP Document 102 Uniform General Conditions of Contract for Private Construction", "publisher_authority": "Construction Industry Authority of the Philippines", "official_url": "https://construction.gov.ph/ciap-document-102-2/", "intended_vitruvius_use": "metadata-only construction contract, closeout, as-built, O&M, warranty, payment, claims, and private construction administration crosswalks"},
    {"source_id": "SRC-RA-9184-GPRA", "source_family": "Republic Act No. 9184 Government Procurement Reform Act", "publisher_authority": "Republic of the Philippines / LawPhil", "official_url": "https://lawphil.net/statutes/repacts/ra2003/ra_9184_2003.html", "intended_vitruvius_use": "metadata-only public bidding, procurement, infrastructure project delivery, contract award, and acceptance crosswalks"},
    {"source_id": "SRC-NSCP-METADATA", "source_family": "National Structural Code of the Philippines source-family metadata", "publisher_authority": "Association of Structural Engineers of the Philippines / source-rights review required", "official_url": "metadata-only reference; verify edition and license before any source admission", "intended_vitruvius_use": "metadata-only structural conceptualization, loads, seismic, wind, and nonstructural coordination labels; no protected standard text stored"},
    {"source_id": "SRC-PEC-METADATA", "source_family": "Philippine Electrical Code source-family metadata", "publisher_authority": "Institute of Integrated Electrical Engineers of the Philippines / source-rights review required", "official_url": "metadata-only reference; verify edition and license before any source admission", "intended_vitruvius_use": "metadata-only electrical systems, grounding, emergency power, lighting, and permit labels; no protected code text stored"},
    {"source_id": "SRC-NATIONAL-PLUMBING-CODE-METADATA", "source_family": "National Plumbing Code of the Philippines source-family metadata", "publisher_authority": "National Master Plumbers Association / source-rights review required", "official_url": "metadata-only reference; verify edition and license before any source admission", "intended_vitruvius_use": "metadata-only plumbing, sanitary drainage, water supply, fixture, backflow, and inspection labels; no protected code text stored"},
    {"source_id": "SRC-PHILIPPINE-GREEN-BUILDING-CODE", "source_family": "Philippine Green Building Code public metadata", "publisher_authority": "Department of Public Works and Highways", "official_url": "https://dpwh.gov.ph/DPWH/references/laws_codes_orders/pgbc", "intended_vitruvius_use": "metadata-only green building, passive design, energy, water, material, site, and indoor environmental quality crosswalks"},
    {"source_id": "SRC-PD-957-SUBDIVISION-CONDOMINIUM", "source_family": "Presidential Decree No. 957 Subdivision and Condominium Buyers' Protective Decree", "publisher_authority": "Republic of the Philippines / LawPhil", "official_url": "https://lawphil.net/statutes/presdecs/pd1976/pd_957_1976.html", "intended_vitruvius_use": "metadata-only housing, subdivision, condominium, land-use, open space, and development-control crosswalks"},
    {"source_id": "SRC-RA-386-CIVIL-CODE-CONSTRUCTION", "source_family": "Republic Act No. 386 Civil Code construction-adjacent obligations metadata", "publisher_authority": "Republic of the Philippines / LawPhil", "official_url": "https://lawphil.net/statutes/repacts/ra1949/ra_386_1949.html", "intended_vitruvius_use": "metadata-only civil obligations, nuisance, property, easement, liability, and construction-administration crosswalks"},
    {"source_id": "SRC-DENR-DAO-2003-30-EIS", "source_family": "DENR DAO 2003-30 Philippine Environmental Impact Statement System public metadata", "publisher_authority": "Department of Environment and Natural Resources / Environmental Management Bureau", "official_url": "https://emb.gov.ph/wp-content/uploads/2015/09/DAO-2003-30.pdf", "intended_vitruvius_use": "metadata-only environmental impact, ECC, site planning, and project applicability crosswalks"},
    {"source_id": "SRC-RAW-ALE-BUILDING-LAWS-XLSX", "source_family": "Local raw-source filename metadata for ALE building laws cross-reference spreadsheet", "publisher_authority": "Unknown third-party / rights review required", "official_url": "local custody path only: 001_Raw-Source-Layer/001-Laws/test/ALE - Building Laws Cross-Reference Table (Pedro Santos Jr).xlsx", "intended_vitruvius_use": "metadata-only raw-source inventory signal; no spreadsheet cells, questions, answer keys, reviewer text, clauses, or tables ingested"},
    {"source_id": "SRC-RAW-ALE-BT-REVIEWER-PDF", "source_family": "Local raw-source filename metadata for ALE building technology reviewer PDF", "publisher_authority": "Unknown third-party / rights review required", "official_url": "local custody path only: 001_Raw-Source-Layer/004-Technology/ALE BT REVIEWER.pdf", "intended_vitruvius_use": "metadata-only raw-source inventory signal; no PDF payload, reviewer text, questions, answer keys, figures, diagrams, or tables ingested"},
    {"source_id": "SRC-RAW-ALE-BT-JUNE-2010-PDF", "source_family": "Local raw-source filename metadata for Building Technology June 2010 ALE PDF", "publisher_authority": "Unknown third-party / rights review required", "official_url": "local custody path only: 001_Raw-Source-Layer/004-Technology/Building Technology June 2010 ALE.pdf", "intended_vitruvius_use": "metadata-only raw-source inventory signal; no PDF payload, exam questions, answer keys, reviewer text, figures, diagrams, or tables ingested"},
]

SOURCE_NODE_SUFFIXES = {
    "SRC-PRC-ARCHITECTURE-BOARD": "PRC",
    "SRC-PRC-ALE-TOS": "TOS",
    "SRC-RA-9266-ARCHITECTURE-ACT": "RAA",
    "SRC-RA-9266-IRR-METADATA": "AIR",
    "SRC-CHED-CMO-61-2017-BS-ARCH": "CMO",
    "SRC-PD-1096-NBCP": "NBC",
    "SRC-PD-1096-REVISED-IRR-METADATA": "NIR",
    "SRC-RA-9514-FIRE-CODE": "FCP",
    "SRC-BP-344-ACCESSIBILITY-LAW": "BPA",
    "SRC-PD-1067-WATER-CODE": "WCP",
    "SRC-PD-856-SANITATION-CODE": "SCP",
    "SRC-RA-7160-LOCAL-GOVERNMENT-CODE": "LGC",
    "SRC-DHSUD-HLURB-CLUP-GUIDEBOOKS": "CLU",
    "SRC-RA-10066-HERITAGE-ACT": "HER",
    "SRC-NCCA-NATIONAL-ARTISTS-ARCHITECTURE": "NCA",
    "SRC-UAP-SPP-CODE-ETHICS-METADATA": "SPP",
    "SRC-CIAP-DOCUMENT-102": "CIA",
    "SRC-RA-9184-GPRA": "GPR",
    "SRC-NSCP-METADATA": "NSC",
    "SRC-PEC-METADATA": "PEC",
    "SRC-NATIONAL-PLUMBING-CODE-METADATA": "NPC",
    "SRC-PHILIPPINE-GREEN-BUILDING-CODE": "GBC",
    "SRC-PD-957-SUBDIVISION-CONDOMINIUM": "PDN",
    "SRC-RA-386-CIVIL-CODE-CONSTRUCTION": "CIV",
    "SRC-DENR-DAO-2003-30-EIS": "EIS",
    "SRC-RAW-ALE-BUILDING-LAWS-XLSX": "RLX",
    "SRC-RAW-ALE-BT-REVIEWER-PDF": "RBR",
    "SRC-RAW-ALE-BT-JUNE-2010-PDF": "RBJ",
}

# parent_path, semantic_node_kind, category, source_ids, items(suffix, label, aliases, definition)
NODE_GROUPS: list[tuple[str, str, str, list[str], list[tuple[str, str, list[str], str]]]] = [
    ("ARC.REG.PHL", "lea_exam_meta", "lea_exam_meta", ["SRC-PRC-ARCHITECTURE-BOARD", "SRC-PRC-ALE-TOS", "SRC-RA-9266-ARCHITECTURE-ACT"], [
        ("ALE", "Philippine Architects Licensure Examination", ["ALE", "Architects Licensure Examination", "Licensure Examination for Architects", "LEA"], "Licensure-exam domain connecting PRC/PRBoA authority, RA 9266 eligibility, exam subjects, and practice authorization."),
        ("BLE", "Board Licensure Examination for Architects", ["BLEA", "board licensure examination for architects", "architecture board exam"], "Board-examination framing for the Philippine architect licensure pathway."),
        ("PRA", "Professional Regulatory Board Of Architecture", ["PRBoA", "PRB of Architecture", "Board of Architecture", "BOA"], "Regulatory board under PRC that administers architecture licensure and professional regulation metadata."),
        ("PRC", "Professional Regulation Commission", ["PRC", "Professional Regulation Commission Philippines", "Commission"], "Government commission context for licensure, registration, certificates, and board administration."),
        ("TOS", "Architecture Licensure Table Of Specifications", ["TOS", "ALE table of specifications", "exam blueprint"], "Metadata node for official subject weighting and exam-scope framing without storing protected exam content."),
        ("SUB", "ALE Subject Domain Crosswalk", ["exam subject crosswalk", "subject-domain crosswalk", "ALE domain map"], "Crosswalk between broad official exam areas and practical architecture subject domains used for study and reasoning."),
        ("DAE", "Diversified Architectural Experience", ["DAE", "diversified experience", "architectural experience prerequisite"], "Practical experience prerequisite concept linking education, mentor certification, and licensure eligibility."),
        ("MEN", "Mentor Architect Certification", ["mentor architect", "DAE mentor", "certifying architect"], "Registered architect mentorship and certification context for diversified architectural experience."),
        ("RLA", "Registered And Licensed Architect", ["RLA", "Registered Licensed Architect", "registered architect", "licensed architect"], "Post-examination professional status associated with lawful practice, signing, sealing, and continuing responsibility."),
        ("ELG", "Architecture Graduate Eligibility", ["ALE eligibility", "architecture graduate prerequisite", "BS Architecture eligibility"], "Eligibility concept linking architecture education, good moral character, experience, and licensure application readiness."),
        ("LER", "PRC LERIS Licensure Application", ["LERIS", "PRC online application", "licensure application portal"], "Metadata-only application workflow node for PRC online examination and registration transactions."),
        ("NOA", "Notice Of Admission For ALE", ["NOA", "notice of admission", "exam admission notice"], "Metadata-only exam-admission document concept; not a schedule tracker or question-content source."),
    ]),
    ("ARC.HIS.SEA", "lea_history_ph_architecture", "history_theory_philippine_architecture", ["SRC-NCCA-NATIONAL-ARTISTS-ARCHITECTURE", "SRC-RA-10066-HERITAGE-ACT"], [
        ("PVA", "Philippine Vernacular Architecture", ["Filipino vernacular architecture", "vernacular Philippine architecture"], "Climate, material, settlement, and cultural building traditions that inform Philippine architecture history."),
        ("IND", "Indigenous Architecture In The Philippines", ["indigenous architecture", "Philippine indigenous dwellings"], "Ethnolinguistic building traditions and settlement forms understood as cultural and environmental responses."),
        ("TRG", "Torogan", ["Maranao torogan", "royal Maranao house"], "Maranao elite house type used as an exam-relevant vernacular architecture example."),
        ("IVT", "Ivatan Stone House", ["Ivatan house", "Batanes stone house", "lime-and-stone house"], "Batanes vernacular house type associated with typhoon-resistant massing and local material response."),
        ("IFB", "Ifugao Bale", ["Ifugao house", "bale", "Ifugao hut"], "Cordillera raised-house type used to connect vernacular form, climate, material, and culture."),
        ("MAR", "Maranao Architecture", ["Maranao built tradition", "okir architecture"], "Mindanao vernacular and decorative tradition connecting torogan, okir, and cultural expression."),
        ("EQB", "Earthquake Baroque In The Philippines", ["earthquake baroque", "seismic colonial church adaptation"], "Colonial church adaptation pattern associated with thick walls, buttresses, and seismic risk response."),
        ("PCH", "Philippine Church Architecture", ["colonial churches", "church complexes", "mission church architecture"], "Church, convento, plaza, and settlement patterns that connect colonial history with urban morphology."),
        ("ADP", "Art Deco In The Philippines", ["Philippine Art Deco", "Manila Art Deco"], "Interwar architectural expression in Philippine cinemas, civic buildings, and commercial districts."),
        ("BPU", "Burnham Plan Urbanism In The Philippines", ["Burnham Plan", "American colonial planning", "Manila and Baguio planning"], "American colonial planning legacy connecting civic centers, axial planning, and Philippine urban design history."),
        ("CPA", "Contemporary Philippine Architecture", ["contemporary Filipino architecture", "current Philippine architecture"], "Recent Philippine architecture context connecting identity, climate response, globalization, and practice."),
        ("CRG", "Critical Regionalism In Philippine Architecture", ["Philippine critical regionalism", "regional modernism"], "Theory-history bridge connecting modern architectural language with climate, culture, and place."),
    ]),
    ("ARC.HIS.ANC", "lea_history_world_architecture", "history_theory_philippine_architecture", ["SRC-CHED-CMO-61-2017-BS-ARCH"], [
        ("ECR", "Early Christian Architecture", ["Early Christian", "basilican church tradition"], "Architectural period focused on basilican worship spaces, liturgical planning, and early church building types."),
        ("BYZ", "Byzantine Architecture", ["Byzantine", "pendentive dome tradition"], "Architectural tradition linking centralized plans, domes, mosaics, and Eastern Christian spatial symbolism."),
        ("ROM", "Romanesque Architecture", ["Romanesque", "round-arch medieval architecture"], "Medieval European tradition associated with massive walls, rounded arches, vaulting, and pilgrimage churches."),
        ("GOT", "Gothic Architecture", ["Gothic", "pointed arch architecture", "rib vault architecture"], "Medieval tradition emphasizing pointed arches, rib vaults, flying buttresses, and vertical light-filled space."),
    ]),
    ("ARC.HIS.MOD", "lea_history_world_architecture", "history_theory_philippine_architecture", ["SRC-CHED-CMO-61-2017-BS-ARCH"], [
        ("REN", "Renaissance Architecture", ["Renaissance", "classical revival"], "Early modern architecture centered on humanism, proportion, orders, perspective, and classical precedent."),
        ("BAR", "Baroque Architecture", ["Baroque", "dramatic classical architecture"], "Architecture of dynamic spatial effects, theatricality, axial compositions, and integrated art."),
        ("ROC", "Rococo Architecture", ["Rococo", "late Baroque interior ornament"], "Late Baroque-associated style emphasizing lightness, asymmetry, interior ornament, and decorative refinement."),
        ("NEO", "Neoclassical Architecture", ["Neoclassicism", "Neoclassical"], "Classical revival movement associated with archaeological interest, civic monumentality, and rational order."),
        ("POM", "Postmodern Architecture", ["Postmodernism", "postmodern architecture"], "Late twentieth-century reaction against strict modernist orthodoxy using historical reference, irony, and pluralism."),
    ]),
    ("FIG.ARD.CAA", "lea_fil_architect", "history_theory_philippine_architecture", ["SRC-NCCA-NATIONAL-ARTISTS-ARCHITECTURE"], [
        ("NAK", "Juan F Nakpil", ["Juan Nakpil", "Juan F. Nakpil", "National Artist Juan Nakpil"], "National Artist for Architecture metadata node linking Filipino modern practice, works, and architectural history study."),
        ("LOC", "Leandro V Locsin", ["Leandro Locsin", "Leandro V. Locsin", "National Artist Leandro Locsin"], "National Artist for Architecture metadata node linking modern Philippine architecture, cultural buildings, and spatial form."),
        ("ANT", "Pablo S Antonio", ["Pablo Antonio", "Pablo S. Antonio", "National Artist Pablo Antonio"], "National Artist metadata node for Philippine modern architecture and Art Deco-related works."),
        ("SAN", "Ildefonso P Santos Jr", ["Ildefonso Santos", "IP Santos", "Ildefonso P. Santos Jr."], "National Artist for landscape architecture metadata node connecting site planning and Philippine landscape practice."),
        ("MAN", "Francisco T Manosa", ["Francisco Mañosa", "Francisco Manosa", "Bobby Mañosa"], "National Artist metadata node for Filipino identity, vernacular inspiration, and tropical architectural expression."),
        ("ZAR", "Jose Maria V Zaragoza", ["Jose Maria Zaragoza", "Jose Maria V. Zaragoza"], "National Artist metadata node connecting Philippine church, institutional, and modern architectural works."),
    ]),
    ("FIG.WRK.BUI", "lea_arch_work", "history_theory_philippine_architecture", ["SRC-NCCA-NATIONAL-ARTISTS-ARCHITECTURE", "SRC-RA-10066-HERITAGE-ACT"], [
        ("CCP", "Cultural Center Of The Philippines Complex", ["CCP Complex", "Cultural Center of the Philippines"], "Philippine cultural-building work cluster used to connect Locsin, modernism, public patronage, and national cultural institutions."),
        ("PIC", "Philippine International Convention Center", ["PICC", "Philippine International Convention Center"], "Convention-center work associated with modern Philippine civic architecture and large-span public assembly planning."),
        ("SJA", "San Agustin Church Manila", ["San Agustin Church", "Intramuros church"], "Heritage church work used to connect colonial church architecture, conservation, and Philippine architectural history."),
        ("UST", "UST Main Building", ["University of Santo Tomas Main Building", "UST Main Building"], "Institutional building work used to connect seismic design history, campus planning, and Philippine modern heritage."),
        ("FHA", "Folk Arts Theater", ["Folk Arts Theater", "Tanghalang Francisco Balagtas"], "Cultural venue work associated with Locsin-era public architecture and performance-space planning."),
        ("COC", "Coconut Palace", ["Tahanang Pilipino", "Coconut Palace"], "Philippine architectural work often discussed for material symbolism, vernacular reference, and cultural representation."),
    ]),
    ("ARC.THE.DPR", "lea_theory_design_principle", "history_theory_philippine_architecture", ["SRC-CHED-CMO-61-2017-BS-ARCH"], [
        ("FRM", "Form In Architecture", ["form", "architectural form"], "Shape, massing, and perceptual configuration as a core architecture theory concept."),
        ("FUN", "Function In Architecture", ["function", "architectural function"], "Use, purpose, and operational need as a design driver and evaluation criterion."),
        ("SPC", "Space In Architecture", ["space", "architectural space", "spatial design"], "Volume, enclosure, sequence, and experience as core architecture design knowledge."),
        ("ORD", "Order In Architecture", ["order", "architectural ordering"], "Organizing logic that makes relationships between form, structure, circulation, and use legible."),
        ("SCL", "Scale In Architecture", ["scale", "human scale", "architectural scale"], "Relationship between built form, human perception, context, and measurable dimensions."),
        ("BAL", "Balance In Composition", ["balance", "visual balance"], "Compositional equilibrium achieved through mass, symmetry, asymmetry, and visual weight."),
        ("SYM", "Symmetry In Architecture", ["symmetry", "bilateral symmetry"], "Ordering device involving mirrored or rotational correspondence around axes or centers."),
        ("DAT", "Datum In Design", ["datum", "ordering datum"], "Line, plane, or volume that organizes otherwise distinct architectural elements."),
        ("TRN", "Transformation In Design", ["transformation", "formal transformation"], "Modification of form or spatial order while preserving identifiable design logic."),
        ("CIR", "Circulation In Architecture", ["circulation", "movement sequence"], "Movement paths and spatial sequences linking users, functions, exits, and experience."),
        ("ANT", "Architectural Anthropometrics", ["anthropometrics", "human dimensions"], "Human body dimensions used to size spaces, furniture, clearances, and ergonomic interfaces."),
        ("ERG", "Architectural Ergonomics", ["ergonomics", "human factors"], "Fit between human users, tasks, reach ranges, comfort, and built-environment elements."),
    ]),
    ("ARC.TAC.SOS", "lea_tropical_design", "sustainability_climate_resilience", ["SRC-CHED-CMO-61-2017-BS-ARCH", "SRC-PHILIPPINE-GREEN-BUILDING-CODE"], [
        ("SNP", "Sun Path Analysis", ["sun path", "solar path", "solar analysis"], "Design analysis of solar position, heat gain, daylight, and shading needs in tropical sites."),
        ("SHD", "External Shading Strategy", ["shading", "sun control", "solar shading"], "Facade and site design tactic for reducing heat gain while supporting daylight and comfort."),
        ("ORI", "Building Orientation For Tropical Design", ["orientation", "solar orientation", "climate orientation"], "Placement and massing decision that affects heat gain, ventilation, daylight, and site response."),
        ("DAY", "Daylighting For Tropical Buildings", ["daylighting", "natural light", "daylight design"], "Use of controlled natural light while managing glare and heat gain in warm climates."),
    ]),
    ("ARC.TAC.NVS", "lea_tropical_design", "sustainability_climate_resilience", ["SRC-CHED-CMO-61-2017-BS-ARCH", "SRC-PHILIPPINE-GREEN-BUILDING-CODE"], [
        ("XVN", "Cross Ventilation", ["cross ventilation", "through ventilation"], "Natural ventilation strategy using pressure differences and openings on multiple sides of space."),
        ("STK", "Stack Ventilation", ["stack effect ventilation", "thermal buoyancy ventilation"], "Passive ventilation strategy using vertical temperature and pressure differences."),
        ("OPN", "Operable Opening Strategy", ["operable windows", "ventilation openings"], "Design of openings to support natural ventilation, daylight, security, rain protection, and user control."),
        ("VTC", "Ventilated Transitional Space", ["veranda", "arcade", "breezeway"], "Semi-open architectural space that moderates climate and links indoor and outdoor use."),
    ]),
    ("ARC.SIT.SAN", "lea_site_planning", "site_planning_urban_design", ["SRC-CHED-CMO-61-2017-BS-ARCH", "SRC-DHSUD-HLURB-CLUP-GUIDEBOOKS"], [
        ("PRG", "Architectural Programming", ["programming", "space program", "brief development"], "Definition of users, activities, areas, relationships, performance needs, and project goals before design."),
        ("BUB", "Bubble Diagram", ["bubble diagram", "relationship diagram"], "Early diagram of spaces and adjacencies used to reason about planning without fixed geometry."),
        ("ADJ", "Adjacency Analysis", ["adjacency matrix", "space adjacency"], "Study of which spaces should be near, separated, connected, or buffered."),
        ("USR", "User Analysis", ["user profile", "user needs analysis"], "Study of user groups, behaviors, capacities, accessibility needs, and operational patterns."),
        ("SLP", "Slope Analysis", ["slope analysis", "terrain slope"], "Site analysis of topography affecting grading, access, drainage, foundations, and buildability."),
        ("WND", "Wind Analysis", ["wind analysis", "prevailing wind"], "Microclimate analysis connecting natural ventilation, comfort, exposure, and building orientation."),
        ("VIE", "Views And Vistas Analysis", ["views", "vistas", "view corridor"], "Site-reading method for protecting desirable views, screening conflicts, and organizing orientation."),
        ("NOI", "Noise Analysis", ["noise analysis", "acoustic site analysis"], "Assessment of sound sources and buffers that influence site planning and interior comfort."),
        ("FIR", "Fire Access Site Planning", ["fire access", "emergency access", "BFP access"], "Site planning of access routes and clearances for fire response and emergency operations."),
        ("DRN", "Site Drainage Planning", ["site drainage", "stormwater routing"], "Surface-water management concept linking grading, legal easements, flood risk, and landscape."),
    ]),
    ("URB.LUZ.CLU", "lea_urban_planning", "site_planning_urban_design", ["SRC-DHSUD-HLURB-CLUP-GUIDEBOOKS", "SRC-RA-7160-LOCAL-GOVERNMENT-CODE"], [
        ("LCC", "Locational Clearance", ["locational clearance", "zoning clearance"], "Local land-use approval concept linking CLUP, zoning ordinance, development controls, and permit workflow."),
        ("LUC", "Land Use Classification", ["land use classification", "land-use category"], "Planning category that constrains permitted uses, intensity, compatibility, and development control."),
        ("RES", "Residential Zone", ["residential zoning", "residential zone"], "Zoning class primarily for dwelling and neighborhood-support uses."),
        ("COM", "Commercial Zone", ["commercial zoning", "commercial zone"], "Zoning class for business, retail, office, and service uses, subject to local ordinances."),
        ("IND", "Industrial Zone", ["industrial zoning", "industrial zone"], "Zoning class for production, logistics, manufacturing, or industrial activities and buffers."),
        ("INS", "Institutional Zone", ["institutional zoning", "institutional zone"], "Zoning class for civic, educational, health, religious, and public-service uses."),
        ("POS", "Parks And Open Space Zone", ["parks and open space", "open space zoning"], "Land-use category preserving recreation, ecological, landscape, or public realm functions."),
        ("HRT", "Heritage District", ["heritage district", "heritage zone"], "Planning overlay for conserving culturally significant urban areas, streetscapes, and built heritage."),
    ]),
    ("LAW.AAP.SAP", "lea_ph_law_practice", "philippine_law_code", ["SRC-RA-9266-ARCHITECTURE-ACT", "SRC-RA-9266-IRR-METADATA", "SRC-UAP-SPP-CODE-ETHICS-METADATA"], [
        ("ADO", "Architectural Documents", ["architectural documents", "architectural plans", "instruments of service"], "Architecture practice documents prepared, signed, sealed, coordinated, and protected within Philippine professional practice."),
        ("AOR", "Architect Of Record", ["AOR", "architect of record"], "Registered architect professionally responsible for architectural documents issued under seal or signature."),
        ("AIC", "Architect In Charge Of Construction", ["AICC", "architect in charge of construction"], "Practice role associated with construction-phase architectural services and responsibility boundaries."),
        ("SER", "Architectural Services", ["scope of architectural services", "design services"], "Professional services covering design, documentation, consultation, coordination, and construction-phase assistance."),
        ("SPP", "Standards Of Professional Practice", ["SPP", "standards of professional practice"], "Professional-practice source-family concept for service scope, responsibilities, deliverables, and agreements."),
        ("IAP", "Integrated Accredited Professional Organization Of Architects", ["IAPOA", "integrated accredited professional organization"], "Professional organization integration concept recognized in architecture regulation metadata."),
        ("UAP", "United Architects Of The Philippines", ["UAP", "United Architects of the Philippines"], "Professional organization context linked to IAPOA, standards, and practice metadata."),
        ("ILP", "Illegal Practice Of Architecture", ["unauthorized practice", "illegal practice"], "Unlawful practice concept connecting title protection, scope, signing/sealing, and enforcement."),
        ("FAP", "Foreign Architect Temporary Special Permit", ["TSP", "temporary special permit", "foreign architect practice"], "Foreign-practice concept requiring regulated authorization and local professional interfaces."),
        ("PFE", "Professional Fees For Architectural Services", ["professional fees", "architectural fees"], "Professional compensation concept connected to services, agreements, ethics, and project delivery."),
    ]),
    ("LAW.PNB.PIE", "lea_ph_building_code", "philippine_law_code", ["SRC-PD-1096-NBCP", "SRC-PD-1096-REVISED-IRR-METADATA"], [
        ("BPE", "Building Permit", ["building permit", "permit to construct"], "Administrative authorization concept for proposed construction before work proceeds."),
        ("OPM", "Occupancy Permit", ["occupancy permit", "permit to occupy"], "Post-construction authorization concept linking inspection, completion, and lawful occupancy."),
        ("COC", "Certificate Of Occupancy", ["certificate of occupancy", "CO"], "Closeout compliance certificate concept associated with inspection and use authorization."),
        ("BOF", "Building Official", ["building official", "OBO", "Office of the Building Official"], "Local official or office context administering building-code permits, review, inspection, and enforcement."),
        ("RCD", "Referral Codes", ["referral codes", "NBCP referral code"], "Related technical code families referenced by building-code administration without storing protected code text."),
        ("ANP", "Ancillary Permits", ["ancillary permits", "discipline permits"], "Trade or discipline permits coordinated with architectural, structural, sanitary, electrical, mechanical, and fire approvals."),
        ("PRV", "Plan Review Workflow", ["plan review", "permit plan review"], "Review workflow connecting architectural documents, code checks, agency referrals, and corrections."),
        ("COR", "Correction Order", ["correction notice", "permit correction"], "Compliance-response concept for deficiencies identified in plan review or inspection."),
    ]),
    ("LAW.PNB.OUC", "lea_ph_building_code", "philippine_law_code", ["SRC-PD-1096-NBCP", "SRC-PD-1096-REVISED-IRR-METADATA"], [
        ("OCL", "Occupancy Classification", ["occupancy classification", "use classification"], "Code applicability concept that influences egress, fire protection, sanitation, parking, and allowable design controls."),
        ("CTY", "Construction Type", ["type of construction", "construction classification"], "Building classification concept tied to fire-resistance, materials, height, area, and code compliance."),
        ("FZN", "Fire Zone", ["fire zone", "fire zoning"], "Planning and code concept affecting building controls, fire risk interfaces, and local applicability."),
        ("ABH", "Allowable Building Height", ["allowable height", "building height limit"], "Height-control concept affected by occupancy, construction type, zoning, and fire-safety criteria."),
        ("ABA", "Allowable Building Area", ["allowable area", "building area limit"], "Area-control concept affected by occupancy, construction type, frontage, fire protection, and site constraints."),
        ("YRD", "Setbacks Yards And Courts", ["setbacks", "yards", "courts"], "Open-space and separation controls affecting light, ventilation, access, fire separation, and site planning."),
        ("LVS", "Light Ventilation And Sanitation Requirement", ["light and ventilation", "LVS", "sanitation requirement"], "Building-planning requirement family linking health, comfort, openings, room planning, and sanitation."),
        ("PRK", "Parking Requirement", ["parking requirement", "off-street parking"], "Design-control concept connecting occupancy, local zoning, accessibility, and site circulation."),
    ]),
    ("LAW.PFC.FSI", "lea_ph_fire_code", "fire_life_safety", ["SRC-RA-9514-FIRE-CODE"], [
        ("BFP", "Bureau Of Fire Protection", ["BFP", "Bureau of Fire Protection"], "Fire authority context for Philippine fire safety evaluation, inspection, enforcement, and coordination."),
        ("FSE", "Fire Safety Evaluation Clearance", ["FSEC", "fire safety evaluation clearance"], "Pre-occupancy or permitting clearance concept linking fire-code review and building permit workflows."),
        ("FIC", "Fire Safety Inspection Certificate", ["FSIC", "fire safety inspection certificate"], "Inspection certificate concept linking occupancy, business operation, maintenance, and BFP approval."),
        ("FPR", "Fire Prevention", ["fire prevention", "fire prevention program"], "Fire-code objective area linking design, maintenance, operations, inspection, and hazard control."),
        ("FIS", "Fire Inspection", ["fire inspection", "BFP inspection"], "Inspection activity connecting fire safety certificates, maintenance, occupancy, and enforcement."),
        ("FSM", "Fire Safety Maintenance", ["fire safety maintenance", "life safety maintenance"], "Operations-phase concept for preserving fire/life-safety systems and safe conditions."),
    ]),
    ("LAW.PFC.OFS", "lea_ph_fire_code", "fire_life_safety", ["SRC-RA-9514-FIRE-CODE"], [
        ("EGR", "Means Of Egress", ["means of egress", "egress system"], "Life-safety concept for safe exit access, exits, and exit discharge coordinated with occupancy and design."),
        ("OCL", "Occupant Load", ["occupant load", "occupancy load"], "Population basis for egress sizing, plumbing fixtures, life safety, and design decisions."),
        ("EAC", "Exit Access", ["exit access", "access to exit"], "Egress component connecting occupied spaces to exits through corridors, aisles, doors, and routes."),
        ("EXT", "Exit", ["exit", "protected exit"], "Egress component providing a protected path toward exit discharge."),
        ("EXD", "Exit Discharge", ["exit discharge", "discharge path"], "Egress component leading from exits to public way or safe dispersal area."),
        ("TRD", "Travel Distance", ["travel distance", "egress travel distance"], "Distance measure connecting plan layout, occupancy, sprinklers, and life-safety design."),
        ("DED", "Dead End Corridor", ["dead-end corridor", "dead end"], "Egress layout condition requiring code review because it affects evacuation reliability."),
        ("EGL", "Emergency Lighting", ["emergency lighting", "egress lighting"], "Electrical/life-safety system concept supporting safe egress during power loss."),
        ("EXS", "Exit Sign", ["exit sign", "egress signage"], "Life-safety signage concept guiding occupants toward egress paths and exits."),
    ]),
    ("LAW.PFC.HMC", "lea_ph_fire_code", "fire_life_safety", ["SRC-RA-9514-FIRE-CODE"], [
        ("HOC", "Hazardous Occupancy", ["hazardous occupancy", "special hazard occupancy"], "Occupancy condition requiring fire-code hazard analysis, separation, controls, and operations coordination."),
        ("CBM", "Combustible Material Storage", ["combustible storage", "storage of combustible materials"], "Fire-hazard topic connecting storage practices, occupancy, housekeeping, and inspection."),
        ("FHA", "Fire Hazard", ["fire hazard", "hazardous condition"], "Unsafe condition or material configuration that increases fire risk and triggers prevention/enforcement response."),
        ("FLN", "Fire Lane", ["fire lane", "fire apparatus access"], "Site fire access concept linking circulation, setbacks, emergency response, and BFP coordination."),
    ]),
    ("LAW.PFC.EPE", "lea_ph_fire_code", "fire_life_safety", ["SRC-RA-9514-FIRE-CODE"], [
        ("FAL", "Fire Alarm System", ["fire alarm", "fire detection and alarm"], "Detection and notification system topic connecting utilities, life safety, occupancy, and acceptance testing."),
        ("FDT", "Fire Detection System", ["fire detection", "smoke detection"], "Sensing system topic that supports alarm initiation, emergency response, and fire safety maintenance."),
        ("ASP", "Automatic Sprinkler System", ["sprinkler system", "automatic sprinklers"], "Water-based suppression system topic connecting fire code, plumbing/fire protection utilities, and maintenance."),
        ("STP", "Standpipe System", ["standpipe", "fire hose standpipe"], "Fire protection system topic supporting manual firefighting in buildings."),
        ("FEX", "Fire Extinguisher", ["fire extinguisher", "portable extinguisher"], "First-aid suppression device topic connecting occupancy, hazards, maintenance, and inspection."),
        ("SMC", "Smoke Control", ["smoke control", "smoke management"], "Fire/life-safety system topic connected to mechanical systems, egress, high-rise, and testing."),
        ("FRC", "Fire Rated Construction", ["fire-rated construction", "fire-resistance rating"], "Compartmentation concept connecting walls, doors, penetrations, materials, and occupancy separations."),
        ("FDR", "Fire Door", ["fire door", "rated door"], "Opening-protection component preserving rated separations while allowing circulation and egress."),
        ("FWA", "Fire Wall", ["fire wall", "fire separation wall"], "Fire-resistance assembly concept separating buildings, areas, or hazards."),
        ("FST", "Firestopping", ["firestopping", "penetration firestop"], "Rated-penetration sealing topic connecting utilities, compartmentation, and construction inspection."),
    ]),
    ("LAW.PAL.ACR", "lea_ph_accessibility", "accessibility_universal_design", ["SRC-BP-344-ACCESSIBILITY-LAW"], [
        ("BRF", "Barrier Free Design", ["barrier-free design", "accessible design"], "Design approach removing physical barriers in public-use buildings, sites, and facilities."),
        ("PWD", "Persons With Disabilities", ["PWD", "persons with disabilities", "disabled persons"], "User group and rights context for accessibility law and inclusive design."),
        ("ARS", "Accessible Route", ["accessible route", "barrier-free route"], "Continuous path connecting site arrival, entrances, circulation, rooms, and amenities."),
        ("RMP", "Accessible Ramp", ["ramp", "accessible ramp"], "Sloped route component used where level changes must be traversed accessibly."),
        ("HND", "Handrail", ["handrail", "grab rail"], "Support element connected to ramps, stairs, toilets, and user stability."),
        ("APK", "Accessible Parking", ["accessible parking", "PWD parking"], "Parking space and access aisle concept connecting site planning and accessible routes."),
        ("ATO", "Accessible Toilet", ["accessible toilet", "PWD toilet", "accessible restroom"], "Sanitary facility planning concept linking clearances, fixtures, door swing, and universal design."),
        ("DCL", "Door Clearance", ["door clearances", "maneuvering clearance"], "Interior-accessibility concept connecting openings, circulation, wheelchair use, and usability."),
        ("COR", "Accessible Corridor", ["accessible corridor", "corridor clearance"], "Circulation concept linking route width, turning, obstructions, and egress."),
        ("ELV", "Accessible Elevator", ["elevator accessibility", "accessible lift"], "Vertical-transport accessibility topic connecting route continuity and multi-story public-use buildings."),
        ("SIG", "Accessible Signage", ["accessibility signage", "signage"], "Wayfinding and communication concept supporting accessible navigation."),
        ("TTI", "Tactile Indicators", ["tactile indicators", "tactile ground surface indicators"], "Sensory accessibility feature supporting navigation and hazard awareness where applicable."),
    ]),
    ("LAW.WCW.DRE", "lea_ph_water_code", "water_sanitation_public_health", ["SRC-PD-1067-WATER-CODE"], [
        ("WRT", "Water Rights", ["water rights", "water right"], "Legal concept for authorized use and control of water resources."),
        ("WPT", "Water Permit", ["water permit", "water appropriation permit"], "Administrative concept for water appropriation and use authorization."),
        ("WAE", "Waterway Easement", ["water easement", "river easement", "water body easement"], "Site constraint concept connecting waterways, setbacks, access, flood risk, and land-use controls."),
        ("DRG", "Drainage Outfall Coordination", ["drainage outfall", "site drainage discharge"], "Site-plumbing concept linking stormwater discharge, receiving waters, easements, and public works interfaces."),
        ("FLD", "Flooding Constraint", ["flooding", "flood hazard", "flood constraint"], "Water-related site constraint affecting elevation, placement, access, utilities, and resilience decisions."),
        ("SWF", "Surface Water", ["surface water", "water body"], "Water-resource topic relevant to site planning, drainage, easements, and environmental protection."),
    ]),
    ("LAW.SCP.MPF", "lea_ph_sanitation_code", "water_sanitation_public_health", ["SRC-PD-856-SANITATION-CODE"], [
        ("TOI", "Toilet And Sanitation Facilities", ["toilet requirements", "sanitary facilities", "comfort rooms"], "Public-health building topic connecting sanitation code, occupancy, plumbing, and accessibility."),
        ("VHE", "Ventilation And Health", ["ventilation for health", "healthy ventilation"], "Health-oriented ventilation concept linking sanitation, indoor air quality, and building planning."),
        ("SOL", "Solid Waste In Building Design", ["solid waste", "refuse storage", "waste management"], "Waste management topic connecting site/service access, sanitation, odor, pests, and operations."),
        ("PWS", "Safe Water Supply", ["safe water supply", "potable water"], "Public-health water topic linking plumbing, sanitation, water continuity, and facility operation."),
        ("SEW", "Sewage And Excreta Disposal", ["sewerage", "excreta disposal", "sewage disposal"], "Sanitation topic connecting sanitary drainage, septic systems, sewer connections, and public health."),
        ("LHA", "Local Health Authority Coordination", ["local health authority", "health officer coordination"], "Jurisdictional coordination concept for sanitation inspection, permits, and public-health enforcement."),
    ]),
    ("ARC.MAT.CON", "lea_materials_methods", "materials_construction_specifications", ["SRC-CHED-CMO-61-2017-BS-ARCH", "SRC-NSCP-METADATA"], [
        ("RCC", "Reinforced Concrete", ["reinforced concrete", "RC"], "Concrete with embedded reinforcement used in slabs, beams, columns, walls, foundations, and frames."),
        ("FRM", "Concrete Formwork", ["formwork", "forms"], "Temporary construction system shaping concrete until it can support itself."),
        ("JNT", "Construction Joint", ["construction joint", "cold joint"], "Planned interface in construction sequence affecting durability, water resistance, and detailing."),
        ("DPC", "Damp Proofing", ["damp proofing", "moisture barrier"], "Moisture-control measure protecting assemblies from ground or capillary moisture."),
    ]),
    ("ARC.MAT.STM", "lea_materials_methods", "materials_construction_specifications", ["SRC-CHED-CMO-61-2017-BS-ARCH", "SRC-NSCP-METADATA"], [
        ("STL", "Structural Steel", ["steel", "structural steel"], "Steel material system used for frames, trusses, long spans, connections, and hybrid structures."),
        ("TIM", "Wood And Timber", ["wood", "timber", "lumber"], "Bio-based material system used in framing, finishes, joinery, and vernacular traditions."),
        ("ALU", "Aluminum Building Products", ["aluminum", "aluminium", "aluminum frames"], "Metal product family used in windows, doors, curtain walls, panels, and hardware."),
        ("GLS", "Architectural Glass", ["glass", "glazing"], "Transparent or translucent material system affecting daylight, envelope performance, safety, and aesthetics."),
    ]),
    ("ARC.MAT.FIN", "lea_materials_methods", "materials_construction_specifications", ["SRC-CHED-CMO-61-2017-BS-ARCH"], [
        ("FLR", "Flooring Materials", ["flooring", "floor finishes"], "Finish material family affecting durability, safety, maintenance, acoustics, and interior character."),
        ("WLF", "Wall Finishes", ["wall finish", "wall covering"], "Interior or exterior finish family affecting protection, aesthetics, acoustics, and maintenance."),
        ("CEF", "Ceiling Systems", ["ceiling", "ceiling system"], "Overhead assembly coordinating acoustics, lighting, sprinklers, diffusers, access panels, and aesthetics."),
        ("PNT", "Paints And Coatings", ["paint", "coating", "architectural coating"], "Applied finish system affecting appearance, substrate protection, maintenance, and indoor environmental quality."),
        ("HDW", "Architectural Hardware", ["hardware", "door hardware"], "Product family coordinating doors, access control, egress, accessibility, security, and operation."),
    ]),
    ("ARC.BLD.STR", "lea_structural_concepts", "structural_utilities_systems", ["SRC-NSCP-METADATA", "SRC-CHED-CMO-61-2017-BS-ARCH"], [
        ("LDP", "Load Path", ["load path", "load transfer"], "Conceptual route by which gravity and lateral loads move through structural elements to foundations."),
        ("DDL", "Dead Load", ["dead load", "permanent load"], "Self-weight and permanent load concept considered in architectural-structural coordination."),
        ("LVL", "Live Load", ["live load", "occupancy load structural"], "Variable occupancy or use load concept affecting structural planning and space use."),
        ("WDL", "Wind Load", ["wind load", "wind action"], "Environmental lateral load concept affecting facade, roof, anchorage, and structural systems."),
        ("SDL", "Seismic Load", ["seismic load", "earthquake load"], "Earthquake loading concept affecting structural system selection, detailing, and nonstructural coordination."),
        ("SGL", "Structural Grid", ["structural grid", "column grid"], "Planning framework coordinating columns, spans, bays, walls, rooms, parking, and services."),
        ("SPN", "Structural Span", ["span", "bay span"], "Distance between supports that influences depth, material, cost, and spatial flexibility."),
        ("DEF", "Deflection", ["deflection", "serviceability deflection"], "Deformation concept affecting partitions, finishes, glazing, drainage, and occupant perception."),
    ]),
    ("ARC.BLD.SRV", "lea_utilities_systems", "structural_utilities_systems", ["SRC-PEC-METADATA", "SRC-NATIONAL-PLUMBING-CODE-METADATA", "SRC-PHILIPPINE-GREEN-BUILDING-CODE"], [
        ("PWS", "Water Supply System Coordination", ["water supply", "domestic water"], "Architectural coordination of water service, shafts, equipment rooms, fixture groups, and maintenance access."),
        ("SDR", "Sanitary Drainage Coordination", ["sanitary drainage", "soil and waste"], "Coordination of drainage stacks, slopes, fixtures, cleanouts, ceiling spaces, and code clearances."),
        ("ELP", "Electrical Power Distribution Coordination", ["power distribution", "electrical distribution"], "Coordination of service rooms, risers, panels, equipment access, and load planning."),
        ("LGT", "Architectural Lighting Coordination", ["lighting", "lighting system"], "Coordination of illumination, controls, ceiling systems, daylight, emergency lighting, and visual comfort."),
        ("HVC", "HVAC Space Coordination", ["HVAC", "mechanical system", "air conditioning"], "Coordination of equipment, ductwork, shafts, ceiling space, intake/exhaust, noise, and maintainability."),
        ("VTR", "Vertical Transportation Coordination", ["vertical transportation", "elevators", "escalators"], "Coordination of lifts, pits, shafts, machine rooms, accessibility, egress, and core planning."),
        ("BAS", "Building Automation Coordination", ["BAS", "building automation", "smart building systems"], "Coordination of sensors, controllers, networks, energy monitoring, commissioning, and operations."),
        ("SEC", "Security And Communications Coordination", ["security systems", "communications systems", "ICT systems"], "Coordination of pathways, equipment rooms, devices, power, data, access control, and operations."),
    ]),
    ("ARC.INT.PAC", "lea_interiors", "interiors_human_factors", ["SRC-CHED-CMO-61-2017-BS-ARCH", "SRC-BP-344-ACCESSIBILITY-LAW"], [
        ("ISP", "Interior Space Planning", ["interior space planning", "space planning"], "Organization of rooms, furniture, circulation, clearances, services, and user activities inside buildings."),
        ("FUR", "Furniture Layout", ["furniture layout", "furniture planning"], "Arrangement of movable and built-in furnishings to support activity, ergonomics, circulation, and accessibility."),
        ("COL", "Color Theory In Interiors", ["color theory", "interior color"], "Use of color for perception, mood, wayfinding, identity, and visual comfort."),
        ("ACU", "Interior Acoustics", ["acoustics", "sound control"], "Interior design topic connecting room finishes, partitions, ceilings, noise, and user comfort."),
        ("WAY", "Interior Wayfinding", ["wayfinding", "signage planning"], "Interior navigation concept linking circulation, signage, landmarks, accessibility, and user behavior."),
        ("IEQ", "Indoor Environmental Quality", ["IEQ", "indoor environmental quality"], "Interior performance concept joining air, light, sound, thermal comfort, materials, and health."),
    ]),
    ("CON.DMC.DBB", "lea_contracts_admin", "professional_practice_contracts", ["SRC-CIAP-DOCUMENT-102", "SRC-RA-9184-GPRA", "SRC-UAP-SPP-CODE-ETHICS-METADATA"], [
        ("BID", "Bid Documents", ["bid documents", "bidding documents"], "Procurement package concept linking drawings, specifications, conditions, instructions, addenda, and proposals."),
        ("ADD", "Addenda", ["addendum", "addenda"], "Pre-award document modifying or clarifying bidding or contract documents."),
        ("COO", "Change Order", ["change order", "variation order"], "Construction-administration mechanism for scope, time, or cost changes after contract award."),
        ("RFI", "Request For Information", ["RFI", "request for information"], "Construction communication used to resolve document questions, coordination gaps, or site conditions."),
        ("SHD", "Shop Drawings", ["shop drawings", "fabrication drawings"], "Contractor/subcontractor submittals showing fabrication, installation, and coordination information."),
        ("SUB", "Submittals", ["submittal", "product submittal"], "Reviewable information such as product data, samples, shop drawings, and method statements."),
        ("PUN", "Punch List", ["punch list", "deficiency list"], "Closeout list of incomplete or deficient work to be corrected before final completion."),
        ("ASB", "As Built Drawings", ["as-built drawings", "record drawings"], "Closeout documents recording installed conditions for operation, maintenance, and future work."),
        ("WAR", "Warranty", ["warranty", "defects liability"], "Post-completion obligation concept connected to closeout, maintenance, and contract administration."),
        ("PAY", "Certificate Of Payment", ["payment certificate", "progress billing"], "Construction-administration concept connecting measured progress, certification, billing, and contract responsibilities."),
    ]),
]

IMPROVE_HINTS: dict[str, tuple[list[str], list[str], str]] = {
    "ARC.REG.PHL": (["LEA", "ALE", "BLEA", "Philippine architecture board exam", "Philippine architect licensure"], ["SRC-PRC-ALE-TOS", "SRC-RA-9266-ARCHITECTURE-ACT"], "lea_domain_anchor"),
    "ARC.REG.PHL.PAH": (["History and Theory", "Planning and Architectural Practice", "Philippine architecture history"], ["SRC-PRC-ALE-TOS", "SRC-CHED-CMO-61-2017-BS-ARCH"], "lea_subject_area"),
    "ARC.REG.PHL.PAS": (["Building Technology", "Building Utilities", "Structural conceptualization", "Architectural specifications"], ["SRC-PRC-ALE-TOS", "SRC-CHED-CMO-61-2017-BS-ARCH"], "lea_subject_area"),
    "ARC.REG.PHL.PAD": (["Architectural Design", "Site Planning", "Urban Design", "Architectural Interiors"], ["SRC-PRC-ALE-TOS"], "lea_subject_area"),
    "ARC.REG.PHL.RPS": (["RA 9266", "Architecture Act", "professional practice law"], ["SRC-RA-9266-ARCHITECTURE-ACT", "SRC-RA-9266-IRR-METADATA"], "lea_law_endpoint"),
    "ARC.REG.PHL.PCC": (["PD 1096", "NBCP", "National Building Code"], ["SRC-PD-1096-NBCP", "SRC-PD-1096-REVISED-IRR-METADATA"], "lea_law_endpoint"),
    "ARC.REG.PHL.BAC": (["BP 344", "Accessibility Law", "barrier-free design"], ["SRC-BP-344-ACCESSIBILITY-LAW"], "lea_law_endpoint"),
    "LAW.AAP": (["RA 9266", "Architecture Act", "architectural practice law"], ["SRC-RA-9266-ARCHITECTURE-ACT"], "lea_law_source"),
    "LAW.PNB": (["PD 1096", "NBCP", "National Building Code of the Philippines"], ["SRC-PD-1096-NBCP"], "lea_law_source"),
    "LAW.PFC": (["RA 9514", "FCP", "Revised Fire Code of the Philippines"], ["SRC-RA-9514-FIRE-CODE"], "lea_law_source"),
    "LAW.PAL": (["BP 344", "Accessibility Law", "Batas Pambansa Blg. 344"], ["SRC-BP-344-ACCESSIBILITY-LAW"], "lea_law_source"),
    "LAW.WCW": (["PD 1067", "Water Code", "water rights"], ["SRC-PD-1067-WATER-CODE"], "lea_law_source"),
    "LAW.SCP": (["PD 856", "Sanitation Code", "Code on Sanitation"], ["SRC-PD-856-SANITATION-CODE"], "lea_law_source"),
    "LAW.ZON": (["CLUP", "zoning ordinance", "locational clearance", "LGU land use"], ["SRC-RA-7160-LOCAL-GOVERNMENT-CODE", "SRC-DHSUD-HLURB-CLUP-GUIDEBOOKS"], "lea_law_source"),
    "LAW.HER": (["RA 10066", "heritage law", "built heritage conservation"], ["SRC-RA-10066-HERITAGE-ACT"], "lea_law_source"),
    "LAW.CON": (["CIAP Document 102", "RA 9184", "construction contract law"], ["SRC-CIAP-DOCUMENT-102", "SRC-RA-9184-GPRA"], "lea_law_source"),
    "ARC.HIS.SEA.BKS": (["bahay kubo", "nipa hut", "climate-responsive vernacular house"], ["SRC-NCCA-NATIONAL-ARTISTS-ARCHITECTURE"], "lea_history_endpoint"),
    "ARC.HIS.SEA.BNB": (["bahay na bato", "stone house", "Spanish-Filipino hybrid house"], ["SRC-NCCA-NATIONAL-ARTISTS-ARCHITECTURE", "SRC-RA-10066-HERITAGE-ACT"], "lea_history_endpoint"),
    "ARC.HIS.SEA.SCC": (["colonial churches", "Spanish colonial church", "mission church complex"], ["SRC-RA-10066-HERITAGE-ACT"], "lea_history_endpoint"),
    "ARC.HIS.MOD.CRC": (["critical regionalism", "regional modernism", "place-based modernism"], ["SRC-CHED-CMO-61-2017-BS-ARCH"], "lea_theory_endpoint"),
    "ARC.TAC": (["tropical design", "climate-responsive design", "Philippine climate design"], ["SRC-CHED-CMO-61-2017-BS-ARCH", "SRC-PHILIPPINE-GREEN-BUILDING-CODE"], "lea_tropical_endpoint"),
    "ARC.SIT.SAN": (["site analysis", "site planning", "environmental site analysis"], ["SRC-CHED-CMO-61-2017-BS-ARCH", "SRC-DHSUD-HLURB-CLUP-GUIDEBOOKS"], "lea_site_endpoint"),
    "ARC.COD.BCA": (["building permit review", "occupancy classification review", "NBCP administration"], ["SRC-PD-1096-NBCP"], "lea_code_endpoint"),
    "ARC.COD.ZLU": (["zoning", "locational clearance", "CLUP"], ["SRC-DHSUD-HLURB-CLUP-GUIDEBOOKS", "SRC-RA-7160-LOCAL-GOVERNMENT-CODE"], "lea_code_endpoint"),
    "ARC.FIR.EGR": (["egress planning", "means of egress", "occupant load design"], ["SRC-RA-9514-FIRE-CODE", "SRC-PD-1096-NBCP"], "lea_fire_endpoint"),
    "ARC.ACC.BFR": (["barrier-free route", "BP 344 route", "accessible path"], ["SRC-BP-344-ACCESSIBILITY-LAW"], "lea_access_endpoint"),
    "PLS.PWS": (["domestic water supply", "safe water supply", "potable water coordination"], ["SRC-NATIONAL-PLUMBING-CODE-METADATA", "SRC-PD-856-SANITATION-CODE"], "lea_utility_endpoint"),
    "PLS.PWS.BAP": (["backflow prevention", "cross-connection control", "backflow testing"], ["SRC-NATIONAL-PLUMBING-CODE-METADATA", "SRC-PD-856-SANITATION-CODE"], "lea_utility_endpoint"),
    "FLS.EGR": (["means of egress", "fire exits", "travel distance"], ["SRC-RA-9514-FIRE-CODE"], "lea_fire_endpoint"),
    "FLS.FDA": (["fire alarm", "fire detection", "BFP acceptance"], ["SRC-RA-9514-FIRE-CODE"], "lea_fire_endpoint"),
    "FLS.ASS": (["automatic sprinkler system", "standpipe", "fire suppression"], ["SRC-RA-9514-FIRE-CODE"], "lea_fire_endpoint"),
    "ELE.LGT": (["architectural lighting", "lighting design", "emergency lighting"], ["SRC-PEC-METADATA", "SRC-PHILIPPINE-GREEN-BUILDING-CODE"], "lea_utility_endpoint"),
    "MEC.VEN": (["mechanical ventilation", "natural ventilation interface", "indoor air quality"], ["SRC-PHILIPPINE-GREEN-BUILDING-CODE", "SRC-PD-856-SANITATION-CODE"], "lea_utility_endpoint"),
    "CON.COM": (["commissioning", "functional testing", "handover"], ["SRC-CIAP-DOCUMENT-102"], "lea_construction_endpoint"),
    "OPS.PRM": (["preventive maintenance", "maintenance setup", "facility handover"], ["SRC-CIAP-DOCUMENT-102"], "lea_operations_endpoint"),
    "DIG.DTA": (["asset data", "digital handover", "COBie-like handover"], ["SRC-CIAP-DOCUMENT-102"], "lea_digital_handover_endpoint"),
}

IMPROVE_HINTS.update({
    "ARC.THE.DPR.PDP": (["parti", "parti diagram", "design concept diagram"], ["SRC-CHED-CMO-61-2017-BS-ARCH"], "lea_theory_endpoint"),
    "ARC.THE.DPR.AHA": (["axis", "hierarchy", "ordering axis"], ["SRC-CHED-CMO-61-2017-BS-ARCH"], "lea_theory_endpoint"),
    "ARC.THE.DPR.RPR": (["rhythm", "proportion", "design rhythm"], ["SRC-CHED-CMO-61-2017-BS-ARCH"], "lea_theory_endpoint"),
    "ARC.HIS.ANC.ETP": (["Egyptian architecture", "temple procession", "ancient Egyptian"], ["SRC-CHED-CMO-61-2017-BS-ARCH"], "lea_history_endpoint"),
    "ARC.HIS.ANC.GTO": (["Greek architecture", "classical orders", "Greek temple orders"], ["SRC-CHED-CMO-61-2017-BS-ARCH"], "lea_history_endpoint"),
    "ARC.HIS.MOD.ACR": (["Arts and Crafts", "craft reform", "anti-industrial design reform"], ["SRC-CHED-CMO-61-2017-BS-ARCH"], "lea_history_endpoint"),
    "ARC.HIS.MOD.BPM": (["Bauhaus", "Bauhaus pedagogy", "modern design education"], ["SRC-CHED-CMO-61-2017-BS-ARCH"], "lea_history_endpoint"),
    "ARC.HIS.MOD.ISC": (["International Style", "curtain wall modernism", "modernist glass box"], ["SRC-CHED-CMO-61-2017-BS-ARCH"], "lea_history_endpoint"),
    "ARC.SIT.GDA": (["grading", "site drainage", "access grading"], ["SRC-DHSUD-HLURB-CLUP-GUIDEBOOKS", "SRC-PD-1067-WATER-CODE"], "lea_site_endpoint"),
    "ARC.SIT.MIC": (["microclimate", "sun wind rain site response", "climate-responsive site planning"], ["SRC-CHED-CMO-61-2017-BS-ARCH", "SRC-PHILIPPINE-GREEN-BUILDING-CODE"], "lea_site_endpoint"),
    "ARC.INT.FIN": (["interior finishes", "finish schedule", "finish materials"], ["SRC-CHED-CMO-61-2017-BS-ARCH"], "lea_interiors_endpoint"),
    "ARC.INT.EQP": (["built-ins", "equipment layout", "interior equipment coordination"], ["SRC-BP-344-ACCESSIBILITY-LAW", "SRC-CHED-CMO-61-2017-BS-ARCH"], "lea_interiors_endpoint"),
    "ARC.MAT.DUR": (["durability", "material performance", "tropical durability"], ["SRC-PHILIPPINE-GREEN-BUILDING-CODE", "SRC-CHED-CMO-61-2017-BS-ARCH"], "lea_materials_endpoint"),
    "ARC.BLD.PER": (["building performance", "thermal visual acoustic performance", "integrated performance"], ["SRC-PHILIPPINE-GREEN-BUILDING-CODE"], "lea_performance_endpoint"),
    "ARC.SUS.PAS": (["passive design", "passive cooling", "passive environmental design"], ["SRC-PHILIPPINE-GREEN-BUILDING-CODE", "SRC-CHED-CMO-61-2017-BS-ARCH"], "lea_sustainability_endpoint"),
    "ARC.SUS.GRN": (["green building", "Philippine Green Building Code", "GB Code"], ["SRC-PHILIPPINE-GREEN-BUILDING-CODE"], "lea_sustainability_endpoint"),
    "LAW.NPC": (["National Plumbing Code", "NPCP", "plumbing code metadata"], ["SRC-NATIONAL-PLUMBING-CODE-METADATA"], "lea_law_source"),
    "LAW.PEC": (["Philippine Electrical Code", "PEC", "electrical code metadata"], ["SRC-PEC-METADATA"], "lea_law_source"),
    "COM.ACC.BFA": (["BP 344 family", "Philippine accessibility law", "barrier-free accessibility"], ["SRC-BP-344-ACCESSIBILITY-LAW"], "lea_source_endpoint"),
    "COM.BLD.NBC": (["NBCP", "PD 1096", "National Building Code of the Philippines"], ["SRC-PD-1096-NBCP"], "lea_source_endpoint"),
    "COM.FIR.LFR": (["local fire regulations", "BFP coordination", "Fire Code Philippines"], ["SRC-RA-9514-FIRE-CODE"], "lea_source_endpoint"),
    "URB.LUZ.CLU": (["CLUP", "Comprehensive Land Use Plan", "local land-use plan"], ["SRC-DHSUD-HLURB-CLUP-GUIDEBOOKS"], "lea_planning_endpoint"),
    "URB.LUZ.ZOO": (["zoning ordinance", "ZO", "local zoning ordinance"], ["SRC-DHSUD-HLURB-CLUP-GUIDEBOOKS", "SRC-RA-7160-LOCAL-GOVERNMENT-CODE"], "lea_planning_endpoint"),
    "CON.DMC": (["delivery methods", "construction contracts", "project delivery"], ["SRC-CIAP-DOCUMENT-102", "SRC-RA-9184-GPRA"], "lea_contract_endpoint"),
    "CON.QAQ": (["quality assurance", "quality control", "inspection and testing"], ["SRC-CIAP-DOCUMENT-102"], "lea_construction_endpoint"),
    "MAT.FIP.PDS": (["product data", "samples", "material submittals"], ["SRC-CIAP-DOCUMENT-102", "SRC-CHED-CMO-61-2017-BS-ARCH"], "lea_materials_endpoint"),
    "STR.SAF.LOP": (["load path", "structural load transfer", "architectural structural concept"], ["SRC-NSCP-METADATA"], "lea_structural_endpoint"),
    "STR.WSD": (["wind and seismic design", "NSCP lateral design metadata", "typhoon and earthquake loads"], ["SRC-NSCP-METADATA"], "lea_structural_endpoint"),
    "SAN.SFP": (["sanitary facility planning", "toilets", "public health fixtures"], ["SRC-PD-856-SANITATION-CODE"], "lea_sanitation_endpoint"),
    "OPS.AST.AIM": (["asset information management", "asset data handover", "digital handover"], ["SRC-CIAP-DOCUMENT-102"], "lea_handover_endpoint"),
})


def _source_path(source_id: str) -> str:
    return f"COM.STD.PHL.{SOURCE_NODE_SUFFIXES[source_id]}"


def _source_ids_for_paths(paths: Iterable[str]) -> list[str]:
    ids: list[str] = []
    for path in paths:
        if path.startswith("LAW.AAP") or path.startswith("ARC.PRC"):
            ids.append("SRC-RA-9266-ARCHITECTURE-ACT")
        elif path.startswith("LAW.PNB") or path.startswith("ARC.COD.BCA"):
            ids.append("SRC-PD-1096-NBCP")
        elif path.startswith("LAW.PFC") or path.startswith("ARC.FIR") or path.startswith("FLS"):
            ids.append("SRC-RA-9514-FIRE-CODE")
        elif path.startswith("LAW.PAL") or path.startswith("ARC.ACC"):
            ids.append("SRC-BP-344-ACCESSIBILITY-LAW")
        elif path.startswith("LAW.WCW"):
            ids.append("SRC-PD-1067-WATER-CODE")
        elif path.startswith("LAW.SCP") or path.startswith("SAN"):
            ids.append("SRC-PD-856-SANITATION-CODE")
        elif path.startswith("URB"):
            ids.append("SRC-DHSUD-HLURB-CLUP-GUIDEBOOKS")
        elif path.startswith("ARC.HIS") or path.startswith("FIG"):
            ids.append("SRC-NCCA-NATIONAL-ARTISTS-ARCHITECTURE")
        elif path.startswith("ARC.TAC") or path.startswith("SUS"):
            ids.append("SRC-PHILIPPINE-GREEN-BUILDING-CODE")
        elif path.startswith("ARC.BLD.STR") or path.startswith("STR"):
            ids.append("SRC-NSCP-METADATA")
        elif path.startswith("ARC.BLD.SRV"):
            ids.extend(["SRC-PEC-METADATA", "SRC-NATIONAL-PLUMBING-CODE-METADATA"])
        elif path.startswith("CON"):
            ids.append("SRC-CIAP-DOCUMENT-102")
        else:
            ids.append("SRC-PRC-ALE-TOS")
    return _dedupe(ids)


def enrich(payload: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    records = [dict(record) for record in payload["records"]]
    relationships = [dict(relationship) for relationship in payload["relationships"]]
    path_to_record = {record["path_code"]: record for record in records if record.get("path_code")}
    existing_edges = {(rel.get("from_id"), rel.get("predicate"), rel.get("to_id")) for rel in relationships}
    next_id = _next_domain_id(records)
    added_nodes: list[dict[str, Any]] = []
    added_relationships: list[dict[str, Any]] = []
    improved_nodes: set[str] = set()
    aliases_added = 0

    def add_edge(from_path: str, predicate: str, to_path: str, category: str, source_ids: list[str]) -> None:
        if from_path not in path_to_record or to_path not in path_to_record:
            missing = from_path if from_path not in path_to_record else to_path
            raise KeyError(f"Missing path_code for relationship endpoint: {missing}")
        from_record = path_to_record[from_path]
        to_record = path_to_record[to_path]
        key = (from_record["id"], predicate, to_record["id"])
        if key in existing_edges:
            return
        relationship = {
            "from_id": from_record["id"],
            "predicate": predicate,
            "to_id": to_record["id"],
            "governed": True,
            "generation_method": GENERATION_METHOD,
            "semantic_overlay_category": category,
            "source_family_ids": _dedupe(source_ids),
            "provenance_note": "Curated metadata-only LEA/ALE semantic relationship; no protected source payload, exam question, answer key, table, clause, figure, diagram, or reviewer text stored.",
        }
        relationships.append(relationship)
        added_relationships.append(relationship)
        existing_edges.add(key)

    def add_node(path_code: str, label: str, level: int, parent_path_code: str, definition: str, aliases: list[str], source_ids: list[str], node_kind: str, category: str) -> dict[str, Any]:
        nonlocal next_id, aliases_added
        if path_code in path_to_record:
            added = _merge_metadata(path_to_record[path_code], aliases, source_ids, node_kind)
            aliases_added += added
            if added:
                improved_nodes.add(path_code)
            return path_to_record[path_code]
        parent = path_to_record[parent_path_code]
        node_id = f"VTN-DOM-{next_id:07d}"
        next_id += 1
        full_aliases = _dedupe([path_code, label.lower(), *aliases])
        record = {
            "id": node_id,
            "canonical_id": node_id,
            "record_type": "BackboneNode",
            "review_status": "steward_admitted",
            "label": label,
            "pref_label": label,
            "definition": definition,
            "path_code": path_code,
            "level": level,
            "parent_path_code": parent_path_code,
            "owner": parent.get("owner") or OWNER,
            "steward": parent.get("steward") or parent.get("owner") or OWNER,
            "release_version": RELEASE_VERSION,
            "aliases": full_aliases,
            "scope_note": SCOPE_NOTE,
            "example_concepts": _dedupe([label.lower(), parent["label"].lower(), path_code.lower(), *aliases[:3]]),
            "generation_method": GENERATION_METHOD,
            "source_family_ids": _dedupe(source_ids),
            "provenance_note": "Kimi-guided, steward-authored metadata-only Philippine LEA/ALE graph enrichment; no protected source payload, exam question, answer key, table, clause, figure, diagram, or reviewer text stored.",
            "confidence": "high",
            "quality_signal": "curated_public_reference_overlay",
            "semantic_node_kind": node_kind,
            "lea_ale_category": category,
        }
        records.append(record)
        path_to_record[path_code] = record
        added_nodes.append(record)
        aliases_added += len(full_aliases)
        add_edge(parent_path_code, "broader_than", path_code, "hierarchy", source_ids)
        return record

    # Metadata-only source family nodes.
    add_node("COM.STD.PHL", "Philippine Architecture Licensure Source Families", 3, "COM.STD", "Metadata-only public/source-rights reference family for Philippine architecture licensure, building laws, codes, standards, and raw-source inventory signals.", ["Philippine architecture licensure sources", "LEA source families", "ALE source references"], ["SRC-PRC-ALE-TOS"], "standard_family", "source_reference")
    for reference in SOURCE_REFERENCES:
        source_id = reference["source_id"]
        suffix = SOURCE_NODE_SUFFIXES[source_id]
        add_node(_source_path(source_id), reference["source_family"], 4, "COM.STD.PHL", f"Metadata-only source-family reference for {reference['source_family']}; used for provenance and crosswalks without storing source payload text.", [source_id, reference["publisher_authority"], reference["source_family"]], [source_id], "standard_reference", "source_reference")
        add_edge(_source_path(source_id), "part_of", "COM.STD.PHL", "source_reference", [source_id])

    # Add subject nodes.
    created_subject_paths: list[str] = []
    paths_by_category: dict[str, list[str]] = {}
    source_ids_by_path: dict[str, list[str]] = {}
    for parent_path, node_kind, category, default_sources, items in NODE_GROUPS:
        for suffix, label, aliases, definition in items:
            path_code = f"{parent_path}.{suffix}"
            add_node(path_code, label, 4, parent_path, definition, aliases, default_sources, node_kind, category)
            created_subject_paths.append(path_code)
            paths_by_category.setdefault(category, []).append(path_code)
            source_ids_by_path[path_code] = default_sources
            for source_id in default_sources[:3]:
                if source_id in SOURCE_NODE_SUFFIXES:
                    add_edge(path_code, "maps_to_external_standard", _source_path(source_id), "source_reference", [source_id])

    # Improve existing endpoints with aliases and source-family IDs.
    for path_code, (aliases, source_ids, kind) in IMPROVE_HINTS.items():
        if path_code not in path_to_record:
            continue
        added = _merge_metadata(path_to_record[path_code], aliases, source_ids, kind)
        aliases_added += added
        if added:
            improved_nodes.add(path_code)
        for source_id in source_ids[:2]:
            if source_id in SOURCE_NODE_SUFFIXES:
                add_edge(path_code, "maps_to_external_standard", _source_path(source_id), "source_reference", [source_id])

    # Official ALE subject-frame overlays without flattening the graph into exam-day buckets.
    for target in ["ARC.REG.PHL.ALE", "ARC.REG.PHL.BLE", "ARC.REG.PHL.TOS", "ARC.REG.PHL.SUB", "ARC.REG.PHL.DAE", "ARC.REG.PHL.ELG"]:
        add_edge("ARC.REG.PHL", "has_facet", target, "lea_exam_meta", ["SRC-PRC-ALE-TOS", "SRC-RA-9266-ARCHITECTURE-ACT"])
    for target in [*paths_by_category.get("history_theory_philippine_architecture", [])[:38], "ARC.THE.DPR", "ARC.HIS.SEA", "FIG.ARD.CAA"]:
        add_edge("ARC.REG.PHL.PAH", "has_facet", target, "history_theory_philippine_architecture", _source_ids_for_paths([target]))
    for target in [*paths_by_category.get("materials_construction_specifications", []), *paths_by_category.get("structural_utilities_systems", []), "ARC.MAT", "ARC.BLD", "STR.SAF", "MEC.VEN", "ELE.LGT", "PLS.PWS", "FLS.ASS"]:
        add_edge("ARC.REG.PHL.PAS", "has_facet", target, "materials_structures_utilities", _source_ids_for_paths([target]))
    for target in [*paths_by_category.get("site_planning_urban_design", []), *paths_by_category.get("accessibility_universal_design", [])[:6], *paths_by_category.get("interiors_human_factors", []), "ARC.SIT", "URB.LUZ", "ARC.INT"]:
        add_edge("ARC.REG.PHL.PAD", "has_facet", target, "design_site_urban_interiors", _source_ids_for_paths([target]))
    for target in [*paths_by_category.get("professional_practice_contracts", []), *paths_by_category.get("philippine_law_code", [])[:34], "ARC.PRC", "LAW.AAP"]:
        add_edge("ARC.REG.PHL.RPS", "has_facet", target, "professional_practice_contracts", _source_ids_for_paths([target]))
    for target in [*paths_by_category.get("philippine_law_code", [])[10:], *paths_by_category.get("fire_life_safety", []), *paths_by_category.get("water_sanitation_public_health", []), "LAW.PNB", "LAW.PFC", "LAW.WCW", "LAW.SCP"]:
        add_edge("ARC.REG.PHL.PCC", "has_facet", target, "philippine_law_code", _source_ids_for_paths([target]))
    for target in paths_by_category.get("accessibility_universal_design", []):
        add_edge("ARC.REG.PHL.BAC", "has_facet", target, "accessibility_universal_design", ["SRC-BP-344-ACCESSIBILITY-LAW"])

    # Law and source-family governance/constraining overlays.
    law_governance = {
        "COM.STD.PHL.RAA": ["LAW.AAP", "ARC.REG.PHL.ALE", "ARC.REG.PHL.DAE", "ARC.REG.PHL.RLA", *paths_by_category.get("philippine_law_code", [])[:10]],
        "COM.STD.PHL.NBC": ["LAW.PNB", "ARC.COD.BCA", "ARC.COD.ZLU", *paths_by_category.get("philippine_law_code", [])[10:26], *paths_by_category.get("site_planning_urban_design", [])[0:10]],
        "COM.STD.PHL.FCP": ["LAW.PFC", "ARC.FIR", "FLS.EGR", "FLS.FDA", "FLS.ASS", *paths_by_category.get("fire_life_safety", [])],
        "COM.STD.PHL.BPA": ["LAW.PAL", "ARC.ACC", *paths_by_category.get("accessibility_universal_design", []), *paths_by_category.get("interiors_human_factors", [])[0:3]],
        "COM.STD.PHL.WCP": ["LAW.WCW", "URB.CRU.FLR", "ARC.SIT.SAN.DRN", *paths_by_category.get("water_sanitation_public_health", [])[0:6]],
        "COM.STD.PHL.SCP": ["LAW.SCP", "SAN.PHE", "PLS.PWS", "MEC.VEN", *paths_by_category.get("water_sanitation_public_health", [])[6:]],
        "COM.STD.PHL.CLU": ["URB.LUZ", "ARC.COD.ZLU", *paths_by_category.get("site_planning_urban_design", [])[10:]],
        "COM.STD.PHL.HER": ["LAW.HER", "ARC.HIS.SEA.PCH", "ARC.HIS.SEA.EQB", "FIG.WRK.BUI.SJA", "URB.LUZ.CLU.HRT"],
        "COM.STD.PHL.CIA": ["LAW.CON", "CON.DMC", "OPS.PRM", "DIG.DTA", *paths_by_category.get("professional_practice_contracts", [])],
    }
    for source_path, targets in law_governance.items():
        for target in targets:
            if target in path_to_record:
                pred = "governs" if target.startswith("LAW") or target.startswith("ARC.REG") else "constrains"
                add_edge(source_path, pred, target, "philippine_law_code", _source_ids_for_paths([source_path, target]))

    # Practical cross-domain semantic relationships.
    semantic_pairs: list[tuple[str, str, str, str]] = [
        ("LAW.PNB.OUC.OCL", "constrains", "LAW.PFC.OFS.OCL", "law_code_crosswalk"),
        ("LAW.PNB.OUC.OCL", "constrains", "LAW.PAL.ACR.ATO", "law_code_crosswalk"),
        ("LAW.PNB.OUC.OCL", "constrains", "LAW.PNB.OUC.PRK", "law_code_crosswalk"),
        ("LAW.PNB.PIE.BPE", "requires", "LAW.AAP.SAP.ADO", "permits_documents"),
        ("LAW.PNB.PIE.OPM", "requires", "LAW.PFC.FSI.FIC", "permits_fire_closeout"),
        ("LAW.PNB.PIE.OPM", "requires", "CON.DMC.DBB.ASB", "permits_closeout"),
        ("LAW.PNB.PIE.RCD", "constrains", "LAW.PEC", "referral_code_crosswalk"),
        ("LAW.PNB.PIE.RCD", "constrains", "LAW.NPC", "referral_code_crosswalk"),
        ("LAW.PNB.PIE.RCD", "constrains", "LAW.PFC", "referral_code_crosswalk"),
        ("LAW.PNB.PIE.ANP", "requires", "ARC.BLD.SRV.ELP", "utilities_permits"),
        ("LAW.PNB.PIE.ANP", "requires", "ARC.BLD.SRV.PWS", "utilities_permits"),
        ("LAW.PNB.PIE.ANP", "requires", "ARC.BLD.SRV.HVC", "utilities_permits"),
        ("LAW.PFC.FSI.FSE", "constrains", "LAW.PNB.PIE.BPE", "fire_permit_crosswalk"),
        ("LAW.PFC.FSI.FIC", "constrains", "LAW.PNB.PIE.OPM", "fire_permit_crosswalk"),
        ("LAW.PFC.OFS.EGR", "requires", "LAW.PFC.OFS.EAC", "egress_structure"),
        ("LAW.PFC.OFS.EGR", "requires", "LAW.PFC.OFS.EXT", "egress_structure"),
        ("LAW.PFC.OFS.EGR", "requires", "LAW.PFC.OFS.EXD", "egress_structure"),
        ("LAW.PFC.OFS.OCL", "constrains", "LAW.PFC.OFS.EGR", "egress_applicability"),
        ("LAW.PFC.OFS.TRD", "constrains", "ARC.SIT.SAN.PRG", "egress_design"),
        ("LAW.PFC.OFS.EGL", "requires", "ARC.BLD.SRV.LGT", "life_safety_utilities"),
        ("LAW.PFC.EPE.FAL", "requires", "ARC.BLD.SRV.ELP", "fire_alarm_utilities"),
        ("LAW.PFC.EPE.ASP", "requires", "ARC.BLD.SRV.PWS", "fire_protection_plumbing"),
        ("LAW.PFC.EPE.SMC", "requires", "ARC.BLD.SRV.HVC", "smoke_control_mechanical"),
        ("LAW.PFC.EPE.FST", "constrains", "ARC.BLD.SRV.SDR", "penetration_firestop"),
        ("LAW.PFC.EPE.FST", "constrains", "ARC.BLD.SRV.ELP", "penetration_firestop"),
        ("LAW.PAL.ACR.ARS", "requires", "LAW.PAL.ACR.RMP", "accessibility_route"),
        ("LAW.PAL.ACR.ARS", "requires", "LAW.PAL.ACR.APK", "accessibility_site"),
        ("LAW.PAL.ACR.ATO", "requires", "ARC.BLD.SRV.SDR", "accessibility_plumbing"),
        ("LAW.PAL.ACR.ELV", "constrains", "ARC.BLD.SRV.VTR", "accessibility_vertical_transport"),
        ("LAW.PAL.ACR.DCL", "constrains", "ARC.INT.PAC.ISP", "accessibility_interiors"),
        ("LAW.PAL.ACR.COR", "constrains", "ARC.INT.PAC.ISP", "accessibility_interiors"),
        ("LAW.PAL.ACR.SIG", "requires", "ARC.INT.PAC.WAY", "accessibility_wayfinding"),
        ("LAW.WCW.DRE.WAE", "constrains", "ARC.SIT.SAN.DRN", "water_site_planning"),
        ("LAW.WCW.DRE.FLD", "constrains", "URB.CRU.FLR", "water_resilience"),
        ("LAW.WCW.DRE.FLD", "constrains", "SUS.CLI.FAD", "water_resilience"),
        ("LAW.WCW.DRE.DRG", "requires", "ARC.SIT.SAN.SLP", "water_site_planning"),
        ("LAW.SCP.MPF.TOI", "requires", "PLS.PWS", "sanitation_plumbing"),
        ("LAW.SCP.MPF.SEW", "requires", "ARC.BLD.SRV.SDR", "sanitation_plumbing"),
        ("LAW.SCP.MPF.VHE", "requires", "MEC.VEN", "sanitation_ventilation"),
        ("LAW.SCP.MPF.SOL", "constrains", "ARC.SIT.SAN.FIR", "sanitation_site_operations"),
        ("URB.LUZ.CLU.LCC", "requires", "LAW.PNB.PIE.BPE", "zoning_permit_workflow"),
        ("URB.LUZ.CLU.LUC", "constrains", "LAW.PNB.OUC.OCL", "zoning_occupancy"),
        ("URB.LUZ.CLU.HRT", "constrains", "LAW.HER", "heritage_zoning"),
        ("ARC.SIT.SAN.PRG", "requires", "ARC.THE.DPR.FUN", "design_prerequisite"),
        ("ARC.SIT.SAN.ADJ", "requires", "ARC.SIT.SAN.PRG", "design_prerequisite"),
        ("ARC.SIT.SAN.BUB", "requires", "ARC.SIT.SAN.ADJ", "design_prerequisite"),
        ("ARC.SIT.SAN.WND", "requires", "ARC.TAC.NVS.XVN", "tropical_site_design"),
        ("ARC.SIT.SAN.SLP", "constrains", "LAW.PNB.OUC.YRD", "site_building_code"),
        ("ARC.TAC.SOS.SNP", "requires", "ARC.TAC.SOS.SHD", "tropical_design"),
        ("ARC.TAC.SOS.ORI", "requires", "ARC.SIT.SAN.WND", "tropical_design"),
        ("ARC.TAC.NVS.XVN", "requires", "ARC.TAC.NVS.OPN", "tropical_design"),
        ("ARC.HIS.SEA.BKS", "has_facet", "ARC.TAC.NVS.XVN", "vernacular_climate"),
        ("ARC.HIS.SEA.BKS", "has_facet", "ARC.TAC.NVS.VTC", "vernacular_climate"),
        ("ARC.HIS.SEA.BNB", "has_facet", "ARC.HIS.SEA.SCC", "philippine_history"),
        ("ARC.HIS.SEA.EQB", "has_facet", "ARC.BLD.STR.SDL", "history_structure"),
        ("ARC.HIS.SEA.CRG", "has_facet", "ARC.TAC.SOS.ORI", "critical_regionalism"),
        ("FIG.ARD.CAA.LOC", "has_facet", "FIG.WRK.BUI.CCP", "filipino_architect_work"),
        ("FIG.ARD.CAA.LOC", "has_facet", "FIG.WRK.BUI.PIC", "filipino_architect_work"),
        ("FIG.ARD.CAA.LOC", "has_facet", "FIG.WRK.BUI.FHA", "filipino_architect_work"),
        ("FIG.ARD.CAA.MAN", "has_facet", "FIG.WRK.BUI.COC", "filipino_architect_work"),
        ("FIG.ARD.CAA.SAN", "has_facet", "ARC.SIT.LAN", "filipino_architect_work"),
        ("FIG.WRK.BUI.SJA", "has_facet", "ARC.HIS.SEA.PCH", "philippine_history"),
        ("ARC.BLD.STR.SGL", "constrains", "ARC.SIT.SAN.BUB", "structure_design_coordination"),
        ("ARC.BLD.STR.SPN", "constrains", "ARC.INT.PAC.ISP", "structure_interiors"),
        ("ARC.BLD.STR.DEF", "constrains", "ARC.MAT.FIN.CEF", "structure_finishes"),
        ("ARC.BLD.STR.WDL", "constrains", "ARC.TAC.SOS.ORI", "structure_climate"),
        ("ARC.BLD.STR.SDL", "constrains", "LAW.PFC.EPE.FST", "structure_firestop"),
        ("ARC.MAT.CON.RCC", "requires", "ARC.BLD.STR.LDP", "materials_structure"),
        ("ARC.MAT.CON.JNT", "constrains", "ARC.MAT.CON.DPC", "materials_detailing"),
        ("ARC.MAT.STM.GLS", "constrains", "ARC.TAC.SOS.SHD", "envelope_tropical"),
        ("ARC.MAT.FIN.CEF", "requires", "ARC.BLD.SRV.LGT", "ceiling_services"),
        ("ARC.MAT.FIN.CEF", "requires", "LAW.PFC.EPE.ASP", "ceiling_fire_protection"),
        ("ARC.MAT.FIN.HDW", "constrains", "LAW.PFC.EPE.FDR", "hardware_life_safety"),
        ("ARC.INT.PAC.ACU", "requires", "MAT.INS.AIN", "interior_acoustics"),
        ("ARC.INT.PAC.IEQ", "requires", "MEC.VEN", "interior_environment"),
        ("ARC.INT.PAC.WAY", "requires", "LAW.PAL.ACR.SIG", "interior_wayfinding"),
        ("ARC.BLD.SRV.PWS", "requires", "LAW.SCP.MPF.PWS", "utilities_public_health"),
        ("ARC.BLD.SRV.SDR", "requires", "LAW.SCP.MPF.SEW", "utilities_public_health"),
        ("ARC.BLD.SRV.ELP", "requires", "LAW.PEC", "utilities_code"),
        ("ARC.BLD.SRV.HVC", "requires", "MEC.VEN", "utilities_mechanical"),
        ("ARC.BLD.SRV.BAS", "requires", "SMS.CSB", "smart_systems"),
        ("ARC.BLD.SRV.SEC", "requires", "SEC", "security_communications"),
        ("CON.DMC.DBB.BID", "requires", "LAW.AAP.SAP.ADO", "practice_contracts"),
        ("CON.DMC.DBB.ADD", "part_of", "CON.DMC.DBB.BID", "practice_contracts"),
        ("CON.DMC.DBB.RFI", "requires", "LAW.AAP.SAP.ADO", "construction_admin"),
        ("CON.DMC.DBB.SHD", "requires", "ARC.BLD.SRV.SEC", "construction_admin"),
        ("CON.DMC.DBB.SUB", "requires", "ARC.MAT.FIN.PNT", "construction_admin"),
        ("CON.DMC.DBB.PUN", "requires", "LAW.PNB.PIE.OPM", "closeout"),
        ("CON.DMC.DBB.ASB", "requires", "OPS.PRM", "handover"),
        ("CON.DMC.DBB.WAR", "requires", "OPS.PRM", "handover"),
        ("LAW.AAP.SAP.SPP", "constrains", "CON.DMC.DBB.BID", "professional_practice_contracts"),
        ("LAW.AAP.SAP.PFE", "constrains", "CON.DMC.DBB.PAY", "professional_practice_contracts"),
        ("LAW.AAP.SAP.ILP", "constrains", "LAW.AAP.SAP.ADO", "professional_responsibility"),
        ("LAW.AAP.SAP.AOR", "requires", "LAW.AAP.SAP.ADO", "professional_responsibility"),
        ("LAW.AAP.SAP.AIC", "requires", "CON.DMC.DBB.RFI", "construction_admin"),
    ]
    for from_path, predicate, to_path, category in semantic_pairs:
        add_edge(from_path, predicate, to_path, category, _source_ids_for_paths([from_path, to_path]))

    # Add source-reference edges for exact PH law/source nodes back to source-family nodes when not covered by groups.
    source_backlinks = {
        "LAW.AAP": ["SRC-RA-9266-ARCHITECTURE-ACT", "SRC-RA-9266-IRR-METADATA"],
        "LAW.PNB": ["SRC-PD-1096-NBCP", "SRC-PD-1096-REVISED-IRR-METADATA"],
        "LAW.PFC": ["SRC-RA-9514-FIRE-CODE"],
        "LAW.PAL": ["SRC-BP-344-ACCESSIBILITY-LAW"],
        "LAW.WCW": ["SRC-PD-1067-WATER-CODE"],
        "LAW.SCP": ["SRC-PD-856-SANITATION-CODE"],
        "LAW.CON": ["SRC-CIAP-DOCUMENT-102", "SRC-RA-9184-GPRA"],
        "LAW.HER": ["SRC-RA-10066-HERITAGE-ACT"],
        "ARC.REG.PHL": ["SRC-PRC-ARCHITECTURE-BOARD", "SRC-PRC-ALE-TOS"],
        "ARC.HIS.SEA": ["SRC-NCCA-NATIONAL-ARTISTS-ARCHITECTURE"],
        "URB.LUZ": ["SRC-DHSUD-HLURB-CLUP-GUIDEBOOKS", "SRC-RA-7160-LOCAL-GOVERNMENT-CODE"],
    }
    for path, source_ids in source_backlinks.items():
        for source_id in source_ids:
            add_edge(path, "maps_to_external_standard", _source_path(source_id), "source_reference", [source_id])

    new_payload = {**payload, "records": records, "relationships": relationships}
    records_by_id = {record["id"]: record for record in records}
    relationship_categories = Counter(rel.get("semantic_overlay_category") for rel in added_relationships)
    predicate_counts = Counter(rel.get("predicate") for rel in added_relationships)
    category_node_counts = Counter(record.get("lea_ale_category") for record in added_nodes)
    cross_domain = [
        rel for rel in added_relationships
        if records_by_id[rel["from_id"]]["path_code"].split(".")[0]
        != records_by_id[rel["to_id"]]["path_code"].split(".")[0]
    ]
    law_relationship_count = sum(
        1 for rel in added_relationships
        if records_by_id[rel["from_id"]]["path_code"].startswith(("LAW", "COM.STD.PHL"))
        or records_by_id[rel["to_id"]]["path_code"].startswith("LAW")
    )
    report = {
        "ok": True,
        "generation_method": GENERATION_METHOD,
        "input_record_count": len(payload["records"]),
        "output_record_count": len(records),
        "input_relationship_count": len(payload["relationships"]),
        "output_relationship_count": len(relationships),
        "added_node_count": len(added_nodes),
        "added_nodes_by_kind": dict(sorted(Counter(record.get("semantic_node_kind") for record in added_nodes).items())),
        "added_nodes_by_category": dict(sorted(category_node_counts.items())),
        "improved_existing_node_count": len(improved_nodes),
        "improved_existing_path_codes": sorted(improved_nodes),
        "added_relationship_count": len(added_relationships),
        "added_relationships_by_predicate": dict(sorted(predicate_counts.items())),
        "added_relationships_by_category": dict(sorted(relationship_categories.items())),
        "cross_domain_relationship_count": len(cross_domain),
        "philippine_law_code_relationship_count": law_relationship_count,
        "aliases_added_or_preserved_on_new_and_improved_nodes": aliases_added,
        "source_reference_ids": [row["source_id"] for row in SOURCE_REFERENCES],
        "raw_source_rights_classification": RAW_SOURCE_RIGHTS_CLASSIFICATION,
        "sample_added_path_codes": [record["path_code"] for record in added_nodes[:120]],
        "rights_safety": {
            "protected_source_payloads_ingested": False,
            "source_payload_mode": "labels_metadata_aliases_original_summaries_and_source_family_references_only",
            "exam_questions_or_answer_keys_ingested": False,
            "reviewer_text_ingested": False,
            "protected_code_tables_clauses_figures_or_diagrams_ingested": False,
            "neo4j_mutation": False,
            "kg_rebuild_reload_reset": False,
            "api_or_explorer_runtime_behavior_changed": False,
            "codex_spark_used_for_research_or_synthesis": False,
            "kimi_used_for_advisory_synthesis": True,
        },
    }
    return new_payload, report


def enrich_source_rights_registry(payload: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    rows = [dict(row) for row in payload.get("source_rights_registry", [])]
    existing_by_id = {row.get("source_id"): row for row in rows}
    existing = set(existing_by_id)
    added: list[dict[str, Any]] = []
    for reference in SOURCE_REFERENCES:
        if reference["source_id"] in existing:
            if reference["source_id"].startswith("SRC-RAW-ALE"):
                row = existing_by_id[reference["source_id"]]
                row["clearance_state"] = "clearance_required"
                row["source_rights_class"] = "reference_only"
                row["declared_use_boundary"] = "raw-source custody metadata only; no PDF/spreadsheet payload, no reviewer text, no exam questions, no answer keys, no tables, no figures, no diagrams"
                row["blocking_notes"] = "raw-source content is treated as protected/unknown-rights and must not be ingested without explicit rights review"
            continue
        row = {
            "source_id": reference["source_id"],
            "source_family": reference["source_family"],
            "publisher_authority": reference["publisher_authority"],
            "edition_version_effective_date": "admission-time verification required",
            "official_url": reference["official_url"],
            "source_rights_class": "reference_only",
            "clearance_state": "planning_reference_only",
            "intended_vitruvius_use": reference["intended_vitruvius_use"],
            "steward_owner": OWNER,
            "declared_use_boundary": "metadata-only labels, aliases, public titles, and source-family references; no source text, exam questions, answer keys, reviewer text, tables, clauses, figures, diagrams, or protected code payload ingest",
            "currentness_check_date": "2026-04-29",
            "update_cadence": "before source admission and per LEA/ALE taxonomy release",
            "blocking_notes": "content ingest blocked until explicit rights/license/legal review; this enrichment uses metadata-only source labels and steward-authored original summaries",
        }
        if reference["source_id"].startswith("SRC-RAW-ALE"):
            row["clearance_state"] = "clearance_required"
            row["source_rights_class"] = "reference_only"
            row["declared_use_boundary"] = "raw-source custody metadata only; no PDF/spreadsheet payload, no reviewer text, no exam questions, no answer keys, no tables, no figures, no diagrams"
            row["blocking_notes"] = "raw-source content is treated as protected/unknown-rights and must not be ingested without explicit rights review"
        rows.append(row)
        added.append(row)
        existing.add(reference["source_id"])
    return {**payload, "source_rights_registry": rows}, {
        "ok": True,
        "generation_method": GENERATION_METHOD,
        "input_source_reference_count": len(payload.get("source_rights_registry", [])),
        "output_source_reference_count": len(rows),
        "added_source_reference_count": len(added),
        "added_source_reference_ids": [row["source_id"] for row in added],
        "raw_source_rights_classification": RAW_SOURCE_RIGHTS_CLASSIFICATION,
        "rights_safety": {
            "protected_source_payloads_ingested": False,
            "source_payload_mode": "source_family_metadata_only",
            "content_ingest_rows_added": False,
        },
    }


def _next_domain_id(records: list[dict[str, Any]]) -> int:
    return max(int(record["id"].split("-")[-1]) for record in records if str(record.get("id", "")).startswith("VTN-DOM-")) + 1


def _merge_metadata(record: dict[str, Any], aliases: list[str], source_ids: list[str], node_kind: str) -> int:
    alias_count = _merge_list(record, "aliases", aliases)
    _merge_list(record, "source_family_ids", source_ids)
    record.setdefault("provenance_note", "Metadata-only LEA/ALE semantic overlay enrichment; no protected source payload stored.")
    record.setdefault("quality_signal", "curated_public_reference_overlay")
    record.setdefault("confidence", "high")
    record.setdefault("semantic_node_kind", node_kind)
    return alias_count


def _merge_list(record: dict[str, Any], key: str, values: list[str]) -> int:
    existing = list(record.get(key, [])) if isinstance(record.get(key, []), list) else []
    before = len(existing)
    record[key] = _dedupe([*existing, *values])
    return len(record[key]) - before


def _dedupe(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for value in values:
        text = str(value).strip()
        if not text or text in seen:
            continue
        seen.add(text)
        out.append(text)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Add Kimi-guided Philippine LEA/ALE semantic graph enrichment to the file-backed AEC-MEPFS backbone.")
    parser.add_argument("--fixture", default="scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json")
    parser.add_argument("--source-rights-registry", default=".ai/03_plans/AEC-MEPFS-Backbone/registry-candidates/source-rights-registry.json")
    parser.add_argument("--report", required=True)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    fixture_path = Path(args.fixture)
    registry_path = Path(args.source_rights_registry)
    payload = json.loads(fixture_path.read_text(encoding="utf-8"))
    enriched, graph_report = enrich(payload)
    registry_payload = json.loads(registry_path.read_text(encoding="utf-8"))
    enriched_registry, source_report = enrich_source_rights_registry(registry_payload)
    report = {"ok": graph_report["ok"] and source_report["ok"], "graph": graph_report, "source_rights_registry": source_report}
    report_path = Path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.write:
        fixture_path.write_text(json.dumps(enriched, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        registry_path.write_text(json.dumps(enriched_registry, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
