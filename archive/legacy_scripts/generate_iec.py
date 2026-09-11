import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Automated Gigafactory Roll-to-Roll Solid-State Battery Electrolyte Coating**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Micron-precision slot-die fluid meniscus profiling, infrared oven continuous web tensioning, and non-destructive inline x-ray thickness gauging). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_BatteryCoatingWebControl\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Automated Gigafactory Roll-to-Roll Solid-State Battery Electrolyte Coating

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_SSB_ElectrolyteCoater
VAR_INPUT
    bEnable                 : BOOL;     (* System master enable signal *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal (TRUE = Safe, FALSE = E-Stop) *)
    rWebTensionActual       : REAL;     (* Current web tension measured by load cells [N] *)
    rCoatingThicknessXRay   : REAL;     (* Inline non-destructive X-ray gauge thickness [um] *)
    rMeniscusPressure       : REAL;     (* Slot-die meniscus vacuum pressure [mBar] *)
    bOvenTempInterlock      : BOOL;     (* IR oven temperature stabilized and within limits *)
    rWebSpeedFeedback       : REAL;     (* Encoder feedback for web speed [m/min] *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;     (* Machine is prepped and ready for production run *)
    rWebSpeedCommand        : REAL;     (* Drive reference for main nip roller [m/min] *)
    rTensionCommand         : REAL;     (* Unwind/Rewind torque reference mapped to tension [N] *)
    rPumpSpeedCommand       : REAL;     (* Slurry delivery gear pump speed reference [RPM] *)
    rDieGapActuator         : REAL;     (* Piezo actuator reference for slot die gap [um] *)
    bFaultAlarm             : BOOL;     (* General machine fault alarm active *)
    iStateCode              : INT;      (* Current active state of the coating machine *)
END_VAR
VAR
    iState                  : INT := 0; 
    tRampTimer              : TON;      
    tFilterTimer            : TON;
    rThicknessFiltered      : REAL := 0.0;
    rThicknessError         : REAL := 0.0;
    rPumpIntegral           : REAL := 0.0;
    rKp_Thickness           : REAL := 0.25;
    rKi_Thickness           : REAL := 0.05;
    rTargetThickness        : REAL := 25.0; (* 25 microns for solid state electrolyte *)
    rTargetTension          : REAL := 150.0; (* 150 N target for web handling *)
    bInitComplete           : BOOL := FALSE;
END_VAR

(* === MAIN LOGIC === *)
(* 1. Safety Interlocks & E-Stop Handler *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bFaultAlarm := TRUE;
    rWebSpeedCommand := 0.0;
    rTensionCommand := 0.0;
    rPumpSpeedCommand := 0.0;
    rDieGapActuator := 0.0;
    iState := 99; (* FAULT STATE *)
    iStateCode := iState;
    RETURN;
END_IF;

(* 2. Signal Conditioning - First-order low pass filter for X-ray gauge noise *)
rThicknessFiltered := rThicknessFiltered + 0.1 * (rCoatingThicknessXRay - rThicknessFiltered);

(* 3. State Machine Control *)
CASE iState OF
    0: (* IDLE *)
        bSystemReady := FALSE;
        bFaultAlarm := FALSE;
        rWebSpeedCommand := 0.0;
        rPumpSpeedCommand := 0.0;
        
        IF bEnable AND bOvenTempInterlock THEN
            iState := 10;
        END_IF;
        
    10: (* INITIALIZE TENSION *)
        rTensionCommand := rTargetTension;
        
        (* Wait for tension to settle within 5% tolerance *)
        IF ABS(rWebTensionActual - rTargetTension) < (rTargetTension * 0.05) THEN
            tRampTimer(IN := TRUE, PT := T#2S);
            IF tRampTimer.Q THEN
                tRampTimer(IN := FALSE);
                bSystemReady := TRUE;
                iState := 20;
            END_IF;
        ELSE
            tRampTimer(IN := FALSE);
        END_IF;
        
    20: (* PRODUCTION RAMP UP *)
        rWebSpeedCommand := 15.0; (* Ramp to 15 m/min *)
        
        IF rWebSpeedFeedback >= 14.5 THEN
            iState := 30;
        END_IF;

    30: (* ACTIVE COATING & THICKNESS PID CONTROL *)
        (* Meniscus vacuum control logic interlock *)
        IF rMeniscusPressure > -10.0 THEN
            (* Vacuum lost, abort coating to prevent edge bead defects *)
            iState := 40; 
        END_IF;
        
        (* PI Control for Slot Die Pump Speed based on X-Ray Feedback *)
        rThicknessError := rTargetThickness - rThicknessFiltered;
        rPumpIntegral := rPumpIntegral + (rThicknessError * rKi_Thickness);
        
        (* Anti-windup for integral term *)
        IF rPumpIntegral > 50.0 THEN rPumpIntegral := 50.0; END_IF;
        IF rPumpIntegral < -50.0 THEN rPumpIntegral := -50.0; END_IF;
        
        rPumpSpeedCommand := 120.0 + (rThicknessError * rKp_Thickness) + rPumpIntegral;
        
        (* Dynamic Piezo Die Gap adjustment for edge profiling *)
        rDieGapActuator := 50.0 - (rThicknessError * 0.5);

        IF NOT bEnable THEN
            iState := 40;
        END_IF;

    40: (* SHUTDOWN SEQUENCE *)
        rPumpSpeedCommand := 0.0;
        rWebSpeedCommand := 0.0;
        
        IF rWebSpeedFeedback < 0.5 THEN
            rTensionCommand := 0.0;
            bSystemReady := FALSE;
            iState := 0;
        END_IF;
        
    99: (* FAULT HANDLING *)
        bFaultAlarm := TRUE;
        IF bEmergencyStop AND bEnable = FALSE THEN
            bFaultAlarm := FALSE;
            iState := 0;
        END_IF;
        
END_CASE;

iStateCode := iState;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": code}
    ]
}

with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
