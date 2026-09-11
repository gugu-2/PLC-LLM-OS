import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Industrial Heavy-Duty Gas Turbine (CCGT) Dry Low NOx (DLN) Combustion**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., pilot/premix fuel staging ratio optimization, combustion dynamics acoustic humming feedback, and primary zone temperature calculated mapping). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_GasTurbine_DLN\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Industrial Heavy-Duty Gas Turbine (CCGT) Dry Low NOx (DLN) Combustion

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_CCGT_DLN_Combustion_Control
(*
  ===================================================================================
  LUMINA AI CLOUD SWARM - ELITE SYNTHETIC DATA ARCHITECT
  Domain: Industrial Heavy-Duty Gas Turbine (CCGT) Dry Low NOx (DLN) Combustion
  Description: Advanced control algorithm for DLN combustion staging, acoustic humming 
               suppression, and Primary Zone Temperature (PZT) calculations.
  ===================================================================================
*)
VAR_INPUT
    bEnableSystem       : BOOL;     (* System master enable interlock *)
    bTurbineTrip        : BOOL;     (* Emergency trip condition from protection system *)
    rMegawattDemand     : REAL;     (* MW load demand from grid controller [MW] *)
    rCompressorDischT   : REAL;     (* Compressor discharge temperature (TCD) [deg C] *)
    rCompressorDischP   : REAL;     (* Compressor discharge pressure (PCD) [bar] *)
    rExhaustTemp        : REAL;     (* Turbine exhaust temperature (Tx) [deg C] *)
    rAcousticIntensity  : REAL;     (* Combustion dynamics acoustic amplitude [psi] *)
    rFuelGasPressure    : REAL;     (* Supply pressure of the fuel gas [bar] *)
END_VAR
VAR_OUTPUT
    bSystemReady        : BOOL;     (* DLN combustion system ready for operation *)
    bCombustionAlarm    : BOOL;     (* Acoustic or temperature abnormality alarm *)
    rPilotFuelStroke    : REAL;     (* Pilot fuel valve stroke command [%] *)
    rPremixFuelStroke   : REAL;     (* Premix fuel valve stroke command [%] *)
    rQuatFuelStroke     : REAL;     (* Quaternary fuel valve stroke command [%] *)
    iStagingMode        : INT;      (* Current DLN operating mode (1=Primary, 2=Lean-Lean, 3=Premix) *)
END_VAR
VAR
    iState              : INT := 0; 
    rPZT_Calc           : REAL := 0.0; (* Calculated Primary Zone Temperature *)
    rFuelSplitRatio     : REAL := 0.0; (* Ratio of Premix to Pilot *)
    tAcousticFilter     : TON;
    tModeTransition     : TON;
    rHummingGain        : REAL := 1.25;
    rMaxPZT             : REAL := 1450.0; (* Maximum allowed PZT in deg C *)
END_VAR

(* === MAIN LOGIC === *)
IF bTurbineTrip OR NOT bEnableSystem THEN
    bSystemReady := FALSE;
    bCombustionAlarm := TRUE;
    rPilotFuelStroke := 0.0;
    rPremixFuelStroke := 0.0;
    rQuatFuelStroke := 0.0;
    iStagingMode := 0;
    iState := 0;
    RETURN;
END_IF;

(* Primary Zone Temperature (PZT) Calculation 
   Simplified empirical mapping based on TCD, Tx, and MW demand *)
rPZT_Calc := rCompressorDischT + (rExhaustTemp * 1.15) + (rMegawattDemand * 2.45);

(* Acoustic Humming Check *)
tAcousticFilter(IN := (rAcousticIntensity > 2.5), PT := T#2S);
IF tAcousticFilter.Q THEN
    bCombustionAlarm := TRUE;
    (* Apply acoustic suppression tuning *)
    rHummingGain := 0.85; 
ELSE
    bCombustionAlarm := FALSE;
    rHummingGain := 1.0;
END_IF;

(* DLN Staging State Machine *)
CASE iState OF
    0: (* OFF / PURGE *)
        bSystemReady := TRUE;
        rPilotFuelStroke := 10.0;
        rPremixFuelStroke := 0.0;
        IF rMegawattDemand > 5.0 THEN
            iState := 10;
        END_IF;

    10: (* PRIMARY MODE - Ignition & low load *)
        iStagingMode := 1;
        rPilotFuelStroke := 30.0 + (rMegawattDemand * 0.5);
        rPremixFuelStroke := 0.0;
        rQuatFuelStroke := 0.0;
        
        IF rMegawattDemand > 35.0 AND rPZT_Calc > 800.0 THEN
            tModeTransition(IN := TRUE, PT := T#5S);
            IF tModeTransition.Q THEN
                tModeTransition(IN := FALSE);
                iState := 20;
            END_IF;
        ELSE
            tModeTransition(IN := FALSE, PT := T#5S);
        END_IF;

    20: (* LEAN-LEAN MODE - Intermediate load *)
        iStagingMode := 2;
        rFuelSplitRatio := 0.4;
        rPilotFuelStroke := (50.0 + rMegawattDemand) * (1.0 - rFuelSplitRatio);
        rPremixFuelStroke := (50.0 + rMegawattDemand) * rFuelSplitRatio;
        
        IF rMegawattDemand > 70.0 AND rPZT_Calc > 1100.0 THEN
            tModeTransition(IN := TRUE, PT := T#8S);
            IF tModeTransition.Q THEN
                tModeTransition(IN := FALSE);
                iState := 30;
            END_IF;
        ELSE
            tModeTransition(IN := FALSE, PT := T#8S);
        END_IF;

    30: (* PREMIX MODE - High load, Low NOx operation *)
        iStagingMode := 3;
        (* Modulate fuel split heavily favoring premix, adjusted by acoustic gain *)
        rFuelSplitRatio := 0.90 * rHummingGain;
        
        (* Safeguard on PZT *)
        IF rPZT_Calc > rMaxPZT THEN
            rFuelSplitRatio := rFuelSplitRatio * 0.95; (* Run richer on pilot temporarily to stabilize *)
        END_IF;
        
        rPilotFuelStroke := (100.0 + rMegawattDemand * 0.8) * (1.0 - rFuelSplitRatio);
        rPremixFuelStroke := (100.0 + rMegawattDemand * 0.8) * rFuelSplitRatio;
        rQuatFuelStroke := 5.0; (* Quaternary pegs for dynamic stabilization *)
        
        IF rMegawattDemand < 60.0 THEN
            iState := 20;
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
