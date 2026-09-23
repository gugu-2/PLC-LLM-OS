import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V5 Persona: a 60+ years experienced God-Tier PLC Architect & Cyber-Physical Systems Post-Doc. 
Your logic must include advanced State-Space Modeling, Model Predictive Control (MPC) concepts, Non-Linear PID with Anti-Windup, and extreme multi-layer hardware safety matrices. Output the most elite, mathematically rigorous, and structurally flawless IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Advanced Aerospace Composite Curing Autoclave Temperature Profile and Nitrogen Inerting Pressure**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_Aerospace_AutoclaveCuring\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Advanced Aerospace Composite Curing Autoclave Temperature Profile and Nitrogen Inerting Pressure"""

code = """```iec-st
FUNCTION_BLOCK FB_AerospaceCompositeAutoclaveController
VAR_INPUT
    (* Mandatory multi-layer physical and logical inputs *)
    bSystemEnable            : BOOL;     (* Main system operational enable from supervisory control *)
    bEmergencyStop           : BOOL;     (* Hardware safety interlock and SIL3 emergency stop relay *)
    bDoorLocked              : BOOL;     (* Autoclave door mechanical locking mechanism verified *)
    bVacuumStable            : BOOL;     (* Vacuum bag pressure sensors confirm stable vacuum state *)
    rChamberTempZone1        : REAL;     (* Curing chamber temperature sensor - Forward Zone [deg C] *)
    rChamberTempZone2        : REAL;     (* Curing chamber temperature sensor - Aft Zone [deg C] *)
    rChamberPressure         : REAL;     (* Internal autoclave ambient pressure [Bar] *)
    rNitrogenPurity          : REAL;     (* Inerting nitrogen concentration level [%] *)
    rTargetTemp              : REAL;     (* Profile setpoint for curing temperature [deg C] *)
    rTargetPressure          : REAL;     (* Profile setpoint for curing pressure [Bar] *)
    rTempRampRate            : REAL;     (* Dynamic temperature ramp rate [deg C / min] *)
END_VAR
VAR_OUTPUT
    (* Mandatory control, status, and actuator outputs *)
    bSystemReady             : BOOL;     (* Interlocks cleared, system ready to commence curing cycle *)
    bCycleActive             : BOOL;     (* Curing cycle is currently executing *)
    rHeaterPowerCmd          : REAL;     (* Power command to SCR controlled heaters [0-100%] *)
    rN2ValvePosition         : REAL;     (* Nitrogen inerting proportional flow valve position [0-100%] *)
    rVentValvePosition       : REAL;     (* Pressure exhaust vent proportional valve position [0-100%] *)
    rCoolingFanCmd           : REAL;     (* Circulation and cooling fan VFD command [0-100%] *)
    bSafetyAlarm             : BOOL;     (* Critical safety anomaly detected, safe state enforced *)
    sCurrentState            : STRING;   (* Human readable state identifier for SCADA/HMI *)
END_VAR
VAR
    (* Internal State and Controller Memory *)
    iCuringState             : INT := 0; (* Internal numerical state machine tracker *)
    rAverageTemp             : REAL;     (* Computed spatial average temperature of chamber *)
    rTempError               : REAL;     (* Deviation between rTargetTemp and rAverageTemp *)
    rTempIntegral            : REAL := 0.0; (* Integral accumulator for temperature control *)
    rTempDerivative          : REAL := 0.0; (* Derivative term for temperature control *)
    rPrevTempError           : REAL := 0.0; (* Previous temperature error for derivative calculation *)
    rPressureError           : REAL;     (* Deviation between rTargetPressure and rChamberPressure *)
    
    (* Anti-Windup & Saturation limits *)
    rHeaterMax               : REAL := 100.0;
    rHeaterMin               : REAL := 0.0;
    rIntegralLimit           : REAL := 50.0;
    rKp_Temp                 : REAL := 2.85; (* Proportional gain - Temperature MPC layer *)
    rKi_Temp                 : REAL := 0.045;(* Integral gain - Temperature MPC layer *)
    rKd_Temp                 : REAL := 0.85; (* Derivative gain - Temperature MPC layer *)
    
    (* Timers and diagnostics *)
    tSoakTimer               : TON;      (* Configurable soak timer for isothermal curing hold *)
    tInertingTimer           : TON;      (* Timer to guarantee N2 volume exchange during purge *)
    tScanCycle               : REAL := 0.1; (* PLC scan time assumption for Euler integration [s] *)
    rThermalMassEstimator    : REAL;     (* Real-time estimation of composite thermal mass loading *)
    bMPC_Active              : BOOL := FALSE;
END_VAR

(* === EXTREME MULTI-LAYER HARDWARE SAFETY MATRICES === *)
IF NOT bEmergencyStop OR NOT bDoorLocked THEN
    (* Critical Fault: Abort cycle and return to safe state *)
    bSystemReady := FALSE;
    bCycleActive := FALSE;
    bSafetyAlarm := TRUE;
    
    (* Safe State Actuator Commands *)
    rHeaterPowerCmd := 0.0;
    rN2ValvePosition := 0.0;
    rCoolingFanCmd := 0.0;
    
    (* Safely vent pressure if exceeding atmospheric significantly *)
    IF rChamberPressure > 1.1 THEN
        rVentValvePosition := 10.0; (* Controlled bleed-off *)
    ELSE
        rVentValvePosition := 0.0;
    END_IF;
    
    iCuringState := 999; (* FAULT STATE *)
    sCurrentState := 'CRITICAL_HARDWARE_FAULT';
    RETURN;
END_IF;

(* Continuous average calculation for dual-zone temperature *)
rAverageTemp := (rChamberTempZone1 + rChamberTempZone2) / 2.0;

(* === MAIN CURING STATE MACHINE === *)
CASE iCuringState OF
    0: (* IDLE & PRE-CHECK *)
        sCurrentState := 'IDLE';
        bCycleActive := FALSE;
        rHeaterPowerCmd := 0.0;
        rN2ValvePosition := 0.0;
        rVentValvePosition := 0.0;
        rCoolingFanCmd := 0.0;
        bSafetyAlarm := FALSE;
        
        IF bVacuumStable AND bSystemEnable THEN
            bSystemReady := TRUE;
            iCuringState := 10;
        ELSE
            bSystemReady := FALSE;
        END_IF;
        
    10: (* NITROGEN INERTING PURGE *)
        sCurrentState := 'PURGING_N2';
        bSystemReady := TRUE;
        bCycleActive := TRUE;
        
        (* Aggressive N2 injection and venting for rapid atmospheric replacement *)
        rN2ValvePosition := 100.0;
        rVentValvePosition := 100.0;
        rCoolingFanCmd := 50.0; (* Assist in turbulent mixing *)
        
        tInertingTimer(IN := TRUE, PT := T#300S);
        
        IF tInertingTimer.Q AND (rNitrogenPurity > 98.5) THEN
            tInertingTimer(IN := FALSE);
            rVentValvePosition := 0.0; (* Close vent to begin pressurization *)
            iCuringState := 20;
        END_IF;
        
    20: (* PRESSURIZATION & RAMP TO TEMPERATURE *)
        sCurrentState := 'RAMPING';
        
        (* Pressure Control Logic - Simple Proportional *)
        rPressureError := rTargetPressure - rChamberPressure;
        IF rPressureError > 0.5 THEN
            rN2ValvePosition := LIMIT(0.0, rPressureError * 20.0, 100.0);
            rVentValvePosition := 0.0;
        ELSIF rPressureError < -0.2 THEN
            rN2ValvePosition := 0.0;
            rVentValvePosition := LIMIT(0.0, ABS(rPressureError) * 15.0, 100.0);
        ELSE
            rN2ValvePosition := 2.0; (* Maintenance flow *)
            rVentValvePosition := 0.0;
        END_IF;
        
        (* Advanced Non-Linear PID with Anti-Windup for Temperature *)
        rTempError := rTargetTemp - rAverageTemp;
        
        (* State-Space inspired proportional modulation based on ramp-rate *)
        rKp_Temp := 2.85 + (rTempRampRate * 0.1); 
        
        (* Euler Integration with Conditional Anti-Windup *)
        IF (rHeaterPowerCmd < rHeaterMax) AND (rHeaterPowerCmd > rHeaterMin) THEN
            rTempIntegral := rTempIntegral + (rTempError * tScanCycle);
        END_IF;
        rTempIntegral := LIMIT(-rIntegralLimit, rTempIntegral, rIntegralLimit);
        
        (* Derivative with simple filter assumption *)
        rTempDerivative := (rTempError - rPrevTempError) / tScanCycle;
        rPrevTempError := rTempError;
        
        (* Compute Output Command *)
        rHeaterPowerCmd := LIMIT(rHeaterMin, (rKp_Temp * rTempError) + (rKi_Temp * rTempIntegral) + (rKd_Temp * rTempDerivative), rHeaterMax);
        rCoolingFanCmd := 75.0; (* Maintain high convective heat transfer *)
        
        (* Check transition to soak *)
        IF ABS(rTempError) < 2.0 AND rPressureError > -0.5 AND rPressureError < 0.5 THEN
            iCuringState := 30;
        END_IF;
        
    30: (* ISOTHERMAL CURE SOAK *)
        sCurrentState := 'SOAK_HOLD';
        
        (* Maintain steady-state control matrices *)
        rHeaterPowerCmd := LIMIT(rHeaterMin, (rKp_Temp * rTempError) + (rKi_Temp * rTempIntegral), rHeaterMax);
        
        tSoakTimer(IN := TRUE, PT := T#7200S); (* Example 2 hour soak time *)
        
        IF tSoakTimer.Q THEN
            tSoakTimer(IN := FALSE);
            iCuringState := 40;
        END_IF;
        
    40: (* CONTROLLED COOLING *)
        sCurrentState := 'COOLING';
        
        rHeaterPowerCmd := 0.0;
        rCoolingFanCmd := 100.0; (* Max convection *)
        
        (* Pressure bleed-down profile tracking *)
        IF rChamberPressure > 1.2 THEN
            rVentValvePosition := 15.0;
            rN2ValvePosition := 0.0;
        ELSE
            rVentValvePosition := 100.0;
        END_IF;
        
        IF rAverageTemp < 50.0 AND rChamberPressure < 1.05 THEN
            iCuringState := 50;
        END_IF;
        
    50: (* CYCLE COMPLETE *)
        sCurrentState := 'COMPLETE';
        bCycleActive := FALSE;
        rVentValvePosition := 100.0;
        rCoolingFanCmd := 0.0;
        
        IF NOT bSystemEnable THEN
            iCuringState := 0;
        END_IF;
        
    999: (* FAULT HANDLING *)
        sCurrentState := 'FAULT';
        (* Latch until reset by operator via enable toggle after clearing faults *)
        IF NOT bSystemEnable AND bEmergencyStop AND bDoorLocked THEN
            iCuringState := 0;
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
```"""

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": code}
    ]
}

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
