import os, json, uuid
os.makedirs('data/swarm_raw', exist_ok=True)
code = '''`iec-st
FUNCTION_BLOCK FB_Ecoat_Cathodic_Process
VAR_INPUT
    bStartProcess : BOOL; (* Start the e-coat process *)
    bEmergencyStop : BOOL; (* Emergency stop active *)
    rTankLevel : REAL; (* Main ED tank level in mm *)
    rBathTemperature : REAL; (* ED bath temperature in Celsius *)
    rBathConductivity : REAL; (* Bath conductivity in uS/cm *)
    rConveyorSpeed : REAL; (* Conveyor speed in m/min *)
    rPartSurfaceArea : REAL; (* Estimated surface area of the current body in m2 *)
    bPartInTank : BOOL; (* Proximity sensor for part presence in the ED tank *)
    rUF1_PermeateFlow : REAL; (* Ultrafiltration 1 flow rate L/min *)
    rUF2_PermeateFlow : REAL; (* Ultrafiltration 2 flow rate L/min *)
    bRO_RinseActive : BOOL; (* Reverse Osmosis rinse zone active flag *)
END_VAR

VAR_OUTPUT
    bRectifierEnable : BOOL; (* Enable rectifier for voltage application *)
    rRectifierVoltageTarget : REAL; (* Voltage setpoint for the rectifier *)
    rRectifierCurrentLimit : REAL; (* Current limit based on surface area *)
    bUF1_PumpEnable : BOOL; (* Enable Ultrafiltration pump 1 *)
    bUF2_PumpEnable : BOOL; (* Enable Ultrafiltration pump 2 *)
    bRO_ZoneIsolationValve : BOOL; (* Valve to isolate RO rinse zone *)
    bChillerEnable : BOOL; (* Enable bath chiller *)
    bHeaterEnable : BOOL; (* Enable bath heater *)
    iProcessState : INT; (* Current state of the electrodeposition process *)
    bAlarmActive : BOOL; (* General alarm flag *)
    sAlarmMessage : STRING(80); (* Detailed alarm message *)
END_VAR

VAR
    rVoltageRampRate : REAL := 15.0; (* V/s ramp rate *)
    rMaxVoltage : REAL := 350.0; (* Maximum coating voltage *)
    rTargetCoatingVoltage : REAL;
    rCurrentVoltage : REAL := 0.0;
    
    tProcessTimer : TON;
    tDwellTimer : TON;
    
    (* State Machine Constants *)
    STATE_IDLE : INT := 0;
    STATE_PRE_CHECK : INT := 10;
    STATE_PART_ENTRY : INT := 20;
    STATE_VOLTAGE_RAMP_UP : INT := 30;
    STATE_COATING_DWELL : INT := 40;
    STATE_VOLTAGE_RAMP_DOWN : INT := 50;
    STATE_PART_EXIT : INT := 60;
    STATE_FAULT : INT := 99;
    
    rTempSetpoint : REAL := 28.0; (* 28 Celsius target *)
    rTempHysteresis : REAL := 1.0;
END_VAR

(* E-Coat Control Logic *)

IF bEmergencyStop THEN
    iProcessState := STATE_FAULT;
    sAlarmMessage := 'EMERGENCY STOP TRIGGERED';
END_IF;

(* Temperature Control *)
IF rBathTemperature > (rTempSetpoint + rTempHysteresis) THEN
    bChillerEnable := TRUE;
    bHeaterEnable := FALSE;
ELSIF rBathTemperature < (rTempSetpoint - rTempHysteresis) THEN
    bChillerEnable := FALSE;
    bHeaterEnable := TRUE;
ELSE
    bChillerEnable := FALSE;
    bHeaterEnable := FALSE;
END_IF;

(* Ultrafiltration Cascade Control *)
IF iProcessState <> STATE_FAULT AND iProcessState <> STATE_IDLE THEN
    (* Maintain permeate flow *)
    bUF1_PumpEnable := (rUF1_PermeateFlow < 50.0); 
    bUF2_PumpEnable := (rUF1_PermeateFlow > 45.0) AND (rUF2_PermeateFlow < 50.0);
ELSE
    bUF1_PumpEnable := FALSE;
    bUF2_PumpEnable := FALSE;
END_IF;

(* RO Rinse Zone Isolation *)
IF bRO_RinseActive AND NOT bPartInTank THEN
    bRO_ZoneIsolationValve := TRUE; (* Isolate to save RO water *)
ELSE
    bRO_ZoneIsolationValve := FALSE;
END_IF;

(* Main State Machine *)
CASE iProcessState OF
    STATE_IDLE:
        bRectifierEnable := FALSE;
        rRectifierVoltageTarget := 0.0;
        rCurrentVoltage := 0.0;
        bAlarmActive := FALSE;
        
        IF bStartProcess AND NOT bEmergencyStop THEN
            iProcessState := STATE_PRE_CHECK;
        END_IF;
        
    STATE_PRE_CHECK:
        IF rTankLevel < 1500.0 THEN
            iProcessState := STATE_FAULT;
            sAlarmMessage := 'TANK LEVEL TOO LOW';
        ELSIF rBathConductivity < 1000.0 OR rBathConductivity > 2000.0 THEN
            iProcessState := STATE_FAULT;
            sAlarmMessage := 'CONDUCTIVITY OUT OF RANGE';
        ELSE
            iProcessState := STATE_PART_ENTRY;
        END_IF;
        
    STATE_PART_ENTRY:
        IF bPartInTank THEN
            (* Calculate target voltage based on conveyor speed and area *)
            rTargetCoatingVoltage := rMaxVoltage * (rConveyorSpeed / 2.0);
            IF rTargetCoatingVoltage > rMaxVoltage THEN
                rTargetCoatingVoltage := rMaxVoltage;
            END_IF;
            
            (* Set current limit based on rule of thumb: 3A per m2 *)
            rRectifierCurrentLimit := rPartSurfaceArea * 3.0;
            
            iProcessState := STATE_VOLTAGE_RAMP_UP;
        END_IF;
        
    STATE_VOLTAGE_RAMP_UP:
        bRectifierEnable := TRUE;
        (* In a real PLC this would be tied to a cycle time, simplifying for FB: *)
        rCurrentVoltage := rCurrentVoltage + rVoltageRampRate;
        
        IF rCurrentVoltage >= rTargetCoatingVoltage THEN
            rCurrentVoltage := rTargetCoatingVoltage;
            tDwellTimer(IN := FALSE); (* Reset timer *)
            iProcessState := STATE_COATING_DWELL;
        END_IF;
        rRectifierVoltageTarget := rCurrentVoltage;
        
    STATE_COATING_DWELL:
        bRectifierEnable := TRUE;
        rRectifierVoltageTarget := rTargetCoatingVoltage;
        
        tDwellTimer(IN := TRUE, PT := T#120S);
        
        IF tDwellTimer.Q THEN
            tDwellTimer(IN := FALSE);
            iProcessState := STATE_VOLTAGE_RAMP_DOWN;
        END_IF;
        
    STATE_VOLTAGE_RAMP_DOWN:
        rCurrentVoltage := rCurrentVoltage - (rVoltageRampRate * 2.0); (* Faster ramp down *)
        IF rCurrentVoltage <= 0.0 THEN
            rCurrentVoltage := 0.0;
            bRectifierEnable := FALSE;
            iProcessState := STATE_PART_EXIT;
        END_IF;
        rRectifierVoltageTarget := rCurrentVoltage;
        
    STATE_PART_EXIT:
        IF NOT bPartInTank THEN
            iProcessState := STATE_IDLE;
        END_IF;
        
    STATE_FAULT:
        bRectifierEnable := FALSE;
        rRectifierVoltageTarget := 0.0;
        bUF1_PumpEnable := FALSE;
        bUF2_PumpEnable := FALSE;
        bAlarmActive := TRUE;
        
        IF NOT bEmergencyStop AND bStartProcess THEN
            (* Manual reset attempt *)
            iProcessState := STATE_IDLE;
        END_IF;
        
    ELSE
        iProcessState := STATE_FAULT;
        sAlarmMessage := 'INVALID STATE';
END_CASE;

END_FUNCTION_BLOCK
`'''
record = {"messages": [{"role": "user", "content": "You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.\nYour specific domain is: Automated E-Coat (Electrodeposition) Line.\nTask: Invent a highly complex control scenario for this domain (e.g., cathodic electrodeposition voltage ramping, ultrafiltration permeate cascades, and reverse osmosis rinse zone isolation).\nWrite a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."}, {"role": "assistant", "content": code}]}
with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
    json.dump(record, f)
print("File generated successfully.")
