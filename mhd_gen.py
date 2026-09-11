import json
import uuid
import os

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Next-Gen Magneto-Hydrodynamic (MHD) Marine Propulsion Thruster**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., 10-Tesla superconducting dipole magnet field stabilization, seawater electrolysis chlorine-gas scrubbing, and Lorentz force vectoring electrode switching). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_MHD_MarineThruster\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Next-Gen Magneto-Hydrodynamic (MHD) Marine Propulsion Thruster

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_MHD_MarineThruster
VAR_INPUT
    bEnableSystem          : BOOL;     (* Main system enable command *)
    bScram                 : BOOL;     (* Emergency shutdown safety interlock (Active LOW) *)
    rDipoleFieldTarget_T   : REAL;     (* Desired magnetic field strength (Tesla) *)
    rSeawaterFlow_m3s      : REAL;     (* Process variable: Seawater mass flow rate (m^3/s) *)
    rElectrodeCurrentCmd_A : REAL;     (* Command: Main Lorentz force drive current (Amps) *)
    rHeLHeLevel_pct        : REAL;     (* Liquid Helium cryogenic coolant level (%) *)
    rMagnetTemp_K          : REAL;     (* Superconducting magnet temperature (Kelvin) *)
    bGasScrubberActive     : BOOL;     (* Chlorine gas neutralization system status OK *)
END_VAR
VAR_OUTPUT
    bThrusterReady         : BOOL;     (* System ready for propulsion vectoring *)
    bQuenchAlarm           : BOOL;     (* Critical Alarm: Magnet quench impending *)
    bScrubberFault         : BOOL;     (* Alarm: Toxic chlorine accumulation *)
    rAppliedCurrent_A      : REAL;     (* Actuator output: Actual delivered current *)
    rVectorForce_kN        : REAL;     (* Estimated Lorentz thrust force (kiloNewtons) *)
    iOperatingState        : INT;      (* Current state machine step *)
END_VAR
VAR
    (* Internal State and Filters *)
    iState                 : INT := 0;
    rFilteredFlow          : REAL := 0.0;
    rFlowFilterCoeff       : REAL := 0.05; (* Low-pass filter coefficient for noise *)
    
    (* Timers *)
    tMagnetChargeTimer     : TON;
    tScrubberTimeout       : TON;
    
    (* Internal logic vars *)
    bMagnetStabilized      : BOOL := FALSE;
    bCoolingOk             : BOOL := FALSE;
    rMaxOperatingTemp_K    : REAL := 4.2;  (* Max allowable temp for SC dipole (NbTi) *)
    rMinHeLevel_pct        : REAL := 25.0; (* Min safety level for LHe *)
END_VAR

(* === MAIN LOGIC === *)

(* 1. Safety Interlocks (Highest Priority) *)
IF NOT bScram THEN
    (* SCRAM active (LOW): Immediate total shutdown *)
    iState := 999;
    bThrusterReady := FALSE;
    rAppliedCurrent_A := 0.0;
    bQuenchAlarm := FALSE;
    bScrubberFault := FALSE;
    iOperatingState := iState;
    RETURN;
END_IF;

(* 2. Cryogenic & Superconducting Health Monitoring *)
bCoolingOk := (rHeLHeLevel_pct >= rMinHeLevel_pct) AND (rMagnetTemp_K <= rMaxOperatingTemp_K);
IF NOT bCoolingOk AND iState > 0 AND iState < 999 THEN
    bQuenchAlarm := TRUE;
    iState := 999; (* Force fault shutdown to prevent explosive boil-off *)
END_IF;

(* 3. Seawater Flow Sensor Noise Filtering (EWMA Filter) *)
rFilteredFlow := (rFlowFilterCoeff * rSeawaterFlow_m3s) + ((1.0 - rFlowFilterCoeff) * rFilteredFlow);

(* 4. State Machine for Thruster Operation *)
CASE iState OF
    0: (* IDLE / OFF *)
        bThrusterReady := FALSE;
        rAppliedCurrent_A := 0.0;
        rVectorForce_kN := 0.0;
        bQuenchAlarm := FALSE;
        IF bEnableSystem AND bCoolingOk THEN
            iState := 10;
        END_IF;

    10: (* MAGNET CHARGING SEQUENCE *)
        (* Slowly ramp up the superconducting magnet to avoid quenching *)
        tMagnetChargeTimer(IN := TRUE, PT := T#30S);
        IF tMagnetChargeTimer.Q THEN
            tMagnetChargeTimer(IN := FALSE);
            bMagnetStabilized := TRUE;
            iState := 20;
        END_IF;

    20: (* ENVIRONMENTAL SYSTEMS CHECK *)
        (* Ensure seawater electrolysis byproducts (Chlorine) are managed *)
        IF NOT bGasScrubberActive THEN
            tScrubberTimeout(IN := TRUE, PT := T#2S);
            IF tScrubberTimeout.Q THEN
                bScrubberFault := TRUE;
                iState := 999; (* Fault *)
            END_IF;
        ELSE
            tScrubberTimeout(IN := FALSE);
            bScrubberFault := FALSE;
            iState := 30; (* Ready for Drive *)
        END_IF;

    30: (* THRUSTER DRIVE ACTIVE *)
        bThrusterReady := TRUE;
        
        (* Vector force calculation: F = I * L * B (Lorentz Force Law)
           Assuming effective electrode length L = 2.0 meters for this scale *)
        rVectorForce_kN := (rElectrodeCurrentCmd_A * 2.0 * rDipoleFieldTarget_T) / 1000.0;
        
        (* Modulate applied current based on available filtered seawater flow to prevent cavitation/boiling *)
        IF rFilteredFlow > 5.0 THEN
            rAppliedCurrent_A := rElectrodeCurrentCmd_A;
        ELSE
            (* Current throttling if flow is too low *)
            rAppliedCurrent_A := rElectrodeCurrentCmd_A * 0.5;
        END_IF;
        
        IF NOT bEnableSystem THEN
            bThrusterReady := FALSE;
            rAppliedCurrent_A := 0.0;
            bMagnetStabilized := FALSE;
            iState := 0;
        END_IF;
        
    999: (* FAULT / SCRAM RECOVERY *)
        bThrusterReady := FALSE;
        rAppliedCurrent_A := 0.0;
        tMagnetChargeTimer(IN := FALSE);
        tScrubberTimeout(IN := FALSE);
        
        (* Require manual reset of Enable command to recover from SCRAM/Fault *)
        IF NOT bEnableSystem AND bScram AND bCoolingOk THEN
            iState := 0;
        END_IF;

END_CASE;

iOperatingState := iState;

END_FUNCTION_BLOCK
```"""

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
