# scratch/generate_dataset.py
# Deep synthesis of FB_Metals_ColdRolling_6StandTandem_HAGC

import json
import uuid
import os
import re

def build_st_code():
    sections = []
    
    # Header block
    sections.append("""FUNCTION_BLOCK FB_Metals_ColdRolling_6StandTandem_HAGC
(*
 ==========================================================================================
  LUMINA CYBER-PHYSICAL AUTOMATION KERNEL - ADVANCED METALLURGY & STEEL ROLLING SUITE
 ==========================================================================================
  SYSTEM IDENTIFIER:   6-STAND CONTINUOUS TANDEM COLD ROLLING MILL (TCM)
  EQUIPMENT TAG:       STAND-06 FINISHING / INTER-STAND 5-6 / HYDRAULIC AGC SERVO COMPLEX
  APPLICATION:         ULTRA-HIGH PRECISION STEEL STRIP THICKNESS & TENSION COUPLING
                       STRIP WIDTH: 1,850 mm | ENTRY: 4.500 mm | EXIT: 0.180 mm
                       MAXIMUM LINE SPEED: 1,800 m/min (30.0 m/s) | DISCRETE CYCLE: 1.0 ms
 ------------------------------------------------------------------------------------------
  CORE CYBER-PHYSICAL DISCIPLINES IMPLEMENTED:
   1. BLAND-FORD-ELLIS NON-LINEAR COLD ROLLING DEFORMATION & HITCHCOCK FLATTENING
   2. BISRA GAUGE-METER MILL SPRING HOUSING STIFFNESS COMPENSATOR (M = 4,850 kN/mm)
   3. 8x8 DISCRETE-TIME STATE-SPACE DYNAMICS: x[k+1] = A*x[k] + B*u[k], y[k] = C*x[k] + D*u[k]
   4. RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) WITH QUADRATIC COST OPTIMIZATION
   5. RECURSIVE KALMAN FILTER DYNAMIC ROLL ECCENTRICITY HARMONIC EXTRACTION (1st, 2nd, 3rd)
   6. HYDRODYNAMIC MORGOIL BEARING OIL FILM WEDGE DYNAMIC COMPENSATOR
   7. DECOUPLED HIGH-SPEED HYDRAULIC PUSH-UP SERVO CYLINDER LEVELING / TILT CONTROL
   8. 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) VOTING & FAULT DEGRADATION LADDER (5 CHANNELS)
   9. 12-STAGE FINITE STATE MACHINE (FSM) COVERING THREADING, ACCEL, FLYING GAUGE, QUICK-OPEN
  10. ISA-18.2 MULTI-TIER ALARM SYSTEM, MILL CHATTER SPECTRUM DETECTOR & FIRST-OUT CAPTURE
 ==========================================================================================
*)
""")

    # VAR_INPUT
    sections.append("""VAR_INPUT
    (* ==================================================================================== *)
    (* === SENSOR TRANSMITTER TRIPLETS (2oo3 TRIPLE MODULAR REDUNDANCY)                  === *)
    (* ==================================================================================== *)
    (* Stand 6 Exit Fast X-Ray Isotope Strip Thickness Transmitters [mm] *)
    XT_XRAY_GAUGE_EXIT_401A         : REAL; (* Exit X-Ray Gauge Stand 6 Channel A [mm] *)
    XT_XRAY_GAUGE_EXIT_401B         : REAL; (* Exit X-Ray Gauge Stand 6 Channel B [mm] *)
    XT_XRAY_GAUGE_EXIT_401C         : REAL; (* Exit X-Ray Gauge Stand 6 Channel C [mm] *)

    (* Stand 6 Total Roll Separating Force Piezoelectric Load Cell Triplet [kN] *)
    WT_ROLL_FORCE_LOADCELL_201A     : REAL; (* Roll Force Load Cell Channel A [kN] *)
    WT_ROLL_FORCE_LOADCELL_201B     : REAL; (* Roll Force Load Cell Channel B [kN] *)
    WT_ROLL_FORCE_LOADCELL_201C     : REAL; (* Roll Force Load Cell Channel C [kN] *)

    (* Stand 6 Operator Side (OS) Hydraulic Push-Up Cylinder LVDT Position Triplet [mm] *)
    ZT_HAGC_POS_STAND1_101A         : REAL; (* Push-Up Cylinder LVDT OS Channel A [mm] *)
    ZT_HAGC_POS_STAND1_101B         : REAL; (* Push-Up Cylinder LVDT OS Channel B [mm] *)
    ZT_HAGC_POS_STAND1_101C         : REAL; (* Push-Up Cylinder LVDT OS Channel C [mm] *)

    (* Stand 6 Drive Side (DS) Hydraulic Push-Up Cylinder LVDT Position Triplet [mm] *)
    ZT_HAGC_POS_STAND1_102A         : REAL; (* Push-Up Cylinder LVDT DS Channel A [mm] *)
    ZT_HAGC_POS_STAND1_102B         : REAL; (* Push-Up Cylinder LVDT DS Channel B [mm] *)
    ZT_HAGC_POS_STAND1_102C         : REAL; (* Push-Up Cylinder LVDT DS Channel C [mm] *)

    (* Interstand 5-6 Looperless Tensiometer Roll Force Sensor Triplet [kN] *)
    ZT_INTERSTAND_TENSION_601A      : REAL; (* Interstand Tensiometer Channel A [kN] *)
    ZT_INTERSTAND_TENSION_601B      : REAL; (* Interstand Tensiometer Channel B [kN] *)
    ZT_INTERSTAND_TENSION_601C      : REAL; (* Interstand Tensiometer Channel C [kN] *)

    (* Hydraulic Push-Up Cylinder Cap-End (Head) Pressure Transmitter Triplet [bar] *)
    PT_SERVO_CYLINDER_HEAD_701A     : REAL; (* Cylinder Cap-End Pressure Channel A [bar] *)
    PT_SERVO_CYLINDER_HEAD_701B     : REAL; (* Cylinder Cap-End Pressure Channel B [bar] *)
    PT_SERVO_CYLINDER_HEAD_701C     : REAL; (* Cylinder Cap-End Pressure Channel C [bar] *)

    (* Hydraulic Push-Up Cylinder Rod-End Pressure Transmitter Triplet [bar] *)
    PT_SERVO_CYLINDER_ROD_702A      : REAL; (* Cylinder Rod-End Pressure Channel A [bar] *)
    PT_SERVO_CYLINDER_ROD_702B      : REAL; (* Cylinder Rod-End Pressure Channel B [bar] *)
    PT_SERVO_CYLINDER_ROD_702C      : REAL; (* Cylinder Rod-End Pressure Channel C [bar] *)

    (* Work Roll Main Drive High-Precision Optical Resolver Triplet [m/min] *)
    ST_ROLL_SPEED_RESOLVER_501A     : REAL; (* Work Roll Linear Surface Speed Ch A [m/min] *)
    ST_ROLL_SPEED_RESOLVER_501B     : REAL; (* Work Roll Linear Surface Speed Ch B [m/min] *)
    ST_ROLL_SPEED_RESOLVER_501C     : REAL; (* Work Roll Linear Surface Speed Ch C [m/min] *)

    (* Strip Entry Pyrometer Infrared Temperature Sensor Triplet [deg C] *)
    TT_STRIP_ENTRY_301A             : REAL; (* Strip Entry Temperature Ch A [deg C] *)
    TT_STRIP_ENTRY_301B             : REAL; (* Strip Entry Temperature Ch B [deg C] *)
    TT_STRIP_ENTRY_301C             : REAL; (* Strip Entry Temperature Ch C [deg C] *)

    (* ==================================================================================== *)
    (* === PROCESS RECIPE TARGETS & METALLURGICAL PARAMETERS                             === *)
    (* ==================================================================================== *)
    rStripWidth_mm                  : REAL; (* Width of steel strip in bite [mm] *)
    rEntryThicknessNom_mm           : REAL; (* Stand 6 Nominal Entry Strip Thickness [mm] *)
    rTargetExitThickness_mm         : REAL; (* Target Delivery Strip Thickness [mm] *)
    rTargetInterstandTension_MPa    : REAL; (* Specific Interstand Target Tension [MPa] *)
    rSteelYoungsModulus_GPa         : REAL; (* Strip Material Young's Modulus [GPa] *)
    rStripBaseYieldStress_MPa       : REAL; (* Annealed Base Yield Stress sigma_0 [MPa] *)
    rStripHardeningExponent_n       : REAL; (* Work Hardening Exponent n [-] *)
    rStripHardeningCoeff_B          : REAL; (* Hardening Coefficient B [-] *)
    rMillHousingModulus_kN_mm       : REAL; (* Measured Mill Modulus Housing Stiffness [kN/mm] *)
    rHydraulicSupplyPressure_bar    : REAL; (* Main Hydraulic Header Pressure [bar] *)

    (* ==================================================================================== *)
    (* === MILL CHATTER SPECTRUM ACCELERATION SENSORS                                    === *)
    (* ==================================================================================== *)
    rVibration_3rdOctave_RMS        : REAL; (* Stand 6 Torsional Chatter RMS (120-180 Hz) [m/s2] *)
    rVibration_5thOctave_RMS        : REAL; (* Stand 6 Acoustic Chatter RMS (500-700 Hz) [m/s2] *)

    (* ==================================================================================== *)
    (* === OPERATOR SUPERVISORY COMMANDS & SAFETY INTERLOCKS                            === *)
    (* ==================================================================================== *)
    bEnableHAGC                     : BOOL; (* Master Automatic Gauge Control Enable *)
    bEmergencyStop                  : BOOL; (* Fail-Safe Safety Circuit E-Stop Tripped *)
    bQuickOpenCmd                   : BOOL; (* Fast Hydraulic Cylinder Dump Command *)
    bFlyingGaugeTrigger             : BOOL; (* Flying Gauge Change Strobe Trigger *)
    rFlyingGaugeNewTarget_mm        : REAL; (* Next Strip Target Thickness [mm] *)
    bRollKissingCalibReq            : BOOL; (* Mill Zeroing & Modulus Kiss Calibration Trigger *)
    bTailOutDetected                : BOOL; (* Coil End / Tail Out Sensor Trigger *)
    bStripBreakSens                 : BOOL; (* Optical Strip Break / Cobble Sensor *)
    bRollBendingAutoEnable          : BOOL; (* Work Roll Crown Bending Closed-Loop Enable *)
    bEccentricityCompEnable         : BOOL; (* Dynamic Kalman Roll Eccentricity Filter Enable *)
    bResetTripAlarms                : BOOL; (* Alarm Manual Acknowledge & Reset Command *)
END_VAR
""")

    # VAR_OUTPUT
    sections.append("""VAR_OUTPUT
    (* ==================================================================================== *)
    (* === ACTUATOR COMMANDS & HIGH-SPEED DRIVE REFERENCES                              === *)
    (* ==================================================================================== *)
    rServoValveSpoolCmd_OS_mA       : REAL; (* Push-Up Cylinder Servo Valve Spool OS [mA] *)
    rServoValveSpoolCmd_DS_mA       : REAL; (* Push-Up Cylinder Servo Valve Spool DS [mA] *)
    rRollBendingPressureCmd_bar     : REAL; (* Work Roll Hydraulic Bending Cylinder [bar] *)
    rMainDriveSpeedTrim_mpm         : REAL; (* Stand 6 Main Drive Motor Trim [m/min] *)
    rStand5SpeedTrim_mpm            : REAL; (* Stand 5 Main Drive Motor Trim [m/min] *)
    bQuickOpenActive                : BOOL; (* Hydraulic Dump Valve Fast Retract Active *)
    bCoolantHeaderShutoffCmd        : BOOL; (* Work Roll Emulsion Coolant Emergency Cutoff *)

    (* ==================================================================================== *)
    (* === MEASURED PROCESS VALUES & ESTIMATED CYBER-PHYSICAL STATES                    === *)
    (* ==================================================================================== *)
    rExitThicknessMeasured_mm       : REAL; (* 2oo3 Voted Stand 6 Exit Thickness [mm] *)
    rGaugeError_um                  : REAL; (* Strip Delivery Thickness Deviation [um] *)
    rVotedRollForce_kN              : REAL; (* 2oo3 Voted Total Roll Separating Force [kN] *)
    rVotedInterstandTension_kN      : REAL; (* 2oo3 Voted Interstand Strip Tension [kN] *)
    rActualSpecificTension_MPa      : REAL; (* Calculated Interstand Specific Stress [MPa] *)
    rMillSpringCompensation_mm      : REAL; (* Real-time Calculated Mill Elastic Stretch [mm] *)
    rRollEccentricityCorrection_mm  : REAL; (* Real-time Kalman Filter Eccentricity Feedforward [mm] *)
    rRollThermalExpansion_mm        : REAL; (* Real-time Work Roll Thermal Crown Expansion [mm] *)
    rHydrodynamicBearingWedge_mm    : REAL; (* Oil Film Thickness Dynamic Compensation [mm] *)
    rForwardSlipRatio               : REAL; (* Calculated Forward Slip Coefficient f_s [-] *)
    rNeutralAngle_rad               : REAL; (* Neutral Plane Angular Position alpha_n [rad] *)
    rFlattenedRollRadius_mm         : REAL; (* Hitchcock Deformed Roll Radius R' [mm] *)

    (* ==================================================================================== *)
    (* === SYSTEM INTEGRITY & DIAGNOSTIC TELEMETRY                                      === *)
    (* ==================================================================================== *)
    iCurrentFSMState                : INT;   (* Active 12-Stage State Machine State [0..11] *)
    bHAGC_InRegulation              : BOOL;  (* True if Exit Thickness Error <= 0.0015 mm *)
    bCobbleInterlockActive          : BOOL;  (* Strip Snap / Mill Cobble Trip Engaged *)
    bChatterVibrationWarning        : BOOL;  (* Mill 3rd/5th Octave Resonance Suppressor Active *)
    dwMillDiagnosticWord1           : DWORD; (* Primary Diagnostic Bitmask Word 1 *)
    dwMillDiagnosticWord2           : DWORD; (* Secondary Diagnostic Bitmask Word 2 *)
    dwAlarmStatusWord               : DWORD; (* ISA-18.2 Active Alarm Bitmask Word *)
END_VAR
""")

    # VAR (Internal variables)
    sections.append("""VAR
    (* ==================================================================================== *)
    (* === DISCRETE 8x8 STATE-SPACE MATRICES & OBSERVER STATE (Ts = 0.001 s)            === *)
    (* ==================================================================================== *)
    A_ss                            : ARRAY[1..8, 1..8] OF REAL; (* Discrete State Transition Matrix *)
    B_ss                            : ARRAY[1..8, 1..3] OF REAL; (* Discrete Actuator Input Gain Matrix *)
    C_ss                            : ARRAY[1..4, 1..8] OF REAL; (* Discrete Measurement Matrix *)
    D_ss                            : ARRAY[1..4, 1..3] OF REAL; (* Discrete Direct Transmission Matrix *)
    L_obs                           : ARRAY[1..8, 1..4] OF REAL; (* Luenberger Observer Feedback Matrix *)
    x_state                         : ARRAY[1..8] OF REAL;       (* Dynamic State Vector: [dh, dsigma, dy_os, dy_ds, dv_os, dv_ds, dfs, dF] *)
    x_pred                          : ARRAY[1..8] OF REAL;       (* One-Step Ahead State Prediction Vector *)
    y_meas                          : ARRAY[1..4] OF REAL;       (* Measured Output Vector: [h_exit_dev, sigma_dev, y_avg_cyl, F_dev] *)
    y_pred                          : ARRAY[1..4] OF REAL;       (* Predicted Output Vector *)
    u_ctrl                          : ARRAY[1..3] OF REAL;       (* Control Input Vector: [spool_os, spool_ds, speed_trim] *)
    u_prev                          : ARRAY[1..3] OF REAL;       (* Previous Step Control Vector *)
    delta_u                         : ARRAY[1..3] OF REAL;       (* Actuator Rate of Change Vector *)

    (* ==================================================================================== *)
    (* === MODEL PREDICTIVE CONTROL (MPC) WEIGHTS & RECEDING-HORIZON SOLVER             === *)
    (* ==================================================================================== *)
    Q_mpc                           : ARRAY[1..8] OF REAL;       (* Diagonal State Penalty Matrix Q *)
    R_mpc                           : ARRAY[1..3] OF REAL;       (* Diagonal Actuator Magnitude Penalty R *)
    S_mpc                           : ARRAY[1..3] OF REAL;       (* Diagonal Actuator Slew Rate Penalty S *)
    P_mpc                           : ARRAY[1..8] OF REAL;       (* Diagonal Terminal Cost Penalty P *)
    r_ref                           : ARRAY[1..8] OF REAL;       (* Target State Reference Vector *)
    x_horiz                         : ARRAY[1..8, 1..8] OF REAL; (* Multi-Step Prediction Trajectory [state, step] *)
    u_cand                          : ARRAY[1..3] OF REAL;       (* Candidate Control Vector in Optimization *)
    grad_J                          : ARRAY[1..3] OF REAL;       (* Cost Functional Gradient Vector *)
    rMpcStepSize                    : REAL := 0.045;             (* Projected Gradient Descent Learning Rate *)
    rCostFunctional                 : REAL;                      (* Accumulated MPC Quadratic Cost J *)

    (* ==================================================================================== *)
    (* === DYNAMIC ROLL ECCENTRICITY RECURSIVE KALMAN FILTER (6-STATE HARMONIC)         === *)
    (* ==================================================================================== *)
    x_ecc                           : ARRAY[1..6] OF REAL;       (* Harmonic Coefficients: [1c, 1s, 2c, 2s, 3c, 3s] *)
    P_cov                           : ARRAY[1..6, 1..6] OF REAL; (* Error Covariance Matrix *)
    Q_proc                          : ARRAY[1..6] OF REAL;       (* Process Noise Covariance (Diagonal) *)
    R_meas                          : REAL := 0.00045;           (* Measurement Noise Covariance *)
    H_vec                           : ARRAY[1..6] OF REAL;       (* Time-Varying Measurement Vector *)
    K_gain                          : ARRAY[1..6] OF REAL;       (* Optimal Kalman Filter Gain Vector *)
    rRollAngleRad                   : REAL := 0.0;               (* Backup Roll Angular Position theta [rad] *)
    rBackupRollRadius_mm            : REAL := 750.0;             (* Backup Roll Nominal Radius [mm] *)
    rWorkRollRadius_mm              : REAL := 260.0;             (* Work Roll Nominal Radius [mm] *)
    rRollEccentricityFeedforward    : REAL := 0.0;               (* Estimated Gap Eccentricity Compensation [mm] *)

    (* ==================================================================================== *)
    (* === 2oo3 TMR SENSOR VOTING STRUCTURES & DISCREPANCY TIMERS                       === *)
    (* ==================================================================================== *)
    (* X-Ray Thickness Gauge TMR *)
    rVotedXrayThickness             : REAL;
    bXray_AB_Discrepancy            : BOOL;
    bXray_BC_Discrepancy            : BOOL;
    bXray_AC_Discrepancy            : BOOL;
    rXrayTimer_AB_ms                : REAL := 0.0;
    rXrayTimer_BC_ms                : REAL := 0.0;
    rXrayTimer_AC_ms                : REAL := 0.0;
    bXray_ChA_Fault                 : BOOL := FALSE;
    bXray_ChB_Fault                 : BOOL := FALSE;
    bXray_ChC_Fault                 : BOOL := FALSE;
    bXray_Degraded1oo2              : BOOL := FALSE;
    bXray_CompleteFailure           : BOOL := FALSE;

    (* Roll Force Load Cell TMR *)
    rVotedRollForce                 : REAL;
    bForce_AB_Discrepancy           : BOOL;
    bForce_BC_Discrepancy           : BOOL;
    bForce_AC_Discrepancy           : BOOL;
    rForceTimer_AB_ms               : REAL := 0.0;
    rForceTimer_BC_ms               : REAL := 0.0;
    rForceTimer_AC_ms               : REAL := 0.0;
    bForce_ChA_Fault                : BOOL := FALSE;
    bForce_ChB_Fault                : BOOL := FALSE;
    bForce_ChC_Fault                : BOOL := FALSE;
    bForce_Degraded1oo2             : BOOL := FALSE;
    bForce_CompleteFailure          : BOOL := FALSE;

    (* Push-Up Cylinder LVDT OS TMR *)
    rVotedPosOS                     : REAL;
    bPosOS_AB_Discrepancy           : BOOL;
    bPosOS_BC_Discrepancy           : BOOL;
    bPosOS_AC_Discrepancy           : BOOL;
    rPosOSTimer_AB_ms               : REAL := 0.0;
    rPosOSTimer_BC_ms               : REAL := 0.0;
    rPosOSTimer_AC_ms               : REAL := 0.0;
    bPosOS_ChA_Fault                : BOOL := FALSE;
    bPosOS_ChB_Fault                : BOOL := FALSE;
    bPosOS_ChC_Fault                : BOOL := FALSE;
    bPosOS_Degraded1oo2             : BOOL := FALSE;
    bPosOS_CompleteFailure          : BOOL := FALSE;

    (* Push-Up Cylinder LVDT DS TMR *)
    rVotedPosDS                     : REAL;
    bPosDS_AB_Discrepancy           : BOOL;
    bPosDS_BC_Discrepancy           : BOOL;
    bPosDS_AC_Discrepancy           : BOOL;
    rPosDSTimer_AB_ms               : REAL := 0.0;
    rPosDSTimer_BC_ms               : REAL := 0.0;
    rPosDSTimer_AC_ms               : REAL := 0.0;
    bPosDS_ChA_Fault                : BOOL := FALSE;
    bPosDS_ChB_Fault                : BOOL := FALSE;
    bPosDS_ChC_Fault                : BOOL := FALSE;
    bPosDS_Degraded1oo2             : BOOL := FALSE;
    bPosDS_CompleteFailure          : BOOL := FALSE;

    (* Interstand Tensiometer TMR *)
    rVotedTension                   : REAL;
    bTens_AB_Discrepancy            : BOOL;
    bTens_BC_Discrepancy            : BOOL;
    bTens_AC_Discrepancy            : BOOL;
    rTensTimer_AB_ms                : REAL := 0.0;
    rTensTimer_BC_ms                : REAL := 0.0;
    rTensTimer_AC_ms                : REAL := 0.0;
    bTens_ChA_Fault                 : BOOL := FALSE;
    bTens_ChB_Fault                 : BOOL := FALSE;
    bTens_ChC_Fault                 : BOOL := FALSE;
    bTens_Degraded1oo2              : BOOL := FALSE;
    bTens_CompleteFailure           : BOOL := FALSE;

    (* Hydraulic Cap-End Pressure TMR *)
    rVotedHeadPres                  : REAL;
    bHeadPres_AB_Discrepancy        : BOOL;
    bHeadPres_BC_Discrepancy        : BOOL;
    bHeadPres_AC_Discrepancy        : BOOL;
    rHeadPresTimer_AB_ms            : REAL := 0.0;
    rHeadPresTimer_BC_ms            : REAL := 0.0;
    rHeadPresTimer_AC_ms            : REAL := 0.0;
    bHeadPres_ChA_Fault             : BOOL := FALSE;
    bHeadPres_ChB_Fault             : BOOL := FALSE;
    bHeadPres_ChC_Fault             : BOOL := FALSE;
    bHeadPres_Degraded1oo2          : BOOL := FALSE;
    bHeadPres_CompleteFailure       : BOOL := FALSE;

    (* Work Roll Speed Resolver TMR *)
    rVotedRollSpeed_mpm             : REAL;
    bSpeed_AB_Discrepancy           : BOOL;
    bSpeed_BC_Discrepancy           : BOOL;
    bSpeed_AC_Discrepancy           : BOOL;
    rSpeedTimer_AB_ms               : REAL := 0.0;
    rSpeedTimer_BC_ms               : REAL := 0.0;
    rSpeedTimer_AC_ms               : REAL := 0.0;
    bSpeed_ChA_Fault                : BOOL := FALSE;
    bSpeed_ChB_Fault                : BOOL := FALSE;
    bSpeed_ChC_Fault                : BOOL := FALSE;
    bSpeed_Degraded1oo2             : BOOL := FALSE;

    (* ==================================================================================== *)
    (* === CYBER-PHYSICAL DEFORMATION & METALLURGY INTERNALS                            === *)
    (* ==================================================================================== *)
    rStripEntryThickness_mm         : REAL := 0.245;  (* Dynamic Stand 6 Entry Thickness [mm] *)
    rDraught_mm                     : REAL;           (* Reduction in bite: h_in - h_out [mm] *)
    rTrueStrain                     : REAL;           (* True logarithmic thickness strain [-] *)
    rFlowStress_MPa                 : REAL;           (* Mean dynamic plastic flow stress [MPa] *)
    rFrictionCoeff_mu               : REAL := 0.038;  (* Dynamic lubricated rolling friction [-] *)
    rHitchcockRadius_mm             : REAL;           (* Flattened roll radius R' [mm] *)
    rRollBiteLength_mm              : REAL;           (* Contact arc length Ld = sqrt(R'*dh) [mm] *)
    rNeutralAngleVal                : REAL;           (* Neutral plane angle alpha_n [rad] *)
    rForwardSlipVal                 : REAL;           (* Forward slip ratio f_s [-] *)
    rBackwardSlipVal                : REAL;           (* Backward slip ratio b_s [-] *)
    rCalculatedRollForce_kN         : REAL;           (* Theoretical Bland-Ford Roll Force [kN] *)
    rMillSpringStretch_mm           : REAL;           (* Elastic housing extension F / M [mm] *)
    rRollThermalCrown_mm            : REAL := 0.015;  (* Accumulated thermal crown expansion [mm] *)
    rOilFilmThickness_mm            : REAL := 0.042;  (* Hydrodynamic Morgoil wedge thickness [mm] *)
    rZeroKissForce_kN               : REAL := 3500.0; (* Reference zeroing kiss force [kN] *)
    rZeroGapOffset_mm               : REAL := 0.0;    (* Calibrated mechanical zero datum [mm] *)

    (* ==================================================================================== *)
    (* === HYDRAULIC SERVO VALVE & CYLINDER ACTUATION INTERNALS                         === *)
    (* ==================================================================================== *)
    rCylHeadArea_m2                 : REAL := 0.5674; (* Head Area: bore 850 mm -> 0.5674 m2 *)
    rCylRodArea_m2                  : REAL := 0.2848; (* Rod Area: rod 600 mm -> 0.2848 m2 net *)
    rHydraulicBulkModulus_bar       : REAL := 14500.0;(* Mobil DTE 24 Hydraulic Oil Bulk Modulus *)
    rOilDensity_kg_m3               : REAL := 875.0;  (* Oil mass density [kg/m3] *)
    rServoValveFlowGain             : REAL := 2.45;   (* Flow factor [L/min/mA @ 70 bar drop] *)
    rSpoolPosOS_mA                  : REAL := 0.0;
    rSpoolPosDS_mA                  : REAL := 0.0;
    rDitherSignal_mA                : REAL := 0.0;    (* 400 Hz anti-stiction dither current *)
    rDitherPhase                    : REAL := 0.0;
    rCylPositionOS_target           : REAL := 0.0;
    rCylPositionDS_target           : REAL := 0.0;
    rCylPositionAvg_target          : REAL := 0.0;
    rCylTiltDiff_target             : REAL := 0.0;
    rRollBendingCmd_bar             : REAL := 120.0;

    (* ==================================================================================== *)
    (* === FINITE STATE MACHINE (FSM) VARIABLES                                         === *)
    (* ==================================================================================== *)
    iFSM_State                      : INT := 1;       (* 0:ZERO, 1:WARMUP, 2:THREAD, 3:TENS_ESTAB, 4:ACCEL, 5:STEADY, 6:FLY_GAUGE, 7:TAIL_OUT, 8:COBBLE, 9:QUICK_OPEN, 10:MAINT, 11:ESTOP *)
    rFSM_StateTimer_ms              : REAL := 0.0;
    rRampTargetSpeed_mpm            : REAL := 1800.0;
    rRampCurrentSpeed_mpm           : REAL := 0.0;
    rRampAcceleration_mpm_s         : REAL := 72.0;   (* 1.2 m/s2 acceleration rate *)
    rFlyingGaugeTransitionTimer_ms  : REAL := 0.0;
    rFlyingGaugeInitialGauge_mm     : REAL := 0.180;
    rFlyingGaugeTargetGauge_mm      : REAL := 0.180;
    bFlyingGaugeActive              : BOOL := FALSE;
    bKissCalibInProgress            : BOOL := FALSE;
    rKissCalibTimer_ms              : REAL := 0.0;

    (* ==================================================================================== *)
    (* === ISA-18.2 ALARM ENGINE & CHATTER INTERLOCKS                                   === *)
    (* ==================================================================================== *)
    rPrevExitThickness_mm           : REAL := 0.180;
    rThicknessRateOfChange_mm_s     : REAL := 0.0;
    rPrevRollForce_kN               : REAL := 15000.0;
    rForceRateOfChange_kN_s         : REAL := 0.0;
    rPrevHeadPres_bar               : REAL := 160.0;
    rHeadPresRateOfChange_bar_s     : REAL := 0.0;

    (* Thickness Alarm Bits *)
    bAlarm_Thickness_HI_HI          : BOOL := FALSE; (* Exceeds +6.0 um *)
    bAlarm_Thickness_HI             : BOOL := FALSE; (* Exceeds +2.5 um *)
    bAlarm_Thickness_LO             : BOOL := FALSE; (* Below -2.5 um *)
    bAlarm_Thickness_LO_LO          : BOOL := FALSE; (* Below -6.0 um *)
    bAlarm_Thickness_ROC            : BOOL := FALSE; (* Rate > 15 um/s *)

    (* Force Alarm Bits *)
    bAlarm_Force_HI_HI              : BOOL := FALSE; (* Exceeds 28,000 kN *)
    bAlarm_Force_HI                 : BOOL := FALSE; (* Exceeds 25,000 kN *)
    bAlarm_Force_LO                 : BOOL := FALSE; (* Below 4,000 kN *)
    bAlarm_Force_LO_LO              : BOOL := FALSE; (* Below 1,500 kN *)
    bAlarm_Force_ROC                : BOOL := FALSE; (* Rate > 8,000 kN/s *)

    (* Tension Alarm Bits *)
    bAlarm_Tension_HI_HI            : BOOL := FALSE; (* Exceeds 220 MPa *)
    bAlarm_Tension_HI               : BOOL := FALSE; (* Exceeds 160 MPa *)
    bAlarm_Tension_LO               : BOOL := FALSE; (* Below 40 MPa *)
    bAlarm_Tension_LO_LO            : BOOL := FALSE; (* Below 15 MPa *)
    bAlarm_Tension_ROC              : BOOL := FALSE; (* Rate > 100 MPa/s *)

    (* Hydraulic Pressure Alarm Bits *)
    bAlarm_HydPres_HI_HI            : BOOL := FALSE; (* Exceeds 315 bar *)
    bAlarm_HydPres_HI               : BOOL := FALSE; (* Exceeds 290 bar *)
    bAlarm_HydPres_LO               : BOOL := FALSE; (* Below 30 bar *)
    bAlarm_HydPres_LO_LO            : BOOL := FALSE; (* Below 10 bar *)
    bAlarm_HydPres_Rupture_ROC      : BOOL := FALSE; (* Drop rate > 150 bar/s *)

    (* Mill Chatter Resonance Bits *)
    bAlarm_Chatter_3rdOctave_Trip   : BOOL := FALSE; (* Torsional mill resonance *)
    bAlarm_Chatter_5thOctave_Warn   : BOOL := FALSE; (* Acoustic roll bite resonance *)

    (* First-Out Latching Register *)
    iFirstOutFaultCode              : INT := 0;

    (* Constant Discrepancy & Threshold Limits *)
    c_rXrayDiscrepancyThreshold_mm  : REAL := 0.0008; (* 0.8 um max discrepancy *)
    c_rForceDiscrepancyThreshold_kN : REAL := 15.0;   (* 15.0 kN max discrepancy *)
    c_rPosDiscrepancyThreshold_mm   : REAL := 0.0020; (* 2.0 um max discrepancy *)
    c_rTensDiscrepancyThreshold_kN  : REAL := 5.0;    (* 5.0 kN max discrepancy *)
    c_rPresDiscrepancyThreshold_bar : REAL := 2.5;    (* 2.5 bar max discrepancy *)
    c_rSpeedDiscrepancyThreshold_mpm: REAL := 2.0;    (* 2.0 m/min max discrepancy *)
    c_rDiscrepancyTimeout_ms        : REAL := 50.0;   (* 50 ms validation debounce *)
    c_rPi                           : REAL := 3.141592653589793;
    c_rTs                           : REAL := 0.001;  (* 1.0 ms fast task period [s] *)
    c_rMillStandModulusNominal      : REAL := 4850.0; (* 4850 kN/mm baseline housing modulus *)

    (* Iteration & Helper Counters *)
    iIterMpc                        : INT;
    iStateIdx                       : INT;
    jStateIdx                       : INT;
    kStepIdx                        : INT;
    iHarmonicIdx                    : INT;
    rMatAccum                       : REAL;
    rGradStepOS                     : REAL;
    rGradStepDS                     : REAL;
    rGradStepSpeed                  : REAL;
    rTempSqrtVal                    : REAL;
    bInitialized                    : BOOL := FALSE;
END_VAR
""")

    return "".join(sections)

