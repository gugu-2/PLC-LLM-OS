import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Fluidized Bed Dryer (Pharmaceutical Granules).
Task: Invent a highly complex control scenario for this domain (e.g., inlet air temperature/humidity cascade profiles, product moisture capacitance tracking, and exhaust filter pulse-jet cleaning).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."""

st_code = """```iec-st
FUNCTION_BLOCK FB_FluidizedBedDryer_AdvancedControl
TITLE = 'Advanced Control for Pharma Fluidized Bed Dryer'
VERSION : '2.1'
AUTHOR : 'Lumina Swarm Architect'

VAR_INPUT
    // Physical I/O
    rInletAirTemp_PV      : REAL;  // [°C] Inlet air temperature
    rInletAirHum_PV       : REAL;  // [%RH] Inlet air humidity
    rProductTemp_PV       : REAL;  // [°C] Product bed temperature
    rProductMoisture_PV   : REAL;  // [%] Capacitance moisture sensor
    rExhaustPressure_PV   : REAL;  // [Pa] Differential pressure across exhaust filter
    rAirflow_PV           : REAL;  // [m3/h] Primary airflow rate
    
    // Settings & SPs
    rProductTemp_SP       : REAL := 60.0; // [°C] Target product temp
    rProductMoisture_SP   : REAL := 2.5;  // [%] Target end moisture
    rExhaustPress_Max     : REAL := 1500.0; // [Pa] Trigger for pulse jet
    tPulseJetDuration     : TIME := T#200MS;
    tPulseJetInterval     : TIME := T#5S;
    
    bStartDrying          : BOOL;
    bEmergencyStop        : BOOL;
END_VAR

VAR_OUTPUT
    rHeaterValve_CV       : REAL; // [0-100%] Control valve for steam/electric heater
    rDehumValve_CV        : REAL; // [0-100%] Chilled water valve for dehumidification
    rBlowerSpeed_CV       : REAL; // [0-100%] VFD speed for main blower
    
    bPulseJetValve1       : BOOL; // Solenoid for exhaust filter cartridge 1
    bPulseJetValve2       : BOOL; // Solenoid for exhaust filter cartridge 2
    
    bDryingComplete       : BOOL;
    bAlarm_HighPressure   : BOOL;
    bAlarm_OverTemp       : BOOL;
END_VAR

VAR
    // Internal States
    eState                : INT := 0; // 0: Idle, 1: Pre-Heat, 2: Main Drying, 3: Cooling, 4: Pulse Clean
    
    // PID Controllers
    pidTempCascade        : FB_PID_Cascade;
    pidMoisture           : FB_PID_Standard;
    
    // Timers
    tonPulseInterval      : TON;
    tofPulseDuration      : TOF;
    
    rInletTemp_SP_Casc    : REAL;
    bToggleCartridge      : BOOL;
    
    // Capacitance tracking algorithm
    rMoistureIntegral     : REAL := 0.0;
    rMoistureDerivative   : REAL := 0.0;
    rLastMoisture         : REAL := 0.0;
END_VAR

// --- MAIN ALGORITHM ---

// Safety Interlocks
IF bEmergencyStop THEN
    rHeaterValve_CV := 0.0;
    rDehumValve_CV  := 0.0;
    rBlowerSpeed_CV := 0.0;
    bPulseJetValve1 := FALSE;
    bPulseJetValve2 := FALSE;
    eState := 0;
    RETURN;
END_IF;

// Pulse-Jet Cleaning Logic (Continuous Background Process based on dP)
bAlarm_HighPressure := (rExhaustPressure_PV > (rExhaustPress_Max * 1.2));

tonPulseInterval(IN := (rExhaustPressure_PV > rExhaustPress_Max) AND bStartDrying, PT := tPulseJetInterval);
IF tonPulseInterval.Q THEN
    bToggleCartridge := NOT bToggleCartridge;
    tonPulseInterval(IN := FALSE); // Reset timer
END_IF;

tofPulseDuration(IN := tonPulseInterval.Q, PT := tPulseJetDuration);

IF tofPulseDuration.Q THEN
    IF bToggleCartridge THEN
        bPulseJetValve1 := TRUE;
        bPulseJetValve2 := FALSE;
    ELSE
        bPulseJetValve1 := FALSE;
        bPulseJetValve2 := TRUE;
    END_IF;
ELSE
    bPulseJetValve1 := FALSE;
    bPulseJetValve2 := FALSE;
END_IF;

// Moisture tracking derivation
rMoistureDerivative := rProductMoisture_PV - rLastMoisture;
rLastMoisture := rProductMoisture_PV;

// State Machine
CASE eState OF
    0: // IDLE
        bDryingComplete := FALSE;
        rHeaterValve_CV := 0.0;
        rDehumValve_CV := 0.0;
        IF bStartDrying THEN
            eState := 1;
        END_IF;
        
    1: // PRE-HEAT
        rBlowerSpeed_CV := 50.0; // Constant low flow for pre-heat
        // Target specific inlet temp
        pidTempCascade.rSetPoint := 50.0; 
        pidTempCascade.rProcessValue := rInletAirTemp_PV;
        pidTempCascade();
        rHeaterValve_CV := pidTempCascade.rControlValue;
        
        IF rProductTemp_PV >= 40.0 THEN
            eState := 2; // Move to main drying once bed is warm
        END_IF;
        
    2: // MAIN DRYING
        // Cascade control: Product temp SP dictates Inlet Temp SP
        pidMoisture.rSetPoint := rProductTemp_SP;
        pidMoisture.rProcessValue := rProductTemp_PV;
        pidMoisture();
        
        // Limit inlet temp to prevent product degradation
        rInletTemp_SP_Casc := pidMoisture.rControlValue;
        IF rInletTemp_SP_Casc > 85.0 THEN
            rInletTemp_SP_Casc := 85.0;
        END_IF;
        
        pidTempCascade.rSetPoint := rInletTemp_SP_Casc;
        pidTempCascade.rProcessValue := rInletAirTemp_PV;
        pidTempCascade();
        rHeaterValve_CV := pidTempCascade.rControlValue;
        
        // Humidity control
        IF rInletAirHum_PV > 15.0 THEN
            rDehumValve_CV := (rInletAirHum_PV - 15.0) * 5.0; 
        ELSE
            rDehumValve_CV := 0.0;
        END_IF;
        
        rBlowerSpeed_CV := 80.0;
        
        // Moisture endpoint detection
        IF rProductMoisture_PV <= rProductMoisture_SP AND rMoistureDerivative > -0.05 THEN
            eState := 3;
        END_IF;
        
    3: // COOLING
        rHeaterValve_CV := 0.0;
        rDehumValve_CV := 100.0; // Max dry air for cooling
        rBlowerSpeed_CV := 60.0;
        
        IF rProductTemp_PV < 35.0 THEN
            bDryingComplete := TRUE;
            eState := 0;
        END_IF;
        
END_CASE;

// Alarms
bAlarm_OverTemp := rProductTemp_PV > (rProductTemp_SP + 10.0) OR rInletAirTemp_PV > 95.0;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
os.makedirs("data", exist_ok=True)

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": st_code}]}

file_id = uuid.uuid4().hex[:8]
swarm_file = f"data/swarm_raw/agent_{file_id}.json"
with open(swarm_file, "w", encoding="utf-8") as f:
    json.dump(record, f)
    
jsonl_file = "data/synthetic_generation_v3_enterprise.jsonl"
with open(jsonl_file, "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\n")
    
print(f"Saved to {swarm_file} and {jsonl_file}")
