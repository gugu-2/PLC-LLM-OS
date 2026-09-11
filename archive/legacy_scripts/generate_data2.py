import json, uuid, os

os.makedirs('data/swarm_raw', exist_ok=True)
prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Next-Gen Deep-Space Solar Sail Deployment Boom**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Carbon-fiber composite unfurling tension hysteresis, highly-flexible multi-body modal vibration suppression, and piezoelectric root actuator damping). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_SolarSailDeployment\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
   record = {\"messages\": [{\"role\": \"user\", \"content\": prompt}, {\"role\": \"assistant\", \"content\": code}]}
   with open(f\"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json\", \"w\", encoding=\"utf-8\") as f:
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
6. REPLY with: EVOLUTION COMPLETE: Next-Gen Deep-Space Solar Sail Deployment Boom

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_SolarSailBoomDeployer
VAR_INPUT
    bEnableDeploy           : BOOL;     (* System master enable for deployment sequence *)
    bEmergencyHalt          : BOOL;     (* Hardware E-stop or critical fault abort signal *)
    rMotorTensionCurrent    : REAL;     (* Measured spool motor current (Amps) to estimate tension *)
    rBoomRootStrain         : REAL;     (* Piezoelectric strain sensor feedback (microstrain) *)
    rPayloadInertia         : REAL;     (* Estimated payload inertia for adaptive gains (kg*m^2) *)
    bThermalInterlockOK     : BOOL;     (* True if structural temperatures are within safe margins *)
END_VAR
VAR_OUTPUT
    bDeploymentReady        : BOOL;     (* True when initialization and thermal checks pass *)
    rMotorVelocityCmd       : REAL;     (* Unfurling rate command to the spool motor (rad/s) *)
    rPiezoDampingCmd        : REAL;     (* Damping voltage command to root actuators (Volts) *)
    bCriticalFault          : BOOL;     (* True if limits exceeded or hardware failure detected *)
    iDeploymentStage        : INT;      (* Current stage: 0=Init, 10=Pre-Tension, 20=Unfurl, etc. *)
END_VAR
VAR
    iState                  : INT := 0;
    tTensionSettleTimer     : TON;
    tVibrationHoldTimer     : TON;
    rFilteredTension        : REAL := 0.0;
    rFilteredStrain         : REAL := 0.0;
    rAlphaTension           : REAL := 0.1;
    rAlphaStrain            : REAL := 0.05;
    rTargetTension          : REAL := 2.5; 
    rMaxStrainLimit         : REAL := 450.0;
    rIntegrationError       : REAL := 0.0;
    rKpTension              : REAL := 1.2;
    rKiTension              : REAL := 0.5;
END_VAR

(* === MAIN LOGIC === *)
(* Handle Emergency Halts and Interlocks *)
IF bEmergencyHalt OR NOT bThermalInterlockOK THEN
    bDeploymentReady := FALSE;
    bCriticalFault := TRUE;
    rMotorVelocityCmd := 0.0;
    rPiezoDampingCmd := 0.0;
    iState := 999; (* FAULT STATE *)
    iDeploymentStage := iState;
    RETURN;
END_IF;

(* First-order low-pass filters for sensor noise rejection *)
rFilteredTension := rFilteredTension + rAlphaTension * (rMotorTensionCurrent - rFilteredTension);
rFilteredStrain := rFilteredStrain + rAlphaStrain * (rBoomRootStrain - rFilteredStrain);

(* Active Modal Vibration Suppression (Feed-forward) *)
IF ABS(rFilteredStrain) > 50.0 THEN
    rPiezoDampingCmd := rFilteredStrain * -0.02 * (1.0 + rPayloadInertia * 0.1);
ELSE
    rPiezoDampingCmd := 0.0;
END_IF;

(* Main Deployment State Machine *)
CASE iState OF
    0: (* IDLE & INIT *)
        bDeploymentReady := TRUE;
        bCriticalFault := FALSE;
        rMotorVelocityCmd := 0.0;
        iDeploymentStage := 0;
        
        IF bEnableDeploy THEN
            iState := 10;
        END_IF;

    10: (* PRE-TENSIONING *)
        iDeploymentStage := 10;
        (* Slowly ramp current to establish initial unfurling tension *)
        rMotorVelocityCmd := 0.05; 
        
        IF rFilteredTension >= (rTargetTension * 0.8) THEN
            tTensionSettleTimer(IN := TRUE, PT := T#2S);
            IF tTensionSettleTimer.Q THEN
                tTensionSettleTimer(IN := FALSE);
                iState := 20;
            END_IF;
        ELSE
            tTensionSettleTimer(IN := FALSE);
        END_IF;

    20: (* CONTROLLED UNFURLING *)
        iDeploymentStage := 20;
        
        (* PI Control for maintaining constant unfurling tension despite hysteresis *)
        rIntegrationError := rIntegrationError + (rTargetTension - rFilteredTension) * 0.01; (* Assume 10ms task *)
        
        (* Anti-windup clamping *)
        IF rIntegrationError > 5.0 THEN rIntegrationError := 5.0; END_IF;
        IF rIntegrationError < -5.0 THEN rIntegrationError := -5.0; END_IF;
        
        rMotorVelocityCmd := 0.5 + (rKpTension * (rTargetTension - rFilteredTension)) + (rKiTension * rIntegrationError);
        
        (* Over-strain modal excitation check *)
        IF ABS(rFilteredStrain) > (rMaxStrainLimit * 0.8) THEN
            (* Induce pause to let piezo actuators damp the structural ringing *)
            iState := 30;
        END_IF;

    30: (* VIBRATION DAMPING HOLD *)
        iDeploymentStage := 30;
        rMotorVelocityCmd := 0.0;
        
        tVibrationHoldTimer(IN := TRUE, PT := T#10S);
        IF ABS(rFilteredStrain) < 20.0 OR tVibrationHoldTimer.Q THEN
            tVibrationHoldTimer(IN := FALSE);
            iState := 20; (* Resume unfurling *)
        END_IF;
        
    999: (* FAULT HANDLING *)
        (* Wait for operator reset sequence, handled via bEmergencyHalt re-arming *)
        IF NOT bEmergencyHalt AND bThermalInterlockOK AND NOT bEnableDeploy THEN
            iState := 0;
        END_IF;
        
END_CASE;

END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
