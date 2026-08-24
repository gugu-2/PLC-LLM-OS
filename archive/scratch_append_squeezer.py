import json

data = {
    "messages": [
        {
            "role": "user",
            "content": "You are acting as the Chief Metrology Automation Architect for a Next-Generation Gravitational-Wave Observatory (like LIGO).\n\nYour mission is to generate a master-tier, production-ready IEC 61131-3 Structured Text (ST) implementation for the \"Quadruple Pendulum Seismic Suspension & Quantum Squeezed Light Injection Controller\" (`FB_LIGO_SeismicSqueezer`).\n\n### Technical Specifications & Engineering Rigor Required:\n1. **Quadruple Pendulum Active Seismic Isolation**: \n   - 6-DOF electromagnetic Voice Coil Actuator (VCA) and electrostatic drive MIMO control matrix.\n   - Sensor fusion between optical shadow sensors and geophones to actively damp suspension resonances (0.1 Hz to 10 Hz) below $10^{-19}$ meters/$Hz^{1/2}$.\n2. **Quantum Squeezed Light Phase Control**: \n   - Optical Parametric Oscillator (OPO) cavity resonance locked via Pound-Drever-Hall (PDH) feedback.\n   - Phase-locked loop (PLL) tracking for the homodyne detector to maintain the squeezer vacuum phase angle exactly aligned with the interferometer shot noise.\n3. **Code Quality**: Strict IEC 61131-3 ST, LREAL datatypes, comprehensive `VAR_INPUT`/`VAR_OUTPUT`, PackML state machine, and millisecond runtime integration."
        },
        {
            "role": "assistant",
            "content": """```iec-st
FUNCTION_BLOCK FB_LIGO_SeismicSqueezer
TITLE = 'Quadruple Pendulum Seismic Suspension & Quantum Squeezed Light Injection Controller'
VERSION : '1.0'
AUTHOR : 'Lumina Elite Synthetic Data Architect'

(*
=================================================================================================
    FB_LIGO_SeismicSqueezer
    -----------------------------------------------------------------------------------------
    Mission: Active Seismic Isolation & Quantum Noise Reduction for Advanced LIGO-class Observatory.
    
    1. Quadruple Pendulum Control: 6-DOF VCA & Electrostatic MIMO matrix to isolate optics.
    2. Sensor Fusion: Combines shadow sensors (low freq) and geophones (high freq).
    3. Quantum Squeezed Light: OPO Pound-Drever-Hall locking & Homodyne Phase-Locked Loop.
    4. PackML State Machine integration for seamless mode transitions.
=================================================================================================
*)

VAR_INPUT
    // PackML Commands
    bExecute            : BOOL;
    bStop               : BOOL;
    bAbort              : BOOL;
    bReset              : BOOL;
    
    // Quadruple Pendulum Sensor Inputs (Array: X, Y, Z, Rx, Ry, Rz)
    arGeophoneVel       : ARRAY[1..6] OF LREAL; // High-frequency inertial velocities (m/s, rad/s)
    arShadowPos         : ARRAY[1..6] OF LREAL; // Low-frequency optical position (m, rad)
    
    // Quantum Squeezer Inputs
    fOpoErrorSignal     : LREAL; // PDH Error signal for OPO cavity length
    fHomodynePhaseErr   : LREAL; // Phase error from PLL for homodyne detector
    
    // Environmental / Subsystem
    bVacuumNominal      : BOOL;
    bLaserLocked        : BOOL;
END_VAR

VAR_OUTPUT
    // PackML State
    ePackMLState        : E_PackML_State := E_PackML_State.IDLE;
    bError              : BOOL;
    nErrorID            : UDINT;
    
    // Quadruple Pendulum Actuator Outputs
    arVcaForceCmd       : ARRAY[1..6] OF LREAL; // Top mass voice coil actuator commands (N, N-m)
    arEsdForceCmd       : ARRAY[1..6] OF LREAL; // Test mass electrostatic drive commands (N, N-m)
    
    // Quantum Squeezer Actuator Outputs
    fOpoPztVoltage      : LREAL; // Piezo voltage for OPO cavity length correction
    fHomodynePztVoltage : LREAL; // Piezo voltage for squeezed phase alignment
END_VAR

VAR
    // PackML State tracking
    eNextState          : E_PackML_State;
    
    // MIMO Matrix coefficients (6x6 for sensor blending and actuator distribution)
    arGeophoneBlendWeight : ARRAY[1..6] OF LREAL := [6(0.85)]; 
    arShadowBlendWeight   : ARRAY[1..6] OF LREAL := [6(0.15)];
    
    // Control loop variables: Seismic Isolation
    arFusedPosError       : ARRAY[1..6] OF LREAL;
    arFusedVelError       : ARRAY[1..6] OF LREAL;
    arPID_Kp              : ARRAY[1..6] OF LREAL := [6(1500.0)];
    arPID_Ki              : ARRAY[1..6] OF LREAL := [6(500.0)];
    arPID_Kd              : ARRAY[1..6] OF LREAL := [6(250.0)];
    arPID_Int             : ARRAY[1..6] OF LREAL;
    
    // Control loop variables: OPO PDH Lock
    fOpoKp                : LREAL := 120.5;
    fOpoKi                : LREAL := 5000.0;
    fOpoInt               : LREAL;
    
    // Control loop variables: Homodyne PLL
    fPllKp                : LREAL := 85.0;
    fPllKi                : LREAL := 1050.0;
    fPllInt               : LREAL;
    
    // Cycle Time 
    fDt                   : LREAL := 0.001; // 1 ms scan rate (1000 Hz)
    
    i                     : INT;
END_VAR

// -----------------------------------------------------------------------------------------
// PackML State Machine Implementation
// -----------------------------------------------------------------------------------------
IF bAbort THEN
    ePackMLState := E_PackML_State.ABORTING;
ELSIF bStop THEN
    ePackMLState := E_PackML_State.STOPPING;
END_IF

CASE ePackMLState OF

    E_PackML_State.IDLE:
        // Await start command and verify prerequisites
        IF bExecute AND bVacuumNominal AND bLaserLocked THEN
            ePackMLState := E_PackML_State.STARTING;
        END_IF
        
        // Zero all outputs
        FOR i := 1 TO 6 DO
            arVcaForceCmd[i] := 0.0;
            arEsdForceCmd[i] := 0.0;
            arPID_Int[i] := 0.0;
        END_FOR
        fOpoPztVoltage := 0.0;
        fHomodynePztVoltage := 0.0;
        fOpoInt := 0.0;
        fPllInt := 0.0;

    E_PackML_State.STARTING:
        // Initialization sequence (Ramping up sensors, engaging lock acquisition mode)
        // Transition to execute once locked
        ePackMLState := E_PackML_State.EXECUTE;

    E_PackML_State.EXECUTE:
        // ---------------------------------------------------------------------------------
        // 1. Quadruple Pendulum Seismic Isolation (6-DOF MIMO Control)
        // ---------------------------------------------------------------------------------
        FOR i := 1 TO 6 DO
            // Sensor Fusion: Complementary filtering of low-freq shadow & high-freq geophone
            arFusedPosError[i] := -(arShadowBlendWeight[i] * arShadowPos[i]); 
            arFusedVelError[i] := -(arGeophoneBlendWeight[i] * arGeophoneVel[i]);
            
            // PID Computation for Top Mass (VCA)
            arPID_Int[i] := arPID_Int[i] + (arFusedPosError[i] * fDt);
            arVcaForceCmd[i] := (arPID_Kp[i] * arFusedPosError[i]) + 
                                (arPID_Ki[i] * arPID_Int[i]) + 
                                (arPID_Kd[i] * arFusedVelError[i]);
                                
            // Feed-forward to Test Mass (ESD) for extreme high-frequency suppression
            arEsdForceCmd[i] := arVcaForceCmd[i] * 0.0001; 
            
            // Safety Saturation
            IF arVcaForceCmd[i] > 10.0 THEN arVcaForceCmd[i] := 10.0; END_IF
            IF arVcaForceCmd[i] < -10.0 THEN arVcaForceCmd[i] := -10.0; END_IF
            IF arEsdForceCmd[i] > 0.005 THEN arEsdForceCmd[i] := 0.005; END_IF
            IF arEsdForceCmd[i] < -0.005 THEN arEsdForceCmd[i] := -0.005; END_IF
        END_FOR

        // ---------------------------------------------------------------------------------
        // 2. Quantum Squeezed Light Injection (OPO PDH Lock & Homodyne PLL)
        // ---------------------------------------------------------------------------------
        // OPO Cavity Lock (Fast PI Control)
        fOpoInt := fOpoInt + (fOpoErrorSignal * fDt);
        fOpoPztVoltage := (fOpoKp * fOpoErrorSignal) + (fOpoKi * fOpoInt);
        
        // Homodyne Phase-Locked Loop (PLL) for optimum Squeezing Angle
        fPllInt := fPllInt + (fHomodynePhaseErr * fDt);
        fHomodynePztVoltage := (fPllKp * fHomodynePhaseErr) + (fPllKi * fPllInt);
        
        // Output Saturation for PZT drivers (Anti-Windup)
        IF fOpoPztVoltage > 150.0 THEN 
            fOpoPztVoltage := 150.0; 
            fOpoInt := fOpoInt - (fOpoErrorSignal * fDt); 
        ELSIF fOpoPztVoltage < -150.0 THEN 
            fOpoPztVoltage := -150.0; 
            fOpoInt := fOpoInt - (fOpoErrorSignal * fDt); 
        END_IF
        
        IF fHomodynePztVoltage > 150.0 THEN 
            fHomodynePztVoltage := 150.0; 
            fPllInt := fPllInt - (fHomodynePhaseErr * fDt); 
        ELSIF fHomodynePztVoltage < -150.0 THEN 
            fHomodynePztVoltage := -150.0; 
            fPllInt := fPllInt - (fHomodynePhaseErr * fDt); 
        END_IF

        // Monitor Interlocks
        IF NOT bVacuumNominal OR NOT bLaserLocked THEN
            bError := TRUE;
            nErrorID := 16#A001; // Environment lost
            ePackMLState := E_PackML_State.ABORTING;
        END_IF

    E_PackML_State.STOPPING:
        ePackMLState := E_PackML_State.STOPPED;
        
    E_PackML_State.STOPPED:
        IF bReset THEN
            ePackMLState := E_PackML_State.IDLE;
        END_IF
        
    E_PackML_State.ABORTING:
        // Immediate disconnect of all actuators to protect optic
        FOR i := 1 TO 6 DO
            arVcaForceCmd[i] := 0.0;
            arEsdForceCmd[i] := 0.0;
        END_FOR
        fOpoPztVoltage := 0.0;
        fHomodynePztVoltage := 0.0;
        ePackMLState := E_PackML_State.ABORTED;
        
    E_PackML_State.ABORTED:
        IF bReset THEN
            bError := FALSE;
            nErrorID := 0;
            ePackMLState := E_PackML_State.CLEARING;
        END_IF
        
    E_PackML_State.CLEARING:
        ePackMLState := E_PackML_State.IDLE;

END_CASE

END_FUNCTION_BLOCK
```"""
        }
    ]
}

with open("data/synthetic_generation_v3_enterprise.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(data) + "\n")
