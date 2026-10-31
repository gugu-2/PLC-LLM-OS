def get_var_internal():
    return """VAR
    (* ============================================================================================= *)
    (* FIRST-SCAN INITIALIZATION & DETERMINISTIC EXECUTION SCHEDULER                                 *)
    (* ============================================================================================= *)
    bFirstScanDone              : BOOL := FALSE;    (* Memory initialization latch for matrices & tables *)
    lrCycleDeltaT_s             : LREAL := 0.002;   (* Nominal cyclic task cycle interval [s] (2.0 ms) *)
    diScanCounter               : DINT := 0;        (* Cyclic tick counter for scheduling & telemetry *)

    (* ============================================================================================= *)
    (* DISCRETE STATE-SPACE MODEL MATRICES (16 STATES, 8 CONTROL INPUTS)                             *)
    (* ============================================================================================= *)
    arrA                        : ARRAY[1..16, 1..16] OF LREAL; (* State transition matrix A (16x16) *)
    arrB                        : ARRAY[1..16, 1..8] OF LREAL;  (* Input coupling matrix B (16x8) *)
    arrC                        : ARRAY[1..16, 1..16] OF LREAL; (* Output measurement matrix C (16x16) *)
    arrD                        : ARRAY[1..16, 1..8] OF LREAL;  (* Direct feedthrough matrix D (16x8) *)
    arrX                        : ARRAY[1..16] OF LREAL;        (* Current state vector x[k] *)
    arrX_Next                   : ARRAY[1..16] OF LREAL;        (* Predicted state vector x[k+1] *)
    arrU                        : ARRAY[1..8] OF LREAL;         (* Control input action vector u[k] *)
    arrY                        : ARRAY[1..16] OF LREAL;        (* Measured system output vector y[k] *)
    arrRef                      : ARRAY[1..16] OF LREAL;        (* State reference setpoint vector *)

    (* ============================================================================================= *)
    (* MODEL PREDICTIVE CONTROL (MPC) QUADRATIC COST WEIGHTING MATRICES                              *)
    (* ============================================================================================= *)
    arrQ                        : ARRAY[1..16, 1..16] OF LREAL; (* State deviation penalty matrix Q *)
    arrR                        : ARRAY[1..8, 1..8] OF LREAL;   (* Control effort penalty matrix R *)
    arrP                        : ARRAY[1..16, 1..16] OF LREAL; (* Terminal state Riccati penalty matrix P *)
    lrMPC_Cost_J                : LREAL := 0.0;                 (* Instantaneous MPC quadratic cost accumulator *)

    (* ============================================================================================= *)
    (* DELTA ROBOT PARALLEL KINEMATICS STRUCTURAL GEOMETRIC CONSTANTS                                *)
    (* ============================================================================================= *)
    lrBaseRadius_Rb             : LREAL := 380.0;   (* Base plate center to motor rotational axis radius [mm] *)
    lrToolRadius_Re             : LREAL := 65.0;    (* Moving tool platform center to ball-joint radius [mm] *)
    lrUpperArm_L1               : LREAL := 400.0;   (* Active upper bicep link mechanical length [mm] *)
    lrLowerArm_L2               : LREAL := 900.0;   (* Passive carbon-fiber forearm parallelogram length [mm] *)

    (* Longitudinal cell reference coordinates of Delta Robot base centers along infeed conveyor *)
    lrBase_X_R1                 : LREAL := 1000.0;  (* Delta Robot 1 mounting base longitudinal coordinate [mm] *)
    lrBase_X_R2                 : LREAL := 2200.0;  (* Delta Robot 2 mounting base longitudinal coordinate [mm] *)
    lrBase_X_R3                 : LREAL := 3400.0;  (* Delta Robot 3 mounting base longitudinal coordinate [mm] *)
    lrBase_X_R4                 : LREAL := 4600.0;  (* Delta Robot 4 mounting base longitudinal coordinate [mm] *)
    lrBase_Y_All                : LREAL := 0.0;     (* Lateral transverse mounting center across conveyor [mm] *)
    lrBase_Z_All                : LREAL := 850.0;   (* Vertical elevation height above infeed belt datum [mm] *)

    (* Kinematic workspace operating boundary & mutual exclusion collision limits *)
    lrR_Work_Radius             : LREAL := 750.0;   (* Maximum reachable horizontal Cartesian radius [mm] *)
    lrZ_Pick_Level              : LREAL := -740.0;  (* Tool TCP pick plane relative to base overhead datum [mm] *)
    lrZ_Place_Level             : LREAL := -680.0;  (* Tool TCP place plane inside secondary carton [mm] *)
    lrZ_Fly_Clearance           : LREAL := -520.0;  (* Elevated transit altitude over conveyor guides [mm] *)

    (* Work-envelope overlap zones & mutual exclusion tokens *)
    iToken_Zone_R1_R2           : INT := 0;         (* Overlap zone 1-2 token: 0=Free, 1=Owned R1, 2=Owned R2 *)
    iToken_Zone_R2_R3           : INT := 0;         (* Overlap zone 2-3 token: 0=Free, 2=Owned R2, 3=Owned R3 *)
    iToken_Zone_R3_R4           : INT := 0;         (* Overlap zone 3-4 token: 0=Free, 3=Owned R3, 4=Owned R4 *)

    (* ============================================================================================= *)
    (* IN-LINE HIGH-SPEED VISION 64-PACKAGE CIRCULAR TRACKING FIFO QUEUE                             *)
    (* ============================================================================================= *)
    arrPkg_ID                   : ARRAY[1..64] OF DINT;     (* Serialized tracking index of package in FIFO *)
    arrPkg_X_Entry              : ARRAY[1..64] OF LREAL;    (* Absolute conveyor X coordinate at camera line-scan [mm] *)
    arrPkg_Y_Entry              : ARRAY[1..64] OF LREAL;    (* Transverse lateral offset across conveyor belt [mm] *)
    arrPkg_Theta_Entry          : ARRAY[1..64] OF LREAL;    (* Package skew angle measured by 3D camera [deg] *)
    arrPkg_EncSnapshot          : ARRAY[1..64] OF DINT;     (* Belt encoder count at camera optical trigger [pulses] *)
    arrPkg_State                : ARRAY[1..64] OF INT;      (* 0=Empty, 1=Queued, 2=Assigned_R1, 3=R2, 4=R3, 5=R4, 6=Picked, 7=Placed, 8=Rejected, 9=Escaped *)
    arrPkg_Defect               : ARRAY[1..64] OF BOOL;     (* Seal leak, skew, or dimension out-of-tolerance *)
    arrPkg_AssignedRobot        : ARRAY[1..64] OF INT;      (* Designated robot index [1..4] *)
    iQueueHead                  : INT := 1;                 (* Ingestion pointer for incoming vision packets *)
    iQueueTail                  : INT := 1;                 (* Egress pointer for expired/completed tracking entries *)
    iQueueCount                 : INT := 0;                 (* Current active package count inside FIFO *)

    (* ============================================================================================= *)
    (* SECONDARY CARTON 4x6 (24-UNIT) COLLATION PACK PATTERN GRID                                    *)
    (* ============================================================================================= *)
    arrCaseGrid_Occupied        : ARRAY[1..4, 1..6] OF BOOL;(* 4 rows x 6 columns pack pocket occupancy grid *)
    iCaseCurrentUnits           : INT := 0;                 (* Current successfully placed units in active carton *)
    iCaseTargetUnits            : INT := 24;                (* Target unit capacity per RSC carton (4x6 array) *)
    lrCartonOriginX             : LREAL := 800.0;           (* Upstream carton corner datum along secondary chain [mm] *)
    lrCartonOriginY             : LREAL := 550.0;           (* Lateral transverse center of secondary chain [mm] *)
    lrCartonOriginZ             : LREAL := -120.0;          (* Bottom floor of corrugated box relative to belt datum [mm] *)
    bCartonFullReadyToDischarge : BOOL := FALSE;            (* Carton collation complete trigger flag *)

    (* ============================================================================================= *)
    (* 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) VOTING & FAULT ARBITRATION ENGINES                       *)
    (* ============================================================================================= *)
    (* Infeed Conveyor Encoders *)
    diVoted_InfeedBelt_Pos      : DINT := 0;        (* Voted infeed conveyor absolute encoder position [pulses] *)
    lrVoted_InfeedBelt_Speed    : LREAL := 0.0;     (* Voted infeed belt linear speed [mm/s] *)
    lrPrev_InfeedBelt_Pos_mm    : LREAL := 0.0;     (* Previous scan belt position for velocity derivation [mm] *)
    bInfeedEnc_Healthy_A        : BOOL := TRUE;
    bInfeedEnc_Healthy_B        : BOOL := TRUE;
    bInfeedEnc_Healthy_C        : BOOL := TRUE;
    iInfeedEnc_DiscrepancyTimer : INT := 0;         (* Debounce counter for infeed encoder discrepancy [ticks] *)

    (* Secondary Carton Lug Chain Encoders *)
    diVoted_Carton_Pos          : DINT := 0;        (* Voted carton lug chain position [pulses] *)
    lrVoted_Carton_Speed        : LREAL := 0.0;     (* Voted carton conveyor speed [mm/s] *)
    lrPrev_Carton_Pos_mm        : LREAL := 0.0;
    bCartonEnc_Healthy_A        : BOOL := TRUE;
    bCartonEnc_Healthy_B        : BOOL := TRUE;
    bCartonEnc_Healthy_C        : BOOL := TRUE;
    iCartonEnc_DiscrepancyTimer : INT := 0;

    (* Vacuum Transducers (R1, R2, R3, R4) *)
    lrVoted_R1_Vac_kPa          : LREAL := 0.0;
    lrVoted_R2_Vac_kPa          : LREAL := 0.0;
    lrVoted_R3_Vac_kPa          : LREAL := 0.0;
    lrVoted_R4_Vac_kPa          : LREAL := 0.0;
    bR1_VacHealthy_A            : BOOL := TRUE; bR1_VacHealthy_B : BOOL := TRUE; bR1_VacHealthy_C : BOOL := TRUE;
    bR2_VacHealthy_A            : BOOL := TRUE; bR2_VacHealthy_B : BOOL := TRUE; bR2_VacHealthy_C : BOOL := TRUE;
    bR3_VacHealthy_A            : BOOL := TRUE; bR3_VacHealthy_B : BOOL := TRUE; bR3_VacHealthy_C : BOOL := TRUE;
    bR4_VacHealthy_A            : BOOL := TRUE; bR4_VacHealthy_B : BOOL := TRUE; bR4_VacHealthy_C : BOOL := TRUE;

    (* ============================================================================================= *)
    (* RECEDING-HORIZON 5th-ORDER S-CURVE TRAJECTORY ENGINE VARIABLES                                *)
    (* ============================================================================================= *)
    (* Delta Robot 1 Trajectory Registers *)
    iR1_Phase                   : INT := 0;         (* Trajectory phase: 0=Idle, 1=Approach, 2=Sync, 3=Grip, 4=Lift, 5=Fly, 6=Descend, 7=BlowOff, 8=Ascend *)
    lrR1_PhaseElapsed_s         : LREAL := 0.0;
    lrR1_PhaseDuration_s        : LREAL := 0.100;
    lrR1_P0_X : LREAL := 0.0; lrR1_P0_Y : LREAL := 0.0; lrR1_P0_Z : LREAL := -520.0; lrR1_P0_Theta : LREAL := 0.0;
    lrR1_P1_X : LREAL := 0.0; lrR1_P1_Y : LREAL := 0.0; lrR1_P1_Z : LREAL := -740.0; lrR1_P1_Theta : LREAL := 0.0;
    lrR1_TCP_X : LREAL := 0.0; lrR1_TCP_Y : LREAL := 0.0; lrR1_TCP_Z : LREAL := -520.0; lrR1_TCP_Theta : LREAL := 0.0;
    lrR1_TCP_Vx : LREAL := 0.0; lrR1_TCP_Vy : LREAL := 0.0; lrR1_TCP_Vz : LREAL := 0.0;

    (* Delta Robot 2 Trajectory Registers *)
    iR2_Phase                   : INT := 0;
    lrR2_PhaseElapsed_s         : LREAL := 0.0;
    lrR2_PhaseDuration_s        : LREAL := 0.100;
    lrR2_P0_X : LREAL := 0.0; lrR2_P0_Y : LREAL := 0.0; lrR2_P0_Z : LREAL := -520.0; lrR2_P0_Theta : LREAL := 0.0;
    lrR2_P1_X : LREAL := 0.0; lrR2_P1_Y : LREAL := 0.0; lrR2_P1_Z : LREAL := -740.0; lrR2_P1_Theta : LREAL := 0.0;
    lrR2_TCP_X : LREAL := 0.0; lrR2_TCP_Y : LREAL := 0.0; lrR2_TCP_Z : LREAL := -520.0; lrR2_TCP_Theta : LREAL := 0.0;
    lrR2_TCP_Vx : LREAL := 0.0; lrR2_TCP_Vy : LREAL := 0.0; lrR2_TCP_Vz : LREAL := 0.0;

    (* Delta Robot 3 Trajectory Registers *)
    iR3_Phase                   : INT := 0;
    lrR3_PhaseElapsed_s         : LREAL := 0.0;
    lrR3_PhaseDuration_s        : LREAL := 0.100;
    lrR3_P0_X : LREAL := 0.0; lrR3_P0_Y : LREAL := 0.0; lrR3_P0_Z : LREAL := -520.0; lrR3_P0_Theta : LREAL := 0.0;
    lrR3_P1_X : LREAL := 0.0; lrR3_P1_Y : LREAL := 0.0; lrR3_P1_Z : LREAL := -740.0; lrR3_P1_Theta : LREAL := 0.0;
    lrR3_TCP_X : LREAL := 0.0; lrR3_TCP_Y : LREAL := 0.0; lrR3_TCP_Z : LREAL := -520.0; lrR3_TCP_Theta : LREAL := 0.0;
    lrR3_TCP_Vx : LREAL := 0.0; lrR3_TCP_Vy : LREAL := 0.0; lrR3_TCP_Vz : LREAL := 0.0;

    (* Delta Robot 4 Trajectory Registers *)
    iR4_Phase                   : INT := 0;
    lrR4_PhaseElapsed_s         : LREAL := 0.0;
    lrR4_PhaseDuration_s        : LREAL := 0.100;
    lrR4_P0_X : LREAL := 0.0; lrR4_P0_Y : LREAL := 0.0; lrR4_P0_Z : LREAL := -520.0; lrR4_P0_Theta : LREAL := 0.0;
    lrR4_P1_X : LREAL := 0.0; lrR4_P1_Y : LREAL := 0.0; lrR4_P1_Z : LREAL := -740.0; lrR4_P1_Theta : LREAL := 0.0;
    lrR4_TCP_X : LREAL := 0.0; lrR4_TCP_Y : LREAL := 0.0; lrR4_TCP_Z : LREAL := -520.0; lrR4_TCP_Theta : LREAL := 0.0;
    lrR4_TCP_Vx : LREAL := 0.0; lrR4_TCP_Vy : LREAL := 0.0; lrR4_TCP_Vz : LREAL := 0.0;

    (* Trajectory intermediate polynomial evaluation terms *)
    lrTau : LREAL := 0.0;
    lrPoly_s : LREAL := 0.0;
    lrPoly_s_dot : LREAL := 0.0;
    lrPoly_s_ddot : LREAL := 0.0;

    (* Intermediate delta inverse kinematics variables *)
    lrRotX : LREAL; lrRotY : LREAL; lrRotZ : LREAL;
    lrY_Shifted : LREAL;
    lrCoeff_E : LREAL; lrCoeff_F : LREAL; lrCoeff_G : LREAL;
    lrDiscriminant : LREAL;
    lrHalfTan_t : LREAL;
    lrSolvedTheta_deg : LREAL;

    (* Loop index iterators *)
    iIdx : INT;
    jIdx : INT;
    kIdx : INT;
    mIdx : INT;
    nIdx : INT;

    (* ISA-18.2 Alarm Deadbands, Setpoints & Latches *)
    lrAlarm_BeltSpeed_HH        : LREAL := 1400.0;  (* Belt overspeed trip setpoint [mm/s] *)
    lrAlarm_BeltSpeed_H         : LREAL := 1280.0;  (* Belt overspeed warning setpoint [mm/s] *)
    lrAlarm_BeltSpeed_L         : LREAL := 400.0;   (* Belt underspeed warning setpoint [mm/s] *)
    lrAlarm_BeltSpeed_LL        : LREAL := 250.0;   (* Belt stall critical trip setpoint [mm/s] *)
    lrAlarm_BeltSpeed_Deadband  : LREAL := 15.0;    (* Hysteresis deadband [mm/s] *)

    lrAlarm_VacuumGrip_HH       : LREAL := -85.0;   (* Excessive vacuum transducer spike [kPa] *)
    lrAlarm_VacuumGrip_L        : LREAL := -62.0;   (* Vacuum grip drop warning threshold [kPa] *)
    lrAlarm_VacuumGrip_LL       : LREAL := -45.0;   (* Vacuum grip failure / dropped package trip [kPa] *)
    lrAlarm_Vacuum_Deadband     : LREAL := 3.0;     (* Vacuum hysteresis deadband [kPa] *)

    lrAlarm_AirPressure_LL      : LREAL := 4.8;     (* Main air header minimum pressure trip [bar] *)
    lrAlarm_AirPressure_L       : LREAL := 5.4;     (* Main air header low warning [bar] *)

    lrAlarm_ServoLag_HH         : LREAL := 8.5;     (* Maximum allowable servo joint lag angle trip [deg] *)
    lrAlarm_ServoLag_H          : LREAL := 4.5;     (* Servo joint lag warning threshold [deg] *)

    (* Alarm Delay & Timer Counters *)
    iTimer_BeltStall            : INT := 0;
    iTimer_VacLoss_R1           : INT := 0;
    iTimer_VacLoss_R2           : INT := 0;
    iTimer_VacLoss_R3           : INT := 0;
    iTimer_VacLoss_R4           : INT := 0;
    iTimer_AirLow               : INT := 0;
    iTimer_CartonJam            : INT := 0;
    iTimer_QueueFull            : INT := 0;
END_VAR
"""
