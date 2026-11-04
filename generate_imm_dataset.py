# -*- coding: utf-8 -*-
"""
Builder and validator for Lumina Synthetic IEC 61131-3 Training Data.
Domain: Heavy Commercial Plastics & High-Tonnage Polymer Processing
System: 1,200-Ton All-Hydraulic Two-Platen Injection Molding Machine (IMM) for Automotive Bumper Fascia
Function Block: FB_Plastics_InjectionMolding_1200T_HydraulicServo_VP
"""

import json
import uuid
import re
import os

def generate_code():
    parts = []
    
    # -------------------------------------------------------------
    # HEADER & DOCUMENTATION
    # -------------------------------------------------------------
    header = """FUNCTION_BLOCK FB_Plastics_InjectionMolding_1200T_HydraulicServo_VP
(*
========================================================================================================================
  LUMINA CYBER-PHYSICAL AUTOMATION ARCHITECTURE - V7 MAX-PERSONA SPECIFICATION
  CORE SECTOR    : HEAVY COMMERCIAL PLASTICS & HIGH-TONNAGE POLYMER PROCESSING
  APPLICATION    : AUTOMOTIVE BUMPER FASCIA MASS PRODUCTION (TPO / PP WITH 15% TALC MINERAL FILLER)
  MACHINE TYPE   : 1,200-METRIC-TON ALL-HYDRAULIC TWO-PLATEN INJECTION MOLDING MACHINE (IMM)
  FUNCTION BLOCK : FB_Plastics_InjectionMolding_1200T_HydraulicServo_VP
  P&ID TAGGING   : ISA-5.1 STANDARD DESIGNATION (ZT, PT, ST, TT, WT, DIT SERIES 100-600)
  REDUNDANCY     : 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) ACROSS ALL 18 PRIMARY PROCESS TRANSMITTER TRIPLETS
  CYBER-PHYSICS  : 8x8 MULTIVARIABLE DISCRETE STATE-SPACE (Ts = 1 ms) COUPLED WITH RECEDING-HORIZON MPC
  THERMODYNAMICS : MODIFIED TAIT EQUATION-OF-STATE (PVT) WITH REAL-TIME COMPRESSIBILITY & SHRINKAGE TRACKING
  TRANSFER LOGIC : HYBRID MULTI-CRITERIA BUMPLESS VELOCITY-TO-PRESSURE (V/P) TRANSFER POINT DETECTOR
  CLAMP BALANCE  : 4-CORNER TIE-BAR TONNAGE BALANCING & PLATEN PARALLELISM OBSERVER (TOLERANCE < 0.05 mm)
  THERMAL CONTROL: 6-ZONE BARREL CONDUCTIVE DECOUPLING & SCREW RECOVERY SHEAR HEATING COMPENSATOR
  EJECTION SYSTEM: MULTI-PULSE HYDRAULIC EJECTOR DE-MOLDING WITH LINEAR SERVO POSITION PROFILES
  SAFETY & ALARM : ISA-18.2 FIVE-TIER MULTI-PARAMETRIC ALARM ENGINE & DUAL-CHANNEL HARDWARE SAFETY INTERLOCKS
  FSM TOPOLOGY   : 12-STAGE DETERMINISTIC OPERATIONAL FINITE STATE MACHINE (FSM)
========================================================================================================================
  THEORETICAL AND MATHEMATICAL FOUNDATION:
  
  1. POLYMER MELT RHEOLOGY & MODIFIED TAIT EQUATION-OF-STATE (PVT):
     Automotive exterior bumper fascia panels require high-flow thermoplastic polyolefin (TPO) melt injected at
     velocities up to 180 mm/s to prevent cosmetic flow hesitations, tiger striping, and cold weld lines.
     The specific volume v(P, T) of the semi-crystalline polymer melt is calculated online via the modified Tait equation:
         v(P, T) = v0(T) * [1.0 - C_tait * ln(1.0 + (P * 1.0E5) / B(T))]
     Where:
         T_kelvin = TT_MELT_NOZZLE_INFRARED_202 + 273.15 [K]
         P_pascal = PT_MOLD_CAVITY_MELT_PRESS_201 * 1.0E5 [Pa]
         v0(T)    = b1m + b2m * (T_kelvin - b5) [m3/kg]
         B(T)     = b3m * exp(-b4m * (T_kelvin - b5)) [Pa]
         C_tait   = 0.0894 (dimensionless universal polymer constant)
     Dynamic polymer melt compressibility beta(P, T):
         beta(P, T) = -(1.0 / v) * (dv / dP) = (C_tait * 1.0E5) / (v * (P_pascal + B(T))) [1/bar]
     Predicted volumetric contraction shrinkage during packing/cooling:
         S_vol(t) = [v(P_inj, T_inj) - v(P_cav, T_cav)] / v(P_inj, T_inj)
     The controller dynamically adapts the Stage 1-3 packing pressure setpoints to inject compensating mass
     into the cavity prior to bumper gate freeze-off, maintaining part volumetric density within +/- 0.15%.

  2. CLOSED-LOOP HYDRAULIC SERVO VALVE CONTROL & HIGH-SPEED ACCUMULATOR INJECTION ASSIST:
     Large-area thin-wall bumper injection demands volumetric filling rates exceeding 1,800 cm3/s at injection
     pressures up to 220 bar hyd (1,450 bar specific melt pressure). A high-response 4-way electro-hydraulic servo
     valve (natural frequency fn > 95 Hz) is coupled with a 150-liter nitrogen-precharged piston accumulator bank.
     Accumulator discharge proportioning is regulated via an auxiliary fast proportional cartridge valve.
     Hydraulic cylinder chamber pressures and flow dynamics follow the compressible continuity equation:
         (V_cyl / Beta_oil) * (dP_hyd / dt) = Q_servo + Q_accum - A_piston * (dz_screw / dt)

  3. BUMPLESS VELOCITY-TO-PRESSURE (V/P) TRANSFER POINT INFLECTION DETECTION:
     A sudden transition from screw velocity control to cavity holding pressure control introduces severe
     hydraulic shock waves, platen shudder, or bumper flashing if timing is imperfect.
     The system monitors four concurrent real-time criteria:
         Criterion 1: Screw stroke linear position threshold: z_screw <= rSet_VP_Position_mm
         Criterion 2: Multi-cavity piezoelectric melt sensor threshold: P_cavity >= rSet_VP_CavityPress_bar
         Criterion 3: Hydraulic pressure derivative surge: dP_hyd/dt >= 1,500 bar/s with deceleration d2z/dt2 < -4,500 mm/s2
         Criterion 4: Cavity melt front arrival derivative: dP_cavity/dt >= 2,500 bar/s
     Upon transfer triggering, the controller calculates the exact bumpless spool pre-position:
         u_hold_init = u_inj_current * (rSet_HoldPress_Stage1_bar / MAX(P_hyd_current, 10.0))
     Eliminating hydraulic pressure overshoot spikes and surface witness lines.

  4. 4-CORNER TIE-BAR STRAIN-GAUGE TONNAGE BALANCING & PLATEN PARALLELISM:
     A two-platen 1,200-ton clamping unit utilizes four large-diameter tie bars (diameter 240 mm, length 3,200 mm).
     Unequal mold thermal expansion or unbalanced multi-cavity injection causes asymmetrical mold breathing,
     leading to platen tilt, bumper parting line flash, and tie-bar fatigue cracking.
     Four triplicated strain-gauge bridge load cells measure individual tie-bar tonnages (W1, W2, W3, W4).
     Platen parallelism deflection differentials:
         Delta_delta_TB    = [(W1 + W2) - (W3 + W4)] / (2.0 * K_tiebar) [mm]
         Delta_delta_LR    = [(W1 + W3) - (W2 + W4)] / (2.0 * K_tiebar) [mm]
         Delta_delta_Twist = [(W1 + W4) - (W2 + W3)] / (2.0 * K_tiebar) [mm]
     The controller dynamically modulates four independent corner hydraulic proportional trim valves
     to enforce platen parallelism deviation |Delta_delta| < 0.05 mm across the entire injection and hold phase.

  5. 8x8 MULTIVARIABLE DISCRETE STATE-SPACE & RECEDING-HORIZON MPC CONTROLLER:
     State vector:
         x = [z_screw, v_screw, P_hyd, P_cav, P_acc, T_melt, Delta_F_tiebar, P_back]^T in R^8
     Actuator control vector:
         u = [u_inj_servo, u_accum_valve, u_backpress_valve, u_tiebar_trim]^T in R^4
     Discretized dynamic state propagation at Ts = 1 ms:
         x[k+1] = A * x[k] + B * u[k]
         y[k]   = C * x[k] + D * u[k]
     Receding-horizon quadratic cost functional minimization:
         J = sum_{i=0}^{Np} (x_{k+i}^T * Q * x_{k+i} + u_{k+i}^T * R * u_{k+i}) + x_{k+Np}^T * P * x_{k+Np}
========================================================================================================================
*)
"""
    parts.append(header)
    
    # -------------------------------------------------------------
    # VAR_INPUT DECLARATION
    # -------------------------------------------------------------
    var_input = """
VAR_INPUT
    (* ============================================================================================== *)
    (* SECTION 1: INJECTION AXIS TRANSDUCERS (2oo3 TRIPLE MODULAR REDUNDANCY)                        *)
    (* ============================================================================================== *)
    ZT_SCREW_POSITION_101A            : REAL := 380.000;  (* Injection Screw Stroke Optical Linear Scale Ch A [mm] *)
    ZT_SCREW_POSITION_101B            : REAL := 380.000;  (* Injection Screw Stroke Optical Linear Scale Ch B [mm] *)
    ZT_SCREW_POSITION_101C            : REAL := 380.000;  (* Injection Screw Stroke Optical Linear Scale Ch C [mm] *)

    PT_INJECTION_HYD_PRESSURE_102A    : REAL := 15.000;   (* Injection Cylinder Head Hydraulic Pressure Ch A [bar] *)
    PT_INJECTION_HYD_PRESSURE_102B    : REAL := 15.000;   (* Injection Cylinder Head Hydraulic Pressure Ch B [bar] *)
    PT_INJECTION_HYD_PRESSURE_102C    : REAL := 15.000;   (* Injection Cylinder Head Hydraulic Pressure Ch C [bar] *)

    ST_SCREW_ROTATION_RPM_103A        : REAL := 0.000;    (* Screw Hydraulic Drive Motor Tachometer Ch A [RPM] *)
    ST_SCREW_ROTATION_RPM_103B        : REAL := 0.000;    (* Screw Hydraulic Drive Motor Tachometer Ch B [RPM] *)
    ST_SCREW_ROTATION_RPM_103C        : REAL := 0.000;    (* Screw Hydraulic Drive Motor Tachometer Ch C [RPM] *)

    PT_MOLD_CAVITY_MELT_PRESS_201A    : REAL := 1.013;    (* Bumper Cavity Piezoelectric Melt Pressure Ch A [bar] *)
    PT_MOLD_CAVITY_MELT_PRESS_201B    : REAL := 1.013;    (* Bumper Cavity Piezoelectric Melt Pressure Ch B [bar] *)
    PT_MOLD_CAVITY_MELT_PRESS_201C    : REAL := 1.013;    (* Bumper Cavity Piezoelectric Melt Pressure Ch C [bar] *)

    TT_MELT_NOZZLE_INFRARED_202A      : REAL := 245.000;  (* Injection Nozzle Melt Stream Pyrometer Ch A [deg C] *)
    TT_MELT_NOZZLE_INFRARED_202B      : REAL := 245.000;  (* Injection Nozzle Melt Stream Pyrometer Ch B [deg C] *)
    TT_MELT_NOZZLE_INFRARED_202C      : REAL := 245.000;  (* Injection Nozzle Melt Stream Pyrometer Ch C [deg C] *)

    (* ============================================================================================== *)
    (* SECTION 2: CLAMPING & TIE-BAR STRAIN TRANSDUCERS (2oo3 TRIPLE MODULAR REDUNDANCY)              *)
    (* ============================================================================================== *)
    WT_TIEBAR_1_STRAIN_TONNAGE_301A   : REAL := 300.000;  (* Tie-Bar #1 Top-Operator Load Cell Ch A [ton] *)
    WT_TIEBAR_1_STRAIN_TONNAGE_301B   : REAL := 300.000;  (* Tie-Bar #1 Top-Operator Load Cell Ch B [ton] *)
    WT_TIEBAR_1_STRAIN_TONNAGE_301C   : REAL := 300.000;  (* Tie-Bar #1 Top-Operator Load Cell Ch C [ton] *)

    WT_TIEBAR_2_STRAIN_TONNAGE_302A   : REAL := 300.000;  (* Tie-Bar #2 Top-Non-Operator Load Cell Ch A [ton] *)
    WT_TIEBAR_2_STRAIN_TONNAGE_302B   : REAL := 300.000;  (* Tie-Bar #2 Top-Non-Operator Load Cell Ch B [ton] *)
    WT_TIEBAR_2_STRAIN_TONNAGE_302C   : REAL := 300.000;  (* Tie-Bar #2 Top-Non-Operator Load Cell Ch C [ton] *)

    WT_TIEBAR_3_STRAIN_TONNAGE_303A   : REAL := 300.000;  (* Tie-Bar #3 Bottom-Operator Load Cell Ch A [ton] *)
    WT_TIEBAR_3_STRAIN_TONNAGE_303B   : REAL := 300.000;  (* Tie-Bar #3 Bottom-Operator Load Cell Ch B [ton] *)
    WT_TIEBAR_3_STRAIN_TONNAGE_303C   : REAL := 300.000;  (* Tie-Bar #3 Bottom-Operator Load Cell Ch C [ton] *)

    WT_TIEBAR_4_STRAIN_TONNAGE_304A   : REAL := 300.000;  (* Tie-Bar #4 Bottom-Non-Operator Load Cell Ch A [ton] *)
    WT_TIEBAR_4_STRAIN_TONNAGE_304B   : REAL := 300.000;  (* Tie-Bar #4 Bottom-Non-Operator Load Cell Ch B [ton] *)
    WT_TIEBAR_4_STRAIN_TONNAGE_304C   : REAL := 300.000;  (* Tie-Bar #4 Bottom-Non-Operator Load Cell Ch C [ton] *)

    ZT_CLAMP_PLATEN_POSITION_305A     : REAL := 0.000;    (* Moving Platen Mold Clamping Optical Scale Ch A [mm] *)
    ZT_CLAMP_PLATEN_POSITION_305B     : REAL := 0.000;    (* Moving Platen Mold Clamping Optical Scale Ch B [mm] *)
    ZT_CLAMP_PLATEN_POSITION_305C     : REAL := 0.000;    (* Moving Platen Mold Clamping Optical Scale Ch C [mm] *)

    (* ============================================================================================== *)
    (* SECTION 3: 6-ZONE BARREL HEATING THERMOCOUPLES (2oo3 TRIPLE MODULAR REDUNDANCY)                *)
    (* ============================================================================================== *)
    TT_BARREL_ZONE1_TEMP_401A         : REAL := 195.000;  (* Barrel Zone 1 Feed Throat Thermocouple Ch A [deg C] *)
    TT_BARREL_ZONE1_TEMP_401B         : REAL := 195.000;  (* Barrel Zone 1 Feed Throat Thermocouple Ch B [deg C] *)
    TT_BARREL_ZONE1_TEMP_401C         : REAL := 195.000;  (* Barrel Zone 1 Feed Throat Thermocouple Ch C [deg C] *)

    TT_BARREL_ZONE2_TEMP_402A         : REAL := 215.000;  (* Barrel Zone 2 Compression Thermocouple Ch A [deg C] *)
    TT_BARREL_ZONE2_TEMP_402B         : REAL := 215.000;  (* Barrel Zone 2 Compression Thermocouple Ch B [deg C] *)
    TT_BARREL_ZONE2_TEMP_402C         : REAL := 215.000;  (* Barrel Zone 2 Compression Thermocouple Ch C [deg C] *)

    TT_BARREL_ZONE3_TEMP_403A         : REAL := 230.000;  (* Barrel Zone 3 Metering Transition Ch A [deg C] *)
    TT_BARREL_ZONE3_TEMP_403B         : REAL := 230.000;  (* Barrel Zone 3 Metering Transition Ch B [deg C] *)
    TT_BARREL_ZONE3_TEMP_403C         : REAL := 230.000;  (* Barrel Zone 3 Metering Transition Ch C [deg C] *)

    TT_BARREL_ZONE4_TEMP_404A         : REAL := 240.000;  (* Barrel Zone 4 Metering Center Ch A [deg C] *)
    TT_BARREL_ZONE4_TEMP_404B         : REAL := 240.000;  (* Barrel Zone 4 Metering Center Ch B [deg C] *)
    TT_BARREL_ZONE4_TEMP_404C         : REAL := 240.000;  (* Barrel Zone 4 Metering Center Ch C [deg C] *)

    TT_BARREL_ZONE5_TEMP_405A         : REAL := 245.000;  (* Barrel Zone 5 Metering Front Ch A [deg C] *)
    TT_BARREL_ZONE5_TEMP_405B         : REAL := 245.000;  (* Barrel Zone 5 Metering Front Ch B [deg C] *)
    TT_BARREL_ZONE5_TEMP_405C         : REAL := 245.000;  (* Barrel Zone 5 Metering Front Ch C [deg C] *)

    TT_BARREL_ZONE6_TEMP_406A         : REAL := 250.000;  (* Barrel Zone 6 Nozzle Adapter Thermocouple Ch A [deg C] *)
    TT_BARREL_ZONE6_TEMP_406B         : REAL := 250.000;  (* Barrel Zone 6 Nozzle Adapter Thermocouple Ch B [deg C] *)
    TT_BARREL_ZONE6_TEMP_406C         : REAL := 250.000;  (* Barrel Zone 6 Nozzle Adapter Thermocouple Ch C [deg C] *)

    (* ============================================================================================== *)
    (* SECTION 4: AUXILIARY HYDRAULIC & EJECTOR TRANSDUCERS (2oo3 TRIPLE MODULAR REDUNDANCY)          *)
    (* ============================================================================================== *)
    PT_ACCUMULATOR_N2_PRECHARGE_501A  : REAL := 210.000;  (* Injection N2 Accumulator Pressure Ch A [bar] *)
    PT_ACCUMULATOR_N2_PRECHARGE_501B  : REAL := 210.000;  (* Injection N2 Accumulator Pressure Ch B [bar] *)
    PT_ACCUMULATOR_N2_PRECHARGE_501C  : REAL := 210.000;  (* Injection N2 Accumulator Pressure Ch C [bar] *)

    ZT_EJECTOR_PULSE_POS_601A         : REAL := 0.000;    (* Hydraulic Ejector Plate LVDT Scale Ch A [mm] *)
    ZT_EJECTOR_PULSE_POS_601B         : REAL := 0.000;    (* Hydraulic Ejector Plate LVDT Scale Ch B [mm] *)
    ZT_EJECTOR_PULSE_POS_601C         : REAL := 0.000;    (* Hydraulic Ejector Plate LVDT Scale Ch C [mm] *)

    TT_HYD_OIL_RESERVOIR_502A         : REAL := 45.000;   (* Main Hydraulic Reservoir Oil Temperature Ch A [deg C] *)
    TT_HYD_OIL_RESERVOIR_502B         : REAL := 45.000;   (* Main Hydraulic Reservoir Oil Temperature Ch B [deg C] *)
    TT_HYD_OIL_RESERVOIR_502C         : REAL := 45.000;   (* Main Hydraulic Reservoir Oil Temperature Ch C [deg C] *)

    PT_SYSTEM_PUMP_SUPPLY_503A        : REAL := 240.000;  (* Main Hydraulic Supply Rail Pressure Ch A [bar] *)
    PT_SYSTEM_PUMP_SUPPLY_503B        : REAL := 240.000;  (* Main Hydraulic Supply Rail Pressure Ch B [bar] *)
    PT_SYSTEM_PUMP_SUPPLY_503C        : REAL := 240.000;  (* Main Hydraulic Supply Rail Pressure Ch C [bar] *)

    (* ============================================================================================== *)
    (* SECTION 5: DISCRETE MACHINE COMMANDS & HARDWARE SAFETY INTERLOCKS                              *)
    (* ============================================================================================== *)
    bMasterStart                      : BOOL := FALSE;    (* Operator Master Automatic Cycle Start Request *)
    bAutoCycleEnable                  : BOOL := FALSE;    (* IMM Global Automatic Production Mode Permissive *)
    bEmergencyStop_CH1                : BOOL := TRUE;     (* Dual-Channel Hardwired E-Stop Relay Channel 1 OK *)
    bEmergencyStop_CH2                : BOOL := TRUE;     (* Dual-Channel Hardwired E-Stop Relay Channel 2 OK *)
    bSafetyGateClosed_CH1             : BOOL := TRUE;     (* Operator Mold Area Safety Gate Cat 4 / PL e Switch 1 *)
    bSafetyGateClosed_CH2             : BOOL := TRUE;     (* Operator Mold Area Safety Gate Cat 4 / PL e Switch 2 *)
    bRobotTakeoutPermissive           : BOOL := TRUE;     (* Bumper Extraction 6-Axis Robot Ready Interlock *)
    bRobotArmClearMoldArea            : BOOL := TRUE;     (* Robot Gripper Flange Confirmed Outside Mold Platen Space *)
    bPurgeModeSelect                  : BOOL := FALSE;    (* Manual/Automatic Barrel Purge Routine Active *)
    bAlarmAcknowledge                 : BOOL := FALSE;    (* Fault Latch Reset / Alarm Acknowledge Pushbutton *)

    (* ============================================================================================== *)
    (* SECTION 6: RECIPE PARAMETERS & PROCESS SETPOINTS                                               *)
    (* ============================================================================================== *)
    rSet_ShotSize_mm                  : REAL := 380.000;  (* Recipe Plasticizing Shot Stroke Setpoint [mm] *)
    rSet_CushionTarget_mm             : REAL := 22.000;   (* Final Expected Residual Melt Cushion [mm] *)
    rSet_InjVel_Stage1_mms            : REAL := 85.000;   (* Injection Velocity Stage 1 (Gate Entry) [mm/s] *)
    rSet_InjVel_Stage2_mms            : REAL := 155.000;  (* Injection Velocity Stage 2 (Fast Main Cavity) [mm/s] *)
    rSet_InjVel_Stage3_mms            : REAL := 95.000;   (* Injection Velocity Stage 3 (End of Cavity) [mm/s] *)
    rSet_InjStroke_Stage1_mm          : REAL := 280.000;  (* Transition Stroke from Stage 1 to Stage 2 [mm] *)
    rSet_InjStroke_Stage2_mm          : REAL := 80.000;   (* Transition Stroke from Stage 2 to Stage 3 [mm] *)
    rSet_VP_Position_mm               : REAL := 38.000;   (* Velocity-to-Pressure Transfer Stroke Threshold [mm] *)
    rSet_VP_CavityPress_bar           : REAL := 420.000;  (* Velocity-to-Pressure Cavity Melt Pressure Threshold [bar] *)
    rSet_VP_HydPressDeriv_bars        : REAL := 1500.00;  (* V/P Hydraulic Pressure Derivative Trigger [bar/s] *)
    iSet_VP_Mode                      : INT  := 4;        (* V/P Mode: 1=Position, 2=Cavity Press, 3=Hyd Deriv, 4=Hybrid *)
    rSet_HoldPress_Stage1_bar         : REAL := 130.000;  (* Holding Pressure Profile Stage 1 (Initial Packing) [bar hyd] *)
    rSet_HoldPress_Stage2_bar         : REAL := 105.000;  (* Holding Pressure Profile Stage 2 (Shrinkage Comp) [bar hyd] *)
    rSet_HoldPress_Stage3_bar         : REAL := 75.000;   (* Holding Pressure Profile Stage 3 (Gate Freeze-off) [bar hyd] *)
    tSet_HoldTime_Stage1_s            : REAL := 4.500;    (* Stage 1 Holding Pressure Duration [s] *)
    tSet_HoldTime_Stage2_s            : REAL := 6.500;    (* Stage 2 Holding Pressure Duration [s] *)
    tSet_HoldTime_Stage3_s            : REAL := 5.000;    (* Stage 3 Holding Pressure Duration [s] *)
    rSet_CoolingTime_s                : REAL := 22.000;   (* In-Mold Bumper Part Solidification Cooling Time [s] *)
    rSet_RecoveryRPM                  : REAL := 65.000;   (* Screw Recovery Plasticizing Rotation Speed [RPM] *)
    rSet_BackPressure_bar             : REAL := 18.500;   (* Closed-Loop Plasticizing Hydraulic Backpressure [bar] *)
    rSet_SuckBack_mm                  : REAL := 12.000;   (* Decompression Suck-Back Stroke [mm] *)
    rSet_TargetTonnage_ton            : REAL := 1200.00;  (* Full Clamping Target Tonnage [metric tons] *)
    rSet_MoldOpenStroke_mm            : REAL := 1450.00;  (* Moving Platen Daylight Open Position Target [mm] *)
    rSet_BarrelTemp_Zone1_degC        : REAL := 195.000;  (* Temperature Setpoint Zone 1 Feed [deg C] *)
    rSet_BarrelTemp_Zone2_degC        : REAL := 215.000;  (* Temperature Setpoint Zone 2 Compression [deg C] *)
    rSet_BarrelTemp_Zone3_degC        : REAL := 230.000;  (* Temperature Setpoint Zone 3 Metering 1 [deg C] *)
    rSet_BarrelTemp_Zone4_degC        : REAL := 240.000;  (* Temperature Setpoint Zone 4 Metering 2 [deg C] *)
    rSet_BarrelTemp_Zone5_degC        : REAL := 245.000;  (* Temperature Setpoint Zone 5 Metering 3 [deg C] *)
    rSet_BarrelTemp_Zone6_degC        : REAL := 250.000;  (* Temperature Setpoint Zone 6 Nozzle [deg C] *)
    iSet_EjectorPulseCount            : INT  := 3;        (* Ejector Multi-Pulse De-Molding Stroke Cycles *)
    rSet_EjectorForwardPos_mm         : REAL := 175.000;  (* Ejector Stroke Forward Extended Limit [mm] *)
    rSet_EjectorRetractPos_mm         : REAL := 5.000;    (* Ejector Stroke Retracted Limit [mm] *)
END_VAR
"""
    parts.append(var_input)

    # -------------------------------------------------------------
    # VAR_OUTPUT DECLARATION
    # -------------------------------------------------------------
    var_output = """
VAR_OUTPUT
    (* ============================================================================================== *)
    (* SECTION 1: ELECTRO-HYDRAULIC ACTUATOR & SERVO OUTPUT COMMANDS                                  *)
    (* ============================================================================================== *)
    rOut_InjServoValve_Pct            : REAL := 0.000;    (* Main Injection Servo Valve Spool Command [-100.0% to +100.0%] *)
    rOut_AccumulatorDischarge_Pct     : REAL := 0.000;    (* N2 High-Speed Assist Proportional Cartridge Valve [0.0% to 100.0%] *)
    rOut_ScrewMotorDisplacement_Pct   : REAL := 0.000;    (* Hydraulic Recovery Motor Variable Swashplate Command [0.0% to 100.0%] *)
    rOut_ProportionalBackpress_bar    : REAL := 0.000;    (* Proportional Backpressure Relief Valve Command [0.0 to 45.0 bar] *)
    rOut_ClampMainProportional_Pct    : REAL := 0.000;    (* Platen Main Tonnage Cylinder Servo Valve Command [0.0% to 100.0%] *)
    rOut_TieBarTrimValve1_Pct         : REAL := 0.000;    (* Tie-Bar 1 Top-Operator Pressure Trim Valve [-50.0% to +50.0%] *)
    rOut_TieBarTrimValve2_Pct         : REAL := 0.000;    (* Tie-Bar 2 Top-Non-Operator Pressure Trim Valve [-50.0% to +50.0%] *)
    rOut_TieBarTrimValve3_Pct         : REAL := 0.000;    (* Tie-Bar 3 Bottom-Operator Pressure Trim Valve [-50.0% to +50.0%] *)
    rOut_TieBarTrimValve4_Pct         : REAL := 0.000;    (* Tie-Bar 4 Bottom-Non-Operator Pressure Trim Valve [-50.0% to +50.0%] *)
    rOut_EjectorServoValve_Pct        : REAL := 0.000;    (* Hydraulic Multi-Pulse Ejector Proportional Valve [-100.0% to +100.0%] *)

    (* ============================================================================================== *)
    (* SECTION 2: 6-ZONE BARREL CERAMIC HEATING PWM & BLOWER OUTPUTS                                  *)
    (* ============================================================================================== *)
    rOut_BarrelZone1_PWM_Pct          : REAL := 0.000;    (* Zone 1 Feed Throat Ceramic Band PWM Duty Cycle [0.0% to 100.0%] *)
    rOut_BarrelZone2_PWM_Pct          : REAL := 0.000;    (* Zone 2 Compression Ceramic Band PWM Duty Cycle [0.0% to 100.0%] *)
    rOut_BarrelZone3_PWM_Pct          : REAL := 0.000;    (* Zone 3 Metering 1 Ceramic Band PWM Duty Cycle [0.0% to 100.0%] *)
    rOut_BarrelZone4_PWM_Pct          : REAL := 0.000;    (* Zone 4 Metering 2 Ceramic Band PWM Duty Cycle [0.0% to 100.0%] *)
    rOut_BarrelZone5_PWM_Pct          : REAL := 0.000;    (* Zone 5 Metering 3 Ceramic Band PWM Duty Cycle [0.0% to 100.0%] *)
    rOut_BarrelZone6_PWM_Pct          : REAL := 0.000;    (* Zone 6 Nozzle Ceramic Band PWM Duty Cycle [0.0% to 100.0%] *)
    bOut_BarrelCoolingFan1            : BOOL := FALSE;    (* Zone 1 Air Cooling Blower Contactor Relay *)
    bOut_BarrelCoolingFan2            : BOOL := FALSE;    (* Zone 2 Air Cooling Blower Contactor Relay *)
    bOut_BarrelCoolingFan3            : BOOL := FALSE;    (* Zone 3 Air Cooling Blower Contactor Relay *)
    bOut_BarrelCoolingFan4            : BOOL := FALSE;    (* Zone 4 Air Cooling Blower Contactor Relay *)
    bOut_BarrelCoolingFan5            : BOOL := FALSE;    (* Zone 5 Air Cooling Blower Contactor Relay *)
    bOut_BarrelCoolingFan6            : BOOL := FALSE;    (* Zone 6 Air Cooling Blower Contactor Relay *)

    (* ============================================================================================== *)
    (* SECTION 3: CYBER-PHYSICAL STATE ESTIMATORS & PROCESS METRICS                                   *)
    (* ============================================================================================== *)
    rEst_PolymerSpecificVolume_cm3g   : REAL := 0.000;    (* Modified Tait PVT Polymer Specific Volume [cm3/g] *)
    rEst_PolymerCompressibility_1bar  : REAL := 0.000;    (* Real-Time Polymer Melt Isothermal Compressibility [1/bar] *)
    rEst_VolumetricShrinkage_Pct      : REAL := 0.000;    (* Estimated In-Mold Volumetric Contraction Shrinkage [%] *)
    rEst_CavityFillingRate_cm3s       : REAL := 0.000;    (* Instantaneous Polymer Melt Cavity Volumetric Inflow [cm3/s] *)
    rEst_TotalClampTonnage_ton        : REAL := 0.000;    (* Summed 4-Tiebar Hydraulic Clamping Tonnage [ton] *)
    rEst_PlatenTiltDifferential_mm    : REAL := 0.000;    (* Maximum Moving Platen Parallelism Deflection [mm] *)
    rEst_PlatenAngularTilt_mrad       : REAL := 0.000;    (* Platen Spatial Angular Deflection [milliradians] *)
    rEst_ScrewShearDissipation_kW     : REAL := 0.000;    (* Plasticizing Polymer Viscous Shear Heating Rate [kW] *)
    bEst_VP_TransferTriggered         : BOOL := FALSE;    (* V/P Transfer Point Latch Flag *)
    rEst_VP_TransferPosition_mm       : REAL := 0.000;    (* Screw Stroke Position at Exact V/P Transfer [mm] *)
    rEst_VP_TransferCavityPress_bar   : REAL := 0.000;    (* Cavity Melt Pressure at Exact V/P Transfer [bar] *)
    rEst_VP_TransferHydPress_bar      : REAL := 0.000;    (* Hydraulic Injection Pressure at Exact V/P Transfer [bar] *)
    rEst_MeasuredCushion_mm           : REAL := 0.000;    (* Actual Measured Residual Polymer Cushion [mm] *)
    rEst_CycleTime_s                  : REAL := 0.000;    (* Total Recorded Bumper Molding Cycle Duration [s] *)

    (* ============================================================================================== *)
    (* SECTION 4: ISA-18.2 ALARMS, DIAGNOSTICS & FSM STATUS                                           *)
    (* ============================================================================================== *)
    dwAlarmWord1_ISA                  : DWORD := 16#00000000; (* ISA-18.2 Process Trip Alarm Register 1 *)
    dwAlarmWord2_ISA                  : DWORD := 16#00000000; (* ISA-18.2 Warning & Deviation Alarm Register 2 *)
    dwDiagnostics_TMR                 : DWORD := 16#00000000; (* 2oo3 Sensor Triplet Degradation Bitmask *)
    dwFSM_StatusWord                  : DWORD := 16#00000000; (* Operational State Machine Status & Interlock Word *)
    iCurrentState                     : INT   := 0;           (* Current Active Operational State (0 to 11) *)
    bCycleCompletedPulse              : BOOL  := FALSE;       (* Single-Scan Pulse Indicating Completed Good Part *)
    bMachineInSafeStop                : BOOL  := FALSE;       (* IMM Safe Hydraulic Dump / E-Stop Active *)
    bAlarmTripActive                  : BOOL  := FALSE;       (* Master Unacknowledged ISA-18.2 Critical Trip Alarm *)
END_VAR
"""
    parts.append(var_output)

    # -------------------------------------------------------------
    # VAR INTERNAL DECLARATION
    # -------------------------------------------------------------
    var_internal = """
VAR
    (* ============================================================================================== *)
    (* SECTION 1: CYBER-PHYSICAL MODEL CONSTANTS & TAIT COEFFICIENTS                                  *)
    (* ============================================================================================== *)
    bInitialized                      : BOOL := FALSE;    (* Cold Start Initialization Latch *)
    c_Ts_Injection                    : REAL := 0.001;    (* Fast Controller Discretization Sample Period [s] *)
    c_ScrewDiameter_mm                : REAL := 130.000;  (* Injection Unit Screw Outer Diameter [mm] *)
    c_ScrewFlightDepth_mm             : REAL := 8.500;    (* Metering Section Channel Flight Depth [mm] *)
    c_TieBarStiffness_tonmm           : REAL := 2970.000; (* Equivalent Longitudinal Axial Stiffness K_tb [ton/mm] *)
    c_PlatenSpanWidth_mm              : REAL := 2400.000; (* Moving Platen Tie-Bar Horizontal Spacing [mm] *)
    c_PlatenSpanHeight_mm             : REAL := 2100.000; (* Moving Platen Tie-Bar Vertical Spacing [mm] *)
    c_Tait_b1m                        : REAL := 0.001152; (* Tait Zero-Pressure Specific Volume Intercept b1m [m3/kg] *)
    c_Tait_b2m                        : REAL := 8.90E-07; (* Tait Specific Volume Temperature Slope b2m [m3/(kg*K)] *)
    c_Tait_b3m                        : REAL := 1.82E+08; (* Tait Pressure Sensitivity Scale Factor b3m [Pa] *)
    c_Tait_b4m                        : REAL := 0.004600; (* Tait Temperature Sensitivity Exponent b4m [1/K] *)
    c_Tait_b5                         : REAL := 473.1500; (* Tait Reference Melt Transition Temperature b5 [K] *)
    c_Tait_C                          : REAL := 0.089400; (* Universal Dimensionless Constant C_tait *)
    c_PolymerMeltZeroViscosity_Pals   : REAL := 1250.000; (* Zero-Shear Polypropylene Melt Viscosity eta0 [Pa*s] *)

    (* ============================================================================================== *)
    (* SECTION 2: 8x8 DISCRETE STATE-SPACE MATRICES & VECTORS (Ts = 1 ms)                             *)
    (* ============================================================================================== *)
    matA                              : ARRAY [0..7, 0..7] OF REAL; (* State Transition Matrix A (8x8) *)
    matB                              : ARRAY [0..7, 0..3] OF REAL; (* Control Input Matrix B (8x4) *)
    matC                              : ARRAY [0..7, 0..7] OF REAL; (* State Observation Matrix C (8x8) *)
    matD                              : ARRAY [0..7, 0..3] OF REAL; (* Direct Feedthrough Matrix D (8x4) *)

    vecX                              : ARRAY [0..7] OF REAL;       (* Current State Vector x[k] *)
    vecX_pred                         : ARRAY [0..7] OF REAL;       (* One-Step Ahead State Prediction x[k+1] *)
    vecX_ref                          : ARRAY [0..7] OF REAL;       (* Reference State Setpoint Vector x_ref *)
    vecErr                            : ARRAY [0..7] OF REAL;       (* State Error Vector e[k] = x_ref - x[k] *)
    vecU                              : ARRAY [0..3] OF REAL;       (* Current Actuator Control Vector u[k] *)
    vecDeltaU                         : ARRAY [0..3] OF REAL;       (* Incremental MPC Control Update delta_u[k] *)
    vecU_prev                         : ARRAY [0..3] OF REAL;       (* Previous Scan Actuator Control Vector *)

    (* MPC Quadratic Cost Functional Penalty Matrices *)
    matQ                              : ARRAY [0..7, 0..7] OF REAL; (* State Error Penalty Matrix Q (8x8) *)
    matR                              : ARRAY [0..3, 0..3] OF REAL; (* Control Action Penalty Matrix R (4x4) *)
    matP                              : ARRAY [0..7, 0..7] OF REAL; (* Terminal State Penalty Matrix P (8x8) *)
    matK_mpc                          : ARRAY [0..3, 0..7] OF REAL; (* Receding-Horizon Optimal Feedback Gain K *)

    (* ============================================================================================== *)
    (* SECTION 3: 2oo3 TMR DISCREPANCY ACCUMULATORS, TOLERANCES & VOTED REGISTERS                     *)
    (* ============================================================================================== *)
"""
    parts.append(var_internal)

    # Generate 18 sensor triplets declarations
    triplet_configs = [
        ("ZT_SCREW_POSITION_101", "ScrewPos_mm", "REAL", "0.800", "50", "380.0"),
        ("PT_INJECTION_HYD_PRESSURE_102", "HydPress_bar", "REAL", "3.500", "40", "15.0"),
        ("ST_SCREW_ROTATION_RPM_103", "ScrewRPM", "REAL", "2.000", "60", "0.0"),
        ("PT_MOLD_CAVITY_MELT_PRESS_201", "CavityMeltPress_bar", "REAL", "15.000", "30", "1.0"),
        ("TT_MELT_NOZZLE_INFRARED_202", "NozzleTemp_degC", "REAL", "3.000", "80", "245.0"),
        ("WT_TIEBAR_1_STRAIN_TONNAGE_301", "Tiebar1_ton", "REAL", "12.000", "50", "300.0"),
        ("WT_TIEBAR_2_STRAIN_TONNAGE_302", "Tiebar2_ton", "REAL", "12.000", "50", "300.0"),
        ("WT_TIEBAR_3_STRAIN_TONNAGE_303", "Tiebar3_ton", "REAL", "12.000", "50", "300.0"),
        ("WT_TIEBAR_4_STRAIN_TONNAGE_304", "Tiebar4_ton", "REAL", "12.000", "50", "300.0"),
        ("ZT_CLAMP_PLATEN_POSITION_305", "PlatenPos_mm", "REAL", "1.500", "50", "0.0"),
        ("TT_BARREL_ZONE1_TEMP_401", "Zone1Temp_degC", "REAL", "2.500", "100", "195.0"),
        ("TT_BARREL_ZONE2_TEMP_402", "Zone2Temp_degC", "REAL", "2.500", "100", "215.0"),
        ("TT_BARREL_ZONE3_TEMP_403", "Zone3Temp_degC", "REAL", "2.500", "100", "230.0"),
        ("TT_BARREL_ZONE4_TEMP_404", "Zone4Temp_degC", "REAL", "2.500", "100", "240.0"),
        ("TT_BARREL_ZONE5_TEMP_405", "Zone5Temp_degC", "REAL", "2.500", "100", "245.0"),
        ("TT_BARREL_ZONE6_TEMP_406", "Zone6Temp_degC", "REAL", "2.500", "100", "250.0"),
        ("PT_ACCUMULATOR_N2_PRECHARGE_501", "AccumPress_bar", "REAL", "4.000", "50", "210.0"),
        ("ZT_EJECTOR_PULSE_POS_601", "EjectorPos_mm", "REAL", "1.000", "40", "0.0"),
        ("TT_HYD_OIL_RESERVOIR_502", "OilTemp_degC", "REAL", "2.000", "50", "45.0"),
        ("PT_SYSTEM_PUMP_SUPPLY_503", "PumpSupplyPress_bar", "REAL", "5.000", "40", "240.0")
    ]

    tmr_vars = []
    for tag, voted_name, data_type, tol, pers, safe_def in triplet_configs:
        tmr_vars.append(f"""    (* 2oo3 TMR Variables for {tag} *)
    rDev_AB_{tag} : REAL := 0.0;
    rDev_BC_{tag} : REAL := 0.0;
    rDev_CA_{tag} : REAL := 0.0;
    udiAccum_AB_{tag} : UDINT := 0;
    udiAccum_BC_{tag} : UDINT := 0;
    udiAccum_CA_{tag} : UDINT := 0;
    bChA_OK_{tag} : BOOL := TRUE;
    bChB_OK_{tag} : BOOL := TRUE;
    bChC_OK_{tag} : BOOL := TRUE;
    bDiscrepancy_{tag} : BOOL := FALSE;
    iHealth_{tag} : INT := 3;
    rVoted_{voted_name} : {data_type} := {safe_def};
    c_tol_{tag} : REAL := {tol};
    c_pLimit_{tag} : UDINT := {pers};
    c_safe_{tag} : REAL := {safe_def};
""")
    parts.append("".join(tmr_vars))

    # Internal Section 4: Derivative Filters, Observers, PID variables, FSM variables
    var_internal_rest = """
    (* ============================================================================================== *)
    (* SECTION 4: DERIVATIVE FILTERS, KINEMATIC OBSERVERS & PVT REGISTERS                            *)
    (* ============================================================================================== *)
    rPrev_ScrewPos_mm                 : REAL := 380.000;
    rPrev_ScrewVel_mms                : REAL := 0.000;
    rPrev_ScrewAcc_mms2               : REAL := 0.000;
    rFilt_ScrewVel_mms                : REAL := 0.000;
    rFilt_ScrewAcc_mms2               : REAL := 0.000;
    rPrev_HydPress_bar                : REAL := 15.000;
    rPrev_CavityMeltPress_bar         : REAL := 1.013;
    rFilt_HydPressDeriv_bars          : REAL := 0.000;
    rFilt_CavPressDeriv_bars          : REAL := 0.000;
    rAlpha_FilterVel                  : REAL := 0.250;
    rAlpha_FilterAcc                  : REAL := 0.200;
    rAlpha_FilterDeriv                : REAL := 0.300;

    (* Tait PVT Calculation Scratchpad *)
    rTait_TempKelvin                  : REAL := 518.150;
    rTait_PressPascal                 : REAL := 101325.0;
    rTait_V0                          : REAL := 0.001192;
    rTait_B                           : REAL := 147800000.0;
    rTait_SpecificVolume_m3kg         : REAL := 0.001150;
    rTait_SpecificVolume_Ambient      : REAL := 0.001085;
    rTait_VolumetricRatio             : REAL := 1.000;

    (* Platen Parallelism & Tie-Bar Balance Registers *)
    rDiff_TieBar_TB_ton               : REAL := 0.000;
    rDiff_TieBar_LR_ton               : REAL := 0.000;
    rDiff_TieBar_Diag_ton             : REAL := 0.000;
    rDeflect_TB_mm                    : REAL := 0.000;
    rDeflect_LR_mm                    : REAL := 0.000;
    rMaxPlatenDeflection_mm           : REAL := 0.000;
    rGain_TieBarTrim                  : REAL := 0.045;

    (* Barrel Thermal Decoupling & PID Accumulators *)
    rZone1_IntegralSum                : REAL := 0.000;
    rZone2_IntegralSum                : REAL := 0.000;
    rZone3_IntegralSum                : REAL := 0.000;
    rZone4_IntegralSum                : REAL := 0.000;
    rZone5_IntegralSum                : REAL := 0.000;
    rZone6_IntegralSum                : REAL := 0.000;
    rZone1_PrevError                  : REAL := 0.000;
    rZone2_PrevError                  : REAL := 0.000;
    rZone3_PrevError                  : REAL := 0.000;
    rZone4_PrevError                  : REAL := 0.000;
    rZone5_PrevError                  : REAL := 0.000;
    rZone6_PrevError                  : REAL := 0.000;
    rThermal_CouplingConductance      : REAL := 0.018;

    (* ============================================================================================== *)
    (* SECTION 5: 12-STAGE OPERATIONAL FSM STEP TIMERS, FLAGS & COUNTERS                              *)
    (* ============================================================================================== *)
    iState                            : INT   := 0;
    iNextState                        : INT   := 0;
    udiStateStep                      : UDINT := 0;
    udiCycleTime_ms                   : UDINT := 0;
    udiHoldTimer_ms                   : UDINT := 0;
    udiCoolingTimer_ms                : UDINT := 0;
    udiSoakTimer_ms                   : UDINT := 0;
    udiEjectorTimer_ms                : UDINT := 0;
    iEjectorCurrentPulse              : INT   := 0;
    bEjectorForwardPhase              : BOOL  := FALSE;
    bTMR_AnyDiscrepancyTrip           : BOOL  := FALSE;
    bFault_TMR_Trip                   : BOOL  := FALSE;
    bSafetyCircuitBreached            : BOOL  := FALSE;
    bColdScrewInterlockActive         : BOOL  := TRUE;

    (* V/P Bumpless Transfer Scratchpad *)
    bVP_Pos_Trigger                   : BOOL  := FALSE;
    bVP_CavPress_Trigger              : BOOL  := FALSE;
    bVP_HydDeriv_Trigger              : BOOL  := FALSE;
    bVP_CavDeriv_Trigger              : BOOL  := FALSE;
    bVP_ConditionMet                  : BOOL  := FALSE;
    rBumplessHoldSpoolBias            : REAL  := 0.000;

    (* ============================================================================================== *)
    (* SECTION 6: ISA-18.2 FIVE-TIER ALARM TRIP THRESHOLDS & STATUS MASKS                             *)
    (* ============================================================================================== *)
    c_Trip_HydPress_HI_HI_bar         : REAL := 240.000;
    c_Warn_HydPress_HI_bar            : REAL := 220.000;
    c_Trip_CavityPress_HI_HI_bar      : REAL := 1350.00;
    c_Warn_CavityPress_HI_bar         : REAL := 1150.00;
    c_Trip_ClampTonnage_HI_HI_ton     : REAL := 1350.00;
    c_Warn_ClampTonnage_HI_ton        : REAL := 1280.00;
    c_Trip_PlatenTilt_HI_HI_mm        : REAL := 0.080;
    c_Warn_PlatenTilt_HI_mm           : REAL := 0.050;
    c_Trip_AccumPress_LO_LO_bar       : REAL := 165.000;
    c_Warn_AccumPress_LO_bar          : REAL := 185.000;
    c_Trip_OilTemp_HI_HI_degC         : REAL := 62.000;
    c_Warn_OilTemp_HI_degC            : REAL := 55.000;
    c_Trip_BarrelTemp_Dev_degC        : REAL := 35.000;
    c_Deadband_Pressure_bar           : REAL := 4.000;
    c_Deadband_Temp_degC              : REAL := 2.000;

    (* Latched ISA-18.2 Alarm Flags *)
    bAlarm_HydPress_HI_HI             : BOOL := FALSE;
    bAlarm_HydPress_HI                : BOOL := FALSE;
    bAlarm_CavityPress_HI_HI          : BOOL := FALSE;
    bAlarm_CavityPress_HI             : BOOL := FALSE;
    bAlarm_ClampTonnage_HI_HI         : BOOL := FALSE;
    bAlarm_ClampTonnage_HI            : BOOL := FALSE;
    bAlarm_PlatenTilt_HI_HI           : BOOL := FALSE;
    bAlarm_PlatenTilt_HI              : BOOL := FALSE;
    bAlarm_AccumPress_LO_LO           : BOOL := FALSE;
    bAlarm_AccumPress_LO              : BOOL := FALSE;
    bAlarm_OilTemp_HI_HI              : BOOL := FALSE;
    bAlarm_OilTemp_HI                 : BOOL := FALSE;
    bAlarm_SafetyGateBreached         : BOOL := FALSE;
    bAlarm_EstopTripped               : BOOL := FALSE;
    bAlarm_ColdScrewBlocked           : BOOL := FALSE;
    bAlarm_CycleTimeout               : BOOL := FALSE;

    (* Loop and Scratch Iterators *)
    iRow                              : INT := 0;
    iCol                              : INT := 0;
    rMatAccum                         : REAL := 0.0;
    rSlewRateLimit                    : REAL := 0.0;
    rControlDelta                     : REAL := 0.0;
END_VAR
"""
    parts.append(var_internal_rest)

    # -------------------------------------------------------------
    # PHASE 0: MODEL MATRICES & CONTROL INITIALIZATION
    # -------------------------------------------------------------
    phase0 = """
(* ==================================================================================================== *)
(* PHASE 0: MODEL MATRICES, CONTROL COEFFICIENTS & COLD START INITIALIZATION                            *)
(* ==================================================================================================== *)
IF NOT bInitialized THEN
    (* ------------------------------------------------------------------------------------------------ *)
    (* Initialize 8x8 Discrete State-Space Transition Matrix A (Ts = 0.001 s)                           *)
    (* States: 0:z_screw, 1:v_screw, 2:P_hyd, 3:P_cav, 4:P_acc, 5:T_melt, 6:Delta_F_tb, 7:P_back       *)
    (* ------------------------------------------------------------------------------------------------ *)
    FOR iRow := 0 TO 7 DO
        FOR iCol := 0 TO 7 DO
            matA[iRow, iCol] := 0.0;
            matC[iRow, iCol] := 0.0;
            matQ[iRow, iCol] := 0.0;
            matP[iRow, iCol] := 0.0;
        END_FOR;
        FOR iCol := 0 TO 3 DO
            matB[iRow, iCol] := 0.0;
            matD[iRow, iCol] := 0.0;
        END_FOR;
    END_FOR;

    FOR iRow := 0 TO 3 DO
        FOR iCol := 0 TO 3 DO
            matR[iRow, iCol] := 0.0;
        END_FOR;
        FOR iCol := 0 TO 7 DO
            matK_mpc[iRow, iCol] := 0.0;
        END_FOR;
    END_FOR;

    (* Continuous-to-discrete diagonal and cross-coupling coefficients for Matrix A *)
    matA[0, 0] := 1.000000;  matA[0, 1] := 0.001000;  matA[0, 2] := 0.000000;  matA[0, 3] := 0.000000;
    matA[0, 4] := 0.000000;  matA[0, 5] := 0.000000;  matA[0, 6] := 0.000000;  matA[0, 7] := 0.000000;

    matA[1, 0] := 0.000000;  matA[1, 1] := 0.985200;  matA[1, 2] := 0.003150;  matA[1, 3] := -0.000480;
    matA[1, 4] := 0.000850;  matA[1, 5] := 0.000120;  matA[1, 6] := 0.000000;  matA[1, 7] := -0.002800;

    matA[2, 0] := 0.000000;  matA[2, 1] := -0.012500; matA[2, 2] := 0.962000;  matA[2, 3] := 0.000850;
    matA[2, 4] := 0.018200;  matA[2, 5] := 0.000000;  matA[2, 6] := 0.000000;  matA[2, 7] := 0.000000;

    matA[3, 0] := 0.000000;  matA[3, 1] := 0.048500;  matA[3, 2] := 0.007200;  matA[3, 3] := 0.978500;
    matA[3, 4] := 0.000000;  matA[3, 5] := 0.002400;  matA[3, 6] := 0.000000;  matA[3, 7] := 0.000000;

    matA[4, 0] := 0.000000;  matA[4, 1] := 0.000000;  matA[4, 2] := -0.001800; matA[4, 3] := 0.000000;
    matA[4, 4] := 0.999100;  matA[4, 5] := 0.000000;  matA[4, 6] := 0.000000;  matA[4, 7] := 0.000000;

    matA[5, 0] := 0.000000;  matA[5, 1] := 0.000140;  matA[5, 2] := 0.000000;  matA[5, 3] := 0.000000;
    matA[5, 4] := 0.000000;  matA[5, 5] := 0.998800;  matA[5, 6] := 0.000000;  matA[5, 7] := 0.000280;

    matA[6, 0] := 0.000000;  matA[6, 1] := 0.000000;  matA[6, 2] := 0.002400;  matA[6, 3] := 0.018500;
    matA[6, 4] := 0.000000;  matA[6, 5] := 0.000000;  matA[6, 6] := 0.994500;  matA[6, 7] := 0.000000;

    matA[7, 0] := 0.000000;  matA[7, 1] := 0.000000;  matA[7, 2] := 0.000000;  matA[7, 3] := 0.000000;
    matA[7, 4] := 0.000000;  matA[7, 5] := 0.000000;  matA[7, 6] := 0.000000;  matA[7, 7] := 0.965000;

    (* ------------------------------------------------------------------------------------------------ *)
    (* Initialize 8x4 Control Input Coupling Matrix B                                                   *)
    (* Inputs: 0:u_inj_servo, 1:u_accum_valve, 2:u_backpress_valve, 3:u_tiebar_trim                     *)
    (* ------------------------------------------------------------------------------------------------ *)
    matB[0, 0] := 0.000000;  matB[0, 1] := 0.000000;  matB[0, 2] := 0.000000;  matB[0, 3] := 0.000000;
    matB[1, 0] := 0.024500;  matB[1, 1] := 0.016200;  matB[1, 2] := -0.008400; matB[1, 3] := 0.000000;
    matB[2, 0] := 0.088000;  matB[2, 1] := 0.045000;  matB[2, 2] := 0.000000;  matB[2, 3] := 0.000000;
    matB[3, 0] := 0.012500;  matB[3, 1] := 0.028000;  matB[3, 2] := 0.000000;  matB[3, 3] := 0.000000;
    matB[4, 0] := 0.000000;  matB[4, 1] := -0.038500; matB[4, 2] := 0.000000;  matB[4, 3] := 0.000000;
    matB[5, 0] := 0.000000;  matB[5, 1] := 0.000000;  matB[5, 2] := 0.001850;  matB[5, 3] := 0.000000;
    matB[6, 0] := 0.000000;  matB[6, 1] := 0.000000;  matB[6, 2] := 0.000000;  matB[6, 3] := -0.085000;
    matB[7, 0] := 0.000000;  matB[7, 1] := 0.000000;  matB[7, 2] := 0.075000;  matB[7, 3] := 0.000000;

    (* Observation Matrix C: Direct Identity Mapping *)
    FOR iRow := 0 TO 7 DO
        matC[iRow, iRow] := 1.0;
    END_FOR;

    (* Model Predictive Control (MPC) Quadratic Weight Matrices *)
    matQ[0, 0] := 15.000; (* Screw Position penalty *)
    matQ[1, 1] := 25.000; (* Screw Velocity penalty *)
    matQ[2, 2] := 8.500;  (* Hydraulic Injection Pressure penalty *)
    matQ[3, 3] := 35.000; (* Cavity Melt Pressure packing penalty *)
    matQ[4, 4] := 2.000;  (* Accumulator Pressure maintenance penalty *)
    matQ[5, 5] := 12.000; (* Nozzle Melt Temperature thermal penalty *)
    matQ[6, 6] := 45.000; (* Tie-bar Tonnage Imbalance severe penalty *)
    matQ[7, 7] := 18.000; (* Screw Plasticizing Backpressure penalty *)

    matR[0, 0] := 1.200;  (* Main Injection Servo spool energy penalty *)
    matR[1, 1] := 0.850;  (* Accumulator discharge throttle penalty *)
    matR[2, 2] := 1.500;  (* Proportional backpressure spool penalty *)
    matR[3, 3] := 3.200;  (* Corner tie-bar trim valve wear penalty *)

    FOR iRow := 0 TO 7 DO
        matP[iRow, iRow] := matQ[iRow, iRow] * 2.85; (* Terminal Lyapunov Riccati cost *)
    END_FOR;

    (* Optimal MPC Feedback Gain Matrix K_mpc (4x8) *)
    matK_mpc[0, 0] := 0.450;  matK_mpc[0, 1] := 0.820;  matK_mpc[0, 2] := 0.185;  matK_mpc[0, 3] := 0.350;
    matK_mpc[0, 4] := 0.045;  matK_mpc[0, 5] := 0.012;  matK_mpc[0, 6] := 0.000;  matK_mpc[0, 7] := 0.000;

    matK_mpc[1, 0] := 0.120;  matK_mpc[1, 1] := 0.480;  matK_mpc[1, 2] := 0.095;  matK_mpc[1, 3] := 0.050;
    matK_mpc[1, 4] := 0.280;  matK_mpc[1, 5] := 0.000;  matK_mpc[1, 6] := 0.000;  matK_mpc[1, 7] := 0.000;

    matK_mpc[2, 0] := 0.000;  matK_mpc[2, 1] := 0.000;  matK_mpc[2, 2] := 0.000;  matK_mpc[2, 3] := 0.000;
    matK_mpc[2, 4] := 0.000;  matK_mpc[2, 5] := 0.015;  matK_mpc[2, 6] := 0.000;  matK_mpc[2, 7] := 0.620;

    matK_mpc[3, 0] := 0.000;  matK_mpc[3, 1] := 0.000;  matK_mpc[3, 2] := 0.000;  matK_mpc[3, 3] := 0.085;
    matK_mpc[3, 4] := 0.000;  matK_mpc[3, 5] := 0.000;  matK_mpc[3, 6] := 1.250;  matK_mpc[3, 7] := 0.000;

    bInitialized := TRUE;
END_IF;
"""
    parts.append(phase0)

    # -------------------------------------------------------------
    # PHASE 1: 2oo3 TMR SENSOR VOTING ENGINES
    # -------------------------------------------------------------
    phase1_header = """
(* ==================================================================================================== *)
(* PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING ENGINES                                  *)
(* ==================================================================================================== *)
bTMR_AnyDiscrepancyTrip := FALSE;
"""
    parts.append(phase1_header)

    tmr_logic_blocks = []
    bit_index = 0
    for tag, voted_name, data_type, tol, pers, safe_def in triplet_configs:
        bit_mask = 1 << bit_index
        tmr_logic_blocks.append(f"""
(* --- 2oo3 TMR Engine: {tag} --- *)
rDev_AB_{tag} := ABS({tag}A - {tag}B);
rDev_BC_{tag} := ABS({tag}B - {tag}C);
rDev_CA_{tag} := ABS({tag}C - {tag}A);

IF (rDev_AB_{tag} > c_tol_{tag}) THEN
    IF (udiAccum_AB_{tag} < 65535) THEN
        udiAccum_AB_{tag} := udiAccum_AB_{tag} + 1;
    END_IF;
ELSE
    IF (udiAccum_AB_{tag} > 0) THEN
        udiAccum_AB_{tag} := udiAccum_AB_{tag} - 1;
    END_IF;
END_IF;

IF (rDev_BC_{tag} > c_tol_{tag}) THEN
    IF (udiAccum_BC_{tag} < 65535) THEN
        udiAccum_BC_{tag} := udiAccum_BC_{tag} + 1;
    END_IF;
ELSE
    IF (udiAccum_BC_{tag} > 0) THEN
        udiAccum_BC_{tag} := udiAccum_BC_{tag} - 1;
    END_IF;
END_IF;

IF (rDev_CA_{tag} > c_tol_{tag}) THEN
    IF (udiAccum_CA_{tag} < 65535) THEN
        udiAccum_CA_{tag} := udiAccum_CA_{tag} + 1;
    END_IF;
ELSE
    IF (udiAccum_CA_{tag} > 0) THEN
        udiAccum_CA_{tag} := udiAccum_CA_{tag} - 1;
    END_IF;
END_IF;

bChA_OK_{tag} := (udiAccum_AB_{tag} < c_pLimit_{tag}) OR (udiAccum_CA_{tag} < c_pLimit_{tag});
bChB_OK_{tag} := (udiAccum_AB_{tag} < c_pLimit_{tag}) OR (udiAccum_BC_{tag} < c_pLimit_{tag});
bChC_OK_{tag} := (udiAccum_BC_{tag} < c_pLimit_{tag}) OR (udiAccum_CA_{tag} < c_pLimit_{tag});

bDiscrepancy_{tag} := (udiAccum_AB_{tag} >= c_pLimit_{tag}) OR 
                      (udiAccum_BC_{tag} >= c_pLimit_{tag}) OR 
                      (udiAccum_CA_{tag} >= c_pLimit_{tag});

IF bDiscrepancy_{tag} THEN
    bTMR_AnyDiscrepancyTrip := TRUE;
    dwDiagnostics_TMR := dwDiagnostics_TMR OR 16#{bit_mask:08X};
ELSE
    dwDiagnostics_TMR := dwDiagnostics_TMR AND NOT 16#{bit_mask:08X};
END_IF;

(* Median Voting & Graceful Bumpless Degradation *)
IF (bChA_OK_{tag} AND bChB_OK_{tag} AND bChC_OK_{tag}) THEN
    IF (({tag}A >= {tag}B AND {tag}A <= {tag}C) OR ({tag}A <= {tag}B AND {tag}A >= {tag}C)) THEN
        rVoted_{voted_name} := {tag}A;
    ELSIF (({tag}B >= {tag}A AND {tag}B <= {tag}C) OR ({tag}B <= {tag}A AND {tag}B >= {tag}C)) THEN
        rVoted_{voted_name} := {tag}B;
    ELSE
        rVoted_{voted_name} := {tag}C;
    END_IF;
    iHealth_{tag} := 3;
ELSIF (bChA_OK_{tag} AND bChB_OK_{tag}) THEN
    rVoted_{voted_name} := ({tag}A + {tag}B) * 0.5;
    iHealth_{tag} := 2;
ELSIF (bChB_OK_{tag} AND bChC_OK_{tag}) THEN
    rVoted_{voted_name} := ({tag}B + {tag}C) * 0.5;
    iHealth_{tag} := 2;
ELSIF (bChA_OK_{tag} AND bChC_OK_{tag}) THEN
    rVoted_{voted_name} := ({tag}A + {tag}C) * 0.5;
    iHealth_{tag} := 2;
ELSIF (bChA_OK_{tag}) THEN
    rVoted_{voted_name} := {tag}A;
    iHealth_{tag} := 1;
ELSIF (bChB_OK_{tag}) THEN
    rVoted_{voted_name} := {tag}B;
    iHealth_{tag} := 1;
ELSIF (bChC_OK_{tag}) THEN
    rVoted_{voted_name} := {tag}C;
    iHealth_{tag} := 1;
ELSE
    rVoted_{voted_name} := c_safe_{tag};
    iHealth_{tag} := 0;
    bFault_TMR_Trip := TRUE;
END_IF;
""")
        bit_index += 1

    parts.append("".join(tmr_logic_blocks))

    # -------------------------------------------------------------
    # PHASE 2: CYBER-PHYSICAL PROPERTY ESTIMATION & DYNAMICS OBSERVERS
    # -------------------------------------------------------------
    phase2 = """
(* ==================================================================================================== *)
(* PHASE 2: REAL-TIME CYBER-PHYSICAL PROPERTY ESTIMATION & OBSERVERS                                    *)
(* ==================================================================================================== *)

(* 1. Kinematic Velocity and Acceleration Estimation with Butterworth Filter *)
IF c_Ts_Injection > 0.0 THEN
    rFilt_ScrewVel_mms := rAlpha_FilterVel * ((rVoted_ScrewPos_mm - rPrev_ScrewPos_mm) / c_Ts_Injection) + (1.0 - rAlpha_FilterVel) * rPrev_ScrewVel_mms;
    rFilt_ScrewAcc_mms2 := rAlpha_FilterAcc * ((rFilt_ScrewVel_mms - rPrev_ScrewVel_mms) / c_Ts_Injection) + (1.0 - rAlpha_FilterAcc) * rPrev_ScrewAcc_mms2;
    rFilt_HydPressDeriv_bars := rAlpha_FilterDeriv * ((rVoted_HydPress_bar - rPrev_HydPress_bar) / c_Ts_Injection) + (1.0 - rAlpha_FilterDeriv) * rFilt_HydPressDeriv_bars;
    rFilt_CavPressDeriv_bars := rAlpha_FilterDeriv * ((rVoted_CavityMeltPress_bar - rPrev_CavityMeltPress_bar) / c_Ts_Injection) + (1.0 - rAlpha_FilterDeriv) * rFilt_CavPressDeriv_bars;
END_IF;

rPrev_ScrewPos_mm := rVoted_ScrewPos_mm;
rPrev_ScrewVel_mms := rFilt_ScrewVel_mms;
rPrev_ScrewAcc_mms2 := rFilt_ScrewAcc_mms2;
rPrev_HydPress_bar := rVoted_HydPress_bar;
rPrev_CavityMeltPress_bar := rVoted_CavityMeltPress_bar;

(* Volumetric Melt Filling Rate [cm3/s] *)
rEst_CavityFillingRate_cm3s := (3.14159265 * (c_ScrewDiameter_mm * 0.5) * (c_ScrewDiameter_mm * 0.5) * ABS(rFilt_ScrewVel_mms)) * 0.001;

(* 2. Modified Tait Equation-of-State (PVT) for Automotive Bumper Polyolefin *)
rTait_TempKelvin := rVoted_NozzleTemp_degC + 273.15;
rTait_PressPascal := rVoted_CavityMeltPress_bar * 100000.0;
rTait_V0 := c_Tait_b1m + c_Tait_b2m * (rTait_TempKelvin - c_Tait_b5);

(* Safe Exponential Approximation for Tait B(T) Parameter *)
IF (rTait_TempKelvin - c_Tait_b5) < 80.0 AND (rTait_TempKelvin - c_Tait_b5) > -80.0 THEN
    rTait_B := c_Tait_b3m * (1.0 - c_Tait_b4m * (rTait_TempKelvin - c_Tait_b5) + 0.5 * (c_Tait_b4m * (rTait_TempKelvin - c_Tait_b5)) * (c_Tait_b4m * (rTait_TempKelvin - c_Tait_b5)));
ELSE
    rTait_B := c_Tait_b3m;
END_IF;

IF rTait_B < 1.0E+07 THEN
    rTait_B := 1.0E+07;
END_IF;

(* Specific Volume Calculation v(P, T) via Natural Log Series *)
rTait_VolumetricRatio := rTait_PressPascal / rTait_B;
IF rTait_VolumetricRatio > 0.001 THEN
    rTait_SpecificVolume_m3kg := rTait_V0 * (1.0 - c_Tait_C * (rTait_VolumetricRatio - 0.5 * rTait_VolumetricRatio * rTait_VolumetricRatio));
ELSE
    rTait_SpecificVolume_m3kg := rTait_V0;
END_IF;

rEst_PolymerSpecificVolume_cm3g := rTait_SpecificVolume_m3kg * 1000.0;

(* Real-Time Isothermal Melt Compressibility beta(P, T) [1/bar] *)
IF (rTait_SpecificVolume_m3kg > 0.0005) AND ((rTait_PressPascal + rTait_B) > 1.0E+06) THEN
    rEst_PolymerCompressibility_1bar := (c_Tait_C * 100000.0) / (rTait_SpecificVolume_m3kg * (rTait_PressPascal + rTait_B));
ELSE
    rEst_PolymerCompressibility_1bar := 0.000045;
END_IF;

(* Volumetric Shrinkage Prediction relative to Room Ambient Solid State *)
IF rTait_SpecificVolume_m3kg > 0.0008 THEN
    rEst_VolumetricShrinkage_Pct := ((rTait_SpecificVolume_m3kg - rTait_SpecificVolume_Ambient) / rTait_SpecificVolume_m3kg) * 100.0;
ELSE
    rEst_VolumetricShrinkage_Pct := 1.65;
END_IF;

(* 3. 4-Corner Tie-Bar Tonnage Balancing & Platen Parallelism Deflection *)
rEst_TotalClampTonnage_ton := rVoted_Tiebar1_ton + rVoted_Tiebar2_ton + rVoted_Tiebar3_ton + rVoted_Tiebar4_ton;
rDiff_TieBar_TB_ton := (rVoted_Tiebar1_ton + rVoted_Tiebar2_ton) - (rVoted_Tiebar3_ton + rVoted_Tiebar4_ton);
rDiff_TieBar_LR_ton := (rVoted_Tiebar1_ton + rVoted_Tiebar3_ton) - (rVoted_Tiebar2_ton + rVoted_Tiebar4_ton);
rDiff_TieBar_Diag_ton := (rVoted_Tiebar1_ton + rVoted_Tiebar4_ton) - (rVoted_Tiebar2_ton + rVoted_Tiebar3_ton);

IF c_TieBarStiffness_tonmm > 0.0 THEN
    rDeflect_TB_mm := rDiff_TieBar_TB_ton / (2.0 * c_TieBarStiffness_tonmm);
    rDeflect_LR_mm := rDiff_TieBar_LR_ton / (2.0 * c_TieBarStiffness_tonmm);
    rMaxPlatenDeflection_mm := SQRT(rDeflect_TB_mm * rDeflect_TB_mm + rDeflect_LR_mm * rDeflect_LR_mm);
    rEst_PlatenTiltDifferential_mm := rMaxPlatenDeflection_mm;
    rEst_PlatenAngularTilt_mrad := (rMaxPlatenDeflection_mm / (c_PlatenSpanWidth_mm * 0.001));
END_IF;

(* Proportional Trim Valve Bias for Dynamic Corner Balancing *)
rOut_TieBarTrimValve1_Pct := -rGain_TieBarTrim * (rVoted_Tiebar1_ton - (rEst_TotalClampTonnage_ton * 0.25));
rOut_TieBarTrimValve2_Pct := -rGain_TieBarTrim * (rVoted_Tiebar2_ton - (rEst_TotalClampTonnage_ton * 0.25));
rOut_TieBarTrimValve3_Pct := -rGain_TieBarTrim * (rVoted_Tiebar3_ton - (rEst_TotalClampTonnage_ton * 0.25));
rOut_TieBarTrimValve4_Pct := -rGain_TieBarTrim * (rVoted_Tiebar4_ton - (rEst_TotalClampTonnage_ton * 0.25));

(* Clamp Trim Valve Limits *)
IF rOut_TieBarTrimValve1_Pct > 50.0 THEN rOut_TieBarTrimValve1_Pct := 50.0; ELSIF rOut_TieBarTrimValve1_Pct < -50.0 THEN rOut_TieBarTrimValve1_Pct := -50.0; END_IF;
IF rOut_TieBarTrimValve2_Pct > 50.0 THEN rOut_TieBarTrimValve2_Pct := 50.0; ELSIF rOut_TieBarTrimValve2_Pct < -50.0 THEN rOut_TieBarTrimValve2_Pct := -50.0; END_IF;
IF rOut_TieBarTrimValve3_Pct > 50.0 THEN rOut_TieBarTrimValve3_Pct := 50.0; ELSIF rOut_TieBarTrimValve3_Pct < -50.0 THEN rOut_TieBarTrimValve3_Pct := -50.0; END_IF;
IF rOut_TieBarTrimValve4_Pct > 50.0 THEN rOut_TieBarTrimValve4_Pct := 50.0; ELSIF rOut_TieBarTrimValve4_Pct < -50.0 THEN rOut_TieBarTrimValve4_Pct := -50.0; END_IF;

(* 4. Screw Recovery Shear Dissipation & Barrel Thermal Conduction Balance *)
rEst_ScrewShearDissipation_kW := (c_PolymerMeltZeroViscosity_Pals * (3.14159 * (c_ScrewDiameter_mm * 0.001) * (rVoted_ScrewRPM / 60.0) / (c_ScrewFlightDepth_mm * 0.001)) * 
                                  (3.14159 * (c_ScrewDiameter_mm * 0.001) * (rVoted_ScrewRPM / 60.0) / (c_ScrewFlightDepth_mm * 0.001)) * 0.035);

(* 5. Hybrid Velocity-to-Pressure (V/P) Transfer Point Detector *)
bVP_Pos_Trigger := (rVoted_ScrewPos_mm <= rSet_VP_Position_mm);
bVP_CavPress_Trigger := (rVoted_CavityMeltPress_bar >= rSet_VP_CavityPress_bar);
bVP_HydDeriv_Trigger := (rFilt_HydPressDeriv_bars >= rSet_VP_HydPressDeriv_bars) AND (rFilt_ScrewAcc_mms2 < -3500.0);
bVP_CavDeriv_Trigger := (rFilt_CavPressDeriv_bars >= 2200.0);

CASE iSet_VP_Mode OF
    1: (* Position Only *)
        bVP_ConditionMet := bVP_Pos_Trigger;
    2: (* Cavity Pressure Only *)
        bVP_ConditionMet := bVP_CavPress_Trigger;
    3: (* Hydraulic Derivative Inflection *)
        bVP_ConditionMet := bVP_HydDeriv_Trigger;
    4: (* Hybrid Auto Mode: Position OR Cavity Pressure OR Inflection within 12 mm window *)
        bVP_ConditionMet := bVP_Pos_Trigger OR bVP_CavPress_Trigger OR 
                            (bVP_HydDeriv_Trigger AND (rVoted_ScrewPos_mm <= (rSet_VP_Position_mm + 12.0))) OR
                            (bVP_CavDeriv_Trigger AND (rVoted_ScrewPos_mm <= (rSet_VP_Position_mm + 15.0)));
ELSE
    bVP_ConditionMet := bVP_Pos_Trigger;
END_CASE;

(* 6. 6-Zone Ceramic Heater Band PID with Thermal Decoupling & Blower Control *)
(* Zone 1 Feed *)
rZone1_IntegralSum := rZone1_IntegralSum + (rSet_BarrelTemp_Zone1_degC - rVoted_Zone1Temp_degC) * c_Ts_Injection;
IF rZone1_IntegralSum > 100.0 THEN rZone1_IntegralSum := 100.0; ELSIF rZone1_IntegralSum < -50.0 THEN rZone1_IntegralSum := -50.0; END_IF;
rOut_BarrelZone1_PWM_Pct := 1.8 * (rSet_BarrelTemp_Zone1_degC - rVoted_Zone1Temp_degC) + 0.04 * rZone1_IntegralSum - rThermal_CouplingConductance * (rVoted_Zone2Temp_degC - rVoted_Zone1Temp_degC);
IF rOut_BarrelZone1_PWM_Pct > 100.0 THEN rOut_BarrelZone1_PWM_Pct := 100.0; ELSIF rOut_BarrelZone1_PWM_Pct < 0.0 THEN rOut_BarrelZone1_PWM_Pct := 0.0; END_IF;
bOut_BarrelCoolingFan1 := (rVoted_Zone1Temp_degC > (rSet_BarrelTemp_Zone1_degC + c_Deadband_Temp_degC + 3.0));

(* Zone 2 Compression *)
rZone2_IntegralSum := rZone2_IntegralSum + (rSet_BarrelTemp_Zone2_degC - rVoted_Zone2Temp_degC) * c_Ts_Injection;
IF rZone2_IntegralSum > 100.0 THEN rZone2_IntegralSum := 100.0; ELSIF rZone2_IntegralSum < -50.0 THEN rZone2_IntegralSum := -50.0; END_IF;
rOut_BarrelZone2_PWM_Pct := 2.0 * (rSet_BarrelTemp_Zone2_degC - rVoted_Zone2Temp_degC) + 0.045 * rZone2_IntegralSum - rThermal_CouplingConductance * (rVoted_Zone3Temp_degC - 2.0 * rVoted_Zone2Temp_degC + rVoted_Zone1Temp_degC);
IF rOut_BarrelZone2_PWM_Pct > 100.0 THEN rOut_BarrelZone2_PWM_Pct := 100.0; ELSIF rOut_BarrelZone2_PWM_Pct < 0.0 THEN rOut_BarrelZone2_PWM_Pct := 0.0; END_IF;
bOut_BarrelCoolingFan2 := (rVoted_Zone2Temp_degC > (rSet_BarrelTemp_Zone2_degC + c_Deadband_Temp_degC + 3.0));

(* Zone 3 Metering Transition *)
rZone3_IntegralSum := rZone3_IntegralSum + (rSet_BarrelTemp_Zone3_degC - rVoted_Zone3Temp_degC) * c_Ts_Injection;
IF rZone3_IntegralSum > 100.0 THEN rZone3_IntegralSum := 100.0; ELSIF rZone3_IntegralSum < -50.0 THEN rZone3_IntegralSum := -50.0; END_IF;
rOut_BarrelZone3_PWM_Pct := 2.2 * (rSet_BarrelTemp_Zone3_degC - rVoted_Zone3Temp_degC) + 0.05 * rZone3_IntegralSum - 0.25 * rEst_ScrewShearDissipation_kW;
IF rOut_BarrelZone3_PWM_Pct > 100.0 THEN rOut_BarrelZone3_PWM_Pct := 100.0; ELSIF rOut_BarrelZone3_PWM_Pct < 0.0 THEN rOut_BarrelZone3_PWM_Pct := 0.0; END_IF;
bOut_BarrelCoolingFan3 := (rVoted_Zone3Temp_degC > (rSet_BarrelTemp_Zone3_degC + c_Deadband_Temp_degC + 2.5));

(* Zone 4 Metering Center *)
rZone4_IntegralSum := rZone4_IntegralSum + (rSet_BarrelTemp_Zone4_degC - rVoted_Zone4Temp_degC) * c_Ts_Injection;
IF rZone4_IntegralSum > 100.0 THEN rZone4_IntegralSum := 100.0; ELSIF rZone4_IntegralSum < -50.0 THEN rZone4_IntegralSum := -50.0; END_IF;
rOut_BarrelZone4_PWM_Pct := 2.2 * (rSet_BarrelTemp_Zone4_degC - rVoted_Zone4Temp_degC) + 0.05 * rZone4_IntegralSum - 0.35 * rEst_ScrewShearDissipation_kW;
IF rOut_BarrelZone4_PWM_Pct > 100.0 THEN rOut_BarrelZone4_PWM_Pct := 100.0; ELSIF rOut_BarrelZone4_PWM_Pct < 0.0 THEN rOut_BarrelZone4_PWM_Pct := 0.0; END_IF;
bOut_BarrelCoolingFan4 := (rVoted_Zone4Temp_degC > (rSet_BarrelTemp_Zone4_degC + c_Deadband_Temp_degC + 2.5));

(* Zone 5 Metering Front *)
rZone5_IntegralSum := rZone5_IntegralSum + (rSet_BarrelTemp_Zone5_degC - rVoted_Zone5Temp_degC) * c_Ts_Injection;
IF rZone5_IntegralSum > 100.0 THEN rZone5_IntegralSum := 100.0; ELSIF rZone5_IntegralSum < -50.0 THEN rZone5_IntegralSum := -50.0; END_IF;
rOut_BarrelZone5_PWM_Pct := 2.1 * (rSet_BarrelTemp_Zone5_degC - rVoted_Zone5Temp_degC) + 0.048 * rZone5_IntegralSum - 0.20 * rEst_ScrewShearDissipation_kW;
IF rOut_BarrelZone5_PWM_Pct > 100.0 THEN rOut_BarrelZone5_PWM_Pct := 100.0; ELSIF rOut_BarrelZone5_PWM_Pct < 0.0 THEN rOut_BarrelZone5_PWM_Pct := 0.0; END_IF;
bOut_BarrelCoolingFan5 := (rVoted_Zone5Temp_degC > (rSet_BarrelTemp_Zone5_degC + c_Deadband_Temp_degC + 2.5));

(* Zone 6 Nozzle Adapter *)
rZone6_IntegralSum := rZone6_IntegralSum + (rSet_BarrelTemp_Zone6_degC - rVoted_Zone6Temp_degC) * c_Ts_Injection;
IF rZone6_IntegralSum > 100.0 THEN rZone6_IntegralSum := 100.0; ELSIF rZone6_IntegralSum < -50.0 THEN rZone6_IntegralSum := -50.0; END_IF;
rOut_BarrelZone6_PWM_Pct := 2.5 * (rSet_BarrelTemp_Zone6_degC - rVoted_Zone6Temp_degC) + 0.055 * rZone6_IntegralSum;
IF rOut_BarrelZone6_PWM_Pct > 100.0 THEN rOut_BarrelZone6_PWM_Pct := 100.0; ELSIF rOut_BarrelZone6_PWM_Pct < 0.0 THEN rOut_BarrelZone6_PWM_Pct := 0.0; END_IF;
bOut_BarrelCoolingFan6 := (rVoted_Zone6Temp_degC > (rSet_BarrelTemp_Zone6_degC + c_Deadband_Temp_degC + 2.0));
"""
    parts.append(phase2)

    # -------------------------------------------------------------
    # PHASE 3: 8x8 DISCRETE STATE-SPACE & RECEDING-HORIZON MPC
    # -------------------------------------------------------------
    phase3 = """
(* ==================================================================================================== *)
(* PHASE 3: DISCRETE STATE-SPACE PROPAGATION & RECEDING-HORIZON MPC                                     *)
(* ==================================================================================================== *)

(* Pack State Vector x[k] from Voted Sensors and Observers *)
vecX[0] := rVoted_ScrewPos_mm;
vecX[1] := rFilt_ScrewVel_mms;
vecX[2] := rVoted_HydPress_bar;
vecX[3] := rVoted_CavityMeltPress_bar;
vecX[4] := rVoted_AccumPress_bar;
vecX[5] := rVoted_NozzleTemp_degC;
vecX[6] := rMaxPlatenDeflection_mm;
vecX[7] := rVoted_HydPress_bar; (* Backpressure mode observation *)

(* One-Step Ahead State Space Prediction: x[k+1] = A * x[k] + B * u[k] *)
FOR iRow := 0 TO 7 DO
    rMatAccum := 0.0;
    FOR iCol := 0 TO 7 DO
        rMatAccum := rMatAccum + matA[iRow, iCol] * vecX[iCol];
    END_FOR;
    FOR iCol := 0 TO 3 DO
        rMatAccum := rMatAccum + matB[iRow, iCol] * vecU[iCol];
    END_FOR;
    vecX_pred[iRow] := rMatAccum;
END_FOR;

(* Calculate State Tracking Errors e[k] = x_ref - x[k] *)
FOR iRow := 0 TO 7 DO
    vecErr[iRow] := vecX_ref[iRow] - vecX[iRow];
END_FOR;

(* Receding-Horizon Optimal MPC Feedback Calculation: delta_u = K_mpc * e *)
FOR iRow := 0 TO 3 DO
    rMatAccum := 0.0;
    FOR iCol := 0 TO 7 DO
        rMatAccum := rMatAccum + matK_mpc[iRow, iCol] * vecErr[iCol];
    END_FOR;
    vecDeltaU[iRow] := rMatAccum;
END_FOR;
"""
    parts.append(phase3)

    # -------------------------------------------------------------
    # PHASE 4: 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM)
    # -------------------------------------------------------------
    phase4 = """
(* ==================================================================================================== *)
(* PHASE 4: 12-STAGE DETERMINISTIC OPERATIONAL FINITE STATE MACHINE (FSM)                               *)
(* ==================================================================================================== *)

(* Global Safety Interlock Verification *)
bSafetyCircuitBreached := NOT (bEmergencyStop_CH1 AND bEmergencyStop_CH2 AND bSafetyGateClosed_CH1 AND bSafetyGateClosed_CH2);
bColdScrewInterlockActive := (rVoted_Zone1Temp_degC < (rSet_BarrelTemp_Zone1_degC - 15.0)) OR
                             (rVoted_Zone2Temp_degC < (rSet_BarrelTemp_Zone2_degC - 15.0)) OR
                             (rVoted_Zone3Temp_degC < (rSet_BarrelTemp_Zone3_degC - 15.0)) OR
                             (rVoted_Zone4Temp_degC < (rSet_BarrelTemp_Zone4_degC - 15.0)) OR
                             (rVoted_Zone5Temp_degC < (rSet_BarrelTemp_Zone5_degC - 15.0)) OR
                             (rVoted_Zone6Temp_degC < (rSet_BarrelTemp_Zone6_degC - 15.0));

IF bSafetyCircuitBreached OR bAlarm_HydPress_HI_HI OR bAlarm_ClampTonnage_HI_HI OR bFault_TMR_Trip THEN
    iState := 11; (* Immediate E-Stop Hydraulic Dump Transition *)
END_IF;

bCycleCompletedPulse := FALSE;

CASE iState OF

    0: (* --------------------------------------------------------------------------------------------- *)
       (* STATE 0: IMM_STANDBY_MOLD_OPEN                                                               *)
       (* Waiting for operator start command, verifying mold clear and safety barriers                  *)
       (* --------------------------------------------------------------------------------------------- *)
        rOut_InjServoValve_Pct          := 0.0;
        rOut_AccumulatorDischarge_Pct   := 0.0;
        rOut_ScrewMotorDisplacement_Pct := 0.0;
        rOut_ProportionalBackpress_bar  := 0.0;
        rOut_ClampMainProportional_Pct  := 0.0;
        rOut_EjectorServoValve_Pct      := 0.0;
        bMachineInSafeStop              := FALSE;
        udiCycleTime_ms                 := 0;
        bEst_VP_TransferTriggered       := FALSE;

        IF bMasterStart AND bAutoCycleEnable AND NOT bSafetyCircuitBreached THEN
            IF bColdScrewInterlockActive THEN
                iState := 1; (* Proceed to Barrel Heating Soak *)
            ELSE
                iState := 2; (* Proceed directly to Mold Clamping *)
            END_IF;
            udiStateStep := 0;
        END_IF;

    1: (* --------------------------------------------------------------------------------------------- *)
       (* STATE 1: BARREL_PREHEAT_SOAK_TEMP                                                            *)
       (* Waiting for 6-zone thermal stabilization and soaking period before screw enable               *)
       (* --------------------------------------------------------------------------------------------- *)
        rOut_InjServoValve_Pct          := 0.0;
        rOut_ScrewMotorDisplacement_Pct := 0.0;
        rOut_ClampMainProportional_Pct  := 0.0;

        IF NOT bColdScrewInterlockActive THEN
            udiSoakTimer_ms := udiSoakTimer_ms + 1;
            IF udiSoakTimer_ms >= 5000 THEN (* 5 second soak confirmation *)
                udiSoakTimer_ms := 0;
                iState := 2; (* Proceed to Mold Clamp *)
                udiStateStep := 0;
            END_IF;
        ELSE
            udiSoakTimer_ms := 0;
        END_IF;

        IF NOT bAutoCycleEnable THEN
            iState := 0;
        END_IF;

    2: (* --------------------------------------------------------------------------------------------- *)
       (* STATE 2: MOLD_CLAMP_TONNAGE_BUILD_1200T                                                      *)
       (* Moving platen high-speed close, low-pressure mold safety, and 1,200-ton lockup               *)
       (* --------------------------------------------------------------------------------------------- *)
        IF bRobotArmClearMoldArea AND (rVoted_EjectorPos_mm <= (rSet_EjectorRetractPos_mm + 2.0)) THEN
            CASE udiStateStep OF
                0: (* Platen Rapid Advance *)
                    rOut_ClampMainProportional_Pct := 75.0;
                    IF rVoted_PlatenPos_mm <= 150.0 THEN
                        udiStateStep := 1; (* Low Pressure Mold Protection Zone *)
                    END_IF;

                1: (* Low-Pressure Mold Protection (Sensitive Obstruction Detection) *)
                    rOut_ClampMainProportional_Pct := 20.0;
                    IF rVoted_HydPress_bar > 45.0 AND rVoted_PlatenPos_mm > 15.0 THEN
                        (* Obstruction trapped between mold halves! *)
                        iState := 8; (* Abort clamp, reopen mold immediately *)
                        udiStateStep := 0;
                    ELSIF rVoted_PlatenPos_mm <= 5.0 THEN
                        udiStateStep := 2; (* Mold Halves Fully Touching, Build High Tonnage *)
                    END_IF;

                2: (* 1,200-Ton High-Pressure Clamping Tonnage Lockup *)
                    rOut_ClampMainProportional_Pct := 95.0;
                    IF rEst_TotalClampTonnage_ton >= (rSet_TargetTonnage_ton * 0.98) THEN
                        rOut_ClampMainProportional_Pct := 65.0; (* Tonnage maintenance pressure *)
                        iState := 3; (* Proceed to High-Speed Injection *)
                        udiStateStep := 0;
                    END_IF;
            END_CASE;
        ELSE
            rOut_ClampMainProportional_Pct := 0.0;
        END_IF;

    3: (* --------------------------------------------------------------------------------------------- *)
       (* STATE 3: HIGH_SPEED_INJECTION_VELOCITY_FILL                                                  *)
       (* Multi-stage closed-loop screw velocity fill with N2 accumulator assist                        *)
       (* --------------------------------------------------------------------------------------------- *)
        udiCycleTime_ms := udiCycleTime_ms + 1;

        (* Check for V/P Transfer Triggering Conditions *)
        IF bVP_ConditionMet THEN
            bEst_VP_TransferTriggered := TRUE;
            rEst_VP_TransferPosition_mm := rVoted_ScrewPos_mm;
            rEst_VP_TransferCavityPress_bar := rVoted_CavityMeltPress_bar;
            rEst_VP_TransferHydPress_bar := rVoted_HydPress_bar;

            (* Pre-condition holding pressure spool command to prevent pressure shock *)
            rBumplessHoldSpoolBias := rOut_InjServoValve_Pct * (rSet_HoldPress_Stage1_bar / MAX(rVoted_HydPress_bar, 10.0));
            iState := 4; (* Transition to Bumpless V/P Transfer *)
            udiStateStep := 0;
        ELSE
            (* Multi-Stage Velocity Profile Interpolation *)
            IF rVoted_ScrewPos_mm > rSet_InjStroke_Stage1_mm THEN
                (* Stage 1: Initial Slow Fill through Bumper Hot Runner Gates *)
                vecX_ref[1] := -rSet_InjVel_Stage1_mms;
                rOut_AccumulatorDischarge_Pct := 15.0;
                rOut_InjServoValve_Pct := 42.0 + vecDeltaU[0];
            ELSIF rVoted_ScrewPos_mm > rSet_InjStroke_Stage2_mm THEN
                (* Stage 2: Main Bumper Fascia High-Speed Injection with Full Accumulator Assist *)
                vecX_ref[1] := -rSet_InjVel_Stage2_mms;
                rOut_AccumulatorDischarge_Pct := 85.0;
                rOut_InjServoValve_Pct := 88.0 + vecDeltaU[0];
            ELSE
                (* Stage 3: Deceleration Fill Approaching 95% Volumetric Cavity Capacity *)
                vecX_ref[1] := -rSet_InjVel_Stage3_mms;
                rOut_AccumulatorDischarge_Pct := 30.0;
                rOut_InjServoValve_Pct := 55.0 + vecDeltaU[0];
            END_IF;

            IF rOut_InjServoValve_Pct > 100.0 THEN rOut_InjServoValve_Pct := 100.0; ELSIF rOut_InjServoValve_Pct < 0.0 THEN rOut_InjServoValve_Pct := 0.0; END_IF;
        END_IF;

    4: (* --------------------------------------------------------------------------------------------- *)
       (* STATE 4: VP_TRANSFER_POINT_TRANSITION                                                        *)
       (* Sub-millisecond smooth bumpless transition from velocity control to cavity holding pressure   *)
       (* --------------------------------------------------------------------------------------------- *)
        udiCycleTime_ms := udiCycleTime_ms + 1;
        rOut_AccumulatorDischarge_Pct := 0.0; (* Immediately isolate accumulator to stop velocity surging *)

        (* Slew spool smoothly from velocity command to holding pressure command *)
        rOut_InjServoValve_Pct := rBumplessHoldSpoolBias + 0.15 * (rSet_HoldPress_Stage1_bar - rVoted_HydPress_bar);
        IF rOut_InjServoValve_Pct > 80.0 THEN rOut_InjServoValve_Pct := 80.0; ELSIF rOut_InjServoValve_Pct < 10.0 THEN rOut_InjServoValve_Pct := 10.0; END_IF;

        udiStateStep := udiStateStep + 1;
        IF udiStateStep >= 15 THEN (* 15 ms bumpless smoothing window *)
            iState := 5; (* Proceed to Dynamic Cavity Pressure Packing *)
            udiStateStep := 0;
            udiHoldTimer_ms := 0;
        END_IF;

    5: (* --------------------------------------------------------------------------------------------- *)
       (* STATE 5: DYNAMIC_CAVITY_PRESSURE_PACKING                                                     *)
       (* 3-Stage holding pressure profile adapted dynamically by Tait PVT shrinkage observer          *)
       (* --------------------------------------------------------------------------------------------- *)
        udiCycleTime_ms := udiCycleTime_ms + 1;
        udiHoldTimer_ms := udiHoldTimer_ms + 1;

        IF udiHoldTimer_ms < REAL_TO_UDINT(tSet_HoldTime_Stage1_s * 1000.0) THEN
            (* Stage 1: High Initial Packing Pressure *)
            vecX_ref[2] := rSet_HoldPress_Stage1_bar;
            rOut_InjServoValve_Pct := 55.0 + 0.22 * (rSet_HoldPress_Stage1_bar - rVoted_HydPress_bar);
        ELSIF udiHoldTimer_ms < REAL_TO_UDINT((tSet_HoldTime_Stage1_s + tSet_HoldTime_Stage2_s) * 1000.0) THEN
            (* Stage 2: Volumetric Shrinkage Compensating Pressure via Tait Observer *)
            vecX_ref[2] := rSet_HoldPress_Stage2_bar + (rEst_VolumetricShrinkage_Pct - 1.5) * 5.0;
            rOut_InjServoValve_Pct := 42.0 + 0.20 * (vecX_ref[2] - rVoted_HydPress_bar);
        ELSIF udiHoldTimer_ms < REAL_TO_UDINT((tSet_HoldTime_Stage1_s + tSet_HoldTime_Stage2_s + tSet_HoldTime_Stage3_s) * 1000.0) THEN
            (* Stage 3: Low Residual Packing until Gate Solidification Freeze-off *)
            vecX_ref[2] := rSet_HoldPress_Stage3_bar;
            rOut_InjServoValve_Pct := 30.0 + 0.18 * (rSet_HoldPress_Stage3_bar - rVoted_HydPress_bar);
        ELSE
            (* Holding Stage Complete: Record Cushion and Transition to Plasticizing *)
            rEst_MeasuredCushion_mm := rVoted_ScrewPos_mm;
            rOut_InjServoValve_Pct := 0.0;
            iState := 6; (* Proceed to Screw Recovery & Plasticizing *)
            udiStateStep := 0;
            udiCoolingTimer_ms := 0;
        END_IF;

        IF rOut_InjServoValve_Pct > 90.0 THEN rOut_InjServoValve_Pct := 90.0; ELSIF rOut_InjServoValve_Pct < 0.0 THEN rOut_InjServoValve_Pct := 0.0; END_IF;

    6: (* --------------------------------------------------------------------------------------------- *)
       (* STATE 6: SCREW_RECOVERY_AND_PLASTICIZING                                                     *)
       (* Hydraulic drive motor rotation, closed-loop proportional backpressure, polymer melting        *)
       (* --------------------------------------------------------------------------------------------- *)
        udiCycleTime_ms := udiCycleTime_ms + 1;
        udiCoolingTimer_ms := udiCoolingTimer_ms + 1;

        (* Engage Hydraulic Screw Drive Motor *)
        rOut_ScrewMotorDisplacement_Pct := 65.0;
        vecX_ref[7] := rSet_BackPressure_bar;

        (* Closed-Loop Proportional Backpressure Valve Control *)
        rOut_ProportionalBackpress_bar := rSet_BackPressure_bar + 0.12 * (rSet_BackPressure_bar - rVoted_HydPress_bar);
        IF rOut_ProportionalBackpress_bar > 40.0 THEN rOut_ProportionalBackpress_bar := 40.0; ELSIF rOut_ProportionalBackpress_bar < 5.0 THEN rOut_ProportionalBackpress_bar := 5.0; END_IF;

        (* Retract Screw under Melt Backpressure until Shot Size Reached *)
        IF rVoted_ScrewPos_mm >= rSet_ShotSize_mm THEN
            rOut_ScrewMotorDisplacement_Pct := 0.0;
            rOut_ProportionalBackpress_bar := 0.0;
            iState := 7; (* Proceed to Melt Decompression Suck-Back & In-Mold Cooling *)
            udiStateStep := 0;
        END_IF;

    7: (* --------------------------------------------------------------------------------------------- *)
       (* STATE 7: COOLING_CYCLE_AND_SUCK_BACK                                                         *)
       (* Hydraulic screw decompression suck-back to prevent drool, complete in-mold bumper cooling    *)
       (* --------------------------------------------------------------------------------------------- *)
        udiCycleTime_ms := udiCycleTime_ms + 1;
        udiCoolingTimer_ms := udiCoolingTimer_ms + 1;

        (* Linear Suck-Back Decompression *)
        IF rVoted_ScrewPos_mm < (rSet_ShotSize_mm + rSet_SuckBack_mm) THEN
            rOut_InjServoValve_Pct := -25.0; (* Retract injection cylinder gently *)
        ELSE
            rOut_InjServoValve_Pct := 0.0;
        END_IF;

        (* In-Mold Solidification Cooling Countdown *)
        IF udiCoolingTimer_ms >= REAL_TO_UDINT(rSet_CoolingTime_s * 1000.0) THEN
            iState := 8; (* Proceed to Mold Open *)
            udiStateStep := 0;
        END_IF;

    8: (* --------------------------------------------------------------------------------------------- *)
       (* STATE 8: MOLD_OPEN_DECELERATION_SOFT_STOP                                                    *)
       (* High-tonnage mold break, fast platen open, smooth deceleration to daylight target             *)
       (* --------------------------------------------------------------------------------------------- *)
        udiCycleTime_ms := udiCycleTime_ms + 1;

        CASE udiStateStep OF
            0: (* Mold Break (High Force Cracking at Slow Velocity) *)
                rOut_ClampMainProportional_Pct := -45.0;
                IF rVoted_PlatenPos_mm >= 60.0 THEN
                    udiStateStep := 1; (* High-Speed Open Traverse *)
                END_IF;

            1: (* Rapid Mold Traverse *)
                rOut_ClampMainProportional_Pct := -85.0;
                IF rVoted_PlatenPos_mm >= (rSet_MoldOpenStroke_mm - 200.0) THEN
                    udiStateStep := 2; (* Deceleration Soft-Stop Zone *)
                END_IF;

            2: (* Deceleration Soft-Stop Cushioning *)
                rOut_ClampMainProportional_Pct := -22.0;
                IF rVoted_PlatenPos_mm >= rSet_MoldOpenStroke_mm THEN
                    rOut_ClampMainProportional_Pct := 0.0;
                    iState := 9; (* Proceed to Hydraulic Multi-Pulse Ejection *)
                    udiStateStep := 0;
                    iEjectorCurrentPulse := 0;
                    bEjectorForwardPhase := TRUE;
                END_IF;
        END_CASE;

    9: (* --------------------------------------------------------------------------------------------- *)
       (* STATE 9: HYDRAULIC_EJECTOR_MULTI_PULSE                                                       *)
       (* Multi-pulse ejector pin pulsing to de-mold massive bumper fascia without distorting clips     *)
       (* --------------------------------------------------------------------------------------------- *)
        udiCycleTime_ms := udiCycleTime_ms + 1;

        IF bEjectorForwardPhase THEN
            (* Advance Ejector Plate Forward *)
            rOut_EjectorServoValve_Pct := 65.0;
            IF rVoted_EjectorPos_mm >= rSet_EjectorForwardPos_mm THEN
                udiEjectorTimer_ms := udiEjectorTimer_ms + 1;
                IF udiEjectorTimer_ms >= 400 THEN (* 400 ms dwell at forward stroke *)
                    udiEjectorTimer_ms := 0;
                    bEjectorForwardPhase := FALSE;
                END_IF;
            END_IF;
        ELSE
            (* Retract Ejector Plate *)
            rOut_EjectorServoValve_Pct := -55.0;
            IF rVoted_EjectorPos_mm <= rSet_EjectorRetractPos_mm THEN
                udiEjectorTimer_ms := udiEjectorTimer_ms + 1;
                IF udiEjectorTimer_ms >= 300 THEN (* 300 ms dwell at retract stroke *)
                    udiEjectorTimer_ms := 0;
                    iEjectorCurrentPulse := iEjectorCurrentPulse + 1;
                    IF iEjectorCurrentPulse >= iSet_EjectorPulseCount THEN
                        rOut_EjectorServoValve_Pct := 0.0;
                        iState := 10; (* Proceed to Robot Gripper Extraction *)
                        udiStateStep := 0;
                    ELSE
                        bEjectorForwardPhase := TRUE;
                    END_IF;
                END_IF;
            END_IF;
        END_IF;

    10: (* -------------------------------------------------------------------------------------------- *)
        (* STATE 10: ROBOT_GRIPPER_PART_TAKEOUT                                                        *)
        (* 6-Axis robot enters mold space, vacuum grips bumper fascia, extracts and clears daylight     *)
        (* -------------------------------------------------------------------------------------------- *)
        udiCycleTime_ms := udiCycleTime_ms + 1;
        rOut_ClampMainProportional_Pct := 0.0;
        rOut_EjectorServoValve_Pct     := 0.0;

        (* Verify Robot Takeout Permissives and Cycle Completion *)
        IF bRobotTakeoutPermissive AND bRobotArmClearMoldArea THEN
            bCycleCompletedPulse := TRUE;
            rEst_CycleTime_s := UDINT_TO_REAL(udiCycleTime_ms) * 0.001;

            IF bAutoCycleEnable THEN
                iState := 2; (* Immediate Clamp Next Cycle *)
                udiStateStep := 0;
                udiCycleTime_ms := 0;
            ELSE
                iState := 0; (* Return to Standby *)
                udiStateStep := 0;
            END_IF;
        END_IF;

    11: (* -------------------------------------------------------------------------------------------- *)
        (* STATE 11: EMERGENCY_ESTOP_HYDRAULIC_DUMP                                                    *)
        (* Fail-safe hydraulic dump: de-energize servo valves, open tank dump valves, lock platen       *)
        (* -------------------------------------------------------------------------------------------- *)
        rOut_InjServoValve_Pct          := 0.0;
        rOut_AccumulatorDischarge_Pct   := 0.0;
        rOut_ScrewMotorDisplacement_Pct := 0.0;
        rOut_ProportionalBackpress_bar  := 0.0;
        rOut_ClampMainProportional_Pct  := 0.0;
        rOut_TieBarTrimValve1_Pct       := 0.0;
        rOut_TieBarTrimValve2_Pct       := 0.0;
        rOut_TieBarTrimValve3_Pct       := 0.0;
        rOut_TieBarTrimValve4_Pct       := 0.0;
        rOut_EjectorServoValve_Pct      := 0.0;
        bMachineInSafeStop              := TRUE;

        (* Reset and Recovery Handling *)
        IF bAlarmAcknowledge AND NOT bSafetyCircuitBreached AND NOT bFault_TMR_Trip THEN
            bMachineInSafeStop := FALSE;
            iState := 0; (* Return to Standby after explicit operator acknowledge *)
            udiStateStep := 0;
        END_IF;

ELSE
    iState := 11; (* Undefined State Safety Clamp *)
END_CASE;

iCurrentState := iState;
"""
    parts.append(phase4)

    # -------------------------------------------------------------
    # PHASE 5: ISA-18.2 PROCESS ALARMS & DIAGNOSTIC WORD BIT-PACKING
    # -------------------------------------------------------------
    phase5 = """
(* ==================================================================================================== *)
(* PHASE 5: ISA-18.2 PROCESS ALARMS & DIAGNOSTIC WORD BIT-PACKING                                       *)
(* ==================================================================================================== *)

(* 1. Hydraulic Injection Cylinder Pressure Alarms *)
IF rVoted_HydPress_bar >= c_Trip_HydPress_HI_HI_bar THEN
    bAlarm_HydPress_HI_HI := TRUE;
ELSIF rVoted_HydPress_bar <= (c_Trip_HydPress_HI_HI_bar - c_Deadband_Pressure_bar) AND bAlarmAcknowledge THEN
    bAlarm_HydPress_HI_HI := FALSE;
END_IF;

IF rVoted_HydPress_bar >= c_Warn_HydPress_HI_bar THEN
    bAlarm_HydPress_HI := TRUE;
ELSIF rVoted_HydPress_bar <= (c_Warn_HydPress_HI_bar - c_Deadband_Pressure_bar) THEN
    bAlarm_HydPress_HI := FALSE;
END_IF;

(* 2. Bumper Mold Cavity Melt Pressure Alarms *)
IF rVoted_CavityMeltPress_bar >= c_Trip_CavityPress_HI_HI_bar THEN
    bAlarm_CavityPress_HI_HI := TRUE;
ELSIF rVoted_CavityMeltPress_bar <= (c_Trip_CavityPress_HI_HI_bar - 25.0) AND bAlarmAcknowledge THEN
    bAlarm_CavityPress_HI_HI := FALSE;
END_IF;

IF rVoted_CavityMeltPress_bar >= c_Warn_CavityPress_HI_bar THEN
    bAlarm_CavityPress_HI := TRUE;
ELSIF rVoted_CavityMeltPress_bar <= (c_Warn_CavityPress_HI_bar - 20.0) THEN
    bAlarm_CavityPress_HI := FALSE;
END_IF;

(* 3. Clamping Tonnage Overload & Tie-Bar Balancing Alarms *)
IF rEst_TotalClampTonnage_ton >= c_Trip_ClampTonnage_HI_HI_ton THEN
    bAlarm_ClampTonnage_HI_HI := TRUE;
ELSIF rEst_TotalClampTonnage_ton <= (c_Trip_ClampTonnage_HI_HI_ton - 30.0) AND bAlarmAcknowledge THEN
    bAlarm_ClampTonnage_HI_HI := FALSE;
END_IF;

IF rEst_TotalClampTonnage_ton >= c_Warn_ClampTonnage_HI_ton THEN
    bAlarm_ClampTonnage_HI := TRUE;
ELSIF rEst_TotalClampTonnage_ton <= (c_Warn_ClampTonnage_HI_ton - 25.0) THEN
    bAlarm_ClampTonnage_HI := FALSE;
END_IF;

(* 4. Moving Platen Parallelism & Tilt Alarms *)
IF rEst_PlatenTiltDifferential_mm >= c_Trip_PlatenTilt_HI_HI_mm THEN
    bAlarm_PlatenTilt_HI_HI := TRUE;
ELSIF rEst_PlatenTiltDifferential_mm <= (c_Trip_PlatenTilt_HI_HI_mm - 0.015) AND bAlarmAcknowledge THEN
    bAlarm_PlatenTilt_HI_HI := FALSE;
END_IF;

IF rEst_PlatenTiltDifferential_mm >= c_Warn_PlatenTilt_HI_mm THEN
    bAlarm_PlatenTilt_HI := TRUE;
ELSIF rEst_PlatenTiltDifferential_mm <= (c_Warn_PlatenTilt_HI_mm - 0.010) THEN
    bAlarm_PlatenTilt_HI := FALSE;
END_IF;

(* 5. N2 Accumulator Precharge Low Pressure Alarms *)
IF rVoted_AccumPress_bar <= c_Trip_AccumPress_LO_LO_bar THEN
    bAlarm_AccumPress_LO_LO := TRUE;
ELSIF rVoted_AccumPress_bar >= (c_Trip_AccumPress_LO_LO_bar + c_Deadband_Pressure_bar) AND bAlarmAcknowledge THEN
    bAlarm_AccumPress_LO_LO := FALSE;
END_IF;

IF rVoted_AccumPress_bar <= c_Warn_AccumPress_LO_bar THEN
    bAlarm_AccumPress_LO := TRUE;
ELSIF rVoted_AccumPress_bar >= (c_Warn_AccumPress_LO_bar + c_Deadband_Pressure_bar) THEN
    bAlarm_AccumPress_LO := FALSE;
END_IF;

(* 6. Hydraulic Oil Reservoir Temperature Alarms *)
IF rVoted_OilTemp_degC >= c_Trip_OilTemp_HI_HI_degC THEN
    bAlarm_OilTemp_HI_HI := TRUE;
ELSIF rVoted_OilTemp_degC <= (c_Trip_OilTemp_HI_HI_degC - c_Deadband_Temp_degC) AND bAlarmAcknowledge THEN
    bAlarm_OilTemp_HI_HI := FALSE;
END_IF;

IF rVoted_OilTemp_degC >= c_Warn_OilTemp_HI_degC THEN
    bAlarm_OilTemp_HI := TRUE;
ELSIF rVoted_OilTemp_degC <= (c_Warn_OilTemp_HI_degC - c_Deadband_Temp_degC) THEN
    bAlarm_OilTemp_HI := FALSE;
END_IF;

(* 7. Hardware Safety Interlocks & Cold Screw Trips *)
bAlarm_SafetyGateBreached := NOT (bSafetyGateClosed_CH1 AND bSafetyGateClosed_CH2);
bAlarm_EstopTripped       := NOT (bEmergencyStop_CH1 AND bEmergencyStop_CH2);
bAlarm_ColdScrewBlocked   := bColdScrewInterlockActive;

(* Master Trip Alarm Indicator *)
bAlarmTripActive := bAlarm_HydPress_HI_HI OR bAlarm_CavityPress_HI_HI OR bAlarm_ClampTonnage_HI_HI OR
                    bAlarm_PlatenTilt_HI_HI OR bAlarm_AccumPress_LO_LO OR bAlarm_OilTemp_HI_HI OR
                    bAlarm_SafetyGateBreached OR bAlarm_EstopTripped OR bFault_TMR_Trip;

(* ---------------------------------------------------------------------------------------------------- *)
(* Bit-Packing into ISA-18.2 DWORD Status Registers                                                     *)
(* ---------------------------------------------------------------------------------------------------- *)
dwAlarmWord1_ISA := 16#00000000;
IF bAlarm_HydPress_HI_HI     THEN dwAlarmWord1_ISA := dwAlarmWord1_ISA OR 16#00000001; END_IF;
IF bAlarm_HydPress_HI        THEN dwAlarmWord1_ISA := dwAlarmWord1_ISA OR 16#00000002; END_IF;
IF bAlarm_CavityPress_HI_HI  THEN dwAlarmWord1_ISA := dwAlarmWord1_ISA OR 16#00000004; END_IF;
IF bAlarm_CavityPress_HI     THEN dwAlarmWord1_ISA := dwAlarmWord1_ISA OR 16#00000008; END_IF;
IF bAlarm_ClampTonnage_HI_HI THEN dwAlarmWord1_ISA := dwAlarmWord1_ISA OR 16#00000010; END_IF;
IF bAlarm_ClampTonnage_HI    THEN dwAlarmWord1_ISA := dwAlarmWord1_ISA OR 16#00000020; END_IF;
IF bAlarm_PlatenTilt_HI_HI   THEN dwAlarmWord1_ISA := dwAlarmWord1_ISA OR 16#00000040; END_IF;
IF bAlarm_PlatenTilt_HI      THEN dwAlarmWord1_ISA := dwAlarmWord1_ISA OR 16#00000080; END_IF;
IF bAlarm_AccumPress_LO_LO   THEN dwAlarmWord1_ISA := dwAlarmWord1_ISA OR 16#00000100; END_IF;
IF bAlarm_AccumPress_LO      THEN dwAlarmWord1_ISA := dwAlarmWord1_ISA OR 16#00000200; END_IF;
IF bAlarm_OilTemp_HI_HI      THEN dwAlarmWord1_ISA := dwAlarmWord1_ISA OR 16#00000400; END_IF;
IF bAlarm_OilTemp_HI         THEN dwAlarmWord1_ISA := dwAlarmWord1_ISA OR 16#00000800; END_IF;
IF bAlarm_SafetyGateBreached THEN dwAlarmWord1_ISA := dwAlarmWord1_ISA OR 16#00001000; END_IF;
IF bAlarm_EstopTripped       THEN dwAlarmWord1_ISA := dwAlarmWord1_ISA OR 16#00002000; END_IF;
IF bAlarm_ColdScrewBlocked   THEN dwAlarmWord1_ISA := dwAlarmWord1_ISA OR 16#00004000; END_IF;
IF bFault_TMR_Trip           THEN dwAlarmWord1_ISA := dwAlarmWord1_ISA OR 16#00008000; END_IF;

dwAlarmWord2_ISA := 16#00000000;
IF bTMR_AnyDiscrepancyTrip   THEN dwAlarmWord2_ISA := dwAlarmWord2_ISA OR 16#00000001; END_IF;
IF bEst_VP_TransferTriggered THEN dwAlarmWord2_ISA := dwAlarmWord2_ISA OR 16#00000002; END_IF;
IF bMachineInSafeStop        THEN dwAlarmWord2_ISA := dwAlarmWord2_ISA OR 16#00000004; END_IF;
IF bAlarmTripActive          THEN dwAlarmWord2_ISA := dwAlarmWord2_ISA OR 16#00000008; END_IF;

dwFSM_StatusWord := INT_TO_DWORD(iState) OR SHL(UDINT_TO_DWORD(udiStateStep), 8) OR SHL(INT_TO_DWORD(iEjectorCurrentPulse), 16);

END_FUNCTION_BLOCK
"""
    parts.append(phase5)

    return "".join(parts)

if __name__ == "__main__":
    code = generate_code()
    print(f"Total Generated Code Characters: {len(code)}")
    print(f"Total Lines: {len(code.splitlines())}")
