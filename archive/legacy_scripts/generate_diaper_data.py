import json
import uuid
import os

base_dir = r"c:\Users\majip\Downloads\LLM REASEARCH\data\swarm_raw"
os.makedirs(base_dir, exist_ok=True)

user_prompt = "Generate a highly complex control scenario for a High-Speed Web Diaper Manufacturing Line (SAP gravimetric dosing, non-woven ultrasonic bonding, and elastic strand tensioning cascades) in Structured Text."

iec_code = """```iec-st
FUNCTION_BLOCK FB_DiaperLine_MasterControl
VAR_INPUT
    bEnableLine : BOOL; (* Main start/stop command *)
    rTargetLineSpeed : REAL; (* [m/min] Target speed of the web *)
    
    (* SAP Dosing Inputs *)
    rSAP_WeightFeedback : REAL; (* [g] Current weight of the SAP hopper *)
    rSAP_TargetGsm : REAL; (* [g/m2] Target superabsorbent polymer density *)
    
    (* Ultrasonic Bonding Inputs *)
    rBondingTempFeedback : REAL; (* [degC] Anvil temperature *)
    rBondingPressureFbk : REAL; (* [N] Current bonding pressure *)
    
    (* Elastic Strand Tensioning Inputs *)
    rElasticTensionFbk : REAL; (* [N] Measured tension of elastic strands *)
    rElasticTargetTension : REAL; (* [N] Setpoint for elastic tension *)
END_VAR

VAR_OUTPUT
    bSystemReady : BOOL;
    bFaultActive : BOOL;
    iFaultCode : INT;
    
    (* SAP Dosing Outputs *)
    rSAP_AugerSpeedRef : REAL; (* [%] Speed reference for dosing auger *)
    
    (* Ultrasonic Outputs *)
    rBondingAmplitudeCmd : REAL; (* [%] Amplitude command to ultrasonic generator *)
    rBondingPressureCmd : REAL; (* [N] Command to pneumatic pressure valve *)
    
    (* Elastic Tension Outputs *)
    rElasticUnwindSpeedCmd : REAL; (* [m/min] Speed command for elastic unwinder *)
END_VAR

VAR
    eState : INT := 0;
    
    (* Internal SAP Variables *)
    rSAP_DosingRate : REAL;
    rSAP_Error : REAL;
    rSAP_Integral : REAL;
    rSAP_Derivative : REAL;
    rSAP_LastError : REAL;
    rSAP_Kp : REAL := 1.5;
    rSAP_Ki : REAL := 0.2;
    rSAP_Kd : REAL := 0.05;
    
    (* Internal Bonding Variables *)
    rBond_BaseAmplitude : REAL := 50.0;
    
    (* Internal Elastic Variables *)
    rTension_Error : REAL;
    rTension_Integral : REAL;
    rTension_Kp : REAL := 2.0;
    rTension_Ki : REAL := 0.5;
    rTension_SpeedTrim : REAL;
    
    (* Timers & Filters *)
    tStartupDelay : TON;
    rFilteredTension : REAL;
END_VAR

(* =========================================================================
   State Machine for Diaper Line Initialization and Operation
   ========================================================================= *)
CASE eState OF
    0: (* IDLE *)
        bSystemReady := FALSE;
        rSAP_AugerSpeedRef := 0.0;
        rBondingAmplitudeCmd := 0.0;
        rBondingPressureCmd := 0.0;
        rElasticUnwindSpeedCmd := 0.0;
        
        IF bEnableLine THEN
            eState := 10;
        END_IF;
        
    10: (* PRE-CHARGE / RAMP-UP *)
        (* Engage bonding pressure before web movement *)
        rBondingPressureCmd := 500.0; (* Base engagement pressure *)
        
        tStartupDelay(IN:=TRUE, PT:=T#2S);
        IF tStartupDelay.Q THEN
            tStartupDelay(IN:=FALSE);
            eState := 20;
        END_IF;
        
    20: (* RUNNING *)
        bSystemReady := TRUE;
        
        (* --- 1. SAP Gravimetric Dosing Cascade Control --- *)
        (* Calculate required dosing rate based on line speed and target GSM *)
        rSAP_DosingRate := (rTargetLineSpeed * rSAP_TargetGsm) / 60.0; 
        
        rSAP_Error := rSAP_DosingRate - rSAP_WeightFeedback;
        rSAP_Integral := rSAP_Integral + (rSAP_Error * 0.01); (* 10ms cycle assumed *)
        rSAP_Derivative := (rSAP_Error - rSAP_LastError) / 0.01;
        
        rSAP_AugerSpeedRef := (rSAP_Kp * rSAP_Error) + (rSAP_Ki * rSAP_Integral) + (rSAP_Kd * rSAP_Derivative);
        
        (* Anti-windup and clamping *)
        IF rSAP_AugerSpeedRef > 100.0 THEN
            rSAP_AugerSpeedRef := 100.0;
        ELSIF rSAP_AugerSpeedRef < 0.0 THEN
            rSAP_AugerSpeedRef := 0.0;
        END_IF;
        rSAP_LastError := rSAP_Error;
        
        (* --- 2. Ultrasonic Bonding Control --- *)
        (* Amplitude is dynamically adjusted based on line speed to ensure consistent energy delivery *)
        IF rTargetLineSpeed > 0.0 THEN
            rBondingAmplitudeCmd := rBond_BaseAmplitude + (rTargetLineSpeed * 0.1);
        ELSE
            rBondingAmplitudeCmd := 0.0;
        END_IF;
        
        (* Ensure amplitude doesn't exceed generator limits *)
        IF rBondingAmplitudeCmd > 100.0 THEN
            rBondingAmplitudeCmd := 100.0;
        END_IF;
        
        (* --- 3. Elastic Strand Tensioning Cascade --- *)
        (* Filter tension feedback *)
        rFilteredTension := rFilteredTension + 0.1 * (rElasticTensionFbk - rFilteredTension);
        
        rTension_Error := rElasticTargetTension - rFilteredTension;
        rTension_Integral := rTension_Integral + (rTension_Error * 0.01);
        
        (* PI Control for speed trim *)
        rTension_SpeedTrim := (rTension_Kp * rTension_Error) + (rTension_Ki * rTension_Integral);
        
        (* Main unwind speed is ratio of line speed + tension trim *)
        rElasticUnwindSpeedCmd := rTargetLineSpeed - rTension_SpeedTrim;
        
        IF NOT bEnableLine THEN
            eState := 30;
        END_IF;
        
    30: (* RAMP-DOWN *)
        bSystemReady := FALSE;
        rSAP_AugerSpeedRef := 0.0;
        rBondingAmplitudeCmd := 0.0;
        rBondingPressureCmd := 0.0;
        rElasticUnwindSpeedCmd := 0.0;
        eState := 0;
        
END_CASE;
```"""

record = {
    "messages": [
        {"role": "user", "content": user_prompt},
        {"role": "assistant", "content": iec_code}
    ]
}

filename = os.path.join(base_dir, f"agent_{uuid.uuid4().hex[:8]}.json")
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)

print(f"Success! Saved to {filename}")
