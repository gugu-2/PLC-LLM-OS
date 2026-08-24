import json
import os

prompt = """You are acting as a Lead Geotechnical Engineer. Evolve a basic PI controller block into a Slurry Wall Trenching Machine (Hydrofraise) Controller. Technical Specs: 1. Dual counter-rotating cutting wheel hydraulic pressure mapping to detect bedrock. 2. Bentonite slurry circulation and desanding plant density control. 3. Z-axis verticality closed-loop correction using onboard inclinometers.

The base PI controller has generic inputs/outputs. Adapt this into a highly complex, production-ready IEC 61131-3 implementation (Structured Text) for the Hydrofraise machine."""

response = """```iec61131-3
FUNCTION_BLOCK FB_Hydrofraise_Controller
TITLE = 'Hydrofraise Trenching Machine Controller'
VERSION : '2.0'
AUTHOR : 'Elite Synthetic Data Architect'

// -----------------------------------------------------------------------------
// DESCRIPTION:
// Complex controller for a slurry wall trenching machine (Hydrofraise).
// Implements:
// 1. Bedrock detection via hydraulic pressure mapping on dual cutting wheels.
// 2. Bentonite slurry density control for continuous cuttings removal.
// 3. Z-axis verticality correction via onboard inclinometers and steering flaps.
// -----------------------------------------------------------------------------

VAR_INPUT
    // Cutter Head Parameters
    rLeftCutterPressure_bar      : REAL; // Left cutting wheel hydraulic pressure
    rRightCutterPressure_bar     : REAL; // Right cutting wheel hydraulic pressure
    rCutterPressureThreshold     : REAL := 250.0; // Pressure indicating bedrock
    
    // Slurry System Parameters
    rSlurryDensityIn_gcm3        : REAL; // Bentonite density from desanding plant
    rSlurryDensityOut_gcm3       : REAL; // Density of slurry returning with cuttings
    rTargetDensityOut_gcm3       : REAL := 1.25; // Desired max return density
    
    // Inclinometer / Verticality
    rInclinometerX_deg           : REAL; // X-axis deviation (pitch)
    rInclinometerY_deg           : REAL; // Y-axis deviation (roll)
    rVerticalityTolerance_deg    : REAL := 0.1; // Acceptable deviation before correction
    
    // Control / System
    bEnableOperation             : BOOL;
    bReset                       : BOOL;
    rCycleTime_ms                : REAL := 10.0;
END_VAR

VAR_OUTPUT
    // Actuators & Pumps
    rLeftCutterTorque_pct        : REAL; // 0-100% command to left wheel
    rRightCutterTorque_pct       : REAL; // 0-100% command to right wheel
    rSlurryPumpSpeed_pct         : REAL; // 0-100% command to circulation pump
    
    // Steering Flaps for Verticality
    rSteerFlapX_pos_pct          : REAL; // Positive X flap extension
    rSteerFlapX_neg_pct          : REAL; // Negative X flap extension
    rSteerFlapY_pos_pct          : REAL; // Positive Y flap extension
    rSteerFlapY_neg_pct          : REAL; // Negative Y flap extension
    
    // Status
    bBedrockDetected             : BOOL;
    bVerticalityWarning          : BOOL;
    bDensityAlarm                : BOOL;
END_VAR

VAR
    // Moving Average for Pressure (Smoothing)
    aLeftPressHistory            : ARRAY[0..9] OF REAL;
    aRightPressHistory           : ARRAY[0..9] OF REAL;
    iPressIndex                  : INT := 0;
    rAvgLeftPress                : REAL;
    rAvgRightPress               : REAL;
    
    // PI Controllers for Verticality
    rKp_Steering                 : REAL := 15.0;
    rKi_Steering                 : REAL := 2.5;
    rIntegralX                   : REAL;
    rIntegralY                   : REAL;
    rErrorX                      : REAL;
    rErrorY                      : REAL;
    rMaxSteering                 : REAL := 100.0;
    
    // Slurry Control
    rDensityError                : REAL;
    rKp_Slurry                   : REAL := 50.0;
    
    i                            : INT;
    rCtrlX                       : REAL;
    rCtrlY                       : REAL;
END_VAR

BEGIN
    IF bReset THEN
        // Reset all states
        rIntegralX := 0.0;
        rIntegralY := 0.0;
        bBedrockDetected := FALSE;
        bVerticalityWarning := FALSE;
        bDensityAlarm := FALSE;
        rLeftCutterTorque_pct := 0.0;
        rRightCutterTorque_pct := 0.0;
        rSlurryPumpSpeed_pct := 0.0;
        rSteerFlapX_pos_pct := 0.0;
        rSteerFlapX_neg_pct := 0.0;
        rSteerFlapY_pos_pct := 0.0;
        rSteerFlapY_neg_pct := 0.0;
        FOR i := 0 TO 9 DO
            aLeftPressHistory[i] := 0.0;
            aRightPressHistory[i] := 0.0;
        END_FOR;
        iPressIndex := 0;
        RETURN;
    END_IF;

    IF NOT bEnableOperation THEN
        rLeftCutterTorque_pct := 0.0;
        rRightCutterTorque_pct := 0.0;
        rSlurryPumpSpeed_pct := 0.0;
        RETURN;
    END_IF;

    // =========================================================================
    // 1. DUAL COUNTER-ROTATING CUTTING WHEEL HYDRAULIC PRESSURE MAPPING
    // =========================================================================
    // Update circular buffer
    aLeftPressHistory[iPressIndex] := rLeftCutterPressure_bar;
    aRightPressHistory[iPressIndex] := rRightCutterPressure_bar;
    iPressIndex := (iPressIndex + 1) MOD 10;
    
    // Calculate averages
    rAvgLeftPress := 0.0;
    rAvgRightPress := 0.0;
    FOR i := 0 TO 9 DO
        rAvgLeftPress := rAvgLeftPress + aLeftPressHistory[i];
        rAvgRightPress := rAvgRightPress + aRightPressHistory[i];
    END_FOR;
    rAvgLeftPress := rAvgLeftPress / 10.0;
    rAvgRightPress := rAvgRightPress / 10.0;
    
    // Bedrock Detection
    IF (rAvgLeftPress > rCutterPressureThreshold) AND (rAvgRightPress > rCutterPressureThreshold) THEN
        bBedrockDetected := TRUE;
    ELSE
        bBedrockDetected := FALSE;
    END_IF;

    // Torque Control based on pressure (reduce torque if approaching stall)
    IF bBedrockDetected THEN
        rLeftCutterTorque_pct := 80.0; // High torque for rock
        rRightCutterTorque_pct := 80.0;
    ELSE
        rLeftCutterTorque_pct := 50.0; // Standard soil
        rRightCutterTorque_pct := 50.0;
    END_IF;

    // =========================================================================
    // 2. BENTONITE SLURRY CIRCULATION & DESANDING PLANT DENSITY CONTROL
    // =========================================================================
    // Calculate how much cuttings we are picking up
    rDensityError := rSlurryDensityOut_gcm3 - rTargetDensityOut_gcm3;
    
    // If output density is too high, increase pump speed to dilute and clear trench
    IF rDensityError > 0.0 THEN
        rSlurryPumpSpeed_pct := 50.0 + (rDensityError * rKp_Slurry);
    ELSE
        rSlurryPumpSpeed_pct := 50.0; // Baseline circulation
    END_IF;
    
    // Limit pump speed
    IF rSlurryPumpSpeed_pct > 100.0 THEN
        rSlurryPumpSpeed_pct := 100.0;
    ELSIF rSlurryPumpSpeed_pct < 20.0 THEN
        rSlurryPumpSpeed_pct := 20.0; // Minimum flow to prevent settlement
    END_IF;
    
    bDensityAlarm := (rSlurryDensityOut_gcm3 > 1.4); // Critical density jam risk

    // =========================================================================
    // 3. Z-AXIS VERTICALITY CLOSED-LOOP CORRECTION
    // =========================================================================
    rErrorX := 0.0 - rInclinometerX_deg; // Target is perfectly vertical (0.0 deg)
    rErrorY := 0.0 - rInclinometerY_deg;
    
    // Warning flag
    bVerticalityWarning := (ABS(rErrorX) > rVerticalityTolerance_deg) OR (ABS(rErrorY) > rVerticalityTolerance_deg);
    
    // X-Axis PI Control
    IF ABS(rErrorX) > 0.02 THEN
        rIntegralX := rIntegralX + (rErrorX * (rCycleTime_ms / 1000.0));
    END_IF;
    // Anti-windup
    IF rIntegralX > 20.0 THEN rIntegralX := 20.0; END_IF;
    IF rIntegralX < -20.0 THEN rIntegralX := -20.0; END_IF;
    
    rCtrlX := (rKp_Steering * rErrorX) + (rKi_Steering * rIntegralX);
    IF rCtrlX > rMaxSteering THEN rCtrlX := rMaxSteering; END_IF;
    IF rCtrlX < -rMaxSteering THEN rCtrlX := -rMaxSteering; END_IF;
    
    IF rCtrlX > 0.0 THEN
        rSteerFlapX_pos_pct := rCtrlX;
        rSteerFlapX_neg_pct := 0.0;
    ELSE
        rSteerFlapX_pos_pct := 0.0;
        rSteerFlapX_neg_pct := ABS(rCtrlX);
    END_IF;

    // Y-Axis PI Control
    IF ABS(rErrorY) > 0.02 THEN
        rIntegralY := rIntegralY + (rErrorY * (rCycleTime_ms / 1000.0));
    END_IF;
    // Anti-windup
    IF rIntegralY > 20.0 THEN rIntegralY := 20.0; END_IF;
    IF rIntegralY < -20.0 THEN rIntegralY := -20.0; END_IF;
    
    rCtrlY := (rKp_Steering * rErrorY) + (rKi_Steering * rIntegralY);
    IF rCtrlY > rMaxSteering THEN rCtrlY := rMaxSteering; END_IF;
    IF rCtrlY < -rMaxSteering THEN rCtrlY := -rMaxSteering; END_IF;
    
    IF rCtrlY > 0.0 THEN
        rSteerFlapY_pos_pct := rCtrlY;
        rSteerFlapY_neg_pct := 0.0;
    ELSE
        rSteerFlapY_pos_pct := 0.0;
        rSteerFlapY_neg_pct := ABS(rCtrlY);
    END_IF;

END_FUNCTION_BLOCK
```"""

entry = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": response}
    ]
}

target_file = r'c:\Users\majip\Downloads\LLM REASEARCH\Local_Ollama_Evol_Pipeline\seeds\tier1_enterprise_grade\synthetic_generation_v3_enterprise.jsonl'
with open(target_file, 'a', encoding='utf-8') as f:
    f.write(json.dumps(entry) + '\n')

print("Hydrofraise Controller evolution complete.")
