# -*- coding: utf-8 -*-
"""
Builder script for 300 mm Dual-Spindle Silicon Wafer Dicing Saw
with In-Line Kerf Width AOI Inspection & Dynamic Blade Wear Tracking.
Target Output: data/swarm_raw/agent_9a10cb4e.json
Function Block: FB_Semiconductor_WaferDicing_DualSpindle_AOI
"""

import json
import os
import sys
import validate_iec

user_prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices (A, B, C, D), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: Semiconductor & Wafer Packaging: 300 mm Dual-Spindle Silicon Wafer Dicing Saw with In-Line Kerf Width AOI Inspection & Dynamic Blade Wear Tracking: FB_Semiconductor_WaferDicing_DualSpindle_AOI - High-throughput 300 mm silicon wafer dicing saw with dual opposed aerostatic air-bearing spindles (Spindle 1 step-cut blade, Spindle 2 full-cut blade, 60,000 RPM, radial/axial runout < 0.05 microns), high-precision air-bearing vacuum chuck table (X feed axis coreless linear motor up to 800 mm/s with 1.0 nm resolution laser scale, Y index axis sub-micron pitch repeatability, Theta rotary axis alignment), in-line optical microscopes with dual-magnification coaxial lighting and line-scan cameras measuring kerf cut width (target 25.0 microns +/- 1.0 micron), top/backside silicon chipping size, and street alignment angle offsets, dynamic blade wear and exposure height tracking (non-contact optical setup sensor measuring blade outer diameter drop due to diamond attrition, closed-loop Z-axis depth-of-cut adjustment to maintain wafer tape penetration depth 20 microns into dicing tape without cutting through backing carrier), cutting fluid deionized water (DIW) delivery (multi-jet high-velocity cooling nozzles, closed-loop resistivity monitoring > 18 MOhm*cm, flow rate, air-mist cleaning), blade breakage acoustic emission (AE) sensor and spindle motor current load monitoring detecting instantaneous blade micro-fracture or binder glazing within 10 ms, 16x16 discrete state-space dynamic model (spindle motor torque dynamics, air-bearing aerodynamic film stiffness, linear axis structural compliance, blade diamond grit attrition mechanics), receding-horizon MPC for optimal feedrate modulation vs cutting resistance torque to prevent kerf wander and blade wander on ultra-thin wafers (50 microns thickness), 2oo3 TMR voting across spindle air bearing pressure transducers, DIW water flowmeters, and optical kerf width metrology readings, 12-stage operational FSM (Wafer Ring Frame Cassette Infeed, Vacuum Chuck Arm Transfer & Centering, Optical Pattern Recognition Theta Alignment, Blade Height Non-Contact Calibration, DIW Cooling Jet Initiation, Step-Cut & Full-Cut Street Dicing, High-Speed In-Flight Kerf Optical AOI, Cross-Street 90-Degree Indexing & Dicing, Wafer DIW Spinner Wash & Air Knife Dry, Wafer Unload to Output Magazine, Blade Glaze Dressing Sequence, Emergency Blade Breakage E-Stop Clamp), and ISA-18.2 multi-tiered alarm matrix.**

Generate a complete, fully implemented IEC 61131-3 Structured Text FUNCTION_BLOCK named FB_Semiconductor_WaferDicing_DualSpindle_AOI with zero placeholders, full state-space matrix initialization, MPC optimization, 2oo3 voting, full FSM execution, and ISA-18.2 alarm matrix."""

def build_header_and_var_input():
    return """FUNCTION_BLOCK FB_Semiconductor_WaferDicing_DualSpindle_AOI
(*
====================================================================================================
PROJECT:        ADVANCED SEMICONDUCTOR BACKEND PACKAGING & WAFER SINGULATION CONTROL
SUBSYSTEM:      300 MM DUAL-SPINDLE SILICON WAFER DICING SAW WITH IN-LINE KERF AOI & WEAR TRACKING
MODULE:         FB_Semiconductor_WaferDicing_DualSpindle_AOI
ARCHITECTURE:   16x16 DISCRETE STATE-SPACE OBSERVER + RECEDING-HORIZON MPC + 2oo3 TMR SENSOR FUSION +
                DYNAMIC BLADE WEAR ADAPTATION + 12-STAGE PRODUCTION FSM + ISA-18.2 MULTI-TIERED ALARMS
AUTHOR:         LUMINA CYBER-PHYSICAL AUTOMATION ARCHITECT (75+ YRS VETERAN FELLOW SPECIFICATION)
STANDARDS:      IEC 61131-3 3RD ED, SEMI E10 (EQUIPMENT RELIABILITY), SEMI G47 (DICING SAW GUIDELINES),
                SEMI S2/S8 (ENVIRONMENTAL HEALTH & SAFETY), ISO 13849-1 (PL-e SAFETY), ISA-18.2
TASK CYCLE:     DETERMINISTIC 10.0 MILLISECOND SYNCHRONOUS PLC SCAN (T_scan = 0.010 s)
====================================================================================================

MATHEMATICAL AND CYBER-PHYSICAL PRINCIPLES:
1. DUAL-SPINDLE STEP-CUT & FULL-CUT WAFER SINGULATION:
   The machine executes dual-spindle opposed kerf dicing on 300 mm (12-inch) single-crystal silicon
   wafers thinned down to 50.0 to 775.0 microns, mounted on UV-curable dicing tape and stainless steel
   ring frames. 
   - Spindle 1 (Step-Cut): Operates a resinoid or metal-bonded diamond blade (grit mesh 2000-3000,
     blade thickness 35.0 um) rotating at up to 60,000 RPM. Spindle 1 cuts the top 30-50% of the silicon
     wafer thickness along the circuit streets, eliminating surface chipping, delamination of low-k dielectric
     interlayer films (dielectric constant k < 2.5), and copper/aluminum interconnect peeling.
   - Spindle 2 (Full-Cut): Operates a high-precision electroformed nickel-diamond blade (blade thickness 25.0 um)
     rotating at 60,000 RPM, tracking in the wake of Spindle 1 along the same street centerline. Spindle 2
     severs the remaining silicon core and penetrates strictly 20.0 +/- 3.0 microns into the flexible
     dicing tape without piercing the underlying tape backing carrier or gouging the ceramic chuck table.

2. AEROSTATIC AIR-BEARING SPINDLE ROTODYNAMICS:
   Both spindles utilize aerostatic air-bearing journals and double-acting thrust bearings pressurized
   at 5.5 to 7.0 bar. Dynamic radial and axial air-film stiffness is governed by Reynolds equation:
       del . (P * h^3 * del(P) / mu) = 6 * U * del(P * h) / del(x) + 12 * del(P * h) / del(t)
   Under operating speeds (omega = 6,283.18 rad/s, peripheral blade velocity v_s = 180 m/s), total radial
   and axial runout is held to delta_r < 0.05 microns. Bearing compliance c_air = 0.012 um/N ensures
   unmatched rotational stability. Aerostatic pressure drop below 4.8 bar induces immediate dynamic braking.

3. CLOSED-LOOP DYNAMIC BLADE WEAR TRACKING & TAPE PENETRATION INTEGRATION:
   Diamond grits wear continuously via micro-attrition, micro-chipping, and mechanical pullout:
       d(Delta_D) / dt = k_attrition * (F_tangential * v_feed) / (H_grit * A_contact)
   Cumulative outer diameter loss delta_D causes the cutting apex to recede upward, leading to incomplete
   wafer cuts. In-line non-contact optical setup laser sensors measure the exact bottom blade edge datum
   at micron resolution. The controller dynamically updates the Z1 (step) and Z2 (full) axis setpoints:
       Z2_setpoint = Z_tape_surface - TargetPenetration + Delta_D2 / 2.0
   An active hardware limit detects if tape penetration exceeds 35.0 um, triggering an immediate safety trip
   to prevent carrier punch-through, slurry ingress, and vacuum collapse.

4. HIGH-VELOCITY DEIONIZED WATER (DIW) COOLANT DELIVERY & CLOSED-LOOP RESISTIVITY:
   Dual multi-jet high-pressure nozzles inject temperature-stabilized (21.0 +/- 0.5 deg C) DIW at > 3.5 L/min
   directly into the grinding contact arc. DIW flushes silicon swarf micro-particles (sub-micron to 5 um)
   to prevent diamond wheel loading (glazing) and thermal micro-cracks. DIW electrical resistivity is
   monitored in real time with temperature compensation:
       rho_25 = rho_meas * [1.0 + alpha_diw * (T_diw - 25.0)]
   Resistivity must remain >= 18.0 MOhm*cm to eliminate galvanic potential and metal migration across
   exposed copper and aluminum bond pads on neighboring active integrated circuits.

5. ACOUSTIC EMISSION (AE) FAST BLADE FRACTURE & GLAZING DETECTION:
   Piezoelectric acoustic emission sensors (100 kHz to 1.0 MHz bandpass) detect high-frequency transient
   elastic stress waves generated during diamond blade binder micro-fracture or binder glaze slip.
   An analog comparator and digital envelope peak-hold algorithm detect amplitude bursts > 85.0 dB or
   motor current surge rates |dI/dt| > 250 A/s within 10.0 ms, commanding immediate 15 ms Z-retract
   and dynamic spindle electrical braking to prevent catastrophic wafer shredding.

6. 16x16 DISCRETE STATE-SPACE MODEL & RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC):
   State vector x (16 states):
     x[1]:  Spindle 1 angular velocity deviation Delta_omega1 [rad/s]
     x[2]:  Spindle 2 angular velocity deviation Delta_omega2 [rad/s]
     x[3]:  Spindle 1 aerostatic radial air film deflection delta_r1 [um]
     x[4]:  Spindle 2 aerostatic radial air film deflection delta_r2 [um]
     x[5]:  Spindle 1 aerostatic axial compliance displacement delta_z1 [um]
     x[6]:  Spindle 2 aerostatic axial compliance displacement delta_z2 [um]
     x[7]:  X-axis coreless linear motor carriage velocity deviation Delta_vx [mm/s]
     x[8]:  X-axis chuck structural compliant vibration mode xi_x [um]
     x[9]:  Blade 1 step-cut tangential grinding force F_t1 [N]
     x[10]: Blade 2 full-cut tangential grinding force F_t2 [N]
     x[11]: Blade 1 diamond grit outer diameter attrition Delta_D1 [um]
     x[12]: Blade 2 diamond grit outer diameter attrition Delta_D2 [um]
     x[13]: Kerf 1 cut width deviation from nominal 25.0 um setpoint Delta_w1 [um]
     x[14]: Kerf 2 cut width deviation from nominal 25.0 um setpoint Delta_w2 [um]
     x[15]: DIW coolant hydrodynamic wedge pressure P_diw [bar]
     x[16]: Ultra-thin wafer micro-crack chipping propagation metric chi_chip [um]
   Input vector u (8 inputs):
     u[1]: Spindle 1 motor torque current demand i_q1 [A]
     u[2]: Spindle 2 motor torque current demand i_q2 [A]
     u[3]: X-axis linear motor feed velocity demand v_x,cmd [mm/s]
     u[4]: Z1-axis step-cut position fine trim Delta_z1 [um]
     u[5]: Z2-axis full-cut position fine trim Delta_z2 [um]
     u[6]: Y-axis index tracking position fine trim Delta_y [um]
     u[7]: DIW coolant nozzle high-pressure valve trim u_diw [%]
     u[8]: Acoustic emission blade breakage adaptive sensitivity factor k_ae [-]
*)

VAR_INPUT
    (* MASTER DIGITAL PERMISSIVES & SUPERVISORY COMMANDS *)
    bEnableSystem                   : BOOL;     (* Master automation enable permissive *)
    bEmergencyStop                  : BOOL;     (* Active-low SIL-3 hardwired safety circuit *)
    bResetFaults                    : BOOL;     (* Master alarm acknowledgement and unlatch command *)
    bAutoCycleStart                 : BOOL;     (* Automatic wafer dicing sequence start *)
    bPauseCycle                     : BOOL;     (* Cycle pause / feed hold command *)
    bDressBladesCmd                 : BOOL;     (* Operator manual blade dressing request *)
    bMpcEnable                      : BOOL;     (* Enable receding-horizon MPC feedrate optimizer *)
    bAoiInspectionEnable            : BOOL;     (* Enable in-line optical kerf AOI metrology *)

    (* TRIPLE MODULAR REDUNDANCY (2oo3) SPINDLE 1 AIR BEARING PRESSURE [bar] *)
    rSpindle1AirPress_A_bar         : REAL;     (* Spindle 1 aerostatic pressure transmitter PT-11A [bar] *)
    rSpindle1AirPress_B_bar         : REAL;     (* Spindle 1 aerostatic pressure transmitter PT-11B [bar] *)
    rSpindle1AirPress_C_bar         : REAL;     (* Spindle 1 aerostatic pressure transmitter PT-11C [bar] *)

    (* TRIPLE MODULAR REDUNDANCY (2oo3) SPINDLE 2 AIR BEARING PRESSURE [bar] *)
    rSpindle2AirPress_A_bar         : REAL;     (* Spindle 2 aerostatic pressure transmitter PT-12A [bar] *)
    rSpindle2AirPress_B_bar         : REAL;     (* Spindle 2 aerostatic pressure transmitter PT-12B [bar] *)
    rSpindle2AirPress_C_bar         : REAL;     (* Spindle 2 aerostatic pressure transmitter PT-12C [bar] *)

    (* TRIPLE MODULAR REDUNDANCY (2oo3) VACUUM CHUCK HOLD-DOWN SENSORS [mbar] *)
    rChuckVacuum_A_mbar             : REAL;     (* Porous ceramic chuck vacuum sensor VT-21A [mbar] *)
    rChuckVacuum_B_mbar             : REAL;     (* Porous ceramic chuck vacuum sensor VT-21B [mbar] *)
    rChuckVacuum_C_mbar             : REAL;     (* Porous ceramic chuck vacuum sensor VT-21C [mbar] *)

    (* TRIPLE MODULAR REDUNDANCY (2oo3) DIW COOLANT FLOWMETERS [L/min] *)
    rDiwCoolantFlow_A_Lmin          : REAL;     (* DIW cooling water flow transmitter FT-31A [L/min] *)
    rDiwCoolantFlow_B_Lmin          : REAL;     (* DIW cooling water flow transmitter FT-31B [L/min] *)
    rDiwCoolantFlow_C_Lmin          : REAL;     (* DIW cooling water flow transmitter FT-31C [L/min] *)

    (* DIW COOLANT WATER QUALITY & TEMPERATURE TRANSMITTERS [MOhm*cm, deg C] *)
    rDiwResistivity_MOhm_cm         : REAL;     (* DIW coolant inline resistivity cell [MOhm*cm] *)
    rDiwTemperature_DegC            : REAL;     (* DIW coolant supply fluid temperature [deg C] *)

    (* HIGH-FREQUENCY SPINDLE MOTORS & ACOUSTIC EMISSION SENSORS [rpm, A, N*m, dB] *)
    rSpindle1SpeedFeedback_rpm      : REAL;     (* Spindle 1 synchronous rotational speed feedback [rpm] *)
    rSpindle2SpeedFeedback_rpm      : REAL;     (* Spindle 2 synchronous rotational speed feedback [rpm] *)
    rSpindle1Current_A              : REAL;     (* Spindle 1 inverter motor phase current [A] *)
    rSpindle2Current_A              : REAL;     (* Spindle 2 inverter motor phase current [A] *)
    rSpindle1Torque_Nm              : REAL;     (* Spindle 1 electromagnetic cutting torque [N*m] *)
    rSpindle2Torque_Nm              : REAL;     (* Spindle 2 electromagnetic cutting torque [N*m] *)
    rSpindle1AcousticEmission_dB    : REAL;     (* Spindle 1 blade AE sensor RMS signal [dB] *)
    rSpindle2AcousticEmission_dB    : REAL;     (* Spindle 2 blade AE sensor RMS signal [dB] *)

    (* LINEAR FEED & ROTARY AXIS ENCODERS [mm, mm/s, deg] *)
    rXAxisPosition_mm               : REAL;     (* X-feed coreless linear motor laser scale position [mm] *)
    rXAxisVelocity_mms              : REAL;     (* X-feed linear motor actual velocity feedback [mm/s] *)
    rY1IndexPosition_mm             : REAL;     (* Spindle 1 Y-axis high-resolution index position [mm] *)
    rY2IndexPosition_mm             : REAL;     (* Spindle 2 Y-axis high-resolution index position [mm] *)
    rZ1StepPosition_mm              : REAL;     (* Spindle 1 Z-axis depth position feedback [mm] *)
    rZ2FullPosition_mm              : REAL;     (* Spindle 2 Z-axis depth position feedback [mm] *)
    rThetaAngle_deg                 : REAL;     (* Porous chuck rotary Theta axis angle [deg] *)

    (* NON-CONTACT OPTICAL SETUP SENSORS FOR BLADE APEX [um] *)
    rBlade1SetupApex_um             : REAL;     (* Non-contact laser setup sensor Blade 1 outer apex [um] *)
    rBlade2SetupApex_um             : REAL;     (* Non-contact laser setup sensor Blade 2 outer apex [um] *)

    (* IN-LINE AOI OPTICAL KERF 1 METROLOGY (2oo3 TRIPLE CAMERA BANK) [um] *)
    rKerf1Width_A_um                : REAL;     (* AOI Camera A Step-Cut Kerf 1 cut width [um] *)
    rKerf1Width_B_um                : REAL;     (* AOI Camera B Step-Cut Kerf 1 cut width [um] *)
    rKerf1Width_C_um                : REAL;     (* AOI Camera C Step-Cut Kerf 1 cut width [um] *)

    (* IN-LINE AOI OPTICAL KERF 2 METROLOGY (2oo3 TRIPLE CAMERA BANK) [um] *)
    rKerf2Width_A_um                : REAL;     (* AOI Camera A Full-Cut Kerf 2 cut width [um] *)
    rKerf2Width_B_um                : REAL;     (* AOI Camera B Full-Cut Kerf 2 cut width [um] *)
    rKerf2Width_C_um                : REAL;     (* AOI Camera C Full-Cut Kerf 2 cut width [um] *)

    (* IN-LINE AOI SILICON DEFECT METROLOGY & STREET ALIGNMENT [um, urad] *)
    rTopChippingSize_um             : REAL;     (* Maximum detected silicon top surface chipping size [um] *)
    rBacksideChippingSize_um        : REAL;     (* Maximum detected silicon backside chipping size [um] *)
    rStreetOffsetX_um               : REAL;     (* Street alignment offset Delta X [um] *)
    rStreetOffsetY_um               : REAL;     (* Street alignment offset Delta Y [um] *)
    rStreetOffsetTheta_urad         : REAL;     (* Street alignment angular error Delta Theta [urad] *)

    (* RECIPE & GEOMETRIC PROCESS PARAMETERS [mm, um, mm/s, MOhm*cm, bar, dB] *)
    rWaferDiameter_mm               : REAL;     (* Silicon wafer outer diameter [mm] *)
    rWaferThickness_um              : REAL;     (* Wafer nominal silicon substrate thickness [um] *)
    rDicingTapeThickness_um         : REAL;     (* Dicing tape carrier substrate thickness [um] *)
    rTargetTapePenetration_um       : REAL;     (* Commanded cut penetration into dicing tape [um] *)
    rStepCutDepth_um                : REAL;     (* Commanded depth of cut for Step Spindle 1 [um] *)
    rStreetPitch_mm                 : REAL;     (* Die street stepping pitch index [mm] *)
    rNominalFeedrate_mms            : REAL;     (* Baseline recipe cutting feedrate [mm/s] *)
    rNominalKerfWidth_um            : REAL;     (* Nominal target kerf cut width setpoint [um] *)
    rMaxAllowableKerfDev_um         : REAL;     (* Maximum allowable kerf deviation tolerance [um] *)
    rMaxAllowableChipping_um        : REAL;     (* Maximum allowable silicon chipping limit [um] *)
    rMinDiwResistivity_MOhm_cm      : REAL;     (* Minimum allowable DIW resistivity threshold [MOhm*cm] *)
    rMinAirBearingPress_bar         : REAL;     (* Minimum safe aerostatic air bearing pressure [bar] *)
    rMaxAcousticTrip_dB             : REAL;     (* Emergency blade breakage acoustic emission trip [dB] *)
