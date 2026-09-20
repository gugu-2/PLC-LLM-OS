import os
import json
import uuid

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V4 Persona: a 50+ years experienced Chief PLC Architect & Control Systems PhD. 
Your logic must include advanced Non-Linear PID with Anti-Windup, 3-level cascade control, digital low-pass filtering, predictive anomaly detection, and multi-layered hardware interlocks. Output the most elite, mathematically rigorous, and structurally flawless IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Automated Extrusion Blow Molding (EBM) Machine Parison Wall Thickness Profiling and Hydraulic Clamp**

Task: Invent a highly complex, ultra-realistic control scenario for this domain. This MUST be drastically better, more advanced, and longer than previous iterations.

CRITICAL RULES - READ EVERY LINE:
1. CODE FENCE: Use TRIPLE backticks + iec-st. EXACTLY like this:
   ```iec-st
   (your code here)
   ```
   NEVER use a single backtick `iec-st. ALWAYS use triple backticks.
2. REQUIRED IEC 61131-3 STRUCTURE (all 5 mandatory):
   a. FUNCTION_BLOCK FB_<Name>   <- first line of code, always
   b. VAR_INPUT ... END_VAR      <- min 6 typed inputs with comments
   c. VAR_OUTPUT ... END_VAR     <- min 5 typed outputs with comments
   d. At least one END_IF; or END_CASE;  <- control logic required
   e. END_FUNCTION_BLOCK         <- last line of code, always
3. LENGTH: The assistant content MUST be >= 2000 characters total. Make it massive and extremely rigorous.
4. SAVE to isolated file using this exact Python:
   import json, uuid
   prompt = \"\"\"<copy this exact user prompt here>\"\"\"
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_BlowMolding_ParisonControl\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
   record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
   with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
       json.dump(record, f, ensure_ascii=False)
5. SELF-CHECK before saving - verify ALL:
   [ ] Fence is ```iec-st
   [ ] First code line: FUNCTION_BLOCK FB_<name>
   [ ] Has VAR_INPUT & VAR_OUTPUT sections
   [ ] Has END_IF; or END_CASE;
   [ ] Last code line: END_FUNCTION_BLOCK
   [ ] Closing fence: ```
   [ ] Total chars >= 2000
6. REPLY with: EVOLUTION COMPLETE: Automated Extrusion Blow Molding (EBM) Machine Parison Wall Thickness Profiling and Hydraulic Clamp"""

code = """```iec-st
FUNCTION_BLOCK FB_BlowMolding_ParisonControl
VAR_INPUT
    (* Machine Safety and Enable Inputs *)
    bMasterEnable           : BOOL;     (* Main safety circuit healthy and system enabled *)
    bEmergencyStop          : BOOL;     (* E-Stop active low (FALSE = STOP) *)
    bSafetyDoorsClosed      : BOOL;     (* Interlock for mold area doors *)
    
    (* Extrusion Process Inputs *)
    rMeltPressure           : REAL;     (* Melt pressure in extruder head (bar) *)
    rMeltTemp               : REAL;     (* Melt temperature at die head (degC) *)
    rDieGapPosition_fb      : REAL;     (* Feedback from LVDT for die gap (mm) *)
    
    (* Parison Profiling Inputs *)
    rTargetThicknessProfile : ARRAY[1..100] OF REAL; (* Desired thickness profile across length *)
    rCurrentParisonLength   : REAL;     (* Current length of extruded parison (mm) *)
    rExtruderSpeed          : REAL;     (* Current screw speed (RPM) *)
    
    (* Hydraulic Clamp Inputs *)
    rClampPressure_fb       : REAL;     (* Hydraulic clamp pressure feedback (bar) *)
    rClampPosition_fb       : REAL;     (* Mold clamp position (mm) *)
