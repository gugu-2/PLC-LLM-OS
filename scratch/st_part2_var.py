# -*- coding: utf-8 -*-

part2_var = """VAR
    (* ===================================================================================== *)
    (* 1.0 PHYSICAL, GEOMETRIC & KINEMATIC CONSTANTS                                         *)
    (* ===================================================================================== *)
    c_rScanTime_Ts                  : REAL := 0.005;    (* Discrete Real-Time Scan Cycle Time (5 milliseconds) [s] *)
    c_rGravity_g                    : REAL := 9.80665;  (* Standard Acceleration of Gravity [m/s^2] *)
    c_rHoistCarriageTareMass_kg     : REAL := 3200.0;   (* Hoist Structural Carriage Platform Unladen Mass [kg] *)
    c_rCounterweightMass_kg         : REAL := 4300.0;   (* Hoist Counterweight Mass (Carriage + 50% Rated Payload) [kg] *)
    c_rTractionSheaveRadius_m       : REAL := 0.320;    (* Direct-Drive Motor Traction Sheave Pitch Radius [m] *)
    c_rRopeElasticModulus_N_mm2     : REAL := 115000.0; (* Steel Wire Traction Rope Effective Elastic Modulus [N/mm^2] *)
    c_rRopeCrossSection_mm2         : REAL := 420.0;    (* Total Cross-Sectional Metallic Area of 6x19 IWRC Ropes [mm^2] *)
    c_rRopeLinearDensity_kg_m       : REAL := 3.45;     (* Suspended Wire Ropes Linear Mass Density [kg/m] *)
    c_rCableBaseStiffness_N_m       : REAL := 145000.0; (* Equivalent Cable Longitudinal Spring Stiffness [N/m] *)
    c_rCableStructuralDamping_Ns_m  : REAL := 3200.0;   (* Cable Internal Viscous Damping Coefficient [N*s/m] *)
    c_rPMSM_RatedTorque_Nm          : REAL := 1450.0;   (* Hoist 75kW PMSM Continuous Rated Electromagnetic Torque [N*m] *)
    c_rPMSM_PeakTorque_Nm           : REAL := 2900.0;   (* Hoist PMSM Transient Acceleration Peak Torque Limit [N*m] *)
    c_rPMSM_RotorInertia_kg_m2      : REAL := 42.5;     (* PMSM Rotor Shaft & Primary Sheave Rotational Inertia [kg*m^2] *)
    c_rShuttleTareMass_kg           : REAL := 850.0;    (* Horizontal Rack Aisle Shuttle Cart Unladen Mass [kg] *)
    c_rShuttleRatedForce_N          : REAL := 4800.0;   (* Shuttle Rack-and-Pinion Drive Continuous Traction Force [N] *)

    (* Silo Level Vertical Coordinates (15 Parking Levels, Ground to Penthouse) [mm] *)
    aFloorElevations_mm             : ARRAY[1..15] OF REAL := [
        0.0,     2600.0,  5200.0,  7800.0,  10400.0,
        13000.0, 15600.0, 18200.0, 20800.0, 23400.0,
        26000.0, 28600.0, 31200.0, 33800.0, 36400.0
    ];

    (* Silo Rack Bay Column Horizontal Coordinates (24 Bays per Aisle) [mm] *)
    aBayColumnPositions_mm          : ARRAY[1..24] OF REAL := [
        1800.0,  4200.0,  6600.0,  9000.0,  11400.0, 13800.0,
        16200.0, 18600.0, 21000.0, 23400.0, 25800.0, 28200.0,
        30600.0, 33000.0, 35400.0, 37800.0, 40200.0, 42600.0,
        45000.0, 47400.0, 49800.0, 52200.0, 54600.0, 57000.0
    ];

    (* Kinematic Motion Constraints for S-Curve Generation *)
    c_rHoistMaxSpeed_m_s            : REAL := 3.50;     (* Hoist Maximum Vertical Cruise Velocity [m/s] *)
    c_rHoistMaxAccel_m_s2           : REAL := 1.20;     (* Hoist Maximum Vertical Acceleration [m/s^2] *)
    c_rHoistMaxJerk_m_s3            : REAL := 2.50;     (* Hoist Maximum S-Curve Jerk Limit [m/s^3] *)
    c_rHoistLevelingSpeed_m_s       : REAL := 0.040;    (* Sub-Millimeter Terminal Docking Creep Speed [m/s] *)
    c_rShuttleMaxSpeed_m_s          : REAL := 1.80;     (* Shuttle Maximum Horizontal Velocity [m/s] *)
    c_rShuttleMaxAccel_m_s2         : REAL := 0.80;     (* Shuttle Maximum Horizontal Acceleration [m/s^2] *)
    c_rShuttleMaxJerk_m_s3          : REAL := 2.00;     (* Shuttle Maximum Horizontal Jerk Limit [m/s^3] *)

    (* Sub-Millimeter Floor Leveling & Mechanical Tolerance Bounds *)
    c_rFloorLevelTolerance_mm       : REAL := 0.50;     (* Sub-Millimeter Floor Docking Permissive Window (+/- 0.5 mm) [mm] *)
    c_rShuttleDockTolerance_mm      : REAL := 1.50;     (* Shuttle Rack Bay Alignment Window (+/- 1.5 mm) [mm] *)
    c_rMaxAllowableSlack_kN         : REAL := 8.0;      (* Minimum Allowable Cable Tension (Slack Rope Trip Threshold) [kN] *)

    (* Cabin Vehicle Dimensional Envelope Limits *)
    c_rMaxVehicleLength_mm          : REAL := 5300.0;   (* Absolute Maximum Vehicle Length Permitted in Silo [mm] *)
    c_rMaxVehicleWidth_mm           : REAL := 2150.0;   (* Absolute Maximum Vehicle Width Permitted in Silo [mm] *)
    c_rMaxVehicleHeight_mm          : REAL := 2050.0;   (* Absolute Maximum Vehicle Height Permitted in Silo [mm] *)
    c_rMaxVehicleMass_kg            : REAL := 2800.0;   (* Maximum Permissible Gross Vehicle Mass [kg] *)
    c_rMinVehicleMass_kg            : REAL := 750.0;    (* Minimum Vehicle Mass Threshold (Detects Empty Pallet) [kg] *)

    (* ===================================================================================== *)
    (* 2.0 TRIPLE MODULAR REDUNDANCY (2oo3) VOTING REGISTERS & DISCREPANCY TIMERS           *)
    (* Dynamic inter-channel deviation tracking, median selection, and bumpless degradation  *)
    (* ===================================================================================== *)
    (* Group 1: Hoist Vertical Optical Laser Distance Meters [mm] *)
    rVotedHoistLaser_mm             : REAL := 0.0;
    bHoistLaser_Degraded            : BOOL := FALSE;
    bHoistLaser_Fault               : BOOL := FALSE;
    rHoistLaser_Tol_mm              : REAL := 5.0;      (* Inter-Laser Spread Trip Threshold [mm] *)
    rTimer_HoistLaser_Discrep       : REAL := 0.0;

    (* Group 2: Hoist Rotary Sheave Absolute Optical Encoders [mm] *)
    rVotedHoistEncoder_mm           : REAL := 0.0;
    bHoistEncoder_Degraded          : BOOL := FALSE;
    bHoistEncoder_Fault             : BOOL := FALSE;
    rHoistEncoder_Tol_mm            : REAL := 3.0;      (* Inter-Encoder Spread Trip Threshold [mm] *)
    rTimer_HoistEncoder_Discrep     : REAL := 0.0;

    (* Cross-Correlation: Optical Laser Elevation vs Rotary Sheave Feedback (Rope Slip) *)
    rLaserVsEncoderDelta_mm         : REAL := 0.0;
    c_rMaxRopeSlipDeviation_mm      : REAL := 15.0;     (* Max Allowable Slip Divergence [mm] *)
    rTimer_RopeSlip_Discrep         : REAL := 0.0;
    bTractionRopeSlipWarning        : BOOL := FALSE;

    (* Group 3: Horizontal Shuttle Optical Distance Meters [mm] *)
    rVotedShuttleLaser_mm           : REAL := 1800.0;
    bShuttleLaser_Degraded          : BOOL := FALSE;
    bShuttleLaser_Fault             : BOOL := FALSE;
    rShuttleLaser_Tol_mm            : REAL := 4.0;      (* Shuttle Laser Spread Tolerance [mm] *)
    rTimer_ShuttleLaser_Discrep     : REAL := 0.0;

    (* Group 4: Entry Cabin Vehicle Weighing Platform Load Cells [kg] *)
    rVotedPlatformWeight_kg         : REAL := 0.0;
    bLoadCell_Degraded              : BOOL := FALSE;
    bLoadCell_Fault                 : BOOL := FALSE;
    rLoadCell_Tol_kg                : REAL := 45.0;     (* Inter-LoadCell Spread Tolerance [kg] *)
    rTimer_LoadCell_Discrep         : REAL := 0.0;

    (* Discrepancy Timeouts & Inter-Channel Differences *)
    c_rMaxSensorDiscrepTime_s       : REAL := 0.200;    (* Discrepancy Persistence Trip Limit (200 ms) [s] *)
    rDiffAB                         : REAL := 0.0;
    rDiffBC                         : REAL := 0.0;
    rDiffCA                         : REAL := 0.0;
    bHealthyA                       : BOOL := TRUE;
    bHealthyB                       : BOOL := TRUE;
    bHealthyC                       : BOOL := TRUE;

    (* ===================================================================================== *)
    (* 3.0 COMPLETE DISCRETE STATE-SPACE CYBER-PHYSICAL MATRICES (Ad, Bd, Cd, Dd)           *)
    (* Discretized continuous mechanical and electrodynamic system at Ts = 0.005 s:          *)
    (* States x = [Delta_z (mm), Delta_v (mm/s), Delta_delta (mm), Delta_dot_delta (mm/s),  *)
    (*             Delta_x_shuttle (mm), Delta_v_shuttle (mm/s),                            *)
    (*             Delta_T_elec (Nm), Delta_V_dc (V)]'                                      *)
    (* Controls u = [Delta_u_hoist (Nm), Delta_u_shuttle (Nm),                              *)
    (*               Delta_u_damper (Nm), Delta_u_regen (kW)]'                              *)
    (* Outputs y = [Delta_z (mm), Delta_delta (mm), Delta_x_shuttle (mm), Delta_V_dc (V)]'   *)
    (* ===================================================================================== *)
    (* Discrete State Transition Matrix Ad (8x8) *)
    Ad_11 : REAL := 0.9998; Ad_12 : REAL := 0.0049; Ad_13 : REAL := 0.0002; Ad_14 : REAL := 0.0000; Ad_15 : REAL := 0.0000; Ad_16 : REAL := 0.0000; Ad_17 : REAL := 0.0001; Ad_18 : REAL := 0.0000;
    Ad_21 : REAL := -0.0580; Ad_22 : REAL := 0.9850; Ad_23 : REAL := 0.0820; Ad_24 : REAL := 0.0035; Ad_25 : REAL := 0.0000; Ad_26 : REAL := 0.0000; Ad_27 : REAL := 0.0245; Ad_28 : REAL := 0.0000;
    Ad_31 : REAL := 0.0012; Ad_32 : REAL := -0.0008; Ad_33 : REAL := 0.9940; Ad_34 : REAL := 0.0048; Ad_35 : REAL := 0.0000; Ad_36 : REAL := 0.0000; Ad_37 : REAL := -0.0015; Ad_38 : REAL := 0.0000;
    Ad_41 : REAL := 0.0240; Ad_42 : REAL := -0.0950; Ad_43 : REAL := -0.2850; Ad_44 : REAL := 0.9620; Ad_45 : REAL := 0.0000; Ad_46 : REAL := 0.0000; Ad_47 : REAL := -0.0480; Ad_48 : REAL := 0.0000;
    Ad_51 : REAL := 0.0000; Ad_52 : REAL := 0.0000; Ad_53 : REAL := 0.0000; Ad_54 : REAL := 0.0000; Ad_55 : REAL := 0.9999; Ad_56 : REAL := 0.0050; Ad_57 : REAL := 0.0000; Ad_58 : REAL := 0.0000;
    Ad_61 : REAL := 0.0000; Ad_62 : REAL := 0.0000; Ad_63 : REAL := 0.0000; Ad_64 : REAL := 0.0000; Ad_65 : REAL := -0.0420; Ad_66 : REAL := 0.9880; Ad_67 : REAL := 0.0000; Ad_68 : REAL := 0.0000;
    Ad_71 : REAL := 0.0000; Ad_72 : REAL := -0.0150; Ad_73 : REAL := 0.0000; Ad_74 : REAL := 0.0000; Ad_75 : REAL := 0.0000; Ad_76 : REAL := 0.0000; Ad_77 : REAL := 0.8950; Ad_78 : REAL := 0.0025;
    Ad_81 : REAL := 0.0000; Ad_82 : REAL := 0.0380; Ad_83 : REAL := 0.0000; Ad_84 : REAL := 0.0000; Ad_85 : REAL := 0.0000; Ad_86 : REAL := 0.0120; Ad_87 : REAL := -0.0280; Ad_88 : REAL := 0.9780;

    (* Discrete Input Coupling Matrix Bd (8x4) *)
    Bd_11 : REAL := 0.0001; Bd_12 : REAL := 0.0000; Bd_13 : REAL := 0.0000; Bd_14 : REAL := 0.0000;
    Bd_21 : REAL := 0.0280; Bd_22 : REAL := 0.0000; Bd_23 : REAL := 0.0150; Bd_24 : REAL := 0.0000;
    Bd_31 : REAL := -0.0018; Bd_32 : REAL := 0.0000; Bd_33 : REAL := -0.0025; Bd_34 : REAL := 0.0000;
    Bd_41 : REAL := -0.0520; Bd_42 : REAL := 0.0000; Bd_43 : REAL := -0.0880; Bd_44 : REAL := 0.0000;
    Bd_51 : REAL := 0.0000; Bd_52 : REAL := 0.0001; Bd_53 : REAL := 0.0000; Bd_54 : REAL := 0.0000;
    Bd_61 : REAL := 0.0000; Bd_62 : REAL := 0.0350; Bd_63 : REAL := 0.0000; Bd_64 : REAL := 0.0000;
    Bd_71 : REAL := 0.1250; Bd_72 : REAL := 0.0000; Bd_73 : REAL := 0.0450; Bd_74 : REAL := 0.0000;
    Bd_81 : REAL := -0.0450; Bd_82 : REAL := -0.0150; Bd_83 : REAL := 0.0000; Bd_84 : REAL := -0.1850;

    (* Discrete Output Measurement Matrix Cd (4x8) *)
    Cd_11 : REAL := 1.0000; Cd_12 : REAL := 0.0000; Cd_13 : REAL := 0.0000; Cd_14 : REAL := 0.0000; Cd_15 : REAL := 0.0000; Cd_16 : REAL := 0.0000; Cd_17 : REAL := 0.0000; Cd_18 : REAL := 0.0000;
    Cd_21 : REAL := 0.0000; Cd_22 : REAL := 0.0000; Cd_23 : REAL := 1.0000; Cd_24 : REAL := 0.0000; Cd_25 : REAL := 0.0000; Cd_26 : REAL := 0.0000; Cd_27 : REAL := 0.0000; Cd_28 : REAL := 0.0000;
    Cd_31 : REAL := 0.0000; Cd_32 : REAL := 0.0000; Cd_33 : REAL := 0.0000; Cd_34 : REAL := 0.0000; Cd_35 : REAL := 1.0000; Cd_36 : REAL := 0.0000; Cd_37 : REAL := 0.0000; Cd_38 : REAL := 0.0000;
    Cd_41 : REAL := 0.0000; Cd_42 : REAL := 0.0000; Cd_43 : REAL := 0.0000; Cd_44 : REAL := 0.0000; Cd_45 : REAL := 0.0000; Cd_46 : REAL := 0.0000; Cd_47 : REAL := 0.0000; Cd_48 : REAL := 1.0000;

    (* Discrete Direct Feedthrough Matrix Dd (4x4) *)
    Dd_11 : REAL := 0.0000; Dd_12 : REAL := 0.0000; Dd_13 : REAL := 0.0000; Dd_14 : REAL := 0.0000;
    Dd_21 : REAL := 0.0000; Dd_22 : REAL := 0.0000; Dd_23 : REAL := 0.0000; Dd_24 : REAL := 0.0000;
    Dd_31 : REAL := 0.0000; Dd_32 : REAL := 0.0000; Dd_33 : REAL := 0.0000; Dd_34 : REAL := 0.0000;
    Dd_41 : REAL := 0.0000; Dd_42 : REAL := 0.0000; Dd_43 : REAL := 0.0000; Dd_44 : REAL := 0.0000;

    (* Current State Excursion Registers x = [x1 .. x8]' *)
    x1_PosDev                       : REAL := 0.0;      (* Hoist Position Error Delta_z [mm] *)
    x2_VelDev                       : REAL := 0.0;      (* Hoist Velocity Error Delta_v [mm/s] *)
    x3_CableStretchDev              : REAL := 0.0;      (* Cable Elastic Stretch Deflection [mm] *)
    x4_CableStretchRateDev          : REAL := 0.0;      (* Cable Elastic Deflection Rate of Change [mm/s] *)
    x5_ShuttlePosDev                : REAL := 0.0;      (* Shuttle Position Error Delta_x [mm] *)
    x6_ShuttleVelDev                : REAL := 0.0;      (* Shuttle Velocity Error Delta_v_shuttle [mm/s] *)
    x7_TorqueDev                    : REAL := 0.0;      (* PMSM Torque Excursion Delta_T [Nm] *)
    x8_DCLinkDev                    : REAL := 0.0;      (* Inverter DC Link Voltage Deviation [V] *)

    (* 1-Step Ahead Predicted States x_pred = Ad * x + Bd * u *)
    x1_Pred : REAL := 0.0; x2_Pred : REAL := 0.0; x3_Pred : REAL := 0.0; x4_Pred : REAL := 0.0;
    x5_Pred : REAL := 0.0; x6_Pred : REAL := 0.0; x7_Pred : REAL := 0.0; x8_Pred : REAL := 0.0;

    (* 1-Step Ahead Predicted Outputs y_pred = Cd * x_pred + Dd * u *)
    y1_PredHoistPos                 : REAL := 0.0;      (* Predicted Carriage Elevation [mm] *)
    y2_PredCableStretch             : REAL := 0.0;      (* Predicted Dynamic Cable Stretch [mm] *)
    y3_PredShuttlePos               : REAL := 0.0;      (* Predicted Shuttle Position [mm] *)
    y4_PredDCLink                   : REAL := 680.0;    (* Predicted DC Link Potential [V] *)

    (* Dynamic Tracking Reference Setpoints *)
    rRef_HoistPos_mm                : REAL := 0.0;      (* Kinematic Trajectory Elevation Setpoint [mm] *)
    rRef_HoistVel_mm_s              : REAL := 0.0;      (* Kinematic Trajectory Velocity Setpoint [mm/s] *)
    rRef_CableStretch_mm            : REAL := 0.0;      (* Ideal Zero Oscillation Dynamic Equilibrium [mm] *)
    rRef_CableStretchRate_mm_s      : REAL := 0.0;      (* Zero Elastic Oscillation Velocity [mm/s] *)
    rRef_ShuttlePos_mm              : REAL := 1800.0;   (* Kinematic Shuttle Trajectory Setpoint [mm] *)
    rRef_ShuttleVel_mm_s            : REAL := 0.0;      (* Kinematic Shuttle Velocity Setpoint [mm/s] *)
    rRef_Torque_Nm                  : REAL := 0.0;      (* Equilibrium Counterbalance Torque Setpoint [Nm] *)
    rRef_DCLink_V                   : REAL := 680.0;    (* Nominal Regulated DC Bus Voltage [V] *)

    (* ===================================================================================== *)
    (* 4.0 MODEL PREDICTIVE CONTROL (MPC) QUADRATIC COST OPTIMIZER REGISTERS                 *)
    (* Minimizes J = x'*Q*x + u'*R*u + Delta_u'*Rd*Delta_u + x_N'*P*x_N                      *)
    (* ===================================================================================== *)
    (* State Tracking Error Penalties (Q) *)
    rMPC_Q1_HoistPos                : REAL := 120.0;    (* Hoist Position Error Penalty (High Priority) *)
    rMPC_Q2_HoistVel                : REAL := 45.0;     (* Hoist Velocity Tracking Penalty *)
    rMPC_Q3_CableStretch            : REAL := 95.0;     (* Cable Longitudinal Vibration Suppression Penalty *)
    rMPC_Q4_CableRate               : REAL := 60.0;     (* Cable Oscillation Damping Penalty *)
    rMPC_Q5_ShuttlePos              : REAL := 85.0;     (* Shuttle Aisle Position Tracking Penalty *)
    rMPC_Q6_ShuttleVel              : REAL := 30.0;     (* Shuttle Velocity Tracking Penalty *)
    rMPC_Q7_Torque                  : REAL := 15.0;     (* Torque Dynamic Overshoot Penalty *)
    rMPC_Q8_DCLink                  : REAL := 70.0;     (* DC Bus Overpotential Suppression Penalty *)

    (* Actuator Control Effort Penalties (R) *)
    rMPC_R1_HoistTorque             : REAL := 5.0;      (* Hoist PMSM Effort Penalty *)
    rMPC_R2_ShuttleServo            : REAL := 4.0;      (* Shuttle Drive Effort Penalty *)
    rMPC_R3_VibrationDamp           : REAL := 2.5;      (* Active Vibration Feedforward Torque Penalty *)
    rMPC_R4_RegenChopper            : REAL := 3.0;      (* Dynamic Braking Energy Dissipation Penalty *)

    (* Actuator Slew Rate Penalties (Rd) *)
    rMPC_Rd1_dHoistTorque           : REAL := 10.0;     (* Jerk / Stress Reduction on Traction Sheave *)
    rMPC_Rd2_dShuttleServo          : REAL := 8.0;      (* Rack-and-Pinion Gear Wear Prevention *)
    rMPC_Rd3_dVibrationDamp         : REAL := 2.0;      (* Fast Dynamic Anti-Vibration Injection Slew *)
    rMPC_Rd4_dRegenChopper          : REAL := 4.0;      (* DC Link Chopper Stress Prevention *)

    (* Terminal State Penalties (P) *)
    rMPC_P1_HoistPos                : REAL := 250.0;    (* Terminal Level Docking Sub-Millimeter Weight *)
    rMPC_P2_HoistVel                : REAL := 80.0;     (* Terminal Zero Velocity Arrival Weight *)
    rMPC_P3_CableStretch            : REAL := 150.0;    (* Terminal Cable Quiescence Weight *)
    rMPC_P4_CableRate               : REAL := 110.0;    (* Terminal Cable Damping Weight *)
    rMPC_P5_ShuttlePos              : REAL := 160.0;    (* Terminal Bay Column Alignment Weight *)
    rMPC_P6_ShuttleVel              : REAL := 60.0;     (* Terminal Shuttle Zero Speed Weight *)
    rMPC_P7_Torque                  : REAL := 25.0;     (* Terminal Motor Torque Equilibrium *)
    rMPC_P8_DCLink                  : REAL := 120.0;    (* Terminal Regulated DC Voltage Weight *)

    (* Analytical Gradient Elements g = Bd'*Q*(x_pred - x_ref) + R*u_prev + Rd*Delta_u *)
    rGrad1_HoistTorque              : REAL := 0.0;
    rGrad2_ShuttleServo             : REAL := 0.0;
    rGrad3_VibrationDamp            : REAL := 0.0;
    rGrad4_RegenChopper             : REAL := 0.0;

    (* Analytical Hessian Diagonal Elements H_ii = sum(Bd_ji^2 * Q_j) + R_i + Rd_i *)
    rHess11_HoistTorque             : REAL := 1.0;
    rHess22_ShuttleServo            : REAL := 1.0;
    rHess33_VibrationDamp           : REAL := 1.0;
    rHess44_RegenChopper            : REAL := 1.0;

    (* Calculated Optimal Control Adjustments Delta_u *)
    rDelta_u1_HoistTorque           : REAL := 0.0;
    rDelta_u2_ShuttleServo          : REAL := 0.0;
    rDelta_u3_VibrationDamp         : REAL := 0.0;
    rDelta_u4_RegenChopper          : REAL := 0.0;

    (* Actuator Prior Memory Storage *)
    rPrev_u1_HoistTorque            : REAL := 0.0;
    rPrev_u2_ShuttleServo           : REAL := 0.0;
    rPrev_u3_VibrationDamp          : REAL := 0.0;
    rPrev_u4_RegenChopper           : REAL := 0.0;
    rPrevDelta_u1                   : REAL := 0.0;
    rPrevDelta_u2                   : REAL := 0.0;
    rPrevDelta_u3                   : REAL := 0.0;
    rPrevDelta_u4                   : REAL := 0.0;

    (* Actuator Saturation & Rate Limits *)
    c_rMaxHoistTorque_Nm            : REAL := 2800.0;
    c_rMinHoistTorque_Nm            : REAL := -2800.0;
    c_rMaxShuttleServo_Nm           : REAL := 320.0;
    c_rMinShuttleServo_Nm           : REAL := -320.0;
    c_rMaxDampTorque_Nm             : REAL := 450.0;
    c_rMinDampTorque_Nm             : REAL := -450.0;
    c_rMaxRegenPower_kW             : REAL := 95.0;
    c_rMinRegenPower_kW             : REAL := 0.0;

    (* ===================================================================================== *)
    (* 5.0 JERK-LIMITED 7-PHASE S-CURVE MOTION PROFILER REGISTERS                            *)
    (* Profile generates continuous position, speed, and acceleration trajectories            *)
    (* ===================================================================================== *)
    iSCurvePhase                    : INT := 0;         (* 0=Rest, 1=Jerk+, 2=AccConst, 3=Jerk-, 4=Cruise, 5=JerkDec+, 6=DecConst, 7=Creep *)
    rSCurveTargetDistance_mm        : REAL := 0.0;      (* Total Distance to Target Floor/Column [mm] *)
    rSCurveStartPos_mm              : REAL := 0.0;      (* Initial Trajectory Starting Position [mm] *)
    rSCurveTraveledDist_mm          : REAL := 0.0;      (* Profile Elapsed Distance [mm] *)
    rSCurveElapsedTimer_s           : REAL := 0.0;      (* Current S-Curve Phase Elapsed Timer [s] *)
    rProfileCurrentPos_mm           : REAL := 0.0;      (* Instantaneous Generated Position Setpoint [mm] *)
    rProfileCurrentVel_m_s          : REAL := 0.0;      (* Instantaneous Generated Velocity Setpoint [m/s] *)
    rProfileCurrentAccel_m_s2       : REAL := 0.0;      (* Instantaneous Generated Acceleration Setpoint [m/s^2] *)
    bSCurveProfileActive            : BOOL := FALSE;    (* S-Curve Motion Execution in Progress *)
    bSCurveProfileCompleted         : BOOL := FALSE;    (* Target Position Reached & Quiescent *)
    rSubMillimeterCreepTimer_s      : REAL := 0.0;      (* Dwell Timer inside Sub-Millimeter Floor Window [s] *)

    (* Shuttle S-Curve Dedicated Profile Registers *)
    iShuttleSCurvePhase             : INT := 0;
    rShuttleTargetDist_mm           : REAL := 0.0;
    rShuttleStartPos_mm             : REAL := 1800.0;
    rShuttleProfilePos_mm           : REAL := 1800.0;
    rShuttleProfileVel_m_s          : REAL := 0.0;
    bShuttleProfileActive           : BOOL := FALSE;
    bShuttleProfileCompleted        : BOOL := FALSE;

    (* ===================================================================================== *)
    (* 6.0 2ND-ORDER VELOCITY & ACCELERATION BACKWARD DIFFERENCE DERIVATIVE REGISTERS       *)
    (* 5-Point Ring Buffer for High-Noise Filtering and Accurate Numerical Differentiation   *)
    (* ===================================================================================== *)
    rPosBuffer_k1                   : REAL := 0.0;      (* Position at Scan k-1 [mm] *)
    rPosBuffer_k2                   : REAL := 0.0;      (* Position at Scan k-2 [mm] *)
    rPosBuffer_k3                   : REAL := 0.0;      (* Position at Scan k-3 [mm] *)
    rPosBuffer_k4                   : REAL := 0.0;      (* Position at Scan k-4 [mm] *)
    rRawVelocity_m_s                : REAL := 0.0;      (* Numerical Backward Difference Velocity [m/s] *)
    rFilteredVelocity_m_s           : REAL := 0.0;      (* Low-Pass Filtered Velocity [m/s] *)
    rRawAccel_m_s2                  : REAL := 0.0;      (* Numerical Backward Difference Acceleration [m/s^2] *)
    rFilteredAccel_m_s2             : REAL := 0.0;      (* Low-Pass Filtered Acceleration [m/s^2] *)
    c_rVelFilterAlpha               : REAL := 0.25;     (* 1st-Order Low-Pass Filter Constant *)

    (* ===================================================================================== *)
    (* 7.0 CABLE ELASTICITY VIBRATION OBSERVER & DIGITAL NOTCH FILTER                        *)
    (* Identifies longitudinal spring stretch modes and computes active canceling torque     *)
    (* ===================================================================================== *)
    rFreeCableLength_m              : REAL := 10.0;     (* Suspended Wire Rope Length to Carriage [m] *)
    rDynamicCableStiffness_N_m      : REAL := 145000.0; (* Load-Dependent Cable Spring Constant [N/m] *)
    rCableNaturalFreq_rad_s         : REAL := 18.5;     (* Calculated Longitudinal Resonance Frequency [rad/s] *)
    rObservedStretch_mm             : REAL := 0.0;      (* Dynamic Stretch Deviation from Equilibrium [mm] *)
    rObservedStretchVelocity_mm_s   : REAL := 0.0;      (* Dynamic Stretch Rate of Change [mm/s] *)
    rPriorObservedStretch_mm        : REAL := 0.0;
    rActiveDampingGain_Kp           : REAL := 18.5;     (* Active Damping Proportional Gain [Nm/mm] *)
    rActiveDampingGain_Kd           : REAL := 2.4;      (* Active Damping Derivative Gain [Nm/(mm/s)] *)

    (* ===================================================================================== *)
    (* 8.0 DYNAMIC THERMAL REPLICA SIMULATORS (IEC 60034 PMSM & MECHANICAL BRAKE)           *)
    (* Continuous accumulation of I^2*t ohmic losses and mechanical kinetic friction heating *)
    (* ===================================================================================== *)
    rSimStatorTemp_degC             : REAL := 45.0;     (* Hoist Motor Stator Copper Winding Replica [deg C] *)
    rSimBrakeTemp_degC              : REAL := 38.0;     (* Mechanical Disc Brake Caliper Surface Replica [deg C] *)
    c_rMotorThermalTimeConst_s      : REAL := 480.0;    (* Stator Winding Thermal Equilibrium Time Constant [s] *)
    c_rMotorRatedCurrent_A          : REAL := 140.0;    (* PMSM Rated Phase RMS Current [A] *)
    c_rMotorRatedRise_degC          : REAL := 65.0;     (* Full-Load Continuous Stator Temperature Rise [deg C] *)
    c_rBrakeCoolingTimeConst_s      : REAL := 720.0;    (* Disc Brake Natural Convective Cooling Time Constant [s] *)
    c_rBrakeFrictionCoeff           : REAL := 0.38;     (* Sintered Bronze Brake Pad Friction Factor *)

    (* ===================================================================================== *)
    (* 9.0 REGENERATIVE BRAKING & DC BUS VOLTAGE REGULATION REGISTERS                        *)
    (* Tracks kinetic and potential energy recovery during descending payload or CW rise     *)
    (* ===================================================================================== *)
    rNetMechanicalPower_kW          : REAL := 0.0;      (* Instantaneous Shaft Mechanical Power P = T * omega [kW] *)
    rCalculatedRegenPower_kW        : REAL := 0.0;      (* Electrical Power Returned to DC Link [kW] *)
    rTotalRegenEnergy_kWh           : REAL := 0.0;      (* Cumulative Regenerated Energy Recovered [kWh] *)
    rChopperDutyCycle_Pct           : REAL := 0.0;      (* Dynamic Braking Chopper Pulse-Width Modulated Duty [%] *)

    (* ===================================================================================== *)
    (* 10.0 SIL-3 MULTI-STAGE FINITE STATE MACHINE (FSM) ARCHITECTURE                        *)
    (* Complete 11-stage lifecycle from Cold Boot to Normal Storage, Retrieval & Clamp Drop  *)
    (* ===================================================================================== *)
    iState                          : INT := 0;         (* Active Sequence State of APS Master Finite State Machine *)
    iPrevState                      : INT := 0;         (* Memory of Previous Operating State for Transition Detection *)
    rStateDwellTimer_s              : REAL := 0.0;      (* Elapsed Dwell Time in Current State [s] *)
    rDoorActionTimer_s              : REAL := 0.0;      (* Shutter Door Opening/Closing Timeout Monitor [s] *)
    rPalletClampTimer_s             : REAL := 0.0;      (* Pallet Centering Clamping Solenoid Action Timer [s] *)
    rCombArmCycleTimer_s            : REAL := 0.0;      (* Telescopic Vehicle Transfer Comb Arms Motion Timer [s] *)
    iMissionType                    : INT := 0;         (* 0=None, 1=Store Vehicle, 2=Retrieve Vehicle *)
    iAssignedStorageLevel           : INT := 1;         (* Latched Target Storage Level Index *)
    iAssignedStorageBay             : INT := 1;         (* Latched Target Storage Bay Column Index *)
    bPalletOccupiedWithVehicle      : BOOL := FALSE;    (* Flag Indicating Carriage Pallet Currently Holds Vehicle *)

    (* ===================================================================================== *)
    (* 11.0 ISA-18.2 MULTI-TIERED ALARM THRESHOLDS & HYSTERESIS REGISTERS                    *)
    (* Standardized High-High (HH), High (H), Low (L), Low-Low (LL) Hierarchy with Deadbands *)
    (* ===================================================================================== *)
    c_rSpeed_HH_m_s                 : REAL := 4.025;    (* 115% Hoist Overspeed Trip Threshold (Safety Clamp Drop) [m/s] *)
    c_rSpeed_H_m_s                  : REAL := 3.650;    (* High Hoist Velocity Advisory Warning [m/s] *)
    c_rSpeed_Deadband_m_s           : REAL := 0.050;

    c_rCableTension_LL_kN           : REAL := 8.0;      (* Slack Rope Critical Safety Trip (Loss of Cable Tension) [kN] *)
    c_rCableTension_L_kN            : REAL := 12.0;     (* Low Cable Tension Warning [kN] *)
    c_rCableTension_HH_kN           : REAL := 95.0;     (* Over-Tension Structural Limit Trip [kN] *)
    c_rCableTension_Deadband_kN     : REAL := 1.5;

    c_rCableOsc_HH_mm               : REAL := 35.0;     (* Severe Longitudinal Cable Elastic Oscillation Trip [mm] *)
    c_rCableOsc_H_mm                : REAL := 18.0;     (* Elevated Cable Vibration Warning [mm] *)
    c_rCableOsc_Deadband_mm         : REAL := 2.5;

    c_rLevelAlign_HH_mm             : REAL := 4.5;      (* Severe Floor Misalignment Trip (Docking Pin Blocked) [mm] *)
    c_rLevelAlign_H_mm              : REAL := 1.5;      (* Floor Misalignment Creep Warning [mm] *)
    c_rLevelAlign_Deadband_mm       : REAL := 0.25;

    c_rDCLink_HH_V                  : REAL := 820.0;    (* Critical DC Bus Overpotential Trip [V] *)
    c_rDCLink_H_V                   : REAL := 750.0;    (* High DC Link Dynamic Braking Chopper Engage Threshold [V] *)
    c_rDCLink_L_V                   : REAL := 580.0;    (* Low DC Link Warning Threshold [V] *)
    c_rDCLink_LL_V                  : REAL := 520.0;    (* Severe DC Link Undervoltage Trip [V] *)
    c_rDCLink_Deadband_V            : REAL := 10.0;

    c_rStatorTemp_HH_degC           : REAL := 135.0;    (* Hoist PMSM Winding Insulation Class H Critical Trip [deg C] *)
    c_rStatorTemp_H_degC            : REAL := 115.0;    (* Stator Winding High Temperature Warning [deg C] *)
    c_rBrakeDiscTemp_HH_degC        : REAL := 180.0;    (* Mechanical Safety Brake Disc Thermal Fade Limit [deg C] *)
    c_rBrakeDiscTemp_H_degC         : REAL := 120.0;    (* Mechanical Brake High Temperature Warning [deg C] *)
    c_rTemp_Deadband_degC           : REAL := 3.0;

    c_rClampPressure_LL_bar         : REAL := 125.0;    (* Hydraulic Safety Wedge Clamp Low Pressure Trip [bar] *)
    c_rClampPressure_L_bar          : REAL := 140.0;    (* Hydraulic Safety Wedge Clamp Low Pressure Warning [bar] *)
    c_rClampPressure_Deadband_bar   : REAL := 4.0;

    c_rWeight_HH_kg                 : REAL := 2800.0;   (* Cabin Maximum Permissible Gross Vehicle Mass Trip [kg] *)
    c_rWeight_Deadband_kg           : REAL := 25.0;

    (* Latched Alarm Status Bits *)
    bAlarm_Speed_HH                 : BOOL := FALSE;
    bAlarm_Speed_H                  : BOOL := FALSE;
    bAlarm_CableTension_LL          : BOOL := FALSE;
    bAlarm_CableTension_L           : BOOL := FALSE;
    bAlarm_CableTension_HH          : BOOL := FALSE;
    bAlarm_CableOsc_HH              : BOOL := FALSE;
    bAlarm_CableOsc_H               : BOOL := FALSE;
    bAlarm_LevelAlign_HH            : BOOL := FALSE;
    bAlarm_LevelAlign_H             : BOOL := FALSE;
    bAlarm_DCLink_HH                : BOOL := FALSE;
    bAlarm_DCLink_H                 : BOOL := FALSE;
    bAlarm_DCLink_L                 : BOOL := FALSE;
    bAlarm_DCLink_LL                : BOOL := FALSE;
    bAlarm_StatorTemp_HH            : BOOL := FALSE;
    bAlarm_StatorTemp_H             : BOOL := FALSE;
    bAlarm_BrakeDiscTemp_HH         : BOOL := FALSE;
    bAlarm_BrakeDiscTemp_H          : BOOL := FALSE;
    bAlarm_ClampPressure_LL         : BOOL := FALSE;
    bAlarm_ClampPressure_L          : BOOL := FALSE;
    bAlarm_Weight_HH                : BOOL := FALSE;
    bAlarm_VehicleLength_HH         : BOOL := FALSE;
    bAlarm_VehicleWidth_HH          : BOOL := FALSE;
    bAlarm_VehicleHeight_HH         : BOOL := FALSE;
    bAlarm_OverhangObstruction      : BOOL := FALSE;
    bAlarm_EStopTripped             : BOOL := FALSE;
    bAlarm_CabinCurtainBreach       : BOOL := FALSE;
    bAlarm_LaserSpread_Trip         : BOOL := FALSE;
    bAlarm_EncoderSpread_Trip       : BOOL := FALSE;
    bAlarm_ShuttleSpread_Trip       : BOOL := FALSE;
    bAlarm_LoadCellSpread_Trip      : BOOL := FALSE;
    bAlarm_TractionRopeSlip         : BOOL := FALSE;
    bAlarm_EmergencyClampDropped    : BOOL := FALSE;

    (* Scratch Loop Counters & Temporary Math Registers *)
    iScratchIndex                   : INT := 0;
    rScratch1                       : REAL := 0.0;
    rScratch2                       : REAL := 0.0;
    rScratch3                       : REAL := 0.0;
    rScratch4                       : REAL := 0.0;
END_VAR
"""
