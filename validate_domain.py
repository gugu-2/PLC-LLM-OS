#!/usr/bin/env python3
"""
validate_domain.py — Stage 1 Domain Triage for Lumina PLC-LLM Corpus
Reference: DOC-01, DOC-02, DOC-05

Validates that Function Blocks belong strictly to sanctioned commercial manufacturing sectors:
- Automotive & Commercial Vehicles
- Electronics & PCB Assembly
- Semiconductor Packaging
- Heavy Machinery & CNC / Press Tooling
- Plastics & Polymer Processing
- Food & Beverage Processing & Packaging
- Metallurgy & Strip Steelmaking

Rejects contaminating domains (Marine, Subsea, Pharma, Defense, Oil/Gas, Power Gen, Mining).
"""

import os
import sys
import json
import re
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple

SANCTIONED_SECTORS = {
    "automotive": [
        "Automotive", "BIW", "BodyInWhite", "PaintBooth", "BellAtomizer", "RollerHemming",
        "SpotWeld", "LaserWeld", "StirWeld", "EngineAssembly", "ColdTest",
        "DynoTest", "GigaCast", "HPDC", "EV", "Battery", "Hairpin",
        "TruckFrame", "MIG", "TIG", "SeamWeld", "GlassEncapsulation",
        "DoorHinge", "Powertrain", "Transmission", "Differential", "Axle",
        "Chassis", "Stator", "Rotor", "CellToPack", "Busbar"
    ],
    "electronics": [
        "Electronics", "SMT", "PickPlace", "Reflow", "ReflowOven", "SolderPaste", "AOI",
        "AXI", "ScreenPrinter", "StagingConveyor", "WaveSolder", "SelectiveSolder",
        "ComponentPlacement", "Feeder", "NozzleChanger", "PCBA", "InspectionVision",
        "MoireAOI", "TapeAndReel"
    ],
    "semiconductor": [
        "Semiconductor", "WireBond", "DieBond", "DieAttach", "FOWLP", "Fan_Out", "WaferLevel",
        "Flip_Chip", "BGA", "Underfill", "Encapsulant", "CleanroomHVAC", "HEPA",
        "FFU", "CMP", "EtchChamber", "PVD", "CVD", "ALD", "SiC", "GaN",
        "WaferHandling", "WaferDicing", "LeadFrame", "MoldingPress", "CuPillar"
    ],
    "heavy_machinery": [
        "HeavyMachinery", "Machinery", "StampingPress", "ProgressiveDie", "TransferDie", "Hydraulic", "ServoPress",
        "ForgePress", "Forging", "GearGrinding", "HobMachine", "Hobbing", "Broach",
        "Broaching", "CNC", "MachiningCenter", "FiveAxis", "5Axis", "GantryMill",
        "DeepHole", "GunDrill", "Honing", "Lapping", "JigBore", "CoordinateMeasure",
        "DieCasting", "ColdForging", "HotForging"
    ],
    "plastics": [
        "Plastics", "Polymer", "InjectionMolding", "IMMC", "CavityPressure", "VtoP", "HotRunner",
        "Extrusion", "TwinScrew", "BlowMolding", "EBM", "IBM", "ISBM",
        "Thermoform", "CastFilm", "BiaxialStretch", "PET", "HDPE", "PP",
        "PVC", "ABS", "Nylon", "Polycarbonate", "Overmold", "ParisonControl"
    ],
    "foodbev": [
        "FoodBev", "Food", "Beverage", "Bottling", "Filler", "Capper", "Labeler", "Pasteurizer", "UHT",
        "CIP", "SIP", "Retort", "Autoclave", "CanSeamer", "Sterilizer",
        "Homogenizer", "Evaporator", "Crystallizer", "Dryer", "SprayDryer",
        "FreezeDry", "AsepticFill", "BlowFill", "PAA", "Peracetic",
        "ConveyorSort", "CaseCarton", "DeltaRobot", "PalletWrapper", "RotaryFiller"
    ],
    "steelmaking": [
        "Steelmaking", "SteelMill", "ColdMill", "HotMill", "TandemMill", "ReversingMill", "Galvanizing",
        "Pickling", "Annealing", "SkinPass", "TensionLevel", "TemperMill",
        "Coiler", "Decoiler", "Slitter", "CutToLength", "EAF", "ElectricArcFurnace",
        "LadleFurnace", "Tundish", "ContinuousCaster", "Caster", "RollForce",
        "AGC", "AFC", "FlatnessMeter", "XRayGauge"
    ]
}

