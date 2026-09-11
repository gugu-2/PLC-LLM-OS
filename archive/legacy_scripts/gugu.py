import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: RO Membrane Manufacturing Line.
Task: Invent a highly complex control scenario for this domain (e.g., polyamide casting thickness feedback, curing oven web tension zones, and optical defect inspection arrays).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O.
"""

st_code = """```iec-st
FUNCTION_BLOCK FB_ROMembrane_MfgLine
VAR_INPUT
    bStartProcess : BOOL;
    bEStop : BOOL;
    rTargetThickness : REAL; // Target polyamide thickness in microns
    rCurrentThickness : REAL; // Measured thickness from laser gauge
    rLineSpeedCmd : REAL; // Commanded line speed m/min
    aOpticalDefects : ARRAY[1..10] OF INT; // Optical inspection defect codes
    rTensionZone1FB : REAL; // Feedback from Tension load cell 1
    rTensionZone2FB : REAL; // Feedback from Tension load cell 2
    rTensionZone3FB : REAL; // Feedback from Tension load cell 3
    rOvenTemp1FB : REAL; // Feedback from Oven Zone 1
    rOvenTemp2FB : REAL; // Feedback from Oven Zone 2
END_VAR

VAR_OUTPUT
    bSystemRunning : BOOL;
    bFaultActive : BOOL;
    iFaultCode : INT;
    rCastingPumpSpeed : REAL; // Speed command for casting pump
    rWebDrive1Cmd : REAL; // Cmd for web drive 1
    rWebDrive2Cmd : REAL; // Cmd for web drive 2
    rWebDrive3Cmd : REAL; // Cmd for web drive 3
    rOvenHeater1Cmd : REAL;
    rOvenHeater2Cmd : REAL;
    bRejectRollerActivate : BOOL;
END_VAR

VAR
    rThicknessError : REAL;
    rThicknessIntegral : REAL;
    rThicknessKp : REAL := 2.5;
    rThicknessKi : REAL := 0.1;
    
    rTension1Err, rTension2Err, rTension3Err : REAL;
    rTensionTarget1 : REAL := 50.0; // N
    rTensionTarget2 : REAL := 55.0; // N
    rTensionTarget3 : REAL := 60.0; // N
    
    iDefectCount : INT;
    i : INT;
    
    TMR_RejectPulse : TP;
END_VAR

// Emergency Stop and Fault Logic
IF bEStop THEN
    bSystemRunning := FALSE;
    bFaultActive := TRUE;
    iFaultCode := 99;
    rCastingPumpSpeed := 0.0;
    rWebDrive1Cmd := 0.0;
    rWebDrive2Cmd := 0.0;
    rWebDrive3Cmd := 0.0;
    rOvenHeater1Cmd := 0.0;
    rOvenHeater2Cmd := 0.0;
    RETURN;
END_IF;

IF bStartProcess AND NOT bFaultActive THEN
    bSystemRunning := TRUE;
END_IF;

IF NOT bSystemRunning THEN
    rCastingPumpSpeed := 0.0;
    rWebDrive1Cmd := 0.0;
    rWebDrive2Cmd := 0.0;
    rWebDrive3Cmd := 0.0;
    RETURN;
END_IF;

// Polyamide Casting Thickness PI Control
rThicknessError := rTargetThickness - rCurrentThickness;
rThicknessIntegral := rThicknessIntegral + (rThicknessError * 0.01); // Assuming 10ms cycle
IF rThicknessIntegral > 100.0 THEN rThicknessIntegral := 100.0; END_IF;
IF rThicknessIntegral < -100.0 THEN rThicknessIntegral := -100.0; END_IF;

rCastingPumpSpeed := (rThicknessError * rThicknessKp) + (rThicknessIntegral * rThicknessKi) + (rLineSpeedCmd * 1.5);

// Web Tension Control (Basic P-control for simplicity, cascading with line speed)
rTension1Err := rTensionTarget1 - rTensionZone1FB;
rTension2Err := rTensionTarget2 - rTensionZone2FB;
rTension3Err := rTensionTarget3 - rTensionZone3FB;

rWebDrive1Cmd := rLineSpeedCmd + (rTension1Err * 0.5);
rWebDrive2Cmd := rWebDrive1Cmd + (rTension2Err * 0.4);
rWebDrive3Cmd := rWebDrive2Cmd + (rTension3Err * 0.4);

// Oven Temperature Control
IF rOvenTemp1FB < 120.0 THEN
    rOvenHeater1Cmd := 100.0;
ELSIF rOvenTemp1FB > 125.0 THEN
    rOvenHeater1Cmd := 0.0;
ELSE
    rOvenHeater1Cmd := 50.0;
END_IF;

IF rOvenTemp2FB < 140.0 THEN
    rOvenHeater2Cmd := 100.0;
ELSIF rOvenTemp2FB > 145.0 THEN
    rOvenHeater2Cmd := 0.0;
ELSE
    rOvenHeater2Cmd := 50.0;
END_IF;

// Optical Defect Inspection Array Processing
iDefectCount := 0;
FOR i := 1 TO 10 DO
    IF aOpticalDefects[i] > 0 THEN
        iDefectCount := iDefectCount + 1;
    END_IF;
END_FOR;

IF iDefectCount >= 3 THEN
    TMR_RejectPulse(IN := TRUE, PT := T#2S);
ELSE
    TMR_RejectPulse(IN := FALSE, PT := T#2S);
END_IF;

bRejectRollerActivate := TMR_RejectPulse.Q;

// Fault limits
IF rCurrentThickness > (rTargetThickness * 1.5) OR rCurrentThickness < (rTargetThickness * 0.5) THEN
    bFaultActive := TRUE;
    iFaultCode := 10;
    bSystemRunning := FALSE;
END_IF;

END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": st_code}]}

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=4)

print(f"Saved to {filename}")