END_VAR
"""

print("Header and VAR_INPUT defined.")
def build_var_output_and_var():
    return """VAR_OUTPUT
    (* DIGITAL SYSTEM HEALTH, STATUS & CRITICAL INTERLOCKS *)
    bSystemRunning                  : BOOL;     (* Auto sequence active and executing *)
    bSystemReady                    : BOOL;     (* All safety permissives and wafer ready *)
    bSystemTripped                  : BOOL;     (* Master emergency safety shutdown latched *)
    bCycleActive                    : BOOL;     (* Dicing cut pass in active progress *)
    bCyclePaused                    : BOOL;     (* Sequence temporarily halted by operator *)
    bAoiPass                        : BOOL;     (* In-line AOI inspection pass on latest street *)
    bAoiFailChipping                : BOOL;     (* Silicon chipping defect exceeded tolerance *)
    bAoiFailKerfWidth               : BOOL;     (* Kerf cut width outside tolerance band *)
    bBlade1BreakageDetected         : BOOL;     (* Spindle 1 blade micro-fracture or burst detected *)
    bBlade2BreakageDetected         : BOOL;     (* Spindle 2 blade micro-fracture or burst detected *)
    bBlade1WearLimitReached         : BOOL;     (* Blade 1 outer diameter worn to flange limit *)
    bBlade2WearLimitReached         : BOOL;     (* Blade 2 outer diameter worn to flange limit *)
    bBlade1GlazeWarning             : BOOL;     (* Blade 1 diamond binder glazed, dressing required *)
    bBlade2GlazeWarning             : BOOL;     (* Blade 2 diamond binder glazed, dressing required *)
    bTapeCutThroughAlarm            : BOOL;     (* Dicing tape penetration exceeded 35.0 um limit *)
    bDegradedSensorMode             : BOOL;     (* At least one 2oo3 sensor bank in 1oo2/1oo1 mode *)
    bMpcActive                      : BOOL;     (* Receding-horizon MPC actively modulating feed *)

    (* ANALOG ACTUATOR & SPEED DEMANDS [rpm, mm/s, mm, deg, L/min, bar] *)
    rSpindle1SpeedDemand_rpm        : REAL;     (* Modulated speed setpoint to Spindle 1 inverter [rpm] *)
    rSpindle2SpeedDemand_rpm        : REAL;     (* Modulated speed setpoint to Spindle 2 inverter [rpm] *)
    rXFeedVelocityDemand_mms        : REAL;     (* Closed-loop feedrate demand to X-axis linear motor [mm/s] *)
    rY1IndexDemand_mm               : REAL;     (* Spindle 1 Y-axis positioning demand [mm] *)
    rY2IndexDemand_mm               : REAL;     (* Spindle 2 Y-axis positioning demand [mm] *)
    rZ1StepCutDemand_mm             : REAL;     (* Spindle 1 Z-axis step-cut depth position demand [mm] *)
    rZ2FullCutDemand_mm             : REAL;     (* Spindle 2 Z-axis full-cut depth position demand [mm] *)
    rThetaDemand_deg                : REAL;     (* Chuck table Theta rotary axis position demand [deg] *)
    rDiwFlowDemand_Lmin             : REAL;     (* Demanded flow rate to DIW supply manifold [L/min] *)
    rDiwPressureDemand_bar          : REAL;     (* Demanded delivery pressure to DIW booster pump [bar] *)
    rSpinnerWashSpeed_rpm           : REAL;     (* Centrifugal spinner wash station rotational speed [rpm] *)
    rAirKnifePressure_bar           : REAL;     (* Deionized air knife drying delivery pressure [bar] *)

    (* VOTED PROCESS ESTIMATES & 2oo3 SYNTHESIZED SIGNALS [bar, mbar, L/min, um] *)
    rVotedAirBearingPress1_bar      : REAL;     (* 2oo3 median voted Spindle 1 air bearing pressure [bar] *)
    rVotedAirBearingPress2_bar      : REAL;     (* 2oo3 median voted Spindle 2 air bearing pressure [bar] *)
    rVotedChuckVacuum_mbar          : REAL;     (* 2oo3 median voted vacuum chuck pressure [mbar] *)
    rVotedDiwFlow_Lmin              : REAL;     (* 2oo3 median voted DIW cooling water flow rate [L/min] *)
    rVotedKerf1Width_um             : REAL;     (* 2oo3 median voted Step Kerf 1 cut width [um] *)
    rVotedKerf2Width_um             : REAL;     (* 2oo3 median voted Full Kerf 2 cut width [um] *)

    (* ROTODYNAMIC, WEAR TRACKING & METROLOGY DERIVATIVES [um, m, N/um, N] *)
    rCalculatedBlade1Wear_um        : REAL;     (* Cumulative Blade 1 diamond outer diameter wear loss [um] *)
    rCalculatedBlade2Wear_um        : REAL;     (* Cumulative Blade 2 diamond outer diameter wear loss [um] *)
    rCumulativeCutDistance1_m       : REAL;     (* Integrated total linear cut travel distance Blade 1 [m] *)
    rCumulativeCutDistance2_m       : REAL;     (* Integrated total linear cut travel distance Blade 2 [m] *)
    rEffectiveZ1Depth_um            : REAL;     (* Wear-compensated actual Z1 step-cut silicon depth [um] *)
    rEffectiveZ2Depth_um            : REAL;     (* Wear-compensated actual Z2 dicing tape penetration [um] *)
    rBlade1AeroStiffness_N_um       : REAL;     (* Spindle 1 dynamic aerostatic squeeze film stiffness [N/um] *)
    rBlade2AeroStiffness_N_um       : REAL;     (* Spindle 2 dynamic aerostatic squeeze film stiffness [N/um] *)
    rEstimatedCuttingForce1_N       : REAL;     (* Estimated tangential micro-grinding force Blade 1 [N] *)
    rEstimatedCuttingForce2_N       : REAL;     (* Estimated tangential micro-grinding force Blade 2 [N] *)
    rKerfWanderOffset_um            : REAL;     (* Lateral kerf wandering offset from street centerline [um] *)

    (* COMPREHENSIVE BIT-PACKED STATUS & ALARM WORDS (ISA-18.2 COMPLIANT) *)
    dwSystemStatusWord              : DWORD;    (* Bit-packed system operational status word *)
    dwAlarmWord1                    : DWORD;    (* Bit-packed emergency safety trips (air loss, breakage) *)
    dwAlarmWord2                    : DWORD;    (* Bit-packed process trips (tape breach, DIW resistivity) *)
    dwWarningWord                   : DWORD;    (* Bit-packed operational advisory warnings *)
    dwDegradationWord               : DWORD;    (* Bit-packed 2oo3 sensor health degradation flags *)
    dwAoiInspectionWord             : DWORD;    (* Bit-packed in-line AOI quality classification flags *)
END_VAR

