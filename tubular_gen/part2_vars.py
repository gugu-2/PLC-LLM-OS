# part2_vars.py
vars_text = """VAR
    (* ======================================================================================================
       INTERNAL DISCRETE STATE-SPACE MODEL MATRICES & STATE ESTIMATION VECTORS
       State Vector x (16-Dimensional):
         x[1]  : Zone 1 Peak Temperature [deg C]
         x[2]  : Zone 2 Peak Temperature [deg C]
         x[3]  : Zone 3 Peak Temperature [deg C]
         x[4]  : Zone 4 Peak Temperature [deg C]
         x[5]  : Reactor Inlet Pressure [bar]
         x[6]  : Mid-Reactor Zone 2 Pressure [bar]
         x[7]  : Reactor Outlet Pressure [bar]
         x[8]  : Free Radical Concentration Zone 1 [mol/m3]
         x[9]  : Free Radical Concentration Zone 2 [mol/m3]
         x[10] : Free Radical Concentration Zone 3 [mol/m3]
         x[11] : Free Radical Concentration Zone 4 [mol/m3]
         x[12] : Per-Pass Cumulative Monomer Conversion [%]
         x[13] : Number-Average Molecular Weight Mn [kg/kmol]
         x[14] : Weight-Average Molecular Weight Mw [kg/kmol]
         x[15] : Maximum Inner Tube Wall Skin Temperature [deg C]
         x[16] : Polymer Melt Apparent Viscosity at Tube Wall [Pa*s]

       Control Vector u (8-Dimensional):
         u[1]  : Zone 1 Peroxide Pump Stroke [0..100 %]
         u[2]  : Zone 2 Peroxide Pump Stroke [0..100 %]
         u[3]  : Zone 3 Peroxide Pump Stroke [0..100 %]
         u[4]  : Zone 4 Peroxide Pump Stroke [0..100 %]
         u[5]  : Zone 1 Jacket Hot Water Mixing Valve [0..100 %]
         u[6]  : Zone 2 Jacket Hot Water Mixing Valve [0..100 %]
         u[7]  : Zone 3/4 Jacket Hot Water Mixing Valve [0..100 %]
         u[8]  : High-Pressure Let-Down Valve Servo Position [0..100 %]
       ====================================================================================================== *)
    xState_Est                      : ARRAY[1..16] OF REAL;
    xState_Pred                     : ARRAY[1..16] OF REAL;
    xState_Ref                      : ARRAY[1..16] OF REAL;
    xState_Err                      : ARRAY[1..16] OF REAL;
    uControl_Curr                   : ARRAY[1..8] OF REAL;
    uControl_Prev                   : ARRAY[1..8] OF REAL;
    uControl_Delta                  : ARRAY[1..8] OF REAL;
    uControl_Opt                    : ARRAY[1..8] OF REAL;
    yOutput_Pred                    : ARRAY[1..8] OF REAL;

    (* Discrete 16x16 System State Transition Matrix A *)
    aState_A                        : ARRAY[1..16, 1..16] OF REAL;
    (* Discrete 16x8 Input Distribution Matrix B *)
    bInput_B                        : ARRAY[1..16, 1..8] OF REAL;
    (* Discrete 8x16 Output Observation Matrix C *)
    cOutput_C                       : ARRAY[1..8, 1..16] OF REAL;
    (* Discrete 8x8 Direct Feed-Through Matrix D *)
    dDirect_D                       : ARRAY[1..8, 1..8] OF REAL;

    (* Model Predictive Control (MPC) Cost Weightings & Tuning *)
    qWeight_Q                       : ARRAY[1..16] OF REAL;
    rWeight_R                       : ARRAY[1..8] OF REAL;
    pWeight_P                       : ARRAY[1..16] OF REAL;
    uMin_Limits                     : ARRAY[1..8] OF REAL;
    uMax_Limits                     : ARRAY[1..8] OF REAL;
    deltaU_Limits                   : ARRAY[1..8] OF REAL;
    mpcGrad                         : ARRAY[1..8] OF REAL;
    mpcHessDiag                     : ARRAY[1..8] OF REAL;
    rMPC_StepSize                   : REAL := 0.042;
    iMPC_Iter                       : INT;
    iMPC_Horiz_Np                   : INT := 10;
    iMPC_Horiz_Nc                   : INT := 4;

    (* Loop index counters *)
    idx_i                           : INT;
    idx_j                           : INT;
    idx_k                           : INT;
    idx_m                           : INT;
    rAccum                          : REAL;
    rTempCalc                       : REAL;

    (* ======================================================================================================
       2oo3 TRIPLE MODULAR REDUNDANCY (TMR) ARCHITECTURAL DATA STRUCTURES
       ====================================================================================================== *)
    (* Channel Discrepancy Timers *)
    tonTMR_Inlet_Dev                : TON;
    tonTMR_Z1_Dev                   : TON;
    tonTMR_Z2_Dev                   : TON;
    tonTMR_Outlet_Dev               : TON;
    tonTMR_Hyper_Dev                : TON;
    tonTMR_T1_Dev                   : TON;
    tonTMR_T2_Dev                   : TON;
    tonTMR_T3_Dev                   : TON;
    tonTMR_T4_Dev                   : TON;
    tonTMR_dPdt1_Dev                : TON;
    tonTMR_dPdt2_Dev                : TON;

    (* Channel Health Bitflags *)
    bInlet_ChA_Healthy              : BOOL := TRUE;
    bInlet_ChB_Healthy              : BOOL := TRUE;
    bInlet_ChC_Healthy              : BOOL := TRUE;
    bZ1_ChA_Healthy                 : BOOL := TRUE;
    bZ1_ChB_Healthy                 : BOOL := TRUE;
    bZ1_ChC_Healthy                 : BOOL := TRUE;
    bZ2_ChA_Healthy                 : BOOL := TRUE;
    bZ2_ChB_Healthy                 : BOOL := TRUE;
    bZ2_ChC_Healthy                 : BOOL := TRUE;
    bOutlet_ChA_Healthy             : BOOL := TRUE;
    bOutlet_ChB_Healthy             : BOOL := TRUE;
    bOutlet_ChC_Healthy             : BOOL := TRUE;
    bHyper_ChA_Healthy              : BOOL := TRUE;
    bHyper_ChB_Healthy              : BOOL := TRUE;
    bHyper_ChC_Healthy              : BOOL := TRUE;
    bT1_ChA_Healthy                 : BOOL := TRUE;
    bT1_ChB_Healthy                 : BOOL := TRUE;
    bT1_ChC_Healthy                 : BOOL := TRUE;
    bT2_ChA_Healthy                 : BOOL := TRUE;
    bT2_ChB_Healthy                 : BOOL := TRUE;
    bT2_ChC_Healthy                 : BOOL := TRUE;
    bT3_ChA_Healthy                 : BOOL := TRUE;
    bT3_ChB_Healthy                 : BOOL := TRUE;
    bT3_ChC_Healthy                 : BOOL := TRUE;
    bT4_ChA_Healthy                 : BOOL := TRUE;
    bT4_ChB_Healthy                 : BOOL := TRUE;
    bT4_ChC_Healthy                 : BOOL := TRUE;
    bdPdt1_ChA_Healthy              : BOOL := TRUE;
    bdPdt1_ChB_Healthy              : BOOL := TRUE;
    bdPdt1_ChC_Healthy              : BOOL := TRUE;
    bdPdt2_ChA_Healthy              : BOOL := TRUE;
    bdPdt2_ChB_Healthy              : BOOL := TRUE;
    bdPdt2_ChC_Healthy              : BOOL := TRUE;

    (* Pairwise Discrepancies *)
    rDev_Inlet_AB                   : REAL;
    rDev_Inlet_BC                   : REAL;
    rDev_Inlet_AC                   : REAL;
    rDev_Z1_AB                      : REAL;
    rDev_Z1_BC                      : REAL;
    rDev_Z1_AC                      : REAL;
    rDev_T1_AB                      : REAL;
    rDev_T1_BC                      : REAL;
    rDev_T1_AC                      : REAL;
    rDev_T2_AB                      : REAL;
    rDev_T2_BC                      : REAL;
    rDev_T2_AC                      : REAL;

    (* Numerical Backward Difference dP/dt Filter Variables *)
    rPress_Inlet_Prev               : REAL := 2800.0;
    rPress_Outlet_Prev              : REAL := 2750.0;
    rCalculated_dPdt_Inlet          : REAL;
    rCalculated_dPdt_Outlet         : REAL;
    rDeltaTime_s                    : REAL := 0.020;

    (* ======================================================================================================
       CHEMICAL KINETICS, THERMODYNAMICS & FLUID RHEOLOGY MODEL CONSTANTS
       ====================================================================================================== *)
    c_R_gas                         : REAL := 8.31446;      (* Universal Gas Constant [J/(mol*K)] *)
    c_DeltaH_rxn                    : REAL := 95000.0;      (* Enthalpy of polymerization [J/mol C2H4] *)
    c_DeltaH_decomp                 : REAL := 126000.0;     (* Explosive decomposition enthalpy [J/mol] *)
    c_MW_Ethylene                   : REAL := 28.054;       (* Molecular weight of C2H4 [kg/kmol] *)
    c_MW_VAM                        : REAL := 86.09;        (* Molecular weight of Vinyl Acetate [kg/kmol] *)

    (* Arrhenius Rate Parameters: Pre-exponential factor A [1/s], Ea [J/mol], DeltaV_star [m3/mol] *)
    c_Ad_Peroxide_Z1                : REAL := 1.25E14;      (* TBPPI pre-exponential factor [1/s] *)
    c_Ea_Peroxide_Z1                : REAL := 122000.0;     (* TBPPI activation energy [J/mol] *)
    c_dV_Peroxide_Z1                : REAL := -1.85E-5;     (* TBPPI activation volume under pressure [m3/mol] *)

    c_Ad_Peroxide_Z2                : REAL := 3.80E14;      (* TBPO pre-exponential factor [1/s] *)
    c_Ea_Peroxide_Z2                : REAL := 129000.0;     (* TBPO activation energy [J/mol] *)
    c_dV_Peroxide_Z2                : REAL := -1.60E-5;     (* TBPO activation volume under pressure [m3/mol] *)

    c_Ad_Peroxide_Z3                : REAL := 8.40E14;      (* TBPEH pre-exponential factor [1/s] *)
    c_Ea_Peroxide_Z3                : REAL := 136000.0;     (* TBPEH activation energy [J/mol] *)
    c_dV_Peroxide_Z3                : REAL := -1.45E-5;     (* TBPEH activation volume under pressure [m3/mol] *)

    c_Ad_Peroxide_Z4                : REAL := 2.50E15;      (* DTBP pre-exponential factor [1/s] *)
    c_Ea_Peroxide_Z4                : REAL := 148000.0;     (* DTBP activation energy [J/mol] *)
    c_dV_Peroxide_Z4                : REAL := -1.20E-5;     (* DTBP activation volume under pressure [m3/mol] *)

    (* Propagation and Termination Kinetics *)
    c_Ap_Propagation                : REAL := 1.88E7;       (* Propagation pre-exponential [m3/(mol*s)] *)
    c_Ea_Propagation                : REAL := 38500.0;      (* Propagation activation energy [J/mol] *)
    c_dV_Propagation                : REAL := -1.95E-5;     (* Negative propagation activation volume [m3/mol] *)

    c_At_Termination                : REAL := 2.20E8;       (* Termination pre-exponential [m3/(mol*s)] *)
    c_Ea_Termination                : REAL := 12000.0;      (* Termination activation energy [J/mol] *)
    c_dV_Termination                : REAL := 1.30E-5;      (* Positive termination activation volume [m3/mol] *)

    (* Carreau-Yasuda Melt Rheology Parameters *)
    c_CY_ZeroShearVisc              : REAL := 12500.0;      (* Zero-shear melt viscosity eta_0 [Pa*s] *)
    c_CY_RelaxTime                  : REAL := 0.85;         (* Relaxation time lambda [s] *)
    c_CY_Yasuda_a                   : REAL := 0.65;         (* Yasuda parameter a *)
    c_CY_PowerLaw_n                 : REAL := 0.38;         (* Power law shear-thinning exponent n *)

    (* Reactor Geometric Dimensions *)
    c_Tube_InnerDiam_m              : REAL := 0.052;        (* Inner tube bore diameter [m] *)
    c_Tube_OuterDiam_m              : REAL := 0.162;        (* Outer tube diameter [m] *)
    c_Zone1_Length_m                : REAL := 550.0;        (* Zone 1 reaction length [m] *)
    c_Zone2_Length_m                : REAL := 550.0;        (* Zone 2 reaction length [m] *)
    c_Zone3_Length_m                : REAL := 500.0;        (* Zone 3 reaction length [m] *)
    c_Zone4_Length_m                : REAL := 550.0;        (* Zone 4 reaction length [m] *)
    c_Tube_CrossSection_m2          : REAL := 0.0021237;    (* Cross-sectional area [m2] *)

    (* Computed Kinetic Variables *)
    rRate_kd1                       : REAL;
    rRate_kd2                       : REAL;
    rRate_kd3                       : REAL;
    rRate_kd4                       : REAL;
    rRate_kp                        : REAL;
    rRate_kt                        : REAL;
    rDensity_Ethylene_kg_m3         : REAL;
    rConcentration_Monomer          : REAL;
    rRadical_Conc_Z1                : REAL;
    rRadical_Conc_Z2                : REAL;
    rRadical_Conc_Z3                : REAL;
    rRadical_Conc_Z4                : REAL;
    rExotherm_Heat_Z1               : REAL;
    rExotherm_Heat_Z2               : REAL;
    rExotherm_Heat_Z3               : REAL;
    rExotherm_Heat_Z4               : REAL;
    rOverall_U_Coeff                : REAL := 620.0;        (* Overall heat transfer coefficient [W/(m2*K)] *)

    (* ======================================================================================================
       OPERATIONAL FINITE STATE MACHINE SEQUENCING & TIMERS
       ====================================================================================================== *)
    iState                          : INT := 10;
    iPrevState                      : INT := 0;
    iSubPhase                       : INT := 0;
    tStateTimer                     : TON;
    tRampTimer                      : TON;
    tPurgeTimer                     : TON;
    tLightOffTimer                  : TON;
    tStabilizeTimer                 : TON;
    tDumpVerificationTimer          : TON;
    tPackingLeakTimer               : TON;

    (* Continuous Ramp Setpoints *)
    rRamp_ReactorPress_bar          : REAL := 150.0;
    rRamp_HyperSpeed_rpm            : REAL := 0.0;
    rRamp_JacketTemp_degC           : REAL := 40.0;
    rRamp_Peroxide_Z1_pct           : REAL := 0.0;
    rRamp_Peroxide_Z2_pct           : REAL := 0.0;
    rRamp_Peroxide_Z3_pct           : REAL := 0.0;
    rRamp_Peroxide_Z4_pct           : REAL := 0.0;

    (* ======================================================================================================
       ISA-18.2 TRIP SETPOINTS, HYSTERESIS DEADBANDS & BITFIELD INTERNAL LATCHES
       ====================================================================================================== *)
    (* Trip Limits *)
    c_Lim_Press_HH_bar              : REAL := 3180.0;
    c_Lim_Press_H_bar               : REAL := 3100.0;
    c_Lim_Press_L_bar               : REAL := 2400.0;
    c_Lim_Press_LL_bar              : REAL := 2100.0;

    c_Lim_Temp_HH_degC              : REAL := 318.0;
    c_Lim_Temp_H_degC               : REAL := 305.0;
    c_Lim_Temp_L_degC               : REAL := 170.0;
    c_Lim_Temp_LL_degC              : REAL := 140.0;

    c_Lim_dPdt_HH_bar_s             : REAL := 1500.0;       (* SIL-3 Explosive Decomposition Trip Point *)
    c_Lim_Vib_HH_mm_s               : REAL := 18.0;
    c_Lim_Vib_H_mm_s                : REAL := 12.0;
    c_Lim_PackingLeak_HH_kg_h       : REAL := 120.0;
    c_Lim_PackingLeak_H_kg_h        : REAL := 60.0;

    (* 1.5% Deadband Hysteresis Values *)
    c_Hyst_Press_bar                : REAL := 45.0;
    c_Hyst_Temp_degC                : REAL := 4.5;
    c_Hyst_dPdt_bar_s               : REAL := 50.0;
    c_Hyst_Vib_mm_s                 : REAL := 1.2;
    c_Hyst_Leak_kg_h                : REAL := 5.0;

    (* Latching Alarm Bools *)
    bAlarm_Press_HH                 : BOOL := FALSE;
    bAlarm_Press_H                  : BOOL := FALSE;
    bAlarm_Press_L                  : BOOL := FALSE;
    bAlarm_Press_LL                 : BOOL := FALSE;
    bAlarm_Temp_HH                  : BOOL := FALSE;
    bAlarm_Temp_H                   : BOOL := FALSE;
    bAlarm_Temp_L                   : BOOL := FALSE;
    bAlarm_Temp_LL                  : BOOL := FALSE;
    bAlarm_dPdt_Decomp_HH           : BOOL := FALSE;
    bAlarm_Vib_Hyper_HH             : BOOL := FALSE;
    bAlarm_Vib_Hyper_H              : BOOL := FALSE;
    bAlarm_PackingLeak_HH           : BOOL := FALSE;
    bAlarm_PackingLeak_H            : BOOL := FALSE;
    bAlarm_DumpAccum_Low            : BOOL := FALSE;
    bAlarm_HPLDV_Cavitation         : BOOL := FALSE;

    (* One-Shot and Execution Pulses *)
    bFirstScanDone                  : BOOL := FALSE;
    bStateChanged                   : BOOL := FALSE;
END_VAR
"""

