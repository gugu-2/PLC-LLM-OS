import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Continuous Catalyst Regeneration (CCR) Reformer.
Task: Invent a highly complex control scenario for this domain (e.g., catalyst lift gas velocity tracking, regeneration air lock sequencing, and multi-zone thermal profiling).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O.
"""

response = """```iec-st
FUNCTION_BLOCK FB_CCR_Reformer_Control
TITLE = 'Continuous Catalyst Regeneration (CCR) Reformer Control'
VERSION : '1.0'

VAR_INPUT
    StartSequence : BOOL; // Start the regeneration sequence
    LiftGasFlowRate : REAL; // Current lift gas flow rate (kg/h)
    LiftGasTemp : REAL; // Lift gas temperature (C)
    Zone1_Temp : REAL; // Burn zone 1 temperature (C)
    Zone2_Temp : REAL; // Burn zone 2 temperature (C)
    Zone3_Temp : REAL; // Chlorination zone temperature (C)
    Zone4_Temp : REAL; // Drying zone temperature (C)
    UpperLockHopperLevel : REAL; // Level of catalyst in upper lock hopper (%)
    LowerLockHopperLevel : REAL; // Level of catalyst in lower lock hopper (%)
    ReactorPressure : REAL; // System pressure (kPa)
    RegeneratorPressure : REAL; // Regenerator pressure (kPa)
    O2Analyzer_BurnZone : REAL; // O2 concentration in burn zone (%)
    MoistureAnalyzer : REAL; // Moisture content in drying zone (ppm)
END_VAR

VAR_OUTPUT
    LiftGasValvePos : REAL; // Output to lift gas control valve (0-100%)
    AirLockUpperValve : BOOL; // Upper air lock valve command
    AirLockLowerValve : BOOL; // Lower air lock valve command
    HeaterZone1_Output : REAL; // Heater control for zone 1 (0-100%)
    HeaterZone2_Output : REAL; // Heater control for zone 2 (0-100%)
    HeaterZone3_Output : REAL; // Heater control for zone 3 (0-100%)
    HeaterZone4_Output : REAL; // Heater control for zone 4 (0-100%)
    RegenAirBlowerSpeed : REAL; // Regeneration air blower speed command (RPM)
    SystemAlarm : BOOL; // System general alarm
    AlarmCode : INT; // Specific alarm code
    SequenceState : INT; // Current step in the sequence
END_VAR

VAR
    TargetLiftVelocity : REAL := 15.5; // m/s target
    CalculatedVelocity : REAL;
    Kp_Lift : REAL := 0.5;
    Ki_Lift : REAL := 0.02;
    Error_Lift : REAL;
    Integral_Lift : REAL := 0.0;
    
    // Thermal Profile Targets
    Target_Z1 : REAL := 480.0;
    Target_Z2 : REAL := 520.0;
    Target_Z3 : REAL := 510.0;
    Target_Z4 : REAL := 540.0;
    
    // Timers
    UpperValveTimer : TON;
    LowerValveTimer : TON;
    PurgeTimer : TON;
    
    // Internal States
    LockHopperState : INT := 0; // 0=Idle, 1=Fill, 2=Purge, 3=Dump
    
    // Interlocks
    PressureDiff : REAL;
END_VAR

(* 
    SECTION 1: Catalyst Lift Gas Velocity Tracking 
    Calculates velocity and uses PI control for the lift gas valve.
*)
CalculatedVelocity := (LiftGasFlowRate * (LiftGasTemp + 273.15)) / (ReactorPressure * 0.035); // Simplified equation

Error_Lift := TargetLiftVelocity - CalculatedVelocity;
Integral_Lift := Integral_Lift + (Error_Lift * 0.1); // Assuming 100ms task cycle

IF Integral_Lift > 100.0 THEN Integral_Lift := 100.0; END_IF;
IF Integral_Lift < -100.0 THEN Integral_Lift := -100.0; END_IF;

LiftGasValvePos := (Kp_Lift * Error_Lift) + (Ki_Lift * Integral_Lift);
IF LiftGasValvePos > 100.0 THEN LiftGasValvePos := 100.0; END_IF;
IF LiftGasValvePos < 0.0 THEN LiftGasValvePos := 0.0; END_IF;

(*
    SECTION 2: Regeneration Air Lock Sequencing
    Manages the catalyst lock hoppers with pressure equalization.
*)
PressureDiff := ReactorPressure - RegeneratorPressure;

CASE LockHopperState OF
    0: // Idle
        AirLockUpperValve := FALSE;
        AirLockLowerValve := FALSE;
        IF StartSequence AND UpperLockHopperLevel < 90.0 THEN
            LockHopperState := 1;
        END_IF;
        
    1: // Fill Upper Lock Hopper
        AirLockUpperValve := TRUE;
        IF UpperLockHopperLevel >= 90.0 THEN
            AirLockUpperValve := FALSE;
            LockHopperState := 2;
        END_IF;
        
    2: // Purge and Equalize
        PurgeTimer(IN:=TRUE, PT:=T#30S);
        IF PurgeTimer.Q THEN
            PurgeTimer(IN:=FALSE);
            IF ABS(PressureDiff) < 10.0 THEN
                LockHopperState := 3;
            ELSE
                SystemAlarm := TRUE;
                AlarmCode := 101; // Equalization failure
                LockHopperState := 0;
            END_IF;
        END_IF;
        
    3: // Dump to Lower Lock Hopper
        AirLockLowerValve := TRUE;
        IF UpperLockHopperLevel <= 5.0 THEN
            AirLockLowerValve := FALSE;
            LockHopperState := 0;
        END_IF;
ELSE
    LockHopperState := 0;
END_CASE;

SequenceState := LockHopperState;

(*
    SECTION 3: Multi-Zone Thermal Profiling
    Independent proportional control for multiple regeneration zones.
*)
// Zone 1: Upper Burn
HeaterZone1_Output := (Target_Z1 - Zone1_Temp) * 2.5;
IF HeaterZone1_Output > 100.0 THEN HeaterZone1_Output := 100.0; ELSIF HeaterZone1_Output < 0.0 THEN HeaterZone1_Output := 0.0; END_IF;

// Zone 2: Lower Burn
HeaterZone2_Output := (Target_Z2 - Zone2_Temp) * 3.0;
IF HeaterZone2_Output > 100.0 THEN HeaterZone2_Output := 100.0; ELSIF HeaterZone2_Output < 0.0 THEN HeaterZone2_Output := 0.0; END_IF;

// Zone 3: Chlorination
HeaterZone3_Output := (Target_Z3 - Zone3_Temp) * 2.0;
IF HeaterZone3_Output > 100.0 THEN HeaterZone3_Output := 100.0; ELSIF HeaterZone3_Output < 0.0 THEN HeaterZone3_Output := 0.0; END_IF;

// Zone 4: Drying
HeaterZone4_Output := (Target_Z4 - Zone4_Temp) * 1.5;
IF HeaterZone4_Output > 100.0 THEN HeaterZone4_Output := 100.0; ELSIF HeaterZone4_Output < 0.0 THEN HeaterZone4_Output := 0.0; END_IF;

(* Safety Interlocks *)
IF O2Analyzer_BurnZone > 1.2 THEN
    SystemAlarm := TRUE;
    AlarmCode := 201; // High O2
    RegenAirBlowerSpeed := 0.0; // Cut blower
ELSE
    // Normal operation blower speed control
    RegenAirBlowerSpeed := 1500.0 + (O2Analyzer_BurnZone * 100.0);
    IF RegenAirBlowerSpeed > 3000.0 THEN RegenAirBlowerSpeed := 3000.0; END_IF;
END_IF;

IF Zone1_Temp > 600.0 OR Zone2_Temp > 600.0 OR Zone3_Temp > 600.0 OR Zone4_Temp > 600.0 THEN
    SystemAlarm := TRUE;
    AlarmCode := 301; // High Temperature Trip
    HeaterZone1_Output := 0.0;
    HeaterZone2_Output := 0.0;
    HeaterZone3_Output := 0.0;
    HeaterZone4_Output := 0.0;
END_IF;

END_FUNCTION_BLOCK
```"""

import os
os.makedirs('data/swarm_raw', exist_ok=True)
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": response}]}
with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
    json.dump(record, f)
print("SUCCESS")
