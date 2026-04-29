from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

GENERATION_METHOD = (
    "steward_governed_cross_domain_overlay_enrichment_from_kimi_guided_public_"
    "aec_mepfs_coordination_commissioning_resilience_and_applicability_sources"
)
OWNER = "Philip Lewis"
RELEASE_VERSION = "0.6.0"
SCOPE_NOTE = (
    "Cross-domain AEC-MEPFS semantic overlay enrichment synthesized from Kimi-guided "
    "review, official public source-family metadata, and steward-authored coordination "
    "patterns; metadata only, no protected source payloads."
)

SOURCE_REFERENCES: list[dict[str, str]] = [
    {
        "source_id": "SRC-FEMA-E74-NONSTRUCTURAL",
        "source_family": "FEMA E-74 nonstructural earthquake damage reduction guidance",
        "publisher_authority": "FEMA",
        "official_url": "https://www.fema.gov/node/reducing-risks-non-structural-earthquake-damage",
        "intended_vitruvius_use": "metadata-only nonstructural seismic restraint, anchorage, equipment support, and operational continuity taxonomy context",
    },
    {
        "source_id": "SRC-SMACNA-SEISMIC-RESTRAINT",
        "source_family": "SMACNA seismic restraint and duct construction manual families",
        "publisher_authority": "SMACNA",
        "official_url": "https://www.smacna.org/resource/smacna-seismic-restraint-manual-4th-edition--45-day-public-review-; https://www.smacna.org/news/news-archive/article/2025/04/01/smacna--ansi-45-day-public-review",
        "intended_vitruvius_use": "metadata-only HVAC duct, piping, hanger, bracing, and seismic restraint taxonomy context",
    },
    {
        "source_id": "SRC-NECA-NEIS-ELECTRICAL",
        "source_family": "NECA National Electrical Installation Standards",
        "publisher_authority": "NECA",
        "official_url": "https://www.necanet.org/topics/codesandstandards/neis/the-standards",
        "intended_vitruvius_use": "metadata-only electrical installation, equipment support, temporary power, workmanship, and maintenance taxonomy context",
    },
    {
        "source_id": "SRC-ASHRAE-IES-202-CX",
        "source_family": "ASHRAE Guideline 0 and ASHRAE/IES Standard 202 commissioning process references",
        "publisher_authority": "ASHRAE / IES",
        "official_url": "https://www.ashrae.org/technical-resources/bookstore/commissioning; https://www.ashrae.org/news/esociety/updated-commissioning-guideline",
        "intended_vitruvius_use": "metadata-only commissioning, OPR, BOD, functional testing, systems manual, and handover taxonomy context",
    },
    {
        "source_id": "SRC-NFPA-4-25-110-ITM-EPSS",
        "source_family": "NFPA integrated testing, fire protection ITM, and emergency power standards",
        "publisher_authority": "NFPA",
        "official_url": "https://www.nfpa.org/codes-and-standards",
        "intended_vitruvius_use": "metadata-only integrated systems testing, fire protection inspection/testing/maintenance, and emergency power acceptance taxonomy context",
    },
    {
        "source_id": "SRC-ISO-22301-BCMS",
        "source_family": "ISO 22301 business continuity management systems",
        "publisher_authority": "ISO",
        "official_url": "https://www.iso.org/standard/75106.html",
        "intended_vitruvius_use": "metadata-only operational resilience, continuity objectives, recovery targets, and business continuity taxonomy context",
    },
    {
        "source_id": "SRC-ISO-IEC-27001-ISMS",
        "source_family": "ISO/IEC 27001 information security management systems",
        "publisher_authority": "ISO / IEC",
        "official_url": "https://www.iso.org/standard/27001",
        "intended_vitruvius_use": "metadata-only building-systems cybersecurity, information security management, and OT network governance taxonomy context",
    },
    {
        "source_id": "SRC-ISA-IEC-62443-IACS",
        "source_family": "ISA/IEC 62443 industrial automation and control systems cybersecurity",
        "publisher_authority": "ISA / IEC",
        "official_url": "https://www.isa.org/standards-and-publications/isa-standards/isa-iec-62443-series-of-standards; https://www.isa.org/connectivity-and-cybersecurity/standards",
        "intended_vitruvius_use": "metadata-only OT, BAS, controls cybersecurity, segmentation, and industrial-control-system lifecycle taxonomy context",
    },
    {
        "source_id": "SRC-ASCE-24-FLOOD-RESISTANT",
        "source_family": "ASCE 24 flood resistant design and construction",
        "publisher_authority": "ASCE",
        "official_url": "https://www.asce.org/publications-and-news/codes-and-standards/asce-sei-24-24/",
        "intended_vitruvius_use": "metadata-only flood hazard area, flood-resistant equipment placement, and critical facility resilience taxonomy context",
    },
    {
        "source_id": "SRC-NIBS-WBDG-COMMISSIONING",
        "source_family": "NIBS Whole Building Design Guide commissioning and facility handover resources",
        "publisher_authority": "National Institute of Building Sciences / WBDG",
        "official_url": "https://www.wbdg.org/building-commissioning; https://www.wbdg.org/building-commissioning/commissioning-documents/; https://www.wbdg.org/building-commissioning/roles-and-responsibilities-commissioning-process",
        "intended_vitruvius_use": "metadata-only commissioning documents, OPR, BOD, systems manual, training, and closeout taxonomy context",
    },
]

