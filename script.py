import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: 5-Axis Waterjet Profiling Machine.
Task: Invent a highly complex control scenario for this domain (e.g., high-pressure intensifier pump sequencing, abrasive garnet hopper metering, and XYZ kinematic vectoring).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O.

CRITICAL RULES:
1. You MUST output the code enclosed in a ```iec-st markdown code fence. DO NOT APOLOGIZE. DO NOT EXPLAIN.
2. The code must be >= 1500 chars, with FUNCTION_BLOCK and VAR_INPUT/VAR_OUTPUT.
3. You MUST save your JSON payload to a uniquely named file in the swarm directory using python.
"""

code = """```iec-st
FUNCTION_BLOCK FB_WaterJet_5Axis_Control
TITLE = '5-Axis Waterjet Kinematics and High-Pressure Control'
VERSION : 1.0

VAR_INPUT
    bEnableSystem : BOOL; (* Master enable for the entire waterjet cell *)
    bStartCut : BOOL; (* Cycle start command for current contour *)
    bEmergencyStop : BOOL; (* SIL3 e-stop circuit feedback *)
    rTargetX : LREAL; (* Commanded X position in mm *)
    rTargetY : LREAL; (* Commanded Y position in mm *)
    rTargetZ : LREAL; (* Commanded Z position in mm *)
    rTargetA : LREAL; (* Commanded A-axis tilt angle in degrees *)
    rTargetB : LREAL; (* Commanded B-axis rotation angle in degrees *)
    rIntensifierPressureSetpoint : LREAL; (* Target cutting pressure in Bar (e.g. 4100 Bar) *)
    rAbrasiveFeedRateSet : LREAL; (* Grams per minute of garnet abrasive *)
    iHydraulicOilTemp : INT; (* Analog input: Hydraulic fluid temperature *)
END_VAR

VAR_OUTPUT
    bSystemReady : BOOL;
    bCuttingActive : BOOL;
    bFaultActive : BOOL;
    iErrorCode : DINT;
    rCurrentPressure : LREAL; (* Actual intensifier pressure *)
    rCurrentX : LREAL;
    rCurrentY : LREAL;
    rCurrentZ : LREAL;
    rCurrentA : LREAL;
    rCurrentB : LREAL;
    q_bHighPressureValve : BOOL; (* Digital Output to HP On/Off Valve *)
    q_bAbrasiveValve : BOOL; (* Digital Output to Abrasive Metering Valve *)
    q_iIntensifierPumpVFD : INT; (* Analog Output to Pump Motor *)
END_VAR

VAR
    eState : INT := 0;
    rActualPressure : LREAL := 0.0;
    rAbrasiveHopperLevel : LREAL := 100.0; (* Simulated % full *)
    tPumpDelay : TON;
    tValveDelay : TON;
    rInterpolationStep : LREAL := 0.5;
END_VAR

VAR CONSTANT
    STATE_INIT : INT := 0;
    STATE_PUMP_STARTUP : INT := 10;
    STATE_PRESSURE_BUILDUP : INT := 20;
    STATE_READY : INT := 30;
    STATE_ABRASIVE_METERING : INT := 40;
    STATE_KINEMATIC_VECTORING : INT := 50;
    STATE_CUTTING : INT := 60;
    STATE_SHUTDOWN : INT := 70;
    STATE_FAULT : INT := 99;
    MAX_PRESSURE_BAR : LREAL := 6000.0;
END_VAR

(* Master Safety Check *)
IF bEmergencyStop OR (iHydraulicOilTemp > 75) THEN
    eState := STATE_FAULT;
    iErrorCode := 9999;
    q_bHighPressureValve := FALSE;
    q_bAbrasiveValve := FALSE;
    q_iIntensifierPumpVFD := 0;
    bSystemReady := FALSE;
    bCuttingActive := FALSE;
END_IF;

