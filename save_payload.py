import json
import os
import uuid

# Define the content
user_content = "Generate a highly complex control scenario for a Municipal Water Flocculation Basin in IEC 61131-3 Structured Text. Include alum coagulant dosing PID cascades, variable-speed flocculator paddle shear rate, and settling basin sludge rakes."

st_code = """```iec-st
FUNCTION_BLOCK FB_FlocculationBasinControl
TITLE = 'Municipal Water Flocculation Basin Advanced Control'
// This FB implements a highly complex, multi-stage flocculation basin control strategy.
// Features:
// - Cascaded PID control for Alum Coagulant dosing based on incoming flow and raw water turbidity.
// - Variable-speed flocculator paddle shear rate (G-value) control based on water temperature and flow rate.
// - Settling basin sludge rake automated sequencing with torque monitoring and overload protection.

VAR_INPUT
    // Flow and Quality
    rRawWaterFlowRate       : REAL; // Incoming raw water flow [MGD]
    rRawWaterTurbidity      : REAL; // Raw water turbidity [NTU]
    rRawWaterTemp           : REAL; // Raw water temperature [C]
    rSettledWaterTurbidity  : REAL; // Settled water turbidity [NTU] (feedback)
    
    // Motor and Rake Status
    bAlumPumpRunStatus      : BOOL; // Alum dosing pump running
    rAlumPumpSpeedFbk       : REAL; // Alum dosing pump speed feedback [RPM]
    
    bFlocPaddleMotorRun     : BOOL; // Flocculator paddle motor running
    rFlocPaddleSpeedFbk     : REAL; // Flocculator paddle speed feedback [RPM]
    
    bSludgeRakeRunStatus    : BOOL; // Sludge rake running
    rSludgeRakeTorque       : REAL; // Sludge rake drive torque [%]
    
    // Command & Control
    bEnableAutoMode         : BOOL; // Master auto mode enable
    bResetFaults            : BOOL; // Reset system faults
END_VAR

VAR_OUTPUT
    // Actuator Commands
    rAlumPumpSpeedCmd       : REAL; // Alum dosing pump speed command [0-100%]
    rFlocPaddleSpeedCmd     : REAL; // Flocculator paddle speed command [0-100%]
    bSludgeRakeStartCmd     : BOOL; // Command to start sludge rake
    bSludgeRakeStopCmd      : BOOL; // Command to stop sludge rake
    
    // System Status & Alarms
    bSystemHealthy          : BOOL;
    bAlumPumpFault          : BOOL;
    bFlocPaddleFault        : BOOL;
    bRakeTorqueHigh         : BOOL;
    bRakeOverloadTrip       : BOOL;
    bTurbidityHighAlarm     : BOOL;
END_VAR

VAR
    // Internal Variables - PID Alum Dosing
    rAlumDoseSP             : REAL; // Calculated target dose [mg/L]
    rFlowFeedForward        : REAL; // Feedforward component from flow
    rTurbidityFeedback      : REAL; // Feedback component from turbidity
    rPID_Kp                 : REAL := 2.5;
    rPID_Ki                 : REAL := 0.8;
    rPID_Kd                 : REAL := 0.1;
    rPID_Integral           : REAL;
    rPID_PrevError          : REAL;
    rPID_Error              : REAL;
    
    // Internal Variables - Flocculator Shear Rate (G-Value)
    rTargetGValue           : REAL; // Target velocity gradient [s^-1]
    rViscosity              : REAL; // Dynamic viscosity based on temp
    rPaddleSpeedCalc        : REAL; // Calculated paddle speed [RPM]
    
    // Internal Variables - Sludge Rake Control
    timerRakeCycle          : TON;
    timerRakeDwell          : TON;
    timerRakeTorqueDelay    : TON;
    bRakeCycleActive        : BOOL;
    nRakeState              : INT := 0; // 0=Idle, 1=Running, 2=Dwell, 3=Fault
    
    // Constants
    c_rMaxAlumDose          : REAL := 50.0;
    c_rMaxRakeTorque        : REAL := 85.0; // 85% torque warning
    c_rTripRakeTorque       : REAL := 95.0; // 95% torque trip
    c_tCycleTime            : TIME := T#4H; // Rake cycle every 4 hours
    c_tDwellTime            : TIME := T#30M; // Rake runs for 30 minutes
END_VAR

// ---------------------------------------------------------
// 1. FAULT MANAGEMENT & SYSTEM HEALTH
// ---------------------------------------------------------
IF bResetFaults THEN
    bAlumPumpFault := FALSE;
    bFlocPaddleFault := FALSE;
    bRakeTorqueHigh := FALSE;
    bRakeOverloadTrip := FALSE;
    bTurbidityHighAlarm := FALSE;
    nRakeState := 0;
END_IF;

bSystemHealthy := NOT (bAlumPumpFault OR bFlocPaddleFault OR bRakeOverloadTrip OR bTurbidityHighAlarm);

IF NOT bEnableAutoMode THEN
    rAlumPumpSpeedCmd := 0.0;
    rFlocPaddleSpeedCmd := 0.0;
    bSludgeRakeStartCmd := FALSE;
    bSludgeRakeStopCmd := TRUE;
    RETURN;
END_IF;

// ---------------------------------------------------------
// 2. ALUM COAGULANT DOSING (CASCADED FEEDFORWARD + PID)
// ---------------------------------------------------------
// Feedforward calculation based on raw water flow and turbidity
// Empirical formula: Base Dose + (Turbidity * Factor)
rFlowFeedForward := (rRawWaterFlowRate * 1.5) + (rRawWaterTurbidity * 0.25);

// Feedback control based on settled water turbidity target (Target = 1.0 NTU)
rPID_Error := rSettledWaterTurbidity - 1.0;

// Anti-windup for integral
IF (rAlumPumpSpeedCmd < 100.0 AND rAlumPumpSpeedCmd > 0.0) THEN
    rPID_Integral := rPID_Integral + (rPID_Error * rPID_Ki);
END_IF;

rTurbidityFeedback := (rPID_Kp * rPID_Error) + rPID_Integral + (rPID_Kd * (rPID_Error - rPID_PrevError));
rPID_PrevError := rPID_Error;

// Total Dose Command (Limit to max allowable)
rAlumDoseSP := rFlowFeedForward + rTurbidityFeedback;
IF rAlumDoseSP > c_rMaxAlumDose THEN
    rAlumDoseSP := c_rMaxAlumDose;
ELSIF rAlumDoseSP < 0.0 THEN
    rAlumDoseSP := 0.0;
END_IF;

// Scale to Pump Command (Assume linear 0-100% = 0-MaxDose)
rAlumPumpSpeedCmd := (rAlumDoseSP / c_rMaxAlumDose) * 100.0;

// ---------------------------------------------------------
// 3. VARIABLE-SPEED FLOCCULATOR PADDLE SHEAR RATE
// ---------------------------------------------------------
// Adjust target G-Value based on temperature (colder water needs higher shear)
IF rRawWaterTemp < 10.0 THEN
    rTargetGValue := 45.0; // High shear for cold water
ELSIF rRawWaterTemp >= 10.0 AND rRawWaterTemp < 20.0 THEN
    rTargetGValue := 35.0; // Medium shear
ELSE
    rTargetGValue := 25.0; // Low shear for warm water
END_IF;

// Calculate required paddle speed (Simplified approximation)
// In reality, P = G^2 * V * mu, Speed is proportional to (Power)^(1/3)
rPaddleSpeedCalc := rTargetGValue * 1.5; // Gain scaling for VFD
rFlocPaddleSpeedCmd := LIMIT(10.0, rPaddleSpeedCalc, 100.0); // Min 10%, Max 100%

// ---------------------------------------------------------
// 4. SETTLING BASIN SLUDGE RAKE SEQUENCING & PROTECTION
// ---------------------------------------------------------
// High Torque Warning and Trip Logic
timerRakeTorqueDelay(IN:=(rSludgeRakeTorque > c_rMaxRakeTorque), PT:=T#5S);
IF timerRakeTorqueDelay.Q THEN
    bRakeTorqueHigh := TRUE;
END_IF;

IF rSludgeRakeTorque > c_rTripRakeTorque THEN
    bRakeOverloadTrip := TRUE;
    nRakeState := 3; // Fault State
END_IF;

// Rake State Machine
CASE nRakeState OF
    0: // Idle State
        bSludgeRakeStartCmd := FALSE;
        bSludgeRakeStopCmd := TRUE;
        timerRakeCycle(IN:=TRUE, PT:=c_tCycleTime);
        IF timerRakeCycle.Q THEN
            timerRakeCycle(IN:=FALSE); // Reset timer
            nRakeState := 1; // Transition to run
        END_IF;
        
    1: // Running State
        bSludgeRakeStartCmd := TRUE;
        bSludgeRakeStopCmd := FALSE;
        timerRakeDwell(IN:=TRUE, PT:=c_tDwellTime);
        IF timerRakeDwell.Q THEN
            timerRakeDwell(IN:=FALSE); // Reset dwell timer
            nRakeState := 0; // Back to idle
        END_IF;
        
    3: // Fault State
        bSludgeRakeStartCmd := FALSE;
        bSludgeRakeStopCmd := TRUE;
        // Wait for bResetFaults
END_CASE;

END_FUNCTION_BLOCK
```"""

record = {
    "messages": [
        {"role": "user", "content": user_content},
        {"role": "assistant", "content": st_code}
    ]
}

# 1. Save to swarm_raw
os.makedirs('data/swarm_raw', exist_ok=True)
with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)

# 2. Append to synthetic_generation_v3_enterprise.jsonl
with open('data/synthetic_generation_v3_enterprise.jsonl', 'a', encoding='utf-8') as f:
    f.write(json.dumps(record) + "\\n")

print("Done")
