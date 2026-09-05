import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Industrial Scale Continuous Cultured Meat Bioreactor**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Microcarrier bead suspension agitation profiling, dissolved oxygen (DO) mass transfer cascading, and mammalian cell media perfusion rate stoichiometry). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_CulturedMeatBioreactor\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Industrial Scale Continuous Cultured Meat Bioreactor

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_CulturedMeatBioreactor
VAR_INPUT
    (* Required: at least 4-8 physical inputs with types and comments *)
    bEnable            : BOOL;     (* System master enable signal *)
    bEmergencyStop     : BOOL;     (* Safety relay OK signal (Normally Closed = TRUE) *)
    rDO_Measurement    : REAL;     (* Dissolved Oxygen [mg/L] *)
    rPHLevel           : REAL;     (* pH Level of the cell culture media *)
    rTemp_degC         : REAL;     (* Bioreactor temperature [°C] *)
    rAgitationSpeed    : REAL;     (* Current Agitation Speed Feedback [RPM] *)
    rPerfusionRateIn   : REAL;     (* Perfusion inlet flow rate [L/h] *)
    rGlucoseConc       : REAL;     (* Glucose concentration [g/L] *)
END_VAR
VAR_OUTPUT
    (* Required: at least 3-6 outputs with types and comments *)
    bSystemReady       : BOOL;     (* System ready status for continuous perfusion *)
    rAgitationOut      : REAL;     (* Command signal to agitator VFD [RPM] *)
    rO2SpargingValve   : REAL;     (* Control signal to Oxygen sparging mass flow controller [%] *)
    rPerfusionPumpOut  : REAL;     (* Command to extraction/harvest perfusion pump [L/h] *)
    bAlarm             : BOOL;     (* Critical fault alarm output *)
    bAcidDosingValve   : BOOL;     (* Acid dosing for pH control *)
    bBaseDosingValve   : BOOL;     (* Base dosing for pH control *)
END_VAR
VAR
    (* Internal state variables *)
    iState             : INT := 0; (* Internal state machine tracker *)
    tStateTimer        : TON;      (* State transition timer *)
    tAlarmDelay        : TON;      (* Alarm debounce timer *)
    
    (* PID Variables for DO Control (Mass Transfer Cascade) *)
    rSetpointDO        : REAL := 4.5;  (* Target DO mg/L for mammalian cell proliferation *)
    rErrorDO           : REAL;         
    rIntegralDO        : REAL := 0.0;
    rDerivativeDO      : REAL;
    rLastErrorDO       : REAL := 0.0;
    rKp_DO             : REAL := 12.5; 
    rKi_DO             : REAL := 2.1;
    rKd_DO             : REAL := 0.5;
    rMaxSparging       : REAL := 100.0;
    
    (* Agitation Profiling for Microcarrier Suspension *)
    rTargetAgitation   : REAL := 45.0; (* Base RPM to keep beads suspended but avoid shear stress *)
    rShearLimitRPM     : REAL := 65.0; (* Maximum allowed RPM before cell sheer death *)
    rAgitationRampRate : REAL := 0.5;  (* RPM increase per execution cycle *)
    
    (* pH Control Limits *)
    rSetpointPH        : REAL := 7.2;
    rDeadbandPH        : REAL := 0.05;
END_VAR

