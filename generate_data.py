import os
import json
import uuid

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Next-Gen Commercial Aviation Autonomous Air-to-Air Refueling (A3R) Boom**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Multi-body aerodynamic wake tracking, stereoscopic machine vision drogue alignment, and high-flow (3000gpm) breakaway surge suppression). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_A3R_BoomControl\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Next-Gen Commercial Aviation Autonomous Air-to-Air Refueling (A3R) Boom

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_A3R_Boom_FlightControl
VAR_INPUT
    (* Core Enable & Safety *)
    bSystemEnable           : BOOL;     (* Overall A3R system enable *)
    bEmergencyBreakaway     : BOOL;     (* Immediate disconnect and retract signal *)
    bReceiverClearance      : BOOL;     (* Receiver aircraft has cleared the envelope *)
    
    (* Vision & Kinematics Data *)
    rReceiverDistX          : LREAL;    (* Relative X distance (forward/aft) in meters *)
    rReceiverDistY          : LREAL;    (* Relative Y distance (lateral) in meters *)
    rReceiverDistZ          : LREAL;    (* Relative Z distance (vertical) in meters *)
    rBoomAngleAzimuth       : LREAL;    (* Current boom azimuth angle in degrees *)
    rBoomAngleElevation     : LREAL;    (* Current boom elevation angle in degrees *)
    rTelescopeExtension     : LREAL;    (* Current telescope extension in meters *)
    
    (* Aerodynamic Wake Data *)
    rWakeVorticityX         : LREAL;    (* Computed wake vortex strength (X-axis) *)
    rWakeVorticityY         : LREAL;    (* Computed wake vortex strength (Y-axis) *)
    rWakeVorticityZ         : LREAL;    (* Computed wake vortex strength (Z-axis) *)
    
    (* Refueling Process Variables *)
    rFuelFlowRate           : LREAL;    (* Current fuel flow rate in GPM *)
    rFuelPressure           : LREAL;    (* Current fuel pressure at nozzle in PSI *)
END_VAR

VAR_OUTPUT
    (* Actuation Commands *)
    rCmdAzimuthRate         : LREAL;    (* Commanded azimuth rate (deg/s) *)
    rCmdElevationRate       : LREAL;    (* Commanded elevation rate (deg/s) *)
    rCmdTelescopeRate       : LREAL;    (* Commanded telescope extension rate (m/s) *)
    rCmdRuddervatorLeft     : LREAL;    (* Commanded left ruddervator deflection (deg) *)
    rCmdRuddervatorRight    : LREAL;    (* Commanded right ruddervator deflection (deg) *)
    
    (* Flow Control Commands *)
    rCmdFuelValvePos        : LREAL;    (* Commanded fuel valve position (0.0 to 1.0) *)
    bCmdPumpBypass          : BOOL;     (* Command to open high-flow surge bypass valve *)
    
    (* Status & Safety *)
    iBoomState              : INT;      (* Current state of the boom control machine *)
    bContactEstablished     : BOOL;     (* True when nozzle is locked in receptacle *)
    bTrackingErrorAlarm     : BOOL;     (* Excessive tracking error warning *)
    bSystemFault            : BOOL;     (* General fault indicator *)
END_VAR

VAR
    (* Internal State Machine Definitions *)
    STATE_INIT              : INT := 0;
    STATE_STOWED            : INT := 10;
    STATE_DEPLOYING         : INT := 20;
    STATE_TRAIL             : INT := 30;
    STATE_TRACKING          : INT := 40;
    STATE_PRE_CONTACT       : INT := 50;
    STATE_CONTACT           : INT := 60;
    STATE_REFUELING         : INT := 70;
    STATE_POST_CONTACT      : INT := 80;
    STATE_RETRACTING        : INT := 90;
    STATE_BREAKAWAY         : INT := 999;
    
    (* Control Gains - Advanced PID & LQR *)
    Kp_Azimuth              : LREAL := 2.45;
    Kd_Azimuth              : LREAL := 0.85;
    Kp_Elevation            : LREAL := 3.12;
    Kd_Elevation            : LREAL := 1.05;
    Kp_Telescope            : LREAL := 1.55;
    
    (* Internal Filters & Trackers *)
    rFilteredErrorX         : LREAL;
    rFilteredErrorY         : LREAL;
    rFilteredErrorZ         : LREAL;
    rPrevErrorX             : LREAL;
    rPrevErrorY             : LREAL;
    rPrevErrorZ             : LREAL;
    
    (* Wake Compensation Variables *)
    rWakeCompAzimuth        : LREAL;
    rWakeCompElevation      : LREAL;
    
    (* Timers & Counters *)
    tBreakawayTimer         : TON;
    tTrackingStableTimer    : TON;
    tSurgeSuppressionTimer  : TON;
    
    (* Constant Constraints *)
    MAX_AZIMUTH_RATE        : LREAL := 15.0;
    MAX_ELEVATION_RATE      : LREAL := 10.0;
    MAX_TELESCOPE_RATE      : LREAL := 2.5;
    MAX_RUDDERVATOR_DEFLECT : LREAL := 30.0;
    MAX_TRACKING_ERROR      : LREAL := 0.5; (* meters *)
    SURGE_PRESSURE_LIMIT    : LREAL := 120.0; (* PSI *)
