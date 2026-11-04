# -*- coding: utf-8 -*-
"""
Part 2: Internal Variable Declarations (VAR ... END_VAR)
for FB_Chemicals_Hydrocracker_TrickleBed_HydrogenQuench
"""

def get_var_block():
    return """VAR
    (* ======================================================================================
     * 1.0 DISCRETE STATE-SPACE CYBER-PHYSICAL PLANT MATRICES & VECTORS (Ts = 0.020 s)
     * State Vector x[k] (8x1):
     *   x[1] = T_bed1  : Bed 1 Catalyst Zone Weighted Temperature [deg C] (Nominal 395.0)
     *   x[2] = T_bed2  : Bed 2 Catalyst Zone Weighted Temperature [deg C] (Nominal 405.0)
     *   x[3] = T_bed3  : Bed 3 Catalyst Zone Weighted Temperature [deg C] (Nominal 415.0)
     *   x[4] = T_bed4  : Bed 4 Catalyst Zone Weighted Temperature [deg C] (Nominal 420.0)
     *   x[5] = M_quench: Total Injected Cold Hydrogen Quench Mass Flow [kg/h] (Nominal 12500.0)
     *   x[6] = DP_rx   : Reactor Overall Hydraulic Differential Pressure [bar] (Nominal 4.80)
     *   x[7] = L_sep   : Cold High-Pressure Separator Liquid Hydrocarbon Level [%] (Nominal 55.0)
     *   x[8] = C_H2S   : Amine Absorber Overhead Acid Gas Concentration [ppm] (Nominal 12.0)
     *
     * Input Control Vector u[k] (6x1):
     *   u[1] = V_q1    : Quench Injection Valve Bed 1-2 Interbed Split [%] (0.0 .. 100.0)
     *   u[2] = V_q2    : Quench Injection Valve Bed 2-3 Interbed Split [%] (0.0 .. 100.0)
     *   u[3] = V_q3    : Quench Injection Valve Bed 3-4 Interbed Split [%] (0.0 .. 100.0)
     *   u[4] = Q_furn  : Combined Feed Charge Heater Fired Duty [%] (0.0 .. 100.0)
     *   u[5] = V_let   : HP Cold Separator Liquid Level Letdown Valve [%] (0.0 .. 100.0)
     *   u[6] = F_amine : Lean MDEA Scrubber Circulation Flow Command [%] (0.0 .. 100.0)
     * ====================================================================================== *)
    matA                            : ARRAY[1..8, 1..8] OF REAL; (* Discrete State Transition Matrix *)
    matB                            : ARRAY[1..8, 1..6] OF REAL; (* Discrete Control Input Coupling Matrix *)
    matC                            : ARRAY[1..8, 1..8] OF REAL; (* Measurement Observation Matrix *)
    matD                            : ARRAY[1..8, 1..6] OF REAL; (* Direct Feedthrough Disturbance Matrix *)

    x_state                         : ARRAY[1..8] OF REAL;       (* Filtered Current State Vector x[k] *)
    x_prev                          : ARRAY[1..8] OF REAL;       (* Delayed Previous State Vector x[k-1] *)
    x_pred                          : ARRAY[1..8] OF REAL;       (* One-Step Ahead State Prediction x[k+1|k] *)
    y_meas                          : ARRAY[1..8] OF REAL;       (* Measured Process Output Vector from TMR Voting *)
    y_est                           : ARRAY[1..8] OF REAL;       (* Model Estimated Output Vector *)
    x_err                           : ARRAY[1..8] OF REAL;       (* Innovation / Tracking Error Vector *)
    u_ctrl                          : ARRAY[1..6] OF REAL;       (* Active Control Action Vector u[k] *)
    u_prev                          : ARRAY[1..6] OF REAL;       (* Previous Control Action Vector u[k-1] *)
    u_delta                         : ARRAY[1..6] OF REAL;       (* Control Rate of Change du[k] = u[k] - u[k-1] *)
    rKalmanGain                     : ARRAY[1..8] OF REAL;       (* Luenberger / Diagonal Kalman Filter Observer Gains *)

    (* Model Predictive Control (MPC) Receding-Horizon Optimization Matrices *)
    matQ                            : ARRAY[1..8, 1..8] OF REAL; (* State Deviation Quadratic Weight Matrix Q *)
    matR                            : ARRAY[1..6, 1..6] OF REAL; (* Actuator Effort / Slew Quadratic Penalty Matrix R *)
    matP                            : ARRAY[1..8, 1..8] OF REAL; (* Terminal Riccati State Cost Penalty Matrix P *)
    rMpcGradient                    : ARRAY[1..6] OF REAL;       (* Unconstrained Gradient Vector dJ/du *)
    rMpcStepSize                    : REAL;                      (* Projected Gradient Descent Learning Rate Alpha *)
    iMpcIter                        : INT;                       (* Active Optimization Iteration Index *)

    (* ======================================================================================
     * 2.0 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING STRUCTURES (8 GROUPS)
     * ====================================================================================== *)
    (* TMR Group 1: Bed 1 Core Temperature Multipoint Thermocouples [deg C] *)
    rTMR1_DiffAB                    : REAL; (* Absolute Discrepancy |TE101A - TE101B| [deg C] *)
    rTMR1_DiffBC                    : REAL; (* Absolute Discrepancy |TE101B - TE101C| [deg C] *)
    rTMR1_DiffCA                    : REAL; (* Absolute Discrepancy |TE101C - TE101A| [deg C] *)
    tTMR1_TimerA                    : REAL; (* Sensor A Persistent Discrepancy Accumulator [s] *)
    tTMR1_TimerB                    : REAL; (* Sensor B Persistent Discrepancy Accumulator [s] *)
    tTMR1_TimerC                    : REAL; (* Sensor C Persistent Discrepancy Accumulator [s] *)
    bTMR1_FaultA                    : BOOL; (* Sensor Channel A Latched Discrepancy Fault *)
    bTMR1_FaultB                    : BOOL; (* Sensor Channel B Latched Discrepancy Fault *)
    bTMR1_FaultC                    : BOOL; (* Sensor Channel C Latched Discrepancy Fault *)
    rTMR1_VotedVal                  : REAL; (* 2oo3 Synthesized Median Core Temperature Bed 1 [deg C] *)
    iTMR1_HealthGrade               : INT;  (* 3=Triple Healthy, 2=Dual Redundant, 1=Single Degraded, 0=Critical Fail *)

    (* TMR Group 2: Bed 2 Core Temperature Multipoint Thermocouples [deg C] *)
    rTMR2_DiffAB                    : REAL; (* Absolute Discrepancy |TE102A - TE102B| [deg C] *)
    rTMR2_DiffBC                    : REAL; (* Absolute Discrepancy |TE102B - TE102C| [deg C] *)
    rTMR2_DiffCA                    : REAL; (* Absolute Discrepancy |TE102C - TE102A| [deg C] *)
    tTMR2_TimerA                    : REAL; (* Sensor A Persistent Discrepancy Accumulator [s] *)
    tTMR2_TimerB                    : REAL; (* Sensor B Persistent Discrepancy Accumulator [s] *)
    tTMR2_TimerC                    : REAL; (* Sensor C Persistent Discrepancy Accumulator [s] *)
    bTMR2_FaultA                    : BOOL; (* Sensor Channel A Latched Discrepancy Fault *)
    bTMR2_FaultB                    : BOOL; (* Sensor Channel B Latched Discrepancy Fault *)
    bTMR2_FaultC                    : BOOL; (* Sensor Channel C Latched Discrepancy Fault *)
    rTMR2_VotedVal                  : REAL; (* 2oo3 Synthesized Median Core Temperature Bed 2 [deg C] *)
    iTMR2_HealthGrade               : INT;

    (* TMR Group 3: Bed 3 Core Temperature Multipoint Thermocouples [deg C] *)
    rTMR3_DiffAB                    : REAL; (* Absolute Discrepancy |TE103A - TE103B| [deg C] *)
    rTMR3_DiffBC                    : REAL; (* Absolute Discrepancy |TE103B - TE103C| [deg C] *)
    rTMR3_DiffCA                    : REAL; (* Absolute Discrepancy |TE103C - TE103A| [deg C] *)
    tTMR3_TimerA                    : REAL; (* Sensor A Persistent Discrepancy Accumulator [s] *)
    tTMR3_TimerB                    : REAL; (* Sensor B Persistent Discrepancy Accumulator [s] *)
    tTMR3_TimerC                    : REAL; (* Sensor C Persistent Discrepancy Accumulator [s] *)
    bTMR3_FaultA                    : BOOL; (* Sensor Channel A Latched Discrepancy Fault *)
    bTMR3_FaultB                    : BOOL; (* Sensor Channel B Latched Discrepancy Fault *)
    bTMR3_FaultC                    : BOOL; (* Sensor Channel C Latched Discrepancy Fault *)
    rTMR3_VotedVal                  : REAL; (* 2oo3 Synthesized Median Core Temperature Bed 3 [deg C] *)
    iTMR3_HealthGrade               : INT;

    (* TMR Group 4: Bed 4 Core Temperature Multipoint Thermocouples [deg C] *)
    rTMR4_DiffAB                    : REAL; (* Absolute Discrepancy |TE104A - TE104B| [deg C] *)
    rTMR4_DiffBC                    : REAL; (* Absolute Discrepancy |TE104B - TE104C| [deg C] *)
    rTMR4_DiffCA                    : REAL; (* Absolute Discrepancy |TE104C - TE104A| [deg C] *)
    tTMR4_TimerA                    : REAL; (* Sensor A Persistent Discrepancy Accumulator [s] *)
    tTMR4_TimerB                    : REAL; (* Sensor B Persistent Discrepancy Accumulator [s] *)
    tTMR4_TimerC                    : REAL; (* Sensor C Persistent Discrepancy Accumulator [s] *)
    bTMR4_FaultA                    : BOOL; (* Sensor Channel A Latched Discrepancy Fault *)
    bTMR4_FaultB                    : BOOL; (* Sensor Channel B Latched Discrepancy Fault *)
    bTMR4_FaultC                    : BOOL; (* Sensor Channel C Latched Discrepancy Fault *)
    rTMR4_VotedVal                  : REAL; (* 2oo3 Synthesized Median Core Temperature Bed 4 [deg C] *)
    iTMR4_HealthGrade               : INT;

    (* TMR Group 5: High-Pressure Separator Nuclear Level Transmitters [%] *)
    rTMR5_DiffAB                    : REAL; (* Absolute Discrepancy |LT201A - LT201B| [%] *)
    rTMR5_DiffBC                    : REAL; (* Absolute Discrepancy |LT201B - LT201C| [%] *)
    rTMR5_DiffCA                    : REAL; (* Absolute Discrepancy |LT201C - LT201A| [%] *)
    tTMR5_TimerA                    : REAL; (* Sensor A Discrepancy Accumulator [s] *)
    tTMR5_TimerB                    : REAL; (* Sensor B Discrepancy Accumulator [s] *)
    tTMR5_TimerC                    : REAL; (* Sensor C Discrepancy Accumulator [s] *)
    bTMR5_FaultA                    : BOOL; (* Sensor Channel A Fault *)
    bTMR5_FaultB                    : BOOL; (* Sensor Channel B Fault *)
    bTMR5_FaultC                    : BOOL; (* Sensor Channel C Fault *)
    rTMR5_VotedVal                  : REAL; (* 2oo3 Voted HP Separator Liquid Level [%] *)
    iTMR5_HealthGrade               : INT;

    (* TMR Group 6: Reactor Overall Differential Pressure Transmitters [bar] *)
    rTMR6_DiffAB                    : REAL; (* Absolute Discrepancy |DPT301A - DPT301B| [bar] *)
    rTMR6_DiffBC                    : REAL; (* Absolute Discrepancy |DPT301B - DPT301C| [bar] *)
    rTMR6_DiffCA                    : REAL; (* Absolute Discrepancy |DPT301C - DPT301A| [bar] *)
    tTMR6_TimerA                    : REAL; (* Sensor A Discrepancy Accumulator [s] *)
    tTMR6_TimerB                    : REAL; (* Sensor B Discrepancy Accumulator [s] *)
    tTMR6_TimerC                    : REAL; (* Sensor C Discrepancy Accumulator [s] *)
    bTMR6_FaultA                    : BOOL; (* Sensor Channel A Fault *)
    bTMR6_FaultB                    : BOOL; (* Sensor Channel B Fault *)
    bTMR6_FaultC                    : BOOL; (* Sensor Channel C Fault *)
    rTMR6_VotedVal                  : REAL; (* 2oo3 Voted Total Reactor Delta-P [bar] *)
    iTMR6_HealthGrade               : INT;

    (* TMR Group 7: Reactor Inlet Head Pressure Transmitters [bar] *)
    rTMR7_DiffAB                    : REAL; (* Absolute Discrepancy |PT401A - PT401B| [bar] *)
    rTMR7_DiffBC                    : REAL; (* Absolute Discrepancy |PT401B - PT401C| [bar] *)
    rTMR7_DiffCA                    : REAL; (* Absolute Discrepancy |PT401C - PT401A| [bar] *)
    tTMR7_TimerA                    : REAL; (* Sensor A Discrepancy Accumulator [s] *)
    tTMR7_TimerB                    : REAL; (* Sensor B Discrepancy Accumulator [s] *)
    tTMR7_TimerC                    : REAL; (* Sensor C Discrepancy Accumulator [s] *)
    bTMR7_FaultA                    : BOOL; (* Sensor Channel A Fault *)
    bTMR7_FaultB                    : BOOL; (* Sensor Channel B Fault *)
    bTMR7_FaultC                    : BOOL; (* Sensor Channel C Fault *)
    rTMR7_VotedVal                  : REAL; (* 2oo3 Voted Reactor Inlet Pressure [bar] *)
    iTMR7_HealthGrade               : INT;

    (* TMR Group 8: Amine Absorber Overhead Acid Gas H2S Analyzers [ppm] *)
    rTMR8_DiffAB                    : REAL; (* Absolute Discrepancy |AT501A - AT501B| [ppm] *)
    rTMR8_DiffBC                    : REAL; (* Absolute Discrepancy |AT501B - AT501C| [ppm] *)
    rTMR8_DiffCA                    : REAL; (* Absolute Discrepancy |AT501C - AT501A| [ppm] *)
    tTMR8_TimerA                    : REAL; (* Sensor A Discrepancy Accumulator [s] *)
    tTMR8_TimerB                    : REAL; (* Sensor B Discrepancy Accumulator [s] *)
    tTMR8_TimerC                    : REAL; (* Sensor C Discrepancy Accumulator [s] *)
    bTMR8_FaultA                    : BOOL; (* Sensor Channel A Fault *)
    bTMR8_FaultB                    : BOOL; (* Sensor Channel B Fault *)
    bTMR8_FaultC                    : BOOL; (* Sensor Channel C Fault *)
    rTMR8_VotedVal                  : REAL; (* 2oo3 Voted Overhead H2S Concentration [ppm] *)
    iTMR8_HealthGrade               : INT;

    (* ======================================================================================
     * 3.0 CYBER-PHYSICAL REACTION KINETIC, THERMODYNAMIC & HYDRODYNAMIC OBSERVERS
     * ====================================================================================== *)
    (* Temperature Derivatives for Dynamic Runaway Detection [deg C/min] *)
    rTempBed1_Hist                  : ARRAY[1..5] OF REAL;       (* Historical Temperature Rolling Buffer Bed 1 *)
    rTempBed2_Hist                  : ARRAY[1..5] OF REAL;       (* Historical Temperature Rolling Buffer Bed 2 *)
    rTempBed3_Hist                  : ARRAY[1..5] OF REAL;       (* Historical Temperature Rolling Buffer Bed 3 *)
    rTempBed4_Hist                  : ARRAY[1..5] OF REAL;       (* Historical Temperature Rolling Buffer Bed 4 *)
    rPressInlet_Hist                : ARRAY[1..5] OF REAL;       (* Historical Pressure Buffer for Blowdown Tracking *)
    rTime_RollingDelta_s            : REAL;                      (* Accumulated Rolling Window Time Delta [s] *)

    (* Catalyst Hydrodynamics & Ergun Two-Phase Frictional Drop *)
    rCatalystBed_VoidFraction       : REAL; (* Packed Bed Bed Interparticle Porosity (Nominal 0.38) *)
    rCatalyst_ParticleDia_m         : REAL; (* Equivalent Extrudate Pellet Diameter [m] (Nominal 0.0016 m = 1.6 mm) *)
    rGas_SuperficialVelocity_ms     : REAL; (* High-Pressure Hydrogen Gas Superficial Linear Velocity [m/s] *)
    rLiquid_SuperficialVelocity_ms  : REAL; (* Hydrocarbon Oil Liquid Superficial Linear Velocity [m/s] *)
    rErgun_GasFrictionalDP_bar      : REAL; (* Single-Phase Modified Ergun Gas Differential Pressure [bar] *)
    rTwoPhase_LockhartMartinelli_X  : REAL; (* Modified Lockhart-Martinelli Two-Phase Hydrodynamic Parameter *)
    rTwoPhase_Multiplier           : REAL; (* Two-Phase Pressure Drop Frictional Friction Factor Multiplier *)

    (* Chemical Heat Release, Hydrogen Consumption & Kinetic Conversion *)
    rFeedMassFlow_kgs               : REAL; (* Hydrocarbon Liquid Feed Mass Flow Rate [kg/s] *)
    rSpecificHeat_Oil_kJkgK         : REAL; (* Heavy Gas Oil Liquid Specific Heat Capacity [kJ/(kg*K)] (Nominal 2.45) *)
    rDeltaT_Bed1                    : REAL; (* Temperature Rise across Bed 1 [deg C] (T_out1 - T_in1) *)
    rDeltaT_Bed2                    : REAL; (* Temperature Rise across Bed 2 [deg C] (T_out2 - T_in2) *)
    rDeltaT_Bed3                    : REAL; (* Temperature Rise across Bed 3 [deg C] (T_out3 - T_in3) *)
    rDeltaT_Bed4                    : REAL; (* Temperature Rise across Bed 4 [deg C] (T_out4 - T_in4) *)
    rTotalReactor_DeltaT            : REAL; (* Cumulative Temperature Rise across entire Reactor [deg C] *)
    rSpecificHydrogenConsumption    : REAL; (* Calculated Chemical Hydrogen Uptake [Nm3 H2 / m3 Feed] *)
    rDMDS_Decomposition_Conversion  : REAL; (* Catalyst Pre-Sulfiding DMDS Conversion to Active H2S [%] *)

    (* Amine Absorption Mass Transfer Equilibrium *)
    rAmine_LiquidGas_Ratio          : REAL; (* MDEA Solvent to Sour Gas Volumetric Ratio [m3 amine / 1000 Nm3 gas] *)
    rAmine_RichLoading_mol_mol      : REAL; (* Acid Gas Rich Loading in Solvent [mol H2S / mol MDEA] *)
    rAmine_LeanLoading_mol_mol      : REAL; (* Clean Lean Solution Acid Gas Loading [mol H2S / mol MDEA] *)

    (* Atmospheric Fractionation Column Reflux & Heat Integration *)
    rFractionator_RefluxRatio       : REAL; (* Top Internal Dynamic Reflux Ratio L/D (Nominal 1.85 .. 2.40) *)
    rFractionator_ReboilerDuty_MW   : REAL; (* Bottom Fired Reboiler Heat Duty [MW thermal] *)
    rOverhead_CondenserDuty_MW      : REAL; (* Overhead Fin-Fan Air Cooler Heat Removal [MW thermal] *)

    (* ======================================================================================
     * 4.0 12-STAGE DETERMINISTIC OPERATIONAL FINITE STATE MACHINE (FSM)
     * ====================================================================================== *)
    iState                          : INT;  (* Active FSM State Code [0 .. 11] *)
    iPrevState                      : INT;  (* Previous Step FSM State Code *)
    tStateTimer_s                   : REAL; (* State Residence Time Accumulator [s] *)
    tStageTotalTimer_s              : REAL; (* Master Plant Operation Timer Accumulator [s] *)
    bStateFirstScan                 : BOOL; (* First Scan Entry Permissive Flag *)
    bStateTransitionPermit          : BOOL; (* Interlock Permissive Flag to Index Next State *)
    iSulfidingStage                 : INT;  (* Catalyst Sulfiding Plateau Index: 1=Low Temp 230C, 2=High Temp 330C *)
    tSulfidingHoldTimer_s           : REAL; (* Dwell Timer at Sulfiding Temperature Plateaus [s] *)
    rDepressurizationStartPress_bar : REAL; (* Recorded Inlet Pressure at Initiation of Emergency Depressurization [bar] *)

    (* ======================================================================================
     * 5.0 ISA-18.2 MULTI-TIERED ALARM ENGINE & RUNAWAY TRIP THRESHOLDS
     * ====================================================================================== *)
    (* Temperature Trip Points with Hysteresis Deadbands *)
    rBedTemp_Runaway_Rate_Trip      : REAL; (* 15.0 deg C/min: SIL-3 Rate-of-Change Runaway Emergency Depressurization *)
    rBedTemp_HH_Trip                : REAL; (* 435.0 deg C: SIL-3 Hotspot High-High Overheat Trip *)
    rBedTemp_H_Trip                 : REAL; (* 425.0 deg C: Process Alarm High Warning *)
    rBedTemp_L_Trip                 : REAL; (* 360.0 deg C: Low Reaction Temperature / Incomplete Cracking *)
    rBedTemp_LL_Trip                : REAL; (* 320.0 deg C: Critical Reaction Extinction *)
    rBedTemp_Deadband               : REAL; (*   2.0 deg C: Temperature Deadband Hysteresis *)

    (* Pressure Trip Points with Hysteresis Deadbands *)
    rReactorPress_HH_Trip           : REAL; (* 198.0 bar: Safety Depressurization Slam High-High *)
    rReactorPress_H_Trip            : REAL; (* 190.0 bar: Pressure Alarm High Warning *)
    rReactorPress_L_Trip            : REAL; (* 160.0 bar: Low Operating Pressure Warning *)
    rReactorPress_LL_Trip           : REAL; (* 130.0 bar: Critical Loss of Reaction Containment *)
    rReactorPress_Deadband          : REAL; (*   1.5 bar: Pressure Hysteresis Deadband *)

    (* Differential Pressure (Fouling / Maldistribution) Trip Points *)
    rReactorDP_HH_Trip              : REAL; (*  12.0 bar: Catalyst Bed Crushing / Severe Maldistribution Trip *)
    rReactorDP_H_Trip               : REAL; (*   8.5 bar: High Differential Pressure Warning *)
    rReactorDP_Deadband             : REAL; (*   0.5 bar: Differential Pressure Deadband *)

    (* High-Pressure Separator Level Trip Points *)
    rHPSepLevel_HH_Trip             : REAL; (*  85.0 %: Gas Carry-Over / Level High-High Overfill Trip *)
    rHPSepLevel_H_Trip              : REAL; (*  72.0 %: Level High Warning *)
    rHPSepLevel_L_Trip              : REAL; (*  30.0 %: Level Low Warning *)
    rHPSepLevel_LL_Trip             : REAL; (*  15.0 %: Liquid Blowby / Depressurization Slam Low-Low *)
    rHPSepLevel_Deadband            : REAL; (*   2.5 %: Level Deadband *)

    (* Sour Gas Amine Column Overhead H2S Trip Points *)
    rAmineH2S_HH_Trip               : REAL; (* 150.0 ppm: Severe Catalyst Poisoning Risk to Recycle Compressor *)
    rAmineH2S_H_Trip                : REAL; (*  50.0 ppm: High H2S Recycle Gas Warning *)
    rAmineH2S_Deadband              : REAL; (*   5.0 ppm: H2S Deadband *)

    (* Alarm Debounce Timers [s] *)
    tAlarmTimer_BedTempHH           : REAL;
    tAlarmTimer_BedTempLL           : REAL;
    tAlarmTimer_PressHH             : REAL;
    tAlarmTimer_PressLL             : REAL;
    tAlarmTimer_DPHH                : REAL;
    tAlarmTimer_SepLvlHH            : REAL;
    tAlarmTimer_SepLvlLL            : REAL;
    tAlarmTimer_AmineH2SHH          : REAL;
    tAlarmTimer_RunawayTrigger      : REAL;

    (* ======================================================================================
     * 6.0 ACTUATOR FIRST-ORDER FILTERS, SLEW LIMITERS & SCRATCHPAD REGISTERS
     * ====================================================================================== *)
    rQuench1_Filtered               : REAL; (* First-Order Lag Filtered Quench 1 Valve Command [%] *)
    rQuench2_Filtered               : REAL; (* First-Order Lag Filtered Quench 2 Valve Command [%] *)
    rQuench3_Filtered               : REAL; (* First-Order Lag Filtered Quench 3 Valve Command [%] *)
    rFurnace_Filtered               : REAL; (* Slew-Rate Limited Fired Heater Command [%] *)
    rLetdownA_Filtered              : REAL; (* Anti-Cavitation Filtered HP Separator Letdown A [%] *)
    rLetdownB_Filtered              : REAL; (* Anti-Cavitation Filtered HP Separator Letdown B [%] *)
    rAminePump_Filtered             : REAL; (* Ramp-Limited Lean Amine Pump VFD Speed [%] *)
    rReflux_Filtered                : REAL; (* Fractionator Dynamic Reflux Valve Position [%] *)
    rReboiler_Filtered              : REAL; (* Reboiler Fired Duty Actuator Command [%] *)

    (* General Iteration Indices & Math Scratchpad Scalars *)
    iIdxI                           : INT;  (* Row Matrix Loop Counter *)
    iIdxJ                           : INT;  (* Column Matrix Loop Counter *)
    iIdxK                           : INT;  (* Vector Loop Counter *)
    rMathSum                        : REAL; (* Inner Product / Matrix Vector Multiplication Accumulator *)
    rMathMin                        : REAL; (* Minimum Comparator Scratchpad *)
    rMathMax                        : REAL; (* Maximum Comparator Scratchpad *)
    rTempMedian                     : REAL; (* Three-Value Sorting Scratchpad *)
    bColdInitDone                   : BOOL; (* Master First-Scan Initialization Latch *)
END_VAR
"""