print("Builder base loaded.")


def get_phase1_tmr():
    return """
(* ========================================================================================= *)
(* === PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING & INTEGRITY ENGINE    === *)
(* ========================================================================================= *)
(* 
   High-integrity 2-out-of-3 majority voting for all mission-critical transmitters.
   Implements continuous channel cross-comparison, discrepancy accumulation timers (50 ms),
   graceful degradation from 2oo3 to 1oo2, channel isolation bitmasks, and fail-safe latching.
*)

(* --- 1.1 Fast X-Ray Isotope Strip Thickness Gauge (Stand 6 Exit) [mm] --- *)
bXray_AB_Discrepancy := ABS(XT_XRAY_GAUGE_EXIT_401A - XT_XRAY_GAUGE_EXIT_401B) > c_rXrayDiscrepancyThreshold_mm;
bXray_BC_Discrepancy := ABS(XT_XRAY_GAUGE_EXIT_401B - XT_XRAY_GAUGE_EXIT_401C) > c_rXrayDiscrepancyThreshold_mm;
bXray_AC_Discrepancy := ABS(XT_XRAY_GAUGE_EXIT_401A - XT_XRAY_GAUGE_EXIT_401C) > c_rXrayDiscrepancyThreshold_mm;

IF bXray_AB_Discrepancy THEN
    rXrayTimer_AB_ms := rXrayTimer_AB_ms + (c_rTs * 1000.0);
ELSE
    rXrayTimer_AB_ms := 0.0;
END_IF;

IF bXray_BC_Discrepancy THEN
    rXrayTimer_BC_ms := rXrayTimer_BC_ms + (c_rTs * 1000.0);
ELSE
    rXrayTimer_BC_ms := 0.0;
END_IF;

IF bXray_AC_Discrepancy THEN
    rXrayTimer_AC_ms := rXrayTimer_AC_ms + (c_rTs * 1000.0);
ELSE
    rXrayTimer_AC_ms := 0.0;
END_IF;

(* Isolate faulty channel based on 2-way discrepancy intersection *)
IF (rXrayTimer_AB_ms > c_rDiscrepancyTimeout_ms) AND (rXrayTimer_AC_ms > c_rDiscrepancyTimeout_ms) THEN
    bXray_ChA_Fault := TRUE;
END_IF;
IF (rXrayTimer_AB_ms > c_rDiscrepancyTimeout_ms) AND (rXrayTimer_BC_ms > c_rDiscrepancyTimeout_ms) THEN
    bXray_ChB_Fault := TRUE;
END_IF;
IF (rXrayTimer_AC_ms > c_rDiscrepancyTimeout_ms) AND (rXrayTimer_BC_ms > c_rDiscrepancyTimeout_ms) THEN
    bXray_ChC_Fault := TRUE;
END_IF;

(* Voting synthesis *)
IF NOT bXray_ChA_Fault AND NOT bXray_ChB_Fault AND NOT bXray_ChC_Fault THEN
    (* All channels healthy: median voting *)
    IF (XT_XRAY_GAUGE_EXIT_401A >= XT_XRAY_GAUGE_EXIT_401B AND XT_XRAY_GAUGE_EXIT_401A <= XT_XRAY_GAUGE_EXIT_401C) OR 
       (XT_XRAY_GAUGE_EXIT_401A <= XT_XRAY_GAUGE_EXIT_401B AND XT_XRAY_GAUGE_EXIT_401A >= XT_XRAY_GAUGE_EXIT_401C) THEN
        rVotedXrayThickness := XT_XRAY_GAUGE_EXIT_401A;
    ELSIF (XT_XRAY_GAUGE_EXIT_401B >= XT_XRAY_GAUGE_EXIT_401A AND XT_XRAY_GAUGE_EXIT_401B <= XT_XRAY_GAUGE_EXIT_401C) OR 
          (XT_XRAY_GAUGE_EXIT_401B <= XT_XRAY_GAUGE_EXIT_401A AND XT_XRAY_GAUGE_EXIT_401B >= XT_XRAY_GAUGE_EXIT_401C) THEN
        rVotedXrayThickness := XT_XRAY_GAUGE_EXIT_401B;
    ELSE
        rVotedXrayThickness := XT_XRAY_GAUGE_EXIT_401C;
    END_IF;
    bXray_Degraded1oo2 := FALSE;
    bXray_CompleteFailure := FALSE;
ELSIF bXray_ChA_Fault AND NOT bXray_ChB_Fault AND NOT bXray_ChC_Fault THEN
    (* Channel A failed: 1oo2 average of B and C *)
    rVotedXrayThickness := 0.5 * (XT_XRAY_GAUGE_EXIT_401B + XT_XRAY_GAUGE_EXIT_401C);
    bXray_Degraded1oo2 := TRUE;
ELSIF bXray_ChB_Fault AND NOT bXray_ChA_Fault AND NOT bXray_ChC_Fault THEN
    (* Channel B failed: 1oo2 average of A and C *)
    rVotedXrayThickness := 0.5 * (XT_XRAY_GAUGE_EXIT_401A + XT_XRAY_GAUGE_EXIT_401C);
    bXray_Degraded1oo2 := TRUE;
ELSIF bXray_ChC_Fault AND NOT bXray_ChA_Fault AND NOT bXray_ChB_Fault THEN
    (* Channel C failed: 1oo2 average of A and B *)
    rVotedXrayThickness := 0.5 * (XT_XRAY_GAUGE_EXIT_401A + XT_XRAY_GAUGE_EXIT_401B);
    bXray_Degraded1oo2 := TRUE;
ELSE
    (* Multiple sensor failure: clamp to model predicted thickness *)
    bXray_CompleteFailure := TRUE;
    rVotedXrayThickness := rTargetExitThickness_mm;
END_IF;
rExitThicknessMeasured_mm := rVotedXrayThickness;
rGaugeError_um := (rExitThicknessMeasured_mm - rTargetExitThickness_mm) * 1000.0;


(* --- 1.2 Total Roll Separating Force Load Cells [kN] --- *)
bForce_AB_Discrepancy := ABS(WT_ROLL_FORCE_LOADCELL_201A - WT_ROLL_FORCE_LOADCELL_201B) > c_rForceDiscrepancyThreshold_kN;
bForce_BC_Discrepancy := ABS(WT_ROLL_FORCE_LOADCELL_201B - WT_ROLL_FORCE_LOADCELL_201C) > c_rForceDiscrepancyThreshold_kN;
bForce_AC_Discrepancy := ABS(WT_ROLL_FORCE_LOADCELL_201A - WT_ROLL_FORCE_LOADCELL_201C) > c_rForceDiscrepancyThreshold_kN;

IF bForce_AB_Discrepancy THEN
    rForceTimer_AB_ms := rForceTimer_AB_ms + (c_rTs * 1000.0);
ELSE
    rForceTimer_AB_ms := 0.0;
END_IF;

IF bForce_BC_Discrepancy THEN
    rForceTimer_BC_ms := rForceTimer_BC_ms + (c_rTs * 1000.0);
ELSE
    rForceTimer_BC_ms := 0.0;
END_IF;

IF bForce_AC_Discrepancy THEN
    rForceTimer_AC_ms := rForceTimer_AC_ms + (c_rTs * 1000.0);
ELSE
    rForceTimer_AC_ms := 0.0;
END_IF;

IF (rForceTimer_AB_ms > c_rDiscrepancyTimeout_ms) AND (rForceTimer_AC_ms > c_rDiscrepancyTimeout_ms) THEN
    bForce_ChA_Fault := TRUE;
END_IF;
IF (rForceTimer_AB_ms > c_rDiscrepancyTimeout_ms) AND (rForceTimer_BC_ms > c_rDiscrepancyTimeout_ms) THEN
    bForce_ChB_Fault := TRUE;
END_IF;
IF (rForceTimer_AC_ms > c_rDiscrepancyTimeout_ms) AND (rForceTimer_BC_ms > c_rDiscrepancyTimeout_ms) THEN
    bForce_ChC_Fault := TRUE;
END_IF;

IF NOT bForce_ChA_Fault AND NOT bForce_ChB_Fault AND NOT bForce_ChC_Fault THEN
    IF (WT_ROLL_FORCE_LOADCELL_201A >= WT_ROLL_FORCE_LOADCELL_201B AND WT_ROLL_FORCE_LOADCELL_201A <= WT_ROLL_FORCE_LOADCELL_201C) OR 
       (WT_ROLL_FORCE_LOADCELL_201A <= WT_ROLL_FORCE_LOADCELL_201B AND WT_ROLL_FORCE_LOADCELL_201A >= WT_ROLL_FORCE_LOADCELL_201C) THEN
        rVotedRollForce := WT_ROLL_FORCE_LOADCELL_201A;
    ELSIF (WT_ROLL_FORCE_LOADCELL_201B >= WT_ROLL_FORCE_LOADCELL_201A AND WT_ROLL_FORCE_LOADCELL_201B <= WT_ROLL_FORCE_LOADCELL_201C) OR 
          (WT_ROLL_FORCE_LOADCELL_201B <= WT_ROLL_FORCE_LOADCELL_201A AND WT_ROLL_FORCE_LOADCELL_201B >= WT_ROLL_FORCE_LOADCELL_201C) THEN
        rVotedRollForce := WT_ROLL_FORCE_LOADCELL_201B;
    ELSE
        rVotedRollForce := WT_ROLL_FORCE_LOADCELL_201C;
    END_IF;
    bForce_Degraded1oo2 := FALSE;
    bForce_CompleteFailure := FALSE;
ELSIF bForce_ChA_Fault AND NOT bForce_ChB_Fault AND NOT bForce_ChC_Fault THEN
    rVotedRollForce := 0.5 * (WT_ROLL_FORCE_LOADCELL_201B + WT_ROLL_FORCE_LOADCELL_201C);
    bForce_Degraded1oo2 := TRUE;
ELSIF bForce_ChB_Fault AND NOT bForce_ChA_Fault AND NOT bForce_ChC_Fault THEN
    rVotedRollForce := 0.5 * (WT_ROLL_FORCE_LOADCELL_201A + WT_ROLL_FORCE_LOADCELL_201C);
    bForce_Degraded1oo2 := TRUE;
ELSIF bForce_ChC_Fault AND NOT bForce_ChA_Fault AND NOT bForce_ChB_Fault THEN
    rVotedRollForce := 0.5 * (WT_ROLL_FORCE_LOADCELL_201A + WT_ROLL_FORCE_LOADCELL_201B);
    bForce_Degraded1oo2 := TRUE;
ELSE
    bForce_CompleteFailure := TRUE;
    rVotedRollForce := rCalculatedRollForce_kN;
END_IF;
rVotedRollForce_kN := rVotedRollForce;


(* --- 1.3 Push-Up Cylinder LVDT Position OS [mm] --- *)
bPosOS_AB_Discrepancy := ABS(ZT_HAGC_POS_STAND1_101A - ZT_HAGC_POS_STAND1_101B) > c_rPosDiscrepancyThreshold_mm;
bPosOS_BC_Discrepancy := ABS(ZT_HAGC_POS_STAND1_101B - ZT_HAGC_POS_STAND1_101C) > c_rPosDiscrepancyThreshold_mm;
bPosOS_AC_Discrepancy := ABS(ZT_HAGC_POS_STAND1_101A - ZT_HAGC_POS_STAND1_101C) > c_rPosDiscrepancyThreshold_mm;

IF bPosOS_AB_Discrepancy THEN
    rPosOSTimer_AB_ms := rPosOSTimer_AB_ms + (c_rTs * 1000.0);
ELSE
    rPosOSTimer_AB_ms := 0.0;
END_IF;

IF bPosOS_BC_Discrepancy THEN
    rPosOSTimer_BC_ms := rPosOSTimer_BC_ms + (c_rTs * 1000.0);
ELSE
    rPosOSTimer_BC_ms := 0.0;
END_IF;

IF bPosOS_AC_Discrepancy THEN
    rPosOSTimer_AC_ms := rPosOSTimer_AC_ms + (c_rTs * 1000.0);
ELSE
    rPosOSTimer_AC_ms := 0.0;
END_IF;

IF (rPosOSTimer_AB_ms > c_rDiscrepancyTimeout_ms) AND (rPosOSTimer_AC_ms > c_rDiscrepancyTimeout_ms) THEN
    bPosOS_ChA_Fault := TRUE;
END_IF;
IF (rPosOSTimer_AB_ms > c_rDiscrepancyTimeout_ms) AND (rPosOSTimer_BC_ms > c_rDiscrepancyTimeout_ms) THEN
    bPosOS_ChB_Fault := TRUE;
END_IF;
IF (rPosOSTimer_AC_ms > c_rDiscrepancyTimeout_ms) AND (rPosOSTimer_BC_ms > c_rDiscrepancyTimeout_ms) THEN
    bPosOS_ChC_Fault := TRUE;
END_IF;

IF NOT bPosOS_ChA_Fault AND NOT bPosOS_ChB_Fault AND NOT bPosOS_ChC_Fault THEN
    IF (ZT_HAGC_POS_STAND1_101A >= ZT_HAGC_POS_STAND1_101B AND ZT_HAGC_POS_STAND1_101A <= ZT_HAGC_POS_STAND1_101C) OR 
       (ZT_HAGC_POS_STAND1_101A <= ZT_HAGC_POS_STAND1_101B AND ZT_HAGC_POS_STAND1_101A >= ZT_HAGC_POS_STAND1_101C) THEN
        rVotedPosOS := ZT_HAGC_POS_STAND1_101A;
    ELSIF (ZT_HAGC_POS_STAND1_101B >= ZT_HAGC_POS_STAND1_101A AND ZT_HAGC_POS_STAND1_101B <= ZT_HAGC_POS_STAND1_101C) OR 
          (ZT_HAGC_POS_STAND1_101B <= ZT_HAGC_POS_STAND1_101A AND ZT_HAGC_POS_STAND1_101B >= ZT_HAGC_POS_STAND1_101C) THEN
        rVotedPosOS := ZT_HAGC_POS_STAND1_101B;
    ELSE
        rVotedPosOS := ZT_HAGC_POS_STAND1_101C;
    END_IF;
    bPosOS_Degraded1oo2 := FALSE;
    bPosOS_CompleteFailure := FALSE;
ELSIF bPosOS_ChA_Fault AND NOT bPosOS_ChB_Fault AND NOT bPosOS_ChC_Fault THEN
    rVotedPosOS := 0.5 * (ZT_HAGC_POS_STAND1_101B + ZT_HAGC_POS_STAND1_101C);
    bPosOS_Degraded1oo2 := TRUE;
ELSIF bPosOS_ChB_Fault AND NOT bPosOS_ChA_Fault AND NOT bPosOS_ChC_Fault THEN
    rVotedPosOS := 0.5 * (ZT_HAGC_POS_STAND1_101A + ZT_HAGC_POS_STAND1_101C);
    bPosOS_Degraded1oo2 := TRUE;
ELSIF bPosOS_ChC_Fault AND NOT bPosOS_ChA_Fault AND NOT bPosOS_ChB_Fault THEN
    rVotedPosOS := 0.5 * (ZT_HAGC_POS_STAND1_101A + ZT_HAGC_POS_STAND1_101B);
    bPosOS_Degraded1oo2 := TRUE;
ELSE
    bPosOS_CompleteFailure := TRUE;
    rVotedPosOS := rCylPositionOS_target;
END_IF;


(* --- 1.4 Push-Up Cylinder LVDT Position DS [mm] --- *)
bPosDS_AB_Discrepancy := ABS(ZT_HAGC_POS_STAND1_102A - ZT_HAGC_POS_STAND1_102B) > c_rPosDiscrepancyThreshold_mm;
bPosDS_BC_Discrepancy := ABS(ZT_HAGC_POS_STAND1_102B - ZT_HAGC_POS_STAND1_102C) > c_rPosDiscrepancyThreshold_mm;
bPosDS_AC_Discrepancy := ABS(ZT_HAGC_POS_STAND1_102A - ZT_HAGC_POS_STAND1_102C) > c_rPosDiscrepancyThreshold_mm;

IF bPosDS_AB_Discrepancy THEN
    rPosDSTimer_AB_ms := rPosDSTimer_AB_ms + (c_rTs * 1000.0);
ELSE
    rPosDSTimer_AB_ms := 0.0;
END_IF;

IF bPosDS_BC_Discrepancy THEN
    rPosDSTimer_BC_ms := rPosDSTimer_BC_ms + (c_rTs * 1000.0);
ELSE
    rPosDSTimer_BC_ms := 0.0;
END_IF;

IF bPosDS_AC_Discrepancy THEN
    rPosDSTimer_AC_ms := rPosDSTimer_AC_ms + (c_rTs * 1000.0);
ELSE
    rPosDSTimer_AC_ms := 0.0;
END_IF;

IF (rPosDSTimer_AB_ms > c_rDiscrepancyTimeout_ms) AND (rPosDSTimer_AC_ms > c_rDiscrepancyTimeout_ms) THEN
    bPosDS_ChA_Fault := TRUE;
END_IF;
IF (rPosDSTimer_AB_ms > c_rDiscrepancyTimeout_ms) AND (rPosDSTimer_BC_ms > c_rDiscrepancyTimeout_ms) THEN
    bPosDS_ChB_Fault := TRUE;
END_IF;
IF (rPosDSTimer_AC_ms > c_rDiscrepancyTimeout_ms) AND (rPosDSTimer_BC_ms > c_rDiscrepancyTimeout_ms) THEN
    bPosDS_ChC_Fault := TRUE;
END_IF;

IF NOT bPosDS_ChA_Fault AND NOT bPosDS_ChB_Fault AND NOT bPosDS_ChC_Fault THEN
    IF (ZT_HAGC_POS_STAND1_102A >= ZT_HAGC_POS_STAND1_102B AND ZT_HAGC_POS_STAND1_102A <= ZT_HAGC_POS_STAND1_102C) OR 
       (ZT_HAGC_POS_STAND1_102A <= ZT_HAGC_POS_STAND1_102B AND ZT_HAGC_POS_STAND1_102A >= ZT_HAGC_POS_STAND1_102C) THEN
        rVotedPosDS := ZT_HAGC_POS_STAND1_102A;
    ELSIF (ZT_HAGC_POS_STAND1_102B >= ZT_HAGC_POS_STAND1_102A AND ZT_HAGC_POS_STAND1_102B <= ZT_HAGC_POS_STAND1_102C) OR 
          (ZT_HAGC_POS_STAND1_102B <= ZT_HAGC_POS_STAND1_102A AND ZT_HAGC_POS_STAND1_102B >= ZT_HAGC_POS_STAND1_102C) THEN
        rVotedPosDS := ZT_HAGC_POS_STAND1_102B;
    ELSE
        rVotedPosDS := ZT_HAGC_POS_STAND1_102C;
    END_IF;
    bPosDS_Degraded1oo2 := FALSE;
    bPosDS_CompleteFailure := FALSE;
ELSIF bPosDS_ChA_Fault AND NOT bPosDS_ChB_Fault AND NOT bPosDS_ChC_Fault THEN
    rVotedPosDS := 0.5 * (ZT_HAGC_POS_STAND1_102B + ZT_HAGC_POS_STAND1_102C);
    bPosDS_Degraded1oo2 := TRUE;
ELSIF bPosDS_ChB_Fault AND NOT bPosDS_ChA_Fault AND NOT bPosDS_ChC_Fault THEN
    rVotedPosDS := 0.5 * (ZT_HAGC_POS_STAND1_102A + ZT_HAGC_POS_STAND1_102C);
    bPosDS_Degraded1oo2 := TRUE;
ELSIF bPosDS_ChC_Fault AND NOT bPosDS_ChA_Fault AND NOT bPosDS_ChB_Fault THEN
    rVotedPosDS := 0.5 * (ZT_HAGC_POS_STAND1_102A + ZT_HAGC_POS_STAND1_102B);
    bPosDS_Degraded1oo2 := TRUE;
ELSE
    bPosDS_CompleteFailure := TRUE;
    rVotedPosDS := rCylPositionDS_target;
END_IF;


(* --- 1.5 Interstand 5-6 Tensiometer Triplet [kN] --- *)
bTens_AB_Discrepancy := ABS(ZT_INTERSTAND_TENSION_601A - ZT_INTERSTAND_TENSION_601B) > c_rTensDiscrepancyThreshold_kN;
bTens_BC_Discrepancy := ABS(ZT_INTERSTAND_TENSION_601B - ZT_INTERSTAND_TENSION_601C) > c_rTensDiscrepancyThreshold_kN;
bTens_AC_Discrepancy := ABS(ZT_INTERSTAND_TENSION_601A - ZT_INTERSTAND_TENSION_601C) > c_rTensDiscrepancyThreshold_kN;

IF bTens_AB_Discrepancy THEN
    rTensTimer_AB_ms := rTensTimer_AB_ms + (c_rTs * 1000.0);
ELSE
    rTensTimer_AB_ms := 0.0;
END_IF;

IF bTens_BC_Discrepancy THEN
    rTensTimer_BC_ms := rTensTimer_BC_ms + (c_rTs * 1000.0);
ELSE
    rTensTimer_BC_ms := 0.0;
END_IF;

IF bTens_AC_Discrepancy THEN
    rTensTimer_AC_ms := rTensTimer_AC_ms + (c_rTs * 1000.0);
ELSE
    rTensTimer_AC_ms := 0.0;
END_IF;

IF (rTensTimer_AB_ms > c_rDiscrepancyTimeout_ms) AND (rTensTimer_AC_ms > c_rDiscrepancyTimeout_ms) THEN
    bTens_ChA_Fault := TRUE;
END_IF;
IF (rTensTimer_AB_ms > c_rDiscrepancyTimeout_ms) AND (rTensTimer_BC_ms > c_rDiscrepancyTimeout_ms) THEN
    bTens_ChB_Fault := TRUE;
END_IF;
IF (rTensTimer_AC_ms > c_rDiscrepancyTimeout_ms) AND (rTensTimer_BC_ms > c_rDiscrepancyTimeout_ms) THEN
    bTens_ChC_Fault := TRUE;
END_IF;

IF NOT bTens_ChA_Fault AND NOT bTens_ChB_Fault AND NOT bTens_ChC_Fault THEN
    IF (ZT_INTERSTAND_TENSION_601A >= ZT_INTERSTAND_TENSION_601B AND ZT_INTERSTAND_TENSION_601A <= ZT_INTERSTAND_TENSION_601C) OR 
       (ZT_INTERSTAND_TENSION_601A <= ZT_INTERSTAND_TENSION_601B AND ZT_INTERSTAND_TENSION_601A >= ZT_INTERSTAND_TENSION_601C) THEN
        rVotedTension := ZT_INTERSTAND_TENSION_601A;
    ELSIF (ZT_INTERSTAND_TENSION_601B >= ZT_INTERSTAND_TENSION_601A AND ZT_INTERSTAND_TENSION_601B <= ZT_INTERSTAND_TENSION_601C) OR 
          (ZT_INTERSTAND_TENSION_601B <= ZT_INTERSTAND_TENSION_601A AND ZT_INTERSTAND_TENSION_601B >= ZT_INTERSTAND_TENSION_601C) THEN
        rVotedTension := ZT_INTERSTAND_TENSION_601B;
    ELSE
        rVotedTension := ZT_INTERSTAND_TENSION_601C;
    END_IF;
    bTens_Degraded1oo2 := FALSE;
    bTens_CompleteFailure := FALSE;
ELSIF bTens_ChA_Fault AND NOT bTens_ChB_Fault AND NOT bTens_ChC_Fault THEN
    rVotedTension := 0.5 * (ZT_INTERSTAND_TENSION_601B + ZT_INTERSTAND_TENSION_601C);
    bTens_Degraded1oo2 := TRUE;
ELSIF bTens_ChB_Fault AND NOT bTens_ChA_Fault AND NOT bTens_ChC_Fault THEN
    rVotedTension := 0.5 * (ZT_INTERSTAND_TENSION_601A + ZT_INTERSTAND_TENSION_601C);
    bTens_Degraded1oo2 := TRUE;
ELSIF bTens_ChC_Fault AND NOT bTens_ChA_Fault AND NOT bTens_ChB_Fault THEN
    rVotedTension := 0.5 * (ZT_INTERSTAND_TENSION_601A + ZT_INTERSTAND_TENSION_601B);
    bTens_Degraded1oo2 := TRUE;
ELSE
    bTens_CompleteFailure := TRUE;
    rVotedTension := (rTargetInterstandTension_MPa * rStripWidth_mm * rStripEntryThickness_mm) / 1000.0;
END_IF;
rVotedInterstandTension_kN := rVotedTension;
IF (rStripWidth_mm * rStripEntryThickness_mm) > 0.001 THEN
    rActualSpecificTension_MPa := (rVotedInterstandTension_kN * 1000.0) / (rStripWidth_mm * rStripEntryThickness_mm);
ELSE
    rActualSpecificTension_MPa := 0.0;
END_IF;


(* --- 1.6 Push-Up Cylinder Cap-End Pressure Triplet [bar] --- *)
bHeadPres_AB_Discrepancy := ABS(PT_SERVO_CYLINDER_HEAD_701A - PT_SERVO_CYLINDER_HEAD_701B) > c_rPresDiscrepancyThreshold_bar;
bHeadPres_BC_Discrepancy := ABS(PT_SERVO_CYLINDER_HEAD_701B - PT_SERVO_CYLINDER_HEAD_701C) > c_rPresDiscrepancyThreshold_bar;
bHeadPres_AC_Discrepancy := ABS(PT_SERVO_CYLINDER_HEAD_701A - PT_SERVO_CYLINDER_HEAD_701C) > c_rPresDiscrepancyThreshold_bar;

IF bHeadPres_AB_Discrepancy THEN
    rHeadPresTimer_AB_ms := rHeadPresTimer_AB_ms + (c_rTs * 1000.0);
ELSE
    rHeadPresTimer_AB_ms := 0.0;
END_IF;

IF bHeadPres_BC_Discrepancy THEN
    rHeadPresTimer_BC_ms := rHeadPresTimer_BC_ms + (c_rTs * 1000.0);
ELSE
    rHeadPresTimer_BC_ms := 0.0;
END_IF;

IF bHeadPres_AC_Discrepancy THEN
    rHeadPresTimer_AC_ms := rHeadPresTimer_AC_ms + (c_rTs * 1000.0);
ELSE
    rHeadPresTimer_AC_ms := 0.0;
END_IF;

IF (rHeadPresTimer_AB_ms > c_rDiscrepancyTimeout_ms) AND (rHeadPresTimer_AC_ms > c_rDiscrepancyTimeout_ms) THEN
    bHeadPres_ChA_Fault := TRUE;
END_IF;
IF (rHeadPresTimer_AB_ms > c_rDiscrepancyTimeout_ms) AND (rHeadPresTimer_BC_ms > c_rDiscrepancyTimeout_ms) THEN
    bHeadPres_ChB_Fault := TRUE;
END_IF;
IF (rHeadPresTimer_AC_ms > c_rDiscrepancyTimeout_ms) AND (rHeadPresTimer_BC_ms > c_rDiscrepancyTimeout_ms) THEN
    bHeadPres_ChC_Fault := TRUE;
END_IF;

IF NOT bHeadPres_ChA_Fault AND NOT bHeadPres_ChB_Fault AND NOT bHeadPres_ChC_Fault THEN
    IF (PT_SERVO_CYLINDER_HEAD_701A >= PT_SERVO_CYLINDER_HEAD_701B AND PT_SERVO_CYLINDER_HEAD_701A <= PT_SERVO_CYLINDER_HEAD_701C) OR 
       (PT_SERVO_CYLINDER_HEAD_701A <= PT_SERVO_CYLINDER_HEAD_701B AND PT_SERVO_CYLINDER_HEAD_701A >= PT_SERVO_CYLINDER_HEAD_701C) THEN
        rVotedHeadPres := PT_SERVO_CYLINDER_HEAD_701A;
    ELSIF (PT_SERVO_CYLINDER_HEAD_701B >= PT_SERVO_CYLINDER_HEAD_701A AND PT_SERVO_CYLINDER_HEAD_701B <= PT_SERVO_CYLINDER_HEAD_701C) OR 
          (PT_SERVO_CYLINDER_HEAD_701B <= PT_SERVO_CYLINDER_HEAD_701A AND PT_SERVO_CYLINDER_HEAD_701B >= PT_SERVO_CYLINDER_HEAD_701C) THEN
        rVotedHeadPres := PT_SERVO_CYLINDER_HEAD_701B;
    ELSE
        rVotedHeadPres := PT_SERVO_CYLINDER_HEAD_701C;
    END_IF;
    bHeadPres_Degraded1oo2 := FALSE;
    bHeadPres_CompleteFailure := FALSE;
ELSIF bHeadPres_ChA_Fault AND NOT bHeadPres_ChB_Fault AND NOT bHeadPres_ChC_Fault THEN
    rVotedHeadPres := 0.5 * (PT_SERVO_CYLINDER_HEAD_701B + PT_SERVO_CYLINDER_HEAD_701C);
    bHeadPres_Degraded1oo2 := TRUE;
ELSIF bHeadPres_ChB_Fault AND NOT bHeadPres_ChA_Fault AND NOT bHeadPres_ChC_Fault THEN
    rVotedHeadPres := 0.5 * (PT_SERVO_CYLINDER_HEAD_701A + PT_SERVO_CYLINDER_HEAD_701C);
    bHeadPres_Degraded1oo2 := TRUE;
ELSIF bHeadPres_ChC_Fault AND NOT bHeadPres_ChA_Fault AND NOT bHeadPres_ChB_Fault THEN
    rVotedHeadPres := 0.5 * (PT_SERVO_CYLINDER_HEAD_701A + PT_SERVO_CYLINDER_HEAD_701B);
    bHeadPres_Degraded1oo2 := TRUE;
ELSE
    bHeadPres_CompleteFailure := TRUE;
    rVotedHeadPres := 160.0;
END_IF;


(* --- 1.7 Work Roll Speed Resolver Triplet [m/min] --- *)
bSpeed_AB_Discrepancy := ABS(ST_ROLL_SPEED_RESOLVER_501A - ST_ROLL_SPEED_RESOLVER_501B) > c_rSpeedDiscrepancyThreshold_mpm;
bSpeed_BC_Discrepancy := ABS(ST_ROLL_SPEED_RESOLVER_501B - ST_ROLL_SPEED_RESOLVER_501C) > c_rSpeedDiscrepancyThreshold_mpm;
bSpeed_AC_Discrepancy := ABS(ST_ROLL_SPEED_RESOLVER_501A - ST_ROLL_SPEED_RESOLVER_501C) > c_rSpeedDiscrepancyThreshold_mpm;

IF bSpeed_AB_Discrepancy THEN
    rSpeedTimer_AB_ms := rSpeedTimer_AB_ms + (c_rTs * 1000.0);
ELSE
    rSpeedTimer_AB_ms := 0.0;
END_IF;

IF bSpeed_BC_Discrepancy THEN
    rSpeedTimer_BC_ms := rSpeedTimer_BC_ms + (c_rTs * 1000.0);
ELSE
    rSpeedTimer_BC_ms := 0.0;
END_IF;

IF bSpeed_AC_Discrepancy THEN
    rSpeedTimer_AC_ms := rSpeedTimer_AC_ms + (c_rTs * 1000.0);
ELSE
    rSpeedTimer_AC_ms := 0.0;
END_IF;

IF (rSpeedTimer_AB_ms > c_rDiscrepancyTimeout_ms) AND (rSpeedTimer_AC_ms > c_rDiscrepancyTimeout_ms) THEN
    bSpeed_ChA_Fault := TRUE;
END_IF;
IF (rSpeedTimer_AB_ms > c_rDiscrepancyTimeout_ms) AND (rSpeedTimer_BC_ms > c_rDiscrepancyTimeout_ms) THEN
    bSpeed_ChB_Fault := TRUE;
END_IF;
IF (rSpeedTimer_AC_ms > c_rDiscrepancyTimeout_ms) AND (rSpeedTimer_BC_ms > c_rDiscrepancyTimeout_ms) THEN
    bSpeed_ChC_Fault := TRUE;
END_IF;

IF NOT bSpeed_ChA_Fault AND NOT bSpeed_ChB_Fault AND NOT bSpeed_ChC_Fault THEN
    IF (ST_ROLL_SPEED_RESOLVER_501A >= ST_ROLL_SPEED_RESOLVER_501B AND ST_ROLL_SPEED_RESOLVER_501A <= ST_ROLL_SPEED_RESOLVER_501C) OR 
       (ST_ROLL_SPEED_RESOLVER_501A <= ST_ROLL_SPEED_RESOLVER_501B AND ST_ROLL_SPEED_RESOLVER_501A >= ST_ROLL_SPEED_RESOLVER_501C) THEN
        rVotedRollSpeed_mpm := ST_ROLL_SPEED_RESOLVER_501A;
    ELSIF (ST_ROLL_SPEED_RESOLVER_501B >= ST_ROLL_SPEED_RESOLVER_501A AND ST_ROLL_SPEED_RESOLVER_501B <= ST_ROLL_SPEED_RESOLVER_501C) OR 
          (ST_ROLL_SPEED_RESOLVER_501B <= ST_ROLL_SPEED_RESOLVER_501A AND ST_ROLL_SPEED_RESOLVER_501B >= ST_ROLL_SPEED_RESOLVER_501C) THEN
        rVotedRollSpeed_mpm := ST_ROLL_SPEED_RESOLVER_501B;
    ELSE
        rVotedRollSpeed_mpm := ST_ROLL_SPEED_RESOLVER_501C;
    END_IF;
    bSpeed_Degraded1oo2 := FALSE;
ELSIF bSpeed_ChA_Fault AND NOT bSpeed_ChB_Fault AND NOT bSpeed_ChC_Fault THEN
    rVotedRollSpeed_mpm := 0.5 * (ST_ROLL_SPEED_RESOLVER_501B + ST_ROLL_SPEED_RESOLVER_501C);
    bSpeed_Degraded1oo2 := TRUE;
ELSIF bSpeed_ChB_Fault AND NOT bSpeed_ChA_Fault AND NOT bSpeed_ChC_Fault THEN
    rVotedRollSpeed_mpm := 0.5 * (ST_ROLL_SPEED_RESOLVER_501A + ST_ROLL_SPEED_RESOLVER_501C);
    bSpeed_Degraded1oo2 := TRUE;
ELSIF bSpeed_ChC_Fault AND NOT bSpeed_ChA_Fault AND NOT bSpeed_ChB_Fault THEN
    rVotedRollSpeed_mpm := 0.5 * (ST_ROLL_SPEED_RESOLVER_501A + ST_ROLL_SPEED_RESOLVER_501B);
    bSpeed_Degraded1oo2 := TRUE;
ELSE
    rVotedRollSpeed_mpm := rRampCurrentSpeed_mpm;
END_IF;
"""

