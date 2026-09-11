import json, uuid, os

# Ensure dir exists
os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Industrial Coffee Roasting Plant.
Task: Invent a highly complex control scenario for this domain (e.g., proportional gas burner roasting profiles, drum rotation kinematics, and chaff cyclone extraction loops).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O.
"""

code = """```iec-st
FUNCTION_BLOCK FB_AdvancedCoffeeRoaster
VAR_INPUT
    bStartRoast : BOOL; (* Initiate roast cycle *)
    bEmergencyStop : BOOL; (* E-Stop condition *)
    rTargetTemperature : REAL; (* Desired end roast temperature [C] *)
    rDrumSpeedSetPoint : REAL; (* Target drum speed [RPM] *)
    iProfileType : INT; (* 1: Light, 2: Medium, 3: Dark, 4: Espresso *)
    rAirflowRateSetPoint : REAL; (* Required airflow [m3/h] *)
    rBeanTemperatureSensor : REAL; (* Measured bean mass temp [C] *)
    rExhaustTemperatureSensor : REAL; (* Measured exhaust temp [C] *)
    rAmbientTemperature : REAL; (* Ambient room temp [C] *)
    bChargeDoorsClosed : BOOL; (* Hopper drop doors status *)
    bDischargeDoorsClosed : BOOL; (* Cooling tray doors status *)
    bIgnitionConfirmed : BOOL; (* Gas burner flame sense *)
END_VAR

VAR_OUTPUT
    rBurnerValveOutput : REAL; (* Proportional gas valve command 0-100% *)
    rDrumMotorVFD : REAL; (* Drum VFD command 0-100% *)
    rExhaustFanVFD : REAL; (* Chaff cyclone exhaust fan 0-100% *)
    bIgniterRelay : BOOL; (* Burner spark ignition relay *)
    bGasSafetyValve : BOOL; (* Main gas line solenoid *)
    bCoolingAgitator : BOOL; (* Cooling tray mixing arms *)
    bCoolingFan : BOOL; (* Cooling tray fan *)
    sRoastStatusMessage : STRING(50); (* Current state machine step text *)
    bRoastComplete : BOOL; (* True when drop temp is reached *)
    bAlarmActive : BOOL; (* True if any interlock fails *)
END_VAR

VAR
    iState : INT := 0; (* State machine tracker *)
    rPID_Kp : REAL := 2.5; (* Temp control proportional gain *)
    rPID_Ki : REAL := 0.1; (* Temp control integral gain *)
    rPID_Kd : REAL := 0.5; (* Temp control derivative gain *)
    rTempError : REAL := 0.0;
    rTempIntegral : REAL := 0.0;
    rTempDerivative : REAL := 0.0;
    rLastTempError : REAL := 0.0;
    rRateOfRise : REAL := 0.0; (* ROR: Degrees per minute *)
    tRoastTimer : TON;
    tCoolingTimer : TON;
    rMaxTempLimit : REAL := 250.0; (* Safety cutoff [C] *)
    bPreheatComplete : BOOL := FALSE;
    bFirstCrackDetected : BOOL := FALSE;
    rFirstCrackTemp : REAL;
END_VAR

(* Implementation *)
IF bEmergencyStop THEN
    rBurnerValveOutput := 0.0;
    bGasSafetyValve := FALSE;
    bIgniterRelay := FALSE;
    rDrumMotorVFD := 0.0;
    rExhaustFanVFD := 100.0; (* Evacuate smoke *)
    bCoolingAgitator := FALSE;
    bCoolingFan := FALSE;
    iState := 999; (* E-Stop State *)
    sRoastStatusMessage := 'EMERGENCY STOP ACTIVE';
    bAlarmActive := TRUE;
    RETURN;
END_IF;

(* Rate of Rise Calculation (Simplified for PLC cycle) *)
rRateOfRise := rBeanTemperatureSensor - rLastTempError; (* Typically filtered over a minute *)

CASE iState OF
    0: (* Idle / Standby *)
        sRoastStatusMessage := 'SYSTEM READY';
        bGasSafetyValve := FALSE;
        rBurnerValveOutput := 0.0;
        rDrumMotorVFD := 10.0; (* Keep drum turning slowly to prevent warping *)
        rExhaustFanVFD := 20.0;
        IF bStartRoast AND bChargeDoorsClosed AND bDischargeDoorsClosed THEN
            iState := 10;
        END_IF;

    10: (* Pre-heat phase *)
        sRoastStatusMessage := 'PREHEATING';
        bGasSafetyValve := TRUE;
        bIgniterRelay := NOT bIgnitionConfirmed;
        rDrumMotorVFD := rDrumSpeedSetPoint;
        rExhaustFanVFD := rAirflowRateSetPoint;
        IF bIgnitionConfirmed THEN
            rBurnerValveOutput := 50.0; (* Initial preheat burner power *)
        END_IF;
        IF rAmbientTemperature > 200.0 THEN (* Assuming drum ambient probe *)
            bPreheatComplete := TRUE;
            iState := 20;
        END_IF;

    20: (* Charge (Drop beans) *)
        sRoastStatusMessage := 'DROP BEANS NOW';
        rBurnerValveOutput := 0.0; (* Turn down heat during drop to prevent scorching *)
        IF NOT bChargeDoorsClosed THEN
            iState := 30;
        END_IF;

    30: (* Turning Point / Drying Phase *)
        sRoastStatusMessage := 'DRYING PHASE';
        rBurnerValveOutput := 30.0; (* Gradual heat application *)
        IF rBeanTemperatureSensor > 150.0 THEN
            iState := 40;
        END_IF;

    40: (* Maillard Reaction Phase *)
        sRoastStatusMessage := 'MAILLARD PHASE';
        (* Simple PID implementation for target trajectory *)
        rTempError := rTargetTemperature - rBeanTemperatureSensor;
        rTempIntegral := rTempIntegral + rTempError;
        rTempDerivative := rTempError - rLastTempError;
        rBurnerValveOutput := (rPID_Kp * rTempError) + (rPID_Ki * rTempIntegral) + (rPID_Kd * rTempDerivative);
        
        (* Clamp burner output *)
        IF rBurnerValveOutput > 100.0 THEN rBurnerValveOutput := 100.0; END_IF;
        IF rBurnerValveOutput < 10.0 THEN rBurnerValveOutput := 10.0; END_IF;
        
        IF rBeanTemperatureSensor >= 195.0 THEN (* First crack onset approx *)
            bFirstCrackDetected := TRUE;
            rFirstCrackTemp := rBeanTemperatureSensor;
            iState := 50;
        END_IF;

    50: (* Development Phase *)
        sRoastStatusMessage := 'DEVELOPMENT PHASE';
        (* Reduce heat to prevent baked flavors, increase airflow *)
        rBurnerValveOutput := rBurnerValveOutput * 0.5; 
        rExhaustFanVFD := rExhaustFanVFD + 10.0; 
        
        IF rBeanTemperatureSensor >= rTargetTemperature THEN
            iState := 60;
        END_IF;

    60: (* Drop and Cool *)
        sRoastStatusMessage := 'ROAST COMPLETE - DROPPING';
        bGasSafetyValve := FALSE;
        rBurnerValveOutput := 0.0;
        bRoastComplete := TRUE;
        
        IF NOT bDischargeDoorsClosed THEN
            bCoolingFan := TRUE;
            bCoolingAgitator := TRUE;
            tCoolingTimer(IN:=TRUE, PT:=T#4M);
            IF tCoolingTimer.Q THEN
                iState := 0; (* Reset for next batch *)
                bRoastComplete := FALSE;
                tCoolingTimer(IN:=FALSE);
                bCoolingFan := FALSE;
                bCoolingAgitator := FALSE;
            END_IF;
        END_IF;

    999: (* Fault handling *)
        (* Needs manual reset *)
        IF NOT bEmergencyStop THEN
            bAlarmActive := FALSE;
            iState := 0;
        END_IF;
END_CASE;

rLastTempError := rTempError;

(* Safety Overrides *)
IF rBeanTemperatureSensor > rMaxTempLimit OR rExhaustTemperatureSensor > (rMaxTempLimit + 50.0) THEN
    bGasSafetyValve := FALSE;
    rBurnerValveOutput := 0.0;
    bAlarmActive := TRUE;
    sRoastStatusMessage := 'ALARM: OVERTEMP';
    iState := 999;
END_IF;
END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f)

print(f"Saved to {filename}")
