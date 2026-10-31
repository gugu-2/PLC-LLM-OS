# build_stamping_dataset.py
# High-Performance IEC 61131-3 Structured Text Synthesizer for 4,000-Ton Automotive Transfer Stamping Press
import json
import os
import sys
import re

def generate_iec_code():
    out = []
    
    # ----------------------------------------------------------------------------------
    # HEADER
    # ----------------------------------------------------------------------------------
    out.append("FUNCTION_BLOCK FB_StampingPress_4000Ton_TransferGantry_DieCushion\n(*\n" +
""" ====================================================================================================
  PROJECT:       COMMERCIAL AUTOMOTIVE METAL STAMPING & BODY-IN-WHITE (BIW) MANUFACTURING LINE
  MODULE:        FB_StampingPress_4000Ton_TransferGantry_DieCushion
  DISCIPLINE:    CYBER-PHYSICAL ADVANCED AUTOMATION / HEAVY METAL FORMING / MULTI-AXIS GANTRY TRANSFER
  STANDARDS:     DIN EN 16092-1 / -2 / -3 (SAFETY OF MACHINE TOOLS - MECHANICAL & HYDRAULIC PRESSES),
                 ISO 13849-1 (SAFETY-RELATED PARTS OF CONTROL SYSTEMS - PL e / CATEGORY 4),
                 IEC 61508 (FUNCTIONAL SAFETY OF ELECTRICAL / ELECTRONIC / PROGRAMMABLE SYSTEMS - SIL 3),
                 VDI 3140 / VDI 3388 (SHEET METAL FORMING TOOLS & PRESS DYNAMICS),
                 ISA-18.2 (MANAGEMENT OF ALARM SYSTEMS FOR THE PROCESS & AUTOMATION INDUSTRIES),
                 IEC 61800-5-2 (ADJUSTABLE SPEED ELECTRICAL POWER DRIVE SYSTEMS - FUNCTIONAL SAFETY).
  AUTHOR:        LUMINA AI CLOUD SWARM - PRINCIPAL AUTOMATION FELLOW & CPS CHAIR (V7 MAX)
  MACHINE CLASS: 4,000 METRIC TON (40,000 kN) MULTI-STATION PROGRESSIVE/TRANSFER STAMPING PRESS
  ACTUATION:     DUAL DIRECT-DRIVE 1,500 kW SYNCHRONOUS TORQUE MOTORS WITH TWIN ECCENTRIC GEAR TRAINS,
                 8-POINT HYDROSTATIC GIB SLIDE GUIDING WITH DYNAMIC OIL FILM GAP MONITORING,
                 8-POINT MULTI-CYLINDER CLOSED-LOOP HYDRAULIC DIE CUSHION (8,000 kN TOTAL HOLDING FORCE),
                 4 DYNAMIC HYDRAULIC TILT-LEVELING CYLINDERS IN BED CORNERS FOR ECCENTRICITY BALANCING,
                 7-AXIS HIGH-SPEED TRI-AXIS TRANSFER GANTRY (X: FEED 2.5 m/s, Y: CLAMP, Z: LIFT 15 m/s^2),
                 HIGH-SPEED DESTACKER BLANK FEEDER WITH DUAL AIR-KNIFE FANNING & 20 ms DOUBLE-BLANK DIVERT,
                 IN-LINE REAL-TIME MULTI-CAMERA OPTICAL PHOTOGRAMMETRY FOR DRAW DEPTH & FLANGE WRINKLING.
  SCAN PERIOD:   T_s = 0.002 s (2 MILLISECONDS DETERMINISTIC REAL-TIME SAFETY & MOTION SCAN CYCLE)
 ----------------------------------------------------------------------------------------------------
  CYBER-PHYSICAL ARCHITECTURAL ARCHITECTURE & MATHEMATICAL FORMULATIONS:
   1. Triple Modular Redundancy (2oo3 TMR) Voting & Discrepancy Fault Integration:
      Performs real-time median voting, spread delta computation, and cumulative discrepancy timing across:
      - Press Main Crank Angle Resolvers (Resolvers 1, 2, 3) [deg]
      - 4-Corner Tie-Rod & Upright Strain Gauge Load Cells (FL, FR, RL, RR - Channels A, B, C) [kN]
      - Multi-Point Hydraulic Die Cushion Manifold Pressure Transmitters (Transmitters A, B, C) [bar]
      - Destacker Laser Sheet Thickness Displacement Transducers (Sensors A, B, C) [mm]
      - Redundant Optical Safety Light Curtain Channels with Hardware Muting & Bumpless Degradation.
   2. Discrete Cyber-Physical State-Space Dynamics (16x16 A_d, 16x8 B_d, 8x16 C_d, 8x8 D_d):
      Models high-order electro-mechanical-hydraulic coupling discretized at T_s = 2.0 ms:
      - x1:  Press slide vertical displacement deviation Delta_z_ram [mm]
      - x2:  Press slide vertical velocity Delta_v_ram [mm/s]
      - x3:  Press structural upright frame strain Delta_epsilon_frame [um/m]
      - x4:  Press upright structural strain rate Delta_dot_epsilon [um/m/s]
      - x5:  Slide tilting pitch angle deviation Delta_theta_pitch [mrad]
      - x6:  Slide tilting roll angle deviation Delta_theta_roll [mrad]
      - x7:  Slide tilting pitch angular velocity Delta_omega_pitch [mrad/s]
      - x8:  Slide tilting roll angular velocity Delta_omega_roll [mrad/s]
      - x9:  Hydraulic die cushion blankholder vertical position Delta_z_cush [mm]
      - x10: Die cushion main hydraulic manifold pressure deviation Delta_P_cush [bar]
      - x11: Die cushion hydraulic fluid compressibility rate Delta_dot_P_cush [bar/s]
      - x12: Transfer gantry feed carriage linear position error Delta_x_gantry [mm]
      - x13: Transfer gantry feed carriage linear velocity Delta_v_gantry [mm/s]
      - x14: Transfer gantry tooling rail 1st structural bending vibration deflection Delta_xi_vibe [mm]
      - x15: Transfer gantry structural vibration velocity Delta_dot_xi_vibe [mm/s]
      - x16: Sheet metal dynamic plastic drawing resistance force perturbation Delta_F_metal [kN]
      Driven by 8 physical control inputs:
      - u1: Dual torque motor master torque reference [kN m]
      - u2: Front-Left (FL) hydraulic dynamic tilt leveling cylinder flow demand [L/min]
      - u3: Front-Right (FR) hydraulic dynamic tilt leveling cylinder flow demand [L/min]
      - u4: Rear-Left (RL) hydraulic dynamic tilt leveling cylinder flow demand [L/min]
      - u5: Rear-Right (RR) hydraulic dynamic tilt leveling cylinder flow demand [L/min]
      - u6: Die cushion proportional servo valve spool flow command [mA]
      - u7: Tri-axis transfer gantry feed carriage X-axis servo torque demand [N m]
      - u8: Tri-axis transfer gantry lift Z-axis servo torque demand [N m]
   3. Receding-Horizon Model Predictive Control (MPC) Quadratic Optimization:
      Formulates an online QP cost functional:
        J = sum_{k=1..Np} [ (x_k - x_ref)' * Q * (x_k - x_ref) + u_k' * R * u_k + Delta_u_k' * R_d * Delta_u_k ]
      Computes analytical gradients grad_J = B_d' * Q * (x_pred - x_ref) + R * u_prev + R_d * Delta_u
      and diagonal Hessian components to execute constrained projected gradient descent with box limits.
   4. Real-Time 4-Corner Center-of-Loading & Dynamic Hydrostatic Tilt Leveling:
      Calculates real-time center of pressure (X_c, Y_c) and eccentric tilting moments (M_x, M_y) from
      the 4-corner load cell array:
        F_total = F_FL + F_FR + F_RL + F_RR
        X_c = [ (F_FR + F_RR) - (F_FL + F_RL) ] / F_total * (W_bed / 2.0)
        Y_c = [ (F_FL + F_FR) - (F_RL + F_RR) ] / F_total * (L_bed / 2.0)
        M_x = F_total * (Y_c / 1000.0) [kN m],  M_y = F_total * (X_c / 1000.0) [kN m]
      Injects closed-loop hydraulic counter-pressure commands into the 4 bed leveling cylinders to cancel
      slide tipping, preventing severe gib scuffing and die guide pillar galling.
   5. 8-Point Multi-Cylinder Hydraulic Die Cushion Profiling & Pre-Acceleration:
      Pre-accelerates cushion cylinders 1..8 upwards prior to punch contact (theta = 110 deg to 125 deg)
      to match instantaneous slide downward velocity v_ram(theta), eliminating impact tonnage shock.
      Executes independent closed-loop servo valve PID profiling during deep draw (theta = 125 deg to 180 deg)
      and provides delayed breakaway cushion lift (theta = 195 deg to 230 deg) preventing vacuum distortion.
   6. High-Speed 7-Axis Tri-Axis Transfer Gantry Electronic Cam (E-Cam) Synchronization:
      Synchronizes transfer gantry Feed X, Clamp Y, and Lift Z axes to virtual master crank angle theta
      using quintic polynomial (5th-order) S-curves. Computes dynamic 3D collision envelope boundaries
      between slide tooling and transfer gripper fingers with hardware-latched SIL-3 interlocks.
   7. Destacker Blank Feeder, Double-Blank Laser Gauging & In-Line Photogrammetry Quality Metrics:
      Coordinates magnetic fanning air-knives, evaluates laser thickness gauge (rejecting double blanks
      > 1.25x t_nom within 20 ms via pneumatic divert gate), and analyzes high-speed photogrammetry
      data (draw depth, flange wrinkle wave amplitude, thinning percentage, split detection).
   8. 12-Stage Operational Finite State Machine (FSM):
      Sequences the complete press cycle from blank pickup to panel egress with sub-millisecond precision.
   9. ISA-18.2 Multi-Tiered Alarm Matrix & Diagnostics Telemetry:
      Categorizes faults into High-High (HH), High (H), Low (L), Low-Low (LL) tiers with deadband hysteresis,
      fail-safe hydraulic overload dump valve tripping, and telemetry bit-packing.
 ====================================================================================================
*)\n""")

    # ----------------------------------------------------------------------------------
    # VAR_INPUT
    # ----------------------------------------------------------------------------------
    out.append("""VAR_INPUT
    (* ===================================================================================== *)
    (* 1.0 SYSTEM MASTER SAFETY & OPERATIONAL DISPATCH COMMANDS                              *)
    (* ===================================================================================== *)
    bEnableMasterSafetyPermissive       : BOOL := FALSE;    (* Master Supervisory Safety Permissive [Active HIGH] *)
    bHardwiredEStopRelayHealthy         : BOOL := TRUE;     (* Dual-Channel Hardwired SIL-3 E-Stop Relay Circuit [Active HIGH] *)
    bSafetyCurtainDieAreaUnbroken_ChA   : BOOL := TRUE;     (* Primary Optical Light Curtain Die Access Area Channel A *)
    bSafetyCurtainDieAreaUnbroken_ChB   : BOOL := TRUE;     (* Primary Optical Light Curtain Die Access Area Channel B *)
    bSafetyCurtainDestackerClear        : BOOL := TRUE;     (* Destacker Loading Zone Optical Muted Safety Barrier *)
    bHydraulicPowerUnitRunning          : BOOL := TRUE;     (* Main Hydraulic HPU Pump Motors Running & Pressure Charged *)
    bHydrostaticGibLubePressureOK       : BOOL := TRUE;     (* 8-Point Hydrostatic Gib Guide Oil Pressure Switch (Min 180 bar) *)
    bClutchBrakeAirPressureOK           : BOOL := TRUE;     (* Pneumatic Dual Safety Valve Supply Air Pressure (Min 5.5 bar) *)
    bDieClampHydraulicPressureOK        : BOOL := TRUE;     (* Upper & Lower Die Hydraulic Clamping System Pressure (Min 250 bar) *)
    bMasterAlarmAcknowledge             : BOOL := FALSE;    (* Operator Master Alarm Acknowledgement & Trip Reset Pushbutton *)
    bAutoCycleStartCommand              : BOOL := FALSE;    (* Operator Two-Hand Console / Supervisory Auto Cycle Start Command *)
    bSingleStrokeInchMode               : BOOL := FALSE;    (* Manual Maintenance Inching / Single-Stroke Setup Mode Select *)
    bDieToolingID_Verified              : BOOL := TRUE;     (* RFID Electronic Tool Identification Verified & Recipe Locked *)
    iActiveDieRecipeID                  : DINT := 101;      (* Active Stamping Die Recipe Identification Index *)
    rNominalPressSpeed_SPM              : REAL := 25.0;     (* Target Continuous Production Press Cadence [strokes/min] *)
    rNominalBlankThickness_mm           : REAL := 1.20;     (* Nominal Body Panel Sheet Metal Thickness [mm] *)
    rMaxAllowableTonnage_kN             : REAL := 40000.0;  (* Rated Stamping Press Structural Tonnage Capacity [kN] *)
    rTargetDrawDepth_mm                 : REAL := 185.0;    (* Target Automotive Body Side Panel Draw Forming Depth [mm] *)

    (* ===================================================================================== *)
    (* 2.0 TRIPLE MODULAR REDUNDANCY (2oo3) DESTACKER LASER THICKNESS DISPLACEMENT SENSORS  *)
    (* High-frequency laser triangulation sensors measuring incoming sheet blank thickness   *)
    (* ===================================================================================== *)
    rDestackerLaserThickness_ChA        : REAL := 1.20;     (* Destacker Optical Laser Thickness Sensor Channel A [mm] *)
    rDestackerLaserThickness_ChB        : REAL := 1.20;     (* Destacker Optical Laser Thickness Sensor Channel B [mm] *)
    rDestackerLaserThickness_ChC        : REAL := 1.20;     (* Destacker Optical Laser Thickness Sensor Channel C [mm] *)

    (* ===================================================================================== *)
    (* 3.0 TRIPLE MODULAR REDUNDANCY (2oo3) PRESS CRANK ANGLE ABSOLUTE ENCODERS / RESOLVERS  *)
    (* Heavy-duty multi-turn resolver transducers mounted directly to main eccentric shafts  *)
    (* ===================================================================================== *)
    rPressCrankAngle_Resolver_ChA       : REAL := 0.0;      (* Press Eccentric Crank Angle Resolver Channel A [deg] *)
    rPressCrankAngle_Resolver_ChB       : REAL := 0.0;      (* Press Eccentric Crank Angle Resolver Channel B [deg] *)
    rPressCrankAngle_Resolver_ChC       : REAL := 0.0;      (* Press Eccentric Crank Angle Resolver Channel C [deg] *)
    rPressSlidePosition_Scale_mm        : REAL := 800.0;    (* Linear Optical Scale Absolute Slide Displacement [mm] *)

    (* ===================================================================================== *)
    (* 4.0 TRIPLE MODULAR REDUNDANCY (2oo3) 4-CORNER TIE-ROD STRAIN GAUGE LOAD CELLS         *)
    (* Full-bridge piezoresistive strain load cells bonded to the 4 press structural columns *)
    (* ===================================================================================== *)
    rTonnage_FL_ChA                     : REAL := 0.0;      (* Front-Left Structural Column Tonnage Load Cell Channel A [kN] *)
    rTonnage_FL_ChB                     : REAL := 0.0;      (* Front-Left Structural Column Tonnage Load Cell Channel B [kN] *)
    rTonnage_FL_ChC                     : REAL := 0.0;      (* Front-Left Structural Column Tonnage Load Cell Channel C [kN] *)
    rTonnage_FR_ChA                     : REAL := 0.0;      (* Front-Right Structural Column Tonnage Load Cell Channel A [kN] *)
    rTonnage_FR_ChB                     : REAL := 0.0;      (* Front-Right Structural Column Tonnage Load Cell Channel B [kN] *)
    rTonnage_FR_ChC                     : REAL := 0.0;      (* Front-Right Structural Column Tonnage Load Cell Channel C [kN] *)
    rTonnage_RL_ChA                     : REAL := 0.0;      (* Rear-Left Structural Column Tonnage Load Cell Channel A [kN] *)
    rTonnage_RL_ChB                     : REAL := 0.0;      (* Rear-Left Structural Column Tonnage Load Cell Channel B [kN] *)
    rTonnage_RL_ChC                     : REAL := 0.0;      (* Rear-Left Structural Column Tonnage Load Cell Channel C [kN] *)
    rTonnage_RR_ChA                     : REAL := 0.0;      (* Rear-Right Structural Column Tonnage Load Cell Channel A [kN] *)
    rTonnage_RR_ChB                     : REAL := 0.0;      (* Rear-Right Structural Column Tonnage Load Cell Channel B [kN] *)
    rTonnage_RR_ChC                     : REAL := 0.0;      (* Rear-Right Structural Column Tonnage Load Cell Channel C [kN] *)

    (* ===================================================================================== *)
    (* 5.0 TRIPLE MODULAR REDUNDANCY (2oo3) HYDRAULIC DIE CUSHION PRESSURE TRANSMITTERS      *)
    (* Piezoresistive high-response pressure sensors on the master die cushion accumulator   *)
    (* ===================================================================================== *)
    rCushionManifoldPressure_ChA        : REAL := 210.0;    (* Die Cushion Common Hydraulic Manifold Pressure Ch A [bar] *)
    rCushionManifoldPressure_ChB        : REAL := 210.0;    (* Die Cushion Common Hydraulic Manifold Pressure Ch B [bar] *)
    rCushionManifoldPressure_ChC        : REAL := 210.0;    (* Die Cushion Common Hydraulic Manifold Pressure Ch C [bar] *)

    (* ===================================================================================== *)
    (* 6.0 8-POINT MULTI-CYLINDER DIE CUSHION DISPLACEMENT & CHAMBER PRESSURE FEEDBACKS      *)
    (* Magnetostrictive linear position transducers and chamber pressure transmitters         *)
    (* ===================================================================================== *)
    rCushionCyl_Pos_mm_1                : REAL := 250.0;    (* Hydraulic Die Cushion Cylinder 1 Piston Displacement [mm] *)
    rCushionCyl_Pos_mm_2                : REAL := 250.0;    (* Hydraulic Die Cushion Cylinder 2 Piston Displacement [mm] *)
    rCushionCyl_Pos_mm_3                : REAL := 250.0;    (* Hydraulic Die Cushion Cylinder 3 Piston Displacement [mm] *)
    rCushionCyl_Pos_mm_4                : REAL := 250.0;    (* Hydraulic Die Cushion Cylinder 4 Piston Displacement [mm] *)
    rCushionCyl_Pos_mm_5                : REAL := 250.0;    (* Hydraulic Die Cushion Cylinder 5 Piston Displacement [mm] *)
    rCushionCyl_Pos_mm_6                : REAL := 250.0;    (* Hydraulic Die Cushion Cylinder 6 Piston Displacement [mm] *)
    rCushionCyl_Pos_mm_7                : REAL := 250.0;    (* Hydraulic Die Cushion Cylinder 7 Piston Displacement [mm] *)
    rCushionCyl_Pos_mm_8                : REAL := 250.0;    (* Hydraulic Die Cushion Cylinder 8 Piston Displacement [mm] *)

    rCushionCyl_Press_bar_1             : REAL := 180.0;    (* Hydraulic Die Cushion Cylinder 1 Working Chamber Pressure [bar] *)
    rCushionCyl_Press_bar_2             : REAL := 180.0;    (* Hydraulic Die Cushion Cylinder 2 Working Chamber Pressure [bar] *)
    rCushionCyl_Press_bar_3             : REAL := 180.0;    (* Hydraulic Die Cushion Cylinder 3 Working Chamber Pressure [bar] *)
    rCushionCyl_Press_bar_4             : REAL := 180.0;    (* Hydraulic Die Cushion Cylinder 4 Working Chamber Pressure [bar] *)
    rCushionCyl_Press_bar_5             : REAL := 180.0;    (* Hydraulic Die Cushion Cylinder 5 Working Chamber Pressure [bar] *)
    rCushionCyl_Press_bar_6             : REAL := 180.0;    (* Hydraulic Die Cushion Cylinder 6 Working Chamber Pressure [bar] *)
    rCushionCyl_Press_bar_7             : REAL := 180.0;    (* Hydraulic Die Cushion Cylinder 7 Working Chamber Pressure [bar] *)
    rCushionCyl_Press_bar_8             : REAL := 180.0;    (* Hydraulic Die Cushion Cylinder 8 Working Chamber Pressure [bar] *)

    (* ===================================================================================== *)
    (* 7.0 7-AXIS TRI-AXIS TRANSFER GANTRY ACTUAL FEEDBACKS                                  *)
    (* High-resolution optical absolute encoders for gantry transfer coordinate positions    *)
    (* ===================================================================================== *)
    rTransferAxisX_ActualPos_mm         : REAL := 0.0;      (* Transfer Gantry Feed Axis X Carriage Actual Position [mm] *)
    rTransferAxisY_ActualPos_mm         : REAL := 0.0;      (* Transfer Gantry Clamp Axis Y Tooling Actual Position [mm] *)
    rTransferAxisZ_ActualPos_mm         : REAL := 0.0;      (* Transfer Gantry Lift Axis Z Carriage Actual Position [mm] *)
    rTransferAxisX_ActualVel_m_s        : REAL := 0.0;      (* Transfer Gantry Feed Axis X Carriage Velocity [m/s] *)

    (* ===================================================================================== *)
    (* 8.0 IN-LINE REAL-TIME OPTICAL PHOTOGRAMMETRY & VISION INSPECTION SIGNALS              *)
    (* High-speed stereoscopic cameras capturing stamped panel geometry at Die Station 6     *)
    (* ===================================================================================== *)
    rPhotogrammetry_DrawDepth_mm        : REAL := 185.0;    (* Measured Stamped Panel Draw Forming Depth [mm] *)
    rPhotogrammetry_WrinkleAmplitude_mm : REAL := 0.04;     (* Measured Flange Surface Wrinkling Amplitude [mm] *)
    rPhotogrammetry_ThinningPct         : REAL := 14.5;     (* Measured Critical Corner Sheet Thinning Percentage [%] *)
    bPhotogrammetry_SplitDetected       : BOOL := FALSE;    (* Machine Vision Sheet Edge Crack / Necking Split Detected *)

    (* ===================================================================================== *)
    (* 9.0 DUAL TORQUE MOTOR DRIVE TELEMETRY & BEARING THERMAL MONITORING                    *)
    (* Inverter drive actual current, active power, and mechanical bearing thermistors       *)
    (* ===================================================================================== *)
    rTorqueMotor1_Current_Arms          : REAL := 220.0;    (* Direct-Drive Torque Motor 1 Stator RMS Current [A] *)
    rTorqueMotor2_Current_Arms          : REAL := 222.0;    (* Direct-Drive Torque Motor 2 Stator RMS Current [A] *)
    rTorqueMotor1_Power_kW              : REAL := 450.0;    (* Direct-Drive Torque Motor 1 Active Electrical Power [kW] *)
    rTorqueMotor2_Power_kW              : REAL := 454.0;    (* Direct-Drive Torque Motor 2 Active Electrical Power [kW] *)
    rTorqueMotor_BearingTemp_degC       : REAL := 52.4      (* Direct-Drive Torque Motor Main Bearing Temperature [deg C] *)
END_VAR
""")

    # ----------------------------------------------------------------------------------
    # VAR_OUTPUT
    # ----------------------------------------------------------------------------------
    out.append("""VAR_OUTPUT
    (* ===================================================================================== *)
    (* 1.0 SYSTEM MASTER SAFETY STATUS & MAIN DRIVE COMMANDS                                 *)
    (* ===================================================================================== *)
    bSystemReadyForAutoCycle            : BOOL := FALSE;    (* Press Automation System Ready for Automatic Cadence *)
    bPressInContinuousStamping          : BOOL := FALSE;    (* Press Slide Cycling in Continuous Multi-Station Cadence *)
    bClutchEngaged_Command              : BOOL := FALSE;    (* Pneumatic Safety Dual Valve Clutch Engagement Command *)
    bBrakeRelease_Command               : BOOL := FALSE;    (* Pneumatic Safety Dual Valve Mechanical Brake Release Command *)
    bEmergencyOverloadDump_Active       : BOOL := FALSE;    (* Fast-Acting Hydraulic Overload Protection (HOLP) Dump Active *)
    bDualTorqueMotorEnable              : BOOL := FALSE;    (* Dual Direct-Drive Torque Motor Inverter Infeed Enable Command *)
    rTorqueMotor1_SpeedDemand_rpm       : REAL := 0.0;      (* Direct-Drive Torque Motor 1 Angular Speed Demand [rpm] *)
    rTorqueMotor2_SpeedDemand_rpm       : REAL := 0.0;      (* Direct-Drive Torque Motor 2 Angular Speed Demand [rpm] *)
    rTorqueMotor1_TorqueLimit_Nm        : REAL := 0.0;      (* Direct-Drive Torque Motor 1 Dynamic Torque Limit [N m] *)
    rTorqueMotor2_TorqueLimit_Nm        : REAL := 0.0;      (* Direct-Drive Torque Motor 2 Dynamic Torque Limit [N m] *)
    rPressSlideVelocity_mm_s            : REAL := 0.0;      (* Real-Time Calculated Press Slide Vertical Velocity [mm/s] *)

    (* ===================================================================================== *)
    (* 2.0 TONNAGE MONITORING & 4-CORNER ECCENTRICITY BALANCING COMMANDS                     *)
    (* ===================================================================================== *)
    rTotalMeasuredTonnage_kN            : REAL := 0.0;      (* Instantaneous Total Measured Stamping Force [kN] *)
    rEccentricityMoment_Mx_kNm          : REAL := 0.0;      (* Calculated Pitch Eccentricity Moment (Front/Rear Tilt) [kN m] *)
    rEccentricityMoment_My_kNm          : REAL := 0.0;      (* Calculated Roll Eccentricity Moment (Left/Right Tilt) [kN m] *)
    rSlideCenterOfLoading_X_mm          : REAL := 0.0;      (* Center of Loading Shift Along Transverse Bed Axis X [mm] *)
    rSlideCenterOfLoading_Y_mm          : REAL := 0.0;      (* Center of Loading Shift Along Longitudinal Bed Axis Y [mm] *)
    rTiltLevelingCyl_Pressure_Cmd_FL_bar: REAL := 150.0;    (* Front-Left Dynamic Bed Tilt Leveling Pressure Demand [bar] *)
    rTiltLevelingCyl_Pressure_Cmd_FR_bar: REAL := 150.0;    (* Front-Right Dynamic Bed Tilt Leveling Pressure Demand [bar] *)
    rTiltLevelingCyl_Pressure_Cmd_RL_bar: REAL := 150.0;    (* Rear-Left Dynamic Bed Tilt Leveling Pressure Demand [bar] *)
    rTiltLevelingCyl_Pressure_Cmd_RR_bar: REAL := 150.0;    (* Rear-Right Dynamic Bed Tilt Leveling Pressure Demand [bar] *)

    (* ===================================================================================== *)
    (* 3.0 8-POINT HYDRAULIC DIE CUSHION PROPORTIONAL SERVO COMMANDS                         *)
    (* ===================================================================================== *)
    rCushionServoValve_Cmd_mA_1         : REAL := 0.0;      (* Die Cushion Cylinder 1 Proportional Servo Valve Demand [mA] *)
    rCushionServoValve_Cmd_mA_2         : REAL := 0.0;      (* Die Cushion Cylinder 2 Proportional Servo Valve Demand [mA] *)
    rCushionServoValve_Cmd_mA_3         : REAL := 0.0;      (* Die Cushion Cylinder 3 Proportional Servo Valve Demand [mA] *)
    rCushionServoValve_Cmd_mA_4         : REAL := 0.0;      (* Die Cushion Cylinder 4 Proportional Servo Valve Demand [mA] *)
    rCushionServoValve_Cmd_mA_5         : REAL := 0.0;      (* Die Cushion Cylinder 5 Proportional Servo Valve Demand [mA] *)
    rCushionServoValve_Cmd_mA_6         : REAL := 0.0;      (* Die Cushion Cylinder 6 Proportional Servo Valve Demand [mA] *)
    rCushionServoValve_Cmd_mA_7         : REAL := 0.0;      (* Die Cushion Cylinder 7 Proportional Servo Valve Demand [mA] *)
    rCushionServoValve_Cmd_mA_8         : REAL := 0.0;      (* Die Cushion Cylinder 8 Proportional Servo Valve Demand [mA] *)
    rTotalCushionHoldingForce_kN        : REAL := 0.0;      (* Total Instantaneous Hydraulic Blankholder Holding Force [kN] *)
    rCushionTargetForce_Current_kN      : REAL := 0.0;      (* Active Recipe Blankholder Target Force Setpoint [kN] *)

    (* ===================================================================================== *)
    (* 4.0 7-AXIS TRI-AXIS TRANSFER GANTRY MOTION & TOOLING COMMANDS                         *)
    (* ===================================================================================== *)
    rTransferAxisX_PosCommand_mm        : REAL := 0.0;      (* Transfer Gantry Feed Axis X Interpolated Target Position [mm] *)
    rTransferAxisY_PosCommand_mm        : REAL := 0.0;      (* Transfer Gantry Clamp Axis Y Interpolated Target Position [mm] *)
    rTransferAxisZ_PosCommand_mm        : REAL := 0.0;      (* Transfer Gantry Lift Axis Z Interpolated Target Position [mm] *)
    rTransferAxisX_VelDemand_m_s        : REAL := 0.0;      (* Transfer Gantry Feed Axis X Instantaneous Velocity Demand [m/s] *)
    bTransferGripperVacuumEngage        : BOOL := FALSE;    (* Pneumatic Venturi Vacuum Cups Engage Command for Grippers *)

    (* ===================================================================================== *)
    (* 5.0 DESTACKER, BLANK CENTERING, LUBRICATION & QUALITY EGRESS COMMANDS                 *)
    (* ===================================================================================== *)
    bDestackerFanningAirBlast           : BOOL := FALSE;    (* Destacker Solenoid Pulse for Magnetic Sheet Fanning Air Knife *)
    bDestackerVacuumCupLift             : BOOL := FALSE;    (* Destacker Overhead Robot Vacuum Pick Cup Arm Lift Solenoid *)
    bDoubleBlankRejectGateDivert        : BOOL := FALSE;    (* High-Speed Pneumatic Diverter Gate for Double Blank Rejection *)
    bBlankCenteringActuatorAdvance      : BOOL := FALSE;    (* Servo-Pneumatic Blank Centering Squaring Table Clamp Command *)
    bDieLubricantSprayPulse             : BOOL := FALSE;    (* Electrostatic Die Cavity Micro-Lubricant Atomizer Spray Pulse *)
    bPartInspectionPassStatus           : BOOL := TRUE;     (* Station 6 Vision Photogrammetry Quality Dimensional PASS *)
    bStampedPanelEgressConveyorRun      : BOOL := FALSE;    (* Finished Body Panel Egress Shuttle Conveyor Drive Run Command *)

    (* ===================================================================================== *)
    (* 6.0 OPERATIONAL STATE & ISA-18.2 MULTI-TIERED ALARM STATUS WORDS                      *)
    (* ===================================================================================== *)
    iOperationalState                   : DINT := 10;       (* Current Discrete FSM Execution State Index [10..120, 999] *)
    dwISA_AlarmWord_HighHigh            : DWORD := 16#00000000; (* ISA-18.2 Priority 1 (High-High) Critical Emergency Trip Word *)
    dwISA_AlarmWord_High                : DWORD := 16#00000000; (* ISA-18.2 Priority 2 (High) Production Warning Word *)
    dwISA_AlarmWord_Interlock           : DWORD := 16#00000000; (* ISA-18.2 Hardware Safety & Process Permissive Interlock Word *)
    dwISA_AlarmWord_Diagnostic          : DWORD := 16#00000000  (* ISA-18.2 Sensor TMR Discrepancy & Health Diagnostic Word *)
END_VAR
""")

    # ----------------------------------------------------------------------------------
    # VAR
    # ----------------------------------------------------------------------------------
    out.append("""VAR
    (* ===================================================================================== *)
    (* 1.0 DISCRETE CYBER-PHYSICAL STATE-SPACE MATRICES & VECTORS (16 STATES, 8 CONTROLS)   *)
    (* Discretized continuous-time press dynamics at sample period T_s = 0.002 s (2.0 ms)    *)
    (* ===================================================================================== *)
    bInitStateSpaceDone                 : BOOL := FALSE;    (* Flag Indicating State-Space Coefficients Initialization *)
    Ad                                  : ARRAY[1..16, 1..16] OF REAL; (* Discrete Plant System State Transition Matrix *)
    Bd                                  : ARRAY[1..16, 1..8] OF REAL;  (* Discrete Plant Input Coupling Matrix *)
    Cd                                  : ARRAY[1..8, 1..16] OF REAL;  (* Discrete Plant Output Measurement Matrix *)
    Dd                                  : ARRAY[1..8, 1..8] OF REAL;   (* Discrete Plant Direct Feedthrough Matrix *)
    x_state                             : ARRAY[1..16] OF REAL; (* Instantaneous Cyber-Physical State Vector *)
    x_pred                              : ARRAY[1..16] OF REAL; (* One-Step Receding Horizon State Prediction Vector *)
    x_ref                               : ARRAY[1..16] OF REAL; (* Dynamic Target State Reference Trajectory Vector *)
    u_ctrl                              : ARRAY[1..8] OF REAL;  (* Active Multi-Actuator Control Demand Vector *)
    u_prev                              : ARRAY[1..8] OF REAL;  (* Previous Scan Actuator Control Vector *)
    delta_u                             : ARRAY[1..8] OF REAL;  (* Actuator Slew Rate Control Incremental Step Vector *)
    y_obs                               : ARRAY[1..8] OF REAL;  (* Estimated Cyber-Physical System Output Vector *)

    (* ===================================================================================== *)
    (* 2.0 MODEL PREDICTIVE CONTROL (MPC) QUADRATIC COST MATRICES & PROJECTION BOUNDS        *)
    (* Quadratic weights balancing tracking error, cushion pressure pacing & mechanical wear *)
    (* ===================================================================================== *)
    Q_diag                              : ARRAY[1..16] OF REAL; (* Diagonal State Tracking Error Penalty Weights *)
    R_diag                              : ARRAY[1..8] OF REAL;  (* Diagonal Actuator Effort Penalty Weights *)
    R_delta_diag                        : ARRAY[1..8] OF REAL;  (* Diagonal Actuator Rate-of-Change Slew Penalty Weights *)
    P_diag                              : ARRAY[1..16] OF REAL; (* Terminal State Cost Horizon Diagonal Penalty Weights *)
    u_min                               : ARRAY[1..8] OF REAL;  (* Physical Actuator Saturation Lower Bounds *)
    u_max                               : ARRAY[1..8] OF REAL;  (* Physical Actuator Saturation Upper Bounds *)
    delta_u_max                         : ARRAY[1..8] OF REAL;  (* Maximum Permissible Actuator Slew Rate Limits *)
    grad_J                              : ARRAY[1..8] OF REAL;  (* Analytical Gradient of MPC Quadratic Cost Functional *)
    Hessian_diag                        : ARRAY[1..8] OF REAL;  (* Exact Diagonal Hessian Components of QP Subproblem *)

    (* ===================================================================================== *)
    (* 3.0 TRIPLE MODULAR REDUNDANCY (2oo3) VOTING ACCUMULATORS & DISCREPANCY TIMERS        *)
    (* ===================================================================================== *)
    rCrankAngle_Voted                   : REAL := 0.0;      (* Voted 2oo3 Press Eccentric Crank Angle [deg] *)
    rSpread_CrankAngle                  : REAL := 0.0;      (* Maximum Channel Deviation Spread for Resolvers [deg] *)
    bCrankAngle_Degraded_1oo2           : BOOL := FALSE;    (* Resolver Subsystem Operating in Degraded 1oo2 Mode *)
    bCrankAngle_TMR_Fault               : BOOL := FALSE;    (* Resolver Subsystem Loss of Redundancy Critical Alarm *)
    tTimer_CrankDiscrepancy             : TON;              (* Persistent Resolver Channel Divergence Filter Timer *)

    rThickness_Voted                    : REAL := 1.20;     (* Voted 2oo3 Destacker Sheet Metal Thickness [mm] *)
    rSpread_Thickness                   : REAL := 0.0;      (* Destacker Laser Sensor Channel Deviation Spread [mm] *)
    bThickness_Degraded_1oo2            : BOOL := FALSE;    (* Destacker Sensor Operating in Degraded 1oo2 Mode *)
    bThickness_TMR_Fault                : BOOL := FALSE;    (* Destacker Sensor Loss of Redundancy Alarm *)
    tTimer_ThicknessDiscrepancy         : TON;              (* Persistent Thickness Sensor Divergence Timer *)

    rTonnage_FL_Voted                   : REAL := 0.0;      (* Voted 2oo3 Front-Left Column Tonnage [kN] *)
    rTonnage_FR_Voted                   : REAL := 0.0;      (* Voted 2oo3 Front-Right Column Tonnage [kN] *)
    rTonnage_RL_Voted                   : REAL := 0.0;      (* Voted 2oo3 Rear-Left Column Tonnage [kN] *)
    rTonnage_RR_Voted                   : REAL := 0.0;      (* Voted 2oo3 Rear-Right Column Tonnage [kN] *)
    rSpread_Tonnage_FL                  : REAL := 0.0;      (* Front-Left Load Cell Channel Spread [kN] *)
    rSpread_Tonnage_FR                  : REAL := 0.0;      (* Front-Right Load Cell Channel Spread [kN] *)
    rSpread_Tonnage_RL                  : REAL := 0.0;      (* Rear-Left Load Cell Channel Spread [kN] *)
    rSpread_Tonnage_RR                  : REAL := 0.0;      (* Rear-Right Load Cell Channel Spread [kN] *)
    bTonnage_FL_Degraded                : BOOL := FALSE;    (* Front-Left Column Operating in Degraded 1oo2 *)
    bTonnage_FR_Degraded                : BOOL := FALSE;    (* Front-Right Column Operating in Degraded 1oo2 *)
    bTonnage_RL_Degraded                : BOOL := FALSE;    (* Rear-Left Column Operating in Degraded 1oo2 *)
    bTonnage_RR_Degraded                : BOOL := FALSE;    (* Rear-Right Column Operating in Degraded 1oo2 *)
    tTimer_TonnageFL_Discrepancy        : TON;              (* Front-Left Load Cell Discrepancy Timer *)
    tTimer_TonnageFR_Discrepancy        : TON;              (* Front-Right Load Cell Discrepancy Timer *)
    tTimer_TonnageRL_Discrepancy        : TON;              (* Rear-Left Load Cell Discrepancy Timer *)
    tTimer_TonnageRR_Discrepancy        : TON;              (* Rear-Right Load Cell Discrepancy Timer *)

    rCushionPress_Voted                 : REAL := 210.0;    (* Voted 2oo3 Die Cushion Manifold Pressure [bar] *)
    rSpread_CushionPress                : REAL := 0.0;      (* Cushion Manifold Pressure Sensor Spread [bar] *)
    bCushionPress_Degraded              : BOOL := FALSE;    (* Cushion Pressure Operating in Degraded 1oo2 *)
    tTimer_CushionPressDiscrepancy      : TON;              (* Cushion Pressure Transmitter Discrepancy Timer *)

    tTimer_LightCurtainDiscrepancy      : TON;              (* Safety Light Curtain Dual Channel Mismatch Timer *)

    (* ===================================================================================== *)
    (* 4.0 PRESS MECHANICAL CONSTANTS & SLIDER-CRANK KINEMATICS                              *)
    (* ===================================================================================== *)
    c_rCrankRadius_mm                   : REAL := 400.0;    (* Main Eccentric Crank Throw Radius (800 mm Stroke) [mm] *)
    c_rConnectingRod_mm                 : REAL := 1600.0;   (* Articulated Pitman Connecting Rod Center Distance [mm] *)
    c_rConnectingRodRatio               : REAL := 0.25;     (* Kinematic Lambda Ratio = r / l = 400 / 1600 = 0.25 *)
    c_rBedLength_mm                     : REAL := 5000.0;   (* Press Bolster Bed Length Along Longitudinal Axis Y [mm] *)
    c_rBedWidth_mm                      : REAL := 2500.0;   (* Press Bolster Bed Width Along Transverse Axis X [mm] *)
    c_rMaxAllowableEccentricity_Mx_kNm  : REAL := 3500.0;   (* Maximum Allowable Pitch Tilting Moment [kN m] *)
    c_rMaxAllowableEccentricity_My_kNm  : REAL := 2000.0;   (* Maximum Allowable Roll Tilting Moment [kN m] *)
    c_rTiltStiffness_Pitch              : REAL := 0.00012;  (* Slide Structural Tilting Pitch Compliance [mrad/kN m] *)
    c_rTiltStiffness_Roll               : REAL := 0.00020;  (* Slide Structural Tilting Roll Compliance [mrad/kN m] *)
    rSlideCalculatedPos_mm              : REAL := 800.0;    (* Kinematic Slider-Crank Position z(theta) [mm] *)
    rSlideCalculatedVel_mm_s            : REAL := 0.0;      (* Kinematic Slider-Crank Slide Velocity v(theta) [mm/s] *)
    rCrankOmega_rad_s                   : REAL := 0.0;      (* Crank Angular Velocity [rad/s] *)

    (* ===================================================================================== *)
    (* 5.0 8-POINT HYDRAULIC DIE CUSHION CLOSED-LOOP PID & PRE-ACCELERATION VARIABLES        *)
    (* ===================================================================================== *)
    c_rCushionCylPistonArea_cm2         : REAL := 78.54;    (* Cushion Cylinder Piston Cross-Section (100 mm Bore) [cm^2] *)
    rCushionTargetTonnageProfile_kN     : REAL := 4500.0;   (* Target Dynamic Drawing Cushion Tonnage [kN] *)
    rCushionPreAccelTargetVel_mm_s      : REAL := 0.0;      (* Cushion Upstroke Pre-Acceleration Velocity Match [mm/s] *)
    rCushionPID_Kp                      : REAL := 0.085;    (* Proportional Gain for Cushion Valve Servo Loop [mA/bar] *)
    rCushionPID_Ki                      : REAL := 0.012;    (* Integral Gain for Cushion Valve Servo Loop [mA/(bar*s)] *)
    rCushionPID_Kd                      : REAL := 0.004;    (* Derivative Gain for Cushion Valve Servo Loop [mA*s/bar] *)
    rCushionPressErr_1                  : REAL := 0.0;      (* Pressure Tracking Error Cylinder 1 [bar] *)
    rCushionPressErr_2                  : REAL := 0.0;      (* Pressure Tracking Error Cylinder 2 [bar] *)
    rCushionPressErr_3                  : REAL := 0.0;      (* Pressure Tracking Error Cylinder 3 [bar] *)
    rCushionPressErr_4                  : REAL := 0.0;      (* Pressure Tracking Error Cylinder 4 [bar] *)
    rCushionPressErr_5                  : REAL := 0.0;      (* Pressure Tracking Error Cylinder 5 [bar] *)
    rCushionPressErr_6                  : REAL := 0.0;      (* Pressure Tracking Error Cylinder 6 [bar] *)
    rCushionPressErr_7                  : REAL := 0.0;      (* Pressure Tracking Error Cylinder 7 [bar] *)
    rCushionPressErr_8                  : REAL := 0.0;      (* Pressure Tracking Error Cylinder 8 [bar] *)
    rCushionIntErr_1                    : REAL := 0.0;      (* Accumulated Integral Error Cylinder 1 [bar*s] *)
    rCushionIntErr_2                    : REAL := 0.0;      (* Accumulated Integral Error Cylinder 2 [bar*s] *)
    rCushionIntErr_3                    : REAL := 0.0;      (* Accumulated Integral Error Cylinder 3 [bar*s] *)
    rCushionIntErr_4                    : REAL := 0.0;      (* Accumulated Integral Error Cylinder 4 [bar*s] *)
    rCushionIntErr_5                    : REAL := 0.0;      (* Accumulated Integral Error Cylinder 5 [bar*s] *)
    rCushionIntErr_6                    : REAL := 0.0;      (* Accumulated Integral Error Cylinder 6 [bar*s] *)
    rCushionIntErr_7                    : REAL := 0.0;      (* Accumulated Integral Error Cylinder 7 [bar*s] *)
    rCushionIntErr_8                    : REAL := 0.0;      (* Accumulated Integral Error Cylinder 8 [bar*s] *)
    rCushionPrevPressErr_1              : REAL := 0.0;      (* Previous Scan Pressure Error Cylinder 1 [bar] *)
    rCushionPrevPressErr_2              : REAL := 0.0;      (* Previous Scan Pressure Error Cylinder 2 [bar] *)
    rCushionPrevPressErr_3              : REAL := 0.0;      (* Previous Scan Pressure Error Cylinder 3 [bar] *)
    rCushionPrevPressErr_4              : REAL := 0.0;      (* Previous Scan Pressure Error Cylinder 4 [bar] *)
    rCushionPrevPressErr_5              : REAL := 0.0;      (* Previous Scan Pressure Error Cylinder 5 [bar] *)
    rCushionPrevPressErr_6              : REAL := 0.0;      (* Previous Scan Pressure Error Cylinder 6 [bar] *)
    rCushionPrevPressErr_7              : REAL := 0.0;      (* Previous Scan Pressure Error Cylinder 7 [bar] *)
    rCushionPrevPressErr_8              : REAL := 0.0;      (* Previous Scan Pressure Error Cylinder 8 [bar] *)

    (* ===================================================================================== *)
    (* 6.0 7-AXIS TRI-AXIS TRANSFER GANTRY ELECTRONIC CAM (E-CAM) TRAJECTORY ENGINE          *)
    (* ===================================================================================== *)
    rVirtualMasterTheta_deg             : REAL := 0.0;      (* Virtual Electronic Master Axis Reference Angle [deg] *)
    rTransferFeedPitch_mm               : REAL := 1800.0;   (* Station-to-Station Transfer Feed Pitch Distance [mm] *)
    rTransferClampStroke_mm             : REAL := 400.0;    (* Transverse Tooling Arm Clamp/Unclamp Travel Stroke [mm] *)
    rTransferLiftStroke_mm              : REAL := 250.0;    (* Vertical Tooling Arm Lift/Lower Travel Stroke [mm] *)
    rDieClearanceWindow_Start_deg       : REAL := 220.0;    (* Crank Angle When Press Slide Ascends Above Transfer Envelope [deg] *)
    rDieClearanceWindow_End_deg         : REAL := 335.0;    (* Crank Angle When Press Slide Descends Into Transfer Envelope [deg] *)
    rMinSafeSlideHeight_mm              : REAL := 450.0;    (* Minimum Slide Height Permitting Transfer Gantry Infeed [mm] *)
    bTransferCollisionEnvelopeBreached  : BOOL := FALSE;    (* Transfer Tooling Inside Die Envelope During Downstroke *)
    rCamNormPhase                       : REAL := 0.0;      (* Normalized Electronic Cam Phase Parameter Tau [0.0..1.0] *)
    rCamPolyS                           : REAL := 0.0;      (* Quintic Polynomial S-Curve Normalized Displacement *)
    rCamPolyV                           : REAL := 0.0;      (* Quintic Polynomial S-Curve Normalized Velocity *)

    (* ===================================================================================== *)
    (* 7.0 DESTACKER, BLANK CENTERING & QUALITY PHOTOGRAMMETRY TIMERS & REGISTERS            *)
    (* ===================================================================================== *)
    tDestackerAirFanningTimer           : TON;              (* Pulsed Magnetic Sheet Fanning Air Knife Solenoid Timer *)
    tDoubleBlankRejectDivertTimer       : TON;              (* High-Speed Pneumatic Reject Gate Divert Active Pulse Timer *)
    tBlankCenteringClampTimer           : TON;              (* Servo-Pneumatic Centering Squaring Table Dwell Timer *)
    tLubricantSprayPulseTimer           : TON;              (* High-Pressure Micro-Droplet Electrostatic Lube Pulse Timer *)
    tDelayedCushionLiftTimer            : TON;              (* Post-Draw Vacuum Breakaway Cushion Delay Timer *)
    tEgressConveyorRunTimer             : TON;              (* Finished Body Panel Discharge Conveyor Run Timer *)
    bDoubleBlankTripLatched             : BOOL := FALSE;    (* Latched Reject Bit for Out-of-Tolerance Blank Thickness *)

    (* ===================================================================================== *)
    (* 8.0 FINITE STATE MACHINE (FSM) TIMERS, FLAGS & PREVIOUS REGISTERS                     *)
    (* ===================================================================================== *)
    iState                              : DINT := 10;       (* Internal Active Execution State Index *)
    iPrevState                          : DINT := 10;       (* Previous Active Execution State Index *)
    bFirstScanState                     : BOOL := TRUE;     (* One-Shot Trigger on Entry to New Discrete State *)
    tStateTimeoutTimer                  : TON;              (* Maximum Allowable Dwell Time Watchdog in Any Discrete State *)
    tCycleWatchdogTimer                 : TON;              (* Full Press Cycle Cadence Time Monitoring Timer *)
    tEmergencyTripHoldTimer             : TON;              (* SIL-3 Hydraulic Overload Dump Valve Trip Hold Time Timer *)

    (* ===================================================================================== *)
    (* 9.0 ITERATION COUNTERS & INTERMEDIATE MATH WORKING REGISTERS                          *)
    (* ===================================================================================== *)
    iLoopIndex                          : INT := 0;         (* General Purpose Inner For-Loop Index *)
    jLoopIndex                          : INT := 0;         (* General Purpose Outer For-Loop Index *)
    kLoopIndex                          : INT := 0;         (* General Purpose Matrix Column For-Loop Index *)
    rTempSum                            : REAL := 0.0;      (* Floating-Point Multiply-Accumulate Scratchpad *)
    rTempGrad                           : REAL := 0.0;      (* MPC Gradient Descent Floating-Point Scratchpad *)
    rSineVal                            : REAL := 0.0;      (* Taylor-Series Sine Trigonometric Approximation *)
    rCosineVal                          : REAL := 0.0;      (* Taylor-Series Cosine Trigonometric Approximation *)
    rRadAngle                           : REAL := 0.0       (* Crank Angle Converted to Radians [rad] *)
END_VAR
""")

    # ----------------------------------------------------------------------------------
    # PHASE 0: FIRST SCAN INITIALIZATIONS
    # ----------------------------------------------------------------------------------
    out.append("""
(* ==================================================================================================== *)
(* PHASE 0: SYSTEM COLD-START STATE-SPACE MODEL & MPC WEIGHT MATRIX INITIALIZATION                      *)
(* Executed on cold boot or first scan to populate 16x16 plant dynamics and quadratic optimization cost *)
(* ==================================================================================================== *)
IF NOT bInitStateSpaceDone THEN
    (* --------------------------------------------------------------------------------- *)
    (* Initialize Discrete State Transition Matrix Ad (16x16) at Ts = 0.002 s           *)
    (* Structural compliance, hydraulic fluid bulk modulus, and gantry flexure dynamics  *)
    (* --------------------------------------------------------------------------------- *)
    FOR iLoopIndex := 1 TO 16 DO
        FOR jLoopIndex := 1 TO 16 DO
            Ad[iLoopIndex, jLoopIndex] := 0.0;
        END_FOR;
    END_FOR;

    (* Diagonal dominant self-decay terms (asymptotically stable open-loop modes) *)
    Ad[1, 1] := 0.9985;   Ad[1, 2] := 0.00198; (* Slide vertical displacement / velocity *)
    Ad[2, 1] := -0.1250;  Ad[2, 2] := 0.9840;  Ad[2, 3] := -0.0450; Ad[2, 16] := -0.0085;
    Ad[3, 3] := 0.9920;   Ad[3, 4] := 0.00195; (* Press frame strain / strain rate *)
    Ad[4, 3] := -24.50;   Ad[4, 4] := 0.9650;  Ad[4, 16] := 0.1200;
    Ad[5, 5] := 0.9940;   Ad[5, 7] := 0.00192; (* Slide tilt pitch angle / pitch rate *)
    Ad[6, 6] := 0.9935;   Ad[6, 8] := 0.00192; (* Slide tilt roll angle / roll rate *)
    Ad[7, 5] := -18.20;   Ad[7, 7] := 0.9720;  (* Slide pitch angular acceleration *)
    Ad[8, 6] := -22.40;   Ad[8, 8] := 0.9680;  (* Slide roll angular acceleration *)
    Ad[9, 9] := 0.9990;   Ad[9, 10] := 0.00045; (* Die cushion position / pressure coupling *)
    Ad[10, 9] := -12.80;  Ad[10, 10] := 0.9820; Ad[10, 11] := 0.00185; (* Die cushion pressure / rate *)
    Ad[11, 10] := -85.00; Ad[11, 11] := 0.9450; (* Fluid compressibility rate *)
    Ad[12, 12] := 0.9995; Ad[12, 13] := 0.00199; (* Transfer gantry feed carriage position / speed *)
    Ad[13, 12] := -0.050; Ad[13, 13] := 0.9880; Ad[13, 14] := -0.0320; (* Structural feed vibration coupling *)
    Ad[14, 14] := 0.9860; Ad[14, 15] := 0.00188; (* Transfer rail 1st bending vibrational deflection *)
    Ad[15, 14] := -38.50; Ad[15, 15] := 0.9520; (* Tooling rail vibration damping *)
    Ad[16, 16] := 0.9750; Ad[16, 2] := 0.0420;  (* Sheet metal dynamic plastic deformation resistance *)

    (* --------------------------------------------------------------------------------- *)
    (* Initialize Discrete Input Matrix Bd (16x8)                                        *)
    (* Actuator influence: torque motors, tilt cylinders, cushion servo, gantry drives   *)
    (* --------------------------------------------------------------------------------- *)
    FOR iLoopIndex := 1 TO 16 DO
        FOR kLoopIndex := 1 TO 8 DO
            Bd[iLoopIndex, kLoopIndex] := 0.0;
        END_FOR;
    END_FOR;

    Bd[2, 1]  := 0.00085;  (* Dual torque motor drive torque -> slide velocity *)
    Bd[5, 2]  := 0.00018;  Bd[5, 3]  := 0.00018;  Bd[5, 4]  := -0.00018; Bd[5, 5] := -0.00018; (* Tilt cylinders -> pitch *)
    Bd[6, 2]  := -0.00022; Bd[6, 3]  := 0.00022;  Bd[6, 4]  := -0.00022; Bd[6, 5] := 0.00022;  (* Tilt cylinders -> roll *)
    Bd[7, 2]  := 0.0450;   Bd[7, 3]  := 0.0450;   Bd[7, 4]  := -0.0450;  Bd[7, 5] := -0.0450;  (* Pitch angular accel *)
    Bd[8, 2]  := -0.0550;  Bd[8, 3]  := 0.0550;   Bd[8, 4]  := -0.0550;  Bd[8, 5] := 0.0550;   (* Roll angular accel *)
    Bd[9, 6]  := 0.00120;  (* Die cushion servo valve spool -> piston motion *)
    Bd[10, 6] := 0.4250;   (* Die cushion servo valve spool -> manifold pressure *)
    Bd[11, 6] := 8.5000;   (* Die cushion servo valve spool -> pressure build-up rate *)
    Bd[12, 7] := 0.00025;  (* Transfer gantry X servo torque -> linear position *)
    Bd[13, 7] := 0.08200;  (* Transfer gantry X servo torque -> linear velocity *)
    Bd[14, 7] := 0.00450;  (* Transfer gantry X servo torque -> flexural excitation *)
    Bd[15, 7] := 1.25000;  (* Transfer gantry structural vibration excitation *)
    Bd[12, 8] := 0.00005;  Bd[13, 8] := 0.01500; (* Transfer gantry Z servo cross-axis coupling *)

    (* --------------------------------------------------------------------------------- *)
    (* Initialize Discrete Output Matrix Cd (8x16) and Direct Feedthrough Dd (8x8)       *)
    (* --------------------------------------------------------------------------------- *)
    FOR iLoopIndex := 1 TO 8 DO
        FOR jLoopIndex := 1 TO 16 DO
            Cd[iLoopIndex, jLoopIndex] := 0.0;
        END_FOR;
        FOR kLoopIndex := 1 TO 8 DO
            Dd[iLoopIndex, kLoopIndex] := 0.0;
        END_FOR;
    END_FOR;

    Cd[1, 1]  := 1.0; (* Slide position y1 = x1 *)
    Cd[2, 2]  := 1.0; (* Slide velocity y2 = x2 *)
    Cd[3, 3]  := 1.0; (* Press frame strain y3 = x3 *)
    Cd[4, 5]  := 1.0; (* Pitch tilt angle y4 = x5 *)
    Cd[5, 6]  := 1.0; (* Roll tilt angle y5 = x6 *)
    Cd[6, 10] := 1.0; (* Cushion pressure y6 = x10 *)
    Cd[7, 12] := 1.0; (* Gantry X feed position y7 = x12 *)
    Cd[8, 14] := 1.0; (* Gantry structural flexure y8 = x14 *)

    (* --------------------------------------------------------------------------------- *)
    (* Initialize Model Predictive Control (MPC) Cost Weight Matrices & Slew Rate Limits *)
    (* --------------------------------------------------------------------------------- *)
    FOR iLoopIndex := 1 TO 16 DO
        Q_diag[iLoopIndex] := 1.0;
        P_diag[iLoopIndex] := 2.5;
        x_state[iLoopIndex] := 0.0;
        x_pred[iLoopIndex] := 0.0;
        x_ref[iLoopIndex] := 0.0;
    END_FOR;

    (* Heavily weight slide tracking precision, tilt suppression, and cushion stability *)
    Q_diag[1]  := 150.0; (* Ram vertical trajectory penalty *)
    Q_diag[2]  := 25.0;  (* Ram velocity tracking penalty *)
    Q_diag[3]  := 80.0;  (* Structural frame stress penalty *)
    Q_diag[5]  := 450.0; (* Slide pitch tilt suppression penalty *)
    Q_diag[6]  := 550.0; (* Slide roll tilt suppression penalty *)
    Q_diag[10] := 320.0; (* Cushion holding pressure regulation penalty *)
    Q_diag[12] := 200.0; (* Transfer gantry positioning penalty *)
    Q_diag[14] := 400.0; (* Transfer rail vibration active damping penalty *)

    P_diag[1]  := 300.0;
    P_diag[5]  := 900.0;
    P_diag[6]  := 1100.0;
    P_diag[10] := 650.0;
    P_diag[12] := 400.0;
    P_diag[14] := 850.0;

    FOR kLoopIndex := 1 TO 8 DO
        R_diag[kLoopIndex] := 0.05;
        R_delta_diag[kLoopIndex] := 0.25;
        u_ctrl[kLoopIndex] := 0.0;
        u_prev[kLoopIndex] := 0.0;
        delta_u[kLoopIndex] := 0.0;
        grad_J[kLoopIndex] := 0.0;
        Hessian_diag[kLoopIndex] := 1.0;
    END_FOR;

    (* Actuator effort weights *)
    R_diag[1] := 0.02; (* Torque motors *)
    R_diag[2] := 0.15; (* Leveling cyl FL *)
    R_diag[3] := 0.15; (* Leveling cyl FR *)
    R_diag[4] := 0.15; (* Leveling cyl RL *)
    R_diag[5] := 0.15; (* Leveling cyl RR *)
    R_diag[6] := 0.08; (* Cushion servo valve *)
    R_diag[7] := 0.12; (* Gantry Feed X drive *)
    R_diag[8] := 0.18; (* Gantry Lift Z drive *)

    R_delta_diag[1] := 0.10;
    R_delta_diag[2] := 0.45;
    R_delta_diag[3] := 0.45;
    R_delta_diag[4] := 0.45;
    R_delta_diag[5] := 0.45;
    R_delta_diag[6] := 0.20;
    R_delta_diag[7] := 0.35;
    R_delta_diag[8] := 0.50;

    (* Physical Actuator Limits *)
    u_min[1] := -120.0; u_max[1] := 120.0; (* Dual torque motor drive torque [kN m] *)
    u_min[2] := -80.0;  u_max[2] := 80.0;  (* Leveling flow FL [L/min] *)
    u_min[3] := -80.0;  u_max[3] := 80.0;  (* Leveling flow FR [L/min] *)
    u_min[4] := -80.0;  u_max[4] := 80.0;  (* Leveling flow RL [L/min] *)
    u_min[5] := -80.0;  u_max[5] := 80.0;  (* Leveling flow RR [L/min] *)
    u_min[6] := -40.0;  u_max[6] := 40.0;  (* Cushion valve command [mA] *)
    u_min[7] := -150.0; u_max[7] := 150.0; (* Gantry X motor torque [N m] *)
    u_min[8] := -220.0; u_max[8] := 220.0; (* Gantry Z motor torque [N m] *)

    delta_u_max[1] := 15.0;  (* Max torque ramp per 2 ms scan *)
    delta_u_max[2] := 8.0;   (* Max tilt flow step per scan *)
    delta_u_max[3] := 8.0;
    delta_u_max[4] := 8.0;
    delta_u_max[5] := 8.0;
    delta_u_max[6] := 4.0;   (* Max servo valve spool rate *)
    delta_u_max[7] := 20.0;  (* Max gantry feed torque step *)
    delta_u_max[8] := 25.0;  (* Max gantry lift torque step *)

    bInitStateSpaceDone := TRUE;
END_IF;
""")

    # ----------------------------------------------------------------------------------
    # PHASE 1: 2oo3 TMR SENSOR VOTING & DISCREPANCY FAULT DIAGNOSTICS
    # ----------------------------------------------------------------------------------
    out.append("""
(* ==================================================================================================== *)
(* PHASE 1: TRIPLE MODULAR REDUNDANCY (2oo3) SENSOR VOTING & BUMPLESS DEGRADATION                       *)
(* Executes median selection, spread evaluation, discrepancy timing, and bumpless fallback              *)
(* ==================================================================================================== *)

(* --------------------------------------------------------------------------------- *)
(* 1.1 Press Crank Angle Resolvers 2oo3 Voting (Resolvers A, B, C)                   *)
(* --------------------------------------------------------------------------------- *)
IF (rPressCrankAngle_Resolver_ChA >= rPressCrankAngle_Resolver_ChB AND rPressCrankAngle_Resolver_ChA <= rPressCrankAngle_Resolver_ChC) OR
   (rPressCrankAngle_Resolver_ChA >= rPressCrankAngle_Resolver_ChC AND rPressCrankAngle_Resolver_ChA <= rPressCrankAngle_Resolver_ChB) THEN
    rCrankAngle_Voted := rPressCrankAngle_Resolver_ChA;
ELSIF (rPressCrankAngle_Resolver_ChB >= rPressCrankAngle_Resolver_ChA AND rPressCrankAngle_Resolver_ChB <= rPressCrankAngle_Resolver_ChC) OR
      (rPressCrankAngle_Resolver_ChB >= rPressCrankAngle_Resolver_ChC AND rPressCrankAngle_Resolver_ChB <= rPressCrankAngle_Resolver_ChA) THEN
    rCrankAngle_Voted := rPressCrankAngle_Resolver_ChB;
ELSE
    rCrankAngle_Voted := rPressCrankAngle_Resolver_ChC;
END_IF;

(* Compute maximum spread between any two resolver channels *)
rSpread_CrankAngle := ABS(rPressCrankAngle_Resolver_ChA - rPressCrankAngle_Resolver_ChB);
IF ABS(rPressCrankAngle_Resolver_ChB - rPressCrankAngle_Resolver_ChC) > rSpread_CrankAngle THEN
    rSpread_CrankAngle := ABS(rPressCrankAngle_Resolver_ChB - rPressCrankAngle_Resolver_ChC);
END_IF;
IF ABS(rPressCrankAngle_Resolver_ChC - rPressCrankAngle_Resolver_ChA) > rSpread_CrankAngle THEN
    rSpread_CrankAngle := ABS(rPressCrankAngle_Resolver_ChC - rPressCrankAngle_Resolver_ChA);
END_IF;

(* Discrepancy integration timer: trigger degraded 1oo2 mode if spread exceeds 1.5 degrees for > 15 ms *)
tTimer_CrankDiscrepancy(IN := (rSpread_CrankAngle > 1.5), PT := T#15MS);
IF tTimer_CrankDiscrepancy.Q THEN
    bCrankAngle_Degraded_1oo2 := TRUE;
    (* Select healthier pairing between optical linear scale and resolver channels *)
    IF ABS(rPressCrankAngle_Resolver_ChA - rPressCrankAngle_Resolver_ChB) <= 1.5 THEN
        rCrankAngle_Voted := 0.5 * (rPressCrankAngle_Resolver_ChA + rPressCrankAngle_Resolver_ChB);
    ELSIF ABS(rPressCrankAngle_Resolver_ChA - rPressCrankAngle_Resolver_ChC) <= 1.5 THEN
        rCrankAngle_Voted := 0.5 * (rPressCrankAngle_Resolver_ChA + rPressCrankAngle_Resolver_ChC);
    ELSIF ABS(rPressCrankAngle_Resolver_ChB - rPressCrankAngle_Resolver_ChC) <= 1.5 THEN
        rCrankAngle_Voted := 0.5 * (rPressCrankAngle_Resolver_ChB + rPressCrankAngle_Resolver_ChC);
    ELSE
        bCrankAngle_TMR_Fault := TRUE;
    END_IF;
END_IF;

(* --------------------------------------------------------------------------------- *)
(* 1.2 Destacker Laser Sheet Thickness Displacement Sensors (Sensors A, B, C)       *)
(* --------------------------------------------------------------------------------- *)
IF (rDestackerLaserThickness_ChA >= rDestackerLaserThickness_ChB AND rDestackerLaserThickness_ChA <= rDestackerLaserThickness_ChC) OR
   (rDestackerLaserThickness_ChA >= rDestackerLaserThickness_ChC AND rDestackerLaserThickness_ChA <= rDestackerLaserThickness_ChB) THEN
    rThickness_Voted := rDestackerLaserThickness_ChA;
ELSIF (rDestackerLaserThickness_ChB >= rDestackerLaserThickness_ChA AND rDestackerLaserThickness_ChB <= rDestackerLaserThickness_ChC) OR
      (rDestackerLaserThickness_ChB >= rDestackerLaserThickness_ChC AND rDestackerLaserThickness_ChB <= rDestackerLaserThickness_ChA) THEN
    rThickness_Voted := rDestackerLaserThickness_ChB;
ELSE
    rThickness_Voted := rDestackerLaserThickness_ChC;
END_IF;

rSpread_Thickness := ABS(rDestackerLaserThickness_ChA - rDestackerLaserThickness_ChB);
IF ABS(rDestackerLaserThickness_ChB - rDestackerLaserThickness_ChC) > rSpread_Thickness THEN
    rSpread_Thickness := ABS(rDestackerLaserThickness_ChB - rDestackerLaserThickness_ChC);
END_IF;
IF ABS(rDestackerLaserThickness_ChC - rDestackerLaserThickness_ChA) > rSpread_Thickness THEN
    rSpread_Thickness := ABS(rDestackerLaserThickness_ChC - rDestackerLaserThickness_ChA);
END_IF;

tTimer_ThicknessDiscrepancy(IN := (rSpread_Thickness > 0.15), PT := T#20MS);
IF tTimer_ThicknessDiscrepancy.Q THEN
    bThickness_Degraded_1oo2 := TRUE;
    IF ABS(rDestackerLaserThickness_ChA - rDestackerLaserThickness_ChB) <= 0.15 THEN
        rThickness_Voted := 0.5 * (rDestackerLaserThickness_ChA + rDestackerLaserThickness_ChB);
    ELSIF ABS(rDestackerLaserThickness_ChA - rDestackerLaserThickness_ChC) <= 0.15 THEN
        rThickness_Voted := 0.5 * (rDestackerLaserThickness_ChA + rDestackerLaserThickness_ChC);
    ELSIF ABS(rDestackerLaserThickness_ChB - rDestackerLaserThickness_ChC) <= 0.15 THEN
        rThickness_Voted := 0.5 * (rDestackerLaserThickness_ChB + rDestackerLaserThickness_ChC);
    ELSE
        bThickness_TMR_Fault := TRUE;
    END_IF;
END_IF;

(* --------------------------------------------------------------------------------- *)
(* 1.3 4-Corner Tie-Rod Strain Gauge Load Cells (FL, FR, RL, RR)                     *)
(* --------------------------------------------------------------------------------- *)
(* Front-Left Load Cell Voting *)
IF (rTonnage_FL_ChA >= rTonnage_FL_ChB AND rTonnage_FL_ChA <= rTonnage_FL_ChC) OR
   (rTonnage_FL_ChA >= rTonnage_FL_ChC AND rTonnage_FL_ChA <= rTonnage_FL_ChB) THEN
    rTonnage_FL_Voted := rTonnage_FL_ChA;
ELSIF (rTonnage_FL_ChB >= rTonnage_FL_ChA AND rTonnage_FL_ChB <= rTonnage_FL_ChC) OR
      (rTonnage_FL_ChB >= rTonnage_FL_ChC AND rTonnage_FL_ChB <= rTonnage_FL_ChA) THEN
    rTonnage_FL_Voted := rTonnage_FL_ChB;
ELSE
    rTonnage_FL_Voted := rTonnage_FL_ChC;
END_IF;

rSpread_Tonnage_FL := ABS(rTonnage_FL_ChA - rTonnage_FL_ChB);
IF ABS(rTonnage_FL_ChB - rTonnage_FL_ChC) > rSpread_Tonnage_FL THEN
    rSpread_Tonnage_FL := ABS(rTonnage_FL_ChB - rTonnage_FL_ChC);
END_IF;
IF ABS(rTonnage_FL_ChC - rTonnage_FL_ChA) > rSpread_Tonnage_FL THEN
    rSpread_Tonnage_FL := ABS(rTonnage_FL_ChC - rTonnage_FL_ChA);
END_IF;
tTimer_TonnageFL_Discrepancy(IN := (rSpread_Tonnage_FL > 500.0), PT := T#10MS);
IF tTimer_TonnageFL_Discrepancy.Q THEN
    bTonnage_FL_Degraded := TRUE;
END_IF;

(* Front-Right Load Cell Voting *)
IF (rTonnage_FR_ChA >= rTonnage_FR_ChB AND rTonnage_FR_ChA <= rTonnage_FR_ChC) OR
   (rTonnage_FR_ChA >= rTonnage_FR_ChC AND rTonnage_FR_ChA <= rTonnage_FR_ChB) THEN
    rTonnage_FR_Voted := rTonnage_FR_ChA;
ELSIF (rTonnage_FR_ChB >= rTonnage_FR_ChA AND rTonnage_FR_ChB <= rTonnage_FR_ChC) OR
      (rTonnage_FR_ChB >= rTonnage_FR_ChC AND rTonnage_FR_ChB <= rTonnage_FR_ChA) THEN
    rTonnage_FR_Voted := rTonnage_FR_ChB;
ELSE
    rTonnage_FR_Voted := rTonnage_FR_ChC;
END_IF;

rSpread_Tonnage_FR := ABS(rTonnage_FR_ChA - rTonnage_FR_ChB);
IF ABS(rTonnage_FR_ChB - rTonnage_FR_ChC) > rSpread_Tonnage_FR THEN
    rSpread_Tonnage_FR := ABS(rTonnage_FR_ChB - rTonnage_FR_ChC);
END_IF;
IF ABS(rTonnage_FR_ChC - rTonnage_FR_ChA) > rSpread_Tonnage_FR THEN
    rSpread_Tonnage_FR := ABS(rTonnage_FR_ChC - rTonnage_FR_ChA);
END_IF;
tTimer_TonnageFR_Discrepancy(IN := (rSpread_Tonnage_FR > 500.0), PT := T#10MS);
IF tTimer_TonnageFR_Discrepancy.Q THEN
    bTonnage_FR_Degraded := TRUE;
END_IF;

(* Rear-Left Load Cell Voting *)
IF (rTonnage_RL_ChA >= rTonnage_RL_ChB AND rTonnage_RL_ChA <= rTonnage_RL_ChC) OR
   (rTonnage_RL_ChA >= rTonnage_RL_ChC AND rTonnage_RL_ChA <= rTonnage_RL_ChB) THEN
    rTonnage_RL_Voted := rTonnage_RL_ChA;
ELSIF (rTonnage_RL_ChB >= rTonnage_RL_ChA AND rTonnage_RL_ChB <= rTonnage_RL_ChC) OR
      (rTonnage_RL_ChB >= rTonnage_RL_ChC AND rTonnage_RL_ChB <= rTonnage_RL_ChA) THEN
    rTonnage_RL_Voted := rTonnage_RL_ChB;
ELSE
    rTonnage_RL_Voted := rTonnage_RL_ChC;
END_IF;

rSpread_Tonnage_RL := ABS(rTonnage_RL_ChA - rTonnage_RL_ChB);
IF ABS(rTonnage_RL_ChB - rTonnage_RL_ChC) > rSpread_Tonnage_RL THEN
    rSpread_Tonnage_RL := ABS(rTonnage_RL_ChB - rTonnage_RL_ChC);
END_IF;
IF ABS(rTonnage_RL_ChC - rTonnage_RL_ChA) > rSpread_Tonnage_RL THEN
    rSpread_Tonnage_RL := ABS(rTonnage_RL_ChC - rTonnage_RL_ChA);
END_IF;
tTimer_TonnageRL_Discrepancy(IN := (rSpread_Tonnage_RL > 500.0), PT := T#10MS);
IF tTimer_TonnageRL_Discrepancy.Q THEN
    bTonnage_RL_Degraded := TRUE;
END_IF;

(* Rear-Right Load Cell Voting *)
IF (rTonnage_RR_ChA >= rTonnage_RR_ChB AND rTonnage_RR_ChA <= rTonnage_RR_ChC) OR
   (rTonnage_RR_ChA >= rTonnage_RR_ChC AND rTonnage_RR_ChA <= rTonnage_RR_ChB) THEN
    rTonnage_RR_Voted := rTonnage_RR_ChA;
ELSIF (rTonnage_RR_ChB >= rTonnage_RR_ChA AND rTonnage_RR_ChB <= rTonnage_RR_ChC) OR
      (rTonnage_RR_ChB >= rTonnage_RR_ChC AND rTonnage_RR_ChB <= rTonnage_RR_ChA) THEN
    rTonnage_RR_Voted := rTonnage_RR_ChB;
ELSE
    rTonnage_RR_Voted := rTonnage_RR_ChC;
END_IF;

rSpread_Tonnage_RR := ABS(rTonnage_RR_ChA - rTonnage_RR_ChB);
IF ABS(rTonnage_RR_ChB - rTonnage_RR_ChC) > rSpread_Tonnage_RR THEN
    rSpread_Tonnage_RR := ABS(rTonnage_RR_ChB - rTonnage_RR_ChC);
END_IF;
IF ABS(rTonnage_RR_ChC - rTonnage_RR_ChA) > rSpread_Tonnage_RR THEN
    rSpread_Tonnage_RR := ABS(rTonnage_RR_ChC - rTonnage_RR_ChA);
END_IF;
tTimer_TonnageRR_Discrepancy(IN := (rSpread_Tonnage_RR > 500.0), PT := T#10MS);
IF tTimer_TonnageRR_Discrepancy.Q THEN
    bTonnage_RR_Degraded := TRUE;
END_IF;

(* --------------------------------------------------------------------------------- *)
(* 1.4 Hydraulic Die Cushion Common Manifold Pressure Transmitters (A, B, C)         *)
(* --------------------------------------------------------------------------------- *)
IF (rCushionManifoldPressure_ChA >= rCushionManifoldPressure_ChB AND rCushionManifoldPressure_ChA <= rCushionManifoldPressure_ChC) OR
   (rCushionManifoldPressure_ChA >= rCushionManifoldPressure_ChC AND rCushionManifoldPressure_ChA <= rCushionManifoldPressure_ChB) THEN
    rCushionPress_Voted := rCushionManifoldPressure_ChA;
ELSIF (rCushionManifoldPressure_ChB >= rCushionManifoldPressure_ChA AND rCushionManifoldPressure_ChB <= rCushionManifoldPressure_ChC) OR
      (rCushionManifoldPressure_ChB >= rCushionManifoldPressure_ChC AND rCushionManifoldPressure_ChB <= rCushionManifoldPressure_ChA) THEN
    rCushionPress_Voted := rCushionManifoldPressure_ChB;
ELSE
    rCushionPress_Voted := rCushionManifoldPressure_ChC;
END_IF;

rSpread_CushionPress := ABS(rCushionManifoldPressure_ChA - rCushionManifoldPressure_ChB);
IF ABS(rCushionManifoldPressure_ChB - rCushionManifoldPressure_ChC) > rSpread_CushionPress THEN
    rSpread_CushionPress := ABS(rCushionManifoldPressure_ChB - rCushionManifoldPressure_ChC);
END_IF;
IF ABS(rCushionManifoldPressure_ChC - rCushionManifoldPressure_ChA) > rSpread_CushionPress THEN
    rSpread_CushionPress := ABS(rCushionManifoldPressure_ChC - rCushionManifoldPressure_ChA);
END_IF;
tTimer_CushionPressDiscrepancy(IN := (rSpread_CushionPress > 12.0), PT := T#25MS);
IF tTimer_CushionPressDiscrepancy.Q THEN
    bCushionPress_Degraded := TRUE;
END_IF;

(* --------------------------------------------------------------------------------- *)
(* 1.5 Safety Light Curtain Dual Channel Interlock Discrepancy Monitoring           *)
(* --------------------------------------------------------------------------------- *)
tTimer_LightCurtainDiscrepancy(IN := (bSafetyCurtainDieAreaUnbroken_ChA <> bSafetyCurtainDieAreaUnbroken_ChB), PT := T#50MS);
""")

    # ----------------------------------------------------------------------------------
    # PHASE 2: CYBER-PHYSICAL KINEMATICS, DYNAMICS & DISCRETE STATE-SPACE MODEL
    # ----------------------------------------------------------------------------------
    out.append("""
(* ==================================================================================================== *)
(* PHASE 2: CYBER-PHYSICAL KINEMATICS, DYNAMICS & DISCRETE STATE PROPAGATION                            *)
(* Computes slider-crank kinematics, angular velocity, and executes x[k+1] = Ad*x[k] + Bd*u[k]          *)
(* ==================================================================================================== *)

(* --------------------------------------------------------------------------------- *)
(* 2.1 Slider-Crank Analytical Kinematics & Angular Velocity Calculation            *)
(* --------------------------------------------------------------------------------- *)
rRadAngle := (rCrankAngle_Voted * 3.141592653589793) / 180.0;
rCrankOmega_rad_s := (rNominalPressSpeed_SPM * 2.0 * 3.141592653589793) / 60.0;

(* Analytical Taylor-series approximation for Cosine and Sine to maximize deterministic execution *)
rCosineVal := 1.0 - (0.5 * rRadAngle * rRadAngle) + (0.041666667 * rRadAngle * rRadAngle * rRadAngle * rRadAngle);
rSineVal   := rRadAngle - (0.16666667 * rRadAngle * rRadAngle * rRadAngle) + (0.008333333 * rRadAngle * rRadAngle * rRadAngle * rRadAngle * rRadAngle);

(* Exact slider-crank displacement: z(theta) = r * [ (1 - cos theta) + (1/lambda) * (1 - sqrt(1 - lambda^2 * sin^2 theta)) ] *)
(* Series expansion: z(theta) approx r * [ (1 - cos theta) + (lambda / 4) * (1 - cos 2theta) ] *)
rSlideCalculatedPos_mm := c_rCrankRadius_mm * ( (1.0 - rCosineVal) + (0.25 * c_rConnectingRodRatio * (1.0 - (2.0 * rCosineVal * rCosineVal - 1.0))) );

(* Exact slide velocity: v(theta) = r * omega * [ sin theta + (lambda * sin 2theta) / (2 * sqrt(1 - lambda^2 * sin^2 theta)) ] *)
rSlideCalculatedVel_mm_s := c_rCrankRadius_mm * rCrankOmega_rad_s * ( rSineVal + (0.5 * c_rConnectingRodRatio * (2.0 * rSineVal * rCosineVal)) );
rPressSlideVelocity_mm_s := rSlideCalculatedVel_mm_s;

(* Update physical observation vector from sensors *)
x_state[1] := rPressSlidePosition_Scale_mm - rSlideCalculatedPos_mm; (* Slide displacement excursion *)
x_state[2] := rSlideCalculatedVel_mm_s;
x_state[3] := (rTonnage_FL_Voted + rTonnage_FR_Voted + rTonnage_RL_Voted + rTonnage_RR_Voted) * 0.052; (* Frame strain *)
x_state[5] := rSlideCenterOfLoading_Y_mm * 0.015; (* Slide pitch tilt *)
x_state[6] := rSlideCenterOfLoading_X_mm * 0.022; (* Slide roll tilt *)
x_state[9] := 0.125 * (rCushionCyl_Pos_mm_1 + rCushionCyl_Pos_mm_2 + rCushionCyl_Pos_mm_3 + rCushionCyl_Pos_mm_4 +
                       rCushionCyl_Pos_mm_5 + rCushionCyl_Pos_mm_6 + rCushionCyl_Pos_mm_7 + rCushionCyl_Pos_mm_8);
x_state[10] := rCushionPress_Voted - 210.0; (* Cushion pressure excursion *)
x_state[12] := rTransferAxisX_ActualPos_mm - rTransferAxisX_PosCommand_mm; (* Gantry feed error *)
x_state[13] := rTransferAxisX_ActualVel_m_s * 1000.0; (* Gantry feed velocity *)

(* --------------------------------------------------------------------------------- *)
(* 2.2 Discrete State Space Model One-Step Prediction: x_pred = Ad * x + Bd * u      *)
(* --------------------------------------------------------------------------------- *)
FOR iLoopIndex := 1 TO 16 DO
    rTempSum := 0.0;
    FOR jLoopIndex := 1 TO 16 DO
        rTempSum := rTempSum + (Ad[iLoopIndex, jLoopIndex] * x_state[jLoopIndex]);
    END_FOR;
    FOR kLoopIndex := 1 TO 8 DO
        rTempSum := rTempSum + (Bd[iLoopIndex, kLoopIndex] * u_ctrl[kLoopIndex]);
    END_FOR;
    x_pred[iLoopIndex] := rTempSum;
END_FOR;

(* --------------------------------------------------------------------------------- *)
(* 2.3 System Output Observation Vector Evaluation: y_obs = Cd * x + Dd * u          *)
(* --------------------------------------------------------------------------------- *)
FOR iLoopIndex := 1 TO 8 DO
    rTempSum := 0.0;
    FOR jLoopIndex := 1 TO 16 DO
        rTempSum := rTempSum + (Cd[iLoopIndex, jLoopIndex] * x_state[jLoopIndex]);
    END_FOR;
    FOR kLoopIndex := 1 TO 8 DO
        rTempSum := rTempSum + (Dd[iLoopIndex, kLoopIndex] * u_ctrl[kLoopIndex]);
    END_FOR;
    y_obs[iLoopIndex] := rTempSum;
END_FOR;
""")

    # ----------------------------------------------------------------------------------
    # PHASE 3: RECEDING-HORIZON MPC OPTIMIZATION
    # ----------------------------------------------------------------------------------
    out.append("""
(* ==================================================================================================== *)
(* PHASE 3: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) OPTIMIZATION                                *)
(* Evaluates analytical gradient and executes projected constrained gradient descent steps               *)
(* ==================================================================================================== *)

(* --------------------------------------------------------------------------------- *)
(* 3.1 Establish Target Reference Trajectory Vector x_ref                            *)
(* --------------------------------------------------------------------------------- *)
x_ref[1]  := 0.0; (* Target slide displacement deviation = 0 *)
x_ref[2]  := rSlideCalculatedVel_mm_s;
x_ref[3]  := 0.0; (* Target structural strain = 0 *)
x_ref[5]  := 0.0; (* Slide tilt pitch angle target = 0 mrad *)
x_ref[6]  := 0.0; (* Slide tilt roll angle target = 0 mrad *)
x_ref[9]  := 250.0; (* Cushion nominal position *)
x_ref[10] := 0.0; (* Cushion nominal pressure delta = 0 *)
x_ref[12] := 0.0; (* Gantry feed error target = 0 *)
x_ref[14] := 0.0; (* Gantry rail flexural vibration target = 0 *)

(* --------------------------------------------------------------------------------- *)
(* 3.2 Compute Analytical QP Gradient Vector: grad_J = Bd' * Q * (x_pred - x_ref)    *)
(*     + R * u_prev + R_delta * (u - u_prev)                                         *)
(* --------------------------------------------------------------------------------- *)
FOR kLoopIndex := 1 TO 8 DO
    rTempGrad := 0.0;
    FOR iLoopIndex := 1 TO 16 DO
        rTempGrad := rTempGrad + (Bd[iLoopIndex, kLoopIndex] * Q_diag[iLoopIndex] * (x_pred[iLoopIndex] - x_ref[iLoopIndex]));
    END_FOR;
    grad_J[kLoopIndex] := rTempGrad + (R_diag[kLoopIndex] * u_prev[kLoopIndex]) + (R_delta_diag[kLoopIndex] * delta_u[kLoopIndex]);

    (* Diagonal Hessian approximation for projected descent *)
    Hessian_diag[kLoopIndex] := R_diag[kLoopIndex] + R_delta_diag[kLoopIndex];
    FOR iLoopIndex := 1 TO 16 DO
        Hessian_diag[kLoopIndex] := Hessian_diag[kLoopIndex] + (Bd[iLoopIndex, kLoopIndex] * Bd[iLoopIndex, kLoopIndex] * Q_diag[iLoopIndex]);
    END_FOR;
    IF Hessian_diag[kLoopIndex] < 0.001 THEN
        Hessian_diag[kLoopIndex] := 0.001; (* Guard against zero division *)
    END_IF;

    (* ----------------------------------------------------------------------------- *)
    (* 3.3 Projected Gradient Descent Step with Actuator Slew Rate & Box Limits     *)
    (* ----------------------------------------------------------------------------- *)
    delta_u[kLoopIndex] := - (grad_J[kLoopIndex] / Hessian_diag[kLoopIndex]);

    (* Slew rate bounding *)
    IF delta_u[kLoopIndex] > delta_u_max[kLoopIndex] THEN
        delta_u[kLoopIndex] := delta_u_max[kLoopIndex];
    ELSIF delta_u[kLoopIndex] < -delta_u_max[kLoopIndex] THEN
        delta_u[kLoopIndex] := -delta_u_max[kLoopIndex];
    END_IF;

    (* Update candidate control vector *)
    u_ctrl[kLoopIndex] := u_prev[kLoopIndex] + delta_u[kLoopIndex];

    (* Hard saturation box constraints *)
    IF u_ctrl[kLoopIndex] > u_max[kLoopIndex] THEN
        u_ctrl[kLoopIndex] := u_max[kLoopIndex];
    ELSIF u_ctrl[kLoopIndex] < u_min[kLoopIndex] THEN
        u_ctrl[kLoopIndex] := u_min[kLoopIndex];
    END_IF;

    (* Latch previous control for rate penalty in next scan *)
    u_prev[kLoopIndex] := u_ctrl[kLoopIndex];
END_FOR;
""")

    # ----------------------------------------------------------------------------------
    # PHASE 4: 4-CORNER ECCENTRICITY BALANCING & DYNAMIC HYDROSTATIC TILT LEVELING
    # ----------------------------------------------------------------------------------
    out.append("""
(* ==================================================================================================== *)
(* PHASE 4: 4-CORNER ECCENTRICITY CALCULATION & DYNAMIC HYDROSTATIC TILT LEVELING                       *)
(* Computes real-time center of loading (Xc, Yc), tilting moments (Mx, My), and injects counter-tilt    *)
(* ==================================================================================================== *)

(* --------------------------------------------------------------------------------- *)
(* 4.1 Total Stamping Force & Center-of-Loading Coordinates                          *)
(* --------------------------------------------------------------------------------- *)
rTotalMeasuredTonnage_kN := rTonnage_FL_Voted + rTonnage_FR_Voted + rTonnage_RL_Voted + rTonnage_RR_Voted;

IF rTotalMeasuredTonnage_kN > 100.0 THEN
    (* Transverse Bed Axis X Center of Loading (Left vs Right imbalance) *)
    rSlideCenterOfLoading_X_mm := ( ( (rTonnage_FR_Voted + rTonnage_RR_Voted) - (rTonnage_FL_Voted + rTonnage_RL_Voted) ) / rTotalMeasuredTonnage_kN ) * (c_rBedWidth_mm / 2.0);

    (* Longitudinal Bed Axis Y Center of Loading (Front vs Rear imbalance) *)
    rSlideCenterOfLoading_Y_mm := ( ( (rTonnage_FL_Voted + rTonnage_FR_Voted) - (rTonnage_RL_Voted + rTonnage_RR_Voted) ) / rTotalMeasuredTonnage_kN ) * (c_rBedLength_mm / 2.0);

    (* Calculated Eccentric Tilting Moments *)
    rEccentricityMoment_Mx_kNm := rTotalMeasuredTonnage_kN * (rSlideCenterOfLoading_Y_mm / 1000.0);
    rEccentricityMoment_My_kNm := rTotalMeasuredTonnage_kN * (rSlideCenterOfLoading_X_mm / 1000.0);
ELSE
    rSlideCenterOfLoading_X_mm := 0.0;
    rSlideCenterOfLoading_Y_mm := 0.0;
    rEccentricityMoment_Mx_kNm := 0.0;
    rEccentricityMoment_My_kNm := 0.0;
END_IF;

(* --------------------------------------------------------------------------------- *)
(* 4.2 Dynamic Bed Tilt Leveling Pressure Biasing Commands                          *)
(* Closed-loop hydraulic counter-pressure injection to prevent slide gib scuffing    *)
(* --------------------------------------------------------------------------------- *)
rTiltLevelingCyl_Pressure_Cmd_FL_bar := 150.0 - (rEccentricityMoment_Mx_kNm * 0.025) - (rEccentricityMoment_My_kNm * 0.035) + u_ctrl[2];
rTiltLevelingCyl_Pressure_Cmd_FR_bar := 150.0 - (rEccentricityMoment_Mx_kNm * 0.025) + (rEccentricityMoment_My_kNm * 0.035) + u_ctrl[3];
rTiltLevelingCyl_Pressure_Cmd_RL_bar := 150.0 + (rEccentricityMoment_Mx_kNm * 0.025) - (rEccentricityMoment_My_kNm * 0.035) + u_ctrl[4];
rTiltLevelingCyl_Pressure_Cmd_RR_bar := 150.0 + (rEccentricityMoment_Mx_kNm * 0.025) + (rEccentricityMoment_My_kNm * 0.035) + u_ctrl[5];

(* Clamp leveling cylinder pressures within safe hydraulic working bounds [50..320 bar] *)
IF rTiltLevelingCyl_Pressure_Cmd_FL_bar > 320.0 THEN rTiltLevelingCyl_Pressure_Cmd_FL_bar := 320.0; ELSIF rTiltLevelingCyl_Pressure_Cmd_FL_bar < 50.0 THEN rTiltLevelingCyl_Pressure_Cmd_FL_bar := 50.0; END_IF;
IF rTiltLevelingCyl_Pressure_Cmd_FR_bar > 320.0 THEN rTiltLevelingCyl_Pressure_Cmd_FR_bar := 320.0; ELSIF rTiltLevelingCyl_Pressure_Cmd_FR_bar < 50.0 THEN rTiltLevelingCyl_Pressure_Cmd_FR_bar := 50.0; END_IF;
IF rTiltLevelingCyl_Pressure_Cmd_RL_bar > 320.0 THEN rTiltLevelingCyl_Pressure_Cmd_RL_bar := 320.0; ELSIF rTiltLevelingCyl_Pressure_Cmd_RL_bar < 50.0 THEN rTiltLevelingCyl_Pressure_Cmd_RL_bar := 50.0; END_IF;
IF rTiltLevelingCyl_Pressure_Cmd_RR_bar > 320.0 THEN rTiltLevelingCyl_Pressure_Cmd_RR_bar := 320.0; ELSIF rTiltLevelingCyl_Pressure_Cmd_RR_bar < 50.0 THEN rTiltLevelingCyl_Pressure_Cmd_RR_bar := 50.0; END_IF;
""")

    # ----------------------------------------------------------------------------------
    # PHASE 5: 8-POINT MULTI-CYLINDER HYDRAULIC DIE CUSHION PROFILING & PRE-ACCELERATION
    # ----------------------------------------------------------------------------------
    out.append("""
(* ==================================================================================================== *)
(* PHASE 5: 8-POINT HYDRAULIC DIE CUSHION PROFILING & PRE-ACCELERATION CONTROL                          *)
(* Manages cushion pre-acceleration match, deep-draw pressure regulation, and delayed return lift       *)
(* ==================================================================================================== *)

(* Calculate total instantaneous blankholder holding force *)
rTotalCushionHoldingForce_kN := (rCushionCyl_Press_bar_1 + rCushionCyl_Press_bar_2 + rCushionCyl_Press_bar_3 + rCushionCyl_Press_bar_4 +
                                 rCushionCyl_Press_bar_5 + rCushionCyl_Press_bar_6 + rCushionCyl_Press_bar_7 + rCushionCyl_Press_bar_8) *
                                (c_rCushionCylPistonArea_cm2 / 100.0) * 0.1;

(* --------------------------------------------------------------------------------- *)
(* 5.1 Cushion Pre-Acceleration Phase (theta = 110 deg to 125 deg)                   *)
(* Prior to metal contact, accelerate cushion downward to match ram velocity         *)
(* --------------------------------------------------------------------------------- *)
IF (rCrankAngle_Voted >= 110.0) AND (rCrankAngle_Voted < 125.0) THEN
    rCushionPreAccelTargetVel_mm_s := rPressSlideVelocity_mm_s * 0.95;
    rCushionTargetForce_Current_kN := 800.0; (* Reduced pre-contact holding force *)
(* --------------------------------------------------------------------------------- *)
(* 5.2 Deep-Draw High-Pressure Holding Phase (theta = 125 deg to 180 deg)            *)
(* Multi-step recipe tonnage profiling to suppress sheet wrinkling & thinning        *)
(* --------------------------------------------------------------------------------- *)
ELSIF (rCrankAngle_Voted >= 125.0) AND (rCrankAngle_Voted <= 180.0) THEN
    rCushionPreAccelTargetVel_mm_s := 0.0;
    (* Profile holding force based on draw depth progress *)
    IF rCrankAngle_Voted < 145.0 THEN
        rCushionTargetForce_Current_kN := rCushionTargetTonnageProfile_kN * 1.10; (* Initial high clamp to seat blank *)
    ELSIF rCrankAngle_Voted < 165.0 THEN
        rCushionTargetForce_Current_kN := rCushionTargetTonnageProfile_kN * 1.00; (* Steady deep draw forming *)
    ELSE
        rCushionTargetForce_Current_kN := rCushionTargetTonnageProfile_kN * 0.85; (* Tonnage taper approaching BDC *)
    END_IF;
(* --------------------------------------------------------------------------------- *)
(* 5.3 Bottom Dead Center (BDC) Dwell & Delayed Breakaway Lift (theta = 180 to 230)  *)
(* --------------------------------------------------------------------------------- *)
ELSIF (rCrankAngle_Voted > 180.0) AND (rCrankAngle_Voted <= 230.0) THEN
    rCushionTargetForce_Current_kN := 400.0; (* Hold down part during punch withdrawal *)
ELSE
    rCushionTargetForce_Current_kN := 1200.0; (* Reset cushion to top resting position *)
END_IF;

(* --------------------------------------------------------------------------------- *)
(* 5.4 8-Point Multi-Cylinder Closed-Loop Servo Valve PID Control                    *)
(* --------------------------------------------------------------------------------- *)
(* Cylinder 1 PID *)
rCushionPressErr_1 := (rCushionTargetForce_Current_kN / 8.0) / ((c_rCushionCylPistonArea_cm2 / 100.0) * 0.1) - rCushionCyl_Press_bar_1;
rCushionIntErr_1 := rCushionIntErr_1 + (rCushionPressErr_1 * 0.002);
IF rCushionIntErr_1 > 500.0 THEN rCushionIntErr_1 := 500.0; ELSIF rCushionIntErr_1 < -500.0 THEN rCushionIntErr_1 := -500.0; END_IF;
rCushionServoValve_Cmd_mA_1 := (rCushionPID_Kp * rCushionPressErr_1) + (rCushionPID_Ki * rCushionIntErr_1) +
                               (rCushionPID_Kd * (rCushionPressErr_1 - rCushionPrevPressErr_1) / 0.002) + u_ctrl[6];
rCushionPrevPressErr_1 := rCushionPressErr_1;

(* Cylinder 2 PID *)
rCushionPressErr_2 := (rCushionTargetForce_Current_kN / 8.0) / ((c_rCushionCylPistonArea_cm2 / 100.0) * 0.1) - rCushionCyl_Press_bar_2;
rCushionIntErr_2 := rCushionIntErr_2 + (rCushionPressErr_2 * 0.002);
IF rCushionIntErr_2 > 500.0 THEN rCushionIntErr_2 := 500.0; ELSIF rCushionIntErr_2 < -500.0 THEN rCushionIntErr_2 := -500.0; END_IF;
rCushionServoValve_Cmd_mA_2 := (rCushionPID_Kp * rCushionPressErr_2) + (rCushionPID_Ki * rCushionIntErr_2) +
                               (rCushionPID_Kd * (rCushionPressErr_2 - rCushionPrevPressErr_2) / 0.002) + u_ctrl[6];
rCushionPrevPressErr_2 := rCushionPressErr_2;

(* Cylinder 3 PID *)
rCushionPressErr_3 := (rCushionTargetForce_Current_kN / 8.0) / ((c_rCushionCylPistonArea_cm2 / 100.0) * 0.1) - rCushionCyl_Press_bar_3;
rCushionIntErr_3 := rCushionIntErr_3 + (rCushionPressErr_3 * 0.002);
IF rCushionIntErr_3 > 500.0 THEN rCushionIntErr_3 := 500.0; ELSIF rCushionIntErr_3 < -500.0 THEN rCushionIntErr_3 := -500.0; END_IF;
rCushionServoValve_Cmd_mA_3 := (rCushionPID_Kp * rCushionPressErr_3) + (rCushionPID_Ki * rCushionIntErr_3) +
                               (rCushionPID_Kd * (rCushionPressErr_3 - rCushionPrevPressErr_3) / 0.002) + u_ctrl[6];
rCushionPrevPressErr_3 := rCushionPressErr_3;

(* Cylinder 4 PID *)
rCushionPressErr_4 := (rCushionTargetForce_Current_kN / 8.0) / ((c_rCushionCylPistonArea_cm2 / 100.0) * 0.1) - rCushionCyl_Press_bar_4;
rCushionIntErr_4 := rCushionIntErr_4 + (rCushionPressErr_4 * 0.002);
IF rCushionIntErr_4 > 500.0 THEN rCushionIntErr_4 := 500.0; ELSIF rCushionIntErr_4 < -500.0 THEN rCushionIntErr_4 := -500.0; END_IF;
rCushionServoValve_Cmd_mA_4 := (rCushionPID_Kp * rCushionPressErr_4) + (rCushionPID_Ki * rCushionIntErr_4) +
                               (rCushionPID_Kd * (rCushionPressErr_4 - rCushionPrevPressErr_4) / 0.002) + u_ctrl[6];
rCushionPrevPressErr_4 := rCushionPressErr_4;

(* Cylinder 5 PID *)
rCushionPressErr_5 := (rCushionTargetForce_Current_kN / 8.0) / ((c_rCushionCylPistonArea_cm2 / 100.0) * 0.1) - rCushionCyl_Press_bar_5;
rCushionIntErr_5 := rCushionIntErr_5 + (rCushionPressErr_5 * 0.002);
IF rCushionIntErr_5 > 500.0 THEN rCushionIntErr_5 := 500.0; ELSIF rCushionIntErr_5 < -500.0 THEN rCushionIntErr_5 := -500.0; END_IF;
rCushionServoValve_Cmd_mA_5 := (rCushionPID_Kp * rCushionPressErr_5) + (rCushionPID_Ki * rCushionIntErr_5) +
                               (rCushionPID_Kd * (rCushionPressErr_5 - rCushionPrevPressErr_5) / 0.002) + u_ctrl[6];
rCushionPrevPressErr_5 := rCushionPressErr_5;

(* Cylinder 6 PID *)
rCushionPressErr_6 := (rCushionTargetForce_Current_kN / 8.0) / ((c_rCushionCylPistonArea_cm2 / 100.0) * 0.1) - rCushionCyl_Press_bar_6;
rCushionIntErr_6 := rCushionIntErr_6 + (rCushionPressErr_6 * 0.002);
IF rCushionIntErr_6 > 500.0 THEN rCushionIntErr_6 := 500.0; ELSIF rCushionIntErr_6 < -500.0 THEN rCushionIntErr_6 := -500.0; END_IF;
rCushionServoValve_Cmd_mA_6 := (rCushionPID_Kp * rCushionPressErr_6) + (rCushionPID_Ki * rCushionIntErr_6) +
                               (rCushionPID_Kd * (rCushionPressErr_6 - rCushionPrevPressErr_6) / 0.002) + u_ctrl[6];
rCushionPrevPressErr_6 := rCushionPrevPressErr_6;

(* Cylinder 7 PID *)
rCushionPressErr_7 := (rCushionTargetForce_Current_kN / 8.0) / ((c_rCushionCylPistonArea_cm2 / 100.0) * 0.1) - rCushionCyl_Press_bar_7;
rCushionIntErr_7 := rCushionIntErr_7 + (rCushionPressErr_7 * 0.002);
IF rCushionIntErr_7 > 500.0 THEN rCushionIntErr_7 := 500.0; ELSIF rCushionIntErr_7 < -500.0 THEN rCushionIntErr_7 := -500.0; END_IF;
rCushionServoValve_Cmd_mA_7 := (rCushionPID_Kp * rCushionPressErr_7) + (rCushionPID_Ki * rCushionIntErr_7) +
                               (rCushionPID_Kd * (rCushionPressErr_7 - rCushionPrevPressErr_7) / 0.002) + u_ctrl[6];
rCushionPrevPressErr_7 := rCushionPrevPressErr_7;

(* Cylinder 8 PID *)
rCushionPressErr_8 := (rCushionTargetForce_Current_kN / 8.0) / ((c_rCushionCylPistonArea_cm2 / 100.0) * 0.1) - rCushionCyl_Press_bar_8;
rCushionIntErr_8 := rCushionIntErr_8 + (rCushionPressErr_8 * 0.002);
IF rCushionIntErr_8 > 500.0 THEN rCushionIntErr_8 := 500.0; ELSIF rCushionIntErr_8 < -500.0 THEN rCushionIntErr_8 := -500.0; END_IF;
rCushionServoValve_Cmd_mA_8 := (rCushionPID_Kp * rCushionPressErr_8) + (rCushionPID_Ki * rCushionIntErr_8) +
                               (rCushionPID_Kd * (rCushionPressErr_8 - rCushionPrevPressErr_8) / 0.002) + u_ctrl[6];
rCushionPrevPressErr_8 := rCushionPressErr_8;

(* Clamp servo valve output currents [-40.0..+40.0 mA] *)
IF rCushionServoValve_Cmd_mA_1 > 40.0 THEN rCushionServoValve_Cmd_mA_1 := 40.0; ELSIF rCushionServoValve_Cmd_mA_1 < -40.0 THEN rCushionServoValve_Cmd_mA_1 := -40.0; END_IF;
IF rCushionServoValve_Cmd_mA_2 > 40.0 THEN rCushionServoValve_Cmd_mA_2 := 40.0; ELSIF rCushionServoValve_Cmd_mA_2 < -40.0 THEN rCushionServoValve_Cmd_mA_2 := -40.0; END_IF;
IF rCushionServoValve_Cmd_mA_3 > 40.0 THEN rCushionServoValve_Cmd_mA_3 := 40.0; ELSIF rCushionServoValve_Cmd_mA_3 < -40.0 THEN rCushionServoValve_Cmd_mA_3 := -40.0; END_IF;
IF rCushionServoValve_Cmd_mA_4 > 40.0 THEN rCushionServoValve_Cmd_mA_4 := 40.0; ELSIF rCushionServoValve_Cmd_mA_4 < -40.0 THEN rCushionServoValve_Cmd_mA_4 := -40.0; END_IF;
IF rCushionServoValve_Cmd_mA_5 > 40.0 THEN rCushionServoValve_Cmd_mA_5 := 40.0; ELSIF rCushionServoValve_Cmd_mA_5 < -40.0 THEN rCushionServoValve_Cmd_mA_5 := -40.0; END_IF;
IF rCushionServoValve_Cmd_mA_6 > 40.0 THEN rCushionServoValve_Cmd_mA_6 := 40.0; ELSIF rCushionServoValve_Cmd_mA_6 < -40.0 THEN rCushionServoValve_Cmd_mA_6 := -40.0; END_IF;
IF rCushionServoValve_Cmd_mA_7 > 40.0 THEN rCushionServoValve_Cmd_mA_7 := 40.0; ELSIF rCushionServoValve_Cmd_mA_7 < -40.0 THEN rCushionServoValve_Cmd_mA_7 := -40.0; END_IF;
IF rCushionServoValve_Cmd_mA_8 > 40.0 THEN rCushionServoValve_Cmd_mA_8 := 40.0; ELSIF rCushionServoValve_Cmd_mA_8 < -40.0 THEN rCushionServoValve_Cmd_mA_8 := -40.0; END_IF;
""")

    # ----------------------------------------------------------------------------------
    # PHASE 6: 7-AXIS TRI-AXIS TRANSFER GANTRY E-CAM SYNCHRONIZATION & COLLISION CLEARANCE
    # ----------------------------------------------------------------------------------
    out.append("""
(* ==================================================================================================== *)
(* PHASE 6: 7-AXIS TRI-AXIS TRANSFER GANTRY E-CAM SYNCHRONIZATION & COLLISION CLEARANCE                *)
(* Computes electronic cam profiles, quintic polynomial S-curves, and verifies collision envelope       *)
(* ==================================================================================================== *)

rVirtualMasterTheta_deg := rCrankAngle_Voted;

(* --------------------------------------------------------------------------------- *)
(* 6.1 Check Die Opening Safety Clearance Envelope                                   *)
(* --------------------------------------------------------------------------------- *)
IF (rPressSlidePosition_Scale_mm < rMinSafeSlideHeight_mm) AND
   ((rVirtualMasterTheta_deg < rDieClearanceWindow_Start_deg) OR (rVirtualMasterTheta_deg > rDieClearanceWindow_End_deg)) THEN
    (* Slide is physically below the safe threshold outside the open window *)
    IF (rTransferAxisY_ActualPos_mm > 50.0) THEN
        (* Transfer gripper tooling is extended into the die cavity! Immediate hazard! *)
        bTransferCollisionEnvelopeBreached := TRUE;
    ELSE
        bTransferCollisionEnvelopeBreached := FALSE;
    END_IF;
ELSE
    bTransferCollisionEnvelopeBreached := FALSE;
END_IF;

(* --------------------------------------------------------------------------------- *)
(* 6.2 Quintic Polynomial E-Cam Motion Generation for Feed X, Clamp Y, Lift Z        *)
(* Phase window: theta = 225 deg to 330 deg (105 deg total transfer transfer window) *)
(* --------------------------------------------------------------------------------- *)
IF (rVirtualMasterTheta_deg >= rDieClearanceWindow_Start_deg) AND (rVirtualMasterTheta_deg <= rDieClearanceWindow_End_deg) THEN
    (* Normalized phase parameter tau in [0.0..1.0] *)
    rCamNormPhase := (rVirtualMasterTheta_deg - rDieClearanceWindow_Start_deg) / (rDieClearanceWindow_End_deg - rDieClearanceWindow_Start_deg);
    IF rCamNormPhase > 1.0 THEN rCamNormPhase := 1.0; ELSIF rCamNormPhase < 0.0 THEN rCamNormPhase := 0.0; END_IF;

    (* 5th-order polynomial: s(tau) = 10*tau^3 - 15*tau^4 + 6*tau^5 *)
    rCamPolyS := (10.0 * rCamNormPhase * rCamNormPhase * rCamNormPhase) -
                 (15.0 * rCamNormPhase * rCamNormPhase * rCamNormPhase * rCamNormPhase) +
                 (6.0 * rCamNormPhase * rCamNormPhase * rCamNormPhase * rCamNormPhase * rCamNormPhase);

    (* Velocity: v(tau) = 30*tau^2 - 60*tau^3 + 30*tau^4 *)
    rCamPolyV := (30.0 * rCamNormPhase * rCamNormPhase) -
                 (60.0 * rCamNormPhase * rCamNormPhase * rCamNormPhase) +
                 (30.0 * rCamNormPhase * rCamNormPhase * rCamNormPhase * rCamNormPhase);

    (* Multi-axis coordinated setpoints *)
    rTransferAxisX_PosCommand_mm := rCamPolyS * rTransferFeedPitch_mm;
    rTransferAxisX_VelDemand_m_s := rCamPolyV * (rTransferFeedPitch_mm / 1000.0) * (rCrankOmega_rad_s / 1.8326);
    rTransferAxisY_PosCommand_mm := rTransferClampStroke_mm; (* Grippers fully clamped *)
    rTransferAxisZ_PosCommand_mm := rTransferLiftStroke_mm;  (* Tooling lifted to pass-line *)
    bTransferGripperVacuumEngage := TRUE;
ELSE
    (* Outside transfer window: return transfer carriage to home pick position *)
    rTransferAxisX_PosCommand_mm := 0.0;
    rTransferAxisX_VelDemand_m_s := 0.0;
    rTransferAxisY_PosCommand_mm := 0.0; (* Unclamped clearance position *)
    rTransferAxisZ_PosCommand_mm := 0.0; (* Lowered to standby *)
    bTransferGripperVacuumEngage := FALSE;
END_IF;
""")

    # ----------------------------------------------------------------------------------
    # PHASE 7: DESTACKER BLANK FEEDER & IN-LINE PHOTOGRAMMETRY
    # ----------------------------------------------------------------------------------
    out.append("""
(* ==================================================================================================== *)
(* PHASE 7: DESTACKER BLANK FEEDER, DOUBLE-BLANK LASER GAUGING & PHOTOGRAMMETRY QUALITY                 *)
(* Controls sheet magnetic fanning, fast 20 ms reject divert gate, and validates panel geometry         *)
(* ==================================================================================================== *)

(* --------------------------------------------------------------------------------- *)
(* 7.1 Double-Blank Laser Gauging & High-Speed Pneumatic Diverter Gate               *)
(* Reject condition: blank thickness > 1.25x nominal (e.g. 1.20 mm * 1.25 = 1.50 mm)  *)
(* --------------------------------------------------------------------------------- *)
IF (rThickness_Voted > (rNominalBlankThickness_mm * 1.25)) OR (rThickness_Voted < (rNominalBlankThickness_mm * 0.75)) THEN
    bDoubleBlankTripLatched := TRUE;
    bDoubleBlankRejectGateDivert := TRUE;
    tDoubleBlankRejectDivertTimer(IN := TRUE, PT := T#250MS);
ELSE
    tDoubleBlankRejectDivertTimer(IN := FALSE);
    IF tDoubleBlankRejectDivertTimer.Q THEN
        bDoubleBlankRejectGateDivert := FALSE;
    END_IF;
END_IF;

(* --------------------------------------------------------------------------------- *)
(* 7.2 In-Line Real-Time Photogrammetry Inspection Analysis                          *)
(* Analyzes draw depth (+/- 0.5 mm), flange wrinkling (< 0.1 mm), and thinning (< 22%) *)
(* --------------------------------------------------------------------------------- *)
IF (ABS(rPhotogrammetry_DrawDepth_mm - rTargetDrawDepth_mm) <= 0.65) AND
   (rPhotogrammetry_WrinkleAmplitude_mm <= 0.10) AND
   (rPhotogrammetry_ThinningPct <= 22.0) AND
   (NOT bPhotogrammetry_SplitDetected) THEN
    bPartInspectionPassStatus := TRUE;
ELSE
    bPartInspectionPassStatus := FALSE;
END_IF;
""")

    # ----------------------------------------------------------------------------------
    # PHASE 8: 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM)
    # ----------------------------------------------------------------------------------
    out.append("""
(* ==================================================================================================== *)
(* PHASE 8: 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM)                                             *)
(* Sequences complete high-speed stamping cycle: destack, transfer, pre-accel, draw, eject, egress      *)
(* ==================================================================================================== *)

IF iState <> iPrevState THEN
    bFirstScanState := TRUE;
    iPrevState := iState;
ELSE
    bFirstScanState := FALSE;
END_IF;

CASE iState OF
    (* ----------------------------------------------------------------------------- *)
    (* STATE 10: DESTACKER SHEET LIFT & MAGNETIC FANNING                             *)
    (* ----------------------------------------------------------------------------- *)
    10:
        bDestackerFanningAirBlast := TRUE;
        bDestackerVacuumCupLift   := TRUE;
        bBlankCenteringActuatorAdvance := FALSE;
        bDieLubricantSprayPulse   := FALSE;
        bStampedPanelEgressConveyorRun := FALSE;

        tDestackerAirFanningTimer(IN := TRUE, PT := T#120MS);
        tStateTimeoutTimer(IN := TRUE, PT := T#1500MS);

        IF tDestackerAirFanningTimer.Q THEN
            tDestackerAirFanningTimer(IN := FALSE);
            tStateTimeoutTimer(IN := FALSE);
            iState := 20; (* Advance to laser thickness verification *)
        ELSIF tStateTimeoutTimer.Q THEN
            tStateTimeoutTimer(IN := FALSE);
            iState := 999; (* Timeout fault *)
        END_IF;

    (* ----------------------------------------------------------------------------- *)
    (* STATE 20: DOUBLE-BLANK LASER VERIFICATION                                     *)
    (* ----------------------------------------------------------------------------- *)
    20:
        bDestackerFanningAirBlast := FALSE;
        tStateTimeoutTimer(IN := TRUE, PT := T#500MS);

        IF bDoubleBlankTripLatched THEN
            (* Double blank detected: divert sheet to reject bin *)
            bDoubleBlankRejectGateDivert := TRUE;
            IF tDoubleBlankRejectDivertTimer.Q THEN
                bDoubleBlankTripLatched := FALSE;
                bDoubleBlankRejectGateDivert := FALSE;
                tStateTimeoutTimer(IN := FALSE);
                iState := 10; (* Retry blank pick *)
            END_IF;
        ELSE
            (* Sheet thickness verified healthy *)
            bDoubleBlankRejectGateDivert := FALSE;
            tStateTimeoutTimer(IN := FALSE);
            iState := 30; (* Advance to centering & lubrication *)
        END_IF;

        IF tStateTimeoutTimer.Q THEN
            tStateTimeoutTimer(IN := FALSE);
            iState := 999;
        END_IF;

    (* ----------------------------------------------------------------------------- *)
    (* STATE 30: BLANK CENTERING & LUBRICANT SPRAY                                   *)
    (* ----------------------------------------------------------------------------- *)
    30:
        bBlankCenteringActuatorAdvance := TRUE;
        bDieLubricantSprayPulse := TRUE;

        tBlankCenteringClampTimer(IN := TRUE, PT := T#180MS);
        tLubricantSprayPulseTimer(IN := TRUE, PT := T#80MS);
        tStateTimeoutTimer(IN := TRUE, PT := T#800MS);

        IF tBlankCenteringClampTimer.Q THEN
            bBlankCenteringActuatorAdvance := FALSE;
            bDieLubricantSprayPulse := FALSE;
            tBlankCenteringClampTimer(IN := FALSE);
            tLubricantSprayPulseTimer(IN := FALSE);
            tStateTimeoutTimer(IN := FALSE);
            iState := 40; (* Advance to transfer pick *)
        ELSIF tStateTimeoutTimer.Q THEN
            tStateTimeoutTimer(IN := FALSE);
            iState := 999;
        END_IF;

    (* ----------------------------------------------------------------------------- *)
    (* STATE 40: TRI-AXIS TRANSFER GANTRY PICK & STATION INFEED                      *)
    (* ----------------------------------------------------------------------------- *)
    40:
        bTransferGripperVacuumEngage := TRUE;
        tStateTimeoutTimer(IN := TRUE, PT := T#1200MS);

        IF (rTransferAxisY_ActualPos_mm >= (rTransferClampStroke_mm - 5.0)) AND
           (rTransferAxisZ_ActualPos_mm >= (rTransferLiftStroke_mm - 5.0)) THEN
            tStateTimeoutTimer(IN := FALSE);
            iState := 50; (* Advance to press ram acceleration *)
        ELSIF tStateTimeoutTimer.Q THEN
            tStateTimeoutTimer(IN := FALSE);
            iState := 999;
        END_IF;

    (* ----------------------------------------------------------------------------- *)
    (* STATE 50: PRESS RAM ACCELERATION & E-CAM SYNCHRONIZATION                      *)
    (* ----------------------------------------------------------------------------- *)
    50:
        bDualTorqueMotorEnable := TRUE;
        bClutchEngaged_Command := TRUE;
        bBrakeRelease_Command  := TRUE;
        bPressInContinuousStamping := TRUE;

        (* Accelerate dual torque motors to match nominal stroke cadence *)
        rTorqueMotor1_SpeedDemand_rpm := (rNominalPressSpeed_SPM * 30.0);
        rTorqueMotor2_SpeedDemand_rpm := (rNominalPressSpeed_SPM * 30.0);
        rTorqueMotor1_TorqueLimit_Nm  := 45000.0;
        rTorqueMotor2_TorqueLimit_Nm  := 45000.0;

        IF (rCrankAngle_Voted >= 105.0) AND (rCrankAngle_Voted < 125.0) THEN
            iState := 60; (* Advance to cushion pre-acceleration *)
        END_IF;

    (* ----------------------------------------------------------------------------- *)
    (* STATE 60: DIE CUSHION PRE-ACCELERATION CONTACT                                *)
    (* ----------------------------------------------------------------------------- *)
    60:
        (* Synchronize cushion cylinder downstroke velocity to eliminate impact shock *)
        IF (rCrankAngle_Voted >= 125.0) THEN
            iState := 70; (* Blankholder contact established; proceed to deep draw *)
        END_IF;

    (* ----------------------------------------------------------------------------- *)
    (* STATE 70: DEEP DRAW FORMING & MULTI-POINT TONNAGE PROFILING                   *)
    (* ----------------------------------------------------------------------------- *)
    70:
        (* Main plastic deformation phase: monitor 4-corner load and dynamic leveling *)
        IF (rCrankAngle_Voted >= 175.0) AND (rCrankAngle_Voted <= 185.0) THEN
            iState := 80; (* Bottom Dead Center BDC reached *)
        END_IF;

    (* ----------------------------------------------------------------------------- *)
    (* STATE 80: BOTTOM DEAD CENTER (BDC) TONNAGE & ECCENTRICITY AUDIT               *)
    (* ----------------------------------------------------------------------------- *)
    80:
        (* Verify tonnage peaks and moments within press rating *)
        IF (rTotalMeasuredTonnage_kN > rMaxAllowableTonnage_kN) OR
           (ABS(rEccentricityMoment_Mx_kNm) > c_rMaxAllowableEccentricity_Mx_kNm) OR
           (ABS(rEccentricityMoment_My_kNm) > c_rMaxAllowableEccentricity_My_kNm) THEN
            (* Tonnage overload / eccentricity limit breached: trip press *)
            iState := 999;
        ELSE
            IF (rCrankAngle_Voted > 185.0) THEN
                iState := 90; (* Slide ascending: delayed cushion ejection *)
            END_IF;
        END_IF;

    (* ----------------------------------------------------------------------------- *)
    (* STATE 90: DELAYED CUSHION LIFT & PART EJECTION                                *)
    (* ----------------------------------------------------------------------------- *)
    90:
        tDelayedCushionLiftTimer(IN := TRUE, PT := T#60MS);

        IF tDelayedCushionLiftTimer.Q AND (rCrankAngle_Voted >= rDieClearanceWindow_Start_deg) THEN
            tDelayedCushionLiftTimer(IN := FALSE);
            iState := 100; (* Transfer window open: advance parts to next stations *)
        END_IF;

    (* ----------------------------------------------------------------------------- *)
    (* STATE 100: TRANSFER GANTRY PART ADVANCE TO NEXT DIE STATION                   *)
    (* ----------------------------------------------------------------------------- *)
    100:
        IF (rVirtualMasterTheta_deg >= 320.0) AND (rTransferAxisX_ActualPos_mm >= (rTransferFeedPitch_mm - 10.0)) THEN
            iState := 110; (* Transfer complete: proceed to egress & vision inspection *)
        END_IF;

    (* ----------------------------------------------------------------------------- *)
    (* STATE 110: STAMPED BODY PANEL EGRESS TO CONVEYOR & VISION AUDIT               *)
    (* ----------------------------------------------------------------------------- *)
    110:
        bStampedPanelEgressConveyorRun := TRUE;
        tEgressConveyorRunTimer(IN := TRUE, PT := T#450MS);

        IF tEgressConveyorRunTimer.Q THEN
            tEgressConveyorRunTimer(IN := FALSE);
            iState := 120; (* Cycle complete *)
        END_IF;

    (* ----------------------------------------------------------------------------- *)
    (* STATE 120: CYCLE COMPLETION DWELL & CONTINUOUS CADENCE RESUMPTION             *)
    (* ----------------------------------------------------------------------------- *)
    120:
        IF bAutoCycleStartCommand AND bEnableMasterSafetyPermissive AND (NOT bDoubleBlankTripLatched) THEN
            iState := 10; (* Seamless continuous cadence into next stroke *)
        ELSE
            bPressInContinuousStamping := FALSE;
            rTorqueMotor1_SpeedDemand_rpm := 0.0;
            rTorqueMotor2_SpeedDemand_rpm := 0.0;
            IF bAutoCycleStartCommand THEN
                iState := 10;
            END_IF;
        END_IF;

    (* ----------------------------------------------------------------------------- *)
    (* STATE 999: EMERGENCY HYDRAULIC OVERLOAD PRESSURE DUMP & SIL-3 TRIP            *)
    (* ----------------------------------------------------------------------------- *)
    999:
        bSystemReadyForAutoCycle      := FALSE;
        bPressInContinuousStamping    := FALSE;
        bClutchEngaged_Command        := FALSE; (* Disengage pneumatic clutch *)
        bBrakeRelease_Command         := FALSE; (* Drop spring-applied mechanical brake *)
        bEmergencyOverloadDump_Active := TRUE;  (* Fast-acting hydraulic overload dump valve open *)
        bDualTorqueMotorEnable        := FALSE;
        rTorqueMotor1_SpeedDemand_rpm := 0.0;
        rTorqueMotor2_SpeedDemand_rpm := 0.0;
        rTorqueMotor1_TorqueLimit_Nm  := 0.0;
        rTorqueMotor2_TorqueLimit_Nm  := 0.0;
        bTransferGripperVacuumEngage  := FALSE;
        bDestackerFanningAirBlast     := FALSE;
        bDestackerVacuumCupLift       := FALSE;
        bBlankCenteringActuatorAdvance := FALSE;
        bDieLubricantSprayPulse       := FALSE;
        bStampedPanelEgressConveyorRun := FALSE;

        (* Reset requires operator master alarm acknowledgement *)
        IF bMasterAlarmAcknowledge AND bHardwiredEStopRelayHealthy THEN
            bEmergencyOverloadDump_Active := FALSE;
            iState := 10; (* Return to standby idle *)
        END_IF;

END_CASE;

iOperationalState := iState;
bSystemReadyForAutoCycle := (iState = 10) AND bEnableMasterSafetyPermissive AND bHardwiredEStopRelayHealthy;
""")

    # ----------------------------------------------------------------------------------
    # PHASE 9: ISA-18.2 MULTI-TIERED ALARM MATRIX & TELEMETRY
    # ----------------------------------------------------------------------------------
    out.append("""
(* ==================================================================================================== *)
(* PHASE 9: ISA-18.2 MULTI-TIERED ALARM MATRIX & DIAGNOSTIC TELEMETRY                                   *)
(* Categorizes faults into HH, H, Interlocks, and Sensor Diagnostics with bit-packed DWORDs             *)
(* ==================================================================================================== *)

(* Reset telemetry words *)
dwISA_AlarmWord_HighHigh   := 16#00000000;
dwISA_AlarmWord_High       := 16#00000000;
dwISA_AlarmWord_Interlock  := 16#00000000;
dwISA_AlarmWord_Diagnostic := 16#00000000;

(* --------------------------------------------------------------------------------- *)
(* 9.1 Priority 1: High-High (HH) Critical Emergency Shutdown Alarms                *)
(* --------------------------------------------------------------------------------- *)
IF rTotalMeasuredTonnage_kN > 42000.0 THEN
    dwISA_AlarmWord_HighHigh := dwISA_AlarmWord_HighHigh OR 16#00000001; (* Bit 0: Total Tonnage HH Trip (> 42,000 kN) *)
    iState := 999;
END_IF;

IF ABS(rEccentricityMoment_Mx_kNm) > 3500.0 THEN
    dwISA_AlarmWord_HighHigh := dwISA_AlarmWord_HighHigh OR 16#00000002; (* Bit 1: Pitch Tilting Moment Mx HH Trip *)
    iState := 999;
END_IF;

IF ABS(rEccentricityMoment_My_kNm) > 2000.0 THEN
    dwISA_AlarmWord_HighHigh := dwISA_AlarmWord_HighHigh OR 16#00000004; (* Bit 2: Roll Tilting Moment My HH Trip *)
    iState := 999;
END_IF;

IF bTransferCollisionEnvelopeBreached THEN
    dwISA_AlarmWord_HighHigh := dwISA_AlarmWord_HighHigh OR 16#00000008; (* Bit 3: Transfer Gantry In-Die Collision Breach *)
    iState := 999;
END_IF;

IF NOT bHardwiredEStopRelayHealthy THEN
    dwISA_AlarmWord_HighHigh := dwISA_AlarmWord_HighHigh OR 16#00000010; (* Bit 4: Hardwired E-Stop Relay Circuit Dropped *)
    iState := 999;
END_IF;

IF bCrankAngle_TMR_Fault THEN
    dwISA_AlarmWord_HighHigh := dwISA_AlarmWord_HighHigh OR 16#00000020; (* Bit 5: Crank Resolver Complete TMR Failure *)
    iState := 999;
END_IF;

IF rTorqueMotor_BearingTemp_degC > 95.0 THEN
    dwISA_AlarmWord_HighHigh := dwISA_AlarmWord_HighHigh OR 16#00000040; (* Bit 6: Torque Motor Bearing Overtemperature HH *)
    iState := 999;
END_IF;

(* --------------------------------------------------------------------------------- *)
(* 9.2 Priority 2: High (H) Production Process Warning Alarms                        *)
(* --------------------------------------------------------------------------------- *)
IF rTotalMeasuredTonnage_kN > 38000.0 THEN
    dwISA_AlarmWord_High := dwISA_AlarmWord_High OR 16#00000001; (* Bit 0: Total Tonnage Warning H (> 38,000 kN) *)
END_IF;

IF ABS(rEccentricityMoment_Mx_kNm) > 2800.0 THEN
    dwISA_AlarmWord_High := dwISA_AlarmWord_High OR 16#00000002; (* Bit 1: Pitch Moment Warning H (> 2,800 kN m) *)
END_IF;

IF ABS(rEccentricityMoment_My_kNm) > 1600.0 THEN
    dwISA_AlarmWord_High := dwISA_AlarmWord_High OR 16#00000004; (* Bit 2: Roll Moment Warning H (> 1,600 kN m) *)
END_IF;

IF (rCushionPress_Voted < 140.0) AND (iState = 70) THEN
    dwISA_AlarmWord_High := dwISA_AlarmWord_High OR 16#00000008; (* Bit 3: Die Cushion Drawing Pressure Drop Warning *)
END_IF;

IF rPhotogrammetry_WrinkleAmplitude_mm > 0.08 THEN
    dwISA_AlarmWord_High := dwISA_AlarmWord_High OR 16#00000010; (* Bit 4: Part Flange Surface Wrinkling Advisory *)
END_IF;

IF rPhotogrammetry_ThinningPct > 18.0 THEN
    dwISA_AlarmWord_High := dwISA_AlarmWord_High OR 16#00000020; (* Bit 5: Part Excessive Corner Thinning Advisory *)
END_IF;

IF bDoubleBlankTripLatched THEN
    dwISA_AlarmWord_High := dwISA_AlarmWord_High OR 16#00000040; (* Bit 6: Double Blank Diverted to Reject Bin *)
END_IF;

(* --------------------------------------------------------------------------------- *)
(* 9.3 Priority 3: Hardware Safety & Process Permissive Interlocks                   *)
(* --------------------------------------------------------------------------------- *)
IF NOT bHydrostaticGibLubePressureOK THEN
    dwISA_AlarmWord_Interlock := dwISA_AlarmWord_Interlock OR 16#00000001; (* Bit 0: Hydrostatic Gib Lube Pressure Low *)
END_IF;

IF NOT bClutchBrakeAirPressureOK THEN
    dwISA_AlarmWord_Interlock := dwISA_AlarmWord_Interlock OR 16#00000002; (* Bit 1: Pneumatic Clutch/Brake Air Low *)
END_IF;

IF NOT bDieClampHydraulicPressureOK THEN
    dwISA_AlarmWord_Interlock := dwISA_AlarmWord_Interlock OR 16#00000004; (* Bit 2: Die Hydraulic Clamp Pressure Low *)
END_IF;

IF NOT bHydraulicPowerUnitRunning THEN
    dwISA_AlarmWord_Interlock := dwISA_AlarmWord_Interlock OR 16#00000008; (* Bit 3: Hydraulic Power Unit HPU Stopped *)
END_IF;

IF NOT bSafetyCurtainDieAreaUnbroken_ChA OR NOT bSafetyCurtainDieAreaUnbroken_ChB THEN
    dwISA_AlarmWord_Interlock := dwISA_AlarmWord_Interlock OR 16#00000010; (* Bit 4: Die Light Curtain Beam Interrupted *)
END_IF;

IF NOT bSafetyCurtainDestackerClear THEN
    dwISA_AlarmWord_Interlock := dwISA_AlarmWord_Interlock OR 16#00000020; (* Bit 5: Destacker Loading Muting Beam Blocked *)
END_IF;

(* --------------------------------------------------------------------------------- *)
(* 9.4 Priority 4: Sensor TMR Discrepancy & Health Diagnostics                       *)
(* --------------------------------------------------------------------------------- *)
IF bCrankAngle_Degraded_1oo2 THEN
    dwISA_AlarmWord_Diagnostic := dwISA_AlarmWord_Diagnostic OR 16#00000001; (* Bit 0: Crank Resolver Degraded to 1oo2 *)
END_IF;

IF bThickness_Degraded_1oo2 THEN
    dwISA_AlarmWord_Diagnostic := dwISA_AlarmWord_Diagnostic OR 16#00000002; (* Bit 1: Destacker Laser Degraded to 1oo2 *)
END_IF;

IF bTonnage_FL_Degraded THEN
    dwISA_AlarmWord_Diagnostic := dwISA_AlarmWord_Diagnostic OR 16#00000004; (* Bit 2: Tonnage FL Degraded to 1oo2 *)
END_IF;

IF bTonnage_FR_Degraded THEN
    dwISA_AlarmWord_Diagnostic := dwISA_AlarmWord_Diagnostic OR 16#00000008; (* Bit 3: Tonnage FR Degraded to 1oo2 *)
END_IF;

IF bTonnage_RL_Degraded THEN
    dwISA_AlarmWord_Diagnostic := dwISA_AlarmWord_Diagnostic OR 16#00000010; (* Bit 4: Tonnage RL Degraded to 1oo2 *)
END_IF;

IF bTonnage_RR_Degraded THEN
    dwISA_AlarmWord_Diagnostic := dwISA_AlarmWord_Diagnostic OR 16#00000020; (* Bit 5: Tonnage RR Degraded to 1oo2 *)
END_IF;

IF bCushionPress_Degraded THEN
    dwISA_AlarmWord_Diagnostic := dwISA_AlarmWord_Diagnostic OR 16#00000040; (* Bit 6: Cushion Pressure Degraded to 1oo2 *)
END_IF;

IF tTimer_LightCurtainDiscrepancy.Q THEN
    dwISA_AlarmWord_Diagnostic := dwISA_AlarmWord_Diagnostic OR 16#00000080; (* Bit 7: Safety Curtain Ch A/B Discrepancy *)
END_IF;
""")

    # ----------------------------------------------------------------------------------
    # CLOSING
    # ----------------------------------------------------------------------------------
    out.append("END_FUNCTION_BLOCK\n")

    return "".join(out)

