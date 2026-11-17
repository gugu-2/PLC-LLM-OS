# build_gigapress_full.py
# Generates the complete, ultra-dense IEC 61131-3 Structured Text FUNCTION_BLOCK
# for FB_Automotive_MegaCasting_9000Ton_RealTimeShot_Vacuum

import json
import uuid
import os
import sys

def get_header():
    return """FUNCTION_BLOCK FB_Automotive_MegaCasting_9000Ton_RealTimeShot_Vacuum
(*
========================================================================================================================
LUMINA CYBER-PHYSICAL AUTOMATION ENGINE - SYNTHETIC DATASET V7 MAX-PERSONA
COMMERCIAL AUTOMOTIVE FOUNDRY & STRUCTURAL MEGA-CASTING DIVISION
========================================================================================================================
SYSTEM SPECIFICATION:
  - Machine Type:        9,000-Ton Ultra-Large High-Pressure Die Casting Machine (Giga-Press / Mega-Casting Cell)
  - Target Component:    Single-Piece Integrated Automotive Rear Underbody Structural Casting
  - Alloy Specification: Hypoeutectic Aluminum-Silicon Die Casting Alloy (AlSi10MnMg / A380 High-Ductility Structural)
  - Shot Dose Weight:    110.0 kg Liquid Aluminum per Machine Cycle (Net casting mass: 82.5 kg, Runners/Biscuits: 27.5 kg)
  - Plunger Dimensions:  Diameter = 180.0 mm (Cross-sectional Area = 0.025447 m^2), Shot Sleeve Length = 1,400.0 mm
  - Nominal Clamp Force: 90,000.0 kN (9,177 Metric Tons) across Four 750.0 mm Diameter High-Tensile 4340 Alloy Tie-Bars
  - Hydraulic Injection: 3-Stage Closed-Loop Hydraulic Servo System with 400 L Piston Nitrogen Accumulator (320 bar precharge)
  - Intensification:     Differential Booster Cylinder (Ratio 4.2:1) capable of peak static squeeze pressure up to 1,400.0 bar
  - High-Vacuum System:  Tri-Stage Roots Blower Station with Evacuated Surge Tank (4,000 L) pulling cavity < 25.0 mbar
  - Vacuum Chill Vent:   Acoustic/Hydraulic High-Speed Chill-Block Shutoff Valve with < 8.0 ms Dynamic Seat Closure
  - Control Execution:   Deterministic 1.0 ms Task Interrupt Cycle (IEC 61131-3 3rd Edition Structured Text)

CYBER-PHYSICAL SYSTEM ARCHITECTURE & GOVERNING PRINCIPLES:
  1. Multi-Phase Closed-Loop Shot Dynamics:
     - Phase 1 (Slow Shot): Plunger advances at nominal velocity v1 = 0.25 m/s. The free surface profile of molten aluminum
       is governed by open-channel shallow water wave dynamics. Plunger acceleration is actively sculpted using critical
       Froude number criteria (Fr = v / sqrt(g * h_eff) < 0.95) to prevent wave rollover, surface turbulence, and air
       entrapment within the shot sleeve before the pour hole is sealed and the sleeve is compacted.
     - Phase 2 (Fast Shot): Plunger accelerates dynamically (a_shot >= 45.0 m/s^2) up to v2 = 8.5 m/s in < 35.0 ms,
       discharging the molten metal front through multiple fanned tangential runners at gate velocities exceeding 65.0 m/s.
       The complete 0.038 m^3 rear underbody thin-walled cavity (mean wall thickness 2.5 mm) is filled in under 40.0 ms
       to eliminate cold shuts and premature laminar freezing.
     - Phase 3 (Intensification Squeeze): Upon instantaneous cavity fill impact (detected by multi-channel gate pressure
       transducers and cavity arrival optical sensors), the servo pilot switches to the 4.2:1 differential intensifier booster.
       Hydraulic head pressure spikes to 1,400.0 bar with a 10%-90% rise time of < 15.0 ms, delivering dynamic squeeze
       pressure into the mushy metal zone to collapse dendritic shrinkage micro-porosity before gate freeze-off occurs.

  2. 4-Tie-Bar Dynamic Clamping Tonnage & Eccentricity Balancing:
     - The movable platen (mass 140 metric tons) is clamped against the fixed cover die by four massive 750 mm diameter
       tie-bars under 90,000 kN nominal pre-stress. Due to asymmetric die cavity geometry, non-uniform thermal expansion,
       and heavy bottom-biased runner layouts, unbalanced thermal and mechanical forces can induce severe platen tilting,
       causing molten aluminum die flash blowouts (catastrophic safety hazard) and permanent tie-bar fatigue cracking.
     - Dynamic strain gauge extensometers continuously measure tension on Tie-Bars 1 (Top-Left), 2 (Top-Right), 3 (Bottom-Left),
       and 4 (Bottom-Right). The block computes horizontal, vertical, and diagonal bending moments and dynamically commands
       individual high-pressure hydraulic pre-stress nuts to maintain total load balance within +/- 2.0% of nominal setpoint.

  3. High-Vacuum Evacuation & Acoustic Chill-Block Fast Shutoff:
     - To achieve structural ductility (> 10% elongation at break for automotive crash safety), dissolved gas and trapped
       air must be extracted prior to metal arrival. A tri-stage Roots vacuum package evacuates the sealed die cavity to
       below 25.0 mbar within 250.0 ms during Phase 1.
     - When the molten metal front reaches the chill-block venting channels at the end of cavity fill, an ultra-fast
       hydraulic chill-block valve must snap shut in < 8.0 ms. If closure is sluggish (> 8.0 ms), molten aluminum penetrates
       the vacuum line, destroying expensive vacuum instrumentation and disabling the entire foundry production cell.

  4. Multivariable Discrete State-Space Model & Receding-Horizon MPC:
     - Continuous-time dynamics linearized around operating trajectory:
         x[k+1] = A * x[k] + B * u[k] + w[k]
         y[k]   = C * x[k] + D * u[k] + v[k]
     - States (6x1):
         x1: Plunger Injection Velocity [m/s]
         x2: Hydraulic Shot Cylinder Head Pressure [bar]
         x3: Mold Cavity Vacuum Level [mbar]
         x4: Total 4-Tie-Bar Clamping Force [kN]
         x5: Mold Cavity Face Surface Temperature [deg C]
         x6: Cast Part Shell Solidification Thickness [mm]
     - Actuators (5x1):
         u1: High-Response Servo Shot Proportional Pilot Valve [%] (0 - 100%)
         u2: High-Speed Accumulator Discharge Poppet Valve [%] (0 - 100%)
         u3: Intensifier Multiplier Booster Pilot Valve [%] (0 - 100%)
         u4: High-Vacuum Cavity Extraction Throttle Valve [%] (0 - 100%)
         u5: Die Tempering Thermal Oil Circulating Pump Speed [%] (0 - 100%)
     - Receding-Horizon MPC executes 10 unrolled Projected Gradient Descent (PGD) iterations solving:
         min J = sum_{k=0}^{N-1} [ (x[k]-x_ref)^T * Q * (x[k]-x_ref) + (u[k]-u_ref)^T * R * (u[k]-u_ref) + delta_u^T * S * delta_u ]
                 + (x[N]-x_ref)^T * P * (x[N]-x_ref)
         subject to actuator velocity limits, hydraulic flow saturation, and tie-bar anti-flash safety bounds.
========================================================================================================================
*)
"""

