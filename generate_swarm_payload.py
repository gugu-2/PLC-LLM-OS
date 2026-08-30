import os, json, uuid

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Rotary Kiln Cement Plant.
Task: Invent a highly complex control scenario for this domain (e.g., clinker burning zone pyrometer tracking, secondary air pre-calciner thermal cascades, and exhaust gas bypass loops).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."""

code = """```iec-st
FUNCTION_BLOCK FB_RotaryKilnAdvancedControl
TITLE = 'Rotary Kiln Advanced Control System'
VERSION : '2.5'
AUTHOR : 'Lumina Swarm'

VAR_INPUT
    // Real-time process variables
    rBurningZoneTemp       : REAL; // Pyrometer reading [°C]
    rSecondaryAirTemp      : REAL; // [°C]
    rPrecalcinerTemp       : REAL; // [°C]
    rKilnFeedRate          : REAL; // Raw meal feed [t/h]
    rMainBurnerFuel        : REAL; // [kg/s]
    rCalcinerFuel          : REAL; // [kg/s]
    rKilnDriveSpeed_RPM    : REAL; // [RPM]
    rKilnTorque            : REAL; // [%]
    rExhaustGasTemp        : REAL; // [°C]
    rBypassDamperPos_In    : REAL; // [%]
    rIDFanSpeed_In         : REAL; // [%]
    bSystemStart           : BOOL;
    bEmergencyStop         : BOOL;
    
    // Setpoints
    rSP_BurningZoneTemp    : REAL := 1450.0;
    rSP_SecondaryAir       : REAL := 1050.0;
    rSP_ExhaustO2          : REAL := 2.5; // [%]
END_VAR

VAR_OUTPUT
    rMainBurnerFuel_Out    : REAL; // Manipulated Variable [kg/s]
    rCalcinerFuel_Out      : REAL; // Manipulated Variable [kg/s]
    rKilnDriveSpeed_Out    : REAL; // [RPM]
    rBypassDamperPos_Out   : REAL; // [%]
    rIDFanSpeed_Out        : REAL; // [%]
    bKilnReady             : BOOL;
    bAlarmHighTorque       : BOOL;
    bAlarmHighTemp         : BOOL;
    bAlarmLowTemp          : BOOL;
    bEmergencyShutdown     : BOOL;
END_VAR

VAR
    // Internal States and PID objects
    pidMainBurner          : FB_PID_Advanced;
    pidCalciner            : FB_PID_Advanced;
    pidIDFan               : FB_PID_Advanced;
    rThermalCascadeError   : REAL;
    rTorqueFilter          : REAL;
    rTempFilterTime        : TIME := T#5S;
    tStabilizationTimer    : TON;
    rBypassControlGain     : REAL := 1.2;
    rFuelToFeedRatio       : REAL;
    rMaxKilnSpeed          : REAL := 5.0; // RPM
    rMinKilnSpeed          : REAL := 0.5; // RPM
    iState                 : INT := 0; 
END_VAR

// Filter incoming noise on critical torque readings
rTorqueFilter := rTorqueFilter * 0.9 + rKilnTorque * 0.1;

// Alarm Logic
bAlarmHighTorque := rTorqueFilter > 95.0;
bAlarmHighTemp := (rBurningZoneTemp > 1600.0) OR (rPrecalcinerTemp > 950.0);
bAlarmLowTemp := (rBurningZoneTemp < 1300.0) AND bSystemStart;

IF bEmergencyStop OR bAlarmHighTorque OR (rBurningZoneTemp > 1650.0) THEN
    bEmergencyShutdown := TRUE;
    rMainBurnerFuel_Out := 0.0;
    rCalcinerFuel_Out := 0.0;
    rKilnDriveSpeed_Out := 0.0;
    rIDFanSpeed_Out := 50.0; // Maintain some draft
    rBypassDamperPos_Out := 100.0; // Open bypass fully
    iState := 99; // Fault state
    RETURN;
END_IF;

bEmergencyShutdown := FALSE;

CASE iState OF
    0: // Standby
        bKilnReady := FALSE;
        IF bSystemStart THEN
            iState := 10;
        END_IF;
        
    10: // Pre-heating
        rMainBurnerFuel_Out := 0.1; // Minimal flame
        rKilnDriveSpeed_Out := rMinKilnSpeed;
        IF rBurningZoneTemp > 800.0 THEN
            iState := 20;
        END_IF;
        
    20: // Ramping up
        // Setup PID for main burner
        pidMainBurner(
            rSP := rSP_BurningZoneTemp,
            rPV := rBurningZoneTemp,
            rKp := 2.5, rTi := 120.0, rTd := 15.0,
            rOut => rMainBurnerFuel_Out
        );
        IF rBurningZoneTemp >= (rSP_BurningZoneTemp - 50.0) THEN
            tStabilizationTimer(IN:=TRUE, PT:=T#10M);
            IF tStabilizationTimer.Q THEN
                iState := 30; // Normal operation
            END_IF;
        END_IF;
        
    30: // Normal Operation
        bKilnReady := TRUE;
        
        // 1. Burning Zone Control via Main Burner Fuel
        pidMainBurner(
            rSP := rSP_BurningZoneTemp,
            rPV := rBurningZoneTemp,
            rKp := 3.0, rTi := 90.0, rTd := 20.0,
            rOut => rMainBurnerFuel_Out
        );
        
        // 2. Precalciner Thermal Cascade Control
        // The setpoint for the calciner adjusts based on secondary air availability
        rThermalCascadeError := rSP_SecondaryAir - rSecondaryAirTemp;
        pidCalciner(
            rSP := 880.0 + (rThermalCascadeError * 0.1),
            rPV := rPrecalcinerTemp,
            rKp := 1.5, rTi := 60.0, rTd := 5.0,
            rOut => rCalcinerFuel_Out
        );
        
        // 3. Exhaust Gas Bypass Loop
        // Used to control volatile cycles (chlorides, alkalis) inferred from temp and pressure
        IF rExhaustGasTemp > 1100.0 THEN
            rBypassDamperPos_Out := rBypassDamperPos_In + ((rExhaustGasTemp - 1100.0) * rBypassControlGain);
            IF rBypassDamperPos_Out > 100.0 THEN rBypassDamperPos_Out := 100.0; END_IF;
        ELSE
            rBypassDamperPos_Out := rBypassDamperPos_In - 0.5;
            IF rBypassDamperPos_Out < 0.0 THEN rBypassDamperPos_Out := 0.0; END_IF;
        END_IF;
        
        // 4. Kiln Drive Speed Optimization
        rFuelToFeedRatio := (rMainBurnerFuel_Out + rCalcinerFuel_Out) / (rKilnFeedRate + 0.001);
        rKilnDriveSpeed_Out := rKilnFeedRate * 0.015; // Base speed based on feed
        
        IF rTorqueFilter > 85.0 THEN
            rKilnDriveSpeed_Out := rKilnDriveSpeed_Out * 0.9; // Reduce speed to handle high torque
        END_IF;
        
        // Clamp speed
        IF rKilnDriveSpeed_Out > rMaxKilnSpeed THEN rKilnDriveSpeed_Out := rMaxKilnSpeed; END_IF;
        IF rKilnDriveSpeed_Out < rMinKilnSpeed THEN rKilnDriveSpeed_Out := rMinKilnSpeed; END_IF;
        
        // 5. Draft Control (ID Fan)
        pidIDFan(
            rSP := rSP_ExhaustO2,
            rPV := 2.0, // Assuming a fixed or measured O2 sensor PV here
            rKp := 5.0, rTi := 30.0, rTd := 0.0,
            rOut => rIDFanSpeed_Out
        );
        
    99: // Fault state
        IF NOT bEmergencyStop AND NOT bAlarmHighTorque AND (rBurningZoneTemp < 1000.0) THEN
            iState := 0; // Reset to standby when safe
        END_IF;
        
END_CASE;

END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
filepath = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"

with open(filepath, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=4)

print(f"Success: Wrote payload to {filepath}")
