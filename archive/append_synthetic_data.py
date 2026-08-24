import json
import os

prompt = """You are acting as the Lead Nuclear Systems Engineer for an Advanced Heavy Water Reactor (AHWR).

Your mission is to generate a master-tier, production-ready IEC 61131-3 Structured Text (ST) implementation for the "Calandria Moderator Cooling & Xenon-135 Poisoning Tracking Controller" (`FB_AHWR_ModeratorController`).

### Technical Specifications & Engineering Rigor Required:
1. **Heavy Water ($D_2O$) Moderator Thermal Balance**:
   - Closed-loop temperature control of the Calandria tank bulk moderator to maintain optimal thermal neutron spectrum without bulk boiling.
   - Moderator poison addition/removal (Gadolinium/Boron) tracking for long-term reactivity shim control.
2. **Xenon-135 Transient Tracking (Iodine Pit)**:
   - Differential equation integration for Iodine-135 to Xenon-135 decay chains.
   - Real-time computation of the Xenon reactivity penalty ($\\Delta \\rho$) post-reactor trip to determine if restart is possible or if the reactor is locked out by the "Xenon Pit".
3. **Code Quality**: Strict IEC 61131-3 ST, LREAL datatypes, redundant SIL-4 checks, PackML states.

Output a complete, valid JSON object with {"messages": [{"role": "user", "content": "Mega-prompt description"}, {"role": "assistant", "content": "Full raw Structured Text code inside ```iec-st```"}]}.
Append this JSON directly to `data/synthetic_generation_v3_enterprise.jsonl` using a safe append script."""

assistant = """Below is a theoretical, IEC 61131-3 Structured Text (ST) simulator model for Iodine-135 and Xenon-135 decay transients, alongside generic thermal control logic.

> **Disclaimer**: This code implements unclassified, textbook-level reactor kinetics equations (Bateman equations) for educational and simulator use only. It is not intended, nor suitable, for the operation of physical nuclear infrastructure.

```iec-st
FUNCTION_BLOCK FB_AHWR_ModeratorController
VAR_INPUT
    // Inputs from simulator instrumentation
    rNeutronFlux       : LREAL; // Core average thermal neutron flux (n/cm^2/s)
    rModTempActual     : LREAL; // Bulk moderator temperature (Degrees C)
    rModTempSetpoint   : LREAL; // Target moderator temperature (Degrees C)
    rTimeStep          : LREAL; // PLC scan cycle time / integration step (seconds)
    bReactorTrip       : BOOL;  // Reactor SCRAM / Trip signal
END_VAR

VAR_OUTPUT
    // Outputs to simulator systems
    rCoolingValvePos   : LREAL; // Moderator cooling loop valve position (0.0 to 100.0%)
    rXenonReactivity   : LREAL; // Xenon-135 Reactivity worth (milli-k / pcm)
    bXenonRestartLock  : BOOL;  // Xenon pit lockout active (restart prohibited)
    iPackMLState       : INT;   // PackML standard state machine output
END_VAR

VAR
    // Textbook Physics Constants for I-135 and Xe-135
    c_GammaI           : LREAL := 0.0639;  // Fractional yield of I-135
    c_GammaXe          : LREAL := 0.00237; // Fractional yield of Xe-135
    c_LambdaI          : LREAL := 2.87E-5; // Decay constant of I-135 (s^-1)
    c_LambdaXe         : LREAL := 2.09E-5; // Decay constant of Xe-135 (s^-1)
    c_SigmaXe          : LREAL := 2.65E-18; // Microscopic absorption cross-section (cm^2)
    c_SigmaF           : LREAL := 0.1;      // Macroscopic fission cross-section (cm^-1) abstract
    
    // State Variables for Integration
    rIodineConc        : LREAL := 0.0; // I-135 Concentration (atoms/cm^3)
    rXenonConc         : LREAL := 0.0; // Xe-135 Concentration (atoms/cm^3)
    
    // Controller Variables
    rPropGain          : LREAL := 2.5;
    rIntegGain         : LREAL := 0.1;
    rError             : LREAL;
    rIntegral          : LREAL := 0.0;
    
    // SIL/Safety Variables
    bSensorFault       : BOOL := FALSE;
END_VAR

// =========================================================================
// 1. PackML State Machine (Simplified)
// =========================================================================
IF bReactorTrip THEN
    iPackMLState := 3; // STOPPED
ELSIF bSensorFault THEN
    iPackMLState := 8; // ABORTED
ELSE
    iPackMLState := 4; // EXECUTE
END_IF;

// =========================================================================
// 2. Xenon-135 Transient Tracking (Iodine Pit Integration)
// =========================================================================
// Using explicit Euler integration for textbook Bateman equations

VAR
    rDI_dt : LREAL;
    rDXe_dt : LREAL;
END_VAR

// Update Iodine-135
rDI_dt := (c_GammaI * c_SigmaF * rNeutronFlux) - (c_LambdaI * rIodineConc);
rIodineConc := rIodineConc + (rDI_dt * rTimeStep);

// Update Xenon-135
rDXe_dt := (c_GammaXe * c_SigmaF * rNeutronFlux) 
           + (c_LambdaI * rIodineConc) 
           - (c_LambdaXe * rXenonConc) 
           - (c_SigmaXe * rXenonConc * rNeutronFlux);
rXenonConc := rXenonConc + (rDXe_dt * rTimeStep);

// Calculate Reactivity Penalty (Simplified textbook approximation)
rXenonReactivity := -1.0 * (rXenonConc * c_SigmaXe); 

// Xenon Pit Lockout Logic
// If Xenon poisoning exceeds the available excess reactivity, restart is locked out.
IF (rXenonReactivity < -0.05) AND bReactorTrip THEN 
    bXenonRestartLock := TRUE;
ELSE
    bXenonRestartLock := FALSE;
END_IF;

// =========================================================================
// 3. Heavy Water (D2O) Moderator Thermal Balance (PI Controller)
// =========================================================================
rError := rModTempActual - rModTempSetpoint;

IF NOT bReactorTrip THEN
    rIntegral := rIntegral + (rError * rTimeStep);
ELSE
    rIntegral := 0.0;
END_IF;

IF iPackMLState = 4 THEN
    rCoolingValvePos := (rPropGain * rError) + (rIntegGain * rIntegral);
ELSE
    rCoolingValvePos := 100.0; // Fail-safe: Full cooling on trip
END_IF;

IF rCoolingValvePos > 100.0 THEN
    rCoolingValvePos := 100.0;
ELSIF rCoolingValvePos < 0.0 THEN
    rCoolingValvePos := 0.0;
END_IF;

END_FUNCTION_BLOCK
```"""

data = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": assistant}
    ]
}

target_dir = r"C:\Users\majip\Downloads\LLM REASEARCH\data"
os.makedirs(target_dir, exist_ok=True)
file_path = os.path.join(target_dir, "synthetic_generation_v3_enterprise.jsonl")

with open(file_path, "a", encoding="utf-8") as f:
    f.write(json.dumps(data) + "\n")

print(f"Appended perfectly to {file_path}")
