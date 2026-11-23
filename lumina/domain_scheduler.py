#!/usr/bin/env python3
"""
lumina/domain_scheduler.py — Domain Rotation & Sector Quota Scheduler
Reference: DOC-02, DOC-03

Maintains balanced distribution of heavy manufacturing sectors:
- Automotive (25%): BIW Spot Weld, Bell Atomizer Paint, Laser Busbar, GigaCast HPDC, Engine Cold Test
- Heavy Machinery (20%): 3500T Hydraulic/Servo Press, 5-Axis Gantry Mill, CNC Gear Grinding, Forging
- Electronics (15%): High-Speed SMT Pick & Place, 12-Zone Reflow Soldering, 3D Moire AOI, Selective Solder
- Semiconductor (15%): Thermosonic Wire Bond, FOWLP D2W Die Attach, Underfill Dispense, Cleanroom FFU
- Plastics (10%): 1200T Injection Molding, Twin-Screw Extrusion, Parison Control Blow Molding, Cast Film
- Food & Beverage (10%): Rotary Aseptic Can Seamer, HTST Pasteurizer, CIP/SIP Caustic Loop, Retort Autoclave
- Steelmaking (5%): 6-High Cold Mill AFC, Continuous Strip Galvanizing, Pickling Line, EAF Melt Control
"""

import random
from typing import Dict, List, Optional, Tuple

SECTOR_SYSTEM_CATALOG = {
    "automotive": [
        ("BIW_LaserWeld", "Robotic Body-in-White Seam & Spot Laser Welding Station"),
        ("PaintBooth_RotaryBell", "Automated Paint Booth High-Speed Bell Atomizer with Electrostatic Shroud"),
        ("EV_Busbar_LaserWeld", "Electric Vehicle Battery Pack Cell-to-Pack Laser Busbar Welding"),
        ("GigaCast_4500T_HPDC", "4,500-Ton High Pressure Die Casting Aluminum Chassis Subframe Cell"),
        ("Engine_Dyno_ColdTest", "Automotive Powertrain Cold-Test Dynamometer Friction & Compression Profiler"),
        ("Chassis_RollerHemming", "Multi-Axis Robotic Roller Hemming for Aluminum Door & Hood Panels")
    ],
    "heavy_machinery": [
        ("ServoPress_2500T", "2,500-Ton Multi-Axis Servo Stamping Press with Electronic Die Cushion"),
        ("CNC_FiveAxis_GantryMill", "5-Axis Gantry CNC Machining Center with Active Thermal Spindle Compensation"),
        ("GearGrinding_ContinuousWorm", "Continuous Generating Gear Grinding Machine with Dynamic In-Process Balancer"),
        ("ForgePress_15000T", "15,000-Ton Closed-Die Hydraulic Forging Press with Pre-Fill Valve Sequence"),
        ("DeepHole_GunDrill", "Multi-Spindle Deep Hole Gun Drilling Machine with High-Pressure Coolant AFC")
    ],
    "electronics": [
        ("SMT_DualGantry_PickPlace", "Dual-Gantry High-Speed SMT Placement Machine (100,000 cph) with Feeder AGC"),
        ("ReflowOven_12Zone_Vacuum", "12-Zone Convection Reflow Soldering Oven with Nitrogen Inerting & Vacuum De-Voiding"),
        ("AOI_3D_MoireInspection", "3D Moire Vision Inspection Conveyor Collation & Sorting Cell"),
        ("SelectiveSolder_MultiNozzle", "Multi-Nozzle Selective Wave Soldering Unit for High-Reliability PCBA")
    ],
    "semiconductor": [
        ("WireBond_Thermosonic_HighSpeed", "High-Speed Thermosonic Gold/Copper Wire Bonder with Real-Time EFO Spark Gap"),
        ("FOWLP_D2W_HybridBonding", "Fan-Out Wafer-Level Packaging Die-to-Wafer Direct Hybrid Bonding System"),
        ("Cleanroom_HEPA_FFU_Control", "ISO Class 3 Semiconductor Cleanroom HVAC FFU Pressure Cascading & Recirculation"),
        ("Underfill_PrecisionDispense", "Flip-Chip Precision Underfill Jetting Dispenser with Dynamic Weight Calibration")
    ],
    "plastics": [
        ("InjectionMolding_1200T_CavityPress", "1,200-Ton Multi-Cavity Injection Molding Machine with Dynamic V/P Transfer Point"),
        ("Extrusion_TwinScrew_Compounding", "Co-Rotating Twin-Screw Extrusion Compounding Line with Loss-in-Weight Feeders"),
        ("BlowMolding_EBM_ParisonControl", "Continuous Extrusion Blow Molding with 100-Point Parison Wall Thickness Regulation"),
        ("CastFilm_MultiLayer_Coextrusion", "9-Layer Barrier Cast Film Line with Automatic Die Lip Thermal Bolt Gauge Control")
    ],
    "foodbev": [
        ("RotaryCanSeamer_1200cpm", "High-Speed 12-Spindle Rotary Beverage Can Seamer (1,200 cans/min) with Seam Defect Vision"),
        ("AsepticFiller_PeraceticAcid", "Continuous Aseptic Rotary Bottle Filler with Peracetic Acid Sterilization Tunnel"),
        ("UHT_DirectSteamInjection", "Ultra-High Temperature (UHT) Direct Steam Injection Milk Pasteurizer with Backpressure Guard"),
        ("CIP_FourTank_CausticLoop", "Automated Four-Tank Clean-In-Place (CIP) Caustic/Acid Sanitization Loop with Conductivity Recovery")
    ],
    "steelmaking": [
        ("ColdMill_6High_Reversing", "6-High Cold Reversing Strip Rolling Mill with Automatic Gauge & Flatness Control (AGC/AFC)"),
        ("Galvanizing_ContinuousStrip", "Continuous Hot-Dip Strip Galvanizing Line with Zinc Air-Knife Coating Thickness Control"),
        ("Pickling_ContinuousTandem", "Continuous Strip Hydrochloric Acid Pickling Line with Cascade Acid Concentration TMR")
    ]
}

