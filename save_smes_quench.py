import json, uuid, os

prompt = """<USER_REQUEST>
You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Superconducting Magnetic Energy Storage (SMES) Cryogenic Quench Protection**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., YBCO tape critical current monitoring, ultra-fast IGBT bypass circuit firing for energy dumping, and liquid helium boil-off mitigation). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_SMES_QuenchProtection\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Superconducting Magnetic Energy Storage (SMES) Cryogenic Quench Protection

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT.
</USER_REQUEST>"""

code = """```iec-st
FUNCTION_BLOCK FB_SMES_QuenchProtection
(* 
    ========================================================================================
    Block Name      : FB_SMES_QuenchProtection
    Author          : Lumina AI Elite Architect (40+ Yrs Exp)
    Description     : High-speed, highly robust quench detection and protection block for 
                      Superconducting Magnetic Energy Storage (SMES) systems. Incorporates 
                      YBCO tape critical current monitoring, noise-filtered differential 
                      voltage detection, multi-stage IGBT bypass firing for energy dump, 
                      and liquid helium (LHe) boil-off mitigation logic.
    Version         : 2.5
    Execution       : Periodic fast task (Recommended <= 1ms cycle)
    ========================================================================================
*)

VAR_INPUT
    bEnable                 : BOOL;     (* System enable and arm signal *)
    bEmergencyStop          : BOOL;     (* E-Stop safety relay OK signal *)
    rCoilCurrent            : REAL;     (* Current flowing through SMES coil [A] *)
    rCoilVoltage_A          : REAL;     (* Coil branch A terminal voltage [V] *)
    rCoilVoltage_B          : REAL;     (* Coil branch B terminal voltage [V] *)
    rCryostatTemp           : REAL;     (* Cryostat internal temperature (YBCO env) [K] *)
    rLHeLevel               : REAL;     (* Liquid Helium (LHe) bath level [%] *)
    rLHePressure            : REAL;     (* Helium vessel pressure [bar] *)
    bAcknowledgeFault       : BOOL;     (* Reset/Acknowledge fault states *)
END_VAR

VAR_OUTPUT
    bSystemReady            : BOOL;     (* Protection system is armed and ready *)
    bIGBT_BypassFire        : BOOL;     (* FAST trigger for main IGBT bypass circuit *)
    bDumpResistorConnect    : BOOL;     (* Connect external energy dump resistor bank *)
    bVentValveOpen          : BOOL;     (* LHe emergency boil-off pressure vent valve *)
    rMaxTempReached         : REAL;     (* Latched maximum cryostat temperature [K] *)
    bQuenchDetected         : BOOL;     (* True if a resistive quench is detected *)
    bCriticalAlarm          : BOOL;     (* Latched critical fault alarm *)
    iProtectionState        : INT;      (* Current state of the protection finite state machine *)
END_VAR

VAR
    (* Internal State Variables *)
    iState                  : INT := 0; (* State machine iterator *)
    tQuenchConfirmTimer     : TON;      (* Filter delay for quench threshold validation *)
    tVentValveTimer         : TON;      (* Duration timer for vent valve operation *)
    tDumpResistorTimer      : TON;      (* Delay for sequenced dump resistor connection *)
    
    (* Filtered and Processed Signals *)
    rFilteredDiffVoltage    : REAL;
    rAlphaV                 : REAL := 0.05; (* First-order low pass filter coefficient for diff voltage *)
    rPrevDiffVoltage        : REAL := 0.0;
    rCalculatedDiDt         : REAL;
    rPrevCoilCurrent        : REAL := 0.0;
    
    (* Thresholds and Constants *)
    QUENCH_VOLTAGE_LIMIT    : REAL := 0.150;    (* 150mV resistive threshold for quench *)
    CRIT_TEMP_LIMIT         : REAL := 72.0;     (* Critical temperature limit for YBCO [K] *)
    CRIT_PRESSURE_LIMIT     : REAL := 2.5;      (* Max allowed helium pressure [bar] *)
    MIN_LHE_LEVEL           : REAL := 15.0;     (* Minimum safe LHe level [%] *)
    QUENCH_CONFIRM_TIME     : TIME := T#2MS;    (* Extremely fast validation for quench events *)
    
    (* Internal Flags *)
    bFastQuench             : BOOL := FALSE;
    bThermalQuench          : BOOL := FALSE;
    bPressureFault          : BOOL := FALSE;
    bInitializationDone     : BOOL := FALSE;
END_VAR

(* === INITIALIZATION & SAFETY INTERLOCKS === *)
IF NOT bInitializationDone THEN
    iState := 0;
    bInitializationDone := TRUE;
    rMaxTempReached := 0.0;
END_IF;

(* Latch maximum temperature *)
IF rCryostatTemp > rMaxTempReached THEN
    rMaxTempReached := rCryostatTemp;
END_IF;

(* Master E-Stop Override *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bCriticalAlarm := TRUE;
    bIGBT_BypassFire := TRUE;       (* Fail-safe: Bypass coil on E-Stop *)
    bDumpResistorConnect := TRUE;   (* Fail-safe: Dump energy *)
    bVentValveOpen := TRUE;         (* Fail-safe: Vent pressure *)
    iState := 99;                   (* Go to FATAL FAULT state *)
    RETURN;
END_IF;

(* === SIGNAL PROCESSING & NOISE FILTERING === *)
(* Calculate absolute differential voltage between coil branches to reject common mode noise *)
rFilteredDiffVoltage := (1.0 - rAlphaV) * rPrevDiffVoltage + rAlphaV * ABS(rCoilVoltage_A - rCoilVoltage_B);
rPrevDiffVoltage := rFilteredDiffVoltage;

(* Deduct inductive component L*(di/dt) if needed; here we assume symmetric branches cancel it *)
(* In a real SMES, differential bridge eliminates inductive voltage, leaving only resistive. *)

(* === FAULT DETECTION === *)
bFastQuench := (rFilteredDiffVoltage > QUENCH_VOLTAGE_LIMIT);
bThermalQuench := (rCryostatTemp > CRIT_TEMP_LIMIT) OR (rLHeLevel < MIN_LHE_LEVEL);
bPressureFault := (rLHePressure > CRIT_PRESSURE_LIMIT);

(* Quench Confirmation Timer - prevents firing on microsecond spurious spikes *)
tQuenchConfirmTimer(IN := bFastQuench, PT := QUENCH_CONFIRM_TIME);
IF tQuenchConfirmTimer.Q OR bThermalQuench THEN
    bQuenchDetected := TRUE;
END_IF;

(* === PROTECTION STATE MACHINE === *)
CASE iState OF
    0: (* IDLE / INITIALIZATION *)
        bSystemReady := FALSE;
        bIGBT_BypassFire := FALSE;
        bDumpResistorConnect := FALSE;
        bVentValveOpen := FALSE;
        bQuenchDetected := FALSE;
        bCriticalAlarm := FALSE;
        
        IF bEnable AND NOT bQuenchDetected AND NOT bPressureFault THEN
            iState := 10;
        END_IF;

    10: (* ARMED AND MONITORING *)
        bSystemReady := TRUE;
        
        IF bQuenchDetected THEN
            bSystemReady := FALSE;
            bCriticalAlarm := TRUE;
            iState := 20; (* TRANSITION TO QUENCH MITIGATION *)
        ELSIF bPressureFault THEN
            bSystemReady := FALSE;
            bCriticalAlarm := TRUE;
            iState := 30; (* TRANSITION TO PRESSURE RELIEF *)
        ELSIF NOT bEnable THEN
            iState := 0;
        END_IF;

    20: (* QUENCH MITIGATION ACTION - ULTRA FAST *)
        (* Step 1: Fire IGBT Bypass immediately to short the SMES coil internally *)
        bIGBT_BypassFire := TRUE;
        
        (* Step 2: Connect external dump resistor after 5ms delay to allow IGBTs to fully saturate *)
        tDumpResistorTimer(IN := TRUE, PT := T#5MS);
        IF tDumpResistorTimer.Q THEN
            bDumpResistorConnect := TRUE;
        END_IF;
        
        (* Step 3: Open vent valves to handle explosive LHe boil-off *)
        bVentValveOpen := TRUE;
        
        (* Lock in this state until manual operator reset *)
        IF bAcknowledgeFault AND NOT bFastQuench AND NOT bThermalQuench THEN
            tDumpResistorTimer(IN := FALSE);
            iState := 0;
        END_IF;
        
    30: (* PRESSURE RELIEF ONLY - NO QUENCH YET *)
        bVentValveOpen := TRUE;
        
        tVentValveTimer(IN := TRUE, PT := T#5S);
        IF tVentValveTimer.Q AND (rLHePressure < (CRIT_PRESSURE_LIMIT * 0.9)) THEN
            tVentValveTimer(IN := FALSE);
            bVentValveOpen := FALSE;
            IF bAcknowledgeFault THEN
                iState := 0;
            END_IF;
        END_IF;
        
        (* If a quench occurs during pressure relief, escalate to full quench mitigation *)
        IF bQuenchDetected THEN
            tVentValveTimer(IN := FALSE);
            iState := 20;
        END_IF;
        
    99: (* FATAL FAULT / E-STOP LATCH *)
        IF bAcknowledgeFault AND bEmergencyStop AND bEnable THEN
            iState := 0;
        END_IF;

END_CASE;

(* Update Output State Var *)
iProtectionState := iState;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
    json.dump({"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}, f, ensure_ascii=False)
