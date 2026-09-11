import json, uuid, os

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Utility-Scale Concentrating Solar Power (CSP) Molten Salt Thermal Storage**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Hot-tank freeze protection skin-effect trace heating, stratified thermocline boundary management, and nitrate salt pump anti-cavitation sub-cooling). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_CSP_MoltenSaltStorage\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Utility-Scale Concentrating Solar Power (CSP) Molten Salt Thermal Storage

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_CSP_MoltenSaltStorage
VAR_INPUT
    (* Required: at least 4-8 physical inputs with types and comments *)
    bEnable                 : BOOL;     (* System master enable signal *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal (1=OK, 0=Stop) *)
    rTankTemperature        : REAL;     (* Bulk molten salt temperature in deg C *)
    rSkinTemperature        : REAL;     (* Tank shell skin temperature in deg C *)
    rPumpSuctionPressure    : REAL;     (* Nitrate salt pump suction pressure in bar *)
    rPumpSpeedFeedback      : REAL;     (* Current pump speed in RPM *)
    rFlowRate               : REAL;     (* Mass flow rate of molten salt in kg/s *)
    rSolarFieldTempOut      : REAL;     (* Heat Transfer Fluid (HTF) temperature from field in deg C *)
END_VAR
VAR_OUTPUT
    (* Required: at least 3-6 outputs with types and comments *)
    bSystemReady            : BOOL;     (* Thermal storage system ready status *)
    bTraceHeatingOn         : BOOL;     (* Command to activate skin-effect trace heating *)
    rPumpSpeedSetpoint      : REAL;     (* Pump VFD speed reference signal 0-100% *)
    bAntiCavitationActive   : BOOL;     (* Anti-cavitation sub-cooling interlock active *)
    bFreezeWarning          : BOOL;     (* Danger of molten salt solidification warning *)
    bSystemFault            : BOOL;     (* Critical fault alarm output *)
END_VAR
VAR
    (* Internal state variables *)
    iState                  : INT := 0; 
    tStartupTimer           : TON;
    tTraceHeatingTimer      : TON;
    tCavitationDelay        : TON;
    rFilteredTemp           : REAL := 0.0;
    rFilteredPressure       : REAL := 0.0;
    rErrorSum               : REAL := 0.0;
    rLastTemp               : REAL := 0.0;
    
    (* Constants for Nitrate Salt Properties *)
    c_rFreezeThreshold      : REAL := 240.0; (* Min safe temp deg C, salt freezes ~220C *)
    c_rTargetTemp           : REAL := 565.0; (* Optimal hot tank temp deg C *)
    c_rMinSuctionPress      : REAL := 1.5;   (* Minimum NPSHa in bar to prevent cavitation *)
    
    (* PID Gains for flow control *)
    c_rKp                   : REAL := 2.5;
    c_rKi                   : REAL := 0.15;
    c_rKd                   : REAL := 0.05;
END_VAR

(* === SENSOR NOISE FILTERING (EWMA) === *)
rFilteredTemp := (rFilteredTemp * 0.8) + (rTankTemperature * 0.2);
rFilteredPressure := (rFilteredPressure * 0.7) + (rPumpSuctionPressure * 0.3);

(* === SAFETY & INTERLOCKS === *)
IF NOT bEmergencyStop THEN
    iState := 999; (* FAULT STATE *)
END_IF;

(* Freeze Protection Interlock *)
IF rFilteredTemp < c_rFreezeThreshold OR rSkinTemperature < (c_rFreezeThreshold - 10.0) THEN
    bFreezeWarning := TRUE;
    bTraceHeatingOn := TRUE;
ELSE
    bFreezeWarning := FALSE;
    bTraceHeatingOn := FALSE;
END_IF;

(* Anti-Cavitation Monitoring *)
tCavitationDelay(IN := (rFilteredPressure < c_rMinSuctionPress AND rPumpSpeedFeedback > 100.0), PT := T#2S);
IF tCavitationDelay.Q THEN
    bAntiCavitationActive := TRUE;
    rPumpSpeedSetpoint := 0.0; (* Force pump shutdown to protect impeller *)
ELSE
    bAntiCavitationActive := FALSE;
END_IF;

(* === MAIN STATE MACHINE === *)
CASE iState OF
    0: (* SYSTEM IDLE *)
        bSystemReady := FALSE;
        rPumpSpeedSetpoint := 0.0;
        bSystemFault := FALSE;
        IF bEnable AND bEmergencyStop AND NOT bFreezeWarning THEN
            iState := 10;
        END_IF;

    10: (* WARM-UP & CIRCULATION *)
        bSystemReady := FALSE;
        rPumpSpeedSetpoint := 15.0; (* Low speed circulation *)
        tStartupTimer(IN := TRUE, PT := T#30S);
        IF tStartupTimer.Q AND rFlowRate > 5.0 THEN
            tStartupTimer(IN := FALSE);
            iState := 20;
        ELSIF tStartupTimer.Q AND rFlowRate <= 5.0 THEN
            (* Failed to establish flow *)
            iState := 999;
        END_IF;

    20: (* NORMAL OPERATION (PID CONTROL) *)
        bSystemReady := TRUE;
        
        IF NOT bEnable THEN
            iState := 0;
        END_IF;
        
        IF NOT bAntiCavitationActive THEN
            (* Execute PID loop to maintain thermocline *)
            rErrorSum := rErrorSum + ((c_rTargetTemp - rFilteredTemp) * 0.1);
            IF rErrorSum > 100.0 THEN rErrorSum := 100.0; END_IF;
            IF rErrorSum < -100.0 THEN rErrorSum := -100.0; END_IF;
            
            rPumpSpeedSetpoint := (c_rKp * (c_rTargetTemp - rFilteredTemp)) + 
                                  (c_rKi * rErrorSum) + 
                                  (c_rKd * (rFilteredTemp - rLastTemp) / 0.1);
                                  
            rLastTemp := rFilteredTemp;
            
            (* Clamp output *)
            IF rPumpSpeedSetpoint > 100.0 THEN rPumpSpeedSetpoint := 100.0; END_IF;
            IF rPumpSpeedSetpoint < 15.0 THEN rPumpSpeedSetpoint := 15.0; END_IF;
        END_IF;

    999: (* FAULT HANDLING *)
        bSystemReady := FALSE;
        bSystemFault := TRUE;
        rPumpSpeedSetpoint := 0.0;
        IF bEmergencyStop AND NOT bAntiCavitationActive AND NOT bFreezeWarning AND NOT bEnable THEN
            (* Reset fault state if enable is cycled and conditions are clear *)
            iState := 0;
            bSystemFault := FALSE;
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

filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
