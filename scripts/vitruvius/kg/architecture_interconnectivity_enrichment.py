from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

from vitruvius.kg.lea_ale_semantic_enrichment import OWNER

GENERATION_METHOD = (
    "steward_governed_architecture_interconnectivity_from_kimi_guided_"
    "materials_people_works_and_source_safe_public_references"
)
RELEASE_VERSION = "0.9.0"
SCOPE_NOTE = (
    "Kimi-guided architecture interconnectivity enrichment using source-safe public metadata, "
    "official Pritzker laureate facts, authority-file crosswalks, and steward-authored original "
    "summaries. No protected source payloads, reviewer text, exam questions, code clauses, "
    "tables, figures, diagrams, biographies, or protected work descriptions are stored."
)
DEFAULT_FIXTURE = Path("scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json")
DEFAULT_SOURCE_RIGHTS = Path(".ai/03_plans/AEC-MEPFS-Backbone/registry-candidates/source-rights-registry.json")
DEFAULT_RESOLVER_FIXTURE = Path("scripts/tests/fixtures/aec_mepfs_backbone/valid_readiness_s2.json")

SOURCE_REFERENCES: list[dict[str, str]] = [
    {
        "source_id": "SRC-PRITZKER-LAUREATES-OFFICIAL",
        "source_family": "Official Pritzker Architecture Prize laureates metadata",
        "publisher_authority": "The Hyatt Foundation / The Pritzker Architecture Prize",
        "official_url": "https://www.pritzkerprize.com/laureates",
        "source_rights_class": "reference_only",
        "clearance_state": "planning_reference_only",
        "intended_vitruvius_use": "metadata-only laureate names, award years, official profile URLs, and prize-status crosswalks; no essays, citations, images, or long source text ingested",
    },
    {
        "source_id": "SRC-WIKIDATA-CC0-AEC-IDENTIFIERS",
        "source_family": "Wikidata CC0 architecture people, works, awards, and material identifiers",
        "publisher_authority": "Wikidata community / Wikimedia Foundation",
        "official_url": "https://www.wikidata.org/wiki/Wikidata:Licensing",
        "source_rights_class": "metadata_crosswalk",
        "clearance_state": "metadata_crosswalk_planned",
        "intended_vitruvius_use": "metadata-only authority identifiers, aliases, award-year hints, and work identifiers cross-checked against safer public sources where needed",
    },
    {
        "source_id": "SRC-GETTY-VOCABULARIES-AAT-ULAN-TGN",
        "source_family": "Getty Vocabularies AAT ULAN TGN linked open data metadata",
        "publisher_authority": "Getty Research Institute",
        "official_url": "https://www.getty.edu/research/tools/vocabularies/obtain/download.html",
        "source_rights_class": "metadata_crosswalk",
        "clearance_state": "metadata_crosswalk_planned",
        "intended_vitruvius_use": "metadata-only architecture/material term, artist/architect authority, and place authority crosswalks with attribution requirements respected",
    },
    {
        "source_id": "SRC-VIAF-AUTHORITY-DATA",
        "source_family": "VIAF international authority metadata",
        "publisher_authority": "OCLC / VIAF contributors",
        "official_url": "https://viaf.org/viaf/data",
        "source_rights_class": "metadata_crosswalk",
        "clearance_state": "metadata_crosswalk_planned",
        "intended_vitruvius_use": "metadata-only personal-name, firm-name, and authority identifier crosswalks; no copyrighted source text ingested",
    },
    {
        "source_id": "SRC-LOC-LINKED-DATA-AUTHORITY",
        "source_family": "Library of Congress linked data authority metadata",
        "publisher_authority": "Library of Congress",
        "official_url": "https://www.loc.gov/apis/additional-apis/linked-data-service/",
        "source_rights_class": "metadata_crosswalk",
        "clearance_state": "metadata_crosswalk_planned",
        "intended_vitruvius_use": "metadata-only authority identifiers and subject-heading crosswalks for people, works, materials, and movements",
    },
    {
        "source_id": "SRC-AIA-CONTRACTS-PRACTICE-METADATA",
        "source_family": "American Institute of Architects contract and practice metadata",
        "publisher_authority": "American Institute of Architects",
        "official_url": "https://www.aia.org/",
        "source_rights_class": "reference_only",
        "clearance_state": "planning_reference_only",
        "intended_vitruvius_use": "metadata-only AIA organization, practice, contract-document, and standards-family classification; no contract text, guide text, tables, figures, or protected payloads ingested",
    },
    {
        "source_id": "SRC-RIBA-PLAN-OF-WORK-METADATA",
        "source_family": "RIBA Plan of Work and practice metadata",
        "publisher_authority": "Royal Institute of British Architects",
        "official_url": "https://www.architecture.com/knowledge-and-resources/resources-landing-page/riba-plan-of-work",
        "source_rights_class": "reference_only",
        "clearance_state": "planning_reference_only",
        "intended_vitruvius_use": "metadata-only RIBA organization, work-stage, practice, and standards-family classification; no guide text, tables, diagrams, or protected payloads ingested",
    },
    {
        "source_id": "SRC-MOMA-ARCHITECTURE-DESIGN-METADATA",
        "source_family": "Museum of Modern Art architecture and design collection metadata",
        "publisher_authority": "The Museum of Modern Art",
        "official_url": "https://www.moma.org/collection/",
        "source_rights_class": "metadata_crosswalk",
        "clearance_state": "metadata_crosswalk_planned",
        "intended_vitruvius_use": "metadata-only modern architecture work, architect, movement, and collection crosswalks; no image, essay, catalog, or protected collection text ingested",
    },
    {
        "source_id": "SRC-ICE-ENGINEERING-HERITAGE-METADATA",
        "source_family": "Institution of Civil Engineers engineering heritage metadata",
        "publisher_authority": "Institution of Civil Engineers",
        "official_url": "https://www.ice.org.uk/",
        "source_rights_class": "reference_only",
        "clearance_state": "planning_reference_only",
        "intended_vitruvius_use": "metadata-only engineering heritage names, people, work identifiers, and structural-system classification; no article text, images, tables, or protected payloads ingested",
    },
    {
        "source_id": "SRC-CTBUH-SKYSCRAPER-CENTER-METADATA",
        "source_family": "CTBUH tall building and structural system metadata",
        "publisher_authority": "Council on Tall Buildings and Urban Habitat",
        "official_url": "https://www.ctbuh.org/",
        "source_rights_class": "metadata_crosswalk",
        "clearance_state": "metadata_crosswalk_planned",
        "intended_vitruvius_use": "metadata-only tall-building names, people, system terms, and public identifier crosswalks; no database payload, images, drawings, or protected text ingested",
    },
    {
        "source_id": "SRC-NCCA-TALAPAMANA-PUBLIC-METADATA",
        "source_family": "NCCA TALAPAMANA public built-heritage metadata",
        "publisher_authority": "National Commission for Culture and the Arts",
        "official_url": "https://talapamana.ncca.gov.ph/",
        "source_rights_class": "reference_only",
        "clearance_state": "planning_reference_only",
        "intended_vitruvius_use": "metadata-only public work names, creator names, aliases, heritage-status labels, and place/source crosswalks; no articles, images, drawings, long descriptions, or protected payloads ingested",
    },
]

MATERIAL_SOURCE_IDS = [
    "SRC-GETTY-VOCABULARIES-AAT-ULAN-TGN",
    "SRC-BSI-BSDD",
    "SRC-CHED-BSARCH-BUILDING-TECHNOLOGY-METADATA",
]
PEOPLE_SOURCE_IDS = [
    "SRC-PRITZKER-LAUREATES-OFFICIAL",
    "SRC-WIKIDATA-CC0-AEC-IDENTIFIERS",
    "SRC-VIAF-AUTHORITY-DATA",
    "SRC-LOC-LINKED-DATA-AUTHORITY",
]
STANDARDS_CLASSIFICATION_SOURCE_IDS = [
    "SRC-AIA-CONTRACTS-PRACTICE-METADATA",
    "SRC-RIBA-PLAN-OF-WORK-METADATA",
    "SRC-NIBS-NBIMS-OMNICLASS",
    "SRC-NIBS-WBDG-COMMISSIONING",
    "SRC-ISO-12006-2",
    "SRC-ICC-ICODES-2024",
]
NCCA_SOURCE_IDS = ["SRC-NCCA-NATIONAL-ARTISTS-ARCHITECTURE", "SRC-NCCA-PHILIPPINE-BUILT-HERITAGE-METADATA"]
PHILIPPINE_ARCHITECTURE_SOURCE_IDS = [*NCCA_SOURCE_IDS, "SRC-NCCA-TALAPAMANA-PUBLIC-METADATA"]
PROJECT_EVIDENCE_SOURCE_IDS = PEOPLE_SOURCE_IDS + [
    "SRC-MOMA-ARCHITECTURE-DESIGN-METADATA",
]
ENGINEERING_WORK_SOURCE_IDS = PEOPLE_SOURCE_IDS + [
    "SRC-ICE-ENGINEERING-HERITAGE-METADATA",
    "SRC-CTBUH-SKYSCRAPER-CENTER-METADATA",
]

# parent_path, suffix, label, aliases, definition, kind, category, source_ids
NODE_GROUPS: list[tuple[str, str, str, list[str], str, str, str, list[str]]] = []

def _add_node(parent: str, suffix: str, label: str, aliases: list[str], definition: str, kind: str, category: str, source_ids: list[str] | None = None) -> None:
    NODE_GROUPS.append((parent, suffix, label, aliases, definition, kind, category, source_ids or MATERIAL_SOURCE_IDS))

# Dedicated material taxonomy/facet: properties, assemblies, concrete, metals, timber/bio, stone, finishes, glass, membranes, insulation, earth.
material_nodes = [
    ("MAT", "PRF", "Material Performance Properties", ["material properties", "material performance", "performance characteristics"], "Cross-cutting material-performance facet for strength, fire, moisture, acoustic, thermal, environmental, and perceptual properties."),
    ("MAT.PRF", "MEC", "Mechanical Material Properties", ["strength properties", "mechanical properties"], "Material properties used to reason about load transfer, stiffness, strength, and deformation in architectural systems."),
    ("MAT.PRF", "FIR", "Fire Material Properties", ["fire behavior", "fire performance"], "Material behavior relevant to fire resistance, flame spread, smoke, and fire-rated assemblies."),
    ("MAT.PRF", "MOI", "Moisture Material Properties", ["moisture behavior", "water resistance"], "Material behavior relevant to water, vapor, humidity, decay, and wet-area service conditions."),
    ("MAT.PRF", "ACO", "Acoustic Material Properties", ["acoustic performance", "sound properties"], "Material properties affecting sound absorption, sound isolation, reverberation, and interior acoustic comfort."),
    ("MAT.PRF", "THE", "Thermal And Optical Material Properties", ["thermal properties", "solar optical properties"], "Material properties affecting thermal mass, insulation, reflectance, daylight, glare, and heat gain."),
    ("MAT.PRF", "ENV", "Environmental Material Properties", ["sustainability properties", "low carbon material metrics"], "Material attributes used for embodied carbon, recyclability, reuse, local sourcing, and lifecycle reasoning."),
    ("MAT.PRF", "AES", "Aesthetic And Tactile Material Properties", ["materiality", "texture", "surface character"], "Perceptual material qualities affecting texture, color, reflectance, craft, atmosphere, and human experience."),
    ("MAT", "ASM", "Material Assemblies", ["building assemblies", "material assemblies"], "Cross-cutting facet for wall, floor, roof, ceiling, facade, wet-area, fire-rated, and acoustic assemblies."),
    ("MAT.ASM", "WAL", "Wall Assembly", ["wall assembly", "wall system"], "Layered wall construction coordinating structure, substrate, finishes, insulation, moisture control, and fire or acoustic performance."),
    ("MAT.ASM", "FLR", "Floor Assembly", ["floor assembly", "floor system"], "Floor construction coordinating structure, underlayment, finishes, acoustics, moisture, slip resistance, and durability."),
    ("MAT.ASM", "ROF", "Roof Assembly", ["roof assembly", "roof system"], "Roof construction coordinating waterproofing, insulation, drainage, structure, maintenance access, and climate response."),
    ("MAT.ASM", "CEI", "Ceiling Assembly", ["ceiling assembly", "ceiling system"], "Ceiling construction coordinating finish, plenum access, acoustics, fire detection, sprinklers, lighting, and HVAC diffusers."),
    ("MAT.ASM", "FAC", "Facade Assembly", ["facade assembly", "envelope assembly"], "Envelope assembly coordinating cladding, glazing, weather barriers, anchors, thermal control, and maintenance."),
    ("MAT.ASM", "WET", "Waterproofed Wet Area Assembly", ["wet area assembly", "waterproofed bathroom assembly"], "Wet-area assembly coordinating tile, waterproofing, slope, substrate, drains, sealants, and sanitation maintenance."),
    ("MAT.ASM", "FRW", "Fire Rated Wall Assembly", ["fire-rated wall", "rated wall assembly"], "Wall assembly intended to maintain compartmentation and coordinate firestopping, doors, joints, and penetrations."),
    ("MAT.ASM", "ACC", "Acoustic Ceiling Assembly", ["acoustic ceiling", "sound absorptive ceiling"], "Ceiling assembly using absorptive materials and detailing to manage reverberation and above-ceiling coordination."),
    ("MAT.ASM", "CUR", "Curtain Wall Assembly", ["curtain wall", "glazed facade"], "Non-load-bearing glazed facade assembly coordinating mullions, glass, anchors, drainage, thermal breaks, and movement."),
    ("MAT.ASM", "WIN", "Window Assembly", ["window system", "fenestration assembly"], "Opening assembly coordinating glazing, frame, hardware, flashing, air/water control, daylight, and ventilation."),
    ("MAT.ASM", "DOR", "Door Assembly", ["door system", "door hardware assembly"], "Door assembly coordinating leaf, frame, hardware, accessibility clearances, fire rating, security, and egress function."),
    ("MAT", "EAR", "Earth And Thatch Materials", ["earth materials", "earthen construction", "thatch materials"], "Material family for earth, adobe, compressed earth, rammed earth, cob, thatch, and related low-energy vernacular construction."),
    ("MAT.EAR", "RME", "Rammed Earth", ["rammed earth", "compacted earth wall"], "Compacted-earth wall material associated with thermal mass, local material use, and moisture-sensitive detailing."),
    ("MAT.EAR", "ADB", "Adobe", ["adobe", "sun-dried earth block"], "Earthen masonry material formed from soil-based units and associated with climate, craft, and moisture protection."),
    ("MAT.EAR", "CEB", "Compressed Earth Block", ["CEB", "compressed earth block"], "Compressed soil block material used in low-carbon wall systems where stabilization, moisture, and detailing are controlled."),
    ("MAT.EAR", "COB", "Cob", ["cob", "monolithic earth wall"], "Hand-formed earth material used for thick walls and sculpted forms, requiring weather protection and compatible finishes."),
    ("MAT.EAR", "THC", "Thatch", ["thatch", "vegetal roofing"], "Plant-based roofing material used in vernacular buildings and requiring pitch, ventilation, replacement cycles, and fire-risk awareness."),
]
for parent, suffix, label, aliases, definition in material_nodes:
    _add_node(parent, suffix, label, aliases, definition, "material_taxonomy_facet", "materials_taxonomy")

concrete_nodes = [
    ("MAT.CMA.CEM", "CIP", "Cast In Place Concrete", ["cast-in-place concrete", "in-situ concrete"], "Concrete placed and cured in its final location, coordinating formwork, reinforcement, curing, joints, finish, and quality control."),
    ("MAT.CMA.CEM", "PSC", "Prestressed Concrete", ["prestressed concrete", "prestressing"], "Concrete system in which internal compressive stress is introduced to improve span and cracking behavior."),
    ("MAT.CMA.CEM", "PTC", "Post Tensioned Concrete", ["post-tensioned concrete", "post tensioning"], "Prestressed concrete where tendons are tensioned after placement, affecting spans, slab depth, penetrations, and coordination."),
    ("MAT.CMA.CEM", "EXP", "Exposed Concrete", ["architectural concrete", "fair-faced concrete", "beton brut"], "Concrete intentionally visible as finish, requiring formwork quality, mix control, joint planning, and surface treatment."),
    ("MAT.CMA.CEM", "BFC", "Board Formed Concrete", ["board-formed concrete", "timber board imprint concrete"], "Exposed concrete finish where boards shape surface texture and construction joint rhythm."),
    ("MAT.CMA.CEM", "LWC", "Lightweight Concrete", ["lightweight concrete", "lightweight aggregate concrete"], "Concrete using lightweight aggregates or voiding strategies for reduced dead load or thermal/acoustic purposes."),
    ("MAT.CMA.CEM", "CHB", "Concrete Hollow Block", ["CHB", "concrete hollow block", "hollow block"], "Hollow concrete masonry unit widely used in Philippine wall construction and coordinated with reinforcement, plaster, openings, and moisture control."),
    ("MAT.CMA.CEM", "RBR", "Reinforcing Bar", ["rebar", "reinforcement bar", "deformed bar"], "Steel reinforcement embedded in concrete or masonry, coordinated with cover, development, spacing, and placement tolerances."),
    ("MAT.CMA.CEM", "AGR", "Aggregate", ["coarse aggregate", "fine aggregate", "sand and gravel"], "Granular material in concrete and mortar that affects strength, workability, texture, durability, and local availability."),
    ("MAT.CMA.CEM", "CBN", "Cement Binder", ["cement", "Portland cement", "cementitious binder"], "Cementitious binder used with aggregates and water in concrete, mortar, plaster, and masonry applications."),
]
for item in concrete_nodes:
    _add_node(item[0], item[1], item[2], item[3], item[4], "material_concrete_detail", "materials_taxonomy")

metal_nodes = [
    ("MAT.STM.STS", "STS", "Stainless Steel", ["stainless steel", "corrosion-resistant steel"], "Steel alloy used where corrosion resistance, hygiene, appearance, or durable hardware performance is important."),
    ("MAT.STM.STS", "WST", "Weathering Steel", ["weathering steel", "Corten steel"], "Steel designed to develop a protective patina, requiring detailing for runoff, staining, and exposure conditions."),
    ("MAT.STM.STS", "LGS", "Light Gauge Steel", ["light-gauge steel", "cold-formed steel framing"], "Thin cold-formed steel framing used for partitions, light structural framing, and nonstructural supports."),
    ("MAT.STM.STS", "MDK", "Metal Decking", ["metal deck", "steel decking"], "Profiled steel deck used with floors or roofs, coordinating span, fire rating, acoustics, and concrete topping where used."),
    ("MAT.STM.MEC", "GIS", "Galvanized Iron Sheet", ["GI sheet", "galvanized sheet", "galvanized roofing"], "Galvanized metal sheet common in roofing, cladding, flashing, and Philippine construction detailing."),
    ("MAT.STM.MEC", "RFS", "Roofing Sheet", ["roof sheet", "corrugated roofing sheet"], "Sheet roofing material coordinated with slope, fasteners, underlayment, overlaps, acoustics, and wind uplift."),
    ("MAT.STM.MEC", "SSM", "Standing Seam Metal Roofing", ["standing seam roof", "standing seam metal roofing"], "Metal roof system using concealed clips or raised seams for water shedding and thermal movement."),
    ("MAT.STM.MEC", "ALP", "Aluminum Composite Panel", ["ACP", "aluminum composite panel"], "Composite metal cladding panel requiring fire, joint, substrate, and facade-detailing review."),
]
for item in metal_nodes:
    _add_node(item[0], item[1], item[2], item[3], item[4], "material_metal_detail", "materials_taxonomy")

timber_nodes = [
    ("MAT.TBB.DIL", "HDW", "Hardwood", ["hardwood", "tropical hardwood"], "Dense timber category used in flooring, joinery, furniture, structural members, and heritage work with durability considerations."),
    ("MAT.TBB.DIL", "SFW", "Softwood", ["softwood", "construction lumber"], "Timber category often used in framing, sheathing, temporary works, joinery, and roof structures."),
    ("MAT.TBB.ENW", "GLU", "Glue Laminated Timber", ["glulam", "glue-laminated timber"], "Engineered timber made from bonded laminations for long spans, expressive structures, and controlled fabrication."),
    ("MAT.TBB.ENW", "CLT", "Cross Laminated Timber", ["CLT", "cross-laminated timber"], "Mass timber panel made from cross-oriented layers, used for walls, floors, roofs, and prefabricated assemblies."),
    ("MAT.TBB.ENW", "LVL", "Laminated Veneer Lumber", ["LVL", "laminated veneer lumber"], "Engineered wood product made from bonded veneers for beams, headers, panels, and high-strength timber components."),
    ("MAT.TBB.ENW", "PLY", "Plywood", ["plywood", "plywood sheathing"], "Layered wood panel used in sheathing, cabinetry, formwork, interiors, and furniture."),
    ("MAT.TBB.BAS", "BCM", "Bamboo Culm", ["bamboo culm", "bamboo pole"], "Bamboo stem used in vernacular and sustainable construction, requiring treatment, jointing, and moisture control."),
    ("MAT.TBB.BAS", "RAT", "Rattan", ["rattan", "cane material"], "Flexible palm material used in furniture, screens, craft, interiors, and vernacular assemblies."),
    ("MAT.TBB.BAS", "NIP", "Nipa", ["nipa", "nipa palm", "nipa thatch"], "Palm material associated with Philippine vernacular roofing and walls, requiring replacement and fire/moisture awareness."),
    ("MAT.TBB.BAS", "ANH", "Anahaw", ["anahaw", "anahaw leaves"], "Philippine palm material used in vernacular roofing, screens, or craft where source-supported and locally appropriate."),
    ("MAT.TBB.BAS", "CAP", "Capiz Shell", ["capiz", "capiz shell window", "window shell"], "Translucent shell material associated with Philippine heritage windows and filtered daylight."),
]
for item in timber_nodes:
    _add_node(item[0], item[1], item[2], item[3], item[4], "material_timber_bio_detail", "materials_taxonomy")

stone_finish_nodes = [
    ("MAT.MST.NAS", "GRA", "Granite", ["granite", "granite stone"], "Hard natural stone used for paving, counters, cladding, monuments, and durable finishes."),
    ("MAT.MST.NAS", "MAR", "Marble", ["marble", "marble stone"], "Metamorphic stone used for floors, walls, counters, sculpture, and high-polish interior finishes."),
    ("MAT.MST.NAS", "LIM", "Limestone", ["limestone", "limestone cladding"], "Sedimentary stone used for masonry, cladding, paving, and historic architectural expression."),
    ("MAT.MST.NAS", "SDS", "Sandstone", ["sandstone", "sandstone masonry"], "Sedimentary stone used for masonry, cladding, carving, and heritage construction."),
    ("MAT.MST.NAS", "ADO", "Adobe Stone", ["adobe stone", "volcanic tuff stone"], "Soft volcanic stone historically used in masonry in some Philippine and colonial contexts, requiring weathering awareness."),
    ("MAT.MST.CMU", "HBL", "Hollow Block", ["hollow block", "concrete hollow block"], "Masonry block with voids used for walls and coordinated with reinforcement, plaster, openings, and moisture control."),
    ("MAT.FIP.FLF", "CER", "Ceramic Tile", ["ceramic tile", "wall and floor tile"], "Fired ceramic finish used for floors, walls, wet areas, and cleanable interior surfaces."),
    ("MAT.FIP.FLF", "POR", "Porcelain Tile", ["porcelain tile", "dense ceramic tile"], "Low-porosity ceramic finish used for durable floors, walls, wet areas, and high-traffic interiors."),
    ("MAT.FIP.FLF", "CMT", "Cement Tile", ["cement tile", "encaustic cement tile"], "Cementitious finish tile requiring substrate, sealing, maintenance, and pattern coordination."),
    ("MAT.FIP.FLF", "TRZ", "Terrazzo", ["terrazzo", "terrazzo flooring"], "Composite finish using chips in binder, coordinated with joints, polishing, durability, and maintenance."),
    ("MAT.FIP.FLF", "VIN", "Vinyl Flooring", ["vinyl flooring", "resilient vinyl floor"], "Resilient flooring used for economical, cleanable, and moisture-aware floor finishes."),
    ("MAT.FIP.FLF", "LNO", "Linoleum", ["linoleum", "natural resilient flooring"], "Resilient flooring made from bio-based ingredients, coordinated with substrate, seams, and maintenance."),
    ("MAT.FIP.FLF", "RUB", "Rubber Flooring", ["rubber floor", "rubber flooring"], "Resilient flooring used for slip resistance, acoustics, comfort, and durable circulation areas."),
    ("MAT.FIP.FLF", "CPT", "Carpet", ["carpet", "carpet tile"], "Soft floor finish used for comfort and acoustic absorption, coordinated with maintenance and indoor air quality."),
    ("MAT.FIP.WAF", "PLS", "Plaster", ["plaster", "cement plaster", "gypsum plaster"], "Wet-applied finish used on masonry, concrete, or lath substrates for smooth or textured surfaces."),
    ("MAT.FIP.WAF", "GYB", "Gypsum Board", ["gypsum board", "drywall", "plasterboard"], "Panel product used for partitions, ceilings, linings, fire-rated assemblies, and interior finishes."),
    ("MAT.FIP.WAF", "FCB", "Fiber Cement Board", ["fiber cement board", "cement board"], "Cementitious sheet material used for wet areas, cladding, backing boards, and durable panels."),
    ("MAT.FIP.CES", "APN", "Acoustic Panel", ["acoustic panel", "absorptive panel"], "Panel used to absorb sound and tune room acoustics in interiors such as classrooms, theaters, and offices."),
]
for item in stone_finish_nodes:
    _add_node(item[0], item[1], item[2], item[3], item[4], "material_finish_detail", "materials_taxonomy")

glass_membrane_insulation_nodes = [
    ("MAT.GLA", "FLG", "Float Glass", ["float glass", "annealed glass"], "Flat glass substrate used as a base for many glazing products and architectural openings."),
    ("MAT.GLA", "TPG", "Tempered Glass", ["tempered glass", "toughened glass"], "Heat-treated safety glass used where impact, thermal stress, or breakage behavior requires coordination."),
    ("MAT.GLA", "LOW", "Low E Glass", ["low-e glass", "low emissivity glass"], "Coated glass used to reduce heat transfer and coordinate daylight, glare, and energy performance."),
    ("MAT.GLA", "CWG", "Curtain Wall Glazing", ["curtain wall glazing", "glazed facade panels"], "Glazing used in curtain wall assemblies and coordinated with frame, sealant, movement, and thermal performance."),
    ("MAT.GLA", "SPG", "Spandrel Glass", ["spandrel glass", "opaque facade glass"], "Opaque or treated glass used at slab edges or concealed facade zones in curtain walls."),
    ("MAT.MEM.RME", "WPM", "Waterproofing Membrane", ["waterproofing membrane", "waterproof membrane"], "Membrane layer used to control water ingress at roofs, basements, decks, balconies, and wet areas."),
    ("MAT.MEM.RME", "SBS", "Modified Bitumen Membrane", ["modified bitumen", "SBS membrane"], "Bituminous waterproofing membrane used in roofs and below-grade assemblies with heat or adhesive installation."),
    ("MAT.MEM.RME", "TPO", "TPO Roof Membrane", ["TPO membrane", "thermoplastic polyolefin roof"], "Single-ply thermoplastic roofing membrane used for low-slope roof waterproofing."),
    ("MAT.MEM.RME", "PVM", "PVC Roof Membrane", ["PVC membrane", "PVC roofing"], "Single-ply PVC roof membrane used for low-slope waterproofing and detailing."),
    ("MAT.MEM.RME", "EPD", "EPDM Membrane", ["EPDM", "rubber roofing membrane"], "Synthetic rubber membrane used for roofing, waterproofing, and flexible sheet applications."),
    ("MAT.MEM.VAP", "DPC", "Damp Proof Course", ["DPC", "damp-proof course"], "Barrier layer used to resist capillary moisture movement through walls and foundations."),
    ("MAT.MEM.VAP", "AIR", "Air Barrier", ["air barrier", "air control layer"], "Continuous layer used to control air leakage through the building envelope."),
    ("MAT.MEM.VAP", "VBR", "Vapor Barrier", ["vapour barrier", "vapor control layer"], "Layer used to control water-vapor diffusion and condensation risk."),
    ("MAT.COA.SEA", "ADH", "Construction Adhesive", ["adhesive", "construction adhesive"], "Bonding material used for finishes, panels, membranes, flooring, and assemblies where compatible with substrates."),
    ("MAT.COA.SEA", "SIL", "Silicone Sealant", ["silicone sealant", "weather sealant"], "Elastic sealant used for facade joints, glazing, wet areas, and movement joints."),
    ("MAT.COA.SEA", "PUS", "Polyurethane Sealant", ["PU sealant", "polyurethane sealant"], "Elastomeric sealant used for movement joints, waterproofing details, and construction joints."),
    ("MAT.COA.PCO", "EPO", "Epoxy Coating", ["epoxy coating", "resin coating"], "Durable coating used for floors, protection, chemical resistance, and high-wear surfaces."),
    ("MAT.COA.PCO", "INT", "Intumescent Coating", ["intumescent paint", "fire-protective coating"], "Fire-protective coating that expands under heat to protect steel or assemblies where specified."),
    ("MAT.INS.TIN", "MIN", "Mineral Wool Insulation", ["mineral wool", "rock wool"], "Fibrous insulation used for thermal, acoustic, and fire-resistant assemblies."),
    ("MAT.INS.TIN", "FIG", "Fiberglass Insulation", ["fiberglass insulation", "glass fiber insulation"], "Fibrous thermal and acoustic insulation used in walls, roofs, ceilings, and ducts."),
    ("MAT.INS.TIN", "FOA", "Foam Insulation", ["foam insulation", "rigid foam"], "Cellular insulation used for envelope thermal resistance and moisture-aware detailing."),
]
for item in glass_membrane_insulation_nodes:
    _add_node(item[0], item[1], item[2], item[3], item[4], "material_envelope_detail", "materials_taxonomy")

