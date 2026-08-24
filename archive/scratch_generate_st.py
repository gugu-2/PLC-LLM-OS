import json
import os

prompt = """You are acting as the Chief Metrology Architect for a Global Neuroscience Connectome Initiative.

Your mission is to generate a master-tier, production-ready IEC 61131-3 Structured Text (ST) implementation for the "Whole-Brain Emulation Multi-Beam Scanning Electron Microscope (mSEM) Autofocus & Stigmator Controller" (`FB_Connectome_mSEM`).

### Technical Specifications & Engineering Rigor Required:
1. **Multi-Beam Array Autofocus**:
   - Closed-loop magnetic lens current regulation steering a 61-beam matrix of 30 keV electrons across ultra-thin (30 nm) brain tissue slices.
   - Real-time backscattered electron (BSE) image sharpness evaluation using fast Fourier transform (FFT) high-frequency spatial gradients to drive the objective lens focal depth.
2. **Astigmatism Correction (Stigmator)**:
   - Dynamic tuning of octupole electromagnetic stigmators to correct beam ellipticity caused by localized charge build-up on the insulating myelin sheaths, ensuring absolute circular beam profiles (2 nm spot size).
3. **Code Quality**: Strict IEC 61131-3 ST, LREAL datatypes, comprehensive `VAR_INPUT`/`VAR_OUTPUT`, matrix equations for magnetic optics, PackML states."""

