# -*- coding: utf-8 -*-
"""
Part 1 of FB_Packaging_Corrugator_SingleFacer_FlyingShear
Contains: Title Block, Detailed Engineering Documentation, VAR_INPUT, VAR_OUTPUT, VAR declarations.
"""

def get_part1():
    return '''FUNCTION_BLOCK FB_Packaging_Corrugator_SingleFacer_FlyingShear
(* =====================================================================================================================
 * LUMINA CYBER-PHYSICAL AUTOMATION ENGINE - SYNTHETIC DATASET V7 MAX-PERSONA
 * COMMERCIAL INDUSTRIAL SECTOR : Paper Converting & Heavy Packaging Machinery
 * SYSTEM                       : Continuous High-Speed 400 m/min Corrugated Cardboard Production Line
 *                                Integrating Wet-End Single Facer (Flute A/B/C Rolls, 25 bar Nip Pressure,
 *                                Starch Film Applicator Gap Servo 0.15 - 0.35 mm with Viscosity/Temp Compensation),
 *                                Bridge Reservoir Web Accumulator & Festoon Tension Balancing (Ultrasonic Catenary Loop),
 *                                Double-Backer Multi-Section Steam Chest Temperature Profile (160 deg C - 185 deg C
 *                                with Dynamic Air-Cushion Ballast Shoes & Warpage/Curl Prediction),
 *                                and Dry-End High-Speed Flying Rotary Slitter / Scorer with Servo Cutoff Synchronization
 *                                (< +/- 0.5 mm Cut Length Accuracy at 400 m/min Web Speed).
 *
 * DETAILED CYBER-PHYSICAL PROCESS FORMULATIONS & THEORY OF OPERATION:
 * 1. Single Facer Medium Fluting & Starch Adhesive Gelatinization Kinetics:
 *    Fluting paper medium is plasticized by saturated steam pre-heaters and high-pressure steam showers at 175 deg C - 185 deg C,
 *    reducing lignocellulosic modulus of elasticity to prevent fiber fracturing during high-speed labyrinth meshing.
 *    Flute geometry parameters:
 *      - Flute A: Flute height h_f = 4.70 mm, Flute pitch p_f = 8.60 mm, Take-up factor alpha_f = 1.540
 *      - Flute B: Flute height h_f = 2.50 mm, Flute pitch p_f = 6.50 mm, Take-up factor alpha_f = 1.320
 *      - Flute C: Flute height h_f = 3.60 mm, Flute pitch p_f = 7.80 mm, Take-up factor alpha_f = 1.430
 *      - Flute E: Flute height h_f = 1.15 mm, Flute pitch p_f = 3.50 mm, Take-up factor alpha_f = 1.270
 *    Fluting medium web consumption velocity: v_medium = v_line * alpha_f.
 *    Starch adhesive rheology follows modified Stein-Hall non-Newtonian shear-thinning behavior:
 *      mu_starch(T, gamma_dot) = mu_0 * exp(E_a / (R * (T + 273.15))) * (1.0 + k_shear * gamma_dot^(n - 1))
 *    Where Stein-Hall viscosity is calibrated in cup seconds (35 to 55 s), gelatinization onset temperature T_gel = 62.0 to 68.0 deg C.
 *    Hydrodynamic film splitting between applicator roll and doctor roll follows the Taylor liquid bridge lubrication model:
 *      h_film = C_roll * Gap_servo * ((mu_starch * v_roll) / sigma_surf)^(1.0 / 3.0)
 *    Starch coat weight dry target: W_dry = 12.0 to 18.0 g/m2 of fluting tip area. Dynamic gap servo trim:
 *      Delta_gap = K_visc * (Visc_actual - Visc_ref) + K_temp * (T_glue - T_ref) + K_speed * (v_line - v_ref).
 *
 * 2. Bridge Reservoir Web Accumulator & Festoon Catenary Loop Mass Balance:
 *    The elevated bridge web accumulator buffers single-face corrugated web between the Single Facer (intermittent flying splice)
 *    and the Double-Backer (continuous traction). Buffer length rate of change:
 *      d(L_bridge) / dt = v_single_facer - v_double_backer
 *    Ultrasonic catenary sensors measure vertical sag y_sag across the festoon suspension span L_span:
 *      y_sag = (H_tension / (rho_board * g * W_web)) * (cosh((rho_board * g * W_web * L_span) / (2.0 * H_tension)) - 1.0)
 *    A dynamic vacuum suction brake table provides regulated frictional counter-tension H_tension = mu_vac * Delta_P_vac * A_table.
 *
 * 3. Double-Backer Multi-Section Steam Chest Thermal Profiling & Board Warpage/Curl Mechanics:
 *    The double-backer bonds the bottom liner to the glued flutes of the single-face web via three independently controlled steam zones:
 *      - Zone 1 (Initial Gelatinization): T_sb1 = 160.0 to 170.0 deg C, high heat flux to achieve gelatinization within 1.2 s.
 *      - Zone 2 (Intensive Moisture Evaporation): T_sb2 = 175.0 to 185.0 deg C, vaporizing excess water from starch glue carrier.
 *      - Zone 3 (Setting & Stress Relief): T_sb3 = 165.0 to 175.0 deg C, controlled thermal conditioning.
 *    Pneumatic air-cushion ballast shoes apply distributed contact pressure P_ballast = 0.20 to 1.80 bar against the top cotton belt.
 *    Cardboard warpage (upward curl vs downward curl) is driven by the differential moisture and thermal contraction:
 *      Curvature_kappa = (alpha_hygro * (M_top - M_bottom) + alpha_thermal * (T_top - T_bottom)) / H_board_total
 *    Warp minimization feedback dynamically redistributes steam chest heat flux and ballast shoe air pressure.
 *
 * 4. Dry-End High-Speed Flying Rotary Slitter/Scorer & Servo Cutoff Shear Synchronization:
 *    Continuous web travels at v_line up to 400.0 m/min (6.667 m/s).
 *    The rotary cutoff shear comprises twin helical blade cylinders of circumference C_knife = 2.0 * pi * R_knife (e.g., 1000.0 mm).
 *    Sheet length control (target cutoff length L_target = 400.0 mm to 3500.0 mm):
 *      When L_target = C_knife: Constant angular velocity omega_knife = v_line / R_knife.
 *      When L_target > C_knife: Knife rotates through cut zone at synchronous speed, then decelerates to a dwell velocity, then re-accelerates.
 *      When L_target < C_knife: Knife accelerates above synchronous speed after cut zone to complete revolution earlier.
 *    Electronic camming (E-CAM) profile utilizes a 5th-order polynomial motion law inside the non-cutting sector:
 *      theta(t) = a_0 + a_1*t + a_2*t^2 + a_3*t^3 + a_4*t^4 + a_5*t^5
 *    Boundary conditions guarantee zero jerk at entry/exit of the synchronous cutting sector (+/- 12.0 deg around bottom dead center).
 *    Cutoff registration sensor measures sheet cutoff error Delta_L. Phase compensation trim:
 *      Delta_theta_corr = K_phase * Delta_L + K_int * Integral(Delta_L dt).
 *
 * 5. Discrete State-Space Model & Receding-Horizon Model Predictive Control (MPC):
 *    State vector x in R^8:
 *      x[1] = Upper corrugating roll surface temperature T_roll_upper [deg C]
 *      x[2] = Single-facer starch film thickness h_glue_film [um]
 *      x[3] = Bridge web accumulator buffer length L_bridge_accum [m]
 *      x[4] = Double-backer Zone 1 steam chest plate temp T_chest_zone1 [deg C]
 *      x[5] = Double-backer Zone 2 steam chest plate temp T_chest_zone2 [deg C]
 *      x[6] = Combined board residual moisture content M_board_moist [%]
 *      x[7] = Dry-end web entry tension F_web_tension [N]
 *      x[8] = Flying cutoff shear angular synchronization error Delta_theta_knife [mrad]
 *    Actuation vector u in R^4:
 *      u[1] = Single-facer steam modulating valve position [0.0 to 100.0 %]
 *      u[2] = Starch applicator gap servo position trim [-50.0 to +50.0 um]
 *      u[3] = Double-backer steam chest control valve position [0.0 to 100.0 %]
 *      u[4] = Flying shear servo velocity trim command [-15.0 to +15.0 m/min]
 *    Discrete state propagation: x[k+1] = A * x[k] + B * u[k], y[k] = C * x[k] + D * u[k].
 *    Receding-horizon quadratic cost function:
 *      J = Sum_{j=1..Np} (x[k+j] - x_ref)^T * Q * (x[k+j] - x_ref) + Sum_{j=0..Nc-1} Delta_u[k+j]^T * R * Delta_u[k+j] + Terminal_P
 *    Solved via Projected Gradient Descent with box constraints on actuator travel and slew limits.
 *
 * 6. Triple Modular Redundancy (TMR 2oo3) Sensor Architecture:
 *    Seven critical process sensor triplets voted every PLC scan (10 ms):
 *      - Triplet 1: Upper corrugating roll RTDs [deg C]
 *      - Triplet 2: Lower corrugating roll RTDs [deg C]
 *      - Triplet 3: Steam supply header pressure transmitters [bar]
 *      - Triplet 4: Bridge catenary loop ultrasonic sag transmitters [mm]
 *      - Triplet 5: Double-backer entry web tension load cells [N]
 *      - Triplet 6: Corrugator master line speed encoders [m/min]
 *      - Triplet 7: Flying shear knife angular position resolvers [deg]
 *    Pairwise discrepancy check with discrepancy timers (accumulating over 150 ms) and bumpless degradation.
 *
 * 7. ISA-18.2 Process Alarm Engine:
 *    Multi-tier alarm classification: High-High (HH), High (H), Low (L), Low-Low (LL), Rate of Change (ROC).
 *    Deadband hysteresis filtering and 45-second unacknowledged escalation logic.
 *
 * 8. 12-Stage Deterministic Production Finite State Machine (FSM):
 *    STATE 1 : Roll Pre-Heat & Thermal Crowning Soak
 *    STATE 2 : Glue Line Priming & Starch Viscosity Conditioning
 *    STATE 3 : Paper Web Threading & Vacuum Table Latch
 *    STATE 4 : Slow Inching & First Flute Formation (25 m/min)
 *    STATE 5 : Speed Acceleration Ramp (to 150 m/min, 25 bar nip clamp)
 *    STATE 6 : Bridge Festoon Accumulation & Double-Backer Pre-Heat
 *    STATE 7 : Continuous High-Speed Corrugating (up to 400 m/min, full MPC)
 *    STATE 8 : Order Changeover Flying Splice & Zero-Gap Slitter Index
 *    STATE 9 : Glue Dam Flush & Starch Scraper Rinse
 *    STATE 10: Mechanical Roll Retraction & Nip De-clamping
 *    STATE 11: Controlled Cooldown & Thermal Sag Slow Spin
 *    STATE 12: Emergency Web Wrap-Up Fast Stop (< 100 ms trip)
 * =====================================================================================================================
 *)
VAR_INPUT
    (* === 2oo3 TMR PROCESS SENSOR TRIPLETS === *)
    rT_RollUpper_ChA                    : REAL;     (* Single-facer upper corrugating roll surface temp RTD channel A [deg C] *)
    rT_RollUpper_ChB                    : REAL;     (* Single-facer upper corrugating roll surface temp RTD channel B [deg C] *)
    rT_RollUpper_ChC                    : REAL;     (* Single-facer upper corrugating roll surface temp RTD channel C [deg C] *)

    rT_RollLower_ChA                    : REAL;     (* Single-facer lower corrugating roll surface temp RTD channel A [deg C] *)
    rT_RollLower_ChB                    : REAL;     (* Single-facer lower corrugating roll surface temp RTD channel B [deg C] *)
    rT_RollLower_ChC                    : REAL;     (* Single-facer lower corrugating roll surface temp RTD channel C [deg C] *)

    rP_SteamSupply_ChA                  : REAL;     (* Steam supply header pressure transmitter channel A [bar] *)
    rP_SteamSupply_ChB                  : REAL;     (* Steam supply header pressure transmitter channel B [bar] *)
    rP_SteamSupply_ChC                  : REAL;     (* Steam supply header pressure transmitter channel C [bar] *)

    rPos_BridgeLoopSag_ChA              : REAL;     (* Bridge catenary accumulator ultrasonic loop sag channel A [mm] *)
    rPos_BridgeLoopSag_ChB              : REAL;     (* Bridge catenary accumulator ultrasonic loop sag channel B [mm] *)
    rPos_BridgeLoopSag_ChC              : REAL;     (* Bridge catenary accumulator ultrasonic loop sag channel C [mm] *)

    rF_WebTensionDB_ChA                 : REAL;     (* Double-backer entry web tension load cell channel A [N] *)
    rF_WebTensionDB_ChB                 : REAL;     (* Double-backer entry web tension load cell channel B [N] *)
    rF_WebTensionDB_ChC                 : REAL;     (* Double-backer entry web tension load cell channel C [N] *)

    rV_MasterLineSpeed_ChA              : REAL;     (* Corrugator master line speed pulse encoder channel A [m/min] *)
    rV_MasterLineSpeed_ChB              : REAL;     (* Corrugator master line speed pulse encoder channel B [m/min] *)
    rV_MasterLineSpeed_ChC              : REAL;     (* Corrugator master line speed pulse encoder channel C [m/min] *)

    rPos_ShearKnifeAngle_ChA            : REAL;     (* Flying rotary cutoff shear knife resolver angle channel A [deg] *)
    rPos_ShearKnifeAngle_ChB            : REAL;     (* Flying rotary cutoff shear knife resolver angle channel B [deg] *)
    rPos_ShearKnifeAngle_ChC            : REAL;     (* Flying rotary cutoff shear knife resolver angle channel C [deg] *)

    (* === PRODUCTION RECIPE & PROCESS SETPOINTS === *)
    rV_TargetLineSpeed_Setpt            : REAL;     (* Target corrugator production line speed setpoint [m/min] *)
    rL_TargetSheetCutoff_Setpt          : REAL;     (* Target dry-end corrugated sheet cutoff length setpoint [mm] *)
    nFluteType_Selector                 : INT;      (* Active flute profile selection: 1=A-Flute, 2=B-Flute, 3=C-Flute, 4=E-Flute [-] *)
    rW_MediumPaperGrammage              : REAL;     (* Fluting medium paper basis weight [g/m2] *)
    rW_LinerPaperGrammage               : REAL;     (* Linerboard basis weight [g/m2] *)
    rVisc_StarchSteinHall_Sec           : REAL;     (* Inline starch adhesive viscosity measurement in Stein-Hall cup seconds [s] *)
    rT_StarchGelatinization_Setpt       : REAL;     (* Starch adhesive target gelatinization onset temperature [deg C] *)
    rP_NipHydraulicPressure_Setpt       : REAL;     (* Single-facer corrugating roll hydraulic nip pressure setpoint [bar] *)
    rT_SteamChestZone1_Setpt            : REAL;     (* Double-backer steam chest zone 1 temperature setpoint [deg C] *)
    rT_SteamChestZone2_Setpt            : REAL;     (* Double-backer steam chest zone 2 temperature setpoint [deg C] *)
    rT_SteamChestZone3_Setpt            : REAL;     (* Double-backer steam chest zone 3 temperature setpoint [deg C] *)
    rP_BallastShoePressure_Setpt        : REAL;     (* Double-backer pneumatic air-cushion ballast shoe loading pressure [bar] *)
    rGap_StarchApplicatorNominal_Setpt  : REAL;     (* Starch applicator gap servo nominal mechanical setpoint [mm] *)

    (* === DISCRETE SUPERVISORY & SAFETY COMMANDS === *)
    bOrderChangeFlyingSplice_Cmd        : BOOL;     (* Dry-end automated order change flying splice trigger flag [-] *)
    bEmergencyStop_Trip                 : BOOL;     (* Hardware E-stop or safety laser scanner trip input [-] *)
    bFaultReset_Cmd                     : BOOL;     (* Master operator push-button fault reset command [-] *)
    bSystemEnable_Cmd                   : BOOL;     (* Master line production run permissives satisfied [-] *)
    bGlueFlushPurge_Cmd                 : BOOL;     (* Automated glue dam and applicator pan wash cycle request [-] *)
    bRollRetraction_Cmd                 : BOOL;     (* Hydraulic corrugating roll retraction command [-] *)
    bAutoSpeedTrack_Enable              : BOOL;     (* Enable automatic closed-loop speed tracking and ramp rate governor [-] *)
    bMpcEnable_Cmd                      : BOOL;     (* Enable multivariable Receding-Horizon Model Predictive Controller [-] *)
    rT_CycleTime_Sec                    : REAL;     (* PLC deterministic scan task period in seconds [s] *)
END_VAR

VAR_OUTPUT
    (* === PROCESS ACTUATOR ANALOG COMMANDS === *)
    rCmd_SingleFacerDrive_Speed         : REAL;     (* Single-facer master AC inverter motor speed command [m/min] *)
    rCmd_BridgeConveyorDrive_Speed      : REAL;     (* Bridge reservoir web accumulator belt speed command [m/min] *)
    rCmd_DoubleBackerDrive_Speed        : REAL;     (* Double-backer main traction drive speed command [m/min] *)
    rCmd_FlyingShearKnife_ServoVelocity : REAL;     (* Flying rotary cutoff knife servo drive velocity feedforward [rpm] *)
    rCmd_FlyingShearKnife_ServoPosition : REAL;     (* Flying rotary cutoff knife servo drive angular position command [deg] *)
    rCmd_StarchApplicatorGap_ServoPos   : REAL;     (* Precision motorized glue applicator gap servo target position [mm] *)
    rCmd_NipHydraulicPropValve_Pct      : REAL;     (* Single-facer nip hydraulic proportional pressure control valve [0.0 to 100.0 %] *)
    rCmd_SteamChestZone1_Valve_Pct      : REAL;     (* Double-backer steam chest zone 1 modulating control valve [0.0 to 100.0 %] *)
    rCmd_SteamChestZone2_Valve_Pct      : REAL;     (* Double-backer steam chest zone 2 modulating control valve [0.0 to 100.0 %] *)
    rCmd_SteamChestZone3_Valve_Pct      : REAL;     (* Double-backer steam chest zone 3 modulating control valve [0.0 to 100.0 %] *)
    rCmd_BallastShoePneumatic_Reg_bar   : REAL;     (* Dynamic ballast shoe pneumatic proportional pressure regulator [bar] *)
    rCmd_BridgeFestoonSuctionBrake_Pct  : REAL;     (* Bridge web tension suction brake table vacuum modulating valve [%] *)

    (* === DISCRETE ACTUATION & SAFETY INTERLOCKS === *)
    bCmd_FlyingSpliceNipEngage          : BOOL;     (* Dry-end flying splice nip roll engage solenoid command [-] *)
    bCmd_SlitterScorerIndexShift        : BOOL;     (* Dry-end tandem rotary slitter/creaser robotic positioning trigger [-] *)
    bCmd_SteamHeaderIsolationValve_Open : BOOL;     (* High-pressure main steam isolation safety valve open permissive [-] *)
    bCmd_RollRetractHydraulicCyl_Retract: BOOL;     (* Single-facer hydraulic cylinder retract solenoid valve command [-] *)
    bCmd_GlueDamWashSolenoid_Open       : BOOL;     (* Starch glue pan automatic flush water wash valve solenoid [-] *)
    bCmd_EmergencyBrakeEngage           : BOOL;     (* High-speed pneumatic caliper safety emergency disc brake engage [-] *)
    bCmd_WebWrapUpDetectorTripped       : BOOL;     (* Corrugating roll optical wrap-up jam fast interlock status [-] *)

    (* === REAL-TIME PROCESS OBSERVATIONS & METRICS === *)
    rErr_SheetLengthCutoff_mm           : REAL;     (* High-speed sheet cutoff length error Delta_L [mm] *)
    rCalc_StarchFilmCoatWeight_gsm      : REAL;     (* Estimated dry starch film coat weight on fluting tips [g/m2] *)
    rCalc_BoardWarpageCurlIndex_Pct     : REAL;     (* Estimated corrugated board warp/curl severity index [-100.0 to +100.0 %] *)
    rCalc_BridgeAccumulatedWebLength_m  : REAL;     (* Accumulated single-face web length currently buffered on bridge [m] *)
    rCalc_CorrugatorThroughput_sqm_h    : REAL;     (* Real-time corrugator production area throughput [m2/h] *)
    rCalc_StarchGelatinizationDegree_Pct: REAL;     (* Estimated starch adhesive gelatinization completion percentage [%] *)
    rAct_WebTensionEntryDB_N            : REAL;     (* Voted real-time web tension entering double-backer [N] *)
    rAct_LineSpeedMaster_m_min          : REAL;     (* Voted master line speed [m/min] *)
    rAct_UpperRollTempVoted_degC        : REAL;     (* Voted upper corrugating roll surface temperature [deg C] *)
    rAct_LowerRollTempVoted_degC        : REAL;     (* Voted lower corrugating roll surface temperature [deg C] *)
    rAct_BridgeSagVoted_mm              : REAL;     (* Voted bridge festoon catenary loop sag depth [mm] *)

    (* === SYSTEM STATUS & DIAGNOSTIC WORDS === *)
    dwStatusWord_State                  : DWORD;    (* Active FSM state, sequencing flags, and operational status bitmask *)
    dwStatusWord_Alarms_Critical        : DWORD;    (* ISA-18.2 Priority 1 & 2 Critical and Emergency Alarm bitmask *)
    dwStatusWord_Alarms_Warning         : DWORD;    (* ISA-18.2 Priority 3 Warning and Process Deviation bitmask *)
    dwStatusWord_TMR_Health             : DWORD;    (* 2oo3 Triple Modular Redundancy sensor triplet health bitmask *)
    dwDiagnosticWord_MPC                : DWORD;    (* Model Predictive Controller status, iterations, and active constraint flags *)
END_VAR

VAR
    (* === 12-STAGE PRODUCTION FINITE STATE MACHINE CONSTANTS === *)
    cSTATE_01_ROLL_PREHEAT              : INT := 1;  (* State 1: Roll Pre-Heat & Thermal Crowning Soak *)
    cSTATE_02_GLUE_LINE_PRIME           : INT := 2;  (* State 2: Glue Line Priming & Starch Viscosity Conditioning *)
    cSTATE_03_PAPER_WEB_THREADING       : INT := 3;  (* State 3: Paper Web Threading & Vacuum Table Latch *)
    cSTATE_04_SLOW_INCHING              : INT := 4;  (* State 4: Slow Inching & First Flute Formation (25 m/min) *)
    cSTATE_05_SPEED_ACCELERATION_RAMP   : INT := 5;  (* State 5: Speed Acceleration Ramp (to 150 m/min, 25 bar nip clamp) *)
    cSTATE_06_BRIDGE_ACCUMULATION       : INT := 6;  (* State 6: Bridge Festoon Accumulation & Double-Backer Pre-Heat *)
    cSTATE_07_CONTINUOUS_HIGH_SPEED     : INT := 7;  (* State 7: Continuous High-Speed Corrugating (up to 400 m/min, full MPC) *)
    cSTATE_08_FLYING_SPLICE_CHANGEOVER  : INT := 8;  (* State 8: Order Changeover Flying Splice & Zero-Gap Slitter Index *)
    cSTATE_09_GLUE_DAM_FLUSH            : INT := 9;  (* State 9: Glue Dam Flush & Starch Scraper Rinse *)
    cSTATE_10_ROLL_RETRACTION           : INT := 10; (* State 10: Mechanical Roll Retraction & Nip De-clamping *)
    cSTATE_11_CONTROLLED_COOLDOWN       : INT := 11; (* State 11: Controlled Cooldown & Thermal Sag Slow Spin *)
    cSTATE_12_EMERGENCY_WRAPUP_STOP     : INT := 12; (* State 12: Emergency Web Wrap-Up Fast Stop (< 100 ms trip) *)

    eCorrugatorState                    : INT := 1;  (* Active FSM State Variable *)
    eCorrugatorPrevState                : INT := 1;  (* Previous FSM State Variable *)
    rStateTimer_Sec                     : REAL := 0.0; (* Time spent in current FSM state [s] *)
    bStateEntry                         : BOOL := TRUE;(* First-scan pulse flag for active state entry actions *)
    bStateTransitionReq                 : BOOL := FALSE;
    eNextState                          : INT := 1;

    (* === 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) INTERNAL STRUCTURES === *)
    (* Channel A, B, C health flags and timers for 7 triplets *)
    bHealth_RollUpper_ChA               : BOOL := TRUE;
    bHealth_RollUpper_ChB               : BOOL := TRUE;
    bHealth_RollUpper_ChC               : BOOL := TRUE;
    rTimerDisc_RollUpper                : REAL := 0.0;

    bHealth_RollLower_ChA               : BOOL := TRUE;
    bHealth_RollLower_ChB               : BOOL := TRUE;
    bHealth_RollLower_ChC               : BOOL := TRUE;
    rTimerDisc_RollLower                : REAL := 0.0;

    bHealth_SteamSupply_ChA             : BOOL := TRUE;
    bHealth_SteamSupply_ChB             : BOOL := TRUE;
    bHealth_SteamSupply_ChC             : BOOL := TRUE;
    rTimerDisc_SteamSupply              : REAL := 0.0;

    bHealth_BridgeSag_ChA               : BOOL := TRUE;
    bHealth_BridgeSag_ChB               : BOOL := TRUE;
    bHealth_BridgeSag_ChC               : BOOL := TRUE;
    rTimerDisc_BridgeSag                : REAL := 0.0;

    bHealth_WebTension_ChA              : BOOL := TRUE;
    bHealth_WebTension_ChB              : BOOL := TRUE;
    bHealth_WebTension_ChC              : BOOL := TRUE;
    rTimerDisc_WebTension               : REAL := 0.0;

    bHealth_MasterSpeed_ChA             : BOOL := TRUE;
    bHealth_MasterSpeed_ChB             : BOOL := TRUE;
    bHealth_MasterSpeed_ChC             : BOOL := TRUE;
    rTimerDisc_MasterSpeed              : REAL := 0.0;

    bHealth_KnifeAngle_ChA              : BOOL := TRUE;
    bHealth_KnifeAngle_ChB              : BOOL := TRUE;
    bHealth_KnifeAngle_ChC              : BOOL := TRUE;
    rTimerDisc_KnifeAngle               : REAL := 0.0;

    (* TMR Discrepancy Tolerance Limits *)
    cTOL_DISC_TEMP_DEGC                 : REAL := 8.5;   (* Maximum allowable RTD temperature divergence [deg C] *)
    cTOL_DISC_PRESSURE_BAR              : REAL := 1.8;   (* Maximum allowable steam pressure transmitter divergence [bar] *)
    cTOL_DISC_SAG_MM                    : REAL := 75.0;  (* Maximum allowable ultrasonic catenary sag divergence [mm] *)
    cTOL_DISC_TENSION_N                 : REAL := 120.0; (* Maximum allowable web tension load cell divergence [N] *)
    cTOL_DISC_SPEED_M_MIN               : REAL := 12.0;  (* Maximum allowable line speed encoder divergence [m/min] *)
    cTOL_DISC_ANGLE_DEG                 : REAL := 4.5;   (* Maximum allowable shear knife resolver angle divergence [deg] *)
    cTIME_DISC_MAX_TRIP_SEC             : REAL := 0.150; (* Maximum discrepancy duration before latching faulty channel [s] *)

    (* === DISCRETE STATE-SPACE MODEL MATRICES (8 States x 4 Actuators) === *)
    (* Continuous-to-discrete sampled matrices A (8x8), B (8x4), C (8x8), D (8x4) *)
    rMat_A : ARRAY[1..8, 1..8] OF REAL;
    rMat_B : ARRAY[1..8, 1..4] OF REAL;
    rMat_C : ARRAY[1..8, 1..8] OF REAL;
    rMat_D : ARRAY[1..8, 1..4] OF REAL;
    rMat_L : ARRAY[1..8, 1..8] OF REAL;  (* Luenberger observer innovation gain matrix *)

    (* State vectors: x[1..8], x_pred[1..8], x_ref[1..8], y_meas[1..8], y_est[1..8] *)
    rVec_X                              : ARRAY[1..8] OF REAL;
    rVec_X_Pred                         : ARRAY[1..8] OF REAL;
    rVec_X_Ref                          : ARRAY[1..8] OF REAL;
    rVec_Y_Meas                         : ARRAY[1..8] OF REAL;
    rVec_Y_Est                          : ARRAY[1..8] OF REAL;

    (* Actuator vector: u[1..4], u_ref[1..4], u_opt[1..4], Delta_u[1..4] *)
    rVec_U                              : ARRAY[1..4] OF REAL;
    rVec_U_Ref                          : ARRAY[1..4] OF REAL;
    rVec_U_Opt                          : ARRAY[1..4] OF REAL;
    rVec_Delta_U                        : ARRAY[1..4] OF REAL;

    (* === MODEL PREDICTIVE CONTROL (MPC) MATRICES & VECTORS === *)
    (* Quadratic cost penalty matrices: Q (8x8 state penalty), R (4x4 actuation penalty), P (8x8 terminal penalty) *)
    rMat_Q : ARRAY[1..8, 1..8] OF REAL;
    rMat_R : ARRAY[1..4, 1..4] OF REAL;
    rMat_P : ARRAY[1..8, 1..8] OF REAL;

    (* MPC solver variables *)
    rGrad_J                             : ARRAY[1..4] OF REAL;  (* Cost function gradient with respect to control increment *)
    rMpcStepSize_Alpha                  : REAL := 0.015;        (* Gradient descent line search step size *)
    nMpcMaxIter                         : INT := 12;            (* Maximum solver iterations per PLC scan *)
    rMpcCost_Current                    : REAL := 0.0;
    rMpcCost_Previous                   : REAL := 0.0;
    rU_Min                              : ARRAY[1..4] OF REAL;  (* Actuator lower box constraints *)
    rU_Max                              : ARRAY[1..4] OF REAL;  (* Actuator upper box constraints *)
    rDelta_U_Max                        : ARRAY[1..4] OF REAL;  (* Actuator maximum slew rate per scan *)

    (* === PHYSICAL CONSTANTS & INTERMEDIATE PROCESS VARIABLES === *)
    rFlutePitch_p_f                     : REAL := 7.80;  (* Active flute pitch [mm] *)
    rFluteHeight_h_f                    : REAL := 3.60;  (* Active flute height [mm] *)
    rFluteTakeUp_alpha_f                : REAL := 1.430; (* Active flute take-up consumption ratio [-] *)
    rWebWidth_m                         : REAL := 2.500; (* Machine trim web width [m] *)
    rBoardBasisWeight_Total_gsm         : REAL := 420.0; (* Total combined board basis weight [g/m2] *)

    (* Starch Adhesive Kinematics & Rheology *)
    rStarchViscosity_cP                 : REAL := 480.0; (* Converted dynamic viscosity in centipoise [cP] *)
    rGlueShearRate_inv_s                : REAL := 1850.0;(* Shear rate in applicator nip [1/s] *)
    rStarchGelDegree_Internal           : REAL := 0.0;   (* Calculated gelatinization fractional progress [0.0 to 1.0] *)
    rStarchDwellTime_Sec                : REAL := 0.0;   (* Contact dwell time under heat nip [s] *)
    rGlueFilmThickness_um               : REAL := 18.5;  (* Dynamic liquid glue film thickness [um] *)

    (* Heat Flux & Steam Chest Mechanics *)
    rQ_SteamChestZone1_kW               : REAL := 0.0;   (* Zone 1 thermal heat transfer rate [kW] *)
    rQ_SteamChestZone2_kW               : REAL := 0.0;   (* Zone 2 thermal heat transfer rate [kW] *)
    rQ_SteamChestZone3_kW               : REAL := 0.0;   (* Zone 3 thermal heat transfer rate [kW] *)
    rPlateTemp_Zone1_Act                : REAL := 165.0; (* Actual steam chest zone 1 hot plate temp [deg C] *)
    rPlateTemp_Zone2_Act                : REAL := 180.0; (* Actual steam chest zone 2 hot plate temp [deg C] *)
    rPlateTemp_Zone3_Act                : REAL := 170.0; (* Actual steam chest zone 3 hot plate temp [deg C] *)
    rBoardMoistureTopLiner_Pct          : REAL := 7.2;   (* Top single-face liner moisture content [%] *)
    rBoardMoistureBottomLiner_Pct       : REAL := 6.8;   (* Bottom liner moisture content [%] *)
    rBoardCurlIndex_Internal            : REAL := 0.0;   (* Warpage curl index [-100.0 to +100.0 %] *)

    (* Bridge Festoon Catenary Kinematics *)
    rBridgeSpanLength_m                 : REAL := 32.0;  (* Total catenary festoon suspension span [m] *)
    rBridgeLinearMassDensity_kg_m       : REAL := 1.050; (* Linear web mass density [kg/m] *)
    rBridgeAccumulatorLength_Act        : REAL := 22.0;  (* Buffered single-face web length [m] *)
    rBridgeAccumulatorLength_Max        : REAL := 55.0;  (* Maximum bridge storage capacity [m] *)
    rBridgeAccumulatorLength_Min        : REAL := 5.0;   (* Minimum bridge storage capacity [m] *)

    (* Flying Rotary Cutoff Shear Kinematics & Electronic Camming *)
    rKnifeRadius_mm                     : REAL := 159.155;(* Effective knife cylinder pitch radius (C = 1000.0 mm) [mm] *)
    rKnifeCircumference_mm              : REAL := 1000.0; (* Knife cylinder perimeter [mm] *)
    rKnifeCutZoneHalfAngle_deg          : REAL := 12.0;   (* Angular half-width of synchronous cutting zone [deg] *)
    rKnifeSyncVelocity_m_min            : REAL := 0.0;    (* Synchronous web linear velocity at cut [m/min] *)
    rKnifeTargetOmega_rpm               : REAL := 0.0;    (* Target knife rotational speed [rpm] *)
    rKnifeActualAngle_deg               : REAL := 0.0;    (* Voted current knife angular position [deg] *)
    rKnifeCutoffPhaseError_deg          : REAL := 0.0;    (* Angular phase error at cut registration mark [deg] *)
    rKnifeIntegralPhaseErr_deg          : REAL := 0.0;    (* Integrated phase error for zero steady-state offset [deg] *)
    bKnifeInSyncCutZone                 : BOOL := FALSE;  (* True when knife blade is inside synchronous cutting window *)
    nCutPulseCount                      : DINT := 0;      (* Cumulative sheet cut registration counter *)

    (* Slitter / Scorer Tandem Indexing *)
    bSlitterIndexBusy                   : BOOL := FALSE;  (* True while robotic tool carousel indexes to new order *)
    rSlitterIndexTimer_Sec              : REAL := 0.0;    (* Timer for tool positioning index delay [s] *)

    (* === ISA-18.2 PROCESS ALARM TRIP SETPOINTS & DEADBANDS === *)
    cALM_TEMP_ROLL_HH                   : REAL := 195.0;  (* Upper roll temperature High-High shutdown [deg C] *)
    cALM_TEMP_ROLL_H                    : REAL := 188.0;  (* Upper roll temperature High warning [deg C] *)
    cALM_TEMP_ROLL_L                    : REAL := 145.0;  (* Upper roll temperature Low warning [deg C] *)
    cALM_TEMP_ROLL_LL                   : REAL := 130.0;  (* Upper roll temperature Low-Low shutdown [deg C] *)
    cALM_TEMP_DEADBAND                  : REAL := 2.5;    (* Temperature alarm deadband [deg C] *)

    cALM_PRESS_STEAM_HH                 : REAL := 28.5;   (* Steam supply pressure High-High trip [bar] *)
    cALM_PRESS_STEAM_H                  : REAL := 26.5;   (* Steam supply pressure High warning [bar] *)
    cALM_PRESS_STEAM_L                  : REAL := 18.0;   (* Steam supply pressure Low warning [bar] *)
    cALM_PRESS_STEAM_LL                 : REAL := 14.0;   (* Steam supply pressure Low-Low trip [bar] *)
    cALM_PRESS_DEADBAND                 : REAL := 0.5;    (* Steam pressure alarm deadband [bar] *)

    cALM_SAG_BRIDGE_HH                  : REAL := 1600.0; (* Bridge catenary sag High-High floor jam trip [mm] *)
    cALM_SAG_BRIDGE_H                   : REAL := 1400.0; (* Bridge catenary sag High warning [mm] *)
    cALM_SAG_BRIDGE_L                   : REAL := 400.0;  (* Bridge catenary sag Low warning [mm] *)
    cALM_SAG_BRIDGE_LL                  : REAL := 200.0;  (* Bridge catenary sag Low-Low web break trip [mm] *)
    cALM_SAG_DEADBAND                   : REAL := 30.0;   (* Bridge sag alarm deadband [mm] *)

    cALM_TENSION_DB_HH                  : REAL := 950.0;  (* Double-backer entry web tension High-High web tear trip [N] *)
    cALM_TENSION_DB_H                   : REAL := 750.0;  (* Double-backer entry web tension High warning [N] *)
    cALM_TENSION_DB_L                   : REAL := 150.0;  (* Double-backer entry web tension Low warning [N] *)
    cALM_TENSION_DB_LL                  : REAL := 50.0;   (* Double-backer entry web tension Low-Low web break trip [N] *)
    cALM_TENSION_DEADBAND               : REAL := 25.0;   (* Web tension alarm deadband [N] *)

    cALM_CUT_ERR_HH                     : REAL := 3.5;    (* Flying shear cut length error High-High trip [mm] *)
    cALM_CUT_ERR_H                      : REAL := 0.5;    (* Flying shear cut length error High warning [mm] *)

    (* ISA-18.2 Priority Escalation Timers *)
    rTimer_AlmEscalate_TempH            : REAL := 0.0;
    rTimer_AlmEscalate_PressH           : REAL := 0.0;
    rTimer_AlmEscalate_SagH             : REAL := 0.0;
    rTimer_AlmEscalate_TensionH         : REAL := 0.0;
    cTIME_ALARM_ESCALATION_SEC          : REAL := 45.0;   (* Priority escalation threshold unacknowledged [s] *)

    (* Active Alarm Condition Latch Bits *)
    bAlm_TempRoll_HH                    : BOOL := FALSE;
    bAlm_TempRoll_H                     : BOOL := FALSE;
    bAlm_TempRoll_L                     : BOOL := FALSE;
    bAlm_TempRoll_LL                    : BOOL := FALSE;

    bAlm_PressSteam_HH                  : BOOL := FALSE;
    bAlm_PressSteam_H                   : BOOL := FALSE;
    bAlm_PressSteam_L                   : BOOL := FALSE;
    bAlm_PressSteam_LL                  : BOOL := FALSE;

    bAlm_SagBridge_HH                   : BOOL := FALSE;
    bAlm_SagBridge_H                    : BOOL := FALSE;
    bAlm_SagBridge_L                    : BOOL := FALSE;
    bAlm_SagBridge_LL                   : BOOL := FALSE;

    bAlm_TensionDB_HH                   : BOOL := FALSE;
    bAlm_TensionDB_H                    : BOOL := FALSE;
    bAlm_TensionDB_L                    : BOOL := FALSE;
    bAlm_TensionDB_LL                   : BOOL := FALSE;

    bAlm_CutErr_HH                      : BOOL := FALSE;
    bAlm_CutErr_H                       : BOOL := FALSE;
    bAlm_WebWrapUpJam_HH                : BOOL := FALSE;

    (* General loop iteration and temporary arithmetic variables *)
    nIdx_i                              : INT := 1;
    nIdx_j                              : INT := 1;
    nIdx_k                              : INT := 1;
    nIdx_iter                           : INT := 1;
    rTemp_Sum                           : REAL := 0.0;
    rTemp_Diff                          : REAL := 0.0;
    rTemp_Term                          : REAL := 0.0;
    rNorm_Grad                          : REAL := 0.0;
END_VAR
'''

if __name__ == '__main__':
    p1 = get_part1()
    print("Part 1 length:", len(p1))
