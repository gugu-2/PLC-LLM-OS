import json, uuid
import os

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Advanced Semiconductor Pitch Multiplication (SADP/SAQP) Spacer Etch**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Conformal ALD spacer oxide thickness tracking, highly anisotropic directional reactive ion etch (RIE), and polymer residue descumming). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_SADP_SpacerEtch\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
   record = {\"messages\": [{\"role\": \"user\", \"content\": prompt}, {\"role\": \"assistant\", \"content\": code}]}
   with open(f\"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json\", \"w\", encoding=\"utf-8\") as f:
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
6. REPLY with: EVOLUTION COMPLETE: Advanced Semiconductor Pitch Multiplication (SADP/SAQP) Spacer Etch

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_SADP_SpacerEtch
VAR_INPUT
    bEnable                 : BOOL;     (* System enable signal for spacer etch sequence *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal; must be TRUE to operate *)
    rChamberPressure        : REAL;     (* Chamber pressure in mTorr, critical for RIE anisotropy *)
    rGasFlowCHF3            : REAL;     (* Flow rate of CHF3 in sccm for fluorocarbon polymer *)
    rGasFlowAr              : REAL;     (* Flow rate of Argon in sccm for ion bombardment *)
    rRFBiasPower            : REAL;     (* RF bias power in Watts controlling ion energy *)
    rWaferTemperature       : REAL;     (* Electrostatic chuck temperature in degrees C *)
    rFilmThicknessInitial   : REAL;     (* Initial spacer ALD oxide thickness in Angstroms *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;     (* System ready status, all interlocks satisfied *)
    bEtchComplete           : BOOL;     (* TRUE when main etch and over-etch are finished *)
    rControlRFPower         : REAL;     (* Setpoint command to the RF generator (Watts) *)
    rThrottleValvePos       : REAL;     (* Throttle valve position command (0-100%) *)
    bAlarm                  : BOOL;     (* Fault alarm output (e.g. pressure/temp out of bounds) *)
    iErrorCode              : INT;      (* 0 = No error, >0 = specific fault code *)
END_VAR
VAR
    iState                  : INT := 0; (* Internal state machine counter *)
    tStepTimer              : TON;      (* Step timer for process control *)
    tOverEtchTimer          : TON;      (* Timer specifically for the descum over-etch phase *)
    rEstimatedThickness     : REAL;     (* Real-time estimation of remaining spacer thickness (A) *)
    rEtchRateAperSec        : REAL := 15.5; (* Nominal oxide etch rate in Angstroms/second *)
    rPolymerDepRate         : REAL := 2.1;  (* Polymer deposition rate in Angstroms/second *)
END_VAR

(* === MAIN SAFETY & INTERLOCK LOGIC === *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bEtchComplete := FALSE;
    rControlRFPower := 0.0;
    rThrottleValvePos := 0.0;
    bAlarm := TRUE;
    iErrorCode := 999; (* Critical E-Stop *)
    iState := 0;
    RETURN;
END_IF;

(* Process variable boundary checking for ultra-precise SAQP constraints *)
IF bEnable AND iState > 0 THEN
    IF rChamberPressure < 10.0 OR rChamberPressure > 50.0 THEN
        bAlarm := TRUE;
        iErrorCode := 101; (* Pressure deviation limits anisotropic profile *)
        iState := 99; (* Transition to safe abort *)
    END_IF;
    
    IF rWaferTemperature < 15.0 OR rWaferTemperature > 60.0 THEN
        bAlarm := TRUE;
        iErrorCode := 102; (* Temperature limits exceeded, risk of polymer burning *)
        iState := 99;
    END_IF;
END_IF;

CASE iState OF
    0: (* IDLE & INITIALIZATION *)
        bSystemReady := TRUE;
        bEtchComplete := FALSE;
        bAlarm := FALSE;
        iErrorCode := 0;
        rControlRFPower := 0.0;
        rThrottleValvePos := 10.0; (* Idle pumping *)
        rEstimatedThickness := rFilmThicknessInitial;
        
        IF bEnable THEN
            bSystemReady := FALSE;
            iState := 10;
        END_IF;

    10: (* GAS STABILIZATION *)
        (* Target 25 mTorr for optimal directional RIE *)
        rThrottleValvePos := 25.0 + (rGasFlowCHF3 + rGasFlowAr) * 0.05;
        
        tStepTimer(IN := TRUE, PT := T#15S);
        IF tStepTimer.Q THEN
            tStepTimer(IN := FALSE);
            iState := 20;
        END_IF;

    20: (* MAIN HIGH-ANISOTROPY ETCH *)
        (* Ramp RF Bias Power to drive Argon ions vertically *)
        IF rRFBiasPower < 400.0 THEN
            rControlRFPower := 450.0; (* Setpoint overshoot to reach fast *)
        ELSE
            rControlRFPower := 400.0;
        END_IF;
        
        (* Integrate Etch Rate (simple discrete approximation for demonstration) *)
        rEstimatedThickness := rEstimatedThickness - (rEtchRateAperSec - rPolymerDepRate) * 0.1; (* assuming 100ms cycle *)
        
        IF rEstimatedThickness <= 20.0 THEN (* Leave 20 Angstroms for soft over-etch *)
            rControlRFPower := 0.0;
            iState := 30;
        END_IF;

    30: (* POLYMER DESCUM / OVER-ETCH *)
        rControlRFPower := 150.0; (* Low bias to avoid damaging underlying silicon/mandrel *)
        rThrottleValvePos := 40.0; (* Increase pressure to favor chemical descum over physical sputtering *)
        
        tOverEtchTimer(IN := TRUE, PT := T#8S);
        IF tOverEtchTimer.Q THEN
            tOverEtchTimer(IN := FALSE);
            rControlRFPower := 0.0;
            iState := 40;
        END_IF;

    40: (* PUMP DOWN & COMPLETE *)
        rThrottleValvePos := 100.0; (* Fully open throttle valve to evacuate chamber *)
        tStepTimer(IN := TRUE, PT := T#10S);
        
        IF tStepTimer.Q THEN
            tStepTimer(IN := FALSE);
            bEtchComplete := TRUE;
            iState := 50;
        END_IF;

    50: (* WAITING FOR DISABLE *)
        IF NOT bEnable THEN
            iState := 0;
        END_IF;

    99: (* FAULT HANDLING *)
        rControlRFPower := 0.0;
        rThrottleValvePos := 100.0;
        bSystemReady := FALSE;
        IF NOT bEnable THEN (* Reset on disable *)
            iState := 0;
            bAlarm := FALSE;
            iErrorCode := 0;
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}

filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
