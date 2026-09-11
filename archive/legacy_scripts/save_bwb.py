import json, uuid, os

os.makedirs('data/swarm_raw', exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Commercial Aviation Subsonic Blended Wing Body (BWB) Fly-by-Wire**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Yaw-pitch-roll coupled elevon aerodynamic blending, span-wise gust load alleviation active fluttering, and quad-redundant hydraulic actuator voting). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_BWB_FlyByWire\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Commercial Aviation Subsonic Blended Wing Body (BWB) Fly-by-Wire

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_BWB_FlyByWire_FCS
VAR_INPUT
    (* Flight Deck Inputs *)
    rPitchCommand     : REAL; (* Commanded pitch angle from side stick (-1.0 to 1.0) *)
    rRollCommand      : REAL; (* Commanded roll angle from side stick (-1.0 to 1.0) *)
    rYawCommand       : REAL; (* Commanded yaw from rudder pedals (-1.0 to 1.0) *)
    
    (* Sensors & Inertial Reference *)
    rAirspeed         : REAL; (* Indicated Airspeed in knots *)
    rAlpha            : REAL; (* Angle of attack in radians *)
    rBeta             : REAL; (* Sideslip angle in radians *)
    
    (* Redundant Hydraulic Pressures *)
    rHydPressureA     : REAL; (* Primary hydraulic system A pressure (psi) *)
    rHydPressureB     : REAL; (* Primary hydraulic system B pressure (psi) *)
    rHydPressureC     : REAL; (* Secondary hydraulic system C pressure (psi) *)
    rHydPressureD     : REAL; (* Secondary hydraulic system D pressure (psi) *)
    
    (* Operational Modes *)
    bAutopilotEnable  : BOOL; (* Autopilot engagement status *)
    bGustAlleviation  : BOOL; (* Span-wise gust load alleviation active flag *)
END_VAR

VAR_OUTPUT
    (* Actuator Commands (Coupled Elevon Blending) *)
    rElevonLeftInb    : REAL; (* Inboard left elevon command (rad) *)
    rElevonLeftOutb   : REAL; (* Outboard left elevon command (rad) *)
    rElevonRightInb   : REAL; (* Inboard right elevon command (rad) *)
    rElevonRightOutb  : REAL; (* Outboard right elevon command (rad) *)
    rRudderCommand    : REAL; (* Rudder displacement command (rad) *)
    
    (* System Status *)
    bSystemFault      : BOOL; (* Quad-redundant hydraulic failure or actuator voter mismatch *)
    bDegradedMode     : BOOL; (* Control laws degraded to direct mode *)
END_VAR

VAR
    (* Internal state variables *)
    iFlightControlState : INT := 0;
    
    (* Gain scheduling based on airspeed and alpha *)
    rPitchGain          : REAL := 1.0;
    rRollGain           : REAL := 1.0;
    rYawGain            : REAL := 1.0;
    
    (* Gust Load Alleviation (GLA) offsets *)
    rGlaOffsetLeft      : REAL := 0.0;
    rGlaOffsetRight     : REAL := 0.0;
    
    (* Hydraulic voting flags *)
    iHydValidCount      : INT := 4;
    bHydSysAFault       : BOOL := FALSE;
    bHydSysBFault       : BOOL := FALSE;
    bHydSysCFault       : BOOL := FALSE;
    bHydSysDFault       : BOOL := FALSE;
    
    (* Constants *)
    MIN_HYD_PRESSURE    : REAL := 2500.0; (* Minimum pressure for valid voting (psi) *)
    MAX_ELEVON_DEFLECT  : REAL := 0.523;  (* Max elevon deflection (~30 degrees) *)
END_VAR

(* === MAIN LOGIC === *)

(* Step 1: Quad-Redundant Hydraulic Actuator Voting & Fault Detection *)
iHydValidCount := 0;

IF rHydPressureA > MIN_HYD_PRESSURE THEN
    bHydSysAFault := FALSE;
    iHydValidCount := iHydValidCount + 1;
ELSE
    bHydSysAFault := TRUE;
END_IF;

IF rHydPressureB > MIN_HYD_PRESSURE THEN
    bHydSysBFault := FALSE;
    iHydValidCount := iHydValidCount + 1;
ELSE
    bHydSysBFault := TRUE;
END_IF;

IF rHydPressureC > MIN_HYD_PRESSURE THEN
    bHydSysCFault := FALSE;
    iHydValidCount := iHydValidCount + 1;
ELSE
    bHydSysCFault := TRUE;
END_IF;

IF rHydPressureD > MIN_HYD_PRESSURE THEN
    bHydSysDFault := FALSE;
    iHydValidCount := iHydValidCount + 1;
ELSE
    bHydSysDFault := TRUE;
END_IF;

(* Step 2: System Health Assessment *)
IF iHydValidCount < 2 THEN
    (* Critical Failure: Less than 2 hydraulic systems available *)
    bSystemFault := TRUE;
    bDegradedMode := TRUE;
    iFlightControlState := 99; (* DIRECT MODE EMERGENCY *)
