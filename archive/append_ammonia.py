import json

file_path = r"c:\Users\majip\Downloads\LLM REASEARCH\data\synthetic_generation_v3_enterprise.jsonl"

user_content = "You are acting as a Lead Chemical Engineer for an Ammonia Plant. Evolve a basic temperature block into a Haber-Bosch Synthesis Loop Controller. Technical Specs: 1. Extreme pressure (200 bar) and temperature (450C) profiling over the iron catalyst beds. 2. Hydrogen-to-Nitrogen (H2:N2) ratio cross-limiting control. 3. Syngas make-up compressor anti-surge matrices. Append to synthetic_generation_v3_enterprise.jsonl."

assistant_content = """```iecst
(*
================================================================================
FUNCTION BLOCK: FB_HaberBosch_SynthesisLoop
VERSION: 3.1.0 (Enterprise-Grade)
AUTHOR: Lumina Elite Synthetic Data Architect
DESCRIPTION: 
Advanced control of a Haber-Bosch ammonia synthesis loop.
Includes:
1. Pressure & Temperature profiling (Nominal 200 bar, 450°C) across 3-bed iron catalyst.
2. H2:N2 Stoichiometric ratio cross-limiting control (Target 3:1).
3. Make-up syngas compressor anti-surge protection using algorithmic matrices.
================================================================================
*)

FUNCTION_BLOCK FB_HaberBosch_SynthesisLoop

VAR_INPUT
    // Process Variables (PV)
    rBed1_Temp_PV       : REAL; // °C (Target 400-450)
    rBed2_Temp_PV       : REAL; // °C (Target 420-470)
    rBed3_Temp_PV       : REAL; // °C (Target 430-480)
    rLoop_Pressure_PV   : REAL; // Bar (Target ~200)
    
    // Gas composition (Analyzer)
    rH2_Concentration   : REAL; // % (Target ~75%)
    rN2_Concentration   : REAL; // % (Target ~25%)
    
    // Compressor Variables
    rComp_Flow_PV       : REAL; // Nm3/h
    rComp_Disch_Press   : REAL; // Bar
    rComp_Speed         : REAL; // RPM
    
    // Setpoints
    rTemp_SP            : REAL := 450.0;
    rPressure_SP        : REAL := 200.0;
    rH2_N2_Ratio_SP     : REAL := 3.0; // Ideal stoichiometry
    
    // Commands
    bEnable_Controller  : BOOL;
    bEmergency_Trip     : BOOL;
END_VAR

VAR_OUTPUT
    // Manipulated Variables (MV)
    rBed1_Quench_CV     : REAL; // 0-100% (Cold syngas bypass valve)
    rBed2_Quench_CV     : REAL; // 0-100%
    
    rH2_Feed_CV         : REAL; // 0-100% H2 make-up valve
    rN2_Feed_CV         : REAL; // 0-100% N2 make-up valve
    
    rComp_AntiSurge_CV  : REAL; // 0-100% Recycle valve for surge protection
    
    // Status & Alarms
    bCatalyst_Temp_HiHi : BOOL;
    bPressure_HiHi      : BOOL;
    bSurge_Warning      : BOOL;
    bTrip_Active        : BOOL;
END_VAR

VAR
    // Internal PID blocks
    pidBed1_Temp        : FB_PID_Advanced;
    pidBed2_Temp        : FB_PID_Advanced;
    pidRatio_Master     : FB_PID_Advanced;
    pidH2_Feed          : FB_PID_Advanced;
    pidN2_Feed          : FB_PID_Advanced;
    
    // Surge Matrix Arrays (3x3 Operating Map)
    arSurge_Flow_Map    : ARRAY[1..3] OF REAL := [1000.0, 2500.0, 5000.0];
    arSurge_Press_Map   : ARRAY[1..3] OF REAL := [100.0, 150.0, 220.0];
    rSurge_Margin       : REAL;
    
    // Cross-limiting internal vars
    rCurrentRatio       : REAL;
    rH2_Demand          : REAL;
    rN2_Demand          : REAL;
    
    // Timers
    tonTripDelay        : TON;
END_VAR

// --- [1] SAFETY AND TRIP LOGIC ---
IF bEmergency_Trip OR (rLoop_Pressure_PV > 220.0) OR (rBed3_Temp_PV > 520.0) THEN
    bTrip_Active := TRUE;
    rBed1_Quench_CV := 100.0; // Max quench to cool
    rBed2_Quench_CV := 100.0;
    rH2_Feed_CV := 0.0;
    rN2_Feed_CV := 0.0;
    rComp_AntiSurge_CV := 100.0; // Fully open recycle
    RETURN;
END_IF;

IF NOT bEnable_Controller THEN
    bTrip_Active := FALSE;
    RETURN;
END_IF;

// --- [2] TEMPERATURE PROFILING OVER IRON CATALYST (QUENCH CONTROL) ---
// Iron catalyst operates optimally between 400C and 500C. Exothermic reaction.
// We control Bed 1 and Bed 2 inlet temperatures by bypassing cold syngas (quench).
pidBed1_Temp(
    EN := TRUE,
    PV := rBed1_Temp_PV,
    SP := rTemp_SP - 15.0, // Bed 1 target slightly lower
    Kp := 1.2, Ti := 45.0, Td := 5.0,
    CV => rBed1_Quench_CV
);

pidBed2_Temp(
    EN := TRUE,
    PV := rBed2_Temp_PV,
    SP := rTemp_SP + 5.0, // Bed 2 takes more heat
    Kp := 1.5, Ti := 40.0, Td := 6.0,
    CV => rBed2_Quench_CV
);

bCatalyst_Temp_HiHi := (rBed1_Temp_PV > 500.0) OR (rBed2_Temp_PV > 510.0) OR (rBed3_Temp_PV > 520.0);
bPressure_HiHi := (rLoop_Pressure_PV > 215.0);

// --- [3] H2:N2 RATIO CROSS-LIMITING CONTROL ---
// Safely adjust H2 and N2 feeds to maintain 3:1 ratio without starving either.
IF rN2_Concentration > 0.0 THEN
    rCurrentRatio := rH2_Concentration / rN2_Concentration;
ELSE
    rCurrentRatio := 3.0;
END_IF;

// Master Ratio Controller dictates overall feed demand based on pressure
pidRatio_Master(
    EN := TRUE,
    PV := rLoop_Pressure_PV,
    SP := rPressure_SP, // 200 bar
    Kp := 2.5, Ti := 120.0, Td := 0.0,
    CV => rH2_Demand // Baseline demand goes to H2
);

// Cross-Limiting: N2 demand is slaved to actual H2 flow/concentration to ensure stoichiometry
rN2_Demand := rH2_Demand / rH2_N2_Ratio_SP;

// If current ratio is too high (excess H2), limit H2 feed
IF rCurrentRatio > (rH2_N2_Ratio_SP + 0.2) THEN
    rH2_Demand := rH2_Demand * 0.9;
END_IF;

pidH2_Feed(EN := TRUE, PV := rH2_Concentration, SP := 75.0, Kp := 0.8, Ti := 30.0, CV => rH2_Feed_CV);
pidN2_Feed(EN := TRUE, PV := rN2_Concentration, SP := 25.0, Kp := 0.8, Ti := 30.0, CV => rN2_Feed_CV);

// --- [4] SYNGAS MAKE-UP COMPRESSOR ANTI-SURGE MATRICES ---
// Evaluate operating point against surge map (Flow vs Pressure)
// simplified distance-to-surge calculation
rSurge_Margin := (rComp_Flow_PV / arSurge_Flow_Map[3]) - (rComp_Disch_Press / arSurge_Press_Map[3]);

IF rSurge_Margin < 0.15 THEN
    bSurge_Warning := TRUE;
    // Proportional opening of anti-surge recycle valve
    rComp_AntiSurge_CV := (0.15 - rSurge_Margin) * 1000.0; 
    IF rComp_AntiSurge_CV > 100.0 THEN rComp_AntiSurge_CV := 100.0; END_IF;
ELSE
    bSurge_Warning := FALSE;
    // Slowly close anti-surge valve if safe
    rComp_AntiSurge_CV := rComp_AntiSurge_CV - 0.5;
    IF rComp_AntiSurge_CV < 0.0 THEN rComp_AntiSurge_CV := 0.0; END_IF;
END_IF;

END_FUNCTION_BLOCK

// --- Helper PID Block stub ---
FUNCTION_BLOCK FB_PID_Advanced
VAR_INPUT
    EN: BOOL; PV: REAL; SP: REAL; Kp: REAL; Ti: REAL; Td: REAL;
END_VAR
VAR_OUTPUT
    CV: REAL;
END_VAR
VAR
    e, e_last, integral: REAL;
END_VAR
IF EN THEN
    e := SP - PV;
    integral := integral + e;
    CV := Kp * e + (Kp/MAX(Ti,0.001)) * integral + (Kp*Td) * (e - e_last);
    IF CV > 100.0 THEN CV := 100.0; ELSIF CV < 0.0 THEN CV := 0.0; END_IF;
    e_last := e;
ELSE
    CV := 0.0; integral := 0.0;
END_IF;
END_FUNCTION_BLOCK
```"""

payload = {
    "messages": [
        {"role": "user", "content": user_content},
        {"role": "assistant", "content": assistant_content}
    ]
}

with open(file_path, "a", encoding="utf-8") as f:
    f.write(json.dumps(payload) + "\n")

print("Appended successfully.")
