import json, uuid, os

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Next-Generation Offshore Oil Spill Skimmer Dynamic Weir Height Regulation**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Sea surface wave motion acoustic heave filtering, oil slick thickness capacitive sensor feedback, and progressive cavity recovery pump flow matching). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
4. SAVE to isolated file using this exact Python...
"""

code = """```iec-st
FUNCTION_BLOCK FB_SkimmerWeirRegulator
VAR_INPUT
    bEnable                 : BOOL;     (* System master enable signal *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal (Normally Closed = TRUE) *)
    rWaveHeaveAcoustic      : REAL;     (* Sea surface wave motion acoustic heave measurement (m) *)
    rOilSlickThickness      : REAL;     (* Capacitive sensor feedback for oil slick thickness (mm) *)
    rCurrentPumpFlow        : REAL;     (* Progressive cavity recovery pump flow rate (m3/h) *)
    rVesselPitch            : REAL;     (* Skimmer vessel pitch angle (degrees) *)
    rVesselRoll             : REAL;     (* Skimmer vessel roll angle (degrees) *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;     (* Dynamic weir regulation system ready status *)
    rTargetWeirHeight       : REAL;     (* Actuator command for dynamic weir height (mm) *)
    rRecoveryPumpCommand    : REAL;     (* Speed command for progressive cavity pump (0-100%) *)
    bSkimmerFault           : BOOL;     (* Fault alarm output (e.g. sensor failure, interlock trip) *)
    bHighWaveWarning        : BOOL;     (* Warning output when wave heave exceeds safe limits *)
END_VAR
VAR
    iState                  : INT := 0; (* Internal state machine state *)
    tStartTimer             : TON;      (* Initialization timer *)
    tFaultDelay             : TON;      (* Fault debounce timer *)
    rFilteredHeave          : REAL := 0.0; (* Low-pass filtered wave heave *)
    rAlpha                  : REAL := 0.15; (* Filter coefficient *)
    rPitchComp              : REAL;     (* Pitch compensation offset *)
    rRollComp               : REAL;     (* Roll compensation offset *)
    rIdealWeirDepth         : REAL;     (* Calculated ideal depth below surface (mm) *)
    rPumpFlowError          : REAL;     (* Flow mismatch error *)
    rPumpIntegral           : REAL := 0.0; (* Pump PI controller integral term *)
    Kp_Pump                 : REAL := 2.5;
    Ki_Pump                 : REAL := 0.1;
END_VAR

(* === MAIN SAFETY AND INTERLOCK LOGIC === *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    rTargetWeirHeight := 0.0; (* Safe position, fully raised *)
    rRecoveryPumpCommand := 0.0;
    bSkimmerFault := TRUE;
    iState := 99; (* Transition to fault state *)
    RETURN;
END_IF;

(* === HEAVE SENSOR LOW-PASS FILTERING === *)
(* Implement a first-order IIR low-pass filter to dampen extreme acoustic sensor noise *)
rFilteredHeave := (rAlpha * rWaveHeaveAcoustic) + ((1.0 - rAlpha) * rFilteredHeave);

(* Check for excessive sea states *)
IF rFilteredHeave > 2.5 THEN
    bHighWaveWarning := TRUE;
ELSE
    bHighWaveWarning := FALSE;
END_IF;

(* === VESSEL MOTION COMPENSATION === *)
(* Simple trigonometric approximations for pitch/roll effects on weir lip position *)
(* Assuming weir is located 2.0m forward of CG and 1.5m starboard of CG *)
rPitchComp := 2000.0 * SIN(rVesselPitch * 3.14159 / 180.0);
rRollComp := 1500.0 * SIN(rVesselRoll * 3.14159 / 180.0);

(* === MAIN CONTROL STATE MACHINE === *)
CASE iState OF
    0: (* IDLE *)
        bSystemReady := TRUE;
        bSkimmerFault := FALSE;
        rTargetWeirHeight := 0.0;
        rRecoveryPumpCommand := 0.0;
        
        IF bEnable AND bEmergencyStop THEN
            iState := 10;
        END_IF;

    10: (* STARTING *)
        bSystemReady := FALSE;
        (* Prime the weir by dropping it slowly to 50mm below static waterline *)
        rTargetWeirHeight := -50.0;
        
        tStartTimer(IN := TRUE, PT := T#10S);
        IF tStartTimer.Q THEN
            tStartTimer(IN := FALSE);
            iState := 20;
        END_IF;

    20: (* DYNAMIC RUNNING *)
        bSystemReady := TRUE;
        
        (* Calculate ideal weir depth based on oil slick thickness to maximize oil ratio *)
        (* If slick is 10mm, target 12mm depth to ensure full capture with minimal water *)
        rIdealWeirDepth := (rOilSlickThickness * -1.2); 
        
        (* Apply dynamic heave and vessel motion compensations *)
        (* rFilteredHeave is in meters, convert to mm for weir control *)
        rTargetWeirHeight := rIdealWeirDepth - (rFilteredHeave * 1000.0) - rPitchComp - rRollComp;
        
        (* Pump flow matching: PI control to match pump flow to expected weir overflow *)
        (* Expected flow = f(weir depth) - simplified linear relation for demo *)
        rPumpFlowError := (ABS(rTargetWeirHeight) * 1.5) - rCurrentPumpFlow;
        rPumpIntegral := rPumpIntegral + (rPumpFlowError * Ki_Pump);
        
        (* Anti-windup limits *)
        IF rPumpIntegral > 100.0 THEN rPumpIntegral := 100.0; END_IF;
        IF rPumpIntegral < 0.0 THEN rPumpIntegral := 0.0; END_IF;
        
        rRecoveryPumpCommand := (rPumpFlowError * Kp_Pump) + rPumpIntegral;
        
        (* Clamp command to 0-100% *)
        IF rRecoveryPumpCommand > 100.0 THEN rRecoveryPumpCommand := 100.0; END_IF;
        IF rRecoveryPumpCommand < 0.0 THEN rRecoveryPumpCommand := 0.0; END_IF;
        
        (* Fault monitoring during run *)
        tFaultDelay(IN := (rCurrentPumpFlow < 0.1 AND rRecoveryPumpCommand > 50.0), PT := T#5S);
        IF tFaultDelay.Q THEN
            iState := 99;
        END_IF;
        
        IF NOT bEnable THEN
            iState := 0;
        END_IF;
        
    99: (* FAULT HANDLING *)
        bSystemReady := FALSE;
        bSkimmerFault := TRUE;
        rTargetWeirHeight := 0.0; (* Failsafe up *)
        rRecoveryPumpCommand := 0.0;
        
        IF NOT bEnable THEN
            (* Require disable to clear fault *)
            iState := 0;
            bSkimmerFault := FALSE;
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