VAR
    (* FINITE STATE MACHINE (FSM) STEP REGISTERS & PROCESS INDICES *)
    iState                          : INT := 0; (* Main supervisory state register *)
    iSubState                       : INT := 0; (* Secondary substep execution register *)
    iPrevState                      : INT := 0; (* History state register for transitions *)
    iCurrentStreet                  : INT := 0; (* Current cutting street index counter *)
    iTotalStreetsX                  : INT := 60;(* Total streets planned along X orientation *)
    iTotalStreetsY                  : INT := 60;(* Total streets planned along Y orientation *)
    bCrossStreetRotated             : BOOL := FALSE; (* Flag: 90-degree rotary cross-street completed *)

    (* INDUSTRIAL TIMER INSTANCES (IEC 61131-3 STANDARD TON) *)
    tStateTimer                     : TON;      (* Primary state dwell timer *)
    tCassetteInfeedTimer            : TON;      (* Cassette robot loader synchronization timer *)
    tVacuumChuckTimer               : TON;      (* Chuck table vacuum stabilization timer *)
    tThetaAlignTimer                : TON;      (* Pattern recognition Theta alignment timer *)
    tBladeSetupTimer                : TON;      (* Non-contact optical setup sensor dwell timer *)
    tDiwPrimeTimer                  : TON;      (* DIW high-pressure coolant purge and prime timer *)
    tCutPassTimer                   : TON;      (* Active wafer dicing cut pass timeout timer *)
    tAoiScanTimer                   : TON;      (* Line-scan optical AOI inspection scan timer *)
    tSpinnerWashTimer               : TON;      (* Centrifugal DIW wafer spinner wash timer *)
    tAirKnifeDryTimer               : TON;      (* High-pressure N2 / air knife drying timer *)
    tUnloadTimer                    : TON;      (* Finished wafer unloader magazine transfer timer *)
    tDressingTimer                  : TON;      (* SiC dressing board abrasive regeneration timer *)
    tEmergencyStopTimer             : TON;      (* Safety clamp and dynamic brake hold timer *)
    tDiscrepancyTimer_Air1          : TON;      (* Spindle 1 air bearing pressure discrepancy debounce *)
    tDiscrepancyTimer_Air2          : TON;      (* Spindle 2 air bearing pressure discrepancy debounce *)
    tDiscrepancyTimer_Vac           : TON;      (* Chuck vacuum discrepancy debounce timer *)
    tDiscrepancyTimer_Diw           : TON;      (* DIW flow discrepancy debounce timer *)
    tDiscrepancyTimer_Kerf1         : TON;      (* Kerf 1 optical measurement discrepancy debounce *)
    tDiscrepancyTimer_Kerf2         : TON;      (* Kerf 2 optical measurement discrepancy debounce *)
    tMpcExecutionTimer              : TON;      (* Periodic receding-horizon MPC scheduler timer *)

    (* 2oo3 TRIPLE MODULAR REDUNDANCY INTERNAL DISCREPANCY & HEALTH FLAGS *)
    (* Bank 1: Spindle 1 Air Bearing Pressure *)
    rDev_Air1_AB                    : REAL := 0.0;
    rDev_Air1_BC                    : REAL := 0.0;
    rDev_Air1_CA                    : REAL := 0.0;
    bAir1_A_Ok                      : BOOL := TRUE;
    bAir1_B_Ok                      : BOOL := TRUE;
    bAir1_C_Ok                      : BOOL := TRUE;
    bAir1_Degraded_1oo2             : BOOL := FALSE;
    bAir1_Trip                      : BOOL := FALSE;

    (* Bank 2: Spindle 2 Air Bearing Pressure *)
    rDev_Air2_AB                    : REAL := 0.0;
    rDev_Air2_BC                    : REAL := 0.0;
    rDev_Air2_CA                    : REAL := 0.0;
    bAir2_A_Ok                      : BOOL := TRUE;
    bAir2_B_Ok                      : BOOL := TRUE;
    bAir2_C_Ok                      : BOOL := TRUE;
    bAir2_Degraded_1oo2             : BOOL := FALSE;
    bAir2_Trip                      : BOOL := FALSE;

    (* Bank 3: Vacuum Chuck Table Pressure *)
    rDev_Vac_AB                     : REAL := 0.0;
    rDev_Vac_BC                     : REAL := 0.0;
    rDev_Vac_CA                     : REAL := 0.0;
    bVac_A_Ok                       : BOOL := TRUE;
    bVac_B_Ok                       : BOOL := TRUE;
    bVac_C_Ok                       : BOOL := TRUE;
    bVac_Degraded_1oo2              : BOOL := FALSE;
    bVac_Trip                       : BOOL := FALSE;

    (* Bank 4: DIW Cooling Water Flow *)
    rDev_Diw_AB                     : REAL := 0.0;
    rDev_Diw_BC                     : REAL := 0.0;
    rDev_Diw_CA                     : REAL := 0.0;
    bDiw_A_Ok                       : BOOL := TRUE;
    bDiw_B_Ok                       : BOOL := TRUE;
    bDiw_C_Ok                       : BOOL := TRUE;
    bDiw_Degraded_1oo2              : BOOL := FALSE;
    bDiw_Trip                       : BOOL := FALSE;

    (* Bank 5: In-Line Kerf 1 Optical Metrology *)
    rDev_Kerf1_AB                   : REAL := 0.0;
    rDev_Kerf1_BC                   : REAL := 0.0;
    rDev_Kerf1_CA                   : REAL := 0.0;
    bKerf1_A_Ok                     : BOOL := TRUE;
    bKerf1_B_Ok                     : BOOL := TRUE;
    bKerf1_C_Ok                     : BOOL := TRUE;
    bKerf1_Degraded_1oo2            : BOOL := FALSE;

    (* Bank 6: In-Line Kerf 2 Optical Metrology *)
    rDev_Kerf2_AB                   : REAL := 0.0;
    rDev_Kerf2_BC                   : REAL := 0.0;
    rDev_Kerf2_CA                   : REAL := 0.0;
    bKerf2_A_Ok                     : BOOL := TRUE;
    bKerf2_B_Ok                     : BOOL := TRUE;
    bKerf2_C_Ok                     : BOOL := TRUE;
    bKerf2_Degraded_1oo2            : BOOL := FALSE;

    (* PHYSICAL PARAMETERS & DIAMOND WEAR INTEGRATION CONSTANTS *)
    c_DiamondWearCoeff1             : REAL := 0.000045; (* Blade 1 wear rate [um/(N*m)] *)
    c_DiamondWearCoeff2             : REAL := 0.000052; (* Blade 2 wear rate [um/(N*m)] *)
    c_SiliconFractureToughness      : REAL := 0.95;     (* Silicon K_Ic [MPa*m^0.5] *)
    c_SiliconHardness               : REAL := 11.5;     (* Silicon Vickers hardness [GPa] *)
    c_SiliconYoungsModulus          : REAL := 169.0;    (* Silicon elastic modulus [GPa] *)
    c_SpecificGrindingEnergy        : REAL := 8.5;      (* Silicon specific energy [J/mm^3] *)
    c_SpindleTorqueConstant_kt      : REAL := 0.045;    (* Spindle PMAC motor torque constant [N*m/A] *)
    c_LinearMotorForceConstant_kf   : REAL := 65.0;     (* X-axis linear motor force constant [N/A] *)
    c_NominalBlade1Diameter_mm      : REAL := 56.000;   (* Brand-new Blade 1 outer diameter [mm] *)
    c_NominalBlade2Diameter_mm      : REAL := 56.000;   (* Brand-new Blade 2 outer diameter [mm] *)
    c_FlangeSafetyDiameter_mm       : REAL := 53.000;   (* Minimum allowable blade diameter before hub [mm] *)
    c_MaxTapePenetration_um         : REAL := 35.0;     (* Hard limit for tape penetration [um] *)
    c_NominalAirBearingClearance_um : REAL := 8.5;      (* Aerostatic journal air gap clearance [um] *)

    (* 16x16 DISCRETE STATE-SPACE MATRICES & MPC OPTIMIZATION REGISTERS *)
    A_mat                           : ARRAY[1..16, 1..16] OF REAL; (* Discrete state transition matrix (16x16) *)
    B_mat                           : ARRAY[1..16, 1..8] OF REAL;  (* Discrete control input matrix (16x8) *)
    C_mat                           : ARRAY[1..16, 1..16] OF REAL; (* Discrete output observation matrix (16x16) *)
    D_mat                           : ARRAY[1..16, 1..8] OF REAL;  (* Direct feedthrough transmission matrix (16x8) *)

    x_state                         : ARRAY[1..16] OF REAL;        (* Current estimated plant state vector *)
    x_pred                          : ARRAY[1..16] OF REAL;        (* One-step-ahead predicted state vector *)
    x_ref                           : ARRAY[1..16] OF REAL;        (* Target reference trajectory vector *)
    x_err                           : ARRAY[1..16] OF REAL;        (* Tracking error residual vector (x - x_ref) *)

    u_mpc                           : ARRAY[1..8] OF REAL;         (* Active MPC commanded control input vector *)
    u_delta                         : ARRAY[1..8] OF REAL;         (* Computed control optimization increment *)
    u_prev                          : ARRAY[1..8] OF REAL;         (* Previous scan control input vector *)

    Q_diag                          : ARRAY[1..16] OF REAL;        (* State tracking penalty weight diagonal *)
    R_diag                          : ARRAY[1..8] OF REAL;         (* Control rate variation suppression weight *)
    P_diag                          : ARRAY[1..16] OF REAL;        (* Terminal state constraint penalty weight *)
    grad_J                          : ARRAY[1..8] OF REAL;         (* Quadratic cost gradient vector *)
    H_diag                          : ARRAY[1..8] OF REAL;         (* Hessian diagonal approximation vector *)

    iRow                            : INT := 1;                    (* Matrix row traversal index *)
    iCol                            : INT := 1;                    (* Matrix column traversal index *)
    iIter                           : INT := 1;                    (* MPC gradient optimization loop index *)
    kInput                          : INT := 1;                    (* Input vector traversal index *)
    rCostValue                      : REAL := 0.0;                 (* Evaluated quadratic performance index J *)
    rStepSize                       : REAL := 0.015;               (* Gradient descent search step coefficient *)
    rPredSum                        : REAL := 0.0;                 (* Inner product summation accumulator *)
    bMatricesInitialized            : BOOL := FALSE;               (* Cold-start matrix initialization latch *)

    (* WEAR TRACKING, APEX OFFSETS & TAPE INTERLOCK WORKING VARIABLES *)
    rBlade1DeltaWear_um             : REAL := 0.0;                 (* Blade 1 diameter attrition from setup [um] *)
    rBlade2DeltaWear_um             : REAL := 0.0;                 (* Blade 2 diameter attrition from setup [um] *)
    rBlade1Exposure_um              : REAL := 1500.0;              (* Usable blade exposure protruding from flange [um] *)
    rBlade2Exposure_um              : REAL := 1500.0;              (* Usable blade exposure protruding from flange [um] *)
    rCalculatedZ1Apex_mm            : REAL := 0.0;                 (* Actual physical cutting apex position Z1 [mm] *)
    rCalculatedZ2Apex_mm            : REAL := 0.0;                 (* Actual physical cutting apex position Z2 [mm] *)
    rChuckDatumZ_mm                 : REAL := 0.0;                 (* Porous ceramic chuck top reference datum [mm] *)
    rTapePenetrationActual_um       : REAL := 20.0;                (* Real-time calculated penetration into tape [um] *)
    rGlazeMetricBlade1              : REAL := 0.0;                 (* Current-to-feedrate ratio for glaze detection *)
    rGlazeMetricBlade2              : REAL := 0.0;                 (* Current-to-feedrate ratio for glaze detection *)
    rCutPassLength_m                : REAL := 0.320;               (* Length of single cutting stroke [m] *)

    (* ACOUSTIC EMISSION FAST BREAKAGE & LOAD TRANSIENT REGISTERS *)
    rPrevSpindle1Current_A          : REAL := 0.0;                 (* Spindle 1 current previous scan history [A] *)
    rPrevSpindle2Current_A          : REAL := 0.0;                 (* Spindle 2 current previous scan history [A] *)
    rSpindle1CurrentDeriv_As        : REAL := 0.0;                 (* Time derivative of Spindle 1 current [A/s] *)
    rSpindle2CurrentDeriv_As        : REAL := 0.0;                 (* Time derivative of Spindle 2 current [A/s] *)
    rAeFiltered1_dB                 : REAL := 45.0;                (* Low-pass filtered AE signal Spindle 1 [dB] *)
    rAeFiltered2_dB                 : REAL := 45.0;                (* Low-pass filtered AE signal Spindle 2 [dB] *)
    rAeSpikeHold1_dB                : REAL := 0.0;                 (* Fast peak-hold AE amplitude register 1 [dB] *)
    rAeSpikeHold2_dB                : REAL := 0.0;                 (* Fast peak-hold AE amplitude register 2 [dB] *)

    (* IN-LINE AOI IMAGE METROLOGY & COORDINATE CONVERSION REGISTERS *)
    rKerf1Deviation_um              : REAL := 0.0;                 (* Kerf 1 cut width minus nominal setpoint [um] *)
    rKerf2Deviation_um              : REAL := 0.0;                 (* Kerf 2 cut width minus nominal setpoint [um] *)
    rResidualTheta_urad             : REAL := 0.0;                 (* Residual angular alignment error [urad] *)
    rThetaCorrected_deg             : REAL := 0.0;                 (* Coordinated Theta angle setpoint [deg] *)
    bStreetAligned                  : BOOL := FALSE;               (* Street alignment lock confirmation *)
    bKerfWidthOk                    : BOOL := TRUE;                (* Kerf width within tolerance flag *)
    bChippingOk                     : BOOL := TRUE;                (* Chipping within tolerance flag *)

    (* SCAN CYCLE TIMING & SLEW-RATE LIMITING ACCUMULATORS *)
    rCycleTime_sec                  : REAL := 0.010;               (* Deterministic task scan duration (10 ms) *)
    rXFeedDemandInternal_mms        : REAL := 0.0;                 (* Rate-limited X-feed velocity setpoint [mm/s] *)
    rSpindle1SpeedInternal_rpm      : REAL := 0.0;                 (* Slew-limited Spindle 1 speed setpoint [rpm] *)
    rSpindle2SpeedInternal_rpm      : REAL := 0.0;                 (* Slew-limited Spindle 2 speed setpoint [rpm] *)
    rDiwFlowInternal_Lmin           : REAL := 0.0;                 (* Rate-limited DIW flow setpoint [L/min] *)
    rCompensatedResistivity_MOhm    : REAL := 18.2;                (* Temperature-corrected DIW resistivity [MOhm*cm] *)
END_VAR
"""

print("VAR_OUTPUT and VAR appended.")
def build_phase1_tmr_voting():
    return """(* ==================================================================================================== *)
(* PHASE 1: TRIPLE MODULAR REDUNDANCY (2oo3) SENSOR VOTING & DISCREPANCY ARBITRATION                   *)
(* ==================================================================================================== *)
(* Deterministic median selection with cross-channel deviation checking across 5 critical sensor banks. *)
(* Gracefully degrades from 2oo3 to 1oo2, and finally to 1oo1 fail-safe before latching a channel trip.  *)

dwDegradationWord := 16#0000_0000;
bDegradedSensorMode := FALSE;

(* ---------------------------------------------------------------------------------------------------- *)
(* 1.1 SPINDLE 1 AEROSTATIC AIR BEARING PRESSURE (PT-11A, PT-11B, PT-11C) [bar]                        *)
(* ---------------------------------------------------------------------------------------------------- *)
rDev_Air1_AB := ABS(rSpindle1AirPress_A_bar - rSpindle1AirPress_B_bar);
rDev_Air1_BC := ABS(rSpindle1AirPress_B_bar - rSpindle1AirPress_C_bar);
rDev_Air1_CA := ABS(rSpindle1AirPress_C_bar - rSpindle1AirPress_A_bar);

bAir1_A_Ok := (rSpindle1AirPress_A_bar >= 3.5) AND (rSpindle1AirPress_A_bar <= 9.0);
bAir1_B_Ok := (rSpindle1AirPress_B_bar >= 3.5) AND (rSpindle1AirPress_B_bar <= 9.0);
bAir1_C_Ok := (rSpindle1AirPress_C_bar >= 3.5) AND (rSpindle1AirPress_C_bar <= 9.0);

IF bAir1_A_Ok AND bAir1_B_Ok AND bAir1_C_Ok THEN
    bAir1_Degraded_1oo2 := FALSE;
    bAir1_Trip := FALSE;
    (* 2oo3 Median Selection *)
    IF ((rSpindle1AirPress_A_bar >= rSpindle1AirPress_B_bar) AND (rSpindle1AirPress_A_bar <= rSpindle1AirPress_C_bar)) OR
       ((rSpindle1AirPress_A_bar >= rSpindle1AirPress_C_bar) AND (rSpindle1AirPress_A_bar <= rSpindle1AirPress_B_bar)) THEN
        rVotedAirBearingPress1_bar := rSpindle1AirPress_A_bar;
    ELSIF ((rSpindle1AirPress_B_bar >= rSpindle1AirPress_A_bar) AND (rSpindle1AirPress_B_bar <= rSpindle1AirPress_C_bar)) OR
          ((rSpindle1AirPress_B_bar >= rSpindle1AirPress_C_bar) AND (rSpindle1AirPress_B_bar <= rSpindle1AirPress_A_bar)) THEN
        rVotedAirBearingPress1_bar := rSpindle1AirPress_B_bar;
    ELSE
        rVotedAirBearingPress1_bar := rSpindle1AirPress_C_bar;
    END_IF;
    
    (* Discrepancy Debounce Evaluation (threshold: 0.40 bar) *)
    tDiscrepancyTimer_Air1(IN := (rDev_Air1_AB > 0.40) OR (rDev_Air1_BC > 0.40) OR (rDev_Air1_CA > 0.40), PT := T#250MS);
    IF tDiscrepancyTimer_Air1.Q THEN
        dwDegradationWord := dwDegradationWord OR 16#0000_0001; (* Bit 0: Spindle 1 Air Discrepancy Warning *)
    END_IF;
ELSIF bAir1_A_Ok AND bAir1_B_Ok THEN
    bAir1_Degraded_1oo2 := TRUE;
    bDegradedSensorMode := TRUE;
    rVotedAirBearingPress1_bar := (rSpindle1AirPress_A_bar + rSpindle1AirPress_B_bar) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0000_0002; (* Bit 1: Spindle 1 Air Degraded to 1oo2 (C Failed) *)
ELSIF bAir1_B_Ok AND bAir1_C_Ok THEN
    bAir1_Degraded_1oo2 := TRUE;
    bDegradedSensorMode := TRUE;
    rVotedAirBearingPress1_bar := (rSpindle1AirPress_B_bar + rSpindle1AirPress_C_bar) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0000_0004; (* Bit 2: Spindle 1 Air Degraded to 1oo2 (A Failed) *)
ELSIF bAir1_A_Ok AND bAir1_C_Ok THEN
    bAir1_Degraded_1oo2 := TRUE;
    bDegradedSensorMode := TRUE;
    rVotedAirBearingPress1_bar := (rSpindle1AirPress_A_bar + rSpindle1AirPress_C_bar) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0000_0008; (* Bit 3: Spindle 1 Air Degraded to 1oo2 (B Failed) *)
ELSIF bAir1_A_Ok THEN
    bDegradedSensorMode := TRUE;
    rVotedAirBearingPress1_bar := rSpindle1AirPress_A_bar;
    dwDegradationWord := dwDegradationWord OR 16#0000_0010; (* Bit 4: Spindle 1 Air 1oo1 Mode (B, C Failed) *)
ELSIF bAir1_B_Ok THEN
    bDegradedSensorMode := TRUE;
    rVotedAirBearingPress1_bar := rSpindle1AirPress_B_bar;
    dwDegradationWord := dwDegradationWord OR 16#0000_0020; (* Bit 5: Spindle 1 Air 1oo1 Mode (A, C Failed) *)
ELSIF bAir1_C_Ok THEN
    bDegradedSensorMode := TRUE;
    rVotedAirBearingPress1_bar := rSpindle1AirPress_C_bar;
    dwDegradationWord := dwDegradationWord OR 16#0000_0040; (* Bit 6: Spindle 1 Air 1oo1 Mode (A, B Failed) *)
ELSE
    bAir1_Trip := TRUE;
    rVotedAirBearingPress1_bar := 0.0;
    dwDegradationWord := dwDegradationWord OR 16#0000_0080; (* Bit 7: Spindle 1 Air Tripped - All Sensors Dead *)
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* 1.2 SPINDLE 2 AEROSTATIC AIR BEARING PRESSURE (PT-12A, PT-12B, PT-12C) [bar]                        *)
(* ---------------------------------------------------------------------------------------------------- *)
rDev_Air2_AB := ABS(rSpindle2AirPress_A_bar - rSpindle2AirPress_B_bar);
rDev_Air2_BC := ABS(rSpindle2AirPress_B_bar - rSpindle2AirPress_C_bar);
rDev_Air2_CA := ABS(rSpindle2AirPress_C_bar - rSpindle2AirPress_A_bar);

