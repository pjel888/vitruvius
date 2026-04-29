from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

from vitruvius.kg.lea_ale_semantic_enrichment import OWNER

GENERATION_METHOD = (
    "steward_governed_lea_ale_resolver_deepening_from_kimi_guided_"
    "public_query_path_and_source_rights_review"
)
RELEASE_VERSION = "0.8.0"
SCOPE_NOTE = (
    "Kimi-guided LEA/ALE resolver and building-technology deepening using metadata-only "
    "public source-family references and steward-authored original summaries; no protected "
    "source payloads, reviewer text, exam questions, answer keys, code clauses, tables, figures, "
    "or diagrams stored."
)
DEFAULT_FIXTURE = Path("scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json")
DEFAULT_SOURCE_RIGHTS = Path(".ai/03_plans/AEC-MEPFS-Backbone/registry-candidates/source-rights-registry.json")
DEFAULT_RESOLVER_FIXTURE = Path("scripts/tests/fixtures/aec_mepfs_backbone/valid_readiness_s2.json")

SOURCE_REFERENCES: list[dict[str, str]] = [
    {"source_id": "SRC-BFP-FIRE-SAFETY-CLEARANCE-METADATA", "source_family": "BFP public fire safety clearance and inspection metadata", "publisher_authority": "Bureau of Fire Protection", "official_url": "https://bfp.gov.ph/", "intended_vitruvius_use": "metadata-only fire safety evaluation, inspection certificate, fire alarm, sprinkler, standpipe, and closeout crosswalks"},
    {"source_id": "SRC-NCDA-BP344-IRR-METADATA", "source_family": "NCDA public BP 344 accessibility IRR metadata", "publisher_authority": "National Council on Disability Affairs", "official_url": "https://ncda.gov.ph/disability-laws/implementing-rules-and-regulations-irr/irr-of-bp-344/", "intended_vitruvius_use": "metadata-only accessibility route, ramp, parking, toilet, signage, and public-building crosswalks"},
    {"source_id": "SRC-NWRB-WATER-PERMIT-METADATA", "source_family": "NWRB water permit and Water Code implementation metadata", "publisher_authority": "National Water Resources Board", "official_url": "https://nwrb.gov.ph/", "intended_vitruvius_use": "metadata-only water rights, water permit, waterways, easement, drainage, and flood-risk crosswalks"},
    {"source_id": "SRC-DOH-SANITATION-IMPLEMENTING-RULES-METADATA", "source_family": "DOH sanitation and public-health implementing-rule metadata", "publisher_authority": "Department of Health", "official_url": "https://doh.gov.ph/", "intended_vitruvius_use": "metadata-only sanitation, public health, toilets, wastewater, ventilation, and local health authority crosswalks"},
    {"source_id": "SRC-DPWH-BUILDING-PERMIT-NBCDO-METADATA", "source_family": "DPWH NBCDO building permit and National Building Code administration metadata", "publisher_authority": "Department of Public Works and Highways", "official_url": "https://www.dpwh.gov.ph/DPWH/references/laws_codes_orders/PD1096", "intended_vitruvius_use": "metadata-only building permit, occupancy permit, building official, referral code, and plan-review crosswalks"},
    {"source_id": "SRC-DHSUD-ZONING-LOCATIONAL-CLEARANCE-METADATA", "source_family": "DHSUD/HLURB zoning and locational-clearance public metadata", "publisher_authority": "Department of Human Settlements and Urban Development", "official_url": "https://dhsud.gov.ph/", "intended_vitruvius_use": "metadata-only CLUP, zoning ordinance, locational clearance, land-use, and site-planning crosswalks"},
    {"source_id": "SRC-CHED-BSARCH-BUILDING-TECHNOLOGY-METADATA", "source_family": "CHED BS Architecture building technology and utilities curriculum metadata", "publisher_authority": "Commission on Higher Education", "official_url": "https://ched.gov.ph/wp-content/uploads/2017/10/CMO-61-s.-2017.pdf", "intended_vitruvius_use": "metadata-only architectural technology, utilities, structures, materials, and professional-practice learning outcome crosswalks"},
    {"source_id": "SRC-NCCA-PHILIPPINE-BUILT-HERITAGE-METADATA", "source_family": "NCCA public Philippine built heritage and National Artist metadata", "publisher_authority": "National Commission for Culture and the Arts", "official_url": "https://ncca.gov.ph/about-culture-and-arts/culture-profile/national-artists-of-the-philippines/", "intended_vitruvius_use": "metadata-only Philippine architecture history, National Artist, major work, heritage, and cultural-expression crosswalks"},
    {"source_id": "SRC-CIAP-CONSTRUCTION-ADMIN-METADATA", "source_family": "CIAP construction administration and contract metadata", "publisher_authority": "Construction Industry Authority of the Philippines", "official_url": "https://construction.gov.ph/", "intended_vitruvius_use": "metadata-only RFI, submittal, change order, punch list, warranty, and contract administration crosswalks"},
    {"source_id": "SRC-DPWH-PHILIPPINE-GREEN-BUILDING-CODE-METADATA", "source_family": "DPWH Philippine Green Building Code public metadata", "publisher_authority": "Department of Public Works and Highways", "official_url": "https://www.dpwh.gov.ph/DPWH/references/laws_codes_orders/pgbc", "intended_vitruvius_use": "metadata-only tropical design, indoor environmental quality, energy efficiency, water efficiency, and building systems crosswalks"},
    {"source_id": "SRC-RAW-LEA-UTILITIES-MOCK-TEST-PDF", "source_family": "Building Laws and Utilities Mock Test with Key PDF (local custody record)", "publisher_authority": "Unknown third-party / rights review required", "official_url": "local custody path only: 001_Raw-Source-Layer/005-Utilities/Building Laws _ Utilities Mock Test with Key.pdf", "intended_vitruvius_use": "metadata-only raw-source inventory signal; no PDF payload, mock-test text, questions, answer keys, figures, diagrams, tables, or explanations ingested"},
    {"source_id": "SRC-RAW-LEA-HISTORY-SAMPLE-EXAM-PDF", "source_family": "History of Architecture Sample Exam PDF (local custody record)", "publisher_authority": "Unknown third-party / rights review required", "official_url": "local custody path only: 001_Raw-Source-Layer/002-History/History of Architecture Sample Exam.pdf", "intended_vitruvius_use": "metadata-only raw-source inventory signal; no exam questions, answers, reviewer text, tables, figures, diagrams, or explanations ingested"},
    {"source_id": "SRC-RAW-LEA-THEORY-REVIEWER-PDF", "source_family": "Theory of Architecture Reviewer PDF (local custody record)", "publisher_authority": "Unknown third-party / rights review required", "official_url": "local custody path only: 001_Raw-Source-Layer/002-History/Theory of Architecture Reviewer.pdf", "intended_vitruvius_use": "metadata-only raw-source inventory signal; no reviewer text, questions, answer keys, figures, diagrams, or tables ingested"},
    {"source_id": "SRC-RAW-LEA-SALVAN-HISTORY-BOOK-PDF", "source_family": "George Salvan Architectural History Book PDF (local custody record)", "publisher_authority": "Private/copyrighted book candidate / rights review required", "official_url": "local custody path only: 001_Raw-Source-Layer/002-History/George Salvan Architectural Character and the History of Architecture.pdf", "intended_vitruvius_use": "metadata-only raw-source inventory signal; no book text, diagrams, figures, tables, or explanations ingested"},
    {"source_id": "SRC-RAW-LEA-FILIPINO-ARCHITECTURE-PDF", "source_family": "Filipino Architecture PDF (local custody record)", "publisher_authority": "Unknown/private source candidate / rights review required", "official_url": "local custody path only: 001_Raw-Source-Layer/002-History/Filipino Architecture.pdf", "intended_vitruvius_use": "metadata-only raw-source inventory signal; no source text, diagrams, figures, tables, or explanations ingested"},
    {"source_id": "SRC-RAW-LEA-TROPICAL-ARCHITECTURE-PDF", "source_family": "TOA 4 Tropical Architecture PDF (local custody record)", "publisher_authority": "Unknown/private handout or reviewer candidate / rights review required", "official_url": "local custody path only: 001_Raw-Source-Layer/003-Theory/TOA 4 (Tropical Architecture).pdf", "intended_vitruvius_use": "metadata-only raw-source inventory signal; no handout/reviewer payload, diagrams, figures, tables, or explanations ingested"},
]

SOURCE_NODE_SUFFIXES = {
    "SRC-BFP-FIRE-SAFETY-CLEARANCE-METADATA": "BFM",
    "SRC-NCDA-BP344-IRR-METADATA": "NCD",
    "SRC-NWRB-WATER-PERMIT-METADATA": "NWR",
    "SRC-DOH-SANITATION-IMPLEMENTING-RULES-METADATA": "DOH",
    "SRC-DPWH-BUILDING-PERMIT-NBCDO-METADATA": "DBP",
    "SRC-DHSUD-ZONING-LOCATIONAL-CLEARANCE-METADATA": "DHS",
    "SRC-CHED-BSARCH-BUILDING-TECHNOLOGY-METADATA": "CBT",
    "SRC-NCCA-PHILIPPINE-BUILT-HERITAGE-METADATA": "NBH",
    "SRC-CIAP-CONSTRUCTION-ADMIN-METADATA": "CCA",
    "SRC-DPWH-PHILIPPINE-GREEN-BUILDING-CODE-METADATA": "DGB",
}

RAW_SOURCE_RIGHTS_CLASSIFICATION = [
    {"path": "001_Raw-Source-Layer/005-Utilities/Building Laws _ Utilities Mock Test with Key.pdf", "classification": "private_or_third_party_mock_test_with_answer_key", "allowed_use": "filename metadata and weak topic signal only; no questions, answer keys, explanations, diagrams, figures, or tables ingested", "source_id": "SRC-RAW-LEA-UTILITIES-MOCK-TEST-PDF"},
    {"path": "001_Raw-Source-Layer/002-History/History of Architecture Sample Exam.pdf", "classification": "private_or_third_party_sample_exam", "allowed_use": "filename metadata only; no exam questions, answers, reviewer text, diagrams, figures, or tables ingested", "source_id": "SRC-RAW-LEA-HISTORY-SAMPLE-EXAM-PDF"},
    {"path": "001_Raw-Source-Layer/002-History/Theory of Architecture Reviewer.pdf", "classification": "private_or_third_party_reviewer_pdf", "allowed_use": "filename metadata and weak topic signal only; no reviewer text, questions, answer keys, diagrams, figures, or tables ingested", "source_id": "SRC-RAW-LEA-THEORY-REVIEWER-PDF"},
    {"path": "001_Raw-Source-Layer/002-History/George Salvan Architectural Character and the History of Architecture.pdf", "classification": "private_copyrighted_book_candidate", "allowed_use": "filename metadata only; no book text, diagrams, figures, tables, or explanations ingested", "source_id": "SRC-RAW-LEA-SALVAN-HISTORY-BOOK-PDF"},
    {"path": "001_Raw-Source-Layer/002-History/Filipino Architecture.pdf", "classification": "unknown_or_private_rights_architecture_reference", "allowed_use": "filename metadata only; no source text, diagrams, figures, tables, or explanations ingested", "source_id": "SRC-RAW-LEA-FILIPINO-ARCHITECTURE-PDF"},
    {"path": "001_Raw-Source-Layer/003-Theory/TOA 4 (Tropical Architecture).pdf", "classification": "unknown_or_private_handout_reviewer_candidate", "allowed_use": "filename metadata and weak topic signal only; no handout/reviewer payload, diagrams, figures, tables, or explanations ingested", "source_id": "SRC-RAW-LEA-TROPICAL-ARCHITECTURE-PDF"},
]

