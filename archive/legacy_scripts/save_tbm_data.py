import json, uuid
import os

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Automated Heavy-Duty Tunnel Boring Machine (TBM) Slurry Shield**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Bentonite slurry density/pressure dynamic matching, multi-axis cutterhead torque-vectoring in mixed-face conditions, and ring-building erector arm 6-DOF kinematics). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_SlurryTBM\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Automated Heavy-Duty Tunnel Boring Machine (TBM) Slurry Shield

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_TBM_SlurryShield_Controller
VAR_INPUT
    (* Core Enable and Safety Interlocks *)
    bSystemEnable           : BOOL;     (* Main system enable command for TBM operations *)
    bEmergencyStopOk        : BOOL;     (* Safety relay loop feedback - MUST be TRUE to operate *)
    bMixedFaceCondition     : BOOL;     (* Sensor detection of mixed rock/soil face geology *)
    
    (* Slurry Circuit Telemetry *)
    rBentoniteInletPress    : REAL;     (* Measured inlet pressure of bentonite slurry (bar) *)
    rBentoniteDensity       : REAL;     (* Measured density of bentonite slurry (kg/m^3) *)
    rExcavationChamberPress : REAL;     (* Dynamic pressure inside the excavation chamber (bar) *)
    
    (* Cutterhead & Drive Telemetry *)
    rCutterheadTorqueAvg    : REAL;     (* Average torque load on the cutterhead motors (kNm) *)
    rAdvanceSpeedTarget     : REAL;     (* Operator or navigation setpoint for advance speed (mm/min) *)
END_VAR
VAR_OUTPUT
    (* Operational Status Outputs *)
    bSystemReady            : BOOL;     (* System fully initialized and ready for automated sequence *)
    bCriticalAlarm          : BOOL;     (* Latched critical fault output requiring operator intervention *)
    
    (* Active Control Commands *)
    rSlurryPumpSpeedCmd     : REAL;     (* Speed command for the main slurry feed pump (%) *)
    rThrustJackForceCmd     : REAL;     (* Calculated thrust cylinder force setpoint (kN) *)
    rCutterheadSpeedCmd     : REAL;     (* Dynamically calculated cutterhead speed setpoint (RPM) *)
    iOperatingState         : INT;      (* Current internal state of the automation state machine *)
END_VAR
VAR
    (* Internal State and Timers *)
    iState                  : INT := 0; (* Internal state machine tracker *)
    tStartupDelay           : TON;      (* Delay timer for hydraulic system pressure buildup *)
    tStallMonitor           : TON;      (* Monitor for cutterhead stall condition during heavy load *)
    
    (* Advanced Control Variables *)
    rPressureError          : REAL := 0.0;
    rTorqueDeviation        : REAL := 0.0;
    rTargetChamberPress     : REAL := 3.5; (* Nominal target pressure (bar) *)
    rKp_Pressure            : REAL := 2.5; (* Proportional gain for slurry pressure control *)
    rKi_Pressure            : REAL := 0.8; (* Integral gain for slurry pressure control *)
    rIntegralAccum          : REAL := 0.0;
    
    (* Constants *)
    c_MAX_PUMP_SPEED        : REAL := 100.0;
    c_MAX_THRUST_FORCE      : REAL := 12000.0;
    c_MAX_CUTTER_SPEED      : REAL := 5.0;
END_VAR

(* === MAIN LOGIC === *)
(* 1. Safety and Watchdog Layer *)
IF NOT bEmergencyStopOk THEN
    bSystemReady := FALSE;
    bCriticalAlarm := TRUE;
    rSlurryPumpSpeedCmd := 0.0;
    rThrustJackForceCmd := 0.0;
    rCutterheadSpeedCmd := 0.0;
    iState := 999; (* Transition to FAULT state *)
    RETURN;
END_IF;

