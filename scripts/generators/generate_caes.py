import json, uuid, os

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Utility-Scale Compressed Air Energy Storage (CAES) Isothermal Expansion**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., High-pressure (100 bar) cavern air adiabatic to isothermal conversion, multi-stage spray liquid piston synchronization, and grid frequency active inertial response). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_CAES_IsothermalExpansion\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Utility-Scale Compressed Air Energy Storage (CAES) Isothermal Expansion

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_CAES_IsothermalExpansion
VAR_INPUT
    (* Core operational signals *)
    bEnable                 : BOOL;     (* System master enable signal for the expansion phase *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal; TRUE = Safe, FALSE = E-STOP *)
    bGridFrequencyActive    : BOOL;     (* Enable active inertial response to grid frequency deviations *)
    
    (* High-pressure cavern conditions *)
    rCavernPressure         : REAL;     (* Current cavern pressure [bar], nominal 100 bar *)
    rCavernTemperature      : REAL;     (* Current cavern temperature [deg C] *)
    
    (* Multi-stage spray liquid piston feedback *)
    rLiquidPistonLevel      : REAL;     (* Current level of the heat exchange fluid in piston [m] *)
    rHeatExchangeTemp       : REAL;     (* Temperature of the spray fluid [deg C] *)
    rGridFrequency          : REAL;     (* Grid frequency [Hz], nominal 50.0 or 60.0 Hz *)
    
    (* Operator setpoints *)
    rTargetPowerOut         : REAL;     (* Desired target power output [MW] *)
END_VAR

VAR_OUTPUT
    (* Status and safety *)
    bSystemReady            : BOOL;     (* System ready status for isothermal expansion *)
    bAlarm                  : BOOL;     (* Fault alarm output (general fault) *)
    
    (* Actuator control commands *)
    rExpansionValveCmd      : REAL;     (* Command for the high-pressure air expansion valve [0-100%] *)
    rSprayPumpSpeedCmd      : REAL;     (* Command for the isothermal spray pump VFD [0-100%] *)
    rGeneratorTorqueCmd     : REAL;     (* Command for generator torque (active power control) [Nm] *)
    
    (* Process monitoring *)
    iCurrentState           : INT;      (* Current state of the expansion control state machine *)
    rCalculatedEfficiency   : REAL;     (* Estimated isothermal efficiency [%] *)
END_VAR

VAR
    (* Internal state variables *)
    iState                  : INT := 0; (* 0: IDLE, 10: PRE_PRESSURIZE, 20: SYNCHRONIZING, 30: RUNNING, 99: FAULT *)
    tStartupDelay           : TON;
    tStabilizationTimer     : TON;
    
    (* Control algorithm constants and variables *)
    rKp_Valve               : REAL := 2.5;
    rKi_Valve               : REAL := 0.12;
    rKd_Valve               : REAL := 0.05;
    rError_Valve            : REAL := 0.0;
    rIntegral_Valve         : REAL := 0.0;
    rPrevError_Valve        : REAL := 0.0;
    
    rTargetIsothermalTemp   : REAL := 25.0; (* [deg C] Optimal temperature to maintain near-isothermal expansion *)
    rTempError              : REAL := 0.0;
    
    rNominalGridFrequency   : REAL := 50.0; (* Hz *)
    rDroopCoefficient       : REAL := 4.0;  (* % droop for primary frequency response *)
    rPowerSetPointAdj       : REAL := 0.0;
END_VAR

(* === MAIN LOGIC === *)
(* 1. Safety Interlocks and E-Stop Handling *)
IF NOT bEmergencyStop THEN
    bSystemReady        := FALSE;
    bAlarm              := TRUE;
    iState              := 99; (* FAULT STATE *)
    rExpansionValveCmd  := 0.0;
    rSprayPumpSpeedCmd  := 0.0;
    rGeneratorTorqueCmd := 0.0;
    iCurrentState       := iState;
    RETURN;
END_IF;

(* 2. Grid Frequency Active Inertial Response (Primary Frequency Control) *)
IF bGridFrequencyActive THEN
    (* Calculate frequency deviation and apply droop control *)
    IF ABS(rNominalGridFrequency - rGridFrequency) > 0.05 THEN
        (* Increase power if frequency drops, decrease if frequency rises *)
        rPowerSetPointAdj := ((rNominalGridFrequency - rGridFrequency) / rNominalGridFrequency) * (100.0 / rDroopCoefficient) * rTargetPowerOut;
    ELSE
        rPowerSetPointAdj := 0.0;
    END_IF;