print("Phase 1 defined.")


def get_phase2_mechanics():
    return """
(* ========================================================================================= *)
(* === PHASE 2: MILL DEFORMATION, HITCHCOCK FLATTENING & BLAND-FORD-ELLIS MODEL         === *)
(* ========================================================================================= *)
(*
   Physics-informed cyber-physical model of the roll bite deformation zone:
   - Evaluates true logarithmic strain and Ludwik-Hollomon dynamic flow stress.
   - Computes non-linear Coulomb friction coefficient dependent on rolling velocity.
   - Solves Hitchcock's implicit roll flattening equation for deformed radius R'.
   - Solves Bland-Ford-Ellis differential equations for neutral plane angle and forward slip.
   - Calculates BISRA mill spring stretch, Morgoil hydrodynamic oil wedge, and thermal crown.
*)

(* Draught and logarithmic strain *)
rStripEntryThickness_mm := rEntryThicknessNom_mm;
IF rStripEntryThickness_mm < 0.05 THEN
    rStripEntryThickness_mm := 0.245;
END_IF;

rDraught_mm := rStripEntryThickness_mm - rExitThicknessMeasured_mm;
IF rDraught_mm < 0.001 THEN
    rDraught_mm := 0.001; (* Prevent singular division in bite equations *)
END_IF;

IF rExitThicknessMeasured_mm > 0.010 THEN
    rTrueStrain := LN(rStripEntryThickness_mm / rExitThicknessMeasured_mm);
ELSE
    rTrueStrain := 0.30;
END_IF;

(* Dynamic Ludwik-Hollomon flow stress with hardening *)
rFlowStress_MPa := rStripBaseYieldStress_MPa * (1.0 + (rStripHardeningCoeff_B * EXPT(rTrueStrain, rStripHardeningExponent_n)));
IF rFlowStress_MPa < 200.0 THEN
    rFlowStress_MPa := 200.0;
ELSIF rFlowStress_MPa > 1200.0 THEN
    rFlowStress_MPa := 1200.0;
END_IF;

(* Dynamic lubricated friction coefficient as function of strip linear speed *)
IF rVotedRollSpeed_mpm > 10.0 THEN
    rFrictionCoeff_mu := 0.048 - (0.012 * (rVotedRollSpeed_mpm / 1800.0));
    IF rFrictionCoeff_mu < 0.022 THEN
        rFrictionCoeff_mu := 0.022;
    END_IF;
ELSE
    rFrictionCoeff_mu := 0.052;
END_IF;

(* Hitchcock flattened roll radius calculation: R' = R * [1 + (16*(1-nu^2) / (pi*E_r)) * (F / (W * dh))] *)
(* With steel work roll E_r = 210,000 MPa, nu = 0.30 -> Factor = 16*(1-0.09)/(pi*210000) = 2.2069e-5 mm2/N = 0.022069 mm2/kN *)
IF (rStripWidth_mm * rDraught_mm) > 0.1 THEN
    rHitchcockRadius_mm := rWorkRollRadius_mm * (1.0 + (0.022069 * (rVotedRollForce_kN / (rStripWidth_mm * rDraught_mm))));
    IF rHitchcockRadius_mm > (rWorkRollRadius_mm * 3.5) THEN
        rHitchcockRadius_mm := rWorkRollRadius_mm * 3.5;
    END_IF;
ELSE
    rHitchcockRadius_mm := rWorkRollRadius_mm;
END_IF;
rFlattenedRollRadius_mm := rHitchcockRadius_mm;

(* Contact arc length in deformation zone *)
rRollBiteLength_mm := SQRT(rHitchcockRadius_mm * rDraught_mm);

(* Bland-Ford-Ellis neutral angle alpha_n calculation *)
IF (rHitchcockRadius_mm * rExitThicknessMeasured_mm) > 0.001 THEN
    rTempSqrtVal := SQRT(rDraught_mm / rExitThicknessMeasured_mm);
    rNeutralAngleVal := SQRT(rExitThicknessMeasured_mm / rHitchcockRadius_mm) * 
                        TAN(0.5 * ATAN(rTempSqrtVal) - (0.25 / rFrictionCoeff_mu) * SQRT(rExitThicknessMeasured_mm / rHitchcockRadius_mm) * 
                        LN((rStripEntryThickness_mm / rExitThicknessMeasured_mm) * ((1.0 - (rActualSpecificTension_MPa / rFlowStress_MPa)) / (1.0 - (0.35 * rActualSpecificTension_MPa / rFlowStress_MPa)))));
    IF rNeutralAngleVal < 0.0001 THEN
        rNeutralAngleVal := 0.0001;
    END_IF;
ELSE
    rNeutralAngleVal := 0.012;
END_IF;
rNeutralAngle_rad := rNeutralAngleVal;

(* Forward slip coefficient f_s = (R' / h_out) * alpha_n^2 *)
IF rExitThicknessMeasured_mm > 0.010 THEN
    rForwardSlipVal := (rHitchcockRadius_mm / rExitThicknessMeasured_mm) * (rNeutralAngleVal * rNeutralAngleVal);
    IF rForwardSlipVal > 0.12 THEN
        rForwardSlipVal := 0.12;
    ELSIF rForwardSlipVal < 0.002 THEN
        rForwardSlipVal := 0.002;
    END_IF;
ELSE
    rForwardSlipVal := 0.035;
END_IF;
rForwardSlipRatio := rForwardSlipVal;

(* Backward slip coefficient b_s = 1 - (1 + f_s) * (h_out / h_in) *)
IF rStripEntryThickness_mm > 0.010 THEN
    rBackwardSlipVal := 1.0 - ((1.0 + rForwardSlipVal) * (rExitThicknessMeasured_mm / rStripEntryThickness_mm));
ELSE
    rBackwardSlipVal := 0.05;
END_IF;

(* Theoretical Bland-Ford Roll Force [kN] *)
rCalculatedRollForce_kN := (rStripWidth_mm * rRollBiteLength_mm * (rFlowStress_MPa - rActualSpecificTension_MPa) * 
                           (1.08 + (1.79 * rFrictionCoeff_mu * rRollBiteLength_mm / (rStripEntryThickness_mm + rExitThicknessMeasured_mm)) - 
                            (1.02 * rDraught_mm / rStripEntryThickness_mm))) / 1000.0;

(* BISRA Mill Spring Elastic Stretch: S_spring = F_roll / M_housing [mm] *)
IF rMillHousingModulus_kN_mm > 500.0 THEN
    rMillSpringStretch_mm := rVotedRollForce_kN / rMillHousingModulus_kN_mm;
ELSE
    rMillSpringStretch_mm := rVotedRollForce_kN / c_rMillStandModulusNominal;
END_IF;
rMillSpringCompensation_mm := rMillSpringStretch_mm;

(* Morgoil hydrodynamic sleeve bearing oil film thickness wedge model *)
IF (rVotedRollForce_kN > 100.0) AND (rVotedRollSpeed_mpm > 5.0) THEN
    rOilFilmThickness_mm := (0.058 * SQRT((0.048 * rVotedRollSpeed_mpm) / (rVotedRollForce_kN / 1000.0 + 3.0))) + 0.012;
    IF rOilFilmThickness_mm > 0.150 THEN
        rOilFilmThickness_mm := 0.150;
    END_IF;
ELSE
    rOilFilmThickness_mm := 0.015;
END_IF;
rHydrodynamicBearingWedge_mm := rOilFilmThickness_mm;

(* Dynamic Work Roll Thermal Crown Expansion differential equation filter *)
(* tau_th * d(C_th)/dt + C_th = K_th * F_roll * v_roll *)
IF rVotedRollSpeed_mpm > 10.0 THEN
    rRollThermalCrown_mm := rRollThermalCrown_mm + (c_rTs / 45.0) * ((0.00000000085 * rVotedRollForce_kN * rVotedRollSpeed_mpm) - rRollThermalCrown_mm);
    IF rRollThermalCrown_mm > 0.080 THEN
        rRollThermalCrown_mm := 0.080;
    ELSIF rRollThermalCrown_mm < 0.002 THEN
        rRollThermalCrown_mm := 0.002;
    END_IF;
END_IF;
rRollThermalExpansion_mm := rRollThermalCrown_mm;
"""

