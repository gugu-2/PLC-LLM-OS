import json, uuid, os

os.makedirs('data/swarm_raw', exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Steel Continuous Casting Machine.
Task: Invent a highly complex control scenario for this domain (e.g., tundish slide-gate liquid metal level, mold oscillation hydraulic servo, and secondary spray cooling zones).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."""

code = """FUNCTION_BLOCK FB_ContinuousCastingMachine_Control
TITLE = 'Steel Continuous Casting Machine Integrated Control'
VERSION : '1.0'
AUTHOR : 'Lumina AI Cloud Swarm'

VAR_INPUT
    bEnableSystem         : BOOL;  (* Master enable for the entire casting machine *)
    rMoldLevelSetpoint    : REAL;  (* Desired liquid metal level in the mold (mm) *)
    rMoldLevelActual      : REAL;  (* Actual liquid metal level measured by radiometric sensor (mm) *)
    rTundishWeight        : REAL;  (* Actual weight of the tundish (tons) *)
    rCastingSpeedActual   : REAL;  (* Actual casting speed of the strand (m/min) *)
    rCastingSpeedSetp     : REAL;  (* Setpoint casting speed (m/min) *)
    rMoldOscFrequency     : REAL;  (* Desired oscillation frequency (Hz) *)
    rMoldOscStroke        : REAL;  (* Desired oscillation stroke (mm) *)
    rSecondaryCoolingP    : REAL;  (* Secondary spray cooling water pressure setpoint (bar) *)
    aZoneTemps            : ARRAY[1..5] OF REAL; (* Actual temperatures of 5 cooling zones *)
    bEmergencyStop        : BOOL;  (* E-Stop condition *)
END_VAR

VAR_OUTPUT
    rSlideGatePositionCmd : REAL;  (* Command to hydraulic servo for tundish slide gate (0-100%) *)
    rOscillatorServoCmd   : REAL;  (* Command to mold oscillation hydraulic servo (-10.0 to 10.0V) *)
    aSprayCoolingValveCmd : ARRAY[1..5] OF REAL; (* Command to spray cooling proportional valves (0-100%) *)
    bSystemReady          : BOOL;  (* System ready status flag *)
    bAlarmLevelHigh       : BOOL;  (* Mold level alarm (high) *)
    bAlarmLevelLow        : BOOL;  (* Mold level alarm (low) *)
    bAlarmCooling         : BOOL;  (* Cooling system alarm flag *)
END_VAR

VAR
    (* Internal State and PID variables *)
    fbMoldLevelPID        : PID_Compact;
    fbOscillationGenerator: LGF_Sine; (* Sine wave generator for oscillation *)
    fbSprayCoolingPID     : ARRAY[1..5] OF PID_Compact;
    
    rMoldLevelError       : REAL;
    rSlideGateIntegrator  : REAL;
    rSlideGateKp          : REAL := 2.5;
    rSlideGateKi          : REAL := 0.15;
    rSlideGateKd          : REAL := 0.05;
    rSlideGatePrevError   : REAL;
    
    tCycleTime            : TIME := T#10ms;
    rCycleTimeSec         : REAL := 0.01;
    
    rOscillationPhase     : REAL := 0.0;
    
    i                     : INT;
    rZoneTargetTemps      : ARRAY[1..5] OF REAL := [900.0, 850.0, 800.0, 750.0, 700.0]; (* Deg C *)
    rCoolingKp            : REAL := 1.2;
    
    bInitDone             : BOOL := FALSE;
END_VAR

(* Initialization phase *)
IF NOT bInitDone THEN
    rSlideGateIntegrator := 0.0;
    rSlideGatePrevError := 0.0;
    rOscillationPhase := 0.0;
    
    FOR i := 1 TO 5 DO
        aSprayCoolingValveCmd[i] := 0.0;
    END_FOR
    
    bSystemReady := TRUE;
    bInitDone := TRUE;
END_IF

(* Emergency Stop Handling *)
IF bEmergencyStop THEN
    rSlideGatePositionCmd := 0.0; (* Close slide gate immediately *)
    rOscillatorServoCmd := 0.0;   (* Stop mold oscillation *)
    FOR i := 1 TO 5 DO
        aSprayCoolingValveCmd[i] := 100.0; (* Max cooling during E-Stop to solidify steel *)
    END_FOR
    bSystemReady := FALSE;
    bAlarmLevelHigh := FALSE;
    bAlarmLevelLow := FALSE;
    bAlarmCooling := TRUE;
    RETURN;
END_IF

IF NOT bEnableSystem THEN
    rSlideGatePositionCmd := 0.0;
    rOscillatorServoCmd := 0.0;
    bSystemReady := TRUE;
    RETURN;
END_IF

(* 1. Tundish Slide-Gate Liquid Metal Level Control (Mold Level Control) *)
rMoldLevelError := rMoldLevelSetpoint - rMoldLevelActual;

(* Simple PID implementation for Slide Gate Position (0-100%) *)
rSlideGateIntegrator := rSlideGateIntegrator + (rMoldLevelError * rCycleTimeSec);

(* Anti-windup for integrator *)
IF rSlideGateIntegrator > 100.0 THEN rSlideGateIntegrator := 100.0; END_IF
IF rSlideGateIntegrator < 0.0 THEN rSlideGateIntegrator := 0.0; END_IF

rSlideGatePositionCmd := (rSlideGateKp * rMoldLevelError) + (rSlideGateKi * rSlideGateIntegrator) + (rSlideGateKd * (rMoldLevelError - rSlideGatePrevError) / rCycleTimeSec);

(* Saturate output *)
IF rSlideGatePositionCmd > 100.0 THEN
    rSlideGatePositionCmd := 100.0;
ELSIF rSlideGatePositionCmd < 0.0 THEN
    rSlideGatePositionCmd := 0.0;
END_IF

rSlideGatePrevError := rMoldLevelError;

(* Mold Level Alarms *)
bAlarmLevelHigh := (rMoldLevelActual > (rMoldLevelSetpoint + 15.0));
bAlarmLevelLow := (rMoldLevelActual < (rMoldLevelSetpoint - 15.0));

(* 2. Mold Oscillation Hydraulic Servo Control *)
(* Generates a position command based on required frequency and stroke *)
(* The command is a sinusoidal wave converted to a +/- 10V analog signal for the servo valve *)

rOscillationPhase := rOscillationPhase + (2.0 * 3.14159265 * rMoldOscFrequency * rCycleTimeSec);
IF rOscillationPhase > (2.0 * 3.14159265) THEN
    rOscillationPhase := rOscillationPhase - (2.0 * 3.14159265);
END_IF

(* Calculate instantaneous position setpoint and scale to servo voltage (-10V to 10V) *)
(* Assuming max stroke is 20mm which equals 10V *)
rOscillatorServoCmd := (rMoldOscStroke / 2.0) * SIN(rOscillationPhase) * (10.0 / 10.0); (* scaled assuming stroke is up to 20mm peak-to-peak *)
IF rOscillatorServoCmd > 10.0 THEN rOscillatorServoCmd := 10.0; END_IF
IF rOscillatorServoCmd < -10.0 THEN rOscillatorServoCmd := -10.0; END_IF

(* 3. Secondary Spray Cooling Zones Control *)
(* Adjusts the proportional valves for water flow based on temperature setpoints per zone *)
bAlarmCooling := FALSE;

FOR i := 1 TO 5 DO
    (* Proportional control for cooling based on temperature deviation *)
    IF aZoneTemps[i] > rZoneTargetTemps[i] THEN
        aSprayCoolingValveCmd[i] := (aZoneTemps[i] - rZoneTargetTemps[i]) * rCoolingKp;
    ELSE
        aSprayCoolingValveCmd[i] := 10.0; (* Minimum cooling flow *)
    END_IF
    
    (* Saturate Valve Command *)
    IF aSprayCoolingValveCmd[i] > 100.0 THEN
        aSprayCoolingValveCmd[i] := 100.0;
    END_IF
    
    (* Cooling Alarm Condition (Overheating) *)
    IF aZoneTemps[i] > (rZoneTargetTemps[i] + 50.0) THEN
        bAlarmCooling := TRUE;
    END_IF
END_FOR

END_FUNCTION_BLOCK
"""

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": f"```iec-st\n{code}\n```"}
    ]
}

file_path = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(file_path, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=4)

print(f"Generated {file_path}")
