import json
import uuid
import os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Commercial Spaceport Launch Pad.
Task: Invent a highly complex control scenario for this domain (e.g., liquid oxygen/methane fueling umbilicals, acoustic suppression water deluge, and strongback erector retraction).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."""

code = """```iec-st
FUNCTION_BLOCK FB_LaunchPadSequencer
VAR_INPUT
    bStartSequence : BOOL;
    bEmergencyStop : BOOL;
    bManualOverride : BOOL;
    rLoxTankLevel : REAL; (* percentage 0.0 - 100.0 *)
    rMethaneTankLevel : REAL; (* percentage 0.0 - 100.0 *)
    rLoxLinePressure : REAL; (* bar *)
    rMethaneLinePressure : REAL; (* bar *)
    rDelugeWaterPressure : REAL; (* bar *)
    bStrongbackFullyRetracted : BOOL;
    bUmbilicalDisconnected : BOOL;
    bIgniterHealthy : BOOL;
    tCountDownStart : TIME := T#15M;
END_VAR
VAR_OUTPUT
    bLoxValveOpen : BOOL;
    bMethaneValveOpen : BOOL;
    bLoxPurgeValve : BOOL;
    bMethanePurgeValve : BOOL;
    bDelugeValveOpen : BOOL;
    bRetractStrongback : BOOL;
    bReleaseUmbilical : BOOL;
    bIgnitionSequenceStart : BOOL;
    iCurrentState : INT;
    rTimeRemaining : TIME;
    sStatusMsg : STRING(80);
    bFault : BOOL;
    bGoForLaunch : BOOL;
END_VAR
VAR
    State : INT := 0;
    StepTimer : TON;
    HoldTimer : TON;
    bTanksFull : BOOL;
    bWaterReady : BOOL;
    bUmbilicalClear : BOOL;
    bStrongbackClear : BOOL;
    bSystemsGo : BOOL;
    rFlowRateLox : REAL;
    rFlowRateMethane : REAL;
END_VAR

(* 
    Commercial Spaceport Launch Pad Control System
    Domain: Launch Pad Ground Support Equipment (GSE)
    Handles LOX/Methane fueling operations, umbilical disconnect, 
    water deluge acoustic suppression, and strongback erector retraction.
*)

(* Global Emergency Stop Check *)
IF bEmergencyStop THEN
    State := 999;
END_IF;

CASE State OF
    0: (* System Idle - Waiting for countdown sequence initiation *)
        bLoxValveOpen := FALSE;
        bMethaneValveOpen := FALSE;
        bLoxPurgeValve := TRUE;
        bMethanePurgeValve := TRUE;
        bDelugeValveOpen := FALSE;
        bRetractStrongback := FALSE;
        bReleaseUmbilical := FALSE;
        bIgnitionSequenceStart := FALSE;
        bGoForLaunch := FALSE;
        sStatusMsg := 'IDLE: Awaiting Sequence Start and Range Clear';
        bFault := FALSE;
        IF bStartSequence AND NOT bEmergencyStop THEN
            State := 10;
        END_IF;
        
    10: (* Purge Phase - Clear lines with inert gas *)
        sStatusMsg := 'PURGE: Purging propellant lines with GN2';
        StepTimer(IN:=TRUE, PT:=T#30S);
        IF StepTimer.Q THEN
            bLoxPurgeValve := FALSE;
            bMethanePurgeValve := FALSE;
            StepTimer(IN:=FALSE);
            State := 20;
        END_IF;

    20: (* Fueling Phase - Cryogenic Loading *)
        sStatusMsg := 'FUELING: Chilldown and Loading of LOX / CH4';
        
        (* LOX Loading Logic *)
        IF rLoxTankLevel < 99.8 AND rLoxLinePressure > 5.0 THEN
            bLoxValveOpen := TRUE;
        ELSE
            bLoxValveOpen := FALSE;
        END_IF;
        
        (* Methane Loading Logic *)
        IF rMethaneTankLevel < 99.8 AND rMethaneLinePressure > 5.0 THEN
            bMethaneValveOpen := TRUE;
        ELSE
            bMethaneValveOpen := FALSE;
        END_IF;
        
        IF (rLoxTankLevel >= 99.8) AND (rMethaneTankLevel >= 99.8) THEN
            bTanksFull := TRUE;
            State := 30;
        END_IF;
        
    30: (* Water Deluge Prep & Terminal Count Start *)
        sStatusMsg := 'DELUGE PREP: Verifying Acoustic Suppression Water Pressure';
        IF rDelugeWaterPressure > 12.5 THEN
            bWaterReady := TRUE;
            State := 40;
        ELSE
            bWaterReady := FALSE;
            HoldTimer(IN:=TRUE, PT:=T#60S);
            IF HoldTimer.Q THEN
                State := 900; (* Fault: Deluge Pressure too low *)
            END_IF;
        END_IF;
        
    40: (* Umbilical Disconnect T-2 minutes *)
        sStatusMsg := 'UMBILICAL: Command Release Quick-Disconnects';
        bReleaseUmbilical := TRUE;
        StepTimer(IN:=TRUE, PT:=T#5S);
        IF bUmbilicalDisconnected AND StepTimer.Q THEN
            bUmbilicalClear := TRUE;
            StepTimer(IN:=FALSE);
            State := 50;
        ELSIF StepTimer.Q THEN
            State := 901; (* Fault: Umbilical failed to disconnect *)
        END_IF;
        
    50: (* Strongback Retraction T-1 minute *)
        sStatusMsg := 'STRONGBACK: Hydraulic Retraction in Progress';
        bRetractStrongback := TRUE;
        IF bStrongbackFullyRetracted THEN
            bStrongbackClear := TRUE;
            State := 60;
        END_IF;
        
    60: (* Final Health Check T-15 seconds *)
        sStatusMsg := 'HEALTH CHECK: Final Avionics and Igniter Verification';
        IF bIgniterHealthy AND bUmbilicalClear AND bStrongbackClear THEN
            bSystemsGo := TRUE;
            State := 70;
        ELSE
            State := 902; (* Fault: Systems not ready for terminal *)
        END_IF;

    70: (* Deluge Activation T-10 seconds *)
        sStatusMsg := 'DELUGE: Acoustic Suppression Activated';
        bDelugeValveOpen := TRUE;
        StepTimer(IN:=TRUE, PT:=T#5S);
        IF StepTimer.Q THEN
            StepTimer(IN:=FALSE);
            State := 80;
        END_IF;
        
    80: (* Ignition Enable T-0 *)
        sStatusMsg := 'IGNITION: Command Engine Start Sequence';
        bIgnitionSequenceStart := TRUE;
        bGoForLaunch := TRUE;
        
    900: (* Fault States *)
        sStatusMsg := 'FAULT: Water Deluge Pressure Out of Bounds';
        bFault := TRUE;
        bLoxValveOpen := FALSE;
        bMethaneValveOpen := FALSE;
    
    901:
        sStatusMsg := 'FAULT: Umbilical Retract Failure';
        bFault := TRUE;
        bLoxValveOpen := FALSE;
        bMethaneValveOpen := FALSE;

    902:
        sStatusMsg := 'FAULT: Pre-Ignition Checks Failed';
        bFault := TRUE;
        bLoxValveOpen := FALSE;
        bMethaneValveOpen := FALSE;

    999: (* Emergency Abort Sequence *)
        sStatusMsg := 'ABORT: Emergency Stop Triggered - Safing Vehicle';
        bLoxValveOpen := FALSE;
        bMethaneValveOpen := FALSE;
        bLoxPurgeValve := TRUE;
        bMethanePurgeValve := TRUE;
        bDelugeValveOpen := TRUE; (* Keep deluge on for safety in case of fire *)
        bRetractStrongback := FALSE;
        bReleaseUmbilical := FALSE;
        bIgnitionSequenceStart := FALSE;
        bGoForLaunch := FALSE;
        bFault := TRUE;
        
    ELSE
        State := 0;
END_CASE;

iCurrentState := State;
```"""

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": code}
    ]
}
os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)

print(f"Generated {filename}")
