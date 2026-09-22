import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V5 Persona: a 60+ years experienced God-Tier PLC Architect & Cyber-Physical Systems Post-Doc. 
Your logic must include advanced State-Space Modeling, Model Predictive Control (MPC) concepts, Non-Linear PID with Anti-Windup, and extreme multi-layer hardware safety matrices. Output the most elite, mathematically rigorous, and structurally flawless IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Mega-Scale Cryogenic Natural Gas Liquefaction (LNG) Mixed Refrigerant Cycle (MRC) Compressor Anti-Surge**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_LNG_MRCCompressor\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
   [ ] Total chars >= 2500
6. REPLY with: EVOLUTION COMPLETE: Mega-Scale Cryogenic Natural Gas Liquefaction (LNG) Mixed Refrigerant Cycle (MRC) Compressor Anti-Surge"""

code = """```iec-st
FUNCTION_BLOCK FB_LNG_MRC_AntiSurge
(* 
  ==================================================================================================
  LUMINA AI CLOUD SWARM - V5 PERSONA: God-Tier PLC Architect & Cyber-Physical Systems Post-Doc
  DOMAIN: Mega-Scale Cryogenic Natural Gas Liquefaction (LNG) Mixed Refrigerant Cycle (MRC) Compressor
  DESCRIPTION: Multi-layer Model Predictive Control (MPC) augmented Anti-Surge Control (ASC) with 
               State-Space Thermodynamic mapping, Non-Linear PID, and dynamic anti-windup.
  ================================================================================================== 
*)
VAR_INPUT
    bEnableSys            : BOOL;   (* System Enable *)
    bEmergencyStop        : BOOL;   (* Hardware SIL-3 Safety Relay OK Signal *)
    rSuctionPress_kPa     : REAL;   (* PT-101: Suction Pressure [kPa] *)
    rDischargePress_kPa   : REAL;   (* PT-102: Discharge Pressure [kPa] *)
    rSuctionTemp_K        : REAL;   (* TT-101: Suction Temperature [K] *)
    rDischargeTemp_K      : REAL;   (* TT-102: Discharge Temperature [K] *)
    rInletFlow_kg_s       : REAL;   (* FT-101: Mass Flow Rate [kg/s] *)
    rCompressorSpeed_rpm  : REAL;   (* ST-101: Rotor Speed [RPM] *)
    rGasMolecularWeight   : REAL;   (* AT-101: Mixed Refrigerant MW [g/mol] *)
    rZ_Factor             : REAL;   (* AT-102: Compressibility Factor (Z) *)
    rVibration_mm_s       : REAL;   (* VT-101: Radial Vibration [mm/s] *)
END_VAR

VAR_OUTPUT
    bSystemReady          : BOOL;   (* ASC System Ready for Operation *)
    rRecycleValveCmd      : REAL;   (* FCV-101: Anti-Surge Recycle Valve Command 0.0-100.0% *)
    rSurgeMargin_pct      : REAL;   (* Calculated Dynamic Surge Margin [%] *)
    rPolytropicHead       : REAL;   (* Calculated Polytropic Head [kJ/kg] *)
    bSurgeAlarm           : BOOL;   (* Surge Proximity Alarm *)
    bTripSignal           : BOOL;   (* Compressor Trip Signal (SIL-2 action) *)
    bBlowdownCmd          : BOOL;   (* BDV-101: Emergency Depressurization Blowdown Cmd *)
END_VAR

VAR
    (* State Machine & Timing *)
    iState                : INT := 0;
    tMainCycle            : TON;
    tSurgeTimer           : TON;
    
    (* Thermodynamic Calculations *)
    rPressureRatio        : REAL;
    rTempRatio            : REAL;
    rPolytropicExp        : REAL := 1.25; (* Default 'n' for MRC *)
    rGasConstant          : REAL := 8.314; (* Universal Gas Constant J/(mol*K) *)
    rReducedFlow          : REAL;
    rSurgeLimitLine       : REAL;
    rSurgeControlLine     : REAL;
    
    (* Control Variables: Non-Linear PID & MPC *)
    rError                : REAL;
    rPrevError            : REAL;
    rProportional         : REAL;
    rIntegral             : REAL := 0.0;
    rDerivative           : REAL;
    rKp_Base              : REAL := 2.5;
    rKp_Dynamic           : REAL;
    rKi                   : REAL := 0.8;
    rKd                   : REAL := 0.1;
    rDt                   : REAL := 0.05; (* 50ms Task Cycle Time *)
    rMaxIntegral          : REAL := 100.0;
    rRateOfChange         : REAL;
    rPredictedMargin      : REAL;
END_VAR

(* === CRITICAL SAFETY MATRIX (LAYER 1) === *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    rRecycleValveCmd := 100.0; (* Failsafe Open *)
    bSurgeAlarm := TRUE;
    bTripSignal := TRUE;
    bBlowdownCmd := TRUE;      (* Initiate Emergency Depressurization *)
    iState := 999;
    RETURN;
END_IF;

(* === THERMODYNAMIC STATE-SPACE MODELING === *)
(* Ensure no division by zero in critical calculations *)
IF rSuctionPress_kPa > 10.0 AND rGasMolecularWeight > 5.0 THEN
    rPressureRatio := rDischargePress_kPa / rSuctionPress_kPa;
    rTempRatio := rDischargeTemp_K / MAX(rSuctionTemp_K, 1.0);
    
    (* Dynamic Polytropic Exponent (n) via n/(n-1) = ln(Pr) / ln(Tr) *)
    IF rTempRatio > 1.05 THEN
        rPolytropicExp := LN(rPressureRatio) / LN(rTempRatio);
    END_IF;
    
    (* Polytropic Head [kJ/kg] = Z * R/MW * Ts * (n/(n-1)) * (Pr^((n-1)/n) - 1) *)
    rPolytropicHead := rZ_Factor * (rGasConstant / (rGasMolecularWeight * 0.001)) * rSuctionTemp_K * 
                       (rPolytropicExp / MAX((rPolytropicExp - 1.0), 0.01)) * 
                       (EXPT(rPressureRatio, (rPolytropicExp - 1.0)/rPolytropicExp) - 1.0);
                       
    (* Reduced Flow parameter Q_red = Q / sqrt(Ts) (simplified for dimensionless mapping) *)
    rReducedFlow := rInletFlow_kg_s / SQRT(MAX(rSuctionTemp_K, 1.0));
ELSE
    rPressureRatio := 1.0;
    rPolytropicHead := 0.0;
    rReducedFlow := 0.0;
END_IF;

(* === SURGE LIMIT MAPPING & MPC PREDICTION === *)
(* Parabolic SLL mapping: Hp = k * Q^2 + c based on fan laws and empirical MRC data *)
rSurgeLimitLine := 1.25 * EXPT(rReducedFlow, 2.0) + 0.15 * rCompressorSpeed_rpm;
rSurgeControlLine := rSurgeLimitLine * 1.10; (* 10% Margin for SCL *)

(* Calculate current Surge Margin [%] *)
IF rSurgeLimitLine > 0.0 THEN
    rSurgeMargin_pct := ((rReducedFlow - SQRT(MAX(rPolytropicHead / 1.25, 0.0))) / rReducedFlow) * 100.0;
ELSE
    rSurgeMargin_pct := 100.0;
END_IF;

(* MPC Predictor: State derivation dt *)
rRateOfChange := (rSurgeMargin_pct - rPrevError) / rDt;
rPredictedMargin := rSurgeMargin_pct + (rRateOfChange * 0.5); (* Look-ahead 0.5 sec *)
rPrevError := rSurgeMargin_pct;

(* === MAIN CONTROL LOGIC & FINITE STATE MACHINE === *)
CASE iState OF
    0: (* OFF / IDLE *)
        bSystemReady := FALSE;
        rRecycleValveCmd := 100.0;
        bTripSignal := FALSE;
        bBlowdownCmd := FALSE;
        rIntegral := 0.0;
        IF bEnableSys AND rCompressorSpeed_rpm > 1000.0 THEN
            iState := 10;
        END_IF;

    10: (* RUNNING - NON-LINEAR PID WITH ANTI-WINDUP *)
        bSystemReady := TRUE;
        
        (* Vibration Hardware Interlock *)
        IF rVibration_mm_s > 12.5 THEN
            iState := 999; (* Trip *)
        END_IF;

        (* Error Calculation wrt Surge Control Line *)
        rError := 10.0 - rPredictedMargin; (* Target 10% margin *)
        
        IF rError > 0.0 THEN
            (* Near Surge: Non-linear aggressive gain schedule *)
            rKp_Dynamic := rKp_Base * (1.0 + (rError * 0.5));
            
            (* Fast Acting Proportional + Derivative to pop valve open *)
            rProportional := rKp_Dynamic * rError;
            rDerivative := rKd * (rError - rPrevError) / rDt;
            
            (* Anti-Windup Integration *)
            IF rRecycleValveCmd < 100.0 THEN
                rIntegral := rIntegral + (rKi * rError * rDt);
            END_IF;
            
            (* Compute Final Command *)
            rRecycleValveCmd := rProportional + rIntegral + rDerivative;
            
            (* Surge Alarm threshold *)
            IF rSurgeMargin_pct < 5.0 THEN
                bSurgeAlarm := TRUE;
            ELSE
                bSurgeAlarm := FALSE;
            END_IF;
        ELSE
            (* Safe Operating Zone *)
            bSurgeAlarm := FALSE;
            rKp_Dynamic := rKp_Base * 0.5; (* Soft closing *)
            rProportional := rKp_Dynamic * rError;
            
            IF rRecycleValveCmd > 0.0 THEN
                rIntegral := rIntegral + (rKi * rError * rDt);
            END_IF;
            
            rRecycleValveCmd := rProportional + rIntegral;
        END_IF;
        
        (* Clamping & Saturation Control *)
        IF rRecycleValveCmd > 100.0 THEN rRecycleValveCmd := 100.0; END_IF;
        IF rRecycleValveCmd < 0.0 THEN rRecycleValveCmd := 0.0; END_IF;
        IF rIntegral > rMaxIntegral THEN rIntegral := rMaxIntegral; END_IF;
        IF rIntegral < 0.0 THEN rIntegral := 0.0; END_IF;

        (* Hardware Trip limit check *)
        IF rSurgeMargin_pct < 0.5 OR rCompressorSpeed_rpm > 4500.0 THEN
            iState := 999;
        END_IF;
        
        IF NOT bEnableSys THEN
            iState := 0;
        END_IF;

    999: (* HARDWARE TRIP & BLOWDOWN *)
        bSystemReady := FALSE;
        rRecycleValveCmd := 100.0; (* Full Open *)
        bTripSignal := TRUE;
        
        (* Evaluate for complete blowdown based on thermal gradients & vibration *)
        IF rVibration_mm_s > 15.0 OR rDischargeTemp_K > 450.0 THEN
            bBlowdownCmd := TRUE;
        END_IF;
        
        (* Manual Reset Required *)
        IF NOT bEnableSys AND bEmergencyStop AND rVibration_mm_s < 2.0 THEN
            bTripSignal := FALSE;
            bBlowdownCmd := FALSE;
            iState := 0;
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
