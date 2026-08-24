import json

user_content = """You are acting as a Lead Metallurgical Engineer for an Aluminum Smelter. Evolve a basic power loop into an AP60 Aluminum Reduction Cell Controller in IEC 61131-3 Structured Text. Technical Specs:
1. Anode effect prediction using pot voltage resistance spikes.
2. Alumina point-feeder crust-breaking synchronization.
3. 500kA DC busbar magnetic compensation."""

assistant_content = """```iecst
(*
================================================================================
AP60 ALUMINUM REDUCTION CELL CONTROLLER - ADVANCED CONTROL MODULE
================================================================================
Version: 3.2 (Enterprise Grade)
Target Platform: IEC 61131-3 Compliant High-Performance PAC
Application: AP60 Aluminum Smelting Technology (500 kA Class)

DESCRIPTION:
This function block manages the core regulatory and supervisory control for an
AP60 aluminum reduction cell. It integrates pseudo-resistance monitoring,
anode effect prediction, alumina point-feeding with crust breaking, and
magnetic field compensation for the 500kA DC busbar network.

FEATURES:
1. Anode Effect (AE) Prediction via micro-resistance (μΩ) spike analysis.
2. Synchronized Alumina Point-Feeding and Crust Breaking Sequence.
3. 500kA DC Busbar Magnetic Compensation via dynamic anode positioning.
================================================================================
*)

FUNCTION_BLOCK FB_AP60_Cell_Controller
VAR_INPUT
    bEnable                 : BOOL;          // Enable controller
    rPotVoltage             : REAL;          // Cell voltage (V)
    rLineCurrent            : REAL;          // Potline current (kA) - Nominal 500kA
    rTargetResistance       : REAL;          // Target pseudo-resistance (μΩ)
    bCrustBreakerAck        : ARRAY[1..6] OF BOOL; // Acknowledgment from 6 crust breakers
    rBusbarMagneticFlux     : REAL;          // Measured magnetic flux density (mT)
END_VAR

VAR_OUTPUT
    bAnodeEffectWarning     : BOOL;          // Early warning for Anode Effect
    bAnodeEffectActive      : BOOL;          // Anode Effect condition detected
    bPointFeederCmd         : ARRAY[1..6] OF BOOL; // Commands to 6 point feeders
    bCrustBreakerCmd        : ARRAY[1..6] OF BOOL; // Commands to 6 crust breakers
    rAnodePositionMove      : REAL;          // Anode beam adjustment command (mm)
    rActualResistance       : REAL;          // Calculated pseudo-resistance (μΩ)
    iActiveControlState     : INT;           // Current state machine state
END_VAR

VAR
    // Pseudo-resistance calculation variables
    rBackEMF                : REAL := 1.65;  // Extrapolated back EMF for Hall-Héroult (V)
    rResFilterBuffer        : ARRAY[1..10] OF REAL;
    iFilterIdx              : INT := 1;
    rFilteredResistance     : REAL;
    rResRateOfChange        : REAL;
    rLastResistance         : REAL;
    
    // Anode Effect Prediction thresholds
    c_rAEPredictSlope       : REAL := 0.05;  // μΩ/s threshold for AE prediction
    c_rAEVoltageThreshold   : REAL := 8.0;   // V threshold for full AE
    
    // Feeding sequence state machine
    iFeedState              : INT := 0;
    tFeedTimer              : TON;
    tBreakerTimer           : TON;
    iCurrentFeeder          : INT := 1;
    
    // Magnetic compensation
    c_rMagCompGain          : REAL := 0.015; // mm/mT gain for anode positioning
    rBaselineFlux           : REAL := 25.0;  // Expected baseline flux (mT)
    rAnodePosOffset         : REAL;          // Calculated compensation offset
    
    // Timers
    tCycleTime              : TON;
END_VAR

(* -----------------------------------------------------------------------------
   1. PSEUDO-RESISTANCE & ANODE EFFECT PREDICTION
   ----------------------------------------------------------------------------- *)
// Protect against division by zero
IF rLineCurrent > 10.0 THEN
    // Calculate pseudo-resistance R = (V - BackEMF) / I
    // Result in micro-Ohms (μΩ) when V is Volts and I is kA
    rActualResistance := (rPotVoltage - rBackEMF) / (rLineCurrent / 1000.0);
ELSE
    rActualResistance := 0.0;
END_IF;

// Moving average filter for resistance (10 samples)
rResFilterBuffer[iFilterIdx] := rActualResistance;
iFilterIdx := iFilterIdx + 1;
IF iFilterIdx > 10 THEN
    iFilterIdx := 1;
END_IF;

rFilteredResistance := 0.0;
FOR iFilterIdx := 1 TO 10 DO
    rFilteredResistance := rFilteredResistance + rResFilterBuffer[iFilterIdx];
END_FOR;
rFilteredResistance := rFilteredResistance / 10.0;

// Calculate Rate of Change (Derivative)
// Assuming 1s cycle time for derivative calculation
tCycleTime(IN:= NOT tCycleTime.Q, PT:= T#1S);
IF tCycleTime.Q THEN
    rResRateOfChange := rFilteredResistance - rLastResistance;
    rLastResistance := rFilteredResistance;
END_IF;

// Anode Effect Detection Logic
IF rPotVoltage > c_rAEVoltageThreshold THEN
    bAnodeEffectActive := TRUE;
    bAnodeEffectWarning := FALSE;
ELSIF rResRateOfChange > c_rAEPredictSlope AND rFilteredResistance > (rTargetResistance * 1.1) THEN
    bAnodeEffectWarning := TRUE;
    bAnodeEffectActive := FALSE;
ELSE
    bAnodeEffectWarning := FALSE;
    bAnodeEffectActive := FALSE;
END_IF;

(* -----------------------------------------------------------------------------
   2. ALUMINA POINT-FEEDER & CRUST BREAKING SYNCHRONIZATION
   ----------------------------------------------------------------------------- *)
// State machine for feeding control
// 0: Idle, 1: Break Crust, 2: Feed Alumina, 3: Retract/Wait
CASE iFeedState OF
    0: // Idle / Check if feeding is required
        // Overfeed if Anode Effect is predicted (Quenching)
        IF bAnodeEffectWarning OR (rFilteredResistance > rTargetResistance) THEN
            iFeedState := 1;
        END_IF;
        
    1: // Fire Crust Breaker
        bCrustBreakerCmd[iCurrentFeeder] := TRUE;
        tBreakerTimer(IN:= TRUE, PT:= T#2S);
        
        IF bCrustBreakerAck[iCurrentFeeder] AND tBreakerTimer.Q THEN
            tBreakerTimer(IN:= FALSE);
            iFeedState := 2;
        END_IF;
        
    2: // Inject Alumina
        bPointFeederCmd[iCurrentFeeder] := TRUE;
        tFeedTimer(IN:= TRUE, PT:= T#1S); // 1kg dose typically takes ~1s
        
        IF tFeedTimer.Q THEN
            tFeedTimer(IN:= FALSE);
            bPointFeederCmd[iCurrentFeeder] := FALSE;
            bCrustBreakerCmd[iCurrentFeeder] := FALSE; // Retract breaker
            iFeedState := 3;
        END_IF;
        
    3: // Transition to next feeder
        iCurrentFeeder := iCurrentFeeder + 1;
        IF iCurrentFeeder > 6 THEN
            iCurrentFeeder := 1;
        END_IF;
        // Wait before next feed cycle
        tFeedTimer(IN:= TRUE, PT:= T#10S);
        IF tFeedTimer.Q THEN
            tFeedTimer(IN:= FALSE);
            iFeedState := 0;
        END_IF;
END_CASE;
iActiveControlState := iFeedState;

(* -----------------------------------------------------------------------------
   3. 500kA DC BUSBAR MAGNETIC COMPENSATION
   ----------------------------------------------------------------------------- *)
// High DC currents (500kA) create massive magnetic fields which distort the 
// metal pad (metal heave). We compensate by adjusting the local anode-cathode 
// distance (ACD) based on magnetic flux deviations.

IF bEnable THEN
    // Calculate magnetic deviation
    rAnodePosOffset := (rBusbarMagneticFlux - rBaselineFlux) * c_rMagCompGain;
    
    // Standard resistance tracking + magnetic compensation offset
    // Limits applied to prevent excessive beam movement
    IF (rFilteredResistance > rTargetResistance + 0.5) THEN
        rAnodePositionMove := -1.0 + rAnodePosOffset; // Move Down
    ELSIF (rFilteredResistance < rTargetResistance - 0.5) THEN
        rAnodePositionMove := 1.0 + rAnodePosOffset; // Move Up
    ELSE
        rAnodePositionMove := 0.0 + rAnodePosOffset; // Hold with magnetic comp
    END_IF;
    
    // Hard limits on movement per cycle (-5mm to +5mm)
    IF rAnodePositionMove > 5.0 THEN rAnodePositionMove := 5.0; END_IF;
    IF rAnodePositionMove < -5.0 THEN rAnodePositionMove := -5.0; END_IF;
ELSE
    rAnodePositionMove := 0.0;
    bAnodeEffectWarning := FALSE;
    FOR iCurrentFeeder := 1 TO 6 DO
        bCrustBreakerCmd[iCurrentFeeder] := FALSE;
        bPointFeederCmd[iCurrentFeeder] := FALSE;
    END_FOR;
END_IF;
```"""

obj = {
    "messages": [
        {"role": "user", "content": user_content},
        {"role": "assistant", "content": assistant_content}
    ]
}

file_path = r"c:\Users\majip\Downloads\LLM REASEARCH\Local_Ollama_Evol_Pipeline\data\synthetic_generation_v3_enterprise.jsonl"
with open(file_path, "a", encoding="utf-8") as f:
    f.write(json.dumps(obj) + "\n")

print("Done")
