# Section 2: VAR_INPUT, VAR_OUTPUT, VAR, and VAR CONSTANT Declarations
def get_sec2_vars():
    return """VAR_INPUT
    (* ============================================================================================================== *)
    (* 1. SUPERVISORY CONTROL & SIL-3 DISCRETE INTERLOCKS                                                             *)
    (* ============================================================================================================== *)
    bEnableSystem                   : BOOL;     (* Master supervisory automation enable command *)
    bEStopTripped                   : BOOL;     (* SIL-3 Emergency Stop safety circuit (Active LOW: FALSE = Tripped) *)
    bResetAlarms                    : BOOL;     (* Operator alarm latch reset and fault acknowledge pushbutton *)
    bAutoModeRequest                : BOOL;     (* Remote DCS automated sequence start request *)
    bEmergencyDepressurizeReq       : BOOL;     (* Remote ESD pipeline emergency depressurization blowdown request *)
    bFastValveKickEnable            : BOOL;     (* Enable open-loop derivative surge kick injection mechanism *)
    bAcousticDampingEnable          : BOOL;     (* Enable active acoustic standing wave pulsation cancellation *)
    bMPCControlEnable               : BOOL;     (* Enable multi-variable state-space Model Predictive Controller *)

    (* ============================================================================================================== *)
    (* 2. TRIPLE MODULAR REDUNDANT (2oo3) PROCESS INSTRUMENTATION                                                    *)
    (* ============================================================================================================== *)
    rSuctionPress_CH1_bar           : REAL;     (* Suction manifold pressure transmitter Channel 1 [bar] *)
    rSuctionPress_CH2_bar           : REAL;     (* Suction manifold pressure transmitter Channel 2 [bar] *)
    rSuctionPress_CH3_bar           : REAL;     (* Suction manifold pressure transmitter Channel 3 [bar] *)

    rDischargePress_CH1_bar         : REAL;     (* Discharge manifold pressure transmitter Channel 1 [bar] *)
    rDischargePress_CH2_bar         : REAL;     (* Discharge manifold pressure transmitter Channel 2 [bar] *)
    rDischargePress_CH3_bar         : REAL;     (* Discharge manifold pressure transmitter Channel 3 [bar] *)

    rSuctionFlowDP_CH1_mbar         : REAL;     (* Suction orifice differential pressure Channel 1 [mbar] *)
    rSuctionFlowDP_CH2_mbar         : REAL;     (* Suction orifice differential pressure Channel 2 [mbar] *)
    rSuctionFlowDP_CH3_mbar         : REAL;     (* Suction orifice differential pressure Channel 3 [mbar] *)

    rSuctionTemp_CH1_K              : REAL;     (* Suction gas temperature RTD Channel 1 [K] *)
    rSuctionTemp_CH2_K              : REAL;     (* Suction gas temperature RTD Channel 2 [K] *)
    rSuctionTemp_CH3_K              : REAL;     (* Suction gas temperature RTD Channel 3 [K] *)

    rDischargeTemp_CH1_K            : REAL;     (* Discharge gas temperature RTD Channel 1 [K] *)
    rDischargeTemp_CH2_K            : REAL;     (* Discharge gas temperature RTD Channel 2 [K] *)
    rDischargeTemp_CH3_K            : REAL;     (* Discharge gas temperature RTD Channel 3 [K] *)

    rShaftSpeed_CH1_rpm             : REAL;     (* Turbocompressor rotor speed magnetic pickup Channel 1 [rpm] *)
    rShaftSpeed_CH2_rpm             : REAL;     (* Turbocompressor rotor speed magnetic pickup Channel 2 [rpm] *)
    rShaftSpeed_CH3_rpm             : REAL;     (* Turbocompressor rotor speed magnetic pickup Channel 3 [rpm] *)

    (* ============================================================================================================== *)
    (* 3. PROCESS GAS COMPOSITION, DRIVER & ELECTRICAL METRICS                                                       *)
    (* ============================================================================================================== *)
    rVolumetricFlow_Nm3h            : REAL;     (* Suction ultrasonic fiscal metering volumetric flow rate [Nm3/h] *)
    rDriverPower_kW                 : REAL;     (* 24 MW High-speed VFD electric motor active electrical power [kW] *)
    rDriverCurrent_A                : REAL;     (* Electric motor stator phase current measurement [A] *)
    rGasMolecularWeight_gmol        : REAL;     (* Online process gas chromatograph measured molecular weight [g/mol] *)
    rGasPurityH2_pct                : REAL;     (* Real-time thermal conductivity hydrogen purity percentage [%] *)
    rGasSpecificHeatRatio           : REAL;     (* Real-time gas specific heat ratio gamma (Cp/Cv) [-] *)

    (* ============================================================================================================== *)
    (* 4. ROTOR DYNAMICS & MECHANICAL SHAFT PROXIMITY SENSORS                                                         *)
    (* ============================================================================================================== *)
    rVibrationRadialDE_X_mms        : REAL;     (* Drive-end radial bearing eddy-current proximity probe X-axis [mm/s] *)
    rVibrationRadialDE_Y_mms        : REAL;     (* Drive-end radial bearing eddy-current proximity probe Y-axis [mm/s] *)
    rVibrationRadialNDE_X_mms       : REAL;     (* Non-drive-end radial bearing proximity probe X-axis [mm/s] *)
    rVibrationRadialNDE_Y_mms       : REAL;     (* Non-drive-end radial bearing proximity probe Y-axis [mm/s] *)
    rShaftAxialThrust_um            : REAL;     (* Active magnetic thrust bearing rotor axial displacement [um] *)
    rBearingMetalTempMax_K          : REAL;     (* Active magnetic bearing coil / radial backup bearing max temp [K] *)

    (* ============================================================================================================== *)
    (* 5. DRY GAS SEAL (DGS) & VACUUM EXTRACTION SUBSYSTEM                                                           *)
    (* ============================================================================================================== *)
    rSealGasSupplyPress_bar         : REAL;     (* Conditioned primary H2 seal gas supply manifold pressure [bar] *)
    rPrimaryVentPress_mbar          : REAL;     (* Primary seal vent collection cavity dynamic pressure [mbar gauge] *)
    rSecondaryVentPress_mbar        : REAL;     (* Secondary seal vent collection cavity dynamic pressure [mbar gauge] *)
    rPrimarySealLeakage_Nm3h        : REAL;     (* Primary seal dynamic face leakage flow meter [Nm3/h] *)
    rSecondarySealLeakage_Nm3h      : REAL;     (* Secondary seal dynamic face leakage flow meter [Nm3/h] *)
    rBufferN2SupplyPress_bar        : REAL;     (* Secondary seal pure nitrogen buffer barrier supply pressure [bar] *)
    rSealVentH2Concentration_LEL    : REAL;     (* Seal vent exhaust duct optical/catalytic H2 concentration [% LEL] *)
    rSealFaceTempDE_K               : REAL;     (* Drive-end stationary silicon-carbide seal face temperature [K] *)
    rSealFaceTempNDE_K              : REAL;     (* Non-drive-end stationary silicon-carbide seal face temperature [K] *)
    rVacuumEjectorMotivePress_bar   : REAL;     (* Motive pure N2 supply pressure to vent vacuum ejector [bar] *)

    (* ============================================================================================================== *)
    (* 6. PIPELINE ACOUSTIC WAVE DYNAMICS & ENVIRONMENTAL BOUNDARIES                                                  *)
    (* ============================================================================================================== *)
    rAcousticDynamicPress_CH1_bar   : REAL;     (* Suction dynamic piezo-electric acoustic pulsation probe [bar] *)
    rAcousticDynamicPress_CH2_bar   : REAL;     (* Discharge dynamic piezo-electric acoustic pulsation probe [bar] *)
    rDischargeHeaderPress_bar       : REAL;     (* Transcontinental downstream 100 bar pipeline header backpressure [bar] *)
    rAmbientTemp_K                  : REAL;     (* Compressor acoustic enclosure interior ambient temperature [K] *)
    rCycleTime_s                    : REAL;     (* Controller discrete execution cycle time interval [s] *)
END_VAR

VAR_OUTPUT
    (* ============================================================================================================== *)
    (* 1. SIL-3 TRIP SIGNALS & DISCRETE VALVE CONTROLS                                                               *)
    (* ============================================================================================================== *)
    bCompressorTrip                 : BOOL;     (* Master SIL-3 emergency shutdown trip signal to safety isolation *)
    bAntiSurgeValveFullOpen         : BOOL;     (* Emergency de-energize fast-dump solenoid valve output *)
    bSystemReady                    : BOOL;     (* Compressor system healthy, pressurized and ready to run *)
    bMPCActive                      : BOOL;     (* Advanced multivariable state-space MPC active and in control *)
    bDegradedSensorMode             : BOOL;     (* Sensor voting running under degraded 1oo2 or 1oo1 backup *)
    bAcousticDampingEngaged         : BOOL;     (* Active acoustic wave standing wave pulsation dither active *)
    bFastValveKickActive            : BOOL;     (* Fast open-loop rate-of-approach surge kick currently firing *)
    bSealVacuumHealthy              : BOOL;     (* Dry gas seal primary vent cavity depression within safe envelope *)

    (* ============================================================================================================== *)
    (* 2. CONTINUOUS ANALOG MODULATION COMMANDS                                                                       *)
    (* ============================================================================================================== *)
    rAntiSurgeValveCmd_pct          : REAL;     (* Modulating anti-surge recycle valve actuator demand [0.0 - 100.0 %] *)
    rVacuumExtractionValveCmd_pct   : REAL;     (* Dry gas seal primary vent vacuum extraction valve demand [0.0 - 100.0 %] *)
    rSpeedReference_rpm             : REAL;     (* 24 MW VFD electric drive shaft speed reference [rpm] *)
    rBlowdownValveCmd_pct           : REAL;     (* Emergency flare depressurization blowdown valve command [0.0 - 100.0 %] *)

    (* ============================================================================================================== *)
    (* 3. REAL-TIME THERMODYNAMIC & AERODYNAMIC ANALYTICS                                                            *)
    (* ============================================================================================================== *)
    rPolytropicHead_kJkg            : REAL;     (* Instantaneous calculated gas polytropic head [kJ/kg] *)
    rCompressionRatio               : REAL;     (* Total compression ratio P_disch / P_suct [-] *)
    rSurgeMargin_pct                : REAL;     (* Instantaneous normalized aerodynamic surge safety margin [%] *)
    rDistanceToSCL_pct              : REAL;     (* Operating point distance to dynamic Surge Control Line [%] *)
    rRateOfApproachToSurge_pct_s    : REAL;     (* Time rate-of-change of surge margin dSigma/dt [%/s] *)
    rPolytropicEfficiency_pct       : REAL;     (* Real-time evaluated turbocompressor polytropic efficiency [%] *)
    rSpeedOfSound_ms                : REAL;     (* Calculated sonic velocity in hydrogen gas mixture [m/s] *)
    rGasDensitySuction_kgm3         : REAL;     (* Calculated gas mass density at compressor suction [kg/m3] *)
    rAcousticPulsationRMS_mbar      : REAL;     (* Root-mean-square dynamic pressure acoustic pulsation [mbar] *)
    rPrimarySealDP_bar              : REAL;     (* Primary seal gas differential pressure over suction [bar] *)

    (* ============================================================================================================== *)
    (* 4. SEQUENCE STATUS & MULTI-TIER DIAGNOSTIC ALARM WORDS                                                        *)
    (* ============================================================================================================== *)
    wCompressorState                : WORD;     (* Active finite state machine sequence operational state index *)
    dwAlarmWord1                    : DWORD;    (* SIL-3 Critical Emergency Shutdown trip bitfield 1 *)
    dwAlarmWord2                    : DWORD;    (* Thermodynamic and process operating boundary trip bitfield 2 *)
    dwAlarmWord3                    : DWORD;    (* Dry gas seal and auxiliary subsystem trip bitfield 3 *)
    dwWarningWord1                  : DWORD;    (* Aerodynamic pre-surge and process warning bitfield 1 *)
    dwWarningWord2                  : DWORD;    (* Instrumentation discrepancy and sensor degradation warning bitfield 2 *)
    uiSurgeCycleCount               : UINT;     (* Cumulative detected surge cycle counter within rolling 60s *)
END_VAR

VAR
    (* ============================================================================================================== *)
    (* INTERNAL CYBER-PHYSICAL STATE, DISCRETE MATRICES & VOTING STRUCTURES                                          *)
    (* ============================================================================================================== *)
    (* Execution Delta Time & Watchdogs *)
    rDt                             : REAL := 0.005; (* Clamped cycle execution interval [s] *)
    diScanCounter                   : DINT := 0;     (* Scan execution iteration counter *)

    (* Voted Process Variables *)
    rSuctPress_Voted_bar            : REAL := 50.0;
    rDischPress_Voted_bar           : REAL := 100.0;
    rFlowDP_Voted_mbar              : REAL := 120.0;
    rSuctTemp_Voted_K               : REAL := 300.0;
    rDischTemp_Voted_K              : REAL := 355.0;
    rShaftSpeed_Voted_rpm           : REAL := 0.0;

    (* Previous Cycle Variables for Numerical Differentiators *)
    rPrevSurgeMargin_pct            : REAL := 25.0;
    rPrevShaftSpeed_rpm             : REAL := 0.0;
    rPrevSuctPress_bar              : REAL := 50.0;
    rPrevDischPress_bar             : REAL := 100.0;
    rPrevFlowDP_mbar                : REAL := 120.0;
    rPrevASVPosition_pct            : REAL := 100.0;

    (* 2oo3 Sensor Voting Diagnostics Arrays and Timers *)
    arrSuctPress_Raw                : ARRAY[1..3] OF REAL;
    arrDischPress_Raw               : ARRAY[1..3] OF REAL;
    arrFlowDP_Raw                   : ARRAY[1..3] OF REAL;
    arrSuctTemp_Raw                 : ARRAY[1..3] OF REAL;
    arrDischTemp_Raw                : ARRAY[1..3] OF REAL;
    arrSpeed_Raw                    : ARRAY[1..3] OF REAL;

    arrSuctPress_Health             : ARRAY[1..3] OF BOOL := [TRUE, TRUE, TRUE];
    arrDischPress_Health            : ARRAY[1..3] OF BOOL := [TRUE, TRUE, TRUE];
    arrFlowDP_Health                : ARRAY[1..3] OF BOOL := [TRUE, TRUE, TRUE];
    arrSuctTemp_Health              : ARRAY[1..3] OF BOOL := [TRUE, TRUE, TRUE];
    arrDischTemp_Health             : ARRAY[1..3] OF BOOL := [TRUE, TRUE, TRUE];
    arrSpeed_Health                 : ARRAY[1..3] OF BOOL := [TRUE, TRUE, TRUE];

    arrSuctPress_FrozenCount        : ARRAY[1..3] OF INT := [0, 0, 0];
    arrDischPress_FrozenCount       : ARRAY[1..3] OF INT := [0, 0, 0];
    arrFlowDP_FrozenCount           : ARRAY[1..3] OF INT := [0, 0, 0];
    arrSpeed_FrozenCount            : ARRAY[1..3] OF INT := [0, 0, 0];

    (* Gas Thermodynamics and Equation of State (EOS) *)
    rZ_Suct                         : REAL := 1.025;
    rZ_Disch                        : REAL := 1.058;
    rZ_Avg                          : REAL := 1.042;
    rGasConstant_Rspec              : REAL := 4124.48;
    rGamma                          : REAL := 1.405;
    rPolytropicExponent_n           : REAL := 1.542;
    rPolytropicFactor_m             : REAL := 0.3515; (* (n-1)/n *)
    rReducedFlow_Squared            : REAL := 0.0;
    rMassFlow_kgs                   : REAL := 0.0;
    rActualVolumetricFlow_m3s       : REAL := 0.0;

    (* Dynamic Anti-Surge Curves & Coordinates *)
    rFlowSquared_SLL                : REAL := 0.0;
    rFlowSquared_SCL                : REAL := 0.0;
    rFlowSquared_SBL                : REAL := 0.0;
    rFlowSquared_SKL                : REAL := 0.0;
    rDynamicSafetyMargin_pct        : REAL := 12.0;
    rRateOfApproachBias_pct         : REAL := 0.0;
    rMolecularWeightShiftBias_pct   : REAL := 0.0;
    rAccelerationBias_pct           : REAL := 0.0;
    rAcousticPulsationBias_pct      : REAL := 0.0;
    rValveKickBias_pct              : REAL := 0.0;
    rValveKickDecay                 : REAL := 0.96;

    (* 5x5 State-Space System Representation *)
    (* State vector: x = [ Delta_Flow(kg/s), Delta_P_disch(bar), Delta_P_suct(bar), Delta_Speed(rpm), Delta_P_ac(mbar) ]^T *)
    arrStateX                       : ARRAY[1..5] OF REAL := [0.0, 0.0, 0.0, 0.0, 0.0];
    arrNextStateX                   : ARRAY[1..5] OF REAL := [0.0, 0.0, 0.0, 0.0, 0.0];
    arrInputU                       : ARRAY[1..3] OF REAL := [0.0, 0.0, 0.0];
    arrOutputY                      : ARRAY[1..4] OF REAL := [0.0, 0.0, 0.0, 0.0];
    arrOutputSP                     : ARRAY[1..4] OF REAL := [15.0, 2.0, 4.5, 0.0]; (* Desired Surge Margin, Rc, Seal DP, Min Acoustic *)

    (* Discrete State-Space Matrices A_d (5x5), B_d (5x3), C_d (4x5), D_d (4x3) *)
    arrMatA                         : ARRAY[1..5, 1..5] OF REAL;
    arrMatB                         : ARRAY[1..5, 1..3] OF REAL;
    arrMatC                         : ARRAY[1..4, 1..5] OF REAL;
    arrMatD                         : ARRAY[1..4, 1..3] OF REAL;

    (* Model Predictive Control (MPC) Optimization Matrices & Buffers *)
    arrWeightQ                      : ARRAY[1..4] OF REAL := [18.0, 6.0, 10.0, 14.0]; (* Output penalties *)
    arrWeightR                      : ARRAY[1..3] OF REAL := [0.75, 1.25, 0.50];     (* Actuator rate penalties *)
    arrDeltaU_Opt                   : ARRAY[1..3] OF REAL := [0.0, 0.0, 0.0];
    arrPredictedY                   : ARRAY[1..5, 1..4] OF REAL;                     (* Horizon N_p=5 predicted outputs *)
    arrGradientG                    : ARRAY[1..3] OF REAL := [0.0, 0.0, 0.0];
    rMpcStepAlpha                   : REAL := 0.045;
    bMpcIllConditioned              : BOOL := FALSE;

    (* Decoupled Backup PID Anti-Surge Controller *)
    rASV_PID_Integral               : REAL := 0.0;
    rASV_PID_Derivative             : REAL := 0.0;
    rASV_PID_PrevError              : REAL := 0.0;
    rASV_PID_Output                 : REAL := 100.0;

    (* Acoustic Pulsation 2nd-Order Butterworth Digital Bandpass Filter *)
    (* Center frequency approx 215 Hz, bandwidth 120 - 350 Hz, sampling rate 200 Hz / oversampled *)
    rAcousticInput_mbar             : REAL := 0.0;
    rAcousticFilt_X0                : REAL := 0.0;
    rAcousticFilt_X1                : REAL := 0.0;
    rAcousticFilt_X2                : REAL := 0.0;
    rAcousticFilt_Y0                : REAL := 0.0;
    rAcousticFilt_Y1                : REAL := 0.0;
    rAcousticFilt_Y2                : REAL := 0.0;
    arrAcousticHistory              : ARRAY[1..100] OF REAL;
    iAcousticHistIndex              : INT := 1;
    rAcousticSumSquares             : REAL := 0.0;
    rAcousticPhaseLeadOutput        : REAL := 0.0;
    rAcousticDitherModulation       : REAL := 0.0;

    (* Dry Gas Seal Vacuum Extraction PID Controller *)
    rVac_PID_Error                  : REAL := 0.0;
    rVac_PID_Integral               : REAL := 25.0;
    rVac_PID_Derivative             : REAL := 0.0;
    rVac_PID_PrevError              : REAL := 0.0;
    rVacExtractionValveRaw_pct      : REAL := 35.0;

    (* Operational Finite State Machine State & Timers *)
    iState                          : INT := 0;      (* Internal sequence state *)
    iPrevState                      : INT := -1;
    tStateTimer                     : TON;
    tPurgeTimer                     : TON;
    tWarmupTimer                    : TON;
    tSurgeCycleTimer                : TON;
    tDecelTimer                     : TON;
    tDepressurizeTimer              : TON;
    tDiscrepancyTimer               : TON;

    (* Surge Cycle Accumulation within Sliding Window *)
    bSurgeCycleLatched              : BOOL := FALSE;
    rSurgeCycleWindowTime_s         : REAL := 0.0;

    (* Actuator Slew Rate Limiters *)
    rAntiSurgeValveActual_pct       : REAL := 100.0;
    rSpeedRefActual_rpm             : REAL := 0.0;
    rVacValveActual_pct             : REAL := 0.0;
END_VAR

VAR CONSTANT
    (* ============================================================================================================== *)
    (* PHYSICAL, THERMODYNAMIC, GEOMETRIC & TUNING CONSTANTS                                                         *)
    (* ============================================================================================================== *)
    c_rUniversalGasConstant         : REAL := 8314.462; (* Universal gas constant R_u [J/(kmol*K)] *)
    c_rNominalMolecularWeight_H2    : REAL := 2.01588;  (* Nominal molecular weight of pure H2 [g/mol] *)
    c_rMaxAllowableMW_Deviation     : REAL := 0.50;     (* Max tolerable MW shift before shutdown [g/mol] *)
    c_rDesignSuctionPressure_bar    : REAL := 50.0;     (* Nominal suction header pressure [bar] *)
    c_rDesignDischargePressure_bar  : REAL := 100.0;    (* Nominal pipeline discharge pressure [bar] *)
    c_rMaxDischargePressure_bar     : REAL := 115.0;    (* Maximum allowable operating pressure MAOP [bar] *)
    c_rMinSuctionPressure_bar       : REAL := 32.0;     (* Minimum suction pressure trip limit [bar] *)

    (* Centrifugal Impeller Aerodynamic Surge Line Coefficients *)
    (* Head = K0 + K1*Flow^2 in reduced coordinates *)
    c_rSLL_K0                       : REAL := 185.0;    (* SLL zero-flow polytropic head intercept [kJ/kg] *)
    c_rSLL_K2                       : REAL := -0.0042;  (* SLL parabolic curvature coefficient *)
    c_rBaseSurgeMargin_pct          : REAL := 12.0;     (* Baseline steady-state surge safety margin [%] *)
    c_rBackupSurgeMargin_pct        : REAL := 6.0;      (* Surge Backup Line (SBL) margin [%] *)
    c_rSolenoidTripMargin_pct       : REAL := 2.0;      (* Solenoid Kick Line (SKL) trip margin [%] *)

    (* Acoustic Resonator & IIR Bandpass Filter Coefficients *)
    (* Discretized 2nd-order Butterworth: center = 215 Hz, Q = 3.5 *)
    c_rIIR_b0                       : REAL := 0.1826;
    c_rIIR_b1                       : REAL := 0.0000;
    c_rIIR_b2                       : REAL := -0.1826;
    c_rIIR_a1                       : REAL := -1.3412;
    c_rIIR_a2                       : REAL := 0.6348;
    c_rAcousticPhaseLeadGain        : REAL := 0.0018;   (* Phase lead sensitivity gain [%/mbar] *)
    c_rAcousticDitherMaxClamp_pct   : REAL := 2.50;     (* Maximum allowable micro-dither amplitude [%] *)

    (* Dry Gas Seal Safety Boundaries *)
    c_rMinPrimarySealDP_bar         : REAL := 3.50;     (* Minimum primary seal gas DP over suction [bar] *)
    c_rCriticalLowSealDP_bar        : REAL := 2.00;     (* SIL-3 Critical seal DP trip threshold [bar] *)
    c_rVacSetpoint_mbar             : REAL := -80.0;    (* Primary vent sub-atmospheric setpoint [mbar gauge] *)
    c_rMaxPrimaryVentPress_mbar     : REAL := 800.0;    (* Primary vent high warning limit [mbar gauge] *)
    c_rTripPrimaryVentPress_mbar    : REAL := 1500.0;   (* Primary vent SIL-3 trip limit [mbar gauge] *)
    c_rMaxPrimaryLeakage_Nm3h       : REAL := 12.0;     (* Primary leakage high warning [Nm3/h] *)
    c_rTripPrimaryLeakage_Nm3h      : REAL := 25.0;     (* Primary leakage SIL-3 trip [Nm3/h] *)
    c_rTripH2Concentration_LEL      : REAL := 50.0;     (* Vent duct hydrogen concentration trip [% LEL] *)

    (* Actuator Slew Rates *)
    c_rASV_MaxOpenRate_pct_s        : REAL := 300.0;    (* Anti-surge fast opening stroke rate [%/s] *)
    c_rASV_MaxCloseRate_pct_s       : REAL := 20.0;     (* Anti-surge slow closing stroke rate [%/s] *)
    c_rSpeed_MaxRampRate_rpm_s      : REAL := 250.0;    (* Motor speed acceleration/deceleration ramp [rpm/s] *)
END_VAR
"""
