import json, uuid, os

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Industrial Chocolate Enrobing and Tempering Viscosity Multi-Zone Temperature Control**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_Chocolate_TemperingControl\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Industrial Chocolate Enrobing and Tempering Viscosity Multi-Zone Temperature Control

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_ChocolateTemperingControl
(* 
  =============================================================================
  LUMINA ELITE AUTOMATION - INDUSTRIAL CHOCOLATE ENROBING AND TEMPERING
  Module: Viscosity Multi-Zone Temperature Control 
  Description: Ultra-precise, multi-zone PID temperature regulation with 
               real-time viscosity compensation, noise filtering, and 
               Category 4 safety interlock validation for continuous chocolate tempering.
  =============================================================================
*)
VAR_INPUT
    (* Required: at least 4-8 physical inputs with types and comments *)
    bEnable             : BOOL;     (* System enable signal from central SCADA *)
    bEmergencyStop      : BOOL;     (* Safety relay OK signal (Active High = Safe) *)
    rTempZone1_C        : REAL;     (* Enrobing Zone 1 Pre-heat Temp [degC] *)
    rTempZone2_C        : REAL;     (* Enrobing Zone 2 Tempering Temp [degC] *)
    rViscosity_cP       : REAL;     (* Measured Chocolate Viscosity [Centipoise] *)
    rMassFlow_kg_h      : REAL;     (* Mass flow rate of chocolate [kg/h] *)
    bCoolingWaterOK     : BOOL;     (* Cooling water jacket flow confirmation *)
    bAgitatorInterlock  : BOOL;     (* Agitator mechanical seal interlock state *)
END_VAR
VAR_OUTPUT
    (* Required: at least 3-6 outputs with types and comments *)
    bSystemReady        : BOOL;     (* System is properly tempered and ready for production *)
    rHeaterOutputZ1_pct : REAL;     (* Heater 1 Control Output [0-100%] *)
    rHeaterOutputZ2_pct : REAL;     (* Heater 2 Control Output [0-100%] *)
    rCoolingValve_pct   : REAL;     (* Cooling water valve output [0-100%] *)
    bAgitatorRun        : BOOL;     (* Command to run the tempering agitator *)
    bAlarm              : BOOL;     (* Global Fault / Alarm active flag *)
    iErrorCode          : INT;      (* Active Error Code for SCADA diagnostics *)
END_VAR
VAR
    (* Internal state variables *)
    iState              : INT := 0; (* Main State Machine Step *)
    tTimer              : TON;      (* General purpose state transition timer *)
    
    (* Filtering Variables for Viscosity *)
    rViscosityFiltered  : REAL := 0.0;
    rViscosityBuffer    : ARRAY[0..9] OF REAL;
    iFilterIndex        : INT := 0;
    rViscositySum       : REAL := 0.0;

    (* PID Controller Variables - Zone 1 & 2 *)
    rSetpointZ1         : REAL := 31.5; (* Tempering optimal temp Z1 (Beta crystals) *)
    rSetpointZ2         : REAL := 32.0; (* Tempering optimal temp Z2 (Working state) *)
    rErrorZ1            : REAL;
    rErrorZ2            : REAL;
    rIntegralZ1         : REAL;
    rIntegralZ2         : REAL;
    rKp                 : REAL := 2.85;
    rKi                 : REAL := 0.04;

    (* Safety State *)
    bSafetyOK           : BOOL;
END_VAR

(* === MAIN LOGIC === *)

(* 1. Safety Interlocks and Hard Stops Evaluation *)
bSafetyOK := bEmergencyStop AND bCoolingWaterOK AND bAgitatorInterlock;

IF NOT bSafetyOK THEN
    iState := 999; (* FORCE FAULT STATE *)
END_IF;

(* 2. Sensor Noise Filtering: 10-Sample Moving Average for Viscosity *)
rViscositySum := rViscositySum - rViscosityBuffer[iFilterIndex];
rViscosityBuffer[iFilterIndex] := rViscosity_cP;
rViscositySum := rViscositySum + rViscosityBuffer[iFilterIndex];
iFilterIndex := (iFilterIndex + 1) MOD 10;
rViscosityFiltered := rViscositySum / 10.0;

