import json, uuid, os

prompt = "Invent a highly complex control scenario for Concentrated Solar Power (CSP) Central Tower (e.g., heliostat field sun vector tracking, molten salt receiver thermal gradient limits, and hot/cold salt tank balancing).\nWrite a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."

iec_st_code = """
FUNCTION_BLOCK FB_CSP_Central_Tower_Control
VAR_INPUT
    rSolarAzimuth : REAL; (* Current solar azimuth angle in degrees *)
    rSolarElevation : REAL; (* Current solar elevation angle in degrees *)
    rDNI : REAL; (* Direct Normal Irradiance W/m^2 *)
    
    rReceiverTempTop : REAL; (* Deg C *)
    rReceiverTempMid : REAL;
    rReceiverTempBot : REAL;
    rReceiverTempLimit : REAL := 650.0; (* Max allowable temp *)
    rMaxThermalGradient : REAL := 15.0; (* Max allowable temp diff between sections Deg C *)
    
    rColdTankLevel : REAL; (* % *)
    rHotTankLevel : REAL; (* % *)
    rColdTankTemp : REAL; (* Deg C, nominal 290 *)
    rHotTankTemp : REAL; (* Deg C, nominal 565 *)
    
    bSystemEnable : BOOL;
    bEmergencyScram : BOOL;
END_VAR

VAR_OUTPUT
    rHeliostatTargetAzimuth : REAL;
    rHeliostatTargetElevation : REAL;
    bFocusHeliostats : BOOL;
    bDefocusHeliostats : BOOL;
    
    rMoltenSaltPumpSpeedRef : REAL; (* 0.0 to 100.0 % *)
    rHeatTracePowerRef : REAL; (* 0.0 to 100.0 % *)
    
    bAlarmHighTemp : BOOL;
    bAlarmHighGradient : BOOL;
    bAlarmTankLevelLow : BOOL;
    
    eSystemState : INT; (* 0: Off, 1: Standby, 2: Preheating, 3: Tracking/Heating, 4: Scram *)
END_VAR

VAR
    rThermalGradientTopMid : REAL;
    rThermalGradientMidBot : REAL;
    rMaxGradientCurrent : REAL;
    rAvgReceiverTemp : REAL;
    rTargetPumpSpeed : REAL;
    
    TMR_ScramReset : TON;
    bScramActive : BOOL;
END_VAR

(* Calculate thermal gradients *)
rThermalGradientTopMid := ABS(rReceiverTempTop - rReceiverTempMid);
rThermalGradientMidBot := ABS(rReceiverTempMid - rReceiverTempBot);

IF rThermalGradientTopMid > rThermalGradientMidBot THEN
    rMaxGradientCurrent := rThermalGradientTopMid;
ELSE
    rMaxGradientCurrent := rThermalGradientMidBot;
END_IF;

rAvgReceiverTemp := (rReceiverTempTop + rReceiverTempMid + rReceiverTempBot) / 3.0;

(* Alarms *)
bAlarmHighTemp := (rReceiverTempTop > rReceiverTempLimit) OR (rReceiverTempMid > rReceiverTempLimit) OR (rReceiverTempBot > rReceiverTempLimit);
bAlarmHighGradient := (rMaxGradientCurrent > rMaxThermalGradient);
bAlarmTankLevelLow := (rColdTankLevel < 10.0) OR (rHotTankLevel < 10.0);

(* Emergency Scram Logic *)
IF bEmergencyScram OR bAlarmHighTemp OR (rHotTankLevel > 95.0) THEN
    bScramActive := TRUE;
END_IF;

IF bScramActive THEN
    eSystemState := 4; (* Scram *)
    bFocusHeliostats := FALSE;
    bDefocusHeliostats := TRUE;
    
    IF rHotTankLevel > 95.0 THEN
        rMoltenSaltPumpSpeedRef := 0.0;
    ELSE
        rMoltenSaltPumpSpeedRef := 100.0;
    END_IF;
    
    rHeliostatTargetAzimuth := rSolarAzimuth + 90.0; (* Stow position *)
    rHeliostatTargetElevation := 0.0;
    
    TMR_ScramReset(IN := NOT bEmergencyScram, PT := T#5m);
    IF TMR_ScramReset.Q AND NOT bAlarmHighTemp THEN
        bScramActive := FALSE;
        eSystemState := 1;
    END_IF;

ELSIF NOT bSystemEnable THEN
    eSystemState := 0; (* Off *)
    bFocusHeliostats := FALSE;
    bDefocusHeliostats := TRUE;
    rMoltenSaltPumpSpeedRef := 0.0;
    rHeliostatTargetAzimuth := 0.0;
    rHeliostatTargetElevation := 90.0; (* Face up *)

ELSE
    (* Normal Operation *)
    IF rAvgReceiverTemp < 300.0 THEN
        eSystemState := 2; (* Preheating *)
        bFocusHeliostats := TRUE;
        bDefocusHeliostats := FALSE;
        
        rHeliostatTargetAzimuth := rSolarAzimuth;
        rHeliostatTargetElevation := rSolarElevation; 
        
        rMoltenSaltPumpSpeedRef := 15.0; 
        rHeatTracePowerRef := 100.0;
        
    ELSE
        eSystemState := 3; (* Tracking/Heating *)
        bFocusHeliostats := TRUE;
        bDefocusHeliostats := FALSE;
        rHeliostatTargetAzimuth := rSolarAzimuth; 
        rHeliostatTargetElevation := rSolarElevation;
        rHeatTracePowerRef := 0.0;
        
        rTargetPumpSpeed := (rAvgReceiverTemp - 500.0) * 2.0; 
        
        IF bAlarmHighGradient THEN
             rTargetPumpSpeed := rTargetPumpSpeed + 20.0;
        END_IF;
        
        IF rTargetPumpSpeed > 100.0 THEN
            rMoltenSaltPumpSpeedRef := 100.0;
        ELSIF rTargetPumpSpeed < 20.0 THEN
            rMoltenSaltPumpSpeedRef := 20.0;
        ELSE
            rMoltenSaltPumpSpeedRef := rTargetPumpSpeed;
        END_IF;
        
        IF rDNI < 300.0 THEN
            bFocusHeliostats := FALSE;
            bDefocusHeliostats := TRUE;
            rMoltenSaltPumpSpeedRef := 10.0;
        END_IF;
        
    END_IF;
END_IF;

END_FUNCTION_BLOCK
"""

os.makedirs("data/swarm_raw", exist_ok=True)
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": f"```iec-st\n{iec_st_code}\n```"}]}
file_path = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(file_path, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)
print(f"Saved to {file_path}")
