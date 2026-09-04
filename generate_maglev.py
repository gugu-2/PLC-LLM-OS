import json, uuid, os
prompt = '''You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: High-Speed Maglev Superconducting Magnet Cooling System**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Liquid helium/nitrogen cryogenic cascade, quench detection ultra-fast fault logic, and redundant compressor active load balancing). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   prompt = """<copy this exact user prompt here>"""
   code = """```iec-st\nFUNCTION_BLOCK FB_MaglevCryoCooling\n//...\nEND_FUNCTION_BLOCK\n```"""
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
6. REPLY with: EVOLUTION COMPLETE: High-Speed Maglev Superconducting Magnet Cooling System

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT.'''

code = '''```iec-st
FUNCTION_BLOCK FB_MaglevCryoCooling
VAR_INPUT
    (* Physical Inputs for Superconducting Magnet Cooling System *)
    bSystemEnable           : BOOL;     (* System master enable signal *)
    bQuenchDetect           : BOOL;     (* Superconducting quench detection relay OK (Active High) *)
    rHeLevel                : REAL;     (* Liquid Helium vessel level (0.0 to 100.0 %) *)
    rN2Level                : REAL;     (* Liquid Nitrogen thermal shield vessel level (0.0 to 100.0 %) *)
    rHeTemp1                : REAL;     (* Helium stage 1 temp (Kelvin) *)
    rHeTemp2                : REAL;     (* Helium stage 2 temp (Kelvin) *)
    rCompPressure           : REAL;     (* Compressor discharge pressure (Bar) *)
    bFlowSensorOK           : BOOL;     (* Helium flow verification *)
END_VAR
VAR_OUTPUT
    (* Physical Outputs for Actuators and Status *)
    bSystemReady            : BOOL;     (* Cryo system is ready and stable for maglev operation *)
    rHeValveCmd             : REAL;     (* LHe flow control valve command (0.0 to 100.0 %) *)
    rN2ValveCmd             : REAL;     (* LN2 thermal shield valve command (0.0 to 100.0 %) *)
    bCompRunCmd             : BOOL;     (* Compressor run command *)
    bQuenchDumpVlv          : BOOL;     (* Quench emergency vent dump valve (Active High = dump) *)
    bCriticalAlarm          : BOOL;     (* Critical fault alarm output *)
    iOperatingState         : INT;      (* Current state of the cooling machine *)
END_VAR
VAR
    (* Internal state and timers *)
    iState                  : INT := 0;
    tStartupDelay           : TON;
    tStabilityTimer         : TON;
    tQuenchLatch            : TOF;
    rIntegralErrorHe        : REAL := 0.0;
    rIntegralErrorN2        : REAL := 0.0;
    rKp_He                  : REAL := 2.5;
    rKi_He                  : REAL := 0.05;
    rKp_N2                  : REAL := 1.8;
    rKi_N2                  : REAL := 0.02;
    rHeSetpoint             : REAL := 85.0; (* 85% fill level *)
    rN2Setpoint             : REAL := 80.0; (* 80% fill level *)
    rErrorHe                : REAL;
    rErrorN2                : REAL;
    bFirstCycle             : BOOL := TRUE;
END_VAR

(* === MAIN LOGIC === *)

(* Initialize / Reset logic *)
IF bFirstCycle THEN
    iState := 0;
    bFirstCycle := FALSE;
END_IF;

(* Ultra-fast Quench Fault Protection (Hard Interlock) *)
IF NOT bQuenchDetect THEN
    (* Immediate dump, stop compressor, drop ready signal *)
    bSystemReady := FALSE;
    bQuenchDumpVlv := TRUE; 
    bCompRunCmd := FALSE;
    rHeValveCmd := 0.0;
    rN2ValveCmd := 0.0;
    bCriticalAlarm := TRUE;
    iState := 999; (* Quench State *)
    RETURN;
ELSE
    bQuenchDumpVlv := FALSE;
END_IF;

(* Master Enable Interlock *)
IF NOT bSystemEnable AND iState <> 999 THEN
    iState := 0;
END_IF;

(* State Machine for Cooling Cascade *)
CASE iState OF
    0: (* IDLE *)
        bSystemReady := FALSE;
        bCompRunCmd := FALSE;
        rHeValveCmd := 0.0;
        rN2ValveCmd := 0.0;
        bCriticalAlarm := FALSE;
        rIntegralErrorHe := 0.0;
        rIntegralErrorN2 := 0.0;
        iOperatingState := 0;
        
        IF bSystemEnable THEN
            iState := 10;
        END_IF;

    10: (* COMPRESSOR START *)
        bCompRunCmd := TRUE;
        iOperatingState := 10;
        
        tStartupDelay(IN := TRUE, PT := T#15S);
        IF tStartupDelay.Q THEN
            tStartupDelay(IN := FALSE);
            (* Verify pressure before moving to next stage *)
            IF rCompPressure > 12.0 THEN
                iState := 20;
            ELSE
                bCriticalAlarm := TRUE;
                iState := 0;
            END_IF;
        END_IF;

    20: (* LN2 SHIELD PRE-COOLING *)
        iOperatingState := 20;
        
        (* PI Control for N2 Level *)
        rErrorN2 := rN2Setpoint - rN2Level;
        rIntegralErrorN2 := rIntegralErrorN2 + (rErrorN2 * 0.1); 
        rN2ValveCmd := (rKp_N2 * rErrorN2) + (rKi_N2 * rIntegralErrorN2);
        
        (* Limit valve output *)
        IF rN2ValveCmd > 100.0 THEN rN2ValveCmd := 100.0; END_IF;
        IF rN2ValveCmd < 0.0 THEN rN2ValveCmd := 0.0; END_IF;
        
        IF rN2Level > 75.0 THEN
            iState := 30;
        END_IF;

    30: (* LHe PRIMARY COOLING *)
        iOperatingState := 30;
        
        (* PI Control for N2 Level - ongoing *)
        rErrorN2 := rN2Setpoint - rN2Level;
        rIntegralErrorN2 := rIntegralErrorN2 + (rErrorN2 * 0.1); 
        rN2ValveCmd := (rKp_N2 * rErrorN2) + (rKi_N2 * rIntegralErrorN2);
        IF rN2ValveCmd > 100.0 THEN rN2ValveCmd := 100.0; END_IF;
        IF rN2ValveCmd < 0.0 THEN rN2ValveCmd := 0.0; END_IF;
        
        (* PI Control for He Level *)
        rErrorHe := rHeSetpoint - rHeLevel;
        rIntegralErrorHe := rIntegralErrorHe + (rErrorHe * 0.1);
        rHeValveCmd := (rKp_He * rErrorHe) + (rKi_He * rIntegralErrorHe);
        IF rHeValveCmd > 100.0 THEN rHeValveCmd := 100.0; END_IF;
        IF rHeValveCmd < 0.0 THEN rHeValveCmd := 0.0; END_IF;
        
        (* Check stability conditions: Temp and Flow *)
        IF (rHeLevel >= 80.0) AND (rHeTemp1 < 4.5) AND bFlowSensorOK THEN
            tStabilityTimer(IN := TRUE, PT := T#30S);
            IF tStabilityTimer.Q THEN
                iState := 40;
            END_IF;
        ELSE
            tStabilityTimer(IN := FALSE);
        END_IF;

    40: (* SYSTEM READY - MAGLEV STABLE *)
        iOperatingState := 40;
        bSystemReady := TRUE;
        
        (* Continual PI Control for He and N2 *)
        rErrorN2 := rN2Setpoint - rN2Level;
        rIntegralErrorN2 := rIntegralErrorN2 + (rErrorN2 * 0.1); 
        rN2ValveCmd := (rKp_N2 * rErrorN2) + (rKi_N2 * rIntegralErrorN2);
        IF rN2ValveCmd > 100.0 THEN rN2ValveCmd := 100.0; END_IF;
        IF rN2ValveCmd < 0.0 THEN rN2ValveCmd := 0.0; END_IF;
        
        rErrorHe := rHeSetpoint - rHeLevel;
        rIntegralErrorHe := rIntegralErrorHe + (rErrorHe * 0.1);
        rHeValveCmd := (rKp_He * rErrorHe) + (rKi_He * rIntegralErrorHe);
        IF rHeValveCmd > 100.0 THEN rHeValveCmd := 100.0; END_IF;
        IF rHeValveCmd < 0.0 THEN rHeValveCmd := 0.0; END_IF;
        
        (* Drop ready if parameters drift *)
        IF rHeTemp1 > 5.0 OR rHeLevel < 70.0 OR NOT bFlowSensorOK THEN
            bSystemReady := FALSE;
            iState := 30;
        END_IF;
        
    999: (* QUENCH RECOVERY / LOCKOUT *)
        iOperatingState := 999;
        bSystemReady := FALSE;
        bCriticalAlarm := TRUE;
        bCompRunCmd := FALSE;
        rHeValveCmd := 0.0;
        rN2ValveCmd := 0.0;
        
        (* Require manual reset by dropping SystemEnable *)
        IF NOT bSystemEnable THEN
            iState := 0;
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
```'''

os.makedirs('data/swarm_raw', exist_ok=True)
record = {'messages': [{'role': 'user', 'content': prompt}, {'role': 'assistant', 'content': code}]}
filename = f'data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json'
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(record, f, ensure_ascii=False)
print(f'Saved to {filename}')
