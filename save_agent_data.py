import json, uuid, os

os.makedirs('data/swarm_raw', exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: High-Speed Submarine Fiber Optic Cable Extrusion Line**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., multi-layer concentricity control, laser micrometer feedback loops, dual-capstan precise tension cascading, and extreme pressure crosshead die regulation). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_CableExtrusion\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: High-Speed Submarine Fiber Optic Cable Extrusion Line

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_SubmarineFiberExtrusion
VAR_INPUT
    bEnable               : BOOL;     (* Main system run command *)
    bEmergencyStop        : BOOL;     (* Safety circuit healthy signal (NC) *)
    rLaserDiameterMicron  : REAL;     (* Feedback from dual-axis laser micrometer [um] *)
    rConcentricityDev_X   : REAL;     (* X-axis deviation from ultrasonic concentricity gauge [um] *)
    rConcentricityDev_Y   : REAL;     (* Y-axis deviation from ultrasonic concentricity gauge [um] *)
    rLineSpeedMpm         : REAL;     (* Master line speed feedback [m/min] *)
    rCrossheadTempC       : REAL;     (* Extruder crosshead melt temperature [deg C] *)
    rCapstanTensionN      : REAL;     (* Feedback from dual-capstan tension loadcell [N] *)
END_VAR
VAR_OUTPUT
    bSystemReady          : BOOL;     (* System is heated and ready for line start *)
    rScrewSpeedRPM        : REAL;     (* Output speed reference to main extruder drive *)
    rCapstanSpeedTrim     : REAL;     (* Speed trim cascade to capstan drive for tension control *)
    rDieCentering_X       : REAL;     (* Servo position for X-axis crosshead centering *)
    rDieCentering_Y       : REAL;     (* Servo position for Y-axis crosshead centering *)
    bAlarm                : BOOL;     (* General fault flag *)
    iErrorCode            : INT;      (* Specific fault code for HMI display *)
END_VAR
VAR
    iState                : INT := 0; (* Main state machine sequencer *)
    tWarmupTimer          : TON;
    rTargetDiameter       : REAL := 17000.0; (* Submarine cable target OD: 17.0 mm *)
    rTargetTension        : REAL := 2500.0;  (* Target tension: 2500 N *)
    
    (* PID state variables for Diameter Control *)
    rDiaError             : REAL;
    rDiaIntegral          : REAL := 0.0;
    rDiaKp                : REAL := 0.05;
    rDiaKi                : REAL := 0.001;
    
    (* PID state variables for Tension Control *)
    rTenError             : REAL;
    rTenIntegral          : REAL := 0.0;
    rTenKp                : REAL := 0.01;
    rTenKi                : REAL := 0.005;
END_VAR

(* === MAIN SAFETY INTERLOCKS === *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    rScrewSpeedRPM := 0.0;
    rCapstanSpeedTrim := 0.0;
    bAlarm := TRUE;
    iErrorCode := 999; (* 999: E-STOP Active *)
    iState := 0;
    RETURN;
END_IF;

(* === STATE MACHINE SUPERVISOR === *)
CASE iState OF
    0: (* IDLE & SAFETY CHECKS *)
        bAlarm := FALSE;
        iErrorCode := 0;
        bSystemReady := FALSE;
        rScrewSpeedRPM := 0.0;
        IF bEnable THEN
            iState := 10;
        END_IF;
        
    10: (* HEATING & SOAKING PHASE *)
        (* Wait for crosshead to reach process temperature (e.g., 210C) *)
        IF rCrossheadTempC > 210.0 THEN
            tWarmupTimer(IN := TRUE, PT := T#300S); (* 5 min thermal soak *)
            IF tWarmupTimer.Q THEN
                tWarmupTimer(IN := FALSE);
                bSystemReady := TRUE;
                iState := 20;
            END_IF;
        ELSE
            tWarmupTimer(IN := FALSE);
        END_IF;
        
        IF NOT bEnable THEN
            iState := 0;
        END_IF;
        
    20: (* RUNNING & DYNAMIC CONTROL REGULATION *)
        (* Loop 1: Outer Diameter Control (Extruder Speed) *)
        rDiaError := rTargetDiameter - rLaserDiameterMicron;
        rDiaIntegral := rDiaIntegral + rDiaError;
        
        (* Anti-windup for diameter loop *)
        IF rDiaIntegral > 5000.0 THEN rDiaIntegral := 5000.0; END_IF;
        IF rDiaIntegral < -5000.0 THEN rDiaIntegral := -5000.0; END_IF;
        
        rScrewSpeedRPM := (rDiaError * rDiaKp) + (rDiaIntegral * rDiaKi) + (rLineSpeedMpm * 0.12);
        IF rScrewSpeedRPM < 0.0 THEN rScrewSpeedRPM := 0.0; END_IF;
        IF rScrewSpeedRPM > 1500.0 THEN rScrewSpeedRPM := 1500.0; END_IF;
        
        (* Loop 2: Capstan Tension Control (Trim Speed) *)
        rTenError := rTargetTension - rCapstanTensionN;
        rTenIntegral := rTenIntegral + rTenError;
        rCapstanSpeedTrim := (rTenError * rTenKp) + (rTenIntegral * rTenKi);
        
        (* Limit capstan trim to +/- 5% of base speed *)
        IF rCapstanSpeedTrim > 5.0 THEN rCapstanSpeedTrim := 5.0; END_IF;
        IF rCapstanSpeedTrim < -5.0 THEN rCapstanSpeedTrim := -5.0; END_IF;
        
        (* Sub-Routine: Extrusion Die Centering (Concentricity) *)
        (* Proportional adjustment based on ultrasonic gauge feedback *)
        rDieCentering_X := rConcentricityDev_X * -0.05;
        rDieCentering_Y := rConcentricityDev_Y * -0.05;
        
        (* Fault Monitoring During Run *)
        IF rLaserDiameterMicron < 15000.0 OR rLaserDiameterMicron > 19000.0 THEN
            bAlarm := TRUE;
            iErrorCode := 101; (* OD Out of tolerance limits *)
        END_IF;
        
        IF NOT bEnable THEN
            iState := 0;
        END_IF;
        
    ELSE
        (* CATCH-ALL FAULT STATE *)
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

filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