property_nodes = [
    ("MAT.PRF.MEC", "CPS", "Compressive Strength", ["compressive strength", "compression capacity"], "Mechanical property describing a material's resistance to compressive stress."),
    ("MAT.PRF.MEC", "TEN", "Tensile Behavior", ["tensile behavior", "tension behavior"], "Mechanical behavior describing how a material responds to pulling forces and tensile stress."),
    ("MAT.PRF.MEC", "STF", "Stiffness", ["stiffness", "elastic modulus"], "Material resistance to deformation, affecting spans, deflection, vibration, and perceptual solidity."),
    ("MAT.PRF.FIR", "FIR", "Fire Resistance", ["fire resistance", "fire-resistive performance"], "Material or assembly capacity to contribute to fire-resistance goals under specified conditions."),
    ("MAT.PRF.FIR", "SMD", "Smoke Development", ["smoke development", "smoke contribution"], "Fire-behavior concern for materials that may affect smoke generation and evacuation conditions."),
    ("MAT.PRF.MOI", "MRS", "Moisture Resistance", ["moisture resistance", "water resistance"], "Material ability to resist moisture, water, humidity, swelling, decay, corrosion, or delamination."),
    ("MAT.PRF.MOI", "DUR", "Durability", ["durability", "service life"], "Material ability to maintain performance over time under exposure, use, maintenance, and weathering."),
    ("MAT.PRF.MOI", "WTH", "Weathering", ["weathering", "patina", "exposure aging"], "Material surface and performance change caused by weather, sunlight, rain, humidity, pollution, or maintenance."),
    ("MAT.PRF.ACO", "ABS", "Acoustic Absorption", ["sound absorption", "acoustic absorption"], "Ability of material or assembly surfaces to absorb sound energy and reduce reverberation."),
    ("MAT.PRF.ACO", "ISO", "Sound Isolation", ["sound isolation", "sound transmission control"], "Ability of assemblies to reduce sound transmission between spaces or from exterior sources."),
    ("MAT.PRF.THE", "THM", "Thermal Mass", ["thermal mass", "heat storage"], "Capacity of material to store and release heat, useful in passive thermal design when climate-appropriate."),
    ("MAT.PRF.THE", "REF", "Solar Reflectance", ["reflectance", "solar reflectance"], "Optical property affecting glare, daylight distribution, heat gain, and heat-island considerations."),
    ("MAT.PRF.ENV", "EBC", "Embodied Carbon", ["embodied carbon", "upfront carbon"], "Lifecycle impact metric for greenhouse-gas emissions associated with material extraction, production, transport, and construction."),
    ("MAT.PRF.ENV", "REC", "Recyclability", ["recyclability", "recycled content potential"], "Potential for material recovery, reuse, recycling, or circular lifecycle strategies."),
    ("MAT.PRF.ENV", "LOC", "Local Material Availability", ["local availability", "local material sourcing"], "Availability of materials in local markets, affecting cost, constructability, resilience, and cultural fit."),
    ("MAT.PRF.AES", "TEX", "Texture", ["texture", "surface texture"], "Surface quality perceived visually or by touch, affecting materiality, craft, slip, and atmosphere."),
    ("MAT.PRF.AES", "COL", "Color", ["color", "material color"], "Visible material quality affecting perception, wayfinding, heat gain, and interior atmosphere."),
    ("MAT.PRF.AES", "SLP", "Slip Resistance", ["slip resistance", "anti-slip finish"], "Walking-surface property relevant to wet areas, accessibility, public safety, and finish specification."),
]
for item in property_nodes:
    _add_node(item[0], item[1], item[2], item[3], item[4], "material_property", "materials_taxonomy")

roles = [
    ("FIG.PTE.ROL", "ARC", "Architect Role", ["architect", "architectural designer"], "Person or firm role responsible for architectural design, spatial coordination, building form, documentation, and design intent."),
    ("FIG.PTE.ROL", "SEN", "Structural Engineer Role", ["structural engineer", "structural designer"], "Engineering role responsible for structural systems, stability, load paths, and structural coordination."),
    ("FIG.PTE.ROL", "CEN", "Civil Engineer Role", ["civil engineer", "infrastructure engineer"], "Engineering role responsible for civil works, bridges, site infrastructure, and public works coordination."),
    ("FIG.PTE.ROL", "AEN", "Architect Engineer Role", ["architect-engineer", "architect and engineer"], "Bridge role for people whose work connects architectural design and engineering reasoning."),
    ("FIG.PTE.ROL", "THE", "Theorist Role", ["architectural theorist", "writer"], "Role associated with architectural theory, writing, pedagogy, or intellectual influence."),
    ("FIG.PTE.ROL", "EDU", "Educator Role", ["educator", "teacher"], "Role associated with teaching, mentoring, and academic influence in architecture or engineering."),
    ("FIG.PTE.ROL", "BLD", "Builder Role", ["builder", "master builder"], "Role associated with construction, fabrication, craft, and built execution."),
    ("FIG.PTE.ROL", "PLN", "Planner Role", ["planner", "urban designer"], "Role associated with planning, urban design, land use, and settlement-scale work."),
    ("FIG.PTE.ROL", "LAU", "Pritzker Laureate Status", ["Pritzker laureate", "Pritzker Architecture Prize laureate"], "Award-status facet for architects recognized by the Pritzker Architecture Prize."),
]
for item in roles:
    _add_node(item[0], item[1], item[2], item[3], item[4], "people_role", "people_works_materials", PEOPLE_SOURCE_IDS)
_add_node("FIG.AWD.PRI", "PZK", "Pritzker Architecture Prize", ["Pritzker Prize", "Pritzker Architecture Prize laureates"], "Annual international architecture prize used as a metadata-only award-status facet for laureate graph navigation.", "architecture_award", "people_works_materials", ["SRC-PRITZKER-LAUREATES-OFFICIAL"])

nationality_nodes = [
    ("USA", "United States Architect Nationality", ["American architects", "United States architects", "US architects"], "Metadata-only nationality facet for architects and engineer-designers with United States association."),
    ("GBR", "British Architect Nationality", ["British architects", "United Kingdom architects", "UK architects"], "Metadata-only nationality facet for architects and engineer-designers with British or United Kingdom association."),
    ("JPN", "Japanese Architect Nationality", ["Japanese architects", "Japan architects"], "Metadata-only nationality facet for architects with Japanese association."),
    ("FRA", "French Architect Nationality", ["French architects", "France architects"], "Metadata-only nationality facet for architects with French association."),
    ("ITA", "Italian Architect Nationality", ["Italian architects", "Italy architects"], "Metadata-only nationality facet for architects and engineer-designers with Italian association."),
    ("DEU", "German Architect Nationality", ["German architects", "Germany architects"], "Metadata-only nationality facet for architects and designers with German association."),
    ("IND", "Indian Architect Nationality", ["Indian architects", "India architects"], "Metadata-only nationality facet for architects with Indian association."),
    ("PRT", "Portuguese Architect Nationality", ["Portuguese architects", "Portugal architects"], "Metadata-only nationality facet for architects with Portuguese association."),
    ("BRA", "Brazilian Architect Nationality", ["Brazilian architects", "Brazil architects"], "Metadata-only nationality facet for architects with Brazilian association."),
    ("MEX", "Mexican Architect Nationality", ["Mexican architects", "Mexico architects"], "Metadata-only nationality facet for architect-engineers with Mexican association."),
    ("ESP", "Spanish Architect Nationality", ["Spanish architects", "Spain architects"], "Metadata-only nationality facet for architects and architect-engineers with Spanish association."),
    ("FIN", "Finnish Architect Nationality", ["Finnish architects", "Finland architects"], "Metadata-only nationality facet for architects with Finnish association."),
    ("NLD", "Dutch Architect Nationality", ["Dutch architects", "Netherlands architects"], "Metadata-only nationality facet for architects with Dutch association."),
    ("CHN", "Chinese Architect Nationality", ["Chinese architects", "China architects"], "Metadata-only nationality facet for architects with Chinese association."),
    ("BFA", "Burkinabe Architect Nationality", ["Burkinabe architects", "Burkina Faso architects"], "Metadata-only nationality facet for architects with Burkina Faso association."),
    ("IRL", "Irish Architect Nationality", ["Irish architects", "Ireland architects"], "Metadata-only nationality facet for architects with Irish association."),
    ("CHL", "Chilean Architect Nationality", ["Chilean architects", "Chile architects"], "Metadata-only nationality facet for architects with Chilean association."),
    ("CAN", "Canadian Architect Nationality", ["Canadian architects", "Canada architects"], "Metadata-only nationality facet for architects with Canadian association."),
    ("CHE", "Swiss Architect Nationality", ["Swiss architects", "Switzerland architects"], "Metadata-only nationality facet for architects and engineers with Swiss association."),
    ("AUT", "Austrian Architect Nationality", ["Austrian architects", "Austria architects"], "Metadata-only nationality facet for engineers and designers with Austrian association."),
    ("AUS", "Australian Architect Nationality", ["Australian architects", "Australia architects"], "Metadata-only nationality facet for architects and designers with Australian association."),
    ("DNK", "Danish Architect Nationality", ["Danish architects", "Denmark architects"], "Metadata-only nationality facet for architects with Danish association."),
    ("PHL", "Philippine Architect Nationality", ["Filipino architects", "Philippine architects"], "Metadata-only nationality facet for Philippine architects and works."),
    ("URY", "Uruguayan Architect Nationality", ["Uruguayan architects", "Uruguay architects"], "Metadata-only nationality facet for engineer-architects with Uruguay association."),
]
_add_node("FIG.PTE", "NAT", "Architect Nationality Facets", ["architect nationality", "architect country facets", "people by nationality"], "Metadata-only country and nationality facets for organizing canonical architects and architect-engineers without duplicating person nodes.", "people_nationality_facet_root", "people_nationality", PEOPLE_SOURCE_IDS)
for suffix, label, aliases, definition in nationality_nodes:
    _add_node("FIG.PTE.NAT", suffix, label, aliases, definition, "people_nationality_facet", "people_nationality", PEOPLE_SOURCE_IDS)

law_jurisdiction_nodes = [
    ("INT", "International Standards And Guidance", ["international standards", "global standards", "international guidance"], "Metadata-only scope facet for international standards and guidance families."),
    ("PHL", "Philippine Laws Codes And Local Standards", ["Philippine laws", "Philippine codes", "local Philippine standards"], "Metadata-only jurisdiction facet for Philippine national laws, codes, and local government standards."),
    ("USA", "United States Standards And Practice Families", ["United States standards", "US standards", "AIA standards", "ICC codes"], "Metadata-only jurisdiction facet for United States standards, model codes, and practice document families."),
    ("GBR", "United Kingdom Standards And Practice Families", ["UK standards", "British standards", "RIBA standards"], "Metadata-only jurisdiction facet for United Kingdom standards and practice document families."),
    ("LOC", "Local Government Standards And Ordinances", ["local standards", "local ordinances", "local code adoption"], "Metadata-only scope facet for local standards, ordinances, and authority adoption contexts."),
]
_add_node("LAW", "JUR", "Law And Standard Jurisdiction Facets", ["jurisdiction facets", "law country facets", "standard scope facets"], "Metadata-only jurisdiction and scope facets for laws, standards, local ordinances, and international guidance without forking the canonical backbone.", "law_jurisdiction_facet_root", "laws_standards_classification", STANDARDS_CLASSIFICATION_SOURCE_IDS)
for suffix, label, aliases, definition in law_jurisdiction_nodes:
    _add_node("LAW.JUR", suffix, label, aliases, definition, "law_jurisdiction_facet", "laws_standards_classification", STANDARDS_CLASSIFICATION_SOURCE_IDS)

standards_family_nodes = [
    ("AIA", "AIA Practice And Contract Standards Family", ["AIA", "American Institute of Architects", "AIA contract documents"], "Metadata-only classification node for AIA practice and contract-document families; no contract text or guide payload is stored.", ["SRC-AIA-CONTRACTS-PRACTICE-METADATA"]),
    ("RIB", "RIBA Practice And Work Stage Standards Family", ["RIBA", "Royal Institute of British Architects", "RIBA Plan of Work"], "Metadata-only classification node for RIBA practice and work-stage families; no guide text, table, or diagram payload is stored.", ["SRC-RIBA-PLAN-OF-WORK-METADATA"]),
    ("IBS", "IBS NIBS Building Standards Family", ["IBS", "NIBS", "National Institute of Building Sciences", "building sciences standards"], "Metadata-only classification node for NIBS and building-sciences standards families, including OmniClass, NBIMS, and WBDG references where rights-safe.", ["SRC-NIBS-NBIMS-OMNICLASS", "SRC-NIBS-WBDG-COMMISSIONING"]),
]
for suffix, label, aliases, definition, sources in standards_family_nodes:
    _add_node("COM.STD", suffix, label, aliases, definition, "standards_family_classification", "laws_standards_classification", sources)

# path, label, aliases, award_year, source_ids
PRITZKER_ARCHITECTS: list[tuple[str, str, list[str], int, list[str]]] = [
    ("RAD", "Smiljan Radic Clarke", ["Smiljan Radić Clarke", "Smiljan Radic"], 2026, PEOPLE_SOURCE_IDS),
    ("LIU", "Liu Jiakun", ["Jiakun Liu"], 2025, PEOPLE_SOURCE_IDS),
    ("YAM", "Riken Yamamoto", ["Yamamoto Riken"], 2024, PEOPLE_SOURCE_IDS),
    ("CHP", "David Chipperfield", ["Sir David Chipperfield"], 2023, PEOPLE_SOURCE_IDS),
    ("KER", "Francis Kere", ["Diébédo Francis Kéré", "Francis Kéré"], 2022, PEOPLE_SOURCE_IDS),
    ("LAC", "Anne Lacaton", ["Lacaton"], 2021, PEOPLE_SOURCE_IDS),
    ("VAS", "Jean Philippe Vassal", ["Jean-Philippe Vassal", "Vassal"], 2021, PEOPLE_SOURCE_IDS),
    ("FAR", "Yvonne Farrell", ["Grafton Architects", "Farrell"], 2020, PEOPLE_SOURCE_IDS),
    ("MCN", "Shelley McNamara", ["Grafton Architects", "McNamara"], 2020, PEOPLE_SOURCE_IDS),
    ("ISO", "Arata Isozaki", ["Isozaki Arata"], 2019, PEOPLE_SOURCE_IDS),
    ("DOS", "Balkrishna Doshi", ["B. V. Doshi", "BV Doshi"], 2018, PEOPLE_SOURCE_IDS),
    ("ARA", "Alejandro Aravena", ["Aravena", "Elemental"], 2016, PEOPLE_SOURCE_IDS),
    ("FOT", "Frei Otto", ["Frei Paul Otto"], 2015, PEOPLE_SOURCE_IDS),
    ("BAN", "Shigeru Ban", ["Ban Shigeru"], 2014, PEOPLE_SOURCE_IDS),
    ("ITO", "Toyo Ito", ["Ito Toyo"], 2013, PEOPLE_SOURCE_IDS),
    ("SEJ", "Kazuyo Sejima", ["SANAA", "Sejima Kazuyo"], 2010, PEOPLE_SOURCE_IDS),
    ("NIZ", "Ryue Nishizawa", ["SANAA", "Nishizawa Ryue"], 2010, PEOPLE_SOURCE_IDS),
    ("WSH", "Wang Shu", ["Wang Shu", "Amateur Architecture Studio"], 2012, PEOPLE_SOURCE_IDS),
    ("SOU", "Eduardo Souto De Moura", ["Eduardo Souto de Moura"], 2011, PEOPLE_SOURCE_IDS),
    ("ZUM", "Peter Zumthor", ["Zumthor"], 2009, PEOPLE_SOURCE_IDS),
    ("NOU", "Jean Nouvel", ["Nouvel"], 2008, PEOPLE_SOURCE_IDS),
    ("RGR", "Richard Rogers", ["Lord Rogers", "Richard George Rogers"], 2007, PEOPLE_SOURCE_IDS),
    ("PMR", "Paulo Mendes Da Rocha", ["Paulo Mendes da Rocha"], 2006, PEOPLE_SOURCE_IDS),
    ("THM", "Thom Mayne", ["Morphosis", "Thomas Mayne"], 2005, PEOPLE_SOURCE_IDS),
    ("KOO", "Rem Koolhaas", ["Koolhaas", "OMA"], 2000, PEOPLE_SOURCE_IDS),
    ("HAD", "Zaha Hadid", ["Dame Zaha Hadid"], 2004, PEOPLE_SOURCE_IDS),
    ("UTZ", "Jorn Utzon", ["Jørn Utzon", "Joern Utzon"], 2003, PEOPLE_SOURCE_IDS),
    ("MUR", "Glenn Murcutt", ["Glenn Marcus Murcutt"], 2002, PEOPLE_SOURCE_IDS),
    ("HER", "Jacques Herzog", ["Herzog & de Meuron", "Jacques Herzog"], 2001, PEOPLE_SOURCE_IDS),
    ("MEU", "Pierre De Meuron", ["Pierre de Meuron", "Herzog & de Meuron"], 2001, PEOPLE_SOURCE_IDS),
    ("FOS", "Norman Foster", ["Lord Foster", "Foster + Partners"], 1999, PEOPLE_SOURCE_IDS),
    ("PIA", "Renzo Piano", ["Renzo Piano Building Workshop"], 1998, PEOPLE_SOURCE_IDS),
    ("MON", "Rafael Moneo", ["José Rafael Moneo Vallés", "Rafael Moneo"], 1996, PEOPLE_SOURCE_IDS),
    ("AND", "Tadao Ando", ["Ando Tadao"], 1995, PEOPLE_SOURCE_IDS),
    ("SIZ", "Alvaro Siza", ["Álvaro Siza", "Alvaro Joaquim de Melo Siza Vieira"], 1992, PEOPLE_SOURCE_IDS),
    ("GEH", "Frank Gehry", ["Frank O. Gehry", "Gehry"], 1989, PEOPLE_SOURCE_IDS),
    ("NIE", "Oscar Niemeyer", ["Oscar Ribeiro de Almeida Niemeyer Soares Filho"], 1988, PEOPLE_SOURCE_IDS),
    ("PEI", "I M Pei", ["I. M. Pei", "Ieoh Ming Pei"], 1983, PEOPLE_SOURCE_IDS),
    ("BAR", "Luis Barragan", ["Luis Barragán"], 1980, PEOPLE_SOURCE_IDS),
    ("PJO", "Philip Johnson", ["Philip Cortelyou Johnson"], 1979, PEOPLE_SOURCE_IDS),
]
for suffix, label, aliases, year, sources in PRITZKER_ARCHITECTS:
    _add_node("FIG.ARD.CAA", suffix, label, [*aliases, "architect", "Pritzker laureate", f"Pritzker {year}"], f"Metadata-only person node for {label}, modeled for architecture history, award status, works, movement, material, and structural-system navigation.", "architect_person", "people_works_materials", sources)

OTHER_ARCHITECTS = [
    ("KAH", "Louis Kahn", ["Louis I. Kahn", "Kahn"], ["SRC-WIKIDATA-CC0-AEC-IDENTIFIERS", "SRC-VIAF-AUTHORITY-DATA"]),
    ("LCO", "Le Corbusier", ["Charles-Edouard Jeanneret", "Le Corbusier"], ["SRC-WIKIDATA-CC0-AEC-IDENTIFIERS", "SRC-VIAF-AUTHORITY-DATA"]),
    ("AAL", "Alvar Aalto", ["Hugo Alvar Henrik Aalto"], ["SRC-WIKIDATA-CC0-AEC-IDENTIFIERS", "SRC-VIAF-AUTHORITY-DATA"]),
    ("MIE", "Mies Van Der Rohe", ["Ludwig Mies van der Rohe", "Mies"], ["SRC-WIKIDATA-CC0-AEC-IDENTIFIERS", "SRC-VIAF-AUTHORITY-DATA"]),
    ("GRO", "Walter Gropius", ["Gropius", "Bauhaus"], ["SRC-WIKIDATA-CC0-AEC-IDENTIFIERS", "SRC-VIAF-AUTHORITY-DATA"]),
]
for suffix, label, aliases, sources in OTHER_ARCHITECTS:
    _add_node("FIG.ARD.CAA", suffix, label, [*aliases, "architect"], f"Metadata-only person node for {label}, used as an architecture history, theory, movement, and work relationship anchor.", "architect_person", "people_works_materials", sources)

ENGINEERS = [
    ("CAL", "Santiago Calatrava", ["Calatrava", "architect engineer", "bridge designer"], "architect_engineer"),
    ("ARU", "Ove Arup", ["Sir Ove Arup", "Arup"], "structural_engineer"),
    ("KHN", "Fazlur Rahman Khan", ["Fazlur Khan", "F. R. Khan", "tubular high-rise systems"], "structural_engineer"),
    ("NRV", "Pier Luigi Nervi", ["Nervi", "reinforced concrete shells"], "engineer_architect"),
    ("MAI", "Robert Maillart", ["Maillart", "concrete bridge engineer"], "civil_engineer"),
    ("EIF", "Gustave Eiffel", ["Eiffel", "tower engineer"], "civil_engineer"),
    ("CAN", "Felix Candela", ["Félix Candela", "thin shell concrete"], "engineer_architect"),
    ("TOR", "Eduardo Torroja", ["Torroja", "thin shell structures"], "structural_engineer"),
    ("RIC", "Peter Rice", ["Rice", "structural designer"], "structural_engineer"),
    ("DIE", "Eladio Dieste", ["Dieste", "reinforced brick"], "engineer_architect"),
    ("BRU", "Isambard Kingdom Brunel", ["Brunel", "bridge engineer"], "civil_engineer"),
    ("FUL", "Buckminster Fuller", ["R. Buckminster Fuller", "geodesic dome"], "designer_engineer"),
    ("FRE", "Eugene Freyssinet", ["Eugène Freyssinet", "prestressed concrete"], "structural_engineer"),
    ("MEN", "Christian Menn", ["Menn", "bridge engineer"], "civil_engineer"),
    ("ISL", "Heinz Isler", ["Isler", "shell structures"], "structural_engineer"),
    ("SCH", "Jorg Schlaich", ["Jörg Schlaich", "Schlaich"], "structural_engineer"),
    ("BAL", "Cecil Balmond", ["Balmond", "structural designer"], "structural_engineer"),
    ("ROB", "Leslie Robertson", ["Robertson", "high-rise structural engineer"], "structural_engineer"),
    ("BAK", "William F Baker", ["Bill Baker", "William Baker", "Burj Khalifa structural engineer"], "structural_engineer"),
    ("WER", "Jane Wernick", ["Wernick", "structural engineer"], "structural_engineer"),
    ("ROE", "John A Roebling", ["John Roebling", "suspension bridge engineer"], "civil_engineer"),
    ("STR", "Joseph Strauss", ["Golden Gate Bridge engineer", "Strauss"], "civil_engineer"),
    ("VIR", "Michel Virlogeux", ["Virlogeux", "bridge engineer"], "civil_engineer"),
    ("TED", "Anton Tedesko", ["Tedesko", "thin shell concrete"], "structural_engineer"),
    ("ARR", "Eduardo Arriola", ["bridge engineer", "structural engineer"], "structural_engineer"),
]
for suffix, label, aliases, kind in ENGINEERS:
    _add_node("FIG.ETS.STE", suffix, label, [*aliases, "engineer", "structural engineering"], f"Metadata-only person node for {label}, used to connect architecture, engineering roles, works, structural systems, and material reasoning.", kind, "people_works_materials", PEOPLE_SOURCE_IDS)

PRITZKER_ARCHITECT_NATIONALITIES = {
    "RAD": "CHL", "LIU": "CHN", "YAM": "JPN", "CHP": "GBR", "KER": "BFA",
    "LAC": "FRA", "VAS": "FRA", "FAR": "IRL", "MCN": "IRL", "ISO": "JPN",
    "DOS": "IND", "ARA": "CHL", "FOT": "DEU", "BAN": "JPN", "ITO": "JPN",
    "SEJ": "JPN", "NIZ": "JPN", "WSH": "CHN", "SOU": "PRT", "ZUM": "CHE",
    "NOU": "FRA", "RGR": "GBR", "PMR": "BRA", "THM": "USA", "KOO": "NLD",
    "HAD": "GBR", "UTZ": "DNK", "MUR": "AUS", "HER": "CHE", "MEU": "CHE",
    "FOS": "GBR", "PIA": "ITA", "MON": "ESP", "AND": "JPN", "SIZ": "PRT",
    "GEH": "CAN", "NIE": "BRA", "PEI": "USA", "BAR": "MEX", "PJO": "USA",
}
OTHER_ARCHITECT_NATIONALITIES = {
    "KAH": "USA", "LCO": "FRA", "AAL": "FIN", "MIE": "DEU", "GRO": "DEU",
}
ENGINEER_ARCHITECT_NATIONALITIES = {
    "CAL": "ESP", "ARU": "GBR", "KHN": "USA", "NRV": "ITA", "MAI": "CHE",
    "EIF": "FRA", "CAN": "MEX", "TOR": "ESP", "RIC": "IRL", "DIE": "URY",
    "BRU": "GBR", "FUL": "USA", "FRE": "FRA", "MEN": "CHE", "ISL": "CHE",
    "SCH": "DEU", "BAL": "GBR", "ROB": "USA", "BAK": "USA", "WER": "GBR",
    "ROE": "USA", "STR": "USA", "VIR": "FRA", "TED": "USA", "ARR": "PHL",
}

WORKS = [
    ("SRP", "Serpentine Pavilion 2014", ["Smiljan Radic Serpentine Pavilion"], "temporary pavilion", "RAD"),
    ("WVJ", "West Village Chengdu", ["Liu Jiakun West Village"], "urban mixed-use work", "LIU"),
    ("YHG", "Yokosuka Museum Of Art", ["Riken Yamamoto Yokosuka Museum"], "museum", "YAM"),
    ("RIV", "River And Rowing Museum", ["David Chipperfield River and Rowing Museum"], "museum", "CHP"),
    ("GAN", "Gando Primary School", ["Francis Kere Gando Primary School"], "school", "KER"),
    ("FRA", "FRAC Nord Pas De Calais", ["Lacaton Vassal FRAC"], "adaptive reuse cultural work", "LAC"),
    ("UBD", "Universita Bocconi Building", ["Grafton Bocconi"], "university building", "FAR"),
    ("MOA", "Museum Of Contemporary Art Los Angeles", ["Arata Isozaki MOCA"], "museum", "ISO"),
    ("IMA", "Indian Institute Of Management Bangalore", ["Balkrishna Doshi IIM Bangalore"], "campus", "DOS"),
    ("QMO", "Quinta Monroy Housing", ["Alejandro Aravena Quinta Monroy"], "incremental housing", "ARA"),
    ("MOS", "Munich Olympic Stadium Roof", ["Frei Otto Munich Olympic roof"], "stadium roof", "FOT"),
    ("PCH", "Paper Church Kobe", ["Shigeru Ban Paper Church"], "temporary church", "BAN"),
    ("SEN", "Sendai Mediatheque", ["Toyo Ito Sendai Mediatheque"], "library media center", "ITO"),
    ("NMC", "New Museum New York", ["SANAA New Museum"], "museum", "SEJ"),
    ("KTH", "Kolumba Museum", ["Peter Zumthor Kolumba"], "museum", "ZUM"),
    ("AGB", "Arab World Institute", ["Jean Nouvel Institut du Monde Arabe"], "cultural institute", "NOU"),
    ("LOY", "Lloyds Building", ["Richard Rogers Lloyd's Building"], "office building", "RGR"),
    ("SCL", "Seattle Central Library", ["Rem Koolhaas Seattle Library", "OMA Seattle Library"], "library", "KOO"),
    ("HKB", "HSBC Main Building Hong Kong", ["Norman Foster HSBC Hong Kong"], "office tower", "FOS"),
    ("POM", "Centre Pompidou", ["Pompidou Centre", "Renzo Piano Richard Rogers Pompidou"], "cultural center", "PIA"),
    ("CHL", "Church Of The Light", ["Tadao Ando Church of the Light"], "church", "AND"),
    ("GUG", "Guggenheim Museum Bilbao", ["Frank Gehry Bilbao Guggenheim"], "museum", "GEH"),
    ("VFS", "Vitra Fire Station", ["Zaha Hadid Vitra Fire Station"], "fire station", "HAD"),
    ("MAX", "MAXXI Museum", ["Zaha Hadid MAXXI"], "museum", "HAD"),
    ("HAC", "Heydar Aliyev Center", ["Zaha Hadid Heydar Aliyev Centre"], "cultural center", "HAD"),
    ("SAL", "Salk Institute", ["Louis Kahn Salk Institute"], "research campus", "KAH"),
    ("KIM", "Kimbell Art Museum", ["Louis Kahn Kimbell"], "museum", "KAH"),
    ("VSA", "Villa Savoye", ["Le Corbusier Villa Savoye"], "house", "LCO"),
    ("UNI", "Unite d Habitation Marseille", ["Unité d'Habitation", "Le Corbusier Unite"], "housing", "LCO"),
    ("MAI", "Maison Louis Carre", ["Alvar Aalto Maison Louis Carré"], "house", "AAL"),
    ("FAR", "Farnsworth House", ["Mies Farnsworth House"], "house", "MIE"),
    ("BAU", "Bauhaus Dessau Building", ["Walter Gropius Bauhaus Dessau"], "school building", "GRO"),
    ("ALB", "Alamillo Bridge", ["Santiago Calatrava Alamillo Bridge"], "bridge", "CAL"),
    ("MAM", "Milwaukee Art Museum Quadracci Pavilion", ["Calatrava Milwaukee Art Museum"], "museum pavilion", "CAL"),
    ("JHC", "John Hancock Center", ["875 North Michigan Avenue", "Fazlur Khan John Hancock"], "high-rise", "KHN"),
    ("WIT", "Willis Tower", ["Sears Tower", "Fazlur Khan Willis Tower"], "high-rise", "KHN"),
    ("PDS", "Palazzetto Dello Sport", ["Nervi Palazzetto dello Sport"], "arena", "NRV"),
    ("SAB", "Salginatobel Bridge", ["Robert Maillart Salginatobel"], "bridge", "MAI"),
    ("EFT", "Eiffel Tower", ["Gustave Eiffel Tower"], "tower", "EIF"),
    ("LMA", "Los Manantiales Restaurant", ["Felix Candela Los Manantiales"], "restaurant shell", "CAN"),
    ("ZAR", "Zarzuela Hippodrome", ["Eduardo Torroja Zarzuela"], "sports venue", "TOR"),
    ("CCO", "Church Of Christ The Worker Atlantida", ["Eladio Dieste Cristo Obrero"], "church", "DIE"),
    ("CSB", "Clifton Suspension Bridge", ["Brunel Clifton Suspension Bridge"], "bridge", "BRU"),
    ("BIO", "Montreal Biosphere", ["Buckminster Fuller geodesic dome"], "geodesic dome", "FUL"),
    ("CCP", "Cultural Center Of The Philippines Complex", ["CCP Complex", "Leandro Locsin CCP"], "Philippine cultural complex", "LOC"),
]
for suffix, label, aliases, typology, owner_suffix in WORKS:
    _add_node("FIG.WRK.BUI", suffix, label, [*aliases, typology, "work anchor"], f"Metadata-only work/project node for {label}, used as an anchor between people, building types, movements, materials, structural systems, and design concepts.", "work_project_anchor", "people_works_materials", PEOPLE_SOURCE_IDS if owner_suffix != "LOC" else NCCA_SOURCE_IDS)