def build_prompt():
    return """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices (A, B, C, D), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: Heavy Machinery & Metal Stamping: 4,000-Ton Multi-Station Automotive Transfer Stamping Press with 7-Axis Tri-Axis Transfer Gantry, Multi-Point Hydraulic Die Cushion & Eccentricity Tonnage Balancing**

CRITICAL RULES:
1. CODE FENCE: Use TRIPLE backticks + iec-st (```iec-st).
2. STRUCTURE:
   a. First line: FUNCTION_BLOCK FB_StampingPress_4000Ton_TransferGantry_DieCushion
   b. VAR_INPUT ... END_VAR (min 8 typed inputs with physical units [kN], [bar], [mm], [m/s], [deg], [strokes/min], [kN m], [%], [kW], [ms])
   c. VAR_OUTPUT ... END_VAR (min 7 typed outputs with engineering units & status words)
   d. VAR ... END_VAR (internal state matrices, filter accumulators, 2oo3 voting vars)
   e. Multi-stage CASE machine with END_CASE;
   f. Last line: END_FUNCTION_BLOCK
3. LENGTH: Assistant content MUST be >= 3500 characters total (target 55,000 - 85,000+ chars). Maximize token usage with deep technical explanations, complex algorithms, and industrial reliability features. DO NOT TRIM OR ENFORCE AN UPPER BOUND LIMIT.
4. PARITY: Ensure 100% exact parity between IF and END_IF, CASE and END_CASE.
5. SAVE using this exact Python:
   import json, uuid
   prompt = \"\"\"<copy this exact user prompt here>\"\"\"
   code = \"\"\"```iec-st
FUNCTION_BLOCK FB_StampingPress_4000Ton_TransferGantry_DieCushion
//...
END_FUNCTION_BLOCK
```\"\"\"
   record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
   with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
       json.dump(record, f, ensure_ascii=False)
6. REPLY with: EVOLUTION COMPLETE: Heavy Machinery & Metal Stamping: 4,000-Ton Multi-Station Automotive Transfer Stamping Press with 7-Axis Tri-Axis Transfer Gantry, Multi-Point Hydraulic Die Cushion & Eccentricity Tonnage Balancing"""

if __name__ == "__main__":
    code = generate_iec_code()
    print(f"Generated IEC ST length: {len(code)} characters.")
    
    prompt = build_prompt()
    assistant_content = f"```iec-st\n{code}```"
    
    record = {
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": assistant_content}
        ]
    }
    
    target_path = "data/swarm_raw/agent_6f1940ac.json"
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(f"Saved dataset record to {target_path}")

