import json
import uuid
import os

workspace = r"c:\Users\majip\Downloads\LLM REASEARCH"
swarm_dir = os.path.join(workspace, "data", "swarm_raw")
os.makedirs(swarm_dir, exist_ok=True)
jsonl_file = os.path.join(workspace, "data", "synthetic_generation_v3_enterprise.jsonl")

prompt = "Invent a highly complex control scenario for an Industrial Bread Proofing Tower (multi-tiered rack helical indexing, ultrasonic humidity injection atomization, and convective heat profiling). Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."

st_code = """```iec-st
FUNCTION_BLOCK FB_BreadProofingTower_HelicalIndexer
TITLE = 'Enterprise Grade Multi-Tier Bread Proofing Tower Control'
VERSION : '1.0'

(*
  This function block handles the deterministic control of an industrial bread proofing tower.
  It coordinates the multi-tiered helical indexing mechanism for rack movement,
  ultrasonic humidity injection atomization for precise moisture control, 
  and convective heat profiling for optimal dough rising.
*)

VAR_INPUT
    bSystemEnable         : BOOL;  (* Master enable for the proofing tower *)
    rTargetTemp_C         : REAL;  (* Target convective heat profile temp in Celsius (e.g. 35.0) *)
    rTargetHum_RH         : REAL;  (* Target relative humidity % (e.g. 85.0) *)
    rIndexerSpeed_RPM     : REAL;  (* Helical indexer rotation speed (e.g. 2.5 RPM) *)
    bTrayLoadDetect       : BOOL;  (* Sensor detecting new dough tray at entrance conveyor *)
    bTrayUnloadDetect     : BOOL;  (* Sensor detecting dough tray at exit conveyor *)
    rExhaustFanTarget_Pct : REAL;  (* Desired exhaust fan speed % *)
    bEmergencyStop        : BOOL;  (* Safety E-Stop signal *)
END_VAR

VAR_OUTPUT
    bHeaterEnable         : BOOL;  (* Enable convective heaters *)
    rHeaterOutput_PWM     : REAL;  (* Heater PWM output 0-100% *)
    bUltrasonicEnable     : BOOL;  (* Enable ultrasonic atomizers *)
    rUltrasonicLevel_PWM  : REAL;  (* Atomizer intensity 0-100% *)
    bIndexerMotorRun      : BOOL;  (* Enable helical indexer motor *)
    rIndexerMotorFreq_Hz  : REAL;  (* VFD frequency for indexer *)
    bSystemReady          : BOOL;  (* Tower is at temperature and humidity setpoints *)
    bAlarmActive          : BOOL;  (* System fault active *)
    iErrorCode            : INT;   (* Fault code for HMI display *)
    rActualTemp_C         : REAL;  (* Measured average tower temperature *)
    rActualHum_RH         : REAL;  (* Measured average tower humidity *)
END_VAR

VAR
    rZone1Temp_C          : REAL := 22.0; (* Simulated sensor 1 *)
    rZone2Temp_C          : REAL := 22.0; (* Simulated sensor 2 *)
    rZone1Hum_RH          : REAL := 40.0; (* Simulated hum 1 *)
    rTempError            : REAL;
    rHumError             : REAL;
    
    (* PID Controller instances *)
    pidTemp               : FB_PID_Controller;
    pidHum                : FB_PID_Controller;
    
    (* State Machine *)
    stateTower            : INT := 0; (* 0=Off, 1=Warmup, 2=Ready, 3=Indexing, 99=Error *)
    timerWarmup           : TON;
    
    (* Internal physical variables *)
    rIndexerPosition_Deg  : REAL := 0.0; (* Current angular position in helical track *)
    bInternalFault        : BOOL := FALSE;
END_VAR

(* --- Safety and Master Control --- *)
IF bEmergencyStop THEN
    stateTower := 99;
    iErrorCode := 9001; (* E-Stop Pressed *)
    bInternalFault := TRUE;
END_IF;

IF NOT bSystemEnable AND NOT bInternalFault THEN
    stateTower := 0;
    bHeaterEnable := FALSE;
    bUltrasonicEnable := FALSE;
    bIndexerMotorRun := FALSE;
    bSystemReady := FALSE;
    iErrorCode := 0;
ELSIF bSystemEnable AND stateTower = 0 AND NOT bInternalFault THEN
    stateTower := 1; (* Transition to Warmup phase *)
    timerWarmup(IN := FALSE);
END_IF;

(* --- Simulated Sensor Averaging --- *)
rActualTemp_C := (rZone1Temp_C + rZone2Temp_C) / 2.0;
rActualHum_RH := rZone1Hum_RH; (* Assuming single central humidity sensor *)

(* --- Convective Heat Profiling (PID) --- *)
rTempError := rTargetTemp_C - rActualTemp_C;
pidTemp.rSetpoint := rTargetTemp_C;
pidTemp.rProcessValue := rActualTemp_C;
pidTemp.rKp := 3.25;
pidTemp.rKi := 0.15;
pidTemp.rKd := 0.05;
pidTemp(bEnable := (stateTower > 0 AND stateTower <> 99));

IF pidTemp.rOutput > 0.0 THEN
    bHeaterEnable := TRUE;
    rHeaterOutput_PWM := pidTemp.rOutput;
ELSE
    bHeaterEnable := FALSE;
    rHeaterOutput_PWM := 0.0;
END_IF;

(* --- Ultrasonic Humidity Injection Atomization (PID) --- *)
rHumError := rTargetHum_RH - rActualHum_RH;
pidHum.rSetpoint := rTargetHum_RH;
pidHum.rProcessValue := rActualHum_RH;
pidHum.rKp := 2.10;
pidHum.rKi := 0.25;
pidHum.rKd := 0.02;
pidHum(bEnable := (stateTower > 0 AND stateTower <> 99));

IF pidHum.rOutput > 0.0 THEN
    bUltrasonicEnable := TRUE;
    rUltrasonicLevel_PWM := pidHum.rOutput;
ELSE
    bUltrasonicEnable := FALSE;
    rUltrasonicLevel_PWM := 0.0;
END_IF;

(* --- Multi-tiered Helical Indexer State Machine --- *)
CASE stateTower OF
    0: (* OFF State *)
        bSystemReady := FALSE;
        bIndexerMotorRun := FALSE;
        rIndexerMotorFreq_Hz := 0.0;

    1: (* WARMUP State: Establish Convective Profile and Atomization Base *)
        timerWarmup(IN := TRUE, PT := T#10M);
        IF (ABS(rTempError) <= 1.5) AND (ABS(rHumError) <= 2.0) THEN
            stateTower := 2;
            bSystemReady := TRUE;
        ELSIF timerWarmup.Q THEN
            stateTower := 99;
            iErrorCode := 1001; (* Warmup Timeout Error - Heating/Humidification failed *)
        END_IF;

    2: (* READY State: Awaiting Tray Load *)
        bSystemReady := TRUE;
        bIndexerMotorRun := FALSE;
        rIndexerMotorFreq_Hz := 0.0;
        
        IF bTrayLoadDetect THEN
            stateTower := 3;
        END_IF;

    3: (* INDEXING State: Helical Rack Movement *)
        bSystemReady := TRUE;
        bIndexerMotorRun := TRUE;
        
        (* Map RPM to VFD Frequency (Assuming 60Hz = 5.0 RPM as arbitrary scaling) *)
        rIndexerMotorFreq_Hz := (rIndexerSpeed_RPM / 5.0) * 60.0;
        
        (* Simulation of helical position increment *)
        rIndexerPosition_Deg := rIndexerPosition_Deg + (rIndexerSpeed_RPM * 6.0); 
        IF rIndexerPosition_Deg >= 360.0 THEN
            rIndexerPosition_Deg := rIndexerPosition_Deg - 360.0;
        END_IF;
        
        (* Exit condition when load clears or unload triggers *)
        IF NOT bTrayLoadDetect AND bTrayUnloadDetect THEN
            stateTower := 2; (* Return to ready for next tray *)
        END_IF;

    99: (* ERROR State *)
        bSystemReady := FALSE;
        bHeaterEnable := FALSE;
        rHeaterOutput_PWM := 0.0;
        bUltrasonicEnable := FALSE;
        rUltrasonicLevel_PWM := 0.0;
        bIndexerMotorRun := FALSE;
        rIndexerMotorFreq_Hz := 0.0;
        bAlarmActive := TRUE;
END_CASE;

END_FUNCTION_BLOCK
```"""

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": st_code}
    ]
}

file_id = uuid.uuid4().hex[:8]
swarm_path = os.path.join(swarm_dir, f"agent_{file_id}.json")
with open(swarm_path, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)

with open(jsonl_file, "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\\n")

print(f"Generated swarm file {swarm_path}")
