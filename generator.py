import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Gigafactory Roll-to-Roll Lithium-Ion Battery Calendering Press**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., hydraulic gap servo pressure control for sub-micron thickness reduction, unwind/rewind multi-zone web tension decoupling, and edge slitting laser web guide tracking). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_BatteryCalendering\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Gigafactory Roll-to-Roll Lithium-Ion Battery Calendering Press

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_Gigafactory_CalenderPress
(* 
   =============================================================================
   Lumina AI Cloud Swarm Synthetic Data
   Domain: Gigafactory Roll-to-Roll Lithium-Ion Battery Calendering Press
   Description: Ultra-precision hydraulic gap servo pressure control, web tension 
   decoupling, and laser web guide tracking for sub-micron thickness reduction.
   Author: 40-year veteran PLC architect
   =============================================================================
*)
VAR_INPUT
    bEnable                 : BOOL;     (* System master enable signal *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal (Normally Closed = Safe) *)
    rInletTensionRef        : REAL;     (* Desired inlet web tension [N] *)
    rOutletTensionRef       : REAL;     (* Desired outlet web tension [N] *)
    rInletTensionAct        : REAL;     (* Actual inlet web tension from load cells [N] *)
    rOutletTensionAct       : REAL;     (* Actual outlet web tension from load cells [N] *)
    rTargetThickness        : REAL;     (* Target electrode thickness [µm] *)
    rActualThicknessPre     : REAL;     (* Pre-calender thickness measurement [µm] *)
    rActualThicknessPost    : REAL;     (* Post-calender thickness from beta gauge [µm] *)
    rPressForceAct          : REAL;     (* Actual hydraulic pressing force [kN] *)
    rWebSpeedRef            : REAL;     (* Master line speed reference [m/min] *)
    bLaserGuideOK           : BOOL;     (* Edge slitting laser guide system healthy *)
    rEdgeDeviation          : REAL;     (* Web edge deviation from centerline [mm] *)
END_VAR

VAR_OUTPUT
    bSystemReady            : BOOL;     (* System ready status for upstream/downstream *)
    rHydraulicValveCmd      : REAL;     (* Servo valve command for hydraulic gap cylinders [-100..100%] *)
    rUnwindTorqueCmd        : REAL;     (* Unwind motor torque command for tension control [Nm] *)
    rRewindTorqueCmd        : REAL;     (* Rewind motor torque command for tension control [Nm] *)
    rEdgeGuidePositionCmd   : REAL;     (* Web guide actuator position command [mm] *)
    bAlarm                  : BOOL;     (* Fault alarm output *)
    iErrorCode              : INT;      (* Detailed error code for HMI *)
    rActualCompressionRatio : REAL;     (* Calculated compression ratio *)
END_VAR

VAR
    (* Internal State and Timers *)
    iState                  : INT := 0;
    tStartDelay             : TON;
    tTensionSettleTime      : TON;
    tSafetyWatchdog         : TON;
    
    (* PI Controllers for Tension and Pressure *)
    rTensionKp              : REAL := 2.5;
    rTensionKi              : REAL := 0.8;
    rTensionErrInlet        : REAL;
    rTensionErrOutlet       : REAL;
    rTensionIntegralInlet   : REAL := 0.0;
    rTensionIntegralOutlet  : REAL := 0.0;
    
    rGapKp                  : REAL := 15.0;
    rGapKi                  : REAL := 4.2;
    rGapKd                  : REAL := 1.1;
    rThicknessErr           : REAL;
    rThicknessIntegral      : REAL := 0.0;
    rThicknessDeriv         : REAL := 0.0;
    rThicknessPrevErr       : REAL := 0.0;
    
    (* Filtering and calculations *)
    rFilteredThickness      : REAL := 0.0;
    rAlphaFilter            : REAL := 0.15; (* Low pass filter coefficient *)
    rMaxTorqueLimit         : REAL := 500.0; (* [Nm] *)
    rMaxValveCmd            : REAL := 100.0; (* [%] *)
END_VAR