ELSIF iHydValidCount < 4 THEN
    (* Degraded Mode *)
    bSystemFault := FALSE;
    bDegradedMode := TRUE;
    iFlightControlState := 2; (* REVERSIONARY CONTROL *)
ELSE
    bSystemFault := FALSE;
    bDegradedMode := FALSE;
    iFlightControlState := 1; (* NORMAL FLY-BY-WIRE *)
END_IF;

(* Step 3: Gain Scheduling (Dynamic Pressure Compensation) *)
IF rAirspeed > 300.0 THEN
    rPitchGain := 0.3;
    rRollGain  := 0.4;
    rYawGain   := 0.2;
ELSIF rAirspeed > 150.0 THEN
    rPitchGain := 0.7;
    rRollGain  := 0.8;
    rYawGain   := 0.6;
ELSE
    rPitchGain := 1.0;
    rRollGain  := 1.0;
    rYawGain   := 1.0;
END_IF;

(* Step 4: Gust Load Alleviation (Active Flutter Suppression) *)
IF bGustAlleviation AND NOT bDegradedMode THEN
    (* Simplified span-wise aerodynamic load shedding *)
    (* Real implementation would use accelerometer derivatives *)
    rGlaOffsetLeft := rAlpha * 0.1;
    rGlaOffsetRight := rAlpha * 0.1;
ELSE
    rGlaOffsetLeft := 0.0;
    rGlaOffsetRight := 0.0;
END_IF;

(* Step 5: Coupled Control Laws & Blending *)
CASE iFlightControlState OF
    1: (* NORMAL CONTROL LAWS (FBW) *)
        (* Yaw-Pitch-Roll Coupled Blending Matrix for BWB *)
        (* Inboard elevons prioritize pitch, outboard prioritize roll/GLA *)
        
        rElevonLeftInb   := (rPitchCommand * rPitchGain) + (rRollCommand * rRollGain * 0.3);
        rElevonRightInb  := (rPitchCommand * rPitchGain) - (rRollCommand * rRollGain * 0.3);
        
        rElevonLeftOutb  := (rPitchCommand * rPitchGain * 0.4) + (rRollCommand * rRollGain) - rGlaOffsetLeft;
        rElevonRightOutb := (rPitchCommand * rPitchGain * 0.4) - (rRollCommand * rRollGain) - rGlaOffsetRight;
        
        rRudderCommand   := (rYawCommand * rYawGain) - (rRollCommand * rBeta * 0.1); (* Turn coordination *)

    2: (* REVERSIONARY MODE *)
        (* Simplified mixing, no load alleviation, reduced authority *)
        rElevonLeftInb   := rPitchCommand * 0.5 + rRollCommand * 0.5;
        rElevonRightInb  := rPitchCommand * 0.5 - rRollCommand * 0.5;
        rElevonLeftOutb  := rElevonLeftInb;
        rElevonRightOutb := rElevonRightInb;
        rRudderCommand   := rYawCommand * 0.5;

    99: (* DIRECT LAW / EMERGENCY *)
        (* Purely mechanical-equivalent direct stick-to-surface mapping *)
        rElevonLeftInb   := rPitchCommand + rRollCommand;
        rElevonRightInb  := rPitchCommand - rRollCommand;
        rElevonLeftOutb  := 0.0; (* Lock outboard surfaces to prevent structural failure without damping *)
        rElevonRightOutb := 0.0;
        rRudderCommand   := rYawCommand;
        
    ELSE
        (* Failsafe *)
        rElevonLeftInb   := 0.0;
        rElevonRightInb  := 0.0;
        rElevonLeftOutb  := 0.0;
        rElevonRightOutb := 0.0;
        rRudderCommand   := 0.0;
END_CASE;

(* Step 6: Actuator Saturation Prevention *)
IF rElevonLeftInb > MAX_ELEVON_DEFLECT THEN rElevonLeftInb := MAX_ELEVON_DEFLECT; END_IF;
IF rElevonLeftInb < -MAX_ELEVON_DEFLECT THEN rElevonLeftInb := -MAX_ELEVON_DEFLECT; END_IF;

IF rElevonRightInb > MAX_ELEVON_DEFLECT THEN rElevonRightInb := MAX_ELEVON_DEFLECT; END_IF;
IF rElevonRightInb < -MAX_ELEVON_DEFLECT THEN rElevonRightInb := -MAX_ELEVON_DEFLECT; END_IF;

IF rElevonLeftOutb > MAX_ELEVON_DEFLECT THEN rElevonLeftOutb := MAX_ELEVON_DEFLECT; END_IF;
IF rElevonLeftOutb < -MAX_ELEVON_DEFLECT THEN rElevonLeftOutb := -MAX_ELEVON_DEFLECT; END_IF;

IF rElevonRightOutb > MAX_ELEVON_DEFLECT THEN rElevonRightOutb := MAX_ELEVON_DEFLECT; END_IF;
IF rElevonRightOutb < -MAX_ELEVON_DEFLECT THEN rElevonRightOutb := -MAX_ELEVON_DEFLECT; END_IF;

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