bAir2_A_Ok := (rSpindle2AirPress_A_bar >= 3.5) AND (rSpindle2AirPress_A_bar <= 9.0);
bAir2_B_Ok := (rSpindle2AirPress_B_bar >= 3.5) AND (rSpindle2AirPress_B_bar <= 9.0);
bAir2_C_Ok := (rSpindle2AirPress_C_bar >= 3.5) AND (rSpindle2AirPress_C_bar <= 9.0);

IF bAir2_A_Ok AND bAir2_B_Ok AND bAir2_C_Ok THEN
    bAir2_Degraded_1oo2 := FALSE;
    bAir2_Trip := FALSE;
    (* 2oo3 Median Selection *)
    IF ((rSpindle2AirPress_A_bar >= rSpindle2AirPress_B_bar) AND (rSpindle2AirPress_A_bar <= rSpindle2AirPress_C_bar)) OR
       ((rSpindle2AirPress_A_bar >= rSpindle2AirPress_C_bar) AND (rSpindle2AirPress_A_bar <= rSpindle2AirPress_B_bar)) THEN
        rVotedAirBearingPress2_bar := rSpindle2AirPress_A_bar;
    ELSIF ((rSpindle2AirPress_B_bar >= rSpindle2AirPress_A_bar) AND (rSpindle2AirPress_B_bar <= rSpindle2AirPress_C_bar)) OR
          ((rSpindle2AirPress_B_bar >= rSpindle2AirPress_C_bar) AND (rSpindle2AirPress_B_bar <= rSpindle2AirPress_A_bar)) THEN
        rVotedAirBearingPress2_bar := rSpindle2AirPress_B_bar;
    ELSE
        rVotedAirBearingPress2_bar := rSpindle2AirPress_C_bar;
    END_IF;
    
    (* Discrepancy Debounce Evaluation (threshold: 0.40 bar) *)
    tDiscrepancyTimer_Air2(IN := (rDev_Air2_AB > 0.40) OR (rDev_Air2_BC > 0.40) OR (rDev_Air2_CA > 0.40), PT := T#250MS);
    IF tDiscrepancyTimer_Air2.Q THEN
        dwDegradationWord := dwDegradationWord OR 16#0000_0100; (* Bit 8: Spindle 2 Air Discrepancy Warning *)
    END_IF;
ELSIF bAir2_A_Ok AND bAir2_B_Ok THEN
    bAir2_Degraded_1oo2 := TRUE;
    bDegradedSensorMode := TRUE;
    rVotedAirBearingPress2_bar := (rSpindle2AirPress_A_bar + rSpindle2AirPress_B_bar) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0000_0200; (* Bit 9: Spindle 2 Air Degraded to 1oo2 (C Failed) *)
ELSIF bAir2_B_Ok AND bAir2_C_Ok THEN
    bAir2_Degraded_1oo2 := TRUE;
    bDegradedSensorMode := TRUE;
    rVotedAirBearingPress2_bar := (rSpindle2AirPress_B_bar + rSpindle2AirPress_C_bar) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0000_0400; (* Bit 10: Spindle 2 Air Degraded to 1oo2 (A Failed) *)
ELSIF bAir2_A_Ok AND bAir2_C_Ok THEN
    bAir2_Degraded_1oo2 := TRUE;
    bDegradedSensorMode := TRUE;
    rVotedAirBearingPress2_bar := (rSpindle2AirPress_A_bar + rSpindle2AirPress_C_bar) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0000_0800; (* Bit 11: Spindle 2 Air Degraded to 1oo2 (B Failed) *)
ELSIF bAir2_A_Ok THEN
    bDegradedSensorMode := TRUE;
    rVotedAirBearingPress2_bar := rSpindle2AirPress_A_bar;
    dwDegradationWord := dwDegradationWord OR 16#0000_1000; (* Bit 12: Spindle 2 Air 1oo1 Mode (B, C Failed) *)
ELSIF bAir2_B_Ok THEN
    bDegradedSensorMode := TRUE;
    rVotedAirBearingPress2_bar := rSpindle2AirPress_B_bar;
    dwDegradationWord := dwDegradationWord OR 16#0000_2000; (* Bit 13: Spindle 2 Air 1oo1 Mode (A, C Failed) *)
ELSIF bAir2_C_Ok THEN
    bDegradedSensorMode := TRUE;
    rVotedAirBearingPress2_bar := rSpindle2AirPress_C_bar;
    dwDegradationWord := dwDegradationWord OR 16#0000_4000; (* Bit 14: Spindle 2 Air 1oo1 Mode (A, B Failed) *)
ELSE
    bAir2_Trip := TRUE;
    rVotedAirBearingPress2_bar := 0.0;
    dwDegradationWord := dwDegradationWord OR 16#0000_8000; (* Bit 15: Spindle 2 Air Tripped - All Sensors Dead *)
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* 1.3 POROUS CERAMIC VACUUM CHUCK PRESSURE (VT-21A, VT-21B, VT-21C) [mbar]                             *)
(* ---------------------------------------------------------------------------------------------------- *)
rDev_Vac_AB := ABS(rChuckVacuum_A_mbar - rChuckVacuum_B_mbar);
rDev_Vac_BC := ABS(rChuckVacuum_B_mbar - rChuckVacuum_C_mbar);
rDev_Vac_CA := ABS(rChuckVacuum_C_mbar - rChuckVacuum_A_mbar);

bVac_A_Ok := (rChuckVacuum_A_mbar >= -1013.0) AND (rChuckVacuum_A_mbar <= 50.0);
bVac_B_Ok := (rChuckVacuum_B_mbar >= -1013.0) AND (rChuckVacuum_B_mbar <= 50.0);
bVac_C_Ok := (rChuckVacuum_C_mbar >= -1013.0) AND (rChuckVacuum_C_mbar <= 50.0);

IF bVac_A_Ok AND bVac_B_Ok AND bVac_C_Ok THEN
    bVac_Degraded_1oo2 := FALSE;
    bVac_Trip := FALSE;
    (* 2oo3 Median Selection *)
    IF ((rChuckVacuum_A_mbar >= rChuckVacuum_B_mbar) AND (rChuckVacuum_A_mbar <= rChuckVacuum_C_mbar)) OR
       ((rChuckVacuum_A_mbar >= rChuckVacuum_C_mbar) AND (rChuckVacuum_A_mbar <= rChuckVacuum_B_mbar)) THEN
        rVotedChuckVacuum_mbar := rChuckVacuum_A_mbar;
    ELSIF ((rChuckVacuum_B_mbar >= rChuckVacuum_A_mbar) AND (rChuckVacuum_B_mbar <= rChuckVacuum_C_mbar)) OR
          ((rChuckVacuum_B_mbar >= rChuckVacuum_C_mbar) AND (rChuckVacuum_B_mbar <= rChuckVacuum_A_mbar)) THEN
        rVotedChuckVacuum_mbar := rChuckVacuum_B_mbar;
    ELSE
        rVotedChuckVacuum_mbar := rChuckVacuum_C_mbar;
    END_IF;
    
    (* Discrepancy Debounce (threshold: 45.0 mbar) *)
    tDiscrepancyTimer_Vac(IN := (rDev_Vac_AB > 45.0) OR (rDev_Vac_BC > 45.0) OR (rDev_Vac_CA > 45.0), PT := T#200MS);
    IF tDiscrepancyTimer_Vac.Q THEN
        dwDegradationWord := dwDegradationWord OR 16#0001_0000; (* Bit 16: Vacuum Transducer Deviation Alert *)
    END_IF;
ELSIF bVac_A_Ok AND bVac_B_Ok THEN
    bVac_Degraded_1oo2 := TRUE;
    bDegradedSensorMode := TRUE;
    rVotedChuckVacuum_mbar := (rChuckVacuum_A_mbar + rChuckVacuum_B_mbar) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0002_0000; (* Bit 17: Vacuum Degraded to 1oo2 (C Failed) *)
ELSIF bVac_B_Ok AND bVac_C_Ok THEN
    bVac_Degraded_1oo2 := TRUE;
    bDegradedSensorMode := TRUE;
    rVotedChuckVacuum_mbar := (rChuckVacuum_B_mbar + rChuckVacuum_C_mbar) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0004_0000; (* Bit 18: Vacuum Degraded to 1oo2 (A Failed) *)
ELSIF bVac_A_Ok AND bVac_C_Ok THEN
    bVac_Degraded_1oo2 := TRUE;
    bDegradedSensorMode := TRUE;
    rVotedChuckVacuum_mbar := (rChuckVacuum_A_mbar + rChuckVacuum_C_mbar) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0008_0000; (* Bit 19: Vacuum Degraded to 1oo2 (B Failed) *)
ELSIF bVac_A_Ok THEN
    bDegradedSensorMode := TRUE;
    rVotedChuckVacuum_mbar := rChuckVacuum_A_mbar;
    dwDegradationWord := dwDegradationWord OR 16#0010_0000; (* Bit 20: Vacuum 1oo1 Mode (B, C Failed) *)
ELSIF bVac_B_Ok THEN
    bDegradedSensorMode := TRUE;
    rVotedChuckVacuum_mbar := rChuckVacuum_B_mbar;
    dwDegradationWord := dwDegradationWord OR 16#0020_0000; (* Bit 21: Vacuum 1oo1 Mode (A, C Failed) *)
ELSIF bVac_C_Ok THEN
    bDegradedSensorMode := TRUE;
    rVotedChuckVacuum_mbar := rChuckVacuum_C_mbar;
    dwDegradationWord := dwDegradationWord OR 16#0040_0000; (* Bit 22: Vacuum 1oo1 Mode (A, B Failed) *)
ELSE
    bVac_Trip := TRUE;
    rVotedChuckVacuum_mbar := 0.0;
    dwDegradationWord := dwDegradationWord OR 16#0080_0000; (* Bit 23: Vacuum Transducer Total Failure *)
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* 1.4 DIW COOLING WATER FLOW RATE (FT-31A, FT-31B, FT-31C) [L/min]                                     *)
(* ---------------------------------------------------------------------------------------------------- *)
rDev_Diw_AB := ABS(rDiwCoolantFlow_A_Lmin - rDiwCoolantFlow_B_Lmin);
rDev_Diw_BC := ABS(rDiwCoolantFlow_B_Lmin - rDiwCoolantFlow_C_Lmin);
rDev_Diw_CA := ABS(rDiwCoolantFlow_C_Lmin - rDiwCoolantFlow_A_Lmin);

bDiw_A_Ok := (rDiwCoolantFlow_A_Lmin >= 0.0) AND (rDiwCoolantFlow_A_Lmin <= 20.0);
bDiw_B_Ok := (rDiwCoolantFlow_B_Lmin >= 0.0) AND (rDiwCoolantFlow_B_Lmin <= 20.0);
bDiw_C_Ok := (rDiwCoolantFlow_C_Lmin >= 0.0) AND (rDiwCoolantFlow_C_Lmin <= 20.0);

IF bDiw_A_Ok AND bDiw_B_Ok AND bDiw_C_Ok THEN
    bDiw_Degraded_1oo2 := FALSE;
    bDiw_Trip := FALSE;
    (* 2oo3 Median Selection *)
    IF ((rDiwCoolantFlow_A_Lmin >= rDiwCoolantFlow_B_Lmin) AND (rDiwCoolantFlow_A_Lmin <= rDiwCoolantFlow_C_Lmin)) OR
       ((rDiwCoolantFlow_A_Lmin >= rDiwCoolantFlow_C_Lmin) AND (rDiwCoolantFlow_A_Lmin <= rDiwCoolantFlow_B_Lmin)) THEN
        rVotedDiwFlow_Lmin := rDiwCoolantFlow_A_Lmin;
    ELSIF ((rDiwCoolantFlow_B_Lmin >= rDiwCoolantFlow_A_Lmin) AND (rDiwCoolantFlow_B_Lmin <= rDiwCoolantFlow_C_Lmin)) OR
          ((rDiwCoolantFlow_B_Lmin >= rDiwCoolantFlow_C_Lmin) AND (rDiwCoolantFlow_B_Lmin <= rDiwCoolantFlow_A_Lmin)) THEN
        rVotedDiwFlow_Lmin := rDiwCoolantFlow_B_Lmin;
    ELSE
        rVotedDiwFlow_Lmin := rDiwCoolantFlow_C_Lmin;
    END_IF;
    
    (* Discrepancy Debounce (threshold: 0.65 L/min) *)
    tDiscrepancyTimer_Diw(IN := (rDev_Diw_AB > 0.65) OR (rDev_Diw_BC > 0.65) OR (rDev_Diw_CA > 0.65), PT := T#300MS);
    IF tDiscrepancyTimer_Diw.Q THEN
        dwDegradationWord := dwDegradationWord OR 16#0100_0000; (* Bit 24: DIW Flowmeter Discrepancy Alert *)
    END_IF;
ELSIF bDiw_A_Ok AND bDiw_B_Ok THEN
    bDiw_Degraded_1oo2 := TRUE;
    bDegradedSensorMode := TRUE;
    rVotedDiwFlow_Lmin := (rDiwCoolantFlow_A_Lmin + rDiwCoolantFlow_B_Lmin) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0200_0000; (* Bit 25: DIW Flow Degraded to 1oo2 (C Failed) *)
ELSIF bDiw_B_Ok AND bDiw_C_Ok THEN
    bDiw_Degraded_1oo2 := TRUE;
    bDegradedSensorMode := TRUE;
    rVotedDiwFlow_Lmin := (rDiwCoolantFlow_B_Lmin + rDiwCoolantFlow_C_Lmin) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0400_0000; (* Bit 26: DIW Flow Degraded to 1oo2 (A Failed) *)
ELSIF bDiw_A_Ok AND bDiw_C_Ok THEN
    bDiw_Degraded_1oo2 := TRUE;
    bDegradedSensorMode := TRUE;
    rVotedDiwFlow_Lmin := (rDiwCoolantFlow_A_Lmin + rDiwCoolantFlow_C_Lmin) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0800_0000; (* Bit 27: DIW Flow Degraded to 1oo2 (B Failed) *)
ELSIF bDiw_A_Ok THEN
    bDegradedSensorMode := TRUE;
    rVotedDiwFlow_Lmin := rDiwCoolantFlow_A_Lmin;
    dwDegradationWord := dwDegradationWord OR 16#1000_0000; (* Bit 28: DIW Flow 1oo1 Mode (B, C Failed) *)
ELSIF bDiw_B_Ok THEN
    bDegradedSensorMode := TRUE;
    rVotedDiwFlow_Lmin := rDiwCoolantFlow_B_Lmin;
    dwDegradationWord := dwDegradationWord OR 16#2000_0000; (* Bit 29: DIW Flow 1oo1 Mode (A, C Failed) *)
ELSIF bDiw_C_Ok THEN
    bDegradedSensorMode := TRUE;
    rVotedDiwFlow_Lmin := rDiwCoolantFlow_C_Lmin;
    dwDegradationWord := dwDegradationWord OR 16#4000_0000; (* Bit 30: DIW Flow 1oo1 Mode (A, B Failed) *)
ELSE
    bDiw_Trip := TRUE;
    rVotedDiwFlow_Lmin := 0.0;
    dwDegradationWord := dwDegradationWord OR 16#8000_0000; (* Bit 31: DIW Flowmeter Total Sensor Failure *)
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* 1.5 IN-LINE AOI KERF 1 & KERF 2 METROLOGY VOTING [um]                                                *)
(* ---------------------------------------------------------------------------------------------------- *)
rDev_Kerf1_AB := ABS(rKerf1Width_A_um - rKerf1Width_B_um);
rDev_Kerf1_BC := ABS(rKerf1Width_B_um - rKerf1Width_C_um);
rDev_Kerf1_CA := ABS(rKerf1Width_C_um - rKerf1Width_A_um);

