# ammonia_refrigeration_builder/build_st_var.py

def get_var_declarations():
    return """VAR
    (* ================================================================================================================ *)
    (* FIRST-PRINCIPLES CYBER-PHYSICAL DISCRETE STATE-SPACE MATRICES & VECTORS (8 STATES, 6 CONTROLS, 3 DISTURBANCES)  *)
    (* ================================================================================================================ *)
    (* Discrete State Transition Matrix A (8x8) @ Sample Time dt = 100 ms *)
    matA                              : ARRAY[1..8, 1..8] OF REAL;
    (* Control Input Distribution Matrix B (8x6) *)
    matB                              : ARRAY[1..8, 1..6] OF REAL;
    (* Exogenous Disturbance Input Matrix Ew (8x3) *)
    matEw                             : ARRAY[1..8, 1..3] OF REAL;
    (* Measurement Observation Matrix C (8x8) *)
    matC                              : ARRAY[1..8, 1..8] OF REAL;
    (* Direct Transmission Feedthrough Matrix D (8x6) *)
    matD                              : ARRAY[1..8, 1..6] OF REAL;
    (* Steady-State Kalman Filter Observer Gain Matrix K (8x8) *)
    matK                              : ARRAY[1..8, 1..8] OF REAL;

    (* Cyber-Physical State Vectors *)
    (* x1: Suction Header Pressure Deviation [bar]                                                                     *)
    (* x2: Suction Vapor Enthalpy Deviation [kJ/kg]                                                                    *)
    (* x3: Compressor Discharge Manifold Pressure Deviation [bar]                                                      *)
    (* x4: Compressor Discharge Gas Temperature Deviation [deg C]                                                      *)
    (* x5: Lubricating Oil Sump Bulk Temperature Deviation [deg C]                                                     *)
    (* x6: Economizer Subcooler Intermediate Pressure Deviation [bar]                                                  *)
    (* x7: Evaporative Condenser Basin Sump Water Temperature Deviation [deg C]                                        *)
    (* x8: Common Suction Superheat Temperature Deviation [K]                                                          *)
    vecX                              : ARRAY[1..8] OF REAL;    (* Instantaneous Internal State Vector [k] *)
    vecX_next                         : ARRAY[1..8] OF REAL;    (* A-Priori Propagated State Vector [k+1] *)
    vecX_hat                          : ARRAY[1..8] OF REAL;    (* A-Posteriori Observer Corrected State Vector [k] *)
    vecR                              : ARRAY[1..8] OF REAL;    (* Dynamic MPC Reference Target Vector [r] *)
    vecY_meas                         : ARRAY[1..8] OF REAL;    (* Physical Voted Measurement Vector [y] *)
    vecY_pred                         : ARRAY[1..8] OF REAL;    (* Observer Predicted Measurement Vector [y_hat] *)
    vecY_innov                        : ARRAY[1..8] OF REAL;    (* Measurement Innovation Residual Vector [e = y - y_hat] *)

    (* Control Vector u (6 Manipulated Actuators) *)
    (* u1: Lead Compressor 1 Slide-Valve Capacity Target [0.0..100.0 %]                                               *)
    (* u2: Lead Compressor 1 VFD Speed Inverter Output [30.0..60.0 Hz]                                                *)
    (* u3: Lag Compressor 2 Slide-Valve Capacity Target [0.0..100.0 %]                                                *)
    (* u4: Economizer Liquid Subcooling Stepper EEV Opening [0.0..100.0 %]                                            *)
    (* u5: Evaporative Condenser EC Fan Bank Modulation [0.0..100.0 %]                                                 *)
    (* u6: Oil Cooler Thermostatic 3-Way Valve Bypass [0.0..100.0 %]                                                  *)
    vecU                              : ARRAY[1..6] OF REAL;    (* Instantaneous Control Actuator Vector [u] *)
    vecU_prev                         : ARRAY[1..6] OF REAL;    (* Previous Cycle Actuator Vector [u(k-1)] *)
    vecDeltaU                         : ARRAY[1..6] OF REAL;    (* Actuator Slew Rate Vector [Delta_u] *)
    vecU_opt                          : ARRAY[1..6] OF REAL;    (* PGD Optimized Output Control Vector *)
    vecU_min                          : ARRAY[1..6] OF REAL;    (* Lower Actuator Saturation Box Limits *)
    vecU_max                          : ARRAY[1..6] OF REAL;    (* Upper Actuator Saturation Box Limits *)
    vecSlew_max                       : ARRAY[1..6] OF REAL;    (* Maximum Permissible Slew Limits per Sample Cycle *)

    (* Exogenous Disturbance Vector w (3 Thermal / Hydraulic Disturbances) *)
    (* w1: Psychrometric Ambient Wet-Bulb Temperature Deviation [deg C]                                               *)
    (* w2: Refrigerated Warehouse Dynamic Thermal Load Shock [kW]                                                     *)
    (* w3: Reverse Hot-Gas Defrost Diversion Vapor Mass Flow [kg/s]                                                    *)
    vecW                              : ARRAY[1..3] OF REAL;    (* Dynamic Disturbance Vector [w] *)

    (* ================================================================================================================ *)
    (* RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) QUADRATIC COST MATRICES & PGD SOLVER                           *)
    (* ================================================================================================================ *)
    matQ                              : ARRAY[1..8, 1..8] OF REAL; (* State Tracking Error Weighting Matrix Q *)
    matR                              : ARRAY[1..6, 1..6] OF REAL; (* Control Actuation Effort Weighting Matrix R *)
    matS                              : ARRAY[1..6, 1..6] OF REAL; (* Control Slew Rate Penalty Matrix S *)
    matP                              : ARRAY[1..8, 1..8] OF REAL; (* Terminal State Lyapunov Weighting Matrix P *)
    vecGradJ                          : ARRAY[1..6] OF REAL;       (* Projected Gradient Cost Vector [grad_J] *)
    rMpcStepSize_alpha                : REAL := 0.0125;            (* PGD Iteration Convergence Step Size *)
    rMpcTotalCost_J                   : REAL := 0.0;               (* Real-Time Quadratic Cost Value *)
    iPgdIteration                     : INT := 0;                  (* Unrolled PGD Iteration Loop Counter *)
    bMatricesInitialized              : BOOL := FALSE;             (* Cold-Boot One-Shot Initialization Latch *)

    (* ================================================================================================================ *)
    (* 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING STRUCTURES & DISCREPANCY TIMERS                               *)
    (* ================================================================================================================ *)
    (* Channel 1: Suction Header Pressure (PT-101A/B/C) [bar] *)
    rTMR_Suction_Median               : REAL := 2.35;
    rTMR_Suction_DevA                 : REAL := 0.0;
    rTMR_Suction_DevB                 : REAL := 0.0;
    rTMR_Suction_DevC                 : REAL := 0.0;
    bTMR_Suction_HealthyA             : BOOL := TRUE;
    bTMR_Suction_HealthyB             : BOOL := TRUE;
    bTMR_Suction_HealthyC             : BOOL := TRUE;
    rTMR_Suction_TimerA               : REAL := 0.0;
    rTMR_Suction_TimerB               : REAL := 0.0;
    rTMR_Suction_TimerC               : REAL := 0.0;
    rDiscLimit_Suction_bar            : REAL := 0.35;     (* Max Discrepancy Tolerance: 0.35 bar *)

    (* Channel 2: Compressor Discharge Temperature (TT-201A/B/C) [deg C] *)
    rTMR_DischTemp_Median             : REAL := 82.5;
    rTMR_DischTemp_DevA               : REAL := 0.0;
    rTMR_DischTemp_DevB               : REAL := 0.0;
    rTMR_DischTemp_DevC               : REAL := 0.0;
    bTMR_DischTemp_HealthyA           : BOOL := TRUE;
    bTMR_DischTemp_HealthyB           : BOOL := TRUE;
    bTMR_DischTemp_HealthyC           : BOOL := TRUE;
    rTMR_DischTemp_TimerA             : REAL := 0.0;
    rTMR_DischTemp_TimerB             : REAL := 0.0;
    rTMR_DischTemp_TimerC             : REAL := 0.0;
    rDiscLimit_DischTemp_degC         : REAL := 5.0;      (* Max Discrepancy Tolerance: 5.0 deg C *)

    (* Channel 3: Lubricating Oil Differential Pressure (PDT-301A/B/C) [bar] *)
    rTMR_OilDP_Median                 : REAL := 3.20;
    rTMR_OilDP_DevA                   : REAL := 0.0;
    rTMR_OilDP_DevB                   : REAL := 0.0;
    rTMR_OilDP_DevC                   : REAL := 0.0;
    bTMR_OilDP_HealthyA               : BOOL := TRUE;
    bTMR_OilDP_HealthyB               : BOOL := TRUE;
    bTMR_OilDP_HealthyC               : BOOL := TRUE;
    rTMR_OilDP_TimerA                 : REAL := 0.0;
    rTMR_OilDP_TimerB                 : REAL := 0.0;
    rTMR_OilDP_TimerC                 : REAL := 0.0;
    rDiscLimit_OilDP_bar              : REAL := 0.40;     (* Max Discrepancy Tolerance: 0.40 bar *)

    (* Channel 4: Machinery Room Ambient Ammonia Detection (AT-401A/B/C) [ppm] *)
    rTMR_AmbientNH3_Median            : REAL := 4.5;
    rTMR_AmbientNH3_DevA              : REAL := 0.0;
    rTMR_AmbientNH3_DevB              : REAL := 0.0;
    rTMR_AmbientNH3_DevC              : REAL := 0.0;
    bTMR_AmbientNH3_HealthyA          : BOOL := TRUE;
    bTMR_AmbientNH3_HealthyB          : BOOL := TRUE;
    bTMR_AmbientNH3_HealthyC          : BOOL := TRUE;
    rTMR_AmbientNH3_TimerA            : REAL := 0.0;
    rTMR_AmbientNH3_TimerB            : REAL := 0.0;
    rTMR_AmbientNH3_TimerC            : REAL := 0.0;
    rDiscLimit_AmbientNH3_ppm         : REAL := 15.0;     (* Max Discrepancy Tolerance: 15.0 ppm *)

    (* Channel 5: Economizer Intermediate Pressure (PT-501A/B/C) [bar] *)
    rTMR_EcoPres_Median               : REAL := 5.80;
    rTMR_EcoPres_DevA                 : REAL := 0.0;
    rTMR_EcoPres_DevB                 : REAL := 0.0;
    rTMR_EcoPres_DevC                 : REAL := 0.0;
    bTMR_EcoPres_HealthyA             : BOOL := TRUE;
    bTMR_EcoPres_HealthyB             : BOOL := TRUE;
    bTMR_EcoPres_HealthyC             : BOOL := TRUE;
    rTMR_EcoPres_TimerA               : REAL := 0.0;
    rTMR_EcoPres_TimerB               : REAL := 0.0;
    rTMR_EcoPres_TimerC               : REAL := 0.0;
    rDiscLimit_EcoPres_bar            : REAL := 0.50;     (* Max Discrepancy Tolerance: 0.50 bar *)

    (* Channel 6: Condenser High-Pressure Discharge (PT-601A/B/C) [bar] *)
    rTMR_CondPres_Median              : REAL := 11.85;
    rTMR_CondPres_DevA                : REAL := 0.0;
    rTMR_CondPres_DevB                : REAL := 0.0;
    rTMR_CondPres_DevC                : REAL := 0.0;
    bTMR_CondPres_HealthyA            : BOOL := TRUE;
    bTMR_CondPres_HealthyB            : BOOL := TRUE;
    bTMR_CondPres_HealthyC            : BOOL := TRUE;
    rTMR_CondPres_TimerA              : REAL := 0.0;
    rTMR_CondPres_TimerB              : REAL := 0.0;
    rTMR_CondPres_TimerC              : REAL := 0.0;
    rDiscLimit_CondPres_bar           : REAL := 0.60;     (* Max Discrepancy Tolerance: 0.60 bar *)

    (* Channel 7: Ambient Psychrometric Wet-Bulb Temperature [deg C] *)
    rTMR_WetBulb_Median               : REAL := 18.2;
    rTMR_WetBulb_DevA                 : REAL := 0.0;
    rTMR_WetBulb_DevB                 : REAL := 0.0;
    rTMR_WetBulb_DevC                 : REAL := 0.0;
    bTMR_WetBulb_HealthyA             : BOOL := TRUE;
    bTMR_WetBulb_HealthyB             : BOOL := TRUE;
    bTMR_WetBulb_HealthyC             : BOOL := TRUE;
    rTMR_WetBulb_TimerA               : REAL := 0.0;
    rTMR_WetBulb_TimerB               : REAL := 0.0;
    rTMR_WetBulb_TimerC               : REAL := 0.0;
    rDiscLimit_WetBulb_degC           : REAL := 2.0;      (* Max Discrepancy Tolerance: 2.0 deg C *)
    rTMR_DiscrepancyTripTime_sec      : REAL := 1.00;     (* Discrepancy Accumulation Trip Delay [s] *)

    (* ================================================================================================================ *)
    (* THERMODYNAMIC PROPERTIES & ANHYDROUS AMMONIA (R717) SATURATION POLYNOMIALS                                      *)
    (* ================================================================================================================ *)
    (* Antoine Equation Coefficients for Pure Anhydrous Ammonia: log10(P_bar) = A - (B / (T_K + C)) *)
    rAntoine_CoeffA                   : REAL := 4.86886;
    rAntoine_CoeffB                   : REAL := 1113.928;
    rAntoine_CoeffC                   : REAL := -10.409;
    rNH3_LiquidDensity_kg_m3          : REAL := 681.5;    (* Liquid Ammonia Density @ -33 deg C [kg/m3] *)
    rNH3_GasGasConstant_R             : REAL := 0.4882;   (* Specific Gas Constant R = R_u / M [kJ/(kg*K)] *)
    rNH3_IsentropicExponent_k         : REAL := 1.310;    (* Adiabatic Isentropic Exponent Cp/Cv for NH3 *)
    rNH3_LatentHeat_hfg_kJ_kg         : REAL := 1368.5;   (* Latent Heat of Vaporization @ -32 deg C [kJ/kg] *)

    (* Real-Time Computed Thermodynamic State Intermediate Variables *)
    rSuctionSatPressure_abs_bar       : REAL := 2.35;     (* Absolute Suction Saturation Pressure [bar] *)
    rCondSatPressure_abs_bar          : REAL := 11.85;    (* Absolute Condenser Saturation Pressure [bar] *)
    rCompPressureRatio                : REAL := 5.04;     (* Operating Compression Ratio P_disch / P_suct [-] *)
    rOptimumVi_Ratio                  : REAL := 3.25;     (* Theoretical Built-In Volume Ratio Vi = (P_d/P_s)^(1/k) *)
    rSuctionVaporDensity_kg_m3        : REAL := 1.82;     (* Superheated Suction Gas Density [kg/m3] *)
    rCompressorTotalFlow_m3_h         : REAL := 0.0;      (* Total Rack Swept Volume Displacement [m3/h] *)
    rRefrigerantMassFlow_kg_s         : REAL := 0.0;      (* Total Circulating Ammonia Mass Flow Rate [kg/s] *)
    rIsentropicEfficiency_eta         : REAL := 0.745;    (* Twin-Screw Isentropic Adiabatic Efficiency [-] *)
    rMechanicalEfficiency_eta         : REAL := 0.930;    (* Motor-Rotor Mechanical Transmission Efficiency [-] *)

    (* ================================================================================================================ *)
    (* DETERMINISTIC 14-STAGE FINITE STATE MACHINE (FSM) CONSTANTS & RUN-TIME TIMERS                                   *)
    (* ================================================================================================================ *)
    (* FSM Stage Enum Definitions *)
    FSM_STATE_INITIALIZE_SYS          : INT := 0;         (* System Cold Pre-Check & Hardware Diagnostic State *)
    FSM_STATE_PRE_LUBE_CIRCULATION    : INT := 1;         (* Auxiliary Oil Pump Lubrication Differential Priming *)
    FSM_STATE_STANDBY_READY           : INT := 2;         (* Standby System Ready Waiting for Refrigeration Load *)
    FSM_STATE_LEAD_COMP_SOFT_START    : INT := 3;         (* Compressor 1 Soft Ramp Start at 15% Unloaded Stroke *)
    FSM_STATE_BASE_LOAD_REGULATION    : INT := 4;         (* Lead Compressor Modulating VFD & Slide via MPC *)
    FSM_STATE_LAG_STAGE_UP_SEQUENCE   : INT := 5;         (* Load Exceeds Capacity: Start Comp 2 Stage-Up Delay *)
    FSM_STATE_MULTI_COMP_COORDINATION : INT := 6;         (* Dual / Triple Compressor Optimized Load Sharing *)
    FSM_STATE_ECONOMIZER_SUBCOOL_ACTIVE: INT := 7;        (* Flash Subcooling EEV Active with Intermediate Injection *)
    FSM_STATE_FLOATING_CONDENSING_CTRL: INT := 8;         (* Dynamic Wet-Bulb Tracking Evaporative Condenser Fans *)
    FSM_STATE_DEFROST_PUMP_DOWN       : INT := 9;         (* Liquid Line Shut, Coils Evacuating Liquid Ammonia *)
    FSM_STATE_DEFROST_HOT_GAS_FEED    : INT := 10;        (* High-Pressure Discharge Hot Gas Injected into Coils *)
    FSM_STATE_DEFROST_BLEED_REPRESS   : INT := 11;        (* Soft Equalization Bleed Relieving Trapped Pressure *)
    FSM_STATE_LAG_STAGE_DOWN_SEQUENCE : INT := 12;        (* Load Dropping: Lag Compressor Controlled Unload & Stop *)
    FSM_STATE_CONTROLLED_DECEL_STANDBY: INT := 13;        (* Controlled Deceleration, Glide Down & Post-Lube Cycle *)
    FSM_STATE_EMERGENCY_VENT_SCRUB    : INT := 14;        (* Toxic Ammonia Leak Scrubber Interlock & Dump Isolation *)

    (* FSM Internal Sequence State & Timers *)
    iFSM_State                        : INT := 0;         (* Current Operational State Register *)
    iFSM_NextState                    : INT := 0;         (* Target Evaluated Next State Register *)
    rFSM_StateStepTimer_sec           : REAL := 0.0;      (* Dwell Time Accumulator in Current Active State [s] *)
    rStageUpDelayTimer_sec            : REAL := 0.0;      (* Compressor Staging Up Sustained Load Delay [s] *)
    rStageDownDelayTimer_sec          : REAL := 0.0;      (* Compressor Staging Down Under-Load Delay [s] *)
    rComp1_AntiRecycleTimer_sec       : REAL := 900.0;    (* Compressor 1 Anti-Short-Cycling Restart Timer [s] *)
    rComp2_AntiRecycleTimer_sec       : REAL := 900.0;    (* Compressor 2 Anti-Short-Cycling Restart Timer [s] *)
    rComp3_AntiRecycleTimer_sec       : REAL := 900.0;    (* Compressor 3 Anti-Short-Cycling Restart Timer [s] *)
    rComp1_CumulativeRunHours         : REAL := 1420.5;   (* Operating Service Hour Meter Comp 1 [hours] *)
    rComp2_CumulativeRunHours         : REAL := 1390.2;   (* Operating Service Hour Meter Comp 2 [hours] *)
    rComp3_CumulativeRunHours         : REAL := 940.8;    (* Operating Service Hour Meter Comp 3 [hours] *)

    (* ================================================================================================================ *)
    (* 4-ZONE REVERSE HOT-GAS DEFROST SCHEDULER & STEP TIMERS                                                           *)
    (* ================================================================================================================ *)
    iDefrostZoneActive                : INT := 0;         (* Currently Active Hot Gas Defrost Zone Index [0..4] *)
    iDefrostStep_Zone1                : INT := 0;         (* Sub-Step State Machine for Zone 1 Defrost [0..4] *)
    iDefrostStep_Zone2                : INT := 0;         (* Sub-Step State Machine for Zone 2 Defrost [0..4] *)
    iDefrostStep_Zone3                : INT := 0;         (* Sub-Step State Machine for Zone 3 Defrost [0..4] *)
    iDefrostStep_Zone4                : INT := 0;         (* Sub-Step State Machine for Zone 4 Defrost [0..4] *)
    rDefrostTimer_Zone1               : REAL := 0.0;      (* Duration Accumulator for Zone 1 Defrost [s] *)
    rDefrostTimer_Zone2               : REAL := 0.0;      (* Duration Accumulator for Zone 2 Defrost [s] *)
    rDefrostTimer_Zone3               : REAL := 0.0;      (* Duration Accumulator for Zone 3 Defrost [s] *)
    rDefrostTimer_Zone4               : REAL := 0.0;      (* Duration Accumulator for Zone 4 Defrost [s] *)

    (* ================================================================================================================ *)
    (* ISA-18.2 MULTI-TIERED ALARM PARAMETERS, HYSTERESIS DEADBANDS & FIRST-OUT REGISTERS                              *)
    (* ================================================================================================================ *)
    (* Trip Limits & Deadbands *)
    rAlarmTrip_Suction_HH_bar         : REAL := 4.80;     (* Suction Pressure High-High Trip [bar] *)
    rAlarmTrip_Suction_H_bar          : REAL := 3.80;     (* Suction Pressure High Warning [bar] *)
    rAlarmTrip_Suction_L_bar          : REAL := 1.25;     (* Suction Pressure Low Warning [bar] *)
    rAlarmTrip_Suction_LL_bar         : REAL := 0.85;     (* Suction Pressure Low-Low Vacuum Trip [bar] *)
    rAlarmDeadband_Suction_bar        : REAL := 0.15;     (* Suction Pressure Alarm Clearance Hysteresis [bar] *)

    rAlarmTrip_DischPress_HH_bar      : REAL := 16.50;    (* Discharge Pressure High-High Safety Trip [bar] *)
    rAlarmTrip_DischPress_H_bar       : REAL := 14.50;    (* Discharge Pressure High Warning [bar] *)
    rAlarmTrip_DischPress_L_bar       : REAL := 8.20;     (* Discharge Pressure Low Warning (Oil Lift Floor) [bar] *)
    rAlarmTrip_DischPress_LL_bar      : REAL := 6.80;     (* Discharge Pressure Low-Low Safety Trip [bar] *)
    rAlarmDeadband_DischPress_bar     : REAL := 0.40;     (* Discharge Pressure Hysteresis Deadband [bar] *)

    rAlarmTrip_DischTemp_HH_degC      : REAL := 115.0;    (* Discharge Temperature High-High Trip [deg C] *)
    rAlarmTrip_DischTemp_H_degC       : REAL := 102.0;    (* Discharge Temperature High Warning [deg C] *)
    rAlarmTrip_DischTemp_L_degC       : REAL := 45.0;     (* Discharge Temperature Low Warning [deg C] *)
    rAlarmDeadband_DischTemp_degC     : REAL := 3.0;      (* Discharge Temperature Hysteresis Deadband [deg C] *)

    rAlarmTrip_OilDP_LL_bar           : REAL := 1.50;     (* Oil Differential Pressure Low-Low Trip [bar] *)
    rAlarmTrip_OilDP_L_bar            : REAL := 2.00;     (* Oil Differential Pressure Low Warning [bar] *)
    rAlarmTrip_OilDP_HH_bar           : REAL := 5.20;     (* Oil Differential Pressure Filter Plugged Trip [bar] *)
    rAlarmDeadband_OilDP_bar          : REAL := 0.20;     (* Oil DP Alarm Clearance Hysteresis [bar] *)

    rAlarmTrip_OilTemp_HH_degC        : REAL := 72.0;     (* Oil Sump High-High Thermal Breakdown Trip [deg C] *)
    rAlarmTrip_OilTemp_H_degC         : REAL := 62.0;     (* Oil Sump High Temperature Warning [deg C] *)
    rAlarmTrip_OilTemp_L_degC         : REAL := 32.0;     (* Oil Sump Low Viscosity Cold Warning [deg C] *)
    rAlarmTrip_OilTemp_LL_degC        : REAL := 22.0;     (* Oil Sump Low-Low Pre-Lube Interlock Floor [deg C] *)
    rAlarmDeadband_OilTemp_degC       : REAL := 2.5;      (* Oil Sump Temperature Hysteresis [deg C] *)

    rAlarmTrip_NH3_Critical_ppm       : REAL := 300.0;    (* Ammonia Toxic Gas Critical Scrubber Interlock [ppm] *)
    rAlarmTrip_NH3_Warning_ppm        : REAL := 50.0;     (* Ammonia OSHA Machinery Room High Warning [ppm] *)
    rAlarmTrip_NH3_Alert_ppm          : REAL := 25.0;     (* Ammonia Minor Leak Detection Alert [ppm] *)
    rAlarmDeadband_NH3_ppm            : REAL := 5.0;      (* Ammonia Sensor Alarm Hysteresis Deadband [ppm] *)

    (* ISA-18.2 First-Out Alarm Latch Register *)
    dwFirstOut_Alarm                  : DWORD := 16#00000000; (* Bit Position of First Tripped Condition *)
    bFirstOutLatched                  : BOOL := FALSE;    (* First-Out Alarm Event Captured Flag *)

    (* Loop Indices & Intermediate Calculation Working Storage *)
    idxRow                            : INT := 1;
    idxCol                            : INT := 1;
    idxIter                           : INT := 1;
    rTempSum                          : REAL := 0.0;
    rTempSum2                         : REAL := 0.0;
    rGradStep                         : REAL := 0.0;
    rDeltaU_Clamped                   : REAL := 0.0;
    rSlewLimit_dt                     : REAL := 0.0;
    rCondenserApproachError           : REAL := 0.0;
    rEconomizerSuperheatError         : REAL := 0.0;
    rTargetFloatingCondTemp           : REAL := 0.0;
    rComputedWetBulbApproach          : REAL := 0.0;
    rSlideValveDemandTotal            : REAL := 0.0;
    rCompressorNetPower_kW            : REAL := 0.0;
    rRefrigerationTonnage_TR          : REAL := 0.0;
END_VAR
"""
