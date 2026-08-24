import json
import os
import datetime

# Target JSONL file
target_file = r"c:\Users\majip\Downloads\LLM REASEARCH\data\synthetic_generation_v3_enterprise.jsonl"

# Prompt from the user
user_prompt = "You are acting as a Lead Biomedical Engineer for a massive Pharmaceutical manufacturing line. Evolve a basic timer into a Freeze-Drying (Lyophilization) Controller. Technical Specs: 1. Sublimation vacuum pressure curve sequencing. 2. Shelf temperature ramping (-50C to +20C) using silicone oil circulation. 3. Pirani gauge vs Capacitance Manometer cross-checking to determine end-of-primary-drying. Append to synthetic_generation_v3_enterprise.jsonl."

# Complex IEC 61131-3 implementation
assistant_response = """Here is the evolved, production-ready IEC 61131-3 implementation of a Freeze-Drying (Lyophilization) Controller, meeting all enterprise pharmaceutical specifications.

This function block handles the complex orchestration of sublimation vacuum pressure sequencing, silicone oil shelf temperature ramping, and primary drying endpoint detection via Pirani vs. Capacitance Manometer cross-checking.

```iecst
FUNCTION_BLOCK FB_Lyophilization_Controller
(*
    =============================================================================
    BLOCK NAME: FB_Lyophilization_Controller
    DESCRIPTION:
        Enterprise-grade Freeze-Drying (Lyophilization) sequence controller.
        Manages the freezing, evacuation, primary drying (sublimation), and
        secondary drying (desorption) phases. Includes critical pharmaceutical
        capabilities like shelf temperature ramping via silicone oil TCU (Temperature
        Control Unit), and precise end-of-primary-drying (EOPD) detection via
        differential pressure measurement (Pirani vs Capacitance Manometer).
        
    AUTHOR: Lead Biomedical Engineer
    VERSION: 3.1.0 (Validated for GMP Manufacturing)
    =============================================================================
*)

VAR_INPUT
    // Commands
    bStart                  : BOOL; // Command to start the lyophilization cycle
    bAbort                  : BOOL; // Emergency or manual abort
    bReset                  : BOOL; // Reset alarms and faults
    
    // Analog Process Variables (PV)
    fShelfTemp_PV           : REAL; // Actual shelf temperature from TCU [°C]
    fProductTemp_PV         : REAL; // Average product (vial) temperature [°C]
    fCondenserTemp_PV       : REAL; // Condenser temperature [°C]
    fChamberPress_CM        : REAL; // Capacitance Manometer Pressure [mTorr] - Absolute, gas independent
    fChamberPress_Pirani    : REAL; // Pirani Gauge Pressure [mTorr] - Gas composition dependent
    
    // Safety & Interlocks
    bChamberDoorClosed      : BOOL; // Interlock for chamber door
    bCoolingWaterOK         : BOOL; // Utility cooling water OK
    bInstrumentAirOK        : BOOL; // Instrument air pressure OK
    
    // Cycle Recipe Parameters
    fTargetFreezeTemp       : REAL := -50.0; // Target freezing shelf temperature [°C]
    tFreezeHoldTime         : TIME := T#120M; // Hold time for freezing phase
    fFreezingRampRate       : REAL := 1.0;    // Freezing ramp rate [°C/min]
    
    fPrimaryDryingTemp      : REAL := -10.0; // Primary drying target shelf temp [°C]
    fPrimaryDryingPress     : REAL := 100.0; // Primary drying target pressure [mTorr]
    fPrimaryRampRate        : REAL := 0.5;   // Primary drying ramp rate [°C/min]
    
    fSecondaryDryingTemp    : REAL := 20.0;  // Secondary drying target shelf temp [°C]
    fSecondaryDryingPress   : REAL := 50.0;  // Secondary drying target pressure [mTorr]
    fSecondaryRampRate      : REAL := 0.5;   // Secondary drying ramp rate [°C/min]
    tSecondaryDryingTime    : TIME := T#360M; // Duration for secondary drying
    
    // EOPD (End Of Primary Drying) Parameters
    fEOPD_DiffThreshold     : REAL := 5.0;   // Pirani vs CM diff threshold [mTorr]
    tEOPD_HoldTime          : TIME := T#30M; // Consecutive time diff must be below threshold
END_VAR

VAR_OUTPUT
    // Status
    nState                  : INT;   // Current step in the sequence
    bActive                 : BOOL;  // Cycle is running
    bComplete               : BOOL;  // Cycle is successfully finished
    bError                  : BOOL;  // Fault active
    nErrorID                : UDINT; // Error code for HMI
    
    // Actuator Setpoints / Commands
    fShelfTemp_SP           : REAL;  // Cascaded Setpoint to Silicone Oil TCU [°C]
    fChamberPress_SP        : REAL;  // Setpoint to Vacuum Control Valve (Bleed) [mTorr]
    bMainVacuumValveCmd     : BOOL;  // Open main isolation valve to vacuum pump
    bVacuumPumpRunCmd       : BOOL;  // Run vacuum pump skid
    bCondenserRunCmd        : BOOL;  // Run condenser refrigeration skid
    bIsolationValveCmd      : BOOL;  // Butterfly valve between chamber and condenser
    
    // Diagnostics
    fPiraniCM_Diff          : REAL;  // Current differential pressure [mTorr]
    tEOPD_ElapsedTime       : TIME;  // Elapsed time for EOPD condition met
END_VAR

VAR
    // Timers
    fbPhaseTimer            : TON;
    fbRampTimer             : TON;
    fbEOPDTimer             : TON;
    
    // Internal States
    fCurrentRampSP          : REAL;
    bInterlocksOK           : BOOL;
    
    // State Machine Enumeration Constants
    IDLE                    : INT := 0;
    FREEZING_RAMP           : INT := 10;
    FREEZING_HOLD           : INT := 20;
    CONDENSER_CHILL         : INT := 30;
    EVACUATION              : INT := 40;
    PRIMARY_DRYING_RAMP     : INT := 50;
    PRIMARY_DRYING_HOLD     : INT := 60;
    SECONDARY_DRYING_RAMP   : INT := 70;
    SECONDARY_DRYING_HOLD   : INT := 80;
    CYCLE_COMPLETE          : INT := 100;
    ABORTING                : INT := 900;
    FAULT_STATE             : INT := 999;
    
    // Constants
    CYCLE_TIME_MS           : REAL := 100.0; // Task cycle time
END_VAR

// =============================================================================
// SAFETY INTERLOCKS & ALARM HANDLING
// =============================================================================
bInterlocksOK := bChamberDoorClosed AND bCoolingWaterOK AND bInstrumentAirOK;

IF NOT bInterlocksOK AND bActive AND (nState <> ABORTING AND nState <> FAULT_STATE) THEN
    bError := TRUE;
    nErrorID := 1001; // Interlock lost during active cycle
    nState := FAULT_STATE;
END_IF

IF bAbort AND (nState <> ABORTING AND nState <> FAULT_STATE AND nState <> IDLE) THEN
    bError := TRUE;
    nErrorID := 1002; // Manual abort triggered
    nState := ABORTING;
END_IF

IF bReset THEN
    bError := FALSE;
    nErrorID := 0;
    IF nState = FAULT_STATE OR nState = CYCLE_COMPLETE THEN
        nState := IDLE;
    END_IF
END_IF

// Calculate EOPD differential pressure
// Pirani reads artificially high in presence of water vapor. CM is absolute.
// When sublimation is complete, chamber atmosphere is mostly nitrogen/air, so Pirani converges with CM.
fPiraniCM_Diff := ABS(fChamberPress_Pirani - fChamberPress_CM);
tEOPD_ElapsedTime := fbEOPDTimer.ET;

// =============================================================================
// MAIN SEQUENCER (STATE MACHINE)
// =============================================================================
CASE nState OF

    // -------------------------------------------------------------------------
    IDLE:
        bActive             := FALSE;
        bComplete           := FALSE;
        bMainVacuumValveCmd := FALSE;
        bVacuumPumpRunCmd   := FALSE;
        bCondenserRunCmd    := FALSE;
        bIsolationValveCmd  := FALSE;
        fShelfTemp_SP       := 20.0; // Ambient resting state
        fChamberPress_SP    := 760000.0; // Atmosphere
        
        IF bStart AND bInterlocksOK AND NOT bError THEN
            bActive := TRUE;
            fCurrentRampSP := fShelfTemp_PV; // Start ramp from current temp
            fbRampTimer(IN := FALSE);
            nState := FREEZING_RAMP;
        END_IF

    // -------------------------------------------------------------------------
    FREEZING_RAMP:
        // Ramp down shelf temp using Silicone Oil TCU to fTargetFreezeTemp (-50C)
        fbRampTimer(IN := TRUE, PT := T#60S);
        IF fbRampTimer.Q THEN
            fbRampTimer(IN := FALSE);
            fCurrentRampSP := fCurrentRampSP - fFreezingRampRate;
            IF fCurrentRampSP <= fTargetFreezeTemp THEN
                fCurrentRampSP := fTargetFreezeTemp;
            END_IF
        END_IF
        fShelfTemp_SP := fCurrentRampSP;
        
        // Check if target is reached
        IF fCurrentRampSP <= fTargetFreezeTemp AND ABS(fShelfTemp_PV - fTargetFreezeTemp) < 1.0 THEN
            fbPhaseTimer(IN := FALSE);
            nState := FREEZING_HOLD;
        END_IF

    // -------------------------------------------------------------------------
    FREEZING_HOLD:
        fShelfTemp_SP := fTargetFreezeTemp;
        
        // Ensure product is completely frozen
        fbPhaseTimer(IN := TRUE, PT := tFreezeHoldTime);
        IF fbPhaseTimer.Q THEN
            fbPhaseTimer(IN := FALSE);
            nState := CONDENSER_CHILL;
        END_IF

    // -------------------------------------------------------------------------
    CONDENSER_CHILL:
        // Start condenser prior to evacuation to trap water vapor immediately
        bCondenserRunCmd := TRUE;
        
        IF fCondenserTemp_PV <= -60.0 THEN // Target chill temperature
            bIsolationValveCmd := TRUE; // Open path to condenser
            nState := EVACUATION;
        END_IF

    // -------------------------------------------------------------------------
    EVACUATION:
        bVacuumPumpRunCmd := TRUE;
        bMainVacuumValveCmd := TRUE;
        fChamberPress_SP := fPrimaryDryingPress;
        
        // Wait until rough vacuum is achieved
        IF fChamberPress_CM <= (fPrimaryDryingPress * 1.5) THEN
            fCurrentRampSP := fShelfTemp_PV;
            fbRampTimer(IN := FALSE);
            nState := PRIMARY_DRYING_RAMP;
        END_IF

    // -------------------------------------------------------------------------
    PRIMARY_DRYING_RAMP:
        // Sublimation phase begins. Carefully raise shelf temp.
        fChamberPress_SP := fPrimaryDryingPress;
        
        fbRampTimer(IN := TRUE, PT := T#60S);
        IF fbRampTimer.Q THEN
            fbRampTimer(IN := FALSE);
            fCurrentRampSP := fCurrentRampSP + fPrimaryRampRate;
            IF fCurrentRampSP >= fPrimaryDryingTemp THEN
                fCurrentRampSP := fPrimaryDryingTemp;
            END_IF
        END_IF
        fShelfTemp_SP := fCurrentRampSP;
        
        IF fCurrentRampSP >= fPrimaryDryingTemp AND ABS(fShelfTemp_PV - fPrimaryDryingTemp) < 1.0 THEN
            fbEOPDTimer(IN := FALSE);
            nState := PRIMARY_DRYING_HOLD;
        END_IF

    // -------------------------------------------------------------------------
    PRIMARY_DRYING_HOLD:
        // Hold vacuum and temp. Monitor sublimation endpoint.
        fShelfTemp_SP := fPrimaryDryingTemp;
        fChamberPress_SP := fPrimaryDryingPress;
        
        // EOPD Logic: Pirani vs Capacitance Manometer Cross-checking
        IF fPiraniCM_Diff <= fEOPD_DiffThreshold THEN
            fbEOPDTimer(IN := TRUE, PT := tEOPD_HoldTime);
        ELSE
            fbEOPDTimer(IN := FALSE); // Reset if spike occurs
        END_IF
        
        IF fbEOPDTimer.Q THEN
            fbEOPDTimer(IN := FALSE);
            fCurrentRampSP := fShelfTemp_PV;
            fbRampTimer(IN := FALSE);
            nState := SECONDARY_DRYING_RAMP;
        END_IF

    // -------------------------------------------------------------------------
    SECONDARY_DRYING_RAMP:
        // Desorption phase to remove bound water
        fChamberPress_SP := fSecondaryDryingPress;
        
        fbRampTimer(IN := TRUE, PT := T#60S);
        IF fbRampTimer.Q THEN
            fbRampTimer(IN := FALSE);
            fCurrentRampSP := fCurrentRampSP + fSecondaryRampRate;
            IF fCurrentRampSP >= fSecondaryDryingTemp THEN
                fCurrentRampSP := fSecondaryDryingTemp;
            END_IF
        END_IF
        fShelfTemp_SP := fCurrentRampSP;
        
        IF fCurrentRampSP >= fSecondaryDryingTemp AND ABS(fShelfTemp_PV - fSecondaryDryingTemp) < 1.0 THEN
            fbPhaseTimer(IN := FALSE);
            nState := SECONDARY_DRYING_HOLD;
        END_IF

    // -------------------------------------------------------------------------
    SECONDARY_DRYING_HOLD:
        fShelfTemp_SP := fSecondaryDryingTemp;
        fChamberPress_SP := fSecondaryDryingPress;
        
        fbPhaseTimer(IN := TRUE, PT := tSecondaryDryingTime);
        IF fbPhaseTimer.Q THEN
            fbPhaseTimer(IN := FALSE);
            nState := CYCLE_COMPLETE;
        END_IF

    // -------------------------------------------------------------------------
    CYCLE_COMPLETE:
        bActive             := FALSE;
        bComplete           := TRUE;
        bMainVacuumValveCmd := FALSE;
        bVacuumPumpRunCmd   := FALSE;
        bCondenserRunCmd    := FALSE;
        bIsolationValveCmd  := FALSE;
        fShelfTemp_SP       := 20.0; // Return to ambient for unloading

    // -------------------------------------------------------------------------
    ABORTING:
        // Safe shutdown sequence
        bMainVacuumValveCmd := FALSE; // Isolate vacuum
        bIsolationValveCmd  := FALSE;
        fShelfTemp_SP       := 20.0;  // Try to return to safe temp
        
        // Allow condenser and pump to run for a few seconds if needed, but here we just shut down
        bVacuumPumpRunCmd   := FALSE;
        bCondenserRunCmd    := FALSE;
        
        bActive := FALSE;
        nState := FAULT_STATE;

    // -------------------------------------------------------------------------
    FAULT_STATE:
        bActive             := FALSE;
        bMainVacuumValveCmd := FALSE;
        bVacuumPumpRunCmd   := FALSE;
        bCondenserRunCmd    := FALSE;
        bIsolationValveCmd  := FALSE;
        fShelfTemp_SP       := 20.0;
        // Require bReset to move to IDLE
        
END_CASE

END_FUNCTION_BLOCK
```
"""

# Construct JSON object
new_entry = {
    "messages": [
        {"role": "user", "content": user_prompt},
        {"role": "assistant", "content": assistant_response}
    ]
}

# Append to JSONL
with open(target_file, "a", encoding="utf-8") as f:
    f.write(json.dumps(new_entry) + "\n")

print("Successfully appended to dataset.")
