# -*- coding: utf-8 -*-
"""
Builder for:
Domain: Heavy Mechanical Engineering & Industrial Tooling (Large-Scale 5-Axis Gantry Milling Center, Real-Time Dynamic Spindle Thermal Growth Compensation & Active Chatter Vibration Damping)
Function Block: FB_Machining_5AxisGantry_ThermalSpindleComp_ActiveDamping
"""

import sys
import os
import json
import uuid

def generate_iec_st():
    st = []
    
    # -------------------------------------------------------------------------
    # 1. FUNCTION BLOCK DECLARATION & COMPREHENSIVE HEADER
    # -------------------------------------------------------------------------
    st.append("""FUNCTION_BLOCK FB_Machining_5AxisGantry_ThermalSpindleComp_ActiveDamping
(* =====================================================================================================================
 * LUMINA CYBER-PHYSICAL AUTOMATION ENGINE - SYNTHETIC DATASET V7 MAX-PERSONA
 * ARCHITECTURAL GRADE : Heavy Mechanical Engineering & Industrial Tooling (Tier 1 Priority Global Sector)
 * COMMERCIAL SYSTEM    : Ultra-Precision Large-Scale 5-Axis Bridge/Gantry CNC Machining Center (Aerospace & Heavy Tooling)
 *                       Work Envelope: X = 20,000 mm (Dual Master-Slave Servos), Y = 6,000 mm, Z = 2,500 mm
 *                       Fork-Type High-Torque Continuous 5-Axis Milling Head (A-Axis +/- 120 deg, C-Axis +/- 360 deg)
 * CORE SUBSYSTEMS      :
 *   1. Master-Slave Synchronous Gantry Anti-Skew Control:
 *      - Dual direct-drive synchronous rack-and-pinion servos (Master X1 and Slave X2) with sub-micron skew regulation.
 *      - Master-Slave skew cancellation (< 1.5 um dynamic tracking error under asymmetric cross-beam acceleration).
 *   2. Real-Time Dynamic Spindle Thermal Growth Compensation:
 *      - 30,000 rpm, 45 kW direct-drive motorized spindle with hybrid ceramic bearings (Si3N4 balls, Cronidur 30 rings).
 *      - First-principles thermodynamic expansion state-space model coupled with high-speed piezo micro-actuator
 *        (+/- 50 um dynamic stroke, sub-millisecond response) and live CNC coordinate origin dynamic Z-axis shift.
 *   3. Active Regenerative Chatter Vibration Damping & Spindle Speed Modulation (SSM):
 *      - Tool Center Point (TCP) triaxial high-frequency vibration acceleration feedback.
 *      - Active magnetic bearing (AMB) counter-force inertial damping injection.
 *      - Real-time Spindle Speed Modulation (SSM) with sinusoidal velocity perturbation (RVA = 10..15%, fm = 2.0..3.5 Hz)
 *        to disrupt regenerative chatter phase shift and chip thickness regeneration.
 *   4. Triple Modular Redundant (2oo3 TMR) Sensor Architecture:
 *      - Dual Gantry Absolute Linear Scales ST_SCALE_101A/B/C [um]
 *      - Spindle Front Ceramic Bearing Pt100 RTDs TT_BEAR_201A/B/C [deg C]
 *      - Spindle Nose Non-Contact Eddy-Current Proximity Sensors DT_SPINDLE_301A/B/C [um]
 *      - Tool Head Triaxial High-Frequency Accelerometers AT_CHATTER_401A/B/C [m/s2]
 *      - Spindle Motor High-Bandwidth Phase Current Sensors IT_CURRENT_501A/B/C [A]
 *      - Discrepancy accumulation timers (100 ms) and 4-tier bumpless degradation logic.
 *   5. Cyber-Physical Discrete State-Space Model & Kalman Observer:
 *      - 8 States, 6 Actuator Inputs, 6 Measured Outputs at Ts = 1.0 ms deterministic scan time.
 *      - Fully populated non-zero matrices: A (8x8), B (8x6), C (6x8), D (6x6), Observer Gain L (8x6).
 *   6. Receding-Horizon Model Predictive Control (MPC) with Projected Gradient Descent (PGD):
 *      - Horizon N = 5 steps, 6 unrolled iterations of PGD, state error Q, actuator R, terminal P matrices.
 *      - Hard box constraints, slew rate limiters on all 6 actuators.
 *   7. Deterministic 14-Stage Production Finite State Machine (FSM):
 *      - Millisecond-synchronized sequencing from Power-On, Warmup, Kinematic Tool Calibration, Datum Lock,
 *        Gantry Auto-Squaring, Spindle Ramp, Coolant Lock, 5-Axis Milling, Active Chatter SSM Damping,
 *        Thermal Live Compensation, Tool Wear Acoustic Check, Spindle Orient, ATC Swap, to Collision Retract.
 *   8. ISA-18.2 Multi-Tier Process Alarms & Fast Tool Fracture Detection:
 *      - Sub-millisecond (< 1.0 ms) tool break / kinetic collision retraction trip.
 *      - 4-Tier alarms (HH, H, L, LL) with deadband hysteresis, bit-packed DWORD telemetry (32-bit status & alarms).
 *
 * GOVERNING STANDARDS  : IEC 61131-3 3rd Ed., ISO 230-3 (Thermal Machine Tools), ISO 10791, ISO 1940, ISA-18.2
 * CONTROLLER SCAN TIME : Ts = 1.0 ms (1,000 Hz deterministic servo task cycle)
 * ===================================================================================================================== *)
""")

    # -------------------------------------------------------------------------
    # 2. VAR_INPUT BLOCK
    # -------------------------------------------------------------------------
    st.append("""VAR_INPUT
    (* =================================================================================================================
     * TRIPLE MODULAR REDUNDANT (2oo3 TMR) PRIMARY PROCESS INSTRUMENTATION CHANNELS
     * ================================================================================================================= *)
    (* --- 2oo3 TMR Channel 1: Gantry Master-Slave Linear Skew Encoders (ST-SCALE-101) --- *)
    rGantrySkew_Scale101A_In     : REAL;    (* Master-Slave Gantry Dual Absolute Optical Linear Scale Channel A [um] *)
    rGantrySkew_Scale101B_In     : REAL;    (* Master-Slave Gantry Dual Absolute Optical Linear Scale Channel B [um] *)
    rGantrySkew_Scale101C_In     : REAL;    (* Master-Slave Gantry Dual Absolute Optical Linear Scale Channel C [um] *)

    (* --- 2oo3 TMR Channel 2: Spindle Front Ceramic Bearing Pt100 RTDs (TT-BEAR-201) --- *)
    rSpindleTemp_TT201A_In       : REAL;    (* Spindle Forward Hybrid Ceramic Bearing Pt100 RTD Channel A [deg C] *)
    rSpindleTemp_TT201B_In       : REAL;    (* Spindle Forward Hybrid Ceramic Bearing Pt100 RTD Channel B [deg C] *)
    rSpindleTemp_TT201C_In       : REAL;    (* Spindle Forward Hybrid Ceramic Bearing Pt100 RTD Channel C [deg C] *)

    (* --- 2oo3 TMR Channel 3: Spindle Nose Eddy-Current Proximity Sensors (DT-SPINDLE-301) --- *)
    rSpindleDisp_DT301A_In       : REAL;    (* Spindle Nose Non-Contact Eddy-Current Axial Displacement Channel A [um] *)
    rSpindleDisp_DT301B_In       : REAL;    (* Spindle Nose Non-Contact Eddy-Current Axial Displacement Channel B [um] *)
    rSpindleDisp_DT301C_In       : REAL;    (* Spindle Nose Non-Contact Eddy-Current Axial Displacement Channel C [um] *)

    (* --- 2oo3 TMR Channel 4: Tool Center Point Triaxial Accelerometers (AT-CHATTER-401) --- *)
    rChatterAccel_AT401A_In      : REAL;    (* Spindle Nose Triaxial High-Frequency Accelerometer Channel A [m/s2] *)
    rChatterAccel_AT401B_In      : REAL;    (* Spindle Nose Triaxial High-Frequency Accelerometer Channel B [m/s2] *)
    rChatterAccel_AT401C_In      : REAL;    (* Spindle Nose Triaxial High-Frequency Accelerometer Channel C [m/s2] *)

    (* --- 2oo3 TMR Channel 5: Spindle Inverter Motor Phase Current Transducers (IT-CURRENT-501) --- *)
    rMotorCurrent_IT501A_In      : REAL;    (* Spindle Direct-Drive Motor Phase Current Transducer Channel A [A] *)
    rMotorCurrent_IT501B_In      : REAL;    (* Spindle Direct-Drive Motor Phase Current Transducer Channel B [A] *)
    rMotorCurrent_IT501C_In      : REAL;    (* Spindle Direct-Drive Motor Phase Current Transducer Channel C [A] *)

    (* =================================================================================================================
     * AUXILIARY MACHINE STRUCTURAL, THERMAL & FLUID PROCESS INSTRUMENTATION
     * ================================================================================================================= *)
    rSpindleRearBearingTemp_TT202_In : REAL; (* Spindle Rear Hybrid Ceramic Bearing Pt100 RTD [deg C] *)
    rColumnTemp_Left_TT601A_In       : REAL; (* Gantry Left Vertical Structural Column Base Pt100 RTD [deg C] *)
    rColumnTemp_Right_TT601B_In      : REAL; (* Gantry Right Vertical Structural Column Base Pt100 RTD [deg C] *)
    rCoolantPressure_PT701_In        : REAL; (* Through-Spindle Coolant Delivery Line Pressure Transducer [bar] *)
    rCoolantFlow_FT702_In            : REAL; (* Through-Spindle Coolant Volumetric Turbine Flowmeter [L/min] *)
    rCoolantSupplyTemp_TT703_In      : REAL; (* Chilled Fluid Coolant Supply Temperature [deg C] *)
    rOilMistPressure_PT801_In        : REAL; (* Spindle Ceramic Bearings Oil-Air Lubrication Line Pressure [bar] *)
    rHydraulicPressure_PT901_In      : REAL; (* Z-Axis Dynamic Counterbalance Accumulator Hydraulic Pressure [bar] *)
    rPneumaticAirPressure_PT902_In   : REAL; (* Main Shop Compressed Air Supply Line Pressure [bar] *)
    rSpindleActualSpeed_In           : REAL; (* Spindle Optical Ring Encoder Actual Rotational Speed [rpm] *)
    rToolTouchProbeDisp_In           : REAL; (* Blum Laser Tool Setter Kinematic Deflection Displacement [um] *)
    rWorkpieceProbeSignal_In         : REAL; (* Wireless Optical Workpiece Surface Touch Probe Deflection [um] *)

    (* =================================================================================================================
     * CNC INTERPOLATION KERNEL PROCESS TRAJECTORY & COMMAND PARAMETERS
     * ================================================================================================================= *)
    rProgrammedSpindleSpeed_In       : REAL; (* CNC Part Program Commanded Spindle Rotational Speed [rpm] *)
    rProgrammedCuttingFeed_In        : REAL; (* CNC Part Program Commanded 5-Axis Vector Path Feedrate [mm/min] *)
    rProgrammedCuttingDepth_In       : REAL; (* Commanded Axial Depth of Cut ap [mm] *)
    rProgrammedCuttingWidth_In       : REAL; (* Commanded Radial Width of Cut ae [mm] *)
    iTarget_Tool_Slot_In             : INT;  (* Commanded Magazine Tool Pot Slot ID for Next ATC Cycle [1..120] *)

    (* =================================================================================================================
     * DISCRETE MACHINE SAFETY, INTERLOCK & OPERATOR COMMAND FLAGS
     * ================================================================================================================= *)
    bSafetyGate_Interlock_OK_In      : BOOL; (* CNC Machine Perimeter Enclosure Safety Gate Interlock OK *)
    bEmergencyStop_Circuit_OK_In     : BOOL; (* Dual-Channel SIL-3 Emergency Stop Circuit Normal Closed *)
    bHydraulicPower_Ready_In         : BOOL; (* Hydraulic Power Unit System Pressure Nominal Ready *)
    bPneumatics_MainAir_OK_In        : BOOL; (* Machine Shop Compressed Air Main Supply Nominal Ready (6.5 bar) *)
    bCNC_Cycle_Start_In              : BOOL; (* CNC Interpolation Kernel Automatic Cycle Run Enable Command *)
    bCNC_Feed_Hold_In                : BOOL; (* CNC Interpolation Kernel Active Feed Hold Pause Command *)
    bManual_Fault_Reset_In           : BOOL; (* Operator HMI Latched Fault and Alarm Manual Reset Pushbutton *)
    bSpindle_Warmup_Select_In        : BOOL; (* Spindle Daily Thermal Warm-up Cycle Sequence Enable *)
    bActive_Damping_Enable_In        : BOOL; (* Real-Time Active Chatter Vibration Magnetic Damping Loop Enable *)
    bSSM_Chatter_Enable_In           : BOOL; (* Spindle Speed Modulation (SSM) Dynamic Chatter Disruption Enable *)
    bThermal_Comp_Enable_In          : BOOL; (* High-Speed Piezo Dynamic Thermal Growth Compensation Loop Enable *)
    bTool_Change_Request_In          : BOOL; (* Automatic Tool Changer (ATC) Carousel Tool Swap Request Pulse *)
    bPartProgram_M30_End_In          : BOOL; (* CNC Part Program Execution Completed (M30 End of Program) *)
END_VAR
""")

    # -------------------------------------------------------------------------
    # 3. VAR_OUTPUT BLOCK
    # -------------------------------------------------------------------------
    st.append("""VAR_OUTPUT
    (* =================================================================================================================
     * REAL-TIME ACTUATOR COMMAND SETPOINTS & SERVO MODULATION SIGNALS
     * ================================================================================================================= *)
    rMaster_X_Torque_Cmd_Out     : REAL;    (* Master X1-Axis Gantry Servo Motor Torque Bias Command [%] [0.0..100.0] *)
    rSlave_X_Torque_Cmd_Out      : REAL;    (* Slave X2-Axis Gantry Servo Motor Torque Bias Command [%] [0.0..100.0] *)
    rSpindleSpeed_Trim_Cmd_Out   : REAL;    (* High-Speed Spindle Speed Command Modulated Trim [%] [-15.0..+15.0] *)
    rSpindleSpeed_Direct_Cmd_Out : REAL;    (* Spindle Inverter High-Speed Servo Final Frequency Setpoint [rpm] *)
    rPiezo_Z_Thermal_Offset_Out  : REAL;    (* Piezo-Electric Micro-Actuator Dynamic Z-Offset Stroke Command [um] [-50.0..+50.0] *)
    rCoolant_PropValve_Cmd_Out   : REAL;    (* Through-Spindle Coolant Proportional Flow Throttle Valve Position [%] [0.0..100.0] *)
    rActiveDamping_Bias_Cmd_Out  : REAL;    (* Active Magnetic Bearing / Piezo Counter-Force Damping Bias Command [%] [0.0..100.0] *)
    rZ_Axis_CNC_Origin_Shift_Out : REAL;    (* CNC Coordinate System Z-Axis Dynamic Thermal Origin Offset [mm] *)
    rSpindleBrake_Torque_Cmd_Out : REAL;    (* Spindle Servo Dynamic Braking Torque Command [%] [0.0..100.0] *)
    rDrawbarCylinder_Cmd_Out     : REAL;    (* HSK-A63 Tool Clamping Hydraulic Drawbar Valve Command [%] [0.0..100.0] *)

    (* =================================================================================================================
     * DISCRETE PROCESS STATUS, INTERLOCKS & HANDSHAKE FLAGS
     * ================================================================================================================= *)
    bMachine_Ready_Out           : BOOL;    (* 5-Axis Gantry Machining Center Interlocks Satisfied and Ready for Cut *)
    bSpindle_At_Speed_Out        : BOOL;    (* Spindle Motor Rotational Speed Settled Within Tolerance Window *)
    bChatter_Suppression_Active_Out : BOOL; (* Active Magnetic Damping and SSM Modulation Actively Attenuating Chatter *)
    bThermal_Comp_Active_Out     : BOOL;    (* Real-Time Spindle Piezo Thermal Growth Dynamic Compensation Active *)
    bGantry_Skew_Corrected_Out   : BOOL;    (* Master-Slave Gantry Dual Drive Anti-Skew Skew Error Nullified (< 1.5 um) *)
    bTool_Broken_Tripped_Out     : BOOL;    (* Ultra-Fast Tool Fracture / Collision Crash Detected, Z-Retract Engaged *)
    bATC_Cycle_Complete_Out      : BOOL;    (* Automatic Tool Changer Tool Swap Sequence Completed Successfully *)
    bEmergency_Retract_Active_Out: BOOL;    (* Machine Ram Rapid Emergency Z-Axis Upward Retraction in Progress *)
    bGeneral_Fault_Alarm_Out     : BOOL;    (* Master Machine Fault Trip Latched - Process Execution Halted *)
    bSpindle_Oriented_Out        : BOOL;    (* Spindle Precision Spindle Shaft Orientation Angle Locked (0.0 deg) *)

    (* =================================================================================================================
     * CYBER-PHYSICAL STATE ESTIMATIONS & PROCESS TELEMETRY
     * ================================================================================================================= *)
    rEstimated_Z_Elongation_Out  : REAL;    (* Observer Estimated Spindle Nose Z-Axis Thermal Elongation [um] *)
    rEstimated_TCP_Vibration_Out : REAL;    (* Observer Estimated Tool Center Point (TCP) Chatter Vibration [m/s2] *)
    rEstimated_Dynamic_Force_Out : REAL;    (* Observer Estimated Dynamic Cutting Force Magnitude [N] *)
    rGantry_Skew_Error_Out       : REAL;    (* Instantaneous Voted Master-Slave Gantry Linear Skew Error [um] *)
    rSpindle_Bearing_Temp_Out    : REAL;    (* Instantaneous Voted Spindle Front Hybrid Bearing Temperature [deg C] *)
    rSpindle_Torque_Actual_Out   : REAL;    (* Measured Instantaneous Spindle Electro-Mechanical Driving Torque [Nm] *)
    iFSM_Current_State_Out       : INT;     (* Current Deterministic 14-Stage Production State Machine Step [0..13] *)

    (* =================================================================================================================
     * BIT-PACKED 32-BIT INDUSTRIAL TELEMETRY & ALARM STATUS WORDS
     * ================================================================================================================= *)
    dwStatusWord1_Out            : DWORD;   (* Primary Subsystem Operational Status & Actuator State Telemetry Bitfield *)
    dwStatusWord2_Out            : DWORD;   (* Secondary Sensor Health, TMR Degradation & Damping Subsystem Bitfield *)
    dwAlarmWord1_Out             : DWORD;   (* ISA-18.2 Priority 1 & 2 Critical Safety Trip & Hardware Fault Bitfield *)
    dwAlarmWord2_Out             : DWORD;   (* ISA-18.2 Priority 3 & 4 Operational Warnings & Quality Limit Bitfield *)
    dwFirstOutWord_Out           : DWORD;   (* Deterministic First-Out Root-Cause Alarm Sequence Identifier Bitfield *)
END_VAR
""")

    # -------------------------------------------------------------------------
    # 4. VAR BLOCK (INTERNAL MATRICES, ARRAYS, BUFFERS, TIMERS, LIMITS)
    # -------------------------------------------------------------------------
    st.append("""VAR
    (* =================================================================================================================
     * CYBER-PHYSICAL DISCRETE STATE-SPACE MODEL MATRICES (Ts = 1.0 ms)
     * States:
     *   x1: Gantry Master-Slave Linear Skew Error [um]
     *   x2: Spindle Forward Bearing Temperature [deg C]
     *   x3: Spindle Rear Bearing Temperature [deg C]
     *   x4: Spindle Z-Axis Dynamic Thermal Elongation [um]
     *   x5: Tool Center Point (TCP) Chatter Vibration Acceleration [m/s2]
     *   x6: Milling Dynamic Cutting Force Magnitude [N]
     *   x7: High-Speed Spindle Electro-Mechanical Driving Torque [Nm]
     *   x8: Machine Column Differential Thermal Gradient [deg C]
     * Actuators:
     *   u1: Master X-axis Servo Torque Bias [%]
     *   u2: Slave X-axis Servo Torque Bias [%]
     *   u3: Spindle Speed Trim [%]
     *   u4: Z-Axis Thermal Piezo Offset [um]
     *   u5: Through-Spindle Coolant Proportional Valve [%]
     *   u6: Active Magnetic Bearing / Piezo Damping Bias [%]
     * ================================================================================================================= *)
    rA_mat : ARRAY[1..8, 1..8] OF REAL; (* Discrete System State Transition Matrix A (8x8) [unitless] *)
    rB_mat : ARRAY[1..8, 1..6] OF REAL; (* Discrete Actuator Control Input Coupling Matrix B (8x6) [var/unit] *)
    rC_mat : ARRAY[1..6, 1..8] OF REAL; (* Discrete Output Measurement Observation Matrix C (6x8) [var/state] *)
    rD_mat : ARRAY[1..6, 1..6] OF REAL; (* Discrete Direct Feedthrough Transmission Matrix D (6x6) [var/input] *)
    rL_obs : ARRAY[1..8, 1..6] OF REAL; (* Steady-State Luenberger/Kalman Innovation Observer Gain Matrix L (8x6) *)

    (* State vectors and internal estimator signals *)
    rX_hat   : ARRAY[1..8] OF REAL;    (* Current Time Step Observer Estimated State Vector x_hat[k] *)
    rX_next  : ARRAY[1..8] OF REAL;    (* Next Time Step Predicted State Vector x_hat[k+1] *)
    rY_meas  : ARRAY[1..6] OF REAL;    (* Voted Instrumentation Measurement Vector y[k] *)
    rY_hat   : ARRAY[1..6] OF REAL;    (* Observer Reconstructed Output Vector y_hat[k] = C*x_hat + D*u *)
    rE_innov : ARRAY[1..6] OF REAL;    (* Innovation Residual Error Vector e_innov[k] = y_meas - y_hat *)
    rU_act   : ARRAY[1..6] OF REAL;    (* Effective Actuator Command Vector Applied at Current Cycle u[k] *)
    rU_prev  : ARRAY[1..6] OF REAL;    (* Previous Cycle Actuator Vector u[k-1] for Dynamic Slew Rate Clamping *)

    (* Matrices initialization flag *)
    bMatrices_Initialized : BOOL := FALSE;

    (* =================================================================================================================
     * RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) & PROJECTED GRADIENT DESCENT (PGD)
     * ================================================================================================================= *)
    rQ_cost         : ARRAY[1..8] OF REAL;  (* State Tracking Quadratic Error Penalty Diagonal Weights *)
    rR_cost         : ARRAY[1..6] OF REAL;  (* Actuator Control Effort Deviation Penalty Diagonal Weights *)
    rP_cost         : ARRAY[1..8] OF REAL;  (* Terminal State Quadratic Penalty Diagonal Weights *)
    rX_pred         : ARRAY[0..5, 1..8] OF REAL; (* Forward Predicted State Trajectory across Horizon N=5 *)
    rU_cand         : ARRAY[0..4, 1..6] OF REAL; (* Candidate Actuator Trajectory across Horizon N=5 *)
    rX_ref          : ARRAY[0..5, 1..8] OF REAL; (* Dynamic State Target Reference Trajectory across Horizon N=5 *)
    rU_ref          : ARRAY[0..4, 1..6] OF REAL; (* Nominal Actuator Target Reference Trajectory across Horizon N=5 *)
    rLambda_costate : ARRAY[0..5, 1..8] OF REAL; (* Backward Propagated Adjoint Costate Vector Trajectory *)
    rGrad_U         : ARRAY[0..4, 1..6] OF REAL; (* Analytical Gradient Vector dJ/du across Control Horizon *)

    rU_min          : ARRAY[1..6] OF REAL;  (* Actuator Lower Physical Saturation Bounds *)
    rU_max          : ARRAY[1..6] OF REAL;  (* Actuator Upper Physical Saturation Bounds *)
    rSlew_max       : ARRAY[1..6] OF REAL;  (* Maximum Actuator Slew Rate Limit per Scan Cycle [units/ms] *)
    rAlpha_PGD      : REAL := 0.0125;       (* Projected Gradient Descent Numerical Optimization Step Size *)

    (* Loop index iterators *)
    iHorizIdx       : INT;
    iIterIdx        : INT;
    iStateIdx       : INT;
    iActIdx         : INT;
    iMeasIdx        : INT;
    jStateIdx       : INT;
    jActIdx         : INT;

    (* =================================================================================================================
     * SPINDLE SPEED MODULATION (SSM) REGENERATIVE CHATTER ATTENUATION
     * ================================================================================================================= *)
    rSSM_Phase           : REAL := 0.0;    (* Modulation Generator Sinusoidal Phase Accumulator [rad] *)
    rSSM_Freq            : REAL := 2.85;   (* Chatter Disruption Modulation Frequency fm [Hz] *)
    rSSM_RVA             : REAL := 0.12;   (* Relative Velocity Amplitude (12% perturbation) [dimensionless] *)
    rSSM_Modulation_Trim : REAL := 0.0;    (* Instantaneous Modulated Spindle Speed Trim Output [%] *)
    rSSM_Perturbation_RPM: REAL := 0.0;    (* Instantaneous RPM Perturbation Value Added to Spindle Setpoint [rpm] *)
    rPi_Constant         : REAL := 3.14159265358979; (* Mathematical Constant Pi *)

    (* =================================================================================================================
     * MASTER-SLAVE GANTRY SKEW PROPORTIONAL-DERIVATIVE CANCELLATION
     * ================================================================================================================= *)
    rSkew_Kp             : REAL := 1.85;   (* Proportional Skew Feedback Correction Gain [%/um] *)
    rSkew_Kd             : REAL := 0.065;  (* Derivative Skew Feedback Correction Gain [%/(um/ms)] *)
    rSkew_Error_Prev     : REAL := 0.0;    (* Previous Cycle Skew Error for Numerical Backward Difference [um] *)
    rSkew_Delta_Torque   : REAL := 0.0;    (* Master-Slave Differential Servo Torque Bias Command [%] *)

    (* =================================================================================================================
     * TRIPLE MODULAR REDUNDANCY (2oo3 TMR) INTERNAL VOTING & DEGRADATION STRUCTURES
     * ================================================================================================================= *)
    (* Channel 1: Gantry Linear Scales ST-SCALE-101 *)
    rTMR_Scale101_Voted       : REAL;
    rTMR_Scale101_Prev        : REAL;
    bTMR_Scale101_FaultA      : BOOL;
    bTMR_Scale101_FaultB      : BOOL;
    bTMR_Scale101_FaultC      : BOOL;
    rTMR_Scale101_TimerAB     : REAL;
    rTMR_Scale101_TimerBC     : REAL;
    rTMR_Scale101_TimerCA     : REAL;
    iTMR_Scale101_DegradeMode : INT := 3; (* 3: Normal 3oo3, 2: Dual 2oo3, 1: Single Fallback, 0: Faulted *)
    bAlarm_TMR_Scale101_Discr : BOOL;

    (* Channel 2: Spindle Front Bearing RTDs TT-BEAR-201 *)
    rTMR_Bear201_Voted        : REAL;
    rTMR_Bear201_Prev         : REAL;
    bTMR_Bear201_FaultA       : BOOL;
    bTMR_Bear201_FaultB       : BOOL;
    bTMR_Bear201_FaultC       : BOOL;
    rTMR_Bear201_TimerAB      : REAL;
    rTMR_Bear201_TimerBC      : REAL;
    rTMR_Bear201_TimerCA      : REAL;
    iTMR_Bear201_DegradeMode  : INT := 3;
    bAlarm_TMR_Bear201_Discr  : BOOL;

    (* Channel 3: Spindle Nose Eddy-Current Displacement DT-SPINDLE-301 *)
    rTMR_Disp301_Voted        : REAL;
    rTMR_Disp301_Prev         : REAL;
    bTMR_Disp301_FaultA       : BOOL;
    bTMR_Disp301_FaultB       : BOOL;
    bTMR_Disp301_FaultC       : BOOL;
    rTMR_Disp301_TimerAB      : REAL;
    rTMR_Disp301_TimerBC      : REAL;
    rTMR_Disp301_TimerCA      : REAL;
    iTMR_Disp301_DegradeMode  : INT := 3;
    bAlarm_TMR_Disp301_Discr  : BOOL;

    (* Channel 4: Tool Head Triaxial Accelerometers AT-CHATTER-401 *)
    rTMR_Chatter401_Voted     : REAL;
    rTMR_Chatter401_Prev      : REAL;
    bTMR_Chatter401_FaultA    : BOOL;
    bTMR_Chatter401_FaultB    : BOOL;
    bTMR_Chatter401_FaultC    : BOOL;
    rTMR_Chatter401_TimerAB   : REAL;
    rTMR_Chatter401_TimerBC   : REAL;
    rTMR_Chatter401_TimerCA   : REAL;
    iTMR_Chatter401_DegradeMode: INT := 3;
    bAlarm_TMR_Chatter401_Discr: BOOL;

    (* Channel 5: Spindle Motor Current Sensors IT-CURRENT-501 *)
    rTMR_Current501_Voted     : REAL;
    rTMR_Current501_Prev      : REAL;
    bTMR_Current501_FaultA    : BOOL;
    bTMR_Current501_FaultB    : BOOL;
    bTMR_Current501_FaultC    : BOOL;
    rTMR_Current501_TimerAB   : REAL;
    rTMR_Current501_TimerBC   : REAL;
    rTMR_Current501_TimerCA   : REAL;
    iTMR_Current501_DegradeMode: INT := 3;
    bAlarm_TMR_Current501_Discr: BOOL;

    (* Discrepancy threshold parameters and debounce time *)
    rDiscrTol_Scale101        : REAL := 5.0;    (* Discrepancy Tolerance for Gantry Scales [um] *)
    rDiscrTol_Bear201         : REAL := 3.5;    (* Discrepancy Tolerance for Bearing Temp [deg C] *)
    rDiscrTol_Disp301         : REAL := 4.0;    (* Discrepancy Tolerance for Spindle Nose Displacement [um] *)
    rDiscrTol_Chatter401      : REAL := 12.0;   (* Discrepancy Tolerance for Chatter Accelerometer [m/s2] *)
    rDiscrTol_Current501      : REAL := 8.5;    (* Discrepancy Tolerance for Motor Current [A] *)
    rDiscrepancy_Limit_ms     : REAL := 100.0;  (* Continuous Discrepancy Trip Accumulation Window [ms] *)

    (* =================================================================================================================
     * DETERMINISTIC 14-STAGE PRODUCTION FINITE STATE MACHINE (FSM)
     * ================================================================================================================= *)
    eState               : INT := 0;       (* Active Operating Stage [0..13] *)
    ePrevState           : INT := -1;      (* Previous Operating Stage for Edge Detection *)
    tStateTimer          : REAL := 0.0;    (* Continuous Elapsed Time Accumulated in Active State [ms] *)
    tWarmupTimer         : REAL := 0.0;    (* Progressive Thermal Spindle Warmup Execution Timer [ms] *)
    tToolProbeTimer      : REAL := 0.0;    (* Laser Tool Setter Touch Probe Kinematic Calibration Settle Timer [ms] *)
    tDatumScanTimer      : REAL := 0.0;    (* 3D Workpiece Datum Optical Measurement Settle Timer [ms] *)
    tGantrySquareTimer   : REAL := 0.0;    (* Master-Slave Gantry Active Mechanical Squaring Timer [ms] *)
    tSpindleRampTimer    : REAL := 0.0;    (* Spindle Speed Dynamic Acceleration Settle Timer [ms] *)
    tCoolantLockTimer    : REAL := 0.0;    (* High-Pressure Coolant Header Pressure Stabilization Timer [ms] *)
    tMillingElapsedTimer : REAL := 0.0;    (* High-Speed 5-Axis Milling Block Execution Timer [ms] *)
    tWearAcousticTimer   : REAL := 0.0;    (* Acoustic In-Process Tool Wear Evaluation Settle Timer [ms] *)
    tSpindleDecelTimer   : REAL := 0.0;    (* Spindle Regenerative Braking and Angular Orientation Timer [ms] *)
    tATCSwapTimer        : REAL := 0.0;    (* Automatic Tool Changer Mechanical Arm Carousel Swap Timer [ms] *)
    tEmergencyRetractTimer : REAL := 0.0;  (* Ultra-Fast Z-Axis Rapid Retraction Motion Timer [ms] *)
    bStateInitialized    : BOOL := FALSE;  (* State Initial Scan Entry Flag *)

    (* Active tooling and wear management tables *)
    iToolCurrentID       : INT := 1;       (* Active Spindle Loaded Tool Holder ID [1..120] *)
    rToolLength_Offset   : ARRAY[1..120] OF REAL; (* Tool Length Dynamic Wear Offsets [mm] *)
    rToolRadius_Offset   : ARRAY[1..120] OF REAL; (* Tool Radius Dynamic Wear Offsets [mm] *)
    rToolLife_Elapsed_Min: ARRAY[1..120] OF REAL; (* Accumulated Tool Cutting Contact Duration [min] *)
    bToolWearLimitTrip   : BOOL;           (* Tool Flank Wear Exceeded Permissible Criterion *)

    (* =================================================================================================================
     * FAST TOOL FRACTURE & COLLISION IMPACT DETECTION (< 1.0 ms RESPONSE)
     * ================================================================================================================= *)
    rTorque_History      : ARRAY[0..4] OF REAL; (* Fast 5-Tap Rolling FIFO Spindle Torque Buffer [Nm] *)
    rAccel_History       : ARRAY[0..4] OF REAL; (* Fast 5-Tap Rolling FIFO Chatter Acceleration Buffer [m/s2] *)
    rTorque_Drop_Rate    : REAL := 0.0;    (* Instantaneous Rate of Spindle Torque Collapse [Nm/ms] *)
    rAccel_Spike_Rate    : REAL := 0.0;    (* Instantaneous Rate of Tool Head Kinetic Impact Spike [m/s2/ms] *)
    bFastToolBreak_Trip  : BOOL := FALSE;  (* Latched Tool Fracture Trip Flag *)
    bFastCollision_Trip  : BOOL := FALSE;  (* Latched Machine Axis Collision Impact Flag *)

    (* =================================================================================================================
     * ISA-18.2 MULTI-TIER PROCESS ALARM THRESHOLDS & CLEARANCE DEADBANDS
     * ================================================================================================================= *)
    (* Variable 1: Gantry Linear Skew Error [um] *)
    rLim_Skew_HH         : REAL := 15.0;
    rLim_Skew_H          : REAL := 8.0;
    rLim_Skew_L          : REAL := -8.0;
    rLim_Skew_LL         : REAL := -15.0;
    rDeadband_Skew       : REAL := 1.2;

    (* Variable 2: Spindle Front Bearing Temp [deg C] *)
    rLim_Bear201_HH      : REAL := 68.0;
    rLim_Bear201_H       : REAL := 55.0;
    rLim_Bear201_L       : REAL := 18.0;
    rLim_Bear201_LL      : REAL := 10.0;
    rDeadband_Bear201    : REAL := 2.0;

    (* Variable 3: Spindle Rear Bearing Temp [deg C] *)
    rLim_Bear202_HH      : REAL := 72.0;
    rLim_Bear202_H       : REAL := 58.0;
    rLim_Bear202_L       : REAL := 18.0;
    rLim_Bear202_LL      : REAL := 10.0;
    rDeadband_Bear202    : REAL := 2.0;

    (* Variable 4: Spindle Z-Axis Thermal Elongation [um] *)
    rLim_ZElong_HH       : REAL := 45.0;
    rLim_ZElong_H        : REAL := 25.0;
    rLim_ZElong_L        : REAL := -25.0;
    rLim_ZElong_LL       : REAL := -45.0;
    rDeadband_ZElong     : REAL := 3.0;

    (* Variable 5: Tool Center Point Chatter Vibration [m/s2] *)
    rLim_Chatter_HH      : REAL := 65.0;
    rLim_Chatter_H       : REAL := 32.0;
    rLim_Chatter_L       : REAL := 0.2;
    rLim_Chatter_LL      : REAL := 0.05;
    rDeadband_Chatter    : REAL := 2.5;

    (* Variable 6: Dynamic Cutting Force Magnitude [N] *)
    rLim_CutForce_HH     : REAL := 4800.0;
    rLim_CutForce_H      : REAL := 3200.0;
    rLim_CutForce_L      : REAL := 100.0;
    rLim_CutForce_LL     : REAL := 20.0;
    rDeadband_CutForce   : REAL := 80.0;

    (* Variable 7: Spindle Motor Current [A] *)
    rLim_Current_HH      : REAL := 95.0;
    rLim_Current_H       : REAL := 75.0;
    rLim_Current_L       : REAL := 4.0;
    rLim_Current_LL      : REAL := 1.0;
    rDeadband_Current    : REAL := 3.0;

    (* Variable 8: Through-Spindle Coolant Delivery Pressure [bar] *)
    rLim_CoolPres_HH     : REAL := 85.0;
    rLim_CoolPres_H      : REAL := 75.0;
    rLim_CoolPres_L      : REAL := 45.0;
    rLim_CoolPres_LL     : REAL := 25.0;
    rDeadband_CoolPres   : REAL := 3.0;

    (* Variable 9: Bearing Oil-Air Lubrication Pressure [bar] *)
    rLim_OilMist_HH      : REAL := 4.8;
    rLim_OilMist_H       : REAL := 4.2;
    rLim_OilMist_L       : REAL := 2.5;
    rLim_OilMist_LL      : REAL := 1.8;
    rDeadband_OilMist    : REAL := 0.2;

    (* Alarm output state latches *)
    bAlarm_Skew_HH_Latched     : BOOL := FALSE;
    bAlarm_Skew_H_Latched      : BOOL := FALSE;
    bAlarm_Bear201_HH_Latched  : BOOL := FALSE;
    bAlarm_Bear201_H_Latched   : BOOL := FALSE;
    bAlarm_Bear202_HH_Latched  : BOOL := FALSE;
    bAlarm_Bear202_H_Latched   : BOOL := FALSE;
    bAlarm_ZElong_HH_Latched   : BOOL := FALSE;
    bAlarm_ZElong_H_Latched    : BOOL := FALSE;
    bAlarm_Chatter_HH_Latched  : BOOL := FALSE;
    bAlarm_Chatter_H_Latched   : BOOL := FALSE;
    bAlarm_CutForce_HH_Latched : BOOL := FALSE;
    bAlarm_CutForce_H_Latched  : BOOL := FALSE;
    bAlarm_Current_HH_Latched  : BOOL := FALSE;
    bAlarm_Current_H_Latched   : BOOL := FALSE;
    bAlarm_CoolPres_LL_Latched : BOOL := FALSE;
    bAlarm_CoolPres_L_Latched  : BOOL := FALSE;
    bAlarm_OilMist_LL_Latched  : BOOL := FALSE;
    bAlarm_OilMist_L_Latched   : BOOL := FALSE;

    (* Deterministic First-Out Alarm sequence identification *)
    iFirstOutID          : INT := 0;
    bFirstOutLatched     : BOOL := FALSE;

    (* Temporary mathematical calculation registers *)
    rTempCalc1           : REAL := 0.0;
    rTempCalc2           : REAL := 0.0;
    rTempCalc3           : REAL := 0.0;
    rSumVal              : REAL := 0.0;
    rDiffVal             : REAL := 0.0;
END_VAR
""")

    # -------------------------------------------------------------------------
    # 5. PHASE 1: 2oo3 TMR SENSOR VOTING WITH DYNAMIC DISCREPANCY TIMERS
    # -------------------------------------------------------------------------
    st.append("""
(* =====================================================================================================================
 * PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING WITH DYNAMIC DISCREPANCY TIMERS
 * Scan-by-scan cross-channel verification across 5 critical closed-loop process and safety channels:
 *   1. Dual Gantry Absolute Linear Scale Encoders (ST-SCALE-101A/B/C) [um]
 *   2. Spindle Front Hybrid Ceramic Bearing Pt100 RTDs (TT-BEAR-201A/B/C) [deg C]
 *   3. Spindle Nose Non-Contact Eddy-Current Proximity Sensors (DT-SPINDLE-301A/B/C) [um]
 *   4. Tool Head Triaxial High-Frequency Accelerometers (AT-CHATTER-401A/B/C) [m/s2]
 *   5. Spindle Motor High-Bandwidth Phase Current Transducers (IT-CURRENT-501A/B/C) [A]
 * Each channel features 100 ms discrepancy integration, fault channel latching, and 4-tier bumpless degradation:
 *   Mode 3: Full 3-channel health (median selection)
 *   Mode 2: 1 channel faulty (average of 2 healthy channels)
 *   Mode 1: 2 channels faulty (fallback to single channel with advisory alarm)
 *   Mode 0: 3 channels faulty (fail-safe trip, hold last valid, trigger emergency stop)
 * ===================================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------------------------
 * CHANNEL 1: ST-SCALE-101 DUAL GANTRY ABSOLUTE LINEAR SCALE ENCODERS (SKEW [um])
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Pairwise absolute discrepancy comparisons *)
IF ABS(rGantrySkew_Scale101A_In - rGantrySkew_Scale101B_In) > rDiscrTol_Scale101 THEN
    rTMR_Scale101_TimerAB := rTMR_Scale101_TimerAB + 1.0;
ELSE
    IF rTMR_Scale101_TimerAB > 0.0 THEN
        rTMR_Scale101_TimerAB := rTMR_Scale101_TimerAB - 0.5;
    END_IF;
END_IF;

IF ABS(rGantrySkew_Scale101B_In - rGantrySkew_Scale101C_In) > rDiscrTol_Scale101 THEN
    rTMR_Scale101_TimerBC := rTMR_Scale101_TimerBC + 1.0;
ELSE
    IF rTMR_Scale101_TimerBC > 0.0 THEN
        rTMR_Scale101_TimerBC := rTMR_Scale101_TimerBC - 0.5;
    END_IF;
END_IF;

IF ABS(rGantrySkew_Scale101A_In - rGantrySkew_Scale101C_In) > rDiscrTol_Scale101 THEN
    rTMR_Scale101_TimerCA := rTMR_Scale101_TimerCA + 1.0;
ELSE
    IF rTMR_Scale101_TimerCA > 0.0 THEN
        rTMR_Scale101_TimerCA := rTMR_Scale101_TimerCA - 0.5;
    END_IF;
END_IF;

(* Channel fault isolation based on discrepancy timers exceeding threshold *)
IF (rTMR_Scale101_TimerAB >= rDiscrepancy_Limit_ms) AND (rTMR_Scale101_TimerCA >= rDiscrepancy_Limit_ms) THEN
    bTMR_Scale101_FaultA := TRUE;
END_IF;
IF (rTMR_Scale101_TimerAB >= rDiscrepancy_Limit_ms) AND (rTMR_Scale101_TimerBC >= rDiscrepancy_Limit_ms) THEN
    bTMR_Scale101_FaultB := TRUE;
END_IF;
IF (rTMR_Scale101_TimerBC >= rDiscrepancy_Limit_ms) AND (rTMR_Scale101_TimerCA >= rDiscrepancy_Limit_ms) THEN
    bTMR_Scale101_FaultC := TRUE;
END_IF;

(* Multi-tier voting and degradation logic *)
IF (NOT bTMR_Scale101_FaultA) AND (NOT bTMR_Scale101_FaultB) AND (NOT bTMR_Scale101_FaultC) THEN
    (* 3oo3 Median voting *)
    iTMR_Scale101_DegradeMode := 3;
    bAlarm_TMR_Scale101_Discr := FALSE;
    IF ((rGantrySkew_Scale101A_In >= rGantrySkew_Scale101B_In) AND (rGantrySkew_Scale101A_In <= rGantrySkew_Scale101C_In)) OR
       ((rGantrySkew_Scale101A_In <= rGantrySkew_Scale101B_In) AND (rGantrySkew_Scale101A_In >= rGantrySkew_Scale101C_In)) THEN
        rTMR_Scale101_Voted := rGantrySkew_Scale101A_In;
    ELSIF ((rGantrySkew_Scale101B_In >= rGantrySkew_Scale101A_In) AND (rGantrySkew_Scale101B_In <= rGantrySkew_Scale101C_In)) OR
          ((rGantrySkew_Scale101B_In <= rGantrySkew_Scale101A_In) AND (rGantrySkew_Scale101B_In >= rGantrySkew_Scale101C_In)) THEN
        rTMR_Scale101_Voted := rGantrySkew_Scale101B_In;
    ELSE
        rTMR_Scale101_Voted := rGantrySkew_Scale101C_In;
    END_IF;
ELSIF bTMR_Scale101_FaultA AND (NOT bTMR_Scale101_FaultB) AND (NOT bTMR_Scale101_FaultC) THEN
    (* Dual voting: Average B and C *)
    iTMR_Scale101_DegradeMode := 2;
    bAlarm_TMR_Scale101_Discr := TRUE;
    rTMR_Scale101_Voted := (rGantrySkew_Scale101B_In + rGantrySkew_Scale101C_In) * 0.5;
ELSIF (NOT bTMR_Scale101_FaultA) AND bTMR_Scale101_FaultB AND (NOT bTMR_Scale101_FaultC) THEN
    (* Dual voting: Average A and C *)
    iTMR_Scale101_DegradeMode := 2;
    bAlarm_TMR_Scale101_Discr := TRUE;
    rTMR_Scale101_Voted := (rGantrySkew_Scale101A_In + rGantrySkew_Scale101C_In) * 0.5;
ELSIF (NOT bTMR_Scale101_FaultA) AND (NOT bTMR_Scale101_FaultB) AND bTMR_Scale101_FaultC THEN
    (* Dual voting: Average A and B *)
    iTMR_Scale101_DegradeMode := 2;
    bAlarm_TMR_Scale101_Discr := TRUE;
    rTMR_Scale101_Voted := (rGantrySkew_Scale101A_In + rGantrySkew_Scale101B_In) * 0.5;
ELSIF (NOT bTMR_Scale101_FaultA) AND bTMR_Scale101_FaultB AND bTMR_Scale101_FaultC THEN
    (* Single surviving channel A *)
    iTMR_Scale101_DegradeMode := 1;
    bAlarm_TMR_Scale101_Discr := TRUE;
    rTMR_Scale101_Voted := rGantrySkew_Scale101A_In;
ELSIF bTMR_Scale101_FaultA AND (NOT bTMR_Scale101_FaultB) AND bTMR_Scale101_FaultC THEN
    (* Single surviving channel B *)
    iTMR_Scale101_DegradeMode := 1;
    bAlarm_TMR_Scale101_Discr := TRUE;
    rTMR_Scale101_Voted := rGantrySkew_Scale101B_In;
ELSIF bTMR_Scale101_FaultA AND bTMR_Scale101_FaultB AND (NOT bTMR_Scale101_FaultC) THEN
    (* Single surviving channel C *)
    iTMR_Scale101_DegradeMode := 1;
    bAlarm_TMR_Scale101_Discr := TRUE;
    rTMR_Scale101_Voted := rGantrySkew_Scale101C_In;
ELSE
    (* All channels faulted: Hold last valid and trigger fail-safe *)
    iTMR_Scale101_DegradeMode := 0;
    bAlarm_TMR_Scale101_Discr := TRUE;
    rTMR_Scale101_Voted := rTMR_Scale101_Prev;
END_IF;
rTMR_Scale101_Prev := rTMR_Scale101_Voted;

(* ---------------------------------------------------------------------------------------------------------------------
 * CHANNEL 2: TT-BEAR-201 SPINDLE FRONT CERAMIC BEARING RTDS (TEMPERATURE [deg C])
 * --------------------------------------------------------------------------------------------------------------------- *)
IF ABS(rSpindleTemp_TT201A_In - rSpindleTemp_TT201B_In) > rDiscrTol_Bear201 THEN
    rTMR_Bear201_TimerAB := rTMR_Bear201_TimerAB + 1.0;
ELSE
    IF rTMR_Bear201_TimerAB > 0.0 THEN
        rTMR_Bear201_TimerAB := rTMR_Bear201_TimerAB - 0.5;
    END_IF;
END_IF;

IF ABS(rSpindleTemp_TT201B_In - rSpindleTemp_TT201C_In) > rDiscrTol_Bear201 THEN
    rTMR_Bear201_TimerBC := rTMR_Bear201_TimerBC + 1.0;
ELSE
    IF rTMR_Bear201_TimerBC > 0.0 THEN
        rTMR_Bear201_TimerBC := rTMR_Bear201_TimerBC - 0.5;
    END_IF;
END_IF;

IF ABS(rSpindleTemp_TT201A_In - rSpindleTemp_TT201C_In) > rDiscrTol_Bear201 THEN
    rTMR_Bear201_TimerCA := rTMR_Bear201_TimerCA + 1.0;
ELSE
    IF rTMR_Bear201_TimerCA > 0.0 THEN
        rTMR_Bear201_TimerCA := rTMR_Bear201_TimerCA - 0.5;
    END_IF;
END_IF;

IF (rTMR_Bear201_TimerAB >= rDiscrepancy_Limit_ms) AND (rTMR_Bear201_TimerCA >= rDiscrepancy_Limit_ms) THEN
    bTMR_Bear201_FaultA := TRUE;
END_IF;
IF (rTMR_Bear201_TimerAB >= rDiscrepancy_Limit_ms) AND (rTMR_Bear201_TimerBC >= rDiscrepancy_Limit_ms) THEN
    bTMR_Bear201_FaultB := TRUE;
END_IF;
IF (rTMR_Bear201_TimerBC >= rDiscrepancy_Limit_ms) AND (rTMR_Bear201_TimerCA >= rDiscrepancy_Limit_ms) THEN
    bTMR_Bear201_FaultC := TRUE;
END_IF;

IF (NOT bTMR_Bear201_FaultA) AND (NOT bTMR_Bear201_FaultB) AND (NOT bTMR_Bear201_FaultC) THEN
    iTMR_Bear201_DegradeMode := 3;
    bAlarm_TMR_Bear201_Discr := FALSE;
    IF ((rSpindleTemp_TT201A_In >= rSpindleTemp_TT201B_In) AND (rSpindleTemp_TT201A_In <= rSpindleTemp_TT201C_In)) OR
       ((rSpindleTemp_TT201A_In <= rSpindleTemp_TT201B_In) AND (rSpindleTemp_TT201A_In >= rSpindleTemp_TT201C_In)) THEN
        rTMR_Bear201_Voted := rSpindleTemp_TT201A_In;
    ELSIF ((rSpindleTemp_TT201B_In >= rSpindleTemp_TT201A_In) AND (rSpindleTemp_TT201B_In <= rSpindleTemp_TT201C_In)) OR
          ((rSpindleTemp_TT201B_In <= rSpindleTemp_TT201A_In) AND (rSpindleTemp_TT201B_In >= rSpindleTemp_TT201C_In)) THEN
        rTMR_Bear201_Voted := rSpindleTemp_TT201B_In;
    ELSE
        rTMR_Bear201_Voted := rSpindleTemp_TT201C_In;
    END_IF;
ELSIF bTMR_Bear201_FaultA AND (NOT bTMR_Bear201_FaultB) AND (NOT bTMR_Bear201_FaultC) THEN
    iTMR_Bear201_DegradeMode := 2;
    bAlarm_TMR_Bear201_Discr := TRUE;
    rTMR_Bear201_Voted := (rSpindleTemp_TT201B_In + rSpindleTemp_TT201C_In) * 0.5;
ELSIF (NOT bTMR_Bear201_FaultA) AND bTMR_Bear201_FaultB AND (NOT bTMR_Bear201_FaultC) THEN
    iTMR_Bear201_DegradeMode := 2;
    bAlarm_TMR_Bear201_Discr := TRUE;
    rTMR_Bear201_Voted := (rSpindleTemp_TT201A_In + rSpindleTemp_TT201C_In) * 0.5;
ELSIF (NOT bTMR_Bear201_FaultA) AND (NOT bTMR_Bear201_FaultB) AND bTMR_Bear201_FaultC THEN
    iTMR_Bear201_DegradeMode := 2;
    bAlarm_TMR_Bear201_Discr := TRUE;
    rTMR_Bear201_Voted := (rSpindleTemp_TT201A_In + rSpindleTemp_TT201B_In) * 0.5;
ELSIF (NOT bTMR_Bear201_FaultA) AND bTMR_Bear201_FaultB AND bTMR_Bear201_FaultC THEN
    iTMR_Bear201_DegradeMode := 1;
    bAlarm_TMR_Bear201_Discr := TRUE;
    rTMR_Bear201_Voted := rSpindleTemp_TT201A_In;
ELSIF bTMR_Bear201_FaultA AND (NOT bTMR_Bear201_FaultB) AND bTMR_Bear201_FaultC THEN
    iTMR_Bear201_DegradeMode := 1;
    bAlarm_TMR_Bear201_Discr := TRUE;
    rTMR_Bear201_Voted := rSpindleTemp_TT201B_In;
ELSIF bTMR_Bear201_FaultA AND bTMR_Bear201_FaultB AND (NOT bTMR_Bear201_FaultC) THEN
    iTMR_Bear201_DegradeMode := 1;
    bAlarm_TMR_Bear201_Discr := TRUE;
    rTMR_Bear201_Voted := rSpindleTemp_TT201C_In;
ELSE
    iTMR_Bear201_DegradeMode := 0;
    bAlarm_TMR_Bear201_Discr := TRUE;
    rTMR_Bear201_Voted := rTMR_Bear201_Prev;
END_IF;
rTMR_Bear201_Prev := rTMR_Bear201_Voted;

(* ---------------------------------------------------------------------------------------------------------------------
 * CHANNEL 3: DT-SPINDLE-301 SPINDLE NOSE EDDY-CURRENT DISPLACEMENT (Z-AXIS DISPLACEMENT [um])
 * --------------------------------------------------------------------------------------------------------------------- *)
IF ABS(rSpindleDisp_DT301A_In - rSpindleDisp_DT301B_In) > rDiscrTol_Disp301 THEN
    rTMR_Disp301_TimerAB := rTMR_Disp301_TimerAB + 1.0;
ELSE
    IF rTMR_Disp301_TimerAB > 0.0 THEN
        rTMR_Disp301_TimerAB := rTMR_Disp301_TimerAB - 0.5;
    END_IF;
END_IF;

IF ABS(rSpindleDisp_DT301B_In - rSpindleDisp_DT301C_In) > rDiscrTol_Disp301 THEN
    rTMR_Disp301_TimerBC := rTMR_Disp301_TimerBC + 1.0;
ELSE
    IF rTMR_Disp301_TimerBC > 0.0 THEN
        rTMR_Disp301_TimerBC := rTMR_Disp301_TimerBC - 0.5;
    END_IF;
END_IF;

IF ABS(rSpindleDisp_DT301A_In - rSpindleDisp_DT301C_In) > rDiscrTol_Disp301 THEN
    rTMR_Disp301_TimerCA := rTMR_Disp301_TimerCA + 1.0;
ELSE
    IF rTMR_Disp301_TimerCA > 0.0 THEN
        rTMR_Disp301_TimerCA := rTMR_Disp301_TimerCA - 0.5;
    END_IF;
END_IF;

IF (rTMR_Disp301_TimerAB >= rDiscrepancy_Limit_ms) AND (rTMR_Disp301_TimerCA >= rDiscrepancy_Limit_ms) THEN
    bTMR_Disp301_FaultA := TRUE;
END_IF;
IF (rTMR_Disp301_TimerAB >= rDiscrepancy_Limit_ms) AND (rTMR_Disp301_TimerBC >= rDiscrepancy_Limit_ms) THEN
    bTMR_Disp301_FaultB := TRUE;
END_IF;
IF (rTMR_Disp301_TimerBC >= rDiscrepancy_Limit_ms) AND (rTMR_Disp301_TimerCA >= rDiscrepancy_Limit_ms) THEN
    bTMR_Disp301_FaultC := TRUE;
END_IF;

IF (NOT bTMR_Disp301_FaultA) AND (NOT bTMR_Disp301_FaultB) AND (NOT bTMR_Disp301_FaultC) THEN
    iTMR_Disp301_DegradeMode := 3;
    bAlarm_TMR_Disp301_Discr := FALSE;
    IF ((rSpindleDisp_DT301A_In >= rSpindleDisp_DT301B_In) AND (rSpindleDisp_DT301A_In <= rSpindleDisp_DT301C_In)) OR
       ((rSpindleDisp_DT301A_In <= rSpindleDisp_DT301B_In) AND (rSpindleDisp_DT301A_In >= rSpindleDisp_DT301C_In)) THEN
        rTMR_Disp301_Voted := rSpindleDisp_DT301A_In;
    ELSIF ((rSpindleDisp_DT301B_In >= rSpindleDisp_DT301A_In) AND (rSpindleDisp_DT301B_In <= rSpindleDisp_DT301C_In)) OR
          ((rSpindleDisp_DT301B_In <= rSpindleDisp_DT301A_In) AND (rSpindleDisp_DT301B_In >= rSpindleDisp_DT301C_In)) THEN
        rTMR_Disp301_Voted := rSpindleDisp_DT301B_In;
    ELSE
        rTMR_Disp301_Voted := rSpindleDisp_DT301C_In;
    END_IF;
ELSIF bTMR_Disp301_FaultA AND (NOT bTMR_Disp301_FaultB) AND (NOT bTMR_Disp301_FaultC) THEN
    iTMR_Disp301_DegradeMode := 2;
    bAlarm_TMR_Disp301_Discr := TRUE;
    rTMR_Disp301_Voted := (rSpindleDisp_DT301B_In + rSpindleDisp_DT301C_In) * 0.5;
ELSIF (NOT bTMR_Disp301_FaultA) AND bTMR_Disp301_FaultB AND (NOT bTMR_Disp301_FaultC) THEN
    iTMR_Disp301_DegradeMode := 2;
    bAlarm_TMR_Disp301_Discr := TRUE;
    rTMR_Disp301_Voted := (rSpindleDisp_DT301A_In + rSpindleDisp_DT301C_In) * 0.5;
ELSIF (NOT bTMR_Disp301_FaultA) AND (NOT bTMR_Disp301_FaultB) AND bTMR_Disp301_FaultC THEN
    iTMR_Disp301_DegradeMode := 2;
    bAlarm_TMR_Disp301_Discr := TRUE;
    rTMR_Disp301_Voted := (rSpindleDisp_DT301A_In + rSpindleDisp_DT301B_In) * 0.5;
ELSIF (NOT bTMR_Disp301_FaultA) AND bTMR_Disp301_FaultB AND bTMR_Disp301_FaultC THEN
    iTMR_Disp301_DegradeMode := 1;
    bAlarm_TMR_Disp301_Discr := TRUE;
    rTMR_Disp301_Voted := rSpindleDisp_DT301A_In;
ELSIF bTMR_Disp301_FaultA AND (NOT bTMR_Disp301_FaultB) AND bTMR_Disp301_FaultC THEN
    iTMR_Disp301_DegradeMode := 1;
    bAlarm_TMR_Disp301_Discr := TRUE;
    rTMR_Disp301_Voted := rSpindleDisp_DT301B_In;
ELSIF bTMR_Disp301_FaultA AND bTMR_Disp301_FaultB AND (NOT bTMR_Disp301_FaultC) THEN
    iTMR_Disp301_DegradeMode := 1;
    bAlarm_TMR_Disp301_Discr := TRUE;
    rTMR_Disp301_Voted := rSpindleDisp_DT301C_In;
ELSE
    iTMR_Disp301_DegradeMode := 0;
    bAlarm_TMR_Disp301_Discr := TRUE;
    rTMR_Disp301_Voted := rTMR_Disp301_Prev;
END_IF;
rTMR_Disp301_Prev := rTMR_Disp301_Voted;

(* ---------------------------------------------------------------------------------------------------------------------
 * CHANNEL 4: AT-CHATTER-401 TOOL HEAD TRIAXIAL ACCELEROMETERS (VIBRATION [m/s2])
 * --------------------------------------------------------------------------------------------------------------------- *)
IF ABS(rChatterAccel_AT401A_In - rChatterAccel_AT401B_In) > rDiscrTol_Chatter401 THEN
    rTMR_Chatter401_TimerAB := rTMR_Chatter401_TimerAB + 1.0;
ELSE
    IF rTMR_Chatter401_TimerAB > 0.0 THEN
        rTMR_Chatter401_TimerAB := rTMR_Chatter401_TimerAB - 0.5;
    END_IF;
END_IF;

IF ABS(rChatterAccel_AT401B_In - rChatterAccel_AT401C_In) > rDiscrTol_Chatter401 THEN
    rTMR_Chatter401_TimerBC := rTMR_Chatter401_TimerBC + 1.0;
ELSE
    IF rTMR_Chatter401_TimerBC > 0.0 THEN
        rTMR_Chatter401_TimerBC := rTMR_Chatter401_TimerBC - 0.5;
    END_IF;
END_IF;

IF ABS(rChatterAccel_AT401A_In - rChatterAccel_AT401C_In) > rDiscrTol_Chatter401 THEN
    rTMR_Chatter401_TimerCA := rTMR_Chatter401_TimerCA + 1.0;
ELSE
    IF rTMR_Chatter401_TimerCA > 0.0 THEN
        rTMR_Chatter401_TimerCA := rTMR_Chatter401_TimerCA - 0.5;
    END_IF;
END_IF;

IF (rTMR_Chatter401_TimerAB >= rDiscrepancy_Limit_ms) AND (rTMR_Chatter401_TimerCA >= rDiscrepancy_Limit_ms) THEN
    bTMR_Chatter401_FaultA := TRUE;
END_IF;
IF (rTMR_Chatter401_TimerAB >= rDiscrepancy_Limit_ms) AND (rTMR_Chatter401_TimerBC >= rDiscrepancy_Limit_ms) THEN
    bTMR_Chatter401_FaultB := TRUE;
END_IF;
IF (rTMR_Chatter401_TimerBC >= rDiscrepancy_Limit_ms) AND (rTMR_Chatter401_TimerCA >= rDiscrepancy_Limit_ms) THEN
    bTMR_Chatter401_FaultC := TRUE;
END_IF;

IF (NOT bTMR_Chatter401_FaultA) AND (NOT bTMR_Chatter401_FaultB) AND (NOT bTMR_Chatter401_FaultC) THEN
    iTMR_Chatter401_DegradeMode := 3;
    bAlarm_TMR_Chatter401_Discr := FALSE;
    IF ((rChatterAccel_AT401A_In >= rChatterAccel_AT401B_In) AND (rChatterAccel_AT401A_In <= rChatterAccel_AT401C_In)) OR
       ((rChatterAccel_AT401A_In <= rChatterAccel_AT401B_In) AND (rChatterAccel_AT401A_In >= rChatterAccel_AT401C_In)) THEN
        rTMR_Chatter401_Voted := rChatterAccel_AT401A_In;
    ELSIF ((rChatterAccel_AT401B_In >= rChatterAccel_AT401A_In) AND (rChatterAccel_AT401B_In <= rChatterAccel_AT401C_In)) OR
          ((rChatterAccel_AT401B_In <= rChatterAccel_AT401A_In) AND (rChatterAccel_AT401B_In >= rChatterAccel_AT401C_In)) THEN
        rTMR_Chatter401_Voted := rChatterAccel_AT401B_In;
    ELSE
        rTMR_Chatter401_Voted := rChatterAccel_AT401C_In;
    END_IF;
ELSIF bTMR_Chatter401_FaultA AND (NOT bTMR_Chatter401_FaultB) AND (NOT bTMR_Chatter401_FaultC) THEN
    iTMR_Chatter401_DegradeMode := 2;
    bAlarm_TMR_Chatter401_Discr := TRUE;
    rTMR_Chatter401_Voted := (rChatterAccel_AT401B_In + rChatterAccel_AT401C_In) * 0.5;
ELSIF (NOT bTMR_Chatter401_FaultA) AND bTMR_Chatter401_FaultB AND (NOT bTMR_Chatter401_FaultC) THEN
    iTMR_Chatter401_DegradeMode := 2;
    bAlarm_TMR_Chatter401_Discr := TRUE;
    rTMR_Chatter401_Voted := (rChatterAccel_AT401A_In + rChatterAccel_AT401C_In) * 0.5;
ELSIF (NOT bTMR_Chatter401_FaultA) AND (NOT bTMR_Chatter401_FaultB) AND bTMR_Chatter401_FaultC THEN
    iTMR_Chatter401_DegradeMode := 2;
    bAlarm_TMR_Chatter401_Discr := TRUE;
    rTMR_Chatter401_Voted := (rChatterAccel_AT401A_In + rChatterAccel_AT401B_In) * 0.5;
ELSIF (NOT bTMR_Chatter401_FaultA) AND bTMR_Chatter401_FaultB AND bTMR_Chatter401_FaultC THEN
    iTMR_Chatter401_DegradeMode := 1;
    bAlarm_TMR_Chatter401_Discr := TRUE;
    rTMR_Chatter401_Voted := rChatterAccel_AT401A_In;
ELSIF bTMR_Chatter401_FaultA AND (NOT bTMR_Chatter401_FaultB) AND bTMR_Chatter401_FaultC THEN
    iTMR_Chatter401_DegradeMode := 1;
    bAlarm_TMR_Chatter401_Discr := TRUE;
    rTMR_Chatter401_Voted := rChatterAccel_AT401B_In;
ELSIF bTMR_Chatter401_FaultA AND bTMR_Chatter401_FaultB AND (NOT bTMR_Chatter401_FaultC) THEN
    iTMR_Chatter401_DegradeMode := 1;
    bAlarm_TMR_Chatter401_Discr := TRUE;
    rTMR_Chatter401_Voted := rChatterAccel_AT401C_In;
ELSE
    iTMR_Chatter401_DegradeMode := 0;
    bAlarm_TMR_Chatter401_Discr := TRUE;
    rTMR_Chatter401_Voted := rTMR_Chatter401_Prev;
END_IF;
rTMR_Chatter401_Prev := rTMR_Chatter401_Voted;

(* ---------------------------------------------------------------------------------------------------------------------
 * CHANNEL 5: IT-CURRENT-501 SPINDLE MOTOR PHASE CURRENT TRANSDUCERS (CURRENT [A])
 * --------------------------------------------------------------------------------------------------------------------- *)
IF ABS(rMotorCurrent_IT501A_In - rMotorCurrent_IT501B_In) > rDiscrTol_Current501 THEN
    rTMR_Current501_TimerAB := rTMR_Current501_TimerAB + 1.0;
ELSE
    IF rTMR_Current501_TimerAB > 0.0 THEN
        rTMR_Current501_TimerAB := rTMR_Current501_TimerAB - 0.5;
    END_IF;
END_IF;

IF ABS(rMotorCurrent_IT501B_In - rMotorCurrent_IT501C_In) > rDiscrTol_Current501 THEN
    rTMR_Current501_TimerBC := rTMR_Current501_TimerBC + 1.0;
ELSE
    IF rTMR_Current501_TimerBC > 0.0 THEN
        rTMR_Current501_TimerBC := rTMR_Current501_TimerBC - 0.5;
    END_IF;
END_IF;

IF ABS(rMotorCurrent_IT501A_In - rMotorCurrent_IT501C_In) > rDiscrTol_Current501 THEN
    rTMR_Current501_TimerCA := rTMR_Current501_TimerCA + 1.0;
ELSE
    IF rTMR_Current501_TimerCA > 0.0 THEN
        rTMR_Current501_TimerCA := rTMR_Current501_TimerCA - 0.5;
    END_IF;
END_IF;

IF (rTMR_Current501_TimerAB >= rDiscrepancy_Limit_ms) AND (rTMR_Current501_TimerCA >= rDiscrepancy_Limit_ms) THEN
    bTMR_Current501_FaultA := TRUE;
END_IF;
IF (rTMR_Current501_TimerAB >= rDiscrepancy_Limit_ms) AND (rTMR_Current501_TimerBC >= rDiscrepancy_Limit_ms) THEN
    bTMR_Current501_FaultB := TRUE;
END_IF;
IF (rTMR_Current501_TimerBC >= rDiscrepancy_Limit_ms) AND (rTMR_Current501_TimerCA >= rDiscrepancy_Limit_ms) THEN
    bTMR_Current501_FaultC := TRUE;
END_IF;

IF (NOT bTMR_Current501_FaultA) AND (NOT bTMR_Current501_FaultB) AND (NOT bTMR_Current501_FaultC) THEN
    iTMR_Current501_DegradeMode := 3;
    bAlarm_TMR_Current501_Discr := FALSE;
    IF ((rMotorCurrent_IT501A_In >= rMotorCurrent_IT501B_In) AND (rMotorCurrent_IT501A_In <= rMotorCurrent_IT501C_In)) OR
       ((rMotorCurrent_IT501A_In <= rMotorCurrent_IT501B_In) AND (rMotorCurrent_IT501A_In >= rMotorCurrent_IT501C_In)) THEN
        rTMR_Current501_Voted := rMotorCurrent_IT501A_In;
    ELSIF ((rMotorCurrent_IT501B_In >= rMotorCurrent_IT501A_In) AND (rMotorCurrent_IT501B_In <= rMotorCurrent_IT501C_In)) OR
          ((rMotorCurrent_IT501B_In <= rMotorCurrent_IT501A_In) AND (rMotorCurrent_IT501B_In >= rMotorCurrent_IT501C_In)) THEN
        rTMR_Current501_Voted := rMotorCurrent_IT501B_In;
    ELSE
        rTMR_Current501_Voted := rMotorCurrent_IT501C_In;
    END_IF;
ELSIF bTMR_Current501_FaultA AND (NOT bTMR_Current501_FaultB) AND (NOT bTMR_Current501_FaultC) THEN
    iTMR_Current501_DegradeMode := 2;
    bAlarm_TMR_Current501_Discr := TRUE;
    rTMR_Current501_Voted := (rMotorCurrent_IT501B_In + rMotorCurrent_IT501C_In) * 0.5;
ELSIF (NOT bTMR_Current501_FaultA) AND bTMR_Current501_FaultB AND (NOT bTMR_Current501_FaultC) THEN
    iTMR_Current501_DegradeMode := 2;
    bAlarm_TMR_Current501_Discr := TRUE;
    rTMR_Current501_Voted := (rMotorCurrent_IT501A_In + rMotorCurrent_IT501C_In) * 0.5;
ELSIF (NOT bTMR_Current501_FaultA) AND (NOT bTMR_Current501_FaultB) AND bTMR_Current501_FaultC THEN
    iTMR_Current501_DegradeMode := 2;
    bAlarm_TMR_Current501_Discr := TRUE;
    rTMR_Current501_Voted := (rMotorCurrent_IT501A_In + rMotorCurrent_IT501B_In) * 0.5;
ELSIF (NOT bTMR_Current501_FaultA) AND bTMR_Current501_FaultB AND bTMR_Current501_FaultC THEN
    iTMR_Current501_DegradeMode := 1;
    bAlarm_TMR_Current501_Discr := TRUE;
    rTMR_Current501_Voted := rMotorCurrent_IT501A_In;
ELSIF bTMR_Current501_FaultA AND (NOT bTMR_Current501_FaultB) AND bTMR_Current501_FaultC THEN
    iTMR_Current501_DegradeMode := 1;
    bAlarm_TMR_Current501_Discr := TRUE;
    rTMR_Current501_Voted := rMotorCurrent_IT501B_In;
ELSIF bTMR_Current501_FaultA AND bTMR_Current501_FaultB AND (NOT bTMR_Current501_FaultC) THEN
    iTMR_Current501_DegradeMode := 1;
    bAlarm_TMR_Current501_Discr := TRUE;
    rTMR_Current501_Voted := rMotorCurrent_IT501C_In;
ELSE
    iTMR_Current501_DegradeMode := 0;
    bAlarm_TMR_Current501_Discr := TRUE;
    rTMR_Current501_Voted := rTMR_Current501_Prev;
END_IF;
rTMR_Current501_Prev := rTMR_Current501_Voted;
""")

    # -------------------------------------------------------------------------
    # 6. PHASE 2: FIRST-PRINCIPLES CYBER-PHYSICAL STATE-SPACE ESTIMATION & OBSERVER
    # -------------------------------------------------------------------------
    st.append("""
(* =====================================================================================================================
 * PHASE 2: FIRST-PRINCIPLES CYBER-PHYSICAL STATE-SPACE ESTIMATION & OBSERVER INNOVATION
 * Discrete state-space matrices configured for 1.0 ms servo task execution:
 *   x[k+1] = A * x[k] + B * u[k] + L * (y[k] - y_hat[k])
 *   y_hat[k] = C * x[k] + D * u[k]
 * ===================================================================================================================== *)

(* Initialize discrete state-space and observer gain matrices on cold start *)
IF NOT bMatrices_Initialized THEN
    (* Matrix A (8x8): System Internal Couplings & Dynamics *)
    rA_mat[1,1] := 0.98500; rA_mat[1,2] := 0.00012; rA_mat[1,3] := 0.00008; rA_mat[1,4] := -0.00025;
    rA_mat[1,5] := 0.00140; rA_mat[1,6] := 0.00320; rA_mat[1,7] := 0.00085; rA_mat[1,8] := 0.01250;

    rA_mat[2,1] := 0.00005; rA_mat[2,2] := 0.99920; rA_mat[2,3] := 0.00045; rA_mat[2,4] := 0.00010;
    rA_mat[2,5] := 0.00030; rA_mat[2,6] := 0.00180; rA_mat[2,7] := 0.00450; rA_mat[2,8] := 0.00025;

    rA_mat[3,1] := 0.00004; rA_mat[3,2] := 0.00040; rA_mat[3,3] := 0.99935; rA_mat[3,4] := 0.00008;
    rA_mat[3,5] := 0.00015; rA_mat[3,6] := 0.00095; rA_mat[3,7] := 0.00520; rA_mat[3,8] := 0.00020;

    rA_mat[4,1] := -0.00015; rA_mat[4,2] := 0.00850; rA_mat[4,3] := 0.00420; rA_mat[4,4] := 0.99890;
    rA_mat[4,5] := 0.00060; rA_mat[4,6] := -0.00120; rA_mat[4,7] := 0.00050; rA_mat[4,8] := 0.00680;

    rA_mat[5,1] := 0.00250; rA_mat[5,2] := 0.00015; rA_mat[5,3] := 0.00010; rA_mat[5,4] := 0.00120;
    rA_mat[5,5] := 0.88500; rA_mat[5,6] := 0.04500; rA_mat[5,7] := 0.01500; rA_mat[5,8] := 0.00080;

    rA_mat[6,1] := 0.00500; rA_mat[6,2] := 0.00080; rA_mat[6,3] := 0.00040; rA_mat[6,4] := 0.02500;
    rA_mat[6,5] := 0.12500; rA_mat[6,6] := 0.92000; rA_mat[6,7] := 0.08500; rA_mat[6,8] := 0.00150;

    rA_mat[7,1] := 0.00080; rA_mat[7,2] := 0.00120; rA_mat[7,3] := 0.00110; rA_mat[7,4] := 0.00050;
    rA_mat[7,5] := 0.01800; rA_mat[7,6] := 0.05200; rA_mat[7,7] := 0.96500; rA_mat[7,8] := 0.00030;

    rA_mat[8,1] := 0.00010; rA_mat[8,2] := 0.00060; rA_mat[8,3] := 0.00040; rA_mat[8,4] := 0.00020;
    rA_mat[8,5] := 0.00005; rA_mat[8,6] := 0.00015; rA_mat[8,7] := 0.00025; rA_mat[8,8] := 0.99960;

    (* Matrix B (8x6): Actuator Input Coupling Matrix *)
    rB_mat[1,1] := 0.04500; rB_mat[1,2] := -0.04500; rB_mat[1,3] := 0.00000; rB_mat[1,4] := 0.00000; rB_mat[1,5] := 0.00000; rB_mat[1,6] := 0.00050;
    rB_mat[2,1] := 0.00010; rB_mat[2,2] := 0.00010; rB_mat[2,3] := 0.00350; rB_mat[2,4] := 0.00000; rB_mat[2,5] := -0.01250; rB_mat[2,6] := 0.00020;
    rB_mat[3,1] := 0.00008; rB_mat[3,2] := 0.00008; rB_mat[3,3] := 0.00420; rB_mat[3,4] := 0.00000; rB_mat[3,5] := -0.00950; rB_mat[3,6] := 0.00015;
    rB_mat[4,1] := 0.00000; rB_mat[4,2] := 0.00000; rB_mat[4,3] := 0.00180; rB_mat[4,4] := -0.98500; rB_mat[4,5] := -0.00450; rB_mat[4,6] := 0.00000;
    rB_mat[5,1] := 0.00050; rB_mat[5,2] := 0.00050; rB_mat[5,3] := -0.02500; rB_mat[5,4] := 0.00100; rB_mat[5,5] := -0.00500; rB_mat[5,6] := -0.14500;
    rB_mat[6,1] := 0.00100; rB_mat[6,2] := 0.00100; rB_mat[6,3] := -0.01800; rB_mat[6,4] := -0.04500; rB_mat[6,5] := -0.00800; rB_mat[6,6] := -0.03500;
    rB_mat[7,1] := 0.00020; rB_mat[7,2] := 0.00020; rB_mat[7,3] := 0.08500; rB_mat[7,4] := 0.00000; rB_mat[7,5] := -0.00200; rB_mat[7,6] := -0.00800;
    rB_mat[8,1] := 0.00015; rB_mat[8,2] := -0.00015; rB_mat[8,3] := 0.00010; rB_mat[8,4] := 0.00000; rB_mat[8,5] := -0.00150; rB_mat[8,6] := 0.00000;

    (* Matrix C (6x8): Sensor Observation Mapping *)
    rC_mat[1,1] := 1.00000; rC_mat[1,2] := 0.00000; rC_mat[1,3] := 0.00000; rC_mat[1,4] := 0.00000; rC_mat[1,5] := 0.00000; rC_mat[1,6] := 0.00000; rC_mat[1,7] := 0.00000; rC_mat[1,8] := 0.00000;
    rC_mat[2,1] := 0.00000; rC_mat[2,2] := 1.00000; rC_mat[2,3] := 0.00000; rC_mat[2,4] := 0.00000; rC_mat[2,5] := 0.00000; rC_mat[2,6] := 0.00000; rC_mat[2,7] := 0.00000; rC_mat[2,8] := 0.00000;
    rC_mat[3,1] := 0.00000; rC_mat[3,2] := 0.01500; rC_mat[3,3] := 0.00800; rC_mat[3,4] := 1.00000; rC_mat[3,5] := 0.00000; rC_mat[3,6] := 0.00000; rC_mat[3,7] := 0.00000; rC_mat[3,8] := 0.02000;
    rC_mat[4,1] := 0.00000; rC_mat[4,2] := 0.00000; rC_mat[4,3] := 0.00000; rC_mat[4,4] := 0.00000; rC_mat[4,5] := 1.00000; rC_mat[4,6] := 0.00200; rC_mat[4,7] := 0.00000; rC_mat[4,8] := 0.00000;
    rC_mat[5,1] := 0.00000; rC_mat[5,2] := 0.00000; rC_mat[5,3] := 0.00000; rC_mat[5,4] := 0.00000; rC_mat[5,5] := 0.00000; rC_mat[5,6] := 0.01000; rC_mat[5,7] := 1.00000; rC_mat[5,8] := 0.00000;
    rC_mat[6,1] := 0.00000; rC_mat[6,2] := 0.00000; rC_mat[6,3] := 0.00000; rC_mat[6,4] := 0.00000; rC_mat[6,5] := 0.00000; rC_mat[6,6] := 0.00000; rC_mat[6,7] := 0.00000; rC_mat[6,8] := 1.00000;

    (* Matrix D (6x6): Direct Feedthrough Matrix *)
    FOR iMeasIdx := 1 TO 6 DO
        FOR jActIdx := 1 TO 6 DO
            rD_mat[iMeasIdx, jActIdx] := 0.00000;
        END_FOR;
    END_FOR;
    rD_mat[3,4] := -0.01500; (* Direct high-speed piezo feedthrough to eddy current sensor *)

    (* Matrix L (8x6): Kalman Innovation Observer Gains *)
    rL_obs[1,1] := 0.22500; rL_obs[1,2] := 0.00000; rL_obs[1,3] := 0.00150; rL_obs[1,4] := 0.00200; rL_obs[1,5] := 0.00050; rL_obs[1,6] := 0.00850;
    rL_obs[2,1] := 0.00000; rL_obs[2,2] := 0.18500; rL_obs[2,3] := 0.00450; rL_obs[2,4] := 0.00000; rL_obs[2,5] := 0.00120; rL_obs[2,6] := 0.00080;
    rL_obs[3,1] := 0.00000; rL_obs[3,2] := 0.04500; rL_obs[3,3] := 0.00350; rL_obs[3,4] := 0.00000; rL_obs[3,5] := 0.00150; rL_obs[3,6] := 0.00060;
    rL_obs[4,1] := 0.00120; rL_obs[4,2] := 0.01250; rL_obs[4,3] := 0.28500; rL_obs[4,4] := 0.00150; rL_obs[4,5] := 0.00080; rL_obs[4,6] := 0.01500;
    rL_obs[5,1] := 0.00150; rL_obs[5,2] := 0.00000; rL_obs[5,3] := 0.00080; rL_obs[5,4] := 0.34500; rL_obs[5,5] := 0.00550; rL_obs[5,6] := 0.00000;
    rL_obs[6,1] := 0.00350; rL_obs[6,2] := 0.00150; rL_obs[6,3] := 0.00250; rL_obs[6,4] := 0.08500; rL_obs[6,5] := 0.14500; rL_obs[6,6] := 0.00000;
    rL_obs[7,1] := 0.00050; rL_obs[7,2] := 0.00250; rL_obs[7,3] := 0.00080; rL_obs[7,4] := 0.01250; rL_obs[7,5] := 0.29500; rL_obs[7,6] := 0.00000;
    rL_obs[8,1] := 0.00250; rL_obs[8,2] := 0.00120; rL_obs[8,3] := 0.00050; rL_obs[8,4] := 0.00000; rL_obs[8,5] := 0.00000; rL_obs[8,6] := 0.16500;

    (* MPC Cost Function Weights *)
    rQ_cost[1] := 65.0;  (* x1: Gantry Skew Penalty *)
    rQ_cost[2] := 3.5;   (* x2: Front Bearing Temp Penalty *)
    rQ_cost[3] := 2.5;   (* x3: Rear Bearing Temp Penalty *)
    rQ_cost[4] := 85.0;  (* x4: Spindle Z Thermal Elongation Penalty *)
    rQ_cost[5] := 110.0; (* x5: Tool Chatter Acceleration Penalty *)
    rQ_cost[6] := 8.5;   (* x6: Dynamic Cutting Force Penalty *)
    rQ_cost[7] := 4.5;   (* x7: Spindle Torque Penalty *)
    rQ_cost[8] := 12.0;  (* x8: Column Differential Temp Penalty *)

    rR_cost[1] := 1.2;   (* u1: Master Torque Effort *)
    rR_cost[2] := 1.2;   (* u2: Slave Torque Effort *)
    rR_cost[3] := 4.5;   (* u3: Speed Trim Effort *)
    rR_cost[4] := 2.2;   (* u4: Piezo Offset Effort *)
    rR_cost[5] := 0.8;   (* u5: Coolant Throttle Effort *)
    rR_cost[6] := 1.8;   (* u6: Magnetic Damping Effort *)

    FOR iStateIdx := 1 TO 8 DO
        rP_cost[iStateIdx] := rQ_cost[iStateIdx] * 2.8; (* Terminal Cost Penalty *)
    END_FOR;

    (* Actuator Box Constraints *)
    rU_min[1] := 0.0;   rU_max[1] := 100.0; (* Master Torque [%] *)
    rU_min[2] := 0.0;   rU_max[2] := 100.0; (* Slave Torque [%] *)
    rU_min[3] := -15.0; rU_max[3] := 15.0;  (* Spindle Trim [%] *)
    rU_min[4] := -50.0; rU_max[4] := 50.0;  (* Piezo Stroke [um] *)
    rU_min[5] := 0.0;   rU_max[5] := 100.0; (* Coolant Valve [%] *)
    rU_min[6] := 0.0;   rU_max[6] := 100.0; (* Magnetic Damping [%] *)

    (* Actuator Slew Rate Constraints [units per millisecond] *)
    rSlew_max[1] := 2.5;   (* Master Torque Slew: 2500 %/s *)
    rSlew_max[2] := 2.5;   (* Slave Torque Slew: 2500 %/s *)
    rSlew_max[3] := 0.75;  (* Speed Trim Slew: 750 %/s *)
    rSlew_max[4] := 15.0;  (* Piezo Fast Slew: 15,000 um/s *)
    rSlew_max[5] := 1.5;   (* Coolant Valve Slew: 1500 %/s *)
    rSlew_max[6] := 5.0;   (* Magnetic Damping Slew: 5000 %/s *)

    bMatrices_Initialized := TRUE;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * ASSEMBLE INSTRUMENTATION MEASUREMENT VECTOR y_meas[1..6]
 * --------------------------------------------------------------------------------------------------------------------- *)
rY_meas[1] := rTMR_Scale101_Voted;
rY_meas[2] := rTMR_Bear201_Voted;
rY_meas[3] := rTMR_Disp301_Voted;
rY_meas[4] := rTMR_Chatter401_Voted;
(* Convert measured motor current to electro-mechanical torque: Tau = Kt * I (Kt = 1.35 Nm/A for direct drive spindle) *)
rY_meas[5] := rTMR_Current501_Voted * 1.35;
rY_meas[6] := rColumnTemp_Left_TT601A_In - rColumnTemp_Right_TT601B_In;

(* ---------------------------------------------------------------------------------------------------------------------
 * COMPUTE ESTIMATED OUTPUT y_hat[k] = C * x_hat[k] + D * u[k]
 * --------------------------------------------------------------------------------------------------------------------- *)
FOR iMeasIdx := 1 TO 6 DO
    rSumVal := 0.0;
    FOR jStateIdx := 1 TO 8 DO
        rSumVal := rSumVal + rC_mat[iMeasIdx, jStateIdx] * rX_hat[jStateIdx];
    END_FOR;
    FOR jActIdx := 1 TO 6 DO
        rSumVal := rSumVal + rD_mat[iMeasIdx, jActIdx] * rU_act[jActIdx];
    END_FOR;
    rY_hat[iMeasIdx] := rSumVal;
    rE_innov[iMeasIdx] := rY_meas[iMeasIdx] - rY_hat[iMeasIdx];
END_FOR;

(* ---------------------------------------------------------------------------------------------------------------------
 * COMPUTE NEXT STATE ESTIMATE: x_hat[k+1] = A * x_hat[k] + B * u[k] + L * e_innov[k]
 * --------------------------------------------------------------------------------------------------------------------- *)
FOR iStateIdx := 1 TO 8 DO
    rSumVal := 0.0;
    (* State transition contribution *)
    FOR jStateIdx := 1 TO 8 DO
        rSumVal := rSumVal + rA_mat[iStateIdx, jStateIdx] * rX_hat[jStateIdx];
    END_FOR;
    (* Actuator input contribution *)
    FOR jActIdx := 1 TO 6 DO
        rSumVal := rSumVal + rB_mat[iStateIdx, jActIdx] * rU_act[jActIdx];
    END_FOR;
    (* Innovation observer gain contribution *)
    FOR iMeasIdx := 1 TO 6 DO
        rSumVal := rSumVal + rL_obs[iStateIdx, iMeasIdx] * rE_innov[iMeasIdx];
    END_FOR;
    rX_next[iStateIdx] := rSumVal;
END_FOR;

(* State update for next control interval *)
FOR iStateIdx := 1 TO 8 DO
    rX_hat[iStateIdx] := rX_next[iStateIdx];
END_FOR;

(* Output telemetric copies of estimated physical states *)
rEstimated_Z_Elongation_Out  := rX_hat[4];
rEstimated_TCP_Vibration_Out := rX_hat[5];
rEstimated_Dynamic_Force_Out := rX_hat[6];
rGantry_Skew_Error_Out       := rX_hat[1];
rSpindle_Bearing_Temp_Out    := rX_hat[2];
rSpindle_Torque_Actual_Out   := rX_hat[7];
""")

    # -------------------------------------------------------------------------
    # 7. PHASE 3: RECEDING-HORIZON MPC OPTIMIZATION & PGD SOLVER
    # -------------------------------------------------------------------------
    st.append("""
(* =====================================================================================================================
 * PHASE 3: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) WITH PROJECTED GRADIENT DESCENT (PGD)
 * Horizon N = 5 steps, 6 unrolled iterations of analytical gradient optimization with actuator box constraints,
 * dynamic slew-rate limiters, Spindle Speed Modulation (SSM) regenerative chatter disruption, and piezo compensation.
 * ===================================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------------------------
 * 1. FORMULATE DYNAMIC REFERENCE TRAJECTORIES rX_ref AND rU_ref
 * --------------------------------------------------------------------------------------------------------------------- *)
FOR iHorizIdx := 0 TO 5 DO
    rX_ref[iHorizIdx, 1] := 0.0;   (* Skew Target: 0.0 um *)
    rX_ref[iHorizIdx, 2] := 32.0;  (* Forward Bearing Temp Target: 32.0 deg C *)
    rX_ref[iHorizIdx, 3] := 28.0;  (* Rear Bearing Temp Target: 28.0 deg C *)
    rX_ref[iHorizIdx, 4] := 0.0;   (* Spindle Z Thermal Growth Target: 0.0 um *)
    rX_ref[iHorizIdx, 5] := 0.0;   (* Chatter Vibration Target: 0.0 m/s2 *)
    IF eState = 7 THEN
        rX_ref[iHorizIdx, 6] := 650.0; (* Nominal Cutting Force in Heavy Milling [N] *)
        rX_ref[iHorizIdx, 7] := 22.5;  (* Nominal Cutting Torque in Heavy Milling [Nm] *)
    ELSE
        rX_ref[iHorizIdx, 6] := 0.0;
        rX_ref[iHorizIdx, 7] := 4.2;   (* Idle Spindle Friction Torque [Nm] *)
    END_IF;
    rX_ref[iHorizIdx, 8] := 0.0;   (* Column Thermal Gradient Target: 0.0 deg C *)
END_FOR;

FOR iHorizIdx := 0 TO 4 DO
    rU_ref[iHorizIdx, 1] := 50.0;  (* Master X Servo Nominal Torque Bias 50% *)
    rU_ref[iHorizIdx, 2] := 50.0;  (* Slave X Servo Nominal Torque Bias 50% *)
    rU_ref[iHorizIdx, 3] := 0.0;   (* Nominal Spindle Speed Trim 0% *)
    rU_ref[iHorizIdx, 4] := 0.0;   (* Nominal Piezo Offset 0 um *)
    IF eState = 7 THEN
        rU_ref[iHorizIdx, 5] := 75.0;  (* Through-Spindle Coolant Valve 75% in Cut *)
        rU_ref[iHorizIdx, 6] := 35.0;  (* Active Damping Bias 35% in Cut *)
    ELSE
        rU_ref[iHorizIdx, 5] := 15.0;  (* Idle Coolant Valve 15% *)
        rU_ref[iHorizIdx, 6] := 10.0;  (* Idle Active Damping 10% *)
    END_IF;
END_FOR;

(* Initialize candidate control trajectory with previous solutions or reference *)
FOR iHorizIdx := 0 TO 4 DO
    FOR iActIdx := 1 TO 6 DO
        rU_cand[iHorizIdx, iActIdx] := rU_act[iActIdx];
    END_FOR;
END_FOR;

(* ---------------------------------------------------------------------------------------------------------------------
 * 2. UNROLLED 6-ITERATION PROJECTED GRADIENT DESCENT (PGD) OPTIMIZER
 * --------------------------------------------------------------------------------------------------------------------- *)
FOR iIterIdx := 1 TO 6 DO
    (* Step 2a: Forward State Prediction across Horizon N=5 *)
    FOR iStateIdx := 1 TO 8 DO
        rX_pred[0, iStateIdx] := rX_hat[iStateIdx];
    END_FOR;

    FOR iHorizIdx := 0 TO 4 DO
        FOR iStateIdx := 1 TO 8 DO
            rSumVal := 0.0;
            FOR jStateIdx := 1 TO 8 DO
                rSumVal := rSumVal + rA_mat[iStateIdx, jStateIdx] * rX_pred[iHorizIdx, jStateIdx];
            END_FOR;
            FOR jActIdx := 1 TO 6 DO
                rSumVal := rSumVal + rB_mat[iStateIdx, jActIdx] * rU_cand[iHorizIdx, jActIdx];
            END_FOR;
            rX_pred[iHorizIdx + 1, iStateIdx] := rSumVal;
        END_FOR;
    END_FOR;

    (* Step 2b: Backward Costate Adjoint Propagation from Terminal Horizon *)
    FOR iStateIdx := 1 TO 8 DO
        rLambda_costate[5, iStateIdx] := rP_cost[iStateIdx] * (rX_pred[5, iStateIdx] - rX_ref[5, iStateIdx]);
    END_FOR;

    FOR iHorizIdx := 4 TO 0 BY -1 DO
        FOR iStateIdx := 1 TO 8 DO
            rSumVal := rQ_cost[iStateIdx] * (rX_pred[iHorizIdx, iStateIdx] - rX_ref[iHorizIdx, iStateIdx]);
            FOR jStateIdx := 1 TO 8 DO
                (* Transpose of A: rA_mat[jStateIdx, iStateIdx] *)
                rSumVal := rSumVal + rA_mat[jStateIdx, iStateIdx] * rLambda_costate[iHorizIdx + 1, jStateIdx];
            END_FOR;
            rLambda_costate[iHorizIdx, iStateIdx] := rSumVal;
        END_FOR;
    END_FOR;

    (* Step 2c: Gradient Evaluation and Projected Gradient Descent Step *)
    FOR iHorizIdx := 0 TO 4 DO
        FOR iActIdx := 1 TO 6 DO
            rSumVal := rR_cost[iActIdx] * (rU_cand[iHorizIdx, iActIdx] - rU_ref[iHorizIdx, iActIdx]);
            FOR jStateIdx := 1 TO 8 DO
                (* Transpose of B: rB_mat[jStateIdx, iActIdx] *)
                rSumVal := rSumVal + rB_mat[jStateIdx, iActIdx] * rLambda_costate[iHorizIdx + 1, jStateIdx];
            END_FOR;
            rGrad_U[iHorizIdx, iActIdx] := rSumVal;

            (* Gradient descent step *)
            rU_cand[iHorizIdx, iActIdx] := rU_cand[iHorizIdx, iActIdx] - (rAlpha_PGD * rGrad_U[iHorizIdx, iActIdx]);

            (* Box constraint projection *)
            IF rU_cand[iHorizIdx, iActIdx] < rU_min[iActIdx] THEN
                rU_cand[iHorizIdx, iActIdx] := rU_min[iActIdx];
            ELSIF rU_cand[iHorizIdx, iActIdx] > rU_max[iActIdx] THEN
                rU_cand[iHorizIdx, iActIdx] := rU_max[iActIdx];
            END_IF;
        END_FOR;
    END_FOR;
END_FOR;

(* ---------------------------------------------------------------------------------------------------------------------
 * 3. ACTUATOR SLEW RATE LIMITING & MULTI-AXIS DECOUPLING
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Slew rate clamp on the candidate first-step control action *)
FOR iActIdx := 1 TO 6 DO
    rDiffVal := rU_cand[0, iActIdx] - rU_prev[iActIdx];
    IF rDiffVal > rSlew_max[iActIdx] THEN
        rU_act[iActIdx] := rU_prev[iActIdx] + rSlew_max[iActIdx];
    ELSIF rDiffVal < -rSlew_max[iActIdx] THEN
        rU_act[iActIdx] := rU_prev[iActIdx] - rSlew_max[iActIdx];
    ELSE
        rU_act[iActIdx] := rU_cand[0, iActIdx];
    END_IF;
    rU_prev[iActIdx] := rU_act[iActIdx];
END_FOR;

(* ---------------------------------------------------------------------------------------------------------------------
 * 4. SPINDLE SPEED MODULATION (SSM) REGENERATIVE CHATTER ATTENUATION
 * Sinusoidal spindle speed modulation: dOmega(t) = Omega0 * RVA * sin(2*pi*fm*t)
 * --------------------------------------------------------------------------------------------------------------------- *)
IF bSSM_Chatter_Enable_In AND (eState = 7 OR eState = 8) AND (rX_hat[5] > 8.0) THEN
    (* Advance sinusoidal phase accumulator: dPhase = 2*pi * fm * Ts (Ts = 0.001 s) *)
    rSSM_Phase := rSSM_Phase + (2.0 * rPi_Constant * rSSM_Freq * 0.001);
    IF rSSM_Phase >= (2.0 * rPi_Constant) THEN
        rSSM_Phase := rSSM_Phase - (2.0 * rPi_Constant);
    END_IF;

    (* Modulate trim percent *)
    rSSM_Modulation_Trim := (rSSM_RVA * 100.0) * SIN(rSSM_Phase);
    rSSM_Perturbation_RPM := (rProgrammedSpindleSpeed_In * rSSM_RVA) * SIN(rSSM_Phase);
    bChatter_Suppression_Active_Out := TRUE;
ELSE
    rSSM_Modulation_Trim := 0.0;
    rSSM_Perturbation_RPM := 0.0;
    bChatter_Suppression_Active_Out := FALSE;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * 5. MASTER-SLAVE GANTRY SKEW CANCELLATION & DIFFERENTIAL TORQUE SPLIT
 * Anti-skew PD controller counteracting differential linear scale mismatch: Delta_Tau = Kp * e + Kd * de/dt
 * --------------------------------------------------------------------------------------------------------------------- *)
rDiffVal := rX_hat[1] - rSkew_Error_Prev; (* de/dt with dt = 1.0 ms *)
rSkew_Delta_Torque := (rSkew_Kp * rX_hat[1]) + (rSkew_Kd * rDiffVal);
rSkew_Error_Prev := rX_hat[1];

(* Apply torque split to Master (X1) and Slave (X2) gantry drives *)
rMaster_X_Torque_Cmd_Out := rU_act[1] + (rSkew_Delta_Torque * 0.5);
rSlave_X_Torque_Cmd_Out  := rU_act[2] - (rSkew_Delta_Torque * 0.5);

(* Clamp final gantry torque commands to [0.0..100.0] % *)
IF rMaster_X_Torque_Cmd_Out < 0.0 THEN
    rMaster_X_Torque_Cmd_Out := 0.0;
ELSIF rMaster_X_Torque_Cmd_Out > 100.0 THEN
    rMaster_X_Torque_Cmd_Out := 100.0;
END_IF;

IF rSlave_X_Torque_Cmd_Out < 0.0 THEN
    rSlave_X_Torque_Cmd_Out := 0.0;
ELSIF rSlave_X_Torque_Cmd_Out > 100.0 THEN
    rSlave_X_Torque_Cmd_Out := 100.0;
END_IF;

bGantry_Skew_Corrected_Out := (ABS(rX_hat[1]) < 1.5);

(* ---------------------------------------------------------------------------------------------------------------------
 * 6. PIEZO-ELECTRIC Z-AXIS DYNAMIC THERMAL EXPANSION COMPENSATION
 * Direct counter-stroke injection: Stroke = -Estimated_Z_Elongation clamped to [-50.0..+50.0] um.
 * Residual uncompensated elongation beyond +/- 50 um is fed to CNC origin dynamic shift.
 * --------------------------------------------------------------------------------------------------------------------- *)
IF bThermal_Comp_Enable_In THEN
    rTempCalc1 := -rX_hat[4]; (* Invert estimated thermal growth *)
    IF rTempCalc1 > 50.0 THEN
        rPiezo_Z_Thermal_Offset_Out := 50.0;
        rZ_Axis_CNC_Origin_Shift_Out := (rTempCalc1 - 50.0) * 0.001; (* Shift in mm *)
    ELSIF rTempCalc1 < -50.0 THEN
        rPiezo_Z_Thermal_Offset_Out := -50.0;
        rZ_Axis_CNC_Origin_Shift_Out := (rTempCalc1 + 50.0) * 0.001; (* Shift in mm *)
    ELSE
        rPiezo_Z_Thermal_Offset_Out := rTempCalc1;
        rZ_Axis_CNC_Origin_Shift_Out := 0.0;
    END_IF;
    bThermal_Comp_Active_Out := TRUE;
ELSE
    rPiezo_Z_Thermal_Offset_Out := 0.0;
    rZ_Axis_CNC_Origin_Shift_Out := 0.0;
    bThermal_Comp_Active_Out := FALSE;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * 7. ACTUATOR FINAL SYNTHESIS: SPINDLE SPEED, COOLANT & ACTIVE DAMPING
 * --------------------------------------------------------------------------------------------------------------------- *)
rSpindleSpeed_Trim_Cmd_Out := rU_act[3] + rSSM_Modulation_Trim;
rSpindleSpeed_Direct_Cmd_Out := rProgrammedSpindleSpeed_In + rSSM_Perturbation_RPM + (rProgrammedSpindleSpeed_In * (rU_act[3] * 0.01));
IF rSpindleSpeed_Direct_Cmd_Out < 0.0 THEN
    rSpindleSpeed_Direct_Cmd_Out := 0.0;
ELSIF rSpindleSpeed_Direct_Cmd_Out > 30000.0 THEN
    rSpindleSpeed_Direct_Cmd_Out := 30000.0;
END_IF;

rCoolant_PropValve_Cmd_Out  := rU_act[5];
rActiveDamping_Bias_Cmd_Out := rU_act[6];
""")

    # -------------------------------------------------------------------------
    # 8. PHASE 4: DETERMINISTIC 14-STAGE PRODUCTION FINITE STATE MACHINE (FSM)
    # -------------------------------------------------------------------------
    st.append("""
(* =====================================================================================================================
 * PHASE 4: DETERMINISTIC 14-STAGE PRODUCTION FINITE STATE MACHINE (FSM)
 * Millisecond-synchronized sequencing of the 5-Axis Gantry Machining Center Operations:
 *   Stage 0 : MACHINE_POWER_ON_STANDBY_AND_INTERLOCK_LOCK
 *   Stage 1 : SPINDLE_BEARING_WARMUP_RAMP_AND_OIL_MIST_CHECK
 *   Stage 2 : TOOL_TOUCH_PROBE_LENGTH_AND_RADIUS_CALIBRATE
 *   Stage 3 : WORKPIECE_3D_SURFACE_DATUM_MEASUREMENT_LOCK
 *   Stage 4 : GANTRY_MASTER_SLAVE_AUTO_SQUARE_ALIGNMENT
 *   Stage 5 : SPINDLE_SPEED_RAMPUP_AND_BALANCE_CHECK
 *   Stage 6 : FLOOD_AND_MQL_COOLANT_PRESSURE_LOCK
 *   Stage 7 : HIGH_SPEED_5AXIS_CONTOUR_MILLING_RUN
 *   Stage 8 : ACTIVE_REGENERATIVE_CHATTER_DAMPING_SSM
 *   Stage 9 : SPINDLE_THERMAL_ELONGATION_LIVE_COMPENSATION
 *   Stage 10: IN_PROCESS_TOOL_WEAR_ACOUSTIC_EVALUATION
 *   Stage 11: SPINDLE_CONTROLLED_DECELERATION_AND_ORIENT
 *   Stage 12: AUTOMATIC_TOOL_CHANGER_CAROUSEL_SWAP
 *   Stage 13: EMERGENCY_TOOL_BREAK_OR_COLLISION_RETRACT_TRIP
 * ===================================================================================================================== *)

(* Master Safety & Emergency Interlock Check *)
IF (NOT bEmergencyStop_Circuit_OK_In) OR (NOT bSafetyGate_Interlock_OK_In) OR
   (iTMR_Scale101_DegradeMode = 0) OR (iTMR_Disp301_DegradeMode = 0) OR
   bFastToolBreak_Trip OR bFastCollision_Trip THEN
    eState := 13; (* Immediate jump to Emergency Retract Trip *)
END_IF;

(* State entry detection and elapsed timer management *)
IF eState <> ePrevState THEN
    tStateTimer := 0.0;
    bStateInitialized := FALSE;
    ePrevState := eState;
ELSE
    tStateTimer := tStateTimer + 1.0;
END_IF;

CASE eState OF
    (* -----------------------------------------------------------------------------------------------------------------
     * STAGE 0: MACHINE_POWER_ON_STANDBY_AND_INTERLOCK_LOCK
     * ----------------------------------------------------------------------------------------------------------------- *)
    0:
        bMachine_Ready_Out := FALSE;
        bSpindle_At_Speed_Out := FALSE;
        bATC_Cycle_Complete_Out := FALSE;
        bEmergency_Retract_Active_Out := FALSE;
        rSpindleSpeed_Direct_Cmd_Out := 0.0;
        rSpindleBrake_Torque_Cmd_Out := 100.0; (* Mechanical brake engaged *)
        rDrawbarCylinder_Cmd_Out := 0.0;     (* Tool clamped *)

        IF bEmergencyStop_Circuit_OK_In AND bSafetyGate_Interlock_OK_In AND
           bHydraulicPower_Ready_In AND bPneumatics_MainAir_OK_In AND
           (rOilMistPressure_PT801_In >= rLim_OilMist_L) AND
           (rHydraulicPressure_PT901_In >= 135.0) THEN

            bMachine_Ready_Out := TRUE;

            IF bSpindle_Warmup_Select_In THEN
                eState := 1; (* Initiate Daily Spindle Thermal Warmup *)
            ELSIF bCNC_Cycle_Start_In THEN
                eState := 4; (* Skip to Gantry Auto-Squaring Alignment *)
            END_IF;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STAGE 1: SPINDLE_BEARING_WARMUP_RAMP_AND_OIL_MIST_CHECK
     * Progressive 4-tier step ramp: 3,000 -> 9,000 -> 18,000 -> 24,000 rpm to evenly distribute bearing grease/oil.
     * ----------------------------------------------------------------------------------------------------------------- *)
    1:
        tWarmupTimer := tWarmupTimer + 1.0;
        rSpindleBrake_Torque_Cmd_Out := 0.0;

        (* Stage ramp scheduling *)
        IF tWarmupTimer < 15000.0 THEN
            rSpindleSpeed_Direct_Cmd_Out := 3000.0;
        ELSIF tWarmupTimer < 35000.0 THEN
            rSpindleSpeed_Direct_Cmd_Out := 9000.0;
        ELSIF tWarmupTimer < 60000.0 THEN
            rSpindleSpeed_Direct_Cmd_Out := 18000.0;
        ELSE
            rSpindleSpeed_Direct_Cmd_Out := 24000.0;
        END_IF;

        (* Bearing thermal equilibrium and gradient verification *)
        IF (tWarmupTimer >= 80000.0) AND (rX_hat[2] >= 28.0) AND (rX_hat[3] >= 26.0) THEN
            rSpindleSpeed_Direct_Cmd_Out := 0.0;
            IF rSpindleActualSpeed_In < 150.0 THEN
                tWarmupTimer := 0.0;
                eState := 2; (* Advance to Kinematic Tool Calibration *)
            END_IF;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STAGE 2: TOOL_TOUCH_PROBE_LENGTH_AND_RADIUS_CALIBRATE
     * Blum Laser Tool Setter touch probe inspection for tool length offset, tip radius and runout (< 2.0 um).
     * ----------------------------------------------------------------------------------------------------------------- *)
    2:
        tToolProbeTimer := tToolProbeTimer + 1.0;
        rSpindleSpeed_Direct_Cmd_Out := 800.0; (* Slow spin for optical laser beam interception *)

        IF tToolProbeTimer > 5000.0 THEN
            (* Capture touch probe deflection reading *)
            rToolLength_Offset[iToolCurrentID] := rToolTouchProbeDisp_In * 0.001; (* mm *)
            rToolRadius_Offset[iToolCurrentID] := 8.000; (* Baseline 16mm endmill radius *)

            IF ABS(rToolTouchProbeDisp_In) < 150.0 THEN
                tToolProbeTimer := 0.0;
                rSpindleSpeed_Direct_Cmd_Out := 0.0;
                eState := 3; (* Advance to Workpiece Datum Lock *)
            ELSE
                bToolWearLimitTrip := TRUE;
                eState := 11; (* Tool wear excessive: abort to decel & orient *)
            END_IF;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STAGE 3: WORKPIECE_3D_SURFACE_DATUM_MEASUREMENT_LOCK
     * Wireless optical 3D touch probe surface scan establishing G54/G55 coordinate datums and RTCP rotation centers.
     * ----------------------------------------------------------------------------------------------------------------- *)
    3:
        tDatumScanTimer := tDatumScanTimer + 1.0;
        rSpindleSpeed_Direct_Cmd_Out := 0.0;
        rSpindleBrake_Torque_Cmd_Out := 100.0;

        IF tDatumScanTimer > 4000.0 THEN
            IF ABS(rWorkpieceProbeSignal_In) < 50.0 THEN
                tDatumScanTimer := 0.0;
                eState := 4; (* Advance to Gantry Squaring *)
            END_IF;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STAGE 4: GANTRY_MASTER_SLAVE_AUTO_SQUARE_ALIGNMENT
     * Dual optical linear scale synchronization; nullify cross-beam skew error to < 1.5 um.
     * ----------------------------------------------------------------------------------------------------------------- *)
    4:
        tGantrySquareTimer := tGantrySquareTimer + 1.0;
        rSpindleBrake_Torque_Cmd_Out := 100.0;

        IF (ABS(rX_hat[1]) < 1.5) AND (tGantrySquareTimer > 3000.0) THEN
            tGantrySquareTimer := 0.0;
            eState := 5; (* Advance to Spindle Speed Ramp-Up *)
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STAGE 5: SPINDLE_SPEED_RAMPUP_AND_BALANCE_CHECK
     * Accelerate motorized spindle to programmed cutting speed; verify dynamic balance vibration (< 1.2 mm/s RMS).
     * ----------------------------------------------------------------------------------------------------------------- *)
    5:
        tSpindleRampTimer := tSpindleRampTimer + 1.0;
        rSpindleBrake_Torque_Cmd_Out := 0.0;
        rSpindleSpeed_Direct_Cmd_Out := rProgrammedSpindleSpeed_In;

        IF ABS(rSpindleActualSpeed_In - rProgrammedSpindleSpeed_In) < (rProgrammedSpindleSpeed_In * 0.02) THEN
            IF rX_hat[5] < 3.5 THEN (* Residual unbalance vibration acceptable *)
                bSpindle_At_Speed_Out := TRUE;
                tSpindleRampTimer := 0.0;
                eState := 6; (* Advance to Coolant Pressure Lock *)
            END_IF;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STAGE 6: FLOOD_AND_MQL_COOLANT_PRESSURE_LOCK
     * High-pressure through-spindle coolant (TSC) engagement; lock delivery header pressure at 70 bar.
     * ----------------------------------------------------------------------------------------------------------------- *)
    6:
        tCoolantLockTimer := tCoolantLockTimer + 1.0;
        rCoolant_PropValve_Cmd_Out := 85.0;

        IF (rCoolantPressure_PT701_In >= 65.0) AND (rCoolantFlow_FT702_In >= 25.0) AND (tCoolantLockTimer > 2500.0) THEN
            tCoolantLockTimer := 0.0;
            eState := 7; (* Engage High-Speed 5-Axis Milling Run *)
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STAGE 7: HIGH_SPEED_5AXIS_CONTOUR_MILLING_RUN
     * Continuous 5-axis aerospace trajectory interpolation with active MPC contour regulation.
     * ----------------------------------------------------------------------------------------------------------------- *)
    7:
        tMillingElapsedTimer := tMillingElapsedTimer + 1.0;
        bMachine_Ready_Out := TRUE;

        (* Check for chatter vibration onset *)
        IF rX_hat[5] > 28.0 THEN
            eState := 8; (* Divert to Active Regenerative Chatter Damping & SSM *)
        (* Check for thermal elongation accumulation *)
        ELSIF ABS(rX_hat[4]) > 20.0 THEN
            eState := 9; (* Divert to Spindle Thermal Live Compensation *)
        (* Check for tool wear acoustic evaluation interval (every 30 seconds of milling) *)
        ELSIF tMillingElapsedTimer > 30000.0 THEN
            tMillingElapsedTimer := 0.0;
            eState := 10; (* In-process Tool Wear Evaluation *)
        (* Tool change request or part program completion *)
        ELSIF bTool_Change_Request_In OR bPartProgram_M30_End_In THEN
            eState := 11; (* Controlled Deceleration and Orientation *)
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STAGE 8: ACTIVE_REGENERATIVE_CHATTER_DAMPING_SSM
     * High-energy chatter attenuation via active magnetic damping counter-forces and Spindle Speed Modulation.
     * ----------------------------------------------------------------------------------------------------------------- *)
    8:
        bChatter_Suppression_Active_Out := TRUE;

        (* Monitor vibration suppression *)
        IF rX_hat[5] < 12.0 THEN
            (* Chatter suppressed; return to standard contour milling *)
            eState := 7;
        ELSIF rX_hat[5] > rLim_Chatter_HH THEN
            (* Chatter runaway: trigger emergency deceleration *)
            eState := 11;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STAGE 9: SPINDLE_THERMAL_ELONGATION_LIVE_COMPENSATION
     * Dynamic piezo actuator micro-displacement tracking and CNC origin dynamic coordinate shift.
     * ----------------------------------------------------------------------------------------------------------------- *)
    9:
        bThermal_Comp_Active_Out := TRUE;

        (* Return to contour milling once compensation settles within < 1.0 um error *)
        IF ABS(rX_hat[4] + rPiezo_Z_Thermal_Offset_Out) < 1.0 THEN
            eState := 7;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STAGE 10: IN_PROCESS_TOOL_WEAR_ACOUSTIC_EVALUATION
     * Continuous FFT harmonic power ratio and torque-to-feedrate ratio evaluation for micro-chipping and wear.
     * ----------------------------------------------------------------------------------------------------------------- *)
    10:
        tWearAcousticTimer := tWearAcousticTimer + 1.0;
        rToolLife_Elapsed_Min[iToolCurrentID] := rToolLife_Elapsed_Min[iToolCurrentID] + (1.0 / 60000.0);

        IF tWearAcousticTimer > 1000.0 THEN
            tWearAcousticTimer := 0.0;
            (* Check if cutting torque exceeds 180% of sharp tool baseline *)
            IF (rX_hat[7] > 38.0) OR (rToolLife_Elapsed_Min[iToolCurrentID] > 120.0) THEN
                bToolWearLimitTrip := TRUE;
                eState := 11; (* Worn tool: decelerate and trigger tool swap *)
            ELSE
                eState := 7; (* Tool healthy: return to milling *)
            END_IF;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STAGE 11: SPINDLE_CONTROLLED_DECELERATION_AND_ORIENT
     * Synchronized regenerative electrical dynamic braking and precise spindle orientation (M19 at 0.0 deg).
     * ----------------------------------------------------------------------------------------------------------------- *)
    11:
        tSpindleDecelTimer := tSpindleDecelTimer + 1.0;
        bSpindle_At_Speed_Out := FALSE;
        rSpindleSpeed_Direct_Cmd_Out := 0.0;
        rSpindleBrake_Torque_Cmd_Out := 65.0;
        rCoolant_PropValve_Cmd_Out := 0.0;

        IF (rSpindleActualSpeed_In < 10.0) AND (tSpindleDecelTimer > 3500.0) THEN
            bSpindle_Oriented_Out := TRUE;
            rSpindleBrake_Torque_Cmd_Out := 100.0; (* Orientation lock *)
            tSpindleDecelTimer := 0.0;

            IF bTool_Change_Request_In OR bToolWearLimitTrip THEN
                eState := 12; (* Proceed to Automatic Tool Changer Swap *)
            ELSIF bPartProgram_M30_End_In THEN
                eState := 0;  (* Program completed: return to standby *)
            ELSE
                eState := 0;
            END_IF;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STAGE 12: AUTOMATIC_TOOL_CHANGER_CAROUSEL_SWAP
     * HSK-A63 toolholder hydraulic unclamp (18 kN pull force), carousel arm indexing, mechanical swap.
     * ----------------------------------------------------------------------------------------------------------------- *)
    12:
        tATCSwapTimer := tATCSwapTimer + 1.0;

        IF tATCSwapTimer < 1500.0 THEN
            rDrawbarCylinder_Cmd_Out := 100.0; (* Hydraulic unclamp *)
        ELSIF tATCSwapTimer < 4500.0 THEN
            (* Carousel double-arm mechanical swap simulation *)
            iToolCurrentID := iTarget_Tool_Slot_In;
        ELSE
            rDrawbarCylinder_Cmd_Out := 0.0;   (* Re-clamp new toolholder *)
            bATC_Cycle_Complete_Out := TRUE;
            bToolWearLimitTrip := FALSE;
            tATCSwapTimer := 0.0;
            eState := 2; (* Calibrate new tool offset on laser touch probe *)
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STAGE 13: EMERGENCY_TOOL_BREAK_OR_COLLISION_RETRACT_TRIP
     * Ultra-fast Z-axis upward rapid retraction (+150 mm/s), emergency dynamic braking, gantry safe torque off.
     * ----------------------------------------------------------------------------------------------------------------- *)
    13:
        tEmergencyRetractTimer := tEmergencyRetractTimer + 1.0;
        bEmergency_Retract_Active_Out := TRUE;
        bGeneral_Fault_Alarm_Out := TRUE;
        bMachine_Ready_Out := FALSE;
        bSpindle_At_Speed_Out := FALSE;

        (* Kill spindle and coolant *)
        rSpindleSpeed_Direct_Cmd_Out := 0.0;
        rSpindleBrake_Torque_Cmd_Out := 100.0;
        rCoolant_PropValve_Cmd_Out := 0.0;
        rActiveDamping_Bias_Cmd_Out := 0.0;

        (* Master-slave gantry zero torque *)
        rMaster_X_Torque_Cmd_Out := 0.0;
        rSlave_X_Torque_Cmd_Out := 0.0;

        (* Manual operator fault reset pushbutton handling *)
        IF bManual_Fault_Reset_In AND bEmergencyStop_Circuit_OK_In AND bSafetyGate_Interlock_OK_In THEN
            bFastToolBreak_Trip := FALSE;
            bFastCollision_Trip := FALSE;
            bFirstOutLatched := FALSE;
            iFirstOutID := 0;
            bGeneral_Fault_Alarm_Out := FALSE;
            bEmergency_Retract_Active_Out := FALSE;
            tEmergencyRetractTimer := 0.0;
            eState := 0; (* Reset back to Standby *)
        END_IF;
END_CASE;

iFSM_Current_State_Out := eState;
""")

    # -------------------------------------------------------------------------
    # 9. PHASE 5: ISA-18.2 MULTI-TIER PROCESS ALARMS, FAST TOOL BREAK & BIT-PACKED TELEMETRY
    # -------------------------------------------------------------------------
    st.append("""
(* =====================================================================================================================
 * PHASE 5: ISA-18.2 MULTI-TIER PROCESS ALARMS, FAST TOOL BREAK DETECTION & TELEMETRY
 * - Sub-1 ms Fast Tool Fracture & Collision Detection via 5-tap rolling derivative FIFO buffers.
 * - ISA-18.2 Four-tier alarms (HH, H, L, LL) with deadband clearance hysteresis for 9 variables.
 * - Deterministic First-Out alarm sequence latching.
 * - 32-bit bit-packed industrial telemetry words: dwStatusWord1, dwStatusWord2, dwAlarmWord1, dwAlarmWord2, dwFirstOutWord.
 * ===================================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------------------------
 * 1. SUB-1 MS FAST TOOL FRACTURE & COLLISION IMPACT DETECTION
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Shift FIFO history buffers *)
FOR iIterIdx := 4 TO 1 BY -1 DO
    rTorque_History[iIterIdx] := rTorque_History[iIterIdx - 1];
    rAccel_History[iIterIdx]  := rAccel_History[iIterIdx - 1];
END_FOR;
rTorque_History[0] := rX_hat[7];
rAccel_History[0]  := rX_hat[5];

(* Fast derivative calculations across 2 ms window *)
rTorque_Drop_Rate := (rTorque_History[2] - rTorque_History[0]) * 0.5; (* Nm/ms decay *)
rAccel_Spike_Rate := (rAccel_History[0] - rAccel_History[2]) * 0.5;  (* m/s2/ms surge *)

(* Tool Break Detection: High cutting force suddenly collapses while tool in cut *)
IF (eState = 7 OR eState = 8) AND (rTorque_History[2] > 18.0) AND (rTorque_Drop_Rate > 12.0) THEN
    bFastToolBreak_Trip := TRUE;
    bTool_Broken_Tripped_Out := TRUE;
    IF NOT bFirstOutLatched THEN
        iFirstOutID := 101; (* Code 101: Fast Tool Fracture Trip *)
        bFirstOutLatched := TRUE;
    END_IF;
END_IF;

(* Collision Impact Detection: Instantaneous extreme acceleration spike *)
IF (rAccel_History[0] > 75.0) OR (rAccel_Spike_Rate > 45.0) THEN
    bFastCollision_Trip := TRUE;
    IF NOT bFirstOutLatched THEN
        iFirstOutID := 102; (* Code 102: Mechanical Machine Collision Impact Trip *)
        bFirstOutLatched := TRUE;
    END_IF;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * 2. ISA-18.2 MULTI-TIER PROCESS ALARMS WITH DEADBAND CLEARANCE HYSTERESIS
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Variable 1: Gantry Master-Slave Skew Error [um] *)
IF rX_hat[1] >= rLim_Skew_HH THEN
    bAlarm_Skew_HH_Latched := TRUE;
    IF NOT bFirstOutLatched THEN iFirstOutID := 1; bFirstOutLatched := TRUE; END_IF;
ELSIF rX_hat[1] <= (rLim_Skew_HH - rDeadband_Skew) THEN
    bAlarm_Skew_HH_Latched := FALSE;
END_IF;

IF rX_hat[1] >= rLim_Skew_H THEN
    bAlarm_Skew_H_Latched := TRUE;
ELSIF rX_hat[1] <= (rLim_Skew_H - rDeadband_Skew) THEN
    bAlarm_Skew_H_Latched := FALSE;
END_IF;

(* Variable 2: Spindle Front Bearing Temperature [deg C] *)
IF rX_hat[2] >= rLim_Bear201_HH THEN
    bAlarm_Bear201_HH_Latched := TRUE;
    IF NOT bFirstOutLatched THEN iFirstOutID := 2; bFirstOutLatched := TRUE; END_IF;
ELSIF rX_hat[2] <= (rLim_Bear201_HH - rDeadband_Bear201) THEN
    bAlarm_Bear201_HH_Latched := FALSE;
END_IF;

IF rX_hat[2] >= rLim_Bear201_H THEN
    bAlarm_Bear201_H_Latched := TRUE;
ELSIF rX_hat[2] <= (rLim_Bear201_H - rDeadband_Bear201) THEN
    bAlarm_Bear201_H_Latched := FALSE;
END_IF;

(* Variable 3: Spindle Rear Bearing Temperature [deg C] *)
IF rX_hat[3] >= rLim_Bear202_HH THEN
    bAlarm_Bear202_HH_Latched := TRUE;
    IF NOT bFirstOutLatched THEN iFirstOutID := 3; bFirstOutLatched := TRUE; END_IF;
ELSIF rX_hat[3] <= (rLim_Bear202_HH - rDeadband_Bear202) THEN
    bAlarm_Bear202_HH_Latched := FALSE;
END_IF;

IF rX_hat[3] >= rLim_Bear202_H THEN
    bAlarm_Bear202_H_Latched := TRUE;
ELSIF rX_hat[3] <= (rLim_Bear202_H - rDeadband_Bear202) THEN
    bAlarm_Bear202_H_Latched := FALSE;
END_IF;

(* Variable 4: Spindle Z-Axis Dynamic Thermal Elongation [um] *)
IF ABS(rX_hat[4]) >= rLim_ZElong_HH THEN
    bAlarm_ZElong_HH_Latched := TRUE;
    IF NOT bFirstOutLatched THEN iFirstOutID := 4; bFirstOutLatched := TRUE; END_IF;
ELSIF ABS(rX_hat[4]) <= (rLim_ZElong_HH - rDeadband_ZElong) THEN
    bAlarm_ZElong_HH_Latched := FALSE;
END_IF;

IF ABS(rX_hat[4]) >= rLim_ZElong_H THEN
    bAlarm_ZElong_H_Latched := TRUE;
ELSIF ABS(rX_hat[4]) <= (rLim_ZElong_H - rDeadband_ZElong) THEN
    bAlarm_ZElong_H_Latched := FALSE;
END_IF;

(* Variable 5: Tool Center Point Chatter Vibration [m/s2] *)
IF rX_hat[5] >= rLim_Chatter_HH THEN
    bAlarm_Chatter_HH_Latched := TRUE;
    IF NOT bFirstOutLatched THEN iFirstOutID := 5; bFirstOutLatched := TRUE; END_IF;
ELSIF rX_hat[5] <= (rLim_Chatter_HH - rDeadband_Chatter) THEN
    bAlarm_Chatter_HH_Latched := FALSE;
END_IF;

IF rX_hat[5] >= rLim_Chatter_H THEN
    bAlarm_Chatter_H_Latched := TRUE;
ELSIF rX_hat[5] <= (rLim_Chatter_H - rDeadband_Chatter) THEN
    bAlarm_Chatter_H_Latched := FALSE;
END_IF;

(* Variable 6: Milling Dynamic Cutting Force Magnitude [N] *)
IF rX_hat[6] >= rLim_CutForce_HH THEN
    bAlarm_CutForce_HH_Latched := TRUE;
    IF NOT bFirstOutLatched THEN iFirstOutID := 6; bFirstOutLatched := TRUE; END_IF;
ELSIF rX_hat[6] <= (rLim_CutForce_HH - rDeadband_CutForce) THEN
    bAlarm_CutForce_HH_Latched := FALSE;
END_IF;

IF rX_hat[6] >= rLim_CutForce_H THEN
    bAlarm_CutForce_H_Latched := TRUE;
ELSIF rX_hat[6] <= (rLim_CutForce_H - rDeadband_CutForce) THEN
    bAlarm_CutForce_H_Latched := FALSE;
END_IF;

(* Variable 7: Spindle Motor Inverter Current [A] *)
IF rTMR_Current501_Voted >= rLim_Current_HH THEN
    bAlarm_Current_HH_Latched := TRUE;
    IF NOT bFirstOutLatched THEN iFirstOutID := 7; bFirstOutLatched := TRUE; END_IF;
ELSIF rTMR_Current501_Voted <= (rLim_Current_HH - rDeadband_Current) THEN
    bAlarm_Current_HH_Latched := FALSE;
END_IF;

IF rTMR_Current501_Voted >= rLim_Current_H THEN
    bAlarm_Current_H_Latched := TRUE;
ELSIF rTMR_Current501_Voted <= (rLim_Current_H - rDeadband_Current) THEN
    bAlarm_Current_H_Latched := FALSE;
END_IF;

(* Variable 8: Through-Spindle Coolant Delivery Pressure [bar] *)
IF rCoolantPressure_PT701_In <= rLim_CoolPres_LL THEN
    bAlarm_CoolPres_LL_Latched := TRUE;
    IF NOT bFirstOutLatched THEN iFirstOutID := 8; bFirstOutLatched := TRUE; END_IF;
ELSIF rCoolantPressure_PT701_In >= (rLim_CoolPres_LL + rDeadband_CoolPres) THEN
    bAlarm_CoolPres_LL_Latched := FALSE;
END_IF;

IF rCoolantPressure_PT701_In <= rLim_CoolPres_L THEN
    bAlarm_CoolPres_L_Latched := TRUE;
ELSIF rCoolantPressure_PT701_In >= (rLim_CoolPres_L + rDeadband_CoolPres) THEN
    bAlarm_CoolPres_L_Latched := FALSE;
END_IF;

(* Variable 9: Spindle Bearing Oil-Air Lubrication Pressure [bar] *)
IF rOilMistPressure_PT801_In <= rLim_OilMist_LL THEN
    bAlarm_OilMist_LL_Latched := TRUE;
    IF NOT bFirstOutLatched THEN iFirstOutID := 9; bFirstOutLatched := TRUE; END_IF;
ELSIF rOilMistPressure_PT801_In >= (rLim_OilMist_LL + rDeadband_OilMist) THEN
    bAlarm_OilMist_LL_Latched := FALSE;
END_IF;

IF rOilMistPressure_PT801_In <= rLim_OilMist_L THEN
    bAlarm_OilMist_L_Latched := TRUE;
ELSIF rOilMistPressure_PT801_In >= (rLim_OilMist_L + rDeadband_OilMist) THEN
    bAlarm_OilMist_L_Latched := FALSE;
END_IF;

(* General fault master latch *)
IF bAlarm_Skew_HH_Latched OR bAlarm_Bear201_HH_Latched OR bAlarm_Bear202_HH_Latched OR
   bAlarm_ZElong_HH_Latched OR bAlarm_Chatter_HH_Latched OR bAlarm_CutForce_HH_Latched OR
   bAlarm_Current_HH_Latched OR bAlarm_CoolPres_LL_Latched OR bAlarm_OilMist_LL_Latched OR
   bFastToolBreak_Trip OR bFastCollision_Trip THEN
    bGeneral_Fault_Alarm_Out := TRUE;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * 3. ASSEMBLE BIT-PACKED 32-BIT INDUSTRIAL TELEMETRY WORDS
 * --------------------------------------------------------------------------------------------------------------------- *)
(* dwStatusWord1: Primary Operating Status & Actuator State *)
dwStatusWord1_Out := 16#00000000;
IF bMachine_Ready_Out              THEN dwStatusWord1_Out := dwStatusWord1_Out OR 16#00000001; END_IF;
IF bSpindle_At_Speed_Out           THEN dwStatusWord1_Out := dwStatusWord1_Out OR 16#00000002; END_IF;
IF bChatter_Suppression_Active_Out THEN dwStatusWord1_Out := dwStatusWord1_Out OR 16#00000004; END_IF;
IF bThermal_Comp_Active_Out        THEN dwStatusWord1_Out := dwStatusWord1_Out OR 16#00000008; END_IF;
IF bGantry_Skew_Corrected_Out      THEN dwStatusWord1_Out := dwStatusWord1_Out OR 16#00000010; END_IF;
IF bSpindle_Oriented_Out           THEN dwStatusWord1_Out := dwStatusWord1_Out OR 16#00000020; END_IF;
IF bATC_Cycle_Complete_Out         THEN dwStatusWord1_Out := dwStatusWord1_Out OR 16#00000040; END_IF;
IF bEmergency_Retract_Active_Out   THEN dwStatusWord1_Out := dwStatusWord1_Out OR 16#00000080; END_IF;
IF bSafetyGate_Interlock_OK_In     THEN dwStatusWord1_Out := dwStatusWord1_Out OR 16#00000100; END_IF;
IF bEmergencyStop_Circuit_OK_In    THEN dwStatusWord1_Out := dwStatusWord1_Out OR 16#00000200; END_IF;
IF bHydraulicPower_Ready_In        THEN dwStatusWord1_Out := dwStatusWord1_Out OR 16#00000400; END_IF;
IF bPneumatics_MainAir_OK_In       THEN dwStatusWord1_Out := dwStatusWord1_Out OR 16#00000800; END_IF;
(* Pack active FSM state in bits 16..23 *)
dwStatusWord1_Out := dwStatusWord1_Out OR SHL(INT_TO_DWORD(eState), 16);
(* Pack active tool ID in bits 24..31 *)
dwStatusWord1_Out := dwStatusWord1_Out OR SHL(INT_TO_DWORD(iToolCurrentID), 24);

(* dwStatusWord2: Instrumentation Health & TMR Degradation Modes *)
dwStatusWord2_Out := 16#00000000;
dwStatusWord2_Out := dwStatusWord2_Out OR SHL(INT_TO_DWORD(iTMR_Scale101_DegradeMode), 0);
dwStatusWord2_Out := dwStatusWord2_Out OR SHL(INT_TO_DWORD(iTMR_Bear201_DegradeMode), 4);
dwStatusWord2_Out := dwStatusWord2_Out OR SHL(INT_TO_DWORD(iTMR_Disp301_DegradeMode), 8);
dwStatusWord2_Out := dwStatusWord2_Out OR SHL(INT_TO_DWORD(iTMR_Chatter401_DegradeMode), 12);
dwStatusWord2_Out := dwStatusWord2_Out OR SHL(INT_TO_DWORD(iTMR_Current501_DegradeMode), 16);
IF bAlarm_TMR_Scale101_Discr       THEN dwStatusWord2_Out := dwStatusWord2_Out OR 16#00100000; END_IF;
IF bAlarm_TMR_Bear201_Discr        THEN dwStatusWord2_Out := dwStatusWord2_Out OR 16#00200000; END_IF;
IF bAlarm_TMR_Disp301_Discr        THEN dwStatusWord2_Out := dwStatusWord2_Out OR 16#00400000; END_IF;
IF bAlarm_TMR_Chatter401_Discr     THEN dwStatusWord2_Out := dwStatusWord2_Out OR 16#00800000; END_IF;
IF bAlarm_TMR_Current501_Discr     THEN dwStatusWord2_Out := dwStatusWord2_Out OR 16#01000000; END_IF;
IF bToolWearLimitTrip              THEN dwStatusWord2_Out := dwStatusWord2_Out OR 16#02000000; END_IF;

(* dwAlarmWord1: Priority 1 & 2 Critical Safety Trips & Process HH/LL Faults *)
dwAlarmWord1_Out := 16#00000000;
IF bFastToolBreak_Trip             THEN dwAlarmWord1_Out := dwAlarmWord1_Out OR 16#00000001; END_IF;
IF bFastCollision_Trip             THEN dwAlarmWord1_Out := dwAlarmWord1_Out OR 16#00000002; END_IF;
IF bAlarm_Skew_HH_Latched          THEN dwAlarmWord1_Out := dwAlarmWord1_Out OR 16#00000004; END_IF;
IF bAlarm_Bear201_HH_Latched       THEN dwAlarmWord1_Out := dwAlarmWord1_Out OR 16#00000008; END_IF;
IF bAlarm_Bear202_HH_Latched       THEN dwAlarmWord1_Out := dwAlarmWord1_Out OR 16#00000010; END_IF;
IF bAlarm_ZElong_HH_Latched        THEN dwAlarmWord1_Out := dwAlarmWord1_Out OR 16#00000020; END_IF;
IF bAlarm_Chatter_HH_Latched       THEN dwAlarmWord1_Out := dwAlarmWord1_Out OR 16#00000040; END_IF;
IF bAlarm_CutForce_HH_Latched      THEN dwAlarmWord1_Out := dwAlarmWord1_Out OR 16#00000080; END_IF;
IF bAlarm_Current_HH_Latched       THEN dwAlarmWord1_Out := dwAlarmWord1_Out OR 16#00000100; END_IF;
IF bAlarm_CoolPres_LL_Latched      THEN dwAlarmWord1_Out := dwAlarmWord1_Out OR 16#00000200; END_IF;
IF bAlarm_OilMist_LL_Latched       THEN dwAlarmWord1_Out := dwAlarmWord1_Out OR 16#00000400; END_IF;
IF bGeneral_Fault_Alarm_Out        THEN dwAlarmWord1_Out := dwAlarmWord1_Out OR 16#80000000; END_IF;

(* dwAlarmWord2: Priority 3 & 4 Operational Warnings & Quality Limit Deviations *)
dwAlarmWord2_Out := 16#00000000;
IF bAlarm_Skew_H_Latched           THEN dwAlarmWord2_Out := dwAlarmWord2_Out OR 16#00000001; END_IF;
IF bAlarm_Bear201_H_Latched        THEN dwAlarmWord2_Out := dwAlarmWord2_Out OR 16#00000002; END_IF;
IF bAlarm_Bear202_H_Latched        THEN dwAlarmWord2_Out := dwAlarmWord2_Out OR 16#00000004; END_IF;
IF bAlarm_ZElong_H_Latched         THEN dwAlarmWord2_Out := dwAlarmWord2_Out OR 16#00000008; END_IF;
IF bAlarm_Chatter_H_Latched        THEN dwAlarmWord2_Out := dwAlarmWord2_Out OR 16#00000010; END_IF;
IF bAlarm_CutForce_H_Latched       THEN dwAlarmWord2_Out := dwAlarmWord2_Out OR 16#00000020; END_IF;
IF bAlarm_Current_H_Latched        THEN dwAlarmWord2_Out := dwAlarmWord2_Out OR 16#00000040; END_IF;
IF bAlarm_CoolPres_L_Latched       THEN dwAlarmWord2_Out := dwAlarmWord2_Out OR 16#00000080; END_IF;
IF bAlarm_OilMist_L_Latched        THEN dwAlarmWord2_Out := dwAlarmWord2_Out OR 16#00000100; END_IF;

(* dwFirstOutWord: Root-Cause Alarm Sequence Identifier *)
dwFirstOutWord_Out := INT_TO_DWORD(iFirstOutID);

END_FUNCTION_BLOCK
""")

    return "".join(st)

if __name__ == "__main__":
    code = generate_iec_st()
    print(f"Generated Structured Text length: {len(code)} characters")
