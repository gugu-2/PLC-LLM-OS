import json, uuid, os

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Dry Pasta Manufacturing Line.
Task: Invent a highly complex control scenario for this domain (e.g., semolina hydration vacuum mixing, Teflon die extrusion pressure, and multi-tier climate-controlled drying profiles).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."""

code = """FUNCTION_BLOCK FB_DryPastaProductionLine
(* 
   Advanced Dry Pasta Manufacturing Line Controller 
   Handles semolina hydration vacuum mixing, Teflon die extrusion pressure, 
   and multi-tier climate-controlled drying profiles.
*)
VAR_INPUT
    bEnableLine : BOOL; (* Start production line *)
    rSemolinaFeedRate : REAL; (* Target Semolina feed rate in kg/h *)
    rWaterFlowTarget : REAL; (* Target hydration water flow in L/h *)
    rVacuumTarget : REAL; (* Target vacuum pressure in mixer (mbar) *)
    rExtrusionPressTarget : REAL; (* Target extrusion die pressure (bar) *)
    rExtruderTempTarget : REAL; (* Target extrusion temperature (Celsius) *)
    rDryingZone1Temp : REAL; (* Phase 1 Drying Temp *)
    rDryingZone1Hum : REAL; (* Phase 1 Humidity *)
    rDryingZone2Temp : REAL; (* Phase 2 Drying Temp *)
    rDryingZone2Hum : REAL; (* Phase 2 Humidity *)
    rDryingZone3Temp : REAL; (* Phase 3 Drying Temp *)
    rDryingZone3Hum : REAL; (* Phase 3 Humidity *)
    bEmergencyStop : BOOL; (* Global Emergency Stop *)
END_VAR

VAR_OUTPUT
    bMixingReady : BOOL;
    bExtrusionActive : BOOL;
    bDryingActive : BOOL;
    rActualExtrusionPress : REAL;
    rActualExtruderTemp : REAL;
    iErrorCode : DINT;
    bAlarmActive : BOOL;
END_VAR

VAR
    (* State Machine *)
    iState : INT := 0; 
    
    (* Mixing Control Loop *)
    rWaterFlowProcessValue : REAL;
    rWaterValveControl : REAL;
    rMixerSpeed : REAL;
    rVacuumLevel : REAL;
    
    (* Extrusion Control Loop *)
    rExtruderMotorSpeed : REAL;
    rDieTemperature : REAL;
    rKnifeSpeed : REAL;
    
    (* Timers *)
    tMixTimer : TON;
    tExtrusionStartup : TON;
    tDryingPhase1 : TON;
    tDryingPhase2 : TON;
    
    (* Drying Profiler variables *)
    rCurrentDryingTemp : REAL;
    rCurrentDryingHum : REAL;
    iDryingPhase : INT := 0;
END_VAR

(* -----------------------------------------------------------------------------
   Main Implementation
----------------------------------------------------------------------------- *)

(* Check for Global Emergency Stop before processing any state logic *)
IF bEmergencyStop THEN
    iState := 99;
    iErrorCode := 16#FFFF; (* Critical Fault Code *)
    bAlarmActive := TRUE;
    bMixingReady := FALSE;
    bExtrusionActive := FALSE;
    bDryingActive := FALSE;
    rWaterValveControl := 0.0;
    rMixerSpeed := 0.0;
    rExtruderMotorSpeed := 0.0;
    rKnifeSpeed := 0.0;
    RETURN;
END_IF;

