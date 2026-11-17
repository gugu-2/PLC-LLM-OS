# test_var_block.py
# Tests the VAR declaration block generation

def get_var_block():
    return """VAR
    (* ===================================================================================== *)
    (* 1.0 DISCRETE STATE-SPACE MATRICES & KALMAN/LUENBERGER OBSERVER STRUCTURES             *)
    (* ===================================================================================== *)
    (* Continuous state-space linearized around nominal high-pressure injection trajectory:  *)
    (*   x[k+1] = A * x[k] + B * u[k]                                                        *)
    (*   y[k]   = C * x[k] + D * u[k]                                                        *)
    (* Observer Innovation:                                                                  *)
    (*   x_hat[k+1] = A * x_hat[k] + B * u[k] + L * (y[k] - C * x_hat[k])                     *)
    A_mat                          : ARRAY[1..6, 1..6] OF REAL; (* Discrete state transition matrix (6x6) *)
    B_mat                          : ARRAY[1..6, 1..5] OF REAL; (* Input control coupling matrix (6x5) *)
    C_mat                          : ARRAY[1..6, 1..6] OF REAL; (* Measurement observation matrix (6x6) *)
    D_mat                          : ARRAY[1..6, 1..5] OF REAL; (* Direct feedthrough matrix (6x5) *)
    L_obs                          : ARRAY[1..6, 1..6] OF REAL; (* Observer Kalman innovation gain matrix (6x6) *)

    x_state                        : ARRAY[1..6] OF REAL; (* True state measurement/reconstruction vector *)
    x_hat                          : ARRAY[1..6] OF REAL; (* Current observer estimated state vector *)
    x_hat_next                     : ARRAY[1..6] OF REAL; (* One-step-ahead predicted state vector *)
    y_meas                         : ARRAY[1..6] OF REAL; (* Filtered process measurement vector *)
    y_est                          : ARRAY[1..6] OF REAL; (* Observer estimated output vector *)
    innov                          : ARRAY[1..6] OF REAL; (* Measurement innovation error vector (y - C*x_hat) *)
    bMatricesInitialized           : BOOL := FALSE;       (* One-shot startup initialization latch flag *)

    (* ===================================================================================== *)
    (* 2.0 RECEDING-HORIZON MPC OPTIMIZER STRUCTURES (10 UNROLLED PGD ITERATIONS)            *)
    (* ===================================================================================== *)
    Q_diag                         : ARRAY[1..6] OF REAL; (* State error quadratic penalty weights *)
    R_diag                         : ARRAY[1..5] OF REAL; (* Control effort rate penalty weights *)
    S_diag                         : ARRAY[1..5] OF REAL; (* Actuator slew rate damping weights *)
    P_diag                         : ARRAY[1..6] OF REAL; (* Terminal state penalty weights *)
    x_ref                          : ARRAY[1..6] OF REAL; (* Dynamic state reference trajectory setpoints *)
    x_err                          : ARRAY[1..6] OF REAL; (* Instantaneous state tracking error vector *)
    u_mpc                          : ARRAY[1..5] OF REAL; (* Active MPC control command vector *)
    u_prev                         : ARRAY[1..5] OF REAL; (* Previous cycle actuator command vector *)
    u_target                       : ARRAY[1..5] OF REAL; (* Feedforward baseline actuator commands *)
    u_delta                        : ARRAY[1..5] OF REAL; (* Commanded actuator change rate per millisecond *)
    u_traj                         : ARRAY[1..10, 1..5] OF REAL; (* Receding horizon predicted input trajectory *)
    x_traj                         : ARRAY[1..10, 1..6] OF REAL; (* Receding horizon predicted state trajectory *)
    lambda_traj                    : ARRAY[1..10, 1..6] OF REAL; (* Adjoint costate vector back-propagation *)
    grad_traj                      : ARRAY[1..10, 1..5] OF REAL; (* Cost function gradient trajectory w.r.t input *)
    H_diag                         : ARRAY[1..5] OF REAL; (* Approximate diagonal Hessian curvature elements *)
    rStepSize                      : REAL := 0.032;       (* Projected gradient descent step size factor *)
    rMpcCost                       : REAL;                (* Total evaluated quadratic objective cost *)

    (* Actuator Slew Rate and Hard Bounds *)
    rMaxPilotSlew_pct_ms           : REAL := 25.0;  (* Max allowable servo pilot rate of change [%/ms] *)
    rMaxPoppetSlew_pct_ms          : REAL := 50.0;  (* Max allowable accumulator poppet rate [%/ms] *)
    rMaxIntensifierSlew_pct_ms     : REAL := 30.0;  (* Max allowable booster multiplier rate [%/ms] *)
    rMaxVacuumSlew_pct_ms          : REAL := 15.0;  (* Max allowable vacuum valve rate [%/ms] *)
    rMaxTemperingSlew_pct_ms       : REAL := 5.0;   (* Max allowable tempering pump slew rate [%/ms] *)

    (* ===================================================================================== *)
    (* 3.0 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) VOTING & DEGRADATION TIMERS                  *)
    (* ===================================================================================== *)
    (* Velocity 2oo3 Bank (rPlungerVel_A, B, C) *)
    rDev_Vel_AB                    : REAL;     (* [m/s] Cross-channel deviation between Transducers A & B *)
    rDev_Vel_BC                    : REAL;     (* [m/s] Cross-channel deviation between Transducers B & C *)
    rDev_Vel_CA                    : REAL;     (* [m/s] Cross-channel deviation between Transducers C & A *)
    bVel_A_Healthy                 : BOOL;     (* [bool] Transducer A signal integrity health flag *)
    bVel_B_Healthy                 : BOOL;     (* [bool] Transducer B signal integrity health flag *)
    bVel_C_Healthy                 : BOOL;     (* [bool] Transducer C signal integrity health flag *)
    rTon_Vel_Discrep_s             : REAL;     (* [s] Persistent cross-channel discrepancy duration *)
    bVel_Degraded_1oo2             : BOOL;     (* [bool] Velocity bank operating in degraded 1oo2 mode *)
    bVel_Failed_Trip               : BOOL;     (* [bool] Velocity bank complete instrument loss trip *)

    (* Hydraulic Shot Pressure 2oo3 Bank (rShotPress_A, B, C) *)
    rDev_Press_AB                  : REAL;     (* [bar] Cross-channel deviation between Sensors A & B *)
    rDev_Press_BC                  : REAL;     (* [bar] Cross-channel deviation between Sensors B & C *)
    rDev_Press_CA                  : REAL;     (* [bar] Cross-channel deviation between Sensors C & A *)
    bPress_A_Healthy               : BOOL;     (* [bool] Shot pressure sensor A integrity health flag *)
    bPress_B_Healthy               : BOOL;     (* [bool] Shot pressure sensor B integrity health flag *)
    bPress_C_Healthy               : BOOL;     (* [bool] Shot pressure sensor C integrity health flag *)
    rTon_Press_Discrep_s           : REAL;     (* [s] Persistent cross-channel discrepancy duration *)
    bPress_Degraded_1oo2           : BOOL;     (* [bool] Pressure bank operating in degraded 1oo2 mode *)
    bPress_Failed_Trip             : BOOL;     (* [bool] Pressure bank complete instrument loss trip *)

    (* Mold Cavity Vacuum 2oo3 Bank (rCavityVac_A, B, C) *)
    rDev_Vac_AB                    : REAL;     (* [mbar] Cross-channel deviation between Vacuum Transmitters A & B *)
    rDev_Vac_BC                    : REAL;     (* [mbar] Cross-channel deviation between Vacuum Transmitters B & C *)
    rDev_Vac_CA                    : REAL;     (* [mbar] Cross-channel deviation between Vacuum Transmitters C & A *)
    bVac_A_Healthy                 : BOOL;     (* [bool] Vacuum transmitter A integrity health flag *)
    bVac_B_Healthy                 : BOOL;     (* [bool] Vacuum transmitter B integrity health flag *)
    bVac_C_Healthy                 : BOOL;     (* [bool] Vacuum transmitter C integrity health flag *)
    rTon_Vac_Discrep_s             : REAL;     (* [s] Persistent cross-channel discrepancy duration *)
    bVac_Degraded_1oo2             : BOOL;     (* [bool] Vacuum bank operating in degraded 1oo2 mode *)
    bVac_Failed_Trip               : BOOL;     (* [bool] Vacuum bank complete instrument loss trip *)

    (* Total Clamping Force 2oo3 Bank (rClampForce_A, B, C) *)
    rDev_Clamp_AB                  : REAL;     (* [kN] Cross-channel deviation between Load Rings A & B *)
    rDev_Clamp_BC                  : REAL;     (* [kN] Cross-channel deviation between Load Rings B & C *)
    rDev_Clamp_CA                  : REAL;     (* [kN] Cross-channel deviation between Load Rings C & A *)
    bClamp_A_Healthy               : BOOL;     (* [bool] Clamp force load ring A integrity health flag *)
    bClamp_B_Healthy               : BOOL;     (* [bool] Clamp force load ring B integrity health flag *)
    bClamp_C_Healthy               : BOOL;     (* [bool] Clamp force load ring C integrity health flag *)
    rTon_Clamp_Discrep_s           : REAL;     (* [s] Persistent cross-channel discrepancy duration *)
    bClamp_Degraded_1oo2           : BOOL;     (* [bool] Clamp bank operating in degraded 1oo2 mode *)
    bClamp_Failed_Trip             : BOOL;     (* [bool] Clamp bank complete instrument loss trip *)

    (* ===================================================================================== *)
    (* 4.0 4-TIE-BAR ECCENTRICITY, LOAD BALANCING & BENDING MOMENTS                          *)
    (* ===================================================================================== *)
    c_TieBar_NominalForce_kN       : REAL := 22500.0; (* [kN] Nominal static pre-stress per tie-bar (90,000 / 4) *)
    c_TieBar_Diameter_mm           : REAL := 750.0;   (* [mm] Massive 4340 alloy steel tie-bar outer diameter *)
    c_TieBar_ElasticModulus_GPa    : REAL := 210.0;   (* [GPa] Young's modulus of tie-bar material *)
    c_TieBar_Length_mm             : REAL := 12500.0; (* [mm] Effective stressed tie-bar stretch length *)
    rTieBar_Mean_kN                : REAL;            (* [kN] Instantaneous average tie-bar tension force *)
    rTieBar_Dev_TB1                : REAL;            (* [kN] Deviation of Tie-Bar 1 from mean *)
    rTieBar_Dev_TB2                : REAL;            (* [kN] Deviation of Tie-Bar 2 from mean *)
    rTieBar_Dev_TB3                : REAL;            (* [kN] Deviation of Tie-Bar 3 from mean *)
    rTieBar_Dev_TB4                : REAL;            (* [kN] Deviation of Tie-Bar 4 from mean *)
    rEccentricity_Horiz_kN         : REAL;            (* [kN] Horizontal platen tilting force delta (TB1+TB3 - TB2+TB4) *)
    rEccentricity_Vert_kN          : REAL;            (* [kN] Vertical platen tilting force delta (TB1+TB2 - TB3+TB4) *)
    rEccentricity_Diag_kN          : REAL;            (* [kN] Diagonal warping torsional force delta (TB1+TB4 - TB2+TB3) *)
    rTieBar_Integral_TB1           : REAL;            (* Hydraulic nut trimming integrator accumulator TB1 *)
    rTieBar_Integral_TB2           : REAL;            (* Hydraulic nut trimming integrator accumulator TB2 *)
    rTieBar_Integral_TB3           : REAL;            (* Hydraulic nut trimming integrator accumulator TB3 *)
    rTieBar_Integral_TB4           : REAL;            (* Hydraulic nut trimming integrator accumulator TB4 *)

    (* ===================================================================================== *)
    (* 5.0 FIRST-PRINCIPLES CYBER-PHYSICAL SHOT HYDRODYNAMICS & SOLIDIFICATION               *)
    (* ===================================================================================== *)
    (* Shot Sleeve Physical Constants *)
    c_SleeveDiameter_m             : REAL := 0.180;     (* [m] Internal diameter of H13 nitrided shot sleeve *)
    c_SleeveArea_m2                : REAL := 0.025447;  (* [m^2] Cross-sectional area of injection shot sleeve *)
    c_SleeveLength_m               : REAL := 1.400;     (* [m] Total usable stroke of shot sleeve *)
    c_CavityVolume_m3              : REAL := 0.0385;    (* [m^3] Rear underbody casting net cavity volume *)
    c_TotalShotDoseVolume_m3       : REAL := 0.0415;    (* [m^3] Total liquid aluminum volume (110.0 kg / 2650 kg/m^3) *)
    c_AlloyLiquidDensity_kg_m3     : REAL := 2650.0;    (* [kg/m^3] Liquid AlSi10MnMg alloy density at 685 deg C *)
    c_AlloySolidDensity_kg_m3      : REAL := 2700.0;    (* [kg/m^3] Solid AlSi10MnMg alloy density at 250 deg C *)
    c_AlloyLatentHeatFusion_J_kg   : REAL := 389000.0;  (* [J/kg] Latent heat of fusion Al-Si eutectic *)
    c_AlloyThermalConduct_W_mK     : REAL := 145.0;     (* [W/m*K] Thermal conductivity of casting alloy *)
    c_DieSteelThermalConduct_W_mK  : REAL := 28.5;      (* [W/m*K] Thermal conductivity of H13 tool steel *)
    c_LiquidusTemp_degC            : REAL := 595.0;     (* [deg C] Liquidus onset temperature *)
    c_SolidusTemp_degC             : REAL := 550.0;     (* [deg C] Coherent dendrite solidus freeze temperature *)
    c_PartMeanThickness_mm         : REAL := 2.50;      (* [mm] Nominal thin-walled structural cast section *)

    (* Kinematic Stroke Transition Boundaries *)
    c_Pos_PourHoleCovered_mm       : REAL := 380.0;     (* [mm] Plunger covers pour inlet slot *)
    c_Pos_WaveDampingStart_mm      : REAL := 450.0;     (* [mm] Onset of continuous anti-slosh acceleration *)
    c_Pos_SleeveCompaction_mm      : REAL := 720.0;     (* [mm] Liquid aluminum gathers fully without void *)
    c_Pos_FastShotTransition_mm    : REAL := 1020.0;    (* [mm] High-acceleration transition into fast shot Phase 2 *)
    c_Pos_CavityFillImpact_mm      : REAL := 1285.0;    (* [mm] Liquid metal impacts cavity walls, Phase 3 onset *)
    c_Pos_MechanicalBumper_mm      : REAL := 1340.0;    (* [mm] Absolute safety stroke end hard stop *)

    (* Wave Kinematics & Free Surface Dynamics *)
    rFillFractionInSleeve          : REAL;     (* Fractional volume filling of shot sleeve (0.0 to 1.0) *)
    rLiquidMetalHeight_m           : REAL;     (* [m] Effective static liquid aluminum height in horizontal sleeve *)
    rCriticalWaveVelocity_ms       : REAL;     (* [m/s] Gravity wave celerity c = sqrt(g * h_eff) *)
    rFroudeNumber                  : REAL;     (* Dimensionless Froude ratio Fr = v_plunger / c_wave *)
    rWaveProfileDampingGain        : REAL;     (* Adaptive wave surge suppression damping factor *)

    (* Vacuum Evacuation & Acoustic Chill-Block Dynamics *)
    c_VacuumRootsSpeed_m3_s        : REAL := 0.850;     (* [m^3/s] Effective Roots pumping extraction speed (3060 m^3/h) *)
    c_TotalVacuumVolume_m3         : REAL := 0.165;     (* [m^3] Cavity + runner + vacuum header total volume *)
    rDynamicVacuumEvacRate_mb_s    : REAL;              (* [mbar/s] Dynamic cavity decompression rate dp/dt *)
    rChillBlockTimer_ms            : REAL;              (* [ms] Acoustic chill-block valve closure response timer *)
    bChillBlockTimerActive         : BOOL;              (* [bool] Fast timer tracking acoustic valve seat travel *)

    (* Solidification Stefan-Chvorinov Kinetics *)
    rSolidificationRate_mm_s       : REAL;     (* [mm/s] Dynamic freezing velocity of shell boundary layer *)
    rHeatFluxToDie_W_m2            : REAL;     (* [W/m^2] Transient interface heat flux into die steel *)

    (* Molten Metal Flash Blowout & Die Separation Force Protection *)
    c_PartingProjectedArea_m2      : REAL := 1.850;     (* [m^2] Total projected frontal area of rear underbody casting *)
    rCavityDynamicPressure_bar     : REAL;              (* [bar] Effective projected hydrostatic cavity metal pressure *)
    rDieSeparationForce_kN         : REAL;              (* [kN] Total hydraulic opening force attempting to gap platens *)
    rFlashBlowoutSafetyMargin_kN   : REAL;              (* [kN] Net clamping safety reserve: F_clamp - F_sep *)

    (* ===================================================================================== *)
    (* 6.0 14-STAGE DETERMINISTIC PRODUCTION FINITE STATE MACHINE (FSM)                      *)
    (* ===================================================================================== *)
    c_STATE_IDLE                                               : INT := 0;
    c_STATE_DIE_SAFETY_DOOR_LOCK_AND_PARTING_AGENT_SPRAY       : INT := 1;
    c_STATE_4_TIE_BAR_HYDRAULIC_CLAMP_TO_90000KN               : INT := 2;
    c_STATE_LADLE_ROBOT_MOLTEN_ALUMINUM_POUR_INTO_SLEEVE       : INT := 3;
    c_STATE_MOLD_CAVITY_HIGH_VACUUM_EVACUATION_BELOW_25MBAR    : INT := 4;
    c_STATE_PHASE1_SLOW_SHOT_WAVE_SURGE_SUPPRESSION            : INT := 5;
    c_STATE_PHASE2_FAST_SHOT_HIGH_ACCELERATION_CAVITY_FILL     : INT := 6;
    c_STATE_VACUUM_CHILL_BLOCK_VALVE_FAST_SHUTOFF              : INT := 7;
    c_STATE_PHASE3_INTENSIFICATION_PRESSURE_SQUEEZE_1400BAR    : INT := 8;
    c_STATE_IN_DIE_SOLIDIFICATION_COOLING_HOLD                 : INT := 9;
    c_STATE_TIE_BAR_DECOMPRESSION_AND_DIE_OPEN_STROKE          : INT := 10;
    c_STATE_HYDRAULIC_EJECTOR_PINS_MULTI_POINT_PUSH            : INT := 11;
    c_STATE_EXTRACTOR_ROBOT_PART_GRIP_AND_LASER_METROLOGY      : INT := 12;
    c_STATE_EMERGENCY_FLASH_BLOWOUT_OR_TIE_BAR_OVERSTRAIN_TRIP : INT := 13;

    rStateTimer_sec                : REAL;     (* [s] Elapsed running time in current state *)
    rStateTimeout_sec              : REAL;     (* [s] Active state watchdog maximum allowable timeout *)
    rClampPressurizationTimer_s    : REAL;     (* [s] Clamping hydraulic ramp build-up timer *)
    rSolidificationTimer_s         : REAL;     (* [s] Part in-die cooling dwell timer *)
    rEjectorTravelTimer_s          : REAL;     (* [s] Hydraulic ejector plate advance timer *)
    rPlatenDecompressionTimer_s    : REAL;     (* [s] Controlled tie-bar pressure release timer *)

    (* ===================================================================================== *)
    (* 7.0 PRESSURIZED DIE THERMAL BALANCING PID CONTROLLERS                                 *)
    (* ===================================================================================== *)
    rCoverDie_Error_degC           : REAL;     (* [deg C] Fixed cover die temperature control error *)
    rCoverDie_Integral             : REAL;     (* Cover die PID integrator *)
    rCoverDie_Derivative           : REAL;     (* Cover die PID derivative *)
    rCoverDie_PrevTemp_degC        : REAL;     (* Cover die previous temperature for derivative *)

    rEjectorDie_Error_degC         : REAL;     (* [deg C] Moving ejector die temperature control error *)
    rEjectorDie_Integral           : REAL;     (* Ejector die PID integrator *)
    rEjectorDie_Derivative         : REAL;     (* Ejector die PID derivative *)
    rEjectorDie_PrevTemp_degC      : REAL;     (* Ejector die previous temperature for derivative *)

    rCoreInsert_Error_degC         : REAL;     (* [deg C] Thin-walled structural core temperature error *)
    rCoreInsert_Integral           : REAL;     (* Core insert PID integrator *)
    rCoreInsert_Derivative         : REAL;     (* Core insert PID derivative *)
    rCoreInsert_PrevTemp_degC      : REAL;     (* Core insert previous temperature for derivative *)

    (* ===================================================================================== *)
    (* 8.0 ISA-18.2 ALARM TRIP POINTS, DEAD-BANDS & PERSISTENCE TIMERS                       *)
    (* ===================================================================================== *)
    (* Process Alarm Threshold Constants *)
    c_ALM_Vel_HH_ms                : REAL := 9.80;    (* [m/s] High-High injection overspeed trip *)
    c_ALM_Vel_H_ms                 : REAL := 8.90;    (* [m/s] High injection velocity warning *)
    c_ALM_Vel_L_ms                 : REAL := 0.15;    (* [m/s] Low injection velocity warning during Phase 1 *)
    c_ALM_Vel_LL_ms                : REAL := 0.05;    (* [m/s] Low-Low plunger stall trip *)
    c_DB_Vel_ms                    : REAL := 0.04;    (* [m/s] Velocity alarm deadband hysteresis *)

    c_ALM_ShotPress_HH_bar         : REAL := 1480.0;  (* [bar] High-High intensifier overpressure trip *)
    c_ALM_ShotPress_H_bar          : REAL := 1350.0;  (* [bar] High intensifier pressure warning *)
    c_ALM_ShotPress_L_bar          : REAL := 180.0;   (* [bar] Low shot pressure warning during fast fill *)
    c_ALM_ShotPress_LL_bar         : REAL := 120.0;   (* [bar] Low-Low shot pressure stall trip *)
    c_DB_ShotPress_bar             : REAL := 12.0;    (* [bar] Shot pressure deadband hysteresis *)

    c_ALM_Vac_HH_mbar              : REAL := 65.0;    (* [mbar] High-High vacuum failure trip (porosity hazard) *)
    c_ALM_Vac_H_mbar               : REAL := 30.0;    (* [mbar] High vacuum level warning (sub-optimal) *)
    c_DB_Vac_mbar                  : REAL := 2.5;     (* [mbar] Vacuum deadband hysteresis *)

    c_ALM_Clamp_HH_kN              : REAL := 96500.0; (* [kN] High-High tie-bar structural yield overstrain trip *)
    c_ALM_Clamp_H_kN               : REAL := 92500.0; (* [kN] High clamp force advisory warning *)
    c_ALM_Clamp_L_kN               : REAL := 87500.0; (* [kN] Low clamp force warning (flash hazard) *)
    c_ALM_Clamp_LL_kN              : REAL := 84000.0; (* [kN] Low-Low clamp force flash blowout trip *)
    c_DB_Clamp_kN                  : REAL := 350.0;   (* [kN] Clamp force deadband hysteresis *)

    c_ALM_Eccentricity_HH_kN       : REAL := 3800.0;  (* [kN] High-High platen diagonal/bending overstrain trip *)
    c_ALM_Eccentricity_H_kN        : REAL := 2200.0;  (* [kN] High platen tilt warning *)
    c_DB_Eccentricity_kN           : REAL := 100.0;   (* [kN] Eccentricity deadband hysteresis *)

    c_ALM_DieTemp_HH_degC          : REAL := 315.0;   (* [deg C] High-High die thermal overheating trip *)
    c_ALM_DieTemp_H_degC           : REAL := 290.0;   (* [deg C] High die temperature warning *)
    c_ALM_DieTemp_L_degC           : REAL := 210.0;   (* [deg C] Low die temperature warning (cold shut risk) *)
    c_ALM_DieTemp_LL_degC          : REAL := 185.0;   (* [deg C] Low-Low die temperature interlock trip *)
    c_DB_DieTemp_degC              : REAL := 3.5;     (* [deg C] Temperature deadband hysteresis *)

    c_ALM_ChillClose_HH_ms         : REAL := 8.00;    (* [ms] High-High acoustic chill-block closure latency trip *)

    (* Alarm Status Flags *)
    bAlm_Vel_HH                    : BOOL;
    bAlm_Vel_H                     : BOOL;
    bAlm_Vel_L                     : BOOL;
    bAlm_Vel_LL                    : BOOL;
    bAlm_ShotPress_HH              : BOOL;
    bAlm_ShotPress_H               : BOOL;
    bAlm_ShotPress_L               : BOOL;
    bAlm_ShotPress_LL              : BOOL;
    bAlm_Vac_HH                    : BOOL;
    bAlm_Vac_H                     : BOOL;
    bAlm_Clamp_HH                  : BOOL;
    bAlm_Clamp_H                   : BOOL;
    bAlm_Clamp_L                   : BOOL;
    bAlm_Clamp_LL                  : BOOL;
    bAlm_Eccentricity_HH           : BOOL;
    bAlm_Eccentricity_H            : BOOL;
    bAlm_DieTemp_HH                : BOOL;
    bAlm_DieTemp_H                 : BOOL;
    bAlm_DieTemp_L                 : BOOL;
    bAlm_DieTemp_LL                : BOOL;
    bAlm_ChillClose_HH             : BOOL;
    bAlm_FlashBlowoutRisk_HH       : BOOL;

    (* ===================================================================================== *)
    (* 9.0 ITERATION COUNTERS, TEMPORARY VARIABLES & MATRIX INDICES                         *)
    (* ===================================================================================== *)
    iIdx1                          : INT;
    iIdx2                          : INT;
    iIdx3                          : INT;
    iIterPgd                       : INT;
    rTempSum                       : REAL;
    rTempDiff                      : REAL;
    rTempDot                       : REAL;
    rMinVal                        : REAL;
    rMaxVal                        : REAL;
    rMedianVal                     : REAL;
    rFlashCheckSeparation_kN       : REAL;
END_VAR
"""

if __name__ == "__main__":
    b = get_var_block()
    print("VAR block len:", len(b))