NODE_GROUPS: list[tuple[str, str, str, list[str], list[tuple[str, str, list[str], str]]]] = [
    ("ARC.BLD.SRV", "lea_utilities_coordination_detail", "utilities_building_systems", ["SRC-CHED-BSARCH-BUILDING-TECHNOLOGY-METADATA", "SRC-DPWH-BUILDING-PERMIT-NBCDO-METADATA"], [
        ("UCO", "Utility Coordination", ["MEP coordination", "building services coordination"], "Architectural coordination of plumbing, electrical, mechanical, fire protection, ICT, security, access, and maintainability requirements."),
        ("ERP", "Equipment Room Planning", ["equipment room", "service room planning"], "Planning of rooms for building systems equipment, access, clearances, ventilation, structure, and maintenance."),
        ("SHA", "Shaft Planning", ["shaft planning", "service shaft"], "Architectural planning of vertical service shafts for ducts, pipes, cables, risers, fire protection, and access."),
        ("RIS", "Riser Planning", ["riser planning", "utility riser"], "Coordination of vertical pipe, conduit, cable, and protection risers through stacked floors."),
        ("PLC", "Ceiling Plenum Coordination", ["ceiling plenum", "above-ceiling coordination"], "Coordination of services above ceilings, including ducts, pipes, trays, sprinklers, detectors, lights, and access zones."),
        ("ACP", "Access Panel", ["access panel", "service access panel"], "Architectural access opening for valves, dampers, cleanouts, junctions, and concealed maintainable components."),
        ("MAC", "Maintenance Access", ["maintenance clearance", "service clearance"], "Operational access and clearances needed for inspection, testing, repair, replacement, and safe facility upkeep."),
        ("RCP", "Reflected Ceiling Plan Coordination", ["RCP coordination", "reflected ceiling plan"], "Ceiling-document coordination of lighting, diffusers, sprinklers, detectors, speakers, access panels, and finishes."),
        ("SCH", "Equipment Schedule Coordination", ["equipment schedule", "equipment list"], "Documentation coordination of equipment identifiers, capacities, locations, access needs, and specification references."),
        ("SEC", "Architectural Section Utility Coordination", ["section coordination", "utility section coordination"], "Use of building sections to coordinate vertical clearances, shafts, plenums, risers, structural zones, and service routes."),
    ]),
    ("ARC.BLD.SRV", "lea_plumbing_sanitary_detail", "utilities_building_systems", ["SRC-NATIONAL-PLUMBING-CODE-METADATA", "SRC-DOH-SANITATION-IMPLEMENTING-RULES-METADATA", "SRC-NWRB-WATER-PERMIT-METADATA"], [
        ("PFP", "Plumbing Fixture Planning", ["fixture planning", "plumbing fixtures"], "Placement and grouping of fixtures in relation to occupancy, accessibility, water supply, drainage, venting, and maintenance."),
        ("WSD", "Water Supply Distribution", ["water distribution", "domestic water distribution"], "Distribution of potable water through mains, branches, risers, valves, and fixtures."),
        ("STD", "Storm Drainage", ["storm drainage", "roof and site drainage"], "Collection and routing of rainwater from roofs, decks, hardscape, and site areas."),
        ("VST", "Vent Stack", ["plumbing vent stack", "sanitary vent"], "Vent piping concept that supports trap seal protection and sanitary drainage performance."),
        ("CLO", "Cleanout", ["cleanout", "drain cleanout"], "Accessible fitting for inspection and clearing of sanitary or storm drainage lines."),
        ("SPS", "Septic System", ["septic tank system", "onsite wastewater system"], "Onsite wastewater treatment and disposal system relevant where sewer connections are unavailable."),
        ("SWC", "Sewer Connection", ["sewer connection", "sewer service"], "Connection between building sanitary drainage and a public or private sewerage system."),
        ("GRI", "Grease Interceptor", ["grease trap", "grease interceptor"], "Plumbing pretreatment device for grease-laden wastewater from food-service or similar uses."),
        ("BFP", "Backflow Prevention", ["backflow preventer", "cross-connection control"], "Protection device or strategy preventing reverse flow contamination of potable water systems."),
    ]),
    ("ARC.BLD.SRV", "lea_electrical_detail", "utilities_building_systems", ["SRC-PEC-METADATA", "SRC-DPWH-BUILDING-PERMIT-NBCDO-METADATA"], [
        ("ESE", "Electrical Service Entrance", ["service entrance", "electrical service"], "Entry and metering point for electrical service coordinated with utility, clearances, safety, and building layout."),
        ("MDP", "Main Distribution Panel", ["MDP", "main switchboard", "main distribution board"], "Primary electrical distribution equipment coordinated with rooms, access, ventilation, and service routes."),
        ("PNB", "Panelboard", ["panelboard", "distribution panel"], "Electrical distribution panel serving branch circuits and requiring code-compliant location and working clearance."),
        ("BRC", "Branch Circuit", ["branch circuit", "final circuit"], "Circuit serving outlets, lighting, equipment, and loads from a panelboard."),
        ("LTC", "Lighting Circuit", ["lighting circuit", "lighting branch circuit"], "Circuit serving luminaires, controls, and emergency/normal lighting coordination."),
        ("ESP", "Exit Sign Power", ["exit sign power", "egress sign power"], "Electrical supply and backup coordination for exit signage and wayfinding during emergencies."),
        ("GBN", "Grounding And Bonding", ["grounding", "bonding", "earthing"], "Electrical safety coordination for fault-current paths, equipment bonding, and grounding systems."),
        ("TRR", "Transformer Room", ["transformer room", "electrical transformer room"], "Room or enclosure for transformers requiring ventilation, access, fire separation, and service coordination."),
        ("GNR", "Generator Room", ["generator room", "genset room"], "Emergency or standby generator space coordinated with fuel, exhaust, ventilation, acoustics, access, and life safety."),
    ]),
    ("ARC.BLD.SRV", "lea_mechanical_detail", "utilities_building_systems", ["SRC-CHED-BSARCH-BUILDING-TECHNOLOGY-METADATA", "SRC-DPWH-PHILIPPINE-GREEN-BUILDING-CODE-METADATA"], [
        ("MER", "Mechanical Equipment Room", ["mechanical room", "plant room"], "Room for HVAC or mechanical equipment requiring access, ventilation, structural support, drainage, and acoustics coordination."),
        ("AHU", "Air Handling Unit", ["AHU", "air handler"], "HVAC equipment for moving and conditioning air, coordinated with plant rooms, ducts, drains, controls, and maintenance."),
        ("CDU", "Condensing Unit", ["condensing unit", "outdoor HVAC unit"], "Outdoor or service-area refrigeration equipment coordinated with heat rejection, access, noise, and placement."),
        ("DRT", "Duct Routing", ["duct routing", "duct layout"], "Routing of supply, return, exhaust, and fresh-air ductwork through ceiling, shafts, and service zones."),
        ("SAF", "Supply Air Distribution", ["supply air", "air supply"], "Distribution of conditioned or ventilation air to occupied spaces through ducts, diffusers, and grilles."),
        ("RAF", "Return Air Path", ["return air", "return path"], "Air path returning room air to mechanical equipment or relief/exhaust systems."),
        ("EAF", "Exhaust Air", ["exhaust air", "exhaust ventilation"], "Removal of air from toilets, kitchens, parking, service rooms, or other spaces requiring extraction."),
        ("FAI", "Fresh Air Intake", ["outdoor air intake", "fresh air intake"], "Intake location and pathway for outdoor air coordinated with pollution sources, access, rain, and security."),
        ("NVP", "Natural Ventilation Path", ["natural ventilation path", "airflow path"], "Passive airflow route connecting openings, rooms, pressure zones, and climate-responsive design."),
        ("IAQ", "Indoor Air Quality Coordination", ["IAQ coordination", "healthy indoor air"], "Design coordination for ventilation, filtration, pollutant control, moisture, materials, and occupant health."),
    ]),
    ("ARC.BLD.SRV", "lea_fire_vertical_ict_detail", "utilities_building_systems", ["SRC-BFP-FIRE-SAFETY-CLEARANCE-METADATA", "SRC-PEC-METADATA", "SRC-CHED-BSARCH-BUILDING-TECHNOLOGY-METADATA"], [
        ("FPR", "Fire Pump Room", ["fire pump room", "pump room"], "Room for fire pump equipment coordinated with water supply, power, drainage, access, ventilation, and fire protection."),
        ("SPR", "Sprinkler Riser", ["sprinkler riser", "sprinkler valve riser"], "Vertical or floor-level sprinkler system riser coordinated with shafts, valve access, alarms, and fire inspection."),
        ("STR", "Standpipe Riser", ["standpipe riser", "fire hose riser"], "Vertical standpipe piping coordinated with stairs, fire department access, shafts, and floor control."),
        ("FAP", "Fire Alarm Control Panel", ["FACP", "fire alarm panel"], "Fire alarm control equipment coordinated with power, communications, BFP response, and accessible monitoring location."),
        ("EMR", "Elevator Machine Room", ["elevator machine room", "lift machine room"], "Elevator equipment room coordinated with hoistway, access, ventilation, fire protection, and structural support."),
        ("MRL", "Machine Room Less Elevator", ["MRL elevator", "machine-room-less elevator"], "Elevator configuration reducing separate machine-room area but still requiring coordination of access and controls."),
        ("ELB", "Elevator Lobby", ["elevator lobby", "lift lobby"], "Lobby space coordinating vertical circulation, accessibility, fire/life safety, wayfinding, and core planning."),
        ("HSW", "Hoistway", ["elevator shaft", "hoistway"], "Vertical shaft for elevator travel coordinated with structure, fire separation, pits, overhead, and clearances."),
        ("ECP", "Escalator Planning", ["escalator planning", "moving stair planning"], "Planning of escalator placement, circulation flow, structural openings, safety, and maintenance access."),
        ("ICT", "ICT Room", ["telecommunications room", "ICT room", "data room"], "Room for communications equipment, racks, patching, power, cooling, pathways, and security."),
        ("CMR", "Communications Riser", ["telecom riser", "communications riser"], "Vertical pathway for data, voice, security, and low-voltage cabling."),
        ("SCR", "Security Control Room", ["security room", "control room"], "Operational room coordinating CCTV, access control, alarms, communications, power, and staff visibility."),
        ("CTV", "CCTV System", ["CCTV", "video surveillance"], "Security video system coordinated with device locations, power, network, privacy, and operations."),
        ("ACS", "Access Control System", ["access control", "card access"], "Security system coordinating controlled doors, hardware, power, data, egress, and operations."),
    ]),
    ("ARC.BLD.STR", "lea_structural_system_detail", "structural_concepts", ["SRC-NSCP-METADATA", "SRC-CHED-BSARCH-BUILDING-TECHNOLOGY-METADATA"], [
        ("SCA", "Structural Concept For Architects", ["structural concept", "architectural structural concept"], "Architectural-level understanding of structural systems, loads, spans, grids, stability, and coordination without engineering calculations."),
        ("TRA", "Tributary Area", ["tributary area", "load tributary area"], "Conceptual area contributing load to a structural member, useful for architectural structural reasoning."),
        ("CGD", "Column Grid", ["column grid", "grid line layout"], "Regular or irregular grid that locates columns and organizes spans, bays, parking, rooms, and services."),
        ("BAY", "Structural Bay", ["bay", "structural module"], "Area or module between structural supports that influences planning, facade rhythm, and construction economy."),
        ("BEM", "Beam", ["beam", "horizontal structural member"], "Horizontal member carrying loads to supports and influencing ceiling depth, openings, and services."),
        ("GIR", "Girder", ["girder", "primary beam"], "Primary beam supporting secondary framing and coordinating with spans, depth, and architectural clearances."),
        ("JOI", "Joist", ["joist", "secondary joist"], "Secondary repetitive framing member supporting floors, roofs, or ceilings."),
        ("SLB", "Slab", ["slab", "floor slab"], "Plate-like floor or roof structural element coordinated with spans, openings, penetrations, and finishes."),
        ("OWS", "One Way Slab", ["one-way slab", "one way slab"], "Slab behavior concept where load is primarily carried in one direction."),
        ("TWS", "Two Way Slab", ["two-way slab", "two way slab"], "Slab behavior concept where load is carried in two directions to supports."),
        ("COL", "Column", ["column", "vertical structural member"], "Vertical compression member coordinating with grids, rooms, parking, facade, and foundations."),
        ("SHW", "Shear Wall", ["shear wall", "lateral wall"], "Wall resisting lateral loads and affecting layouts, cores, openings, and seismic/wind coordination."),
        ("BRW", "Bearing Wall", ["bearing wall", "load-bearing wall"], "Wall carrying gravity loads and constraining openings, planning, and alteration flexibility."),
        ("RTW", "Retaining Wall", ["retaining wall", "earth retaining wall"], "Wall retaining soil or grade differences and coordinating drainage, site levels, and structure."),
        ("FDS", "Foundation System", ["foundation system", "substructure"], "System transferring loads to soil or rock and coordinating with site, soil, basements, and utilities."),
        ("FOO", "Footing", ["footing", "spread footing"], "Foundation element spreading column or wall loads to soil."),
        ("IFT", "Isolated Footing", ["isolated footing", "pad footing"], "Footing supporting a single column or point load."),
        ("CBF", "Combined Footing", ["combined footing", "shared footing"], "Footing supporting multiple columns where spacing or property constraints require shared support."),
        ("SPF", "Strip Footing", ["strip footing", "wall footing"], "Continuous footing supporting walls or lines of closely spaced supports."),
        ("MTF", "Mat Foundation", ["mat foundation", "raft foundation"], "Large foundation slab supporting multiple columns or walls over a broad area."),
        ("PIF", "Pile Foundation", ["pile foundation", "deep foundation"], "Deep foundation transferring loads to deeper strata where shallow bearing is insufficient."),
        ("FSS", "Foundation Settlement", ["settlement", "differential settlement"], "Foundation movement concern affecting finishes, doors, partitions, utilities, and serviceability."),
        ("LST", "Lateral Stability", ["lateral stability", "stability system"], "Resistance to wind and seismic actions through frames, walls, bracing, cores, or diaphragms."),
        ("BRF", "Braced Frame", ["braced frame", "bracing system"], "Frame stabilized by diagonal or other bracing members, affecting openings and planning."),
        ("MFR", "Moment Frame", ["moment frame", "rigid frame"], "Frame resisting lateral loads through beam-column joint action and member stiffness."),
        ("TRU", "Truss", ["truss", "triangulated frame"], "Triangulated structural system useful for roofs, spans, and expressive architectural form."),
        ("ARS", "Arch Structure", ["arch", "arch structure"], "Curved compression form spanning an opening or space and influencing architectural expression."),
        ("SHL", "Shell Structure", ["shell structure", "thin shell"], "Curved surface structure carrying loads through shape and surface action."),
        ("TNS", "Tensile Structure", ["tensile structure", "membrane structure"], "Structure relying primarily on tension, cables, membranes, or fabric action."),
        ("LSS", "Long Span Structure", ["long-span structure", "large span"], "Structural strategy for large column-free spaces such as halls, terminals, arenas, and assembly areas."),
        ("EXJ", "Expansion Joint", ["expansion joint", "movement joint"], "Joint allowing thermal, seismic, settlement, or building movement between parts."),
        ("CSJ", "Construction Joint In Structure", ["structural construction joint", "pour joint"], "Joint formed by construction sequencing that must coordinate with structure, waterproofing, and finishes."),
        ("SEJ", "Seismic Joint", ["seismic joint", "separation joint"], "Building separation allowing seismic movement and reducing pounding or restraint."),
        ("CAM", "Camber", ["camber", "pre-camber"], "Intentional upward curvature or offset to manage deflection and serviceability perception."),
        ("SBC", "Soil Bearing Capacity", ["soil bearing capacity", "allowable bearing"], "Soil-support concept affecting foundation type, size, settlement risk, and site feasibility."),
        ("NCC", "Nonstructural Component Coordination", ["nonstructural coordination", "architectural nonstructural components"], "Coordination of ceilings, partitions, cladding, equipment, and services with structural movement and anchorage."),
        ("ASC", "Architectural Structural Coordination", ["architecture-structure coordination", "architectural structural coordination"], "Design coordination between architectural layout/form and structural grids, systems, depths, loads, and details."),
        ("RCF", "Reinforced Concrete Frame", ["RC frame", "reinforced concrete frame"], "Frame system using reinforced concrete beams, columns, and slabs."),
        ("STF", "Steel Frame", ["steel frame", "structural steel frame"], "Frame system using steel columns, beams, girders, bracing, or moment connections."),
        ("TFR", "Timber Frame", ["timber frame", "wood frame"], "Structural system using timber or engineered wood members."),
        ("CPS", "Composite Structural System", ["composite structure", "steel-concrete composite"], "Structural system combining materials to use complementary behavior and construction efficiencies."),
    ]),
]