bKerf1_A_Ok := (rKerf1Width_A_um >= 15.0) AND (rKerf1Width_A_um <= 50.0);
bKerf1_B_Ok := (rKerf1Width_B_um >= 15.0) AND (rKerf1Width_B_um <= 50.0);
bKerf1_C_Ok := (rKerf1Width_C_um >= 15.0) AND (rKerf1Width_C_um <= 50.0);

IF bKerf1_A_Ok AND bKerf1_B_Ok AND bKerf1_C_Ok THEN
    bKerf1_Degraded_1oo2 := FALSE;
    IF ((rKerf1Width_A_um >= rKerf1Width_B_um) AND (rKerf1Width_A_um <= rKerf1Width_C_um)) OR
       ((rKerf1Width_A_um >= rKerf1Width_C_um) AND (rKerf1Width_A_um <= rKerf1Width_B_um)) THEN
        rVotedKerf1Width_um := rKerf1Width_A_um;
    ELSIF ((rKerf1Width_B_um >= rKerf1Width_A_um) AND (rKerf1Width_B_um <= rKerf1Width_C_um)) OR
          ((rKerf1Width_B_um >= rKerf1Width_C_um) AND (rKerf1Width_B_um <= rKerf1Width_A_um)) THEN
        rVotedKerf1Width_um := rKerf1Width_B_um;
    ELSE
        rVotedKerf1Width_um := rKerf1Width_C_um;
    END_IF;
ELSIF bKerf1_A_Ok AND bKerf1_B_Ok THEN
    bKerf1_Degraded_1oo2 := TRUE;
    rVotedKerf1Width_um := (rKerf1Width_A_um + rKerf1Width_B_um) * 0.5;
ELSIF bKerf1_B_Ok AND bKerf1_C_Ok THEN
    bKerf1_Degraded_1oo2 := TRUE;
    rVotedKerf1Width_um := (rKerf1Width_B_um + rKerf1Width_C_um) * 0.5;
ELSIF bKerf1_A_Ok AND bKerf1_C_Ok THEN
    bKerf1_Degraded_1oo2 := TRUE;
    rVotedKerf1Width_um := (rKerf1Width_A_um + rKerf1Width_C_um) * 0.5;
ELSIF bKerf1_A_Ok THEN
    rVotedKerf1Width_um := rKerf1Width_A_um;
ELSIF bKerf1_B_Ok THEN
    rVotedKerf1Width_um := rKerf1Width_B_um;
ELSIF bKerf1_C_Ok THEN
    rVotedKerf1Width_um := rKerf1Width_C_um;
ELSE
    rVotedKerf1Width_um := rNominalKerfWidth_um;
END_IF;

(* Kerf 2 Optical Metrology Voting *)
rDev_Kerf2_AB := ABS(rKerf2Width_A_um - rKerf2Width_B_um);
rDev_Kerf2_BC := ABS(rKerf2Width_B_um - rKerf2Width_C_um);
rDev_Kerf2_CA := ABS(rKerf2Width_C_um - rKerf2Width_A_um);

bKerf2_A_Ok := (rKerf2Width_A_um >= 15.0) AND (rKerf2Width_A_um <= 50.0);
bKerf2_B_Ok := (rKerf2Width_B_um >= 15.0) AND (rKerf2Width_B_um <= 50.0);
bKerf2_C_Ok := (rKerf2Width_C_um >= 15.0) AND (rKerf2Width_C_um <= 50.0);

IF bKerf2_A_Ok AND bKerf2_B_Ok AND bKerf2_C_Ok THEN
    bKerf2_Degraded_1oo2 := FALSE;
    IF ((rKerf2Width_A_um >= rKerf2Width_B_um) AND (rKerf2Width_A_um <= rKerf2Width_C_um)) OR
       ((rKerf2Width_A_um >= rKerf2Width_C_um) AND (rKerf2Width_A_um <= rKerf2Width_B_um)) THEN
        rVotedKerf2Width_um := rKerf2Width_A_um;
    ELSIF ((rKerf2Width_B_um >= rKerf2Width_A_um) AND (rKerf2Width_B_um <= rKerf2Width_C_um)) OR
          ((rKerf2Width_B_um >= rKerf2Width_C_um) AND (rKerf2Width_B_um <= rKerf2Width_A_um)) THEN
        rVotedKerf2Width_um := rKerf2Width_B_um;
    ELSE
        rVotedKerf2Width_um := rKerf2Width_C_um;
    END_IF;
ELSIF bKerf2_A_Ok AND bKerf2_B_Ok THEN
    bKerf2_Degraded_1oo2 := TRUE;
    rVotedKerf2Width_um := (rKerf2Width_A_um + rKerf2Width_B_um) * 0.5;
ELSIF bKerf2_B_Ok AND bKerf2_C_Ok THEN
    bKerf2_Degraded_1oo2 := TRUE;
    rVotedKerf2Width_um := (rKerf2Width_B_um + rKerf2Width_C_um) * 0.5;
ELSIF bKerf2_A_Ok AND bKerf2_C_Ok THEN
    bKerf2_Degraded_1oo2 := TRUE;
    rVotedKerf2Width_um := (rKerf2Width_A_um + rKerf2Width_C_um) * 0.5;
ELSIF bKerf2_A_Ok THEN
    rVotedKerf2Width_um := rKerf2Width_A_um;
ELSIF bKerf2_B_Ok THEN
    rVotedKerf2Width_um := rKerf2Width_B_um;
ELSIF bKerf2_C_Ok THEN
    rVotedKerf2Width_um := rKerf2Width_C_um;
ELSE
    rVotedKerf2Width_um := rNominalKerfWidth_um;
END_IF;
"""

print("Phase 1 TMR defined.")
def build_phase2_blade_wear():
    return """(* ==================================================================================================== *)
(* PHASE 2: DYNAMIC BLADE WEAR TRACKING & TAPE PENETRATION CLOSED LOOP                                 *)
(* ==================================================================================================== *)
(* Real-time integration of diamond abrasive wear, non-contact laser calibration offset integration,   *)
(* aerostatic film stiffness calculation, and closed-loop Z-axis depth adjustment to maintain 20.0 um   *)
(* tape penetration without cutting through backing carrier or chuck table.                             *)

(* 2.1 Cutting Distance Integration *)
IF bCycleActive AND (ABS(rXAxisVelocity_mms) > 0.5) THEN
    rCumulativeCutDistance1_m := rCumulativeCutDistance1_m + (ABS(rXAxisVelocity_mms) * rCycleTime_sec * 0.001);
    rCumulativeCutDistance2_m := rCumulativeCutDistance2_m + (ABS(rXAxisVelocity_mms) * rCycleTime_sec * 0.001);
END_IF;

(* 2.2 Tangential Micro-Grinding Force & Aerostatic Stiffness Estimation *)
IF c_NominalBlade1Diameter_mm > 10.0 THEN
    rEstimatedCuttingForce1_N := rSpindle1Torque_Nm / (0.5 * c_NominalBlade1Diameter_mm * 0.001);
ELSE
    rEstimatedCuttingForce1_N := 0.0;
END_IF;

IF c_NominalBlade2Diameter_mm > 10.0 THEN
    rEstimatedCuttingForce2_N := rSpindle2Torque_Nm / (0.5 * c_NominalBlade2Diameter_mm * 0.001);
ELSE
    rEstimatedCuttingForce2_N := 0.0;
END_IF;

(* Dynamic Aerostatic Squeeze Film Stiffness [N/um] *)
rBlade1AeroStiffness_N_um := (rVotedAirBearingPress1_bar * 12.5) / (c_NominalAirBearingClearance_um + ABS(x_state[3]) + 0.001);
rBlade2AeroStiffness_N_um := (rVotedAirBearingPress2_bar * 12.5) / (c_NominalAirBearingClearance_um + ABS(x_state[4]) + 0.001);

(* 2.3 Diamond Attrition Rate & Cumulative Diameter Loss Calculation *)
rBlade1DeltaWear_um := c_DiamondWearCoeff1 * (rEstimatedCuttingForce1_N + 0.1) * rCumulativeCutDistance1_m;
rBlade2DeltaWear_um := c_DiamondWearCoeff2 * (rEstimatedCuttingForce2_N + 0.1) * rCumulativeCutDistance2_m;

rCalculatedBlade1Wear_um := rBlade1DeltaWear_um;
rCalculatedBlade2Wear_um := rBlade2DeltaWear_um;

(* 2.4 Usable Blade Exposure Tracking & Flange Safety Limit Check *)
rBlade1Exposure_um := ((c_NominalBlade1Diameter_mm * 1000.0) - rBlade1DeltaWear_um - (c_FlangeSafetyDiameter_mm * 1000.0)) * 0.5;
rBlade2Exposure_um := ((c_NominalBlade2Diameter_mm * 1000.0) - rBlade2DeltaWear_um - (c_FlangeSafetyDiameter_mm * 1000.0)) * 0.5;

bBlade1WearLimitReached := (rBlade1Exposure_um <= 450.0);
bBlade2WearLimitReached := (rBlade2Exposure_um <= 450.0);

(* 2.5 Closed-Loop Z1 & Z2 Cutting Depth Synthesis with Tape Penetration Control *)
(* Spindle 1 (Step Cut): Penetrates silicon from top surface down to commanded step depth *)
rCalculatedZ1Apex_mm := (rChuckDatumZ_mm + ((rDicingTapeThickness_um + rWaferThickness_um - rStepCutDepth_um) * 0.001)) - (rBlade1DeltaWear_um * 0.0005);
rEffectiveZ1Depth_um := rStepCutDepth_um + (rBlade1DeltaWear_um * 0.5);

(* Spindle 2 (Full Cut): Severs remaining silicon and penetrates commanded depth into dicing tape *)
rCalculatedZ2Apex_mm := (rChuckDatumZ_mm + ((rDicingTapeThickness_um - rTargetTapePenetration_um) * 0.001)) - (rBlade2DeltaWear_um * 0.0005);
rTapePenetrationActual_um := ((rChuckDatumZ_mm + (rDicingTapeThickness_um * 0.001)) - rCalculatedZ2Apex_mm) * 1000.0;
rEffectiveZ2Depth_um := rTapePenetrationActual_um;

(* Dicing Tape Cut-Through Protection Interlock: Trip if tape penetration > 35.0 um *)
IF rTapePenetrationActual_um > c_MaxTapePenetration_um THEN
    bTapeCutThroughAlarm := TRUE;
ELSE
    bTapeCutThroughAlarm := FALSE;
END_IF;

(* 2.6 Diamond Binder Glazing Index Calculation *)
IF ABS(rXAxisVelocity_mms) > 2.0 THEN
    rGlazeMetricBlade1 := rSpindle1Current_A / ABS(rXAxisVelocity_mms);
    rGlazeMetricBlade2 := rSpindle2Current_A / ABS(rXAxisVelocity_mms);
ELSE
    rGlazeMetricBlade1 := 0.0;
    rGlazeMetricBlade2 := 0.0;
END_IF;

bBlade1GlazeWarning := (rGlazeMetricBlade1 > 0.38);
bBlade2GlazeWarning := (rGlazeMetricBlade2 > 0.38);

(* 2.7 Acoustic Emission (AE) & Spindle Motor Current Fast Breakage Detection (< 10 ms) *)
rSpindle1CurrentDeriv_As := (rSpindle1Current_A - rPrevSpindle1Current_A) / rCycleTime_sec;
rSpindle2CurrentDeriv_As := (rSpindle2Current_A - rPrevSpindle2Current_A) / rCycleTime_sec;
rPrevSpindle1Current_A := rSpindle1Current_A;
rPrevSpindle2Current_A := rSpindle2Current_A;

(* Exponential smoothing filter on AE signals *)
rAeFiltered1_dB := (0.80 * rAeFiltered1_dB) + (0.20 * rSpindle1AcousticEmission_dB);
rAeFiltered2_dB := (0.80 * rAeFiltered2_dB) + (0.20 * rSpindle2AcousticEmission_dB);

(* Instantaneous blade micro-fracture or binder burst detector *)
IF (rSpindle1AcousticEmission_dB > rMaxAcousticTrip_dB) OR (ABS(rSpindle1CurrentDeriv_As) > 280.0) THEN
    bBlade1BreakageDetected := TRUE;
END_IF;

IF (rSpindle2AcousticEmission_dB > rMaxAcousticTrip_dB) OR (ABS(rSpindle2CurrentDeriv_As) > 280.0) THEN
    bBlade2BreakageDetected := TRUE;
END_IF;

(* 2.8 Deionized Water (DIW) Temperature-Compensated Resistivity Calculation *)
rCompensatedResistivity_MOhm := rDiwResistivity_MOhm_cm * (1.0 + (0.021 * (rDiwTemperature_DegC - 25.0)));
"""

print("Phase 2 Blade Wear defined.")
def build_phase3_statespace():
    return """(* ==================================================================================================== *)
(* PHASE 3: DISCRETE STATE-SPACE PREDICTION (x[k+1] = A*x[k] + B*u[k])                                  *)
(* ==================================================================================================== *)
(* Comprehensive 16-state, 8-input discrete dynamic observer modeling high-speed aerostatic spindle     *)
(* compliance, coreless linear motor table kinematics, silicon micro-grinding ductile/brittle mechanics, *)
(* diamond abrasive grit attrition, kerf cut width propagation, and DIW coolant hydrodynamics.          *)

