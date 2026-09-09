import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Advanced Bio-Synthetic mRNA Vaccine High-Shear Micro-Fluidizer**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., 30,000 psi interaction chamber localized thermal mapping, lipid nanoparticle (LNP) size distribution feedback, and sterile barrier cascading pressure zones). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_mRNA_MicroFluidizer\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Advanced Bio-Synthetic mRNA Vaccine High-Shear Micro-Fluidizer

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_mRNA_MicroFluidizer
VAR_INPUT
    bSystemEnable         : BOOL;      (* Main system enable command from master DCS *)
    bEmergencyStop        : BOOL;      (* Hardware safety chain status (TRUE = OK) *)
    rInletPressure        : REAL;      (* Inlet feed pressure from formulation tanks (psi) *)
    rInteractionTemp      : REAL;      (* Localized thermal mapping in interaction chamber (deg C) *)
    rLNP_SizeMean         : REAL;      (* Real-time DLS lipid nanoparticle size feedback (nm) *)
    bSterileBarrierOK     : BOOL;      (* Cascading pressure zones sterile boundary status *)
    rPumpFlowRateReq      : REAL;      (* Requested flow rate for intensifier pump (L/min) *)
    rCoolingWaterFlow     : REAL;      (* Chilled water flow rate for heat exchanger (L/min) *)
END_VAR
VAR_OUTPUT
    bSystemReady          : BOOL;      (* System is ready for vaccine processing *)
    bProcessActive        : BOOL;      (* High-shear microfluidization is actively running *)
    rIntensifierPressure  : REAL;      (* Commanded stroke pressure to the intensifier pump (psi) *)
    rChillerValveCmd      : REAL;      (* Cooling valve command (0.0 to 100.0 %) *)
    bWarningLNPSize       : BOOL;      (* Warning: LNP size deviating from target formulation *)
    bCriticalAlarm        : BOOL;      (* Critical fault: thermal run-away or pressure loss *)
    iProcessState         : INT;       (* Current state of the fluidizer state machine *)
END_VAR
VAR
    iState                : INT := 0;  (* Internal state variable for processing *)
    tStartupDelay         : TON;       (* Timer for pressure stabilization *)
    tChillerDelay         : TON;       (* Timer for thermal stabilization *)
    rTargetPressure       : REAL := 30000.0; (* 30,000 psi operating pressure *)
    rMaxTempLimit         : REAL := 15.0;    (* Max allowable temperature for mRNA stability *)
    rTargetLNPSize        : REAL := 80.0;    (* Target LNP size in nm *)
    rLNPSizeTolerance     : REAL := 15.0;    (* +/- 15 nm acceptable range *)
    rKp                   : REAL := 2.5;     (* Proportional gain for chiller PID pseudo-code *)
    rErrorTemp            : REAL;            (* Temperature error for cooling loop *)
END_VAR

(* === MAIN LOGIC === *)
(* 1. Safety and Interlock Checks *)
IF NOT bEmergencyStop OR NOT bSterileBarrierOK THEN
    bSystemReady := FALSE;
    bProcessActive := FALSE;
    rIntensifierPressure := 0.0;
    rChillerValveCmd := 100.0; (* Failsafe: full cooling *)
    bCriticalAlarm := TRUE;
    iState := 999; (* Fault state *)
    iProcessState := iState;
    RETURN;
END_IF;

(* 2. Thermal Protection Overrides *)
IF rInteractionTemp > rMaxTempLimit THEN
    bCriticalAlarm := TRUE;
    rIntensifierPressure := 0.0; (* Drop pressure immediately to stop shear heating *)
    rChillerValveCmd := 100.0;
    iState := 999;
END_IF;

(* 3. LNP Quality Monitoring *)
IF ABS(rLNP_SizeMean - rTargetLNPSize) > rLNPSizeTolerance THEN
    bWarningLNPSize := TRUE;
ELSE
    bWarningLNPSize := FALSE;
END_IF;

(* 4. State Machine for High-Shear Process *)
CASE iState OF
    0: (* IDLE - Waiting for DCS Enable *)
        bSystemReady := TRUE;
        bProcessActive := FALSE;
        rIntensifierPressure := 0.0;
        bCriticalAlarm := FALSE;
        rChillerValveCmd := 0.0;
        
        IF bSystemEnable AND (rInletPressure > 50.0) THEN
            iState := 10; (* Move to priming *)
        END_IF;

    10: (* PRIMING - Pre-cooling and low pressure start *)
        bSystemReady := TRUE;
        bProcessActive := TRUE;
        rIntensifierPressure := 5000.0; (* Low pressure prime *)
        rChillerValveCmd := 50.0;
        
        tStartupDelay(IN := TRUE, PT := T#10S);
        IF tStartupDelay.Q THEN
            tStartupDelay(IN := FALSE);
            iState := 20;
        END_IF;

    20: (* RAMPING - Bring up to 30,000 psi *)
        rIntensifierPressure := rIntensifierPressure + 100.0;
        IF rIntensifierPressure >= rTargetPressure THEN
            rIntensifierPressure := rTargetPressure;
            iState := 30;
        END_IF;
        
        (* Simple P-control for thermal loop during ramp *)
        rErrorTemp := rInteractionTemp - 4.0; (* Target 4 deg C *)
        IF rErrorTemp > 0.0 THEN
            rChillerValveCmd := rChillerValveCmd + (rErrorTemp * rKp);
        END_IF;
        IF rChillerValveCmd > 100.0 THEN rChillerValveCmd := 100.0; END_IF;

    30: (* PRODUCTION - Steady state microfluidization *)
        rIntensifierPressure := rTargetPressure;
        
        (* Thermal regulation loop *)
        rErrorTemp := rInteractionTemp - 4.0;
        IF rErrorTemp > 0.0 THEN
            rChillerValveCmd := rChillerValveCmd + (rErrorTemp * rKp * 0.5);
        ELSE
            rChillerValveCmd := rChillerValveCmd - 5.0;
        END_IF;
        
        (* Valve saturation limits *)
        IF rChillerValveCmd > 100.0 THEN rChillerValveCmd := 100.0; END_IF;
        IF rChillerValveCmd < 10.0 THEN rChillerValveCmd := 10.0; END_IF;
        
        IF NOT bSystemEnable THEN
            iState := 40;
        END_IF;

    40: (* SHUTDOWN - Ramp down pressure safely *)
        rIntensifierPressure := rIntensifierPressure - 500.0;
        IF rIntensifierPressure <= 0.0 THEN
            rIntensifierPressure := 0.0;
            bProcessActive := FALSE;
            iState := 0;
        END_IF;

    999: (* FAULT - Requires hard reset *)
        bSystemReady := FALSE;
        bProcessActive := FALSE;
        IF NOT bEmergencyStop THEN
            (* Wait for E-stop clear *)
        ELSIF bSystemEnable = FALSE AND rInteractionTemp < 10.0 THEN
            bCriticalAlarm := FALSE;
            iState := 0;
        END_IF;

END_CASE;

(* Update external state tracker *)
iProcessState := iState;

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
