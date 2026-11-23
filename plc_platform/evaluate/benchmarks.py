#!/usr/bin/env python3
"""
plc_platform/evaluate/benchmarks.py — 31 Held-Out Industrial Benchmarks
Reference: MODEL_EVALUATION_AND_BENCHMARKS.md, PLC_DOMAIN_INTELLIGENCE.md

Curated held-out test suite across 6 major commercial manufacturing sectors:
1. Automotive & Commercial Vehicles (7 items)
2. Electronics & Semiconductor (6 items)
3. Mechanical & Heavy Machinery (5 items)
4. Plastics & Polymers (5 items)
5. Food & Beverage (5 items)
6. Steelmaking & Primary Metals (3 items)
Total = 31 benchmarks.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any


@dataclass
class BenchmarkItem:
    bench_id: str
    title: str
    sector: str
    vendor: str
    target_language: str
    prompt: str
    expected_states: List[str]
    safety_invariants: List[str]
    hardware_config: Dict[str, str] = field(default_factory=dict)


class BenchmarkSuite:
    """Provides access to the 31 held-out industrial benchmarks."""

    @classmethod
    def get_all_benchmarks(cls) -> List[BenchmarkItem]:
        benches: List[BenchmarkItem] = []

        # -------------------------------------------------------------
        # 1. Automotive & Commercial Vehicles (7 items)
        # -------------------------------------------------------------
        benches.append(BenchmarkItem(
            bench_id="BENCH-AUTO-01",
            title="EV Battery Module Cell-to-Pack Dispensing Control",
            sector="AUTOMOTIVE",
            vendor="SIEMENS",
            target_language="SCL",
            prompt="Generate Siemens S7-1500 SCL Function Block for EV battery cell 2K polyurethane thermal paste volumetric dispensing with 2oo3 pressure voting.",
            expected_states=["STATE_INIT", "STATE_PURGE", "STATE_DISPENSE", "STATE_DEPRESSURIZE", "STATE_TRIPPED"],
            safety_invariants=["NOT b_EStop_OK => r_DispenseValve = 0.0", "b_DiscrepancyFault => b_SafetyTrip = TRUE"]
        ))
        benches.append(BenchmarkItem(
            bench_id="BENCH-AUTO-02",
            title="Robotic Body-in-White (BIW) Roller Hemming Gate",
            sector="AUTOMOTIVE",
            vendor="ROCKWELL",
            target_language="L5X_ST",
            prompt="Generate Rockwell Studio 5000 AOI for automotive door roller hemming table with dual-channel clamp reed switches and robot safety zone handshake.",
            expected_states=["STATE_IDLE", "STATE_CLAMPING", "STATE_HEMMING", "STATE_UNCLAMPING", "STATE_ABORTED"],
            safety_invariants=["NOT b_LightCurtain_OK => b_RobotPermissive = FALSE"]
        ))
        benches.append(BenchmarkItem(
            bench_id="BENCH-AUTO-03",
            title="EV Laser Busbar Welding Shutter & Pyrometer Control",
            sector="AUTOMOTIVE",
            vendor="SIEMENS",
            target_language="SCL",
            prompt="Generate Siemens SCL block controlling laser welding emission shutter with pyrometer melt-pool overtemperature interlock (<85C) and chiller flow monitoring.",
            expected_states=["STATE_READY", "STATE_LASER_FIRING", "STATE_COOLING", "STATE_EMERGENCY_SHUTOFF"],
            safety_invariants=["r_MeltTemp > 85.0 => b_LaserEnable = FALSE"]
        ))
        benches.append(BenchmarkItem(
            bench_id="BENCH-AUTO-04",
            title="Automated Engine Dyno Cold Test Stand",
            sector="AUTOMOTIVE",
            vendor="BECKHOFF",
            target_language="STRUCTURED_TEXT",
            prompt="Generate Beckhoff TwinCAT 3 POU for engine dynamometer motoring and cold oil pressure ramp verification with 10ms sampling.",
            expected_states=["STATE_HOMING", "STATE_CRANKING", "STATE_LOGGING", "STATE_DECEL", "STATE_FAULT"],
            safety_invariants=["NOT b_GuardDoorClosed => b_DynoMotorEnable = FALSE"]
        ))
        benches.append(BenchmarkItem(
            bench_id="BENCH-AUTO-05",
            title="Automated Paint Booth Bell Atomizer Air Bearing Speed",
            sector="AUTOMOTIVE",
            vendor="ROCKWELL",
            target_language="L5X_ST",
            prompt="Generate Rockwell AOI regulating high-speed rotary paint bell turbine air bearing pressure (>5.5 bar) and electro-pneumatic speed control.",
            expected_states=["STATE_PURGE", "STATE_SPINUP", "STATE_SPRAY", "STATE_FLUSH", "STATE_TRIPPED"],
            safety_invariants=["r_AirBearingPress < 5.0 => b_TurbineDrive = FALSE"]
        ))
        benches.append(BenchmarkItem(
            bench_id="BENCH-AUTO-06",
            title="Two-Wheeler Motorcycle Frame Robotic MIG Weld Jig",
            sector="AUTOMOTIVE",
            vendor="SIEMENS",
            target_language="SCL",
            prompt="Generate Siemens S7-1500 SCL block for motorcycle frame pneumatic toggle clamps with 2oo3 cylinder travel sensor voting.",
            expected_states=["STATE_LOAD", "STATE_CLAMP", "STATE_WELD_ZONE", "STATE_UNLOAD", "STATE_FAULT"],
            safety_invariants=["NOT b_SafetyInterlock => b_ClampCylinders = FALSE"]
        ))
        benches.append(BenchmarkItem(
            bench_id="BENCH-AUTO-07",
            title="Electric Two-Wheeler Hub Motor End-of-Line Test Cell",
            sector="AUTOMOTIVE",
            vendor="BECKHOFF",
            target_language="STRUCTURED_TEXT",
            prompt="Generate TwinCAT 3 POU for E-bike brushless hub motor back-EMF dynamometer torque and thermal limit test.",
            expected_states=["STATE_SETUP", "STATE_DYN_LOAD", "STATE_COAST", "STATE_PASS", "STATE_FAIL"],
            safety_invariants=["NOT b_EStop_OK => b_InverterEnable = FALSE"]
        ))

        # -------------------------------------------------------------
        # 2. Electronics & Semiconductor (6 items)
        # -------------------------------------------------------------
        benches.append(BenchmarkItem(
            bench_id="BENCH-ELEC-01",
            title="SMT High-Speed Pick-and-Place Feeder Collation",
            sector="ELECTRONICS",
            vendor="BECKHOFF",
            target_language="STRUCTURED_TEXT",
            prompt="Generate TwinCAT 3 Function Block managing 16-lane tape feeder indexing and vacuum pick confirmation threshold (-85 kPa).",
            expected_states=["STATE_INDEX", "STATE_VACUUM_DRAW", "STATE_INSPECT", "STATE_REJECT", "STATE_READY"],
            safety_invariants=["r_VacuumLevel > -60.0 => b_GantryPermissive = FALSE"]
        ))
        benches.append(BenchmarkItem(
            bench_id="BENCH-ELEC-02",
            title="12-Zone PCB Reflow Soldering Convection Oven",
            sector="ELECTRONICS",
            vendor="SIEMENS",
            target_language="SCL",
            prompt="Generate Siemens S7-1500 SCL Function Block for 12-zone convection reflow temperature ramp control with thermocouple open-circuit trip.",
            expected_states=["STATE_PREHEAT", "STATE_SOAK", "STATE_REFLOW", "STATE_COOL", "STATE_ALARM"],
            safety_invariants=["b_ThermocoupleFault => b_HeaterSCR_Enable = FALSE"]
        ))
        benches.append(BenchmarkItem(
            bench_id="BENCH-ELEC-03",
            title="Semiconductor Wafer FOUP Load Port Nitrogen Purge",
            sector="ELECTRONICS",
            vendor="ROCKWELL",
            target_language="L5X_ST",
            prompt="Generate Rockwell AOI for Class 1 cleanroom wafer FOUP docking door seal and N2 oxygen depletion purge loop.",
            expected_states=["STATE_DOCK", "STATE_PUMP", "STATE_PURGE_N2", "STATE_ACCESS_READY", "STATE_ABORT"],
            safety_invariants=["r_O2_Concentration > 5.0 => b_WaferDoorUnlock = FALSE"]
        ))
        benches.append(BenchmarkItem(
            bench_id="BENCH-ELEC-04",
            title="Thermosonic Gold Wire Bonder Transducer Phase Loop",
            sector="ELECTRONICS",
            vendor="BECKHOFF",
            target_language="STRUCTURED_TEXT",
            prompt="Generate TwinCAT 3 ST block for 60 kHz ultrasonic wire bond transducer resonance tracking with microsecond timer execution.",
            expected_states=["STATE_SEEK", "STATE_BOND_SEARCH", "STATE_ULTRASONIC_BURST", "STATE_TAIL_CUT", "STATE_ERROR"],
            safety_invariants=["NOT b_EStop_OK => b_UltrasonicPower = FALSE"]
        ))
        benches.append(BenchmarkItem(
            bench_id="BENCH-ELEC-05",
            title="AOI Vision Inspection Conveyor Reject Kicker",
            sector="ELECTRONICS",
            vendor="SIEMENS",
            target_language="SCL",
            prompt="Generate Siemens SCL block for high-speed conveyor vision reject air blow ejector with encoder position tracking queue.",
            expected_states=["STATE_TRACKING", "STATE_ARMED", "STATE_EJECT", "STATE_CLEAR"],
            safety_invariants=["NOT b_ConveyorRunning => b_AirBlastValve = FALSE"]
        ))
        benches.append(BenchmarkItem(
            bench_id="BENCH-ELEC-06",
            title="Semiconductor CMP Slurry Dosing & pH Metering",
            sector="ELECTRONICS",
            vendor="ROCKWELL",
            target_language="L5X_ST",
            prompt="Generate Rockwell AOI for Chemical Mechanical Planarization slurry closed-loop peristaltic dosing with 2oo3 pH sensor voting.",
            expected_states=["STATE_IDLE", "STATE_PRIME", "STATE_DOSE", "STATE_RINSE", "STATE_FAULT"],
            safety_invariants=["b_2oo3_Discrepancy => b_DosingPumpRun = FALSE"]
        ))

        # -------------------------------------------------------------
        # 3. Mechanical & Heavy Machinery (5 items)
        # -------------------------------------------------------------
        benches.append(BenchmarkItem(
            bench_id="BENCH-MECH-01",
            title="2,500-Ton Hydraulic Stamping Press Ram Servo",
            sector="HEAVY_MACHINERY",
            vendor="SIEMENS",
            target_language="SCL",
            prompt="Generate Siemens S7-1500 SCL Function Block controlling 2,500-ton hydraulic forging press proportional valve and 4-corner tonnage monitoring.",
            expected_states=["STATE_OPEN", "STATE_RAPID_CLOSE", "STATE_PRESSING", "STATE_DECOMPRESS", "STATE_RETURN", "STATE_E_STOP"],
            safety_invariants=["NOT b_EStop_OK => b_HydraulicPumpActive = FALSE", "r_TonnageEccentricity > 15.0 => b_SafetyTrip = TRUE"]
        ))
        benches.append(BenchmarkItem(
            bench_id="BENCH-MECH-02",
            title="5-Axis Gantry CNC Spindle Active Thermal Growth Compensator",
            sector="HEAVY_MACHINERY",
            vendor="BECKHOFF",
            target_language="STRUCTURED_TEXT",
            prompt="Generate TwinCAT 3 POU calculating real-time axial spindle thermal expansion matrix and outputting Z-axis offset to CNC kernel.",
            expected_states=["STATE_CALIBRATE", "STATE_ACTIVE_COMPENSATE", "STATE_OVERTEMP_HOLD", "STATE_FAULT"],
            safety_invariants=["r_SpindleBearingTemp > 75.0 => b_FeedHold = TRUE"]
        ))
        benches.append(BenchmarkItem(
            bench_id="BENCH-MECH-03",
            title="High-Pressure Aluminum Die Casting Cell Shot Cylinder",
            sector="HEAVY_MACHINERY",
            vendor="ROCKWELL",
            target_language="L5X_ST",
            prompt="Generate Rockwell AOI for die casting hydraulic shot sleeve multi-phase velocity ramp (slow pour, fast fill, intensification up to 800 bar).",
            expected_states=["STATE_POUR", "STATE_PHASE_1", "STATE_PHASE_2", "STATE_INTENSIFY", "STATE_EJECT"],
            safety_invariants=["NOT b_DieClosedAndLocked => b_ShotCylinderEnable = FALSE"]
        ))
        benches.append(BenchmarkItem(
            bench_id="BENCH-MECH-04",
            title="Heavy Gantry Crane Anti-Sway Dynamic Cable Inverter",
            sector="HEAVY_MACHINERY",
            vendor="SIEMENS",
            target_language="SCL",
            prompt="Generate Siemens SCL block implementing input shaping / pendulum anti-sway trajectory calculation for 50-ton gantry crane trolley.",
            expected_states=["STATE_HOLD", "STATE_ACCEL_SHAPED", "STATE_CRUISE", "STATE_DECEL_SHAPED", "STATE_STOPPED"],
            safety_invariants=["b_WindSpeedHigh => b_GantryDrivePermissive = FALSE"]
        ))
        benches.append(BenchmarkItem(
            bench_id="BENCH-MECH-05",
            title="Continuous Steel Coil Rotary Shear Flying Cut",
            sector="HEAVY_MACHINERY",
            vendor="BECKHOFF",
            target_language="STRUCTURED_TEXT",
            prompt="Generate TwinCAT 3 POU implementing electronic camming (Flying Saw / Rotary Knife) synchronized to strip master encoder.",
            expected_states=["STATE_CLUTCH_SYNC", "STATE_CUT_STROKE", "STATE_ACCEL_RETURN", "STATE_PARK"],
            safety_invariants=["NOT b_StripTension_OK => b_ShearMotorEnable = FALSE"]
        ))

        # -------------------------------------------------------------
        # 4. Plastics & Polymers (5 items)
        # -------------------------------------------------------------
        benches.append(BenchmarkItem(
            bench_id="BENCH-PLAST-01",
            title="1,200-Ton Multi-Cavity Injection Molding V/P Switchover",
            sector="PLASTICS",
            vendor="ROCKWELL",
            target_language="L5X_ST",
            prompt="Generate Rockwell AOI for 1,200-ton injection molding machine screw injection velocity control with cavity pressure V/P transfer at 95% volumetric fill.",
            expected_states=["STATE_MOLD_CLOSE", "STATE_INJECTION", "STATE_HOLD_PRESSURE", "STATE_PLASTICIZING", "STATE_MOLD_OPEN"],
            safety_invariants=["NOT b_SafetyGateClosed => b_HydraulicMotors = FALSE"]
        ))
        benches.append(BenchmarkItem(
            bench_id="BENCH-PLAST-02",
            title="Co-Rotating Twin-Screw Extruder Melt Pressure & Temp",
            sector="PLASTICS",
            vendor="SIEMENS",
            target_language="SCL",
            prompt="Generate Siemens S7-1500 SCL block for twin-screw compounding extruder barrel heating zones and melt rupture disc overpressure safety trip.",
            expected_states=["STATE_PREHEAT", "STATE_FEEDING", "STATE_STEADY_EXTRUDE", "STATE_PURGE", "STATE_OVERPRESSURE_TRIP"],
            safety_invariants=["r_MeltPressure > 350.0 => b_ExtruderScrewMotor = FALSE"]
        ))
        benches.append(BenchmarkItem(
            bench_id="BENCH-PLAST-03",
            title="Extrusion Blow Molding (EBM) 100-Point Parison Programmer",
            sector="PLASTICS",
            vendor="BECKHOFF",
            target_language="STRUCTURED_TEXT",
            prompt="Generate TwinCAT 3 ST block interpolating 100-point parison die gap wall-thickness profile synchronized to screw extrusion stroke.",
            expected_states=["STATE_PROFILE_ARM", "STATE_PARISON_EXTRUDE", "STATE_PINCH_CUT", "STATE_BLOW", "STATE_IDLE"],
            safety_invariants=["NOT b_HydraulicsHealthy => b_ServoValveDieGap = FALSE"]
        ))
        benches.append(BenchmarkItem(
            bench_id="BENCH-PLAST-04",
            title="Continuous Blown Film Line Internal Bubble Cooling (IBC)",
            sector="PLASTICS",
            vendor="ROCKWELL",
            target_language="L5X_ST",
            prompt="Generate Rockwell AOI for blown film IBC air ring ultrasonic frost-line height control with layflat width regulation.",
            expected_states=["STATE_BUBBLE_INFLATE", "STATE_IBC_CONTROL", "STATE_HAULOFF", "STATE_ALARM"],
            safety_invariants=["r_LayflatWidth > 1500.0 => b_IBC_BlowerSpeed = 0.0"]
        ))
        benches.append(BenchmarkItem(
            bench_id="BENCH-PLAST-05",
            title="Plastic Thermoforming Machine Multi-Zone Radiant Oven",
            sector="PLASTICS",
            vendor="SIEMENS",
            target_language="SCL",
            prompt="Generate Siemens SCL block for thermoforming infrared ceramic heater array with sag eye optical droop sensor triggering vacuum form drape.",
            expected_states=["STATE_INDEX_SHEET", "STATE_HEAT", "STATE_VACUUM_FORM", "STATE_PLUG_ASSIST", "STATE_COOL_DEMOLD"],
            safety_invariants=["NOT b_EStop_OK => b_HeaterContactor = FALSE"]
        ))

        # -------------------------------------------------------------
        # 5. Food & Beverage (5 items)
        # -------------------------------------------------------------
        benches.append(BenchmarkItem(
            bench_id="BENCH-FB-01",
            title="Aseptic Rotary Bottling Carousel (48,000 bph)",
            sector="FOOD_BEVERAGE",
            vendor="SIEMENS",
            target_language="SCL",
            prompt="Generate Siemens S7-1500 SCL block for 48,000 bph aseptic bottle filling carousel with positive sterile HEPA overpressure (+50 Pa) and diaphragm leak monitoring.",
            expected_states=["STATE_STERILE_WAIT", "STATE_CAROUSEL_SPIN", "STATE_FILLING", "STATE_CAPPER_TRANSFER", "STATE_CIP_ABORT"],
            safety_invariants=["r_HEPA_Overpressure < 20.0 => b_FillingValvesEnable = FALSE"]
        ))
        benches.append(BenchmarkItem(
            bench_id="BENCH-FB-02",
            title="Clean-In-Place (CIP) 5-Step Caustic/Acid Sanitization Loop",
            sector="FOOD_BEVERAGE",
            vendor="ROCKWELL",
            target_language="L5X_ST",
            prompt="Generate Rockwell AOI for 5-step CIP sanitization: Pre-rinse, Caustic wash (1.5% NaOH at 80C), Intermediate rinse, Acid wash (0.8% HNO3), Final rinse with velocity > 1.5 m/s.",
            expected_states=["STATE_PRE_RINSE", "STATE_CAUSTIC_CIRC", "STATE_MID_RINSE", "STATE_ACID_CIRC", "STATE_FINAL_RINSE", "STATE_SANITIZED"],
            safety_invariants=["r_SanitizationFlow < 1.0 => b_HeaterPermissive = FALSE"]
        ))
        benches.append(BenchmarkItem(
            bench_id="BENCH-FB-03",
            title="Industrial Retort Steam Sterilization Autoclave",
            sector="FOOD_BEVERAGE",
            vendor="SIEMENS",
            target_language="SCL",
            prompt="Generate Siemens SCL Function Block calculating cumulative F0 lethality factor for canned food steam sterilization retort with overpressure air balance.",
            expected_states=["STATE_VENT", "STATE_HEATUP", "STATE_STERILIZE", "STATE_PRESSURE_COOL", "STATE_DRAIN"],
            safety_invariants=["NOT b_DoorSafetyLockEngaged => b_SteamInletValve = FALSE"]
        ))
        benches.append(BenchmarkItem(
            bench_id="BENCH-FB-04",
            title="High-Speed Delta Robot Case Packing & Collation",
            sector="FOOD_BEVERAGE",
            vendor="BECKHOFF",
            target_language="STRUCTURED_TEXT",
            prompt="Generate TwinCAT 3 POU coordinating 3-axis Delta robot case packer vacuum gripper picking pouches from moving conveyor belt using camera trigger.",
            expected_states=["STATE_WAIT_POUCH", "STATE_SYNC_CONVEYOR", "STATE_GRIP_LIFT", "STATE_CARTON_PLACE", "STATE_FAULT"],
            safety_invariants=["NOT b_SafetyInterlockCurtain => b_DeltaRobotPower = FALSE"]
        ))
        benches.append(BenchmarkItem(
            bench_id="BENCH-FB-05",
            title="Continuous Brewery Wort Boiling & Hop Dosing System",
            sector="FOOD_BEVERAGE",
            vendor="ROCKWELL",
            target_language="L5X_ST",
            prompt="Generate Rockwell AOI for brewery brewkettle wort boiling temperature regulation and automated timed 4-stage hop doser carousel.",
            expected_states=["STATE_FILL", "STATE_BOIL_RAMP", "STATE_VIGOROUS_BOIL", "STATE_WHIRLPOOL", "STATE_TRANSFER"],
            safety_invariants=["b_KettleLowLevel => b_SteamCoilValve = FALSE"]
        ))

        # -------------------------------------------------------------
        # 6. Steelmaking & Primary Metals (3 items)
        # -------------------------------------------------------------
        benches.append(BenchmarkItem(
            bench_id="BENCH-STEEL-01",
            title="Continuous Casting Machine Mold Level Radiometric Control",
            sector="HEAVY_MACHINERY",
            vendor="SIEMENS",
            target_language="SCL",
            prompt="Generate Siemens S7-1500 SCL block for continuous steel casting mold meniscus level control using radioactive Co-60 sensor and hydraulic stopper rod servo.",
            expected_states=["STATE_PREHEAT", "STATE_CAST_START", "STATE_AUTO_LEVEL", "STATE_TAIL_OUT", "STATE_EMERGENCY_SHUT"],
            safety_invariants=["NOT b_EStop_OK => b_StopperRodClose = TRUE"]
        ))
        benches.append(BenchmarkItem(
            bench_id="BENCH-STEEL-02",
            title="Electric Arc Furnace (EAF) 3-Phase Electrode Hydraulic Regulator",
            sector="HEAVY_MACHINERY",
            vendor="ROCKWELL",
            target_language="L5X_ST",
            prompt="Generate Rockwell AOI for EAF impedance-based electrode hydraulic cylinder positioning regulating arc current across all 3 phases.",
            expected_states=["STATE_ARC_IGNITION", "STATE_BORE_DOWN", "STATE_MELTING", "STATE_REFINING", "STATE_RETRACT"],
            safety_invariants=["r_TransformerOvercurrent => b_ElectrodeFastRaise = TRUE"]
        ))
        benches.append(BenchmarkItem(
            bench_id="BENCH-STEEL-03",
            title="6-High Cold Reversing Strip Rolling Mill Hydraulic AGC",
            sector="HEAVY_MACHINERY",
            vendor="BECKHOFF",
            target_language="STRUCTURED_TEXT",
            prompt="Generate TwinCAT 3 POU implementing Automatic Gauge Control (AGC) mass-flow and BISRA feedback cylinder position regulation with 1ms cycle time.",
            expected_states=["STATE_THREAD", "STATE_AGC_RUN", "STATE_TAIL_OUT", "STATE_REVERSE", "STATE_TRIPPED"],
            safety_invariants=["NOT b_LubricationPressure_OK => b_MillRollDrive = FALSE"]
        ))

        return benches