(* 3.1 Cold-Start Matrix Initialization *)
IF NOT bMatricesInitialized THEN
    (* Zero-clear all matrix elements *)
    FOR iRow := 1 TO 16 DO
        FOR iCol := 1 TO 16 DO
            A_mat[iRow, iCol] := 0.0;
            C_mat[iRow, iCol] := 0.0;
        END_FOR;
        FOR kInput := 1 TO 8 DO
            B_mat[iRow, kInput] := 0.0;
            D_mat[iRow, kInput] := 0.0;
        END_FOR;
    END_FOR;

    (* ------------------------------------------------------------------------------------------------ *)
    (* State Transition Matrix A (16x16): System Physics & Inter-State Coupling                         *)
    (* ------------------------------------------------------------------------------------------------ *)
    (* x1: Spindle 1 angular velocity deviation Delta_omega1 [rad/s] *)
    A_mat[1, 1]  := 0.9850; (* Rotational inertia damping time constant *)
    A_mat[1, 9]  := -0.0420;(* Deceleration torque from Step Blade 1 cutting force F_t1 *)

    (* x2: Spindle 2 angular velocity deviation Delta_omega2 [rad/s] *)
    A_mat[2, 2]  := 0.9850; (* Rotational inertia damping time constant *)
    A_mat[2, 10] := -0.0510;(* Deceleration torque from Full Blade 2 cutting force F_t2 *)

    (* x3: Spindle 1 aerostatic radial air film deflection delta_r1 [um] *)
    A_mat[3, 3]  := 0.9120; (* Aerostatic journal squeeze-film stiffness retention *)
    A_mat[3, 9]  := 0.0180; (* Radial film deflection induced by tangential cutting force F_t1 *)

    (* x4: Spindle 2 aerostatic radial air film deflection delta_r2 [um] *)
    A_mat[4, 4]  := 0.9120; (* Aerostatic journal squeeze-film stiffness retention *)
    A_mat[4, 10] := 0.0220; (* Radial film deflection induced by tangential cutting force F_t2 *)

    (* x5: Spindle 1 aerostatic axial compliance displacement delta_z1 [um] *)
    A_mat[5, 5]  := 0.9350; (* Double-acting aerostatic thrust bearing recovery *)
    A_mat[5, 9]  := 0.0085; (* Axial thrust cross-coupling from micro-grinding torque *)

    (* x6: Spindle 2 aerostatic axial compliance displacement delta_z2 [um] *)
    A_mat[6, 6]  := 0.9350; (* Double-acting aerostatic thrust bearing recovery *)
    A_mat[6, 10] := 0.0098; (* Axial thrust cross-coupling from micro-grinding torque *)

    (* x7: X-axis coreless linear motor carriage velocity Delta_vx [mm/s] *)
    A_mat[7, 7]  := 0.9400; (* Linear motor electromagnetic velocity damping *)
    A_mat[7, 8]  := -0.0250;(* Carriage compliance coupling with structural vibration mode *)
    A_mat[7, 9]  := -0.0150;(* Feed deceleration caused by Blade 1 cutting resistance *)
    A_mat[7, 10] := -0.0180;(* Feed deceleration caused by Blade 2 cutting resistance *)

    (* x8: X-axis chuck structural compliant vibration mode xi_x [um] *)
    A_mat[8, 8]  := 0.8800; (* Machine granite bed structural modal damping *)
    A_mat[8, 7]  := 0.0350; (* Table acceleration excitation of resonant mode *)
    A_mat[8, 9]  := 0.0120; (* Grinding force chatter excitation Blade 1 *)
    A_mat[8, 10] := 0.0150; (* Grinding force chatter excitation Blade 2 *)

    (* x9: Blade 1 step-cut tangential grinding force F_t1 [N] *)
    A_mat[9, 9]  := 0.8200; (* Micro-grinding contact arc force dissipation *)
    A_mat[9, 7]  := 0.0650; (* Force increase with linear feed velocity v_x *)
    A_mat[9, 11] := 0.0400; (* Force increase as diamond grits dull and wear *)

    (* x10: Blade 2 full-cut tangential grinding force F_t2 [N] *)
    A_mat[10, 10] := 0.8100;(* Micro-grinding contact arc force dissipation *)
    A_mat[10, 7]  := 0.0780;(* Force increase with linear feed velocity v_x *)
    A_mat[10, 12] := 0.0480;(* Force increase as diamond grits dull and wear *)

    (* x11: Blade 1 diamond grit outer diameter attrition Delta_D1 [um] *)
    A_mat[11, 11] := 1.0000;(* Material loss persistence (irreversible cumulative wear) *)
    A_mat[11, 9]  := 0.000045; (* Wear progression rate proportional to cutting force *)

    (* x12: Blade 2 diamond grit outer diameter attrition Delta_D2 [um] *)
    A_mat[12, 12] := 1.0000;(* Material loss persistence (irreversible cumulative wear) *)
    A_mat[12, 10] := 0.000052; (* Wear progression rate proportional to cutting force *)

    (* x13: Kerf 1 cut width deviation Delta_w1 [um] *)
    A_mat[13, 13] := 0.8500;(* Kerf geometric profile persistence *)
    A_mat[13, 3]  := 0.2800;(* Spindle 1 radial film deflection broadens kerf cut *)
    A_mat[13, 8]  := 0.1500;(* Chuck table micro-vibration widens kerf channel *)
    A_mat[13, 11] := 0.1200;(* Diamond abrasive pullout and blade fluttering *)

    (* x14: Kerf 2 cut width deviation Delta_w2 [um] *)
    A_mat[14, 14] := 0.8400;(* Kerf geometric profile persistence *)
    A_mat[14, 4]  := 0.3100;(* Spindle 2 radial film deflection broadens kerf cut *)
    A_mat[14, 8]  := 0.1600;(* Chuck table micro-vibration widens kerf channel *)
    A_mat[14, 12] := 0.1400;(* Diamond abrasive pullout and blade fluttering *)

    (* x15: DIW coolant hydrodynamic wedge pressure P_diw [bar] *)
    A_mat[15, 15] := 0.8900;(* Coolant hydraulic pressure boundary dissipation *)
    A_mat[15, 7]  := 0.0200;(* Hydrodynamic squeeze entrainment with feed velocity *)

    (* x16: Ultra-thin wafer micro-crack chipping propagation metric chi_chip [um] *)
    A_mat[16, 16] := 0.8600;(* Micro-crack tip stress concentration relaxation *)
    A_mat[16, 9]  := 0.0350;(* Chipping propagation driven by Step Blade force F_t1 *)
    A_mat[16, 10] := 0.0450;(* Chipping propagation driven by Full Blade force F_t2 *)
    A_mat[16, 15] := -0.0280;(* Hydrodynamic DIW coolant dampens chipping and flushes swarf *)

    (* ------------------------------------------------------------------------------------------------ *)
    (* Control Input Matrix B (16x8): Actuator Influence onto State Dynamics                            *)
    (* ------------------------------------------------------------------------------------------------ *)
    (* u1: Spindle 1 motor torque current demand i_q1 [A] *)
    B_mat[1, 1]  := 1.4500; (* Torque acceleration on Spindle 1 angular speed *)

    (* u2: Spindle 2 motor torque current demand i_q2 [A] *)
    B_mat[2, 2]  := 1.4500; (* Torque acceleration on Spindle 2 angular speed *)

    (* u3: X-axis linear motor feed velocity demand v_x,cmd [mm/s] *)
    B_mat[7, 3]  := 0.0850; (* Linear motor servo drive velocity tracking gain *)

    (* u4: Z1-axis step-cut position fine trim Delta_z1 [um] *)
    B_mat[9, 4]  := 0.1200; (* Depth-of-cut modulation directly shifts grinding force F_t1 *)
    B_mat[13, 4] := 0.0350; (* Depth trim alters kerf cut boundary *)

    (* u5: Z2-axis full-cut position fine trim Delta_z2 [um] *)
    B_mat[10, 5] := 0.1450; (* Depth-of-cut modulation directly shifts grinding force F_t2 *)
    B_mat[14, 5] := 0.0420; (* Depth trim alters kerf cut boundary *)

    (* u6: Y-axis index tracking position fine trim Delta_y [um] *)
    B_mat[13, 6] := 0.0150; (* Y-axis tracking fine correction for Kerf 1 *)
    B_mat[14, 6] := 0.0150; (* Y-axis tracking fine correction for Kerf 2 *)

    (* u7: DIW coolant nozzle high-pressure valve trim u_diw [%] *)
    B_mat[15, 7] := 0.0450; (* Coolant supply valve modulation alters wedge pressure *)
    B_mat[16, 7] := -0.0180;(* Increased coolant flush directly suppresses edge chipping *)

    (* u8: Acoustic emission blade breakage adaptive sensitivity factor k_ae [-] *)
    B_mat[16, 8] := -0.0050;(* Sensitivity adaptation for fracture monitoring *)

    (* ------------------------------------------------------------------------------------------------ *)
    (* Output Observation Matrix C (16x16) & Direct Feedthrough D (16x8)                                *)
    (* ------------------------------------------------------------------------------------------------ *)
    FOR iRow := 1 TO 16 DO
        C_mat[iRow, iRow] := 1.0000; (* Direct unity observation scaling *)
    END_FOR;

    (* ------------------------------------------------------------------------------------------------ *)
    (* MPC Weighting Matrices: Q_diag (States), R_diag (Move Suppression), P_diag (Terminal)            *)
    (* ------------------------------------------------------------------------------------------------ *)
    Q_diag[1]  := 1.20;  (* Spindle 1 speed stability *)
    Q_diag[2]  := 1.20;  (* Spindle 2 speed stability *)
    Q_diag[3]  := 8.50;  (* Spindle 1 aerostatic radial deflection penalty *)
    Q_diag[4]  := 8.50;  (* Spindle 2 aerostatic radial deflection penalty *)
    Q_diag[5]  := 4.00;  (* Spindle 1 axial compliance penalty *)
    Q_diag[6]  := 4.00;  (* Spindle 2 axial compliance penalty *)
    Q_diag[7]  := 2.50;  (* Feed velocity regulation *)
    Q_diag[8]  := 12.00; (* Machine vibration suppression *)
    Q_diag[9]  := 6.50;  (* Tangential grinding force 1 regulation *)
    Q_diag[10] := 7.50;  (* Tangential grinding force 2 regulation *)
    Q_diag[11] := 3.00;  (* Blade 1 wear monitoring *)
    Q_diag[12] := 3.00;  (* Blade 2 wear monitoring *)
    Q_diag[13] := 25.00; (* High priority: Kerf 1 cut width tolerance (25.0 um +/- 1.0 um) *)
    Q_diag[14] := 25.00; (* High priority: Kerf 2 cut width tolerance (25.0 um +/- 1.0 um) *)
    Q_diag[15] := 5.00;  (* DIW coolant pressure maintenance *)
    Q_diag[16] := 30.00; (* Critical priority: Silicon edge chipping suppression (< 15 um) *)

    R_diag[1]  := 0.45;  (* Spindle 1 torque move rate suppression *)
    R_diag[2]  := 0.45;  (* Spindle 2 torque move rate suppression *)
    R_diag[3]  := 0.85;  (* Linear motor feedrate acceleration limiter *)
    R_diag[4]  := 1.20;  (* Z1 depth trim slew penalty *)
    R_diag[5]  := 1.20;  (* Z2 depth trim slew penalty *)
    R_diag[6]  := 2.50;  (* Y index stepping slew penalty *)
    R_diag[7]  := 0.35;  (* DIW valve slew penalty *)
    R_diag[8]  := 0.10;  (* AE sensitivity slew penalty *)

    FOR iRow := 1 TO 16 DO
        P_diag[iRow] := Q_diag[iRow] * 2.20; (* Terminal state penalty *)
    END_FOR;

    bMatricesInitialized := TRUE;
END_IF;

(* 3.2 State Vector Assembly from Measured Plant Variables *)
x_state[1]  := (rSpindle1SpeedFeedback_rpm - 60000.0) * 0.1047198; (* Convert rpm error to rad/s *)
x_state[2]  := (rSpindle2SpeedFeedback_rpm - 60000.0) * 0.1047198;
x_state[3]  := (7.0 - rVotedAirBearingPress1_bar) * 1.25;           (* Radial film deflection proxy *)
x_state[4]  := (7.0 - rVotedAirBearingPress2_bar) * 1.25;
x_state[5]  := (rZ1StepPosition_mm - rCalculatedZ1Apex_mm) * 1000.0;(* Axial compliance error [um] *)
x_state[6]  := (rZ2FullPosition_mm - rCalculatedZ2Apex_mm) * 1000.0;
x_state[7]  := rXAxisVelocity_mms - rNominalFeedrate_mms;
x_state[8]  := 0.5 * (rDev_Air1_AB + rDev_Air2_AB);                 (* Structural compliance proxy [um] *)
x_state[9]  := rEstimatedCuttingForce1_N;
x_state[10] := rEstimatedCuttingForce2_N;
x_state[11] := rBlade1DeltaWear_um;
x_state[12] := rBlade2DeltaWear_um;
x_state[13] := rVotedKerf1Width_um - rNominalKerfWidth_um;
x_state[14] := rVotedKerf2Width_um - rNominalKerfWidth_um;
x_state[15] := rVotedDiwFlow_Lmin * 0.65;                          (* Coolant pressure proxy [bar] *)
x_state[16] := rTopChippingSize_um;

(* 3.3 Reference Trajectory Vector Assembly *)
x_ref[1]  := 0.0;
x_ref[2]  := 0.0;
x_ref[3]  := 0.0;
x_ref[4]  := 0.0;
x_ref[5]  := 0.0;
x_ref[6]  := 0.0;
x_ref[7]  := 0.0;
x_ref[8]  := 0.0;
x_ref[9]  := 4.50; (* Target nominal grinding force Step Blade [N] *)
x_ref[10] := 5.20; (* Target nominal grinding force Full Blade [N] *)
x_ref[11] := 0.0;
x_ref[12] := 0.0;
x_ref[13] := 0.0; (* Zero kerf 1 width deviation *)
x_ref[14] := 0.0; (* Zero kerf 2 width deviation *)
x_ref[15] := 3.80; (* Target coolant wedge pressure [bar] *)
x_ref[16] := 0.0; (* Zero edge chipping goal *)

(* 3.4 Discrete One-Step-Ahead State Prediction (x_pred = A * x + B * u) *)
FOR iRow := 1 TO 16 DO
    rPredSum := 0.0;
    FOR iCol := 1 TO 16 DO
        rPredSum := rPredSum + (A_mat[iRow, iCol] * x_state[iCol]);
    END_FOR;
    FOR kInput := 1 TO 8 DO
        rPredSum := rPredSum + (B_mat[iRow, kInput] * u_mpc[kInput]);
    END_FOR;
    x_pred[iRow] := rPredSum;
END_FOR;
"""

print("Phase 3 State Space defined.")
def build_phase4_mpc():
    return """(* ==================================================================================================== *)
(* PHASE 4: RECEDING-HORIZON MPC CONTROL ACTION                                                         *)
(* ==================================================================================================== *)
(* Solves unconstrained quadratic programming (QP) active-set gradient descent optimization at 100 Hz.  *)
(* Dynamically modulates linear feedrate v_x to prevent kerf wander and edge micro-chipping on thin     *)
(* 50-micron wafers while optimizing spindle current demands and coolant pressure.                       *)

IF bMpcEnable AND bCycleActive THEN
    bMpcActive := TRUE;

    (* 4.1 Compute Tracking Error Residuals (x_err = x_pred - x_ref) *)
    FOR iRow := 1 TO 16 DO
        x_err[iRow] := x_pred[iRow] - x_ref[iRow];
    END_FOR;

    (* 4.2 Evaluate Quadratic Cost Function J *)
    rCostValue := 0.0;
    FOR iRow := 1 TO 16 DO
        rCostValue := rCostValue + (Q_diag[iRow] * x_err[iRow] * x_err[iRow]);
    END_FOR;
    FOR kInput := 1 TO 8 DO
        rCostValue := rCostValue + (R_diag[kInput] * (u_mpc[kInput] - u_prev[kInput]) * (u_mpc[kInput] - u_prev[kInput]));
    END_FOR;

    (* 4.3 Compute Analytical Cost Gradient Vector (grad_J = 2*R*(u - u_prev) + 2*B^T*Q*x_err) *)
    FOR kInput := 1 TO 8 DO
        grad_J[kInput] := 2.0 * R_diag[kInput] * (u_mpc[kInput] - u_prev[kInput]);
        FOR iRow := 1 TO 16 DO
            grad_J[kInput] := grad_J[kInput] + (2.0 * Q_diag[iRow] * B_mat[iRow, kInput] * x_err[iRow]);
        END_FOR;
    END_FOR;

    (* 4.4 Projected Gradient Descent Control Move Update *)
    FOR kInput := 1 TO 8 DO
        u_delta[kInput] := -rStepSize * grad_J[kInput];
        u_mpc[kInput] := u_mpc[kInput] + u_delta[kInput];
    END_FOR;

    (* 4.5 Physical Actuator Saturation & Cyber-Physical Safety Invariants *)
    (* Invariant 1: Spindle 1 & 2 Motor Torque Current Bounds [A] *)
    IF u_mpc[1] > 22.0 THEN u_mpc[1] := 22.0; ELSIF u_mpc[1] < 1.0 THEN u_mpc[1] := 1.0; END_IF;
    IF u_mpc[2] > 22.0 THEN u_mpc[2] := 22.0; ELSIF u_mpc[2] < 1.0 THEN u_mpc[2] := 1.0; END_IF;

    (* Invariant 2: X-Axis Linear Feedrate Modulation & Derating Rules *)
    (* Rule A: High Cutting Force Derating (Prevents blade deflection and kerf wander) *)
    IF (rEstimatedCuttingForce1_N + rEstimatedCuttingForce2_N) > 10.5 THEN
        u_mpc[3] := MIN(u_mpc[3], rNominalFeedrate_mms * 0.65);
    END_IF;

    (* Rule B: Ultra-Thin Wafer (< 100 um) Fragility Constraint *)
    IF rWaferThickness_um < 100.0 THEN
        u_mpc[3] := MIN(u_mpc[3], 90.0); (* Cap feedrate to 90 mm/s to prevent brittle wafer cracking *)
    END_IF;

    (* Rule C: Wafer Edge Ingress / Egress Deceleration (Minimizes perimeter chipping) *)
    IF (ABS(rXAxisPosition_mm) > ((0.5 * rWaferDiameter_mm) - 20.0)) THEN
        u_mpc[3] := MIN(u_mpc[3], rNominalFeedrate_mms * 0.45);
    END_IF;

    (* Rule D: Absolute Physical Travel Limits on Feedrate [mm/s] *)
    IF u_mpc[3] > 400.0 THEN u_mpc[3] := 400.0; ELSIF u_mpc[3] < 15.0 THEN u_mpc[3] := 15.0; END_IF;

    (* Invariant 3: Z1 & Z2 Position Trim Limits [-15.0 um .. +15.0 um] *)
    IF u_mpc[4] > 15.0 THEN u_mpc[4] := 15.0; ELSIF u_mpc[4] < -15.0 THEN u_mpc[4] := -15.0; END_IF;
    IF u_mpc[5] > 15.0 THEN u_mpc[5] := 15.0; ELSIF u_mpc[5] < -15.0 THEN u_mpc[5] := -15.0; END_IF;

    (* Invariant 4: Y-Axis Index Offset Trim [-5.0 um .. +5.0 um] *)
    IF u_mpc[6] > 5.0 THEN u_mpc[6] := 5.0; ELSIF u_mpc[6] < -5.0 THEN u_mpc[6] := -5.0; END_IF;

    (* Invariant 5: DIW Coolant Valve Demand [40.0% .. 100.0%] *)
    IF u_mpc[7] > 100.0 THEN u_mpc[7] := 100.0; ELSIF u_mpc[7] < 40.0 THEN u_mpc[7] := 40.0; END_IF;

    (* Invariant 6: AE Adaptive Sensitivity [0.5 .. 2.0] *)
    IF u_mpc[8] > 2.0 THEN u_mpc[8] := 2.0; ELSIF u_mpc[8] < 0.5 THEN u_mpc[8] := 0.5; END_IF;

    (* 4.6 Synthesize Physical Actuator Demands *)
    rSpindle1SpeedDemand_rpm := 60000.0 + (u_mpc[1] * 20.0);
    rSpindle2SpeedDemand_rpm := 60000.0 + (u_mpc[2] * 20.0);
    rXFeedVelocityDemand_mms := u_mpc[3];
    rZ1StepCutDemand_mm := rCalculatedZ1Apex_mm + (u_mpc[4] * 0.001);
    rZ2FullCutDemand_mm := rCalculatedZ2Apex_mm + (u_mpc[5] * 0.001);
    rDiwFlowDemand_Lmin := 4.0 + (u_mpc[7] * 0.045);
    rDiwPressureDemand_bar := 3.2 + (u_mpc[7] * 0.028);

    (* Store History for Next Iteration Rate-of-Change Suppression *)
    FOR kInput := 1 TO 8 DO
        u_prev[kInput] := u_mpc[kInput];
    END_FOR;
