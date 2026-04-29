from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

GENERATION_METHOD = (
    "steward_governed_targeted_semantic_enrichment_from_kimi_guided_public_"
    "aec_mepfs_standard_family_taxonomies"
)
SCOPE_NOTE = (
    "Targeted AEC-MEPFS semantic enrichment synthesized from Kimi-guided taxonomy "
    "review, public standards-family metadata, official standards landing pages, "
    "professional body topic structures, and rights-safe domain knowledge; labels "
    "and metadata only, no protected source payloads."
)
OWNER = "Philip Lewis"
RELEASE_VERSION = "0.5.0"

SOURCE_REFERENCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC-ASHRAE-62-1-90-1-55-CX",
        "source_family": "ASHRAE ventilation, energy, comfort, and commissioning standards",
        "publisher_authority": "ASHRAE",
        "official_url": "https://www.ashrae.org/technical-resources/bookstore/standard-90-1; https://www.ashrae.org/resources--publications/bookstore/standards-62-1--62-2; https://www.ashrae.org/news/esociety/updated-commissioning-guideline",
        "intended_vitruvius_use": "metadata-only HVAC, IAQ, energy, comfort, and commissioning taxonomy context",
    },
    {
        "source_id": "SRC-NFPA-70-101-13-72-14-20",
        "source_family": "NFPA electrical, life-safety, sprinkler, alarm, standpipe, and fire-pump standards",
        "publisher_authority": "NFPA",
        "official_url": "https://www.nfpa.org/codes-and-standards",
        "intended_vitruvius_use": "metadata-only fire, life-safety, electrical, and emergency-system taxonomy context",
    },
    {
        "source_id": "SRC-ICC-IBC-IPC-IFC-IECC-IEBC",
        "source_family": "ICC I-Code building, plumbing, fire, energy, and existing-building code families",
        "publisher_authority": "International Code Council",
        "official_url": "https://www.iccsafe.org/products-and-services/i-codes/2024-i-codes/",
        "intended_vitruvius_use": "metadata-only code-family and discipline crosswalk taxonomy context",
    },
    {
        "source_id": "SRC-TIA-BICSI-ICT-INFRASTRUCTURE",
        "source_family": "TIA and BICSI ICT infrastructure standards and methods",
        "publisher_authority": "TIA / BICSI",
        "official_url": "https://www.bicsi.org/standards; https://tiaonline.org/what-we-do/standards/",
        "intended_vitruvius_use": "metadata-only structured cabling, pathways, spaces, bonding, and ICT infrastructure taxonomy context",
    },
    {
        "source_id": "SRC-NIST-CSF-IOT-CONTROLS",
        "source_family": "NIST cybersecurity framework, IoT baseline, and security control guidance",
        "publisher_authority": "NIST",
        "official_url": "https://www.nist.gov/itl/applied-cybersecurity/nist-cybersecurity-iot-program; https://www.nist.gov/cyberframework",
        "intended_vitruvius_use": "metadata-only smart-systems, IoT, cyber-physical security, and control-system taxonomy context",
    },
    {
        "source_id": "SRC-WHO-WASH-SANITATION-SAFETY",
        "source_family": "WHO water, sanitation, hygiene, and sanitation safety planning guidance",
        "publisher_authority": "World Health Organization",
        "official_url": "https://www.who.int/teams/environment-climate-change-and-health/water-sanitation-and-health/sanitation-safety/sanitation-safety-planning",
        "intended_vitruvius_use": "metadata-only sanitation risk, WASH, public-health engineering, and wastewater safety taxonomy context",
    },
    {
        "source_id": "SRC-ICOMOS-CONSERVATION-CHARTERS",
        "source_family": "ICOMOS conservation charters and doctrinal texts",
        "publisher_authority": "ICOMOS",
        "official_url": "https://www.icomos.org/en/resources/charters-and-texts",
        "intended_vitruvius_use": "metadata-only heritage conservation principles, authenticity, intervention, and interpretation taxonomy context",
    },
    {
        "source_id": "SRC-ISO-14040-14044-LCA",
        "source_family": "ISO 14040 / ISO 14044 life-cycle assessment standards",
        "publisher_authority": "ISO",
        "official_url": "https://www.iso.org/standard/37456.html; https://www.iso.org/standard/38498.html",
        "intended_vitruvius_use": "metadata-only sustainability, embodied-carbon, and LCA taxonomy context",
    },
    {
        "source_id": "SRC-ISO-41001-55001-FM-AM",
        "source_family": "ISO 41001 facility management and ISO 55001 asset management standards",
        "publisher_authority": "ISO",
        "official_url": "https://www.iso.org/standard/68021.html; https://www.iso.org/standard/55089.html",
        "intended_vitruvius_use": "metadata-only facility management, asset management, maintenance, and operations taxonomy context",
    },
    {
        "source_id": "SRC-IES-LIGHTING-LIBRARY",
        "source_family": "IES Lighting Library and lighting practice standards",
        "publisher_authority": "Illuminating Engineering Society",
        "official_url": "https://www.ies.org/standards/; https://www.ies.org/standards/lighting-library/",
        "intended_vitruvius_use": "metadata-only illumination, emergency lighting, daylighting, photometry, and lighting commissioning taxonomy context",
    },
    {
        "source_id": "SRC-ASCE-SEISMIC-RESILIENCE",
        "source_family": "ASCE 7 / ASCE 41 seismic and resilience reference families",
        "publisher_authority": "ASCE",
        "official_url": "https://www.asce.org/topics/asce-7; https://www.asce.org/publications-and-news/asce-41",
        "intended_vitruvius_use": "metadata-only equipment anchorage, seismic bracing, drift, load, and resilience taxonomy context",
    },
    {
        "source_id": "SRC-FEMA-P58-PUBLICATIONS",
        "source_family": "FEMA P-58 seismic performance assessment publications",
        "publisher_authority": "FEMA",
        "official_url": "https://www.fema.gov/emergency-managers/risk-management/building-science/earthquake/publications",
        "intended_vitruvius_use": "metadata-only seismic performance and recovery taxonomy context",
    },
]

