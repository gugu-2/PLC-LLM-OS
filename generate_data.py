import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Semiconductor Deep Reactive-Ion Etching (DRIE) Bosch Process Chamber**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., ultra-fast SF6/C4F8 gas switching cycles, inductively coupled plasma (ICP) RF matching network, and wafer backside helium cooling pressure regulation). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_DRIE_Chamber\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Semiconductor Deep Reactive-Ion Etching (DRIE) Bosch Process Chamber

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_DRIE_Bosch_Process_Chamber
(* 
   =============================================================================
   Block Name    : FB_DRIE_Bosch_Process_Chamber
   Description   : Advanced Deep Reactive-Ion Etching (DRIE) Control Block
                   Executes the Bosch process with ultra-fast gas switching
                   (SF6 for etching, C4F8 for passivation), manages the ICP RF 
                   matching network, and regulates wafer backside helium cooling
                   pressure to strictly maintain wafer temperature.
   =============================================================================
*)
VAR_INPUT
    bEnableProc     : BOOL;  (* System enable signal for the DRIE process *)
    bEmergencyStop  : BOOL;  (* Safety interlock / Emergency Stop signal (Active HIGH OK) *)
    rChamberPress   : REAL;  (* Chamber pressure measurement (mTorr) *)
    rHeBacksidePress: REAL;  (* Wafer backside Helium cooling pressure (Torr) *)
    rICPFwdPower    : REAL;  (* Inductively Coupled Plasma Forward Power (Watts) *)
    rICPRflPower    : REAL;  (* Inductively Coupled Plasma Reflected Power (Watts) *)
    bRecipeLoaded   : BOOL;  (* True if a valid Bosch process recipe is loaded *)
END_VAR

VAR_OUTPUT
    bSystemReady    : BOOL;  (* System ready status / No active faults *)
    bProcRunning    : BOOL;  (* Process is actively running *)
    rSF6_ValveCmd   : REAL;  (* Control signal for SF6 MFC (0-100%) *)
    rC4F8_ValveCmd  : REAL;  (* Control signal for C4F8 MFC (0-100%) *)
    rICP_PowerCmd   : REAL;  (* Commanded ICP generator output power (Watts) *)
    bAlarm          : BOOL;  (* Fault alarm output *)
    iErrorCode      : INT;   (* Specific error code if an alarm is triggered *)
END_VAR

VAR
    iState          : INT := 0;      (* Internal state machine step *)
    iCycleCount     : INT := 0;      (* Counter for total etched cycles *)
    tEtchTimer      : TON;           (* Timer for SF6 etching phase *)
    tPassTimer      : TON;           (* Timer for C4F8 passivation phase *)
    tPurgeTimer     : TON;           (* Timer for intermediate purge step *)
    
    (* Process Parameters (could be linked to recipe) *)
    rTargetHePress  : REAL := 10.0;  (* Target He pressure in Torr *)
    rMaxReflectedPwr: REAL := 50.0;  (* Maximum allowed reflected power (Watts) *)
    iMaxCycles      : INT := 1000;   (* Target number of Bosch cycles to execute *)
END_VAR

(* === MAIN LOGIC === *)

(* Safety and Interlock Check *)
IF NOT bEmergencyStop THEN
    bSystemReady   := FALSE;
    bProcRunning   := FALSE;
    rSF6_ValveCmd  := 0.0;
    rC4F8_ValveCmd := 0.0;
    rICP_PowerCmd  := 0.0;
    bAlarm         := TRUE;
    iErrorCode     := 999; (* 999: E-Stop triggered *)
    iState         := 0;
    RETURN;
END_IF;

(* Continuous Monitoring *)
IF rICPRflPower > rMaxReflectedPwr THEN
    bAlarm := TRUE;
    iErrorCode := 101; (* 101: RF Match Fault *)
    iState := 99;      (* Move to fault state *)
END_IF;

IF (rHeBacksidePress < rTargetHePress * 0.8) OR (rHeBacksidePress > rTargetHePress * 1.2) THEN
    (* Minor He pressure deviation can trigger a warning, major deviation a fault *)
    bAlarm := TRUE;
    iErrorCode := 102; (* 102: He cooling pressure out of bounds *)
END_IF;

(* Bosch Process State Machine *)
CASE iState OF
    0: (* IDLE - Wait for recipe and enable *)
        bSystemReady := TRUE;
        bProcRunning := FALSE;
        rSF6_ValveCmd := 0.0;
        rC4F8_ValveCmd := 0.0;
        rICP_PowerCmd := 0.0;
        
        IF bEnableProc AND bRecipeLoaded AND NOT bAlarm THEN
            iState := 10; (* Start process *)
            iCycleCount := 0;
        END_IF;

    10: (* IGNITE PLASMA & STABILIZE *)
        bProcRunning := TRUE;
        rICP_PowerCmd := 1500.0; (* Pre-strike power *)
        
        (* Wait for chamber pressure and RF forward power to reach thresholds *)
        IF (rChamberPress > 15.0) AND (rICPFwdPower > 1400.0) THEN
            iState := 20; (* Enter Etch Phase *)
        END_IF;

    20: (* ETCH PHASE (SF6 ON, C4F8 OFF) *)
        rSF6_ValveCmd := 100.0;
        rC4F8_ValveCmd := 0.0;
        
        tEtchTimer(IN := TRUE, PT := T#2S); (* 2-second ultra-fast etch step *)
        IF tEtchTimer.Q THEN
            tEtchTimer(IN := FALSE);
            iState := 30;
        END_IF;

    30: (* PASSIVATION PHASE (C4F8 ON, SF6 OFF) *)
        rSF6_ValveCmd := 0.0;
        rC4F8_ValveCmd := 100.0;
        
        tPassTimer(IN := TRUE, PT := T#1S); (* 1-second ultra-fast passivation step *)
        IF tPassTimer.Q THEN
            tPassTimer(IN := FALSE);
            iCycleCount := iCycleCount + 1;
            
            IF iCycleCount >= iMaxCycles THEN
                iState := 40; (* Process complete *)
            ELSE
                iState := 20; (* Next cycle *)
            END_IF;
        END_IF;

    40: (* COMPLETE / PURGE *)
        rSF6_ValveCmd := 0.0;
        rC4F8_ValveCmd := 0.0;
        rICP_PowerCmd := 0.0;
        
        tPurgeTimer(IN := TRUE, PT := T#10S);
        IF tPurgeTimer.Q THEN
            tPurgeTimer(IN := FALSE);
            bProcRunning := FALSE;
            
            IF NOT bEnableProc THEN
                iState := 0; (* Reset to IDLE *)
            END_IF;
        END_IF;

    99: (* FAULT HANDLING *)
        rSF6_ValveCmd := 0.0;
        rC4F8_ValveCmd := 0.0;
        rICP_PowerCmd := 0.0;
        bProcRunning := FALSE;
        bSystemReady := FALSE;
        
        IF NOT bEnableProc THEN
            (* Wait for operator to clear enable before attempting reset *)
            bAlarm := FALSE;
            iErrorCode := 0;
            iState := 0;
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump({"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}, f, ensure_ascii=False)
print(f"Saved to {filename}")
