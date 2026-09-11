import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Air Cargo Elevating Transfer Vehicle (ETV).
Task: Invent a highly complex control scenario for this domain (e.g., ULD (Unit Load Device) friction drive nesting, scissor lift hydraulic leveling, and dynamic rack sway compensation).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O.

CRITICAL RULES:
1. You MUST output the code enclosed in a ```iec-st markdown code fence. DO NOT APOLOGIZE. DO NOT EXPLAIN.
2. The code must be >= 1500 chars, with FUNCTION_BLOCK and VAR_INPUT/VAR_OUTPUT.
3. You MUST save your JSON payload to a uniquely named file in the swarm directory using python."""

st_code = """```iec-st
FUNCTION_BLOCK FB_ETV_Complex_Control
VAR_INPUT
    bSystemEnable : BOOL; (* Main power and safety loop OK *)
    bAutoMode : BOOL; (* Automatic operation active *)
    
    rTargetPosition_X : REAL; (* Target rack aisle position [m] *)
    rTargetPosition_Y : REAL; (* Target lift height position [m] *)
    rTargetPosition_Z : REAL; (* Target friction drive extension [m] *)
    
    rCurrentPosition_X : REAL; (* Current X position feedback [m] *)
    rCurrentPosition_Y : REAL; (* Current Y position feedback [m] *)
    rCurrentPosition_Z : REAL; (* Current Z position feedback [m] *)
    
    rRackSwaySensor_Front : REAL; (* Front laser distance to rack [mm] *)
    rRackSwaySensor_Rear : REAL; (* Rear laser distance to rack [mm] *)
    
    rHydraulicPressure_Left : REAL; (* Left scissor cylinder pressure [bar] *)
    rHydraulicPressure_Right : REAL; (* Right scissor cylinder pressure [bar] *)
    
    bUldPresent : BOOL; (* ULD detected on the ETV platform *)
    bUldSeated : BOOL; (* ULD seated properly in the storage rack *)
    
    rFrictionDriveTorqueFB : REAL; (* Feedback torque from friction drive [Nm] *)
END_VAR

VAR_OUTPUT
    bInPosition : BOOL; (* ETV has reached target and is stable *)
    bFault : BOOL; (* Fault condition active *)
    iFaultCode : INT; (* Specific fault diagnostic code *)
    
    rDriveCommand_X : REAL; (* Commanded speed to X travel drive [%] *)
    rLiftValveCommand_Left : REAL; (* Commanded opening left prop valve [%] *)
    rLiftValveCommand_Right : REAL; (* Commanded opening right prop valve [%] *)
    rFrictionDriveCommand_Z : REAL; (* Commanded speed to Z friction drive [%] *)
    bFrictionDriveEnable : BOOL; (* Enable signal to Z drive inverter *)
END_VAR

VAR
    (* Internal State Machine *)
    eState : INT := 0; (* 0: Idle, 10: Move X/Y, 20: Sway Comp, 30: Extend Z, 40: Retract Z, 99: Error *)
    
    (* Sway Compensation Controller *)
    rSwayError : REAL;
    rSwayKp : REAL := 1.75;
    rSwayKd : REAL := 0.85;
    rSwayDerivative : REAL;
    rLastSwayError : REAL;
    
    (* Hydraulic Leveling Controller *)
    rLevelError : REAL;
    rLevelKp : REAL := 2.50;
    rPressureDifferential : REAL;
    rPressureCompGain : REAL := 0.15;
    rHydraulicOffset : REAL;
    
    (* Friction Drive Nesting Control *)
    rTorqueLimit : REAL := 125.0; (* Max allowable torque for nesting [Nm] *)
    bTorqueLimitReached : BOOL;
    
    (* Timers *)
    tSwaySettle : TON;
    tDriveTimeout : TON;
END_VAR

(* -----------------------------------------------------------------------------
   Main Control Logic
   ----------------------------------------------------------------------------- *)
IF NOT bSystemEnable OR NOT bAutoMode THEN
    eState := 0;
    bInPosition := FALSE;
    bFault := FALSE;
    rDriveCommand_X := 0.0;
    rLiftValveCommand_Left := 0.0;
    rLiftValveCommand_Right := 0.0;
    rFrictionDriveCommand_Z := 0.0;
    bFrictionDriveEnable := FALSE;
    RETURN;
END_IF;

(* 1. Hydraulic Scissor Lift Leveling Control (Continuous) *)
(* Ensures the platform remains perfectly level despite asymmetric ULD loads *)
rLevelError := rTargetPosition_Y - rCurrentPosition_Y;
rPressureDifferential := rHydraulicPressure_Left - rHydraulicPressure_Right;

(* Calculate asymmetric compensation based on pressure diff *)
rHydraulicOffset := rPressureDifferential * rPressureCompGain;

(* Apply base lift command plus differential leveling *)
rLiftValveCommand_Left := (rLevelError * rLevelKp) - rHydraulicOffset;
rLiftValveCommand_Right := (rLevelError * rLevelKp) + rHydraulicOffset;

