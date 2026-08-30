import os
import json
import uuid

os.makedirs('data/swarm_raw', exist_ok=True)
os.makedirs('data', exist_ok=True)

prompt = "Invent a highly complex control scenario for a Port Grain Terminal (e.g., ship unloader bucket elevator capacity tracking, silo aeration thermal mapping, and dust explosion suppression interlocks). Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."

code = """```iec-st
FUNCTION_BLOCK FB_PortGrainTerminal_MasterControl
TITLE = 'Port Grain Terminal Master Control & Safety Interlock'
VERSION : '1.0'
AUTHOR  : 'Lumina Swarm Architect'

VAR_INPUT
    // Ship Unloader & Bucket Elevator
    rBucketElevatorSpeed_rpm     : REAL;       // Current speed of the bucket elevator (RPM)
    rBucketElevatorTorque_pct    : REAL;       // Motor torque percentage
    rInfeedMassFlow_tph          : REAL;       // Mass flow rate in tons per hour
    bElevatorRunning             : BOOL;       // Elevator run status

    // Silo Aeration & Thermal Mapping
    arrSiloTempSensors           : ARRAY[1..16] OF REAL; // 16-point vertical temperature profile (deg C)
    rAmbientTemp                 : REAL;       // Ambient air temperature
    rAmbientHumidity             : REAL;       // Ambient relative humidity
    bAerationFansRunning         : ARRAY[1..4] OF BOOL;  // Status of the 4 silo aeration fans

    // Dust Explosion Suppression System (ATEX)
    rDustConcentration_mgm3      : REAL;       // Dust concentration in elevator casing
    rLowerExplosionLimit         : REAL := 40.0; // LEL limit (mg/m3)
    bSparkDetected               : BOOL;       // IR spark detector input
    bPressureReliefOpen          : BOOL;       // Explosion vent panel status
END_VAR

VAR_OUTPUT
    // Actuators & Control
    bStartAeration               : BOOL;       // Command to start aeration fans
    bStopAeration                : BOOL;       // Command to stop aeration fans
    rTargetElevatorSpeed_rpm     : REAL;       // Speed setpoint for elevator drive
    bChokeValveClose             : BOOL;       // Command to close the infeed choke valve

    // Safety Interlocks
    bSuppressorDischarge         : BOOL;       // Trigger active chemical explosion suppression
    bEmergencyStop               : BOOL;       // Trigger global E-STOP
    bAlarmHighDust               : BOOL;       // High dust concentration alarm
    bAlarmThermalRunaway         : BOOL;       // Silo thermal runaway detected
END_VAR

VAR
    // Internal state
    i                            : INT;
    rMaxSiloTemp                 : REAL;
    rTempGradient                : REAL;
    rTotalCapacity_tons          : REAL;
    tDustTimer                   : TON;
    tAerationTimer               : TON;
    bExplosionRisk               : BOOL;
    bThermalCritical             : BOOL;
    rCalculatedDewPoint          : REAL;
    rSafeTempThreshold           : REAL := 35.0; // Degrees C
    rCriticalTempThreshold       : REAL := 55.0; // Degrees C
END_VAR

(* --- [1] Ship Unloader Capacity Tracking --- *)
// Integrate mass flow to track total unloaded grain capacity
IF bElevatorRunning THEN
    // Simplified discrete integration assuming 100ms cycle time (0.1s / 3600s)
    rTotalCapacity_tons := rTotalCapacity_tons + (rInfeedMassFlow_tph * 0.00002777);
END_IF;

// Load control: throttle elevator speed if torque exceeds 90%
IF rBucketElevatorTorque_pct > 90.0 THEN
    rTargetElevatorSpeed_rpm := rTargetElevatorSpeed_rpm * 0.95; // Ramp down 5%
ELSIF rBucketElevatorTorque_pct < 70.0 AND rInfeedMassFlow_tph > 10.0 THEN
    rTargetElevatorSpeed_rpm := rBucketElevatorSpeed_rpm * 1.02; // Ramp up 2%
END_IF;

// Bounds checking for speed
IF rTargetElevatorSpeed_rpm > 1500.0 THEN
    rTargetElevatorSpeed_rpm := 1500.0;
ELSIF rTargetElevatorSpeed_rpm < 100.0 THEN
    rTargetElevatorSpeed_rpm := 100.0;
END_IF;

(* --- [2] Silo Aeration Thermal Mapping --- *)
rMaxSiloTemp := -50.0;
FOR i := 1 TO 16 DO
    IF arrSiloTempSensors[i] > rMaxSiloTemp THEN
        rMaxSiloTemp := arrSiloTempSensors[i];
    END_IF;
END_FOR;

// Calculate generic dew point proxy (simple Magnus formula approx)
rCalculatedDewPoint := rAmbientTemp - ((100.0 - rAmbientHumidity) / 5.0);

bThermalCritical := rMaxSiloTemp > rCriticalTempThreshold;
bAlarmThermalRunaway := bThermalCritical;

// Aeration logic: cool down if temp > safe threshold AND ambient is cooler than silo
IF (rMaxSiloTemp > rSafeTempThreshold) AND (rAmbientTemp < (rMaxSiloTemp - 5.0)) THEN
    bStartAeration := TRUE;
    bStopAeration  := FALSE;
ELSE
    bStartAeration := FALSE;
END_IF;

// Stop aeration if drawing in moist air (condensation risk)
IF rCalculatedDewPoint > rMaxSiloTemp THEN
    bStopAeration := TRUE;
    bStartAeration := FALSE;
END_IF;

(* --- [3] Dust Explosion Suppression Interlocks --- *)
bAlarmHighDust := (rDustConcentration_mgm3 > (rLowerExplosionLimit * 0.8)); // 80% LEL

// High dust timer logic
tDustTimer(IN := bAlarmHighDust, PT := T#5s);

// Determine explosion risk condition
bExplosionRisk := bSparkDetected OR bPressureReliefOpen OR tDustTimer.Q OR (rDustConcentration_mgm3 > rLowerExplosionLimit);

IF bExplosionRisk THEN
    bSuppressorDischarge := TRUE;  // Fire the chemical suppressors
    bEmergencyStop       := TRUE;  // Halt the entire terminal
    bChokeValveClose     := TRUE;  // Isolate the infeed
    rTargetElevatorSpeed_rpm := 0.0; // Stop motor
    bStopAeration        := TRUE;  // Stop fanning oxygen/dust
ELSE
    bSuppressorDischarge := FALSE;
END_IF;

// If thermal runaway is detected, also trigger E-STOP to isolate
IF bThermalCritical THEN
    bEmergencyStop := TRUE;
END_IF;

END_FUNCTION_BLOCK
```"""

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": code}
    ]
}

# Write user-requested output format
file_path_user = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(file_path_user, "w", encoding="utf-8") as f:
    json.dump(record, f)

# Write system-requested output format
file_path_sys = "data/synthetic_generation_v3_enterprise.jsonl"
with open(file_path_sys, "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\n")

print(f"Success. Files created: {file_path_user} and appended to {file_path_sys}")
