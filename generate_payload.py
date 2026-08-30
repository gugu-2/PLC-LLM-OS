import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Continuous Aluminium Extrusion Press.
Task: Invent a highly complex control scenario for this domain (e.g., billet induction pre-heating profiles, dummy block hydraulic sequencing, and run-out table quench cooling).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O.
"""

st_code = """```iec-st
FUNCTION_BLOCK FB_AluminiumExtrusionControl
VAR_INPUT
    bEnable : BOOL; (* System Enable *)
    bEmergencyStop : BOOL; (* E-Stop *)
    rBilletTargetTemp : REAL; (* Target Temp in Celcius *)
    rRamPressureSet : REAL; (* Extrusion Ram Pressure *)
    bDummyBlockRetractCmd : BOOL;
    rQuenchWaterFlowSP : REAL; (* Quench Flow Setpoint *)
    
    (* Sensors *)
    rBilletActualTemp : REAL; 
    rRamActualPressure : REAL;
    rRamPosition : REAL;
    bDummyBlockHome : BOOL;
    bDummyBlockExt : BOOL;
    rQuenchActualFlow : REAL;
END_VAR

VAR_OUTPUT
    bHeatingCoilOn : BOOL;
    rHeatingPowerCmd : REAL;
    bRamAdvance : BOOL;
    bRamRetract : BOOL;
    rRamValveCmd : REAL;
    bDummyBlockAdvance : BOOL;
    bDummyBlockRetract : BOOL;
    rQuenchValveCmd : REAL;
    bSystemFault : BOOL;
    sStatusMessage : STRING;
END_VAR

VAR
    (* Internal State *)
    eState : (INIT, HEATING, LOAD_BILLET, EXTRUSION, QUENCH_COOLING, RETRACT, FAULT);
    PID_Heater : FB_PID_Controller; (* Assuming external PID block *)
    PID_Quench : FB_PID_Controller;
    PID_Ram : FB_PID_Controller;
    
    TMR_HeatingWatchdog : TON;
    TMR_CoolingDelay : TON;
    rTempError : REAL;
END_VAR

(* Implementation *)
IF bEmergencyStop THEN
    eState := FAULT;
    sStatusMessage := 'E-STOP PRESSED. SYSTEM SECURED.';
    bHeatingCoilOn := FALSE;
    rHeatingPowerCmd := 0.0;
    bRamAdvance := FALSE;
    bRamRetract := TRUE; (* Safe state *)
    bDummyBlockAdvance := FALSE;
    bDummyBlockRetract := TRUE;
    rQuenchValveCmd := 0.0;
    bSystemFault := TRUE;
    RETURN;
END_IF;

IF NOT bEnable THEN
    eState := INIT;
    bSystemFault := FALSE;
    sStatusMessage := 'SYSTEM DISABLED.';
    bHeatingCoilOn := FALSE;
    rHeatingPowerCmd := 0.0;
    bRamAdvance := FALSE;
    bRamRetract := FALSE;
    rQuenchValveCmd := 0.0;
    RETURN;
END_IF;

CASE eState OF
    INIT:
        sStatusMessage := 'INITIALIZING EXTRUSION PRESS...';
        IF bDummyBlockHome AND (rRamPosition < 5.0) THEN
            eState := HEATING;
        ELSE
            bDummyBlockRetract := TRUE;
            bRamRetract := TRUE;
        END_IF;
        
    HEATING:
        sStatusMessage := 'HEATING BILLET...';
        bHeatingCoilOn := TRUE;
        
        (* Simple Proportional Control for Heater, normally PID is used *)
        rTempError := rBilletTargetTemp - rBilletActualTemp;
        IF rTempError > 10.0 THEN
            rHeatingPowerCmd := 100.0;
        ELSIF rTempError > 0.0 THEN
            rHeatingPowerCmd := rTempError * 10.0; 
        ELSE
            rHeatingPowerCmd := 0.0;
        END_IF;
        
        TMR_HeatingWatchdog(IN := TRUE, PT := T#300s);
        
        IF (rBilletActualTemp >= (rBilletTargetTemp - 2.0)) THEN
            eState := LOAD_BILLET;
            TMR_HeatingWatchdog(IN := FALSE);
        ELSIF TMR_HeatingWatchdog.Q THEN
            eState := FAULT;
            sStatusMessage := 'HEATING TIMEOUT FAULT.';
        END_IF;
        
    LOAD_BILLET:
        sStatusMessage := 'LOADING BILLET INTO PRESS...';
        bHeatingCoilOn := FALSE;
        rHeatingPowerCmd := 0.0;
        
        bDummyBlockAdvance := TRUE;
        IF bDummyBlockExt THEN
            bDummyBlockAdvance := FALSE;
            eState := EXTRUSION;
        END_IF;
        
    EXTRUSION:
        sStatusMessage := 'EXTRUDING PROFILE...';
        bRamAdvance := TRUE;
        
        (* Pressure Control *)
        IF rRamActualPressure < rRamPressureSet THEN
            rRamValveCmd := rRamValveCmd + 0.5;
        ELSE
            rRamValveCmd := rRamValveCmd - 0.5;
        END_IF;
        
        IF rRamValveCmd > 100.0 THEN rRamValveCmd := 100.0; END_IF;
        IF rRamValveCmd < 0.0 THEN rRamValveCmd := 0.0; END_IF;
        
        IF rRamPosition > 950.0 THEN (* End of stroke *)
            bRamAdvance := FALSE;
            rRamValveCmd := 0.0;
            eState := QUENCH_COOLING;
        END_IF;
        
    QUENCH_COOLING:
        sStatusMessage := 'QUENCH COOLING RUN-OUT...';
        
        IF rQuenchActualFlow < rQuenchWaterFlowSP THEN
            rQuenchValveCmd := rQuenchValveCmd + 1.0;
        ELSE
            rQuenchValveCmd := rQuenchValveCmd - 1.0;
        END_IF;
        
        IF rQuenchValveCmd > 100.0 THEN rQuenchValveCmd := 100.0; END_IF;
        IF rQuenchValveCmd < 0.0 THEN rQuenchValveCmd := 0.0; END_IF;
        
        TMR_CoolingDelay(IN := TRUE, PT := T#30s);
        IF TMR_CoolingDelay.Q THEN
            eState := RETRACT;
            TMR_CoolingDelay(IN := FALSE);
        END_IF;
        
    RETRACT:
        sStatusMessage := 'RETRACTING RAM AND DUMMY BLOCK...';
        rQuenchValveCmd := 0.0;
        bRamRetract := TRUE;
        bDummyBlockRetract := TRUE;
        
        IF (rRamPosition < 5.0) AND bDummyBlockHome THEN
            bRamRetract := FALSE;
            bDummyBlockRetract := FALSE;
            eState := HEATING; (* Ready for next cycle *)
        END_IF;
        
    FAULT:
        bSystemFault := TRUE;
        bHeatingCoilOn := FALSE;
        rHeatingPowerCmd := 0.0;
        bRamAdvance := FALSE;
        rRamValveCmd := 0.0;
        bDummyBlockAdvance := FALSE;
        rQuenchValveCmd := 0.0;
END_CASE;

END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": st_code}]}
os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)
print(f"Saved to {filename}")
