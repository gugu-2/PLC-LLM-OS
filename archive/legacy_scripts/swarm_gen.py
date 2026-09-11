import json
import uuid
import os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Next-Gen Subsea Multiphase Flow Meter (MPFM)**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Gamma-ray attenuation density cross-correlation, venturi delta-P capacitive phase fraction slip modeling, and deep-water temperature-pressure (PT) PVT compensation). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_Subsea_MPFM\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Next-Gen Subsea Multiphase Flow Meter (MPFM)

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_Subsea_MPFM
VAR_INPUT
    (* Required: at least 4-8 physical inputs with types and comments *)
    bEnable           : BOOL;     (* System enable signal for multiphase calculations *)
    bEmergencyStop    : BOOL;     (* Safety relay OK signal (TRUE = safe, FALSE = trip) *)
    rGammaCounts      : REAL;     (* Gamma-ray detector raw counts per second (cps) *)
    rVenturiDp        : REAL;     (* Venturi differential pressure across throat (mbar) *)
    rCapacitance      : REAL;     (* Coaxial capacitive sensor reading for water cut (pF) *)
    rLineTemp         : REAL;     (* Subsea flowline temperature (deg C) *)
    rLinePress        : REAL;     (* Subsea flowline absolute pressure (bar) *)
END_VAR
VAR_OUTPUT
    (* Required: at least 3-6 outputs with types and comments *)
    bSystemReady      : BOOL;     (* System ready status (diagnostics passed) *)
    rOilFlowRate      : REAL;     (* Standard condition oil flow rate (Sm3/h) *)
    rWaterFlowRate    : REAL;     (* Standard condition water flow rate (Sm3/h) *)
    rGasFlowRate      : REAL;     (* Standard condition gas flow rate (Sm3/h) *)
    rWaterLiquidRatio : REAL;     (* Water Liquid Ratio (WLR) as percentage (%) *)
    bAlarm            : BOOL;     (* Critical fault alarm output (e.g. sensor fail) *)
END_VAR
VAR
    (* Internal state and diagnostic variables *)
    iState            : INT := 0; (* Main execution state machine pointer *)
    tTimer            : TON;      (* General purpose settling timer *)
    tDiagTimer        : TON;      (* Diagnostic window timer *)

    (* PVT & Calibration Constants *)
    c_rGammaEmpty     : REAL := 150000.0; (* Reference gamma counts for empty pipe *)
    c_rAbsorbGas      : REAL := 0.001;    (* Gamma mass absorption coefficient - gas *)
    c_rAbsorbOil      : REAL := 0.095;    (* Gamma mass absorption coefficient - oil *)
    c_rAbsorbWater    : REAL := 0.105;    (* Gamma mass absorption coefficient - water *)
    c_rDischargeCoeff : REAL := 0.985;    (* Venturi discharge coefficient (Cd) *)

    (* Intermediate Calculation Variables *)
    rMixDensity       : REAL;     (* Calculated mixture density from gamma (kg/m3) *)
    rPhaseFractionG   : REAL;     (* Gas Volume Fraction (GVF) *)
    rPhaseFractionL   : REAL;     (* Liquid Volume Fraction (LVF) *)
    rSlipVelocity     : REAL;     (* Slip velocity between gas and liquid phases (m/s) *)
    rBulkFlowRate     : REAL;     (* Total bulk volumetric flow rate (m3/h) *)
    rCompFactorZ      : REAL;     (* Real gas compressibility factor (Z) at P, T *)
END_VAR

