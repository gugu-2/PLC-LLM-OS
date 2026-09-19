import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Automated Submarine Cable Laying Vessel Dynamic Positioning and Cable Tension Payout**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_SubmarineCable_Payout\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Automated Submarine Cable Laying Vessel Dynamic Positioning and Cable Tension Payout

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_CableLayVessel_DP_TensionControl
(* 
   =============================================================================
   Block Name    : FB_CableLayVessel_DP_TensionControl
   Description   : Advanced coordinated controller for submarine cable payout 
                   tension and vessel Dynamic Positioning (DP). Includes noise
                   filtering, surge suppression, catenary calculation, PID 
                   regulation of tension, and fault management.
   Version       : 4.1.2
   =============================================================================
*)
VAR_INPUT
    bSystemEnable       : BOOL;     (* Main enable signal for tension control *)
    bEmergencyStop      : BOOL;     (* Active HIGH safety stop loop OK signal *)
    rVesselSpeedKnots   : REAL;     (* Current vessel speed over ground (SOG) in knots *)
    rWaterDepthMeters   : REAL;     (* Measured water depth at laying position (m) *)
    rTargetTensionKN    : REAL;     (* Setpoint for cable tension (kiloNewtons) *)
    rMeasuredTensionKN  : REAL;     (* Feedback from load cell / tensioner (kN) *)
    rCablePayoutSpeed   : REAL;     (* Current linear payout speed of cable (m/s) *)
    rHeaveCompMeters    : REAL;     (* Active heave compensation offset (m) *)
END_VAR

VAR_OUTPUT
    bSystemReady        : BOOL;     (* Indicates system is initialized and ready to run *)
    rTensionerCmdRPM    : REAL;     (* Output speed command to main tensioner drives (RPM) *)
    rDPOffsetCmdMeters  : REAL;     (* Requested DP position offset to maintain catenary (m) *)
    bPayoutFaultAlarm   : BOOL;     (* Critical fault requiring immediate action *)
    bWarningAlarm       : BOOL;     (* Warning - tension deviation or sensor noise *)
    iOperatingState     : INT;      (* Current state machine state (0=IDLE, 1=RUN, etc.) *)
END_VAR

VAR
    (* Internal State and Filters *)
    iState              : INT := 0;
    rFilteredTension    : REAL := 0.0;
    rFilterAlpha        : REAL := 0.15; (* Exponential moving average factor *)
    
    (* PID Variables *)
    rError              : REAL := 0.0;
    rIntegral           : REAL := 0.0;
    rDerivative         : REAL := 0.0;
    rLastError          : REAL := 0.0;
    rKp                 : REAL := 1.25;
    rKi                 : REAL := 0.05;
    rKd                 : REAL := 0.35;
    
    (* Limits *)
    rMaxTensionCmd      : REAL := 1500.0; (* RPM *)
    rMaxIntegral        : REAL := 500.0;
    
    (* Timers *)
    tFaultDelay         : TON;
    tStartupDelay       : TON;
    
    (* Catenary Math *)
    rCatenaryWeightFactor : REAL := 0.085; (* kN/m in water *)
    rEstimatedTension   : REAL;
END_VAR

(* === MAIN LOGIC === *)

(* Safety Interlock Check *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bPayoutFaultAlarm := TRUE;
    rTensionerCmdRPM := 0.0;
    rDPOffsetCmdMeters := 0.0;
    iState := 99; (* FAULT STATE *)
    iOperatingState := iState;
    RETURN;
END_IF;

(* Input Signal Noise Filtering (EMA) *)
rFilteredTension := (rFilterAlpha * rMeasuredTensionKN) + ((1.0 - rFilterAlpha) * rFilteredTension);

(* Theoretical Catenary Tension Estimation (simplified for baseline check) *)
rEstimatedTension := rWaterDepthMeters * rCatenaryWeightFactor;

(* State Machine *)
CASE iState OF
    0: (* IDLE & INITIALIZATION *)
        bSystemReady := TRUE;
        bPayoutFaultAlarm := FALSE;
        bWarningAlarm := FALSE;
        rTensionerCmdRPM := 0.0;
        rDPOffsetCmdMeters := 0.0;
        rIntegral := 0.0;
        
        IF bSystemEnable AND (rTargetTensionKN > 10.0) THEN
            tStartupDelay(IN := TRUE, PT := T#2S);
            IF tStartupDelay.Q THEN
                tStartupDelay(IN := FALSE);
                iState := 10; (* TRANSITION TO PRE-TENSION *)
            END_IF;
        ELSE
            tStartupDelay(IN := FALSE);
        END_IF;

    10: (* PRE-TENSION / RAMP UP *)
        bSystemReady := TRUE;
        rError := rTargetTensionKN - rFilteredTension;
        
        (* Gentle proportional control for pre-tension *)
        rTensionerCmdRPM := rError * (rKp * 0.5); 
        
        IF ABS(rError) < (rTargetTensionKN * 0.1) THEN
            iState := 20; (* RUNNING - ACTIVE PAYOUT *)
        END_IF;
        
        IF NOT bSystemEnable THEN
            iState := 0;
        END_IF;

    20: (* RUNNING - ACTIVE PAYOUT *)
        (* PID Computation *)
        rError := rTargetTensionKN - rFilteredTension;
        
        rIntegral := rIntegral + (rError * rKi);
        IF rIntegral > rMaxIntegral THEN
            rIntegral := rMaxIntegral;
        ELSIF rIntegral < -rMaxIntegral THEN
            rIntegral := -rMaxIntegral;
        END_IF;
        
        rDerivative := (rError - rLastError) * rKd;
        rLastError := rError;
        
        rTensionerCmdRPM := (rError * rKp) + rIntegral + rDerivative;
        
        (* Limit output *)
        IF rTensionerCmdRPM > rMaxTensionCmd THEN
            rTensionerCmdRPM := rMaxTensionCmd;
        ELSIF rTensionerCmdRPM < -100.0 THEN
            rTensionerCmdRPM := -100.0; (* Allow slight reverse for recovery *)
        END_IF;
        
        (* DP Integration: If tension deviates significantly, ask DP to adjust vessel position *)
        IF rError > (rTargetTensionKN * 0.2) THEN
            rDPOffsetCmdMeters := -0.5; (* Ask DP to fall back slightly *)
            bWarningAlarm := TRUE;
        ELSIF rError < -(rTargetTensionKN * 0.2) THEN
            rDPOffsetCmdMeters := 0.5; (* Ask DP to push forward *)
            bWarningAlarm := TRUE;
        ELSE
            rDPOffsetCmdMeters := 0.0;
            bWarningAlarm := FALSE;
        END_IF;
        
        (* Heave Compensation Trim (Feed-forward) *)
        rTensionerCmdRPM := rTensionerCmdRPM + (rHeaveCompMeters * 2.0);
        
        (* Fault Detection *)
        tFaultDelay(IN := (ABS(rError) > (rTargetTensionKN * 0.5)), PT := T#3S);
        IF tFaultDelay.Q THEN
            iState := 99; (* FAULT STATE *)
        END_IF;
        
        IF NOT bSystemEnable THEN
            iState := 0;
        END_IF;

    99: (* FAULT / ERROR STATE *)
        bPayoutFaultAlarm := TRUE;
        bSystemReady := FALSE;
        rTensionerCmdRPM := 0.0;
        rDPOffsetCmdMeters := 0.0;
        
        IF NOT bSystemEnable AND NOT bEmergencyStop THEN
            (* Require operator reset via disable and physical safety reset *)
            iState := 0;
        END_IF;
        
END_CASE;

iOperatingState := iState;

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
