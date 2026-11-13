# cz_silicon_builder/mod_var_decl.py
# -*- coding: utf-8 -*-

def generate_var_decl():
    return """VAR
    (* ======================================================================================
       INTERNAL REAL-TIME SYSTEM ENGINE VARIABLES & TIMING CONTROL
       ====================================================================================== *)
    bFirstScan : BOOL := TRUE; (* Flag asserted exclusively on cold restart PLC cycle *)
    rCycleTimeSec : REAL := 0.1; (* Deterministic scan interval [s] derived from tCycleTime *)
    rTotalProcessElapsedTime : REAL := 0.0; (* Monotonically increasing campaign run timer [s] *)
    rCurrentStateDwellTime : REAL := 0.0; (* Current state elapsed duration timer [s] *)
    iLastStateIndex : INT := 0; (* Historical FSM state for edge transition detection *)
    iLoopIndex : INT := 0; (* Generic scratch index for deterministic unrolled math loops *)
    jLoopIndex : INT := 0; (* Secondary scratch iteration index *)
    kLoopIndex : INT := 0; (* Tertiary scratch iteration index *)

    (* ======================================================================================
       CYBER-PHYSICAL THERMODYNAMIC, STEFAN BOUNDARY & MATERIAL CONSTANTS
       ====================================================================================== *)
    k_s_solid : REAL := 22.0; (* [W/(m*K)] Solid silicon thermal conductivity at 1,414 deg C *)
    k_l_liquid : REAL := 64.0; (* [W/(m*K)] Liquid molten silicon thermal conductivity *)
    rho_s_solid : REAL := 2330.0; (* [kg/m3] Solid crystalline silicon density at melting point *)
    rho_l_liquid : REAL := 2570.0; (* [kg/m3] Liquid molten silicon density at 1,414 deg C *)
    L_f_latent : REAL := 1800000.0; (* [J/kg] Latent heat of crystallization fusion *)
    T_melt_point : REAL := 1414.0; (* [deg C] Equilibrium solid-liquid melting temperature *)
    gamma_m_tension : REAL := 0.720; (* [N/m] Liquid silicon surface tension at 1,414 deg C *)
    g_gravity : REAL := 9.80665; (* [m/s2] Standard gravitational acceleration *)
    theta_c_steady_deg : REAL := 11.0; (* [deg] Equilibrium dynamic meniscus growth contact angle *)
    PI_VAL : REAL := 3.14159265358979; (* Mathematical constant Pi *)
    rCrucibleRadius_mm : REAL := 406.4; (* [mm] Inner radius of 32-inch quartz crucible (812.8 mm OD / 2) *)
    rCrucibleCrossArea_mm2 : REAL := 518884.0; (* [mm2] Inner cross-sectional area of quartz crucible *)

    (* VORONKOV DEFECT MANAGEMENT CRITERION PARAMETERS (v / G_0) *)
    xi_crit_threshold : REAL := 0.220; (* [mm2/(min*K)] Critical vacancy-interstitial crossover ratio *)
    xi_window_min : REAL := 0.200; (* [mm2/(min*K)] Low threshold for defect-free crystal window *)
    xi_window_max : REAL := 0.240; (* [mm2/(min*K)] High threshold for defect-free crystal window *)
    rInterfaceAxialGradient_G0 : REAL := 3.45; (* [K/mm] Axial temperature gradient at interface dT/dz *)
    rLiquidThermalGradient_Gl : REAL := 1.85; (* [K/mm] Thermal gradient in liquid melt near tri-junction *)

    (* ======================================================================================
       2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSING SUITE & DISCREPANCY TIMERS
       ====================================================================================== *)
    (* 1. Triplicated Meniscus Optical Pyrometers [deg C] *)
    rPyro_DiffAB : REAL := 0.0; (* Absolute difference between Channel A and B *)
    rPyro_DiffBC : REAL := 0.0; (* Absolute difference between Channel B and C *)
    rPyro_DiffCA : REAL := 0.0; (* Absolute difference between Channel C and A *)
    rPyro_DevLimit_degC : REAL := 12.0; (* Max allowable inter-channel divergence limit [deg C] *)
    bPyro_FltA : BOOL := FALSE; (* Pyrometer Channel A out-of-tolerance discrepancy flag *)
    bPyro_FltB : BOOL := FALSE; (* Pyrometer Channel B out-of-tolerance discrepancy flag *)
    bPyro_FltC : BOOL := FALSE; (* Pyrometer Channel C out-of-tolerance discrepancy flag *)
    ton_PyroA_Discrep : TON; (* Channel A discrepancy persistence timer (200 ms) *)
    ton_PyroB_Discrep : TON; (* Channel B discrepancy persistence timer (200 ms) *)
    ton_PyroC_Discrep : TON; (* Channel C discrepancy persistence timer (200 ms) *)
    bPyro_DegradedMode : BOOL := FALSE; (* Voted operating in 2-channel degraded average mode *)
    bPyro_CriticalFailSafe : BOOL := FALSE; (* All 3 channels failed; bumpless latch to safe hold *)

    (* 2. Triplicated High-Speed CCD Camera Diameter Channels [mm] *)
    rCCD_DiffAB : REAL := 0.0;
    rCCD_DiffBC : REAL := 0.0;
    rCCD_DiffCA : REAL := 0.0;
    rCCD_DevLimit_mm : REAL := 2.50; (* Max allowable diameter divergence limit [mm] *)
    bCCD_FltA : BOOL := FALSE;
    bCCD_FltB : BOOL := FALSE;
    bCCD_FltC : BOOL := FALSE;
    ton_CCDA_Discrep : TON;
    ton_CCDB_Discrep : TON;
    ton_CCDC_Discrep : TON;
    bCCD_DegradedMode : BOOL := FALSE;
    bCCD_CriticalFailSafe : BOOL := FALSE;

    (* 3. Triplicated Seed Suspension Load Cell Channels [kg] *)
    rLoadCell_DiffAB : REAL := 0.0;
    rLoadCell_DiffBC : REAL := 0.0;
    rLoadCell_DiffCA : REAL := 0.0;
    rLoadCell_DevLimit_kg : REAL := 3.50; (* Max allowable crystal weight divergence limit [kg] *)
    bLoadCell_FltA : BOOL := FALSE;
    bLoadCell_FltB : BOOL := FALSE;
    bLoadCell_FltC : BOOL := FALSE;
    ton_LoadCellA_Discrep : TON;
    ton_LoadCellB_Discrep : TON;
    ton_LoadCellC_Discrep : TON;
    bLoadCell_DegradedMode : BOOL := FALSE;
    bLoadCell_CriticalFailSafe : BOOL := FALSE;

    (* 4. Triplicated Main Graphite Heater Thermocouple Arrays [deg C] *)
    rHeater_DiffAB : REAL := 0.0;
    rHeater_DiffBC : REAL := 0.0;
    rHeater_DiffCA : REAL := 0.0;
    rHeater_DevLimit_degC : REAL := 28.0; (* Max allowable heater thermocouple divergence [deg C] *)
    bHeater_FltA : BOOL := FALSE;
    bHeater_FltB : BOOL := FALSE;
    bHeater_FltC : BOOL := FALSE;
    ton_HeaterA_Discrep : TON;
    ton_HeaterB_Discrep : TON;
    ton_HeaterC_Discrep : TON;
    bHeater_DegradedMode : BOOL := FALSE;
    bHeater_CriticalFailSafe : BOOL := FALSE;

    tDiscrepancyPersistence : TIME := T#200MS; (* Standardized persistence duration for sensor trip *)

    (* Historical Latched Voted Values for Bumpless Degradation *)
    rLastValidVotedMeniscusTemp : REAL := 1414.0;
    rLastValidVotedIngotDiameter : REAL := 300.0;
    rLastValidVotedCrystalWeight : REAL := 0.0;
    rLastValidVotedHeaterTemp : REAL := 1520.0;

    (* ======================================================================================
       6x6 DISCRETE STATE-SPACE OBSERVER & SYSTEM MATRICES (A, B, C, D, L)
       ======================================================================================
       States:
         x1: Ingot diameter at solidification front [mm]
         x2: Meniscus melt temperature at tri-junction [deg C]
         x3: Solid silicon crystal temperature gradient [K/mm]
         x4: Bulk crucible melt average temperature [deg C]
         x5: Melt convection velocity fluctuation intensity [mm/s]
         x6: Ingot pull speed deviation from nominal [mm/min]
       Actuators:
         u1: Crystal pull motor servo speed [mm/min]
         u2: Main graphite resistance heater thyristor power [kW]
         u3: Bottom crucible lift motor servo speed [mm/min]
         u4: Top/bottom cusp magnetic field coil current [A]
         u5: Crystal seed shaft rotation speed [RPM]
       Measurements:
         y1: Voted Meniscus Pyrometer Temperature [deg C]
         y2: Voted CCD Optical Diameter [mm]
         y3: Ingot Load Cell Weight Rate Equivalent Diameter [mm]
         y4: Voted Main Graphite Heater Temperature [deg C]
         y5: Melt surface convection turbulence intensity estimate [mm/s]
         y6: Crystal pull servo encoder actual speed [mm/min]
       ====================================================================================== *)
    A_mat : ARRAY[1..6, 1..6] OF REAL; (* Discrete state transition matrix (6x6) *)
    B_mat : ARRAY[1..6, 1..5] OF REAL; (* Discrete input gain matrix (6x5) *)
    C_mat : ARRAY[1..6, 1..6] OF REAL; (* Discrete measurement observation matrix (6x6) *)
    D_mat : ARRAY[1..6, 1..5] OF REAL; (* Direct feedthrough matrix (6x5) *)
    L_mat : ARRAY[1..6, 1..6] OF REAL; (* Luenberger Kalman innovation observer gain matrix (6x6) *)

    (* State Vectors *)
    x_state : ARRAY[1..6] OF REAL; (* Plant physical internal state vector *)
    x_hat : ARRAY[1..6] OF REAL; (* Full-order observer estimated state vector *)
    x_hat_next : ARRAY[1..6] OF REAL; (* Propagated next-scan observer state *)
    x_ref : ARRAY[1..6] OF REAL; (* Target reference setpoint state vector *)
    x_err : ARRAY[1..6] OF REAL; (* Tracking error vector (x_hat - x_ref) *)

    (* Measurement and Innovation Vectors *)
    y_meas : ARRAY[1..6] OF REAL; (* Sensor voted measurement vector *)
    y_est : ARRAY[1..6] OF REAL; (* Predicted measurement vector (C * x_hat + D * u) *)
    y_innov : ARRAY[1..6] OF REAL; (* Measurement innovation residual (y_meas - y_est) *)

    (* Control Actuator Vectors *)
    u_cmd : ARRAY[1..5] OF REAL; (* Commanded actuator outputs *)
    u_prev : ARRAY[1..5] OF REAL; (* Actuator outputs from previous execution scan *)
    u_rate : ARRAY[1..5] OF REAL; (* Rate of change of control inputs (slew rate) *)
    u_min : ARRAY[1..5] OF REAL; (* Physical lower saturation limits *)
    u_max : ARRAY[1..5] OF REAL; (* Physical upper saturation limits *)
    du_max : ARRAY[1..5] OF REAL; (* Maximum permissible slew delta per cycle *)

    (* ======================================================================================
       RECEDING-HORIZON MPC WITH 10 UNROLLED PROJECTED GRADIENT DESCENT (PGD) ITERATIONS
       ====================================================================================== *)
    Q_mat : ARRAY[1..6, 1..6] OF REAL; (* State deviation penalty quadratic matrix *)
    R_mat : ARRAY[1..5, 1..5] OF REAL; (* Actuator energy penalty quadratic matrix *)
    S_mat : ARRAY[1..5, 1..5] OF REAL; (* Actuator slew rate penalty quadratic matrix *)
    P_mat : ARRAY[1..6, 1..6] OF REAL; (* Terminal state cost quadratic matrix *)

    (* MPC Prediction Horizon Trajectories (Horizon Steps N = 5) *)
    x_pred : ARRAY[0..5, 1..6] OF REAL; (* Predicted state trajectory across horizon *)
    u_plan : ARRAY[0..4, 1..5] OF REAL; (* Optimized actuator command sequence *)
    lambda_costate : ARRAY[0..5, 1..6] OF REAL; (* Adjoint backward costate trajectory *)
    grad_cost : ARRAY[0..4, 1..5] OF REAL; (* Gradient of quadratic objective wrt control inputs *)

    alpha_pgd_step : REAL := 0.0035; (* Gradient descent learning rate parameter *)
    rTotalMPCCost : REAL := 0.0; (* Accumulated quadratic cost value *)
    iPGDIteration : INT := 0; (* Iteration index for 10 unrolled PGD passes *)

    (* ======================================================================================
       ADDITIONAL THERMAL, MENISCUS, AND MAGNETIC FLUID VARIABLES
       ====================================================================================== *)
    rStefanPullRate_calc : REAL := 0.0; (* [mm/min] Crystal growth rate calculated via Stefan condition *)
    rMeniscusHeight_calc : REAL := 0.0; (* [mm] Meniscus height calculated via Laplace-Young *)
    rCalculatedContactAngle : REAL := 11.0; (* [deg] Dynamic meniscus contact wetting angle *)
    rCapillaryConstant_mm : REAL := 7.56; (* [mm] Capillary constant for molten silicon *)
    rLorentzDampingFactor : REAL := 1.0; (* Dimensionless convection damping efficiency (0.05 to 1.0) *)
    rBulkConvectionVelocity_RMS : REAL := 4.2; (* [mm/s] RMS turbulence velocity in molten bath *)
    rCrucibleLiftKinematicSpeed : REAL := 0.0; (* [mm/min] Theoretical crucible lift for mass balance *)
    rMeltLevelDroopError_mm : REAL := 0.0; (* [mm] Deviation of melt surface from heat shield datum *)
    rCrucibleLevelTrimGain : REAL := 0.15; (* Proportional correction gain for crucible lift *)
    rCrystalWeightRate_kg_hr : REAL := 0.0; (* [kg/h] Differential crystal weight accumulation rate *)
    rLastCrystalWeightSample : REAL := 0.0; (* [kg] Filtered weight sample from previous time step *)

    (* Length and Weight Trackers *)
    rIngotDashNeckLength_mm : REAL := 0.0; (* [mm] Length of thin Dash neck section *)
    rIngotCrownLength_mm : REAL := 0.0; (* [mm] Length of conical crown expansion section *)
    rIngotBodyLength_mm : REAL := 0.0; (* [mm] Length of nominal 300 mm cylindrical body section *)
    rIngotTailLength_mm : REAL := 0.0; (* [mm] Length of end-cone tailout section *)
    rTotalIngotLength_mm : REAL := 0.0; (* [mm] Overall accumulated single-crystal length *)
    rSiliconMeltMassRemaining_kg : REAL := 350.0; (* [kg] Mass of liquid silicon remaining in crucible *)

    (* ======================================================================================
       14-STAGE DETERMINISTIC PRODUCTION FINITE STATE MACHINE (FSM) ENUMERATION & TIMERS
       ====================================================================================== *)
    STATE_IDLE : INT := 0;
    STATE_CHAMBER_VACUUM_EVACUATION_AND_LEAK_CHECK : INT := 1;
    STATE_ARGON_MELT_PURGE_AND_PRESSURE_STABILIZE : INT := 2;
    STATE_POLYSILICON_CHARGE_MELTDOWN_FULL_POWER : INT := 3;
    STATE_MELT_EQUILIBRIUM_AND_CUSP_MAGNETIC_LOCK : INT := 4;
    STATE_SEED_CRYSTAL_DIP_AND_MELT_WETTING : INT := 5;
    STATE_DASH_NECKING_DISLOCATION_ELIMINATION : INT := 6;
    STATE_CROWN_EXPANSION_CONE_ANGLE_RAMP : INT := 7;
    STATE_SHOULDER_RADIUS_ROLLOVER_TRANSITION : INT := 8;
    STATE_BODY_EQUAL_DIAMETER_GROWTH_MPC_ACTIVE : INT := 9;
    STATE_TAILOUT_END_CONE_THERMAL_SHOCK_TAPERING : INT := 10;
    STATE_CRYSTAL_SEPARATION_AND_LIFT_TO_COOL_CHAMBER : INT := 11;
    STATE_RESIDUAL_MELT_COOLDOWN_AND_CRUCIBLE_PURGE : INT := 12;
    STATE_EMERGENCY_MELT_LEAK_OR_VACUUM_COLLAPSE_TRIP : INT := 13;

    (* FSM Sequence Dwell Timers *)
    ton_StateTimer : TON;
    ton_VacuumEvacTimer : TON;
    ton_LeakRateCheckTimer : TON;
    ton_ArgonBackfillTimer : TON;
    ton_MeltdownSoakTimer : TON;
    ton_CuspMagneticSoakTimer : TON;
    ton_SeedThermalSoakTimer : TON;
    ton_DashHabitLineTimer : TON;
    ton_ShoulderRadiusRolloverTimer : TON;
    ton_SeparationThermalShockTimer : TON;
    ton_ChamberCoolingPurgeTimer : TON;

    (* Dislocation & Habit Lines Optical Metrology Verification *)
    bHabitLinesDetected : BOOL := FALSE; (* 4 sharp crystallographic ridges detected on neck *)
    bSeedMeltPinched : BOOL := FALSE; (* Premature seed melt-off failure flag *)
    bDislocationDislodged : BOOL := FALSE; (* Slip dislocation propagated into crystal body *)

    (* ======================================================================================
       ISA-18.2 MULTI-TIER ALARM LIMITS, DEADBANDS & TRIP FLAGS
       ====================================================================================== *)
    (* Meniscus Temperature Limits [deg C] *)
    rMeniscusTemp_HH_Limit : REAL := 1435.0;
    rMeniscusTemp_H_Limit  : REAL := 1425.0;
    rMeniscusTemp_L_Limit  : REAL := 1411.0;
    rMeniscusTemp_LL_Limit : REAL := 1406.0;
    rMeniscusTemp_Deadband : REAL := 1.50;

    (* Ingot Diameter Deviation Limits [mm] *)
    rDiameter_HH_Limit : REAL := 304.0;
    rDiameter_H_Limit  : REAL := 301.2;
    rDiameter_L_Limit  : REAL := 298.8;
    rDiameter_LL_Limit : REAL := 296.0;
    rDiameter_Deadband : REAL := 0.25;

    (* Chamber Vacuum Pressure Limits [mbar] *)
    rVacuum_HH_Limit : REAL := 45.0;
    rVacuum_H_Limit  : REAL := 32.0;
    rVacuum_L_Limit  : REAL := 12.0;
    rVacuum_LL_Limit : REAL := 4.0;
    rVacuum_Deadband : REAL := 1.0;

    (* Main Graphite Heater Temperature Limits [deg C] *)
    rHeater_HH_Limit : REAL := 1720.0;
    rHeater_H_Limit  : REAL := 1680.0;
    rHeater_L_Limit  : REAL := 1200.0;
    rHeater_LL_Limit : REAL := 950.0;
    rHeater_Deadband : REAL := 8.0;

    (* Chamber Cooling Water Flow [L/min] and Temperature [deg C] *)
    rCoolingFlow_L_Limit  : REAL := 42.0;
    rCoolingFlow_LL_Limit : REAL := 32.0;
    rCoolingFlow_Deadband : REAL := 2.0;
    rCoolingTemp_H_Limit  : REAL := 30.0;
    rCoolingTemp_HH_Limit : REAL := 36.0;
    rCoolingTemp_Deadband : REAL := 1.0;

    (* ISA-18.2 Alarm Flags *)
    bAlm_Meniscus_HH : BOOL := FALSE;
    bAlm_Meniscus_H  : BOOL := FALSE;
    bAlm_Meniscus_L  : BOOL := FALSE;
    bAlm_Meniscus_LL : BOOL := FALSE;

    bAlm_Diameter_HH : BOOL := FALSE;
    bAlm_Diameter_H  : BOOL := FALSE;
    bAlm_Diameter_L  : BOOL := FALSE;
    bAlm_Diameter_LL : BOOL := FALSE;

    bAlm_Vacuum_HH : BOOL := FALSE;
    bAlm_Vacuum_H  : BOOL := FALSE;
    bAlm_Vacuum_L  : BOOL := FALSE;
    bAlm_Vacuum_LL : BOOL := FALSE;

    bAlm_Heater_HH : BOOL := FALSE;
    bAlm_Heater_H  : BOOL := FALSE;
    bAlm_Heater_L  : BOOL := FALSE;
    bAlm_Heater_LL : BOOL := FALSE;

    bAlm_CoolingWater_FlowLow : BOOL := FALSE;
    bAlm_CoolingWater_FlowTrip : BOOL := FALSE;
    bAlm_CoolingWater_TempHigh : BOOL := FALSE;
    bAlm_CoolingWater_TempTrip : BOOL := FALSE;

    bAlm_VoronkovRatioTrip : BOOL := FALSE;
    bAlm_CuspCoilTrip : BOOL := FALSE;
    bAlm_CrucibleMeltLeakDetected : BOOL := FALSE;
    bAlm_QuartzCrucibleRupture : BOOL := FALSE;
    bAlm_LossOfStructureDislocation : BOOL := FALSE;
    bAlm_EStopActive : BOOL := FALSE;

    (* First-Out Latching Identification Register *)
    iFirstOutCode : INT := 0;
END_VAR"""
