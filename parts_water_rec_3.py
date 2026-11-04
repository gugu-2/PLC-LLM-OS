# parts_water_rec_3.py - Internal VAR declarations

def get_var_internal():
    return """VAR
    (* =================================================================================================================
     * SECTION 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) VOTING INTERNAL STRUCTURES & TIMERS
     * ================================================================================================================= *)
    (* Group 1: MABR Bulk Liquid Dissolved Oxygen Transmitters *)
    rVoted_MABR_DO                  : REAL;
    rDelta_MABR_DO_AB               : REAL;
    rDelta_MABR_DO_BC               : REAL;
    rDelta_MABR_DO_CA               : REAL;
    tTimer_MABR_DO_AB               : REAL;
    tTimer_MABR_DO_BC               : REAL;
    tTimer_MABR_DO_CA               : REAL;
    bHealth_MABR_DO_A               : BOOL;
    bHealth_MABR_DO_B               : BOOL;
    bHealth_MABR_DO_C               : BOOL;

    (* Group 2: MABR Ammonium Ion-Selective Electrodes *)
    rVoted_MABR_NH4                 : REAL;
    rDelta_MABR_NH4_AB              : REAL;
    rDelta_MABR_NH4_BC              : REAL;
    rDelta_MABR_NH4_CA              : REAL;
    tTimer_MABR_NH4_AB              : REAL;
    tTimer_MABR_NH4_BC              : REAL;
    tTimer_MABR_NH4_CA              : REAL;
    bHealth_MABR_NH4_A              : BOOL;
    bHealth_MABR_NH4_B              : BOOL;
    bHealth_MABR_NH4_C              : BOOL;

    (* Group 3: MABR Nitrate Ion-Selective Electrodes *)
    rVoted_MABR_NO3                 : REAL;
    rDelta_MABR_NO3_AB              : REAL;
    rDelta_MABR_NO3_BC              : REAL;
    rDelta_MABR_NO3_CA              : REAL;
    tTimer_MABR_NO3_AB              : REAL;
    tTimer_MABR_NO3_BC              : REAL;
    tTimer_MABR_NO3_CA              : REAL;
    bHealth_MABR_NO3_A              : BOOL;
    bHealth_MABR_NO3_B              : BOOL;
    bHealth_MABR_NO3_C              : BOOL;

    (* Group 4: Submerged UF Transmembrane Pressure Transmitters *)
    rVoted_UF_TMP                   : REAL;
    rDelta_UF_TMP_AB                : REAL;
    rDelta_UF_TMP_BC                : REAL;
    rDelta_UF_TMP_CA                : REAL;
    tTimer_UF_TMP_AB                : REAL;
    tTimer_UF_TMP_BC                : REAL;
    tTimer_UF_TMP_CA                : REAL;
    bHealth_UF_TMP_A                : BOOL;
    bHealth_UF_TMP_B                : BOOL;
    bHealth_UF_TMP_C                : BOOL;

    (* Group 5: Submerged UF Permeate Turbidity Transmitters *)
    rVoted_UF_Turb                  : REAL;
    rDelta_UF_Turb_AB               : REAL;
    rDelta_UF_Turb_BC               : REAL;
    rDelta_UF_Turb_CA               : REAL;
    tTimer_UF_Turb_AB               : REAL;
    tTimer_UF_Turb_BC               : REAL;
    tTimer_UF_Turb_CA               : REAL;
    bHealth_UF_Turb_A               : BOOL;
    bHealth_UF_Turb_B               : BOOL;
    bHealth_UF_Turb_C               : BOOL;

    (* Group 6: RO High-Pressure Primary Feed Pressure Transmitters *)
    rVoted_RO_HP_Feed               : REAL;
    rDelta_RO_HP_Feed_AB            : REAL;
    rDelta_RO_HP_Feed_BC            : REAL;
    rDelta_RO_HP_Feed_CA            : REAL;
    tTimer_RO_HP_Feed_AB            : REAL;
    tTimer_RO_HP_Feed_BC            : REAL;
    tTimer_RO_HP_Feed_CA            : REAL;
    bHealth_RO_HP_Feed_A            : BOOL;
    bHealth_RO_HP_Feed_B            : BOOL;
    bHealth_RO_HP_Feed_C            : BOOL;

    (* Group 7: RO Stage 2 Concentrate Brine Pressure Transmitters *)
    rVoted_RO_Conc_Press            : REAL;
    rDelta_RO_Conc_Press_AB         : REAL;
    rDelta_RO_Conc_Press_BC         : REAL;
    rDelta_RO_Conc_Press_CA         : REAL;
    tTimer_RO_Conc_Press_AB         : REAL;
    tTimer_RO_Conc_Press_BC         : REAL;
    tTimer_RO_Conc_Press_CA         : REAL;
    bHealth_RO_Conc_Press_A         : BOOL;
    bHealth_RO_Conc_Press_B         : BOOL;
    bHealth_RO_Conc_Press_C         : BOOL;

    (* Group 8: RO Permeate Electrical Conductivity Transmitters *)
    rVoted_RO_Cond                  : REAL;
    rDelta_RO_Cond_AB               : REAL;
    rDelta_RO_Cond_BC               : REAL;
    rDelta_RO_Cond_CA               : REAL;
    tTimer_RO_Cond_AB               : REAL;
    tTimer_RO_Cond_BC               : REAL;
    tTimer_RO_Cond_CA               : REAL;
    bHealth_RO_Cond_A               : BOOL;
    bHealth_RO_Cond_B               : BOOL;
    bHealth_RO_Cond_C               : BOOL;

    (* Group 9: Isobaric ERD High-Pressure Brine Inlet Pressure Transmitters *)
    rVoted_ERD_HP_In                : REAL;
    rDelta_ERD_HP_In_AB             : REAL;
    rDelta_ERD_HP_In_BC             : REAL;
    rDelta_ERD_HP_In_CA             : REAL;
    tTimer_ERD_HP_In_AB             : REAL;
    tTimer_ERD_HP_In_BC             : REAL;
    tTimer_ERD_HP_In_CA             : REAL;
    bHealth_ERD_HP_In_A             : BOOL;
    bHealth_ERD_HP_In_B             : BOOL;
    bHealth_ERD_HP_In_C             : BOOL;

    (* Group 10: UV Disinfection Transmittance (UVT-254) Spectrophotometers *)
    rVoted_UV_Trans                 : REAL;
    rDelta_UV_Trans_AB              : REAL;
    rDelta_UV_Trans_BC              : REAL;
    rDelta_UV_Trans_CA              : REAL;
    tTimer_UV_Trans_AB              : REAL;
    tTimer_UV_Trans_BC              : REAL;
    tTimer_UV_Trans_CA              : REAL;
    bHealth_UV_Trans_A              : BOOL;
    bHealth_UV_Trans_B              : BOOL;
    bHealth_UV_Trans_C              : BOOL;

    (* TMR Discrepancy Debounce Time Thresholds *)
    tDebounce_Limit_Sec             : REAL := 2.50; (* Debounce timer qualification limit [s] *)
    rTol_MABR_DO                    : REAL := 0.25; (* Discrepancy threshold [mg/L] *)
    rTol_MABR_NH4                   : REAL := 2.00; (* Discrepancy threshold [mg/L] *)
    rTol_MABR_NO3                   : REAL := 2.50; (* Discrepancy threshold [mg/L] *)
    rTol_UF_TMP                     : REAL := 0.08; (* Discrepancy threshold [bar] *)
    rTol_UF_Turb                    : REAL := 0.04; (* Discrepancy threshold [NTU] *)
    rTol_RO_HP_Feed                 : REAL := 2.50; (* Discrepancy threshold [bar] *)
    rTol_RO_Conc_Press              : REAL := 2.50; (* Discrepancy threshold [bar] *)
    rTol_RO_Cond                    : REAL := 8.00; (* Discrepancy threshold [uS/cm] *)
    rTol_ERD_HP_In                  : REAL := 2.50; (* Discrepancy threshold [bar] *)
    rTol_UV_Trans                   : REAL := 2.00; (* Discrepancy threshold [%] *)

    (* =================================================================================================================
     * SECTION 2: DISCRETE 8x8 CYBER-PHYSICAL STATE-SPACE MATRICES AND MPC REGISTERS
     * ================================================================================================================= *)
    (* State vector x: [DO, NH4, NOx, TMP, Rcake, RO_Press, RO_Cond, ERD_RPM]^T *)
    x_state                         : ARRAY[1..8] OF REAL;
    x_pred                          : ARRAY[1..8] OF REAL;
    x_ref                           : ARRAY[1..8] OF REAL;
    x_err                           : ARRAY[1..8] OF REAL;

    (* Actuator vector u: [LumenAir, RecycleRPM, UFSuction, UFAirScour, HPFeedVFD, ERDBooster, BrineValve, Antiscalant]^T *)
    u_curr                          : ARRAY[1..8] OF REAL;
    u_opt                           : ARRAY[1..8] OF REAL;
    u_delta                         : ARRAY[1..8] OF REAL;
    u_prev                          : ARRAY[1..8] OF REAL;

    (* State-Space Matrices: x[k+1] = A * x[k] + B * u[k] *)
    A_mat                           : ARRAY[1..8, 1..8] OF REAL;
    B_mat                           : ARRAY[1..8, 1..8] OF REAL;
    C_mat                           : ARRAY[1..8, 1..8] OF REAL;
    D_mat                           : ARRAY[1..8, 1..8] OF REAL;

    (* MPC Quadratic Cost Weighting Matrices *)
    Q_diag                          : ARRAY[1..8] OF REAL;
    R_diag                          : ARRAY[1..8] OF REAL;
    P_term                          : ARRAY[1..8, 1..8] OF REAL;

    (* MPC Optimization Internal Iteration Variables *)
    iMPC_Iter                       : INT;
    rMPC_Alpha_Step                 : REAL := 0.015;
    rGrad_Vec                       : ARRAY[1..8] OF REAL;
    u_max_slew                      : ARRAY[1..8] OF REAL;
    u_bound_low                     : ARRAY[1..8] OF REAL;
    u_bound_high                    : ARRAY[1..8] OF REAL;

    (* =================================================================================================================
     * SECTION 3: ADVANCED CYBER-PHYSICAL TRANSPORT OBSERVERS INTERNAL VARIABLES
     * ================================================================================================================= *)
    (* MABR Biofilm Mass Transfer and Monod Kinetics *)
    rMABR_Lf_Biofilm_Current_um     : REAL := 220.0;    (* Initial baseline biofilm thickness [um] *)
    rMABR_Lf_Deriv                  : REAL;
    rMABR_KL_Oxygen_Permeance       : REAL := 0.00045;  (* Mass transfer coefficient [m/s] *)
    rMABR_Henry_O2                  : REAL := 0.0315;   (* Dimensionless Henry solubility coefficient *)
    rMABR_DO_Interface_mg_L         : REAL;
    rMABR_Mu_Max_AOB                : REAL := 0.85;     (* Max specific growth rate Nitrifiers [1/d] *)
    rMABR_Mu_Max_DEN                : REAL := 2.40;     (* Max specific growth rate Denitrifiers [1/d] *)
    rMABR_K_DO_AOB                  : REAL := 0.50;     (* Half-saturation DO for AOB [mg/L] *)
    rMABR_K_NH4                     : REAL := 1.00;     (* Half-saturation NH4-N [mg/L] *)
    rMABR_K_O2_Inhibit_DEN          : REAL := 0.15;     (* Oxygen inhibition coefficient for denitrifiers [mg/L] *)
    rMABR_K_NO3                     : REAL := 0.80;     (* Half-saturation NO3-N [mg/L] *)
    rMABR_K_COD                     : REAL := 20.0;     (* Half-saturation COD [mg/L] *)
    rMABR_Theta_Nitrif              : REAL := 1.072;    (* Arrhenius temperature coefficient for nitrification *)
    rMABR_Theta_Denitrif            : REAL := 1.050;    (* Arrhenius temperature coefficient for denitrification *)
    rMABR_Biofilm_Decay_Rate        : REAL := 0.050;    (* Endogenous biomass decay rate [1/d] *)
    rMABR_Biofilm_Shear_Detach_Coeff: REAL := 0.000085; (* Hydrodynamic and bubbling shear detachment factor *)

    (* Submerged UF Resistance-in-Series Parameters *)
    rUF_Water_Viscosity_Pa_s        : REAL;
    rUF_Permeate_Flux_m_s           : REAL;
    rUF_Permeate_Flux_LMH           : REAL;
    rUF_Membrane_Area_Total_m2      : REAL := 65000.0;  (* Total submerged membrane surface area [m2] *)
    rUF_Cake_Resistance_Accum       : REAL := 3.2E11;   (* Initial dynamic cake layer resistance [1/m] *)
    rUF_Specific_Cake_Resistivity   : REAL := 4.8E13;   (* Specific cake resistance alpha [m/kg] *)
    rUF_Air_Scour_Cleaning_Eff      : REAL := 0.0042;   (* Shear relaxation detachment coefficient *)

    (* RO Concentration Polarization, Osmotic Pressure, and ERD Physics *)
    rRO_TDS_Concentration_Feed_g_L  : REAL;
    rRO_Osmotic_Pressure_Feed_bar   : REAL;
    rRO_Osmotic_Pressure_Conc_bar   : REAL;
    rRO_Osmotic_Pressure_Avg_bar    : REAL;
    rRO_Permeability_A_LMH_bar      : REAL := 3.85;     (* Pure water permeability coefficient at 25C *)
    rRO_Mass_Transfer_Coeff_k       : REAL := 0.000022; (* Feed channel spacer mass transfer velocity [m/s] *)
    rRO_Permeate_Flux_m_s           : REAL;
    rRO_Permeate_Flux_LMH           : REAL;
    rRO_Membrane_Area_RO_m2         : REAL := 42000.0;  (* Total active SWRO/BWRO membrane area [m2] *)
    rERD_Target_RPM                 : REAL;
    rERD_Duct_Pressure_Drop_bar     : REAL;

    (* Silt Density Index (SDI-15) and UV Disinfection Parameters *)
    rSDI_Dynamic_Membrane_Fouling   : REAL;
    rUV_Absorbance_254nm            : REAL;
    rUV_Average_Fluence_Rate_mW_cm2 : REAL;
    rUV_Reactor_Volume_m3           : REAL := 45.0;     (* Validated closed-vessel UV reactor volume [m3] *)
    rUV_Hydraulic_Retention_Time_s  : REAL;

    (* =================================================================================================================
     * SECTION 4: DETERMINISTIC 12-STAGE FINITE STATE MACHINE (FSM) STATE REGISTERS & TIMERS
     * ================================================================================================================= *)
    iFSM_State                      : INT := 0;         (* Initial State: PLANT_WETTING_LINE_PURGE *)
    iFSM_NextState                  : INT := 0;
    iFSM_SubPhase                   : INT := 0;
    tFSM_StateTimer_Sec             : REAL := 0.0;
    tFSM_SubPhaseTimer_Sec          : REAL := 0.0;
    bFSM_FirstScanInState           : BOOL := TRUE;
    bFSM_TransitionRequested        : BOOL := FALSE;

    (* UF Backwash Cycle Periodic Counter *)
    tUF_Filtration_Run_Timer_Sec    : REAL := 0.0;
    tUF_Filtration_Cycle_Limit_Sec  : REAL := 1200.0;   (* 20 minutes normal forward filtration *)
    tRO_CIP_Accumulated_Hours       : REAL := 0.0;

    (* =================================================================================================================
     * SECTION 5: ISA-18.2 MULTI-TIERED ALARM LADDER REGISTERS, TRIP LIMITS & DEADBANDS
     * ================================================================================================================= *)
    (* MABR DO Alarms *)
    bAlarm_MABR_DO_HH               : BOOL;
    bAlarm_MABR_DO_H                : BOOL;
    bAlarm_MABR_DO_L                : BOOL;
    bAlarm_MABR_DO_LL               : BOOL;
    rROC_MABR_DO                    : REAL;
    rPrev_MABR_DO                   : REAL;
    bAlarm_MABR_DO_ROC              : BOOL;

    (* MABR Ammonium Alarms *)
    bAlarm_MABR_NH4_HH              : BOOL;
    bAlarm_MABR_NH4_H               : BOOL;

    (* Submerged UF TMP Alarms *)
    bAlarm_UF_TMP_HH                : BOOL;
    bAlarm_UF_TMP_H                 : BOOL;
    rROC_UF_TMP                     : REAL;
    rPrev_UF_TMP                    : REAL;
    bAlarm_UF_TMP_ROC               : BOOL;

    (* Submerged UF Turbidity Integrity Alarms *)
    bAlarm_UF_Turb_HH               : BOOL;
    bAlarm_UF_Turb_H                : BOOL;

    (* RO High-Pressure Feed Alarms *)
    bAlarm_RO_HP_Feed_HH            : BOOL;
    bAlarm_RO_HP_Feed_H             : BOOL;
    bAlarm_RO_HP_Feed_L             : BOOL;
    bAlarm_RO_HP_Feed_LL            : BOOL;
    rROC_RO_HP_Feed                 : REAL;
    rPrev_RO_HP_Feed                : REAL;
    bAlarm_RO_HP_Feed_ROC           : BOOL;

    (* RO Permeate Electrical Conductivity Alarms *)
    bAlarm_RO_Cond_HH               : BOOL;
    bAlarm_RO_Cond_H                : BOOL;

    (* ERD Rotor Speed Alarms *)
    bAlarm_ERD_RPM_HH               : BOOL;
    bAlarm_ERD_RPM_H                : BOOL;
    bAlarm_ERD_RPM_L                : BOOL;
    bAlarm_ERD_RPM_LL               : BOOL;

    (* Feed SDI and UV Inactivation Alarms *)
    bAlarm_Feed_SDI_HH              : BOOL;
    bAlarm_Feed_SDI_H               : BOOL;
    bAlarm_UV_Trans_LL              : BOOL;
    bAlarm_UV_Trans_L               : BOOL;
    bAlarm_UV_Dose_LL               : BOOL;
    bAlarm_UV_Dose_L                : BOOL;

    (* Deadband Hysteresis Registers *)
    rDB_MABR_DO                     : REAL := 0.05;     (* [mg/L] *)
    rDB_MABR_NH4                    : REAL := 0.50;     (* [mg/L] *)
    rDB_UF_TMP                      : REAL := 0.02;     (* [bar] *)
    rDB_UF_Turb                     : REAL := 0.01;     (* [NTU] *)
    rDB_RO_HP_Feed                  : REAL := 0.75;     (* [bar] *)
    rDB_RO_Cond                     : REAL := 3.00;     (* [uS/cm] *)
    rDB_ERD_RPM                     : REAL := 25.0;     (* [RPM] *)
    rDB_Feed_SDI                    : REAL := 0.20;     (* [dimensionless] *)
    rDB_UV_Trans                    : REAL := 0.80;     (* [%] *)
    rDB_UV_Dose                     : REAL := 1.50;     (* [mJ/cm2] *)

    (* Matrix & Loop Iteration Counters *)
    iIdx                            : INT;
    jIdx                            : INT;
    kIdx                            : INT;
    mIdx                            : INT;
END_VAR
"""