STANDARD_FAMILIES: list[dict[str, Any]] = [
    {
        "path_code": "COM.STD.ASH",
        "label": "ASHRAE Standards",
        "definition": "Metadata-only standards-family node for HVAC, ventilation, energy, thermal comfort, and commissioning references used in AEC-MEPFS taxonomy crosswalks.",
        "aliases": ["ASHRAE", "ASHRAE standards", "HVAC standards"],
        "source_ids": ["SRC-ASHRAE-62-1-90-1-55-CX"],
        "children": [
            ("VNT", "ASHRAE 62.1 Ventilation And IAQ", ["ASHRAE 62.1", "ventilation for acceptable indoor air quality", "IAQ ventilation standard"]),
            ("ENE", "ASHRAE 90.1 Building Energy Standard", ["ASHRAE 90.1", "building energy standard", "energy standard for buildings"]),
            ("THC", "ASHRAE 55 Thermal Comfort Standard", ["ASHRAE 55", "thermal environmental conditions", "thermal comfort standard"]),
            ("CXP", "ASHRAE Commissioning Process", ["ASHRAE Guideline 0", "ASHRAE Standard 202", "commissioning process"]),
            ("EXC", "Existing HVAC Commissioning Guidance", ["existing building commissioning", "HVAC commissioning", "retrocommissioning"]),
        ],
    },
    {
        "path_code": "COM.STD.NFP",
        "label": "NFPA Standards",
        "definition": "Metadata-only standards-family node for electrical safety, life safety, fire suppression, alarms, standpipes, and fire pumps.",
        "aliases": ["NFPA", "National Fire Protection Association", "NFPA code families"],
        "source_ids": ["SRC-NFPA-70-101-13-72-14-20"],
        "children": [
            ("NEC", "NFPA 70 National Electrical Code", ["NEC", "NFPA 70", "National Electrical Code"]),
            ("LSC", "NFPA 101 Life Safety Code", ["NFPA 101", "Life Safety Code", "LSC"]),
            ("SPR", "NFPA 13 Sprinkler Systems", ["NFPA 13", "sprinkler standard", "automatic sprinkler systems"]),
            ("FAL", "NFPA 72 Fire Alarm And Signaling", ["NFPA 72", "fire alarm code", "signaling code"]),
            ("STP", "NFPA 14 Standpipe And Hose Systems", ["NFPA 14", "standpipe standard", "hose systems"]),
        ],
    },
    {
        "path_code": "COM.STD.TIA",
        "label": "TIA And BICSI ICT Standards",
        "definition": "Metadata-only standards-family node for structured cabling, pathways, spaces, bonding, distribution methods, and data-center telecommunications infrastructure.",
        "aliases": ["TIA standards", "BICSI", "ICT infrastructure standards"],
        "source_ids": ["SRC-TIA-BICSI-ICT-INFRASTRUCTURE"],
        "children": [
            ("CAB", "TIA Structured Cabling Standard", ["ANSI/TIA-568", "structured cabling", "commercial building cabling"]),
            ("PAS", "TIA Pathways And Spaces Standard", ["ANSI/TIA-569", "telecommunications pathways", "telecommunications spaces"]),
            ("BON", "Telecommunications Bonding And Grounding Standard", ["TIA-607", "telecom bonding", "telecom grounding"]),
            ("TDM", "BICSI Telecommunications Distribution Methods", ["BICSI TDMM", "telecommunications distribution methods", "ICT design methods"]),
            ("DCT", "Data Center Telecommunications Infrastructure", ["data center cabling", "TIA-942", "data center telecom infrastructure"]),
        ],
    },
    {
        "path_code": "COM.STD.ICC",
        "label": "ICC I-Code Families",
        "definition": "Metadata-only code-family node for international building, plumbing, fire, energy, and existing-building code references.",
        "aliases": ["ICC codes", "I-Codes", "International Code Council"],
        "source_ids": ["SRC-ICC-IBC-IPC-IFC-IECC-IEBC"],
        "children": [
            ("IBC", "International Building Code", ["IBC", "building code", "international building code"]),
            ("IPC", "International Plumbing Code", ["IPC", "plumbing code", "international plumbing code"]),
            ("IFC", "International Fire Code", ["IFC", "fire code", "international fire code"]),
            ("IEC", "International Energy Conservation Code", ["IECC", "energy conservation code", "building energy code"]),
            ("IEB", "International Existing Building Code", ["IEBC", "existing building code", "existing buildings"]),
        ],
    },
    {
        "path_code": "COM.STD.WHO",
        "label": "WHO WASH Guidance",
        "definition": "Metadata-only guidance-family node for water, sanitation, hygiene, sanitation safety planning, and public-health engineering risk management.",
        "aliases": ["WHO WASH", "water sanitation and hygiene", "public health sanitation guidance"],
        "source_ids": ["SRC-WHO-WASH-SANITATION-SAFETY"],
        "children": [
            ("SSP", "Sanitation Safety Planning", ["SSP", "sanitation safety plan", "risk-based sanitation management"]),
            ("WSP", "Water Safety Planning", ["WSP", "water safety plan", "drinking water risk management"]),
            ("SGH", "Guidelines On Sanitation And Health", ["sanitation and health", "safe sanitation", "sanitation health guidelines"]),
            ("WHF", "WASH In Health Care Facilities", ["WASH in HCF", "health care WASH", "health facility sanitation"]),
            ("WST", "Safe Use Of Wastewater And Excreta", ["wastewater reuse safety", "excreta reuse", "greywater safety"]),
        ],
    },
    {
        "path_code": "COM.STD.NIS",
        "label": "NIST Cybersecurity Guidance",
        "definition": "Metadata-only guidance-family node for cybersecurity framework, IoT security baselines, device cybersecurity capabilities, and cyber-physical security controls.",
        "aliases": ["NIST cybersecurity", "NIST CSF", "NIST IoT guidance"],
        "source_ids": ["SRC-NIST-CSF-IOT-CONTROLS"],
        "children": [
            ("CSF", "NIST Cybersecurity Framework", ["NIST CSF", "cybersecurity framework", "govern identify protect detect respond recover"]),
            ("IOT", "IoT Core Baseline", ["NISTIR 8259", "IoT core baseline", "IoT cybersecurity baseline"]),
            ("IDC", "IoT Device Cybersecurity Capability Catalog", ["IoT capability catalog", "device cybersecurity catalog", "IoT controls catalog"]),
            ("SPC", "Security And Privacy Controls", ["NIST SP 800-53", "security controls", "privacy controls"]),
            ("BCS", "Building Control System Cybersecurity", ["BAS cybersecurity", "building controls cybersecurity", "OT security for buildings"]),
        ],
    },
    {
        "path_code": "COM.STD.ICM",
        "label": "ICOMOS Conservation Doctrine",
        "definition": "Metadata-only doctrine-family node for conservation charters, authenticity, structural conservation, interpretation, and historic urban landscape principles.",
        "aliases": ["ICOMOS", "conservation charters", "heritage doctrine"],
        "source_ids": ["SRC-ICOMOS-CONSERVATION-CHARTERS"],
        "children": [
            ("VEN", "Venice Charter Conservation Principles", ["Venice Charter", "monuments and sites conservation", "conservation charter"]),
            ("NAR", "Nara Document On Authenticity", ["Nara Document", "authenticity", "heritage authenticity"]),
            ("STR", "Built Heritage Structural Conservation Principles", ["structural conservation", "heritage structures", "minimum intervention"]),
            ("INT", "Cultural Heritage Interpretation Charter", ["interpretation charter", "heritage presentation", "public interpretation"]),
            ("HUL", "Historic Urban Landscape Principles", ["historic urban landscape", "HUL", "urban heritage landscape"]),
        ],
    },
    {
        "path_code": "COM.STD.IES",
        "label": "IES Lighting Standards",
        "definition": "Metadata-only standards-family node for lighting practice, emergency illumination, daylighting metrics, photometric testing, and lighting commissioning.",
        "aliases": ["IES", "Illuminating Engineering Society", "lighting standards"],
        "source_ids": ["SRC-IES-LIGHTING-LIBRARY"],
        "children": [
            ("LIB", "IES Lighting Library", ["IES Lighting Library", "lighting practice standards", "illumination guidance"]),
            ("EMG", "Emergency Lighting Practice", ["emergency lighting", "egress illumination", "life safety lighting"]),
            ("DYL", "Daylighting Metrics", ["sDA", "ASE", "daylight autonomy"]),
            ("PHO", "Photometric Testing And Data", ["LM-79", "photometric data", "luminaire testing"]),
            ("CXM", "Lighting Commissioning And Maintenance", ["lighting commissioning", "lighting maintenance", "lighting controls acceptance"]),
        ],
    },
]

