import os, json, uuid

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Industrial Scale Continuous Pharmaceutical Twin-Screw Granulation (TSG)**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Liquid binder to powder mass-flow ratio (L/S) micro-dispensing, barrel temperature zone cascading, and near-infrared (NIR) moisture content feedback). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_ContinuousTSG\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Industrial Scale Continuous Pharmaceutical Twin-Screw Granulation (TSG)

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_ContinuousTSG_AdvancedControl
VAR_INPUT
    (* Primary Safety and Control Signals *)
    bEnable                 : BOOL;     (* System enable signal / Master Start *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal (TRUE = Safe) *)
    
    (* Process Variable Feedbacks *)
    rPowderMassFlow         : REAL;     (* kg/hr - Dry blend mass flow rate from Loss-in-Weight feeder *)
    rLiquidBinderFlow       : REAL;     (* g/min - Actual liquid binder flow from Coriolis mass flow meter *)
    rNIRMoistureContent     : REAL;     (* %w/w  - Inline Near-Infrared moisture sensor reading *)
    rScrewTorque            : REAL;     (* Nm    - Actual twin-screw motor torque *)
    rBarrelTempZone1_PV     : REAL;     (* degC  - Feeding zone temperature PV *)
    rBarrelTempZone2_PV     : REAL;     (* degC  - Kneading/Granulation zone temperature PV *)
    
    (* Recipe Parameters *)
    rTargetLSRatio          : REAL;     (* %w/w  - Target Liquid-to-Solid ratio *)
    rMaxTorqueLimit         : REAL;     (* Nm    - Maximum allowable torque before safety trip *)
END_VAR

VAR_OUTPUT
    (* System Status *)
    bSystemReady            : BOOL;     (* System ready for operation / warmed up *)
    bAlarm                  : BOOL;     (* General fault alarm output *)
    
    (* Actuator Commands *)
    rLiquidPumpSpeedCmd     : REAL;     (* RPM   - Command to liquid binder micro-dispensing pump *)
    rScrewSpeedCmd          : REAL;     (* RPM   - Command to twin-screw extruder motor *)
    rBarrelTempZone1_SP     : REAL;     (* degC  - Feeding zone temperature Setpoint *)
    rBarrelTempZone2_SP     : REAL;     (* degC  - Kneading zone temperature Setpoint *)
    
    (* Data/Diagnostics *)
    rCalculatedMoistureBias : REAL;     (* %w/w  - PID compensated moisture error *)
END_VAR

VAR
    (* Internal State and Timers *)
    iState                  : INT := 0; (* State Machine Index *)
    tWarmupTimer            : TON;      (* Barrel heating wait timer *)
    tStabilizationTimer     : TON;      (* Process stabilization timer *)
    
    (* Internal PID / Control Variables *)
    rMoistureError          : REAL;
    rMoistureIntegral       : REAL := 0.0;
    rKp                     : REAL := 0.25; 
    rKi                     : REAL := 0.05;
    rTargetLiquidFlow       : REAL;
    rPumpBaseSpeed          : REAL;
    
    (* Constants *)
    c_LiquidDensity         : REAL := 1.02; (* g/cm3 - Example binder density *)
END_VAR

(* === MAIN SAFETY INTERLOCK === *)
IF NOT bEmergencyStop THEN
    bSystemReady            := FALSE;
    bAlarm                  := TRUE;
    rLiquidPumpSpeedCmd     := 0.0;
    rScrewSpeedCmd          := 0.0;
    iState                  := 99; (* Fault State *)
    RETURN;
END_IF;

