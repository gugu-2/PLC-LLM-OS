import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Deep Sea Mining Nodule Collector.
Task: Invent a highly complex control scenario for this domain (e.g., hydraulic track drives in high-pressure fluid, acoustic altimeter seabed following, and lift pipe slurry density).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."""

st_code = """```iec-st
FUNCTION_BLOCK FB_NoduleCollectorControl
TITLE = 'Deep Sea Mining Nodule Collector Control System'
VERSION : '1.0'

VAR_INPUT
    bEnableSystem         : BOOL;  // Main system enable
    rTargetSpeed          : REAL;  // Desired forward speed (m/s)
    rTargetClearance      : REAL;  // Target altitude above seabed (m)
    rAcousticAltimeter1   : REAL;  // Seabed distance front (m)
    rAcousticAltimeter2   : REAL;  // Seabed distance rear (m)
    rHydraulicPressureIn  : REAL;  // Main hydraulic supply pressure (bar)
    rAmbientPressure      : REAL;  // External hydrostatic pressure (bar)
    rSlurryDensityIn      : REAL;  // Lift pipe slurry density (kg/m3)
    rTrackSlipLeft        : REAL;  // Left track slip percentage
    rTrackSlipRight       : REAL;  // Right track slip percentage
END_VAR

VAR_OUTPUT
    rValveCmdTrackLeft    : REAL;  // Left track hydraulic valve command (0-100%)
    rValveCmdTrackRight   : REAL;  // Right track hydraulic valve command (0-100%)
    rValveCmdSuspension   : REAL;  // Suspension height control valve (0-100%)
    rPumpCmdSlurryLift    : REAL;  // Slurry lift pump speed command (0-100%)
    bSystemFault          : BOOL;  // Critical system fault
    iFaultCode            : INT;   // Active fault code
END_VAR

VAR
    // Internal state variables
    rCurrentClearance     : REAL;
    rClearanceError       : REAL;
    rClearanceIntegral    : REAL;
    rClearanceDerivative  : REAL;
    rLastClearanceError   : REAL;
    
    rSpeedControlLeft     : REAL;
    rSpeedControlRight    : REAL;
    
    // PID Constants
    Kp_Alt                : REAL := 15.5;
    Ki_Alt                : REAL := 2.1;
    Kd_Alt                : REAL := 5.0;
    
    Kp_Track              : REAL := 20.0;
    
    // Safety limits
    MAX_SLIP_ALLOWABLE    : REAL := 15.0;
    MIN_HYD_PRESSURE      : REAL := 250.0;
    MAX_SLURRY_DENSITY    : REAL := 1350.0;
    
    // Timers
    tHydraulicFaultTimer  : TON;
    tSlipFaultTimer       : TON;
END_VAR

// System State Evaluation
IF NOT bEnableSystem THEN
    rValveCmdTrackLeft := 0.0;
    rValveCmdTrackRight := 0.0;
    rValveCmdSuspension := 0.0;
    rPumpCmdSlurryLift := 0.0;
    bSystemFault := FALSE;
    iFaultCode := 0;
    RETURN;
END_IF;

// Calculate current average clearance from acoustic altimeters
rCurrentClearance := (rAcousticAltimeter1 + rAcousticAltimeter2) / 2.0;

// Altitude PID Control for Suspension
rClearanceError := rTargetClearance - rCurrentClearance;
rClearanceIntegral := rClearanceIntegral + (rClearanceError * 0.1); // Assuming 100ms cycle
rClearanceDerivative := (rClearanceError - rLastClearanceError) / 0.1;

rValveCmdSuspension := (Kp_Alt * rClearanceError) + (Ki_Alt * rClearanceIntegral) + (Kd_Alt * rClearanceDerivative);
rLastClearanceError := rClearanceError;

// Limit suspension command
IF rValveCmdSuspension > 100.0 THEN
    rValveCmdSuspension := 100.0;
ELSIF rValveCmdSuspension < -100.0 THEN
    rValveCmdSuspension := -100.0;
END_IF;

// Hydraulic Track Drive Control with Slip Compensation
// Adjust speed target based on slip
rSpeedControlLeft := rTargetSpeed;
IF rTrackSlipLeft > 5.0 THEN
    rSpeedControlLeft := rTargetSpeed * (1.0 - (rTrackSlipLeft / 100.0) * Kp_Track);
END_IF;

rSpeedControlRight := rTargetSpeed;
IF rTrackSlipRight > 5.0 THEN
    rSpeedControlRight := rTargetSpeed * (1.0 - (rTrackSlipRight / 100.0) * Kp_Track);
END_IF;

rValveCmdTrackLeft := rSpeedControlLeft * 10.0; // Scale to valve %
rValveCmdTrackRight := rSpeedControlRight * 10.0;

// Limit track commands
IF rValveCmdTrackLeft > 100.0 THEN rValveCmdTrackLeft := 100.0; END_IF;
IF rValveCmdTrackRight > 100.0 THEN rValveCmdTrackRight := 100.0; END_IF;
IF rValveCmdTrackLeft < 0.0 THEN rValveCmdTrackLeft := 0.0; END_IF;
IF rValveCmdTrackRight < 0.0 THEN rValveCmdTrackRight := 0.0; END_IF;

// Lift Pipe Slurry Density Control
// Adjust lift pump based on ambient pressure and slurry density to prevent choking
IF rSlurryDensityIn > MAX_SLURRY_DENSITY THEN
    // Reduce pump speed to dilute slurry
    rPumpCmdSlurryLift := 100.0; // Max speed to clear dense plug
ELSE
    // Normal operation, scale based on target density 1200 kg/m3
    rPumpCmdSlurryLift := 50.0 + ((rSlurryDensityIn - 1000.0) * 0.1);
END_IF;
IF rPumpCmdSlurryLift > 100.0 THEN rPumpCmdSlurryLift := 100.0; END_IF;

// Fault Monitoring
// Hydraulic Pressure Fault
tHydraulicFaultTimer(IN := (rHydraulicPressureIn - rAmbientPressure) < MIN_HYD_PRESSURE, PT := T#2S);
IF tHydraulicFaultTimer.Q THEN
    bSystemFault := TRUE;
    iFaultCode := 101; // Low differential pressure
END_IF;

// Excessive Slip Fault
tSlipFaultTimer(IN := (rTrackSlipLeft > MAX_SLIP_ALLOWABLE) OR (rTrackSlipRight > MAX_SLIP_ALLOWABLE), PT := T#5S);
IF tSlipFaultTimer.Q THEN
    bSystemFault := TRUE;
    iFaultCode := 102; // Track slip timeout
END_IF;

// Failsafe override
IF bSystemFault THEN
    rValveCmdTrackLeft := 0.0;
    rValveCmdTrackRight := 0.0;
    rPumpCmdSlurryLift := 10.0; // Minimal flow to prevent settling
END_IF;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": st_code}]}
filepath = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filepath, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=4)
print(f"File created: {filepath}")

with open("data/synthetic_generation_v3_enterprise.jsonl", "a", encoding="utf-8") as f:
    json.dump(record, f)
    f.write("\n")
