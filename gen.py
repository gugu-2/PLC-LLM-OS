import json
import uuid
import os

code = """FUNCTION_BLOCK FB_BOG_Reliquefaction_Control
TITLE = 'LNG Carrier BOG Reliquefaction Control (Brayton Cycle)'
VERSION : '2.1'
AUTHOR  : 'Lumina Elite Synthetic Data Architect'

VAR_INPUT
    bEnable : BOOL; // System Enable Command
    rBOG_Inlet_Pressure : REAL; // kPa
    rBOG_Inlet_Temp : REAL; // °C
    rColdBox_Temp : REAL; // °C
    rExpander_RPM_Actual : REAL; // RPM
    rFlashGasSeparator_Level : REAL; // %
    rCompressor_Discharge_Press : REAL; // kPa
    bESD_Active : BOOL; // Emergency Shut Down
    rNitrogen_Buffer_Pressure : REAL; // kPa
END_VAR

VAR_OUTPUT
    bSystemReady : BOOL;
    rExpander_Speed_Setpoint : REAL; // RPM
    rCompressor_IGV_Position : REAL; // Inlet Guide Vane %
    rJT_Valve_Position : REAL; // Joule-Thomson Valve %
    rSeparator_Drain_Valve : REAL; // %
    bStart_Expander : BOOL;
    bTrip_Expander : BOOL;
    iState : INT; // State machine step
    sStatusMsg : STRING[50];
END_VAR

VAR
    rExpander_RPM_Limit_Max : REAL := 45000.0;
    rExpander_RPM_Limit_Min : REAL := 15000.0;
    rTarget_ColdBox_Temp : REAL := -163.0; // °C
    PID_ColdBox : FB_PID; // Assuming standard PID FB
    PID_Level : FB_PID;
    PID_Surge : FB_PID;
    
    TON_StartDelay : TON;
    TON_TripDelay : TON;
    rTempError : REAL;
    bInterlocks_OK : BOOL;
    
    // Internal States
    STATE_OFF : INT := 0;
    STATE_PURGE : INT := 10;
    STATE_COOLDOWN : INT := 20;
    STATE_STEADY : INT := 30;
    STATE_TRIP : INT := 99;
END_VAR

(* Implementation *)
// Safety interlocks
bInterlocks_OK := NOT bESD_Active AND (rNitrogen_Buffer_Pressure > 500.0) AND (rBOG_Inlet_Pressure < 300.0);

IF NOT bInterlocks_OK THEN
    iState := STATE_TRIP;
END_IF;

CASE iState OF
    0: // STATE_OFF
        bSystemReady := bInterlocks_OK;
        bStart_Expander := FALSE;
        rExpander_Speed_Setpoint := 0.0;
        rCompressor_IGV_Position := 0.0;
        rJT_Valve_Position := 0.0;
        rSeparator_Drain_Valve := 0.0;
        sStatusMsg := 'System Off';
        
        IF bEnable AND bSystemReady THEN
            iState := STATE_PURGE;
        END_IF;

    10: // STATE_PURGE
        sStatusMsg := 'Nitrogen Purge Active';
        TON_StartDelay(IN:=TRUE, PT:=T#30s);
        IF TON_StartDelay.Q THEN
            TON_StartDelay(IN:=FALSE);
            iState := STATE_COOLDOWN;
        END_IF;

    20: // STATE_COOLDOWN
        sStatusMsg := 'Cold-Box Cooldown';
        bStart_Expander := TRUE;
        // Ramp up expander speed slowly
        IF rExpander_Speed_Setpoint < rExpander_RPM_Limit_Min THEN
            rExpander_Speed_Setpoint := rExpander_Speed_Setpoint + 50.0; // Ramp rate
        END_IF;
        
        // JT Valve for initial cooldown
        rJT_Valve_Position := 15.0; 
        
        IF (rColdBox_Temp <= -150.0) AND (rExpander_RPM_Actual >= rExpander_RPM_Limit_Min) THEN
            iState := STATE_STEADY;
        END_IF;

    30: // STATE_STEADY
        sStatusMsg := 'Steady State Reliquefaction';
        
        // Cold-box temperature control via Expander Speed
        rTempError := rTarget_ColdBox_Temp - rColdBox_Temp;
        PID_ColdBox(
            EN := TRUE,
            SP := rTarget_ColdBox_Temp,
            PV := rColdBox_Temp,
            KP := 2.5,
            TI := 10.0,
            TD := 1.0,
            OUT => rExpander_Speed_Setpoint
        );
        
        // Clamp Expander Speed
        IF rExpander_Speed_Setpoint > rExpander_RPM_Limit_Max THEN
            rExpander_Speed_Setpoint := rExpander_RPM_Limit_Max;
        ELSIF rExpander_Speed_Setpoint < rExpander_RPM_Limit_Min THEN
            rExpander_Speed_Setpoint := rExpander_RPM_Limit_Min;
        END_IF;
        
        // Flash Gas Separator Level Control
        PID_Level(
            EN := TRUE,
            SP := 50.0, // 50% target level
            PV := rFlashGasSeparator_Level,
            KP := 1.5,
            TI := 5.0,
            OUT => rSeparator_Drain_Valve
        );
        
        // Anti-surge control for comp stage
        IF rCompressor_Discharge_Press > 2500.0 THEN
            rCompressor_IGV_Position := rCompressor_IGV_Position - 1.0;
        ELSE
            rCompressor_IGV_Position := 100.0; // Fully open normally
        END_IF;
        
    99: // STATE_TRIP
        sStatusMsg := 'SYSTEM TRIPPED';
        bTrip_Expander := TRUE;
        bStart_Expander := FALSE;
        rExpander_Speed_Setpoint := 0.0;
        rJT_Valve_Position := 0.0;
        rSeparator_Drain_Valve := 100.0; // Dump liquid
        
        IF NOT bESD_Active AND NOT bEnable THEN
            bTrip_Expander := FALSE;
            iState := STATE_OFF;
        END_IF;
        
    ELSE
        iState := STATE_OFF;
END_CASE;

END_FUNCTION_BLOCK
"""

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: LNG Carrier Boil-Off Gas (BOG) Reliquefaction.
Task: Invent a highly complex control scenario for this domain (e.g., Brayton cycle cryogenic expander RPM limits, flash gas separator liquid levels, and cold-box thermal integration).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."""

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": f"```iec-st\n{code}\n```"}
    ]
}

os.makedirs("data/swarm_raw", exist_ok=True)
os.makedirs("data", exist_ok=True)
with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
    json.dump(record, f)

with open("data/synthetic_generation_v3_enterprise.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\n")