(* 3. Multi-Zone Process State Machine *)
CASE iState OF
    0: (* IDLE *)
        bSystemReady := FALSE;
        bAgitatorRun := FALSE;
        rHeaterOutputZ1_pct := 0.0;
        rHeaterOutputZ2_pct := 0.0;
        rCoolingValve_pct := 0.0;
        bAlarm := FALSE;
        iErrorCode := 0;
        
        (* Reset PID Integrators *)
        rIntegralZ1 := 0.0;
        rIntegralZ2 := 0.0;
        
        IF bEnable AND bSafetyOK THEN
            iState := 10; (* Transition to PREHEAT *)
        END_IF;

    10: (* PREHEAT PHASE - AGGRESSIVE RAMP *)
        (* Simple Proportional Control for Fast Preheat *)
        rErrorZ1 := rSetpointZ1 - rTempZone1_C;
        rErrorZ2 := rSetpointZ2 - rTempZone2_C;
        
        IF rErrorZ1 > 0.5 THEN
            rHeaterOutputZ1_pct := 100.0;
        ELSE
            rHeaterOutputZ1_pct := 0.0;
        END_IF;

        IF rErrorZ2 > 0.5 THEN
            rHeaterOutputZ2_pct := 100.0;
        ELSE
            rHeaterOutputZ2_pct := 0.0;
        END_IF;
        
        (* Ensure mass movement to prevent burning *)
        bAgitatorRun := TRUE;

        (* Wait for Zone 1 and 2 to reach near-setpoint *)
        IF (rTempZone1_C >= (rSetpointZ1 - 0.5)) AND (rTempZone2_C >= (rSetpointZ2 - 0.5)) THEN
            tTimer(IN := TRUE, PT := T#45S);
            IF tTimer.Q THEN
                tTimer(IN := FALSE);
                iState := 20; (* Transition to STABILIZATION & PID CONTROL *)
            END_IF;
        ELSE
            tTimer(IN := FALSE, PT := T#45S);
        END_IF;

    20: (* RUNNING / TEMPERING ACTIVE (PID + VISCOSITY COMPENSATION) *)
        bSystemReady := TRUE;
        bAgitatorRun := TRUE;
        
        (* Calculate Errors *)
        rErrorZ1 := rSetpointZ1 - rTempZone1_C;
        rErrorZ2 := rSetpointZ2 - rTempZone2_C;
        
        (* Integrate Errors with Anti-Windup *)
        rIntegralZ1 := rIntegralZ1 + rErrorZ1;
        rIntegralZ2 := rIntegralZ2 + rErrorZ2;
        
        IF rIntegralZ1 > 1500.0 THEN rIntegralZ1 := 1500.0; END_IF;
        IF rIntegralZ1 < -1500.0 THEN rIntegralZ1 := -1500.0; END_IF;
        IF rIntegralZ2 > 1500.0 THEN rIntegralZ2 := 1500.0; END_IF;
        IF rIntegralZ2 < -1500.0 THEN rIntegralZ2 := -1500.0; END_IF;
        
        (* PID Calculation *)
        rHeaterOutputZ1_pct := (rErrorZ1 * rKp) + (rIntegralZ1 * rKi);
        rHeaterOutputZ2_pct := (rErrorZ2 * rKp) + (rIntegralZ2 * rKi);
        
        (* Advanced Viscosity Compensation Override *)
        (* If viscosity exceeds threshold (thick), trim cooling and boost heat slightly *)
        IF rViscosityFiltered > 16500.0 THEN
            rHeaterOutputZ1_pct := rHeaterOutputZ1_pct + 10.0;
            rCoolingValve_pct := 0.0;
        ELSIF rViscosityFiltered < 9500.0 THEN
            (* If viscosity is too low (thin), apply proportional cooling jacket control *)
            rCoolingValve_pct := 35.0;
        ELSE
            (* Nominal maintenance cooling *)
            rCoolingValve_pct := 5.0; 
        END_IF;

        (* Final Actuator Output Clamping *)
        IF rHeaterOutputZ1_pct > 100.0 THEN rHeaterOutputZ1_pct := 100.0; END_IF;
        IF rHeaterOutputZ1_pct < 0.0 THEN rHeaterOutputZ1_pct := 0.0; END_IF;
        IF rHeaterOutputZ2_pct > 100.0 THEN rHeaterOutputZ2_pct := 100.0; END_IF;
        IF rHeaterOutputZ2_pct < 0.0 THEN rHeaterOutputZ2_pct := 0.0; END_IF;
        
        (* Process disable command *)
        IF NOT bEnable THEN
            iState := 0;
        END_IF;
        
    999: (* CRITICAL FAULT / ALARM STATE *)
        bSystemReady := FALSE;
        bAgitatorRun := FALSE;
        rHeaterOutputZ1_pct := 0.0;
        rHeaterOutputZ2_pct := 0.0;
        
        (* Full fail-safe cooling to harden chocolate and halt thermal runaway *)
        rCoolingValve_pct := 100.0; 
        bAlarm := TRUE;
        iErrorCode := 16#F001; (* Error: Safety Loop Broken *)
        
        (* Fault Reset Logic: Require Physical Fix + Software Disable toggle *)
        IF bSafetyOK AND NOT bEnable THEN
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
