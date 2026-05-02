"""Bounded AEC-MEPFS domain-cluster enrichment for Backbone fixtures.

This module is intentionally file-backed and runtime-disconnected. It adds
source-family-grounded Backbone nodes, governed relationship metadata, source
rights rows, and resolver QA cases without importing protected source content,
rebuilding a live graph, writing Neo4j, or changing API/Explorer defaults.
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

GENERATION_METHOD = "steward_governed_aec_mepfs_domain_cluster_interrelationships_from_source_family_research"
HIERARCHY_GENERATION_METHOD = "steward_governed_aec_mepfs_domain_cluster_hierarchy_from_source_family_research"
REPORT_SCHEMA_VERSION = "aec-mepfs-domain-cluster-enrichment-report/v1"
DEFAULT_BACKBONE_PATH = Path("scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json")
DEFAULT_SOURCE_RIGHTS_PATH = Path(".ai/03_plans/AEC-MEPFS-Backbone/registry-candidates/source-rights-registry.json")
DEFAULT_READINESS_FIXTURE_PATH = Path("scripts/tests/fixtures/aec_mepfs_backbone/valid_readiness_s2.json")
REPORT_ROOT = Path("006_System-Manifests/aec-mepfs-backbone/domain-cluster-enrichment")
REPORT_FILENAME = "domain-cluster-enrichment-report.json"
OWNER = "Philip Lewis"
RELEASE_VERSION = "0.1.0"
ACCESS_DATE = "2026-05-01"
PROVENANCE_NOTE = (
    "Metadata-only source-family synthesis for AEC-MEPFS relationship reasoning; "
    "no protected source text, tables, figures, clauses, or source payloads ingested."
)

SOURCE_ROWS = [
    ("SRC-BUILDINGSMART-IDS-1-0", "buildingSMART Information Delivery Specification IDS 1.0", "buildingSMART International", "https://www.buildingsmart.org/standards/bsi-standards/information-delivery-specification-ids/", "open-reference", "metadata grounding for information-requirement and validation relationships only"),
    ("SRC-W3C-LBD-BOT", "W3C Linked Building Data Community Group Building Topology Ontology", "W3C Linked Building Data Community Group", "https://w3c-lbd-cg.github.io/bot/", "open-reference", "metadata grounding for building topology, space, element, and zone relationships"),
    ("SRC-BRICK-SCHEMA", "Brick Schema building metadata ontology", "Brick Schema project", "https://docs.brickschema.org/brick/overview.html", "open-reference", "metadata grounding for equipment, point, location, feed, and operational relationships"),
    ("SRC-PROJECT-HAYSTACK", "Project Haystack semantic modeling documentation", "Project Haystack", "https://project-haystack.org/doc/docHaystack/Intro", "open-reference", "metadata grounding for equipment, point, reference, trend, and command semantics"),
    ("SRC-CDC-LEGIONELLA-BUILDING-WATER", "CDC Legionella control and building water guidance", "Centers for Disease Control and Prevention", "https://www.cdc.gov/control-legionella/index.html", "reference_only", "public-health metadata grounding for building water risk-management relationships"),
    ("SRC-ASHRAE-188-LEGIONELLA", "ASHRAE Standard 188 Legionellosis risk management for building water systems", "ASHRAE", "https://www.ashrae.org/technical-resources/bookstore/ansi-ashrae-standard-188-2021-legionellosis-risk-management-for-building-water-systems", "reference_only", "metadata grounding for water-management-program relationships only"),
    ("SRC-WBDG-SYSTEMS-INTEGRATION", "Whole Building Design Guide systems integration and whole-building design guidance", "National Institute of Building Sciences Whole Building Design Guide", "https://www.wbdg.org/do/functional/systems-integration", "reference_only", "metadata grounding for interdisciplinary coordination, serviceability, O&M, and lifecycle relationships"),
    ("SRC-IAPMO-UPC-METADATA", "IAPMO Uniform Plumbing Code public metadata", "International Association of Plumbing and Mechanical Officials", "https://codes.iapmo.org/home.aspx?code=UPC", "reference_only", "jurisdiction-sensitive plumbing source-family metadata only"),
]

# id|path|label|definition|aliases(;)|clusters(;)
NODE_ROWS = """
VTN-DOM-0012678|ARC.SPC.OCP|Occupied Space|A usable building space whose expected occupants drive ventilation, egress, lighting, plumbing, comfort, and life-safety coordination.|occupiable space;occupied room|occupancy_hvac_comfort;egress_fire_plumbing
VTN-DOM-0012679|ARC.BLD.SRV.MPR|Mechanical Plant Room|A building services room allocated for major mechanical equipment, clearances, replacement access, drainage, power, ventilation, and separation coordination.|plant room;mechanical equipment room|plant_room_coordination
VTN-DOM-0012680|ARC.BLD.SRV.CSV|Ceiling Services Void|A ceiling or plenum zone used to route and access building services while respecting fire, acoustic, structural, and maintenance constraints.|ceiling void;ceiling plenum|plant_room_coordination;fire_penetration_coordination
VTN-DOM-0012681|ARC.BLD.SRV.RIS|Service Riser|A vertical services zone used to route ducts, pipes, cables, or fire-protection services between levels with compartmentation and access coordination.|riser shaft;services riser|fire_penetration_coordination;plant_room_coordination
VTN-DOM-0012682|ARC.BLD.SRV.MAZ|Maintenance Access Zone|An allocated spatial clearance zone that enables inspection, testing, cleaning, filter replacement, valve operation, or component maintenance.|service clearance;access clearance|plant_room_coordination;operations_handover
VTN-DOM-0012683|ARC.BLD.SRV.RPT|Equipment Replacement Path|A lifecycle access route reserved so large maintainable assets can be removed and replaced without destructive building intervention where feasible.|replacement route;asset removal path|plant_room_coordination;operations_handover
VTN-DOM-0012684|ARC.ECD.DLG|Daylighting Design|Architectural planning of useful daylight while coordinating glare, envelope loads, lighting controls, comfort, and energy performance.|daylight strategy|occupancy_hvac_comfort;sustainability_performance
VTN-DOM-0012685|STR.NSC.EQL|Equipment Load Allowance|Structural allowance for permanent equipment loads, dynamic effects, maintenance loads, and replacement scenarios assigned during coordination.|equipment loads;plant load allowance|plant_room_coordination;electrical_mechanical_resilience
VTN-DOM-0012686|STR.NSC.VIR|Vibration Isolation Support|Structural and services coordination for mounts or supports that limit vibration transfer from equipment into the building fabric.|vibration isolation;resilient equipment support|plant_room_coordination
VTN-DOM-0012687|STR.NSC.SBR|Seismic Bracing And Restraint|Nonstructural support coordination for mechanical, electrical, plumbing, and fire-protection components subject to seismic restraint requirements.|seismic restraint;seismic bracing|plant_room_coordination;fire_pump_sprinkler_alarm_power
VTN-DOM-0012688|STR.NSC.SLV|Sleeve And Opening Coordination|Coordination of structural sleeves, embeds, and openings for routed services while preserving structural capacity and fire-resistance intent.|structural opening coordination;service sleeves|fire_penetration_coordination;plant_room_coordination
VTN-DOM-0012689|MEC.AHD.DUD.SAD|Supply Air Duct|A duct path that conveys supply air from air-handling or terminal equipment toward served spaces through coordinated routing and fire or smoke interfaces.|supply duct;supply ductwork|occupancy_hvac_comfort;fire_penetration_coordination
VTN-DOM-0012690|MEC.AHD.DUD.RAD|Return Air Duct|A duct path or return-air route that conveys room or zone air back toward air-handling equipment or relief and exhaust strategy.|return duct;return air path|occupancy_hvac_comfort
VTN-DOM-0012691|MEC.AHD.DTD.SDF|Supply Air Diffuser|An air terminal device that introduces supply air into a space with distribution, comfort, noise, ceiling, and maintenance implications.|diffuser;supply diffuser|occupancy_hvac_comfort
VTN-DOM-0012692|MEC.AHD.DTD.VAV|Variable Air Volume Terminal Unit|A terminal device that modulates supply airflow to a zone and can integrate reheating, controls, power, balancing, and maintenance requirements.|VAV box;VAV terminal|occupancy_hvac_comfort;electrical_mechanical_resilience
VTN-DOM-0012693|MEC.ACD.ZON.HVZ|HVAC Zone|A control or load zone served by HVAC equipment based on thermal load, ventilation, occupancy, exposure, schedule, and control strategy.|thermal zone;conditioning zone|occupancy_hvac_comfort
VTN-DOM-0012694|MEC.CTL.SNS.COS|Carbon Dioxide Sensor|A sensing point used as an indoor-air-quality or demand-control input where a design sequence uses carbon dioxide as an occupancy or ventilation proxy.|CO2 sensor;carbon dioxide point|occupancy_hvac_comfort;operations_handover
VTN-DOM-0012695|MEC.CTL.SNS.TMS|Temperature Sensor|A sensing point that measures space, duct, pipe, or equipment temperature for control, monitoring, comfort, alarms, or analytics.|temperature point;space temperature sensor|occupancy_hvac_comfort;operations_handover
VTN-DOM-0012696|MEC.SMK.EXH.SCF|Smoke Control Fan|A fan assigned to smoke-control or smoke-exhaust operation with fire-alarm, damper, power, testing, and compartmentation interfaces.|smoke exhaust fan;smoke management fan|fire_penetration_coordination;fire_pump_sprinkler_alarm_power
VTN-DOM-0012697|ELE.PDS.TRS.SWG|Main Switchgear|Primary electrical distribution equipment that receives service or transformer output and distributes power to downstream feeders or distribution equipment.|switchgear;main distribution switchgear|electrical_mechanical_resilience;plant_room_coordination
VTN-DOM-0012698|ELE.PDS.TRS.XFM|Distribution Transformer|Electrical equipment that changes voltage levels for downstream distribution and imposes heat, clearance, access, support, and protection requirements.|transformer|electrical_mechanical_resilience
VTN-DOM-0012699|ELE.PDS.PAF.PNL|Panelboard|Electrical distribution assembly containing overcurrent devices that feed branch circuits or loads and require access, labeling, and coordination.|distribution board;electrical panel|electrical_mechanical_resilience
VTN-DOM-0012700|ELE.PDS.PAF.FDR|Feeder|Electrical conductor path that supplies downstream distribution equipment or major loads from a source distribution point.|electrical feeder|electrical_mechanical_resilience
VTN-DOM-0012701|ELE.PDS.BRC.CIR|Branch Circuit|Final electrical circuit segment that supplies utilization equipment, receptacles, lighting, control panels, or other loads.|circuit;final circuit|electrical_mechanical_resilience
VTN-DOM-0012702|ELE.ESP.GTS.ATS|Automatic Transfer Switch|Electrical switching equipment that transfers selected loads between normal and alternate power sources according to the emergency or standby power strategy.|ATS;transfer switch|electrical_mechanical_resilience;fire_pump_sprinkler_alarm_power
VTN-DOM-0012703|ELE.CTL.BMS.NET|BMS Network|Controls communication infrastructure that links controllers, equipment, meters, sensors, alarms, and supervisory building management functions.|building management network;controls network|occupancy_hvac_comfort;operations_handover
VTN-DOM-0012704|PLS.PWS.WSM.CWS|Potable Cold Water Distribution|Domestic cold-water distribution serving fixtures and equipment while protecting water quality, pressure, backflow boundaries, and maintenance access.|cold water supply;domestic cold water|plumbing_public_health
VTN-DOM-0012705|PLS.HOT.WHE.DWH|Domestic Water Heater|Equipment that heats potable water for fixtures or processes and interfaces with energy, controls, safety devices, maintenance, and water-quality programs.|water heater;domestic hot water heater|plumbing_public_health;electrical_mechanical_resilience
VTN-DOM-0012706|PLS.PFE.FIS.PFX|Plumbing Fixture|A plumbing endpoint such as a lavatory, sink, shower, water closet, or similar fixture requiring supply, drainage, venting, access, and public-health coordination.|fixture;sanitary fixture|plumbing_public_health;egress_fire_plumbing
VTN-DOM-0012707|PLS.SDS.DRS.SDR|Sanitary Drainage Piping|Drainage piping that conveys sanitary waste from fixtures toward stacks, building drains, treatment, or utility connection with slope and venting coordination.|sanitary drain;waste pipe|plumbing_public_health
VTN-DOM-0012708|PLS.SAN.TRA.FXT|Fixture Trap|A trap associated with a plumbing fixture that maintains a water seal to separate occupied spaces from drainage system gases.|trap;P-trap|plumbing_public_health
VTN-DOM-0012709|PLS.VES.VPS.VST|Vent Stack|A plumbing vent path that supports pressure equalization and drainage function while coordinating roof penetrations, routing, and termination locations.|sanitary vent stack;vent pipe stack|plumbing_public_health;fire_penetration_coordination
VTN-DOM-0012710|PLS.PWS.BAP.BFP|Backflow Preventer|A device or assembly used to protect potable water from reverse flow contamination at defined hazard or connection boundaries.|backflow prevention assembly|plumbing_public_health;operations_handover
VTN-DOM-0012711|PLS.SDS.DRS.CDN|Condensate Drainage|Drainage path for condensate from cooling coils, dehumidification equipment, or other HVAC equipment requiring slope, trap, discharge, and access coordination.|condensate drain;AC condensate drain|occupancy_hvac_comfort;plumbing_public_health;plant_room_coordination
VTN-DOM-0012712|PLS.PWS.WSM.WQP|Building Water Quality Program|An operational program for monitoring and managing building water quality risks such as stagnation, temperature control, disinfectant residual, and maintenance actions.|water management program;building water safety program|plumbing_public_health;operations_handover
VTN-DOM-0012713|FLS.CMP.PEN.DUP|Duct Penetration|A duct opening through a wall, floor, shaft, or rated assembly that requires coordination of fire, smoke, structural, and mechanical performance.|duct opening;ductwork penetration|fire_penetration_coordination;occupancy_hvac_comfort
VTN-DOM-0012714|FLS.CMP.PEN.PIP|Pipe Penetration|A pipe opening through a wall, floor, shaft, or rated assembly requiring coordination of firestop, movement, sleeve, and serviceability requirements.|piping penetration|fire_penetration_coordination;plumbing_public_health
VTN-DOM-0012715|FLS.CMP.PEN.CAB|Cable Penetration|A cable, conduit, or cable-tray opening through a wall, floor, shaft, or rated assembly requiring firestop and pathway coordination.|conduit penetration;cable tray penetration|fire_penetration_coordination;electrical_mechanical_resilience
VTN-DOM-0012716|FLS.CMP.PEN.FST|Firestop System|A tested or engineered penetration-protection approach used to maintain fire-resistance continuity where services pass through protected assemblies.|firestopping;penetration firestop|fire_penetration_coordination
VTN-DOM-0012717|FLS.SCC.FID.FDA|Fire Damper Assembly|A damper assembly used at selected duct openings to help maintain fire-resistance compartmentation where required by the design and adopted code.|fire damper|fire_penetration_coordination
VTN-DOM-0012718|FLS.SCC.SMD|Smoke Damper|A damper used to limit smoke movement or participate in smoke-control sequences where required by the smoke-control and compartmentation strategy.|smoke control damper|fire_penetration_coordination;fire_pump_sprinkler_alarm_power
VTN-DOM-0012719|FLS.CMP.FBA.FDR|Fire Door Assembly|A protected opening assembly in a fire-resistance-rated barrier that coordinates door hardware, smoke control, egress, inspection, and compartmentation performance.|fire door|fire_penetration_coordination;egress_fire_plumbing
VTN-DOM-0012720|FLS.FPR.SPR.SYS|Automatic Sprinkler System|A fire-protection water-based system arranged to detect heat at sprinklers and discharge water over a protected area according to the hazard and design basis.|sprinkler system|fire_pump_sprinkler_alarm_power
VTN-DOM-0012721|FLS.FPR.SPR.ZON|Sprinkler Zone|A sprinkler control, alarm, or design zone used to organize waterflow monitoring, isolation, inspection, and protected-area reasoning.|sprinkler control zone;sprinkler alarm zone|fire_pump_sprinkler_alarm_power
VTN-DOM-0012722|FLS.FPR.FPU.PMP|Fire Pump Assembly|A fire pump and associated appurtenances that supply pressure and flow to water-based fire-protection systems where the water supply alone is insufficient.|fire pump;stationary fire pump|fire_pump_sprinkler_alarm_power;plant_room_coordination
VTN-DOM-0012723|FLS.FPR.FPU.CTR|Fire Pump Controller|Control equipment associated with a fire pump that starts, supervises, and interfaces the pump with power, alarms, testing, and protection sequences.|fire pump control panel|fire_pump_sprinkler_alarm_power
VTN-DOM-0012724|FLS.FPR.FPU.JKY|Jockey Pump|A pressure-maintenance pump used in some fire-protection systems to maintain system pressure without starting the main fire pump for minor pressure losses.|pressure maintenance pump|fire_pump_sprinkler_alarm_power
VTN-DOM-0012725|FLS.FDA.IND.FSW|Waterflow Switch|A fire-protection initiating device used to signal water movement from sprinkler or standpipe system operation to the fire alarm system.|flow switch;sprinkler waterflow switch|fire_pump_sprinkler_alarm_power
VTN-DOM-0012726|FLS.FDA.IND.TSW|Valve Tamper Switch|A supervisory initiating device used to monitor the position of a fire-protection control valve and report abnormal valve status.|tamper switch;supervisory valve switch|fire_pump_sprinkler_alarm_power
VTN-DOM-0012727|OPS.AST.REG.MAR|Maintainable Asset Record|An asset-register entry for equipment or components that require maintenance, inspection, replacement, warranty tracking, or operational analytics.|maintainable asset;asset record|operations_handover
VTN-DOM-0012728|OPS.PRM.MAS.PMS|Preventive Maintenance Schedule|A recurring maintenance plan that assigns inspection, testing, calibration, cleaning, or replacement activities to maintainable assets.|PM schedule;planned maintenance schedule|operations_handover
VTN-DOM-0012729|OPS.FAC.WOR.CWO|Corrective Work Order|A facilities work record generated to investigate, repair, reset, or replace an asset after a fault, alarm, failure, or occupant request.|work order;corrective maintenance order|operations_handover
VTN-DOM-0012730|SMS.BUA.ATL.ALM|BMS Alarm|A building management alarm event associated with monitored equipment, sensors, setpoints, faults, or operating states.|controls alarm;building automation alarm|operations_handover;occupancy_hvac_comfort
VTN-DOM-0012731|DIG.DTA.SDS.TRD|Trend Data|Time-series operational data recorded from meters, sensors, commands, alarms, or equipment points for analytics, commissioning, or fault detection.|historian data;time series|operations_handover;sustainability_performance
VTN-DOM-0012732|DIG.DTA.AIR.EIR|Exchange Information Requirement|A structured statement of information needed at an exchange point to support design, construction, handover, operation, or validation.|EIR;information exchange requirement|operations_handover;sustainability_performance
VTN-DOM-0012733|PER.IEQ.TCO|Thermal Comfort Performance|Performance outcome describing occupant thermal satisfaction as influenced by temperature, humidity, air movement, radiant effects, clothing, activity, and control.|thermal comfort|occupancy_hvac_comfort;sustainability_performance
VTN-DOM-0012734|PER.IEQ.IAQ|Indoor Air Quality Performance|Performance outcome for acceptable indoor air quality as influenced by ventilation, source control, filtration, humidity, operation, and monitoring.|IAQ performance;indoor environmental quality air|occupancy_hvac_comfort;sustainability_performance
VTN-DOM-0012735|PER.ENE.OEM|Operational Energy Metering|Metering and data organization for measuring energy use by building, system, distribution board, equipment, or end-use category.|energy metering;submetered energy|electrical_mechanical_resilience;sustainability_performance;operations_handover
VTN-DOM-0012736|SUS.ECS.ECA|Embodied Carbon Assessment|Lifecycle assessment activity estimating greenhouse-gas impacts associated with materials, products, construction, replacement, and end-of-life scenarios.|embodied carbon;whole-life carbon assessment|sustainability_performance
VTN-DOM-0012737|SUS.WAC.WEF|Water Efficiency|Performance strategy for reducing potable water demand, losses, and waste while maintaining hygiene, function, maintainability, and user needs.|water conservation;water-use efficiency|plumbing_public_health;sustainability_performance
""".strip()

# from|to|predicate|relation_type|category|nature(;)|weight|confidence|discipline(;)|lifecycle(;)|sources(;)|rationale
EDGE_ROWS = """
ARC.SPC.OCP|COM.OCC.OLO|requires|drives_occupant_load_assessment|dependency|informational;regulatory|0.86|0.86|architecture;compliance|planning;design|SRC-ICC-IBC-IPC-IFC-IECC-IEBC;SRC-WBDG-SYSTEMS-INTEGRATION|Expected use of an occupied space is an input to occupant-load reasoning used by egress, fixtures, and services planning.
COM.OCC.OLO|MEC.IEQ.VER|constrains|drives_ventilation_demand|performance|performance;regulatory|0.90|0.86|mechanical;architecture;compliance|design;operation|SRC-ASHRAE-62-1-90-1-55-CX;SRC-ICC-IBC-IPC-IFC-IECC-IEBC|Occupant load and use assumptions influence nonresidential ventilation demand and indoor-air-quality design inputs.
COM.OCC.OLO|FLS.EGR.OLO|constrains|drives_egress_capacity|regulatory_authority|safety-critical;regulatory|0.88|0.84|fire_safety;architecture;compliance|planning;design|SRC-ICC-IBC-IPC-IFC-IECC-IEBC;SRC-NFPA-70-101-13-72-14-20|Occupant-load assumptions are used by life-safety and egress planning to size and verify exit capacity.
COM.OCC.OLO|PLS.PFE.FIS|constrains|drives_fixture_count_basis|regulatory_authority|regulatory;public-health|0.76|0.78|plumbing;architecture;compliance|planning;design|SRC-ICC-IBC-IPC-IFC-IECC-IEBC;SRC-IAPMO-UPC-METADATA|Occupancy and use categories commonly inform plumbing fixture-count and fixture-selection analysis under adopted plumbing codes.
COM.OCC.OLO|ELE.LLC|constrains|drives_lighting_load_and_controls|performance|performance;operational|0.67|0.72|electrical;architecture;sustainability|design;operation|SRC-ASHRAE-62-1-90-1-55-CX;SRC-WBDG-SYSTEMS-INTEGRATION|Occupancy, schedules, and use patterns influence lighting load assumptions and control zoning.
MEC.IEQ.VER|MEC.ACD.ZON.HVZ|constrains|constrains_hvac_zone_design|performance|performance;functional|0.84|0.82|mechanical;architecture|design;commissioning;operation|SRC-ASHRAE-62-1-90-1-55-CX;SRC-WBDG-SYSTEMS-INTEGRATION|Ventilation and IAQ criteria affect zone grouping, control sequence, and outdoor-air delivery strategy.
ARC.SPC.OCP|MEC.ACD.ZON.HVZ|constrains|space_use_informs_zone_grouping|spatial_topological|functional;performance|0.80|0.80|architecture;mechanical|planning;design|SRC-W3C-LBD-BOT;SRC-ASHRAE-62-1-90-1-55-CX|A space function, schedule, exposure, and occupancy are inputs to HVAC zone grouping; space and HVAC zone remain distinct concepts.
MEC.AHD.AHU|MEC.AHD.DUD.SAD|requires|supplies_air_to|system_flow|functional;physical|0.92|0.88|mechanical|design;construction;operation|SRC-ASHRAE-62-1-90-1-55-CX;SRC-WBDG-SYSTEMS-INTEGRATION|An AHU commonly delivers conditioned or ventilation air into a supply duct distribution path.
MEC.AHD.DUD.SAD|MEC.AHD.DTD.VAV|requires|supplies_air_to|system_flow|functional;physical|0.84|0.82|mechanical|design;construction;operation|SRC-ASHRAE-62-1-90-1-55-CX|A ducted VAV system routes supply air through ductwork to zone terminal units.
MEC.AHD.DTD.VAV|MEC.AHD.DTD.SDF|requires|supplies_air_to|system_flow|functional;physical|0.82|0.80|mechanical|design;construction;operation|SRC-ASHRAE-62-1-90-1-55-CX|Terminal units discharge air through downstream distribution and diffusers to the served zone.
MEC.AHD.DTD.SDF|ARC.SPC.OCP|requires|serves_space|functional_service|functional;performance|0.86|0.80|mechanical;architecture|design;construction;operation|SRC-W3C-LBD-BOT;SRC-ASHRAE-62-1-90-1-55-CX|A supply diffuser serves an occupied space by delivering air required for ventilation, conditioning, and comfort.
ARC.SPC.OCP|MEC.AHD.DUD.RAD|requires|returns_air_from|system_flow|functional;physical|0.78|0.74|mechanical;architecture|design;operation|SRC-ASHRAE-62-1-90-1-55-CX;SRC-WBDG-SYSTEMS-INTEGRATION|Occupied spaces often require an engineered return, transfer, relief, or exhaust path to complete air-distribution balance.
MEC.AHD.DUD.RAD|MEC.AHD.AHU|requires|returns_air_to|system_flow|functional;physical|0.78|0.74|mechanical|design;operation|SRC-ASHRAE-62-1-90-1-55-CX|Return-air paths commonly deliver air back to AHU mixing, filtration, relief, or recirculation functions.
MEC.CTL.SNS.COS|ARC.SPC.OCP|requires|measures_space_condition|functional_service|operational;performance|0.76|0.74|mechanical;operations;smart_systems|design;commissioning;operation|SRC-ASHRAE-62-1-90-1-55-CX;SRC-BRICK-SCHEMA;SRC-PROJECT-HAYSTACK|A CO2 sensor can provide a measured proxy for occupancy or ventilation-control logic in a served space.
MEC.CTL.SNS.TMS|MEC.ACD.ZON.HVZ|requires|measures_zone_temperature|functional_service|operational;performance|0.84|0.82|mechanical;operations;smart_systems|design;commissioning;operation|SRC-BRICK-SCHEMA;SRC-PROJECT-HAYSTACK;SRC-ASHRAE-62-1-90-1-55-CX|Temperature sensing is a typical feedback input for HVAC zone control and comfort monitoring.
ELE.CTL.BMS.NET|MEC.AHD.DTD.VAV|requires|controls|functional_service|operational;informational|0.80|0.78|electrical;mechanical;smart_systems|design;commissioning;operation|SRC-BRICK-SCHEMA;SRC-PROJECT-HAYSTACK|A BMS network commonly communicates supervisory commands, setpoints, alarms, or status points for terminal-unit control.
ELE.CTL.BMS.NET|MEC.AHD.AHU|requires|controls|functional_service|operational;informational|0.82|0.80|electrical;mechanical;smart_systems|design;commissioning;operation|SRC-BRICK-SCHEMA;SRC-PROJECT-HAYSTACK;SRC-WBDG-SYSTEMS-INTEGRATION|AHU operation is commonly supervised by building management controls for schedules, setpoints, safeties, and alarms.
MEC.AHD.AHU|PER.IEQ.TCO|constrains|impacts_thermal_comfort|performance_sustainability|performance;operational|0.84|0.82|mechanical;performance|design;commissioning;operation|SRC-ASHRAE-62-1-90-1-55-CX;SRC-WBDG-SYSTEMS-INTEGRATION|AHU capacity, control, distribution, and commissioning materially affect delivered thermal comfort.
MEC.AHD.AHU|PER.IEQ.IAQ|constrains|impacts_indoor_air_quality|performance_sustainability|performance;operational|0.86|0.84|mechanical;performance|design;commissioning;operation|SRC-ASHRAE-62-1-90-1-55-CX|Ventilation, filtration, outdoor-air intake, and operation of AHUs affect indoor-air-quality outcomes.
MEC.AHD.AHU|PER.ENE.OEM|constrains|consumes_energy_measured_by|performance_sustainability|performance;operational|0.82|0.78|mechanical;electrical;sustainability|design;operation|SRC-ASHRAE-62-1-90-1-55-CX;SRC-WBDG-SYSTEMS-INTEGRATION|Fan, coil, and control operation drive operational energy use that should be metered or estimated for performance management.
ARC.ECD.DLG|PER.ENE.OEM|constrains|reduces_or_shifts_lighting_energy|performance_sustainability|performance;sustainability|0.64|0.70|architecture;electrical;sustainability|planning;design;operation|SRC-WBDG-SYSTEMS-INTEGRATION;SRC-ASHRAE-62-1-90-1-55-CX|Daylighting and controls can reduce or shift electric lighting demand while creating envelope and glare tradeoffs.
FLS.CMP.FBA|FLS.CMP|part_of|supports_compartmentation|physical_composition|safety-critical;physical|0.90|0.86|fire_safety;architecture|design;construction;operation|SRC-ICC-IBC-IPC-IFC-IECC-IEBC;SRC-NFPA-70-101-13-72-14-20|Fire barriers are components of a compartmentation strategy that limits fire and smoke spread.
MAT.ASM.FRW|FLS.CMP.FBA|part_of|forms_fire_resistance_boundary|physical_composition|safety-critical;physical|0.86|0.82|architecture;fire_safety|design;construction;operation|SRC-ICC-IBC-IPC-IFC-IECC-IEBC|A fire-rated wall assembly can form part of a fire barrier or compartment boundary where the design requires separation.
FLS.CMP.PEN.DUP|MAT.ASM.FRW|constrains|penetrates_fire_rated_assembly|physical_composition|safety-critical;physical|0.82|0.80|mechanical;fire_safety;architecture|design;construction;inspection|SRC-ICC-IBC-IPC-IFC-IECC-IEBC;SRC-NFPA-70-101-13-72-14-20|Duct openings through rated walls require coordinated protection to preserve the intended rating and smoke or fire strategy.
FLS.CMP.PEN.PIP|MAT.ASM.FRW|constrains|penetrates_fire_rated_assembly|physical_composition|safety-critical;physical|0.82|0.80|plumbing;fire_safety;architecture|design;construction;inspection|SRC-ICC-IBC-IPC-IFC-IECC-IEBC|Pipe openings through rated assemblies require appropriate sleeve, annular-space, movement, and firestop coordination.
FLS.CMP.PEN.CAB|MAT.ASM.FRW|constrains|penetrates_fire_rated_assembly|physical_composition|safety-critical;physical|0.82|0.80|electrical;fire_safety;architecture|design;construction;inspection|SRC-ICC-IBC-IPC-IFC-IECC-IEBC;SRC-NFPA-70-101-13-72-14-20|Cable, conduit, or cable-tray openings through rated assemblies require pathway and firestop coordination.
FLS.CMP.PEN.FST|FLS.CMP.PEN.PIP|requires|protects_penetration|functional_service|safety-critical;physical|0.90|0.84|fire_safety;plumbing;construction|design;construction;inspection;operation|SRC-ICC-IBC-IPC-IFC-IECC-IEBC|A firestop system protects many pipe penetrations when matched to the assembly and service condition.
FLS.CMP.PEN.FST|FLS.CMP.PEN.CAB|requires|protects_penetration|functional_service|safety-critical;physical|0.90|0.84|fire_safety;electrical;construction|design;construction;inspection;operation|SRC-ICC-IBC-IPC-IFC-IECC-IEBC;SRC-NFPA-70-101-13-72-14-20|A firestop or protected pathway solution is needed for many electrical penetrations through rated assemblies.
FLS.CMP.PEN.FST|FLS.CMP.PEN.DUP|requires|protects_penetration_when_applicable|functional_service|safety-critical;physical|0.72|0.76|fire_safety;mechanical;construction|design;construction;inspection;operation|SRC-ICC-IBC-IPC-IFC-IECC-IEBC|Some duct penetration conditions use firestop or sealing systems depending on tested assembly and code path.
FLS.SCC.FID.FDA|FLS.CMP.PEN.DUP|requires|protects_duct_opening|functional_service|safety-critical;physical|0.84|0.78|fire_safety;mechanical|design;construction;inspection;operation|SRC-ICC-IBC-IPC-IFC-IECC-IEBC;SRC-NFPA-70-101-13-72-14-20|A fire damper assembly may be required at selected duct openings through rated construction to preserve fire separation.
FLS.SCC.SMD|FLS.CMP.PEN.DUP|requires|limits_smoke_transfer_at_duct_opening|functional_service|safety-critical;physical;operational|0.78|0.76|fire_safety;mechanical|design;commissioning;operation|SRC-NFPA-CODES;SRC-ICC-IBC-IPC-IFC-IECC-IEBC|A smoke damper may be part of a smoke-control or compartmentation strategy at selected duct openings.
FLS.CMP.FBA.FDR|FLS.CMP.FBA|part_of|protects_opening|physical_composition|safety-critical;physical|0.86|0.82|fire_safety;architecture|design;construction;inspection;operation|SRC-ICC-IBC-IPC-IFC-IECC-IEBC;SRC-NFPA-70-101-13-72-14-20|A fire door assembly protects an opening in a fire barrier while maintaining circulation and egress where allowed.
FLS.CMP|FLS.EGR|requires|supports_egress_tenability|risk_failure|safety-critical;regulatory|0.84|0.80|fire_safety;architecture|planning;design;operation|SRC-ICC-IBC-IPC-IFC-IECC-IEBC;SRC-NFPA-70-101-13-72-14-20|Compartmentation supports life-safety strategy by limiting spread and helping protect egress routes.
CON.QAC|FLS.CMP.PEN.FST|requires|inspects_firestop_installation|lifecycle_process|safety-critical;operational|0.78|0.76|construction;fire_safety|construction;inspection;operation|SRC-ICC-IBC-IPC-IFC-IECC-IEBC;SRC-WBDG-SYSTEMS-INTEGRATION|Penetration protection depends on installed condition, so inspection and quality control are part of maintaining barrier performance.
STR.NSC.SLV|FLS.CMP.PEN.PIP|requires|coordinates_sleeve_and_firestop|dependency|physical;safety-critical|0.80|0.78|structural;plumbing;fire_safety|design;construction|SRC-ICC-IBC-IPC-IFC-IECC-IEBC;SRC-WBDG-SYSTEMS-INTEGRATION|Pipe penetrations require coordinated sleeves and openings so structural capacity and firestop geometry are not treated independently.
STR.NSC.SLV|FLS.CMP.PEN.DUP|requires|coordinates_structural_opening|dependency|physical;safety-critical|0.80|0.76|structural;mechanical;fire_safety|design;construction|SRC-WBDG-SYSTEMS-INTEGRATION;SRC-ICC-IBC-IPC-IFC-IECC-IEBC|Duct openings through structure and rated assemblies need coordinated geometry, support, and protection strategy.
FLS.FPR.FPU.PMP|FLS.FPR.FPU|part_of|part_of_fire_pump_system|physical_composition|physical;safety-critical|0.94|0.88|fire_safety;plumbing|design;construction;operation|SRC-NFPA-70-101-13-72-14-20;SRC-NFPA-CODES|A fire pump assembly is a primary component within the fire-pump system concept.
FLS.FPR.FPU.CTR|FLS.FPR.FPU.PMP|requires|controls_fire_pump|functional_service|safety-critical;operational|0.92|0.86|fire_safety;electrical|design;commissioning;operation|SRC-NFPA-70-101-13-72-14-20;SRC-NFPA-CODES|A fire pump controller supervises and starts the fire pump according to the fire-protection design.
FLS.FPR.FPU.PMP|FLS.FPR.SPR.SYS|requires|supplies_fire_protection_water_to|system_flow|safety-critical;physical|0.90|0.84|fire_safety;plumbing|design;construction;operation|SRC-NFPA-70-101-13-72-14-20;SRC-NFPA-CODES|Where provided, a fire pump supplies pressure and flow needed by sprinkler system demand.
FLS.FPR.FPU.PMP|FLS.FPR.STP|requires|supplies_fire_protection_water_to|system_flow|safety-critical;physical|0.88|0.82|fire_safety;plumbing|design;construction;operation|SRC-NFPA-70-101-13-72-14-20;SRC-NFPA-CODES|A fire pump may also support standpipe demand depending on system design and code basis.
FLS.FPR.SPR.ZON|FLS.FPR.SPR.SYS|part_of|part_of_sprinkler_system|physical_composition|safety-critical;physical|0.84|0.80|fire_safety|design;construction;operation|SRC-NFPA-70-101-13-72-14-20|Sprinkler systems are commonly organized by zones for control, isolation, alarm, and inspection.
FLS.FDA.IND.FSW|FLS.FPR.SPR.ZON|requires|monitors_waterflow|functional_service|safety-critical;operational|0.86|0.82|fire_safety;electrical|design;commissioning;operation|SRC-NFPA-70-101-13-72-14-20;SRC-NFPA-CODES|Waterflow switches provide fire alarm initiating signals associated with sprinkler water movement.
FLS.FDA.IND.TSW|FLS.FPR.SPR.ZON|requires|monitors_control_valve_status|functional_service|safety-critical;operational|0.82|0.80|fire_safety;electrical|design;commissioning;operation|SRC-NFPA-70-101-13-72-14-20;SRC-NFPA-CODES|Tamper switches help supervise fire-protection valve position so impaired sprinkler zones can be identified.
FLS.FDA.IND.FSW|FLS.FDA.FAC|requires|monitored_by_fire_alarm|functional_service|safety-critical;informational|0.88|0.84|fire_safety;electrical|design;commissioning;operation|SRC-NFPA-70-101-13-72-14-20;SRC-NFPA-CODES|Waterflow alarm signals are monitored and processed by the fire alarm control unit.
FLS.FDA.IND.TSW|FLS.FDA.FAC|requires|monitored_by_fire_alarm|functional_service|safety-critical;informational|0.86|0.84|fire_safety;electrical|design;commissioning;operation|SRC-NFPA-70-101-13-72-14-20;SRC-NFPA-CODES|Valve supervisory devices report abnormal valve status to the fire alarm control unit.
FLS.FDA.FAC|FLS.FDA.NOA|requires|notifies_occupants|functional_service|safety-critical;operational|0.90|0.86|fire_safety;electrical|design;commissioning;operation|SRC-NFPA-70-101-13-72-14-20;SRC-NFPA-CODES|Fire alarm control functions activate notification appliances according to the alarm and emergency communication design.
ELE.ESP.GTS.ATS|FLS.FPR.FPU.CTR|requires|requires_emergency_power|dependency|safety-critical;operational|0.78|0.74|electrical;fire_safety|design;commissioning;operation|SRC-NFPA-70-101-13-72-14-20;SRC-NFPA-4-25-110-ITM-EPSS|Selected fire pump arrangements can require alternate or protected power interfaces depending on design, driver, and adopted code.
ELE.ESP.GTS.ATS|FLS.FDA.FAC|requires|requires_emergency_power|dependency|safety-critical;operational|0.78|0.78|electrical;fire_safety|design;commissioning;operation|SRC-NFPA-70-101-13-72-14-20;SRC-NFPA-4-25-110-ITM-EPSS|Fire alarm power continuity is a life-safety coordination issue involving normal, standby, or battery-backed arrangements.
CON.COM.IST|FLS.FPR.FPU.PMP|requires|verified_by_integrated_systems_testing|lifecycle_process|safety-critical;operational|0.76|0.76|commissioning;fire_safety|commissioning;operation|SRC-NFPA-4-25-110-ITM-EPSS;SRC-ASHRAE-IES-202-CX|Fire pump readiness depends on testing of pump, controller, power, alarms, and water-supply interfaces.
FLS.FPR.FPU.PMP|FLS.EGR|constrains|failure_impacts_life_safety|risk_failure|safety-critical;risk|0.86|0.78|fire_safety;operations|operation;maintenance|SRC-NFPA-70-101-13-72-14-20;SRC-NFPA-4-25-110-ITM-EPSS|Loss of required fire pump function can impair water-based fire protection and therefore life-safety strategy.
ELE.PDS.TRS.XFM|ELE.PDS.TRS.SWG|requires|supplies_power_to|system_flow|physical;functional|0.86|0.80|electrical|design;construction;operation|SRC-NFPA-70-101-13-72-14-20;SRC-WBDG-SYSTEMS-INTEGRATION|A transformer commonly supplies downstream switchgear after voltage transformation.
ELE.PDS.TRS.SWG|ELE.PDS.PAF.FDR|requires|supplies_power_to|system_flow|physical;functional|0.90|0.84|electrical|design;construction;operation|SRC-NFPA-70-101-13-72-14-20|Main switchgear distributes power through feeders to downstream equipment.
ELE.PDS.PAF.FDR|ELE.PDS.PAF.PNL|requires|supplies_power_to|system_flow|physical;functional|0.88|0.84|electrical|design;construction;operation|SRC-NFPA-70-101-13-72-14-20|Feeders supply panelboards or distribution equipment according to electrical distribution design.
ELE.PDS.PAF.PNL|ELE.PDS.BRC.CIR|requires|supplies_power_to|system_flow|physical;functional|0.90|0.86|electrical|design;construction;operation|SRC-NFPA-70-101-13-72-14-20|Panelboards supply branch circuits that serve final utilization loads.
ELE.PDS.BRC.CIR|MEC.AHD.AHU|requires|powers|dependency|functional;operational|0.86|0.80|electrical;mechanical|design;construction;operation|SRC-WBDG-SYSTEMS-INTEGRATION;SRC-NFPA-70-101-13-72-14-20|AHU fans, controls, and auxiliaries depend on electrical circuits or feeders for operation.
ELE.PDS.BRC.CIR|MEC.PLT.PMP|requires|powers|dependency|functional;operational|0.84|0.80|electrical;mechanical|design;construction;operation|SRC-WBDG-SYSTEMS-INTEGRATION;SRC-NFPA-70-101-13-72-14-20|Mechanical pumps require electrical power and coordinated disconnect, controls, and maintenance access.
ELE.PDS.BRC.CIR|MEC.PLT.CHL|requires|powers|dependency|functional;operational|0.84|0.78|electrical;mechanical|design;construction;operation|SRC-WBDG-SYSTEMS-INTEGRATION;SRC-NFPA-70-101-13-72-14-20|Chillers and auxiliaries require coordinated electrical supply and operational monitoring.
ELE.PDS.BRC.CIR|MEC.AHD.DTD.VAV|requires|powers|dependency|functional;operational|0.72|0.72|electrical;mechanical|design;construction;operation|SRC-WBDG-SYSTEMS-INTEGRATION|Some terminal units require electrical power for actuators, controls, reheat, or fan-powered operation.
ELE.PDS.BRC.CIR|ELE.CTL.BMS.NET|requires|powers_controls_network|dependency|operational;informational|0.78|0.76|electrical;smart_systems|design;construction;operation|SRC-BRICK-SCHEMA;SRC-PROJECT-HAYSTACK;SRC-WBDG-SYSTEMS-INTEGRATION|Controllers and network equipment require reliable power for monitoring, control, alarms, and trends.
ELE.ESP.GTS.ATS|ELE.ESP.LSL|part_of|backs_up_selected_life_safety_loads|dependency|safety-critical;operational|0.84|0.78|electrical;fire_safety|design;commissioning;operation|SRC-NFPA-70-101-13-72-14-20;SRC-NFPA-4-25-110-ITM-EPSS|Transfer equipment participates in emergency or standby power strategy for selected life-safety loads when required.
ELE.ESP.LSL|MEC.SMK.EXH.SCF|requires|supports_life_safety_function|dependency|safety-critical;operational|0.82|0.76|electrical;mechanical;fire_safety|design;commissioning;operation|SRC-NFPA-CODES;SRC-ICC-IBC-IPC-IFC-IECC-IEBC|Smoke-control fan power continuity can be life-safety-critical where emergency smoke-control operation is required.
ELE.MON.SUB|PER.ENE.OEM|requires|measures_energy_use|functional_service|performance;operational|0.82|0.78|electrical;sustainability;operations|design;operation|SRC-WBDG-SYSTEMS-INTEGRATION;SRC-BRICK-SCHEMA|Electrical submetering provides measured energy data used to manage operational energy performance.
PER.ENE.OEM|DIG.DTA.SDS.TRD|requires|feeds_analytics|information_management|informational;performance|0.78|0.76|digital_delivery;operations;sustainability|operation|SRC-BRICK-SCHEMA;SRC-PROJECT-HAYSTACK|Energy meter readings become trend data used for performance tracking, fault detection, and analytics.
PLS.PFE.FIS.PFX|PLS.PWS.WSM.CWS|requires|supplied_by_potable_cold_water|system_flow|functional;public-health|0.88|0.84|plumbing|design;construction;operation|SRC-ICC-IBC-IPC-IFC-IECC-IEBC;SRC-IAPMO-UPC-METADATA;SRC-WHO-WASH-SANITATION-SAFETY|Plumbing fixtures commonly require potable cold-water supply protected by distribution and backflow boundaries.
PLS.PFE.FIS.PFX|PLS.HOT.WHE.DWH|requires|supplied_by_domestic_hot_water|system_flow|functional;public-health|0.78|0.78|plumbing;mechanical|design;construction;operation|SRC-ICC-IBC-IPC-IFC-IECC-IEBC;SRC-IAPMO-UPC-METADATA|Fixtures needing hot water depend on domestic water-heating equipment and distribution strategy.
PLS.PFE.FIS.PFX|PLS.SDS.DRS.SDR|requires|drains_to|system_flow|functional;public-health|0.90|0.86|plumbing|design;construction;operation|SRC-ICC-IBC-IPC-IFC-IECC-IEBC;SRC-IAPMO-UPC-METADATA|Fixtures that discharge waste require sanitary drainage paths to convey wastewater away from occupied spaces.
PLS.PFE.FIS.PFX|PLS.SAN.TRA.FXT|requires|requires_trap|dependency|public-health;functional|0.88|0.84|plumbing|design;construction;operation|SRC-ICC-IBC-IPC-IFC-IECC-IEBC;SRC-IAPMO-UPC-METADATA|A fixture trap protects the indoor environment from drainage system gases while allowing fixture drainage.
PLS.SAN.TRA.FXT|PLS.VES.VPS.VST|requires|requires_vent|dependency|public-health;functional|0.86|0.84|plumbing|design;construction;operation|SRC-ICC-IBC-IPC-IFC-IECC-IEBC;SRC-IAPMO-UPC-METADATA|Venting supports trap seal protection and drainage pressure balance in typical sanitary drainage systems.
PLS.PWS.BAP.BFP|PLS.PWS.WSM.CWS|requires|protected_by_backflow_prevention|functional_service|public-health;safety-critical|0.90|0.84|plumbing;operations|design;construction;operation;maintenance|SRC-ICC-IBC-IPC-IFC-IECC-IEBC;SRC-IAPMO-UPC-METADATA;SRC-WHO-WASH-SANITATION-SAFETY|Backflow prevention protects potable water from contamination at defined connection and hazard boundaries.
PLS.HOT.WHE.DWH|PLS.PWS.WSM.CWS|requires|heats_potable_water_from|system_flow|functional;public-health|0.82|0.78|plumbing;mechanical|design;operation|SRC-ICC-IBC-IPC-IFC-IECC-IEBC;SRC-ASHRAE-188-LEGIONELLA|Domestic water heaters use potable supply and create hot-water distribution with water-quality and safety implications.
PLS.PWS.WSM.WQP|PLS.HOT.WHE.DWH|requires|water_quality_risk_managed_for|risk_failure|public-health;operational|0.78|0.78|plumbing;operations|commissioning;operation;maintenance|SRC-ASHRAE-188-LEGIONELLA;SRC-CDC-LEGIONELLA-BUILDING-WATER;SRC-WHO-WASH-SANITATION-SAFETY|Building water programs consider hot-water generation, storage, distribution, temperature, stagnation, and maintenance risks.
PLS.PWS.WSM.WQP|PLS.PWS.WSM.CWS|requires|water_quality_risk_managed_for|risk_failure|public-health;operational|0.76|0.78|plumbing;operations|commissioning;operation;maintenance|SRC-ASHRAE-188-LEGIONELLA;SRC-CDC-LEGIONELLA-BUILDING-WATER;SRC-WHO-WASH-SANITATION-SAFETY|Potable cold-water distribution can require monitoring and flushing when stagnation, temperature, or disinfectant conditions create risk.
PLS.SDS.DRS.CDN|MEC.AHD.AHU|requires|drains_condensate_from|system_flow|functional;operational|0.76|0.74|mechanical;plumbing|design;construction;operation;maintenance|SRC-WBDG-SYSTEMS-INTEGRATION;SRC-ASHRAE-62-1-90-1-55-CX|Cooling coils and dehumidification components can produce condensate requiring drainage, trapping, slope, and maintenance coordination.
PLS.VES.VPS.VST|FLS.CMP.PEN.PIP|constrains|penetrates_fire_rated_assembly|physical_composition|physical;safety-critical|0.70|0.72|plumbing;fire_safety;architecture|design;construction;inspection|SRC-ICC-IBC-IPC-IFC-IECC-IEBC;SRC-IAPMO-UPC-METADATA|Vent stacks and drainage risers often pass through floors, shafts, or roofs and require penetration coordination where rated construction is involved.
PLS.PFE.FIS.PFX|SUS.WAC.WEF|constrains|impacts_water_use|performance_sustainability|sustainability;performance|0.76|0.74|plumbing;sustainability|planning;design;operation|SRC-WBDG-SYSTEMS-INTEGRATION;SRC-WHO-WASH-SANITATION-SAFETY|Fixture selection and operation affect potable water consumption while needing to preserve hygiene and user function.
ARC.BLD.SRV.MPR|MEC.PLT|part_of|contains_mechanical_plant|physical_composition|physical;functional|0.84|0.80|architecture;mechanical|planning;design;construction;operation|SRC-WBDG-SYSTEMS-INTEGRATION|A mechanical plant room is planned around contained plant, access, services, support, and maintainability.
ARC.BLD.SRV.MPR|MEC.AHD.AHU|part_of|contains_equipment|physical_composition|physical;functional|0.72|0.72|architecture;mechanical|planning;design;operation|SRC-WBDG-SYSTEMS-INTEGRATION|Some AHUs are located in plant rooms, where room planning coordinates equipment access, services, and replacement.
ARC.BLD.SRV.MPR|MEC.PLT.CHL|part_of|contains_equipment|physical_composition|physical;functional|0.72|0.72|architecture;mechanical|planning;design;operation|SRC-WBDG-SYSTEMS-INTEGRATION|Chillers may be located in plant rooms or plant areas and require support, ventilation, power, access, and service clearances.
MEC.PLT.CHL|STR.NSC.EQL|requires|imposes_equipment_load|dependency|physical;safety-critical|0.84|0.78|mechanical;structural|planning;design;construction|SRC-ASCE-SEI-7;SRC-WBDG-SYSTEMS-INTEGRATION|Heavy mechanical equipment imposes loads that must be coordinated with structural support and replacement scenarios.
MEC.AHD.AHU|STR.NSC.VIR|requires|requires_vibration_isolation|dependency|physical;performance|0.70|0.72|mechanical;structural;architecture|design;construction;operation|SRC-WBDG-SYSTEMS-INTEGRATION;SRC-SMACNA-SEISMIC-RESTRAINT|Rotating equipment can require vibration isolation or support coordination to reduce transmitted vibration and noise.
MEC.PLT.PMP|STR.NSC.VIR|requires|requires_vibration_isolation|dependency|physical;performance|0.72|0.72|mechanical;structural|design;construction;operation|SRC-WBDG-SYSTEMS-INTEGRATION;SRC-SMACNA-SEISMIC-RESTRAINT|Pump vibration and alignment can require support and isolation coordination.
MEC.PLT.PMP|STR.NSC.SBR|requires|requires_seismic_restraint|dependency|physical;safety-critical|0.68|0.68|mechanical;structural|design;construction;inspection|SRC-ASCE-SEI-7;SRC-SMACNA-SEISMIC-RESTRAINT|In seismic contexts, mechanical equipment may require nonstructural restraint coordinated with the support structure.
ARC.BLD.SRV.MPR|ARC.BLD.SRV.MAZ|requires|requires_access_for|dependency|operational;physical|0.86|0.82|architecture;mechanical;operations|planning;design;operation;maintenance|SRC-WBDG-SYSTEMS-INTEGRATION;SRC-NIBS-WBDG-COMMISSIONING|Plant rooms require maintenance access zones for service, inspection, filter changes, valve operation, and safe operations.
ARC.BLD.SRV.MPR|ARC.BLD.SRV.RPT|requires|requires_replacement_path|lifecycle_process|operational;physical|0.78|0.76|architecture;mechanical;operations|planning;design;operation;maintenance|SRC-WBDG-SYSTEMS-INTEGRATION;SRC-NIBS-WBDG-COMMISSIONING|Major plant should be planned with a replacement route so lifecycle renewal does not require avoidable destructive work.
ARC.BLD.SRV.MPR|PLS.SDS.DRS.CDN|requires|requires_drainage|dependency|functional;operational|0.72|0.74|architecture;mechanical;plumbing|design;construction;operation|SRC-WBDG-SYSTEMS-INTEGRATION;SRC-ICC-IBC-IPC-IFC-IECC-IEBC|Plant rooms commonly require floor, equipment, condensate, or relief drainage depending on contained equipment and strategy.
ARC.BLD.SRV.MPR|ELE.PDS.BRC.CIR|requires|requires_power_supply|dependency|functional;operational|0.80|0.78|architecture;electrical;mechanical|design;construction;operation|SRC-WBDG-SYSTEMS-INTEGRATION;SRC-NFPA-70-101-13-72-14-20|Plant rooms need coordinated power for equipment, controls, lighting, receptacles, and safe maintenance.
ARC.BLD.SRV.MPR|FLS.CMP.FBA|requires|requires_fire_separation_review|regulatory_authority|safety-critical;regulatory|0.72|0.72|architecture;fire_safety;mechanical|planning;design;construction|SRC-ICC-IBC-IPC-IFC-IECC-IEBC;SRC-WBDG-SYSTEMS-INTEGRATION|Plant rooms may require fire-separation review depending on equipment hazards, occupancy, fuel, power, and adopted-code context.
ARC.BLD.SRV.MPR|MEC.IEQ.VER|requires|requires_room_ventilation|functional_service|functional;performance|0.70|0.70|architecture;mechanical|design;operation|SRC-ASHRAE-62-1-90-1-55-CX;SRC-WBDG-SYSTEMS-INTEGRATION|Mechanical plant rooms often require ventilation, heat rejection, or combustion-air coordination depending on equipment.
OPS.AST.REG.MAR|MEC.AHD.AHU|requires|documents_maintainable_asset|information_management|informational;operational|0.84|0.82|operations;mechanical;digital_delivery|handover;operation;maintenance|SRC-BRICK-SCHEMA;SRC-PROJECT-HAYSTACK;SRC-WBDG-SYSTEMS-INTEGRATION|AHUs are maintainable assets that benefit from asset-register identity, O&M links, and maintenance planning.
OPS.AST.REG.MAR|FLS.FPR.FPU.PMP|requires|documents_maintainable_asset|information_management|informational;operational;safety-critical|0.88|0.84|operations;fire_safety;digital_delivery|handover;operation;maintenance|SRC-NFPA-4-25-110-ITM-EPSS;SRC-WBDG-SYSTEMS-INTEGRATION|Fire pumps are maintainable life-safety assets requiring identity, inspection, testing, maintenance, and handover data.
OPS.AST.REG.MAR|PLS.HOT.WHE.DWH|requires|documents_maintainable_asset|information_management|informational;operational;public-health|0.80|0.78|operations;plumbing;digital_delivery|handover;operation;maintenance|SRC-ASHRAE-188-LEGIONELLA;SRC-WBDG-SYSTEMS-INTEGRATION|Domestic water-heating equipment requires asset records for maintenance, water-quality management, warranty, and replacement planning.
OPS.PRM.MAS.PMS|OPS.AST.REG.MAR|requires|maintained_by|lifecycle_process|operational;informational|0.82|0.80|operations|operation;maintenance|SRC-WBDG-SYSTEMS-INTEGRATION;SRC-NIBS-WBDG-COMMISSIONING|Preventive maintenance schedules link planned tasks to maintainable asset records.
OPS.PRM.MAS.PMS|FLS.FPR.FPU.PMP|requires|inspected_and_tested_by|lifecycle_process|safety-critical;operational|0.88|0.82|operations;fire_safety|operation;maintenance|SRC-NFPA-4-25-110-ITM-EPSS;SRC-NFPA-70-101-13-72-14-20|Fire pump readiness is sustained by recurring inspection, testing, and maintenance activities.
MEC.CTL.SNS.TMS|DIG.DTA.SDS.TRD|requires|feeds_analytics|information_management|informational;operational;performance|0.78|0.78|mechanical;smart_systems;operations|commissioning;operation|SRC-BRICK-SCHEMA;SRC-PROJECT-HAYSTACK|Temperature sensor histories can feed commissioning review, trend analysis, comfort diagnostics, and fault detection.
MEC.CTL.SNS.COS|DIG.DTA.SDS.TRD|requires|feeds_analytics|information_management|informational;operational;performance|0.74|0.74|mechanical;smart_systems;operations|commissioning;operation|SRC-BRICK-SCHEMA;SRC-PROJECT-HAYSTACK|CO2 sensor trend data can support ventilation diagnostics where the control strategy uses it.
SMS.BUA.ATL.ALM|OPS.FAC.WOR.CWO|requires|triggers_work_order|lifecycle_process|operational;informational|0.72|0.72|operations;smart_systems|operation;maintenance|SRC-BRICK-SCHEMA;SRC-PROJECT-HAYSTACK;SRC-WBDG-SYSTEMS-INTEGRATION|A prioritized BMS alarm can trigger a corrective work order or investigation depending on operations workflow.
ELE.CTL.BMS.NET|SMS.BUA.ATL.ALM|requires|reports_alarm_to|information_management|informational;operational|0.78|0.76|electrical;smart_systems;operations|commissioning;operation|SRC-BRICK-SCHEMA;SRC-PROJECT-HAYSTACK|The BMS network reports equipment, sensor, or control alarms to supervisory logs and operator workflows.
DIG.DTA.AIR.EIR|OPS.AST.REG.MAR|requires|has_information_requirement|information_management|informational;operational|0.82|0.80|digital_delivery;operations|design;construction;handover;operation|SRC-BUILDINGSMART-IDS-1-0;SRC-BSI-IFC-ISO-16739-1;SRC-WBDG-SYSTEMS-INTEGRATION|Exchange information requirements define asset data needed for reliable handover and operations.
DIG.IDS|DIG.DTA.AIR.EIR|requires|validated_by_information_delivery_specification|information_management|informational|0.76|0.78|digital_delivery|design;construction;handover|SRC-BUILDINGSMART-IDS-1-0;SRC-BSI-IFC-ISO-16739-1|IDS can be used to formalize and check IFC information requirements at exchange points.
DIG.EXC.IFC|OPS.AST.REG.MAR|requires|exchanged_using_model_data|information_management|informational|0.68|0.72|digital_delivery;operations|design;construction;handover|SRC-BSI-IFC-ISO-16739-1;SRC-BUILDINGSMART-IDS-1-0|IFC can carry model and asset data for exchange, but it is not the physical asset or the whole operational KG.
CON.COM.HND|OPS.AST.REG.MAR|requires|generates_asset_record|lifecycle_process|informational;operational|0.84|0.82|commissioning;operations;digital_delivery|construction;handover;operation|SRC-ASHRAE-IES-202-CX;SRC-NIBS-WBDG-COMMISSIONING;SRC-WBDG-SYSTEMS-INTEGRATION|Handover should deliver asset records and O&M information needed for operations and maintenance.
CON.COM.FTE|MEC.AHD.AHU|requires|verified_by_commissioning|lifecycle_process|performance;operational|0.82|0.82|commissioning;mechanical|commissioning;operation|SRC-ASHRAE-IES-202-CX;SRC-NIBS-WBDG-COMMISSIONING|Functional testing verifies AHU operation, controls, safeties, and interfaces against the commissioning plan and OPR.
CON.COM.FTE|MEC.MCC.TAB|requires|depends_on_testing_adjusting_balancing|lifecycle_process|performance;operational|0.78|0.78|commissioning;mechanical|commissioning|SRC-ASHRAE-IES-202-CX;SRC-NIBS-WBDG-COMMISSIONING|Functional performance checks for air systems depend on prerequisite balancing where flows are part of acceptance.
MEC.AHD.AHU|SUS.ECS.ECA|constrains|has_replacement_embodied_carbon_impact|performance_sustainability|sustainability;lifecycle|0.58|0.66|mechanical;sustainability|planning;design;operation;reuse|SRC-WBDG-SYSTEMS-INTEGRATION|Major mechanical equipment replacement, refrigerants, and product choices can affect lifecycle carbon; quantification needs project LCA data.
MAT.ASM.FRW|SUS.ECS.ECA|constrains|impacts_embodied_carbon|performance_sustainability|sustainability;physical|0.62|0.68|architecture;fire_safety;sustainability|planning;design;construction;reuse|SRC-WBDG-SYSTEMS-INTEGRATION|Fire-rated assembly material choices can influence embodied carbon while maintaining fire-resistance and acoustic objectives.
ARC.ECD.DLG|PER.IEQ.IAQ|constrains|tradeoff_with_iaq_and_loads|performance_sustainability|performance;sustainability|0.56|0.64|architecture;mechanical;sustainability|planning;design|SRC-WBDG-SYSTEMS-INTEGRATION;SRC-ASHRAE-62-1-90-1-55-CX|Daylighting decisions interact with envelope heat gains, glare, ventilation, and occupant comfort.
PLS.PWS.WSM.WQP|SUS.WAC.WEF|constrains|tradeoff_with_water_efficiency|performance_sustainability|public-health;sustainability|0.62|0.70|plumbing;operations;sustainability|design;operation;maintenance|SRC-ASHRAE-188-LEGIONELLA;SRC-CDC-LEGIONELLA-BUILDING-WATER;SRC-WHO-WASH-SANITATION-SAFETY|Low-flow strategies must be coordinated with stagnation, temperature, disinfectant, and maintenance risks in building water systems.
ARC.BLD.SRV.CSV|MEC.AHD.DUD.SAD|constrains|constrains_service_routing_clearance|spatial_topological|physical;functional|0.74|0.76|architecture;mechanical;fire_safety|planning;design;construction|SRC-WBDG-SYSTEMS-INTEGRATION;SRC-ICC-IBC-IPC-IFC-IECC-IEBC|Ceiling service void depth and access constrain duct routing, fire/smoke separation, acoustic treatment, and maintenance coordination.
FLS.FPR.FPU.JKY|FLS.FPR.FPU|part_of|part_of_fire_pump_system|physical_composition|physical;safety-critical|0.76|0.74|fire_safety;plumbing|design;construction;operation;maintenance|SRC-NFPA-70-101-13-72-14-20;SRC-NFPA-CODES|A jockey pump is a design-dependent pressure-maintenance component within some fire-pump system arrangements.
FIG.WRK.BUI.MAX|FIG.ARD.CAA.HAD|has_facet|designed_by|information_management|informational;historical|0.86|0.82|architecture;cultural_history|planning;design;operation|SRC-PRITZKER-LAUREATES-OFFICIAL;SRC-WIKIDATA-CC0-AEC-IDENTIFIERS|The building node is explicitly connected back to its canonical architect so work-to-designer traversal is available.
FIG.WRK.BUI.CHL|FIG.ARD.CAA.AND|has_facet|designed_by|information_management|informational;historical|0.86|0.82|architecture;cultural_history|planning;design;operation|SRC-PRITZKER-LAUREATES-OFFICIAL;SRC-WIKIDATA-CC0-AEC-IDENTIFIERS|The building node is explicitly connected back to its canonical architect to support work-to-architect traversal.
FIG.WRK.BUI.SYD|FIG.ARD.CAA.UTZ|has_facet|designed_by|information_management|informational;historical|0.84|0.80|architecture;cultural_history|planning;design;operation|SRC-PRITZKER-LAUREATES-OFFICIAL;SRC-WIKIDATA-CC0-AEC-IDENTIFIERS|The Sydney Opera House work node gains a direct link to the canonical architect node for inverse traversal.
FIG.WRK.BUI.SYD|FIG.ETS.STE.ARU|has_facet|engineered_by|information_management|informational;historical|0.78|0.76|structural;architecture;cultural_history|planning;design;construction|SRC-WIKIDATA-CC0-AEC-IDENTIFIERS|The work node is linked to the canonical engineering figure to support architect-engineer-building traversal.
FIG.WRK.BUI.CHS|FIG.ARD.CAA.LOC|has_facet|designed_by|information_management|informational;historical|0.84|0.80|architecture;cultural_history|planning;design;operation|SRC-NCCA-NATIONAL-ARTISTS-ARCHITECTURE;SRC-WIKIDATA-CC0-AEC-IDENTIFIERS|The building node is explicitly connected to the canonical architect node so landmark-building queries can traverse to the designer.
FIG.WRK.BUI.FEU|FIG.ARD.CAA.ANT|has_facet|designed_by|information_management|informational;historical|0.84|0.80|architecture;cultural_history|planning;design;operation|SRC-NCCA-NATIONAL-ARTISTS-ARCHITECTURE;SRC-WIKIDATA-CC0-AEC-IDENTIFIERS|The building node is explicitly connected to the canonical architect node for work-first graph traversal.
""".strip()

RESOLVER_CASES = [
    ("RES-DOMAIN-CLUSTER-001", "VTN-DOM-0012678", "From an occupied space, traverse ventilation, HVAC zoning, controls, energy, comfort, egress, and plumbing implications.", ["VTN-DOM-0012678", "VTN-DOM-0000546", "VTN-DOM-0003104", "VTN-DOM-0012693", "VTN-DOM-0000438", "VTN-DOM-0003243"], ["architecture", "mechanical", "fire_safety", "plumbing", "electrical", "sustainability"], ["SRC-ASHRAE-62-1-90-1-55-CX", "SRC-ICC-IBC-IPC-IFC-IECC-IEBC", "SRC-WBDG-SYSTEMS-INTEGRATION"], "Composed relationships connect occupied-space concept to ventilation, HVAC, egress, plumbing, lighting, and performance implications."),
    ("RES-DOMAIN-CLUSTER-002", "VTN-DOM-0003075", "From an AHU, find supply air path, power, condensate drainage, controls, maintenance access, commissioning, and fire-smoke interfaces.", ["VTN-DOM-0003075", "VTN-DOM-0012689", "VTN-DOM-0012701", "VTN-DOM-0012711", "VTN-DOM-0012727"], ["mechanical", "electrical", "plumbing", "fire_safety", "operations", "commissioning"], ["SRC-ASHRAE-62-1-90-1-55-CX", "SRC-WBDG-SYSTEMS-INTEGRATION", "SRC-BRICK-SCHEMA"], "Composed relationships expose AHU system-flow, controls, power, drainage, commissioning, and operations dependencies."),
    ("RES-DOMAIN-CLUSTER-003", "VTN-DOM-0012315", "From a fire-rated wall, find duct, pipe, and cable penetration protection concepts plus inspection and egress implications.", ["VTN-DOM-0012315", "VTN-DOM-0012713", "VTN-DOM-0012714", "VTN-DOM-0012715", "VTN-DOM-0012716", "VTN-DOM-0012717"], ["architecture", "fire_safety", "mechanical", "plumbing", "electrical", "construction"], ["SRC-ICC-IBC-IPC-IFC-IECC-IEBC", "SRC-NFPA-70-101-13-72-14-20"], "Composed relationships connect rated assemblies to MEP penetrations, firestop systems, dampers, inspection, and egress support."),
    ("RES-DOMAIN-CLUSTER-004", "VTN-DOM-0012722", "From a fire pump, find sprinkler and standpipe demand, controller, emergency power, alarm monitoring, testing, and life-safety risk dependencies.", ["VTN-DOM-0012722", "VTN-DOM-0012720", "VTN-DOM-0000431", "VTN-DOM-0012723", "VTN-DOM-0012702", "VTN-DOM-0000490"], ["fire_safety", "electrical", "plumbing", "commissioning", "operations"], ["SRC-NFPA-70-101-13-72-14-20", "SRC-NFPA-4-25-110-ITM-EPSS"], "Composed relationships expose fire-pump water, power, controller, alarm, testing, inspection, and life-safety dependencies."),
    ("RES-DOMAIN-CLUSTER-005", "VTN-DOM-0012706", "From a plumbing fixture, find potable cold water, domestic hot water, sanitary drainage, trap, vent, backflow, and water-quality implications.", ["VTN-DOM-0012706", "VTN-DOM-0012704", "VTN-DOM-0012705", "VTN-DOM-0012707", "VTN-DOM-0012708", "VTN-DOM-0012709"], ["plumbing", "operations", "sustainability", "architecture"], ["SRC-ICC-IBC-IPC-IFC-IECC-IEBC", "SRC-IAPMO-UPC-METADATA", "SRC-CDC-LEGIONELLA-BUILDING-WATER"], "Composed relationships expose fixture supply, drainage, venting, backflow, water quality, public-health, and water-efficiency dependencies."),
    ("RES-DOMAIN-CLUSTER-006", "VTN-DOM-0012679", "From a mechanical plant room, find structural loads, vibration, drainage, power, ventilation, fire separation, access, and replacement path dependencies.", ["VTN-DOM-0012679", "VTN-DOM-0012685", "VTN-DOM-0012682", "VTN-DOM-0012683", "VTN-DOM-0012711", "VTN-DOM-0000439"], ["architecture", "mechanical", "structural", "electrical", "plumbing", "fire_safety", "operations"], ["SRC-WBDG-SYSTEMS-INTEGRATION", "SRC-ASCE-SEI-7", "SRC-SMACNA-SEISMIC-RESTRAINT"], "Composed relationships make the plant room an interdisciplinary coordination node rather than an isolated architectural room."),
    ("RES-DOMAIN-CLUSTER-007", "VTN-DOM-0012578", "From a canonical building work, traverse to its architect or engineer rather than relying only on person-to-work links.", ["VTN-DOM-0012578", "VTN-DOM-0012565", "VTN-DOM-0012459"], ["architecture", "structural", "cultural_history"], ["SRC-PRITZKER-LAUREATES-OFFICIAL", "SRC-WIKIDATA-CC0-AEC-IDENTIFIERS"], "Compatible composed inverse relationships support work-first traversal between canonical buildings, architects, and engineers."),
]


def enrich_backbone_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """Return an enriched copy of the admitted Backbone payload."""
    enriched = deepcopy(payload)
    records = _dict_list(enriched.setdefault("records", []))
    relationships = _dict_list(enriched.setdefault("relationships", []))
    path_to_record = {str(row.get("path_code") or ""): row for row in records if row.get("path_code")}

    for spec in _node_specs():
        existing = path_to_record.get(spec["path_code"])
        if existing is None:
            node = _node_from_spec(spec)
            records.append(node)
            path_to_record[node["path_code"]] = node
        else:
            _merge_node_metadata(existing, spec)

    existing_keys = {_relationship_key(row) for row in relationships}
    for spec in _node_specs():
        node = path_to_record[spec["path_code"]]
        parent_path = str(node.get("parent_path_code") or "")
        if not parent_path:
            continue
        parent = path_to_record.get(parent_path)
        if parent is None:
            raise ValueError(f"missing parent path for {spec['path_code']}: {parent_path}")
        hierarchy = _relationship_row(
            from_id=str(parent["id"]),
            to_id=str(node["id"]),
            predicate="broader_than",
            relation_type="taxonomy_parent_of",
            relation_category="taxonomy",
            relation_nature=["informational"],
            weight=1.0,
            confidence_score=0.96,
            discipline=_disciplines_from_path(spec["path_code"]),
            lifecycle_phase=["planning", "design"],
            source_family_ids=_sources_for_node(spec),
            rationale=f"{node['label']} is admitted as a narrower Backbone concept under {parent['label']} for clustered AEC-MEPFS reasoning.",
            generation_method=HIERARCHY_GENERATION_METHOD,
        )
        if _relationship_key(hierarchy) not in existing_keys:
            relationships.append(hierarchy)
            existing_keys.add(_relationship_key(hierarchy))

    path_to_record = {str(row.get("path_code") or ""): row for row in records if row.get("path_code")}
    for spec in _edge_specs():
        from_record = path_to_record.get(spec["from_path"])
        to_record = path_to_record.get(spec["to_path"])
        if from_record is None or to_record is None:
            missing = spec["from_path"] if from_record is None else spec["to_path"]
            raise ValueError(f"relationship spec references missing path_code: {missing}")
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
            "edition_version_effective_date": f"public metadata currentness checked {ACCESS_DATE}; adopted edition or release may vary",
            "official_url": url,
            "source_rights_class": rights_class,
            "clearance_state": "metadata_crosswalk_planned" if rights_class == "open-reference" else "planning_reference_only",
            "intended_vitruvius_use": intended_use,
            "steward_owner": OWNER,
            "declared_use_boundary": "No source text, tables, figures, images, clauses, or protected payloads ingested; source content reuse remains blocked.",
            "currentness_check_date": ACCESS_DATE,
            "update_cadence": "before source admission or ontology mapping changes",
            "blocking_notes": "Use as source-family metadata only; local AHJ, project brief, and source-rights review control any stronger claim.",
        }
        if source_id not in by_id:
            rows.append(row)
        else:
            for key, value in row.items():
                by_id[source_id].setdefault(key, value)
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
    return {
        "nodes_before": len(before_records),
        "nodes_after": len(after_records),
        "relationships_before": len(before_relationships),
        "relationships_after": len(after_relationships),
        "new_node_count": len(after_record_ids - before_record_ids),
        "new_relationship_count": len(after_rel_keys - before_rel_keys),
        "domain_cluster_relationship_count": len(enriched_relations),
        "domain_cluster_hierarchy_relationship_count": len(hierarchy_relations),
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
        "write_applied": write,
        "boundaries": {
            "file_backed_only": True,
            "live_neo4j_writes": False,
            "kg_rebuild": False,
            "api_explorer_cutover": False,
            "protected_content_ingest": False,
            "canonical_content_admission": False,
        },
        "paths": {
            "backbone_fixture": _relative_to_root(backbone_file, root),
            "source_rights_registry": _relative_to_root(source_file, root),
            "readiness_fixture": _relative_to_root(readiness_file, root),
            "report": _relative_to_root(report_file, root),
        },
        "deltas": {
            "backbone": summarize_delta(before_backbone, after_backbone),
            "source_rights_registry": {
                "source_rows_before": len(_dict_list(before_sources.get("source_rights_registry"))),
                "source_rows_after": len(_dict_list(after_sources.get("source_rights_registry"))),
                "source_rows_added": len({row[0] for row in SOURCE_ROWS} - old_sources),
            },
            "readiness_fixture": {
                "resolver_golden_cases_before": len(_dict_list(before_readiness.get("resolver_golden_cases"))),
                "resolver_golden_cases_after": len(_dict_list(after_readiness.get("resolver_golden_cases"))),
                "resolver_golden_cases_added": len({row[0] for row in RESOLVER_CASES} - old_cases),
            },
        },
        "clusters": sorted({cluster for spec in _node_specs() for cluster in spec["clusters"]}),
        "source_family_ids_used": sorted(_source_family_ids_used()),
        "assumptions": [
            "Source-family references are metadata/provenance anchors, not admitted protected source content.",
            "ASHRAE, NFPA, ICC, IAPMO, ASCE, SMACNA, CDC, WBDG, buildingSMART, Brick, Haystack, and BOT references are jurisdiction- or use-context sensitive.",
            "Existing governed predicate vocabulary is preserved; relation_type metadata records the more specific mechanism without a schema bump.",
            "BIM and openBIM metadata help organize information but do not replace installed assets, operations records, or domain reasoning.",
        ],
    }
    _write_json(report_file, report)
    return report


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Apply bounded AEC-MEPFS domain-cluster enrichment to file-backed fixtures.")
    parser.add_argument("--backbone", default=str(DEFAULT_BACKBONE_PATH))
    parser.add_argument("--source-rights", default=str(DEFAULT_SOURCE_RIGHTS_PATH))
    parser.add_argument("--readiness-fixture", default=str(DEFAULT_READINESS_FIXTURE_PATH))
    parser.add_argument("--repo-root", default=None)
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--output", default=None)
    parser.add_argument("--check", action="store_true", help="Write report only; do not mutate fixtures.")
    args = parser.parse_args(argv)
    try:
        report = apply_enrichment(
            backbone_path=args.backbone,
            source_rights_path=args.source_rights,
            readiness_fixture_path=args.readiness_fixture,
            repo_root=args.repo_root,
            run_id=args.run_id,
            output_path=args.output,
            write=not args.check,
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
        specs.append(
            {
                "id": node_id,
                "path_code": path_code,
                "label": label,
                "definition": definition,
                "aliases": _split_semicolon(aliases),
                "clusters": _split_semicolon(clusters),
            }
        )
    return specs


def _edge_specs() -> list[dict[str, Any]]:
    specs: list[dict[str, Any]] = []
    for line in EDGE_ROWS.splitlines():
        parts = line.split("|", 11)
        if len(parts) != 12:
            raise ValueError(f"invalid edge row: {line}")
        from_path, to_path, predicate, relation_type, category, nature, weight, confidence, discipline, lifecycle, sources, rationale = parts
        specs.append(
            {
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
            }
        )
    return specs


def _resolver_cases() -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    for case_id, concept_id, text, refs, disciplines, sources, rationale in RESOLVER_CASES:
        cases.append(
            {
                "case_id": case_id,
                "effective_date": ACCESS_DATE,
                "expected_confidence": "deterministic",
                "expected_node_refs": [
                    {"node_id": node_id, "role": "domain_cluster_trace_node"} for node_id in refs
                ],
                "expected_result_type": "composed",
                "fallback_reason": "domain_cluster_relationship_trace",
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
                "trace_safe_rationale": "Reports canonical IDs and paraphrased relationship rationales only; no protected source text is exposed.",
            }
        )
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
        "scope_note": "Domain concept added for cross-discipline AEC-MEPFS reasoning; project-specific values require local validation.",
        "example_concepts": [],
        "path_code": path_code,
        "level": len(path_code.split(".")),
        "parent_path_code": ".".join(path_code.split(".")[:-1]) if "." in path_code else None,
        "owner": OWNER,
        "steward": OWNER,
        "release_version": RELEASE_VERSION,
        "generation_method": GENERATION_METHOD,
        "semantic_overlay_category": "aec_mepfs_domain_cluster_node",
        "source_family_ids": _sources_for_node(spec),
        "provenance_note": PROVENANCE_NOTE,
        "domain_clusters": spec["clusters"],
    }


def _merge_node_metadata(existing: dict[str, Any], spec: dict[str, Any]) -> None:
    aliases = list(dict.fromkeys([*_list_strings(existing.get("aliases")), *spec["aliases"]]))
    if aliases:
        existing["aliases"] = aliases
    clusters = list(dict.fromkeys([*_list_strings(existing.get("domain_clusters")), *spec["clusters"]]))
    if clusters:
        existing["domain_clusters"] = clusters
    existing.setdefault("source_family_ids", _sources_for_node(spec))
    existing.setdefault("provenance_note", PROVENANCE_NOTE)


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
        "semantic_overlay_category": "aec_mepfs_domain_cluster_interrelationship",
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
    }


def _merge_relationship_metadata(rows: list[dict[str, Any]], key: tuple[str, str, str], candidate: dict[str, Any]) -> None:
    metadata_fields = (
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
    )
    for row in rows:
        if _relationship_key(row) == key:
            for field in metadata_fields:
                if not row.get(field) and candidate.get(field) is not None:
                    row[field] = candidate[field]
            return


def _relationship_key(row: dict[str, Any]) -> tuple[str, str, str]:
    return (
        str(row.get("from_id") or ""),
        str(row.get("predicate") or row.get("edge_type") or ""),
        str(row.get("to_id") or ""),
    )


def _sources_for_node(spec: dict[str, Any]) -> list[str]:
    path = spec["path_code"]
    clusters = set(spec["clusters"])
    sources: set[str] = {"SRC-WBDG-SYSTEMS-INTEGRATION"}
    if path.startswith("MEC") or "occupancy_hvac_comfort" in clusters:
        sources.add("SRC-ASHRAE-62-1-90-1-55-CX")
    if path.startswith("ELE"):
        sources.add("SRC-NFPA-70-101-13-72-14-20")
    if path.startswith("PLS") or "plumbing_public_health" in clusters:
        sources.update({"SRC-ICC-IBC-IPC-IFC-IECC-IEBC", "SRC-IAPMO-UPC-METADATA"})
    if path.startswith("FLS") or "fire_penetration_coordination" in clusters:
        sources.update({"SRC-NFPA-70-101-13-72-14-20", "SRC-ICC-IBC-IPC-IFC-IECC-IEBC"})
    if path.startswith("STR"):
        sources.update({"SRC-ASCE-SEI-7", "SRC-SMACNA-SEISMIC-RESTRAINT"})
    if path.startswith(("OPS", "SMS", "DIG")):
        sources.update({"SRC-BRICK-SCHEMA", "SRC-PROJECT-HAYSTACK"})
    if "operations_handover" in clusters:
        sources.update({"SRC-BUILDINGSMART-IDS-1-0", "SRC-BSI-IFC-ISO-16739-1"})
    if path in {"PLS.PWS.WSM.WQP", "PLS.HOT.WHE.DWH"}:
        sources.update({"SRC-ASHRAE-188-LEGIONELLA", "SRC-CDC-LEGIONELLA-BUILDING-WATER"})
    return sorted(sources)


def _source_family_ids_used() -> set[str]:
    ids = {row[0] for row in SOURCE_ROWS}
    for spec in _node_specs():
        ids.update(_sources_for_node(spec))
    for spec in _edge_specs():
        ids.update(spec["source_family_ids"])
    for _, _, _, _, _, sources, _ in RESOLVER_CASES:
        ids.update(sources)
    return ids


def _disciplines_from_path(path_code: str) -> list[str]:
    root = path_code.split(".", 1)[0]
    return [{
        "ARC": "architecture",
        "STR": "structural",
        "MEC": "mechanical",
        "ELE": "electrical",
        "PLS": "plumbing",
        "FLS": "fire_safety",
        "OPS": "operations",
        "SMS": "smart_systems",
        "DIG": "digital_delivery",
        "PER": "performance",
        "SUS": "sustainability",
        "COM": "compliance",
        "FIG": "architecture",
    }.get(root, "aec")]


def _split_semicolon(value: str) -> list[str]:
    return [item.strip() for item in value.split(";") if item.strip()]


def _dict_list(value: Any) -> list[dict[str, Any]]:
    return [item for item in value if isinstance(item, dict)] if isinstance(value, list) else []


def _list_strings(value: Any) -> list[str]:
    return [str(item) for item in value if str(item).strip()] if isinstance(value, list) else []


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
    resolved.parent.mkdir(parents=True, exist_ok=True)
    return resolved


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
