# scratch/gen_declarations.py
def get_declarations():
    return """VAR_INPUT
    (* ========================================================================= *)
    (* CLASS 1E SAFETY-CRITICAL 2oo3 TRIPLE MODULAR REDUNDANCY SENSOR CHANNELS  *)
    (* ========================================================================= *)
    
    (* Primary Steam Generator Narrow-Range Level Transmitters [-1000.0..1000.0 mm from NWL] *)
    fLT_NR_101A : LREAL := 0.0; (* SG Narrow Range Level Channel A [-1000.0..1000.0 mm] *)
    fLT_NR_101B : LREAL := 0.0; (* SG Narrow Range Level Channel B [-1000.0..1000.0 mm] *)
    fLT_NR_101C : LREAL := 0.0; (* SG Narrow Range Level Channel C [-1000.0..1000.0 mm] *)
    bLT_NR_101A_Valid : BOOL := TRUE; (* Health status discrete for LT_NR_101A [BOOL] *)
    bLT_NR_101B_Valid : BOOL := TRUE; (* Health status discrete for LT_NR_101B [BOOL] *)
    bLT_NR_101C_Valid : BOOL := TRUE; (* Health status discrete for LT_NR_101C [BOOL] *)

    (* Steam Generator Wide-Range Level Transmitters [0.0..15000.0 mm above tubesheet] *)
    fLT_WR_102A : LREAL := 10500.0; (* SG Wide Range Level Channel A [0.0..15000.0 mm] *)
    fLT_WR_102B : LREAL := 10500.0; (* SG Wide Range Level Channel B [0.0..15000.0 mm] *)
    fLT_WR_102C : LREAL := 10500.0; (* SG Wide Range Level Channel C [0.0..15000.0 mm] *)
    bLT_WR_102A_Valid : BOOL := TRUE; (* Health status discrete for LT_WR_102A [BOOL] *)
    bLT_WR_102B_Valid : BOOL := TRUE; (* Health status discrete for LT_WR_102B [BOOL] *)
    bLT_WR_102C_Valid : BOOL := TRUE; (* Health status discrete for LT_WR_102C [BOOL] *)

    (* Main Steam Line Drum Pressure Transmitters [0.0..100.0 bar] *)
    fPT_MS_201A : LREAL := 68.5; (* Main Steam Drum Pressure Channel A [0.0..100.0 bar] *)
    fPT_MS_201B : LREAL := 68.5; (* Main Steam Drum Pressure Channel B [0.0..100.0 bar] *)
    fPT_MS_201C : LREAL := 68.5; (* Main Steam Drum Pressure Channel C [0.0..100.0 bar] *)
    bPT_MS_201A_Valid : BOOL := TRUE; (* Health status discrete for PT_MS_201A [BOOL] *)
    bPT_MS_201B_Valid : BOOL := TRUE; (* Health status discrete for PT_MS_201B [BOOL] *)
    bPT_MS_201C_Valid : BOOL := TRUE; (* Health status discrete for PT_MS_201C [BOOL] *)

    (* Main Steam Mass Flow Rate Transmitters [0.0..2500.0 t/h] *)
    fFT_MS_301A : LREAL := 1850.0; (* Main Steam Mass Flow Rate Channel A [0.0..2500.0 t/h] *)
    fFT_MS_301B : LREAL := 1850.0; (* Main Steam Mass Flow Rate Channel B [0.0..2500.0 t/h] *)
    fFT_MS_301C : LREAL := 1850.0; (* Main Steam Mass Flow Rate Channel C [0.0..2500.0 t/h] *)
    bFT_MS_301A_Valid : BOOL := TRUE; (* Health status discrete for FT_MS_301A [BOOL] *)
    bFT_MS_301B_Valid : BOOL := TRUE; (* Health status discrete for FT_MS_301B [BOOL] *)
    bFT_MS_301C_Valid : BOOL := TRUE; (* Health status discrete for FT_MS_301C [BOOL] *)

    (* Main Feedwater Mass Flow Rate Transmitters [0.0..2500.0 t/h] *)
    fFT_FW_401A : LREAL := 1850.0; (* Main Feedwater Mass Flow Rate Channel A [0.0..2500.0 t/h] *)
    fFT_FW_401B : LREAL := 1850.0; (* Main Feedwater Mass Flow Rate Channel B [0.0..2500.0 t/h] *)
    fFT_FW_401C : LREAL := 1850.0; (* Main Feedwater Mass Flow Rate Channel C [0.0..2500.0 t/h] *)
    bFT_FW_401A_Valid : BOOL := TRUE; (* Health status discrete for FT_FW_401A [BOOL] *)
    bFT_FW_401B_Valid : BOOL := TRUE; (* Health status discrete for FT_FW_401B [BOOL] *)
    bFT_FW_401C_Valid : BOOL := TRUE; (* Health status discrete for FT_FW_401C [BOOL] *)

    (* Reactor Coolant System (RCS) Cold Leg Return Temperatures [250.0..330.0 deg C] *)
    fTE_CL_501A : LREAL := 292.0; (* RCS Cold Leg Temperature Channel A [250.0..330.0 deg C] *)
    fTE_CL_501B : LREAL := 292.0; (* RCS Cold Leg Temperature Channel B [250.0..330.0 deg C] *)
    fTE_CL_501C : LREAL := 292.0; (* RCS Cold Leg Temperature Channel C [250.0..330.0 deg C] *)
    bTE_CL_501A_Valid : BOOL := TRUE; (* Health status discrete for TE_CL_501A [BOOL] *)
    bTE_CL_501B_Valid : BOOL := TRUE; (* Health status discrete for TE_CL_501B [BOOL] *)
    bTE_CL_501C_Valid : BOOL := TRUE; (* Health status discrete for TE_CL_501C [BOOL] *)

    (* Secondary Side N-16 / Noble Gas SGTR Radiation Monitors [0.0..1.0E7 Bq/m3] *)
    fRE_SGTR_601A : LREAL := 120.0; (* SGTR Line N-16 Radiation Channel A [0.0..1.0E7 Bq/m3] *)
    fRE_SGTR_601B : LREAL := 120.0; (* SGTR Line N-16 Radiation Channel B [0.0..1.0E7 Bq/m3] *)
    fRE_SGTR_601C : LREAL := 120.0; (* SGTR Line N-16 Radiation Channel C [0.0..1.0E7 Bq/m3] *)
    bRE_SGTR_601A_Valid : BOOL := TRUE; (* Health status discrete for RE_SGTR_601A [BOOL] *)
    bRE_SGTR_601B_Valid : BOOL := TRUE; (* Health status discrete for RE_SGTR_601B [BOOL] *)
    bRE_SGTR_601C_Valid : BOOL := TRUE; (* Health status discrete for RE_SGTR_601C [BOOL] *)

    (* Auxiliary Thermal-Hydraulic Plant Transmitters *)
    fTE_HL_502 : LREAL := 326.5; (* Primary Coolant Hot Leg Inlet Temperature [280.0..350.0 deg C] *)
    fTE_FW_503 : LREAL := 226.0; (* High Pressure Economizer Feedwater Temp [120.0..240.0 deg C] *)
    fPT_TURB_202 : LREAL := 45.2; (* HP Turbine First-Stage Impulse Pressure [0.0..60.0 bar] *)
    fNI_ReactorThermalPower : LREAL := 100.0; (* Nuclear Instrumentation Reactor Power [0.0..120.0 %] *)
    fPT_COND_203 : LREAL := 48.0; (* Main Surface Condenser Backpressure [10.0..1000.0 mbar] *)

    (* Safety System Interlocks, Operator Commands, & Supervisory Flags *)
    bEnableControlBlock : BOOL := TRUE; (* Master Software Enable Supervisory Command [BOOL] *)
    bMasterResetTrip : BOOL := FALSE; (* Master Safety Latch Reset Pushbutton [BOOL] *)
    bManualControlSelect : BOOL := FALSE; (* Operator Manual Override Station Selection [BOOL] *)
    bReactorScramActive : BOOL := FALSE; (* Reactor Protection System (RPS) Hardwired Scram [BOOL] *)
    bTurbineTripActive : BOOL := FALSE; (* Main Turbine Trip Electro-Hydraulic Protection [BOOL] *)
    bMSIV_ClosureActive : BOOL := FALSE; (* Main Steam Isolation Valves Fast Closure Interlock [BOOL] *)
    bLossOfMainFeedwater : BOOL := FALSE; (* Loss of All Operating Main Feedwater Pumps [BOOL] *)
    bStationBlackoutSignal : BOOL := FALSE; (* Station Blackout (SBO) Loss of Offsite & Onsite AC [BOOL] *)
    bSafetyInjectionActuated : BOOL := FALSE; (* Primary Side Safety Injection (SI) Actuation [BOOL] *)

    (* Operator Manual Modulation Setpoints & Dynamic Trims *)
    fManualDemand_MFRV : LREAL := 75.0; (* Operator Manual Station Demand for MFRV [0.0..100.0 %] *)
    fManualDemand_BPV : LREAL := 0.0; (* Operator Manual Station Demand for BPV [0.0..100.0 %] *)
    fManualDemand_AFW : LREAL := 0.0; (* Operator Manual Station Demand for AFW [0.0..100.0 %] *)
    fOperatorLevelBias_mm : LREAL := 0.0; (* Operator Trim Offset for Narrow Range Level [-200.0..200.0 mm] *)
    fCycleTime_Ts : LREAL := 0.025; (* Discrete Task Scan Interval Delta Time [0.010..0.100 s] *)
END_VAR
VAR_OUTPUT
    (* ========================================================================= *)
    (* ACTUATOR DEMANDS, TRIPS, ALARMS, OBSERVER STATES, & TELEMETRY REGISTERS   *)
    (* ========================================================================= *)
    
    (* Primary Actuator Modulating Commands *)
    fMFRV_PositionDemand : LREAL := 0.0; (* Main Feedwater Regulating Valve Demand [0.0..100.0 %] *)
    fBPV_PositionDemand : LREAL := 0.0; (* Low Power Bypass Feedwater Valve Demand [0.0..100.0 %] *)
    fAFW_MotorPump1_SpeedDemand : LREAL := 0.0; (* MDAFW Pump 1 Modulating Speed Demand [0.0..100.0 %] *)
    fAFW_MotorPump2_SpeedDemand : LREAL := 0.0; (* MDAFW Pump 2 Modulating Speed Demand [0.0..100.0 %] *)
    fAFW_TurbinePump_GovernorDemand : LREAL := 0.0; (* TDAFW Turbine Steam Governor Demand [0.0..100.0 %] *)

    (* Safety-Critical Discrete Trip & Actuation Commands *)
    bMFRV_FastTripClosureCmd : BOOL := FALSE; (* MFRV Fast Hydraulic Trip Close Solenoid [BOOL] *)
    bBPV_FastTripClosureCmd : BOOL := FALSE; (* BPV Fast Hydraulic Trip Close Solenoid [BOOL] *)
    bAFW_MotorPump1_AutoStartCmd : BOOL := FALSE; (* Motor AFW Pump 1 Breaker Close Auto-Start [BOOL] *)
    bAFW_MotorPump2_AutoStartCmd : BOOL := FALSE; (* Motor AFW Pump 2 Breaker Close Auto-Start [BOOL] *)
    bAFW_TurbinePump_AutoStartCmd : BOOL := FALSE; (* Turbine AFW Pump Steam Admission Open [BOOL] *)
    bReactorScramSG_TripReq : BOOL := FALSE; (* SG Trip Request to Reactor Protection System [BOOL] *)
    bTurbineTripSG_Req : BOOL := FALSE; (* SG Level High-High Turbine Trip Request [BOOL] *)
    bMSIV_SG_IsolationReq : BOOL := FALSE; (* Secondary Side Main Steam Line Isolation Cmd [BOOL] *)
    bBlowdownIsolationCmd : BOOL := FALSE; (* SG Continuous Blowdown Isolation Trip Close [BOOL] *)

    (* Validated 2oo3 TMR Process Measurements *)
    fVotedNarrowRangeLevel_mm : LREAL := 0.0; (* 2oo3 TMR Validated Narrow Range Water Level [-1000.0..1000.0 mm] *)
    fVotedWideRangeLevel_mm : LREAL := 10500.0; (* 2oo3 TMR Validated Wide Range Water Level [0.0..15000.0 mm] *)
    fVotedDrumPressure_bar : LREAL := 68.5; (* 2oo3 TMR Validated Main Steam Drum Pressure [0.0..100.0 bar] *)
    fVotedSteamFlow_t_h : LREAL := 1850.0; (* 2oo3 TMR Validated Main Steam Mass Flow Rate [0.0..2500.0 t/h] *)
    fVotedFeedwaterFlow_t_h : LREAL := 1850.0; (* 2oo3 TMR Validated Main Feedwater Mass Flow Rate [0.0..2500.0 t/h] *)
    fVotedColdLegTemp_degC : LREAL := 292.0; (* 2oo3 TMR Validated RCS Cold Leg Temperature [250.0..330.0 deg C] *)
    fVotedSGTR_Rad_Bq_m3 : LREAL := 120.0; (* 2oo3 TMR Validated N-16 Steam Line Radiation [0.0..1.0E7 Bq/m3] *)

    (* Kalman Filter Corrected Cyber-Physical States *)
    fStateSpaceEstimatedLevel_mm : LREAL := 0.0; (* Estimated True Physical Water Level [mm] *)
    fStateSpaceEstimatedDowncomerFlow_kg_s : LREAL := 513.8; (* Estimated Downcomer Recirculation Flow [kg/s] *)
    fStateSpaceEstimatedVoidFraction : LREAL := 0.425; (* Estimated Riser Mean Void Fraction [0.0..1.0] *)
    fStateSpaceEstimatedHeatTransfer_MW : LREAL := 950.0; (* Estimated Primary-Secondary Heat Transfer [MW] *)
    fStateSpaceEstimatedPressure_bar : LREAL := 68.5; (* Estimated Steam Drum Saturated Pressure [bar] *)
    fStateSpaceEstimatedColdLegTemp_degC : LREAL := 292.0; (* Estimated Cold Leg Return Temperature [deg C] *)
    fStateSpaceEstimatedValveTrim_pct : LREAL := 75.0; (* Estimated Effective Valve Trim Position [%] *)
    fStateSpaceEstimatedNMP_LeadLag_mm : LREAL := 0.0; (* Estimated Shrink/Swell Dynamic State [mm] *)

    (* MPC and Dynamic Inverse Compensation Metrics *)
    fShrinkSwellCompensatedDemand_pct : LREAL := 0.0; (* Dynamic Feedforward Anti-Shrink/Swell Bias [%] *)
    fMPC_ComputedCostJ : LREAL := 0.0; (* Receding Horizon Optimal Cost Function Value [cost] *)
    nActiveFSMStateID : DINT := 0; (* Current Active Deterministic State Machine Stage [0..13] *)

    (* Bit-Packed 32-Bit Telemetry Words & Safety Status *)
    dwStatusWord1 : DWORD := 16#00000000; (* Bit-Packed Operational Telemetry Status Word 1 [DWORD] *)
    dwStatusWord2 : DWORD := 16#00000000; (* Bit-Packed Operational Telemetry Status Word 2 [DWORD] *)
    dwAlarmWord1 : DWORD := 16#00000000; (* ISA-18.2 Process Trip and Alert Alarm Word 1 [DWORD] *)
    dwAlarmWord2 : DWORD := 16#00000000; (* ISA-18.2 TMR Discrepancy & Diagnostic Word 2 [DWORD] *)
    dwFirstOutWord : DWORD := 16#00000000; (* IEEE 603 / ISA-18.2 Latched First-Out Trip Cause [DWORD] *)
    bSystemHealthy : BOOL := TRUE; (* Overall System Healthy Integrity Status [BOOL] *)
    bDegradedTMR : BOOL := FALSE; (* TMR Triple Redundancy Operating in Degraded Mode [BOOL] *)
    bTripLockoutActive : BOOL := FALSE; (* Safety Trip Lockout Latched Until Master Reset [BOOL] *)
END_VAR
VAR
    (* ========================================================================= *)
    (* INTERNAL DISCRETE STATE-SPACE MATRICES, MPC ARRAYS, TMR TIMERS, & ALARMS  *)
    (* ========================================================================= *)
    
    (* Discrete State-Space Model Matrices (Sampled at Ts = 0.025 s) *)
    A_Matrix : ARRAY[1..8, 1..8] OF LREAL; (* Discrete System Dynamics Matrix A (8x8) *)
    B_Matrix : ARRAY[1..8, 1..5] OF LREAL; (* Discrete Control Input Matrix B (8x5) *)
    C_Matrix : ARRAY[1..5, 1..8] OF LREAL; (* Discrete Output Measurement Matrix C (5x8) *)
    D_Matrix : ARRAY[1..5, 1..5] OF LREAL; (* Discrete Direct Feedthrough Matrix D (5x5) *)
    L_Matrix : ARRAY[1..8, 1..5] OF LREAL; (* Kalman Filter Observer Gain Matrix L (8x5) *)

    (* State Vector and Observation Arrays *)
    x_hat : ARRAY[1..8] OF LREAL; (* Corrected State Estimates: x1..x8 *)
    x_pred : ARRAY[1..8] OF LREAL; (* A-Priori One-Step Ahead State Predictions *)
    y_meas : ARRAY[1..5] OF LREAL; (* Measured Process Output Vector *)
    y_pred : ARRAY[1..5] OF LREAL; (* Predicted Process Output Vector *)
    innov : ARRAY[1..5] OF LREAL; (* Measurement Residual / Innovation Vector *)
    u_vector : ARRAY[1..5] OF LREAL; (* Current Process Inputs Vector *)

    (* MPC Quadratic Cost Weighting Matrices & Horizon Variables *)
    Q_diag : ARRAY[1..8] OF LREAL; (* State Tracking Error Penalties (8x8 Diagonal) *)
    R_diag : ARRAY[1..2] OF LREAL; (* Control Actuation Effort Penalties (2x2 Diagonal) *)
    S_diag : ARRAY[1..2] OF LREAL; (* Control Slew Rate Penalties (2x2 Diagonal) *)
    P_diag : ARRAY[1..8] OF LREAL; (* Terminal State Error Penalties (8x8 Diagonal) *)

    (* Receding Horizon Prediction Arrays (Horizon N = 5 Steps) *)
    u_mpc_horiz : ARRAY[1..5, 1..2] OF LREAL; (* Control Trajectory [Step, Input] *)
    x_mpc_horiz : ARRAY[1..5, 1..8] OF LREAL; (* State Trajectory Prediction [Step, State] *)
    lambda_mpc : ARRAY[1..5, 1..8] OF LREAL; (* Adjoint Costate Backpropagation Vector *)
    grad_u_mpc : ARRAY[1..5, 1..2] OF LREAL; (* Projected Cost Gradients w.r.t Inputs *)
    r_mpc_ref : ARRAY[1..5, 1..8] OF LREAL; (* Reference Trajectory Setpoints *)
    u_prev_cycle : ARRAY[1..2] OF LREAL; (* Manipulated Variable Memory from Previous Scan *)

    (* Dynamic Inverse Response (Shrink/Swell) Filter Registers *)
    fSteamFlow_Filtered_Prev : LREAL := 1850.0;
    fFeedwaterFlow_Filtered_Prev : LREAL := 1850.0;
    fDerivSteamFlow : LREAL := 0.0;
    fDerivFeedwaterFlow : LREAL := 0.0;
    fLeadLagInternalState : LREAL := 0.0;
    fAntiSwellBias : LREAL := 0.0;

    (* 2oo3 TMR Triple Modular Redundancy Channel Structures *)
    (* Channel 1: Narrow Range Level *)
    fDev_LT_NR_AB : LREAL := 0.0;
    fDev_LT_NR_BC : LREAL := 0.0;
    fDev_LT_NR_CA : LREAL := 0.0;
    tDiscrep_LT_NR_AB : LREAL := 0.0;
    tDiscrep_LT_NR_BC : LREAL := 0.0;
    tDiscrep_LT_NR_CA : LREAL := 0.0;
    bDiscrep_LT_NR_AB : BOOL := FALSE;
    bDiscrep_LT_NR_BC : BOOL := FALSE;
    bDiscrep_LT_NR_CA : BOOL := FALSE;
    nHealthyCount_LT_NR : INT := 3;
    bChA_Healthy_LT_NR : BOOL := TRUE;
    bChB_Healthy_LT_NR : BOOL := TRUE;
    bChC_Healthy_LT_NR : BOOL := TRUE;
    fPrevVal_LT_NR_A : LREAL := 0.0;
    fPrevVal_LT_NR_B : LREAL := 0.0;
    fPrevVal_LT_NR_C : LREAL := 0.0;

    (* Channel 2: Wide Range Level *)
    fDev_LT_WR_AB : LREAL := 0.0;
    fDev_LT_WR_BC : LREAL := 0.0;
    fDev_LT_WR_CA : LREAL := 0.0;
    tDiscrep_LT_WR_AB : LREAL := 0.0;
    tDiscrep_LT_WR_BC : LREAL := 0.0;
    tDiscrep_LT_WR_CA : LREAL := 0.0;
    bDiscrep_LT_WR_AB : BOOL := FALSE;
    bDiscrep_LT_WR_BC : BOOL := FALSE;
    bDiscrep_LT_WR_CA : BOOL := FALSE;
    nHealthyCount_LT_WR : INT := 3;
    bChA_Healthy_LT_WR : BOOL := TRUE;
    bChB_Healthy_LT_WR : BOOL := TRUE;
    bChC_Healthy_LT_WR : BOOL := TRUE;
    fPrevVal_LT_WR_A : LREAL := 10500.0;
    fPrevVal_LT_WR_B : LREAL := 10500.0;
    fPrevVal_LT_WR_C : LREAL := 10500.0;

    (* Channel 3: Drum Pressure *)
    fDev_PT_MS_AB : LREAL := 0.0;
    fDev_PT_MS_BC : LREAL := 0.0;
    fDev_PT_MS_CA : LREAL := 0.0;
    tDiscrep_PT_MS_AB : LREAL := 0.0;
    tDiscrep_PT_MS_BC : LREAL := 0.0;
    tDiscrep_PT_MS_CA : LREAL := 0.0;
    bDiscrep_PT_MS_AB : BOOL := FALSE;
    bDiscrep_PT_MS_BC : BOOL := FALSE;
    bDiscrep_PT_MS_CA : BOOL := FALSE;
    nHealthyCount_PT_MS : INT := 3;
    bChA_Healthy_PT_MS : BOOL := TRUE;
    bChB_Healthy_PT_MS : BOOL := TRUE;
    bChC_Healthy_PT_MS : BOOL := TRUE;
    fPrevVal_PT_MS_A : LREAL := 68.5;
    fPrevVal_PT_MS_B : LREAL := 68.5;
    fPrevVal_PT_MS_C : LREAL := 68.5;

    (* Channel 4: Steam Mass Flow *)
    fDev_FT_MS_AB : LREAL := 0.0;
    fDev_FT_MS_BC : LREAL := 0.0;
    fDev_FT_MS_CA : LREAL := 0.0;
    tDiscrep_FT_MS_AB : LREAL := 0.0;
    tDiscrep_FT_MS_BC : LREAL := 0.0;
    tDiscrep_FT_MS_CA : LREAL := 0.0;
    bDiscrep_FT_MS_AB : BOOL := FALSE;
    bDiscrep_FT_MS_BC : BOOL := FALSE;
    bDiscrep_FT_MS_CA : BOOL := FALSE;
    nHealthyCount_FT_MS : INT := 3;
    bChA_Healthy_FT_MS : BOOL := TRUE;
    bChB_Healthy_FT_MS : BOOL := TRUE;
    bChC_Healthy_FT_MS : BOOL := TRUE;
    fPrevVal_FT_MS_A : LREAL := 1850.0;
    fPrevVal_FT_MS_B : LREAL := 1850.0;
    fPrevVal_FT_MS_C : LREAL := 1850.0;

    (* Channel 5: Feedwater Mass Flow *)
    fDev_FT_FW_AB : LREAL := 0.0;
    fDev_FT_FW_BC : LREAL := 0.0;
    fDev_FT_FW_CA : LREAL := 0.0;
    tDiscrep_FT_FW_AB : LREAL := 0.0;
    tDiscrep_FT_FW_BC : LREAL := 0.0;
    tDiscrep_FT_FW_CA : LREAL := 0.0;
    bDiscrep_FT_FW_AB : BOOL := FALSE;
    bDiscrep_FT_FW_BC : BOOL := FALSE;
    bDiscrep_FT_FW_CA : BOOL := FALSE;
    nHealthyCount_FT_FW : INT := 3;
    bChA_Healthy_FT_FW : BOOL := TRUE;
    bChB_Healthy_FT_FW : BOOL := TRUE;
    bChC_Healthy_FT_FW : BOOL := TRUE;
    fPrevVal_FT_FW_A : LREAL := 1850.0;
    fPrevVal_FT_FW_B : LREAL := 1850.0;
    fPrevVal_FT_FW_C : LREAL := 1850.0;

    (* Channel 6: Cold Leg Temperature *)
    fDev_TE_CL_AB : LREAL := 0.0;
    fDev_TE_CL_BC : LREAL := 0.0;
    fDev_TE_CL_CA : LREAL := 0.0;
    tDiscrep_TE_CL_AB : LREAL := 0.0;
    tDiscrep_TE_CL_BC : LREAL := 0.0;
    tDiscrep_TE_CL_CA : LREAL := 0.0;
    bDiscrep_TE_CL_AB : BOOL := FALSE;
    bDiscrep_TE_CL_BC : BOOL := FALSE;
    bDiscrep_TE_CL_CA : BOOL := FALSE;
    nHealthyCount_TE_CL : INT := 3;
    bChA_Healthy_TE_CL : BOOL := TRUE;
    bChB_Healthy_TE_CL : BOOL := TRUE;
    bChC_Healthy_TE_CL : BOOL := TRUE;
    fPrevVal_TE_CL_A : LREAL := 292.0;
    fPrevVal_TE_CL_B : LREAL := 292.0;
    fPrevVal_TE_CL_C : LREAL := 292.0;

    (* Channel 7: Secondary SGTR Radiation *)
    fDev_RE_SGTR_AB : LREAL := 0.0;
    fDev_RE_SGTR_BC : LREAL := 0.0;
    fDev_RE_SGTR_CA : LREAL := 0.0;
    tDiscrep_RE_SGTR_AB : LREAL := 0.0;
    tDiscrep_RE_SGTR_BC : LREAL := 0.0;
    tDiscrep_RE_SGTR_CA : LREAL := 0.0;
    bDiscrep_RE_SGTR_AB : BOOL := FALSE;
    bDiscrep_RE_SGTR_BC : BOOL := FALSE;
    bDiscrep_RE_SGTR_CA : BOOL := FALSE;
    nHealthyCount_RE_SGTR : INT := 3;
    bChA_Healthy_RE_SGTR : BOOL := TRUE;
    bChB_Healthy_RE_SGTR : BOOL := TRUE;
    bChC_Healthy_RE_SGTR : BOOL := TRUE;
    fPrevVal_RE_SGTR_A : LREAL := 120.0;
    fPrevVal_RE_SGTR_B : LREAL := 120.0;
    fPrevVal_RE_SGTR_C : LREAL := 120.0;

    (* Deterministic 14-Stage FSM State Variables *)
    eCurrentState : DINT := 0;
    ePreviousState : DINT := 0;
    fStateElapsedTime : LREAL := 0.0;
    bStateFirstScan : BOOL := TRUE;
    fBumplessTransferTimer : LREAL := 0.0;
    fTransferRampRate : LREAL := 0.0;
    fBypassValveHoldPosition : LREAL := 0.0;
    fMainValveHoldPosition : LREAL := 0.0;
    fProgrammedLevelTarget : LREAL := 0.0;
    fFilteredLevelTarget : LREAL := 0.0;
    fDecayHeatCooldownRate : LREAL := 0.0;

    (* ISA-18.2 Process Alarm Engine Variables *)
    bTrip_Level_HH : BOOL := FALSE;
    bAlert_Level_H : BOOL := FALSE;
    bWarning_Level_L : BOOL := FALSE;
    bTrip_Level_LL : BOOL := FALSE;
    bTrip_Pressure_HH : BOOL := FALSE;
    bAlert_Pressure_H : BOOL := FALSE;
    bWarning_Pressure_L : BOOL := FALSE;
    bTrip_Pressure_LL : BOOL := FALSE;
    bAlert_FlowMismatch_H : BOOL := FALSE;
    bTrip_SGTR_Rad_HH : BOOL := FALSE;
    bAlert_TMR_Discrepancy : BOOL := FALSE;
    bTrip_SensorLoss_Fatal : BOOL := FALSE;
    bAlert_FeedwaterTemp_L : BOOL := FALSE;
    bAlert_VoidFractionSurge : BOOL := FALSE;
    bTrip_OverfillRisk : BOOL := FALSE;
    bTrip_DryoutRisk : BOOL := FALSE;

    (* Alarm Debounce and Latching Registers *)
    tTimer_Level_HH : LREAL := 0.0;
    tTimer_Level_H : LREAL := 0.0;
    tTimer_Level_L : LREAL := 0.0;
    tTimer_Level_LL : LREAL := 0.0;
    tTimer_Pressure_HH : LREAL := 0.0;
    tTimer_Pressure_H : LREAL := 0.0;
    tTimer_Pressure_L : LREAL := 0.0;
    tTimer_Pressure_LL : LREAL := 0.0;
    tTimer_FlowMismatch : LREAL := 0.0;
    tTimer_SGTR_Rad : LREAL := 0.0;
    bFirstOutLocked : BOOL := FALSE;

    (* General Execution Metrics, Counters, & Scratch Indices *)
    bInitialized : BOOL := FALSE;
    nExecutionCycleCounter : ULINT := 0;
    fModelScanTime_s : LREAL := 0.025;
    nLoopIdx1 : INT := 0;
    nLoopIdx2 : INT := 0;
    nStepIdx : INT := 0;
    nIterIdx : INT := 0;
    fTempSum : LREAL := 0.0;
    fTempDelta : LREAL := 0.0;
    fTrialInput : LREAL := 0.0;
    fMaxAllowedDelta : LREAL := 0.0;
    fBaseSetpoint : LREAL := 0.0;
    fPowerFraction : LREAL := 1.0;
END_VAR
"""
