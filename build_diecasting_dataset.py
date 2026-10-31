# -*- coding: utf-8 -*-
"""
Builder script for 3,500-Ton High-Pressure Aluminum Die Casting Cell
with Multi-Phase Injection Intensifier & Robotic Ladler/Sprayer.
Target Output: data/swarm_raw/agent_5b20a17f.json
"""

import json
import os
import validate_iec

user_prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices (A, B, C, D), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: Metallurgy & Heavy Tooling: 3,500-Ton High-Pressure Aluminum Die Casting Cell with Multi-Phase Injection Intensifier & Robotic Ladler/Sprayer: FB_DieCasting_HighPressure_Aluminium_LadlerSprayer - 3,500-Ton Hydraulic Toggle Clamp Tonnage Locking, 4-Tie-Bar Strain Gauge Elongation Balancing, Real-Time Closed-Loop Injection Shot Cylinder Control (Phase 1 Slow Shot 0.1-0.4 m/s Wave Rollover Avoidance, Phase 2 Fast Shot up to 8.5 m/s with 40g Acceleration, Phase 3 Hydraulic Intensifier 1,200 bar Micro-Porosity Shrinkage Consolidation within 15 ms), 10x10 Discrete State-Space Dynamic Model (Plunger Dynamics, Fluid Dynamics, Accumulator Discharge, Intensifier Travel), Receding-Horizon MPC Velocity Profile Pacing with Valve Deadband Compensation & Terminal Deceleration Braking, 2oo3 TMR Vacuum Mold Evacuation Transducers (< 50 mbar), 6-Axis Robotic Ladler Metal Dosing Synchronization (Temp Compensation, Slag Skim, Repeatable Shot Weight +/- 1.0%), Multi-Axis Die Spray Lubricant Atomization & Blow-Dry Purge, 12-Stage Heavy Foundry FSM (Die Close, Tonnage Lock, Ladle Pour, Vacuum Draw, Slow Shot, Fast Injection, Intensification, Biscuit Solidification Dwell, Die Open & Core Pull, Robotic Extraction, Die Spray, Cycle Recock), and ISA-18.2 Multi-Tiered Alarm Matrix.**

Generate a complete, fully implemented IEC 61131-3 Structured Text FUNCTION_BLOCK named FB_DieCasting_HighPressure_Aluminium_LadlerSprayer with zero placeholders, full state-space matrix initialization, MPC optimization, 2oo3 voting, full FSM execution, and ISA-18.2 alarm matrix."""

def build_code():
    parts = []
    
    # -------------------------------------------------------------------------
    # PART 1: Function Block Header & Cyber-Physical Technical Comments
    # -------------------------------------------------------------------------
    parts.append("""FUNCTION_BLOCK FB_DieCasting_HighPressure_Aluminium_LadlerSprayer
(*
====================================================================================================
PROJECT:        HEAVY METALLURGY & AUTOMOTIVE FOUNDRY AUTOMATION CYBER-PHYSICAL CONTROL
SUBSYSTEM:      3,500-TON HIGH-PRESSURE DIE CASTING (HPDC) CELL WITH MULTI-PHASE INJECTION
                INTENSIFIER, 2oo3 CAVITY VACUUM EVACUATION, ROBOTIC LADLER & MULTI-AXIS SPRAYER
MODULE:         FB_DieCasting_HighPressure_Aluminium_LadlerSprayer
ARCHITECTURE:   DISCRETE 10-STATE DYNAMIC OBSERVER + RECEDING-HORIZON MPC + 2oo3 TMR SENSOR FUSION +
                4-TIE-BAR STRAIN BALANCING + 12-STAGE FOUNDRY FSM + ISA-18.2 MULTI-TIERED ALARM TREE
AUTHOR:         LUMINA CYBER-PHYSICAL AUTOMATION ARCHITECT (75+ YRS VETERAN FELLOW SPECIFICATION)
STANDARDS:      IEC 61131-3 3RD ED, ISO 13849-1 (PL-d/PL-e SAFETY), ISO 12100, NADCA DIE CASTING,
                ISA-18.2 (ALARM MANAGEMENT), DIN EN 869 (DIE CASTING MACHINE SAFETY REQUIREMENTS)
====================================================================================================

MATHEMATICAL AND CYBER-PHYSICAL FOUNDRY ARCHITECTURE:
----------------------------------------------------------------------------------------------------
1. 3,500-TON (34.33 MN) HYDRAULIC TOGGLE CLAMP & 4 TIE-BAR STRAIN BALANCING:
   - Heavy structural megacasting (e.g. EV rear floor pans, shock towers in AlSi10MnMg / A380 alloy)
     exerts projected casting cavity separation forces exceeding 30,000 kN during Phase 3 intensification.
   - Four massive chrome-nickel alloy steel tie-bars (diameter D_tb = 280 mm, active length L = 8,500 mm,
     Young's modulus E = 210,000 N/mm^2).
   - Elastic strain-gauge bridge installed on each tie-bar (Tie-Bar 1: Upper Left, Tie-Bar 2: Upper Right,
     Tie-Bar 3: Lower Left, Tie-Bar 4: Lower Right).
   - Elastic elongation equation:
       Delta_L = (F_bar * L_0) / (E * A_tb)
       A_tb = pi * (D_tb / 2)^2 = 0.061575 m^2 (61,575 mm^2)
       Strain epsilon = Delta_L / L_0 = F_bar / (E * A_tb)
       F_bar [N] = epsilon * E * A_tb
       F_bar [metric tons] = F_bar [N] / (9,806.65 N/ton)
   - Dynamic cross-diagonal and quadrant imbalance calculation:
       F_total = F_tb1 + F_tb2 + F_tb3 + F_tb4
       F_mean = F_total / 4.0
       Imbalance_pct = (MAX(F_tb1..4) - MIN(F_tb1..4)) / F_mean * 100.0%
   - Closed-loop motorized tie-bar nut trim adjustment actively balances platen parallelism to
     prevent flash expulsion, die cavitation wear, and catastrophic tie-bar fatigue cracking.

2. THREE-PHASE INJECTION SHOT CYLINDER HYDRODYNAMICS & INTENSIFIER:
   The injection process governs casting metallurgical integrity through three distinct phases:
   - PHASE 1: SLOW SHOT (0.10 m/s to 0.40 m/s):
     Liquid aluminum bath (680 deg C - 710 deg C) rests in the horizontal beryllium-copper sleeve
     (inner diameter D_sleeve = 140 mm, stroke = 1,100 mm). The plunger advances slowly to allow the
     molten wave to coalesce without wave crest breaking (avoiding Eulerian wave rollover and trapped
     gas bubbles). The critical wave velocity limit follows shallow-water open channel wave speed:
       v_crit = sqrt(g * h_eff * (1 - f_fill))
     Plunger velocity is held strictly below v_crit until the melt reaches the narrow runner in-gate.
   - PHASE 2: FAST SHOT (up to 8.5 m/s, Acceleration > 40g = 392 m/s^2):
     Triggered precisely at the in-gate crossing position encoder setpoint (s_gate = 450 mm).
     High-pressure nitrogen-oil piston accumulator (250 L, 210 bar) dumps directly through a high-response
     cartridge valve into the 200 mm injection cylinder. Cavity fill time t_fill = 25 ms to 45 ms.
     Receding-horizon MPC tracks the rapid velocity ramp while executing active terminal deceleration
     braking prior to hard mechanical impact to protect the die tooling.
   - PHASE 3: HYDRAULIC INTENSIFICATION CONSOLIDATION (up to 1,200 bar within 15 ms):
     Upon cavity fill detection (pressure spike dP/dt > 12,000 bar/s and velocity drop), the intensifier
     fast-firing poppet dumps 315 bar hydraulic oil onto the intensifier booster piston (ratio 3.8:1),
     delivering 1,200 bar specific metal pressure on the freezing biscuit. This collapses gas porosity,
     crushes dendritic micro-shrinkage voids, and feeds solidification shrinkage front.

3. DISCRETE 10-STATE HYDRO-MECHANICAL STATE-SPACE SYSTEM (x[k+1] = A*x[k] + B*u[k]):
   Discretized at Ts = 1.0 ms (fast injection loop control task):
   State vector x in R^10:
     x[1] : Plunger linear position s_p [mm]
     x[2] : Plunger linear velocity v_p [m/s]
     x[3] : Plunger linear acceleration a_p [m/s^2]
     x[4] : Injection cylinder head chamber pressure P_head [bar]
     x[5] : Injection cylinder rod back-pressure P_rod [bar]
     x[6] : Nitrogen hydraulic accumulator dynamic pressure P_acc [bar]
     x[7] : Intensifier multiplication piston position s_int [mm]
     x[8] : Intensifier chamber output pressure P_int [bar]
     x[9] : Molten aluminum fluid drag / gate flow resistance pressure P_metal [bar]
     x[10]: Solidified biscuit skin thickness / freezing fraction xi_biscuit [%]
   Actuation vector u in R^8:
     u[1] : Main injection servovalve spool command [-100%..+100%]
     u[2] : Fast-shot pilot accumulator cartridge command [0..100%]
     u[3] : Intensifier ultra-fast poppet pilot valve command [0..100%]
     u[4] : Accumulator hydraulic charging pump swashplate displacement [0..100%]
     u[5] : Vacuum evacuation gate valve proportional command [0..100%]
     u[6] : Tie-bar motorized nut trim servo correction velocity [mm/s]
     u[7] : Robotic ladler metal dosing stream rate [kg/s]
     u[8] : Die thermoregulation cooling channel proportional manifold duty [%]
   Measurement vector y in R^6:
     y[1] : Dual optical/magnetostrictive plunger position encoder [mm]
     y[2] : Plunger digital velocity pulse tachometer / differentiated encoder [m/s]
     y[3] : Injection cylinder head piezoresistive pressure transmitter [bar]
     y[4] : Nitrogen accumulator pressure transmitter [bar]
     y[5] : Intensifier chamber pressure transducer [bar]
     y[6] : 2oo3 voted mold cavity vacuum pressure [mbar]

4. RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) VELOCITY & BRAKING:
   Horizon N_p = 5 steps, control horizon N_c = 3 steps. Quadratic objective cost function:
     J = sum_{i=1}^{Np} (x_{k+i} - x_ref)^T * Q * (x_{k+i} - x_ref) + sum_{j=0}^{Nc-1} delta_u_{k+j}^T * R * delta_u_{k+j} + (x_{k+Np} - x_ref)^T * P * (x_{k+Np} - x_ref)
   Incorporates non-linear hydraulic valve spool deadband inversion (+/- 7.5% spool deadband) and
   terminal braking constraints to guarantee platen safety and zero cavity flashing.

5. 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) VACUUM MOLD EVACUATION:
   Three independent piezoresistive pressure transmitters (PT_VAC_1, PT_VAC_2, PT_VAC_3) monitor
   mold cavity vacuum down to < 50 mbar absolute prior to fast shot authorization. Discrepancy timers
   audit sensor drift (> 15 mbar delta) and trigger bumpless degradation (2oo3 -> 1oo2 -> 1oo1 -> Inhibit).

6. 6-AXIS ROBOTIC LADLER & MULTI-AXIS DIE SPRAYER SYNCHRONIZATION:
   - Robotic ladler doses exact shot weight (e.g. 18.5 kg +/- 1.0%) with molten aluminum temperature
     density compensation: rho(T) = 2380 - 0.35 * (T_melt - 660.0) kg/m^3.
   - Multi-axis robotic sprayer atomizes water-polymer release lubricant at 4.5 bar with multi-zone
     flow control followed by high-velocity dry air purge to eliminate residual water (porosity prevention).

7. 12-STAGE OPERATIONAL FOUNDRY FSM:
   State 10: DIE_CLOSE_AND_LOCK
   State 20: TONNAGE_VERIFICATION
   State 30: LADLER_POURING
   State 40: SLEEVE_VACUUM_DRAW
   State 50: PHASE_1_SLOW_SHOT
   State 60: PHASE_2_FAST_INJECTION
   State 70: PHASE_3_INTENSIFICATION
   State 80: BISCUIT_SOLIDIFICATION_DWELL
   State 90: DIE_OPEN_AND_CORE_PULL
   State 100: ROBOTIC_PART_EXTRACTION
   State 110: DIE_SPRAY_LUBRICATION_AND_AIR_PURGE
   State 120: CYCLE_RECOCK_AND_READY
   State 999: FAULT_SAFE_STOP
