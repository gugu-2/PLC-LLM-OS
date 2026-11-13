# build_imm_dataset.py
# Generator for FB_Plastics_AllElectric_IMM_VPTransfer_CavityPressure
import sys
import json
import uuid
import re
import os

def generate_header():
    return """FUNCTION_BLOCK FB_Plastics_AllElectric_IMM_VPTransfer_CavityPressure
(*
========================================================================================================================
LUMINA CYBER-PHYSICAL AUTOMATION ENGINE - SYNTHETIC DATASET V7 MAX-PERSONA
COMMERCIAL PLASTICS & POLYMER PROCESSING DIVISION - HEAVY AUTOMOTIVE OPTICAL MOLDING
========================================================================================================================
SYSTEM SPECIFICATION:
  - Machine Designation : 2,500-Metric-Ton (25,000 kN) All-Electric High-Precision Injection Molding Machine (IMM).
  - Target Application : Multi-Cavity Automotive Matrix LED Headlamp Optical Primary Lens & Thick Light Guides.
  - Polymer Substrate   : Optical-Grade Polycarbonate (PC) / High-Purity PMMA with High Optical Transmittance (>92%).
  - Cycle Scan Time     : Discrete Deterministic Real-Time Synchronous Execution Cycle Ts = 1.0 ms (1,000 Hz).
  - Primary Subsystems  :
    1. High-Performance All-Electric Injection Unit:
       * Dual synchronous AC permanent magnet servo drives (2x 75 kW, 3,000 rpm) coupled to twin precision planetary
         roller screws with dynamic torque synchronization and sub-0.05 um optical scale position feedback.
       * Injection velocity dynamic range: 0.01 mm/s to 350.0 mm/s; maximum injection pressure: 2,200.0 bar.
    2. Precision Plasticizing Extruder & Recovery Unit:
       * Direct-drive water-cooled high-torque permanent magnet servomotor (45 kW, 0-350 RPM continuous).
       * Closed-loop proportional electric backpressure valve and load cell (0.0 to 250.0 bar) ensuring melt density
         homogeneity and zero micro-bubble entrainment.
       * 5-Zone high-watt-density ceramic heating barrel with integrated solid-state relays and dual thermocouples.
    3. Ultra-Rigid 25,000 kN Clamping Unit & Tie-Bar Parallelism Engine:
       * Five-point double-toggle high-rigidity clamping mechanism actuated by a 110 kW high-torque servo drive.
       * 4 high-tensile alloy steel tie-bars (diameter 280 mm, span 2,400 mm x 2,100 mm) with individual piezoelectric
         quartz load washers monitoring dynamic tie-bar strain, mold platen tilt, and platen bending moments.
       * Real-time tie-bar asymmetry calculation and parting-line separation deflection observer (< 1 ms trip).
    4. Multi-Cavity Hot Runner & In-Cavity Direct Piezoelectric Quartz Instrumentation:
       * 4-Cavity hot runner manifold with individual high-speed servo-pneumatic needle valve gates.
       * Flush-mounted piezoelectric quartz pressure sensors located in Cavity 1 (near gate) and Cavity 4 (end-of-fill).
       * Conformal oil temperature conditioning circuits (115.0 deg C to 135.0 deg C) with proportional 3-way mixing.
    5. Cyber-Physical Automation Core:
       * 8-State discrete state-space formulation at Ts = 1.0 ms: x[k+1] = A*x[k] + B*u[k], y[k] = C*x[k] + D*u[k].
       * Steady-state Luenberger / Kalman observer innovation gain matrix L (8x6) with error residual correction.
       * Receding-Horizon Model Predictive Control (MPC) quadratic cost optimization with prediction horizon N = 5 steps
         and 6 unrolled iterations of Projected Gradient Descent (PGD) with analytical box and slew rate saturation.
       * High-speed dynamic V/P (Velocity-to-Pressure) transfer point decoupling (< 0.5 ms trigger, sub-0.1 mm window).
       * 2oo3 (Two-out-of-Three) Triple Modular Redundancy (TMR) voting suite across 5 critical sensor channels with
         100 ms discrepancy debounce timers and bumpless degradation.
       * Deterministic 14-Stage Production Finite State Machine (FSM) governing mold close, lockup, fill, V/P switch,
         5-stage packing, gate freeze-off detection, plasticizing, decompression, mold open, and servo ejection.
       * ISA-18.2 multi-tiered process alarm matrix (HH, H, L, LL), deadband hysteresis, and 32-bit packed telemetry.

========================================================================================================================
THEORETICAL FOUNDATIONS & POLYMER RHEOLOGICAL ARCHITECTURE:
------------------------------------------------------------------------------------------------------------------------
1. NON-NEWTONIAN POLYMER MELT RHEOLOGY & CROSS-WLF EQUATION:
   Polycarbonate melt exhibits strong non-Newtonian pseudoplastic (shear-thinning) behavior governed by temperature,
   hydrostatic pressure, and shear rate. The apparent dynamic viscosity eta(T, P, gamma_dot) is modeled via the Cross-WLF
   constitutive relationship:
       eta(T, P, gamma_dot) = eta_0(T, P) / ( 1.0 + ( (eta_0(T, P) * gamma_dot) / tau_star )^(1.0 - n_index) )
   where:
       eta_0(T, P) = Zero-shear viscosity [Pa.s]
       tau_star    = Critical shear stress at the onset of shear thinning [Pa] (approx 1.95e5 Pa for optical PC)
       n_index     = Power-law pseudoplastic shear-thinning index [-] (approx 0.31 for optical PC)
       gamma_dot   = Apparent shear rate in runner/nozzle [1/s]
   The zero-shear viscosity eta_0 depends on melt temperature T and hydrostatic pressure P via the Williams-Landel-Ferry (WLF)
   free-volume expression referenced to glass transition temperature T_g:
       eta_0(T, P) = D1 * exp( - (A1 * (T - T_star)) / (A2 + (T - T_star)) )
       T_star      = D2 + (D3 * P)
       A2          = A2_prime + (D3 * P)
   For automotive optical grade Polycarbonate:
       D1 = 3.80e11 Pa.s, D2 = 418.15 K (145.0 deg C), D3 = 0.00e-6 K/Pa, A1 = 28.50, A2_prime = 51.60 K.
   Apparent shear rate at the nozzle orifice (radius R_nozzle = 4.0 mm) is evaluated dynamically:
       Q_volumetric = A_screw * v_screw = (PI * R_screw^2) * v_screw
       gamma_dot    = (4.0 * Q_volumetric) / (PI * R_nozzle^3)

2. TAIT & SPENCER-GILMORE EQUATIONS OF STATE (PVT COMPRESSIBILITY):
   High-precision optical lens molding requires micro-volumetric shrinkage control to prevent sink marks, optical
   aberrations, and localized residual stress birefringence. The Spencer-Gilmore PVT equation of state relates pressure P,
   specific volume v_hat, and absolute temperature T:
       ( P + P_const ) * ( v_hat - v_const ) = ( R_polymer * T )
   For Polycarbonate:
       P_const   = 2.124e8 Pa (2,124.0 bar)
       v_const   = 0.000822 m^3/kg
       R_polymer = 79.25 J/(kg.K)
   During volumetric filling and packing, melt compressibility beta_melt is evaluated dynamically:
       beta_melt = - (1.0 / v_hat) * (dv_hat / dP)_T = 1.0 / ( P + P_const ) [1/Pa]
   Bulk modulus K_bulk = 1.0 / beta_melt ranges from 12,000 bar to 24,000 bar. This governs nozzle pressure rise rate:
       dP_nozzle / dt = (K_bulk / V_melt(s)) * ( A_screw * v_screw - Q_cavity )

3. GATE SOLIDIFICATION & THERMAL PENETRATION 1D STEFAN PROBLEM:
   The transition from multi-stage holding pressure to gate freeze-off represents the point of mass isolation for the
   molded optical lens. Thermal conduction into the cold mold wall (T_mold = 120.0 deg C) from melt (T_melt = 295.0 deg C)
   drives solidified frozen skin layer growth delta_skin(t) across gate half-thickness b_gate (b_gate = 1.50 mm):
       delta_skin(t) = 2.0 * lambda_solid * sqrt( alpha_thermal * t_pack )
   where:
       alpha_thermal = k_thermal / (rho_melt * Cp_melt) approx 1.15e-7 m^2/s
       lambda_solid  = Solidification eigenvalue determined by transcendental Stefan phase-change condition:
                       lambda * exp(lambda^2) * erf(lambda) = St / sqrt(PI)
                       St = Stefan Number = Cp_melt * (T_melt - T_mold) / Delta_H_fusion
   Gate freeze-off is confirmed when delta_skin(t) >= b_gate, melt flow ceases (Q_gate -> 0), cavity pressure derivative
   d(P_cavity)/dt decays to zero, and screw forward displacement halts.

4. MOLD CLAMPING FORCE & PARTING LINE DEFLECTION MECHANICS:
   A total clamping force of 25,000 kN (2,500 metric tons) is distributed across 4 massive tie-bars. Mold cavity projected
   area A_projected = 0.285 m^2 (285,000 mm^2). Dynamic melt pressure inside the 4 cavities generates an opening force:
       F_opening(t) = sum_{c=1}^4 P_cavity_c(t) * A_cavity_c
   When F_opening approaches clamping pre-load F_clamp, mold core-cavity separation occurs:
       Delta_z_parting = ( F_opening - F_clamp ) / K_mold_stiffness  [for F_opening > F_clamp]
   Parting line separation exceeding 15.0 um produces optical lens flash, ruining lens optical edge seals and causing
   permanent tool damage. The cyber-physical controller implements a sub-1.0 ms mold flash safety dump loop.
*)
"""