END_VAR
VAR_OUTPUT
    (* Machine Status Outputs *)
    bSystemReady            : BOOL;     (* System ready for extrusion and clamping *)
    bSystemFault            : BOOL;     (* Global fault flag *)
    iFaultCode              : INT;      (* Diagnostics fault code *)
    
    (* Control Signals *)
    rDieGapCommand          : REAL;     (* Command to die gap servo valve (mm) *)
    rClampValveCommand      : REAL;     (* Command to proportional hydraulic valve for clamp (-100 to 100%) *)
    
    (* Predictive Alarms *)
    bThicknessAnomaly       : BOOL;     (* Predictive warning for out-of-spec parison *)
    bHydraulicLeakWarning   : BOOL;     (* Warning for pressure decay in hydraulic circuit *)
END_VAR
VAR
    (* Internal State Machine *)
    iState                  : INT := 0;
    
    (* Digital Low-Pass Filters *)
    rFilteredMeltPressure   : REAL := 0.0;
    rFilteredDieGap_fb      : REAL := 0.0;
    rAlphaPressure          : REAL := 0.15; (* Filter coefficient for pressure *)
    rAlphaDieGap            : REAL := 0.25; (* Filter coefficient for LVDT *)
    
    (* Advanced PID Variables (Die Gap) *)
    rGapError               : REAL;
    rGapError_Prev          : REAL;
    rGapIntegral            : REAL;
    rGapDerivative          : REAL;
    rKp_Gap                 : REAL := 2.5;
    rKi_Gap                 : REAL := 0.5;
    rKd_Gap                 : REAL := 0.1;
    rGapDeadband            : REAL := 0.02; (* Deadband for servo jitter reduction *)
    
    (* Cascade Control Variables (Clamp Pressure/Position) *)
    rTargetClampPos         : REAL;
    rPosError               : REAL;
    rTargetClampPress       : REAL;
    rPressError             : REAL;
    
    (* Timers and Interlocks *)
    tExtrusionTimer         : TON;
    tClampSettleTimer       : TON;
    rParisonIndex           : INT;
    
    (* Anomaly Detection buffers *)
    rHistoricalPressure     : ARRAY[1..10] OF REAL;
    iHistIdx                : INT := 1;
    rPressureTrend          : REAL;
END_VAR

(* === MAIN SAFETY AND HARDWARE INTERLOCKS === *)
IF NOT bEmergencyStop OR NOT bSafetyDoorsClosed THEN
    bSystemReady := FALSE;
    bSystemFault := TRUE;
    iFaultCode := 1001; (* E-Stop or Doors open *)
    rDieGapCommand := 0.0;
    rClampValveCommand := 0.0;
    iState := 0;
    RETURN;
END_IF;

(* === DIGITAL LOW-PASS FILTERING === *)
(* Exponential Moving Average for noisy sensor data *)
rFilteredMeltPressure := (rAlphaPressure * rMeltPressure) + ((1.0 - rAlphaPressure) * rFilteredMeltPressure);
rFilteredDieGap_fb := (rAlphaDieGap * rDieGapPosition_fb) + ((1.0 - rAlphaDieGap) * rFilteredDieGap_fb);

(* === PREDICTIVE ANOMALY DETECTION === *)
(* Hydraulic leak detection via pressure derivative analysis *)
rHistoricalPressure[iHistIdx] := rClampPressure_fb;
iHistIdx := iHistIdx + 1;
IF iHistIdx > 10 THEN
    iHistIdx := 1;
END_IF;
rPressureTrend := rHistoricalPressure[iHistIdx] - rHistoricalPressure[IF iHistIdx=1 THEN 10 ELSE iHistIdx-1 END_IF];
IF iState = 40 AND rPressureTrend < -5.0 THEN
    bHydraulicLeakWarning := TRUE; (* Sudden pressure drop during clamp hold *)
ELSE
    bHydraulicLeakWarning := FALSE;
END_IF;