CASE iState OF
    0: (* Idle State - Waiting for Start Command *)
        IF bEnableLine THEN
            iState := 10;
            iErrorCode := 0;
            bAlarmActive := FALSE;
            iDryingPhase := 0;
        END_IF;
        
    10: (* Hydration & Vacuum Mixing Phase *)
        (* Emulate Water flow control PI loop *)
        IF rWaterFlowProcessValue < rWaterFlowTarget THEN
            rWaterValveControl := rWaterValveControl + 1.25;
            rWaterFlowProcessValue := rWaterFlowProcessValue + 2.0;
        ELSE
            rWaterValveControl := rWaterValveControl - 0.75;
            rWaterFlowProcessValue := rWaterFlowProcessValue - 1.0;
        END_IF;
        
        (* Regulate Vacuum level in the mixing chamber to prevent oxidation *)
        IF rVacuumLevel > rVacuumTarget THEN
            rVacuumLevel := rVacuumLevel - 5.0; (* Pump down *)
        END_IF;
        
        rMixerSpeed := 1500.0; (* Standard hydration RPM *)
        
        tMixTimer(IN := TRUE, PT := T#10M);
        IF tMixTimer.Q THEN
            bMixingReady := TRUE;
            iState := 20;
            tMixTimer(IN := FALSE);
        END_IF;
        
    20: (* Extrusion Phase through Teflon Die *)
        bExtrusionActive := TRUE;
        
        (* Pressure Control Loop: Regulate auger speed to maintain die pressure *)
        IF rActualExtrusionPress < rExtrusionPressTarget THEN
            rExtruderMotorSpeed := LIMIT(0.0, rExtruderMotorSpeed + 0.5, 100.0);
            rActualExtrusionPress := rActualExtrusionPress + 1.2;
        ELSE
            rExtruderMotorSpeed := LIMIT(0.0, rExtruderMotorSpeed - 0.2, 100.0);
            rActualExtrusionPress := rActualExtrusionPress - 0.5;
        END_IF;
        
        (* Temperature Control Loop for the extrusion barrel *)
        IF rActualExtruderTemp < rExtruderTempTarget THEN
            rDieTemperature := rDieTemperature + 1.5;
            rActualExtruderTemp := rActualExtruderTemp + 0.5;
        END_IF;
        
        (* Cutter knife sync based on extrusion pressure to maintain pasta length *)
        rKnifeSpeed := rActualExtrusionPress * 0.5; 
        
        tExtrusionStartup(IN := TRUE, PT := T#5M);
        IF tExtrusionStartup.Q THEN
            iState := 30;
            tExtrusionStartup(IN := FALSE);
        END_IF;
        
    30: (* Multi-Tier Climate Controlled Drying - Profiling *)
        bDryingActive := TRUE;
        
        (* Advanced multi-phase drying logic to prevent pasta cracking (checking) *)
        CASE iDryingPhase OF
            0: (* Pre-drying (Incartamento) - High Temp, Low Humidity to form crust *)
                rCurrentDryingTemp := rDryingZone1Temp;
                rCurrentDryingHum := rDryingZone1Hum;
                tDryingPhase1(IN := TRUE, PT := T#45M);
                IF tDryingPhase1.Q THEN
                    iDryingPhase := 1;
                    tDryingPhase1(IN := FALSE);
                END_IF;
                
            1: (* Main Drying - Sweating Phase - Moderate Temp, High Humidity *)
                rCurrentDryingTemp := rDryingZone2Temp;
                rCurrentDryingHum := rDryingZone2Hum;
                tDryingPhase2(IN := TRUE, PT := T#120M);
                IF tDryingPhase2.Q THEN
                    iDryingPhase := 2;
                    tDryingPhase2(IN := FALSE);
                END_IF;
                
            2: (* Stabilization & Cooling - Ambient Temp, Controlled Humidity *)
                rCurrentDryingTemp := rDryingZone3Temp;
                rCurrentDryingHum := rDryingZone3Hum;
                
                (* End of complete cycle *)
                IF NOT bEnableLine THEN
                    iState := 0;
                    bMixingReady := FALSE;
                    bExtrusionActive := FALSE;
                    bDryingActive := FALSE;
                    iDryingPhase := 0;
                END_IF;
        END_CASE;
        
    99: (* Fault Handling State *)
        bAlarmActive := TRUE;
        IF NOT bEmergencyStop THEN
            iState := 0; (* Auto-recover if E-stop is physically cleared, requires operator reset *)
            iErrorCode := 0;
        END_IF;
END_CASE;
END_FUNCTION_BLOCK"""

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": f"```iec-st\n{code}\n```"}
    ]
}

with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)
