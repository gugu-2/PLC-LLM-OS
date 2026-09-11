import json, uuid, os

prompt = """<USER_REQUEST>
You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Industrial Scale Closed-Loop Aquaculture System (RAS) Biofilter**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Nitrosomonas/Nitrobacter nitrification boundary DO (Dissolved Oxygen) tracking, redox potential ozonation breakpoint control, and ultra-violet trans-membrane clarification). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_RAS_BiofilterControl\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Industrial Scale Closed-Loop Aquaculture System (RAS) Biofilter

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT.
</USER_REQUEST>"""

code = """```iec-st
FUNCTION_BLOCK FB_RAS_BiofilterControl
VAR_INPUT
    bEnable                 : BOOL;     (* System master enable signal *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal, active TRUE *)
    rDissolvedOxygen        : REAL;     (* DO concentration in mg/L *)
    rWaterTemp              : REAL;     (* Water temperature in degrees C *)
    rORP_Value              : REAL;     (* Oxidation Reduction Potential in mV *)
    rAmmoniaLevel           : REAL;     (* TAN - Total Ammonia Nitrogen mg/L *)
    rNitrateLevel           : REAL;     (* NO3-N in mg/L *)
    bUVSystemOK             : BOOL;     (* UV Sterilizer ready and OK *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;     (* System ready status *)
    rOzoneDosingRate        : REAL;     (* O3 generator output command % *)
    rO2InjectionRate        : REAL;     (* Oxygen injection command % *)
    rBypassValvePos         : REAL;     (* Biofilter bypass valve 0-100% *)
    bAlarmDO                : BOOL;     (* DO Alarm active *)
    bAlarmORP               : BOOL;     (* ORP limits breached *)
    bSystemFault            : BOOL;     (* General system fault *)
END_VAR
VAR
    (* Internal State and Filtering *)
    iState                  : INT := 0;
    tTimer                  : TON;
    tDelayOzone             : TON;
    
    (* Filtered values *)
    rDO_Filtered            : REAL := 0.0;
    rORP_Filtered           : REAL := 0.0;
    rTemp_Filtered          : REAL := 0.0;
    
    (* Filter Constants (EMA) *)
    rAlpha                  : REAL := 0.1;
    
    (* PID internal values (simplified for ST) *)
    rO2_Setpoint            : REAL := 8.5;
    rORP_Setpoint           : REAL := 320.0;
    rO2_Error               : REAL := 0.0;
    rORP_Error              : REAL := 0.0;
    rO2_P_Term              : REAL := 0.0;
    rORP_P_Term             : REAL := 0.0;
    
    (* Constants *)
    Kp_O2                   : REAL := 25.0;
    Kp_ORP                  : REAL := 0.15;
    DO_MIN_LIMIT            : REAL := 6.0;
    DO_MAX_LIMIT            : REAL := 12.0;
    ORP_MAX_LIMIT           : REAL := 400.0;
END_VAR

(* === MAIN LOGIC === *)
(* Multi-layer Safety Interlock *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bSystemFault := TRUE;
    rOzoneDosingRate := 0.0;
    rO2InjectionRate := 0.0;
    rBypassValvePos := 100.0; (* Full bypass on E-Stop *)
    iState := 0;
    RETURN;
END_IF;

(* Sensor Noise Filtering using Exponential Moving Average *)
rDO_Filtered := (rAlpha * rDissolvedOxygen) + ((1.0 - rAlpha) * rDO_Filtered);
rORP_Filtered := (rAlpha * rORP_Value) + ((1.0 - rAlpha) * rORP_Filtered);
rTemp_Filtered := (rAlpha * rWaterTemp) + ((1.0 - rAlpha) * rTemp_Filtered);

(* Alarm Management *)
bAlarmDO := (rDO_Filtered < DO_MIN_LIMIT) OR (rDO_Filtered > DO_MAX_LIMIT);
bAlarmORP := (rORP_Filtered > ORP_MAX_LIMIT);
bSystemFault := bAlarmDO OR bAlarmORP OR NOT bUVSystemOK;

CASE iState OF
    0: (* IDLE & SAFETY CHECK *)
        bSystemReady := FALSE;
        rOzoneDosingRate := 0.0;
        rO2InjectionRate := 0.0;
        rBypassValvePos := 100.0; (* Bypass active *)
        
        IF bEnable AND NOT bSystemFault THEN
            iState := 10;
        END_IF;

    10: (* INITIALIZATION / PRIMING *)
        rBypassValvePos := 50.0; (* Partial bypass during prime *)
        tTimer(IN := TRUE, PT := T#10S);
        
        IF tTimer.Q THEN
            tTimer(IN := FALSE);
            iState := 20;
        END_IF;
        
        IF NOT bEnable OR bSystemFault THEN
            tTimer(IN := FALSE);
            iState := 0;
        END_IF;

    20: (* RUNNING: Advanced PID & State Machine Resilience *)
        bSystemReady := TRUE;
        rBypassValvePos := 0.0; (* Full flow through biofilter *)
        
        (* Nitrosomonas / Nitrobacter boundary DO tracking *)
        (* Adjust O2 Setpoint dynamically based on Ammonia load (Feed-Forward) *)
        IF rAmmoniaLevel > 1.5 THEN
            rO2_Setpoint := 9.5;
        ELSIF rAmmoniaLevel > 0.5 THEN
            rO2_Setpoint := 8.5;
        ELSE
            rO2_Setpoint := 7.5;
        END_IF;
        
        (* Proportional control for O2 Injection *)
        rO2_Error := rO2_Setpoint - rDO_Filtered;
        IF rO2_Error > 0.0 THEN
            rO2_P_Term := rO2_Error * Kp_O2;
        ELSE
            rO2_P_Term := 0.0;
        END_IF;
        
        (* Clamp O2 Injection Rate 0-100% *)
        IF rO2_P_Term > 100.0 THEN
            rO2InjectionRate := 100.0;
        ELSIF rO2_P_Term < 0.0 THEN
            rO2InjectionRate := 0.0;
        ELSE
            rO2InjectionRate := rO2_P_Term;
        END_IF;
        
        (* Redox potential ozonation breakpoint control *)
        rORP_Error := rORP_Setpoint - rORP_Filtered;
        IF rORP_Error > 0.0 THEN
            rORP_P_Term := rORP_Error * Kp_ORP;
        ELSE
            rORP_P_Term := 0.0;
        END_IF;
        
        (* Clamp Ozone Dosing Rate 0-100% *)
        IF rORP_P_Term > 100.0 THEN
            rOzoneDosingRate := 100.0;
        ELSIF rORP_P_Term < 0.0 THEN
            rOzoneDosingRate := 0.0;
        ELSE
            rOzoneDosingRate := rORP_P_Term;
        END_IF;
        
        (* Ozonation safety delay / anti-oscillation timer *)
        tDelayOzone(IN := (rORP_Filtered > rORP_Setpoint + 20.0), PT := T#5S);
        IF tDelayOzone.Q THEN
            rOzoneDosingRate := 0.0;
        END_IF;
        
        (* Watchdogs and Fallbacks *)
        IF NOT bEnable OR bSystemFault THEN
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