print("Phase 2 defined.")


def get_phase3_kalman():
    return """
(* ========================================================================================= *)
(* === PHASE 3: DYNAMIC ROLL ECCENTRICITY FILTERING (KALMAN FILTER)                     === *)
(* ========================================================================================= *)
(*
   Real-time recursive 6-state Kalman filter tracking the 1st, 2nd, and 3rd harmonic Fourier
   coefficients of backup roll runout / eccentricity:
   - Synchronized to backup roll rotation resolver angle theta_BUR.
   - Extracts roll gap periodic runout without phase lag (pure predictive harmonic feedforward).
   - Inverts eccentricity into hydraulic push-up cylinder feedforward command to cancel out
     cyclic thickness oscillations on the exit steel strip.
*)

(* Backup roll angular velocity and angle integration *)
IF rVotedRollSpeed_mpm > 1.0 THEN
    (* Backup roll linear speed = work roll linear speed / (1 + forward_slip) *)
    (* Angular velocity omega = v / R_BUR [rad/s] *)
    rRollAngleRad := rRollAngleRad + (((rVotedRollSpeed_mpm * 1000.0 / 60.0) / rBackupRollRadius_mm) * c_rTs);
    WHILE rRollAngleRad >= (2.0 * c_rPi) DO
        rRollAngleRad := rRollAngleRad - (2.0 * c_rPi);
    END_WHILE;
END_IF;

(* Evaluate time-varying trigonometric harmonic basis vectors *)
H_vec[1] := COS(rRollAngleRad);
H_vec[2] := SIN(rRollAngleRad);
H_vec[3] := COS(2.0 * rRollAngleRad);
H_vec[4] := SIN(2.0 * rRollAngleRad);
H_vec[5] := COS(3.0 * rRollAngleRad);
H_vec[6] := SIN(3.0 * rRollAngleRad);

(* Process noise diagonal configuration *)
Q_proc[1] := 0.00000008;
Q_proc[2] := 0.00000008;
Q_proc[3] := 0.00000004;
Q_proc[4] := 0.00000004;
Q_proc[5] := 0.00000002;
Q_proc[6] := 0.00000002;

(* Prior error covariance time propagation: P_prior = P + Q *)
FOR iHarmonicIdx := 1 TO 6 DO
    P_cov[iHarmonicIdx, iHarmonicIdx] := P_cov[iHarmonicIdx, iHarmonicIdx] + Q_proc[iHarmonicIdx];
END_FOR;

(* Innovation measurement: force-based gap variation minus known gauge error [mm] *)
rTempSqrtVal := ((rVotedRollForce_kN - rCalculatedRollForce_kN) / c_rMillStandModulusNominal) - (rExitThicknessMeasured_mm - rTargetExitThickness_mm);

(* Innovation scalar covariance: S = H * P * H^T + R *)
rMatAccum := R_meas;
FOR iHarmonicIdx := 1 TO 6 DO
    FOR jStateIdx := 1 TO 6 DO
        rMatAccum := rMatAccum + (H_vec[iHarmonicIdx] * P_cov[iHarmonicIdx, jStateIdx] * H_vec[jStateIdx]);
    END_FOR;
END_FOR;

IF rMatAccum < 0.00001 THEN
    rMatAccum := 0.00001;
END_IF;

(* Optimal Kalman gain vector: K = P * H^T / S *)
FOR iHarmonicIdx := 1 TO 6 DO
    K_gain[iHarmonicIdx] := 0.0;
    FOR jStateIdx := 1 TO 6 DO
        K_gain[iHarmonicIdx] := K_gain[iHarmonicIdx] + (P_cov[iHarmonicIdx, jStateIdx] * H_vec[jStateIdx]);
    END_FOR;
    K_gain[iHarmonicIdx] := K_gain[iHarmonicIdx] / rMatAccum;
END_FOR;

(* Measurement estimate and residual *)
rGradStepOS := 0.0;
FOR iHarmonicIdx := 1 TO 6 DO
    rGradStepOS := rGradStepOS + (H_vec[iHarmonicIdx] * x_ecc[iHarmonicIdx]);
END_FOR;
rGradStepDS := rTempSqrtVal - rGradStepOS; (* y_innov residual *)

(* State update: x_hat = x_hat + K * y_innov *)
FOR iHarmonicIdx := 1 TO 6 DO
    x_ecc[iHarmonicIdx] := x_ecc[iHarmonicIdx] + (K_gain[iHarmonicIdx] * rGradStepDS);
    (* Clamp state coefficients to realistic roll runout boundaries (+/- 0.035 mm) *)
    IF x_ecc[iHarmonicIdx] > 0.035 THEN
        x_ecc[iHarmonicIdx] := 0.035;
    ELSIF x_ecc[iHarmonicIdx] < -0.035 THEN
        x_ecc[iHarmonicIdx] := -0.035;
    END_IF;
END_FOR;

(* Posterior error covariance measurement update: P = (I - K * H) * P *)
FOR iHarmonicIdx := 1 TO 6 DO
    FOR jStateIdx := 1 TO 6 DO
        rMatAccum := 0.0;
        FOR kStepIdx := 1 TO 6 DO
            rMatAccum := rMatAccum + (K_gain[iHarmonicIdx] * H_vec[kStepIdx] * P_cov[kStepIdx, jStateIdx]);
        END_FOR;
        P_cov[iHarmonicIdx, jStateIdx] := P_cov[iHarmonicIdx, jStateIdx] - rMatAccum;
    END_FOR;
END_FOR;

(* Synthesize roll eccentricity feedforward compensation signal *)
IF bEccentricityCompEnable AND (rVotedRollSpeed_mpm > 60.0) THEN
    rRollEccentricityFeedforward := -( (H_vec[1] * x_ecc[1]) + (H_vec[2] * x_ecc[2]) + 
                                       (H_vec[3] * x_ecc[3]) + (H_vec[4] * x_ecc[4]) + 
                                       (H_vec[5] * x_ecc[5]) + (H_vec[6] * x_ecc[6]) );
    IF rRollEccentricityFeedforward > 0.025 THEN
        rRollEccentricityFeedforward := 0.025;
    ELSIF rRollEccentricityFeedforward < -0.025 THEN
        rRollEccentricityFeedforward := -0.025;
    END_IF;
ELSE
    rRollEccentricityFeedforward := 0.0;
END_IF;
rRollEccentricityCorrection_mm := rRollEccentricityFeedforward;
"""

