import json, uuid, os
os.makedirs('data/swarm_raw', exist_ok=True)
os.makedirs('data', exist_ok=True)

code='''```iec-st
FUNCTION_BLOCK FB_TissueMachineMasterControl
TITLE = 'Tissue Paper Machine Master Control - Yankee, Crepe, Calendar'
VERSION : '2.4.1'
AUTHOR : 'Lumina AI Cloud Swarm'

VAR_INPUT
    // System Control
    xEnableSystem          : BOOL;   // Master enable switch
    xEmergencyStop         : BOOL;   // E-Stop active low
    xResetFaults           : BOOL;   // Reset alarm latches
    
    // Yankee Dryer Sensors
    rYankeeSurfaceTemp     : REAL;   // Current Yankee cylinder surface temperature [C]
    rMainSteamPressure     : REAL;   // Main header steam pressure [bar]
    rYankeeCondensateLevel : REAL;   // Condensate level inside the Yankee [mm]
    
    // Crepe Doctor Blade Sensors
    rBladeWearSensor       : REAL;   // Doctor blade wear measurement [mm]
    rHydraulicSupplyPress  : REAL;   // Hydraulic system supply pressure [bar]
    rBladeVibrationLevel   : REAL;   // Vibration monitoring for chatter [mm/s]
    
    // Calendar Stack Sensors
    rWebTension            : REAL;   // Sheet tension entering calendar [N/m]
    rNipLoadCell1          : REAL;   // Drive side nip load cell [kN/m]
    rNipLoadCell2          : REAL;   // Tender side nip load cell [kN/m]
    rTargetCaliper         : REAL;   // Target sheet thickness [microns]
    
    // Target Setpoints
    rTargetYankeeTemp      : REAL;   // Target Yankee temperature [C]
    rTargetBladeLoad       : REAL;   // Target doctor blade linear load [kN/m]
    rTargetNipPressure     : REAL;   // Target average nip pressure [kN/m]
END_VAR

VAR_OUTPUT
    // Actuators - Yankee
    rSteamValveCommand     : REAL;   // Command to Yankee steam inlet valve [0-100%]
    rBlowThroughValveCmd   : REAL;   // Command to condensate blow-through valve [0-100%]
    xCondensatePumpRun     : BOOL;   // Start/Stop for condensate removal pump
    
    // Actuators - Crepe Blade
    rBladeLoadValveDrive   : REAL;   // Proportional valve cmd for drive side blade load [0-100%]
    rBladeLoadValveTender  : REAL;   // Proportional valve cmd for tender side blade load [0-100%]
    xBladeOscillatorRun    : BOOL;   // Enable cross-machine blade oscillation
    
    // Actuators - Calendar Stack
    rNipHydraulicCmdDrive  : REAL;   // Calendar loading cylinder drive side [0-100%]
    rNipHydraulicCmdTender : REAL;   // Calendar loading cylinder tender side [0-100%]
    
    // Status and Alarms
    xSystemReady           : BOOL;
    xYankeeTempOK          : BOOL;
    xBladeChatterAlarm     : BOOL;
    xWebBreakAlarm         : BOOL;
    wErrorCode             : WORD;   // Bitmask of active faults
END_VAR

VAR
    // Internal Control States
    rTempError             : REAL;
    rTempIntegral          : REAL := 0.0;
    rTempDerivative        : REAL := 0.0;
    rLastTempError         : REAL := 0.0;
    
    rPressureSetpoint      : REAL;
    rPressureError         : REAL;
    rPressureIntegral      : REAL := 0.0;
    
    // Tuning Parameters
    rKp_Temp               : REAL := 2.5;
    rKi_Temp               : REAL := 0.15;
    rKd_Temp               : REAL := 0.05;
    
    rKp_Press              : REAL := 5.0;
    rKi_Press              : REAL := 0.8;
    
    // Timers
    tonCondensateDrain     : TON;
    tonVibrationFilter     : TON;
    
    // Safety Limits
    rMaxSteamPressure      : REAL := 8.5; // Maximum allowable Yankee steam pressure
    rMaxBladeVibration     : REAL := 12.0; // Vibration trip limit
    rMinWebTension         : REAL := 50.0; // Minimum tension before assuming web break
    
    // Local flags
    xFaultActive           : BOOL;
    
    // Calcs
    rCompensatedLoad       : REAL;
    rNipErrorDrive         : REAL;
    rNipErrorTender        : REAL;
END_VAR

// -----------------------------------------------------------------------------
// FAULT HANDLING AND SAFETY INTERLOCKS
// -----------------------------------------------------------------------------
xFaultActive := FALSE;
wErrorCode := 0;

IF NOT xEmergencyStop THEN
    wErrorCode := wErrorCode OR 16#0001;
    xFaultActive := TRUE;
END_IF;

IF rMainSteamPressure > rMaxSteamPressure THEN
    wErrorCode := wErrorCode OR 16#0002;
    xFaultActive := TRUE;
END_IF;

tonVibrationFilter(IN := (rBladeVibrationLevel > rMaxBladeVibration), PT := T#2S);
IF tonVibrationFilter.Q THEN
    xBladeChatterAlarm := TRUE;
    wErrorCode := wErrorCode OR 16#0004;
    xFaultActive := TRUE;
END_IF;

IF (rWebTension < rMinWebTension) AND xEnableSystem THEN
    xWebBreakAlarm := TRUE;
    wErrorCode := wErrorCode OR 16#0008;
END_IF;

IF xResetFaults THEN
    xBladeChatterAlarm := FALSE;
    xWebBreakAlarm := FALSE;
    xFaultActive := FALSE;
    wErrorCode := 0;
END_IF;

// Fast stop on critical fault
IF xFaultActive THEN
    rSteamValveCommand := 0.0;
    rBlowThroughValveCmd := 100.0; // Vent
    rBladeLoadValveDrive := 0.0;
    rBladeLoadValveTender := 0.0;
    xBladeOscillatorRun := FALSE;
    rNipHydraulicCmdDrive := 0.0;
    rNipHydraulicCmdTender := 0.0;
    xSystemReady := FALSE;
    RETURN;
END_IF;

// -----------------------------------------------------------------------------
// CASCADE PID: YANKEE DRYER TEMPERATURE TO STEAM PRESSURE
// -----------------------------------------------------------------------------
// Outer Loop: Temperature to Pressure Setpoint
rTempError := rTargetYankeeTemp - rYankeeSurfaceTemp;
rTempIntegral := rTempIntegral + (rTempError * 0.1); // Assuming 100ms task
rTempDerivative := (rTempError - rLastTempError) / 0.1;
rLastTempError := rTempError;

// Anti-windup for Outer Loop
IF rTempIntegral > 50.0 THEN rTempIntegral := 50.0; END_IF;
IF rTempIntegral < -50.0 THEN rTempIntegral := -50.0; END_IF;

rPressureSetpoint := (rKp_Temp * rTempError) + (rKi_Temp * rTempIntegral) + (rKd_Temp * rTempDerivative);

// Clamp Pressure Setpoint
IF rPressureSetpoint > (rMaxSteamPressure - 0.5) THEN
    rPressureSetpoint := rMaxSteamPressure - 0.5;
ELSIF rPressureSetpoint < 0.0 THEN
    rPressureSetpoint := 0.0;
END_IF;

// Inner Loop: Pressure Setpoint to Valve Command
rPressureError := rPressureSetpoint - rMainSteamPressure;
rPressureIntegral := rPressureIntegral + (rPressureError * 0.1);

// Anti-windup for Inner Loop
IF rPressureIntegral > 100.0 THEN rPressureIntegral := 100.0; END_IF;
IF rPressureIntegral < 0.0 THEN rPressureIntegral := 0.0; END_IF;

rSteamValveCommand := (rKp_Press * rPressureError) + (rKi_Press * rPressureIntegral);
IF rSteamValveCommand > 100.0 THEN rSteamValveCommand := 100.0; END_IF;
IF rSteamValveCommand < 0.0 THEN rSteamValveCommand := 0.0; END_IF;

// Condensate Management
xCondensatePumpRun := (rYankeeCondensateLevel > 150.0) OR (rMainSteamPressure > 4.0);
IF rYankeeCondensateLevel > 250.0 THEN
    rBlowThroughValveCmd := 80.0; // Aggressive blow-through
ELSE
    rBlowThroughValveCmd := 20.0; // Baseline DP control
END_IF;

xYankeeTempOK := ABS(rTempError) < 2.5;

// -----------------------------------------------------------------------------
// CREPE DOCTOR BLADE HYDRAULIC LOADING
// -----------------------------------------------------------------------------
IF xEnableSystem AND NOT xWebBreakAlarm THEN
    // Compensate target load based on blade wear profile (simple linear scaling)
    rCompensatedLoad := rTargetBladeLoad * (1.0 + (rBladeWearSensor * 0.02));
    
    // Distribute load evenly assuming uniform cross-machine profile, but offset if needed
    rBladeLoadValveDrive := (rCompensatedLoad / rHydraulicSupplyPress) * 100.0;
    rBladeLoadValveTender := (rCompensatedLoad / rHydraulicSupplyPress) * 100.0;
    
    // Clamp output commands
    IF rBladeLoadValveDrive > 100.0 THEN rBladeLoadValveDrive := 100.0; END_IF;
    IF rBladeLoadValveTender > 100.0 THEN rBladeLoadValveTender := 100.0; END_IF;
    
    xBladeOscillatorRun := TRUE;
ELSE
    rBladeLoadValveDrive := 0.0;
    rBladeLoadValveTender := 0.0;
    xBladeOscillatorRun := FALSE;
END_IF;

// -----------------------------------------------------------------------------
// CALENDAR STACK NIP PRESSURE
// -----------------------------------------------------------------------------
IF xEnableSystem AND NOT xWebBreakAlarm THEN
    // Target Nip Pressure is split between Drive and Tender sides based on load cells
    rNipErrorDrive := rTargetNipPressure - rNipLoadCell1;
    rNipErrorTender := rTargetNipPressure - rNipLoadCell2;
    
    // Simple Proportional feedback for Nip Gap
    rNipHydraulicCmdDrive := rNipHydraulicCmdDrive + (rNipErrorDrive * 0.1);
    rNipHydraulicCmdTender := rNipHydraulicCmdTender + (rNipErrorTender * 0.1);
    
    // Clamping logic
    IF rNipHydraulicCmdDrive > 100.0 THEN rNipHydraulicCmdDrive := 100.0; END_IF;
    IF rNipHydraulicCmdDrive < 0.0 THEN rNipHydraulicCmdDrive := 0.0; END_IF;
    
    IF rNipHydraulicCmdTender > 100.0 THEN rNipHydraulicCmdTender := 100.0; END_IF;
    IF rNipHydraulicCmdTender < 0.0 THEN rNipHydraulicCmdTender := 0.0; END_IF;
ELSE
    rNipHydraulicCmdDrive := 0.0;
    rNipHydraulicCmdTender := 0.0;
END_IF;

xSystemReady := TRUE;
END_FUNCTION_BLOCK
```'''

prompt='Invent a highly complex control scenario for a Tissue Paper Machine (Yankee dryer steam pressure cascading, crepe doctor blade hydraulic loading, and calendar stack nip pressure). Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O.'
record={'messages':[{'role':'user','content':prompt},{'role':'assistant','content':code}]}

# 1. Save to unique file
filepath=f'data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json'
with open(filepath,'w',encoding='utf-8') as f:
    json.dump(record,f,indent=2)
    
# 2. Append to jsonl
with open('data/synthetic_generation_v3_enterprise.jsonl','a',encoding='utf-8') as f:
    f.write(json.dumps(record) + "\n")
    
print('Success: ' + filepath)
