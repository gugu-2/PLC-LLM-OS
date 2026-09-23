import json, uuid, os

os.makedirs('data/swarm_raw', exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V5 Persona: a 60+ years experienced God-Tier PLC Architect & Cyber-Physical Systems Post-Doc. 
Your logic must include advanced State-Space Modeling, Model Predictive Control (MPC) concepts, Non-Linear PID with Anti-Windup, and extreme multi-layer hardware safety matrices. Output the most elite, mathematically rigorous, and structurally flawless IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Advanced Pharmaceutical Nanoparticle Encapsulation Microfluidic Mixing Ratio and Pressure Drop**

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
   code = \"\"\"```iec-st\nFUNCTION_BLOCK FB_Pharma_NanoparticleMicrofluidics\n//...\nEND_FUNCTION_BLOCK\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Advanced Pharmaceutical Nanoparticle Encapsulation Microfluidic Mixing Ratio and Pressure Drop"""

code = """```iec-st
FUNCTION_BLOCK FB_Pharma_NanoparticleMicrofluidics
VAR_INPUT
    (* Critical process inputs for microfluidic encapsulation *)
    bEnable                 : BOOL;     (* System enable signal for the encapsulation process *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal; extreme multi-layer hardware safety interlock *)
    rFlowRateAqueous        : REAL;     (* Main aqueous phase flow rate [mL/min], measured via Coriolis meter *)
    rFlowRateLipid          : REAL;     (* Organic/lipid phase flow rate [mL/min], measured via Coriolis meter *)
    rPressureInlet          : REAL;     (* Microfluidic chip inlet pressure [bar], high resolution sensor *)
    rPressureOutlet         : REAL;     (* Microfluidic chip outlet pressure [bar], high resolution sensor *)
    rTemperatureMixer       : REAL;     (* Mixer zone temperature [deg C], RTD PT100 feedback *)
    rTargetRatio            : REAL;     (* Target volumetric flow ratio Aqueous:Lipid for precise nanoparticle sizing *)
    rTargetPressureDrop     : REAL;     (* Desired pressure drop [bar] across the microfluidic junction *)
END_VAR
VAR_OUTPUT
    (* Critical process outputs and actuators *)
    bSystemReady            : BOOL;     (* System ready status for upstream automation sequence *)
    rPumpCmdAqueous         : REAL;     (* Aqueous pump speed/stroke command [0.0 - 100.0 %] *)
    rPumpCmdLipid           : REAL;     (* Lipid pump speed/stroke command [0.0 - 100.0 %] *)
    rCalculatedPressureDrop : REAL;     (* Calculated DP across the microfluidic chip [bar] *)
    bAlarmPressureHigh      : BOOL;     (* High pressure drop alarm, indicates potential chip fouling or clogging *)
    bAlarmRatioMismatch     : BOOL;     (* Flow ratio out of tolerance alarm, impacts particle Polydispersity Index (PDI) *)
    bAlarmTemperature       : BOOL;     (* Temperature out of bounds, impacts lipid transition state *)
END_VAR
VAR
    (* State-Space and MPC internal variables *)
    iState                  : INT := 0; (* Internal state machine step index *)
    tStartupDelay           : TON;      (* Startup and flow stabilization timer *)
    tMixerStable            : TON;      (* Mixer temperature stabilization timer *)
    
    (* Non-Linear PID with Anti-Windup for Flow Ratio *)
    rErrorRatio             : REAL := 0.0;
    rIntegralRatio          : REAL := 0.0;
    rDerivativeRatio        : REAL := 0.0;
    rPrevErrorRatio         : REAL := 0.0;
    rActualRatio            : REAL := 0.0;
    
    (* PID Tuning Parameters with Gain Scheduling *)
    Kp_Base                 : REAL := 2.75;
    Ki_Base                 : REAL := 0.125;
    Kd_Base                 : REAL := 0.05;
    rKp_Active              : REAL;
    
    (* Anti-windup and Saturation Limits *)
    rMaxPumpCmd             : REAL := 100.0;
    rMinPumpCmd             : REAL := 0.0;
    rIntegralMax            : REAL := 45.0;
    rIntegralMin            : REAL := -45.0;
    
    (* Advanced Model Predictive Control (MPC) observer states *)
    rPredictedPressureDrop  : REAL;
    rModelError             : REAL;
    rFoulingFactor          : REAL := 1.0; (* Adaptive fouling estimation factor *)
END_VAR

(* === MAIN LOGIC === *)

(* 1. Extreme Multi-Layer Hardware Safety Matrix & Interlocks *)
IF NOT bEmergencyStop THEN
    (* Immediate deterministic halt *)
    bSystemReady := FALSE;
    bAlarmPressureHigh := TRUE;
    bAlarmRatioMismatch := TRUE;
    bAlarmTemperature := TRUE;
    
    rPumpCmdAqueous := 0.0;
    rPumpCmdLipid := 0.0;
    iState := 0;
    
    rIntegralRatio := 0.0;
    
    RETURN;
END_IF;

(* 2. Data Pre-Processing and Derived Variable Calculation *)
rCalculatedPressureDrop := rPressureInlet - rPressureOutlet;

IF rFlowRateLipid > 0.001 THEN
    rActualRatio := rFlowRateAqueous / rFlowRateLipid;
ELSE
    rActualRatio := 0.0;
END_IF;

(* 3. Model Predictive Control (MPC) Observer for Pressure Drop *)
(* Predicts expected DP based on fluid dynamics, total flow, and historical fouling *)
rPredictedPressureDrop := ((rFlowRateAqueous + rFlowRateLipid) * 0.42 * rFoulingFactor);
rModelError := rCalculatedPressureDrop - rPredictedPressureDrop;

(* Adaptive Fouling Update via Recursive State Estimation *)
IF rCalculatedPressureDrop > 1.0 AND rFlowRateAqueous > 5.0 THEN
    rFoulingFactor := rFoulingFactor + (rModelError * 0.001); 
END_IF;

(* 4. Safety Fault Detection Algorithms *)
IF rCalculatedPressureDrop > (rPredictedPressureDrop * 1.45) THEN
    bAlarmPressureHigh := TRUE;
ELSE
    bAlarmPressureHigh := FALSE;
END_IF;

IF rTemperatureMixer > 65.0 OR rTemperatureMixer < 15.0 THEN
    bAlarmTemperature := TRUE;
ELSE
    bAlarmTemperature := FALSE;
END_IF;

(* 5. Main State-Space Machine *)
CASE iState OF
    0: (* IDLE - Awaiting Command *)
        bSystemReady := FALSE;
        rPumpCmdAqueous := 0.0;
        rPumpCmdLipid := 0.0;
        rIntegralRatio := 0.0;
        IF bEnable AND NOT bAlarmTemperature THEN
            iState := 10;
        END_IF;

    10: (* PRIMING & TEMPERATURE STABILIZATION *)
        tStartupDelay(IN := TRUE, PT := T#15S);
        
        (* Low flow prime to purge air from microfluidic channels *)
        rPumpCmdAqueous := 15.0; 
        rPumpCmdLipid := 15.0;
        
        IF tStartupDelay.Q AND rTemperatureMixer >= 20.0 THEN
            tStartupDelay(IN := FALSE);
            iState := 20;
        END_IF;

    20: (* ADVANCED NON-LINEAR PID RATIO CONTROL *)
        bSystemReady := TRUE;
        
        (* Feed-forward action for Aqueous pump based on target throughput *)
        rPumpCmdAqueous := rFlowRateAqueous * 1.15; 
        
        (* Non-Linear Gain Scheduling based on error magnitude *)
        rErrorRatio := rTargetRatio - rActualRatio;
        IF ABS(rErrorRatio) > (rTargetRatio * 0.2) THEN
            rKp_Active := Kp_Base * 1.5; (* Aggressive gain for large deviations *)
        ELSE
            rKp_Active := Kp_Base;
        END_IF;
        
        (* Calculate Integral term with precise Anti-Windup *)
        rIntegralRatio := rIntegralRatio + (rErrorRatio * Ki_Base);
        IF rIntegralRatio > rIntegralMax THEN
            rIntegralRatio := rIntegralMax;
        ELSIF rIntegralRatio < rIntegralMin THEN
            rIntegralRatio := rIntegralMin;
        END_IF;
        
        (* Derivative term *)
        rDerivativeRatio := (rErrorRatio - rPrevErrorRatio) * Kd_Base;
        rPrevErrorRatio := rErrorRatio;
        
        (* Final Control Element Output for Lipid Pump *)
        (* Includes baseline feed-forward + P + I + D *)
        rPumpCmdLipid := (rFlowRateAqueous / rTargetRatio) * 1.05 + (rKp_Active * rErrorRatio) + rIntegralRatio + rDerivativeRatio;
        
        (* Actuator Saturation Clamping *)
        IF rPumpCmdLipid > rMaxPumpCmd THEN
            rPumpCmdLipid := rMaxPumpCmd;
        ELSIF rPumpCmdLipid < rMinPumpCmd THEN
            rPumpCmdLipid := rMinPumpCmd;
        END_IF;
        
        (* Ratio Out-of-Tolerance Alarm *)
        IF ABS(rErrorRatio) > (rTargetRatio * 0.15) THEN
            bAlarmRatioMismatch := TRUE;
        ELSE
            bAlarmRatioMismatch := FALSE;
        END_IF;
        
        (* State Transition logic *)
        IF NOT bEnable OR bAlarmPressureHigh OR bAlarmTemperature THEN
            iState := 30; (* Move to fault handling / shutdown *)
            tStartupDelay(IN := FALSE);
        END_IF;

    30: (* CONTROLLED SHUTDOWN / FAULT HANDLING *)
        bSystemReady := FALSE;
        rPumpCmdAqueous := rPumpCmdAqueous * 0.9; (* Soft ramp down *)
        rPumpCmdLipid := rPumpCmdLipid * 0.9;
        
        IF rPumpCmdAqueous < 1.0 AND rPumpCmdLipid < 1.0 THEN
            rPumpCmdAqueous := 0.0;
            rPumpCmdLipid := 0.0;
            IF NOT bEnable THEN
                iState := 0; (* Return to IDLE once cleared *)
            END_IF;
        END_IF;
        
END_CASE;

END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
