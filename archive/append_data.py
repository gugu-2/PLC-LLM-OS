import json
import os

prompt = """You are acting as the Principal Hardware Architect for an Exascale Photonic Supercomputing Consortium.

Your mission is to generate a master-tier, production-ready IEC 61131-3 Structured Text (ST) implementation for the "Exascale Optical Cross-Connect (OXC) & Micro-Ring Resonator Thermal Tuning Controller" (`FB_Photonic_Supercomputer_OXC`).

### Technical Specifications & Engineering Rigor Required:
1. **Silicon Photonics Micro-Ring Resonator Tuning**:
   - Closed-loop micro-heater control over a 10,000-node matrix of silicon micro-ring resonators, stabilizing their temperature to within $0.01^\\circ\\text{C}$.
   - This thermal tuning alters the refractive index via the thermo-optic effect, locking the resonant wavelength of each ring to precisely drop or add specific DWDM (Dense Wavelength Division Multiplexing) optical channels carrying terabits of data.
2. **Sub-Nanosecond Optical Switching (MZI)**:
   - Mach-Zehnder Interferometer (MZI) switch network control using electro-optic carrier depletion (forward/reverse bias P-N junctions) for non-blocking, latency-free optical packet routing between thousands of AI tensor cores.
3. **Code Quality**: Strict IEC 61131-3 ST, LREAL datatypes, comprehensive `VAR_INPUT`/`VAR_OUTPUT`, thermo-optic physics equations, PackML states.

Output a complete, valid JSON object with {"messages": [{"role": "user", "content": "Mega-prompt description"}, {"role": "assistant", "content": "Full raw Structured Text code inside ```iec-st```"}]}.
Append this JSON directly to `data/synthetic_generation_v3_enterprise.jsonl` using a safe append script."""