STANDARD_FAMILIES: list[dict[str, Any]] = [
    {"path_code": "COM.STD.ASC", "label": "ASCE Standards", "definition": "Metadata-only ASCE standards-family node for structural loads, seismic coordination, existing-building evaluation, and flood-resistant design crosswalks.", "aliases": ["ASCE", "ASCE standards", "civil and structural standards"], "source_ids": ["SRC-ASCE-SEISMIC-RESILIENCE", "SRC-ASCE-24-FLOOD-RESISTANT"], "children": [("LDN", "ASCE 7 Loads And Nonstructural Criteria", ["ASCE 7", "minimum design loads", "nonstructural component criteria"], "SRC-ASCE-SEISMIC-RESILIENCE"), ("FLD", "ASCE 24 Flood Resistant Design", ["ASCE 24", "flood resistant design", "flood design standard"], "SRC-ASCE-24-FLOOD-RESISTANT"), ("EXB", "ASCE 41 Existing Building Evaluation", ["ASCE 41", "existing building seismic evaluation", "seismic retrofit standard"], "SRC-ASCE-SEISMIC-RESILIENCE")]},
    {"path_code": "COM.STD.FEM", "label": "FEMA Mitigation Guidance", "definition": "Metadata-only FEMA source-family node for nonstructural earthquake damage reduction, seismic performance assessment, and public mitigation references.", "aliases": ["FEMA mitigation", "FEMA earthquake guidance", "FEMA resilience guidance"], "source_ids": ["SRC-FEMA-E74-NONSTRUCTURAL", "SRC-FEMA-P58-PUBLICATIONS"], "children": [("NSE", "FEMA E-74 Nonstructural Earthquake Damage Reduction", ["FEMA E-74", "nonstructural earthquake damage", "nonstructural mitigation"], "SRC-FEMA-E74-NONSTRUCTURAL"), ("SPA", "FEMA P-58 Seismic Performance Assessment", ["FEMA P-58", "seismic performance assessment", "performance-based earthquake assessment"], "SRC-FEMA-P58-PUBLICATIONS")]},
    {"path_code": "COM.STD.SMA", "label": "SMACNA Technical Manuals", "definition": "Metadata-only SMACNA standards-family node for HVAC duct construction, seismic restraint, hanger, support, and bracing references.", "aliases": ["SMACNA", "Sheet Metal and Air Conditioning Contractors National Association", "HVAC duct standards"], "source_ids": ["SRC-SMACNA-SEISMIC-RESTRAINT"], "children": [("SRM", "SMACNA Seismic Restraint Manual", ["SMACNA SRM", "seismic restraint manual", "mechanical seismic bracing"], "SRC-SMACNA-SEISMIC-RESTRAINT"), ("DCT", "SMACNA Duct Construction Standards", ["duct construction standards", "HVAC duct construction", "duct pressure class"], "SRC-SMACNA-SEISMIC-RESTRAINT")]},
    {"path_code": "COM.STD.NEI", "label": "NECA Installation Standards", "definition": "Metadata-only NECA NEIS standards-family node for electrical installation workmanship, temporary power, microgrids, hazardous locations, and maintenance references.", "aliases": ["NECA", "NEIS", "National Electrical Installation Standards"], "source_ids": ["SRC-NECA-NEIS-ELECTRICAL"], "children": [("NEI", "NECA National Electrical Installation Standards", ["NEIS", "NECA standards", "electrical workmanship standards"], "SRC-NECA-NEIS-ELECTRICAL"), ("TMP", "NECA Temporary Electric Power Standard", ["temporary electric power", "temporary power standard", "construction temporary power"], "SRC-NECA-NEIS-ELECTRICAL"), ("MIC", "NECA Microgrid Installation And Maintenance", ["microgrid installation", "microgrid maintenance", "NECA microgrids"], "SRC-NECA-NEIS-ELECTRICAL")]},
    {"path_code": "COM.STD.NIB", "label": "NIBS WBDG Commissioning Guidance", "definition": "Metadata-only NIBS/WBDG source-family node for commissioning process, roles, documents, OPR, BOD, and facility handover references.", "aliases": ["NIBS WBDG", "Whole Building Design Guide", "commissioning guidance"], "source_ids": ["SRC-NIBS-WBDG-COMMISSIONING"], "children": [("CXP", "WBDG Commissioning Process", ["building commissioning", "Cx process", "commissioning process"], "SRC-NIBS-WBDG-COMMISSIONING"), ("OPR", "Owner Project Requirements Guidance", ["OPR", "owner's project requirements", "owner project requirements"], "SRC-NIBS-WBDG-COMMISSIONING"), ("BOD", "Basis Of Design Guidance", ["BOD", "basis of design", "design basis"], "SRC-NIBS-WBDG-COMMISSIONING")]},
    {"path_code": "COM.STD.ISA", "label": "ISA IEC 62443 Cybersecurity Standards", "definition": "Metadata-only ISA/IEC 62443 standards-family node for industrial automation, building controls, OT cybersecurity, zones, conduits, and lifecycle security references.", "aliases": ["ISA/IEC 62443", "IEC 62443", "industrial cybersecurity standards"], "source_ids": ["SRC-ISA-IEC-62443-IACS"], "children": [("IAC", "ISA IEC 62443 IACS Cybersecurity", ["IACS cybersecurity", "OT security", "industrial automation control systems security"], "SRC-ISA-IEC-62443-IACS")]},
]

EXISTING_STANDARD_CHILDREN: list[tuple[str, str, str, list[str], str]] = [
    ("COM.STD.ASH", "CPS", "ASHRAE IES 202 Commissioning Process", ["ASHRAE/IES 202", "commissioning process standard", "building systems commissioning"], "SRC-ASHRAE-IES-202-CX"),
    ("COM.STD.ASH", "CXG", "ASHRAE Guideline 0 Commissioning Process", ["ASHRAE Guideline 0", "Cx guideline", "whole building commissioning"], "SRC-ASHRAE-IES-202-CX"),
    ("COM.STD.NFP", "IFT", "NFPA 4 Integrated Fire Protection And Life Safety Testing", ["NFPA 4", "integrated systems testing", "integrated fire protection testing"], "SRC-NFPA-4-25-110-ITM-EPSS"),
    ("COM.STD.NFP", "ITM", "NFPA 25 Water-Based Fire Protection ITM", ["NFPA 25", "inspection testing maintenance", "water-based fire protection ITM"], "SRC-NFPA-4-25-110-ITM-EPSS"),
    ("COM.STD.NFP", "EPS", "NFPA 110 Emergency And Standby Power Systems", ["NFPA 110", "EPSS", "emergency power supply systems"], "SRC-NFPA-4-25-110-ITM-EPSS"),
    ("COM.STD.ISO", "BCM", "ISO 22301 Business Continuity Management", ["ISO 22301", "BCMS", "business continuity management"], "SRC-ISO-22301-BCMS"),
    ("COM.STD.ISO", "ISM", "ISO IEC 27001 Information Security Management", ["ISO/IEC 27001", "ISMS", "information security management system"], "SRC-ISO-IEC-27001-ISMS"),
]