def generate_var_input():
    return """VAR_INPUT
    (* ================================================================================================ *)
    (* SENSOR INPUTS: TRIPLE MODULAR REDUNDANCY (2oo3) SUITE                                            *)
    (* ================================================================================================ *)
    rPT_Nozzle_101A                     : REAL;     (* Nozzle Melt Pressure Transducer Channel A [bar] *)
    rPT_Nozzle_101B                     : REAL;     (* Nozzle Melt Pressure Transducer Channel B [bar] *)
    rPT_Nozzle_101C                     : REAL;     (* Nozzle Melt Pressure Transducer Channel C [bar] *)
    rPT_Cavity_201A                     : REAL;     (* Cavity 1 Quartz Piezoelectric Sensor Channel A [bar] *)
    rPT_Cavity_201B                     : REAL;     (* Cavity 1 Quartz Piezoelectric Sensor Channel B [bar] *)
    rPT_Cavity_201C                     : REAL;     (* Cavity 1 Quartz Piezoelectric Sensor Channel C [bar] *)
    rPT_Cavity_204_EndFill              : REAL;     (* Cavity 4 Quartz Piezoelectric Sensor End-of-Fill [bar] *)
    rST_ScrewPos_301A                   : REAL;     (* Screw Linear Optical Scale Channel A [mm] *)
    rST_ScrewPos_301B                   : REAL;     (* Screw Linear Optical Scale Channel B [mm] *)
    rST_ScrewPos_301C                   : REAL;     (* Screw Linear Optical Scale Channel C [mm] *)
    rWT_Tonnage_401A                    : REAL;     (* Tie-Bar 1 Piezoelectric Strain Gauge Load Cell [kN] *)
    rWT_Tonnage_401B                    : REAL;     (* Tie-Bar 2 Piezoelectric Strain Gauge Load Cell [kN] *)
    rWT_Tonnage_401C                    : REAL;     (* Tie-Bar 3 Piezoelectric Strain Gauge Load Cell [kN] *)
    rWT_Tonnage_404_TB4                 : REAL;     (* Tie-Bar 4 Piezoelectric Strain Gauge Load Cell [kN] *)
    rTT_MoldTemp_501A                   : REAL;     (* Mold Core Tooling Thermocouple Channel A [deg C] *)
    rTT_MoldTemp_501B                   : REAL;     (* Mold Core Tooling Thermocouple Channel B [deg C] *)
    rTT_MoldTemp_501C                   : REAL;     (* Mold Core Tooling Thermocouple Channel C [deg C] *)

    (* Auxiliary Process Transducers & Position Encoders *)
    rTT_BarrelMeltTemp_Zone1            : REAL;     (* Barrel Heating Zone 1 Nozzle Melt Temperature [deg C] *)
    rTT_BarrelMeltTemp_Zone2            : REAL;     (* Barrel Heating Zone 2 Front Metering Temperature [deg C] *)
    rTT_BarrelMeltTemp_Zone3            : REAL;     (* Barrel Heating Zone 3 Middle Transition Temperature [deg C] *)
    rTT_BarrelMeltTemp_Zone4            : REAL;     (* Barrel Heating Zone 4 Feed Throat Temperature [deg C] *)
    rPT_Backpressure_FB                 : REAL;     (* Electric Backpressure Load Cell Feedback [bar] *)
    rST_MoldPlatenPos                   : REAL;     (* Moving Platen Absolute Linear Optical Scale [mm] *)
    rST_EjectorPos                      : REAL;     (* Servo Multi-Pin Ejector Rod Position [mm] *)
    rST_CarriagePos                     : REAL;     (* Injection Unit Carriage Cylinder Position [mm] *)
    rWT_NozzleContactForce              : REAL;     (* Carriage Nozzle-to-Sprue Touch Load Cell [kN] *)

    (* Operator Control Commands & Digital Safety Interlocks *)
    bAutoCycleStart                     : BOOL;     (* Semi/Full Automatic Production Cycle Start Trigger [-] *)
    bAutoCycleStop                      : BOOL;     (* Production Cycle Orderly Stop at End of Shot [-] *)
    bEmergencyStop                      : BOOL;     (* Hardwired Dual-Channel E-Stop Safety Relay Health [-] *)
    bSafetyGateClosed                   : BOOL;     (* Operator Safety Front Guard Gate Interlock Closed [-] *)
    bRearSafetyGateClosed               : BOOL;     (* Rear Service Guard Safety Interlock Closed [-] *)
    bPartDropVerified                   : BOOL;     (* Optical Light Curtain Lens Drop Verification [-] *)
    bRobotTakeoutHandshake              : BOOL;     (* 6-Axis Part Extraction Robot Clear Handshake [-] *)
    bHydraulicPumpsReady                : BOOL;     (* Auxiliary Hydraulic Core-Pull Unit Running [-] *)
    bElectricServosReady                : BOOL;     (* All Servo Drive DC Bus Power & Feedback Healthy [-] *)
    bManualResetAlarms                  : BOOL;     (* Pushbutton Manual Alarm Acknowledge & Reset [-] *)

    (* Production Recipes & Process Setpoints *)
    rSet_ClampTonnage_Target            : REAL;     (* High-Pressure Mold Clamping Force Setpoint [kN] *)
    rSet_InjectionSpeed_Stage1          : REAL;     (* Injection Fill Velocity Profile Stage 1 [mm/s] *)
    rSet_InjectionSpeed_Stage2          : REAL;     (* Injection Fill Velocity Profile Stage 2 [mm/s] *)
    rSet_InjectionSpeed_Stage3          : REAL;     (* Injection Fill Velocity Profile Stage 3 [mm/s] *)
    rSet_InjectionSpeed_Stage4          : REAL;     (* Injection Fill Velocity Profile Stage 4 [mm/s] *)
    rSet_VP_PositionThreshold           : REAL;     (* Primary V/P Switchover Linear Stroke Threshold [mm] *)
    rSet_VP_CavityPressureThreshold     : REAL;     (* Dynamic V/P Switchover Cavity Pressure Threshold [bar] *)
    rSet_VP_PressureDerivThreshold      : REAL;     (* Dynamic V/P Switchover Cavity Pressure Derivative [bar/s] *)
    rSet_HoldPressure_Stage1            : REAL;     (* Holding Pressure Profile Stage 1 Initial Pack [bar] *)
    rSet_HoldPressure_Stage2            : REAL;     (* Holding Pressure Profile Stage 2 Main Pack [bar] *)
    rSet_HoldPressure_Stage3            : REAL;     (* Holding Pressure Profile Stage 3 Density Pack [bar] *)
    rSet_HoldPressure_Stage4            : REAL;     (* Holding Pressure Profile Stage 4 Gate Freeze Pack [bar] *)
    rSet_HoldPressure_Stage5            : REAL;     (* Holding Pressure Profile Stage 5 Stress Relaxation [bar] *)
    rSet_HoldTime_Stage1                : REAL;     (* Holding Duration Profile Stage 1 [s] *)
    rSet_HoldTime_Stage2                : REAL;     (* Holding Duration Profile Stage 2 [s] *)
    rSet_HoldTime_Stage3                : REAL;     (* Holding Duration Profile Stage 3 [s] *)
    rSet_HoldTime_Stage4                : REAL;     (* Holding Duration Profile Stage 4 [s] *)
    rSet_HoldTime_Stage5                : REAL;     (* Holding Duration Profile Stage 5 [s] *)
    rSet_PlasticizingRPM                : REAL;     (* Screw Recovery Metering Rotation Speed [rpm] *)
    rSet_PlasticizingBackpress          : REAL;     (* Proportional Backpressure Setpoint During Recovery [bar] *)
    rSet_PlasticizingStroke             : REAL;     (* Metering Shot Size Screw Stroke Target [mm] *)
    rSet_DecompressionStroke            : REAL;     (* Post-Recovery Melt Suckback Stroke [mm] *)
    rSet_CoolingTime                    : REAL;     (* In-Mold Quench Cooling Time Duration [s] *)
    rSet_MoldOpenStroke                 : REAL;     (* Moving Platen Daylight Open Position Target [mm] *)
    rSet_EjectorStroke                  : REAL;     (* Multi-Pin Servo Ejector Stroke Forward [mm] *)
    rSet_EjectorPulses                  : DINT;     (* Number of Ejection Shaking Demolding Pulses [-] *)
    rSet_MaxFillTimeLimit               : REAL      (* Watchdog Volumetric Fill Timeout Limit [s] *)
END_VAR
"""

