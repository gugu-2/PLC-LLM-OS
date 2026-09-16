import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Automated Laser Powder Bed Fusion (L-PBF) 3D Printer**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Dual-laser galvanometer synchronization, argon shield gas laminar flow mapping, and melt-pool pyrometry feed-forward adjustment). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_LPBF_3DPrinter\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Automated Laser Powder Bed Fusion (L-PBF) 3D Printer

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_Advanced_LPBF_Control
VAR_INPUT
    bEnable                 : BOOL;     (* System master enable *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal - inverted logic *)
    rArgonFlowRate          : REAL;     (* Measured argon shield gas flow in L/min *)
    rMeltPoolTemp1          : REAL;     (* Pyrometer 1 reading in deg C *)
    rMeltPoolTemp2          : REAL;     (* Pyrometer 2 reading in deg C *)
    rLaser1Pos_X            : REAL;     (* Galvo 1 X position feedback *)
    rLaser1Pos_Y            : REAL;     (* Galvo 1 Y position feedback *)
    rLaser2Pos_X            : REAL;     (* Galvo 2 X position feedback *)
    rLaser2Pos_Y            : REAL;     (* Galvo 2 Y position feedback *)
    rBuildPlateTemp         : REAL;     (* Build plate thermocouple reading *)
    rChamberOxygen          : REAL;     (* Chamber oxygen level in ppm *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;     (* L-PBF System ready status *)
    rLaser1PowerCmd         : REAL;     (* Laser 1 power output command (W) *)
    rLaser2PowerCmd         : REAL;     (* Laser 2 power output command (W) *)
    rArgonValveCmd          : REAL;     (* Argon flow control valve position (0-100%) *)
    bLaserInterlockOk       : BOOL;     (* Hardware interlock release for lasers *)
    bAlarm                  : BOOL;     (* Global fault alarm output *)
    iErrorCode              : INT;      (* Diagnostics error code *)
END_VAR
VAR
    iState                  : INT := 0; (* Main state machine state *)
    tStateTimer             : TON;
    tFilterTimer            : TON;
    rFilteredPoolTemp1      : REAL;
    rFilteredPoolTemp2      : REAL;
    rOxygenSp               : REAL := 500.0; (* Max allowable oxygen ppm *)
    rArgonNominal           : REAL := 15.0;  (* Nominal flow L/min *)
    rKp_Laser               : REAL := 0.25;  (* P-gain for melt pool temp *)
    rMeltPoolSp             : REAL := 1650.0; (* Target melt pool temp deg C *)
    
    (* Filter variables *)
    rAlpha                  : REAL := 0.1; (* Low pass filter coefficient *)
END_VAR

(* === MAIN LOGIC === *)
(* 1. Safety and Interlocks *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bLaserInterlockOk := FALSE;
    rLaser1PowerCmd := 0.0;
    rLaser2PowerCmd := 0.0;
    rArgonValveCmd := 0.0;
    bAlarm := TRUE;
    iErrorCode := 9999; (* E-STOP Active *)
    iState := 0;
    RETURN;
END_IF;

(* 2. Signal Filtering (First-Order Low Pass) *)
rFilteredPoolTemp1 := rFilteredPoolTemp1 + rAlpha * (rMeltPoolTemp1 - rFilteredPoolTemp1);
rFilteredPoolTemp2 := rFilteredPoolTemp2 + rAlpha * (rMeltPoolTemp2 - rFilteredPoolTemp2);

(* 3. Main State Machine *)
CASE iState OF
    0: (* IDLE / INITIALIZATION *)
        bSystemReady := FALSE;
        bLaserInterlockOk := FALSE;
        rLaser1PowerCmd := 0.0;
        rLaser2PowerCmd := 0.0;
        bAlarm := FALSE;
        iErrorCode := 0;
        
        IF bEnable THEN
            iState := 10; (* Move to Purge *)
        END_IF;

    10: (* PURGE CHAMBER *)
        rArgonValveCmd := 100.0; (* Full open for purge *)
        
        IF rChamberOxygen < rOxygenSp THEN
            tStateTimer(IN := TRUE, PT := T#10S);
            IF tStateTimer.Q THEN
                tStateTimer(IN := FALSE);
                iState := 20; (* Move to Preheat *)
            END_IF;
        ELSE
            tStateTimer(IN := FALSE);
        END_IF;

    20: (* PREHEAT BUILD PLATE *)
        rArgonValveCmd := 50.0; (* Regulate to nominal *)
        IF rBuildPlateTemp >= 200.0 THEN
            iState := 30; (* Ready for processing *)
        END_IF;

    30: (* SYSTEM READY / PROCESSING *)
        bSystemReady := TRUE;
        bLaserInterlockOk := TRUE;
        
        (* Argon Flow Control - Simple Proportional *)
        rArgonValveCmd := 50.0 + (rArgonNominal - rArgonFlowRate) * 5.0;
        
        (* Limit Argon Valve *)
        IF rArgonValveCmd > 100.0 THEN rArgonValveCmd := 100.0; END_IF;
        IF rArgonValveCmd < 0.0 THEN rArgonValveCmd := 0.0; END_IF;

        (* Feed-forward melt pool temperature control *)
        (* Adjust laser power dynamically based on pyrometer feedback *)
        rLaser1PowerCmd := 400.0 + (rMeltPoolSp - rFilteredPoolTemp1) * rKp_Laser;
        rLaser2PowerCmd := 400.0 + (rMeltPoolSp - rFilteredPoolTemp2) * rKp_Laser;
        
        (* Clamp Laser Power Command *)
        IF rLaser1PowerCmd > 1000.0 THEN rLaser1PowerCmd := 1000.0; END_IF;
        IF rLaser1PowerCmd < 0.0 THEN rLaser1PowerCmd := 0.0; END_IF;
        IF rLaser2PowerCmd > 1000.0 THEN rLaser2PowerCmd := 1000.0; END_IF;
        IF rLaser2PowerCmd < 0.0 THEN rLaser2PowerCmd := 0.0; END_IF;

        (* Fault Detection *)
        IF rChamberOxygen > (rOxygenSp + 100.0) THEN
            iErrorCode := 101; (* Oxygen Level High Warning *)
            bAlarm := TRUE;
        END_IF;
        
        IF NOT bEnable THEN
            iState := 0;
            tStateTimer(IN := FALSE);
        END_IF;
        
    ELSE
        (* Invalid state trap *)
        iState := 0;
        iErrorCode := 500;
        bAlarm := TRUE;
END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs('data/swarm_raw', exist_ok=True)
record = {'messages': [{'role': 'user', 'content': prompt}, {'role': 'assistant', 'content': code}]}
filename = f'data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json'
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(record, f, ensure_ascii=False)
print(f'Saved to {filename}')
