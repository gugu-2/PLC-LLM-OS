import os
import json
import uuid

prompt = "You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.\\nYour specific domain is: Automotive Tire Building Machine (TBM).\\nTask: Invent a highly complex control scenario for this domain (e.g., ply drum expansion servo indexing, tread application vision profiling, and carcass stitcher roller dynamic pressure).\\nWrite a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."

st_code = """FUNCTION_BLOCK FB_TireBuildingMachine_MasterControl
TITLE = 'Automotive Tire Building Machine Master Controller'
VERSION : '1.0'

VAR_INPUT
    bEnable                 : BOOL;   (* System Enable *)
    bStartAutoCycle         : BOOL;   (* Initiate TBM cycle *)
    bEmergencyStop          : BOOL;   (* E-Stop active low *)
    bVisionDataReady        : BOOL;   (* Vision system data is ready *)
    rTargetPlyDrumDia       : REAL;   (* Target expansion diameter in mm *)
    rActualPlyDrumDia       : REAL;   (* Actual drum diameter from LVDT/Encoder *)
    rTreadVisionProfile     : ARRAY[0..127] OF REAL; (* Tread thickness mapping *)
    rStitcherBasePressure   : REAL;   (* Base pneumatic/hydraulic pressure in bar *)
    rActualStitcherPress    : REAL;   (* Actual stitcher roller pressure *)
    rDrumRotationalPos      : REAL;   (* 0.0 to 360.0 degrees *)
END_VAR

VAR_OUTPUT
    bSystemReady            : BOOL;   (* System is ready for operation *)
    bCycleActive            : BOOL;   (* Automatic cycle in progress *)
    bFault                  : BOOL;   (* Global fault indicator *)
    iFaultCode              : INT;    (* Fault code for HMI *)
    sStateDescription       : STRING(50); (* Current state machine step text *)
    rDrumExpansionServoCmd  : REAL;   (* Analog/Network command to expansion servo *)
    rDrumRotationServoCmd   : REAL;   (* Command to drum rotation servo *)
    rStitcherPressureCmd    : REAL;   (* Dynamic command to proportional valve *)
    bVisionTrigger          : BOOL;   (* Trigger vision capture *)
END_VAR

VAR
    iState                  : INT := 0; (* Main sequence state *)
    tStepTimer              : TON;      (* General step delay timer *)
    tStitchTimer            : TON;      (* Stitching duration timer *)
    
    (* Expansion PID Variables *)
    rExpError               : REAL;
    rExpIntegral            : REAL;
    rExpDerivative          : REAL;
    rExpLastError           : REAL;
    rKp_Exp                 : REAL := 2.5;
    rKi_Exp                 : REAL := 0.5;
    rKd_Exp                 : REAL := 0.1;
    
    (* Vision and Stitcher Variables *)
    iProfileIndex           : INT;
    rDynamicPressureMod     : REAL;
    
    (* State Constants *)
    STATE_IDLE              : INT := 0;
    STATE_INIT_EXPANSION    : INT := 10;
    STATE_WAIT_EXPANSION    : INT := 11;
    STATE_APPLY_INNERLINER  : INT := 20;
    STATE_VISION_PROFILING  : INT := 30;
    STATE_TREAD_APPLICATION : INT := 40;
    STATE_CARCASS_STITCHING : INT := 50;
    STATE_RETRACT           : INT := 60;
    STATE_FAULT             : INT := 999;
END_VAR

(* --------------------------------------------------------------------------
   FAULT HANDLING & EMERGENCY STOP
   -------------------------------------------------------------------------- *)
IF NOT bEmergencyStop THEN
    iState := STATE_FAULT;
    iFaultCode := 1001; (* E-Stop Pressed *)
END_IF;

IF bFault THEN
    bSystemReady := FALSE;
    bCycleActive := FALSE;
    rDrumExpansionServoCmd := 0.0;
    rDrumRotationServoCmd := 0.0;
    rStitcherPressureCmd := 0.0;
    sStateDescription := 'FAULT ACTIVE';
    
    IF bEnable AND bEmergencyStop THEN
        (* Reset logic *)
        bFault := FALSE;
        iFaultCode := 0;
        iState := STATE_IDLE;
    END_IF;
    RETURN;
END_IF;

(* --------------------------------------------------------------------------
   MAIN STATE MACHINE
   -------------------------------------------------------------------------- *)
CASE iState OF

    STATE_IDLE:
        sStateDescription := 'IDLE - WAITING FOR START';
        bSystemReady := TRUE;
        bCycleActive := FALSE;
        rDrumExpansionServoCmd := 0.0;
        rStitcherPressureCmd := 0.0;
        
        IF bEnable AND bStartAutoCycle THEN
            bSystemReady := FALSE;
            bCycleActive := TRUE;
            iState := STATE_INIT_EXPANSION;
            
            (* Reset PID *)
            rExpIntegral := 0.0;
            rExpLastError := 0.0;
        END_IF;

    STATE_INIT_EXPANSION:
        sStateDescription := 'EXPANDING PLY DRUM';
        
        (* PID Control for Drum Expansion Servo *)
        rExpError := rTargetPlyDrumDia - rActualPlyDrumDia;
        rExpIntegral := rExpIntegral + rExpError;
        rExpDerivative := rExpError - rExpLastError;
        
        (* Anti-windup *)
        IF rExpIntegral > 1000.0 THEN rExpIntegral := 1000.0; END_IF;
        IF rExpIntegral < -1000.0 THEN rExpIntegral := -1000.0; END_IF;
        
        rDrumExpansionServoCmd := (rKp_Exp * rExpError) + (rKi_Exp * rExpIntegral) + (rKd_Exp * rExpDerivative);
        rExpLastError := rExpError;
        
        IF ABS(rExpError) < 0.5 THEN
            tStepTimer(IN := TRUE, PT := T#500MS);
            IF tStepTimer.Q THEN
                tStepTimer(IN := FALSE);
                rDrumExpansionServoCmd := 0.0; (* Hold position *)
                iState := STATE_APPLY_INNERLINER;
            END_IF;
        ELSE
            tStepTimer(IN := FALSE);
        END_IF;
        
        (* Safety timeout *)
        IF rDrumExpansionServoCmd > 100.0 THEN rDrumExpansionServoCmd := 100.0; END_IF;
        IF rDrumExpansionServoCmd < -100.0 THEN rDrumExpansionServoCmd := -100.0; END_IF;

    STATE_APPLY_INNERLINER:
        sStateDescription := 'APPLYING INNERLINER';
        (* Turn drum slowly for innerliner application *)
        rDrumRotationServoCmd := 15.0; 
        
        (* Assume external sensor flags transition, mocked by a timer here *)
        tStepTimer(IN := TRUE, PT := T#3S);
        IF tStepTimer.Q THEN
            tStepTimer(IN := FALSE);
            rDrumRotationServoCmd := 0.0;
            iState := STATE_VISION_PROFILING;
            bVisionTrigger := TRUE;
        END_IF;

    STATE_VISION_PROFILING:
        sStateDescription := 'TREAD VISION PROFILING';
        
        IF bVisionDataReady THEN
            bVisionTrigger := FALSE;
            iState := STATE_TREAD_APPLICATION;
        END_IF;

    STATE_TREAD_APPLICATION:
        sStateDescription := 'TREAD APPLICATION';
        rDrumRotationServoCmd := 30.0; (* Higher speed for tread *)
        
        tStepTimer(IN := TRUE, PT := T#4S);
        IF tStepTimer.Q THEN
            tStepTimer(IN := FALSE);
            iState := STATE_CARCASS_STITCHING;
        END_IF;

    STATE_CARCASS_STITCHING:
        sStateDescription := 'CARCASS STITCHER DYNAMIC PRESS';
        
        (* Calculate dynamic pressure based on vision profile and drum rotation *)
        iProfileIndex := REAL_TO_INT((rDrumRotationalPos / 360.0) * 127.0);
        
        IF iProfileIndex < 0 THEN iProfileIndex := 0; END_IF;
        IF iProfileIndex > 127 THEN iProfileIndex := 127; END_IF;
        
        (* Adjust pressure modifier inversely to tread thickness to ensure uniform bonding *)
        rDynamicPressureMod := (10.0 - rTreadVisionProfile[iProfileIndex]) * 0.5;
        rStitcherPressureCmd := rStitcherBasePressure + rDynamicPressureMod;
        
        (* Pressure limits *)
        IF rStitcherPressureCmd > 8.0 THEN rStitcherPressureCmd := 8.0; END_IF;
        IF rStitcherPressureCmd < 1.0 THEN rStitcherPressureCmd := 1.0; END_IF;
        
        rDrumRotationServoCmd := 20.0;
        
        tStitchTimer(IN := TRUE, PT := T#10S); (* Stitching duration *)
        IF tStitchTimer.Q THEN
            tStitchTimer(IN := FALSE);
            rStitcherPressureCmd := 0.0; (* Retract stitcher *)
            rDrumRotationServoCmd := 0.0;
            iState := STATE_RETRACT;
        END_IF;

    STATE_RETRACT:
        sStateDescription := 'RETRACTING DRUM';
        (* Command negative expansion to release the green tire *)
        rDrumExpansionServoCmd := -50.0;
        
        IF rActualPlyDrumDia <= (rTargetPlyDrumDia * 0.8) THEN (* Retracted 20% *)
            rDrumExpansionServoCmd := 0.0;
            bCycleActive := FALSE;
            iState := STATE_IDLE;
        END_IF;

    STATE_FAULT:
        bFault := TRUE;
        bCycleActive := FALSE;
        rDrumExpansionServoCmd := 0.0;
        rDrumRotationServoCmd := 0.0;
        rStitcherPressureCmd := 0.0;

    ELSE
        iState := STATE_FAULT;
        iFaultCode := 9999; (* Invalid State *)
END_CASE;
END_FUNCTION_BLOCK"""

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": f"```iec-st\\n{st_code}\\n```"}
    ]
}

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"

with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)

os.makedirs("data", exist_ok=True)
with open("data/synthetic_generation_v3_enterprise.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\\n")
    
print(f"Success. Wrote to {filename} and data/synthetic_generation_v3_enterprise.jsonl")