PROJECT_EVIDENCE_NODES = [
    ("FIG.WRK.BUI", "RON", "Notre Dame Du Haut Ronchamp", ["Ronchamp chapel", "Chapelle Notre-Dame du Haut"], "Metadata-only work/project node for a Le Corbusier chapel used to anchor reinforced-concrete, light, sculptural-form, and modern sacred-architecture paths.", "work_project_anchor", "project_evidence_paths", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.WRK.BUI", "LAT", "Sainte Marie De La Tourette", ["La Tourette", "Couvent de La Tourette"], "Metadata-only work/project node for a Le Corbusier monastery used to anchor béton brut, brise-soleil, modular, and Brutalist-modernism study paths.", "work_project_anchor", "project_evidence_paths", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.WRK.BUI", "NAD", "National Assembly Building Dhaka", ["Jatiya Sangsad Bhaban", "National Assembly Dhaka"], "Metadata-only work/project node for a Louis Kahn civic complex used to anchor geometric order, daylight, concrete, and monumental spatial-composition paths.", "work_project_anchor", "project_evidence_paths", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.WRK.BUI", "EXE", "Exeter Library", ["Phillips Exeter Academy Library", "Kahn Exeter Library"], "Metadata-only work/project node for a Louis Kahn library used to anchor brick, concrete, central void, and institutional reading-room paths.", "work_project_anchor", "project_evidence_paths", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.WRK.BUI", "PAI", "Paimio Sanatorium", ["Alvar Aalto Paimio Sanatorium"], "Metadata-only work/project node for an Alvar Aalto health building used to anchor humane modernism, daylight, ventilation, color, and furniture/interior paths.", "work_project_anchor", "project_evidence_paths", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.WRK.BUI", "SAY", "Saynatsalo Town Hall", ["Säynätsalo Town Hall", "Alvar Aalto Saynatsalo"], "Metadata-only work/project node for an Alvar Aalto civic building used to anchor brick, timber, courtyard, civic modernism, and material warmth paths.", "work_project_anchor", "project_evidence_paths", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.WRK.BUI", "BCP", "Barcelona Pavilion", ["German Pavilion Barcelona", "Mies Barcelona Pavilion"], "Metadata-only work/project node for Mies van der Rohe's pavilion used to anchor steel, glass, stone, minimalism, and planar spatial-order paths.", "work_project_anchor", "project_evidence_paths", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.WRK.BUI", "SEA", "Seagram Building", ["Mies Seagram Building"], "Metadata-only work/project node for a Mies high-rise used to anchor curtain-wall logic, steel frame expression, International Style, and office tower paths.", "work_project_anchor", "project_evidence_paths", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.WRK.BUI", "SYD", "Sydney Opera House", ["Utzon Sydney Opera House"], "Metadata-only work/project node for Jørn Utzon and Ove Arup collaboration paths linking shell structures, roof geometry, ceramics, and architectural-engineering coordination.", "work_project_anchor", "project_evidence_paths", PROJECT_EVIDENCE_SOURCE_IDS + ENGINEERING_WORK_SOURCE_IDS),
    ("FIG.WRK.BUI", "TAT", "Tate Modern", ["Herzog de Meuron Tate Modern"], "Metadata-only work/project node for Herzog & de Meuron adaptive reuse paths connecting industrial heritage, brick, contemporary museum design, and conversion work.", "work_project_anchor", "project_evidence_paths", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.WRK.BUI", "NBS", "Beijing National Stadium", ["Bird's Nest Stadium", "Herzog de Meuron Beijing Stadium"], "Metadata-only work/project node for stadium paths connecting steel exoskeleton expression, long-span systems, and contemporary civic spectacle.", "work_project_anchor", "project_evidence_paths", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.WRK.BUI", "MAV", "Marika Alderton House", ["Glenn Murcutt Marika-Alderton House"], "Metadata-only work/project node for Glenn Murcutt climate-response paths connecting lightweight construction, shading, ventilation, and regional material logic.", "work_project_anchor", "project_evidence_paths", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.WRK.BUI", "NHB", "Ningbo History Museum", ["Wang Shu Ningbo Museum"], "Metadata-only work/project node for Wang Shu paths connecting recycled masonry, regional memory, material reuse, and cultural continuity.", "work_project_anchor", "project_evidence_paths", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.WRK.BUI", "BMS", "Brazilian Museum Of Sculpture", ["MuBE", "Paulo Mendes da Rocha Brazilian Museum of Sculpture"], "Metadata-only work/project node for Paulo Mendes da Rocha paths connecting concrete, large-span civic space, structural expression, and Brazilian modernism.", "work_project_anchor", "project_evidence_paths", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.WRK.BUI", "BRG", "Braga Municipal Stadium", ["Eduardo Souto de Moura Braga Stadium"], "Metadata-only work/project node for Eduardo Souto de Moura paths connecting concrete, landscape excavation, stadium structure, and site-material integration.", "work_project_anchor", "project_evidence_paths", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.WRK.BUI", "CAL", "Caltrans District Seven Headquarters", ["Caltrans District 7", "Thom Mayne Caltrans"], "Metadata-only work/project node for Thom Mayne and Morphosis paths connecting metal screens, environmental control, civic workplace, and contemporary facade performance.", "work_project_anchor", "project_evidence_paths", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.WRK.BUI", "KRS", "Kursaal Congress Centre", ["Rafael Moneo Kursaal"], "Metadata-only work/project node for Rafael Moneo paths connecting glass volumes, urban waterfront setting, and contemporary cultural-building form.", "work_project_anchor", "project_evidence_paths", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.WRK.BUI", "GHK", "Thirty St Mary Axe", ["30 St Mary Axe", "The Gherkin"], "Metadata-only work/project node for Foster paths connecting diagrid structure, glass facade, high-rise aerodynamics, and office-tower sustainability discussion.", "work_project_anchor", "project_evidence_paths", PROJECT_EVIDENCE_SOURCE_IDS + ENGINEERING_WORK_SOURCE_IDS),
    ("FIG.WRK.BUI", "HAN", "Hearst Tower New York", ["Hearst Tower", "Foster Hearst Tower"], "Metadata-only work/project node for Foster paths connecting diagrid steel framing, glass facade, adaptive high-rise insertion, and structural efficiency.", "work_project_anchor", "project_evidence_paths", PROJECT_EVIDENCE_SOURCE_IDS + ENGINEERING_WORK_SOURCE_IDS),
    ("FIG.WRK.BUI", "MVA", "Millau Viaduct", ["Viaduc de Millau", "Millau bridge"], "Metadata-only work/project node for Virlogeux and Foster paths connecting cable-stayed bridge design, steel deck, pylons, and long-span structural expression.", "work_project_anchor", "project_evidence_paths", ENGINEERING_WORK_SOURCE_IDS),
    ("FIG.WRK.BUI", "BMG", "British Museum Great Court Roof", ["Great Court roof", "British Museum Queen Elizabeth II Great Court"], "Metadata-only work/project node for Foster/Balmond paths connecting glass-and-steel roof gridshell logic, daylighting, and courtyard enclosure.", "work_project_anchor", "project_evidence_paths", PROJECT_EVIDENCE_SOURCE_IDS + ENGINEERING_WORK_SOURCE_IDS),
    ("FIG.WRK.BUI", "BRJ", "Burj Khalifa", ["Burj Dubai", "Burj Khalifa tower"], "Metadata-only work/project node for William F Baker paths connecting buttressed-core high-rise systems, wind response, concrete/steel coordination, and tall-building design.", "work_project_anchor", "project_evidence_paths", ENGINEERING_WORK_SOURCE_IDS),
    ("FIG.WRK.BUI", "BRB", "Brooklyn Bridge", ["Roebling Brooklyn Bridge"], "Metadata-only work/project node for Roebling paths connecting suspension bridges, steel cables, masonry towers, and civil-engineering heritage.", "work_project_anchor", "project_evidence_paths", ENGINEERING_WORK_SOURCE_IDS),
    ("FIG.WRK.BUI", "GGB", "Golden Gate Bridge", ["Golden Gate suspension bridge"], "Metadata-only work/project node for Strauss/bridge-engineering paths connecting suspension systems, steel cables, towers, and structural expression.", "work_project_anchor", "project_evidence_paths", ENGINEERING_WORK_SOURCE_IDS),
    ("FIG.WRK.BUI", "THV", "Therme Vals", ["Peter Zumthor Therme Vals"], "Metadata-only work/project node for Peter Zumthor paths connecting stone, atmosphere, phenomenology, tactile materiality, and bathing-space sequence.", "work_project_anchor", "project_evidence_paths", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.WRK.BUI", "BKF", "Bruder Klaus Field Chapel", ["Peter Zumthor Bruder Klaus Chapel"], "Metadata-only work/project node for Peter Zumthor paths connecting cast concrete, board/formwork memory, light, and material atmosphere.", "work_project_anchor", "project_evidence_paths", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.WRK.BUI", "LAD", "Louvre Abu Dhabi", ["Jean Nouvel Louvre Abu Dhabi"], "Metadata-only work/project node for Jean Nouvel paths connecting dome-filtered daylight, steel structure, climate response, and cultural-building form.", "work_project_anchor", "project_evidence_paths", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.WRK.BUI", "PCT", "Paper Log House Kobe", ["Shigeru Ban Paper Log House", "Paper Log House"], "Metadata-only work/project node for Shigeru Ban paths connecting paper tubes, temporary shelter, disaster response, and material innovation.", "work_project_anchor", "project_evidence_paths", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.WRK.BUI", "LYC", "Lycée Schorge Secondary School", ["Francis Kere Lycée Schorge", "Schorge Secondary School"], "Metadata-only work/project node for Francis Kéré paths connecting local materials, climate-responsive school design, shading, ventilation, and social architecture.", "work_project_anchor", "project_evidence_paths", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.WRK.BUI", "LUY", "Luyeyuan Stone Sculpture Art Museum", ["Liu Jiakun Luyeyuan", "Luyeyuan Museum"], "Metadata-only work/project node for Liu Jiakun paths connecting museum typology, masonry/stone memory, regional craft, and landscape setting.", "work_project_anchor", "project_evidence_paths", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.WRK.BUI", "SIK", "Suzhou Museum Of Imperial Kiln Brick", ["Liu Jiakun Suzhou Kiln Brick Museum", "Imperial Kiln Brick Museum"], "Metadata-only work/project node for Liu Jiakun paths connecting brick, heritage interpretation, craft material history, and museum design.", "work_project_anchor", "project_evidence_paths", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.WRK.BUI", "HAK", "Hotakubo Housing", ["Riken Yamamoto Hotakubo Housing"], "Metadata-only work/project node for Riken Yamamoto paths connecting collective housing, shared thresholds, community planning, and residential urban form.", "work_project_anchor", "project_evidence_paths", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.WRK.BUI", "AQA", "London Aquatics Centre", ["Zaha Hadid London Aquatics Centre"], "Metadata-only work/project node for Zaha Hadid paths connecting long-span roof form, fluid geometry, concrete/steel coordination, and public sports architecture.", "work_project_anchor", "project_evidence_paths", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.WRK.BUI", "DDP", "Dongdaemun Design Plaza", ["Zaha Hadid DDP", "Dongdaemun Design Plaza and Park"], "Metadata-only work/project node for Zaha Hadid paths connecting aluminum cladding, parametric form, urban cultural infrastructure, and contemporary surface systems.", "work_project_anchor", "project_evidence_paths", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.WRK.BUI", "NEM", "Neues Museum Berlin", ["David Chipperfield Neues Museum"], "Metadata-only work/project node for David Chipperfield paths connecting conservation, brick/stone repair, museum adaptation, and historic fabric continuity.", "work_project_anchor", "project_evidence_paths", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.WRK.BUI", "MNY", "Magney House", ["Glenn Murcutt Magney House", "Murcutt Magney House"], "Metadata-only work/project node for Glenn Murcutt climate reasoning, connecting roof form, metal-sheet envelope logic, passive environmental control, and regional residential design.", "work_project_anchor", "project_evidence_paths", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.WRK.BUI", "RLC", "Rolex Learning Center", ["SANAA Rolex Learning Center"], "Metadata-only work/project node for SANAA paths connecting open-plan learning landscapes, concrete slab continuity, daylight, and gentle topographic section.", "work_project_anchor", "project_evidence_paths", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.WRK.BUI", "TAU", "Tama Art University Library", ["Toyo Ito Tama Art University Library"], "Metadata-only work/project node for Toyo Ito paths connecting concrete arches, open reading space, structural rhythm, and library typology.", "work_project_anchor", "project_evidence_paths", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.WRK.BUI", "FVL", "Fondation Louis Vuitton", ["Frank Gehry Fondation Louis Vuitton"], "Metadata-only work/project node for Frank Gehry paths connecting glass sails, steel framing, museum envelope complexity, and contemporary cultural architecture.", "work_project_anchor", "project_evidence_paths", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.WRK.BUI", "DIS", "Walt Disney Concert Hall", ["Frank Gehry Disney Concert Hall"], "Metadata-only work/project node for Frank Gehry paths connecting metal cladding, concert hall acoustics, structural framing, and sculptural deconstructivist form.", "work_project_anchor", "project_evidence_paths", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.WRK.BUI", "BEY", "Fondation Beyeler", ["Renzo Piano Fondation Beyeler"], "Metadata-only work/project node for Renzo Piano paths connecting daylighting, refined envelope design, museum galleries, and landscape integration.", "work_project_anchor", "project_evidence_paths", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.WRK.BUI", "TJI", "Tjibaou Cultural Centre", ["Renzo Piano Tjibaou Center", "Jean-Marie Tjibaou Cultural Centre"], "Metadata-only work/project node for Renzo Piano paths connecting timber rib forms, cultural interpretation, ventilation, and climate-responsive regional design.", "work_project_anchor", "project_evidence_paths", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.WRK.BUI", "SAC", "Sainsbury Centre For Visual Arts", ["Foster Sainsbury Centre"], "Metadata-only work/project node for Norman Foster paths connecting high-tech enclosure, steel space-frame logic, services integration, and flexible gallery space.", "work_project_anchor", "project_evidence_paths", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.WRK.BUI", "GAR", "Garabit Viaduct", ["Eiffel Garabit Viaduct"], "Metadata-only work/project node for Gustave Eiffel paths connecting metal arch bridge structure, structural expression, and civil-engineering heritage.", "work_project_anchor", "project_evidence_paths", ENGINEERING_WORK_SOURCE_IDS),
    ("FIG.WRK.BUI", "SWB", "Schwandbach Bridge", ["Robert Maillart Schwandbach Bridge"], "Metadata-only work/project node for Robert Maillart paths connecting reinforced concrete bridge design, deck/arch integration, and elegant structural expression.", "work_project_anchor", "project_evidence_paths", ENGINEERING_WORK_SOURCE_IDS),
    ("FIG.WRK.BUI", "ORL", "Orly Airship Hangars", ["Freyssinet Orly hangars"], "Metadata-only work/project node for Eugène Freyssinet paths connecting reinforced concrete shells, prestressing lineage, and long-span industrial construction.", "work_project_anchor", "project_evidence_paths", ENGINEERING_WORK_SOURCE_IDS),
    ("FIG.WRK.BUI", "MHL", "Mannheim Multihalle", ["Frei Otto Mannheim Multihalle"], "Metadata-only work/project node for Frei Otto paths connecting timber gridshells, lightweight structures, form-finding, and long-span roof systems.", "work_project_anchor", "project_evidence_paths", PROJECT_EVIDENCE_SOURCE_IDS + ENGINEERING_WORK_SOURCE_IDS),
    ("FIG.WRK.BUI", "LNE", "London Eye", ["Millennium Wheel", "London Eye wheel"], "Metadata-only work/project node for Jane Wernick and engineering paths connecting steel, cables, tension, circular structure, and public landmark infrastructure.", "work_project_anchor", "project_evidence_paths", ENGINEERING_WORK_SOURCE_IDS),
    ("FIG.WRK.BUI", "CHS", "Church Of The Holy Sacrifice", ["Leandro Locsin Church of the Holy Sacrifice"], "Metadata-only work/project node for Philippine modernism paths connecting thin-shell concrete, sacred space, Locsin, and tropical modern architectural expression.", "work_project_anchor", "project_evidence_paths", NCCA_SOURCE_IDS),
    ("FIG.WRK.BUI", "FEU", "Far Eastern University Buildings", ["Pablo Antonio FEU", "FEU Art Deco campus"], "Metadata-only work/project node for Pablo Antonio paths connecting Philippine Art Deco, educational buildings, concrete, and modern Philippine architecture.", "work_project_anchor", "project_evidence_paths", NCCA_SOURCE_IDS),
    ("MAT.STM.STS", "CBL", "Steel Cable", ["steel cable", "bridge cable", "tension cable"], "Steel tension material used in suspension, cable-stayed, and tensile-structure paths; modeled as a material/system anchor, not a calculation payload.", "material_metal_detail", "materials_taxonomy", ENGINEERING_WORK_SOURCE_IDS),
    ("MAT.TBB.ENW", "PPT", "Paper Tube", ["paper tube", "cardboard tube", "paper-tube structure"], "Engineered paper/cardboard tube material used as a source-safe material-innovation anchor for temporary and humanitarian architecture paths.", "material_timber_bio_detail", "materials_taxonomy", PROJECT_EVIDENCE_SOURCE_IDS),
    ("MAT.GLA", "STG", "Stained Glass", ["stained glass", "colored glass"], "Glass material and craft system associated with Gothic and sacred architecture, daylight modulation, and heritage envelope assemblies.", "material_envelope_detail", "materials_taxonomy", MATERIAL_SOURCE_IDS),
    ("ARC.BLD.STR", "FBU", "Flying Buttress", ["flying buttress", "buttress system"], "Structural system facet for external thrust-resisting masonry elements in Gothic architecture and vault-support reasoning.", "structural_system_detail", "project_evidence_paths", MATERIAL_SOURCE_IDS),
    ("ARC.BLD.STR", "RBV", "Rib Vault", ["rib vault", "Gothic rib vault"], "Structural system facet for ribbed masonry vaulting paths in Gothic architecture and long-span sacred spaces.", "structural_system_detail", "project_evidence_paths", MATERIAL_SOURCE_IDS),
    ("ARC.BLD.STR", "DOM", "Dome Structure", ["dome", "dome structure"], "Structural system facet for domes, shells, and central-plan architecture paths from Roman/Byzantine precedents to contemporary roof systems.", "structural_system_detail", "project_evidence_paths", MATERIAL_SOURCE_IDS),
    ("CIV.BRG", "SUS", "Suspension Bridge System", ["suspension bridge", "suspension system"], "Bridge-system facet for suspended decks, towers, and cable paths used in civil-engineering and architecture-structure reasoning.", "structural_system_detail", "project_evidence_paths", ENGINEERING_WORK_SOURCE_IDS),
    ("CIV.BRG", "CBS", "Cable Stayed Bridge System", ["cable-stayed bridge", "cable stayed system"], "Bridge-system facet for decks supported by inclined stays from pylons, used to connect Calatrava, Virlogeux, long-span systems, and steel cables.", "structural_system_detail", "project_evidence_paths", ENGINEERING_WORK_SOURCE_IDS),
    ("STR.SSS.MBF", "DGF", "Diagrid Frame", ["diagrid", "diagrid steel frame"], "Structural frame facet for diagonal grid high-rise structures that bridge steel, glass envelopes, structural efficiency, and tall-building expression.", "structural_system_detail", "project_evidence_paths", ENGINEERING_WORK_SOURCE_IDS),
    ("STR.RCS.SWC", "BTC", "Buttressed Core System", ["buttressed core", "buttressed core high-rise system"], "Tall-building structural-system facet for bundled/buttressed core paths connecting high-rise stability, concrete cores, wind response, and structural engineering.", "structural_system_detail", "project_evidence_paths", ENGINEERING_WORK_SOURCE_IDS),
    ("ARC.TAC.SOS", "BRS", "Brise Soleil", ["brise-soleil", "sun breaker", "concrete sun screen"], "Climate-response shading device facet connecting tropical modernism, concrete screens, solar control, daylight, and facade composition.", "design_climate_material_detail", "project_evidence_paths", MATERIAL_SOURCE_IDS),
    ("ARC.HIS.MOD", "MIN", "Minimalist Material Restraint", ["minimalism", "minimalist architecture", "material restraint"], "Movement/style facet for restrained material palettes, precise details, light, proportion, and atmosphere paths.", "movement_material_bridge", "history_material_bridge", PROJECT_EVIDENCE_SOURCE_IDS),
]
for parent, suffix, label, aliases, definition, kind, category, sources in PROJECT_EVIDENCE_NODES:
    _add_node(parent, suffix, label, aliases, definition, kind, category, sources)

PHILIPPINE_ARCHITECTURE_PEOPLE = [
    ("ARE", "Juan M Arellano", ["Juan Arellano", "Metropolitan Theater architect", "National Artist architecture work context"], "architect_person"),
    ("MAP", "Tomas Mapua", ["Tomás Mapúa", "Tomas Mapúa", "Mapua"], "architect_person"),
    ("AAC", "Arcadio Arellano", ["Arcadio de Guzman Arellano", "Arcadio Arellano"], "architect_person"),
    ("CON", "Cesar H Concio", ["Cesar Concio", "University of the Philippines campus architect"], "architect_person"),
    ("ARG", "Carlos D Arguelles", ["Carlos Arguelles", "Philam Life Building architect"], "architect_person"),
    ("COS", "William V Coscolluela", ["William Coscolluela", "WV Coscolluela"], "architect_person"),
    ("FOR", "Gabriel Formoso", ["Gabriel A Formoso", "Formoso architect"], "architect_person"),
    ("MEN", "Felipe M Mendoza", ["Felipe Mendoza", "Mendoza architect"], "architect_person"),
    ("LUN", "Andres Luna De San Pedro", ["Andrés Luna de San Pedro", "Andres Luna", "Juan Luna son architect"], "architect_person"),
    ("ILU", "Federico Ilustre", ["Federico S Ilustre", "Quezon Memorial Shrine architect"], "architect_person"),
]
for suffix, label, aliases, kind in PHILIPPINE_ARCHITECTURE_PEOPLE:
    _add_node(
        "FIG.ARD.CAA",
        suffix,
        label,
        [*aliases, "Filipino architect", "Philippine architecture"],
        f"Metadata-only Filipino architect node for {label}, used to anchor Philippine work, movement, heritage, material, and LEA/ALE history paths.",
        kind,
        "people_works_materials",
        PHILIPPINE_ARCHITECTURE_SOURCE_IDS,
    )

PHILIPPINE_ARCHITECTURE_WORK_ANCHORS = [
    ("MTH", "Manila Metropolitan Theater", ["Metropolitan Theater", "Met", "Manila Met"], "Art Deco theater and heritage landmark path connecting Juan Arellano, Philippine Art Deco, theater/civic space, concrete, ornament, and heritage conservation."),
    ("OLB", "Old Legislative Building", ["Former Legislative Building", "National Museum legislative building"], "Civic and museum heritage work path connecting Juan Arellano, neoclassical civic order, heritage conservation, and public institutional architecture."),
    ("QZH", "Quezon Hall", ["UP Quezon Hall", "University of the Philippines Quezon Hall"], "Campus civic building path connecting Philippine institutional architecture, public space, and modern national-university planning."),
    ("QMS", "Quezon Memorial Shrine", ["Quezon Memorial Circle shrine", "Quezon Memorial"], "Memorial and civic monument path connecting national memory, vertical form, public park setting, and Philippine civic architecture."),
    ("MCC", "Makati Commercial Center Landscape", ["Makati Commercial Center", "Makati pedestrian mall"], "Landscape architecture work path connecting Ildefonso Santos Jr, pedestrian commercial space, outdoor rooms, planting, water features, and modern Philippine landscape practice."),
    ("PAP", "Paco Park Landscape", ["Paco Park", "Paco Park landscape"], "Landscape architecture and heritage-park path connecting Ildefonso Santos Jr, adaptive public space, heritage setting, circulation, and urban landscape design."),
    ("SDC", "Santo Domingo Church Quezon City", ["Sto Domingo Church", "Santo Domingo Church and Convent"], "Modern ecclesiastical architecture path connecting Jose Maria Zaragoza, church planning, reinforced concrete, sacred space, and postwar Philippine modernism."),
    ("SMB", "San Miguel Corporation Building", ["San Miguel Building Ortigas", "Mañosa San Miguel Building"], "Philippine corporate architecture path connecting Francisco Mañosa, vernacular-inspired form, tropical material reasoning, and contemporary Philippine identity."),
    ("BHT", "Bamboo House Ternate", ["Mañosa Bamboo House", "Bamboo House"], "Philippine residential experiment path connecting Francisco Mañosa, bamboo, vernacular influence, tropical design, and sustainable local-material reasoning."),
    ("OLP", "Our Lady Of Peace Shrine EDSA", ["EDSA Shrine", "Our Lady of Peace and Good Voyage Shrine"], "Post-1986 sacred civic work path connecting Francisco Mañosa, public memory, Philippine contemporary architecture, and open-air tropical gathering space."),
    ("MER", "Meralco Building Pasig", ["Meralco Building", "Meralco Ortigas"], "Modern office-building path connecting Jose Maria Zaragoza, postwar Philippine modernism, corporate architecture, and concrete/envelope coordination."),
    ("IHM", "Immaculate Heart Of Mary Parish Quezon City", ["Immaculate Heart of Mary Parish", "IHMP"], "Locsin church path connecting Philippine modern sacred architecture, roof geometry, light, concrete, and heritage-significance metadata."),
    ("RIZ", "Rizal Theater", ["Rizal Theatre", "Nakpil Rizal Theater"], "Theater work path connecting Juan Nakpil, modern Philippine entertainment architecture, civic/theater typology, and Philippine architecture history."),
    ("IDL", "Ideal Theater", ["Pablo Antonio Ideal Theater"], "Philippine theater work path connecting Pablo Antonio, modern theater planning, Art Deco/modern Philippine architecture, and civic entertainment history."),
    ("LYR", "Lyric Theater", ["Pablo Antonio Lyric Theater"], "Philippine theater work path connecting Pablo Antonio, modern entertainment architecture, theater typology, and Philippine architecture history."),
    ("GLX", "Galaxy Theater", ["Pablo Antonio Galaxy Theater"], "Philippine theater work path connecting Pablo Antonio, modern theater design, civic entertainment, and postwar urban culture."),
    ("MPC", "Manila Polo Club", ["Pablo Antonio Manila Polo Club"], "Clubhouse work path connecting Pablo Antonio, social/recreational building type, tropical site planning, and modern Philippine practice."),
    ("CAP", "Capitol Theater", ["Juan Nakpil Capitol Theater"], "Theater work path connecting Juan Nakpil, Philippine entertainment architecture, civic/theater typology, and modern Philippine architecture."),
    ("MJC", "Manila Jockey Club", ["Juan Nakpil Manila Jockey Club"], "Sports and club work path connecting Juan Nakpil, assembly planning, civic recreation, and Philippine modern architecture."),
    ("RUF", "Rufino Building", ["Juan Nakpil Rufino Building"], "Office-building work path connecting Juan Nakpil, commercial architecture, urban development, and Philippine modern practice."),
    ("PVH", "Philippine Village Hotel", ["Juan Nakpil Philippine Village Hotel"], "Hospitality work path connecting Juan Nakpil, tourism architecture, tropical planning, and Philippine modern identity."),
    ("DBC", "Don Bosco Church Makati", ["Jose Maria Zaragoza Don Bosco Church", "Don Bosco Church"], "Modern church work path connecting Jose Maria Zaragoza, ecclesiastical architecture, reinforced concrete, and postwar Philippine sacred space."),
    ("PXC", "Pius XII Center", ["Jose Maria Zaragoza Pius XII Center"], "Religious/institutional work path connecting Jose Maria Zaragoza, Catholic institutional architecture, civic assembly, and modern Philippine practice."),
    ("VSM", "Villa San Miguel", ["Jose Maria Zaragoza Villa San Miguel"], "Ecclesiastical-institutional work path connecting Jose Maria Zaragoza, modern religious administration, and Philippine postwar architecture."),
    ("CMC", "Cebu Metropolitan Cathedral", ["Metropolitan Cathedral of Cebu City", "Jose Maria Zaragoza Cebu Cathedral"], "Cathedral work path connecting Jose Maria Zaragoza, sacred architecture, heritage continuity, and modern liturgical design."),
    ("PFR", "Pearl Farm Resort Samal", ["Francisco Manosa Pearl Farm Resort", "Pearl Farm Resort"], "Resort work path connecting Francisco Mañosa, tropical hospitality, vernacular material influence, and climate-responsive site planning."),
    ("AMN", "Amanpulo Resort Palawan", ["Francisco Manosa Amanpulo", "Amanpulo Resort"], "Resort work path connecting Francisco Mañosa, tropical resort planning, local-material expression, and Philippine contemporary architecture."),
    ("LMP", "Loyola Memorial Park", ["Ildefonso Santos Loyola Memorial Park", "Loyola Memorial Parks"], "Landscape work path connecting Ildefonso Santos Jr, memorial landscape, circulation, cultural landscape, and Philippine landscape architecture."),
    ("THR", "Tagaytay Highlands Resort Landscape", ["Ildefonso Santos Tagaytay Highlands", "Tagaytay Highlands Resort"], "Resort landscape work path connecting Ildefonso Santos Jr, highland site planning, recreation landscapes, and Philippine landscape practice."),
    ("BKB", "Bahay Kubo Building Type", ["nipa hut", "bahay kubo", "Philippine stilt house"], "Learner-facing building-type anchor for Philippine vernacular architecture, bamboo, nipa, timber framing, raised-floor logic, passive cooling, and tropical design."),
    ("BNB", "Bahay Na Bato Building Type", ["bahay na bato", "stone house"], "Learner-facing building-type anchor for Spanish-colonial Philippine domestic architecture, stone or masonry base, timber upper level, capiz windows, ventilation, and heritage adaptation."),
    ("TRG", "Torogan Building Type", ["Maranao torogan", "torogan"], "Learner-facing building-type anchor for Maranao royal-house traditions, timber construction, cultural heritage, carved ornament, and Philippine vernacular architecture."),
    ("IVT", "Ivatan Stone House Building Type", ["Ivatan house", "Ivatan stone house", "Batanes stone house"], "Learner-facing building-type anchor for Ivatan stone-house traditions, thick masonry, typhoon response, lime/stone materiality, and climate resilience."),
    ("IFB", "Ifugao Bale Building Type", ["Ifugao bale", "Ifugao house", "bale"], "Learner-facing building-type anchor for Ifugao timber house traditions, raised-floor construction, joinery, cultural landscape, and vernacular climate response."),
]
for suffix, label, aliases, definition in PHILIPPINE_ARCHITECTURE_WORK_ANCHORS:
    _add_node(
        "FIG.WRK.BUI",
        suffix,
        label,
        aliases,
        f"Metadata-only Philippine work/building-type node for {definition} No protected source payload stored.",
        "work_project_anchor",
        "project_evidence_paths",
        PHILIPPINE_ARCHITECTURE_SOURCE_IDS,
    )

PHILIPPINE_ROLE_NODES = [
    ("NAA", "National Artist For Architecture Status", ["National Artist for Architecture", "Order of National Artist architecture"], "Metadata-only status facet for Filipino architects admitted through official National Artist public metadata."),
    ("LAR", "Landscape Architect Role", ["landscape architect", "landscape architecture role"], "Role facet for architecture-adjacent landscape architects whose work anchors site planning, public space, and Philippine landscape architecture reasoning."),
]
for suffix, label, aliases, definition in PHILIPPINE_ROLE_NODES:
    _add_node("FIG.PTE.ROL", suffix, label, aliases, definition, "people_role_facet", "people_works_materials", PHILIPPINE_ARCHITECTURE_SOURCE_IDS)

IMPROVE_HINTS: dict[str, tuple[list[str], list[str], str, str]] = {
    "ARC.TAC": (["tropical materials", "Philippine climate response", "sun wind rain material strategy"], MATERIAL_SOURCE_IDS, "architecture_climate_materials", "architecture_material_bridge"),
    "ARC.HIS.SEA.PVA": (["bamboo nipa timber capiz vernacular materials", "Philippine vernacular materials"], NCCA_SOURCE_IDS, "philippine_vernacular_materials", "architecture_material_bridge"),
    "ARC.HIS.SEA.BKS": (["bamboo house", "nipa house", "passive cooling material precedent"], NCCA_SOURCE_IDS, "bahay_kubo_materials", "architecture_material_bridge"),
    "ARC.HIS.SEA.BNB": (["capiz window house", "stone timber hybrid house", "climate adapted colonial house materials"], NCCA_SOURCE_IDS, "bahay_na_bato_materials", "architecture_material_bridge"),
    "ARC.MAT": (["material taxonomy", "materials ontology", "materiality"], MATERIAL_SOURCE_IDS, "materials_taxonomy_root", "materials_taxonomy"),
    "MAT": (["materials ontology", "architectural materials taxonomy", "building material families"], MATERIAL_SOURCE_IDS, "materials_taxonomy_root", "materials_taxonomy"),
    "FIG": (["people works materials interconnectivity", "architect engineer work graph"], PEOPLE_SOURCE_IDS, "people_works_interconnectivity", "people_works_materials"),
    "FIG.ARD.CAA.LOC": (["Pritzker-style work anchor not applicable", "Philippine modernism", "reinforced concrete and cultural architecture"], NCCA_SOURCE_IDS, "filipino_architect_existing", "people_works_materials"),
    "FIG.ARD.CAA.NAK": (["National Artist for Architecture", "Philippine architecture history"], NCCA_SOURCE_IDS, "filipino_architect_existing", "people_works_materials"),
    "FIG.ARD.CAA.ANT": (["National Artist for Architecture", "Art Deco in the Philippines"], NCCA_SOURCE_IDS, "filipino_architect_existing", "people_works_materials"),
    "ARC.HIS.MOD.BME": (["béton brut", "raw concrete expression", "exposed concrete modernism"], MATERIAL_SOURCE_IDS, "movement_material_existing", "history_material_bridge"),
    "ARC.HIS.MOD.ISC": (["steel glass curtain wall", "glass and steel modernism"], MATERIAL_SOURCE_IDS, "movement_material_existing", "history_material_bridge"),
    "HIS.MOA.BRS": (["Brutalism material evidence", "béton brut movement path", "exposed concrete movement"], PROJECT_EVIDENCE_SOURCE_IDS, "brutalism_material_path", "history_material_bridge"),
    "HIS.MOV.MOD": (["steel glass reinforced concrete modernism", "modern materials movement path"], PROJECT_EVIDENCE_SOURCE_IDS, "modernism_material_path", "history_material_bridge"),
    "HIS.POC.HTA": (["high-tech steel glass exposed services", "high-tech material expression"], PROJECT_EVIDENCE_SOURCE_IDS, "high_tech_material_path", "history_material_bridge"),
    "ARC.HIS.SEA.TMS": (["tropical modernism material path", "brise soleil tropical modernism"], NCCA_SOURCE_IDS + MATERIAL_SOURCE_IDS, "tropical_modernism_material_path", "history_material_bridge"),
    "ARC.HIS.ANC.GOT": (["stone rib vault stained glass flying buttress", "Gothic material system path"], MATERIAL_SOURCE_IDS, "gothic_material_system_path", "history_material_bridge"),
    "ARC.HIS.ANC.BYZ": (["dome structure sacred architecture", "Byzantine dome path"], MATERIAL_SOURCE_IDS, "byzantine_dome_path", "history_material_bridge"),
    "ARC.WAC.MSW.GRV": (["rib vault flying buttress stone system", "Gothic structure evidence path"], MATERIAL_SOURCE_IDS, "gothic_structural_system_path", "history_material_bridge"),
    "ARC.WAC.CIT.RCV": (["Roman concrete vault dome path", "Roman concrete structural system"], MATERIAL_SOURCE_IDS, "roman_concrete_system_path", "history_material_bridge"),
    "MAT.CMA.CEM.EXP": (["béton brut", "exposed concrete work anchor", "architectural concrete path"], PROJECT_EVIDENCE_SOURCE_IDS, "exposed_concrete_evidence_path", "materials_taxonomy"),
    "MAT.CMA.CEM.CIP": (["cast in place concrete work anchor", "in situ concrete project path"], PROJECT_EVIDENCE_SOURCE_IDS, "cast_in_place_project_path", "materials_taxonomy"),
    "MAT.STM.STS.STS": (["structural steel work anchor", "steel frame project path", "bridge steel path"], ENGINEERING_WORK_SOURCE_IDS, "structural_steel_evidence_path", "materials_taxonomy"),
    "MAT.GLA.CWG": (["curtain wall project anchor", "glass facade evidence path"], PROJECT_EVIDENCE_SOURCE_IDS, "glass_facade_evidence_path", "materials_taxonomy"),
    "MAT.TBB.BAS.BCM": (["bamboo vernacular evidence path", "Philippine bamboo material path"], NCCA_SOURCE_IDS, "bamboo_vernacular_path", "materials_taxonomy"),
    "MAT.TBB.BAS.CAP": (["capiz shell heritage window path", "Philippine capiz material path"], NCCA_SOURCE_IDS, "capiz_heritage_path", "materials_taxonomy"),
    "ARC.BLD.STR.TNS": (["tensile structure work anchor", "membrane and cable structure path"], ENGINEERING_WORK_SOURCE_IDS, "tensile_structure_project_path", "project_evidence_paths"),
    "ARC.BLD.STR.SHL": (["shell structure work anchor", "concrete shell evidence path"], ENGINEERING_WORK_SOURCE_IDS, "shell_structure_project_path", "project_evidence_paths"),
    "ARC.BLD.STR.STF": (["steel frame high rise path", "tall building structural frame"], ENGINEERING_WORK_SOURCE_IDS, "steel_frame_project_path", "project_evidence_paths"),
    "CIV.BRG": (["bridge design architecture engineering path", "bridge structural expression"], ENGINEERING_WORK_SOURCE_IDS, "bridge_architecture_engineering_path", "project_evidence_paths"),
    "FIG.ETS.STE.CAL": (["Calatrava bridge structural expression", "architect-engineer bridge path"], ENGINEERING_WORK_SOURCE_IDS, "calatrava_project_evidence_path", "people_works_materials"),
    "FIG.ETS.STE.KHN": (["tube structural systems high rise", "Fazlur Khan high-rise evidence path"], ENGINEERING_WORK_SOURCE_IDS, "khan_high_rise_evidence_path", "people_works_materials"),
    "FIG.ARD.CAA.AND": (["Church of the Light exposed concrete path", "Ando light concrete materiality"], PROJECT_EVIDENCE_SOURCE_IDS, "ando_project_evidence_path", "people_works_materials"),
    "FIG.ARD.CAA.HAD": (["Hadid MAXXI concrete path", "Hadid deconstructivist work anchor"], PROJECT_EVIDENCE_SOURCE_IDS, "hadid_project_evidence_path", "people_works_materials"),
    "FIG.ARD.CAA.BAN": (["Shigeru Ban paper tube path", "humanitarian material innovation"], PROJECT_EVIDENCE_SOURCE_IDS, "ban_project_evidence_path", "people_works_materials"),
    "FIG.ARD.CAA.KER": (["Francis Kere local material climate path", "Kere social architecture material path"], PROJECT_EVIDENCE_SOURCE_IDS, "kere_project_evidence_path", "people_works_materials"),
}
IMPROVE_HINTS.update({
    "FIG.ARD.CAA.LOC": (["National Artist for Architecture", "Locsin CCP complex", "Locsin thin-shell concrete", "Philippine modernism work path"], PHILIPPINE_ARCHITECTURE_SOURCE_IDS, "filipino_architect_existing", "people_works_materials"),
    "FIG.ARD.CAA.NAK": (["National Artist for Architecture", "Nakpil theater works", "Philippine modern architecture pioneer"], PHILIPPINE_ARCHITECTURE_SOURCE_IDS, "filipino_architect_existing", "people_works_materials"),
    "FIG.ARD.CAA.ANT": (["National Artist for Architecture", "Pablo Antonio FEU", "Philippine Art Deco modernism"], PHILIPPINE_ARCHITECTURE_SOURCE_IDS, "filipino_architect_existing", "people_works_materials"),
    "FIG.ARD.CAA.SAN": (["Ildefonso Santos Jr landscape architect", "Father of Philippine Landscape Architecture", "Paco Park", "Makati Commercial Center"], PHILIPPINE_ARCHITECTURE_SOURCE_IDS, "filipino_landscape_architect_existing", "people_works_materials"),
    "FIG.ARD.CAA.MAN": (["National Artist for Architecture and Allied Arts", "Bobby Manosa", "Filipinism", "Coconut Palace", "Bamboo House"], PHILIPPINE_ARCHITECTURE_SOURCE_IDS, "filipino_architect_existing", "people_works_materials"),
    "FIG.ARD.CAA.ZAR": (["National Artist for Architecture", "modern ecclesiastical architecture", "Santo Domingo Church", "Meralco Building"], PHILIPPINE_ARCHITECTURE_SOURCE_IDS, "filipino_architect_existing", "people_works_materials"),
    "FIG.WRK.BUI.CCP": (["Locsin CCP complex", "Cultural Center of the Philippines", "Philippine modernism concrete civic work"], PHILIPPINE_ARCHITECTURE_SOURCE_IDS, "philippine_work_existing", "project_evidence_paths"),
    "FIG.WRK.BUI.PIC": (["Locsin PICC", "Philippine International Convention Center", "conference architecture"], PHILIPPINE_ARCHITECTURE_SOURCE_IDS, "philippine_work_existing", "project_evidence_paths"),
    "FIG.WRK.BUI.FHA": (["Folk Arts Theater", "Tanghalang Francisco Balagtas", "Locsin theater work"], PHILIPPINE_ARCHITECTURE_SOURCE_IDS, "philippine_work_existing", "project_evidence_paths"),
    "FIG.WRK.BUI.COC": (["Tahanang Pilipino", "Coconut Palace", "Manosa vernacular material path"], PHILIPPINE_ARCHITECTURE_SOURCE_IDS, "philippine_work_existing", "project_evidence_paths"),
    "FIG.WRK.BUI.CHS": (["Locsin Church of the Holy Sacrifice", "thin-shell concrete church", "Philippine modern sacred architecture"], PHILIPPINE_ARCHITECTURE_SOURCE_IDS, "philippine_work_existing", "project_evidence_paths"),
    "FIG.WRK.BUI.FEU": (["Pablo Antonio FEU campus", "Philippine Art Deco educational buildings", "concrete campus architecture"], PHILIPPINE_ARCHITECTURE_SOURCE_IDS, "philippine_work_existing", "project_evidence_paths"),
    "ARC.HIS.SEA.PMP": (["postwar Philippine modernism", "Locsin Antonio Zaragoza modernism", "Philippine concrete modernism"], PHILIPPINE_ARCHITECTURE_SOURCE_IDS, "philippine_modernism_material_path", "history_material_bridge"),
    "ARC.HIS.SEA.ADP": (["Philippine Art Deco", "Manila Metropolitan Theater", "Pablo Antonio FEU", "Filipinized Art Deco"], PHILIPPINE_ARCHITECTURE_SOURCE_IDS, "philippine_art_deco_path", "history_material_bridge"),
    "ARC.HIS.SEA.CPA": (["contemporary Philippine architecture", "Manosa Filipinism", "vernacular-inspired contemporary architecture"], PHILIPPINE_ARCHITECTURE_SOURCE_IDS, "contemporary_philippine_architecture_path", "history_material_bridge"),
    "ARC.HIS.SEA.SCC": (["Spanish colonial Philippine architecture", "Bahay na Bato and church heritage", "masonry timber capiz heritage"], PHILIPPINE_ARCHITECTURE_SOURCE_IDS, "spanish_colonial_philippine_material_path", "history_material_bridge"),
    "ARC.HIS.SEA.TRG": (["Maranao torogan", "vernacular royal house", "timber carved cultural heritage"], PHILIPPINE_ARCHITECTURE_SOURCE_IDS, "philippine_vernacular_building_type", "architecture_material_bridge"),
    "ARC.HIS.SEA.IVT": (["Ivatan stone house", "Batanes stone house", "typhoon-resilient vernacular architecture"], PHILIPPINE_ARCHITECTURE_SOURCE_IDS, "philippine_vernacular_building_type", "architecture_material_bridge"),
    "ARC.HIS.SEA.IFB": (["Ifugao bale", "Cordillera timber house", "raised-floor vernacular architecture"], PHILIPPINE_ARCHITECTURE_SOURCE_IDS, "philippine_vernacular_building_type", "architecture_material_bridge"),
    "MAT.TBB.BAS.NIP": (["nipa roofing", "nipa thatch", "bahay kubo roof material"], PHILIPPINE_ARCHITECTURE_SOURCE_IDS, "nipa_vernacular_path", "materials_taxonomy"),
    "MAT.TBB.DIL.HDW": (["Philippine hardwood heritage path", "timber vernacular construction"], PHILIPPINE_ARCHITECTURE_SOURCE_IDS, "hardwood_vernacular_path", "materials_taxonomy"),
    "MAT.MST.NAS.LIM": (["limestone Ivatan house path", "stone vernacular material"], PHILIPPINE_ARCHITECTURE_SOURCE_IDS, "stone_vernacular_path", "materials_taxonomy"),
    "MAT.MST.CLB": (["brick heritage path", "masonry heritage material"], PHILIPPINE_ARCHITECTURE_SOURCE_IDS, "masonry_heritage_path", "materials_taxonomy"),
})

RELATIONSHIPS: list[tuple[str, str, str, str, list[str]]] = []

def add_rel(from_path: str, predicate: str, to_path: str, category: str, source_ids: list[str] | None = None) -> None:
    RELATIONSHIPS.append((from_path, predicate, to_path, category, source_ids or MATERIAL_SOURCE_IDS))

# Material taxonomy and property/assembly bridges.
for material in [
    "MAT.CMA.CEM.CIP", "MAT.CMA.CEM.PSC", "MAT.CMA.CEM.PTC", "MAT.CMA.CEM.EXP", "MAT.CMA.CEM.BFC", "MAT.CMA.CEM.LWC", "MAT.CMA.CEM.CHB", "MAT.CMA.CEM.RBR", "MAT.CMA.CEM.AGR", "MAT.CMA.CEM.CBN",
]:
    add_rel(material, "has_facet", "MAT.PRF.MEC.CPS", "material_property")
    add_rel(material, "has_facet", "MAT.PRF.MOI.DUR", "material_property")
add_rel("MAT.CMA.CEM.CIP", "requires", "CON.TMP.FOR", "material_method")
add_rel("MAT.CMA.CEM.EXP", "requires", "ARC.MAT.CON.FRM", "material_method")
add_rel("MAT.CMA.CEM.BFC", "requires", "ARC.MAT.CON.FRM", "material_method")
add_rel("MAT.CMA.CEM.RBR", "has_facet", "ARC.MAT.CON.RCC", "material_system")
for component in ["ARC.BLD.STR.SLB", "ARC.BLD.STR.BEM", "ARC.BLD.STR.COL", "ARC.BLD.STR.SHW", "ARC.BLD.STR.FDS"]:
    add_rel("ARC.MAT.CON.RCC", "has_facet", component, "material_structural_component")
for material in ["MAT.STM.STS.STS", "MAT.STM.STS.WST", "MAT.STM.STS.LGS", "MAT.STM.STS.MDK", "MAT.STM.MEC.GIS", "MAT.STM.MEC.RFS", "MAT.STM.MEC.SSM", "MAT.STM.MEC.ALP"]:
    add_rel(material, "has_facet", "MAT.PRF.MEC.TEN", "material_property")
    add_rel(material, "has_facet", "MAT.PRF.FIR.FIR", "material_property")
for material in ["MAT.TBB.DIL.HDW", "MAT.TBB.DIL.SFW", "MAT.TBB.ENW.GLU", "MAT.TBB.ENW.CLT", "MAT.TBB.ENW.LVL", "MAT.TBB.ENW.PLY", "MAT.TBB.BAS.BCM", "MAT.TBB.BAS.RAT", "MAT.TBB.BAS.NIP", "MAT.TBB.BAS.ANH", "MAT.TBB.BAS.CAP"]:
    add_rel(material, "has_facet", "MAT.PRF.ENV.LOC", "material_locality")
    add_rel(material, "has_facet", "MAT.PRF.AES.TEX", "material_perception")
for material in ["MAT.TBB.BAS.BCM", "MAT.TBB.BAS.NIP", "MAT.TBB.BAS.ANH", "MAT.TBB.BAS.CAP", "MAT.TBB.DIL.HDW"]:
    add_rel("ARC.HIS.SEA.PVA", "has_facet", material, "philippine_vernacular_materials", NCCA_SOURCE_IDS)
    add_rel("ARC.TAC", "has_facet", material, "tropical_materials", NCCA_SOURCE_IDS)
add_rel("ARC.HIS.SEA.BKS", "has_facet", "MAT.TBB.BAS.BCM", "bahay_kubo_materials", NCCA_SOURCE_IDS)
add_rel("ARC.HIS.SEA.BKS", "has_facet", "MAT.TBB.BAS.NIP", "bahay_kubo_materials", NCCA_SOURCE_IDS)
add_rel("ARC.HIS.SEA.BNB", "has_facet", "MAT.TBB.BAS.CAP", "bahay_na_bato_materials", NCCA_SOURCE_IDS)
add_rel("ARC.HIS.SEA.BNB", "has_facet", "MAT.TBB.DIL.HDW", "bahay_na_bato_materials", NCCA_SOURCE_IDS)
for material in ["MAT.MST.NAS.GRA", "MAT.MST.NAS.MAR", "MAT.MST.NAS.LIM", "MAT.MST.NAS.SDS", "MAT.MST.NAS.ADO", "MAT.MST.CMU.HBL"]:
    add_rel(material, "has_facet", "MAT.ASM.WAL", "material_assembly")
    add_rel(material, "has_facet", "MAT.PRF.THE.THM", "material_property")
for material in ["MAT.FIP.FLF.CER", "MAT.FIP.FLF.POR", "MAT.FIP.FLF.CMT", "MAT.FIP.FLF.TRZ", "MAT.FIP.FLF.VIN", "MAT.FIP.FLF.LNO", "MAT.FIP.FLF.RUB", "MAT.FIP.FLF.CPT"]:
    add_rel(material, "has_facet", "MAT.ASM.FLR", "material_assembly")
    add_rel(material, "has_facet", "MAT.PRF.AES.SLP", "material_finish_property")
add_rel("MAT.FIP.FLF.CER", "has_facet", "MAT.ASM.WET", "wet_area_material")
add_rel("MAT.FIP.FLF.POR", "has_facet", "MAT.ASM.WET", "wet_area_material")
for material in ["MAT.FIP.WAF.GYB", "MAT.FIP.WAF.FCB", "MAT.FIP.CES.APN"]:
    add_rel(material, "has_facet", "MAT.ASM.CEI", "ceiling_wall_assembly")
    add_rel(material, "has_facet", "MAT.PRF.ACO.ABS", "acoustic_material")
for material in ["MAT.GLA.FLG", "MAT.GLA.TPG", "MAT.GLA.LOW", "MAT.GLA.CWG", "MAT.GLA.SPG"]:
    add_rel(material, "has_facet", "MAT.ASM.CUR", "glazing_assembly")
    add_rel(material, "has_facet", "ARC.TAC.SOS.DAY", "daylighting_material")
    add_rel(material, "has_facet", "MAT.PRF.THE.REF", "optical_property")
for material in ["MAT.MEM.RME.WPM", "MAT.MEM.RME.SBS", "MAT.MEM.RME.TPO", "MAT.MEM.RME.PVM", "MAT.MEM.RME.EPD", "MAT.MEM.VAP.DPC", "MAT.MEM.VAP.AIR", "MAT.MEM.VAP.VBR"]:
    add_rel(material, "has_facet", "MAT.ASM.ROF", "waterproofing_assembly")
    add_rel(material, "has_facet", "MAT.PRF.MOI.MRS", "moisture_property")
    add_rel(material, "constrains", "ARC.ENV.ROF.RDP", "envelope_detail")
for material in ["MAT.INS.TIN.MIN", "MAT.INS.TIN.FIG", "MAT.INS.TIN.FOA"]:
    add_rel(material, "has_facet", "MAT.PRF.THE.THM", "thermal_property")
    add_rel(material, "has_facet", "MAT.PRF.ACO.ABS", "acoustic_property")
for material in ["MAT.EAR.RME", "MAT.EAR.ADB", "MAT.EAR.CEB", "MAT.EAR.COB", "MAT.EAR.THC"]:
    add_rel(material, "has_facet", "MAT.PRF.ENV.EBC", "low_carbon_material")
    add_rel(material, "has_facet", "MAT.PRF.THE.THM", "passive_design_material")
    add_rel(material, "has_facet", "ARC.TAC", "tropical_material_path")

# Project-specific evidence pass: material bridge edges used to explain why works,
# systems, assemblies, and LEA/ALE study topics are connected. These remain
# concept-to-concept edges, never person-to-material shortcuts.
for material in ["MAT.CMA.CEM.CIP", "MAT.CMA.CEM.PSC", "MAT.CMA.CEM.PTC", "MAT.CMA.CEM.EXP"]:
    for component in ["ARC.BLD.STR.SLB", "ARC.BLD.STR.BEM", "ARC.BLD.STR.COL", "ARC.BLD.STR.FDS"]:
        add_rel(material, "has_facet", component, "material_structural_component")
for material, facet in [
    ("MAT.CMA.CEM.PSC", "ARC.BLD.STR.LSS"),
    ("MAT.CMA.CEM.PTC", "ARC.BLD.STR.LSS"),
    ("MAT.CMA.CEM.PTC", "ARC.BLD.STR.SLB"),
    ("MAT.CMA.CEM.EXP", "MAT.PRF.AES.TEX"),
    ("MAT.CMA.CEM.EXP", "ARC.HIS.MOD.BME"),
    ("MAT.CMA.CEM.CHB", "MAT.ASM.WAL"),
    ("MAT.CMA.CEM.CHB", "MAT.FIP.WAF.PLS"),
    ("MAT.CMA.CEM.RBR", "STR.RCS.SBC"),
    ("ARC.MAT.STM.STL", "ARC.BLD.STR.LSS"),
    ("ARC.MAT.STM.STL", "ARC.BLD.STR.STF"),
    ("ARC.MAT.STM.STL", "STR.SSS.MBF"),
    ("ARC.MAT.STM.STL", "STR.SSS.TCM"),
    ("ARC.MAT.STM.STL", "HIS.POC.HTA"),
    ("MAT.STM.STS.CBL", "CIV.BRG"),
    ("MAT.STM.STS.CBL", "STR.SSS.TCM"),
    ("MAT.STM.MEC.RFS", "MAT.ASM.ROF"),
    ("MAT.STM.MEC.RFS", "ARC.ENV.ROF"),
    ("MAT.STM.MEC.ALP", "MAT.ASM.FAC"),
    ("MAT.TBB.DIL.HDW", "MAT.ASM.FLR"),
    ("MAT.TBB.DIL.HDW", "MAT.ASM.DOR"),
    ("MAT.TBB.DIL.HDW", "MAT.ASM.WIN"),
    ("MAT.TBB.ENW.GLU", "ARC.BLD.STR.LSS"),
    ("MAT.TBB.ENW.GLU", "MAT.ASM.ROF"),
    ("MAT.TBB.ENW.GLU", "ARC.BLD.STR.ARS"),
    ("MAT.TBB.ENW.CLT", "MAT.ASM.WAL"),
    ("MAT.TBB.ENW.CLT", "MAT.ASM.FLR"),
    ("MAT.TBB.ENW.CLT", "MAT.ASM.ROF"),
    ("MAT.TBB.BAS.BCM", "ARC.HIS.SEA.BKS"),
    ("MAT.TBB.BAS.BCM", "ARC.TAC.NVS"),
    ("MAT.TBB.BAS.NIP", "MAT.ASM.ROF"),
    ("MAT.TBB.BAS.NIP", "ARC.HIS.SEA.BKS"),
    ("MAT.TBB.BAS.CAP", "MAT.ASM.WIN"),
    ("MAT.TBB.BAS.CAP", "ARC.TAC.SOS.DAY"),
    ("MAT.TBB.BAS.CAP", "ARC.HIS.SEA.BNB"),
    ("MAT.GLA.CWG", "MAT.ASM.FAC"),
    ("MAT.GLA.CWG", "ARC.ENV.WAL"),
    ("MAT.GLA.LOW", "ARC.TAC.SOS.SHD"),
    ("MAT.GLA.TPG", "MAT.ASM.WIN"),
    ("MAT.GLA.STG", "MAT.ASM.WIN"),
    ("MAT.GLA.STG", "ARC.TAC.SOS.DAY"),
    ("MAT.FIP.FLF.CER", "LAW.SCP.MPF.TOI"),
    ("MAT.FIP.FLF.CER", "ARC.INT.FIN"),
    ("MAT.FIP.FLF.POR", "LAW.SCP.MPF.TOI"),
    ("MAT.FIP.FLF.CMT", "MAT.ASM.WET"),
    ("MAT.FIP.FLF.TRZ", "MAT.ASM.WET"),
    ("MAT.FIP.FLF.TRZ", "ARC.INT.FIN"),
    ("MAT.FIP.FLF.CPT", "MAT.PRF.ACO.ABS"),
    ("MAT.MEM.RME.WPM", "MAT.ASM.WET"),
    ("MAT.MEM.RME.WPM", "ARC.ENV"),
    ("MAT.MEM.VAP.DPC", "MAT.ASM.WAL"),
    ("MAT.MEM.VAP.AIR", "MAT.ASM.FAC"),
    ("MAT.INS.TIN.MIN", "MAT.ASM.FRW"),
    ("MAT.INS.TIN.MIN", "MAT.ASM.ACC"),
    ("MAT.FIP.CES.APN", "ARC.INT.PAC.ACU"),
    ("MAT.FIP.CES.APN", "MAT.ASM.ACC"),
    ("MAT.FIP.WAF.GYB", "MAT.ASM.FRW"),
    ("MAT.FIP.WAF.FCB", "MAT.ASM.WET"),
]:
    add_rel(material, "has_facet", facet, "material_cross_bridge")

# Movement/material and theory/material bridges.
for material in ["ARC.MAT.CON.RCC", "MAT.CMA.CEM.EXP", "MAT.CMA.CEM.BFC"]:
    add_rel("ARC.HIS.MOD.BME", "has_facet", material, "movement_material_path")
for material in ["MAT.GLA.CWG", "ARC.MAT.STM.STL", "MAT.STM.STS.MDK"]:
    add_rel("ARC.HIS.MOD.ISC", "has_facet", material, "movement_material_path")
for material in ["MAT.MST.NAS.LIM", "MAT.MST.NAS.SDS", "MAT.GLA.FLG"]:
    add_rel("ARC.HIS.ANC.GOT", "has_facet", material, "movement_material_path")
for material in ["MAT.CMA.CEM.CBN", "MAT.CMA.CEM.CIP", "MAT.MST.NAS.ADO"]:
    add_rel("ARC.HIS.ANC.RFB", "has_facet", material, "movement_material_path")
for material in ["MAT.PRF.AES.TEX", "MAT.PRF.AES.COL", "MAT.PRF.THE.REF", "MAT.PRF.ENV.EBC"]:
    add_rel("ARC.DTS.PPT.PLM", "has_facet", material, "theory_materiality_path")

# People, award, role, work, and work-material/system paths.
for suffix, label, aliases, year, sources in PRITZKER_ARCHITECTS:
    person = f"FIG.ARD.CAA.{suffix}"
    add_rel(person, "has_facet", "FIG.PTE.ROL.ARC", "person_role", sources)
    add_rel(person, "has_facet", "FIG.PTE.ROL.LAU", "award_status", sources)
    add_rel("FIG.AWD.PRI.PZK", "has_facet", person, "pritzker_laureate", ["SRC-PRITZKER-LAUREATES-OFFICIAL"])
    nationality = PRITZKER_ARCHITECT_NATIONALITIES.get(suffix)
    if nationality:
        add_rel(person, "has_facet", f"FIG.PTE.NAT.{nationality}", "architect_nationality", sources)
for suffix, *_ in OTHER_ARCHITECTS:
    add_rel(f"FIG.ARD.CAA.{suffix}", "has_facet", "FIG.PTE.ROL.ARC", "person_role", PEOPLE_SOURCE_IDS)
    nationality = OTHER_ARCHITECT_NATIONALITIES.get(suffix)
    if nationality:
        add_rel(f"FIG.ARD.CAA.{suffix}", "has_facet", f"FIG.PTE.NAT.{nationality}", "architect_nationality", PEOPLE_SOURCE_IDS)
for suffix, label, aliases, kind in ENGINEERS:
    person = f"FIG.ETS.STE.{suffix}"
    add_rel(person, "has_facet", "FIG.PTE.ROL.SEN", "person_role", PEOPLE_SOURCE_IDS)
    nationality = ENGINEER_ARCHITECT_NATIONALITIES.get(suffix)
    if nationality:
        add_rel(person, "has_facet", f"FIG.PTE.NAT.{nationality}", "architect_engineer_nationality", PEOPLE_SOURCE_IDS)
    if kind in {"architect_engineer", "engineer_architect", "designer_engineer"}:
        add_rel(person, "has_facet", "FIG.PTE.ROL.ARC", "architect_engineer_role", PEOPLE_SOURCE_IDS)
        add_rel(person, "has_facet", "FIG.PTE.ROL.AEN", "architect_engineer_role", PEOPLE_SOURCE_IDS)
        add_rel("FIG.PTE.ROL.AEN", "has_facet", person, "architect_engineer_index", PEOPLE_SOURCE_IDS)
for architect_engineer_path in ["FIG.ARD.CAA.FOT"]:
    add_rel(architect_engineer_path, "has_facet", "FIG.PTE.ROL.AEN", "architect_engineer_role", PEOPLE_SOURCE_IDS)
    add_rel(architect_engineer_path, "has_facet", "FIG.PTE.ROL.SEN", "architect_engineer_role", PEOPLE_SOURCE_IDS)
    add_rel("FIG.PTE.ROL.AEN", "has_facet", architect_engineer_path, "architect_engineer_index", PEOPLE_SOURCE_IDS)

# Rights-safe law, country, local, and standards-family classification overlays.
for standard_path, jurisdiction_path, category in [
    ("COM.STD.AIA", "LAW.JUR.USA", "aia_us_practice_standards"),
    ("COM.STD.RIB", "LAW.JUR.GBR", "riba_uk_practice_standards"),
    ("COM.STD.IBS", "LAW.JUR.USA", "ibs_nibs_us_building_sciences"),
    ("COM.STD.NIB", "LAW.JUR.USA", "nibs_us_building_sciences"),
    ("COM.STD.ICC", "LAW.JUR.USA", "icc_us_model_codes"),
    ("COM.STD.BSF", "LAW.JUR.GBR", "british_standards_family"),
    ("COM.STD.ISO", "LAW.JUR.INT", "international_standards_family"),
    ("COM.STD.WHO", "LAW.JUR.INT", "international_guidance_family"),
    ("COM.STD.ICM", "LAW.JUR.INT", "international_conservation_doctrine"),
    ("COM.STD.PHL", "LAW.JUR.PHL", "philippine_law_source_family"),
]:
    add_rel(standard_path, "has_facet", jurisdiction_path, category, STANDARDS_CLASSIFICATION_SOURCE_IDS)
for law_path in ["LAW.LGZ", "LAW.SCH.SUS", "LAW.SCP", "LAW.PFC", "LAW.PAL", "LAW.AAP"]:
    add_rel(law_path, "has_facet", "LAW.JUR.PHL", "philippine_law_jurisdiction", STANDARDS_CLASSIFICATION_SOURCE_IDS)
add_rel("LAW.LGZ", "has_facet", "LAW.JUR.LOC", "local_government_law_scope", STANDARDS_CLASSIFICATION_SOURCE_IDS)
add_rel("LAW.SCH.SUS", "has_facet", "LAW.JUR.LOC", "local_subdivision_standard_scope", STANDARDS_CLASSIFICATION_SOURCE_IDS)

# Existing Filipino architect/work anchors.
for person, work in [("FIG.ARD.CAA.LOC", "FIG.WRK.BUI.CCP"), ("FIG.ARD.CAA.LOC", "FIG.WRK.BUI.PIC"), ("FIG.ARD.CAA.LOC", "FIG.WRK.BUI.FHA"), ("FIG.ARD.CAA.MAN", "FIG.WRK.BUI.COC"), ("FIG.ARD.CAA.NAK", "FIG.WRK.BUI.UST")]:
    add_rel(person, "has_facet", work, "filipino_architect_work", NCCA_SOURCE_IDS)
for person in ["FIG.ARD.CAA.LOC", "FIG.ARD.CAA.NAK", "FIG.ARD.CAA.ANT", "FIG.ARD.CAA.SAN", "FIG.ARD.CAA.MAN", "FIG.ARD.CAA.ZAR"]:
    add_rel(person, "has_facet", "FIG.PTE.ROL.ARC", "person_role", NCCA_SOURCE_IDS)
    add_rel(person, "has_facet", "ARC.HIS.SEA.PMP", "philippine_modernism_path", NCCA_SOURCE_IDS)

WORK_OWNER_PREFIX = {suffix: owner for suffix, _label, _aliases, _typology, owner in WORKS}
for suffix, owner in WORK_OWNER_PREFIX.items():
    work = f"FIG.WRK.BUI.{suffix}"
    if owner in {x[0] for x in PRITZKER_ARCHITECTS} or owner in {x[0] for x in OTHER_ARCHITECTS}:
        add_rel(f"FIG.ARD.CAA.{owner}", "has_facet", work, "person_work", PEOPLE_SOURCE_IDS)
    elif owner == "LOC":
        add_rel("FIG.ARD.CAA.LOC", "has_facet", work, "person_work", NCCA_SOURCE_IDS)
    else:
        add_rel(f"FIG.ETS.STE.{owner}", "has_facet", work, "person_work", PEOPLE_SOURCE_IDS)

work_facets: dict[str, list[str]] = {
    "FIG.WRK.BUI.CHL": ["MAT.CMA.CEM.EXP", "ARC.TAC.SOS.DAY", "ARC.DTS.CPT.GSP"],
    "FIG.WRK.BUI.GUG": ["MAT.STM.STS.STS", "MAT.GLA.CWG", "ARC.HIS.MOD.CPD"],
    "FIG.WRK.BUI.VFS": ["MAT.CMA.CEM.CIP", "ARC.HIS.MOD.DFS", "ARC.DTS.PST.PDF"],
    "FIG.WRK.BUI.MAX": ["MAT.CMA.CEM.CIP", "ARC.HIS.MOD.DFS", "ARC.THE.DPR.CIR"],
    "FIG.WRK.BUI.HAC": ["MAT.ASM.FAC", "ARC.HIS.MOD.CPD", "ARC.DTS.PST.PDF"],
    "FIG.WRK.BUI.SAL": ["MAT.CMA.CEM.EXP", "MAT.PRF.THE.THM", "ARC.THE.DPR.ORD"],
    "FIG.WRK.BUI.KIM": ["MAT.CMA.CEM.CIP", "ARC.TAC.SOS.DAY", "ARC.THE.DPR.SCL"],
    "FIG.WRK.BUI.VSA": ["ARC.MAT.CON.RCC", "ARC.HIS.MOD.ISC", "ARC.DTS.MDD.PLF"],
    "FIG.WRK.BUI.UNI": ["MAT.CMA.CEM.EXP", "ARC.HIS.MOD.BME", "ARC.DTS.MDD.MSH"],
    "FIG.WRK.BUI.FAR": ["MAT.GLA.CWG", "MAT.STM.STS.STS", "ARC.HIS.MOD.ISC"],
    "FIG.WRK.BUI.BAU": ["MAT.GLA.CWG", "ARC.HIS.MOD.BPM", "ARC.DTS.MDD.MAA"],
    "FIG.WRK.BUI.POM": ["ARC.MAT.STM.STL", "MAT.GLA.CWG", "ARC.HIS.MOD.ISC"],
    "FIG.WRK.BUI.LOY": ["ARC.MAT.STM.STL", "MAT.GLA.CWG", "ARC.BLD.SRV.UCO"],
    "FIG.WRK.BUI.HKB": ["ARC.MAT.STM.STL", "MAT.GLA.CWG", "ARC.BLD.STR.STF"],
    "FIG.WRK.BUI.SCL": ["MAT.GLA.CWG", "ARC.THE.DPR.CIR", "ARC.DTS.PST.DID"],
    "FIG.WRK.BUI.MOS": ["ARC.BLD.STR.TNS", "STR.SYS.SPC", "MAT.PRF.MEC.TEN"],
    "FIG.WRK.BUI.PCH": ["MAT.TBB.ENW.PLY", "MAT.EAR.THC", "ARC.HIS.SEA.PVA"],
    "FIG.WRK.BUI.GAN": ["MAT.EAR.CEB", "MAT.PRF.ENV.LOC", "ARC.TAC.NVS.XVN"],
    "FIG.WRK.BUI.SRP": ["MAT.ASM.FAC", "MAT.PRF.AES.TEX", "ARC.DTS.PPT.MMA"],
    "FIG.WRK.BUI.ALB": ["ARC.BLD.STR.TNS", "CIV.BRG.SPN", "MAT.PRF.MEC.TEN"],
    "FIG.WRK.BUI.MAM": ["ARC.BLD.STR.LSS", "MAT.STM.STS.STS", "ARC.THE.DPR.TRN"],
    "FIG.WRK.BUI.JHC": ["ARC.BLD.STR.STF", "STR.SSS.MBF", "MAT.STM.STS.STS"],
    "FIG.WRK.BUI.WIT": ["ARC.BLD.STR.STF", "STR.SSS.MBF", "MAT.STM.STS.STS"],
    "FIG.WRK.BUI.PDS": ["ARC.MAT.CON.RCC", "ARC.BLD.STR.SHL", "STR.RCS.SBC"],
    "FIG.WRK.BUI.SAB": ["ARC.MAT.CON.RCC", "CIV.BRG.SPN", "ARC.BLD.STR.ARS"],
    "FIG.WRK.BUI.EFT": ["MAT.STM.STS.STS", "ARC.BLD.STR.LSS", "CIV.BRG.SPN"],
    "FIG.WRK.BUI.LMA": ["ARC.MAT.CON.RCC", "ARC.BLD.STR.SHL", "MAT.PRF.MEC.CPS"],
    "FIG.WRK.BUI.ZAR": ["ARC.MAT.CON.RCC", "ARC.BLD.STR.SHL", "STR.SYS.SPC"],
    "FIG.WRK.BUI.CCO": ["MAT.MST.CLB", "ARC.BLD.STR.SHL", "MAT.PRF.AES.TEX"],
    "FIG.WRK.BUI.CSB": ["MAT.STM.STS.STS", "CIV.BRG.SPN", "MAT.PRF.MEC.TEN"],
    "FIG.WRK.BUI.BIO": ["ARC.BLD.STR.LSS", "MAT.PRF.MEC.TEN", "ARC.DTS.PST.PDF"],
    "FIG.WRK.BUI.CCP": ["ARC.MAT.CON.RCC", "ARC.HIS.SEA.PMP", "ARC.THE.DPR.FRM"],
    "FIG.WRK.BUI.PIC": ["ARC.MAT.CON.RCC", "ARC.HIS.SEA.PMP", "CON.DMC.DBB.BID"],
    "FIG.WRK.BUI.COC": ["MAT.TBB.BAS.BCM", "MAT.TBB.BAS.CAP", "ARC.HIS.SEA.CPA"],
}
for work, facets in work_facets.items():
    for facet in facets:
        add_rel(work, "has_facet", facet, "work_material_system_movement", NCCA_SOURCE_IDS if work in {"FIG.WRK.BUI.CCP", "FIG.WRK.BUI.PIC", "FIG.WRK.BUI.COC"} else PEOPLE_SOURCE_IDS)

# Project-specific deepening: explicit people -> work -> material/system/movement paths.
project_person_work_edges = [
    ("FIG.ARD.CAA.LCO", "FIG.WRK.BUI.RON", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.ARD.CAA.LCO", "FIG.WRK.BUI.LAT", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.ARD.CAA.KAH", "FIG.WRK.BUI.NAD", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.ARD.CAA.KAH", "FIG.WRK.BUI.EXE", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.ARD.CAA.AAL", "FIG.WRK.BUI.PAI", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.ARD.CAA.AAL", "FIG.WRK.BUI.SAY", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.ARD.CAA.MIE", "FIG.WRK.BUI.BCP", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.ARD.CAA.MIE", "FIG.WRK.BUI.SEA", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.ARD.CAA.UTZ", "FIG.WRK.BUI.SYD", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.ETS.STE.ARU", "FIG.WRK.BUI.SYD", ENGINEERING_WORK_SOURCE_IDS),
    ("FIG.ARD.CAA.HER", "FIG.WRK.BUI.TAT", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.ARD.CAA.MEU", "FIG.WRK.BUI.TAT", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.ARD.CAA.HER", "FIG.WRK.BUI.NBS", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.ARD.CAA.MEU", "FIG.WRK.BUI.NBS", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.ARD.CAA.MUR", "FIG.WRK.BUI.MAV", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.ARD.CAA.WSH", "FIG.WRK.BUI.NHB", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.ARD.CAA.PMR", "FIG.WRK.BUI.BMS", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.ARD.CAA.SOU", "FIG.WRK.BUI.BRG", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.ARD.CAA.THM", "FIG.WRK.BUI.CAL", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.ARD.CAA.MON", "FIG.WRK.BUI.KRS", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.ARD.CAA.FOS", "FIG.WRK.BUI.GHK", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.ARD.CAA.FOS", "FIG.WRK.BUI.HAN", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.ARD.CAA.FOS", "FIG.WRK.BUI.MVA", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.ETS.STE.VIR", "FIG.WRK.BUI.MVA", ENGINEERING_WORK_SOURCE_IDS),
    ("FIG.ARD.CAA.FOS", "FIG.WRK.BUI.BMG", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.ETS.STE.BAL", "FIG.WRK.BUI.BMG", ENGINEERING_WORK_SOURCE_IDS),
    ("FIG.ETS.STE.BAK", "FIG.WRK.BUI.BRJ", ENGINEERING_WORK_SOURCE_IDS),
    ("FIG.ETS.STE.ROE", "FIG.WRK.BUI.BRB", ENGINEERING_WORK_SOURCE_IDS),
    ("FIG.ETS.STE.STR", "FIG.WRK.BUI.GGB", ENGINEERING_WORK_SOURCE_IDS),
    ("FIG.ARD.CAA.ZUM", "FIG.WRK.BUI.THV", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.ARD.CAA.ZUM", "FIG.WRK.BUI.BKF", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.ARD.CAA.NOU", "FIG.WRK.BUI.LAD", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.ARD.CAA.BAN", "FIG.WRK.BUI.PCT", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.ARD.CAA.KER", "FIG.WRK.BUI.LYC", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.ETS.STE.RIC", "FIG.WRK.BUI.POM", ENGINEERING_WORK_SOURCE_IDS),
    ("FIG.ARD.CAA.LIU", "FIG.WRK.BUI.LUY", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.ARD.CAA.LIU", "FIG.WRK.BUI.SIK", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.ARD.CAA.YAM", "FIG.WRK.BUI.HAK", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.ARD.CAA.HAD", "FIG.WRK.BUI.AQA", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.ARD.CAA.HAD", "FIG.WRK.BUI.DDP", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.ARD.CAA.CHP", "FIG.WRK.BUI.NEM", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.ARD.CAA.MUR", "FIG.WRK.BUI.MNY", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.ARD.CAA.SEJ", "FIG.WRK.BUI.RLC", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.ARD.CAA.NIZ", "FIG.WRK.BUI.RLC", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.ARD.CAA.ITO", "FIG.WRK.BUI.TAU", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.ARD.CAA.GEH", "FIG.WRK.BUI.FVL", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.ARD.CAA.GEH", "FIG.WRK.BUI.DIS", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.ARD.CAA.PIA", "FIG.WRK.BUI.BEY", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.ARD.CAA.PIA", "FIG.WRK.BUI.TJI", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.ARD.CAA.FOS", "FIG.WRK.BUI.SAC", PROJECT_EVIDENCE_SOURCE_IDS),
    ("FIG.ETS.STE.EIF", "FIG.WRK.BUI.GAR", ENGINEERING_WORK_SOURCE_IDS),
    ("FIG.ETS.STE.MAI", "FIG.WRK.BUI.SWB", ENGINEERING_WORK_SOURCE_IDS),
    ("FIG.ETS.STE.FRE", "FIG.WRK.BUI.ORL", ENGINEERING_WORK_SOURCE_IDS),
    ("FIG.ARD.CAA.FOT", "FIG.WRK.BUI.MHL", PROJECT_EVIDENCE_SOURCE_IDS + ENGINEERING_WORK_SOURCE_IDS),
    ("FIG.ETS.STE.WER", "FIG.WRK.BUI.LNE", ENGINEERING_WORK_SOURCE_IDS),
    ("FIG.ARD.CAA.LOC", "FIG.WRK.BUI.CHS", NCCA_SOURCE_IDS),
    ("FIG.ARD.CAA.ANT", "FIG.WRK.BUI.FEU", NCCA_SOURCE_IDS),
    ("FIG.ETS.STE.ARU", "FIG.WRK.BUI.POM", ENGINEERING_WORK_SOURCE_IDS),
    ("FIG.ETS.STE.SCH", "FIG.WRK.BUI.MOS", ENGINEERING_WORK_SOURCE_IDS),
    ("FIG.ETS.STE.RIC", "FIG.WRK.BUI.SYD", ENGINEERING_WORK_SOURCE_IDS),
    ("FIG.ETS.STE.NRV", "FIG.WRK.BUI.PDS", ENGINEERING_WORK_SOURCE_IDS),
    ("FIG.ETS.STE.CAN", "FIG.WRK.BUI.LMA", ENGINEERING_WORK_SOURCE_IDS),
    ("FIG.ETS.STE.TOR", "FIG.WRK.BUI.ZAR", ENGINEERING_WORK_SOURCE_IDS),
]
for person, work, sources in project_person_work_edges:
    add_rel(person, "has_facet", work, "person_work", sources)

project_work_facets: dict[str, list[str]] = {
    "FIG.WRK.BUI.RON": ["ARC.MAT.CON.RCC", "MAT.CMA.CEM.CIP", "ARC.THE.DPR.FRM", "ARC.TAC.SOS.DAY"],
    "FIG.WRK.BUI.LAT": ["MAT.CMA.CEM.EXP", "ARC.TAC.SOS.BRS", "ARC.HIS.MOD.BME", "ARC.DTS.MDD.USM"],
    "FIG.WRK.BUI.NAD": ["MAT.CMA.CEM.CIP", "ARC.THE.DPR.ORD", "ARC.TAC.SOS.DAY", "ARC.DTS.PPT.PLM"],
    "FIG.WRK.BUI.EXE": ["MAT.MST.CLB", "MAT.CMA.CEM.CIP", "ARC.THE.DPR.CIR", "ARC.INT.PAC.ACU"],
    "FIG.WRK.BUI.PAI": ["ARC.ECD.VEN", "ARC.TAC.SOS.DAY", "MAT.PRF.AES.COL", "ARC.INT.FIN"],
    "FIG.WRK.BUI.SAY": ["MAT.MST.CLB", "MAT.TBB.DIL.HDW", "ARC.THE.DPR.CIR", "ARC.HIS.MOD.ISC"],
    "FIG.WRK.BUI.BCP": ["MAT.GLA.FLG", "ARC.MAT.STM.STL", "MAT.MST.NAS.MAR", "ARC.HIS.MOD.MIN"],
    "FIG.WRK.BUI.SEA": ["MAT.GLA.CWG", "ARC.MAT.STM.STL", "ARC.BLD.STR.STF", "ARC.HIS.MOD.ISC"],
    "FIG.WRK.BUI.SYD": ["ARC.BLD.STR.SHL", "ARC.BLD.STR.DOM", "MAT.FIP.FLF.CER", "ARC.DTS.PST.PDF"],
    "FIG.WRK.BUI.TAT": ["MAT.MST.CLB", "ARC.HER.ADM", "ARC.HIS.MOD.CPD", "ARC.DOC.DET"],
    "FIG.WRK.BUI.NBS": ["ARC.MAT.STM.STL", "ARC.BLD.STR.LSS", "STR.SYS.SPC", "ARC.HIS.MOD.CPD"],
    "FIG.WRK.BUI.MAV": ["ARC.TAC.NVS", "ARC.TAC.SOS.SHD", "MAT.STM.MEC.RFS", "MAT.TBB.DIL.HDW"],
    "FIG.WRK.BUI.NHB": ["MAT.MST.CLB", "MAT.FIP.FLF.CMT", "ARC.HER.FAB", "SUS.RSC.MAT"],
    "FIG.WRK.BUI.BMS": ["MAT.CMA.CEM.EXP", "ARC.BLD.STR.LSS", "ARC.HIS.MOD.BME", "ARC.THE.DPR.FRM"],
    "FIG.WRK.BUI.BRG": ["MAT.CMA.CEM.CIP", "ARC.BLD.STR.LSS", "GEO.TOP", "ARC.HIS.MOD.CRC"],
    "FIG.WRK.BUI.CAL": ["MAT.STM.MEC.ALP", "ARC.TAC.SOS.BRS", "MAT.ASM.FAC", "ARC.HIS.MOD.CPD"],
    "FIG.WRK.BUI.KRS": ["MAT.GLA.CWG", "MAT.ASM.FAC", "ARC.HIS.MOD.CPD", "ARC.THE.DPR.FRM"],
    "FIG.WRK.BUI.GHK": ["STR.SSS.MBF.DGF", "MAT.GLA.CWG", "ARC.MAT.STM.STL", "COM.APP.HIG"],
    "FIG.WRK.BUI.HAN": ["STR.SSS.MBF.DGF", "MAT.GLA.CWG", "ARC.MAT.STM.STL", "ARC.HER.ADM"],
    "FIG.WRK.BUI.MVA": ["CIV.BRG.CBS", "MAT.STM.STS.CBL", "MAT.STM.STS.STS", "ARC.BLD.STR.LSS"],
    "FIG.WRK.BUI.BMG": ["MAT.GLA.CWG", "ARC.MAT.STM.STL", "ARC.TAC.SOS.DAY", "ARC.BLD.STR.LSS"],
    "FIG.WRK.BUI.BRJ": ["STR.RCS.SWC.BTC", "ARC.BLD.STR.LST", "ARC.BLD.STR.WDL", "COM.APP.HIG"],
    "FIG.WRK.BUI.BRB": ["CIV.BRG.SUS", "MAT.STM.STS.CBL", "MAT.MST.NAS.SDS", "CIV.BRG.SPN"],
    "FIG.WRK.BUI.GGB": ["CIV.BRG.SUS", "MAT.STM.STS.CBL", "MAT.STM.STS.STS", "CIV.BRG.SPN"],
    "FIG.WRK.BUI.THV": ["MAT.MST.NAS.GRA", "ARC.DTS.PPT.PLM", "MAT.PRF.AES.TEX", "ARC.THE.DPR.CIR"],
    "FIG.WRK.BUI.BKF": ["MAT.CMA.CEM.CIP", "MAT.CMA.CEM.BFC", "ARC.TAC.SOS.DAY", "ARC.DTS.PPT.MMA"],
    "FIG.WRK.BUI.LAD": ["ARC.BLD.STR.DOM", "ARC.MAT.STM.STL", "ARC.TAC.SOS.DAY", "ARC.TAC.SOS.SHD"],
    "FIG.WRK.BUI.PCT": ["MAT.TBB.ENW.PPT", "MAT.TBB.ENW.PLY", "URB.RES.DRR", "CON.TMP"],
    "FIG.WRK.BUI.LYC": ["MAT.EAR.CEB", "MAT.PRF.ENV.LOC", "ARC.TAC.NVS.XVN", "ARC.TAC.SOS.SHD"],
    "FIG.WRK.BUI.LUY": ["MAT.MST.NAS.LIM", "MAT.MST.NAS.SDS", "ARC.HER.FAB", "ARC.HIS.MOD.CRC"],
    "FIG.WRK.BUI.SIK": ["MAT.MST.CLB", "ARC.HER.FAB", "SUS.RSC.MAT", "MAT.PRF.AES.TEX"],
    "FIG.WRK.BUI.HAK": ["URB.HOU", "ARC.URB.NHD", "ARC.THE.DPR.CIR", "ARC.SIT"],
    "FIG.WRK.BUI.AQA": ["ARC.BLD.STR.LSS", "ARC.MAT.STM.STL", "MAT.GLA.CWG", "ARC.DTS.PST.PDF"],
    "FIG.WRK.BUI.DDP": ["MAT.STM.MEC.ALP", "MAT.ASM.FAC", "ARC.HIS.MOD.CPD", "ARC.DTS.PST.PDF"],
    "FIG.WRK.BUI.NEM": ["ARC.HER.CIN", "ARC.HER.FAB", "MAT.MST.CLB", "MAT.MST.NAS.LIM"],
    "FIG.WRK.BUI.MNY": ["MAT.STM.MEC.RFS", "ARC.TAC.SOS.SHD", "ARC.TAC.NVS", "ARC.ECD.VEN"],
    "FIG.WRK.BUI.RLC": ["MAT.CMA.CEM.CIP", "ARC.THE.DPR.CIR", "ARC.TAC.SOS.DAY", "ARC.DTS.PST.PDF"],
    "FIG.WRK.BUI.TAU": ["MAT.CMA.CEM.CIP", "ARC.BLD.STR.ARS", "ARC.THE.DPR.CIR", "ARC.TAC.SOS.DAY"],
    "FIG.WRK.BUI.FVL": ["MAT.GLA.CWG", "ARC.MAT.STM.STL", "MAT.ASM.FAC", "ARC.HIS.MOD.CPD"],
    "FIG.WRK.BUI.DIS": ["MAT.STM.STS.STS", "ARC.INT.PAC.ACU", "ARC.HIS.MOD.DFS", "ARC.BLD.STR.STF"],
    "FIG.WRK.BUI.BEY": ["MAT.GLA.CWG", "ARC.TAC.SOS.DAY", "MAT.ASM.FAC", "ARC.THE.DPR.ORD"],
    "FIG.WRK.BUI.TJI": ["MAT.TBB.ENW.GLU", "ARC.TAC.NVS", "ARC.TAC.SOS.SHD", "ARC.HIS.MOD.CRC"],
    "FIG.WRK.BUI.SAC": ["ARC.MAT.STM.STL", "MAT.GLA.CWG", "ARC.BLD.SRV.UCO", "HIS.POC.HTA"],
    "FIG.WRK.BUI.GAR": ["ARC.MAT.STM.STL", "ARC.BLD.STR.ARS", "CIV.BRG.SPN", "MAT.STM.STS.STS"],
    "FIG.WRK.BUI.SWB": ["ARC.MAT.CON.RCC", "CIV.BRG.SPN", "ARC.BLD.STR.ARS", "MAT.CMA.CEM.CIP"],
    "FIG.WRK.BUI.ORL": ["ARC.MAT.CON.RCC", "ARC.BLD.STR.SHL", "STR.SYS.SPC", "MAT.CMA.CEM.PSC"],
    "FIG.WRK.BUI.MHL": ["MAT.TBB.ENW.GLU", "ARC.BLD.STR.LSS", "STR.SYS.SPC", "ARC.BLD.STR.TNS"],
    "FIG.WRK.BUI.LNE": ["MAT.STM.STS.CBL", "ARC.MAT.STM.STL", "ARC.BLD.STR.TNS", "CIV.BRG.SPN"],
    "FIG.WRK.BUI.CHS": ["ARC.MAT.CON.RCC", "ARC.BLD.STR.SHL", "ARC.HIS.SEA.PMP", "ARC.TAC.NVS"],
    "FIG.WRK.BUI.FEU": ["MAT.CMA.CEM.CIP", "ARC.HIS.SEA.ADP", "ARC.HIS.SEA.PMP", "ARC.DOC.DET"],
}
for work, facets in project_work_facets.items():
    sources = ENGINEERING_WORK_SOURCE_IDS if work in {"FIG.WRK.BUI.MVA", "FIG.WRK.BUI.BRJ", "FIG.WRK.BUI.BRB", "FIG.WRK.BUI.GGB"} else PROJECT_EVIDENCE_SOURCE_IDS
    for facet in facets:
        add_rel(work, "has_facet", facet, "work_material_system_movement", sources)

# Project-evidence material, system, movement, and LEA/ALE bridges.
for material in ["MAT.STM.STS.CBL", "MAT.TBB.ENW.PPT", "MAT.GLA.STG"]:
    add_rel(material, "has_facet", "MAT.PRF.AES.TEX", "material_property", PROJECT_EVIDENCE_SOURCE_IDS)
for material in ["MAT.STM.STS.CBL", "ARC.MAT.STM.STL", "MAT.STM.STS.STS"]:
    add_rel(material, "has_facet", "STR.SSS.TCM", "material_structural_component", ENGINEERING_WORK_SOURCE_IDS)
    add_rel(material, "has_facet", "ARC.BLD.STR.LSS", "material_structural_component", ENGINEERING_WORK_SOURCE_IDS)
add_rel("MAT.STM.STS.CBL", "has_facet", "ARC.BLD.STR.TNS", "material_structural_component", ENGINEERING_WORK_SOURCE_IDS)
add_rel("MAT.STM.STS.CBL", "has_facet", "CIV.BRG.SUS", "material_structural_component", ENGINEERING_WORK_SOURCE_IDS)
add_rel("MAT.STM.STS.CBL", "has_facet", "CIV.BRG.CBS", "material_structural_component", ENGINEERING_WORK_SOURCE_IDS)
add_rel("MAT.TBB.ENW.PPT", "has_facet", "CON.TMP", "material_method", PROJECT_EVIDENCE_SOURCE_IDS)
add_rel("MAT.TBB.ENW.PPT", "has_facet", "URB.RES.DRR", "lea_materials_methods", PROJECT_EVIDENCE_SOURCE_IDS)
add_rel("MAT.GLA.STG", "has_facet", "ARC.HIS.ANC.GOT", "movement_material_path", MATERIAL_SOURCE_IDS)
add_rel("MAT.GLA.STG", "has_facet", "MAT.PRF.THE.REF", "optical_property", MATERIAL_SOURCE_IDS)
for system in ["ARC.BLD.STR.FBU", "ARC.BLD.STR.RBV"]:
    add_rel("ARC.HIS.ANC.GOT", "has_facet", system, "movement_material_path", MATERIAL_SOURCE_IDS)
    add_rel("ARC.WAC.MSW.GRV", "has_facet", system, "movement_material_path", MATERIAL_SOURCE_IDS)
add_rel("ARC.HIS.ANC.GOT", "has_facet", "MAT.GLA.STG", "movement_material_path", MATERIAL_SOURCE_IDS)
add_rel("ARC.HIS.ANC.GOT", "has_facet", "MAT.MST.NAS.LIM", "movement_material_path", MATERIAL_SOURCE_IDS)
add_rel("ARC.HIS.ANC.RFB", "has_facet", "ARC.BLD.STR.DOM", "movement_material_path", MATERIAL_SOURCE_IDS)
add_rel("ARC.WAC.CIT.RCV", "has_facet", "ARC.BLD.STR.DOM", "movement_material_path", MATERIAL_SOURCE_IDS)
add_rel("HIS.MOA.BRS", "has_facet", "MAT.CMA.CEM.EXP", "movement_material_path", PROJECT_EVIDENCE_SOURCE_IDS)
add_rel("HIS.MOA.BRS", "has_facet", "ARC.HIS.MOD.BME", "movement_material_path", PROJECT_EVIDENCE_SOURCE_IDS)
add_rel("HIS.MOV.MOD", "has_facet", "ARC.MAT.STM.STL", "movement_material_path", PROJECT_EVIDENCE_SOURCE_IDS)
add_rel("HIS.MOV.MOD", "has_facet", "MAT.GLA.CWG", "movement_material_path", PROJECT_EVIDENCE_SOURCE_IDS)
add_rel("HIS.MOV.MOD", "has_facet", "ARC.MAT.CON.RCC", "movement_material_path", PROJECT_EVIDENCE_SOURCE_IDS)
add_rel("HIS.POC.HTA", "has_facet", "ARC.MAT.STM.STL", "movement_material_path", PROJECT_EVIDENCE_SOURCE_IDS)
add_rel("HIS.POC.HTA", "has_facet", "MAT.GLA.CWG", "movement_material_path", PROJECT_EVIDENCE_SOURCE_IDS)
add_rel("HIS.POC.HTA", "has_facet", "ARC.BLD.SRV.UCO", "movement_material_path", PROJECT_EVIDENCE_SOURCE_IDS)
add_rel("ARC.HIS.SEA.TMS", "has_facet", "ARC.TAC.SOS.BRS", "tropical_materials", NCCA_SOURCE_IDS + MATERIAL_SOURCE_IDS)
add_rel("ARC.HIS.SEA.TMS", "has_facet", "ARC.TAC.NVS.XVN", "tropical_materials", NCCA_SOURCE_IDS + MATERIAL_SOURCE_IDS)
add_rel("ARC.HIS.SEA.TMS", "has_facet", "MAT.CMA.CEM.CIP", "tropical_materials", NCCA_SOURCE_IDS + MATERIAL_SOURCE_IDS)
add_rel("ARC.HIS.MOD.MIN", "has_facet", "MAT.CMA.CEM.EXP", "movement_material_path", PROJECT_EVIDENCE_SOURCE_IDS)
add_rel("ARC.HIS.MOD.MIN", "has_facet", "ARC.DTS.PPT.PLM", "theory_materiality_path", PROJECT_EVIDENCE_SOURCE_IDS)
add_rel("ARC.HIS.MOD.MIN", "has_facet", "MAT.MST.NAS.MAR", "movement_material_path", PROJECT_EVIDENCE_SOURCE_IDS)

# Engineer/system bridges without direct person-material shortcuts.
for person, systems in {
    "FIG.ETS.STE.CAL": ["CIV.BRG", "ARC.BLD.STR.TNS", "ARC.BLD.STR.LSS"],
    "FIG.ETS.STE.KHN": ["ARC.BLD.STR.STF", "STR.SSS.MBF", "STR.SYS.FRM"],
    "FIG.ETS.STE.NRV": ["ARC.BLD.STR.SHL", "ARC.MAT.CON.RCC", "STR.RCS.SBC"],
    "FIG.ETS.STE.MAI": ["CIV.BRG", "ARC.BLD.STR.ARS", "ARC.MAT.CON.RCC"],
    "FIG.ETS.STE.EIF": ["ARC.BLD.STR.LSS", "MAT.STM.STS.STS", "CIV.BRG"],
    "FIG.ETS.STE.CAN": ["ARC.BLD.STR.SHL", "ARC.MAT.CON.RCC", "STR.SYS.SPC"],
    "FIG.ETS.STE.TOR": ["ARC.BLD.STR.SHL", "ARC.MAT.CON.RCC", "STR.SYS.SPC"],
    "FIG.ARD.CAA.FOT": ["ARC.BLD.STR.TNS", "STR.SYS.SPC", "MAT.PRF.MEC.TEN"],
    "FIG.ETS.STE.DIE": ["MAT.MST.CLB", "ARC.BLD.STR.SHL", "ARC.HIS.MOD.CRC"],
    "FIG.ETS.STE.FUL": ["ARC.BLD.STR.LSS", "ARC.DTS.PST.PDF", "STR.SYS.SPC"],
}.items():
    for system in systems:
        # These are person-to-system/concept anchors. Avoid person-to-material edges except where the target is an existing structural system concept or role.
        if system.startswith("MAT") or system.startswith("ARC.MAT"):
            continue
        add_rel(person, "has_facet", system, "person_structure_system", PEOPLE_SOURCE_IDS)

# LEA/ALE cross-subject links involving materials, structures, history, theory, construction, and practice.
for material in ["MAT.CMA.CEM.CHB", "MAT.FIP.FLF.CER", "MAT.FIP.FLF.POR", "MAT.MEM.RME.WPM", "MAT.FIP.WAF.GYB", "MAT.FIP.WAF.FCB", "MAT.GLA.TPG"]:
    add_rel("ARC.MAT", "has_facet", material, "lea_materials_methods")
    add_rel(material, "has_facet", "CON.DMC.DBB.BID", "specification_contract_path")
add_rel("MAT.ASM.WET", "requires", "LAW.SCP.MPF.TOI", "sanitation_material_path")
add_rel("MAT.ASM.WET", "requires", "LAW.PAL.ACR.ATO", "accessibility_material_path")
add_rel("MAT.ASM.FRW", "constrains", "LAW.PFC.EPE.FST", "fire_material_path")
add_rel("MAT.ASM.CEI", "requires", "ARC.BLD.SRV.RCP", "ceiling_utilities_path")
add_rel("MAT.ASM.CUR", "requires", "ARC.TAC.SOS.DAY", "glazing_daylight_path")
add_rel("MAT.ASM.CUR", "constrains", "ARC.TAC.SOS.SHD", "glazing_solar_path")
add_rel("MAT.PRF.ENV.EBC", "has_facet", "SUS.CAR.LCA", "sustainability_material_path")
add_rel("MAT.PRF.MOI.MRS", "constrains", "ARC.TAC.MMR", "tropical_moisture_path")
add_rel("MAT.PRF.ACO.ABS", "requires", "ARC.INT.PAC.ACU", "interiors_acoustic_path")
add_rel("MAT.PRF.AES.SLP", "constrains", "LAW.PAL.ACR.ARS", "accessibility_finish_path")

PHILIPPINE_PERSON_WORK_EDGES = [
    ("FIG.ARD.CAA.LOC", "FIG.WRK.BUI.CCP"),
    ("FIG.ARD.CAA.LOC", "FIG.WRK.BUI.PIC"),
    ("FIG.ARD.CAA.LOC", "FIG.WRK.BUI.FHA"),
    ("FIG.ARD.CAA.LOC", "FIG.WRK.BUI.CHS"),
    ("FIG.ARD.CAA.LOC", "FIG.WRK.BUI.IHM"),
    ("FIG.ARD.CAA.NAK", "FIG.WRK.BUI.UST"),
    ("FIG.ARD.CAA.NAK", "FIG.WRK.BUI.RIZ"),
    ("FIG.ARD.CAA.NAK", "FIG.WRK.BUI.CAP"),
    ("FIG.ARD.CAA.NAK", "FIG.WRK.BUI.MJC"),
    ("FIG.ARD.CAA.NAK", "FIG.WRK.BUI.RUF"),
    ("FIG.ARD.CAA.NAK", "FIG.WRK.BUI.PVH"),
    ("FIG.ARD.CAA.ANT", "FIG.WRK.BUI.FEU"),
    ("FIG.ARD.CAA.ANT", "FIG.WRK.BUI.IDL"),
    ("FIG.ARD.CAA.ANT", "FIG.WRK.BUI.LYR"),
    ("FIG.ARD.CAA.ANT", "FIG.WRK.BUI.GLX"),
    ("FIG.ARD.CAA.ANT", "FIG.WRK.BUI.MPC"),
    ("FIG.ARD.CAA.SAN", "FIG.WRK.BUI.MCC"),
    ("FIG.ARD.CAA.SAN", "FIG.WRK.BUI.PAP"),
    ("FIG.ARD.CAA.SAN", "FIG.WRK.BUI.LMP"),
    ("FIG.ARD.CAA.SAN", "FIG.WRK.BUI.THR"),
    ("FIG.ARD.CAA.MAN", "FIG.WRK.BUI.COC"),
    ("FIG.ARD.CAA.MAN", "FIG.WRK.BUI.SMB"),
    ("FIG.ARD.CAA.MAN", "FIG.WRK.BUI.BHT"),
    ("FIG.ARD.CAA.MAN", "FIG.WRK.BUI.OLP"),
    ("FIG.ARD.CAA.MAN", "FIG.WRK.BUI.PFR"),
    ("FIG.ARD.CAA.MAN", "FIG.WRK.BUI.AMN"),
    ("FIG.ARD.CAA.ZAR", "FIG.WRK.BUI.SDC"),
    ("FIG.ARD.CAA.ZAR", "FIG.WRK.BUI.MER"),
    ("FIG.ARD.CAA.ZAR", "FIG.WRK.BUI.DBC"),
    ("FIG.ARD.CAA.ZAR", "FIG.WRK.BUI.PXC"),
    ("FIG.ARD.CAA.ZAR", "FIG.WRK.BUI.VSM"),
    ("FIG.ARD.CAA.ZAR", "FIG.WRK.BUI.CMC"),
    ("FIG.ARD.CAA.ARE", "FIG.WRK.BUI.MTH"),
    ("FIG.ARD.CAA.ARE", "FIG.WRK.BUI.OLB"),
    ("FIG.ARD.CAA.AAC", "FIG.WRK.BUI.MTH"),
    ("FIG.ARD.CAA.CON", "FIG.WRK.BUI.QZH"),
    ("FIG.ARD.CAA.ILU", "FIG.WRK.BUI.QMS"),
]
for person, work in PHILIPPINE_PERSON_WORK_EDGES:
    add_rel(person, "has_facet", work, "filipino_architect_work", PHILIPPINE_ARCHITECTURE_SOURCE_IDS)

for person in [
    "FIG.ARD.CAA.LOC", "FIG.ARD.CAA.NAK", "FIG.ARD.CAA.ANT", "FIG.ARD.CAA.MAN",
    "FIG.ARD.CAA.ZAR", "FIG.ARD.CAA.ARE", "FIG.ARD.CAA.MAP", "FIG.ARD.CAA.AAC",
    "FIG.ARD.CAA.CON", "FIG.ARD.CAA.ARG", "FIG.ARD.CAA.COS", "FIG.ARD.CAA.FOR",
    "FIG.ARD.CAA.MEN", "FIG.ARD.CAA.LUN", "FIG.ARD.CAA.ILU",
]:
    add_rel(person, "has_facet", "FIG.PTE.ROL.ARC", "person_role", PHILIPPINE_ARCHITECTURE_SOURCE_IDS)
    add_rel(person, "has_facet", "FIG.PTE.NAT.PHL", "person_nationality", PHILIPPINE_ARCHITECTURE_SOURCE_IDS)
for person in ["FIG.ARD.CAA.LOC", "FIG.ARD.CAA.NAK", "FIG.ARD.CAA.ANT", "FIG.ARD.CAA.SAN", "FIG.ARD.CAA.MAN", "FIG.ARD.CAA.ZAR"]:
    add_rel(person, "has_facet", "FIG.PTE.ROL.NAA", "person_role", PHILIPPINE_ARCHITECTURE_SOURCE_IDS)
add_rel("FIG.ARD.CAA.SAN", "has_facet", "FIG.PTE.ROL.LAR", "person_role", PHILIPPINE_ARCHITECTURE_SOURCE_IDS)

PHILIPPINE_WORK_FACETS = {
    "FIG.WRK.BUI.MTH": ["ARC.HIS.SEA.ADP", "HIS.GHA.CTS", "ARC.HER", "ARC.CHC", "MAT.CMA.CEM.CIP", "MAT.GLA.STG", "HIS.BEC.COS"],
    "FIG.WRK.BUI.OLB": ["ARC.WAC.MCT.NCO", "ARC.BTY.CIV", "ARC.HER", "ARC.CHC", "MAT.MST.NAS.LIM", "MAT.MST.CLB"],
    "FIG.WRK.BUI.QZH": ["ARC.BTY.CIV", "ARC.SIT", "URB.PBR.CIV", "ARC.HIS.SEA.ACC", "ARC.HIS.SEA.PMP"],
    "FIG.WRK.BUI.QMS": ["ARC.BTY.CIV", "URB.PBR.CIV", "ARC.HIS.SEA.ACC", "ARC.HIS.MOD.NEO", "ARC.SIT"],
    "FIG.WRK.BUI.MCC": ["ARC.SIT", "URB.PBR", "ARC.SIT.LAN", "ARC.TAC.NVS", "ARC.HIS.SEA.PMP"],
    "FIG.WRK.BUI.PAP": ["ARC.HER.ADM", "ARC.CHC", "URB.PBR", "ARC.SIT", "HRC"],
    "FIG.WRK.BUI.SDC": ["ARC.MAT.CON.RCC", "MAT.CMA.CEM.CIP", "ARC.HIS.SEA.PMP", "HIS.BEC.RCT", "ARC.BLD.STR.LSS", "ARC.THE.DPR.CIR"],
    "FIG.WRK.BUI.SMB": ["ARC.HIS.SEA.CPA", "ARC.HIS.SEA.PVA", "ARC.TAC", "MAT.TBB.BAS.BCM", "MAT.TBB.BAS.CAP", "HIS.BEC.COS"],
    "FIG.WRK.BUI.BHT": ["ARC.HIS.SEA.BKS", "ARC.HIS.SEA.PVA", "MAT.TBB.BAS.BCM", "MAT.TBB.BAS.NIP", "ARC.TAC.NVS", "SUS.ENE.PDE"],
    "FIG.WRK.BUI.OLP": ["ARC.BTY.CIV", "HIS.BEC.RCT", "ARC.HIS.SEA.CPA", "ARC.TAC.NVS", "URB.PBR.CIV"],
    "FIG.WRK.BUI.MER": ["ARC.MAT.CON.RCC", "MAT.CMA.CEM.CIP", "ARC.HIS.SEA.PMP", "ARC.BTY.CIV", "MAT.ASM.FAC"],
    "FIG.WRK.BUI.IHM": ["ARC.MAT.CON.RCC", "ARC.BLD.STR.SHL", "ARC.TAC.SOS.DAY", "HIS.BEC.RCT", "ARC.HIS.SEA.PMP"],
    "FIG.WRK.BUI.RIZ": ["HIS.GHA.CTS", "ARC.HIS.SEA.PMP", "ARC.BTY.CIV", "ARC.HER", "MAT.CMA.CEM.CIP"],
    "FIG.WRK.BUI.IDL": ["HIS.GHA.CTS", "ARC.HIS.SEA.ADP", "ARC.HIS.SEA.PMP", "MAT.CMA.CEM.CIP"],
    "FIG.WRK.BUI.LYR": ["HIS.GHA.CTS", "ARC.HIS.SEA.ADP", "ARC.HIS.SEA.PMP", "MAT.CMA.CEM.CIP"],
    "FIG.WRK.BUI.GLX": ["HIS.GHA.CTS", "ARC.HIS.SEA.PMP", "ARC.BTY.CIV", "MAT.CMA.CEM.CIP"],
    "FIG.WRK.BUI.MPC": ["ARC.BTY.CIV", "ARC.SIT", "ARC.TAC.NVS", "ARC.HIS.SEA.PMP"],
    "FIG.WRK.BUI.CAP": ["HIS.GHA.CTS", "ARC.HIS.SEA.PMP", "ARC.BTY.CIV", "MAT.CMA.CEM.CIP"],
    "FIG.WRK.BUI.MJC": ["ARC.BTY.CIV", "ARC.SIT", "HIS.GHA.CTS", "ARC.HIS.SEA.PMP"],
    "FIG.WRK.BUI.RUF": ["ARC.BTY.CIV", "MAT.ASM.FAC", "ARC.HIS.SEA.PMP", "ARC.MAT.CON.RCC"],
    "FIG.WRK.BUI.PVH": ["ARC.TAC", "ARC.SIT", "ARC.HIS.SEA.CPA", "MAT.ASM.FAC"],
    "FIG.WRK.BUI.DBC": ["HIS.BEC.RCT", "ARC.HIS.SEA.PMP", "ARC.MAT.CON.RCC", "MAT.CMA.CEM.CIP"],
    "FIG.WRK.BUI.PXC": ["ARC.BTY.CIV", "HIS.BEC.RCT", "ARC.HIS.SEA.PMP", "MAT.ASM.FAC"],
    "FIG.WRK.BUI.VSM": ["ARC.BTY.CIV", "HIS.BEC.RCT", "ARC.HIS.SEA.PMP", "ARC.CHC"],
    "FIG.WRK.BUI.CMC": ["HIS.BEC.RCT", "ARC.CHC", "ARC.HIS.SEA.SCC", "ARC.HER"],
    "FIG.WRK.BUI.PFR": ["ARC.TAC", "ARC.SIT", "ARC.HIS.SEA.CPA", "MAT.TBB.BAS.BCM", "MAT.TBB.DIL.HDW"],
    "FIG.WRK.BUI.AMN": ["ARC.TAC", "ARC.SIT", "ARC.HIS.SEA.CPA", "MAT.TBB.DIL.HDW", "SUS.ENE.PDE"],
    "FIG.WRK.BUI.LMP": ["ARC.SIT.LAN", "ARC.CHC.CLC", "HRC.LAN", "URB.PBR"],
    "FIG.WRK.BUI.THR": ["ARC.SIT.LAN", "ARC.TAC", "ARC.SIT", "URB.PBR"],
    "FIG.WRK.BUI.BKB": ["ARC.HIS.SEA.BKS", "ARC.HIS.SEA.PVA", "MAT.TBB.BAS.BCM", "MAT.TBB.BAS.NIP", "MAT.TBB.DIL.HDW", "ARC.TAC.NVS", "SUS.ENE.PDE"],
    "FIG.WRK.BUI.BNB": ["ARC.HIS.SEA.BNB", "ARC.HIS.SEA.SCC", "MAT.TBB.BAS.CAP", "MAT.TBB.DIL.HDW", "MAT.MST.NAS.LIM", "ARC.TAC.NVS", "ARC.HER"],
    "FIG.WRK.BUI.TRG": ["ARC.HIS.SEA.TRG", "ARC.HIS.SEA.PVA", "MAT.TBB.DIL.HDW", "ARC.CHC", "HIS.BEC.COS"],
    "FIG.WRK.BUI.IVT": ["ARC.HIS.SEA.IVT", "MAT.MST.NAS.LIM", "MAT.MST.CLB", "ARC.TAC", "STR.WSD", "ARC.HER"],
    "FIG.WRK.BUI.IFB": ["ARC.HIS.SEA.IFB", "MAT.TBB.DIL.HDW", "ARC.HIS.SEA.PVA", "ARC.TAC.NVS", "ARC.CHC.CLC"],
}
for work, facets in PHILIPPINE_WORK_FACETS.items():
    for facet in facets:
        add_rel(work, "has_facet", facet, "work_material_system_movement", PHILIPPINE_ARCHITECTURE_SOURCE_IDS)

PHILIPPINE_CONCEPT_BRIDGES = [
    ("ARC.HIS.SEA.PVA", "FIG.WRK.BUI.BKB"),
    ("ARC.HIS.SEA.PVA", "FIG.WRK.BUI.BNB"),
    ("ARC.HIS.SEA.PVA", "FIG.WRK.BUI.TRG"),
    ("ARC.HIS.SEA.PVA", "FIG.WRK.BUI.IVT"),
    ("ARC.HIS.SEA.PVA", "FIG.WRK.BUI.IFB"),
    ("ARC.HIS.SEA.BKS", "FIG.WRK.BUI.BKB"),
    ("ARC.HIS.SEA.BNB", "FIG.WRK.BUI.BNB"),
    ("ARC.HIS.SEA.TRG", "FIG.WRK.BUI.TRG"),
    ("ARC.HIS.SEA.IVT", "FIG.WRK.BUI.IVT"),
    ("ARC.HIS.SEA.IFB", "FIG.WRK.BUI.IFB"),
    ("ARC.TAC", "FIG.WRK.BUI.BKB"),
    ("ARC.TAC", "FIG.WRK.BUI.BNB"),
    ("ARC.TAC", "FIG.WRK.BUI.BHT"),
    ("ARC.HIS.SEA.PMP", "FIG.WRK.BUI.CHS"),
    ("ARC.HIS.SEA.PMP", "FIG.WRK.BUI.CCP"),
    ("ARC.HIS.SEA.PMP", "FIG.WRK.BUI.PIC"),
    ("ARC.HIS.SEA.PMP", "FIG.WRK.BUI.SDC"),
    ("ARC.HIS.SEA.ADP", "FIG.WRK.BUI.MTH"),
    ("ARC.HIS.SEA.ADP", "FIG.WRK.BUI.FEU"),
    ("ARC.HIS.SEA.CPA", "FIG.WRK.BUI.COC"),
    ("ARC.HIS.SEA.CPA", "FIG.WRK.BUI.SMB"),
    ("ARC.CHC", "FIG.WRK.BUI.MTH"),
    ("ARC.CHC", "FIG.WRK.BUI.OLB"),
    ("ARC.CHC", "FIG.WRK.BUI.TRG"),
    ("ARC.CHC", "FIG.WRK.BUI.IVT"),
]
for concept, work in PHILIPPINE_CONCEPT_BRIDGES:
    add_rel(concept, "has_facet", work, "philippine_architecture_bridge", PHILIPPINE_ARCHITECTURE_SOURCE_IDS)

PHILIPPINE_MATERIAL_BRIDGES = [
    ("MAT.TBB.BAS.BCM", "FIG.WRK.BUI.BKB"),
    ("MAT.TBB.BAS.BCM", "FIG.WRK.BUI.BHT"),
    ("MAT.TBB.BAS.NIP", "FIG.WRK.BUI.BKB"),
    ("MAT.TBB.BAS.CAP", "FIG.WRK.BUI.BNB"),
    ("MAT.TBB.BAS.CAP", "FIG.WRK.BUI.COC"),
    ("MAT.TBB.DIL.HDW", "FIG.WRK.BUI.BNB"),
    ("MAT.TBB.DIL.HDW", "FIG.WRK.BUI.TRG"),
    ("MAT.TBB.DIL.HDW", "FIG.WRK.BUI.IFB"),
    ("MAT.MST.NAS.LIM", "FIG.WRK.BUI.IVT"),
    ("MAT.MST.NAS.LIM", "FIG.WRK.BUI.OLB"),
    ("ARC.MAT.CON.RCC", "FIG.WRK.BUI.CHS"),
    ("ARC.MAT.CON.RCC", "FIG.WRK.BUI.SDC"),
    ("MAT.CMA.CEM.CIP", "FIG.WRK.BUI.MTH"),
    ("MAT.CMA.CEM.CIP", "FIG.WRK.BUI.MER"),
]
for material, work in PHILIPPINE_MATERIAL_BRIDGES:
    add_rel(material, "has_facet", work, "philippine_material_work_path", PHILIPPINE_ARCHITECTURE_SOURCE_IDS)

RESOLVER_CASE_SPECS: list[dict[str, Any]] = [
    {"case_id": "ARCH-INT-001", "text": "Who are architects that are also engineers?", "asset_context": "architect_engineer_people", "concept_path": "FIG.PTE.ROL.AEN", "path_refs": [("FIG.ETS.STE.CAL", "architect_engineer"), ("FIG.ARD.CAA.FOT", "engineer_architect"), ("FIG.ETS.STE.NRV", "engineer_architect")], "source_evidence": PEOPLE_SOURCE_IDS, "result_type": "single_value", "confidence": "deterministic", "rationale": "Architect-engineer role facets return people whose graph paths connect architectural and structural thinking.", "fallback_reason": "exact_architect_engineer_role_match", "context_paths": ["FIG.PTE.ROL.AEN", "FIG.ETS.STE"]},
    {"case_id": "ARCH-INT-002", "text": "Which people connect architecture and structural engineering?", "asset_context": "architecture_structural_people", "concept_path": "FIG.ETS.STE.CAL", "path_refs": [("FIG.ETS.STE.CAL", "bridge_architect_engineer"), ("FIG.ETS.STE.KHN", "high_rise_structural_engineer"), ("FIG.ETS.STE.NRV", "concrete_shell_engineer")], "source_evidence": PEOPLE_SOURCE_IDS, "result_type": "single_value", "confidence": "deterministic", "rationale": "Person-role and person-system facets expose people who bridge architectural expression and structural systems.", "fallback_reason": "exact_people_structure_path_match", "context_paths": ["FIG.ETS.STE", "ARC.BLD.STR"]},
    {"case_id": "ARCH-INT-003", "text": "Which Pritzker laureates are connected to concrete through specific works?", "asset_context": "pritzker_concrete_work_paths", "concept_path": "FIG.AWD.PRI.PZK", "path_refs": [("FIG.ARD.CAA.AND", "pritzker_laureate"), ("FIG.WRK.BUI.CHL", "work_anchor"), ("MAT.CMA.CEM.EXP", "exposed_concrete")], "source_evidence": ["SRC-PRITZKER-LAUREATES-OFFICIAL", "SRC-WIKIDATA-CC0-AEC-IDENTIFIERS"], "result_type": "composed", "confidence": "deterministic", "rationale": "Award, person, work, and material facets compose a safe metadata-only path rather than a generic person-to-material edge.", "fallback_reason": "composed_pritzker_work_material_path", "context_paths": ["FIG.AWD.PRI.PZK", "MAT.CMA.CEM.EXP"]},
    {"case_id": "ARCH-INT-004", "text": "Which architects are associated with exposed concrete?", "asset_context": "exposed_concrete_architects", "concept_path": "MAT.CMA.CEM.EXP", "path_refs": [("FIG.ARD.CAA.AND", "architect"), ("FIG.WRK.BUI.CHL", "work_anchor"), ("MAT.CMA.CEM.EXP", "exposed_concrete")], "source_evidence": PEOPLE_SOURCE_IDS, "result_type": "composed", "confidence": "deterministic", "rationale": "The answer is resolved through architect-work-material paths, not direct unsupported person-material links.", "fallback_reason": "composed_work_material_anchor_path", "context_paths": ["FIG.ARD.CAA", "MAT.CMA.CEM"]},
    {"case_id": "ARCH-INT-005", "text": "Which materials connect to tropical design?", "asset_context": "tropical_materials", "concept_path": "ARC.TAC", "path_refs": [("MAT.TBB.BAS.BCM", "bamboo"), ("MAT.TBB.BAS.NIP", "nipa"), ("MAT.TBB.BAS.CAP", "capiz")], "source_evidence": ["SRC-NCCA-PHILIPPINE-BUILT-HERITAGE-METADATA", "SRC-GETTY-VOCABULARIES-AAT-ULAN-TGN"], "result_type": "single_value", "confidence": "deterministic", "rationale": "Tropical and Philippine vernacular material facets provide study paths from climate response to material assemblies.", "fallback_reason": "exact_tropical_material_path_match", "context_paths": ["ARC.TAC", "ARC.HIS.SEA.PVA"]},
    {"case_id": "ARCH-INT-006", "text": "Which materials connect to Philippine vernacular architecture?", "asset_context": "philippine_vernacular_materials", "concept_path": "ARC.HIS.SEA.PVA", "path_refs": [("MAT.TBB.BAS.BCM", "bamboo"), ("MAT.TBB.BAS.NIP", "nipa"), ("MAT.TBB.BAS.CAP", "capiz")], "source_evidence": NCCA_SOURCE_IDS, "result_type": "single_value", "confidence": "deterministic", "rationale": "Philippine vernacular nodes connect to safe material-topic metadata and tropical-design concepts.", "fallback_reason": "exact_philippine_vernacular_material_path_match", "context_paths": ["ARC.HIS.SEA.PVA"]},
    {"case_id": "ARCH-INT-007", "text": "Which materials are used in wet areas?", "asset_context": "wet_area_materials", "concept_path": "MAT.ASM.WET", "path_refs": [("MAT.FIP.FLF.CER", "ceramic_tile"), ("MAT.FIP.FLF.POR", "porcelain_tile"), ("MAT.MEM.RME.WPM", "waterproofing_membrane")], "source_evidence": MATERIAL_SOURCE_IDS, "result_type": "single_value", "confidence": "deterministic", "rationale": "Wet-area assembly facets connect finish materials, waterproofing, sanitation, and accessibility without copying code tables.", "fallback_reason": "exact_wet_area_assembly_path_match", "context_paths": ["MAT.ASM.WET"]},
    {"case_id": "ARCH-INT-008", "text": "How does concrete connect to slabs beams columns foundations and formwork?", "asset_context": "concrete_structural_components", "concept_path": "ARC.MAT.CON.RCC", "path_refs": [("ARC.MAT.CON.RCC", "reinforced_concrete"), ("ARC.BLD.STR.SLB", "slab"), ("ARC.BLD.STR.BEM", "beam"), ("ARC.BLD.STR.COL", "column"), ("CON.TMP.FOR", "formwork")], "source_evidence": MATERIAL_SOURCE_IDS, "result_type": "single_value", "confidence": "deterministic", "rationale": "Concrete connects through existing structural concept nodes and formwork requirements.", "fallback_reason": "exact_concrete_structural_path_match", "context_paths": ["ARC.MAT.CON", "ARC.BLD.STR"]},
    {"case_id": "ARCH-INT-009", "text": "How does timber connect to vernacular architecture roof framing interiors and sustainability?", "asset_context": "timber_vernacular_sustainability", "concept_path": "MAT.TBB", "path_refs": [("MAT.TBB.DIL.HDW", "hardwood"), ("MAT.TBB.ENW.GLU", "glulam"), ("ARC.HIS.SEA.PVA", "philippine_vernacular"), ("MAT.PRF.ENV.EBC", "embodied_carbon")], "source_evidence": MATERIAL_SOURCE_IDS + NCCA_SOURCE_IDS, "result_type": "composed", "confidence": "deterministic", "rationale": "Timber and bio-based material families compose paths through vernacular context and sustainability properties.", "fallback_reason": "composed_timber_vernacular_sustainability_path", "context_paths": ["MAT.TBB", "ARC.HIS.SEA.PVA", "SUS"]},
    {"case_id": "ARCH-INT-010", "text": "How do tiles connect to flooring wall finishes toilets kitchens wet areas and specifications?", "asset_context": "tile_wet_area_specifications", "concept_path": "MAT.FIP.FLF.CER", "path_refs": [("MAT.FIP.FLF.CER", "ceramic_tile"), ("MAT.ASM.WET", "wet_area"), ("LAW.SCP.MPF.TOI", "toilet_sanitation"), ("CON.DMC.DBB.BID", "specifications")], "source_evidence": MATERIAL_SOURCE_IDS, "result_type": "composed", "confidence": "deterministic", "rationale": "Tile material nodes bridge finishes, wet-area assemblies, sanitation/accessibility concerns, and contract-document specification paths.", "fallback_reason": "composed_tile_specification_path", "context_paths": ["MAT.FIP.FLF", "CON.DMC.DBB"]},
    {"case_id": "ARCH-INT-011", "text": "How does glass connect to daylighting curtain walls windows and thermal performance?", "asset_context": "glass_daylighting_envelope", "concept_path": "MAT.GLA.CWG", "path_refs": [("MAT.GLA.CWG", "curtain_wall_glazing"), ("MAT.ASM.CUR", "curtain_wall_assembly"), ("ARC.TAC.SOS.DAY", "daylighting"), ("MAT.PRF.THE.REF", "solar_reflectance")], "source_evidence": MATERIAL_SOURCE_IDS, "result_type": "composed", "confidence": "deterministic", "rationale": "Glazing paths connect material type, facade assembly, daylighting, and thermal/optical performance.", "fallback_reason": "composed_glass_envelope_path", "context_paths": ["MAT.GLA", "ARC.ENV"]},
    {"case_id": "ARCH-INT-012", "text": "Which architects or engineers are connected to tensile structures?", "asset_context": "tensile_structure_people", "concept_path": "ARC.BLD.STR.TNS", "path_refs": [("FIG.ARD.CAA.FOT", "tensile_structure_person"), ("FIG.ETS.STE.CAL", "bridge_tensile_system"), ("FIG.WRK.BUI.MOS", "work_anchor")], "source_evidence": PEOPLE_SOURCE_IDS, "result_type": "single_value", "confidence": "deterministic", "rationale": "Tensile-structure people are surfaced through role and work/system anchors.", "fallback_reason": "exact_tensile_people_path_match", "context_paths": ["ARC.BLD.STR.TNS", "FIG"]},
    {"case_id": "ARCH-INT-013", "text": "Which engineers are associated with reinforced concrete or shell structures?", "asset_context": "engineers_concrete_shells", "concept_path": "ARC.BLD.STR.SHL", "path_refs": [("FIG.ETS.STE.NRV", "concrete_shell_engineer"), ("FIG.ETS.STE.CAN", "thin_shell_engineer"), ("FIG.ETS.STE.TOR", "shell_engineer")], "source_evidence": PEOPLE_SOURCE_IDS, "result_type": "single_value", "confidence": "deterministic", "rationale": "Engineer-system paths identify concrete and shell structure specialists using work/system anchors.", "fallback_reason": "exact_engineer_shell_path_match", "context_paths": ["FIG.ETS.STE", "ARC.BLD.STR.SHL"]},
    {"case_id": "ARCH-INT-014", "text": "Which movements are strongly connected to specific materials?", "asset_context": "movement_materials", "concept_path": "ARC.HIS.MOD.BME", "path_refs": [("ARC.HIS.MOD.BME", "brutalist_material_expression"), ("MAT.CMA.CEM.EXP", "exposed_concrete"), ("ARC.HIS.MOD.ISC", "steel_glass_modernism")], "source_evidence": MATERIAL_SOURCE_IDS, "result_type": "composed", "confidence": "deterministic", "rationale": "Movement-material paths are modeled through movement nodes and material/property facets, not generic history edges.", "fallback_reason": "composed_movement_material_path", "context_paths": ["ARC.HIS.MOD", "MAT"]},
    {"case_id": "ARCH-INT-015", "text": "How do material choices connect to fire safety acoustics sustainability and specifications?", "asset_context": "material_performance_specifications", "concept_path": "MAT.PRF", "path_refs": [("MAT.PRF.FIR.FIR", "fire_resistance"), ("MAT.PRF.ACO.ABS", "acoustic_absorption"), ("MAT.PRF.ENV.EBC", "embodied_carbon"), ("CON.DMC.DBB.BID", "specification_document")], "source_evidence": MATERIAL_SOURCE_IDS, "result_type": "composed", "confidence": "deterministic", "rationale": "Material-performance facets connect choices to life safety, acoustics, sustainability, and specification paths.", "fallback_reason": "composed_material_performance_spec_path", "context_paths": ["MAT.PRF", "CON.DMC.DBB"]},
    {"case_id": "ARCH-INT-016", "text": "What graph path connects Zaha Hadid to concrete?", "asset_context": "zaha_concrete_path", "concept_path": "FIG.ARD.CAA.HAD", "path_refs": [("FIG.ARD.CAA.HAD", "architect"), ("FIG.WRK.BUI.VFS", "work_anchor"), ("MAT.CMA.CEM.CIP", "cast_in_place_concrete")], "source_evidence": PEOPLE_SOURCE_IDS, "result_type": "composed", "confidence": "deterministic", "rationale": "The graph resolves Zaha Hadid to concrete through specific work anchors, avoiding unsupported direct person-material edges.", "fallback_reason": "composed_zaha_work_material_path", "context_paths": ["FIG.ARD.CAA.HAD", "MAT.CMA.CEM"]},
    {"case_id": "ARCH-INT-017", "text": "What graph path connects Santiago Calatrava to architecture and engineering?", "asset_context": "calatrava_architecture_engineering_path", "concept_path": "FIG.ETS.STE.CAL", "path_refs": [("FIG.ETS.STE.CAL", "person"), ("FIG.PTE.ROL.ARC", "architect_role"), ("FIG.PTE.ROL.SEN", "engineer_role"), ("CIV.BRG", "bridge_domain")], "source_evidence": PEOPLE_SOURCE_IDS, "result_type": "single_value", "confidence": "deterministic", "rationale": "Role facets and bridge/structural-system paths connect Calatrava to both architecture and engineering.", "fallback_reason": "exact_calatrava_role_path_match", "context_paths": ["FIG.ETS.STE.CAL"]},
    {"case_id": "ARCH-INT-018", "text": "What graph path connects Pritzker laureates to materials and structural systems?", "asset_context": "pritzker_material_system_paths", "concept_path": "FIG.AWD.PRI.PZK", "path_refs": [("FIG.AWD.PRI.PZK", "award"), ("FIG.ARD.CAA.FOT", "laureate"), ("FIG.WRK.BUI.MOS", "work"), ("ARC.BLD.STR.TNS", "structural_system")], "source_evidence": ["SRC-PRITZKER-LAUREATES-OFFICIAL"], "result_type": "composed", "confidence": "deterministic", "rationale": "Pritzker status connects to material and structural systems through laureate and work anchors.", "fallback_reason": "composed_pritzker_system_path", "context_paths": ["FIG.AWD.PRI.PZK", "ARC.BLD.STR"]},
    {"case_id": "ARCH-INT-019", "text": "What graph path connects Philippine vernacular architecture to bamboo nipa timber and tropical design?", "asset_context": "philippine_vernacular_tropical_material_path", "concept_path": "ARC.HIS.SEA.PVA", "path_refs": [("ARC.HIS.SEA.PVA", "vernacular"), ("MAT.TBB.BAS.BCM", "bamboo"), ("MAT.TBB.BAS.NIP", "nipa"), ("ARC.TAC", "tropical_design")], "source_evidence": NCCA_SOURCE_IDS, "result_type": "composed", "confidence": "deterministic", "rationale": "Philippine vernacular, local materials, and tropical design compose a learner-facing study path.", "fallback_reason": "composed_philippine_vernacular_material_path", "context_paths": ["ARC.HIS.SEA.PVA", "ARC.TAC"]},
    {"case_id": "ARCH-INT-020", "text": "How does waterproofing connect to roofs basements wet areas balconies and building envelope?", "asset_context": "waterproofing_envelope_path", "concept_path": "MAT.MEM.RME.WPM", "path_refs": [("MAT.MEM.RME.WPM", "waterproofing_membrane"), ("MAT.ASM.ROF", "roof_assembly"), ("MAT.ASM.WET", "wet_area_assembly"), ("ARC.ENV.ROF.RDP", "roof_drainage_plane")], "source_evidence": MATERIAL_SOURCE_IDS, "result_type": "single_value", "confidence": "deterministic", "rationale": "Waterproofing membrane nodes connect to envelope and wet-area assemblies through moisture-control paths.", "fallback_reason": "exact_waterproofing_envelope_path_match", "context_paths": ["MAT.MEM.RME", "ARC.ENV"]},
    {"case_id": "ARCH-INT-021", "text": "What path connects Zaha Hadid to concrete and long span public architecture?", "asset_context": "hadid_aquatics_concrete_long_span", "concept_path": "FIG.ARD.CAA.HAD", "path_refs": [("FIG.ARD.CAA.HAD", "architect"), ("FIG.WRK.BUI.AQA", "work_anchor"), ("ARC.BLD.STR.LSS", "long_span_structure"), ("ARC.MAT.STM.STL", "structural_steel")], "source_evidence": PROJECT_EVIDENCE_SOURCE_IDS, "result_type": "composed", "confidence": "deterministic", "rationale": "Hadid's public-work path composes person, project, long-span system, and material-system facets without a direct person-material shortcut.", "fallback_reason": "composed_hadid_aquatics_long_span_path", "context_paths": ["FIG.ARD.CAA.HAD", "ARC.BLD.STR.LSS"]},
    {"case_id": "ARCH-INT-022", "text": "How does Dongdaemun Design Plaza connect Zaha Hadid to aluminum facade systems?", "asset_context": "hadid_ddp_aluminum_facade", "concept_path": "FIG.WRK.BUI.DDP", "path_refs": [("FIG.ARD.CAA.HAD", "architect"), ("FIG.WRK.BUI.DDP", "work_anchor"), ("MAT.STM.MEC.ALP", "aluminum_composite_panel"), ("MAT.ASM.FAC", "facade_assembly")], "source_evidence": PROJECT_EVIDENCE_SOURCE_IDS, "result_type": "composed", "confidence": "deterministic", "rationale": "The DDP path composes architect, work, facade assembly, and aluminum cladding concepts.", "fallback_reason": "composed_hadid_ddp_facade_path", "context_paths": ["FIG.ARD.CAA.HAD", "MAT.ASM.FAC"]},
    {"case_id": "ARCH-INT-023", "text": "What path connects Tadao Ando to exposed concrete, light, and spatial atmosphere?", "asset_context": "ando_exposed_concrete_light", "concept_path": "FIG.ARD.CAA.AND", "path_refs": [("FIG.ARD.CAA.AND", "architect"), ("FIG.WRK.BUI.CHL", "work_anchor"), ("MAT.CMA.CEM.EXP", "exposed_concrete"), ("ARC.TAC.SOS.DAY", "daylight")], "source_evidence": PROJECT_EVIDENCE_SOURCE_IDS, "result_type": "composed", "confidence": "deterministic", "rationale": "The Ando path composes person, Church of the Light, exposed concrete, and daylight concepts.", "fallback_reason": "composed_ando_concrete_light_path", "context_paths": ["FIG.ARD.CAA.AND", "MAT.CMA.CEM.EXP"]},
    {"case_id": "ARCH-INT-024", "text": "How does Le Corbusier connect to béton brut, brise-soleil, and Brutalist material expression?", "asset_context": "le_corbusier_beton_brut_brise_soleil", "concept_path": "FIG.ARD.CAA.LCO", "path_refs": [("FIG.ARD.CAA.LCO", "architect"), ("FIG.WRK.BUI.LAT", "work_anchor"), ("MAT.CMA.CEM.EXP", "beton_brut"), ("ARC.TAC.SOS.BRS", "brise_soleil"), ("ARC.HIS.MOD.BME", "brutalist_material_expression")], "source_evidence": PROJECT_EVIDENCE_SOURCE_IDS, "result_type": "composed", "confidence": "deterministic", "rationale": "Le Corbusier's monastery work composes concrete finish, sun-control, and movement material-expression nodes.", "fallback_reason": "composed_le_corbusier_beton_brut_path", "context_paths": ["FIG.ARD.CAA.LCO", "ARC.HIS.MOD.BME"]},
    {"case_id": "ARCH-INT-025", "text": "How does Louis Kahn connect concrete, brick, daylight, and civic monumentality?", "asset_context": "kahn_concrete_brick_daylight", "concept_path": "FIG.ARD.CAA.KAH", "path_refs": [("FIG.ARD.CAA.KAH", "architect"), ("FIG.WRK.BUI.NAD", "work_anchor"), ("MAT.CMA.CEM.CIP", "cast_in_place_concrete"), ("ARC.TAC.SOS.DAY", "daylight"), ("FIG.WRK.BUI.EXE", "library_work"), ("MAT.MST.CLB", "brick")], "source_evidence": PROJECT_EVIDENCE_SOURCE_IDS, "result_type": "composed", "confidence": "deterministic", "rationale": "Kahn work anchors compose concrete, brick, daylight, and institutional/civic spatial order.", "fallback_reason": "composed_kahn_material_daylight_path", "context_paths": ["FIG.ARD.CAA.KAH", "MAT.CMA.CEM"]},
    {"case_id": "ARCH-INT-026", "text": "How do Mies works connect glass, steel, stone, and International Style?", "asset_context": "mies_glass_steel_international_style", "concept_path": "FIG.ARD.CAA.MIE", "path_refs": [("FIG.ARD.CAA.MIE", "architect"), ("FIG.WRK.BUI.BCP", "pavilion_work"), ("MAT.GLA.FLG", "glass"), ("ARC.MAT.STM.STL", "steel"), ("MAT.MST.NAS.MAR", "stone"), ("ARC.HIS.MOD.ISC", "international_style")], "source_evidence": PROJECT_EVIDENCE_SOURCE_IDS, "result_type": "composed", "confidence": "deterministic", "rationale": "Mies work anchors compose glass, steel, stone, and International Style rather than a generic architect-material claim.", "fallback_reason": "composed_mies_material_style_path", "context_paths": ["FIG.ARD.CAA.MIE", "ARC.HIS.MOD.ISC"]},
    {"case_id": "ARCH-INT-027", "text": "How does the Sydney Opera House connect architecture and engineering through shell structure?", "asset_context": "sydney_opera_house_shell_coordination", "concept_path": "FIG.WRK.BUI.SYD", "path_refs": [("FIG.ARD.CAA.UTZ", "architect"), ("FIG.ETS.STE.ARU", "engineer"), ("FIG.WRK.BUI.SYD", "work_anchor"), ("ARC.BLD.STR.SHL", "shell_structure"), ("MAT.FIP.FLF.CER", "ceramic_tile")], "source_evidence": PROJECT_EVIDENCE_SOURCE_IDS + ENGINEERING_WORK_SOURCE_IDS, "result_type": "composed", "confidence": "deterministic", "rationale": "Sydney Opera House composes architect, engineering collaborator, shell structure, and material-surface nodes.", "fallback_reason": "composed_sydney_shell_coordination_path", "context_paths": ["FIG.WRK.BUI.SYD", "ARC.BLD.STR.SHL"]},
    {"case_id": "ARCH-INT-028", "text": "How do Herzog and de Meuron works connect brick, steel, adaptive reuse, and contemporary civic architecture?", "asset_context": "herzog_de_meuron_brick_steel_reuse", "concept_path": "FIG.ARD.CAA.HER", "path_refs": [("FIG.ARD.CAA.HER", "architect"), ("FIG.ARD.CAA.MEU", "architect"), ("FIG.WRK.BUI.TAT", "adaptive_reuse_work"), ("MAT.MST.CLB", "brick"), ("ARC.HER.ADM", "adaptive_reuse"), ("FIG.WRK.BUI.NBS", "stadium_work"), ("ARC.MAT.STM.STL", "steel")], "source_evidence": PROJECT_EVIDENCE_SOURCE_IDS, "result_type": "composed", "confidence": "deterministic", "rationale": "The paired works anchor brick/adaptive-reuse and steel/long-span paths for the same practice.", "fallback_reason": "composed_herzog_de_meuron_work_material_path", "context_paths": ["FIG.ARD.CAA.HER", "ARC.HER.ADM"]},
    {"case_id": "ARCH-INT-029", "text": "How does Glenn Murcutt connect regional houses to shading, natural ventilation, and metal roofing?", "asset_context": "murcutt_climate_material_path", "concept_path": "FIG.ARD.CAA.MUR", "path_refs": [("FIG.ARD.CAA.MUR", "architect"), ("FIG.WRK.BUI.MAV", "work_anchor"), ("FIG.WRK.BUI.MNY", "magney_house"), ("ARC.TAC.NVS", "natural_ventilation"), ("ARC.TAC.SOS.SHD", "shading"), ("MAT.STM.MEC.RFS", "roofing_sheet")], "source_evidence": PROJECT_EVIDENCE_SOURCE_IDS, "result_type": "composed", "confidence": "deterministic", "rationale": "Murcutt regional-house anchors compose climate response and lightweight material-system paths.", "fallback_reason": "composed_murcutt_climate_material_path", "context_paths": ["FIG.ARD.CAA.MUR", "ARC.TAC"]},
    {"case_id": "ARCH-INT-030", "text": "How does Wang Shu connect recycled masonry, brick, heritage fabric, and cultural memory?", "asset_context": "wang_shu_recycled_masonry_heritage", "concept_path": "FIG.ARD.CAA.WSH", "path_refs": [("FIG.ARD.CAA.WSH", "architect"), ("FIG.WRK.BUI.NHB", "museum_work"), ("FIG.WRK.BUI.SIK", "kiln_brick_museum"), ("MAT.MST.CLB", "brick"), ("SUS.RSC.MAT", "material_reuse"), ("ARC.HER.FAB", "historic_fabric")], "source_evidence": PROJECT_EVIDENCE_SOURCE_IDS, "result_type": "composed", "confidence": "deterministic", "rationale": "Wang Shu work anchors compose masonry, material reuse, craft, and heritage-fabric nodes.", "fallback_reason": "composed_wang_shu_masonry_heritage_path", "context_paths": ["FIG.ARD.CAA.WSH", "ARC.HER.FAB"]},
    {"case_id": "ARCH-INT-031", "text": "How do Norman Foster works connect diagrid, glass, steel, high-rise, and bridge systems?", "asset_context": "foster_diagrid_glass_bridge_systems", "concept_path": "FIG.ARD.CAA.FOS", "path_refs": [("FIG.ARD.CAA.FOS", "architect"), ("FIG.WRK.BUI.GHK", "diagrid_work"), ("STR.SSS.MBF.DGF", "diagrid_frame"), ("MAT.GLA.CWG", "curtain_wall_glazing"), ("FIG.WRK.BUI.MVA", "bridge_work"), ("CIV.BRG.CBS", "cable_stayed_bridge")], "source_evidence": PROJECT_EVIDENCE_SOURCE_IDS + ENGINEERING_WORK_SOURCE_IDS, "result_type": "composed", "confidence": "deterministic", "rationale": "Foster work anchors compose tall-building and bridge paths through systems and materials.", "fallback_reason": "composed_foster_system_material_path", "context_paths": ["FIG.ARD.CAA.FOS", "STR.SSS.MBF"]},
    {"case_id": "ARCH-INT-032", "text": "How do suspension bridges connect Roebling and Strauss to steel cables and bridge structure?", "asset_context": "suspension_bridge_engineer_cable_path", "concept_path": "CIV.BRG.SUS", "path_refs": [("FIG.ETS.STE.ROE", "engineer"), ("FIG.WRK.BUI.BRB", "brooklyn_bridge"), ("FIG.ETS.STE.STR", "engineer"), ("FIG.WRK.BUI.GGB", "golden_gate_bridge"), ("CIV.BRG.SUS", "suspension_bridge"), ("MAT.STM.STS.CBL", "steel_cable")], "source_evidence": ENGINEERING_WORK_SOURCE_IDS, "result_type": "composed", "confidence": "deterministic", "rationale": "Suspension-bridge work anchors compose engineers, bridge system, and steel cable material paths.", "fallback_reason": "composed_suspension_bridge_cable_path", "context_paths": ["CIV.BRG", "MAT.STM.STS.CBL"]},
    {"case_id": "ARCH-INT-033", "text": "How does Burj Khalifa connect tall-building design to buttressed core and wind load concepts?", "asset_context": "burj_buttressed_core_wind_path", "concept_path": "FIG.WRK.BUI.BRJ", "path_refs": [("FIG.ETS.STE.BAK", "engineer"), ("FIG.WRK.BUI.BRJ", "work_anchor"), ("STR.RCS.SWC.BTC", "buttressed_core"), ("ARC.BLD.STR.LST", "lateral_stability"), ("ARC.BLD.STR.WDL", "wind_load")], "source_evidence": ENGINEERING_WORK_SOURCE_IDS, "result_type": "composed", "confidence": "deterministic", "rationale": "The tall-building path composes engineer, work, structural system, lateral stability, and wind-load concepts.", "fallback_reason": "composed_burj_buttressed_core_path", "context_paths": ["FIG.WRK.BUI.BRJ", "ARC.BLD.STR"]},
    {"case_id": "ARCH-INT-034", "text": "How does Peter Zumthor connect stone, board-formed concrete, atmosphere, and phenomenology?", "asset_context": "zumthor_material_atmosphere_path", "concept_path": "FIG.ARD.CAA.ZUM", "path_refs": [("FIG.ARD.CAA.ZUM", "architect"), ("FIG.WRK.BUI.THV", "stone_work"), ("MAT.MST.NAS.GRA", "stone"), ("FIG.WRK.BUI.BKF", "chapel_work"), ("MAT.CMA.CEM.BFC", "board_formed_concrete"), ("ARC.DTS.PPT.PLM", "phenomenology")], "source_evidence": PROJECT_EVIDENCE_SOURCE_IDS, "result_type": "composed", "confidence": "deterministic", "rationale": "Zumthor work anchors compose material texture, atmosphere, and phenomenological design concepts.", "fallback_reason": "composed_zumthor_material_atmosphere_path", "context_paths": ["FIG.ARD.CAA.ZUM", "ARC.DTS.PPT"]},
    {"case_id": "ARCH-INT-035", "text": "How does Louvre Abu Dhabi connect dome structure, filtered daylight, steel, and climate response?", "asset_context": "nouvel_louvre_abu_dhabi_dome_daylight", "concept_path": "FIG.WRK.BUI.LAD", "path_refs": [("FIG.ARD.CAA.NOU", "architect"), ("FIG.WRK.BUI.LAD", "work_anchor"), ("ARC.BLD.STR.DOM", "dome_structure"), ("ARC.MAT.STM.STL", "steel"), ("ARC.TAC.SOS.DAY", "daylight"), ("ARC.TAC.SOS.SHD", "shading")], "source_evidence": PROJECT_EVIDENCE_SOURCE_IDS, "result_type": "composed", "confidence": "deterministic", "rationale": "The Louvre Abu Dhabi path composes dome, steel, filtered daylight, and solar-control concepts.", "fallback_reason": "composed_nouvel_dome_daylight_path", "context_paths": ["FIG.ARD.CAA.NOU", "ARC.BLD.STR.DOM"]},
    {"case_id": "ARCH-INT-036", "text": "How does Shigeru Ban connect paper tubes to temporary works and disaster relief architecture?", "asset_context": "ban_paper_tube_disaster_relief", "concept_path": "FIG.ARD.CAA.BAN", "path_refs": [("FIG.ARD.CAA.BAN", "architect"), ("FIG.WRK.BUI.PCT", "work_anchor"), ("MAT.TBB.ENW.PPT", "paper_tube"), ("CON.TMP", "temporary_works"), ("URB.RES.DRR", "disaster_risk_reduction")], "source_evidence": PROJECT_EVIDENCE_SOURCE_IDS, "result_type": "composed", "confidence": "deterministic", "rationale": "Ban's humanitarian-material path composes work, paper-tube material, temporary works, and disaster-response concepts.", "fallback_reason": "composed_ban_paper_tube_relief_path", "context_paths": ["FIG.ARD.CAA.BAN", "URB.RES.DRR"]},
    {"case_id": "ARCH-INT-037", "text": "How does Francis Kere connect local materials, ventilation, shading, and social architecture?", "asset_context": "kere_local_material_climate_school", "concept_path": "FIG.ARD.CAA.KER", "path_refs": [("FIG.ARD.CAA.KER", "architect"), ("FIG.WRK.BUI.LYC", "work_anchor"), ("MAT.PRF.ENV.LOC", "local_materials"), ("ARC.TAC.NVS.XVN", "cross_ventilation"), ("ARC.TAC.SOS.SHD", "shading")], "source_evidence": PROJECT_EVIDENCE_SOURCE_IDS, "result_type": "composed", "confidence": "deterministic", "rationale": "Kere school paths compose local materials, climate response, and social architecture without copying project descriptions.", "fallback_reason": "composed_kere_local_climate_path", "context_paths": ["FIG.ARD.CAA.KER", "ARC.TAC"]},
    {"case_id": "ARCH-INT-038", "text": "How do Gothic architecture paths connect stone, rib vaults, flying buttresses, and stained glass?", "asset_context": "gothic_stone_vault_stained_glass", "concept_path": "ARC.HIS.ANC.GOT", "path_refs": [("ARC.HIS.ANC.GOT", "gothic_architecture"), ("MAT.MST.NAS.LIM", "limestone"), ("ARC.BLD.STR.RBV", "rib_vault"), ("ARC.BLD.STR.FBU", "flying_buttress"), ("MAT.GLA.STG", "stained_glass")], "source_evidence": MATERIAL_SOURCE_IDS, "result_type": "composed", "confidence": "deterministic", "rationale": "Gothic material/system paths compose masonry, vaulting, buttressing, and colored-glass envelope concepts.", "fallback_reason": "composed_gothic_material_system_path", "context_paths": ["ARC.HIS.ANC.GOT", "MAT.GLA.STG"]},
    {"case_id": "ARCH-INT-039", "text": "How do Roman and Byzantine paths connect concrete, vaults, arches, and domes?", "asset_context": "roman_byzantine_concrete_vault_dome", "concept_path": "ARC.HIS.ANC.RFB", "path_refs": [("ARC.HIS.ANC.RFB", "roman_architecture"), ("MAT.CMA.CEM.CIP", "cast_in_place_concrete"), ("ARC.BLD.STR.DOM", "dome_structure"), ("ARC.WAC.CIT.RCV", "roman_concrete_vaulting")], "source_evidence": MATERIAL_SOURCE_IDS, "result_type": "composed", "confidence": "deterministic", "rationale": "Ancient architecture paths compose concrete material, vault/dome systems, and historical construction concepts.", "fallback_reason": "composed_roman_byzantine_concrete_dome_path", "context_paths": ["ARC.HIS.ANC.RFB", "ARC.BLD.STR.DOM"]},
    {"case_id": "ARCH-INT-040", "text": "How does tropical modernism connect brise soleil, natural ventilation, and concrete climate response?", "asset_context": "tropical_modernism_brise_ventilation_concrete", "concept_path": "ARC.HIS.SEA.TMS", "path_refs": [("ARC.HIS.SEA.TMS", "tropical_modernism"), ("ARC.TAC.SOS.BRS", "brise_soleil"), ("ARC.TAC.NVS.XVN", "cross_ventilation"), ("MAT.CMA.CEM.CIP", "cast_in_place_concrete"), ("ARC.TAC", "tropical_architecture")], "source_evidence": NCCA_SOURCE_IDS + MATERIAL_SOURCE_IDS, "result_type": "composed", "confidence": "deterministic", "rationale": "Tropical modernism composes climate-response concepts and material paths relevant to LEA/ALE study.", "fallback_reason": "composed_tropical_modernism_material_path", "context_paths": ["ARC.HIS.SEA.TMS", "ARC.TAC"]},
    {"case_id": "ARCH-INT-041", "text": "How does Philippine vernacular architecture connect bamboo, nipa, capiz, and passive cooling?", "asset_context": "philippine_vernacular_bamboo_nipa_capiz", "concept_path": "ARC.HIS.SEA.PVA", "path_refs": [("ARC.HIS.SEA.PVA", "philippine_vernacular"), ("ARC.HIS.SEA.BKS", "bahay_kubo"), ("MAT.TBB.BAS.BCM", "bamboo"), ("MAT.TBB.BAS.NIP", "nipa"), ("ARC.HIS.SEA.BNB", "bahay_na_bato"), ("MAT.TBB.BAS.CAP", "capiz"), ("ARC.TAC", "tropical_architecture")], "source_evidence": NCCA_SOURCE_IDS, "result_type": "composed", "confidence": "deterministic", "rationale": "Philippine vernacular paths compose building types, local materials, filtered light, and climate response.", "fallback_reason": "composed_philippine_vernacular_materials_path", "context_paths": ["ARC.HIS.SEA.PVA", "ARC.TAC"]},
    {"case_id": "ARCH-INT-042", "text": "How does Leandro Locsin connect Philippine modernism to thin-shell concrete?", "asset_context": "locsin_church_holy_sacrifice_shell_concrete", "concept_path": "FIG.ARD.CAA.LOC", "path_refs": [("FIG.ARD.CAA.LOC", "filipino_architect"), ("FIG.WRK.BUI.CHS", "work_anchor"), ("ARC.MAT.CON.RCC", "reinforced_concrete"), ("ARC.BLD.STR.SHL", "shell_structure"), ("ARC.HIS.SEA.PMP", "postwar_philippine_modernism")], "source_evidence": NCCA_SOURCE_IDS, "result_type": "composed", "confidence": "deterministic", "rationale": "Locsin's Philippine-modernism path composes architect, work, shell structure, concrete, and national architectural history.", "fallback_reason": "composed_locsin_shell_concrete_path", "context_paths": ["FIG.ARD.CAA.LOC", "ARC.HIS.SEA.PMP"]},
    {"case_id": "ARCH-INT-043", "text": "How does Pablo Antonio connect Philippine Art Deco to concrete educational buildings?", "asset_context": "pablo_antonio_feu_art_deco", "concept_path": "FIG.ARD.CAA.ANT", "path_refs": [("FIG.ARD.CAA.ANT", "filipino_architect"), ("FIG.WRK.BUI.FEU", "work_anchor"), ("ARC.HIS.SEA.ADP", "philippine_art_deco"), ("MAT.CMA.CEM.CIP", "cast_in_place_concrete"), ("ARC.HIS.SEA.PMP", "philippine_modernism")], "source_evidence": NCCA_SOURCE_IDS, "result_type": "composed", "confidence": "deterministic", "rationale": "Pablo Antonio paths compose Filipino architect, campus work anchor, Art Deco, concrete, and Philippine modernism concepts.", "fallback_reason": "composed_pablo_antonio_art_deco_path", "context_paths": ["FIG.ARD.CAA.ANT", "ARC.HIS.SEA.ADP"]},
    {"case_id": "ARCH-INT-044", "text": "How do materials connect to LEA subjects like construction methods, specifications, structures, interiors, and tropical design?", "asset_context": "lea_materials_subject_bridge", "concept_path": "ARC.MAT", "path_refs": [("ARC.MAT", "materials_methods"), ("CON.DMC.DBB.BID", "specifications_contracts"), ("ARC.BLD.STR.SLB", "structural_component"), ("ARC.INT.PAC.ACU", "interiors_acoustics"), ("ARC.TAC", "tropical_design")], "source_evidence": MATERIAL_SOURCE_IDS + NCCA_SOURCE_IDS, "result_type": "composed", "confidence": "deterministic", "rationale": "LEA/ALE material paths compose construction, specification, structure, interior, and tropical-design study domains.", "fallback_reason": "composed_lea_material_subject_path", "context_paths": ["ARC.MAT", "ARC.TAC"]},
    {"case_id": "ARCH-INT-045", "text": "Searching Tropical Architecture should resolve the clean concept node, not raw-source filename metadata.", "asset_context": "clean_tropical_architecture_label", "concept_path": "ARC.TAC", "path_refs": [("ARC.TAC", "clean_concept"), ("ARC.TAC.SOS.BRS", "solar_control"), ("ARC.TAC.NVS.XVN", "natural_ventilation"), ("MAT.TBB.BAS.BCM", "vernacular_material")], "source_evidence": NCCA_SOURCE_IDS + MATERIAL_SOURCE_IDS, "result_type": "single_value", "confidence": "deterministic", "rationale": "Default learner-facing resolution must prefer the clean Tropical Architecture concept and exclude raw-source filename metadata labels.", "fallback_reason": "exact_clean_tropical_architecture_concept", "context_paths": ["ARC.TAC", "ARC.HIS.SEA.PVA"]},
]
RESOLVER_CASE_SPECS.extend([
    {"case_id": "ARCH-INT-046", "text": "How does Juan Arellano connect to Manila Metropolitan Theater and Philippine Art Deco?", "asset_context": "arellano_met_art_deco", "concept_path": "FIG.ARD.CAA.ARE", "path_refs": [("FIG.ARD.CAA.ARE", "filipino_architect"), ("FIG.WRK.BUI.MTH", "work_anchor"), ("ARC.HIS.SEA.ADP", "philippine_art_deco"), ("HIS.GHA.CTS", "theater_civic_space")], "source_evidence": PHILIPPINE_ARCHITECTURE_SOURCE_IDS, "result_type": "composed", "confidence": "deterministic", "rationale": "Juan Arellano resolves through a verified work anchor and style/theater concepts rather than generic person-style edges.", "fallback_reason": "composed_arellano_met_art_deco_path", "context_paths": ["FIG.ARD.CAA.ARE", "ARC.HIS.SEA.ADP"]},
    {"case_id": "ARCH-INT-047", "text": "How does Manila Metropolitan Theater connect heritage conservation, Art Deco, concrete, and stained glass?", "asset_context": "metropolitan_theater_material_heritage", "concept_path": "FIG.WRK.BUI.MTH", "path_refs": [("FIG.WRK.BUI.MTH", "work_anchor"), ("ARC.HIS.SEA.ADP", "art_deco"), ("ARC.HER", "heritage"), ("MAT.CMA.CEM.CIP", "cast_in_place_concrete"), ("MAT.GLA.STG", "stained_glass")], "source_evidence": PHILIPPINE_ARCHITECTURE_SOURCE_IDS, "result_type": "composed", "confidence": "deterministic", "rationale": "The Met path composes a Philippine work anchor with heritage, style, and material concepts from safe public metadata.", "fallback_reason": "composed_met_heritage_material_path", "context_paths": ["FIG.WRK.BUI.MTH", "ARC.HER"]},
    {"case_id": "ARCH-INT-048", "text": "How does Ildefonso Santos Jr connect landscape architecture, Makati Commercial Center, Paco Park, and site planning?", "asset_context": "santos_landscape_site_planning", "concept_path": "FIG.ARD.CAA.SAN", "path_refs": [("FIG.ARD.CAA.SAN", "filipino_landscape_architect"), ("FIG.PTE.ROL.LAR", "landscape_architect_role"), ("FIG.WRK.BUI.MCC", "commercial_landscape_work"), ("FIG.WRK.BUI.PAP", "heritage_park_work"), ("ARC.SIT.LAN", "landscape_interface")], "source_evidence": PHILIPPINE_ARCHITECTURE_SOURCE_IDS, "result_type": "composed", "confidence": "deterministic", "rationale": "Landscape architecture paths are resolved through role and work anchors tied to site-planning concepts.", "fallback_reason": "composed_santos_landscape_path", "context_paths": ["FIG.ARD.CAA.SAN", "ARC.SIT"]},
    {"case_id": "ARCH-INT-049", "text": "How does Francisco Manosa connect Coconut Palace, bamboo, capiz, vernacular architecture, and tropical design?", "asset_context": "manosa_coconut_palace_material_path", "concept_path": "FIG.ARD.CAA.MAN", "path_refs": [("FIG.ARD.CAA.MAN", "filipino_architect"), ("FIG.WRK.BUI.COC", "work_anchor"), ("MAT.TBB.BAS.BCM", "bamboo"), ("MAT.TBB.BAS.CAP", "capiz"), ("ARC.HIS.SEA.PVA", "philippine_vernacular"), ("ARC.TAC", "tropical_architecture")], "source_evidence": PHILIPPINE_ARCHITECTURE_SOURCE_IDS, "result_type": "composed", "confidence": "deterministic", "rationale": "Mañosa material reasoning uses work and vernacular building paths, not direct unsourced person-material claims.", "fallback_reason": "composed_manosa_vernacular_material_path", "context_paths": ["FIG.ARD.CAA.MAN", "ARC.HIS.SEA.PVA"]},
    {"case_id": "ARCH-INT-050", "text": "How does Bamboo House Ternate connect Francisco Manosa to bamboo, nipa, sustainability, and tropical ventilation?", "asset_context": "manosa_bamboo_house_tropical_path", "concept_path": "FIG.WRK.BUI.BHT", "path_refs": [("FIG.ARD.CAA.MAN", "filipino_architect"), ("FIG.WRK.BUI.BHT", "work_anchor"), ("MAT.TBB.BAS.BCM", "bamboo"), ("MAT.TBB.BAS.NIP", "nipa"), ("ARC.TAC.NVS", "natural_ventilation"), ("SUS.ENE.PDE", "passive_design")], "source_evidence": PHILIPPINE_ARCHITECTURE_SOURCE_IDS, "result_type": "composed", "confidence": "deterministic", "rationale": "The Bamboo House path composes person, work, local materials, passive design, and ventilation concepts.", "fallback_reason": "composed_bamboo_house_tropical_path", "context_paths": ["FIG.WRK.BUI.BHT", "ARC.TAC"]},
    {"case_id": "ARCH-INT-051", "text": "How does Jose Maria Zaragoza connect Santo Domingo Church to modern ecclesiastical architecture and reinforced concrete?", "asset_context": "zaragoza_santo_domingo_modern_church", "concept_path": "FIG.ARD.CAA.ZAR", "path_refs": [("FIG.ARD.CAA.ZAR", "filipino_architect"), ("FIG.WRK.BUI.SDC", "work_anchor"), ("HIS.BEC.RCT", "church_typology"), ("ARC.MAT.CON.RCC", "reinforced_concrete"), ("ARC.HIS.SEA.PMP", "postwar_philippine_modernism")], "source_evidence": PHILIPPINE_ARCHITECTURE_SOURCE_IDS, "result_type": "composed", "confidence": "deterministic", "rationale": "Zaragoza resolves through an ecclesiastical work anchor connected to church typology, concrete, and postwar modernism.", "fallback_reason": "composed_zaragoza_church_concrete_path", "context_paths": ["FIG.ARD.CAA.ZAR", "HIS.BEC.RCT"]},
    {"case_id": "ARCH-INT-052", "text": "How does Leandro Locsin connect Immaculate Heart of Mary Parish to concrete shell form, daylight, and sacred space?", "asset_context": "locsin_ihmp_shell_daylight", "concept_path": "FIG.WRK.BUI.IHM", "path_refs": [("FIG.ARD.CAA.LOC", "filipino_architect"), ("FIG.WRK.BUI.IHM", "work_anchor"), ("ARC.MAT.CON.RCC", "reinforced_concrete"), ("ARC.BLD.STR.SHL", "shell_structure"), ("ARC.TAC.SOS.DAY", "daylight")], "source_evidence": PHILIPPINE_ARCHITECTURE_SOURCE_IDS, "result_type": "composed", "confidence": "deterministic", "rationale": "The IHMP path extends Locsin's church-work evidence through shell, concrete, and light concepts.", "fallback_reason": "composed_locsin_ihmp_shell_path", "context_paths": ["FIG.ARD.CAA.LOC", "ARC.BLD.STR.SHL"]},
    {"case_id": "ARCH-INT-053", "text": "How does Bahay Kubo connect bamboo, nipa, raised timber logic, passive cooling, and tropical architecture?", "asset_context": "bahay_kubo_material_climate_path", "concept_path": "FIG.WRK.BUI.BKB", "path_refs": [("FIG.WRK.BUI.BKB", "building_type_anchor"), ("ARC.HIS.SEA.BKS", "bahay_kubo_concept"), ("MAT.TBB.BAS.BCM", "bamboo"), ("MAT.TBB.BAS.NIP", "nipa"), ("MAT.TBB.DIL.HDW", "timber"), ("ARC.TAC.NVS", "natural_ventilation")], "source_evidence": PHILIPPINE_ARCHITECTURE_SOURCE_IDS, "result_type": "composed", "confidence": "deterministic", "rationale": "Bahay Kubo resolves as a building-type anchor connecting clean concept, materials, and climate-response nodes.", "fallback_reason": "composed_bahay_kubo_material_path", "context_paths": ["ARC.HIS.SEA.BKS", "ARC.TAC"]},
    {"case_id": "ARCH-INT-054", "text": "How does Bahay Na Bato connect capiz windows, timber, stone, Spanish colonial architecture, and climate adaptation?", "asset_context": "bahay_na_bato_material_heritage_path", "concept_path": "FIG.WRK.BUI.BNB", "path_refs": [("FIG.WRK.BUI.BNB", "building_type_anchor"), ("ARC.HIS.SEA.BNB", "bahay_na_bato_concept"), ("MAT.TBB.BAS.CAP", "capiz"), ("MAT.TBB.DIL.HDW", "timber"), ("MAT.MST.NAS.LIM", "stone"), ("ARC.HIS.SEA.SCC", "spanish_colonial_context")], "source_evidence": PHILIPPINE_ARCHITECTURE_SOURCE_IDS, "result_type": "composed", "confidence": "deterministic", "rationale": "Bahay na Bato resolves through a building-type anchor and material/cultural-history concepts useful for LEA/ALE study.", "fallback_reason": "composed_bahay_na_bato_material_path", "context_paths": ["ARC.HIS.SEA.BNB", "ARC.HIS.SEA.SCC"]},
    {"case_id": "ARCH-INT-055", "text": "How does Torogan connect Maranao architecture, timber, ornament, and cultural heritage?", "asset_context": "torogan_timber_heritage_path", "concept_path": "FIG.WRK.BUI.TRG", "path_refs": [("FIG.WRK.BUI.TRG", "building_type_anchor"), ("ARC.HIS.SEA.TRG", "torogan_concept"), ("MAT.TBB.DIL.HDW", "timber"), ("HIS.BEC.COS", "ornament_system"), ("ARC.CHC", "cultural_heritage")], "source_evidence": PHILIPPINE_ARCHITECTURE_SOURCE_IDS, "result_type": "composed", "confidence": "deterministic", "rationale": "Torogan resolves through vernacular building-type, timber, ornament, and heritage nodes without source payload copying.", "fallback_reason": "composed_torogan_heritage_path", "context_paths": ["ARC.HIS.SEA.TRG", "ARC.CHC"]},
    {"case_id": "ARCH-INT-056", "text": "How does Ivatan stone house connect stone masonry, climate resilience, heritage, and tropical conditions?", "asset_context": "ivatan_stone_house_resilience_path", "concept_path": "FIG.WRK.BUI.IVT", "path_refs": [("FIG.WRK.BUI.IVT", "building_type_anchor"), ("ARC.HIS.SEA.IVT", "ivatan_stone_house"), ("MAT.MST.NAS.LIM", "stone"), ("STR.WSD", "wind_seismic_design"), ("ARC.HER", "heritage")], "source_evidence": PHILIPPINE_ARCHITECTURE_SOURCE_IDS, "result_type": "composed", "confidence": "deterministic", "rationale": "Ivatan stone-house paths connect material, climate resilience, and heritage concepts through a clean building-type anchor.", "fallback_reason": "composed_ivatan_stone_resilience_path", "context_paths": ["ARC.HIS.SEA.IVT", "STR.WSD"]},
    {"case_id": "ARCH-INT-057", "text": "How does Ifugao Bale connect timber house traditions, raised-floor construction, cultural landscape, and natural ventilation?", "asset_context": "ifugao_bale_timber_landscape_path", "concept_path": "FIG.WRK.BUI.IFB", "path_refs": [("FIG.WRK.BUI.IFB", "building_type_anchor"), ("ARC.HIS.SEA.IFB", "ifugao_bale_concept"), ("MAT.TBB.DIL.HDW", "timber"), ("ARC.TAC.NVS", "natural_ventilation"), ("ARC.CHC.CLC", "cultural_landscape_context")], "source_evidence": PHILIPPINE_ARCHITECTURE_SOURCE_IDS, "result_type": "composed", "confidence": "deterministic", "rationale": "Ifugao Bale resolves through timber, ventilation, and cultural landscape concepts for Philippine vernacular reasoning.", "fallback_reason": "composed_ifugao_bale_timber_path", "context_paths": ["ARC.HIS.SEA.IFB", "ARC.CHC"]},
    {"case_id": "ARCH-INT-058", "text": "How does Philippine modernism connect Locsin, Antonio, Zaragoza, concrete, churches, civic centers, and theaters?", "asset_context": "philippine_modernism_people_works_materials", "concept_path": "ARC.HIS.SEA.PMP", "path_refs": [("ARC.HIS.SEA.PMP", "philippine_modernism"), ("FIG.ARD.CAA.LOC", "locsin"), ("FIG.ARD.CAA.ANT", "antonio"), ("FIG.ARD.CAA.ZAR", "zaragoza"), ("ARC.MAT.CON.RCC", "reinforced_concrete"), ("FIG.WRK.BUI.CHS", "locsin_church"), ("FIG.WRK.BUI.FEU", "antonio_campus")], "source_evidence": PHILIPPINE_ARCHITECTURE_SOURCE_IDS, "result_type": "composed", "confidence": "deterministic", "rationale": "Philippine modernism is resolved as a multi-anchor path across people, works, typologies, and material systems.", "fallback_reason": "composed_philippine_modernism_evidence_path", "context_paths": ["ARC.HIS.SEA.PMP", "ARC.MAT.CON"]},
    {"case_id": "ARCH-INT-059", "text": "How do Philippine National Artists for Architecture connect to official status, works, and LEA history study?", "asset_context": "national_artist_architecture_status_paths", "concept_path": "FIG.PTE.ROL.NAA", "path_refs": [("FIG.PTE.ROL.NAA", "national_artist_status"), ("FIG.ARD.CAA.LOC", "locsin"), ("FIG.ARD.CAA.NAK", "nakpil"), ("FIG.ARD.CAA.ANT", "antonio"), ("FIG.ARD.CAA.SAN", "santos"), ("FIG.ARD.CAA.MAN", "manosa"), ("FIG.ARD.CAA.ZAR", "zaragoza")], "source_evidence": PHILIPPINE_ARCHITECTURE_SOURCE_IDS, "result_type": "single_value", "confidence": "deterministic", "rationale": "Official public metadata supplies a status facet that connects National Artists to learner-facing works and history paths.", "fallback_reason": "exact_national_artist_architecture_status_path", "context_paths": ["FIG.PTE.ROL.NAA", "FIG.PTE.NAT.PHL"]},
    {"case_id": "ARCH-INT-060", "text": "How does Philippine theater architecture connect Metropolitan Theater, Rizal Theater, Folk Arts Theater, Art Deco, and modernism?", "asset_context": "philippine_theater_architecture_path", "concept_path": "HIS.GHA.CTS", "path_refs": [("HIS.GHA.CTS", "theater_typology"), ("FIG.WRK.BUI.MTH", "metropolitan_theater"), ("FIG.WRK.BUI.RIZ", "rizal_theater"), ("FIG.WRK.BUI.FHA", "folk_arts_theater"), ("ARC.HIS.SEA.ADP", "art_deco"), ("ARC.HIS.SEA.PMP", "philippine_modernism")], "source_evidence": PHILIPPINE_ARCHITECTURE_SOURCE_IDS, "result_type": "composed", "confidence": "deterministic", "rationale": "Theater architecture resolves through work anchors instead of a flat style list.", "fallback_reason": "composed_philippine_theater_architecture_path", "context_paths": ["HIS.GHA.CTS", "ARC.HIS.SEA.ADP"]},
    {"case_id": "ARCH-INT-061", "text": "How does Philippine civic architecture connect Old Legislative Building, Quezon Hall, Quezon Memorial Shrine, public space, and heritage?", "asset_context": "philippine_civic_heritage_path", "concept_path": "ARC.BTY.CIV", "path_refs": [("ARC.BTY.CIV", "civic_architecture"), ("FIG.WRK.BUI.OLB", "old_legislative_building"), ("FIG.WRK.BUI.QZH", "quezon_hall"), ("FIG.WRK.BUI.QMS", "quezon_memorial_shrine"), ("URB.PBR.CIV", "civic_space"), ("ARC.CHC", "cultural_heritage")], "source_evidence": PHILIPPINE_ARCHITECTURE_SOURCE_IDS, "result_type": "composed", "confidence": "deterministic", "rationale": "Civic architecture resolves through Philippine public-building anchors and public-space/heritage concepts.", "fallback_reason": "composed_philippine_civic_heritage_path", "context_paths": ["ARC.BTY.CIV", "URB.PBR.CIV"]},
    {"case_id": "ARCH-INT-062", "text": "How does Philippine work evidence connect source-safe metadata without exposing raw-source filename labels?", "asset_context": "philippine_source_safe_metadata_path", "concept_path": "ARC.HIS.SEA.PVA", "path_refs": [("ARC.HIS.SEA.PVA", "clean_concept"), ("FIG.WRK.BUI.BKB", "building_type_anchor"), ("MAT.TBB.BAS.BCM", "material_anchor"), ("ARC.TAC", "tropical_architecture")], "source_evidence": PHILIPPINE_ARCHITECTURE_SOURCE_IDS, "result_type": "single_value", "confidence": "deterministic", "rationale": "Default resolver output uses clean concept and work labels while source-rights rows retain only metadata-only provenance.", "fallback_reason": "exact_source_safe_clean_label_path", "context_paths": ["ARC.HIS.SEA.PVA", "ARC.TAC"]},
    {"case_id": "ARCH-INT-063", "text": "How do Filipino architect work paths avoid direct person-to-material shortcuts?", "asset_context": "philippine_no_direct_person_material_guardrail", "concept_path": "FIG.ARD.CAA.MAN", "path_refs": [("FIG.ARD.CAA.MAN", "person"), ("FIG.WRK.BUI.COC", "work_anchor"), ("MAT.TBB.BAS.CAP", "material_via_work"), ("ARC.HIS.SEA.PVA", "vernacular_context")], "source_evidence": PHILIPPINE_ARCHITECTURE_SOURCE_IDS, "result_type": "composed", "confidence": "deterministic", "rationale": "Person-material reasoning composes through work anchors, preserving the no generic direct person-to-material relationship guardrail.", "fallback_reason": "composed_no_direct_person_material_path", "context_paths": ["FIG.ARD.CAA.MAN", "MAT.TBB.BAS.CAP"]},
    {"case_id": "ARCH-INT-064", "text": "How does Philippine architecture search distinguish Tropical Architecture from source-rights metadata?", "asset_context": "philippine_search_clean_tropical_architecture", "concept_path": "ARC.TAC", "path_refs": [("ARC.TAC", "clean_tropical_architecture"), ("FIG.WRK.BUI.BKB", "bahay_kubo_anchor"), ("MAT.TBB.BAS.NIP", "nipa_material"), ("ARC.TAC.NVS", "natural_ventilation")], "source_evidence": PHILIPPINE_ARCHITECTURE_SOURCE_IDS, "result_type": "single_value", "confidence": "deterministic", "rationale": "Search and resolver cases pin the clean Tropical Architecture node and exclude raw-source metadata labels in learner-facing output.", "fallback_reason": "exact_clean_tropical_architecture_search_path", "context_paths": ["ARC.TAC"]},
    {"case_id": "ARCH-INT-065", "text": "How do Philippine works connect to LEA architecture history, materials, structures, and site-planning study?", "asset_context": "philippine_work_lea_subject_bridge", "concept_path": "ARC.REG.PHL.PAH", "path_refs": [("ARC.REG.PHL.PAH", "lea_history_practice_area"), ("FIG.WRK.BUI.CHS", "shell_concrete_work"), ("FIG.WRK.BUI.MTH", "art_deco_heritage_work"), ("FIG.WRK.BUI.BKB", "vernacular_material_work"), ("ARC.SIT.LAN", "site_landscape"), ("ARC.MAT", "materials_methods")], "source_evidence": PHILIPPINE_ARCHITECTURE_SOURCE_IDS, "result_type": "composed", "confidence": "deterministic", "rationale": "Philippine works compose LEA/ALE history, materials, structures, and site-planning study paths in a source-safe way.", "fallback_reason": "composed_philippine_work_lea_bridge_path", "context_paths": ["ARC.REG.PHL.PAH", "ARC.MAT"]},
])


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
            "level": level,
            "owner": OWNER,
            "parent_path_code": parent_path,
            "path_code": path_code,
            "pref_label": label,
            "provenance_note": "Metadata-only architecture interconnectivity enrichment; no protected source payload stored.",
            "quality_signal": "curated_public_reference_overlay",
            "record_type": "BackboneNode",
            "release_version": RELEASE_VERSION,
            "review_status": "steward_admitted",
            "scope_note": SCOPE_NOTE,
            "semantic_node_kind": node_kind,
            "interconnectivity_category": category,
            "source_family_ids": _dedupe(source_ids),
            "steward": OWNER,
            "visibility": "learner_facing",
        }
        records.append(record)
        path_to_record[path_code] = record
        id_to_record[record_id] = record
        added_nodes.append(record)
        aliases_added += len(full_aliases)
        if parent_path:
            add_edge(parent_path, "broader_than", path_code, "hierarchy", source_ids)
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
            "provenance_note": "Metadata-only architecture interconnectivity edge; no protected source payload stored.",
            "review_status": "steward_admitted",
            "semantic_overlay_category": category,
            "source_family_ids": _dedupe(source_ids),
            "to_id": to_record["id"],
        }
        relationships.append(edge)
        added_relationships.append(edge)
        edge_keys.add(key)

    def merge_existing(path_code: str, aliases: list[str], source_ids: list[str], node_kind: str, category: str) -> None:
        nonlocal aliases_added
        record = path_to_record.get(path_code)
        if record is None:
            return
        added = _merge_metadata(record, aliases, source_ids, node_kind, category)
        aliases_added += added
        if added:
            improved_nodes.add(path_code)

    for parent, suffix, label, aliases, definition, kind, category, source_ids in NODE_GROUPS:
        path_code = f"{parent}.{suffix}"
        add_node(path_code, label, len(path_code.split(".")), parent, definition, aliases, source_ids, kind, category)

    for path_code, (aliases, source_ids, node_kind, category) in IMPROVE_HINTS.items():
        merge_existing(path_code, aliases, source_ids, node_kind, category)

    for from_path, predicate, to_path, category, source_ids in RELATIONSHIPS:
        add_edge(from_path, predicate, to_path, category, _source_ids_for_paths(path_to_record, [from_path, to_path], source_ids))

    new_payload = {**payload, "records": records, "relationships": relationships}
    records_by_id = {record["id"]: record for record in records}
    material_nodes = [node for node in added_nodes if node.get("interconnectivity_category") == "materials_taxonomy"]
    person_nodes = [node for node in added_nodes if str(node.get("semantic_node_kind", "")).endswith(("person", "engineer", "architect", "engineer_architect", "designer_engineer", "structural_engineer", "civil_engineer", "architect_engineer")) or node.get("semantic_node_kind") in {"architect_person", "structural_engineer", "civil_engineer", "architect_engineer", "engineer_architect", "designer_engineer"}]
    pritzker_nodes = [node for node in added_nodes if "Pritzker laureate" in node.get("aliases", []) or any(str(alias).startswith("Pritzker ") for alias in node.get("aliases", []))]
    engineer_nodes = [node for node in added_nodes if node.get("path_code", "").startswith("FIG.ETS.STE.") or "engineer" in str(node.get("semantic_node_kind", ""))]
    work_nodes = [node for node in added_nodes if node.get("semantic_node_kind") == "work_project_anchor"]
    person_work_edges = [rel for rel in added_relationships if rel.get("semantic_overlay_category") in {"person_work", "filipino_architect_work"}]
    work_material_edges = [rel for rel in added_relationships if rel.get("semantic_overlay_category") == "work_material_system_movement"]
    material_property_edges = [rel for rel in added_relationships if rel.get("semantic_overlay_category") in {"material_property", "material_assembly", "material_method", "material_system", "material_structural_component", "material_finish_property", "material_locality", "material_perception", "material_cross_bridge", "wet_area_material", "ceiling_wall_assembly", "glazing_assembly", "waterproofing_assembly", "acoustic_material", "low_carbon_material", "passive_design_material", "tropical_material_path", "movement_material_path", "theory_materiality_path", "optical_property"}]
    lea_cross_categories = {
        "lea_materials_methods",
        "philippine_vernacular_materials",
        "tropical_materials",
        "tropical_material_path",
        "material_cross_bridge",
        "material_structural_component",
        "movement_material_path",
        "theory_materiality_path",
        "work_material_system_movement",
    }
    lea_cross_edges = [
        rel
        for rel in added_relationships
        if rel.get("semantic_overlay_category") in lea_cross_categories
        or rel.get("semantic_overlay_category", "").startswith(("lea_", "philippine_", "tropical_", "sanitation_", "accessibility_", "fire_", "sustainability_", "interiors_", "ceiling_", "glazing_"))
    ]
    engineer_structural_edges = [
        rel
        for rel in added_relationships
        if rel.get("semantic_overlay_category")
        in {"person_structure_system", "architect_engineer_role", "architect_engineer_index", "material_structural_component"}
    ]
    engineer_work_edges = [
        rel
        for rel in person_work_edges
        if records_by_id[rel["from_id"]]["path_code"].startswith("FIG.ETS.STE")
        or records_by_id[rel["from_id"]]["path_code"] in {"FIG.ARD.CAA.FOT"}
    ]
    work_structural_edges = [
        rel
        for rel in work_material_edges
        if records_by_id[rel["to_id"]]["path_code"].startswith(("ARC.BLD.STR", "STR.", "CIV.BRG"))
    ]
    engineer_structural_path_count = len(engineer_structural_edges) + len(engineer_work_edges) + len(work_structural_edges)
    pritzker_suffixes = {suffix for suffix, *_ in PRITZKER_ARCHITECTS}
    pritzker_person_work_edges = [
        rel
        for rel in person_work_edges
        if records_by_id[rel["from_id"]]["path_code"].split(".")[-1] in pritzker_suffixes
    ]
    pritzker_work_paths = {records_by_id[rel["to_id"]]["path_code"] for rel in pritzker_person_work_edges}
    pritzker_work_facet_edges = [
        rel
        for rel in work_material_edges
        if records_by_id[rel["from_id"]]["path_code"] in pritzker_work_paths
    ]
    pritzker_work_material_paths = min(len(pritzker_person_work_edges), len(pritzker_work_facet_edges))
    report = {
        "ok": True,
        "generation_method": GENERATION_METHOD,
        "input_record_count": len(payload["records"]),
        "output_record_count": len(records),
        "input_relationship_count": len(payload["relationships"]),
        "output_relationship_count": len(relationships),
        "added_node_count": len(added_nodes),
        "added_nodes_by_category": dict(sorted(Counter(node.get("interconnectivity_category") for node in added_nodes).items())),
        "added_nodes_by_kind": dict(sorted(Counter(node.get("semantic_node_kind") for node in added_nodes).items())),
        "improved_existing_node_count": len(improved_nodes),
        "improved_existing_path_codes": sorted(improved_nodes),
        "aliases_added_or_preserved_on_new_and_improved_nodes": aliases_added,
        "material_nodes_added_or_improved": len(material_nodes) + sum(1 for p in improved_nodes if p.startswith(("MAT", "ARC.MAT"))),
        "person_nodes_added_or_improved": len(person_nodes) + sum(1 for p in improved_nodes if p.startswith("FIG.ARD") or p.startswith("FIG.ETS")),
        "pritzker_laureate_nodes_added_or_improved": len(pritzker_nodes),
        "engineer_architect_engineer_nodes_added_or_improved": len(engineer_nodes),
        "work_project_nodes_added_or_improved": len(work_nodes),
        "added_relationship_count": len(added_relationships),
        "added_relationships_by_predicate": dict(sorted(Counter(rel.get("predicate") for rel in added_relationships).items())),
        "added_relationships_by_category": dict(sorted(Counter(rel.get("semantic_overlay_category") for rel in added_relationships).items())),
        "person_work_material_paths_added_or_improved": min(len(person_work_edges), len(work_material_edges)),
        "person_work_relationships_added_or_improved": len(person_work_edges),
        "work_material_system_movement_relationships_added_or_improved": len(work_material_edges),
        "material_property_method_assembly_relationships_added_or_improved": len(material_property_edges),
        "engineer_architect_engineer_structural_paths_added_or_improved": engineer_structural_path_count,
        "pritzker_person_work_material_paths_added_or_improved": pritzker_work_material_paths,
        "lea_ale_cross_subject_relationships_added_or_improved": len(lea_cross_edges),
        "rights_safety": _rights_safety(),
        "quality_controls": {
            "direct_person_to_material_edges_added": _direct_person_to_material_edges(added_relationships, records_by_id),
            "generic_related_to_edges_added": sum(1 for rel in added_relationships if rel.get("predicate") == "related_to"),
            "learner_facing_source_process_labels_added": _bad_label_count(added_nodes),
        },
    }
    return new_payload, report


def enrich_source_rights_registry(payload: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    rows = [dict(row) for row in payload.get("source_rights_registry", [])]
    existing = {row.get("source_id"): row for row in rows}
    added: list[dict[str, Any]] = []
    improved: list[str] = []
    for reference in SOURCE_REFERENCES:
        row = existing.get(reference["source_id"])
        if row is None:
            row = {
                "source_id": reference["source_id"],
                "source_family": reference["source_family"],
                "publisher_authority": reference["publisher_authority"],
                "edition_version_effective_date": "admission-time verification required",
                "official_url": reference["official_url"],
                "source_rights_class": reference["source_rights_class"],
                "clearance_state": reference["clearance_state"],
                "intended_vitruvius_use": reference["intended_vitruvius_use"],
                "steward_owner": OWNER,
                "declared_use_boundary": _metadata_boundary(),
                "currentness_check_date": "2026-04-29",
                "update_cadence": "before source admission and per architecture interconnectivity release",
                "blocking_notes": "content ingest blocked unless explicit rights/license/legal review permits it; this row is metadata-only provenance",
            }
            rows.append(row)
            existing[reference["source_id"]] = row
            added.append(row)
        else:
            before = json.dumps(row, sort_keys=True)
            row["source_rights_class"] = reference["source_rights_class"]
            row["clearance_state"] = reference["clearance_state"]
            row["intended_vitruvius_use"] = reference["intended_vitruvius_use"]
            row["declared_use_boundary"] = row.get("declared_use_boundary") or _metadata_boundary()
            row["blocking_notes"] = row.get("blocking_notes") or "content ingest blocked unless explicit rights/license/legal review permits it"
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
        "rights_safety": _rights_safety(),
    }


def enrich_resolver_fixture(payload: dict[str, Any], graph_payload: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    records_by_path = {record["path_code"]: record for record in graph_payload["records"]}
    existing_cases = list(payload.get("resolver_golden_cases", []))
    existing_by_id = {case.get("case_id"): case for case in existing_cases}
    added: list[dict[str, Any]] = []
    improved: list[str] = []
    for spec in RESOLVER_CASE_SPECS:
        case = _materialize_case(spec, records_by_path)
        if spec["case_id"] in existing_by_id:
            existing = existing_by_id[spec["case_id"]]
            before = json.dumps(existing, sort_keys=True)
            existing.clear()
            existing.update(case)
            if json.dumps(existing, sort_keys=True) != before:
                improved.append(spec["case_id"])
            continue
        existing_cases.append(case)
        added.append(case)
        existing_by_id[spec["case_id"]] = case
    return {**payload, "resolver_golden_cases": existing_cases}, {
        "ok": True,
        "generation_method": GENERATION_METHOD,
        "input_resolver_golden_case_count": len(payload.get("resolver_golden_cases", [])),
        "output_resolver_golden_case_count": len(existing_cases),
        "added_resolver_golden_case_count": len(added),
        "improved_resolver_golden_case_count": len(improved),
        "added_case_ids": [case["case_id"] for case in added],
        "improved_case_ids": improved,
        "rights_safety": _rights_safety(),
    }


def _materialize_case(spec: dict[str, Any], records_by_path: dict[str, dict[str, Any]]) -> dict[str, Any]:
    refs = []
    for path_code, role in spec.get("path_refs", []):
        if path_code not in records_by_path:
            raise KeyError(f"resolver case {spec['case_id']} references missing path {path_code}")
        refs.append({"node_id": records_by_path[path_code]["id"], "role": role})
    concept_path = spec.get("concept_path")
    concept_id = records_by_path[concept_path]["id"] if concept_path in records_by_path else "VTN-DOM-0000001"
    context_ids = [records_by_path[path]["id"] for path in spec.get("context_paths", []) if path in records_by_path]
    rationale = spec["rationale"]
    if spec["result_type"] == "composed" and "compose" not in rationale.lower() and "compatible" not in rationale.lower():
        rationale = f"{rationale} Compatible concepts compose into a multi-hop reasoning path."
    return {
        "case_id": spec["case_id"],
        "query": {
            "concept_id": concept_id,
            "asset_context": spec["asset_context"],
            "text": spec["text"],
            "context_ids": context_ids,
            "jurisdiction_filters": spec.get("jurisdiction_filters", ["global", "PH"]),
            "discipline_filters": spec.get("discipline_filters", ["architecture", "structures", "materials"]),
            "trace_requested": True,
        },
        "jurisdiction": spec.get("jurisdiction", "global"),
        "effective_date": "2026-04-29",
        "expected_result_type": spec["result_type"],
        "expected_confidence": spec["confidence"],
        "rationale": rationale,
        "source_evidence": spec["source_evidence"],
        "expected_node_refs": refs,
        "fallback_reason": spec["fallback_reason"],
        "trace_safe_rationale": "Metadata-only architecture interconnectivity resolver golden case; returns canonical node IDs and source IDs only, with no protected source text.",
        "owner": OWNER,
        "review_status": "candidate",
    }


def _source_ids_for_paths(path_to_record: dict[str, dict[str, Any]], paths: list[str], fallback: list[str]) -> list[str]:
    ids: list[str] = []
    for path in paths:
        record = path_to_record.get(path)
        if record:
            ids.extend(str(item) for item in record.get("source_family_ids", []) if item)
    return _dedupe([*ids, *fallback])


def _direct_person_to_material_edges(relationships: list[dict[str, Any]], records_by_id: dict[str, dict[str, Any]]) -> int:
    count = 0
    for rel in relationships:
        from_path = records_by_id[rel["from_id"]]["path_code"]
        to_path = records_by_id[rel["to_id"]]["path_code"]
        if from_path.startswith(("FIG.ARD", "FIG.ETS")) and to_path.startswith(("MAT", "ARC.MAT")):
            count += 1
    return count


def _bad_label_count(records: list[dict[str, Any]]) -> int:
    bad_patterns = ["raw-source", "filename metadata", "metadata-only source", "source-family reference", "protected payload", "reviewer candidate", "unknown/private", "local file", "registry row", "planning_reference_only"]
    return sum(1 for record in records if any(pattern in str(record.get("label", "")).lower() for pattern in bad_patterns))


def _next_domain_id(records: list[dict[str, Any]]) -> int:
    return max(int(record["id"].split("-")[-1]) for record in records if str(record.get("id", "")).startswith("VTN-DOM-")) + 1


def _merge_metadata(record: dict[str, Any], aliases: list[str], source_ids: list[str], node_kind: str, category: str) -> int:
    alias_count = _merge_list(record, "aliases", aliases)
    _merge_list(record, "source_family_ids", source_ids)
    record.setdefault("provenance_note", "Metadata-only architecture interconnectivity enrichment; no protected source payload stored.")
    record.setdefault("quality_signal", "curated_public_reference_overlay")
    record.setdefault("confidence", "high")
    record.setdefault("semantic_node_kind", node_kind)
    record.setdefault("interconnectivity_category", category)
    record.setdefault("visibility", "learner_facing")
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
    return "metadata-only names, public identifiers, source-family references, aliases, and original summaries; no biography text, protected work descriptions, essays, source payloads, reviewer text, exam questions, answer keys, protected tables, clauses, figures, or diagrams ingested"


def _rights_safety() -> dict[str, Any]:
    return {
        "protected_source_payloads_ingested": False,
        "source_payload_mode": "metadata_labels_aliases_original_summaries_ids_and_source_family_references_only",
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
    parser = argparse.ArgumentParser(description="Enrich architecture/materials/people/work interconnectivity in the file-backed AEC-MEPFS backbone.")
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
    report = {
        "ok": graph_report["ok"] and source_report["ok"] and resolver_report["ok"],
        "graph": graph_report,
        "source_rights_registry": source_report,
        "resolver_fixture": resolver_report,
    }
    report_path = Path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.write:
        fixture_path.write_text(json.dumps(enriched_graph, indent=2) + "\n", encoding="utf-8")
        registry_path.write_text(json.dumps(enriched_registry, indent=2) + "\n", encoding="utf-8")
        resolver_path.write_text(json.dumps(enriched_resolver, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