ISO_STANDARD_CHILDREN = [
    ("LCA", "ISO Life Cycle Assessment Framework", ["ISO 14040", "ISO 14044", "life cycle assessment"], "SRC-ISO-14040-14044-LCA"),
    ("FMS", "ISO Facility Management System Standard", ["ISO 41001", "facility management system", "FM management system"], "SRC-ISO-41001-55001-FM-AM"),
    ("AMS", "ISO Asset Management System Standard", ["ISO 55001", "asset management system", "physical asset management"], "SRC-ISO-41001-55001-FM-AM"),
    ("EMS", "ISO Environmental Management System Standard", ["ISO 14001", "environmental management system", "EMS"], "SRC-ISO-14040-14044-LCA"),
    ("ENM", "ISO Energy Management System Standard", ["ISO 50001", "energy management system", "EnMS"], "SRC-ISO-41001-55001-FM-AM"),
]

DOMAIN_GROUPS: list[dict[str, Any]] = [
    {"parent": "MEC.ACD.CHW", "standard": "COM.STD.ASH.ENE", "source_ids": ["SRC-ASHRAE-62-1-90-1-55-CX"], "topics": [("DTM", "Chilled Water Delta T Management", ["low delta T", "CHW delta T", "temperature differential management"]), ("PSP", "Primary Secondary Pumping", ["primary-secondary pumping", "decoupled pumping", "CHW pumping arrangement"]), ("VPF", "Variable Primary Flow", ["VPF", "variable primary pumping", "variable flow chilled water"]), ("CPS", "Chiller Plant Staging", ["chiller sequencing", "plant staging", "chiller staging logic"])]},
    {"parent": "MEC.VEN.OAI", "standard": "COM.STD.ASH.VNT", "source_ids": ["SRC-ASHRAE-62-1-90-1-55-CX"], "topics": [("DCV", "Demand Controlled Ventilation", ["DCV", "CO2-based ventilation", "occupancy ventilation reset"]), ("ECO", "Economizer Outdoor Air Intake", ["airside economizer", "outdoor air economizer", "free cooling intake"]), ("ICS", "Intake Contaminant Separation", ["outdoor air intake separation", "contaminant source clearance", "intake location"]), ("AFV", "Outdoor Airflow Verification", ["outdoor airflow measurement", "ventilation verification", "OA flow station"])]},
    {"parent": "MEC.CTL.BAS", "standard": "COM.STD.NIS.BCS", "source_ids": ["SRC-ASHRAE-62-1-90-1-55-CX", "SRC-NIST-CSF-IOT-CONTROLS"], "topics": [("BPM", "BACnet Point Mapping", ["BACnet points", "BMS point list", "BAS point mapping"]), ("TLC", "Trend Log Configuration", ["trend logs", "BAS trending", "historian point logging"]), ("APR", "Alarm Prioritization", ["alarm rationalization", "BAS alarms", "operator alarm priority"]), ("OOG", "Operator Override Governance", ["manual override", "BAS override", "operator override log"])]},
    {"parent": "MEC.MCC.FPT", "standard": "COM.STD.ASH.CXP", "source_ids": ["SRC-ASHRAE-62-1-90-1-55-CX"], "topics": [("FTS", "Commissioning Functional Test Scripts", ["FPT scripts", "functional test procedure", "commissioning script"]), ("SCV", "Sensor Calibration Verification", ["sensor calibration", "calibration check", "instrument verification"]), ("TDC", "TAB Deficiency Closure", ["TAB punch list", "balancing deficiency", "testing adjusting balancing closure"]), ("STP", "Seasonal Testing Plan", ["seasonal commissioning", "deferred seasonal test", "opposite season test"])]},
    {"parent": "ELE.PDS.TRS", "standard": "COM.STD.NFP.NEC", "source_ids": ["SRC-NFPA-70-101-13-72-14-20"], "topics": [("SCS", "Selective Coordination Study", ["selective coordination", "coordination study", "protective device coordination"]), ("SCD", "Short Circuit Duty Verification", ["short-circuit current", "interrupting rating", "fault current verification"]), ("AFL", "Arc Flash Labeling", ["arc flash label", "incident energy label", "NFPA 70E label"]), ("SMC", "Switchgear Maintenance Clearance", ["electrical working clearance", "switchgear access", "maintenance clearance"])]},
    {"parent": "ELE.GRD.GES", "standard": "COM.STD.NFP.NEC", "source_ids": ["SRC-NFPA-70-101-13-72-14-20"], "topics": [("GRE", "Ground Ring Electrode", ["ground ring", "grounding electrode", "ring electrode"]), ("UFE", "Concrete Encased Electrode", ["Ufer ground", "concrete-encased electrode", "foundation grounding electrode"]), ("GRT", "Ground Resistance Testing", ["earth resistance test", "fall-of-potential test", "ground test"]), ("TBB", "Telecommunications Bonding Backbone", ["TBB", "telecom bonding backbone", "ICT bonding backbone"])]},
    {"parent": "ELE.EPW.GEN", "standard": "COM.STD.NFP.NEC", "source_ids": ["SRC-NFPA-70-101-13-72-14-20"], "topics": [("LDS", "Emergency Generator Load Step", ["load step", "generator transient response", "genset load acceptance"]), ("FSA", "Fuel Supply Autonomy", ["fuel runtime", "fuel storage autonomy", "emergency generator fuel supply"]), ("ANN", "Generator Annunciator Interface", ["remote annunciator", "generator alarm panel", "genset annunciation"]), ("EXR", "Generator Exhaust Routing", ["generator exhaust", "engine exhaust routing", "exhaust discharge coordination"])]},
    {"parent": "ELE.LVC.STC", "standard": "COM.STD.TIA.CAB", "source_ids": ["SRC-TIA-BICSI-ICT-INFRASTRUCTURE"], "topics": [("HCC", "Horizontal Cabling Channel", ["horizontal cabling", "permanent link", "telecom outlet channel"]), ("TRS", "Telecommunications Room Sizing", ["TR sizing", "telecom room", "IDF room sizing"]), ("BFR", "Backbone Fiber Routing", ["fiber backbone", "riser fiber", "campus backbone cabling"]), ("CPF", "Cable Pathway Firestopping", ["firestop sleeve", "cable penetration firestop", "pathway firestopping"])]},
    {"parent": "FLS.FDA.FAC", "standard": "COM.STD.NFP.FAL", "source_ids": ["SRC-NFPA-70-101-13-72-14-20"], "topics": [("ALC", "Addressable Loop Capacity", ["SLC capacity", "addressable loop", "signaling line circuit capacity"]), ("ICS", "Initiating Circuit Supervision", ["IDC supervision", "initiating device circuit", "circuit supervision"]), ("BSC", "Battery Standby Calculation", ["battery calc", "standby battery", "fire alarm battery sizing"]), ("SMX", "Fire Alarm Sequence Matrix", ["cause and effect matrix", "fire alarm matrix", "sequence of operations"])]},
    {"parent": "FLS.FPR.SPR", "standard": "COM.STD.NFP.SPR", "source_ids": ["SRC-NFPA-70-101-13-72-14-20"], "topics": [("HCA", "Hydraulic Calculation Area", ["hydraulic remote area", "sprinkler calculation area", "remote design area"]), ("HTR", "Sprinkler Head Temperature Rating", ["temperature rating", "sprinkler thermal element", "head rating"]), ("WFS", "Waterflow Switch Interface", ["waterflow switch", "sprinkler alarm interface", "flow switch"]), ("ITC", "Inspector Test Connection", ["inspector test", "ITC", "test and drain connection"])]},
    {"parent": "FLS.SMK.SCO", "standard": "COM.STD.ASH.CXP", "source_ids": ["SRC-NFPA-70-101-13-72-14-20", "SRC-ASHRAE-62-1-90-1-55-CX"], "topics": [("SRA", "Smoke Control Rational Analysis", ["rational analysis", "smoke control report", "smoke management analysis"]), ("SPI", "Smoke Control Special Inspection", ["special inspection", "smoke control acceptance", "system verification"]), ("FSP", "Fan Status Proof", ["fan proof", "airflow proving", "status feedback"]), ("FCP", "Firefighter Smoke Control Panel", ["FSCP", "smoke control panel", "firefighter control panel"])]},
    {"parent": "FLS.EGR.EXI", "standard": "COM.STD.NFP.LSC", "source_ids": ["SRC-NFPA-70-101-13-72-14-20", "SRC-ICC-IBC-IPC-IFC-IECC-IEBC"], "topics": [("EDC", "Exit Discharge Continuity", ["exit discharge", "egress discharge", "public way continuity"]), ("DHC", "Exit Door Hardware Coordination", ["panic hardware", "door hardware", "egress door hardware"]), ("ESV", "Exit Sign Visibility", ["exit sign", "directional exit sign", "egress signage"]), ("ECA", "Exit Capacity Aggregation", ["exit capacity", "egress capacity", "capacity aggregation"])]},
    {"parent": "PLS.PWS.BAP", "standard": "COM.STD.ICC.IPC", "source_ids": ["SRC-ICC-IBC-IPC-IFC-IECC-IEBC"], "topics": [("RPZ", "Reduced Pressure Zone Assembly", ["RPZ", "RP assembly", "reduced pressure backflow preventer"]), ("DCA", "Double Check Valve Assembly", ["DCVA", "double check assembly", "double-check backflow preventer"]), ("TPA", "Backflow Test Port Access", ["test cocks", "backflow test access", "test port clearance"]), ("CCS", "Cross Connection Survey", ["cross-connection survey", "hazard survey", "backflow hazard assessment"])]},
    {"parent": "PLS.SAN.VST", "standard": "COM.STD.ICC.IPC", "source_ids": ["SRC-ICC-IBC-IPC-IFC-IECC-IEBC"], "topics": [("VSZ", "Vent Stack Sizing", ["vent sizing", "stack vent sizing", "vent pipe sizing"]), ("RVC", "Relief Vent Coordination", ["relief vent", "circuit vent relief", "vent relief coordination"]), ("VTL", "Vent Terminal Location", ["vent termination", "roof vent terminal", "vent outlet location"]), ("TSP", "Trap Seal Protection", ["trap seal", "trap primer", "siphonage protection"])]},
    {"parent": "SAN.PHE.HRC", "standard": "COM.STD.WHO.SSP", "source_ids": ["SRC-WHO-WASH-SANITATION-SAFETY"], "topics": [("HSP", "Hand Hygiene Station Placement", ["handwashing station", "hand hygiene", "wash basin placement"]), ("SBP", "Sanitation Barrier Planning", ["sanitary barrier", "pathogen barrier", "contamination barrier"]), ("PER", "Pathogen Exposure Route Mapping", ["exposure route", "pathogen pathway", "fecal exposure pathway"]), ("PHI", "Public Health Inspection Checklist", ["health inspection", "sanitation checklist", "public health checklist"])]},
    {"parent": "SAN.WSS.CCC", "standard": "COM.STD.WHO.WSP", "source_ids": ["SRC-WHO-WASH-SANITATION-SAFETY", "SRC-ICC-IBC-IPC-IFC-IECC-IEBC"], "topics": [("PNS", "Potable Nonpotable Separation", ["potable separation", "nonpotable separation", "water system separation"]), ("CHR", "Cross Connection Hazard Rating", ["hazard rating", "cross-connection risk", "backflow hazard class"]), ("AGV", "Air Gap Verification", ["air gap", "physical separation", "air gap check"]), ("BPR", "Backflow Program Records", ["backflow records", "test record", "backflow prevention program"])]},
    {"parent": "SEC.ACS.CRT", "standard": "COM.STD.NIS.CSF", "source_ids": ["SRC-NIST-CSF-IOT-CONTROLS"], "topics": [("SCC", "Smart Card Credential", ["smart card", "contactless credential", "card credential"]), ("MCP", "Mobile Credential Provisioning", ["mobile credential", "phone credential", "digital access pass"]), ("BTG", "Biometric Template Governance", ["biometric template", "biometric privacy", "template protection"]), ("CRW", "Credential Revocation Workflow", ["credential revocation", "badge deactivation", "access rights removal"])]},
    {"parent": "SEC.VSS.VIA", "standard": "COM.STD.NIS.CSF", "source_ids": ["SRC-NIST-CSF-IOT-CONTROLS"], "topics": [("PDA", "Person Detection Analytics", ["person detection", "object detection", "video analytics rule"]), ("LDR", "Loitering Detection Rules", ["loitering detection", "dwell rule", "behavior analytics"]), ("LPR", "License Plate Recognition Governance", ["LPR", "ANPR", "plate recognition governance"]), ("FAT", "Analytics False Alarm Tuning", ["false alarm tuning", "analytics calibration", "event threshold tuning"])]},
    {"parent": "SMS.IOT.DIX", "standard": "COM.STD.NIS.IOT", "source_ids": ["SRC-NIST-CSF-IOT-CONTROLS"], "topics": [("DCE", "Device Certificate Enrollment", ["device certificate", "PKI enrollment", "certificate provisioning"]), ("SBA", "Secure Boot Attestation", ["secure boot", "device attestation", "firmware integrity"]), ("IAI", "IoT Asset Inventory", ["IoT inventory", "connected device register", "device asset inventory"]), ("DDP", "Device Decommissioning Proof", ["device retirement", "decommissioning evidence", "secure disposal proof"])]},
    {"parent": "HRC.PRN.MIX", "standard": "COM.STD.ICM.STR", "source_ids": ["SRC-ICOMOS-CONSERVATION-CHARTERS"], "topics": [("RFS", "Reversible Fixing Strategy", ["reversible fixing", "reversible attachment", "non-destructive fixing"]), ("LFR", "Like For Like Repair Assessment", ["like-for-like repair", "matching repair", "material replacement assessment"]), ("IIL", "Intervention Impact Log", ["intervention log", "impact record", "conservation intervention record"]), ("CMR", "Conservation Mockup Review", ["conservation mockup", "trial repair", "sample panel review"])]},
    {"parent": "SUS.CAR.LCA", "standard": "COM.STD.ISO.LCA", "source_ids": ["SRC-ISO-14040-14044-LCA"], "topics": [("GSD", "Goal And Scope Definition", ["LCA goal and scope", "functional unit", "system boundary"]), ("LCI", "Life Cycle Inventory Dataset", ["LCI", "inventory data", "life cycle inventory"]), ("ICS", "Impact Category Selection", ["LCIA categories", "impact categories", "life cycle impact assessment"]), ("CRS", "Critical Review Statement", ["critical review", "third-party LCA review", "review statement"])]},
    {"parent": "OPS.AST.AIM", "standard": "COM.STD.ISO.FMS", "source_ids": ["SRC-ISO-41001-55001-FM-AM"], "topics": [("MAN", "Maintainable Asset Naming", ["asset naming", "maintainable asset", "asset tag naming"]), ("WDC", "Warranty Data Capture", ["warranty data", "warranty register", "defects liability data"]), ("CBM", "COBie Handover Mapping", ["COBie", "asset data handover", "COBie mapping"]), ("ACC", "Asset Criticality Classification", ["asset criticality", "critical asset", "criticality ranking"])]},
]

