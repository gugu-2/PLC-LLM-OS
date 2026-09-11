import os, json, uuid
os.makedirs('data/swarm_raw', exist_ok=True)
prompt = "You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.\nYour specific domain is: Commercial Aircraft Engine Test Cell.\nTask: Invent a highly complex control scenario for this domain (e.g., thrust dynamometer load mapping, afterburner fuel scheduling transients, and bypass ratio airflow measurement).\nWrite a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."
code = """```iec-st
FUNCTION_BLOCK FB_AeroEngineTestCell
VAR_INPUT
    bStartTest : BOOL; // Initiate test sequence
    bEmergencyStop : BOOL; // Emergency kill switch
    rTargetThrust : REAL; // Target thrust command (kN)
    rFuelFlowCmd : REAL; // Fuel flow command (kg/s)
    bEnableAfterburner : BOOL; // Afterburner trigger
    rAirflowBypassCmd : REAL; // Bypass ratio adjustment
    rDynoLoadSetPt : REAL; // Dynamometer load mapping setpoint
    rN1_Speed_Meas : REAL; // Low pressure compressor speed (RPM)
    rN2_Speed_Meas : REAL; // High pressure compressor speed (RPM)
    rEGT_Meas : REAL; // Exhaust gas temperature (C)
    rVibration_Meas : REAL; // Engine vibration (mm/s)
END_VAR
VAR_OUTPUT
    bTestActive : BOOL; // Test in progress
    bAlarmCondition : BOOL; // Safety alarm triggered
    sStatusMessage : STRING(50); // System status
    rActualThrust : REAL; // Measured thrust (kN)
    rDynoLoadApply : REAL; // Dynamometer applied load (N-m)
    rFuelValvePos : REAL; // Main fuel valve position (%)
    rABFuelValvePos : REAL; // Afterburner fuel valve pos (%)
    rBleedValvePos : REAL; // Bleed air valve pos (%)
END_VAR
VAR
    eState : INT;
    IDLE: INT := 0; SPOOL_UP: INT := 1; STABILIZE: INT := 2; THUST_MAPPING: INT := 3; AFTERBURNER_TEST: INT := 4; SHUTDOWN: INT := 5; FAULT: INT := 6;
    fbPID_Thrust : PID_CONTROLLER;
    fbPID_Fuel : PID_CONTROLLER;
    fbTimer : TON;
    rEGT_Limit : REAL := 1250.0;
    rVib_Limit : REAL := 25.0;
    rOverspeed_N1 : REAL := 11000.0;
    rOverspeed_N2 : REAL := 18000.0;
END_VAR

// Safety Interlocks
IF bEmergencyStop OR (rEGT_Meas > rEGT_Limit) OR (rVibration_Meas > rVib_Limit) OR (rN1_Speed_Meas > rOverspeed_N1) OR (rN2_Speed_Meas > rOverspeed_N2) THEN
    eState := FAULT;
END_IF;

CASE eState OF
    0: // IDLE
        bTestActive := FALSE;
        bAlarmCondition := FALSE;
        rFuelValvePos := 0.0;
        rABFuelValvePos := 0.0;
        rDynoLoadApply := 0.0;
        sStatusMessage := 'System Ready. Waiting for start.';
        IF bStartTest AND NOT bEmergencyStop THEN
            eState := SPOOL_UP;
            fbTimer(IN:=FALSE, PT:=T#0s);
        END_IF;

    1: // SPOOL_UP
        bTestActive := TRUE;
        sStatusMessage := 'Spooling up... N1/N2 increasing.';
        rFuelValvePos := rFuelValvePos + 0.5; 
        IF rFuelValvePos > 25.0 THEN
            rFuelValvePos := 25.0;
        END_IF;
        
        IF (rN1_Speed_Meas > 2000.0) AND (rN2_Speed_Meas > 5000.0) THEN
            eState := STABILIZE;
            fbTimer(IN:=TRUE, PT:=T#10s);
        END_IF;

    2: // STABILIZE
        sStatusMessage := 'Stabilizing idle parameters.';
        fbTimer(IN:=TRUE);
        IF fbTimer.Q THEN
            eState := THUST_MAPPING;
            fbTimer(IN:=FALSE, PT:=T#0s);
        END_IF;
        
    3: // THUST_MAPPING
        sStatusMessage := 'Thrust Dynamometer Load Mapping.';
        fbPID_Thrust(
            Enable := TRUE,
            Setpoint := rTargetThrust,
            Feedback := rActualThrust,
            Kp := 0.85,
            Ki := 0.15,
            Output => rFuelValvePos
        );
        rDynoLoadApply := rDynoLoadSetPt * 0.98; 
        
        IF bEnableAfterburner THEN
            eState := AFTERBURNER_TEST;
        ELSIF NOT bStartTest THEN
            eState := SHUTDOWN;
        END_IF;

    4: // AFTERBURNER_TEST
        sStatusMessage := 'Afterburner Fuel Scheduling Transients.';
        rABFuelValvePos := 100.0; 
        rBleedValvePos := rAirflowBypassCmd * 1.5; 
        fbPID_Fuel(
            Enable := TRUE,
            Setpoint := rFuelFlowCmd,
            Feedback := rFuelValvePos, 
            Kp := 1.2,
            Ki := 0.3,
            Output => rFuelValvePos
        );
        IF NOT bEnableAfterburner THEN
            rABFuelValvePos := 0.0;
            eState := THUST_MAPPING;
        END_IF;

    5: // SHUTDOWN
        sStatusMessage := 'Controlled Shutdown Sequence.';
        rFuelValvePos := rFuelValvePos - 1.0;
        rABFuelValvePos := 0.0;
        rDynoLoadApply := rDynoLoadApply * 0.5;
        IF rFuelValvePos <= 0.0 THEN
            rFuelValvePos := 0.0;
            IF (rN1_Speed_Meas < 100.0) THEN
                eState := IDLE;
                bTestActive := FALSE;
            END_IF;
        END_IF;

    6: // FAULT
        bTestActive := FALSE;
        bAlarmCondition := TRUE;
        sStatusMessage := 'EMERGENCY FAULT! Fuel Cutoff.';
        rFuelValvePos := 0.0;
        rABFuelValvePos := 0.0;
        rBleedValvePos := 100.0; 
        rDynoLoadApply := 0.0;
        IF NOT bEmergencyStop AND (rEGT_Meas < 500.0) AND (rN1_Speed_Meas < 50.0) THEN
            eState := IDLE; 
        END_IF;
END_CASE;
END_FUNCTION_BLOCK
```"""
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)
print("Done")