TARGET_RATIOS = {
    "automotive": 0.25,
    "heavy_machinery": 0.20,
    "electronics": 0.15,
    "semiconductor": 0.15,
    "plastics": 0.10,
    "foodbev": 0.10,
    "steelmaking": 0.05
}

class DomainScheduler:
    """Orchestrates balanced sector assignments across multiple agent tasks."""

    def __init__(self, current_sector_counts: Optional[Dict[str, int]] = None):
        self.counts = current_sector_counts or {s: 0 for s in TARGET_RATIOS}

    def update_count(self, sector: str):
        if sector in self.counts:
            self.counts[sector] += 1

    def get_distribution(self) -> Dict[str, float]:
        """Returns current actual percentage distribution across sectors."""
        total = sum(self.counts.values())
        if total == 0:
            return {s: 0.0 for s in TARGET_RATIOS}
        return {s: self.counts.get(s, 0) / total for s in TARGET_RATIOS}

    def get_deficits(self) -> Dict[str, float]:
        """Returns current deficit (target_pct - actual_pct) for all sectors."""
        total = sum(self.counts.values())
        if total == 0:
            return TARGET_RATIOS.copy()
        return {s: TARGET_RATIOS[s] - (self.counts.get(s, 0) / total) for s in TARGET_RATIOS}

    def select_next_assignment(self, auto_update: bool = False) -> Tuple[str, str, str]:
        """
        Selects next (sector, system_code, system_description) prioritizing highest deficit.
        If auto_update is True, automatically updates the sector count upon selection.
        """
        total = sum(self.counts.values())
        if total == 0:
            sector = "automotive"
        else:
            deficits = self.get_deficits()
            sector = max(deficits, key=deficits.get)

        if auto_update:
            self.update_count(sector)

        # Pick a system within the chosen sector
        systems = SECTOR_SYSTEM_CATALOG[sector]
        system_code, system_desc = random.choice(systems)
        return sector, system_code, system_desc