def get_var_input():
    return """VAR_INPUT
    (* === MASTER AUTOMATION CONTROL & SYNCHRONIZATION COMMANDS === *)
    bCycleStartCommand             : BOOL;     (* [bool] Master automatic casting cycle initiation trigger *)
    bCycleAbortCommand             : BOOL;     (* [bool] Immediate cycle abort and return to safe standby *)
    bAlarmReset                    : BOOL;     (* [bool] Master fault acknowledge and alarm latch reset *)
    bEmergencyStopCircuit_NC       : BOOL;     (* [bool] Dual-channel hardwired safety relay contact active high *)
    bSafetyPerimeterCageLocked     : BOOL;     (* [bool] Foundry cell perimeter interlock fence gate locked *)
    bManualAutoModeSelect          : BOOL;     (* [bool] Cell operating mode selector (FALSE = Manual, TRUE = Auto) *)
    rCycleTime_sec                 : REAL := 0.001; (* [s] Deterministic task execution cycle period nominal 1.0 ms *)

    (* === TRIPLE MODULAR REDUNDANT (2oo3) PROCESS INSTRUMENTATION CHANNELS === *)
    (* Channel A, B, C Magnetostrictive Plunger Velocity Sensors *)
    rPlungerVel_A_ms               : REAL;     (* [m/s] Injection cylinder rod velocity transducer channel A *)
    rPlungerVel_B_ms               : REAL;     (* [m/s] Injection cylinder rod velocity transducer channel B *)
    rPlungerVel_C_ms               : REAL;     (* [m/s] Injection cylinder rod velocity transducer channel C *)

    (* Channel A, B, C Hydraulic Shot Head Pressure Sensors *)
    rShotPress_A_bar               : REAL;     (* [bar] Piezoresistive injection cylinder head pressure channel A *)
    rShotPress_B_bar               : REAL;     (* [bar] Piezoresistive injection cylinder head pressure channel B *)
    rShotPress_C_bar               : REAL;     (* [bar] Piezoresistive injection cylinder head pressure channel C *)

    (* Channel A, B, C High-Speed Mold Cavity Vacuum Transmitters *)
    rCavityVac_A_mbar              : REAL;     (* [mbar] High-vacuum Pirani/capacitance cavity sensor channel A *)
    rCavityVac_B_mbar              : REAL;     (* [mbar] High-vacuum Pirani/capacitance cavity sensor channel B *)
    rCavityVac_C_mbar              : REAL;     (* [mbar] High-vacuum Pirani/capacitance cavity sensor channel C *)

    (* Channel A, B, C Gross Tie-Bar Clamping Force Load Cells *)
    rClampForce_A_kN               : REAL;     (* [kN] Gross hydraulic clamping force strain ring channel A *)
    rClampForce_B_kN               : REAL;     (* [kN] Gross hydraulic clamping force strain ring channel B *)
    rClampForce_C_kN               : REAL;     (* [kN] Gross hydraulic clamping force strain ring channel C *)

    (* === INDIVIDUAL 4-TIE-BAR HIGH-PRECISION STRAIN EXTENSOMETERS === *)
    rTieBarForce_TB1_kN            : REAL;     (* [kN] Tie-Bar #1 Top-Left mechanical tension strain load *)
    rTieBarForce_TB2_kN            : REAL;     (* [kN] Tie-Bar #2 Top-Right mechanical tension strain load *)
    rTieBarForce_TB3_kN            : REAL;     (* [kN] Tie-Bar #3 Bottom-Left mechanical tension strain load *)
    rTieBarForce_TB4_kN            : REAL;     (* [kN] Tie-Bar #4 Bottom-Right mechanical tension strain load *)

    (* === SHOT SLEEVE & PLUNGER KINEMATIC POSITION ENCODERS === *)
    rPlungerPos_mm                 : REAL;     (* [mm] Shot plunger absolute linear position encoder (0 - 1400 mm) *)
    rAccumulatorPressure_bar       : REAL;     (* [bar] High-pressure nitrogen shot accumulator bottle pressure *)
    rIntensifierSupplyPress_bar    : REAL;     (* [bar] Hydraulic power unit intensifier supply rail pressure *)

    (* === LIQUID METAL FRONT DETECTION & ARRIVAL CONTINUITY SENSORS === *)
    bMetalFront_Gate1              : BOOL;     (* [bool] Fast electrical continuity sensor at runner gate #1 *)
    bMetalFront_Gate2              : BOOL;     (* [bool] Fast electrical continuity sensor at runner gate #2 *)
    bMetalFront_ChillBlock         : BOOL;     (* [bool] Optical/conductivity arrival sensor at chill vent inlet *)

    (* === PRESSURIZED DIE THERMAL REGULATION SENSORS === *)
    rDieTemp_Cover_degC            : REAL;     (* [deg C] Fixed cover platen cavity surface infrared thermocouple *)
    rDieTemp_Ejector_degC          : REAL;     (* [deg C] Moving ejector platen cavity surface thermocouple *)
    rDieTemp_CoreInsert_degC       : REAL;     (* [deg C] Critical thin-walled structural core insert thermocouple *)
    rTemperingOilSupplyTemp_degC   : REAL;     (* [deg C] Thermal fluid circuit manifold supply temperature *)
    rTemperingOilReturnTemp_degC   : REAL;     (* [deg C] Thermal fluid circuit manifold return temperature *)

    (* === ROBOTIC AUTOMATION & FOUNDRY CELL INTERFACING PERMISSIVES === *)
    rMeltTemp_degC                 : REAL;     (* [deg C] Molten aluminum holding furnace ladle tap temperature *)
    rLadleDoseWeight_kg            : REAL;     (* [kg] Liquid alloy pour weight delivered by dosing robot *)
    bLadlePourComplete             : BOOL;     (* [bool] Dosing ladle pour cycle finished and ladle arm clear *)
    bDieSprayedAndDried            : BOOL;     (* [bool] Gantry lube robot release agent spray & air purge complete *)
    bExtractorRobotInPosition      : BOOL;     (* [bool] Heavy gantry casting extractor gripper in home position *)
    bEjectorPlatesRetracted_LS     : BOOL;     (* [bool] Multi-point hydraulic ejector pin mechanism retracted *)
    bChillBlockValveOpen_LS        : BOOL;     (* [bool] Acoustic chill-block vacuum shutoff valve open limit switch *)
    bChillBlockValveClosed_LS      : BOOL;     (* [bool] Acoustic chill-block vacuum shutoff valve closed limit switch *)
    bHydraulicPowerUnitReady       : BOOL;     (* [bool] Main 750 kW hydraulic power unit pressure and flow healthy *)
    bVacuumRootsStationReady       : BOOL;     (* [bool] Multi-stage Roots vacuum station running and tank evacuated *)
    bMpcGovernorEnable             : BOOL := TRUE; (* [bool] Enable multivariable Receding-Horizon MPC optimization *)
END_VAR
"""

