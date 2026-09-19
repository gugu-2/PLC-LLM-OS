import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Large-Scale Desalination Reverse Osmosis High-Pressure Pump VFD and Energy Recovery Device Interlock**

Task: Invent a highly complex, ultra-realistic control scenario for this domain. Make this code EVEN BETTER, MORE ADVANCED, and MORE RIGOROUS than previous iterations. Include extreme edge-case handling, advanced math, and robust fault-tolerance.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_RO_Desalination\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Large-Scale Desalination Reverse Osmosis High-Pressure Pump VFD and Energy Recovery Device Interlock

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_RO_HPP_ERD_Interlock
VAR_INPUT
    bSystemEnable           : BOOL;     (* Main system enable command *)
    bEmergencyStop          : BOOL;     (* Safety circuit OK (Active High) *)
    rInletPressure          : REAL;     (* Pre-treatment feed pressure in bar *)
    rHPPDischargePressure   : REAL;     (* High Pressure Pump discharge pressure in bar *)
    rPermeateFlow           : REAL;     (* Permeate flow rate in m3/h *)
    rBrineFlow              : REAL;     (* Brine reject flow rate in m3/h *)
    rFeedConductivity       : REAL;     (* Feed water conductivity in uS/cm *)
    rVFD_SpeedFeedback      : REAL;     (* HPP VFD actual speed in % *)
END_VAR
VAR_OUTPUT
    bHPP_RunCmd             : BOOL;     (* Command to start High Pressure Pump *)
    rHPP_SpeedSetpoint      : REAL;     (* Speed setpoint for HPP VFD (0-100%) *)
    bERD_BoosterCmd         : BOOL;     (* Command to start ERD Booster Pump *)
    rERD_FlowTarget         : REAL;     (* ERD flow target setpoint in m3/h *)
    bAlarm                  : BOOL;     (* General fault alarm *)
    iFaultCode              : INT;      (* Specific fault code for HMI diagnosis *)
END_VAR
VAR
    iState                  : INT := 0; (* Internal state machine step *)
    tStartupTimer           : TON;      (* Timer for step transitions during start up *)
    tERD_Delay              : TON;      (* Delay timer for ERD synchronization *)
    tFaultTimer             : TON;      (* Persistence timer for fault conditions *)
    
    rFilteredInletPres      : REAL;     (* Low-pass filtered inlet pressure *)
    rPrevInletPres          : REAL := 0.0;
    rAlpha                  : REAL := 0.1; (* Filter coefficient *)
    
    rTargetRecovery         : REAL := 45.0; (* Desired RO recovery in % *)
    rActualRecovery         : REAL;     (* Calculated actual recovery *)
    
    (* PID Controller variables for Pressure control *)
    rError                  : REAL;
    rIntegral               : REAL := 0.0;
    rDerivative             : REAL := 0.0;
    rLastError              : REAL := 0.0;
    rKp                     : REAL := 1.2;
    rKi                     : REAL := 0.05;
    rKd                     : REAL := 0.01;
    rPID_Output             : REAL;
    rPressureSetpoint       : REAL := 60.0; (* Bar *)
END_VAR

(* === MAIN LOGIC === *)

(* Noise filtering on critical inlet pressure sensor *)
rFilteredInletPres := (rAlpha * rInletPressure) + ((1.0 - rAlpha) * rPrevInletPres);
rPrevInletPres := rFilteredInletPres;

(* Safety Interlocks & Fault Detection *)
IF NOT bEmergencyStop THEN
    bHPP_RunCmd := FALSE;
    bERD_BoosterCmd := FALSE;
    rHPP_SpeedSetpoint := 0.0;
    bAlarm := TRUE;
    iFaultCode := 99; (* E-Stop Active *)
    iState := 0;
    RETURN;
END_IF;