END_VAR

(* === MAIN LOGIC === *)

(* Global Safety Interlock: Emergency Breakaway *)
IF bEmergencyBreakaway THEN
    iBoomState := STATE_BREAKAWAY;
END_IF;

(* Surge Suppression Logic - Runs unconditionally for safety *)
IF rFuelPressure > SURGE_PRESSURE_LIMIT AND iBoomState = STATE_REFUELING THEN
    bCmdPumpBypass := TRUE;
    rCmdFuelValvePos := 0.0;
    tSurgeSuppressionTimer(IN:=TRUE, PT:=T#2S);
ELSE
    tSurgeSuppressionTimer(IN:=FALSE);
    IF tSurgeSuppressionTimer.Q THEN
        bCmdPumpBypass := FALSE;
    END_IF;
END_IF;

CASE iBoomState OF

    0: (* STATE_INIT *)
        bSystemFault := FALSE;
        bTrackingErrorAlarm := FALSE;
        bContactEstablished := FALSE;
        rCmdFuelValvePos := 0.0;
        bCmdPumpBypass := FALSE;
        IF bSystemEnable THEN
            iBoomState := STATE_STOWED;
        END_IF;

    10: (* STATE_STOWED *)
        rCmdAzimuthRate := 0.0;
        rCmdElevationRate := 0.0;
        rCmdTelescopeRate := 0.0;
        rCmdRuddervatorLeft := 0.0;
        rCmdRuddervatorRight := 0.0;
        IF bSystemEnable AND NOT bEmergencyBreakaway THEN
            iBoomState := STATE_DEPLOYING;
        END_IF;

    20: (* STATE_DEPLOYING *)
        (* Command ruddervators to deploy boom to trail position *)
        rCmdElevationRate := -5.0; (* Lowering boom *)
        IF rBoomAngleElevation <= -30.0 THEN
            rCmdElevationRate := 0.0;
            iBoomState := STATE_TRAIL;
        END_IF;

    30: (* STATE_TRAIL *)
        (* Boom in trail, waiting for receiver aircraft to enter tracking envelope *)
        IF rReceiverDistZ < 20.0 AND rReceiverDistX < 30.0 THEN
            iBoomState := STATE_TRACKING;
        END_IF;
        IF NOT bSystemEnable THEN
            iBoomState := STATE_RETRACTING;
        END_IF;

    40: (* STATE_TRACKING *)
        (* Advanced multi-body aerodynamic wake tracking and stereoscopic alignment *)
        
        (* Calculate raw positional errors *)
        rFilteredErrorX := rFilteredErrorX * 0.8 + rReceiverDistX * 0.2;
        rFilteredErrorY := rFilteredErrorY * 0.8 + rReceiverDistY * 0.2;
        rFilteredErrorZ := rFilteredErrorZ * 0.8 + rReceiverDistZ * 0.2;
        
        (* Aerodynamic Wake Compensation Matrix *)
        (* Compensate for vortices generated by receiver's bow wave *)
        rWakeCompAzimuth := rWakeVorticityZ * 0.05 + rWakeVorticityY * 0.01;
        rWakeCompElevation := rWakeVorticityX * 0.04 - rWakeVorticityY * 0.02;
        
        (* PD Control for Ruddervator deflection (Azimuth / Elevation) *)
        rCmdAzimuthRate := (Kp_Azimuth * rFilteredErrorY) + (Kd_Azimuth * (rFilteredErrorY - rPrevErrorY)) + rWakeCompAzimuth;
        rCmdElevationRate := (Kp_Elevation * rFilteredErrorZ) + (Kd_Elevation * (rFilteredErrorZ - rPrevErrorZ)) + rWakeCompElevation;
        
        (* Rate Limiting *)
        IF rCmdAzimuthRate > MAX_AZIMUTH_RATE THEN rCmdAzimuthRate := MAX_AZIMUTH_RATE; END_IF;
        IF rCmdAzimuthRate < -MAX_AZIMUTH_RATE THEN rCmdAzimuthRate := -MAX_AZIMUTH_RATE; END_IF;
        IF rCmdElevationRate > MAX_ELEVATION_RATE THEN rCmdElevationRate := MAX_ELEVATION_RATE; END_IF;
        IF rCmdElevationRate < -MAX_ELEVATION_RATE THEN rCmdElevationRate := -MAX_ELEVATION_RATE; END_IF;
        
        (* Map aerodynamic control surfaces *)
        rCmdRuddervatorLeft := (rCmdElevationRate * 0.7) - (rCmdAzimuthRate * 0.7);
        rCmdRuddervatorRight := (rCmdElevationRate * 0.7) + (rCmdAzimuthRate * 0.7);
        
        (* Tracking error monitor *)
        IF ABS(rFilteredErrorY) > MAX_TRACKING_ERROR OR ABS(rFilteredErrorZ) > MAX_TRACKING_ERROR THEN
            tTrackingStableTimer(IN:=FALSE);
            bTrackingErrorAlarm := TRUE;
        ELSE
            bTrackingErrorAlarm := FALSE;
            tTrackingStableTimer(IN:=TRUE, PT:=T#3S);
            IF tTrackingStableTimer.Q THEN
                iBoomState := STATE_PRE_CONTACT;
            END_IF;
        END_IF;
        
        (* Store previous errors *)
        rPrevErrorX := rFilteredErrorX;
        rPrevErrorY := rFilteredErrorY;
        rPrevErrorZ := rFilteredErrorZ;

    50: (* STATE_PRE_CONTACT *)
        (* Extend telescope to insert nozzle into receiver receptacle *)
        rCmdTelescopeRate := MAX_TELESCOPE_RATE;
        IF rTelescopeExtension >= (rReceiverDistX - 0.1) THEN (* Within 10cm *)
            rCmdTelescopeRate := 0.0;
            iBoomState := STATE_CONTACT;
        END_IF;
        IF bTrackingErrorAlarm THEN
            (* Revert to tracking if stability lost *)
            rCmdTelescopeRate := -MAX_TELESCOPE_RATE;
            iBoomState := STATE_TRACKING;
        END_IF;

    60: (* STATE_CONTACT *)
        bContactEstablished := TRUE;
        (* In contact mode, mechanical lock handles tension; control surfaces enter damping mode *)
        rCmdRuddervatorLeft := rCmdRuddervatorLeft * 0.1;
        rCmdRuddervatorRight := rCmdRuddervatorRight * 0.1;
        
        (* Wait for flow sequence command from operator or auto-sequence *)
        IF bSystemEnable AND NOT bSystemFault THEN
            iBoomState := STATE_REFUELING;
        END_IF;

    70: (* STATE_REFUELING *)
        (* Ramp up fuel flow while monitoring pressure *)
        IF rCmdFuelValvePos < 1.0 THEN
            rCmdFuelValvePos := rCmdFuelValvePos + 0.05; (* Ramp open *)
        END_IF;
        
        (* If receiver signals full or breakaway commanded *)
        IF NOT bSystemEnable THEN
            rCmdFuelValvePos := 0.0;
            iBoomState := STATE_POST_CONTACT;
        END_IF;

    80: (* STATE_POST_CONTACT *)
        bContactEstablished := FALSE;
        rCmdFuelValvePos := 0.0;
        (* Retract telescope *)
        rCmdTelescopeRate := -MAX_TELESCOPE_RATE;
        IF rTelescopeExtension <= 0.1 THEN
            rCmdTelescopeRate := 0.0;
            iBoomState := STATE_TRAIL;
        END_IF;

    90: (* STATE_RETRACTING *)
        rCmdElevationRate := 5.0; (* Raise boom *)
        rCmdTelescopeRate := -MAX_TELESCOPE_RATE; (* Fully retract *)
        IF rBoomAngleElevation >= 0.0 AND rTelescopeExtension <= 0.1 THEN
            rCmdElevationRate := 0.0;
            rCmdTelescopeRate := 0.0;
            iBoomState := STATE_STOWED;
        END_IF;

    999: (* STATE_BREAKAWAY *)
        (* High-speed emergency retraction and pressure surge relief *)
        bContactEstablished := FALSE;
        rCmdFuelValvePos := 0.0;
        bCmdPumpBypass := TRUE; (* Dump pressure immediately *)
        
        (* Max aerodynamic lift to clear receiver *)
        rCmdRuddervatorLeft := MAX_RUDDERVATOR_DEFLECT;
        rCmdRuddervatorRight := MAX_RUDDERVATOR_DEFLECT;
        
        (* Max retract speed *)
        rCmdTelescopeRate := -MAX_TELESCOPE_RATE * 1.5; 
        
        tBreakawayTimer(IN:=TRUE, PT:=T#10S);
        IF bReceiverClearance OR tBreakawayTimer.Q THEN
            tBreakawayTimer(IN:=FALSE);
            bCmdPumpBypass := FALSE;
            iBoomState := STATE_RETRACTING;
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
