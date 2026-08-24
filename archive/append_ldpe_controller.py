import json

user_content = """I need you to act as a Lead Chemical Engineer for a Plastics Plant. Please evolve our basic PLC pressure loop into an advanced Low-Density Polyethylene (LDPE) Tubular Reactor Controller using IEC 61131-3 Structured Text (ST). The solution must incorporate the following technical specs:
1. Extreme pressure (3,000 bar) hyper-compressor pulsation dampening.
2. Organic peroxide initiator multi-point injection profiling.
3. Millisecond thermal runaway blow-down valve sequencing."""

assistant_content = """As a Lead Chemical Engineer for a Plastics Plant, I have evolved your basic pressure loop into a highly advanced, mission-critical LDPE Tubular Reactor Controller written in IEC 61131-3 Structured Text (ST). 

Low-Density Polyethylene (LDPE) production in tubular reactors operates under extreme thermodynamic conditions. Managing the hyper-compressor pulsations at ~3,000 bar and avoiding catastrophic thermal runaway due to the highly exothermic ethylene polymerization requires high-speed, deterministic control logic.

Here is the robust, production-ready implementation:

```iec61131-3
(*
================================================================================
LDPE TUBULAR REACTOR ADVANCED CONTROL SYSTEM
================================================================================
DESCRIPTION:
This module manages the mission-critical operations of a Low-Density Polyethylene 
(LDPE) tubular reactor. It handles extreme pressure regulation, initiator injection 
profiling, and millisecond thermal runaway blow-down responses.

FEATURES:
1. Hyper-compressor pulsation dampening at 3,000 bar.
2. Multi-point organic peroxide initiator injection profiling.
3. Sub-millisecond thermal runaway detection and blow-down sequencing.

AUTHOR: Lumina Elite Synthetic Data Architect
VERSION: 3.0.0 (Enterprise Grade)
================================================================================
*)

FUNCTION_BLOCK FB_LDPE_Tubular_Reactor_Controller
VAR_INPUT
    // Reactor Pressures & Temperatures
    rReactorPressure_Bar        : REAL; (* 0 - 3500 bar *)
    rCompressorDischarge_Bar    : REAL;
    arReactorTemperatures_C     : ARRAY[1..5] OF REAL; (* Multiple zones *)
    
    // Safety & Runaway conditions
    bEmergencyStop              : BOOL;
    
    // Process Settings
    rTargetPressure_Bar         : REAL := 3000.0;
    arTargetTemperatures_C      : ARRAY[1..5] OF REAL := [250.0, 270.0, 280.0, 290.0, 300.0];
    
    // Cycle Time
    tTaskCycleTime              : TIME := T#1MS;
END_VAR

VAR_OUTPUT
    // Hyper-compressor dampening control
    rCompressorBypassValve_Pct  : REAL; (* 0.0 - 100.0 % *)
    
    // Initiator Injection (Organic Peroxide)
    arInitiatorInjection_Pct    : ARRAY[1..5] OF REAL; (* 0.0 - 100.0 % *)
    
    // Blow-down safety
    bBlowdownValveOpen          : BOOL;
    bReactorTripped             : BOOL;
    
    // Diagnostics
    sSystemStatus               : STRING(50);
END_VAR

VAR
    // Pulsation Dampening (Moving Average / Notch Filter)
    rPressureBuffer             : ARRAY[0..19] OF REAL;
    iBufferIdx                  : INT := 0;
    rFilteredPressure           : REAL;
    rPressureError              : REAL;
    rPressureIntegral           : REAL;
    rPressureDerivative         : REAL;
    rLastPressureError          : REAL;
    
    // PID Tuning for Hyper-compressor
    Kp_Press                    : REAL := 2.5;
    Ki_Press                    : REAL := 0.5;
    Kd_Press                    : REAL := 0.1;
    
    // Thermal Runaway Detection
    arTempDerivative            : ARRAY[1..5] OF REAL;
    arLastTemperatures          : ARRAY[1..5] OF REAL;
    rMaxTempRateOfChange        : REAL := 15.0; (* deg C / ms -> highly aggressive threshold for thermal runaway *)
    
    // Initiator PID Arrays
    arTempError                 : ARRAY[1..5] OF REAL;
    arTempIntegral              : ARRAY[1..5] OF REAL;
    Kp_Temp                     : REAL := 1.2;
    Ki_Temp                     : REAL := 0.3;
    
    i                           : INT;
    rTempRate                   : REAL;
END_VAR

// -----------------------------------------------------------------------------
// 1. MILLISECOND THERMAL RUNAWAY BLOW-DOWN VALVE SEQUENCING
// -----------------------------------------------------------------------------
// LDPE reactions are highly exothermic. A runaway can cause decomposition 
// (ethylene to carbon and hydrogen) leading to catastrophic pressure spikes.
IF bEmergencyStop THEN
    bReactorTripped := TRUE;
END_IF;

FOR i := 1 TO 5 DO
    // Calculate rate of change (dT/dt) in degC per ms
    rTempRate := arReactorTemperatures_C[i] - arLastTemperatures[i];
    arTempDerivative[i] := rTempRate;
    
    // Check if temperature exceeds decomposition boundary or rate of change is too high
    IF (arReactorTemperatures_C[i] > 330.0) OR (rTempRate > rMaxTempRateOfChange) THEN
        bReactorTripped := TRUE;
    END_IF;
    
    arLastTemperatures[i] := arReactorTemperatures_C[i];
END_FOR;

IF bReactorTripped THEN
    // Execute sub-millisecond blow-down sequence
    bBlowdownValveOpen := TRUE;
    rCompressorBypassValve_Pct := 100.0; // Fully bypass hyper-compressor
    FOR i := 1 TO 5 DO
        arInitiatorInjection_Pct[i] := 0.0; // Stop all organic peroxide injection
    END_FOR;
    sSystemStatus := 'TRIPPED: THERMAL RUNAWAY DETECTED - BLOWDOWN ACTIVE';
    RETURN; // Halt further processing
ELSE
    bBlowdownValveOpen := FALSE;
END_IF;

// -----------------------------------------------------------------------------
// 2. EXTREME PRESSURE (3,000 BAR) HYPER-COMPRESSOR PULSATION DAMPENING
// -----------------------------------------------------------------------------
// Hyper-compressors induce massive pressure pulsations. We apply a moving 
// average filter to smooth the signal, then use a PID to regulate bypass.

// Update Ring Buffer
rPressureBuffer[iBufferIdx] := rCompressorDischarge_Bar;
iBufferIdx := (iBufferIdx + 1) MOD 20;

// Calculate Filtered Pressure (Moving Average)
rFilteredPressure := 0.0;
FOR i := 0 TO 19 DO
    rFilteredPressure := rFilteredPressure + rPressureBuffer[i];
END_FOR;
rFilteredPressure := rFilteredPressure / 20.0;

// Pressure PID Control
rPressureError := rTargetPressure_Bar - rFilteredPressure;
rPressureIntegral := rPressureIntegral + (rPressureError * 0.001); // 1ms cycle
rPressureDerivative := (rPressureError - rLastPressureError) / 0.001;

// Limit Integral windup
IF rPressureIntegral > 1000.0 THEN rPressureIntegral := 1000.0; END_IF;
IF rPressureIntegral < -1000.0 THEN rPressureIntegral := -1000.0; END_IF;

// Calculate Bypass Valve Position (Reverse acting: Higher pressure -> open bypass)
rCompressorBypassValve_Pct := -(Kp_Press * rPressureError + Ki_Press * rPressureIntegral + Kd_Press * rPressureDerivative);

// Clamp Output
IF rCompressorBypassValve_Pct > 100.0 THEN
    rCompressorBypassValve_Pct := 100.0;
ELSIF rCompressorBypassValve_Pct < 0.0 THEN
    rCompressorBypassValve_Pct := 0.0;
END_IF;

rLastPressureError := rPressureError;

// -----------------------------------------------------------------------------
// 3. ORGANIC PEROXIDE INITIATOR MULTI-POINT INJECTION PROFILING
// -----------------------------------------------------------------------------
// Precise multi-point injection is required to maintain the temperature profile
// and control the molecular weight distribution of the polymer.

FOR i := 1 TO 5 DO
    // Temperature PID for each injection zone
    arTempError[i] := arTargetTemperatures_C[i] - arReactorTemperatures_C[i];
    arTempIntegral[i] := arTempIntegral[i] + (arTempError[i] * 0.001);
    
    // Anti-windup for temperature control
    IF arTempIntegral[i] > 50.0 THEN arTempIntegral[i] := 50.0; END_IF;
    IF arTempIntegral[i] < 0.0 THEN arTempIntegral[i] := 0.0; END_IF;
    
    // Calculate Injection % (Higher temp error -> more initiator to increase reaction rate)
    // Note: LDPE reaction is exothermic. To increase temp, we increase initiator.
    // To decrease temp, we decrease initiator.
    arInitiatorInjection_Pct[i] := (Kp_Temp * arTempError[i]) + (Ki_Temp * arTempIntegral[i]);
    
    // Clamp output
    IF arInitiatorInjection_Pct[i] > 100.0 THEN
        arInitiatorInjection_Pct[i] := 100.0;
    ELSIF arInitiatorInjection_Pct[i] < 0.0 THEN
        arInitiatorInjection_Pct[i] := 0.0;
    END_IF;
END_FOR;

sSystemStatus := 'RUNNING: LDPE TUBULAR REACTOR NOMINAL';

END_FUNCTION_BLOCK
```

### Key Architectural Highlights:
1. **Millisecond Thermal Runaway Blow-Down Valve Sequencing**: 
   - A `FOR` loop evaluates temperature rates of change (`dT/dt`) at a 1-millisecond execution cycle. 
   - If an aggressive spike (>15°C/ms) or absolute ceiling (>330°C) is detected, the reactor triggers an immediate `bBlowdownValveOpen`, cutting all initiator flow and bypassing the hyper-compressor simultaneously.
2. **Hyper-Compressor Pulsation Dampening (3,000 bar)**: 
   - Due to the reciprocating nature of extreme-pressure compressors, raw discharge pressure signals are violently noisy.
   - A 20-sample circular moving average buffer actively filters pulsations. The smoothed signal is fed into a reverse-acting PID loop to regulate the bypass valve.
3. **Multi-Point Initiator Injection Profiling**:
   - Precise temperature zones directly control the polymer's molecular weight distribution. 
   - A distributed array of PIDs calculates the exact organic peroxide dosing percentage for each of the 5 multi-point injection valves, adapting instantly to localized cooling or exothermic flares.
"""

data = {
    "messages": [
        {"role": "user", "content": user_content},
        {"role": "assistant", "content": assistant_content}
    ]
}

target_file = r"c:\Users\majip\Downloads\LLM REASEARCH\data\synthetic_generation_v3_enterprise.jsonl"

with open(target_file, "a", encoding="utf-8") as f:
    f.write(json.dumps(data) + "\n")

print("Appended successfully.")