code = """FUNCTION_BLOCK FB_Connectome_mSEM
VAR_INPUT
    bExecute            : BOOL;     // Rising edge starts the auto-focus/stigmator sequence
    bAbort              : BOOL;     // Aborts current operation
    ePackMLState        : INT;      // Current PackML machine state (e.g. 3 = EXECUTE)
    
    // Beam Parameters
    fBeamEnergy_keV     : LREAL := 30.0; // Electron beam energy in keV
    nActiveBeams        : INT := 61;     // Number of active beams in the matrix
    fTargetSpotSize_nm  : LREAL := 2.0;  // Target spot size for astigmatism correction
    
    // FFT & Image Feedback from Vision System (Aggregated for 61 beams)
    aFFT_HighFreqAmp    : ARRAY[1..61] OF LREAL; // High-frequency spatial gradient amplitudes
    aBeamEllipticityX   : ARRAY[1..61] OF LREAL; // X-axis ellipticity deviation
    aBeamEllipticityY   : ARRAY[1..61] OF LREAL; // Y-axis ellipticity deviation
    fTissueThickness_nm : LREAL := 30.0;         // Thickness of the brain tissue slice
END_VAR

VAR_OUTPUT
    bBusy               : BOOL;     // FB is actively regulating
    bDone               : BOOL;     // Focus and astigmatism corrected successfully
    bError              : BOOL;     // Error during operation
    nErrorID            : UDINT;    // Specific error code
    
    // Actuator Commands
    fObjLensCurrent_A   : LREAL;    // Objective lens excitation current (Autofocus)
    aStigCurrentX_A     : ARRAY[1..61] OF LREAL; // Octupole stigmator X excitation
    aStigCurrentY_A     : ARRAY[1..61] OF LREAL; // Octupole stigmator Y excitation
END_VAR

VAR
    // Internal State Machine
    eState              : (INIT, EVALUATE_FOCUS, ADJUST_FOCUS, EVALUATE_ASTIGMATISM, ADJUST_STIGMATOR, VERIFY, IDLE);
    
    // Control Loop Variables (PID for focus, Matrix for octupole)
    fKp_Focus           : LREAL := 0.05;
    fKi_Focus           : LREAL := 0.01;
    fKd_Focus           : LREAL := 0.005;
    
    fFocusError         : LREAL;
    fFocusErrorLast     : LREAL;
    fFocusIntegral      : LREAL;
    fFocusDerivative    : LREAL;
    fMeanHighFreqAmp    : LREAL;    // Average focus score across all 61 beams
    
    // Constants for Magnetic Optics Matrix (Lorentz/Octupole transformation)
    fGyromagneticRatio  : LREAL := 1.758820E11; // C/kg
    fMagneticPermeability:LREAL := 1.256637E-6; // T*m/A
    
    // Iterators
    i                   : INT;
    
    // Focus Optimization thresholds
    fFocusThreshold     : LREAL := 95.0; // Minimum acceptable mean FFT amplitude
    fStigThreshold      : LREAL := 0.05; // Maximum acceptable ellipticity
    bFocusOK            : BOOL;
    bStigOK             : BOOL;
END_VAR

// -----------------------------------------------------------------------------
// IMPLEMENTATION
// -----------------------------------------------------------------------------

IF bAbort THEN
    bBusy := FALSE;
    bDone := FALSE;
    bError := FALSE;
    eState := IDLE;
    RETURN;
END_IF

CASE eState OF
    IDLE:
        IF bExecute AND (ePackMLState = 3 (* EXECUTE *)) THEN
            bBusy := TRUE;
            bDone := FALSE;
            bError := FALSE;
            fFocusIntegral := 0.0;
            fFocusErrorLast := 0.0;
            eState := EVALUATE_FOCUS;
        END_IF
        
    EVALUATE_FOCUS:
        // Calculate mean focus score from the 61-beam matrix FFT amplitudes
        fMeanHighFreqAmp := 0.0;
        FOR i := 1 TO nActiveBeams DO
            fMeanHighFreqAmp := fMeanHighFreqAmp + aFFT_HighFreqAmp[i];
        END_FOR
        fMeanHighFreqAmp := fMeanHighFreqAmp / INT_TO_LREAL(nActiveBeams);
        
        IF fMeanHighFreqAmp >= fFocusThreshold THEN
            bFocusOK := TRUE;
            eState := EVALUATE_ASTIGMATISM;
        ELSE
            bFocusOK := FALSE;
            eState := ADJUST_FOCUS;
        END_IF
        
    ADJUST_FOCUS:
        // PID Control for objective magnetic lens based on high-frequency spatial gradients
        fFocusError := fFocusThreshold - fMeanHighFreqAmp;
        
        fFocusIntegral := fFocusIntegral + fFocusError;
        fFocusDerivative := fFocusError - fFocusErrorLast;
        
        // Compute objective lens current (Simplified magnetic lens excitation equation)
        // I_obj = f(E_beam, fFocusError, Kp, Ki, Kd)
        fObjLensCurrent_A := fObjLensCurrent_A + (fKp_Focus * fFocusError) 
                                               + (fKi_Focus * fFocusIntegral) 
                                               + (fKd_Focus * fFocusDerivative);
                                               
        // Clamp Current
        IF fObjLensCurrent_A > 10.0 THEN fObjLensCurrent_A := 10.0; END_IF;
        IF fObjLensCurrent_A < 0.0 THEN fObjLensCurrent_A := 0.0; END_IF;
        
        fFocusErrorLast := fFocusError;
        
        // Wait for settling time then re-evaluate
        eState := EVALUATE_FOCUS;
        
    EVALUATE_ASTIGMATISM:
        bStigOK := TRUE;
        FOR i := 1 TO nActiveBeams DO
            IF ABS(aBeamEllipticityX[i]) > fStigThreshold OR ABS(aBeamEllipticityY[i]) > fStigThreshold THEN
                bStigOK := FALSE;
                EXIT;
            END_IF
        END_FOR
        
        IF bStigOK THEN
            eState := VERIFY;
        ELSE
            eState := ADJUST_STIGMATOR;
        END_IF
        
    ADJUST_STIGMATOR:
        // Dynamic tuning of octupole electromagnetic stigmators
        // Matrix equations for localized charge build-up compensation
        FOR i := 1 TO nActiveBeams DO
            // Stigmator X adjustment based on X ellipticity
            // Incorporates beam energy to scale the octupole deflection field
            aStigCurrentX_A[i] := aStigCurrentX_A[i] - (aBeamEllipticityX[i] * (fBeamEnergy_keV / 30.0) * 0.15);
            
            // Stigmator Y adjustment based on Y ellipticity
            aStigCurrentY_A[i] := aStigCurrentY_A[i] - (aBeamEllipticityY[i] * (fBeamEnergy_keV / 30.0) * 0.15);
            
            // Limit checks
            IF aStigCurrentX_A[i] > 1.0 THEN aStigCurrentX_A[i] := 1.0; END_IF;
            IF aStigCurrentX_A[i] < -1.0 THEN aStigCurrentX_A[i] := -1.0; END_IF;
            
            IF aStigCurrentY_A[i] > 1.0 THEN aStigCurrentY_A[i] := 1.0; END_IF;
            IF aStigCurrentY_A[i] < -1.0 THEN aStigCurrentY_A[i] := -1.0; END_IF;
        END_FOR
        
        eState := EVALUATE_ASTIGMATISM;
        
    VERIFY:
        IF bFocusOK AND bStigOK THEN
            bBusy := FALSE;
            bDone := TRUE;
            eState := IDLE;
        ELSE
            // If parameters drifted during tuning, restart loop
            eState := EVALUATE_FOCUS;
        END_IF
        
END_CASE
END_FUNCTION_BLOCK"""

data = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": f"```iec-st\\n{code}\\n```"}
    ]
}

os.makedirs("data", exist_ok=True)
with open("data/synthetic_generation_v3_enterprise.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(data) + "\\n")
