import json, uuid, os

st_code = """```iec-st
FUNCTION_BLOCK FB_GravurePress_ESA_Lel_DoctorBlade
TITLE = 'Gravure Printing Press Advanced Control'
VERSION : '1.0'

VAR_INPUT
    bEnable : BOOL; // Enable advanced press control
    rWebSpeed_mmin : REAL; // Current web speed in m/min
    rDoctorBladePressure_bar : REAL; // Current applied pressure to doctor blade
    rBladeAngle_deg : REAL; // Current doctor blade angle
    rImpressionRollerForce_N : REAL; // Impression roller force
    rInkViscosity_mPas : REAL; // Current ink viscosity
    rVaporLEL_Percent : REAL; // Current Lower Explosive Limit percentage from sensors
    aESA_VoltageFeedback_kV : ARRAY[1..8] OF REAL; // Feedback voltages from ESA units
    rTemperature_C : REAL; // Ambient temperature at printing unit
END_VAR

VAR_OUTPUT
    aESA_VoltageSetpoint_kV : ARRAY[1..8] OF REAL; // High-voltage setpoints for electrostatic assist
    rDoctorBladeComp_mm : REAL; // Calculated wear compensation position adjustment
    bLEL_Warning : BOOL; // Vapor concentration warning
    bLEL_CriticalShutdown : BOOL; // Critical shutdown signal due to vapor concentration
    rExhaustFanSpeed_RPM : REAL; // Setpoint for exhaust ventilation fans
    bESA_Fault : BOOL; // Fault flag for electrostatic ink assist
END_VAR

VAR
    i : INT;
    rWearRate_mm_per_1000m : REAL;
    rTotalWebLength_m : LREAL;
    rAccumulatedWear_mm : REAL;
    rDynamicVoltageTarget_kV : REAL;
    rVaporSafetyMargin : REAL := 15.0; // 15% safety margin
    rCriticalVaporLimit : REAL := 45.0; // 45% LEL shutdown limit
    Timer_Update : TON;
    bFirstCycle : BOOL := TRUE;
    rPrevWebSpeed : REAL;
END_VAR

// INITIALIZATION
IF bFirstCycle THEN
    rTotalWebLength_m := 0.0;
    rAccumulatedWear_mm := 0.0;
    bFirstCycle := FALSE;
END_IF;

// TIMER UPDATE FOR INTEGRATION
Timer_Update(IN := NOT Timer_Update.Q, PT := T#100ms);

// 1. EXPLOSIVE VAPOR LEL TRACKING & VENTILATION CONTROL
IF rVaporLEL_Percent >= rCriticalVaporLimit THEN
    bLEL_CriticalShutdown := TRUE;
    bLEL_Warning := TRUE;
    rExhaustFanSpeed_RPM := 3000.0; // Max speed during emergency
ELSIF rVaporLEL_Percent >= (rCriticalVaporLimit - rVaporSafetyMargin) THEN
    bLEL_CriticalShutdown := FALSE;
    bLEL_Warning := TRUE;
    rExhaustFanSpeed_RPM := 2500.0; // High speed
ELSE
    bLEL_CriticalShutdown := FALSE;
    bLEL_Warning := FALSE;
    // Base ventilation on web speed and current evaporation rate estimation
    rExhaustFanSpeed_RPM := 1000.0 + (rWebSpeed_mmin * 2.5) + (rVaporLEL_Percent * 20.0);
END_IF;

// Limit fan speed
IF rExhaustFanSpeed_RPM > 3000.0 THEN
    rExhaustFanSpeed_RPM := 3000.0;
ELSIF rExhaustFanSpeed_RPM < 500.0 AND bEnable THEN
    rExhaustFanSpeed_RPM := 500.0;
END_IF;

IF NOT bEnable THEN
    // Reset outputs and accumulate values if disabled but keep safe fan speed
    aESA_VoltageSetpoint_kV[1] := 0.0;
    bESA_Fault := FALSE;
    RETURN;
END_IF;

// 2. DOCTOR BLADE WEAR COMPENSATION
IF Timer_Update.Q THEN
    // Integrate web length
    rTotalWebLength_m := rTotalWebLength_m + (rWebSpeed_mmin / 600.0); 
    
    // Calculate wear rate based on pressure, speed, and angle
    // Empirical formula for steel blade wear in gravure application
    rWearRate_mm_per_1000m := 0.005 * (rDoctorBladePressure_bar / 2.0) * (rWebSpeed_mmin / 300.0);
    
    // Increment accumulated wear
    rAccumulatedWear_mm := rAccumulatedWear_mm + (rWearRate_mm_per_1000m * (rWebSpeed_mmin / 600.0) / 1000.0);
    
    // Compensation value applied to positioner
    rDoctorBladeComp_mm := rAccumulatedWear_mm;
END_IF;

// 3. ELECTROSTATIC INK ASSIST (ESA) HIGH-VOLTAGE PROFILING
// Dynamic voltage calculation based on speed and ink viscosity
// Higher speed needs more charge transfer, higher viscosity needs more penetration force
rDynamicVoltageTarget_kV := 1.5 + (rWebSpeed_mmin * 0.003) + ((rInkViscosity_mPas - 15.0) * 0.05);

// Cap max voltage
IF rDynamicVoltageTarget_kV > 6.0 THEN
    rDynamicVoltageTarget_kV := 6.0;
END_IF;

bESA_Fault := FALSE;

// Distribute and monitor voltage across the 8 zones
FOR i := 1 TO 8 DO
    aESA_VoltageSetpoint_kV[i] := rDynamicVoltageTarget_kV;
    
    // Fault detection: if feedback differs significantly from setpoint
    IF ABS(aESA_VoltageFeedback_kV[i] - aESA_VoltageSetpoint_kV[i]) > 1.0 THEN
        bESA_Fault := TRUE;
    END_IF;
END_FOR;

// Ensure ESA is off during critical shutdown
IF bLEL_CriticalShutdown THEN
    FOR i := 1 TO 8 DO
        aESA_VoltageSetpoint_kV[i] := 0.0;
    END_FOR;
END_IF;

END_FUNCTION_BLOCK
```"""

prompt = "You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data. Your specific domain is: High-Speed Web Gravure Printing Press. Task: Invent a highly complex control scenario for this domain (e.g., electrostatic ink assist (ESA) high-voltage profiling, doctor blade wear compensation, and explosive vapor LEL tracking). Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": st_code}
    ]
}

os.makedirs("data/swarm_raw", exist_ok=True)
file_name = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(file_name, "w", encoding="utf-8") as f:
    json.dump(record, f)

print(f"File written to {file_name}")