print("Phase 3 defined.")


def get_phase4_statespace():
    return """
(* ========================================================================================= *)
(* === PHASE 4: 8x8 DISCRETE STATE-SPACE PREDICTION (x[k+1] = A*x[k] + B*u[k])           === *)
(* ========================================================================================= *)
(*
   Rigorous 8th-order coupled cyber-physical discrete state-space formulation at Ts = 0.001 s:
   State vector x = [dh, dsigma, dy_os, dy_ds, dv_os, dv_ds, dfs, dF]^T
   Input vector u = [spool_os, spool_ds, speed_trim]^T
   Output vector y = [dh_meas, dsigma_meas, dy_avg_meas, dF_meas]^T
   Observer updates states via Luenberger innovation matrix L_obs.
*)

(* Static Matrix Initialization on First PLC Execution Scan *)
IF NOT bInitialized THEN
    (* Row 1: dh exit thickness dynamics *)
    A_ss[1,1] := 0.94250;  A_ss[1,2] := -0.00012; A_ss[1,3] := 0.48500;  A_ss[1,4] := 0.48500;
    A_ss[1,5] := 0.00045;  A_ss[1,6] := 0.00045;  A_ss[1,7] := -0.08200; A_ss[1,8] := 0.00021;

    (* Row 2: dsigma interstand tension dynamics *)
    A_ss[2,1] := 18.4200;  A_ss[2,2] := 0.98250;  A_ss[2,3] := -6.25000; A_ss[2,4] := -6.25000;
    A_ss[2,5] := -0.01250; A_ss[2,6] := -0.01250; A_ss[2,7] := 142.5000; A_ss[2,8] := -0.00480;

    (* Row 3: dy_os cylinder OS position integration *)
    A_ss[3,1] := 0.00000;  A_ss[3,2] := 0.00000;  A_ss[3,3] := 1.00000;  A_ss[3,4] := 0.00000;
    A_ss[3,5] := 0.00100;  A_ss[3,6] := 0.00000;  A_ss[3,7] := 0.00000;  A_ss[3,8] := 0.00000;

    (* Row 4: dy_ds cylinder DS position integration *)
    A_ss[4,1] := 0.00000;  A_ss[4,2] := 0.00000;  A_ss[4,3] := 0.00000;  A_ss[4,4] := 1.00000;
    A_ss[4,5] := 0.00000;  A_ss[4,6] := 0.00100;  A_ss[4,7] := 0.00000;  A_ss[4,8] := 0.00000;

    (* Row 5: dv_os cylinder OS hydraulic velocity *)
    A_ss[5,1] := 0.00000;  A_ss[5,2] := 0.00000;  A_ss[5,3] := -85.4000; A_ss[5,4] := 12.50000;
    A_ss[5,5] := 0.86500;  A_ss[5,6] := -0.04500; A_ss[5,7] := 0.00000;  A_ss[5,8] := -0.01850;

    (* Row 6: dv_ds cylinder DS hydraulic velocity *)
    A_ss[6,1] := 0.00000;  A_ss[6,2] := 0.00000;  A_ss[6,3] := 12.50000; A_ss[6,4] := -85.4000;
    A_ss[6,5] := -0.04500; A_ss[6,6] := 0.86500;  A_ss[6,7] := 0.00000;  A_ss[6,8] := -0.01850;

    (* Row 7: dfs forward slip dynamics *)
    A_ss[7,1] := -0.14500; A_ss[7,2] := 0.00035;  A_ss[7,3] := 0.08500;  A_ss[7,4] := 0.08500;
    A_ss[7,5] := 0.00012;  A_ss[7,6] := 0.00012;  A_ss[7,7] := 0.89500;  A_ss[7,8] := 0.00008;

    (* Row 8: dF dynamic roll separating force *)
    A_ss[8,1] := -12450.0; A_ss[8,2] := -15.8000; A_ss[8,3] := 2420.000; A_ss[8,4] := 2420.000;
    A_ss[8,5] := 1.85000;  A_ss[8,6] := 1.85000;  A_ss[8,7] := -850.000; A_ss[8,8] := 0.92500;

    (* Actuator Input Gain Matrix B_ss [8x3] *)
    B_ss[1,1] := 0.00015;  B_ss[1,2] := 0.00015;  B_ss[1,3] := -0.00008;
    B_ss[2,1] := -0.08500; B_ss[2,2] := -0.08500; B_ss[2,3] := 0.42500;
    B_ss[3,1] := 0.00000;  B_ss[3,2] := 0.00000;  B_ss[3,3] := 0.00000;
    B_ss[4,1] := 0.00000;  B_ss[4,2] := 0.00000;  B_ss[4,3] := 0.00000;
    B_ss[5,1] := 3.45000;  B_ss[5,2] := -0.15000; B_ss[5,3] := 0.00000;
    B_ss[6,1] := -0.15000; B_ss[6,2] := 3.45000;  B_ss[6,3] := 0.00000;
    B_ss[7,1] := 0.00025;  B_ss[7,2] := 0.00025;  B_ss[7,3] := 0.00185;
    B_ss[8,1] := 45.2000;  B_ss[8,2] := 45.2000;  B_ss[8,3] := -8.45000;

    (* Measurement Matrix C_ss [4x8] *)
    C_ss[1,1] := 1.0; C_ss[1,2] := 0.0; C_ss[1,3] := 0.0; C_ss[1,4] := 0.0; C_ss[1,5] := 0.0; C_ss[1,6] := 0.0; C_ss[1,7] := 0.0; C_ss[1,8] := 0.0;
    C_ss[2,1] := 0.0; C_ss[2,2] := 1.0; C_ss[2,3] := 0.0; C_ss[2,4] := 0.0; C_ss[2,5] := 0.0; C_ss[2,6] := 0.0; C_ss[2,7] := 0.0; C_ss[2,8] := 0.0;
    C_ss[3,1] := 0.0; C_ss[3,2] := 0.0; C_ss[3,3] := 0.5; C_ss[3,4] := 0.5; C_ss[3,5] := 0.0; C_ss[3,6] := 0.0; C_ss[3,7] := 0.0; C_ss[3,8] := 0.0;
    C_ss[4,1] := 0.0; C_ss[4,2] := 0.0; C_ss[4,3] := 0.0; C_ss[4,4] := 0.0; C_ss[4,5] := 0.0; C_ss[4,6] := 0.0; C_ss[4,7] := 0.0; C_ss[4,8] := 1.0;

    (* Direct Transmission Matrix D_ss [4x3] *)
    D_ss[1,1] := 0.0; D_ss[1,2] := 0.0; D_ss[1,3] := 0.0;
    D_ss[2,1] := 0.0; D_ss[2,2] := 0.0; D_ss[2,3] := 0.0;
    D_ss[3,1] := 0.0; D_ss[3,2] := 0.0; D_ss[3,3] := 0.0;
    D_ss[4,1] := 0.0; D_ss[4,2] := 0.0; D_ss[4,3] := 0.0;

    (* Luenberger Observer Gain Matrix L_obs [8x4] *)
    L_obs[1,1] := 0.2850; L_obs[1,2] := 0.0001; L_obs[1,3] := 0.1250; L_obs[1,4] := 0.00005;
    L_obs[2,1] := 2.4500; L_obs[2,2] := 0.3200; L_obs[2,3] := -0.850; L_obs[2,4] := -0.0012;
    L_obs[3,1] := 0.0150; L_obs[3,2] := -0.001; L_obs[3,3] := 0.4500; L_obs[3,4] := 0.00002;
    L_obs[4,1] := 0.0150; L_obs[4,2] := -0.001; L_obs[4,3] := 0.4500; L_obs[4,4] := 0.00002;
    L_obs[5,1] := 0.8500; L_obs[5,2] := -0.050; L_obs[5,3] := 12.500; L_obs[5,4] := -0.0045;
    L_obs[6,1] := 0.8500; L_obs[6,2] := -0.050; L_obs[6,3] := 12.500; L_obs[6,4] := -0.0045;
    L_obs[7,1] := -0.045; L_obs[7,2] := 0.0025; L_obs[7,3] := 0.0150; L_obs[7,4] := 0.00001;
    L_obs[8,1] := -850.0; L_obs[8,2] := -4.500; L_obs[8,3] := 520.00; L_obs[8,4] := 0.24500;

    (* MPC Weight Matrices *)
    Q_mpc[1] := 185000.0; (* Massive penalty on strip exit thickness error *)
    Q_mpc[2] := 12.5;     (* Interstand tension penalty *)
    Q_mpc[3] := 45.0;     (* OS cylinder position deviation *)
    Q_mpc[4] := 45.0;     (* DS cylinder position deviation *)
    Q_mpc[5] := 0.85;     (* OS velocity *)
    Q_mpc[6] := 0.85;     (* DS velocity *)
    Q_mpc[7] := 1250.0;   (* Forward slip stability *)
    Q_mpc[8] := 0.0025;   (* Roll force variation *)

    R_mpc[1] := 0.15;     (* OS servo valve current penalty *)
    R_mpc[2] := 0.15;     (* DS servo valve current penalty *)
    R_mpc[3] := 0.045;    (* Main drive speed trim penalty *)

    S_mpc[1] := 2.50;     (* OS servo valve slew rate penalty *)
    S_mpc[2] := 2.50;     (* DS servo valve slew rate penalty *)
    S_mpc[3] := 1.20;     (* Speed trim acceleration penalty *)

    P_mpc[1] := 350000.0; (* Terminal thickness penalty *)
    P_mpc[2] := 25.0;
    P_mpc[3] := 80.0;
    P_mpc[4] := 80.0;
    P_mpc[5] := 1.5;
    P_mpc[6] := 1.5;
    P_mpc[7] := 2500.0;
    P_mpc[8] := 0.005;

    (* Initialize Kalman Error Covariance Matrix P_cov [6x6] *)
    FOR iHarmonicIdx := 1 TO 6 DO
        FOR jStateIdx := 1 TO 6 DO
            IF iHarmonicIdx = jStateIdx THEN
                P_cov[iHarmonicIdx, jStateIdx] := 0.0025;
            ELSE
                P_cov[iHarmonicIdx, jStateIdx] := 0.0;
            END_IF;
        END_FOR;
    END_FOR;

    bInitialized := TRUE;
END_IF;

(* Formulate Output Vector y_meas [4] *)
y_meas[1] := rExitThicknessMeasured_mm - rTargetExitThickness_mm;
y_meas[2] := rActualSpecificTension_MPa - rTargetInterstandTension_MPa;
y_meas[3] := (0.5 * (rVotedPosOS + rVotedPosDS)) - rZeroGapOffset_mm;
y_meas[4] := rVotedRollForce_kN - rCalculatedRollForce_kN;

(* Predicted Output: y_pred = C_ss * x_state *)
FOR iStateIdx := 1 TO 4 DO
    y_pred[iStateIdx] := 0.0;
    FOR jStateIdx := 1 TO 8 DO
        y_pred[iStateIdx] := y_pred[iStateIdx] + (C_ss[iStateIdx, jStateIdx] * x_state[jStateIdx]);
    END_FOR;
END_FOR;

(* One-Step Ahead State Space Propagation: x_pred = A_ss * x_state + B_ss * u_ctrl *)
FOR iStateIdx := 1 TO 8 DO
    x_pred[iStateIdx] := 0.0;
    FOR jStateIdx := 1 TO 8 DO
        x_pred[iStateIdx] := x_pred[iStateIdx] + (A_ss[iStateIdx, jStateIdx] * x_state[jStateIdx]);
    END_FOR;
    FOR jStateIdx := 1 TO 3 DO
        x_pred[iStateIdx] := x_pred[iStateIdx] + (B_ss[iStateIdx, jStateIdx] * u_ctrl[jStateIdx]);
    END_FOR;
END_FOR;

(* Luenberger Observer State Correction: x_state = x_pred + L_obs * (y_meas - y_pred) *)
FOR iStateIdx := 1 TO 8 DO
    rMatAccum := 0.0;
    FOR jStateIdx := 1 TO 4 DO
        rMatAccum := rMatAccum + (L_obs[iStateIdx, jStateIdx] * (y_meas[jStateIdx] - y_pred[jStateIdx]));
    END_FOR;
    x_state[iStateIdx] := x_pred[iStateIdx] + rMatAccum;
END_FOR;
"""

