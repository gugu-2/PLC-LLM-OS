import json
import os

data = {
    "messages": [
        {
            "role": "user",
            "content": "You are acting as a Chief Chemical Engineer for a Cryogenic Air Separation Unit (ASU). Evolve a basic temperature loop into a massive Fractional Distillation Controller. Technical Specs:\n1. Liquid Oxygen (LOX) and Liquid Nitrogen (LIN) boiling point phase-state tracking based on column pressure.\n2. Expansion turbine bypass valve algorithms for cold-box temperature tuning.\n3. Argon rectification column side-draw control."
        },
        {
            "role": "assistant",
            "content": """Here is the advanced implementation of the Fractional Distillation Controller for a Cryogenic Air Separation Unit, written in IEC 61131-3 Structured Text (SCL).

```pascal
FUNCTION_BLOCK FB_ASU_FractionalDistillation
TITLE = 'Cryogenic Air Separation Unit - Advanced Fractional Distillation Controller'
AUTHOR : 'Lumina Elite Synthetic Data Architect'
VERSION : '3.0'

VAR_INPUT
    // Process Variables
    rMainColumnPressure      : REAL; // barg
    rMainColumnTemp          : REAL; // K
    rArgonColumnPressure     : REAL; // barg
    rExpanderInletTemp       : REAL; // K
    rColdBoxTemp             : REAL; // K
    rFeedAirFlow             : REAL; // Nm3/h
    rArgonDrawRatio          : REAL; // Setpoint ratio %
    
    // Commands
    xEnableControl           : BOOL;
    xEmergencyShutdown       : BOOL;
END_VAR

VAR_OUTPUT
    // Valve Commands (0-100%)
    rLINRefluxValve          : REAL; 
    rLOXBoiloffValve         : REAL;
    rExpanderBypassValve     : REAL;
    rArgonSideDrawValve      : REAL;
    
    // Status
    rCalculatedLIN_BP        : REAL; // Boiling point of LIN at current pressure (K)
    rCalculatedLOX_BP        : REAL; // Boiling point of LOX at current pressure (K)
    xPhaseWarning            : BOOL; // TRUE if column temp out of phase window
    xArgonPurityInterlock    : BOOL; 
END_VAR

VAR
    // Internal States
    rColdBoxTempSP           : REAL := 95.0; // Target cold box temp (K)
    rExpanderPID_Error       : REAL;
    rExpanderPID_Integral    : REAL;
    rExpanderPID_Prop        : REAL;
    
    rRefluxPID_Error         : REAL;
    rRefluxPID_Integral      : REAL;
    rRefluxPID_Prop          : REAL;
    
    // Constants for Antoine Equation (Simplified for Cryo ranges)
    // P = 10^(A - B/(T+C)) => T = B/(A - log10(P)) - C
    c_LIN_A : REAL := 3.933; 
    c_LIN_B : REAL := 253.87;
    c_LIN_C : REAL := -4.16;
    
    c_LOX_A : REAL := 4.072;
    c_LOX_B : REAL := 338.45;
    c_LOX_C : REAL := -3.73;
    
    rAbsPressure : REAL;
    rLogP : REAL;
END_VAR

BEGIN
// Global Interlocks
IF xEmergencyShutdown THEN
    rLINRefluxValve := 100.0; // Max reflux to save column profile
    rLOXBoiloffValve := 0.0;
    rExpanderBypassValve := 100.0; // Bypass expander to shut down cooling
    rArgonSideDrawValve := 0.0;
    xPhaseWarning := TRUE;
    RETURN;
END_IF;

IF NOT xEnableControl THEN
    rLINRefluxValve := 0.0;
    rLOXBoiloffValve := 0.0;
    rExpanderBypassValve := 100.0;
    rArgonSideDrawValve := 0.0;
    RETURN;
END_IF;

// 1. LOX and LIN Boiling Point Phase-State Tracking
// Convert barg to absolute pressure (assuming 1.013 bar atm)
rAbsPressure := rMainColumnPressure + 1.013;

IF rAbsPressure > 0.1 THEN
    // Base-10 log approx for Antoine Equation tracking
    rLogP := LOG(rAbsPressure);
    
    // LIN Boiling Point Tracking (Nitrogen saturation curve)
    rCalculatedLIN_BP := c_LIN_B / (c_LIN_A - rLogP) - c_LIN_C;
    
    // LOX Boiling Point Tracking (Oxygen saturation curve)
    rCalculatedLOX_BP := c_LOX_B / (c_LOX_A - rLogP) - c_LOX_C;
ELSE
    rCalculatedLIN_BP := 77.36; // Standard BP at 1 atm
    rCalculatedLOX_BP := 90.19; // Standard BP at 1 atm
END_IF;

// Phase Warning Logic: 
// Ensure column temperature gradient is between LIN and LOX boiling points
IF (rMainColumnTemp < (rCalculatedLIN_BP - 2.0)) OR (rMainColumnTemp > (rCalculatedLOX_BP + 2.0)) THEN
    xPhaseWarning := TRUE;
ELSE
    xPhaseWarning := FALSE;
END_IF;

// Reflux Control (Basic PI loop mapping temp error to LOX/LIN balance)
rRefluxPID_Error := rMainColumnTemp - ((rCalculatedLIN_BP + rCalculatedLOX_BP) / 2.0);
rRefluxPID_Prop := rRefluxPID_Error * 5.0; // Kp = 5.0
rRefluxPID_Integral := rRefluxPID_Integral + (rRefluxPID_Error * 0.1); // Ki = 0.1

rLINRefluxValve := rRefluxPID_Prop + rRefluxPID_Integral + 50.0; // Base 50% valve position

// Anti-windup and limits for Reflux Valve
IF rLINRefluxValve > 100.0 THEN
    rLINRefluxValve := 100.0;
    rRefluxPID_Integral := rRefluxPID_Integral - (rRefluxPID_Error * 0.1);
ELSIF rLINRefluxValve < 0.0 THEN
    rLINRefluxValve := 0.0;
    rRefluxPID_Integral := rRefluxPID_Integral - (rRefluxPID_Error * 0.1);
END_IF;

// 2. Expansion Turbine Bypass Valve Algorithms for Cold-Box Tuning
// If cold box is too warm, close bypass to push more flow through expander (more cooling)
// If cold box is too cold, open bypass
rExpanderPID_Error := rColdBoxTemp - rColdBoxTempSP; // Positive if too warm
rExpanderPID_Prop := rExpanderPID_Error * -10.0; // Negative gain: open bypass if too cold
rExpanderPID_Integral := rExpanderPID_Integral + (rExpanderPID_Error * -0.5);

rExpanderBypassValve := rExpanderPID_Prop + rExpanderPID_Integral + 30.0; // Nominal 30% bypass

// Anti-windup for Expander Bypass Valve
IF rExpanderBypassValve > 100.0 THEN
    rExpanderBypassValve := 100.0;
    rExpanderPID_Integral := rExpanderPID_Integral - (rExpanderPID_Error * -0.5);
ELSIF rExpanderBypassValve < 0.0 THEN
    rExpanderBypassValve := 0.0;
    rExpanderPID_Integral := rExpanderPID_Integral - (rExpanderPID_Error * -0.5);
END_IF;

// 3. Argon Rectification Column Side-Draw Control
// Argon accumulates at the belly of the LP column (around 87-89K)
// Flow draw is ratioed to feed air flow, modified by main column thermal profile.
IF NOT xPhaseWarning THEN
    rArgonSideDrawValve := (rFeedAirFlow / 100000.0) * rArgonDrawRatio;
    xArgonPurityInterlock := FALSE;
ELSE
    // If main column is unstable, stop argon draw to prevent oxygen punch-through to Argon column
    rArgonSideDrawValve := 0.0;
    xArgonPurityInterlock := TRUE;
END_IF;

// Final scaling and limits for Argon Draw Valve
IF rArgonSideDrawValve > 100.0 THEN
    rArgonSideDrawValve := 100.0;
ELSIF rArgonSideDrawValve < 0.0 THEN
    rArgonSideDrawValve := 0.0;
END_IF;

END_FUNCTION_BLOCK
```"""
        }
    ]
}

file_path = r"c:\Users\majip\Downloads\LLM REASEARCH\data\synthetic_generation_v3_enterprise.jsonl"
with open(file_path, "a", encoding="utf-8") as f:
    f.write(json.dumps(data) + "\n")
