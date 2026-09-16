import json, uuid, os

prompt = """<USER_REQUEST>
You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Cryogenic LNG Ship-to-Shore Loading Arm Kinematic Compensation**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_LNG_LoadingArm\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Cryogenic LNG Ship-to-Shore Loading Arm Kinematic Compensation

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT.
</USER_REQUEST>"""

code = """```iec-st
FUNCTION_BLOCK FB_LNG_KinematicCompensation
VAR_INPUT
    bEnable                 : BOOL;     (* System master enable signal *)
    bEmergencyStop          : BOOL;     (* ESD (Emergency Shutdown) hardwired safety relay OK signal *)
    rShipHeave              : REAL;     (* Ship vertical displacement (Heave) in meters, via laser reference *)
    rShipSway               : REAL;     (* Ship lateral displacement (Sway) in meters *)
    rShipSurge              : REAL;     (* Ship longitudinal displacement (Surge) in meters *)
    rArmAngleAlpha          : REAL;     (* Inboard arm angle sensor feedback (degrees) *)
    rArmAngleBeta           : REAL;     (* Outboard arm angle sensor feedback (degrees) *)
    rCryoTempCelsius        : REAL;     (* Cryogenic product temperature at swivel joints (-162C typical) *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;     (* System fully initialized and ready for auto compensation *)
    rCompensatedTargetAlpha : REAL;     (* Kinematically compensated target angle for Alpha joint *)
    rCompensatedTargetBeta  : REAL;     (* Kinematically compensated target angle for Beta joint *)
    bEnvelopeWarning        : BOOL;     (* Warning: Ship drifting near maximum safe loading envelope *)
    bAlarm                  : BOOL;     (* Critical fault or envelope breach alarm - triggers ESD *)
END_VAR
VAR
    iState                  : INT := 0; (* Internal state machine state *)
    tESDTimer               : TON;      (* Delay timer for debounce of emergency signals *)
    tKinematicCycle         : TON;      (* Cycle timer for kinematic loop computation *)
    rAlphaCurrentFilter     : REAL;     (* Low-pass filtered Alpha angle *)
    rBetaCurrentFilter      : REAL;     (* Low-pass filtered Beta angle *)
    rMaxEnvelopeRadius      : REAL := 15.0; (* Maximum safe tracking envelope in meters *)
    rWarningRadius          : REAL := 12.5; (* Pre-alarm warning envelope in meters *)
    rCurrentRadius          : REAL;     (* Calculated Pythagorean radius of ship drift *)
    rThermalShrinkFactor    : REAL;     (* Compensation factor for arm length change due to cryogenic temps *)
    rAlphaD                 : REAL;     (* Derivative term for Alpha *)
    rAlphaPrev              : REAL;     (* Previous Alpha for derivative *)
END_VAR

(* === MAIN LOGIC === *)

(* Low Pass Filtering on Sensor Inputs for Noise Reduction *)
rAlphaCurrentFilter := rAlphaCurrentFilter + 0.1 * (rArmAngleAlpha - rAlphaCurrentFilter);
rBetaCurrentFilter := rBetaCurrentFilter + 0.1 * (rArmAngleBeta - rBetaCurrentFilter);

(* Emergency Stop Interlock Check *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bAlarm := TRUE;
    rCompensatedTargetAlpha := rAlphaCurrentFilter; (* Freeze in place *)
    rCompensatedTargetBeta := rBetaCurrentFilter;   (* Freeze in place *)
    iState := 99; (* Fault state *)
    RETURN;
END_IF;

(* Compute the 3D drift radius of the ship manifold relative to shore base *)
rCurrentRadius := SQRT(rShipHeave * rShipHeave + rShipSway * rShipSway + rShipSurge * rShipSurge);

(* Thermal Contraction Compensation: Arms shrink at -162 Celsius, shifting kinematics *)
rThermalShrinkFactor := 1.0 - ((20.0 - rCryoTempCelsius) * 0.000015); (* Approx coeff for stainless *)

CASE iState OF
    0: (* IDLE & INITIALIZATION *)
        bSystemReady := FALSE;
        bAlarm := FALSE;
        bEnvelopeWarning := FALSE;
        rCompensatedTargetAlpha := rAlphaCurrentFilter;
        rCompensatedTargetBeta := rBetaCurrentFilter;
        
        IF bEnable THEN
            tKinematicCycle(IN := FALSE);
            iState := 10;
        END_IF;

    10: (* RUNNING KINEMATIC SOLVER *)
        (* Determine Envelope Boundaries *)
        IF rCurrentRadius >= rMaxEnvelopeRadius THEN
            bAlarm := TRUE; 
            iState := 99; (* Breach triggers fault *)
        ELSIF rCurrentRadius >= rWarningRadius THEN
            bEnvelopeWarning := TRUE;
        ELSE
            bEnvelopeWarning := FALSE;
        END_IF;

        (* Compute Inverse Kinematics for Targets (Simplified Mockup of 3D Jacobian) *)
        rCompensatedTargetAlpha := rAlphaCurrentFilter + (rShipHeave * 0.5 + rShipSurge * 0.2) / rThermalShrinkFactor;
        rCompensatedTargetBeta  := rBetaCurrentFilter - (rShipSway * 0.3) / rThermalShrinkFactor;

        (* Limit Rate of Change / Derivative checking *)
        rAlphaD := (rCompensatedTargetAlpha - rAlphaPrev);
        IF rAlphaD > 2.0 THEN
            rCompensatedTargetAlpha := rAlphaPrev + 2.0; (* Rate limit *)
        ELSIF rAlphaD < -2.0 THEN
            rCompensatedTargetAlpha := rAlphaPrev - 2.0; (* Rate limit *)
        END_IF;
        rAlphaPrev := rCompensatedTargetAlpha;

        tKinematicCycle(IN := TRUE, PT := T#50MS);
        IF tKinematicCycle.Q THEN
            tKinematicCycle(IN := FALSE);
            iState := 20;
        END_IF;

    20: (* CYCLE COMPLETE, AWAITING NEXT TICK *)
        bSystemReady := TRUE;
        IF NOT bEnable THEN
            iState := 0;
        ELSE
            iState := 10;
        END_IF;

    99: (* FAULT HANDLING *)
        bSystemReady := FALSE;
        bEnvelopeWarning := FALSE;
        IF bEnable = FALSE AND bEmergencyStop = TRUE AND rCurrentRadius < rMaxEnvelopeRadius THEN
            bAlarm := FALSE;
            iState := 0; (* Reset sequence *)
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