(* === MAIN LOGIC === *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bAlarm := TRUE;
    rAgitationOut := 0.0;
    rO2SpargingValve := 0.0;
    rPerfusionPumpOut := 0.0;
    bAcidDosingValve := FALSE;
    bBaseDosingValve := FALSE;
    iState := 999; (* Fault State *)
    RETURN;
END_IF;

CASE iState OF
    0: (* IDLE & INITIALIZATION *)
        bSystemReady := FALSE;
        rAgitationOut := 0.0;
        rO2SpargingValve := 0.0;
        rPerfusionPumpOut := 0.0;
        bAlarm := FALSE;
        rIntegralDO := 0.0; (* Reset Integrator *)
        
        IF bEnable THEN
            iState := 10;
        END_IF;

    10: (* RAMPING AGITATION FOR MICROCARRIER SUSPENSION *)
        IF rAgitationOut < rTargetAgitation THEN
            rAgitationOut := rAgitationOut + rAgitationRampRate;
        ELSE
            rAgitationOut := rTargetAgitation;
            iState := 20;
        END_IF;
        
        (* Prevent sheer stress limit violation *)
        IF rAgitationOut > rShearLimitRPM THEN
            rAgitationOut := rShearLimitRPM;
        END_IF;

    20: (* STABILIZATION & MASS TRANSFER (DO CASCADE) *)
        (* PID Calculation for Oxygen Sparging *)
        rErrorDO := rSetpointDO - rDO_Measurement;
        rIntegralDO := rIntegralDO + rErrorDO;
        rDerivativeDO := rErrorDO - rLastErrorDO;
        rLastErrorDO := rErrorDO;
        
        rO2SpargingValve := (rKp_DO * rErrorDO) + (rKi_DO * rIntegralDO) + (rKd_DO * rDerivativeDO);
        
        (* Anti-windup and clamping for mass flow controller *)
        IF rO2SpargingValve > rMaxSparging THEN
            rO2SpargingValve := rMaxSparging;
            rIntegralDO := rIntegralDO - rErrorDO; (* Anti-windup *)
        ELSIF rO2SpargingValve < 0.0 THEN
            rO2SpargingValve := 0.0;
        END_IF;
        
        tStateTimer(IN := (ABS(rErrorDO) < 0.2 AND rTemp_degC > 36.5 AND rTemp_degC < 37.5), PT := T#5M);
        IF tStateTimer.Q THEN
            tStateTimer(IN := FALSE);
            iState := 30;
        END_IF;

    30: (* CONTINUOUS CULTURE & PERFUSION *)
        bSystemReady := TRUE;
        
        (* Keep DO Loop Active *)
        rErrorDO := rSetpointDO - rDO_Measurement;
        rIntegralDO := rIntegralDO + rErrorDO;
        rDerivativeDO := rErrorDO - rLastErrorDO;
        rO2SpargingValve := (rKp_DO * rErrorDO) + (rKi_DO * rIntegralDO) + (rKd_DO * rDerivativeDO);
        IF rO2SpargingValve > rMaxSparging THEN rO2SpargingValve := rMaxSparging; ELSIF rO2SpargingValve < 0.0 THEN rO2SpargingValve := 0.0; END_IF;
        rLastErrorDO := rErrorDO;
        
        (* Match Perfusion extraction to inlet to maintain constant volume (Chemostat principle) *)
        rPerfusionPumpOut := rPerfusionRateIn; 
        
        (* Stoichiometric pH Control (Lactic Acid Buffer) *)
        IF rPHLevel > (rSetpointPH + rDeadbandPH) THEN
            bAcidDosingValve := TRUE;
            bBaseDosingValve := FALSE;
        ELSIF rPHLevel < (rSetpointPH - rDeadbandPH) THEN
            bBaseDosingValve := TRUE;
            bAcidDosingValve := FALSE;
        ELSE
            bAcidDosingValve := FALSE;
            bBaseDosingValve := FALSE;
        END_IF;
        
        (* Monitor Critical Metabolic Alarms *)
        tAlarmDelay(IN := (rGlucoseConc < 0.5), PT := T#10S);
        IF tAlarmDelay.Q THEN
            bAlarm := TRUE;
            iState := 999;
        END_IF;
        
        IF NOT bEnable THEN
            iState := 0;
        END_IF;
        
    999: (* FAULT HANDLING *)
        bAlarm := TRUE;
        bSystemReady := FALSE;
        rO2SpargingValve := 0.0;
        rPerfusionPumpOut := 0.0;
        bAcidDosingValve := FALSE;
        bBaseDosingValve := FALSE;
        (* Maintain minimal agitation to prevent cell settling and death if safe to do so *)
        rAgitationOut := rTargetAgitation * 0.5;
        
        IF bEnable = FALSE AND bEmergencyStop = TRUE THEN
            iState := 0;
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
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
