import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Automated Tire Manufacturing Tread Extrusion and Calendering Synchronization**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_Tire_TreadExtrusion\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Automated Tire Manufacturing Tread Extrusion and Calendering Synchronization

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_Tire_TreadExtrusion_Sync
VAR_INPUT
    bEnable                 : BOOL;     (* System master enable signal *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal (Active HIGH) *)
    rExtruderPressure       : REAL;     (* Melt pressure at extruder head [Bar] *)
    rExtruderTempZ1         : REAL;     (* Extruder zone 1 temperature [DegC] *)
    rExtruderTempZ2         : REAL;     (* Extruder zone 2 temperature [DegC] *)
    rCalenderSpeedMaster    : REAL;     (* Master line speed reference from calender [m/min] *)
    rTreadThicknessRef      : REAL;     (* Target tread thickness setpoint [mm] *)
    rTreadThicknessAct      : REAL;     (* Actual measured tread thickness via laser [mm] *)
    rTensionLoadCell        : REAL;     (* Measured web tension between extruder and calender [N] *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;     (* System is ready for production *)
    rExtruderSpeedCmd       : REAL;     (* Extruder screw speed command to drive [RPM] *)
    rTakeawayConveyorSpeed  : REAL;     (* Takeaway conveyor speed command [m/min] *)
    rCoolingWaterValveCmd   : REAL;     (* Cooling water valve position command [0-100%] *)
    bAlarmThicknessLimit    : BOOL;     (* Tread thickness out of tolerance alarm *)
    bAlarmTensionLimit      : BOOL;     (* Web tension out of tolerance alarm *)
    bAlarmThermal           : BOOL;     (* Thermal zone out of limits alarm *)
END_VAR
VAR
    iState                  : INT := 0; (* Internal state machine state *)
    tStartupDelay           : TON;      (* Delay timer for startup sequence *)
    tStabilizationTimer     : TON;      (* Timer to wait for thermal stabilization *)
    
    (* Filter variables *)
    rFilteredThickness      : REAL := 0.0;
    rFilteredTension        : REAL := 0.0;
    
    (* PID Controller for Tension *)
    rTensionSetpoint        : REAL := 150.0; (* N *)
    rTensionKp              : REAL := 0.5;
    rTensionKi              : REAL := 0.1;
    rTensionError           : REAL := 0.0;
    rTensionIntegral        : REAL := 0.0;
    
    (* Constants *)
    rALPHA                  : REAL := 0.1; (* Low pass filter coefficient *)
END_VAR

(* === MAIN LOGIC === *)
(* 1. Safety and Interlocks *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    rExtruderSpeedCmd := 0.0;
    rTakeawayConveyorSpeed := 0.0;
    rCoolingWaterValveCmd := 0.0;
    bAlarmThicknessLimit := FALSE;
    bAlarmTensionLimit := FALSE;
    bAlarmThermal := FALSE;
    iState := 0;
    RETURN;
END_IF;

(* 2. Signal Filtering (Exponential Moving Average) *)
rFilteredThickness := (rALPHA * rTreadThicknessAct) + ((1.0 - rALPHA) * rFilteredThickness);
rFilteredTension := (rALPHA * rTensionLoadCell) + ((1.0 - rALPHA) * rFilteredTension);

(* 3. Alarm Checks *)
IF (rFilteredThickness > rTreadThicknessRef * 1.1) OR (rFilteredThickness < rTreadThicknessRef * 0.9) THEN
    bAlarmThicknessLimit := TRUE;
ELSE
    bAlarmThicknessLimit := FALSE;
END_IF;

IF (rFilteredTension > 300.0) OR (rFilteredTension < 50.0) THEN
    bAlarmTensionLimit := TRUE;
ELSE
    bAlarmTensionLimit := FALSE;
END_IF;

IF (rExtruderTempZ1 > 150.0) OR (rExtruderTempZ2 > 160.0) THEN
    bAlarmThermal := TRUE;
ELSE
    bAlarmThermal := FALSE;
END_IF;

(* 4. State Machine Control *)
CASE iState OF
    0: (* IDLE - Wait for Enable *)
        bSystemReady := FALSE;
        rExtruderSpeedCmd := 0.0;
        rTakeawayConveyorSpeed := 0.0;
        rCoolingWaterValveCmd := 0.0;
        
        IF bEnable AND NOT bAlarmThermal THEN
            iState := 10;
        END_IF;

    10: (* HEATING STABILIZATION *)
        rCoolingWaterValveCmd := 50.0; (* Standby cooling *)
        tStabilizationTimer(IN := TRUE, PT := T#30S);
        
        IF tStabilizationTimer.Q THEN
            tStabilizationTimer(IN := FALSE);
            iState := 20;
        END_IF;

    20: (* RAMP UP *)
        bSystemReady := TRUE;
        rExtruderSpeedCmd := rExtruderSpeedCmd + 0.1; (* Ramp up extruder speed *)
        rTakeawayConveyorSpeed := rCalenderSpeedMaster * 0.8; (* Start takeaway conveyor slightly slower *)
        
        IF rExtruderSpeedCmd >= 50.0 THEN (* Target initial speed *)
            iState := 30;
        END_IF;
        
        IF NOT bEnable THEN
            iState := 0;
        END_IF;

    30: (* SYNCHRONIZED RUNNING *)
        (* Tension PID Control modifying takeaway speed *)
        rTensionError := rTensionSetpoint - rFilteredTension;
        rTensionIntegral := rTensionIntegral + rTensionError * 0.1; (* dt approx 0.1s *)
        
        (* Anti-windup *)
        IF rTensionIntegral > 50.0 THEN
            rTensionIntegral := 50.0;
        ELSIF rTensionIntegral < -50.0 THEN
            rTensionIntegral := -50.0;
        END_IF;
        
        (* Calculate Conveyor speed command based on master speed and tension correction *)
        rTakeawayConveyorSpeed := rCalenderSpeedMaster + (rTensionError * rTensionKp) + (rTensionIntegral * rTensionKi);
        
        (* Feed-forward Extruder Control based on target thickness and master line speed *)
        rExtruderSpeedCmd := (rCalenderSpeedMaster * rTreadThicknessRef) * 2.5; (* Calibration factor 2.5 *)
        
        (* Cooling control based on extruder temp *)
        IF rExtruderTempZ1 > 120.0 THEN
            rCoolingWaterValveCmd := 100.0;
        ELSE
            rCoolingWaterValveCmd := 20.0;
        END_IF;
        
        IF NOT bEnable OR bAlarmTensionLimit THEN
            iState := 40; (* Go to safe shutdown *)
        END_IF;

    40: (* SHUTDOWN SEQUENCE *)
        rExtruderSpeedCmd := 0.0;
        rTakeawayConveyorSpeed := rTakeawayConveyorSpeed * 0.9; (* Ramp down *)
        
        IF rTakeawayConveyorSpeed < 1.0 THEN
            rTakeawayConveyorSpeed := 0.0;
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

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
