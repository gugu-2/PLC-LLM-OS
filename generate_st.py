import os, json, uuid
os.makedirs('data/swarm_raw', exist_ok=True)
prompt = "You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.\nYour specific domain is: Lead-Acid Battery Plate Curing.\nTask: Invent a highly complex control scenario for this domain (e.g., hydroset chamber humidity/temperature cascades, grid pasting thickness feedback, and exothermic reaction cooling logic).\nWrite a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."

st_code = """```iec-st
FUNCTION_BLOCK FB_BatteryPlateCuringController
TITLE = 'Lead-Acid Battery Plate Curing and Hydroset Controller'
VERSION : '1.5'

(*
  This function block handles the complex multi-phase curing process
  for lead-acid battery plates, specifically managing the hydroset chamber
  humidity/temperature cascades, grid pasting thickness feedback compensation,
  and exothermic reaction cooling logic to prevent plate thermal runaway.
*)

VAR_INPUT
    bEnableProcess       : BOOL;   (* Start the curing process *)
    bEmergencyStop       : BOOL;   (* Safety stop *)
    rActualTemp          : REAL;   (* Chamber temperature feedback (Deg C) *)
    rActualHumidity      : REAL;   (* Chamber Relative Humidity (%) *)
    rPlateSurfaceTemp    : REAL;   (* IR sensor for exothermic reaction detection (Deg C) *)
    rPasteThickness      : REAL;   (* Feedback from inline thickness gauge (mm) *)
    rTargetThickness     : REAL;   (* Setpoint for plate thickness (mm) *)
    rBaseTempSetpoint    : REAL;   (* Base hydroset temp setpoint (Deg C) *)
    rBaseHumidSetpoint   : REAL;   (* Base hydroset humidity setpoint (%) *)
    rExoDeltaT_Limit     : REAL;   (* Maximum allowed delta between surface and chamber temp *)
END_VAR

VAR_OUTPUT
    bHeaterEnable        : BOOL;   (* Chamber heater control *)
    rHeaterCV            : REAL;   (* Heater control value 0-100% *)
    bSteamValveEnable    : BOOL;   (* Steam injection valve *)
    rSteamValveCV        : REAL;   (* Steam valve control value 0-100% *)
    bCoolingFanEnable    : BOOL;   (* Exothermic cooling fan *)
    rCoolingFanCV        : REAL;   (* Fan speed control 0-100% *)
    iCurrentPhase        : INT;    (* 0=Idle, 1=Flash Dry, 2=Hydroset, 3=Final Dry, 4=Cooling *)
    bProcessComplete     : BOOL;
    bAlarmThermalRunaway : BOOL;
    rCalculatedTempSP    : REAL;
    rCalculatedHumidSP   : REAL;
END_VAR

VAR
    rThicknessOffset     : REAL;
    rTempError           : REAL;
    rHumidError          : REAL;
    rTempIntegral        : REAL;
    rHumidIntegral       : REAL;
    tPhaseTimer          : TON;
    rKp_Temp             : REAL := 2.5;
    rKi_Temp             : REAL := 0.1;
    rKp_Humid            : REAL := 1.8;
    rKi_Humid            : REAL := 0.05;
    rExoDelta            : REAL;
END_VAR

(* Check for Emergency Stop *)
IF bEmergencyStop THEN
    bHeaterEnable        := FALSE;
    rHeaterCV            := 0.0;
    bSteamValveEnable    := FALSE;
    rSteamValveCV        := 0.0;
    bCoolingFanEnable    := TRUE;
    rCoolingFanCV        := 100.0;
    iCurrentPhase        := 0;
    bProcessComplete     := FALSE;
    RETURN;
END_IF;

(* Process Logic Enable *)
IF NOT bEnableProcess THEN
    iCurrentPhase := 0;
    bProcessComplete := FALSE;
    bHeaterEnable := FALSE;
    bSteamValveEnable := FALSE;
    bCoolingFanEnable := FALSE;
    rHeaterCV := 0.0;
    rSteamValveCV := 0.0;
    rCoolingFanCV := 0.0;
    tPhaseTimer(IN := FALSE);
    RETURN;
END_IF;

(* Thickness Feedback Compensation: Thicker plates require higher temp/humidity *)
rThicknessOffset := (rPasteThickness - rTargetThickness) * 1.5;

(* Phase Management Timer *)
tPhaseTimer(IN := bEnableProcess, PT := T#72h);

IF tPhaseTimer.ET < T#1h THEN
    iCurrentPhase := 1; (* Flash Dry *)
    rCalculatedTempSP := 65.0 + rThicknessOffset;
    rCalculatedHumidSP := 40.0;
ELSIF tPhaseTimer.ET < T#24h THEN
    iCurrentPhase := 2; (* Hydroset Phase *)
    rCalculatedTempSP := rBaseTempSetpoint + rThicknessOffset;
    rCalculatedHumidSP := rBaseHumidSetpoint + (rThicknessOffset * 2.0);
ELSIF tPhaseTimer.ET < T#70h THEN
    iCurrentPhase := 3; (* Final Dry Phase *)
    rCalculatedTempSP := 55.0;
    rCalculatedHumidSP := 15.0;
ELSIF tPhaseTimer.ET < T#72h THEN
    iCurrentPhase := 4; (* Cooling Phase *)
    rCalculatedTempSP := 25.0;
    rCalculatedHumidSP := 0.0;
ELSE
    iCurrentPhase := 5; (* Done *)
    bProcessComplete := TRUE;
END_IF;

(* Exothermic Reaction Cooling Logic *)
rExoDelta := rPlateSurfaceTemp - rActualTemp;
IF rExoDelta > rExoDeltaT_Limit THEN
    bAlarmThermalRunaway := TRUE;
    bCoolingFanEnable := TRUE;
    rCoolingFanCV := 100.0;
    (* Override Heater *)
    rHeaterCV := 0.0;
    bHeaterEnable := FALSE;
ELSE
    bAlarmThermalRunaway := FALSE;
    (* Standard Cooling Fan control for dehumidification/circulation *)
    bCoolingFanEnable := (iCurrentPhase = 4);
    rCoolingFanCV := SEL(iCurrentPhase = 4, 20.0, 80.0);
END_IF;

(* Cascaded PID for Temperature *)
IF NOT bAlarmThermalRunaway THEN
    rTempError := rCalculatedTempSP - rActualTemp;
    rTempIntegral := rTempIntegral + (rTempError * 0.1);
    IF rTempIntegral > 100.0 THEN rTempIntegral := 100.0; END_IF;
    IF rTempIntegral < 0.0 THEN rTempIntegral := 0.0; END_IF;
    
    rHeaterCV := (rKp_Temp * rTempError) + (rKi_Temp * rTempIntegral);
    
    IF rHeaterCV > 100.0 THEN rHeaterCV := 100.0; END_IF;
    IF rHeaterCV < 0.0 THEN rHeaterCV := 0.0; END_IF;
    
    bHeaterEnable := (rHeaterCV > 5.0);
END_IF;

(* Cascaded PID for Humidity *)
rHumidError := rCalculatedHumidSP - rActualHumidity;
rHumidIntegral := rHumidIntegral + (rHumidError * 0.1);
IF rHumidIntegral > 100.0 THEN rHumidIntegral := 100.0; END_IF;
IF rHumidIntegral < 0.0 THEN rHumidIntegral := 0.0; END_IF;

rSteamValveCV := (rKp_Humid * rHumidError) + (rKi_Humid * rHumidIntegral);

IF rSteamValveCV > 100.0 THEN rSteamValveCV := 100.0; END_IF;
IF rSteamValveCV < 0.0 THEN rSteamValveCV := 0.0; END_IF;

(* Do not inject steam during cooling *)
IF iCurrentPhase = 4 OR iCurrentPhase = 5 THEN
    rSteamValveCV := 0.0;
END_IF;

bSteamValveEnable := (rSteamValveCV > 5.0);

END_FUNCTION_BLOCK
```"""

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": st_code}
    ]
}
filepath = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filepath, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)

print("SUCCESS: Wrote JSON to", filepath)

# Also append to synthetic_generation_v3_enterprise.jsonl
os.makedirs('data', exist_ok=True)
with open("data/synthetic_generation_v3_enterprise.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\n")
