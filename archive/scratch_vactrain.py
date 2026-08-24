import json
import os

prompt = """You are acting as the Lead Traction Engineer for a Global High-Speed Transit Initiative.

Your mission is to generate a master-tier, production-ready IEC 61131-3 Structured Text (ST) implementation for the "Vacuum Tube Superconducting Maglev (vactrain) Linear Synchronous Motor Controller" (`FB_VacuumMaglev_Propulsion`).

### Technical Specifications & Engineering Rigor Required:
1. **Linear Synchronous Motor (LSM) Block Switching**:
   - Real-time stator block energization spanning hundreds of kilometers, activating only the guideway coils directly beneath the vehicle to propel it to Mach 1 ($1,200\\text{ km/h}$).
   - Sub-millisecond synchronization of the stator AC phase angle with the moving onboard Niobium-Titanium superconducting magnets to maximize forward thrust while minimizing parasitic drag.
2. **Vacuum Tube Aerodynamics & Null-Drift Levitation**:
   - Electrodynamic Suspension (EDS) null-flux coil tracking to ensure the vehicle remains perfectly centered within the steel vacuum tube, utilizing active damping to suppress lateral "hunting" oscillations.
   - Piston-effect aerodynamic drag calculations compensating for the residual tube pressure ($100\\text{ Pa}$).
3. **Code Quality**: Strict IEC 61131-3 ST, LREAL datatypes, comprehensive `VAR_INPUT`/`VAR_OUTPUT`, Maxwell's equations integration, PackML states.

Output a complete, valid JSON object with {"messages": [{"role": "user", "content": "Mega-prompt description"}, {"role": "assistant", "content": "Full raw Structured Text code inside ```iec-st```"}]}.
Append this JSON directly to `data/synthetic_generation_v3_enterprise.jsonl` using a safe append script."""