ELSE
    bMpcActive := FALSE;
    rXFeedVelocityDemand_mms := rNominalFeedrate_mms;
    rSpindle1SpeedDemand_rpm := 60000.0;
    rSpindle2SpeedDemand_rpm := 60000.0;
    rZ1StepCutDemand_mm := rCalculatedZ1Apex_mm;
    rZ2FullCutDemand_mm := rCalculatedZ2Apex_mm;
    rDiwFlowDemand_Lmin := 5.0;
    rDiwPressureDemand_bar := 4.0;
END_IF;
"""

print("Phase 4 MPC defined.")
def build_phase5_aoi():
    return """(* ==================================================================================================== *)
(* PHASE 5: HIGH-SPEED IN-LINE AOI KERF & CHIPPING METROLOGY ANALYSIS                                   *)
(* ==================================================================================================== *)
(* High-magnification optical line-scan metrology executing real-time sub-micron kerf width measurement, *)
(* top and backside silicon chipping defect classification, and street fiducial alignment tracking.     *)

dwAoiInspectionWord := 16#0000_0000;

(* 5.1 Kerf Cut Width Residuals & Lateral Wander Estimation *)
rKerf1Deviation_um := rVotedKerf1Width_um - rNominalKerfWidth_um;
rKerf2Deviation_um := rVotedKerf2Width_um - rNominalKerfWidth_um;
rKerfWanderOffset_um := 0.5 * (rKerf1Deviation_um + rKerf2Deviation_um);

(* 5.2 Quality Criteria Evaluation *)
bKerfWidthOk := (ABS(rKerf1Deviation_um) <= rMaxAllowableKerfDev_um) AND 
                (ABS(rKerf2Deviation_um) <= rMaxAllowableKerfDev_um);

bChippingOk := (rTopChippingSize_um <= rMaxAllowableChipping_um) AND 
               (rBacksideChippingSize_um <= 20.0);

bAoiPass := bKerfWidthOk AND bChippingOk AND 
            (ABS(rStreetOffsetX_um) <= 2.5) AND 
            (ABS(rStreetOffsetY_um) <= 2.5);

bAoiFailKerfWidth := NOT bKerfWidthOk;
bAoiFailChipping := NOT bChippingOk;

(* 5.3 Street Theta Angular Misalignment Correction *)
rResidualTheta_urad := rStreetOffsetTheta_urad;
IF ABS(rResidualTheta_urad) > 17.5 THEN (* Threshold: 17.5 urad = 0.001 degrees *)
    rThetaCorrected_deg := rThetaAngle_deg - (rResidualTheta_urad * 0.00005729578);
    bStreetAligned := FALSE;
ELSE
    rThetaCorrected_deg := rThetaAngle_deg;
    bStreetAligned := TRUE;
END_IF;

(* 5.4 Bit-Packed AOI Inspection Diagnostic Word (dwAoiInspectionWord) *)
dwAoiInspectionWord := dwAoiInspectionWord OR 16#0000_0001; (* Bit 0: Inspection Scan Executed *)

IF ABS(rKerf1Deviation_um) <= rMaxAllowableKerfDev_um THEN
    dwAoiInspectionWord := dwAoiInspectionWord OR 16#0000_0002; (* Bit 1: Kerf 1 Width Within Spec *)
ELSIF rKerf1Deviation_um < -rMaxAllowableKerfDev_um THEN
    dwAoiInspectionWord := dwAoiInspectionWord OR 16#0000_0008; (* Bit 3: Kerf 1 Under-Width (< 24.0 um) *)
ELSE
    dwAoiInspectionWord := dwAoiInspectionWord OR 16#0000_0010; (* Bit 4: Kerf 1 Over-Width / Broadened (> 26.0 um) *)
END_IF;

IF ABS(rKerf2Deviation_um) <= rMaxAllowableKerfDev_um THEN
    dwAoiInspectionWord := dwAoiInspectionWord OR 16#0000_0004; (* Bit 2: Kerf 2 Width Within Spec *)
ELSIF rKerf2Deviation_um < -rMaxAllowableKerfDev_um THEN
    dwAoiInspectionWord := dwAoiInspectionWord OR 16#0000_0020; (* Bit 5: Kerf 2 Under-Width (< 24.0 um) *)
ELSE
    dwAoiInspectionWord := dwAoiInspectionWord OR 16#0000_0040; (* Bit 6: Kerf 2 Over-Width / Broadened (> 26.0 um) *)
END_IF;

IF rTopChippingSize_um <= rMaxAllowableChipping_um THEN
    dwAoiInspectionWord := dwAoiInspectionWord OR 16#0000_0080; (* Bit 7: Top Silicon Chipping Within Spec *)
ELSE
    dwAoiInspectionWord := dwAoiInspectionWord OR 16#0000_0100; (* Bit 8: Top Chipping Exceeded Limit (> 15.0 um) *)
END_IF;

IF rBacksideChippingSize_um <= 20.0 THEN
    dwAoiInspectionWord := dwAoiInspectionWord OR 16#0000_0200; (* Bit 9: Backside Chipping Within Spec *)
ELSE
    dwAoiInspectionWord := dwAoiInspectionWord OR 16#0000_0400; (* Bit 10: Backside Chipping Exceeded Limit (> 20.0 um) *)
END_IF;

IF ABS(rStreetOffsetX_um) <= 2.5 THEN
    dwAoiInspectionWord := dwAoiInspectionWord OR 16#0000_0800; (* Bit 11: Street Offset Delta X In Spec *)
END_IF;

IF ABS(rStreetOffsetY_um) <= 2.5 THEN
    dwAoiInspectionWord := dwAoiInspectionWord OR 16#0000_1000; (* Bit 12: Street Offset Delta Y In Spec *)
END_IF;

IF bStreetAligned THEN
    dwAoiInspectionWord := dwAoiInspectionWord OR 16#0000_2000; (* Bit 13: Theta Alignment Locked In Spec *)
END_IF;

IF (rTopChippingSize_um > 25.0) OR (rBacksideChippingSize_um > 30.0) THEN
    dwAoiInspectionWord := dwAoiInspectionWord OR 16#0000_4000; (* Bit 14: Die Delamination / Gross Chipping Breach *)
END_IF;

IF bAoiPass THEN
    dwAoiInspectionWord := dwAoiInspectionWord OR 16#0000_8000; (* Bit 15: Comprehensive Street Metrology Passed *)
END_IF;
"""

print("Phase 5 AOI defined.")
def build_phase6_fsm():
    return """(* ==================================================================================================== *)
(* PHASE 6: MULTI-STAGE 12-PHASE OPERATIONAL FINITE STATE MACHINE (FSM)                                *)
(* ==================================================================================================== *)
(* Coordinates wafer infeed, vacuum clamping, optical theta alignment, non-contact blade calibration,   *)
(* dual-spindle dicing, in-flight AOI, cross-street 90-deg index, spinner washing, unloading, dressing,  *)
(* and emergency blade fracture fast mitigation.                                                        *)

