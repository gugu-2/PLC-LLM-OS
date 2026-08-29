import json, uuid, os

st_code = """```iec-st
FUNCTION_BLOCK FB_CBW_Controller
(*
    Continuous Batch Washer (CBW) Industrial Laundry Controller
    Manages multi-compartment counterflow water cascading, 
    variable chemical dosing integration, and hydraulic cake press.
*)
VAR_INPUT
    bEnable                 : BOOL; // System enable
    bEStop                  : BOOL; // Emergency stop
    rMainWaterTemp          : REAL; // Incoming water temperature (C)
    rMainWaterPressure      : REAL; // Main water pressure (Bar)
    arrCompartmentTemp      : ARRAY[1..12] OF REAL; // Temp per compartment
    arrCompartmentPh        : ARRAY[1..12] OF REAL; // pH per compartment
    arrLoadWeight           : ARRAY[1..12] OF REAL; // Load weight per compartment (kg)
    bCakePressReady         : BOOL; // Press ready signal
    rCakePressPressure      : REAL; // Current press pressure
END_VAR

VAR_OUTPUT
    bSystemReady            : BOOL; // System ready for next batch
    arrHeaterValves         : ARRAY[1..12] OF BOOL; // Steam valves for heating
    arrWaterTransfer        : ARRAY[1..11] OF BOOL; // Transfer pumps/valves between compartments
    arrChemicalDoseValves   : ARRAY[1..4] OF BOOL; // Alkali, Detergent, Bleach, Sour
    rChemicalDoseRate       : ARRAY[1..4] OF REAL; // Dose rates (ml/min)
    bCakePressStart         : BOOL; // Start press cycle
    nActiveAlarms           : INT; // Number of active alarms
END_VAR

VAR
    i                       : INT;
    rTargetTemp             : ARRAY[1..12] OF REAL := [30.0, 40.0, 50.0, 60.0, 70.0, 75.0, 75.0, 65.0, 50.0, 40.0, 30.0, 25.0];
    rTargetPh               : ARRAY[1..12] OF REAL := [7.0, 8.5, 9.5, 10.5, 11.0, 11.0, 10.5, 9.0, 8.0, 7.0, 6.0, 5.5];
    tStateTimer             : TON;
    nState                  : INT := 0; // 0: Idle, 1: Fill, 2: Wash/Dose, 3: Transfer, 4: Press
    bAlarmState             : BOOL;
END_VAR

// Main Logic
IF bEStop THEN
    nState := 0;
    bSystemReady := FALSE;
    bCakePressStart := FALSE;
    FOR i := 1 TO 12 DO
        arrHeaterValves[i] := FALSE;
        IF i < 12 THEN arrWaterTransfer[i] := FALSE; END_IF
    END_FOR
    FOR i := 1 TO 4 DO
        arrChemicalDoseValves[i] := FALSE;
        rChemicalDoseRate[i] := 0.0;
    END_FOR
    RETURN;
END_IF;

IF bEnable THEN
    CASE nState OF
        0: // Idle
            bSystemReady := TRUE;
            IF rMainWaterPressure > 2.0 AND bCakePressReady THEN
                nState := 1;
            END_IF;
            
        1: // Temp Control & Counterflow Water Cascade
            bSystemReady := FALSE;
            FOR i := 1 TO 12 DO
                // Bang-bang temp control with hysteresis
                IF arrCompartmentTemp[i] < (rTargetTemp[i] - 2.0) THEN
                    arrHeaterValves[i] := TRUE;
                ELSIF arrCompartmentTemp[i] >= rTargetTemp[i] THEN
                    arrHeaterValves[i] := FALSE;
                END_IF;
            END_FOR;
            // Activate cascading pumps
            FOR i := 2 TO 12 DO
                arrWaterTransfer[i-1] := TRUE;
            END_FOR;
            
            tStateTimer(IN:=TRUE, PT:=T#60S);
            IF tStateTimer.Q THEN
                tStateTimer(IN:=FALSE);
                nState := 2;
            END_IF;
            
        2: // Chemical Dosing based on pH and weight
            FOR i := 1 TO 4 DO
                arrChemicalDoseValves[i] := TRUE;
                // Calculate rate based on load weight in primary wash (e.g. comp 4)
                rChemicalDoseRate[i] := arrLoadWeight[4] * 0.5; 
            END_FOR;
            
            tStateTimer(IN:=TRUE, PT:=T#120S);
            IF tStateTimer.Q THEN
                tStateTimer(IN:=FALSE);
                FOR i := 1 TO 4 DO
                    arrChemicalDoseValves[i] := FALSE;
                    rChemicalDoseRate[i] := 0.0;
                END_FOR;
                nState := 3;
            END_IF;
            
        3: // Load Transfer
            // Simulated load transfer delay
            tStateTimer(IN:=TRUE, PT:=T#30S);
            IF tStateTimer.Q THEN
                tStateTimer(IN:=FALSE);
                nState := 4;
            END_IF;
            
        4: // Cake Press integration
            IF bCakePressReady THEN
                bCakePressStart := TRUE;
                IF rCakePressPressure >= 40.0 THEN // Max pressure reached
                    bCakePressStart := FALSE;
                    nState := 0; // Return to idle
                END_IF;
            END_IF;
    END_CASE;
ELSE
    bSystemReady := FALSE;
    nState := 0;
END_IF;
END_FUNCTION_BLOCK
```"""

prompt = "Invent a highly complex control scenario for Continuous Batch Washer (CBW) Industrial Laundry."

os.makedirs('data/swarm_raw', exist_ok=True)
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": st_code}]}
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)
print(f"Saved to {filename}")
