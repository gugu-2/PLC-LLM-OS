import json
import os

prompt = """Evolve a basic IEC 61131-3 tank level control function block into a complex Marine Ballast Water Management System (BWMS). The basic block just monitors level and toggles a pump. The evolved system must include pitch/roll inclinometer compensation for accurate volume calculation, port/starboard tank balancing algorithms (cross-flooding), UV reactor treatment sequencing (warm-up, intensity monitoring, cooldown), and extensive safety interlocks (e-stops, pump thermal overloads, high/low level alarms). Use Structured Text (ST)."""

response = """Here is the evolved Marine Ballast Water Management System (BWMS) implemented in IEC 61131-3 Structured Text (ST).

```iecst
(* 
   =============================================================================
   Function Block: FB_Marine_BWMS
   Description:    Marine Ballast Water Management System with Inclinometer 
                   Compensation, Tank Balancing, and UV Treatment.
   Author:         Lumina Elite Synthetic Data Architect
   Version:        1.0
   =============================================================================
*)
TYPE E_UV_State :
(
    UV_OFF := 0,
    UV_WARMUP := 1,
    UV_READY := 2,
    UV_TREATMENT := 3,
    UV_COOLDOWN := 4,
    UV_FAULT := 5
);
END_TYPE

FUNCTION_BLOCK FB_Marine_BWMS
VAR_INPUT
    // Safety and General Commands
    bEStop             : BOOL;    // Emergency Stop (NC, TRUE = OK)
    bSystemEnable      : BOOL;    // Master enable for system operation
    bStartBallast      : BOOL;    // Command to start ballasting
    bStartDeBallast    : BOOL;    // Command to start de-ballasting
    
    // Inclinometer Inputs
    rPitchAngle        : REAL;    // Vessel pitch angle in degrees
    rRollAngle         : REAL;    // Vessel roll angle in degrees
    
    // Tank Level Sensors (Raw Height in meters)
    rPortLevelRaw      : REAL;
    rStbdLevelRaw      : REAL;
    
    // UV Reactor Inputs
    rUVIntensity       : REAL;    // W/m2
    rUVTemperature     : REAL;    // Deg C
    
    // Pump and Valve Status
    bPumpPortThermalOk : BOOL;    // Port pump thermal overload (NC)
    bPumpStbdThermalOk : BOOL;    // Stbd pump thermal overload (NC)
    
    // Settings
    rMaxTankLevel      : REAL := 10.0; // Max permitted level (m)
    rMinTankLevel      : REAL := 0.5;  // Min permitted level (m)
    rMaxImbalance      : REAL := 1.0;  // Max port/stbd diff before balancing (m)
    rTankLength        : REAL := 20.0; // Tank dimension for compensation (m)
    rTankWidth         : REAL := 15.0; // Tank dimension for compensation (m)
    
    rMinUVIntensity    : REAL := 300.0; // Min acceptable UV intensity
    rMaxUVTemp         : REAL := 60.0;  // Max UV temp
END_VAR

VAR_OUTPUT
    // Actuators
    bPumpPortCmd       : BOOL;
    bPumpStbdCmd       : BOOL;
    bCrossFloodValve   : BOOL;
    bUVLampsCmd        : BOOL;
    bMainInletValve    : BOOL;
    
    // Compensated Levels
    rPortLevelComp     : REAL;
    rStbdLevelComp     : REAL;
    
    // Status
    eUVState           : E_UV_State;
    bSystemFault       : BOOL;
    sStatusMessage     : STRING(50);
END_VAR

VAR
    // Timers
    tUVWarmup          : TON;
    tUVCooldown        : TON;
    tAlarmDelay        : TON;
    
    // Internal Flags
    bSafetyOK          : BOOL;
    bImbalanceFault    : BOOL;
    
    // Compensation Math Constants
    rPi                : REAL := 3.1415926535;
END_VAR

// -----------------------------------------------------------------------------
// 1. Safety Interlocks & Hardware Abstractions
// -----------------------------------------------------------------------------
bSafetyOK := bEStop AND bPumpPortThermalOk AND bPumpStbdThermalOk AND (rUVTemperature < rMaxUVTemp);

IF NOT bSafetyOK THEN
    bSystemFault := TRUE;
    sStatusMessage := 'CRITICAL FAULT: Safety Interlock Tripped';
    
    // Fail-safe state
    bPumpPortCmd := FALSE;
    bPumpStbdCmd := FALSE;
    bCrossFloodValve := FALSE;
    bUVLampsCmd := FALSE;
    bMainInletValve := FALSE;
    eUVState := UV_OFF;
    RETURN; // Halt further execution
END_IF;

// -----------------------------------------------------------------------------
// 2. Pitch / Roll Inclinometer Compensation
// -----------------------------------------------------------------------------
// Calculates true volumetric equivalent height based on vessel attitude
// Uses simplified trigonometric compensation for rectangular tanks:
// TrueLevel = RawLevel * cos(Pitch) * cos(Roll) + Center_Offset_Corrections

VAR
    rPitchRad : REAL;
    rRollRad  : REAL;
    rCorrectionPort : REAL;
    rCorrectionStbd : REAL;
END_VAR

rPitchRad := (rPitchAngle * rPi) / 180.0;
rRollRad  := (rRollAngle * rPi) / 180.0;

// Basic geometric correction for level sensor located at tank corner
rCorrectionPort := (rTankLength/2.0 * SIN(rPitchRad)) + (rTankWidth/2.0 * SIN(rRollRad));
rCorrectionStbd := (rTankLength/2.0 * SIN(rPitchRad)) - (rTankWidth/2.0 * SIN(rRollRad));

rPortLevelComp := (rPortLevelRaw * COS(rPitchRad) * COS(rRollRad)) - rCorrectionPort;
rStbdLevelComp := (rStbdLevelRaw * COS(rPitchRad) * COS(rRollRad)) - rCorrectionStbd;

// Ensure non-negative levels
IF rPortLevelComp < 0.0 THEN rPortLevelComp := 0.0; END_IF;
IF rStbdLevelComp < 0.0 THEN rStbdLevelComp := 0.0; END_IF;

// -----------------------------------------------------------------------------
// 3. Port / Starboard Tank Balancing Algorithm
// -----------------------------------------------------------------------------
bImbalanceFault := ABS(rPortLevelComp - rStbdLevelComp) > rMaxImbalance;

IF bImbalanceFault AND bSystemEnable THEN
    // Open cross-flood valve to equalize levels via gravity/pump
    bCrossFloodValve := TRUE;
    sStatusMessage := 'WARNING: Tank Imbalance - Cross Flooding';
ELSE
    bCrossFloodValve := FALSE;
END_IF;

// -----------------------------------------------------------------------------
// 4. UV Reactor Treatment Sequencing State Machine
// -----------------------------------------------------------------------------
// UV Timer Configurations
tUVWarmup(IN := (eUVState = UV_WARMUP), PT := T#3M);
tUVCooldown(IN := (eUVState = UV_COOLDOWN), PT := T#5M);

CASE eUVState OF
    UV_OFF:
        bUVLampsCmd := FALSE;
        IF bSystemEnable AND (bStartBallast OR bStartDeBallast) THEN
            eUVState := UV_WARMUP;
        END_IF;
        
    UV_WARMUP:
        bUVLampsCmd := TRUE;
        sStatusMessage := 'UV Reactor Warming Up';
        IF tUVWarmup.Q THEN
            eUVState := UV_READY;
        END_IF;
        IF NOT bSystemEnable THEN
            eUVState := UV_COOLDOWN;
        END_IF;
        
    UV_READY:
        bUVLampsCmd := TRUE;
        IF rUVIntensity >= rMinUVIntensity THEN
            eUVState := UV_TREATMENT;
        END_IF;
        IF NOT (bStartBallast OR bStartDeBallast) OR NOT bSystemEnable THEN
            eUVState := UV_COOLDOWN;
        END_IF;
        
    UV_TREATMENT:
        bUVLampsCmd := TRUE;
        sStatusMessage := 'UV Treatment Active';
        
        // Monitoring Intensity During Treatment
        IF rUVIntensity < rMinUVIntensity THEN
            eUVState := UV_FAULT;
        END_IF;
        
        IF NOT (bStartBallast OR bStartDeBallast) OR NOT bSystemEnable THEN
            eUVState := UV_COOLDOWN;
        END_IF;
        
    UV_COOLDOWN:
        bUVLampsCmd := FALSE; // Lamps off, but cooling water may flow
        sStatusMessage := 'UV Reactor Cooling Down';
        IF tUVCooldown.Q THEN
            eUVState := UV_OFF;
        END_IF;
        
    UV_FAULT:
        bUVLampsCmd := FALSE;
        bSystemFault := TRUE;
        sStatusMessage := 'FAULT: UV Intensity Drop';
        IF NOT bSystemEnable THEN // Reset fault by disabling system
            eUVState := UV_OFF;
            bSystemFault := FALSE;
        END_IF;
END_CASE;

// -----------------------------------------------------------------------------
// 5. Main Pump & Valve Control
// -----------------------------------------------------------------------------
IF eUVState = UV_TREATMENT AND NOT bSystemFault THEN
    bMainInletValve := TRUE;
    
    IF bStartBallast THEN
        // Fill tanks up to max level
        bPumpPortCmd := (rPortLevelComp < rMaxTankLevel);
        bPumpStbdCmd := (rStbdLevelComp < rMaxTankLevel);
        
    ELSIF bStartDeBallast THEN
        // Empty tanks down to min level
        bPumpPortCmd := (rPortLevelComp > rMinTankLevel);
        bPumpStbdCmd := (rStbdLevelComp > rMinTankLevel);
    END_IF;
ELSE
    // If not treating, ensure main lines and pumps are off
    bMainInletValve := FALSE;
    bPumpPortCmd := FALSE;
    bPumpStbdCmd := FALSE;
END_IF;

// Overrides for Overfill / Run-Dry
IF rPortLevelComp >= rMaxTankLevel THEN bPumpPortCmd := FALSE; END_IF;
IF rStbdLevelComp >= rMaxTankLevel THEN bPumpStbdCmd := FALSE; END_IF;

IF rPortLevelComp <= rMinTankLevel AND bStartDeBallast THEN bPumpPortCmd := FALSE; END_IF;
IF rStbdLevelComp <= rMinTankLevel AND bStartDeBallast THEN bPumpStbdCmd := FALSE; END_IF;

END_FUNCTION_BLOCK
```
"""

entry = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": response}
    ]
}

file_path = "c:\\\\Users\\\\majip\\\\Downloads\\\\LLM REASEARCH\\\\data\\\\evol_instruct_dataset.jsonl"
os.makedirs(os.path.dirname(file_path), exist_ok=True)

with open(file_path, "a", encoding="utf-8") as f:
    f.write(json.dumps(entry) + "\\n")
