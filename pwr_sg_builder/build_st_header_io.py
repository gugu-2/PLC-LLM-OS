# build_st_header_io.py
# Section 1: Header and I/O Variable Declarations for FB_Nuclear_PWR_SteamGenerator_NarrowRangeLevel_ShrinkSwell

def get_header_and_io():
    return """FUNCTION_BLOCK FB_Nuclear_PWR_SteamGenerator_NarrowRangeLevel_ShrinkSwell
(* =====================================================================================================================
 * LUMINA CYBER-PHYSICAL AUTOMATION ENGINE - SYNTHETIC DATASET V7 MAX-PERSONA
 * COMMERCIAL INDUSTRIAL SECTOR : Nuclear Power Generation & Safety-Critical Thermo-Hydraulics
 * SYSTEM                       : Westinghouse 4-Loop / Framatome N4 Class 1300 MWe Pressurized Water Reactor (PWR)
 * SUBSYSTEM                    : Steam Generator (SG) Narrow-Range Water Level Control & Dynamic Shrink/Swell Mitigation
 * COGNIZANT STANDARDS          : IEC 61513 Nuclear Safety I&C / IEEE 603 Safety Systems / IEEE 7-4.3.2 Digital Computers /
 *                                IEC 61131-3 3rd Ed. / ISA-18.2 Process Alarm Systems / NUREG-0800 Standard Review Plan
 * SAFETY INTEGRITY LEVEL       : Nuclear Safety Class 1E / IEC 61508 SIL 3 Equivalent
 * SCAN CYCLE EXECUTION PERIOD  : Ts = 25.0 ms (40.0 Hz Deterministic Hard Real-Time Periodic Task)
 * ARCHITECTURE OVERVIEW        :
 *   1) 2oo3 Triple Modular Redundancy (TMR) voting with continuous discrepancy accumulation timers (500 ms fault window)
 *      and bumpless 3-to-2-to-1-to-0 degradation logic for 5 safety-critical process measurement triplets.
 *   2) First-Principles 8th-Order Thermo-Hydraulic State-Space Model capturing Irving-Miossec reverse response (shrink/swell),
 *      bulk boiling riser void fraction, downcomer natural circulation momentum, primary U-tube heat transfer, and drum pressure.
 *   3) Discrete-Time Kalman Filter State Observer (L-matrix 8x5) for full state vector reconstruction under high sensor noise.
 *   4) Receding-Horizon Model Predictive Control (MPC) with 5-step prediction horizon (Np=5) and 5 unrolled iterations of
 *      Projected Gradient Descent (PGD) with state/control constraints and actuator slew rate enforcement.
 *   5) Dynamic Inverse Response Feedforward Decoupling Compensator cancelling non-minimum phase zero dynamics.
 *   6) 14-Stage Deterministic Nuclear Island Finite State Machine (FSM) governing Cold Shutdown through Full Power to SCRAM.
 *   7) ISA-18.2 Class 1E Multi-Tiered Process Alarm Engine with bit-packed DWORD telemetry and First-Out forensic latching.
 * ===================================================================================================================== *)

VAR_INPUT
    (* =================================================================================================================
     * SECTION 1.1: 2oo3 TRIPLE MODULAR REDUNDANT PROCESS INSTRUMENTATION (5 TRIPLETS = 15 TRANSMITTERS)
     * ================================================================================================================= *)
    (* Steam Generator Narrow-Range Level Transmitters (LT-101A/B/C) [mm], Calibrated Range: 0.0 mm to 4000.0 mm *)
    rLevel_NR_Transmitter_A         : REAL; (* Narrow Range Level Differential Pressure Channel A [mm] *)
    rLevel_NR_Transmitter_B         : REAL; (* Narrow Range Level Differential Pressure Channel B [mm] *)
    rLevel_NR_Transmitter_C         : REAL; (* Narrow Range Level Differential Pressure Channel C [mm] *)

    (* Steam Generator Wide-Range Level Transmitters (LT-102A/B/C) [mm], Calibrated Range: 0.0 mm to 15000.0 mm *)
    rLevel_WR_Transmitter_A         : REAL; (* Wide Range Level Transmitter Channel A [mm] *)
    rLevel_WR_Transmitter_B         : REAL; (* Wide Range Level Transmitter Channel B [mm] *)
    rLevel_WR_Transmitter_C         : REAL; (* Wide Range Level Transmitter Channel C [mm] *)

    (* Main Steam Drum Pressure Transmitters (PT-201A/B/C) [bar], Calibrated Range: 0.0 bar to 100.0 bar *)
    rPress_SteamDrum_Transmitter_A  : REAL; (* Steam Drum Saturation Pressure Channel A [bar] *)
    rPress_SteamDrum_Transmitter_B  : REAL; (* Steam Drum Saturation Pressure Channel B [bar] *)
    rPress_SteamDrum_Transmitter_C  : REAL; (* Steam Drum Saturation Pressure Channel C [bar] *)

    (* Main Steam Header Mass Flow Rate Transmitters (FT-301A/B/C) [t/h], Calibrated Range: 0.0 t/h to 2500.0 t/h *)
    rFlow_MainSteam_Transmitter_A   : REAL; (* Main Steam Header Flow Rate Channel A [t/h] *)
    rFlow_MainSteam_Transmitter_B   : REAL; (* Main Steam Header Flow Rate Channel B [t/h] *)
    rFlow_MainSteam_Transmitter_C   : REAL; (* Main Steam Header Flow Rate Channel C [t/h] *)

    (* Main Feedwater Mass Flow Rate Transmitters (FT-401A/B/C) [t/h], Calibrated Range: 0.0 t/h to 2500.0 t/h *)
    rFlow_Feedwater_Transmitter_A   : REAL; (* Main Feedwater Flow Rate Channel A [t/h] *)
    rFlow_Feedwater_Transmitter_B   : REAL; (* Main Feedwater Flow Rate Channel B [t/h] *)
    rFlow_Feedwater_Transmitter_C   : REAL; (* Main Feedwater Flow Rate Channel C [t/h] *)

    (* =================================================================================================================
     * SECTION 1.2: PRIMARY REACTOR COOLANT SYSTEM (RCS) & THERMAL-HYDRAULIC SENSORS
     * ================================================================================================================= *)
    rTemp_HotLeg_Primary            : REAL; (* Primary Coolant Core Outlet Hot Leg Temperature [deg C] *)
    rTemp_ColdLeg_Primary           : REAL; (* Primary Coolant SG Outlet Cold Leg Temperature [deg C] *)
    rPress_Primary_RCS              : REAL; (* Primary Coolant System Pressurizer Operating Pressure [bar] *)
    rFlow_Primary_Coolant_Loop      : REAL; (* Primary Reactor Coolant Loop Volumetric Flow Rate [m3/h] *)
    rReactor_Thermal_Power_Pct      : REAL; (* Nuclear Ex-Core Calibrated Reactor Thermal Power [% RTP] *)

    (* =================================================================================================================
     * SECTION 1.3: RADIATION MONITORING & SECONDARY INTEGRITY SENSORS
     * ================================================================================================================= *)
    rRad_N16_SteamLine_ChA          : REAL; (* N-16 Secondary Main Steam Gamma Activity Channel A [Bq/m3] *)
    rRad_N16_SteamLine_ChB          : REAL; (* N-16 Secondary Main Steam Gamma Activity Channel B [Bq/m3] *)
    rRad_Blowdown_Liquid            : REAL; (* SG Continuous Blowdown Liquid Scintillation Activity [Bq/m3] *)
    rTemp_Feedwater_Inlet           : REAL; (* Economizer Feedwater Inlet Temperature [deg C] *)

    (* =================================================================================================================
     * SECTION 1.4: CLASS 1E DISCRETE SAFETY & INTERLOCK SIGNALS
     * ================================================================================================================= *)
    bDigital_RPS_Reactor_Scram      : BOOL; (* Class 1E Reactor Protection System Hardwired SCRAM Command Active *)
    bDigital_Turbine_Trip           : BOOL; (* Main Turbine Stop Valve Rapid Closure Trip Command Active *)
    bDigital_MSIV_Closed_Limit      : BOOL; (* Main Steam Isolation Valve (MSIV) Fully Closed Limit Switch *)
    bDigital_SIAS_Active            : BOOL; (* Safety Injection Actuation Signal Active from Containment/PZR *)
    bDigital_AFW_Manual_Initiate    : BOOL; (* Auxiliary Feedwater Manual Emergency Initiation Pushbutton *)
    bDigital_Grid_Load_Drop_Alert   : BOOL; (* Fast Turbine Runback Demand from Grid Operator Dispatch *)

    (* =================================================================================================================
     * SECTION 1.5: OPERATOR DEMANDS, SETPOINTS & SUPERVISORY INTERFACES
     * ================================================================================================================= *)
    rOperator_Level_Setpoint_NR     : REAL; (* Operator Narrow-Range Water Level Target Setpoint [mm] *)
    rOperator_MFRV_Manual_Demand    : REAL; (* Main Feedwater Regulating Valve Manual Trim Demand [%] *)
    rOperator_Bypass_Manual_Demand  : REAL; (* Low-Power Feedwater Bypass Valve Manual Trim Demand [%] *)
    bSelect_Manual_Control_Mode     : BOOL; (* Hand/Auto Station Transfer to Manual Actuator Override *)
    bAcknowledge_Alarms             : BOOL; (* ISA-18.2 Operator Alarm Acknowledge Pushbutton *)
    bReset_Trip_Interlocks          : BOOL; (* Safety Channel Post-Trip Master Reset Interlock *)
    rTarget_Thermal_Ramp_Rate       : REAL; (* Target Power Slew Ramp Rate for Maneuvering [%/min] *)
END_VAR

VAR_OUTPUT
    (* =================================================================================================================
     * SECTION 2.1: FINAL ACTUATOR COMMANDS & VALVE POSITION DEMANDS
     * ================================================================================================================= *)
    rCommand_MFRV_Position          : REAL; (* Main Feedwater Regulating Valve (MFRV) Position Demand [%] *)
    rCommand_Bypass_Valve_Pos       : REAL; (* Low-Power Feedwater Bypass Regulating Valve Demand [%] *)
    rCommand_AFW_Motor_Pump_Speed   : REAL; (* Motor-Driven Auxiliary Feedwater Pump Speed Demand [%] *)
    rCommand_AFW_Turbine_Pump_Flow  : REAL; (* Turbine-Driven Auxiliary Feedwater Mass Flow Target [t/h] *)
    rCommand_Blowdown_Valve_Pos     : REAL; (* Continuous SG Bottom Blowdown Regulating Valve Demand [%] *)

    (* =================================================================================================================
     * SECTION 2.2: CLASS 1E REACTOR PROTECTION & EMERGENCY SAFETY ACTUATION SIGNALS
     * ================================================================================================================= *)
    bDemand_RPS_Reactor_Trip        : BOOL; (* Class 1E RPS Level High-High or Low-Low Trip Actuation Demand *)
    bDemand_Turbine_Runback         : BOOL; (* Turbine Governor Fast Runback Inhibit & Throttle Demand *)
    bDemand_MSIV_Fast_Closure       : BOOL; (* Main Steam Line Isolation Fast Closure Interlock Demand *)
    bDemand_MFRV_Isolation_P14      : BOOL; (* P-14 High-High Level Main Feedwater Isolation Fast Trip Signal *)
    bDemand_AFW_Motor_Pump_Start    : BOOL; (* Auxiliary Feedwater Motor-Driven Pump Train Auto-Start Command *)
    bDemand_AFW_Turbine_Pump_Start  : BOOL; (* Auxiliary Feedwater Turbine-Driven Pump Train Auto-Start Command *)

    (* =================================================================================================================
     * SECTION 2.3: 2oo3 VOTED PROCESS SIGNALS & DIAGNOSTIC VALIDATION STATUS
     * ================================================================================================================= *)
    rVoted_Level_NR                 : REAL; (* 2oo3 Synthesized Validated Narrow-Range Water Level [mm] *)
    rVoted_Level_WR                 : REAL; (* 2oo3 Synthesized Validated Wide-Range Water Level [mm] *)
    rVoted_Press_SteamDrum          : REAL; (* 2oo3 Synthesized Validated Main Steam Drum Pressure [bar] *)
    rVoted_Flow_MainSteam           : REAL; (* 2oo3 Synthesized Validated Main Steam Mass Flow Rate [t/h] *)
    rVoted_Flow_Feedwater           : REAL; (* 2oo3 Synthesized Validated Main Feedwater Mass Flow Rate [t/h] *)

    (* =================================================================================================================
     * SECTION 2.4: STATE-SPACE ESTIMATES, KALMAN INNOVATION & CYBER-PHYSICAL INTERMEDIATES
     * ================================================================================================================= *)
    rState_Est_Level_NR             : REAL; (* Kalman Reconstructed Narrow Range Level State x1 [mm] *)
    rState_Est_Downcomer_Flow       : REAL; (* Kalman Reconstructed Downcomer Recirculation Flow x2 [kg/s] *)
    rState_Est_Riser_Void_Fraction  : REAL; (* Kalman Reconstructed Boiling Riser Void Fraction x3 [ratio 0..1] *)
    rState_Est_Primary_Heat_MW      : REAL; (* Kalman Reconstructed Primary U-Tube Heat Transfer x4 [MW] *)
    rState_Est_Drum_Pressure        : REAL; (* Kalman Reconstructed Steam Drum Saturation Pressure x5 [bar] *)
    rState_Est_ColdLeg_Temp         : REAL; (* Kalman Reconstructed Primary Cold Leg Temperature x6 [deg C] *)
    rState_Est_FeedValve_Trim       : REAL; (* Kalman Reconstructed Feedwater Valve Trim State x7 [%] *)
    rState_Est_ShrinkSwell_Bias     : REAL; (* Non-Minimum Phase Dynamic Swell/Shrink Offset State x8 [mm] *)
    rDynamic_Feedforward_Bias       : REAL; (* Lead-Lag Feedforward Inverse Response Decoupling Term [mm] *)
    rMPC_Optimization_Cost_J        : REAL; (* Receding-Horizon Quadratic Performance Cost Metric [-] *)

    (* =================================================================================================================
     * SECTION 2.5: BIT-PACKED TELEMETRY WORDS & SYSTEM STATE WORDS
     * ================================================================================================================= *)
    dwStatusWord1                   : DWORD; (* System Operational State, FSM Step & Active Control Subsystems *)
    dwStatusWord2                   : DWORD; (* 2oo3 Sensor Triplets Health, Degradation Tiers & Maintenance Bypasses *)
    dwAlarmWord1                    : DWORD; (* ISA-18.2 Process Advisory, Pre-Trip Warnings & Limit Discrepancies *)
    dwAlarmWord2                    : DWORD; (* Class 1E Safety Actuation Latches, SCRAM Triggers & Trips *)
    dwFirstOutWord                  : DWORD; (* First-Out Root-Cause Trip Telemetry for Forensic Sequence-of-Events *)
    nActiveStateIndex               : INT;   (* Deterministic 14-Stage Nuclear State Machine Active Index (0..13) *)
    bExecution_Valid_Tick           : BOOL;  (* Cyclic Hard Real-Time Execution Integrity Watchdog Pulse *)
END_VAR
"""

if __name__ == "__main__":
    s = get_header_and_io()
    print("Header & IO length:", len(s))