====================================================================================================
*)
VAR_INPUT
    (* =====================================================================================
       SECTION 1: SYSTEM SUPERVISORY, AUTOMATION PERMISSIVES & TIMING INTERFACES
       ===================================================================================== *)
    bEnable                         : BOOL := FALSE;    (* Master Foundry Cell Automation Enable Interlock [TRUE=Active] *)
    bReset                          : BOOL := FALSE;    (* Master Fault Reset and ISA-18.2 Alarm Acknowledge [TRUE=Reset] *)
    bEmergencyStopOk                : BOOL := TRUE;     (* Hardwired Dual-Channel Safety Relay E-Stop String [TRUE=Healthy] *)
    bAutoCycleStartCmd              : BOOL := FALSE;    (* Operator Auto-Cycle Initiation Pushbutton [TRUE=Start Cycle] *)
    bManualStepMode                 : BOOL := FALSE;    (* Engineering Maintenance Manual Single-Step Mode [TRUE=Manual] *)
    rSampleTime_s                   : REAL := 0.001;    (* Fast Cyclic Execution Sample Time Delta-T [s] (Nominal 1.0 ms) *)

    (* =====================================================================================
       SECTION 2: 3,500-TON CLAMP & 4 TIE-BAR STRAIN GAUGE TRANSDUCERS
       ===================================================================================== *)
    rTieBarStrain_UL_ue             : REAL := 0.0;      (* Tie-Bar 1 Upper-Left Micro-Strain Reading [ue] (10^-6 m/m) *)
    rTieBarStrain_UR_ue             : REAL := 0.0;      (* Tie-Bar 2 Upper-Right Micro-Strain Reading [ue] (10^-6 m/m) *)
    rTieBarStrain_LL_ue             : REAL := 0.0;      (* Tie-Bar 3 Lower-Left Micro-Strain Reading [ue] (10^-6 m/m) *)
    rTieBarStrain_LR_ue             : REAL := 0.0;      (* Tie-Bar 4 Lower-Right Micro-Strain Reading [ue] (10^-6 m/m) *)
    rToggleCylinderHeadPress_bar    : REAL := 0.0;      (* Hydraulic Toggle Clamp Closing Cylinder Head Pressure [bar] *)
    rToggleCylinderRodPress_bar     : REAL := 0.0;      (* Hydraulic Toggle Clamp Opening Cylinder Rod Pressure [bar] *)
    rToggleStrokePos_mm             : REAL := 0.0;      (* Toggle Mechanical Linkage Cross-Head Position LVDT [mm] *)
    rMovingPlatenPos_mm             : REAL := 0.0;      (* Moving Platen Absolute Linear Position Encoder [mm] *)
    bMoldSafetyGateClosed           : BOOL := FALSE;    (* High-Speed Die Enclosure Interlocked Safety Doors Closed [TRUE=OK] *)

    (* =====================================================================================
       SECTION 3: THREE-PHASE INJECTION CYLINDER & ACCUMULATOR TRANSDUCERS
       ===================================================================================== *)
    rPlungerPosition_mm             : REAL := 0.0;      (* Primary Injection Plunger Linear Scale Magnetostrictive SSI [mm] *)
    rPlungerPositionAux_mm          : REAL := 0.0;      (* Redundant Plunger Linear Position Scale Encoder [mm] *)
    rPlungerVelocity_mps            : REAL := 0.0;      (* Real-Time Injection Plunger Measured Linear Velocity [m/s] *)
    rInjectionCylinderHeadPress_bar : REAL := 0.0;      (* Main Injection Cylinder Head-End Hydraulic Pressure [bar] *)
    rInjectionCylinderRodPress_bar  : REAL := 0.0;      (* Main Injection Cylinder Rod-End Hydraulic Back-Pressure [bar] *)
    rAccumulatorPress_bar           : REAL := 210.0;    (* 250-Liter Piston Hydraulic Accumulator Gas/Oil Pressure [bar] *)
    rIntensifierPos_mm              : REAL := 0.0;      (* Pressure Intensifier Multiplication Piston Stroke LVDT [mm] *)
    rIntensifierPress_bar           : REAL := 0.0;      (* High-Pressure Intensification Chamber Hydraulic Pressure [bar] *)

    (* =====================================================================================
       SECTION 4: 2oo3 TMR VACUUM MOLD EVACUATION TRANSDUCERS
       ===================================================================================== *)
    rVacuumPressure_Ch1_mbar        : REAL := 1013.0;   (* Cavity Vacuum Piezoresistive Transmitter Channel 1 [mbar] *)
    rVacuumPressure_Ch2_mbar        : REAL := 1013.0;   (* Cavity Vacuum Piezoresistive Transmitter Channel 2 [mbar] *)
    rVacuumPressure_Ch3_mbar        : REAL := 1013.0;   (* Cavity Vacuum Piezoresistive Transmitter Channel 3 [mbar] *)
    bVacuumValveLimitSwOpen         : BOOL := FALSE;    (* High-Speed Pneumatic Chill-Vent Vacuum Valve Fully Open Limit *)
    bVacuumValveLimitSwClosed       : BOOL := TRUE;     (* High-Speed Pneumatic Chill-Vent Vacuum Valve Fully Closed Limit *)

    (* =====================================================================================
       SECTION 5: 6-AXIS ROBOTIC LADLER & MOLTEN ALUMINUM DOSING INTERFACES
       ===================================================================================== *)
    rFurnaceMetalTemp_degC          : REAL := 700.0;    (* Dosing Holding Furnace Molten Aluminum Bath Temperature [deg C] *)
    rLadleDosedWeight_kg            : REAL := 0.0;      (* Robotic Ladle Strain-Gauge Cup Measured Metal Weight [kg] *)
    rLadleTargetWeight_kg           : REAL := 18.5;     (* Nominal Target Liquid Aluminum Shot Weight Setpoint [kg] *)
    bLadlerInPosition               : BOOL := FALSE;    (* Ladler Robot In Sleeve Pour Hole Pouring Envelope [TRUE=Ready] *)
    bLadlerPouringComplete          : BOOL := FALSE;    (* Ladler Robot Tilt Pouring Complete Handshake Pulse [TRUE=Done] *)
    bLadlerHomeSafe                 : BOOL := TRUE;     (* Ladler Robot Retracted to Safe Home Interference Perimeter *)

    (* =====================================================================================
       SECTION 6: HYDRAULIC CORE PULLS & DIE PLATEN ACTUATION SENSORS
       ===================================================================================== *)
    rCore1Pos_mm                    : REAL := 0.0;      (* Hydraulic Slide Core 1 Linear Position Transducer [mm] *)
    bCore1InLimit                   : BOOL := FALSE;    (* Hydraulic Slide Core 1 Fully Inserted Casting Interlock Limit *)
    bCore1OutLimit                  : BOOL := TRUE;     (* Hydraulic Slide Core 1 Fully Retracted Ejection Interlock Limit *)
    rCore2Pos_mm                    : REAL := 0.0;      (* Hydraulic Slide Core 2 Linear Position Transducer [mm] *)
    bCore2InLimit                   : BOOL := FALSE;    (* Hydraulic Slide Core 2 Fully Inserted Casting Interlock Limit *)
    bCore2OutLimit                  : BOOL := TRUE;     (* Hydraulic Slide Core 2 Fully Retracted Ejection Interlock Limit *)
    rEjectorStroke_mm               : REAL := 0.0;      (* Hydraulic Ejector Plate Advance/Retract Stroke LVDT [mm] *)
    bEjectorForwardLimit            : BOOL := FALSE;    (* Ejector Plate Full Forward Stroke Mechanical Proximity Limit *)
    bEjectorRetractLimit            : BOOL := TRUE;     (* Ejector Plate Full Home Retract Mechanical Proximity Limit *)

    (* =====================================================================================
       SECTION 7: ROBOTIC EXTRACTOR, SPRAY MANIFOLD & THERMAL TRANSDUCERS
       ===================================================================================== *)
    bExtractorPartPresent           : BOOL := FALSE;    (* 6-Axis Extractor Robot Gripper Optical/Vacuum Part Detect *)
    bExtractorArmClear              : BOOL := TRUE;     (* 6-Axis Extractor Robot Arm Clear of Platen Daylight Stroke *)
    bSprayerInDieClearance          : BOOL := FALSE;    (* Multi-Axis Die Spray Robot Arm Centered Between Open Platens *)
    bSprayerCycleDone               : BOOL := FALSE;    (* Die Spray Cassette Lubrication & Blow-Dry Cycle Complete *)
    bSprayerHomeSafe                : BOOL := TRUE;     (* Die Spray Robot Retracted to Safe Parked Interference Envelope *)
    rDieTempFixed_degC              : REAL := 205.0;    (* Fixed Die Half Embedded Pt100 Core Insert Temperature [deg C] *)
    rDieTempMoving_degC             : REAL := 195.0;    (* Moving Die Half Embedded Pt100 Core Insert Temperature [deg C] *)
    rHydraulicOilTemp_degC          : REAL := 48.0;     (* Main Hydraulic Power Unit Mineral Oil Reservoir Temp [deg C] *)
    rDieLubeLinePress_bar           : REAL := 5.2;      (* Pressurized Release Agent Lubricant Supply Line Pressure [bar] *)
    rAirBlastLinePress_bar          : REAL := 6.5;      (* High-Velocity Die Cavity Compressed Air Purge Header Press [bar] *)
END_VAR
""")
    
    # -------------------------------------------------------------------------
    # PART 2: VAR_OUTPUT Block
    # -------------------------------------------------------------------------
    parts.append("""
VAR_OUTPUT
    (* =====================================================================================
       SECTION 1: HYDRAULIC ACTUATION COMMANDS & PILOT PROPORTIONAL VALVES
       ===================================================================================== *)
    rToggleClampValve_pct           : REAL := 0.0;      (* Proportional Toggle Clamp Servo Directional Valve Command [%] *)
    rInjectionServoSpool_pct        : REAL := 0.0;      (* High-Dynamic Main Injection Servovalve Spool Command [%] *)
    bFastShotCartridgeOpen          : BOOL := FALSE;    (* High-Speed Accumulator Discharge Cartridge Valve Pilot Solenoid *)
    bIntensifierPoppetFire          : BOOL := FALSE;    (* Ultra-Fast Intensifier Firing Poppet Cartridge Pilot Solenoid *)
    rIntensifierRegValve_pct        : REAL := 0.0;      (* Intensification Pressure Closed-Loop Proportional Regulator [%] *)
    bAccumulatorChargeCmd           : BOOL := FALSE;    (* Variable Displacement Pump Swashplate Accumulator Charge Pilot *)
    bTieBarNutAdjustFwd             : BOOL := FALSE;    (* Motorized Tie-Bar Parallelism Trim Adjustment Forward Step *)
    bTieBarNutAdjustRev             : BOOL := FALSE;    (* Motorized Tie-Bar Parallelism Trim Adjustment Reverse Step *)
    iTieBarTargetNutIndex           : INT := 0;         (* Tie-Bar Nut Channel Under Active Balancing Trim (1..4) *)

    (* =====================================================================================
       SECTION 2: VACUUM, CORES, EJECTORS & AUXILIARY SOLENOIDS
       ===================================================================================== *)
    bVacuumGateValveOpen            : BOOL := FALSE;    (* High-Speed Cavity Vacuum Exhaust Isolation Gate Valve Solenoid *)
    bVacuumPumpBypass               : BOOL := FALSE;    (* Liquid Ring / Roots Vacuum Blower System Suction Bypass Valve *)
    bCore1ExtendCmd                 : BOOL := FALSE;    (* Hydraulic Slide Core 1 Forward Insert Directional Solenoid *)
    bCore1RetractCmd                : BOOL := FALSE;    (* Hydraulic Slide Core 1 Retract Pull Directional Solenoid *)
    bCore2ExtendCmd                 : BOOL := FALSE;    (* Hydraulic Slide Core 2 Forward Insert Directional Solenoid *)
    bCore2RetractCmd                : BOOL := FALSE;    (* Hydraulic Slide Core 2 Retract Pull Directional Solenoid *)
    bEjectorExtendCmd               : BOOL := FALSE;    (* Hydraulic Ejector Pins Forward Ejection Solenoid *)
    bEjectorRetractCmd              : BOOL := FALSE;    (* Hydraulic Ejector Pins Home Retraction Solenoid *)

    (* =====================================================================================
       SECTION 3: ROBOTIC INTERFACE PERMISSIVES & SYNCHRONIZATION HANDSHAKES
       ===================================================================================== *)
    bLadlerPermissive               : BOOL := FALSE;    (* Platen Locked & Vacuum Ready: Permissive for Ladler to Pour *)
    bLadlerStartPourCmd             : BOOL := FALSE;    (* Trigger Command to Robotic Ladler to Begin Programmed Pour *)
    bExtractorPermissive            : BOOL := FALSE;    (* Die Open & Ejected: Permissive for Extractor Robot to Enter *)
    bExtractorStartTakeoutCmd       : BOOL := FALSE;    (* Trigger Command to Extractor Robot to Grip and Extract Casting *)
    bSprayerPermissive              : BOOL := FALSE;    (* Part Extracted & Clear: Permissive for Spray Robot to Enter *)
    bSprayerStartLubeCmd            : BOOL := FALSE;    (* Trigger Command to Sprayer Robot to Execute Lube & Blow Routine *)
    wSprayerZoneMask                : WORD := 16#0000;  (* Multi-Zone Die Spray Lubrication Cassette Active Zone Mask *)

    (* =====================================================================================
       SECTION 4: REAL-TIME FOUNDRY PROCESS DIAGNOSTIC TELEMETRY
       ===================================================================================== *)
    rTotalClampTonnage_tons         : REAL := 0.0;      (* Real-Time Total Verified Toggle Clamp Locking Tonnage [metric tons] *)
    rTieBarImbalance_pct            : REAL := 0.0;      (* Calculated Tie-Bar Micro-Strain Asymmetric Imbalance Ratio [%] *)
    rVotedVacuumPressure_mbar       : REAL := 1013.0;   (* 2oo3 TMR High-Reliability Voted Mold Cavity Vacuum Pressure [mbar] *)
    rPhase1Velocity_mps             : REAL := 0.0;      (* Phase 1 Slow-Shot Measured Average Plunger Linear Velocity [m/s] *)
    rPhase2PeakVelocity_mps         : REAL := 0.0;      (* Phase 2 Fast-Shot Peak Injection Plunger Velocity Achieved [m/s] *)
    rCavityFillTime_ms              : REAL := 0.0;      (* Measured Dynamic Cavity Filling Duration from In-Gate to Impact [ms] *)
    rPhase3PeakPressure_bar         : REAL := 0.0;      (* Phase 3 Peak Specific Intensification Hydraulic Pressure [bar] *)
    rIntensificationRiseTime_ms     : REAL := 0.0;      (* Intensifier Pressure Rise Time (10% to 90% Target Pressure) [ms] *)
    rMeasuredBiscuitThickness_mm    : REAL := 0.0;      (* Solidified Molten Aluminum Biscuit Residual Cake Thickness [mm] *)
    rCurrentCycleTime_s             : REAL := 0.0;      (* Elapsed Operational Duration for Active Casting Cycle [s] *)
    rLastCycleTime_s                : REAL := 0.0;      (* Total Completed Duration for Previous Operational Cycle [s] *)
    diTotalShotCounter              : DINT := 0;        (* Cumulative Lifetime Die Casting Shot Injection Stroke Count *)
    diGoodPartsCounter              : DINT := 0;        (* Total Approved Castings Conforming to Metallurgical Tolerance *)
    diRejectedPartsCounter          : DINT := 0;        (* Total Castings Scrapped Due to Out-of-Spec Shot Curve or Vacuum *)

    (* =====================================================================================
       SECTION 5: FSM STATUS & ISA-18.2 INTEGRATED ALARM TELEMETRY WORDS
       ===================================================================================== *)
    iCurrentFsmStage                : INT := 10;        (* Current Active 12-Stage Heavy Foundry Operational FSM State *)
    dwSystemStatusWord1             : DWORD := 16#0;    (* System Hardware Interlocks, Permissives & Robot Handshakes *)
    dwSystemStatusWord2             : DWORD := 16#0;    (* Subsystem Quality Flags, Shot Trajectory Health & Vacuum Bits *)
    dwIsaAlarmWord1                 : DWORD := 16#0;    (* ISA-18.2 Priority 1 / Emergency Unrecoverable Trip Bits *)
    dwIsaAlarmWord2                 : DWORD := 16#0;    (* ISA-18.2 Priority 2 / High Severity Operational Warning Bits *)
    dwIsaAlarmWord3                 : DWORD := 16#0;    (* ISA-18.2 Unacknowledged Alarm Latch Registry *)
    dwIsaAlarmWord4                 : DWORD := 16#0;    (* ISA-18.2 Bypassed / Suppressed Fault Mask Registry *)
    bCriticalTripActive             : BOOL := FALSE;    (* Master Critical Cell Interlock Emergency Shutdown Active *)
    bWarningActive                  : BOOL := FALSE;    (* Operational Quality Degradation Warning Annunciation Active *)
END_VAR
""")

    # -------------------------------------------------------------------------
    # PART 3: VAR Block (State-space, MPC, 2oo3 TMR, FSM, Alarms)
    # -------------------------------------------------------------------------
    parts.append("""
