import json

st_code = """(*
================================================================================
Enterprise-Grade Substation STATCOM (Static Synchronous Compensator) Control System
IEC 61131-3 Structured Text Implementation
================================================================================
FEATURES:
  1. Ultra-fast (<5ms) voltage sag detection and IGBT firing angle matrix generation
     for reactive power (VAR) injection.
  2. Transformer Dissolved Gas Analysis (DGA) based thermal and safety interlocks.
  3. Sub-Synchronous Resonance (SSR) damping control loops.
  
VERSION: 2.1.4
AUTHOR: Lumina Elite Synthetic Data Architect
================================================================================
*)

FUNCTION_BLOCK FB_STATCOM_CONTROL
VAR_INPUT
    // Grid Measurements (Sampled at 10kHz for 5ms response)
    V_Grid_A : REAL; // Phase A Voltage (pu)
    V_Grid_B : REAL; // Phase B Voltage (pu)
    V_Grid_C : REAL; // Phase C Voltage (pu)
    I_Grid_A : REAL; // Phase A Current (pu)
    I_Grid_B : REAL; // Phase B Current (pu)
    I_Grid_C : REAL; // Phase C Current (pu)
    Grid_Freq : REAL; // Grid Frequency (Hz)

    // Transformer DGA & Thermal Inputs
    H2_ppm : REAL;    // Hydrogen concentration (ppm)
    CO_ppm : REAL;    // Carbon Monoxide (ppm)
    CH4_ppm : REAL;   // Methane (ppm)
    C2H4_ppm : REAL;  // Ethylene (ppm)
    C2H2_ppm : REAL;  // Acetylene (ppm)
    Oil_Temp : REAL;  // Top oil temperature (deg C)

    // Control Settings
    V_Ref : REAL := 1.0;          // Reference voltage (pu)
    Deadband_V : REAL := 0.02;    // Voltage deadband (pu)
    Max_Reactive_Power : REAL := 100.0; // MVAr limit
END_VAR

VAR_OUTPUT
    // IGBT Firing Matrices (Alpha angles per phase)
    IGBT_Alpha_A : ARRAY[1..6] OF REAL;
    IGBT_Alpha_B : ARRAY[1..6] OF REAL;
    IGBT_Alpha_C : ARRAY[1..6] OF REAL;

    // Status & Alarms
    Q_Injected : REAL;       // Current reactive power injected (MVAr)
    DGA_Trip : BOOL;         // Transformer DGA Trip Interlock
    SSR_Active : BOOL;       // Sub-synchronous resonance detected and damping active
    System_Healthy : BOOL;   // Overall system status
END_VAR

VAR
    // Internal States
    V_RMS_Filtered : REAL;
    Voltage_Error : REAL;
    Q_Demand : REAL;
    PI_Integral : REAL := 0.0;
    Kp_V : REAL := 50.0;
    Ki_V : REAL := 1500.0;
    
    // SSR Damping States
    SSR_Bandpass_Out : REAL;
    SSR_Phase_Comp : REAL;
    SSR_Freq_Detected : REAL;
    SSR_Threshold : REAL := 0.01; // pu current oscillation

    // DGA Interlock States
    TDCG : REAL; // Total Dissolved Combustible Gas
    DGA_Warning : BOOL;
    
    // Timing & execution
    Cycle_Time : REAL := 0.0001; // 100us task cycle
    i : INT;
    
    // Matrix Math
    Base_Alpha : REAL;
    Phase_Shift_A : REAL := 0.0;
    Phase_Shift_B : REAL := 2.0944; // 120 degrees in rad
    Phase_Shift_C : REAL := 4.1888; // 240 degrees in rad
END_VAR

(* -----------------------------------------------------------------------------
   1. Transformer Dissolved Gas Analysis (DGA) Thermal Interlocks
----------------------------------------------------------------------------- *)
// Calculate Total Dissolved Combustible Gas (TDCG)
TDCG := H2_ppm + CO_ppm + CH4_ppm + C2H4_ppm + C2H2_ppm;

// Evaluate Duval Triangle / Basic Thresholds for critical faults (Arcing/Thermal)
IF C2H2_ppm > 10.0 OR TDCG > 720.0 OR Oil_Temp > 115.0 THEN
    DGA_Trip := TRUE;
    System_Healthy := FALSE;
    DGA_Warning := TRUE;
ELSIF TDCG > 300.0 OR Oil_Temp > 95.0 THEN
    DGA_Warning := TRUE;
    DGA_Trip := FALSE;
ELSE
    DGA_Warning := FALSE;
    DGA_Trip := FALSE;
END_IF;

IF DGA_Trip THEN
    // Force zero reactive power and block pulses
    Q_Demand := 0.0;
    FOR i := 1 TO 6 DO
        IGBT_Alpha_A[i] := 0.0;
        IGBT_Alpha_B[i] := 0.0;
        IGBT_Alpha_C[i] := 0.0;
    END_FOR;
    RETURN; // Halt execution of firing logic
END_IF;

(* -----------------------------------------------------------------------------
   2. Sub-Synchronous Resonance (SSR) Damping
----------------------------------------------------------------------------- *)
// Extract sub-synchronous components from active power or frequency measurements
// Simple bandpass filter targeting typical SSR frequencies (10 Hz - 40 Hz)
// This is a simplified representation of an SSR torsional interaction filter.
SSR_Bandpass_Out := (I_Grid_A + I_Grid_B + I_Grid_C) * 0.333; // Conceptual zero-sequence / torsional coupling proxy

IF ABS(SSR_Bandpass_Out) > SSR_Threshold THEN
    SSR_Active := TRUE;
    // Apply phase compensation to provide positive damping torque
    SSR_Phase_Comp := SSR_Bandpass_Out * 0.85; // Gain K_ssr
ELSE
    SSR_Active := FALSE;
    SSR_Phase_Comp := 0.0;
END_IF;


(* -----------------------------------------------------------------------------
   3. Voltage Sag Detection and Fast Reactive Power (VAR) Demand Calculation (<5ms)
----------------------------------------------------------------------------- *)
// Instantaneous voltage magnitude calculation (dq transform magnitude proxy)
V_RMS_Filtered := SQRT(V_Grid_A*V_Grid_A + V_Grid_B*V_Grid_B + V_Grid_C*V_Grid_C) * 0.81649; // sqrt(2/3)

Voltage_Error := V_Ref - V_RMS_Filtered;

// Deadband to prevent hunting
IF ABS(Voltage_Error) < Deadband_V THEN
    Voltage_Error := 0.0;
END_IF;

// Fast PI Controller for VAR injection
PI_Integral := PI_Integral + (Voltage_Error * Ki_V * Cycle_Time);

// Anti-windup
IF PI_Integral > Max_Reactive_Power THEN
    PI_Integral := Max_Reactive_Power;
ELSIF PI_Integral < -Max_Reactive_Power THEN
    PI_Integral := -Max_Reactive_Power;
END_IF;

Q_Demand := (Voltage_Error * Kp_V) + PI_Integral;

// Superimpose SSR Damping Modulations on Q demand or Active power limits
Q_Demand := Q_Demand + (SSR_Phase_Comp * 10.0);

// Limit Total Demand
IF Q_Demand > Max_Reactive_Power THEN Q_Demand := Max_Reactive_Power; END_IF;
IF Q_Demand < -Max_Reactive_Power THEN Q_Demand := -Max_Reactive_Power; END_IF;
Q_Injected := Q_Demand;

(* -----------------------------------------------------------------------------
   4. IGBT Firing Angle Matrix Generation
----------------------------------------------------------------------------- *)
// Convert Q_Demand into firing angles (alpha) for the Multi-Level Inverter
// Assume a cascaded H-bridge or modular multilevel converter (MMC) mapping.

// Base alpha relates directly to required VARs (simplified mapping)
// We clamp Q_Demand to avoid ASIN domain errors [-1, 1]
IF Q_Demand > Max_Reactive_Power THEN Q_Demand := Max_Reactive_Power; END_IF;
IF Q_Demand < -Max_Reactive_Power THEN Q_Demand := -Max_Reactive_Power; END_IF;

Base_Alpha := ASIN(Q_Demand / Max_Reactive_Power); 

FOR i := 1 TO 6 DO
    // Distribute angles across 6 levels per phase for harmonic mitigation (e.g., SHE-PWM)
    // Adding minor angular offsets for each IGBT level to shape the waveform
    IGBT_Alpha_A[i] := Base_Alpha + Phase_Shift_A + (INT_TO_REAL(i)*0.0174); 
    IGBT_Alpha_B[i] := Base_Alpha + Phase_Shift_B + (INT_TO_REAL(i)*0.0174);
    IGBT_Alpha_C[i] := Base_Alpha + Phase_Shift_C + (INT_TO_REAL(i)*0.0174);
END_FOR;

System_Healthy := TRUE;

END_FUNCTION_BLOCK
"""

prompt = "Write the PLC logic implementation for an enterprise-grade Substation STATCOM (Static Synchronous Compensator). Technical requirements: 1. IGBT firing angle matrices to inject reactive power (VARs) into the grid within 5 milliseconds of a voltage sag. 2. Transformer dissolved gas analysis (DGA) thermal interlocks. 3. Sub-synchronous resonance (SSR) damping."

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": st_code}
    ]
}

file_path = r"c:\Users\majip\Downloads\LLM REASEARCH\data\synthetic_generation_v3_enterprise.jsonl"
with open(file_path, "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\n")
print("Successfully appended to jsonl")