(* === MAIN LOGIC === *)
(* 1. Safety and Interlocks Check *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bAlarm := TRUE;
    iErrorCode := 999; (* E-STOP Active *)
    rHydraulicValveCmd := 0.0;
    rUnwindTorqueCmd := 0.0;
    rRewindTorqueCmd := 0.0;
    rEdgeGuidePositionCmd := 0.0;
    iState := 0;
    RETURN;
END_IF;

IF NOT bLaserGuideOK THEN
    bAlarm := TRUE;
    iErrorCode := 101; (* Laser Guide Fault *)
END_IF;

(* 2. Signal Processing & Filtering *)
rFilteredThickness := rFilteredThickness + rAlphaFilter * (rActualThicknessPost - rFilteredThickness);
IF rActualThicknessPre > 0.0 THEN
    rActualCompressionRatio := (rActualThicknessPre - rFilteredThickness) / rActualThicknessPre * 100.0;
ELSE
    rActualCompressionRatio := 0.0;
END_IF;

(* 3. State Machine for Calendering Process *)
CASE iState OF
    0: (* IDLE & INITIALIZATION *)
        bSystemReady := FALSE;
        bAlarm := FALSE;
        iErrorCode := 0;
        rHydraulicValveCmd := 0.0;
        rUnwindTorqueCmd := 0.0;
        rRewindTorqueCmd := 0.0;
        rTensionIntegralInlet := 0.0;
        rTensionIntegralOutlet := 0.0;
        rThicknessIntegral := 0.0;
        rThicknessPrevErr := 0.0;
        
        IF bEnable AND bEmergencyStop AND bLaserGuideOK THEN
            iState := 10;
        END_IF;
        
    10: (* PRE-TENSIONING WEB *)
        (* Inlet Tension PI Control *)
        rTensionErrInlet := rInletTensionRef - rInletTensionAct;
        rTensionIntegralInlet := rTensionIntegralInlet + (rTensionErrInlet * rTensionKi);
        
        (* Anti-windup *)
        IF rTensionIntegralInlet > rMaxTorqueLimit THEN rTensionIntegralInlet := rMaxTorqueLimit; END_IF;
        IF rTensionIntegralInlet < -rMaxTorqueLimit THEN rTensionIntegralInlet := -rMaxTorqueLimit; END_IF;
        
        rUnwindTorqueCmd := (rTensionErrInlet * rTensionKp) + rTensionIntegralInlet;
        
        (* Outlet Tension PI Control *)
        rTensionErrOutlet := rOutletTensionRef - rOutletTensionAct;
        rTensionIntegralOutlet := rTensionIntegralOutlet + (rTensionErrOutlet * rTensionKi);
        
        IF rTensionIntegralOutlet > rMaxTorqueLimit THEN rTensionIntegralOutlet := rMaxTorqueLimit; END_IF;
        IF rTensionIntegralOutlet < -rMaxTorqueLimit THEN rTensionIntegralOutlet := -rMaxTorqueLimit; END_IF;
        
        rRewindTorqueCmd := (rTensionErrOutlet * rTensionKp) + rTensionIntegralOutlet;
        
        tTensionSettleTime(IN := TRUE, PT := T#3S);
        IF tTensionSettleTime.Q THEN
            IF ABS(rTensionErrInlet) < (rInletTensionRef * 0.05) AND ABS(rTensionErrOutlet) < (rOutletTensionRef * 0.05) THEN
                iState := 20;
                tTensionSettleTime(IN := FALSE);
            END_IF;
        END_IF;
        
    20: (* GAP SERVO HYDRAULIC ENGAGEMENT & PRODUCTION RUNNING *)
        bSystemReady := TRUE;
        
        (* Maintain Tension Control *)
        rTensionErrInlet := rInletTensionRef - rInletTensionAct;
        rTensionIntegralInlet := rTensionIntegralInlet + (rTensionErrInlet * rTensionKi);
        rUnwindTorqueCmd := (rTensionErrInlet * rTensionKp) + rTensionIntegralInlet;
        
        rTensionErrOutlet := rOutletTensionRef - rOutletTensionAct;
        rTensionIntegralOutlet := rTensionIntegralOutlet + (rTensionErrOutlet * rTensionKi);
        rRewindTorqueCmd := (rTensionErrOutlet * rTensionKp) + rTensionIntegralOutlet;
        
        (* Thickness PID Control -> Hydraulic Valve Cascade *)
        rThicknessErr := rTargetThickness - rFilteredThickness;
        rThicknessIntegral := rThicknessIntegral + (rThicknessErr * rGapKi);
        rThicknessDeriv := (rThicknessErr - rThicknessPrevErr) * rGapKd;
        
        (* Anti-windup for Gap Control *)
        IF rThicknessIntegral > rMaxValveCmd THEN rThicknessIntegral := rMaxValveCmd; END_IF;
        IF rThicknessIntegral < -rMaxValveCmd THEN rThicknessIntegral := -rMaxValveCmd; END_IF;
        
        rHydraulicValveCmd := (rThicknessErr * rGapKp) + rThicknessIntegral + rThicknessDeriv;
        
        (* Feedforward based on Web Speed *)
        rHydraulicValveCmd := rHydraulicValveCmd + (rWebSpeedRef * 0.05);
        
        (* Clamp Output *)
        IF rHydraulicValveCmd > rMaxValveCmd THEN rHydraulicValveCmd := rMaxValveCmd; END_IF;
        IF rHydraulicValveCmd < -rMaxValveCmd THEN rHydraulicValveCmd := -rMaxValveCmd; END_IF;
        
        rThicknessPrevErr := rThicknessErr;
        
        (* Edge Guide Laser Tracking - Proportional Control *)
        rEdgeGuidePositionCmd := rEdgeDeviation * 1.25; 
        
        (* Check for out of bounds thickness (Critical Fault) *)
        IF ABS(rThicknessErr) > (rTargetThickness * 0.1) THEN
            tSafetyWatchdog(IN := TRUE, PT := T#2S);
            IF tSafetyWatchdog.Q THEN
                iState := 99; (* FAULT STATE *)
            END_IF;
        ELSE
            tSafetyWatchdog(IN := FALSE);
        END_IF;
        
        IF NOT bEnable THEN
            iState := 30;
        END_IF;
        
    30: (* RAMP DOWN & DE-TENSION *)
        bSystemReady := FALSE;
        rHydraulicValveCmd := 0.0; (* Retract cylinders *)
        
        (* Gently release tension *)
        rUnwindTorqueCmd := rUnwindTorqueCmd * 0.99;
        rRewindTorqueCmd := rRewindTorqueCmd * 0.99;
        
        IF ABS(rUnwindTorqueCmd) < 5.0 AND ABS(rRewindTorqueCmd) < 5.0 THEN
            iState := 0;
        END_IF;
        
    99: (* FAULT HANDLING *)
        bSystemReady := FALSE;
        bAlarm := TRUE;
        iErrorCode := 500; (* Process Tolerance Exceeded Fault *)
        rHydraulicValveCmd := -100.0; (* Full open/retract to save rolls *)
        rUnwindTorqueCmd := 0.0;
        rRewindTorqueCmd := 0.0;
        rEdgeGuidePositionCmd := 0.0;
        
        IF NOT bEnable THEN
            iState := 0; (* Require disable to reset fault *)
        END_IF;
        
END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
