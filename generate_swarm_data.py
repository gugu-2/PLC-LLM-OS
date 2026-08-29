import os, json, uuid
os.makedirs('data/swarm_raw', exist_ok=True)
os.makedirs('data', exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Industrial Coffee Roaster.
Task: Invent a highly complex control scenario for this domain (e.g., PID drum temperature roast profiling, chaff cyclone extraction pressure, and emergency water quenching cascades).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."""

st_code = """```iec-st
FUNCTION_BLOCK FB_CoffeeRoasterControl
VAR_INPUT
    bEnable : BOOL; // System enable
    bStartRoast : BOOL; // Start roasting cycle
    bEStop : BOOL; // Emergency stop
    rDrumTempActual : REAL; // Actual drum temperature (C)
    rExhaustTempActual : REAL; // Actual exhaust temperature (C)
    rCyclonePressure : REAL; // Cyclone extraction pressure (mbar)
    rBeanTempActual : REAL; // Actual bean temperature (C)
    iRecipeID : INT; // Current recipe profile ID
    rGasPressure : REAL; // Inlet gas pressure (mbar)
END_VAR

VAR_OUTPUT
    bBurnerIgnition : BOOL; // Command to ignite burner
    rGasValvePos : REAL; // Gas proportional valve (0-100%)
    rDrumMotorSpeed : REAL; // Drum motor VFD speed (0-100%)
    rExhaustFanSpeed : REAL; // Exhaust fan VFD speed (0-100%)
    bCoolingTrayFan : BOOL; // Cooling tray fan
    bCoolingTrayStirrer : BOOL; // Cooling tray stirrer
    bQuenchValve : BOOL; // Emergency water quench valve
    bChaffRotaryValve : BOOL; // Chaff collection rotary valve
    eSystemState : INT; // Current state of the roasting system
    bAlarmActive : BOOL; // Any alarm active
END_VAR

VAR
    // PID for Drum Temperature
    PID_DrumTemp : PID;
    rDrumTempSetpoint : REAL;
    
    // PID for Cyclone Pressure
    PID_Cyclone : PID;
    rCyclonePressureSP : REAL := -12.5; // Target mbar
    
    // Timers
    TMR_RoastDuration : TON;
    TMR_Ignition : TON;
    TMR_QuenchDuration : TON;
    TMR_CoolingDuration : TON;
    
    // Internal States
    STATE_IDLE : INT := 0;
    STATE_PURGE : INT := 10;
    STATE_IGNITION : INT := 20;
    STATE_PREHEAT : INT := 30;
    STATE_CHARGE : INT := 40;
    STATE_DRYING : INT := 50;
    STATE_MAILLARD : INT := 60;
    STATE_FIRST_CRACK : INT := 70;
    STATE_DEVELOPMENT : INT := 80;
    STATE_DROP : INT := 90;
    STATE_COOLING : INT := 100;
    STATE_QUENCH : INT := 999;
    
    iCurrentState : INT := 0;
    
    // Alarms and Limits
    rMaxDrumTemp : REAL := 280.0;
    rMaxBeanTemp : REAL := 250.0;
    rMinGasPressure : REAL := 20.0;
    
    bOverTempAlarm : BOOL;
    bGasPressureAlarm : BOOL;
END_VAR

// Alarm Monitoring
bOverTempAlarm := (rDrumTempActual > rMaxDrumTemp) OR (rBeanTempActual > rMaxBeanTemp);
bGasPressureAlarm := rGasPressure < rMinGasPressure;
bAlarmActive := bOverTempAlarm OR bGasPressureAlarm OR bEStop;

IF bAlarmActive OR bEStop THEN
    iCurrentState := STATE_QUENCH;
END_IF;

// State Machine
CASE iCurrentState OF
    STATE_IDLE:
        bBurnerIgnition := FALSE;
        rGasValvePos := 0.0;
        rDrumMotorSpeed := 0.0;
        rExhaustFanSpeed := 0.0;
        bCoolingTrayFan := FALSE;
        bCoolingTrayStirrer := FALSE;
        bQuenchValve := FALSE;
        bChaffRotaryValve := FALSE;
        
        IF bEnable AND bStartRoast AND NOT bAlarmActive THEN
            iCurrentState := STATE_PURGE;
            TMR_Ignition(IN := FALSE);
        END_IF;
        
    STATE_PURGE:
        rExhaustFanSpeed := 100.0;
        rDrumMotorSpeed := 50.0;
        TMR_Ignition(IN := TRUE, PT := T#30s);
        
        IF TMR_Ignition.Q THEN
            iCurrentState := STATE_IGNITION;
            TMR_Ignition(IN := FALSE);
        END_IF;
        
    STATE_IGNITION:
        bBurnerIgnition := TRUE;
        rGasValvePos := 20.0; // Low fire
        TMR_Ignition(IN := TRUE, PT := T#5s);
        
        IF TMR_Ignition.Q THEN
            iCurrentState := STATE_PREHEAT;
        END_IF;
        
    STATE_PREHEAT:
        // Ramp to target charge temp based on recipe
        rDrumTempSetpoint := 200.0; // Example static, would be recipe driven
        PID_DrumTemp(ACT := rDrumTempActual, SET := rDrumTempSetpoint, KP := 2.5, TN := T#10s, TV := T#2s);
        rGasValvePos := PID_DrumTemp.OUT;
        
        IF rDrumTempActual >= 195.0 THEN
            iCurrentState := STATE_CHARGE;
        END_IF;
        
    STATE_CHARGE:
        // Wait for beans to drop into drum
        // Simulating charge phase
        rGasValvePos := 0.0; // Cut gas briefly
        iCurrentState := STATE_DRYING;
        TMR_RoastDuration(IN := FALSE);
        
    STATE_DRYING:
        TMR_RoastDuration(IN := TRUE, PT := T#20m);
        rDrumTempSetpoint := 150.0;
        PID_DrumTemp(ACT := rBeanTempActual, SET := rDrumTempSetpoint, KP := 1.8, TN := T#15s);
        rGasValvePos := PID_DrumTemp.OUT;
        
        IF rBeanTempActual >= 150.0 THEN
            iCurrentState := STATE_MAILLARD;
        END_IF;
        
    STATE_MAILLARD:
        rDrumTempSetpoint := 200.0;
        PID_DrumTemp(ACT := rBeanTempActual, SET := rDrumTempSetpoint, KP := 2.0, TN := T#12s);
        rGasValvePos := PID_DrumTemp.OUT;
        
        IF rBeanTempActual >= 195.0 THEN
            iCurrentState := STATE_FIRST_CRACK;
        END_IF;
        
    STATE_FIRST_CRACK:
        // Modulate heat to avoid crashing the roast
        rGasValvePos := rGasValvePos * 0.8;
        IF rBeanTempActual >= 205.0 THEN
            iCurrentState := STATE_DEVELOPMENT;
        END_IF;
        
    STATE_DEVELOPMENT:
        // Final development phase
        rGasValvePos := 15.0; // Low fire
        IF rBeanTempActual >= 215.0 THEN // Drop temp
            iCurrentState := STATE_DROP;
        END_IF;
        
    STATE_DROP:
        bBurnerIgnition := FALSE;
        rGasValvePos := 0.0;
        rDrumMotorSpeed := 100.0; // Eject beans
        bCoolingTrayFan := TRUE;
        bCoolingTrayStirrer := TRUE;
        iCurrentState := STATE_COOLING;
        TMR_CoolingDuration(IN := FALSE);
        
    STATE_COOLING:
        TMR_CoolingDuration(IN := TRUE, PT := T#4m);
        IF TMR_CoolingDuration.Q THEN
            bCoolingTrayFan := FALSE;
            bCoolingTrayStirrer := FALSE;
            rDrumMotorSpeed := 0.0;
            rExhaustFanSpeed := 0.0;
            iCurrentState := STATE_IDLE;
        END_IF;
        
    STATE_QUENCH:
        // Emergency cascade
        bBurnerIgnition := FALSE;
        rGasValvePos := 0.0;
        rExhaustFanSpeed := 100.0; // Full exhaust
        rDrumMotorSpeed := 0.0;
        
        // If overtemp, activate quench valve
        IF bOverTempAlarm THEN
            bQuenchValve := TRUE;
            TMR_QuenchDuration(IN := TRUE, PT := T#1m);
            IF TMR_QuenchDuration.Q THEN
                bQuenchValve := FALSE;
            END_IF;
        END_IF;
        
        IF NOT bAlarmActive AND NOT bEStop THEN
            iCurrentState := STATE_IDLE;
        END_IF;
END_CASE;

// Cyclone extraction pressure control (runs parallel to state machine)
IF iCurrentState >= STATE_PURGE AND iCurrentState <= STATE_DROP THEN
    PID_Cyclone(ACT := rCyclonePressure, SET := rCyclonePressureSP, KP := 1.0, TN := T#5s);
    rExhaustFanSpeed := PID_Cyclone.OUT;
    bChaffRotaryValve := TRUE; // Run rotary valve during roasting
ELSE
    bChaffRotaryValve := FALSE;
END_IF;

eSystemState := iCurrentState;

END_FUNCTION_BLOCK
```"""

record = {
    'messages': [
        {'role': 'user', 'content': prompt},
        {'role': 'assistant', 'content': st_code}
    ]
}

# Write to swarm dir
filepath = f'data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json'
with open(filepath, 'w', encoding='utf-8') as f:
    json.dump(record, f)

# Also append to the jsonl file as per system instructions
with open('data/synthetic_generation_v3_enterprise.jsonl', 'a', encoding='utf-8') as f:
    f.write(json.dumps(record) + '\n')
    
print('Successfully wrote JSON payload')
