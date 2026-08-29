import json, uuid, os

os.makedirs("data/swarm_raw", exist_ok=True)
prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Commercial Coffee Freeze-Drying (Lyophilization).
Task: Invent a highly complex control scenario for this domain (e.g., sublimation vacuum chamber pressure profiling, radiant heating shelf thermal zones, and condenser ice loading limit).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."""

code = """```iec-st
FUNCTION_BLOCK FB_CoffeeLyophilizer
VAR_INPUT
    bStartCycle : BOOL;
    bEmergencyStop : BOOL;
    rChamberPressure : REAL; (* Current chamber pressure in mTorr *)
    rCondenserTemp : REAL; (* Condenser temperature in Celsius *)
    rShelfTemp_Zone1 : REAL; (* Shelf 1 temperature in Celsius *)
    rShelfTemp_Zone2 : REAL; (* Shelf 2 temperature in Celsius *)
    rProductTemp_Avg : REAL; (* Average product temperature from RTDs *)
    rTargetPressure : REAL; (* Target pressure setpoint *)
    rTargetShelfTemp : REAL; (* Target shelf temperature setpoint *)
    tPrimaryDryingTime : TIME := T#24H;
    tSecondaryDryingTime : TIME := T#6H;
END_VAR

VAR_OUTPUT
    bVacuumPumpRun : BOOL;
    rVacuumValvePos : REAL; (* 0-100% position *)
    bCompressorRun : BOOL;
    rHeatingValve_Zone1 : REAL; (* 0-100% heating valve *)
    rHeatingValve_Zone2 : REAL; (* 0-100% heating valve *)
    rCoolingValve_Zone1 : REAL; (* 0-100% cooling valve *)
    rCoolingValve_Zone2 : REAL; (* 0-100% cooling valve *)
    eState : INT; (* 0: Idle, 1: Freezing, 2: Primary Drying, 3: Secondary Drying, 4: Complete, 5: Fault *)
    bAlarm : BOOL;
    sStatusMessage : STRING[50];
END_VAR

VAR
    tCycleTimer : TON;
    rPressureError : REAL;
    rShelfTempError1 : REAL;
    rShelfTempError2 : REAL;
    PID_Vacuum : FB_PID;
    PID_Shelf1 : FB_PID;
    PID_Shelf2 : FB_PID;
    bInitialize : BOOL := TRUE;
END_VAR

(* Implementation *)
IF bEmergencyStop THEN
    eState := 5;
    bAlarm := TRUE;
    sStatusMessage := 'EMERGENCY STOP';
    bVacuumPumpRun := FALSE;
    bCompressorRun := FALSE;
    rVacuumValvePos := 0.0;
    rHeatingValve_Zone1 := 0.0;
    rHeatingValve_Zone2 := 0.0;
    rCoolingValve_Zone1 := 100.0; (* Failsafe cool *)
    rCoolingValve_Zone2 := 100.0;
    RETURN;
END_IF;

IF bInitialize THEN
    PID_Vacuum.Kp := 0.5;
    PID_Vacuum.Ki := 0.1;
    PID_Vacuum.Kd := 0.05;
    
    PID_Shelf1.Kp := 1.2;
    PID_Shelf1.Ki := 0.2;
    PID_Shelf1.Kd := 0.1;
    
    PID_Shelf2.Kp := 1.2;
    PID_Shelf2.Ki := 0.2;
    PID_Shelf2.Kd := 0.1;
    
    bInitialize := FALSE;
END_IF;

CASE eState OF
    0: (* Idle *)
        IF bStartCycle THEN
            eState := 1; (* Move to Freezing *)
            sStatusMessage := 'Freezing Phase';
            bCompressorRun := TRUE;
        END_IF;
        
    1: (* Freezing *)
        (* Deep freeze the product below eutectic point *)
        IF rProductTemp_Avg < -40.0 THEN
            eState := 2; (* Move to Primary Drying *)
            sStatusMessage := 'Primary Drying (Sublimation)';
            bVacuumPumpRun := TRUE;
            tCycleTimer(IN := FALSE); (* Reset timer *)
        END_IF;
        
    2: (* Primary Drying - Sublimation *)
        tCycleTimer(IN := TRUE, PT := tPrimaryDryingTime);
        
        (* Pressure Control via Vacuum Valve *)
        PID_Vacuum(
            rSetpoint := rTargetPressure,
            rProcessValue := rChamberPressure,
            rOutput => rVacuumValvePos
        );
        
        (* Shelf Heating Control *)
        PID_Shelf1(
            rSetpoint := rTargetShelfTemp,
            rProcessValue := rShelfTemp_Zone1,
            rOutput => rHeatingValve_Zone1
        );
        PID_Shelf2(
            rSetpoint := rTargetShelfTemp,
            rProcessValue := rShelfTemp_Zone2,
            rOutput => rHeatingValve_Zone2
        );
        
        IF tCycleTimer.Q THEN
            eState := 3; (* Move to Secondary Drying *)
            sStatusMessage := 'Secondary Drying (Desorption)';
            tCycleTimer(IN := FALSE);
        END_IF;
        
    3: (* Secondary Drying - Desorption *)
        tCycleTimer(IN := TRUE, PT := tSecondaryDryingTime);
        
        (* Higher temperature, lower pressure *)
        PID_Vacuum(
            rSetpoint := rTargetPressure / 2.0,
            rProcessValue := rChamberPressure,
            rOutput => rVacuumValvePos
        );
        
        PID_Shelf1(
            rSetpoint := rTargetShelfTemp + 10.0,
            rProcessValue := rShelfTemp_Zone1,
            rOutput => rHeatingValve_Zone1
        );
        PID_Shelf2(
            rSetpoint := rTargetShelfTemp + 10.0,
            rProcessValue := rShelfTemp_Zone2,
            rOutput => rHeatingValve_Zone2
        );
        
        IF tCycleTimer.Q THEN
            eState := 4; (* Complete *)
            sStatusMessage := 'Cycle Complete';
            bVacuumPumpRun := FALSE;
            rVacuumValvePos := 0.0;
        END_IF;
        
    4: (* Complete *)
        rHeatingValve_Zone1 := 0.0;
        rHeatingValve_Zone2 := 0.0;
        IF NOT bStartCycle THEN
            eState := 0;
            sStatusMessage := 'Idle';
        END_IF;
        
    5: (* Fault *)
        (* Fault logic already handled by e-stop, additional monitoring could go here *)
        IF NOT bEmergencyStop THEN
            bAlarm := FALSE;
            eState := 0;
        END_IF;
END_CASE;

(* Condenser limit monitoring *)
IF rCondenserTemp > -50.0 AND (eState = 2 OR eState = 3) THEN
    bAlarm := TRUE;
    sStatusMessage := 'WARNING: Condenser Overload';
    (* Reduce shelf heating to slow sublimation *)
    rHeatingValve_Zone1 := rHeatingValve_Zone1 * 0.5;
    rHeatingValve_Zone2 := rHeatingValve_Zone2 * 0.5;
END_IF;

END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)
print(f"Generated {filename}")
