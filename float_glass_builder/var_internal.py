# var_internal.py for FB_Glass_FloatLine_TinBath_AnnealingLehr_ThicknessCooling

def generate_var_internal():
    return """VAR
    (* =====================================================================================================
     * INTERNAL CYBER-PHYSICAL STATE-SPACE MATRICES & OBSERVER STRUCTURES (6x6 SYSTEM)
     * Discrete State Formulation: x[k+1] = A * x[k] + B * u[k] + L * (y[k] - C * x[k] - D * u[k])
     * States:
     *   x[1]: Dynamic glass ribbon center thickness deviation Delta_h [um]
     *   x[2]: Glass ribbon total width deviation Delta_W [mm]
     *   x[3]: Tin bath molten tin longitudinal temperature gradient Delta_T_bath [deg C]
     *   x[4]: Protective atmosphere reducing gas pressure Delta_P_bath [mbar]
     *   x[5]: Annealing Lehr zone residual thermal birefringence stress Delta_sigma [nm/cm]
     *   x[6]: Lehr main line conveyor draw speed deviation Delta_v_line [m/min]
     * Inputs:
     *   u[1]: Top-roller knurl aggregate draw velocity trim [RPM]
     *   u[2]: Top-roller knurl aggregate toe-in angle trim [deg]
     *   u[3]: Tin bath roof SiC electrical radiant heater bank power trim [%]
     *   u[4]: Protective atmosphere reducing gas N2/H2 supply valve trim [%]
     *   u[5]: Annealing Lehr transverse cooling damper air trim [%]
     *   u[6]: Lehr main line drive conveyor motor speed trim [m/min]
     * ===================================================================================================== *)
    matA : ARRAY[1..6, 1..6] OF REAL;  (* Continuous-to-discrete system state transition dynamics matrix A *)
    matB : ARRAY[1..6, 1..6] OF REAL;  (* Discrete input coupling control effectiveness matrix B *)
    matC : ARRAY[1..6, 1..6] OF REAL;  (* Discrete measurement observation state output matrix C *)
    matD : ARRAY[1..6, 1..6] OF REAL;  (* Discrete direct input-to-output feedforward matrix D *)
    matL : ARRAY[1..6, 1..6] OF REAL;  (* Stationary discrete Kalman / Luenberger observer innovation gain matrix L *)

    (* State and Observation Vectors *)
    arrStateX_Hat           : ARRAY[1..6] OF REAL; (* Estimated state vector x_hat[k] at current scan cycle *)
    arrStateX_Next          : ARRAY[1..6] OF REAL; (* Predicted state vector x_hat[k+1] for next scan cycle *)
    arrInputU               : ARRAY[1..6] OF REAL; (* Synthesized control effort vector u[k] *)
    arrInputU_Prev          : ARRAY[1..6] OF REAL; (* Previous scan cycle control effort vector u[k-1] for slew limits *)
    arrOutputY_Meas         : ARRAY[1..6] OF REAL; (* Observed sensor output measurement vector y[k] *)
    arrOutputY_Est          : ARRAY[1..6] OF REAL; (* Model estimated observation vector y_hat[k] *)
    arrInnovationError      : ARRAY[1..6] OF REAL; (* Innovation residual vector e[k] = y[k] - y_hat[k] *)
    arrStateX_Ref           : ARRAY[1..6] OF REAL; (* Optimal target state trajectory reference vector x_ref *)
    arrInputU_Ref           : ARRAY[1..6] OF REAL; (* Steady-state feedforward nominal control bias vector u_ref *)

    (* Intermediate Matrix Multiplication Accumulators *)
    rAx_Sum                 : REAL;
    rBu_Sum                 : REAL;
    rCx_Sum                 : REAL;
    rDu_Sum                 : REAL;
    rLe_Sum                 : REAL;

    (* =====================================================================================================
     * RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) & UNROLLED PGD OPTIMIZATION (10 ITERATIONS)
     * Cost: J = sum (x - x_ref)^T * Q * (x - x_ref) + sum (u - u_ref)^T * R * (u - u_ref) + du^T * S * du + x_T^T * P * x_T
     * ===================================================================================================== *)
    matQ : ARRAY[1..6, 1..6] OF REAL;  (* Positive semi-definite state tracking error penalty weight matrix Q *)
    matR : ARRAY[1..6, 1..6] OF REAL;  (* Positive definite actuator control effort penalty weight matrix R *)
    matP : ARRAY[1..6, 1..6] OF REAL;  (* Terminal state stability algebraic Riccati cost-to-go penalty matrix P *)

    (* Actuator Hard Saturation Box Bounds & Dynamic Slew Rate Limits *)
    arrU_Min                : ARRAY[1..6] OF REAL; (* Lower physical box constraint limits on control vector u *)
    arrU_Max                : ARRAY[1..6] OF REAL; (* Upper physical box constraint limits on control vector u *)
    arrDeltaU_Max           : ARRAY[1..6] OF REAL; (* Maximum allowable rate-of-change slew limit per scan cycle *)

    (* PGD Unrolled Optimization Trajectory Variables *)
    rMpcStepSizeAlpha       : REAL := 0.0125;      (* Projected Gradient Descent descent step size scaling factor *)
    arrU_PGD_Iter           : ARRAY[0..10, 1..6] OF REAL; (* Unrolled control iteration steps [iteration 0..10, dim 1..6] *)
    arrGradJ_Iter           : ARRAY[1..6] OF REAL; (* Quadratic cost gradient vector nabla_J(u) *)
    rMpcCurrentCost         : REAL;                (* Total accumulated quadratic objective performance index J *)
    rMpcPriorCost           : REAL;                (* Objective function value in preceding scan *)
    bMpcConverged           : BOOL;                (* PGD gradient norm convergence flag (< epsilon) *)

    (* =====================================================================================================
     * 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSING STRUCTURES & DISCREPANCY TIMERS
     * Sensors Monitored:
     *   1. Non-contact Laser Optical Thickness Gauges (Thick1, Thick2, Thick3) [mm]
     *   2. Tin Bath Multi-Wavelength Optical Infrared Pyrometers (Pyro1, Pyro2, Pyro3) [deg C]
     *   3. Tin Bath Hermetic Protective Atmosphere Pressure Transmitters (Press1, Press2, Press3) [mbar]
     *   4. Lehr Cold-End Polarimetric Optical Stress Birefringence Transducers (Stress1, Stress2, Stress3) [nm/cm]
     * ===================================================================================================== *)
    (* Thickness 2oo3 Structure *)
    rThick_DiscrepancyLimit_mm  : REAL := 0.080;   (* Discrepancy tolerance threshold between channels [mm] *)
    rThick_TimerLimit_sec       : REAL := 2.50;    (* Discrepancy trip timeout before channel isolation [s] *)
    rDiff_Thick_12              : REAL;            (* Absolute discrepancy between channel 1 and 2 [mm] *)
    rDiff_Thick_23              : REAL;            (* Absolute discrepancy between channel 2 and 3 [mm] *)
    rDiff_Thick_13              : REAL;            (* Absolute discrepancy between channel 1 and 3 [mm] *)
    rTimer_Thick_12             : REAL := 0.0;     (* Accumulated elapsed discrepancy timer for pair 1-2 [s] *)
    rTimer_Thick_23             : REAL := 0.0;     (* Accumulated elapsed discrepancy timer for pair 2-3 [s] *)
    rTimer_Thick_13             : REAL := 0.0;     (* Accumulated elapsed discrepancy timer for pair 1-3 [s] *)
    bThick_Ch1_Valid            : BOOL := TRUE;    (* Thickness channel 1 operational health status *)
    bThick_Ch2_Valid            : BOOL := TRUE;    (* Thickness channel 2 operational health status *)
    bThick_Ch3_Valid            : BOOL := TRUE;    (* Thickness channel 3 operational health status *)
    nThick_HealthyChannels      : INT := 3;        (* Count of currently validated healthy thickness channels *)
    nThick_VotingMode           : INT := 3;        (* 3=2oo3 TMR, 2=1oo2 Degraded, 1=1oo1 Single, 0=Failover Trip *)

    (* Pyrometer 2oo3 Structure *)
    rPyro_DiscrepancyLimit_degC : REAL := 12.0;    (* Discrepancy tolerance threshold between pyrometers [deg C] *)
    rPyro_TimerLimit_sec        : REAL := 3.00;    (* Discrepancy trip timeout before pyrometer isolation [s] *)
    rDiff_Pyro_12               : REAL;            (* Absolute discrepancy between pyrometer 1 and 2 [deg C] *)
    rDiff_Pyro_23               : REAL;            (* Absolute discrepancy between pyrometer 2 and 3 [deg C] *)
    rDiff_Pyro_13               : REAL;            (* Absolute discrepancy between pyrometer 1 and 3 [deg C] *)
    rTimer_Pyro_12              : REAL := 0.0;     (* Discrepancy timer pair 1-2 [s] *)
    rTimer_Pyro_23              : REAL := 0.0;     (* Discrepancy timer pair 2-3 [s] *)
    rTimer_Pyro_13              : REAL := 0.0;     (* Discrepancy timer pair 1-3 [s] *)
    bPyro_Ch1_Valid             : BOOL := TRUE;    (* Pyrometer 1 health status *)
    bPyro_Ch2_Valid             : BOOL := TRUE;    (* Pyrometer 2 health status *)
    bPyro_Ch3_Valid             : BOOL := TRUE;    (* Pyrometer 3 health status *)
    nPyro_HealthyChannels       : INT := 3;        (* Count of healthy pyrometers *)
    nPyro_VotingMode            : INT := 3;        (* 3=2oo3, 2=1oo2, 1=1oo1, 0=Failover *)

    (* Atmosphere Pressure 2oo3 Structure *)
    rPress_DiscrepancyLimit_mbar: REAL := 0.12;    (* Discrepancy tolerance between pressure transmitters [mbar] *)
    rPress_TimerLimit_sec       : REAL := 1.50;    (* Discrepancy trip timeout for pressure channels [s] *)
    rDiff_Press_12              : REAL;            (* Discrepancy pair 1-2 [mbar] *)
    rDiff_Press_23              : REAL;            (* Discrepancy pair 2-3 [mbar] *)
    rDiff_Press_13              : REAL;            (* Discrepancy pair 1-3 [mbar] *)
    rTimer_Press_12             : REAL := 0.0;     (* Discrepancy timer pair 1-2 [s] *)
    rTimer_Press_23             : REAL := 0.0;     (* Discrepancy timer pair 2-3 [s] *)
    rTimer_Press_13             : REAL := 0.0;     (* Discrepancy timer pair 1-3 [s] *)
    bPress_Ch1_Valid            : BOOL := TRUE;    (* Pressure transmitter 1 health status *)
    bPress_Ch2_Valid            : BOOL := TRUE;    (* Pressure transmitter 2 health status *)
    bPress_Ch3_Valid            : BOOL := TRUE;    (* Pressure transmitter 3 health status *)
    nPress_HealthyChannels      : INT := 3;        (* Count of healthy pressure transmitters *)
    nPress_VotingMode           : INT := 3;        (* 3=2oo3, 2=1oo2, 1=1oo1, 0=Failover *)

    (* Lehr Residual Stress 2oo3 Structure *)
    rStress_DiscrepancyLimit_nm : REAL := 6.0;     (* Discrepancy tolerance between optical polarimeters [nm/cm] *)
    rStress_TimerLimit_sec      : REAL := 3.50;    (* Discrepancy trip timeout for stress sensors [s] *)
    rDiff_Stress_12             : REAL;            (* Discrepancy pair 1-2 [nm/cm] *)
    rDiff_Stress_23             : REAL;            (* Discrepancy pair 2-3 [nm/cm] *)
    rDiff_Stress_13             : REAL;            (* Discrepancy pair 1-3 [nm/cm] *)
    rTimer_Stress_12            : REAL := 0.0;     (* Discrepancy timer pair 1-2 [s] *)
    rTimer_Stress_23            : REAL := 0.0;     (* Discrepancy timer pair 2-3 [s] *)
    rTimer_Stress_13            : REAL := 0.0;     (* Discrepancy timer pair 1-3 [s] *)
    bStress_Ch1_Valid           : BOOL := TRUE;    (* Polarimeter 1 health status *)
    bStress_Ch2_Valid           : BOOL := TRUE;    (* Polarimeter 2 health status *)
    bStress_Ch3_Valid           : BOOL := TRUE;    (* Polarimeter 3 health status *)
    nStress_HealthyChannels     : INT := 3;        (* Count of healthy polarimeters *)
    nStress_VotingMode          : INT := 3;        (* 3=2oo3, 2=1oo2, 1=1oo1, 0=Failover *)

    (* =====================================================================================================
     * FIRST-PRINCIPLES CYBER-PHYSICAL MODELING & THERMO-FLUID DYNAMIC VARIABLES
     * ===================================================================================================== *)
    (* Equilibrium Spread Natural Thickness Computation (Langmuir-Three-Phase Wetting Formulation) *)
    rSurfaceTension_g_tin       : REAL := 0.380;   (* Interfacial surface tension molten soda-lime glass / tin [N/m] *)
    rSurfaceTension_g_atm       : REAL := 0.350;   (* Molten glass / reducing atmosphere surface tension [N/m] *)
    rSurfaceTension_tin_atm     : REAL := 0.540;   (* Molten tin / reducing atmosphere surface tension [N/m] *)
    rDensityLiquidTin           : REAL := 6500.0;  (* Mass density of liquid tin pool at 900 deg C [kg/m3] *)
    rDensityMoltenGlass         : REAL := 2500.0;  (* Mass density of molten soda-lime-silica glass [kg/m3] *)
    rGravitationalConst         : REAL := 9.80665; (* Standard gravitational acceleration constant [m/s2] *)
    rEquilibriumThickness_heq   : REAL;            (* Natural equilibrium glass sheet thickness h_eq [mm] *)

    (* Vogel-Fulcher-Tammann (VFT) Viscosity-Temperature Dynamics: log10(eta) = A_vft + B_vft / (T - T0_vft) *)
    rVFT_Param_A                : REAL := -2.585;  (* High-temperature asymptotic log-viscosity constant *)
    rVFT_Param_B                : REAL := 4215.0;  (* Activation energy thermal slope constant [deg C] *)
    rVFT_Param_T0               : REAL := 265.0;   (* Ideal glass transition singularity temperature T0 [deg C] *)
    rCalculatedLogViscosityCanal: REAL;            (* Computed canal glass viscosity log10(dPa.s) *)
    rCalculatedViscosityBathExit: REAL;            (* Computed bath exit glass viscosity [dPa.s] *)

    (* 16 Motorized Top-Roller Knurl Machines Operational States & Kinematics *)
    arrTopRollerActualSpeed     : ARRAY[1..16] OF REAL; (* Actual feedback rotational speed from encoder [RPM] *)
    arrTopRollerActualAngle     : ARRAY[1..16] OF REAL; (* Actual angular orientation toe angle vs ribbon axis [deg] *)
    arrTopRollerActualPen       : ARRAY[1..16] OF REAL; (* Actual vertical penetration into molten ribbon edge [mm] *)
    arrTopRollerMotorTorque     : ARRAY[1..16] OF REAL; (* Motor shaft electromechanical torque feedback [% rated] *)
    arrTopRollerMotorCurrent    : ARRAY[1..16] OF REAL; (* VFD motor drive phase current feedback [A] *)
    arrTopRollerShaftWaterFlow  : ARRAY[1..16] OF REAL; (* Internal hollow shaft cooling water flow rate [L/min] *)
    arrTopRollerShaftTemp       : ARRAY[1..16] OF REAL; (* Shaft internal thermocouple temperature [deg C] *)
    arrTopRollerTractiveForce_N : ARRAY[1..16] OF REAL; (* Computed lateral tractive tension force exerted on ribbon [N] *)
    arrTopRollerSlipRatio       : ARRAY[1..16] OF REAL; (* Knurl tooth-to-glass slip ratio: 1.0 - (v_ribbon / v_knurl) *)
    arrTopRollerSlipTrip        : ARRAY[1..16] OF BOOL; (* Knurl machine slip fault latch flag *)

    (* Thermal Management: Tin Bath Roof Heaters & Annealing Lehr Cooling Zones *)
    arrTinBathZoneTempActual    : ARRAY[1..8] OF REAL;  (* Roof thermocouple actual temperature feedback [deg C] *)
    arrTinBathZoneTempSP        : ARRAY[1..8] OF REAL;  (* Thermal zone setpoint profile along 65m bath [deg C] *)
    arrTinBathZonePowerkW       : ARRAY[1..8] OF REAL;  (* Silicon carbide electric heating element power [kW] *)
    arrLehrZoneTempActual       : ARRAY[1..12] OF REAL; (* Lehr zone centerline actual temperature [deg C] *)
    arrLehrZoneTempSP           : ARRAY[1..12] OF REAL; (* Lehr longitudinal cooling curve setpoints [deg C] *)
    arrLehrTransverseDeltaT     : ARRAY[1..12] OF REAL; (* Edge-to-center cross-belt transverse temperature differential [deg C] *)
    arrLehrCrossDamperActual    : ARRAY[1..12] OF REAL; (* Lehr cooling air damper actuator position feedback [%] *)

    (* Viscoelastic Thermal Stress Relaxation (Narayanaswamy / Tool-Narayanaswamy Formulation) *)
    rFictiveTemperatureTf       : REAL;            (* Structural relaxation fictive temperature [deg C] *)
    rNarayanaswamyTauZero       : REAL := 1.25;    (* Shear relaxation reference time constant [s] *)
    rCalculatedThermalStressMPa : REAL;            (* Transverse residual parabolic thermal stress [MPa] *)
    rPhotoelasticConstantC      : REAL := 2.65;    (* Brewsters photoelastic stress-optical coefficient [nm/(cm*MPa)] *)

    (* =====================================================================================================
     * 14-STAGE DETERMINISTIC PRODUCTION FINITE STATE MACHINE (FSM) VARIABLES
     * ===================================================================================================== *)
    nOperationalSubState        : INT := 0;        (* Minor phase sub-sequence step index [0..20] *)
    nPreviousState              : INT := 0;        (* Historical state from immediately preceding cycle *)
    rStateTimer_sec             : REAL := 0.0;     (* Continuous active state dwell duration timer [s] *)
    rSubStateTimer_sec          : REAL := 0.0;     (* Sub-state dwell duration timer [s] *)
    bStateFirstScan             : BOOL := TRUE;    (* One-shot initial execution pulse on entering state *)
    bStateTransitionPermitted   : BOOL := FALSE;   (* Transition interlock validation permissive flag *)
    nTargetStateRequest         : INT := 0;        (* Requested destination state for transition sequence *)

    (* State Machine Numerical Code Constants *)
    cSTATE_IDLE                                     : INT := 0;
    cSTATE_TIN_BATH_ELECTRICAL_ROOF_HEATER_WARMUP   : INT := 1;
    cSTATE_PROTECTIVE_ATMOSPHERE_N2_H2_PURGE_AND_SEAL: INT := 2;
    cSTATE_CANAL_TWEEL_LIFT_AND_MOLTEN_GLASS_FLOW   : INT := 3;
    cSTATE_TIN_BATH_MOLTEN_GLASS_POOL_SPREAD_EQUIL  : INT := 4;
    cSTATE_TOP_ROLLER_ENGAGE_AND_WIDTH_GRIP_ACQUISIT: INT := 5;
    cSTATE_RIBBON_ATTENUATION_AND_THICKNESS_CONVERGE: INT := 6;
    cSTATE_LIFT_OUT_ROLL_TRANSITION_INTO_LEHR       : INT := 7;
    cSTATE_LEHR_COOLING_GRADIENT_CLOSED_LOOP_STRESS : INT := 8;
    cSTATE_NOMINAL_CONTINUOUS_FLOAT_PRODUCTION_RUN  : INT := 9;
    cSTATE_DYNAMIC_PRODUCT_THICKNESS_RECIPE_CHANGE  : INT := 10;
    cSTATE_RIBBON_WAISTING_OR_NECK_IN_AUTO_CORRECT  : INT := 11;
    cSTATE_CONTROLLED_TWEEL_SHUT_AND_LEHR_CLEARING  : INT := 12;
    cSTATE_EMERGENCY_RIBBON_BREAK_CULLET_DUMP_TRIP  : INT := 13;

    (* Dynamic Recipe Transition Controller *)
    rRecipeTransitionProgressPct: REAL := 0.0;     (* Smooth ramp interpolation progress percentage [0..100%] *)
    rRecipeInitialThickness_mm  : REAL;            (* Base thickness prior to transition initiation [mm] *)
    rRecipeInitialWidth_mm      : REAL;            (* Base ribbon width prior to transition [mm] *)
    rRecipeInitialLineSpeed_mpm : REAL;            (* Base lehr line conveyor speed [m/min] *)
    rRecipeTransitionRampRate   : REAL := 0.050;   (* Maximum thickness change rate limit [mm/min] *)

    (* Ribbon Waisting / Neck-In Hydrodynamic Auto-Correction Loop *)
    rWaistingDefectThreshold_mm : REAL := 80.0;    (* Critical allowable edge waist neck-in contraction [mm] *)
    rMeasuredWaistContraction_mm: REAL;            (* Current calculated neck-in magnitude at zone 4-6 [mm] *)
    rTopRollerAngleBiasTrim_deg : REAL := 0.0;     (* Computed dynamic toe-in angular widening bias [deg] *)
    rTopRollerSpeedBiasTrim_RPM : REAL := 0.0;     (* Longitudinal speed deceleration compensation bias [RPM] *)

    (* =====================================================================================================
     * ISA-18.2 MULTI-TIERED ALARM ENGINE & BIT-PACKED STATUS ENCODING
     * Four Tiers: High-High (HH), High (H), Low (L), Low-Low (LL) with Clear Deadbands & Time Delays
     * ===================================================================================================== *)
    (* Laser Optical Thickness Alarms [deviation in mm relative to target] *)
    rThickAlarm_HH_Limit        : REAL := 0.250;   (* Thickness High-High Deviation Limit (+250 um) [mm] *)
    rThickAlarm_H_Limit         : REAL := 0.100;   (* Thickness High Deviation Limit (+100 um) [mm] *)
    rThickAlarm_L_Limit         : REAL := -0.100;  (* Thickness Low Deviation Limit (-100 um) [mm] *)
    rThickAlarm_LL_Limit        : REAL := -0.250;  (* Thickness Low-Low Deviation Limit (-250 um) [mm] *)
    rThickAlarm_Deadband        : REAL := 0.015;   (* Clearance hysteresis deadband (15 um) [mm] *)

    (* Tin Bath Roof Inlet Pyrometer Alarms [deg C] *)
    rPyroAlarm_HH_Limit         : REAL := 1110.0;  (* Tin Bath Inlet High-High Refractory Protection Limit [deg C] *)
    rPyroAlarm_H_Limit          : REAL := 1075.0;  (* Tin Bath Inlet High Warning Threshold [deg C] *)
    rPyroAlarm_L_Limit          : REAL := 1020.0;  (* Tin Bath Inlet Low Viscous Stagnation Warning [deg C] *)
    rPyroAlarm_LL_Limit         : REAL := 990.0;   (* Tin Bath Inlet Low-Low Molten Glass Freezing Trip [deg C] *)
    rPyroAlarm_Deadband         : REAL := 5.0;     (* Clearance deadband [deg C] *)

    (* Tin Bath Protective Atmosphere Pressure Alarms [mbar] *)
    rPressAlarm_HH_Limit        : REAL := 1.25;    (* High-High Pressure Casing Mechanical Strain Limit [mbar] *)
    rPressAlarm_H_Limit         : REAL := 0.90;    (* High Overpressure Venting Warning [mbar] *)
    rPressAlarm_L_Limit         : REAL := 0.20;    (* Low Atmosphere Ingress Warning [mbar] *)
    rPressAlarm_LL_Limit        : REAL := 0.06;    (* Low-Low Atmospheric Air Oxygen Contamination Trip [mbar] *)
    rPressAlarm_Deadband        : REAL := 0.03;    (* Clearance deadband [mbar] *)

    (* Lehr Residual Optical Stress Birefringence Alarms [nm/cm] *)
    rStressAlarm_HH_Limit       : REAL := 45.0;    (* High-High Thermal Stress Glass Spontaneous Fracture Limit [nm/cm] *)
    rStressAlarm_H_Limit        : REAL := 30.0;    (* High Annealing Retardation Out-of-Spec Warning [nm/cm] *)
    rStressAlarm_Deadband       : REAL := 2.5;     (* Clearance deadband [nm/cm] *)

    (* Gas Chemistry Alarms *)
    rH2_Alarm_LL_Limit          : REAL := 2.50;    (* Low-Low Hydrogen Scavenger Concentration Trip [% vol H2] *)
    rH2_Alarm_L_Limit           : REAL := 3.80;    (* Low Hydrogen Scavenger Warning [% vol H2] *)
    rH2_Alarm_HH_Limit          : REAL := 8.50;    (* High-High Hydrogen Flammability Safety Upper Limit [% vol H2] *)
    rO2_Alarm_HH_Limit          : REAL := 15.0;    (* High-High Oxygen Ingress Stannous Oxide Hazard [ppm O2] *)

    (* Individual Latched Alarm Flags *)
    bAlarm_Thick_HH             : BOOL := FALSE;
    bAlarm_Thick_H              : BOOL := FALSE;
    bAlarm_Thick_L              : BOOL := FALSE;
    bAlarm_Thick_LL             : BOOL := FALSE;
    bAlarm_Pyro_HH              : BOOL := FALSE;
    bAlarm_Pyro_H               : BOOL := FALSE;
    bAlarm_Pyro_L               : BOOL := FALSE;
    bAlarm_Pyro_LL              : BOOL := FALSE;
    bAlarm_Press_HH             : BOOL := FALSE;
    bAlarm_Press_H              : BOOL := FALSE;
    bAlarm_Press_L              : BOOL := FALSE;
    bAlarm_Press_LL             : BOOL := FALSE;
    bAlarm_Stress_HH            : BOOL := FALSE;
    bAlarm_Stress_H             : BOOL := FALSE;
    bAlarm_H2_LowLow            : BOOL := FALSE;
    bAlarm_H2_Low               : BOOL := FALSE;
    bAlarm_H2_HighHigh          : BOOL := FALSE;
    bAlarm_O2_HighHigh          : BOOL := FALSE;
    bAlarm_RibbonWaisting       : BOOL := FALSE;
    bAlarm_TopRollerAnySlip     : BOOL := FALSE;
    bAlarm_TopRollerCoolingFail : BOOL := FALSE;
    bAlarm_CulletTrapdoorOpen   : BOOL := FALSE;
    bAlarm_TMR_Degraded_Thick   : BOOL := FALSE;
    bAlarm_TMR_Degraded_Pyro    : BOOL := FALSE;
    bAlarm_TMR_Degraded_Press   : BOOL := FALSE;
    bAlarm_TMR_Degraded_Stress  : BOOL := FALSE;
    bAlarm_TMR_Trip_AllFailed   : BOOL := FALSE;

    (* General Purpose Loop Iterators and Execution Housekeeping *)
    idxRow                      : INT;             (* Matrix row indexing variable *)
    idxCol                      : INT;             (* Matrix column indexing variable *)
    idxIter                     : INT;             (* Unrolled MPC PGD iteration loop index *)
    idxRoller                   : INT;             (* Top-roller machine pair loop counter [1..16] *)
    idxZone                     : INT;             (* Thermal heater and damper zone iterator [1..12] *)
    rScanDeltaTime_sec          : REAL;            (* Discrete scan execution delta time converted to seconds [s] *)
    bInitializationExecuted     : BOOL := FALSE;   (* Cold-start matrix and parameter initialization latch *)
END_VAR
"""

if __name__ == "__main__":
    s = generate_var_internal()
    print(f"Var internal length: {len(s)} chars")
