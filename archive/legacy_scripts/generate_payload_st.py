import json, uuid, os

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Anaerobic Digester Biogas Plant.
Task: Invent a highly complex control scenario for this domain (e.g., sludge heat exchanger thermal cascades, methane/H2S gas flaring logic, and CHP (Combined Heat and Power) genset load balancing).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."""

code = """```iec-st
FUNCTION_BLOCK FB_AnaerobicDigesterControl
VAR_INPUT
    rSludgeTempIn       : REAL; // Sludge temperature from primary digester [°C]
    rSludgeFlowRate     : REAL; // Sludge flow rate [m3/h]
    rMethaneLevel       : REAL; // Methane (CH4) concentration in biogas [%]
    rH2SLevel           : REAL; // Hydrogen Sulfide (H2S) concentration [ppm]
    rBiogasPressure     : REAL; // Biogas holder pressure [mbar]
    rGridDemandKW       : REAL; // Electrical grid power demand [kW]
    bGensetReady        : BOOL; // CHP Genset ready status
    bEmergencyStop      : BOOL; // E-Stop active
END_VAR
VAR_OUTPUT
    rHeatExchangerValve : REAL; // Heating loop mixing valve position [0-100%]
    rFlareValvePos      : REAL; // Flare gas control valve position [0-100%]
    rCHPPowerSetpoint   : REAL; // Power setpoint to CHP unit [kW]
    bFlareIgnition      : BOOL; // Command to ignite gas flare
    bDesulfurizationOn  : BOOL; // H2S scrubber system active
    bSystemAlarm        : BOOL; // General fault alarm
    iErrorCode          : INT;  // Specific error code
END_VAR
VAR
    rTargetSludgeTemp   : REAL := 38.5; // Mesophilic target temp [°C]
    rMaxBiogasPressure  : REAL := 25.0; // Max allowable pressure [mbar]
    rFlareStartPressure : REAL := 22.0; // Flare cut-in pressure [mbar]
    rH2SLimit           : REAL := 200.0;// Max H2S before scrubbing [ppm]
    
    // PID state variables
    rTempError          : REAL;
    rTempIntegral       : REAL;
    rTempDerivative     : REAL;
    rTempLastError      : REAL;
    
    // Timers
    tFlareTimer         : TON;
    tGensetTimer        : TON;
END_VAR

// --- E-Stop Logic ---
IF bEmergencyStop THEN
    rHeatExchangerValve := 0.0;
    rFlareValvePos := 100.0; // Vent to flare
    bFlareIgnition := TRUE;
    rCHPPowerSetpoint := 0.0;
    bDesulfurizationOn := FALSE;
    bSystemAlarm := TRUE;
    iErrorCode := 999;
    RETURN;
END_IF;

// --- Sludge Heating Cascade Control (PID approximation) ---
rTempError := rTargetSludgeTemp - rSludgeTempIn;
rTempIntegral := rTempIntegral + rTempError * 0.1; 
rTempDerivative := (rTempError - rTempLastError) / 0.1;
rTempLastError := rTempError;

rHeatExchangerValve := (rTempError * 5.0) + (rTempIntegral * 0.2) + (rTempDerivative * 0.1);
IF rHeatExchangerValve > 100.0 THEN rHeatExchangerValve := 100.0; END_IF;
IF rHeatExchangerValve < 0.0 THEN rHeatExchangerValve := 0.0; END_IF;

// --- Gas Management & Flaring Logic ---
IF rH2SLevel > rH2SLimit THEN
    bDesulfurizationOn := TRUE;
ELSE
    bDesulfurizationOn := FALSE;
END_IF;

IF rBiogasPressure > rFlareStartPressure THEN
    rFlareValvePos := (rBiogasPressure - rFlareStartPressure) * 10.0; // Proportional flaring
    IF rFlareValvePos > 100.0 THEN rFlareValvePos := 100.0; END_IF;
    
    tFlareTimer(IN := TRUE, PT := T#5S);
    IF tFlareTimer.Q THEN
        bFlareIgnition := TRUE;
    END_IF;
ELSE
    rFlareValvePos := 0.0;
    bFlareIgnition := FALSE;
    tFlareTimer(IN := FALSE);
END_IF;

// --- CHP Genset Load Balancing ---
IF bGensetReady AND rMethaneLevel > 50.0 AND rBiogasPressure > 5.0 THEN
    // Calculate max power possible based on gas flow & methane content (simplified)
    rCHPPowerSetpoint := rGridDemandKW;
    // Cap at some arbitrary max power, e.g. 500kW
    IF rCHPPowerSetpoint > 500.0 THEN
        rCHPPowerSetpoint := 500.0;
    END_IF;
ELSE
    rCHPPowerSetpoint := 0.0;
END_IF;

// --- Alarms ---
IF rBiogasPressure > rMaxBiogasPressure THEN
    bSystemAlarm := TRUE;
    iErrorCode := 101; // Overpressure
ELSIF rSludgeTempIn > 42.0 THEN
    bSystemAlarm := TRUE;
    iErrorCode := 102; // Overheating
ELSE
    bSystemAlarm := FALSE;
    iErrorCode := 0;
END_IF;

END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
    json.dump(record, f)
