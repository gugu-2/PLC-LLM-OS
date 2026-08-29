import os, json, uuid
os.makedirs('data/swarm_raw', exist_ok=True)
os.makedirs('data', exist_ok=True)

prompt = "Generate a highly complex IEC 61131-3 Structured Text FUNCTION_BLOCK for an Advanced Waste-to-Energy Incinerator. Include moving grate combustion optimization, selective catalytic reduction (SCR) urea injection, and baghouse pulse-jet cleaning with physical I/O and comprehensive VAR declarations."

st_code = """FUNCTION_BLOCK FB_WTE_Incinerator_Control
TITLE = 'Advanced Waste-to-Energy Incinerator Control'
VERSION : '2.1'
AUTHOR : 'Lumina AI Cloud Swarm'

VAR_INPUT
    rWasteFeedRate       : REAL; // Tons per hour
    rPrimaryAirTemp      : REAL; // Celsius
    rSecondaryAirFlow    : REAL; // m3/h
    rFurnaceTemp         : REAL; // Celsius (Target > 850C for 2 seconds)
    rO2Level             : REAL; // Percentage in flue gas
    rNOxConcentration    : REAL; // mg/Nm3
    rSCRTemp             : REAL; // Celsius
    bUreaTankLevelLow    : BOOL;
    rDiffPressure        : REAL; // mbar across baghouse filter
    rFlueGasFlow         : REAL; // m3/h
END_VAR

VAR_OUTPUT
    rGrateSpeedCmd       : REAL; // 0-100%
    rPrimaryAirCmd       : REAL; // 0-100% valve position
    rSecondaryAirCmd     : REAL; // 0-100% valve position
    rUreaDosingCmd       : REAL; // L/h
    bAtomizationAirVlv   : BOOL; // Open/Close
    bPulseJetValve1      : BOOL;
    bPulseJetValve2      : BOOL;
    bPulseJetValve3      : BOOL;
    bAlarmFurnaceTempLow : BOOL;
    bAlarmNOxHigh        : BOOL;
    bAlarmFilterClogged  : BOOL;
END_VAR

VAR
    tFurnaceTempTimer    : TON;
    tPulseJetTimer       : TON;
    iPulseSeqStep        : INT := 1;
    rGratePID_Error      : REAL;
    rGratePID_Int        : REAL;
    rGrateKp             : REAL := 1.5;
    rGrateKi             : REAL := 0.05;
    rUreaPID_Error       : REAL;
    rUreaPID_Int         : REAL;
    rUreaKp              : REAL := 2.2;
    rUreaKi              : REAL := 0.1;
    rTargetFurnaceTemp   : REAL := 950.0; // Setpoint
    rTargetNOx           : REAL := 45.0;  // Emission limit
    rMaxDiffPressure     : REAL := 15.0;  // mbar
    rMinSCRTemp          : REAL := 200.0; // Min temp for urea injection
END_VAR

// ==============================================================================
// 1. MOVING GRATE COMBUSTION OPTIMIZATION
// ==============================================================================

tFurnaceTempTimer(IN := (rFurnaceTemp < 850.0), PT := T#2S);
bAlarmFurnaceTempLow := tFurnaceTempTimer.Q;

rGratePID_Error := rTargetFurnaceTemp - rFurnaceTemp;
rGratePID_Int := rGratePID_Int + (rGratePID_Error * 0.1);

IF rGratePID_Int > 50.0 THEN rGratePID_Int := 50.0; END_IF;
IF rGratePID_Int < -50.0 THEN rGratePID_Int := -50.0; END_IF;

rGrateSpeedCmd := (rGrateKp * rGratePID_Error) + (rGrateKi * rGratePID_Int) + 50.0;

IF rGrateSpeedCmd > 100.0 THEN rGrateSpeedCmd := 100.0; END_IF;
IF rGrateSpeedCmd < 10.0 THEN rGrateSpeedCmd := 10.0; END_IF;

IF rO2Level < 5.0 THEN
    rSecondaryAirCmd := 80.0;
    rPrimaryAirCmd := 60.0;
ELSIF rO2Level > 9.0 THEN
    rSecondaryAirCmd := 30.0;
    rPrimaryAirCmd := 40.0;
ELSE
    rSecondaryAirCmd := 55.0;
    rPrimaryAirCmd := 50.0;
END_IF;

// ==============================================================================
// 2. SELECTIVE CATALYTIC REDUCTION (SCR) UREA INJECTION
// ==============================================================================

bAlarmNOxHigh := (rNOxConcentration > 200.0);

IF rSCRTemp >= rMinSCRTemp AND NOT bUreaTankLevelLow THEN
    bAtomizationAirVlv := TRUE;
    rUreaPID_Error := rNOxConcentration - rTargetNOx;
    rUreaPID_Int := rUreaPID_Int + (rUreaPID_Error * 0.1);
    
    IF rUreaPID_Int > 100.0 THEN rUreaPID_Int := 100.0; END_IF;
    IF rUreaPID_Int < 0.0 THEN rUreaPID_Int := 0.0; END_IF;

    IF rUreaPID_Error > 0.0 THEN
        rUreaDosingCmd := (rUreaKp * rUreaPID_Error) + (rUreaKi * rUreaPID_Int);
    ELSE
        rUreaDosingCmd := 2.0;
    END_IF;
ELSE
    bAtomizationAirVlv := FALSE;
    rUreaDosingCmd := 0.0;
END_IF;

// ==============================================================================
// 3. BAGHOUSE PULSE-JET CLEANING
// ==============================================================================

bAlarmFilterClogged := (rDiffPressure > 25.0);

IF rDiffPressure > rMaxDiffPressure THEN
    tPulseJetTimer(IN := NOT tPulseJetTimer.Q, PT := T#5S);
    
    IF tPulseJetTimer.Q THEN
        iPulseSeqStep := iPulseSeqStep + 1;
        IF iPulseSeqStep > 4 THEN
            iPulseSeqStep := 1;
        END_IF;
    END_IF;
    
    bPulseJetValve1 := (iPulseSeqStep = 1);
    bPulseJetValve2 := (iPulseSeqStep = 2);
    bPulseJetValve3 := (iPulseSeqStep = 3);
ELSE
    tPulseJetTimer(IN := FALSE);
    iPulseSeqStep := 1;
    bPulseJetValve1 := FALSE;
    bPulseJetValve2 := FALSE;
    bPulseJetValve3 := FALSE;
END_IF;

END_FUNCTION_BLOCK"""

assistant_content = f"```iec-st\n{st_code}\n```"
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": assistant_content}]}

uid = uuid.uuid4().hex[:8]

swarm_file = f"data/swarm_raw/agent_{uid}.json"
with open(swarm_file, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)
print(f"Saved {swarm_file}")

jsonl_file = "data/synthetic_generation_v3_enterprise.jsonl"
with open(jsonl_file, "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\n")
print(f"Appended to {jsonl_file}")
