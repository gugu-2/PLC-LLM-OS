import json
import uuid
import os

user_prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Subsea Oil/Gas Wellhead Control System.
Task: Invent a highly complex control scenario for this domain (e.g., Blowout Preventer (BOP) hydraulic accumulator cascades, choke valve sand erosion compensation, and multiphase flow metering).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."""

assistant_response = """```iec-st
FUNCTION_BLOCK FB_SubseaWellheadControl
VAR_INPUT
    bEnable : BOOL; // Enable subsea control algorithms
    bEmergencyShutdown : BOOL; // ESD signal (active high triggers shutdown)
    rHydraulicSupplyPres : REAL; // Accumulator supply pressure (bar)
    rChokeValvePosition : REAL; // Feedback of current choke position (%)
    rMultiphaseFlowRate : REAL; // Raw multiphase flow input (m3/h)
    rSandDetectorAcoustic : REAL; // Acoustic sand detector signal (mV)
    bBOP_CommandClose : BOOL; // Manual command to close BOP
    rWellheadPressure : REAL; // Wellhead pressure (bar)
    rWellheadTemp : REAL; // Wellhead temperature (C)
END_VAR
VAR_OUTPUT
    bBOP_CloseCoil : BOOL; // Output to solenoid valve to close BOP
    bBOP_OpenCoil : BOOL; // Output to solenoid valve to open BOP
    rChokeValveSetpoint : REAL; // Setpoint for choke valve position (%)
    bAccumulatorPumpRun : BOOL; // Command to start hydraulic pumps
    bESD_Triggered : BOOL; // Acknowledgment of ESD state
    rCalculatedErosionRate : REAL; // Estimated sand erosion rate (mm/yr)
    bChokeAlarm : BOOL; // Alarm indicating choke valve anomaly
    bFlowAlarm : BOOL; // Alarm indicating abnormal flow conditions
END_VAR
VAR
    eState : (INIT, NORMAL_OP, CHOKE_ADJUST, ACCUMULATOR_CHARGE, ESD_SHUTDOWN);
    TmrESD : TON;
    rErosionAccumulator : REAL := 0.0;
    rFlowSmoothingFilter : REAL := 0.0;
    rPreviousSandSignal : REAL := 0.0;
    bLowPressureAlarm : BOOL;
    iLoopCounter : INT;
END_VAR
VAR CONSTANT
    rMaxErosionThreshold : REAL := 2.5; // Max allowed erosion rate in mm/yr
    rMinHydraulicPres : REAL := 207.0; // Minimum allowed hydraulic pressure (bar) (approx 3000 psi)
    rHydraulicPresSetpoint : REAL := 345.0; // Target pressure (bar) (approx 5000 psi)
    rFilterAlpha : REAL := 0.1; // Low pass filter constant
END_VAR

// State Machine Initialization
IF NOT bEnable THEN
    eState := INIT;
    bBOP_CloseCoil := FALSE;
    bBOP_OpenCoil := FALSE;
    rChokeValveSetpoint := 0.0;
    bAccumulatorPumpRun := FALSE;
    bESD_Triggered := FALSE;
    RETURN;
END_IF;

// Emergency Shutdown Overrides Everything
IF bEmergencyShutdown OR bBOP_CommandClose THEN
    eState := ESD_SHUTDOWN;
END_IF;

// Multiphase Flow Smoothing (First Order Low Pass Filter)
rFlowSmoothingFilter := rFilterAlpha * rMultiphaseFlowRate + (1.0 - rFilterAlpha) * rFlowSmoothingFilter;

// Sand Erosion Compensation Calculation
IF rSandDetectorAcoustic > 0.0 THEN
    rErosionAccumulator := (rSandDetectorAcoustic - rPreviousSandSignal) * rFlowSmoothingFilter * 0.005;
    rCalculatedErosionRate := rCalculatedErosionRate + rErosionAccumulator;
END_IF;
rPreviousSandSignal := rSandDetectorAcoustic;

IF rCalculatedErosionRate > rMaxErosionThreshold THEN
    bChokeAlarm := TRUE;
ELSE
    bChokeAlarm := FALSE;
END_IF;

// Hydraulic Accumulator Cascade Management
IF rHydraulicSupplyPres < rMinHydraulicPres THEN
    bLowPressureAlarm := TRUE;
ELSE
    bLowPressureAlarm := FALSE;
END_IF;

// Main Control State Machine
CASE eState OF
    INIT:
        bESD_Triggered := FALSE;
        rChokeValveSetpoint := 0.0;
        IF bEnable AND NOT bEmergencyShutdown THEN
            eState := ACCUMULATOR_CHARGE;
        END_IF;
        
    ACCUMULATOR_CHARGE:
        IF rHydraulicSupplyPres < rHydraulicPresSetpoint THEN
            bAccumulatorPumpRun := TRUE;
        ELSE
            bAccumulatorPumpRun := FALSE;
            eState := NORMAL_OP;
        END_IF;
        
    NORMAL_OP:
        IF rHydraulicSupplyPres < (rHydraulicPresSetpoint - 20.0) THEN
             bAccumulatorPumpRun := TRUE;
        ELSE
             bAccumulatorPumpRun := FALSE;
        END_IF;
        
        bBOP_OpenCoil := TRUE;
        bBOP_CloseCoil := FALSE;
        
        IF rWellheadPressure > 300.0 THEN
             rChokeValveSetpoint := rChokeValveSetpoint - 1.5;
        ELSIF rWellheadPressure < 250.0 AND rFlowSmoothingFilter > 50.0 THEN
             rChokeValveSetpoint := rChokeValveSetpoint + 0.5;
        END_IF;
        
        IF rChokeValveSetpoint > 100.0 THEN
             rChokeValveSetpoint := 100.0;
        ELSIF rChokeValveSetpoint < 0.0 THEN
             rChokeValveSetpoint := 0.0;
        END_IF;

    ESD_SHUTDOWN:
        bESD_Triggered := TRUE;
        bAccumulatorPumpRun := FALSE;
        
        rChokeValveSetpoint := 0.0;
        
        bBOP_OpenCoil := FALSE;
        bBOP_CloseCoil := TRUE;
        
        IF NOT bEmergencyShutdown AND NOT bBOP_CommandClose THEN
            eState := ESD_SHUTDOWN;
        END_IF;
        
END_CASE;

IF (rFlowSmoothingFilter > 500.0) OR (rWellheadPressure > 400.0) THEN
    bFlowAlarm := TRUE;
ELSE
    bFlowAlarm := FALSE;
END_IF;

END_FUNCTION_BLOCK
```"""

import os

data_dir = "data"
os.makedirs(data_dir, exist_ok=True)
swarm_dir = os.path.join(data_dir, "swarm_raw")
os.makedirs(swarm_dir, exist_ok=True)

record = {
    "messages": [
        {"role": "user", "content": user_prompt},
        {"role": "assistant", "content": assistant_response}
    ]
}

# Save to enterprise jsonl
with open(os.path.join(data_dir, "synthetic_generation_v3_enterprise.jsonl"), "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\n")

# Save to swarm raw
unique_id = uuid.uuid4().hex[:8]
with open(os.path.join(swarm_dir, f"agent_{unique_id}.json"), "w", encoding="utf-8") as f:
    json.dump(record, f)

print("Data saved.")
