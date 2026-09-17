import json
import uuid
import os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Industrial Scale Paint Mixing and Dispensing Viscosity and Color Match Control**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_PaintMixing_Control\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
   record = {\"messages\": [{\"role\": \"user\", \"content\": prompt}, {\"role\": \"assistant\", \"content\": code}]}
   with open(f\"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json\", \"w\", encoding=\"utf-8\") as f:
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
6. REPLY with: EVOLUTION COMPLETE: Industrial Scale Paint Mixing and Dispensing Viscosity and Color Match Control

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_PaintMixingViscosityColorControl
VAR_INPUT
    (* System Operation & Safety *)
    bEnable            : BOOL;     (* System sequence enable command *)
    bEStop_OK          : BOOL;     (* Emergency stop circuit healthy (failsafe) *)
    
    (* Physical Process Sensors *)
    rViscositySensor   : REAL;     (* Current measured viscosity in centiPoise (cP) *)
    rViscosityTarget   : REAL;     (* Target setpoint viscosity in cP *)
    rColorDeltaE       : REAL;     (* Spectrophotometer Delta E reading (color difference from target) *)
    rColorTargetDE     : REAL;     (* Acceptable Delta E tolerance threshold (usually < 1.0) *)
    rTankTemperature   : REAL;     (* Mixing tank fluid temperature in degrees Celsius *)
    rAgitatorFeedback  : REAL;     (* Actual agitator speed feedback in RPM *)
END_VAR
VAR_OUTPUT
    (* System Status *)
    bSystemReady       : BOOL;     (* System is in standby, ready for a new batch *)
    bMixingActive      : BOOL;     (* Mixing sequence currently in progress *)
    
    (* Control Actuators *)
    rViscosityModVlv   : REAL;     (* Viscosity modifier dosing valve command (0.0 - 100.0%) *)
    rPigmentDosingVlv  : REAL;     (* Pigment dosing valve position command (0.0 - 100.0%) *)
    rAgitatorSpeedRef  : REAL;     (* Target agitator VFD speed reference in RPM *)
    
    (* Alarms *)
    bAlarm             : BOOL;     (* Critical fault active requiring operator intervention *)
    iFaultCode         : INT;      (* Detailed integer fault code for HMI diagnostics *)
END_VAR
VAR
    (* Internal State & Timers *)
    iState             : INT := 0; (* Main sequence state machine step *)
    tMixTimer          : TON;      (* Configurable mixing duration timer *)
    tStabTimer         : TON;      (* Stabilization/settling timer post-dosing *)
    
    (* Viscosity PID Control Variables *)
    rViscError         : REAL;     (* Viscosity control proportional error *)
    rViscIntegral      : REAL;     (* Viscosity PID integral accumulator *)
    rKp_Visc           : REAL := 0.25;  (* Viscosity loop proportional gain *)
    rKi_Visc           : REAL := 0.05;  (* Viscosity loop integral gain *)
    
    (* Environmental Compensation *)
    rTempCompFactor    : REAL;     (* Temperature compensation coefficient for viscosity *)
    bTempValid         : BOOL;     (* Temperature sensor validation flag *)
END_VAR

(* === MAIN LOGIC === *)

(* 1. Safety and Interlock Evaluation *)
IF NOT bEStop_OK THEN
    iState := 99; (* Force immediate transition to fault state *)
    iFaultCode := 1001; (* Fault Code 1001: Emergency Stop Active *)
END_IF;

(* 2. Sensor Validation & Temperature Compensation *)
(* Ensure temperature is within physically plausible and safe operating limits *)
IF rTankTemperature > 5.0 AND rTankTemperature < 80.0 THEN
    bTempValid := TRUE;
    (* Calculate simplified Arrhenius-style temperature compensation factor *)
    (* Viscosity typically drops as temperature rises *)
    rTempCompFactor := 1.0 + ((25.0 - rTankTemperature) * 0.015);
ELSE
    bTempValid := FALSE;
    rTempCompFactor := 1.0; (* Fallback to nominal factor if sensor fails *)
    IF bMixingActive THEN
        iState := 99;
        iFaultCode := 2001; (* Fault Code 2001: Temperature Out of Range *)
    END_IF;
END_IF;

(* 3. Main Sequential Control State Machine *)
CASE iState OF
    0: (* IDLE & READY *)
        bSystemReady := TRUE;
        bMixingActive := FALSE;
        rViscosityModVlv := 0.0;
        rPigmentDosingVlv := 0.0;
        rAgitatorSpeedRef := 0.0;
        bAlarm := FALSE;
        iFaultCode := 0;
        
        (* Transition to active sequence upon enable *)
        IF bEnable AND bTempValid THEN
            bSystemReady := FALSE;
            bMixingActive := TRUE;
            rViscIntegral := 0.0; (* Reset PID integral term *)
            iState := 10;
        END_IF;

    10: (* BASE AGITATION (LOW SHEAR) *)
        rAgitatorSpeedRef := 300.0; (* Low shear initial homogenization *)
        
        tMixTimer(IN := TRUE, PT := T#30S);
        IF tMixTimer.Q THEN
            tMixTimer(IN := FALSE);
            iState := 20;
        END_IF;

    20: (* VISCOSITY CONTROL (PID LOOP WITH ANTI-WINDUP) *)
        rAgitatorSpeedRef := 750.0; (* High shear for viscosity modifier dispersion *)
        
        (* Calculate compensated error, applying temp correction to raw sensor data *)
        rViscError := (rViscosityTarget - (rViscositySensor * rTempCompFactor));
        
        (* Integral term accumulation (assuming cyclical execution, e.g., 100ms) *)
        rViscIntegral := rViscIntegral + (rViscError * 0.1); 
        
        (* Integral Anti-Windup Limits *)
        IF rViscIntegral > 50.0 THEN rViscIntegral := 50.0; END_IF;
        IF rViscIntegral < -50.0 THEN rViscIntegral := -50.0; END_IF;
        
        (* Calculate Control Output *)
        rViscosityModVlv := (rViscError * rKp_Visc) + (rViscIntegral * rKi_Visc);
        
        (* Output Saturation/Clamping *)
        IF rViscosityModVlv > 100.0 THEN rViscosityModVlv := 100.0; END_IF;
        IF rViscosityModVlv < 0.0 THEN rViscosityModVlv := 0.0; END_IF;
        
        (* Stability Check: Transition when viscosity error is tightly controlled *)
        IF ABS(rViscError) < 2.0 THEN
            tStabTimer(IN := TRUE, PT := T#15S);
            IF tStabTimer.Q THEN
                tStabTimer(IN := FALSE);
                rViscosityModVlv := 0.0; (* Terminate modifier dosing *)
                iState := 30;
            END_IF;
        ELSE
            tStabTimer(IN := FALSE); (* Reset stability timer on disturbance *)
        END_IF;

    30: (* COLOR MATCHING & SPECTROPHOTOMETER FEEDBACK *)
        rAgitatorSpeedRef := 500.0; (* Medium shear for color pigment blending *)
        
        IF rColorDeltaE > rColorTargetDE THEN
            (* Non-linear Pulsed Dosing Strategy based on Delta E magnitude *)
            IF rColorDeltaE > 5.0 THEN
                rPigmentDosingVlv := 45.0; (* Aggressive macro-dose *)
            ELSIF rColorDeltaE > 2.0 THEN
                rPigmentDosingVlv := 20.0; (* Moderate corrective dose *)
            ELSE
                rPigmentDosingVlv := 5.0;  (* Micro-dose for final polish *)
            END_IF;
            
            tMixTimer(IN := TRUE, PT := T#5S);
            IF tMixTimer.Q THEN
                rPigmentDosingVlv := 0.0; (* Close valve to allow homogenization *)
                tMixTimer(IN := FALSE);
                iState := 40;
            END_IF;
        ELSE
            (* Color matches target specification *)
            rPigmentDosingVlv := 0.0;
            iState := 50;
        END_IF;
        
    40: (* COLOR HOMOGENIZATION / STABILIZATION DELAY *)
        rPigmentDosingVlv := 0.0; (* Ensure dosing is halted *)
        tStabTimer(IN := TRUE, PT := T#20S);
        IF tStabTimer.Q THEN
            tStabTimer(IN := FALSE);
            iState := 30; (* Return to color matching logic to re-evaluate Delta E *)
        END_IF;

    50: (* BATCH COMPLETE / HOLDING *)
        rAgitatorSpeedRef := 100.0; (* Keep-alive slow rotation prevents pigment settling *)
        bSystemReady := TRUE;       (* Signal external systems that batch is ready *)
        
        (* Wait for operator or supervisory system to drop enable *)
        IF NOT bEnable THEN
            iState := 0;
        END_IF;

    99: (* FAULT HANDLING *)
        bAlarm := TRUE;
        bSystemReady := FALSE;
        bMixingActive := FALSE;
        
        (* Fail-safe state for all actuators *)
        rViscosityModVlv := 0.0;
        rPigmentDosingVlv := 0.0;
        rAgitatorSpeedRef := 0.0;
        
        (* Reset condition requires clearance of E-Stop and manual toggle of Enable *)
        IF bEStop_OK AND NOT bEnable THEN
            iState := 0; 
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
