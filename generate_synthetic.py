import json, uuid
import os

os.makedirs("data/swarm_raw", exist_ok=True)
os.makedirs("data", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Subsea Cable Trenching ROV.
Task: Invent a highly complex control scenario for this domain (e.g., water jetting sword differential pressure, track slippage odometry compensation, and seabed burial depth profiling).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."""

iec_st_code = """```iec-st
FUNCTION_BLOCK FB_SubseaTrenchingROV
VAR_INPUT
    bEnable : BOOL;
    fPortTrackSpeedCmd : REAL; (* m/s *)
    fStbdTrackSpeedCmd : REAL; (* m/s *)
    fPortTrackEncoder : REAL; (* pulses/sec *)
    fStbdTrackEncoder : REAL; (* pulses/sec *)
    fJetPump1Pressure : REAL; (* bar *)
    fJetPump2Pressure : REAL; (* bar *)
    fSwordDepthSensor : REAL; (* mm *)
    fAltimeterForward : REAL; (* mm *)
    fAltimeterAft : REAL; (* mm *)
    fPitchAngle : REAL; (* degrees *)
    fRollAngle : REAL; (* degrees *)
END_VAR
VAR_OUTPUT
    fPortTrackDriveOut : REAL; (* 0-100% *)
    fStbdTrackDriveOut : REAL; (* 0-100% *)
    fJetPump1VFDOut : REAL; (* 0-100% *)
    fJetPump2VFDOut : REAL; (* 0-100% *)
    fSwordActuatorOut : REAL; (* -100 to 100% *)
    bAlarmSlippage : BOOL;
    bAlarmJetPressure : BOOL;
    bAlarmBurialDepth : BOOL;
    fEstimatedBurialDepth : REAL; (* mm *)
END_VAR
VAR
    (* Internal State and Timers *)
    fPortTrackSpeedAct : REAL;
    fStbdTrackSpeedAct : REAL;
    fPortSlipRatio : REAL;
    fStbdSlipRatio : REAL;
    fEncoderScaling : REAL := 0.005; (* m/pulse *)
    
    (* PI Controllers for Tracks *)
    fPortKp : REAL := 2.5;
    fPortKi : REAL := 0.5;
    fPortError : REAL;
    fPortErrorInt : REAL;
    
    fStbdKp : REAL := 2.5;
    fStbdKi : REAL := 0.5;
    fStbdError : REAL;
    fStbdErrorInt : REAL;
    
    (* Jetting Control *)
    fJetPressureSetPt : REAL := 150.0; (* bar *)
    fJetKp : REAL := 1.2;
    fJetError1 : REAL;
    fJetError2 : REAL;
    
    (* Sword and Depth Profiling *)
    fTargetBurialDepth : REAL := 1500.0; (* mm *)
    fDepthError : REAL;
    fSwordKp : REAL := 3.0;
    
    (* Timers for Alarms *)
    tSlipTimer : TON;
    tJetTimer : TON;
    tDepthTimer : TON;
END_VAR

IF NOT bEnable THEN
    fPortTrackDriveOut := 0.0;
    fStbdTrackDriveOut := 0.0;
    fJetPump1VFDOut := 0.0;
    fJetPump2VFDOut := 0.0;
    fSwordActuatorOut := 0.0;
    bAlarmSlippage := FALSE;
    bAlarmJetPressure := FALSE;
    bAlarmBurialDepth := FALSE;
    fPortErrorInt := 0.0;
    fStbdErrorInt := 0.0;
    RETURN;
END_IF;

(* Track Slippage Odometry Compensation *)
fPortTrackSpeedAct := fPortTrackEncoder * fEncoderScaling;
fStbdTrackSpeedAct := fStbdTrackEncoder * fEncoderScaling;

IF fPortTrackSpeedCmd > 0.0 THEN
    fPortSlipRatio := (fPortTrackSpeedCmd - fPortTrackSpeedAct) / fPortTrackSpeedCmd;
ELSE
    fPortSlipRatio := 0.0;
END_IF;

IF fStbdTrackSpeedCmd > 0.0 THEN
    fStbdSlipRatio := (fStbdTrackSpeedCmd - fStbdTrackSpeedAct) / fStbdTrackSpeedCmd;
ELSE
    fStbdSlipRatio := 0.0;
END_IF;

bAlarmSlippage := (fPortSlipRatio > 0.3) OR (fStbdSlipRatio > 0.3);

(* PI Control for Port Track with Slip Compensation *)
fPortError := (fPortTrackSpeedCmd * (1.0 + fPortSlipRatio)) - fPortTrackSpeedAct;
fPortErrorInt := fPortErrorInt + fPortError * 0.1; (* 100ms cycle assumed *)
IF fPortErrorInt > 100.0 THEN fPortErrorInt := 100.0; END_IF;
IF fPortErrorInt < -100.0 THEN fPortErrorInt := -100.0; END_IF;
fPortTrackDriveOut := (fPortKp * fPortError) + (fPortKi * fPortErrorInt);

(* PI Control for Stbd Track with Slip Compensation *)
fStbdError := (fStbdTrackSpeedCmd * (1.0 + fStbdSlipRatio)) - fStbdTrackSpeedAct;
fStbdErrorInt := fStbdErrorInt + fStbdError * 0.1;
IF fStbdErrorInt > 100.0 THEN fStbdErrorInt := 100.0; END_IF;
IF fStbdErrorInt < -100.0 THEN fStbdErrorInt := -100.0; END_IF;
fStbdTrackDriveOut := (fStbdKp * fStbdError) + (fStbdKi * fStbdErrorInt);

(* Water Jetting Sword Differential Pressure Control *)
fJetError1 := fJetPressureSetPt - fJetPump1Pressure;
fJetPump1VFDOut := fJetPump1VFDOut + (fJetKp * fJetError1 * 0.1);

fJetError2 := fJetPressureSetPt - fJetPump2Pressure;
fJetPump2VFDOut := fJetPump2VFDOut + (fJetKp * fJetError2 * 0.1);

IF fJetPump1VFDOut > 100.0 THEN fJetPump1VFDOut := 100.0; END_IF;
IF fJetPump1VFDOut < 0.0 THEN fJetPump1VFDOut := 0.0; END_IF;
IF fJetPump2VFDOut > 100.0 THEN fJetPump2VFDOut := 100.0; END_IF;
IF fJetPump2VFDOut < 0.0 THEN fJetPump2VFDOut := 0.0; END_IF;

bAlarmJetPressure := (fJetPump1Pressure < (fJetPressureSetPt * 0.7)) OR (fJetPump2Pressure < (fJetPressureSetPt * 0.7));

(* Seabed Burial Depth Profiling and Sword Control *)
fEstimatedBurialDepth := fSwordDepthSensor * COS(fPitchAngle * 3.14159 / 180.0) + ((fAltimeterForward + fAltimeterAft) / 2.0);

fDepthError := fTargetBurialDepth - fEstimatedBurialDepth;
fSwordActuatorOut := fSwordKp * fDepthError;

IF fSwordActuatorOut > 100.0 THEN fSwordActuatorOut := 100.0; END_IF;
IF fSwordActuatorOut < -100.0 THEN fSwordActuatorOut := -100.0; END_IF;

bAlarmBurialDepth := ABS(fDepthError) > 200.0;

END_FUNCTION_BLOCK
```"""

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": iec_st_code}
    ]
}

# 1. Save to swarm_raw per user prompt
file_path = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(file_path, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)

# 2. Append to synthetic_generation_v3_enterprise.jsonl per agent system instructions
with open("data/synthetic_generation_v3_enterprise.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\\n")

print(f"JSON generation completed successfully.")
