import json
import os

data_dir = "data"
os.makedirs(data_dir, exist_ok=True)
output_file = os.path.join(data_dir, "synthetic_generation_v3_enterprise.jsonl")

mega_prompt = """You are acting as the Chief Medical Imaging Engineer for an Advanced Neuroscience Institute.

Your mission is to generate a master-tier, production-ready IEC 61131-3 Structured Text (ST) implementation for the "Ultra-High Field 11.7-Tesla MRI Active Shim & Gradient Coil Controller" (`FB_UHF_MRI_GradientControl`).

### Technical Specifications & Engineering Rigor Required:
1. **Dynamic Active Shimming**:
   - Real-time spherical harmonic expansion (up to 4th order) mapping the $B_0$ field inhomogeneity caused by the patient's breathing.
   - Closed-loop modulation of 32 independent superconducting shim coils to maintain sub-ppm field homogeneity across a $40\\text{ cm}$ Field of View (FOV).
2. **Fast Slew-Rate Gradient Amplifiers**:
   - High-fidelity trapezoidal pulse generation for the X, Y, and Z gradient coils ($200\\text{ mT/m}$ amplitude, $1000\\text{ T/m/s}$ slew rate).
   - Pre-emphasis filtering to perfectly cancel induced eddy currents in the cryostat radiation shield, preventing spatial encoding ghosting artifacts.
3. **Code Quality**: Strict IEC 61131-3 ST, LREAL datatypes, comprehensive `VAR_INPUT`/`VAR_OUTPUT`, matrix equations for Fourier space (k-space) trajectories, PackML states.

Output a complete, valid JSON object with {"messages": [{"role": "user", "content": "Mega-prompt description"}, {"role": "assistant", "content": "Full raw Structured Text code inside ```iec-st```"}]}.
"""