(* Critical low pressure fault check *)
tFaultTimer(IN := (rFilteredInletPres < 2.0 AND bHPP_RunCmd), PT := T#2S);
IF tFaultTimer.Q THEN
    bHPP_RunCmd := FALSE;
    bERD_BoosterCmd := FALSE;
    rHPP_SpeedSetpoint := 0.0;
    bAlarm := TRUE;
    iFaultCode := 10; (* Low Inlet Pressure - Cavitation Risk *)
    iState := 0;
    RETURN;
END_IF;

(* High Pressure fault check *)
IF rHPPDischargePressure > 80.0 THEN
    bHPP_RunCmd := FALSE;
    bERD_BoosterCmd := FALSE;
    rHPP_SpeedSetpoint := 0.0;
    bAlarm := TRUE;
    iFaultCode := 20; (* Overpressure Fault *)
    iState := 0;
    RETURN;
END_IF;

(* State Machine for RO Startup Sequence *)
CASE iState OF
    0: (* IDLE *)
        bHPP_RunCmd := FALSE;
        bERD_BoosterCmd := FALSE;
        rHPP_SpeedSetpoint := 0.0;
        bAlarm := FALSE;
        iFaultCode := 0;
        
        IF bSystemEnable AND rFilteredInletPres >= 2.5 THEN
            iState := 10;
        END_IF;
        
    10: (* ERD PRIMING *)
        bERD_BoosterCmd := TRUE;
        tStartupTimer(IN := TRUE, PT := T#10S);
        
        IF tStartupTimer.Q THEN
            tStartupTimer(IN := FALSE);
            iState := 20;
        END_IF;
        
    20: (* HPP RAMP UP *)
        bHPP_RunCmd := TRUE;
        (* Open loop ramp up *)
        rHPP_SpeedSetpoint := rHPP_SpeedSetpoint + 0.1;
        
        IF rHPP_SpeedSetpoint >= 30.0 AND rHPPDischargePressure > 30.0 THEN
            iState := 30;
        END_IF;
        
    30: (* PID PRESSURE CONTROL *)
        bHPP_RunCmd := TRUE;
        bERD_BoosterCmd := TRUE;
        
        (* Calculate Actual Recovery *)
        IF (rPermeateFlow + rBrineFlow) > 0.0 THEN
            rActualRecovery := (rPermeateFlow / (rPermeateFlow + rBrineFlow)) * 100.0;
        ELSE
            rActualRecovery := 0.0;
        END_IF;
        
        (* ERD Flow Target adjustment based on Recovery *)
        rERD_FlowTarget := rBrineFlow * 0.95; (* Target 95% brine flow through ERD *)
        
        (* PID Control for HPP VFD Speed to maintain discharge pressure *)
        rError := rPressureSetpoint - rHPPDischargePressure;
        rIntegral := rIntegral + (rError * 0.1); (* Assuming 100ms task cycle *)
        
        (* Anti-windup for integral term *)
        IF rIntegral > 100.0 THEN rIntegral := 100.0; END_IF;
        IF rIntegral < -100.0 THEN rIntegral := -100.0; END_IF;
        
        rDerivative := (rError - rLastError) / 0.1;
        rLastError := rError;
        
        rPID_Output := (rKp * rError) + (rKi * rIntegral) + (rKd * rDerivative);
        
        rHPP_SpeedSetpoint := 30.0 + rPID_Output; (* Base speed + PID trim *)
        
        (* Clamp VFD Speed *)
        IF rHPP_SpeedSetpoint > 100.0 THEN
            rHPP_SpeedSetpoint := 100.0;
        ELSIF rHPP_SpeedSetpoint < 30.0 THEN
            rHPP_SpeedSetpoint := 30.0;
        END_IF;
        
        IF NOT bSystemEnable THEN
            iState := 40;
        END_IF;
        
    40: (* SHUTDOWN RAMP DOWN *)
        rHPP_SpeedSetpoint := rHPP_SpeedSetpoint - 0.2;
        
        IF rHPP_SpeedSetpoint <= 10.0 THEN
            bHPP_RunCmd := FALSE;
            tERD_Delay(IN := TRUE, PT := T#15S);
            IF tERD_Delay.Q THEN
                tERD_Delay(IN := FALSE);
                bERD_BoosterCmd := FALSE;
                iState := 0;
            END_IF;
        END_IF;
        
END_CASE;

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
