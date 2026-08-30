import json
import uuid
import os

os.makedirs('data/swarm_raw', exist_ok=True)

prompt = "You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.\nYour specific domain is: Automotive Robotic Spot Welding Cell.\nTask: Invent a highly complex control scenario for this domain (e.g., servo weld-gun tip dressing, welding transformer current ramping, and fixture pneumatic clamp staging)."

st_code = """FUNCTION_BLOCK FB_RoboticSpotWeldingCell
TITLE = 'Automotive Robotic Spot Welding Cell Control'
// This function block manages the intricate sequencing of an automotive robotic spot weld cell.
// Includes servo gun tip dressing, transformer current ramping, and fixture pneumatic staging.

VAR_INPUT
    bEnableSystem : BOOL;            // Master Enable
    bSafetyOk : BOOL;                // Safety Gate and E-Stops OK
    bPartPresent : BOOL;             // Photoeye detects part in fixture
    bCycleStart : BOOL;              // Operator initiates cycle
    bWaterFlowOk : BOOL;             // Chilled water for weld gun
    bAirPressureOk : BOOL;           // Main pneumatic pressure
    bRobotInClear : BOOL;            // Robot is at home/clear position
    rActualWeldCurrent : REAL;       // Feedback from weld controller
    nTipDressCount : INT;            // Number of welds since last dress
END_VAR

VAR_OUTPUT
    bFixtureClamp1 : BOOL;           // Actuate Clamp 1
    bFixtureClamp2 : BOOL;           // Actuate Clamp 2
    bRobotStart : BOOL;              // Signal robot to begin weld path
    bWeldTrigger : BOOL;             // Trigger weld controller
    rWeldCommandCurrent : REAL;      // Analog command to weld controller
    bTipDresserRun : BOOL;           // Start tip dresser motor
    bCellFault : BOOL;               // Fault indicator
    nCellStateCode : INT;            // Current state for HMI
END_VAR

VAR
    nState : INT := 0;               // Main State Machine
    nFaultCode : INT := 0;
    tonClampDelay : TON;             // Timer for clamp actuation
    tonWeldSqueeze : TON;            // Squeeze time before weld
    tonWeldHold : TON;               // Hold time after weld
    tonTipDress : TON;               // Tip dressing duration
    rRampIncrement : REAL;           // Calculated ramp step
    nRampStep : INT;
    bRampingDone : BOOL;
    bCycleComplete : BOOL;
END_VAR

// Constants
VAR CONSTANT
    STATE_IDLE : INT := 0;
    STATE_STAGING : INT := 10;
    STATE_CLAMPING : INT := 20;
    STATE_ROBOT_APPROACH : INT := 30;
    STATE_WELD_RAMPING : INT := 40;
    STATE_WELD_HOLD : INT := 50;
    STATE_UNCLAMPING : INT := 60;
    STATE_TIP_DRESS : INT := 70;
    STATE_FAULT : INT := 999;
    
    MAX_WELD_CURRENT : REAL := 12500.0; // Amps
    RAMP_STEPS : INT := 10;
    TIP_DRESS_LIMIT : INT := 50;
END_VAR

// Logic
IF NOT bEnableSystem OR NOT bSafetyOk OR NOT bWaterFlowOk OR NOT bAirPressureOk THEN
    nState := STATE_FAULT;
    nFaultCode := 1; // General interlock fault
END_IF;

CASE nState OF
    STATE_IDLE:
        bFixtureClamp1 := FALSE;
        bFixtureClamp2 := FALSE;
        bRobotStart := FALSE;
        bWeldTrigger := FALSE;
        rWeldCommandCurrent := 0.0;
        bTipDresserRun := FALSE;
        bCellFault := FALSE;
        nCellStateCode := 0;
        bCycleComplete := FALSE;
        
        IF bCycleStart AND bPartPresent AND bRobotInClear THEN
            nState := STATE_STAGING;
        ELSIF nTipDressCount >= TIP_DRESS_LIMIT AND bRobotInClear THEN
            nState := STATE_TIP_DRESS;
        END_IF;

    STATE_STAGING:
        nCellStateCode := 10;
        // Engage staging pins or pre-clamps
        bFixtureClamp1 := TRUE;
        tonClampDelay(IN := TRUE, PT := T#500MS);
        IF tonClampDelay.Q THEN
            tonClampDelay(IN := FALSE);
            nState := STATE_CLAMPING;
        END_IF;

    STATE_CLAMPING:
        nCellStateCode := 20;
        bFixtureClamp2 := TRUE;
        tonClampDelay(IN := TRUE, PT := T#500MS);
        IF tonClampDelay.Q THEN
            tonClampDelay(IN := FALSE);
            bRobotStart := TRUE;
            nState := STATE_ROBOT_APPROACH;
        END_IF;

    STATE_ROBOT_APPROACH:
        nCellStateCode := 30;
        // Wait for robot to squeeze gun (simulated by external input or timer)
        tonWeldSqueeze(IN := TRUE, PT := T#2S);
        IF tonWeldSqueeze.Q THEN
            tonWeldSqueeze(IN := FALSE);
            nRampStep := 0;
            bRampingDone := FALSE;
            bWeldTrigger := TRUE;
            nState := STATE_WELD_RAMPING;
        END_IF;

    STATE_WELD_RAMPING:
        nCellStateCode := 40;
        // Ramp up current to prolong tip life and improve nugget formation
        IF NOT bRampingDone THEN
            rRampIncrement := MAX_WELD_CURRENT / INT_TO_REAL(RAMP_STEPS);
            rWeldCommandCurrent := rRampIncrement * INT_TO_REAL(nRampStep);
            nRampStep := nRampStep + 1;
            IF nRampStep > RAMP_STEPS THEN
                bRampingDone := TRUE;
                rWeldCommandCurrent := MAX_WELD_CURRENT;
            END_IF;
        ELSE
            // Hold at max current
            tonWeldHold(IN := TRUE, PT := T#300MS);
            IF tonWeldHold.Q THEN
                tonWeldHold(IN := FALSE);
                bWeldTrigger := FALSE;
                rWeldCommandCurrent := 0.0;
                nState := STATE_UNCLAMPING;
            END_IF;
        END_IF;

    STATE_UNCLAMPING:
        nCellStateCode := 60;
        bRobotStart := FALSE;
        bFixtureClamp1 := FALSE;
        bFixtureClamp2 := FALSE;
        tonClampDelay(IN := TRUE, PT := T#1S);
        IF tonClampDelay.Q THEN
            tonClampDelay(IN := FALSE);
            bCycleComplete := TRUE;
            nState := STATE_IDLE;
        END_IF;
        
    STATE_TIP_DRESS:
        nCellStateCode := 70;
        bTipDresserRun := TRUE;
        tonTipDress(IN := TRUE, PT := T#5S);
        IF tonTipDress.Q THEN
            tonTipDress(IN := FALSE);
            bTipDresserRun := FALSE;
            nState := STATE_IDLE;
        END_IF;

    STATE_FAULT:
        bCellFault := TRUE;
        bFixtureClamp1 := FALSE;
        bFixtureClamp2 := FALSE;
        bRobotStart := FALSE;
        bWeldTrigger := FALSE;
        rWeldCommandCurrent := 0.0;
        bTipDresserRun := FALSE;
        nCellStateCode := 999;
        // Reset logic would go here
        IF bEnableSystem AND bSafetyOk THEN
            nState := STATE_IDLE;
        END_IF;
        
END_CASE;
END_FUNCTION_BLOCK
"""

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": f"```iec-st\n{st_code}\n```"}
    ]
}

file_name = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(file_name, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=4)
print(f"File successfully saved to {file_name}")
