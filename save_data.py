import json, uuid, os

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V4 Persona: a 50+ years experienced Chief PLC Architect & Control Systems PhD. 
Your logic must include advanced Non-Linear PID with Anti-Windup, 3-level cascade control, digital low-pass filtering, predictive anomaly detection, and multi-layered hardware interlocks. Output the most elite, mathematically rigorous, and structurally flawless IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Automated Semiconductor Wafer Electroplating (ECD) Bath Chemical Dosing and Anode Current Density**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_SemiECD_PlatingControl\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
   [ ] Total chars >= 2000
6. REPLY with: EVOLUTION COMPLETE: Automated Semiconductor Wafer Electroplating (ECD) Bath Chemical Dosing and Anode Current Density"""

code = """```iec-st
FUNCTION_BLOCK FB_SemiECD_PlatingControl
VAR_INPUT
    (* System & Safety Interlocks *)
    bEnable                     : BOOL;     (* Main sequence enable from SCADA *)
    bEStop                      : BOOL;     (* Hardware E-Stop OK = TRUE *)
    bInterlocksOK               : BOOL;     (* Fume hood closed, exhaust active, leakage sensors OK *)
    
    (* Process Target Parameters *)
    rWaferArea_cm2              : REAL;     (* Calculated exposed area for plating based on pattern density *)
    rTargetThickness_um         : REAL;     (* Desired Cu deposition thickness *)
    
    (* Real-time Bath Metrology *)
    rCuConcentration_gL         : REAL;     (* Spectroscopic Cu++ ion concentration *)
    rAcidConcentration_gL       : REAL;     (* Suppressor/Accelerator Acid concentration *)
    rBathTemp_C                 : REAL;     (* RTD Bath temperature feedback *)
    rBathLevel_mm               : REAL;     (* Ultrasonic Electrolyte level *)
    
    (* Electrical Feedback from Rectifier *)
    rActualCurrent_A            : REAL;     (* Measured anode current *)
    rActualVoltage_V            : REAL;     (* Measured cell voltage *)
END_VAR
VAR_OUTPUT
    (* Process Status & Commands *)
    bSystemReady                : BOOL;     (* Ready for wafer handling robot entry *)
    bPlatingActive              : BOOL;     (* Main rectifier active status *)
    rAnodeCurrentSP_A           : REAL;     (* Current setpoint out to rectifier *)
    
    (* Advanced Chemical Dosing Control *)
    rDosingPumpSpeed_Cu_RPM     : REAL;     (* Cu replenishment peristaltic pump control *)
    rDosingPumpSpeed_Acid_RPM   : REAL;     (* Acid/additive replenishment pump control *)
    
    (* System Diagnostics *)
    bAlarm                      : BOOL;     (* Global fault flag *)
    iErrorCode                  : INT;      (* Specific fault code for HMI reporting *)
    rEstTimeRemaining_s         : REAL;     (* Calculated process completion time *)
END_VAR
VAR
    (* Sequential Control State Management *)
    iState                      : INT := 0;
    
    (* DSP: Digital Low-pass Filtering *)
    rFilteredVoltage            : REAL;
    rFilteredCurrent            : REAL;
    rAlpha                      : REAL := 0.125; (* Exponential moving average smoothing factor *)
    
    (* Cascade Control: Level 1 - Thickness Trajectory (Outer Loop) *)
    rThicknessError             : REAL;
    rThicknessInt               : REAL;
    rThicknessKp                : REAL := 3.2;
    rThicknessKi                : REAL := 0.08;
    rThicknessMaxInt            : REAL := 60.0;
    
    (* Cascade Control: Level 2 - Current Density Setpoint (Middle Loop) *)
    rDensitySP                  : REAL;
    
    (* Process Modeling Constants *)
    rFaradayEfficiency          : REAL := 0.98;
    rCuDensity_g_cm3            : REAL := 8.96;
    rMolarMass_Cu               : REAL := 63.546;
    rPlatedThickness            : REAL := 0.0;
    rDepositionRate_ums         : REAL;
    
    (* Predictive Anomaly Detection (Impedance Monitoring) *)
    rCellResistance             : REAL;
    rResistanceBaseline         : REAL := 0.0;
    rResistanceThreshold        : REAL := 1.75; (* Maximum Ohmic deviation indicating anode passivation *)
    tPassivationTimer           : TON;
    rVoltageDerivative          : REAL;
    rLastFilteredVoltage        : REAL;
    
    (* General Timers *)
    tStepTimer                  : TON;
    tDosingInterval             : TON;
END_VAR

(* ===================================================================== *)
(* 1. HARDWARE MULTI-LAYERED INTERLOCKS & SAFETY                         *)
(* ===================================================================== *)
IF NOT bEStop OR NOT bInterlocksOK THEN
    bSystemReady := FALSE;
    bPlatingActive := FALSE;
    rAnodeCurrentSP_A := 0.0;
    rDosingPumpSpeed_Cu_RPM := 0.0;
    rDosingPumpSpeed_Acid_RPM := 0.0;
    bAlarm := TRUE;
    iErrorCode := 9001; (* Critical hardware interlock trip - IMMEDIATE ABORT *)
    iState := 99;
    RETURN;
END_IF;

(* ===================================================================== *)
(* 2. DSP: DIGITAL LOW-PASS FILTERING FOR NOISY RECTIFIER FEEDBACK       *)
(* ===================================================================== *)
rLastFilteredVoltage := rFilteredVoltage;
rFilteredVoltage := rFilteredVoltage + rAlpha * (rActualVoltage_V - rFilteredVoltage);
rFilteredCurrent := rFilteredCurrent + rAlpha * (rActualCurrent_A - rFilteredCurrent);
rVoltageDerivative := rFilteredVoltage - rLastFilteredVoltage;

(* ===================================================================== *)
(* 3. PREDICTIVE ANOMALY DETECTION (IMPEDANCE & PASSIVATION ANALYSIS)    *)
(* ===================================================================== *)
(* Calculate apparent dynamic resistance to detect anode passivation or bubble masking *)
IF rFilteredCurrent > 0.5 THEN
    rCellResistance := rFilteredVoltage / rFilteredCurrent;
ELSE
    rCellResistance := 0.0;
END_IF;

(* Passivation detection: Sustained elevated resistance beyond baseline threshold *)
IF (rCellResistance > (rResistanceBaseline + rResistanceThreshold)) AND (iState = 30) THEN
    tPassivationTimer(IN := TRUE, PT := T#2.5S);
    IF tPassivationTimer.Q THEN
        iState := 99;
        iErrorCode := 8005; (* Predictive Maintenance Flag: Severe Anode Passivation or Substrate Dewetting detected *)
    END_IF;
ELSE
    tPassivationTimer(IN := FALSE);
END_IF;

(* ===================================================================== *)
(* 4. MAIN STATE MACHINE (WAFER PLATING SEQUENCE)                        *)
(* ===================================================================== *)
CASE iState OF
    0: (* STATE 0: INITIALIZATION & BATH CONDITION VERIFICATION *)
        bSystemReady := FALSE;
        bAlarm := FALSE;
        iErrorCode := 0;
        rThicknessInt := 0.0;
        rPlatedThickness := 0.0;
        rAnodeCurrentSP_A := 0.0;
        
        (* Verify strict bath physical chemistry limits *)
        IF rBathLevel_mm > 240.0 AND rBathTemp_C > 22.0 AND rBathTemp_C < 28.0 THEN
            iState := 10;
        END_IF;
        
    10: (* STATE 10: IDLE & BASELINE CHEMICAL DOSING *)
        bSystemReady := TRUE;
        bPlatingActive := FALSE;
        rAnodeCurrentSP_A := 0.0;
        
        (* Non-linear baseline dosing based on evaporation/drag-out *)
        IF rCuConcentration_gL < 42.0 THEN
            rDosingPumpSpeed_Cu_RPM := (42.0 - rCuConcentration_gL) * 2.5;
        ELSE
            rDosingPumpSpeed_Cu_RPM := 0.0;
        END_IF;
        
        IF bEnable THEN
            bSystemReady := FALSE;
            rResistanceBaseline := rCellResistance; (* Snapshot ideal wetting resistance *)
            tStepTimer(IN := FALSE);
            iState := 20;
        END_IF;
        
    20: (* STATE 20: PRE-DOSE, WETTING & CIRCULATION HOMOGENIZATION *)
        (* High speed acid circulation before applying electrical field to ensure wetting *)
        rDosingPumpSpeed_Acid_RPM := 45.0;
        tStepTimer(IN := TRUE, PT := T#4S);
        IF tStepTimer.Q THEN
            tStepTimer(IN := FALSE);
            iState := 30;
        END_IF;
        
    30: (* STATE 30: ACTIVE PLATING WITH 3-LEVEL CASCADE PID CONTROL *)
        bPlatingActive := TRUE;
        
        (* LEVEL 1: Thickness Trajectory Control (Outer Loop) *)
        rThicknessError := rTargetThickness_um - rPlatedThickness;
        
        (* Anti-Windup Conditional Integration *)
        IF rThicknessError > 0.0 THEN
            rThicknessInt := rThicknessInt + (rThicknessError * rThicknessKi);
        END_IF;
        (* Saturation limits *)
        IF rThicknessInt > rThicknessMaxInt THEN rThicknessInt := rThicknessMaxInt; END_IF;
        IF rThicknessInt < 0.0 THEN rThicknessInt := 0.0; END_IF;
        
        (* LEVEL 2: Current Density Target (Middle Loop) *)
        rDensitySP := (rThicknessError * rThicknessKp) + rThicknessInt;
        
        (* LEVEL 3: Non-Linear Geometric Mapping (Inner Target Translation) *)
        (* Translates ideal current density (mA/cm2) to gross rectifier current (A) *)
        rAnodeCurrentSP_A := rDensitySP * (rWaferArea_cm2 / 1000.0);
        
        (* Faraday Deposition Modeling (Feed-forward thickness estimator) *)
        rDepositionRate_ums := (rFilteredCurrent * rFaradayEfficiency * 3.29E-4) / rWaferArea_cm2;
        rPlatedThickness := rPlatedThickness + rDepositionRate_ums;
        
        (* End-of-Run Prediction *)
        IF rDepositionRate_ums > 0.0001 THEN
            rEstTimeRemaining_s := rThicknessError / rDepositionRate_ums;
        ELSE
            rEstTimeRemaining_s := 9999.0;
        END_IF;
        
        (* Dynamic real-time chemical replenishment proportional to actual charge consumed *)
        rDosingPumpSpeed_Cu_RPM := (rFilteredCurrent * 0.15) + 5.0;
        rDosingPumpSpeed_Acid_RPM := (rFilteredCurrent * 0.05);
        
        (* Sequence Completion Check *)
        IF rPlatedThickness >= rTargetThickness_um THEN
            bPlatingActive := FALSE;
            rAnodeCurrentSP_A := 0.0;
            iState := 40;
        END_IF;
        
    40: (* STATE 40: POST-WASH / DRAIN DOWN / RELAXATION *)
        rDosingPumpSpeed_Cu_RPM := 0.0;
        rDosingPumpSpeed_Acid_RPM := 0.0;
        tStepTimer(IN := TRUE, PT := T#8S);
        IF tStepTimer.Q THEN
            IF NOT bEnable THEN
                iState := 10;
            END_IF;
        END_IF;
        
    99: (* STATE 99: SYSTEM FAULT LATCH & SAFE ABORT *)
        bSystemReady := FALSE;
        bPlatingActive := FALSE;
        rAnodeCurrentSP_A := 0.0;
        rDosingPumpSpeed_Cu_RPM := 0.0;
        rDosingPumpSpeed_Acid_RPM := 0.0;
        bAlarm := TRUE;
        
        (* Requires manual SCADA reset (dropping Enable) while interlocks are clear *)
        IF NOT bEnable AND bInterlocksOK AND bEStop THEN
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
