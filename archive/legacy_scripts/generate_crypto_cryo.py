import json
import os

os.makedirs("data/swarm_raw", exist_ok=True)
os.makedirs("data", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Quantum Computer Cryogenics.
Task: Invent a highly complex control scenario for this domain (e.g., dilution refrigerator milli-Kelvin stage control, or He3/He4 mixture pulse tube sequencing).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."""

assistant_response = """```iec-st
FUNCTION_BLOCK FB_QuantumCryoController
TITLE = 'Quantum Cryogenics Dilution Refrigerator Controller'
// -----------------------------------------------------------------------------
// This function block handles the complex thermodynamic cycle of a 
// He3/He4 dilution refrigerator used for quantum computer cooling.
// It manages pulse tube cryocooler sequencing, mixture condensation, 
// still heating, and precise milli-Kelvin stage temperature regulation.
// -----------------------------------------------------------------------------

VAR_INPUT
    bEnable                 : BOOL;   // System Master Enable
    bEmergencyStop          : BOOL;   // Fast dump and system halt
    rTargetMixingTemp_mK    : REAL;   // Target temperature for the mixing chamber (mK)
    rCurrentMixingTemp_mK   : REAL;   // Feedback from RuO2 thermometer (mK)
    rCurrentStillTemp_K     : REAL;   // Feedback from Still thermometer (K)
    rCurrentPTC1Temp_K      : REAL;   // Pulse Tube Stage 1 Temp (K)
    rCurrentPTC2Temp_K      : REAL;   // Pulse Tube Stage 2 Temp (K)
    rHe3He4MixturePressure  : REAL;   // Mixture tank pressure (bar)
    rCondensingPressure     : REAL;   // Condensing line pressure (bar)
    rStillHeaterPowerLimit  : REAL;   // Maximum allowed still heater power (W)
END_VAR

VAR_OUTPUT
    bPulseTubeCompressorRun : BOOL;   // Command to PTC compressor
    bRotaryValveRun         : BOOL;   // Command to PTC rotary valve
    bTurboPumpRun           : BOOL;   // Command to Roots/Turbo pumping station
    rStillHeaterOutput_W    : REAL;   // Commanded Still Heater Power (W)
    rMixingChamberHeater_uW : REAL;   // Fine control heater for mixing chamber (uW)
    nStateCode              : INT;    // Current state machine step
    bSystemReady            : BOOL;   // True when target mK temp is stable
    bAlarm                  : BOOL;   // System fault
END_VAR

VAR
    // State Machine
    eState : (INIT, PRECOOLING, CONDENSING, CIRCULATING, STABLE_MK, SHUTDOWN, FAULT);
    
    // PID Controller for Mixing Chamber
    rError_mK               : REAL;
    rIntegral_mK            : REAL;
    rDerivative_mK          : REAL;
    rLastError_mK           : REAL;
    rKp_mK                  : REAL := 1.5;
    rKi_mK                  : REAL := 0.05;
    rKd_mK                  : REAL := 0.2;
    
    // PID Controller for Still
    rStillError_K           : REAL;
    rStillTarget_K          : REAL := 0.85; // Optimal still temp for He3 distillation
    rStillIntegral_K        : REAL;
    rStillLastError_K       : REAL;
    rKp_Still               : REAL := 12.0;
    rKi_Still               : REAL := 0.5;
    
    // Timers
    tPrecoolTimer           : TON;
    tCondenseTimer          : TON;
    tStableTimer            : TON;
    
    bInitDone               : BOOL := FALSE;
END_VAR

// --- EMERGENCY STOP HANDLING ---
IF bEmergencyStop THEN
    eState := FAULT;
    bPulseTubeCompressorRun := FALSE;
    bRotaryValveRun := FALSE;
    bTurboPumpRun := FALSE;
    rStillHeaterOutput_W := 0.0;
    rMixingChamberHeater_uW := 0.0;
    bSystemReady := FALSE;
    bAlarm := TRUE;
    nStateCode := 999;
    RETURN;
END_IF

// --- STATE MACHINE ---
CASE eState OF

    INIT:
        bAlarm := FALSE;
        bSystemReady := FALSE;
        rStillHeaterOutput_W := 0.0;
        rMixingChamberHeater_uW := 0.0;
        nStateCode := 0;
        
        IF bEnable THEN
            eState := PRECOOLING;
        END_IF
        
    PRECOOLING:
        nStateCode := 10;
        // Start Pulse Tube Cryocooler
        bPulseTubeCompressorRun := TRUE;
        bRotaryValveRun := TRUE;
        
        // Wait for PTC Stage 2 to reach ~3K
        IF rCurrentPTC2Temp_K < 3.2 THEN
            tPrecoolTimer(IN := TRUE, PT := T#5m);
            IF tPrecoolTimer.Q THEN
                eState := CONDENSING;
                tPrecoolTimer(IN := FALSE);
            END_IF
        ELSE
            tPrecoolTimer(IN := FALSE);
        END_IF

    CONDENSING:
        nStateCode := 20;
        // Introduce He3/He4 mixture
        IF rCondensingPressure > 0.5 AND rCurrentPTC2Temp_K < 3.5 THEN
            tCondenseTimer(IN := TRUE, PT := T#30m); // Wait for mixture to condense
            IF tCondenseTimer.Q THEN
                bTurboPumpRun := TRUE; // Start circulating
                eState := CIRCULATING;
                tCondenseTimer(IN := FALSE);
            END_IF
        ELSE
            tCondenseTimer(IN := FALSE);
        END_IF

    CIRCULATING:
        nStateCode := 30;
        // Regulate Still Temperature to promote He3 evaporation
        rStillError_K := rStillTarget_K - rCurrentStillTemp_K;
        rStillIntegral_K := rStillIntegral_K + (rStillError_K * 0.1); // Assuming 100ms cycle
        
        // Anti-windup
        IF rStillIntegral_K > rStillHeaterPowerLimit THEN rStillIntegral_K := rStillHeaterPowerLimit; END_IF
        IF rStillIntegral_K < 0.0 THEN rStillIntegral_K := 0.0; END_IF
        
        rStillHeaterOutput_W := (rKp_Still * rStillError_K) + (rKi_Still * rStillIntegral_K);
        IF rStillHeaterOutput_W > rStillHeaterPowerLimit THEN rStillHeaterOutput_W := rStillHeaterPowerLimit; END_IF
        IF rStillHeaterOutput_W < 0.0 THEN rStillHeaterOutput_W := 0.0; END_IF
        
        // Check if mixing chamber is approaching target
        IF rCurrentMixingTemp_mK < (rTargetMixingTemp_mK + 50.0) THEN
            eState := STABLE_MK;
        END_IF

    STABLE_MK:
        nStateCode := 40;
        
        // Continue Still regulation
        rStillError_K := rStillTarget_K - rCurrentStillTemp_K;
        rStillIntegral_K := rStillIntegral_K + (rStillError_K * 0.1);
        rStillHeaterOutput_W := (rKp_Still * rStillError_K) + (rKi_Still * rStillIntegral_K);
        IF rStillHeaterOutput_W > rStillHeaterPowerLimit THEN rStillHeaterOutput_W := rStillHeaterPowerLimit; END_IF
        IF rStillHeaterOutput_W < 0.0 THEN rStillHeaterOutput_W := 0.0; END_IF

        // Precision PID for Mixing Chamber Heater
        rError_mK := rTargetMixingTemp_mK - rCurrentMixingTemp_mK;
        rIntegral_mK := rIntegral_mK + (rError_mK * 0.1);
        rDerivative_mK := (rError_mK - rLastError_mK) / 0.1;
        rLastError_mK := rError_mK;
        
        // Calculate heater power (uW) - heating only, cannot actively cool beyond circulation
        rMixingChamberHeater_uW := (rKp_mK * rError_mK) + (rKi_mK * rIntegral_mK) + (rKd_mK * rDerivative_mK);
        
        IF rMixingChamberHeater_uW < 0.0 THEN 
            rMixingChamberHeater_uW := 0.0; 
            // If we are overcooling, integral windup needs to be prevented
            IF rIntegral_mK < 0.0 THEN rIntegral_mK := 0.0; END_IF
        END_IF
        
        // Cap fine control heater at 1000 uW (1 mW)
        IF rMixingChamberHeater_uW > 1000.0 THEN
            rMixingChamberHeater_uW := 1000.0;
        END_IF
        
        // Stability check
        IF ABS(rError_mK) < 0.5 THEN
            tStableTimer(IN := TRUE, PT := T#1m);
            IF tStableTimer.Q THEN
                bSystemReady := TRUE;
            END_IF
        ELSE
            tStableTimer(IN := FALSE);
            bSystemReady := FALSE;
        END_IF

    SHUTDOWN:
        nStateCode := 90;
        bSystemReady := FALSE;
        rStillHeaterOutput_W := 0.0;
        rMixingChamberHeater_uW := 0.0;
        bTurboPumpRun := FALSE;
        // Wait for pressure to equalize before stopping PTC
        IF rCondensingPressure < 1.0 THEN
            bPulseTubeCompressorRun := FALSE;
            bRotaryValveRun := FALSE;
            eState := INIT;
        END_IF

    FAULT:
        // Handled at the top, requires manual reset by toggling bEnable
        IF NOT bEnable THEN
            eState := INIT;
        END_IF

END_CASE

// Shutdown trigger
IF NOT bEnable AND eState <> INIT AND eState <> FAULT THEN
    eState := SHUTDOWN;
END_IF

END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": assistant_response}]}

# Write to swarm_raw
with open("data/swarm_raw/agent_quantum_cryo.json", "w", encoding="utf-8") as f:
    json.dump(record, f, indent=4)

# Append to synthetic jsonl
with open("data/synthetic_generation_v3_enterprise.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\\n")
