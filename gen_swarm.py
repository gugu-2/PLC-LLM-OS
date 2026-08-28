import json, uuid, os

os.makedirs('data/swarm_raw', exist_ok=True)

prompt = "Invent a highly complex control scenario for Nuclear Submarine Propulsion (e.g., pressurized water reactor primary coolant flow regulation). Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."

st_code = """```iec-st
FUNCTION_BLOCK FB_PWR_PrimaryCoolantControl
TITLE = 'Nuclear Submarine PWR Primary Coolant Regulation'
VERSION : '2.5'

(* 
  This function block manages the primary coolant loop of a naval pressurized water reactor.
  It controls Main Coolant Pump (MCP) speed to maintain optimal delta-T across the core,
  regulates pressurizer pressure using heaters and spray valves, and monitors critical
  safety limits to initiate an automatic scram (reactor trip) if necessary.
*)

VAR_INPUT
    rReactorPower_Pct      : REAL;   (* Reactor thermal power (0.0 to 100.0 %) *)
    rCoreInletTemp_C       : REAL;   (* Primary coolant core inlet temperature (deg C) *)
    rCoreOutletTemp_C      : REAL;   (* Primary coolant core outlet temperature (deg C) *)
    rPrimaryPressure_MPa   : REAL;   (* Primary loop pressure (MPa) *)
    rMCPSpeedFeedback_RPM  : REAL;   (* Main Coolant Pump speed feedback (RPM) *)
    rSG_Level_Pct          : REAL;   (* Steam Generator water level (0.0 to 100.0 %) *)
    bExternalScram         : BOOL;   (* External scram command *)
    bAckAlarms             : BOOL;   (* Acknowledge alarms *)
    tCycleTime_ms          : REAL := 10.0; (* Execution cycle time in ms *)
END_VAR

VAR_OUTPUT
    rMCPSpeedSetpoint_RPM  : REAL;   (* Commanded MCP speed (RPM) *)
    rPressurizerHeater_Pct : REAL;   (* Proportional heater command (0.0 to 100.0 %) *)
    bPressurizerSprayValve : BOOL;   (* Spray valve open command *)
    bScramInitiated        : BOOL;   (* Reactor scram triggered *)
    bAlarm_HighTemp        : BOOL;   (* High temperature alarm flag *)
    bAlarm_HighPressure    : BOOL;   (* High pressure alarm flag *)
    bAlarm_LowPressure     : BOOL;   (* Low pressure alarm flag *)
    bAlarm_MCPTrip         : BOOL;   (* Main coolant pump trip alarm *)
END_VAR

VAR
    rTargetDeltaT          : REAL;   (* Calculated target delta T based on power *)
    rActualDeltaT          : REAL;   (* Actual core delta T *)
    rSpeedError            : REAL;   (* Speed error for MCP PI controller *)
    rSpeedIntegral         : REAL;   (* Integral term for MCP PI *)
    rKp_MCP                : REAL := 15.5;  (* Proportional gain for MCP *)
    rKi_MCP                : REAL := 2.2;   (* Integral gain for MCP *)
    rMaxMCPSpeed           : REAL := 3600.0; (* Max pump speed in RPM *)
    rMinMCPSpeed           : REAL := 450.0;  (* Min pump speed in RPM (decay heat removal) *)

    rNominalPressure       : REAL := 15.5;   (* Nominal primary pressure (MPa) *)
    rPressureError         : REAL;
    
    bScramLatch            : BOOL := FALSE;
END_VAR

VAR CONSTANT
    MAX_CORE_OUTLET_TEMP   : REAL := 320.0;  (* Deg C, scram limit *)
    MAX_PRIMARY_PRESSURE   : REAL := 17.2;   (* MPa, scram limit *)
    MIN_PRIMARY_PRESSURE   : REAL := 12.5;   (* MPa, scram limit *)
    SCRAM_PUMP_SPEED       : REAL := 450.0;  (* RPM, minimal flow post-scram *)
END_VAR

(* --- Safety & Scram Logic --- *)
IF rCoreOutletTemp_C > MAX_CORE_OUTLET_TEMP THEN
    bAlarm_HighTemp := TRUE;
END_IF;

IF rPrimaryPressure_MPa > MAX_PRIMARY_PRESSURE THEN
    bAlarm_HighPressure := TRUE;
ELSIF rPrimaryPressure_MPa < MIN_PRIMARY_PRESSURE THEN
    bAlarm_LowPressure := TRUE;
END_IF;

IF (bAlarm_HighTemp OR bAlarm_HighPressure OR bAlarm_LowPressure OR bExternalScram) THEN
    bScramLatch := TRUE;
END_IF;

bScramInitiated := bScramLatch;

(* --- Main Coolant Pump Speed Control --- *)
IF bScramLatch THEN
    (* Post-scram decay heat removal mode *)
    rMCPSpeedSetpoint_RPM := SCRAM_PUMP_SPEED;
    rSpeedIntegral := 0.0; (* Reset integral windup *)
ELSE
    (* Normal operations: calculate required flow based on power level *)
    rTargetDeltaT := rReactorPower_Pct * 0.35; (* Empirical thermal curve *)
    rActualDeltaT := rCoreOutletTemp_C - rCoreInletTemp_C;
    
    (* Cascade control: temperature error drives flow demand *)
    rSpeedError := (rActualDeltaT - rTargetDeltaT) * 50.0; 
    
    rSpeedIntegral := rSpeedIntegral + (rSpeedError * rKi_MCP * (tCycleTime_ms / 1000.0));
    
    (* Anti-windup limits *)
    IF rSpeedIntegral > rMaxMCPSpeed THEN
        rSpeedIntegral := rMaxMCPSpeed;
    ELSIF rSpeedIntegral < 0.0 THEN
        rSpeedIntegral := 0.0;
    END_IF;
    
    rMCPSpeedSetpoint_RPM := (rSpeedError * rKp_MCP) + rSpeedIntegral + rMinMCPSpeed;
    
    (* Saturate MCP Output *)
    IF rMCPSpeedSetpoint_RPM > rMaxMCPSpeed THEN
        rMCPSpeedSetpoint_RPM := rMaxMCPSpeed;
    ELSIF rMCPSpeedSetpoint_RPM < rMinMCPSpeed THEN
        rMCPSpeedSetpoint_RPM := rMinMCPSpeed;
    END_IF;
END_IF;

(* --- Pressurizer Control --- *)
rPressureError := rNominalPressure - rPrimaryPressure_MPa;

IF rPressureError > 0.2 THEN
    (* Pressure too low -> activate proportional heaters *)
    rPressurizerHeater_Pct := rPressureError * 150.0; 
    IF rPressurizerHeater_Pct > 100.0 THEN
        rPressurizerHeater_Pct := 100.0;
    END_IF;
    bPressurizerSprayValve := FALSE;
ELSIF rPressureError < -0.2 THEN
    (* Pressure too high -> deactivate heaters, open spray valve *)
    rPressurizerHeater_Pct := 0.0;
    bPressurizerSprayValve := TRUE;
ELSE
    (* Deadband *)
    rPressurizerHeater_Pct := 0.0;
    bPressurizerSprayValve := FALSE;
END_IF;

(* --- Alarm Acknowledgement --- *)
IF bAckAlarms AND NOT (rCoreOutletTemp_C > MAX_CORE_OUTLET_TEMP) THEN
    bAlarm_HighTemp := FALSE;
END_IF;

IF bAckAlarms AND NOT (rPrimaryPressure_MPa > MAX_PRIMARY_PRESSURE) THEN
    bAlarm_HighPressure := FALSE;
END_IF;

IF bAckAlarms AND NOT (rPrimaryPressure_MPa < MIN_PRIMARY_PRESSURE) THEN
    bAlarm_LowPressure := FALSE;
END_IF;

END_FUNCTION_BLOCK
```"""

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": st_code}
    ]
}

file_name = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(file_name, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=4)
    
print(f"Saved to {file_name}")
