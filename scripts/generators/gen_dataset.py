import json, uuid, os

prompt = """<USER_REQUEST>
You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Automotive Solid-State Battery (SSB) Roll-to-Roll Sintering**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Solid electrolyte ceramic powder layer micro-calendering, multi-zone flash photonic sintering synchronization, and extremely low dew point (<-70°C) argon micro-environment mapping). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_SSB_Sintering\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Automotive Solid-State Battery (SSB) Roll-to-Roll Sintering

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT.
</USER_REQUEST>"""

code = """```iec-st
FUNCTION_BLOCK FB_SSB_Sintering_ZoneSync
VAR_INPUT
    (* Main process enables and safety *)
    bSystemEnable           : BOOL;     (* System master enable for the sintering process line *)
    bEStop_OK               : BOOL;     (* Safety circuit OK, monitors all emergency stops and light curtains *)
    
    (* Process variables for Roll-to-Roll and Sintering *)
    rWebTensionAct          : REAL;     (* Actual web tension from load cells (N) *)
    rWebSpeedAct            : REAL;     (* Actual web speed from encoder feedback (m/s) *)
    rDewPointArgon          : REAL;     (* Micro-environment dew point, critical for solid electrolyte (DegC) *)
    rThicknessPreCalender   : REAL;     (* Solid electrolyte thickness measured before calendering via laser (um) *)
    
    (* Zone temperature measurements *)
    arZoneTempAct           : ARRAY[1..10] OF REAL; (* Actual temp across 10 photonic flash sintering zones (DegC) *)
END_VAR
VAR_OUTPUT
    (* Status and Control signals *)
    bSystemReady            : BOOL;     (* Control system is ready for production and environment is stable *)
    bProcessFault           : BOOL;     (* Latched process fault indicator, requiring manual reset *)
    
    (* Control Outputs *)
    rTensionCmd             : REAL;     (* Tension command to unwinder/rewinder servo drives (N) *)
    rSpeedCmd               : REAL;     (* Master speed command for the entire roll-to-roll line (m/s) *)
    rCalenderPressureCmd    : REAL;     (* Target hydraulic pressure for micro-calendering rollers (bar) *)
    arZonePowerCmd          : ARRAY[1..10] OF REAL; (* Power command to photonic flash lamps for rapid sintering (%) *)
END_VAR
VAR
    (* Internal state and PID controllers *)
    iState                  : INT := 0;
    tArgonPurgeTimer        : TON;
    tFlashSyncTimer         : TON;
    
    i                       : INT;
    rThicknessError         : REAL;
    rPID_P_Tension          : REAL := 0.75;
    rPID_I_Tension          : REAL := 0.015;
    rTensionIntegral        : REAL := 0.0;
    rTensionMaxIntegral     : REAL := 50.0;
    
    (* Constants for extreme condition mapping *)
    C_MAX_DEW_POINT         : REAL := -70.0; (* Max allowable dew point for solid electrolyte processing *)
    C_TARGET_THICKNESS      : REAL := 25.0;  (* Target solid electrolyte thickness (um) *)
    C_TARGET_TENSION        : REAL := 150.0; (* Target web tension for delicate ceramic layer (N) *)
    C_NOMINAL_LINE_SPEED    : REAL := 2.5;   (* Production speed for continuous roll-to-roll (m/s) *)
END_VAR

(* === MAIN LOGIC === *)
(* 1. Safety and Interlocks: Highest priority, evaluated every scan cycle *)
IF NOT bEStop_OK THEN
    bSystemReady := FALSE;
    bProcessFault := TRUE;
    rSpeedCmd := 0.0;
    rTensionCmd := 0.0;
    rCalenderPressureCmd := 0.0;
    FOR i := 1 TO 10 DO
        arZonePowerCmd[i] := 0.0;
    END_FOR;
    iState := 0;
    RETURN;
END_IF;

(* 2. Environment Validation: Critical requirement for Solid-State Batteries *)
IF rDewPointArgon > C_MAX_DEW_POINT THEN
    bProcessFault := TRUE;
    bSystemReady := FALSE;
    (* Trigger emergency environmental seal protocol (output flags omitted for brevity) *)
    rSpeedCmd := 0.0; (* Halt web to prevent material degradation *)
    FOR i := 1 TO 10 DO
        arZonePowerCmd[i] := 0.0;
    END_FOR;
    iState := 0;
    RETURN;
END_IF;

(* 3. Master State Machine: Managing the complex process flow *)
CASE iState OF
    0: (* INIT / IDLE *)
        bSystemReady := FALSE;
        rSpeedCmd := 0.0;
        IF bSystemEnable AND NOT bProcessFault AND (rDewPointArgon <= C_MAX_DEW_POINT) THEN
            iState := 10;
        END_IF;

    10: (* PURGE AND PRE-TENSION: Establish environment and tension before motion *)
        tArgonPurgeTimer(IN := TRUE, PT := T#45S);
        
        (* Custom Tension PI Control for delicate ceramic substrate *)
        rTensionIntegral := rTensionIntegral + (C_TARGET_TENSION - rWebTensionAct) * rPID_I_Tension;
        (* Anti-windup for integral term *)
        IF rTensionIntegral > rTensionMaxIntegral THEN
            rTensionIntegral := rTensionMaxIntegral;
        ELSIF rTensionIntegral < -rTensionMaxIntegral THEN
            rTensionIntegral := -rTensionMaxIntegral;
        END_IF;
        
        rTensionCmd := (C_TARGET_TENSION - rWebTensionAct) * rPID_P_Tension + rTensionIntegral;
        
        (* Wait for atmosphere purge and tension stabilization *)
        IF tArgonPurgeTimer.Q AND (ABS(rWebTensionAct - C_TARGET_TENSION) < 2.5) THEN
            tArgonPurgeTimer(IN := FALSE);
            iState := 20;
        END_IF;

    20: (* SINTERING AND CALENDERING RAMP: Operational state *)
        bSystemReady := TRUE;
        rSpeedCmd := C_NOMINAL_LINE_SPEED; (* Running at nominal speed *)
        
        (* Active micro-calendering pressure control based on incoming thickness feedback *)
        rThicknessError := rThicknessPreCalender - C_TARGET_THICKNESS;
        IF rThicknessError > 0.0 THEN
            (* Feedforward + Proportional compensation for oversized coating *)
            rCalenderPressureCmd := 120.0 + (rThicknessError * 3.5); 
        ELSE
            rCalenderPressureCmd := 120.0; (* Base calendering pressure *)
        END_IF;
        
        (* Advanced Flash Photonic Sintering Zone Control *)
        (* Synchronizing multi-zone thermal profile to ensure solid electrolyte density *)
        FOR i := 1 TO 10 DO
            IF arZoneTempAct[i] < 500.0 THEN
                arZonePowerCmd[i] := 90.0; (* Aggressive initial heating profile for ceramic bonding *)
            ELSIF arZoneTempAct[i] > 650.0 THEN
                arZonePowerCmd[i] := 10.0; (* Prevent thermal runaway and substrate melting *)
            ELSE
                arZonePowerCmd[i] := 55.0; (* Maintain optimal thermal equilibrium for sintering *)
            END_IF;
        END_FOR;
        
        IF NOT bSystemEnable THEN
            iState := 30;
        END_IF;

    30: (* SHUTDOWN SEQUENCE: Controlled stop to prevent web tearing *)
        rSpeedCmd := 0.0;
        rCalenderPressureCmd := 0.0; (* Release nip rollers *)
        FOR i := 1 TO 10 DO
            arZonePowerCmd[i] := 0.0; (* Extinguish flash lamps *)
        END_FOR;
        
        IF rWebSpeedAct < 0.05 THEN
            iState := 0; (* Return to idle once web is fully stopped *)
        END_IF;
        
    ELSE
        (* Failsafe default *)
        iState := 0;
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
