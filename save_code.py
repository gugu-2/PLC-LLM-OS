import os, json, uuid
os.makedirs('data/swarm_raw', exist_ok=True)
prompt = '''You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Advanced Biopharmaceutical Mammalian Cell Culture Bioreactor**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Perfusion cascade control for dissolved oxygen (DO) and pH, glucose/lactate metabolic shift multi-variate feeding, and anti-foaming mechanical/chemical intervention). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   prompt = """<copy this exact user prompt here>"""
   code = """```iec-st\nFUNCTION_BLOCK FB_MammalianBioreactor\n//...\nEND_FUNCTION_BLOCK\n```"""
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
6. REPLY with: EVOLUTION COMPLETE: Advanced Biopharmaceutical Mammalian Cell Culture Bioreactor

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT.'''

code = '''```iec-st
FUNCTION_BLOCK FB_MammalianBioreactorControl
VAR_INPUT
    (* Essential Physical I/O & Measurements *)
    bSystemEnable       : BOOL;     (* Global Enable for Bioreactor Control *)
    bEmergencyStop      : BOOL;     (* Safety Relay Status (TRUE = OK, FALSE = E-STOP) *)
    rpH_Measurement     : REAL;     (* Current pH value from primary sensor (0.0 - 14.0) *)
    rDO_Measurement     : REAL;     (* Dissolved Oxygen (%) *)
    rTemp_Measurement   : REAL;     (* Bioreactor Temperature (Deg C) *)
    rAgitatorSpeed      : REAL;     (* Current Agitator Speed (RPM) *)
    rGlucoseConc        : REAL;     (* Online Glucose Concentration (g/L) *)
    rLactateConc        : REAL;     (* Online Lactate Concentration (g/L) *)
    bFoamDetected       : BOOL;     (* Foam detection probe active high *)
END_VAR
VAR_OUTPUT
    (* Actuator Control Commands *)
    bSystemReady        : BOOL;     (* Interlocks verified, ready for operation *)
    rAgitatorSetpoint   : REAL;     (* Commanded Agitator Speed (RPM) *)
    rO2_SpargingRate    : REAL;     (* Oxygen MFC Setpoint (SLPM) *)
    rAir_SpargingRate   : REAL;     (* Air MFC Setpoint (SLPM) *)
    rBase_PumpSpeed     : REAL;     (* Base Addition Pump Speed (%) *)
    rCO2_SpargingRate   : REAL;     (* CO2 MFC Setpoint (SLPM) for pH Control *)
    rFeed_PumpSpeed     : REAL;     (* Nutrient Feed Pump Speed (%) *)
    bAntiFoam_PumpCmd   : BOOL;     (* Anti-foam addition pump command *)
    bCriticalAlarm      : BOOL;     (* Critical process deviation alarm *)
END_VAR
VAR
    (* Internal PID Controllers and State Variables *)
    iControlState       : INT := 0; (* 0: IDLE, 10: INIT, 20: RUN_PHASE_1, 30: METABOLIC_SHIFT, 99: FAULT *)
    tProcessTimer       : TON;
    tAntiFoamTimer      : TON;
    
    (* PID Internal Variables for DO Control (Cascade O2 Sparging & Agitation) *)
    rDO_Setpoint        : REAL := 40.0; (* 40% DO Target *)
    rDO_Error           : REAL;
    rDO_Integral        : REAL := 0.0;
    rKp_DO              : REAL := 1.5;
    rKi_DO              : REAL := 0.05;
    
    (* PID Internal Variables for pH Control *)
    rpH_Setpoint        : REAL := 7.05;
    rpH_Error           : REAL;
    rpH_Integral        : REAL := 0.0;
    rKp_pH              : REAL := 2.0;
    rKi_pH              : REAL := 0.1;
    
    (* Metabolic Control Parameters *)
    rGlucoseTarget      : REAL := 3.0; (* Target glucose g/L *)
    rLactateThreshold   : REAL := 2.5; (* Lactate shift threshold g/L *)
    
    bShiftActive        : BOOL := FALSE;
END_VAR

(* === MAIN LOGIC === *)

(* Safety and Interlock Verification *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bCriticalAlarm := TRUE;
    iControlState := 99;
    
    (* Safe State Enforcement *)
    rAgitatorSetpoint := 0.0;
    rO2_SpargingRate := 0.0;
    rAir_SpargingRate := 0.0;
    rBase_PumpSpeed := 0.0;
    rCO2_SpargingRate := 0.0;
    rFeed_PumpSpeed := 0.0;
    bAntiFoam_PumpCmd := FALSE;
    RETURN;
END_IF;

(* State Machine for Bioreactor Lifecycle *)
CASE iControlState OF
    0: (* IDLE STATE *)
        bSystemReady := TRUE;
        bCriticalAlarm := FALSE;
        IF bSystemEnable THEN
            iControlState := 10;
        END_IF;

    10: (* INITIALIZATION *)
        (* Bring up base agitation and air flow *)
        rAgitatorSetpoint := 50.0; (* Minimum RPM *)
        rAir_SpargingRate := 0.5;  (* Minimum SLPM *)
        
        tProcessTimer(IN := TRUE, PT := T#30S);
        IF tProcessTimer.Q THEN
            tProcessTimer(IN := FALSE);
            iControlState := 20;
        END_IF;

    20: (* RUN PHASE 1: EXPONENTIAL GROWTH *)
        (* DO Control: Cascade implementation using Oxygen sparging and Agitation *)
        rDO_Error := rDO_Setpoint - rDO_Measurement;
        rDO_Integral := rDO_Integral + rDO_Error * 0.1; (* Assuming 100ms task rate *)
        
        (* Prevent Integral Windup *)
        IF rDO_Integral > 100.0 THEN rDO_Integral := 100.0; END_IF;
        IF rDO_Integral < -100.0 THEN rDO_Integral := -100.0; END_IF;
        
        (* Calculate Total DO Demand *)
        rO2_SpargingRate := (rKp_DO * rDO_Error) + (rKi_DO * rDO_Integral);
        IF rO2_SpargingRate < 0.0 THEN rO2_SpargingRate := 0.0; END_IF;
        
        (* pH Control: Split range for CO2 (acidic) and Base *)
        rpH_Error := rpH_Setpoint - rpH_Measurement;
        rpH_Integral := rpH_Integral + rpH_Error * 0.1;
        
        IF rpH_Error > 0.0 THEN
            (* pH is too low -> add base *)
            rBase_PumpSpeed := (rKp_pH * rpH_Error) + (rKi_pH * rpH_Integral);
            rCO2_SpargingRate := 0.0;
        ELSE
            (* pH is too high -> add CO2 *)
            rCO2_SpargingRate := ABS(rKp_pH * rpH_Error) + ABS(rKi_pH * rpH_Integral);
            rBase_PumpSpeed := 0.0;
        END_IF;
        
        (* Glucose Feeding Strategy *)
        IF rGlucoseConc < rGlucoseTarget THEN
            rFeed_PumpSpeed := 15.0; (* Base feed rate *)
        ELSE
            rFeed_PumpSpeed := 0.0;
        END_IF;
        
        (* Metabolic Shift Detection based on Lactate accumulation *)
        IF rLactateConc > rLactateThreshold THEN
            bShiftActive := TRUE;
            iControlState := 30;
        END_IF;

    30: (* METABOLIC SHIFT / PRODUCTION PHASE *)
        (* Reduce Glucose Target to induce specific production metabolism *)
        rGlucoseTarget := 1.0; 
        
        (* Maintain pH and DO but with more aggressive Agitation vs Sparging to limit shear stress *)
        rAgitatorSetpoint := 75.0;
        rDO_Setpoint := 30.0; (* Lower DO target in production phase *)
        
        (* Continue Feed at adjusted rate *)
        IF rGlucoseConc < rGlucoseTarget THEN
            rFeed_PumpSpeed := 5.0;
        ELSE
            rFeed_PumpSpeed := 0.0;
        END_IF;

    99: (* FAULT STATE *)
        (* Active interlock failure - hold safe state until cleared *)
        IF bEmergencyStop AND NOT bSystemEnable THEN
            iControlState := 0;
        END_IF;
END_CASE;

(* Anti-Foaming Mechanical/Chemical Intervention (Independent of main state, active while running) *)
IF iControlState >= 10 AND iControlState < 90 THEN
    IF bFoamDetected THEN
        bAntiFoam_PumpCmd := TRUE;
        tAntiFoamTimer(IN := TRUE, PT := T#5S);
    END_IF;
    
    IF tAntiFoamTimer.Q THEN
        bAntiFoam_PumpCmd := FALSE;
        IF NOT bFoamDetected THEN
            tAntiFoamTimer(IN := FALSE);
        END_IF;
    END_IF;
ELSE
    bAntiFoam_PumpCmd := FALSE;
    tAntiFoamTimer(IN := FALSE);
END_IF;

END_FUNCTION_BLOCK
```'''

record = {'messages': [{'role': 'user', 'content': prompt}, {'role': 'assistant', 'content': code}]}
filename = f'data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json'
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(record, f, ensure_ascii=False)
print(f'Saved to {filename}')
