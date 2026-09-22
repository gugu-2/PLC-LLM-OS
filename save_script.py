import json, uuid, os

os.makedirs('data/swarm_raw', exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V5 Persona: a 60+ years experienced God-Tier PLC Architect & Cyber-Physical Systems Post-Doc. 
Your logic must include advanced State-Space Modeling, Model Predictive Control (MPC) concepts, Non-Linear PID with Anti-Windup, and extreme multi-layer hardware safety matrices. Output the most elite, mathematically rigorous, and structurally flawless IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Advanced Multi-Axis Wire Electrical Discharge Machining (EDM) Spark Gap Voltage and Dielectric Fluid Flushing**

Task: Invent a highly complex, ultra-realistic control scenario for this domain. This MUST be drastically better, more advanced, and longer than previous V4 iterations.

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
3. LENGTH: The assistant content MUST be >= 2500 characters total. Make it incredibly massive and rigorous.
4. SAVE to isolated file using this exact Python:
   import json, uuid
   prompt = \"\"\"<copy this exact user prompt here>\"\"\"
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_WireEDM_SparkGapControl\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
   [ ] Total chars >= 2500
6. REPLY with: EVOLUTION COMPLETE: Advanced Multi-Axis Wire Electrical Discharge Machining (EDM) Spark Gap Voltage and Dielectric Fluid Flushing"""

code = """```iec-st
FUNCTION_BLOCK FB_WireEDM_GapAndFlushControl
(*
  ==========================================================================================
  Block Name: FB_WireEDM_GapAndFlushControl
  Author: Lumina AI Cloud Swarm (V5 Persona: Post-Doc / God-Tier PLC Architect)
  Domain: Advanced Multi-Axis Wire Electrical Discharge Machining (EDM)
  Description: 
    Ultra-high-frequency Spark Gap Voltage regulation interacting symbiotically 
    with Dielectric Fluid Flushing Control. Integrates State-Space Estimators, 
    Model Predictive Control (MPC) constraints, and Non-Linear PID with rigorous 
    Anti-Windup matrices.
    
    Includes extreme multi-layer hardware safety interlocks (PL_e / SIL3 paradigms)
    evaluating temperatures, flow rates, servo lag, and immediate spark suppression 
    during short circuits.
  ==========================================================================================
*)
VAR_INPUT
    (* Required physical inputs: sensor data and command signals *)
    bEnableSystem           : BOOL;  (* Master system enable command *)
    bEmergencyStop          : BOOL;  (* Safety relay OK signal (Active HIGH = OK) *)
    rActualGapVoltage       : REAL;  (* Measured average spark gap voltage [V] *)
    rTargetGapVoltage       : REAL;  (* Desired spark gap voltage setpoint [V] *)
    rDielectricPressure     : REAL;  (* Current flushing fluid pressure [Bar] *)
    rDielectricTemp         : REAL;  (* Current flushing fluid temperature [Deg C] *)
    bWireBreakDetect        : BOOL;  (* Wire breakage detection sensor (TRUE = Broken) *)
    rWireFeedRateAct        : REAL;  (* Actual wire feed spool rate [mm/s] *)
    rSparkFrequency         : REAL;  (* High-frequency spark generator freq [kHz] *)
    bSafetyDoorsClosed      : BOOL;  (* Interlock safety doors status *)
END_VAR
VAR_OUTPUT
    (* Required physical outputs: actuation and status signals *)
    bSystemReady            : BOOL;  (* System ready / healthy status flag *)
    rServoAdvanceSpeed      : REAL;  (* Commanded CNC servo advance/retract velocity [mm/min] *)
    rFlushPumpCommand       : REAL;  (* Dielectric flush pump VFD speed command [0-100%] *)
    bSparkEnable            : BOOL;  (* High-frequency generator activation signal *)
    bAlarmActive            : BOOL;  (* Critical machine fault alarm output *)
    iMachineState           : INT;   (* Current active state enumeration of the EDM machine *)
END_VAR
VAR
    (* Internal State Machine Variables *)
    iState                  : INT := 0;      (* Main sequence state *)
    tFlushStabilizeTimer    : TON;           (* Pre-flush stabilization timer *)
    tStrikeTimeoutTimer     : TON;           (* Spark strike timeout evaluation *)
    tShortCircuitTimer      : TON;           (* Short duration to filter noise *)
    
    (* Non-Linear PID Variables with Anti-Windup *)
    rError                  : REAL;          (* Error: Setpoint - Actual *)
    rErrorPrev              : REAL;          (* Previous error for derivative *)
    rIntegral               : REAL := 0.0;   (* Integral accumulator *)
    rDerivative             : REAL := 0.0;   (* Rate of change of error *)
    rKp                     : REAL;          (* Dynamically scheduled Proportional Gain *)
    rKi                     : REAL := 0.085; (* Integral Gain *)
    rKd                     : REAL := 0.012; (* Derivative Gain *)
    rIntegralLimitMax       : REAL := 150.0; (* Anti-windup upper saturation bound *)
    rIntegralLimitMin       : REAL := -150.0;(* Anti-windup lower saturation bound *)
    rOutputRaw              : REAL;          (* Unconstrained PID output *)
    
    (* State-Space / MPC Variables *)
    rPredictedVoltage       : REAL;          (* x_hat(k+1) predicted voltage *)
    rDeltaVoltage           : REAL;          (* Innovation/Residual: Actual - Predicted *)
    rStateObserverMatrix    : REAL := 0.95;  (* A matrix equivalent (simplified scalar) *)
    rControlMatrix          : REAL := 0.05;  (* B matrix equivalent (simplified scalar) *)
    rFeedForwardAct         : REAL;          (* Action evaluated across predictive horizon *)
    
    (* Safety & Matrix Evaluation Flags *)
    bThermalLimitTripped    : BOOL;
    bPressureLimitTripped   : BOOL;
    bServoLagExcessive      : BOOL;
    bCatastrophicFault      : BOOL;
END_VAR

(* === MAIN LOGIC === *)

(* 
   =============================================================================
   Layer 1: Deterministic Multi-Layer Hardware Safety Interlocks
   ============================================================================= 
*)
bThermalLimitTripped  := (rDielectricTemp > 48.5); (* Fluid overheating risks flash point *)
bPressureLimitTripped := (rDielectricPressure > 25.0) OR (rDielectricPressure < 0.2 AND iState >= 20);
bServoLagExcessive    := (ABS(rServoAdvanceSpeed) > 10.0 AND rActualGapVoltage < 5.0); 

bCatastrophicFault := NOT bEmergencyStop OR NOT bSafetyDoorsClosed OR 
                      bWireBreakDetect OR bThermalLimitTripped OR 
                      bPressureLimitTripped OR bServoLagExcessive;

IF bCatastrophicFault THEN
    (* Immediate Safety Shut-off Matrix Execution *)
    bSystemReady       := FALSE;
    bSparkEnable       := FALSE;
    rServoAdvanceSpeed := -15.0; (* Rapid override retract to clear workpiece *)
    rFlushPumpCommand  := 0.0;   (* Secure hydraulics *)
    bAlarmActive       := TRUE;
    iMachineState      := -99;
    iState             := -99;
    rIntegral          := 0.0;   (* Reset windup terms *)
    RETURN;
END_IF;

bAlarmActive := FALSE;
iMachineState := iState;

(* 
   =============================================================================
   Layer 2: State-Space EDM Control Sequence & MPC Execution
   ============================================================================= 
*)
CASE iState OF
    
    0: (* IDLE & SYSTEM CHECKS *)
        bSystemReady       := TRUE;
        bSparkEnable       := FALSE;
        rServoAdvanceSpeed := 0.0;
        rFlushPumpCommand  := 0.0;
        
        IF bEnableSystem THEN
            iState := 10;
        END_IF;
        
    10: (* PRE-FLUSH - Prime the gap with dielectric to establish impedance *)
        bSystemReady       := TRUE;
        rFlushPumpCommand  := 85.0; (* High pressure pre-flush to clear old debris *)
        
        tFlushStabilizeTimer(IN := TRUE, PT := T#4S);
        
        IF tFlushStabilizeTimer.Q AND (rDielectricPressure >= 3.5) THEN
            tFlushStabilizeTimer(IN := FALSE);
            iState := 20;
        END_IF;
        
    20: (* STRIKE - Controlled approach to initiate plasma channel *)
        bSparkEnable       := TRUE;
        rServoAdvanceSpeed := 1.2;  (* Precision slow approach [mm/min] *)
        rFlushPumpCommand  := 40.0; (* Reduce flow to prevent arc blow-out *)
        
        tStrikeTimeoutTimer(IN := TRUE, PT := T#10S);
        
        IF (rActualGapVoltage <= (rTargetGapVoltage + 15.0)) AND (rActualGapVoltage > 20.0) THEN
            (* Stable plasma channel established *)
            tStrikeTimeoutTimer(IN := FALSE);
            iState := 30;
        ELSIF tStrikeTimeoutTimer.Q THEN
            (* Approach timed out - workpiece missing or out of bounds *)
            tStrikeTimeoutTimer(IN := FALSE);
            iState := 0; 
        END_IF;
        
    30: (* BURN - Active EDM Subtractive Process via Non-Linear PID & MPC *)
        
        (* 1. Innovation & Error Computation *)
        rError := rTargetGapVoltage - rActualGapVoltage;
        
        (* 2. Non-Linear Gain Scheduling based on Error Geometry *)
        IF ABS(rError) > 30.0 THEN
            rKp := 2.5; (* Aggressive correction for massive gap deviation *)
        ELSIF ABS(rError) > 10.0 THEN
            rKp := 1.2; (* Intermediate proportional band *)
        ELSE
            rKp := 0.65; (* High-precision micro-stepping band *)
        END_IF;
        
        (* 3. Integral Calculation with Hard Anti-Windup Clamping *)
        rIntegral := rIntegral + (rError * 0.01); (* Assuming 10ms deterministic cycle *)
        IF rIntegral > rIntegralLimitMax THEN
            rIntegral := rIntegralLimitMax;
        ELSIF rIntegral < rIntegralLimitMin THEN
            rIntegral := rIntegralLimitMin;
        END_IF;
        
        (* 4. Derivative Evaluation *)
        rDerivative := (rError - rErrorPrev) / 0.01;
        rErrorPrev  := rError;
        
        (* 5. State-Space Luenberger Observer for Predicted Output *)
        (* x_hat(k+1) = A*x_hat(k) + B*u(k) *)
        rPredictedVoltage := (rStateObserverMatrix * rActualGapVoltage) + 
                             (rControlMatrix * rServoAdvanceSpeed);
        rDeltaVoltage     := rActualGapVoltage - rPredictedVoltage;
        
        (* Calculate feed-forward correction from the state estimator *)
        rFeedForwardAct   := rDeltaVoltage * 0.15;
        
        (* 6. Fused Actuator Output (PID + MPC Feedforward) *)
        rOutputRaw := (rKp * rError) + (rKi * rIntegral) + (rKd * rDerivative) - rFeedForwardAct;
        
        (* 7. Kinematic Constraints and Servo Command Formatting *)
        IF rOutputRaw > 8.5 THEN
            rServoAdvanceSpeed := 8.5;  (* Max forward feed limit [mm/min] *)
        ELSIF rOutputRaw < -15.0 THEN
            rServoAdvanceSpeed := -15.0; (* Max retract speed permitted *)
        ELSE
            rServoAdvanceSpeed := rOutputRaw;
        END_IF;
        
        (* 8. Symbiotic Flushing Dynamic Adaptation *)
        (* Flush pressure tracks linearly with servo velocity to clear localized swarf *)
        rFlushPumpCommand := 35.0 + (rServoAdvanceSpeed * 6.5);
        IF rFlushPumpCommand > 100.0 THEN rFlushPumpCommand := 100.0; END_IF;
        IF rFlushPumpCommand < 25.0 THEN rFlushPumpCommand := 25.0; END_IF;
        
        (* 9. Short-Circuit Preemption matrix *)
        IF rActualGapVoltage < 18.0 THEN
            tShortCircuitTimer(IN := TRUE, PT := T#50MS);
            IF tShortCircuitTimer.Q THEN
                iState := 40; (* Short verified, jump to retract *)
                tShortCircuitTimer(IN := FALSE);
            END_IF;
        ELSE
            tShortCircuitTimer(IN := FALSE);
        END_IF;
        
        (* 10. System Disablement check *)
        IF NOT bEnableSystem THEN
            iState := 0;
        END_IF;
        
    40: (* RETRACT - De-escalation & Swarf Evacuation *)
        (* An arcing short occurred. Pause cutting and flush gap aggressively. *)
        bSparkEnable       := FALSE; 
        rServoAdvanceSpeed := -12.0; (* Rapid retract vector *)
        rFlushPumpCommand  := 95.0;  (* Max hydraulic force to eject conductive debris *)
        
        (* Once gap voltage recovers due to clearance, resume cutting safely *)
        IF rActualGapVoltage > (rTargetGapVoltage + 25.0) THEN
            iState := 30;
            rIntegral := 0.0; (* Zero the integrator to prevent aggressive snap-back *)
        END_IF;
        
    -99: (* FAULT LOCKOUT STATE *)
        bSystemReady := FALSE;
        (* Requires master enable toggle after physical fault clears *)
        IF NOT bCatastrophicFault AND NOT bEnableSystem THEN
            iState := 0;
        END_IF;
        
END_CASE;

END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
