# build_st_var.py
# Section 2: Internal Variable Declarations (VAR ... END_VAR) for FB_Nuclear_PWR_SteamGenerator_NarrowRangeLevel_ShrinkSwell

def get_var_declarations():
    return """VAR
    (* =================================================================================================================
     * SECTION 3.1: FUNDAMENTAL CYCLE TIME, SIMULATION CONSTANTS & PHYSICAL COEFFICIENTS
     * ================================================================================================================= *)
    rScan_Period_Ts                 : REAL := 0.025;      (* Real-Time Sampling Execution Period [s] (25 ms) *)
    bInitialized                    : BOOL := FALSE;      (* Master First-Scan Cold Initialization Latch *)
    rSG_Rated_Thermal_MW            : REAL := 850.0;      (* Single Steam Generator Rated Thermal Capacity [MW] *)
    rSG_Full_Power_Steam_Flow_t_h   : REAL := 1820.0;     (* Rated Steam Mass Flow Rate at 100% RTP [t/h] *)
    rSG_Full_Power_Feed_Flow_t_h    : REAL := 1820.0;     (* Rated Feedwater Mass Flow Rate at 100% RTP [t/h] *)
    rSG_Nominal_Operating_Pressure  : REAL := 68.5;       (* Normal Operating Saturated Steam Pressure [bar] *)
    rNominal_ColdLeg_Temperature    : REAL := 292.0;      (* Reference Full-Power Primary Cold Leg Temperature [deg C] *)
    rNominal_HotLeg_Temperature     : REAL := 326.0;      (* Reference Full-Power Primary Hot Leg Temperature [deg C] *)
    rSpecific_Heat_Water_Cp         : REAL := 4.184;      (* Primary Light Water Specific Heat Capacity [kJ/(kg*K)] *)
    rEnthalpy_Vaporization_hfg      : REAL := 1510.0;     (* Latent Heat of Steam Vaporization at 68.5 bar [kJ/kg] *)

    (* =================================================================================================================
     * SECTION 3.2: DISCRETE STATE-SPACE MATRICES (8 STATES x 5 INPUTS x 5 OUTPUTS)
     * ================================================================================================================= *)
    (* State Vector x:
     *   x[1] = Steam Generator Narrow-Range Level Deviation [mm]
     *   x[2] = Downcomer Recirculation Flow Rate Deviation [kg/s]
     *   x[3] = Boiling Riser Average Bulk Void Fraction Deviation [ratio 0..1]
     *   x[4] = Primary-to-Secondary U-Tube Heat Transfer Rate Deviation [MW]
     *   x[5] = Steam Drum Saturated Pressure Deviation [bar]
     *   x[6] = Primary Coolant Cold Leg Temperature Deviation [deg C]
     *   x[7] = Main Feedwater Regulating Valve Trim Effective Dynamic Position [%]
     *   x[8] = Dynamic Inverse Response Lead-Lag Non-Minimum Phase Swell State [mm]
     *)
    A_mat                           : ARRAY[1..8, 1..8] OF REAL; (* Discrete System Dynamics Matrix A (8x8) [-] *)
    B_mat                           : ARRAY[1..8, 1..5] OF REAL; (* Discrete Actuator/Disturbance Input Matrix B (8x5) [-] *)
    C_mat                           : ARRAY[1..5, 1..8] OF REAL; (* Discrete Observation Matrix C (5x8) [-] *)
    D_mat                           : ARRAY[1..5, 1..5] OF REAL; (* Discrete Direct Feedthrough Matrix D (5x5) [-] *)
    L_mat                           : ARRAY[1..8, 1..5] OF REAL; (* Discrete Kalman Filter Observer Gain Matrix L (8x5) [-] *)

    (* Model Predictive Control Quadratic Cost Weighting Matrices *)
    Q_mat                           : ARRAY[1..8, 1..8] OF REAL; (* State Error Quadratic Cost Penalty Matrix Q (8x8) [-] *)
    R_mat                           : ARRAY[1..5, 1..5] OF REAL; (* Control Actuation Effort Penalty Matrix R (5x5) [-] *)
    P_mat                           : ARRAY[1..8, 1..8] OF REAL; (* Terminal State Error Quadratic Penalty Matrix P (8x8) [-] *)

    (* State, Control, Measurement & Innovation Vectors *)
    x_hat                           : ARRAY[1..8] OF REAL;       (* Filtered a-posteriori State Vector Estimate [-] *)
    x_pred                          : ARRAY[1..8] OF REAL;       (* One-step Ahead a-priori State Vector Prediction [-] *)
    x_ref                           : ARRAY[1..8] OF REAL;       (* Target Reference State Vector Setpoint [-] *)
    u_vec                           : ARRAY[1..5] OF REAL;       (* Plant Control Vector: [MFRV %, Bypass %, AFW-M %, AFW-T t/h, Blowdown %] *)
    u_prev                          : ARRAY[1..5] OF REAL;       (* Previous Execution Cycle Control Vector [-] *)
    y_meas                          : ARRAY[1..5] OF REAL;       (* Validated Voted Measurement Vector [mm, bar, t/h, t/h, deg C] *)
    y_pred                          : ARRAY[1..5] OF REAL;       (* Observer Output Prediction Vector [-] *)
    y_res                           : ARRAY[1..5] OF REAL;       (* Measurement Innovation Residual Vector y_meas - y_pred [-] *)

    (* Receding-Horizon MPC Rolling Optimization Workspace *)
    x_traj                          : ARRAY[1..6, 1..8] OF REAL; (* State Trajectory Prediction Horizon Np=5 (steps 1..6) *)
    u_traj                          : ARRAY[1..5, 1..5] OF REAL; (* Optimal Actuator Control Trajectory Np=5 (steps 1..5) *)
    u_traj_prev                     : ARRAY[1..5, 1..5] OF REAL; (* Warm-Start Previous Slew Baseline Trajectory [-] *)
    lambda_costate                  : ARRAY[1..6, 1..8] OF REAL; (* Backward Adjoint Costate Multipliers (steps 6 down to 1) *)
    grad_u                          : ARRAY[1..5, 1..5] OF REAL; (* Projected Gradient of Quadratic Cost Functional w.r.t Actuation *)
    rPGD_StepSize                   : REAL := 0.015;             (* Projected Gradient Descent Learning Rate Step Size [-] *)
    rMPC_MFRV_Upper_Bound           : REAL := 100.0;             (* Maximum Allowable MFRV Position [%] *)
    rMPC_MFRV_Lower_Bound           : REAL := 0.0;               (* Minimum Allowable MFRV Position [%] *)
    rMPC_Bypass_Upper_Bound         : REAL := 100.0;             (* Maximum Allowable Low-Power Bypass Position [%] *)
    rMPC_Bypass_Lower_Bound         : REAL := 0.0;               (* Minimum Allowable Low-Power Bypass Position [%] *)
    rMax_Actuator_Slew_Rate_pct_s   : REAL := 5.0;               (* Maximum Allowable Actuator Slew Rate [%/s] *)
    rMax_Slew_Per_Cycle             : REAL := 0.125;             (* Slew Limit Clamping per 25 ms Cycle (5.0 * 0.025) [%] *)

    (* =================================================================================================================
     * SECTION 3.3: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) ARCHITECTURAL DATA STRUCTURES
     * ================================================================================================================= *)
    (* Narrow Range Level Triplet (LT_NR) *)
    rTMR_NR_Discrepancy_Limit       : REAL := 80.0;              (* Channel-to-Median Allowed Level Deviation [mm] *)
    rTMR_NR_Timer_ChA               : REAL := 0.0;               (* Channel A Accumulated Discrepancy Timer [s] *)
    rTMR_NR_Timer_ChB               : REAL := 0.0;               (* Channel B Accumulated Discrepancy Timer [s] *)
    rTMR_NR_Timer_ChC               : REAL := 0.0;               (* Channel C Accumulated Discrepancy Timer [s] *)
    bTMR_NR_Failed_ChA              : BOOL := FALSE;             (* Channel A Out-of-Spec Latched Failure *)
    bTMR_NR_Failed_ChB              : BOOL := FALSE;             (* Channel B Out-of-Spec Latched Failure *)
    bTMR_NR_Failed_ChC              : BOOL := FALSE;             (* Channel C Out-of-Spec Latched Failure *)
    nHealth_TMR_Level_NR            : INT  := 3;                 (* Healthy Channel Count (3=2oo3, 2=1oo2, 1=1oo1, 0=Fail) *)

    (* Wide Range Level Triplet (LT_WR) *)
    rTMR_WR_Discrepancy_Limit       : REAL := 250.0;             (* Channel-to-Median Allowed Level Deviation [mm] *)
    rTMR_WR_Timer_ChA               : REAL := 0.0;               (* Channel A Accumulated Discrepancy Timer [s] *)
    rTMR_WR_Timer_ChB               : REAL := 0.0;               (* Channel B Accumulated Discrepancy Timer [s] *)
    rTMR_WR_Timer_ChC               : REAL := 0.0;               (* Channel C Accumulated Discrepancy Timer [s] *)
    bTMR_WR_Failed_ChA              : BOOL := FALSE;             (* Channel A Out-of-Spec Latched Failure *)
    bTMR_WR_Failed_ChB              : BOOL := FALSE;             (* Channel B Out-of-Spec Latched Failure *)
    bTMR_WR_Failed_ChC              : BOOL := FALSE;             (* Channel C Out-of-Spec Latched Failure *)
    nHealth_TMR_Level_WR            : INT  := 3;                 (* Healthy Channel Count *)

    (* Steam Drum Pressure Triplet (PT_MS) *)
    rTMR_Press_Discrepancy_Limit    : REAL := 1.75;              (* Channel-to-Median Allowed Pressure Deviation [bar] *)
    rTMR_Press_Timer_ChA            : REAL := 0.0;               (* Channel A Accumulated Discrepancy Timer [s] *)
    rTMR_Press_Timer_ChB            : REAL := 0.0;               (* Channel B Accumulated Discrepancy Timer [s] *)
    rTMR_Press_Timer_ChC            : REAL := 0.0;               (* Channel C Accumulated Discrepancy Timer [s] *)
    bTMR_Press_Failed_ChA           : BOOL := FALSE;             (* Channel A Out-of-Spec Latched Failure *)
    bTMR_Press_Failed_ChB           : BOOL := FALSE;             (* Channel B Out-of-Spec Latched Failure *)
    bTMR_Press_Failed_ChC           : BOOL := FALSE;             (* Channel C Out-of-Spec Latched Failure *)
    nHealth_TMR_Press_MS            : INT  := 3;                 (* Healthy Channel Count *)

    (* Main Steam Mass Flow Triplet (FT_MS) *)
    rTMR_FlowMS_Discrepancy_Limit   : REAL := 55.0;              (* Channel-to-Median Allowed Steam Flow Deviation [t/h] *)
    rTMR_FlowMS_Timer_ChA           : REAL := 0.0;               (* Channel A Accumulated Discrepancy Timer [s] *)
    rTMR_FlowMS_Timer_ChB           : REAL := 0.0;               (* Channel B Accumulated Discrepancy Timer [s] *)
    rTMR_FlowMS_Timer_ChC           : REAL := 0.0;               (* Channel C Accumulated Discrepancy Timer [s] *)
    bTMR_FlowMS_Failed_ChA          : BOOL := FALSE;             (* Channel A Out-of-Spec Latched Failure *)
    bTMR_FlowMS_Failed_ChB          : BOOL := FALSE;             (* Channel B Out-of-Spec Latched Failure *)
    bTMR_FlowMS_Failed_ChC          : BOOL := FALSE;             (* Channel C Out-of-Spec Latched Failure *)
    nHealth_TMR_Flow_MS             : INT  := 3;                 (* Healthy Channel Count *)

    (* Main Feedwater Mass Flow Triplet (FT_FW) *)
    rTMR_FlowFW_Discrepancy_Limit   : REAL := 55.0;              (* Channel-to-Median Allowed Feedwater Flow Deviation [t/h] *)
    rTMR_FlowFW_Timer_ChA           : REAL := 0.0;               (* Channel A Accumulated Discrepancy Timer [s] *)
    rTMR_FlowFW_Timer_ChB           : REAL := 0.0;               (* Channel B Accumulated Discrepancy Timer [s] *)
    rTMR_FlowFW_Timer_ChC           : REAL := 0.0;               (* Channel C Accumulated Discrepancy Timer [s] *)
    bTMR_FlowFW_Failed_ChA          : BOOL := FALSE;             (* Channel A Out-of-Spec Latched Failure *)
    bTMR_FlowFW_Failed_ChB          : BOOL := FALSE;             (* Channel B Out-of-Spec Latched Failure *)
    bTMR_FlowFW_Failed_ChC          : BOOL := FALSE;             (* Channel C Out-of-Spec Latched Failure *)
    nHealth_TMR_Flow_FW             : INT  := 3;                 (* Healthy Channel Count *)

    (* Shared Discrepancy Window Constant *)
    rTMR_Fault_Accum_Time_Limit     : REAL := 0.500;             (* Maximum Continuous Discrepancy Duration [s] (500 ms) *)

    (* =================================================================================================================
     * SECTION 3.4: ISA-18.2 NUCLEAR CLASS 1E PROCESS ALARM TRIP SETPOINTS & DEBOUNCE TIMERS
     * ================================================================================================================= *)
    (* Narrow Range Water Level Trips *)
    rTrip_Level_NR_HighHigh_HH      : REAL := 3250.0;            (* High-High Trip (Turbine Trip & P-14 Isolation) [mm] *)
    rAlarm_Level_NR_High_H          : REAL := 2850.0;            (* High Pre-Trip Warning Level [mm] *)
    rAlarm_Level_NR_Low_L           : REAL := 2150.0;            (* Low Pre-Trip Warning Level [mm] *)
    rTrip_Level_NR_LowLow_LL        : REAL := 1750.0;            (* Low-Low Trip (Class 1E RPS SCRAM & AFW Auto-Start) [mm] *)
    rDeadband_Level_NR              : REAL := 25.0;              (* Alarm Reset Deadband Hysteresis [mm] *)

    (* Main Steam Drum Pressure Trips *)
    rTrip_Press_SteamDrum_HH        : REAL := 76.5;              (* High-High Pressure Overpressure Relief Trip [bar] *)
    rAlarm_Press_SteamDrum_H        : REAL := 72.0;              (* High Drum Pressure Advisory Alarm [bar] *)
    rAlarm_Press_SteamDrum_L        : REAL := 58.0;              (* Low Drum Pressure Operational Warning [bar] *)
    rTrip_Press_SteamDrum_LL        : REAL := 45.0;              (* Low-Low Pressure Steam Line Rupture Trip [bar] *)
    rDeadband_Press_SteamDrum       : REAL := 0.8;               (* Drum Pressure Deadband Hysteresis [bar] *)

    (* Steam/Feedwater Mass Flow Mismatch & Thermal Alarms *)
    rAlarm_Flow_Mismatch_Limit      : REAL := 120.0;             (* Mass Balance Feedwater-to-Steam Mismatch Alarm [t/h] *)
    rTrip_N16_Radiation_SGTR_HH     : REAL := 1850000.0;         (* N-16 Primary-to-Secondary Tube Rupture Trip [Bq/m3] *)
    rAlarm_N16_Radiation_SGTR_H     : REAL := 370000.0;          (* N-16 High Tube Leakage Warning [Bq/m3] *)
    rAlarm_Level_Rate_Of_Change_Lim : REAL := 60.0;              (* Maximum Expected Shrink/Swell Level Slew Rate [mm/s] *)

    (* Alarm Qualification Debounce Timers *)
    rTimer_Alarm_Level_HH           : REAL := 0.0;               (* High-High Level Debounce Filter Accumulator [s] *)
    rTimer_Alarm_Level_H            : REAL := 0.0;               (* High Level Debounce Filter Accumulator [s] *)
    rTimer_Alarm_Level_L            : REAL := 0.0;               (* Low Level Debounce Filter Accumulator [s] *)
    rTimer_Alarm_Level_LL           : REAL := 0.0;               (* Low-Low Level Debounce Filter Accumulator [s] *)
    rTimer_Alarm_Press_HH           : REAL := 0.0;               (* High-High Pressure Debounce Accumulator [s] *)
    rTimer_Alarm_Press_LL           : REAL := 0.0;               (* Low-Low Pressure Debounce Accumulator [s] *)
    rTimer_Alarm_FlowMismatch       : REAL := 0.0;               (* Flow Mismatch Debounce Accumulator [s] *)
    rTimer_Alarm_SGTR_Activity      : REAL := 0.0;               (* Tube Rupture Debounce Accumulator [s] *)

    (* Latched Alarm Status Bits *)
    bActive_Alarm_Level_HH          : BOOL := FALSE;             (* Level High-High Latched Trip Status *)
    bActive_Alarm_Level_H           : BOOL := FALSE;             (* Level High Active Status *)
    bActive_Alarm_Level_L           : BOOL := FALSE;             (* Level Low Active Status *)
    bActive_Alarm_Level_LL          : BOOL := FALSE;             (* Level Low-Low Latched Trip Status *)
    bActive_Alarm_Press_HH          : BOOL := FALSE;             (* Drum Pressure High-High Trip Status *)
    bActive_Alarm_Press_LL          : BOOL := FALSE;             (* Drum Pressure Low-Low Trip Status *)
    bActive_Alarm_FlowMismatch      : BOOL := FALSE;             (* Feed-Steam Flow Mismatch Warning *)
    bActive_Alarm_SGTR_Trip         : BOOL := FALSE;             (* Steam Generator Tube Rupture Emergency Trip *)

    (* =================================================================================================================
     * SECTION 3.5: DETERMINISTIC 14-STAGE NUCLEAR FINITE STATE MACHINE (FSM) VARIABLES
     * ================================================================================================================= *)
    eCurrentState                   : INT  := 0;                 (* Active Execution State Index (0..13) *)
    ePreviousState                  : INT  := 0;                 (* State History from Prior Evaluation Tick *)
    rState_Dwell_Timer              : REAL := 0.0;               (* Dwell Duration inside Current State [s] *)
    bState_Entry_Flag               : BOOL := TRUE;              (* One-Shot Rising Edge Pulse on State Entry *)
    bTransfer_Permissive_Met        : BOOL := FALSE;             (* Interlock Inter-State Transition Permissive *)
    rBumpless_Transition_Ramp       : REAL := 0.0;               (* Bumpless Transfer Cross-Fading Weighting [0..1] *)
    rMFRV_Auto_Demand_Unclamped     : REAL := 0.0;               (* Raw Optimal MFRV Demand prior to Slew Limiter [%] *)
    rBypass_Auto_Demand_Unclamped   : REAL := 0.0;               (* Raw Optimal Bypass Demand prior to Slew Limiter [%] *)
    rMFRV_Rate_Clamped_Prev         : REAL := 0.0;               (* Prior Cycle Clamped MFRV Command [%] *)
    rBypass_Rate_Clamped_Prev       : REAL := 0.0;               (* Prior Cycle Clamped Bypass Command [%] *)

    (* Dynamic Inverse Response Decoupling Filters *)
    rLeadLag_State_X1               : REAL := 0.0;               (* Irving-Miossec First Lead-Lag State [mm] *)
    rLeadLag_State_X2               : REAL := 0.0;               (* Irving-Miossec Second Lead-Lag State [mm] *)
    rSteam_Flow_Derivative          : REAL := 0.0;               (* Real-Time Filtered Steam Demand Rate-of-Change [t/(h*s)] *)
    rPrev_Voted_Steam_Flow          : REAL := 0.0;               (* Previous Cycle Voted Steam Flow [t/h] *)
    rPrev_Voted_Feed_Flow           : REAL := 0.0;               (* Previous Cycle Voted Feedwater Flow [t/h] *)
    rPrev_Voted_Level_NR            : REAL := 0.0;               (* Previous Cycle Voted Water Level [mm] *)
    rMeasured_Level_Rate_mm_s       : REAL := 0.0;               (* Computed Level Differential Velocity [mm/s] *)

    (* Iteration & Matrix Arithmetic Indices *)
    i_idx                           : INT  := 1;                 (* Outer Iteration Row Index *)
    j_idx                           : INT  := 1;                 (* Inner Iteration Column Index *)
    k_idx                           : INT  := 1;                 (* Receding Horizon Stage Index *)
    m_idx                           : INT  := 1;                 (* PGD Iteration Counter Index *)
    sum_accum                       : REAL := 0.0;               (* Matrix Dot-Product Accumulator Temp Variable *)
    cost_accum                      : REAL := 0.0;               (* Quadratic Cost Functional Evaluator Temp Variable *)
END_VAR
"""

if __name__ == "__main__":
    s = get_var_declarations()
    print("VAR block length:", len(s))