FORBIDDEN_DOMAINS = {
    "marine": [
        "Sonar", "Submarine", "Vessel", "Ship", "Hull", "Propulsion",
        "BallastWater", "Bilge", "SeaWater", "Offshore", "Marine",
        "Subsea", "ROV", "AUV", "FPSO", "Mooring", "Anchor", "Maritime"
    ],
    "pharmaceutical": [
        "Pharma", "Pharmaceutical", "Lyophilizer", "Lyophilization", "Bioreactor", "Fermenter",
        "ChromatographyColumn", "VialFiller_Pharma", "SyringeFiller",
        "PharmaCleanroom", "ActivePharmaceutical", "WFI_Loop", "CleanSteam"
    ],
    "defense": [
        "Defense", "Military", "Weapon", "Missile", "Torpedo", "RadarSystem", "Sonar_Defense",
        "Munition", "Artillery", "Warhead", "Ballistic", "DefenseSystem",
        "MilitarySpec", "ITAR"
    ],
    "oil_gas": [
        "OilGas", "Petrochemical", "Petrochem", "Wellhead", "SubseaManifold", "FPSO_OilGas", "CrudeOilPipeline",
        "OilSeparator", "GasTreater", "LNG_Terminal", "CNG_Compressor",
        "Fracking", "MudPump", "BlowoutPreventer", "BOP_Control", "FlareStack", "GOSP"
    ],
    "power_generation": [
        "PowerGeneration", "PowerGrid", "NuclearReactor", "TurbineGenerator_Power", "SteamTurbine_Power",
        "GasTurbine_Power", "HRSG_Boiler", "BoilerFeedwater", "GridSynchronizer",
        "HydroelectricTurbine", "WindTurbinePitch"
    ],
    "mining": [
        "Mining", "OreCrusher", "BallMill_Mining", "SAGMill", "FloatationCell",
        "TailingThickener", "SlurryPipeline", "BucketWheelExcavator",
        "MineDragline", "UndergroundMineHoist"
    ],
    "datacenter": [
        "DataCenter", "DataCenterCRAC", "ServerRackCooling", "ChillerPlant_DataCenter", "CRAH"
    ]
}

def extract_fb_name(content: str) -> str:
    """Extract FUNCTION_BLOCK identifier from ST text."""
    match = re.search(r'\bFUNCTION_BLOCK\s+(FB_\w+)', content, re.IGNORECASE)
    if match:
        return match.group(1)
    match2 = re.search(r'\bFUNCTION_BLOCK\s+(\w+)', content, re.IGNORECASE)
    return match2.group(1) if match2 else "FB_UNKNOWN"

def check_no_forbidden_keywords(content: str, fb_name: str = "") -> List[str]:
    """Scan content and FB name for non-sanctioned domain keywords."""
    hits = []
    scan_text = f"{fb_name} {content[:8000]}"
    normalized_scan = re.sub(r'[_]+', ' ', scan_text)
    for domain, kws in FORBIDDEN_DOMAINS.items():
        for kw in kws:
            pattern = rf'\b{re.escape(kw)}\b'
            if re.search(pattern, scan_text, re.IGNORECASE) or re.search(pattern, normalized_scan, re.IGNORECASE):
                hits.append(f"{domain}::{kw}")
    return hits

def verify_manufacturing_domain(fb_name: str, content: str) -> Tuple[Optional[str], List[str]]:
    """Determine matching manufacturing sector."""
    scan_text = f"{fb_name} {content[:10000]}"
    normalized_fb = re.sub(r'[_]+', ' ', fb_name)
    normalized_scan = re.sub(r'[_]+', ' ', scan_text)
    matched_sector = None
    all_hits = []
    
    # Priority check: FB name first
    for sector, kws in SANCTIONED_SECTORS.items():
        for kw in kws:
            pattern = r'\bABS\b(?!\s*\()' if kw == "ABS" else rf'\b{re.escape(kw)}\b'
            if re.search(pattern, fb_name, re.IGNORECASE) or re.search(pattern, normalized_fb, re.IGNORECASE):
                matched_sector = sector
                all_hits.append(f"{sector}::{kw}")
                break
        if matched_sector:
            break

    # If FB name didn't match, check content head
    if not matched_sector:
        for sector, kws in SANCTIONED_SECTORS.items():
            for kw in kws:
                pattern = r'\bABS\b(?!\s*\()' if kw == "ABS" else rf'\b{re.escape(kw)}\b'
                if re.search(pattern, scan_text, re.IGNORECASE) or re.search(pattern, normalized_scan, re.IGNORECASE):
                    matched_sector = sector
                    all_hits.append(f"{sector}::{kw}")
                    break
            if matched_sector:
                break

    return matched_sector, all_hits

