"""Architecture/Civil/Structural enrichment for the file-backed Backbone.

The enrichment is metadata-only and runtime-disconnected: it adds admitted
Backbone nodes, typed relationship metadata, source-family rows, and resolver
QA cases without importing protected standards text or writing live graph
infrastructure.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

GENERATION_METHOD = "steward_governed_architecture_civil_structural_interrelationships_from_source_family_research"
HIERARCHY_GENERATION_METHOD = "steward_governed_architecture_civil_structural_hierarchy_from_source_family_research"
REFINEMENT_METHOD = "steward_governed_architecture_civil_structural_node_refinement_from_source_family_research"
REPORT_SCHEMA_VERSION = "aec-mepfs-architecture-civil-structural-enrichment-report/v1"
DEFAULT_BACKBONE_PATH = Path("scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json")
DEFAULT_SOURCE_RIGHTS_PATH = Path(".ai/03_plans/AEC-MEPFS-Backbone/registry-candidates/source-rights-registry.json")
DEFAULT_READINESS_FIXTURE_PATH = Path("scripts/tests/fixtures/aec_mepfs_backbone/valid_readiness_s2.json")
REPORT_ROOT = Path("006_System-Manifests/aec-mepfs-backbone/architecture-civil-structural-enrichment")
REPORT_FILENAME = "architecture-civil-structural-enrichment-report.json"
RAW_SOURCE_ROOT = Path("001_Raw-Source-Layer")
OWNER = "Philip Lewis"
RELEASE_VERSION = "0.1.0"
ACCESS_DATE = "2026-05-01"
PROVENANCE_NOTE = (
    "Metadata-only source-family synthesis for Architecture, Civil Engineering, "
    "Geotechnical, and Structural Engineering reasoning; no protected source "
    "text, clauses, formulas, tables, figures, or source payloads ingested."
)

SOURCE_ROWS = [
    ("SRC-US-ACCESS-BOARD-ADA-PROWAG", "US Access Board ADA and Public Right-of-Way Accessibility Guidelines public guidance", "US Access Board", "https://www.access-board.gov/ada/", "reference_only", "accessible-route, slope, curb-ramp, and site-to-building access relationships"),
    ("SRC-FHWA-HEC-22-URBAN-DRAINAGE", "FHWA HEC-22 Urban Drainage Design Manual", "Federal Highway Administration", "https://www.fhwa.dot.gov/engineering/hydraulics/pubs/10009/", "reference_only", "runoff, inlet, storm drain, hydraulic grade line, and detention relationships"),
    ("SRC-NOAA-ATLAS-14-PRECIPITATION-FREQUENCY", "NOAA Atlas 14 precipitation-frequency data", "National Oceanic and Atmospheric Administration", "https://hdsc.nws.noaa.gov/pfds/", "reference_only", "rainfall intensity-duration-frequency and design-storm basis relationships"),
    ("SRC-EPA-GREEN-INFRASTRUCTURE", "EPA green infrastructure and stormwater management public guidance", "United States Environmental Protection Agency", "https://www.epa.gov/green-infrastructure", "reference_only", "low-impact development, bioretention, permeable pavement, and runoff-reduction relationships"),
    ("SRC-FHWA-GEOTECH-SUBSURFACE-INVESTIGATION", "FHWA geotechnical site characterization and subsurface investigation references", "Federal Highway Administration", "https://www.fhwa.dot.gov/engineering/geotech/", "reference_only", "geotechnical investigation, bearing, settlement, groundwater, and foundation-interface relationships"),
    ("SRC-FHWA-ASCE-38-SUE-UTILITY-DATA", "FHWA subsurface utility engineering and ASCE 38 utility data-quality source family", "Federal Highway Administration and ASCE", "https://www.fhwa.dot.gov/programadmin/sueindex.cfm", "reference_only", "utility corridor, service-entry, cover, conflict, and data-quality relationships"),
    ("SRC-ACI-318-STRUCTURAL-CONCRETE", "ACI 318 structural concrete source-family metadata", "American Concrete Institute", "https://www.concrete.org/store/productdetail.aspx?ItemID=318U19", "reference_only", "structural concrete, slab, column, reinforcement, footing, and serviceability relationships"),
    ("SRC-AISC-360-STRUCTURAL-STEEL", "AISC 360 structural steel specification source-family metadata", "American Institute of Steel Construction", "https://www.aisc.org/Specification-for-Structural-Steel-Buildings-ANSIAISC-360-22-1", "reference_only", "structural steel members, connections, base plates, anchor bolts, and force-transfer relationships"),
    ("SRC-NIBS-WBDG-BUILDING-ENVELOPE", "WBDG building envelope design guide", "National Institute of Building Sciences Whole Building Design Guide", "https://www.wbdg.org/guides-specifications/building-envelope-design-guide", "reference_only", "envelope, waterproofing, air barrier, facade, roof, and movement-joint interface relationships"),
]

# id|path|label|definition|aliases(;)|clusters(;)
NODE_ROWS = """
VTN-DOM-0012738|ARC.SPC.CIR.ASR|Accessible Site-To-Building Route|A continuous architectural access path connecting site arrival points to building entrances while coordinating slope, clear width, thresholds, drainage, and jurisdiction-specific accessibility criteria.|accessible exterior route;barrier-free site route|acs_access_egress_site
VTN-DOM-0012739|ARC.SPC.CIR.EDS|Egress Discharge Site Interface|The point and route where exit discharge connects occupants from a building egress system to a site path, public way, refuge, or dispersal area.|exit discharge interface;site egress discharge|acs_access_egress_site
VTN-DOM-0012740|ARC.BLD.STR.AFD|Architectural Finished Floor Datum|A coordinated floor elevation datum that links building planning, thresholds, accessibility, flood-resilience assumptions, foundation interfaces, and site grading.|finished floor datum;floor elevation datum|acs_site_structure_datum
VTN-DOM-0012741|ARC.BLD.STR.FOC|Floor Opening Coordination|Architectural coordination of openings through floors or slabs for stairs, shafts, risers, services, or access while protecting structural, fire, acoustic, and waterproofing performance.|slab opening coordination;floor penetration coordination|acs_openings_fire_acoustic_structure
VTN-DOM-0012742|ARC.ENV.ROF.RDI|Roof Drainage Interface|The architectural envelope interface where roof falls, outlets, scuppers, gutters, overflows, waterproofing, and civil stormwater discharge are coordinated.|roof runoff interface;roof outlet coordination|acs_roof_stormwater_loads
VTN-DOM-0012743|ARC.ENV.WAL.FAI|Facade Anchor Interface|The coordinated interface where facade or cladding support transfers wind, dead load, movement, tolerance, and waterproofing demands into the primary or secondary structure.|cladding anchor interface;curtain wall anchor interface|acs_facade_wind_structure
VTN-DOM-0012744|ARC.DET.ENV.WCI|Waterproofing Continuity Interface|A detail interface that preserves water-control continuity across envelope transitions, roof outlets, movement joints, penetrations, and below-grade or podium conditions.|waterproofing transition;moisture-control continuity|acs_envelope_movement_water
VTN-DOM-0012745|ARC.TEC.JNT.MJC|Architectural Movement Joint Cover|An architectural cover, seal, or detail assembly that spans a structural or building movement joint while preserving access, fire, acoustic, waterproofing, and finish continuity where required.|expansion joint cover;movement joint cover|acs_envelope_movement_water
VTN-DOM-0012746|ARC.FIR.EGR.FSS|Architectural Fire Separation Strategy|Architectural planning of fire-resistance-rated separations, protected openings, exit enclosure relationships, and penetration protection without assuming universal code applicability.|fire separation strategy;compartmentation planning|acs_openings_fire_acoustic_structure
VTN-DOM-0012747|ARC.ECD.DAY.DOI|Daylight Opening Interface|A window, skylight, or aperture coordination concept linking daylight access with envelope, glare, heat gain, waterproofing, structure, and occupant experience.|daylight aperture interface;glazing daylight interface|acs_envelope_daylight_structure
VTN-DOM-0012748|ARC.ECD.ACO.ASI|Acoustic Separation Interface|A coordination interface where partitions, slabs, penetrations, joints, doors, and services preserve intended acoustic separation between spaces.|acoustic seal interface;sound separation interface|acs_openings_fire_acoustic_structure
VTN-DOM-0012749|CIV.SDV.GRD.FFE|Site Finished Floor Elevation Interface|A civil site-grading interface that coordinates finished floor elevation with drainage, flood risk, accessible routes, earthworks, thresholds, and foundation construction.|FFE interface;building pad elevation interface|acs_site_structure_datum
VTN-DOM-0012804|CIV.HDI.FCI.DFE|Design Flood Elevation Interface|A civil and architectural datum interface that links flood hazard applicability, site grading, finished-floor elevation, foundation detailing, and local flood-resistant design criteria without assuming universal jurisdictional adoption.|flood elevation interface;design flood datum|acs_site_structure_datum;acs_flood_resilience_foundation
VTN-DOM-0012750|CIV.SDV.GRD.TPS|Topography Survey Surface|A surveyed ground-surface representation used to inform grading, cut and fill, drainage paths, accessible route slopes, excavation, and civil quantity decisions.|existing ground survey;surveyed terrain surface|acs_site_topography_grading
VTN-DOM-0012751|CIV.LDE.EAB.CFB|Cut And Fill Balance|Earthworks coordination that estimates and sequences excavation and embankment quantities while managing haulage, compaction, drainage, contamination, and constructability constraints.|cut-fill balance;earthworks balance|acs_site_topography_grading
VTN-DOM-0012752|CIV.SDV.GRD.ESC|Civil Erosion And Sediment Control|Temporary or permanent civil measures used to reduce sediment-laden runoff from disturbed soil during construction and site operation.|sediment control;erosion control|acs_site_topography_grading
VTN-DOM-0012753|CIV.SDV.ACC.PSG|Pedestrian Site Gradient Control|Civil and accessibility coordination of walking-surface grade, cross slope, landings, transitions, and drainage along exterior pedestrian access routes.|exterior route slope control;pedestrian cross-slope control|acs_access_egress_site
VTN-DOM-0012754|CIV.SDV.ACC.EVA|Emergency Vehicle Access Route|A site access route planned for emergency response vehicles while coordinating grades, clear widths, turning geometry, obstructions, fire department access, and civil drainage.|fire apparatus access route;emergency access drive|acs_access_egress_site
VTN-DOM-0012755|CIV.DRN.HYD|Hydrologic Design Basis|A civil hydrology concept grouping rainfall, catchment, runoff timing, and design-storm assumptions used to size stormwater conveyance and detention systems.|stormwater hydrology basis;runoff design basis|acs_stormwater_hydrology
VTN-DOM-0012756|CIV.DRN.HYD.IDF|Rainfall Intensity Duration Frequency Basis|A precipitation-frequency basis used to select rainfall intensity for stormwater analysis while remaining region, edition, and currentness sensitive.|IDF basis;precipitation frequency basis|acs_stormwater_hydrology
VTN-DOM-0012757|CIV.DRN.HYD.TOC|Time Of Concentration|The runoff travel-time concept used to relate catchment geometry, surface condition, and flow path to stormwater peak-flow estimation.|runoff travel time;catchment time of concentration|acs_stormwater_hydrology
VTN-DOM-0012758|CIV.DRN.CON.SRO|Surface Runoff|Stormwater flowing over ground, pavement, roof discharge areas, or landscape surfaces before collection, infiltration, detention, or discharge.|overland runoff;surface stormwater flow|acs_stormwater_hydrology
VTN-DOM-0012759|CIV.DRN.CON.CBI|Catch Basin|A drainage inlet structure that collects surface runoff and conveys it into a storm sewer, sump, or conveyance path while requiring access and sediment maintenance.|stormwater inlet;drainage inlet|acs_stormwater_conveyance
VTN-DOM-0012760|CIV.DRN.CON.SSP|Storm Sewer Pipe|A stormwater conveyance pipe that carries collected runoff from inlets or roof connections toward detention, retention, infiltration, or outfall points.|storm drain pipe;stormwater conduit|acs_stormwater_conveyance
VTN-DOM-0012761|CIV.DRN.CON.HGL|Hydraulic Grade Line|An analytical representation of stormwater energy level used to assess pipe capacity, surcharge, inlet behavior, and backwater risk.|HGL;storm drain hydraulic grade line|acs_stormwater_conveyance
VTN-DOM-0012762|CIV.DRN.CON.ICV|Inlet Capacity|The hydraulic capacity of an inlet or catch basin to intercept runoff under design flow, grade, clogging, and maintenance assumptions.|storm inlet capacity;catch basin capture capacity|acs_stormwater_conveyance
VTN-DOM-0012763|CIV.DRN.CON.OVF|Overland Stormwater Overflow Path|A planned surface route for stormwater flows that exceed inlet or pipe capacity, intended to reduce uncontrolled ponding or damage where feasible.|major storm overflow route;overland relief path|acs_stormwater_resilience
VTN-DOM-0012764|CIV.DRN.CON.RDO|Roof Drainage Discharge Interface|The civil receiving interface where roof runoff from drains, leaders, scuppers, or downspouts enters surface flow, storm sewer, detention, or infiltration strategy.|roof runoff discharge;downspout discharge interface|acs_roof_stormwater_loads
VTN-DOM-0012765|CIV.DRN.CON.PDR|Perimeter Drain|A drainage component or path near below-grade walls, foundations, or retaining structures that manages groundwater or seepage where the design includes such drainage.|foundation drain;retaining wall drain|acs_retaining_groundwater_foundation
VTN-DOM-0012766|CIV.DRN.LID.BRC|Bioretention Cell|A vegetated low-impact stormwater practice that stores, filters, and infiltrates or underdrains runoff subject to soil, groundwater, maintenance, and overflow constraints.|rain garden;biofiltration cell|acs_low_impact_stormwater
VTN-DOM-0012767|CIV.DRN.LID.PPV|Permeable Pavement|A pavement system that can reduce surface runoff by allowing water to pass through wearing surface and storage layers subject to subgrade, clogging, maintenance, and traffic constraints.|pervious pavement;porous pavement|acs_low_impact_stormwater
VTN-DOM-0012768|CIV.MIS.UCC.USE|Utility Service Entry Coordination|Coordination of site utility corridors and building entry points for water, sewer, storm, power, telecom, fire services, cover, clearances, and conflict avoidance.|service entry coordination;utility penetration coordination|acs_utility_entry_site_structure
VTN-DOM-0012803|CIV.MIS.UCC.SUC|Subsurface Utility Conflict Review|A civil coordination review that compares utility records, SUE quality levels, field data, excavation limits, foundation layouts, and service-entry routes to identify conflicts before construction.|utility conflict review;SUE conflict review|acs_utility_entry_site_structure;acs_subsurface_utility_conflicts
VTN-DOM-0012805|CIV.MIS.UCC.UQL|Subsurface Utility Data Quality Level|A subsurface utility engineering information-quality concept used to distinguish record-based, surveyed, designated, and physically exposed utility evidence before design coordination or excavation.|SUE quality level;utility data-quality level;subsurface utility data quality|acs_utility_entry_site_structure;acs_subsurface_utility_conflicts
VTN-DOM-0012806|CIV.MIS.UCC.TPH|Test Hole Utility Verification|A targeted field verification activity that exposes or confirms a utility's position, depth, material, and conflict condition at selected locations before excavation, foundation, or service-entry work.|potholing;test pit verification;utility test hole;vacuum excavation verification|acs_utility_entry_site_structure;acs_subsurface_utility_conflicts
VTN-DOM-0012807|CIV.PAV.SBG|Pavement Subgrade Preparation|Civil preparation of the soil or aggregate support layer beneath pavement, coordinating compaction, drainage, moisture sensitivity, earthworks, and construction quality before pavement layers are placed.|subgrade preparation;pavement foundation;prepared subgrade|acs_pavement_access_drainage
VTN-DOM-0012808|CIV.PAV.PST|Pavement Structure Interface|A civil pavement-system interface linking surface layer, base, subbase, subgrade support, drainage, access-route performance, emergency vehicle movement, and maintenance conditions without prescribing project-specific thickness or material design.|pavement structure;pavement section interface;roadway pavement assembly|acs_pavement_access_drainage
VTN-DOM-0012809|CIV.SDV.ACC.CRG|Curb Ramp Geometry Interface|A civil and accessibility coordination interface for curb ramps, landings, flares, transitions, drainage, detectable warnings, and route continuity between sidewalks, crossings, site grades, and building approaches.|curb ramp interface;accessible curb transition;sidewalk ramp geometry|acs_access_egress_site;acs_pavement_access_drainage
VTN-DOM-0012810|CIV.SDV.ACC.EAG|Emergency Access Geometry Basis|A civil planning basis for emergency access route geometry, clear width, turning movement, vertical clearance, pavement performance, grading, and obstruction control subject to the adopted fire-service and AHJ strategy.|fire apparatus geometry basis;emergency route turning basis|acs_access_egress_site;acs_pavement_access_drainage
VTN-DOM-0012811|CIV.DRN.CON.SMA|Stormwater Maintenance Access Interface|An operational civil-drainage interface that preserves maintainable access to inlets, conveyance structures, overflow routes, and detention or retention assets for inspection, sediment removal, cleaning, and work-order response.|drainage maintenance access;storm inlet maintenance interface;stormwater O and M access|acs_stormwater_conveyance;acs_operations_handoff
VTN-DOM-0012812|OPS.AST.REG.CAR|Civil Asset Handover Record|A lifecycle handover record that links civil drainage, pavement, utility-entry, access-route, and survey information to asset-register fields, maintenance obligations, and operations-facing identifiers without admitting protected source payloads.|civil asset record;civil O and M asset record;site infrastructure asset record|acs_operations_handoff
VTN-DOM-0012813|CIV.RDC.PED.ATI|Accessible Public-Way Crossing Tie-In|A civil-access coordination interface that links accessible site routes, public-way crossing tie-ins, curb ramps, pedestrian gradients, drainage, and AHJ or public-right-of-way review without storing universal slope or clearance values.|public-way tie-in;accessible crossing tie-in;site crossing interface|acs_access_egress_site;acs_public_way_access
VTN-DOM-0012814|CIV.HDI.CCD.CDI|Culvert Drainage Interface|A civil hydraulic interface coordinating culvert conveyance, inlet and outlet control, tailwater, overflow bypass, scour screening, grading, and maintenance access without admitting project-specific hydraulic calculations.|culvert hydraulic interface;culvert conveyance interface|acs_stormwater_hydrology;acs_flood_resilience_foundation
VTN-DOM-0012815|CIV.PAV.PSI|Pavement Subgrade Interface|A pavement design interface linking prepared subgrade, support variability, drainage, utility restorations, emergency access performance, and maintenance triggers without prescribing section thickness or traffic design values.|pavement subgrade interface;pavement support interface|acs_pavement_access_drainage;acs_civil_specialty_modeling
VTN-DOM-0012816|STR.LOA.CBG|Structural Criteria Basis Gate|A non-numeric governance gate that links structural load concepts to project basis, AHJ adoption, risk category, seismic applicability, source-rights status, and steward approval before numerical criteria may be admitted.|load criteria gate;structural design-basis gate;adopted load basis gate|acs_structural_loads;acs_external_gate_scaffold
VTN-DOM-0012769|GEO.SIS.GTI|Geotechnical Investigation Interface|A process and information interface that translates subsurface exploration, testing, groundwater observations, and engineering interpretation into foundation, excavation, and site-risk assumptions.|subsurface investigation interface;geotechnical report interface|acs_geotech_foundation
VTN-DOM-0012770|GEO.SIS.SIR|Soil Infiltration Rate|A geotechnical and hydrologic property used to assess feasibility and sizing of infiltration-based stormwater practices, subject to test method, soil variability, and groundwater separation.|infiltration rate;percolation rate|acs_low_impact_stormwater
VTN-DOM-0012771|GEO.GWT.GDL|Groundwater Design Level|A design assumption or observed range for groundwater elevation used to coordinate excavation, dewatering, basement waterproofing, buoyancy, retaining walls, and infiltration feasibility.|design groundwater level;water table design level|acs_retaining_groundwater_foundation
VTN-DOM-0012772|GEO.FOE.ABP|Allowable Bearing Pressure|A geotechnical design value or recommendation expressing permissible foundation bearing pressure under defined assumptions, safety factors, settlement limits, and project context.|allowable soil pressure;allowable bearing capacity|acs_geotech_foundation
VTN-DOM-0012773|GEO.FOE.DSE|Differential Settlement Evaluation|Assessment of nonuniform foundation or ground movement and its compatibility with structure, facade, partitions, services, waterproofing, and serviceability expectations.|differential settlement check;settlement compatibility review|acs_geotech_foundation
VTN-DOM-0012774|STR.LOA.GRV.DDL|Structural Dead Load|Permanent gravity load from self-weight and fixed construction that forms part of structural load-path reasoning and design load combinations according to adopted basis.|dead load;permanent load;self weight|acs_structural_loads
VTN-DOM-0012775|STR.LOA.GRV.LVL|Occupancy Live Load|Occupancy or use-related imposed load that may vary by space function, occupancy, maintenance, storage, or adopted design criteria.|live load;imposed load;occupancy live load|acs_structural_loads
VTN-DOM-0012776|STR.LOA.ENV.RPL|Rain Ponding Load|Roof rainwater accumulation or ponding load concept used to coordinate drainage reliability, roof slope, deflection, overflow, and structural capacity where relevant.|roof rain load;ponding load|acs_roof_stormwater_loads
VTN-DOM-0012777|STR.LOA.LAT.WND|Structural Wind Load|Lateral and uplift load from wind acting on building envelope and structure, requiring source-specific design basis and coordination with facade, roof, and lateral systems.|wind load;wind action;wind pressure|acs_facade_wind_structure
VTN-DOM-0012778|STR.LOA.LAT.SEI|Structural Seismic Load|Earthquake-induced design action dependent on site hazard, structural system, mass, ductility, detailing, and adopted design basis.|seismic load;earthquake load;seismic action|acs_lateral_systems
VTN-DOM-0012779|STR.RCS.SBC.SLS|Suspended Slab System|A structural floor or roof slab spanning between supports and participating in gravity load transfer, diaphragm action, serviceability, openings, and construction sequencing.|suspended slab;framed slab|acs_vertical_load_path
VTN-DOM-0012780|STR.SSS.BEG.SBM|Structural Beam|A horizontal structural member that spans between supports and transfers loads from slabs, joists, walls, or secondary framing to girders, columns, walls, or cores.|beam member;primary beam|acs_vertical_load_path
VTN-DOM-0012781|STR.RCS.SBC.COL|Structural Column|A vertical or inclined structural compression member that transfers gravity and sometimes lateral forces from supported framing toward foundations.|column member;vertical load-bearing member|acs_vertical_load_path
VTN-DOM-0012782|STR.FND.SHL.FTG|Footing Foundation|A shallow foundation element that distributes column, wall, or frame reactions to supporting soil or rock subject to bearing, settlement, uplift, sliding, and constructability checks.|spread footing;isolated footing|acs_geotech_foundation
VTN-DOM-0012783|STR.FND.DEP.PFS|Pile Foundation System|A deep foundation system using piles or similar elements to transfer loads through weak near-surface soils to deeper strata or by shaft resistance under defined geotechnical assumptions.|pile system;deep pile foundation|acs_geotech_foundation
VTN-DOM-0012784|STR.FND.DEP.PCP|Pile Cap|A structural foundation component that collects loads from columns or walls and distributes them into a group of piles while coordinating reinforcement, tolerance, and construction sequencing.|pile cap foundation;pile group cap|acs_geotech_foundation
VTN-DOM-0012785|STR.FND.SHL.GRB|Grade Beam|A reinforced concrete beam at or near grade that ties foundations, supports walls, spans weak areas, or distributes loads according to the foundation strategy.|ground beam;foundation tie beam|acs_geotech_foundation
VTN-DOM-0012786|STR.FND.SHL.SOG|Slab-On-Grade|A slab supported by prepared subgrade or base layers whose performance depends on subgrade support, moisture, joints, loads, and construction quality.|ground-bearing slab;slab on ground|acs_geotech_foundation
VTN-DOM-0012787|STR.WSD.DIC.DIA|Diaphragm Action|Structural behavior by which floor or roof diaphragms collect and transfer lateral forces to collectors, chords, shear walls, frames, cores, or other lateral-force-resisting elements.|floor diaphragm action;roof diaphragm action|acs_lateral_systems
VTN-DOM-0012788|STR.WSD.DIC.CDR|Collector Drag Strut|A diaphragm force-transfer member or zone that collects lateral forces and delivers them to vertical lateral-force-resisting elements.|collector;drag strut|acs_lateral_systems
VTN-DOM-0012789|STR.WSD.DIC.DPO|Diaphragm Opening Coordination|Structural coordination of floor or roof diaphragm openings so force transfer, chords, collectors, fire separation, and service penetrations remain consistent with design intent.|diaphragm penetration coordination;large slab opening review|acs_openings_fire_acoustic_structure
VTN-DOM-0012790|STR.RCS.SWC.COR|Structural Core|A vertical structural core, often around stairs, lifts, or shafts, that can contribute to lateral stability, gravity support, egress protection, and service coordination.|core wall system;lateral core|acs_core_egress_lateral
VTN-DOM-0012791|STR.SSS.CBP.BPC|Base Plate Connection|A structural steel or hybrid connection interface that transfers column reactions into concrete foundations through base plate, anchors, grout, and bearing details.|column base plate;base connection|acs_connections_force_transfer
VTN-DOM-0012792|STR.SSS.CBP.ABG|Anchor Bolt Group|A group of anchor rods or bolts that transfers tension, shear, and positioning demands between base plates, embedded elements, supports, and concrete foundations.|anchor rods;foundation anchors|acs_connections_force_transfer
VTN-DOM-0012793|STR.SSS.CBP.FTC|Force Transfer Connection|A structural connection concept describing how axial, shear, moment, uplift, or diaphragm forces pass between members, plates, anchors, welds, bolts, and supporting elements.|load transfer connection;structural connection path|acs_connections_force_transfer
VTN-DOM-0012794|STR.SSS.CBP.MJT|Structural Movement Joint|A structural separation or movement joint arranged to accommodate thermal, shrinkage, seismic, settlement, or construction movement while coordinating envelope, fire, acoustic, and MEP crossings.|structural expansion joint;seismic separation joint|acs_envelope_movement_water
VTN-DOM-0012795|STR.SSS.MBF.LSS|Lateral Stability System|A structural system or combination of frames, walls, cores, braces, diaphragms, collectors, and foundations that resists lateral instability and transfers lateral actions to support.|lateral force resisting system;stability system|acs_lateral_systems
VTN-DOM-0012796|STR.RCS.SBC.DFC|Deflection Compatibility|Serviceability coordination that checks structural deflection, drift, shortening, or movement against partitions, facade, glazing, waterproofing, finishes, and occupant comfort.|movement compatibility;serviceability compatibility|acs_serviceability_interfaces
VTN-DOM-0012797|STR.FND.SHL.FBC|Foundation Bearing Capacity Interface|The structural-geotechnical interface where foundation geometry and load effects are checked against bearing pressure assumptions and settlement criteria.|foundation bearing check;soil bearing interface|acs_geotech_foundation
VTN-DOM-0012798|STR.FND.SHL.STP|Settlement Performance|Serviceability performance of foundations and supported structure under total and differential settlement, including impacts on envelope, finishes, services, and operation.|foundation settlement performance;settlement serviceability|acs_geotech_foundation
VTN-DOM-0012799|STR.FND.SHL.RTW|Structural Retaining Wall|A structural retaining element that resists lateral earth, surcharge, or water pressures while coordinating drainage, waterproofing, foundations, backfill, and site grading.|retaining wall structure;basement retaining wall|acs_retaining_groundwater_foundation
VTN-DOM-0012800|STR.TMA.TWS.TBR|Temporary Bracing|Temporary structural bracing used during erection, excavation, or construction sequencing to maintain stability before the permanent system is complete.|construction bracing;temporary stability bracing|acs_construction_sequence_stability
VTN-DOM-0012801|STR.TMA.TWS.ERS|Erection Stability Condition|A construction-stage structural condition in which incomplete framing, temporary works, crane loads, formwork, or sequencing controls are needed to maintain stability.|construction-stage stability;temporary erection stability|acs_construction_sequence_stability
VTN-DOM-0012802|STR.CON.RCO.RBR|Structural Reinforcing Bar|Steel reinforcement used in concrete members to resist tensile, shear, crack-control, development, and ductility demands according to the structural design basis.|reinforcing bar;rebar;reinforcement bar|acs_concrete_reinforcement
""".strip()

REFINEMENT_ROWS = """
ARC.SPC.CIR|circulation route planning;access circulation|acs_access_egress_site|spatial_planning_category|architecture;accessibility|planning;design;operation|SRC-US-ACCESS-BOARD-ADA-PROWAG;SRC-WBDG-SYSTEMS-INTEGRATION
ARC.ENV.ROF|roof envelope system;roof assembly planning|acs_roof_stormwater_loads|envelope_category|architecture;civil;structural|planning;design;construction;operation|SRC-NIBS-WBDG-BUILDING-ENVELOPE;SRC-FHWA-HEC-22-URBAN-DRAINAGE
ARC.ENV.WAL|facade system;external wall envelope|acs_facade_wind_structure|envelope_category|architecture;structural|planning;design;construction;operation|SRC-NIBS-WBDG-BUILDING-ENVELOPE;SRC-ASCE-SEI-7
CIV.SDV.GRD|grading design;site levels coordination|acs_site_topography_grading|civil_site_category|civil;architecture;geotechnical|planning;design;construction|SRC-FHWA-HEC-22-URBAN-DRAINAGE;SRC-WBDG-SYSTEMS-INTEGRATION
CIV.DRN.CON|stormwater conveyance;drainage conveyance path|acs_stormwater_conveyance|civil_drainage_category|civil|planning;design;construction;operation|SRC-FHWA-HEC-22-URBAN-DRAINAGE
CIV.DRN.LID|green infrastructure stormwater;low-impact stormwater controls|acs_low_impact_stormwater|civil_green_infrastructure_category|civil;sustainability|planning;design;operation;maintenance|SRC-EPA-GREEN-INFRASTRUCTURE
GEO.SIS|subsurface investigation;site characterization|acs_geotech_foundation|geotechnical_category|geotechnical;civil;structural|planning;design;construction|SRC-FHWA-GEOTECH-SUBSURFACE-INVESTIGATION
GEO.FOE|foundation geotechnical engineering;foundation soil interface|acs_geotech_foundation|geotechnical_category|geotechnical;structural|planning;design;construction|SRC-FHWA-GEOTECH-SUBSURFACE-INVESTIGATION
STR.RCS.SBC|slab beam column system;primary concrete frame components|acs_vertical_load_path|structural_system_category|structural|planning;design;construction;inspection|SRC-ACI-318-STRUCTURAL-CONCRETE;SRC-ASCE-SEI-7
STR.FND.SHL|shallow foundation system;near-surface foundation interface|acs_geotech_foundation|structural_foundation_category|structural;geotechnical|planning;design;construction;inspection|SRC-FHWA-GEOTECH-SUBSURFACE-INVESTIGATION;SRC-ACI-318-STRUCTURAL-CONCRETE
STR.WSD.DIC|diaphragm collector system;lateral load diaphragm system|acs_lateral_systems|structural_lateral_category|structural|planning;design;construction|SRC-ASCE-SEI-7;SRC-AISC-360-STRUCTURAL-STEEL
STR.SSS.CBP|connection and base plate force transfer;steel connection interface|acs_connections_force_transfer|structural_connection_category|structural|design;construction;inspection|SRC-AISC-360-STRUCTURAL-STEEL
""".strip()

# from_path|to_path|predicate|relation_type|category|nature(;)|weight|confidence|discipline(;)|lifecycle(;)|sources(;)|rationale
EDGE_ROWS = """
CIV.SDV.GRD.TPS|CIV.SDV.GRD|requires|informs_site_grading|site_condition|informational;physical|0.88|0.84|civil;geotechnical|planning;design|SRC-WBDG-SYSTEMS-INTEGRATION;SRC-FHWA-GEOTECH-SUBSURFACE-INVESTIGATION|Surveyed topography is an input for site grading because proposed levels, slopes, cut-fill, and runoff paths are measured against existing ground.
CIV.SDV.GRD.TPS|GEO.RSS.SLS|requires|informs_slope_stability_assessment|site_condition|informational;geotechnical|0.82|0.78|civil;geotechnical|planning;design|SRC-FHWA-GEOTECH-SUBSURFACE-INVESTIGATION;SRC-WBDG-SYSTEMS-INTEGRATION|Topographic survey surface information informs slope stability assessment by defining existing grades, slope geometry, drainage paths, and adjacent ground conditions.
GEO.RSS.SLS|CIV.SDV.GRD|constrains|constrains_grading_slope_stability|site_condition|geotechnical;physical;performance|0.84|0.80|geotechnical;civil|planning;design;construction|SRC-FHWA-GEOTECH-SUBSURFACE-INVESTIGATION;SRC-WBDG-SYSTEMS-INTEGRATION|Slope stability assessment constrains grading because proposed cuts, fills, and drainage patterns can change stability and construction risk.
GEO.RSS.SLS|STR.FND.SHL.RTW|constrains|constrains_retaining_wall_stability_basis|site_condition|geotechnical;structural|0.82|0.78|geotechnical;structural;civil|planning;design;construction|SRC-FHWA-GEOTECH-SUBSURFACE-INVESTIGATION;SRC-ASCE-SEI-7|Slope stability assessment constrains retaining wall basis by linking retained heights, ground movement risk, surcharge, drainage, and global stability considerations.
CIV.SDV.GRD|CIV.SDV.GRD.FFE|constrains|coordinates_finished_floor_elevation|coordination|physical;performance|0.88|0.82|civil;architecture;structural|planning;design;construction|SRC-ASCE-24-FLOOD-RESISTANT;SRC-WBDG-SYSTEMS-INTEGRATION|Site grading coordinates finished floor elevation so thresholds, drainage away from the building, flood assumptions, and foundation construction align.
CIV.SDV.GRD.FFE|ARC.BLD.STR.AFD|requires|sets_building_datum_interface|coordination|informational;physical|0.86|0.82|civil;architecture;structural|planning;design;construction|SRC-ASCE-24-FLOOD-RESISTANT;SRC-WBDG-SYSTEMS-INTEGRATION|The site finished-floor interface and architectural floor datum must be coordinated to avoid threshold, drainage, accessibility, and foundation mismatches.
COM.APP.FHA|CIV.HDI.FCI.DFE|constrains|sets_flood_elevation_applicability_basis|regulatory_authority|regulatory;informational|0.78|0.76|compliance;civil;architecture|planning;design|SRC-ASCE-24-FLOOD-RESISTANT;SRC-ICC-IBC-IPC-IFC-IECC-IEBC|Flood hazard applicability sets the source-family and AHJ-sensitive basis for whether a design flood elevation interface must constrain building datum and foundation coordination.
CIV.HDI.FCI.DFE|CIV.SDV.GRD.FFE|constrains|constrains_finished_floor_elevation_interface|site_condition|regulatory;physical;resilience|0.82|0.78|civil;architecture;structural|planning;design;construction|SRC-ASCE-24-FLOOD-RESISTANT;SRC-WBDG-SYSTEMS-INTEGRATION|A design flood elevation interface constrains finished-floor elevation coordination where flood-resistant design criteria, site grading, thresholds, and access remain jurisdiction-sensitive.
CIV.HDI.FCI.DFE|STR.FND.SHL.FTG|constrains|constrains_flood_resistant_foundation_interface|coordination|regulatory;physical;resilience|0.72|0.72|civil;structural;geotechnical|planning;design;construction|SRC-ASCE-24-FLOOD-RESISTANT;SRC-ACI-318-STRUCTURAL-CONCRETE|Flood elevation coordination can constrain foundation interface assumptions such as embedment, flood loads, scour exposure, durability, and construction sequencing without prescribing a universal code detail.
CIV.SDV.GRD|CIV.SDV.ACC.PSG|constrains|sets_pedestrian_gradient_basis|spatial_topological|physical;regulatory|0.84|0.80|civil;accessibility|planning;design;construction|SRC-US-ACCESS-BOARD-ADA-PROWAG;SRC-WBDG-SYSTEMS-INTEGRATION|Grading establishes walking-surface slopes and cross slopes that govern whether an exterior route can function as an accessible path.
CIV.SDV.ACC.PSG|ARC.SPC.CIR.ASR|constrains|constrains_accessible_route_slope_and_cross_slope|spatial_topological|physical;regulatory|0.88|0.84|civil;architecture;accessibility|planning;design;construction|SRC-US-ACCESS-BOARD-ADA-PROWAG|Pedestrian grade and cross-slope control are direct civil constraints on an accessible route from site arrival to building entrance.
ARC.SPC.CIR.ASR|CIV.SDV.ACC.PSG|requires|requires_pedestrian_gradient_control_for_accessible_route|coordination|physical;regulatory;performance|0.82|0.76|architecture;civil;accessibility|planning;design;construction;operation|SRC-US-ACCESS-BOARD-ADA-PROWAG;SRC-WBDG-SYSTEMS-INTEGRATION|An architectural accessible route depends on civil pedestrian gradient control so walking surfaces, landings, thresholds, and drainage transitions remain usable and code-checkable in the project jurisdiction.
ARC.SPC.CIR.EDS|FLS.EGR|part_of|part_of_egress_strategy|spatial_topological|safety-critical;functional|0.82|0.80|architecture;fire_safety|planning;design;operation|SRC-ICC-IBC-IPC-IFC-IECC-IEBC;SRC-NFPA-70-101-13-72-14-20|Exit discharge at the site is part of an egress strategy because occupants must continue from exits to a safe exterior path or public way.
ARC.SPC.CIR.EDS|CIV.SDV.ACC.EVA|constrains|coordinates_egress_discharge_with_site_access|coordination|safety-critical;physical|0.70|0.72|architecture;civil;fire_safety|planning;design;construction|SRC-ICC-IBC-IPC-IFC-IECC-IEBC;SRC-WBDG-SYSTEMS-INTEGRATION|Egress discharge planning must coordinate with site paths, emergency response access, grading, and obstructions without treating one code family as universal.
CIV.SDV.ACC.EVA|FLS.FDS.ACC|requires|supports_fire_apparatus_access|functional_service|safety-critical;physical|0.80|0.78|civil;fire_safety|planning;design;operation|SRC-NFPA-70-101-13-72-14-20;SRC-ICC-IBC-IPC-IFC-IECC-IEBC|Emergency vehicle access routes provide civil access geometry and clearances needed for fire apparatus access where required by the adopted strategy.
MAT.ASM.ROF|ARC.ENV.ROF.RDI|requires|requires_roof_drainage_interface|coordination|physical;performance|0.86|0.82|architecture;civil;structural|design;construction;operation|SRC-NIBS-WBDG-BUILDING-ENVELOPE;SRC-FHWA-HEC-22-URBAN-DRAINAGE|Roof assemblies require drainage interfaces to control water, protect waterproofing, limit ponding, and coordinate discharge to site stormwater paths.
ARC.ENV.ROF.RDI|CIV.DRN.CON.RDO|requires|discharges_roof_runoff_to_site_network|civil_hydraulic_flow|functional;physical|0.84|0.80|architecture;civil;plumbing|design;construction;operation|SRC-NIBS-WBDG-BUILDING-ENVELOPE;SRC-FHWA-HEC-22-URBAN-DRAINAGE|The roof drainage interface routes roof runoff to a civil receiving condition such as surface discharge, storm sewer, detention, or infiltration.
CIV.DRN.CON.RDO|CIV.MIS.STN|requires|connects_roof_discharge_to_stormwater_network|civil_hydraulic_flow|functional;physical|0.80|0.78|civil;architecture|design;construction;operation|SRC-FHWA-HEC-22-URBAN-DRAINAGE|Roof drainage discharge must be coordinated with the site stormwater network so downstream capacity and overflow paths are understood.
CIV.DRN.CON.RDO|CIV.DRN.CON.CBI|requires|routes_roof_runoff_to_stormwater_inlet_or_pipe|civil_hydraulic_flow|physical;performance|0.78|0.74|civil;architecture|design;construction;operation|SRC-FHWA-HEC-22-URBAN-DRAINAGE;SRC-NIBS-WBDG-BUILDING-ENVELOPE|Roof drainage discharge must be routed to a stormwater inlet, pipe, or approved discharge point, creating a traversable path from roof design to civil conveyance and detention checks.
CIV.SDV.GRD|CIV.DRN.CON.SRO|constrains|directs_surface_runoff|civil_hydraulic_flow|physical;performance|0.90|0.84|civil|planning;design;construction;operation|SRC-FHWA-HEC-22-URBAN-DRAINAGE|Grading establishes surface flow directions, ponding locations, and runoff paths before stormwater is collected, infiltrated, or conveyed.
CIV.DRN.CON.SRO|CIV.DRN.CON.CBI|requires|collected_by_inlet|civil_hydraulic_flow|functional;physical|0.86|0.82|civil|design;construction;operation|SRC-FHWA-HEC-22-URBAN-DRAINAGE|Surface runoff is collected by catch basins or inlets when the drainage strategy uses piped conveyance.
CIV.DRN.CON.CBI|CIV.DRN.CON.SSP|requires|drains_to_storm_pipe|civil_hydraulic_flow|functional;physical|0.88|0.84|civil|design;construction;operation|SRC-FHWA-HEC-22-URBAN-DRAINAGE|Catch basins convey captured runoff into storm sewer pipes or equivalent downstream conveyance paths.
CIV.DRN.CON.SSP|CIV.DRN.DET|requires|discharges_to_detention_or_outfall|civil_hydraulic_flow|functional;physical|0.82|0.78|civil;sustainability|design;construction;operation|SRC-FHWA-HEC-22-URBAN-DRAINAGE;SRC-EPA-GREEN-INFRASTRUCTURE|Storm sewer pipes discharge collected runoff toward detention, retention, infiltration, or outfall systems depending on the civil drainage strategy.
CIV.DRN.CON.HGL|CIV.DRN.CON.SSP|constrains|constrains_pipe_capacity_and_backwater|civil_hydraulic_flow|analytical;performance|0.82|0.78|civil|design;operation|SRC-FHWA-HEC-22-URBAN-DRAINAGE|Hydraulic grade line analysis constrains pipe sizing, surcharge, backwater, and inlet performance for storm drain systems.
CIV.DRN.CON.ICV|CIV.DRN.CON.CBI|constrains|sets_inlet_capture_capacity|civil_hydraulic_flow|analytical;performance|0.82|0.78|civil;operations|design;operation;maintenance|SRC-FHWA-HEC-22-URBAN-DRAINAGE|Inlet capacity determines how much runoff a catch basin captures before bypass, ponding, or overflow occurs.
CIV.SDV.GRD|CIV.DRN.CON.OVF|requires|requires_safe_overland_flow_path|risk|physical;resilience|0.78|0.74|civil;sustainability|planning;design;operation|SRC-FHWA-HEC-22-URBAN-DRAINAGE;SRC-WBDG-SYSTEMS-INTEGRATION|Site grading should identify overland overflow paths for flows exceeding inlet or pipe capacity to reduce uncontrolled ponding and damage.
CIV.DRN.HYD.IDF|CIV.DRN.HYD|requires|sets_design_rainfall_basis|site_condition|informational;analytical|0.86|0.82|civil|planning;design|SRC-NOAA-ATLAS-14-PRECIPITATION-FREQUENCY;SRC-FHWA-HEC-22-URBAN-DRAINAGE|Rainfall intensity-duration-frequency data provides a source-family basis for hydrologic design assumptions, subject to local currentness and adoption.
CIV.DRN.HYD.TOC|CIV.DRN.HYD|requires|sets_runoff_timing_basis|site_condition|analytical;performance|0.82|0.78|civil|planning;design|SRC-FHWA-HEC-22-URBAN-DRAINAGE|Time of concentration links catchment geometry and surface flow characteristics to peak-flow estimation.
CIV.DRN.HYD|CIV.DRN.DET|constrains|sizes_detention_storage|civil_hydraulic_flow|analytical;performance|0.82|0.78|civil;sustainability|planning;design|SRC-FHWA-HEC-22-URBAN-DRAINAGE;SRC-EPA-GREEN-INFRASTRUCTURE|Hydrologic design assumptions constrain detention and retention storage volumes, release rates, and overflow strategy.
CIV.DRN.LID.BRC|GEO.SIS.SIR|requires|depends_on_soil_infiltration_rate|site_condition|geotechnical;performance|0.82|0.78|civil;geotechnical;sustainability|planning;design;operation|SRC-EPA-GREEN-INFRASTRUCTURE;SRC-FHWA-GEOTECH-SUBSURFACE-INVESTIGATION|Bioretention and infiltration-based practices depend on soil infiltration rate, groundwater separation, underdrain strategy, and maintenance assumptions.
GEO.GWT.GDL|CIV.DRN.LID.BRC|constrains|constrains_infiltration_strategy|site_condition|geotechnical;performance|0.76|0.74|geotechnical;civil;sustainability|planning;design;operation|SRC-FHWA-GEOTECH-SUBSURFACE-INVESTIGATION;SRC-EPA-GREEN-INFRASTRUCTURE|High or variable groundwater can limit infiltration feasibility or require underdrains and overflow controls.
CIV.DRN.LID.PPV|CIV.DRN.CON.SRO|constrains|reduces_surface_runoff_when_maintained|civil_hydraulic_flow|performance;sustainability|0.68|0.72|civil;sustainability;operations|design;operation;maintenance|SRC-EPA-GREEN-INFRASTRUCTURE|Permeable pavement can reduce surface runoff when subgrade, storage, clogging, and maintenance conditions remain suitable.
CIV.SDV.GRD.ESC|CIV.DRN.CON.SRO|constrains|mitigates_sediment_runoff|risk|construction;sustainability|0.76|0.74|civil;construction;sustainability|construction;operation|SRC-EPA-GREEN-INFRASTRUCTURE;SRC-FHWA-HEC-22-URBAN-DRAINAGE|Erosion and sediment controls mitigate sediment transport in runoff from disturbed site areas during construction and stabilization.
CIV.MIS.UCC.USE|CIV.SDV.GRD|constrains|constrains_cover_clearance_and_finished_grade|coordination|physical;informational|0.78|0.74|civil;architecture;construction|planning;design;construction|SRC-FHWA-ASCE-38-SUE-UTILITY-DATA;SRC-WBDG-SYSTEMS-INTEGRATION|Utility service entry depth, cover, clearances, and conflict data constrain grading, slab penetrations, and building entry coordination.
CIV.MIS.UCC.SUC|STR.FND.SHL.FTG|constrains|constrains_foundation_layout_and_clearance|coordination|informational;physical|0.76|0.76|civil;structural;geotechnical|planning;design;construction|SRC-FHWA-ASCE-38-SUE-UTILITY-DATA;SRC-FHWA-GEOTECH-SUBSURFACE-INVESTIGATION|Subsurface utility conflict review constrains footing layout, clearances, protection zones, and redesign risk where existing or proposed utilities intersect foundation work.
CIV.MIS.UCC.SUC|GEO.EXC.SHR|constrains|constrains_excavation_support_and_utility_protection|construction_process|construction;safety-critical|0.74|0.74|civil;geotechnical;structural;construction|design;construction;inspection|SRC-FHWA-ASCE-38-SUE-UTILITY-DATA;SRC-FHWA-GEOTECH-SUBSURFACE-INVESTIGATION|Utility conflict review constrains excavation support and protection planning because buried utilities can affect shoring limits, temporary support, sequencing, and safe excavation methods.
CIV.MIS.UCC.SUC|CIV.MIS.UCC.USE|requires|informs_utility_service_entry_routing|coordination|informational;physical|0.80|0.78|civil;architecture;construction|planning;design;construction|SRC-FHWA-ASCE-38-SUE-UTILITY-DATA;SRC-WBDG-SYSTEMS-INTEGRATION|Subsurface utility conflict review informs utility service-entry routing so incoming services avoid avoidable conflicts with grading, foundations, existing utilities, and internal riser strategy.
CIV.MIS.UCC.USE|ARC.BLD.SRV.RIS|requires|coordinates_site_utility_entry_with_riser_strategy|coordination|physical;functional|0.70|0.70|civil;architecture;mechanical;electrical;plumbing|planning;design;construction|SRC-FHWA-ASCE-38-SUE-UTILITY-DATA;SRC-WBDG-SYSTEMS-INTEGRATION|Site utility entry points must coordinate with internal riser and service routing strategies without treating utility corridors as building shafts.
GEO.SIS.GTI|GEO.FOE.ABP|requires|derives_bearing_pressure_basis|site_condition|informational;geotechnical|0.88|0.84|geotechnical;structural|planning;design|SRC-FHWA-GEOTECH-SUBSURFACE-INVESTIGATION|Geotechnical investigation findings and interpretation provide the source-family basis for allowable bearing pressure recommendations.
GEO.SIS.GTI|GEO.FOE.DSE|requires|derives_settlement_design_basis|site_condition|informational;geotechnical|0.86|0.82|geotechnical;structural|planning;design|SRC-FHWA-GEOTECH-SUBSURFACE-INVESTIGATION|Subsurface exploration and testing inform total and differential settlement evaluation for foundation and building performance.
GEO.FOE.ABP|STR.FND.SHL.FBC|constrains|translates_soil_capacity_to_foundation_design|structural_load_path|geotechnical;analytical|0.90|0.86|geotechnical;structural|design;construction|SRC-FHWA-GEOTECH-SUBSURFACE-INVESTIGATION;SRC-ASCE-SEI-7|Allowable bearing pressure constrains structural foundation sizing and load transfer assumptions for shallow foundations.
STR.FND.SHL.FBC|STR.FND.SHL.FTG|requires|constrains_footing_selection|structural_load_path|analytical;physical|0.86|0.82|structural;geotechnical|design;construction|SRC-FHWA-GEOTECH-SUBSURFACE-INVESTIGATION;SRC-ACI-318-STRUCTURAL-CONCRETE|Foundation bearing checks constrain footing area, depth, reinforcement, and bearing interface decisions.
GEO.FOE.DSE|STR.FND.SHL.STP|constrains|sets_settlement_performance_basis|performance|geotechnical;serviceability|0.86|0.82|geotechnical;structural;architecture|design;operation|SRC-FHWA-GEOTECH-SUBSURFACE-INVESTIGATION;SRC-WBDG-SYSTEMS-INTEGRATION|Differential settlement evaluation sets a serviceability basis for foundation performance and compatibility with architectural and envelope systems.
GEO.GWT.GDL|STR.FND.SHL.FTG|constrains|constrains_foundation_excavation_and_dewatering|site_condition|geotechnical;construction|0.78|0.76|geotechnical;structural;civil|design;construction|SRC-FHWA-GEOTECH-SUBSURFACE-INVESTIGATION;SRC-NIBS-WBDG-BUILDING-ENVELOPE|Groundwater design level affects footing excavation, dewatering, waterproofing, uplift, and construction sequencing assumptions.
STR.LOA.GRV.DDL|STR.RCS.SBC.SLS|requires|imposes_dead_load_on_slab|structural_load_path|physical;analytical|0.88|0.84|structural|planning;design|SRC-ASCE-SEI-7;SRC-ACI-318-STRUCTURAL-CONCRETE|Dead load from permanent construction is a direct gravity action on suspended slabs and roof or floor systems.
STR.LOA.GRV.LVL|STR.RCS.SBC.SLS|requires|imposes_live_load_on_slab|structural_load_path|physical;analytical|0.86|0.82|structural;architecture|planning;design;operation|SRC-ASCE-SEI-7;SRC-ICC-IBC-IPC-IFC-IECC-IEBC|Live load depends on space use and occupancy assumptions and is applied to floor systems through the gravity load path.
ARC.SPC.OCP|STR.LOA.GRV.LVL|constrains|space_use_informs_live_load_basis|coordination|informational;analytical|0.76|0.76|architecture;structural|planning;design|SRC-ASCE-SEI-7;SRC-WBDG-SYSTEMS-INTEGRATION|Occupied space use informs live-load assumptions, reinforcing that space planning and structural load criteria are linked but distinct.
STR.RCS.SBC.SLS|STR.SSS.BEG.SBM|requires|transfers_gravity_load_to|structural_load_path|physical;functional|0.90|0.84|structural|design;construction;operation|SRC-ASCE-SEI-7;SRC-ACI-318-STRUCTURAL-CONCRETE|A suspended slab commonly transfers gravity loads to supporting beams, girders, walls, or columns depending on the framing system.
STR.SSS.BEG.SBM|STR.RCS.SBC.COL|requires|transfers_gravity_load_to|structural_load_path|physical;functional|0.90|0.84|structural|design;construction;operation|SRC-ASCE-SEI-7;SRC-AISC-360-STRUCTURAL-STEEL|A beam transfers supported gravity reactions to columns, walls, girders, or cores in the structural load path.
STR.RCS.SBC.COL|STR.FND.SHL.FTG|requires|transfers_gravity_load_to|structural_load_path|physical;functional|0.90|0.84|structural;geotechnical|design;construction;operation|SRC-ASCE-SEI-7;SRC-ACI-318-STRUCTURAL-CONCRETE|Columns transfer accumulated gravity loads and reactions into foundations or transfer structures.
STR.FND.SHL.FTG|GEO.FOE.ABP|requires|transfers_load_to_ground_capacity|structural_load_path|physical;geotechnical|0.88|0.82|structural;geotechnical|design;construction;operation|SRC-FHWA-GEOTECH-SUBSURFACE-INVESTIGATION;SRC-ACI-318-STRUCTURAL-CONCRETE|Footings transfer structural loads to soil or rock through a bearing interface checked against geotechnical capacity assumptions.
STR.FND.DEP.PCP|STR.FND.DEP.PFS|part_of|part_of_pile_foundation_system|physical_composition|physical;structural|0.84|0.80|structural;geotechnical|design;construction|SRC-FHWA-GEOTECH-SUBSURFACE-INVESTIGATION;SRC-ACI-318-STRUCTURAL-CONCRETE|Pile caps are components of pile foundation systems because they collect superstructure reactions and distribute them to pile groups.
STR.FND.SHL.GRB|STR.FND.SHL.FTG|requires|ties_shallow_foundations_and_wall_supports|structural_load_path|physical;functional|0.72|0.72|structural;geotechnical|design;construction|SRC-ACI-318-STRUCTURAL-CONCRETE|Grade beams can tie shallow foundations or support walls where the foundation strategy requires continuity across local ground or framing conditions.
STR.LOA.LAT.WND|ARC.ENV.WAL.FAI|constrains|imposes_wind_load_on_facade_interface|structural_load_path|physical;performance|0.86|0.82|structural;architecture|planning;design|SRC-ASCE-SEI-7;SRC-NIBS-WBDG-BUILDING-ENVELOPE|Wind load acts on facade and cladding interfaces and must be transferred through anchors to supporting structural elements.
ARC.ENV.WAL.FAI|STR.SSS.CBP.ABG|requires|anchors_facade_to_structure|coordination|physical;functional|0.80|0.76|architecture;structural|design;construction;inspection|SRC-NIBS-WBDG-BUILDING-ENVELOPE;SRC-AISC-360-STRUCTURAL-STEEL|Facade anchorage requires coordinated anchor groups or equivalent support hardware capable of transferring cladding loads and tolerances.
ARC.ENV.WAL.FAI|STR.SSS.CBP.FTC|requires|transfers_wind_load_to_frame|structural_load_path|physical;functional|0.82|0.78|architecture;structural|design;construction;operation|SRC-ASCE-SEI-7;SRC-NIBS-WBDG-BUILDING-ENVELOPE|Facade anchor interfaces transfer wind pressure reactions and self-weight into structural connections or framing.
STR.LOA.LAT.WND|STR.WSD.DIC.DIA|requires|imposes_lateral_load_on_diaphragm|structural_load_path|physical;analytical|0.82|0.80|structural|planning;design|SRC-ASCE-SEI-7|Wind actions can be collected by diaphragms and transferred to lateral force-resisting elements according to the structural system.
STR.LOA.LAT.SEI|STR.WSD.DIC.DIA|requires|imposes_lateral_load_on_diaphragm|structural_load_path|physical;analytical|0.82|0.80|structural;geotechnical|planning;design|SRC-ASCE-SEI-7;SRC-ASCE-SEISMIC-RESILIENCE|Seismic inertia forces are transferred through diaphragm action to collectors and lateral force-resisting systems in many building structures.
STR.WSD.DIC.DIA|STR.WSD.DIC.CDR|requires|transfers_lateral_load_to_collector|structural_load_path|physical;functional|0.90|0.84|structural|design;construction;operation|SRC-ASCE-SEI-7;SRC-AISC-360-STRUCTURAL-STEEL|Diaphragm action transfers lateral forces to collectors or drag struts that deliver those forces to vertical resisting elements.
STR.WSD.DIC.CDR|STR.RCS.SWC.COR|requires|transfers_lateral_load_to_core|structural_load_path|physical;functional|0.86|0.82|structural|design;construction;operation|SRC-ASCE-SEI-7;SRC-ACI-318-STRUCTURAL-CONCRETE|Collectors can transfer diaphragm forces into a structural core or other vertical lateral-force-resisting element.
STR.RCS.SWC.COR|STR.FND.SHL.FTG|requires|transfers_lateral_load_to_foundation|structural_load_path|physical;functional|0.82|0.78|structural;geotechnical|design;construction;operation|SRC-ASCE-SEI-7;SRC-ACI-318-STRUCTURAL-CONCRETE|A structural core transfers overturning, shear, and axial effects from lateral actions into foundations through its support conditions.
STR.SSS.MBF.LSS|STR.WSD.DIC.DIA|requires|receives_lateral_load_from_diaphragm|structural_load_path|physical;functional|0.80|0.78|structural|design;construction;operation|SRC-ASCE-SEI-7;SRC-AISC-360-STRUCTURAL-STEEL|The lateral stability system receives forces collected by diaphragms and transfers them to vertical resisting members and foundations.
STR.LOA.ENV.RPL|ARC.ENV.ROF.RDI|constrains|requires_drainage_to_limit_ponding_load|performance|physical;performance|0.82|0.78|structural;architecture;civil|design;operation|SRC-ASCE-SEI-7;SRC-FHWA-HEC-22-URBAN-DRAINAGE|Rain ponding load risk links roof drainage performance, overflow strategy, deflection, and structural design assumptions.
STR.LOA.ENV.RPL|STR.RCS.SBC.SLS|requires|imposes_roof_rain_load_on_structure|structural_load_path|physical;analytical|0.76|0.76|structural;architecture|design;operation|SRC-ASCE-SEI-7|Rain accumulation on roofs can impose gravity load on supporting slab or roof framing when drainage or deflection conditions permit ponding.
ARC.BLD.STR.FOC|STR.WSD.DIC.DPO|requires|requires_diaphragm_opening_coordination|coordination|physical;structural|0.86|0.82|architecture;structural|planning;design;construction|SRC-ASCE-SEI-7;SRC-WBDG-SYSTEMS-INTEGRATION|Large floor openings can interrupt diaphragm force transfer and therefore require explicit structural opening coordination.
ARC.BLD.STR.FOC|STR.RCS.SBC.SLS|requires|requires_slab_opening_review|coordination|physical;structural|0.86|0.82|architecture;structural|planning;design;construction;inspection|SRC-ACI-318-STRUCTURAL-CONCRETE;SRC-WBDG-SYSTEMS-INTEGRATION|Floor openings through slabs require review of trimming, reinforcement, load path, fire rating, acoustic separation, and constructability.
ARC.BLD.STR.FOC|STR.SSS.BEG.SBM|constrains|requires_beam_trimmer_review|coordination|physical;structural|0.74|0.74|architecture;structural|planning;design;construction|SRC-ASCE-SEI-7;SRC-WBDG-SYSTEMS-INTEGRATION|Openings near beams or framing can require trimming, reinforcement, or alternate support so load transfer remains clear.
ARC.BLD.STR.FOC|MAT.ASM.FRW|constrains|requires_fire_separation_reinstatement|coordination|safety-critical;physical|0.78|0.76|architecture;fire_safety;structural|design;construction;inspection|SRC-ICC-IBC-IPC-IFC-IECC-IEBC;SRC-NFPA-70-101-13-72-14-20|Floor openings through rated construction require fire-separation continuity review rather than assuming the opening is harmless.
ARC.BLD.STR.FOC|ARC.ECD.ACO.ASI|requires|requires_acoustic_seal_coordination|coordination|performance;physical|0.68|0.70|architecture;structural|design;construction;operation|SRC-WBDG-SYSTEMS-INTEGRATION;SRC-NIBS-WBDG-BUILDING-ENVELOPE|Openings, shafts, and penetrations can bypass acoustic separation unless seals, assemblies, and service routes are coordinated.
STR.RCS.SBC.DFC|ARC.INT.PAC|constrains|constrains_partition_deflection_compatibility|performance|serviceability;physical|0.78|0.76|structural;architecture|design;construction;operation|SRC-ASCE-SEI-7;SRC-WBDG-SYSTEMS-INTEGRATION|Structural deflection compatibility constrains partition detailing, head tracks, jointing, and finish performance.
STR.RCS.SBC.DFC|ARC.ENV.WAL|constrains|constrains_facade_deflection_compatibility|performance|serviceability;physical|0.80|0.78|structural;architecture|design;construction;operation|SRC-ASCE-SEI-7;SRC-NIBS-WBDG-BUILDING-ENVELOPE|Facade systems must accommodate structural deflection, drift, and tolerances to maintain envelope performance and avoid distress.
ARC.TEC.JNT.MJC|STR.SSS.CBP.MJT|requires|covers_structural_movement_joint|physical_composition|physical;functional|0.82|0.78|architecture;structural|design;construction;maintenance|SRC-NIBS-WBDG-BUILDING-ENVELOPE;SRC-ASCE-SEI-7|Architectural movement joint covers span or protect structural movement joints while allowing intended movement and preserving finish continuity.
STR.SSS.CBP.MJT|ARC.DET.ENV.WCI|requires|requires_waterproofing_continuity_detail|coordination|physical;performance|0.82|0.78|structural;architecture|design;construction;maintenance|SRC-NIBS-WBDG-BUILDING-ENVELOPE|Structural movement joints crossing the envelope require waterproofing continuity details to allow movement without uncontrolled leakage.
ARC.BLD.STR.EXJ|ARC.TEC.JNT.MJC|requires|requires_architectural_joint_cover|coordination|physical;functional|0.78|0.76|architecture;structural|design;construction;maintenance|SRC-NIBS-WBDG-BUILDING-ENVELOPE;SRC-WBDG-SYSTEMS-INTEGRATION|An expansion joint in building planning usually requires an architectural cover or seal strategy where it crosses occupied or envelope areas.
STR.SSS.CBP.BPC|STR.SSS.CBP.ABG|requires|requires_anchor_bolt_group|physical_composition|physical;structural|0.86|0.82|structural|design;construction;inspection|SRC-AISC-360-STRUCTURAL-STEEL;SRC-ACI-318-STRUCTURAL-CONCRETE|Base plate connections commonly rely on anchor bolt groups to transfer tension, shear, and positioning demands into the supporting foundation.
STR.SSS.CBP.ABG|STR.FND.SHL.FTG|requires|anchors_column_base_to_foundation|structural_load_path|physical;functional|0.84|0.80|structural|design;construction;inspection|SRC-AISC-360-STRUCTURAL-STEEL;SRC-ACI-318-STRUCTURAL-CONCRETE|Anchor bolts connect base plates to concrete foundations so column-base forces can be transferred safely.
STR.CON.RCO.RBR|STR.RCS.SBC.SLS|requires|reinforces_concrete_member|material_behavior|physical;structural|0.86|0.82|structural;materials|design;construction;inspection|SRC-ACI-318-STRUCTURAL-CONCRETE|Reinforcing bars are placed in concrete slabs or members to resist tensile, shear, crack-control, and ductility demands according to design.
GEO.RSS.LEP|STR.FND.SHL.RTW|constrains|sets_retaining_wall_pressure_basis|site_condition|geotechnical;analytical|0.88|0.84|geotechnical;structural;civil|planning;design|SRC-FHWA-GEOTECH-SUBSURFACE-INVESTIGATION;SRC-ASCE-SEI-7|Lateral earth pressure parameters constrain retaining wall design actions, support conditions, drainage, and stability checks.
STR.FND.SHL.RTW|GEO.RSS.LEP|requires|resists_lateral_earth_pressure|structural_load_path|physical;geotechnical|0.90|0.84|structural;geotechnical;civil|design;construction;operation|SRC-FHWA-GEOTECH-SUBSURFACE-INVESTIGATION;SRC-ACI-318-STRUCTURAL-CONCRETE|A retaining wall is structurally arranged to resist lateral earth pressure and transfer the resulting forces into its foundation or restraint system.
STR.FND.SHL.RTW|CIV.DRN.CON.PDR|requires|requires_rear_drainage_or_pressure_relief|civil_hydraulic_flow|geotechnical;physical|0.78|0.76|structural;civil;geotechnical|design;construction;operation;maintenance|SRC-FHWA-GEOTECH-SUBSURFACE-INVESTIGATION;SRC-NIBS-WBDG-BUILDING-ENVELOPE|Retaining structures commonly require drainage or pressure-relief coordination to limit hydrostatic pressure where the design includes drained behavior.
GEO.GWT.GDL|STR.FND.SHL.RTW|constrains|constrains_hydrostatic_pressure_design|site_condition|geotechnical;performance|0.80|0.78|geotechnical;structural;civil|planning;design;operation|SRC-FHWA-GEOTECH-SUBSURFACE-INVESTIGATION;SRC-NIBS-WBDG-BUILDING-ENVELOPE|Groundwater design level constrains retaining wall waterproofing, drainage, buoyancy, and hydrostatic pressure assumptions.
CIV.SDV.GRD|STR.FND.SHL.RTW|constrains|coordinates_grading_with_retaining_wall|coordination|physical;geotechnical|0.78|0.76|civil;structural;geotechnical|planning;design;construction|SRC-FHWA-GEOTECH-SUBSURFACE-INVESTIGATION;SRC-WBDG-SYSTEMS-INTEGRATION|Grading changes retained heights, surcharge, drainage patterns, and access around retaining walls.
GEO.EXC.SHR|STR.TMA.TWS.TBR|requires|requires_temporary_bracing_for_excavation_support|construction_process|construction;safety-critical|0.78|0.76|geotechnical;structural;construction|design;construction;inspection|SRC-FHWA-GEOTECH-SUBSURFACE-INVESTIGATION;SRC-ASCE-SEI-7|Excavation support can require temporary bracing or struts to maintain stability until permanent works or backfill are complete.
STR.TMA.TWS.TBR|STR.TMA.TWS.ERS|requires|maintains_erection_stability|construction_process|construction;safety-critical|0.84|0.80|structural;construction|design;construction;inspection|SRC-ASCE-SEI-7;SRC-WBDG-SYSTEMS-INTEGRATION|Temporary bracing is a means of maintaining construction-stage stability before the permanent lateral or gravity system is complete.
CON.TMP.FOR|STR.TMA.TWS.ERS|requires|supports_concrete_until_strength_gain|construction_process|construction;physical|0.72|0.72|construction;structural|construction;inspection|SRC-ACI-318-STRUCTURAL-CONCRETE;SRC-WBDG-SYSTEMS-INTEGRATION|Formwork and temporary support maintain geometry and stability while concrete gains sufficient strength for the next sequence.
CIV.LDE.EAB.CFB|CIV.SDV.GRD|requires|balances_earthworks_for_grading_design|construction_process|physical;informational|0.76|0.74|civil;geotechnical;construction|planning;design;construction|SRC-FHWA-GEOTECH-SUBSURFACE-INVESTIGATION;SRC-WBDG-SYSTEMS-INTEGRATION|Cut-and-fill balance is part of grading design because earthworks quantities, haulage, compaction, and drainage influence feasible site levels.
CIV.LDE.EAB.CFB|STR.FND.SHL.SOG|constrains|constrains_subgrade_preparation_for_slab_on_grade|site_condition|physical;geotechnical|0.74|0.74|civil;geotechnical;structural|design;construction|SRC-FHWA-GEOTECH-SUBSURFACE-INVESTIGATION;SRC-ACI-318-STRUCTURAL-CONCRETE|Earthworks, compaction, and subgrade preparation influence slab-on-grade support and long-term performance.
STR.FND.SHL.SOG|GEO.FOE.DSE|constrains|sensitive_to_differential_settlement|performance|geotechnical;serviceability|0.72|0.72|structural;geotechnical|design;operation|SRC-FHWA-GEOTECH-SUBSURFACE-INVESTIGATION;SRC-ACI-318-STRUCTURAL-CONCRETE|Slab-on-grade performance can be sensitive to differential settlement, subgrade moisture, and support variability.
ARC.ECD.DAY.DOI|ARC.ENV.WAL.FAI|constrains|coordinates_daylight_opening_with_facade_anchor_layout|coordination|physical;performance|0.66|0.70|architecture;structural;sustainability|planning;design;construction|SRC-NIBS-WBDG-BUILDING-ENVELOPE;SRC-WBDG-SYSTEMS-INTEGRATION|Daylight openings and facade anchors must be coordinated so glazing, mullions, brackets, tolerances, and structure do not conflict.
ARC.FIR.EGR.FSS|ARC.BLD.STR.FOC|constrains|requires_opening_protection_strategy|regulatory_authority|safety-critical;regulatory|0.80|0.78|architecture;fire_safety;structural|planning;design;inspection|SRC-ICC-IBC-IPC-IFC-IECC-IEBC;SRC-NFPA-70-101-13-72-14-20|A fire separation strategy constrains how floor openings, shafts, doors, and penetrations are protected without assuming one jurisdiction's code universally applies.
ARC.ECD.ACO.ASI|ARC.BLD.STR.FOC|constrains|requires_acoustic_continuity_at_opening|performance|performance;physical|0.70|0.72|architecture;structural|design;construction;operation|SRC-WBDG-SYSTEMS-INTEGRATION;SRC-NIBS-WBDG-BUILDING-ENVELOPE|Acoustic separation interfaces constrain opening and shaft detailing where sound flanking paths would compromise intended room separation.
STR.FND.SHL.STP|ARC.DET.ENV.WCI|constrains|settlement_affects_waterproofing_continuity|performance|serviceability;physical|0.66|0.70|structural;geotechnical;architecture|design;operation;maintenance|SRC-FHWA-GEOTECH-SUBSURFACE-INVESTIGATION;SRC-NIBS-WBDG-BUILDING-ENVELOPE|Settlement and differential movement can distress waterproofing continuity at podium, below-grade, or envelope transitions.
STR.RCS.SWC.COR|ARC.SPC.CIR.EDS|constrains|coordinates_core_with_egress_discharge|coordination|safety-critical;physical|0.70|0.72|structural;architecture;fire_safety|planning;design;construction|SRC-ASCE-SEI-7;SRC-ICC-IBC-IPC-IFC-IECC-IEBC|Structural cores often coordinate with stairs, shafts, and egress paths, linking lateral stability with circulation and life-safety planning.
STR.WSD.DIC.DPO|ARC.BLD.SRV.RIS|constrains|coordinates_riser_opening_with_diaphragm_path|coordination|physical;structural|0.74|0.76|structural;architecture;mechanical;electrical;plumbing|planning;design;construction|SRC-ASCE-SEI-7;SRC-WBDG-SYSTEMS-INTEGRATION|Riser openings through floor diaphragms must be coordinated so service routing does not break force-transfer or fire-separation intent.
STR.SSS.CBP.MJT|FLS.CMP.PEN.FST|constrains|requires_firestop_movement_capability_review|coordination|safety-critical;physical|0.66|0.70|structural;fire_safety;architecture|design;construction;inspection|SRC-ICC-IBC-IPC-IFC-IECC-IEBC;SRC-NIBS-WBDG-BUILDING-ENVELOPE|Movement joints crossing rated assemblies or services require firestop and joint systems that accommodate expected movement.
CIV.MIS.UCC.UQL|CIV.MIS.UCC.SUC|constrains|qualifies_utility_conflict_evidence_strength|information_management|informational;risk|0.86|0.82|civil;construction|planning;design;construction|SRC-FHWA-ASCE-38-SUE-UTILITY-DATA|Subsurface utility data quality levels qualify how strongly utility evidence should affect conflict review, route selection, excavation planning, and uncertainty communication.
CIV.MIS.UCC.TPH|CIV.MIS.UCC.UQL|requires|verifies_utility_quality_level_by_exposure|construction_process|informational;physical|0.82|0.80|civil;construction;geotechnical|design;construction;inspection|SRC-FHWA-ASCE-38-SUE-UTILITY-DATA|Test-hole verification can upgrade or confirm utility-location confidence by physically exposing selected utilities before construction decisions rely on the data.
CIV.MIS.UCC.UQL|CIV.MIS.UCC.USE|constrains|informs_utility_service_entry_uncertainty|coordination|informational;physical|0.76|0.76|civil;architecture;construction|planning;design;construction|SRC-FHWA-ASCE-38-SUE-UTILITY-DATA;SRC-WBDG-SYSTEMS-INTEGRATION|Utility data-quality metadata informs service-entry routing because low-confidence location information increases conflict, redesign, and excavation-protection risk.
CIV.MIS.UCC.TPH|STR.FND.SHL.FTG|constrains|confirms_foundation_clearance_before_excavation|coordination|informational;physical|0.70|0.72|civil;geotechnical;structural;construction|design;construction;inspection|SRC-FHWA-ASCE-38-SUE-UTILITY-DATA;SRC-FHWA-GEOTECH-SUBSURFACE-INVESTIGATION|Targeted utility verification can confirm clearance or reveal conflicts before footing excavation, shoring, service-entry, or redesign decisions proceed.
CIV.PAV.SBG|CIV.PAV.PST|requires|supports_pavement_structure_performance|site_condition|physical;performance|0.84|0.80|civil;geotechnical|design;construction;operation|SRC-FHWA-GEOTECH-SUBSURFACE-INVESTIGATION;SRC-FHWA-HEC-22-URBAN-DRAINAGE|Prepared subgrade supports pavement structure performance by controlling support, compaction, moisture, drainage, and construction variability before pavement layers are placed.
CIV.LDE.EAB.CFB|CIV.PAV.SBG|constrains|constrains_pavement_subgrade_preparation|construction_process|physical;geotechnical|0.78|0.76|civil;geotechnical;construction|planning;design;construction|SRC-FHWA-GEOTECH-SUBSURFACE-INVESTIGATION;SRC-WBDG-SYSTEMS-INTEGRATION|Cut-fill balance and earthworks sequencing constrain subgrade preparation because fill quality, compaction, drainage, and moisture conditions affect pavement support.
CIV.SDV.GRD|CIV.PAV.SBG|constrains|coordinates_finished_grades_with_subgrade|coordination|physical;performance|0.74|0.74|civil;geotechnical|design;construction|SRC-FHWA-GEOTECH-SUBSURFACE-INVESTIGATION;SRC-FHWA-HEC-22-URBAN-DRAINAGE|Site grading coordinates pavement subgrade elevations and drainage paths so surface grades, base layers, and runoff control align.
CIV.PAV.PST|CIV.SDV.ACC.EVA|requires|supports_emergency_access_surface_performance|functional_service|physical;safety-critical|0.76|0.74|civil;fire_safety;operations|design;construction;operation|SRC-ICC-IBC-IPC-IFC-IECC-IEBC;SRC-WBDG-SYSTEMS-INTEGRATION|Pavement structure performance supports emergency access routes by providing a durable surface capable of supporting the adopted response strategy without encoding project-specific vehicle loads.
CIV.DRN.LID.PPV|CIV.PAV.SBG|requires|requires_subgrade_infiltration_and_storage_basis|site_condition|geotechnical;performance;sustainability|0.70|0.72|civil;geotechnical;sustainability|planning;design;operation;maintenance|SRC-EPA-GREEN-INFRASTRUCTURE;SRC-FHWA-GEOTECH-SUBSURFACE-INVESTIGATION|Permeable pavement performance depends on subgrade support, infiltration or underdrain assumptions, storage capacity, clogging risk, and maintenance conditions.
CIV.SDV.ACC.CRG|ARC.SPC.CIR.ASR|constrains|constrains_accessible_route_transition_geometry|spatial_topological|physical;regulatory|0.82|0.80|civil;architecture;accessibility|planning;design;construction|SRC-US-ACCESS-BOARD-ADA-PROWAG;SRC-WBDG-SYSTEMS-INTEGRATION|Curb-ramp geometry constrains accessible route continuity at transitions between roadway, sidewalk, site grade, and building approach without prescribing universal dimensions.
CIV.SDV.GRD|CIV.SDV.ACC.CRG|constrains|constrains_curb_ramp_running_and_cross_slope|spatial_topological|physical;regulatory|0.78|0.76|civil;accessibility|planning;design;construction|SRC-US-ACCESS-BOARD-ADA-PROWAG;SRC-FHWA-HEC-22-URBAN-DRAINAGE|Site grading constrains curb-ramp running slope, cross slope, landings, drainage, and tie-in elevations because accessibility and stormwater performance share the transition zone.
CIV.DRN.CON.SRO|CIV.SDV.ACC.CRG|constrains|requires_drainage_to_limit_accessible_transition_ponding|civil_hydraulic_flow|physical;performance|0.66|0.70|civil;accessibility;operations|design;operation;maintenance|SRC-US-ACCESS-BOARD-ADA-PROWAG;SRC-FHWA-HEC-22-URBAN-DRAINAGE|Surface-runoff behavior constrains curb-ramp and accessible-transition detailing because ponding, sediment, or ice-prone drainage conditions can degrade route usability.
CIV.SDV.ACC.EAG|CIV.SDV.ACC.EVA|constrains|sets_emergency_access_turning_and_clearance_basis|coordination|physical;safety-critical|0.82|0.78|civil;fire_safety|planning;design;operation|SRC-ICC-IBC-IPC-IFC-IECC-IEBC;SRC-WBDG-SYSTEMS-INTEGRATION|Emergency access geometry basis constrains the route concept by capturing turning, clearance, obstruction, grade, and fire-service coordination assumptions subject to AHJ adoption.
CIV.PAV.PST|CIV.SDV.ACC.EAG|requires|supports_emergency_access_geometry_with_pavement_basis|functional_service|physical;safety-critical|0.72|0.72|civil;fire_safety;operations|design;construction;operation|SRC-ICC-IBC-IPC-IFC-IECC-IEBC;SRC-WBDG-SYSTEMS-INTEGRATION|The pavement structure interface supports emergency access geometry because route feasibility depends on surface durability, grades, curbs, drainage, and maintenance conditions.
COM.APP.AHJ|CIV.SDV.ACC.EAG|constrains|sets_emergency_access_adoption_basis|regulatory_authority|regulatory;informational|0.72|0.72|compliance;civil;fire_safety|planning;design|SRC-ICC-IBC-IPC-IFC-IECC-IEBC;SRC-WBDG-SYSTEMS-INTEGRATION|Authority-having-jurisdiction coordination sets whether emergency access geometry assumptions are adopted, modified, or replaced for a project.
CIV.DRN.CON.SMA|CIV.DRN.CON.CBI|requires|requires_access_for_inlet_sediment_maintenance|lifecycle_process|physical;operational|0.78|0.78|civil;operations|design;operation;maintenance|SRC-FHWA-HEC-22-URBAN-DRAINAGE;SRC-WBDG-SYSTEMS-INTEGRATION|Stormwater maintenance access is required for catch basins because inlet cleaning, sediment removal, inspection, and obstruction response depend on reachable structures.
CIV.DRN.CON.SMA|CIV.DRN.DET.DRM|requires|coordinates_detention_maintenance_access|lifecycle_process|physical;operational|0.72|0.74|civil;operations;sustainability|design;operation;maintenance|SRC-FHWA-HEC-22-URBAN-DRAINAGE;SRC-EPA-GREEN-INFRASTRUCTURE|Stormwater maintenance access coordinates with detention and retention maintenance requirements so downstream storage and overflow assets remain inspectable and serviceable.
CIV.DRN.CON.SMA|OPS.AST.REG.CAR|requires|creates_civil_asset_record_for_handover|information_management|informational;operational|0.78|0.78|civil;operations|handover;operation;maintenance|SRC-WBDG-SYSTEMS-INTEGRATION;SRC-NIBS-WBDG-COMMISSIONING|Stormwater maintenance access should be represented in civil asset handover records so operations teams know which drainage assets require inspection and cleaning access.
GEO.SRV.ASB|OPS.AST.REG.CAR|requires|documents_civil_as_built_condition_for_asset_register|information_management|informational;operational|0.74|0.74|geotechnical;civil;operations|handover;operation|SRC-WBDG-SYSTEMS-INTEGRATION;SRC-FHWA-GEOTECH-SUBSURFACE-INVESTIGATION|As-built survey information documents civil asset location and condition for asset registers, especially where drainage, utilities, grading, or access-route records must remain traceable.
CIV.MIS.UCC.USE|OPS.AST.REG.CAR|requires|generates_utility_service_asset_record|information_management|informational;operational|0.74|0.74|civil;operations;architecture|handover;operation;maintenance|SRC-FHWA-ASCE-38-SUE-UTILITY-DATA;SRC-WBDG-SYSTEMS-INTEGRATION|Utility service-entry coordination generates handover information for service locations, entry points, access constraints, and operations-facing asset records.
CIV.PAV.PST|OPS.AST.REG.CAR|requires|records_pavement_access_asset_for_operations|information_management|informational;operational|0.68|0.70|civil;operations|handover;operation;maintenance|SRC-WBDG-SYSTEMS-INTEGRATION;SRC-FHWA-HEC-22-URBAN-DRAINAGE|Pavement and emergency-access assets benefit from operations records so maintenance teams can manage route condition, drainage issues, defects, and access restrictions.
COM.APP.AHJ|CIV.HDI.FCI.DFE|constrains|sets_flood_elevation_ahj_adoption_basis|regulatory_authority|regulatory;informational|0.74|0.74|compliance;civil;architecture;structural|planning;design|SRC-ASCE-24-FLOOD-RESISTANT;SRC-ICC-IBC-IPC-IFC-IECC-IEBC|AHJ coordination governs whether flood elevation concepts are adopted for a project, while this graph records only source-family applicability and not jurisdiction-specific numeric criteria.
COM.APP.AHJ|CIV.SDV.ACC.CRG|constrains|sets_accessible_transition_adoption_basis|regulatory_authority|regulatory;informational|0.70|0.72|compliance;civil;accessibility|planning;design|SRC-US-ACCESS-BOARD-ADA-PROWAG;SRC-WBDG-SYSTEMS-INTEGRATION|AHJ coordination governs which accessibility criteria apply to curb-ramp and exterior-route transitions; the graph preserves the dependency without asserting universal dimensions.
COM.APP.AHJ|STR.LOA.GRV.LVL|constrains|requires_adopted_live_load_basis|regulatory_authority|regulatory;analytical|0.76|0.76|compliance;structural|planning;design|SRC-ASCE-SEI-7;SRC-ICC-IBC-IPC-IFC-IECC-IEBC|Occupancy live-load assumptions require an adopted project basis, so the graph links the load concept to AHJ coordination without storing numerical criteria.
COM.APP.AHJ|STR.LOA.LAT.WND|constrains|requires_adopted_wind_load_basis|regulatory_authority|regulatory;analytical|0.76|0.76|compliance;structural|planning;design|SRC-ASCE-SEI-7;SRC-ICC-IBC-IPC-IFC-IECC-IEBC|Wind-load criteria require an adopted project basis and site context, so the graph records the dependency while avoiding universal wind-speed, exposure, or pressure values.
COM.APP.AHJ|STR.LOA.LAT.SEI|constrains|requires_adopted_seismic_load_basis|regulatory_authority|regulatory;analytical|0.76|0.76|compliance;structural|planning;design|SRC-ASCE-SEI-7;SRC-ICC-IBC-IPC-IFC-IECC-IEBC|Seismic-load criteria depend on adopted hazard, site, risk, and detailing basis, so the graph marks the dependency without encoding jurisdiction-specific numerical design parameters.
COM.APP.AHJ|STR.LOA.ENV.RPL|constrains|requires_adopted_rain_ponding_load_basis|regulatory_authority|regulatory;analytical|0.70|0.72|compliance;structural;civil|planning;design|SRC-ASCE-SEI-7;SRC-NOAA-ATLAS-14-PRECIPITATION-FREQUENCY;SRC-FHWA-HEC-22-URBAN-DRAINAGE|Rain ponding and roof-drainage load assumptions require adopted rainfall, drainage, and structural criteria; this edge preserves the design-basis gate without numeric values.
CIV.RDC.PED.ATI|CIV.SDV.ACC.PSG|requires|coordinates_crossing_with_pedestrian_gradient_control|spatial_topological|physical;regulatory|0.78|0.74|civil;accessibility|planning;design;construction|SRC-US-ACCESS-BOARD-ADA-PROWAG;SRC-WBDG-SYSTEMS-INTEGRATION|The public-way crossing tie-in depends on pedestrian gradient control because route transitions, landings, and cross slopes must be coordinated before accessibility can be verified locally.
CIV.RDC.PED.ATI|CIV.DRN.CON.SRO|requires|requires_crossing_surface_runoff_control|civil_hydraulic_flow|physical;performance|0.72|0.72|civil;accessibility|design;construction;operation|SRC-FHWA-HEC-22-URBAN-DRAINAGE;SRC-US-ACCESS-BOARD-ADA-PROWAG|Crossing tie-ins require surface runoff coordination so curb ramps, sidewalks, and approach transitions do not create ponding or unsafe drainage conflicts.
ARC.SPC.CIR.ASR|CIV.RDC.PED.ATI|requires|requires_public_way_crossing_tie_in_review|coordination|physical;regulatory;performance|0.78|0.74|architecture;civil;accessibility|planning;design;construction|SRC-US-ACCESS-BOARD-ADA-PROWAG;SRC-WBDG-SYSTEMS-INTEGRATION|An accessible site-to-building route must coordinate with public-way crossing tie-ins where site arrival, sidewalks, curb ramps, drainage transitions, and AHJ public-right-of-way review affect continuity.
CIV.DRN.HYD|CIV.HDI.CCD.CDI|constrains|sets_culvert_hydrology_basis|civil_hydraulic_flow|analytical;performance|0.80|0.76|civil|planning;design|SRC-FHWA-HEC-22-URBAN-DRAINAGE;SRC-NOAA-ATLAS-14-PRECIPITATION-FREQUENCY|Hydrologic design basis constrains culvert drainage interfaces because catchment runoff and rainfall assumptions shape conveyance and overflow review, while numeric sizing remains project-specific.
CIV.HDI.CCD.CDI|CIV.DRN.CON.OVF|requires|coordinates_culvert_with_overland_overflow_path|civil_hydraulic_flow|physical;resilience|0.76|0.74|civil;sustainability|planning;design;operation|SRC-FHWA-HEC-22-URBAN-DRAINAGE;SRC-WBDG-SYSTEMS-INTEGRATION|Culvert drainage interfaces require an overland overflow path so bypass, blockage, or major storm behavior remains traceable in site resilience reasoning.
CIV.HDI.CCD.CDI|GEO.HAZ.FLO|requires|requires_flood_and_scour_hazard_review|risk|hydraulic;geotechnical;resilience|0.72|0.72|civil;geotechnical;structural|planning;design|SRC-FHWA-HEC-22-URBAN-DRAINAGE;SRC-FHWA-GEOTECH-SUBSURFACE-INVESTIGATION|Culvert interfaces can create flood and scour concerns at inlets, outlets, embankments, or adjacent foundations, so hazard review is required before project-specific design adoption.
CIV.PAV.PSI|GEO.FOE.DSE|constrains|sensitive_to_subgrade_settlement_variability|site_condition|geotechnical;performance|0.74|0.74|civil;geotechnical;structural|design;construction;operation|SRC-FHWA-GEOTECH-SUBSURFACE-INVESTIGATION;SRC-WBDG-SYSTEMS-INTEGRATION|Pavement subgrade interfaces are sensitive to differential settlement and support variability that affect rideability, drainage, emergency access, and maintenance performance.
CIV.MIS.UCC.SUC|CIV.PAV.PSI|constrains|constrains_pavement_restoration_at_utility_crossings|coordination|physical;construction;operational|0.72|0.72|civil;construction;operations|design;construction;maintenance|SRC-FHWA-ASCE-38-SUE-UTILITY-DATA;SRC-FHWA-GEOTECH-SUBSURFACE-INVESTIGATION|Utility conflict review constrains pavement restoration around utility crossings because trench backfill, compaction, cover, and future settlement can affect pavement performance.
CIV.PAV.PSI|CIV.DRN.CON.SRO|requires|requires_pavement_surface_drainage_coordination|civil_hydraulic_flow|physical;performance|0.74|0.74|civil|design;construction;operation|SRC-FHWA-HEC-22-URBAN-DRAINAGE;SRC-WBDG-SYSTEMS-INTEGRATION|Pavement subgrade and surface interfaces require drainage coordination so runoff, infiltration, ponding, and maintenance are addressed before service performance is assumed.
COM.APP.AHJ|CIV.DRN.HYD.IDF|constrains|requires_local_rainfall_basis_confirmation|regulatory_authority|regulatory;informational|0.72|0.74|compliance;civil|planning;design|SRC-NOAA-ATLAS-14-PRECIPITATION-FREQUENCY;SRC-FHWA-HEC-22-URBAN-DRAINAGE|AHJ or project criteria confirm which rainfall basis is adopted; the graph keeps IDF data source-family-only and does not store design-storm values.
CON.COM.BOD|STR.LOA.CBG|requires|records_structural_criteria_basis|information_management|informational;regulatory|0.76|0.76|commissioning;structural;compliance|planning;design|SRC-WBDG-SYSTEMS-INTEGRATION;SRC-ASCE-SEI-7|The basis-of-design record should capture the structural criteria basis so load assumptions can be traced without treating source-family standards as automatically adopted criteria.
COM.APP.AHJ|STR.LOA.CBG|constrains|gates_structural_criteria_by_authority_basis|regulatory_authority|regulatory;informational|0.82|0.80|compliance;structural|planning;design|SRC-ASCE-SEI-7;SRC-ICC-IBC-IPC-IFC-IECC-IEBC|AHJ coordination gates structural criteria adoption because live, wind, seismic, and rain-load values depend on adopted authority, project context, and current editions.
COM.APP.RCA|STR.LOA.CBG|constrains|gates_structural_criteria_by_risk_context|regulatory_authority|regulatory;analytical|0.76|0.76|compliance;structural|planning;design|SRC-ASCE-SEI-7;SRC-ICC-IBC-IPC-IFC-IECC-IEBC|Risk category applicability constrains the structural criteria basis because importance, occupancy, and consequence context affect later adopted load parameters.
COM.APP.SDC|STR.LOA.CBG|constrains|gates_seismic_criteria_basis|regulatory_authority|regulatory;analytical|0.76|0.76|compliance;structural|planning;design|SRC-ASCE-SEI-7;SRC-ICC-IBC-IPC-IFC-IECC-IEBC|Seismic design category applicability gates seismic criteria basis while avoiding universal hazard, site class, or detailing values in the file-backed graph.
STR.LOA.CBG|STR.LOA.GRV.LVL|constrains|gates_live_load_basis_before_application|regulatory_authority|regulatory;analytical|0.78|0.78|structural;compliance|planning;design|SRC-ASCE-SEI-7;SRC-ICC-IBC-IPC-IFC-IECC-IEBC|The structural criteria basis gate must be satisfied before occupancy live-load values can be applied, keeping source-family concepts separate from adopted numerical criteria.
STR.LOA.CBG|STR.LOA.LAT.WND|constrains|gates_wind_load_basis_before_application|regulatory_authority|regulatory;analytical|0.78|0.78|structural;compliance|planning;design|SRC-ASCE-SEI-7;SRC-ICC-IBC-IPC-IFC-IECC-IEBC|The structural criteria basis gate prevents wind-load concepts from being treated as adopted wind speeds, exposures, or pressures without project and authority evidence.
STR.LOA.CBG|STR.LOA.LAT.SEI|constrains|gates_seismic_load_basis_before_application|regulatory_authority|regulatory;analytical|0.78|0.78|structural;compliance|planning;design|SRC-ASCE-SEI-7;SRC-ICC-IBC-IPC-IFC-IECC-IEBC|The structural criteria basis gate prevents seismic-load concepts from becoming adopted hazard or detailing requirements without project, risk, and authority evidence.
CIV.DRN.CON.CBI|OPS.MNT.PMA|requires|requires_drainage_inlet_maintenance_plan|lifecycle_process|operational;physical|0.72|0.74|civil;operations|handover;operation;maintenance|SRC-FHWA-HEC-22-URBAN-DRAINAGE;SRC-ISO-41001-55001-FM-AM|Catch basins require preventive maintenance planning because sediment removal, grate cleaning, and obstruction response affect drainage performance.
CIV.DRN.LID.BRC|OPS.AST.CDA|requires|requires_bioretention_condition_data_handoff|information_management|operational;informational|0.70|0.72|civil;operations;sustainability|handover;operation;maintenance|SRC-EPA-GREEN-INFRASTRUCTURE;SRC-ISO-41001-55001-FM-AM|Bioretention cells require condition-data handoff so vegetation, media, underdrain, overflow, and maintenance state remain visible to operations.
STR.SSS.CBP.MJT|OPS.INS.RIN|requires|requires_movement_joint_condition_inspection|lifecycle_process|operational;physical|0.70|0.72|structural;operations|handover;operation;maintenance|SRC-WBDG-SYSTEMS-INTEGRATION;SRC-NIBS-WBDG-BUILDING-ENVELOPE|Movement joints require routine inspection because seals, covers, waterproofing continuity, and movement accommodation can degrade during operation.
STR.FND.SHL.RTW|OPS.INS.RIN|requires|requires_retaining_wall_drainage_condition_inspection|lifecycle_process|operational;physical|0.70|0.72|structural;civil;operations|handover;operation;maintenance|SRC-FHWA-GEOTECH-SUBSURFACE-INVESTIGATION;SRC-ISO-41001-55001-FM-AM|Retaining walls require inspection attention to drainage and seepage conditions because blocked drains or water pressure can affect wall performance.
""".strip()

RESOLVER_CASES = [
    ("RES-ACS-001", "VTN-DOM-0012738", "From an accessible site-to-building route, traverse site grading, pedestrian slope control, egress discharge, and emergency access implications.", ["VTN-DOM-0012738", "VTN-DOM-0012753", "VTN-DOM-0012739", "VTN-DOM-0012754"], ["architecture", "civil", "accessibility", "fire_safety"], ["SRC-US-ACCESS-BOARD-ADA-PROWAG", "SRC-WBDG-SYSTEMS-INTEGRATION"], "Compatible composed relationships connect exterior accessibility, grading, egress discharge, and emergency access without encoding universal numeric code thresholds."),
    ("RES-ACS-002", "VTN-DOM-0012742", "From a roof drainage interface, traverse roof assembly, rain ponding load, civil roof discharge, storm sewer, and detention/outfall implications.", ["VTN-DOM-0012742", "VTN-DOM-0012776", "VTN-DOM-0012764", "VTN-DOM-0012760", "VTN-DOM-0012755"], ["architecture", "civil", "structural"], ["SRC-NIBS-WBDG-BUILDING-ENVELOPE", "SRC-FHWA-HEC-22-URBAN-DRAINAGE", "SRC-ASCE-SEI-7"], "Compatible composed relationships connect roof envelope, structural rain-load risk, and civil stormwater conveyance as a cross-taxonomy reasoning path."),
    ("RES-ACS-003", "VTN-DOM-0012769", "From geotechnical investigation, find bearing pressure, settlement evaluation, footing design, groundwater constraints, and foundation performance.", ["VTN-DOM-0012769", "VTN-DOM-0012772", "VTN-DOM-0012773", "VTN-DOM-0012797", "VTN-DOM-0012782"], ["geotechnical", "structural", "civil"], ["SRC-FHWA-GEOTECH-SUBSURFACE-INVESTIGATION", "SRC-ASCE-SEI-7"], "Compatible composed relationships expose how subsurface investigation informs foundation bearing, settlement, groundwater, and structural foundation choices."),
    ("RES-ACS-004", "VTN-DOM-0012779", "From a suspended slab, follow gravity load transfer through beam, column, footing, and soil bearing interface.", ["VTN-DOM-0012779", "VTN-DOM-0012780", "VTN-DOM-0012781", "VTN-DOM-0012782", "VTN-DOM-0012772"], ["structural", "geotechnical"], ["SRC-ASCE-SEI-7", "SRC-ACI-318-STRUCTURAL-CONCRETE", "SRC-FHWA-GEOTECH-SUBSURFACE-INVESTIGATION"], "Compatible composed relationships encode a queryable gravity load path from slab to beam, column, foundation, and ground capacity."),
    ("RES-ACS-005", "VTN-DOM-0012777", "From wind load, traverse facade anchor interface, force transfer connection, diaphragm action, collector, core, and foundation path.", ["VTN-DOM-0012777", "VTN-DOM-0012743", "VTN-DOM-0012793", "VTN-DOM-0012787", "VTN-DOM-0012790"], ["architecture", "structural"], ["SRC-ASCE-SEI-7", "SRC-NIBS-WBDG-BUILDING-ENVELOPE", "SRC-AISC-360-STRUCTURAL-STEEL"], "Compatible composed relationships link facade load collection with structural lateral load transfer rather than treating facade and frame as unrelated objects."),
    ("RES-ACS-006", "VTN-DOM-0012741", "From floor opening coordination, traverse slab, beam, diaphragm opening, fire separation, acoustic continuity, and service riser implications.", ["VTN-DOM-0012741", "VTN-DOM-0012779", "VTN-DOM-0012780", "VTN-DOM-0012789", "VTN-DOM-0012746"], ["architecture", "structural", "fire_safety"], ["SRC-ASCE-SEI-7", "SRC-WBDG-SYSTEMS-INTEGRATION", "SRC-ICC-IBC-IPC-IFC-IECC-IEBC"], "Compatible composed relationships decompose floor openings into structural, fire, acoustic, and riser coordination mechanisms."),
    ("RES-ACS-007", "VTN-DOM-0012799", "From a structural retaining wall, find lateral earth pressure, groundwater, perimeter drainage, grading, and foundation interaction.", ["VTN-DOM-0012799", "VTN-DOM-0012771", "VTN-DOM-0012765", "VTN-DOM-0012749", "VTN-DOM-0012750"], ["structural", "geotechnical", "civil"], ["SRC-FHWA-GEOTECH-SUBSURFACE-INVESTIGATION", "SRC-NIBS-WBDG-BUILDING-ENVELOPE"], "Compatible composed relationships connect retaining wall behavior to earth pressure, groundwater, drainage, and grading constraints."),
    ("RES-ACS-008", "VTN-DOM-0012794", "From structural movement joint, traverse architectural joint cover, waterproofing continuity, firestop movement review, and envelope continuity.", ["VTN-DOM-0012794", "VTN-DOM-0012745", "VTN-DOM-0012744", "VTN-DOM-0012716"], ["structural", "architecture", "fire_safety"], ["SRC-NIBS-WBDG-BUILDING-ENVELOPE", "SRC-ASCE-SEI-7", "SRC-ICC-IBC-IPC-IFC-IECC-IEBC"], "Compatible composed relationships distinguish structural movement from architectural cover, waterproofing continuity, and firestop movement coordination."),
    ("RES-ACS-009", "VTN-DOM-0012803", "From subsurface utility conflict review, traverse foundation layout, excavation shoring, utility service entry, and conflict-avoidance implications.", ["VTN-DOM-0012803", "VTN-DOM-0012782", "VTN-DOM-0000314", "VTN-DOM-0012768"], ["civil", "geotechnical", "structural", "construction"], ["SRC-FHWA-ASCE-38-SUE-UTILITY-DATA", "SRC-FHWA-GEOTECH-SUBSURFACE-INVESTIGATION"], "Compatible composed relationships connect utility data/conflict review to footing layout, excavation support, and service-entry routing without exposing source payloads."),
    ("RES-ACS-010", "VTN-DOM-0012804", "From design flood elevation interface, traverse flood applicability, finished-floor elevation, foundation interface, and grading implications.", ["VTN-DOM-0012804", "VTN-DOM-0011901", "VTN-DOM-0012749", "VTN-DOM-0012782"], ["civil", "architecture", "structural", "compliance"], ["SRC-ASCE-24-FLOOD-RESISTANT", "SRC-ICC-IBC-IPC-IFC-IECC-IEBC", "SRC-WBDG-SYSTEMS-INTEGRATION"], "Compatible composed relationships connect flood hazard applicability to finished-floor and foundation interfaces while keeping AHJ adoption and project context explicit."),
    ("RES-ACS-011", "VTN-DOM-0003029", "From slope stability, traverse topography, site grading, retaining wall basis, and geotechnical risk implications.", ["VTN-DOM-0003029", "VTN-DOM-0012750", "VTN-DOM-0000232", "VTN-DOM-0012799"], ["geotechnical", "civil", "structural"], ["SRC-FHWA-GEOTECH-SUBSURFACE-INVESTIGATION", "SRC-WBDG-SYSTEMS-INTEGRATION"], "Compatible composed relationships connect surveyed terrain and slope stability to grading and retaining-wall stability basis without prescribing a jurisdiction-specific design method."),
    ("RES-ACS-012", "VTN-DOM-0012806", "From test-hole utility verification, traverse utility data quality, conflict review, service entry, excavation support, and foundation clearance implications.", ["VTN-DOM-0012806", "VTN-DOM-0012805", "VTN-DOM-0012803", "VTN-DOM-0012768", "VTN-DOM-0012782"], ["civil", "geotechnical", "structural", "construction"], ["SRC-FHWA-ASCE-38-SUE-UTILITY-DATA", "SRC-FHWA-GEOTECH-SUBSURFACE-INVESTIGATION"], "Compatible composed relationships show how utility verification strengthens evidence before excavation, foundation layout, and service-entry decisions."),
    ("RES-ACS-013", "VTN-DOM-0012807", "From pavement subgrade preparation, traverse pavement structure, emergency access, grading, drainage, and operations handover implications.", ["VTN-DOM-0012807", "VTN-DOM-0012808", "VTN-DOM-0012754", "VTN-DOM-0012810", "VTN-DOM-0012812"], ["civil", "geotechnical", "fire_safety", "operations"], ["SRC-FHWA-GEOTECH-SUBSURFACE-INVESTIGATION", "SRC-WBDG-SYSTEMS-INTEGRATION"], "Compatible composed relationships link pavement support to access-route performance, emergency response function, and lifecycle asset records without numeric pavement design claims."),
    ("RES-ACS-014", "VTN-DOM-0012811", "From stormwater maintenance access, traverse catch basin cleaning, detention maintenance, hydraulic performance, and civil asset handover records.", ["VTN-DOM-0012811", "VTN-DOM-0012759", "VTN-DOM-0005778", "VTN-DOM-0012812"], ["civil", "operations", "sustainability"], ["SRC-FHWA-HEC-22-URBAN-DRAINAGE", "SRC-WBDG-SYSTEMS-INTEGRATION", "SRC-NIBS-WBDG-COMMISSIONING"], "Compatible composed relationships connect stormwater maintainability with inlet cleaning, detention O and M, and asset-register handover for operations."),
    ("RES-ACS-015", "VTN-DOM-0011893", "From AHJ coordination, traverse adopted-basis gates for emergency access, flood elevation, live load, wind load, seismic load, and rain ponding without numeric criteria.", ["VTN-DOM-0011893", "VTN-DOM-0012810", "VTN-DOM-0012804", "VTN-DOM-0012775", "VTN-DOM-0012777", "VTN-DOM-0012778"], ["compliance", "civil", "structural", "fire_safety"], ["SRC-ASCE-SEI-7", "SRC-ASCE-24-FLOOD-RESISTANT", "SRC-ICC-IBC-IPC-IFC-IECC-IEBC"], "Compatible composed relationships make project/AHJ adoption explicit for criteria-sensitive concepts while blocking ungrounded universal numerical requirements."),
    ("RES-ACS-016", "VTN-DOM-0012813", "From accessible public-way crossing tie-in, traverse accessible site route, pedestrian gradients, surface runoff, and AHJ-sensitive public-way coordination.", ["VTN-DOM-0012813", "VTN-DOM-0012738", "VTN-DOM-0012753", "VTN-DOM-0012758", "VTN-DOM-0011893"], ["architecture", "civil", "accessibility", "compliance"], ["SRC-US-ACCESS-BOARD-ADA-PROWAG", "SRC-FHWA-HEC-22-URBAN-DRAINAGE", "SRC-WBDG-SYSTEMS-INTEGRATION"], "Compatible composed relationships connect accessible public-way tie-in coordination with route continuity, gradient control, runoff control, and authority-sensitive criteria without storing universal dimensions."),
    ("RES-ACS-017", "VTN-DOM-0012814", "From culvert drainage interface, traverse hydrologic basis, overland overflow, flood and scour review, and downstream stormwater operations implications.", ["VTN-DOM-0012814", "VTN-DOM-0012755", "VTN-DOM-0012763", "VTN-DOM-0000292", "VTN-DOM-0012812"], ["civil", "geotechnical", "operations", "sustainability"], ["SRC-FHWA-HEC-22-URBAN-DRAINAGE", "SRC-FHWA-GEOTECH-SUBSURFACE-INVESTIGATION", "SRC-WBDG-SYSTEMS-INTEGRATION"], "Compatible composed relationships deepen flood-hydraulic reasoning from source-family hydrology through culvert, overflow, hazard review, and maintainable civil asset handover."),
    ("RES-ACS-018", "VTN-DOM-0012816", "From structural criteria basis gate, traverse AHJ, risk, seismic applicability, live load, wind load, and seismic load concepts without admitting numeric criteria.", ["VTN-DOM-0012816", "VTN-DOM-0011893", "VTN-DOM-0011898", "VTN-DOM-0011900", "VTN-DOM-0012775", "VTN-DOM-0012777", "VTN-DOM-0012778"], ["structural", "compliance"], ["SRC-ASCE-SEI-7", "SRC-ICC-IBC-IPC-IFC-IECC-IEBC"], "Compatible composed relationships convert externally gated criteria into explicit basis dependencies while keeping numerical project criteria unadmitted."),
]


def enrich_backbone_payload(payload: dict[str, Any]) -> dict[str, Any]:
    enriched = deepcopy(payload)
    records = _dict_list(enriched.setdefault("records", []))
    relationships = _dict_list(enriched.setdefault("relationships", []))
    path_to_record = {str(row.get("path_code") or ""): row for row in records if row.get("path_code")}

    for spec in _refinement_specs():
        existing = path_to_record.get(spec["path_code"])
        if existing is not None:
            _merge_node_refinement(existing, spec)

    for spec in _node_specs():
        existing = path_to_record.get(spec["path_code"])
        if existing is None:
            node = _node_from_spec(spec)
            records.append(node)
            path_to_record[node["path_code"]] = node
        else:
            _merge_node_refinement(existing, spec)

    existing_keys = {_relationship_key(row) for row in relationships}
    for spec in _node_specs():
        node = path_to_record[spec["path_code"]]
        parent_path = str(node.get("parent_path_code") or "")
        parent = path_to_record.get(parent_path)
        if parent is None:
            raise ValueError(f"missing parent path for {spec['path_code']}: {parent_path}")
        row = _relationship_row(
            from_id=str(parent["id"]),
            to_id=str(node["id"]),
            predicate="broader_than",
            relation_type="taxonomy_parent_of",
            relation_category="taxonomy",
            relation_nature=["informational"],
            weight=0.64,
            confidence_score=0.86,
            discipline=spec["disciplines"],
            lifecycle_phase=spec["lifecycle"],
            source_family_ids=spec["sources"],
            rationale=f"{node['label']} is admitted under {parent.get('label')} to keep the ACS concept in the governed Backbone taxonomy.",
            generation_method=HIERARCHY_GENERATION_METHOD,
        )
        key = _relationship_key(row)
        if key in existing_keys:
            _merge_relationship_metadata(relationships, key, row)
        else:
            relationships.append(row)
            existing_keys.add(key)

    for spec in _edge_specs():
        from_record = path_to_record.get(spec["from_path"])
        to_record = path_to_record.get(spec["to_path"])
        if from_record is None or to_record is None:
            raise ValueError(f"edge references missing path: {spec['from_path']} -> {spec['to_path']}")
        row = _relationship_row(
            from_id=str(from_record["id"]),
            to_id=str(to_record["id"]),
            predicate=spec["predicate"],
            relation_type=spec["relation_type"],
            relation_category=spec["relation_category"],
            relation_nature=spec["relation_nature"],
            weight=spec["weight"],
            confidence_score=spec["confidence_score"],
            discipline=spec["discipline"],
            lifecycle_phase=spec["lifecycle_phase"],
            source_family_ids=spec["source_family_ids"],
            rationale=spec["rationale"],
            generation_method=GENERATION_METHOD,
        )
        key = _relationship_key(row)
        if key in existing_keys:
            _merge_relationship_metadata(relationships, key, row)
        else:
            relationships.append(row)
            existing_keys.add(key)

    enriched["records"] = sorted(records, key=lambda row: (str(row.get("path_code") or "~"), str(row.get("id") or "")))
    enriched["relationships"] = sorted(
        relationships,
        key=lambda row: (
            str(row.get("from_id") or ""),
            str(row.get("predicate") or row.get("edge_type") or ""),
            str(row.get("to_id") or ""),
            str(row.get("relation_type") or ""),
        ),
    )
    return enriched


def enrich_source_rights_payload(payload: dict[str, Any]) -> dict[str, Any]:
    enriched = deepcopy(payload)
    rows = _dict_list(enriched.setdefault("source_rights_registry", []))
    by_id = {str(row.get("source_id") or ""): row for row in rows}
    for source_id, family, publisher, url, rights_class, intended_use in SOURCE_ROWS:
        row = {
            "source_id": source_id,
            "source_family": family,
            "publisher_authority": publisher,
            "edition_version_effective_date": f"public metadata currentness checked {ACCESS_DATE}; adopted edition, jurisdiction, or release may vary",
            "official_url": url,
            "source_rights_class": rights_class,
            "clearance_state": "planning_reference_only",
            "intended_vitruvius_use": intended_use,
            "steward_owner": OWNER,
            "declared_use_boundary": "No source text, formulas, tables, figures, images, clauses, or protected payloads ingested; source content reuse remains blocked.",
            "currentness_check_date": ACCESS_DATE,
            "update_cadence": "before source admission, edition-specific mapping, or jurisdiction-specific relationship changes",
            "blocking_notes": "Use as source-family metadata only; AHJ adoption, project brief, and source-rights review control stronger claims.",
        }
        if source_id not in by_id:
            rows.append(row)
        else:
            for key, value in row.items():
                if not by_id[source_id].get(key):
                    by_id[source_id][key] = value
    enriched["source_rights_registry"] = sorted(rows, key=lambda row: str(row.get("source_id") or ""))
    return enriched


def enrich_readiness_fixture(payload: dict[str, Any]) -> dict[str, Any]:
    enriched = deepcopy(payload)
    cases = _dict_list(enriched.setdefault("resolver_golden_cases", []))
    existing = {str(case.get("case_id") or "") for case in cases}
    for case in _resolver_cases():
        if case["case_id"] not in existing:
            cases.append(case)
    enriched["resolver_golden_cases"] = sorted(cases, key=lambda row: str(row.get("case_id") or ""))
    return enriched


def summarize_delta(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    before_records = _dict_list(before.get("records"))
    after_records = _dict_list(after.get("records"))
    before_relationships = _dict_list(before.get("relationships"))
    after_relationships = _dict_list(after.get("relationships"))
    before_record_ids = {str(row.get("id") or "") for row in before_records}
    after_record_ids = {str(row.get("id") or "") for row in after_records}
    before_rel_keys = {_relationship_key(row) for row in before_relationships}
    after_rel_keys = {_relationship_key(row) for row in after_relationships}
    enriched_relations = [row for row in after_relationships if row.get("generation_method") == GENERATION_METHOD]
    hierarchy_relations = [row for row in after_relationships if row.get("generation_method") == HIERARCHY_GENERATION_METHOD]
    refined_records = [row for row in after_records if REFINEMENT_METHOD in _list_strings(row.get("refinement_methods"))]
    return {
        "nodes_before": len(before_records),
        "nodes_after": len(after_records),
        "relationships_before": len(before_relationships),
        "relationships_after": len(after_relationships),
        "new_node_count": len(after_record_ids - before_record_ids),
        "new_relationship_count": len(after_rel_keys - before_rel_keys),
        "refined_node_count": len(refined_records),
        "acs_relationship_count": len(enriched_relations),
        "acs_hierarchy_relationship_count": len(hierarchy_relations),
        "relation_types_added": dict(sorted(Counter(str(row.get("relation_type") or "") for row in enriched_relations).items())),
        "clusters_added": dict(sorted(Counter(cluster for spec in _node_specs() for cluster in spec["clusters"]).items())),
    }


def apply_enrichment(
    *,
    backbone_path: str | Path = DEFAULT_BACKBONE_PATH,
    source_rights_path: str | Path = DEFAULT_SOURCE_RIGHTS_PATH,
    readiness_fixture_path: str | Path = DEFAULT_READINESS_FIXTURE_PATH,
    repo_root: str | Path | None = None,
    run_id: str | None = None,
    output_path: str | Path | None = None,
    write: bool = True,
) -> dict[str, Any]:
    root = _repo_root(repo_root)
    backbone_file = _resolve_file(root, Path(backbone_path))
    source_file = _resolve_file(root, Path(source_rights_path))
    readiness_file = _resolve_file(root, Path(readiness_fixture_path))
    resolved_run_id = _run_id(run_id)
    if write:
        _reject_protected_write_target(root, backbone_file, "backbone_path")
        _reject_protected_write_target(root, source_file, "source_rights_path")
        _reject_protected_write_target(root, readiness_file, "readiness_fixture_path")
    report_file = _resolve_report_path(root, resolved_run_id, Path(output_path) if output_path else None)

    before_backbone = _load_json_object(backbone_file)
    before_sources = _load_json_object(source_file)
    before_readiness = _load_json_object(readiness_file)
    after_backbone = enrich_backbone_payload(before_backbone)
    after_sources = enrich_source_rights_payload(before_sources)
    after_readiness = enrich_readiness_fixture(before_readiness)

    if write:
        _write_json(backbone_file, after_backbone)
        _write_json(source_file, after_sources)
        _write_json(readiness_file, after_readiness)

    old_sources = {str(row.get("source_id") or "") for row in _dict_list(before_sources.get("source_rights_registry"))}
    old_cases = {str(row.get("case_id") or "") for row in _dict_list(before_readiness.get("resolver_golden_cases"))}
    report = {
        "schema_version": REPORT_SCHEMA_VERSION,
        "ok": True,
        "run_id": resolved_run_id,
        "generated_at_utc": _utc_now(),
        "write": write,
        "safety_boundaries": {
            "shadow_only": True,
            "file_backed_only": True,
            "live_neo4j_writes": False,
            "kg_rebuild": False,
            "feature_flag_cutover": False,
            "api_explorer_cutover": False,
            "canonical_content_admission": False,
            "protected_content_ingest": False,
        },
        "delta": summarize_delta(before_backbone, after_backbone),
        "source_delta": {
            "source_rows_before": len(_dict_list(before_sources.get("source_rights_registry"))),
            "source_rows_after": len(_dict_list(after_sources.get("source_rights_registry"))),
            "new_source_ids": sorted(_source_family_ids_used() - old_sources),
        },
        "resolver_delta": {
            "resolver_cases_before": len(_dict_list(before_readiness.get("resolver_golden_cases"))),
            "resolver_cases_after": len(_dict_list(after_readiness.get("resolver_golden_cases"))),
            "new_case_ids": sorted({case["case_id"] for case in _resolver_cases()} - old_cases),
        },
        "backbone_path": _relative_to_root(backbone_file, root),
        "source_rights_path": _relative_to_root(source_file, root),
        "readiness_fixture_path": _relative_to_root(readiness_file, root),
        "report_path": _relative_to_root(report_file, root),
    }
    _write_json(report_file, report)
    return report


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Apply file-backed Architecture/Civil/Structural Backbone enrichment.")
    parser.add_argument("--backbone", default=str(DEFAULT_BACKBONE_PATH))
    parser.add_argument("--source-rights", default=str(DEFAULT_SOURCE_RIGHTS_PATH))
    parser.add_argument("--readiness-fixture", default=str(DEFAULT_READINESS_FIXTURE_PATH))
    parser.add_argument("--repo-root", default=None)
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--output", default=None)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    try:
        report = apply_enrichment(
            backbone_path=args.backbone,
            source_rights_path=args.source_rights,
            readiness_fixture_path=args.readiness_fixture,
            repo_root=args.repo_root,
            run_id=args.run_id,
            output_path=args.output,
            write=not args.dry_run,
        )
    except (OSError, ValueError) as exc:
        print(json.dumps({"ok": False, "errors": [str(exc)]}, indent=2, sort_keys=True))
        return 1
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["ok"] else 1


def _node_specs() -> list[dict[str, Any]]:
    specs: list[dict[str, Any]] = []
    for line in NODE_ROWS.splitlines():
        node_id, path_code, label, definition, aliases, clusters = line.split("|", 5)
        specs.append({
            "id": node_id,
            "path_code": path_code,
            "label": label,
            "definition": definition,
            "aliases": _split_semicolon(aliases),
            "clusters": _split_semicolon(clusters),
            "disciplines": _disciplines_for_path(path_code, clusters),
            "lifecycle": _lifecycle_for_path(path_code, clusters),
            "sources": _sources_for_path(path_code, clusters),
            "node_kind": _node_kind_for_path(path_code, clusters),
        })
    return specs


def _refinement_specs() -> list[dict[str, Any]]:
    specs: list[dict[str, Any]] = []
    for line in REFINEMENT_ROWS.splitlines():
        path_code, aliases, clusters, node_kind, disciplines, lifecycle, sources = line.split("|", 6)
        specs.append({
            "path_code": path_code,
            "aliases": _split_semicolon(aliases),
            "clusters": _split_semicolon(clusters),
            "node_kind": node_kind,
            "disciplines": _split_semicolon(disciplines),
            "lifecycle": _split_semicolon(lifecycle),
            "sources": _split_semicolon(sources),
        })
    return specs


def _edge_specs() -> list[dict[str, Any]]:
    specs: list[dict[str, Any]] = []
    for line in EDGE_ROWS.splitlines():
        parts = line.split("|", 11)
        if len(parts) != 12:
            raise ValueError(f"invalid edge row: {line}")
        from_path, to_path, predicate, relation_type, category, nature, weight, confidence, discipline, lifecycle, sources, rationale = parts
        specs.append({
            "from_path": from_path,
            "to_path": to_path,
            "predicate": predicate,
            "relation_type": relation_type,
            "relation_category": category,
            "relation_nature": _split_semicolon(nature),
            "weight": float(weight),
            "confidence_score": float(confidence),
            "discipline": _split_semicolon(discipline),
            "lifecycle_phase": _split_semicolon(lifecycle),
            "source_family_ids": _split_semicolon(sources),
            "rationale": rationale,
        })
    return specs


def _resolver_cases() -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    for case_id, concept_id, text, refs, disciplines, sources, rationale in RESOLVER_CASES:
        cases.append({
            "case_id": case_id,
            "effective_date": ACCESS_DATE,
            "expected_confidence": "deterministic",
            "expected_node_refs": [{"node_id": node_id, "role": "acs_trace_node"} for node_id in refs],
            "expected_result_type": "composed",
            "fallback_reason": "architecture_civil_structural_relationship_trace",
            "jurisdiction": "source-family-mixed-ahj-required",
            "owner": OWNER,
            "query": {
                "asset_context": case_id.lower().replace("-", "_"),
                "concept_id": concept_id,
                "context_ids": refs[:3],
                "discipline_filters": disciplines,
                "jurisdiction_filters": ["source-family-mixed"],
                "text": text,
                "trace_requested": True,
            },
            "rationale": rationale,
            "review_status": "candidate",
            "source_evidence": sources,
            "trace_safe_rationale": "Reports canonical IDs and paraphrased ACS relationship rationales only; no protected source text is exposed.",
        })
    return cases


def _node_from_spec(spec: dict[str, Any]) -> dict[str, Any]:
    path_code = spec["path_code"]
    return {
        "id": spec["id"],
        "canonical_id": spec["id"],
        "record_type": "BackboneNode",
        "review_status": "steward_admitted",
        "label": spec["label"],
        "pref_label": spec["label"],
        "definition": spec["definition"],
        "aliases": spec["aliases"],
        "scope_note": "ACS domain concept added for cross-taxonomy reasoning; project-specific values require local validation.",
        "example_concepts": [],
        "path_code": path_code,
        "level": len(path_code.split(".")),
        "parent_path_code": ".".join(path_code.split(".")[:-1]) if "." in path_code else None,
        "owner": OWNER,
        "steward": OWNER,
        "release_version": RELEASE_VERSION,
        "generation_method": GENERATION_METHOD,
        "semantic_overlay_category": "architecture_civil_structural_domain_node",
        "semantic_node_kind": spec["node_kind"],
        "discipline": spec["disciplines"],
        "lifecycle_phase": spec["lifecycle"],
        "source_family_ids": spec["sources"],
        "provenance_note": PROVENANCE_NOTE,
        "domain_clusters": spec["clusters"],
    }


def _merge_node_refinement(existing: dict[str, Any], spec: dict[str, Any]) -> None:
    if existing.get("generation_method") == GENERATION_METHOD:
        if spec.get("label"):
            existing["label"] = spec["label"]
            existing["pref_label"] = spec["label"]
        if spec.get("definition"):
            existing["definition"] = spec["definition"]
        existing["scope_note"] = "ACS domain concept added for cross-taxonomy reasoning; project-specific values require local validation."
        existing["semantic_overlay_category"] = "architecture_civil_structural_domain_node"
    if spec.get("aliases"):
        existing["aliases"] = list(dict.fromkeys([*_list_strings(existing.get("aliases")), *spec["aliases"]]))
    if spec.get("clusters"):
        existing["domain_clusters"] = list(dict.fromkeys([*_list_strings(existing.get("domain_clusters")), *spec["clusters"]]))
    if spec.get("sources"):
        existing["source_family_ids"] = list(dict.fromkeys([*_list_strings(existing.get("source_family_ids")), *spec["sources"]]))
    if spec.get("disciplines"):
        existing["discipline"] = list(dict.fromkeys([*_list_strings(existing.get("discipline")), *spec["disciplines"]]))
    if spec.get("lifecycle"):
        existing["lifecycle_phase"] = list(dict.fromkeys([*_list_strings(existing.get("lifecycle_phase")), *spec["lifecycle"]]))
    if spec.get("node_kind") and not existing.get("semantic_node_kind"):
        existing["semantic_node_kind"] = spec["node_kind"]
    existing["provenance_note"] = existing.get("provenance_note") or PROVENANCE_NOTE
    existing["refinement_methods"] = list(dict.fromkeys([*_list_strings(existing.get("refinement_methods")), REFINEMENT_METHOD]))


def _relationship_row(
    *,
    from_id: str,
    to_id: str,
    predicate: str,
    relation_type: str,
    relation_category: str,
    relation_nature: Sequence[str],
    weight: float,
    confidence_score: float,
    discipline: Sequence[str],
    lifecycle_phase: Sequence[str],
    source_family_ids: Sequence[str],
    rationale: str,
    generation_method: str,
) -> dict[str, Any]:
    return {
        "from_id": from_id,
        "to_id": to_id,
        "predicate": predicate,
        "governed": True,
        "generation_method": generation_method,
        "semantic_overlay_category": "architecture_civil_structural_interrelationship",
        "relation_type": relation_type,
        "relation_category": relation_category,
        "relation_nature": list(relation_nature),
        "direction": "from_to",
        "weight": round(float(weight), 3),
        "confidence_score": round(float(confidence_score), 3),
        "discipline": list(discipline),
        "lifecycle_phase": list(lifecycle_phase),
        "source_family_ids": list(source_family_ids),
        "rationale": rationale,
        "provenance_note": PROVENANCE_NOTE,
        "review_status": "steward_admitted",
        "applicability_basis": "source_family_only_ahj_or_project_basis_required",
        "jurisdiction_context": "source-family-mixed-ahj-required",
        "design_basis_status": "no_project_numeric_criteria_admitted",
    }


def _merge_relationship_metadata(rows: list[dict[str, Any]], key: tuple[str, str, str], candidate: dict[str, Any]) -> None:
    for row in rows:
        if _relationship_key(row) == key:
            for field in (
                "relation_type",
                "relation_category",
                "relation_nature",
                "direction",
                "weight",
                "confidence_score",
                "discipline",
                "lifecycle_phase",
                "source_family_ids",
                "rationale",
                "provenance_note",
                "generation_method",
                "review_status",
                "semantic_overlay_category",
                "applicability_basis",
                "jurisdiction_context",
                "design_basis_status",
            ):
                if not row.get(field) and candidate.get(field) is not None:
                    row[field] = candidate[field]
            return


def _disciplines_for_path(path_code: str, clusters: str) -> list[str]:
    disciplines = {
        "ARC": ["architecture"],
        "CIV": ["civil"],
        "GEO": ["geotechnical"],
        "OPS": ["operations"],
        "STR": ["structural"],
    }.get(path_code.split(".", 1)[0], ["aec"])
    if "access" in clusters:
        disciplines.append("accessibility")
    if "fire" in clusters:
        disciplines.append("fire_safety")
    if "stormwater" in clusters:
        disciplines.append("civil")
    if "geotech" in clusters:
        disciplines.append("geotechnical")
    if "structure" in clusters or "structural" in clusters:
        disciplines.append("structural")
    if "operations" in clusters or "handoff" in clusters:
        disciplines.append("operations")
    return list(dict.fromkeys(disciplines))


def _lifecycle_for_path(path_code: str, clusters: str) -> list[str]:
    phases = ["planning", "design", "construction"]
    if any(token in clusters for token in ("drainage", "stormwater", "settlement", "movement", "access")):
        phases.append("operation")
    if any(token in clusters for token in ("drainage", "movement", "stormwater")):
        phases.append("maintenance")
    if "handoff" in clusters:
        phases.extend(["handover", "operation", "maintenance"])
    if path_code.startswith("STR.TMA"):
        phases = ["planning", "design", "construction", "inspection"]
    return phases


def _sources_for_path(path_code: str, clusters: str) -> list[str]:
    sources = {"SRC-WBDG-SYSTEMS-INTEGRATION"}
    if path_code.startswith("ARC"):
        sources.add("SRC-NIBS-WBDG-BUILDING-ENVELOPE")
    if path_code.startswith("CIV"):
        sources.add("SRC-FHWA-HEC-22-URBAN-DRAINAGE")
    if path_code.startswith("GEO") or "geotech" in clusters:
        sources.add("SRC-FHWA-GEOTECH-SUBSURFACE-INVESTIGATION")
    if path_code.startswith("STR"):
        sources.add("SRC-ASCE-SEI-7")
    if path_code.startswith("OPS"):
        sources.add("SRC-NIBS-WBDG-COMMISSIONING")
    if "access" in clusters:
        sources.add("SRC-US-ACCESS-BOARD-ADA-PROWAG")
    if "utility" in clusters:
        sources.add("SRC-FHWA-ASCE-38-SUE-UTILITY-DATA")
    if "flood" in clusters:
        sources.add("SRC-ASCE-24-FLOOD-RESISTANT")
        sources.add("SRC-ICC-IBC-IPC-IFC-IECC-IEBC")
    if "stormwater" in clusters or "drainage" in clusters:
        sources.add("SRC-FHWA-HEC-22-URBAN-DRAINAGE")
    if "pavement" in clusters:
        sources.add("SRC-FHWA-GEOTECH-SUBSURFACE-INVESTIGATION")
    if "handoff" in clusters or "operations" in clusters:
        sources.add("SRC-NIBS-WBDG-COMMISSIONING")
    if "low_impact" in clusters:
        sources.add("SRC-EPA-GREEN-INFRASTRUCTURE")
    if "concrete" in clusters or path_code.startswith(("STR.RCS", "STR.FND")):
        sources.add("SRC-ACI-318-STRUCTURAL-CONCRETE")
    if path_code.startswith("STR.SSS"):
        sources.add("SRC-AISC-360-STRUCTURAL-STEEL")
    if "facade" in clusters or "roof" in clusters or "movement" in clusters:
        sources.add("SRC-NIBS-WBDG-BUILDING-ENVELOPE")
    return sorted(sources)


def _node_kind_for_path(path_code: str, clusters: str) -> str:
    if path_code.startswith("ARC"):
        return "architectural_coordination_concept"
    if path_code.startswith("CIV"):
        return "civil_site_or_drainage_concept"
    if path_code.startswith("GEO"):
        return "geotechnical_site_condition_or_process"
    if path_code.startswith("OPS"):
        return "operations_handover_record"
    if path_code.startswith("STR.LOA"):
        return "structural_load_concept"
    if path_code.startswith("STR.TMA"):
        return "temporary_works_concept"
    return "structural_engineering_concept"


def _relationship_key(row: dict[str, Any]) -> tuple[str, str, str]:
    return (
        str(row.get("from_id") or ""),
        str(row.get("predicate") or row.get("edge_type") or ""),
        str(row.get("to_id") or ""),
        str(row.get("relation_type") or ""),
    )


def _source_family_ids_used() -> set[str]:
    ids = {row[0] for row in SOURCE_ROWS}
    for spec in _node_specs():
        ids.update(spec["sources"])
    for spec in _refinement_specs():
        ids.update(spec["sources"])
    for spec in _edge_specs():
        ids.update(spec["source_family_ids"])
    for _, _, _, _, _, sources, _ in RESOLVER_CASES:
        ids.update(sources)
    return ids


def _split_semicolon(value: str) -> list[str]:
    return [item.strip() for item in value.split(";") if item.strip()]


def _dict_list(value: Any) -> list[dict[str, Any]]:
    return [item for item in value if isinstance(item, dict)] if isinstance(value, list) else []


def _list_strings(value: Any) -> list[str]:
    return [str(item).strip() for item in value if str(item).strip()] if isinstance(value, list) else []


def _load_json_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return payload


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _resolve_file(root: Path, path: Path) -> Path:
    resolved = path if path.is_absolute() else root / path
    resolved = resolved.resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"{path}: path must stay inside repository root") from exc
    if not resolved.is_file():
        raise FileNotFoundError(f"{path}: file does not exist")
    return resolved


def _resolve_report_path(root: Path, run_id: str, output_path: Path | None) -> Path:
    target = output_path if output_path is not None else REPORT_ROOT / run_id / REPORT_FILENAME
    resolved = target if target.is_absolute() else root / target
    resolved = resolved.resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"{target}: output path must stay inside repository root") from exc
    _reject_protected_write_target(root, resolved, "output_path")
    expected_root = (root / REPORT_ROOT).resolve()
    try:
        resolved.relative_to(expected_root)
    except ValueError as exc:
        raise ValueError(f"{target}: output path must stay inside {REPORT_ROOT.as_posix()}") from exc
    if resolved.name != REPORT_FILENAME:
        raise ValueError(f"{target}: output filename must be {REPORT_FILENAME}")
    resolved.parent.mkdir(parents=True, exist_ok=True)
    return resolved


def _reject_protected_write_target(root: Path, resolved: Path, label: str) -> None:
    raw_root = (root / RAW_SOURCE_ROOT).resolve()
    try:
        resolved.relative_to(raw_root)
    except ValueError:
        return
    raise ValueError(f"{label}: write target must not be inside immutable raw source custody layer {RAW_SOURCE_ROOT.as_posix()}")


def _repo_root(repo_root: str | Path | None) -> Path:
    return Path(repo_root).resolve() if repo_root is not None else Path.cwd().resolve()


def _run_id(run_id: str | None) -> str:
    value = run_id or datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    if not re.match(r"^[A-Za-z0-9_.-]+$", value):
        raise ValueError("run_id contains unsupported characters")
    return value


def _relative_to_root(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def _utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