(* === MAIN STATE MACHINE === *)
CASE iState OF
    0: (* IDLE & INITIALIZATION *)
        IF bMasterEnable THEN
            rGapIntegral := 0.0;
            rGapError_Prev := 0.0;
            bSystemFault := FALSE;
            iFaultCode := 0;
            bThicknessAnomaly := FALSE;
            bSystemReady := TRUE;
            iState := 10;
        END_IF;

    10: (* PARISON EXTRUSION & WALL THICKNESS PROFILING *)
        (* Map current parison length to profile array index *)
        rParisonIndex := REAL_TO_INT(rCurrentParisonLength * 0.1); (* Assuming 1000mm total length mapped to 1..100 *)
        IF rParisonIndex < 1 THEN rParisonIndex := 1; END_IF;
        IF rParisonIndex > 100 THEN rParisonIndex := 100; END_IF;
        
        (* Target die gap is derived from thickness profile and melt properties *)
        rGapError := rTargetThicknessProfile[rParisonIndex] - rFilteredDieGap_fb;
        
        (* Deadband to prevent valve micro-oscillations *)
        IF ABS(rGapError) < rGapDeadband THEN
            rGapError := 0.0;
        END_IF;
        
        (* Non-Linear PID with Anti-Windup *)
        rGapIntegral := rGapIntegral + (rGapError * 0.01); (* 10ms task cycle assumption *)
        (* Anti-windup limits *)
        IF rGapIntegral > 10.0 THEN rGapIntegral := 10.0; END_IF;
        IF rGapIntegral < -10.0 THEN rGapIntegral := -10.0; END_IF;
        
        rGapDerivative := (rGapError - rGapError_Prev) / 0.01;
        
        (* Compute Output *)
        rDieGapCommand := (rKp_Gap * rGapError) + (rKi_Gap * rGapIntegral) + (rKd_Gap * rGapDerivative);
        rGapError_Prev := rGapError;
        
        (* Transition to clamping if parison reached target length *)
        IF rCurrentParisonLength >= 1000.0 THEN
            iState := 20;
        END_IF;

    20: (* CLAMP FAST APPROACH (POSITION CONTROL) *)
        rTargetClampPos := 5.0; (* 5mm from close *)
        rPosError := rTargetClampPos - rClampPosition_fb;
        rClampValveCommand := LIMIT(-100.0, rPosError * 5.0, 100.0);
        
        IF ABS(rPosError) < 1.0 THEN
            iState := 30;
        END_IF;

    30: (* CLAMP HIGH PRESSURE BUILD (CASCADE CONTROL) *)
        (* Outer Loop: Position dictates target pressure *)
        rTargetClampPos := 0.0; (* fully closed *)
        rTargetClampPress := 150.0 + ( (rClampPosition_fb - rTargetClampPos) * 10.0 );
        
        (* Inner Loop: Pressure control *)
        rPressError := rTargetClampPress - rClampPressure_fb;
        rClampValveCommand := LIMIT(0.0, rPressError * 0.5, 100.0);
        
        IF rClampPressure_fb >= 145.0 THEN
            iState := 40;
            tClampSettleTimer(IN := FALSE); (* Reset timer *)
        END_IF;

    40: (* CLAMP HOLD & BLOW MOLDING COOLING PHASE *)
        tClampSettleTimer(IN := TRUE, PT := T#10S);
        rClampValveCommand := 10.0; (* Maintenance pressure holding *)
        
        IF tClampSettleTimer.Q THEN
            tClampSettleTimer(IN := FALSE);
            iState := 50;
        END_IF;
        
    50: (* MOLD OPENING *)
        rTargetClampPos := 500.0; (* Fully open *)
        rPosError := rTargetClampPos - rClampPosition_fb;
        rClampValveCommand := LIMIT(-100.0, rPosError * -2.0, 100.0);
        
        IF ABS(rPosError) < 5.0 THEN
            iState := 10; (* Loop back for next parison *)
        END_IF;
        
    ELSE
        iState := 0;
END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
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
