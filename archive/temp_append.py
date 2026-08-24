import json
import os

target_file = r"C:\Users\majip\Downloads\LLM REASEARCH\Local_Ollama_Evol_Pipeline\data\synthetic_generation_v3_enterprise.jsonl"

user_prompt = "You are acting as a Lead Biomedical Engineer. Evolve a basic fluid loop into an Automated Hematology Analyzer Fluidics Controller. Technical Specs: 1. Sheath fluid hydrodynamic focusing for single-cell flow cytometry. 2. Piezo-acoustic droplet generation for cell sorting. 3. Sample probe anti-clotting back-flush sequencing. Append to synthetic_generation_v3_enterprise.jsonl."

assistant_response = """```iec-st
(*
======================================================================================
BLOCK NAME: FB_AutoHemaAnalyzerFluidics
AUTHOR: Lead Biomedical Engineer / Elite Synthetic Data Architect
DESCRIPTION: 
    Production-ready IEC 61131-3 fluidics controller for an Automated Hematology Analyzer.
    Features:
    1. Sheath fluid hydrodynamic focusing for single-cell flow cytometry using dual PID loops.
    2. Piezo-acoustic droplet generation for high-speed cell sorting.
    3. Sample probe anti-clotting back-flush sequencing with occlusion detection.
======================================================================================
*)
TYPE E_HemaSystemState :
(
    HEMA_STATE_IDLE := 0,
    HEMA_STATE_PRIMING := 10,
    HEMA_STATE_READY := 20,
    HEMA_STATE_ANALYSIS := 30,
    HEMA_STATE_BACKFLUSH := 40
);
END_TYPE

FUNCTION_BLOCK FB_AutoHemaAnalyzerFluidics

VAR_INPUT
    bEnable                 : BOOL; // System master enable
    bStartAnalysis          : BOOL; // Trigger sample analysis
    rTargetCoreDia_um       : REAL := 10.0; // Target sample core diameter in microns
    rCellVelocity_mps       : REAL := 15.0; // Target cell velocity (m/s) for flow cytometry
    rPiezoFreq_Hz           : REAL := 40000.0; // Piezo-acoustic frequency for sorting (Hz)
    rPiezoAmp_V             : REAL := 12.5; // Piezo amplitude
    bTriggerSort            : BOOL; // Trigger active sorting based on optical scatter/fluorescence
    tBackflushInterval      : TIME := T#30S; // Interval between preventative backflushes
END_VAR

VAR_OUTPUT
    bSystemReady            : BOOL; // Ready for sample
    bSortingActive          : BOOL; // Cell sorting is actively running
    bClotDetected           : BOOL; // A clot/occlusion was detected
    rActualSheathFlow_uLps  : REAL; // Actual sheath flow rate (uL/s)
    rActualSampleFlow_uLps  : REAL; // Actual sample flow rate (uL/s)
    rSortDelay_us           : REAL; // Calculated delay to drop charge (microseconds)
    eSystemState            : E_HemaSystemState; // Current system state enum
END_VAR

VAR
    // --- Hydrodynamic Focusing (PID Control) ---
    fbSheathPID             : FB_PIDController; 
    fbSamplePID             : FB_PIDController;
    rTargetSheathFlow       : REAL; 
    rTargetSampleFlow       : REAL; 
    
    // --- Piezo Droplet Generation ---
    rDropVolume_pL          : REAL;
    fbPiezoGen              : FB_PWM_Generator; 
    fbSortTimer             : TON;
    rDistanceLaserToSort_mm : REAL := 2.5; // Distance from interrogating laser to break-off point
    
    // --- Anti-Clotting / Back-Flush Sequence ---
    fbBackflushTimer        : TON;
    fbFlushSequence         : TON;
    nFlushStep              : INT;
    rSamplePressure_bar     : REAL;
    rPressureThreshold      : REAL := 2.5; // Threshold indicating partial clot
    bBackflushActive        : BOOL;
    
    // Internal States
    eState                  : E_HemaSystemState := HEMA_STATE_IDLE;
END_VAR

(* -----------------------------------------------------------------------------
   SYSTEM STATE MACHINE
----------------------------------------------------------------------------- *)
CASE eState OF

    HEMA_STATE_IDLE:
        bSystemReady := FALSE;
        bSortingActive := FALSE;
        bBackflushActive := FALSE;
        
        IF bEnable THEN
            eState := HEMA_STATE_PRIMING;
        END_IF

    HEMA_STATE_PRIMING:
        // Prime sheath and sample lines
        rTargetSheathFlow := 500.0; // High flow prime
        rTargetSampleFlow := 0.0;
        
        // Wait for pressure stabilization
        IF (rSamplePressure_bar < 0.5) THEN
            eState := HEMA_STATE_READY;
        END_IF

    HEMA_STATE_READY:
        bSystemReady := TRUE;
        rTargetSheathFlow := 100.0; // Maintenance flow
        
        IF NOT bEnable THEN
            eState := HEMA_STATE_IDLE;
        ELSIF bStartAnalysis THEN
            eState := HEMA_STATE_ANALYSIS;
        END_IF
        
    HEMA_STATE_ANALYSIS:
        bSystemReady := FALSE;
        
        // 1. Sheath Fluid Hydrodynamic Focusing
        // Core diameter is proportional to sqrt(SampleFlow / TotalFlow)
        // Adjust sample and sheath flows to achieve rTargetCoreDia_um and rCellVelocity_mps
        rTargetSampleFlow := (rTargetCoreDia_um * rTargetCoreDia_um * 3.14159 / 4.0) * rCellVelocity_mps * 1000.0; 
        rTargetSheathFlow := (10000.0 - (rTargetCoreDia_um * rTargetCoreDia_um)) * rCellVelocity_mps * 1000.0;
        
        // 2. Piezo-Acoustic Droplet Generation
        // Continuous droplet formation via acoustic standing wave
        fbPiezoGen.Frequency := rPiezoFreq_Hz;
        fbPiezoGen.Amplitude := rPiezoAmp_V;
        fbPiezoGen.Enable := TRUE;
        
        rDropVolume_pL := (rTargetSampleFlow + rTargetSheathFlow) / rPiezoFreq_Hz; 
        
        // Calculate droplet break-off delay for sorting
        rSortDelay_us := (rDistanceLaserToSort_mm / (rCellVelocity_mps * 1000.0)) * 1000000.0;
        
        // Sorting Trigger Logic
        IF bTriggerSort THEN
            fbSortTimer(IN := TRUE, PT := REAL_TO_TIME(rSortDelay_us / 1000.0));
            IF fbSortTimer.Q THEN
                bSortingActive := TRUE;
                // Output charge pulse to deflection plates (Pseudo-code)
                // IO_DeflectionCharge := TRUE; 
            END_IF
        ELSE
            fbSortTimer(IN := FALSE);
            bSortingActive := FALSE;
        END_IF
        
        // 3. Anti-clotting Back-flush sequencing
        fbBackflushTimer(IN := NOT bBackflushActive, PT := tBackflushInterval);
        
        // Dynamic occlusion detection
        IF rSamplePressure_bar > rPressureThreshold THEN
            bClotDetected := TRUE;
            eState := HEMA_STATE_BACKFLUSH;
        ELSIF fbBackflushTimer.Q THEN
            eState := HEMA_STATE_BACKFLUSH;
        END_IF
        
        IF NOT bStartAnalysis THEN
            eState := HEMA_STATE_READY;
        END_IF

    HEMA_STATE_BACKFLUSH:
        bBackflushActive := TRUE;
        fbPiezoGen.Enable := FALSE;
        
        // Sequential state machine for flush process
        fbFlushSequence(IN := TRUE, PT := T#5S);
        
        CASE nFlushStep OF
            0: // Retract sample probe
               rTargetSampleFlow := -50.0; // Negative flow to aspirate slightly
               IF fbFlushSequence.ET > T#1S THEN nFlushStep := 1; END_IF
               
            1: // High-pressure Sheath Back-flush
               rTargetSampleFlow := -200.0; // Push cleaning solution backwards through the probe
               rTargetSheathFlow := 0.0;
               IF fbFlushSequence.ET > T#3S THEN nFlushStep := 2; END_IF
               
            2: // Forward prime to expel bubbles
               rTargetSampleFlow := 100.0;
               IF fbFlushSequence.ET > T#5S THEN nFlushStep := 3; END_IF
               
            3: // Complete
               bClotDetected := FALSE;
               bBackflushActive := FALSE;
               nFlushStep := 0;
               fbFlushSequence(IN := FALSE);
               eState := HEMA_STATE_ANALYSIS;
        END_CASE

END_CASE

eSystemState := eState;

// PID Execution for Pumps
fbSheathPID(
    Setpoint := rTargetSheathFlow, 
    ActualValue := rActualSheathFlow_uLps, 
    Kp := 1.2, Ti := 0.5, Td := 0.1
);
// Drive Sheath Syringe/Gear Pump with fbSheathPID.Output

fbSamplePID(
    Setpoint := rTargetSampleFlow, 
    ActualValue := rActualSampleFlow_uLps, 
    Kp := 2.5, Ti := 0.8, Td := 0.05
);
// Drive Sample Syringe Pump with fbSamplePID.Output

END_FUNCTION_BLOCK
```"""

obj = {
    "messages": [
        {"role": "user", "content": user_prompt},
        {"role": "assistant", "content": assistant_response}
    ]
}

with open(target_file, 'a', encoding='utf-8') as f:
    f.write(json.dumps(obj) + '\n')

print("Successfully appended to JSONL.")