VAR
    (* =====================================================================================
       SECTION 1: DISCRETE 10-STATE HYDRO-MECHANICAL SYSTEM MATRICES (ZOH Ts = 1.0 ms)
       x[k+1] = A * x[k] + B * u[k] + L * (y[k] - C * x[k])
       ===================================================================================== *)
    aMatrixA                        : ARRAY[1..10, 1..10] OF REAL;  (* State Transition Dynamic Plant Matrix (10x10) *)
    aMatrixB                        : ARRAY[1..10, 1..8] OF REAL;   (* Actuator Control Input Matrix (10x8) *)
    aMatrixC                        : ARRAY[1..6, 1..10] OF REAL;   (* Process Measurement Output Matrix (6x10) *)
    aMatrixD                        : ARRAY[1..6, 1..8] OF REAL;    (* Feedthrough Direct Transmission Matrix (6x8) *)
    aObserverGainL                  : ARRAY[1..10, 1..6] OF REAL;   (* Discrete Luenberger Observer Correction Gain (10x6) *)

    (* Observer State Vectors *)
    aStateX                         : ARRAY[1..10] OF REAL;         (* True Estimated Process Physical State Vector *)
    aStateX_hat                     : ARRAY[1..10] OF REAL;         (* A-Priori Propagated Observer State Vector *)
    aStateX_pred                    : ARRAY[1..10] OF REAL;         (* Multi-Step MPC Trajectory Prediction State Vector *)
    aInputU                         : ARRAY[1..8] OF REAL;          (* Scaled Actuation Control Vector to Physical Plant *)
    aOutputY                        : ARRAY[1..6] OF REAL;          (* Actual Sensor Measurement Vector From Transducers *)
    aOutputY_hat                    : ARRAY[1..6] OF REAL;          (* Estimated Process Measurement Vector *)
    aOutputResidual                 : ARRAY[1..6] OF REAL;          (* Innovation Error Residual Vector (y - y_hat) *)
    bMatricesInitialized            : BOOL := FALSE;                (* One-Time State-Space Coefficients Initialization Flag *)

    (* =====================================================================================
       SECTION 2: RECEDING-HORIZON MPC VELOCITY & PRESSURE OPTIMIZATION (Np=5, Nc=3)
       ===================================================================================== *)
    aMatrixQ                        : ARRAY[1..10] OF REAL;         (* Diagonal State Error Quadratic Weight Penalties *)
    aMatrixR                        : ARRAY[1..8] OF REAL;          (* Diagonal Actuator Slew Rate Quadratic Penalties *)
    aMatrixP                        : ARRAY[1..10] OF REAL;         (* Terminal State Trajectory Tracking Penalties *)
    aTargetStateRef                 : ARRAY[1..10] OF REAL;         (* Dynamic Trajectory Reference State Vector Target *)
    aMpcStatePred                   : ARRAY[1..5, 1..10] OF REAL;   (* Receding Prediction Horizon Predicted States (5x10) *)
    aMpcDeltaU                      : ARRAY[1..3, 1..8] OF REAL;    (* Control Horizon Incremental Actuation Vector (3x8) *)
    rMpcBestCost                    : REAL := 1.0E30;               (* Running Minimal Quadratic Cost Metric *)
    rMpcCandidateCost               : REAL := 0.0;                  (* Evaluated Cost Metric for Candidate Trajectory *)
    rOptimalSpoolCmd                : REAL := 0.0;                  (* Computed Unconstrained Optimal Servovalve Spool *)
    rSlewRateLimit_pct              : REAL := 25.0;                 (* Maximum Permissible Valve Spool Slew Rate [%/ms] *)
    rSpoolDeadband_pct              : REAL := 7.5;                  (* Servovalve Mechanical Spool Overlap Deadband [%] *)

    (* =====================================================================================
       SECTION 3: 2oo3 TMR VACUUM VOTING, TIE-BAR BALANCING & SENSOR HEALTH
       ===================================================================================== *)
    bVacSens1_Healthy               : BOOL := TRUE;                 (* Cavity Vacuum Sensor Channel 1 Plausibility Status *)
    bVacSens2_Healthy               : BOOL := TRUE;                 (* Cavity Vacuum Sensor Channel 2 Plausibility Status *)
    bVacSens3_Healthy               : BOOL := TRUE;                 (* Cavity Vacuum Sensor Channel 3 Plausibility Status *)
    rVacDiff_12                     : REAL := 0.0;                  (* Absolute Deviation Between Vacuum Channel 1 and 2 [mbar] *)
    rVacDiff_23                     : REAL := 0.0;                  (* Absolute Deviation Between Vacuum Channel 2 and 3 [mbar] *)
    rVacDiff_31                     : REAL := 0.0;                  (* Absolute Deviation Between Vacuum Channel 3 and 1 [mbar] *)
    tVacDiscrepancyTimer            : TON;                          (* Persistent Sensor Discrepancy Debounce Timer *)
    iVacVotingHealthMode            : INT := 3;                     (* Vacuum Health Mode: 3=2oo3, 2=1oo2, 1=1oo1, 0=Fail *)
    rTieBarTonnage_UL               : REAL := 0.0;                  (* Tie-Bar 1 Upper-Left Measured Force [metric tons] *)
    rTieBarTonnage_UR               : REAL := 0.0;                  (* Tie-Bar 2 Upper-Right Measured Force [metric tons] *)
    rTieBarTonnage_LL               : REAL := 0.0;                  (* Tie-Bar 3 Lower-Left Measured Force [metric tons] *)
    rTieBarTonnage_LR               : REAL := 0.0;                  (* Tie-Bar 4 Lower-Right Measured Force [metric tons] *)
    rTieBarMean_tons                : REAL := 0.0;                  (* Calculated Arithmetic Mean Force Per Tie-Bar [tons] *)
    rTieBarMax_tons                 : REAL := 0.0;                  (* Maximum Recorded Tie-Bar Force Among All 4 Bars [tons] *)
    rTieBarMin_tons                 : REAL := 0.0;                  (* Minimum Recorded Tie-Bar Force Among All 4 Bars [tons] *)
    tPlungerEncoderDiscrepancyTimer : TON;                          (* Discrepancy Timer for Dual Magnetostrictive SSI Probes *)

    (* =====================================================================================
       SECTION 4: INJECTION PROFILE TRAJECTORY GENERATION & METALLURGY
       ===================================================================================== *)
    rGatePosition_mm                : REAL := 450.0;                (* In-Gate Ingress Position Setpoint for Phase 2 Fast Shot [mm] *)
    rBrakingPosition_mm             : REAL := 720.0;                (* Terminal Braking Deceleration Trigger Position [mm] *)
    rNominalStrokeLimit_mm          : REAL := 780.0;                (* Hard Mechanical Plunger Stroke Full Travel Limit [mm] *)
    rPhase1TargetVelocity_mps       : REAL := 0.28;                 (* Critical Wave Anti-Rollover Slow Shot Target Velocity [m/s] *)
    rPhase2TargetVelocity_mps       : REAL := 6.80;                 (* Dynamic Cavity In-Filling Fast Shot Target Velocity [m/s] *)
    rPhase3TargetPressure_bar       : REAL := 1150.0;               (* Specific Molten Aluminum Consolidation Pressure [bar] *)
    bInGateTriggerCrossed           : BOOL := FALSE;                (* Plunger In-Gate Crossing Event Latch *)
    bCavityFullImpactDetected       : BOOL := FALSE;                (* Cavity Hydraulic End-of-Fill Impact Spike Detected *)
    rIntensifierStartTimestamp_s    : REAL := 0.0;                  (* Timer Timestamp when Intensifier Poppet Fired [s] *)
    rIntensifierPressure10Pct_bar   : REAL := 115.0;                (* 10% Pressure Benchmark for Rise Time Calculation [bar] *)
    rIntensifierPressure90Pct_bar   : REAL := 1035.0;               (* 90% Pressure Benchmark for Rise Time Calculation [bar] *)
    rTimeAt10Pct_s                  : REAL := 0.0;                  (* Timestamp when Intensifier Pressure Crossed 10% [s] *)
    rTimeAt90Pct_s                  : REAL := 0.0;                  (* Timestamp when Intensifier Pressure Crossed 90% [s] *)
    bRiseTimeCalcDone               : BOOL := FALSE;                (* Flag Indicating Rise Time Measurement Complete *)

    (* Solidification & Biscuit Thickness Calculations *)
    rSolidificationDwellDuration_s  : REAL := 12.0;                 (* Required Holding Duration for Metallurgical Freezing [s] *)
    rSolidificationFront_mm         : REAL := 0.0;                  (* Calculated 1D Stefan Solidification Front Depth [mm] *)
    rStefanSolidificationConst_K    : REAL := 3.25;                 (* Stefan Rate Constant for H13 Tool Steel Chill [mm/s^0.5] *)
    rSolidificationTimerAccum_s     : REAL := 0.0;                  (* Integrated Elapsed Time in Solidification Dwell [s] *)

    (* =====================================================================================
       SECTION 5: 12-STAGE OPERATIONAL FOUNDRY FINITE STATE MACHINE (FSM)
       ===================================================================================== *)
    iFsmState                       : INT := 10;                    (* Active Operational FSM State Index (10..120, 999) *)
    iFsmPreviousState               : INT := 10;                    (* Preceding Cycle State Index for Diagnostic Tracking *)
    rFsmStageTimer_s                : REAL := 0.0;                  (* Elapsed Time Spent within Current Operational State [s] *)
    rCycleDurationAccum_s           : REAL := 0.0;                  (* Continuous Active Cycle Timer Accumulator [s] *)
    tMoldProtectWatchdog            : TON;                          (* Low-Pressure Mold Protection Safety Timeout Timer *)
    tTonnageLockWatchdog            : TON;                          (* Tie-Bar Tonnage Build-up Timeout Timer *)
    tLadlePourWatchdog              : TON;                          (* Robotic Ladler Liquid Metal Pouring Timeout Timer *)
    tVacuumDrawWatchdog             : TON;                          (* Cavity Vacuum Evacuation Rate Timeout Timer *)
    tSlowShotWatchdog               : TON;                          (* Phase 1 Plunger Slow Shot Stroke Timeout Timer *)
    tFastShotWatchdog               : TON;                          (* Phase 2 Dynamic Cavity Filling Safety Timeout Timer *)
    tIntensifierWatchdog            : TON;                          (* Phase 3 Pressure Consolidation Rise Timeout Timer *)
    tDieCrackWatchdog               : TON;                          (* Platen High-Tonnage Breakaway Crack Timeout Timer *)
    tExtractorWatchdog              : TON;                          (* 6-Axis Part Extraction Takeout Sequence Timeout Timer *)
    tSprayerWatchdog                : TON;                          (* Die Lubrication & Air Purge Cycle Timeout Timer *)

    (* =====================================================================================
       SECTION 6: ISA-18.2 MULTI-TIERED ALARM MATRIX TRIP POINTS & DEADBANDS
       ===================================================================================== *)
    c_rTonnage_HH                   : REAL := 3700.0;               (* Tie-Bar Overload High-High Emergency Trip Limit [tons] *)
    c_rTonnage_H                    : REAL := 3580.0;               (* Tie-Bar Force High Warning Warning Limit [tons] *)
    c_rTonnage_L                    : REAL := 3350.0;               (* Clamping Force Low Inadequate Lock Limit [tons] *)
    c_rTonnage_LL                   : REAL := 3150.0;               (* Clamping Force Low-Low Under-Tonnage Trip Limit [tons] *)
    c_rTonnageDeadband              : REAL := 30.0;                 (* Tie-Bar Tonnage Alarm Recovery Hysteresis Deadband [tons] *)
    c_rImbalance_H                  : REAL := 6.5;                  (* Tie-Bar Quadrant Imbalance High Warning Ratio [%] *)
    c_rImbalance_HH                 : REAL := 10.0;                 (* Tie-Bar Quadrant Imbalance Critical Trip Limit [%] *)
    c_rVacuum_H                     : REAL := 80.0;                 (* Cavity Vacuum Insufficient Warning Limit [mbar] *)
    c_rVacuum_HH                    : REAL := 150.0;                (* Cavity Vacuum Gross Atmosphere Leak Trip Limit [mbar] *)
    c_rIntensPress_L                : REAL := 980.0;                (* Phase 3 Consolidation Pressure Inadequate Warning [bar] *)
    c_rIntensPress_LL               : REAL := 850.0;                (* Phase 3 Consolidation Pressure Failure Critical Trip [bar] *)
    c_rIntensRiseTime_H             : REAL := 18.0;                 (* Intensifier Piston Rise Time Sluggish Warning Limit [ms] *)
    c_rIntensRiseTime_HH            : REAL := 25.0;                 (* Intensifier Piston Rise Time Failure Critical Trip [ms] *)
    c_rBiscuit_LL                   : REAL := 15.0;                 (* Metal Shot Cake Flash Under-Thickness Critical Trip [mm] *)
    c_rBiscuit_L                    : REAL := 20.0;                 (* Biscuit Residual Cake Under-Thickness Warning [mm] *)
    c_rBiscuit_H                    : REAL := 42.0;                 (* Biscuit Residual Cake Over-Thickness Warning [mm] *)
    c_rBiscuit_HH                   : REAL := 55.0;                 (* Biscuit Residual Cake Over-Thickness Critical Trip [mm] *)
    c_rOilTemp_H                    : REAL := 55.0;                 (* Hydraulic Power Reservoir Oil Temp High Warning [deg C] *)
    c_rOilTemp_HH                   : REAL := 65.0;                 (* Hydraulic Power Reservoir Oil Temp Emergency Trip [deg C] *)
    c_rMetalTemp_L                  : REAL := 670.0;                (* Furnace Dosing Bath Liquid Temperature Low Warning [deg C] *)
    c_rMetalTemp_H                  : REAL := 735.0;                (* Furnace Dosing Bath Liquid Temperature High Warning [deg C] *)

    (* Loop Counters, Array Indices & Math Buffers *)
    iIdxRow                         : INT := 1;                     (* Matrix Row Iterator Index *)
    iIdxCol                         : INT := 1;                     (* Matrix Column Iterator Index *)
    iIdxHoriz                       : INT := 1;                     (* MPC Prediction Horizon Step Index *)
    iIdxInput                       : INT := 1;                     (* Actuator Control Input Iterator Index *)
    rAccumulatorVar                 : REAL := 0.0;                  (* Multi-Purpose High-Precision Summation Register *)
    rTempCalcDelta                  : REAL := 0.0;                  (* Temporary Scratch Register for Difference Floating Points *)
    rTieBarModulusElasticity        : REAL := 210000.0;             (* Chrome-Nickel Steel Modulus E [N/mm^2] *)
    rTieBarArea_mm2                 : REAL := 61575.2;              (* Solid Circular Tie-Bar Cross Section Area [mm^2] *)
    rTieBarGaugeLength_mm           : REAL := 8500.0;               (* Active Strain Sensor Gauge Span Length [mm] *)
END_VAR
""")

    # -------------------------------------------------------------------------
    # PART 4: Phase 1: 2oo3 TMR Voting & 4 Tie-Bar Strain Gauge Force Balancing
    # -------------------------------------------------------------------------
    parts.append("""
(* =========================================================================================
   PHASE 1: 2oo3 TMR CAVITY VACUUM SENSOR VOTING & 4 TIE-BAR STRAIN BALANCING
   ========================================================================================= *)

(* --- 1.1: 2oo3 TMR Cavity Vacuum Pressure Sensor Voting & Health Discrimination --- *)
(* Calculate absolute inter-channel discrepancies across all three transducers *)
rVacDiff_12 := ABS(rVacuumPressure_Ch1_mbar - rVacuumPressure_Ch2_mbar);
rVacDiff_23 := ABS(rVacuumPressure_Ch2_mbar - rVacuumPressure_Ch3_mbar);
rVacDiff_31 := ABS(rVacuumPressure_Ch3_mbar - rVacuumPressure_Ch1_mbar);

(* Audit individual channel plausibility limits [0.0 mbar to 1050.0 mbar] *)
bVacSens1_Healthy := (rVacuumPressure_Ch1_mbar >= 0.0) AND (rVacuumPressure_Ch1_mbar <= 1050.0);
bVacSens2_Healthy := (rVacuumPressure_Ch2_mbar >= 0.0) AND (rVacuumPressure_Ch2_mbar <= 1050.0);
bVacSens3_Healthy := (rVacuumPressure_Ch3_mbar >= 0.0) AND (rVacuumPressure_Ch3_mbar <= 1050.0);