OVERLAY_PARENTS: list[dict[str, Any]] = [
    {"path_code": "COM.APP", "label": "Applicability Overlays", "parent": "COM", "definition": "Jurisdiction, code-adoption, facility-type, hazard, and lifecycle applicability concepts that constrain whether AEC-MEPFS requirements apply.", "aliases": ["applicability overlays", "code applicability", "jurisdictional applicability"], "source_ids": ["SRC-ICC-IBC-IPC-IFC-IECC-IEBC"], "children": [
        ("AHJ", "Authority Having Jurisdiction Coordination", ["AHJ", "code official coordination", "authority coordination"], ["SRC-ICC-IBC-IPC-IFC-IECC-IEBC"]),
        ("LCA", "Local Code Adoption", ["local code adoption", "adopted code", "local amendments"], ["SRC-ICC-IBC-IPC-IFC-IECC-IEBC"]),
        ("MCA", "Model Code Adoption", ["model code adoption", "I-Code adoption", "reference model code"], ["SRC-ICC-IBC-IPC-IFC-IECC-IEBC"]),
        ("OCC", "Occupancy Applicability", ["occupancy classification applicability", "use group applicability", "occupancy-based trigger"], ["SRC-ICC-IBC-IPC-IFC-IECC-IEBC"]),
        ("CTY", "Construction Type Applicability", ["construction type", "type of construction", "combustibility classification"], ["SRC-ICC-IBC-IPC-IFC-IECC-IEBC"]),
        ("RCA", "Risk Category Applicability", ["risk category", "importance category", "essential facility category"], ["SRC-ASCE-SEISMIC-RESILIENCE"]),
        ("CLZ", "Climate Zone Applicability", ["climate zone", "energy climate zone", "weather-dependent applicability"], ["SRC-ICC-IBC-IPC-IFC-IECC-IEBC", "SRC-ASHRAE-62-1-90-1-55-CX"]),
        ("SDC", "Seismic Design Category Applicability", ["SDC", "seismic design category", "seismic applicability trigger"], ["SRC-ASCE-SEISMIC-RESILIENCE", "SRC-FEMA-E74-NONSTRUCTURAL"]),
        ("FHA", "Flood Hazard Area Applicability", ["flood hazard area", "floodplain applicability", "design flood elevation trigger"], ["SRC-ASCE-24-FLOOD-RESISTANT"]),
        ("HCL", "Hazard Classification Applicability", ["hazard classification", "hazard occupancy", "special hazard trigger"], ["SRC-NFPA-70-101-13-72-14-20", "SRC-ICC-IBC-IPC-IFC-IECC-IEBC"]),
        ("FAR", "Fire Area Applicability", ["fire area", "fire compartment area", "sprinkler threshold area"], ["SRC-NFPA-70-101-13-72-14-20", "SRC-ICC-IBC-IPC-IFC-IECC-IEBC"]),
        ("EGR", "Means Of Egress Applicability", ["egress applicability", "exit access trigger", "means of egress trigger"], ["SRC-NFPA-70-101-13-72-14-20", "SRC-ICC-IBC-IPC-IFC-IECC-IEBC"]),
        ("EXB", "Existing Building Applicability", ["existing building applicability", "alteration trigger", "change of occupancy trigger"], ["SRC-ICC-IBC-IPC-IFC-IECC-IEBC"]),
        ("HIS", "Historic Building Applicability", ["historic building applicability", "heritage exception", "conservation code interface"], ["SRC-ICOMOS-CONSERVATION-CHARTERS", "SRC-ICC-IBC-IPC-IFC-IECC-IEBC"]),
        ("HIG", "High-Rise Building Applicability", ["high-rise applicability", "high-rise building trigger", "tower life-safety trigger"], ["SRC-ICC-IBC-IPC-IFC-IECC-IEBC", "SRC-NFPA-70-101-13-72-14-20"]),
        ("HCF", "Healthcare Facility Applicability", ["healthcare facility applicability", "hospital trigger", "health facility requirements"], ["SRC-NFPA-70-101-13-72-14-20", "SRC-FEMA-E74-NONSTRUCTURAL"]),
        ("DCT", "Data Center Applicability", ["data center applicability", "critical IT facility", "mission critical facility trigger"], ["SRC-TIA-BICSI-ICT-INFRASTRUCTURE", "SRC-ISO-22301-BCMS"]),
        ("LAB", "Laboratory Applicability", ["laboratory applicability", "lab hazard trigger", "research facility trigger"], ["SRC-NFPA-70-101-13-72-14-20", "SRC-ICC-IBC-IPC-IFC-IECC-IEBC"]),
        ("IND", "Industrial Facility Applicability", ["industrial facility applicability", "process hazard trigger", "industrial occupancy trigger"], ["SRC-ICC-IBC-IPC-IFC-IECC-IEBC", "SRC-ISA-IEC-62443-IACS"]),
        ("CRT", "Critical Facility Applicability", ["critical facility", "essential facility", "mission critical building"], ["SRC-ISO-22301-BCMS", "SRC-FEMA-P58-PUBLICATIONS"]),
        ("CPH", "Commissioning Phase Applicability", ["commissioning phase", "acceptance phase", "verification phase"], ["SRC-ASHRAE-IES-202-CX", "SRC-NIBS-WBDG-COMMISSIONING"]),
        ("OPH", "Operations Phase Applicability", ["operations phase", "in-use phase", "operational readiness"], ["SRC-ISO-41001-55001-FM-AM", "SRC-ISO-22301-BCMS"]),
        ("MPH", "Maintenance Phase Applicability", ["maintenance phase", "inspection cycle applicability", "maintenance trigger"], ["SRC-ISO-41001-55001-FM-AM", "SRC-NFPA-4-25-110-ITM-EPSS"]),
    ]},
    {"path_code": "STR.NSC", "label": "Nonstructural Support Coordination", "parent": "STR", "definition": "Cross-discipline coordination area for anchorage, restraints, supports, hangers, bracing, pads, penetrations, firestopping, and access clearances for nonstructural AEC-MEPFS components.", "aliases": ["nonstructural coordination", "equipment anchorage coordination", "support and bracing coordination"], "source_ids": ["SRC-FEMA-E74-NONSTRUCTURAL", "SRC-ASCE-SEISMIC-RESILIENCE"], "children": [
        ("SRN", "Seismic Restraint Coordination", ["seismic restraint", "seismic bracing", "nonstructural seismic restraint"], ["SRC-FEMA-E74-NONSTRUCTURAL", "SRC-ASCE-SEISMIC-RESILIENCE"]),
        ("WDR", "Wind Restraint Coordination", ["wind restraint", "wind anchorage", "wind load coordination"], ["SRC-ASCE-SEISMIC-RESILIENCE"]),
        ("FLP", "Flood-Resilient Equipment Placement", ["flood resilient placement", "equipment elevation", "floodproof equipment placement"], ["SRC-ASCE-24-FLOOD-RESISTANT"]),
        ("VIB", "Vibration Isolation Coordination", ["vibration isolation", "isolation mounts", "equipment vibration control"], ["SRC-ASHRAE-62-1-90-1-55-CX", "SRC-SMACNA-SEISMIC-RESTRAINT"]),
        ("HSK", "Housekeeping Pad Coordination", ["housekeeping pad", "equipment pad", "concrete equipment base"], ["SRC-FEMA-E74-NONSTRUCTURAL", "SRC-NECA-NEIS-ELECTRICAL"]),
        ("EQS", "Equipment Support Coordination", ["equipment supports", "equipment frames", "support coordination"], ["SRC-FEMA-E74-NONSTRUCTURAL", "SRC-SMACNA-SEISMIC-RESTRAINT"]),
        ("HBR", "Hangers And Bracing Coordination", ["hangers and bracing", "pipe bracing", "duct bracing"], ["SRC-SMACNA-SEISMIC-RESTRAINT", "SRC-FEMA-E74-NONSTRUCTURAL"]),
        ("PEN", "Penetration Coordination", ["penetration coordination", "sleeves and openings", "services penetrations"], ["SRC-ICC-IBC-IPC-IFC-IECC-IEBC"]),
        ("FST", "Firestopping Coordination", ["firestopping", "firestop systems", "rated penetration seal"], ["SRC-NFPA-70-101-13-72-14-20", "SRC-ICC-IBC-IPC-IFC-IECC-IEBC"]),
        ("ACR", "Access Clearance Coordination", ["access clearance", "service clearance", "working clearance"], ["SRC-NECA-NEIS-ELECTRICAL", "SRC-NFPA-70-101-13-72-14-20"]),
        ("MCL", "Maintenance Clearance Coordination", ["maintenance clearance", "replacement clearance", "maintainability access"], ["SRC-ISO-41001-55001-FM-AM"]),
        ("CEP", "Critical Equipment Protection", ["critical equipment protection", "essential equipment protection", "mission critical equipment"], ["SRC-ISO-22301-BCMS", "SRC-FEMA-E74-NONSTRUCTURAL"]),
    ]},
    {"path_code": "PER.ORC", "label": "Operational Resilience And Continuity", "parent": "PER", "definition": "Operational resilience overlay for continuity planning, backup power, redundancy, environmental event response, cybersecurity, recovery objectives, and critical facility operation.", "aliases": ["operational resilience", "facility continuity", "business continuity for facilities"], "source_ids": ["SRC-ISO-22301-BCMS", "SRC-NIST-CSF-IOT-CONTROLS"], "children": [
        ("BCP", "Business Continuity Planning", ["BCP", "business continuity plan", "continuity planning"], ["SRC-ISO-22301-BCMS"]),
        ("BIA", "Business Impact Analysis For Facility Systems", ["BIA", "business impact analysis", "facility impact analysis"], ["SRC-ISO-22301-BCMS"]),
        ("RTO", "Recovery Time Objective", ["RTO", "recovery time target", "time to recover"], ["SRC-ISO-22301-BCMS"]),
        ("RPO", "Recovery Point Objective", ["RPO", "recovery point target", "data recovery point"], ["SRC-ISO-22301-BCMS"]),
        ("NPO", "N Plus One Redundancy", ["N+1 redundancy", "standby capacity", "redundant capacity"], ["SRC-ISO-22301-BCMS"]),
        ("FLT", "Fault Tolerance", ["fault tolerance", "single point of failure control", "failover capacity"], ["SRC-ISO-22301-BCMS", "SRC-NIST-CSF-IOT-CONTROLS"]),
        ("WSR", "Wildfire Smoke Resilience", ["wildfire smoke resilience", "smoke event IAQ", "outdoor smoke response"], ["SRC-ASHRAE-62-1-90-1-55-CX"]),
        ("EHR", "Extreme Heat Resilience", ["extreme heat resilience", "heat event response", "thermal continuity"], ["SRC-ASHRAE-62-1-90-1-55-CX"]),
        ("WCT", "Water Continuity", ["water continuity", "potable water continuity", "water service resilience"], ["SRC-WHO-WASH-SANITATION-SAFETY"]),
        ("SNC", "Sanitation Continuity", ["sanitation continuity", "wastewater continuity", "public health continuity"], ["SRC-WHO-WASH-SANITATION-SAFETY"]),
        ("EMC", "Emergency Communications Continuity", ["emergency communications continuity", "resilient communications", "emergency messaging continuity"], ["SRC-NFPA-70-101-13-72-14-20", "SRC-TIA-BICSI-ICT-INFRASTRUCTURE"]),
        ("DRF", "Disaster Recovery For Facility Systems", ["facility disaster recovery", "building systems disaster recovery", "facility systems recovery"], ["SRC-ISO-22301-BCMS", "SRC-ISO-IEC-27001-ISMS"]),
    ]},
]

