import json, uuid, os

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Glass Fiber Drawing & Winding.
Task: Invent a highly complex control scenario for this domain (e.g., Platinum-Rhodium bushing temperature tracking, strand sizing applicator cascades, and high-speed turret collet tension).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."""

response = """```iec-st
FUNCTION_BLOCK FB_GlassFiberDrawControl
VAR_INPUT
    bEnableDraw             : BOOL;                 (* Start overall draw process *)
    rBushingTempSetPoint    : REAL := 1250.0;       (* Platinum-Rhodium bushing temp setpoint °C *)
    rActualBushingTemp      : REAL;                 (* Feedback from IR sensor or thermocouple *)
    rDrawSpeedSetPoint      : REAL := 25.0;         (* Target drawing speed in m/s *)
    rActualDrawSpeed        : REAL;                 (* Feedback from turret encoder *)
    rWindingTensionSetPoint : REAL := 10.0;         (* Target strand winding tension in N *)
    rActualWindingTension   : REAL;                 (* Feedback from tension load cell *)
    rApplicatorFlowSetPoint : REAL := 5.0;          (* Sizing applicator flow rate L/min *)
    rActualApplicatorFlow   : REAL;                 (* Feedback from flow meter *)
    bColletTransferReq      : BOOL;                 (* Request to transfer to new collet on turret *)
END_VAR

VAR_OUTPUT
    bSystemReady            : BOOL;                 (* All parameters within tolerance, ready to run *)
    rBushingPowerOutput     : REAL;                 (* 0-100% control signal to thyristor pack *)
    rColletMotorTorqueReq   : REAL;                 (* 0-100% control signal to collet motor drive *)
    rApplicatorPumpSpeed    : REAL;                 (* 0-100% control signal to sizing pump *)
    bTurretRotate           : BOOL;                 (* Command to rotate turret for bobbin swap *)
    bTurretCutStrand        : BOOL;                 (* Command to actuate chopper/cutter during swap *)
    iAlarmCode              : INT;                  (* 0=No Alarm, >0 = specific fault *)
END_VAR

VAR
    rTempError              : REAL;
    rTempIntegral           : REAL;
    rTempKp                 : REAL := 0.25;
    rTempKi                 : REAL := 0.05;
    
    rSpeedError             : REAL;
    rSpeedIntegral          : REAL;
    rSpeedKp                : REAL := 1.2;
    rSpeedKi                : REAL := 0.15;

    rTensionError           : REAL;
    rTensionIntegral        : REAL;
    rTensionKp              : REAL := 0.8;
    rTensionKi              : REAL := 0.1;
    
    rFlowError              : REAL;
    rFlowIntegral           : REAL;
    rFlowKp                 : REAL := 1.5;
    rFlowKi                 : REAL := 0.2;

    iTransferStep           : INT := 0;
    rTransferTimer          : REAL := 0.0;
    bTransferActive         : BOOL := FALSE;
    
    rCycleTime              : REAL := 0.01;         (* 10ms execution cycle *)
END_VAR

(* 1. Bushing Temperature Control (PID) *)
rTempError := rBushingTempSetPoint - rActualBushingTemp;
IF bEnableDraw THEN
    rTempIntegral := rTempIntegral + (rTempError * rCycleTime);
    (* Anti-windup *)
    IF rTempIntegral > 1000.0 THEN rTempIntegral := 1000.0; END_IF;
    IF rTempIntegral < -1000.0 THEN rTempIntegral := -1000.0; END_IF;
    rBushingPowerOutput := (rTempKp * rTempError) + (rTempKi * rTempIntegral);
    (* Clamp output 0-100 *)
    IF rBushingPowerOutput > 100.0 THEN rBushingPowerOutput := 100.0; END_IF;
    IF rBushingPowerOutput < 0.0 THEN rBushingPowerOutput := 0.0; END_IF;
ELSE
    rTempIntegral := 0.0;
    rBushingPowerOutput := 0.0;
END_IF;

(* 2. Sizing Applicator Cascade Control (PID) *)
rFlowError := rApplicatorFlowSetPoint - rActualApplicatorFlow;
IF bEnableDraw AND rActualBushingTemp > (rBushingTempSetPoint - 50.0) THEN
    rFlowIntegral := rFlowIntegral + (rFlowError * rCycleTime);
    (* Anti-windup *)
    IF rFlowIntegral > 500.0 THEN rFlowIntegral := 500.0; END_IF;
    IF rFlowIntegral < -500.0 THEN rFlowIntegral := -500.0; END_IF;
    rApplicatorPumpSpeed := (rFlowKp * rFlowError) + (rFlowKi * rFlowIntegral);
    IF rApplicatorPumpSpeed > 100.0 THEN rApplicatorPumpSpeed := 100.0; END_IF;
    IF rApplicatorPumpSpeed < 0.0 THEN rApplicatorPumpSpeed := 0.0; END_IF;
ELSE
    rFlowIntegral := 0.0;
    rApplicatorPumpSpeed := 0.0;
END_IF;

(* 3. High-Speed Turret Collet Tension Control (PID) *)
rTensionError := rWindingTensionSetPoint - rActualWindingTension;
IF bEnableDraw THEN
    rTensionIntegral := rTensionIntegral + (rTensionError * rCycleTime);
    (* Anti-windup *)
    IF rTensionIntegral > 500.0 THEN rTensionIntegral := 500.0; END_IF;
    IF rTensionIntegral < -500.0 THEN rTensionIntegral := -500.0; END_IF;
    rColletMotorTorqueReq := (rTensionKp * rTensionError) + (rTensionKi * rTensionIntegral);
    (* Add feed-forward based on draw speed setpoint *)
    rColletMotorTorqueReq := rColletMotorTorqueReq + (rDrawSpeedSetPoint * 0.5);
    IF rColletMotorTorqueReq > 100.0 THEN rColletMotorTorqueReq := 100.0; END_IF;
    IF rColletMotorTorqueReq < 0.0 THEN rColletMotorTorqueReq := 0.0; END_IF;
ELSE
    rTensionIntegral := 0.0;
    rColletMotorTorqueReq := 0.0;
END_IF;

(* 4. Turret Auto-Transfer Sequence *)
IF bColletTransferReq AND NOT bTransferActive THEN
    bTransferActive := TRUE;
    iTransferStep := 1;
    rTransferTimer := 0.0;
END_IF;

IF bTransferActive THEN
    rTransferTimer := rTransferTimer + rCycleTime;
    CASE iTransferStep OF
        1: (* Accelerate empty collet *)
            IF rTransferTimer > 2.0 THEN
                iTransferStep := 2;
                rTransferTimer := 0.0;
                bTurretRotate := TRUE;
            END_IF;
        2: (* Rotate turret *)
            IF rTransferTimer > 1.5 THEN
                iTransferStep := 3;
                rTransferTimer := 0.0;
                bTurretRotate := FALSE;
                bTurretCutStrand := TRUE;
            END_IF;
        3: (* Cut and snatch strand *)
            IF rTransferTimer > 0.5 THEN
                iTransferStep := 4;
                rTransferTimer := 0.0;
                bTurretCutStrand := FALSE;
            END_IF;
        4: (* Transfer complete *)
            bTransferActive := FALSE;
            iTransferStep := 0;
    END_CASE;
ELSE
    bTurretRotate := FALSE;
    bTurretCutStrand := FALSE;
END_IF;

(* 5. Diagnostics and Readiness *)
bSystemReady := (ABS(rTempError) < 5.0) AND (ABS(rFlowError) < 0.5);
iAlarmCode := 0;
IF ABS(rTempError) > 20.0 THEN iAlarmCode := 1; END_IF; (* Temperature deviation fault *)
IF ABS(rTensionError) > 5.0 THEN iAlarmCode := 2; END_IF; (* Tension break / slip fault *)
IF rActualBushingTemp > 1300.0 THEN iAlarmCode := 3; END_IF; (* Over-temp safety trip *)

END_FUNCTION_BLOCK
```"""
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": response}]}
file_path = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(file_path, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False, indent=2)
print(file_path)
