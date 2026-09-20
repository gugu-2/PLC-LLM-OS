import json
import uuid
import os

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V4 Persona: a 50+ years experienced Chief PLC Architect & Control Systems PhD. 
Your logic must include advanced Non-Linear PID with Anti-Windup, 3-level cascade control, digital low-pass filtering, predictive anomaly detection, and multi-layered hardware interlocks. Output the most elite, mathematically rigorous, and structurally flawless IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Industrial Scale Lithium-Ion Battery Foil Coating Roll-to-Roll Tension and Thickness Scanning**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_LiIonBattery_FoilCoating\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Industrial Scale Lithium-Ion Battery Foil Coating Roll-to-Roll Tension and Thickness Scanning"""

code = """```iec-st
FUNCTION_BLOCK FB_LiIonBattery_FoilCoating
VAR_INPUT
    (* Physical Safety & Enable Inputs *)
    bSystemEnable           : BOOL;     (* Main line enable command *)
    bEmergencyStop          : BOOL;     (* Safety relay loop feedback (TRUE = OK) *)
    bDriveInterlocksReady   : BOOL;     (* AC/DC drive healthy statuses aggregated *)
    bScannerAirPurgeOk      : BOOL;     (* Radiation thickness scanner air purge status *)

    (* Process Variables (Sensors) *)
    rTensionUnwindActual    : REAL;     (* Actual web tension from Unwind load cells (N) *)
    rTensionRewindActual    : REAL;     (* Actual web tension from Rewind load cells (N) *)
    rThicknessActualLeft    : REAL;     (* Beta-gauge scanner thickness actual - Left (um) *)
    rThicknessActualRight   : REAL;     (* Beta-gauge scanner thickness actual - Right (um) *)
    rLineSpeedActual        : REAL;     (* Main capstan line speed (m/min) *)

    (* Setpoints from HMI/SCADA *)
    rTensionSetpoint        : REAL;     (* Target web tension (N) *)
    rThicknessSetpoint      : REAL;     (* Target foil coating thickness (um) *)
    rLineSpeedSetpoint      : REAL;     (* Target line speed (m/min) *)
END_VAR

VAR_OUTPUT
    (* Status & Alarms *)
    bSystemReady            : BOOL;     (* All conditions met, PID active *)
    bTensionAlarm           : BOOL;     (* Tension out of bounds for > 3 sec *)
    bThicknessAlarm         : BOOL;     (* Coating out of tolerance (A/B grade reject) *)
    bEmergencyTrip          : BOOL;     (* System tripped due to interlock loss *)

    (* Control Outputs to Drives / Actuators *)
    rUnwindTorqueCmd        : REAL;     (* Unwind brake/motor torque command (%) *)
    rRewindTorqueCmd        : REAL;     (* Rewind motor torque command (%) *)
    rCoaterDieGapLeftCmd    : REAL;     (* Left servo position command for slot die gap (um) *)
    rCoaterDieGapRightCmd   : REAL;     (* Right servo position command for slot die gap (um) *)
    rMainDriveSpeedCmd      : REAL;     (* Line speed reference to master drive (m/min) *)
END_VAR

VAR
    (* Internal State & Cascaded PID Architecture Variables *)
    iState                  : INT := 0; (* Master State Machine *)
    
    (* Timers *)
    tStartupDelay           : TON;
    tTensionAlarmTimer      : TON;
    tThicknessAlarmTimer    : TON;

    (* Digital Low-Pass Filters *)
    rTensionFiltered        : REAL;
    rThicknessLeftFiltered  : REAL;
    rThicknessRightFiltered : REAL;
    rAlphaTension           : REAL := 0.15; (* Filter coefficient for tension *)
    rAlphaThickness         : REAL := 0.05; (* Filter coefficient for thickness *)

    (* Non-Linear PID - Unwind Tension *)
    rTensionError           : REAL;
    rTensionErrorPrev       : REAL;
    rTensionIntegral        : REAL;
    rTensionDerivative      : REAL;
    rTensionKp              : REAL; (* Dynamically adapted based on coil diameter *)
    rTensionKi              : REAL := 0.5;
    rTensionKd              : REAL := 0.05;
    rTensionMaxAw           : REAL := 50.0; (* Anti-windup max *)
    
    (* Master-Slave Cascade - Thickness Control *)
    rThickErrorLeft         : REAL;
    rThickErrorRight        : REAL;
    rThickIntegralLeft      : REAL;
    rThickIntegralRight     : REAL;
    rThickKp                : REAL := 2.2;
    rThickKi                : REAL := 0.1;
    rDieGapBase             : REAL := 150.0; (* Base mechanical gap offset in um *)
    
    (* Predictive Anomaly Detection *)
    rDerivativeThreshold    : REAL := 15.0; (* Max allowable rate of change in thickness *)
    bPredictiveFault        : BOOL := FALSE;
END_VAR

(* ====================================================================
   MAIN CONTROL LOGIC: LITHIUM-ION FOIL COATING
   ==================================================================== *)

(* 1. HARDWARE INTERLOCKS & SAFETY EVALUATION *)
IF NOT bEmergencyStop OR NOT bDriveInterlocksReady OR NOT bScannerAirPurgeOk THEN
    (* Immediate Halt *)
    bSystemReady            := FALSE;
    bEmergencyTrip          := TRUE;
    rUnwindTorqueCmd        := 0.0;
    rRewindTorqueCmd        := 0.0;
    rMainDriveSpeedCmd      := 0.0;
    
    (* Hold die gap at current position for safety *)
    iState                  := 0;
    rTensionIntegral        := 0.0; (* Reset integrals to prevent windup on restart *)
    rThickIntegralLeft      := 0.0;
    rThickIntegralRight     := 0.0;
    RETURN; (* Halt further execution *)
END_IF;

bEmergencyTrip := FALSE;

(* 2. SENSOR SIGNAL PROCESSING (Digital Low-Pass Filters) *)
(* Eq: y_k = alpha * x_k + (1 - alpha) * y_{k-1} *)
rTensionFiltered        := (rAlphaTension * rTensionUnwindActual) + ((1.0 - rAlphaTension) * rTensionFiltered);
rThicknessLeftFiltered  := (rAlphaThickness * rThicknessActualLeft) + ((1.0 - rAlphaThickness) * rThicknessLeftFiltered);
rThicknessRightFiltered := (rAlphaThickness * rThicknessActualRight) + ((1.0 - rAlphaThickness) * rThicknessRightFiltered);

(* 3. PREDICTIVE ANOMALY DETECTION *)
(* Calculate instantaneous rate of change of thickness to catch tearing or die clogs *)
IF ABS(rThicknessActualLeft - rThicknessLeftFiltered) > rDerivativeThreshold OR 
   ABS(rThicknessActualRight - rThicknessRightFiltered) > rDerivativeThreshold THEN
    bPredictiveFault := TRUE;
ELSE
    bPredictiveFault := FALSE;
END_IF;

(* 4. MASTER STATE MACHINE *)
CASE iState OF
    0: (* IDLE & SAFE STATE *)
        bSystemReady := FALSE;
        rMainDriveSpeedCmd := 0.0;
        
        IF bSystemEnable AND NOT bPredictiveFault THEN
            tStartupDelay(IN := TRUE, PT := T#2S);
            IF tStartupDelay.Q THEN
                iState := 10;
                tStartupDelay(IN := FALSE);
            END_IF;
        ELSE
            tStartupDelay(IN := FALSE);
        END_IF;

    10: (* TENSION ESTABLISHMENT PHASE *)
        (* Slowly apply brake torque before starting line *)
        rUnwindTorqueCmd := rUnwindTorqueCmd + 0.1;
        IF rUnwindTorqueCmd > 10.0 THEN
            iState := 20;
        END_IF;

    20: (* RUNNING & CASCADE PID ACTIVE *)
        bSystemReady := TRUE;
        rMainDriveSpeedCmd := rLineSpeedSetpoint;
        
        (* --- A. NON-LINEAR PID FOR WEB TENSION WITH ANTI-WINDUP --- *)
        rTensionError := rTensionSetpoint - rTensionFiltered;
        
        (* Gain Scheduling: Higher Kp at lower line speeds for stability *)
        IF rLineSpeedActual < 10.0 THEN
            rTensionKp := 1.5;
        ELSE
            rTensionKp := 0.8;
        END_IF;
        
        (* Integral with Anti-Windup Clamping *)
        rTensionIntegral := rTensionIntegral + (rTensionError * rTensionKi);
        IF rTensionIntegral > rTensionMaxAw THEN rTensionIntegral := rTensionMaxAw; END_IF;
        IF rTensionIntegral < -rTensionMaxAw THEN rTensionIntegral := -rTensionMaxAw; END_IF;
        
        rTensionDerivative := (rTensionError - rTensionErrorPrev) * rTensionKd;
        rTensionErrorPrev := rTensionError;
        
        (* Compute Output *)
        rUnwindTorqueCmd := (rTensionError * rTensionKp) + rTensionIntegral + rTensionDerivative;
        
        (* Torque Output Clamping (0% to 100%) *)
        IF rUnwindTorqueCmd > 100.0 THEN rUnwindTorqueCmd := 100.0; END_IF;
        IF rUnwindTorqueCmd < 0.0 THEN rUnwindTorqueCmd := 0.0; END_IF;
        
        (* Set rewind torque proportionally (simplified for this example) *)
        rRewindTorqueCmd := rUnwindTorqueCmd * 1.05; 

        (* --- B. CASCADE CONTROL: THICKNESS TO DIE GAP --- *)
        (* Left Side *)
        rThickErrorLeft := rThicknessSetpoint - rThicknessLeftFiltered;
        rThickIntegralLeft := rThickIntegralLeft + (rThickErrorLeft * rThickKi);
        rCoaterDieGapLeftCmd := rDieGapBase + (rThickErrorLeft * rThickKp) + rThickIntegralLeft;
        
        (* Right Side *)
        rThickErrorRight := rThicknessSetpoint - rThicknessRightFiltered;
        rThickIntegralRight := rThickIntegralRight + (rThickErrorRight * rThickKi);
        rCoaterDieGapRightCmd := rDieGapBase + (rThickErrorRight * rThickKp) + rThickIntegralRight;
        
        (* Safety bounds on Die Gap (Prevent crashing die into roller) *)
        IF rCoaterDieGapLeftCmd < 50.0 THEN rCoaterDieGapLeftCmd := 50.0; END_IF;
        IF rCoaterDieGapRightCmd < 50.0 THEN rCoaterDieGapRightCmd := 50.0; END_IF;

        (* Check for Stop Command *)
        IF NOT bSystemEnable THEN
            iState := 30;
        END_IF;

    30: (* CONTROLLED DECELERATION *)
        bSystemReady := FALSE;
        rMainDriveSpeedCmd := rMainDriveSpeedCmd - 0.5;
        IF rMainDriveSpeedCmd <= 0.0 THEN
            rMainDriveSpeedCmd := 0.0;
            rUnwindTorqueCmd := 0.0;
            rRewindTorqueCmd := 0.0;
            iState := 0;
        END_IF;

END_CASE;

(* 5. ALARM GENERATION *)
tTensionAlarmTimer(
    IN := (ABS(rTensionSetpoint - rTensionFiltered) > (rTensionSetpoint * 0.1)) AND (iState = 20), 
    PT := T#3S
);
bTensionAlarm := tTensionAlarmTimer.Q;

tThicknessAlarmTimer(
    IN := ((ABS(rThickErrorLeft) > 5.0) OR (ABS(rThickErrorRight) > 5.0)) AND (iState = 20),
    PT := T#5S
);
bThicknessAlarm := tThicknessAlarmTimer.Q OR bPredictiveFault;

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
print(f"File saved: {filename}")
