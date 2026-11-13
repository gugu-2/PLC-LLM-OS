# -*- coding: utf-8 -*-
"""
Module: retort_builder/mod_header_io.py
Declares Header, VAR_INPUT, and VAR_OUTPUT for FB_FoodBev_RetortAutoclave_SteamAirSterilization_Fo.
"""

def generate_header_io():
    return '''FUNCTION_BLOCK FB_FoodBev_RetortAutoclave_SteamAirSterilization_Fo
(* =====================================================================================================================
 * LUMINA CYBER-PHYSICAL AUTOMATION ENGINE - SYNTHETIC DATASET V7 MAX-PERSONA
 * COMMERCIAL INDUSTRIAL SECTOR : Commercial Food & Beverage Heavy Processing (Tier 1 Priority Sector)
 * SUBSYSTEM                    : Continuous Rotary Overpressure Retort Autoclave (LACF Low-Acid Canned Foods)
 * FUNCTION BLOCK               : FB_FoodBev_RetortAutoclave_SteamAirSterilization_Fo
 * DESIGN STANDARDS             : IEC 61131-3 3rd Ed., FDA 21 CFR Part 113, NFPA 86, ISA-18.2, ASME Sec VIII Div 1
 * CYBER-PHYSICAL RIGOR         : 8x8 State-Space Estimation, Receding-Horizon Decoupled MPC, 2oo3 TMR Sensor Voting,
 *                                Ball Process Formula Dynamic Catch-up, Deflection Counter-Pressure Protection,
 *                                14-Stage Deterministic Production FSM, Bit-Packed Status/Warning/Fault/FDA Words.
 * ===================================================================================================================== *)

VAR_INPUT
    (* ==================== 2oo3 TRIPLE MODULAR REDUNDANT SENSORS ==================== *)
    rTT_101A_VesselTemp_degC        : REAL; (* Retort Vessel Steam Temperature Sensor Channel A [deg C] *)
    rTT_101B_VesselTemp_degC        : REAL; (* Retort Vessel Steam Temperature Sensor Channel B [deg C] *)
    rTT_101C_VesselTemp_degC        : REAL; (* Retort Vessel Steam Temperature Sensor Channel C [deg C] *)

    rPT_201A_VesselPress_bar        : REAL; (* Retort Vessel Absolute Pressure Sensor Channel A [bar] *)
    rPT_201B_VesselPress_bar        : REAL; (* Retort Vessel Absolute Pressure Sensor Channel B [bar] *)
    rPT_201C_VesselPress_bar        : REAL; (* Retort Vessel Absolute Pressure Sensor Channel C [bar] *)

    rTT_301A_CanCoreTemp_degC       : REAL; (* Simulated/Telemetry Product Cold-Spot Core Temp Channel A [deg C] *)
    rTT_301B_CanCoreTemp_degC       : REAL; (* Simulated/Telemetry Product Cold-Spot Core Temp Channel B [deg C] *)
    rTT_301C_CanCoreTemp_degC       : REAL; (* Simulated/Telemetry Product Cold-Spot Core Temp Channel C [deg C] *)

    rLT_401A_SumpLevel_mm           : REAL; (* Vessel Condensate / Cooling Water Sump Level Channel A [mm] *)
    rLT_401B_SumpLevel_mm           : REAL; (* Vessel Condensate / Cooling Water Sump Level Channel B [mm] *)
    rLT_401C_SumpLevel_mm           : REAL; (* Vessel Condensate / Cooling Water Sump Level Channel C [mm] *)

    (* ==================== AUXILIARY PROCESS SENSORS & TRANSDUCERS ==================== *)
    rPT_001_SteamHeaderPress_bar    : REAL; (* Plant Culinary Steam Supply Header Pressure [bar] *)
    rPT_002_AirHeaderPress_bar      : REAL; (* Plant High-Pressure Compressed Air Supply Header Pressure [bar] *)
    rPT_003_CoolingWaterPress_bar   : REAL; (* Plant Sterile Cooling Water Supply Header Pressure [bar] *)
    rTT_004_CoolingWaterTemp_degC   : REAL; (* Plant Cooling Water Supply Inflow Temperature [deg C] *)
    rFT_101_RecircFlow_m3h          : REAL; (* Recirculation Loop Water Spray Flow Rate [m3/h] *)
    rST_101_RotaryBasketRPM         : REAL; (* Agitation Basket Rotary Drum Speed Feedback [RPM] *)
    rDT_501_CanDeflection_mm        : REAL; (* Pilot Flexible Pouch / Rigid Can Lid Deflection Transducer [mm] *)
    rPT_601_DoorSealPress_bar       : REAL; (* Vessel Door Inflatable Pneumatic Elastomer Seal Pressure [bar] *)

    (* ==================== DIGITAL INTERLOCKS & SAFETY DISCRETES ==================== *)
    bDI_DoorClosedLimit_ZS101       : BOOL; (* Vessel Door Full Mechanical Closed Proximity Limit Switch [-] *)
    bDI_DoorLockedLimit_ZS102       : BOOL; (* Hydraulic Safety Locking Pin Full Engagement Limit Switch [-] *)
    bDI_DoorSealPressureOK_PS103    : BOOL; (* Inflatable Door Gasket Pressure Switch Interlock (>= 5.0 bar) [-] *)
    bDI_EmergencyStop_PB100         : BOOL; (* Main Control Console Hardwired Emergency Stop Pushbutton [-] *)
    bDI_SafetyReliefValve_Open_ZS201: BOOL; (* Mechanical Safety Relief Valve Poppet Lift Proximity Switch [-] *)
    bDI_CondensateDrainClosed_ZS301 : BOOL; (* Bottom Condensate Purge Trap Bypass Isolation Valve Closed [-] *)

    (* ==================== OPERATOR COMMANDS & RECIPE SETPOINTS ==================== *)
    bCmd_StartCycle                 : BOOL; (* Operator Command: Initiate Automated LACF Thermal Cycle [-] *)
    bCmd_StopCycle                  : BOOL; (* Operator Command: Controlled Cycle Abort and Pre-Cool Drain [-] *)
    bCmd_HoldCycle                  : BOOL; (* Operator Command: Freeze Current Stage / Manual Hold [-] *)
    bCmd_ResumeCycle                : BOOL; (* Operator Command: Resume Normal Sequence from Manual Hold [-] *)
    bCmd_AcknowledgeAlarm           : BOOL; (* Operator Command: Acknowledge Active ISA-18.2 Process Alarms [-] *)
    bCmd_ResetTrip                  : BOOL; (* Operator Command: Reset Latched Faults Following Alarm Clear [-] *)
    bCmd_StartCIP                   : BOOL; (* Operator Command: Initiate Clean-In-Place / SIP Cycle [-] *)

    rSet_TargetCookTemp_degC        : REAL; (* Scheduled Thermal Sterilization Holding Temperature [deg C] *)
    rSet_TargetOverpressure_bar     : REAL; (* Total Vessel Absolute Counter-Pressure Cook Setpoint [bar] *)
    rSet_TargetF0_min               : REAL; (* Target Equivalent Thermal Lethality F0 for LACF Batch [min] *)
    rSet_ScheduledCookTime_s        : REAL; (* Ball Formula Scheduled Process Cook Time Duration [s] *)
    rSet_ComeUpRampRate_degCpm      : REAL; (* Thermal Come-Up Linear Ramp Rate Limit [deg C/min] *)
    rSet_TargetCoolingTemp_degC     : REAL; (* Final Container Product Core Temperature at Cycle End [deg C] *)
    rSet_RotaryCookRPM              : REAL; (* Basket Agitation Drum Target Rotational Speed [RPM] *)
    rSet_Ball_fh_min                : REAL; (* Heat Penetration Factor: Time for Straight-Line Curve to Traverse 1 Log Cycle [min] *)
    rSet_Ball_jch                   : REAL; (* Thermal Heating Lag Factor (j-value of Container Cold Spot) [-] *)
    rSet_Ball_z_degC                : REAL; (* Thermal Resistance z-value for Clostridium botulinum Spores [deg C] *)
    rSet_CanHeadspace_pct           : REAL; (* Container Gaseous Headspace Volume Fraction of Total Can Volume [%] *)
    rSet_MaxAllowableDeltaP_bar     : REAL; (* Maximum Allowable Container Internal-to-Vessel Pressure Difference [bar] *)
    rSet_VentPurgeDuration_s        : REAL; (* Atmospheric Vent Purge Duration to Displace Non-Condensable Air [s] *)
    rSet_PreCoolAirCushion_bar      : REAL; (* Deflection Balancing Overpressure Cushion Prior to Cold Water Inrush [bar] *)
END_VAR

VAR_OUTPUT
    (* ==================== ANALOG ACTUATOR COMMANDS ==================== *)
    rAO_SteamControlValve_pct       : REAL; (* Culinary Steam Modulating Control Valve Command [%] *)
    rAO_AirOverpressValve_pct       : REAL; (* Compressed Air Overpressure Modulating Control Valve Command [%] *)
    rAO_CoolingWaterValve_pct       : REAL; (* Sterile Cooling Water Spray Modulating Control Valve Command [%] *)
    rAO_VentModulatingValve_pct     : REAL; (* Atmospheric Exhaust / Pressure Vent Modulating Valve Command [%] *)
    rAO_RotaryDriveSpeed_RPM        : REAL; (* Agitation Drum Motor Variable Frequency Drive Speed Command [RPM] *)

    (* ==================== DIGITAL ACTUATOR & VALVE DISCRETES ==================== *)
    bDO_MainSteamIsolationValve     : BOOL; (* Main High-Pressure Steam Emergency Fast-Shutoff Valve [-] *)
    bDO_AirOverpressSupplyValve     : BOOL; (* Compressed Air Supply Header Fast-Acting Solenoid Valve [-] *)
    bDO_CoolingWaterPumpRun         : BOOL; (* High-Volume Cooling Water Recirculation Spray Pump Contactor [-] *)
    bDO_RecirculationPumpRun        : BOOL; (* Bottom Sump Water Recirculation & Evaporative Pump Contactor [-] *)
    bDO_SumpDrainValveOpen          : BOOL; (* Vessel Bottom Water Drainage Modulating Dump Valve Solenoid [-] *)
    bDO_VacuumBreakValveOpen        : BOOL; (* Atmospheric Vacuum Relief Siphon Breaker Valve Solenoid [-] *)
    bDO_DoorSealInflateSol          : BOOL; (* Vessel Door Gasket Pneumatic Air Inflation Solenoid [-] *)
    bDO_DoorSealDeflateSol          : BOOL; (* Vessel Door Gasket Pneumatic Rapid Exhaust Solenoid [-] *)
    bDO_HydraulicPinLockActuate     : BOOL; (* Door Locking Ring Hydraulic Linear Actuator Lock Direction [-] *)
    bDO_EmergencyQuenchValve        : BOOL; (* Extreme Overpressure / Over-Temperature Safety Deluge Valve [-] *)
    bDO_RotaryBrakeRelease          : BOOL; (* Agitation Drum Mechanical Friction Holding Brake Release [-] *)

    (* ==================== SYNTHESIZED CYBER-PHYSICAL STATE OUTPUTS ==================== *)
    iState                          : INT;  (* Active Deterministic Operational FSM Stage Index (0..14) [-] *)
    sStateName                      : STRING[40]; (* Human-Readable Descriptor of Current Operational State [-] *)
    rCurrentF0_min                  : REAL; (* Real-Time Cumulative Ball Thermal Lethality Integral [min] *)
    rVotedVesselTemp_degC           : REAL; (* 2oo3 TMR Reconciled Retort Vessel Steam-Air Temperature [deg C] *)
    rVotedVesselPress_bar           : REAL; (* 2oo3 TMR Reconciled Retort Vessel Absolute Pressure [bar] *)
    rVotedCanCoreTemp_degC          : REAL; (* 2oo3 TMR Reconciled Container Product Cold-Spot Temperature [deg C] *)
    rVotedSumpLevel_mm              : REAL; (* 2oo3 TMR Reconciled Bottom Condensate / Water Sump Level [mm] *)
    rCanInternalPress_bar           : REAL; (* Estimated Real-Time Container Gaseous & Vapor Internal Pressure [bar] *)
    rCanDifferentialPress_bar       : REAL; (* Net Stress Differential Pressure Across Can Pouch Wall (Pcan - Pv) [bar] *)
    rCycleElapsedTime_s             : REAL; (* Total Accumulated Autoclave Sterilization Cycle Duration [s] *)
    rStageElapsedTime_s             : REAL; (* Elapsed Operational Duration in Current FSM Processing State [s] *)
    rRemainingCookTime_s            : REAL; (* Calculated Time Remaining in Isothermal Sterilization Hold [s] *)
    rBallCatchupTimeRemaining_s     : REAL; (* Supplementary Thermal Time Required to Compensate Process Deviation [s] *)

    (* ==================== PROCESS QUALIFICATION & DIAGNOSTIC FLAGS ==================== *)
    bProcessQualified_FDA           : BOOL; (* FDA 21 CFR 113 Scheduled Thermal Lethality Target F0 Satisfied [-] *)
    bBallDeviationCatchupActive     : BOOL; (* C.O. Ball Process Deviation Catch-up Compensation Engaged [-] *)
    bCycleComplete                  : BOOL; (* Sterilization and Cooling Complete; Safe for Door Depressurization [-] *)
    bEmergencyStopActive            : BOOL; (* Latched Emergency Stop or Safety Interlock Trip Status [-] *)
    bAlarmCommon                    : BOOL; (* Master Summary Flag for Any Active ISA-18.2 Warning or Trip [-] *)

    (* ==================== 32-BIT PACKED WORDS (ISA-18.2 & REGULATORY) ==================== *)
    dwStatusWord                    : DWORD;(* Bit-Packed 32-Bit System Operational State & Permissives Word [-] *)
    dwWarningWord                   : DWORD;(* Bit-Packed 32-Bit ISA-18.2 Severity Level 2 Advisory Warning Word [-] *)
    dwFaultWord                     : DWORD;(* Bit-Packed 32-Bit ISA-18.2 Severity Level 1 Emergency Trip Word [-] *)
    dwFDAComplianceWord             : DWORD;(* Bit-Packed 32-Bit FDA 21 CFR 113 Legal Batch Validation Audit Word [-] *)
END_VAR
'''

if __name__ == "__main__":
    s = generate_header_io()
    print("Header & IO length:", len(s))
    print(s[:300])