def generate_var_output():
    return """VAR_OUTPUT
    (* ================================================================================================ *)
    (* SERVO DRIVE COMMANDS & ACTUATION OUTPUTS                                                         *)
    (* ================================================================================================ *)
    rCmd_InjectionServoCurrent_pct      : REAL;     (* Injection Servo Drive Torque/Current Command [-100.0..100.0] [%] *)
    rCmd_HoldingPressure_bar            : REAL;     (* Holding Pressure Servo Pressure Regulator [0.0..2200.0] [bar] *)
    rCmd_ScrewRotationSpeed_rpm         : REAL;     (* Plasticizing Extruder Motor Speed Command [0.0..350.0] [rpm] *)
    rCmd_BackpressureValve_bar          : REAL;     (* Proportional Electric Backpressure Valve Command [0.0..250.0] [bar] *)
    rCmd_MoldCoolingValve_pct           : REAL;     (* Conformal Oil Temperature Proportional Valve [0.0..100.0] [%] *)
    rCmd_ClampingToggleServo_pct        : REAL;     (* Five-Point Clamping Toggle Servo Speed Command [0.0..100.0] [%] *)
    rCmd_EjectorServoSpeed_pct          : REAL;     (* Multi-Pin Servo Ejector Advance/Retract Command [-100.0..100.0] [%] *)
    rCmd_CarriageServoSpeed_pct         : REAL;     (* Injection Carriage Forward/Retract Speed [-100.0..100.0] [%] *)
    bCmd_HotRunnerValveGatesOpen        : BOOL;     (* 4-Cavity Pneumatic Valve Gate Solenoid Actuators [-] *)
    bCmd_PurgeGuardLock                 : BOOL;     (* Nozzle Purge Shield Safety Solenoid Guard Lock [-] *)

    (* Real-Time Monitored & Estimated Cyber-Physical Telemetry *)
    nState_Current                      : DINT;     (* Current Active Production FSM State Index [0..13] [-] *)
    rEst_ScrewVelocity_mms              : REAL;     (* Observer Filtered Screw Linear Velocity [mm/s] *)
    rEst_NozzlePressure_bar             : REAL;     (* Observer Filtered Nozzle Dynamic Pressure [bar] *)
    rEst_Cavity1Pressure_bar            : REAL;     (* Observer Filtered Cavity 1 Dynamic Pressure [bar] *)
    rEst_Cavity4Pressure_bar            : REAL;     (* Observer Filtered Cavity 4 Dynamic Pressure [bar] *)
    rEst_ClampingTonnage_kN             : REAL;     (* Observer Filtered Total Tie-Bar Clamping Force [kN] *)
    rEst_TieBarAsymmetry_kN             : REAL;     (* Maximum Tie-Bar Diagonal Strain Imbalance [kN] *)
    rEst_MoldDeflection_um              : REAL;     (* Dynamic Mold Parting Line Separation Deflection [um] *)
    rEst_GateSkinThickness_um           : REAL;     (* Real-Time Gate Solidification Frozen Skin Thickness [um] *)
    rEst_MeltApparentViscosity_Pas      : REAL;     (* Cross-WLF Online Melt Apparent Dynamic Viscosity [Pa.s] *)
    rEst_MeltShearRate_s1               : REAL;     (* Real-Time Nozzle Melt Apparent Shear Rate [1/s] *)
    rEst_CavityPressureDeriv_bars       : REAL;     (* Numerical Filtered Derivative of Cavity 1 Pressure [bar/s] *)
    rMon_CushionPosition_mm             : REAL;     (* Minimum Screw Cushion Reached at Holding Completion [mm] *)
    rMon_FillTime_sec                   : REAL;     (* Measured Volumetric Injection Fill Duration [s] *)
    rMon_CycleTime_sec                  : REAL;     (* Total Shot-to-Shot Machine Cycle Duration [s] *)
    rMon_PeakCavityPressure_bar         : REAL;     (* Peak Cavity Pressure Recorded During Injection Shot [bar] *)
    rMon_ScrewLinearPos_mm              : REAL;     (* Filtered Screw Absolute Linear Position [mm] *)
    bVP_TransferTriggered               : BOOL;     (* High-Speed V/P Transfer Switchover Event Latched [-] *)
    bGateFreezeOffAchieved              : BOOL;     (* Gate Solidification Mass Isolation Confirmed [-] *)
    bCycleCompletePulse                 : BOOL;     (* One-Shot Machine Cycle Finished Strobe Pulse [-] *)

    (* Safety & ISA-18.2 Process Alarms *)
    bAlarm_DieFlashMoldSeparationTrip   : BOOL;     (* Ultra-Fast Parting Line Separation / Flash Safety Trip [-] *)
    bAlarm_TieBarImbalanceTrip          : BOOL;     (* Tie-Bar Strain Asymmetry Exceeded Permissible Limit [-] *)
    bAlarm_OverpressureNozzle_HH        : BOOL;     (* Nozzle Pressure High-High Emergency Dump Safety Trip [-] *)
    bAlarm_OverpressureCavity_HH        : BOOL;     (* Cavity Pressure High-High Tool Protection Safety Trip [-] *)
    bAlarm_LowCushionWarning_L          : BOOL;     (* Screw Cushion Low Warning (Process Repeatability) [-] *)
    bAlarm_GateFreezeTimeout            : BOOL;     (* Gate Solidification Watchdog Expired Warning [-] *)
    bAlarm_TmrSensorFault               : BOOL;     (* Any 2oo3 Sensor Group Discordance Active [-] *)

    (* 32-Bit Telemetry Bit-Packed Registers *)
    dwStatusWord1                       : DWORD;    (* Bit-Packed Operational Status Register 1 [32 bits] *)
    dwStatusWord2                       : DWORD;    (* Bit-Packed Operational Status Register 2 [32 bits] *)
    dwAlarmWord1                        : DWORD;    (* Bit-Packed ISA-18.2 Critical Emergency Trip Register [32 bits] *)
    dwAlarmWord2                        : DWORD;    (* Bit-Packed ISA-18.2 Process Warning & Limit Register [32 bits] *)
    dwFirstOutWord                      : DWORD     (* Bit-Packed First-Out Root Cause Diagnostic Register [32 bits] *)
END_VAR
"""

