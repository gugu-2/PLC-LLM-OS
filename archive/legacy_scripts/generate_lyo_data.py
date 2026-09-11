import json
import uuid
import os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Pharmaceutical Lyophilizer (Freeze-Dryer).
Task: Invent a highly complex control scenario for this domain (e.g., ice condenser defrosting cascades, vacuum pump crossover sequencing, and silicone oil thermal fluid profiling).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."""

st_code = """```iec-st
FUNCTION_BLOCK FB_Lyophilizer_CoreSequence
TITLE = 'Lyophilizer Master Control Sequence'
AUTHOR = 'Lumina_Elite_Synthetic_Data_Architect'
VERSION = '2.1'

(*
Description:
This block manages the complex interactions in a pharmaceutical freeze-dryer.
It coordinates the silicone oil thermal fluid profiling for the shelves,
the vacuum pump crossover sequencing (Main to Roots blower), and the
ice condenser defrosting cascade.
*)

VAR_INPUT
    bEnableSequence : BOOL;             // Master enable sequence
    bEmergencyStop : BOOL;              // E-Stop active low
    rChamberPressure : REAL;            // Current chamber pressure (mBar)
    rCondenserTemp : REAL;              // Condenser coil temperature (C)
    rShelfTemp : REAL;                  // Shelf surface temperature (C)
    rSiliconeOilInletTemp : REAL;       // Silicone oil inlet temp (C)
    bDefrostRequest : BOOL;             // Request to initiate defrost cascade
    rPrimaryDryingTargetPress : REAL;   // Target pressure for primary drying
    rPrimaryDryingTargetTemp : REAL;    // Target temp for primary drying
    rSecondaryDryingTargetTemp : REAL;  // Target temp for secondary drying
END_VAR

VAR_OUTPUT
    bVacuumPumpMainCmd : BOOL;          // Start/Stop Main Vacuum Pump
    bVacuumPumpRootsCmd : BOOL;         // Start/Stop Roots Blower Vacuum Pump
    bProportionalValveCmd : REAL;       // Bleed valve for vacuum control (0-100%)
    rSiliconeOilHeaterCmd : REAL;       // Heating output (0-100%)
    rSiliconeOilCoolerCmd : REAL;       // Cooling output (0-100%)
    bCondenserCompressorCmd : BOOL;     // Condenser refrigeration cmd
    bCondenserDefrostHeaterCmd : BOOL;  // Hot gas / electrical defrost heater
    iActiveState : INT;                 // Sequence current state
    bSequenceError : BOOL;              // Global error flag
    sStatusMessage : STRING(50);        // HMI status text
END_VAR

VAR
    eState : (IDLE, PRE_COOLING, FREEZING, EVACUATION, PRIMARY_DRYING, SECONDARY_DRYING, CONDENSER_DEFROST, ERROR_STATE) := IDLE;
    
    fbVacuumTimer : TON;
    fbDefrostTimer : TON;
    fbRootsCrossoverTimer : TON;
    fbFreezingTimer : TON;
    
    rTargetShelfTemp : REAL;
    rTargetChamberPressure : REAL;
    
    bVacuumCrossoverPermissive : BOOL;
    
    // PID Controllers
    fbPID_SiliconeOil : FB_PID_Controller;
    fbPID_Vacuum : FB_PID_Controller;
END_VAR

(* ----- Emergency Stop & Interlocks ----- *)
IF NOT bEmergencyStop THEN
    eState := ERROR_STATE;
    bSequenceError := TRUE;
    sStatusMessage := 'E-STOP ACTIVE';
    
    // Fail-safe outputs
    bVacuumPumpMainCmd := FALSE;
    bVacuumPumpRootsCmd := FALSE;
    rSiliconeOilHeaterCmd := 0.0;
    rSiliconeOilCoolerCmd := 100.0; // Max cooling on fault
    bCondenserCompressorCmd := TRUE; // Keep condenser cold
    bCondenserDefrostHeaterCmd := FALSE;
    bProportionalValveCmd := 0.0;
    RETURN;
END_IF

(* ----- Main State Machine ----- *)
CASE eState OF
    
    IDLE:
        sStatusMessage := 'READY / IDLE';
        iActiveState := 0;
        bVacuumPumpMainCmd := FALSE;
        bVacuumPumpRootsCmd := FALSE;
        bCondenserCompressorCmd := FALSE;
        bCondenserDefrostHeaterCmd := FALSE;
        rTargetShelfTemp := 20.0; // Ambient setpoint
        
        IF bEnableSequence THEN
            IF bDefrostRequest THEN
                eState := CONDENSER_DEFROST;
            ELSE
                eState := PRE_COOLING;
            END_IF
        END_IF
        
    PRE_COOLING:
        sStatusMessage := 'PRE-COOLING SHELVES & CONDENSER';
        iActiveState := 10;
        
        // Start refrigeration for condenser
        bCondenserCompressorCmd := TRUE;
        
        // Set shelf target for freezing
        rTargetShelfTemp := -45.0; 
        
        // Wait for condenser to reach optimal vapor trapping temperature
        IF (rCondenserTemp <= -60.0) AND (rShelfTemp <= -40.0) THEN
            fbFreezingTimer(IN := TRUE, PT := T#120M); // 2 hour freeze hold
            IF fbFreezingTimer.Q THEN
                fbFreezingTimer(IN := FALSE); // Reset
                eState := EVACUATION;
            END_IF
        ELSE
            fbFreezingTimer(IN := FALSE);
        END_IF
        
    EVACUATION:
        sStatusMessage := 'EVACUATING CHAMBER (CROSSOVER PENDING)';
        iActiveState := 20;
        
        // Start Primary Vacuum Pump
        bVacuumPumpMainCmd := TRUE;
        
        // Vacuum Crossover Logic for Roots Blower
        // Roots blower must not start until pressure is below crossover threshold (e.g., 50 mBar)
        IF (rChamberPressure < 50.0) THEN
            fbRootsCrossoverTimer(IN := TRUE, PT := T#10S);
            IF fbRootsCrossoverTimer.Q THEN
                bVacuumPumpRootsCmd := TRUE;
            END_IF
        ELSE
            fbRootsCrossoverTimer(IN := FALSE);
            bVacuumPumpRootsCmd := FALSE;
        END_IF
        
        // Transition to Primary Drying once target vacuum achieved
        IF (rChamberPressure <= rPrimaryDryingTargetPress) AND bVacuumPumpRootsCmd THEN
            eState := PRIMARY_DRYING;
        END_IF
        
    PRIMARY_DRYING:
        sStatusMessage := 'PRIMARY DRYING - SUBLIMATION PHASE';
        iActiveState := 30;
        
        rTargetShelfTemp := rPrimaryDryingTargetTemp;
        rTargetChamberPressure := rPrimaryDryingTargetPress;
        
        // Vacuum Control via Bleed Valve
        fbPID_Vacuum(
            rSetpoint := rTargetChamberPressure,
            rProcessValue := rChamberPressure,
            rKp := 2.5,
            rKi := 0.1,
            rKd := 0.05,
            rOutput => bProportionalValveCmd
        );
        
        // Primary drying termination logic placeholder
        IF NOT bEnableSequence THEN 
            eState := SECONDARY_DRYING;
        END_IF
        
    SECONDARY_DRYING:
        sStatusMessage := 'SECONDARY DRYING - DESORPTION PHASE';
        iActiveState := 40;
        
        rTargetShelfTemp := rSecondaryDryingTargetTemp;
        bProportionalValveCmd := 0.0; 
        
        IF NOT bEnableSequence THEN 
            eState := IDLE;
        END_IF
        
    CONDENSER_DEFROST:
        sStatusMessage := 'CONDENSER DEFROST CASCADE';
        iActiveState := 50;
        
        bCondenserCompressorCmd := FALSE;
        bVacuumPumpMainCmd := FALSE;
        bVacuumPumpRootsCmd := FALSE;
        
        // Activate Hot Gas or Electrical Defrost
        bCondenserDefrostHeaterCmd := TRUE;
        
        fbDefrostTimer(IN := TRUE, PT := T#45M);
        IF fbDefrostTimer.Q OR (rCondenserTemp > 25.0) THEN
            bCondenserDefrostHeaterCmd := FALSE;
            fbDefrostTimer(IN := FALSE);
            bDefrostRequest := FALSE;
            eState := IDLE;
        END_IF
        
    ERROR_STATE:
        iActiveState := 99;
        IF NOT bEmergencyStop AND NOT bEnableSequence THEN
            bSequenceError := FALSE;
            eState := IDLE;
        END_IF
        
END_CASE

(* ----- Thermal Fluid Profiling (Silicone Oil PID) ----- *)
IF (eState <> ERROR_STATE) THEN
    fbPID_SiliconeOil(
        rSetpoint := rTargetShelfTemp,
        rProcessValue := rShelfTemp,
        rKp := 5.0,
        rKi := 0.2,
        rKd := 1.0,
        rOutputMax := 100.0,
        rOutputMin := -100.0
    );
    
    // Split range output
    IF fbPID_SiliconeOil.rOutput > 0.0 THEN
        rSiliconeOilHeaterCmd := fbPID_SiliconeOil.rOutput;
        rSiliconeOilCoolerCmd := 0.0;
    ELSE
        rSiliconeOilHeaterCmd := 0.0;
        rSiliconeOilCoolerCmd := ABS(fbPID_SiliconeOil.rOutput);
    END_IF
END_IF
END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
os.makedirs("data", exist_ok=True)

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": st_code}
    ]
}

file_id = uuid.uuid4().hex[:8]
filename = f"data/swarm_raw/agent_{file_id}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)

with open("data/synthetic_generation_v3_enterprise.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\\n")

print(f"Generated successfully: {filename}")