CASE eState OF
    STATE_INIT:
        bFaultActive := FALSE;
        iErrorCode := 0;
        q_bHighPressureValve := FALSE;
        q_bAbrasiveValve := FALSE;
        q_iIntensifierPumpVFD := 0;
        IF bEnableSystem AND NOT bEmergencyStop THEN
            eState := STATE_PUMP_STARTUP;
        END_IF;

    STATE_PUMP_STARTUP:
        q_iIntensifierPumpVFD := 16384; (* 50% Speed command via analog *)
        tPumpDelay(IN:=TRUE, PT:=T#5S);
        IF tPumpDelay.Q THEN
            tPumpDelay(IN:=FALSE);
            eState := STATE_PRESSURE_BUILDUP;
        END_IF;

    STATE_PRESSURE_BUILDUP:
        q_iIntensifierPumpVFD := 32767; (* 100% Speed *)
        IF rActualPressure < rIntensifierPressureSetpoint THEN
            rActualPressure := rActualPressure + 120.5; (* Simulated pressure ramp *)
        ELSE
            bSystemReady := TRUE;
            eState := STATE_READY;
        END_IF;

    STATE_READY:
        q_bHighPressureValve := FALSE;
        q_bAbrasiveValve := FALSE;
        bCuttingActive := FALSE;
        IF bStartCut AND bSystemReady THEN
            eState := STATE_ABRASIVE_METERING;
        END_IF;
        IF NOT bEnableSystem THEN
            eState := STATE_SHUTDOWN;
        END_IF;

    STATE_ABRASIVE_METERING:
        q_bHighPressureValve := TRUE;
        tValveDelay(IN:=TRUE, PT:=T#500MS);
        IF tValveDelay.Q AND rAbrasiveHopperLevel > 1.0 THEN
            q_bAbrasiveValve := TRUE;
            tValveDelay(IN:=FALSE);
            eState := STATE_KINEMATIC_VECTORING;
        ELSIF rAbrasiveHopperLevel <= 1.0 THEN
            eState := STATE_FAULT;
            iErrorCode := 1010; (* Abrasive Low *)
        END_IF;

    STATE_KINEMATIC_VECTORING:
        (* Simplified Linear Interpolation for 5-Axis Vectoring *)
        IF ABS(rTargetX - rCurrentX) > rInterpolationStep THEN rCurrentX := rCurrentX + rInterpolationStep * SEL(rTargetX > rCurrentX, -1.0, 1.0); END_IF;
        IF ABS(rTargetY - rCurrentY) > rInterpolationStep THEN rCurrentY := rCurrentY + rInterpolationStep * SEL(rTargetY > rCurrentY, -1.0, 1.0); END_IF;
        IF ABS(rTargetZ - rCurrentZ) > rInterpolationStep THEN rCurrentZ := rCurrentZ + rInterpolationStep * SEL(rTargetZ > rCurrentZ, -1.0, 1.0); END_IF;
        IF ABS(rTargetA - rCurrentA) > rInterpolationStep THEN rCurrentA := rCurrentA + rInterpolationStep * SEL(rTargetA > rCurrentA, -1.0, 1.0); END_IF;
        IF ABS(rTargetB - rCurrentB) > rInterpolationStep THEN rCurrentB := rCurrentB + rInterpolationStep * SEL(rTargetB > rCurrentB, -1.0, 1.0); END_IF;

        IF ABS(rTargetX - rCurrentX) <= rInterpolationStep AND ABS(rTargetY - rCurrentY) <= rInterpolationStep AND ABS(rTargetZ - rCurrentZ) <= rInterpolationStep AND ABS(rTargetA - rCurrentA) <= rInterpolationStep AND ABS(rTargetB - rCurrentB) <= rInterpolationStep THEN
            eState := STATE_CUTTING;
        END_IF;

    STATE_CUTTING:
        bCuttingActive := TRUE;
        rAbrasiveHopperLevel := rAbrasiveHopperLevel - (rAbrasiveFeedRateSet * 0.0001); (* Drain abrasive *)
        IF NOT bStartCut THEN
            eState := STATE_READY;
        END_IF;

    STATE_SHUTDOWN:
        bSystemReady := FALSE;
        q_iIntensifierPumpVFD := 0;
        q_bHighPressureValve := FALSE;
        q_bAbrasiveValve := FALSE;
        rActualPressure := rActualPressure * 0.90;
        IF rActualPressure < 50.0 THEN
            rActualPressure := 0.0;
            eState := STATE_INIT;
        END_IF;

    STATE_FAULT:
        bFaultActive := TRUE;
        bSystemReady := FALSE;
        bCuttingActive := FALSE;
        q_bHighPressureValve := FALSE;
        q_bAbrasiveValve := FALSE;
        q_iIntensifierPumpVFD := 0;
        rActualPressure := 0.0;
        IF NOT bEmergencyStop AND bEnableSystem THEN
            eState := STATE_INIT;
        END_IF;
END_CASE;

rCurrentPressure := rActualPressure;
END_FUNCTION_BLOCK
```"""

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": code}
    ]
}

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=4)
print(filename)