IMPROVE_HINTS: dict[str, tuple[list[str], list[str], str]] = {
    "ARC.BLD.SRV.PWS": (["water supply distribution", "domestic cold water", "potable water riser"], ["SRC-NATIONAL-PLUMBING-CODE-METADATA", "SRC-DOH-SANITATION-IMPLEMENTING-RULES-METADATA"], "phase2_utility_aliases"),
    "ARC.BLD.SRV.SDR": (["sanitary drainage stack", "soil waste and vent", "drainage cleanout"], ["SRC-NATIONAL-PLUMBING-CODE-METADATA", "SRC-DOH-SANITATION-IMPLEMENTING-RULES-METADATA"], "phase2_utility_aliases"),
    "ARC.BLD.SRV.ELP": (["electrical service entrance", "main distribution", "panelboard coordination"], ["SRC-PEC-METADATA"], "phase2_utility_aliases"),
    "ARC.BLD.SRV.LGT": (["reflected ceiling plan lighting", "lighting circuit", "emergency lighting coordination"], ["SRC-PEC-METADATA", "SRC-DPWH-PHILIPPINE-GREEN-BUILDING-CODE-METADATA"], "phase2_utility_aliases"),
    "ARC.BLD.SRV.HVC": (["duct routing", "air handling unit", "fresh air intake", "indoor air quality"], ["SRC-CHED-BSARCH-BUILDING-TECHNOLOGY-METADATA", "SRC-DPWH-PHILIPPINE-GREEN-BUILDING-CODE-METADATA"], "phase2_utility_aliases"),
    "ARC.BLD.SRV.VTR": (["hoistway", "elevator lobby", "machine-room-less elevator", "escalator planning"], ["SRC-CHED-BSARCH-BUILDING-TECHNOLOGY-METADATA"], "phase2_utility_aliases"),
    "ARC.BLD.SRV.BAS": (["controls integration", "BAS points", "automation commissioning"], ["SRC-DPWH-PHILIPPINE-GREEN-BUILDING-CODE-METADATA"], "phase2_utility_aliases"),
    "ARC.BLD.SRV.SEC": (["ICT room", "communications riser", "CCTV", "access control"], ["SRC-CHED-BSARCH-BUILDING-TECHNOLOGY-METADATA"], "phase2_utility_aliases"),
    "ARC.BLD.STR.LDP": (["gravity load path", "lateral load path", "foundation load transfer"], ["SRC-NSCP-METADATA"], "phase2_structural_aliases"),
    "ARC.BLD.STR.SGL": (["column grid", "structural bay", "planning grid"], ["SRC-NSCP-METADATA", "SRC-CHED-BSARCH-BUILDING-TECHNOLOGY-METADATA"], "phase2_structural_aliases"),
    "ARC.BLD.STR.SPN": (["long span", "structural bay span", "clear span"], ["SRC-NSCP-METADATA"], "phase2_structural_aliases"),
    "ARC.BLD.STR.DEF": (["serviceability", "camber", "finish cracking risk"], ["SRC-NSCP-METADATA"], "phase2_structural_aliases"),
    "LAW.AAP.SIS": (["signing and sealing", "architect seal", "professional seal"], ["SRC-RA-9266-ARCHITECTURE-ACT"], "phase2_practice_aliases"),
    "LAW.AAP.PRC": (["Code of Ethics", "client architect agreement", "professional responsibility"], ["SRC-RA-9266-ARCHITECTURE-ACT", "SRC-CIAP-CONSTRUCTION-ADMIN-METADATA"], "phase2_practice_aliases"),
    "CON.DMC.DBB": (["contract documents", "construction administration", "RFI submittal change order punch list"], ["SRC-CIAP-CONSTRUCTION-ADMIN-METADATA"], "phase2_contract_aliases"),
    "ARC.HIS.SEA.BKS": (["passive cooling", "raised floor vernacular", "tropical ventilation precedent"], ["SRC-NCCA-PHILIPPINE-BUILT-HERITAGE-METADATA"], "phase2_history_aliases"),
    "ARC.HIS.SEA.BNB": (["Spanish Filipino hybrid house", "climate-adapted colonial house", "heritage residential type"], ["SRC-NCCA-PHILIPPINE-BUILT-HERITAGE-METADATA"], "phase2_history_aliases"),
    "ARC.MAT.CON.JNT": (["structural pour joint", "construction sequence joint"], ["SRC-CHED-BSARCH-BUILDING-TECHNOLOGY-METADATA"], "phase2_material_aliases"),
    "ARC.MAT.DUR": (["moisture control", "waterproofing durability", "building envelope durability"], ["SRC-DPWH-PHILIPPINE-GREEN-BUILDING-CODE-METADATA"], "phase2_material_aliases"),
    "LAW.PFC.FSI.FSE": (["FSEC", "BFP fire safety evaluation", "fire clearance for permit"], ["SRC-BFP-FIRE-SAFETY-CLEARANCE-METADATA"], "phase2_fire_aliases"),
    "LAW.PFC.FSI.FIC": (["FSIC", "BFP fire safety inspection", "occupancy fire inspection"], ["SRC-BFP-FIRE-SAFETY-CLEARANCE-METADATA"], "phase2_fire_aliases"),
    "LAW.PAL.ACR.ARS": (["accessible circulation path", "barrier-free route continuity"], ["SRC-NCDA-BP344-IRR-METADATA"], "phase2_accessibility_aliases"),
    "LAW.WCW.DRE.WAE": (["waterway easement", "river easement", "water body setback"], ["SRC-NWRB-WATER-PERMIT-METADATA"], "phase2_water_aliases"),
    "LAW.SCP.MPF.TOI": (["toilet fixture planning", "public sanitary facilities", "accessible toilet coordination"], ["SRC-DOH-SANITATION-IMPLEMENTING-RULES-METADATA"], "phase2_sanitation_aliases"),
    "ARC.SIT.SAN.DRN": (["storm drainage", "site drainage discharge", "flood-resilient drainage"], ["SRC-NWRB-WATER-PERMIT-METADATA"], "phase2_site_aliases"),
    "ARC.TAC.NVS.XVN": (["natural ventilation path", "cross-breeze", "passive cooling airflow"], ["SRC-DPWH-PHILIPPINE-GREEN-BUILDING-CODE-METADATA"], "phase2_tropical_aliases"),
    "ARC.TAC.SOS.SHD": (["solar shading", "external sun control", "tropical envelope shading"], ["SRC-DPWH-PHILIPPINE-GREEN-BUILDING-CODE-METADATA"], "phase2_tropical_aliases"),
    "LAW.PNB.PIE.BPE": (["building permit workflow", "permit drawings", "OBO plan review"], ["SRC-DPWH-BUILDING-PERMIT-NBCDO-METADATA"], "phase2_permit_aliases"),
    "LAW.PNB.PIE.OPM": (["occupancy permit workflow", "certificate of occupancy closeout", "post-construction inspection"], ["SRC-DPWH-BUILDING-PERMIT-NBCDO-METADATA"], "phase2_permit_aliases"),
    "URB.LUZ.CLU.LCC": (["locational clearance", "zoning clearance", "development permit precursor"], ["SRC-DHSUD-ZONING-LOCATIONAL-CLEARANCE-METADATA"], "phase2_zoning_aliases"),
}


def _source_path(source_id: str) -> str:
    return f"COM.STD.PHL.{SOURCE_NODE_SUFFIXES[source_id]}"