def classify_dataset(fb_name: str, content: str) -> Dict:
    """
    Classify a dataset:
    Returns dict with verdict: PASS | REJECT | AMBIGUOUS
    """
    forbidden_hits = check_no_forbidden_keywords(content, fb_name)
    matched_sector, sanctioned_hits = verify_manufacturing_domain(fb_name, content)
    
    if forbidden_hits:
        verdict = "REJECT"
        forbidden_domain = forbidden_hits[0].split("::")[0]
    elif matched_sector:
        verdict = "PASS"
        forbidden_domain = None
    else:
        verdict = "AMBIGUOUS"
        forbidden_domain = None
        
    return {
        "verdict": verdict,
        "matched_sector": matched_sector,
        "forbidden_domain": forbidden_domain,
        "sanctioned_hits": sanctioned_hits,
        "forbidden_hits": forbidden_hits
    }

def validate_domain_content(content: str) -> Dict:
    """Convenience helper to extract FB name and classify directly from content."""
    fb_name = extract_fb_name(content)
    res = classify_dataset(fb_name, content)
    res["fb_name"] = fb_name
    return res

def validate_domain_file(filepath: Path) -> Dict:
    """Validate a single JSON or ST file."""
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        if filepath.suffix.lower() == ".json":
            try:
                data = json.load(f)
                content = ""
                for msg in data.get("messages", []):
                    if msg.get("role") == "assistant":
                        content = msg.get("content", "")
                        break
            except Exception as e:
                return {
                    "file": str(filepath),
                    "verdict": "REJECT",
                    "reason": f"Corrupt JSON: {e}",
                    "matched_sector": None,
                    "forbidden_domain": None,
                    "sanctioned_hits": [],
                    "forbidden_hits": []
                }
        else:
            content = f.read()

    fb_name = extract_fb_name(content)
    result = classify_dataset(fb_name, content)
    result["file"] = str(filepath)
    result["fb_name"] = fb_name
    result["char_count"] = len(content)
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lumina Domain Triage Validator")
    parser.add_argument("input_path", nargs="?", default="data/swarm_raw", help="Path to file or directory")
    parser.add_argument("--report", default="reports/domain_triage_report.json", help="Path for JSON summary report")
    parser.add_argument("--summary", action="store_true", help="Print summary counts only")
    args = parser.parse_args()

    input_p = Path(args.input_path)
    if not input_p.exists():
        print(f"Error: Path {input_p} does not exist.")
        sys.exit(1)

    if input_p.is_file():
        res = validate_domain_file(input_p)
        print(json.dumps(res, indent=2))
        sys.exit(0 if res["verdict"] == "PASS" else 1)

    # Directory scan
    json_files = list(input_p.glob("*.json"))
    print(f"Scanning {len(json_files)} datasets in {input_p}...")
    results = {"PASS": [], "REJECT": [], "AMBIGUOUS": []}
    sector_counts = {}

    for fp in json_files:
        r = validate_domain_file(fp)
        verdict = r["verdict"]
        results[verdict].append(r)
        if verdict == "PASS" and r["matched_sector"]:
            sec = r["matched_sector"]
            sector_counts[sec] = sector_counts.get(sec, 0) + 1

    summary = {
        "total_scanned": len(json_files),
        "pass_count": len(results["PASS"]),
        "reject_count": len(results["REJECT"]),
        "ambiguous_count": len(results["AMBIGUOUS"]),
        "pass_rate_pct": round(len(results["PASS"]) / max(1, len(json_files)) * 100, 2),
        "sector_distribution": sector_counts
    }

    print("\n--- DOMAIN TRIAGE SUMMARY ---")
    print(f"Total Scanned: {summary['total_scanned']}")
    print(f"PASS (Approved Manufacturing): {summary['pass_count']} ({summary['pass_rate_pct']}%)")
    print(f"REJECT (Off-Target / Forbidden): {summary['reject_count']}")
    print(f"AMBIGUOUS (Needs Review): {summary['ambiguous_count']}")
    print(f"Sector Distribution: {json.dumps(sector_counts, indent=2)}")

    if args.report:
        rep_p = Path(args.report)
        rep_p.parent.mkdir(parents=True, exist_ok=True)
        with open(rep_p, "w", encoding="utf-8") as rf:
            json.dump({"summary": summary, "results": results}, rf, indent=2)
        print(f"Detailed report saved to {rep_p}")
