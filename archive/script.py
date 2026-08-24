import json
import sys

prompt = """You are acting as the Principal Materials Scientist for an Advanced Superconductor Fabrication Facility.

Your mission is to generate a master-tier, production-ready IEC 61131-3 Structured Text (ST) implementation for the "Pulsed Laser Deposition (PLD) YBCO High-Temperature Superconductor Epitaxial Growth Controller" (`FB_PLD_Superconductor`).

### Technical Specifications & Engineering Rigor Required:
1. **Excimer Laser Target Ablation**:
   - Nanosecond-precision triggering of a 248 nm KrF excimer laser at 50 Hz to ablate a YBCO ($YBa_2Cu_3O_{7-x}$) ceramic target.
   - Raster-scanning mirror control to ensure uniform target erosion and prevent particulate "boulder" formation in the plasma plume.
2. **Epitaxial Plume Dynamics & Oxygenation**:
   - Real-time mass flow control of background Oxygen gas (200 mTorr) to ensure proper stoichiometry of the expanding plasma plume as it strikes the heated Strontium Titanate (STO) substrate.
   - PID substrate heater control maintaining exactly 750°C to promote perfect monocrystalline epitaxial alignment for maximum superconducting critical current ($J_c$).
3. **Code Quality**: Strict IEC 61131-3 ST, LREAL datatypes, comprehensive `VAR_INPUT`/`VAR_OUTPUT`, PackML states."""

