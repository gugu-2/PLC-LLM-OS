import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Municipal Solid Waste (MSW) Incinerator.
Task: Invent a highly complex control scenario for this domain (e.g., walking grate combustion sequencing, flue gas wet scrubber pH cascades, and Selective Non-Catalytic Reduction (SNCR)).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O.
"""

st_code = """```iec-st
FUNCTION_BLOCK FB_MSW_Incinerator_Control
TITLE = 'MSW Incinerator Comprehensive Control'
VERSION : '2.1'
AUTHOR : 'Lumina AI'

VAR_INPUT
    bSystemEnable : BOOL; // Main system enable
    rGrateTemp1 : REAL; // Grate Zone 1 Temperature (C) - Drying
    rGrateTemp2 : REAL; // Grate Zone 2 Temperature (C) - Combustion
    rGrateTemp3 : REAL; // Grate Zone 3 Temperature (C) - Burnout
    rBoilerSteamPress : REAL; // Boiler Steam Pressure (Bar)
    rFlueGasOxygen : REAL; // Flue Gas O2 Level (%)
    rScrubberPH : REAL; // Scrubber Effluent pH
    rFlueGasNOx : REAL; // Flue Gas NOx Concentration (mg/Nm3)
    bWasteFeedReady : BOOL; // Waste Crane/Feeder ready
END_VAR

VAR_OUTPUT
    rGrateSpeed1 : REAL; // Grate Zone 1 Speed (%)
    rGrateSpeed2 : REAL; // Grate Zone 2 Speed (%)
    rGrateSpeed3 : REAL; // Grate Zone 3 Speed (%)
    rPrimaryAirFlow : REAL; // Primary Air Fan Setpoint (%)
    rSecondaryAirFlow : REAL; // Secondary Air Fan Setpoint (%)
    rCausticDosingPump : REAL; // NaOH Dosing Pump Speed (%)
    rAmmoniaInjectionRate : REAL; // NH3 Injection Rate for SNCR (L/h)
    bSystemAlarm : BOOL;
    iStateCode : INT;
END_VAR

VAR
    // Internal States and Setpoints
    rTempSetpoint : REAL := 950.0; // Desired Combustion Temp
    rO2Setpoint : REAL := 6.0; // Desired O2 %
    rPHSetpoint : REAL := 7.5; // Scrubber Neutralization
    rNOxLimit : REAL := 150.0; // Emission Limit
    
    // PID Controllers for complex cascades
    PID_TempZone1 : FB_PID_Advanced;
    PID_TempZone2 : FB_PID_Advanced;
    PID_TempZone3 : FB_PID_Advanced;
    PID_AirO2 : FB_PID_Advanced;
    PID_ScrubberPH : FB_PID_Advanced;
    PID_SNCR : FB_PID_Advanced;
    
    timerStartUp : TON;
    bCombustionActive : BOOL;
END_VAR

// 1. Grate Sequencing & Combustion Control
// Walking grate systems require precise staging. Zone 1 dries, Zone 2 burns, Zone 3 extracts remaining energy.
IF bSystemEnable AND bWasteFeedReady THEN
    bCombustionActive := TRUE;
    iStateCode := 10;
ELSE
    bCombustionActive := FALSE;
    rGrateSpeed1 := 0.0;
    rGrateSpeed2 := 0.0;
    rGrateSpeed3 := 0.0;
    rPrimaryAirFlow := 10.0; // Purge flow
    iStateCode := 0;
END_IF;

IF bCombustionActive THEN
    // Grate Speed Control based on localized temperatures
    // Zone 1: Drive faster if temp is low to bring in more fuel, but constrained by drying rate.
    PID_TempZone1(EN := TRUE, PV := rGrateTemp1, SP := rTempSetpoint - 150.0, Kp := 2.5, Ki := 0.1, Kd := 0.5, OUT => rGrateSpeed1);
    
    // Zone 2: Main combustion, precise control to maintain 950C.
    PID_TempZone2(EN := TRUE, PV := rGrateTemp2, SP := rTempSetpoint, Kp := 3.0, Ki := 0.15, Kd := 0.4, OUT => rGrateSpeed2);
    
    // Zone 3: Burnout, slowing down if temp is too high to allow complete ash formation.
    PID_TempZone3(EN := TRUE, PV := rGrateTemp3, SP := rTempSetpoint - 250.0, Kp := 1.5, Ki := 0.05, Kd := 0.2, OUT => rGrateSpeed3);
    
    // Primary and Secondary Air Control based on O2 and Boiler Pressure cascade
    PID_AirO2(EN := TRUE, PV := rFlueGasOxygen, SP := rO2Setpoint, Kp := 5.0, Ki := 0.2, Kd := 1.0);
    
    IF rBoilerSteamPress < 40.0 THEN
        rPrimaryAirFlow := PID_AirO2.OUT + 15.0; // Boost combustion if steam pressure drops
    ELSE
        rPrimaryAirFlow := PID_AirO2.OUT;
    END_IF;
    
    // Secondary air is injected above the grate for turbulence and CO destruction.
    rSecondaryAirFlow := rPrimaryAirFlow * 0.65; 
    
    // 2. Wet Scrubber pH Cascade Control
    // Neutralizing acid gases (HCl, SO2) with NaOH. Negative Kp due to inverse reaction (higher dosing raises pH).
    PID_ScrubberPH(EN := TRUE, PV := rScrubberPH, SP := rPHSetpoint, Kp := -12.0, Ki := -0.8, Kd := -0.1, OUT => rCausticDosingPump);
    
    // Clamp dosing pump output to physical limits 0-100%
    IF rCausticDosingPump < 0.0 THEN rCausticDosingPump := 0.0; END_IF;
    IF rCausticDosingPump > 100.0 THEN rCausticDosingPump := 100.0; END_IF;
    
    // 3. Selective Non-Catalytic Reduction (SNCR) - Ammonia Injection
    // The SNCR process requires a strict temperature window (850C - 1050C) to prevent ammonia slip.
    IF rGrateTemp2 > 850.0 AND rGrateTemp2 < 1050.0 THEN
        PID_SNCR(EN := TRUE, PV := rFlueGasNOx, SP := rNOxLimit * 0.85, Kp := 1.2, Ki := 0.05, Kd := 0.2, OUT => rAmmoniaInjectionRate);
    ELSE
        // Outside the thermal window, NO reduction is inefficient or causes excessive ammonia slip.
        rAmmoniaInjectionRate := 0.0; 
        iStateCode := 99; // SNCR Inhibited Warning
    END_IF;
    
    // Comprehensive Alarming
    IF rFlueGasNOx > (rNOxLimit * 1.1) OR rScrubberPH < 5.0 OR rScrubberPH > 10.0 THEN
        bSystemAlarm := TRUE;
    ELSE
        bSystemAlarm := FALSE;
    END_IF;
    
END_IF;
END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": st_code}]}

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)

print(f"Success. Saved to {filename}")
