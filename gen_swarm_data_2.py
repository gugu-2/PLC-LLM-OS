import json
import uuid
import os

prompt = "Invent a highly complex control scenario for a Fully Automated Smart Mining Excavator. Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."

code = """```iec-st
FUNCTION_BLOCK FB_AutonomousExcavatorCore
TITLE = 'Fully Automated Smart Mining Excavator Core'
VERSION : '1.0'
AUTHOR : 'Lumina AI Cloud Swarm'

VAR_INPUT
    bEnableAutoMode : BOOL; // Enable autonomous operations
    bEmergencyStop : BOOL; // Global E-Stop
    rTargetX : REAL; // Target digging X coordinate (m)
    rTargetY : REAL; // Target digging Y coordinate (m)
    rTargetZ : REAL; // Target digging Z coordinate (m)
    rDumpTruckX : REAL; // Target dump X coordinate (m)
    rDumpTruckY : REAL; // Target dump Y coordinate (m)
    rDumpTruckZ : REAL; // Target dump Z coordinate (m)
    rLidarPayloadEst : REAL; // Volume estimation from LiDAR (m^3)
    rBoomPressureA : REAL; // Boom cylinder A pressure (bar)
    rBoomPressureB : REAL; // Boom cylinder B pressure (bar)
    rStickPressureA : REAL; // Stick cylinder A pressure (bar)
    rStickPressureB : REAL; // Stick cylinder B pressure (bar)
    rBucketPressureA : REAL; // Bucket cylinder A pressure (bar)
    rBucketPressureB : REAL; // Bucket cylinder B pressure (bar)
    rSwingSpeedAct : REAL; // Actual swing speed (rad/s)
END_VAR

VAR_OUTPUT
    bSystemReady : BOOL; // System is initialized and ready
    rBoomValveCmd : REAL; // Boom valve command (-100.0 to 100.0%)
    rStickValveCmd : REAL; // Stick valve command (-100.0 to 100.0%)
    rBucketValveCmd : REAL; // Bucket valve command (-100.0 to 100.0%)
    rSwingValveCmd : REAL; // Swing valve command (-100.0 to 100.0%)
    bLoadComplete : BOOL; // Current load cycle complete
    iFaultCode : INT; // Active fault code (0 = no fault)
    rEstimatedForce : REAL; // Calculated bucket tip force (kN)
END_VAR

VAR
    iStateMachine : INT := 0; // Internal state machine 
    // 0=IDLE, 10=DIG_APPROACH, 20=PENETRATE, 30=CURL_LIFT, 40=SWING_TO_TRUCK, 50=DUMP, 60=RETURN
    rCycleTimer : REAL := 0.0;
    rDeltaTime : REAL := 0.01; // 10ms cycle
    rForceVectorX : REAL;
    rForceVectorZ : REAL;
    rPayloadMass : REAL;
    rMaterialDensity : REAL := 1800.0; // kg/m^3
    bTargetReached : BOOL;
    
    // PID Controllers (Simplified for FB)
    rErrBoom, rErrStick, rErrBucket, rErrSwing : REAL;
    rIntBoom, rIntStick, rIntBucket, rIntSwing : REAL;
    
    // Limits
    MAX_FORCE_KN : REAL := 850.0;
    MAX_PRESSURE_BAR : REAL := 350.0;
END_VAR

// Execution starts here
IF bEmergencyStop THEN
    rBoomValveCmd := 0.0;
    rStickValveCmd := 0.0;
    rBucketValveCmd := 0.0;
    rSwingValveCmd := 0.0;
    iStateMachine := 0;
    iFaultCode := 999; // E-Stop active
    bSystemReady := FALSE;
    RETURN;
END_IF;

IF iFaultCode = 999 AND NOT bEmergencyStop THEN
    iFaultCode := 0;
END_IF;

bSystemReady := NOT bEmergencyStop AND iFaultCode = 0;

// Hydraulic Bucket Force Vectoring Calculation
// Simplistic representation of hydraulic force at bucket tip
rForceVectorX := (rStickPressureA - rStickPressureB) * 0.15 + (rBucketPressureA - rBucketPressureB) * 0.05;
rForceVectorZ := (rBoomPressureA - rBoomPressureB) * 0.2 + (rStickPressureA - rStickPressureB) * 0.1;
rEstimatedForce := SQRT(rForceVectorX * rForceVectorX + rForceVectorZ * rForceVectorZ);

IF rEstimatedForce > MAX_FORCE_KN THEN
    iFaultCode := 101; // Overload
END_IF;

// Pressure limit monitoring
IF rBoomPressureA > MAX_PRESSURE_BAR OR rStickPressureA > MAX_PRESSURE_BAR THEN
    iFaultCode := 102; // Overpressure
END_IF;

IF NOT bEnableAutoMode THEN
    iStateMachine := 0;
    RETURN;
END_IF;

// Main Autonomous Dig Cycle State Machine
CASE iStateMachine OF
    0: // IDLE
        IF bSystemReady AND bEnableAutoMode THEN
            iStateMachine := 10;
            bLoadComplete := FALSE;
        END_IF;
        
    10: // DIG_APPROACH - Move to rTarget coordinates
        rErrBoom := rTargetZ - 5.0; // Dummy reference
        rErrStick := rTargetX - 10.0;
        
        rBoomValveCmd := rErrBoom * 2.5; 
        rStickValveCmd := rErrStick * 2.0;
        rBucketValveCmd := 50.0; // Open bucket
        
        // Assume target reached condition
        IF ABS(rErrBoom) < 0.5 AND ABS(rErrStick) < 0.5 THEN
            iStateMachine := 20;
        END_IF;
        
    20: // PENETRATE - Force vectoring to optimize cutting
        rBoomValveCmd := -40.0; // Push down
        rStickValveCmd := 60.0; // Pull in
        rBucketValveCmd := 20.0; // Slight curl
        
        // Modulate based on force feedback to avoid stall
        IF rEstimatedForce > 700.0 THEN
            rStickValveCmd := rStickValveCmd * 0.5;
            rBoomValveCmd := 10.0; // Relieve pressure
        END_IF;
        
        rCycleTimer := rCycleTimer + rDeltaTime;
        IF rCycleTimer > 3.0 THEN
            rCycleTimer := 0.0;
            iStateMachine := 30;
        END_IF;
        
    30: // CURL_LIFT - Capture payload
        rBoomValveCmd := 80.0; // Lift fast
        rStickValveCmd := 20.0;
        rBucketValveCmd := 90.0; // Hard curl
        
        // LiDAR Payload Estimation Update
        rPayloadMass := rLidarPayloadEst * rMaterialDensity;
        
        IF rCycleTimer > 2.0 THEN
            rCycleTimer := 0.0;
            iStateMachine := 40;
        END_IF;
        rCycleTimer := rCycleTimer + rDeltaTime;
        
    40: // SWING_TO_TRUCK - Autonomous trajectory generation
        rErrSwing := rDumpTruckX - 0.0; // simplified swing angle error
        rSwingValveCmd := rErrSwing * 1.5;
        
        // Limit speed based on mass (centrifugal compensation)
        IF rPayloadMass > 15000.0 THEN
            IF rSwingValveCmd > 50.0 THEN rSwingValveCmd := 50.0; END_IF;
            IF rSwingValveCmd < -50.0 THEN rSwingValveCmd := -50.0; END_IF;
        END_IF;
        
        IF ABS(rErrSwing) < 0.1 AND ABS(rSwingSpeedAct) < 0.05 THEN
            iStateMachine := 50;
        END_IF;
        
    50: // DUMP - Open bucket at truck location
        rBucketValveCmd := -100.0; // Full open
        
        rCycleTimer := rCycleTimer + rDeltaTime;
        IF rCycleTimer > 1.5 THEN
            rCycleTimer := 0.0;
            bLoadComplete := TRUE;
            iStateMachine := 60;
        END_IF;
        
    60: // RETURN - Swing back to trench
        rErrSwing := 0.0 - rDumpTruckX; // Return to origin
        rSwingValveCmd := rErrSwing * 2.0; // Faster return empty
        
        IF ABS(rErrSwing) < 0.1 THEN
            iStateMachine := 0;
        END_IF;
        
    ELSE
        iStateMachine := 0;
END_CASE;

// Valve command saturation limits
IF rBoomValveCmd > 100.0 THEN rBoomValveCmd := 100.0; ELSIF rBoomValveCmd < -100.0 THEN rBoomValveCmd := -100.0; END_IF;
IF rStickValveCmd > 100.0 THEN rStickValveCmd := 100.0; ELSIF rStickValveCmd < -100.0 THEN rStickValveCmd := -100.0; END_IF;
IF rBucketValveCmd > 100.0 THEN rBucketValveCmd := 100.0; ELSIF rBucketValveCmd < -100.0 THEN rBucketValveCmd := -100.0; END_IF;
IF rSwingValveCmd > 100.0 THEN rSwingValveCmd := 100.0; ELSIF rSwingValveCmd < -100.0 THEN rSwingValveCmd := -100.0; END_IF;

END_FUNCTION_BLOCK
```"""

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": code}
    ]
}

os.makedirs('data', exist_ok=True)
with open('data/synthetic_generation_v3_enterprise.jsonl', 'a', encoding='utf-8') as f:
    f.write(json.dumps(record) + "\\n")