ELSE
    rPowerSetPointAdj := 0.0;
END_IF;

(* 3. State Machine for CAES Isothermal Expansion *)
CASE iState OF
    0: (* IDLE - Waiting for start command *)
        bSystemReady        := TRUE;
        bAlarm              := FALSE;
        rExpansionValveCmd  := 0.0;
        rSprayPumpSpeedCmd  := 0.0;
        rGeneratorTorqueCmd := 0.0;
        
        IF bEnable AND rCavernPressure > 30.0 THEN
            bSystemReady := FALSE;
            iState := 10;
        END_IF;

    10: (* PRE_PRESSURIZE - Prime the liquid piston and stabilize heat exchange fluid *)
        (* Run spray pumps at minimum safe speed to establish flow before air enters *)
        rSprayPumpSpeedCmd := 25.0; 
        tStartupDelay(IN := TRUE, PT := T#10S);
        
        IF tStartupDelay.Q THEN
            tStartupDelay(IN := FALSE);
            iState := 20;
        END_IF;

    20: (* SYNCHRONIZING - Ramp up valves and synchronize with grid *)
        (* Slowly open expansion valve and adjust spray based on cavern temperature *)
        rExpansionValveCmd := MIN(rExpansionValveCmd + 0.5, 30.0);
        rSprayPumpSpeedCmd := 50.0;
        
        tStabilizationTimer(IN := TRUE, PT := T#15S);
        IF tStabilizationTimer.Q THEN
            tStabilizationTimer(IN := FALSE);
            iState := 30;
        END_IF;
        
        IF NOT bEnable THEN
            iState := 0;
        END_IF;

    30: (* RUNNING - Steady state isothermal expansion and power generation *)
        (* Valve PID control based on power demand (adjusted for grid frequency) *)
        rError_Valve := (rTargetPowerOut + rPowerSetPointAdj) - (rExpansionValveCmd * 1.5); (* Simplified power model *)
        rIntegral_Valve := rIntegral_Valve + rError_Valve;
        rExpansionValveCmd := (rKp_Valve * rError_Valve) + (rKi_Valve * rIntegral_Valve) + (rKd_Valve * (rError_Valve - rPrevError_Valve));
        
        (* Saturate valve command 0-100% *)
        IF rExpansionValveCmd > 100.0 THEN rExpansionValveCmd := 100.0; END_IF;
        IF rExpansionValveCmd < 0.0 THEN rExpansionValveCmd := 0.0; END_IF;
        
        rPrevError_Valve := rError_Valve;
        
        (* Spray pump speed control for isothermal behavior *)
        rTempError := rTargetIsothermalTemp - rHeatExchangeTemp;
        rSprayPumpSpeedCmd := 50.0 - (rTempError * 2.0); (* Increase flow if too cold, decrease if too hot, simplified *)
        IF rSprayPumpSpeedCmd > 100.0 THEN rSprayPumpSpeedCmd := 100.0; END_IF;
        IF rSprayPumpSpeedCmd < 20.0 THEN rSprayPumpSpeedCmd := 20.0; END_IF;
        
        (* Generator torque command correlates with valve opening in this simplified model *)
        rGeneratorTorqueCmd := rExpansionValveCmd * 10.0;
        
        (* Calculate theoretical efficiency based on heat exchange deviation *)
        rCalculatedEfficiency := 100.0 - ABS(rTempError);
        
        IF NOT bEnable THEN
            iState := 0;
            rIntegral_Valve := 0.0;
        END_IF;
        
        (* Safety check on cavern pressure *)
        IF rCavernPressure < 20.0 THEN
            bAlarm := TRUE;
            iState := 99;
        END_IF;

    99: (* FAULT STATE *)
        rExpansionValveCmd  := 0.0;
        rSprayPumpSpeedCmd  := 0.0;
        rGeneratorTorqueCmd := 0.0;
        bSystemReady        := FALSE;
        
        IF bEnable = FALSE AND bEmergencyStop = TRUE AND rCavernPressure >= 20.0 THEN
            bAlarm := FALSE;
            iState := 0;
        END_IF;

END_CASE;

(* Update outputs *)
iCurrentState := iState;

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

print(f"Saved to {filename}")
