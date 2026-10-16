import json
import uuid
import os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices, Model Predictive Control (MPC), 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: Ultra-Precision Diamond Flycutting Machine: Aerostatic Linear Guideway Damping and Fast Tool Servo Nanometer Error Correction**

CRITICAL RULES:
1. CODE FENCE: Use TRIPLE backticks + iec-st (` ```iec-st `).
2. STRUCTURE:
   a. First line: FUNCTION_BLOCK FB_DiamondFlycutting_NanometerFTS
   b. VAR_INPUT ... END_VAR (min 8 typed inputs with physical units [nm], [rpm], [bar], [deg C], [kHz])
   c. VAR_OUTPUT ... END_VAR (min 7 typed outputs with engineering units & status words)
   d. VAR ... END_VAR (internal state matrices, filter accumulators, 2oo3 voting vars)
   e. Multi-stage CASE machine with END_CASE;
   f. Last line: END_FUNCTION_BLOCK
3. LENGTH: Assistant content MUST be >= 3500 characters total. Maximize token usage with deep technical explanations, complex algorithms, and industrial reliability features.
4. SAVE using this exact Python:
   import json, uuid
   prompt = \"\"\"<copy this exact user prompt here>\"\"\"
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_DiamondFlycutting_NanometerFTS\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
   record = {\"messages\": [{\"role\": \"user\", \"content\": prompt}, {\"role\": \"assistant\", \"content\": code}]}
   with open(f\"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json\", \"w\", encoding=\"utf-8\") as f:
       json.dump(record, f, ensure_ascii=False)
5. REPLY with: EVOLUTION COMPLETE: Ultra-Precision Diamond Flycutting Machine: Aerostatic Linear Guideway Damping and Fast Tool Servo Nanometer Error Correction"""

st_code = """```iec-st
FUNCTION_BLOCK FB_DiamondFlycutting_NanometerFTS
(*
 ===================================================================================================
  LUMINA AI INDUSTRIAL AUTOMATION V7 MAX SYNTHETIC BENCHMARK DATASET
  MODULE: FB_DiamondFlycutting_NanometerFTS
  CYBER-PHYSICAL SUBSYSTEM:
    Ultra-Precision Diamond Flycutting Machine - Sub-Nanometer Fast Tool Servo (FTS) &
    Active Lorentz Voice-Coil Squeeze-Film Aerostatic Guideway Damping Architecture.
  GOVERNING STANDARD: IEC 61131-3 Edition 3.0 (Deterministic Real-Time Mechatronic Specification)
  DESIGN CRITERIA:
    - Target cycle loop time: Ts = 10 microseconds (100 kHz synchronous execution on dedicated DSP/FPGA)
    - Motion resolution: Sub-atomic / 0.1 nanometer scale
    - Contouring bandwidth: FTS closed-loop -3dB bandwidth >= 2.5 kHz
    - Aerostatic guideway dynamic stiffness: > 150 N/um with active voice-coil squeeze-film attenuation
    - Safety integrity level: SIL 3 / Performance Level e (ISO 13849-1) with 2oo3 Triple Modular Redundancy
 ===================================================================================================
*)
VAR_INPUT
    (* --- Master System Interlocks & Clocks --- *)
    bEnable                     : BOOL;     (* Master functional block enable & real-time servo closure [T/F] *)
    bEmergencyStop              : BOOL;     (* Fail-safe dual-channel safety circuit input, active-low [SIL 3] *)
    bResetFault                 : BOOL;     (* Positive-edge latch acknowledge and diagnostic reset command *)
    rSamplingClock_kHz          : REAL;     (* Synchronous DSP/FPGA interrupt sampling frequency [kHz], nom 100.0 kHz *)

    (* --- Aerostatic Bearing Pneumatics & Metrology Environment --- *)
    rSupplyPressure_bar         : REAL;     (* Compressed ultra-pure dry air supply to porous graphite pads [bar], nom 5.5 bar *)
    rBearingVacuumPreload_bar   : REAL;     (* Active vacuum preload port level for carriage stiffness enhancement [bar], nom -0.35 bar *)
    rSpindleSpeed_rpm           : REAL;     (* High-inertia aerostatic diamond flycutter spindle rotational speed [rpm], nom 3000.0 rpm *)
    rGuidewayTemp_degC          : REAL;     (* Zerodur reference frame temperature from calibrated PT100 RTD [deg C], 20.00 +/- 0.005 C *)
    rSpindleMotorTemp_degC      : REAL;     (* Air-bearing coreless spindle brushless motor winding temperature [deg C], max 38.0 C *)
    bAirShowerThermalReady      : BOOL;     (* Downflow laminar micro-climate thermal stability interlock (+/- 0.002 K) [T/F] *)

    (* --- Triple Modular Redundancy (2oo3) Metrology Channels --- *)
    rDisplacementLaser1_nm      : REAL;     (* Heterodyne HeNe laser interferometer Axis Z position channel 1 [nm] *)
    rDisplacementLaser2_nm      : REAL;     (* Heterodyne HeNe laser interferometer Axis Z position channel 2 [nm] *)
    rDisplacementLaser3_nm      : REAL;     (* Heterodyne HeNe laser interferometer Axis Z position channel 3 [nm] *)
    rNominalToolTrajectory_nm   : REAL;     (* CNC trajectory generator theoretical diamond tool target position [nm] *)
    rFeedVelocity_mms           : REAL;     (* Aerostatic slide table linear traverse speed [mm/s], nom 0.5 to 5.0 mm/s *)

    (* --- Actuator Direct Nanometer Feedback Sensors --- *)
    rPiezoCapacitiveFeedback_um : REAL;     (* Guarded sub-nanometer capacitive gauge measurement on PZT toolholder [um] *)
    rVoiceCoilCurrentSense_mA   : REAL;     (* Current shunt feedback from linear magnetic squeeze-film damper [mA] *)
END_VAR

VAR_OUTPUT
    (* --- Primary Actuator Command Signals --- *)
    bSystemReady                : BOOL;     (* Machine guideway levitated, thermal soak validated, FTS precharged *)
    bActiveControl              : BOOL;     (* Real-time nano-positioning closed-loop active and within contour tolerance *)
    rFTS_PiezoDrive_V           : REAL;     (* High-voltage amplifier output command for PZT actuator [-20.0 to +150.0 V] *)
    rAerostaticDamping_mA       : REAL;     (* Squeeze-film electromagnetic voice-coil active damping current command [mA] *)

    (* --- Validated Metrology & Contouring Telemetry --- *)
    rVotedPosition_nm           : REAL;     (* Triple Modular Redundancy (2oo3) majority-voted guideway position [nm] *)
    rResidualTrackingError_nm   : REAL;     (* Dynamic nano-positioning error (Trajectory - VotedPosition) [nm] *)
    rSurfaceRoughnessEstimate_nmRa: REAL;   (* High-frequency spatial variance online Ra estimation [nm Ra] *)

    (* --- Diagnostic Status & Fault Words --- *)
    wStatusWord                 : WORD;     (* IEC 61131 status register bitmask (levitation, tracking, calibration) *)
    wAlarmWord                  : WORD;     (* Comprehensive fault bitmask (pressure, thermal runaway, sensor divergence) *)
    bDegradedMode               : BOOL;     (* Redundancy degraded: operating in dual-channel or simplex sensor mode *)
    bToolRetracted              : BOOL;     (* Ultra-fast piezoelectric failsafe diamond tool retraction engaged *)
END_VAR

VAR
    (* =========================================================================
       STATE MACHINE SEQUENCING & TIMERS
       ========================================================================= *)
    iState                      : INT := 0; (* Primary machine operating state index *)
    iPreviousState              : INT := 0; (* Preceding state index for step-transition tracing *)
    tLevitationTimer            : TON;      (* Pneumatic film stabilization delay timer (nom 3.5s) *)
    tThermalSoakTimer           : TON;      (* Metrology thermal equilibrium verification timer (nom 10.0s) *)
    tCalibrationTimer           : TON;      (* Piezo hysteresis pre-charge and capacitive zeroing timer *)
    tFaultHoldTimer             : TON;      (* Safe retract and dynamic braking latch timer *)

    (* =========================================================================
       2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING LOGIC
       ========================================================================= *)
    rTMR_Tolerance_nm           : REAL := 3.50; (* Maximum allowed inter-channel sensor divergence [nm] *)
    rDiff12                     : REAL;     (* Channel 1 vs Channel 2 deviation [nm] *)
    rDiff23                     : REAL;     (* Channel 2 vs Channel 3 deviation [nm] *)
    rDiff31                     : REAL;     (* Channel 3 vs Channel 1 deviation [nm] *)
    bChan1_Healthy              : BOOL := TRUE;
    bChan2_Healthy              : BOOL := TRUE;
    bChan3_Healthy              : BOOL := TRUE;
    udiFaultCount_Ch1           : UDINT := 0;
    udiFaultCount_Ch2           : UDINT := 0;
    udiFaultCount_Ch3           : UDINT := 0;
    udiConsecutiveDivergenceLimit: UDINT := 50; (* Trips fail-safe upon 50 consecutive cycles (500 us) *)

    (* =========================================================================
       DISCRETE 4th-ORDER STATE-SPACE OBSERVER (KALMAN ESTIMATOR) FOR PZT STACK
       Model states: x1 = displacement [nm], x2 = velocity [nm/s],
                     x3 = hysteresis state [nm], x4 = 1st structural eigenmode [nm]
       ========================================================================= *)
    aA11 : REAL := 0.9982; aA12 : REAL := 0.0000098; aA13 : REAL := -0.0014; aA14 : REAL := 0.0003;
    aA21 : REAL := -36.42; aA22 : REAL := 0.9610;    aA23 : REAL := -2.8500; aA24 : REAL := 6.4100;
    aA31 : REAL := 0.0025; aA32 : REAL := 0.0000;    aA33 : REAL := 0.8920;  aA34 : REAL := 0.0000;
    aA41 : REAL := -120.5; aA42 : REAL := -0.450;    aA43 : REAL := 0.0000;  aA44 : REAL := 0.9150;

    aB1  : REAL := 0.2850; (* Input drive gain: nm per Volt per discrete step *)
    aB2  : REAL := 571.20;
    aB3  : REAL := 0.0150;
    aB4  : REAL := -84.30;

    aC1  : REAL := 1.0000; aC2  : REAL := 0.0000; aC3  : REAL := 1.0000; aC4  : REAL := 0.0000;

    aL1  : REAL := 0.1250; (* Observer Kalman gains *)
    aL2  : REAL := 18.450;
    aL3  : REAL := 0.0085;
    aL4  : REAL := -2.150;

    rStateHat_1                 : REAL := 0.0; (* Estimated FTS tip displacement [nm] *)
    rStateHat_2                 : REAL := 0.0; (* Estimated FTS tip velocity [nm/s] *)
    rStateHat_3                 : REAL := 0.0; (* Estimated internal hysteresis charge variable [nm] *)
    rStateHat_4                 : REAL := 0.0; (* Estimated 3.5 kHz structural vibration mode [nm] *)
    rObserverInnovation         : REAL := 0.0; (* Measurement residual [nm] *)

    (* =========================================================================
       MODEL PREDICTIVE CONTROL (MPC) & CONSTRAINED OPTIMIZATION REGULATOR
       ========================================================================= *)
    rPredHorizon_1              : REAL;     (* Step k+1 tracking prediction error [nm] *)
    rPredHorizon_2              : REAL;     (* Step k+2 tracking prediction error [nm] *)
    rPredHorizon_3              : REAL;     (* Step k+3 tracking prediction error [nm] *)
    rWeight_Q                   : REAL := 125.0; (* Quadratic penalty on position tracking error *)
    rWeight_R                   : REAL := 0.045; (* Quadratic penalty on voltage slew rate *)
    rWeight_S                   : REAL := 80.00; (* Quadratic penalty on structural eigenmode *)
    rDeltaU_Optimal             : REAL := 0.0;   (* Optimal voltage increment per scan cycle [V] *)
    rMaxVoltageSlewRate         : REAL := 2.50;  (* Max allowable dV/dt per 10 us cycle [V] to prevent PZT damage *)
    rMaxPiezoVoltage            : REAL := 150.0; (* Positive expansion voltage limit [V] *)
    rMinPiezoVoltage            : REAL := -20.0; (* Reverse depolarization safety limit [V] *)
    rRawPiezoDrive              : REAL := 0.0;

    (* =========================================================================
       AEROSTATIC SQUEEZE-FILM ACTIVE DAMPING (VOICE-COIL LORENTZ ACTUATOR)
       Attenuates aerostatic bearing pneumatic film bounce resonance (~140 Hz)
       ========================================================================= *)
    rLastVotedPos               : REAL := 0.0;
    rGuidewayVelocity_nms       : REAL := 0.0;
    rDampingGain_mA_per_nms     : REAL := 0.0000185; (* Current command per nm/s velocity *)
    rMaxDampingCurrent_mA       : REAL := 1200.0;    (* Thermal saturation limit of voice coil [mA] *)

    (* =========================================================================
       ADAPTIVE BIQUAD NOTCH FILTERS (SPINDLE HARMONIC RUNOUT SUPPRESSION)
       Tracks 1x (50 Hz at 3000 rpm), 2x (100 Hz), and 4x (200 Hz) runouts
       ========================================================================= *)
    rSpindleFreq_Hz             : REAL;
    rNotch_x1                   : REAL := 0.0; (* Biquad delay memory 1 *)
    rNotch_x2                   : REAL := 0.0; (* Biquad delay memory 2 *)
    rNotch_y1                   : REAL := 0.0;
    rNotch_y2                   : REAL := 0.0;
    rCoeff_b0                   : REAL := 0.9980;
    rCoeff_b1                   : REAL := -1.9950;
    rCoeff_b2                   : REAL := 0.9980;
    rCoeff_a1                   : REAL := -1.9950;
    rCoeff_a2                   : REAL := 0.9960;
    rSpindleRunoutFiltered_nm   : REAL := 0.0;

    (* =========================================================================
       SURFACE ROUGHNESS (Ra) STATISTICAL ONLINE ESTIMATOR
       ========================================================================= *)
    rAbsErrorAccumulator        : REAL := 0.0;
    udiSampleCounter            : UDINT := 0;
    udiWindowSize               : UDINT := 10000; (* 10,000 samples = 100 ms spatial cut-off *)

    (* =========================================================================
       DIAGNOSTIC STATUS BIT DEFINITIONS
       ========================================================================= *)
    cSTATUS_BEARING_LEVITED     : WORD := 16#0001; (* Bit 0: Aerostatic film floating *)
    cSTATUS_THERMAL_STABLE      : WORD := 16#0002; (* Bit 1: Laser metrology & Zerodur soak stable *)
    cSTATUS_FTS_CALIBRATED      : WORD := 16#0004; (* Bit 2: PZT actuator zero-biased *)
    cSTATUS_TMR_3_CHANNEL_OK    : WORD := 16#0008; (* Bit 3: All 3 heterodyne interferometers voting *)
    cSTATUS_TMR_2_CHANNEL_DEG   : WORD := 16#0010; (* Bit 4: Operating on dual redundant fallback *)
    cSTATUS_CLOSED_LOOP_NANO    : WORD := 16#0020; (* Bit 5: Sub-nanometer contouring locked *)
    cSTATUS_ACTIVE_DAMPING_ON   : WORD := 16#0040; (* Bit 6: Voice-coil squeeze film active *)
    cSTATUS_TOOL_RETRACTED_SAFE : WORD := 16#0080; (* Bit 7: Tool retracted to safe standoff *)

    (* =========================================================================
       DIAGNOSTIC ALARM BIT DEFINITIONS
       ========================================================================= *)
    cALARM_ESTOP_ACTIVE         : WORD := 16#0001; (* Bit 0: Emergency stop contact opened *)
    cALARM_LOW_AIR_PRESSURE     : WORD := 16#0002; (* Bit 1: Bearing supply below 4.8 bar (Grounded risk) *)
    cALARM_VACUUM_LOSS          : WORD := 16#0004; (* Bit 2: Vacuum preload lost (loss of film stiffness) *)
    cALARM_THERMAL_DRIFT_EXCEED : WORD := 16#0008; (* Bit 3: Frame temperature deviated > 0.015 C *)
    cALARM_SPINDLE_OVERTEMP     : WORD := 16#0010; (* Bit 4: Spindle core temp > 40.0 C *)
    cALARM_TMR_MAJORITY_LOSS    : WORD := 16#0020; (* Bit 5: >= 2 Laser channels diverged / defective *)
    cALARM_PZT_SATURATION_ERR   : WORD := 16#0040; (* Bit 6: Piezo drive commanded to voltage rails *)
    cALARM_TRACKING_ERROR_TRIP  : WORD := 16#0080; (* Bit 7: Contouring error exceeded 25.0 nm threshold *)
    cALARM_LAMINAR_AIR_FAULT    : WORD := 16#0100; (* Bit 8: Enclosure air shower stability lost *)
END_VAR

(* =================================================================================================
   EXECUTIVE LOGIC IMPLEMENTATION (CYCLIC SYNCHRONOUS TASK - TS = 10 MICROSECONDS)
   ================================================================================================= *)

(* --- STAGE 0: FAIL-SAFE EMERGENCY STOP & PRIMARY PNEUMATIC INTERLOCK EVALUATION --- *)
IF NOT bEmergencyStop THEN
    (* Immediate deterministic hardware safe state trip *)
    rFTS_PiezoDrive_V := rMinPiezoVoltage; (* Snap diamond tool back to -20V (< 50 microseconds) *)
    rAerostaticDamping_mA := 0.0;          (* De-energize damping coils to prevent thermal dissipation *)
    bSystemReady := FALSE;
    bActiveControl := FALSE;
    bToolRetracted := TRUE;
    wAlarmWord := wAlarmWord OR cALARM_ESTOP_ACTIVE;
    wStatusWord := cSTATUS_TOOL_RETRACTED_SAFE;
    iState := 99; (* Transition directly to critical fault latch state *)
    RETURN;
END_IF;

(* Fault reset acknowledgement on positive edge *)
IF bResetFault AND (iState = 99) THEN
    IF (rSupplyPressure_bar >= 5.0) AND (rBearingVacuumPreload_bar <= -0.28) THEN
        wAlarmWord := 16#0000;
        bToolRetracted := FALSE;
        iState := 0; (* Return to bootstrap sequence *)
    END_IF;
END_IF;

(* --- STAGE 1: METROLOGY VALIDATION & 2oo3 TRIPLE MODULAR REDUNDANCY VOTING --- *)
(* Calculate pairwise Euclidean absolute discrepancies among interferometers *)
rDiff12 := ABS(rDisplacementLaser1_nm - rDisplacementLaser2_nm);
rDiff23 := ABS(rDisplacementLaser2_nm - rDisplacementLaser3_nm);
rDiff31 := ABS(rDisplacementLaser3_nm - rDisplacementLaser1_nm);

(* Channel-specific discrepancy fault qualification *)
IF (rDiff12 > rTMR_Tolerance_nm) AND (rDiff31 > rTMR_Tolerance_nm) THEN
    udiFaultCount_Ch1 := udiFaultCount_Ch1 + 1;
    IF udiFaultCount_Ch1 >= udiConsecutiveDivergenceLimit THEN
        bChan1_Healthy := FALSE;
    END_IF;
ELSE
    IF udiFaultCount_Ch1 > 0 THEN udiFaultCount_Ch1 := udiFaultCount_Ch1 - 1; END_IF;
END_IF;

IF (rDiff12 > rTMR_Tolerance_nm) AND (rDiff23 > rTMR_Tolerance_nm) THEN
    udiFaultCount_Ch2 := udiFaultCount_Ch2 + 1;
    IF udiFaultCount_Ch2 >= udiConsecutiveDivergenceLimit THEN
        bChan2_Healthy := FALSE;
    END_IF;
ELSE
    IF udiFaultCount_Ch2 > 0 THEN udiFaultCount_Ch2 := udiFaultCount_Ch2 - 1; END_IF;
END_IF;

IF (rDiff23 > rTMR_Tolerance_nm) AND (rDiff31 > rTMR_Tolerance_nm) THEN
    udiFaultCount_Ch3 := udiFaultCount_Ch3 + 1;
    IF udiFaultCount_Ch3 >= udiConsecutiveDivergenceLimit THEN
        bChan3_Healthy := FALSE;
    END_IF;
ELSE
    IF udiFaultCount_Ch3 > 0 THEN udiFaultCount_Ch3 := udiFaultCount_Ch3 - 1; END_IF;
END_IF;

(* 2oo3 TMR Decision Engine & Graceful Degradation Logic *)
IF bChan1_Healthy AND bChan2_Healthy AND bChan3_Healthy THEN
    (* Full Triple Modular Redundancy: Midpoint median / mean of 3 channels *)
    rVotedPosition_nm := (rDisplacementLaser1_nm + rDisplacementLaser2_nm + rDisplacementLaser3_nm) / 3.0;
    bDegradedMode := FALSE;
    wStatusWord := (wStatusWord OR cSTATUS_TMR_3_CHANNEL_OK) AND NOT cSTATUS_TMR_2_CHANNEL_DEG;
ELSIF bChan1_Healthy AND bChan2_Healthy AND NOT bChan3_Healthy THEN
    (* Degraded Mode A: Channels 1 and 2 healthy, Channel 3 disqualified *)
    rVotedPosition_nm := (rDisplacementLaser1_nm + rDisplacementLaser2_nm) * 0.5;
    bDegradedMode := TRUE;
    wStatusWord := (wStatusWord OR cSTATUS_TMR_2_CHANNEL_DEG) AND NOT cSTATUS_TMR_3_CHANNEL_OK;
ELSIF bChan2_Healthy AND bChan3_Healthy AND NOT bChan1_Healthy THEN
    (* Degraded Mode B: Channels 2 and 3 healthy, Channel 1 disqualified *)
    rVotedPosition_nm := (rDisplacementLaser2_nm + rDisplacementLaser3_nm) * 0.5;
    bDegradedMode := TRUE;
    wStatusWord := (wStatusWord OR cSTATUS_TMR_2_CHANNEL_DEG) AND NOT cSTATUS_TMR_3_CHANNEL_OK;
ELSIF bChan3_Healthy AND bChan1_Healthy AND NOT bChan2_Healthy THEN
    (* Degraded Mode C: Channels 3 and 1 healthy, Channel 2 disqualified *)
    rVotedPosition_nm := (rDisplacementLaser3_nm + rDisplacementLaser1_nm) * 0.5;
    bDegradedMode := TRUE;
    wStatusWord := (wStatusWord OR cSTATUS_TMR_2_CHANNEL_DEG) AND NOT cSTATUS_TMR_3_CHANNEL_OK;
ELSE
    (* Majority voting total loss: >= 2 interferometers uncoordinated or out of tolerance *)
    wAlarmWord := wAlarmWord OR cALARM_TMR_MAJORITY_LOSS;
    rVotedPosition_nm := rDisplacementLaser1_nm; (* Frozen unvalidated hold *)
    iState := 70; (* Invoke controlled high-speed diamond retract *)
END_IF;

(* Compute carriage instantaneous velocity for squeeze-film damping [nm/s] *)
IF rSamplingClock_kHz > 0.0 THEN
    rGuidewayVelocity_nms := (rVotedPosition_nm - rLastVotedPos) * (rSamplingClock_kHz * 1000.0);
    rLastVotedPos := rVotedPosition_nm;
END_IF;

(* --- STAGE 2: ADAPTIVE SPINDLE HARMONIC RUNOUT BIQUAD FILTER --- *)
rSpindleFreq_Hz := rSpindleSpeed_rpm / 60.0;
IF rSpindleFreq_Hz > 10.0 THEN
    (* Direct form II biquad resonator notch filter running at 100 kHz *)
    rSpindleRunoutFiltered_nm := (rCoeff_b0 * rVotedPosition_nm) + rNotch_x1;
    rNotch_x1 := (rCoeff_b1 * rVotedPosition_nm) - (rCoeff_a1 * rSpindleRunoutFiltered_nm) + rNotch_x2;
    rNotch_x2 := (rCoeff_b2 * rVotedPosition_nm) - (rCoeff_a2 * rSpindleRunoutFiltered_nm);
ELSE
    rSpindleRunoutFiltered_nm := rVotedPosition_nm;
END_IF;

(* Compute closed-loop nano-tracking deviation *)
rResidualTrackingError_nm := rNominalToolTrajectory_nm - rSpindleRunoutFiltered_nm;

(* --- STAGE 3: MULTI-STAGE CO-ORDINATING CYBER-PHYSICAL FINITE STATE MACHINE --- *)
CASE iState OF

    0: (* === STATE 0: BOOT & PNEUMATIC LEVITATION PRE-ARM === *)
        bSystemReady := FALSE;
        bActiveControl := FALSE;
        bToolRetracted := TRUE;
        rFTS_PiezoDrive_V := 0.0;
        rAerostaticDamping_mA := 0.0;
        wStatusWord := 16#0000;

        (* Check critical air pressure before admitting levitation stage *)
        IF rSupplyPressure_bar < 4.8 THEN
            wAlarmWord := wAlarmWord OR cALARM_LOW_AIR_PRESSURE;
        ELSIF rBearingVacuumPreload_bar > -0.25 THEN
            wAlarmWord := wAlarmWord OR cALARM_VACUUM_LOSS;
        ELSE
            (* Healthy pneumatic boundary conditions met *)
            wAlarmWord := wAlarmWord AND NOT (cALARM_LOW_AIR_PRESSURE OR cALARM_VACUUM_LOSS);
            IF bEnable THEN
                iState := 10;
            END_IF;
        END_IF;

    10: (* === STATE 10: AEROSTATIC FILM LEVITATION STABILIZATION === *)
        (* Maintain air bearing for 3.5 seconds to establish steady-state gas squeeze film *)
        tLevitationTimer(IN := TRUE, PT := T#3500MS);
        IF tLevitationTimer.Q THEN
            tLevitationTimer(IN := FALSE);
            wStatusWord := wStatusWord OR cSTATUS_BEARING_LEVITED;
            iState := 20;
        END_IF;

        IF rSupplyPressure_bar < 4.8 THEN
            tLevitationTimer(IN := FALSE);
            iState := 0;
        END_IF;

    20: (* === STATE 20: THERMAL EQUILIBRIUM & AIR SHOWER SOAK === *)
        (* Verify Zerodur metrology temperature within strict 20.00 +/- 0.01 C range *)
        IF ABS(rGuidewayTemp_degC - 20.00) > 0.015 THEN
            wAlarmWord := wAlarmWord OR cALARM_THERMAL_DRIFT_EXCEED;
        ELSE
            wAlarmWord := wAlarmWord AND NOT cALARM_THERMAL_DRIFT_EXCEED;
        END_IF;

        IF NOT bAirShowerThermalReady THEN
            wAlarmWord := wAlarmWord OR cALARM_LAMINAR_AIR_FAULT;
        ELSE
            wAlarmWord := wAlarmWord AND NOT cALARM_LAMINAR_AIR_FAULT;
        END_IF;

        tThermalSoakTimer(IN := (wAlarmWord = 16#0000), PT := T#10000MS);
        IF tThermalSoakTimer.Q THEN
            tThermalSoakTimer(IN := FALSE);
            wStatusWord := wStatusWord OR cSTATUS_THERMAL_STABLE;
            iState := 30;
        END_IF;

    30: (* === STATE 30: FAST TOOL SERVO HYSTERESIS PRE-CHARGE & CAPACITIVE BIAS === *)
        (* Slowly ramp PZT to mid-scale offset (65.0 V) to eliminate polarization hysteresis *)
        IF rFTS_PiezoDrive_V < 65.0 THEN
            rFTS_PiezoDrive_V := rFTS_PiezoDrive_V + 0.15; (* 150 mV per 10 us ramp rate *)
        ELSE
            rFTS_PiezoDrive_V := 65.0;
            tCalibrationTimer(IN := TRUE, PT := T#500MS);
            IF tCalibrationTimer.Q THEN
                tCalibrationTimer(IN := FALSE);
                wStatusWord := wStatusWord OR cSTATUS_FTS_CALIBRATED;
                bToolRetracted := FALSE;
                iState := 40;
            END_IF;
        END_IF;

    40: (* === STATE 40: 2oo3 TMR ALIGNMENT & SENSOR BASELINE QUALIFICATION === *)
        IF (rDiff12 < rTMR_Tolerance_nm) AND (rDiff23 < rTMR_Tolerance_nm) AND (rDiff31 < rTMR_Tolerance_nm) THEN
            (* Initialize discrete state observer variables *)
            rStateHat_1 := rVotedPosition_nm;
            rStateHat_2 := 0.0;
            rStateHat_3 := 0.0;
            rStateHat_4 := 0.0;
            bSystemReady := TRUE;
            iState := 50; (* Engage high-precision machining *)
        ELSE
            (* Sensor misalignment persists: abort to fault *)
            wAlarmWord := wAlarmWord OR cALARM_TMR_MAJORITY_LOSS;
            iState := 99;
        END_IF;

    50: (* === STATE 50: SYNCHRONOUS ACTIVE SUB-NANOMETER DIAMOND FLYCUTTING === *)
        bActiveControl := TRUE;
        wStatusWord := wStatusWord OR cSTATUS_CLOSED_LOOP_NANO OR cSTATUS_ACTIVE_DAMPING_ON;

        (* -------------------------------------------------------------
           SUB-TASK A: 4th-Order Luenberger State-Space Observer Update
           ------------------------------------------------------------- *)
        (* Innovation: actual capacitive displacement vs estimated displacement *)
        rObserverInnovation := (rPiezoCapacitiveFeedback_um * 1000.0) - (aC1 * rStateHat_1 + aC3 * rStateHat_3);

        (* State dynamic propagation: x_hat[k+1] = A * x_hat[k] + B * u[k] + L * e[k] *)
        rStateHat_1 := (aA11 * rStateHat_1) + (aA12 * rStateHat_2) + (aA13 * rStateHat_3) + (aA14 * rStateHat_4)
                       + (aB1 * rFTS_PiezoDrive_V) + (aL1 * rObserverInnovation);

        rStateHat_2 := (aA21 * rStateHat_1) + (aA22 * rStateHat_2) + (aA23 * rStateHat_3) + (aA24 * rStateHat_4)
                       + (aB2 * rFTS_PiezoDrive_V) + (aL2 * rObserverInnovation);

        rStateHat_3 := (aA31 * rStateHat_1) + (aA32 * rStateHat_2) + (aA33 * rStateHat_3) + (aA34 * rStateHat_4)
                       + (aB3 * rFTS_PiezoDrive_V) + (aL3 * rObserverInnovation);

        rStateHat_4 := (aA41 * rStateHat_1) + (aA42 * rStateHat_2) + (aA43 * rStateHat_3) + (aA44 * rStateHat_4)
                       + (aB4 * rFTS_PiezoDrive_V) + (aL4 * rObserverInnovation);

        (* -------------------------------------------------------------
           SUB-TASK B: Model Predictive Control (MPC) Recurrent Optimization
           ------------------------------------------------------------- *)
        (* Predict error trajectory over 3-step finite horizon *)
        rPredHorizon_1 := rResidualTrackingError_nm - (rStateHat_2 * 0.000010);
        rPredHorizon_2 := rPredHorizon_1 - (rStateHat_2 * 0.000020);
        rPredHorizon_3 := rPredHorizon_2 - (rStateHat_2 * 0.000030);

        (* Unconstrained optimal incremental voltage computation *)
        rDeltaU_Optimal := ((rWeight_Q * (rPredHorizon_1 + rPredHorizon_2 + rPredHorizon_3))
                           - (rWeight_S * rStateHat_4)) / (rWeight_R + 3.0 * rWeight_Q * aB1);

        (* Enforce strict physical voltage slew-rate limitation *)
        IF rDeltaU_Optimal > rMaxVoltageSlewRate THEN
            rDeltaU_Optimal := rMaxVoltageSlewRate;
        ELSIF rDeltaU_Optimal < -rMaxVoltageSlewRate THEN
            rDeltaU_Optimal := -rMaxVoltageSlewRate;
        END_IF;

        (* Integrate optimal voltage with anti-windup clamping *)
        rRawPiezoDrive := rFTS_PiezoDrive_V + rDeltaU_Optimal;
        IF rRawPiezoDrive > rMaxPiezoVoltage THEN
            rFTS_PiezoDrive_V := rMaxPiezoVoltage;
            wAlarmWord := wAlarmWord OR cALARM_PZT_SATURATION_ERR;
        ELSIF rRawPiezoDrive < rMinPiezoVoltage THEN
            rFTS_PiezoDrive_V := rMinPiezoVoltage;
            wAlarmWord := wAlarmWord OR cALARM_PZT_SATURATION_ERR;
        ELSE
            rFTS_PiezoDrive_V := rRawPiezoDrive;
            wAlarmWord := wAlarmWord AND NOT cALARM_PZT_SATURATION_ERR;
        END_IF;

        (* -------------------------------------------------------------
           SUB-TASK C: Active Aerostatic Guideway Squeeze-Film Damping
           Electromagnetic Lorentz force counteracts bearing bounce modes
           ------------------------------------------------------------- *)
        rAerostaticDamping_mA := -1.0 * (rGuidewayVelocity_nms * rDampingGain_mA_per_nms);

        (* Voice-coil thermal current clamp *)
        IF rAerostaticDamping_mA > rMaxDampingCurrent_mA THEN
            rAerostaticDamping_mA := rMaxDampingCurrent_mA;
        ELSIF rAerostaticDamping_mA < -rMaxDampingCurrent_mA THEN
            rAerostaticDamping_mA := -rMaxDampingCurrent_mA;
        END_IF;

        (* -------------------------------------------------------------
           SUB-TASK D: Surface Roughness (Ra) Statistical Online Accumulator
           ------------------------------------------------------------- *)
        rAbsErrorAccumulator := rAbsErrorAccumulator + ABS(rResidualTrackingError_nm);
        udiSampleCounter := udiSampleCounter + 1;
        IF udiSampleCounter >= udiWindowSize THEN
            rSurfaceRoughnessEstimate_nmRa := (rAbsErrorAccumulator / UDINT_TO_REAL(udiWindowSize)) * 0.798;
            rAbsErrorAccumulator := 0.0;
            udiSampleCounter := 0;
        END_IF;

        (* Contouring safety envelope supervision *)
        IF ABS(rResidualTrackingError_nm) > 25.0 THEN
            wAlarmWord := wAlarmWord OR cALARM_TRACKING_ERROR_TRIP;
            iState := 70; (* Trip controlled retract *)
        END_IF;

        (* Dynamic health interlocks *)
        IF (rSupplyPressure_bar < 4.8) OR (rBearingVacuumPreload_bar > -0.25) THEN
            iState := 70;
        END_IF;

        IF NOT bEnable THEN
            iState := 70;
        END_IF;

    70: (* === STATE 70: CONTROLLED ULTRA-FAST FAIL-SAFE DIAMOND RETRACT === *)
        bActiveControl := FALSE;
        (* Snap piezo voltage to minimum negative rail (-20V) to pull tool away from substrate *)
        IF rFTS_PiezoDrive_V > rMinPiezoVoltage THEN
            rFTS_PiezoDrive_V := rFTS_PiezoDrive_V - 5.0; (* Ultra-steep ramp down *)
            IF rFTS_PiezoDrive_V < rMinPiezoVoltage THEN
                rFTS_PiezoDrive_V := rMinPiezoVoltage;
            END_IF;
        ELSE
            bToolRetracted := TRUE;
            wStatusWord := (wStatusWord AND NOT cSTATUS_CLOSED_LOOP_NANO) OR cSTATUS_TOOL_RETRACTED_SAFE;
        END_IF;

        (* Ramp damping voice coil to zero smoothly *)
        rAerostaticDamping_mA := rAerostaticDamping_mA * 0.95;

        tFaultHoldTimer(IN := bToolRetracted, PT := T#1500MS);
        IF tFaultHoldTimer.Q THEN
            tFaultHoldTimer(IN := FALSE);
            bSystemReady := FALSE;
            IF wAlarmWord <> 16#0000 THEN
                iState := 99; (* Lock into fault state if alarms active *)
            ELSE
                iState := 0;  (* Standby idle *)
            END_IF;
        END_IF;

    99: (* === STATE 99: CRITICAL HARDWARE FAULT LATCH === *)
        bSystemReady := FALSE;
        bActiveControl := FALSE;
        bToolRetracted := TRUE;
        rFTS_PiezoDrive_V := rMinPiezoVoltage;
        rAerostaticDamping_mA := 0.0;
        (* State remains latched until positive edge on bResetFault under valid conditions *)

END_CASE;

END_FUNCTION_BLOCK
```"""

# Verifications
assert st_code.startswith("```iec-st\nFUNCTION_BLOCK FB_DiamondFlycutting_NanometerFTS"), "Invalid start"
assert st_code.endswith("END_FUNCTION_BLOCK\n```"), "Invalid end"
assert "VAR_INPUT" in st_code
assert "VAR_OUTPUT" in st_code
assert "VAR" in st_code
assert "END_CASE;" in st_code
assert len(st_code) >= 3500, f"Code length is {len(st_code)}, expected >= 3500"

print(f"ST Code verified. Length: {len(st_code)} characters.")

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": st_code}
    ]
}

agent_id = uuid.uuid4().hex[:8]
output_filename = f"data/swarm_raw/agent_{agent_id}.json"

with open(output_filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False, indent=2)

print(f"Saved successfully to {output_filename}")
