import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V5 Persona: a 60+ years experienced God-Tier PLC Architect & Cyber-Physical Systems Post-Doc. 
Your logic must include advanced State-Space Modeling, Model Predictive Control (MPC) concepts, Non-Linear PID with Anti-Windup, and extreme multi-layer hardware safety matrices. Output the most elite, mathematically rigorous, and structurally flawless IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Advanced Multi-Megawatt Geothermal Binary Cycle Power Plant Turbine Bypass and Isopentane Vaporization**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_GeothermalBinary_TurbineBypass\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Advanced Multi-Megawatt Geothermal Binary Cycle Power Plant Turbine Bypass and Isopentane Vaporization"""

code = """```iec-st
FUNCTION_BLOCK FB_GeothermalBinary_TurbineBypass
(*=================================================================================================================
  Function Block: FB_GeothermalBinary_TurbineBypass
  Description:
    Advanced Control of Multi-Megawatt Geothermal Binary Cycle Power Plant Turbine Bypass and Isopentane Vaporization.
    Incorporates Model Predictive Control (MPC) concepts, Non-Linear PID with Anti-Windup,
    and extreme multi-layer hardware safety matrices.
  Version: 5.0
  Author: God-Tier PLC Architect & Cyber-Physical Systems Post-Doc
=================================================================================================================*)
VAR_INPUT
    bEnable                 : BOOL;       (* System enable signal from DCS *)
    bEmergencyStop          : BOOL;       (* Safety relay OK signal (1 = OK, 0 = E-STOP) *)
    bGridTrip               : BOOL;       (* Grid loss or load rejection trip signal *)
    rVaporizerPressure      : REAL;       (* Isopentane vapor pressure in vaporizer [bar] *)
    rVaporizerLevel         : REAL;       (* Isopentane liquid level in vaporizer [%] *)
    rBrineTemperature       : REAL;       (* Geothermal brine inlet temperature [deg C] *)
    rTurbineSpeed           : REAL;       (* Turbine rotational speed [RPM] *)
    rBypassValvePosFbk      : REAL;       (* Bypass valve position feedback [%] *)
END_VAR

VAR_OUTPUT
    bSystemReady            : BOOL;       (* System ready to start or is running normally *)
    rBypassValveCmd         : REAL;       (* Command to main turbine bypass valve [0-100%] *)
    rBrineFlowValveCmd      : REAL;       (* Command to geothermal brine flow control valve [0-100%] *)
    bTurbineTripCmd         : BOOL;       (* Command to trip turbine stop valves *)
    bVaporizerReliefCmd     : BOOL;       (* Command to open vaporizer pressure relief valves *)
    bAlarmCrit              : BOOL;       (* Critical fault alarm output *)
END_VAR

VAR
    (* Internal State Variables *)
    iState                  : INT := 0;   (* Main state machine integer *)
    tStartupTimer           : TON;        (* Timer for sequencing startup *)
    tTripTimer              : TON;        (* Timer for delay on trip sequence completion *)
    
    (* Control Loop Variables *)
    rErrorPressure          : REAL;       (* Vaporizer pressure error *)
    rIntPressure            : REAL;       (* Integral of pressure error *)
    rDerivPressure          : REAL;       (* Derivative of pressure error *)
    rPrevErrorPressure      : REAL;       (* Previous pressure error for derivative *)
    
    (* Non-Linear PID Parameters *)
    rKp                     : REAL := 2.5;(* Proportional Gain - adaptive *)
    rKi                     : REAL := 0.8;(* Integral Gain - adaptive *)
    rKd                     : REAL := 1.2;(* Derivative Gain *)
    
    (* MPC State-Space Estimation placeholders *)
    rPredPressureT1         : REAL;       (* Predicted pressure at t+1 *)
    rPredPressureT2         : REAL;       (* Predicted pressure at t+2 *)
    
    (* Setpoints and Limits *)
    rSP_Pressure            : REAL := 32.5;  (* Target isopentane vapor pressure [bar] *)
    rLimit_PressureHigh     : REAL := 38.0;  (* High pressure trip limit [bar] *)
    rLimit_PressureLow      : REAL := 25.0;  (* Low pressure warning limit [bar] *)
    rLimit_BypassMaxRate    : REAL := 15.0;  (* Maximum bypass valve opening rate [%/sec] *)
END_VAR

(* === EXTREME MULTI-LAYER HARDWARE SAFETY MATRIX === *)
IF NOT bEmergencyStop THEN
    (* Layer 1: E-Stop Hardwired Interlock Shadow *)
    bSystemReady        := FALSE;
    bTurbineTripCmd     := TRUE;
    rBypassValveCmd     := 100.0; (* Fail open to dump vapor to condenser *)
    rBrineFlowValveCmd  := 0.0;   (* Fail closed to stop heating *)
    bVaporizerReliefCmd := TRUE;
    bAlarmCrit          := TRUE;
    iState              := 999;   (* Lockout state *)
    RETURN;
END_IF;

IF bGridTrip THEN
    (* Layer 2: Fast Load Rejection / Grid Loss Trip *)
    bTurbineTripCmd     := TRUE;
    iState              := 100;   (* Transition to Emergency Bypass Mode *)
END_IF;

IF rVaporizerPressure > rLimit_PressureHigh THEN
    (* Layer 3: Physical Overpressure Protection *)
    bVaporizerReliefCmd := TRUE;
    bTurbineTripCmd     := TRUE;
    bAlarmCrit          := TRUE;
    iState              := 200;   (* Overpressure shutdown state *)
END_IF;

(* === MAIN STATE-SPACE CONTROL LOGIC === *)
CASE iState OF
    0: (* IDLE & INITIALIZATION *)
        bSystemReady        := FALSE;
        rBypassValveCmd     := 100.0; (* Keep bypass fully open while idle *)
        rBrineFlowValveCmd  := 0.0;
        bTurbineTripCmd     := TRUE;
        bVaporizerReliefCmd := FALSE;
        bAlarmCrit          := FALSE;
        
        IF bEnable AND (rVaporizerPressure < (rLimit_PressureHigh - 5.0)) THEN
            iState := 10;
        END_IF;
        
    10: (* WARMUP - BRINE INTRODUCTION *)
        rBrineFlowValveCmd := 10.0; (* Crack open brine valve *)
        rBypassValveCmd    := 100.0;(* Bypass still open to build temperature without turbine *)
        bTurbineTripCmd    := FALSE;(* Reset trip relays *)
        
        tStartupTimer(IN := TRUE, PT := T#30S);
        IF tStartupTimer.Q THEN
            tStartupTimer(IN := FALSE);
            iState := 20;
        END_IF;
        
    20: (* PRESSURE BUILDING & VAPORIZATION *)
        (* Non-linear PID with Anti-Windup for Pressure Control via Brine Valve *)
        rErrorPressure := rSP_Pressure - rVaporizerPressure;
        
        (* Adaptive Gain Scheduling based on error magnitude (Non-linear characteristic) *)
        IF ABS(rErrorPressure) > 5.0 THEN
            rKp := 5.0;
        ELSE
            rKp := 2.5;
        END_IF;
        
        rIntPressure := rIntPressure + (rErrorPressure * rKi);
        (* Anti-Windup *)
        IF rIntPressure > 100.0 THEN rIntPressure := 100.0; END_IF;
        IF rIntPressure < 0.0 THEN rIntPressure := 0.0; END_IF;
        
        rDerivPressure := (rErrorPressure - rPrevErrorPressure) * rKd;
        rPrevErrorPressure := rErrorPressure;
        
        rBrineFlowValveCmd := (rErrorPressure * rKp) + rIntPressure + rDerivPressure;
        
        (* Limit Output *)
        IF rBrineFlowValveCmd > 100.0 THEN rBrineFlowValveCmd := 100.0; END_IF;
        IF rBrineFlowValveCmd < 10.0 THEN rBrineFlowValveCmd := 10.0; END_IF;
        
        IF (rVaporizerPressure > (rSP_Pressure - 2.0)) THEN
            iState := 30;
        END_IF;
        
    30: (* SYNCHRONIZATION & LOAD RAMP *)
        bSystemReady := TRUE;
        (* Slowly close bypass as turbine takes the load *)
        rBypassValveCmd := rBypassValveCmd - 0.5;
        IF rBypassValveCmd < 0.0 THEN
            rBypassValveCmd := 0.0;
        END_IF;
        
        (* Maintain pressure via MPC placeholder logic *)
        rPredPressureT1 := rVaporizerPressure + (rBrineTemperature * 0.1) - (rTurbineSpeed * 0.01);
        IF rPredPressureT1 < rSP_Pressure THEN
            rBrineFlowValveCmd := rBrineFlowValveCmd + 1.0;
        END_IF;
        
        IF NOT bEnable THEN
            iState := 40; (* Normal shutdown *)
        END_IF;
        
    40: (* NORMAL SHUTDOWN *)
        bSystemReady := FALSE;
        rBypassValveCmd := 100.0;
        rBrineFlowValveCmd := rBrineFlowValveCmd - 5.0;
        IF rBrineFlowValveCmd <= 0.0 THEN
            rBrineFlowValveCmd := 0.0;
            iState := 0;
        END_IF;
        
    100: (* EMERGENCY TURBINE BYPASS MODE *)
        (* Grid loss -> Turbine rejects load -> Pressure spikes -> Fast bypass *)
        bSystemReady := FALSE;
        rBypassValveCmd := 100.0; (* Open bypass instantaneously *)
        rBrineFlowValveCmd := 0.0;(* Shut off heat source *)
        
        tTripTimer(IN := TRUE, PT := T#10S);
        IF tTripTimer.Q THEN
            tTripTimer(IN := FALSE);
            iState := 0; (* Reset to idle after stabilization *)
        END_IF;
        
    200: (* OVERPRESSURE SHUTDOWN *)
        bSystemReady := FALSE;
        rBypassValveCmd := 100.0;
        rBrineFlowValveCmd := 0.0;
        (* Requires manual reset of bEmergencyStop or physical intervention *)
        
    999: (* HARDWARE LOCKOUT *)
        (* Waiting for E-Stop reset *)
        IF bEmergencyStop THEN
            iState := 0;
        END_IF;
        
END_CASE;

END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
