# subsea_boosting_builder/st_var_declarations.py

def get_var_declarations():
    return """VAR
    (* Execution Control & Initialization Flags *)
    bFirstScanDone                              : BOOL := FALSE;    (* Cold boot system initialization completed flag *)
    rScanTime_s                                 : REAL := 0.020;    (* Discrete sample time Ts [s] *)
    rTime_Accumulator_s                         : REAL := 0.0;      (* Global continuous running time accumulator [s] *)

    (* ==================================================================================================== *)
    (* 1. DISCRETE STATE-SPACE MATRICES & SYSTEM VECTORS (6x6 Full Coupled System)                           *)
    (* States:                                                                                              *)
    (*   x[0]: P_suction deviation [bar]                                                                    *)
    (*   x[1]: P_discharge deviation [bar]                                                                  *)
    (*   x[2]: GVF Gas Volume Fraction deviation [%]                                                        *)
    (*   x[3]: c_acoustic mixture sonic velocity deviation [m/s]                                            *)
    (*   x[4]: Delta_P twin-screw differential pressure deviation [bar]                                     *)
    (*   x[5]: tau_hyd pump absorbed hydraulic torque deviation [kNm]                                       *)
    (* Controls:                                                                                            *)
    (*   u[0]: VFD Motor Speed [RPM] (1200..4500)                                                           *)
    (*   u[1]: Anti-Surge Fast Kickback Valve Position [%] (0..100)                                         *)
    (*   u[2]: MEG Thermodynamic Hydrate Inhibitor Metering Valve [%] (0..100)                              *)
    (*   u[3]: Barrier Fluid Accumulator Charge Valve [%] (0..100)                                          *)
    (*   u[4]: Subsea Production Export Choke Trim [%] (0..100)                                             *)
    (*   u[5]: High-GVF Mist Cooling Liquid Recycle Valve [%] (0..100)                                      *)
    (* ==================================================================================================== *)
    matA                                        : ARRAY[0..5, 0..5] OF REAL; (* Discrete System Transition Matrix A *)
    matB                                        : ARRAY[0..5, 0..5] OF REAL; (* Discrete Control Input Matrix B *)
    matC                                        : ARRAY[0..5, 0..5] OF REAL; (* Discrete Output Measurement Matrix C *)
    matD                                        : ARRAY[0..5, 0..5] OF REAL; (* Discrete Direct Feedthrough Matrix D *)
    matL                                        : ARRAY[0..5, 0..5] OF REAL; (* Luenberger Kalman Innovation Observer Matrix L *)

    (* State & Control Vectors *)
    vecX                                        : ARRAY[0..5] OF REAL; (* Physical state absolute vector *)
    vecX_est                                    : ARRAY[0..5] OF REAL; (* Observer estimated state vector *)
    vecX_pred                                   : ARRAY[0..5] OF REAL; (* Single-step predictive state vector *)
    vecX_ref                                    : ARRAY[0..5] OF REAL; (* State reference setpoint vector *)
    vecX_nominal                                : ARRAY[0..5] OF REAL; (* Operating linearization point equilibrium vector *)
    vecX_err                                    : ARRAY[0..5] OF REAL; (* State tracking error vector e = x_est - x_ref *)

    vecY_meas                                   : ARRAY[0..5] OF REAL; (* Measured system output vector *)
    vecY_est                                    : ARRAY[0..5] OF REAL; (* Observer estimated output vector *)
    vecY_err                                    : ARRAY[0..5] OF REAL; (* Innovation residual error vector *)

    vecU                                        : ARRAY[0..5] OF REAL; (* Commanded actuator control vector *)
    vecU_prev                                   : ARRAY[0..5] OF REAL; (* Previous cycle actuator control vector *)
    vecU_cmd                                    : ARRAY[0..5] OF REAL; (* Unconstrained optimal control demand *)
    vecU_target                                 : ARRAY[0..5] OF REAL; (* Nominal target control equilibrium setpoint *)
    vecU_rate                                   : ARRAY[0..5] OF REAL; (* Instantaneous actuator slew rate [units/s] *)
    vecU_min                                    : ARRAY[0..5] OF REAL; (* Physical lower actuator saturation boundaries *)
    vecU_max                                    : ARRAY[0..5] OF REAL; (* Physical upper actuator saturation boundaries *)
    vecU_slew_max                               : ARRAY[0..5] OF REAL; (* Maximum allowable actuator slew velocity *)

    (* MPC Quadratic Cost Functional Weights *)
    vecQ_weight                                 : ARRAY[0..5] OF REAL; (* State error diagonal quadratic weights Q *)
    vecR_weight                                 : ARRAY[0..5] OF REAL; (* Control effort diagonal quadratic weights R *)
    vecR_rate_weight                            : ARRAY[0..5] OF REAL; (* Control slew rate quadratic weights R_rate *)
    vecP_terminal                               : ARRAY[0..5] OF REAL; (* Terminal state stability Lyapunov weights P *)

    (* Receding-Horizon MPC Optimization Trajectories (Np = 10, Nc = 5) *)
    matX_traj                                   : ARRAY[0..10, 0..5] OF REAL; (* Multi-step state prediction rollout *)
    matU_traj                                   : ARRAY[0..9, 0..5] OF REAL;  (* Multi-step control sequence candidate *)
    matGrad_U                                   : ARRAY[0..9, 0..5] OF REAL;  (* Unrolled cost functional gradient *)
    rAlpha_step                                 : REAL := 0.0085;             (* Projected gradient descent step size *)
    rCost_State                                 : REAL := 0.0;                (* Instantaneous prediction state penalty *)
    rCost_Control                               : REAL := 0.0;                (* Instantaneous control energy penalty *)
    rCost_Slew                                  : REAL := 0.0;                (* Instantaneous control rate penalty *)
    rCost_Terminal                              : REAL := 0.0;                (* Prediction terminal boundary cost *)
    rCost_Total                                 : REAL := 0.0;                (* Total accumulated MPC cost functional *)

    (* Loop & Matrix Indices *)
    mIdx                                        : INT := 0;
    nIdx                                        : INT := 0;
    pIdx                                        : INT := 0;
    nIterMPC                                    : INT := 0;
    nStepMPC                                    : INT := 0;

    (* ==================================================================================================== *)
    (* 2. 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING STRUCTURES                                      *)
    (* ==================================================================================================== *)
    (* Suction Pressure TMR Engine *)
    rSuction_ChA_Val                            : REAL := 45.0;
    rSuction_ChB_Val                            : REAL := 45.0;
    rSuction_ChC_Val                            : REAL := 45.0;
    bSuction_ChA_Healthy                        : BOOL := TRUE;
    bSuction_ChB_Healthy                        : BOOL := TRUE;
    bSuction_ChC_Healthy                        : BOOL := TRUE;
    bSuction_ChA_Degraded                       : BOOL := FALSE;
    bSuction_ChB_Degraded                       : BOOL := FALSE;
    bSuction_ChC_Degraded                       : BOOL := FALSE;
    rSuction_Diff_AB                            : REAL := 0.0;
    rSuction_Diff_BC                            : REAL := 0.0;
    rSuction_Diff_CA                            : REAL := 0.0;
    tSuction_DiscTimer_AB_s                     : REAL := 0.0;
    tSuction_DiscTimer_BC_s                     : REAL := 0.0;
    tSuction_DiscTimer_CA_s                     : REAL := 0.0;
    nSuction_VotingMode                         : INT := 3; (* 3: 2oo3 median, 2: 1oo2 average, 1: 1oo1, 0: Fault *)
    rSuction_VotedRaw                           : REAL := 45.0;
    rSuction_VotedFiltered                      : REAL := 45.0;
    rSuction_DiscLimit_bar                      : REAL := 3.5;
    rSuction_DiscTripDelay_s                    : REAL := 0.250;

    (* Discharge Pressure TMR Engine *)
    rDischarge_ChA_Val                          : REAL := 115.0;
    rDischarge_ChB_Val                          : REAL := 115.0;
    rDischarge_ChC_Val                          : REAL := 115.0;
    bDischarge_ChA_Healthy                      : BOOL := TRUE;
    bDischarge_ChB_Healthy                      : BOOL := TRUE;
    bDischarge_ChC_Healthy                      : BOOL := TRUE;
    bDischarge_ChA_Degraded                     : BOOL := FALSE;
    bDischarge_ChB_Degraded                     : BOOL := FALSE;
    bDischarge_ChC_Degraded                     : BOOL := FALSE;
    rDischarge_Diff_AB                          : REAL := 0.0;
    rDischarge_Diff_BC                          : REAL := 0.0;
    rDischarge_Diff_CA                          : REAL := 0.0;
    tDischarge_DiscTimer_AB_s                   : REAL := 0.0;
    tDischarge_DiscTimer_BC_s                   : REAL := 0.0;
    tDischarge_DiscTimer_CA_s                   : REAL := 0.0;
    nDischarge_VotingMode                       : INT := 3;
    rDischarge_VotedRaw                         : REAL := 115.0;
    rDischarge_VotedFiltered                    : REAL := 115.0;
    rDischarge_DiscLimit_bar                    : REAL := 5.0;
    rDischarge_DiscTripDelay_s                  : REAL := 0.250;

    (* GVF Fraction Meter TMR Engine *)
    rGVF_ChA_Val                                : REAL := 65.0;
    rGVF_ChB_Val                                : REAL := 65.0;
    rGVF_ChC_Val                                : REAL := 65.0;
    bGVF_ChA_Healthy                            : BOOL := TRUE;
    bGVF_ChB_Healthy                            : BOOL := TRUE;
    bGVF_ChC_Healthy                            : BOOL := TRUE;
    bGVF_ChA_Degraded                           : BOOL := FALSE;
    bGVF_ChB_Degraded                           : BOOL := FALSE;
    bGVF_ChC_Degraded                           : BOOL := FALSE;
    rGVF_Diff_AB                                : REAL := 0.0;
    rGVF_Diff_BC                                : REAL := 0.0;
    rGVF_Diff_CA                                : REAL := 0.0;
    tGVF_DiscTimer_AB_s                         : REAL := 0.0;
    tGVF_DiscTimer_BC_s                         : REAL := 0.0;
    tGVF_DiscTimer_CA_s                         : REAL := 0.0;
    nGVF_VotingMode                             : INT := 3;
    rGVF_VotedRaw                               : REAL := 65.0;
    rGVF_VotedFiltered                          : REAL := 65.0;
    rGVF_DiscLimit_pct                          : REAL := 8.0;
    rGVF_DiscTripDelay_s                        : REAL := 0.350;

    (* Barrier Fluid Seal Differential Pressure TMR Engine *)
    rSealDP_ChA_Val                             : REAL := 42.0;
    rSealDP_ChB_Val                             : REAL := 42.0;
    rSealDP_ChC_Val                             : REAL := 42.0;
    bSealDP_ChA_Healthy                         : BOOL := TRUE;
    bSealDP_ChB_Healthy                         : BOOL := TRUE;
    bSealDP_ChC_Healthy                         : BOOL := TRUE;
    bSealDP_ChA_Degraded                        : BOOL := FALSE;
    bSealDP_ChB_Degraded                        : BOOL := FALSE;
    bSealDP_ChC_Degraded                        : BOOL := FALSE;
    rSealDP_Diff_AB                             : REAL := 0.0;
    rSealDP_Diff_BC                             : REAL := 0.0;
    rSealDP_Diff_CA                             : REAL := 0.0;
    tSealDP_DiscTimer_AB_s                      : REAL := 0.0;
    tSealDP_DiscTimer_BC_s                      : REAL := 0.0;
    tSealDP_DiscTimer_CA_s                      : REAL := 0.0;
    nSealDP_VotingMode                          : INT := 3;
    rSealDP_VotedRaw                            : REAL := 42.0;
    rSealDP_VotedFiltered                       : REAL := 42.0;
    rSealDP_DiscLimit_bar                       : REAL := 3.0;
    rSealDP_DiscTripDelay_s                     : REAL := 0.200;

    (* Common Bumpless Slew Rate Limiter Variables *)
    rBumplessSlewLimit_bar_s                    : REAL := 25.0;
    rBumplessSlewLimit_pct_s                    : REAL := 40.0;

    (* ==================================================================================================== *)
    (* 3. CYBER-PHYSICAL FLUID MECHANICS, ACOUSTICS & THERMODYNAMICS                                        *)
    (* ==================================================================================================== *)
    (* Multiphase Fluid Properties *)
    rGasDensityStandard_kgm3                    : REAL := 1.25;     (* Standard gas reference density [kg/m3] *)
    rLiquidDensity_kgm3                         : REAL := 845.0;    (* Produced crude liquid density [kg/m3] *)
    rWaterCut_pct                               : REAL := 32.0;     (* Produced water cut fraction [%] *)
    rGasSpecificGravity                         : REAL := 0.68;     (* Hydrocarbon gas specific gravity relative to air *)
    rGasCompressibilityZ                        : REAL := 0.88;     (* Real gas deviation factor Z *)
    rOperatingGasDensity_kgm3                   : REAL := 38.5;     (* In-situ dynamic gas density [kg/m3] *)
    rMixtureGasMassFraction                     : REAL := 0.085;    (* Quality / gas mass fraction *)
    rMixtureAcousticSonicSpeed_mps              : REAL := 185.0;    (* Wood's formula multiphase acoustic velocity [m/s] *)
    rMixtureBulkModulus_bar                     : REAL := 480.0;    (* Multiphase effective compressibility modulus [bar] *)

    (* Slug Detection & Dynamic Gas Surge Tracking *)
    rGVF_RateOfChange_pct_s                     : REAL := 0.0;      (* Filtered time derivative d(GVF)/dt [%/s] *)
    rGVF_Previous_pct                           : REAL := 65.0;     (* Previous scan cycle GVF [%] *)
    bGasSlugDetected                            : BOOL := FALSE;    (* High-acceleration gas slug arrival alarm flag *)
    bLiquidSlugDetected                         : BOOL := FALSE;    (* Dense liquid slug arrival alarm flag *)
    tGasSlugPersistTimer_s                      : REAL := 0.0;      (* Gas slug duration counter [s] *)
    rDynamicPressureRatio                       : REAL := 2.55;     (* Pressure ratio Pi = P_dis / P_suc *)
    rSurgeLimitLine_Ratio                       : REAL := 3.65;     (* Theoretical twin-screw surge limit line *)
    rSurgeControlLine_Ratio                     : REAL := 3.10;     (* Active anti-surge control setpoint line *)
    rSurgeDistance_Margin                       : REAL := 0.55;     (* Instantaneous operating distance to surge *)

    (* Mono-Ethylene Glycol (MEG) Hydrate Thermodynamic Inhibition *)
    rHydrateEquilibriumTemp_degC                : REAL := 19.8;     (* Hammerschmidt hydrate dissociation temperature [deg C] *)
    rHydrateSubcoolingTemp_degC                 : REAL := 18.5;     (* Safety subcooling temperature margin T_fluid - T_hyd [deg C] *)
    rRequiredMEG_WeightFraction_pct             : REAL := 32.5;     (* Minimum required aqueous phase MEG concentration [wt%] *)
    rCurrentMEG_DosingRate_kg_h                 : REAL := 245.0;    (* Commanded subsea MEG mass injection rate [kg/h] *)
    rMEG_InjectionSupplyDP_bar                  : REAL := 265.0;    (* Differential pressure across MEG injection nozzle [bar] *)
    bHydrateRiskWarning                         : BOOL := FALSE;    (* Hydrate subcooling margin low advisory warning *)
    bHydrateCriticalInterlock                   : BOOL := FALSE;    (* Hydrate imminent nucleation critical alarm *)

    (* Twin-Screw Thermal Growth & Dynamic Radial Running Clearances *)
    rRotorTemperature_degC                      : REAL := 88.5;     (* Observer estimated twin-screw rotor core temperature [deg C] *)
    rCasingTemperature_degC                     : REAL := 72.0;     (* Observer estimated pump stator casing temperature [deg C] *)
    rThermalExpansionCoeff_Rotor_perC           : REAL := 1.25E-5;  (* High-alloy martensitic stainless rotor alpha [1/deg C] *)
    rThermalExpansionCoeff_Casing_perC          : REAL := 1.10E-5;  (* Duplex stainless casing alpha [1/deg C] *)
    rRotorLength_mm                             : REAL := 1250.0;   (* Effective active screw intermeshing length [mm] *)
    rRotorNominalClearanceCold_um               : REAL := 120.0;    (* Cold static factory radial running clearance [um] *)
    rRotorThermalExpansion_um                   : REAL := 0.0;      (* Dynamic rotor radial thermal expansion [um] *)
    rCasingThermalExpansion_um                  : REAL := 0.0;      (* Dynamic casing bore thermal expansion [um] *)
    rDifferentialGrowth_um                      : REAL := 0.0;      (* Net differential clearance loss delta_L [um] *)
    rActiveRadialClearance_um                   : REAL := 110.0;    (* Real-time remaining radial running clearance [um] *)
    bClearanceWarning                           : BOOL := FALSE;    (* Radial clearance approaching minimum safe limit *)
    bClearanceCriticalTrip                      : BOOL := FALSE;    (* Radial clearance exhausted mechanical contact trip *)
    rMistCoolingPID_Integral                    : REAL := 0.0;      (* Thermal cooling mist injection controller integrator *)

    (* Subsea Pressurized Barrier Fluid Closed-Loop (Plan 53B/C) Diagnostics *)
    rBarrierFluidInternalPress_bar              : REAL := 157.0;    (* Sealed barrier loop internal absolute pressure [bar] *)
    rBarrierFluidOverpressure_bar               : REAL := 42.0;     (* Barrier overpressure over highest pump chamber [bar] *)
    rBarrierFluidAccumulatorVolume_L            : REAL := 38.5;     (* Subsea piston accumulator remaining nitrogen volume [L] *)
    bBarrierAccumulatorLowVolume                : BOOL := FALSE;    (* Accumulator pre-charge depletion advisory flag *)
    tBarrierLeakIntegrator_s                    : REAL := 0.0;      (* Accumulator volume leak rate tracking timer [s] *)
    rBarrierLeakAccumulated_mL                  : REAL := 0.0;      (* Cumulative barrier seal consumption [mL] *)

    (* ==================================================================================================== *)
    (* 4. 14-STAGE DETERMINISTIC PRODUCTION FINITE STATE MACHINE (FSM)                                      *)
    (* ==================================================================================================== *)
    nFSM_CurrentState                           : INT := 0;         (* Active FSM state enum index (0..13) *)
    nFSM_PreviousState                          : INT := 0;         (* Previous cycle FSM state index *)
    bFSM_StateFirstScan                         : BOOL := TRUE;     (* One-shot transition pulse for state entry *)
    tFSM_StateTimer_s                           : REAL := 0.0;      (* Continuous elapsed time in current active state [s] *)
    tFSM_StepTimer_s                            : REAL := 0.0;      (* Sub-sequence transition timer [s] *)
    nFSM_SubStep                                : INT := 0;         (* Internal phase sequencing step index *)

    (* FSM Sequence Timers, Permissives & Ramp Generators *)
    rVFD_RampTarget_RPM                         : REAL := 0.0;      (* Internal trajectory target speed for VFD ramps [RPM] *)
    rKickback_RampTarget_pct                    : REAL := 100.0;    (* Internal trajectory target for kickback valve [%] *)
    rChoke_RampTarget_pct                       : REAL := 0.0;      (* Internal trajectory target for choke valve [%] *)
    tStartupDelayTimer_s                        : REAL := 0.0;      (* Pre-lubrication and spin-up soak timer [s] *)
    tTurndownFlushTimer_s                       : REAL := 0.0;      (* MEG shutdown preservation flush timer [s] *)
    bThermalEquilibriumAchieved                 : BOOL := FALSE;    (* Casing and rotor temperature stabilization flag *)
    bAntiSurgeValveStroked                      : BOOL := FALSE;    (* High-speed recycle valve stroke verification flag *)

    (* ==================================================================================================== *)
    (* 5. ISA-18.2 MULTI-TIERED ALARM ENGINE & BIT-PACKED STATUS WORDS                                      *)
    (* ==================================================================================================== *)
    (* Trip Point Thresholds & Deadbands *)
    rSuctionPress_LL_Trip_bar                   : REAL := 18.0;     (* Suction Low-Low trip threshold [bar] *)
    rSuctionPress_L_Warn_bar                    : REAL := 28.0;     (* Suction Low warning threshold [bar] *)
    rSuctionPress_H_Warn_bar                    : REAL := 72.0;     (* Suction High warning threshold [bar] *)
    rSuctionPress_HH_Trip_bar                   : REAL := 85.0;     (* Suction High-High trip threshold [bar] *)
    rSuctionPress_Hysteresis_bar                : REAL := 1.5;      (* Deadband hysteresis [bar] *)

    rDischargePress_LL_Trip_bar                 : REAL := 65.0;     (* Discharge Low-Low trip threshold [bar] *)
    rDischargePress_L_Warn_bar                  : REAL := 85.0;     (* Discharge Low warning threshold [bar] *)
    rDischargePress_H_Warn_bar                  : REAL := 145.0;    (* Discharge High warning threshold [bar] *)
    rDischargePress_HH_Trip_bar                 : REAL := 160.0;    (* Discharge High-High trip threshold [bar] *)
    rDischargePress_Hysteresis_bar              : REAL := 2.0;      (* Deadband hysteresis [bar] *)

    rDiffPress_H_Warn_bar                       : REAL := 85.0;     (* Differential pressure High warning [bar] *)
    rDiffPress_HH_Trip_bar                      : REAL := 95.0;     (* Differential pressure High-High trip [bar] *)

    rGVF_H_Warn_pct                             : REAL := 90.0;     (* Gas Volume Fraction High warning [%] *)
    rGVF_HH_Trip_pct                            : REAL := 98.0;     (* Gas Volume Fraction High-High trip [%] *)

    rSealDP_LL_Trip_bar                         : REAL := 25.0;     (* Barrier Seal DP Low-Low trip threshold [bar] *)
    rSealDP_L_Warn_bar                          : REAL := 32.0;     (* Barrier Seal DP Low warning threshold [bar] *)
    rSealDP_H_Warn_bar                          : REAL := 65.0;     (* Barrier Seal DP High warning threshold [bar] *)
    rSealDP_HH_Trip_bar                         : REAL := 78.0;     (* Barrier Seal DP High-High trip threshold [bar] *)

    rBarrierLeak_H_Warn_mLmin                   : REAL := 5.0;      (* Barrier fluid leak rate High warning [mL/min] *)
    rBarrierLeak_HH_Trip_mLmin                  : REAL := 12.0;     (* Barrier fluid leak rate High-High trip [mL/min] *)

    rThermalGrowth_H_Warn_um                    : REAL := 70.0;     (* Differential thermal growth High warning [um] *)
    rThermalGrowth_HH_Trip_um                   : REAL := 95.0;     (* Differential thermal growth High-High trip [um] *)

    rVibration_H_Warn_mps2                      : REAL := 4.5;      (* Radial vibration RMS High warning [m/s2] *)
    rVibration_HH_Trip_mps2                     : REAL := 8.5;      (* Radial vibration RMS High-High trip [m/s2] *)

    rMotorStatorTemp_H_Warn_degC                : REAL := 115.0;    (* Motor stator winding High warning [deg C] *)
    rMotorStatorTemp_HH_Trip_degC               : REAL := 135.0;    (* Motor stator winding High-High trip [deg C] *)

    rHydrateMargin_L_Warn_degC                  : REAL := 5.0;      (* Hydrate subcooling margin Low warning [deg C] *)
    rHydrateMargin_LL_Trip_degC                 : REAL := 2.0;      (* Hydrate subcooling margin Low-Low trip [deg C] *)

    (* Alarm Debounce On-Delay Timers [s] *)
    tTimer_SuctionPress_LL_s                    : REAL := 0.0;
    tTimer_SuctionPress_L_s                     : REAL := 0.0;
    tTimer_SuctionPress_H_s                     : REAL := 0.0;
    tTimer_SuctionPress_HH_s                    : REAL := 0.0;
    tTimer_DischargePress_LL_s                  : REAL := 0.0;
    tTimer_DischargePress_L_s                   : REAL := 0.0;
    tTimer_DischargePress_H_s                   : REAL := 0.0;
    tTimer_DischargePress_HH_s                  : REAL := 0.0;
    tTimer_DiffPress_H_s                        : REAL := 0.0;
    tTimer_DiffPress_HH_s                       : REAL := 0.0;
    tTimer_GVF_H_s                              : REAL := 0.0;
    tTimer_GVF_HH_s                             : REAL := 0.0;
    tTimer_SealDP_LL_s                          : REAL := 0.0;
    tTimer_SealDP_L_s                           : REAL := 0.0;
    tTimer_SealDP_H_s                           : REAL := 0.0;
    tTimer_SealDP_HH_s                          : REAL := 0.0;
    tTimer_BarrierLeak_H_s                      : REAL := 0.0;
    tTimer_BarrierLeak_HH_s                     : REAL := 0.0;
    tTimer_ThermalGrowth_H_s                    : REAL := 0.0;
    tTimer_ThermalGrowth_HH_s                   : REAL := 0.0;
    tTimer_Vibration_H_s                        : REAL := 0.0;
    tTimer_Vibration_HH_s                       : REAL := 0.0;
    tTimer_MotorStatorTemp_H_s                  : REAL := 0.0;
    tTimer_MotorStatorTemp_HH_s                 : REAL := 0.0;
    tTimer_HydrateMargin_L_s                    : REAL := 0.0;
    tTimer_HydrateMargin_LL_s                   : REAL := 0.0;

    (* Active Alarm Condition Latches *)
    bAlarm_SuctionPress_LL                      : BOOL := FALSE;
    bAlarm_SuctionPress_L                       : BOOL := FALSE;
    bAlarm_SuctionPress_H                       : BOOL := FALSE;
    bAlarm_SuctionPress_HH                      : BOOL := FALSE;
    bAlarm_DischargePress_LL                    : BOOL := FALSE;
    bAlarm_DischargePress_L                     : BOOL := FALSE;
    bAlarm_DischargePress_H                     : BOOL := FALSE;
    bAlarm_DischargePress_HH                    : BOOL := FALSE;
    bAlarm_DiffPress_H                          : BOOL := FALSE;
    bAlarm_DiffPress_HH                         : BOOL := FALSE;
    bAlarm_GVF_H                                : BOOL := FALSE;
    bAlarm_GVF_HH                               : BOOL := FALSE;
    bAlarm_SealDP_LL                            : BOOL := FALSE;
    bAlarm_SealDP_L                             : BOOL := FALSE;
    bAlarm_SealDP_H                             : BOOL := FALSE;
    bAlarm_SealDP_HH                            : BOOL := FALSE;
    bAlarm_BarrierLeak_H                        : BOOL := FALSE;
    bAlarm_BarrierLeak_HH                       : BOOL := FALSE;
    bAlarm_ThermalGrowth_H                      : BOOL := FALSE;
    bAlarm_ThermalGrowth_HH                     : BOOL := FALSE;
    bAlarm_Vibration_H                          : BOOL := FALSE;
    bAlarm_Vibration_HH                         : BOOL := FALSE;
    bAlarm_MotorStatorTemp_H                    : BOOL := FALSE;
    bAlarm_MotorStatorTemp_HH                   : BOOL := FALSE;
    bAlarm_HydrateMargin_L                      : BOOL := FALSE;
    bAlarm_HydrateMargin_LL                     : BOOL := FALSE;

    (* Master First-Out Incident Latch *)
    nFirstOutAlarmIndex                         : INT := 0;
    bFirstOutLatched                            : BOOL := FALSE;
END_VAR
"""
