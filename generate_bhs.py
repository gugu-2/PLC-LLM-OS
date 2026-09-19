import json, uuid, os

prompt = """<copy this exact user prompt here>"""
code = """```iec-st
FUNCTION_BLOCK FB_BHS_HighSpeed_CrossBeltSorter
VAR_INPUT
    bEnable                 : BOOL;     (* System enable command from main supervisory system *)
    bEmergencyStopOK        : BOOL;     (* Safety circuit loop status, TRUE = OK *)
    rMainBeltSpeedAct       : REAL;     (* Main sorter belt actual speed in m/s *)
    rBagWeightAct           : REAL;     (* Current bag weight measured by in-feed scale in kg *)
    bBagPresentPEC          : BOOL;     (* Photo-electric cell detecting bag at induction point *)
    rInductionBeltSpeedSet  : REAL;     (* Desired induction belt speed reference in m/s *)
    iDestChuteID            : INT;      (* Target chute ID for the current bag *)
    bChuteFullPEC           : BOOL;     (* Target chute full detection *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;     (* Sorter is ready to accept bags *)
    bInductionDriveRun      : BOOL;     (* Command to run induction belt drive *)
    rInductionDriveSpeed    : REAL;     (* Induction belt drive speed output (m/s) *)
    bCrossBeltActionTrigger : BOOL;     (* Trigger cross-belt discharge action *)
    bAlarmFault             : BOOL;     (* System fault active *)
    iFaultCode              : INT;      (* Active fault code for HMI diagnostics *)
    rCalculatedDischargeTime: REAL;     (* Calculated time to discharge in ms *)
END_VAR
VAR
    iState                  : INT := 0; (* Main state machine variable *)
    tInductionTimeout       : TON;      (* Timeout for induction process *)
    tDischargeTimer         : TON;      (* Timer for tracking bag to chute *)
    rBagPosition            : REAL;     (* Tracked bag position on main belt *)
    rDischargeDistance      : REAL;     (* Distance to target chute in meters *)
    iCurrentBagID           : DINT;     (* Internal tracking ID for bag *)
    
    (* Filter variables for speed *)
    rMainBeltSpeedFiltered  : REAL;
    rFilterAlpha            : REAL := 0.1; (* Low pass filter coefficient *)
    
    (* Constants *)
    rMAX_BELT_SPEED         : REAL := 3.5; (* Maximum main belt speed m/s *)
    rMIN_BELT_SPEED         : REAL := 0.5; (* Minimum main belt speed m/s *)
    rCHUTE_SPACING          : REAL := 1.2; (* Distance between chutes in meters *)
END_VAR

(* === MAIN LOGIC === *)
(* 1. Safety and Enable Interlocks *)
IF NOT bEmergencyStopOK THEN
    bSystemReady := FALSE;
    bInductionDriveRun := FALSE;
    rInductionDriveSpeed := 0.0;
    bCrossBeltActionTrigger := FALSE;
    bAlarmFault := TRUE;
    iFaultCode := 99; (* E-Stop active *)
    iState := 0;
    RETURN;
END_IF;

(* 2. Input Filtering (Low-pass filter for main belt speed noise reduction) *)
rMainBeltSpeedFiltered := rMainBeltSpeedFiltered + rFilterAlpha * (rMainBeltSpeedAct - rMainBeltSpeedFiltered);

(* 3. Fault Monitoring *)
IF bEnable AND (rMainBeltSpeedFiltered > rMAX_BELT_SPEED OR rMainBeltSpeedFiltered < rMIN_BELT_SPEED) THEN
    bAlarmFault := TRUE;
    iFaultCode := 10; (* Belt speed out of limits *)
    iState := 999; (* Fault state *)
END_IF;

IF bChuteFullPEC AND iState = 30 THEN
    bAlarmFault := TRUE;
    iFaultCode := 20; (* Target chute full during routing *)
    iState := 999;
END_IF;

(* 4. Main State Machine *)
CASE iState OF
    0: (* IDLE / INIT *)
        bSystemReady := FALSE;
        bInductionDriveRun := FALSE;
        bCrossBeltActionTrigger := FALSE;
        bAlarmFault := FALSE;
        iFaultCode := 0;
        
        IF bEnable AND NOT bAlarmFault THEN
            iState := 10;
        END_IF;
        
    10: (* READY FOR INDUCTION *)
        bSystemReady := TRUE;
        bInductionDriveRun := FALSE;
        
        IF bBagPresentPEC THEN
            bSystemReady := FALSE; (* Busy *)
            iState := 20;
        END_IF;
        
    20: (* INDUCTING BAG *)
        bInductionDriveRun := TRUE;
        
        (* Match induction speed with main belt speed for smooth transfer, adjusting for bag weight slip factor *)
        IF rBagWeightAct > 25.0 THEN
            rInductionDriveSpeed := rMainBeltSpeedFiltered * 1.05; (* Heavy bag compensation *)
        ELSE
            rInductionDriveSpeed := rMainBeltSpeedFiltered;
        END_IF;
        
        tInductionTimeout(IN := TRUE, PT := T#3S);
        
        (* Assume bag has transferred when PEC clears *)
        IF NOT bBagPresentPEC THEN
            tInductionTimeout(IN := FALSE);
            bInductionDriveRun := FALSE;
            
            (* Calculate discharge geometry *)
            rDischargeDistance := INT_TO_REAL(iDestChuteID) * rCHUTE_SPACING;
            IF rMainBeltSpeedFiltered > 0.1 THEN
                rCalculatedDischargeTime := (rDischargeDistance / rMainBeltSpeedFiltered) * 1000.0; (* in ms *)
            ELSE
                rCalculatedDischargeTime := 99999.0;
            END_IF;
            
            iState := 30;
        ELSIF tInductionTimeout.Q THEN
            (* Induction jam *)
            tInductionTimeout(IN := FALSE);
            bAlarmFault := TRUE;
            iFaultCode := 30; (* Jam at induction *)
            iState := 999;
        END_IF;
        
    30: (* TRACKING ON MAIN BELT *)
        (* Start timer to simulate physical tracking to the chute *)
        (* In a real system, encoder pulses would track this precisely *)
        tDischargeTimer(IN := TRUE, PT := REAL_TO_TIME(rCalculatedDischargeTime));
        
        IF tDischargeTimer.Q THEN
            tDischargeTimer(IN := FALSE);
            bCrossBeltActionTrigger := TRUE;
            iState := 40;
        END_IF;
        
    40: (* DISCHARGING *)
        (* Trigger pulse remains high for 1 scan cycle or specific duration *)
        bCrossBeltActionTrigger := FALSE; 
        iState := 10; (* Return to ready for next bag *)
        
    999: (* FAULT HANDLING *)
        bSystemReady := FALSE;
        bInductionDriveRun := FALSE;
        rInductionDriveSpeed := 0.0;
        bCrossBeltActionTrigger := FALSE;
        
        IF NOT bEnable THEN
            bAlarmFault := FALSE;
            iFaultCode := 0;
            iState := 0; (* Reset fault when enable is dropped *)
        END_IF;
        
END_CASE;

END_FUNCTION_BLOCK
```"""

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Commercial Airport Automated Baggage Handling System (BHS) High-Speed Cross-Belt Sorter**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_Baggage_CrossBeltSorter\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Commercial Airport Automated Baggage Handling System (BHS) High-Speed Cross-Belt Sorter

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

os.makedirs("data/swarm_raw", exist_ok=True)
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