STANDARD_DOMAIN_TARGETS: dict[str, str] = {
    "COM.STD.ASH": "MEC",
    "COM.STD.NFP": "FLS",
    "COM.STD.TIA": "ELE.LVC",
    "COM.STD.ICC": "COM",
    "COM.STD.WHO": "SAN",
    "COM.STD.NIS": "SMS",
    "COM.STD.ICM": "HRC",
    "COM.STD.IES": "ELE.LGT",
    "COM.STD.ISO": "SUS",
}


def enrich(payload: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    records = [dict(record) for record in payload["records"]]
    relationships = [dict(relationship) for relationship in payload["relationships"]]
    path_to_record = {record["path_code"]: record for record in records if record.get("path_code")}
    id_to_record = {record["id"]: record for record in records if record.get("id")}
    existing_edges = {
        (relationship.get("from_id"), relationship.get("predicate"), relationship.get("to_id"))
        for relationship in relationships
    }
    next_id = _next_domain_id(records)
    added_nodes: list[dict[str, Any]] = []
    improved_nodes: set[str] = set()
    added_relationships: list[dict[str, Any]] = []
    aliases_added = 0

    def add_node(
        *,
        path_code: str,
        label: str,
        level: int,
        parent_path_code: str,
        definition: str,
        aliases: list[str],
        source_ids: list[str],
        standard_target: str | None = None,
        node_kind: str,
    ) -> dict[str, Any]:
        nonlocal next_id, aliases_added
        existing = path_to_record.get(path_code)
        if existing is not None:
            added_aliases = _merge_metadata(existing, aliases, source_ids, node_kind)
            aliases_added += added_aliases
            if added_aliases:
                improved_nodes.add(path_code)
            return existing
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
            "provenance_note": "Kimi-guided, human-integrated metadata-only taxonomy enrichment; no standards clauses or protected source text stored.",
            "confidence": "high",
            "quality_signal": "curated_public_reference_taxonomy",
            "semantic_node_kind": node_kind,
        }
        if standard_target:
            record["standard_target_path_code"] = standard_target
        records.append(record)
        path_to_record[path_code] = record
        id_to_record[node_id] = record
        added_nodes.append(record)
        aliases_added += len(full_aliases)
        _add_edge(parent["id"], "broader_than", node_id)
        return record

    def _add_edge(from_id: str, predicate: str, to_id: str) -> None:
        edge = (from_id, predicate, to_id)
        if edge in existing_edges:
            return
        relationship = {
            "from_id": from_id,
            "predicate": predicate,
            "to_id": to_id,
            "governed": True,
            "generation_method": GENERATION_METHOD,
            "provenance_note": "Curated semantic relationship added during targeted public-taxonomy enrichment.",
        }
        relationships.append(relationship)
        added_relationships.append(relationship)
        existing_edges.add(edge)

    for family in STANDARD_FAMILIES:
        parent = add_node(
            path_code=family["path_code"],
            label=family["label"],
            level=3,
            parent_path_code="COM.STD",
            definition=family["definition"],
            aliases=family["aliases"],
            source_ids=family["source_ids"],
            node_kind="standard_family",
        )
        target = STANDARD_DOMAIN_TARGETS[family["path_code"]]
        if target in path_to_record:
            _add_edge(parent["id"], "has_facet", path_to_record[target]["id"])
        for suffix, label, aliases in family["children"]:
            child = add_node(
                path_code=f"{family['path_code']}.{suffix}",
                label=label,
                level=4,
                parent_path_code=family["path_code"],
                definition=f"Metadata-only reference node for {label}, used to connect AEC-MEPFS topics to a public standards-family label without storing standard text.",
                aliases=aliases,
                source_ids=family["source_ids"],
                node_kind="standard_reference",
            )
            _add_edge(child["id"], "part_of", parent["id"])
            if target in path_to_record:
                _add_edge(child["id"], "constrains", path_to_record[target]["id"])

    iso_parent = path_to_record["COM.STD.ISO"]
    added_aliases = _merge_metadata(
        iso_parent,
        ["ISO standards", "international standards", "ISO reference families"],
        ["SRC-ISO-14040-14044-LCA", "SRC-ISO-41001-55001-FM-AM"],
        "standard_family",
    )
    aliases_added += added_aliases
    if added_aliases:
        improved_nodes.add("COM.STD.ISO")
    for suffix, label, aliases, source_id in ISO_STANDARD_CHILDREN:
        child = add_node(
            path_code=f"COM.STD.ISO.{suffix}",
            label=label,
            level=4,
            parent_path_code="COM.STD.ISO",
            definition=f"Metadata-only ISO reference node for {label}, used for sustainability, operations, and asset-management taxonomy crosswalks without storing standards text.",
            aliases=aliases,
            source_ids=[source_id],
            node_kind="standard_reference",
        )
        _add_edge(child["id"], "part_of", iso_parent["id"])
        target = "OPS" if source_id == "SRC-ISO-41001-55001-FM-AM" else "SUS"
        _add_edge(child["id"], "constrains", path_to_record[target]["id"])

    for group in DOMAIN_GROUPS:
        parent = path_to_record[group["parent"]]
        added_aliases = _merge_metadata(
            parent,
            [f"curated {parent['label'].lower()}", f"{parent['path_code']} curated topic parent"],
            group["source_ids"],
            "curated_parent",
        )
        aliases_added += added_aliases
        if added_aliases:
            improved_nodes.add(group["parent"])
        standard = path_to_record[group["standard"]]
        for suffix, label, aliases in group["topics"]:
            child = add_node(
                path_code=f"{group['parent']}.{suffix}",
                label=label,
                level=4,
                parent_path_code=group["parent"],
                definition=(
                    f"Curated {group['parent'].split('.')[0]} topic covering {label.lower()} decisions, "
                    f"coordination checks, acceptance evidence, and metadata under {parent['label']}."
                ),
                aliases=aliases,
                source_ids=group["source_ids"],
                standard_target=group["standard"],
                node_kind="discipline_topic",
            )
            _add_edge(child["id"], "maps_to_external_standard", standard["id"])
            _add_edge(child["id"], "requires", parent["id"])

    new_payload = {**payload, "records": records, "relationships": relationships}
    hierarchy_added = [edge for edge in added_relationships if edge["predicate"] == "broader_than"]
    semantic_added = [edge for edge in added_relationships if edge["predicate"] != "broader_than"]
    root_counts = Counter(record["path_code"].split(".")[0] for record in added_nodes)
    report = {
        "ok": True,
        "generation_method": GENERATION_METHOD,
        "input_record_count": len(payload["records"]),
        "output_record_count": len(records),
        "input_relationship_count": len(payload["relationships"]),
        "output_relationship_count": len(relationships),
        "added_node_count": len(added_nodes),
        "added_standard_family_l3_count": sum(1 for record in added_nodes if record.get("semantic_node_kind") == "standard_family"),
        "added_standard_reference_l4_count": sum(1 for record in added_nodes if record.get("semantic_node_kind") == "standard_reference"),
        "added_discipline_topic_l4_count": sum(1 for record in added_nodes if record.get("semantic_node_kind") == "discipline_topic"),
        "improved_existing_node_count": len(improved_nodes),
        "added_relationship_count": len(added_relationships),
        "added_hierarchy_relationship_count": len(hierarchy_added),
        "added_semantic_relationship_count": len(semantic_added),
        "aliases_added_or_preserved_on_new_and_improved_nodes": aliases_added,
        "added_nodes_by_root": dict(sorted(root_counts.items())),
        "semantic_relationships_by_predicate": dict(sorted(Counter(edge["predicate"] for edge in semantic_added).items())),
        "sample_added_path_codes": [record["path_code"] for record in added_nodes[:60]],
        "source_reference_ids": [row["source_id"] for row in SOURCE_REFERENCES],
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
            "blocking_notes": "content ingest blocked until explicit license/legal review; this enrichment uses metadata-only topic labels",
        }
        rows.append(row)
        added.append(row)
        existing.add(reference["source_id"])
    new_payload = {**payload, "source_rights_registry": rows}
    return new_payload, {
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


def _next_domain_id(records: list[dict[str, Any]]) -> int:
    return max(int(record["id"].split("-")[-1]) for record in records if str(record.get("id", "")).startswith("VTN-DOM-")) + 1


def _merge_metadata(record: dict[str, Any], aliases: list[str], source_ids: list[str], node_kind: str) -> int:
    alias_count = _merge_list(record, "aliases", aliases)
    _merge_list(record, "source_family_ids", source_ids)
    record.setdefault("provenance_note", "Metadata-only taxonomy enrichment; no protected source payload stored.")
    record.setdefault("quality_signal", "curated_public_reference_taxonomy")
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
    parser = argparse.ArgumentParser(description="Add targeted, Kimi-guided, source-backed AEC-MEPFS taxonomy enrichment.")
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
