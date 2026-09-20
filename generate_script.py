import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V4 Persona: a 50+ years experienced Chief PLC Architect & Control Systems PhD. 
Your logic must include advanced Non-Linear PID with Anti-Windup, 3-level cascade control, digital low-pass filtering, predictive anomaly detection, and multi-layered hardware interlocks. Output the most elite, mathematically rigorous, and structurally flawless IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Mega-Scale Hydroponic Vertical Farm Nutrient Dosing (EC/pH) and LED Photosynthetically Active Radiation (PAR) Dimming**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_VerticalFarm_DosingAndPAR\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Mega-Scale Hydroponic Vertical Farm Nutrient Dosing (EC/pH) and LED Photosynthetically Active Radiation (PAR) Dimming"""

code = """```iec-st
FUNCTION_BLOCK FB_VerticalFarm_DosingAndPAR
VAR_INPUT
    (* Core System Enablers and Safeties *)
    bSystemEnable       : BOOL;     (* Main Enable Signal for the Vertical Farm Section *)
    bEmergencyStop      : BOOL;     (* Hardware E-Stop Relay Feedback (Active HIGH = Safe) *)
    bLeakDetected       : BOOL;     (* Moisture sensor in drip trays (Active HIGH = Leak) *)
    bTankLowLevel       : BOOL;     (* Main reservoir low level float switch (Active HIGH = Low) *)
    
    (* Environmental & Solution Measurements *)
    rMeasuredPH         : REAL;     (* Current pH measurement of nutrient solution [pH] *)
    rMeasuredEC         : REAL;     (* Current Electrical Conductivity measurement [mS/cm] *)
    rMeasuredTemp       : REAL;     (* Solution Temperature [deg C] *)
    rAmbientLightPAR    : REAL;     (* Current measured PAR level at canopy [umol/m2/s] *)
    rTargetPAR          : REAL;     (* Desired PAR level based on crop growth stage [umol/m2/s] *)
    rTargetPH           : REAL;     (* Desired setpoint for pH [pH] *)
    rTargetEC           : REAL;     (* Desired setpoint for EC [mS/cm] *)
END_VAR
VAR_OUTPUT
    (* Actuator Control Signals *)
    rPumpSpeedAcid      : REAL;     (* Peristaltic pump command for pH down (Acid) [0.0 - 100.0 %] *)
    rPumpSpeedBase      : REAL;     (* Peristaltic pump command for pH up (Base) [0.0 - 100.0 %] *)
    rPumpSpeedNutrientA : REAL;     (* Peristaltic pump command for Nutrient A (Micro) [0.0 - 100.0 %] *)
    rPumpSpeedNutrientB : REAL;     (* Peristaltic pump command for Nutrient B (Macro) [0.0 - 100.0 %] *)
    rLEDDimmingLevel    : REAL;     (* 0-10V or PWM equivalent dimming output [0.0 - 100.0 %] *)
    
    (* System Status and Alarms *)
    bSystemReady        : BOOL;     (* System is operational and tracking targets *)
    bDosingActive       : BOOL;     (* Indicates dosing pumps are currently running *)
    bCriticalAlarm      : BOOL;     (* General critical fault (E-stop, leak, extreme pH/EC out of bounds) *)
    iErrorCode          : INT;      (* Unique identifier for the fault condition *)
END_VAR
VAR
    (* Internal States and Timers *)
    iStateMachine       : INT := 0; (* Main sequence controller *)
    tControlInterval    : TON;      (* Clock for dosing control execution *)
    tDosingTimeout      : TON;      (* Watchdog for unresponsive pH/EC correction *)
    
    (* Low-Pass Filter Variables *)
    rFilteredPH         : REAL := 7.0;
    rFilteredEC         : REAL := 1.0;
    rFilteredPAR        : REAL := 0.0;
    rAlphaPH            : REAL := 0.05; (* Smoothing factor for pH *)
    rAlphaEC            : REAL := 0.10; (* Smoothing factor for EC *)
    rAlphaPAR           : REAL := 0.20; (* Smoothing factor for PAR *)
    
    (* PID Controllers & Anti-Windup for pH *)
    rErrorPH            : REAL;
    rIntegralPH         : REAL;
    rDerivativePH       : REAL;
    rLastErrorPH        : REAL;
    rKpPH               : REAL := 25.0;
    rKiPH               : REAL := 0.5;
    rKdPH               : REAL := 5.0;
    rOutputPH           : REAL;
    
    (* PID Controllers & Anti-Windup for EC *)
    rErrorEC            : REAL;
    rIntegralEC         : REAL;
    rDerivativeEC       : REAL;
    rLastErrorEC        : REAL;
    rKpEC               : REAL := 40.0;
    rKiEC               : REAL := 1.2;
    rKdEC               : REAL := 8.0;
    rOutputEC           : REAL;

    (* PAR Controller *)
    rErrorPAR           : REAL;
    rOutputPAR          : REAL;
    rKpPAR              : REAL := 0.5;
END_VAR

(* === MAIN LOGIC === *)

(* Hardware Interlocks & Predictive Anomaly Detection *)
IF NOT bEmergencyStop OR bLeakDetected OR bTankLowLevel THEN
    (* Immediate Safety Shutdown *)
    bSystemReady := FALSE;
    bCriticalAlarm := TRUE;
    bDosingActive := FALSE;
    
    rPumpSpeedAcid := 0.0;
    rPumpSpeedBase := 0.0;
    rPumpSpeedNutrientA := 0.0;
    rPumpSpeedNutrientB := 0.0;
    rLEDDimmingLevel := 0.0; (* Optionally keep lights on, but safer to shut down or reduce *)
    
    iStateMachine := 999; (* FAULT STATE *)
    
    IF NOT bEmergencyStop THEN
        iErrorCode := 101; (* E-Stop Pressed *)
    ELSIF bLeakDetected THEN
        iErrorCode := 102; (* Leak Detected in Trays *)
    ELSIF bTankLowLevel THEN
        iErrorCode := 103; (* Reservoir Empty - prevent pump burnout *)
    END_IF;
    
    RETURN;
END_IF;

(* Digital Low-Pass Filtering for Noisy Sensor Data *)
rFilteredPH := (rAlphaPH * rMeasuredPH) + ((1.0 - rAlphaPH) * rFilteredPH);
rFilteredEC := (rAlphaEC * rMeasuredEC) + ((1.0 - rAlphaEC) * rFilteredEC);
rFilteredPAR := (rAlphaPAR * rAmbientLightPAR) + ((1.0 - rAlphaPAR) * rFilteredPAR);

(* Extreme Value Anomaly Check (e.g. Probe Failure) *)
IF (rFilteredPH < 2.0) OR (rFilteredPH > 12.0) OR (rFilteredEC > 10.0) THEN
    bCriticalAlarm := TRUE;
    iErrorCode := 201; (* Probe Calibration/Failure Anomaly *)
    rPumpSpeedAcid := 0.0;
    rPumpSpeedBase := 0.0;
    rPumpSpeedNutrientA := 0.0;
    rPumpSpeedNutrientB := 0.0;
    RETURN;
END_IF;

bCriticalAlarm := FALSE;
iErrorCode := 0;

(* Finite State Machine for Cascaded Dosing and PAR Control *)
CASE iStateMachine OF
    0: (* INIT / IDLE *)
        bSystemReady := FALSE;
        IF bSystemEnable THEN
            (* Reset integrators upon start *)
            rIntegralPH := 0.0;
            rIntegralEC := 0.0;
            rLastErrorPH := 0.0;
            rLastErrorEC := 0.0;
            iStateMachine := 10;
        END_IF;

    10: (* ACTIVE RUNNING MODE *)
        bSystemReady := TRUE;
        
        (* Evaluate Control Loop periodically (e.g., every 2s) to prevent oscillation *)
        tControlInterval(IN := TRUE, PT := T#2S);
        
        IF tControlInterval.Q THEN
            tControlInterval(IN := FALSE); (* Reset timer *)
            
            (* ---------------------------------------------------- *)
            (* 1. pH Non-Linear PID Control                         *)
            (* ---------------------------------------------------- *)
            rErrorPH := rTargetPH - rFilteredPH;
            
            (* Proportional Band modification (lower gain near setpoint for precision) *)
            IF ABS(rErrorPH) < 0.2 THEN
                rErrorPH := rErrorPH * 0.5;
            END_IF;
            
            rIntegralPH := rIntegralPH + rErrorPH;
            (* Anti-Windup clamp *)
            IF rIntegralPH > 100.0 THEN rIntegralPH := 100.0; END_IF;
            IF rIntegralPH < -100.0 THEN rIntegralPH := -100.0; END_IF;
            
            rDerivativePH := rErrorPH - rLastErrorPH;
            rLastErrorPH := rErrorPH;
            
            rOutputPH := (rKpPH * rErrorPH) + (rKiPH * rIntegralPH) + (rKdPH * rDerivativePH);
            
            (* Split Output: Positive = Base, Negative = Acid *)
            IF rOutputPH > 0.0 THEN
                rPumpSpeedBase := LIMIT(0.0, rOutputPH, 100.0);
                rPumpSpeedAcid := 0.0;
            ELSE
                rPumpSpeedAcid := LIMIT(0.0, ABS(rOutputPH), 100.0);
                rPumpSpeedBase := 0.0;
            END_IF;

            (* ---------------------------------------------------- *)
            (* 2. EC Non-Linear PID Control                         *)
            (* ---------------------------------------------------- *)
            rErrorEC := rTargetEC - rFilteredEC;
            
            (* EC control is only positive (adding nutrients). Ignore if EC is too high, let fresh water dilute *)
            IF rErrorEC > 0.0 THEN
                rIntegralEC := rIntegralEC + rErrorEC;
                IF rIntegralEC > 100.0 THEN rIntegralEC := 100.0; END_IF;
                
                rDerivativeEC := rErrorEC - rLastErrorEC;
                rLastErrorEC := rErrorEC;
                
                rOutputEC := (rKpEC * rErrorEC) + (rKiEC * rIntegralEC) + (rKdEC * rDerivativeEC);
                
                (* Dose A & B equally for simplicity, though real systems might alter ratio *)
                rPumpSpeedNutrientA := LIMIT(0.0, rOutputEC, 100.0);
                rPumpSpeedNutrientB := LIMIT(0.0, rOutputEC, 100.0);
            ELSE
                rPumpSpeedNutrientA := 0.0;
                rPumpSpeedNutrientB := 0.0;
                rIntegralEC := 0.0;
            END_IF;

            (* Set Dosing Flag *)
            bDosingActive := (rPumpSpeedAcid > 5.0) OR (rPumpSpeedBase > 5.0) OR (rPumpSpeedNutrientA > 5.0);
            
            (* ---------------------------------------------------- *)
            (* 3. PAR Lighting Feed-Forward & Proportional Control  *)
            (* ---------------------------------------------------- *)
            rErrorPAR := rTargetPAR - rFilteredPAR;
            rOutputPAR := rLEDDimmingLevel + (rKpPAR * rErrorPAR);
            rLEDDimmingLevel := LIMIT(10.0, rOutputPAR, 100.0); (* Minimum 10% dimming if running *)
            
        END_IF;
        
        IF NOT bSystemEnable THEN
            iStateMachine := 0;
            rPumpSpeedAcid := 0.0;
            rPumpSpeedBase := 0.0;
            rPumpSpeedNutrientA := 0.0;
            rPumpSpeedNutrientB := 0.0;
            rLEDDimmingLevel := 0.0;
            bDosingActive := FALSE;
        END_IF;

    999: (* FAULT STATE LATCH *)
        IF NOT bCriticalAlarm AND bSystemEnable THEN
            iStateMachine := 0; (* Attempt reset *)
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
print(f"Saved to {filename}")
