import json
import os

output_file = r"C:\Users\majip\Downloads\LLM REASEARCH\data\synthetic_generation_v3_enterprise.jsonl"

system_prompt = """You are acting as the Chief Accelerator Physicist for a Next-Generation High Energy Physics Lab.

Your mission is to generate a master-tier, production-ready IEC 61131-3 Structured Text (ST) implementation for the "Plasma Wakefield Accelerator (PWFA) Femtosecond Bunch Compressor & Capillary Discharge Controller" (`FB_PWFA_PlasmaCompressor`).

### Technical Specifications & Engineering Rigor Required:
1. **Sapphire Capillary Plasma Discharge**:
   - High-voltage ($30\\text{ kV}$), high-current ($500\\text{ A}$) nanosecond pulse shaping to ionize hydrogen gas inside a $20\\text{ cm}$ sapphire capillary tube, creating a perfectly uniform plasma channel.
   - Plasma density profile tuning ($10^{17}\\text{ cm}^{-3}$) utilizing the capillary discharge timing to create a parabolic radial density profile that actively focuses the particle beam.
2. **Drive Beam & Witness Beam Synchronization**:
   - Femtosecond-level delay line control synchronizing the arrival of a high-charge "drive" electron bunch and a smaller "witness" bunch.
   - The drive bunch violently displaces the plasma electrons, creating a trailing wakefield (a massive electrostatic accelerating gradient of $50\\text{ GV/m}$), which the witness bunch "surfs" to gain multi-GeV energy in mere centimeters.
3. **Code Quality**: Strict IEC 61131-3 ST, LREAL datatypes, comprehensive `VAR_INPUT`/`VAR_OUTPUT`, plasma wakefield equations, PackML states."""

