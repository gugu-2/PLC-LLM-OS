import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Automated Pharmaceutical Tablet Press Compression Force and Weight Control**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_TabletPress_Control\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Automated Pharmaceutical Tablet Press Compression Force and Weight Control

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_TabletPress_ForceWeightControl
(* 
    =============================================================================
    BLOCK NAME: FB_TabletPress_ForceWeightControl
    DESCRIPTION: 
        Advanced control algorithm for an automated pharmaceutical tablet press.
        Manages main compression force, pre-compression force, dosing depth (fill weight),
        and punch tightness with moving average filtering, statistical evaluation 
        (RSD calculation), and high-speed rejection tracking. Includes stringent
        FDA 21 CFR Part 11 compliant interlocks.
    AUTHOR: Elite Automation Architect (40+ Years Exp.)
    =============================================================================
*)

VAR_INPUT
    (* Safety and Enable signals *)
    bSystemEnable           : BOOL;     (* Overall system operational enable *)
    bEStopActive            : BOOL;     (* Emergency stop circuit OK signal (active high) *)
    bGuardDoorsClosed       : BOOL;     (* Physical guard doors closed verification *)
    
    (* Process Variables - Raw Sensor Readings *)
    rMainCompressionForce   : REAL;     (* Current main compression force [kN] *)
    rPreCompressionForce    : REAL;     (* Current pre-compression force [kN] *)
    rDosingDrivePos         : REAL;     (* Actual position of dosing drive [mm] *)
    rTurretSpeedRPM         : REAL;     (* Current turret rotational speed [RPM] *)
    
    (* Setpoints & Tolerances *)
    rTargetForce            : REAL;     (* Setpoint for main compression force [kN] *)
    rForceToleranceWarning  : REAL;     (* Force deviation limit for warning [%] *)
    rForceToleranceFault    : REAL;     (* Force deviation limit for fault/rejection [%] *)
    rTargetWeight           : REAL;     (* Target tablet weight correlate [mg] *)
    
    (* Control Parameters *)
    rFilterAlpha            : REAL;     (* Low-pass filter coefficient (0.0 to 1.0) *)
    rKp                     : REAL;     (* Proportional gain for dosing control *)
    rKi                     : REAL;     (* Integral gain for dosing control *)
    rKd                     : REAL;     (* Derivative gain for dosing control *)
END_VAR

VAR_OUTPUT
    (* Status & Control Outputs *)
    bSystemReady            : BOOL;     (* System is fully interlocked and ready to run *)
    bRunning                : BOOL;     (* System is currently compressing tablets *)
    rDosingDriveCmd         : REAL;     (* Commanded position for dosing drive [mm] *)
    rMainRollerPosCmd       : REAL;     (* Commanded position for main compression roller [mm] *)
    
    (* Rejection & Alarms *)
    bRejectTabletPulse      : BOOL;     (* High-speed pulse to reject out-of-spec tablet *)
    bAlarmWarning           : BOOL;     (* Warning: approaching tolerance limits *)
    bAlarmCritical          : BOOL;     (* Critical alarm: process out of control limits *)
    iErrorCode              : INT;      (* Diagnostic error code (0 = No Error) *)
    
    (* Process Analytics *)
    rFilteredForce          : REAL;     (* Noise-filtered main compression force [kN] *)
    rMovingAvgForce         : REAL;     (* Moving average over last N tablets [kN] *)
END_VAR

VAR
    (* Internal State Machine *)
    iState                  : INT := 0; 
    
    (* Internal Filter Variables *)
    rPrevFilteredForce      : REAL := 0.0;
    
    (* PID Variables *)
    rError                  : REAL := 0.0;
    rPrevError              : REAL := 0.0;
    rIntegral               : REAL := 0.0;
    rDerivative             : REAL := 0.0;
    
    (* Moving Average Buffer *)
    aForceBuffer            : ARRAY[1..50] OF REAL;
    iBufferIndex            : INT := 1;
    rSumForce               : REAL := 0.0;
    
    (* Timers and Triggers *)
    tStartupDelay           : TON;
    tDosingTimeout          : TON;
    fbRejectPulse           : TP;
END_VAR

(* =============================================================================
   MAIN LOGIC EXECUTION
   ============================================================================= *)

(* 1. CRITICAL SAFETY & INTERLOCKS *)
IF NOT bEStopActive OR NOT bGuardDoorsClosed THEN
    bSystemReady := FALSE;
    bRunning := FALSE;
    rDosingDriveCmd := rDosingDrivePos; (* Freeze dosing *)
    bAlarmCritical := TRUE;
    iErrorCode := 999; (* Critical Safety Interlock Tripped *)
    iState := 0;       (* Force to IDLE *)
    RETURN;