print("Phase 4 defined.")


def get_phase5_mpc():
    return """
(* ========================================================================================= *)
(* === PHASE 5: RECEDING-HORIZON MPC OPTIMIZATION & DECOUPLED GAP-SPEED-BEND CONTROL    === *)
(* ========================================================================================= *)
(*
   Real-time Model Predictive Control (MPC) quadratic cost optimization:
   - Receding horizon N_p = 8 steps unrolled trajectory.
   - Solves for optimal hydraulic servo spool commands (OS and DS) and main drive speed trim.
   - Simultaneously stabilizes strip exit thickness (+/- 0.0015 mm) and inter-stand strip tension.
   - Projected Gradient Descent (PGD) with physical actuator hard box constraints & slew rate limits.
   - Dynamic roll bending cylinder hydraulic pressure calculation for roll crown compensation.
*)

(* Reference Setpoint Initialization *)
FOR iStateIdx := 1 TO 8 DO
    r_ref[iStateIdx] := 0.0;
END_FOR;

(* Candidate control initialized to previous control action *)
u_cand[1] := u_prev[1];
u_cand[2] := u_prev[2];
u_cand[3] := u_prev[3];

(* Iterative Projected Gradient Descent Solver (6 iterations per 1.0 ms PLC scan) *)
FOR iIterMpc := 1 TO 6 DO
    (* 5.1 Multi-step state trajectory prediction across N_p = 8 horizon *)
    FOR iStateIdx := 1 TO 8 DO
        rMatAccum := 0.0;
        FOR jStateIdx := 1 TO 8 DO
            rMatAccum := rMatAccum + (A_ss[iStateIdx, jStateIdx] * x_state[jStateIdx]);
        END_FOR;
        FOR jStateIdx := 1 TO 3 DO
            rMatAccum := rMatAccum + (B_ss[iStateIdx, jStateIdx] * u_cand[jStateIdx]);
        END_FOR;
        x_horiz[iStateIdx, 1] := rMatAccum;
    END_FOR;

    FOR kStepIdx := 2 TO 8 DO
        FOR iStateIdx := 1 TO 8 DO
            rMatAccum := 0.0;
            FOR jStateIdx := 1 TO 8 DO
                rMatAccum := rMatAccum + (A_ss[iStateIdx, jStateIdx] * x_horiz[jStateIdx, kStepIdx - 1]);
            END_FOR;
            FOR jStateIdx := 1 TO 3 DO
                rMatAccum := rMatAccum + (B_ss[iStateIdx, jStateIdx] * u_cand[jStateIdx]);
            END_FOR;
            x_horiz[iStateIdx, kStepIdx] := rMatAccum;
        END_FOR;
    END_FOR;

    (* 5.2 Accumulated Quadratic Cost Functional Evaluation *)
    rCostFunctional := 0.0;
    (* State tracking penalty *)
    FOR kStepIdx := 1 TO 7 DO
        FOR iStateIdx := 1 TO 8 DO
            rCostFunctional := rCostFunctional + (Q_mpc[iStateIdx] * (x_horiz[iStateIdx, kStepIdx] - r_ref[iStateIdx]) * (x_horiz[iStateIdx, kStepIdx] - r_ref[iStateIdx]));
        END_FOR;
    END_FOR;
    (* Terminal state penalty *)
    FOR iStateIdx := 1 TO 8 DO
        rCostFunctional := rCostFunctional + (P_mpc[iStateIdx] * (x_horiz[iStateIdx, 8] - r_ref[iStateIdx]) * (x_horiz[iStateIdx, 8] - r_ref[iStateIdx]));
    END_FOR;
    (* Actuator energy and slew penalties *)
    FOR jStateIdx := 1 TO 3 DO
        rCostFunctional := rCostFunctional + (R_mpc[jStateIdx] * u_cand[jStateIdx] * u_cand[jStateIdx]);
        rCostFunctional := rCostFunctional + (S_mpc[jStateIdx] * (u_cand[jStateIdx] - u_prev[jStateIdx]) * (u_cand[jStateIdx] - u_prev[jStateIdx]));
    END_FOR;

    (* 5.3 Analytical Gradient Calculation dJ / du *)
    (* Gradient for u_cand[1]: OS Push-up servo spool *)
    grad_J[1] := (2.0 * R_mpc[1] * u_cand[1]) + (2.0 * S_mpc[1] * (u_cand[1] - u_prev[1]));
    FOR kStepIdx := 1 TO 7 DO
        grad_J[1] := grad_J[1] + (2.0 * Q_mpc[1] * (x_horiz[1, kStepIdx] - r_ref[1]) * B_ss[1,1] * INT_TO_REAL(kStepIdx));
        grad_J[1] := grad_J[1] + (2.0 * Q_mpc[2] * (x_horiz[2, kStepIdx] - r_ref[2]) * B_ss[2,1] * INT_TO_REAL(kStepIdx));
        grad_J[1] := grad_J[1] + (2.0 * Q_mpc[5] * (x_horiz[5, kStepIdx] - r_ref[5]) * B_ss[5,1]);
        grad_J[1] := grad_J[1] + (2.0 * Q_mpc[8] * (x_horiz[8, kStepIdx] - r_ref[8]) * B_ss[8,1]);
    END_FOR;
    grad_J[1] := grad_J[1] + (2.0 * P_mpc[1] * (x_horiz[1, 8] - r_ref[1]) * B_ss[1,1] * 8.0);

    (* Gradient for u_cand[2]: DS Push-up servo spool *)
    grad_J[2] := (2.0 * R_mpc[2] * u_cand[2]) + (2.0 * S_mpc[2] * (u_cand[2] - u_prev[2]));
    FOR kStepIdx := 1 TO 7 DO
        grad_J[2] := grad_J[2] + (2.0 * Q_mpc[1] * (x_horiz[1, kStepIdx] - r_ref[1]) * B_ss[1,2] * INT_TO_REAL(kStepIdx));
        grad_J[2] := grad_J[2] + (2.0 * Q_mpc[2] * (x_horiz[2, kStepIdx] - r_ref[2]) * B_ss[2,2] * INT_TO_REAL(kStepIdx));
        grad_J[2] := grad_J[2] + (2.0 * Q_mpc[6] * (x_horiz[6, kStepIdx] - r_ref[6]) * B_ss[6,2]);
        grad_J[2] := grad_J[2] + (2.0 * Q_mpc[8] * (x_horiz[8, kStepIdx] - r_ref[8]) * B_ss[8,2]);
    END_FOR;
    grad_J[2] := grad_J[2] + (2.0 * P_mpc[1] * (x_horiz[1, 8] - r_ref[1]) * B_ss[1,2] * 8.0);

    (* Gradient for u_cand[3]: Main drive motor speed trim *)
    grad_J[3] := (2.0 * R_mpc[3] * u_cand[3]) + (2.0 * S_mpc[3] * (u_cand[3] - u_prev[3]));
    FOR kStepIdx := 1 TO 7 DO
        grad_J[3] := grad_J[3] + (2.0 * Q_mpc[1] * (x_horiz[1, kStepIdx] - r_ref[1]) * B_ss[1,3]);
        grad_J[3] := grad_J[3] + (2.0 * Q_mpc[2] * (x_horiz[2, kStepIdx] - r_ref[2]) * B_ss[2,3] * INT_TO_REAL(kStepIdx));
        grad_J[3] := grad_J[3] + (2.0 * Q_mpc[7] * (x_horiz[7, kStepIdx] - r_ref[7]) * B_ss[7,3]);
    END_FOR;
    grad_J[3] := grad_J[3] + (2.0 * P_mpc[2] * (x_horiz[2, 8] - r_ref[2]) * B_ss[2,3] * 8.0);

    (* 5.4 Gradient Descent Update Step *)
    u_cand[1] := u_cand[1] - (rMpcStepSize * grad_J[1]);
    u_cand[2] := u_cand[2] - (rMpcStepSize * grad_J[2]);
    u_cand[3] := u_cand[3] - (rMpcStepSize * grad_J[3]);

    (* 5.5 Actuator Hard Box Constraints Projection *)
    (* Moog D661 Servo spool command limits: [-40.0 mA, +40.0 mA] *)
    IF u_cand[1] > 40.0 THEN u_cand[1] := 40.0; ELSIF u_cand[1] < -40.0 THEN u_cand[1] := -40.0; END_IF;
    IF u_cand[2] > 40.0 THEN u_cand[2] := 40.0; ELSIF u_cand[2] < -40.0 THEN u_cand[2] := -40.0; END_IF;
    (* Speed trim limits: [-60.0 m/min, +60.0 m/min] *)
    IF u_cand[3] > 60.0 THEN u_cand[3] := 60.0; ELSIF u_cand[3] < -60.0 THEN u_cand[3] := -60.0; END_IF;

    (* Actuator Slew Rate Limiting *)
    IF (u_cand[1] - u_prev[1]) > 4.5 THEN u_cand[1] := u_prev[1] + 4.5;
    ELSIF (u_cand[1] - u_prev[1]) < -4.5 THEN u_cand[1] := u_prev[1] - 4.5; END_IF;

    IF (u_cand[2] - u_prev[2]) > 4.5 THEN u_cand[2] := u_prev[2] + 4.5;
    ELSIF (u_cand[2] - u_prev[2]) < -4.5 THEN u_cand[2] := u_prev[2] - 4.5; END_IF;

    IF (u_cand[3] - u_prev[3]) > 2.5 THEN u_cand[3] := u_prev[3] + 2.5;
    ELSIF (u_cand[3] - u_prev[3]) < -2.5 THEN u_cand[3] := u_prev[3] - 2.5; END_IF;
END_FOR;

(* Assign Optimal Controls *)
u_ctrl[1] := u_cand[1];
u_ctrl[2] := u_cand[2];
u_ctrl[3] := u_cand[3];

delta_u[1] := u_ctrl[1] - u_prev[1];
delta_u[2] := u_ctrl[2] - u_prev[2];
delta_u[3] := u_ctrl[3] - u_prev[3];

u_prev[1] := u_ctrl[1];
u_prev[2] := u_ctrl[2];
u_prev[3] := u_ctrl[3];

(* 5.6 Roll Crown Bending Cylinder Closed-Loop Compensation *)
(* Positive bending increases roll gap at strip center, negative bending relieves edge wave *)
IF bRollBendingAutoEnable THEN
    rRollBendingCmd_bar := 120.0 + (0.0035 * (rVotedRollForce_kN - rZeroKissForce_kN)) + 
                           (2.85 * (rExitThicknessMeasured_mm - rTargetExitThickness_mm) * 1000.0) - 
                           (850.0 * rRollThermalCrown_mm);
    IF rRollBendingCmd_bar > 240.0 THEN
        rRollBendingCmd_bar := 240.0;
    ELSIF rRollBendingCmd_bar < 40.0 THEN
        rRollBendingCmd_bar := 40.0;
    END_IF;
ELSE
    rRollBendingCmd_bar := 120.0;
END_IF;
rRollBendingPressureCmd_bar := rRollBendingCmd_bar;

(* 5.7 Decoupled Speed Trim Distribution Between Stand 5 and Stand 6 *)
(* Differential speed trimming directly manipulates interstand tension without changing total mass flow *)
rMainDriveSpeedTrim_mpm := u_ctrl[3] + (0.085 * (rActualSpecificTension_MPa - rTargetInterstandTension_MPa));
rStand5SpeedTrim_mpm := (-0.5 * u_ctrl[3]) - (0.085 * (rActualSpecificTension_MPa - rTargetInterstandTension_MPa));
"""

print("Phase 5 defined.")