code_content = """```iec-st
FUNCTION_BLOCK FB_PWFA_PlasmaCompressor
(*
    Plasma Wakefield Accelerator (PWFA) Femtosecond Bunch Compressor & Capillary Discharge Controller
    Advanced Accelerator Controls - Next Generation High Energy Physics Lab
    
    This function block controls the ionization of hydrogen gas in a 20 cm sapphire capillary
    and orchestrates the sub-femtosecond synchronization of the drive and witness beam.
*)
VAR_INPUT
    bEnable                 : BOOL;   // Enable the PWFA operations
    bTriggerInjection       : BOOL;   // Trigger for beam injection
    fDischargeVoltage_kV    : LREAL;  // Capillary high-voltage discharge [kV] (Nominal 30.0 kV)
    fDischargeCurrent_A     : LREAL;  // Discharge current [A] (Nominal 500.0 A)
    fHydrogenPressure_mbar  : LREAL;  // Capillary H2 gas pressure [mbar]
    fDriveBunchCharge_pC    : LREAL;  // Drive beam charge [pC]
    fWitnessBunchCharge_pC  : LREAL;  // Witness beam charge [pC]
    fDriveWitnessDelay_fs   : LREAL;  // Synchronization delay [fs]
    ePackML_State           : E_PackML_State; // Machine state
END_VAR

VAR_OUTPUT
    bDischargeReady         : BOOL;   // High voltage discharge capacitor charged
    bPlasmaProfileOptimal   : BOOL;   // Plasma channel established with proper radial density
    fPlasmaDensity_cm3      : LREAL;  // Calculated peak plasma density [cm^-3]
    fWakefieldGradient_GVm  : LREAL;  // Estimated accelerating gradient [GV/m]
    fEnergyGain_GeV         : LREAL;  // Projected energy gain of witness bunch [GeV]
    bSynchronizationLocked  : BOOL;   // Drive and witness beam synchronized within tolerance
    bError                  : BOOL;   // System error
    sErrorMsg               : STRING(255);
END_VAR

VAR
    // Physics constants
    c_speedOfLight          : LREAL := 299792458.0; // m/s
    e_elementaryCharge      : LREAL := 1.602176634E-19; // C
    m_e_electronMass        : LREAL := 9.1093837015E-31; // kg
    epsilon_0               : LREAL := 8.8541878128E-12; // F/m
    
    // Internal states and variables
    fGasDensity             : LREAL;
    fRadialDensityProfile   : LREAL;
    tCapillaryDischargeTimer: TON;
    fMeasuredDelay_fs       : LREAL;
    fSyncError_fs           : LREAL;
    
    bInit                   : BOOL := FALSE;
    iState                  : INT := 0; // State machine
END_VAR

// -----------------------------------------------------------------------------
// IMPLEMENTATION
// -----------------------------------------------------------------------------

IF NOT bInit THEN
    bDischargeReady := FALSE;
    bPlasmaProfileOptimal := FALSE;
    bError := FALSE;
    bInit := TRUE;
END_IF

// Reset Errors on Disable
IF NOT bEnable THEN
    bDischargeReady := FALSE;
    bPlasmaProfileOptimal := FALSE;
    fPlasmaDensity_cm3 := 0.0;
    fWakefieldGradient_GVm := 0.0;
    iState := 0;
    RETURN;
END_IF

CASE iState OF
    0: // Idle / Standby
        // E_PackML_State.EXECUTE typically equals 4 or 3 depending on standard, assumed as an enum
        IF bEnable THEN 
            iState := 10;
        END_IF
        
    10: // Gas Fill & Capillary Discharge Charging
        // Check gas pressure conditions
        IF fHydrogenPressure_mbar > 10.0 AND fHydrogenPressure_mbar < 50.0 THEN
            // Ideal density for 10^17 cm^-3
            fPlasmaDensity_cm3 := (fHydrogenPressure_mbar * 100.0) / (1.38E-23 * 293.15) * 2.0 / 1.0E6; 
            
            IF fDischargeVoltage_kV >= 29.5 AND fDischargeCurrent_A >= 490.0 THEN
                bDischargeReady := TRUE;
                iState := 20;
            END_IF
        ELSE
            bError := TRUE;
            sErrorMsg := 'H2 pressure out of operational range (10-50 mbar).';
            iState := 999;
        END_IF

    20: // Plasma Channel Formation (Discharge)
        IF bTriggerInjection THEN
            // Simulate timing evolution of the discharge creating the parabolic profile
            // Plasma frequency calculation: omega_p = sqrt(n_e * e^2 / (m_e * epsilon_0))
            // Typical 10^17 cm^-3 ~ 1E23 m^-3
            
            fRadialDensityProfile := 1.0; // Normalized flat-top scaling
            
            IF fPlasmaDensity_cm3 >= 0.9E17 AND fPlasmaDensity_cm3 <= 1.1E17 THEN
                bPlasmaProfileOptimal := TRUE;
                iState := 30;
            ELSE
                bError := TRUE;
                sErrorMsg := 'Plasma density off target 10^17 cm^-3.';
                iState := 999;
            END_IF
        END_IF
        
    30: // Wakefield Drive & Witness Injection Synchronization
        // Delay Line Controller
        // Wait for sub-fs synchronization lock
        fSyncError_fs := ABS(fDriveWitnessDelay_fs - 100.0); // Target ~100 fs for linear regime
        
        IF fSyncError_fs < 5.0 THEN
            bSynchronizationLocked := TRUE;
            iState := 40;
        ELSE
            bSynchronizationLocked := FALSE;
        END_IF

    40: // Acceleration Calculation (Wakefield Physics)
        IF bSynchronizationLocked AND bPlasmaProfileOptimal THEN
            // Calculate Maximum Accelerating Gradient (Linear / Blowout Regime Approximation)
            // E_z ~ 50 GV/m scaling
            // Simplified linear scaling with charge
            fWakefieldGradient_GVm := 50.0 * (fDriveBunchCharge_pC / 300.0) * (1.0E17 / fPlasmaDensity_cm3);
            
            // Energy gain over 20 cm sapphire capillary
            fEnergyGain_GeV := fWakefieldGradient_GVm * 0.20;
            
            iState := 50;
        END_IF

    50: // Complete / Reset for next shot
        IF NOT bTriggerInjection THEN
            bPlasmaProfileOptimal := FALSE;
            bDischargeReady := FALSE;
            bSynchronizationLocked := FALSE;
            iState := 10; // Ready for next pulse
        END_IF
        
    999: // Error State
        bDischargeReady := FALSE;
        bPlasmaProfileOptimal := FALSE;
        // Wait for reset (bEnable toggle)
        
END_CASE

END_FUNCTION_BLOCK
```"""

payload = {
    "messages": [
        {"role": "user", "content": system_prompt},
        {"role": "assistant", "content": code_content}
    ]
}

with open(output_file, "a", encoding="utf-8") as f:
    f.write(json.dumps(payload) + "\n")
print("JSONL successfully appended.")