def enrich_graph(payload: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    records = [dict(record) for record in payload["records"]]
    relationships = [dict(rel) for rel in payload["relationships"]]
    path_to_record = {record["path_code"]: record for record in records}
    id_to_record = {record["id"]: record for record in records}
    edge_keys = {(rel["from_id"], rel["predicate"], rel["to_id"]) for rel in relationships}
    next_id = _next_domain_id(records)
    added_nodes: list[dict[str, Any]] = []
    added_relationships: list[dict[str, Any]] = []
    improved_nodes: set[str] = set()
    aliases_added = 0

    def add_node(path_code: str, label: str, level: int, parent_path: str | None, definition: str, aliases: list[str], source_ids: list[str], node_kind: str, category: str) -> dict[str, Any]:
        nonlocal next_id, aliases_added
        existing = path_to_record.get(path_code)
        if existing is not None:
            added = _merge_metadata(existing, aliases, source_ids, node_kind, category)
            aliases_added += added
            if added:
                improved_nodes.add(path_code)
            return existing
        record_id = f"VTN-DOM-{next_id:07d}"
        next_id += 1
        full_aliases = _dedupe([path_code, label.lower(), *aliases])
        record = {
            "aliases": full_aliases,
            "canonical_id": record_id,
            "confidence": "high",
            "definition": definition,
            "example_concepts": aliases[:4] or [label],
            "generation_method": GENERATION_METHOD,
            "id": record_id,
            "label": label,
            "lea_ale_category": category,
            "level": level,
            "owner": OWNER,
            "parent_path_code": parent_path,
            "path_code": path_code,
            "pref_label": label,
            "provenance_note": "Metadata-only LEA/ALE resolver deepening; no protected source payload stored.",
            "quality_signal": "curated_public_reference_overlay",
            "record_type": "BackboneNode",
            "release_version": RELEASE_VERSION,
            "review_status": "steward_admitted",
            "scope_note": SCOPE_NOTE,
            "semantic_node_kind": node_kind,
            "source_family_ids": source_ids,
            "steward": OWNER,
        }
        records.append(record)
        path_to_record[path_code] = record
        id_to_record[record_id] = record
        added_nodes.append(record)
        aliases_added += len(full_aliases)
        if parent_path:
            add_edge(parent_path, "broader_than", path_code, "hierarchy", source_ids)
        for source_id in source_ids:
            source_path = _source_path(source_id) if source_id in SOURCE_NODE_SUFFIXES else None
            if source_path and source_path in path_to_record:
                add_edge(path_code, "maps_to_external_standard", source_path, "source_reference", [source_id])
        return record

    def add_edge(from_path: str, predicate: str, to_path: str, category: str, source_ids: list[str]) -> None:
        from_record = path_to_record.get(from_path)
        to_record = path_to_record.get(to_path)
        if from_record is None or to_record is None:
            return
        key = (from_record["id"], predicate, to_record["id"])
        if key in edge_keys:
            return
        edge = {
            "from_id": from_record["id"],
            "generation_method": GENERATION_METHOD,
            "governed": True,
            "predicate": predicate,
            "provenance_note": "Metadata-only LEA/ALE resolver deepening edge; no protected source payload stored.",
            "review_status": "steward_admitted",
            "semantic_overlay_category": category,
            "source_family_ids": _dedupe(source_ids),
            "to_id": to_record["id"],
        }
        relationships.append(edge)
        added_relationships.append(edge)
        edge_keys.add(key)

    def merge_existing(path_code: str, aliases: list[str], source_ids: list[str], category: str) -> None:
        nonlocal aliases_added
        record = path_to_record.get(path_code)
        if record is None:
            return
        added = _merge_metadata(record, aliases, source_ids, record.get("semantic_node_kind", category), category)
        aliases_added += added
        if added:
            improved_nodes.add(path_code)

    # Add phase-2 source reference nodes under existing Philippine source-family parent.
    for reference in SOURCE_REFERENCES:
        if reference["source_id"] not in SOURCE_NODE_SUFFIXES:
            continue
        add_node(
            _source_path(reference["source_id"]),
            reference["source_family"],
            4,
            "COM.STD.PHL",
            f"Metadata-only source-family reference for {reference['source_family']}; used for provenance and crosswalks without storing source payload text.",
            [reference["source_id"], reference["publisher_authority"], reference["source_family"]],
            [reference["source_id"]],
            "standard_reference",
            "source_reference",
        )

    for parent, node_kind, category, source_ids, items in NODE_GROUPS:
        for suffix, label, aliases, definition in items:
            add_node(f"{parent}.{suffix}", label, 4, parent, definition, aliases, source_ids, node_kind, category)

    for path_code, (aliases, source_ids, category) in IMPROVE_HINTS.items():
        merge_existing(path_code, aliases, source_ids, category)

    # Utility coordination edges.
    for utility_path in [p for p in path_to_record if p.startswith("ARC.BLD.SRV.") and p.count(".") == 3]:
        if utility_path not in {"ARC.BLD.SRV.UCO", "ARC.BLD.SRV.RCP", "ARC.BLD.SRV.SEC"}:
            add_edge("ARC.BLD.SRV.UCO", "requires", utility_path, "utility_coordination", _source_ids_for_paths(path_to_record, ["ARC.BLD.SRV.UCO", utility_path]))
        add_edge(utility_path, "requires", "LAW.AAP.SAP.ADO", "utilities_documents", _source_ids_for_paths(path_to_record, [utility_path, "LAW.AAP.SAP.ADO"]))
        add_edge(utility_path, "requires", "ARC.BLD.SRV.MAC", "utilities_maintenance", _source_ids_for_paths(path_to_record, [utility_path, "ARC.BLD.SRV.MAC"]))

    utility_specific_edges = [
        ("ARC.BLD.SRV.RCP", "requires", "ARC.BLD.SRV.LGT", "rcp_coordination"), ("ARC.BLD.SRV.RCP", "requires", "ARC.BLD.SRV.DRT", "rcp_coordination"), ("ARC.BLD.SRV.RCP", "requires", "ARC.BLD.SRV.SPR", "rcp_coordination"), ("ARC.BLD.SRV.RCP", "requires", "ARC.BLD.SRV.FAP", "rcp_coordination"), ("ARC.BLD.SRV.RCP", "requires", "ARC.BLD.SRV.ACP", "rcp_coordination"),
        ("ARC.BLD.SRV.SHA", "requires", "ARC.BLD.SRV.RIS", "shaft_riser_coordination"), ("ARC.BLD.SRV.SHA", "requires", "ARC.BLD.SRV.CMR", "shaft_riser_coordination"), ("ARC.BLD.SRV.SHA", "requires", "ARC.BLD.SRV.SPR", "shaft_riser_coordination"), ("ARC.BLD.SRV.SHA", "requires", "ARC.BLD.SRV.STR", "shaft_riser_coordination"),
        ("ARC.BLD.SRV.ERP", "requires", "ARC.BLD.SRV.MER", "equipment_room_coordination"), ("ARC.BLD.SRV.ERP", "requires", "ARC.BLD.SRV.TRR", "equipment_room_coordination"), ("ARC.BLD.SRV.ERP", "requires", "ARC.BLD.SRV.GNR", "equipment_room_coordination"), ("ARC.BLD.SRV.ERP", "requires", "ARC.BLD.SRV.FPR", "equipment_room_coordination"), ("ARC.BLD.SRV.ERP", "requires", "ARC.BLD.SRV.ICT", "equipment_room_coordination"),
        ("ARC.BLD.SRV.PFP", "requires", "ARC.BLD.SRV.WSD", "plumbing_fixture_coordination"), ("ARC.BLD.SRV.PFP", "requires", "ARC.BLD.SRV.SDR", "plumbing_fixture_coordination"), ("ARC.BLD.SRV.PFP", "requires", "LAW.PAL.ACR.ATO", "accessibility_plumbing"), ("ARC.BLD.SRV.PFP", "requires", "LAW.SCP.MPF.TOI", "sanitation_plumbing"),
        ("ARC.BLD.SRV.SDR", "requires", "ARC.BLD.SRV.VST", "sanitary_drainage"), ("ARC.BLD.SRV.SDR", "requires", "ARC.BLD.SRV.CLO", "sanitary_drainage"), ("ARC.BLD.SRV.SDR", "requires", "ARC.BLD.SRV.SWC", "sanitary_drainage"), ("ARC.BLD.SRV.SDR", "requires", "ARC.BLD.SRV.SPS", "sanitary_drainage"), ("ARC.BLD.SRV.SDR", "requires", "ARC.BLD.SRV.GRI", "sanitary_drainage"),
        ("ARC.BLD.SRV.PWS", "requires", "ARC.BLD.SRV.BFP", "potable_water_safety"), ("ARC.BLD.SRV.PWS", "requires", "ARC.BLD.SRV.WSD", "potable_water_distribution"), ("ARC.BLD.SRV.STD", "requires", "ARC.SIT.SAN.DRN", "stormwater_site_coordination"), ("ARC.BLD.SRV.STD", "requires", "LAW.WCW.DRE.DRG", "stormwater_site_coordination"),
        ("ARC.BLD.SRV.ELP", "requires", "ARC.BLD.SRV.ESE", "electrical_distribution"), ("ARC.BLD.SRV.ELP", "requires", "ARC.BLD.SRV.MDP", "electrical_distribution"), ("ARC.BLD.SRV.MDP", "requires", "ARC.BLD.SRV.PNB", "electrical_distribution"), ("ARC.BLD.SRV.PNB", "requires", "ARC.BLD.SRV.BRC", "electrical_distribution"), ("ARC.BLD.SRV.LGT", "requires", "ARC.BLD.SRV.LTC", "lighting_coordination"), ("LAW.PFC.OFS.EXS", "requires", "ARC.BLD.SRV.ESP", "egress_power"), ("ARC.BLD.SRV.ELP", "requires", "ARC.BLD.SRV.GBN", "electrical_safety"),
        ("ARC.BLD.SRV.HVC", "requires", "ARC.BLD.SRV.MER", "mechanical_coordination"), ("ARC.BLD.SRV.HVC", "requires", "ARC.BLD.SRV.AHU", "mechanical_coordination"), ("ARC.BLD.SRV.HVC", "requires", "ARC.BLD.SRV.CDU", "mechanical_coordination"), ("ARC.BLD.SRV.HVC", "requires", "ARC.BLD.SRV.DRT", "mechanical_coordination"), ("ARC.BLD.SRV.DRT", "requires", "ARC.BLD.SRV.SAF", "air_distribution"), ("ARC.BLD.SRV.DRT", "requires", "ARC.BLD.SRV.RAF", "air_distribution"), ("ARC.BLD.SRV.DRT", "requires", "ARC.BLD.SRV.EAF", "air_distribution"), ("ARC.BLD.SRV.DRT", "requires", "ARC.BLD.SRV.FAI", "air_distribution"), ("ARC.BLD.SRV.HVC", "requires", "ARC.BLD.SRV.IAQ", "indoor_environment"), ("ARC.TAC.NVS.XVN", "requires", "ARC.BLD.SRV.NVP", "tropical_ventilation"),
        ("LAW.PFC.EPE.ASP", "requires", "ARC.BLD.SRV.SPR", "fire_protection_utilities"), ("LAW.PFC.EPE.STP", "requires", "ARC.BLD.SRV.STR", "fire_protection_utilities"), ("LAW.PFC.EPE.FAL", "requires", "ARC.BLD.SRV.FAP", "fire_alarm_utilities"), ("ARC.BLD.SRV.FPR", "requires", "ARC.BLD.SRV.PWS", "fire_pump_water"), ("ARC.BLD.SRV.FPR", "requires", "ARC.BLD.SRV.GNR", "fire_pump_power"),
        ("ARC.BLD.SRV.VTR", "requires", "ARC.BLD.SRV.HSW", "vertical_transport"), ("ARC.BLD.SRV.VTR", "requires", "ARC.BLD.SRV.ELB", "vertical_transport"), ("ARC.BLD.SRV.VTR", "requires", "ARC.BLD.SRV.EMR", "vertical_transport"), ("ARC.BLD.SRV.VTR", "has_facet", "ARC.BLD.SRV.MRL", "vertical_transport"), ("ARC.BLD.SRV.ECP", "constrains", "ARC.INT.PAC.ISP", "vertical_circulation"),
        ("ARC.BLD.SRV.SEC", "requires", "ARC.BLD.SRV.ICT", "ict_security_coordination"), ("ARC.BLD.SRV.SEC", "requires", "ARC.BLD.SRV.CMR", "ict_security_coordination"), ("ARC.BLD.SRV.SEC", "requires", "ARC.BLD.SRV.SCR", "ict_security_coordination"), ("ARC.BLD.SRV.SEC", "requires", "ARC.BLD.SRV.CTV", "ict_security_coordination"), ("ARC.BLD.SRV.SEC", "requires", "ARC.BLD.SRV.ACS", "ict_security_coordination"), ("ARC.BLD.SRV.ACS", "constrains", "ARC.MAT.FIN.HDW", "security_hardware"),
    ]

    structural_specific_edges = [
        ("ARC.BLD.STR.SCA", "requires", "ARC.BLD.STR.LDP", "structural_concept"), ("ARC.BLD.STR.SCA", "requires", "ARC.BLD.STR.SGL", "structural_concept"), ("ARC.BLD.STR.SCA", "requires", "ARC.BLD.STR.LST", "structural_concept"), ("ARC.BLD.STR.SCA", "requires", "ARC.BLD.STR.FDS", "structural_concept"),
        ("ARC.BLD.STR.LDP", "requires", "ARC.BLD.STR.TRA", "load_path_reasoning"), ("ARC.BLD.STR.LDP", "requires", "ARC.BLD.STR.COL", "load_path_reasoning"), ("ARC.BLD.STR.LDP", "requires", "ARC.BLD.STR.BEM", "load_path_reasoning"), ("ARC.BLD.STR.LDP", "requires", "ARC.BLD.STR.SLB", "load_path_reasoning"), ("ARC.BLD.STR.LDP", "requires", "ARC.BLD.STR.FDS", "load_path_reasoning"),
        ("ARC.BLD.STR.SGL", "requires", "ARC.BLD.STR.CGD", "grid_bay_span"), ("ARC.BLD.STR.SGL", "requires", "ARC.BLD.STR.BAY", "grid_bay_span"), ("ARC.BLD.STR.BAY", "requires", "ARC.BLD.STR.SPN", "grid_bay_span"), ("ARC.BLD.STR.SPN", "constrains", "ARC.BLD.STR.BEM", "span_member_depth"), ("ARC.BLD.STR.SPN", "constrains", "ARC.BLD.STR.GIR", "span_member_depth"),
        ("ARC.BLD.STR.BEM", "requires", "ARC.BLD.STR.COL", "frame_system"), ("ARC.BLD.STR.GIR", "requires", "ARC.BLD.STR.COL", "frame_system"), ("ARC.BLD.STR.JOI", "requires", "ARC.BLD.STR.GIR", "floor_framing"), ("ARC.BLD.STR.SLB", "has_facet", "ARC.BLD.STR.OWS", "slab_system"), ("ARC.BLD.STR.SLB", "has_facet", "ARC.BLD.STR.TWS", "slab_system"),
        ("ARC.BLD.STR.LST", "requires", "ARC.BLD.STR.SHW", "lateral_system"), ("ARC.BLD.STR.LST", "requires", "ARC.BLD.STR.BRF", "lateral_system"), ("ARC.BLD.STR.LST", "requires", "ARC.BLD.STR.MFR", "lateral_system"), ("ARC.BLD.STR.WDL", "constrains", "ARC.BLD.STR.LST", "wind_resilience"), ("ARC.BLD.STR.SDL", "constrains", "ARC.BLD.STR.LST", "earthquake_resilience"),
        ("ARC.BLD.STR.FDS", "has_facet", "ARC.BLD.STR.FOO", "foundation_system"), ("ARC.BLD.STR.FDS", "has_facet", "ARC.BLD.STR.IFT", "foundation_system"), ("ARC.BLD.STR.FDS", "has_facet", "ARC.BLD.STR.CBF", "foundation_system"), ("ARC.BLD.STR.FDS", "has_facet", "ARC.BLD.STR.SPF", "foundation_system"), ("ARC.BLD.STR.FDS", "has_facet", "ARC.BLD.STR.MTF", "foundation_system"), ("ARC.BLD.STR.FDS", "has_facet", "ARC.BLD.STR.PIF", "foundation_system"), ("ARC.BLD.STR.SBC", "constrains", "ARC.BLD.STR.FDS", "site_foundation"), ("ARC.BLD.STR.FSS", "constrains", "ARC.MAT.FIN.FLR", "settlement_finish_coordination"),
        ("ARC.BLD.STR.TRU", "has_facet", "ARC.BLD.STR.LSS", "long_span_systems"), ("ARC.BLD.STR.ARS", "has_facet", "ARC.BLD.STR.LSS", "long_span_systems"), ("ARC.BLD.STR.SHL", "has_facet", "ARC.BLD.STR.LSS", "long_span_systems"), ("ARC.BLD.STR.TNS", "has_facet", "ARC.BLD.STR.LSS", "long_span_systems"),
        ("ARC.BLD.STR.EXJ", "constrains", "ARC.MAT.CON.JNT", "movement_joint_detailing"), ("ARC.BLD.STR.CSJ", "constrains", "ARC.MAT.CON.JNT", "movement_joint_detailing"), ("ARC.BLD.STR.SEJ", "constrains", "LAW.PFC.EPE.FST", "seismic_firestop_coordination"), ("ARC.BLD.STR.DEF", "constrains", "ARC.MAT.FIN.CEF", "deflection_finish_coordination"), ("ARC.BLD.STR.CAM", "constrains", "ARC.BLD.STR.DEF", "serviceability"),
        ("ARC.BLD.STR.NCC", "constrains", "ARC.MAT.FIN.CEF", "nonstructural_coordination"), ("ARC.BLD.STR.NCC", "constrains", "LAW.PFC.EPE.FST", "nonstructural_coordination"), ("ARC.BLD.STR.NCC", "constrains", "ARC.BLD.SRV.ERP", "nonstructural_coordination"), ("ARC.BLD.STR.ASC", "requires", "LAW.AAP.SAP.ADO", "structural_documents"), ("ARC.BLD.STR.ASC", "requires", "CON.DMC.DBB.SHD", "shop_drawing_coordination"),
        ("ARC.BLD.STR.RCF", "requires", "ARC.MAT.CON.RCC", "material_structural_system"), ("ARC.BLD.STR.STF", "requires", "ARC.MAT.STM.STL", "material_structural_system"), ("ARC.BLD.STR.TFR", "requires", "ARC.MAT.STM.TIM", "material_structural_system"), ("ARC.BLD.STR.CPS", "requires", "ARC.MAT.STM.STL", "material_structural_system"), ("ARC.BLD.STR.CPS", "requires", "ARC.MAT.CON.RCC", "material_structural_system"),
    ]

    reasoning_edges = [
        ("LAW.AAP", "governs", "LAW.AAP.SIS", "practice_reasoning"), ("LAW.AAP.SIS", "requires", "LAW.AAP.SAP.ADO", "practice_reasoning"), ("LAW.AAP.SIS", "requires", "LAW.AAP.SAP.AOR", "practice_reasoning"), ("LAW.AAP.PRC", "constrains", "LAW.AAP.SAP.SER", "ethics_services"), ("LAW.AAP.PRC", "constrains", "CON.DMC.DBB.BID", "ethics_contracts"),
        ("LAW.AAP.SAP.SPP", "constrains", "LAW.AAP.SAP.SER", "spp_services"), ("LAW.AAP.SAP.SER", "requires", "CON.DMC.DBB.BID", "services_contract_documents"), ("CON.DMC.DBB.BID", "requires", "CON.DMC.DBB.RFI", "construction_admin_path"), ("CON.DMC.DBB.RFI", "requires", "CON.DMC.DBB.SUB", "construction_admin_path"), ("CON.DMC.DBB.SUB", "requires", "CON.DMC.DBB.PUN", "construction_admin_path"),
        ("LAW.PNB", "governs", "LAW.PNB.PIE.BPE", "building_code_path"), ("LAW.PNB.PIE.BPE", "requires", "LAW.PNB.PIE.PRV", "building_permit_path"), ("LAW.PNB.PIE.PRV", "requires", "LAW.AAP.SAP.ADO", "building_permit_path"), ("LAW.PNB.OUC.OCL", "constrains", "LAW.PFC.OFS.OCL", "occupancy_fire_path"), ("LAW.PFC.OFS.OCL", "constrains", "LAW.PFC.OFS.EGR", "occupancy_fire_path"),
        ("LAW.PFC", "governs", "LAW.PFC.FSI.FSE", "fire_code_path"), ("LAW.PFC.FSI.FSE", "requires", "LAW.PNB.PIE.BPE", "fire_permit_path"), ("LAW.PFC.FSI.FIC", "requires", "LAW.PNB.PIE.OPM", "fire_closeout_path"), ("LAW.PFC.FSI.FIS", "requires", "CON.DMC.DBB.PUN", "fire_closeout_path"),
        ("LAW.PAL", "governs", "LAW.PAL.ACR.ARS", "accessibility_path"), ("LAW.PAL.ACR.ARS", "requires", "ARC.SIT.SAN.USR", "accessibility_site_path"), ("LAW.PAL.ACR.ARS", "requires", "ARC.INT.PAC.ISP", "accessibility_interiors_path"), ("LAW.PAL.ACR.RMP", "constrains", "ARC.SIT.SAN.SLP", "accessibility_site_path"),
        ("LAW.WCW", "governs", "LAW.WCW.DRE.WAE", "water_code_path"), ("LAW.WCW.DRE.WAE", "constrains", "ARC.SIT.SAN.SLP", "water_site_path"), ("LAW.WCW.DRE.FLD", "constrains", "ARC.BLD.SRV.STD", "flood_drainage_path"), ("LAW.SCP", "governs", "LAW.SCP.MPF.TOI", "sanitation_path"), ("LAW.SCP.MPF.TOI", "requires", "ARC.BLD.SRV.PFP", "sanitation_plumbing_path"),
        ("ARC.HIS.SEA.BKS", "has_facet", "ARC.TAC.NVS.NVP", "vernacular_tropical_path"), ("ARC.HIS.SEA.BKS", "has_facet", "ARC.TAC.NVS.VTC", "vernacular_tropical_path"), ("ARC.HIS.SEA.BNB", "has_facet", "ARC.MAT.STM.TIM", "colonial_material_path"), ("ARC.HIS.SEA.BNB", "has_facet", "ARC.TAC.SOS.SHD", "colonial_climate_path"), ("ARC.HIS.SEA.PVA", "has_facet", "ARC.TAC.NVS.XVN", "vernacular_passive_path"),
        ("URB.LUZ.CLU.LCC", "requires", "LAW.ZON", "zoning_site_path"), ("LAW.ZON", "constrains", "ARC.SIT.SAN.PRG", "zoning_site_path"), ("LAW.ZON", "constrains", "LAW.PNB.OUC.OCL", "zoning_occupancy_path"),
        ("ARC.MAT.CON.JNT", "constrains", "ARC.BLD.STR.CSJ", "materials_structural_path"), ("ARC.MAT.CON.DPC", "requires", "ARC.MAT.DUR", "moisture_control_path"), ("ARC.MAT.DUR", "requires", "ARC.BLD.SRV.STD", "moisture_drainage_path"), ("ARC.MAT.FIN.CEF", "requires", "ARC.BLD.SRV.RCP", "ceiling_coordination_path"),
        ("ARC.BLD.STR.SGL", "constrains", "ARC.SIT.SAN.ADJ", "structure_space_path"), ("ARC.BLD.STR.CGD", "constrains", "ARC.INT.PAC.ISP", "structure_interiors_path"), ("ARC.BLD.STR.SPN", "constrains", "ARC.THE.DPR.SCL", "structure_theory_path"), ("ARC.BLD.STR.NCC", "constrains", "ARC.BLD.SRV.PLC", "structure_utilities_path"),
        ("ARC.TAC.SOS.SNP", "requires", "ARC.TAC.SOS.ORI", "tropical_energy_path"), ("ARC.TAC.SOS.SHD", "constrains", "ARC.INT.PAC.IEQ", "tropical_comfort_path"), ("ARC.TAC.NVS.XVN", "requires", "ARC.BLD.SRV.NVP", "tropical_ventilation_path"), ("ARC.BLD.SRV.IAQ", "requires", "ARC.TAC.NVS.XVN", "iaq_tropical_path"),
        ("COM.STD.PHL.RAA", "applicable_in_jurisdiction", "ARC.COD.JUR", "jurisdiction_overlay"), ("COM.STD.PHL.NBC", "applicable_in_jurisdiction", "ARC.COD.JUR", "jurisdiction_overlay"), ("COM.STD.PHL.FCP", "applicable_in_jurisdiction", "ARC.COD.JUR", "jurisdiction_overlay"), ("COM.STD.PHL.BPA", "applicable_in_jurisdiction", "ARC.COD.JUR", "jurisdiction_overlay"), ("COM.STD.PHL.WCP", "applicable_in_jurisdiction", "ARC.COD.JUR", "jurisdiction_overlay"), ("COM.STD.PHL.SCP", "applicable_in_jurisdiction", "ARC.COD.JUR", "jurisdiction_overlay"),
        ("LAW.HER", "conflicts_with", "LAW.PAL.ACR.ARS", "heritage_accessibility_conflict"), ("ARC.HIS.SEA.SCC", "conflicts_with", "LAW.PAL.ACR.RMP", "heritage_accessibility_conflict"), ("COM.STD.PHL.AIR", "supersedes", "COM.STD.PHL.RAA", "source_temporal_overlay"), ("COM.STD.PHL.NIR", "supersedes", "COM.STD.PHL.NBC", "source_temporal_overlay"),
    ]

    for from_path, predicate, to_path, category in [*utility_specific_edges, *structural_specific_edges, *reasoning_edges]:
        add_edge(from_path, predicate, to_path, category, _source_ids_for_paths(path_to_record, [from_path, to_path]))

    # Source governance edges for phase-2 reference nodes.
    for source_id in SOURCE_NODE_SUFFIXES:
        source_path = _source_path(source_id)
        if source_path in path_to_record:
            for target in _source_targets_for(source_id):
                if target in path_to_record:
                    add_edge(source_path, "constrains" if not target.startswith("COM.STD") else "maps_to_external_standard", target, "source_reference", [source_id])

    new_payload = {**payload, "records": records, "relationships": relationships}
    records_by_id = {record["id"]: record for record in records}
    cross_domain = [
        rel for rel in added_relationships
        if records_by_id[rel["from_id"]]["path_code"].split(".")[0]
        != records_by_id[rel["to_id"]]["path_code"].split(".")[0]
    ]
    utility_relationships = [rel for rel in added_relationships if _edge_touches_prefix(records_by_id, rel, "ARC.BLD.SRV")]
    structural_relationships = [rel for rel in added_relationships if _edge_touches_prefix(records_by_id, rel, "ARC.BLD.STR")]
    law_relationships = [rel for rel in added_relationships if _edge_touches_prefix(records_by_id, rel, "LAW") or _edge_touches_prefix(records_by_id, rel, "COM.STD.PHL")]
    report = {
        "ok": True,
        "generation_method": GENERATION_METHOD,
        "input_record_count": len(payload["records"]),
        "output_record_count": len(records),
        "input_relationship_count": len(payload["relationships"]),
        "output_relationship_count": len(relationships),
        "added_node_count": len(added_nodes),
        "added_nodes_by_kind": dict(sorted(Counter(record.get("semantic_node_kind") for record in added_nodes).items())),
        "added_nodes_by_category": dict(sorted(Counter(record.get("lea_ale_category") for record in added_nodes).items())),
        "improved_existing_node_count": len(improved_nodes),
        "improved_existing_path_codes": sorted(improved_nodes),
        "added_relationship_count": len(added_relationships),
        "added_relationships_by_predicate": dict(sorted(Counter(rel.get("predicate") for rel in added_relationships).items())),
        "added_relationships_by_category": dict(sorted(Counter(rel.get("semantic_overlay_category") for rel in added_relationships).items())),
        "cross_domain_relationship_count": len(cross_domain),
        "utilities_relationship_count": len(utility_relationships),
        "structural_relationship_count": len(structural_relationships),
        "philippine_law_code_relationship_count": len(law_relationships),
        "aliases_added_or_preserved_on_new_and_improved_nodes": aliases_added,
        "raw_source_rights_classification": RAW_SOURCE_RIGHTS_CLASSIFICATION,
        "rights_safety": _rights_safety(),
    }
    return new_payload, report


def enrich_source_rights_registry(payload: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    rows = [dict(row) for row in payload.get("source_rights_registry", [])]
    existing_by_id = {row.get("source_id"): row for row in rows}
    added: list[dict[str, Any]] = []
    improved: list[str] = []
    for reference in SOURCE_REFERENCES:
        row = existing_by_id.get(reference["source_id"])
        is_raw = reference["source_id"].startswith("SRC-RAW-LEA")
        if row is None:
            row = {
                "source_id": reference["source_id"],
                "source_family": reference["source_family"],
                "publisher_authority": reference["publisher_authority"],
                "edition_version_effective_date": "admission-time verification required",
                "official_url": reference["official_url"],
                "source_rights_class": "reference_only",
                "clearance_state": "clearance_required" if is_raw else "planning_reference_only",
                "intended_vitruvius_use": reference["intended_vitruvius_use"],
                "steward_owner": OWNER,
                "declared_use_boundary": _raw_boundary() if is_raw else _metadata_boundary(),
                "currentness_check_date": "2026-04-29",
                "update_cadence": "before source admission and per LEA/ALE resolver release",
                "blocking_notes": _raw_blocking_notes() if is_raw else "content ingest blocked until explicit rights/license/legal review; this row is metadata-only provenance",
            }
            rows.append(row)
            existing_by_id[reference["source_id"]] = row
            added.append(row)
        else:
            before = json.dumps(row, sort_keys=True)
            row["source_rights_class"] = "reference_only"
            row["clearance_state"] = "clearance_required" if is_raw else row.get("clearance_state", "planning_reference_only")
            row["declared_use_boundary"] = _raw_boundary() if is_raw else row.get("declared_use_boundary", _metadata_boundary())
            row["blocking_notes"] = _raw_blocking_notes() if is_raw else row.get("blocking_notes", "content ingest blocked until explicit rights/license/legal review")
            row["currentness_check_date"] = "2026-04-29"
            if json.dumps(row, sort_keys=True) != before:
                improved.append(reference["source_id"])
    return {**payload, "source_rights_registry": rows}, {
        "ok": True,
        "generation_method": GENERATION_METHOD,
        "input_source_reference_count": len(payload.get("source_rights_registry", [])),
        "output_source_reference_count": len(rows),
        "added_source_reference_count": len(added),
        "improved_source_reference_count": len(improved),
        "added_source_reference_ids": [row["source_id"] for row in added],
        "improved_source_reference_ids": improved,
        "raw_source_rights_classification": RAW_SOURCE_RIGHTS_CLASSIFICATION,
        "rights_safety": {"protected_source_payloads_ingested": False, "source_payload_mode": "source_family_metadata_only", "content_ingest_rows_added": False},
    }


def enrich_resolver_fixture(payload: dict[str, Any], graph_payload: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    records_by_path = {record["path_code"]: record for record in graph_payload["records"]}
    existing_cases = list(payload.get("resolver_golden_cases", []))
    existing_ids = {case.get("case_id") for case in existing_cases}
    added: list[dict[str, Any]] = []
    for spec in _resolver_case_specs():
        if spec["case_id"] in existing_ids:
            continue
        case = _materialize_case(spec, records_by_path)
        existing_cases.append(case)
        added.append(case)
        existing_ids.add(spec["case_id"])
    return {**payload, "resolver_golden_cases": existing_cases}, {
        "ok": True,
        "generation_method": GENERATION_METHOD,
        "input_resolver_golden_case_count": len(payload.get("resolver_golden_cases", [])),
        "output_resolver_golden_case_count": len(existing_cases),
        "added_resolver_golden_case_count": len(added),
        "added_case_ids": [case["case_id"] for case in added],
        "rights_safety": _rights_safety(),
    }


def _materialize_case(spec: dict[str, Any], records_by_path: dict[str, dict[str, Any]]) -> dict[str, Any]:
    refs = []
    for path_code, role in spec.get("path_refs", []):
        if path_code not in records_by_path:
            raise KeyError(f"resolver case {spec['case_id']} references missing path {path_code}")
        refs.append({"node_id": records_by_path[path_code]["id"], "role": role})
    concept_path = spec.get("concept_path")
    concept_id = records_by_path[concept_path]["id"] if concept_path in records_by_path else spec.get("concept_id", "VTN-DOM-0000001")
    context_paths = spec.get("context_paths", [])
    context_ids = [records_by_path[path]["id"] for path in context_paths if path in records_by_path]
    return {
        "case_id": spec["case_id"],
        "query": {
            "concept_id": concept_id,
            "asset_context": spec["asset_context"],
            "text": spec["text"],
            "context_ids": context_ids,
            "jurisdiction_filters": spec.get("jurisdiction_filters", ["PH"]),
            "discipline_filters": spec.get("discipline_filters", ["architecture"]),
            "trace_requested": True,
        },
        "jurisdiction": spec.get("jurisdiction", "PH"),
        "effective_date": "2026-04-29",
        "expected_result_type": spec["result_type"],
        "expected_confidence": spec["confidence"],
        "rationale": spec["rationale"],
        "source_evidence": spec["source_evidence"],
        "expected_node_refs": refs,
        "fallback_reason": spec["fallback_reason"],
        "trace_safe_rationale": "Metadata-only LEA/ALE resolver golden case; returns canonical node IDs and source IDs only, with no protected source text.",
        "owner": OWNER,
        "review_status": "candidate",
    }


def _resolver_case_specs() -> list[dict[str, Any]]:
    single_specs = [
        ("LEA-RES-001", "What does R.A. 9266 govern?", "architecture_law_practice", "LAW.AAP", [("LAW.AAP", "governing_law"), ("LAW.AAP.SAP.ADO", "practice_document")], ["SRC-RA-9266-ARCHITECTURE-ACT"]),
        ("LEA-RES-002", "How does R.A. 9266 relate to signing and sealing?", "signing_sealing", "LAW.AAP.SIS", [("LAW.AAP.SIS", "signing_sealing_topic"), ("LAW.AAP.SAP.ADO", "sealed_document")], ["SRC-RA-9266-ARCHITECTURE-ACT"]),
        ("LEA-RES-003", "How does the Architecture Act relate to architectural documents?", "architectural_documents", "LAW.AAP.SAP.ADO", [("LAW.AAP.SAP.ADO", "architectural_document"), ("LAW.AAP.SAP.AOR", "responsible_architect")], ["SRC-RA-9266-ARCHITECTURE-ACT"]),
        ("LEA-RES-004", "How do Standards of Professional Practice relate to architectural services?", "spp_services", "LAW.AAP.SAP.SPP", [("LAW.AAP.SAP.SPP", "practice_standard"), ("LAW.AAP.SAP.SER", "architectural_service")], ["SRC-UAP-SPP-CODE-ETHICS-METADATA"]),
        ("LEA-RES-005", "How does diversified architectural experience relate to licensure?", "licensure_experience", "ARC.REG.PHL.DAE", [("ARC.REG.PHL.DAE", "experience_prerequisite"), ("ARC.REG.PHL.ALE", "licensure_exam")], ["SRC-PRC-ALE-TOS", "SRC-RA-9266-ARCHITECTURE-ACT"]),
        ("LEA-RES-006", "How does the National Building Code relate to occupancy classification?", "nbcp_occupancy", "LAW.PNB.OUC.OCL", [("LAW.PNB", "building_code"), ("LAW.PNB.OUC.OCL", "occupancy_classification")], ["SRC-PD-1096-NBCP"]),
        ("LEA-RES-007", "How does P.D. 1096 relate to building permits and occupancy permits?", "permit_workflow", "LAW.PNB.PIE.BPE", [("LAW.PNB.PIE.BPE", "building_permit"), ("LAW.PNB.PIE.OPM", "occupancy_permit")], ["SRC-PD-1096-NBCP", "SRC-DPWH-BUILDING-PERMIT-NBCDO-METADATA"]),
        ("LEA-RES-008", "What LEA topics are connected to the Building Official?", "building_official", "LAW.PNB.PIE.BOF", [("LAW.PNB.PIE.BOF", "building_official"), ("LAW.PNB.PIE.PRV", "plan_review")], ["SRC-PD-1096-NBCP"]),
        ("LEA-RES-009", "How does the Fire Code relate to means of egress?", "fire_egress", "LAW.PFC.OFS.EGR", [("LAW.PFC", "fire_code"), ("LAW.PFC.OFS.EGR", "means_of_egress")], ["SRC-RA-9514-FIRE-CODE"]),
        ("LEA-RES-010", "How do FSEC and FSIC connect to architectural permitting?", "fire_permit_closeout", "LAW.PFC.FSI.FSE", [("LAW.PFC.FSI.FSE", "fire_safety_evaluation"), ("LAW.PFC.FSI.FIC", "fire_safety_inspection"), ("LAW.PNB.PIE.BPE", "building_permit")], ["SRC-RA-9514-FIRE-CODE", "SRC-BFP-FIRE-SAFETY-CLEARANCE-METADATA"]),
        ("LEA-RES-011", "How does B.P. 344 relate to ramps accessible parking toilets and public buildings?", "accessibility_components", "LAW.PAL.ACR.ARS", [("LAW.PAL", "accessibility_law"), ("LAW.PAL.ACR.RMP", "ramp"), ("LAW.PAL.ACR.APK", "accessible_parking"), ("LAW.PAL.ACR.ATO", "accessible_toilet")], ["SRC-BP-344-ACCESSIBILITY-LAW", "SRC-NCDA-BP344-IRR-METADATA"]),
        ("LEA-RES-012", "How does accessibility connect to site planning interiors circulation and universal design?", "accessibility_design", "LAW.PAL.ACR.ARS", [("LAW.PAL.ACR.ARS", "accessible_route"), ("ARC.SIT.SAN.USR", "user_analysis"), ("ARC.INT.PAC.ISP", "interior_planning")], ["SRC-BP-344-ACCESSIBILITY-LAW"]),
        ("LEA-RES-013", "How does the Water Code relate to site planning near waterways?", "waterway_site", "LAW.WCW.DRE.WAE", [("LAW.WCW.DRE.WAE", "waterway_easement"), ("ARC.SIT.SAN.DRN", "site_drainage")], ["SRC-PD-1067-WATER-CODE", "SRC-NWRB-WATER-PERMIT-METADATA"]),
        ("LEA-RES-014", "How does the Sanitation Code relate to building design and plumbing?", "sanitation_plumbing", "LAW.SCP.MPF.TOI", [("LAW.SCP.MPF.TOI", "sanitary_facility"), ("ARC.BLD.SRV.PFP", "fixture_planning"), ("ARC.BLD.SRV.SDR", "sanitary_drainage")], ["SRC-PD-856-SANITATION-CODE", "SRC-DOH-SANITATION-IMPLEMENTING-RULES-METADATA"]),
        ("LEA-RES-015", "How do drainage stormwater flood risk and site planning connect?", "drainage_flood_site", "ARC.BLD.SRV.STD", [("ARC.BLD.SRV.STD", "storm_drainage"), ("LAW.WCW.DRE.FLD", "flood_constraint"), ("ARC.SIT.SAN.DRN", "site_drainage")], ["SRC-PD-1067-WATER-CODE"]),
        ("LEA-RES-016", "How does Bahay Kubo connect to tropical design?", "vernacular_tropical", "ARC.HIS.SEA.BKS", [("ARC.HIS.SEA.BKS", "vernacular_type"), ("ARC.TAC.NVS.XVN", "cross_ventilation"), ("ARC.BLD.SRV.NVP", "natural_ventilation_path")], ["SRC-NCCA-PHILIPPINE-BUILT-HERITAGE-METADATA"]),
        ("LEA-RES-017", "How does Bahay na Bato connect to Spanish colonial architecture and climate adaptation?", "colonial_climate", "ARC.HIS.SEA.BNB", [("ARC.HIS.SEA.BNB", "philippine_house_type"), ("ARC.HIS.SEA.SCC", "colonial_context"), ("ARC.TAC.SOS.SHD", "climate_response")], ["SRC-NCCA-PHILIPPINE-BUILT-HERITAGE-METADATA", "SRC-RA-10066-HERITAGE-ACT"]),
        ("LEA-RES-018", "How do design principles support architectural design?", "design_principles", "ARC.THE.DPR.ORD", [("ARC.THE.DPR.ORD", "ordering_principle"), ("ARC.THE.DPR.SCL", "scale_principle"), ("ARC.THE.DPR.CIR", "circulation_principle")], ["SRC-CHED-CMO-61-2017-BS-ARCH"]),
        ("LEA-RES-019", "How do specifications relate to materials workmanship quality control and contract documents?", "specifications_contracts", "CON.DMC.DBB.BID", [("CON.DMC.DBB.BID", "contract_document"), ("ARC.MAT.CON.RCC", "material"), ("CON.QAQ", "quality_control")], ["SRC-CIAP-CONSTRUCTION-ADMIN-METADATA", "SRC-CHED-BSARCH-BUILDING-TECHNOLOGY-METADATA"]),
        ("LEA-RES-020", "How do waterproofing damp proofing building envelope and moisture control connect?", "moisture_control", "ARC.MAT.CON.DPC", [("ARC.MAT.CON.DPC", "damp_proofing"), ("ARC.MAT.DUR", "durability"), ("ARC.BLD.SRV.STD", "drainage_coordination")], ["SRC-DPWH-PHILIPPINE-GREEN-BUILDING-CODE-METADATA"]),
        ("LEA-RES-021", "How do load path structural grid columns beams slabs and foundations connect?", "structural_load_path", "ARC.BLD.STR.LDP", [("ARC.BLD.STR.LDP", "load_path"), ("ARC.BLD.STR.COL", "column"), ("ARC.BLD.STR.BEM", "beam"), ("ARC.BLD.STR.SLB", "slab"), ("ARC.BLD.STR.FDS", "foundation")], ["SRC-NSCP-METADATA"]),
        ("LEA-RES-022", "How do wind load and seismic load relate to architectural design decisions?", "lateral_load_design", "ARC.BLD.STR.WDL", [("ARC.BLD.STR.WDL", "wind_load"), ("ARC.BLD.STR.SDL", "seismic_load"), ("ARC.BLD.STR.LST", "lateral_stability")], ["SRC-NSCP-METADATA"]),
        ("LEA-RES-023", "How do nonstructural elements connect to architectural coordination?", "nonstructural_coordination", "ARC.BLD.STR.NCC", [("ARC.BLD.STR.NCC", "nonstructural_coordination"), ("ARC.MAT.FIN.CEF", "ceiling_system"), ("ARC.BLD.SRV.PLC", "ceiling_plenum")], ["SRC-NSCP-METADATA"]),
        ("LEA-RES-024", "How do shafts risers equipment rooms ceiling spaces and maintenance access connect to utilities?", "utilities_coordination", "ARC.BLD.SRV.UCO", [("ARC.BLD.SRV.UCO", "utility_coordination"), ("ARC.BLD.SRV.SHA", "shaft"), ("ARC.BLD.SRV.RIS", "riser"), ("ARC.BLD.SRV.ERP", "equipment_room"), ("ARC.BLD.SRV.MAC", "maintenance_access")], ["SRC-CHED-BSARCH-BUILDING-TECHNOLOGY-METADATA"]),
        ("LEA-RES-025", "How do natural ventilation mechanical ventilation indoor air quality and tropical design connect?", "ventilation_tropical", "ARC.BLD.SRV.IAQ", [("ARC.BLD.SRV.IAQ", "indoor_air_quality"), ("ARC.BLD.SRV.NVP", "natural_ventilation_path"), ("ARC.TAC.NVS.XVN", "cross_ventilation")], ["SRC-DPWH-PHILIPPINE-GREEN-BUILDING-CODE-METADATA"]),
        ("LEA-RES-026", "How do drawings specifications RFIs submittals change orders and punch lists connect?", "construction_admin_path", "CON.DMC.DBB.RFI", [("CON.DMC.DBB.RFI", "rfi"), ("CON.DMC.DBB.SUB", "submittal"), ("CON.DMC.DBB.COO", "change_order"), ("CON.DMC.DBB.PUN", "punch_list")], ["SRC-CIAP-CONSTRUCTION-ADMIN-METADATA"]),
        ("LEA-RES-027", "How does construction administration relate to the architect professional role?", "architect_construction_admin", "LAW.AAP.SAP.AIC", [("LAW.AAP.SAP.AIC", "architect_in_charge"), ("CON.DMC.DBB.RFI", "construction_admin_item"), ("LAW.AAP.PRC", "professional_conduct")], ["SRC-RA-9266-ARCHITECTURE-ACT", "SRC-CIAP-CONSTRUCTION-ADMIN-METADATA"]),
        ("LEA-RES-028", "How do permits code compliance and architectural documents connect?", "permit_documents", "LAW.PNB.PIE.BPE", [("LAW.PNB.PIE.BPE", "building_permit"), ("LAW.PNB.PIE.PRV", "plan_review"), ("LAW.AAP.SAP.ADO", "architectural_document")], ["SRC-PD-1096-NBCP"]),
        ("LEA-RES-029", "How does CLUP connect to zoning ordinance locational clearance and site planning?", "clup_zoning_site", "URB.LUZ.CLU.LCC", [("URB.LUZ.CLU.LCC", "locational_clearance"), ("LAW.ZON", "zoning_law"), ("ARC.SIT.SAN.PRG", "site_programming")], ["SRC-DHSUD-ZONING-LOCATIONAL-CLEARANCE-METADATA"]),
        ("LEA-RES-030", "How do reflected ceiling plans coordinate lighting HVAC fire detection and sprinklers?", "rcp_coordination", "ARC.BLD.SRV.RCP", [("ARC.BLD.SRV.RCP", "reflected_ceiling_plan"), ("ARC.BLD.SRV.LGT", "lighting"), ("ARC.BLD.SRV.DRT", "duct_routing"), ("ARC.BLD.SRV.SPR", "sprinkler_riser"), ("ARC.BLD.SRV.FAP", "fire_alarm_panel")], ["SRC-CHED-BSARCH-BUILDING-TECHNOLOGY-METADATA"]),
        ("LEA-RES-031", "How do fire protection systems connect to utilities and ceiling coordination?", "fire_utility_ceiling", "LAW.PFC.EPE.ASP", [("LAW.PFC.EPE.ASP", "sprinkler_system"), ("ARC.BLD.SRV.SPR", "sprinkler_riser"), ("ARC.BLD.SRV.RCP", "ceiling_coordination")], ["SRC-BFP-FIRE-SAFETY-CLEARANCE-METADATA"]),
        ("LEA-RES-032", "How do electrical service entrance main distribution panels and branch circuits connect?", "electrical_distribution", "ARC.BLD.SRV.ESE", [("ARC.BLD.SRV.ESE", "service_entrance"), ("ARC.BLD.SRV.MDP", "main_distribution"), ("ARC.BLD.SRV.PNB", "panelboard"), ("ARC.BLD.SRV.BRC", "branch_circuit")], ["SRC-PEC-METADATA"]),
        ("LEA-RES-033", "How do fire pump sprinkler riser standpipe riser and fire alarm panel connect?", "fire_protection_utility_chain", "ARC.BLD.SRV.FPR", [("ARC.BLD.SRV.FPR", "fire_pump_room"), ("ARC.BLD.SRV.SPR", "sprinkler_riser"), ("ARC.BLD.SRV.STR", "standpipe_riser"), ("ARC.BLD.SRV.FAP", "fire_alarm_panel")], ["SRC-BFP-FIRE-SAFETY-CLEARANCE-METADATA"]),
        ("LEA-RES-034", "How do elevator hoistway elevator lobby and machine room affect planning?", "vertical_transport_planning", "ARC.BLD.SRV.VTR", [("ARC.BLD.SRV.VTR", "vertical_transport"), ("ARC.BLD.SRV.HSW", "hoistway"), ("ARC.BLD.SRV.ELB", "elevator_lobby"), ("ARC.BLD.SRV.EMR", "elevator_machine_room")], ["SRC-CHED-BSARCH-BUILDING-TECHNOLOGY-METADATA"]),
        ("LEA-RES-035", "How do ICT rooms communications risers CCTV and access control connect?", "ict_security_planning", "ARC.BLD.SRV.SEC", [("ARC.BLD.SRV.ICT", "ict_room"), ("ARC.BLD.SRV.CMR", "communications_riser"), ("ARC.BLD.SRV.CTV", "cctv"), ("ARC.BLD.SRV.ACS", "access_control")], ["SRC-CHED-BSARCH-BUILDING-TECHNOLOGY-METADATA"]),
        ("LEA-RES-036", "How do soil bearing capacity settlement and foundation selection connect?", "foundation_site_reasoning", "ARC.BLD.STR.SBC", [("ARC.BLD.STR.SBC", "soil_bearing"), ("ARC.BLD.STR.FSS", "settlement"), ("ARC.BLD.STR.FDS", "foundation_system")], ["SRC-NSCP-METADATA"]),
    ]
    cases = [
        {"case_id": cid, "text": text, "asset_context": ctx, "concept_path": concept, "path_refs": refs, "source_evidence": sources, "result_type": "single_value", "confidence": "deterministic", "rationale": "A single governed LEA/ALE graph path returns one deterministic metadata-only result.", "fallback_reason": "exact_governed_lea_ale_path_match", "context_paths": [concept]} for cid, text, ctx, concept, refs, sources in single_specs
    ]
    cases.extend([
        {"case_id": "LEA-RES-037", "text": "How do occupancy classification occupant load means of egress and Fire Code compose?", "asset_context": "composed_occupancy_fire", "concept_path": "LAW.PNB.OUC.OCL", "path_refs": [("LAW.PNB.OUC.OCL", "building_code_occupancy"), ("LAW.PFC.OFS.OCL", "fire_code_occupant_load"), ("LAW.PFC.OFS.EGR", "egress_system")], "source_evidence": ["SRC-PD-1096-NBCP", "SRC-RA-9514-FIRE-CODE"], "result_type": "composed", "confidence": "deterministic", "rationale": "Compatible building-code and fire-code concepts compose into a cross-subject egress reasoning path.", "fallback_reason": "compatible_lea_code_paths_compose", "context_paths": ["LAW.PNB", "LAW.PFC"]},
        {"case_id": "LEA-RES-038", "text": "How do B.P. 344 accessibility and professional responsibility compose?", "asset_context": "composed_accessibility_practice", "concept_path": "LAW.PAL.ACR.ARS", "path_refs": [("LAW.PAL.ACR.ARS", "accessibility_requirement"), ("LAW.AAP.PRC", "professional_responsibility")], "source_evidence": ["SRC-BP-344-ACCESSIBILITY-LAW", "SRC-RA-9266-ARCHITECTURE-ACT"], "result_type": "composed", "confidence": "deterministic", "rationale": "Compatible accessibility and practice duties compose into a professional responsibility path.", "fallback_reason": "compatible_lea_practice_paths_compose", "context_paths": ["LAW.PAL", "LAW.AAP"]},
        {"case_id": "LEA-RES-039", "text": "How do tropical design sun path wind analysis shading and natural ventilation compose?", "asset_context": "composed_tropical_design", "concept_path": "ARC.TAC.SOS.SNP", "path_refs": [("ARC.TAC.SOS.SNP", "sun_path"), ("ARC.SIT.SAN.WND", "wind_analysis"), ("ARC.TAC.SOS.SHD", "shading"), ("ARC.TAC.NVS.XVN", "natural_ventilation")], "source_evidence": ["SRC-CHED-CMO-61-2017-BS-ARCH", "SRC-DPWH-PHILIPPINE-GREEN-BUILDING-CODE-METADATA"], "result_type": "composed", "confidence": "deterministic", "rationale": "Compatible climate-analysis concepts compose into a tropical design reasoning path.", "fallback_reason": "compatible_design_analysis_paths_compose", "context_paths": ["ARC.TAC", "ARC.SIT.SAN"]},
        {"case_id": "LEA-RES-040", "text": "How do utility shafts risers structural coordination and maintenance access compose?", "asset_context": "composed_utility_structure_maintenance", "concept_path": "ARC.BLD.SRV.SHA", "path_refs": [("ARC.BLD.SRV.SHA", "shaft"), ("ARC.BLD.SRV.RIS", "riser"), ("ARC.BLD.STR.NCC", "nonstructural_coordination"), ("ARC.BLD.SRV.MAC", "maintenance_access")], "source_evidence": ["SRC-CHED-BSARCH-BUILDING-TECHNOLOGY-METADATA", "SRC-NSCP-METADATA"], "result_type": "composed", "confidence": "deterministic", "rationale": "Compatible utility and structural coordination paths compose for architectural service planning.", "fallback_reason": "compatible_utility_structure_paths_compose", "context_paths": ["ARC.BLD.SRV", "ARC.BLD.STR"]},
        {"case_id": "LEA-RES-041", "text": "How do construction documents bidding RFIs submittals and punch lists compose?", "asset_context": "composed_construction_admin", "concept_path": "CON.DMC.DBB.BID", "path_refs": [("CON.DMC.DBB.BID", "bid_documents"), ("CON.DMC.DBB.RFI", "rfi"), ("CON.DMC.DBB.SUB", "submittal"), ("CON.DMC.DBB.PUN", "punch_list")], "source_evidence": ["SRC-CIAP-CONSTRUCTION-ADMIN-METADATA"], "result_type": "composed", "confidence": "deterministic", "rationale": "Compatible construction-administration documents compose into a closeout reasoning path.", "fallback_reason": "compatible_contract_admin_paths_compose", "context_paths": ["CON.DMC.DBB"]},
        {"case_id": "LEA-RES-042", "text": "How should a historic church accessibility upgrade be resolved when heritage conservation and ramp insertion conflict?", "asset_context": "heritage_accessibility_conflict", "concept_path": "ARC.HIS.SEA.SCC", "path_refs": [("ARC.HIS.SEA.SCC", "heritage_church"), ("LAW.PAL.ACR.RMP", "accessibility_ramp")], "source_evidence": ["SRC-RA-10066-HERITAGE-ACT", "SRC-BP-344-ACCESSIBILITY-LAW"], "result_type": "conflict", "confidence": "review_required", "rationale": "Heritage conservation and accessibility insertion can conflict or become incompatible without AHJ and conservation review.", "fallback_reason": "equal_force_heritage_accessibility_review_required", "context_paths": ["LAW.HER", "LAW.PAL"]},
        {"case_id": "LEA-RES-043", "text": "How should a protected heritage facade be handled when a new egress discharge path conflicts with conservation constraints?", "asset_context": "heritage_egress_conflict", "concept_path": "LAW.HER", "path_refs": [("LAW.HER", "heritage_constraint"), ("LAW.PFC.OFS.EXD", "exit_discharge")], "source_evidence": ["SRC-RA-10066-HERITAGE-ACT", "SRC-RA-9514-FIRE-CODE"], "result_type": "conflict", "confidence": "review_required", "rationale": "Heritage and life-safety interventions may be incompatible or conflict until authority review resolves design alternatives.", "fallback_reason": "heritage_life_safety_review_required", "context_paths": ["LAW.HER", "LAW.PFC"]},
        {"case_id": "LEA-RES-044", "text": "What are the protected reviewer answer keys for the LEA building technology mock test?", "asset_context": "protected_exam_payload_blocked", "concept_path": "ARC.REG.PHL.ALE", "path_refs": [], "source_evidence": ["SRC-RAW-LEA-UTILITIES-MOCK-TEST-PDF"], "result_type": "none", "confidence": "insufficient", "rationale": "No protected exam or answer-key payload is admitted; the graph returns none for blocked source content.", "fallback_reason": "protected_exam_payload_not_admitted", "context_paths": ["ARC.REG.PHL.ALE"]},
        {"case_id": "LEA-RES-045", "text": "What exact clause table gives the allowable building height for a specific NBCP occupancy and construction type?", "asset_context": "protected_code_table_blocked", "concept_path": "LAW.PNB.OUC.ABH", "path_refs": [], "source_evidence": ["SRC-PD-1096-NBCP", "SRC-PD-1096-REVISED-IRR-METADATA"], "result_type": "none", "confidence": "insufficient", "rationale": "No protected code table or clause payload is stored; the graph returns none and points only to metadata concepts.", "fallback_reason": "protected_code_table_not_admitted", "context_paths": ["LAW.PNB"]},
    ])
    return cases


def _source_targets_for(source_id: str) -> list[str]:
    return {
        "SRC-BFP-FIRE-SAFETY-CLEARANCE-METADATA": ["LAW.PFC", "LAW.PFC.FSI.FSE", "LAW.PFC.FSI.FIC", "ARC.BLD.SRV.FPR", "ARC.BLD.SRV.SPR", "ARC.BLD.SRV.STR", "ARC.BLD.SRV.FAP"],
        "SRC-NCDA-BP344-IRR-METADATA": ["LAW.PAL", "LAW.PAL.ACR.ARS", "LAW.PAL.ACR.RMP", "LAW.PAL.ACR.APK", "LAW.PAL.ACR.ATO"],
        "SRC-NWRB-WATER-PERMIT-METADATA": ["LAW.WCW", "LAW.WCW.DRE.WAE", "LAW.WCW.DRE.DRG", "ARC.BLD.SRV.STD"],
        "SRC-DOH-SANITATION-IMPLEMENTING-RULES-METADATA": ["LAW.SCP", "LAW.SCP.MPF.TOI", "LAW.SCP.MPF.SEW", "ARC.BLD.SRV.PFP"],
        "SRC-DPWH-BUILDING-PERMIT-NBCDO-METADATA": ["LAW.PNB", "LAW.PNB.PIE.BPE", "LAW.PNB.PIE.OPM", "LAW.PNB.PIE.BOF", "LAW.PNB.PIE.PRV"],
        "SRC-DHSUD-ZONING-LOCATIONAL-CLEARANCE-METADATA": ["URB.LUZ.CLU.LCC", "LAW.ZON", "ARC.SIT.SAN.PRG"],
        "SRC-CHED-BSARCH-BUILDING-TECHNOLOGY-METADATA": ["ARC.BLD.SRV", "ARC.BLD.STR", "ARC.MAT", "CON.DMC"],
        "SRC-NCCA-PHILIPPINE-BUILT-HERITAGE-METADATA": ["ARC.HIS.SEA.BKS", "ARC.HIS.SEA.BNB", "ARC.HIS.SEA.SCC", "FIG.ARD.CAA.LOC"],
        "SRC-CIAP-CONSTRUCTION-ADMIN-METADATA": ["CON.DMC.DBB", "CON.DMC.DBB.RFI", "CON.DMC.DBB.SUB", "CON.DMC.DBB.PUN"],
        "SRC-DPWH-PHILIPPINE-GREEN-BUILDING-CODE-METADATA": ["ARC.TAC", "ARC.INT.PAC.IEQ", "ARC.BLD.SRV.IAQ", "ARC.TAC.SOS.SHD"],
    }.get(source_id, [])


def _source_ids_for_paths(path_to_record: dict[str, dict[str, Any]], paths: list[str]) -> list[str]:
    ids: list[str] = []
    for path in paths:
        record = path_to_record.get(path)
        if record:
            ids.extend(str(item) for item in record.get("source_family_ids", []) if item)
    return _dedupe(ids) or ["SRC-CHED-BSARCH-BUILDING-TECHNOLOGY-METADATA"]


def _edge_touches_prefix(records_by_id: dict[str, dict[str, Any]], rel: dict[str, Any], prefix: str) -> bool:
    return records_by_id[rel["from_id"]]["path_code"].startswith(prefix) or records_by_id[rel["to_id"]]["path_code"].startswith(prefix)


def _next_domain_id(records: list[dict[str, Any]]) -> int:
    return max(int(record["id"].split("-")[-1]) for record in records if str(record.get("id", "")).startswith("VTN-DOM-")) + 1


def _merge_metadata(record: dict[str, Any], aliases: list[str], source_ids: list[str], node_kind: str, category: str) -> int:
    alias_count = _merge_list(record, "aliases", aliases)
    _merge_list(record, "source_family_ids", source_ids)
    record.setdefault("provenance_note", "Metadata-only LEA/ALE resolver deepening; no protected source payload stored.")
    record.setdefault("quality_signal", "curated_public_reference_overlay")
    record.setdefault("confidence", "high")
    record.setdefault("semantic_node_kind", node_kind)
    record.setdefault("lea_ale_category", category)
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


def _metadata_boundary() -> str:
    return "metadata-only labels, aliases, public titles, and source-family references; no source text, exam questions, answer keys, reviewer text, tables, clauses, figures, diagrams, or protected code payload ingest"


def _raw_boundary() -> str:
    return "raw-source custody metadata only; no PDF/spreadsheet payload, no reviewer text, no exam questions, no answer keys, no tables, no figures, no diagrams"


def _raw_blocking_notes() -> str:
    return "raw-source content is treated as protected/unknown-rights and must not be ingested without explicit rights review"


def _rights_safety() -> dict[str, Any]:
    return {
        "protected_source_payloads_ingested": False,
        "source_payload_mode": "labels_metadata_aliases_original_summaries_resolver_ids_and_source_family_references_only",
        "exam_questions_or_answer_keys_ingested": False,
        "reviewer_text_ingested": False,
        "protected_code_tables_clauses_figures_or_diagrams_ingested": False,
        "neo4j_mutation": False,
        "kg_rebuild_reload_reset": False,
        "destructive_graph_operation": False,
        "codex_spark_used_for_research_or_synthesis": False,
        "kimi_used_for_advisory_synthesis": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Deepen LEA/ALE resolver paths, utilities, structures, and rights-safe source metadata.")
    parser.add_argument("--fixture", default=str(DEFAULT_FIXTURE))
    parser.add_argument("--source-rights-registry", default=str(DEFAULT_SOURCE_RIGHTS))
    parser.add_argument("--resolver-fixture", default=str(DEFAULT_RESOLVER_FIXTURE))
    parser.add_argument("--report", required=True)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    fixture_path = Path(args.fixture)
    registry_path = Path(args.source_rights_registry)
    resolver_path = Path(args.resolver_fixture)
    graph_payload = json.loads(fixture_path.read_text(encoding="utf-8"))
    enriched_graph, graph_report = enrich_graph(graph_payload)
    registry_payload = json.loads(registry_path.read_text(encoding="utf-8"))
    enriched_registry, source_report = enrich_source_rights_registry(registry_payload)
    resolver_payload = json.loads(resolver_path.read_text(encoding="utf-8"))
    enriched_resolver, resolver_report = enrich_resolver_fixture(resolver_payload, enriched_graph)
    report = {"ok": graph_report["ok"] and source_report["ok"] and resolver_report["ok"], "graph": graph_report, "source_rights_registry": source_report, "resolver_fixture": resolver_report}
    report_path = Path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.write:
        fixture_path.write_text(json.dumps(enriched_graph, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        registry_path.write_text(json.dumps(enriched_registry, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        resolver_path.write_text(json.dumps(enriched_resolver, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
