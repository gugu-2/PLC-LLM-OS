import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Advanced Aerospace Carbon Fiber Tape Laying (AFP) End Effector**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., 200W/cm2 infrared laser nip-point thermoplastic consolidation heating, pneumatic conformable compaction roller force mapping, and real-time fuzz/resin-buildup optical inspection). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_AFP_TapeLayingHead\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Advanced Aerospace Carbon Fiber Tape Laying (AFP) End Effector

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_AFP_TapeLayingHead
VAR_INPUT
    bEnable                 : BOOL;     (* System master enable for AFP head *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal (Dual Channel SIL3) *)
    rLaserTargetTemp        : REAL;     (* Target IR laser heating temperature in deg C (range: 200-500) *)
    rLaserActualTemp        : REAL;     (* Pyrometer feedback of nip-point temp in deg C *)
    rCompactionForceRef     : REAL;     (* Target compaction roller force in Newtons *)
    rCompactionForceFbk     : REAL;     (* Load cell actual force in Newtons *)
    bFuzzInspectOK          : BOOL;     (* Optical inspection vision system OK signal *)
    rTapeTensionRef         : REAL;     (* Desired incoming tape tension in N *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;     (* End effector initialization complete and ready *)
    rLaserPowerCmd          : REAL;     (* Output to IR laser controller (0.0 to 100.0 %) *)
    rRollerPressureCmd      : REAL;     (* Output to pneumatic proportional valve (Bar) *)
    bDefectAlarm            : BOOL;     (* Major defect or fault detected *)
    iHeadState              : INT;      (* Current state machine step *)
END_VAR
VAR
    (* Internal State and Timers *)
    iState                  : INT := 0;
    tPreheatTimer           : TON;
    tInspectionTimer        : TON;
    tDelayTimer             : TON;
    
    (* Filter variables *)
    rTempFbkFiltered        : REAL;
    rForceFbkFiltered       : REAL;
    rAlphaTemp              : REAL := 0.2;  (* Exponential moving average alpha for temp *)
    rAlphaForce             : REAL := 0.1;  (* Exponential moving average alpha for force *)
    
    (* PID Controllers *)
    rLaserErr               : REAL;
    rLaserIntegral          : REAL := 0.0;
    rLaserKp                : REAL := 2.5;
    rLaserKi                : REAL := 0.1;
    rLaserKd                : REAL := 0.05;
    rLaserPrevErr           : REAL := 0.0;
    rLaserDerivative        : REAL;
    
    rForceErr               : REAL;
    rForceIntegral          : REAL := 0.0;
    rForceKp                : REAL := 1.2;
    rForceKi                : REAL := 0.05;
    rForcePrevErr           : REAL := 0.0;
END_VAR

(* === MAIN LOGIC === *)

(* Safety and Interlocks - SIL3 compliance check *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bDefectAlarm := TRUE;
    rLaserPowerCmd := 0.0;
    rRollerPressureCmd := 0.0;
    iState := 999; (* FAULT STATE *)
    iHeadState := iState;
    RETURN;
END_IF;

(* Sensor Noise Filtering (EMA) *)
rTempFbkFiltered := (rAlphaTemp * rLaserActualTemp) + ((1.0 - rAlphaTemp) * rTempFbkFiltered);
rForceFbkFiltered := (rAlphaForce * rCompactionForceFbk) + ((1.0 - rAlphaForce) * rForceFbkFiltered);

(* Main State Machine *)
CASE iState OF
    0: (* IDLE *)
        bSystemReady := FALSE;
        rLaserPowerCmd := 0.0;
        rRollerPressureCmd := 0.0;
        bDefectAlarm := FALSE;
        
        IF bEnable THEN
            iState := 10;
        END_IF;

    10: (* PRE-HEAT & CALIBRATION *)
        (* Bring laser to idle standby temp (e.g., 50C below target) *)
        rLaserErr := (rLaserTargetTemp - 50.0) - rTempFbkFiltered;
        rLaserPowerCmd := (rLaserErr * rLaserKp);
        IF rLaserPowerCmd > 20.0 THEN
            rLaserPowerCmd := 20.0; (* Clamp standby power *)
        ELSIF rLaserPowerCmd < 0.0 THEN
            rLaserPowerCmd := 0.0;
        END_IF;
        
        tPreheatTimer(IN := TRUE, PT := T#3S);
        IF tPreheatTimer.Q THEN
            tPreheatTimer(IN := FALSE);
            iState := 20;
        END_IF;

    20: (* READY TO LAY TAPE *)
        bSystemReady := TRUE;
        rLaserPowerCmd := 20.0; (* Maintain idle temp *)
        
        IF bEnable AND bFuzzInspectOK THEN
            iState := 30;
        ELSIF NOT bFuzzInspectOK THEN
            iState := 900; (* INSPECTION FAULT *)
        END_IF;

    30: (* ACTIVE TAPE LAYING - PID CONTROL LOOPS *)
        (* Temperature PID Control Loop *)
        rLaserErr := rLaserTargetTemp - rTempFbkFiltered;
        rLaserIntegral := rLaserIntegral + (rLaserErr * 0.01); (* Assuming 10ms cycle *)
        
        (* Anti-windup for Laser PID *)
        IF rLaserIntegral > 50.0 THEN rLaserIntegral := 50.0; END_IF;
        IF rLaserIntegral < -50.0 THEN rLaserIntegral := -50.0; END_IF;
        
        rLaserDerivative := (rLaserErr - rLaserPrevErr) / 0.01;
        rLaserPowerCmd := (rLaserKp * rLaserErr) + (rLaserKi * rLaserIntegral) + (rLaserKd * rLaserDerivative);
        
        IF rLaserPowerCmd > 100.0 THEN rLaserPowerCmd := 100.0; END_IF;
        IF rLaserPowerCmd < 0.0 THEN rLaserPowerCmd := 0.0; END_IF;
        rLaserPrevErr := rLaserErr;

        (* Compaction Force PI Control Loop *)
        rForceErr := rCompactionForceRef - rForceFbkFiltered;
        rForceIntegral := rForceIntegral + (rForceErr * 0.01);
        
        IF rForceIntegral > 10.0 THEN rForceIntegral := 10.0; END_IF;
        IF rForceIntegral < -10.0 THEN rForceIntegral := -10.0; END_IF;
        
        rRollerPressureCmd := (rForceKp * rForceErr) + (rForceKi * rForceIntegral);
        
        IF rRollerPressureCmd > 6.0 THEN rRollerPressureCmd := 6.0; END_IF; (* Max 6 Bar *)
        IF rRollerPressureCmd < 0.0 THEN rRollerPressureCmd := 0.0; END_IF;
        
        (* Continuous Inspection Monitoring *)
        IF NOT bFuzzInspectOK THEN
            tInspectionTimer(IN := TRUE, PT := T#500MS);
            IF tInspectionTimer.Q THEN
                iState := 900;
            END_IF;
        ELSE
            tInspectionTimer(IN := FALSE);
        END_IF;
        
        IF NOT bEnable THEN
            iState := 0;
            rLaserIntegral := 0.0;
            rForceIntegral := 0.0;
        END_IF;

    900: (* INSPECTION FAULT *)
        bSystemReady := FALSE;
        bDefectAlarm := TRUE;
        rLaserPowerCmd := 0.0;
        rRollerPressureCmd := 0.0;
        
        IF NOT bEnable THEN
            iState := 0; (* Reset attempt *)
        END_IF;
        
    999: (* FATAL ERROR / E-STOP *)
        bDefectAlarm := TRUE;
        rLaserPowerCmd := 0.0;
        rRollerPressureCmd := 0.0;
        (* Requires E-Stop reset and cycle power to recover *)

END_CASE;

iHeadState := iState;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": code}
    ]
}
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
