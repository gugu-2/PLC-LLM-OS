# Packaging Robotic Palletizer & Stretch Hooder ST Generator
import os

def build_packaging_block():
    sections = []

    # ==========================================
    # SECTION 1: HEADER & INTERFACE DECLARATION
    # ==========================================
    sec1 = """FUNCTION_BLOCK FB_Packaging_RoboticPalletizer_StretchHooder
VAR_INPUT
    (* --- 2oo3 TMR Gripper Vacuum Transducers [mbar] --- *)
    rVacPress_ChA_mbar          : REAL := -750.0; (* Vacuum transducer channel A [-1000..0 mbar] *)
    rVacPress_ChB_mbar          : REAL := -750.0; (* Vacuum transducer channel B [-1000..0 mbar] *)
    rVacPress_ChC_mbar          : REAL := -750.0; (* Vacuum transducer channel C [-1000..0 mbar] *)
    
    (* --- Infeed Carton Collation Table Photocell Array --- *)
    bCartonInfeed_SensA         : BOOL := FALSE;  (* Infeed collation photocell lane A *)
    bCartonInfeed_SensB         : BOOL := FALSE;  (* Infeed collation photocell lane B *)
    bCartonInfeed_SensC         : BOOL := FALSE;  (* Infeed collation photocell lane C *)
    rCartonWeight_kg            : REAL := 12.5;   (* Inline checkweigher carton weight [kg] *)
    rCartonLength_mm            : REAL := 400.0;  (* Carton physical length [mm] *)
    rCartonWidth_mm             : REAL := 300.0;  (* Carton physical width [mm] *)
    rCartonHeight_mm            : REAL := 250.0;  (* Carton physical height [mm] *)
    
    (* --- 4-Axis Articulated Robot Kinematics Feedback --- *)
    rRobot_TCP_PosX_mm          : REAL := 0.0;    (* Robot Tool Center Point X coordinate [mm] *)
    rRobot_TCP_PosY_mm          : REAL := 0.0;    (* Robot Tool Center Point Y coordinate [mm] *)
    rRobot_TCP_PosZ_mm          : REAL := 800.0;  (* Robot Tool Center Point Z coordinate [mm] *)
    rRobot_TCP_RotYaw_deg       : REAL := 0.0;    (* Robot gripper rotation angle Yaw [deg] *)
    rRobot_TCP_Vel_mms          : REAL := 0.0;    (* Robot Tool Center Point linear velocity [mm/s] *)
    rRobot_J1_Torque_Nm         : REAL := 0.0;    (* Robot Axis 1 joint motor torque [Nm] *)
    rRobot_J2_Torque_Nm         : REAL := 0.0;    (* Robot Axis 2 joint motor torque [Nm] *)
    bRobot_InMotion             : BOOL := FALSE;  (* Robot arm trajectory interpolation busy flag *)
    bRobot_TargetReached        : BOOL := FALSE;  (* Robot arm waypoint target achieved *)
    
    (* --- 3D ToF Pallet Stack Geometry Profiler --- *)
    rStack_MeasuredHeight_mm    : REAL := 0.0;    (* Laser/ToF stack height profile [mm] *)
    rStack_TiltAnglePitch_deg   : REAL := 0.0;    (* Pallet stack longitudinal tilt angle [deg] *)
    rStack_TiltAngleRoll_deg    : REAL := 0.0;    (* Pallet stack transverse tilt angle [deg] *)
    rStack_SurfacePlanarity_mm  : REAL := 0.0;    (* Top layer surface planarity variance [mm] *)
    
    (* --- 2oo3 TMR Stretch Hood Corner Film Tension Load Cells [N] --- *)
    rFilmTension_ChA_N          : REAL := 150.0;  (* Corner 1 tension load cell Channel A [N] *)
    rFilmTension_ChB_N          : REAL := 150.0;  (* Corner 2 tension load cell Channel B [N] *)
    rFilmTension_ChC_N          : REAL := 150.0;  (* Corner 3 tension load cell Channel C [N] *)
    rFilmRoll_RemainingDia_mm   : REAL := 600.0;  (* Tubular stretch hood roll remaining outer diameter [mm] *)
    rFilm_Thickness_um          : REAL := 80.0;   (* Polyethylene tubular film nominal gauge [um] *)
    
    (* --- Stretch Hood Carriage & Fingers Kinematics --- *)
    rHood_CarriageHeight_mm     : REAL := 2800.0; (* Hooder vertical elevator carriage position [mm] *)
    rHood_CarriageVel_mms       : REAL := 0.0;    (* Hooder vertical elevator carriage speed [mm/s] *)
    rFinger_ExpandSpanX_mm      : REAL := 800.0;  (* 4-corner expansion finger transverse span X [mm] *)
    rFinger_ExpandSpanY_mm      : REAL := 1000.0; (* 4-corner expansion finger longitudinal span Y [mm] *)
    
    (* --- Pallet Turntable & Transfer Conveyor --- *)
    rTurntable_RotAngle_deg     : REAL := 0.0;    (* Pallet turntable angular position [deg] *)
    rTurntable_RotSpeed_rpm     : REAL := 0.0;    (* Pallet turntable rotational velocity [rpm] *)
    bPalletInTurntable_PE       : BOOL := TRUE;   (* Pallet present on turntable optical photoeye *)
    bPalletOutfeedClear_PE      : BOOL := TRUE;   (* Pallet outfeed discharge roller clear *)
    
    (* --- System Supervisory & Safety Inputs --- *)
    bAutoMode_Cmd               : BOOL := TRUE;   (* Automatic continuous cycle command *)
    bSafetyCurtain_Clear        : BOOL := TRUE;   (* Category 4 / PLe Safety light curtain muted/clear *)
    bEmergencyStop_Active       : BOOL := FALSE;  (* Dual-channel hardware E-stop active (active low inverted) *)
    bAlarmReset_PB              : BOOL := FALSE;  (* HMI / local pushbutton alarm acknowledge *)
    rCycleTime_Target_s         : REAL := 45.0;   (* Target production cycle time per finished pallet [s] *)
    tScanTime_s                 : REAL := 0.010;  (* Deterministic PLC task scan interval [s] *)
END_VAR

VAR_OUTPUT
    (* --- Robot Kinematic Override & Motion Commands --- *)
    rRobot_SpeedScale_Pct       : REAL := 100.0;  (* Dynamic robot trajectory velocity scale [0..100 %] *)
    rRobot_AccelScale_Pct       : REAL := 100.0;  (* Dynamic robot trajectory acceleration scale [0..100 %] *)
    bRobot_StartCycle_Cmd       : BOOL := FALSE;  (* Trigger next layer pick & place trajectory *)
    diRobot_PatternRecipe_ID    : DINT := 1;      (* Selected layer pattern recipe index [1..8] *)
    bGripper_VacZone1_En        : BOOL := FALSE;  (* Solenoid pilot vacuum zone 1 activate *)
    bGripper_VacZone2_En        : BOOL := FALSE;  (* Solenoid pilot vacuum zone 2 activate *)
    bGripper_VacZone3_En        : BOOL := FALSE;  (* Solenoid pilot vacuum zone 3 activate *)
    bGripper_VacZone4_En        : BOOL := FALSE;  (* Solenoid pilot vacuum zone 4 activate *)
    bGripper_Blowoff_Pulse      : BOOL := FALSE;  (* Compressed air blow-off release pulse *)
    
    (* --- Infeed & Collation Table Conveyor Drives --- *)
    rInfeedConveyor_Speed_mps   : REAL := 0.0;    (* Infeed carton metering belt linear speed [m/s] *)
    bInfeedPusher_Extend_Cmd    : BOOL := FALSE;  (* Pneumatic layer grouping collation pusher *)
    bSlipSheet_Dispense_Cmd     : BOOL := FALSE;  (* Robotic slip-sheet dispenser pick cycle *)
    
    (* --- Stretch Hood Applicator Motion Commands --- *)
    rHood_CarriageSpeed_mms     : REAL := 0.0;    (* Vertical descent carriage servo speed command [mm/s] *)
    rFinger_ExpandVel_mms       : REAL := 0.0;    (* 4-corner finger expansion cylinder speed [mm/s] *)
    bFilm_UnrollFeed_Cmd        : BOOL := FALSE;  (* Motorized film feed traction roll enable *)
    bFilm_CutKnife_Cmd          : BOOL := FALSE;  (* Rotary/guillotine film severance knife pulse *)
    bFilm_SealingBar_Cmd        : BOOL := FALSE;  (* Thermal/ultrasonic transverse top sealing bar *)
    bBottomUndercut_Tuck_Cmd    : BOOL := FALSE;  (* Pallet deck undercut fold tucking fingers *)
    
    (* --- Turntable & Outfeed Drives --- *)
    rTurntable_SpeedCmd_rpm     : REAL := 0.0;    (* Turntable servo rotation speed command [rpm] *)
    bOutfeedConveyor_Run_Cmd    : BOOL := FALSE;  (* Outfeed chain/roller transport conveyor motor *)
    
    (* --- Supervisory & Diagnostics --- *)
    wPalletizer_StatusWord      : WORD := 16#0000; (* Packed IEC status word for robot cell *)
    wStretchHood_StatusWord     : WORD := 16#0000; (* Packed IEC status word for hooder cell *)
    wAlarmWord_PriorityHH       : WORD := 16#0000; (* ISA-18.2 Critical high-high alarm word *)
    wAlarmWord_PriorityH        : WORD := 16#0000; (* ISA-18.2 Warning high alarm word *)
    wAlarmWord_PriorityL        : WORD := 16#0000; (* ISA-18.2 Low warning alarm word *)
    rPallet_CoG_Eccentricity_mm : REAL := 0.0;     (* Calculated center-of-gravity radial offset [mm] *)
    rPallet_StackStability_Idx  : REAL := 1.0;     (* Normalized dynamic stability index [0..1] *)
    diCurrentLayer_Num          : DINT := 0;       (* Current stacked layer count [0..10] *)
    diCompletedPallets_Count    : DINT := 0;       (* Shift finished wrapped pallet accumulator *)
    rCycleTime_Actual_s         : REAL := 0.0;     (* Elapsed cycle time for active pallet [s] *)
    bSafety_EStopTripped        : BOOL := FALSE;   (* Safety shutdown active flag *)
END_VAR
"""
    sections.append(sec1)

    # ==========================================
    # SECTION 2: VAR DECLARATIONS (MATRICES, MPC, TIMERS, TMR)
    # ==========================================
    sec2 = """VAR
    (* --- 2oo3 TMR Voting Variables & Discrepancy Timers --- *)
    rVoted_VacPress_mbar        : REAL := -750.0;
    bVacSensor_Fault_A          : BOOL := FALSE;
    bVacSensor_Fault_B          : BOOL := FALSE;
    bVacSensor_Fault_C          : BOOL := FALSE;
    rVac_DiscrepancyTimer_A_s   : REAL := 0.0;
    rVac_DiscrepancyTimer_B_s   : REAL := 0.0;
    rVac_DiscrepancyTimer_C_s   : REAL := 0.0;
    
    bVoted_CartonInfeed         : BOOL := FALSE;
    rInfeed_DebounceTimer_s     : REAL := 0.0;
    bInfeed_SensorFault         : BOOL := FALSE;
    
    rVoted_FilmTension_N        : REAL := 150.0;
    bFilmTension_Fault_A        : BOOL := FALSE;
    bFilmTension_Fault_B        : BOOL := FALSE;
    bFilmTension_Fault_C        : BOOL := FALSE;
    rFilmTen_DiscrepTimer_A_s   : REAL := 0.0;
    rFilmTen_DiscrepTimer_B_s   : REAL := 0.0;
    rFilmTen_DiscrepTimer_C_s   : REAL := 0.0;
    
    (* --- Discrete State-Space Model Matrices (8x8) --- *)
    (* States x: [TCP_pos_err, TCP_vel, P_vac, CoG_ecc, H_stack, Film_elong, Film_stress, TT_omega] *)
    matA                        : ARRAY[1..8, 1..8] OF REAL;
    matB                        : ARRAY[1..8, 1..4] OF REAL;
    matC                        : ARRAY[1..4, 1..8] OF REAL;
    matD                        : ARRAY[1..4, 1..4] OF REAL;
    
    vecState_x                  : ARRAY[1..8] OF REAL;
    vecState_xPred              : ARRAY[1..8] OF REAL;
    vecState_xObs               : ARRAY[1..8] OF REAL;
    vecOutput_y                 : ARRAY[1..4] OF REAL;
    vecOutput_yMeas             : ARRAY[1..4] OF REAL;
    vecControl_u                : ARRAY[1..4] OF REAL;
    vecControl_uPrev            : ARRAY[1..4] OF REAL;
    
    (* --- Observer Kalman Innovation Gain Matrix (8x4) --- *)
    matK_Obs                    : ARRAY[1..8, 1..4] OF REAL;
    vecInnov_Resid              : ARRAY[1..4] OF REAL;
    
    (* --- Receding Horizon MPC Matrices (Q: 8x8, R: 4x4, P: 8x8) --- *)
    matQ_Cost                   : ARRAY[1..8, 1..8] OF REAL;
    matR_Cost                   : ARRAY[1..4, 1..4] OF REAL;
    matP_Terminal               : ARRAY[1..8, 1..8] OF REAL;
    vecRef_x                    : ARRAY[1..8] OF REAL;
    rMPC_PredictedCost          : REAL := 0.0;
    
    (* --- Pallet Stability & Pattern Kinematics Storage --- *)
    rLayer_CoG_X_mm             : ARRAY[1..12] OF REAL; (* Layer X center of gravity [mm] *)
    rLayer_CoG_Y_mm             : ARRAY[1..12] OF REAL; (* Layer Y center of gravity [mm] *)
    rLayer_Mass_kg              : ARRAY[1..12] OF REAL; (* Layer total payload mass [kg] *)
    diBoxesPerLayer_Arr         : ARRAY[1..12] OF DINT; (* Number of cartons per layer *)
    rTotalPallet_Mass_kg        : REAL := 0.0;
    rGlobal_CoG_X_mm            : REAL := 0.0;
    rGlobal_CoG_Y_mm            : REAL := 0.0;
    rGlobal_CoG_Z_mm            : REAL := 0.0;
    rDynamic_Overturning_Mom_Nm : REAL := 0.0;
    rRestoring_Stabilizing_Mom_Nm: REAL := 0.0;
    
    (* --- Stretch Hood Film Rheology & Mechanics (Maxwell-Voigt) --- *)
    rFilm_ElasticModulus_MPa    : REAL := 220.0;  (* Low-density polyethylene tensile modulus [MPa] *)
    rFilm_ViscousDamping_MPas   : REAL := 15.5;   (* Viscoelastic damping parameter [MPa*s] *)
    rFilm_YieldStress_MPa       : REAL := 18.0;   (* Plastic yield threshold [MPa] *)
    rFilm_CrossSection_mm2      : REAL := 0.0;    (* Biaxial cross section area [mm2] *)
    rFilm_NominalPerimeter_mm   : REAL := 3800.0; (* Relaxed tubular perimeter [mm] *)
    rPallet_Perimeter_mm        : REAL := 4400.0; (* Stretched envelope perimeter (1200x1000 + 10%) [mm] *)
    rTarget_LongitudinalStretch : REAL := 1.15;   (* Target vertical stretch elongation factor (15%) *)
    rTarget_TransverseStretch   : REAL := 1.25;   (* Target radial stretch elongation factor (25%) *)
    rFilm_Strain_Epsilon        : REAL := 0.0;
    rFilm_Stress_Sigma_MPa      : REAL := 0.0;
    
    (* --- Finite State Machine State Enumeration --- *)
    nFSM_CurrentState           : INT := 0;
    nFSM_PreviousState          : INT := -1;
    rStateTimer_s               : REAL := 0.0;
    rStateTimeout_s             : REAL := 60.0;
    bStateTimeout_Alarm         : BOOL := FALSE;
    bLayerComplete_Flag         : BOOL := FALSE;
    bPalletComplete_Flag        : BOOL := FALSE;
    bHoodApplied_Flag           : BOOL := FALSE;
    bCellInterlock_Permissive   : BOOL := FALSE;
    
    (* --- ISA-18.2 Multi-Tiered Alarm Thresholds & Hysteresis --- *)
    rVac_Trip_HH_mbar           : REAL := -350.0; (* Carton drop danger HH *)
    rVac_Trip_H_mbar            : REAL := -600.0; (* Vacuum marginal H *)
    rVac_Hysteresis_mbar        : REAL := 25.0;
    
    rFilmTen_Trip_HH_N          : REAL := 420.0;  (* Film overstretch rupture HH *)
    rFilmTen_Trip_H_N           : REAL := 320.0;  (* High tension warning H *)
    rFilmTen_Trip_L_N           : REAL := 60.0;   (* Low tension warning L *)
    rFilmTen_Trip_LL_N          : REAL := 15.0;   (* Film tear / snapped LL *)
    rFilmTen_Hysteresis_N       : REAL := 10.0;
    
    rTilt_Trip_H_deg            : REAL := 2.5;    (* Pallet leaning warning H *)
    rTilt_Trip_HH_deg           : REAL := 5.0;    (* Pallet topple imminent HH *)
    rTilt_Hysteresis_deg        : REAL := 0.4;
    
    (* --- Loop Iterators & Temporary Calculation Registers --- *)
    i                           : INT := 0;
    j                           : INT := 0;
    k                           : INT := 0;
    rTemp_Sum                   : REAL := 0.0;
    rTemp_Diff                  : REAL := 0.0;
    rTemp_Term                  : REAL := 0.0;
    rInterlockRatio             : REAL := 0.0;
    bInitMatrices_Done          : BOOL := FALSE;
END_VAR
"""
    sections.append(sec2)

    # ==========================================
    # SECTION 3: MATRIX INITIALIZATION
    # ==========================================
    sec3 = """(* ========================================================================= *)
(* PHASE 1: DISCRETE STATE-SPACE (8x8) & MPC COST MATRIX DETERMINISTIC SETUP *)
(* ========================================================================= *)
IF NOT bInitMatrices_Done THEN
    (* Initialize State Transition Matrix A (8x8) *)
    (* Dynamics: Robot positioning, suction cup vacuum rate, pallet CoG inertia, film viscoelasticity *)
    FOR i := 1 TO 8 DO
        FOR j := 1 TO 8 DO
            matA[i, j] := 0.0;
            matQ_Cost[i, j] := 0.0;
            matP_Terminal[i, j] := 0.0;
        END_FOR;
    END_FOR;
    
    (* Row 1: Robot TCP Position Error (damping: 0.965, velocity coupling: 0.0098) *)
    matA[1, 1] := 0.9650;
    matA[1, 2] := 0.0098;
    matA[1, 4] := -0.0012; (* CoG eccentricity disturbance feedback *)
    
    (* Row 2: Robot TCP Velocity (inertial decay: 0.9420, acceleration response) *)
    matA[2, 1] := -0.0850;
    matA[2, 2] := 0.9420;
    matA[2, 4] := -0.0150;
    
    (* Row 3: Gripper Vacuum Manifold Pressure (vacuum leak/charge time constant tau = 0.08 s) *)
    matA[3, 3] := 0.8825; (* exp(-0.010 / 0.08) *)
    matA[3, 2] := -0.0045; (* Inertial carton peel disturbance during rapid TCP motion *)
    
    (* Row 4: Pallet Stack CoG Eccentricity (accumulated tilt & centrifugal drift) *)
    matA[4, 4] := 0.9920;
    matA[4, 2] := 0.0035; (* Robot motion vibration coupling *)
    matA[4, 8] := 0.0450; (* Turntable centrifugal acceleration force *)
    
    (* Row 5: Pallet Stack Height (constant between layer additions) *)
    matA[5, 5] := 1.0000;
    
    (* Row 6: Stretch Hood Tubular Film Elongation (viscoelastic relaxation: Kelvin-Voigt) *)
    matA[6, 6] := 0.9250;
    matA[6, 7] := 0.0038;
    
    (* Row 7: Stretch Hood Corner Film Stress (Maxwell relaxation: tau_rel = 0.45 s) *)
    matA[7, 6] := 1.8500; (* Hooke's modulus coupling dSigma/dEpsilon *)
    matA[7, 7] := 0.9780; (* exp(-0.010 / 0.45) *)
    
    (* Row 8: Turntable Rotational Speed (servo inertia & viscous friction) *)
    matA[8, 8] := 0.9550;
    
    (* Initialize Input Matrix B (8x4) *)
    (* Inputs: u1 = Robot Accel Cmd, u2 = Vacuum Valve Cmd, u3 = Finger Expand Cmd, u4 = Carriage Speed Cmd *)
    FOR i := 1 TO 8 DO
        FOR j := 1 TO 4 DO
            matB[i, j] := 0.0;
        END_FOR;
    END_FOR;
    
    matB[1, 1] := 0.0049; (* Position acceleration integral dt^2 / 2 *)
    matB[2, 1] := 0.9850; (* Direct acceleration drive *)
    matB[3, 2] := -14.500; (* Vacuum pump pull-down capacity [mbar/%] *)
    matB[4, 1] := 0.0125; (* Robot acceleration side-load on carton stack *)
    matB[6, 3] := 0.0850; (* Finger expansion displacement -> elongation *)
    matB[7, 3] := 1.4500; (* Finger expansion displacement -> stress increment *)
    matB[7, 4] := 0.6500; (* Carriage descent drag tension increase *)
    matB[8, 1] := 0.0020; (* Mechanical base resonance coupling *)
    
    (* Initialize Output Matrix C (4x8) *)
    (* Measured y: [TCP_pos_err, Vacuum_press, Film_tension, CoG_eccentricity] *)
    FOR i := 1 TO 4 DO
        FOR j := 1 TO 8 DO
            matC[i, j] := 0.0;
        END_FOR;
    END_FOR;
    matC[1, 1] := 1.0; (* TCP position error *)
    matC[2, 3] := 1.0; (* Vacuum pressure *)
    matC[3, 7] := 1.0; (* Corner film tension stress *)
    matC[4, 4] := 1.0; (* Pallet stack CoG eccentricity *)
    
    (* Initialize Direct Feedthrough Matrix D (4x4) *)
    FOR i := 1 TO 4 DO
        FOR j := 1 TO 4 DO
            matD[i, j] := 0.0;
        END_FOR;
    END_FOR;
    
    (* Initialize Kalman Innovation Filter Gain Matrix matK_Obs (8x4) *)
    matK_Obs[1, 1] := 0.2850; matK_Obs[1, 2] := 0.0000; matK_Obs[1, 3] := 0.0000; matK_Obs[1, 4] := 0.0120;
    matK_Obs[2, 1] := 0.3420; matK_Obs[2, 2] := 0.0000; matK_Obs[2, 3] := 0.0000; matK_Obs[2, 4] := 0.0250;
    matK_Obs[3, 1] := 0.0000; matK_Obs[3, 2] := 0.4150; matK_Obs[3, 3] := 0.0000; matK_Obs[3, 4] := 0.0000;
    matK_Obs[4, 1] := 0.0150; matK_Obs[4, 2] := 0.0000; matK_Obs[4, 3] := 0.0000; matK_Obs[4, 4] := 0.3800;
    matK_Obs[5, 1] := 0.0000; matK_Obs[5, 2] := 0.0000; matK_Obs[5, 3] := 0.0000; matK_Obs[5, 4] := 0.0000;
    matK_Obs[6, 1] := 0.0000; matK_Obs[6, 2] := 0.0000; matK_Obs[6, 3] := 0.2950; matK_Obs[6, 4] := 0.0000;
    matK_Obs[7, 1] := 0.0000; matK_Obs[7, 2] := 0.0000; matK_Obs[7, 3] := 0.4650; matK_Obs[7, 4] := 0.0000;
    matK_Obs[8, 1] := 0.0000; matK_Obs[8, 2] := 0.0000; matK_Obs[8, 3] := 0.0000; matK_Obs[8, 4] := 0.1250;
    
    (* Initialize MPC Cost Weights: Q (State deviations) *)
    matQ_Cost[1, 1] := 120.0; (* TCP position tracking penalty *)
    matQ_Cost[2, 2] := 15.0;  (* TCP velocity smoothing *)
    matQ_Cost[3, 3] := 85.0;  (* Vacuum loss critical penalty *)
    matQ_Cost[4, 4] := 250.0; (* Stack CoG eccentricity penalty (tipping prevention) *)
    matQ_Cost[5, 5] := 10.0;  (* Height consistency *)
    matQ_Cost[6, 6] := 45.0;  (* Film elongation regulation *)
    matQ_Cost[7, 7] := 180.0; (* Film tension over-stress/tear penalty *)
    matQ_Cost[8, 8] := 35.0;  (* Turntable jerk penalty *)
    
    (* Initialize MPC Cost Weights: R (Actuator effort and slew) *)
    matR_Cost[1, 1] := 12.0;  (* Robot acceleration effort *)
    matR_Cost[2, 2] := 4.5;   (* Vacuum solenoid throttling *)
    matR_Cost[3, 3] := 28.0;  (* Finger expander hydraulic effort *)
    matR_Cost[4, 4] := 18.0;  (* Carriage descent motor power *)
    
    (* Terminal Cost Matrix P *)
    FOR i := 1 TO 8 DO
        matP_Terminal[i, i] := matQ_Cost[i, i] * 2.85;
    END_FOR;
    
    (* Default state references *)
    vecRef_x[1] := 0.0;    (* Zero TCP error *)
    vecRef_x[2] := 0.0;    (* Target steady velocity *)
    vecRef_x[3] := -800.0; (* Ideal suction vacuum [mbar] *)
    vecRef_x[4] := 0.0;    (* Zero CoG eccentricity *)
    vecRef_x[5] := 1600.0; (* Target full pallet height [mm] *)
    vecRef_x[6] := 18.0;   (* 18% target film elongation *)
    vecRef_x[7] := 140.0;  (* 140 N target film tension *)
    vecRef_x[8] := 0.0;    (* Idle turntable *)
    
    bInitMatrices_Done := TRUE;
END_IF;
"""
    sections.append(sec3)

    # ==========================================
    # SECTION 4: 2oo3 TMR SENSOR VOTING
    # ==========================================
    sec4 = """(* ========================================================================= *)
(* PHASE 2: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING ENGINE         *)
(* ========================================================================= *)
(* 1. Gripper Suction Manifold Vacuum Transducers (ChA, ChB, ChC) *)
(* Check channel discrepancies: max allowable deviation = 85.0 mbar *)
IF ABS(rVacPress_ChA_mbar - rVacPress_ChB_mbar) > 85.0 THEN
    rVac_DiscrepancyTimer_A_s := rVac_DiscrepancyTimer_A_s + tScanTime_s;
ELSE
    rVac_DiscrepancyTimer_A_s := 0.0;
END_IF;

IF ABS(rVacPress_ChB_mbar - rVacPress_ChC_mbar) > 85.0 THEN
    rVac_DiscrepancyTimer_B_s := rVac_DiscrepancyTimer_B_s + tScanTime_s;
ELSE
    rVac_DiscrepancyTimer_B_s := 0.0;
END_IF;

IF ABS(rVacPress_ChC_mbar - rVacPress_ChA_mbar) > 85.0 THEN
    rVac_DiscrepancyTimer_C_s := rVac_DiscrepancyTimer_C_s + tScanTime_s;
ELSE
    rVac_DiscrepancyTimer_C_s := 0.0;
END_IF;

(* Latch fault flags after 0.150s persistence *)
IF rVac_DiscrepancyTimer_A_s > 0.150 AND rVac_DiscrepancyTimer_C_s > 0.150 THEN
    bVacSensor_Fault_A := TRUE;
END_IF;
IF rVac_DiscrepancyTimer_A_s > 0.150 AND rVac_DiscrepancyTimer_B_s > 0.150 THEN
    bVacSensor_Fault_B := TRUE;
END_IF;
IF rVac_DiscrepancyTimer_B_s > 0.150 AND rVac_DiscrepancyTimer_C_s > 0.150 THEN
    bVacSensor_Fault_C := TRUE;
END_IF;

IF bAlarmReset_PB THEN
    bVacSensor_Fault_A := FALSE;
    bVacSensor_Fault_B := FALSE;
    bVacSensor_Fault_C := FALSE;
END_IF;

(* 2oo3 Median Voting Algorithm *)
IF NOT bVacSensor_Fault_A AND NOT bVacSensor_Fault_B AND NOT bVacSensor_Fault_C THEN
    (* All 3 healthy: Exact Median selection *)
    IF (rVacPress_ChA_mbar >= rVacPress_ChB_mbar AND rVacPress_ChA_mbar <= rVacPress_ChC_mbar) OR
       (rVacPress_ChA_mbar <= rVacPress_ChB_mbar AND rVacPress_ChA_mbar >= rVacPress_ChC_mbar) THEN
        rVoted_VacPress_mbar := rVacPress_ChA_mbar;
    ELSIF (rVacPress_ChB_mbar >= rVacPress_ChA_mbar AND rVacPress_ChB_mbar <= rVacPress_ChC_mbar) OR
          (rVacPress_ChB_mbar <= rVacPress_ChA_mbar AND rVacPress_ChB_mbar >= rVacPress_ChC_mbar) THEN
        rVoted_VacPress_mbar := rVacPress_ChB_mbar;
    ELSE
        rVoted_VacPress_mbar := rVacPress_ChC_mbar;
    END_IF;
ELSIF bVacSensor_Fault_A AND NOT bVacSensor_Fault_B AND NOT bVacSensor_Fault_C THEN
    (* Degradation to 1oo2 average of B and C *)
    rVoted_VacPress_mbar := (rVacPress_ChB_mbar + rVacPress_ChC_mbar) * 0.5;
ELSIF bVacSensor_Fault_B AND NOT bVacSensor_Fault_A AND NOT bVacSensor_Fault_C THEN
    (* Degradation to 1oo2 average of A and C *)
    rVoted_VacPress_mbar := (rVacPress_ChA_mbar + rVacPress_ChC_mbar) * 0.5;
ELSIF bVacSensor_Fault_C AND NOT bVacSensor_Fault_A AND NOT bVacSensor_Fault_B THEN
    (* Degradation to 1oo2 average of A and B *)
    rVoted_VacPress_mbar := (rVacPress_ChA_mbar + rVacPress_ChB_mbar) * 0.5;
ELSIF NOT bVacSensor_Fault_A THEN
    rVoted_VacPress_mbar := rVacPress_ChA_mbar;
ELSIF NOT bVacSensor_Fault_B THEN
    rVoted_VacPress_mbar := rVacPress_ChB_mbar;
ELSE
    rVoted_VacPress_mbar := rVacPress_ChC_mbar;
END_IF;

(* 2. Infeed Collation Table Optical Sensors (SensA, SensB, SensC) *)
(* 2oo3 Boolean Majority Voting with Debounce *)
IF (bCartonInfeed_SensA AND bCartonInfeed_SensB) OR
   (bCartonInfeed_SensB AND bCartonInfeed_SensC) OR
   (bCartonInfeed_SensA AND bCartonInfeed_SensC) THEN
    rInfeed_DebounceTimer_s := rInfeed_DebounceTimer_s + tScanTime_s;
    IF rInfeed_DebounceTimer_s >= 0.050 THEN
        bVoted_CartonInfeed := TRUE;
    END_IF;
ELSE
    rInfeed_DebounceTimer_s := 0.0;
    bVoted_CartonInfeed := FALSE;
END_IF;

(* Diagnostic Check: Sensor discrepancy *)
IF (bCartonInfeed_SensA <> bCartonInfeed_SensB) OR (bCartonInfeed_SensB <> bCartonInfeed_SensC) THEN
    bInfeed_SensorFault := TRUE;
ELSE
    bInfeed_SensorFault := FALSE;
END_IF;

(* 3. Stretch Hood Corner Film Tension Load Cells (ChA, ChB, ChC) *)
IF ABS(rFilmTension_ChA_N - rFilmTension_ChB_N) > 40.0 THEN
    rFilmTen_DiscrepTimer_A_s := rFilmTen_DiscrepTimer_A_s + tScanTime_s;
ELSE
    rFilmTen_DiscrepTimer_A_s := 0.0;
END_IF;

IF ABS(rFilmTension_ChB_N - rFilmTension_ChC_N) > 40.0 THEN
    rFilmTen_DiscrepTimer_B_s := rFilmTen_DiscrepTimer_B_s + tScanTime_s;
ELSE
    rFilmTen_DiscrepTimer_B_s := 0.0;
END_IF;

IF ABS(rFilmTension_ChC_N - rFilmTension_ChA_N) > 40.0 THEN
    rFilmTen_DiscrepTimer_C_s := rFilmTen_DiscrepTimer_C_s + tScanTime_s;
ELSE
    rFilmTen_DiscrepTimer_C_s := 0.0;
END_IF;

IF rFilmTen_DiscrepTimer_A_s > 0.200 AND rFilmTen_DiscrepTimer_C_s > 0.200 THEN
    bFilmTension_Fault_A := TRUE;
END_IF;
IF rFilmTen_DiscrepTimer_A_s > 0.200 AND rFilmTen_DiscrepTimer_B_s > 0.200 THEN
    bFilmTension_Fault_B := TRUE;
END_IF;
IF rFilmTen_DiscrepTimer_B_s > 0.200 AND rFilmTen_DiscrepTimer_C_s > 0.200 THEN
    bFilmTension_Fault_C := TRUE;
END_IF;

IF bAlarmReset_PB THEN
    bFilmTension_Fault_A := FALSE;
    bFilmTension_Fault_B := FALSE;
    bFilmTension_Fault_C := FALSE;
END_IF;

(* Voted Film Tension Calculation *)
IF NOT bFilmTension_Fault_A AND NOT bFilmTension_Fault_B AND NOT bFilmTension_Fault_C THEN
    IF (rFilmTension_ChA_N >= rFilmTension_ChB_N AND rFilmTension_ChA_N <= rFilmTension_ChC_N) OR
       (rFilmTension_ChA_N <= rFilmTension_ChB_N AND rFilmTension_ChA_N >= rFilmTension_ChC_N) THEN
        rVoted_FilmTension_N := rFilmTension_ChA_N;
    ELSIF (rFilmTension_ChB_N >= rFilmTension_ChA_N AND rFilmTension_ChB_N <= rFilmTension_ChC_N) OR
          (rFilmTension_ChB_N <= rFilmTension_ChA_N AND rFilmTension_ChB_N >= rFilmTension_ChC_N) THEN
        rVoted_FilmTension_N := rFilmTension_ChB_N;
    ELSE
        rVoted_FilmTension_N := rFilmTension_ChC_N;
    END_IF;
ELSIF bFilmTension_Fault_A AND NOT bFilmTension_Fault_B AND NOT bFilmTension_Fault_C THEN
    rVoted_FilmTension_N := (rFilmTension_ChB_N + rFilmTension_ChC_N) * 0.5;
ELSIF bFilmTension_Fault_B AND NOT bFilmTension_Fault_A AND NOT bFilmTension_Fault_C THEN
    rVoted_FilmTension_N := (rFilmTension_ChA_N + rFilmTension_ChC_N) * 0.5;
ELSIF bFilmTension_Fault_C AND NOT bFilmTension_Fault_A AND NOT bFilmTension_Fault_B THEN
    rVoted_FilmTension_N := (rFilmTension_ChA_N + rFilmTension_ChB_N) * 0.5;
ELSIF NOT bFilmTension_Fault_A THEN
    rVoted_FilmTension_N := rFilmTension_ChA_N;
ELSIF NOT bFilmTension_Fault_B THEN
    rVoted_FilmTension_N := rFilmTension_ChB_N;
ELSE
    rVoted_FilmTension_N := rFilmTension_ChC_N;
END_IF;
"""
    sections.append(sec4)

    # ==========================================
    # SECTION 5: PALLET STACK STABILITY & COG OBSERVER
    # ==========================================
    sec5 = """(* ========================================================================= *)
(* PHASE 3: PALLET STACK STABILITY OBSERVER & LAYER COG KINEMATICS           *)
(* ========================================================================= *)
(* Calculate cumulative payload mass and 3D Center of Gravity (CoG) *)
rTotalPallet_Mass_kg := 25.0; (* Base wood/plastic pallet tare mass [kg] *)
rTemp_Sum := 0.0;
rTemp_Term := 0.0;

IF diCurrentLayer_Num > 0 THEN
    FOR i := 1 TO 12 DO
        IF i <= diCurrentLayer_Num THEN
            rTotalPallet_Mass_kg := rTotalPallet_Mass_kg + rLayer_Mass_kg[i];
            rTemp_Sum := rTemp_Sum + (rLayer_Mass_kg[i] * rLayer_CoG_X_mm[i]);
            rTemp_Term := rTemp_Term + (rLayer_Mass_kg[i] * rLayer_CoG_Y_mm[i]);
        END_FOR;
    END_IF;
    
    IF rTotalPallet_Mass_kg > 0.0 THEN
        rGlobal_CoG_X_mm := rTemp_Sum / rTotalPallet_Mass_kg;
        rGlobal_CoG_Y_mm := rTemp_Term / rTotalPallet_Mass_kg;
    ELSE
        rGlobal_CoG_X_mm := 0.0;
        rGlobal_CoG_Y_mm := 0.0;
    END_IF;
    rGlobal_CoG_Z_mm := (DINT_TO_REAL(diCurrentLayer_Num) * rCartonHeight_mm * 0.5) + 145.0; (* 145mm pallet deck *)
ELSE
    rGlobal_CoG_X_mm := 0.0;
    rGlobal_CoG_Y_mm := 0.0;
    rGlobal_CoG_Z_mm := 72.5;
END_IF;

(* Radial eccentricity of Center of Gravity from pallet geometric center [mm] *)
rPallet_CoG_Eccentricity_mm := SQRT((rGlobal_CoG_X_mm * rGlobal_CoG_X_mm) + (rGlobal_CoG_Y_mm * rGlobal_CoG_Y_mm));

(* Dynamic Overturning Moment Calculation:
   M_overturn = Mass * ( g * sin(theta_tilt) + a_transverse * cos(theta_tilt) ) * CoG_Z
   Where a_transverse includes turntable centrifugal acceleration: omega^2 * r_cog *)
rDynamic_Overturning_Mom_Nm := rTotalPallet_Mass_kg * (
    (9.81 * SIN((rStack_TiltAnglePitch_deg + rStack_TiltAngleRoll_deg) * 0.0174533)) +
    (((rTurntable_RotSpeed_rpm * 0.10472) * (rTurntable_RotSpeed_rpm * 0.10472) * (rPallet_CoG_Eccentricity_mm * 0.001)) +
     (rRobot_TCP_Vel_mms * 0.0001)) (* Robot inertial reaction on frame *)
) * (rGlobal_CoG_Z_mm * 0.001);

(* Restoring Moment: M_restore = Mass * g * (Half_Pallet_Base_Width - CoG_offset) *)
(* Standard Euro/Industrial pallet base width: 1000 mm / 2 = 500 mm *)
IF (500.0 - rPallet_CoG_Eccentricity_mm) > 50.0 THEN
    rRestoring_Stabilizing_Mom_Nm := rTotalPallet_Mass_kg * 9.81 * ((500.0 - rPallet_CoG_Eccentricity_mm) * 0.001);
ELSE
    rRestoring_Stabilizing_Mom_Nm := rTotalPallet_Mass_kg * 9.81 * 0.050; (* Min safety floor *)
END_IF;

(* Normalized Stability Index [0.0 .. 1.0] *)
IF rRestoring_Stabilizing_Mom_Nm > 0.0 THEN
    rPallet_StackStability_Idx := 1.0 - (ABS(rDynamic_Overturning_Mom_Nm) / rRestoring_Stabilizing_Mom_Nm);
    IF rPallet_StackStability_Idx < 0.0 THEN
        rPallet_StackStability_Idx := 0.0;
    ELSIF rPallet_StackStability_Idx > 1.0 THEN
        rPallet_StackStability_Idx := 1.0;
    END_IF;
ELSE
    rPallet_StackStability_Idx := 0.0;
END_IF;

(* Dynamic Robot Kinematic Scaling based on stack height and stability index *)
IF rPallet_StackStability_Idx < 0.50 THEN
    (* Severe instability risk: scale down robot and turntable speed *)
    rRobot_SpeedScale_Pct := 40.0 + (rPallet_StackStability_Idx * 40.0);
    rRobot_AccelScale_Pct := 25.0 + (rPallet_StackStability_Idx * 50.0);
ELSIF rPallet_StackStability_Idx < 0.80 THEN
    (* Moderate caution *)
    rRobot_SpeedScale_Pct := 75.0 + ((rPallet_StackStability_Idx - 0.50) * 50.0);
    rRobot_AccelScale_Pct := 60.0 + ((rPallet_StackStability_Idx - 0.50) * 80.0);
ELSE
    (* Full nominal velocity *)
    rRobot_SpeedScale_Pct := 100.0;
    rRobot_AccelScale_Pct := 100.0;
END_IF;

(* Further de-rate when stacking top layers (height > 1800 mm) *)
IF rStack_MeasuredHeight_mm > 1800.0 THEN
    rRobot_SpeedScale_Pct := rRobot_SpeedScale_Pct * 0.85;
    rRobot_AccelScale_Pct := rRobot_AccelScale_Pct * 0.70;
END_IF;
"""
    sections.append(sec5)

    # ==========================================
    # SECTION 6: STATE-SPACE PREDICTION & KALMAN FILTER
    # ==========================================
    sec6 = """(* ========================================================================= *)
(* PHASE 4: STATE-SPACE PROPAGATION & KALMAN INNOVATION OBSERVER             *)
(* ========================================================================= *)
(* Pack measured observation vector y_meas:
   y_meas[1] = TCP position error = Robot_TCP_PosZ_mm - Target_Layer_Z
   y_meas[2] = Voted vacuum pressure [mbar]
   y_meas[3] = Voted corner film tension [N]
   y_meas[4] = Stack CoG eccentricity [mm] *)
vecOutput_yMeas[1] := rRobot_TCP_PosZ_mm - ((DINT_TO_REAL(diCurrentLayer_Num) * rCartonHeight_mm) + 200.0);
vecOutput_yMeas[2] := rVoted_VacPress_mbar;
vecOutput_yMeas[3] := rVoted_FilmTension_N;
vecOutput_yMeas[4] := rPallet_CoG_Eccentricity_mm;

(* 1. Calculate Observer Innovation Residual: e = y_meas - (C * x_hat + D * u) *)
FOR i := 1 TO 4 DO
    rTemp_Sum := 0.0;
    FOR j := 1 TO 8 DO
        rTemp_Sum := rTemp_Sum + (matC[i, j] * vecState_xObs[j]);
    END_FOR;
    FOR j := 1 TO 4 DO
        rTemp_Sum := rTemp_Sum + (matD[i, j] * vecControl_uPrev[j]);
    END_FOR;
    vecInnov_Resid[i] := vecOutput_yMeas[i] - rTemp_Sum;
END_FOR;

(* 2. Correct State Estimate with Kalman Gain: x_hat = x_pred + K * e *)
FOR i := 1 TO 8 DO
    rTemp_Sum := 0.0;
    FOR j := 1 TO 4 DO
        rTemp_Sum := rTemp_Sum + (matK_Obs[i, j] * vecInnov_Resid[j]);
    END_FOR;
    vecState_xObs[i] := vecState_xPred[i] + rTemp_Sum;
    vecState_x[i] := vecState_xObs[i];
END_FOR;

(* 3. Propagate Discrete State-Space Model for Next Cycle: x_pred[k+1] = A * x_hat + B * u *)
FOR i := 1 TO 8 DO
    rTemp_Sum := 0.0;
    FOR j := 1 TO 8 DO
        rTemp_Sum := rTemp_Sum + (matA[i, j] * vecState_xObs[j]);
    END_FOR;
    FOR j := 1 TO 4 DO
        rTemp_Sum := rTemp_Sum + (matB[i, j] * vecControl_u[j]);
    END_FOR;
    vecState_xPred[i] := rTemp_Sum;
END_FOR;

(* Store previous control inputs *)
FOR i := 1 TO 4 DO
    vecControl_uPrev[i] := vecControl_u[i];
END_FOR;
"""
    sections.append(sec6)

    # ==========================================
    # SECTION 7: RECEDING HORIZON MPC OPTIMIZER
    # ==========================================
    sec7 = """(* ========================================================================= *)
(* PHASE 5: RECEDING-HORIZON MODEL PREDICTIVE CONTROL OPTIMIZATION            *)
(* ========================================================================= *)
(* Evaluate Quadratic Objective Cost Function:
   J = sum( (x - x_ref)^T * Q * (x - x_ref) ) + sum( u^T * R * u ) + (x_N - x_ref)^T * P * (x_N - x_ref) *)
rMPC_PredictedCost := 0.0;

(* State Tracking Error Cost *)
FOR i := 1 TO 8 DO
    rTemp_Diff := vecState_x[i] - vecRef_x[i];
    FOR j := 1 TO 8 DO
        rMPC_PredictedCost := rMPC_PredictedCost + (rTemp_Diff * matQ_Cost[i, j] * (vecState_x[j] - vecRef_x[j]));
    END_FOR;
END_FOR;

(* Control Effort Cost *)
FOR i := 1 TO 4 DO
    FOR j := 1 TO 4 DO
        rMPC_PredictedCost := rMPC_PredictedCost + (vecControl_u[i] * matR_Cost[i, j] * vecControl_u[j]);
    END_FOR;
END_FOR;

(* Terminal State Cost *)
FOR i := 1 TO 8 DO
    rTemp_Diff := vecState_xPred[i] - vecRef_x[i];
    FOR j := 1 TO 8 DO
        rMPC_PredictedCost := rMPC_PredictedCost + (rTemp_Diff * matP_Terminal[i, j] * (vecState_xPred[j] - vecRef_x[j]));
    END_FOR;
END_FOR;

(* Optimal Control Derivation via Constrained Gradient Step *)
(* u1: Robot TCP Acceleration Limit Override [0 .. 100 %] *)
IF vecState_x[4] > 35.0 THEN
    (* Excessive CoG eccentricity: de-rate robot acceleration proportionally *)
    vecControl_u[1] := 100.0 - ((vecState_x[4] - 35.0) * 1.85);
    IF vecControl_u[1] < 20.0 THEN
        vecControl_u[1] := 20.0;
    END_IF;
ELSE
    vecControl_u[1] := 100.0;
END_IF;

(* u2: Pneumatic Vacuum Generator Solenoid Pulse Rate [%] *)
IF vecState_x[3] > -650.0 THEN
    (* Vacuum leaking or insufficient seal: boost pump pulse rate to maximum *)
    vecControl_u[2] := 100.0;
ELSIF vecState_x[3] < -850.0 THEN
    (* High seal achieved: economy mode valve pulsing *)
    vecControl_u[2] := 35.0;
ELSE
    vecControl_u[2] := 70.0;
END_IF;

(* u3: Stretch Hood 4-Corner Finger Expansion Displacement Velocity [mm/s] *)
IF ABS(vecState_x[7] - vecRef_x[7]) > 25.0 THEN
    (* Modulate finger expansion rate based on measured film tension *)
    IF vecState_x[7] < vecRef_x[7] THEN
        (* Tension too low: expand fingers faster *)
        vecControl_u[3] := 45.0 + ((vecRef_x[7] - vecState_x[7]) * 0.85);
    ELSE
        (* Tension too high: slow down expansion to prevent film necking/rupture *)
        vecControl_u[3] := 45.0 - ((vecState_x[7] - vecRef_x[7]) * 0.95);
        IF vecControl_u[3] < 10.0 THEN
            vecControl_u[3] := 10.0;
        END_IF;
    END_IF;
ELSE
    vecControl_u[3] := 45.0; (* Nominal finger expansion velocity [mm/s] *)
END_IF;

(* u4: Stretch Hood Elevator Carriage Vertical Descent Velocity [mm/s] *)
IF rStack_MeasuredHeight_mm > 0.0 AND rHood_CarriageHeight_mm > 150.0 THEN
    (* S-curve deceleration profile approaching pallet base *)
    IF rHood_CarriageHeight_mm < 600.0 THEN
        vecControl_u[4] := 120.0 * (rHood_CarriageHeight_mm / 600.0);
        IF vecControl_u[4] < 35.0 THEN
            vecControl_u[4] := 35.0; (* Creep speed for bottom undercut locking *)
        END_IF;
    ELSE
        vecControl_u[4] := 300.0; (* Nominal high-speed descent *)
    END_IF;
ELSE
    vecControl_u[4] := 0.0;
END_IF;
"""
    sections.append(sec7)

    # ==========================================
    # SECTION 8: PATTERN GENERATOR & RHEOLOGY
    # ==========================================
    sec8 = """(* ========================================================================= *)
(* PHASE 6: LAYER PATTERN GENERATION & STRETCH HOOD FILM RHEOLOGY             *)
(* ========================================================================= *)
(* 1. Layer Interlocking Pattern Formulation:
   Even Layers vs. Odd Layers alternating 90/180 degree rotation to build brick-bond column integrity *)
IF (diCurrentLayer_Num MOD 2) = 1 THEN
    (* Odd Layer: Pinwheel 5-carton interlock pattern *)
    diRobot_PatternRecipe_ID := 1;
    rInterlockRatio := 0.82;
    (* Expected CoG offsets for odd pattern layout [mm] *)
    IF diCurrentLayer_Num <= 12 THEN
        rLayer_CoG_X_mm[diCurrentLayer_Num] := 12.0;
        rLayer_CoG_Y_mm[diCurrentLayer_Num] := -8.5;
        rLayer_Mass_kg[diCurrentLayer_Num] := 5.0 * rCartonWeight_kg;
        diBoxesPerLayer_Arr[diCurrentLayer_Num] := 5;
    END_IF;
ELSE
    (* Even Layer: Mirrored 5-carton cross-bond pattern *)
    diRobot_PatternRecipe_ID := 2;
    rInterlockRatio := 0.88;
    IF diCurrentLayer_Num <= 12 AND diCurrentLayer_Num > 0 THEN
        rLayer_CoG_X_mm[diCurrentLayer_Num] := -10.5;
        rLayer_CoG_Y_mm[diCurrentLayer_Num] := 11.0;
        rLayer_Mass_kg[diCurrentLayer_Num] := 5.0 * rCartonWeight_kg;
        diBoxesPerLayer_Arr[diCurrentLayer_Num] := 5;
    END_IF;
END_IF;

(* 2. Stretch Hood Tubular Film Mechanics (Non-linear Viscoelastic Model) *)
(* Calculate actual stretched perimeter: 2 * (SpanX + SpanY) *)
rPallet_Perimeter_mm := 2.0 * (rFinger_ExpandSpanX_mm + rFinger_ExpandSpanY_mm);

(* Engineering Strain Epsilon = (Perimeter_stretched - Perimeter_relaxed) / Perimeter_relaxed *)
IF rFilm_NominalPerimeter_mm > 0.0 THEN
    rFilm_Strain_Epsilon := (rPallet_Perimeter_mm - rFilm_NominalPerimeter_mm) / rFilm_NominalPerimeter_mm;
ELSE
    rFilm_Strain_Epsilon := 0.0;
END_IF;

(* Cross-sectional area of tubular film under biaxial tension:
   Area = 2 * Perimeter * Thickness / (1 + Poisson_Ratio * Epsilon) *)
rFilm_CrossSection_mm2 := 2.0 * rFilm_NominalPerimeter_mm * (rFilm_Thickness_um * 0.001) / (1.0 + (0.45 * rFilm_Strain_Epsilon));

(* Viscoelastic Constitutive Law: Sigma = E * Epsilon + Eta * (dEpsilon/dt) *)
rFilm_Stress_Sigma_MPa := (rFilm_ElasticModulus_MPa * rFilm_Strain_Epsilon) + 
                          (rFilm_ViscousDamping_MPas * (rFinger_ExpandVel_mms * 0.001));

(* Check Plastic Yield Criterion: If Sigma > Sigma_yield, risk of permanent necking *)
IF rFilm_Stress_Sigma_MPa > rFilm_YieldStress_MPa THEN
    (* Reduce finger span expansion rate immediately *)
    rFinger_ExpandVel_mms := rFinger_ExpandVel_mms * 0.60;
END_IF;
"""
    sections.append(sec8)

    # ==========================================
    # SECTION 9: ISA-18.2 ALARMS & DIAGNOSTICS
    # ==========================================
    sec9 = """(* ========================================================================= *)
(* PHASE 7: ISA-18.2 MULTI-TIERED ALARM MATRIX & STATUS PACKING              *)
(* ========================================================================= *)
(* Clear transient alarm bits before cyclic evaluation *)
wAlarmWord_PriorityHH := 16#0000;
wAlarmWord_PriorityH := 16#0000;
wAlarmWord_PriorityL := 16#0000;

(* --- ALARM 1: Gripper Vacuum Level / Carton Drop Hazard --- *)
(* HH Trip: Vacuum worse than -350 mbar during robotic transfer *)
IF rVoted_VacPress_mbar > rVac_Trip_HH_mbar AND bRobot_InMotion THEN
    wAlarmWord_PriorityHH := wAlarmWord_PriorityHH OR 16#0001; (* Bit 0: VACUUM_FAILURE_DROP_RISK_HH *)
ELSIF rVoted_VacPress_mbar > rVac_Trip_H_mbar THEN
    wAlarmWord_PriorityH := wAlarmWord_PriorityH OR 16#0001;   (* Bit 0: VACUUM_MARGINAL_H *)
END_IF;

(* --- ALARM 2: Stretch Hood Film Tension Rupture / Under-Tension --- *)
(* HH Trip: Tension > 420 N (film rupture imminent) *)
IF rVoted_FilmTension_N > rFilmTen_Trip_HH_N THEN
    wAlarmWord_PriorityHH := wAlarmWord_PriorityHH OR 16#0002; (* Bit 1: FILM_OVERSTRETCH_RUPTURE_HH *)
ELSIF rVoted_FilmTension_N > rFilmTen_Trip_H_N THEN
    wAlarmWord_PriorityH := wAlarmWord_PriorityH OR 16#0002;   (* Bit 1: FILM_HIGH_TENSION_WARNING_H *)
END_IF;

(* LL Trip: Tension < 15 N during hood sleeve downward application (film snapped / torn) *)
IF rVoted_FilmTension_N < rFilmTen_Trip_LL_N AND (nFSM_CurrentState = 70) THEN
    wAlarmWord_PriorityHH := wAlarmWord_PriorityHH OR 16#0004; (* Bit 2: FILM_TEAR_SNAPPED_LL *)
ELSIF rVoted_FilmTension_N < rFilmTen_Trip_L_N AND (nFSM_CurrentState = 70) THEN
    wAlarmWord_PriorityL := wAlarmWord_PriorityL OR 16#0002;   (* Bit 1: FILM_LOW_TENSION_WARNING_L *)
END_IF;

(* --- ALARM 3: Pallet Stack Stability & Tilt Angle --- *)
(* HH Trip: Tilt angle > 5.0 deg (stack toppling) *)
IF (ABS(rStack_TiltAnglePitch_deg) > rTilt_Trip_HH_deg) OR (ABS(rStack_TiltAngleRoll_deg) > rTilt_Trip_HH_deg) THEN
    wAlarmWord_PriorityHH := wAlarmWord_PriorityHH OR 16#0008; (* Bit 3: PALLET_STACK_TOPPLE_DANGER_HH *)
ELSIF (ABS(rStack_TiltAnglePitch_deg) > rTilt_Trip_H_deg) OR (ABS(rStack_TiltAngleRoll_deg) > rTilt_Trip_H_deg) THEN
    wAlarmWord_PriorityH := wAlarmWord_PriorityH OR 16#0004;   (* Bit 2: PALLET_STACK_TILT_EXCESSIVE_H *)
END_IF;

(* --- ALARM 4: Sensor TMR Voting Discrepancies --- *)
IF bVacSensor_Fault_A OR bVacSensor_Fault_B OR bVacSensor_Fault_C THEN
    wAlarmWord_PriorityL := wAlarmWord_PriorityL OR 16#0004;   (* Bit 2: VAC_SENSOR_TMR_DISCREPANCY *)
END_IF;

IF bFilmTension_Fault_A OR bFilmTension_Fault_B OR bFilmTension_Fault_C THEN
    wAlarmWord_PriorityL := wAlarmWord_PriorityL OR 16#0008;   (* Bit 3: FILM_TENSION_TMR_DISCREPANCY *)
END_IF;

IF bInfeed_SensorFault THEN
    wAlarmWord_PriorityL := wAlarmWord_PriorityL OR 16#0010;   (* Bit 4: INFEED_SENSOR_DISCREPANCY *)
END_IF;

(* --- ALARM 5: Safety Light Curtain & E-Stop Intrusion --- *)
IF NOT bSafetyCurtain_Clear THEN
    wAlarmWord_PriorityHH := wAlarmWord_PriorityHH OR 16#0010; (* Bit 4: SAFETY_CURTAIN_MUTING_VIOLATION_HH *)
END_IF;

IF bEmergencyStop_Active THEN
    wAlarmWord_PriorityHH := wAlarmWord_PriorityHH OR 16#0020; (* Bit 5: HARDWARE_EMERGENCY_STOP_HH *)
    bSafety_EStopTripped := TRUE;
ELSE
    bSafety_EStopTripped := FALSE;
END_IF;

(* --- ALARM 6: State Machine Timeout --- *)
IF bStateTimeout_Alarm THEN
    wAlarmWord_PriorityH := wAlarmWord_PriorityH OR 16#0008;   (* Bit 3: FSM_CYCLE_TIMEOUT_FAULT_H *)
END_IF;

(* Pack Diagnostic Status Words *)
(* wPalletizer_StatusWord:
   Bit 0: Auto Mode Active
   Bit 1: Infeed Collation Table Full
   Bit 2: Robot Active Trajectory
   Bit 3: Gripper Vacuum Established
   Bit 4: Slip-Sheet Dispenser Cycle
   Bit 5: Layer Build Complete
   Bit 6: Full Pallet Build Complete
   Bit 7: Turntable In Motion *)
wPalletizer_StatusWord := 16#0000;
IF bAutoMode_Cmd THEN wPalletizer_StatusWord := wPalletizer_StatusWord OR 16#0001; END_IF;
IF bVoted_CartonInfeed THEN wPalletizer_StatusWord := wPalletizer_StatusWord OR 16#0002; END_IF;
IF bRobot_InMotion THEN wPalletizer_StatusWord := wPalletizer_StatusWord OR 16#0004; END_IF;
IF rVoted_VacPress_mbar < -600.0 THEN wPalletizer_StatusWord := wPalletizer_StatusWord OR 16#0008; END_IF;
IF bSlipSheet_Dispense_Cmd THEN wPalletizer_StatusWord := wPalletizer_StatusWord OR 16#0010; END_IF;
IF bLayerComplete_Flag THEN wPalletizer_StatusWord := wPalletizer_StatusWord OR 16#0020; END_IF;
IF bPalletComplete_Flag THEN wPalletizer_StatusWord := wPalletizer_StatusWord OR 16#0040; END_IF;
IF ABS(rTurntable_RotSpeed_rpm) > 0.5 THEN wPalletizer_StatusWord := wPalletizer_StatusWord OR 16#0080; END_IF;

(* wStretchHood_StatusWord:
   Bit 0: Hooder Auto Permissive Ready
   Bit 1: Film Roll Low Warning (< 250mm)
   Bit 2: Film Unrolling Active
   Bit 3: Ultrasonic Sealing Bar Active
   Bit 4: Guillotine Cut Knife Active
   Bit 5: 4-Corner Fingers Expanded
   Bit 6: Hood Carriage Descending
   Bit 7: Bottom Deck Tuck Complete *)
wStretchHood_StatusWord := 16#0000;
IF bCellInterlock_Permissive THEN wStretchHood_StatusWord := wStretchHood_StatusWord OR 16#0001; END_IF;
IF rFilmRoll_RemainingDia_mm < 250.0 THEN wStretchHood_StatusWord := wStretchHood_StatusWord OR 16#0002; END_IF;
IF bFilm_UnrollFeed_Cmd THEN wStretchHood_StatusWord := wStretchHood_StatusWord OR 16#0004; END_IF;
IF bFilm_SealingBar_Cmd THEN wStretchHood_StatusWord := wStretchHood_StatusWord OR 16#0008; END_IF;
IF bFilm_CutKnife_Cmd THEN wStretchHood_StatusWord := wStretchHood_StatusWord OR 16#0010; END_IF;
IF rFinger_ExpandSpanX_mm > 1000.0 THEN wStretchHood_StatusWord := wStretchHood_StatusWord OR 16#0020; END_IF;
IF rHood_CarriageSpeed_mms > 20.0 THEN wStretchHood_StatusWord := wStretchHood_StatusWord OR 16#0040; END_IF;
IF bBottomUndercut_Tuck_Cmd THEN wStretchHood_StatusWord := wStretchHood_StatusWord OR 16#0080; END_IF;
"""
    sections.append(sec9)

    # ==========================================
    # SECTION 10: MULTI-STAGE FINITE STATE MACHINE
    # ==========================================
    sec10 = """(* ========================================================================= *)
(* PHASE 8: MULTI-STAGE CELL FINITE STATE MACHINE (FSM)                       *)
(* ========================================================================= *)
(* State timer accumulation *)
IF nFSM_CurrentState = nFSM_PreviousState THEN
    rStateTimer_s := rStateTimer_s + tScanTime_s;
    IF rStateTimer_s >= rStateTimeout_s THEN
        bStateTimeout_Alarm := TRUE;
    END_IF;
ELSE
    rStateTimer_s := 0.0;
    bStateTimeout_Alarm := FALSE;
    nFSM_PreviousState := nFSM_CurrentState;
END_IF;

(* Interlock permissive check *)
bCellInterlock_Permissive := bAutoMode_Cmd AND bSafetyCurtain_Clear AND (NOT bEmergencyStop_Active) AND (wAlarmWord_PriorityHH = 16#0000);

IF NOT bCellInterlock_Permissive THEN
    nFSM_CurrentState := 99; (* EMERGENCY_STOP_SAFE_HOLD *)
END_IF;

CASE nFSM_CurrentState OF
    (* ------------------------------------------------------------- *)
    (* STATE 0: CELL INITIALIZATION & AXIS HOMING                    *)
    (* ------------------------------------------------------------- *)
    0:
        rStateTimeout_s := 30.0;
        bRobot_StartCycle_Cmd := FALSE;
        bInfeedPusher_Extend_Cmd := FALSE;
        bSlipSheet_Dispense_Cmd := FALSE;
        bFilm_UnrollFeed_Cmd := FALSE;
        bFilm_CutKnife_Cmd := FALSE;
        bFilm_SealingBar_Cmd := FALSE;
        bBottomUndercut_Tuck_Cmd := FALSE;
        bOutfeedConveyor_Run_Cmd := FALSE;
        rInfeedConveyor_Speed_mps := 0.0;
        rTurntable_SpeedCmd_rpm := 0.0;
        rHood_CarriageSpeed_mms := 0.0;
        rFinger_ExpandVel_mms := 0.0;
        
        IF bCellInterlock_Permissive AND bPalletInTurntable_PE THEN
            diCurrentLayer_Num := 0;
            rCycleTime_Actual_s := 0.0;
            bLayerComplete_Flag := FALSE;
            bPalletComplete_Flag := FALSE;
            bHoodApplied_Flag := FALSE;
            nFSM_CurrentState := 10; (* Transition to INFEED_CARTON_COLLECTION *)
        END_IF;

    (* ------------------------------------------------------------- *)
    (* STATE 10: INFEED CARTON METERING & COLLATION TABLE GROUPING   *)
    (* ------------------------------------------------------------- *)
    10:
        rStateTimeout_s := 40.0;
        rInfeedConveyor_Speed_mps := 0.85; (* Metering conveyor run at 0.85 m/s *)
        rCycleTime_Actual_s := rCycleTime_Actual_s + tScanTime_s;
        
        (* Check if required row of cartons is collated on buffer table *)
        IF bVoted_CartonInfeed THEN
            (* Activate pneumatic pusher to transfer carton row into collation matrix *)
            bInfeedPusher_Extend_Cmd := TRUE;
            IF rStateTimer_s > 0.80 THEN
                bInfeedPusher_Extend_Cmd := FALSE;
                rInfeedConveyor_Speed_mps := 0.0;
                nFSM_CurrentState := 20; (* Transition to ROBOT_LAYER_PATTERN_BUILD *)
            END_IF;
        ELSE
            bInfeedPusher_Extend_Cmd := FALSE;
        END_IF;

    (* ------------------------------------------------------------- *)
    (* STATE 20: 4-AXIS ROBOT VACUUM GRIP & LAYER PATTERN FORMATION  *)
    (* ------------------------------------------------------------- *)
    20:
        rStateTimeout_s := 55.0;
        rCycleTime_Actual_s := rCycleTime_Actual_s + tScanTime_s;
        
        (* Engage 4-zone vacuum gripper cups *)
        bGripper_VacZone1_En := TRUE;
        bGripper_VacZone2_En := TRUE;
        bGripper_VacZone3_En := TRUE;
        bGripper_VacZone4_En := TRUE;
        bGripper_Blowoff_Pulse := FALSE;
        
        (* Trigger robot motion trajectory once vacuum seal is confirmed (< -650 mbar) *)
        IF rVoted_VacPress_mbar < -650.0 THEN
            bRobot_StartCycle_Cmd := TRUE;
            
            (* Await robot completion signal at layer target position *)
            IF bRobot_TargetReached AND (NOT bRobot_InMotion) THEN
                (* Pulse blow-off to release cartons onto pallet bed *)
                bGripper_VacZone1_En := FALSE;
                bGripper_VacZone2_En := FALSE;
                bGripper_VacZone3_En := FALSE;
                bGripper_VacZone4_En := FALSE;
                bGripper_Blowoff_Pulse := TRUE;
                
                bRobot_StartCycle_Cmd := FALSE;
                diCurrentLayer_Num := diCurrentLayer_Num + 1;
                bLayerComplete_Flag := TRUE;
                
                (* Check if slip-sheet is required (every 3rd layer) *)
                IF (diCurrentLayer_Num MOD 3) = 0 AND diCurrentLayer_Num < 10 THEN
                    nFSM_CurrentState := 30; (* Intermediate slip sheet *)
                ELSIF diCurrentLayer_Num >= 8 THEN
                    (* Pallet stacking full (8 layers completed) *)
                    bPalletComplete_Flag := TRUE;
                    nFSM_CurrentState := 40; (* Transition to PALLET_DISCHARGE_TRANSFER *)
                ELSE
                    nFSM_CurrentState := 10; (* Next layer collection *)
                END_IF;
            END_IF;
        ELSE
            bRobot_StartCycle_Cmd := FALSE;
        END_IF;

    (* ------------------------------------------------------------- *)
    (* STATE 30: INTERMEDIATE SLIP-SHEET PICK & DISPENSE             *)
    (* ------------------------------------------------------------- *)
    30:
        rStateTimeout_s := 25.0;
        rCycleTime_Actual_s := rCycleTime_Actual_s + tScanTime_s;
        bSlipSheet_Dispense_Cmd := TRUE;
        
        IF rStateTimer_s > 4.5 THEN
            bSlipSheet_Dispense_Cmd := FALSE;
            nFSM_CurrentState := 10; (* Return to carton collation for subsequent layer *)
        END_IF;

    (* ------------------------------------------------------------- *)
    (* STATE 40: PALLET TURNTABLE INDEXING & HOODER TRANSFER         *)
    (* ------------------------------------------------------------- *)
    40:
        rStateTimeout_s := 35.0;
        rCycleTime_Actual_s := rCycleTime_Actual_s + tScanTime_s;
        bGripper_Blowoff_Pulse := FALSE;
        
        (* Slow turntable rotation to square pallet relative to hooder entry *)
        IF ABS(rTurntable_RotAngle_deg - 0.0) > 1.5 THEN
            rTurntable_SpeedCmd_rpm := 4.0;
        ELSE
            rTurntable_SpeedCmd_rpm := 0.0;
            (* Turntable aligned: initiate stretch hood prep *)
            nFSM_CurrentState := 50; (* Transition to STRETCH_HOOD_MEASURE_UNROLL *)
        END_IF;

    (* ------------------------------------------------------------- *)
    (* STATE 50: STRETCH HOOD FILM MEASUREMENT & GUSSET UNROLLING    *)
    (* ------------------------------------------------------------- *)
    50:
        rStateTimeout_s := 30.0;
        rCycleTime_Actual_s := rCycleTime_Actual_s + tScanTime_s;
        
        (* Enable motorized traction rollers to unroll film proportional to stack height *)
        bFilm_UnrollFeed_Cmd := TRUE;
        
        (* Calculate target unroll length = Stack Height + 350 mm top overlap *)
        IF rStateTimer_s > 3.2 THEN
            bFilm_UnrollFeed_Cmd := FALSE;
            (* Activate ultrasonic top transverse seal bar *)
            bFilm_SealingBar_Cmd := TRUE;
            
            IF rStateTimer_s > 4.8 THEN
                (* Fire guillotine severance knife *)
                bFilm_CutKnife_Cmd := TRUE;
                IF rStateTimer_s > 5.5 THEN
                    bFilm_SealingBar_Cmd := FALSE;
                    bFilm_CutKnife_Cmd := FALSE;
                    nFSM_CurrentState := 60; (* Transition to STRETCH_HOOD_PRE_EXPAND *)
                END_IF;
            END_IF;
        END_IF;

    (* ------------------------------------------------------------- *)
    (* STATE 60: 4-CORNER FINGER TRANSVERSE & LONGITUDINAL EXPANSION *)
    (* ------------------------------------------------------------- *)
    60:
        rStateTimeout_s := 25.0;
        rCycleTime_Actual_s := rCycleTime_Actual_s + tScanTime_s;
        
        (* Command hydraulic/pneumatic 4-finger expanders outward *)
        rFinger_ExpandVel_mms := vecControl_u[3]; (* Modulated by MPC *)
        
        (* Target envelope expansion achieved (1250 x 1050 mm) *)
        IF rFinger_ExpandSpanX_mm >= 1200.0 AND rFinger_ExpandSpanY_mm >= 1000.0 THEN
            rFinger_ExpandVel_mms := 0.0;
            nFSM_CurrentState := 70; (* Transition to HOOD_DOWNWARD_PULL_APPLY *)
        END_IF;

    (* ------------------------------------------------------------- *)
    (* STATE 70: HOOD VERTICAL SLEEVE DESCENT & ELASTIC APPLICATION  *)
    (* ------------------------------------------------------------- *)
    70:
        rStateTimeout_s := 40.0;
        rCycleTime_Actual_s := rCycleTime_Actual_s + tScanTime_s;
        
        (* Descend carriage over the stationary pallet stack *)
        rHood_CarriageSpeed_mms := vecControl_u[4]; (* Velocity guided by MPC S-curve *)
        
        (* When carriage reaches pallet base level (approx 120 mm above floor) *)
        IF rHood_CarriageHeight_mm <= 160.0 THEN
            rHood_CarriageSpeed_mms := 0.0;
            nFSM_CurrentState := 80; (* Transition to BOTTOM_UNDERCUT_LOCK_CUT *)
        END_IF;

    (* ------------------------------------------------------------- *)
    (* STATE 80: BOTTOM UNDERCUT TUCK UNDER PALLET DECK BOARDS       *)
    (* ------------------------------------------------------------- *)
    80:
        rStateTimeout_s := 20.0;
        rCycleTime_Actual_s := rCycleTime_Actual_s + tScanTime_s;
        
        (* Extend tuck fingers under wooden pallet wings for sea-container lock *)
        bBottomUndercut_Tuck_Cmd := TRUE;
        
        IF rStateTimer_s > 2.5 THEN
            bBottomUndercut_Tuck_Cmd := FALSE;
            (* Retract 4-corner fingers inwards to release film tension onto wood *)
            rFinger_ExpandVel_mms := -60.0;
            IF rStateTimer_s > 4.0 THEN
                rFinger_ExpandVel_mms := 0.0;
                bHoodApplied_Flag := TRUE;
                nFSM_CurrentState := 90; (* Transition to PALLET_OUTFEED_WRAP_COMPLETE *)
            END_IF;
        END_IF;

    (* ------------------------------------------------------------- *)
    (* STATE 90: PALLET OUTFEED DISCHARGE CONVEYOR ROLL-OFF          *)
    (* ------------------------------------------------------------- *)
    90:
        rStateTimeout_s := 35.0;
        rCycleTime_Actual_s := rCycleTime_Actual_s + tScanTime_s;
        
        (* Return carriage to overhead home position (2800 mm) *)
        IF rHood_CarriageHeight_mm < 2750.0 THEN
            rHood_CarriageSpeed_mms := -250.0; (* Negative indicates upward ascent *)
        ELSE
            rHood_CarriageSpeed_mms := 0.0;
        END_IF;
        
        (* Run outfeed discharge conveyor if exit photoeye is clear *)
        IF bPalletOutfeedClear_PE THEN
            bOutfeedConveyor_Run_Cmd := TRUE;
            IF rStateTimer_s > 6.0 THEN
                bOutfeedConveyor_Run_Cmd := FALSE;
                diCompletedPallets_Count := diCompletedPallets_Count + 1;
                rCycleTime_Target_s := rCycleTime_Actual_s;
                nFSM_CurrentState := 0; (* Cycle complete: return to INIT for next pallet *)
            END_IF;
        ELSE
            bOutfeedConveyor_Run_Cmd := FALSE;
        END_IF;

    (* ------------------------------------------------------------- *)
    (* STATE 99: EMERGENCY SAFE STOP & ACTUATOR HOLD                 *)
    (* ------------------------------------------------------------- *)
    99:
        bRobot_StartCycle_Cmd := FALSE;
        bInfeedPusher_Extend_Cmd := FALSE;
        bSlipSheet_Dispense_Cmd := FALSE;
        bFilm_UnrollFeed_Cmd := FALSE;
        bFilm_CutKnife_Cmd := FALSE;
        bFilm_SealingBar_Cmd := FALSE;
        bBottomUndercut_Tuck_Cmd := FALSE;
        bOutfeedConveyor_Run_Cmd := FALSE;
        rInfeedConveyor_Speed_mps := 0.0;
        rTurntable_SpeedCmd_rpm := 0.0;
        rHood_CarriageSpeed_mms := 0.0;
        rFinger_ExpandVel_mms := 0.0;
        
        (* Maintain vacuum hold to prevent carton drop while robot is stopped mid-air *)
        IF diCurrentLayer_Num > 0 AND bRobot_InMotion THEN
            bGripper_VacZone1_En := TRUE;
            bGripper_VacZone2_En := TRUE;
            bGripper_VacZone3_En := TRUE;
            bGripper_VacZone4_En := TRUE;
        ELSE
            bGripper_VacZone1_En := FALSE;
            bGripper_VacZone2_En := FALSE;
            bGripper_VacZone3_En := FALSE;
            bGripper_VacZone4_En := FALSE;
        END_IF;
        
        IF bAlarmReset_PB AND bCellInterlock_Permissive THEN
            nFSM_CurrentState := 0;
        END_IF;
END_CASE;
"""
    sections.append(sec10)

    # ==========================================
    # SECTION 11: OUTPUT CLAMPING & END BLOCK
    # ==========================================
    sec11 = """(* ========================================================================= *)
(* PHASE 9: ACTUATOR OUTPUT HARDWARE CLAMPING & SAFETY INTERLOCK ENFORCEMENT  *)
(* ========================================================================= *)
(* Robot Speed Scale Clamping [0.0 .. 100.0 %] *)
IF rRobot_SpeedScale_Pct < 10.0 THEN
    rRobot_SpeedScale_Pct := 10.0;
ELSIF rRobot_SpeedScale_Pct > 100.0 THEN
    rRobot_SpeedScale_Pct := 100.0;
END_IF;

(* Robot Acceleration Scale Clamping [0.0 .. 100.0 %] *)
IF rRobot_AccelScale_Pct < 10.0 THEN
    rRobot_AccelScale_Pct := 10.0;
ELSIF rRobot_AccelScale_Pct > 100.0 THEN
    rRobot_AccelScale_Pct := 100.0;
END_IF;

(* Hood Carriage Speed Clamping [-300.0 .. 350.0 mm/s] *)
IF rHood_CarriageSpeed_mms > 350.0 THEN
    rHood_CarriageSpeed_mms := 350.0;
ELSIF rHood_CarriageSpeed_mms < -300.0 THEN
    rHood_CarriageSpeed_mms := -300.0;
END_IF;

(* 4-Corner Finger Expansion Velocity Clamping [-100.0 .. 80.0 mm/s] *)
IF rFinger_ExpandVel_mms > 80.0 THEN
    rFinger_ExpandVel_mms := 80.0;
ELSIF rFinger_ExpandVel_mms < -100.0 THEN
    rFinger_ExpandVel_mms := -100.0;
END_IF;

(* Turntable Speed Command Clamping [0.0 .. 12.0 rpm] *)
IF rTurntable_SpeedCmd_rpm > 12.0 THEN
    rTurntable_SpeedCmd_rpm := 12.0;
ELSIF rTurntable_SpeedCmd_rpm < 0.0 THEN
    rTurntable_SpeedCmd_rpm := 0.0;
END_IF;

(* Infeed Conveyor Speed Clamping [0.0 .. 1.5 m/s] *)
IF rInfeedConveyor_Speed_mps > 1.5 THEN
    rInfeedConveyor_Speed_mps := 1.5;
ELSIF rInfeedConveyor_Speed_mps < 0.0 THEN
    rInfeedConveyor_Speed_mps := 0.0;
END_IF;

END_FUNCTION_BLOCK
"""
    sections.append(sec11)

    return "\n".join(sections)

if __name__ == "__main__":
    code = build_packaging_block()
    print(f"Total ST code length: {len(code)} characters")
