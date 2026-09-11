import json, os

st_code = """FUNCTION_BLOCK FB_FGD_Control
TITLE = 'Flue Gas Desulfurization (FGD) Unit Advanced Control'
VERSION : '2.0'

VAR_INPUT
    rFlueGasInletFlow       : REAL; // m3/h
    rFlueGasInletSO2        : REAL; // mg/Nm3
    rAbsorberLevel          : REAL; // m
    rAbsorberPH             : REAL; // pH
    rSlurryDensity          : REAL; // kg/m3
    bSprayPump1_Running     : BOOL;
    bSprayPump2_Running     : BOOL;
    bSprayPump3_Running     : BOOL;
    bSprayPump4_Running     : BOOL;
    rGypsumCentrifugeSpeed  : REAL; // rpm
    rLimestoneSiloLevel     : REAL; // %
    bSystemEnable           : BOOL;
END_VAR

VAR_OUTPUT
    rLimestoneFeedRate      : REAL; // kg/h
    rOxidationAirFlow       : REAL; // Nm3/h
    bSprayPump1_Cmd         : BOOL;
    bSprayPump2_Cmd         : BOOL;
    bSprayPump3_Cmd         : BOOL;
    bSprayPump4_Cmd         : BOOL;
    rCentrifugeFeedRate     : REAL; // m3/h
    bSystemAlarm            : BOOL;
    iAlarmCode              : INT;
    rAbsorberPH_SP_Calc     : REAL; 
END_VAR

VAR
    rSO2Load                : REAL;
    rStoichiometricRatio    : REAL := 1.05;
    rBaseLimestoneDemand    : REAL;
    rPH_Error               : REAL;
    rPH_Kp                  : REAL := 50.0;
    rPH_Ki                  : REAL := 2.5;
    rPH_Integral            : REAL;
    rActiveSprayPumps       : INT;
    rRequiredSprayPumps     : INT;
    rDensityError           : REAL;
    rDensity_SP             : REAL := 1150.0; // kg/m3
END_VAR

// FGD Control Logic
IF NOT bSystemEnable THEN
    rLimestoneFeedRate := 0.0;
    rOxidationAirFlow := 0.0;
    bSprayPump1_Cmd := FALSE;
    bSprayPump2_Cmd := FALSE;
    bSprayPump3_Cmd := FALSE;
    bSprayPump4_Cmd := FALSE;
    rCentrifugeFeedRate := 0.0;
    bSystemAlarm := FALSE;
    iAlarmCode := 0;
    rPH_Integral := 0.0;
    RETURN;
END_IF;

// 1. Calculate SO2 Load
rSO2Load := (rFlueGasInletFlow / 3600.0) * rFlueGasInletSO2 / 1000.0; // kg/s SO2

// 2. Cascade pH Control & Limestone Feed
// Calculate desired pH setpoint based on SO2 load (higher load -> higher pH SP to capture more SO2)
rAbsorberPH_SP_Calc := 5.2 + (rSO2Load * 0.05);
IF rAbsorberPH_SP_Calc > 5.8 THEN
    rAbsorberPH_SP_Calc := 5.8;
END_IF;

rPH_Error := rAbsorberPH_SP_Calc - rAbsorberPH;
rPH_Integral := rPH_Integral + (rPH_Error * rPH_Ki);

// Anti-windup
IF rPH_Integral > 500.0 THEN
    rPH_Integral := 500.0;
ELSIF rPH_Integral < -500.0 THEN
    rPH_Integral := -500.0;
END_IF;

rBaseLimestoneDemand := rSO2Load * rStoichiometricRatio * 1.56; // Molar mass ratio adjustment
rLimestoneFeedRate := rBaseLimestoneDemand * 3600.0 + (rPH_Error * rPH_Kp) + rPH_Integral;

IF rLimestoneFeedRate < 0.0 THEN
    rLimestoneFeedRate := 0.0;
ELSIF rLimestoneFeedRate > 15000.0 THEN
    rLimestoneFeedRate := 15000.0;
END_IF;

// 3. Oxidation Air Flow Control
// Oxidation of CaSO3 to CaSO4 (Gypsum)
rOxidationAirFlow := rSO2Load * 3.0 * 3600.0; // Rule of thumb: 3 Nm3 air per kg SO2

// 4. Spray Header Pump Management
IF rSO2Load > 25.0 THEN
    rRequiredSprayPumps := 4;
ELSIF rSO2Load > 18.0 THEN
    rRequiredSprayPumps := 3;
ELSIF rSO2Load > 10.0 THEN
    rRequiredSprayPumps := 2;
ELSE
    rRequiredSprayPumps := 1;
END_IF;

// Simplified sequencing
bSprayPump1_Cmd := (rRequiredSprayPumps >= 1);
bSprayPump2_Cmd := (rRequiredSprayPumps >= 2);
bSprayPump3_Cmd := (rRequiredSprayPumps >= 3);
bSprayPump4_Cmd := (rRequiredSprayPumps >= 4);

// 5. Gypsum Dewatering (Centrifuge Feed Control)
rDensityError := rSlurryDensity - rDensity_SP;
IF rDensityError > 10.0 THEN
    // Slurry too dense, increase feed to centrifuge
    rCentrifugeFeedRate := rCentrifugeFeedRate + 0.5;
ELSIF rDensityError < -10.0 THEN
    // Slurry too thin, decrease feed
    rCentrifugeFeedRate := rCentrifugeFeedRate - 0.5;
END_IF;

IF rCentrifugeFeedRate > 150.0 THEN
    rCentrifugeFeedRate := 150.0;
ELSIF rCentrifugeFeedRate < 0.0 THEN
    rCentrifugeFeedRate := 0.0;
END_IF;

// 6. Alarms
bSystemAlarm := FALSE;
iAlarmCode := 0;

IF rAbsorberLevel > 15.0 THEN
    bSystemAlarm := TRUE;
    iAlarmCode := 1; // High Level
ELSIF rLimestoneSiloLevel < 10.0 THEN
    bSystemAlarm := TRUE;
    iAlarmCode := 2; // Low Limestone
ELSIF rAbsorberPH < 4.5 THEN
    bSystemAlarm := TRUE;
    iAlarmCode := 3; // Low pH
END_IF;

END_FUNCTION_BLOCK
"""

prompt = "Invent a highly complex control scenario for Flue Gas Desulfurization (FGD) Unit..."
record = {'messages': [{'role': 'user', 'content': prompt}, {'role': 'assistant', 'content': f'```iec-st\\n{st_code}\\n```'}]}
os.makedirs('data', exist_ok=True)
with open('data/synthetic_generation_v3_enterprise.jsonl', 'a', encoding='utf-8') as f:
    f.write(json.dumps(record) + '\\n')
print('Appended to JSONL')
