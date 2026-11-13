# mega_casting_builder/build_var.py

def get_var_declarations():
    return """VAR
    (* =================================================================================================================
     * SECTION 1: SYSTEM INITIALIZATION & EXECUTION CONTROL FLAGS
     * ================================================================================================================= *)
    bStateSpace_Initialized                : BOOL := FALSE; (* Cold-start initialization flag for matrix coefficients *)
    bSystem_ColdBoot                       : BOOL := TRUE;  (* One-shot reboot flag *)
    bCycleStarted                          : BOOL := FALSE; (* Active cycle execution in progress *)
    bCycleAborted                          : BOOL := FALSE; (* Execution aborted due to safety or process trip *)
    rScanDeltaT                            : REAL := 0.001; (* Internal working cycle time copy [s] *)
    rTotalRunTime_Sec                      : REAL := 0.0;   (* Cumulative controller operational hours timer [s] *)
    rShotCycle_Timer_Sec                   : REAL := 0.0;   (* Active single-shot injection execution timer [s] *)

    (* =================================================================================================================
     * SECTION 2: 6x6 CYBER-PHYSICAL STATE-SPACE MATRICES & ESTIMATOR VECTORS (Ts = 1.0 ms)
     * Continuous-to-discrete system representation x[k+1] = A * x[k] + B * u[k] + Ew * w[k]
     * Sensor observation model             y[k]   = C * x[k] + D * u[k]
     * Observer correction (Kalman)         x_hat[k+1] = A * x_hat[k] + B * u[k] + L * (y[k] - y_hat[k])
     * States:
     *   x1: Plunger Linear Stroke Position [mm]
     *   x2: Plunger Instantaneous Axial Velocity [m/s]
     *   x3: Injection Cylinder Head Chamber Pressure [bar]
     *   x4: Molten Aluminum In-Cavity Dynamic Pressure [bar]
     *   x5: Parting Plane Vacuum Evacuation Pressure [mbar]
     *   x6: Clamping Tie-Bar Dynamic Elastic Strain Stretch [um]
     * Inputs:
     *   u1: Ultra-Fast Servo Proportional Injection Valve Spool [%] (-100% to +100%)
     *   u2: High-Speed Accumulator Discharge Cartridge Valve Trim [%] (0 to 100%)
     *   u3: Phase 3 Intensification Booster Valve [%] (0 to 100%)
     *   u4: Parting Plane Vacuum Evacuation Throttle Valve [%] (0 to 100%)
     *   u5: Mold Multi-Circuit Thermal Oil Flow Trim [%] (0 to 100%)
     *   u6: Toggle Clamping Locking Pilot Pressure Trim [%] (0 to 100%)
     * ================================================================================================================= *)
    rMatrix_A                              : ARRAY[1..6, 1..6] OF REAL; (* Discrete State Transition Matrix A (6x6) *)
    rMatrix_B                              : ARRAY[1..6, 1..6] OF REAL; (* Actuator Input Coupling Matrix B (6x6) *)
    rMatrix_Ew                             : ARRAY[1..6, 1..6] OF REAL; (* Exogenous Disturbance Matrix Ew (6x6) *)
    rMatrix_C                              : ARRAY[1..6, 1..6] OF REAL; (* Measurement Output Matrix C (6x6) *)
    rMatrix_D                              : ARRAY[1..6, 1..6] OF REAL; (* Direct Feedthrough Matrix D (6x6) *)
    rMatrix_L                              : ARRAY[1..6, 1..6] OF REAL; (* Steady-State Observer Innovation Gain L (6x6) *)

    rState_x                               : ARRAY[1..6] OF REAL;       (* True Internal Physical State Vector x *)
    rState_x_hat                           : ARRAY[1..6] OF REAL;       (* Estimated Filtered State Vector x_hat *)
    rState_x_hat_next                      : ARRAY[1..6] OF REAL;       (* Prior Prediction Vector x_hat[k+1|k] *)
    rInput_u                               : ARRAY[1..6] OF REAL;       (* Current Actuator Command Vector u *)
    rInput_u_prev                          : ARRAY[1..6] OF REAL;       (* Previous Scan Actuator Command Vector u[k-1] *)
    rOutput_y                              : ARRAY[1..6] OF REAL;       (* Measured Observation Vector y *)
    rOutput_y_hat                          : ARRAY[1..6] OF REAL;       (* Predicted Observation Vector y_hat *)
    rDisturbance_w                         : ARRAY[1..6] OF REAL;       (* Estimated Disturbance Vector w *)
    rInnovation_Residual                   : ARRAY[1..6] OF REAL;       (* Innovation Residual Vector e_y = y - y_hat *)

    (* =================================================================================================================
     * SECTION 3: MODEL PREDICTIVE CONTROL (MPC) RECURSIVE HORIZON & PROJECTED GRADIENT DESCENT (PGD)
     * Horizon N = 5 steps, 10 Unrolled Optimization Iterations per Scan
     * ================================================================================================================= *)
    rMPC_Matrix_Q                          : ARRAY[1..6, 1..6] OF REAL; (* State Trajectory Tracking Penalty Matrix Q *)
    rMPC_Matrix_R                          : ARRAY[1..6, 1..6] OF REAL; (* Actuator Effort Energy Penalty Matrix R *)
    rMPC_Matrix_P                          : ARRAY[1..6, 1..6] OF REAL; (* Terminal Horizon State Penalty Matrix P *)
    rMPC_Matrix_S                          : ARRAY[1..6, 1..6] OF REAL; (* Actuator Slew Rate Dynamic Penalty Matrix S *)

    rMPC_Ref_x                             : ARRAY[1..6] OF REAL;       (* State Target Trajectory Reference Vector *)
    rMPC_Pred_u                            : ARRAY[1..5, 1..6] OF REAL; (* Predicted Actuator Trajectory across Horizon *)
    rMPC_Pred_x                            : ARRAY[1..5, 1..6] OF REAL; (* Predicted State Trajectory across Horizon *)
    rMPC_Grad_u                            : ARRAY[1..5, 1..6] OF REAL; (* Analytical Gradient Vector dJ/du *)

    rMPC_u_Min                             : ARRAY[1..6] OF REAL;       (* Hard Lower Actuator Saturation Limits *)
    rMPC_u_Max                             : ARRAY[1..6] OF REAL;       (* Hard Upper Actuator Saturation Limits *)
    rMPC_Slew_Max                          : ARRAY[1..6] OF REAL;       (* Maximum Allowable Slew Rate per Scan Delta_u *)

    rMPC_LearningRate_Alpha                : REAL := 0.015;             (* Projected Gradient Descent Step Size Alpha *)
    rMPC_Cost_Total                        : REAL := 0.0;               (* Current Horizon Evaluated Quadratic Cost J *)
    rMPC_Cost_State                        : REAL := 0.0;               (* State Deviation Sub-Cost *)
    rMPC_Cost_Actuator                     : REAL := 0.0;               (* Actuator Energy Sub-Cost *)
    rMPC_Cost_Slew                         : REAL := 0.0;               (* Dynamic Slew Rate Sub-Cost *)

    (* MPC Internal Iteration Counters *)
    k_iter                                 : INT := 1;
    n_step                                 : INT := 1;
    i_idx                                  : INT := 1;
    j_idx                                  : INT := 1;
    m_idx                                  : INT := 1;

    (* =================================================================================================================
     * SECTION 4: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) ARCHITECTURE & DISCREPANCY TIMERS
     * Pairwise differential comparison, discrepancy fault counters, bumpless transfer low-pass smoothing
     * ================================================================================================================= *)
    (* Plunger Linear Position TMR *)
    rPlunger_Diff_12                       : REAL := 0.0;
    rPlunger_Diff_23                       : REAL := 0.0;
    rPlunger_Diff_31                       : REAL := 0.0;
    rPlunger_Discrepancy_Timer1            : REAL := 0.0;
    rPlunger_Discrepancy_Timer2            : REAL := 0.0;
    rPlunger_Discrepancy_Timer3            : REAL := 0.0;
    bPlunger_Sensor1_Healthy               : BOOL := TRUE;
    bPlunger_Sensor2_Healthy               : BOOL := TRUE;
    bPlunger_Sensor3_Healthy               : BOOL := TRUE;
    iPlunger_TMR_HealthMode                : INT  := 3; (* 3=Healthy 2oo3, 2=Degraded 2oo2/1oo2, 1=Single Channel, 0=Fail *)
    rPlungerPos_Raw_Voted                  : REAL := 0.0;
    rPlungerPos_Prev                       : REAL := 0.0;

    (* Hydraulic Injection Head Pressure TMR *)
    rHeadPress_Diff_12                     : REAL := 0.0;
    rHeadPress_Diff_23                     : REAL := 0.0;
    rHeadPress_Diff_31                     : REAL := 0.0;
    rHeadPress_Discrepancy_Timer1          : REAL := 0.0;
    rHeadPress_Discrepancy_Timer2          : REAL := 0.0;
    rHeadPress_Discrepancy_Timer3          : REAL := 0.0;
    bHeadPress_Sensor1_Healthy             : BOOL := TRUE;
    bHeadPress_Sensor2_Healthy             : BOOL := TRUE;
    bHeadPress_Sensor3_Healthy             : BOOL := TRUE;
    iHeadPress_TMR_HealthMode              : INT  := 3;
    rHeadPress_Raw_Voted                   : REAL := 0.0;

    (* In-Cavity Quartz Piezoelectric Pressure TMR *)
    rCavityPress_Diff_12                   : REAL := 0.0;
    rCavityPress_Diff_23                   : REAL := 0.0;
    rCavityPress_Diff_31                   : REAL := 0.0;
    rCavityPress_Discrepancy_Timer1        : REAL := 0.0;
    rCavityPress_Discrepancy_Timer2        : REAL := 0.0;
    rCavityPress_Discrepancy_Timer3        : REAL := 0.0;
    bCavityPress_Sensor1_Healthy           : BOOL := TRUE;
    bCavityPress_Sensor2_Healthy           : BOOL := TRUE;
    bCavityPress_Sensor3_Healthy           : BOOL := TRUE;
    iCavityPress_TMR_HealthMode            : INT  := 3;
    rCavityPress_Raw_Voted                 : REAL := 0.0;
    rCavityPress_Prev                      : REAL := 0.0;

    (* Parting Plane Vacuum Evacuation TMR *)
    rVac_Diff_12                           : REAL := 0.0;
    rVac_Diff_23                           : REAL := 0.0;
    rVac_Diff_31                           : REAL := 0.0;
    rVac_Discrepancy_Timer1                : REAL := 0.0;
    rVac_Discrepancy_Timer2                : REAL := 0.0;
    rVac_Discrepancy_Timer3                : REAL := 0.0;
    bVac_Sensor1_Healthy                   : BOOL := TRUE;
    bVac_Sensor2_Healthy                   : BOOL := TRUE;
    bVac_Sensor3_Healthy                   : BOOL := TRUE;
    iVac_TMR_HealthMode                    : INT  := 3;
    rVac_Raw_Voted                         : REAL := 0.0;
    rVac_Prev                              : REAL := 0.0;
    rVac_LeakRate_Actual_mbar_s            : REAL := 0.0;

    (* TMR Discrepancy Tolerances & Persistence Limits *)
    rTMR_Tol_Pos_mm                        : REAL := 1.25;  (* Maximum tolerated plunger discrepancy [mm] *)
    rTMR_Tol_HeadPress_bar                 : REAL := 15.0;  (* Maximum tolerated head pressure discrepancy [bar] *)
    rTMR_Tol_CavityPress_bar               : REAL := 25.0;  (* Maximum tolerated cavity piezo discrepancy [bar] *)
    rTMR_Tol_Vac_mbar                      : REAL := 5.0;   (* Maximum tolerated vacuum discrepancy [mbar] *)
    rTMR_Discrepancy_TripTime_Sec          : REAL := 0.050; (* Persistence before isolating faulty sensor [s] *)

    (* Bumpless Transfer Smoothing Coefficients *)
    rBumpless_Alpha_Pos                    : REAL := 0.85;
    rBumpless_Alpha_Head                   : REAL := 0.80;
    rBumpless_Alpha_Cavity                 : REAL := 0.70;
    rBumpless_Alpha_Vac                    : REAL := 0.90;

    (* =================================================================================================================
     * SECTION 5: 6,000-TON TOGGLE CLAMP & TIE-BAR ELASTOMACRO STRAIN CALCULATIONS
     * 4-Corner Column Elasticity: F = E * A * (Delta_L / L)
     * ================================================================================================================= *)
    rTieBar_Modulus_GPa                    : REAL := 206.0;   (* 42CrMo4 Forged Alloy Steel Elastic Modulus [GPa] *)
    rTieBar_Diameter_m                     : REAL := 0.440;   (* Tie-bar column outer diameter [m] *)
    rTieBar_Area_m2                        : REAL := 0.15205; (* Column cross-sectional area [m2] *)
    rTieBar_Length_Nominal_m               : REAL := 12.20;   (* Effective active tie-bar load length [m] *)

    rForce_Column1_kN                      : REAL := 0.0;     (* Column 1 Top-Left Axial Force [kN] *)
    rForce_Column2_kN                      : REAL := 0.0;     (* Column 2 Top-Right Axial Force [kN] *)
    rForce_Column3_kN                      : REAL := 0.0;     (* Column 3 Bottom-Left Axial Force [kN] *)
    rForce_Column4_kN                      : REAL := 0.0;     (* Column 4 Bottom-Right Axial Force [kN] *)

    rPlaten_Delta_TopBottom_um             : REAL := 0.0;     (* Top to bottom platen tilt deflection [um] *)
    rPlaten_Delta_LeftRight_um             : REAL := 0.0;     (* Left to right platen tilt deflection [um] *)
    rPlaten_MaxEccentricity_Pct            : REAL := 0.0;     (* Max load asymmetry ratio [%] *)

    (* =================================================================================================================
     * SECTION 6: HYDRAULIC INJECTION GEOMETRY & FLUID MECHANICS
     * Critical Wave Crest Suppression & Phase 1 Wave Velocity (v_wave = SQRT(g * h_fill))
     * ================================================================================================================= *)
    rCylHead_Diameter_m                    : REAL := 0.320;   (* Injection hydraulic cylinder bore [m] *)
    rCylRod_Diameter_m                     : REAL := 0.180;   (* Injection hydraulic piston rod diameter [m] *)
    rPlunger_Diameter_m                    : REAL := 0.140;   (* Shot sleeve beryllium-copper plunger tip diameter [m] *)
    rCylHead_Area_m2                       : REAL := 0.08042; (* Cylinder head cross-sectional area [m2] *)
    rCylRod_Area_m2                        : REAL := 0.05498; (* Cylinder rod annular area [m2] *)
    rPlunger_Area_m2                       : REAL := 0.01539; (* Plunger tip cross-sectional area [m2] *)

    rSleeve_Fill_Ratio                     : REAL := 0.45;    (* Liquid aluminum fill fraction in sleeve (0.35..0.55) *)
    rCritical_Wave_Velocity_ms             : REAL := 0.865;   (* Wave speed limit avoiding wave reflection [m/s] *)
    rAcoustic_FillFront_Gradient           : REAL := 0.0;     (* Measured rate of rise dP_cavity/dt [bar/ms] *)

    (* Phase 3 Intensification Timing Engine *)
    bIntensification_Triggered             : BOOL := FALSE;   (* Latch indicating Phase 3 entry *)
    rIntensification_Timer_ms              : REAL := 0.0;     (* Timer tracking pressure rise from fill to peak [ms] *)
    rIntensification_StartPress_bar        : REAL := 0.0;     (* Hydraulic pressure at onset of intensification [bar] *)
    bIntensification_Complete              : BOOL := FALSE;   (* Intensification target pressure reached *)

    (* Biscuit Thickness Tracking *)
    rTotalStrokeLength_mm                  : REAL := 1250.0;  (* Total mechanical injection cylinder stroke [mm] *)
    rPlunger_FinalCushionPos_mm            : REAL := 0.0;     (* Plunger stroke coordinate at solidification rest [mm] *)

    (* =================================================================================================================
     * SECTION 7: 14-STAGE DETERMINISTIC PRODUCTION FINITE STATE MACHINE (FSM)
     * Step indices 0 through 13 strictly mapped to production HPDC sequence
     * ================================================================================================================= *)
    iFSM_State                             : INT := 0;        (* Current execution stage *)
    iFSM_PrevState                         : INT := 0;        (* Previous scan stage *)
    bFSM_FirstScan                         : BOOL := TRUE;    (* One-shot entry trigger for active stage *)
    rFSM_StateTimer_s                      : REAL := 0.0;     (* Dwell timer within active stage [s] *)
    rFSM_StateTimeout_s                    : REAL := 120.0;   (* Watchdog timeout limit for active stage [s] *)

    (* Stage Completion / Interlock Handshake Flags *)
    bPreheat_Balanced                      : BOOL := FALSE;
    bLadle_Pour_Ready                      : BOOL := FALSE;
    bClamp_Locked_Permissive               : BOOL := FALSE;
    bVacuum_Evacuated_Permissive           : BOOL := FALSE;
    bPhase1_Complete                       : BOOL := FALSE;
    bPhase2_Complete                       : BOOL := FALSE;
    bPhase3_Complete                       : BOOL := FALSE;
    bPhase4_Complete                       : BOOL := FALSE;
    bVacuum_Vented_Permissive              : BOOL := FALSE;
    bClamp_Open_Permissive                 : BOOL := FALSE;
    bDemold_Ejection_Permissive            : BOOL := FALSE;
    bPart_Extracted_Permissive             : BOOL := FALSE;
    bDie_Sprayed_Permissive                : BOOL := FALSE;

    (* =================================================================================================================
     * SECTION 8: POROSITY PREDICTION & CYBER-PHYSICAL SOLIDIFICATION CRITERION
     * Multi-Factor Defect Probability (Gas Entrapment, Shrinkage Feeding, Thermal Gradient)
     * ================================================================================================================= *)
    rPorosity_GasEntrap_Factor             : REAL := 0.0;     (* Gas porosity score driven by vacuum level & wave break *)
    rPorosity_Shrinkage_Factor             : REAL := 0.0;     (* Shrinkage porosity score driven by intensification delay *)
    rPorosity_Thermal_Factor               : REAL := 0.0;     (* Defect score driven by die delta T and cooling gradient *)
    rWeiler_Porosity_Index                 : REAL := 0.0;     (* Semi-empirical Weiler casting integrity index *)
    rSolidification_CoolingRate_C_s        : REAL := 0.0;     (* Measured steel die interface temperature rate [C/s] *)
    rPrev_FixedDie_Temp                    : REAL := 220.0;

    (* =================================================================================================================
     * SECTION 9: MULTI-CIRCUIT THERMAL OIL PID REGULATION
     * Discrete Parallel Form PID with Anti-Windup for Fixed and Moving Die Cavity Halves
     * ================================================================================================================= *)
    rThermal_Kp                            : REAL := 3.50;    (* Proportional gain [%/deg C] *)
    rThermal_Ki                            : REAL := 0.045;   (* Integral gain [%/(deg C * s)] *)
    rThermal_Kd                            : REAL := 12.0;    (* Derivative gain [% * s / deg C] *)
    rThermal_Integral_Fixed                : REAL := 0.0;     (* Accumulated integral error fixed die *)
    rThermal_Integral_Moving               : REAL := 0.0;     (* Accumulated integral error moving die *)
    rThermal_PrevError_Fixed               : REAL := 0.0;     (* Error at scan k-1 fixed die *)
    rThermal_PrevError_Moving              : REAL := 0.0;     (* Error at scan k-1 moving die *)

    (* =================================================================================================================
     * SECTION 10: ISA-18.2 MULTI-TIER ALARM TRIP MATRIX & HYSTERESIS ENGINE
     * 4-Tier Monitoring: High-High (HH), High (H), Low (L), Low-Low (LL) with Clear Deadbands
     * ================================================================================================================= *)
    (* Hydraulic Head Overpressure Trips *)
    rTrip_HeadPress_HH                     : REAL := 1250.0;  (* Critical hydraulic line burst limit [bar] *)
    rTrip_HeadPress_H                      : REAL := 1150.0;  (* High operational warning limit [bar] *)
    rDeadband_HeadPress                    : REAL := 15.0;    (* Reset clearance hysteresis [bar] *)
    bAlarm_HeadPress_HH                    : BOOL := FALSE;
    bAlarm_HeadPress_H                     : BOOL := FALSE;

    (* In-Cavity Dynamic Shock Trips *)
    rTrip_CavityPress_HH                   : REAL := 1100.0;  (* Peak mold cavity safety threshold [bar] *)
    rTrip_CavityPress_H                    : REAL := 950.0;   (* Infill completion threshold [bar] *)
    rDeadband_CavityPress                  : REAL := 20.0;    (* Reset hysteresis [bar] *)
    bAlarm_CavityPress_HH                  : BOOL := FALSE;
    bAlarm_CavityPress_H                   : BOOL := FALSE;

    (* Plunger Velocity Overspeed Trips *)
    rTrip_PlungerVel_HH                    : REAL := 11.0;    (* Plunger runaway cavitation limit [m/s] *)
    rTrip_PlungerVel_H                     : REAL := 10.0;    (* Maximum recipe upper limit [m/s] *)
    rDeadband_PlungerVel                   : REAL := 0.20;    (* Reset hysteresis [m/s] *)
    bAlarm_PlungerVel_HH                   : BOOL := FALSE;
    bAlarm_PlungerVel_H                    : BOOL := FALSE;

    (* Parting Plane Vacuum Insufficiency Trips *)
    rTrip_Vac_LL                           : REAL := 100.0;   (* Severe evacuation failure trip [mbar] *)
    rTrip_Vac_L                            : REAL := 45.0;    (* Sub-optimal vacuum warning [mbar] *)
    rDeadband_Vac                          : REAL := 5.0;     (* Reset hysteresis [mbar] *)
    bAlarm_Vac_LL                          : BOOL := FALSE;
    bAlarm_Vac_L                           : BOOL := FALSE;

    (* Clamping Force Tonnage Underload & Overload Trips *)
    rTrip_Clamp_HH                         : REAL := 66000.0; (* Extreme tie-bar tensile limit [kN] *)
    rTrip_Clamp_LL                         : REAL := 52000.0; (* Risk of metal flash liquid blowout [kN] *)
    rDeadband_Clamp                        : REAL := 500.0;   (* Reset hysteresis [kN] *)
    bAlarm_Clamp_HH                        : BOOL := FALSE;
    bAlarm_Clamp_LL                        : BOOL := FALSE;

    (* Platen Tilt Parallelism Asymmetry Trips *)
    rTrip_PlatenTilt_HH                    : REAL := 180.0;   (* Destructive tie-bar shear deflection [um] *)
    rTrip_PlatenTilt_H                     : REAL := 95.0;    (* Preventative platen alignment warning [um] *)
    rDeadband_PlatenTilt                   : REAL := 10.0;    (* Reset hysteresis [um] *)
    bAlarm_PlatenTilt_HH                   : BOOL := FALSE;
    bAlarm_PlatenTilt_H                    : BOOL := FALSE;

    (* Casting Biscuit Thickness Integrity Trips *)
    rTrip_Biscuit_HH                       : REAL := 32.0;    (* Overfilling / sleeve overflow [mm] *)
    rTrip_Biscuit_LL                       : REAL := 12.0;    (* Metal volume starvation / short shot [mm] *)
    rDeadband_Biscuit                      : REAL := 1.5;     (* Reset hysteresis [mm] *)
    bAlarm_Biscuit_HH                      : BOOL := FALSE;
    bAlarm_Biscuit_LL                      : BOOL := FALSE;

    (* Intensification Rise Delay Trip *)
    rTrip_IntensificationDelay_HH          : REAL := 22.0;    (* Gate premature freeze-off threshold [ms] *)
    bAlarm_IntensificationDelay_HH         : BOOL := FALSE;

    (* Sensor Discrepancy & Hardware Trips *)
    bAlarm_Plunger_TMR_Fault               : BOOL := FALSE;
    bAlarm_HeadPress_TMR_Fault             : BOOL := FALSE;
    bAlarm_CavityPress_TMR_Fault           : BOOL := FALSE;
    bAlarm_Vac_TMR_Fault                   : BOOL := FALSE;
    bAlarm_EmergencyStop_Active            : BOOL := FALSE;
    bAlarm_SafetyGate_Breach               : BOOL := FALSE;
    bAlarm_FlashBlowout_Detected           : BOOL := FALSE;

    (* First-Out Recording Engine *)
    bFirstOut_Latched                      : BOOL := FALSE;   (* True if first-out trip captured *)
    dwFirstOut_Code                        : DWORD := 16#00000000;
END_VAR
"""