(* 2oo3 Voting Logic with Deterministic Bumpless Degradation Mode *)
IF bVacSens1_Healthy AND bVacSens2_Healthy AND bVacSens3_Healthy THEN
    (* All three channels electrically healthy: evaluate median cross-check *)
    IF (rVacDiff_12 <= 20.0) AND (rVacDiff_23 <= 20.0) AND (rVacDiff_31 <= 20.0) THEN
        (* Standard 2oo3 Triple Redundancy: select arithmetic median of 3 channels *)
        IF ((rVacuumPressure_Ch1_mbar >= rVacuumPressure_Ch2_mbar) AND (rVacuumPressure_Ch1_mbar <= rVacuumPressure_Ch3_mbar)) OR
           ((rVacuumPressure_Ch1_mbar >= rVacuumPressure_Ch3_mbar) AND (rVacuumPressure_Ch1_mbar <= rVacuumPressure_Ch2_mbar)) THEN
            rVotedVacuumPressure_mbar := rVacuumPressure_Ch1_mbar;
        ELSIF ((rVacuumPressure_Ch2_mbar >= rVacuumPressure_Ch1_mbar) AND (rVacuumPressure_Ch2_mbar <= rVacuumPressure_Ch3_mbar)) OR
              ((rVacuumPressure_Ch2_mbar >= rVacuumPressure_Ch3_mbar) AND (rVacuumPressure_Ch2_mbar <= rVacuumPressure_Ch1_mbar)) THEN
            rVotedVacuumPressure_mbar := rVacuumPressure_Ch2_mbar;
        ELSE
            rVotedVacuumPressure_mbar := rVacuumPressure_Ch3_mbar;
        END_IF;
        iVacVotingHealthMode := 3; (* Full 2oo3 TMR Health *)
    ELSIF (rVacDiff_12 <= 20.0) THEN
        (* Channel 3 deviates: vote average of Ch1 and Ch2 *)
        rVotedVacuumPressure_mbar := (rVacuumPressure_Ch1_mbar + rVacuumPressure_Ch2_mbar) * 0.5;
        iVacVotingHealthMode := 2; (* Degraded 1oo2 Mode *)
    ELSIF (rVacDiff_23 <= 20.0) THEN
        (* Channel 1 deviates: vote average of Ch2 and Ch3 *)
        rVotedVacuumPressure_mbar := (rVacuumPressure_Ch2_mbar + rVacuumPressure_Ch3_mbar) * 0.5;
        iVacVotingHealthMode := 2; (* Degraded 1oo2 Mode *)
    ELSIF (rVacDiff_31 <= 20.0) THEN
        (* Channel 2 deviates: vote average of Ch1 and Ch3 *)
        rVotedVacuumPressure_mbar := (rVacuumPressure_Ch1_mbar + rVacuumPressure_Ch3_mbar) * 0.5;
        iVacVotingHealthMode := 2; (* Degraded 1oo2 Mode *)
    ELSE
        (* All channels disparate: select lowest conservative vacuum pressure *)
        rVotedVacuumPressure_mbar := rVacuumPressure_Ch1_mbar;
        IF rVacuumPressure_Ch2_mbar < rVotedVacuumPressure_mbar THEN
            rVotedVacuumPressure_mbar := rVacuumPressure_Ch2_mbar;
        END_IF;
        IF rVacuumPressure_Ch3_mbar < rVotedVacuumPressure_mbar THEN
            rVotedVacuumPressure_mbar := rVacuumPressure_Ch3_mbar;
        END_IF;
        iVacVotingHealthMode := 1; (* Degraded 1oo1 Mode *)
    END_IF;
ELSIF bVacSens1_Healthy AND bVacSens2_Healthy THEN
    rVotedVacuumPressure_mbar := (rVacuumPressure_Ch1_mbar + rVacuumPressure_Ch2_mbar) * 0.5;
    iVacVotingHealthMode := 2;
ELSIF bVacSens2_Healthy AND bVacSens3_Healthy THEN
    rVotedVacuumPressure_mbar := (rVacuumPressure_Ch2_mbar + rVacuumPressure_Ch3_mbar) * 0.5;
    iVacVotingHealthMode := 2;
ELSIF bVacSens1_Healthy AND bVacSens3_Healthy THEN
    rVotedVacuumPressure_mbar := (rVacuumPressure_Ch1_mbar + rVacuumPressure_Ch3_mbar) * 0.5;
    iVacVotingHealthMode := 2;
ELSIF bVacSens1_Healthy THEN
    rVotedVacuumPressure_mbar := rVacuumPressure_Ch1_mbar;
    iVacVotingHealthMode := 1;
ELSIF bVacSens2_Healthy THEN
    rVotedVacuumPressure_mbar := rVacuumPressure_Ch2_mbar;
    iVacVotingHealthMode := 1;
ELSIF bVacSens3_Healthy THEN
    rVotedVacuumPressure_mbar := rVacuumPressure_Ch3_mbar;
    iVacVotingHealthMode := 1;
ELSE
    (* Total Sensor Triplet Failure *)
    rVotedVacuumPressure_mbar := 1013.0;
    iVacVotingHealthMode := 0; (* Failed *)
END_IF;

