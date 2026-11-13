# fpso_gen/declarations.py
def get_declarations():
    return """FUNCTION_BLOCK FB_OilGas_FPSO_TopsideGasCompression_TEGDehydration
(* =====================================================================================================================
 * LUMINA CYBER-PHYSICAL AUTOMATION ENGINE - SYNTHETIC DATASET V7 MAX-PERSONA
 * ARCHITECTURAL GRADE : Offshore Oil & Gas Floating Production (Tier 1 Priority Global Commercial Sector)
 * COMMERCIAL SYSTEM   : FPSO Topside 3-Stage Centrifugal Compression Train (60 MW VFD, 250 bar export pressure),
 *                       Anti-Surge Closed-Loop Recycle Valve Cascade (< 1.2 s stroke), Triethylene Glycol (TEG)
 *                       High-Pressure Absorption Contactor Tower & Stripping Reboiler Still Column, Molecular Sieve
 *                       Moisture Tracking, Marine Hull 6-DOF Pitch/Roll Wave Motion Decoupling, and SIL-3
 *                       Emergency Depressurization (EDP) to High-Pressure Flare.
 * APPLICABLE CODES    : API 617 (Centrifugal Compressors), API 521 (Depressurization & Flare Blowdown),
 *                       ISO 13623 / ISO 10439 (Petroleum & Natural Gas Industries), IEC 61508 / IEC 61511 (SIL-3),
 *                       ISA-18.2 (Alarm Systems Management), GPSA Engineering Data Book Section 20 (Dehydration).
 * ===================================================================================================================== *)

VAR_INPUT
    (* =================================================================================================================
     * SECTION 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) CRITICAL SAFETY SENSOR TRIPLET CHANNELS
     * ================================================================================================================= *)
    rSuctionPres_PT101A_In          : REAL;    (* Stage 1 Suction Pressure Sensor Channel A [bar] *)
    rSuctionPres_PT101B_In          : REAL;    (* Stage 1 Suction Pressure Sensor Channel B [bar] *)
    rSuctionPres_PT101C_In          : REAL;    (* Stage 1 Suction Pressure Sensor Channel C [bar] *)

    rDischargePres_PT201A_In        : REAL;    (* Stage 3 Discharge Export Pressure Sensor Channel A [bar] *)
    rDischargePres_PT201B_In        : REAL;    (* Stage 3 Discharge Export Pressure Sensor Channel B [bar] *)
    rDischargePres_PT201C_In        : REAL;    (* Stage 3 Discharge Export Pressure Sensor Channel C [bar] *)

    rSuctionDP_PDT301A_In           : REAL;    (* Stage 1 Suction Venturi DP Channel A [mbar] *)
    rSuctionDP_PDT301B_In           : REAL;    (* Stage 1 Suction Venturi DP Channel B [mbar] *)
    rSuctionDP_PDT301C_In           : REAL;    (* Stage 1 Suction Venturi DP Channel C [mbar] *)

    rShaftVib_VT401A_In             : REAL;    (* Compressor Drive-End Shaft Radial Vibration Probe A [um] *)
    rShaftVib_VT401B_In             : REAL;    (* Compressor Drive-End Shaft Radial Vibration Probe B [um] *)
    rShaftVib_VT401C_In             : REAL;    (* Compressor Drive-End Shaft Radial Vibration Probe C [um] *)

    rExportMoisture_AT501A_In       : REAL;    (* Export Gas Moisture Analyzer Channel A [ppmv] *)
    rExportMoisture_AT501B_In       : REAL;    (* Export Gas Moisture Analyzer Channel B [ppmv] *)
    rExportMoisture_AT501C_In       : REAL;    (* Export Gas Moisture Analyzer Channel C [ppmv] *)

    (* =================================================================================================================
     * SECTION 2: MULTI-STAGE COMPRESSION PROCESS TRANSMITTERS & AUXILIARY SIGNALS
     * ================================================================================================================= *)
    rSuctionTemp_TT101_In           : REAL;    (* Stage 1 Suction Gas Temperature [deg C] *)
    rInterstagePres_PT102_In        : REAL;    (* Stage 2 Suction Interstage Pressure [bar] *)
    rInterstageTemp_TT102_In        : REAL;    (* Stage 2 Suction Interstage Temperature [deg C] *)
    rInterstageDP_PDT302_In         : REAL;    (* Stage 2 Suction Orifice Flow Differential Pressure [mbar] *)
    rStage3SuctionPres_PT103_In     : REAL;    (* Stage 3 Suction Interstage Pressure [bar] *)
    rStage3DischargeTemp_TT201_In   : REAL;    (* Stage 3 Discharge Gas Temperature [deg C] *)
    rStage3DP_PDT303_In             : REAL;    (* Stage 3 Suction Orifice Flow Differential Pressure [mbar] *)
    rCompressorSpeed_ST101_In       : REAL;    (* 60 MW Drive Shaft Speed Tachometer Feedback [rpm] *)
    rMotorPower_WT101_In            : REAL;    (* VFD Electric Motor Active Electric Power Draw [kW] *)
    rLubeOilPres_PT601_In           : REAL;    (* Compressor Bearing Header Lube Oil Pressure [bar] *)
    rLubeOilTemp_TT601_In           : REAL;    (* Compressor Bearing Header Lube Oil Supply Temperature [deg C] *)
    rSealGasDP_PDT701_In            : REAL;    (* Dry Gas Seal Primary Differential Pressure [bar] *)

    (* =================================================================================================================
     * SECTION 3: TRIETHYLENE GLYCOL (TEG) DEHYDRATION & REGENERATION TRANSMITTERS
     * ================================================================================================================= *)
    rTEG_ContactorPres_PT502_In     : REAL;    (* TEG Absorption Contactor Column Operating Pressure [bar] *)
    rTEG_ContactorDP_PDT503_In      : REAL;    (* TEG Contactor Column Packed Bed Differential Pressure [mbar] *)
    rTEG_LeanFlow_FT501_In          : REAL;    (* Lean TEG Glycol Infeed Volumetric Flow Rate [m3/h] *)
    rTEG_LeanTemp_TT502_In          : REAL;    (* Lean TEG Glycol Infeed Temperature to Contactor [deg C] *)
    rTEG_ReboilerTemp_TT503_In      : REAL;    (* TEG Regeneration Stripping Reboiler Temperature [deg C] *)
    rTEG_ReboilerLevel_LT501_In     : REAL;    (* TEG Reboiler Liquid Sump Level [%] *)
    rTEG_LeanPurity_AT502_In        : REAL;    (* Stripped Lean TEG Glycol Mass Fraction Purity [%] *)
    rTEG_FlashDrumPres_PT504_In     : REAL;    (* TEG Rich Glycol Flash Drum Pressure [bar] *)

    (* =================================================================================================================
     * SECTION 4: FPSO MARINE HULL 6-DOF WAVE MOTION & ACCELERATION TRANSMITTERS
     * ================================================================================================================= *)
    rFPSO_RollAngle_In              : REAL;    (* Vessel Marine Hull Dynamic Roll Angle [deg] *)
    rFPSO_PitchAngle_In             : REAL;    (* Vessel Marine Hull Dynamic Pitch Angle [deg] *)
    rFPSO_HeaveAccel_In             : REAL;    (* Vessel Marine Hull Vertical Heave Wave Acceleration [m/s2] *)
    rFPSO_RollRate_In               : REAL;    (* Vessel Marine Hull Roll Angular Velocity [deg/s] *)
    rFPSO_PitchRate_In              : REAL;    (* Vessel Marine Hull Pitch Angular Velocity [deg/s] *)
    rFPSO_YawRate_In                : REAL;    (* Vessel Marine Hull Yaw Angular Velocity [deg/s] *)

    (* =================================================================================================================
     * SECTION 5: PIPELINE BOUNDARY, PROCESS COMPOSITION & SUPERVISORY PERMISSIVES
     * ================================================================================================================= *)
    rPipeline_BackPres_PT801_In     : REAL;    (* Subsea Export Gas Export Pipeline Header Pressure [bar] *)
    rGasMolecularWeight_In          : REAL;    (* Process Feed Gas Calculated Molecular Weight [kg/kmol] *)
    bPermissive_InfeedGas_In        : BOOL;    (* Upstream Slug Catcher Gas Delivery Ready Permissive [bool] *)
    bPermissive_FlareSystem_In      : BOOL;    (* High Pressure Topside Flare Header Open Permissive [bool] *)
    bPermissive_ExportPipeline_In   : BOOL;    (* Subsea Gas Export Pipeline ESD Valve Open Permissive [bool] *)
    bCmd_Start_In                   : BOOL;    (* Operator Master Train Start Command Pulse [bool] *)
    bCmd_Stop_In                    : BOOL;    (* Operator Master Train Controlled Stop Command Pulse [bool] *)
    bCmd_Reset_In                   : BOOL;    (* Master Safety & Diagnostics Fault Acknowledgment Reset [bool] *)
    bCmd_EmergencyDepress_In        : BOOL;    (* Topside SIS SIL-3 Emergency Depressurization (EDP) Manual Trip Pushbutton [bool] *)
END_VAR

VAR_OUTPUT
    (* =================================================================================================================
     * SECTION 1: FAST ANTI-SURGE RECYCLE ACTUATOR & VFD SPEED CONTROL DEMANDS
     * ================================================================================================================= *)
    rAntiSurgeValve_Stg1_Cmd_Out    : REAL;    (* Stage 1 Fast Anti-Surge Recycle Throttle Valve Demand [%] *)
    rAntiSurgeValve_Stg2_Cmd_Out    : REAL;    (* Stage 2 Fast Anti-Surge Recycle Throttle Valve Demand [%] *)
    rAntiSurgeValve_Stg3_Cmd_Out    : REAL;    (* Stage 3 Fast Anti-Surge Recycle Throttle Valve Demand [%] *)
    rVFD_Speed_Demand_Out           : REAL;    (* 60 MW Variable Speed Drive Master Speed Reference [rpm] *)

    (* =================================================================================================================
     * SECTION 2: TEG DEHYDRATION & REGENERATION ACTUATOR SIGNALS
     * ================================================================================================================= *)
    rTEG_Pump_Speed_Cmd_Out         : REAL;    (* High-Pressure Triplex Lean Glycol Circulation Pump Demand [%] *)
    rTEG_Reboiler_Duty_Cmd_Out      : REAL;    (* Regeneration Reboiler Thermic Fluid Heating Control Valve [%] *)
    rTEG_StrippingGas_Cmd_Out       : REAL;    (* Reboiler Still Column Stripping Gas Control Valve [%] *)

    (* =================================================================================================================
     * SECTION 3: PROCESS HEADER VALVES & THERMAL BYPASS MODULATION
     * ================================================================================================================= *)
    rSuctionChoke_Cmd_Out           : REAL;    (* Stage 1 Suction Header Pressure Regulating Valve [%] *)
    rExportChoke_Cmd_Out            : REAL;    (* High-Pressure Subsea Export Flow Control Choke Valve [%] *)
    rInterstageCooler1_Bypass_Out   : REAL;    (* Interstage Cooler 1 Temperature Bypass Valve [%] *)
    rInterstageCooler2_Bypass_Out   : REAL;    (* Interstage Cooler 2 Temperature Bypass Valve [%] *)

    (* =================================================================================================================
     * SECTION 4: SIL-3 SAFETY INSTRUMENTED SHUTDOWN & EMERGENCY DEPRESSURIZATION
     * ================================================================================================================= *)
    bEDP_HP_FlareValve_Open_Out     : BOOL;    (* SIL-3 Emergency Depressurization Fast High-Pressure Flare Valve [bool] *)
    bEDP_LP_FlareValve_Open_Out     : BOOL;    (* SIL-3 Emergency Depressurization Low-Pressure Scrubber Flare Valve [bool] *)
    bInfeed_Isolation_Close_Out     : BOOL;    (* Upstream Feed Gas Emergency Isolation Valve Trip Signal [bool] *)
    bExport_Isolation_Close_Out     : BOOL;    (* Subsea Export Pipeline Emergency Isolation Valve Trip Signal [bool] *)
    bVFD_EmergencyTrip_Out          : BOOL;    (* 60 MW Drive Fast Hardware Interlock Shutdown Trip [bool] *)
    bLubeOil_AuxPump_Start_Out      : BOOL;    (* Standby Lube Oil Auxiliary Skid Motor Start Command [bool] *)

    (* =================================================================================================================
     * SECTION 5: REAL-TIME CYBER-PHYSICAL COMPUTED METRICS & PROCESS TELEMETRY
     * ================================================================================================================= *)
    rSurgeMargin_Stg1_Out           : REAL;    (* Stage 1 Calculated Real-Time Surge Proximity Ratio [-] *)
    rSurgeMargin_Stg2_Out           : REAL;    (* Stage 2 Calculated Real-Time Surge Proximity Ratio [-] *)
    rSurgeMargin_Stg3_Out           : REAL;    (* Stage 3 Calculated Real-Time Surge Proximity Ratio [-] *)
    rPolytropicHead_Total_Out       : REAL;    (* Total Polytropic Compression Head [kJ/kg] *)
    rPolytropicEfficiency_Out       : REAL;    (* Overall Train Polytropic Thermodynamic Efficiency [%] *)
    rVesselMotion_Derate_Factor_Out : REAL;    (* Marine Hull Wave Motion Dynamic Surge Bias Derate Factor [-] *)
    rContactor_FoamIndex_Out        : REAL;    (* TEG Contactor Tray Differential Pressure Foaming Metric [-] *)

    (* =================================================================================================================
     * SECTION 6: 2oo3 VOTED PROCESS SIGNALS
     * ================================================================================================================= *)
    rVoted_SuctionPres_Out          : REAL;    (* 2oo3 Voted Stage 1 Suction Pressure [bar] *)
    rVoted_DischargePres_Out        : REAL;    (* 2oo3 Voted Stage 3 Discharge Export Pressure [bar] *)
    rVoted_SuctionDP_Out            : REAL;    (* 2oo3 Voted Stage 1 Suction Venturi DP [mbar] *)
    rVoted_ShaftVib_Out             : REAL;    (* 2oo3 Voted Drive-End Shaft Radial Vibration [um] *)
    rVoted_ExportMoisture_Out       : REAL;    (* 2oo3 Voted Export Gas Moisture Content [ppmv] *)

    (* =================================================================================================================
     * SECTION 7: 32-BIT BIT-PACKED STATUS & ALARM TELEMETRY REGISTERS
     * ================================================================================================================= *)
    dwStatus_FSM_State_Out          : DWORD;   (* Current Active FSM Stage (1-14) and State Machine Telemetry [dword] *)
    dwStatus_TMR_Health_Out         : DWORD;   (* 32-Bit Health Bitmask for 5 Sets of 2oo3 Sensor Channels [dword] *)
    dwStatus_Actuator_Flags_Out     : DWORD;   (* 32-Bit Bitmask for Actuator Feedback & Solenoid Status [dword] *)
    dwAlarm_Trip_Critical_Out       : DWORD;   (* ISA-18.2 Priority 1 / SIL-3 Emergency Safety Trip Alarms [dword] *)
    dwAlarm_Warnings_High_Out       : DWORD;   (* ISA-18.2 Priority 2 Process Parameter High Warning Alarms [dword] *)
    dwAlarm_Warnings_Low_Out        : DWORD;   (* ISA-18.2 Priority 3 Process Parameter Low Warning Alarms [dword] *)
    bSystem_Trip_Latched_Out        : BOOL;    (* Master Safety Shutdown Latched Flag [bool] *)
    bSystem_Ready_Out               : BOOL;    (* Compression Train Ready for Process Gas Start Permissive [bool] *)
END_VAR

VAR
    (* =================================================================================================================
     * SECTION 1: GLOBAL CONSTANTS & EXECUTION CYCLE PARAMETERS
     * ================================================================================================================= *)
    rTs                             : REAL := 0.010;        (* Discrete Execution Cycle Sample Time [s] *)
    rGasConstant_R                  : REAL := 8314.462;     (* Universal Gas Constant [J/(kmol*K)] *)
    rStdGravity                     : REAL := 9.80665;      (* Standard Sea-Level Gravitational Acceleration [m/s2] *)

    (* =================================================================================================================
     * SECTION 2: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) INTERNAL STRUCTURES & TIMERS
     * ================================================================================================================= *)
    (* PT-101 Suction Pressure *)
    rTMR_PT101_ValA                 : REAL := 0.0;
    rTMR_PT101_ValB                 : REAL := 0.0;
    rTMR_PT101_ValC                 : REAL := 0.0;
    rTMR_PT101_DeltaAB              : REAL := 0.0;
    rTMR_PT101_DeltaBC              : REAL := 0.0;
    rTMR_PT101_DeltaCA              : REAL := 0.0;
    rTMR_PT101_TimerA               : REAL := 0.0;
    rTMR_PT101_TimerB               : REAL := 0.0;
    rTMR_PT101_TimerC               : REAL := 0.0;
    bTMR_PT101_HealthyA             : BOOL := TRUE;
    bTMR_PT101_HealthyB             : BOOL := TRUE;
    bTMR_PT101_HealthyC             : BOOL := TRUE;
    rTMR_PT101_Tol                  : REAL := 1.25;         (* Channel Tolerance Deviation Limit [bar] *)
    rTMR_PT101_TimeLimit            : REAL := 0.250;        (* Discrepancy Fault Integration Threshold [s] *)
    rVoted_PT101_Internal           : REAL := 25.0;

    (* PT-201 Discharge Pressure *)
    rTMR_PT201_ValA                 : REAL := 0.0;
    rTMR_PT201_ValB                 : REAL := 0.0;
    rTMR_PT201_ValC                 : REAL := 0.0;
    rTMR_PT201_DeltaAB              : REAL := 0.0;
    rTMR_PT201_DeltaBC              : REAL := 0.0;
    rTMR_PT201_DeltaCA              : REAL := 0.0;
    rTMR_PT201_TimerA               : REAL := 0.0;
    rTMR_PT201_TimerB               : REAL := 0.0;
    rTMR_PT201_TimerC               : REAL := 0.0;
    bTMR_PT201_HealthyA             : BOOL := TRUE;
    bTMR_PT201_HealthyB             : BOOL := TRUE;
    bTMR_PT201_HealthyC             : BOOL := TRUE;
    rTMR_PT201_Tol                  : REAL := 5.00;         (* Channel Tolerance Deviation Limit [bar] *)
    rTMR_PT201_TimeLimit            : REAL := 0.250;        (* Discrepancy Fault Integration Threshold [s] *)
    rVoted_PT201_Internal           : REAL := 250.0;

    (* PDT-301 Stage 1 Suction Venturi DP *)
    rTMR_PDT301_ValA                : REAL := 0.0;
    rTMR_PDT301_ValB                : REAL := 0.0;
    rTMR_PDT301_ValC                : REAL := 0.0;
    rTMR_PDT301_DeltaAB             : REAL := 0.0;
    rTMR_PDT301_DeltaBC             : REAL := 0.0;
    rTMR_PDT301_DeltaCA             : REAL := 0.0;
    rTMR_PDT301_TimerA              : REAL := 0.0;
    rTMR_PDT301_TimerB              : REAL := 0.0;
    rTMR_PDT301_TimerC              : REAL := 0.0;
    bTMR_PDT301_HealthyA            : BOOL := TRUE;
    bTMR_PDT301_HealthyB            : BOOL := TRUE;
    bTMR_PDT301_HealthyC            : BOOL := TRUE;
    rTMR_PDT301_Tol                 : REAL := 15.0;         (* Channel Tolerance Deviation Limit [mbar] *)
    rTMR_PDT301_TimeLimit           : REAL := 0.100;        (* Discrepancy Fault Integration Threshold [s] *)
    rVoted_PDT301_Internal          : REAL := 120.0;

    (* VT-401 Shaft Radial Vibration *)
    rTMR_VT401_ValA                 : REAL := 0.0;
    rTMR_VT401_ValB                 : REAL := 0.0;
    rTMR_VT401_ValC                 : REAL := 0.0;
    rTMR_VT401_DeltaAB              : REAL := 0.0;
    rTMR_VT401_DeltaBC              : REAL := 0.0;
    rTMR_VT401_DeltaCA              : REAL := 0.0;
    rTMR_VT401_TimerA               : REAL := 0.0;
    rTMR_VT401_TimerB               : REAL := 0.0;
    rTMR_VT401_TimerC               : REAL := 0.0;
    bTMR_VT401_HealthyA             : BOOL := TRUE;
    bTMR_VT401_HealthyB             : BOOL := TRUE;
    bTMR_VT401_HealthyC             : BOOL := TRUE;
    rTMR_VT401_Tol                  : REAL := 8.5;          (* Channel Tolerance Deviation Limit [um] *)
    rTMR_VT401_TimeLimit            : REAL := 0.150;        (* Discrepancy Fault Integration Threshold [s] *)
    rVoted_VT401_Internal           : REAL := 22.0;

    (* AT-501 Export Gas Moisture *)
    rTMR_AT501_ValA                 : REAL := 0.0;
    rTMR_AT501_ValB                 : REAL := 0.0;
    rTMR_AT501_ValC                 : REAL := 0.0;
    rTMR_AT501_DeltaAB              : REAL := 0.0;
    rTMR_AT501_DeltaBC              : REAL := 0.0;
    rTMR_AT501_DeltaCA              : REAL := 0.0;
    rTMR_AT501_TimerA               : REAL := 0.0;
    rTMR_AT501_TimerB               : REAL := 0.0;
    rTMR_AT501_TimerC               : REAL := 0.0;
    bTMR_AT501_HealthyA             : BOOL := TRUE;
    bTMR_AT501_HealthyB             : BOOL := TRUE;
    bTMR_AT501_HealthyC             : BOOL := TRUE;
    rTMR_AT501_Tol                  : REAL := 3.5;          (* Channel Tolerance Deviation Limit [ppmv] *)
    rTMR_AT501_TimeLimit            : REAL := 0.500;        (* Discrepancy Fault Integration Threshold [s] *)
    rVoted_AT501_Internal           : REAL := 18.0;

    (* =================================================================================================================
     * SECTION 3: 6-STATE CYBER-PHYSICAL DISCRETE STATE-SPACE MATRICES & OBSERVER
     * State Vector x = [delta_Ps1, delta_Pd3, delta_MassFlow, delta_ShaftSpeed, delta_Moisture, delta_RecyclePres]^T
     * Input Vector u = [u_ASV1, u_ASV2, u_ASV3, delta_VFD_Speed]^T
     * Disturbance Vector w = [w_PipelineBackPres, w_WaveHeaveAccel, w_FeedMoistureSat]^T
     * ================================================================================================================= *)
    rMatrix_A                       : ARRAY[1..6, 1..6] OF REAL;
    rMatrix_B                       : ARRAY[1..6, 1..4] OF REAL;
    rMatrix_C                       : ARRAY[1..6, 1..6] OF REAL;
    rMatrix_D                       : ARRAY[1..6, 1..4] OF REAL;
    rMatrix_Ew                      : ARRAY[1..6, 1..3] OF REAL;
    rObserver_L                     : ARRAY[1..6, 1..6] OF REAL;

    rVec_x                          : ARRAY[1..6] OF REAL;  (* Physical Process Deviation State Vector *)
    rVec_x_hat                      : ARRAY[1..6] OF REAL;  (* Luenberger Observer Estimated State Vector *)
    rVec_x_sp                       : ARRAY[1..6] OF REAL;  (* Model Predictive Control Target Setpoint Vector *)
    rVec_y                          : ARRAY[1..6] OF REAL;  (* Measured System Output Vector *)
    rVec_y_hat                      : ARRAY[1..6] OF REAL;  (* Observer Predicted Output Vector *)
    rVec_u                          : ARRAY[1..4] OF REAL;  (* Applied Control Demand Vector *)
    rVec_u_prev                     : ARRAY[1..4] OF REAL;  (* Previous Execution Step Control Vector *)
    rVec_w                          : ARRAY[1..3] OF REAL;  (* External Disturbance Estimation Vector *)
    rVec_e_obs                      : ARRAY[1..6] OF REAL;  (* Innovation Output Estimation Error *)
    bStateSpace_Initialized         : BOOL := FALSE;

    (* =================================================================================================================
     * SECTION 4: MODEL PREDICTIVE CONTROL (MPC) & PROJECTED GRADIENT DESCENT (PGD) ARRAYS
     * ================================================================================================================= *)
    rMPC_Weight_Q                   : ARRAY[1..6] OF REAL;  (* State Deviation Penalty Matrix Q Diagonal *)
    rMPC_Weight_R                   : ARRAY[1..4] OF REAL;  (* Control Actuation Penalty Matrix R Diagonal *)
    rMPC_Weight_S                   : ARRAY[1..4] OF REAL;  (* Control Rate-of-Change Penalty Matrix S Diagonal *)
    rMPC_Weight_P                   : ARRAY[1..6] OF REAL;  (* Terminal State Penalty Matrix P Diagonal *)

    rMPC_x_pred                     : ARRAY[1..5, 1..6] OF REAL; (* Prediction Horizon (Np=5) State Trajectory *)
    rMPC_u_pred                     : ARRAY[1..5, 1..4] OF REAL; (* Prediction Horizon (Np=5) Control Inputs *)
    rMPC_grad                       : ARRAY[1..5, 1..4] OF REAL; (* Unrolled Cost Functional Gradient Vector *)
    rMPC_StepSize                   : REAL := 0.00045;      (* PGD Optimization Gradient Step Factor *)
    rMPC_MaxSlewASV                 : REAL := 0.8333;       (* Valve Slew Limit (100% in 1.2s -> 0.833% per 10ms) [%] *)
    rMPC_MaxSlewVFD                 : REAL := 0.5000;       (* VFD Speed Slew Limit (50 rpm/s -> 0.5 rpm per 10ms) [rpm] *)
    rMPC_BarrierGain                : REAL := 150000.0;     (* Surge Margin Hard Asymmetric Penalty Multiplier *)

    (* =================================================================================================================
     * SECTION 5: MARINE HULL 6-DOF WAVE MOTION DYNAMIC DECOUPLING VARIABLES
     * ================================================================================================================= *)
    rVessel_TiltAngle               : REAL := 0.0;          (* Total Dynamic Hull Tilt Vector Magnitude [deg] *)
    rVessel_TiltRate                : REAL := 0.0;          (* Total Hull Angular Velocity Vector Magnitude [deg/s] *)
    rVessel_EffGravity              : REAL := 9.80665;      (* Effective Vertical Acceleration Vector [m/s2] *)
    rContactor_SloshDampingFactor   : REAL := 1.0;          (* TEG Contactor Mass Transfer Wetting Factor [-] *)
    rContactor_FoamIndex            : REAL := 0.0;          (* Contactor Tray Hydraulic Foaming Indicator [-] *)
    rDemister_CarryoverRisk         : REAL := 0.0;          (* Suction Scrubber Mist Eliminator Entrainment Metric [-] *)
    rGyro_PrecessionBearingLoad     : REAL := 0.0;          (* Shaft Radial Bearing Dynamic Precession Force [kN] *)
    rDynamicSurgeBias_Wave          : REAL := 0.0;          (* Added Surge Control Line Margin Due to Waves [-] *)

    (* =================================================================================================================
     * SECTION 6: THERMODYNAMIC, AERODYNAMIC & SURGE PROTECTION PARAMETERS
     * ================================================================================================================= *)
    rGas_Mw                         : REAL := 19.85;        (* Natural Gas Molecular Weight [kg/kmol] *)
    rGas_Z_Avg                      : REAL := 0.885;        (* Average Real Gas Supercompressibility Factor [-] *)
    rGas_k_Isentropic               : REAL := 1.265;        (* Ratio of Specific Heats (Cp/Cv) [-] *)
    rGas_n_Polytropic               : REAL := 1.345;        (* Polytropic Thermodynamic Compression Exponent [-] *)
    rPolytropicHead_Stg1            : REAL := 0.0;          (* Stage 1 Polytropic Compression Head [kJ/kg] *)
    rPolytropicHead_Stg2            : REAL := 0.0;          (* Stage 2 Polytropic Compression Head [kJ/kg] *)
    rPolytropicHead_Stg3            : REAL := 0.0;          (* Stage 3 Polytropic Compression Head [kJ/kg] *)

    rK_Surge_Stg1                   : REAL := 0.420;        (* Stage 1 Surge Limit Line Parabolic Constant [-] *)
    rK_Surge_Stg2                   : REAL := 0.385;        (* Stage 2 Surge Limit Line Parabolic Constant [-] *)
    rK_Surge_Stg3                   : REAL := 0.350;        (* Stage 3 Surge Limit Line Parabolic Constant [-] *)
    rSurgeLimitDP_Stg1              : REAL := 0.0;          (* Stage 1 Surge Limit Orifice Differential [mbar] *)
    rSurgeLimitDP_Stg2              : REAL := 0.0;          (* Stage 2 Surge Limit Orifice Differential [mbar] *)
    rSurgeLimitDP_Stg3              : REAL := 0.0;          (* Stage 3 Surge Limit Orifice Differential [mbar] *)
    rSurgeMargin_Stg1               : REAL := 1.25;         (* Stage 1 Real-Time Proximity Index [-] *)
    rSurgeMargin_Stg2               : REAL := 1.25;         (* Stage 2 Real-Time Proximity Index [-] *)
    rSurgeMargin_Stg3               : REAL := 1.25;         (* Stage 3 Real-Time Proximity Index [-] *)

    rPDT301_Prev                    : REAL := 120.0;        (* Previous Orifice DP for Derivative Computation [mbar] *)
    rdPDT301_dt                     : REAL := 0.0;          (* Filtered Rate-of-Change of Flow Differential [mbar/s] *)
    rDynamicSurgeBias_Rate          : REAL := 0.0;          (* Dynamic Proactive Surge Bias on Fast Flow Drop [-] *)
    rSurgeMargin_Target             : REAL := 1.120;        (* Active Surge Control Line Safety Setpoint [-] *)

    (* =================================================================================================================
     * SECTION 7: TRIETHYLENE GLYCOL (TEG) ABSORPTION & REGENERATOR BALANCE
     * ================================================================================================================= *)
    rTEG_WaterEquilibriumPpmv       : REAL := 0.0;          (* Contactor Water Vapor Equilibrium Concentration [ppmv] *)
    rTEG_WaterAbsorptionRate        : REAL := 0.0;          (* Instantaneous Water Mass Extracted From Gas [kg/h] *)
    rTEG_ReboilerTargetTemp         : REAL := 204.0;        (* Optimum Glycol Regeneration Temperature [deg C] *)
    rTEG_ReboilerThermalDutyKW      : REAL := 0.0;          (* Calculated Reboiler Heat Input [kW] *)

    (* =================================================================================================================
     * SECTION 8: 14-STAGE DETERMINISTIC PRODUCTION FINITE STATE MACHINE (FSM)
     * ================================================================================================================= *)
    iFSM_State                      : INT := 10;            (* Master State Machine State Identifier (10 - 140) *)
    iFSM_PrevState                  : INT := 10;            (* Previous Scan State Machine State Identifier *)
    rFSM_StateTimer                 : REAL := 0.0;          (* Current Stage Elapsed Execution Dwell Timer [s] *)
    rFSM_SubTimer                   : REAL := 0.0;          (* Auxiliary State Step Sequence Delay Timer [s] *)
    bFSM_TransitionRequested        : BOOL := FALSE;
    iFSM_TargetState                : INT := 10;
    bTrain_Pressurized              : BOOL := FALSE;
    bWarmup_Completed               : BOOL := FALSE;
    bLubeOil_Normal                 : BOOL := FALSE;
    bSealGas_Normal                 : BOOL := FALSE;
    bCompressor_AtIdle              : BOOL := FALSE;
    bCompressor_AtFullSpeed         : BOOL := FALSE;
    bTEG_SystemLocked               : BOOL := FALSE;
    bExport_Synchronized            : BOOL := FALSE;
    bEDP_Active                     : BOOL := FALSE;
    rEDP_RampTimer                  : REAL := 0.0;          (* Emergency Depressurization Blowdown Elapsed Time [s] *)

    (* =================================================================================================================
     * SECTION 9: ISA-18.2 ALARM TRIP POINTS, DEADBANDS & INTERLOCK REGISTERS
     * ================================================================================================================= *)
    (* Suction Pressure PT-101 *)
    rSet_PT101_HH                   : REAL := 32.0;         (* Suction High-High Trip Limit [bar] *)
    rSet_PT101_H                    : REAL := 28.5;         (* Suction High Warning Limit [bar] *)
    rSet_PT101_L                    : REAL := 21.5;         (* Suction Low Warning Limit [bar] *)
    rSet_PT101_LL                   : REAL := 18.0;         (* Suction Low-Low Trip Limit [bar] *)
    rDB_PT101                       : REAL := 0.50;         (* Hysteresis Deadband [bar] *)

    (* Discharge Pressure PT-201 *)
    rSet_PT201_HH                   : REAL := 275.0;        (* Discharge High-High Trip Limit [bar] *)
    rSet_PT201_H                    : REAL := 260.0;        (* Discharge High Warning Limit [bar] *)
    rSet_PT201_L                    : REAL := 220.0;        (* Discharge Low Warning Limit [bar] *)
    rSet_PT201_LL                   : REAL := 180.0;        (* Discharge Low-Low Trip Limit [bar] *)
    rDB_PT201                       : REAL := 3.00;         (* Hysteresis Deadband [bar] *)

    (* Surge Proximity Margins *)
    rSet_Surge_LL                   : REAL := 1.03;         (* Critical Surge Incursion SIL-3 Trip Margin [-] *)
    rSet_Surge_L                    : REAL := 1.10;         (* Low Surge Proximity Control Warning Margin [-] *)
    rDB_Surge                       : REAL := 0.02;         (* Surge Deadband [-] *)

    (* Shaft Radial Vibration VT-401 *)
    rSet_VT401_HH                   : REAL := 95.0;         (* Shaft Vibration High-High Trip Limit [um] *)
    rSet_VT401_H                    : REAL := 65.0;         (* Shaft Vibration High Warning Limit [um] *)
    rDB_VT401                       : REAL := 4.0;          (* Vibration Deadband [um] *)

    (* Export Moisture AT-501 *)
    rSet_AT501_HH                   : REAL := 38.0;         (* Export Moisture Off-Spec Flare Divert Trip [ppmv] *)
    rSet_AT501_H                    : REAL := 28.0;         (* Export Moisture High Warning [ppmv] *)
    rDB_AT501                       : REAL := 1.5;          (* Moisture Deadband [ppmv] *)

    (* Lube Oil Pressure PT-601 *)
    rSet_PT601_LL                   : REAL := 2.20;         (* Lube Oil Pressure Low-Low Mechanical Trip [bar] *)
    rSet_PT601_L                    : REAL := 3.20;         (* Lube Oil Pressure Low Warning / Aux Pump Start [bar] *)
    rDB_PT601                       : REAL := 0.20;         (* Lube Oil Deadband [bar] *)

    (* Seal Gas Differential PDT-701 *)
    rSet_PDT701_LL                  : REAL := 1.80;         (* Seal Gas Primary DP Low-Low Trip [bar] *)
    rSet_PDT701_L                   : REAL := 2.50;         (* Seal Gas Primary DP Low Warning [bar] *)
    rDB_PDT701                      : REAL := 0.15;         (* Seal Gas Deadband [bar] *)

    (* TEG Reboiler Temperature TT-503 *)
    rSet_TT503_HH                   : REAL := 206.5;        (* Reboiler Glycol Thermal Degradation Trip [deg C] *)
    rSet_TT503_H                    : REAL := 205.0;        (* Reboiler High Warning [deg C] *)
    rSet_TT503_L                    : REAL := 195.0;        (* Reboiler Low Warning [deg C] *)
    rSet_TT503_LL                   : REAL := 185.0;        (* Reboiler Low-Low Incomplete Stripping Trip [deg C] *)
    rDB_TT503                       : REAL := 1.0;          (* Reboiler Temp Deadband [deg C] *)

    (* Contactor Foaming Index *)
    rSet_Foam_HH                    : REAL := 2.80;         (* Contactor Severe Foaming Shutdown Trip [-] *)
    rSet_Foam_H                     : REAL := 1.85;         (* Contactor High Foaming Antifoam Injection Warning [-] *)
    rDB_Foam                        : REAL := 0.15;         (* Foaming Deadband [-] *)

    (* Master Latch Flags *)
    bTrip_SuctionPres_HH            : BOOL := FALSE;
    bTrip_SuctionPres_LL            : BOOL := FALSE;
    bTrip_DischargePres_HH          : BOOL := FALSE;
    bTrip_SurgeIncursion            : BOOL := FALSE;
    bTrip_ShaftVibration_HH         : BOOL := FALSE;
    bTrip_ExportMoisture_HH         : BOOL := FALSE;
    bTrip_LubeOil_LL                : BOOL := FALSE;
    bTrip_SealGas_LL                : BOOL := FALSE;
    bTrip_Reboiler_HH               : BOOL := FALSE;
    bTrip_Foam_HH                   : BOOL := FALSE;
    bTrip_TMR_CriticalLoss          : BOOL := FALSE;
    bTrip_EmergencyDepress_Manual   : BOOL := FALSE;

    (* Actuator Slew Filtering States *)
    rASV1_Actual_Filt               : REAL := 100.0;
    rASV2_Actual_Filt               : REAL := 100.0;
    rASV3_Actual_Filt               : REAL := 100.0;
    rVFD_Speed_Actual_Filt          : REAL := 0.0;

    (* Iteration Loop Counters *)
    iLoopRow                        : INT := 1;
    iLoopCol                        : INT := 1;
    iLoopHorizon                    : INT := 1;
    iLoopIter                       : INT := 1;
END_VAR
"""
