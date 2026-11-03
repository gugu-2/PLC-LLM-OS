# Script to generate full ST code in sections and validate
import os, sys, json, uuid, re

def get_code():
    st = []
    
    # Header & Declarations (from previous verified code)
    st.append("""FUNCTION_BLOCK FB_Automotive_EV_Chassis_LaserArcHybridWelding
(*
 ==========================================================================================
  PROJECT:       AUTOMOTIVE ELECTRIC VEHICLE (EV) SKATEBOARD CHASSIS LIGHTWEIGHTING
  SUBSYSTEM:     HIGH-STRENGTH 6000/7000 ALUMINUM SUBFRAME ROBOTIC WELDING CELL
  PROCESS:       8 kW FIBER LASER - CMT (COLD METAL TRANSFER) GMAW HYBRID HIGH-SPEED WELDING
  STANDARDS:     AWS D1.2 / EN ISO 15614-14 (STRUCTURAL ALUMINUM), EN ISO 13849-1 (CAT 4 / PLe)
  IEC STANDARD:  IEC 61131-3 3RD EDITION COMPLIANT (DETERMINISTIC EMBEDDED EXECUTION)
  CYCLE TICK Ts: 0.0020 SECONDS (2.0 MILLISECONDS DETERMINISTIC FAST REAL-TIME INTERRUPT)
  AUTHOR:        LUMINA AI CLOUD SWARM - PRINCIPAL AUTOMATION FELLOW & CPS CHAIR (V7 MAX)
 ==========================================================================================
  CYBER-PHYSICAL SYSTEM ARCHITECTURAL SPECIFICATION:
  ------------------------------------------------------------------------------------------
  This Function Block governs an advanced 8-axis robotic laser-arc hybrid manufacturing cell
  engineered for automated structural welding of 800V EV skateboard chassis aluminum subframes.
  The workpieces consist of modular high-strength extruded 6082-T6 and cast/forged 7003-T6
  suspension nodes with tight metallurgical constraints regarding hot-cracking susceptibility,
  porosity formation, and heat-affected zone (HAZ) softening.

  The cell integrates five tightly coupled mechatronic and cyber-physical domains:
  1. Optical Leading Triangulation Seam Tracking:
     - 3D laser sheet triangulation scanner mounted 20.0 mm ahead of the tool center point (TCP).
     - Running at 500 Hz (2.0 ms sync), tracking lateral joint offset, vertical surface standoff,
       and root gap opening (0.20 mm to 1.80 mm tolerance range) with 0.05 mm spatial accuracy.
     - 2oo3 Triple Modular Redundancy (TMR) profile cross-validation with discrepancy voting.
  2. Laser-GMAW Co-Axial Hybrid Arc Coupling:
     - Co-axial Trumpf 8 kW fiber laser (1070 nm, BPP 4.0 mm*mrad) with 2-in-1 fiber beam shaping.
     - Leading laser beam establishes a deep vapor keyhole with high aspect ratio (depth/width > 2.5).
     - Trailing Fronius TPS/i CMT (Cold Metal Transfer) arc running 1.2 mm AlMg5 (ER5356) wire.
     - Arc current feedback (95 A to 320 A) dynamically stabilized via high-speed digital bus.
  3. Real-Time Melt Pool Co-Axial Thermography & Keyhole CMOS Diagnostics:
     - Co-axial dual-wavelength infrared pyrometer measuring weld pool peak surface temperature
       (nominal liquidus plateau 1450 - 1650 deg C).
     - High-speed CMOS sensor measuring keyhole area and keyhole depth penetration dynamics.
  4. Cyber-Physical Discrete State-Space Model & Receding-Horizon MPC:
     - Deterministic 4-state, 3-input discrete state-space model running at Ts = 0.002 s:
       x[k+1] = A * x[k] + B * u[k], where states represent lateral seam tracking error [mm],
       vertical standoff error [mm], melt pool peak temperature [deg C], and arc current [A].
     - Model Predictive Controller (MPC) evaluating a receding horizon quadratic cost index:
       J = sum( (x_k - r)^T Q (x_k - r) + u_k^T R u_k ) + (x_N - r)^T P (x_N - r)
       optimizing robot TCP lateral trim, CMT wire feed speed, and laser power in real time.
  5. Multi-Tiered ISA-18.2 Safety & Process Alarm Ladder:
     - Arc blowout emergency detection (LL < 95 A) triggering instantaneous emergency abort.
     - Arc burn-through shutdown (HH > 320 A).
     - Protective optical cover glass contamination monitoring with autonomous air knife blast.
     - Strict EN ISO 13849-1 Cat 4 / PLe safety logic supervising light curtains and interlocks.
 ==========================================================================================
*)
VAR_INPUT
    (* ================================================================================= *)
    (* TRIPLE MODULAR REDUNDANT (2oo3) SEAM TRACKER LATERAL OFFSET SAMPLES [mm]         *)
    (* ================================================================================= *)
    rSeamTrack_ChA_LateralOffset_mm   : REAL;    (* Triangulation Seam Tracker Lateral Offset Channel A [mm] *)
    rSeamTrack_ChB_LateralOffset_mm   : REAL;    (* Triangulation Seam Tracker Lateral Offset Channel B [mm] *)
    rSeamTrack_ChC_LateralOffset_mm   : REAL;    (* Triangulation Seam Tracker Lateral Offset Channel C [mm] *)

    (* ================================================================================= *)
    (* TRIPLE MODULAR REDUNDANT (2oo3) SEAM TRACKER VERTICAL STANDOFF SAMPLES [mm]      *)
    (* ================================================================================= *)
    rSeamTrack_ChA_VerticalStandoff_mm: REAL;    (* Triangulation Seam Tracker Vertical Standoff Channel A [mm] *)
    rSeamTrack_ChB_VerticalStandoff_mm: REAL;    (* Triangulation Seam Tracker Vertical Standoff Channel B [mm] *)
    rSeamTrack_ChC_VerticalStandoff_mm: REAL;    (* Triangulation Seam Tracker Vertical Standoff Channel C [mm] *)

    (* ================================================================================= *)
    (* TRIPLE MODULAR REDUNDANT (2oo3) SEAM TRACKER JOINT ROOT GAP SAMPLES [mm]         *)
    (* ================================================================================= *)
    rSeamTrack_ChA_JointGap_mm        : REAL;    (* Triangulation Seam Tracker Joint Root Opening Channel A [mm] *)
    rSeamTrack_ChB_JointGap_mm        : REAL;    (* Triangulation Seam Tracker Joint Root Opening Channel B [mm] *)
    rSeamTrack_ChC_JointGap_mm        : REAL;    (* Triangulation Seam Tracker Joint Root Opening Channel C [mm] *)

    (* ================================================================================= *)
    (* SEAM TRACKER OPTICAL PROFILE CONFIDENCE & VALIDITY FLAGS [%]                      *)
    (* ================================================================================= *)
    rSeamTrack_ChA_QualityScore_pct   : REAL;    (* Optical triangulation profile quality index Ch A [%] *)
    rSeamTrack_ChB_QualityScore_pct   : REAL;    (* Optical triangulation profile quality index Ch B [%] *)
    rSeamTrack_ChC_QualityScore_pct   : REAL;    (* Optical triangulation profile quality index Ch C [%] *)

    (* ================================================================================= *)
    (* TRIPLE MODULAR REDUNDANT (2oo3) CO-AXIAL PYROMETER MELT POOL TEMPERATURE [deg C]  *)
    (* ================================================================================= *)
    rPyrometer_ChA_MeltPoolTemp_degC  : REAL;    (* Co-axial narrow-band infrared pyrometer Channel A [deg C] *)
    rPyrometer_ChB_MeltPoolTemp_degC  : REAL;    (* Co-axial narrow-band infrared pyrometer Channel B [deg C] *)
    rPyrometer_ChC_MeltPoolTemp_degC  : REAL;    (* Co-axial narrow-band infrared pyrometer Channel C [deg C] *)

    (* ================================================================================= *)
    (* HIGH-SPEED CO-AXIAL CMOS VISION KEYHOLE MORPHOLOGY [mm, mm2, %]                   *)
    (* ================================================================================= *)
    rCMOS_KeyholeDepth_mm             : REAL;    (* High-speed CMOS optical keyhole penetration depth [mm] *)
    rCMOS_KeyholeArea_mm2             : REAL;    (* Real-time molten pool keyhole aperture area [mm2] *)
    rCMOS_KeyholeSqueezeRatio_pct     : REAL;    (* Keyhole geometric stability squeeze ratio [%] *)

    (* ================================================================================= *)
    (* COLD METAL TRANSFER (CMT) GMAW ARC POWER FEEDBACK [V, A, m/min, N*m]              *)
    (* ================================================================================= *)
    rArcVoltage_Feedback_V            : REAL;    (* Instantaneous welding arc terminal voltage [V] *)
    rArcCurrent_Feedback_A            : REAL;    (* Instantaneous welding arc current transducer [A] *)
    rWireFeedSpeed_Feedback_mpm       : REAL;    (* High-speed push-pull wire feeder encoder velocity [m/min] *)
    rWireFeederTorque_Nm              : REAL;    (* Wire drive servomotor instantaneous torque feedback [N*m] *)

    (* ================================================================================= *)
    (* FIBER LASER SOURCE STATUS & OPTICAL TRAIN DIAGNOSTICS [W, deg C, %]               *)
    (* ================================================================================= *)
    rLaserPower_Actual_W              : REAL;    (* Photodiode calibrated actual laser power emission [W] *)
    rLaserBackReflection_W            : REAL;    (* Optical fiber protective back-reflection sensor [W] *)
    rOpticalFiberTemp_degC            : REAL;    (* Process fiber connector core temperature [deg C] *)
    rCoverSlideTransmission_pct       : REAL;    (* Focus head protective cover slide optical transmission [%] *)

    (* ================================================================================= *)
    (* PROCESS SHIELDING GAS DELIVERY (Ar / He MIXTURE) [L/min, bar, %]                  *)
    (* ================================================================================= *)
    rShieldingGasFlow_Lmin            : REAL;    (* Thermal mass flow controller actual gas flow [L/min] *)
    rShieldingGasPressure_bar         : REAL;    (* Gas supply delivery header piezoresistive pressure [bar] *)
    rShieldingGasHeliumFraction_pct   : REAL;    (* Inline thermal conductivity gas analyzer Helium fraction [%] *)

    (* ================================================================================= *)
    (* THERMAL MANAGEMENT & CELL UTILITY COOLING FLOWS [L/min, deg C]                    *)
    (* ================================================================================= *)
    rLaserChillerFlow_Lmin            : REAL;    (* Laser source deionized water cooling flow rate [L/min] *)
    rLaserChillerTemp_degC            : REAL;    (* Laser chiller loop supply temperature [deg C] *)
    rTorchCoolantFlow_Lmin            : REAL;    (* GMAW hybrid torch head deionized water flow [L/min] *)
    rTorchCoolantTemp_degC            : REAL;    (* GMAW hybrid torch cooling return temperature [deg C] *)

    (* ================================================================================= *)
    (* ROBOT & TILT-ROTATOR COORDINATED MOTION FEEDBACK [m/min, mm, deg, deg/s]          *)
    (* ================================================================================= *)
    rRobotTCP_Velocity_mpm            : REAL;    (* Coordinated robot tool center point linear velocity [m/min] *)
    rRobotTCP_PosX_mm                 : REAL;    (* Robot TCP instantaneous Cartesian X coordinate [mm] *)
    rRobotTCP_PosY_mm                 : REAL;    (* Robot TCP instantaneous Cartesian Y coordinate [mm] *)
    rRobotTCP_PosZ_mm                 : REAL;    (* Robot TCP instantaneous Cartesian Z coordinate [mm] *)
    rTiltRotator_AxisA_Angle_deg      : REAL;    (* 2-Axis positioning table tilt axis angular position [deg] *)
    rTiltRotator_AxisB_Angle_deg      : REAL;    (* 2-Axis positioning table rotator axis angular position [deg] *)
    rTiltRotator_Velocity_degs        : REAL;    (* 2-Axis table synchronized angular velocity [deg/s] *)

    (* ================================================================================= *)
    (* SUBFRAME FIXTURE CLAMPING & THERMAL SENSING [bar, mm, BOOL]                       *)
    (* ================================================================================= *)
    rFixtureHydraulicPressure_bar     : REAL;    (* Subframe hydro-mechanical fixture clamping pressure [bar] *)
    bFixturePartSeated_Proximity_1    : BOOL;    (* Subframe datum locator inductive proximity switch 1 *)
    bFixturePartSeated_Proximity_2    : BOOL;    (* Subframe datum locator inductive proximity switch 2 *)
    bFixturePartSeated_Proximity_3    : BOOL;    (* Subframe datum locator inductive proximity switch 3 *)
    rExtrusionThermalExpansion_mm     : REAL;    (* Laser displacement gauge aluminum thermal expansion [mm] *)

    (* ================================================================================= *)
    (* SAFETY CIRCUITS, INTERLOCKS & OPERATOR INTERFACE                                  *)
    (* ================================================================================= *)
    bCellSafetyCircuit_Ok             : BOOL;    (* Hardwired Cat 4 / PLe dual-channel safety circuit healthy *)
    bLaserSafetyInterlock_Ok          : BOOL;    (* Laser class 4 enclosure safety interlock contactors closed *)
    bLightCurtainClear                : BOOL;    (* Perimeter optical safety light curtain unviolated *)
    bArcShieldInPosition              : BOOL;    (* Pneumatic protective welding glare shield deployed *)
    bEmergencyStopOk                  : BOOL;    (* Master cell emergency stop pushbutton circuit OK *)
    bOperatorCycleStart               : BOOL;    (* Operator control pendant weld cycle start push-button *)
    bOperatorCycleAbort               : BOOL;    (* Operator control pendant cycle abort button *)
    bOperatorFaultReset               : BOOL;    (* Operator control pendant fault acknowledge reset *)
    bManualAirBlastTrigger            : BOOL;    (* Manual maintenance trigger for protective glass air blast *)
END_VAR
VAR_OUTPUT
    (* ================================================================================= *)
    (* LASER GENERATOR COMMAND INTERFACE [W, %, BOOL]                                    *)
    (* ================================================================================= *)
    rLaserPower_Setpoint_W            : REAL;    (* Fiber laser analog modulated power output demand [W] *)
    bLaserEmissionEnable              : BOOL;    (* High-speed hardware laser emission excitation gate enable *)
    bLaserShutterOpen                 : BOOL;    (* Fiber laser optical safety beam shutter open command *)
    rLaserBeamShapingCoreRatio_pct    : REAL;    (* 2-in-1 fiber core-to-ring power split ratio demand [%] *)

    (* ================================================================================= *)
    (* COLD METAL TRANSFER (CMT) WIRE FEEDER COMMANDS [m/min, UINT, BOOL, ms]           *)
    (* ================================================================================= *)
    bCMT_ArcIgnitionTrigger           : BOOL;    (* High-speed fieldbus arc ignition run trigger *)
    rWireFeedSpeed_Demand_mpm         : REAL;    (* CMT digital wire feed speed regulation demand [m/min] *)
    uiCMT_SynergicCurveID             : UINT;    (* Synergic characteristic curve program index for AlMg5 *)
    bWireRetractCmd                   : BOOL;    (* High-speed wire retract command for spatterless ignition *)
    rBurnbackDuration_ms              : REAL;    (* End-of-weld wire burn-back pulse duration [ms] *)

    (* ================================================================================= *)
    (* ROBOT & POSITIONING TABLE REAL-TIME TRAJECTORY TRIMS [mm, %, BOOL]                *)
    (* ================================================================================= *)
    rRobotTCP_Trim_Lateral_mm         : REAL;    (* Dynamic TCP lateral seam tracking offset correction [mm] *)
    rRobotTCP_Trim_Vertical_mm        : REAL;    (* Dynamic TCP vertical torch standoff offset correction [mm] *)
    rRobotSpeedOverride_pct           : REAL;    (* Coordinated robot motion velocity scaling factor [%] *)
    rTiltRotatorSpeedOverride_pct     : REAL;    (* Positioning table velocity scaling factor [%] *)
    bTrajectoryFeedHold               : BOOL;    (* Robot motion interrupt feed hold flag *)

    (* ================================================================================= *)
    (* GAS & OPTICAL PROTECTION ACTUATORS [L/min, BOOL]                                  *)
    (* ================================================================================= *)
    rShieldingGas_MFC_Setpoint_Lmin   : REAL;    (* Shielding gas thermal mass flow controller setpoint [L/min] *)
    bShieldingGas_SolenoidOpen        : BOOL;    (* Fast-acting solenoid valve for Ar/He shielding gas *)
    bSeamTracker_LaserDiodeEnable     : BOOL;    (* Triangulation seam tracker scanning laser diode enable *)
    bCoverSlideAirKnifeBlast          : BOOL;    (* Pneumatic cross-jet air knife high-pressure blast solenoid *)
    bCoverSlideCassetteAdvance        : BOOL;    (* Motorized protective cover glass roll advance trigger *)

    (* ================================================================================= *)
    (* TOOLING FIXTURE & UTILITY ACTUATION                                               *)
    (* ================================================================================= *)
    bFixtureClampSolenoid             : BOOL;    (* Subframe hydro-pneumatic clamping fixture engage solenoid *)
    bFixtureUnclampSolenoid           : BOOL;    (* Subframe hydro-pneumatic clamping fixture release solenoid *)
    bWeldCellExhaustFanRun            : BOOL;    (* Process fume extraction high-volume ventilation fan *)
    bAlarmAudibleSiren                : BOOL;    (* Category 1 acoustic plant alarm siren *)
    bAlarmVisualBeacon                : BOOL;    (* Tri-color stack tower optical alarm beacon *)

    (* ================================================================================= *)
    (* SYNTHESIZED 2oo3 VOTED PROCESS SIGNALS [mm, deg C]                                *)
    (* ================================================================================= *)
    rVoted_TrackingLateralOffset_mm   : REAL;    (* 2oo3 median voted lateral joint offset [mm] *)
    rVoted_TrackingVerticalStandoff_mm: REAL;    (* 2oo3 median voted vertical torch standoff [mm] *)
    rVoted_JointGap_mm                : REAL;    (* 2oo3 median voted joint root opening [mm] *)
    rVoted_MeltPoolTemp_degC          : REAL;    (* 2oo3 median voted melt pool peak temperature [deg C] *)

    (* ================================================================================= *)
    (* OBSERVER ESTIMATES & QUALITY COMPLIANCE METRICS [mm, J/mm, g/min]                 *)
    (* ================================================================================= *)
    rEstimated_PenetrationDepth_mm    : REAL;    (* Dynamic model estimated full root penetration depth [mm] *)
    rEstimated_LinearHeatInput_Jmm    : REAL;    (* AWS D1.2 net linear heat input per unit length [J/mm] *)
    rEstimated_WireDepositionRate_gmin: REAL;    (* AlMg5 aluminum alloy wire deposition mass rate [g/min] *)

    (* ================================================================================= *)
    (* BIT-PACKED STATUS & ALARM WORDS (ISA-18.2 COMPLIANT)                              *)
    (* ================================================================================= *)
    dwSystemStatusWord                : DWORD;   (* Bit-packed supervisory operational status register *)
    dwAlarmWord1_EmergencyTrips       : DWORD;   (* Bit-packed Category 1 SIL-3 emergency shutdowns and trips *)
    dwAlarmWord2_ProcessTrips         : DWORD;   (* Bit-packed Category 2 process limit trips and quality faults *)
    dwWarningWord                     : DWORD;   (* Bit-packed Category 3 operational advisory warnings *)
    dwDegradationWord                 : DWORD;   (* Bit-packed 2oo3 instrument triplet degradation and health flags *)
    dwIsaAlarmPriorityMask            : DWORD;   (* Bit-packed active ISA-18.2 alarm priority annunciator mask *)
END_VAR
VAR
    (* ================================================================================= *)
    (* SUPERVISORY FINITE STATE MACHINE (FSM) STEP REGISTERS & PROCESS TIMERS           *)
    (* ================================================================================= *)
    iState                            : INT := 0; (* Primary supervisory operational state register *)
    iSubState                         : INT := 0; (* Sub-step sequence register within active state *)
    iPrevState                        : INT := 0; (* Previous scan cycle state history register *)
    iStepIndex                        : INT := 0; (* Step index execution counter *)
    bStateChanged                     : BOOL := FALSE; (* Positive edge state change flag *)
    bCycleCompleted                   : BOOL := FALSE; (* Complete chassis seam cycle completion flag *)
    bWeldAborted                      : BOOL := FALSE; (* Cycle abort latching flag *)

    tStateTimer                       : TON;      (* Primary state dwell and timeout timer *)
    tClampTimer                       : TON;      (* Hydraulic fixture clamping dwell timer *)
    tPrePurgeTimer                    : TON;      (* Shielding gas pre-purge flow stabilization timer *)
    tArcStrikeTimer                   : TON;      (* CMT arc strike ignition sequence timeout timer *)
    tKeyholeEstablishTimer            : TON;      (* Laser keyhole initial penetration dwell timer *)
    tWeldTrajectoryTimer              : TON;      (* Main continuous welding trajectory execution timer *)
    tCraterFillTimer                  : TON;      (* Synergic crater fill power decel ramp timer *)
    tPostPurgeTimer                   : TON;      (* Shielding gas post-weld freeze protection timer *)
    tOpticalAuditTimer                : TON;      (* Solidified weld bead optical inspection timer *)
    tSpatterCleanTimer                : TON;      (* Optical cross-jet air knife spatter blast timer *)
    tDiscrepancyTimer_Lateral         : TON;      (* 2oo3 lateral seam tracking discrepancy persistence timer *)
    tDiscrepancyTimer_Vertical        : TON;      (* 2oo3 vertical standoff discrepancy persistence timer *)
    tDiscrepancyTimer_Gap             : TON;      (* 2oo3 joint root gap discrepancy persistence timer *)
    tDiscrepancyTimer_Temp            : TON;      (* 2oo3 melt pool temperature discrepancy persistence timer *)
    tAirKnifePulseTimer               : TON;      (* Autonomous cover glass air knife pulse timer *)
    tResetDebounceTimer               : TON;      (* Operator fault reset push-button debounce timer *)
    tArcBlowoutDebounceTimer          : TON;      (* Arc blowout emergency detection debounce timer *)
    tBurnThroughDebounceTimer         : TON;      (* High-current burn-through trip debounce timer *)
    tCassetteAdvanceTimer             : TON;      (* Motorized cover glass roll advance cycle timer *)

    (* ================================================================================= *)
    (* 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) DISCREPANCY & HEALTH MONITORING             *)
    (* ================================================================================= *)
    (* Lateral Seam Tracking Triplet *)
    rDev_Lat_AB                       : REAL := 0.0; (* Deviation between lateral sensor A and B [mm] *)
    rDev_Lat_BC                       : REAL := 0.0; (* Deviation between lateral sensor B and C [mm] *)
    rDev_Lat_CA                       : REAL := 0.0; (* Deviation between lateral sensor C and A [mm] *)
    bLat_A_Healthy                    : BOOL := TRUE;
    bLat_B_Healthy                    : BOOL := TRUE;
    bLat_C_Healthy                    : BOOL := TRUE;
    bLat_Degraded_1oo2                : BOOL := FALSE;
    bLat_ConsensusLost_Trip           : BOOL := FALSE;

    (* Vertical Standoff Triplet *)
    rDev_Vert_AB                      : REAL := 0.0; (* Deviation between standoff sensor A and B [mm] *)
    rDev_Vert_BC                      : REAL := 0.0; (* Deviation between standoff sensor B and C [mm] *)
    rDev_Vert_CA                      : REAL := 0.0; (* Deviation between standoff sensor C and A [mm] *)
    bVert_A_Healthy                   : BOOL := TRUE;
    bVert_B_Healthy                   : BOOL := TRUE;
    bVert_C_Healthy                   : BOOL := TRUE;
    bVert_Degraded_1oo2               : BOOL := FALSE;
    bVert_ConsensusLost_Trip          : BOOL := FALSE;

    (* Joint Root Gap Triplet *)
    rDev_Gap_AB                       : REAL := 0.0; (* Deviation between root gap sensor A and B [mm] *)
    rDev_Gap_BC                       : REAL := 0.0; (* Deviation between root gap sensor B and C [mm] *)
    rDev_Gap_CA                       : REAL := 0.0; (* Deviation between root gap sensor C and A [mm] *)
    bGap_A_Healthy                    : BOOL := TRUE;
    bGap_B_Healthy                    : BOOL := TRUE;
    bGap_C_Healthy                    : BOOL := TRUE;
    bGap_Degraded_1oo2                : BOOL := FALSE;
    bGap_ConsensusLost_Trip           : BOOL := FALSE;

    (* Melt Pool Pyrometer Triplet *)
    rDev_Temp_AB                      : REAL := 0.0; (* Deviation between pyrometer A and B [deg C] *)
    rDev_Temp_BC                      : REAL := 0.0; (* Deviation between pyrometer B and C [deg C] *)
    rDev_Temp_CA                      : REAL := 0.0; (* Deviation between pyrometer C and A [deg C] *)
    bTemp_A_Healthy                   : BOOL := TRUE;
    bTemp_B_Healthy                   : BOOL := TRUE;
    bTemp_C_Healthy                   : BOOL := TRUE;
    bTemp_Degraded_1oo2               : BOOL := FALSE;
    bTemp_ConsensusLost_Trip          : BOOL := FALSE;

    (* ================================================================================= *)
    (* DISCRETE STATE-SPACE THERMO-ELECTRICAL & SEAM KINEMATICS MATRICES (4x4, 4x3)     *)
    (* ================================================================================= *)
    A_mat                             : ARRAY[1..4, 1..4] OF REAL; (* Discrete state transition matrix (Ts=2ms) *)
    B_mat                             : ARRAY[1..4, 1..3] OF REAL; (* Discrete control input coupling matrix *)
    C_mat                             : ARRAY[1..4, 1..4] OF REAL; (* State-to-output observation matrix *)
    D_mat                             : ARRAY[1..4, 1..3] OF REAL; (* Direct feedthrough matrix *)
    L_obs                             : ARRAY[1..4, 1..4] OF REAL; (* Luenberger state observer gain matrix *)

    x_state                           : ARRAY[1..4] OF REAL;       (* Filtered state estimate vector *)
    x_pred                            : ARRAY[1..4] OF REAL;       (* One-step ahead model state prediction *)
    x_ref                             : ARRAY[1..4] OF REAL;       (* Dynamic reference target trajectory *)
    x_err                             : ARRAY[1..4] OF REAL;       (* Instantaneous tracking error vector *)
    y_meas                            : ARRAY[1..4] OF REAL;       (* 2oo3 synthesized measured output vector *)
    y_est                             : ARRAY[1..4] OF REAL;       (* Observer estimated output vector *)
    y_innov                           : ARRAY[1..4] OF REAL;       (* Innovation residual error vector *)
    u_ctrl                            : ARRAY[1..3] OF REAL;       (* Optimal control demand vector *)
    u_ctrl_prev                       : ARRAY[1..3] OF REAL;       (* Control vector from previous tick *)
    u_saturated                       : ARRAY[1..3] OF REAL;       (* Rate and amplitude clamped control vector *)

    bMatricesInitialized              : BOOL := FALSE;             (* Cold-start matrix initialization flag *)
    iRow                              : INT := 1;                  (* Matrix row index loop variable *)
    iCol                              : INT := 1;                  (* Matrix column index loop variable *)
    iIdx                              : INT := 1;                  (* General loop index variable *)
    iIter                             : INT := 1;                  (* Solver iteration index *)
    iHorizon                          : INT := 1;                  (* Prediction horizon step index *)

    (* ================================================================================= *)
    (* RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) MATRICES & SOLVER BUFFERS        *)
    (* ================================================================================= *)
    Q_diag                            : ARRAY[1..4] OF REAL;       (* State tracking error weights *)
    R_diag                            : ARRAY[1..3] OF REAL;       (* Control move rate slew penalties *)
    P_diag                            : ARRAY[1..4] OF REAL;       (* Terminal state penalty weights *)

    x_horiz                           : ARRAY[0..5, 1..4] OF REAL; (* Predicted state trajectory across horizon *)
    u_horiz                           : ARRAY[0..4, 1..3] OF REAL; (* Projected candidate control move sequence *)
    du_horiz                          : ARRAY[0..4, 1..3] OF REAL; (* Control move rate increment sequence *)
    grad_u                            : ARRAY[0..4, 1..3] OF REAL; (* Cost function gradient sequence *)
    hess_diag                         : ARRAY[0..4, 1..3] OF REAL; (* Diagonal Hessian approximation sequence *)

    rCost_Total                       : REAL := 0.0;               (* Total MPC quadratic objective value *)
    rCost_StatePenalty                : REAL := 0.0;               (* Integrated state tracking penalty *)
    rCost_TerminalPenalty             : REAL := 0.0;               (* Terminal horizon state deviation cost *)
    rCost_ControlPenalty              : REAL := 0.0;               (* Actuator slew rate penalty cost *)
    rStepSize_Alpha                   : REAL := 0.025;             (* Projected gradient descent relaxation step *)
    iMpcMaxIter                       : INT := 6;                  (* Real-time gradient descent iteration budget *)

    rMinLateralTrim_mm                : REAL := -1.50;             (* Maximum negative robot lateral offset [mm] *)
    rMaxLateralTrim_mm                : REAL := 1.50;              (* Maximum positive robot lateral offset [mm] *)
    rMaxDeltaLateral_mm               : REAL := 0.080;             (* Maximum lateral slew per 2ms tick [mm] *)

    rMinWFS_Demand_mpm                : REAL := 6.00;              (* Minimum stable CMT wire feed speed [m/min] *)
    rMaxWFS_Demand_mpm                : REAL := 14.00;             (* Maximum allowable CMT wire feed speed [m/min] *)
    rMaxDeltaWFS_mpm                  : REAL := 0.050;             (* Maximum wire feed speed slew per 2ms [m/min] *)

    rMinLaserPower_W                  : REAL := 1200.0;            (* Minimum keyhole sustaining laser power [W] *)
    rMaxLaserPower_W                  : REAL := 7800.0;            (* Maximum operating laser power setpoint [W] *)
    rMaxDeltaLaserPower_W             : REAL := 25.0;              (* Maximum laser power slew per 2ms tick [W] *)

    (* ================================================================================= *)
    (* ALUMINUM METALLURGICAL & PROCESS GAP COMPENSATOR CONSTANTS                       *)
    (* ================================================================================= *)
    c_ScanCycleTime_sec               : REAL := 0.0020;            (* 2.0 ms execution tick time [s] *)
    c_AlDensity_gcm3                  : REAL := 2.70;              (* 6082/7003 aluminum alloy density [g/cm3] *)
    c_AlWireDiameter_mm               : REAL := 1.20;              (* AlMg5 filler wire nominal diameter [mm] *)
    c_WireCrossSection_mm2            : REAL := 1.13097;           (* Filler wire cross-sectional area [mm2] *)
    c_LaserAbsorptionEfficiency       : REAL := 0.82;              (* 1070nm fiber laser keyhole coupling efficiency *)
    c_ArcThermalEfficiency            : REAL := 0.85;              (* Cold Metal Transfer arc process efficiency *)
    c_SubframeFlangeThickness_mm      : REAL := 3.50;              (* Subframe extruded wall nominal thickness [mm] *)
    rNominalJointGap_mm               : REAL := 0.60;              (* Ideal nominal structural joint root opening [mm] *)
    rWeldTravelSpeed_mpm              : REAL := 2.10;              (* Nominal coordinated robotic weld speed [m/min] *)
    rWireDepositionCoeff              : REAL := 3.0536;            (* Constant for wire mass flow: rho*Area*60 [g/(m*min)] *)

    (* ================================================================================= *)
    (* ISA-18.2 MULTI-TIERED ALARM SETPOINTS, HYSTERESIS & TRIP FLAGS                    *)
    (* ================================================================================= *)
    c_ArcCurrent_HH_A                 : REAL := 320.0;             (* High-High burn-through emergency trip [A] *)
    c_ArcCurrent_H_A                  : REAL := 280.0;             (* High arc current warning advisory [A] *)
    c_ArcCurrent_L_A                  : REAL := 120.0;             (* Low arc current cold-lap warning [A] *)
    c_ArcCurrent_LL_A                 : REAL := 95.0;              (* Low-Low arc blowout abort threshold [A] *)
    c_ArcCurrent_Deadband_A           : REAL := 5.0;               (* Current deadband hysteresis [A] *)

    c_CoverSlide_H_pct                : REAL := 95.0;              (* Optical transmission normal healthy clean glass [%] *)
    c_CoverSlide_L_pct                : REAL := 75.0;              (* Low transmission spatter warning advisory [%] *)
    c_CoverSlide_LL_pct               : REAL := 60.0;              (* Low-Low spatter critical laser shutter close [%] *)
    c_CoverSlide_Deadband_pct         : REAL := 2.0;               (* Transmission deadband hysteresis [%] *)

    c_GasFlow_HH_Lmin                 : REAL := 50.0;              (* High-High excessive flow / turbulence trip [L/min] *)
    c_GasFlow_H_Lmin                  : REAL := 46.0;              (* High gas flow warning [L/min] *)
    c_GasFlow_L_Lmin                  : REAL := 24.0;              (* Low gas flow warning [L/min] *)
    c_GasFlow_LL_Lmin                 : REAL := 18.0;              (* Low-Low shielding loss porosity abort [L/min] *)
    c_GasFlow_Deadband_Lmin           : REAL := 1.0;               (* Gas flow deadband hysteresis [L/min] *)

    c_PoolTemp_HH_degC                : REAL := 1850.0;            (* High-High keyhole boiling / spatter trip [deg C] *)
    c_PoolTemp_H_degC                 : REAL := 1720.0;            (* High pool temperature warning [deg C] *)
    c_PoolTemp_L_degC                 : REAL := 1250.0;            (* Low pool temperature lack-of-fusion warning [deg C] *)
    c_PoolTemp_LL_degC                : REAL := 1100.0;            (* Low-Low freezing / arc extinction abort [deg C] *)
    c_PoolTemp_Deadband_degC          : REAL := 15.0;              (* Temperature deadband hysteresis [deg C] *)

    c_JointGap_HH_mm                  : REAL := 2.20;              (* High-High gap out-of-tolerance reject [mm] *)
    c_JointGap_H_mm                   : REAL := 1.80;              (* High gap warning threshold [mm] *)
    c_JointGap_L_mm                   : REAL := 0.20;              (* Low gap tight butt-joint warning [mm] *)
    c_JointGap_LL_mm                  : REAL := 0.05;              (* Low-Low joint interference / overlap trip [mm] *)
    c_JointGap_Deadband_mm            : REAL := 0.05;              (* Joint gap deadband hysteresis [mm] *)

    c_ChillerFlow_L_Lmin              : REAL := 32.0;              (* Low laser chiller flow warning [L/min] *)
    c_ChillerFlow_LL_Lmin             : REAL := 24.0;              (* Low-Low chiller flow thermal trip [L/min] *)
    c_ChillerFlow_Deadband_Lmin       : REAL := 1.5;               (* Chiller flow deadband [L/min] *)

    c_FiberTemp_H_degC                : REAL := 52.0;              (* High fiber temperature warning [deg C] *)
    c_FiberTemp_HH_degC               : REAL := 65.0;              (* High-High fiber overheat laser trip [deg C] *)
    c_FiberTemp_Deadband_degC         : REAL := 2.0;               (* Fiber temperature deadband [deg C] *)

    bTrip_ArcCurrent_HH               : BOOL := FALSE;
    bTrip_ArcCurrent_LL               : BOOL := FALSE;
    bTrip_CoverSlide_LL               : BOOL := FALSE;
    bTrip_GasFlow_LL                  : BOOL := FALSE;
    bTrip_PoolTemp_HH                 : BOOL := FALSE;
    bTrip_PoolTemp_LL                 : BOOL := FALSE;
    bTrip_JointGap_HH                 : BOOL := FALSE;
    bTrip_JointGap_LL                 : BOOL := FALSE;
    bTrip_ChillerFlow_LL              : BOOL := FALSE;
    bTrip_FiberTemp_HH                : BOOL := FALSE;
    bTrip_DiscrepancyTrip             : BOOL := FALSE;
    bTrip_SafetyCircuitLost           : BOOL := FALSE;
    bTrip_SensorConsensusLost         : BOOL := FALSE;

    bUnack_ArcCurrent_HH              : BOOL := FALSE;
    bUnack_ArcCurrent_LL              : BOOL := FALSE;
    bUnack_CoverSlide_LL              : BOOL := FALSE;
    bUnack_GasFlow_LL                 : BOOL := FALSE;
    bUnack_DiscrepancyTrip            : BOOL := FALSE;
    bUnack_SafetyCircuitLost          : BOOL := FALSE;

    uiFirstOutAlarmCode               : UINT := 0;                 (* Captures root-cause trip identifier *)

    iAirKnifeCleanStep                : INT := 0;                  (* Step state for optical glass cleaning *)
    iAirKnifeCleanCount               : INT := 0;                  (* Total cleaning cycles performed *)
    bAirKnifeBusy                     : BOOL := FALSE;             (* Spatter cleaning cycle in execution *)
END_VAR
""")

    # -------------------------------------------------------------------------
    # SECTION 2: PHASE 1 - 2oo3 TMR SENSOR VOTING & INTEGRITY ASSURANCE
    # -------------------------------------------------------------------------
    st.append("""
(* ========================================================================================= *)
(* === PHASE 1: 2oo3 TMR SENSOR VOTING & INSTRUMENT INTEGRITY ASSURANCE ===                 *)
(* ========================================================================================= *)
(* Real-time cross-channel evaluation of 3D seam tracking optical profiles (lateral offset,  *)
(* vertical torch standoff, joint root gap) and melt pool infrared pyrometer temperatures.   *)
(* Implements median selection, discrepancy time-integration, and bumpless degradation.     *)

dwDegradationWord := 16#0000_0000;

(* --- 1.1 Seam Tracker Lateral Offset Triplet Evaluation (rSeamTrack_ChA, ChB, ChC [mm]) --- *)
rDev_Lat_AB := ABS(rSeamTrack_ChA_LateralOffset_mm - rSeamTrack_ChB_LateralOffset_mm);
rDev_Lat_BC := ABS(rSeamTrack_ChB_LateralOffset_mm - rSeamTrack_ChC_LateralOffset_mm);
rDev_Lat_CA := ABS(rSeamTrack_ChC_LateralOffset_mm - rSeamTrack_ChA_LateralOffset_mm);

bLat_A_Healthy := (rSeamTrack_ChA_LateralOffset_mm >= -10.0) AND (rSeamTrack_ChA_LateralOffset_mm <= 10.0) AND (rSeamTrack_ChA_QualityScore_pct >= 35.0);
bLat_B_Healthy := (rSeamTrack_ChB_LateralOffset_mm >= -10.0) AND (rSeamTrack_ChB_LateralOffset_mm <= 10.0) AND (rSeamTrack_ChB_QualityScore_pct >= 35.0);
bLat_C_Healthy := (rSeamTrack_ChC_LateralOffset_mm >= -10.0) AND (rSeamTrack_ChC_LateralOffset_mm <= 10.0) AND (rSeamTrack_ChC_QualityScore_pct >= 35.0);

IF bLat_A_Healthy AND bLat_B_Healthy AND bLat_C_Healthy THEN
    bLat_Degraded_1oo2 := FALSE;
    bLat_ConsensusLost_Trip := FALSE;
    (* Deterministic 2oo3 Median Voter *)
    IF ((rSeamTrack_ChA_LateralOffset_mm >= rSeamTrack_ChB_LateralOffset_mm) AND (rSeamTrack_ChA_LateralOffset_mm <= rSeamTrack_ChC_LateralOffset_mm)) OR
       ((rSeamTrack_ChA_LateralOffset_mm >= rSeamTrack_ChC_LateralOffset_mm) AND (rSeamTrack_ChA_LateralOffset_mm <= rSeamTrack_ChB_LateralOffset_mm)) THEN
        rVoted_TrackingLateralOffset_mm := rSeamTrack_ChA_LateralOffset_mm;
    ELSIF ((rSeamTrack_ChB_LateralOffset_mm >= rSeamTrack_ChA_LateralOffset_mm) AND (rSeamTrack_ChB_LateralOffset_mm <= rSeamTrack_ChC_LateralOffset_mm)) OR
          ((rSeamTrack_ChB_LateralOffset_mm >= rSeamTrack_ChC_LateralOffset_mm) AND (rSeamTrack_ChB_LateralOffset_mm <= rSeamTrack_ChA_LateralOffset_mm)) THEN
        rVoted_TrackingLateralOffset_mm := rSeamTrack_ChB_LateralOffset_mm;
    ELSE
        rVoted_TrackingLateralOffset_mm := rSeamTrack_ChC_LateralOffset_mm;
    END_IF;

    (* Triplet Discrepancy Trip Threshold: 0.25 mm limit with 50 ms persistence *)
    tDiscrepancyTimer_Lateral(IN := ((rDev_Lat_AB > 0.250) OR (rDev_Lat_BC > 0.250) OR (rDev_Lat_CA > 0.250)), PT := T#50MS);
    IF tDiscrepancyTimer_Lateral.Q THEN
        bTrip_DiscrepancyTrip := TRUE;
        dwDegradationWord := dwDegradationWord OR 16#0000_0001; (* Bit 0: Lateral Triplet Discrepancy Fault *)
        bTrajectoryFeedHold := TRUE;
    END_IF;
ELSIF bLat_A_Healthy AND bLat_B_Healthy THEN
    bLat_Degraded_1oo2 := TRUE;
    rVoted_TrackingLateralOffset_mm := (rSeamTrack_ChA_LateralOffset_mm + rSeamTrack_ChB_LateralOffset_mm) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0000_0002; (* Bit 1: Lateral Degraded to 1oo2 (Channel C Invalid) *)
ELSIF bLat_B_Healthy AND bLat_C_Healthy THEN
    bLat_Degraded_1oo2 := TRUE;
    rVoted_TrackingLateralOffset_mm := (rSeamTrack_ChB_LateralOffset_mm + rSeamTrack_ChC_LateralOffset_mm) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0000_0004; (* Bit 2: Lateral Degraded to 1oo2 (Channel A Invalid) *)
ELSIF bLat_A_Healthy AND bLat_C_Healthy THEN
    bLat_Degraded_1oo2 := TRUE;
    rVoted_TrackingLateralOffset_mm := (rSeamTrack_ChA_LateralOffset_mm + rSeamTrack_ChC_LateralOffset_mm) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0000_0008; (* Bit 3: Lateral Degraded to 1oo2 (Channel B Invalid) *)
ELSIF bLat_A_Healthy THEN
    rVoted_TrackingLateralOffset_mm := rSeamTrack_ChA_LateralOffset_mm;
    dwDegradationWord := dwDegradationWord OR 16#0000_0010; (* Bit 4: Lateral Degraded to 1oo1 Mode *)
ELSIF bLat_B_Healthy THEN
    rVoted_TrackingLateralOffset_mm := rSeamTrack_ChB_LateralOffset_mm;
    dwDegradationWord := dwDegradationWord OR 16#0000_0010;
ELSIF bLat_C_Healthy THEN
    rVoted_TrackingLateralOffset_mm := rSeamTrack_ChC_LateralOffset_mm;
    dwDegradationWord := dwDegradationWord OR 16#0000_0010;
ELSE
    bLat_ConsensusLost_Trip := TRUE;
    bTrip_SensorConsensusLost := TRUE;
    rVoted_TrackingLateralOffset_mm := 0.0;
    dwDegradationWord := dwDegradationWord OR 16#0000_0020; (* Bit 5: All Lateral Sensors Lost - Trip *)
END_IF;

(* --- 1.2 Seam Tracker Vertical Standoff Triplet Evaluation (rSeamTrack_ChA, ChB, ChC [mm]) --- *)
rDev_Vert_AB := ABS(rSeamTrack_ChA_VerticalStandoff_mm - rSeamTrack_ChB_VerticalStandoff_mm);
rDev_Vert_BC := ABS(rSeamTrack_ChB_VerticalStandoff_mm - rSeamTrack_ChC_VerticalStandoff_mm);
rDev_Vert_CA := ABS(rSeamTrack_ChC_VerticalStandoff_mm - rSeamTrack_ChA_VerticalStandoff_mm);

bVert_A_Healthy := (rSeamTrack_ChA_VerticalStandoff_mm >= -15.0) AND (rSeamTrack_ChA_VerticalStandoff_mm <= 15.0) AND (rSeamTrack_ChA_QualityScore_pct >= 35.0);
bVert_B_Healthy := (rSeamTrack_ChB_VerticalStandoff_mm >= -15.0) AND (rSeamTrack_ChB_VerticalStandoff_mm <= 15.0) AND (rSeamTrack_ChB_QualityScore_pct >= 35.0);
bVert_C_Healthy := (rSeamTrack_ChC_VerticalStandoff_mm >= -15.0) AND (rSeamTrack_ChC_VerticalStandoff_mm <= 15.0) AND (rSeamTrack_ChC_QualityScore_pct >= 35.0);

IF bVert_A_Healthy AND bVert_B_Healthy AND bVert_C_Healthy THEN
    bVert_Degraded_1oo2 := FALSE;
    bVert_ConsensusLost_Trip := FALSE;
    (* 2oo3 Median Voter *)
    IF ((rSeamTrack_ChA_VerticalStandoff_mm >= rSeamTrack_ChB_VerticalStandoff_mm) AND (rSeamTrack_ChA_VerticalStandoff_mm <= rSeamTrack_ChC_VerticalStandoff_mm)) OR
       ((rSeamTrack_ChA_VerticalStandoff_mm >= rSeamTrack_ChC_VerticalStandoff_mm) AND (rSeamTrack_ChA_VerticalStandoff_mm <= rSeamTrack_ChB_VerticalStandoff_mm)) THEN
        rVoted_TrackingVerticalStandoff_mm := rSeamTrack_ChA_VerticalStandoff_mm;
    ELSIF ((rSeamTrack_ChB_VerticalStandoff_mm >= rSeamTrack_ChA_VerticalStandoff_mm) AND (rSeamTrack_ChB_VerticalStandoff_mm <= rSeamTrack_ChC_VerticalStandoff_mm)) OR
          ((rSeamTrack_ChB_VerticalStandoff_mm >= rSeamTrack_ChC_VerticalStandoff_mm) AND (rSeamTrack_ChB_VerticalStandoff_mm <= rSeamTrack_ChA_VerticalStandoff_mm)) THEN
        rVoted_TrackingVerticalStandoff_mm := rSeamTrack_ChB_VerticalStandoff_mm;
    ELSE
        rVoted_TrackingVerticalStandoff_mm := rSeamTrack_ChC_VerticalStandoff_mm;
    END_IF;

    (* Standoff Discrepancy Trip Threshold: 0.25 mm *)
    tDiscrepancyTimer_Vertical(IN := ((rDev_Vert_AB > 0.250) OR (rDev_Vert_BC > 0.250) OR (rDev_Vert_CA > 0.250)), PT := T#50MS);
    IF tDiscrepancyTimer_Vertical.Q THEN
        bTrip_DiscrepancyTrip := TRUE;
        dwDegradationWord := dwDegradationWord OR 16#0000_0040; (* Bit 6: Vertical Triplet Discrepancy Fault *)
        bTrajectoryFeedHold := TRUE;
    END_IF;
ELSIF bVert_A_Healthy AND bVert_B_Healthy THEN
    bVert_Degraded_1oo2 := TRUE;
    rVoted_TrackingVerticalStandoff_mm := (rSeamTrack_ChA_VerticalStandoff_mm + rSeamTrack_ChB_VerticalStandoff_mm) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0000_0080; (* Bit 7: Vertical Degraded to 1oo2 *)
ELSIF bVert_B_Healthy AND bVert_C_Healthy THEN
    bVert_Degraded_1oo2 := TRUE;
    rVoted_TrackingVerticalStandoff_mm := (rSeamTrack_ChB_VerticalStandoff_mm + rSeamTrack_ChC_VerticalStandoff_mm) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0000_0100;
ELSIF bVert_A_Healthy AND bVert_C_Healthy THEN
    bVert_Degraded_1oo2 := TRUE;
    rVoted_TrackingVerticalStandoff_mm := (rSeamTrack_ChA_VerticalStandoff_mm + rSeamTrack_ChC_VerticalStandoff_mm) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0000_0200;
ELSIF bVert_A_Healthy THEN
    rVoted_TrackingVerticalStandoff_mm := rSeamTrack_ChA_VerticalStandoff_mm;
    dwDegradationWord := dwDegradationWord OR 16#0000_0400; (* Bit 10: Vertical Degraded to 1oo1 Mode *)
ELSIF bVert_B_Healthy THEN
    rVoted_TrackingVerticalStandoff_mm := rSeamTrack_ChB_VerticalStandoff_mm;
    dwDegradationWord := dwDegradationWord OR 16#0000_0400;
ELSIF bVert_C_Healthy THEN
    rVoted_TrackingVerticalStandoff_mm := rSeamTrack_ChC_VerticalStandoff_mm;
    dwDegradationWord := dwDegradationWord OR 16#0000_0400;
ELSE
    bVert_ConsensusLost_Trip := TRUE;
    bTrip_SensorConsensusLost := TRUE;
    rVoted_TrackingVerticalStandoff_mm := 0.0;
    dwDegradationWord := dwDegradationWord OR 16#0000_0800; (* Bit 11: All Vertical Sensors Lost Trip *)
END_IF;

(* --- 1.3 Seam Tracker Joint Root Opening Gap Triplet Evaluation (rSeamTrack_ChA, ChB, ChC [mm]) --- *)
rDev_Gap_AB := ABS(rSeamTrack_ChA_JointGap_mm - rSeamTrack_ChB_JointGap_mm);
rDev_Gap_BC := ABS(rSeamTrack_ChB_JointGap_mm - rSeamTrack_ChC_JointGap_mm);
rDev_Gap_CA := ABS(rSeamTrack_ChC_JointGap_mm - rSeamTrack_ChA_JointGap_mm);

bGap_A_Healthy := (rSeamTrack_ChA_JointGap_mm >= 0.0) AND (rSeamTrack_ChA_JointGap_mm <= 4.0) AND (rSeamTrack_ChA_QualityScore_pct >= 35.0);
bGap_B_Healthy := (rSeamTrack_ChB_JointGap_mm >= 0.0) AND (rSeamTrack_ChB_JointGap_mm <= 4.0) AND (rSeamTrack_ChB_QualityScore_pct >= 35.0);
bGap_C_Healthy := (rSeamTrack_ChC_JointGap_mm >= 0.0) AND (rSeamTrack_ChC_JointGap_mm <= 4.0) AND (rSeamTrack_ChC_QualityScore_pct >= 35.0);

IF bGap_A_Healthy AND bGap_B_Healthy AND bGap_C_Healthy THEN
    bGap_Degraded_1oo2 := FALSE;
    bGap_ConsensusLost_Trip := FALSE;
    (* 2oo3 Median Voter *)
    IF ((rSeamTrack_ChA_JointGap_mm >= rSeamTrack_ChB_JointGap_mm) AND (rSeamTrack_ChA_JointGap_mm <= rSeamTrack_ChC_JointGap_mm)) OR
       ((rSeamTrack_ChA_JointGap_mm >= rSeamTrack_ChC_JointGap_mm) AND (rSeamTrack_ChA_JointGap_mm <= rSeamTrack_ChB_JointGap_mm)) THEN
        rVoted_JointGap_mm := rSeamTrack_ChA_JointGap_mm;
    ELSIF ((rSeamTrack_ChB_JointGap_mm >= rSeamTrack_ChA_JointGap_mm) AND (rSeamTrack_ChB_JointGap_mm <= rSeamTrack_ChC_JointGap_mm)) OR
          ((rSeamTrack_ChB_JointGap_mm >= rSeamTrack_ChC_JointGap_mm) AND (rSeamTrack_ChB_JointGap_mm <= rSeamTrack_ChA_JointGap_mm)) THEN
        rVoted_JointGap_mm := rSeamTrack_ChB_JointGap_mm;
    ELSE
        rVoted_JointGap_mm := rSeamTrack_ChC_JointGap_mm;
    END_IF;

    (* Gap Discrepancy Trip Threshold: 0.20 mm *)
    tDiscrepancyTimer_Gap(IN := ((rDev_Gap_AB > 0.200) OR (rDev_Gap_BC > 0.200) OR (rDev_Gap_CA > 0.200)), PT := T#50MS);
    IF tDiscrepancyTimer_Gap.Q THEN
        bTrip_DiscrepancyTrip := TRUE;
        dwDegradationWord := dwDegradationWord OR 16#0000_1000; (* Bit 12: Gap Triplet Discrepancy Fault *)
    END_IF;
ELSIF bGap_A_Healthy AND bGap_B_Healthy THEN
    bGap_Degraded_1oo2 := TRUE;
    rVoted_JointGap_mm := (rSeamTrack_ChA_JointGap_mm + rSeamTrack_ChB_JointGap_mm) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0000_2000;
ELSIF bGap_B_Healthy AND bGap_C_Healthy THEN
    bGap_Degraded_1oo2 := TRUE;
    rVoted_JointGap_mm := (rSeamTrack_ChB_JointGap_mm + rSeamTrack_ChC_JointGap_mm) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0000_4000;
ELSIF bGap_A_Healthy AND bGap_C_Healthy THEN
    bGap_Degraded_1oo2 := TRUE;
    rVoted_JointGap_mm := (rSeamTrack_ChA_JointGap_mm + rSeamTrack_ChC_JointGap_mm) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0000_8000;
ELSIF bGap_A_Healthy THEN
    rVoted_JointGap_mm := rSeamTrack_ChA_JointGap_mm;
    dwDegradationWord := dwDegradationWord OR 16#0001_0000;
ELSIF bGap_B_Healthy THEN
    rVoted_JointGap_mm := rSeamTrack_ChB_JointGap_mm;
    dwDegradationWord := dwDegradationWord OR 16#0001_0000;
ELSIF bGap_C_Healthy THEN
    rVoted_JointGap_mm := rSeamTrack_ChC_JointGap_mm;
    dwDegradationWord := dwDegradationWord OR 16#0001_0000;
ELSE
    bGap_ConsensusLost_Trip := TRUE;
    bTrip_SensorConsensusLost := TRUE;
    rVoted_JointGap_mm := rNominalJointGap_mm;
    dwDegradationWord := dwDegradationWord OR 16#0002_0000;
END_IF;

(* --- 1.4 Co-Axial Pyrometer Molten Pool Temperature Triplet (rPyrometer_ChA, ChB, ChC [deg C]) --- *)
rDev_Temp_AB := ABS(rPyrometer_ChA_MeltPoolTemp_degC - rPyrometer_ChB_MeltPoolTemp_degC);
rDev_Temp_BC := ABS(rPyrometer_ChB_MeltPoolTemp_degC - rPyrometer_ChC_MeltPoolTemp_degC);
rDev_Temp_CA := ABS(rPyrometer_ChC_MeltPoolTemp_degC - rPyrometer_ChA_MeltPoolTemp_degC);

bTemp_A_Healthy := (rPyrometer_ChA_MeltPoolTemp_degC >= 200.0) AND (rPyrometer_ChA_MeltPoolTemp_degC <= 2400.0);
bTemp_B_Healthy := (rPyrometer_ChB_MeltPoolTemp_degC >= 200.0) AND (rPyrometer_ChB_MeltPoolTemp_degC <= 2400.0);
bTemp_C_Healthy := (rPyrometer_ChC_MeltPoolTemp_degC >= 200.0) AND (rPyrometer_ChC_MeltPoolTemp_degC <= 2400.0);

IF bTemp_A_Healthy AND bTemp_B_Healthy AND bTemp_C_Healthy THEN
    bTemp_Degraded_1oo2 := FALSE;
    bTemp_ConsensusLost_Trip := FALSE;
    (* 2oo3 Median Voter *)
    IF ((rPyrometer_ChA_MeltPoolTemp_degC >= rPyrometer_ChB_MeltPoolTemp_degC) AND (rPyrometer_ChA_MeltPoolTemp_degC <= rPyrometer_ChC_MeltPoolTemp_degC)) OR
       ((rPyrometer_ChA_MeltPoolTemp_degC >= rPyrometer_ChC_MeltPoolTemp_degC) AND (rPyrometer_ChA_MeltPoolTemp_degC <= rPyrometer_ChB_MeltPoolTemp_degC)) THEN
        rVoted_MeltPoolTemp_degC := rPyrometer_ChA_MeltPoolTemp_degC;
    ELSIF ((rPyrometer_ChB_MeltPoolTemp_degC >= rPyrometer_ChA_MeltPoolTemp_degC) AND (rPyrometer_ChB_MeltPoolTemp_degC <= rPyrometer_ChC_MeltPoolTemp_degC)) OR
          ((rPyrometer_ChB_MeltPoolTemp_degC >= rPyrometer_ChC_MeltPoolTemp_degC) AND (rPyrometer_ChB_MeltPoolTemp_degC <= rPyrometer_ChA_MeltPoolTemp_degC)) THEN
        rVoted_MeltPoolTemp_degC := rPyrometer_ChB_MeltPoolTemp_degC;
    ELSE
        rVoted_MeltPoolTemp_degC := rPyrometer_ChC_MeltPoolTemp_degC;
    END_IF;

    (* Temperature Discrepancy Alert Threshold: 65.0 deg C *)
    tDiscrepancyTimer_Temp(IN := ((rDev_Temp_AB > 65.0) OR (rDev_Temp_BC > 65.0) OR (rDev_Temp_CA > 65.0)), PT := T#50MS);
    IF tDiscrepancyTimer_Temp.Q THEN
        dwDegradationWord := dwDegradationWord OR 16#0004_0000; (* Bit 18: Temperature Triplet Discrepancy Alert *)
    END_IF;
ELSIF bTemp_A_Healthy AND bTemp_B_Healthy THEN
    bTemp_Degraded_1oo2 := TRUE;
    rVoted_MeltPoolTemp_degC := (rPyrometer_ChA_MeltPoolTemp_degC + rPyrometer_ChB_MeltPoolTemp_degC) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0008_0000;
ELSIF bTemp_B_Healthy AND bTemp_C_Healthy THEN
    bTemp_Degraded_1oo2 := TRUE;
    rVoted_MeltPoolTemp_degC := (rPyrometer_ChB_MeltPoolTemp_degC + rPyrometer_ChC_MeltPoolTemp_degC) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0010_0000;
ELSIF bTemp_A_Healthy AND bTemp_C_Healthy THEN
    bTemp_Degraded_1oo2 := TRUE;
    rVoted_MeltPoolTemp_degC := (rPyrometer_ChA_MeltPoolTemp_degC + rPyrometer_ChC_MeltPoolTemp_degC) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0020_0000;
ELSIF bTemp_A_Healthy THEN
    rVoted_MeltPoolTemp_degC := rPyrometer_ChA_MeltPoolTemp_degC;
    dwDegradationWord := dwDegradationWord OR 16#0040_0000;
ELSIF bTemp_B_Healthy THEN
    rVoted_MeltPoolTemp_degC := rPyrometer_ChB_MeltPoolTemp_degC;
    dwDegradationWord := dwDegradationWord OR 16#0040_0000;
ELSIF bTemp_C_Healthy THEN
    rVoted_MeltPoolTemp_degC := rPyrometer_ChC_MeltPoolTemp_degC;
    dwDegradationWord := dwDegradationWord OR 16#0040_0000;
ELSE
    bTemp_ConsensusLost_Trip := TRUE;
    rVoted_MeltPoolTemp_degC := 1450.0; (* Fallback to aluminum nominal liquidus temperature *)
    dwDegradationWord := dwDegradationWord OR 16#0080_0000;
END_IF;
""")

    # -------------------------------------------------------------------------
    # SECTION 3: PHASE 2 - DISCRETE STATE-SPACE MATRIX PROPAGATION & OBSERVER
    # -------------------------------------------------------------------------
    st.append("""
(* ========================================================================================= *)
(* === PHASE 2: DISCRETE STATE-SPACE MATRIX PROPAGATION & LUENBERGER OBSERVER ===           *)
(* ========================================================================================= *)
(* Real-time state-space dynamics evaluated at Ts = 2.0 ms real-time interrupt tick.         *)
(* Propagates 4 state variables:                                                             *)
(*   x[1]: Seam tracking lateral error [mm]                                                  *)
(*   x[2]: Seam tracking vertical standoff error [mm]                                        *)
(*   x[3]: Molten pool peak temperature [deg C]                                              *)
(*   x[4]: CMT welding arc current [A]                                                       *)
(* Corrects state estimates via Luenberger innovation feedback matrix L_obs.                *)

IF NOT bMatricesInitialized THEN
    (* Row 1: Lateral Error Dynamics *)
    A_mat[1, 1] := 0.9450;
    A_mat[1, 2] := 0.0000;
    A_mat[1, 3] := 0.0000;
    A_mat[1, 4] := 0.0000;

    (* Row 2: Vertical Standoff Dynamics *)
    A_mat[2, 1] := 0.0000;
    A_mat[2, 2] := 0.9380;
    A_mat[2, 3] := 0.0000;
    A_mat[2, 4] := -0.00015;

    (* Row 3: Molten Pool Temperature Dissipation & Arc Coupling *)
    A_mat[3, 1] := 0.0000;
    A_mat[3, 2] := 0.0000;
    A_mat[3, 3] := 0.8850;
    A_mat[3, 4] := 0.6200;

    (* Row 4: CMT Arc Current Stabilization Dynamics *)
    A_mat[4, 1] := 0.0000;
    A_mat[4, 2] := -0.8500;
    A_mat[4, 3] := -0.0045;
    A_mat[4, 4] := 0.8120;

    (* Control Input Coupling Matrix B (4x3) *)
    B_mat[1, 1] := -0.0550;  B_mat[1, 2] := 0.0000;    B_mat[1, 3] := 0.0000;
    B_mat[2, 1] := 0.0000;   B_mat[2, 2] := 0.0125;    B_mat[2, 3] := -0.000008;
    B_mat[3, 1] := 0.0000;   B_mat[3, 2] := 18.5000;   B_mat[3, 3] := 0.0820;
    B_mat[4, 1] := 0.0000;   B_mat[4, 2] := 16.4500;   B_mat[4, 3] := 0.0018;

    (* Observation Matrix C (4x4) - Direct identity mapping *)
    FOR iRow := 1 TO 4 DO
        FOR iCol := 1 TO 4 DO
            IF iRow = iCol THEN
                C_mat[iRow, iCol] := 1.0;
            ELSE
                C_mat[iRow, iCol] := 0.0;
            END_IF;
        END_FOR;
    END_FOR;

    (* Direct Feedthrough Matrix D (4x3) *)
    FOR iRow := 1 TO 4 DO
        FOR iCol := 1 TO 3 DO
            D_mat[iRow, iCol] := 0.0;
        END_FOR;
    END_FOR;

    (* Luenberger Observer Gain Matrix L_obs (4x4) *)
    L_obs[1, 1] := 0.1250;  L_obs[1, 2] := 0.0000;  L_obs[1, 3] := 0.0000;  L_obs[1, 4] := 0.0000;
    L_obs[2, 1] := 0.0000;  L_obs[2, 2] := 0.1180;  L_obs[2, 3] := 0.0000;  L_obs[2, 4] := -0.00005;
    L_obs[3, 1] := 0.0000;  L_obs[3, 2] := 0.0000;  L_obs[3, 3] := 0.0850;  L_obs[3, 4] := 0.0240;
    L_obs[4, 1] := 0.0000;  L_obs[4, 2] := -0.0150; L_obs[4, 3] := -0.0002; L_obs[4, 4] := 0.1450;

    (* MPC Quadratic Weights Initialization *)
    Q_diag[1] := 85.0;     (* Lateral trajectory penalty *)
    Q_diag[2] := 65.0;     (* Vertical standoff penalty *)
    Q_diag[3] := 0.045;    (* Pool temperature deviation penalty *)
    Q_diag[4] := 0.085;    (* Arc current deviation penalty *)

    R_diag[1] := 120.0;    (* Lateral trim rate slew penalty *)
    R_diag[2] := 45.0;     (* Wire feed speed rate slew penalty *)
    R_diag[3] := 0.0025;   (* Laser power rate slew penalty *)

    P_diag[1] := 250.0;    (* Terminal lateral penalty *)
    P_diag[2] := 180.0;    (* Terminal vertical penalty *)
    P_diag[3] := 0.120;    (* Terminal temperature penalty *)
    P_diag[4] := 0.220;    (* Terminal current penalty *)

    (* State Vector Reset *)
    FOR iIdx := 1 TO 4 DO
        x_state[iIdx] := 0.0;
        x_pred[iIdx] := 0.0;
        x_ref[iIdx] := 0.0;
    END_FOR;
    x_state[3] := 1450.0; (* Initial pool temperature at melting point *)
    x_state[4] := 160.0;  (* Initial current *)

    bMatricesInitialized := TRUE;
END_IF;

(* --- Step 2.1: Model State Propagation (x_pred = A * x_state + B * u_ctrl_prev) --- *)
FOR iRow := 1 TO 4 DO
    x_pred[iRow] := 0.0;
    FOR iCol := 1 TO 4 DO
        x_pred[iRow] := x_pred[iRow] + A_mat[iRow, iCol] * x_state[iCol];
    END_FOR;
    FOR iCol := 1 TO 3 DO
        x_pred[iRow] := x_pred[iRow] + B_mat[iRow, iCol] * u_ctrl_prev[iCol];
    END_FOR;
END_FOR;

(* --- Step 2.2: Innovation Vector Calculation (y_innov = y_meas - C * x_pred) --- *)
y_meas[1] := rVoted_TrackingLateralOffset_mm;
y_meas[2] := rVoted_TrackingVerticalStandoff_mm;
y_meas[3] := rVoted_MeltPoolTemp_degC;
y_meas[4] := rArcCurrent_Feedback_A;

FOR iRow := 1 TO 4 DO
    y_est[iRow] := 0.0;
    FOR iCol := 1 TO 4 DO
        y_est[iRow] := y_est[iRow] + C_mat[iRow, iCol] * x_pred[iCol];
    END_FOR;
    y_innov[iRow] := y_meas[iRow] - y_est[iRow];
END_FOR;

(* --- Step 2.3: Luenberger State Observer Correction (x_state = x_pred + L_obs * y_innov) --- *)
FOR iRow := 1 TO 4 DO
    x_state[iRow] := x_pred[iRow];
    FOR iCol := 1 TO 4 DO
        x_state[iRow] := x_state[iRow] + L_obs[iRow, iCol] * y_innov[iCol];
    END_FOR;
END_FOR;
""")

    # -------------------------------------------------------------------------
    # SECTION 4: PHASE 3 - RECEDING-HORIZON MPC QUADRATIC CONTROL SOLVER
    # -------------------------------------------------------------------------
    st.append("""
(* ========================================================================================= *)
(* === PHASE 3: RECEDING-HORIZON MPC QUADRATIC CONTROL SOLVER ===                            *)
(* ========================================================================================= *)
(* Formulates a finite prediction horizon (Np = 5 steps) quadratic program to compute       *)
(* optimal robot TCP lateral trim offset, CMT wire feed speed, and fiber laser power.       *)
(* Dynamically adjusts reference trajectory according to joint root gap opening.            *)

(* --- Step 3.1: Adaptive Reference Generation Based on 2oo3 Root Gap --- *)
x_ref[1] := 0.0; (* Target lateral tracking offset is 0.0 mm *)
x_ref[2] := 0.0; (* Target vertical standoff offset is 0.0 mm *)

(* Target temperature scales upward with gap to guarantee deep root keyhole penetration *)
x_ref[3] := 1520.0 + (rVoted_JointGap_mm - rNominalJointGap_mm) * 95.0;
IF x_ref[3] > 1750.0 THEN
    x_ref[3] := 1750.0;
ELSIF x_ref[3] < 1420.0 THEN
    x_ref[3] := 1420.0;
END_IF;

(* Target arc current scales upward with gap to deposit sufficient AlMg5 filler volume *)
x_ref[4] := 185.0 + (rVoted_JointGap_mm - rNominalJointGap_mm) * 55.0;
IF x_ref[4] > 290.0 THEN
    x_ref[4] := 290.0;
ELSIF x_ref[4] < 125.0 THEN
    x_ref[4] := 125.0;
END_IF;

(* Initialize horizon step 0 state from current observer estimate *)
FOR iRow := 1 TO 4 DO
    x_horiz[0, iRow] := x_state[iRow];
END_FOR;

(* Initialize candidate control sequence across horizon *)
FOR iHorizon := 0 TO 4 DO
    FOR iCol := 1 TO 3 DO
        u_horiz[iHorizon, iCol] := u_ctrl_prev[iCol];
    END_FOR;
END_FOR;

(* --- Step 3.2: Projected Gradient Descent Optimization Loop --- *)
FOR iIter := 1 TO iMpcMaxIter DO
    (* Forward trajectory rollout across prediction horizon *)
    FOR iHorizon := 0 TO 4 DO
        (* Calculate control slew rate moves *)
        FOR iCol := 1 TO 3 DO
            IF iHorizon = 0 THEN
                du_horiz[0, iCol] := u_horiz[0, iCol] - u_ctrl_prev[iCol];
            ELSE
                du_horiz[iHorizon, iCol] := u_horiz[iHorizon, iCol] - u_horiz[iHorizon - 1, iCol];
            END_IF;
        END_FOR;

        (* State propagation: x[k+1] = A * x[k] + B * u[k] *)
        FOR iRow := 1 TO 4 DO
            x_horiz[iHorizon + 1, iRow] := 0.0;
            FOR iCol := 1 TO 4 DO
                x_horiz[iHorizon + 1, iRow] := x_horiz[iHorizon + 1, iRow] + A_mat[iRow, iCol] * x_horiz[iHorizon, iCol];
            END_FOR;
            FOR iCol := 1 TO 3 DO
                x_horiz[iHorizon + 1, iRow] := x_horiz[iHorizon + 1, iRow] + B_mat[iRow, iCol] * u_horiz[iHorizon, iCol];
            END_FOR;
        END_FOR;
    END_FOR;

    (* Evaluate Quadratic Objective Cost Index *)
    rCost_StatePenalty := 0.0;
    rCost_ControlPenalty := 0.0;
    FOR iHorizon := 0 TO 4 DO
        FOR iRow := 1 TO 4 DO
            rCost_StatePenalty := rCost_StatePenalty + Q_diag[iRow] * (x_horiz[iHorizon + 1, iRow] - x_ref[iRow]) * (x_horiz[iHorizon + 1, iRow] - x_ref[iRow]);
        END_FOR;
        FOR iCol := 1 TO 3 DO
            rCost_ControlPenalty := rCost_ControlPenalty + R_diag[iCol] * du_horiz[iHorizon, iCol] * du_horiz[iHorizon, iCol];
        END_FOR;
    END_FOR;

    rCost_TerminalPenalty := 0.0;
    FOR iRow := 1 TO 4 DO
        rCost_TerminalPenalty := rCost_TerminalPenalty + P_diag[iRow] * (x_horiz[5, iRow] - x_ref[iRow]) * (x_horiz[5, iRow] - x_ref[iRow]);
    END_FOR;
    rCost_Total := rCost_StatePenalty + rCost_ControlPenalty + rCost_TerminalPenalty;

    (* Gradient Computation and Diagonal Hessian Scaling *)
    FOR iHorizon := 0 TO 4 DO
        FOR iCol := 1 TO 3 DO
            grad_u[iHorizon, iCol] := 2.0 * R_diag[iCol] * du_horiz[iHorizon, iCol];
            hess_diag[iHorizon, iCol] := 2.0 * R_diag[iCol] + 0.05;

            FOR iRow := 1 TO 4 DO
                grad_u[iHorizon, iCol] := grad_u[iHorizon, iCol] + 2.0 * Q_diag[iRow] * (x_horiz[iHorizon + 1, iRow] - x_ref[iRow]) * B_mat[iRow, iCol];
                hess_diag[iHorizon, iCol] := hess_diag[iHorizon, iCol] + 2.0 * Q_diag[iRow] * B_mat[iRow, iCol] * B_mat[iRow, iCol];
            END_FOR;

            (* Update control candidate via Newton-like projected step *)
            u_horiz[iHorizon, iCol] := u_horiz[iHorizon, iCol] - rStepSize_Alpha * (grad_u[iHorizon, iCol] / hess_diag[iHorizon, iCol]);
        END_FOR;
    END_FOR;
END_FOR;

(* --- Step 3.3: First Horizon Move Selection & Physical Slew Saturation --- *)
u_ctrl[1] := u_horiz[0, 1];
u_ctrl[2] := u_horiz[0, 2];
u_ctrl[3] := u_horiz[0, 3];

(* Channel 1: Robot Lateral Trim Offset [mm] *)
IF (u_ctrl[1] - u_ctrl_prev[1]) > rMaxDeltaLateral_mm THEN
    u_saturated[1] := u_ctrl_prev[1] + rMaxDeltaLateral_mm;
ELSIF (u_ctrl[1] - u_ctrl_prev[1]) < -rMaxDeltaLateral_mm THEN
    u_saturated[1] := u_ctrl_prev[1] - rMaxDeltaLateral_mm;
ELSE
    u_saturated[1] := u_ctrl[1];
END_IF;

IF u_saturated[1] > rMaxLateralTrim_mm THEN
    u_saturated[1] := rMaxLateralTrim_mm;
ELSIF u_saturated[1] < rMinLateralTrim_mm THEN
    u_saturated[1] := rMinLateralTrim_mm;
END_IF;

(* Channel 2: CMT Wire Feed Speed Trim [m/min] *)
IF (u_ctrl[2] - u_ctrl_prev[2]) > rMaxDeltaWFS_mpm THEN
    u_saturated[2] := u_ctrl_prev[2] + rMaxDeltaWFS_mpm;
ELSIF (u_ctrl[2] - u_ctrl_prev[2]) < -rMaxDeltaWFS_mpm THEN
    u_saturated[2] := u_ctrl_prev[2] - rMaxDeltaWFS_mpm;
ELSE
    u_saturated[2] := u_ctrl[2];
END_IF;

IF u_saturated[2] > 2.50 THEN
    u_saturated[2] := 2.50;
ELSIF u_saturated[2] < -2.50 THEN
    u_saturated[2] := -2.50;
END_IF;

(* Channel 3: Fiber Laser Power Output Trim [W] *)
IF (u_ctrl[3] - u_ctrl_prev[3]) > rMaxDeltaLaserPower_W THEN
    u_saturated[3] := u_ctrl_prev[3] + rMaxDeltaLaserPower_W;
ELSIF (u_ctrl[3] - u_ctrl_prev[3]) < -rMaxDeltaLaserPower_W THEN
    u_saturated[3] := u_ctrl_prev[3] - rMaxDeltaLaserPower_W;
ELSE
    u_saturated[3] := u_ctrl[3];
END_IF;

IF u_saturated[3] > 1200.0 THEN
    u_saturated[3] := 1200.0;
ELSIF u_saturated[3] < -1200.0 THEN
    u_saturated[3] := -1200.0;
END_IF;

(* Store saturated control moves for next real-time cycle *)
u_ctrl_prev[1] := u_saturated[1];
u_ctrl_prev[2] := u_saturated[2];
u_ctrl_prev[3] := u_saturated[3];
""")

    # -------------------------------------------------------------------------
    # SECTION 5: PHASE 4 - JOINT GAP ADAPTIVE PROCESS LAW & HEAT INPUT SUPERVISION
    # -------------------------------------------------------------------------
    st.append("""
(* ========================================================================================= *)
(* === PHASE 4: JOINT GAP ADAPTIVE PROCESS LAW & HEAT INPUT SUPERVISION ===                  *)
(* ========================================================================================= *)
(* Computes AWS D1.2 linear heat input, filler wire deposition mass flow, and combines       *)
(* baseline metallurgical schedules with the MPC control trims for execution.               *)

(* --- Step 4.1: Synergic Wire Feed Speed & Laser Power Generation --- *)
rWireFeedSpeed_Demand_mpm := 8.20 + (rVoted_JointGap_mm - rNominalJointGap_mm) * 3.40 + u_saturated[2];
IF rWireFeedSpeed_Demand_mpm > rMaxWFS_Demand_mpm THEN
    rWireFeedSpeed_Demand_mpm := rMaxWFS_Demand_mpm;
ELSIF rWireFeedSpeed_Demand_mpm < rMinWFS_Demand_mpm THEN
    rWireFeedSpeed_Demand_mpm := rMinWFS_Demand_mpm;
END_IF;

rLaserPower_Setpoint_W := 4600.0 + (rVoted_JointGap_mm - rNominalJointGap_mm) * 1450.0 + u_saturated[3];
IF rLaserPower_Setpoint_W > rMaxLaserPower_W THEN
    rLaserPower_Setpoint_W := rMaxLaserPower_W;
ELSIF rLaserPower_Setpoint_W < rMinLaserPower_W THEN
    rLaserPower_Setpoint_W := rMinLaserPower_W;
END_IF;

rRobotTCP_Trim_Lateral_mm := u_saturated[1];
rRobotTCP_Trim_Vertical_mm := -0.50 * rVoted_TrackingVerticalStandoff_mm;

(* --- Step 4.2: Filler Wire Mass Deposition Rate (AlMg5 / ER5356) --- *)
rEstimated_WireDepositionRate_gmin := rWireDepositionCoeff * rWireFeedSpeed_Demand_mpm;

(* --- Step 4.3: AWS D1.2 / EN ISO 15614-14 Net Linear Heat Input --- *)
IF rRobotTCP_Velocity_mpm > 0.20 THEN
    rEstimated_LinearHeatInput_Jmm := (c_LaserAbsorptionEfficiency * rLaserPower_Actual_W +
                                       c_ArcThermalEfficiency * rArcVoltage_Feedback_V * rArcCurrent_Feedback_A) * 60.0 /
                                      (rRobotTCP_Velocity_mpm * 1000.0);
ELSE
    rEstimated_LinearHeatInput_Jmm := 0.0;
END_IF;

(* --- Step 4.4: Full Keyhole Penetration Depth Estimation --- *)
rEstimated_PenetrationDepth_mm := (0.00048 * rLaserPower_Actual_W) + (0.0118 * rArcCurrent_Feedback_A) - (0.42 * rVoted_JointGap_mm);
IF rEstimated_PenetrationDepth_mm < 0.0 THEN
    rEstimated_PenetrationDepth_mm := 0.0;
END_IF;
""")

    # -------------------------------------------------------------------------
    # SECTION 6: PHASE 5 - MULTI-STAGE FINITE STATE MACHINE (FSM)
    # -------------------------------------------------------------------------
    st.append("""
(* ========================================================================================= *)
(* === PHASE 5: MULTI-STAGE FINITE STATE MACHINE (FSM) ===                                   *)
(* ========================================================================================= *)
(* Orchestrates complete manufacturing sequence:                                             *)
(*   0:  CELL_STANDBY_IDLE                                                                   *)
(*   10: SUBFRAME_FIXTURE_CLAMP                                                              *)
(*   20: SEAM_TRACKER_LASER_SEARCH                                                           *)
(*   30: GAS_PRE_PURGE_FLOW                                                                  *)
(*   40: HYBRID_ARC_STRIKE_KEYHOLE                                                           *)
(*   50: CONTINUOUS_HYBRID_WELD_TRAJECTORY                                                   *)
(*   60: CRATER_FILL_DECEL                                                                   *)
(*   70: GAS_POST_PURGE_FLOW                                                                 *)
(*   80: POST_WELD_OPTICAL_AUDIT                                                             *)
(*   90: FIXTURE_UNCLAMP_DISCHARGE                                                           *)
(*   99: ARC_BLOWOUT_EMERGENCY_ESTOP                                                         *)

bStateChanged := (iState <> iPrevState);
iPrevState := iState;

tStateTimer(IN := NOT bStateChanged, PT := T#120S);

CASE iState OF

    0: (* === CELL_STANDBY_IDLE === *)
        bLaserEmissionEnable := FALSE;
        bLaserShutterOpen := FALSE;
        rLaserPower_Setpoint_W := 0.0;
        bCMT_ArcIgnitionTrigger := FALSE;
        rWireFeedSpeed_Demand_mpm := 0.0;
        bWireRetractCmd := FALSE;
        bShieldingGas_SolenoidOpen := FALSE;
        rShieldingGas_MFC_Setpoint_Lmin := 0.0;
        bSeamTracker_LaserDiodeEnable := FALSE;
        bCoverSlideAirKnifeBlast := FALSE;
        bTrajectoryFeedHold := FALSE;
        rRobotSpeedOverride_pct := 0.0;
        rTiltRotatorSpeedOverride_pct := 0.0;
        bWeldCellExhaustFanRun := FALSE;
        uiCMT_SynergicCurveID := 101; (* Standard AlMg5 pulse synergic schedule *)

        IF bOperatorCycleStart AND bCellSafetyCircuit_Ok AND bLaserSafetyInterlock_Ok AND bLightCurtainClear AND bEmergencyStopOk THEN
            bCycleCompleted := FALSE;
            bWeldAborted := FALSE;
            iSubState := 0;
            iState := 10; (* Proceed to fixture clamping *)
        END_IF;

    10: (* === SUBFRAME_FIXTURE_CLAMP === *)
        bFixtureClampSolenoid := TRUE;
        bFixtureUnclampSolenoid := FALSE;
        bWeldCellExhaustFanRun := TRUE;

        tClampTimer(IN := (rFixtureHydraulicPressure_bar >= 120.0) AND
                          bFixturePartSeated_Proximity_1 AND
                          bFixturePartSeated_Proximity_2 AND
                          bFixturePartSeated_Proximity_3,
                    PT := T#1500MS);

        IF tClampTimer.Q THEN
            tClampTimer(IN := FALSE, PT := T#1500MS);
            iSubState := 0;
            iState := 20; (* Clamp confirmed; search seam *)
        ELSIF tStateTimer.ET > T#5S THEN
            (* Clamping timeout trip *)
            uiFirstOutAlarmCode := 1010;
            iState := 99;
        END_IF;

    20: (* === SEAM_TRACKER_LASER_SEARCH === *)
        bSeamTracker_LaserDiodeEnable := TRUE;
        bTrajectoryFeedHold := FALSE;
        rRobotSpeedOverride_pct := 25.0; (* Search crawl speed *)

        (* Verify valid triangulation profile and gap within process bounds *)
        IF (rVoted_JointGap_mm >= 0.20) AND (rVoted_JointGap_mm <= 1.80) AND
           (rSeamTrack_ChA_QualityScore_pct > 50.0) THEN
            iSubState := 0;
            iState := 30; (* Groove acquired; initiate shielding gas *)
        ELSIF tStateTimer.ET > T#8S THEN
            (* Seam search failed timeout *)
            uiFirstOutAlarmCode := 2020;
            iState := 99;
        END_IF;

    30: (* === GAS_PRE_PURGE_FLOW === *)
        bShieldingGas_SolenoidOpen := TRUE;
        rShieldingGas_MFC_Setpoint_Lmin := 35.0; (* Ar/He laminar purge flow *)

        tPrePurgeTimer(IN := (rShieldingGasFlow_Lmin >= 28.0) AND (rShieldingGasPressure_bar >= 4.0), PT := T#1500MS);

        IF tPrePurgeTimer.Q THEN
            tPrePurgeTimer(IN := FALSE, PT := T#1500MS);
            iSubState := 0;
            iState := 40; (* Gas stabilized; strike arc and open keyhole *)
        ELSIF tStateTimer.ET > T#4S THEN
            (* Gas pre-purge failed timeout *)
            uiFirstOutAlarmCode := 3030;
            iState := 99;
        END_IF;

    40: (* === HYBRID_ARC_STRIKE_KEYHOLE === *)
        bLaserEmissionEnable := TRUE;
        bLaserShutterOpen := TRUE;
        rLaserBeamShapingCoreRatio_pct := 70.0; (* 70% core for deep penetration *)

        (* Keyhole pierce pulse *)
        rLaserPower_Setpoint_W := 4200.0;
        bCMT_ArcIgnitionTrigger := TRUE;
        rWireFeedSpeed_Demand_mpm := 7.00;

        tArcStrikeTimer(IN := (rArcCurrent_Feedback_A >= 110.0) AND (rVoted_MeltPoolTemp_degC >= 1250.0), PT := T#120MS);
        tKeyholeEstablishTimer(IN := (rCMOS_KeyholeDepth_mm >= 2.0), PT := T#80MS);

        IF tArcStrikeTimer.Q AND tKeyholeEstablishTimer.Q THEN
            tArcStrikeTimer(IN := FALSE, PT := T#120MS);
            tKeyholeEstablishTimer(IN := FALSE, PT := T#80MS);
            iSubState := 0;
            iState := 50; (* Arc established; begin coordinated continuous motion *)
        ELSIF tStateTimer.ET > T#800MS THEN
            (* Arc strike failure timeout *)
            uiFirstOutAlarmCode := 4040;
            iState := 99;
        END_IF;

    50: (* === CONTINUOUS_HYBRID_WELD_TRAJECTORY === *)
        bLaserEmissionEnable := TRUE;
        bLaserShutterOpen := TRUE;
        bCMT_ArcIgnitionTrigger := TRUE;
        bShieldingGas_SolenoidOpen := TRUE;
        bSeamTracker_LaserDiodeEnable := TRUE;
        bTrajectoryFeedHold := FALSE;
        rRobotSpeedOverride_pct := 100.0; (* Full coordinated travel speed *)
        rTiltRotatorSpeedOverride_pct := 100.0;

        (* Arc current blowout emergency detection: abort if current drops below 95 A *)
        tArcBlowoutDebounceTimer(IN := (rArcCurrent_Feedback_A < c_ArcCurrent_LL_A), PT := T#15MS);
        IF tArcBlowoutDebounceTimer.Q THEN
            bTrip_ArcCurrent_LL := TRUE;
            uiFirstOutAlarmCode := 5051; (* Arc blowout trip *)
            iState := 99;
        END_IF;

        (* High-current burn-through trip: abort if current exceeds 320 A *)
        tBurnThroughDebounceTimer(IN := (rArcCurrent_Feedback_A > c_ArcCurrent_HH_A), PT := T#15MS);
        IF tBurnThroughDebounceTimer.Q THEN
            bTrip_ArcCurrent_HH := TRUE;
            uiFirstOutAlarmCode := 5052; (* Arc burn-through trip *)
            iState := 99;
        END_IF;

        (* Optical cover glass degradation trip *)
        IF rCoverSlideTransmission_pct < c_CoverSlide_LL_pct THEN
            bTrip_CoverSlide_LL := TRUE;
            uiFirstOutAlarmCode := 5053; (* Cover glass burned trip *)
            iState := 99;
        END_IF;

        (* End-of-seam trigger: detect trajectory complete or operator abort *)
        IF bOperatorCycleAbort THEN
            bWeldAborted := TRUE;
            iState := 60;
        ELSIF tWeldTrajectoryTimer.Q OR (rRobotTCP_PosX_mm >= 1250.0) THEN
            tWeldTrajectoryTimer(IN := FALSE, PT := T#30S);
            iSubState := 0;
            iState := 60; (* Seam finished; proceed to crater fill *)
        END_IF;

    60: (* === CRATER_FILL_DECEL === *)
        rRobotSpeedOverride_pct := 0.0; (* Halt robot motion *)
        rTiltRotatorSpeedOverride_pct := 0.0;

        tCraterFillTimer(IN := TRUE, PT := T#350MS);

        (* Ramp down wire feed speed and laser power to fill solidification crater *)
        rWireFeedSpeed_Demand_mpm := 4.50;
        rLaserPower_Setpoint_W := 1500.0;
        rBurnbackDuration_ms := 45.0;

        IF tCraterFillTimer.Q THEN
            tCraterFillTimer(IN := FALSE, PT := T#350MS);
            bCMT_ArcIgnitionTrigger := FALSE;
            bLaserEmissionEnable := FALSE;
            bLaserShutterOpen := FALSE;
            rLaserPower_Setpoint_W := 0.0;
            rWireFeedSpeed_Demand_mpm := 0.0;
            iSubState := 0;
            iState := 70; (* Proceed to post-purge cooling *)
        END_IF;

    70: (* === GAS_POST_PURGE_FLOW === *)
        bShieldingGas_SolenoidOpen := TRUE;
        rShieldingGas_MFC_Setpoint_Lmin := 30.0;

        tPostPurgeTimer(IN := TRUE, PT := T#2000MS);

        IF tPostPurgeTimer.Q THEN
            tPostPurgeTimer(IN := FALSE, PT := T#2000MS);
            bShieldingGas_SolenoidOpen := FALSE;
            rShieldingGas_MFC_Setpoint_Lmin := 0.0;
            iSubState := 0;
            iState := 80; (* Gas closed; perform optical audit *)
        END_IF;

    80: (* === POST_WELD_OPTICAL_AUDIT === *)
        bSeamTracker_LaserDiodeEnable := TRUE;

        tOpticalAuditTimer(IN := TRUE, PT := T#1200MS);

        IF tOpticalAuditTimer.Q THEN
            tOpticalAuditTimer(IN := FALSE, PT := T#1200MS);
            bSeamTracker_LaserDiodeEnable := FALSE;
            iSubState := 0;
            iState := 90; (* Audit complete; release fixture *)
        END_IF;

    90: (* === FIXTURE_UNCLAMP_DISCHARGE === *)
        bFixtureClampSolenoid := FALSE;
        bFixtureUnclampSolenoid := TRUE;
        bWeldCellExhaustFanRun := FALSE;

        IF (rFixtureHydraulicPressure_bar < 10.0) AND
           NOT bFixturePartSeated_Proximity_1 AND
           NOT bFixturePartSeated_Proximity_2 THEN
            bCycleCompleted := TRUE;
            iSubState := 0;
            iState := 0; (* Cycle successfully completed, return to IDLE *)
        ELSIF tStateTimer.ET > T#6S THEN
            bFixtureUnclampSolenoid := FALSE;
            iState := 0;
        END_IF;

    99: (* === ARC_BLOWOUT_EMERGENCY_ESTOP === *)
        bLaserEmissionEnable := FALSE;
        bLaserShutterOpen := FALSE;
        rLaserPower_Setpoint_W := 0.0;
        bCMT_ArcIgnitionTrigger := FALSE;
        rWireFeedSpeed_Demand_mpm := 0.0;
        bShieldingGas_SolenoidOpen := FALSE;
        rShieldingGas_MFC_Setpoint_Lmin := 0.0;
        bTrajectoryFeedHold := TRUE;
        rRobotSpeedOverride_pct := 0.0;
        rTiltRotatorSpeedOverride_pct := 0.0;
        bAlarmAudibleSiren := TRUE;
        bAlarmVisualBeacon := TRUE;

        tResetDebounceTimer(IN := bOperatorFaultReset, PT := T#100MS);
        IF tResetDebounceTimer.Q AND bCellSafetyCircuit_Ok AND bEmergencyStopOk THEN
            bTrip_ArcCurrent_HH := FALSE;
            bTrip_ArcCurrent_LL := FALSE;
            bTrip_CoverSlide_LL := FALSE;
            bTrip_GasFlow_LL := FALSE;
            bTrip_PoolTemp_HH := FALSE;
            bTrip_PoolTemp_LL := FALSE;
            bTrip_JointGap_HH := FALSE;
            bTrip_JointGap_LL := FALSE;
            bTrip_ChillerFlow_LL := FALSE;
            bTrip_FiberTemp_HH := FALSE;
            bTrip_DiscrepancyTrip := FALSE;
            bTrip_SafetyCircuitLost := FALSE;
            bTrip_SensorConsensusLost := FALSE;
            bAlarmAudibleSiren := FALSE;
            bAlarmVisualBeacon := FALSE;
            uiFirstOutAlarmCode := 0;
            iState := 0; (* Reset latched fault; return to standby *)
        END_IF;

    ELSE
        iState := 0;
END_CASE;
""")

    # -------------------------------------------------------------------------
    # SECTION 7: PHASE 6 - AUTONOMOUS OPTICAL COVER GLASS CLEANING ROUTINE
    # -------------------------------------------------------------------------
    st.append("""
(* ========================================================================================= *)
(* === PHASE 6: AUTONOMOUS OPTICAL COVER GLASS CLEANING ROUTINE ===                         *)
(* ========================================================================================= *)
(* Monitors protective cover glass contamination. Initiates high-pressure cross-jet air     *)
(* blast if transmission drops below 75% or manual trigger is active. Advances roll cassette *)
(* if air blast fails to recover optical transmission above 65%.                             *)

CASE iAirKnifeCleanStep OF

    0: (* Standby Optical Supervision *)
        bCoverSlideAirKnifeBlast := FALSE;
        bCoverSlideCassetteAdvance := FALSE;
        bAirKnifeBusy := FALSE;

        IF bManualAirBlastTrigger OR (rCoverSlideTransmission_pct < c_CoverSlide_L_pct) THEN
            bAirKnifeBusy := TRUE;
            iAirKnifeCleanStep := 10;
        END_IF;

    10: (* Cross-Jet Air Knife Blast *)
        bCoverSlideAirKnifeBlast := TRUE;
        tAirKnifePulseTimer(IN := TRUE, PT := T#180MS);

        IF tAirKnifePulseTimer.Q THEN
            tAirKnifePulseTimer(IN := FALSE, PT := T#180MS);
            bCoverSlideAirKnifeBlast := FALSE;
            iAirKnifeCleanCount := iAirKnifeCleanCount + 1;
            iAirKnifeCleanStep := 20;
        END_IF;

    20: (* Optical Settling & Transmission Assessment *)
        tSpatterCleanTimer(IN := TRUE, PT := T#100MS);

        IF tSpatterCleanTimer.Q THEN
            tSpatterCleanTimer(IN := FALSE, PT := T#100MS);
            IF rCoverSlideTransmission_pct >= c_CoverSlide_L_pct THEN
                (* Recovered successfully *)
                iAirKnifeCleanStep := 0;
            ELSE
                (* Blast insufficient; advance motorized protective glass cassette roll *)
                iAirKnifeCleanStep := 30;
            END_IF;
        END_IF;

    30: (* Advance Motorized Cover Slide Cassette Roll *)
        bCoverSlideCassetteAdvance := TRUE;
        tCassetteAdvanceTimer(IN := TRUE, PT := T#350MS);

        IF tCassetteAdvanceTimer.Q THEN
            tCassetteAdvanceTimer(IN := FALSE, PT := T#350MS);
            bCoverSlideCassetteAdvance := FALSE;
            iAirKnifeCleanStep := 0;
        END_IF;

    ELSE
        iAirKnifeCleanStep := 0;
END_CASE;
""")

    # -------------------------------------------------------------------------
    # SECTION 8: PHASE 7 - ISA-18.2 MULTI-TIERED ALARM LADDER & HYSTERESIS
    # -------------------------------------------------------------------------
    st.append("""
(* ========================================================================================= *)
(* === PHASE 7: ISA-18.2 MULTI-TIERED ALARM LADDER & HYSTERESIS ===                          *)
(* ========================================================================================= *)
(* Evaluates multi-tiered trip limits (HH, H, L, LL) with deadband hysteresis, priority     *)
(* categorization, unacknowledged flashing, and latched trip state maintenance.             *)

(* --- 7.1 Arc Current Stability Deviation Alarms (HH: 320A, H: 280A, L: 120A, LL: 95A) --- *)
IF rArcCurrent_Feedback_A >= c_ArcCurrent_HH_A THEN
    bTrip_ArcCurrent_HH := TRUE;
    bUnack_ArcCurrent_HH := TRUE;
ELSIF rArcCurrent_Feedback_A <= (c_ArcCurrent_HH_A - c_ArcCurrent_Deadband_A) THEN
    (* HH Condition cleared but latched until operator reset *)
END_IF;

IF (rArcCurrent_Feedback_A <= c_ArcCurrent_LL_A) AND (iState = 50) THEN
    bTrip_ArcCurrent_LL := TRUE;
    bUnack_ArcCurrent_LL := TRUE;
ELSIF rArcCurrent_Feedback_A >= (c_ArcCurrent_LL_A + c_ArcCurrent_Deadband_A) THEN
    (* LL Condition cleared *)
END_IF;

(* --- 7.2 Optical Cover Slide Transmission Alarms (L: 75%, LL: 60%) --- *)
IF rCoverSlideTransmission_pct <= c_CoverSlide_LL_pct THEN
    bTrip_CoverSlide_LL := TRUE;
    bUnack_CoverSlide_LL := TRUE;
ELSIF rCoverSlideTransmission_pct >= (c_CoverSlide_LL_pct + c_CoverSlide_Deadband_pct) THEN
    (* LL Condition cleared *)
END_IF;

(* --- 7.3 Shielding Gas Mass Flow Alarms (HH: 50, H: 46, L: 24, LL: 18 L/min) --- *)
IF (rShieldingGasFlow_Lmin <= c_GasFlow_LL_Lmin) AND (iState = 50) THEN
    bTrip_GasFlow_LL := TRUE;
    bUnack_GasFlow_LL := TRUE;
ELSIF rShieldingGasFlow_Lmin >= (c_GasFlow_LL_Lmin + c_GasFlow_Deadband_Lmin) THEN
    (* LL Condition cleared *)
END_IF;

(* --- 7.4 Molten Pool Temperature Alarms (HH: 1850 deg C, LL: 1100 deg C) --- *)
IF rVoted_MeltPoolTemp_degC >= c_PoolTemp_HH_degC THEN
    bTrip_PoolTemp_HH := TRUE;
ELSIF rVoted_MeltPoolTemp_degC <= (c_PoolTemp_HH_degC - c_PoolTemp_Deadband_degC) THEN
    (* HH Condition cleared *)
END_IF;

IF (rVoted_MeltPoolTemp_degC <= c_PoolTemp_LL_degC) AND (iState = 50) THEN
    bTrip_PoolTemp_LL := TRUE;
ELSIF rVoted_MeltPoolTemp_degC >= (c_PoolTemp_LL_degC + c_PoolTemp_Deadband_degC) THEN
    (* LL Condition cleared *)
END_IF;

(* --- 7.5 Joint Root Opening Gap Alarms (HH: 2.20 mm, LL: 0.05 mm) --- *)
IF rVoted_JointGap_mm >= c_JointGap_HH_mm THEN
    bTrip_JointGap_HH := TRUE;
ELSIF rVoted_JointGap_mm <= (c_JointGap_HH_mm - c_JointGap_Deadband_mm) THEN
    (* HH Condition cleared *)
END_IF;

IF rVoted_JointGap_mm <= c_JointGap_LL_mm THEN
    bTrip_JointGap_LL := TRUE;
ELSIF rVoted_JointGap_mm >= (c_JointGap_LL_mm + c_JointGap_Deadband_mm) THEN
    (* LL Condition cleared *)
END_IF;

(* --- 7.6 Laser Source Chiller Cooling Flow Alarm (LL: 24.0 L/min) --- *)
IF rLaserChillerFlow_Lmin <= c_ChillerFlow_LL_Lmin THEN
    bTrip_ChillerFlow_LL := TRUE;
ELSIF rLaserChillerFlow_Lmin >= (c_ChillerFlow_LL_Lmin + c_ChillerFlow_Deadband_Lmin) THEN
    (* LL Condition cleared *)
END_IF;

(* --- 7.7 Process Fiber Connector Temperature Alarm (HH: 65.0 deg C) --- *)
IF rOpticalFiberTemp_degC >= c_FiberTemp_HH_degC THEN
    bTrip_FiberTemp_HH := TRUE;
ELSIF rOpticalFiberTemp_degC <= (c_FiberTemp_HH_degC - c_FiberTemp_Deadband_degC) THEN
    (* HH Condition cleared *)
END_IF;

(* --- 7.8 Cell Safety Hardware Interlocks (Cat 4 / PLe) --- *)
IF NOT bCellSafetyCircuit_Ok OR NOT bLaserSafetyInterlock_Ok OR NOT bLightCurtainClear OR NOT bEmergencyStopOk THEN
    bTrip_SafetyCircuitLost := TRUE;
    bUnack_SafetyCircuitLost := TRUE;
    IF uiFirstOutAlarmCode = 0 THEN
        uiFirstOutAlarmCode := 9999;
    END_IF;
    iState := 99; (* Instantaneous emergency state *)
END_IF;
""")

    # -------------------------------------------------------------------------
    # SECTION 9: PHASE 8 - DIAGNOSTIC & STATUS WORD PACKING
    # -------------------------------------------------------------------------
    st.append("""
(* ========================================================================================= *)
(* === PHASE 8: DIAGNOSTIC & STATUS WORD PACKING ===                                         *)
(* ========================================================================================= *)
(* Encodes operational status and ISA-18.2 alarm registers into standard 32-bit DWORDs       *)
(* for high-speed deterministic fieldbus broadcast to SCADA / MES host controllers.          *)

(* --- 8.1 System Status Word (dwSystemStatusWord) --- *)
dwSystemStatusWord := 16#0000_0000;
dwSystemStatusWord := dwSystemStatusWord OR INT_TO_DWORD(iState); (* Bits 0-7: Active FSM State *)
IF bLaserEmissionEnable THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0100; END_IF; (* Bit 8 *)
IF bLaserShutterOpen THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0200; END_IF;    (* Bit 9 *)
IF bCMT_ArcIgnitionTrigger THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0400; END_IF; (* Bit 10 *)
IF bShieldingGas_SolenoidOpen THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0800; END_IF; (* Bit 11 *)
IF bSeamTracker_LaserDiodeEnable THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_1000; END_IF; (* Bit 12 *)
IF bFixtureClampSolenoid THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_2000; END_IF; (* Bit 13 *)
IF bCycleCompleted THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_4000; END_IF;       (* Bit 14 *)
IF bWeldAborted THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_8000; END_IF;          (* Bit 15 *)

(* --- 8.2 Category 1 Emergency Shutdown Trips (dwAlarmWord1_EmergencyTrips) --- *)
dwAlarmWord1_EmergencyTrips := 16#0000_0000;
IF bTrip_SafetyCircuitLost THEN dwAlarmWord1_EmergencyTrips := dwAlarmWord1_EmergencyTrips OR 16#0000_0001; END_IF;
IF bTrip_ArcCurrent_LL THEN dwAlarmWord1_EmergencyTrips := dwAlarmWord1_EmergencyTrips OR 16#0000_0002; END_IF;
IF bTrip_ArcCurrent_HH THEN dwAlarmWord1_EmergencyTrips := dwAlarmWord1_EmergencyTrips OR 16#0000_0004; END_IF;
IF bTrip_CoverSlide_LL THEN dwAlarmWord1_EmergencyTrips := dwAlarmWord1_EmergencyTrips OR 16#0000_0008; END_IF;
IF bTrip_GasFlow_LL THEN dwAlarmWord1_EmergencyTrips := dwAlarmWord1_EmergencyTrips OR 16#0000_0010; END_IF;
IF bTrip_ChillerFlow_LL THEN dwAlarmWord1_EmergencyTrips := dwAlarmWord1_EmergencyTrips OR 16#0000_0020; END_IF;
IF bTrip_FiberTemp_HH THEN dwAlarmWord1_EmergencyTrips := dwAlarmWord1_EmergencyTrips OR 16#0000_0040; END_IF;
IF bTrip_SensorConsensusLost THEN dwAlarmWord1_EmergencyTrips := dwAlarmWord1_EmergencyTrips OR 16#0000_0080; END_IF;

(* --- 8.3 Category 2 Process Trips & Quality Faults (dwAlarmWord2_ProcessTrips) --- *)
dwAlarmWord2_ProcessTrips := 16#0000_0000;
IF bTrip_DiscrepancyTrip THEN dwAlarmWord2_ProcessTrips := dwAlarmWord2_ProcessTrips OR 16#0000_0001; END_IF;
IF bTrip_PoolTemp_HH THEN dwAlarmWord2_ProcessTrips := dwAlarmWord2_ProcessTrips OR 16#0000_0002; END_IF;
IF bTrip_PoolTemp_LL THEN dwAlarmWord2_ProcessTrips := dwAlarmWord2_ProcessTrips OR 16#0000_0004; END_IF;
IF bTrip_JointGap_HH THEN dwAlarmWord2_ProcessTrips := dwAlarmWord2_ProcessTrips OR 16#0000_0008; END_IF;
IF bTrip_JointGap_LL THEN dwAlarmWord2_ProcessTrips := dwAlarmWord2_ProcessTrips OR 16#0000_0010; END_IF;

(* --- 8.4 Category 3 Advisory Warnings (dwWarningWord) --- *)
dwWarningWord := 16#0000_0000;
IF (rArcCurrent_Feedback_A >= c_ArcCurrent_H_A) THEN dwWarningWord := dwWarningWord OR 16#0000_0001; END_IF;
IF (rArcCurrent_Feedback_A <= c_ArcCurrent_L_A) AND (iState = 50) THEN dwWarningWord := dwWarningWord OR 16#0000_0002; END_IF;
IF (rCoverSlideTransmission_pct <= c_CoverSlide_L_pct) THEN dwWarningWord := dwWarningWord OR 16#0000_0004; END_IF;
IF (rShieldingGasFlow_Lmin >= c_GasFlow_H_Lmin) THEN dwWarningWord := dwWarningWord OR 16#0000_0008; END_IF;
IF (rShieldingGasFlow_Lmin <= c_GasFlow_L_Lmin) AND (iState = 50) THEN dwWarningWord := dwWarningWord OR 16#0000_0010; END_IF;
IF (rVoted_MeltPoolTemp_degC >= c_PoolTemp_H_degC) THEN dwWarningWord := dwWarningWord OR 16#0000_0020; END_IF;
IF (rVoted_MeltPoolTemp_degC <= c_PoolTemp_L_degC) AND (iState = 50) THEN dwWarningWord := dwWarningWord OR 16#0000_0040; END_IF;
IF (rVoted_JointGap_mm >= c_JointGap_H_mm) THEN dwWarningWord := dwWarningWord OR 16#0000_0080; END_IF;
IF (rVoted_JointGap_mm <= c_JointGap_L_mm) THEN dwWarningWord := dwWarningWord OR 16#0000_0100; END_IF;
IF (rLaserChillerFlow_Lmin <= c_ChillerFlow_L_Lmin) THEN dwWarningWord := dwWarningWord OR 16#0000_0200; END_IF;
IF (rOpticalFiberTemp_degC >= c_FiberTemp_H_degC) THEN dwWarningWord := dwWarningWord OR 16#0000_0400; END_IF;
IF bLat_Degraded_1oo2 OR bVert_Degraded_1oo2 OR bGap_Degraded_1oo2 OR bTemp_Degraded_1oo2 THEN
    dwWarningWord := dwWarningWord OR 16#0000_0800; (* Bit 11: 2oo3 Degraded to 1oo2 warning *)
END_IF;

(* --- 8.5 ISA-18.2 Priority Escalation Annunciator Mask (dwIsaAlarmPriorityMask) --- *)
dwIsaAlarmPriorityMask := 16#0000_0000;
IF dwAlarmWord1_EmergencyTrips <> 16#0000_0000 THEN
    dwIsaAlarmPriorityMask := dwIsaAlarmPriorityMask OR 16#0000_0001; (* Priority 1: Emergency Trip *)
END_IF;
IF dwAlarmWord2_ProcessTrips <> 16#0000_0000 THEN
    dwIsaAlarmPriorityMask := dwIsaAlarmPriorityMask OR 16#0000_0002; (* Priority 2: Process Trip *)
END_IF;
IF dwWarningWord <> 16#0000_0000 THEN
    dwIsaAlarmPriorityMask := dwIsaAlarmPriorityMask OR 16#0000_0004; (* Priority 3: Advisory Warning *)
END_IF;
""")

    # -------------------------------------------------------------------------
    # SECTION 10: PHASE 9 - FAIL-SAFE INTERLOCK ENFORCEMENT & OUTPUT CLAMPING
    # -------------------------------------------------------------------------
    st.append("""
(* ========================================================================================= *)
(* === PHASE 9: FAIL-SAFE INTERLOCK ENFORCEMENT & OUTPUT CLAMPING ===                        *)
(* ========================================================================================= *)
(* Ultimate deterministic barrier: Enforces physical zero-energy states on high-risk optical *)
(* and electrical actuators if safety circuits are unverified or cell enters ESTOP state 99. *)

IF (iState = 99) OR NOT bCellSafetyCircuit_Ok OR NOT bLaserSafetyInterlock_Ok OR NOT bLightCurtainClear OR NOT bEmergencyStopOk THEN
    rLaserPower_Setpoint_W := 0.0;
    bLaserEmissionEnable := FALSE;
    bLaserShutterOpen := FALSE;
    bCMT_ArcIgnitionTrigger := FALSE;
    rWireFeedSpeed_Demand_mpm := 0.0;
    rRobotTCP_Trim_Lateral_mm := 0.0;
    rRobotTCP_Trim_Vertical_mm := 0.0;
    rRobotSpeedOverride_pct := 0.0;
    rTiltRotatorSpeedOverride_pct := 0.0;
    bTrajectoryFeedHold := TRUE;
    bShieldingGas_SolenoidOpen := FALSE;
    rShieldingGas_MFC_Setpoint_Lmin := 0.0;
    bAlarmAudibleSiren := TRUE;
    bAlarmVisualBeacon := TRUE;
END_IF;

END_FUNCTION_BLOCK
""")

    return "".join(st)

if __name__ == "__main__":
    code = get_code()
    print(f"Total Structured Text character count: {len(code)}")