COMMISSIONING_NODES: list[tuple[str, str, list[str], list[str]]] = [
    ("CON.COM.OPR", "Owner Project Requirements", ["OPR", "owner's project requirements", "owner project requirements"], ["SRC-ASHRAE-IES-202-CX", "SRC-NIBS-WBDG-COMMISSIONING"]),
    ("CON.COM.BOD", "Basis Of Design", ["BOD", "basis of design", "design basis"], ["SRC-ASHRAE-IES-202-CX", "SRC-NIBS-WBDG-COMMISSIONING"]),
    ("CON.COM.CXP", "Commissioning Plan", ["Cx plan", "commissioning plan", "commissioning planning"], ["SRC-ASHRAE-IES-202-CX", "SRC-NIBS-WBDG-COMMISSIONING"]),
    ("CON.COM.IST", "Integrated Systems Testing", ["IST", "integrated systems testing", "integrated life safety testing"], ["SRC-NFPA-4-25-110-ITM-EPSS"]),
    ("CON.COM.FAT", "Fire Alarm Acceptance Testing", ["fire alarm acceptance", "fire alarm testing", "alarm acceptance test"], ["SRC-NFPA-4-25-110-ITM-EPSS"]),
    ("CON.COM.SAT", "Sprinkler Acceptance Testing", ["sprinkler acceptance", "water-based fire protection testing", "sprinkler testing"], ["SRC-NFPA-4-25-110-ITM-EPSS"]),
    ("CON.COM.SCT", "Smoke Control Acceptance Testing", ["smoke control testing", "smoke control acceptance", "smoke management test"], ["SRC-ASHRAE-IES-202-CX", "SRC-NFPA-4-25-110-ITM-EPSS"]),
    ("CON.COM.EPT", "Emergency Power Testing", ["EPSS testing", "emergency power testing", "generator acceptance testing"], ["SRC-NFPA-4-25-110-ITM-EPSS"]),
    ("CON.COM.LCA", "Lighting Controls Acceptance Testing", ["lighting controls acceptance", "lighting control testing", "controls acceptance test"], ["SRC-IES-LIGHTING-LIBRARY", "SRC-ASHRAE-IES-202-CX"]),
    ("CON.COM.ICT", "ICT Certification Testing", ["cabling certification", "ICT testing", "structured cabling certification"], ["SRC-TIA-BICSI-ICT-INFRASTRUCTURE"]),
    ("CON.COM.SSA", "Security System Acceptance", ["security acceptance testing", "access control acceptance", "video surveillance acceptance"], ["SRC-NIST-CSF-IOT-CONTROLS", "SRC-ISO-IEC-27001-ISMS"]),
    ("CON.COM.WDT", "Domestic Water Disinfection And Testing", ["domestic water disinfection", "water flushing and testing", "potable water testing"], ["SRC-WHO-WASH-SANITATION-SAFETY", "SRC-ICC-IBC-IPC-IFC-IECC-IEBC"]),
    ("CON.COM.BFT", "Backflow Prevention Testing", ["backflow testing", "backflow preventer test", "cross-connection test"], ["SRC-ICC-IBC-IPC-IFC-IECC-IEBC", "SRC-WHO-WASH-SANITATION-SAFETY"]),
    ("CON.COM.COB", "COBie Digital Handover Acceptance", ["COBie handover", "digital handover acceptance", "asset data handover acceptance"], ["SRC-ISO-41001-55001-FM-AM", "SRC-NIBS-WBDG-COMMISSIONING"]),
]

RELATIONSHIPS: list[tuple[str, str, str, str, list[str]]] = []

def add_rel(from_path: str, predicate: str, to_path: str, category: str, source_ids: list[str]) -> None:
    RELATIONSHIPS.append((from_path, predicate, to_path, category, source_ids))

# Equipment anchorage and nonstructural support coordination.
for target in ["MEC.AHD", "MEC.HPS", "MEC.PLT", "ELE.PDS", "ELE.ESP.GTS", "FLS.ASS", "PLS.PMP", "PLS.SDS", "SEC.VSS", "SEC.ACS", "SMS.BAS", "ELE.LVC.DRR"]:
    add_rel("STR.NSC.SRN", "constrains", target, "equipment_anchorage", ["SRC-FEMA-E74-NONSTRUCTURAL", "SRC-ASCE-SEISMIC-RESILIENCE"])
for target in ["MEC.PLT", "ELE.ESP.GTS", "PLS.STD", "SEC.PRS", "SMS.EDG", "FLS.FPR", "ELE.LVC.TEP", "SEC.SOC"]:
    add_rel("STR.NSC.WDR", "constrains", target, "equipment_anchorage", ["SRC-ASCE-SEISMIC-RESILIENCE"])
for target in ["ELE.ESP.GTS", "ELE.ESP.UPS", "MEC.PLT", "PLS.PMP", "SEC.SOC", "SMS.EDG", "SAN.WST", "OPS.EMO.BUP"]:
    add_rel("STR.NSC.FLP", "constrains", target, "equipment_anchorage", ["SRC-ASCE-24-FLOOD-RESISTANT"])
for target in ["MEC.HPS", "MEC.PLT", "FLS.ASS.FIP", "PLS.PMP", "ELE.ESP.GTS", "MEC.IEQ.NVC"]:
    add_rel("STR.NSC.VIB", "constrains", target, "equipment_anchorage", ["SRC-ASHRAE-62-1-90-1-55-CX", "SRC-SMACNA-SEISMIC-RESTRAINT"])
for target in ["MEC.PLT", "ELE.ESP.GTS", "FLS.ASS.FIP", "PLS.PMP", "SMS.EDG", "ELE.PDS.TRS"]:
    add_rel("STR.NSC.HSK", "requires", target, "equipment_anchorage", ["SRC-FEMA-E74-NONSTRUCTURAL", "SRC-NECA-NEIS-ELECTRICAL"])