def get_phase6_servo():
    return """
(* ========================================================================================= *)
(* === PHASE 6: HYDRAULIC PUSH-UP CYLINDER HIGH-SPEED DECOUPLED SERVO CONTROL           === *)
(* ========================================================================================= *)
(*
   Sub-millisecond hydraulic push-up cylinder closed-loop position control:
   - High-speed decoupled servo loop combining BISRA gap target, tilt leveling & MPC trimming.
   - Non-linear square root valve pressure drop compensation: Q = Cd * A_v * sqrt(2*dP/rho).
   - Dynamic cross-coupling leveling regulator preventing strip wedge / camber walk.
   - 400 Hz continuous high-frequency anti-stiction dither current synthesis.
*)

(* 6.1 Total Cylinder Gap Setpoint Formulation *)
rCylPositionAvg_target := rTargetExitThickness_mm - rMillSpringCompensation_mm + 
                          rRollEccentricityFeedforward + rRollThermalExpansion_mm + 
                          rHydrodynamicBearingWedge_mm + rZeroGapOffset_mm;

(* Strip leveling tilt differential setpoint (Operator Side vs Drive Side) *)
rCylTiltDiff_target := 0.0; (* Level gap target across roll barrel *)

rCylPositionOS_target := rCylPositionAvg_target + (0.5 * rCylTiltDiff_target);
rCylPositionDS_target := rCylPositionAvg_target - (0.5 * rCylTiltDiff_target);

(* 6.2 Fast Position Error Calculation *)
rGradStepOS := rCylPositionOS_target - rVotedPosOS; (* OS position error [mm] *)
rGradStepDS := rCylPositionDS_target - rVotedPosDS; (* DS position error [mm] *)

(* Cross-coupling roll leveling / wedge error *)
rGradStepSpeed := (rVotedPosOS - rVotedPosDS) - rCylTiltDiff_target;

(* 6.3 Proportional + Velocity Feedforward + MPC Servo Law *)
(* Base servo gains: K_p = 120.0 mA/mm, K_d = 0.85 mA/(mm/s) *)
rSpoolPosOS_mA := (120.0 * rGradStepOS) - (0.85 * x_state[5]) - (35.0 * rGradStepSpeed) + u_ctrl[1];
rSpoolPosDS_mA := (120.0 * rGradStepDS) - (0.85 * x_state[6]) + (35.0 * rGradStepSpeed) + u_ctrl[2];

(* 6.4 Non-Linear Square Root Pressure Drop Orifice Compensation *)
(* Normalizes spool authority against hydraulic supply line pressure fluctuations *)
rTempSqrtVal := rHydraulicSupplyPressure_bar - rVotedHeadPres;
IF rTempSqrtVal < 15.0 THEN
    rTempSqrtVal := 15.0; (* Prevent square root singularity / reversal *)
END_IF;
rTempSqrtVal := SQRT(70.0 / rTempSqrtVal); (* 70 bar standard test delta-P *)
IF rTempSqrtVal > 2.2 THEN
    rTempSqrtVal := 2.2;
ELSIF rTempSqrtVal < 0.65 THEN
    rTempSqrtVal := 0.65;
END_IF;

rSpoolPosOS_mA := rSpoolPosOS_mA * rTempSqrtVal;
rSpoolPosDS_mA := rSpoolPosDS_mA * rTempSqrtVal;

(* 6.5 Anti-Stiction 400 Hz Dither Current Injection *)
rDitherPhase := rDitherPhase + (2.0 * c_rPi * 400.0 * c_rTs);
WHILE rDitherPhase >= (2.0 * c_rPi) DO
    rDitherPhase := rDitherPhase - (2.0 * c_rPi);
END_WHILE;
rDitherSignal_mA := 0.75 * SIN(rDitherPhase);

rSpoolPosOS_mA := rSpoolPosOS_mA + rDitherSignal_mA;
rSpoolPosDS_mA := rSpoolPosDS_mA + rDitherSignal_mA;

(* 6.6 Valve Spool Saturation Protection *)
IF rSpoolPosOS_mA > 40.0 THEN
    rSpoolPosOS_mA := 40.0;
ELSIF rSpoolPosOS_mA < -40.0 THEN
    rSpoolPosOS_mA := -40.0;
END_IF;

IF rSpoolPosDS_mA > 40.0 THEN
    rSpoolPosDS_mA := 40.0;
ELSIF rSpoolPosDS_mA < -40.0 THEN
    rSpoolPosDS_mA := -40.0;
END_IF;

rServoValveSpoolCmd_OS_mA := rSpoolPosOS_mA;
rServoValveSpoolCmd_DS_mA := rSpoolPosDS_mA;
"""

print("Phase 6 defined.")


def get_phase7_fsm():
    return """
(* ========================================================================================= *)
(* === PHASE 7: MULTI-STAGE 12-STATE INDUSTRIAL FINITE STATE MACHINE (FSM)              === *)
(* ========================================================================================= *)
(*
   12-Stage Deterministic Finite State Machine governing mill operational life-cycle:
   0: MILL_ZEROING_CALIBRATION    - Roll kissing & mill housing modulus calibration
   1: HYDRAULIC_WARMUP            - Pre-fill, valve dither & hydraulic oil circulation
   2: STRIP_THREADING_LOW_SPEED   - Low speed threading (60 m/min) & bite detection
   3: TENSION_ESTABLISHMENT       - Looperless tension pull-in & speed synchronization
   4: MILL_ACCELERATION_RAMP      - Acceleration to 1,800 m/min with dynamic friction comp
   5: FULL_PRODUCTION_STEADY_STATE- Continuous high-speed gauge regulation (1,800 m/min)
   6: FLYING_GAUGE_CHANGE         - In-line dynamic gauge transition on weld seam
   7: TAIL_OUT_DECELERATION       - Controlled deceleration & roll bite unloading
   8: COIL_STRIP_BREAK_TRIP       - Cobble / strip break emergency containment
   9: WORK_ROLL_QUICK_OPEN        - High-speed hydraulic dump (<40 ms retract)
  10: MAINTENANCE_ROLL_CHANGE     - Mechanical lock-out for automated roll car change
  11: EMERGENCY_ESTOP             - Catastrophic fail-safe E-stop clamp
*)

(* Global Safety Interlocks Override *)
IF bEmergencyStop THEN
    iFSM_State := 11; (* Direct forced transition to EMERGENCY_ESTOP *)
ELSIF bQuickOpenCmd THEN
    iFSM_State := 9;  (* Direct forced transition to WORK_ROLL_QUICK_OPEN *)
ELSIF bStripBreakSens OR (rActualSpecificTension_MPa < 5.0 AND iFSM_State >= 4 AND iFSM_State <= 6) THEN
    iFSM_State := 8;  (* Cobble / Strip Break Detected! *)
END_IF;

rFSM_StateTimer_ms := rFSM_StateTimer_ms + (c_rTs * 1000.0);

CASE iFSM_State OF
    0: (* MILL_ZEROING_CALIBRATION *)
        bQuickOpenActive := FALSE;
        bCoolantHeaderShutoffCmd := FALSE;
        bHAGC_InRegulation := FALSE;
        rRampCurrentSpeed_mpm := 0.0;

        (* Slowly close cylinders to kissing contact force 3,500 kN *)
        IF bRollKissingCalibReq THEN
            bKissCalibInProgress := TRUE;
            rKissCalibTimer_ms := rKissCalibTimer_ms + (c_rTs * 1000.0);
            (* Target kiss force ramp *)
            IF rVotedRollForce_kN < rZeroKissForce_kN THEN
                rCylPositionOS_target := rCylPositionOS_target - (0.001 * c_rTs * 1000.0);
                rCylPositionDS_target := rCylPositionDS_target - (0.001 * c_rTs * 1000.0);
            ELSE
                (* Kiss force reached: store mechanical zero datum & calibrate mill modulus *)
                rZeroGapOffset_mm := 0.5 * (rVotedPosOS + rVotedPosDS);
                rMillHousingModulus_kN_mm := rVotedRollForce_kN / ABS(rZeroGapOffset_mm + 0.0001);
                IF rMillHousingModulus_kN_mm < 3500.0 THEN
                    rMillHousingModulus_kN_mm := 3500.0;
                ELSIF rMillHousingModulus_kN_mm > 6000.0 THEN
                    rMillHousingModulus_kN_mm := 6000.0;
                END_IF;
                bKissCalibInProgress := FALSE;
                rKissCalibTimer_ms := 0.0;
                iFSM_State := 1; (* Transition to HYDRAULIC_WARMUP *)
                rFSM_StateTimer_ms := 0.0;
            END_IF;
        ELSE
            rKissCalibTimer_ms := 0.0;
        END_IF;

    1: (* HYDRAULIC_WARMUP *)
        bQuickOpenActive := FALSE;
        bCoolantHeaderShutoffCmd := FALSE;
        bHAGC_InRegulation := FALSE;
        rRampCurrentSpeed_mpm := 0.0;

        (* Park push-up cylinders at safe standby gap (10.0 mm) *)
        rCylPositionOS_target := 10.0;
        rCylPositionDS_target := 10.0;

        (* Check hydraulic supply pressure & sensor health *)
        IF (rHydraulicSupplyPressure_bar >= 240.0) AND (rFSM_StateTimer_ms > 3000.0) THEN
            IF bEnableHAGC THEN
                iFSM_State := 2; (* Transition to STRIP_THREADING_LOW_SPEED *)
                rFSM_StateTimer_ms := 0.0;
            END_IF;
        END_IF;

    2: (* STRIP_THREADING_LOW_SPEED *)
        bQuickOpenActive := FALSE;
        bCoolantHeaderShutoffCmd := FALSE;
        bHAGC_InRegulation := FALSE;
        rRampCurrentSpeed_mpm := 60.0; (* Threading velocity 60 m/min *)

        (* Preset roll gap to strip nominal entry thickness plus lead clearance (0.05 mm) *)
        rCylPositionAvg_target := rStripEntryThickness_mm + 0.050;
        rCylPositionOS_target := rCylPositionAvg_target;
        rCylPositionDS_target := rCylPositionAvg_target;

        (* Bite detection: roll separating force jump indicates strip head entered roll bite *)
        IF rVotedRollForce_kN > 500.0 THEN
            iFSM_State := 3; (* Transition to TENSION_ESTABLISHMENT *)
            rFSM_StateTimer_ms := 0.0;
        END_IF;

    3: (* TENSION_ESTABLISHMENT *)
        bQuickOpenActive := FALSE;
        bCoolantHeaderShutoffCmd := FALSE;
        bHAGC_InRegulation := FALSE;
        rRampCurrentSpeed_mpm := 60.0;

        (* Looperless inter-stand tension control active: Stand 5/6 differential speed pull *)
        IF rActualSpecificTension_MPa >= (0.75 * rTargetInterstandTension_MPa) THEN
            IF rFSM_StateTimer_ms > 800.0 THEN
                iFSM_State := 4; (* Transition to MILL_ACCELERATION_RAMP *)
                rFSM_StateTimer_ms := 0.0;
            END_IF;
        END_IF;

    4: (* MILL_ACCELERATION_RAMP *)
        bQuickOpenActive := FALSE;
        bCoolantHeaderShutoffCmd := FALSE;

        (* Ramp mill speed from 60 m/min up to 1,800 m/min at 1.2 m/s2 (72 m/min/s) *)
        IF rRampCurrentSpeed_mpm < rRampTargetSpeed_mpm THEN
            rRampCurrentSpeed_mpm := rRampCurrentSpeed_mpm + (rRampAcceleration_mpm_s * c_rTs);
        ELSE
            rRampCurrentSpeed_mpm := rRampTargetSpeed_mpm;
        END_IF;

        (* Dynamic thickness tolerance check *)
        IF ABS(rGaugeError_um) <= 1.5 THEN
            bHAGC_InRegulation := TRUE;
        ELSE
            bHAGC_InRegulation := FALSE;
        END_IF;

        IF rRampCurrentSpeed_mpm >= 1795.0 THEN
            iFSM_State := 5; (* Transition to FULL_PRODUCTION_STEADY_STATE *)
            rFSM_StateTimer_ms := 0.0;
        END_IF;

    5: (* FULL_PRODUCTION_STEADY_STATE *)
        bQuickOpenActive := FALSE;
        bCoolantHeaderShutoffCmd := FALSE;
        rRampCurrentSpeed_mpm := 1800.0;

        (* Steady-state high-precision gauge regulation *)
        IF ABS(rGaugeError_um) <= 1.5 THEN
            bHAGC_InRegulation := TRUE;
        ELSE
            bHAGC_InRegulation := FALSE;
        END_IF;

        (* Monitor triggers for flying gauge change or tail out *)
        IF bFlyingGaugeTrigger THEN
            rFlyingGaugeInitialGauge_mm := rTargetExitThickness_mm;
            rFlyingGaugeTargetGauge_mm := rFlyingGaugeNewTarget_mm;
            rFlyingGaugeTransitionTimer_ms := 0.0;
            bFlyingGaugeActive := TRUE;
            iFSM_State := 6; (* Transition to FLYING_GAUGE_CHANGE *)
            rFSM_StateTimer_ms := 0.0;
        ELSIF bTailOutDetected THEN
            iFSM_State := 7; (* Transition to TAIL_OUT_DECELERATION *)
            rFSM_StateTimer_ms := 0.0;
        END_IF;

    6: (* FLYING_GAUGE_CHANGE *)
        bQuickOpenActive := FALSE;
        bCoolantHeaderShutoffCmd := FALSE;
        rFlyingGaugeTransitionTimer_ms := rFlyingGaugeTransitionTimer_ms + (c_rTs * 1000.0);

        (* Smooth S-curve interpolation of target thickness over 1,500 ms *)
        IF rFlyingGaugeTransitionTimer_ms < 1500.0 THEN
            rTempSqrtVal := rFlyingGaugeTransitionTimer_ms / 1500.0;
            (* Smooth Hermite polynomial: 3*t^2 - 2*t^3 *)
            rTempSqrtVal := (3.0 * rTempSqrtVal * rTempSqrtVal) - (2.0 * rTempSqrtVal * rTempSqrtVal * rTempSqrtVal);
            rTargetExitThickness_mm := rFlyingGaugeInitialGauge_mm + (rTempSqrtVal * (rFlyingGaugeTargetGauge_mm - rFlyingGaugeInitialGauge_mm));
        ELSE
            rTargetExitThickness_mm := rFlyingGaugeTargetGauge_mm;
            bFlyingGaugeActive := FALSE;
            iFSM_State := 5; (* Return to steady state *)
            rFSM_StateTimer_ms := 0.0;
        END_IF;

    7: (* TAIL_OUT_DECELERATION *)
        bQuickOpenActive := FALSE;
        bCoolantHeaderShutoffCmd := FALSE;
        bHAGC_InRegulation := FALSE;

        (* Decelerate mill to tail-out velocity (120 m/min) at 2.4 m/s2 *)
        IF rRampCurrentSpeed_mpm > 120.0 THEN
            rRampCurrentSpeed_mpm := rRampCurrentSpeed_mpm - (144.0 * c_rTs);
        ELSE
            rRampCurrentSpeed_mpm := 120.0;
        END_IF;

        (* Tail bite release detection: roll force collapses when strip tail exits Stand 6 *)
        IF rVotedRollForce_kN < 250.0 THEN
            (* Strip tail has cleared bite: open roll gap immediately *)
            iFSM_State := 1; (* Return to HYDRAULIC_WARMUP for next coil *)
            rFSM_StateTimer_ms := 0.0;
        END_IF;

    8: (* COIL_STRIP_BREAK_TRIP *)
        bCobbleInterlockActive := TRUE;
        bCoolantHeaderShutoffCmd := TRUE;
        bHAGC_InRegulation := FALSE;
        rMainDriveSpeedTrim_mpm := 0.0;
        rStand5SpeedTrim_mpm := 0.0;

        (* Immediate transition to quick open *)
        iFSM_State := 9;
        rFSM_StateTimer_ms := 0.0;

    9: (* WORK_ROLL_QUICK_OPEN *)
        bQuickOpenActive := TRUE;
        bCoolantHeaderShutoffCmd := TRUE;
        bHAGC_InRegulation := FALSE;

        (* Force hydraulic servo spools to full negative retract (-40 mA) to open gap in <40 ms *)
        rServoValveSpoolCmd_OS_mA := -40.0;
        rServoValveSpoolCmd_DS_mA := -40.0;
        rRollBendingPressureCmd_bar := 0.0;
        rMainDriveSpeedTrim_mpm := 0.0;
        rStand5SpeedTrim_mpm := 0.0;

        (* Operator reset required after cobble or manual quick open *)
        IF bResetTripAlarms AND (rFSM_StateTimer_ms > 2000.0) THEN
            bCobbleInterlockActive := FALSE;
            bQuickOpenActive := FALSE;
            iFSM_State := 1; (* Return to HYDRAULIC_WARMUP *)
            rFSM_StateTimer_ms := 0.0;
        END_IF;

    10: (* MAINTENANCE_ROLL_CHANGE *)
        bQuickOpenActive := TRUE;
        bCoolantHeaderShutoffCmd := TRUE;
        bHAGC_InRegulation := FALSE;
        rServoValveSpoolCmd_OS_mA := 0.0;
        rServoValveSpoolCmd_DS_mA := 0.0;
        rRollBendingPressureCmd_bar := 0.0;

        IF bRollKissingCalibReq THEN
            iFSM_State := 0; (* Initiate kissing zeroing calibration *)
            rFSM_StateTimer_ms := 0.0;
        END_IF;

    11: (* EMERGENCY_ESTOP *)
        bQuickOpenActive := TRUE;
        bCoolantHeaderShutoffCmd := TRUE;
        bHAGC_InRegulation := FALSE;
        bCobbleInterlockActive := TRUE;
        rServoValveSpoolCmd_OS_mA := -40.0;
        rServoValveSpoolCmd_DS_mA := -40.0;
        rRollBendingPressureCmd_bar := 0.0;
        rMainDriveSpeedTrim_mpm := 0.0;
        rStand5SpeedTrim_mpm := 0.0;
        rRampCurrentSpeed_mpm := 0.0;

        IF NOT bEmergencyStop AND bResetTripAlarms THEN
            bCobbleInterlockActive := FALSE;
            bQuickOpenActive := FALSE;
            iFSM_State := 1; (* Clear to HYDRAULIC_WARMUP *)
            rFSM_StateTimer_ms := 0.0;
        END_IF;

END_CASE;

iCurrentFSMState := iFSM_State;
"""

print("Phase 7 defined.")