response = """```iec-st
FUNCTION_BLOCK FB_Photonic_Supercomputer_OXC
TITLE = 'Exascale Optical Cross-Connect & Micro-Ring Resonator Controller'
AUTHOR = 'Lumina Elite Synthetic Data Architect'
VERSION = '3.0'

// -----------------------------------------------------------------------------
// DESCRIPTION:
// Master-tier controller for an Exascale Photonic Supercomputing framework.
// Features:
// 1. Closed-loop micro-heater control over a 10,000-node matrix of silicon 
//    micro-ring resonators, stabilizing their temperature to within 0.01 degC.
// 2. Adjusts refractive index via the thermo-optic effect to lock resonant 
//    wavelengths for DWDM optical channels.
// 3. Manages Mach-Zehnder Interferometer (MZI) switch networks using 
//    electro-optic carrier depletion for sub-nanosecond non-blocking optical routing.
// 4. Follows ISA-88/PackML state models for reliable industrial execution.
// -----------------------------------------------------------------------------

VAR_INPUT
    bEnable                  : BOOL;   // Master enable
    bStart                   : BOOL;   // Start tuning & switching matrix
    bStop                    : BOOL;   // Stop operations, revert to safe state
    bReset                   : BOOL;   // Reset faults
    
    // MZI and Ring Resonator Matrix Status
    aRingTemperatures        : ARRAY[1..10000] OF LREAL; // Current temp of each ring (degC)
    aOpticalPowerInputs      : ARRAY[1..10000] OF LREAL; // Incoming optical power (mW)
    aDesiredWavelengths      : ARRAY[1..10000] OF LREAL; // Target resonant wavelength (nm)
    
    // Ambient and cooling
    lrDieTemperature         : LREAL;  // Silicon die baseline temp (degC)
    lrCoolantFlowRate        : LREAL;  // L/min of phase-change coolant
END_VAR

VAR_OUTPUT
    // MZI Switch Control (Voltage for electro-optic modulation)
    aMZIBiasVoltages         : ARRAY[1..10000] OF LREAL; // P-N junction bias (V)
    
    // Micro-Heater Control
    aMicroHeaterPWM          : ARRAY[1..10000] OF LREAL; // PWM duty cycle 0.0 to 100.0%
    
    // PackML Status
    ePackMLState             : INT;    // Current PackML State (e.g., 3=Stopped, 6=Execute)
    bSystemReady             : BOOL;   // Matrix is locked and ready for routing
    
    bFault                   : BOOL;   // Fault active
    nFaultCode               : UDINT;  // Fault ID
END_VAR

VAR
    // Constants for Thermo-Optic Physics
    cThermoOpticCoeff        : LREAL := 1.86E-4; // dn/dT for Silicon at 1550nm (1/K)
    cGroupIndex              : LREAL := 4.23;    // Group index for waveguide
    cRingRadius              : LREAL := 10.0;    // um
    cReferenceTemp           : LREAL := 25.0;    // degC
    cReferenceWavelength     : LREAL := 1550.0;  // nm
    
    // Control variables
    i                        : INT;
    lrErrorTemp              : LREAL;
    lrTargetTemp             : LREAL;
    lrDeltaWavelength        : LREAL;
    
    // PID state for each ring
    aIntegralSum             : ARRAY[1..10000] OF LREAL;
    aLastError               : ARRAY[1..10000] OF LREAL;
    
    // PID Gains
    lrKp                     : LREAL := 150.5;
    lrKi                     : LREAL := 12.0;
    lrKd                     : LREAL := 5.1;
    lrDt                     : LREAL := 0.001; // 1 ms scan time
    
    // Internal PackML State Machine Constants
    STATE_ABORTED            : INT := 1;
    STATE_STOPPED            : INT := 3;
    STATE_IDLE               : INT := 4;
    STATE_STARTING           : INT := 5;
    STATE_EXECUTE            : INT := 6;
    STATE_ABORTING           : INT := 9;
    STATE_STOPPING           : INT := 10;
END_VAR

// =============================================================================
// MAIN EXECUTION LOGIC
// =============================================================================

// Fault Handling
IF lrDieTemperature > 85.0 THEN
    bFault := TRUE;
    nFaultCode := 16#F001; // Over-temperature critical fault
    ePackMLState := STATE_ABORTING;
END_IF;

IF bReset THEN
    bFault := FALSE;
    nFaultCode := 0;
    IF ePackMLState = STATE_ABORTED THEN
        ePackMLState := STATE_STOPPED;
    END_IF;
END_IF;

// PackML State Machine
CASE ePackMLState OF

    STATE_ABORTED:
        bSystemReady := FALSE;
        // Zero all outputs
        FOR i := 1 TO 10000 DO
            aMicroHeaterPWM[i] := 0.0;
            aMZIBiasVoltages[i] := 0.0;
        END_FOR;
        
    STATE_STOPPED:
        bSystemReady := FALSE;
        IF bEnable THEN
            ePackMLState := STATE_IDLE;
        END_IF;
        
    STATE_IDLE:
        IF NOT bEnable THEN
            ePackMLState := STATE_STOPPED;
        ELSIF bStart THEN
            ePackMLState := STATE_STARTING;
        END_IF;
        
    STATE_STARTING:
        // Initialize PID structures
        FOR i := 1 TO 10000 DO
            aIntegralSum[i] := 0.0;
            aLastError[i] := 0.0;
        END_FOR;
        ePackMLState := STATE_EXECUTE;
        
    STATE_EXECUTE:
        IF bStop THEN
            ePackMLState := STATE_STOPPING;
        ELSIF NOT bEnable THEN
            ePackMLState := STATE_ABORTING;
        ELSE
            // -----------------------------------------------------------------
            // Core Physics & Tuning Loop (10,000 Nodes)
            // -----------------------------------------------------------------
            bSystemReady := TRUE; // Assume ready until proven otherwise
            
            FOR i := 1 TO 10000 DO
                // 1. Calculate required temperature shift based on wavelength targeting
                // Formula: dW = W0 * (dn/dT) * dT / n_g
                lrDeltaWavelength := aDesiredWavelengths[i] - cReferenceWavelength;
                
                // Solve for required target temperature
                // dT = (dW * n_g) / (W0 * (dn/dT))
                lrTargetTemp := cReferenceTemp + ((lrDeltaWavelength * cGroupIndex) / (cReferenceWavelength * cThermoOpticCoeff));
                
                // 2. PID Control for Micro-Heaters
                lrErrorTemp := lrTargetTemp - aRingTemperatures[i];
                
                // If any ring is off target by more than 0.01 degC, system is not fully locked
                IF ABS(lrErrorTemp) > 0.01 THEN
                    bSystemReady := FALSE;
                END_IF;
                
                // Accumulate Integral
                aIntegralSum[i] := aIntegralSum[i] + (lrErrorTemp * lrDt);
                // Anti-windup
                IF aIntegralSum[i] > 1000.0 THEN aIntegralSum[i] := 1000.0; END_IF;
                IF aIntegralSum[i] < -1000.0 THEN aIntegralSum[i] := -1000.0; END_IF;
                
                // Calculate output
                aMicroHeaterPWM[i] := (lrKp * lrErrorTemp) + (lrKi * aIntegralSum[i]) + (lrKd * (lrErrorTemp - aLastError[i]) / lrDt);
                
                // Clamp PWM to 0.0% - 100.0%
                IF aMicroHeaterPWM[i] > 100.0 THEN
                    aMicroHeaterPWM[i] := 100.0;
                ELSIF aMicroHeaterPWM[i] < 0.0 THEN
                    aMicroHeaterPWM[i] := 0.0;
                END_IF;
                
                aLastError[i] := lrErrorTemp;
                
                // 3. MZI Switching Control
                // Apply reverse bias based on optical routing demands (simplified to a mapping here)
                // Carrier depletion modulation typically uses 1V to 5V reverse bias to alter phase.
                IF aDesiredWavelengths[i] > 1550.0 THEN
                    // Routing active
                    aMZIBiasVoltages[i] := 2.5; // -2.5V Bias
                ELSE
                    // Pass-through
                    aMZIBiasVoltages[i] := 0.0; // 0V Bias
                END_IF;
            END_FOR;
        END_IF;
        
    STATE_STOPPING:
        bSystemReady := FALSE;
        // Graceful power down of heaters
        FOR i := 1 TO 10000 DO
            aMicroHeaterPWM[i] := aMicroHeaterPWM[i] * 0.95; // Decay
            aMZIBiasVoltages[i] := 0.0;
            IF aMicroHeaterPWM[i] < 0.1 THEN
                aMicroHeaterPWM[i] := 0.0;
            END_IF;
        END_FOR;
        // If all off, transition
        ePackMLState := STATE_STOPPED;
        
    STATE_ABORTING:
        bSystemReady := FALSE;
        FOR i := 1 TO 10000 DO
            aMicroHeaterPWM[i] := 0.0;
            aMZIBiasVoltages[i] := 0.0;
        END_FOR;
        ePackMLState := STATE_ABORTED;
        
    ELSE
        ePackMLState := STATE_ABORTED;
        
END_CASE;
END_FUNCTION_BLOCK
```"""

obj = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": response}
    ]
}

os.makedirs('data', exist_ok=True)
with open('data/synthetic_generation_v3_enterprise.jsonl', 'a', encoding='utf-8') as f:
    f.write(json.dumps(obj) + '\\n')
print("Successfully appended to data/synthetic_generation_v3_enterprise.jsonl")