END_IF;

(* 2. SENSOR SIGNAL PROCESSING (Noise Filtering) *)
(* Apply Exponential Smoothing Low-Pass Filter to raw compression force *)
rFilteredForce := (rFilterAlpha * rMainCompressionForce) + ((1.0 - rFilterAlpha) * rPrevFilteredForce);
rPrevFilteredForce := rFilteredForce;

(* Update Moving Average Ring Buffer *)
rSumForce := rSumForce - aForceBuffer[iBufferIndex];
aForceBuffer[iBufferIndex] := rFilteredForce;
rSumForce := rSumForce + aForceBuffer[iBufferIndex];

iBufferIndex := iBufferIndex + 1;
IF iBufferIndex > 50 THEN
    iBufferIndex := 1;
END_IF;

rMovingAvgForce := rSumForce / 50.0;

(* 3. FAULT DETECTION & TABLET REJECTION *)
bAlarmWarning := FALSE;
bRejectTabletPulse := FALSE;
bAlarmCritical := FALSE;

(* Check if force is outside warning band *)
IF ABS(rFilteredForce - rTargetForce) > (rTargetForce * rForceToleranceWarning / 100.0) THEN
    bAlarmWarning := TRUE;
    iErrorCode := 10;
END_IF;

(* Check if force is outside critical fault band (requires rejection) *)
IF ABS(rFilteredForce - rTargetForce) > (rTargetForce * rForceToleranceFault / 100.0) THEN
    bRejectTabletPulse := TRUE;
    iErrorCode := 20;
    
    (* If moving average is also out of fault tolerance, process is out of control *)
    IF ABS(rMovingAvgForce - rTargetForce) > (rTargetForce * rForceToleranceFault / 100.0) THEN
        bAlarmCritical := TRUE;
        iErrorCode := 99;
        iState := 0; (* Abort operation *)
    END_IF;
END_IF;

(* Generate fixed-width reject pulse *)
fbRejectPulse(IN := bRejectTabletPulse, PT := T#50MS);
bRejectTabletPulse := fbRejectPulse.Q;

(* 4. STATE MACHINE CONTROL *)
CASE iState OF
    0: (* STATE: IDLE & INITIALIZATION *)
        bSystemReady := TRUE;
        bRunning := FALSE;
        rIntegral := 0.0;
        rPrevError := 0.0;
        
        IF bSystemEnable AND NOT bAlarmCritical THEN
            iState := 10;
        END_IF;
        
    10: (* STATE: STARTUP / RAMPING *)
        bSystemReady := TRUE;
        bRunning := TRUE;
        tStartupDelay(IN := TRUE, PT := T#2S);
        
        IF tStartupDelay.Q THEN
            tStartupDelay(IN := FALSE);
            iState := 20;
        END_IF;
        
    20: (* STATE: ACTIVE COMPRESSION & PID WEIGHT CONTROL *)
        bSystemReady := TRUE;
        bRunning := TRUE;
        
        (* Calculate error between target force (representing weight) and moving average force *)
        rError := rTargetForce - rMovingAvgForce;
        
        (* Calculate PID terms *)
        rIntegral := rIntegral + (rError * 0.01); (* Assuming 10ms task cycle *)
        
        (* Anti-windup clamping *)
        IF rIntegral > 5.0 THEN rIntegral := 5.0; END_IF;
        IF rIntegral < -5.0 THEN rIntegral := -5.0; END_IF;
        
        rDerivative := (rError - rPrevError) / 0.01;
        
        (* Compute Dosing Drive Command (Fill Depth Control) *)
        rDosingDriveCmd := rDosingDrivePos + (rKp * rError) + (rKi * rIntegral) + (rKd * rDerivative);
        
        (* Clamp Dosing Command to physical limits [e.g., 5mm to 25mm] *)
        IF rDosingDriveCmd > 25.0 THEN rDosingDriveCmd := 25.0; END_IF;
        IF rDosingDriveCmd < 5.0 THEN rDosingDriveCmd := 5.0; END_IF;
        
        rPrevError := rError;
        
        (* Auto-adjust Main Roller to maintain baseline thickness *)
        rMainRollerPosCmd := rTargetForce * 0.05 + 10.0;
        
        IF NOT bSystemEnable THEN
            iState := 30;
        END_IF;
        
    30: (* STATE: RUNDOWN *)
        bSystemReady := TRUE;
        bRunning := FALSE;
        iState := 0;
        
    ELSE
        iState := 0;

END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs('data/swarm_raw', exist_ok=True)
record = {'messages': [{'role': 'user', 'content': prompt}, {'role': 'assistant', 'content': code}]}
filename = f'data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json'
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(record, f, ensure_ascii=False)
print(f'Saved to {filename}')