def get_phase8_alarms():
    return """
(* ========================================================================================= *)
(* === PHASE 8: ISA-18.2 ALARMS, CHATTER FREQUENCY DETECTION & DIAGNOSTIC PACKING       === *)
(* ========================================================================================= *)
(*
   Rigorous ISA-18.2 5-tier alarm hierarchy with deadband hysteresis & debouncing:
   - High-High (HI_HI), High (HI), Low (LO), Low-Low (LO_LO), and Rate-of-Change (ROC).
   - Dynamic mill chatter spectrum monitoring (3rd octave torsional & 5th octave acoustic).
   - Catastrophic hydraulic line rupture detector (negative pressure rate > 150 bar/s).
   - First-Out diagnostic latch capturing root cause trip before cascaded shutdowns.
   - Comprehensive 32-bit DWORD telemetry packing.
*)

(* 8.1 Rate of Change Calculations *)
rThicknessRateOfChange_mm_s := (rExitThicknessMeasured_mm - rPrevExitThickness_mm) / c_rTs;
rPrevExitThickness_mm := rExitThicknessMeasured_mm;

rForceRateOfChange_kN_s := (rVotedRollForce_kN - rPrevRollForce_kN) / c_rTs;
rPrevRollForce_kN := rVotedRollForce_kN;

rHeadPresRateOfChange_bar_s := (rVotedHeadPres - rPrevHeadPres_bar) / c_rTs;
rPrevHeadPres_bar := rVotedHeadPres;

(* 8.2 Strip Thickness Deviation Alarms [um] with Deadband Hysteresis *)
IF rGaugeError_um >= 6.0 THEN
    bAlarm_Thickness_HI_HI := TRUE;
ELSIF rGaugeError_um < 5.5 THEN
    bAlarm_Thickness_HI_HI := FALSE;
END_IF;

IF rGaugeError_um >= 2.5 THEN
    bAlarm_Thickness_HI := TRUE;
ELSIF rGaugeError_um < 2.0 THEN
    bAlarm_Thickness_HI := FALSE;
END_IF;

IF rGaugeError_um <= -2.5 THEN
    bAlarm_Thickness_LO := TRUE;
ELSIF rGaugeError_um > -2.0 THEN
    bAlarm_Thickness_LO := FALSE;
END_IF;

IF rGaugeError_um <= -6.0 THEN
    bAlarm_Thickness_LO_LO := TRUE;
ELSIF rGaugeError_um > -5.5 THEN
    bAlarm_Thickness_LO_LO := FALSE;
END_IF;

IF ABS(rThicknessRateOfChange_mm_s * 1000.0) >= 15.0 THEN
    bAlarm_Thickness_ROC := TRUE;
ELSE
    bAlarm_Thickness_ROC := FALSE;
END_IF;

(* 8.3 Roll Separating Force Alarms [kN] with Deadband Hysteresis *)
IF rVotedRollForce_kN >= 28000.0 THEN
    bAlarm_Force_HI_HI := TRUE;
ELSIF rVotedRollForce_kN < 27500.0 THEN
    bAlarm_Force_HI_HI := FALSE;
END_IF;

IF rVotedRollForce_kN >= 25000.0 THEN
    bAlarm_Force_HI := TRUE;
ELSIF rVotedRollForce_kN < 24500.0 THEN
    bAlarm_Force_HI := FALSE;
END_IF;

IF (rVotedRollForce_kN <= 4000.0) AND (iFSM_State >= 4) THEN
    bAlarm_Force_LO := TRUE;
ELSIF rVotedRollForce_kN > 4500.0 THEN
    bAlarm_Force_LO := FALSE;
END_IF;

IF (rVotedRollForce_kN <= 1500.0) AND (iFSM_State >= 4) THEN
    bAlarm_Force_LO_LO := TRUE;
ELSIF rVotedRollForce_kN > 2000.0 THEN
    bAlarm_Force_LO_LO := FALSE;
END_IF;

IF ABS(rForceRateOfChange_kN_s) >= 8000.0 THEN
    bAlarm_Force_ROC := TRUE;
ELSE
    bAlarm_Force_ROC := FALSE;
END_IF;

(* 8.4 Interstand Specific Tension Alarms [MPa] with Deadband Hysteresis *)
IF rActualSpecificTension_MPa >= 220.0 THEN
    bAlarm_Tension_HI_HI := TRUE;
ELSIF rActualSpecificTension_MPa < 210.0 THEN
    bAlarm_Tension_HI_HI := FALSE;
END_IF;

IF rActualSpecificTension_MPa >= 160.0 THEN
    bAlarm_Tension_HI := TRUE;
ELSIF rActualSpecificTension_MPa < 150.0 THEN
    bAlarm_Tension_HI := FALSE;
END_IF;

IF (rActualSpecificTension_MPa <= 40.0) AND (iFSM_State >= 4) THEN
    bAlarm_Tension_LO := TRUE;
ELSIF rActualSpecificTension_MPa > 48.0 THEN
    bAlarm_Tension_LO := FALSE;
END_IF;

IF (rActualSpecificTension_MPa <= 15.0) AND (iFSM_State >= 4) THEN
    bAlarm_Tension_LO_LO := TRUE;
ELSIF rActualSpecificTension_MPa > 22.0 THEN
    bAlarm_Tension_LO_LO := FALSE;
END_IF;

(* 8.5 Hydraulic Push-Up Cylinder Pressure Alarms [bar] *)
IF rVotedHeadPres >= 315.0 THEN
    bAlarm_HydPres_HI_HI := TRUE;
ELSIF rVotedHeadPres < 305.0 THEN
    bAlarm_HydPres_HI_HI := FALSE;
END_IF;

IF rVotedHeadPres >= 290.0 THEN
    bAlarm_HydPres_HI := TRUE;
ELSIF rVotedHeadPres < 280.0 THEN
    bAlarm_HydPres_HI := FALSE;
END_IF;

IF rVotedHeadPres <= 30.0 THEN
    bAlarm_HydPres_LO := TRUE;
ELSIF rVotedHeadPres > 40.0 THEN
    bAlarm_HydPres_LO := FALSE;
END_IF;

IF rVotedHeadPres <= 10.0 THEN
    bAlarm_HydPres_LO_LO := TRUE;
ELSIF rVotedHeadPres > 18.0 THEN
    bAlarm_HydPres_LO_LO := FALSE;
END_IF;

(* Catastrophic Hydraulic Line Rupture Interlock: Sudden pressure loss rate > 150 bar/s *)
IF rHeadPresRateOfChange_bar_s <= -150.0 THEN
    bAlarm_HydPres_Rupture_ROC := TRUE;
    (* Force immediate emergency stop *)
    iFSM_State := 11;
ELSIF rHeadPresRateOfChange_bar_s > -50.0 THEN
    bAlarm_HydPres_Rupture_ROC := FALSE;
END_IF;

(* 8.6 Mill Chatter Acoustic & Torsional Spectral Detection *)
(* 3rd Octave Torsional Resonance (120-180 Hz): trip speed trim rollback *)
IF rVibration_3rdOctave_RMS >= 4.5 THEN
    bAlarm_Chatter_3rdOctave_Trip := TRUE;
    bChatterVibrationWarning := TRUE;
    (* Rollback line speed reference by 10% to move away from critical chatter resonance *)
    rMainDriveSpeedTrim_mpm := rMainDriveSpeedTrim_mpm - 45.0;
ELSIF rVibration_3rdOctave_RMS < 3.2 THEN
    bAlarm_Chatter_3rdOctave_Trip := FALSE;
    bChatterVibrationWarning := FALSE;
END_IF;

(* 5th Octave Acoustic Roll Bite Chatter (500-700 Hz): gauge gain damping *)
IF rVibration_5thOctave_RMS >= 8.0 THEN
    bAlarm_Chatter_5thOctave_Warn := TRUE;
ELSIF rVibration_5thOctave_RMS < 6.0 THEN
    bAlarm_Chatter_5thOctave_Warn := FALSE;
END_IF;

(* 8.7 First-Out Fault Latching Root Cause Capture *)
IF iFirstOutFaultCode = 0 THEN
    IF bEmergencyStop THEN
        iFirstOutFaultCode := 1; (* Safety E-Stop Circuit *)
    ELSIF bAlarm_HydPres_Rupture_ROC THEN
        iFirstOutFaultCode := 2; (* Hydraulic Line Burst / Rupture *)
    ELSIF bCobbleInterlockActive THEN
        iFirstOutFaultCode := 3; (* Steel Strip Cobble / Snap *)
    ELSIF bAlarm_Force_HI_HI THEN
        iFirstOutFaultCode := 4; (* Roll Separating Force HI_HI Overload *)
    ELSIF bAlarm_Chatter_3rdOctave_Trip THEN
        iFirstOutFaultCode := 5; (* Mill Torsional Chatter Resonance *)
    ELSIF bAlarm_Thickness_HI_HI THEN
        iFirstOutFaultCode := 6; (* Exit Thickness Delivery Out of Tolerance *)
    ELSIF bAlarm_Tension_HI_HI THEN
        iFirstOutFaultCode := 7; (* Strip Interstand Tension Overstrain *)
    ELSIF bXray_CompleteFailure OR bForce_CompleteFailure OR bPosOS_CompleteFailure OR bPosDS_CompleteFailure OR bTens_CompleteFailure THEN
        iFirstOutFaultCode := 8; (* Redundant TMR Sensor Infrastructure Collapse *)
    END_IF;
ELSIF bResetTripAlarms THEN
    IF NOT bEmergencyStop AND NOT bAlarm_HydPres_Rupture_ROC AND NOT bCobbleInterlockActive THEN
        iFirstOutFaultCode := 0;
    END_IF;
END_IF;

(* 8.8 Telemetry Bit Packing: dwMillDiagnosticWord1 *)
dwMillDiagnosticWord1 := 16#00000000;
dwMillDiagnosticWord1 := dwMillDiagnosticWord1 OR INT_TO_DWORD(iFSM_State AND 16#0F);
IF bHAGC_InRegulation THEN dwMillDiagnosticWord1 := dwMillDiagnosticWord1 OR 16#00000010; END_IF;
IF bCobbleInterlockActive THEN dwMillDiagnosticWord1 := dwMillDiagnosticWord1 OR 16#00000020; END_IF;
IF bQuickOpenActive THEN dwMillDiagnosticWord1 := dwMillDiagnosticWord1 OR 16#00000040; END_IF;
IF bFlyingGaugeActive THEN dwMillDiagnosticWord1 := dwMillDiagnosticWord1 OR 16#00000080; END_IF;
IF bKissCalibInProgress THEN dwMillDiagnosticWord1 := dwMillDiagnosticWord1 OR 16#00000100; END_IF;
IF bEccentricityCompEnable THEN dwMillDiagnosticWord1 := dwMillDiagnosticWord1 OR 16#00000200; END_IF;
IF bRollBendingAutoEnable THEN dwMillDiagnosticWord1 := dwMillDiagnosticWord1 OR 16#00000400; END_IF;
IF bChatterVibrationWarning THEN dwMillDiagnosticWord1 := dwMillDiagnosticWord1 OR 16#00000800; END_IF;
IF bXray_Degraded1oo2 THEN dwMillDiagnosticWord1 := dwMillDiagnosticWord1 OR 16#00001000; END_IF;
IF bXray_CompleteFailure THEN dwMillDiagnosticWord1 := dwMillDiagnosticWord1 OR 16#00002000; END_IF;
IF bForce_Degraded1oo2 THEN dwMillDiagnosticWord1 := dwMillDiagnosticWord1 OR 16#00004000; END_IF;
IF bForce_CompleteFailure THEN dwMillDiagnosticWord1 := dwMillDiagnosticWord1 OR 16#00008000; END_IF;
IF bPosOS_Degraded1oo2 THEN dwMillDiagnosticWord1 := dwMillDiagnosticWord1 OR 16#00010000; END_IF;
IF bPosOS_CompleteFailure THEN dwMillDiagnosticWord1 := dwMillDiagnosticWord1 OR 16#00020000; END_IF;
IF bPosDS_Degraded1oo2 THEN dwMillDiagnosticWord1 := dwMillDiagnosticWord1 OR 16#00040000; END_IF;
IF bPosDS_CompleteFailure THEN dwMillDiagnosticWord1 := dwMillDiagnosticWord1 OR 16#00080000; END_IF;
IF bTens_Degraded1oo2 THEN dwMillDiagnosticWord1 := dwMillDiagnosticWord1 OR 16#00100000; END_IF;
IF bTens_CompleteFailure THEN dwMillDiagnosticWord1 := dwMillDiagnosticWord1 OR 16#00200000; END_IF;
IF bHeadPres_Degraded1oo2 THEN dwMillDiagnosticWord1 := dwMillDiagnosticWord1 OR 16#00400000; END_IF;
IF bHeadPres_CompleteFailure THEN dwMillDiagnosticWord1 := dwMillDiagnosticWord1 OR 16#00800000; END_IF;
IF bSpeed_Degraded1oo2 THEN dwMillDiagnosticWord1 := dwMillDiagnosticWord1 OR 16#01000000; END_IF;

(* 8.9 Telemetry Bit Packing: dwMillDiagnosticWord2 *)
dwMillDiagnosticWord2 := 16#00000000;
IF rSpoolPosOS_mA >= 39.9 THEN dwMillDiagnosticWord2 := dwMillDiagnosticWord2 OR 16#00000001; END_IF;
IF rSpoolPosOS_mA <= -39.9 THEN dwMillDiagnosticWord2 := dwMillDiagnosticWord2 OR 16#00000002; END_IF;
IF rSpoolPosDS_mA >= 39.9 THEN dwMillDiagnosticWord2 := dwMillDiagnosticWord2 OR 16#00000004; END_IF;
IF rSpoolPosDS_mA <= -39.9 THEN dwMillDiagnosticWord2 := dwMillDiagnosticWord2 OR 16#00000008; END_IF;
IF rMainDriveSpeedTrim_mpm >= 59.9 THEN dwMillDiagnosticWord2 := dwMillDiagnosticWord2 OR 16#00000010; END_IF;
IF rMainDriveSpeedTrim_mpm <= -59.9 THEN dwMillDiagnosticWord2 := dwMillDiagnosticWord2 OR 16#00000020; END_IF;
IF rRollBendingPressureCmd_bar >= 239.9 THEN dwMillDiagnosticWord2 := dwMillDiagnosticWord2 OR 16#00000040; END_IF;
IF rRollBendingPressureCmd_bar <= 40.1 THEN dwMillDiagnosticWord2 := dwMillDiagnosticWord2 OR 16#00000080; END_IF;
dwMillDiagnosticWord2 := dwMillDiagnosticWord2 OR SHL(INT_TO_DWORD(iFirstOutFaultCode AND 16#FF), 8);

(* 8.10 Telemetry Bit Packing: dwAlarmStatusWord (ISA-18.2) *)
dwAlarmStatusWord := 16#00000000;
IF bAlarm_Thickness_HI_HI THEN dwAlarmStatusWord := dwAlarmStatusWord OR 16#00000001; END_IF;
IF bAlarm_Thickness_HI THEN dwAlarmStatusWord := dwAlarmStatusWord OR 16#00000002; END_IF;
IF bAlarm_Thickness_LO THEN dwAlarmStatusWord := dwAlarmStatusWord OR 16#00000004; END_IF;
IF bAlarm_Thickness_LO_LO THEN dwAlarmStatusWord := dwAlarmStatusWord OR 16#00000008; END_IF;
IF bAlarm_Thickness_ROC THEN dwAlarmStatusWord := dwAlarmStatusWord OR 16#00000010; END_IF;
IF bAlarm_Force_HI_HI THEN dwAlarmStatusWord := dwAlarmStatusWord OR 16#00000020; END_IF;
IF bAlarm_Force_HI THEN dwAlarmStatusWord := dwAlarmStatusWord OR 16#00000040; END_IF;
IF bAlarm_Force_LO THEN dwAlarmStatusWord := dwAlarmStatusWord OR 16#00000080; END_IF;
IF bAlarm_Force_LO_LO THEN dwAlarmStatusWord := dwAlarmStatusWord OR 16#00000100; END_IF;
IF bAlarm_Force_ROC THEN dwAlarmStatusWord := dwAlarmStatusWord OR 16#00000200; END_IF;
IF bAlarm_Tension_HI_HI THEN dwAlarmStatusWord := dwAlarmStatusWord OR 16#00000400; END_IF;
IF bAlarm_Tension_HI THEN dwAlarmStatusWord := dwAlarmStatusWord OR 16#00000800; END_IF;
IF bAlarm_Tension_LO THEN dwAlarmStatusWord := dwAlarmStatusWord OR 16#00001000; END_IF;
IF bAlarm_Tension_LO_LO THEN dwAlarmStatusWord := dwAlarmStatusWord OR 16#00002000; END_IF;
IF bAlarm_HydPres_HI_HI THEN dwAlarmStatusWord := dwAlarmStatusWord OR 16#00004000; END_IF;
IF bAlarm_HydPres_HI THEN dwAlarmStatusWord := dwAlarmStatusWord OR 16#00008000; END_IF;
IF bAlarm_HydPres_LO THEN dwAlarmStatusWord := dwAlarmStatusWord OR 16#00010000; END_IF;
IF bAlarm_HydPres_LO_LO THEN dwAlarmStatusWord := dwAlarmStatusWord OR 16#00020000; END_IF;
IF bAlarm_HydPres_Rupture_ROC THEN dwAlarmStatusWord := dwAlarmStatusWord OR 16#00040000; END_IF;
IF bAlarm_Chatter_3rdOctave_Trip THEN dwAlarmStatusWord := dwAlarmStatusWord OR 16#00080000; END_IF;
IF bAlarm_Chatter_5thOctave_Warn THEN dwAlarmStatusWord := dwAlarmStatusWord OR 16#00100000; END_IF;

END_FUNCTION_BLOCK
"""

print("Phase 8 defined.")


def test_generation():
    st_code = build_st_code() + get_phase1_tmr() + get_phase2_mechanics() + get_phase3_kalman() + get_phase4_statespace() + get_phase5_mpc() + get_phase6_servo() + get_phase7_fsm() + get_phase8_alarms()
    print("Total ST Code Length (characters):", len(st_code))
    return st_code

if __name__ == "__main__":
    code = test_generation()
