import os, json, uuid

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Cryogenic Air Separation Unit (ASU).
Task: Invent a highly complex control scenario for this domain (e.g., expansion turbine RPM limits, cryogenic distillation column thermal profiles, and argon/oxygen/nitrogen fractioning).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O.
"""

response = """```iec-st
FUNCTION_BLOCK FB_ASU_Distillation_Control
TITLE = 'Cryogenic Air Separation Unit Distillation Control'
VERSION : '1.0'

VAR_INPUT
    rFeedFlow_Nm3_h     : REAL;  // Incoming compressed air flow
    rFeedTemp_C         : REAL;  // Feed temperature, typical -170 C
    rFeedPressure_kPa   : REAL;  // Feed pressure to primary column
    rTurbineSpeed_RPM   : REAL;  // Expansion turbine current speed
    rMainCol_TopTemp_C  : REAL;  // Main distillation column top temperature
    rMainCol_BotTemp_C  : REAL;  // Main distillation column bottom temperature
    rArgonDraw_Flow_Nm3 : REAL;  // Argon draw-off flow rate
    rO2_Purity_Percent  : REAL;  // Measured O2 purity at bottom
    bEmergencyStop      : BOOL;  // Emergency shutdown signal
    bStartSequence      : BOOL;  // Sequence start command
END_VAR

VAR_OUTPUT
    rTurbineValve_Pos_Pct : REAL; // Turbine inlet valve position command
    rRefluxValve_Pos_Pct  : REAL; // Nitrogen reflux valve position
    rProductO2_Valve_Pct  : REAL; // Oxygen product draw valve position
    rArgonVent_Valve_Pct  : REAL; // Argon column vent valve position
    bTurbineTrip          : BOOL; // Turbine trip command
    bSystemSafe           : BOOL; // System status indicator
    iActiveState          : INT;  // Current control state machine step
END_VAR

VAR
    rPID_Error_O2         : REAL;
    rPID_Int_O2           : REAL;
    rPID_PrevErr_O2       : REAL;
    
    rPID_Error_Temp       : REAL;
    rPID_Int_Temp         : REAL;
    rPID_PrevErr_Temp     : REAL;
    
    rTargetO2Purity       : REAL := 99.6; // Minimum 99.6% purity
    rTargetTopTemp        : REAL := -195.8; // Target for LN2 reflux
    rMaxTurbineRPM        : REAL := 45000.0;
    rMinTurbineRPM        : REAL := 25000.0;
    rTurbineTripRPM       : REAL := 48000.0;
    
    rKp_O2 : REAL := 2.5;
    rKi_O2 : REAL := 0.05;
    rKd_O2 : REAL := 0.1;
    
    rKp_Temp : REAL := 1.8;
    rKi_Temp : REAL := 0.02;
    rKd_Temp : REAL := 0.05;
    
    tStateTimer : TON;
    tStabilizationTimer : TON;
    iState : INT := 0; 
END_VAR

// Constants
VAR CONSTANT
    STATE_INIT : INT := 0;
    STATE_PURGE : INT := 10;
    STATE_COOLDOWN : INT := 20;
    STATE_STEADY : INT := 30;
    STATE_SHUTDOWN : INT := 99;
END_VAR

// Control Logic
IF bEmergencyStop THEN
    iState := STATE_SHUTDOWN;
END_IF;

IF rTurbineSpeed_RPM >= rTurbineTripRPM THEN
    bTurbineTrip := TRUE;
    iState := STATE_SHUTDOWN;
ELSE
    bTurbineTrip := FALSE;
END_IF;

CASE iState OF
    STATE_INIT:
        rTurbineValve_Pos_Pct := 0.0;
        rRefluxValve_Pos_Pct := 0.0;
        rProductO2_Valve_Pct := 0.0;
        rArgonVent_Valve_Pct := 100.0; // Vent open
        bSystemSafe := TRUE;
        
        IF bStartSequence AND NOT bEmergencyStop THEN
            iState := STATE_PURGE;
        END_IF;
        
    STATE_PURGE:
        // Purging logic, simulating time delay
        tStateTimer(IN := TRUE, PT := T#30s);
        rTurbineValve_Pos_Pct := 5.0; // Minimal flow
        rArgonVent_Valve_Pct := 100.0;
        
        IF tStateTimer.Q THEN
            tStateTimer(IN := FALSE);
            iState := STATE_COOLDOWN;
        END_IF;
        
    STATE_COOLDOWN:
        // Ramp up turbine to drop temperature
        tStateTimer(IN := TRUE, PT := T#120s);
        
        IF rTurbineSpeed_RPM < rMaxTurbineRPM - 2000.0 THEN
            rTurbineValve_Pos_Pct := rTurbineValve_Pos_Pct + 0.1;
        END_IF;
        
        IF rTurbineValve_Pos_Pct > 85.0 THEN
            rTurbineValve_Pos_Pct := 85.0;
        END_IF;
        
        IF (rMainCol_BotTemp_C <= -180.0) AND (rMainCol_TopTemp_C <= -190.0) THEN
            tStateTimer(IN := FALSE);
            iState := STATE_STEADY;
        END_IF;
        
    STATE_STEADY:
        bSystemSafe := TRUE;
        
        // --- O2 Purity PID Control (Controls O2 Product Draw Valve) ---
        rPID_Error_O2 := rO2_Purity_Percent - rTargetO2Purity;
        rPID_Int_O2 := rPID_Int_O2 + rPID_Error_O2;
        
        // Anti-windup
        IF rPID_Int_O2 > 500.0 THEN rPID_Int_O2 := 500.0; END_IF;
        IF rPID_Int_O2 < -500.0 THEN rPID_Int_O2 := -500.0; END_IF;
        
        rProductO2_Valve_Pct := (rKp_O2 * rPID_Error_O2) + (rKi_O2 * rPID_Int_O2) + (rKd_O2 * (rPID_Error_O2 - rPID_PrevErr_O2));
        rPID_PrevErr_O2 := rPID_Error_O2;
        
        IF rProductO2_Valve_Pct > 100.0 THEN rProductO2_Valve_Pct := 100.0; END_IF;
        IF rProductO2_Valve_Pct < 0.0 THEN rProductO2_Valve_Pct := 0.0; END_IF;
        
        // --- Top Temperature PID Control (Controls Reflux Valve) ---
        rPID_Error_Temp := rMainCol_TopTemp_C - rTargetTopTemp;
        rPID_Int_Temp := rPID_Int_Temp + rPID_Error_Temp;
        
        // Anti-windup
        IF rPID_Int_Temp > 200.0 THEN rPID_Int_Temp := 200.0; END_IF;
        IF rPID_Int_Temp < -200.0 THEN rPID_Int_Temp := -200.0; END_IF;
        
        rRefluxValve_Pos_Pct := (rKp_Temp * rPID_Error_Temp) + (rKi_Temp * rPID_Int_Temp) + (rKd_Temp * (rPID_Error_Temp - rPID_PrevErr_Temp));
        rPID_PrevErr_Temp := rPID_Error_Temp;
        
        IF rRefluxValve_Pos_Pct > 100.0 THEN rRefluxValve_Pos_Pct := 100.0; END_IF;
        IF rRefluxValve_Pos_Pct < 10.0 THEN rRefluxValve_Pos_Pct := 10.0; END_IF; // Maintain min reflux
        
        // --- Turbine Speed Regulation ---
        IF rTurbineSpeed_RPM > rMaxTurbineRPM THEN
            rTurbineValve_Pos_Pct := rTurbineValve_Pos_Pct - 1.0;
        ELSIF rTurbineSpeed_RPM < rMinTurbineRPM THEN
            rTurbineValve_Pos_Pct := rTurbineValve_Pos_Pct + 0.5;
        END_IF;
        
        // --- Argon Side-draw Control ---
        IF rO2_Purity_Percent > 99.5 AND rArgonDraw_Flow_Nm3 > 10.0 THEN
             rArgonVent_Valve_Pct := 20.0; // Normal venting
        ELSE
             rArgonVent_Valve_Pct := 80.0; // Flush argon if O2 purity drops
        END_IF;
        
    STATE_SHUTDOWN:
        bSystemSafe := FALSE;
        rTurbineValve_Pos_Pct := 0.0;
        rRefluxValve_Pos_Pct := 0.0;
        rProductO2_Valve_Pct := 0.0;
        rArgonVent_Valve_Pct := 100.0;
        tStateTimer(IN := FALSE);
        
        IF NOT bEmergencyStop AND NOT bStartSequence THEN
            iState := STATE_INIT;
        END_IF;
        
    ELSE
        iState := STATE_SHUTDOWN;
END_CASE;

iActiveState := iState;

END_FUNCTION_BLOCK
```"""

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": response}
    ]
}

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=4)
print(f"Saved to {filename}")
