import os, json, uuid

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Superconducting Fault Current Limiter (SFCL) Substation Protection**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Ultra-fast transient quench detection within 2ms, liquid nitrogen level/pressure regulation, and grid re-synchronization post-fault recovery). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

CRITICAL RULES - READ EVERY LINE:
1. CODE FENCE: Use TRIPLE backticks + iec-st. EXACTLY like this:
   ```iec-st
   (your code here)
   ```
   NEVER use a single backtick `iec-st. ALWAYS use triple backticks.
2. REQUIRED IEC 61131-3 STRUCTURE (all 5 mandatory):
   a. FUNCTION_BLOCK FB_<Name>   <- first line of code, always
   b. VAR_INPUT ... END_VAR      <- min 4 typed inputs with comments
   c. VAR_OUTPUT ... END_VAR     <- min 3 typed outputs with comments
   d. At least one END_IF; or END_CASE;  <- control logic required
   e. END_FUNCTION_BLOCK         <- last line of code, always
3. LENGTH: The assistant content MUST be >= 1500 characters total.
4. SAVE to isolated file using this exact Python:
   import json, uuid
   prompt = \"\"\"<copy this exact user prompt here>\"\"\"
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_SFCL_Substation\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
   record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
   with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
       json.dump(record, f, ensure_ascii=False)
5. SELF-CHECK before saving - verify ALL:
   [ ] Fence is ```iec-st
   [ ] First code line: FUNCTION_BLOCK FB_<name>
   [ ] Has VAR_INPUT section
   [ ] Has VAR_OUTPUT section
   [ ] Has END_IF; or END_CASE;
   [ ] Last code line: END_FUNCTION_BLOCK
   [ ] Closing fence: ```
   [ ] Total chars >= 1500
6. REPLY with: EVOLUTION COMPLETE: Superconducting Fault Current Limiter (SFCL) Substation Protection

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_SFCL_Protection_Control
VAR_INPUT
    (* Physical Inputs for SFCL Protection *)
    bEnableSys          : BOOL;     (* System master enable *)
    bEmergencyStop      : BOOL;     (* Safety circuit loop OK *)
    rGridCurrent_A      : REAL;     (* High-speed phase current measurement (Amps) *)
    rGridVoltage_V      : REAL;     (* High-speed phase voltage measurement (Volts) *)
    rLN2_Level_pct      : REAL;     (* Liquid Nitrogen level (0-100%) *)
    rLN2_Pressure_bar   : REAL;     (* Cryostat internal pressure (bar) *)
    rLN2_Temp_K         : REAL;     (* Superconductor temperature (Kelvin) *)
    bGridSyncPulse      : BOOL;     (* External synchronization pulse *)
END_VAR
VAR_OUTPUT
    (* Control and Status Outputs *)
    bBreakerTrip        : BOOL;     (* Fast trip signal to main grid breaker *)
    bQuenchDetected     : BOOL;     (* Superconducting quench event flag *)
    rCoolingValveCmd    : REAL;     (* Cryo cooling valve command (0-100%) *)
    rPressureVentCmd    : REAL;     (* Pressure relief valve command (0-100%) *)
    iSystemState        : INT;      (* Current operational state machine step *)
    bSystemAlarm        : BOOL;     (* Critical alarm output *)
END_VAR
VAR
    (* Internal state and memory variables *)
    iState              : INT := 0;
    rCurrentDerivative  : REAL := 0.0;
    rLastCurrent        : REAL := 0.0;
    rFilteredTemp       : REAL := 77.0;
    rFilteredLevel      : REAL := 100.0;
    
    (* Timers and triggers *)
    tStartupDelay       : TON;
    tRecoveryTimer      : TON;
    tQuenchCooldown     : TON;
    
    (* Thresholds and tuning parameters *)
    c_rQuenchThresholdA : REAL := 15000.0; (* 15 kA fault threshold *)
    c_rQuenchDiDtMax    : REAL := 5000.0;  (* 5 kA/ms derivative limit *)
    c_rTempMax_K        : REAL := 82.0;    (* Critical temp threshold *)
    
    (* PID variables for pressure control *)
    rPressKp            : REAL := 2.5;
    rPressKi            : REAL := 0.1;
    rPressError         : REAL := 0.0;
    rPressIntegral      : REAL := 0.0;
    
    (* Cycle counters *)
    wCycleCount         : WORD := 0;
END_VAR

(* === MAIN LOGIC === *)

(* 1. Safety Interlocks & Emergency Handling *)
IF NOT bEmergencyStop THEN
    bBreakerTrip := TRUE;
    rCoolingValveCmd := 100.0; (* Max cooling on E-Stop *)
    rPressureVentCmd := 100.0; (* Vent pressure safely *)
    bSystemAlarm := TRUE;
    iState := 999; (* Fault State *)
    iSystemState := iState;
    RETURN;
END_IF;

(* 2. Signal Filtering (Moving Average / First-order lag) *)
rFilteredTemp := rFilteredTemp + 0.1 * (rLN2_Temp_K - rFilteredTemp);
rFilteredLevel := rFilteredLevel + 0.05 * (rLN2_Level_pct - rFilteredLevel);

(* 3. Ultra-fast Transient Quench Detection (simulated 1ms cycle) *)
rCurrentDerivative := ABS(rGridCurrent_A - rLastCurrent);
rLastCurrent := rGridCurrent_A;

IF (ABS(rGridCurrent_A) > c_rQuenchThresholdA) OR (rCurrentDerivative > c_rQuenchDiDtMax) THEN
    bQuenchDetected := TRUE;
END_IF;

(* 4. State Machine for SFCL Substation Logic *)
CASE iState OF
    0: (* INIT / IDLE *)
        bBreakerTrip := FALSE;
        bQuenchDetected := FALSE;
        rCoolingValveCmd := 0.0;
        rPressureVentCmd := 0.0;
        bSystemAlarm := FALSE;
        
        IF bEnableSys AND (rFilteredTemp < c_rTempMax_K) THEN
            iState := 10;
        END_IF;
        
    10: (* PRE-COOLING AND PRESSURIZATION *)
        rCoolingValveCmd := 80.0; (* Pre-chill phase *)
        tStartupDelay(IN := TRUE, PT := T#10S);
        
        IF tStartupDelay.Q THEN
            tStartupDelay(IN := FALSE);
            iState := 20; (* READY *)
        END_IF;
        
    20: (* ONLINE / MONITORING *)
        (* PID Control for LN2 Pressure *)
        rPressError := 1.5 - rLN2_Pressure_bar; (* Target 1.5 bar *)
        rPressIntegral := rPressIntegral + (rPressError * 0.01);
        rPressureVentCmd := (rPressKp * rPressError) + (rPressKi * rPressIntegral);
        
        (* Limit outputs *)
        IF rPressureVentCmd > 100.0 THEN rPressureVentCmd := 100.0; END_IF;
        IF rPressureVentCmd < 0.0 THEN rPressureVentCmd := 0.0; END_IF;
        
        (* Level maintenance *)
        IF rFilteredLevel < 85.0 THEN
            rCoolingValveCmd := 50.0;
        ELSIF rFilteredLevel > 95.0 THEN
            rCoolingValveCmd := 10.0;
        END_IF;
        
        (* Quench Protection Tripping *)
        IF bQuenchDetected OR (rFilteredTemp >= c_rTempMax_K) THEN
            bBreakerTrip := TRUE;
            bSystemAlarm := TRUE;
            iState := 30;
        END_IF;
        
    30: (* FAULT RECOVERY & COOLDOWN *)
        rCoolingValveCmd := 100.0; (* Max flood *)
        rPressureVentCmd := 50.0;  (* Manage boil-off gas *)
        
        tQuenchCooldown(IN := TRUE, PT := T#60S);
        IF tQuenchCooldown.Q AND (rFilteredTemp < 78.0) AND bGridSyncPulse THEN
            tQuenchCooldown(IN := FALSE);
            bQuenchDetected := FALSE;
            bSystemAlarm := FALSE;
            iState := 40;
        END_IF;
        
    40: (* GRID RE-SYNCHRONIZATION *)
        IF bGridSyncPulse AND (ABS(rGridVoltage_V) < 100.0) THEN
            bBreakerTrip := FALSE; (* Re-close breaker on zero crossing *)
            iState := 20; (* Return to ONLINE *)
        END_IF;
        
    999: (* FAULT LOCKOUT *)
        (* Requires manual reset via E-Stop toggle and Enable clear *)
        IF NOT bEnableSys AND bEmergencyStop THEN
            iState := 0;
        END_IF;
        
END_CASE;

iSystemState := iState;
wCycleCount := wCycleCount + 1;

END_FUNCTION_BLOCK
```"""

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": code}
    ]
}

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
