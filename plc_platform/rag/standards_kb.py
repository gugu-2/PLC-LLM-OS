#!/usr/bin/env python3
"""
plc_platform/rag/standards_kb.py — Authoritative Industrial Standards Knowledge Corpus
Reference: PLC_DOMAIN_INTELLIGENCE.md, PROJECT_ARCHITECTURE.md

Contains structured, verified technical specifications, guidelines, and diagnostic rules:
- ISA-88 Batch Control (Physical Hierarchy, Procedural Hierarchy, State Models)
- OMAC PackML TR28.00.02 (17 Machine States, PackTags, State Transition Logic)
- ISA-18.2 Alarm Management (Deadband Hysteresis, Priorities, Flood Suppression)
- IEC 61131-3 Standard (Scan Cycles, Memory PII/PIQ, Standard Types & FBs)
- Siemens S7-1500 / S7-1200 TIA Portal Engineering & Diagnostics (OBs, DBs, SFCs)
- Rockwell Automation ControlLogix / Studio 5000 AOI & Fault Codes
- Beckhoff TwinCAT 3 ADS, Real-Time Task Configuration & PLCopen Motion
- Manufacturing Sector Directives (Automotive, SMT, Machinery, Plastics, Food/Beverage)
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any


@dataclass
class StandardDocument:
    doc_id: str
    title: str
    standard_name: str  # ISA-88, PACKML, ISA-18.2, IEC-61131-3, SIEMENS, ROCKWELL, BECKHOFF, SECTOR_SPECS
    category: str      # HIERARCHY, STATE_MACHINE, ALARM, SYNTAX, DIAGNOSTICS, SAFETY
    vendor: str        # SIEMENS, ROCKWELL, BECKHOFF, ALL
    sector: str        # AUTOMOTIVE, ELECTRONICS, HEAVY_MACHINERY, PLASTICS, FOOD_BEVERAGE, ALL
    content: str
    tags: List[str] = field(default_factory=list)

    @property
    def standard(self) -> str:
        return self.standard_name


class IndustrialStandardsCorpus:
    """Pre-indexed repository of verified industrial automation standards and specifications."""

    @staticmethod
    def get_all_documents() -> List[StandardDocument]:
        docs: List[StandardDocument] = []

        # 1. ISA-88 Physical & Procedural Hierarchy
        docs.append(StandardDocument(
            doc_id="ISA88-001",
            title="ANSI/ISA-88.01 Batch Control Physical & Procedural Models",
            standard_name="ISA-88",
            category="HIERARCHY",
            vendor="ALL",
            sector="ALL",
            content=(
                "ANSI/ISA-88 (IEC 61512) defines a 7-level physical model:\n"
                "1. Enterprise: Multi-plant business entity.\n"
                "2. Site: Single physical manufacturing location.\n"
                "3. Area: Dedicated manufacturing plant division.\n"
                "4. Process Cell: Aggregation of equipment required to produce a complete batch.\n"
                "5. Unit: Major equipment item executing processing activities (reactor, mixer, buffer tank).\n"
                "6. Equipment Module (EM): Functional group carrying out finite processing tasks (dosing header, heating jacket).\n"
                "7. Control Module (CM): Direct actuator/sensor lowest level control (valve, motor starter, transmitter).\n\n"
                "The Procedural Hierarchy divides recipe control into:\n"
                "- Procedure -> Unit Procedure -> Operation -> Phase.\n"
                "Control modules must NOT depend on unit procedures; they execute commands issued by phases."
            ),
            tags=["isa-88", "batch", "physical-model", "procedural-model", "equipment-module", "control-module"]
        ))

        # 2. PackML Machine States & PackTags
        docs.append(StandardDocument(
            doc_id="PACKML-001",
            title="OMAC PackML TR28.00.02 Unit/Machine 17-State Model & PackTags",
            standard_name="PACKML",
            category="STATE_MACHINE",
            vendor="ALL",
            sector="ALL",
            content=(
                "PackML defines 17 standardized machine operating states:\n"
                "Wait States (Stable until commanded):\n"
                "- STOPPED (State 2), RESETTING (1), IDLE (4), STARTING (3), EXECUTE (6),\n"
                "- COMPLETING (16), COMPLETE (17), HOLDING (10), HELD (11), UNHOLDING (13),\n"
                "- SUSPENDING (5), SUSPENDED (7), UNSUSPENDING (8), STOPPING (7), ABORTING (9), ABORTED (8), CLEARING (15).\n\n"
                "State Transition Rules:\n"
                "- When transitioning to ABORTING, all actuators must de-energize instantly.\n"
                "- Moving from HELD to EXECUTE requires passing through UNHOLDING.\n"
                "- PackTags are standardized data structures divided into: Command (CntrlCmd, UnitModeChangeRequest), "
                "Status (CurMode, StateCurrent, MachineSpeed), and Admin (Alarm, CumulativeCounters)."
            ),
            tags=["packml", "omac", "state-machine", "packtags", "execute", "holding", "aborting"]
        ))

        # 3. ISA-18.2 Alarm Management & Deadband Hysteresis
        docs.append(StandardDocument(
            doc_id="ISA182-001",
            title="ANSI/ISA-18.2 Management of Alarm Systems for the Process Industries",
            standard_name="ISA-18.2",
            category="ALARM",
            vendor="ALL",
            sector="ALL",
            content=(
                "ISA-18.2 establishes rationalized alarm trip points, deadbands, and flood mitigation:\n"
                "1. Tiered Alarm Limits: High-High (HH: Emergency/Interlock), High (H: Pre-warning), "
                "Low (L: Operating threshold), Low-Low (LL: Safety trip).\n"
                "2. Hysteresis Deadband Calculation:\n"
                "   Deadband = 0.02 to 0.05 * (Span_High - Span_Low).\n"
                "   Alarm Cleared condition: Value < (Threshold_H - Deadband) or Value > (Threshold_L + Deadband).\n"
                "3. Alarm Flood Suppression:\n"
                "   Defined as > 10 alarms per 10 minutes per operator console.\n"
                "   Dynamic shelving, state-based alarm masking (suppress downstream alarms during unit shutdown), "
                "and discrepancy on-delay timers (typically T#100ms..T#500ms) prevent alarm chattering."
            ),
            tags=["isa-18.2", "alarms", "deadband", "hysteresis", "alarm-flood", "chattering", "trip-points"]
        ))

        # 4. IEC 61131-3 Scan Cycle and Memory Execution Model
        docs.append(StandardDocument(
            doc_id="IEC61131-001",
            title="IEC 61131-3 Deterministic Scan Cycle & Process Image (PII/PIQ)",
            standard_name="IEC-61131-3",
            category="SYNTAX",
            vendor="ALL",
            sector="ALL",
            content=(
                "IEC 61131-3 PLCs operate on a deterministic cyclical scan loop:\n"
                "Phase 1: Process Image Input (PII) update — physical inputs copied into memory.\n"
                "Phase 2: Logic execution — POU execution in order of task priority without preemption "
                "unless higher-priority cyclic interrupt (e.g. OB35 / 10ms task) triggers.\n"
                "Phase 3: Process Image Output (PIQ) write — output buffer pushed to physical I/O hardware.\n"
                "Phase 4: Diagnostics & Communications overhead (HMI, Fieldbus PROFINET/EtherNet/IP scan).\n\n"
                "Critical Constraints:\n"
                "- Never use blocking delay loops (WHILE timer < 5s DO) inside a PLC scan. This triggers watchdog timeout.\n"
                "- Output coils (OTE) written multiple times in the same scan result in the last assignment winning (Last-Write-Wins hazard).\n"
                "- Functions (FC) are memoryless; Function Blocks (FB) maintain state across scans in instance memory."
            ),
            tags=["iec-61131-3", "scan-cycle", "pii", "piq", "watchdog", "deterministic", "function-block"]
        ))

        # 5. Siemens S7-1500 TIA Portal Engineering & Diagnostics
        docs.append(StandardDocument(
            doc_id="SIEMENS-001",
            title="Siemens SIMATIC S7-1500 / TIA Portal Engineering Guidelines",
            standard_name="SIEMENS",
            category="DIAGNOSTICS",
            vendor="SIEMENS",
            sector="ALL",
            content=(
                "Siemens S7-1500 TIA Portal SCL Best Practices:\n"
                "1. Data Blocks: Always enforce { S7_Optimized_Access := 'TRUE' }. Avoid absolute DB addressing (%DB1.DBX0.0) "
                "which causes unaligned memory penalties and breaks symbolic compilation.\n"
                "2. Tag Scoping: Local variables inside Function Blocks must be addressed with '#' prefix (#b_EStop_OK).\n"
                "3. Organization Blocks:\n"
                "   - OB1: Main cyclical execution.\n"
                "   - OB30..OB38: Cyclic Interrupts (e.g., OB35 at 10ms for fast closed-loop control).\n"
                "   - OB82: Diagnostic Interrupt (wire break, short circuit detection on analog/digital modules).\n"
                "   - OB86: Rack/Station Failure (PROFINET IO device disconnection).\n"
                "   - OB100: Startup routine (prescan initialization of states and parameters).\n"
                "   - OB121/122: Programming error and I/O access error trap (prevents CPU Stop on peripheral read fault).\n"
                "4. System Functions: SFC20 (BLKMOV), SFB4 (TON), SFB5 (TOF), SFC51 (RDSYSST)."
            ),
            tags=["siemens", "s7-1500", "tia-portal", "scl", "optimized-db", "ob1", "ob35", "ob82", "profinet"]
        ))

        # 6. Rockwell Studio 5000 Logix Designer AOI & Diagnostics
        docs.append(StandardDocument(
            doc_id="ROCKWELL-001",
            title="Rockwell Automation Studio 5000 ControlLogix AOI & System Architecture",
            standard_name="ROCKWELL",
            category="DIAGNOSTICS",
            vendor="ROCKWELL",
            sector="ALL",
            content=(
                "Rockwell Logix5000 Architecture & Add-On Instructions (AOI):\n"
                "1. AOI Requirements: All AOIs automatically generate EnableIn and EnableOut parameters. "
                "Inputs are passed by value (copied into AOI on call), InOut are passed by reference.\n"
                "2. Prescan & EnableInFalse: Prescan routine runs on Program transition to RUN; EnableInFalse runs "
                "when the calling rung condition is FALSE (use to clear latch coils or stop timers).\n"
                "3. Controller Fault Codes:\n"
                "   - Type 01 (Task Overlap): Task execution exceeded requested period (Rate).\n"
                "   - Type 03 (I/O Fault): Communication loss with remote EtherNet/IP adapter (1756-EN2T/1734-AENT).\n"
                "   - Type 04 (Arithmetic Fault): Floating point overflow/underflow, divide-by-zero, NaN.\n"
                "4. GSV/SSV (Get/Set System Value): Used to read Controller Task status, WallClockTime, and Module fault LED states."
            ),
            tags=["rockwell", "controllogix", "studio-5000", "aoi", "l5x", "gsv", "ssv", "ethernet-ip"]
        ))

        # 7. Beckhoff TwinCAT 3 Real-Time & ADS Diagnostics
        docs.append(StandardDocument(
            doc_id="BECKHOFF-001",
            title="Beckhoff TwinCAT 3 Real-Time Architecture & ADS Communication",
            standard_name="BECKHOFF",
            category="DIAGNOSTICS",
            vendor="BECKHOFF",
            sector="ALL",
            content=(
                "Beckhoff TwinCAT 3 e!RUNTIME Architecture:\n"
                "1. Real-Time OS: Runs on dedicated isolated CPU cores with cycle times down to 250 microseconds.\n"
                "2. Pragmas: {attribute 'qualified_only'} prevents namespace pollution. {attribute 'Tc2GvlVar'} exports to HMI.\n"
                "3. ADS (Automation Device Specification) Error Codes:\n"
                "   - 0x0700: Device error / general failure.\n"
                "   - 0x0704: Target port not found (TwinCAT PLC runtime port 851 unreachable).\n"
                "   - 0x0705: Symbol not found in PLC dictionary.\n"
                "   - 0x0706: Invalid index group or index offset.\n"
                "   - 0x0745: Timeout elapsed during synchronous ADS service call.\n"
                "4. Motion Control: PLCopen Part 1/2 standard function blocks (MC_Power, MC_MoveAbsolute, MC_Stop, MC_Home)."
            ),
            tags=["beckhoff", "twincat-3", "ads", "ethercat", "plcopen", "motion-control", "mc-power"]
        ))

        # 8. Commercial Automotive Sector: Body-in-White & Battery Assembly
        docs.append(StandardDocument(
            doc_id="SECTOR-AUTO-001",
            title="Automotive BIW Robotic Welding & EV Battery Pack Assembly Rules",
            standard_name="SECTOR_SPECS",
            category="SAFETY",
            vendor="ALL",
            sector="AUTOMOTIVE",
            content=(
                "Automotive Manufacturing Automation Directives:\n"
                "1. Body-in-White (BIW): Roller hemming and spot weld cells require hardware E-Stop dual-channel "
                "safety circuits (ISO 13849-1 Cat 4 / PL e). Clamp tooling cylinders must verify Advance and Retract "
                "reed switches within 1500ms discrepancy timeout before robot entry.\n"
                "2. EV Battery Pack Laser Busbar Welding: Laser emission shutter interlock must check chiller flow rate "
                "> 18.5 L/min and workpiece clamp pressure > 6.2 bar. Pyrometer optical feedback must cut laser power within 2ms "
                "if thermal runaway temperature exceeds 85 deg C."
            ),
            tags=["automotive", "biw", "ev-battery", "laser-weld", "hemming", "safety-ple", "interlock"]
        ))

        # 9. Electronics & Semiconductor: SMT High-Speed Assembly
        docs.append(StandardDocument(
            doc_id="SECTOR-ELEC-001",
            title="Electronics SMT High-Speed Pick & Place and 12-Zone Reflow Rules",
            standard_name="SECTOR_SPECS",
            category="SAFETY",
            vendor="ALL",
            sector="ELECTRONICS",
            content=(
                "Electronics Manufacturing Automation Directives:\n"
                "1. SMT Pick & Place: Vacuum sensor threshold (-85 kPa) must be validated before gantry trajectory initiation. "
                "Missing component optical trigger increments drop counter and triggers purge sequence after 3 consecutive failures.\n"
                "2. 12-Zone PCB Reflow Soldering Ovens: Temperature ramp-rate must not exceed 2.5 deg C/sec to prevent solder splattering. "
                "Heater element SCR firing angle controller uses closed-loop PID with thermocouple open-circuit fail-safe trip."
            ),
            tags=["electronics", "smt", "pick-and-place", "reflow-oven", "vacuum-sensor", "pid-temperature"]
        ))

        # 10. Heavy Machinery & Mechanical: 2500-Ton Hydraulic Stamping Press
        docs.append(StandardDocument(
            doc_id="SECTOR-MECH-001",
            title="Heavy Machinery Hydraulic & Servo Stamping Press Safety Protocols",
            standard_name="SECTOR_SPECS",
            category="SAFETY",
            vendor="ALL",
            sector="HEAVY_MACHINERY",
            content=(
                "Heavy Machinery & Hydraulic Stamping Directives:\n"
                "1. Hydraulic Ram Motion: Dual safety proportional valves with spool position monitoring switches (LVDT). "
                "Ram descent prohibited unless optical light curtains (Type 4) are unobstructed and dual-hand control pushbuttons "
                "are pressed concurrently within 500ms anti-tiedown window.\n"
                "2. Dynamic Tonnage Monitoring: Strain gauge load cells on all 4 tie-rods must verify symmetric load balance "
                "within 10% tolerance; off-center eccentric loading > 15% trips emergency hydraulic decompression."
            ),
            tags=["heavy-machinery", "hydraulic-press", "stamping", "light-curtain", "dual-hand", "tonnage-monitor"]
        ))

        # 11. Plastics & Polymer: 1200-Ton Injection Molding V/P Transfer
        docs.append(StandardDocument(
            doc_id="SECTOR-PLAST-001",
            title="Plastics Injection Molding V/P Switchover and Mold Safety Protocols",
            standard_name="SECTOR_SPECS",
            category="SAFETY",
            vendor="ALL",
            sector="PLASTICS",
            content=(
                "Plastics Injection Molding Automation Directives:\n"
                "1. Velocity-to-Pressure (V/P) Switchover: Injection phase transitions to holding pressure phase based on: "
                "Screw position (95-98% volumetric fill), cavity pressure peak (e.g. 850 bar), or hydraulic pressure spike.\n"
                "2. Mold Protection: Low-pressure mold close stage (P < 15 bar) must reach clamp lock position within 2.0s; "
                "if resistance is met (part stuck on pins), mold instantly opens and robot alarm sounds."
            ),
            tags=["plastics", "injection-molding", "vp-switchover", "cavity-pressure", "mold-protection"]
        ))

        # 12. Food & Beverage: Continuous Aseptic Bottling (48,000 bph) & CIP/SIP
        docs.append(StandardDocument(
            doc_id="SECTOR-FB-001",
            title="Food & Beverage Aseptic Rotary Bottling & CIP/SIP Sanitization Protocols",
            standard_name="SECTOR_SPECS",
            category="SAFETY",
            vendor="ALL",
            sector="FOOD_BEVERAGE",
            content=(
                "Food & Beverage Aseptic Bottling Automation Directives:\n"
                "1. Aseptic Filling Carousel: Isobaric counter-pressure filling must maintain sterile HEPA positive overpressure (+50 Pa). "
                "Filling valve diaphragm seal leak detection via optical conductivity sensors.\n"
                "2. Clean-In-Place / Steam-In-Place (CIP/SIP): Multi-step sequence: Pre-rinse (ambient water), Caustic wash (1.5% NaOH at 80 deg C), "
                "Intermediate rinse, Acid wash (0.8% HNO3), Final sterile water rinse. Flow velocity > 1.5 m/s enforced to ensure turbulent scouring."
            ),
            tags=["food-beverage", "aseptic-filling", "bottling", "cip-sip", "sanitization", "turbulent-flow"]
        ))

        return docs


KNOWLEDGE_BASE: List[StandardDocument] = IndustrialStandardsCorpus.get_all_documents()

__all__ = ["StandardDocument", "IndustrialStandardsCorpus", "KNOWLEDGE_BASE"]
