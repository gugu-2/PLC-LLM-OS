import os, json, uuid

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Semiconductor Plasma-Enhanced Chemical Vapor Deposition (PECVD)**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Silane/ammonia dual-frequency RF matching network dynamic tuning, showerhead impedance cross-coupling, and capacitive coupled plasma (CCP) sheath thickness estimation). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_PECVD_Reactor\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Semiconductor Plasma-Enhanced Chemical Vapor Deposition (PECVD)

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_PECVD_RF_Match_Controller
VAR_INPUT
    bEnable                 : BOOL;     (* Master enable signal for the PECVD control loop *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal (FALSE = Active E-Stop) *)
    rChamberPressure        : REAL;     (* Current chamber pressure in mTorr *)
    rSiH4FlowFeedback       : REAL;     (* Silane gas flow feedback in sccm *)
    rNH3FlowFeedback        : REAL;     (* Ammonia gas flow feedback in sccm *)
    rHF_ForwardPower        : REAL;     (* High-frequency (13.56 MHz) forward power in Watts *)
    rLF_ForwardPower        : REAL;     (* Low-frequency (400 kHz) forward power in Watts *)
    rRF_ReflectedPower      : REAL;     (* Combined reflected RF power in Watts *)
    rPlasmaImpedance_Real   : REAL;     (* Measured real part of plasma impedance in Ohms *)
    rPlasmaImpedance_Imag   : REAL;     (* Measured imaginary part of plasma impedance in Ohms *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;     (* System is ready for deposition (impedance matched) *)
    bPlasmaIgnited          : BOOL;     (* Indication that capacitive coupled plasma is struck *)
    rTuneCapacitorPos       : REAL;     (* Control signal for vacuum tune capacitor (0-100%) *)
    rLoadCapacitorPos       : REAL;     (* Control signal for vacuum load capacitor (0-100%) *)
    rEstimatedSheath        : REAL;     (* Calculated plasma sheath thickness in mm *)
    bAlarm                  : BOOL;     (* Fault alarm output (e.g., mismatch, reflection too high) *)
    iErrorCode              : INT;      (* Specific error code for HMI diagnostics *)
END_VAR
VAR
    iState                  : INT := 0; (* Internal state machine step *)
    tStabilizeTimer         : TON;      (* Timer for plasma stabilization *)
    tIgnitionTimeout        : TON;      (* Timeout for plasma ignition phase *)
    rTuneKp                 : REAL := 0.05; (* Proportional gain for tune capacitor *)
    rLoadKp                 : REAL := 0.075;(* Proportional gain for load capacitor *)
    rError_Real             : REAL;     (* Error in real impedance (Target: 50 Ohms) *)
    rError_Imag             : REAL;     (* Error in imaginary impedance (Target: 0 Ohms) *)
    rElectronDensity        : REAL;     (* Intermediate calculation for sheath *)
    rDebyeLength            : REAL;     (* Intermediate calculation for sheath *)
END_VAR

(* === MAIN LOGIC AND SAFETY INTERLOCKS === *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bPlasmaIgnited := FALSE;
    bAlarm := TRUE;
    iErrorCode := 9999; (* Critical Safety Interlock Triggered *)
    rTuneCapacitorPos := 0.0;
    rLoadCapacitorPos := 0.0;
    iState := 0;
    RETURN;
END_IF;

(* Evaluate Plasma State Based on Reflected Power and Forward Power *)
IF (rHF_ForwardPower > 50.0) AND (rRF_ReflectedPower < (rHF_ForwardPower * 0.2)) THEN
    bPlasmaIgnited := TRUE;
ELSE
    bPlasmaIgnited := FALSE;
END_IF;

(* Main PECVD RF Match State Machine *)
CASE iState OF
    0: (* IDLE & INITIALIZATION *)
        bSystemReady := FALSE;
        bAlarm := FALSE;
        iErrorCode := 0;
        rTuneCapacitorPos := 50.0; (* Preset to mid-range for faster tuning *)
        rLoadCapacitorPos := 50.0;
        
        IF bEnable AND (rChamberPressure > 1.0) AND (rChamberPressure < 10.0) THEN
            (* Pressure is in acceptable striking regime for SiH4/NH3 mix *)
            iState := 10;
        END_IF;

    10: (* IGNITION PHASE *)
        (* Wait for forward power to be applied and plasma to strike *)
        tIgnitionTimeout(IN := TRUE, PT := T#3S);
        
        IF bPlasmaIgnited THEN
            tIgnitionTimeout(IN := FALSE);
            iState := 20;
        ELSIF tIgnitionTimeout.Q THEN
            (* Failed to strike plasma within 3 seconds *)
            tIgnitionTimeout(IN := FALSE);
            bAlarm := TRUE;
            iErrorCode := 1001; (* Ignition failure *)
            iState := 99; (* Fault state *)
        END_IF;

    20: (* TUNING & IMPEDANCE MATCHING *)
        (* Target impedance for RF generator is typically 50 + j0 Ohms *)
        rError_Real := 50.0 - rPlasmaImpedance_Real;
        rError_Imag := 0.0 - rPlasmaImpedance_Imag;
        
        (* Proportional feedback loop for vacuum capacitors *)
        (* Note: Tune primarily affects imaginary part, Load primarily affects real part in L-type network *)
        rTuneCapacitorPos := rTuneCapacitorPos + (rTuneKp * rError_Imag);
        rLoadCapacitorPos := rLoadCapacitorPos + (rLoadKp * rError_Real);
        
        (* Clamp capacitor positions *)
        IF rTuneCapacitorPos > 100.0 THEN rTuneCapacitorPos := 100.0; END_IF;
        IF rTuneCapacitorPos < 0.0 THEN rTuneCapacitorPos := 0.0; END_IF;
        IF rLoadCapacitorPos > 100.0 THEN rLoadCapacitorPos := 100.0; END_IF;
        IF rLoadCapacitorPos < 0.0 THEN rLoadCapacitorPos := 0.0; END_IF;
        
        (* Check if matched *)
        IF (ABS(rError_Real) < 2.0) AND (ABS(rError_Imag) < 2.0) AND (rRF_ReflectedPower < 10.0) THEN
            tStabilizeTimer(IN := TRUE, PT := T#2S);
            IF tStabilizeTimer.Q THEN
                tStabilizeTimer(IN := FALSE);
                iState := 30;
            END_IF;
        ELSE
            tStabilizeTimer(IN := FALSE);
        END_IF;

    30: (* DEPOSITION AND METROLOGY *)
        bSystemReady := TRUE;
        
        (* Calculate approximated CCP Sheath Thickness based on Child-Langmuir law simplifications *)
        (* and dual-frequency cross-coupling metrics. Highly empirical formulation for this reactor. *)
        IF rHF_ForwardPower > 0.0 THEN
            rElectronDensity := (rHF_ForwardPower * 1.5) / (rChamberPressure * 0.1);
            rDebyeLength := SQRT(2.5 / (rElectronDensity + 0.001)); (* Avoid div by zero *)
            
            (* Final sheath estimate incorporates LF power driving the ion bombardment *)
            rEstimatedSheath := 3.14 * rDebyeLength * (1.0 + (rLF_ForwardPower / rHF_ForwardPower));
        END_IF;
        
        (* Continuous minor tuning to maintain match during deposition drifts *)
        rError_Real := 50.0 - rPlasmaImpedance_Real;
        rError_Imag := 0.0 - rPlasmaImpedance_Imag;
        rTuneCapacitorPos := rTuneCapacitorPos + (rTuneKp * 0.1 * rError_Imag); (* Reduced gain during run *)
        rLoadCapacitorPos := rLoadCapacitorPos + (rLoadKp * 0.1 * rError_Real);
        
        IF NOT bEnable OR NOT bPlasmaIgnited THEN
            iState := 0;
        END_IF;
        
    99: (* FAULT HANDLING *)
        bSystemReady := FALSE;
        rTuneCapacitorPos := 0.0;
        rLoadCapacitorPos := 0.0;
        (* Require manual reset of bEnable to clear fault *)
        IF NOT bEnable THEN
            bAlarm := FALSE;
            iErrorCode := 0;
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

filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
