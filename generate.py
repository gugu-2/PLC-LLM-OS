import json, uuid
import os

code = """```iec-st
FUNCTION_BLOCK FB_RO_DesalinationControl
VAR_INPUT
    bStartSequence : BOOL;
    bEmergencyStop : BOOL;
    rFeedPressure : REAL; (* Bar *)
    rPermeateFlow : REAL; (* m3/h *)
    rConcentrateFlow : REAL; (* m3/h *)
    rFeedConductivity : REAL; (* uS/cm *)
    rMembraneDiffPressure : REAL; (* Bar *)
    rAntiScalantTankLevel : REAL; (* % *)
END_VAR
VAR_OUTPUT
    bHighPressurePumpCmd : BOOL;
    bERDBoosterPumpCmd : BOOL;
    rAntiScalantDosingRate : REAL; (* L/h *)
    rRejectControlValvePos : REAL; (* 0-100% *)
    bSystemReady : BOOL;
    bAlarmActive : BOOL;
    iStateSequence : INT;
END_VAR
VAR
    TON_StartupDelay : TON;
    TON_RampUp : TON;
    rTargetPressure : REAL := 65.0; (* Bar *)
    rCurrentDosingSetpoint : REAL := 0.0;
    bMembraneFoulingWarning : BOOL := FALSE;
    bStartupComplete : BOOL := FALSE;
    rRecoveryRate : REAL := 0.0;
END_VAR

(* Control Logic for RO Desalination Plant *)

IF bEmergencyStop THEN
    bHighPressurePumpCmd := FALSE;
    bERDBoosterPumpCmd := FALSE;
    rAntiScalantDosingRate := 0.0;
    rRejectControlValvePos := 100.0; (* Fully open for safe shutdown *)
    iStateSequence := 0;
    bAlarmActive := TRUE;
    bSystemReady := FALSE;
    RETURN;
END_IF;

(* Calculate Recovery Rate *)
IF (rPermeateFlow + rConcentrateFlow) > 0.0 THEN
    rRecoveryRate := (rPermeateFlow / (rPermeateFlow + rConcentrateFlow)) * 100.0;
END_IF;

(* Membrane Fouling Detection *)
IF rMembraneDiffPressure > 2.5 THEN
    bMembraneFoulingWarning := TRUE;
ELSE
    bMembraneFoulingWarning := FALSE;
END_IF;

(* Anti-scalant Dosing Control - Flow Proportional *)
IF bHighPressurePumpCmd AND rFeedPressure > 10.0 THEN
    (* Base dosing rate on feed flow and setpoint *)
    rCurrentDosingSetpoint := (rPermeateFlow + rConcentrateFlow) * 0.02; (* 20 ppm *)
    IF rAntiScalantTankLevel < 10.0 THEN
        bAlarmActive := TRUE; (* Low level alarm *)
        rAntiScalantDosingRate := rCurrentDosingSetpoint;
    ELSE
        rAntiScalantDosingRate := rCurrentDosingSetpoint;
    END_IF;
ELSE
    rAntiScalantDosingRate := 0.0;
END_IF;

(* Sequence Control *)
CASE iStateSequence OF
    0: (* Standby *)
        bSystemReady := TRUE;
        bHighPressurePumpCmd := FALSE;
        bERDBoosterPumpCmd := FALSE;
        rRejectControlValvePos := 100.0; 
        IF bStartSequence AND NOT bAlarmActive THEN
            iStateSequence := 10;
            bSystemReady := FALSE;
        END_IF;
        
    10: (* Pre-checks and ERD Booster Start *)
        bERDBoosterPumpCmd := TRUE;
        TON_StartupDelay(IN:=TRUE, PT:=T#5S);
        IF TON_StartupDelay.Q THEN
            TON_StartupDelay(IN:=FALSE);
            iStateSequence := 20;
        END_IF;
        
    20: (* High Pressure Pump Ramp Up *)
        bHighPressurePumpCmd := TRUE;
        TON_RampUp(IN:=TRUE, PT:=T#30S);
        
        (* Gradually close reject valve to build pressure *)
        IF rRejectControlValvePos > 40.0 THEN
            rRejectControlValvePos := rRejectControlValvePos - 0.1;
        END_IF;
        
        IF rFeedPressure >= rTargetPressure OR TON_RampUp.Q THEN
            iStateSequence := 30;
            TON_RampUp(IN:=FALSE);
        END_IF;
        
    30: (* Steady State Operation *)
        bStartupComplete := TRUE;
        
        (* Pressure Control via Reject Valve *)
        IF rFeedPressure < rTargetPressure - 1.0 THEN
            rRejectControlValvePos := rRejectControlValvePos - 0.05;
        ELSIF rFeedPressure > rTargetPressure + 1.0 THEN
            rRejectControlValvePos := rRejectControlValvePos + 0.05;
        END_IF;
        
        (* Limit valve position *)
        IF rRejectControlValvePos > 100.0 THEN rRejectControlValvePos := 100.0; END_IF;
        IF rRejectControlValvePos < 10.0 THEN rRejectControlValvePos := 10.0; END_IF;
        
        IF NOT bStartSequence THEN
            iStateSequence := 40; (* Shutdown sequence *)
        END_IF;
        
    40: (* Normal Shutdown *)
        bHighPressurePumpCmd := FALSE;
        bStartupComplete := FALSE;
        rRejectControlValvePos := 100.0; (* Open reject valve *)
        TON_StartupDelay(IN:=TRUE, PT:=T#10S);
        IF TON_StartupDelay.Q THEN
            bERDBoosterPumpCmd := FALSE;
            TON_StartupDelay(IN:=FALSE);
            iStateSequence := 0;
        END_IF;
END_CASE;

END_FUNCTION_BLOCK
```"""

prompt = "Invent a highly complex control scenario for a Reverse Osmosis (RO) Desalination Plant (e.g., high-pressure pump Energy Recovery Device (ERD) sequencing, membrane differential pressure tracking, and anti-scalant dosing). Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}

os.makedirs("data", exist_ok=True)
jsonl_file = "data/synthetic_generation_v3_enterprise.jsonl"
with open(jsonl_file, "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\\n")
print(f"Appended to {jsonl_file}")