(* Interlock Check: If emergency stop tripped, force immediate jump to State 999 *)
IF bSystemTripped OR (dwAlarmWord1 <> 16#0000_0000) OR (dwAlarmWord2 <> 16#0000_0000) THEN
    iState := 999;
END_IF;

CASE iState OF
    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 0: IDLE / STANDBY READY                                                                    *)
    (* ------------------------------------------------------------------------------------------------ *)
    0:
        bSystemRunning := FALSE;
        bCycleActive := FALSE;
        bCyclePaused := FALSE;
        iSubState := 0;
        
        (* Maintain Spindles at low idle or ready standby *)
        rSpindle1SpeedDemand_rpm := 10000.0;
        rSpindle2SpeedDemand_rpm := 10000.0;
        rXFeedVelocityDemand_mms := 0.0;
        rZ1StepCutDemand_mm := 15.0; (* Clearance height *)
        rZ2FullCutDemand_mm := 15.0; (* Clearance height *)
        rDiwFlowDemand_Lmin := 0.0;
        rDiwPressureDemand_bar := 0.0;
        rSpinnerWashSpeed_rpm := 0.0;
        rAirKnifePressure_bar := 0.0;

        bSystemReady := bEnableSystem AND bEmergencyStop AND NOT bAir1_Trip AND NOT bAir2_Trip AND 
                        NOT bBlade1WearLimitReached AND NOT bBlade2WearLimitReached;

        IF bAutoCycleStart AND bSystemReady THEN
            bSystemRunning := TRUE;
            bCrossStreetRotated := FALSE;
            iCurrentStreet := 1;
            iState := 10; (* Transition to Infeed *)
        ELSIF bDressBladesCmd AND bSystemReady THEN
            bSystemRunning := TRUE;
            iState := 110; (* Transition to Blade Dressing *)
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 10: WAFER RING FRAME CASSETTE INFEED                                                       *)
    (* ------------------------------------------------------------------------------------------------ *)
    10:
        tCassetteInfeedTimer(IN := TRUE, PT := T#2000MS);
        
        (* Robot loader synchronizes with wafer cassette elevator *)
        rZ1StepCutDemand_mm := 15.0;
        rZ2FullCutDemand_mm := 15.0;
        rXFeedVelocityDemand_mms := 0.0;

        IF tCassetteInfeedTimer.Q THEN
            tCassetteInfeedTimer(IN := FALSE);
            iState := 20; (* Transition to Vacuum Chuck Transfer *)
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 20: VACUUM CHUCK ARM TRANSFER & CENTERING                                                  *)
    (* ------------------------------------------------------------------------------------------------ *)
    20:
        tVacuumChuckTimer(IN := TRUE, PT := T#1500MS);
        
        (* Porous ceramic chuck table applies active vacuum pull-down *)
        IF tVacuumChuckTimer.Q THEN
            tVacuumChuckTimer(IN := FALSE);
            (* Verify 2oo3 vacuum level is sufficient (< -850 mbar gauge) *)
            IF rVotedChuckVacuum_mbar < -850.0 THEN
                iState := 30; (* Transition to Optical Alignment *)
            ELSE
                (* Vacuum seal failure *)
                iState := 999;
            END_IF;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 30: OPTICAL PATTERN RECOGNITION THETA ALIGNMENT                                             *)
    (* ------------------------------------------------------------------------------------------------ *)
    30:
        tThetaAlignTimer(IN := TRUE, PT := T#1800MS);
        
        (* Apply closed-loop Theta rotary alignment to chuck table *)
        rThetaDemand_deg := rThetaCorrected_deg;

        IF tThetaAlignTimer.Q THEN
            tThetaAlignTimer(IN := FALSE);
            IF bStreetAligned OR (ABS(rResidualTheta_urad) <= 25.0) THEN
                iState := 40; (* Transition to Blade Setup Calibration *)
            ELSE
                (* Retry fine alignment *)
                rThetaDemand_deg := rThetaCorrected_deg;
                iState := 40;
            END_IF;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 40: BLADE HEIGHT NON-CONTACT CALIBRATION                                                   *)
    (* ------------------------------------------------------------------------------------------------ *)
    40:
        tBladeSetupTimer(IN := TRUE, PT := T#1200MS);

        (* Both spindles position over non-contact laser optical micrometer *)
        IF tBladeSetupTimer.Q THEN
            tBladeSetupTimer(IN := FALSE);
            (* Check if blade wear has reached hub flange safety threshold *)
            IF bBlade1WearLimitReached OR bBlade2WearLimitReached THEN
                iState := 0; (* Abort to Idle - Blade replacement required *)
            ELSE
                iState := 50; (* Transition to DIW Cooling Initiation *)
            END_IF;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 50: DIW COOLING JET INITIATION & SPINDLE SPIN-UP                                           *)
    (* ------------------------------------------------------------------------------------------------ *)
    50:
        tDiwPrimeTimer(IN := TRUE, PT := T#2500MS);

        (* Spin Spindles to full 60,000 RPM dicing speed *)
        rSpindle1SpeedDemand_rpm := 60000.0;
        rSpindle2SpeedDemand_rpm := 60000.0;
        rDiwFlowDemand_Lmin := 5.5;
        rDiwPressureDemand_bar := 4.2;

        IF tDiwPrimeTimer.Q THEN
            tDiwPrimeTimer(IN := FALSE);
            (* Interlock verification: Flow > 3.5 L/min and Resistivity >= 18.0 MOhm*cm *)
            IF (rVotedDiwFlow_Lmin >= 3.5) AND (rCompensatedResistivity_MOhm >= rMinDiwResistivity_MOhm_cm) AND
               (rSpindle1SpeedFeedback_rpm >= 58500.0) AND (rSpindle2SpeedFeedback_rpm >= 58500.0) THEN
                iState := 60; (* Transition to Dicing Cut *)
            ELSE
                iState := 999; (* Process interlock trip *)
            END_IF;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 60: STEP-CUT & FULL-CUT STREET DICING                                                      *)
    (* ------------------------------------------------------------------------------------------------ *)
    60:
        bCycleActive := TRUE;
        tCutPassTimer(IN := TRUE, PT := T#10S);

        (* Lower cutting spindles to calibrated silicon and tape depths *)
        rZ1StepCutDemand_mm := rCalculatedZ1Apex_mm;
        rZ2FullCutDemand_mm := rCalculatedZ2Apex_mm;

        (* Feed table across 300 mm wafer via linear motor *)
        rXFeedVelocityDemand_mms := u_mpc[3];

        (* Check if cutting pass has completed stroke length *)
        IF (rXAxisPosition_mm >= ((0.5 * rWaferDiameter_mm) + 15.0)) OR tCutPassTimer.Q THEN
            tCutPassTimer(IN := FALSE);
            bCycleActive := FALSE;
            
            (* Retract cutting spindles to clearance height *)
            rZ1StepCutDemand_mm := 10.0;
            rZ2FullCutDemand_mm := 10.0;
            rXFeedVelocityDemand_mms := 0.0;

            iState := 70; (* Transition to In-Flight AOI *)
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 70: HIGH-SPEED IN-FLIGHT KERF OPTICAL AOI                                                  *)
    (* ------------------------------------------------------------------------------------------------ *)
    70:
        tAoiScanTimer(IN := TRUE, PT := T#1000MS);

        (* Line-scan optical camera inspects kerf channel during return stroke *)
        IF tAoiScanTimer.Q THEN
            tAoiScanTimer(IN := FALSE);

            (* Check for street index progression *)
            IF NOT bCrossStreetRotated THEN
                IF iCurrentStreet < iTotalStreetsX THEN
                    iCurrentStreet := iCurrentStreet + 1;
                    rY1IndexDemand_mm := rY1IndexDemand_mm + rStreetPitch_mm;
                    rY2IndexDemand_mm := rY2IndexDemand_mm + rStreetPitch_mm;
                    iState := 60; (* Loop to next street *)
                ELSE
                    iState := 80; (* Completed all X streets -> 90-deg index *)
                END_IF;
            ELSE
                IF iCurrentStreet < iTotalStreetsY THEN
                    iCurrentStreet := iCurrentStreet + 1;
                    rY1IndexDemand_mm := rY1IndexDemand_mm + rStreetPitch_mm;
                    rY2IndexDemand_mm := rY2IndexDemand_mm + rStreetPitch_mm;
                    iState := 60; (* Loop to next perpendicular street *)
                ELSE
                    iState := 90; (* Singulation 100% complete -> Wash & Dry *)
                END_IF;
            END_IF;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 80: CROSS-STREET 90-DEGREE INDEXING & ROTATION                                             *)
    (* ------------------------------------------------------------------------------------------------ *)
    80:
        rZ1StepCutDemand_mm := 15.0;
        rZ2FullCutDemand_mm := 15.0;
        rXFeedVelocityDemand_mms := 0.0;

        (* Rotate Theta axis by exactly 90 degrees *)
        rThetaDemand_deg := rThetaAngle_deg + 90.0;
        bCrossStreetRotated := TRUE;
        iCurrentStreet := 1;

        (* Reset Y index to beginning of perpendicular die street field *)
        rY1IndexDemand_mm := -0.5 * (INT_TO_REAL(iTotalStreetsY) * rStreetPitch_mm);
        rY2IndexDemand_mm := rY1IndexDemand_mm;

        iState := 30; (* Re-verify optical pattern alignment for perpendicular streets *)

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 90: WAFER DIW SPINNER WASH & AIR KNIFE DRY                                                 *)
    (* ------------------------------------------------------------------------------------------------ *)
    90:
        rDiwFlowDemand_Lmin := 0.0; (* Shut off spindle cutting fluid *)
        rDiwPressureDemand_bar := 0.0;
        rSpindle1SpeedDemand_rpm := 10000.0; (* Decelerate spindles to idle *)
        rSpindle2SpeedDemand_rpm := 10000.0;

        IF iSubState = 0 THEN
            (* Substep 0: Start DIW centrifugal surfactant spin wash at 1,800 RPM *)
            rSpinnerWashSpeed_rpm := 1800.0;
            tSpinnerWashTimer(IN := TRUE, PT := T#5000MS);
            IF tSpinnerWashTimer.Q THEN
                tSpinnerWashTimer(IN := FALSE);
                iSubState := 1;
            END_IF;
        ELSIF iSubState = 1 THEN
            (* Substep 1: Ramp spinner to 3,000 RPM with 4.0 bar deionized air knife drying *)
            rSpinnerWashSpeed_rpm := 3000.0;
            rAirKnifePressure_bar := 4.0;
            tAirKnifeDryTimer(IN := TRUE, PT := T#7000MS);
            IF tAirKnifeDryTimer.Q THEN
                tAirKnifeDryTimer(IN := FALSE);
                rSpinnerWashSpeed_rpm := 0.0;
                rAirKnifePressure_bar := 0.0;
                iSubState := 0;
                iState := 100; (* Transition to Unload *)
            END_IF;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 100: WAFER UNLOAD TO OUTPUT MAGAZINE                                                       *)
    (* ------------------------------------------------------------------------------------------------ *)
    100:
        tUnloadTimer(IN := TRUE, PT := T#2500MS);

        IF tUnloadTimer.Q THEN
            tUnloadTimer(IN := FALSE);
            (* Check if diamond blade glazing requires scheduled dressing *)
            IF bBlade1GlazeWarning OR bBlade2GlazeWarning OR bDressBladesCmd THEN
                iState := 110; (* Transition to Blade Dressing *)
            ELSE
                iState := 0; (* Cycle complete -> Return to Idle *)
            END_IF;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 110: BLADE GLAZE DRESSING SEQUENCE (SiC DRESSING BOARD)                                    *)
    (* ------------------------------------------------------------------------------------------------ *)
    110:
        tDressingTimer(IN := TRUE, PT := T#8000MS);

        (* Spindles plunge into SiC dressing board at low feedrate (5 mm/s) to refresh diamond abrasive *)
        rSpindle1SpeedDemand_rpm := 60000.0;
        rSpindle2SpeedDemand_rpm := 60000.0;
        rDiwFlowDemand_Lmin := 6.0;
        rDiwPressureDemand_bar := 4.5;
        rXFeedVelocityDemand_mms := 5.0;

        IF tDressingTimer.Q THEN
            tDressingTimer(IN := FALSE);
            bBlade1GlazeWarning := FALSE;
            bBlade2GlazeWarning := FALSE;
            iState := 40; (* Re-calibrate blade apex heights after dressing *)
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 999: EMERGENCY BLADE BREAKAGE E-STOP CLAMP                                                 *)
    (* ------------------------------------------------------------------------------------------------ *)
    999:
        bSystemTripped := TRUE;
        bSystemRunning := FALSE;
        bCycleActive := FALSE;

        (* Instantaneous 15 ms Z-retract to maximum upward clearance *)
        rZ1StepCutDemand_mm := 25.0;
        rZ2FullCutDemand_mm := 25.0;

        (* Emergency dynamic electrical braking on aerostatic spindles *)
        rSpindle1SpeedDemand_rpm := 0.0;
        rSpindle2SpeedDemand_rpm := 0.0;

        (* Lock X-axis coreless linear motor carriage *)
        rXFeedVelocityDemand_mms := 0.0;

        (* Shut off all cutting DIW coolant valves immediately *)
        rDiwFlowDemand_Lmin := 0.0;
        rDiwPressureDemand_bar := 0.0;
        rSpinnerWashSpeed_rpm := 0.0;
        rAirKnifePressure_bar := 0.0;

        (* Await Operator Fault Reset *)
        IF bResetFaults AND bEmergencyStop AND bEnableSystem AND NOT bAir1_Trip AND NOT bAir2_Trip THEN
            bSystemTripped := FALSE;
            bBlade1BreakageDetected := FALSE;
            bBlade2BreakageDetected := FALSE;
            bTapeCutThroughAlarm := FALSE;
            iState := 0; (* Return to Standby *)
        END_IF;

    ELSE
        iState := 0;
END_CASE;
"""

print("Phase 6 FSM defined.")
def build_phase7_alarms_and_telemetry():
    return """(* ==================================================================================================== *)
(* PHASE 7: ISA-18.2 ALARMS & DIAGNOSTIC WORD PACKING                                                   *)
(* ==================================================================================================== *)
(* Evaluates multi-tiered safety interlocks, process protection trips, advisory warnings with deadband   *)
(* hysteresis, and synthesizes 32-bit packed diagnostic telemetry words.                                *)

dwAlarmWord1 := 16#0000_0000;
dwAlarmWord2 := 16#0000_0000;
dwWarningWord := 16#0000_0000;
dwSystemStatusWord := 16#0000_0000;

(* 7.1 Emergency Safety Trips (dwAlarmWord1) *)
IF NOT bEmergencyStop THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0001; (* Bit 0: SIL-3 E-Stop Relay Open *)
END_IF;

IF NOT bEnableSystem THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0002; (* Bit 1: System Master Enable Dropped *)
END_IF;

IF rVotedAirBearingPress1_bar < 4.50 THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0004; (* Bit 2: Spindle 1 Air Bearing Pressure LL Trip *)
END_IF;

IF rVotedAirBearingPress2_bar < 4.50 THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0008; (* Bit 3: Spindle 2 Air Bearing Pressure LL Trip *)
END_IF;

IF rVotedChuckVacuum_mbar > -600.0 THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0010; (* Bit 4: Chuck Table Vacuum Lost (< 60 kPa) *)
END_IF;

IF bBlade1BreakageDetected THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0020; (* Bit 5: Spindle 1 Blade Fracture / Burst Trip *)
END_IF;

IF bBlade2BreakageDetected THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0040; (* Bit 6: Spindle 2 Blade Fracture / Burst Trip *)
END_IF;

IF rSpindle1Current_A > 38.0 THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0080; (* Bit 7: Spindle 1 Motor Overcurrent / Stall *)
END_IF;

IF rSpindle2Current_A > 38.0 THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0100; (* Bit 8: Spindle 2 Motor Overcurrent / Stall *)
END_IF;

IF bAir1_Trip THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0200; (* Bit 9: Spindle 1 Air Pressure Transducers Dead *)
END_IF;

IF bAir2_Trip THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0400; (* Bit 10: Spindle 2 Air Pressure Transducers Dead *)
END_IF;

IF bVac_Trip THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0800; (* Bit 11: Vacuum Transducers Total Failure *)
END_IF;

IF bDiw_Trip THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_1000; (* Bit 12: DIW Flowmeters Total Failure *)
END_IF;

(* 7.2 Process & Quality Critical Trips (dwAlarmWord2) *)
IF rCompensatedResistivity_MOhm < 15.0 THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0001; (* Bit 0: DIW Resistivity Low-Low (< 15 MOhm*cm) *)
END_IF;

IF (rVotedDiwFlow_Lmin < 2.50) AND bCycleActive THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0002; (* Bit 1: DIW Coolant Flow Starvation During Cut *)
END_IF;

IF bTapeCutThroughAlarm THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0004; (* Bit 2: Dicing Tape Penetration Limit Breach (> 35 um) *)
END_IF;

IF rTopChippingSize_um > 25.0 THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0008; (* Bit 3: Extreme Silicon Surface Chipping Breach *)
END_IF;

IF rBacksideChippingSize_um > 30.0 THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0010; (* Bit 4: Extreme Silicon Backside Chipping Breach *)
END_IF;

IF bBlade1WearLimitReached THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0020; (* Bit 5: Blade 1 Outer Exposure Limit Reached *)
END_IF;

IF bBlade2WearLimitReached THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0040; (* Bit 6: Blade 2 Outer Exposure Limit Reached *)
END_IF;

IF (rXAxisVelocity_mms > 450.0) OR (ABS(x_state[7]) > 80.0) THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0080; (* Bit 7: X-Feed Linear Carriage Velocity Runaway *)
END_IF;

(* Master Safety Trip Latch *)
IF (dwAlarmWord1 <> 16#0000_0000) OR (dwAlarmWord2 <> 16#0000_0000) THEN
    bSystemTripped := TRUE;
END_IF;

(* 7.3 Operational Advisory Warnings (dwWarningWord) *)
IF rCompensatedResistivity_MOhm < rMinDiwResistivity_MOhm_cm THEN
    dwWarningWord := dwWarningWord OR 16#0000_0001; (* Bit 0: DIW Resistivity Low Warning (< 18 MOhm*cm) *)
END_IF;

IF rDiwTemperature_DegC > 23.5 THEN
    dwWarningWord := dwWarningWord OR 16#0000_0002; (* Bit 1: DIW Supply Temperature Drift High *)
END_IF;

IF rBlade1Exposure_um < 600.0 THEN
    dwWarningWord := dwWarningWord OR 16#0000_0004; (* Bit 2: Blade 1 Remaining Life Low Warning *)
END_IF;

IF rBlade2Exposure_um < 600.0 THEN
    dwWarningWord := dwWarningWord OR 16#0000_0008; (* Bit 3: Blade 2 Remaining Life Low Warning *)
END_IF;

IF bBlade1GlazeWarning THEN
    dwWarningWord := dwWarningWord OR 16#0000_0010; (* Bit 4: Blade 1 Binder Glaze Dressing Advised *)
END_IF;

IF bBlade2GlazeWarning THEN
    dwWarningWord := dwWarningWord OR 16#0000_0020; (* Bit 5: Blade 2 Binder Glaze Dressing Advised *)
END_IF;

IF ABS(rKerf1Deviation_um) > rMaxAllowableKerfDev_um THEN
    dwWarningWord := dwWarningWord OR 16#0000_0040; (* Bit 6: Kerf 1 Cut Width Deviation Tolerance Warning *)
END_IF;

IF ABS(rKerf2Deviation_um) > rMaxAllowableKerfDev_um THEN
    dwWarningWord := dwWarningWord OR 16#0000_0080; (* Bit 7: Kerf 2 Cut Width Deviation Tolerance Warning *)
END_IF;

IF rTopChippingSize_um > 12.0 THEN
    dwWarningWord := dwWarningWord OR 16#0000_0100; (* Bit 8: Silicon Surface Micro-Chipping Approaching Limit *)
END_IF;

IF rVotedAirBearingPress1_bar < 5.20 THEN
    dwWarningWord := dwWarningWord OR 16#0000_0200; (* Bit 9: Spindle 1 Air Bearing Pressure Low Warning *)
END_IF;

IF rVotedAirBearingPress2_bar < 5.20 THEN
    dwWarningWord := dwWarningWord OR 16#0000_0400; (* Bit 10: Spindle 2 Air Bearing Pressure Low Warning *)
END_IF;

IF rVotedChuckVacuum_mbar > -800.0 THEN
    dwWarningWord := dwWarningWord OR 16#0000_0800; (* Bit 11: Vacuum Clamping Margin Advisory Warning *)
END_IF;

IF ABS(rResidualTheta_urad) > 15.0 THEN
    dwWarningWord := dwWarningWord OR 16#0000_1000; (* Bit 12: Residual Theta Alignment Warning *)
END_IF;

IF bDegradedSensorMode THEN
    dwWarningWord := dwWarningWord OR 16#0000_2000; (* Bit 13: 2oo3 Sensor Bank Operating Degraded *)
END_IF;

(* 7.4 Bit-Packed Global System Status Word (dwSystemStatusWord) *)
dwSystemStatusWord := dwSystemStatusWord OR (INT_TO_DWORD(iState) AND 16#0000_00FF);

IF bSystemRunning THEN
    dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0100; (* Bit 8: Sequence Active *)
END_IF;

IF bSystemReady THEN
    dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0200; (* Bit 9: System Ready *)
END_IF;

IF bCycleActive THEN
    dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0400; (* Bit 10: Cut Pass Active *)
END_IF;

IF bCyclePaused THEN
    dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0800; (* Bit 11: Feed Hold Paused *)
END_IF;

IF bMpcActive THEN
    dwSystemStatusWord := dwSystemStatusWord OR 16#0000_1000; (* Bit 12: MPC Controller Active *)
END_IF;

IF bAoiPass THEN
    dwSystemStatusWord := dwSystemStatusWord OR 16#0000_2000; (* Bit 13: AOI Metrology Passing *)
END_IF;

IF bDegradedSensorMode THEN
    dwSystemStatusWord := dwSystemStatusWord OR 16#0000_4000; (* Bit 14: Degraded Sensor Mode *)
END_IF;

IF bCrossStreetRotated THEN
    dwSystemStatusWord := dwSystemStatusWord OR 16#0000_8000; (* Bit 15: Cross Streets Rotated *)
END_IF;

dwSystemStatusWord := dwSystemStatusWord OR SHL(INT_TO_DWORD(iCurrentStreet), 16);
dwSystemStatusWord := dwSystemStatusWord OR SHL(INT_TO_DWORD(iSubState), 24);

END_FUNCTION_BLOCK
"""

print("Phase 7 Alarms defined.")