for target in ["MEC.AHD", "MEC.HPS", "MEC.PLT", "ELE.PDS", "ELE.LVC.DRR", "FLS.ASS", "PLS.PWS", "PLS.SDS", "SEC.VSS", "SEC.ACS", "SMS.BAS", "SMS.NET"]:
    add_rel("STR.NSC.EQS", "requires", target, "equipment_anchorage", ["SRC-FEMA-E74-NONSTRUCTURAL", "SRC-SMACNA-SEISMIC-RESTRAINT"])
for target in ["MEC.AHD", "MEC.HPS", "FLS.ASS", "PLS.SDS", "ELE.LVC.TEP", "ELE.PDS.TRS", "SEC.CPI", "SMS.BAS"]:
    add_rel("STR.NSC.HBR", "constrains", target, "equipment_anchorage", ["SRC-SMACNA-SEISMIC-RESTRAINT", "SRC-FEMA-E74-NONSTRUCTURAL"])
for target in ["MEC.AHD", "ELE.PDS", "FLS.ASS", "PLS.SDS", "SEC.CPI", "SMS.BAS", "FLS.CMP", "ARC.COO.CRE"]:
    add_rel("STR.NSC.PEN", "constrains", target, "equipment_anchorage", ["SRC-ICC-IBC-IPC-IFC-IECC-IEBC"])
for target in ["MEC.AHD", "ELE.PDS", "FLS.ASS", "PLS.SDS", "FLS.CMP", "FLS.SCC", "ARC.FIR.COM"]:
    add_rel("STR.NSC.FST", "constrains", target, "equipment_anchorage", ["SRC-NFPA-70-101-13-72-14-20", "SRC-ICC-IBC-IPC-IFC-IECC-IEBC"])
for target in ["ELE.PDS", "ELE.ESP.GTS", "ELE.ESP.UPS", "MEC.PLT", "FLS.FDA.FAC", "SEC.SOC", "SMS.EDG"]:
    add_rel("STR.NSC.ACR", "requires", target, "equipment_anchorage", ["SRC-NECA-NEIS-ELECTRICAL", "SRC-NFPA-70-101-13-72-14-20"])
for target in ["MEC.PLT", "MEC.HPS", "ELE.ESP.GTS", "ELE.ESP.UPS", "FLS.ASS.FIP", "PLS.PMP", "OPS.PRM.MAS", "OPS.ASM.ASC"]:
    add_rel("STR.NSC.MCL", "requires", target, "equipment_anchorage", ["SRC-ISO-41001-55001-FM-AM"])
for target in ["ELE.ESP.GTS", "ELE.ESP.UPS", "FLS.FDA.FAC", "FLS.SMK.SCO", "SEC.EMC", "SMS.CSB", "OPS.EMO.BCP"]:
    add_rel("STR.NSC.CEP", "constrains", target, "equipment_anchorage", ["SRC-ISO-22301-BCMS", "SRC-FEMA-E74-NONSTRUCTURAL"])
for standard in ["COM.STD.ASC.LDN", "COM.STD.FEM.NSE", "COM.STD.SMA.SRM", "COM.STD.ASC.FLD"]:
    add_rel("STR.NSC", "maps_to_external_standard", standard, "equipment_anchorage", ["SRC-FEMA-E74-NONSTRUCTURAL", "SRC-ASCE-SEISMIC-RESILIENCE"])

# Commissioning, testing, acceptance, and handover.
for target in ["CON.COM.OPR", "CON.COM.BOD", "CON.COM.CXP", "CON.COM.FTE", "CON.COM.HND", "OPS.COM.OAM", "OPS.COM.TRA"]:
    add_rel("COM.APP.CPH", "constrains", target, "commissioning_handover", ["SRC-ASHRAE-IES-202-CX", "SRC-NIBS-WBDG-COMMISSIONING"])
add_rel("CON.COM.CXP", "requires", "CON.COM.OPR", "commissioning_handover", ["SRC-ASHRAE-IES-202-CX"])
add_rel("CON.COM.CXP", "requires", "CON.COM.BOD", "commissioning_handover", ["SRC-ASHRAE-IES-202-CX"])
add_rel("CON.COM.BOD", "requires", "CON.COM.OPR", "commissioning_handover", ["SRC-NIBS-WBDG-COMMISSIONING"])
for standard in ["COM.STD.ASH.CPS", "COM.STD.ASH.CXG", "COM.STD.NIB.CXP", "COM.STD.NIB.OPR", "COM.STD.NIB.BOD"]:
    add_rel("CON.COM.CXP", "maps_to_external_standard", standard, "commissioning_handover", ["SRC-ASHRAE-IES-202-CX", "SRC-NIBS-WBDG-COMMISSIONING"])
commissioning_requires = {
    "CON.COM.IST": ["FLS.FDA.FAC", "FLS.SMK.SCO", "ELE.ESP.GTS", "SMS.BAS", "MEC.SMK"],
    "CON.COM.FAT": ["FLS.FDA.FAC", "FLS.FDA.IND", "FLS.FDA.NOA"],
    "CON.COM.SAT": ["FLS.ASS.SHC", "FLS.ASS.FIP", "FLS.ASS.STA"],
    "CON.COM.SCT": ["FLS.SMK.SCO", "MEC.SMK", "SMS.BAS"],
    "CON.COM.EPT": ["ELE.ESP.GTS", "ELE.ESP.UPS", "ELE.ESP.LSL", "ELE.ESP.SEC"],
    "CON.COM.LCA": ["ELE.LLC.ODC", "ELE.LLC.EML", "SMS.SEN"],
    "CON.COM.ICT": ["ELE.LVC.STC", "ELE.LVC.DRR", "ELE.LVC.TEP"],
    "CON.COM.SSA": ["SEC.ACS", "SEC.VSS", "SEC.SOR.SMT"],
    "CON.COM.WDT": ["PLS.PWS", "PLS.PWS.BAP", "SAN.WST.WQM"],
    "CON.COM.BFT": ["PLS.PWS.BAP", "PLS.PWS.PRC", "SAN.PHE.HRC"],
    "CON.COM.COB": ["DIG.EXC.CDA", "DIG.DTA.LDH", "OPS.AST.AIM", "OPS.COM.OAM"],
}
for source, targets in commissioning_requires.items():
    for target in targets:
        add_rel(source, "requires", target, "commissioning_handover", ["SRC-ASHRAE-IES-202-CX", "SRC-NIBS-WBDG-COMMISSIONING"])
commissioning_standards = {
    "CON.COM.IST": ["COM.STD.NFP.IFT"],
    "CON.COM.FAT": ["COM.STD.NFP.FAL"],
    "CON.COM.SAT": ["COM.STD.NFP.SPR", "COM.STD.NFP.ITM"],
    "CON.COM.SCT": ["COM.STD.ASH.CPS", "COM.STD.NFP.IFT"],
    "CON.COM.EPT": ["COM.STD.NFP.EPS"],
    "CON.COM.LCA": ["COM.STD.IES.CXM"],
    "CON.COM.ICT": ["COM.STD.TIA.CAB", "COM.STD.NIB.CXP"],
    "CON.COM.SSA": ["COM.STD.NIS.CSF", "COM.STD.ISO.ISM"],
    "CON.COM.WDT": ["COM.STD.ICC.IPC", "COM.STD.WHO.WSP"],
    "CON.COM.BFT": ["COM.STD.ICC.IPC", "COM.STD.WHO.SSP"],
    "CON.COM.COB": ["COM.STD.ISO.FMS", "COM.STD.ISO.AMS"],
}
for source, standards in commissioning_standards.items():
    for standard in standards:
        add_rel(source, "maps_to_external_standard", standard, "commissioning_handover", ["SRC-ASHRAE-IES-202-CX"])