response = """```iec-st
FUNCTION_BLOCK FB_VacuumMaglev_Propulsion
VAR_INPUT
    bEnable                 : BOOL;             // Enable the vactrain propulsion and levitation system
    bEmergencyStop          : BOOL;             // Safety interlock for immediate deceleration and drop
    fTargetVelocity         : LREAL;            // Mach 1 target (m/s) [typically up to ~340.29 m/s]
    fActualVelocity         : LREAL;            // Real-time speed feedback (m/s)
    fVehiclePosition        : LREAL;            // Absolute position along guideway (m)
    fTubePressure           : LREAL;            // Vacuum tube residual pressure, typically 100 Pa
    fLateralDeviation       : LREAL;            // Deviation from null-flux center (m)
    fVerticalDeviation      : LREAL;            // Vertical displacement from optimal suspension height (m)
    fGuidewayTemp           : LREAL;            // Temperature of guideway components (K)
END_VAR

VAR_OUTPUT
    eState                  : E_PackML_State;   // Standard PackML operational state
    fCurrentCommandD        : LREAL;            // Stator d-axis current command (A) for levitation/flux-control
    fCurrentCommandQ        : LREAL;            // Stator q-axis current command (A) for thrust
    fStatorFrequency        : LREAL;            // Output AC frequency to drive moving magnetic field (Hz)
    fStatorPhaseAngle       : LREAL;            // Synchronous phase angle (rad)
    nActiveStatorBlockID    : UDINT;            // ID of the currently energized guideway block
    bBlockTransition        : BOOL;             // High during active block handoff
    fLateralCorrectionForce : LREAL;            // Active damping force requested (N)
    bCryoCoolingWarning     : BOOL;             // High if Nb-Ti SC magnets require thermal intervention
END_VAR

VAR
    // PackML State Machine
    eNextState              : E_PackML_State := E_PackML_State.STOPPED;
    
    // LSM Constants & Variables
    fPolePitch              : LREAL := 0.5;     // Pole pitch of stator winding (m)
    fNominalThrust          : LREAL := 50000.0; // Base thrust mapping coefficient
    fMaxThrust              : LREAL := 250000.0;// Peak thrust capacity (N)
    fPI_Kp                  : LREAL := 1500.0;  // Velocity controller proportional gain
    fPI_Ki                  : LREAL := 500.0;   // Velocity controller integral gain
    fPI_Error               : LREAL;
    fPI_Integral            : LREAL;
    
    // Block Switching
    fBlockLength            : LREAL := 2000.0;  // 2 km stator block segments
    fPositionInBlock        : LREAL;
    
    // Aerodynamics & Drag
    fAeroDragCoef           : LREAL := 2.1;     // Piston effect drag coefficient in confined tube
    fVehicleFrontalArea     : LREAL := 12.0;    // Cross-sectional area (m^2)
    fAirDensity100Pa        : LREAL := 0.00118; // Approx density of air at 100 Pa, 293K (kg/m^3)
    fCalculatedDrag         : LREAL;            // Piston effect drag (N)
    
    // Null-Flux EDS Levitation & Damping
    fNullFluxStiffness      : LREAL := 150000.0;// N/m lateral restoring stiffness
    fNullFluxDamping        : LREAL := 25000.0; // N/(m/s) lateral damping coefficient
    fPrevLateralDev         : LREAL;
    fLateralVelocity        : LREAL;
    
    // Time tracking
    fDeltaT                 : LREAL := 0.001;   // 1 ms cycle time
END_VAR

// -----------------------------------------------------------------------------
// STATE MACHINE IMPLEMENTATION (PackML Subset)
// -----------------------------------------------------------------------------
IF bEmergencyStop THEN
    eState := E_PackML_State.ABORTED;
END_IF

CASE eState OF

    E_PackML_State.STOPPED:
        fCurrentCommandD := 0.0;
        fCurrentCommandQ := 0.0;
        fPI_Integral := 0.0;
        IF bEnable THEN
            eState := E_PackML_State.STARTING;
        END_IF
        
    E_PackML_State.STARTING:
        // Initialize block logic and zero integral terms
        nActiveStatorBlockID := LREAL_TO_UDINT(fVehiclePosition / fBlockLength);
        fPI_Integral := 0.0;
        eState := E_PackML_State.EXECUTE;

    E_PackML_State.EXECUTE:
        IF NOT bEnable THEN
            eState := E_PackML_State.STOPPING;
        ELSE
            // -----------------------------------------------------------------
            // 1. LINEAR SYNCHRONOUS MOTOR (LSM) BLOCK SWITCHING
            // -----------------------------------------------------------------
            // Determine active block and phase handoff
            nActiveStatorBlockID := LREAL_TO_UDINT(fVehiclePosition / fBlockLength);
            fPositionInBlock := fVehiclePosition - (UDINT_TO_LREAL(nActiveStatorBlockID) * fBlockLength);
            
            // Set BlockTransition flag if we are within 50m of the next block
            bBlockTransition := (fPositionInBlock > (fBlockLength - 50.0));

            // -----------------------------------------------------------------
            // 2. SYNCHRONOUS FREQUENCY & PHASE ANGLE (Sub-millisecond resolution)
            // -----------------------------------------------------------------
            // v = 2 * tau * f => f = v / (2 * tau)
            fStatorFrequency := fActualVelocity / (2.0 * fPolePitch);
            
            // Integrate frequency for phase angle: theta = integral(2 * pi * f * dt)
            // Since fActualVelocity changes, phase must track precise vehicle position
            fStatorPhaseAngle := MOD_LREAL( (fVehiclePosition * 3.14159265359 / fPolePitch), (2.0 * 3.14159265359) );

            // -----------------------------------------------------------------
            // 3. AERODYNAMIC DRAG (PISTON EFFECT IN VACUUM TUBE)
            // -----------------------------------------------------------------
            // Drag Equation: F_d = 0.5 * rho * v^2 * C_d * A
            fCalculatedDrag := 0.5 * fAirDensity100Pa * (fActualVelocity * fActualVelocity) * fAeroDragCoef * fVehicleFrontalArea;
            
            // Scale drag slightly based on actual tube pressure variation from 100 Pa baseline
            fCalculatedDrag := fCalculatedDrag * (fTubePressure / 100.0);

            // -----------------------------------------------------------------
            // 4. NULL-FLUX EDS LEVITATION & ACTIVE LATERAL DAMPING
            // -----------------------------------------------------------------
            // Differentiate lateral deviation to find lateral velocity
            fLateralVelocity := (fLateralDeviation - fPrevLateralDev) / fDeltaT;
            fPrevLateralDev := fLateralDeviation;
            
            // Active damping force to suppress lateral "hunting" oscillations
            fLateralCorrectionForce := -(fNullFluxStiffness * fLateralDeviation) - (fNullFluxDamping * fLateralVelocity);
            
            // Modulate d-axis current to support vertical/lateral adjustments
            // (Base D-axis current keeps the Superconducting field stable)
            fCurrentCommandD := 100.0 - (fVerticalDeviation * 1000.0);

            // -----------------------------------------------------------------
            // 5. THRUST VECTORING & Q-AXIS CONTROL
            // -----------------------------------------------------------------
            // Velocity PI Control
            fPI_Error := fTargetVelocity - fActualVelocity;
            fPI_Integral := fPI_Integral + (fPI_Error * fDeltaT);
            
            // Anti-windup
            IF fPI_Integral > fMaxThrust THEN fPI_Integral := fMaxThrust; END_IF
            IF fPI_Integral < -fMaxThrust THEN fPI_Integral := -fMaxThrust; END_IF
            
            // Compute total required thrust including aerodynamic feed-forward
            fCurrentCommandQ := (fPI_Kp * fPI_Error) + (fPI_Ki * fPI_Integral) + fCalculatedDrag;
            
            // Saturate Q-axis command
            IF fCurrentCommandQ > fMaxThrust THEN
                fCurrentCommandQ := fMaxThrust;
            ELSIF fCurrentCommandQ < -fMaxThrust THEN
                fCurrentCommandQ := -fMaxThrust;
            END_IF
            
            // Map thrust to current (simplification: linear mapping in Q-axis)
            fCurrentCommandQ := fCurrentCommandQ / fNominalThrust;
            
            // -----------------------------------------------------------------
            // 6. CRYOGENICS SAFETY MONITORING
            // -----------------------------------------------------------------
            // Nb-Ti superconductor critical temp is ~9.3 K, operate at 4.2 K (liquid helium)
            // If guideway thermal radiation increases tube temp locally, flag warning
            bCryoCoolingWarning := (fGuidewayTemp > 295.0);
            
        END_IF
        
    E_PackML_State.STOPPING:
        // Regenerative braking phase
        fPI_Error := 0.0 - fActualVelocity;
        fCurrentCommandQ := (fPI_Kp * fPI_Error);
        IF fCurrentCommandQ < -fMaxThrust THEN fCurrentCommandQ := -fMaxThrust; END_IF
        
        IF fActualVelocity < 0.1 THEN
            eState := E_PackML_State.STOPPED;
        END_IF
        
    E_PackML_State.ABORTED:
        // Immediate disconnect of stator propulsion, relying on aerodynamic / friction brakes
        fCurrentCommandQ := 0.0;
        fCurrentCommandD := 0.0; // Drops EDS levitation, lands on wheels
        nActiveStatorBlockID := 0;
        IF NOT bEmergencyStop THEN
            eState := E_PackML_State.STOPPED;
        END_IF

END_CASE
END_FUNCTION_BLOCK
```"""

item = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": response}
    ]
}

target_file = 'data/synthetic_generation_v3_enterprise.jsonl'
os.makedirs('data', exist_ok=True)
with open(target_file, 'a', encoding='utf-8') as f:
    f.write(json.dumps(item) + '\\n')
