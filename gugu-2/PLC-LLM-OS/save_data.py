import json, uuid, os

prompt = """<USER_REQUEST>
You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Automated Commercial Logistics Hub Palletizing Gantry Robot and Stretch Wrapper Interlock**

Task: Invent a highly complex, ultra-realistic control scenario for this domain. Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_Palletizer_StretchWrap\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Automated Commercial Logistics Hub Palletizing Gantry Robot and Stretch Wrapper Interlock

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT.
</USER_REQUEST>"""

code = """```iec-st
FUNCTION_BLOCK FB_GantryPalletizerWrapperInterlock
(* 
   Elite Industrial Standard IEC 61131-3 Implementation
   Domain: Automated Commercial Logistics Hub Palletizing Gantry Robot and Stretch Wrapper Interlock
   Author: Lumina AI Cloud Swarm
   Description: Advanced coordination between high-speed gantry robot palletizing system 
                and automated stretch wrapper, featuring deterministic handshake, 
                collision avoidance zones, safety relay integrations, and recovery mechanisms.
*)
VAR_INPUT
    bSystemEnable            : BOOL;     (* Main system enable command from SCADA/HMI *)
    bEStopSafetyRelayOK      : BOOL;     (* Dual-channel safety relay OK signal for Zone 1 & 2 *)
    bGantryHomePosition      : BOOL;     (* TRUE if gantry robot is confirmed at physical home *)
    bWrapperHomePosition     : BOOL;     (* TRUE if stretch wrapper carriage is at bottom home *)
    bPalletFullSignal        : BOOL;     (* Triggered by gantry logic when palletizing sequence is complete *)
    bPalletDischargeClear    : BOOL;     (* Downstream conveyor clear signal via PE photo-eye *)
    rWrapperFilmTensionAct   : REAL;     (* Actual film tension feedback from wrapper load cell (kg) *)
    rWrapperFilmTensionSP    : REAL;     (* Film tension setpoint from recipe (kg) *)
END_VAR

VAR_OUTPUT
    bGantryPermissive        : BOOL;     (* Permissive signal to gantry robot to enter wrapping zone *)
    bWrapperCycleStart       : BOOL;     (* Command to initiate stretch wrapping cycle *)
    bConveyorTransferEnable  : BOOL;     (* Command to transfer pallet from build zone to wrapper zone *)
    rCalculatedTensionTrim   : REAL;     (* Real-time tension PID trim value for wrapper motor drive *)
    bSystemFaultAlarm        : BOOL;     (* Global fault flag indicating sequence breakdown or safety trip *)
    iCurrentState            : INT;      (* State machine current step indicator for HMI diagnostic *)
END_VAR

VAR
    iStateMachine            : INT := 0; 
    tZoneTransferTimer       : TON;
    tWrapperTimeoutTimer     : TON;
    tSafetyDebounce          : TON;
    bSafetyLatched           : BOOL := FALSE;
    bFaultLatched            : BOOL := FALSE;
    
    (* PID control variables for film tension *)
    rError                   : REAL := 0.0;
    rIntegral                : REAL := 0.0;
    rDerivative              : REAL := 0.0;
    rLastError               : REAL := 0.0;
    rKp                      : REAL := 2.5;
    rKi                      : REAL := 0.8;
    rKd                      : REAL := 0.1;
    
    (* Constants *)
    STATE_INIT               : INT := 0;
    STATE_READY              : INT := 10;
    STATE_PALLETIZING        : INT := 20;
    STATE_TRANSFER_WAIT      : INT := 30;
    STATE_TRANSFERRING       : INT := 40;
    STATE_WRAPPING           : INT := 50;
    STATE_DISCHARGING        : INT := 60;
    STATE_FAULT              : INT := 99;
END_VAR

(* === MAIN SAFETY AND PERMISSIVE LOGIC === *)
tSafetyDebounce(IN := NOT bEStopSafetyRelayOK, PT := T#50MS);
IF tSafetyDebounce.Q THEN
    bSafetyLatched := TRUE;
END_IF;

IF bSafetyLatched OR NOT bSystemEnable THEN
    iStateMachine := STATE_FAULT;
    bGantryPermissive := FALSE;
    bWrapperCycleStart := FALSE;
    bConveyorTransferEnable := FALSE;
    bSystemFaultAlarm := TRUE;
    
    IF bEStopSafetyRelayOK AND bSystemEnable AND NOT bFaultLatched THEN
        (* Reset condition *)
        bSafetyLatched := FALSE;
        bSystemFaultAlarm := FALSE;
        iStateMachine := STATE_INIT;
    END_IF;
    
    iCurrentState := iStateMachine;
    RETURN;
END_IF;

(* === MAIN STATE MACHINE === *)
CASE iStateMachine OF
    
    STATE_INIT: (* Initialize and check home states *)
        bGantryPermissive := FALSE;
        bWrapperCycleStart := FALSE;
        bConveyorTransferEnable := FALSE;
        
        IF bGantryHomePosition AND bWrapperHomePosition THEN
            iStateMachine := STATE_READY;
        END_IF;

    STATE_READY: (* Wait for palletizing start *)
        bGantryPermissive := TRUE;
        IF NOT bPalletFullSignal THEN
            iStateMachine := STATE_PALLETIZING;
        END_IF;

    STATE_PALLETIZING: (* Gantry is actively building the pallet *)
        bGantryPermissive := TRUE;
        IF bPalletFullSignal THEN
            bGantryPermissive := FALSE;
            iStateMachine := STATE_TRANSFER_WAIT;
        END_IF;

    STATE_TRANSFER_WAIT: (* Ensure wrapper is ready for new pallet *)
        IF bWrapperHomePosition AND bGantryHomePosition THEN
            tZoneTransferTimer(IN := TRUE, PT := T#2S);
            IF tZoneTransferTimer.Q THEN
                tZoneTransferTimer(IN := FALSE);
                iStateMachine := STATE_TRANSFERRING;
            END_IF;
        ELSE
            tZoneTransferTimer(IN := FALSE);
        END_IF;

    STATE_TRANSFERRING: (* Move pallet to wrapper *)
        bConveyorTransferEnable := TRUE;
        (* In a real system, a photo-eye would confirm arrival. Using a timer here for simulation. *)
        tZoneTransferTimer(IN := TRUE, PT := T#5S);
        IF tZoneTransferTimer.Q THEN
            bConveyorTransferEnable := FALSE;
            tZoneTransferTimer(IN := FALSE);
            iStateMachine := STATE_WRAPPING;
        END_IF;

    STATE_WRAPPING: (* Execute wrapping cycle with active tension control *)
        bWrapperCycleStart := TRUE;
        
        (* PID Tension Control Loop *)
        rError := rWrapperFilmTensionSP - rWrapperFilmTensionAct;
        rIntegral := rIntegral + (rError * 0.1); (* Assuming 100ms cycle time *)
        IF rIntegral > 50.0 THEN rIntegral := 50.0; END_IF;
        IF rIntegral < -50.0 THEN rIntegral := -50.0; END_IF;
        rDerivative := (rError - rLastError) / 0.1;
        rCalculatedTensionTrim := (rKp * rError) + (rKi * rIntegral) + (rKd * rDerivative);
        rLastError := rError;
        
        tWrapperTimeoutTimer(IN := TRUE, PT := T#45S); (* Wrapping should complete in 45s *)
        
        (* Assuming the wrapper cycle drops the start signal internally when done or we wait for wrapper home *)
        IF bWrapperHomePosition AND tWrapperTimeoutTimer.ET > T#5S THEN
            bWrapperCycleStart := FALSE;
            tWrapperTimeoutTimer(IN := FALSE);
            rIntegral := 0.0; (* Reset PID *)
            iStateMachine := STATE_DISCHARGING;
        ELSIF tWrapperTimeoutTimer.Q THEN
            (* Wrapper sequence timed out *)
            bFaultLatched := TRUE;
            iStateMachine := STATE_FAULT;
        END_IF;

    STATE_DISCHARGING: (* Eject finished pallet *)
        IF bPalletDischargeClear THEN
            bConveyorTransferEnable := TRUE;
            tZoneTransferTimer(IN := TRUE, PT := T#4S);
            IF tZoneTransferTimer.Q THEN
                bConveyorTransferEnable := FALSE;
                tZoneTransferTimer(IN := FALSE);
                iStateMachine := STATE_READY;
            END_IF;
        END_IF;

    STATE_FAULT: (* System faulted out *)
        bSystemFaultAlarm := TRUE;
        bGantryPermissive := FALSE;
        bWrapperCycleStart := FALSE;
        bConveyorTransferEnable := FALSE;
        tZoneTransferTimer(IN := FALSE);
        tWrapperTimeoutTimer(IN := FALSE);
        
        IF NOT bFaultLatched THEN
            iStateMachine := STATE_INIT;
        END_IF;

END_CASE;

iCurrentState := iStateMachine;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump({"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}, f, ensure_ascii=False)
print(f"Saved to {filename}")