def get_var_output():
    return """VAR_OUTPUT
    (* === HIGH-RESPONSE HYDRAULIC ACTUATOR ANALOG COMMAND OUTPUTS === *)
    rPilotValve_Shot_pct           : REAL;     (* [%] u1: High-response Moog/Bosch servo proportional pilot valve (0-100%) *)
    rAccumulatorPoppet_pct         : REAL;     (* [%] u2: Ultra-fast cartridge accumulator discharge poppet valve (0-100%) *)
    rIntensifierValve_pct          : REAL;     (* [%] u3: 4.2:1 Intensification booster multiplier pilot valve (0-100%) *)
    rVacuumValve_pct               : REAL;     (* [%] u4: High-vacuum line extraction proportional throttle valve (0-100%) *)
    rTemperingPump_pct             : REAL;     (* [%] u5: Die thermal tempering oil circulating pump speed command (0-100%) *)
    rEjectorDrive_pct              : REAL;     (* [%] Hydraulic multi-point ejector plate proportional drive (0-100%) *)

    (* === INDIVIDUAL 4-TIE-BAR HYDRAULIC PRE-STRESS BALANCING ACTUATORS === *)
    rTieBar1_HydNut_pct            : REAL;     (* [%] Tie-Bar 1 Top-Left hydraulic pre-stress nut servo valve command *)
    rTieBar2_HydNut_pct            : REAL;     (* [%] Tie-Bar 2 Top-Right hydraulic pre-stress nut servo valve command *)
    rTieBar3_HydNut_pct            : REAL;     (* [%] Tie-Bar 3 Bottom-Left hydraulic pre-stress nut servo valve command *)
    rTieBar4_HydNut_pct            : REAL;     (* [%] Tie-Bar 4 Bottom-Right hydraulic pre-stress nut servo valve command *)

    (* === ULTRA-FAST DIGITAL SAFETY & SEQUENCE TRIGGER COMMANDS === *)
    bFastShutoffChillValve_CMD     : BOOL;     (* [bool] Acoustic/hydraulic chill-block shutoff valve fast pilot trigger *)
    bDieSafetyClampLock_CMD        : BOOL;     (* [bool] Platen mechanical toggle & hydraulic pre-stress lock command *)
    bLadleRobotPermissive_CMD      : BOOL;     (* [bool] Safe pour permissive to robotic molten aluminum ladle *)
    bSprayRobotInitiate_CMD        : BOOL;     (* [bool] Parting agent spray sequence initiation trigger *)
    bExtractorRobotInitiate_CMD    : BOOL;     (* [bool] Heavy gantry part extraction sequence trigger *)
    bVacuumRootsIsolation_CMD      : BOOL;     (* [bool] High-vacuum surge tank main suction isolation butterfly valve *)

    (* === 2oo3 TMR VALIDATED PROCESS TELEMETRY & ESTIMATED STATES === *)
    iState                         : INT;      (* [enum] Active FSM operating state index (0 to 13) *)
    rPlungerVel_Voted_ms           : REAL;     (* [m/s] 2oo3 TMR median voted injection plunger velocity *)
    rShotPress_Voted_bar           : REAL;     (* [bar] 2oo3 TMR median voted injection head pressure *)
    rCavityVac_Voted_mbar          : REAL;     (* [mbar] 2oo3 TMR median voted mold cavity vacuum pressure *)
    rClampForce_Voted_kN           : REAL;     (* [kN] 2oo3 TMR median voted total clamping force *)
    rSolidificationThickness_mm    : REAL;     (* [mm] State-space estimated structural part skin thickness *)
    rTieBarMaxEccentricity_kN      : REAL;     (* [kN] Maximum measured dynamic tie-bar tension asymmetry *)
    rCavityPeakPressure_bar        : REAL;     (* [bar] Peak hydraulic head pressure during intensification squeeze *)

    (* === PROCESS METROLOGY & QUALITY ASSURANCE RECORDINGS === *)
    rPhase1Duration_ms             : REAL;     (* [ms] Measured elapsed time for Phase 1 slow shot compaction *)
    rPhase2Duration_ms             : REAL;     (* [ms] Measured elapsed time for Phase 2 fast cavity fill (< 40.0 ms) *)
    rPhase3RiseTime_ms             : REAL;     (* [ms] Measured 10% to 90% rise time of 1,400 bar intensification *)
    rChillValveCloseTime_ms        : REAL;     (* [ms] Measured acoustic chill-block closure latency (< 8.0 ms) *)
    rTotalCycleDuration_sec        : REAL;     (* [s] Total floor-to-floor casting machine cycle duration *)

    (* === AUTOMATION RUN STATUS, INTERLOCKS & ISA-18.2 ALARM TELEMETRY === *)
    bSystemRunning                 : BOOL;     (* [bool] Automatic mega-casting cycle active and executing *)
    bSystemReady                   : BOOL;     (* [bool] All cycle start permissives satisfied, standing by *)
    bSystemTripped                 : BOOL;     (* [bool] Hard process trip latched, machine in emergency safe hold *)
    bWarningActive                 : BOOL;     (* [bool] ISA-18.2 Priority 3 advisory warning active *)
    bMpcInOptimization             : BOOL;     (* [bool] Receding-horizon MPC gradient descent active this cycle *)
    dwStatusWord1                  : DWORD;    (* [dword] Bit-packed 32-bit production FSM and subsystem sequence status *)
    dwStatusWord2                  : DWORD;    (* [dword] Bit-packed 32-bit 2oo3 TMR instrument degradation status *)
    dwAlarmWord1                   : DWORD;    (* [dword] Bit-packed 32-bit ISA-18.2 Priority 1 & 2 process trip alarms *)
    dwAlarmWord2                   : DWORD;    (* [dword] Bit-packed 32-bit ISA-18.2 Priority 3 & 4 equipment warning alarms *)
    dwFirstOutWord                 : DWORD;    (* [dword] Bit-packed 32-bit ISA-18.2 First-Out root cause trip capture *)
END_VAR
"""

if __name__ == "__main__":
    print("Testing Header and IO blocks...")
    print("Header len:", len(get_header()))
    print("Var Input len:", len(get_var_input()))
    print("Var Output len:", len(get_var_output()))
