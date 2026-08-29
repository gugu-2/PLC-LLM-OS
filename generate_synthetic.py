import json
import uuid
import os

# Create swarm directory
os.makedirs("data/swarm_raw", exist_ok=True)
os.makedirs("data", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Fully Automated Electroplating Line.
Task: Invent a highly complex control scenario for this domain (e.g., anodic oxidation current density profiling, hoist crane drag-out delay timing, and scrubber pH neutralization).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."""

code = """```iec-st
FUNCTION_BLOCK FB_ElectroplatingLineCtrl
VAR_INPUT
    bEnableLine : BOOL; // Main system enable
    rHoistPositionX : REAL; // Crane horizontal position [mm]
    rHoistPositionY : REAL; // Crane vertical position [mm]
    bTank1_Ready : BOOL; // Cleaning tank ready
    bTank2_Ready : BOOL; // Anodizing tank ready
    rCurrentDensityFbk : REAL; // Feedback from rectifier [A/dm2]
    rScrubber_pH : REAL; // Scrubber tank pH level
    rPartSurfaceArea : REAL; // Calculated surface area of the batch [dm2]
END_VAR
VAR_OUTPUT
    bHoistMoveFwd : BOOL;
    bHoistMoveRev : BOOL;
    bHoistMoveUp : BOOL;
    bHoistMoveDown : BOOL;
    rRectifierSetpt : REAL; // Current setpoint to rectifier [A]
    bRectifierEnable : BOOL;
    rAcidDosingPump_Cmd : REAL; // Pump speed 0-100%
    rBaseDosingPump_Cmd : REAL; // Pump speed 0-100%
    iActiveState : INT; // Diagnostics
END_VAR
VAR
    // State Machine
    eHoistState : INT := 0; // 0=IDLE, 1=PICK_UP, 2=MOVE_CLEAN, 3=CLEANING, 4=MOVE_ANODIZE, 5=ANODIZING, 6=DRAG_OUT, 7=MOVE_DROP, 8=DROP_OFF, 9=RETURN_HOME
    
    // Timers
    tonCleanDelay : TON;
    tonAnodizeDelay : TON;
    tonDragOut : TON;
    
    // Profiling
    rRampRate : REAL := 0.5; // A/sec
    rTargetDensity : REAL := 1.5; // A/dm2
    rCurrentSetpt_Internal : REAL;
    
    // Scrubber PI Control
    rError_pH : REAL;
    rTarget_pH : REAL := 7.5;
    rPropBand : REAL := 2.0;
    rIntegral : REAL := 0.0;
    rKi : REAL := 0.1;
    
    // Constants
    POS_HOME_X : REAL := 0.0;
    POS_CLEAN_X : REAL := 2000.0;
    POS_ANODIZE_X : REAL := 5000.0;
    POS_DROP_X : REAL := 8000.0;
    POS_UP_Y : REAL := 3000.0;
    POS_DOWN_Y : REAL := 500.0;
    POS_TOLERANCE : REAL := 5.0;
END_VAR

// Scrubber pH Neutralization Control (Continuous Process)
rError_pH := rScrubber_pH - rTarget_pH;
rIntegral := rIntegral + (rError_pH * rKi);

IF rIntegral > 100.0 THEN rIntegral := 100.0; END_IF;
IF rIntegral < -100.0 THEN rIntegral := -100.0; END_IF;

IF rError_pH > 0.5 THEN
    rAcidDosingPump_Cmd := (rError_pH * rPropBand) + rIntegral;
    rBaseDosingPump_Cmd := 0.0;
ELSIF rError_pH < -0.5 THEN
    rBaseDosingPump_Cmd := (ABS(rError_pH) * rPropBand) + ABS(rIntegral);
    rAcidDosingPump_Cmd := 0.0;
ELSE
    rAcidDosingPump_Cmd := 0.0;
    rBaseDosingPump_Cmd := 0.0;
END_IF;

// Limit outputs
IF rAcidDosingPump_Cmd > 100.0 THEN rAcidDosingPump_Cmd := 100.0; END_IF;
IF rBaseDosingPump_Cmd > 100.0 THEN rBaseDosingPump_Cmd := 100.0; END_IF;

// Main Hoist and Process State Machine
IF NOT bEnableLine THEN
    eHoistState := 0;
    bHoistMoveFwd := FALSE; bHoistMoveRev := FALSE;
    bHoistMoveUp := FALSE; bHoistMoveDown := FALSE;
    bRectifierEnable := FALSE;
    rRectifierSetpt := 0.0;
ELSE
    CASE eHoistState OF
        0: // IDLE
            IF ABS(rHoistPositionX - POS_HOME_X) < POS_TOLERANCE AND ABS(rHoistPositionY - POS_UP_Y) < POS_TOLERANCE THEN
                eHoistState := 1;
            END_IF;
            
        1: // PICK_UP
            bHoistMoveDown := TRUE; bHoistMoveUp := FALSE;
            IF ABS(rHoistPositionY - POS_DOWN_Y) < POS_TOLERANCE THEN
                bHoistMoveDown := FALSE;
                eHoistState := 2;
            END_IF;
            
        2: // MOVE_CLEAN
            bHoistMoveUp := TRUE;
            IF ABS(rHoistPositionY - POS_UP_Y) < POS_TOLERANCE THEN
                bHoistMoveUp := FALSE;
                bHoistMoveFwd := TRUE;
                IF ABS(rHoistPositionX - POS_CLEAN_X) < POS_TOLERANCE THEN
                    bHoistMoveFwd := FALSE;
                    bHoistMoveDown := TRUE;
                    IF ABS(rHoistPositionY - POS_DOWN_Y) < POS_TOLERANCE THEN
                        bHoistMoveDown := FALSE;
                        eHoistState := 3;
                    END_IF;
                END_IF;
            END_IF;
            
        3: // CLEANING
            tonCleanDelay(IN:= TRUE, PT:= T#120S);
            IF tonCleanDelay.Q THEN
                tonCleanDelay(IN:= FALSE);
                eHoistState := 4;
            END_IF;
            
        4: // MOVE_ANODIZE
            bHoistMoveUp := TRUE;
            IF ABS(rHoistPositionY - POS_UP_Y) < POS_TOLERANCE THEN
                bHoistMoveUp := FALSE;
                bHoistMoveFwd := TRUE;
                IF ABS(rHoistPositionX - POS_ANODIZE_X) < POS_TOLERANCE THEN
                    bHoistMoveFwd := FALSE;
                    bHoistMoveDown := TRUE;
                    IF ABS(rHoistPositionY - POS_DOWN_Y) < POS_TOLERANCE THEN
                        bHoistMoveDown := FALSE;
                        eHoistState := 5;
                    END_IF;
                END_IF;
            END_IF;
            
        5: // ANODIZING
            bRectifierEnable := TRUE;
            // Anodic oxidation current density profiling
            rCurrentSetpt_Internal := rCurrentSetpt_Internal + rRampRate;
            IF rCurrentSetpt_Internal > (rTargetDensity * rPartSurfaceArea) THEN
                rCurrentSetpt_Internal := rTargetDensity * rPartSurfaceArea;
            END_IF;
            rRectifierSetpt := rCurrentSetpt_Internal;
            
            tonAnodizeDelay(IN:= TRUE, PT:= T#600S);
            IF tonAnodizeDelay.Q THEN
                tonAnodizeDelay(IN:= FALSE);
                bRectifierEnable := FALSE;
                rRectifierSetpt := 0.0;
                rCurrentSetpt_Internal := 0.0;
                eHoistState := 6;
            END_IF;
            
        6: // DRAG_OUT_DELAY
            // Lift slightly above tank and hold for drag-out
            bHoistMoveUp := TRUE;
            IF ABS(rHoistPositionY - (POS_DOWN_Y + 500.0)) < POS_TOLERANCE THEN
                bHoistMoveUp := FALSE;
                tonDragOut(IN:= TRUE, PT:= T#15S); // Delay for dripping
                IF tonDragOut.Q THEN
                    tonDragOut(IN:= FALSE);
                    eHoistState := 7;
                END_IF;
            END_IF;
            
        7: // MOVE_DROP
            bHoistMoveUp := TRUE;
            IF ABS(rHoistPositionY - POS_UP_Y) < POS_TOLERANCE THEN
                bHoistMoveUp := FALSE;
                bHoistMoveFwd := TRUE;
                IF ABS(rHoistPositionX - POS_DROP_X) < POS_TOLERANCE THEN
                    bHoistMoveFwd := FALSE;
                    bHoistMoveDown := TRUE;
                    IF ABS(rHoistPositionY - POS_DOWN_Y) < POS_TOLERANCE THEN
                        bHoistMoveDown := FALSE;
                        eHoistState := 8;
                    END_IF;
                END_IF;
            END_IF;
            
        8: // DROP_OFF
            // Logic to release part would go here
            eHoistState := 9;
            
        9: // RETURN_HOME
            bHoistMoveUp := TRUE;
            IF ABS(rHoistPositionY - POS_UP_Y) < POS_TOLERANCE THEN
                bHoistMoveUp := FALSE;
                bHoistMoveRev := TRUE;
                IF ABS(rHoistPositionX - POS_HOME_X) < POS_TOLERANCE THEN
                    bHoistMoveRev := FALSE;
                    eHoistState := 0;
                END_IF;
            END_IF;
    END_CASE;
END_IF;
iActiveState := eHoistState;
END_FUNCTION_BLOCK
```"""

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": code}
    ]
}

# Write to unique swarm_raw file
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)

# Write to synthetic_generation_v3_enterprise.jsonl
with open("data/synthetic_generation_v3_enterprise.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\\n")

print(f"Generated and written successfully to {filename} and data/synthetic_generation_v3_enterprise.jsonl")
