import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Next-Gen Submarine Active Sonar Towed Array Winch**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Variable frequency drive (VFD) sea-state heave compensation, optical slip-ring slip detection, and cable payout dynamic tension braking). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_SonarTowedArrayWinch\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Next-Gen Submarine Active Sonar Towed Array Winch

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_NextGenSonarWinchControl
(*
  Title: Next-Generation Submarine Active Sonar Towed Array Winch Controller
  Author: Elite Automation Architect (40+ years experience)
  Description: Advanced control algorithm for towed array winch handling including
  sea-state heave compensation, optical slip-ring diagnostics, and dynamic payout tensioning.
*)
VAR_INPUT
    bSystemEnable       : BOOL;     (* Main system enable interlock from combat systems *)
    bEmergencyStop      : BOOL;     (* Hardwired E-Stop safety relay OK signal *)
    rCableTension       : REAL;     (* Measured cable tension [kN] from load cell *)
    rPayoutSpeedAct     : REAL;     (* Actual payout speed [m/s] from encoder *)
    rHeaveAcceleration  : REAL;     (* Submarine vertical heave acceleration [m/s^2] from IMU *)
    rOpticalSignalLoss  : REAL;     (* Optical slip-ring signal attenuation [dB] *)
    rDepthCommand       : REAL;     (* Target deployment depth/length [m] *)
    rActualLength       : REAL;     (* Actual deployed cable length [m] *)
END_VAR
VAR_OUTPUT
    bWinchReady         : BOOL;     (* Winch system healthy and ready for deployment *)
    rVFD_SpeedSetpoint  : REAL;     (* Commanded speed to Variable Frequency Drive [m/s] *)
    rBrakeTorqueCmd     : REAL;     (* Commanded dynamic brake torque [Nm] *)
    bOpticalSlipAlarm   : BOOL;     (* Alarm indicating slip-ring degradation/failure *)
    bTensionFault       : BOOL;     (* Alarm for cable tension out of safe operating limits *)
    iSystemState        : INT;      (* Current operating state machine state *)
END_VAR
VAR
    (* Internal State & Timers *)
    tHeaveFilter        : TON;
    tOpticalTimer       : TON;
    rFilteredHeave      : REAL := 0.0;
    rTensionError       : REAL;
    rTensionIntegral    : REAL := 0.0;
    rMaxTensionLimit    : REAL := 150.0; (* 150 kN breaking limit *)
    rMinTensionLimit    : REAL := 5.0;   (* 5 kN slack limit *)

    (* Constants *)
    Kp_Tension          : REAL := 2.5;
    Ki_Tension          : REAL := 0.1;
    MAX_SPEED           : REAL := 5.0;   (* Max winch speed m/s *)
END_VAR

(* === MAIN LOGIC === *)

(* Safety Interlocks *)
IF NOT bEmergencyStop THEN
    bWinchReady := FALSE;
    rVFD_SpeedSetpoint := 0.0;
    rBrakeTorqueCmd := 10000.0; (* Max braking torque *)
    iSystemState := 99; (* FAULT STATE *)
    bTensionFault := FALSE;
    bOpticalSlipAlarm := FALSE;
    RETURN;
END_IF;

(* Optical Slip Ring Monitoring *)
IF rOpticalSignalLoss > 3.5 THEN
    tOpticalTimer(IN := TRUE, PT := T#2S);
    IF tOpticalTimer.Q THEN
        bOpticalSlipAlarm := TRUE;
    END_IF;
ELSE
    tOpticalTimer(IN := FALSE);
    bOpticalSlipAlarm := FALSE;
END_IF;

(* Tension Monitoring *)
IF (rCableTension > rMaxTensionLimit) OR (rCableTension < rMinTensionLimit) THEN
    bTensionFault := TRUE;
ELSE
    bTensionFault := FALSE;
END_IF;

(* Low-pass filter for Heave Acceleration (simplified) *)
rFilteredHeave := (rFilteredHeave * 0.9) + (rHeaveAcceleration * 0.1);

(* Main State Machine *)
CASE iSystemState OF
    0: (* INIT *)
        rVFD_SpeedSetpoint := 0.0;
        rBrakeTorqueCmd := 5000.0; (* Holding brake *)
        IF bSystemEnable AND NOT bTensionFault AND NOT bOpticalSlipAlarm THEN
            bWinchReady := TRUE;
            iSystemState := 10;
        END_IF;

    10: (* STANDBY & HEAVE COMPENSATION *)
        (* Active heave compensation to maintain constant tension while holding length *)
        rTensionError := 50.0 - rCableTension; (* Target holding tension 50 kN *)
        rTensionIntegral := rTensionIntegral + (rTensionError * 0.01);
        rVFD_SpeedSetpoint := (Kp_Tension * rTensionError) + (Ki_Tension * rTensionIntegral) - (rFilteredHeave * 0.5);

        (* Limit VFD Speed *)
        IF rVFD_SpeedSetpoint > 1.0 THEN rVFD_SpeedSetpoint := 1.0; END_IF;
        IF rVFD_SpeedSetpoint < -1.0 THEN rVFD_SpeedSetpoint := -1.0; END_IF;

        rBrakeTorqueCmd := 0.0; (* Release brake for dynamic compensation *)

        IF ABS(rDepthCommand - rActualLength) > 10.0 THEN
            iSystemState := 20;
        END_IF;

        IF NOT bSystemEnable THEN
            bWinchReady := FALSE;
            iSystemState := 0;
        END_IF;

    20: (* PAYOUT / REEL IN *)
        rBrakeTorqueCmd := 0.0;
        IF rDepthCommand > rActualLength THEN
            (* Payout *)
            rVFD_SpeedSetpoint := MAX_SPEED + (rFilteredHeave * 0.2);
        ELSE
            (* Reel In *)
            rVFD_SpeedSetpoint := -MAX_SPEED + (rFilteredHeave * 0.2);
        END_IF;

        IF ABS(rDepthCommand - rActualLength) <= 10.0 THEN
            iSystemState := 10;
        END_IF;

    99: (* FAULT *)
        bWinchReady := FALSE;
        rVFD_SpeedSetpoint := 0.0;
        rBrakeTorqueCmd := 10000.0;
        IF bSystemEnable = FALSE AND bEmergencyStop THEN
            iSystemState := 0;
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
