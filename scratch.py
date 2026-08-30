import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Float Glass Lehr Annealing Furnace.
Task: Invent a highly complex control scenario for this domain (e.g., transverse thermal stress relieving zones, ribbon thickness draw speed tracking, and SO2 surface treatment).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."""

response_content = """```iec-st
FUNCTION_BLOCK FB_Lehr_Annealing_Furnace
VAR_INPUT
    bEnable : BOOL; // System Enable
    rRibbonSpeed : REAL; // Draw speed in m/min
    rRibbonThickness : REAL; // Ribbon thickness in mm
    rZone1_Temp_SetPt : REAL; // Transverse Zone 1 Temp Setpoint (Celsius)
    rZone2_Temp_SetPt : REAL; // Transverse Zone 2 Temp Setpoint (Celsius)
    rZone3_Temp_SetPt : REAL; // Transverse Zone 3 Temp Setpoint (Celsius)
    rZone1_Temp_Act : REAL; // Actual Temp Zone 1
    rZone2_Temp_Act : REAL; // Actual Temp Zone 2
    rZone3_Temp_Act : REAL; // Actual Temp Zone 3
    rSO2_Flow_SetPt : REAL; // SO2 Surface treatment flow setpoint (mg/m2)
    rSO2_Flow_Act : REAL; // Actual SO2 flow
    bEmergencyStop : BOOL; // E-Stop
END_VAR
VAR_OUTPUT
    rZone1_Heater_Cmd : REAL; // 0-100% Heating Command
    rZone2_Heater_Cmd : REAL; // 0-100% Heating Command
    rZone3_Heater_Cmd : REAL; // 0-100% Heating Command
    rZone1_Cooling_Cmd : REAL; // 0-100% Cooling Command
    rZone2_Cooling_Cmd : REAL; // 0-100% Cooling Command
    rZone3_Cooling_Cmd : REAL; // 0-100% Cooling Command
    rSO2_Valve_Cmd : REAL; // 0-100% Valve Command
    bAlarmActive : BOOL; // Global Alarm
    iAlarmCode : INT; // Alarm code for HMI
    rCalculatedThermalStress : REAL; // Estimated stress (MPa)
END_VAR
VAR
    // PID Controllers for Zones
    pidZone1 : FB_PID_Advanced;
    pidZone2 : FB_PID_Advanced;
    pidZone3 : FB_PID_Advanced;
    pidSO2 : FB_PID_Advanced;

    // Internal Variables
    rCoolingRateLimit : REAL := -2.5; // degC/sec max cooling
    rHeatingRateLimit : REAL := 5.0; // degC/sec max heating
    rMassFlow : REAL; // Calculated mass flow of glass
    rBaseCooling : REAL; // Feedforward cooling based on speed and thickness

    // Timers
    tProcessDelay : TON;
    tAlarmDelay : TON;

    // State Machine
    eState : (INIT, RUNNING, FAULT, STOPPED) := INIT;
END_VAR

// Implementation
IF bEmergencyStop THEN
    eState := FAULT;
    iAlarmCode := 999;
END_IF;

CASE eState OF
    INIT:
        rZone1_Heater_Cmd := 0.0;
        rZone2_Heater_Cmd := 0.0;
        rZone3_Heater_Cmd := 0.0;
        rZone1_Cooling_Cmd := 0.0;
        rZone2_Cooling_Cmd := 0.0;
        rZone3_Cooling_Cmd := 0.0;
        rSO2_Valve_Cmd := 0.0;
        bAlarmActive := FALSE;
        iAlarmCode := 0;
        IF bEnable AND NOT bEmergencyStop THEN
            eState := RUNNING;
        END_IF;

    RUNNING:
        IF NOT bEnable THEN
            eState := STOPPED;
        END_IF;

        // 1. Ribbon Tracking & Mass Flow Calculation
        // Density of glass ~2500 kg/m^3. Ribbon width assumed 3.2m
        rMassFlow := rRibbonSpeed * (rRibbonThickness / 1000.0) * 3.2 * 2500.0;

        // 2. Feedforward Cooling Requirement based on Thickness & Speed
        // Thicker ribbon requires slower cooling to prevent stress
        rBaseCooling := rMassFlow * 0.015;

        // 3. Zone 1 PID Control (Heating / Cooling)
        pidZone1(
            rSetpoint := rZone1_Temp_SetPt,
            rActual := rZone1_Temp_Act,
            rKp := 2.5, rKi := 0.1, rKd := 0.5,
            rFeedForward := rBaseCooling * 0.4
        );
        IF pidZone1.rOutput > 0.0 THEN
            rZone1_Heater_Cmd := pidZone1.rOutput;
            rZone1_Cooling_Cmd := 0.0;
        ELSE
            rZone1_Heater_Cmd := 0.0;
            rZone1_Cooling_Cmd := ABS(pidZone1.rOutput);
        END_IF;

        // 4. Zone 2 PID Control
        pidZone2(
            rSetpoint := rZone2_Temp_SetPt,
            rActual := rZone2_Temp_Act,
            rKp := 3.0, rKi := 0.15, rKd := 0.6,
            rFeedForward := rBaseCooling * 0.5
        );
        IF pidZone2.rOutput > 0.0 THEN
            rZone2_Heater_Cmd := pidZone2.rOutput;
            rZone2_Cooling_Cmd := 0.0;
        ELSE
            rZone2_Heater_Cmd := 0.0;
            rZone2_Cooling_Cmd := ABS(pidZone2.rOutput);
        END_IF;

        // 5. Zone 3 PID Control
        pidZone3(
            rSetpoint := rZone3_Temp_SetPt,
            rActual := rZone3_Temp_Act,
            rKp := 4.0, rKi := 0.2, rKd := 0.8,
            rFeedForward := rBaseCooling * 0.1
        );
        IF pidZone3.rOutput > 0.0 THEN
            rZone3_Heater_Cmd := pidZone3.rOutput;
            rZone3_Cooling_Cmd := 0.0;
        ELSE
            rZone3_Heater_Cmd := 0.0;
            rZone3_Cooling_Cmd := ABS(pidZone3.rOutput);
        END_IF;

        // 6. SO2 Surface Treatment Flow Control
        // Required flow scales with ribbon speed and surface area
        pidSO2(
            rSetpoint := rSO2_Flow_SetPt * (rRibbonSpeed * 3.2),
            rActual := rSO2_Flow_Act,
            rKp := 1.2, rKi := 0.05, rKd := 0.1
        );
        rSO2_Valve_Cmd := pidSO2.rOutput;

        // 7. Thermal Stress Estimation (simplified transverse gradient model)
        rCalculatedThermalStress := ABS(rZone1_Temp_Act - rZone3_Temp_Act) * 0.52 * (rRibbonThickness / 10.0);

        // 8. Alarm Handling
        IF rCalculatedThermalStress > 15.0 THEN
            bAlarmActive := TRUE;
            iAlarmCode := 101; // High Thermal Stress
        ELSIF ABS(rZone1_Temp_SetPt - rZone1_Temp_Act) > 20.0 THEN
            bAlarmActive := TRUE;
            iAlarmCode := 102; // Zone 1 Temp Deviation
        ELSE
            bAlarmActive := FALSE;
            iAlarmCode := 0;
        END_IF;

    STOPPED:
        rZone1_Heater_Cmd := 0.0;
        rZone2_Heater_Cmd := 0.0;
        rZone3_Heater_Cmd := 0.0;
        rZone1_Cooling_Cmd := 0.0;
        rZone2_Cooling_Cmd := 0.0;
        rZone3_Cooling_Cmd := 0.0;
        rSO2_Valve_Cmd := 0.0;
        IF bEnable AND NOT bEmergencyStop THEN
            eState := INIT;
        END_IF;

    FAULT:
        rZone1_Heater_Cmd := 0.0;
        rZone2_Heater_Cmd := 0.0;
        rZone3_Heater_Cmd := 0.0;
        rZone1_Cooling_Cmd := 100.0; // Max cooling on fault
        rZone2_Cooling_Cmd := 100.0;
        rZone3_Cooling_Cmd := 100.0;
        rSO2_Valve_Cmd := 0.0;
        bAlarmActive := TRUE;
        IF NOT bEmergencyStop AND bEnable THEN
            eState := INIT; // Reset fault if E-Stop cleared and re-enabled
        END_IF;

END_CASE;
END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": response_content}]}
filepath = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filepath, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)

print(f"Saved to {filepath}")