(* === STATE MACHINE LOGIC === *)
CASE iState OF
    0: (* IDLE & PREPARATION *)
        bSystemReady := FALSE;
        bAlarm := FALSE;
        rScrewSpeedCmd := 0.0;
        rLiquidPumpSpeedCmd := 0.0;
        
        IF bEnable THEN
            (* Set initial temperature profiles for pharmaceutical granulation *)
            rBarrelTempZone1_SP := 25.0; (* Cooler feed zone *)
            rBarrelTempZone2_SP := 40.0; (* Warm kneading zone for binder activation *)
            iState := 10;
        END_IF;
        
    10: (* HEATING WARMUP *)
        (* Wait for barrel temperatures to reach within +/- 2.0 degC of setpoint *)
        IF (ABS(rBarrelTempZone1_PV - rBarrelTempZone1_SP) < 2.0) AND 
           (ABS(rBarrelTempZone2_PV - rBarrelTempZone2_SP) < 2.0) THEN
            
            tWarmupTimer(IN := TRUE, PT := T#30S);
            IF tWarmupTimer.Q THEN
                tWarmupTimer(IN := FALSE);
                bSystemReady := TRUE;
                iState := 20;
            END_IF;
        ELSE
            tWarmupTimer(IN := FALSE);
        END_IF;
        
    20: (* STEADY STATE PRODUCTION *)
        IF NOT bEnable THEN
            iState := 0;
        END_IF;
        
        (* 1. Screw Speed Logic - Fixed for steady state, unless torque spikes *)
        rScrewSpeedCmd := 400.0; (* Nominal 400 RPM *)
        
        (* Torque overload protection (predictive ramp-down) *)
        IF rScrewTorque > (rMaxTorqueLimit * 0.90) THEN
            rScrewSpeedCmd := rScrewSpeedCmd * 0.8; (* Reduce speed by 20% to prevent jam *)
            bAlarm := TRUE;
        END_IF;

        (* 2. Cascaded L/S Ratio & Moisture Control Loop *)
        (* Calculate base required liquid flow (g/min) from dry powder mass flow (kg/hr) *)
        (* Conversion: kg/hr to g/min = * (1000/60) *)
        rTargetLiquidFlow := (rPowderMassFlow * 16.6667) * (rTargetLSRatio / 100.0);
        
        (* NIR Moisture Feedback PID Override (Trim) *)
        (* Target moisture usually correlates to L/S ratio, assuming e.g. 15% w/w *)
        rMoistureError := (rTargetLSRatio) - rNIRMoistureContent;
        
        (* Anti-windup for integral term *)
        IF (rMoistureIntegral < 10.0) AND (rMoistureIntegral > -10.0) THEN
            rMoistureIntegral := rMoistureIntegral + (rMoistureError * 0.1); (* 100ms task assumed *)
        END_IF;
        
        rCalculatedMoistureBias := (rKp * rMoistureError) + (rKi * rMoistureIntegral);
        
        (* Apply moisture bias to target flow *)
        rTargetLiquidFlow := rTargetLiquidFlow + rCalculatedMoistureBias;
        
        (* Convert required mass flow (g/min) to pump RPM based on density and pump displacement *)
        rPumpBaseSpeed := rTargetLiquidFlow / (c_LiquidDensity * 2.5); (* Assume 2.5 cc/rev pump displacement *)
        
        (* Boundary clamp for safety *)
        IF rPumpBaseSpeed > 150.0 THEN
            rLiquidPumpSpeedCmd := 150.0;
        ELSIF rPumpBaseSpeed < 0.0 THEN
            rLiquidPumpSpeedCmd := 0.0;
        ELSE
            rLiquidPumpSpeedCmd := rPumpBaseSpeed;
        END_IF;

    99: (* FAULT HANDLING *)
        rLiquidPumpSpeedCmd := 0.0;
        rScrewSpeedCmd := 0.0;
        rBarrelTempZone1_SP := 20.0;
        rBarrelTempZone2_SP := 20.0;
        
        IF NOT bEmergencyStop THEN
            (* Wait for safety reset *)
        ELSE
            IF NOT bEnable THEN
                iState := 0; (* Reset fault when enable is dropped and E-Stop is OK *)
            END_IF;
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