def generate_var():
    return """VAR
    (* Execution Control & Initialization Variables *)
    bInitialized                        : BOOL := FALSE;    (* One-Shot System Memory & Matrix Initialization Latch [-] *)
    nScanCounter                        : DINT := 0;        (* Discrete PLC Execution Scan Counter [-] *)
    rCycleTime_sec                      : REAL := 0.001;    (* Discrete PLC Execution Cycle Interval Ts = 1.0 ms [s] *)
    i                                   : DINT;             (* General Purpose Loop Index i [-] *)
    j                                   : DINT;             (* General Purpose Loop Index j [-] *)
    k_idx                               : DINT;             (* MPC Horizon Rollout Step Index k [-] *)
    iter_idx                            : DINT;             (* MPC Projected Gradient Descent Iteration Index [-] *)
    rTempSum                            : REAL;             (* Temporary Matrix Multiplication Accumulator [various] *)

    (* Cyber-Physical 8-State Discrete State-Space Model Vectors & Matrices *)
    (* State Vector x in R^8:
         x[1]: Screw Linear Velocity [mm/s]
         x[2]: Nozzle Melt Dynamic Pressure [bar]
         x[3]: Cavity 1 Direct Piezoelectric Pressure [bar]
         x[4]: Cavity 4 Direct Piezoelectric Pressure [bar]
         x[5]: Clamping Unit 4-Tie-Bar Total Tonnage [kN]
         x[6]: Mold Cavity Surface Temperature [deg C]
         x[7]: Gate Solidification Skin Thickness [um]
         x[8]: Screw Electric Backpressure [bar]
       Control Vector u in R^6:
         u[1]: Injection Servo Drive Current Command [-100.0..100.0] [%]
         u[2]: Holding Pressure Servo Pressure Command [0.0..2200.0] [bar]
         u[3]: Plasticizing Screw Rotation Speed [0.0..350.0] [rpm]
         u[4]: Backpressure Proportional Valve Command [0.0..250.0] [bar]
         u[5]: Mold Oil Temperature Valve Command [0.0..100.0] [%]
         u[6]: Clamping Toggle Servo Speed Command [0.0..100.0] [%]
       Output Measurement Vector y in R^6:
         y[1]: Screw Linear Velocity [mm/s]
         y[2]: Nozzle Dynamic Pressure [bar]
         y[3]: Cavity 1 Piezo Pressure [bar]
         y[4]: Cavity 4 Piezo Pressure [bar]
         y[5]: Clamping Total Tonnage [kN]
         y[6]: Mold Cavity Surface Temperature [deg C] *)
    x_state                             : ARRAY[1..8] OF REAL;      (* Estimated Cyber-Physical State Vector x[k] [various] *)
    x_hat                               : ARRAY[1..8] OF REAL;      (* Luenberger Innovation-Corrected State Vector [various] *)
    x_pred                              : ARRAY[1..8] OF REAL;      (* A-Priori Predicted State Vector x[k+1|k] [various] *)
    x_ref                               : ARRAY[1..8] OF REAL;      (* Target State Reference Trajectory Vector [various] *)
    u_ctrl                              : ARRAY[1..6] OF REAL;      (* Applied Control Actuator Vector u[k] [various] *)
    u_prev                              : ARRAY[1..6] OF REAL;      (* Previous Scan Control Vector u[k-1] [various] *)
    u_mpc_opt                           : ARRAY[1..6] OF REAL;      (* MPC Optimal Unconstrained Control Vector [various] *)
    y_meas                              : ARRAY[1..6] OF REAL;      (* Filtered 2oo3 Sensor Measurement Vector [various] *)
    y_est                               : ARRAY[1..6] OF REAL;      (* Model Estimated Physical Output Vector [various] *)
    e_innov                             : ARRAY[1..6] OF REAL;      (* Luenberger Innovation Residual Vector [various] *)

    matA                                : ARRAY[1..8, 1..8] OF REAL;(* Discrete State Transition Matrix A (8x8) [-] *)
    matB                                : ARRAY[1..8, 1..6] OF REAL;(* Manipulated Input Coupling Matrix B (8x6) [-] *)
    matC                                : ARRAY[1..6, 1..8] OF REAL;(* Observation Measurement Matrix C (6x8) [-] *)
    matD                                : ARRAY[1..6, 1..6] OF REAL;(* Direct Feedthrough Coupling Matrix D (6x6) [-] *)
    matL                                : ARRAY[1..8, 1..6] OF REAL;(* Luenberger Observer Innovation Gains (8x6) [-] *)

    (* Model Predictive Control (MPC) Cost Matrices & Saturation Bounds *)
    matQ                                : ARRAY[1..8, 1..8] OF REAL;(* State Tracking Quadratic Penalty Matrix (8x8) [-] *)
    matR                                : ARRAY[1..6, 1..6] OF REAL;(* Actuator Effort Quadratic Penalty Matrix (6x6) [-] *)
    matS                                : ARRAY[1..6, 1..6] OF REAL;(* Actuator Slew Rate Quadratic Penalty Matrix (6x6) [-] *)
    matP                                : ARRAY[1..8, 1..8] OF REAL;(* Terminal State Riccati Penalty Matrix (8x8) [-] *)
    u_min                               : ARRAY[1..6] OF REAL;      (* Actuator Lower Box Saturation Bounds [various] *)
    u_max                               : ARRAY[1..6] OF REAL;      (* Actuator Upper Box Saturation Bounds [various] *)
    du_max                              : ARRAY[1..6] OF REAL;      (* Actuator Maximum Allowable Slew Rate Per Scan [various] *)

    (* MPC Receding-Horizon Rollout Arrays (Np = 5, Iterations = 6) *)
    x_rollout                           : ARRAY[1..5, 1..8] OF REAL;(* Predicted State Trajectory across Horizon [various] *)
    u_horizon                           : ARRAY[1..5, 1..6] OF REAL;(* Planned Manipulated Actuator Sequence [various] *)
    grad_J                              : ARRAY[1..6] OF REAL;      (* Projected Gradient Vector of Cost Functional J [various] *)
    rAlpha_pgd                          : REAL := 0.00085;          (* PGD Optimization Gradient Step Length [-] *)
    rCost_J                             : REAL;                     (* Cumulative Quadratic Objective Function Value [-] *)
    rDelta_u                            : REAL;                     (* Temporary Actuator Slew Rate Delta [various] *)

    (* 2oo3 TMR Voting Structures & Discrepancy Debounce Timers *)
    bHealthy_PT101A                     : BOOL := TRUE;             (* Channel A Health Flag PT-101 Nozzle Pressure [-] *)
    bHealthy_PT101B                     : BOOL := TRUE;             (* Channel B Health Flag PT-101 Nozzle Pressure [-] *)
    bHealthy_PT101C                     : BOOL := TRUE;             (* Channel C Health Flag PT-101 Nozzle Pressure [-] *)
    rTimer_PT101_AB_sec                 : REAL := 0.0;              (* Pairwise Discrepancy Timer PT-101 AB [s] *)
    rTimer_PT101_BC_sec                 : REAL := 0.0;              (* Pairwise Discrepancy Timer PT-101 BC [s] *)
    rTimer_PT101_CA_sec                 : REAL := 0.0;              (* Pairwise Discrepancy Timer PT-101 CA [s] *)
    bDiscrepancy_PT101                  : BOOL := FALSE;            (* Group Discrepancy Warning Flag PT-101 [-] *)
    bDegraded_PT101                     : BOOL := FALSE;            (* Degraded Single/Dual Sensor Mode Active PT-101 [-] *)
    rVoted_PT101_bar                    : REAL := 0.0;              (* 2oo3 Voted Filtered Value PT-101 [bar] *)
    rVoted_PT101_Prev                   : REAL := 0.0;              (* Previous Scan Voted Value PT-101 [bar] *)

    bHealthy_PT201A                     : BOOL := TRUE;             (* Channel A Health Flag PT-201 Cavity 1 Pressure [-] *)
    bHealthy_PT201B                     : BOOL := TRUE;             (* Channel B Health Flag PT-201 Cavity 1 Pressure [-] *)
    bHealthy_PT201C                     : BOOL := TRUE;             (* Channel C Health Flag PT-201 Cavity 1 Pressure [-] *)
    rTimer_PT201_AB_sec                 : REAL := 0.0;              (* Pairwise Discrepancy Timer PT-201 AB [s] *)
    rTimer_PT201_BC_sec                 : REAL := 0.0;              (* Pairwise Discrepancy Timer PT-201 BC [s] *)
    rTimer_PT201_CA_sec                 : REAL := 0.0;              (* Pairwise Discrepancy Timer PT-201 CA [s] *)
    bDiscrepancy_PT201                  : BOOL := FALSE;            (* Group Discrepancy Warning Flag PT-201 [-] *)
    bDegraded_PT201                     : BOOL := FALSE;            (* Degraded Single/Dual Sensor Mode Active PT-201 [-] *)
    rVoted_PT201_bar                    : REAL := 0.0;              (* 2oo3 Voted Filtered Value PT-201 [bar] *)
    rVoted_PT201_Prev                   : REAL := 0.0;              (* Previous Scan Voted Value PT-201 [bar] *)

    bHealthy_ST301A                     : BOOL := TRUE;             (* Channel A Health Flag ST-301 Screw Position [-] *)
    bHealthy_ST301B                     : BOOL := TRUE;             (* Channel B Health Flag ST-301 Screw Position [-] *)
    bHealthy_ST301C                     : BOOL := TRUE;             (* Channel C Health Flag ST-301 Screw Position [-] *)
    rTimer_ST301_AB_sec                 : REAL := 0.0;              (* Pairwise Discrepancy Timer ST-301 AB [s] *)
    rTimer_ST301_BC_sec                 : REAL := 0.0;              (* Pairwise Discrepancy Timer ST-301 BC [s] *)
    rTimer_ST301_CA_sec                 : REAL := 0.0;              (* Pairwise Discrepancy Timer ST-301 CA [s] *)
    bDiscrepancy_ST301                  : BOOL := FALSE;            (* Group Discrepancy Warning Flag ST-301 [-] *)
    bDegraded_ST301                     : BOOL := FALSE;            (* Degraded Single/Dual Sensor Mode Active ST-301 [-] *)
    rVoted_ST301_mm                     : REAL := 0.0;              (* 2oo3 Voted Filtered Value ST-301 [mm] *)
    rVoted_ST301_Prev                   : REAL := 0.0;              (* Previous Scan Voted Value ST-301 [mm] *)

    bHealthy_WT401A                     : BOOL := TRUE;             (* Channel A Health Flag WT-401 Tie-Bar Strain [-] *)
    bHealthy_WT401B                     : BOOL := TRUE;             (* Channel B Health Flag WT-401 Tie-Bar Strain [-] *)
    bHealthy_WT401C                     : BOOL := TRUE;             (* Channel C Health Flag WT-401 Tie-Bar Strain [-] *)
    rTimer_WT401_AB_sec                 : REAL := 0.0;              (* Pairwise Discrepancy Timer WT-401 AB [s] *)
    rTimer_WT401_BC_sec                 : REAL := 0.0;              (* Pairwise Discrepancy Timer WT-401 BC [s] *)
    rTimer_WT401_CA_sec                 : REAL := 0.0;              (* Pairwise Discrepancy Timer WT-401 CA [s] *)
    bDiscrepancy_WT401                  : BOOL := FALSE;            (* Group Discrepancy Warning Flag WT-401 [-] *)
    bDegraded_WT401                     : BOOL := FALSE;            (* Degraded Single/Dual Sensor Mode Active WT-401 [-] *)
    rVoted_WT401_kN                     : REAL := 0.0;              (* 2oo3 Voted Filtered Value WT-401 [kN] *)
    rVoted_WT401_Prev                   : REAL := 0.0;              (* Previous Scan Voted Value WT-401 [kN] *)

    bHealthy_TT501A                     : BOOL := TRUE;             (* Channel A Health Flag TT-501 Mold Temperature [-] *)
    bHealthy_TT501B                     : BOOL := TRUE;             (* Channel B Health Flag TT-501 Mold Temperature [-] *)
    bHealthy_TT501C                     : BOOL := TRUE;             (* Channel C Health Flag TT-501 Mold Temperature [-] *)
    rTimer_TT501_AB_sec                 : REAL := 0.0;              (* Pairwise Discrepancy Timer TT-501 AB [s] *)
    rTimer_TT501_BC_sec                 : REAL := 0.0;              (* Pairwise Discrepancy Timer TT-501 BC [s] *)
    rTimer_TT501_CA_sec                 : REAL := 0.0;              (* Pairwise Discrepancy Timer TT-501 CA [s] *)
    bDiscrepancy_TT501                  : BOOL := FALSE;            (* Group Discrepancy Warning Flag TT-501 [-] *)
    bDegraded_TT501                     : BOOL := FALSE;            (* Degraded Single/Dual Sensor Mode Active TT-501 [-] *)
    rVoted_TT501_degC                   : REAL := 120.0;            (* 2oo3 Voted Filtered Value TT-501 [deg C] *)
    rVoted_TT501_Prev                   : REAL := 120.0;            (* Previous Scan Voted Value TT-501 [deg C] *)

    rDiscrepancyThreshold_PT_Nozzle_bar : REAL := 35.0;             (* Pairwise Tolerance for Melt Pressure Cells [bar] *)
    rDiscrepancyThreshold_PT_Cavity_bar : REAL := 25.0;             (* Pairwise Tolerance for Quartz Piezo Sensors [bar] *)
    rDiscrepancyThreshold_ST_Screw_mm   : REAL := 0.35;             (* Pairwise Tolerance for Optical Linear Scales [mm] *)
    rDiscrepancyThreshold_WT_Tonnage_kN : REAL := 350.0;            (* Pairwise Tolerance for Tie-Bar Strain Washers [kN] *)
    rDiscrepancyThreshold_TT_Mold_degC  : REAL := 3.5;              (* Pairwise Tolerance for Mold Core Thermocouples [deg C] *)
    rTmrDebounceTimeLimit_sec           : REAL := 0.100;            (* Discrepancy Accumulation Debounce Time Limit [s] *)

    (* Cross-WLF Polymer Rheology & Physical Variables *)
    rPolymer_D1_Pas                     : REAL := 3.80e11;          (* Cross-WLF Zero-Shear Reference Viscosity D1 [Pa.s] *)
    rPolymer_D2_K                       : REAL := 418.15;           (* Cross-WLF Reference Temperature D2 [K] *)
    rPolymer_D3_KPa                     : REAL := 0.0;              (* Cross-WLF Pressure Sensitivity Constant D3 [K/Pa] *)
    rPolymer_A1                         : REAL := 28.50;            (* Cross-WLF WLF Free-Volume Parameter A1 [-] *)
    rPolymer_A2_prime_K                 : REAL := 51.60;            (* Cross-WLF WLF Free-Volume Parameter A2 [K] *)
    rPolymer_TauStar_Pa                 : REAL := 195000.0;         (* Cross-WLF Critical Shear Stress Tau* [Pa] *)
    rPolymer_PowerLaw_n                 : REAL := 0.31;             (* Cross-WLF Pseudoplastic Power-Law Index n [-] *)
    rScrewDiameter_m                    : REAL := 0.120;            (* Screw Barrel Outer Bore Diameter [m] *)
    rScrewArea_m2                       : REAL := 0.0113097;        (* Screw Cross-Sectional Area A_screw [m2] *)
    rNozzleRadius_m                     : REAL := 0.0040;           (* Injection Nozzle Tip Orifice Radius [m] *)
    rGateHalfThickness_um               : REAL := 1500.0;           (* Optical Lens Submarine Gate Half-Thickness [um] *)
    rThermalDiffusivity_m2s             : REAL := 1.15e-7;          (* Polycarbonate Thermal Diffusivity alpha [m2/s] *)
    rMoldStiffness_kNmm                 : REAL := 1850000.0;        (* Mold Base Machine Deflection Stiffness K_mold [kN/mm] *)
    rProjectedArea_m2                   : REAL := 0.285;            (* Total Multi-Cavity Projected Parting Area [m2] *)

    (* Real-Time Calculated Physics Variables *)
    rMeltTemp_Kelvin                    : REAL;                     (* Absolute Melt Temperature in Kelvin [K] *)
    rZeroShearViscosity_Pas             : REAL;                     (* Evaluated Zero-Shear Dynamic Viscosity eta_0 [Pa.s] *)
    rShearStressRatio                   : REAL;                     (* Ratio (eta_0 * gamma_dot) / tau_star [-] *)
    rMeltFlowRate_m3s                   : REAL;                     (* Instantaneous Melt Volumetric Flow Rate Q [m3/s] *)
    rCalculatedShearRate_s1             : REAL;                     (* Apparent Shear Rate gamma_dot [1/s] *)
    rCalculatedViscosity_Pas            : REAL;                     (* Apparent Non-Newtonian Dynamic Viscosity eta [Pa.s] *)
    rMeltTotalOpeningForce_kN           : REAL;                     (* Dynamic Cavity Melt Opening Force F_open [kN] *)
    rMoldSeparation_um                  : REAL;                     (* Mold Parting Line Physical Separation [um] *)
    rSkinGrowthRate_ums                 : REAL;                     (* Instantaneous Gate Skin Solidification Rate [um/s] *)
    rCalculatedScrewVelocity_mms        : REAL;                     (* Differentiated Linear Screw Velocity [mm/s] *)
    rPrevScrewPos_mm                    : REAL := 0.0;              (* Previous Scan Screw Position [mm] *)
    rPrevCavity1Press_bar               : REAL := 0.0;              (* Previous Scan Cavity 1 Pressure [bar] *)
    rRaw_dPCav_dt                       : REAL;                     (* Raw Numerical Derivative of Cavity Pressure [bar/s] *)
    rFiltered_dPCav_dt                  : REAL := 0.0;              (* Low-Pass Filtered Cavity Pressure Derivative [bar/s] *)
    rTieBar1_kN                         : REAL;                     (* Tie-Bar 1 Individual Load Strain [kN] *)
    rTieBar2_kN                         : REAL;                     (* Tie-Bar 2 Individual Load Strain [kN] *)
    rTieBar3_kN                         : REAL;                     (* Tie-Bar 3 Individual Load Strain [kN] *)
    rTieBar4_kN                         : REAL;                     (* Tie-Bar 4 Individual Load Strain [kN] *)
    rMaxTieBarDelta_kN                  : REAL;                     (* Maximum Measured Tie-Bar Load Imbalance [kN] *)

    (* Dynamic V/P Switchover Logic Variables *)
    bVP_Cond_Position                   : BOOL := FALSE;            (* V/P Trigger Condition: Linear Screw Stroke Reached [-] *)
    bVP_Cond_CavityPressure             : BOOL := FALSE;            (* V/P Trigger Condition: Cavity Quartz Pressure Peak [-] *)
    bVP_Cond_PressureDeriv              : BOOL := FALSE;            (* V/P Trigger Condition: Cavity Pressure Derivative [-] *)
    bVP_Cond_NozzleSpike                : BOOL := FALSE;            (* V/P Trigger Condition: Hydraulic Nozzle Pressure [-] *)
    bVP_Cond_Timeout                    : BOOL := FALSE;            (* V/P Trigger Condition: Watchdog Volumetric Fill [-] *)
    rSwitchoverScrewPos_mm              : REAL := 0.0;              (* Screw Position Captured Exactly at V/P Switch [mm] *)
    rSwitchoverPeakPress_bar            : REAL := 0.0;              (* Peak Nozzle Pressure Captured at V/P Switch [bar] *)
    rSwitchoverFillTime_sec             : REAL := 0.0;              (* Fill Duration Captured Exactly at V/P Switch [s] *)
    rSwitchoverCavityPress_bar          : REAL := 0.0;              (* Cavity Pressure Captured Exactly at V/P Switch [bar] *)

    (* Finite State Machine (FSM) Internal Variables *)
    nFsmState                           : DINT := 0;                (* Current Active Production FSM State [-] *)
    nFsmNextState                       : DINT := 0;                (* Next State Target for Transition Evaluation [-] *)
    sFsmStateName                       : STRING[40] := 'IDLE';     (* Human-Readable Text Name of Current State [-] *)
    bStateFirstScan                     : BOOL := TRUE;             (* One-Shot Pulse on State Entry [-] *)
    rStateElapsedTime_sec               : REAL := 0.0;              (* Elapsed Duration in Current State [s] *)
    rTotalCycleTimer_sec                : REAL := 0.0;              (* Total Machine Shot-to-Shot Cycle Stopwatch [s] *)
    rFillStageStopwatch_sec             : REAL := 0.0;              (* Dedicated Volumetric Fill Phase Stopwatch [s] *)
    rPackStageStopwatch_sec             : REAL := 0.0;              (* Dedicated Multi-Stage Packing Phase Stopwatch [s] *)
    rCoolingStopwatch_sec               : REAL := 0.0;              (* In-Mold Quench Cooling Phase Stopwatch [s] *)
    nHoldingProfileSubStage             : DINT := 1;                (* Active Sub-Stage Index of 5-Stage Packing Profile [-] *)
    rSubStageTimer_sec                  : REAL := 0.0;              (* Elapsed Duration in Current Holding Sub-Stage [s] *)
    nEjectorPulseCounter                : DINT := 0;                (* Multi-Pulse Ejection Cycle Accumulator [-] *)
    bEjectorStrokeForwardActive         : BOOL := FALSE;            (* Multi-Pin Ejector Stroke Forward Direction Latch [-] *)
    rPeakCavityPressHold_bar            : REAL := 0.0;              (* Maximum Cavity Pressure Memory Register [bar] *)
    rMinCushionHold_mm                  : REAL := 999.0;            (* Minimum Screw Cushion Memory Register [mm] *)

    (* ISA-18.2 Multi-Tier Process Alarm Limits & Deadbands *)
    rSp_NozzlePress_HH_bar              : REAL := 2200.0;           (* Nozzle Pressure High-High Emergency Safety Trip [bar] *)
    rSp_NozzlePress_H_bar               : REAL := 1950.0;           (* Nozzle Pressure High Warning Limit [bar] *)
    rSp_NozzlePress_H_Deadband_bar      : REAL := 50.0;             (* Nozzle Pressure High Warning Deadband [bar] *)
    rSp_CavityPress_HH_bar              : REAL := 1150.0;           (* Cavity Pressure High-High Tool Protection Trip [bar] *)
    rSp_CavityPress_H_bar               : REAL := 950.0;            (* Cavity Pressure High Warning Limit [bar] *)
    rSp_CavityPress_H_Deadband_bar      : REAL := 40.0;             (* Cavity Pressure High Warning Deadband [bar] *)
    rSp_Tonnage_HH_kN                   : REAL := 26500.0;          (* Clamping Unit Total Tonnage High-High Trip [kN] *)
    rSp_Tonnage_H_kN                    : REAL := 25500.0;          (* Clamping Unit Total Tonnage High Warning [kN] *)
    rSp_Tonnage_L_kN                    : REAL := 23000.0;          (* Clamping Unit Total Tonnage Low Warning [kN] *)
    rSp_Tonnage_LL_kN                   : REAL := 21000.0;          (* Clamping Unit Total Tonnage Low-Low Trip [kN] *)
    rSp_TieBarImbalance_HH_kN           : REAL := 650.0;            (* Tie-Bar Asymmetry High-High Emergency Trip [kN] *)
    rSp_TieBarImbalance_H_kN            : REAL := 400.0;            (* Tie-Bar Asymmetry High Warning Limit [kN] *)
    rSp_PartingSeparation_HH_um         : REAL := 15.0;             (* Mold Parting Line Separation Ultra-Fast Dump Trip [um] *)
    rSp_PartingSeparation_H_um          : REAL := 10.0;             (* Mold Parting Line Separation High Warning [um] *)
    rSp_MoldTemp_H_degC                 : REAL := 135.0;            (* Mold Tooling Temperature High Warning [deg C] *)
    rSp_MoldTemp_L_degC                 : REAL := 105.0;            (* Mold Tooling Temperature Low Warning [deg C] *)
    rSp_Cushion_L_mm                    : REAL := 6.0;              (* Minimum Screw Cushion Warning Limit [mm] *)
    rSp_Cushion_LL_mm                   : REAL := 2.5;              (* Minimum Screw Cushion Low-Low Trip Limit [mm] *)
    rSp_GateFreezeTimeout_sec           : REAL := 22.0;             (* Gate Freeze-Off Detection Maximum Watchdog [s] *)

    (* Alarm Status Latches & Bit Packing Registers *)
    bAlarmLatched_FlashTrip             : BOOL := FALSE;            (* Latched Mold Flash Parting Line Trip Flag [-] *)
    bAlarmLatched_TieBarTrip            : BOOL := FALSE;            (* Latched Tie-Bar Strain Imbalance Trip Flag [-] *)
    bAlarmLatched_NozzlePressHH         : BOOL := FALSE;            (* Latched Nozzle High-High Overpressure Trip Flag [-] *)
    bAlarmLatched_CavityPressHH         : BOOL := FALSE;            (* Latched Cavity High-High Overpressure Trip Flag [-] *)
    bAlarmLatched_ClampTonnageHH        : BOOL := FALSE;            (* Latched Clamping High-High Tonnage Trip Flag [-] *)
    bAlarmLatched_ClampTonnageLL        : BOOL := FALSE;            (* Latched Clamping Low-Low Tonnage Loss Trip Flag [-] *)
    bAlarmLatched_CushionLL             : BOOL := FALSE;            (* Latched Screw Bottoming Cushion Low-Low Trip [-] *)
    bAlarmLatched_FillTimeout           : BOOL := FALSE;            (* Latched Injection Fill Timeout Watchdog Trip [-] *)
    bAlarmLatched_MoldProtectTrip       : BOOL := FALSE;            (* Latched Mold Protect Low-Pressure Obstruction Trip [-] *)

    bAlarmWarn_NozzlePressH             : BOOL := FALSE;            (* Active Nozzle Pressure High Warning [-] *)
    bAlarmWarn_CavityPressH             : BOOL := FALSE;            (* Active Cavity Pressure High Warning [-] *)
    bAlarmWarn_TieBarImbalanceH         : BOOL := FALSE;            (* Active Tie-Bar Asymmetry High Warning [-] *)
    bAlarmWarn_PartingSeparationH       : BOOL := FALSE;            (* Active Mold Separation High Warning [-] *)
    bAlarmWarn_MoldTempH                : BOOL := FALSE;            (* Active Mold Temperature High Warning [-] *)
    bAlarmWarn_MoldTempL                : BOOL := FALSE;            (* Active Mold Temperature Low Warning [-] *)
    bAlarmWarn_CushionL                 : BOOL := FALSE;            (* Active Screw Cushion Low Warning [-] *)
    bAlarmWarn_GateFreezeDelay          : BOOL := FALSE;            (* Active Gate Freeze-Off Delay Warning [-] *)

    (* Internal First-Out Diagnostic Memory *)
    nFirstOutAlarmCode                  : DINT := 0                 (* First-Out Failure Reason Code Register [-] *)
END_VAR
"""

if __name__ == "__main__":
    print("Writing builder script modules...")