code = """```iec-st
(*
================================================================================
FB_PLD_Superconductor
================================================================================
Description:
Master-tier Pulsed Laser Deposition (PLD) controller for YBCO High-Temperature 
Superconductor Epitaxial Growth. Controls KrF Excimer Laser triggering (50 Hz), 
raster-scanning target erosion mirrors, oxygen background mass flow, and PID 
substrate heating (750 degC) for optimal epitaxial alignment on STO substrate.

PackML State Model implemented for industrial robustness.
================================================================================
*)

FUNCTION_BLOCK FB_PLD_Superconductor
VAR_INPUT
    bEnable                 : BOOL;                 (* Enable PLD System *)
    bStart                  : BOOL;                 (* Start Deposition Cycle *)
    bStop                   : BOOL;                 (* Stop Deposition Cycle *)
    bAbort                  : BOOL;                 (* Emergency Abort *)
    
    // Process Setpoints
    fTargetO2Pressure       : LREAL := 200.0;       (* mTorr, Background O2 Pressure *)
    fTargetSubstrateTemp    : LREAL := 750.0;       (* degC, Heater Setpoint *)
    fLaserFrequency         : LREAL := 50.0;        (* Hz, KrF Excimer Rep Rate *)
    fLaserEnergy            : LREAL := 450.0;       (* mJ, Laser Pulse Energy *)
    
    // Process Feedback
    fActualO2Pressure       : LREAL;                (* mTorr, from Baratron Gauge *)
    fActualSubstrateTemp    : LREAL;                (* degC, from Pyrometer/TC *)
    fLaserPowerFeedback     : LREAL;                (* mJ, from Energy Monitor *)
    bVacuumInterlockOk      : BOOL;                 (* Vacuum level acceptable *)
    bLaserReady             : BOOL;                 (* Laser warmed up and ready *)
END_VAR

VAR_OUTPUT
    // PackML State
    eCurrentState           : E_PackML_State;       (* Current PackML State *)
    bActive                 : BOOL;                 (* Deposition in progress *)
    bError                  : BOOL;                 (* System Error Active *)
    nErrorID                : UDINT;                (* Error Code *)
    
    // Actuator Commands
    bLaserTrigger           : BOOL;                 (* Nanosecond Trigger to KrF Laser *)
    fO2MassFlowCmd          : LREAL;                (* sccm, Command to O2 MFC *)
    fHeaterPowerCmd         : LREAL;                (* %, Command to Substrate Heater *)
    fMirrorX_PosCmd         : LREAL;                (* mm, Raster X-Axis *)
    fMirrorY_PosCmd         : LREAL;                (* mm, Raster Y-Axis *)
END_VAR

VAR
    // Internal State
    eNextState              : E_PackML_State := E_PackML_State.STOPPED;
    
    // Controllers
    fbHeaterPID             : FB_PID_Advanced;
    fbPressurePID           : FB_PID_Advanced;
    
    // Timers & Triggers
    fbLaserTriggerTimer     : TON;
    fLaserPeriodMs          : LREAL;
    
    // Raster Scanning Variables
    fRasterPhaseX           : LREAL := 0.0;
    fRasterPhaseY           : LREAL := 0.0;
    fRasterAmplitude        : LREAL := 15.0;        (* mm *)
    fRasterSpeedX           : LREAL := 2.5;         (* rad/s *)
    fRasterSpeedY           : LREAL := 1.7;         (* rad/s - irrational ratio for lissajous *)
    fDtSeconds              : LREAL;
    
    // System Constants
    cTempTolerance          : LREAL := 1.5;         (* degC *)
    cPressTolerance         : LREAL := 5.0;         (* mTorr *)
    
    // Diagnostics
    nTotalPulses            : UDINT := 0;
END_VAR

// -----------------------------------------------------------------------------
// 1. PackML State Machine
// -----------------------------------------------------------------------------
IF bAbort THEN
    eNextState := E_PackML_State.ABORTING;
END_IF

eCurrentState := eNextState;

CASE eCurrentState OF

    E_PackML_State.STOPPED:
        bActive := FALSE;
        bLaserTrigger := FALSE;
        fHeaterPowerCmd := 0.0;
        fO2MassFlowCmd := 0.0;
        
        IF bEnable AND bStart THEN
            eNextState := E_PackML_State.STARTING;
        END_IF
        
    E_PackML_State.STARTING:
        // Initialize PID Controllers
        fbHeaterPID.fKp := 2.5;
        fbHeaterPID.fKi := 0.05;
        fbHeaterPID.fKd := 0.1;
        
        fbPressurePID.fKp := 1.0;
        fbPressurePID.fKi := 0.2;
        fbPressurePID.fKd := 0.0;
        
        IF bVacuumInterlockOk THEN
            eNextState := E_PackML_State.EXECUTE;
        ELSE
            eNextState := E_PackML_State.HOLDING; // Waiting for vacuum
        END_IF
        
    E_PackML_State.EXECUTE:
        bActive := TRUE;
        
        // ---------------------------------------------------------------------
        // Substrate Heating Control (750 degC for Epitaxy)
        // ---------------------------------------------------------------------
        fbHeaterPID(
            fSetpoint := fTargetSubstrateTemp,
            fFeedback := fActualSubstrateTemp,
            fOutput => fHeaterPowerCmd
        );
        
        // ---------------------------------------------------------------------
        // Background Oxygen Control (200 mTorr)
        // ---------------------------------------------------------------------
        fbPressurePID(
            fSetpoint := fTargetO2Pressure,
            fFeedback := fActualO2Pressure,
            fOutput => fO2MassFlowCmd
        );
        
        // Check Conditions for Laser Firing
        IF bLaserReady AND 
           ABS(fActualSubstrateTemp - fTargetSubstrateTemp) < cTempTolerance AND
           ABS(fActualO2Pressure - fTargetO2Pressure) < cPressTolerance THEN
           
            // -----------------------------------------------------------------
            // Target Raster-Scanning (Lissajous Pattern to prevent boulders)
            // -----------------------------------------------------------------
            // Calculate dt
            fDtSeconds := 0.01; // Assuming 10ms task cycle time for this block
            
            fRasterPhaseX := fRasterPhaseX + (fRasterSpeedX * fDtSeconds);
            fRasterPhaseY := fRasterPhaseY + (fRasterSpeedY * fDtSeconds);
            
            IF fRasterPhaseX > 6.2831853 THEN fRasterPhaseX := fRasterPhaseX - 6.2831853; END_IF
            IF fRasterPhaseY > 6.2831853 THEN fRasterPhaseY := fRasterPhaseY - 6.2831853; END_IF
            
            fMirrorX_PosCmd := fRasterAmplitude * SIN(fRasterPhaseX);
            fMirrorY_PosCmd := fRasterAmplitude * SIN(fRasterPhaseY);
            
            // -----------------------------------------------------------------
            // KrF Excimer Laser Triggering (50 Hz)
            // -----------------------------------------------------------------
            fLaserPeriodMs := 1000.0 / fLaserFrequency;
            fbLaserTriggerTimer(IN := NOT fbLaserTriggerTimer.Q, PT := LREAL_TO_TIME(fLaserPeriodMs));
            
            IF fbLaserTriggerTimer.Q THEN
                bLaserTrigger := TRUE;
                nTotalPulses := nTotalPulses + 1;
            ELSE
                bLaserTrigger := FALSE;
            END_IF
            
        ELSE
            bLaserTrigger := FALSE; // Suppress laser if conditions drift
        END_IF
        
        IF bStop THEN
            eNextState := E_PackML_State.STOPPING;
        END_IF
        
    E_PackML_State.STOPPING:
        bLaserTrigger := FALSE;
        fHeaterPowerCmd := 0.0;
        fO2MassFlowCmd := 0.0;
        eNextState := E_PackML_State.STOPPED;
        
    E_PackML_State.ABORTING:
        bLaserTrigger := FALSE;
        fHeaterPowerCmd := 0.0;
        fO2MassFlowCmd := 0.0;
        bError := TRUE;
        nErrorID := 999;
        eNextState := E_PackML_State.ABORTED;
        
    E_PackML_State.ABORTED:
        // Wait for reset
        IF NOT bAbort THEN
            bError := FALSE;
            eNextState := E_PackML_State.STOPPED;
        END_IF

END_CASE;
END_FUNCTION_BLOCK
```"""

entry = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": code}
    ]
}

file_path = r"c:\Users\majip\Downloads\LLM REASEARCH\data\synthetic_generation_v3_enterprise.jsonl"
with open(file_path, "a", encoding="utf-8") as f:
    f.write(json.dumps(entry) + "\n")

print("Done")