for target in ["OPS.COM.OAM", "OPS.COM.TRA", "OPS.AST.AIM", "OPS.PRM.MAS", "OPS.PRM.EQR", "OPS.ASM.ASC"]:
    add_rel("CON.COM.HND", "requires", target, "commissioning_handover", ["SRC-NIBS-WBDG-COMMISSIONING", "SRC-ISO-41001-55001-FM-AM"])

# Operational resilience and continuity.
for standard in ["COM.STD.ISO.BCM", "COM.STD.ISO.FMS", "COM.STD.ISO.AMS"]:
    add_rel("PER.ORC", "maps_to_external_standard", standard, "resilience_continuity", ["SRC-ISO-22301-BCMS", "SRC-ISO-41001-55001-FM-AM"])
resilience_requires = {
    "PER.ORC.BCP": ["OPS.EMO.BCP", "OPS.EMO.ICI", "OPS.EMO.BUP", "PER.REP.COO"],
    "PER.ORC.BIA": ["OPS.ASM.ASC", "PER.RSK.FMO", "PER.REP.HAI", "DIG.DTA.AIR"],
    "PER.ORC.RTO": ["PER.REP.RTT", "OPS.EMO.BCP", "ELE.ESP.GTS", "SMS.CSB"],
    "PER.ORC.RPO": ["DIG.DTA.LDH", "DIG.DTA.OPD", "SMS.DAT", "SEC.SOC"],
    "PER.ORC.NPO": ["ELE.ESP.GTS", "ELE.ESP.UPS", "MEC.HPS", "SMS.NET"],
    "PER.ORC.FLT": ["ELE.ESP.SEC", "SMS.CSB.NES", "SMS.EDG", "SEC.SOC"],
    "PER.ORC.WSR": ["MEC.IEQ.VER", "MEC.VEN", "MEC.AHD", "PER.IEQ"],
    "PER.ORC.EHR": ["MEC.COO", "MEC.HPS", "PER.THM", "OPS.EMO.BUP"],
    "PER.ORC.WCT": ["PLS.PWS", "SAN.WST", "OPS.EMO.BUP", "PLS.PMP"],
    "PER.ORC.SNC": ["PLS.SDS", "SAN.PHE", "SAN.WCT", "OPS.EMO.BUP"],
    "PER.ORC.EMC": ["SEC.EMC", "FLS.FDA.EVC", "ELE.LVC.PAS", "ELE.ESP.GTS"],
    "PER.ORC.DRF": ["SMS.CSB", "SMS.CSB.NES", "SEC.CPI", "DIG.DTA.LDH", "OPS.EMO.BCP"],
}
for source, targets in resilience_requires.items():
    for target in targets:
        add_rel(source, "requires", target, "resilience_continuity", ["SRC-ISO-22301-BCMS"])
resilience_constraints = {
    "COM.APP.CRT": ["PER.ORC.BCP", "PER.ORC.RTO", "PER.ORC.NPO", "ELE.ESP", "FLS.ERI", "SEC.EMC"],
    "COM.APP.DCT": ["PER.ORC.NPO", "PER.ORC.RPO", "ELE.ESP.UPS", "ELE.LVC.DRR", "SMS.CSB.NES"],
    "COM.APP.HCF": ["PER.ORC.BCP", "FLS.ERI", "ELE.ESP", "PLS.PWS", "SAN.PHE"],
    "COM.APP.FHA": ["PER.ORC.WCT", "STR.NSC.FLP", "ELE.ESP.GTS", "MEC.PLT"],
}
for source, targets in resilience_constraints.items():
    for target in targets:
        add_rel(source, "constrains", target, "resilience_continuity", ["SRC-ISO-22301-BCMS", "SRC-ASCE-24-FLOOD-RESISTANT"])
for source, standards in {"PER.ORC.DRF": ["COM.STD.NIS.BCS", "COM.STD.ISO.ISM", "COM.STD.ISA.IAC"], "PER.ORC.BCP": ["COM.STD.ISO.BCM"], "PER.ORC.WSR": ["COM.STD.ASH.VNT"], "PER.ORC.WCT": ["COM.STD.WHO.WSP"], "PER.ORC.SNC": ["COM.STD.WHO.SSP"]}.items():
    for standard in standards:
        add_rel(source, "maps_to_external_standard", standard, "resilience_continuity", ["SRC-ISO-22301-BCMS"])

# Jurisdiction, code, standard, and applicability overlays.
for target in ["COM.BLD.IBC", "COM.FIR", "COM.OCC.OCL", "COM.INS.SIN", "FLS.RIS", "FLS.FDS", "FLS.ERI", "CON.COM.IST"]:
    add_rel("COM.APP.AHJ", "governs", target, "applicability_overlay", ["SRC-ICC-IBC-IPC-IFC-IECC-IEBC", "SRC-NFPA-70-101-13-72-14-20"])
for target in ["COM.BLD.IBC", "COM.BLD.NBC", "COM.BLD.NCC", "COM.FIR", "COM.ENV", "COM.PER"]:
    add_rel("COM.APP.LCA", "applicable_in_jurisdiction", target, "applicability_overlay", ["SRC-ICC-IBC-IPC-IFC-IECC-IEBC"])
for target in ["COM.STD.ICC.IBC", "COM.STD.ICC.IPC", "COM.STD.ICC.IFC", "COM.STD.ICC.IEC", "COM.STD.ICC.IEB"]:
    add_rel("COM.APP.MCA", "maps_to_external_standard", target, "applicability_overlay", ["SRC-ICC-IBC-IPC-IFC-IECC-IEBC"])
for source, targets in {
    "COM.APP.OCC": ["COM.OCC.OCL", "FLS.MEE", "FLS.ASS.SHC", "PLS.PFE", "SEC.SOR.THA"],
    "COM.APP.CTY": ["COM.CAD.COT", "ARC.FIR.COM", "FLS.CMP", "STR.SYS"],
    "COM.APP.RCA": ["STR.WSD", "STR.NSC.SRN", "ELE.ESP", "PER.ORC.BCP"],
    "COM.APP.CLZ": ["PER.ENE", "MEC.IEQ", "MEC.VEN", "SUS.CLI.FAD"],
    "COM.APP.SDC": ["STR.SEI", "STR.NSC.SRN", "MEC.PLT", "ELE.ESP.GTS", "FLS.ASS", "PLS.PMP"],
    "COM.APP.FHA": ["STR.NSC.FLP", "ELE.ESP.GTS", "PLS.PMP", "SAN.DFS", "PER.ORC.WCT"],
    "COM.APP.HCL": ["FLS.HAZ", "FLS.ASS.SHC", "PLS.GAS", "MEC.REF"],
    "COM.APP.FAR": ["FLS.ASS", "FLS.FDA", "FLS.SCC", "ARC.FIR.COM"],
    "COM.APP.EGR": ["FLS.MEE", "FLS.EGR", "FLS.FDA.NOA", "SEC.EMC"],
    "COM.APP.EXB": ["COM.STD.ICC.IEB", "HRC.ADP", "OPS.REN", "ARC.COD.JUR"],
    "COM.APP.HIS": ["HRC.PRN", "HRC.HST", "HRC.ADP", "ARC.COD.JUR"],
    "COM.APP.HIG": ["FLS.SMK", "FLS.ERI", "ELE.ESP", "SEC.EMC", "MEC.SMK"],
    "COM.APP.HCF": ["FLS.ERI", "ELE.ESP", "PLS.PWS", "SAN.PHE", "STR.NSC.SRN"],
    "COM.APP.DCT": ["ELE.LVC.DRR", "ELE.ESP.UPS", "SMS.CSB", "PER.ORC.NPO"],
    "COM.APP.LAB": ["FLS.HAZ", "PLS.GAS", "MEC.VEN", "SAN.IWW"],
    "COM.APP.IND": ["FLS.HAZ", "SMS.CSB", "SEC.CPI", "MEC.REF"],
    "COM.APP.CPH": ["CON.COM", "MEC.MCC", "FLS.FDA", "ELE.ESP", "PLS.PWS"],
    "COM.APP.OPH": ["OPS.FAC", "OPS.EMO", "PER.ORC", "SMS.CSB"],
    "COM.APP.MPH": ["OPS.PRM", "OPS.INS", "FLS.ASS", "ELE.ESP"],
}.items():
    for target in targets:
        add_rel(source, "constrains", target, "applicability_overlay", ["SRC-ICC-IBC-IPC-IFC-IECC-IEBC"])