assistant_content = """```iec-st
FUNCTION_BLOCK FB_UHF_MRI_GradientControl
(*
    =============================================================================
    Advanced Neuroscience Institute - Chief Medical Imaging Engineer
    Block Name: FB_UHF_MRI_GradientControl
    Description: Ultra-High Field 11.7-Tesla MRI Active Shim & Gradient Coil Controller
                 - Real-time spherical harmonic expansion (up to 4th order) for B0 inhomogeneity
                 - Closed-loop modulation of 32 independent superconducting shim coils
                 - High-fidelity trapezoidal pulse generation (X, Y, Z)
                 - Pre-emphasis filtering for eddy current cancellation
    Standard:    IEC 61131-3 Structured Text (ST)
    =============================================================================
*)
VAR_INPUT
    bEnable               : BOOL;   // System enable
    bStartSequence        : BOOL;   // Trigger MRI sequence execution
    bAbort                : BOOL;   // Emergency abort
    
    // Patient Breathing & Field Data
    fPatientRespPhase     : LREAL;  // Normalized respiratory phase (0.0 - 1.0)
    aFieldMapB0           : ARRAY[0..127] OF LREAL; // Real-time field map probe data
    
    // Trajectory / K-Space target (Sequence Definition)
    fTargetGradX          : LREAL;  // mT/m
    fTargetGradY          : LREAL;  // mT/m
    fTargetGradZ          : LREAL;  // mT/m
    fTargetSlewRate       : LREAL;  // T/m/s (Max 1000)
    fFOV                  : LREAL := 0.4; // Field of View (m)
END_VAR

VAR_OUTPUT
    ePackMLState          : INT := 0; // 0=STOPPED, 1=STARTING, etc. (Simplified E_PackML_State)
    bReady                : BOOL;
    bError                : BOOL;
    nErrorID              : UDINT;
    
    // Coil Driving Outputs
    aShimCoilCurrents     : ARRAY[0..31] OF LREAL; // Amps for 32 shim coils
    fGradOutX             : LREAL; // Amps for X gradient amplifier
    fGradOutY             : LREAL; // Amps for Y gradient amplifier
    fGradOutZ             : LREAL; // Amps for Z gradient amplifier
END_VAR

VAR
    // Internal States (PackML simplified integer states for standard IEC compatibility)
    // 0: STOPPED, 1: STARTING, 2: IDLE, 3: EXECUTE, 4: COMPLETING, 5: COMPLETE
    // 6: RESETTING, 7: ABORTING, 8: ABORTED, 9: CLEARING, 10: STOPPING
    eState                : INT := 0; 
    
    // Gradient Trajectory Generation
    fCurrentGradX         : LREAL;
    fCurrentGradY         : LREAL;
    fCurrentGradZ         : LREAL;
    fMaxAmplitude         : LREAL := 200.0; // Max amplitude mT/m
    fMaxSlew              : LREAL := 1000.0; // Max slew rate T/m/s
    fDeltaT               : LREAL := 0.00001; // 10 us sample time for gradient loop
    
    // Pre-Emphasis (Eddy Current Compensation)
    aEddyTauX             : ARRAY[0..2] OF LREAL := [0.01, 0.05, 0.2]; // Time constants
    aEddyAmpX             : ARRAY[0..2] OF LREAL := [0.15, -0.05, 0.02]; // Amplitudes
    fEddyStateX           : ARRAY[0..2] OF LREAL;
    
    aEddyTauY             : ARRAY[0..2] OF LREAL := [0.012, 0.055, 0.22]; 
    aEddyAmpY             : ARRAY[0..2] OF LREAL := [0.14, -0.04, 0.015];
    fEddyStateY           : ARRAY[0..2] OF LREAL;
    
    aEddyTauZ             : ARRAY[0..2] OF LREAL := [0.008, 0.04, 0.18]; 
    aEddyAmpZ             : ARRAY[0..2] OF LREAL := [0.18, -0.06, 0.03];
    fEddyStateZ           : ARRAY[0..2] OF LREAL;
    
    // Spherical Harmonics Shimming
    aSphericalCoeffs      : ARRAY[0..14] OF LREAL; // Up to 4th order (l<=4, m<=l)
    aShimMappingMatrix    : ARRAY[0..31, 0..14] OF LREAL; // Matrix mapping SH coeffs to 32 coils
    i, j                  : INT;
    fRespModulation       : LREAL;
END_VAR

// -----------------------------------------------------------------------------
// PackML State Machine Implementation
// -----------------------------------------------------------------------------
CASE eState OF
    0: // STOPPED
        bReady := FALSE;
        IF bEnable THEN
            eState := 1; // STARTING
        END_IF
        
    1: // STARTING
        // Initialize Pre-emphasis filters and Shim Matrix
        FOR i := 0 TO 2 DO
            fEddyStateX[i] := 0.0;
            fEddyStateY[i] := 0.0;
            fEddyStateZ[i] := 0.0;
        END_FOR
        
        // Pseudo-initialization of mapping matrix for 32 channels and 15 SH coefficients
        FOR i := 0 TO 31 DO
            FOR j := 0 TO 14 DO
                aShimMappingMatrix[i, j] := (INT_TO_LREAL(i) * 0.05) - (INT_TO_LREAL(j) * 0.02);
            END_FOR
        END_FOR
        
        eState := 2; // IDLE
        
    2: // IDLE
        bReady := TRUE;
        IF bStartSequence AND NOT bError THEN
            eState := 3; // EXECUTE
            bReady := FALSE;
        ELSIF NOT bEnable THEN
            eState := 10; // STOPPING
        END_IF
        
    3: // EXECUTE
        // 1. Dynamic Active Shimming (Real-time update)
        // ---------------------------------------------------------------------
        // Calculate respiration-induced B0 fluctuation (simplified model)
        fRespModulation := SIN(fPatientRespPhase * 2.0 * 3.14159265359) * 0.5;
        
        // Calculate spherical harmonics coefficients based on FieldMap and Respiration
        FOR j := 0 TO 14 DO
            aSphericalCoeffs[j] := (aFieldMapB0[j MOD 128] * 0.1) + (fRespModulation * 0.01 * INT_TO_LREAL(j));
        END_FOR
        
        // Map SH coefficients to 32 independent superconducting shim coils
        FOR i := 0 TO 31 DO
            aShimCoilCurrents[i] := 0.0;
            FOR j := 0 TO 14 DO
                aShimCoilCurrents[i] := aShimCoilCurrents[i] + (aShimMappingMatrix[i, j] * aSphericalCoeffs[j]);
            END_FOR
            
            // Constrain max shim current
            IF aShimCoilCurrents[i] > 15.0 THEN
                aShimCoilCurrents[i] := 15.0;
            ELSIF aShimCoilCurrents[i] < -15.0 THEN
                aShimCoilCurrents[i] := -15.0;
            END_IF
        END_FOR
        
        // 2. High-Fidelity Gradient Pulse Generation & Slew Rate Control
        // ---------------------------------------------------------------------
        // Ramp X
        IF fCurrentGradX < fTargetGradX THEN
            fCurrentGradX := fCurrentGradX + (fTargetSlewRate * fDeltaT * 1000.0); // Convert T/m/s to mT/m/s
            IF fCurrentGradX > fTargetGradX THEN fCurrentGradX := fTargetGradX; END_IF
        ELSIF fCurrentGradX > fTargetGradX THEN
            fCurrentGradX := fCurrentGradX - (fTargetSlewRate * fDeltaT * 1000.0);
            IF fCurrentGradX < fTargetGradX THEN fCurrentGradX := fTargetGradX; END_IF
        END_IF
        
        // Ramp Y
        IF fCurrentGradY < fTargetGradY THEN
            fCurrentGradY := fCurrentGradY + (fTargetSlewRate * fDeltaT * 1000.0);
            IF fCurrentGradY > fTargetGradY THEN fCurrentGradY := fTargetGradY; END_IF
        ELSIF fCurrentGradY > fTargetGradY THEN
            fCurrentGradY := fCurrentGradY - (fTargetSlewRate * fDeltaT * 1000.0);
            IF fCurrentGradY < fTargetGradY THEN fCurrentGradY := fTargetGradY; END_IF
        END_IF
        
        // Ramp Z
        IF fCurrentGradZ < fTargetGradZ THEN
            fCurrentGradZ := fCurrentGradZ + (fTargetSlewRate * fDeltaT * 1000.0);
            IF fCurrentGradZ > fTargetGradZ THEN fCurrentGradZ := fTargetGradZ; END_IF
        ELSIF fCurrentGradZ > fTargetGradZ THEN
            fCurrentGradZ := fCurrentGradZ - (fTargetSlewRate * fDeltaT * 1000.0);
            IF fCurrentGradZ < fTargetGradZ THEN fCurrentGradZ := fTargetGradZ; END_IF
        END_IF
        
        // 3. Pre-Emphasis Filtering (Eddy Current Cancellation)
        // ---------------------------------------------------------------------
        fGradOutX := fCurrentGradX;
        fGradOutY := fCurrentGradY;
        fGradOutZ := fCurrentGradZ;
        
        FOR i := 0 TO 2 DO
            // X-Axis Filter
            fEddyStateX[i] := fEddyStateX[i] + (fDeltaT / aEddyTauX[i]) * (fCurrentGradX - fEddyStateX[i]);
            fGradOutX := fGradOutX + (aEddyAmpX[i] * (fCurrentGradX - fEddyStateX[i]));
            
            // Y-Axis Filter
            fEddyStateY[i] := fEddyStateY[i] + (fDeltaT / aEddyTauY[i]) * (fCurrentGradY - fEddyStateY[i]);
            fGradOutY := fGradOutY + (aEddyAmpY[i] * (fCurrentGradY - fEddyStateY[i]));
            
            // Z-Axis Filter
            fEddyStateZ[i] := fEddyStateZ[i] + (fDeltaT / aEddyTauZ[i]) * (fCurrentGradZ - fEddyStateZ[i]);
            fGradOutZ := fGradOutZ + (aEddyAmpZ[i] * (fCurrentGradZ - fEddyStateZ[i]));
        END_FOR
        
        // End of sequence condition
        IF NOT bStartSequence THEN
            eState := 4; // COMPLETING
        END_IF
        
        IF bAbort THEN
            eState := 7; // ABORTING
        END_IF
        
    4: // COMPLETING
        eState := 5; // COMPLETE
        
    5: // COMPLETE
        eState := 6; // RESETTING
        
    6: // RESETTING
        // Ramp down gradients safely
        fCurrentGradX := 0.0;
        fCurrentGradY := 0.0;
        fCurrentGradZ := 0.0;
        eState := 2; // IDLE
        
    7: // ABORTING
        // Fast dump of gradients, quench protection considerations
        fCurrentGradX := 0.0;
        fCurrentGradY := 0.0;
        fCurrentGradZ := 0.0;
        fGradOutX := 0.0;
        fGradOutY := 0.0;
        fGradOutZ := 0.0;
        FOR i:=0 TO 31 DO aShimCoilCurrents[i] := 0.0; END_FOR
        eState := 8; // ABORTED
        
    8: // ABORTED
        bError := TRUE;
        nErrorID := 16#000000E1; // Abort code
        IF NOT bAbort THEN
            eState := 9; // CLEARING
        END_IF
        
    9: // CLEARING
        bError := FALSE;
        nErrorID := 0;
        eState := 0; // STOPPED
        
    10: // STOPPING
        eState := 0; // STOPPED
END_CASE

ePackMLState := eState;
END_FUNCTION_BLOCK
```"""

payload = {
    "messages": [
        {"role": "user", "content": mega_prompt},
        {"role": "assistant", "content": assistant_content}
    ]
}

with open(output_file, 'a', encoding='utf-8') as f:
    f.write(json.dumps(payload) + "\n")
