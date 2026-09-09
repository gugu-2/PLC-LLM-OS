import json, uuid, os

prompt = """<USER_REQUEST>
You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Industrial Scale Bio-Synthetic Spider Silk Extrusion Spinneret**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Transgenic protein dope shear-thinning rheology matching, sub-micron coagulation bath pH cascade, and 10,000 RPM take-up winder tension servoing). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_SpiderSilkExtrusion\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Industrial Scale Bio-Synthetic Spider Silk Extrusion Spinneret

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT.
</USER_REQUEST>"""

code = """```iec-st
FUNCTION_BLOCK FB_SpiderSilkExtrusion
(* 
   ================================================================================
   Block Name    : FB_SpiderSilkExtrusion
   Description   : Ultra-high precision control system for transgenic protein dope 
                   extrusion into a sub-micron coagulation bath. Includes rheology
                   compensation, shear-thinning tracking, pH cascade control, and 
                   high-speed (10,000 RPM) take-up winder tension servoing.
   Author        : 40-Year Veteran Industrial Architect
   ================================================================================
*)

VAR_INPUT
    bEnable                 : BOOL;     (* System master enable *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal (TRUE = OK) *)
    
    (* Extrusion Process Inputs *)
    rDopePressure           : REAL;     (* Measured dope extrusion pressure (Bar) *)
    rDopeTemperature        : REAL;     (* Measured dope temperature (Deg C) *)
    rCoagulationPH          : REAL;     (* Coagulation bath pH measurement *)
    rWinderTensionFeedback  : REAL;     (* Winder tension feedback (N) *)
    rWinderSpeedFb          : REAL;     (* Take-up winder speed feedback (RPM) *)
    
    (* Setpoints *)
    rTargetPressure         : REAL := 120.5;
    rTargetPH               : REAL := 4.50;
    rTargetTension          : REAL := 15.0;
    rTargetSpeed            : REAL := 10000.0;
END_VAR

VAR_OUTPUT
    bSystemReady            : BOOL;     (* System ready for extrusion process *)
    bActive                 : BOOL;     (* Extrusion currently active *)
    bAlarm                  : BOOL;     (* Fault/Alarm state *)
    iAlarmCode              : INT;      (* Diagnostics code *)
    
    (* Actuator Outputs *)
    rPumpSpeedCmd           : REAL;     (* Dope extrusion pump speed command (0-100%) *)
    rAcidValveCmd           : REAL;     (* Acid dosing valve command for pH (0-100%) *)
    rWinderTorqueCmd        : REAL;     (* Winder servo torque command (0-100%) *)
END_VAR

VAR
    (* Internal State Machine *)
    iExtrusionState         : INT := 0; 
    
    (* PID Controllers *)
    fbPressurePID           : PID;      (* PID for extrusion pressure *)
    fbPHPID                 : PID;      (* PID for coagulation bath pH *)
    fbTensionPID            : PID;      (* PID for winder tension *)
    
    (* Timers and Filters *)
    tStabilizationTimer     : TON;
    tDopeRheologyDelay      : TON;
    rFilteredTension        : REAL;
    rShearThinningFactor    : REAL;     (* Dynamic rheology compensation *)
    
    (* Constants *)
    TENSION_FILTER_TC       : REAL := 0.05; (* First-order filter time constant *)
    MAX_PRESSURE_DEV        : REAL := 5.0;  (* Max allowable pressure deviation *)
END_VAR

(* === MAIN LOGIC START === *)

(* Safety Interlock Check *)
IF NOT bEmergencyStop THEN
    bSystemReady        := FALSE;
    bActive             := FALSE;
    bAlarm              := TRUE;
    iAlarmCode          := 999; (* E-Stop active *)
    rPumpSpeedCmd       := 0.0;
    rAcidValveCmd       := 0.0;
    rWinderTorqueCmd    := 0.0;
    iExtrusionState     := 0;
    RETURN;
END_IF;

(* Clear basic alarms if E-Stop is OK and not in fault state *)
IF iExtrusionState <> 99 THEN
    bAlarm := FALSE;
    iAlarmCode := 0;
END_IF;

(* First order low-pass filter for winder tension feedback *)
rFilteredTension := rFilteredTension + (rWinderTensionFeedback - rFilteredTension) * TENSION_FILTER_TC;

(* State Machine for Extrusion Process *)
CASE iExtrusionState OF

    0: (* IDLE & INITIALIZATION *)
        bSystemReady := TRUE;
        bActive      := FALSE;
        rPumpSpeedCmd := 0.0;
        rAcidValveCmd := 0.0;
        rWinderTorqueCmd := 0.0;
        
        IF bEnable THEN
            bSystemReady := FALSE;
            bActive := TRUE;
            iExtrusionState := 10;
        END_IF;

    10: (* PRIMING & RHEOLOGY STABILIZATION *)
        (* Calculate dynamic shear-thinning factor based on temp & pressure *)
        IF rDopeTemperature > 20.0 THEN
            rShearThinningFactor := 1.0 - ((rDopeTemperature - 20.0) * 0.015);
        ELSE
            rShearThinningFactor := 1.0;
        END_IF;
        
        (* Ramp up pump speed slowly *)
        rPumpSpeedCmd := rPumpSpeedCmd + 0.1;
        IF rPumpSpeedCmd > 10.0 THEN
            rPumpSpeedCmd := 10.0;
        END_IF;
        
        (* Start timer to let dope rheology stabilize in the spinneret *)
        tDopeRheologyDelay(IN := TRUE, PT := T#10S);
        
        IF tDopeRheologyDelay.Q THEN
            tDopeRheologyDelay(IN := FALSE);
            iExtrusionState := 20;
        END_IF;

    20: (* EXTRUSION & COAGULATION CONTROL *)
        (* Pressure PID Execution *)
        fbPressurePID(
            ACT := rDopePressure,
            SET := rTargetPressure,
            KP  := 2.5,
            TN  := 1.2,
            TV  := 0.1,
            Y   => rPumpSpeedCmd
        );
        
        (* Apply shear-thinning compensation to pump command *)
        rPumpSpeedCmd := rPumpSpeedCmd * rShearThinningFactor;
        
        (* pH Cascade Control *)
        fbPHPID(
            ACT := rCoagulationPH,
            SET := rTargetPH,
            KP  := 1.8,
            TN  := 5.0,
            Y   => rAcidValveCmd
        );
        
        (* Transition to Winder start once pressure is stable *)
        IF ABS(rDopePressure - rTargetPressure) < MAX_PRESSURE_DEV THEN
            tStabilizationTimer(IN := TRUE, PT := T#5S);
            IF tStabilizationTimer.Q THEN
                tStabilizationTimer(IN := FALSE);
                iExtrusionState := 30;
            END_IF;
        ELSE
            tStabilizationTimer(IN := FALSE);
        END_IF;

    30: (* TAKE-UP WINDER TENSION SERVOING *)
        (* Continue maintaining pressure and pH *)
        fbPressurePID(ACT := rDopePressure, SET := rTargetPressure, KP := 2.5, TN := 1.2, TV := 0.1, Y => rPumpSpeedCmd);
        rPumpSpeedCmd := rPumpSpeedCmd * rShearThinningFactor;
        
        fbPHPID(ACT := rCoagulationPH, SET := rTargetPH, KP := 1.8, TN := 5.0, Y => rAcidValveCmd);
        
        (* Winder Tension PID Execution - High speed servo loop *)
        fbTensionPID(
            ACT := rFilteredTension,
            SET := rTargetTension,
            KP  := 5.0,
            TN  := 0.5,
            TV  := 0.05,
            Y   => rWinderTorqueCmd
        );
        
        (* Fault detection: Web Break or Over-tension *)
        IF rFilteredTension < 1.0 OR rFilteredTension > (rTargetTension * 2.0) THEN
            iExtrusionState := 99;
            iAlarmCode := 101; (* Web break or tension fault *)
        END_IF;
        
        IF NOT bEnable THEN
            iExtrusionState := 40; (* Ramp down *)
        END_IF;
        
    40: (* RAMP DOWN *)
        rWinderTorqueCmd := rWinderTorqueCmd * 0.9;
        rPumpSpeedCmd    := rPumpSpeedCmd * 0.95;
        rAcidValveCmd    := 0.0;
        
        IF rPumpSpeedCmd < 1.0 AND rWinderTorqueCmd < 1.0 THEN
            iExtrusionState := 0;
        END_IF;

    99: (* FAULT HANDLING *)
        bAlarm := TRUE;
        rPumpSpeedCmd := 0.0;
        rAcidValveCmd := 0.0;
        rWinderTorqueCmd := 0.0;
        
        IF NOT bEnable THEN
            iExtrusionState := 0; (* Reset fault state on enable toggle *)
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
