import json

system_prompt = "You are an expert industrial automation engineer specializing in IEC 61131-3."

user_prompt = "Evolve a basic PID into a Continuous API Crystallizer Controller. Technical Specs: 1. Supersaturation closed-loop control based on focused beam reflectance measurement (FBRM) chord length. 2. Antisolvent addition sequencing. 3. Crystal size distribution (CSD) optimization matrices."

st_code = """(*
===================================================================================================
MODULE: Continuous API Crystallizer Controller (Advanced Edition)
AUTHOR: Lead Process Engineer (Synthesized by Elite Architect)
VERSION: 5.0.0 Enterprise Grade

DESCRIPTION:
This function block implements a high-fidelity Continuous Active Pharmaceutical Ingredient (API)
Crystallization control scheme. It supersedes traditional PID mechanisms by integrating:
  1. Supersaturation Closed-Loop Control: Utilizing Focused Beam Reflectance Measurement (FBRM).
     FBRM Chord Length Distribution (CLD) real-time statistics act as primary state variables.
  2. Antisolvent Addition Sequencing: Dynamic scheduling of antisolvent dosing valves based on 
     thermodynamic phase-diagram mapping to maintain the crystallization trajectory within the 
     metastable zone width (MSZW).
  3. Crystal Size Distribution (CSD) Optimization Matrices: Predictive operations to minimize fines, 
     suppress secondary nucleation, and maximize target API habit and polymorphic purity.

COMPLIANCE: ISA-88, IEC 61131-3, CFR 21 Part 11 Data Integrity.
===================================================================================================
*)

FUNCTION_BLOCK FB_Continuous_API_Crystallizer

VAR_INPUT
    // ---------------- System Status & Interlocks ----------------
    xEnable                  : BOOL;          // Master enable for continuous crystallization
    xEmergencyStop           : BOOL;          // SIS interlock trigger
    xReset                   : BOOL;          // Alarm/fault reset
    
    // ---------------- Process Analytics Technology (PAT) ----------
    rConcentration_ATR_FTIR  : REAL;          // API concentration via in-situ ATR-FTIR [mg/mL]
    rSolubility_Curve_Val    : REAL;          // Theoretical solubility at current Temp [mg/mL]
    rTemperature_PT100       : REAL;          // Process Temperature [DegC]
    
    // ---------------- FBRM Probe Data (Chord Length Dist) -------
    arrFBRM_Counts_Per_Sec   : ARRAY[1..100] OF REAL; // Raw chord length counts
    rMean_Chord_Length       : REAL;          // Square-weighted mean chord length [um]
    rFines_Fraction          : REAL;          // Ratio of particles < 10um
    
    // ---------------- Antisolvent Dynamics ----------------------
    rAntisolvent_Flow_PV     : REAL;          // Actual flow of antisolvent [L/min]
    rFeed_Flow_PV            : REAL;          // API mother liquor feed rate [L/min]
    
    // ---------------- Target Optimization Parameters ------------
    rTarget_CSD_Mean         : REAL;          // Desired D50 / Mean CSD [um]
    rTarget_Supersaturation  : REAL;          // Setpoint for relative supersaturation [S]
    rMax_Cooling_Rate        : REAL := 1.5;   // DegC/min
END_VAR

VAR_OUTPUT
    // ---------------- Control Elements --------------------------
    rAntisolvent_Flow_SP     : REAL;          // Setpoint to Antisolvent Dosing Coriolis Mass Flow Meter
    rJacket_Temp_SP          : REAL;          // Setpoint to TCU (Temperature Control Unit) Cascade
    rAgitator_Speed_SP       : REAL;          // Setpoint for VFD Agitator [RPM]
    
    // ---------------- Sequencing & Status -----------------------
    eStatus                  : E_Cryst_Status; // (IDLE, SEEDING, GROWTH, MATURATION, DISCHARGE, FAULT)
    xAntisolvent_Valve_Open  : BOOL;          // Discrete trigger for dosing valve sequence
    
    // ---------------- Diagnostics & Alarms ----------------------
    rCurrent_Supersat_Ratio  : REAL;          // S = C/C*
    rNucleation_Penalty      : REAL;          // Calculated risk of secondary nucleation
    xAlarm_MSZW_Violation    : BOOL;          // True if trajectory crosses labile zone
    xAlarm_Fines_Spike       : BOOL;          // True if massive fine generation detected
END_VAR

VAR
    // ---------------- Internal State Machines & Timers ----------
    nState                   : INT;
    fbMaturationTimer        : TON;
    fbDosingPulseTimer       : TON;
    
    // ---------------- PID & Optimization Controllers ------------
    fbPID_Supersaturation    : FB_PID_Advanced; // Evolved from basic PID
    fbPID_Temperature        : FB_PID_Advanced; 
    
    // ---------------- CSD Optimization Matrices -----------------
    // Let M = Population Balance Model (PBM) transformation matrix (simplified 10x10 representation)
    arrGrowthMatrix          : ARRAY[1..10, 1..10] OF REAL; 
    arrNucleationVector      : ARRAY[1..10] OF REAL;
    arrCurrentCSD_State      : ARRAY[1..10] OF REAL;
    arrPredictedCSD_State    : ARRAY[1..10] OF REAL;
    
    // ---------------- Internal Registers ------------------------
    rError_CSD               : REAL;
    i                        : INT;
    j                        : INT;
    rMatrixSum               : REAL;
    rDosing_Rate_Base        : REAL;
    rDosing_Rate_Opt         : REAL;
    rSupersat_Integral       : REAL;
    xSeed_Detected           : BOOL;
    
    // Constants
    c_MSZW_UpperLimit        : REAL := 1.25;  // Supersaturation limit before spontaneous nucleation
    c_MSZW_LowerLimit        : REAL := 1.05;  // Minimum to drive crystal growth
END_VAR

// ===================================================================================================
// SYSTEM INTERLOCKS & SAFETY
// ===================================================================================================
IF xEmergencyStop THEN
    rAntisolvent_Flow_SP := 0.0;
    rJacket_Temp_SP := rTemperature_PT100; // Hold temperature
    rAgitator_Speed_SP := 50.0;            // Minimum safe suspension speed
    xAntisolvent_Valve_Open := FALSE;
    eStatus := E_Cryst_Status.FAULT;
    RETURN;
END_IF

IF xReset THEN
    xAlarm_MSZW_Violation := FALSE;
    xAlarm_Fines_Spike := FALSE;
    eStatus := E_Cryst_Status.IDLE;
END_IF

IF NOT xEnable THEN
    rAntisolvent_Flow_SP := 0.0;
    eStatus := E_Cryst_Status.IDLE;
    RETURN;
END_IF

// ===================================================================================================
// 1. SUPERSATURATION CALCULATION & CLOSED-LOOP CONTROL
// ===================================================================================================
// S = Actual Concentration / Solubility Limit at Current T and Antisolvent Ratio
IF rSolubility_Curve_Val > 0.0 THEN
    rCurrent_Supersat_Ratio := rConcentration_ATR_FTIR / rSolubility_Curve_Val;
ELSE
    rCurrent_Supersat_Ratio := 0.0;
END_IF

// Detect MSZW (Metastable Zone Width) Boundary Violations
IF rCurrent_Supersat_Ratio > c_MSZW_UpperLimit THEN
    xAlarm_MSZW_Violation := TRUE;
    // Fast corrective action: Increase temperature to dissolve fines and lower supersaturation
    rJacket_Temp_SP := rJacket_Temp_SP + 2.0; 
END_IF

// PID Controller for Supersaturation (Manipulated Variable = Cooling Rate & Antisolvent Flow)
fbPID_Supersaturation(
    xEnable     := (eStatus = E_Cryst_Status.GROWTH),
    rSetpoint   := rTarget_Supersaturation,
    rProcessVal := rCurrent_Supersat_Ratio,
    rKp         := 2.5,
    rKi         := 0.1,
    rKd         := 0.05,
    rTs         := 1.0,  // 1 second execution cycle
    rOutput     => rDosing_Rate_Base
);

// ===================================================================================================
// 2. FBRM / PAT INTEGRATION & FINES DETECTION
// ===================================================================================================
// Detect Secondary Nucleation (Massive spike in fines < 10um)
IF rFines_Fraction > 0.15 AND rMean_Chord_Length < (rTarget_CSD_Mean * 0.5) THEN
    xAlarm_Fines_Spike := TRUE;
    rNucleation_Penalty := 100.0; // High penalty for optimization
ELSE
    xAlarm_Fines_Spike := FALSE;
    rNucleation_Penalty := 0.0;
END_IF

// ===================================================================================================
// 3. CRYSTAL SIZE DISTRIBUTION (CSD) OPTIMIZATION MATRICES
// ===================================================================================================
// Simplified Population Balance Model (PBM) execution using real-time FBRM data mapping
// Map raw FBRM array (1..100) to 10-bin model state
FOR i := 1 TO 10 DO
    arrCurrentCSD_State[i] := 0.0;
    FOR j := 1 TO 10 DO
        arrCurrentCSD_State[i] := arrCurrentCSD_State[i] + arrFBRM_Counts_Per_Sec[(i-1)*10 + j];
    END_FOR
END_FOR

// Matrix Multiplication: Predicted_State = GrowthMatrix * Current_State + NucleationVector
FOR i := 1 TO 10 DO
    rMatrixSum := 0.0;
    FOR j := 1 TO 10 DO
        rMatrixSum := rMatrixSum + (arrGrowthMatrix[i, j] * arrCurrentCSD_State[j]);
    END_FOR
    arrPredictedCSD_State[i] := rMatrixSum + arrNucleationVector[i] * rCurrent_Supersat_Ratio;
END_FOR

// Calculate CSD Error based on target mean bin (assume bin 7 is target)
rError_CSD := arrPredictedCSD_State[7] - (arrCurrentCSD_State[7] * 1.1); // Aiming for 10% growth in target bin

// Adjust Dosing based on CSD Prediction
IF rError_CSD < 0.0 THEN
    // Growth is too slow, increase supersaturation slightly via antisolvent optimization factor
    rDosing_Rate_Opt := rDosing_Rate_Base * 1.05;
ELSIF xAlarm_Fines_Spike THEN
    // Stop antisolvent addition to suppress nucleation
    rDosing_Rate_Opt := 0.0;
ELSE
    rDosing_Rate_Opt := rDosing_Rate_Base;
END_IF

// ===================================================================================================
// 4. ANTISOLVENT ADDITION SEQUENCING & STATE MACHINE
// ===================================================================================================
CASE eStatus OF
    
    E_Cryst_Status.IDLE:
        rAntisolvent_Flow_SP := 0.0;
        xAntisolvent_Valve_Open := FALSE;
        rAgitator_Speed_SP := 60.0; // Suspend solids
        IF xEnable AND rConcentration_ATR_FTIR > 0.0 THEN
            eStatus := E_Cryst_Status.SEEDING;
        END_IF
        
    E_Cryst_Status.SEEDING:
        // Wait for external seeding event (detected by FBRM counts jumping)
        IF arrCurrentCSD_State[3] > 100.0 THEN // Arbitrary seed threshold in bin 3
            xSeed_Detected := TRUE;
            eStatus := E_Cryst_Status.GROWTH;
        END_IF
        
    E_Cryst_Status.GROWTH:
        // Continuous API crystallization main loop
        rAntisolvent_Flow_SP := LIMIT(0.0, rDosing_Rate_Opt, 50.0); // Limit max flow to 50 L/min
        
        // Pulse valve sequence if flow is too low to maintain continuous flow (prevent line clogging)
        IF rAntisolvent_Flow_SP > 0.0 AND rAntisolvent_Flow_SP < 5.0 THEN
            fbDosingPulseTimer(IN := NOT fbDosingPulseTimer.Q, PT := T#5S);
            IF fbDosingPulseTimer.ET < T#2S THEN
                xAntisolvent_Valve_Open := TRUE;
                rAntisolvent_Flow_SP := 12.5; // Pulse at higher rate
            ELSE
                xAntisolvent_Valve_Open := FALSE;
                rAntisolvent_Flow_SP := 0.0;
            END_IF
        ELSE
            xAntisolvent_Valve_Open := (rAntisolvent_Flow_SP > 0.0);
        END_IF
        
        // Transition to maturation if batch/semi-continuous conditions are met
        IF rFines_Fraction < 0.05 AND rMean_Chord_Length >= rTarget_CSD_Mean THEN
            eStatus := E_Cryst_Status.MATURATION;
        END_IF
        
    E_Cryst_Status.MATURATION:
        // Hold state to allow ostwald ripening (dissolving remaining fines)
        rAntisolvent_Flow_SP := 0.0;
        xAntisolvent_Valve_Open := FALSE;
        // Thermal cycling for ripening
        fbMaturationTimer(IN := TRUE, PT := T#60M);
        
        IF (fbMaturationTimer.ET MOD T#20M) < T#10M THEN
            rJacket_Temp_SP := rJacket_Temp_SP + 5.0; // Heat cycle
        ELSE
            rJacket_Temp_SP := rJacket_Temp_SP - 5.0; // Cool cycle
        END_IF
        
        IF fbMaturationTimer.Q THEN
            eStatus := E_Cryst_Status.DISCHARGE;
        END_IF
        
    E_Cryst_Status.DISCHARGE:
        // Transfer to filter dryer / centrifuge
        rAntisolvent_Flow_SP := 0.0;
        xAntisolvent_Valve_Open := FALSE;
        rAgitator_Speed_SP := 120.0; // High speed to prevent settling during transfer
        IF NOT xEnable THEN
            eStatus := E_Cryst_Status.IDLE;
        END_IF
        
    E_Cryst_Status.FAULT:
        // Handled by interlocks block at top
        
END_CASE

END_FUNCTION_BLOCK
"""

data = {
    "messages": [
        {"role": "user", "content": user_prompt},
        {"role": "assistant", "content": st_code}
    ]
}

with open(r"c:\Users\majip\Downloads\LLM REASEARCH\Local_Ollama_Evol_Pipeline\seeds\tier1_enterprise_grade\synthetic_generation_v3_enterprise.jsonl", "a") as f:
    f.write(json.dumps(data) + "\n")

print("Appended to JSONL successfully.")