(* 2. Main State Machine for TBM Slurry Shield Operation *)
CASE iState OF
    0: (* STATE 0: IDLE AND INITIALIZATION *)
        bSystemReady := FALSE;
        bCriticalAlarm := FALSE;
        rSlurryPumpSpeedCmd := 0.0;
        rThrustJackForceCmd := 0.0;
        rCutterheadSpeedCmd := 0.0;
        rIntegralAccum := 0.0;
        iOperatingState := 0;
        
        IF bSystemEnable THEN
            tStartupDelay(IN := TRUE, PT := T#3S);
            IF tStartupDelay.Q THEN
                tStartupDelay(IN := FALSE);
                bSystemReady := TRUE;
                iState := 10;
            END_IF;
        ELSE
            tStartupDelay(IN := FALSE);
        END_IF;

    10: (* STATE 10: PRE-CONDITIONING AND SLURRY CIRCUIT STARTUP *)
        iOperatingState := 10;
        
        (* Ramp up slurry pump to establish base pressure *)
        IF rSlurryPumpSpeedCmd < 40.0 THEN
            rSlurryPumpSpeedCmd := rSlurryPumpSpeedCmd + 0.5;
        ELSE
            (* Check if chamber pressure is within acceptable start tolerance *)
            IF rExcavationChamberPress >= (rTargetChamberPress * 0.8) THEN
                iState := 20;
            END_IF;
        END_IF;
        
        IF NOT bSystemEnable THEN
            iState := 0;
        END_IF;

    20: (* STATE 20: ACTIVE EXCAVATION AND DYNAMIC PRESSURE MATCHING *)
        iOperatingState := 20;
        
        (* PI Control for Excavation Chamber Pressure using Slurry Pump Speed *)
        rPressureError := rTargetChamberPress - rExcavationChamberPress;
        rIntegralAccum := rIntegralAccum + (rPressureError * 0.1); (* Assuming 100ms task cycle *)
        
        (* Anti-windup for integral accumulator *)
        IF rIntegralAccum > 20.0 THEN rIntegralAccum := 20.0; END_IF;
        IF rIntegralAccum < -20.0 THEN rIntegralAccum := -20.0; END_IF;
        
        rSlurryPumpSpeedCmd := 40.0 + (rPressureError * rKp_Pressure) + (rIntegralAccum * rKi_Pressure);
        
        (* Clamp pump speed limits *)
        IF rSlurryPumpSpeedCmd > c_MAX_PUMP_SPEED THEN rSlurryPumpSpeedCmd := c_MAX_PUMP_SPEED; END_IF;
        IF rSlurryPumpSpeedCmd < 20.0 THEN rSlurryPumpSpeedCmd := 20.0; END_IF;
        
        (* Torque Vectoring and Advance Rate Control *)
        IF bMixedFaceCondition THEN
            (* Mixed face: lower RPM, higher torque margin, careful advance *)
            rCutterheadSpeedCmd := c_MAX_CUTTER_SPEED * 0.4; 
            rThrustJackForceCmd := c_MAX_THRUST_FORCE * 0.6;
        ELSE
            (* Homogeneous face: optimize for target advance speed *)
            rCutterheadSpeedCmd := c_MAX_CUTTER_SPEED * 0.8;
            rThrustJackForceCmd := (rAdvanceSpeedTarget / 100.0) * c_MAX_THRUST_FORCE;
        END_IF;
        
        (* Thrust force clamping *)
        IF rThrustJackForceCmd > c_MAX_THRUST_FORCE THEN rThrustJackForceCmd := c_MAX_THRUST_FORCE; END_IF;
        
        (* Stall Detection *)
        IF rCutterheadTorqueAvg > 8000.0 THEN (* Threshold for stall *)
            tStallMonitor(IN := TRUE, PT := T#2S);
            IF tStallMonitor.Q THEN
                iState := 30; (* Overload recovery state *)
            END_IF;
        ELSE
            tStallMonitor(IN := FALSE);
        END_IF;
        
        IF NOT bSystemEnable THEN
            iState := 0;
        END_IF;
        
    30: (* STATE 30: OVERLOAD RECOVERY *)
        iOperatingState := 30;
        tStallMonitor(IN := FALSE);
        
        (* Stop advance, maintain pressure, clear the face *)
        rThrustJackForceCmd := 0.0;
        rCutterheadSpeedCmd := c_MAX_CUTTER_SPEED * 0.2; (* Slow rotation to clear muck *)
        
        IF rCutterheadTorqueAvg < 3000.0 THEN
            (* Torque normalized, resume excavation *)
            iState := 20;
        END_IF;
        
    999: (* STATE 999: CRITICAL FAULT LATCH *)
        iOperatingState := 999;
        bSystemReady := FALSE;
        rSlurryPumpSpeedCmd := 0.0;
        rThrustJackForceCmd := 0.0;
        rCutterheadSpeedCmd := 0.0;
        
        (* Requires E-Stop reset and manual intervention to clear *)
        IF bEmergencyStopOk AND NOT bSystemEnable THEN
            iState := 0;
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
