import json

content = """(*
================================================================================
FUNCTION_BLOCK FB_AHU_Controller
================================================================================
Description:
    Advanced Air Handling Unit (AHU) Controller for Enterprise BMS.
    Includes hardware abstractions, safety interlocks, freeze protection,
    economizer logic, and chilled water PID control.

Author: Lumina Synthetic Data Architect
Version: 2.0.0
================================================================================
*)
FUNCTION_BLOCK FB_AHU_Controller

VAR_INPUT
    // Hardware Abstractions (Physical Inputs)
    bHw_SupplyFanStatus     : BOOL;  // Supply Fan Proof of Airflow (Current Switch/DP)
    bHw_ReturnFanStatus     : BOOL;  // Return Fan Proof of Airflow
    bHw_FreezeStat          : BOOL;  // Hardwired low-limit freeze stat (NC, opens on freeze)
    bHw_FireAlarm           : BOOL;  // Fire Alarm Interlock (NC, opens on alarm)
    bHw_ThermalOverload     : BOOL;  // Supply Fan VFD/Motor Thermal Overload (NC)
    bHw_EStop               : BOOL;  // Emergency Stop Pushbutton (NC)
    
    // Analog Inputs
    rHw_SupplyAirTemp       : REAL;  // Supply Air Temperature (deg C)
    rHw_ReturnAirTemp       : REAL;  // Return Air Temperature (deg C)
    rHw_MixedAirTemp        : REAL;  // Mixed Air Temperature (deg C)
    rHw_OutsideAirTemp      : REAL;  // Outside Air Temperature (deg C)
    rHw_OutsideAirEnthalpy  : REAL;  // Outside Air Enthalpy (kJ/kg)
    rHw_ReturnAirEnthalpy   : REAL;  // Return Air Enthalpy (kJ/kg)
    
    // Setpoints & Configuration
    bEnable                 : BOOL;  // System Enable Command
    rSupplyAirTempSp        : REAL;  // Supply Air Temperature Setpoint (deg C)
    rMinDamperPos           : REAL;  // Minimum Outside Air Damper Position (%)
    rEconomizerEnthalpySp   : REAL;  // Enthalpy Setpoint for Economizer (kJ/kg)
    
    // PID Parameters (Chilled Water)
    rChwKp                  : REAL := 2.5;
    rChwKi                  : REAL := 0.1;
    rChwKd                  : REAL := 0.0;
END_VAR

VAR_OUTPUT
    // Hardware Abstractions (Physical Outputs)
    bHw_SupplyFanCmd        : BOOL;  // Supply Fan Start/Stop Command
    bHw_ReturnFanCmd        : BOOL;  // Return Fan Start/Stop Command
    rHw_OaDamperCmd         : REAL;  // Outside Air Damper Command (0-100%)
    rHw_EaDamperCmd         : REAL;  // Exhaust Air Damper Command (0-100%)
    rHw_MaDamperCmd         : REAL;  // Mixed/Return Air Damper Command (0-100%)
    rHw_ChwValveCmd         : REAL;  // Chilled Water Valve Command (0-100%)
    
    // Status & Alarms
    bSystemRunning          : BOOL;
    bAlarm_EStop            : BOOL;
    bAlarm_Fire             : BOOL;
    bAlarm_Freeze           : BOOL;
    bAlarm_ThermalOverload  : BOOL;
    bAlarm_FanFailure       : BOOL;
    bEconomizerActive       : BOOL;
END_VAR

VAR
    // Internal State Machine
    eState                  : (INIT, OFF, PRESTART, RUNNING, FAULT);
    
    // Timers
    tonFanProof             : TON;
    tonPrestartDelay        : TON;
    
    // PIDs
    fbChwPID                : FB_PID; // Assuming standard library PID implementation
    
    // Internal Variables
    bSafetyOk               : BOOL;
    rCoolingDemand          : REAL;
END_VAR

(*=============================================================================
   Safety & Interlock Processing
=============================================================================*)
// Fail-safe logic: Inputs are Normally Closed (NC), so TRUE means OK, FALSE means Alarm.
bAlarm_EStop           := NOT bHw_EStop;
bAlarm_Fire            := NOT bHw_FireAlarm;
bAlarm_Freeze          := NOT bHw_FreezeStat;
bAlarm_ThermalOverload := NOT bHw_ThermalOverload;

// Global Safety Interlock
bSafetyOk := NOT bAlarm_EStop AND 
             NOT bAlarm_Fire AND 
             NOT bAlarm_Freeze AND 
             NOT bAlarm_ThermalOverload;

(*=============================================================================
   State Machine for AHU Control
=============================================================================*)
CASE eState OF
    
    INIT:
        // Initialization state: force outputs safely off
        bHw_SupplyFanCmd := FALSE;
        bHw_ReturnFanCmd := FALSE;
        rHw_OaDamperCmd  := 0.0;
        rHw_EaDamperCmd  := 0.0;
        rHw_MaDamperCmd  := 100.0; // Recirculate fully on init
        rHw_ChwValveCmd  := 0.0;
        IF bSafetyOk THEN
            eState := OFF;
        END_IF;
        
    OFF:
        // System off state
        bHw_SupplyFanCmd := FALSE;
        bHw_ReturnFanCmd := FALSE;
        rHw_OaDamperCmd  := 0.0;
        rHw_EaDamperCmd  := 0.0;
        rHw_MaDamperCmd  := 100.0;
        rHw_ChwValveCmd  := 0.0;
        
        IF bEnable AND bSafetyOk THEN
            eState := PRESTART;
        ELSIF NOT bSafetyOk THEN
            eState := FAULT;
        END_IF;
        
    PRESTART:
        // Open dampers to minimum position before starting fans to prevent duct implosion
        rHw_OaDamperCmd := rMinDamperPos;
        rHw_MaDamperCmd := 100.0 - rMinDamperPos;
        rHw_EaDamperCmd := rMinDamperPos;
        
        tonPrestartDelay(IN := TRUE, PT := T#10S);
        
        IF tonPrestartDelay.Q AND bSafetyOk THEN
            eState := RUNNING;
            tonPrestartDelay(IN := FALSE);
        ELSIF NOT bSafetyOk OR NOT bEnable THEN
            eState := OFF;
            tonPrestartDelay(IN := FALSE);
        END_IF;

    RUNNING:
        bSystemRunning := TRUE;
        bHw_SupplyFanCmd := TRUE;
        bHw_ReturnFanCmd := TRUE;
        
        // Fan proof of airflow evaluation (allow 30s for fans to spool up)
        tonFanProof(IN := bHw_SupplyFanCmd, PT := T#30S);
        IF tonFanProof.Q AND (NOT bHw_SupplyFanStatus OR NOT bHw_ReturnFanStatus) THEN
            bAlarm_FanFailure := TRUE;
            eState := FAULT;
        END_IF;
        
        IF NOT bSafetyOk OR NOT bEnable THEN
            eState := OFF;
            bSystemRunning := FALSE;
        END_IF;
        
    FAULT:
        // Fault override state
        bHw_SupplyFanCmd := FALSE;
        bHw_ReturnFanCmd := FALSE;
        rHw_OaDamperCmd  := 0.0;
        rHw_EaDamperCmd  := 0.0;
        rHw_MaDamperCmd  := 100.0;
        
        // Freeze protection override: if freezing, open CHW valve to allow flow and prevent coil rupture
        IF bAlarm_Freeze THEN
            rHw_ChwValveCmd := 100.0;
        ELSE
            rHw_ChwValveCmd := 0.0;
        END_IF;
        
        IF bSafetyOk AND NOT bAlarm_FanFailure THEN
            eState := OFF;
        END_IF;
        
END_CASE;

(*=============================================================================
   Economizer & Temperature Control Logic (Only active in RUNNING state)
=============================================================================*)
IF eState = RUNNING THEN
    
    // 1. Economizer Suitability Check
    // Active if Outside Air Enthalpy is lower than Return Air Enthalpy AND lower than Setpoint
    bEconomizerActive := (rHw_OutsideAirEnthalpy < rHw_ReturnAirEnthalpy) AND 
                         (rHw_OutsideAirEnthalpy < rEconomizerEnthalpySp);
                         
    // 2. Chilled Water PID Loop calculation
    fbChwPID(
        ENABLE := TRUE,
        SP := rSupplyAirTempSp,
        PV := rHw_SupplyAirTemp,
        KP := rChwKp,
        KI := rChwKi,
        KD := rChwKd
    );
    rCoolingDemand := fbChwPID.Y; // 0.0 to 100.0 assumed output range
    
    // 3. Control Sequencing (Economizer vs Mechanical Cooling)
    IF bEconomizerActive THEN
        // Use outside air for free cooling
        // Linearly scale cooling demand (0-100%) to damper positions (MinOa-100%)
        rHw_OaDamperCmd := rMinDamperPos + (rCoolingDemand * (100.0 - rMinDamperPos) / 100.0);
        rHw_EaDamperCmd := rHw_OaDamperCmd;
        rHw_MaDamperCmd := 100.0 - rHw_OaDamperCmd;
        
        // Split-range control for CHW Valve: activate if cooling demand > 50%
        IF rCoolingDemand > 50.0 THEN
            rHw_ChwValveCmd := (rCoolingDemand - 50.0) * 2.0; 
            IF rHw_ChwValveCmd < 0.0 THEN rHw_ChwValveCmd := 0.0; END_IF;
            IF rHw_ChwValveCmd > 100.0 THEN rHw_ChwValveCmd := 100.0; END_IF;
        ELSE
            rHw_ChwValveCmd := 0.0;
        END_IF;
        
    ELSE
        // Economizer inactive: Dampers at minimum position, use mechanical cooling exclusively
        rHw_OaDamperCmd := rMinDamperPos;
        rHw_EaDamperCmd := rMinDamperPos;
        rHw_MaDamperCmd := 100.0 - rMinDamperPos;
        
        rHw_ChwValveCmd := rCoolingDemand;
    END_IF;
    
ELSE
    // Reset PIDs and states when not running
    fbChwPID(ENABLE := FALSE);
    bEconomizerActive := FALSE;
END_IF;

END_FUNCTION_BLOCK
"""

dataset_entry = {
    "messages": [
        {
            "role": "user",
            "content": "Evolve the basic analog temperature reading logic into a comprehensive Enterprise-Grade Building Management System (BMS) Air Handling Unit (AHU) controller in IEC 61131-3 Structured Text. The implementation must include complex state machines, safety interlocks (e-stops, thermal overloads, freeze stat protection), hardware abstractions, mixed-air damper economizer logic, and chilled water valve PID loops. Add flawless, production-ready comments."
        },
        {
            "role": "assistant",
            "content": content
        }
    ]
}

with open(r'C:\Users\majip\Downloads\LLM REASEARCH\data\evol_instruct_dataset.jsonl', 'a') as f:
    f.write(json.dumps(dataset_entry) + '\n')
