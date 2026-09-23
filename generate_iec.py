import json, uuid, os
os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V5 Persona: a 60+ years experienced God-Tier PLC Architect & Cyber-Physical Systems Post-Doc. 
Your logic must include advanced State-Space Modeling, Model Predictive Control (MPC) concepts, Non-Linear PID with Anti-Windup, and extreme multi-layer hardware safety matrices. Output the most elite, mathematically rigorous, and structurally flawless IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Industrial Scale Closed-Loop Aquaculture System (RAS) Ozone Disinfection and Biofilter Nitrification Rate**

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
   code = \"\"\"```iec-st\nFUNCTION_BLOCK FB_Aquaculture_OzoneBiofilter\n//...\nEND_FUNCTION_BLOCK\n```\"\"\"
   record = {\"messages\": [{\"role\": \"user\", \"content\": prompt}, {\"role\": \"assistant\", \"content\": code}]}
   with open(f\"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json\", \"w\", encoding=\"utf-8\") as f:
       json.dump(record, f, ensure_ascii=False)
5. SELF-CHECK before saving - verify ALL:
   [ ] Fence is ```iec-st
   [ ] First code line: FUNCTION_BLOCK FB_<name>
   [ ] Has VAR_INPUT & VAR_OUTPUT sections
   [ ] Has END_IF; or END_CASE;
   [ ] Last code line: END_FUNCTION_BLOCK
   [ ] Closing fence: ```
   [ ] Total chars >= 2500
6. REPLY with: EVOLUTION COMPLETE: Industrial Scale Closed-Loop Aquaculture System (RAS) Ozone Disinfection and Biofilter Nitrification Rate"""

code = """```iec-st
FUNCTION_BLOCK FB_Aquaculture_OzoneBiofilter_Advanced_MPC

VAR_INPUT
    (* Mandatory Minimum 6 Physical Inputs *)
    bSystemEnable           : BOOL;     (* System master enable interlock *)
    bEmergencyStop          : BOOL;     (* Main ESTOP safety circuit (NC) *)
    rOzoneResidual_mgL      : REAL;     (* Measured O3 residual in contact chamber (mg/L) *)
    rORP_mV                 : REAL;     (* Oxidation-Reduction Potential (mV) *)
    rWaterTemp_C            : REAL;     (* Biofilter influent water temperature (deg C) *)
    rAmmonia_TAN_mgL        : REAL;     (* Total Ammonia Nitrogen (mg/L) entering biofilter *)
    rNitrite_NO2_mgL        : REAL;     (* Nitrite (mg/L) exiting biofilter *)
    rDissolvedOxygen_mgL    : REAL;     (* DO levels post-aeration cone (mg/L) *)
    rFlowRate_Lpm           : REAL;     (* Main loop flow rate (L/min) *)
    rpH_Value               : REAL;     (* System pH (critical for TAN to NH3 equilibrium) *)
    bOzoneGenerator_Fault   : BOOL;     (* Hardware fault from O3 generator *)
    bBiofilter_BypassValve  : BOOL;     (* Physical limit switch for bypass valve *)
END_VAR

VAR_OUTPUT
    (* Mandatory Minimum 5 Physical Outputs *)
    bSystemReady            : BOOL;     (* Global RAS readiness indicator *)
    bAlarmCritical          : BOOL;     (* Critical life-support alarm *)
    rOzoneDoseRate_gHr      : REAL;     (* Output setpoint to Ozone Generator (g/hr) *)
    rAlkalinityDose_mLpm    : REAL;     (* Dosing pump setpoint for NaOH/Bicarbonate (mL/min) *)
    rOxygenInjection_Lpm    : REAL;     (* Setpoint for pure O2 injection (L/min) *)
    bOzoneDestruct_Enable   : BOOL;     (* Enable signal for UV/Thermal ozone destruct unit *)
    bBiofilter_BackwashReq  : BOOL;     (* Request automatic backwash sequence *)
END_VAR

VAR
    (* Internal State and Timers *)
    iControlState           : INT := 0;
    tInitDelay              : TON;
    tSafetyMonitor          : TON;
    tBackwashTimer          : TON;
    
    (* Non-Linear PID variables for Ozone Control *)
    rO3_Error               : REAL;
    rO3_Error_Prev          : REAL;
    rO3_Integral            : REAL;
    rO3_Derivative          : REAL;
    rO3_Kp                  : REAL := 2.5;
    rO3_Ki                  : REAL := 0.15;
    rO3_Kd                  : REAL := 1.2;
    rO3_Integral_Max        : REAL := 50.0;
    rO3_Setpoint            : REAL := 0.05; (* mg/L max safe residual *)
    
    (* MPC / State-Space variables for Biofilter *)
    rNitrificationRate      : REAL;
    rEstimatedAmmonia_Next  : REAL;
    rOptimalTemp            : REAL := 25.0; (* deg C optimal for Nitrosomonas *)
    rTempFactor             : REAL;
    rpHFactor               : REAL;
    rAlkalinityReq          : REAL;
    
    (* Advanced Diagnostics *)
    bHardwareFail           : BOOL;
    bLethalToxicity         : BOOL;
    iSafetyMatrixCode       : DINT;
END_VAR

(* ==================================================================== *)
(* === MAIN LOGIC: SAFETY INTERLOCKS AND EMERGENCY SHUTDOWN MATRIX  === *)
(* ==================================================================== *)

IF NOT bEmergencyStop THEN
    (* Immediate catastrophic halt *)
    bSystemReady := FALSE;
    bAlarmCritical := TRUE;
    rOzoneDoseRate_gHr := 0.0;
    rAlkalinityDose_mLpm := 0.0;
    rOxygenInjection_Lpm := 10.0; (* Maintain life support O2 *)
    bOzoneDestruct_Enable := TRUE; (* Dump any remaining ozone *)
    iSafetyMatrixCode := 16#FF; (* ESTOP Code *)
    iControlState := 999; 
    RETURN;
END_IF;

bHardwareFail := bOzoneGenerator_Fault OR bBiofilter_BypassValve;

(* Lethal Toxicity Detection: Ammonia > 5.0 mg/L or Ozone > 0.15 mg/L or Nitrite > 2.0 mg/L *)
IF (rAmmonia_TAN_mgL > 5.0) OR (rOzoneResidual_mgL > 0.15) OR (rNitrite_NO2_mgL > 2.0) THEN
    bLethalToxicity := TRUE;
ELSE
    bLethalToxicity := FALSE;
END_IF;

IF bHardwareFail OR bLethalToxicity THEN
    bAlarmCritical := TRUE;
    bSystemReady := FALSE;
    rOzoneDoseRate_gHr := 0.0; (* Cut ozone immediately to protect biofilter *)
    iControlState := 900; (* Fault State *)
END_IF;

(* ==================================================================== *)
(* === ADVANCED CONTROL STATE MACHINE (MPC & NON-LINEAR PID)        === *)
(* ==================================================================== *)

CASE iControlState OF
    0:  (* IDLE / INITIALIZATION *)
        bSystemReady := FALSE;
        bAlarmCritical := FALSE;
        rOzoneDoseRate_gHr := 0.0;
        rAlkalinityDose_mLpm := 0.0;
        bOzoneDestruct_Enable := FALSE;
        
        IF bSystemEnable AND NOT bHardwareFail AND NOT bLethalToxicity THEN
            tInitDelay(IN := TRUE, PT := T#10S);
            IF tInitDelay.Q THEN
                tInitDelay(IN := FALSE);
                iControlState := 10;
            END_IF;
        END_IF;
        
    10: (* SYSTEM STARTUP & ORP STABILIZATION *)
        bSystemReady := TRUE;
        bOzoneDestruct_Enable := TRUE; (* Ensure destruct is on before generation *)
        
        (* Oxygen base level for fish life support *)
        rOxygenInjection_Lpm := 5.0 + (rFlowRate_Lpm * 0.01);
        
        IF rORP_mV > 250.0 THEN
            iControlState := 20;
        END_IF;
        
        IF NOT bSystemEnable THEN
            iControlState := 0;
        END_IF;

    20: (* NORMAL OPERATION: OZONE MPC & BIOFILTER NITRIFICATION OPTIMIZATION *)
        
        (* 1. Biofilter State-Space Model (Nitrification Kinetics) *)
        (* Nitrosomonas and Nitrobacter efficiency depends on Temp and pH *)
        rTempFactor := EXP(-0.5 * EXPT((rWaterTemp_C - rOptimalTemp)/5.0, 2.0));
        rpHFactor := EXP(-0.5 * EXPT((rpH_Value - 7.5)/0.8, 2.0));
        
        (* Calculate predicted nitrification rate (g N / day / m^3 ) *)
        rNitrificationRate := 0.85 * rAmmonia_TAN_mgL * rTempFactor * rpHFactor;
        
        (* Alkalinity consumption: 7.14 mg CaCO3 consumed per mg NH4+ oxidized *)
        rAlkalinityReq := rAmmonia_TAN_mgL * 7.14 * (rFlowRate_Lpm / 1000.0);
        rAlkalinityDose_mLpm := rAlkalinityReq * 1.05; (* 5% safety margin *)

        (* 2. Non-Linear PID for Ozone Dosing with Anti-Windup *)
        (* Target ORP is ~300mV for clear water, but must limit residual O3 *)
        rO3_Error := rO3_Setpoint - rOzoneResidual_mgL;
        
        (* Gain scheduling: Be highly aggressive if O3 exceeds setpoint (prevent biofilter wipeout) *)
        IF rO3_Error < 0.0 THEN
            rO3_Kp := 5.0;
            rO3_Ki := 0.5;
        ELSE
            rO3_Kp := 2.5;
            rO3_Ki := 0.15;
        END_IF;
        
        rO3_Integral := rO3_Integral + (rO3_Error * 0.1); (* 100ms assumed scan rate *)
        (* Anti-Windup Limit *)
        IF rO3_Integral > rO3_Integral_Max THEN
            rO3_Integral := rO3_Integral_Max;
        ELSIF rO3_Integral < 0.0 THEN
            rO3_Integral := 0.0;
        END_IF;
        
        rO3_Derivative := (rO3_Error - rO3_Error_Prev) / 0.1;
        rOzoneDoseRate_gHr := (rO3_Kp * rO3_Error) + (rO3_Ki * rO3_Integral) + (rO3_Kd * rO3_Derivative);
        
        IF rOzoneDoseRate_gHr < 0.0 THEN
            rOzoneDoseRate_gHr := 0.0;
        ELSIF rOzoneDoseRate_gHr > 100.0 THEN
            rOzoneDoseRate_gHr := 100.0; (* Max capacity of generator *)
        END_IF;
        
        rO3_Error_Prev := rO3_Error;
        
        (* 3. Biofilter Maintenance Predictor *)
        IF (rNitrificationRate < 0.2 * rAmmonia_TAN_mgL) AND (rAmmonia_TAN_mgL > 1.0) THEN
            (* Nitrification stalled, possible channeling or biomass loss *)
            bBiofilter_BackwashReq := TRUE;
        ELSE
            bBiofilter_BackwashReq := FALSE;
        END_IF;
        
        (* Oxygen Modulation based on DO deficit and Nitrification demand (4.57mg O2 per mg N) *)
        rOxygenInjection_Lpm := (10.0 - rDissolvedOxygen_mgL) * 2.0 + (rNitrificationRate * 0.1);

        IF NOT bSystemEnable THEN
            iControlState := 0;
        END_IF;

    900: (* FAULT RECOVERY / LOCKOUT *)
        rOzoneDoseRate_gHr := 0.0;
        bOzoneDestruct_Enable := TRUE;
        rOxygenInjection_Lpm := 15.0; (* Max emergency aeration *)
        rAlkalinityDose_mLpm := 0.0;
        
        IF NOT bLethalToxicity AND NOT bHardwareFail THEN
            (* Wait for operator manual reset via SystemEnable toggle *)
            IF NOT bSystemEnable THEN
                iControlState := 0;
            END_IF;
        END_IF;

    999: (* ESTOP / CATASTROPHIC *)
        (* Must power cycle or clear hardware estop first *)
        IF bEmergencyStop THEN
            iControlState := 900;
        END_IF;
        
END_CASE;

END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