IMPROVE_HINTS: dict[str, tuple[list[str], list[str], str]] = {
    "MEC.PLT": (["mechanical plant equipment", "central plant equipment", "mechanical equipment anchorage"], ["SRC-FEMA-E74-NONSTRUCTURAL", "SRC-SMACNA-SEISMIC-RESTRAINT"], "equipment_coordination_endpoint"),
    "MEC.AHD": (["air distribution supports", "duct bracing", "air handling support coordination"], ["SRC-SMACNA-SEISMIC-RESTRAINT"], "equipment_coordination_endpoint"),
    "MEC.HPS": (["hydronic equipment support", "pump support coordination", "pipe bracing coordination"], ["SRC-SMACNA-SEISMIC-RESTRAINT"], "equipment_coordination_endpoint"),
    "ELE.PDS": (["electrical equipment anchorage", "switchgear support coordination", "electrical support coordination"], ["SRC-NECA-NEIS-ELECTRICAL", "SRC-FEMA-E74-NONSTRUCTURAL"], "equipment_coordination_endpoint"),
    "ELE.ESP": (["emergency power resilience", "standby power continuity", "EPSS coordination"], ["SRC-NFPA-4-25-110-ITM-EPSS"], "resilience_endpoint"),
    "ELE.LVC.DRR": (["ICT rack support", "data room rack anchorage", "cabinet support coordination"], ["SRC-TIA-BICSI-ICT-INFRASTRUCTURE", "SRC-FEMA-E74-NONSTRUCTURAL"], "equipment_coordination_endpoint"),
    "FLS.FDA.FAC": (["fire alarm acceptance", "fire alarm control unit testing", "alarm system continuity"], ["SRC-NFPA-4-25-110-ITM-EPSS"], "commissioning_endpoint"),
    "FLS.ASS": (["sprinkler support coordination", "water-based fire protection ITM", "suppression acceptance"], ["SRC-NFPA-4-25-110-ITM-EPSS", "SRC-FEMA-E74-NONSTRUCTURAL"], "commissioning_endpoint"),
    "FLS.SMK.SCO": (["smoke control acceptance", "smoke control integrated testing", "smoke control commissioning"], ["SRC-ASHRAE-IES-202-CX", "SRC-NFPA-4-25-110-ITM-EPSS"], "commissioning_endpoint"),
    "PLS.PWS": (["water continuity", "potable water acceptance", "domestic water testing"], ["SRC-WHO-WASH-SANITATION-SAFETY", "SRC-ICC-IBC-IPC-IFC-IECC-IEBC"], "resilience_endpoint"),
    "PLS.PWS.BAP": (["backflow testing", "cross-connection control", "backflow prevention acceptance"], ["SRC-WHO-WASH-SANITATION-SAFETY", "SRC-ICC-IBC-IPC-IFC-IECC-IEBC"], "commissioning_endpoint"),
    "SEC.SOC": (["security operations continuity", "security command center resilience", "SOC continuity"], ["SRC-ISO-22301-BCMS", "SRC-NIST-CSF-IOT-CONTROLS"], "resilience_endpoint"),
    "SEC.EMC": (["emergency communication continuity", "emergency messaging resilience", "duress communications continuity"], ["SRC-NFPA-70-101-13-72-14-20", "SRC-TIA-BICSI-ICT-INFRASTRUCTURE"], "resilience_endpoint"),
    "SMS.CSB": (["building systems cybersecurity", "BAS cybersecurity", "OT network security"], ["SRC-NIST-CSF-IOT-CONTROLS", "SRC-ISO-IEC-27001-ISMS", "SRC-ISA-IEC-62443-IACS"], "resilience_endpoint"),
    "SMS.CSB.NES": (["OT network segmentation", "building controls network zones", "segmented BAS network"], ["SRC-NIST-CSF-IOT-CONTROLS", "SRC-ISA-IEC-62443-IACS"], "resilience_endpoint"),
    "DIG.DTA.LDH": (["digital handover", "asset data closeout", "lifecycle information handover"], ["SRC-ISO-41001-55001-FM-AM", "SRC-NIBS-WBDG-COMMISSIONING"], "handover_endpoint"),
    "OPS.AST.AIM": (["asset information handover", "AIM handover", "facility asset data handover"], ["SRC-ISO-41001-55001-FM-AM", "SRC-NIBS-WBDG-COMMISSIONING"], "handover_endpoint"),
    "OPS.EMO.BCP": (["facility business continuity plan", "building continuity plan", "operational continuity plan"], ["SRC-ISO-22301-BCMS"], "resilience_endpoint"),
    "OPS.PRM.MAS": (["preventive maintenance setup", "maintenance schedule handover", "PM program setup"], ["SRC-ISO-41001-55001-FM-AM"], "handover_endpoint"),
    "PER.REP.RTT": (["recovery time target", "RTO", "facility recovery time"], ["SRC-ISO-22301-BCMS"], "resilience_endpoint"),
    "PER.RSK.RED": (["redundancy planning", "N+1 redundancy", "standby capacity"], ["SRC-ISO-22301-BCMS"], "resilience_endpoint"),
    "COM.OCC.OCL": (["occupancy applicability", "occupancy trigger", "use group trigger"], ["SRC-ICC-IBC-IPC-IFC-IECC-IEBC"], "applicability_endpoint"),
    "COM.CAD.COT": (["construction type trigger", "construction classification", "type of construction applicability"], ["SRC-ICC-IBC-IPC-IFC-IECC-IEBC"], "applicability_endpoint"),
    "FLS.HAZ": (["hazard classification applicability", "special hazard trigger", "hazard occupancy"], ["SRC-NFPA-70-101-13-72-14-20", "SRC-ICC-IBC-IPC-IFC-IECC-IEBC"], "applicability_endpoint"),
    "HRC.ADP": (["historic building applicability", "adaptive reuse code interface", "heritage code coordination"], ["SRC-ICOMOS-CONSERVATION-CHARTERS", "SRC-ICC-IBC-IPC-IFC-IECC-IEBC"], "applicability_endpoint"),
    "ELE.ESP.GTS": (["generator anchorage", "EPSS acceptance testing", "generator continuity"], ["SRC-NFPA-4-25-110-ITM-EPSS", "SRC-FEMA-E74-NONSTRUCTURAL"], "multi_overlay_endpoint"),
    "ELE.ESP.UPS": (["UPS resilience", "UPS support coordination", "battery backup continuity"], ["SRC-ISO-22301-BCMS", "SRC-FEMA-E74-NONSTRUCTURAL"], "multi_overlay_endpoint"),
}


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

    def add_node(path_code: str, label: str, level: int, parent_path_code: str, definition: str, aliases: list[str], source_ids: list[str], node_kind: str) -> dict[str, Any]:
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
            "example_concepts": _dedupe([label.lower(), parent["label"].lower(), path_code.lower()]),
            "generation_method": GENERATION_METHOD,
            "source_family_ids": source_ids,
            "provenance_note": "Kimi-guided, human-integrated metadata-only semantic overlay enrichment; no standards clauses or protected source text stored.",
            "confidence": "high",
            "quality_signal": "curated_public_reference_overlay",
            "semantic_node_kind": node_kind,
        }
        records.append(record)
        path_to_record[path_code] = record
        added_nodes.append(record)
        aliases_added += len(full_aliases)
        add_edge(parent_path_code, "broader_than", path_code, "hierarchy", source_ids)
        return record

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
            "source_family_ids": source_ids,
            "provenance_note": "Curated metadata-only semantic overlay relationship added during cross-domain AEC-MEPFS enrichment.",
        }
        relationships.append(relationship)
        added_relationships.append(relationship)
        existing_edges.add(key)

    # Add source-backed standards/guidance reference nodes.
    for family in STANDARD_FAMILIES:
        add_node(family["path_code"], family["label"], 3, "COM.STD", family["definition"], family["aliases"], family["source_ids"], "standard_family")
        for suffix, label, aliases, source_id in family["children"]:
            child_path = f"{family['path_code']}.{suffix}"
            add_node(child_path, label, 4, family["path_code"], f"Metadata-only reference node for {label}, used to connect AEC-MEPFS overlay topics to public source-family labels without storing standard text.", aliases, [source_id], "standard_reference")
            add_edge(child_path, "part_of", family["path_code"], "source_reference", [source_id])
    for parent_path, suffix, label, aliases, source_id in EXISTING_STANDARD_CHILDREN:
        child_path = f"{parent_path}.{suffix}"
        add_node(child_path, label, 4, parent_path, f"Metadata-only reference node for {label}, used for commissioning, resilience, or cybersecurity crosswalks without storing protected source text.", aliases, [source_id], "standard_reference")
        add_edge(child_path, "part_of", parent_path, "source_reference", [source_id])

    # Add overlay and commissioning nodes.
    for parent in OVERLAY_PARENTS:
        add_node(parent["path_code"], parent["label"], 2, parent["parent"], parent["definition"], parent["aliases"], parent["source_ids"], "semantic_overlay_parent")
        for suffix, label, aliases, source_ids in parent["children"]:
            add_node(f"{parent['path_code']}.{suffix}", label, 3, parent["path_code"], f"Cross-domain overlay concept for {label.lower()} across AEC-MEPFS coordination, lifecycle, and applicability decisions.", aliases, source_ids, "semantic_overlay")
    for path_code, label, aliases, source_ids in COMMISSIONING_NODES:
        add_node(path_code, label, 3, "CON.COM", f"Commissioning, acceptance, testing, or handover overlay concept for {label.lower()} in AEC-MEPFS delivery workflows.", aliases, source_ids, "commissioning_overlay")

    # Improve existing nodes before creating relationship report.
    for path_code, (aliases, source_ids, kind) in IMPROVE_HINTS.items():
        if path_code not in path_to_record:
            continue
        added = _merge_metadata(path_to_record[path_code], aliases, source_ids, kind)
        aliases_added += added
        if added:
            improved_nodes.add(path_code)

    for from_path, predicate, to_path, category, source_ids in RELATIONSHIPS:
        add_edge(from_path, predicate, to_path, category, source_ids)
        # source endpoint provenance improvements make the graph itself more queryable.
        for endpoint in (from_path, to_path):
            if endpoint in path_to_record:
                added = _merge_metadata(path_to_record[endpoint], [], source_ids, path_to_record[endpoint].get("semantic_node_kind", "semantic_overlay_endpoint"))
                if added:
                    aliases_added += added
                    improved_nodes.add(endpoint)

    new_payload = {**payload, "records": records, "relationships": relationships}
    relationship_categories = Counter(rel.get("semantic_overlay_category") for rel in added_relationships)
    predicate_counts = Counter(rel.get("predicate") for rel in added_relationships)
    cross_domain = [
        rel for rel in added_relationships
        if path_to_record_by_id(records, rel["from_id"])["path_code"].split(".")[0]
        != path_to_record_by_id(records, rel["to_id"])["path_code"].split(".")[0]
    ]
    report = {
        "ok": True,
        "generation_method": GENERATION_METHOD,
        "input_record_count": len(payload["records"]),
        "output_record_count": len(records),
        "input_relationship_count": len(payload["relationships"]),
        "output_relationship_count": len(relationships),
        "added_node_count": len(added_nodes),
        "added_nodes_by_kind": dict(sorted(Counter(record.get("semantic_node_kind") for record in added_nodes).items())),
        "improved_existing_node_count": len(improved_nodes),
        "added_relationship_count": len(added_relationships),
        "added_relationships_by_predicate": dict(sorted(predicate_counts.items())),
        "added_relationships_by_category": dict(sorted(relationship_categories.items())),
        "cross_domain_relationship_count": len(cross_domain),
        "aliases_added_or_preserved_on_new_and_improved_nodes": aliases_added,
        "source_reference_ids": [row["source_id"] for row in SOURCE_REFERENCES],
        "sample_added_path_codes": [record["path_code"] for record in added_nodes[:80]],
        "rights_safety": {
            "protected_source_payloads_ingested": False,
            "source_payload_mode": "labels_metadata_and_source_family_references_only",
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
    existing = {row.get("source_id") for row in rows}
    added: list[dict[str, Any]] = []
    for reference in SOURCE_REFERENCES:
        if reference["source_id"] in existing:
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
            "declared_use_boundary": "no standards text, table, figure, diagram, or clause ingest; source-family metadata labels only",
            "currentness_check_date": "2026-04-29",
            "update_cadence": "before source admission and per taxonomy release",
            "blocking_notes": "content ingest blocked until explicit license/legal review; this enrichment uses metadata-only topic labels and relationships",
        }
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
        "rights_safety": {
            "protected_source_payloads_ingested": False,
            "source_payload_mode": "source_family_metadata_only",
            "content_ingest_rows_added": False,
        },
    }