(* === MAIN LOGIC === *)
(* Ensure fail-safe conditions are met first *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bAlarm := TRUE;
    rOilFlowRate := 0.0;
    rWaterFlowRate := 0.0;
    rGasFlowRate := 0.0;
    iState := 99; (* Transition to fault state *)
    RETURN;
END_IF;

(* Subsea MPFM State Machine *)
CASE iState OF
    0: (* IDLE & INITIALIZATION *)
        bSystemReady := FALSE;
        bAlarm := FALSE;
        IF bEnable THEN
            tTimer(IN := FALSE);
            iState := 10;
        END_IF;

    10: (* SENSOR DIAGNOSTICS & WARMUP *)
        (* Wait for subsea instrumentation signals to stabilize *)
        tTimer(IN := TRUE, PT := T#5S);
        IF tTimer.Q THEN
            (* Check for basic signal integrity *)
            IF rGammaCounts < 100.0 OR rLinePress < 1.0 THEN
                bAlarm := TRUE;
                iState := 99;
            ELSE
                tTimer(IN := FALSE);
                iState := 20;
            END_IF;
        END_IF;

    20: (* DENSITY & FRACTION ACQUISITION (Cross-Correlation & Gamma) *)
        (* Calculate mixture density via Beer-Lambert Law approximation *)
        IF rGammaCounts > 0.0 THEN
            rMixDensity := (LN(c_rGammaEmpty) - LN(rGammaCounts)) * 100.0;
        ELSE
            rMixDensity := 1000.0;
        END_IF;

        (* Crude Gas Volume Fraction (GVF) estimation based on mixed density limits *)
        (* Assuming standard seawater/oil mix vs gas *)
        IF rMixDensity < 150.0 THEN
            rPhaseFractionG := 0.95;
        ELSIF rMixDensity > 950.0 THEN
            rPhaseFractionG := 0.05;
        ELSE
            rPhaseFractionG := (1000.0 - rMixDensity) / 1000.0;
        END_IF;

        rPhaseFractionL := 1.0 - rPhaseFractionG;

        (* Capacitive sensor derives WLR (Water Liquid Ratio) *)
        (* simplified complex dielectric mapping: 2.0pF -> 0% water, 80pF -> 100% water *)
        rWaterLiquidRatio := ((rCapacitance - 2.0) / 78.0) * 100.0;
        IF rWaterLiquidRatio < 0.0 THEN rWaterLiquidRatio := 0.0; END_IF;
        IF rWaterLiquidRatio > 100.0 THEN rWaterLiquidRatio := 100.0; END_IF;

        iState := 30;

    30: (* PVT COMPENSATION & SLIP MODELING *)
        (* High pressure/temperature compensation for real gas density *)
        (* Compressibility Z-factor approximation (simplified for IEC block) *)
        rCompFactorZ := 1.0 - (rLinePress * 0.002) + (rLineTemp * 0.0005);
        IF rCompFactorZ < 0.3 THEN rCompFactorZ := 0.3; END_IF;

        (* Chisholm slip correlation abstraction *)
        rSlipVelocity := 1.1 + (0.2 * rPhaseFractionG);
        iState := 40;

    40: (* VENTURI FLOW CALCULATION & OUTPUT ROUTING *)
        (* Bulk flow from Bernoulli's principle adapted for multiphase *)
        IF rVenturiDp > 0.0 AND rMixDensity > 0.0 THEN
            (* Q = Cd * A * sqrt(2 * dp / rho) - Constants aggregated into 3600 factor *)
            rBulkFlowRate := c_rDischargeCoeff * 3600.0 * SQRT((2.0 * rVenturiDp * 100.0) / rMixDensity);
        ELSE
            rBulkFlowRate := 0.0;
        END_IF;

        (* Phase flow rates at line conditions, scaled to standard conditions via PVT (Z) *)
        rGasFlowRate := rBulkFlowRate * rPhaseFractionG * rSlipVelocity * (rLinePress / (1.01325 * rCompFactorZ));

        (* Liquid phases splitting *)
        rOilFlowRate := rBulkFlowRate * rPhaseFractionL * (1.0 - (rWaterLiquidRatio / 100.0));
        rWaterFlowRate := rBulkFlowRate * rPhaseFractionL * (rWaterLiquidRatio / 100.0);

        bSystemReady := TRUE;

        (* Continuous sampling loop *)
        IF NOT bEnable THEN
            iState := 0;
        ELSE
            iState := 20; (* Loop back to acquisition *)
        END_IF;

    99: (* FAULT HANDLING *)
        bSystemReady := FALSE;
        rOilFlowRate := 0.0;
        rWaterFlowRate := 0.0;
        rGasFlowRate := 0.0;
        IF bEmergencyStop AND NOT bEnable THEN
            iState := 0; (* Reset requested via enable cycle *)
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": code}
    ]
}
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
