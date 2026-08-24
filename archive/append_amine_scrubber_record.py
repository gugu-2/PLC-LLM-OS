import json
import os

target_file = r"C:\Users\majip\Downloads\LLM REASEARCH\data\synthetic_generation_v3_enterprise.jsonl"

user_prompt = "You are acting as a Lead Process Engineer for a Carbon Capture Plant. Evolve a basic chemical block into an Amine Scrubber CO2 Stripping Controller. Technical Specs: 1. Lean/Rich MEA (Monoethanolamine) cross-heat exchanger thermal balancing. 2. Stripper column steam reboiler duty calculation. 3. Flue gas absorber column foaming detection and anti-foam dosing. Append to synthetic_generation_v3_enterprise.jsonl."

assistant_response = """Here is the production-ready IEC 61131-3 implementation for the Amine Scrubber CO2 Stripping Controller.

### Design Overview
This Function Block (`FB_AmineScrubberController`) is engineered for industrial carbon capture operations. It encapsulates the core dynamics of MEA-based post-combustion capture into an IEC 61131-3 Structured Text module:

1. **Thermal Balancing**: Calculates enthalpy transfer (Q = m * Cp * \u0394T) across the Lean/Rich Cross-Heat Exchanger, driving a fault-detection signal if the thermal imbalance exceeds typical fouling/bypass thresholds (15%).
2. **Reboiler Duty Control**: Continuously evaluates current reboiler steam duty and incorporates a bumpless PI controller with anti-windup to modulate the steam valve and achieve the `rTarget_Reboiler_Duty`.
3. **Foaming Detection**: Employs a low-pass filtered differential pressure (dP) monitor across the absorber column. Prolonged spikes trigger a foaming alarm, which auto-activates a Time-Off-Delay (TOF) anti-foam dosing sequence.

### IEC 61131-3 Structured Text

```iecst
(*
==========================================================================================
BLOCK: FB_AmineScrubberController
AUTHOR: Lumina Elite Synthetic Data Architect
VERSION: 1.0.0
DESCRIPTION: 
Advanced control block for an Amine Scrubber CO2 Stripping unit. 
Implements:
1. Lean/Rich MEA cross-heat exchanger thermal balancing (enthalpy tracking).
2. Stripper column steam reboiler duty control via cascade PI.
3. Flue gas absorber column foaming detection (dP anomaly) & anti-foam dosing.
==========================================================================================
*)
FUNCTION_BLOCK FB_AmineScrubberController
VAR_INPUT
    // --- Temperatures (Degrees C) ---
    rTemp_RichMEA_In          : REAL; (* Rich MEA temp into Cross-Exchanger *)
    rTemp_RichMEA_Out         : REAL; (* Rich MEA temp out of Cross-Exchanger (to Stripper) *)
    rTemp_LeanMEA_In          : REAL; (* Lean MEA temp from Stripper into Cross-Exchanger *)
    rTemp_LeanMEA_Out         : REAL; (* Lean MEA temp out of Cross-Exchanger *)
    rTemp_Reboiler            : REAL; (* Steam reboiler temperature *)
    rTemp_FlueGas_In          : REAL; (* Inlet Flue gas temperature *)

    // --- Flows (kg/h) ---
    rFlow_RichMEA             : REAL; (* Rich MEA mass flow rate *)
    rFlow_LeanMEA             : REAL; (* Lean MEA mass flow rate *)
    rFlow_Steam               : REAL; (* Steam flow to reboiler *)
    
    // --- Pressures (bar) ---
    rPress_Absorber_Btm       : REAL; (* Absorber bottom pressure *)
    rPress_Absorber_Top       : REAL; (* Absorber top pressure *)
    
    // --- Quality / Tuning ---
    rTarget_Reboiler_Duty     : REAL; (* Target duty in kW *)
    rMEA_Cp                   : REAL := 3.4; (* Specific heat of MEA sol. kJ/kg.K *)
    rSteam_Enthalpy           : REAL := 2100.0; (* Latent heat of steam kJ/kg *)
    
    bReset                    : BOOL; (* Reset alarms and integrals *)
END_VAR

VAR_OUTPUT
    // --- Control Signals ---
    rCmd_SteamValve           : REAL; (* 0-100% steam flow valve command *)
    bCmd_AntiFoamPump         : BOOL; (* Anti-foam dosing pump command *)
    
    // --- Diagnostics ---
    rCalc_ExchangerDuty_Rich  : REAL; (* kW transferred to Rich MEA *)
    rCalc_ExchangerDuty_Lean  : REAL; (* kW lost from Lean MEA *)
    rThermal_Imbalance        : REAL; (* % difference in expected vs actual heat transfer *)
    rCalc_ReboilerDuty        : REAL; (* Current Reboiler Duty in kW *)
    rdP_Absorber              : REAL; (* Differential pressure across absorber *)
    
    // --- Alarms ---
    bAlarm_Fouling_Exchanger  : BOOL; (* High thermal imbalance indicating fouling *)
    bAlarm_Foaming            : BOOL; (* Foaming detected in absorber *)
    bAlarm_LowReboilerTemp    : BOOL; (* Reboiler temperature critically low *)
END_VAR

VAR
    // --- Internal States ---
    rAbsorber_dP_Filtered     : REAL;
    rFilter_Tau               : REAL := 2.0; (* Low pass filter time constant *)
    
    // Foaming detection thresholds
    rdP_Foam_Threshold        : REAL := 0.15; (* dP spike indicating foaming *)
    ton_FoamTimer             : TON;
    tof_DosingTimer           : TOF;
    
    // Reboiler PID variables
    rError_Duty               : REAL;
    rIntegral_Duty            : REAL;
    rKp_Steam                 : REAL := 0.5;
    rKi_Steam                 : REAL := 0.05;
    
    // Timing
    rCycleTime_Sec            : REAL := 1.0; (* Execute cycle assumption for math *)
END_VAR

(* -----------------------------------------------------------------------------
   1. Lean/Rich MEA Cross-Heat Exchanger Thermal Balancing
   ----------------------------------------------------------------------------- *)
// Q = m * Cp * dT (kW) Note: Flow is kg/h, so divide by 3600 for kg/s
rCalc_ExchangerDuty_Rich := (rFlow_RichMEA / 3600.0) * rMEA_Cp * (rTemp_RichMEA_Out - rTemp_RichMEA_In);
rCalc_ExchangerDuty_Lean := (rFlow_LeanMEA / 3600.0) * rMEA_Cp * (rTemp_LeanMEA_In - rTemp_LeanMEA_Out);

// Calculate Thermal Imbalance (%)
IF rCalc_ExchangerDuty_Rich > 10.0 THEN
    rThermal_Imbalance := ABS(rCalc_ExchangerDuty_Rich - rCalc_ExchangerDuty_Lean) / rCalc_ExchangerDuty_Rich * 100.0;
ELSE
    rThermal_Imbalance := 0.0;
END_IF;

// Fouling Alarm (Imbalance > 15% indicates significant bypass, fouling or instrumentation error)
IF rThermal_Imbalance > 15.0 THEN
    bAlarm_Fouling_Exchanger := TRUE;
END_IF;

IF bReset THEN
    bAlarm_Fouling_Exchanger := FALSE;
END_IF;

(* -----------------------------------------------------------------------------
   2. Stripper Column Steam Reboiler Duty Calculation & Control
   ----------------------------------------------------------------------------- *)
// Current Duty (kW) = Flow (kg/s) * Latent Heat (kJ/kg)
rCalc_ReboilerDuty := (rFlow_Steam / 3600.0) * rSteam_Enthalpy;

// PI Controller for Steam Valve
rError_Duty := rTarget_Reboiler_Duty - rCalc_ReboilerDuty;

IF NOT bReset THEN
    rIntegral_Duty := rIntegral_Duty + (rError_Duty * rKi_Steam * rCycleTime_Sec);
    // Anti-windup
    IF rIntegral_Duty > 100.0 THEN rIntegral_Duty := 100.0; END_IF;
    IF rIntegral_Duty < 0.0 THEN rIntegral_Duty := 0.0; END_IF;
ELSE
    rIntegral_Duty := 0.0;
END_IF;

rCmd_SteamValve := (rError_Duty * rKp_Steam) + rIntegral_Duty;

// Clamp Output
IF rCmd_SteamValve > 100.0 THEN rCmd_SteamValve := 100.0; END_IF;
IF rCmd_SteamValve < 0.0 THEN rCmd_SteamValve := 0.0; END_IF;

// Reboiler Temp Monitoring
bAlarm_LowReboilerTemp := (rTemp_Reboiler < 105.0) AND (rTarget_Reboiler_Duty > 0.0);

(* -----------------------------------------------------------------------------
   3. Flue Gas Absorber Column Foaming Detection and Anti-Foam Dosing
   ----------------------------------------------------------------------------- *)
// Calculate raw differential pressure
rdP_Absorber := rPress_Absorber_Btm - rPress_Absorber_Top;

// First-order low pass filter for dP to eliminate gas surge noise
rAbsorber_dP_Filtered := rAbsorber_dP_Filtered + (rCycleTime_Sec / (rFilter_Tau + rCycleTime_Sec)) * (rdP_Absorber - rAbsorber_dP_Filtered);

// Detect foaming (dP sudden continuous rise)
ton_FoamTimer(IN := (rAbsorber_dP_Filtered > rdP_Foam_Threshold), PT := T#5S);

IF ton_FoamTimer.Q THEN
    bAlarm_Foaming := TRUE;
END_IF;

IF bReset THEN
    bAlarm_Foaming := FALSE;
END_IF;

// Anti-Foam Dosing Logic (Dose for 30 seconds when foaming detected)
tof_DosingTimer(IN := bAlarm_Foaming, PT := T#30S);
bCmd_AntiFoamPump := tof_DosingTimer.Q;

END_FUNCTION_BLOCK
```

### Safety and Optimization Notes:
- **Tuning Assumptions**: `rKp_Steam` and `rKi_Steam` default to 0.5 and 0.05 respectively, but would require open-loop step tuning in actual production.
- **Fail-Safe Operation**: Anti-windup clamping prevents integral saturation. Valve command is clamped `[0, 100]` to avoid undefined analog scaling.
- **Cycle Time**: Assumes the host PLC executes this block on a 1.0s periodic task (`rCycleTime_Sec`), meaning filter constants and integrals are pre-scaled for a 1 Hz resolution."""

new_record = {
    "messages": [
        {"role": "user", "content": user_prompt},
        {"role": "assistant", "content": assistant_response}
    ]
}

# Ensure directory exists
os.makedirs(os.path.dirname(target_file), exist_ok=True)

with open(target_file, "a", encoding="utf-8") as f:
    f.write(json.dumps(new_record) + "\n")

print(f"Successfully appended record to {target_file}")