(* Discrepancy Debounce Timer for ISA-18.2 Sensor Fault Annunciation *)
tVacDiscrepancyTimer(IN := (iVacVotingHealthMode < 3), PT := T#2S);

(* --- 1.2: Dual Magnetostrictive Plunger Position Encoder Cross-Check --- *)
tPlungerEncoderDiscrepancyTimer(IN := (ABS(rPlungerPosition_mm - rPlungerPositionAux_mm) > 3.0), PT := T#100MS);

(* --- 1.3: 4 Tie-Bar Strain-to-Tonnage Conversion & Dynamic Imbalance Balancing --- *)
(* Formula: Force [N] = (epsilon * 10^-6) * E [N/mm^2] * Area [mm^2] *)
(* Conversion to Metric Tons: Tonnage = Force [N] / 9806.65 N/ton *)
rTieBarTonnage_UL := (rTieBarStrain_UL_ue * 1.0E-6 * rTieBarModulusElasticity * rTieBarArea_mm2) / 9806.65;
rTieBarTonnage_UR := (rTieBarStrain_UR_ue * 1.0E-6 * rTieBarModulusElasticity * rTieBarArea_mm2) / 9806.65;
rTieBarTonnage_LL := (rTieBarStrain_LL_ue * 1.0E-6 * rTieBarModulusElasticity * rTieBarArea_mm2) / 9806.65;
rTieBarTonnage_LR := (rTieBarStrain_LR_ue * 1.0E-6 * rTieBarModulusElasticity * rTieBarArea_mm2) / 9806.65;

(* Enforce non-negative clamp forces *)
IF rTieBarTonnage_UL < 0.0 THEN rTieBarTonnage_UL := 0.0; END_IF;
IF rTieBarTonnage_UR < 0.0 THEN rTieBarTonnage_UR := 0.0; END_IF;
IF rTieBarTonnage_LL < 0.0 THEN rTieBarTonnage_LL := 0.0; END_IF;
IF rTieBarTonnage_LR < 0.0 THEN rTieBarTonnage_LR := 0.0; END_IF;

(* Total 3,500-Ton Toggle Clamping Force Summation *)
rTotalClampTonnage_tons := rTieBarTonnage_UL + rTieBarTonnage_UR + rTieBarTonnage_LL + rTieBarTonnage_LR;
rTieBarMean_tons := rTotalClampTonnage_tons * 0.25;

(* Identify Maximum and Minimum Tie-Bar Force for Imbalance Auditing *)
rTieBarMax_tons := rTieBarTonnage_UL;
IF rTieBarTonnage_UR > rTieBarMax_tons THEN rTieBarMax_tons := rTieBarTonnage_UR; END_IF;
IF rTieBarTonnage_LL > rTieBarMax_tons THEN rTieBarMax_tons := rTieBarTonnage_LL; END_IF;
IF rTieBarTonnage_LR > rTieBarMax_tons THEN rTieBarMax_tons := rTieBarTonnage_LR; END_IF;

rTieBarMin_tons := rTieBarTonnage_UL;
IF rTieBarTonnage_UR < rTieBarMin_tons THEN rTieBarMin_tons := rTieBarTonnage_UR; END_IF;
IF rTieBarTonnage_LL < rTieBarMin_tons THEN rTieBarMin_tons := rTieBarTonnage_LL; END_IF;
IF rTieBarTonnage_LR < rTieBarMin_tons THEN rTieBarMin_tons := rTieBarTonnage_LR; END_IF;

(* Percentage Imbalance Calculation relative to Average Bar Force *)
IF rTieBarMean_tons > 100.0 THEN
    rTieBarImbalance_pct := ((rTieBarMax_tons - rTieBarMin_tons) / rTieBarMean_tons) * 100.0;
ELSE
    rTieBarImbalance_pct := 0.0;
END_IF;

(* Dynamic Tie-Bar Motorized Nut Trim Calculation *)
IF (iFsmState = 20) AND (rTieBarImbalance_pct > c_rImbalance_H) AND (rTotalClampTonnage_tons > 2000.0) THEN
    (* Determine which quadrant requires corrective nut motion *)
    IF rTieBarMax_tons = rTieBarTonnage_UL THEN
        iTieBarTargetNutIndex := 1; (* Relax UL nut *)
        bTieBarNutAdjustRev := TRUE;
        bTieBarNutAdjustFwd := FALSE;
    ELSIF rTieBarMax_tons = rTieBarTonnage_UR THEN
        iTieBarTargetNutIndex := 2; (* Relax UR nut *)
        bTieBarNutAdjustRev := TRUE;
        bTieBarNutAdjustFwd := FALSE;
    ELSIF rTieBarMax_tons = rTieBarTonnage_LL THEN
        iTieBarTargetNutIndex := 3; (* Relax LL nut *)
        bTieBarNutAdjustRev := TRUE;
        bTieBarNutAdjustFwd := FALSE;
    ELSE
        iTieBarTargetNutIndex := 4; (* Relax LR nut *)
        bTieBarNutAdjustRev := TRUE;
        bTieBarNutAdjustFwd := FALSE;
    END_IF;
ELSE
    bTieBarNutAdjustFwd := FALSE;
    bTieBarNutAdjustRev := FALSE;
    iTieBarTargetNutIndex := 0;
END_IF;
""")

    # -------------------------------------------------------------------------
    # PART 5: Phase 2: Discrete State-Space Model Initialization & Observer
    # -------------------------------------------------------------------------
    parts.append("""
(* =========================================================================================
   PHASE 2: DISCRETE 10-STATE HYDRO-MECHANICAL SYSTEM PROPAGATION & OBSERVER
   x[k+1] = A * x[k] + B * u[k] + L * (y[k] - C * x[k])
   ========================================================================================= *)

(* --- 2.1: One-Time Initialization of High-Fidelity Discrete Hydrodynamic Matrices --- *)
IF NOT bMatricesInitialized THEN
    (* Row 1: Plunger Position s_p [mm] *)
    aMatrixA[1, 1] := 1.0000; aMatrixA[1, 2] := 0.0010; aMatrixA[1, 3] := 0.0000005; aMatrixA[1, 4] := 0.0000;
    aMatrixA[1, 5] := 0.0000; aMatrixA[1, 6] := 0.0000; aMatrixA[1, 7] := 0.0000;    aMatrixA[1, 8] := 0.0000;
    aMatrixA[1, 9] := 0.0000; aMatrixA[1, 10]:= 0.0000;

    (* Row 2: Plunger Velocity v_p [m/s] *)
    aMatrixA[2, 1] := 0.0000; aMatrixA[2, 2] := 0.9850; aMatrixA[2, 3] := 0.00095;   aMatrixA[2, 4] := 0.0012;
    aMatrixA[2, 5] :=-0.0008; aMatrixA[2, 6] := 0.0005; aMatrixA[2, 7] := 0.0000;    aMatrixA[2, 8] := 0.0000;
    aMatrixA[2, 9] :=-0.0018; aMatrixA[2, 10]:=-0.0004;

    (* Row 3: Plunger Acceleration a_p [m/s^2] *)
    aMatrixA[3, 1] := 0.0000; aMatrixA[3, 2] :=-0.1250; aMatrixA[3, 3] := 0.8800;    aMatrixA[3, 4] := 1.1500;
    aMatrixA[3, 5] :=-0.7800; aMatrixA[3, 6] := 0.4800; aMatrixA[3, 7] := 0.0000;    aMatrixA[3, 8] := 0.0000;
    aMatrixA[3, 9] :=-1.6500; aMatrixA[3, 10]:=-0.3200;

    (* Row 4: Injection Cylinder Head Pressure P_head [bar] *)
    aMatrixA[4, 1] := 0.0000; aMatrixA[4, 2] :=-0.0850; aMatrixA[4, 3] :=-0.0042;   aMatrixA[4, 4] := 0.9650;
    aMatrixA[4, 5] := 0.0000; aMatrixA[4, 6] := 0.0320; aMatrixA[4, 7] := 0.0000;    aMatrixA[4, 8] := 0.0150;
    aMatrixA[4, 9] := 0.0050; aMatrixA[4, 10]:= 0.0000;

    (* Row 5: Injection Cylinder Rod Back-Pressure P_rod [bar] *)
    aMatrixA[5, 1] := 0.0000; aMatrixA[5, 2] := 0.0650; aMatrixA[5, 3] := 0.0031;    aMatrixA[5, 4] := 0.0000;
    aMatrixA[5, 5] := 0.9450; aMatrixA[5, 6] := 0.0000; aMatrixA[5, 7] := 0.0000;    aMatrixA[5, 8] := 0.0000;
    aMatrixA[5, 9] := 0.0000; aMatrixA[5, 10]:= 0.0000;

    (* Row 6: Nitrogen Accumulator Pressure P_acc [bar] *)
    aMatrixA[6, 1] := 0.0000; aMatrixA[6, 2] :=-0.0350; aMatrixA[6, 3] :=-0.0018;   aMatrixA[6, 4] := 0.0050;
    aMatrixA[6, 5] := 0.0000; aMatrixA[6, 6] := 0.9920; aMatrixA[6, 7] :=-0.0020;   aMatrixA[6, 8] := 0.0000;
    aMatrixA[6, 9] := 0.0000; aMatrixA[6, 10]:= 0.0000;

    (* Row 7: Intensifier Multiplication Piston Stroke s_int [mm] *)
    aMatrixA[7, 1] := 0.0000; aMatrixA[7, 2] := 0.0000; aMatrixA[7, 3] := 0.0000;    aMatrixA[7, 4] := 0.0000;
    aMatrixA[7, 5] := 0.0000; aMatrixA[7, 6] := 0.0025; aMatrixA[7, 7] := 0.9750;    aMatrixA[7, 8] :=-0.0012;
    aMatrixA[7, 9] := 0.0000; aMatrixA[7, 10]:= 0.0000;

    (* Row 8: Intensifier Chamber Output Pressure P_int [bar] *)
    aMatrixA[8, 1] := 0.0000; aMatrixA[8, 2] := 0.0000; aMatrixA[8, 3] := 0.0000;    aMatrixA[8, 4] := 0.0000;
    aMatrixA[8, 5] := 0.0000; aMatrixA[8, 6] := 0.0850; aMatrixA[8, 7] := 0.1250;    aMatrixA[8, 8] := 0.9550;
    aMatrixA[8, 9] :=-0.0450; aMatrixA[8, 10]:=-0.0150;

    (* Row 9: Molten Aluminum In-Gate Drag Resistance P_metal [bar] *)
    aMatrixA[9, 1] := 0.0005; aMatrixA[9, 2] := 0.1450; aMatrixA[9, 3] := 0.0085;    aMatrixA[9, 4] := 0.0000;
    aMatrixA[9, 5] := 0.0000; aMatrixA[9, 6] := 0.0000; aMatrixA[9, 7] := 0.0000;    aMatrixA[9, 8] := 0.0025;
    aMatrixA[9, 9] := 0.9200; aMatrixA[9, 10]:= 0.0850;

    (* Row 10: Biscuit Solidification Fraction xi_biscuit [%] *)
    aMatrixA[10, 1]:= 0.0000; aMatrixA[10, 2]:= 0.0000; aMatrixA[10, 3]:= 0.0000;    aMatrixA[10, 4]:= 0.0000;
    aMatrixA[10, 5]:= 0.0000; aMatrixA[10, 6]:= 0.0000; aMatrixA[10, 7]:= 0.0000;    aMatrixA[10, 8]:= 0.0015;
    aMatrixA[10, 9]:= 0.0000; aMatrixA[10, 10]:= 0.9980;

    (* Actuator Input Coupling Matrix B (10x8) *)
    aMatrixB[1, 1] := 0.0001;  aMatrixB[1, 2] := 0.0000;  aMatrixB[1, 3] := 0.0000;  aMatrixB[1, 4] := 0.0000;
    aMatrixB[1, 5] := 0.0000;  aMatrixB[1, 6] := 0.0000;  aMatrixB[1, 7] := 0.0000;  aMatrixB[1, 8] := 0.0000;

    aMatrixB[2, 1] := 0.0850;  aMatrixB[2, 2] := 0.1250;  aMatrixB[2, 3] := 0.0000;  aMatrixB[2, 4] := 0.0000;
    aMatrixB[2, 5] := 0.0000;  aMatrixB[2, 6] := 0.0000;  aMatrixB[2, 7] :=-0.0020;  aMatrixB[2, 8] := 0.0000;

    aMatrixB[3, 1] := 0.8500;  aMatrixB[3, 2] := 1.4500;  aMatrixB[3, 3] := 0.0000;  aMatrixB[3, 4] := 0.0000;
    aMatrixB[3, 5] := 0.0000;  aMatrixB[3, 6] := 0.0000;  aMatrixB[3, 7] :=-0.0150;  aMatrixB[3, 8] := 0.0000;

    aMatrixB[4, 1] := 0.4500;  aMatrixB[4, 2] := 0.9500;  aMatrixB[4, 3] := 0.0000;  aMatrixB[4, 4] := 0.0250;
    aMatrixB[4, 5] := 0.0000;  aMatrixB[4, 6] := 0.0000;  aMatrixB[4, 7] := 0.0000;  aMatrixB[4, 8] := 0.0000;

    aMatrixB[5, 1] :=-0.2500;  aMatrixB[5, 2] := 0.0000;  aMatrixB[5, 3] := 0.0000;  aMatrixB[5, 4] := 0.0000;
    aMatrixB[5, 5] := 0.0000;  aMatrixB[5, 6] := 0.0000;  aMatrixB[5, 7] := 0.0000;  aMatrixB[5, 8] := 0.0000;

    aMatrixB[6, 1] :=-0.0850;  aMatrixB[6, 2] :=-0.2200;  aMatrixB[6, 3] :=-0.1500;  aMatrixB[6, 4] := 0.1800;
    aMatrixB[6, 5] := 0.0000;  aMatrixB[6, 6] := 0.0000;  aMatrixB[6, 7] := 0.0000;  aMatrixB[6, 8] := 0.0000;

    aMatrixB[7, 1] := 0.0000;  aMatrixB[7, 2] := 0.0000;  aMatrixB[7, 3] := 0.1850;  aMatrixB[7, 4] := 0.0000;
    aMatrixB[7, 5] := 0.0000;  aMatrixB[7, 6] := 0.0000;  aMatrixB[7, 7] := 0.0000;  aMatrixB[7, 8] := 0.0000;

    aMatrixB[8, 1] := 0.0000;  aMatrixB[8, 2] := 0.0000;  aMatrixB[8, 3] := 1.8500;  aMatrixB[8, 4] := 0.0000;
    aMatrixB[8, 5] := 0.0000;  aMatrixB[8, 6] := 0.0000;  aMatrixB[8, 7] := 0.0000;  aMatrixB[8, 8] := 0.0000;

    aMatrixB[9, 1] := 0.0000;  aMatrixB[9, 2] := 0.0550;  aMatrixB[9, 3] := 0.0000;  aMatrixB[9, 4] := 0.0000;
    aMatrixB[9, 5] :=-0.0120;  aMatrixB[9, 6] := 0.0000;  aMatrixB[9, 7] := 0.0450;  aMatrixB[9, 8] := 0.0000;

    aMatrixB[10, 1]:= 0.0000;  aMatrixB[10, 2]:= 0.0000;  aMatrixB[10, 3]:= 0.0050;  aMatrixB[10, 4]:= 0.0000;
    aMatrixB[10, 5]:= 0.0000;  aMatrixB[10, 6]:= 0.0000;  aMatrixB[10, 7]:= 0.0000;  aMatrixB[10, 8] := 0.0150;

    (* Output Extraction Matrix C (6x10) *)
    FOR iIdxRow := 1 TO 6 DO
        FOR iIdxCol := 1 TO 10 DO
            aMatrixC[iIdxRow, iIdxCol] := 0.0;
        END_FOR;
    END_FOR;
    aMatrixC[1, 1] := 1.0; (* Measured Plunger Position s_p [mm] *)
    aMatrixC[2, 2] := 1.0; (* Measured Plunger Velocity v_p [m/s] *)
    aMatrixC[3, 4] := 1.0; (* Measured Injection Cylinder Head Pressure P_head [bar] *)
    aMatrixC[4, 6] := 1.0; (* Measured Accumulator Pressure P_acc [bar] *)
    aMatrixC[5, 8] := 1.0; (* Measured Intensifier Output Pressure P_int [bar] *)
    aMatrixC[6, 9] := 0.1; (* Correlated Cavity Ingress Back-Pressure Resistance *)

    (* Observer Kalman Gain Matrix L (10x6) *)
    FOR iIdxRow := 1 TO 10 DO
        FOR iIdxCol := 1 TO 6 DO
            aObserverGainL[iIdxRow, iIdxCol] := 0.0;
        END_FOR;
    END_FOR;
    aObserverGainL[1, 1] := 0.250; aObserverGainL[1, 2] := 0.015;
    aObserverGainL[2, 1] := 0.045; aObserverGainL[2, 2] := 0.320; aObserverGainL[2, 3] := 0.008;
    aObserverGainL[3, 1] := 0.010; aObserverGainL[3, 2] := 0.450; aObserverGainL[3, 3] := 0.055;
    aObserverGainL[4, 3] := 0.280; aObserverGainL[4, 4] := 0.025;
    aObserverGainL[5, 3] :=-0.085;
    aObserverGainL[6, 4] := 0.350;
    aObserverGainL[7, 5] := 0.045;
    aObserverGainL[8, 5] := 0.420;
    aObserverGainL[9, 2] := 0.035; aObserverGainL[9, 3] := 0.015; aObserverGainL[9, 6] := 0.150;
    aObserverGainL[10, 5]:= 0.012;

    (* MPC Quadratic Weights Initialization *)
    aMatrixQ[1] := 25.0;  (* Plunger position error penalty *)
    aMatrixQ[2] := 150.0; (* Plunger velocity tracking penalty *)
    aMatrixQ[3] := 5.0;   (* Acceleration jitter penalty *)
    aMatrixQ[4] := 12.0;  (* Head pressure tracking penalty *)
    aMatrixQ[5] := 2.0;   (* Back-pressure penalty *)
    aMatrixQ[6] := 8.0;   (* Accumulator pressure droop penalty *)
    aMatrixQ[7] := 10.0;  (* Intensifier stroke penalty *)
    aMatrixQ[8] := 85.0;  (* Intensification pressure tracking penalty *)
    aMatrixQ[9] := 1.0;   (* Metal drag penalty *)
    aMatrixQ[10]:= 4.0;   (* Solidification progress weight *)

    aMatrixR[1] := 1.5;   (* Main servovalve slew penalty *)
    aMatrixR[2] := 2.0;   (* Fast shot valve actuation penalty *)
    aMatrixR[3] := 5.0;   (* Intensifier valve firing penalty *)
    aMatrixR[4] := 0.5;   (* Accumulator charge valve penalty *)
    aMatrixR[5] := 0.2;   (* Vacuum valve penalty *)
    aMatrixR[6] := 10.0;  (* Tie-bar trim motor wear penalty *)
    aMatrixR[7] := 1.0;   (* Ladler flow rate penalty *)
    aMatrixR[8] := 0.5;   (* Spray duty cycle penalty *)

    FOR iIdxRow := 1 TO 10 DO
        aMatrixP[iIdxRow] := aMatrixQ[iIdxRow] * 2.5; (* Terminal State Weighting *)
    END_FOR;

    bMatricesInitialized := TRUE;
END_IF;

(* --- 2.2: Map Sensor Feedbacks to Output Measurement Vector y --- *)
aOutputY[1] := rPlungerPosition_mm;
aOutputY[2] := rPlungerVelocity_mps;
aOutputY[3] := rInjectionCylinderHeadPress_bar;
aOutputY[4] := rAccumulatorPress_bar;
aOutputY[5] := rIntensifierPress_bar;
aOutputY[6] := rVotedVacuumPressure_mbar * 0.1;

(* Map Previous Actuator Commands to Input Vector u *)
aInputU[1] := rInjectionServoSpool_pct;
IF bFastShotCartridgeOpen THEN aInputU[2] := 100.0; ELSE aInputU[2] := 0.0; END_IF;
IF bIntensifierPoppetFire THEN aInputU[3] := 100.0; ELSE aInputU[3] := 0.0; END_IF;
IF bAccumulatorChargeCmd THEN aInputU[4] := 100.0; ELSE aInputU[4] := 0.0; END_IF;
IF bVacuumGateValveOpen THEN aInputU[5] := 100.0; ELSE aInputU[5] := 0.0; END_IF;
IF bTieBarNutAdjustFwd THEN aInputU[6] := 1.0; ELSIF bTieBarNutAdjustRev THEN aInputU[6] := -1.0; ELSE aInputU[6] := 0.0; END_IF;
aInputU[7] := rLadleDosedWeight_kg;
aInputU[8] := 50.0; (* Die thermal balance duty cycle *)

(* --- 2.3: Compute Estimated Output y_hat = C * x_hat --- *)
FOR iIdxRow := 1 TO 6 DO
    rAccumulatorVar := 0.0;
    FOR iIdxCol := 1 TO 10 DO
        rAccumulatorVar := rAccumulatorVar + (aMatrixC[iIdxRow, iIdxCol] * aStateX[iIdxCol]);
    END_FOR;
    aOutputY_hat[iIdxRow] := rAccumulatorVar;
    aOutputResidual[iIdxRow] := aOutputY[iIdxRow] - aOutputY_hat[iIdxRow];
END_FOR;

(* --- 2.4: Discrete State-Space Propagation & Observer Correction --- *)
(* x[k+1] = A * x[k] + B * u[k] + L * e[k] *)
FOR iIdxRow := 1 TO 10 DO
    rAccumulatorVar := 0.0;
    (* State Dynamic Coupling A * x *)
    FOR iIdxCol := 1 TO 10 DO
        rAccumulatorVar := rAccumulatorVar + (aMatrixA[iIdxRow, iIdxCol] * aStateX[iIdxCol]);
    END_FOR;
    (* Actuation Coupling B * u *)
    FOR iIdxInput := 1 TO 8 DO
        rAccumulatorVar := rAccumulatorVar + (aMatrixB[iIdxRow, iIdxInput] * aInputU[iIdxInput]);
    END_FOR;
    (* Observer Innovation Correction L * e *)
    FOR iIdxCol := 1 TO 6 DO
        rAccumulatorVar := rAccumulatorVar + (aObserverGainL[iIdxRow, iIdxCol] * aOutputResidual[iIdxCol]);
    END_FOR;
    aStateX_hat[iIdxRow] := rAccumulatorVar;
END_FOR;

(* Commit Propagated State Vector *)
FOR iIdxRow := 1 TO 10 DO
    aStateX[iIdxRow] := aStateX_hat[iIdxRow];
END_FOR;
""")

    # -------------------------------------------------------------------------
    # PART 6: Phase 3: Receding-Horizon MPC Velocity Profile Tracking & Braking
    # -------------------------------------------------------------------------
    parts.append("""
(* =========================================================================================
   PHASE 3: RECEDING-HORIZON MPC VELOCITY & PRESSURE PROFILE TRACKING
   ========================================================================================= *)

(* --- 3.1: Multi-Phase Injection Target Trajectory Generation --- *)
IF (iFsmState = 50) THEN
    (* Phase 1: Slow-Shot Critical Wave Anti-Rollover Target *)
    aTargetStateRef[1] := rGatePosition_mm;
    aTargetStateRef[2] := rPhase1TargetVelocity_mps; (* 0.28 m/s *)
    aTargetStateRef[3] := 0.0;
    aTargetStateRef[4] := 45.0;                      (* Cylinder Head Drive Pressure [bar] *)
    aTargetStateRef[5] := 15.0;
    aTargetStateRef[6] := 205.0;
    aTargetStateRef[7] := 0.0;
    aTargetStateRef[8] := 0.0;
    aTargetStateRef[9] := 12.0;
    aTargetStateRef[10]:= 0.0;
ELSIF (iFsmState = 60) THEN
    (* Phase 2: Dynamic Fast-Shot Cavity Filling Target *)
    IF rPlungerPosition_mm < rBrakingPosition_mm THEN
        (* High-Speed Filling Acceleration Zone *)
        aTargetStateRef[1] := rBrakingPosition_mm;
        aTargetStateRef[2] := rPhase2TargetVelocity_mps; (* 6.8 m/s *)
        aTargetStateRef[3] := 120.0;                     (* High Acceleration Rate *)
        aTargetStateRef[4] := 160.0;
        aTargetStateRef[5] := 25.0;
        aTargetStateRef[6] := 190.0;
        aTargetStateRef[7] := 0.0;
        aTargetStateRef[8] := 0.0;
        aTargetStateRef[9] := 85.0;
        aTargetStateRef[10]:= 5.0;
    ELSE
        (* Terminal Deceleration Braking Zone to Protect Tooling *)
        aTargetStateRef[1] := rNominalStrokeLimit_mm;
        aTargetStateRef[2] := 0.65;                      (* Controlled Impact Deceleration Speed *)
        aTargetStateRef[3] :=-250.0;                     (* Heavy Deceleration Braking Force *)
        aTargetStateRef[4] := 140.0;
        aTargetStateRef[5] := 85.0;                      (* Rod Back-Pressure Deceleration Cushion *)
        aTargetStateRef[6] := 180.0;
        aTargetStateRef[7] := 0.0;
        aTargetStateRef[8] := 0.0;
        aTargetStateRef[9] := 140.0;
        aTargetStateRef[10]:= 15.0;
    END_IF;
ELSIF (iFsmState = 70) OR (iFsmState = 80) THEN
    (* Phase 3 & Solidification Dwell: High-Pressure Consolidation *)
    aTargetStateRef[1] := rNominalStrokeLimit_mm;
    aTargetStateRef[2] := 0.0;
    aTargetStateRef[3] := 0.0;
    aTargetStateRef[4] := 180.0;
    aTargetStateRef[5] := 20.0;
    aTargetStateRef[6] := 175.0;
    aTargetStateRef[7] := 65.0;                          (* Intensifier Stroke Active *)
    aTargetStateRef[8] := rPhase3TargetPressure_bar;     (* 1,150 bar High-Pressure Consolidation *)
    aTargetStateRef[9] := 1150.0;
    aTargetStateRef[10]:= 100.0;                         (* Complete Biscuit Solidification *)
ELSE
    (* System Idle / Platen Retract Target *)
    aTargetStateRef[1] := 0.0;
    aTargetStateRef[2] := 0.0;
    aTargetStateRef[3] := 0.0;
    aTargetStateRef[4] := 0.0;
    aTargetStateRef[5] := 0.0;
    aTargetStateRef[6] := 210.0;
    aTargetStateRef[7] := 0.0;
    aTargetStateRef[8] := 0.0;
    aTargetStateRef[9] := 0.0;
    aTargetStateRef[10]:= 0.0;
END_IF;

(* --- 3.2: Receding-Horizon Multi-Step Prediction Simulation (Np=5) --- *)
(* Seed step 1 prediction with current observed state *)
FOR iIdxRow := 1 TO 10 DO
    aMpcStatePred[1, iIdxRow] := aStateX[iIdxRow];
END_FOR;

(* Unroll Dynamic Propagation across Prediction Horizon *)
FOR iIdxHoriz := 1 TO 4 DO
    FOR iIdxRow := 1 TO 10 DO
        rAccumulatorVar := 0.0;
        FOR iIdxCol := 1 TO 10 DO
            rAccumulatorVar := rAccumulatorVar + (aMatrixA[iIdxRow, iIdxCol] * aMpcStatePred[iIdxHoriz, iIdxCol]);
        END_FOR;
        FOR iIdxInput := 1 TO 8 DO
            rAccumulatorVar := rAccumulatorVar + (aMatrixB[iIdxRow, iIdxInput] * aInputU[iIdxInput]);
        END_FOR;
        aMpcStatePred[iIdxHoriz + 1, iIdxRow] := rAccumulatorVar;
    END_FOR;
END_FOR;

(* --- 3.3: Quadratic Objective Cost Function Optimization --- *)
rMpcCandidateCost := 0.0;
FOR iIdxHoriz := 1 TO 5 DO
    FOR iIdxRow := 1 TO 10 DO
        rTempCalcDelta := aMpcStatePred[iIdxHoriz, iIdxRow] - aTargetStateRef[iIdxRow];
        IF iIdxHoriz < 5 THEN
            rMpcCandidateCost := rMpcCandidateCost + (rTempCalcDelta * rTempCalcDelta * aMatrixQ[iIdxRow]);
        ELSE
            (* Terminal Horizon Penalty Matrix P *)
            rMpcCandidateCost := rMpcCandidateCost + (rTempCalcDelta * rTempCalcDelta * aMatrixP[iIdxRow]);
        END_IF;
    END_FOR;
END_FOR;

(* --- 3.4: Closed-Loop Unconstrained Optimal Spool Command Computation --- *)
IF (iFsmState = 50) THEN
    (* Phase 1 Slow Shot Proportional Pacing *)
    rOptimalSpoolCmd := 18.0 + (aTargetStateRef[2] - aStateX[2]) * 85.0 + (aTargetStateRef[4] - aStateX[4]) * 0.15;
ELSIF (iFsmState = 60) THEN
    (* Phase 2 Dynamic Fast Shot Tracking & Deceleration Braking *)
    IF rPlungerPosition_mm < rBrakingPosition_mm THEN
        rOptimalSpoolCmd := 75.0 + (aTargetStateRef[2] - aStateX[2]) * 45.0 + (aTargetStateRef[3] - aStateX[3]) * 0.05;
    ELSE
        (* Active Hydraulic Braking on Rod Cushion *)
        rOptimalSpoolCmd := 12.0 - (aStateX[2] - aTargetStateRef[2]) * 65.0 - (aStateX[3]) * 0.08;
    END_IF;
ELSIF (iFsmState = 70) THEN
    (* Phase 3 Intensification Valve Spool *)
    rOptimalSpoolCmd := 95.0;
ELSE
    rOptimalSpoolCmd := 0.0;
END_IF;

(* --- 3.5: Non-Linear Hydraulic Servovalve Deadband Compensation & Slew Limiting --- *)
(* Invert +/- 7.5% Spool Overlap Deadband *)
IF rOptimalSpoolCmd > 0.5 THEN
    rOptimalSpoolCmd := rSpoolDeadband_pct + ((100.0 - rSpoolDeadband_pct) / 100.0) * rOptimalSpoolCmd;
ELSIF rOptimalSpoolCmd < -0.5 THEN
    rOptimalSpoolCmd := -rSpoolDeadband_pct + ((100.0 - rSpoolDeadband_pct) / 100.0) * rOptimalSpoolCmd;
ELSE
    rOptimalSpoolCmd := 0.0;
END_IF;

(* Slew Rate Saturation Limiter (Maximum +/- 25.0% change per millisecond cycle) *)
IF (rOptimalSpoolCmd - rInjectionServoSpool_pct) > rSlewRateLimit_pct THEN
    rInjectionServoSpool_pct := rInjectionServoSpool_pct + rSlewRateLimit_pct;
ELSIF (rInjectionServoSpool_pct - rOptimalSpoolCmd) > rSlewRateLimit_pct THEN
    rInjectionServoSpool_pct := rInjectionServoSpool_pct - rSlewRateLimit_pct;
ELSE
    rInjectionServoSpool_pct := rOptimalSpoolCmd;
END_IF;

(* Bounding Hard Output Limits [-100.0% to +100.0%] *)
IF rInjectionServoSpool_pct > 100.0 THEN
    rInjectionServoSpool_pct := 100.0;
ELSIF rInjectionServoSpool_pct < -100.0 THEN
    rInjectionServoSpool_pct := -100.0;
END_IF;
""")

    # -------------------------------------------------------------------------
    # PART 7: Phase 4: 12-Stage Operational Heavy Foundry FSM
    # -------------------------------------------------------------------------
    parts.append("""
(* =========================================================================================
   PHASE 4: 12-STAGE OPERATIONAL HEAVY FOUNDRY FINITE STATE MACHINE (FSM)
   ========================================================================================= *)

(* Update Operational State Timers *)
rFsmStageTimer_s := rFsmStageTimer_s + rSampleTime_s;
rCurrentCycleTime_s := rCurrentCycleTime_s + rSampleTime_s;

(* Master Safety Interlock Check *)
IF NOT bEmergencyStopOk OR NOT bEnable OR bCriticalTripActive THEN
    iFsmState := 999; (* Transition Immediately to Fail-Safe Stop State *)
END_IF;

CASE iFsmState OF
    10: (* =============================================================================
           STAGE 10: DIE CLOSE & CLAMP TOGGLE STROKE
           - Verify die daylight clear of robotic arms (ladler, extractor, sprayer).
           - High-speed platen closing transitioning to low-pressure mold protection zone.
           ============================================================================= *)
        (* Reset Operational Actuators *)
        bFastShotCartridgeOpen := FALSE;
        bIntensifierPoppetFire := FALSE;
        bVacuumGateValveOpen := FALSE;
        bLadlerStartPourCmd := FALSE;
        bExtractorStartTakeoutCmd := FALSE;
        bSprayerStartLubeCmd := FALSE;
        bAccumulatorChargeCmd := (rAccumulatorPress_bar < 205.0);

        (* Interlock: All Robots Must Be Confirmed Parked in Safe Home Position *)
        IF bLadlerHomeSafe AND bExtractorArmClear AND bSprayerHomeSafe AND bMoldSafetyGateClosed THEN
            (* Three-Stage Toggle Clamping Velocity Profile *)
            IF rMovingPlatenPos_mm > 400.0 THEN
                (* Stage 1: High-Speed Rapid Advance *)
                rToggleClampValve_pct := 70.0;
                tMoldProtectWatchdog(IN := FALSE, PT := T#5S);
            ELSIF (rMovingPlatenPos_mm <= 400.0) AND (rMovingPlatenPos_mm > 50.0) THEN
                (* Stage 2: Low-Pressure Mold Protection Zone *)
                rToggleClampValve_pct := 15.0;
                tMoldProtectWatchdog(IN := TRUE, PT := T#3S);
                (* If obstacle detected via hydraulic pressure rise before die touch *)
                IF rToggleCylinderHeadPress_bar > 45.0 THEN
                    (* Foreign body / stuck casting in mold protection zone *)
                    iFsmState := 999;
                END_IF;
            ELSE
                (* Stage 3: Low-Speed Final Platen Touch *)
                rToggleClampValve_pct := 8.0;
                tMoldProtectWatchdog(IN := FALSE, PT := T#5S);
                (* Platen Closed Proximity Reached *)
                IF (rMovingPlatenPos_mm <= 2.0) THEN
                    rToggleClampValve_pct := 0.0;
                    rFsmStageTimer_s := 0.0;
                    iFsmPreviousState := 10;
                    iFsmState := 20; (* Proceed to High-Tonnage Lock-Over *)
                END_IF;
            END_IF;
        ELSE
            rToggleClampValve_pct := 0.0;
        END_IF;

        (* Timeout Watchdog on Platen Close *)
        IF tMoldProtectWatchdog.Q THEN
            iFsmState := 999;
        END_IF;

    20: (* =============================================================================
           STAGE 20: 3,500-TON TOGGLE LOCK-OVER & STRAIN GAUGE VERIFICATION
           - Hydraulic crosshead toggles drive over-center into mechanical lock.
           - Strain-gauge bridges on all 4 tie-bars verify clamp tonnage >= 3,450 tons.
           - Check cross-diagonal imbalance ratio (< 6.5%).
           ============================================================================= *)
        (* Drive Toggle Cylinder with Maximum Lock-Over Pressure *)
        rToggleClampValve_pct := 100.0;
        tTonnageLockWatchdog(IN := TRUE, PT := T#4S);

        (* Verify Full 3,500-Ton Tonnage & Platen Parallelism *)
        IF (rTotalClampTonnage_tons >= c_rTonnage_L) AND (rTieBarImbalance_pct <= c_rImbalance_H) THEN
            tTonnageLockWatchdog(IN := FALSE, PT := T#4S);
            rToggleClampValve_pct := 0.0; (* Mechanical Over-Center Lock Holds Tonnage *)
            
            (* Insert Hydraulic Slide Cores 1 and 2 *)
            bCore1ExtendCmd := TRUE;
            bCore2ExtendCmd := TRUE;

            IF bCore1InLimit AND bCore2InLimit THEN
                rFsmStageTimer_s := 0.0;
                iFsmPreviousState := 20;
                iFsmState := 30; (* Proceed to Robotic Ladler Metal Dosing *)
            END_IF;
        END_IF;

        IF tTonnageLockWatchdog.Q THEN
            iFsmState := 999; (* Clamping Tonnage Timeout Fault *)
        END_IF;

    30: (* =============================================================================
           STAGE 30: 6-AXIS ROBOTIC LADLER MOLTEN ALUMINUM DOSING
           - Authorize robotic ladler permissive handshake.
           - Verify molten aluminum holding bath temperature (680 deg C - 725 deg C).
           - Robot pours 18.5 kg shot weight into horizontal sleeve pour hole.
           ============================================================================= *)
        bLadlerPermissive := TRUE;
        bLadlerStartPourCmd := TRUE;
        tLadlePourWatchdog(IN := TRUE, PT := T#12S);

        (* Check Molten Metal Temperature Limits *)
        IF (rFurnaceMetalTemp_degC >= c_rMetalTemp_L) AND (rFurnaceMetalTemp_degC <= c_rMetalTemp_H) THEN
            (* Await Handshake from Ladler Robot Signaling Complete Dosing & Retraction *)
            IF bLadlerPouringComplete AND bLadlerHomeSafe THEN
                tLadlePourWatchdog(IN := FALSE, PT := T#12S);
                bLadlerPermissive := FALSE;
                bLadlerStartPourCmd := FALSE;
                rFsmStageTimer_s := 0.0;
                iFsmPreviousState := 30;
                iFsmState := 40; (* Proceed to Sleeve & Cavity Vacuum Evacuation *)
            END_IF;
        ELSE
            (* Melt Temperature Out of Tolerance *)
            bLadlerStartPourCmd := FALSE;
            IF tLadlePourWatchdog.Q THEN
                iFsmState := 999;
            END_IF;
        END_IF;

    40: (* =============================================================================
           STAGE 40: SLEEVE & DIE CAVITY VACUUM EVACUATION DRAW
           - High-speed chill-vent vacuum valve opens.
           - Cavity air and volatile lubricant vapors evacuated to < 50 mbar.
           - 2oo3 voted pressure verified prior to metal injection.
           ============================================================================= *)
        bVacuumGateValveOpen := TRUE;
        bVacuumPumpBypass := FALSE;
        tVacuumDrawWatchdog(IN := TRUE, PT := T#2500MS);

        (* Await Vacuum Pulldown Below 50 mbar Benchmark *)
        IF (rVotedVacuumPressure_mbar <= 50.0) AND bVacuumValveLimitSwOpen THEN
            tVacuumDrawWatchdog(IN := FALSE, PT := T#2500MS);
            rFsmStageTimer_s := 0.0;
            iFsmPreviousState := 40;
            iFsmState := 50; (* Proceed to Phase 1 Slow Shot *)
        ELSIF tVacuumDrawWatchdog.Q THEN
            (* Vacuum pulldown timed out: evaluate if permissive for atmospheric degraded shot *)
            tVacuumDrawWatchdog(IN := FALSE, PT := T#2500MS);
            IF rVotedVacuumPressure_mbar < c_rVacuum_H THEN
                (* Marginal vacuum: proceed with warning *)
                rFsmStageTimer_s := 0.0;
                iFsmPreviousState := 40;
                iFsmState := 50;
            ELSE
                (* Gross atmospheric vacuum leak: abort to prevent explosive porosity *)
                iFsmState := 999;
            END_IF;
        END_IF;

    50: (* =============================================================================
           STAGE 50: PHASE 1 SLOW-SHOT INJECTION (0.10 m/s - 0.40 m/s)
           - Closed-loop MPC paces plunger at 0.28 m/s.
           - Prevents wave crest rollover and air entrapment in the horizontal sleeve.
           - Transitions when plunger passes in-gate position encoder (450 mm).
           ============================================================================= *)
        tSlowShotWatchdog(IN := TRUE, PT := T#4S);
        bFastShotCartridgeOpen := FALSE;
        bIntensifierPoppetFire := FALSE;

        (* Log Phase 1 Measured Velocity *)
        rPhase1Velocity_mps := rPlungerVelocity_mps;

        (* Check Gate Trigger Position *)
        IF rPlungerPosition_mm >= rGatePosition_mm THEN
            tSlowShotWatchdog(IN := FALSE, PT := T#4S);
            bInGateTriggerCrossed := TRUE;
            rFsmStageTimer_s := 0.0;
            iFsmPreviousState := 50;
            iFsmState := 60; (* Trigger Phase 2 Fast Injection Shot *)
        END_IF;

        IF tSlowShotWatchdog.Q THEN
            iFsmState := 999; (* Slow Shot Stroke Timeout / Plunger Seizure *)
        END_IF;

    60: (* =============================================================================
           STAGE 60: PHASE 2 FAST-SHOT INJECTION (Up to 8.5 m/s, Acceleration > 40g)
           - Accumulator cartridge pilot fires: rapid nitrogen dump into cylinder.
           - Closed-loop MPC tracks rapid velocity ramp and executes terminal braking.
           - Cavity fill completed in 25-45 ms; detects pressure spike upon impact.
           ============================================================================= *)
        bFastShotCartridgeOpen := TRUE;
        tFastShotWatchdog(IN := TRUE, PT := T#500MS);

        (* Record Peak Fast Shot Velocity *)
        IF rPlungerVelocity_mps > rPhase2PeakVelocity_mps THEN
            rPhase2PeakVelocity_mps := rPlungerVelocity_mps;
        END_IF;

        (* Detect Cavity Filling Impact Spike *)
        (* Condition: Velocity sharply decreases while head pressure surges above 150 bar *)
        IF (rInjectionCylinderHeadPress_bar > 150.0) AND (rPlungerVelocity_mps < 1.5) AND (rPlungerPosition_mm > rGatePosition_mm) THEN
            bCavityFullImpactDetected := TRUE;
            rCavityFillTime_ms := rFsmStageTimer_s * 1000.0;

            (* Instantly Close Vacuum Valve to Prevent Molten Metal Ingress into Vacuum Lines *)
            bVacuumGateValveOpen := FALSE;
            tFastShotWatchdog(IN := FALSE, PT := T#500MS);
            
            rFsmStageTimer_s := 0.0;
            rIntensifierStartTimestamp_s := rCurrentCycleTime_s;
            bRiseTimeCalcDone := FALSE;
            iFsmPreviousState := 60;
            iFsmState := 70; (* Fire Phase 3 Pressure Intensifier *)
        END_IF;

        IF tFastShotWatchdog.Q THEN
            iFsmState := 999; (* Cavity Fill Timeout Fault *)
        END_IF;

    70: (* =============================================================================
           STAGE 70: PHASE 3 HYDRAULIC PRESSURE INTENSIFICATION (Up to 1,200 bar)
           - Ultra-fast poppet dumps 315 bar oil onto intensifier booster piston (3.8:1).
           - Specific pressure on molten aluminum surges to 1,150-1,200 bar within 15 ms.
           - Closes micro-shrinkage dendritic pores in freezing casting.
           ============================================================================= *)
        bFastShotCartridgeOpen := TRUE;
        bIntensifierPoppetFire := TRUE;
        rIntensifierRegValve_pct := 100.0;
        tIntensifierWatchdog(IN := TRUE, PT := T#250MS);

        (* Log Peak Intensification Pressure *)
        IF rIntensifierPress_bar > rPhase3PeakPressure_bar THEN
            rPhase3PeakPressure_bar := rIntensifierPress_bar;
        END_IF;

        (* Audit Intensifier Dynamic Rise Time (10% to 90% benchmark) *)
        IF NOT bRiseTimeCalcDone THEN
            IF (rIntensifierPress_bar >= rIntensifierPressure10Pct_bar) AND (rTimeAt10Pct_s = 0.0) THEN
                rTimeAt10Pct_s := rCurrentCycleTime_s;
            END_IF;
            IF (rIntensifierPress_bar >= rIntensifierPressure90Pct_bar) AND (rTimeAt10Pct_s > 0.0) THEN
                rTimeAt90Pct_s := rCurrentCycleTime_s;
                rIntensificationRiseTime_ms := (rTimeAt90Pct_s - rTimeAt10Pct_s) * 1000.0;
                bRiseTimeCalcDone := TRUE;
            END_IF;
        END_IF;

        (* Once Intensifier Pressure Exceeds 950 bar Benchmark -> Transition to Dwell *)
        IF (rIntensifierPress_bar >= c_rIntensPress_L) OR (rFsmStageTimer_s >= 0.080) THEN
            tIntensifierWatchdog(IN := FALSE, PT := T#250MS);
            rSolidificationTimerAccum_s := 0.0;
            rFsmStageTimer_s := 0.0;
            iFsmPreviousState := 70;
            iFsmState := 80; (* Proceed to Solidification Dwell *)
        END_IF;

        IF tIntensifierWatchdog.Q THEN
            iFsmState := 999; (* Intensifier Firing Timeout Fault *)
        END_IF;

    80: (* =============================================================================
           STAGE 80: BISCUIT SOLIDIFICATION & COOLING DWELL
           - Maintain intensifier compaction holding pressure.
           - Integrate 1D Stefan thermal freezing front equation: X_skin = K * sqrt(t).
           - Measure residual biscuit cake thickness.
           ============================================================================= *)
        bIntensifierPoppetFire := TRUE;
        rIntensifierRegValve_pct := 90.0;
        rSolidificationTimerAccum_s := rSolidificationTimerAccum_s + rSampleTime_s;

        (* Dynamic Stefan Solidification Front Depth Calculation [mm] *)
        IF rSolidificationTimerAccum_s > 0.0 THEN
            rSolidificationFront_mm := rStefanSolidificationConst_K * SQRT(rSolidificationTimerAccum_s);
        END_IF;

        (* Compute Measured Solidified Biscuit Thickness [mm] *)
        rMeasuredBiscuitThickness_mm := rNominalStrokeLimit_mm - rPlungerPosition_mm;

        (* Dwell Timer Expiration Check *)
        IF rSolidificationTimerAccum_s >= rSolidificationDwellDuration_s THEN
            (* De-energize Intensifier & Fast Shot Cartridges *)
            bIntensifierPoppetFire := FALSE;
            bFastShotCartridgeOpen := FALSE;
            rIntensifierRegValve_pct := 0.0;

            rFsmStageTimer_s := 0.0;
            iFsmPreviousState := 80;
            iFsmState := 90; (* Proceed to Die Opening & Core Pull *)
        END_IF;

    90: (* =============================================================================
           STAGE 90: DIE OPENING, HIGH-TONNAGE CRACK & HYDRAULIC CORE PULL
           - Decompress hydraulic injection cylinder.
           - Retract hydraulic slide cores 1 & 2.
           - Execute high-tonnage breakaway mold cracking stroke.
           - Rapid platen opening to full stroke (1,650 mm).
           ============================================================================= *)
        tDieCrackWatchdog(IN := TRUE, PT := T#8S);

        (* Pull Hydraulic Slide Cores *)
        bCore1ExtendCmd := FALSE;
        bCore1RetractCmd := TRUE;
        bCore2ExtendCmd := FALSE;
        bCore2RetractCmd := TRUE;

        (* Platen Opening Kinematic Profile *)
        IF bCore1OutLimit AND bCore2OutLimit THEN
            IF rMovingPlatenPos_mm < 30.0 THEN
                (* High-Pressure Breakaway Die Crack *)
                rToggleClampValve_pct := -95.0;
            ELSIF (rMovingPlatenPos_mm >= 30.0) AND (rMovingPlatenPos_mm < 1400.0) THEN
                (* High-Speed Rapid Opening Platen Stroke *)
                rToggleClampValve_pct := -75.0;
            ELSE
                (* Final Deceleration Cushioning into Open Stop *)
                rToggleClampValve_pct := -20.0;
            END_IF;

            (* Platen Fully Open Verification *)
            IF (rMovingPlatenPos_mm >= 1600.0) THEN
                tDieCrackWatchdog(IN := FALSE, PT := T#8S);
                rToggleClampValve_pct := 0.0;
                rFsmStageTimer_s := 0.0;
                iFsmPreviousState := 90;
                iFsmState := 100; (* Proceed to Robotic Casting Extraction *)
            END_IF;
        ELSE
            rToggleClampValve_pct := 0.0; (* Hold Platen until Slide Cores are Fully Retracted *)
        END_IF;

        IF tDieCrackWatchdog.Q THEN
            iFsmState := 999; (* Die Opening Timeout Fault *)
        END_IF;

    100: (* ============================================================================
            STAGE 100: ROBOTIC CASTING PART EXTRACTION
            - Authorize 6-axis extractor robot permissive.
            - Fire hydraulic ejector plate forward to push casting off moving die pins.
            - Robot grips biscuit and runner; confirms optical/vacuum part detect.
            - Ejector retracts; robot exits platen clearance envelope.
            ============================================================================ *)
        bExtractorPermissive := TRUE;
        bExtractorStartTakeoutCmd := TRUE;
        tExtractorWatchdog(IN := TRUE, PT := T#15S);

        (* Fire Hydraulic Ejector Forward Once Robot Is in Extraction Envelope *)
        bEjectorExtendCmd := TRUE;
        bEjectorRetractCmd := FALSE;

        (* Await Robot Confirmation of Casting Grip & Ejector Full Forward Stroke *)
        IF bExtractorPartPresent AND bEjectorForwardLimit THEN
            (* Retract Ejector Plate to Home Position *)
            bEjectorExtendCmd := FALSE;
            bEjectorRetractCmd := TRUE;

            (* Confirm Robot Has Cleared Platen Interference Daylight *)
            IF bExtractorArmClear AND bEjectorRetractLimit THEN
                tExtractorWatchdog(IN := FALSE, PT := T#15S);
                bExtractorPermissive := FALSE;
                bExtractorStartTakeoutCmd := FALSE;
                rFsmStageTimer_s := 0.0;
                iFsmPreviousState := 100;
                iFsmState := 110; (* Proceed to Die Spray Lubrication & Air Purge *)
            END_IF;
        END_IF;

        IF tExtractorWatchdog.Q THEN
            iFsmState := 999; (* Extractor Robot Timeout Fault *)
        END_IF;

    110: (* ============================================================================
            STAGE 110: DIE SPRAY LUBRICATION & HIGH-VELOCITY AIR PURGE
            - Multi-axis spray robot cassette enters daylight between open dies.
            - Multi-zone atomized release agent application (fixed die, moving die, slides).
            - High-velocity compressed air blow-dry to remove all water pools (anti-porosity).
            ============================================================================ *)
        bSprayerPermissive := TRUE;
        bSprayerStartLubeCmd := TRUE;
        tSprayerWatchdog(IN := TRUE, PT := T#18S);

        (* Select Active Multi-Zone Spray Sequence Based on Stage Timer *)
        IF rFsmStageTimer_s < 4.0 THEN
            wSprayerZoneMask := 16#0003; (* Zone 1 & 2: Fixed Die Sprue & Cavity Lube *)
        ELSIF (rFsmStageTimer_s >= 4.0) AND (rFsmStageTimer_s < 8.0) THEN
            wSprayerZoneMask := 16#000C; (* Zone 3 & 4: Moving Die Cavity & Ejector Pin Lube *)
        ELSIF (rFsmStageTimer_s >= 8.0) AND (rFsmStageTimer_s < 11.0) THEN
            wSprayerZoneMask := 16#0030; (* Zone 5 & 6: Slide Core Ways Lubrication *)
        ELSE
            wSprayerZoneMask := 16#00C0; (* Zone 7 & 8: High-Velocity Compressed Air Dry Purge *)
        END_IF;

        (* Verify Spray Routine Completion & Safe Retraction *)
        IF bSprayerCycleDone AND bSprayerHomeSafe THEN
            tSprayerWatchdog(IN := FALSE, PT := T#18S);
            bSprayerPermissive := FALSE;
            bSprayerStartLubeCmd := FALSE;
            wSprayerZoneMask := 16#0000;
            rFsmStageTimer_s := 0.0;
            iFsmPreviousState := 110;
            iFsmState := 120; (* Proceed to Cycle Recock & Quality Accounting *)
        END_IF;

        IF tSprayerWatchdog.Q THEN
            iFsmState := 999; (* Die Spray Timeout Fault *)
        END_IF;

    120: (* ============================================================================
            STAGE 120: CELL RECOCK, QUALITY AUDIT & RE-ARMING
            - Retract injection plunger back to pour home loading position (0.0 mm).
            - Recharge hydraulic accumulator to 210 bar via charging pump.
            - Audit shot quality metrics (fill time, peak pressure, biscuit thickness).
            - Auto-cycle re-triggering.
            ============================================================================ *)
        (* Retract Injection Plunger *)
        rInjectionServoSpool_pct := -35.0;
        bAccumulatorChargeCmd := (rAccumulatorPress_bar < 210.0);

        (* Quality Acceptance Evaluation *)
        IF (rFsmStageTimer_s >= 1.5) AND (rPlungerPosition_mm <= 5.0) THEN
            rInjectionServoSpool_pct := 0.0;
            diTotalShotCounter := diTotalShotCounter + 1;

            (* Quality Criteria: Vacuum < 80 mbar, Biscuit within 18..42 mm, Intensifier > 980 bar *)
            IF (rVotedVacuumPressure_mbar <= c_rVacuum_H) AND
               (rMeasuredBiscuitThickness_mm >= c_rBiscuit_L) AND
               (rMeasuredBiscuitThickness_mm <= c_rBiscuit_H) AND
               (rPhase3PeakPressure_bar >= c_rIntensPress_L) AND
               (rTieBarImbalance_pct <= c_rImbalance_H) THEN
                diGoodPartsCounter := diGoodPartsCounter + 1;
            ELSE
                diRejectedPartsCounter := diRejectedPartsCounter + 1;
            END_IF;

            (* Cycle Duration Accounting *)
            rLastCycleTime_s := rCurrentCycleTime_s;
            rCurrentCycleTime_s := 0.0;
            rFsmStageTimer_s := 0.0;
            iFsmPreviousState := 120;

            (* Determine Next Cycle Action *)
            IF bAutoCycleStartCmd AND NOT bCriticalTripActive THEN
                iFsmState := 10; (* Continuous Auto-Cycle: Loop back to Stage 10 *)
            ELSE
                iFsmState := 10; (* Idle awaiting operator cycle start *)
            END_IF;
        END_IF;

    999: (* ============================================================================
            STAGE 999: FAIL-SAFE EMERGENCY SHUTDOWN STOP
            - Neutralize all hydraulic valves to zero displacement.
            - De-energize intensifier poppet, fast shot cartridge, and vacuum gate.
            - Retain clamping pressure if locked to prevent molten aluminum blowout.
            - Require operator manual intervention and reset.
            ============================================================================ *)
        rToggleClampValve_pct := 0.0;
        rInjectionServoSpool_pct := 0.0;
        bFastShotCartridgeOpen := FALSE;
        bIntensifierPoppetFire := FALSE;
        rIntensifierRegValve_pct := 0.0;
        bAccumulatorChargeCmd := FALSE;
        bVacuumGateValveOpen := FALSE;
        bLadlerPermissive := FALSE;
        bLadlerStartPourCmd := FALSE;
        bExtractorPermissive := FALSE;
        bExtractorStartTakeoutCmd := FALSE;
        bSprayerPermissive := FALSE;
        bSprayerStartLubeCmd := FALSE;
        wSprayerZoneMask := 16#0000;
        bCriticalTripActive := TRUE;

        (* Reset and Recovery Logic *)
        IF bReset AND bEmergencyStopOk THEN
            bCriticalTripActive := FALSE;
            rFsmStageTimer_s := 0.0;
            iFsmPreviousState := 999;
            iFsmState := 10; (* Return to Base Die Close State *)
        END_IF;
END_CASE;

iCurrentFsmStage := iFsmState;
""")

    # -------------------------------------------------------------------------
    # PART 8: Phase 5: ISA-18.2 Alarms & Diagnostic Word Packing
    # -------------------------------------------------------------------------
    parts.append("""
(* =========================================================================================
   PHASE 5: ISA-18.2 MULTI-TIERED ALARM MATRIX & BIT-PACKED DIAGNOSTIC WORDS
   ========================================================================================= *)

(* --- 5.1: Priority 1 / Emergency Critical Trips (dwIsaAlarmWord1) --- *)
(* Bit 0: Clamping Tie-Bar Overload High-High (> 3,700 tons) *)
IF rTotalClampTonnage_tons >= c_rTonnage_HH THEN
    dwIsaAlarmWord1 := dwIsaAlarmWord1 OR 16#00000001;
ELSIF rTotalClampTonnage_tons < (c_rTonnage_HH - c_rTonnageDeadband) THEN
    dwIsaAlarmWord1 := dwIsaAlarmWord1 AND NOT 16#00000001;
END_IF;

(* Bit 1: Tie-Bar Asymmetric Imbalance Critical Trip (> 10.0%) *)
IF rTieBarImbalance_pct >= c_rImbalance_HH THEN
    dwIsaAlarmWord1 := dwIsaAlarmWord1 OR 16#00000002;
ELSIF rTieBarImbalance_pct < (c_rImbalance_HH - 1.0) THEN
    dwIsaAlarmWord1 := dwIsaAlarmWord1 AND NOT 16#00000002;
END_IF;

(* Bit 2: Phase 3 Intensification Peak Pressure Low-Low Failure (< 850 bar) *)
IF (iFsmState >= 70) AND (rPhase3PeakPressure_bar < c_rIntensPress_LL) AND (rFsmStageTimer_s > 0.150) THEN
    dwIsaAlarmWord1 := dwIsaAlarmWord1 OR 16#00000004;
ELSIF rPhase3PeakPressure_bar >= c_rIntensPress_L THEN
    dwIsaAlarmWord1 := dwIsaAlarmWord1 AND NOT 16#00000004;
END_IF;

(* Bit 3: Intensifier Dynamic Rise Time Sluggish Failure (> 25 ms) *)
IF bRiseTimeCalcDone AND (rIntensificationRiseTime_ms >= c_rIntensRiseTime_HH) THEN
    dwIsaAlarmWord1 := dwIsaAlarmWord1 OR 16#00000008;
ELSIF bRiseTimeCalcDone AND (rIntensificationRiseTime_ms < c_rIntensRiseTime_H) THEN
    dwIsaAlarmWord1 := dwIsaAlarmWord1 AND NOT 16#00000008;
END_IF;

(* Bit 4: Mold Protection Low-Pressure Obstruction Detected *)
IF (iFsmState = 10) AND (rToggleCylinderHeadPress_bar > 45.0) AND (rMovingPlatenPos_mm > 5.0) AND (rMovingPlatenPos_mm <= 400.0) THEN
    dwIsaAlarmWord1 := dwIsaAlarmWord1 OR 16#00000010;
END_IF;

(* Bit 5: Dual Magnetostrictive Plunger Position Encoder Failure *)
IF tPlungerEncoderDiscrepancyTimer.Q THEN
    dwIsaAlarmWord1 := dwIsaAlarmWord1 OR 16#00000020;
ELSE
    dwIsaAlarmWord1 := dwIsaAlarmWord1 AND NOT 16#00000020;
END_IF;

(* Bit 6: Hydraulic Reservoir Oil Temperature High-High Emergency (> 65 deg C) *)
IF rHydraulicOilTemp_degC >= c_rOilTemp_HH THEN
    dwIsaAlarmWord1 := dwIsaAlarmWord1 OR 16#00000040;
ELSIF rHydraulicOilTemp_degC < (c_rOilTemp_HH - 3.0) THEN
    dwIsaAlarmWord1 := dwIsaAlarmWord1 AND NOT 16#00000040;
END_IF;

(* Bit 7: Hardwired Safety String E-Stop Tripped *)
IF NOT bEmergencyStopOk THEN
    dwIsaAlarmWord1 := dwIsaAlarmWord1 OR 16#00000080;
ELSE
    dwIsaAlarmWord1 := dwIsaAlarmWord1 AND NOT 16#00000080;
END_IF;

(* Bit 8: Solidified Biscuit Cake Under-Thickness Flash Blowout (< 15 mm) *)
IF (iFsmState >= 80) AND (rMeasuredBiscuitThickness_mm < c_rBiscuit_LL) AND (rMeasuredBiscuitThickness_mm > 0.0) THEN
    dwIsaAlarmWord1 := dwIsaAlarmWord1 OR 16#00000100;
END_IF;

(* Bit 9: Solidified Biscuit Cake Over-Thickness Cold Shot Freeze (> 55 mm) *)
IF (iFsmState >= 80) AND (rMeasuredBiscuitThickness_mm >= c_rBiscuit_HH) THEN
    dwIsaAlarmWord1 := dwIsaAlarmWord1 OR 16#00000200;
END_IF;

(* Bit 10: 2oo3 Cavity Vacuum Transducers Total Loss of Redundancy *)
IF iVacVotingHealthMode = 0 THEN
    dwIsaAlarmWord1 := dwIsaAlarmWord1 OR 16#00000400;
ELSE
    dwIsaAlarmWord1 := dwIsaAlarmWord1 AND NOT 16#00000400;
END_IF;

(* Bit 11: Safety Door Enclosure Breached During Cycle *)
IF NOT bMoldSafetyGateClosed AND (iFsmState > 10) AND (iFsmState < 120) THEN
    dwIsaAlarmWord1 := dwIsaAlarmWord1 OR 16#00000800;
END_IF;

(* --- 5.2: Priority 2 / Operational Warnings & Quality Interlocks (dwIsaAlarmWord2) --- *)
(* Bit 0: Tie-Bar Asymmetric Imbalance Warning (> 6.5%) *)
IF (rTieBarImbalance_pct >= c_rImbalance_H) AND (rTieBarImbalance_pct < c_rImbalance_HH) THEN
    dwIsaAlarmWord2 := dwIsaAlarmWord2 OR 16#00000001;
ELSE
    dwIsaAlarmWord2 := dwIsaAlarmWord2 AND NOT 16#00000001;
END_IF;

(* Bit 1: Cavity Vacuum Insufficient Warning (> 80 mbar at In-Gate Trigger) *)
IF (iFsmState >= 50) AND (rVotedVacuumPressure_mbar > c_rVacuum_H) THEN
    dwIsaAlarmWord2 := dwIsaAlarmWord2 OR 16#00000002;
ELSE
    dwIsaAlarmWord2 := dwIsaAlarmWord2 AND NOT 16#00000002;
END_IF;

(* Bit 2: 2oo3 Cavity Vacuum Transducer Sensor Discrepancy Debounced *)
IF tVacDiscrepancyTimer.Q THEN
    dwIsaAlarmWord2 := dwIsaAlarmWord2 OR 16#00000004;
ELSE
    dwIsaAlarmWord2 := dwIsaAlarmWord2 AND NOT 16#00000004;
END_IF;

(* Bit 3: Nitrogen Accumulator Charge Pressure Under-Pressure (< 195 bar) *)
IF rAccumulatorPress_bar < 195.0 THEN
    dwIsaAlarmWord2 := dwIsaAlarmWord2 OR 16#00000008;
ELSIF rAccumulatorPress_bar >= 208.0 THEN
    dwIsaAlarmWord2 := dwIsaAlarmWord2 AND NOT 16#00000008;
END_IF;

(* Bit 4: Holding Furnace Molten Aluminum Bath Temperature Out of Range *)
IF (rFurnaceMetalTemp_degC < c_rMetalTemp_L) OR (rFurnaceMetalTemp_degC > c_rMetalTemp_H) THEN
    dwIsaAlarmWord2 := dwIsaAlarmWord2 OR 16#00000010;
ELSE
    dwIsaAlarmWord2 := dwIsaAlarmWord2 AND NOT 16#00000010;
END_IF;

(* Bit 5: Hydraulic Reservoir Oil Temperature High Warning (> 55 deg C) *)
IF (rHydraulicOilTemp_degC >= c_rOilTemp_H) AND (rHydraulicOilTemp_degC < c_rOilTemp_HH) THEN
    dwIsaAlarmWord2 := dwIsaAlarmWord2 OR 16#00000020;
ELSIF rHydraulicOilTemp_degC < (c_rOilTemp_H - 2.0) THEN
    dwIsaAlarmWord2 := dwIsaAlarmWord2 AND NOT 16#00000020;
END_IF;

(* Bit 6: Die Release Agent Lubrication Supply Pressure Low (< 4.0 bar) *)
IF rDieLubeLinePress_bar < 4.0 THEN
    dwIsaAlarmWord2 := dwIsaAlarmWord2 OR 16#00000040;
ELSE
    dwIsaAlarmWord2 := dwIsaAlarmWord2 AND NOT 16#00000040;
END_IF;

(* Bit 7: Compressed Air Cavity Blow-Dry Header Pressure Low (< 5.0 bar) *)
IF rAirBlastLinePress_bar < 5.0 THEN
    dwIsaAlarmWord2 := dwIsaAlarmWord2 OR 16#00000080;
ELSE
    dwIsaAlarmWord2 := dwIsaAlarmWord2 AND NOT 16#00000080;
END_IF;

(* Bit 8: Fixed Die Core Insert Surface Temperature High (> 250 deg C) *)
IF rDieTempFixed_degC > 250.0 THEN
    dwIsaAlarmWord2 := dwIsaAlarmWord2 OR 16#00000100;
ELSE
    dwIsaAlarmWord2 := dwIsaAlarmWord2 AND NOT 16#00000100;
END_IF;

(* Bit 9: Moving Die Core Insert Surface Temperature High (> 250 deg C) *)
IF rDieTempMoving_degC > 250.0 THEN
    dwIsaAlarmWord2 := dwIsaAlarmWord2 OR 16#00000200;
ELSE
    dwIsaAlarmWord2 := dwIsaAlarmWord2 AND NOT 16#00000200;
END_IF;

(* Bit 10: Biscuit Residual Thickness Minor Out-of-Tolerance Deviation *)
IF ((rMeasuredBiscuitThickness_mm < c_rBiscuit_L) AND (rMeasuredBiscuitThickness_mm >= c_rBiscuit_LL)) OR
   ((rMeasuredBiscuitThickness_mm > c_rBiscuit_H) AND (rMeasuredBiscuitThickness_mm <= c_rBiscuit_HH)) THEN
    dwIsaAlarmWord2 := dwIsaAlarmWord2 OR 16#00000400;
ELSE
    dwIsaAlarmWord2 := dwIsaAlarmWord2 AND NOT 16#00000400;
END_IF;

(* --- 5.3: Alarm Latching & Acknowledgment Management (dwIsaAlarmWord3 & Word4) --- *)
IF bReset THEN
    dwIsaAlarmWord3 := 16#00000000; (* Clear Unacknowledged Alarm Latches *)
ELSE
    (* Latch Any Newly Triggered Critical Trip or Warning *)
    dwIsaAlarmWord3 := dwIsaAlarmWord3 OR dwIsaAlarmWord1 OR dwIsaAlarmWord2;
END_IF;

(* Aggregate Master Critical Trip and Warning Status *)
bCriticalTripActive := (dwIsaAlarmWord1 <> 16#00000000);
bWarningActive := (dwIsaAlarmWord2 <> 16#00000000);

(* --- 5.4: Bit-Pack Machine Status Words (dwSystemStatusWord1 & Word2) --- *)
dwSystemStatusWord1 := 16#00000000;
IF bEnable THEN dwSystemStatusWord1 := dwSystemStatusWord1 OR 16#00000001; END_IF;
IF bEmergencyStopOk THEN dwSystemStatusWord1 := dwSystemStatusWord1 OR 16#00000002; END_IF;
IF bMoldSafetyGateClosed THEN dwSystemStatusWord1 := dwSystemStatusWord1 OR 16#00000004; END_IF;
IF (rTotalClampTonnage_tons >= c_rTonnage_L) THEN dwSystemStatusWord1 := dwSystemStatusWord1 OR 16#00000008; END_IF;
IF bCore1InLimit AND bCore2InLimit THEN dwSystemStatusWord1 := dwSystemStatusWord1 OR 16#00000010; END_IF;
IF bVacuumGateValveOpen THEN dwSystemStatusWord1 := dwSystemStatusWord1 OR 16#00000020; END_IF;
IF bFastShotCartridgeOpen THEN dwSystemStatusWord1 := dwSystemStatusWord1 OR 16#00000040; END_IF;
IF bIntensifierPoppetFire THEN dwSystemStatusWord1 := dwSystemStatusWord1 OR 16#00000080; END_IF;
IF bLadlerPermissive THEN dwSystemStatusWord1 := dwSystemStatusWord1 OR 16#00000100; END_IF;
IF bExtractorPermissive THEN dwSystemStatusWord1 := dwSystemStatusWord1 OR 16#00000200; END_IF;
IF bSprayerPermissive THEN dwSystemStatusWord1 := dwSystemStatusWord1 OR 16#00000400; END_IF;
IF bAccumulatorChargeCmd THEN dwSystemStatusWord1 := dwSystemStatusWord1 OR 16#00000800; END_IF;
IF bAutoCycleStartCmd THEN dwSystemStatusWord1 := dwSystemStatusWord1 OR 16#00001000; END_IF;

dwSystemStatusWord2 := 16#00000000;
dwSystemStatusWord2 := dwSystemStatusWord2 OR INT_TO_DWORD(iFsmState);
IF bCavityFullImpactDetected THEN dwSystemStatusWord2 := dwSystemStatusWord2 OR 16#00010000; END_IF;
IF bInGateTriggerCrossed THEN dwSystemStatusWord2 := dwSystemStatusWord2 OR 16#00020000; END_IF;
IF (iVacVotingHealthMode = 3) THEN dwSystemStatusWord2 := dwSystemStatusWord2 OR 16#00040000; END_IF;
IF (iVacVotingHealthMode = 2) THEN dwSystemStatusWord2 := dwSystemStatusWord2 OR 16#00080000; END_IF;
IF (iVacVotingHealthMode <= 1) THEN dwSystemStatusWord2 := dwSystemStatusWord2 OR 16#00100000; END_IF;

END_FUNCTION_BLOCK
""")

    code_str = "".join(parts)
    return code_str

def main():
    code_body = build_code()
    full_content = "```iec-st\n" + code_body.strip() + "\n```"
    
    print(f"Generated ST code character count: {len(full_content)}")
    
    # Run in-memory validation
    errs = validate_iec.validate_iec_st(code_body)
    if errs:
        print("VALIDATION ERRORS:")
        for e in errs:
            print(" -", e)
        return False
    else:
        print("IN-MEMORY VALIDATION PASSED!")

    # Write JSON record
    record = {
        "messages": [
            {"role": "user", "content": user_prompt},
            {"role": "assistant", "content": full_content}
        ]
    }
    
    out_path = "data/swarm_raw/agent_5b20a17f.json"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
        
    print(f"Saved dataset successfully to {out_path}")
    
    # Validate written file
    file_errs = validate_iec.validate_json_file(out_path)
    if file_errs:
        print("FILE VALIDATION ERRORS:")
        for e in file_errs:
            print(" -", e)
        return False
    else:
        print("FILE VALIDATION PASSED COMPLETELY!")
        return True

if __name__ == "__main__":
    main()