(* 2. Dynamic Rack Sway Compensation *)
(* Uses dual laser sensors to detect rack sway and adjust X position to track it *)
rSwayError := rRackSwaySensor_Front - rRackSwaySensor_Rear;
rSwayDerivative := rSwayError - rLastSwayError;
rLastSwayError := rSwayError;

(* 3. State Machine Execution *)
CASE eState OF
    0: (* Idle *)
        IF ABS(rTargetPosition_X - rCurrentPosition_X) > 0.05 OR ABS(rTargetPosition_Y - rCurrentPosition_Y) > 0.05 THEN
            eState := 10;
            bInPosition := FALSE;
        ELSIF bUldPresent AND NOT bUldSeated AND ABS(rTargetPosition_Z) > 0.1 THEN
            eState := 30;
            bInPosition := FALSE;
        END_IF;
        
    10: (* Move X/Y to target coordinates *)
        (* X drive command combines standard P-control with sway tracking derivative *)
        rDriveCommand_X := ((rTargetPosition_X - rCurrentPosition_X) * 4.5) + (rSwayError * rSwayKp) + (rSwayDerivative * rSwayKd);
        
        IF ABS(rTargetPosition_X - rCurrentPosition_X) <= 0.05 AND ABS(rTargetPosition_Y - rCurrentPosition_Y) <= 0.05 THEN
            rDriveCommand_X := 0.0;
            IF bUldPresent AND NOT bUldSeated THEN
                eState := 30; (* Proceed to nesting *)
            ELSE
                bInPosition := TRUE;
                eState := 0;
            END_IF;
        END_IF;
        
    30: (* Extend Z - Friction Drive Nesting Sequence *)
        bFrictionDriveEnable := TRUE;
        (* Approach speed based on distance *)
        rFrictionDriveCommand_Z := (rTargetPosition_Z - rCurrentPosition_Z) * 12.0;
        
        bTorqueLimitReached := rFrictionDriveTorqueFB > rTorqueLimit;
        
        IF bTorqueLimitReached THEN
            (* Check if torque spike is at valid nesting depth *)
            IF ABS(rTargetPosition_Z - rCurrentPosition_Z) < 0.15 AND bUldSeated THEN
                eState := 40; (* Successfully nested, retract *)
            ELSE
                (* Torque limit hit prematurely = Jammed *)
                bFault := TRUE;
                iFaultCode := 5001; (* ETV Z-Drive Nesting Jam Fault *)
                rFrictionDriveCommand_Z := 0.0;
                eState := 99;
            END_IF;
        ELSIF ABS(rTargetPosition_Z - rCurrentPosition_Z) <= 0.05 THEN
             (* Reached target but no torque spike/seating confirmed *)
             bFault := TRUE;
             iFaultCode := 5002; (* ULD Seating Sensor Missed *)
             rFrictionDriveCommand_Z := 0.0;
             eState := 99;
        END_IF;
        
    40: (* Retract Z back to home *)
        rFrictionDriveCommand_Z := -45.0; (* Fixed retract speed *)
        IF rCurrentPosition_Z <= 0.05 THEN
            bFrictionDriveEnable := FALSE;
            rFrictionDriveCommand_Z := 0.0;
            bInPosition := TRUE;
            eState := 0;
        END_IF;
        
    99: (* Error State *)
        rDriveCommand_X := 0.0;
        rLiftValveCommand_Left := 0.0;
        rLiftValveCommand_Right := 0.0;
        rFrictionDriveCommand_Z := 0.0;
        bFrictionDriveEnable := FALSE;
        (* Requires bSystemEnable toggle to clear *)
END_CASE;

(* 4. Final Output Limiting / Anti-Windup *)
IF rDriveCommand_X > 100.0 THEN rDriveCommand_X := 100.0; ELSIF rDriveCommand_X < -100.0 THEN rDriveCommand_X := -100.0; END_IF;
IF rLiftValveCommand_Left > 100.0 THEN rLiftValveCommand_Left := 100.0; ELSIF rLiftValveCommand_Left < -100.0 THEN rLiftValveCommand_Left := -100.0; END_IF;
IF rLiftValveCommand_Right > 100.0 THEN rLiftValveCommand_Right := 100.0; ELSIF rLiftValveCommand_Right < -100.0 THEN rLiftValveCommand_Right := -100.0; END_IF;
IF rFrictionDriveCommand_Z > 100.0 THEN rFrictionDriveCommand_Z := 100.0; ELSIF rFrictionDriveCommand_Z < -100.0 THEN rFrictionDriveCommand_Z := -100.0; END_IF;

END_FUNCTION_BLOCK
```"""

os.makedirs(r"C:\Users\majip\Downloads\LLM REASEARCH\data\swarm_raw", exist_ok=True)
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": st_code}]}
with open(f"C:\\Users\\majip\\Downloads\\LLM REASEARCH\\data\\swarm_raw\\agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
    json.dump(record, f, indent=4)
print("Saved json file successfully")
