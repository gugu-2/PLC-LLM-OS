# st_header_and_io.py
# Contains FB header, documentation, VAR_INPUT and VAR_OUTPUT blocks

def get_header_and_io():
    return """FUNCTION_BLOCK FB_Semiconductor_Thermosonic_WireBonder_HighSpeed
(*
    ==========================================================================================================
    LUMINA CYBER-PHYSICAL SYSTEMS & ADVANCED PROCESS CONTROL SPECIFICATION
    System: Electronics & Semiconductor Packaging: Ultra-High-Speed Dual-Head Thermosonic Gold Wire Bonder
            (22 Wires/Sec, 35 um Pitch) with Electronic Flame-Off (EFO) Spark & Voice Coil Z-Drive
    Architecture: Dual-Head Ultra-High-Throughput Thermosonic Ball-Stitch Wire Interconnect Cell
    Applicable Standards: SEMI G45 (Leadframe Specification), SEMI E10 (RAM Reliability),
                          ISO 13849-1 Category 4 / PL e, IEC 61508 SIL 3, ISA-18.2 Alarm Management
    Target Performance: 22 Wires/Second per bondhead (~45.45 ms cycle period), 35 um ultra-fine pitch,
                        15-25 um 4N Au / 2N Cu wire, loop height repeatability +/- 2.0 um,
                        ball diameter repeatability +/- 0.5 um, soft-landing contact force < 0.15 N.
    ==========================================================================================================
*)

VAR_INPUT
    (* Master Supervisory & Interlock Commands *)
    b_Enable                            : BOOL;     (* System Master Enable supervisory run permit [boolean] *)
    b_EmergencyStop                     : BOOL;     (* Active-low hardware dual-channel E-Stop loop [boolean] *)
    b_CycleStart                        : BOOL;     (* High-speed auto-cycle initiation trigger [boolean] *)
    b_ResetAlarms                       : BOOL;     (* Global ISA-18.2 alarm acknowledge and reset [boolean] *)
    b_AutoTuneTransducer                : BOOL;     (* Trigger ultrasonic transducer impedance scan [boolean] *)
    b_CalibrateForceSensor              : BOOL;     (* Trigger tare calibration of piezoelectric load cells [boolean] *)
    b_EFO_FireManual                    : BOOL;     (* Manual maintenance trigger for EFO spark test [boolean] *)
    b_LeadframeIndexTrigger             : BOOL;     (* External indexer advance handshake trigger [boolean] *)

    (* Substrate Vacuum Workholder Sensors *)
    f_StageVacuum_Ch1_mbar              : LREAL;    (* Vacuum chuck pressure sensor Channel 1 [mbar] *)
    f_StageVacuum_Ch2_mbar              : LREAL;    (* Vacuum chuck pressure sensor Channel 2 [mbar] *)
    f_StageVacuum_Ch3_mbar              : LREAL;    (* Vacuum chuck pressure sensor Channel 3 [mbar] *)
    f_StageTemp_Zone1_degC              : LREAL;    (* Workholder substrate heater thermocouple Zone 1 [deg C] *)
    f_StageTemp_Zone2_degC              : LREAL;    (* Workholder substrate heater thermocouple Zone 2 [deg C] *)
    f_StageTemp_Zone3_degC              : LREAL;    (* Workholder substrate heater thermocouple Zone 3 [deg C] *)

    (* Voice Coil Motor (VCM) Z-Axis Optical Encoders (10 nm Resolution) *)
    f_ZEncoder_Ch1_nm                   : LREAL;    (* Linear optical scale Z-axis Channel 1 [nm] *)
    f_ZEncoder_Ch2_nm                   : LREAL;    (* Linear optical scale Z-axis Channel 2 [nm] *)
    f_ZEncoder_Ch3_nm                   : LREAL;    (* Linear optical scale Z-axis Channel 3 [nm] *)

    (* Dynamic Piezoelectric Contact Bond Force Sensors *)
    f_BondForce_LoadCell1_mN            : LREAL;    (* Capillary bondhead load cell Channel 1 [mN] *)
    f_BondForce_LoadCell2_mN            : LREAL;    (* Capillary bondhead load cell Channel 2 [mN] *)
    f_BondForce_LoadCell3_mN            : LREAL;    (* Capillary bondhead load cell Channel 3 [mN] *)

    (* Dual-Frequency Ultrasonic Generator & Transducer Sensors *)
    f_US_FeedbackPower_Ch1_mW           : LREAL;    (* Ultrasonic electrical power feedback Channel 1 [mW] *)
    f_US_FeedbackPower_Ch2_mW           : LREAL;    (* Ultrasonic electrical power feedback Channel 2 [mW] *)
    f_US_FeedbackPower_Ch3_mW           : LREAL;    (* Ultrasonic electrical power feedback Channel 3 [mW] *)
    f_US_ImpedancePhase_deg             : LREAL;    (* Transducer V-I dynamic phase angle [-90.0..+90.0 deg] *)
    f_US_Frequency_kHz                  : LREAL;    (* Ultrasonic active resonant drive frequency [kHz] *)
    f_US_Current_mA                     : LREAL;    (* Ultrasonic drive current RMS monitor [mA] *)
    b_US_DualFreq_SelectHigh            : BOOL;     (* Select 138 kHz mode (TRUE) or 60 kHz mode (FALSE) [boolean] *)

    (* Electronic Flame-Off (EFO) Spark Sensors *)
    f_EFOCurrent_mA                     : LREAL;    (* EFO spark discharge gap current monitor [mA] *)
    f_EFOVoltage_V                      : LREAL;    (* EFO capacitive high-voltage pulse monitor [V] *)
    f_EFOTime_us                        : LREAL;    (* EFO spark breakdown pulse duration [us] *)

    (* Optical Pattern Recognition (PR) In-Line Vision Alignment *)
    f_PR_OffsetX_um                     : LREAL;    (* Vision measured die placement translation X [um] *)
    f_PR_OffsetY_um                     : LREAL;    (* Vision measured die placement translation Y [um] *)
    f_PR_OffsetTheta_mrad               : LREAL;    (* Vision measured die placement rotational error [mrad] *)
    b_PR_MatchValid                     : BOOL;     (* Optical vision match validity and confidence flag [boolean] *)
    f_PR_CorrelationScore               : LREAL;    (* Normalized cross-correlation score [0.0..1.0] *)

    (* Wire Spool & Wire Clamping Feed System *)
    f_WireSpoolTension_mN               : LREAL;    (* Gold/Copper wire de-reeler back tension monitor [mN] *)
    f_WireDiameter_Nominal_um           : LREAL;    (* Nominal wire diameter specified for recipe [um] *)
    f_WireTailLength_Sensor_um          : LREAL;    (* Laser triangulation tail length measurement [um] *)
    b_WireDragSensor_Tripped            : BOOL;     (* Optical sensor detecting broken or drag wire [boolean] *)

    (* Process Recipe Setpoints *)
    n_TargetBondCount                   : DINT;     (* Total wire interconnect count required per die unit [count] *)
    f_SetBondForce_1st_mN               : LREAL;    (* 1st bond (ball) commanded contact force setpoint [mN] *)
    f_SetBondForce_2nd_mN               : LREAL;    (* 2nd bond (stitch) commanded contact force setpoint [mN] *)
    f_SetUSPower_1st_mW                 : LREAL;    (* 1st bond commanded ultrasonic power setpoint [mW] *)
    f_SetUSPower_2nd_mW                 : LREAL;    (* 2nd bond commanded ultrasonic power setpoint [mW] *)
    f_SetBondTime_1st_ms                : LREAL;    (* 1st bond ultrasonic burst duration setpoint [ms] *)
    f_SetBondTime_2nd_ms                : LREAL;    (* 2nd bond ultrasonic burst duration setpoint [ms] *)
    f_SetLoopHeight_um                  : LREAL;    (* Commanded wire loop apex target height [um] *)
    f_SetLoopSpan_um                    : LREAL;    (* Commanded ball-to-stitch interconnect span length [um] *)
    f_SetStageTemp_degC                 : LREAL;    (* Commanded workholder vacuum stage temperature setpoint [deg C] *)
    f_EFO_DischargeEnergy_uJ            : LREAL;    (* Commanded EFO spark discharge energy setpoint [uJ] *)
    f_LeadframeIndexPitch_mm            : LREAL;    (* Leadframe indexer pitch step distance [mm] *)
END_VAR

VAR_OUTPUT
    (* Supervisory Status Flags *)
    b_Ready                             : BOOL;     (* Wire bonder module ready for indexing & bonding [boolean] *)
    b_Active                            : BOOL;     (* Wire bonder executing high-speed bonding cycle [boolean] *)
    b_Done                              : BOOL;     (* Current die/unit interconnect wire mesh completed [boolean] *)
    b_Error                             : BOOL;     (* Master fault trip flag [boolean] *)
    n_ErrorCode                         : DINT;     (* Active fault diagnostic error code [enum] *)
    n_CurrentState                      : INT;      (* Active FSM state enumeration index [1..12] *)

    (* Actuator Command Signals *)
    f_VCM_DriveCurrent_mA               : LREAL;    (* Commanded voice coil motor drive current [-5000.0..+5000.0 mA] *)
    f_US_DrivePower_mW                  : LREAL;    (* Commanded ultrasonic transducer drive power [0.0..1500.0 mW] *)
    f_US_PLL_Frequency_kHz              : LREAL;    (* Active ultrasonic resonant frequency command [kHz] *)
    f_EFO_TriggerPulse_V                : LREAL;    (* Commanded EFO capacitive discharge trigger voltage [V] *)
    b_WireClampSol_Open                 : BOOL;     (* High-speed pneumatic wire clamp open actuator command [boolean] *)
    b_WireClampSol_Close                : BOOL;     (* High-speed pneumatic wire clamp close actuator command [boolean] *)
    b_AirTensioner_Active               : BOOL;     (* Air-bearing wire drag/tensioner pneumatic solenoid command [boolean] *)
    f_WorkholderHeatPwr_Zone1_pct       : LREAL;    (* Substrate Zone 1 PWM heating duty cycle command [0.0..100.0 %] *)
    f_WorkholderHeatPwr_Zone2_pct       : LREAL;    (* Substrate Zone 2 PWM heating duty cycle command [0.0..100.0 %] *)
    f_WorkholderHeatPwr_Zone3_pct       : LREAL;    (* Substrate Zone 3 PWM heating duty cycle command [0.0..100.0 %] *)
    b_StageVacuumSol_Cmd                : BOOL;     (* Substrate chuck vacuum venturi solenoid command [boolean] *)
    b_LeadframeClamped                  : BOOL;     (* Mechanical edge clamp engaged status [boolean] *)
    b_LeadframeIndexPulse               : BOOL;     (* Leadframe stepper index command pulse [boolean] *)

    (* 2oo3 TMR Voted Process Telemetry *)
    f_Voted_ZPos_nm                     : LREAL;    (* 2oo3 validated Z-axis position [nm] *)
    f_Voted_BondForce_mN                : LREAL;    (* 2oo3 validated contact bond force [mN] *)
    f_Voted_USPower_mW                  : LREAL;    (* 2oo3 validated ultrasonic power [mW] *)
    f_Voted_StageVacuum_mbar            : LREAL;    (* 2oo3 validated substrate vacuum chuck pressure [mbar] *)

    (* In-Line Metrology & Closed-Loop Quality Metrics *)
    f_FAB_MeasuredDiameter_um           : LREAL;    (* In-line optical verified Free Air Ball diameter [um] *)
    f_BondDeformation_um                : LREAL;    (* Real-time ultrasonic ball squashing/deformation [um] *)
    f_IntermetallicGrowth_nm            : LREAL;    (* Estimated Au-Al / Cu-Al intermetallic layer thickness [nm] *)
    f_EstimatedShearStrength_gf         : LREAL;    (* Estimated atomic joint shear bond strength [gf] *)
    f_CurrentBondRate_wps               : LREAL;    (* Instantaneous throughput bonding rate [wires/second] *)
    n_CompletedWiresDie                 : DINT;     (* Completed wires count on current die unit [count] *)
    n_TotalWiresAccumulated             : LINT;     (* Total life-cycle wire bonds completed [count] *)

    (* ISA-18.2 Alarm Groups & Diagnostics *)
    dw_AlarmsGroup1                     : DWORD;    (* ISA-18.2 Critical Process Trip Alarms bit-packed [dword] *)
    dw_AlarmsGroup2                     : DWORD;    (* ISA-18.2 Warning & Degradation Alarms bit-packed [dword] *)
    dw_DiagnosticsWord                  : DWORD;    (* System hardware & TMR diagnostic telemetry bit-packed [dword] *)
END_VAR
"""
