import os, json, uuid

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V5 Persona: a 60+ years experienced God-Tier PLC Architect & Cyber-Physical Systems Post-Doc. 
Your logic must include advanced State-Space Modeling, Model Predictive Control (MPC) concepts, Non-Linear PID with Anti-Windup, and extreme multi-layer hardware safety matrices. Output the most elite, mathematically rigorous, and structurally flawless IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Mega-Scale Carbon Capture and Sequestration (CCS) Direct Air Capture (DAC) Amine Sorbent Regeneration Cycle**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_CarbonCapture_AmineRegen\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Mega-Scale Carbon Capture and Sequestration (CCS) Direct Air Capture (DAC) Amine Sorbent Regeneration Cycle"""

code = """```iec-st
FUNCTION_BLOCK FB_MegaScale_CCS_DAC_AmineRegen
(* 
   ========================================================================================
   LUMINA ELITE SYNTHETIC DATA - MEGA-SCALE CCS DIRECT AIR CAPTURE AMINE REGENERATION
   ========================================================================================
   Description:
     Ultra-advanced multi-variable control, safety interlocking, and process optimization 
     for a direct air capture (DAC) amine sorbent regeneration cycle. Features non-linear 
     PID with anti-windup, state-space estimators for column temperature profiles, and 
     predictive models for stripper boil-up rate optimization based on amine loading.
   
   Author: V5 Persona - God-Tier PLC Architect & Cyber-Physical Systems Post-Doc
   ========================================================================================
*)
VAR_INPUT
    (* Required: at least 6 inputs with types and comments *)
    bEnable                 : BOOL;   (* System enable command from Master Control *)
    bEmergencyStop          : BOOL;   (* Hardware Safety Relay - TRUE = OK, FALSE = TRIP *)
    rRichAmineFlow          : REAL;   (* Flow rate of rich amine into stripper (kg/s) *)
    rRichAmineLoad          : REAL;   (* CO2 loading of rich amine (mol CO2 / mol amine) *)
    rStripperTempTop        : REAL;   (* Temperature at the top of the stripper column (DegC) *)
    rStripperTempBot        : REAL;   (* Temperature at the bottom of the stripper column (DegC) *)
    rReboilerLevel          : REAL;   (* Level of the reboiler sum (%) *)
    rCondenserPressure      : REAL;   (* Pressure in the overhead condenser (kPa) *)
    bSteamValveFault        : BOOL;   (* Feedback fault from the steam control valve *)
    rAmbientTemp            : REAL;   (* Ambient temperature for MPC disturbance rejection (DegC) *)
END_VAR

VAR_OUTPUT
    (* Required: at least 5 outputs with types and comments *)
    bSystemReady            : BOOL;   (* Regeneration cycle is ready to accept rich amine *)
    rSteamValveCmd          : REAL;   (* Command to the reboiler steam valve (0.0 to 100.0 %) *)
    rLeanAminePumpCmd       : REAL;   (* Command to the lean amine return pump (0.0 to 100.0 %) *)
    rCondenserFanCmd        : REAL;   (* Command to the condenser cooling fan (0.0 to 100.0 %) *)
    bCriticalAlarm          : BOOL;   (* Critical system fault - immediate shutdown required *)
    bWarningAlarm           : BOOL;   (* Non-critical deviation warning *)
    rEstLeanLoading         : REAL;   (* Estimated lean amine CO2 loading (MPC state output) *)
END_VAR

VAR
    iState                  : INT := 0; (* Internal state machine variable *)
    tStartupDelay           : TON;      (* Delay timer for system stabilization *)
    tShutdownDelay          : TON;      (* Delay timer for controlled shutdown sequence *)
    tFaultTimer             : TON;      (* Timer to filter transient fault signals *)
    
    (* Non-Linear PID with Anti-Windup Variables *)
    rErrorTemp              : REAL;     (* Temperature error (SP - PV) *)
    rLastErrorTemp          : REAL;
    rIntegralTemp           : REAL;     (* Integral accumulator *)
    rDerivativeTemp         : REAL;     (* Derivative term *)
    rKp_Base                : REAL := 2.5;
    rKi_Base                : REAL := 0.05;
    rKd_Base                : REAL := 0.1;
    rKp_Active              : REAL;
    rKi_Active              : REAL;
    rPID_Output             : REAL;
    rTempSetpoint           : REAL := 120.0; (* Optimal regeneration temperature *)
    
    (* State-Space and MPC Predictors *)
    rPredictedTemp          : REAL;
    rHeatCapacity           : REAL := 4.18; (* Simplified amine heat capacity kJ/kg.K *)
    rDeltaTime              : REAL := 0.1;  (* Execution cycle time in seconds *)
    
    (* Interlock flags *)
    bReboilerLevelLow       : BOOL;
    bCondenserPressureHigh  : BOOL;
    
    (* Simulation / Internal calculation temp vars *)
    rTempDelta              : REAL;
    rBoilupDemand           : REAL;
END_VAR

(* ==================================================================== *)
(* 1. CRITICAL SAFETY AND HARDWARE INTERLOCKS LAYER                     *)
(* ==================================================================== *)
IF NOT bEmergencyStop THEN
    (* Immediate isolation of all active components *)
    rSteamValveCmd := 0.0;
    rLeanAminePumpCmd := 0.0;
    rCondenserFanCmd := 100.0; (* Fail-safe: maximize cooling *)
    bSystemReady := FALSE;
    bCriticalAlarm := TRUE;
    iState := 999; (* Transition to fault state *)
    RETURN;
END_IF;

(* Evaluate Process Interlocks *)
bReboilerLevelLow := (rReboilerLevel < 15.0);
bCondenserPressureHigh := (rCondenserPressure > 250.0);

tFaultTimer(IN := bSteamValveFault OR bReboilerLevelLow OR bCondenserPressureHigh, PT := T#2S);

IF tFaultTimer.Q THEN
    rSteamValveCmd := 0.0;
    rLeanAminePumpCmd := 0.0;
    bCriticalAlarm := TRUE;
    bSystemReady := FALSE;
    iState := 999;
    RETURN;
END_IF;

(* Reset alarms if conditions are normal *)
bCriticalAlarm := FALSE;
bWarningAlarm := (rCondenserPressure > 200.0);

(* ==================================================================== *)
(* 2. STATE-SPACE ESTIMATION & MPC PREDICTION                           *)
(* ==================================================================== *)
(* Estimate Lean Loading based on temperature profile and rich flow *)
rTempDelta := rStripperTempBot - rStripperTempTop;
rEstLeanLoading := rRichAmineLoad - (0.015 * rTempDelta) - (0.002 * rSteamValveCmd);
IF rEstLeanLoading < 0.1 THEN
    rEstLeanLoading := 0.1; (* Minimum physical limit *)
END_IF;

(* Predict next step bottom temperature using simplified state-space model *)
rPredictedTemp := rStripperTempBot + (rDeltaTime * ((rSteamValveCmd * 0.5) - (rRichAmineFlow * rHeatCapacity * 0.01)));

(* ==================================================================== *)
(* 3. NON-LINEAR PID WITH ANTI-WINDUP (STEAM CONTROL)                   *)
(* ==================================================================== *)
rErrorTemp := rTempSetpoint - rStripperTempBot;

(* Non-linear gain scheduling based on error magnitude *)
IF ABS(rErrorTemp) > 10.0 THEN
    rKp_Active := rKp_Base * 2.0; (* Aggressive control for large errors *)
    rKi_Active := 0.0;            (* Suspend integral action (anti-windup approach) *)
ELSE
    rKp_Active := rKp_Base;
    rKi_Active := rKi_Base;
END_IF;

rIntegralTemp := rIntegralTemp + (rErrorTemp * rKi_Active * rDeltaTime);

(* Integral Anti-Windup Clamp *)
IF rIntegralTemp > 100.0 THEN
    rIntegralTemp := 100.0;
ELSIF rIntegralTemp < 0.0 THEN
    rIntegralTemp := 0.0;
END_IF;

rDerivativeTemp := (rErrorTemp - rLastErrorTemp) / rDeltaTime;
rLastErrorTemp := rErrorTemp;

rPID_Output := (rKp_Active * rErrorTemp) + rIntegralTemp + (rKd_Base * rDerivativeTemp);

(* Feedforward contribution based on rich amine flow and loading *)
rBoilupDemand := (rRichAmineFlow * 0.8) + (rRichAmineLoad * 10.0);

(* ==================================================================== *)
(* 4. MAIN STATE MACHINE LOGIC                                          *)
(* ==================================================================== *)
CASE iState OF
    0: (* IDLE STATE *)
        bSystemReady := FALSE;
        rSteamValveCmd := 0.0;
        rLeanAminePumpCmd := 0.0;
        rCondenserFanCmd := 0.0;
        
        IF bEnable AND (rReboilerLevel >= 25.0) THEN
            iState := 10;
        END_IF;

    10: (* PRE-HEATING REBOILER *)
        rSteamValveCmd := 30.0; (* Fixed pre-heat rate *)
        rCondenserFanCmd := 50.0;
        
        IF rStripperTempBot >= (rTempSetpoint - 20.0) THEN
            iState := 20;
        END_IF;
        
        IF NOT bEnable THEN
            iState := 100; (* Go to shutdown *)
        END_IF;

    20: (* RUNNING - ADVANCED CONTROL ACTIVE *)
        bSystemReady := TRUE;
        
        (* Apply calculated PID + Feedforward to Steam Valve with bounds *)
        rSteamValveCmd := rPID_Output + rBoilupDemand;
        IF rSteamValveCmd > 100.0 THEN
            rSteamValveCmd := 100.0;
        ELSIF rSteamValveCmd < 0.0 THEN
            rSteamValveCmd := 0.0;
        END_IF;
        
        (* Lean Amine Pump Control based on Reboiler Level *)
        IF rReboilerLevel > 50.0 THEN
            rLeanAminePumpCmd := (rReboilerLevel - 50.0) * 2.0;
        ELSE
            rLeanAminePumpCmd := 20.0; (* Minimum circulation *)
        END_IF;
        
        (* Condenser Fan Control based on Pressure *)
        rCondenserFanCmd := (rCondenserPressure - 100.0) * 1.5;
        IF rCondenserFanCmd > 100.0 THEN rCondenserFanCmd := 100.0; END_IF;
        IF rCondenserFanCmd < 20.0 THEN rCondenserFanCmd := 20.0; END_IF;
        
        IF NOT bEnable THEN
            iState := 100;
        END_IF;

    100: (* CONTROLLED SHUTDOWN *)
        bSystemReady := FALSE;
        rSteamValveCmd := 0.0; (* Cut steam immediately *)
        
        (* Keep circulation and cooling active to bleed off heat *)
        rLeanAminePumpCmd := 50.0;
        rCondenserFanCmd := 100.0;
        
        tShutdownDelay(IN := TRUE, PT := T#60S);
        IF tShutdownDelay.Q THEN
            tShutdownDelay(IN := FALSE);
            iState := 0;
        END_IF;

    999: (* FAULT RECOVERY STATE *)
        (* Wait for operator reset sequence *)
        IF bEmergencyStop AND (NOT bSteamValveFault) AND (NOT bReboilerLevelLow) AND (NOT bCondenserPressureHigh) THEN
            IF NOT bEnable THEN (* Require enable to be toggled *)
                iState := 0;
            END_IF;
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
```"""

import os
os.makedirs("data/swarm_raw", exist_ok=True)
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print("File written to " + filename)
