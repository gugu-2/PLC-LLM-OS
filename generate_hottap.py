import os, json, uuid
os.makedirs('data/swarm_raw', exist_ok=True)
prompt = '''You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Autonomous Subsea Pipeline Hot-Tapping Machine**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Subsea 200-bar ambient hydraulic coupon cutter feed rate, pipeline wall thickness acoustic resonance sensing, and emergency pressure-balanced isolation seal deployment). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = """```iec-st\nFUNCTION_BLOCK FB_Subsea_HotTapping\n//...\nEND_FUNCTION_BLOCK\n```"""
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
6. REPLY with: EVOLUTION COMPLETE: Autonomous Subsea Pipeline Hot-Tapping Machine

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT.'''

code = '''```iec-st
FUNCTION_BLOCK FB_Subsea_HotTapping_Control
VAR_INPUT
    (* Subsea 200-bar environment and hot-tapping operational inputs *)
    bSystemEnable           : BOOL;     (* Master system enable for autonomous subsea operation *)
    bEmergencyAbort         : BOOL;     (* Safety-critical abort (SIL-3 hardware relay input) *)
    rAmbientPressure        : REAL;     (* Ambient hydrostatic pressure in Bar (nom. 200 Bar) *)
    rPipelinePressure       : REAL;     (* Internal pipeline fluid pressure in Bar *)
    rCutterRpmFeedback      : REAL;     (* Hydraulic cutter actual RPM feedback from encoder *)
    rAcousticThickness      : REAL;     (* Real-time pipeline wall thickness from acoustic sensor (mm) *)
    bSealDeployConfirm      : BOOL;     (* Proximity switch confirming emergency seal deployment *)
    rFeedForce              : REAL;     (* Hydraulic feed force acting on coupon cutter (kN) *)
END_VAR
VAR_OUTPUT
    (* Hot-tapping operational outputs and safety state *)
    bSystemReady            : BOOL;     (* Indicates system is self-checked and ready for autonomous cut *)
    rCutterSpeedCmd         : REAL;     (* Commanded RPM for the hydraulic cutter spindle *)
    rFeedRateCmd            : REAL;     (* Commanded feed rate for coupon penetration (mm/min) *)
    bDeployIsolationSeal    : BOOL;     (* Command to deploy pressure-balanced isolation seal *)
    bCriticalAlarm          : BOOL;     (* Indicates severe malfunction requiring ROV intervention *)
    iOperationState         : INT;      (* Current state of the hot-tapping finite state machine *)
END_VAR
VAR
    (* Internal State and Filtering Variables *)
    iState                  : INT := 0; (* Main FSM state variable *)
    tStartupDelay           : TON;      (* Initialization delay timer *)
    tCuttingPhaseTimer      : TON;      (* Max allowed duration for the cutting phase *)
    
    (* Signal Filtering *)
    rFilteredAcoustic       : REAL := 0.0;
    rFilteredFeedForce      : REAL := 0.0;
    rAlphaAcoustic          : REAL := 0.15; (* Low-pass filter constant for acoustic sensor *)
    rAlphaForce             : REAL := 0.10; (* Low-pass filter constant for feed force *)
    
    (* Process Parameters *)
    rTargetSpeed            : REAL := 120.0; (* Base target speed in RPM *)
    rBaseFeedRate           : REAL := 2.5;   (* Base feed rate in mm/min *)
    
    (* Safety thresholds *)
    rMaxDifferentialPress   : REAL := 50.0;  (* Max allowable differential pressure (Bar) *)
    rMaxFeedForce           : REAL := 15.0;  (* Max allowable feed force (kN) before jamming risk *)
END_VAR

(* === MAIN LOGIC === *)
(* 1. Safety Interlocks and Hardware Abort Processing *)
IF bEmergencyAbort THEN
    (* Immediate shutdown protocol: retraction and sealing *)
    bSystemReady := FALSE;
    rCutterSpeedCmd := 0.0;
    rFeedRateCmd := -10.0; (* Rapid retract *)
    bDeployIsolationSeal := TRUE;
    bCriticalAlarm := TRUE;
    iState := 999; (* Fault state *)
    iOperationState := iState;
    RETURN;
END_IF;

(* 2. Real-time Sensor Noise Filtering (EWMA Filter) *)
rFilteredAcoustic := (rAlphaAcoustic * rAcousticThickness) + ((1.0 - rAlphaAcoustic) * rFilteredAcoustic);
rFilteredFeedForce := (rAlphaForce * rFeedForce) + ((1.0 - rAlphaForce) * rFilteredFeedForce);

(* 3. Differential Pressure Monitoring *)
(* Absolute difference between pipeline interior and ambient subsea pressure must be managed *)
IF ABS(rPipelinePressure - rAmbientPressure) > rMaxDifferentialPress AND iState > 0 AND iState < 100 THEN
    (* Unsafe pressure differential detected, trigger abort *)
    bCriticalAlarm := TRUE;
    bDeployIsolationSeal := TRUE;
    rCutterSpeedCmd := 0.0;
    rFeedRateCmd := -5.0;
    iState := 999;
END_IF;

(* 4. Main Autonomous Hot-Tapping Finite State Machine *)
CASE iState OF
    0: (* IDLE & SELF-CHECK *)
        bSystemReady := FALSE;
        rCutterSpeedCmd := 0.0;
        rFeedRateCmd := 0.0;
        bDeployIsolationSeal := FALSE;
        bCriticalAlarm := FALSE;
        
        IF bSystemEnable AND (rAmbientPressure > 10.0) THEN
            (* Subsea environment confirmed, initiate pre-checks *)
            tStartupDelay(IN := TRUE, PT := T#10S);
            IF tStartupDelay.Q THEN
                tStartupDelay(IN := FALSE);
                bSystemReady := TRUE;
                iState := 10;
            END_IF;
        ELSE
            tStartupDelay(IN := FALSE);
        END_IF;

    10: (* APPROACH & CALIBRATE *)
        (* Slow advance until wall contact detected via force feedback *)
        rCutterSpeedCmd := 30.0; (* Low speed approach *)
        rFeedRateCmd := 1.5;     (* Slow feed *)
        
        IF rFilteredFeedForce > 2.0 THEN
            (* Contact established, calculate optimal cut parameters based on wall thickness *)
            iState := 20;
        END_IF;

    20: (* MAIN HOT-TAPPING CUT *)
        (* Dynamic feed rate and RPM adjustment based on acoustic resonance wall thickness measurement *)
        tCuttingPhaseTimer(IN := TRUE, PT := T#30M);
        
        (* Adjust speed based on remaining wall thickness *)
        IF rFilteredAcoustic > 5.0 THEN
            rCutterSpeedCmd := rTargetSpeed;
            rFeedRateCmd := rBaseFeedRate;
        ELSE
            (* Approaching breakthrough, reduce speed and feed to prevent coupon drop *)
            rCutterSpeedCmd := rTargetSpeed * 0.6;
            rFeedRateCmd := rBaseFeedRate * 0.4;
        END_IF;
        
        (* Force overload protection *)
        IF rFilteredFeedForce > rMaxFeedForce THEN
            (* Back off momentarily to clear chips/jamming *)
            rFeedRateCmd := -1.0;
        END_IF;
        
        (* Detect breakthrough *)
        IF rFilteredAcoustic <= 0.2 OR rFilteredFeedForce < 0.5 THEN
            (* Cut complete or near-complete *)
            tCuttingPhaseTimer(IN := FALSE);
            iState := 30;
        END_IF;
        
        (* Timeout watchdog *)
        IF tCuttingPhaseTimer.Q THEN
            bCriticalAlarm := TRUE;
            iState := 999;
        END_IF;

    30: (* RETRACT AND ISOLATE *)
        rCutterSpeedCmd := 0.0;
        rFeedRateCmd := -5.0; (* Retract cutter/coupon *)
        
        (* Wait for retraction to complete conceptually, then seal *)
        bDeployIsolationSeal := TRUE;
        
        IF bSealDeployConfirm THEN
            iState := 100;
        END_IF;

    100: (* OPERATION COMPLETE *)
        rFeedRateCmd := 0.0;
        bSystemReady := FALSE;
        IF NOT bSystemEnable THEN
            iState := 0;
        END_IF;
        
    999: (* FAULT HANDLING *)
        (* Remain in safe isolated state until ROV reset *)
        rCutterSpeedCmd := 0.0;
        rFeedRateCmd := 0.0;
        bDeployIsolationSeal := TRUE;
        IF NOT bSystemEnable AND NOT bEmergencyAbort THEN
            bCriticalAlarm := FALSE;
            iState := 0;
        END_IF;
        
END_CASE;

iOperationState := iState;

END_FUNCTION_BLOCK
```'''
record = {'messages': [{'role': 'user', 'content': prompt}, {'role': 'assistant', 'content': code}]}
filename = f'data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json'
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(record, f, ensure_ascii=False)
print(f'Saved to {filename}')
