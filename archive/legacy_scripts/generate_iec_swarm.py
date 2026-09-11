import json
import uuid
import os

prompt = "Write a deterministic Structured Text (ST) FUNCTION_BLOCK for a High-Speed Web Aseptic Carton Filling Machine. Include H2O2 bath sterilization, ultrasonic sealing pressure, and volumetric servo dosing. Include complete VAR declarations."

st_code = """```iec-st
FUNCTION_BLOCK FB_AsepticWebFiller_MasterControl
TITLE = 'Aseptic Web Carton Filler - Core Process Loop'
VERSION : '1.5'

VAR_INPUT
    bEnableSystem       : BOOL;   // System Master Enable
    bEStopAct           : BOOL;   // Emergency Stop Active
    rWebSpeedSetpt      : REAL;   // Target Web Speed [m/min]
    rH2O2TempSetpt      : REAL;   // Target H2O2 Bath Temp [degC]
    rDosingVolumeSetpt  : REAL;   // Target Volume per Carton [ml]
    rSealForceSetpt     : REAL;   // Target Sealing Force [N]
    rActualWebSpeed     : REAL;   // Feedback from Web Drive Encoder
    rActualH2O2Temp     : REAL;   // RTD Feedback from H2O2 Bath
    rActualH2O2Conc     : REAL;   // H2O2 Concentration Sensor [%]
    rActualSealForce    : REAL;   // Load cell feedback [N]
    rActualDosingPos    : REAL;   // Servo position feedback [mm]
END_VAR

VAR_OUTPUT
    bReadyForProd       : BOOL;   // System Ready for Production
    bFaultActive        : BOOL;   // Fault Active
    iDosingServoCmd     : DINT;   // Command to Dosing Servo Drive
    rWebDriveSpeedCmd   : REAL;   // Command to Web Pull Drive [m/min]
    iUltrasonicAmpCmd   : INT;    // Ultrasonic Amplitude Command [0-100%]
    rH2O2HeaterCmd      : REAL;   // PID Output for Heater [0-100%]
    sCurrentState       : STRING[32]; // State Machine String
END_VAR

VAR
    eState              : (INIT, WARMUP, STERILIZE, PROD_RUN, STOPPING, FAULT);
    PID_Heater          : FB_PID; // Internal PID for H2O2 Heating
    TMR_SterilTime      : TON;
    TMR_SealDwell       : TON;
    rTempError          : REAL;
    bTempInBand         : BOOL;
    bConcInBand         : BOOL;
    rPosError           : REAL;
    rDosingScaleFact    : REAL := 2.45; // mm per ml
END_VAR

// ---------------------------------------------------------
// Main Control Logic
// ---------------------------------------------------------
IF bEStopAct THEN
    eState := FAULT;
    sCurrentState := 'EMERGENCY STOP';
END_IF;

// Safety and Interlock Monitor
bTempInBand := (rActualH2O2Temp > rH2O2TempSetpt - 2.0) AND (rActualH2O2Temp < rH2O2TempSetpt + 2.0);
bConcInBand := (rActualH2O2Conc > 34.0) AND (rActualH2O2Conc < 36.0); // 35% typical

CASE eState OF
    INIT:
        bReadyForProd := FALSE;
        bFaultActive := FALSE;
        rWebDriveSpeedCmd := 0.0;
        iDosingServoCmd := 0;
        iUltrasonicAmpCmd := 0;
        rH2O2HeaterCmd := 0.0;
        sCurrentState := 'INITIALIZATION';

        IF bEnableSystem AND NOT bEStopAct THEN
            eState := WARMUP;
        END_IF;

    WARMUP:
        sCurrentState := 'BATH WARMUP';
        // Simple P-Control for H2O2 Heater (Replace with FB_PID in real app)
        rTempError := rH2O2TempSetpt - rActualH2O2Temp;
        rH2O2HeaterCmd := LIMIT(0.0, rTempError * 15.0, 100.0);

        IF bTempInBand THEN
            TMR_SterilTime(IN:=TRUE, PT:=T#5S);
            IF TMR_SterilTime.Q THEN
                eState := STERILIZE;
            END_IF;
        ELSE
            TMR_SterilTime(IN:=FALSE);
        END_IF;

    STERILIZE:
        sCurrentState := 'STERILIZING ZONE';
        IF bConcInBand THEN
            eState := PROD_RUN;
        END_IF;

    PROD_RUN:
        sCurrentState := 'PRODUCTION RUN';
        bReadyForProd := TRUE;
        rWebDriveSpeedCmd := rWebSpeedSetpt;

        // Dosing Control
        // Calculate servo position based on volume target and scale factor
        rPosError := (rDosingVolumeSetpt * rDosingScaleFact) - rActualDosingPos;
        iDosingServoCmd := REAL_TO_DINT(LIMIT(-10000.0, rPosError * 50.0, 10000.0));

        // Ultrasonic Sealer Control based on Force Feedback
        IF rActualSealForce < rSealForceSetpt THEN
            iUltrasonicAmpCmd := iUltrasonicAmpCmd + 1; // Increase amplitude
        ELSIF rActualSealForce > rSealForceSetpt THEN
            iUltrasonicAmpCmd := iUltrasonicAmpCmd - 1; // Decrease amplitude
        END_IF;
        iUltrasonicAmpCmd := LIMIT(0, iUltrasonicAmpCmd, 100);

        IF NOT bEnableSystem THEN
            eState := STOPPING;
        END_IF;

    STOPPING:
        sCurrentState := 'SYSTEM STOPPING';
        bReadyForProd := FALSE;
        rWebDriveSpeedCmd := rWebDriveSpeedCmd - 5.0; // Ramp down
        IF rWebDriveSpeedCmd <= 0.0 THEN
            rWebDriveSpeedCmd := 0.0;
            eState := INIT;
        END_IF;

    FAULT:
        bReadyForProd := FALSE;
        bFaultActive := TRUE;
        rWebDriveSpeedCmd := 0.0;
        iDosingServoCmd := 0;
        iUltrasonicAmpCmd := 0;
        rH2O2HeaterCmd := 0.0;
        IF NOT bEStopAct AND bEnableSystem THEN
            eState := INIT;
        END_IF;

END_CASE;
END_FUNCTION_BLOCK
```"""

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": st_code}
    ]
}

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"

with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)

os.makedirs("data", exist_ok=True)
with open("data/synthetic_generation_v3_enterprise.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\n")

print(f"Successfully wrote {filename} and appended to jsonl.")
