import json, uuid, os

prompt = """<USER_REQUEST>
You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Industrial Scale High-Volume Water Desalination (SWRO)**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Reverse osmosis isobaric energy recovery device (ERD) hydraulic balancing, high-pressure pump (HPP) variable frequency cavitation prevention, and membrane bio-fouling shock dosing). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_SWRO_Desalination\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Industrial Scale High-Volume Water Desalination (SWRO)

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT.
</USER_REQUEST>"""

code = """```iec-st
FUNCTION_BLOCK FB_SWRO_Desalination_ERD_HPP_Control
VAR_INPUT
    (* Required physical inputs *)
    bSystemEnable           : BOOL;     (* Overall system enable signal *)
    bEmergencyStop          : BOOL;     (* Safety circuit OK (active high) *)
    rFeedWaterPress         : REAL;     (* Feed water pressure to HPP (bar) *)
    rHPP_DischargePress     : REAL;     (* HPP discharge pressure (bar) *)
    rERD_BrineFlow          : REAL;     (* Brine flow through ERD (m3/h) *)
    rMembraneDiffPress      : REAL;     (* Membrane differential pressure (bar) *)
    rFeedSalinity           : REAL;     (* Feed water salinity (TDS ppm) *)
    rFeedTemp               : REAL;     (* Feed water temperature (deg C) *)
END_VAR
VAR_OUTPUT
    (* Required physical outputs *)
    bSystemReady            : BOOL;     (* System ready for operation *)
    bSystemFault            : BOOL;     (* General fault flag *)
    rHPP_VFD_SpeedCmd       : REAL;     (* High Pressure Pump VFD Speed Command (0-100%) *)
    rERD_ValvePosCmd        : REAL;     (* ERD balancing valve position command (0-100%) *)
    bBioFoulingDoseActive   : BOOL;     (* Shock dosing pump active flag *)
    iCurrentState           : INT;      (* Current operating state code *)
END_VAR
VAR
    (* Internal State and Timers *)
    iState                  : INT := 0; (* 0: IDLE, 10: PRE_CHECK, 20: STARTUP, 30: RUN, 40: DOSING, 99: FAULT *)
    tStartupDelay           : TON;
    tDoseTimer              : TON;
    tFaultTimer             : TON;
    
    (* Internal process calculation variables *)
    rTargetHPP_Press        : REAL;
    rOsmoticPressOffset     : REAL;
    rFlowError              : REAL;
    rPID_Integral           : REAL := 0.0;
    rPID_Kp                 : REAL := 2.5;
    rPID_Ki                 : REAL := 0.5;
    bPressFault             : BOOL;
    
    (* Constants *)
    MIN_FEED_PRESS          : REAL := 2.5; (* bar *)
    MAX_DIFF_PRESS          : REAL := 4.5; (* bar *)
    NOMINAL_FLOW            : REAL := 1200.0; (* m3/h *)
END_VAR

(* === MAIN LOGIC === *)
(* 1. Safety and Interlocks *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bSystemFault := TRUE;
    rHPP_VFD_SpeedCmd := 0.0;
    rERD_ValvePosCmd := 0.0;
    bBioFoulingDoseActive := FALSE;
    iState := 99;
    iCurrentState := iState;
    RETURN;
END_IF;

(* 2. Process Fault Detection *)
bPressFault := (rFeedWaterPress < MIN_FEED_PRESS) OR (rMembraneDiffPress > MAX_DIFF_PRESS);
tFaultTimer(IN := bPressFault, PT := T#3S);

IF tFaultTimer.Q THEN
    bSystemFault := TRUE;
    iState := 99;
END_IF;

(* 3. Osmotic Pressure Compensation Calculation *)
(* Rough estimation of osmotic pressure based on Salinity and Temp *)
rOsmoticPressOffset := (rFeedSalinity * 0.00069) * (rFeedTemp + 273.15) / 298.15;
rTargetHPP_Press := 55.0 + rOsmoticPressOffset; 

(* 4. State Machine Control *)
CASE iState OF
    0: (* IDLE *)
        bSystemReady := TRUE;
        bSystemFault := FALSE;
        rHPP_VFD_SpeedCmd := 0.0;
        rERD_ValvePosCmd := 0.0;
        bBioFoulingDoseActive := FALSE;
        
        IF bSystemEnable AND NOT bPressFault THEN
            bSystemReady := FALSE;
            iState := 10;
        END_IF;

    10: (* PRE_CHECK & PRIMING *)
        (* Position ERD Valve to safe starting position *)
        rERD_ValvePosCmd := 50.0; 
        tStartupDelay(IN := TRUE, PT := T#10S);
        
        IF tStartupDelay.Q THEN
            tStartupDelay(IN := FALSE);
            iState := 20;
        END_IF;

    20: (* STARTUP RAMP *)
        (* Slowly ramp up HPP VFD *)
        rHPP_VFD_SpeedCmd := rHPP_VFD_SpeedCmd + 0.1;
        IF rHPP_VFD_SpeedCmd > 30.0 THEN
            iState := 30;
        END_IF;

    30: (* NORMAL RUN - Hydraulic Balancing & HPP Control *)
        (* Simple PI control for ERD flow balancing *)
        rFlowError := NOMINAL_FLOW - rERD_BrineFlow;
        rPID_Integral := rPID_Integral + (rFlowError * rPID_Ki * 0.1); 
        
        (* Anti-windup *)
        IF rPID_Integral > 100.0 THEN rPID_Integral := 100.0; END_IF;
        IF rPID_Integral < -100.0 THEN rPID_Integral := -100.0; END_IF;
        
        rERD_ValvePosCmd := (rFlowError * rPID_Kp) + rPID_Integral;
        
        (* Saturation limits for Valve *)
        IF rERD_ValvePosCmd > 100.0 THEN rERD_ValvePosCmd := 100.0; END_IF;
        IF rERD_ValvePosCmd < 0.0 THEN rERD_ValvePosCmd := 0.0; END_IF;

        (* VFD Speed matching target pressure *)
        IF rHPP_DischargePress < rTargetHPP_Press THEN
            rHPP_VFD_SpeedCmd := rHPP_VFD_SpeedCmd + 0.05;
        ELSIF rHPP_DischargePress > rTargetHPP_Press THEN
            rHPP_VFD_SpeedCmd := rHPP_VFD_SpeedCmd - 0.05;
        END_IF;
        
        (* Saturation limits for VFD *)
        IF rHPP_VFD_SpeedCmd > 100.0 THEN rHPP_VFD_SpeedCmd := 100.0; END_IF;
        IF rHPP_VFD_SpeedCmd < 20.0 THEN rHPP_VFD_SpeedCmd := 20.0; END_IF;

        (* Check if Membrane Bio-Fouling Shock Dosing is needed *)
        IF rMembraneDiffPress > (MAX_DIFF_PRESS * 0.8) THEN
            iState := 40;
        END_IF;
        
        IF NOT bSystemEnable THEN
            iState := 0;
        END_IF;

    40: (* BIO-FOULING SHOCK DOSING *)
        bBioFoulingDoseActive := TRUE;
        tDoseTimer(IN := TRUE, PT := T#5M); (* Dose for 5 minutes *)
        
        IF tDoseTimer.Q THEN
            tDoseTimer(IN := FALSE);
            bBioFoulingDoseActive := FALSE;
            iState := 30; (* Return to normal run *)
        END_IF;

    99: (* FAULT STATE *)
        bSystemFault := TRUE;
        bSystemReady := FALSE;
        rHPP_VFD_SpeedCmd := 0.0;
        rERD_ValvePosCmd := 0.0;
        bBioFoulingDoseActive := FALSE;
        
        IF NOT bPressFault AND NOT bSystemEnable THEN
            iState := 0; (* Reset fault if clear and enable drops *)
        END_IF;
        
END_CASE;

iCurrentState := iState;

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