def path_to_record_by_id(records: list[dict[str, Any]], record_id: str) -> dict[str, Any]:
    for record in records:
        if record.get("id") == record_id:
            return record
    raise KeyError(record_id)


def _next_domain_id(records: list[dict[str, Any]]) -> int:
    return max(int(record["id"].split("-")[-1]) for record in records if str(record.get("id", "")).startswith("VTN-DOM-")) + 1


def _merge_metadata(record: dict[str, Any], aliases: list[str], source_ids: list[str], node_kind: str) -> int:
    alias_count = _merge_list(record, "aliases", aliases)
    _merge_list(record, "source_family_ids", source_ids)
    record.setdefault("provenance_note", "Metadata-only semantic overlay enrichment; no protected source payload stored.")
    record.setdefault("quality_signal", "curated_public_reference_overlay")
    record.setdefault("confidence", "high")
    record.setdefault("semantic_node_kind", node_kind)
    return alias_count


def _merge_list(record: dict[str, Any], key: str, values: list[str]) -> int:
    existing = list(record.get(key, [])) if isinstance(record.get(key, []), list) else []
    before = len(existing)
    record[key] = _dedupe([*existing, *values])
    return len(record[key]) - before


def _dedupe(values: list[str]) -> list[str]:
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
    parser = argparse.ArgumentParser(description="Add Kimi-guided cross-domain semantic overlay relationships to the AEC-MEPFS backbone.")
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
