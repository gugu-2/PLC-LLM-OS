import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Mega-Scale Desalination Reverse Osmosis Energy Recovery Device (ERD)**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., high-pressure pump active power matching, isobaric chamber pressure exchange synchronization, permeate total dissolved solids (TDS) feed-forward adjustment, and automated CIP backwash sequencing). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_DesalinationERD\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Mega-Scale Desalination Reverse Osmosis Energy Recovery Device

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_Desal_Isobaric_ERD_Control
VAR_INPUT
    (* System Operation Interlocks *)
    bEnable              : BOOL;     (* System master sequence enable command *)
    bEmergencyStop       : BOOL;     (* Safety relay OK status, MUST be TRUE to run *)
    bCIP_Active          : BOOL;     (* Clean-in-Place sequence active override *)
    
    (* Process Variable Measurements *)
    rHighPressureFlow    : REAL;     (* HP pump feed flow rate (m3/h) *)
    rBrineRejectPress    : REAL;     (* Brine reject pressure from RO membranes (bar) *)
    rPermeateTDS         : REAL;     (* Permeate total dissolved solids quality (ppm) *)
    rIsobaricPos_Ch1     : REAL;     (* Isobaric chamber 1 piston position (0.0-100.0%) *)
    rIsobaricPos_Ch2     : REAL;     (* Isobaric chamber 2 piston position (0.0-100.0%) *)
END_VAR
VAR_OUTPUT
    (* System Status Flags *)
    bSystemReady         : BOOL;     (* ERD synchronization achieved, process ready *)
    bCriticalAlarm       : BOOL;     (* ERD critical process or hardware fault alarm *)
    bSalinityWarning     : BOOL;     (* High permeate TDS warning feed-forward active *)
    
    (* Control Outputs *)
    rBoosterPumpSpeed    : REAL;     (* VFD speed reference for ERD booster pump (%) *)
    bValveSeqTrigger_Ch1 : BOOL;     (* Trigger sequence for HP/LP valves on Chamber 1 *)
    bValveSeqTrigger_Ch2 : BOOL;     (* Trigger sequence for HP/LP valves on Chamber 2 *)
END_VAR
VAR
    (* Internal State & Timers *)
    iState               : INT := 0; (* ERD Internal state machine (0=IDLE, 10=PRECHARGE, 20=SYNC, 99=FAULT) *)
    tSyncTimer           : TON;      (* Hydraulic synchronization integration timer *)
    tValveDwell          : TON;      (* Valve switching dwell time to prevent water hammer *)
    
    (* Mathematical & Control Variables *)
    rFeedForwardOffset   : REAL := 0.0; (* Calculated TDS compensation offset *)
    rFlowDifferential    : REAL := 0.0; (* Volumetric tracking delta for pump matching *)
    bSyncActive          : BOOL := FALSE;
END_VAR

(* === MAIN LOGIC === *)

(* 1. Safety & Override Interlock Evaluation *)
IF NOT bEmergencyStop THEN
    iState := 99; (* Transition immediately to critical fault state on E-Stop *)
END_IF;

IF bCIP_Active AND (iState <> 99) THEN
    (* CIP Override - Force Safe Standby for chemical wash *)
    iState := 0;
    bSystemReady := FALSE;
    rBoosterPumpSpeed := 0.0;
    bValveSeqTrigger_Ch1 := FALSE;
    bValveSeqTrigger_Ch2 := FALSE;
    RETURN; (* Halt further execution during CIP *)
END_IF;

(* 2. Feed-forward TDS Compensation Calculation *)
(* Adjusts booster pump effort to maintain recovery ratio against rising salinity/osmotic pressure *)
IF rPermeateTDS > 350.0 THEN
    bSalinityWarning := TRUE;
    rFeedForwardOffset := (rPermeateTDS - 350.0) * 0.015;
    IF rFeedForwardOffset > 5.0 THEN
        rFeedForwardOffset := 5.0; (* Cap maximum feed-forward compensation *)
    END_IF;
ELSE
    bSalinityWarning := FALSE;
    rFeedForwardOffset := 0.0;
END_IF;

(* 3. Core ERD Synchronization State Machine *)
CASE iState OF
    0: (* IDLE STATE - Zero Energy Wait *)
        bSystemReady := FALSE;
        bValveSeqTrigger_Ch1 := FALSE;
        bValveSeqTrigger_Ch2 := FALSE;
        rBoosterPumpSpeed := 0.0;
        bCriticalAlarm := FALSE;
        bSyncActive := FALSE;
        tSyncTimer(IN := FALSE);

        IF bEnable AND bEmergencyStop THEN
            iState := 10; (* Transition to Precharge Phase *)
        END_IF;

    10: (* PRECHARGE & HYDRAULIC EQUILIBRATION *)
        (* Initiate low speed boost to equalize membrane pressures safely *)
        rBoosterPumpSpeed := 15.0; (* 15% minimum VFD safe speed to build head *)
        tSyncTimer(IN := TRUE, PT := T#10S);
        
        IF tSyncTimer.Q AND (rBrineRejectPress > 20.0) THEN
            tSyncTimer(IN := FALSE);
            iState := 20; (* Transition to Active Synchronization *)
        ELSIF tSyncTimer.Q AND (rBrineRejectPress <= 20.0) THEN
            (* Failed to build required pre-charge pressure in allotted time *)
            iState := 99; 
        END_IF;

    20: (* ISOBARIC SYNCHRONIZATION & ACTIVE POWER MATCHING *)
        bSyncActive := TRUE;
        
        (* Track Piston Position to command alternating isobaric chamber valves *)
        (* Ensure non-overlapping actuation to mitigate severe water hammer *)
        IF rIsobaricPos_Ch1 >= 95.0 AND rIsobaricPos_Ch2 <= 5.0 THEN
            bValveSeqTrigger_Ch1 := TRUE;
            bValveSeqTrigger_Ch2 := FALSE;
        ELSIF rIsobaricPos_Ch2 >= 95.0 AND rIsobaricPos_Ch1 <= 5.0 THEN
            bValveSeqTrigger_Ch1 := FALSE;
            bValveSeqTrigger_Ch2 := TRUE;
        END_IF;

        (* Base speed calculation based on High Pressure flow and differential *)
        (* Assumes 98% volumetric efficiency across the energy recovery turbine/pistons *)
        rFlowDifferential := rHighPressureFlow * 0.98;
        rBoosterPumpSpeed := (rFlowDifferential / 1000.0) * 80.0 + rFeedForwardOffset;
        
        (* Absolute constraint clamping on VFD Speed to prevent mechanical damage *)
        IF rBoosterPumpSpeed > 100.0 THEN
            rBoosterPumpSpeed := 100.0;
        ELSIF rBoosterPumpSpeed < 20.0 THEN
            rBoosterPumpSpeed := 20.0;
        END_IF;

        bSystemReady := TRUE; (* Synchronization fully achieved *)

        IF NOT bEnable THEN
            iState := 0; (* Graceful stop requested *)
        END_IF;

    99: (* FAULT HANDLING & LOCKOUT *)
        bSystemReady := FALSE;
        bCriticalAlarm := TRUE;
        bValveSeqTrigger_Ch1 := FALSE;
        bValveSeqTrigger_Ch2 := FALSE;
        rBoosterPumpSpeed := 0.0;
        bSyncActive := FALSE;
        tSyncTimer(IN := FALSE);

        (* Latch fault until reset manually by dropping the Enable signal *)
        IF NOT bEnable AND bEmergencyStop THEN
            iState := 0;
        END_IF;

END_CASE;

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
