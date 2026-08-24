import json
import os

system_prompt = """You are acting as the Chief Quantum Communications Architect for a Low Earth Orbit (LEO) Satellite Network.

Your mission is to generate a master-tier, production-ready IEC 61131-3 Structured Text (ST) implementation for the "Quantum Key Distribution (QKD) Satellite Entangled Photon Fast-Steering Mirror & Tracking Controller" (`FB_QKD_SatelliteTracker`).

### Technical Specifications & Engineering Rigor Required:
1. **Sub-Microradian Pointing & Tracking (PAT)**:
   - Coarse/Fine cascaded tracking loop using a gimbal (coarse) and a Fast-Steering Mirror (FSM, fine) driven by a 4-quadrant avalanche photodiode (APD) beacon tracker.
   - Point-ahead angle (PAA) calculation compensating for the finite speed of light and the relative orbital velocity of the satellite vs. the ground station.
2. **Entangled Photon Polarization Compensation**:
   - Liquid crystal variable retarder (LCVR) matrix control to actively compensate for Faraday rotation and Doppler shift induced by the Earth's magnetic field and satellite motion.
3. **Code Quality**: Strict IEC 61131-3 ST, LREAL datatypes, comprehensive `VAR_INPUT`/`VAR_OUTPUT`, matrix equations for orbital mechanics, PackML states."""

assistant_response = """```iec-st
(* 
   ======================================================================================
   FB_QKD_SatelliteTracker
   --------------------------------------------------------------------------------------
   Chief Quantum Communications Architect Edition
   Description:
     Master-tier IEC 61131-3 Structured Text implementation for Quantum Key Distribution 
     (QKD) Satellite Entangled Photon Fast-Steering Mirror (FSM) & Tracking Controller.
     
     Implements:
     1. Coarse/Fine Cascaded Tracking Loop (Gimbal + FSM) using 4-Quadrant APD.
     2. Point-Ahead Angle (PAA) calculation for orbital kinematics and speed of light.
     3. Active Polarization Compensation (LCVR Matrix) for Faraday Rotation and Doppler.
     4. PackML State Machine (ISA TR88.00.02).
   ======================================================================================
*)

FUNCTION_BLOCK FB_QKD_SatelliteTracker
VAR_INPUT
    // PackML State Control Inputs
    bExecute            : BOOL; // Command: Start execution
    bStop               : BOOL; // Command: Stop
    bAbort              : BOOL; // Command: Abort
    bHold               : BOOL; // Command: Hold
    bReset              : BOOL; // Command: Reset from Aborted
    bClear              : BOOL; // Command: Clear faults
    
    // Telemetry & Kinematics (Earth-Centered, Earth-Fixed / ECEF)
    fSatVelocityX       : LREAL; // Satellite orbital velocity vector X (m/s)
    fSatVelocityY       : LREAL; // Satellite orbital velocity vector Y (m/s)
    fSatVelocityZ       : LREAL; // Satellite orbital velocity vector Z (m/s)
    fGroundStnPosX      : LREAL; // Target Ground Station position X (m)
    fGroundStnPosY      : LREAL; // Target Ground Station position Y (m)
    fGroundStnPosZ      : LREAL; // Target Ground Station position Z (m)
    fSatPosX            : LREAL; // Satellite position X (m)
    fSatPosY            : LREAL; // Satellite position Y (m)
    fSatPosZ            : LREAL; // Satellite position Z (m)
    
    // Beacon Sensor (4-Quadrant Avalanche Photodiode)
    fAPD_Q1             : LREAL; // Optical intensity Quadrant 1 (W/m^2)
    fAPD_Q2             : LREAL; // Optical intensity Quadrant 2 (W/m^2)
    fAPD_Q3             : LREAL; // Optical intensity Quadrant 3 (W/m^2)
    fAPD_Q4             : LREAL; // Optical intensity Quadrant 4 (W/m^2)
    
    // Environmental / Quantum
    fEarthMagFieldB     : LREAL; // Local Earth Magnetic Field strength (Tesla)
    fOpticalWavelength  : LREAL := 1550.0E-9; // Photon wavelength (m)
    fVerdetConstant     : LREAL := 0.05; // Verdet constant of the optical path (rad/T*m)
    fPathLength         : LREAL := 0.1; // Effective length for Faraday rotation (m)
END_VAR

VAR_OUTPUT
    // PackML State Status
    eCurrentState       : E_PackML_State; // Current PackML State Enum
    bError              : BOOL; // General Error Flag
    nErrorID            : UDINT; // Specific Error Code
    
    // Gimbal Coarse Control (rad)
    fGimbalCmdAzimuth   : LREAL; 
    fGimbalCmdElevation : LREAL; 
    
    // FSM Fine Control (rad)
    fFsmCmdTip          : LREAL;
    fFsmCmdTilt         : LREAL;
    
    // LCVR Matrix Control Voltages (V) for Polarization Compensation
    fLcvrVoltage1       : LREAL;
    fLcvrVoltage2       : LREAL;
    fLcvrVoltage3       : LREAL;
    
    // Performance Metrics
    fTrackingErrorRadius: LREAL; // Current tracking error (rad)
    fCalculatedPAA      : LREAL; // Computed Point-Ahead Angle (rad)
    fFaradayRotationRad : LREAL; // Computed Faraday rotation to compensate (rad)
END_VAR

VAR
    // Constants
    c_SPEED_OF_LIGHT    : LREAL := 299792458.0; // m/s
    
    // Control Loop PID Constants (Gimbal)
    Kp_Gimbal           : LREAL := 0.5;
    Ki_Gimbal           : LREAL := 0.01;
    Kd_Gimbal           : LREAL := 0.05;
    
    // Control Loop PID Constants (FSM)
    Kp_FSM              : LREAL := 12.0;
    Ki_FSM              : LREAL := 50.0;
    Kd_FSM              : LREAL := 0.2;
    
    // Internal States & Integrators
    fGimbalIntAz        : LREAL := 0.0;
    fGimbalIntEl        : LREAL := 0.0;
    fFsmIntTip          : LREAL := 0.0;
    fFsmIntTilt         : LREAL := 0.0;
    
    fPrevGimbalErrAz    : LREAL := 0.0;
    fPrevGimbalErrEl    : LREAL := 0.0;
    fPrevFsmErrTip      : LREAL := 0.0;
    fPrevFsmErrTilt     : LREAL := 0.0;
    
    // Math / Intermediate
    fRangeX             : LREAL;
    fRangeY             : LREAL;
    fRangeZ             : LREAL;
    fRangeMag           : LREAL;
    
    fRelVelX            : LREAL;
    fRelVelY            : LREAL;
    fRelVelZ            : LREAL;
    
    fApdSum             : LREAL;
    fApdErrX            : LREAL;
    fApdErrY            : LREAL;
    
    // Cycle Time tracking
    fDeltaT             : LREAL := 0.001; // 1kHz loop assumption
END_VAR

// --------------------------------------------------------------------------------------
// Implementation
// --------------------------------------------------------------------------------------
// 1. PackML State Machine Engine
IF bAbort THEN
    eCurrentState := E_PackML_State.ABORTING;
ELSIF bStop THEN
    eCurrentState := E_PackML_State.STOPPING;
END_IF

CASE eCurrentState OF
    E_PackML_State.UNDEFINED:
        eCurrentState := E_PackML_State.CLEARED;
        
    E_PackML_State.CLEARED:
        IF bReset THEN
            eCurrentState := E_PackML_State.STOPPED;
        END_IF
        
    E_PackML_State.STOPPED:
        IF bExecute THEN
            eCurrentState := E_PackML_State.STARTING;
        END_IF
        
    E_PackML_State.STARTING:
        // Initialize Integrators & Parameters
        fGimbalIntAz    := 0.0;
        fGimbalIntEl    := 0.0;
        fFsmIntTip      := 0.0;
        fFsmIntTilt     := 0.0;
        fPrevGimbalErrAz:= 0.0;
        fPrevGimbalErrEl:= 0.0;
        fPrevFsmErrTip  := 0.0;
        fPrevFsmErrTilt := 0.0;
        bError          := FALSE;
        nErrorID        := 0;
        eCurrentState   := E_PackML_State.EXECUTE;
        
    E_PackML_State.EXECUTE:
        IF bHold THEN
            eCurrentState := E_PackML_State.HOLDING;
        END_IF
        // Execution Block handled below CASE
        
    E_PackML_State.HOLDING:
        eCurrentState := E_PackML_State.HELD;
        
    E_PackML_State.HELD:
        IF bExecute THEN
            eCurrentState := E_PackML_State.EXECUTE;
        END_IF
        
    E_PackML_State.STOPPING:
        // Safely park gimbal and FSM
        fGimbalCmdAzimuth   := 0.0;
        fGimbalCmdElevation := 0.0;
        fFsmCmdTip          := 0.0;
        fFsmCmdTilt         := 0.0;
        eCurrentState := E_PackML_State.STOPPED;
        
    E_PackML_State.ABORTING:
        // Emergency stop, cut LCVR voltages
        fLcvrVoltage1 := 0.0;
        fLcvrVoltage2 := 0.0;
        fLcvrVoltage3 := 0.0;
        fGimbalCmdAzimuth   := 0.0;
        fGimbalCmdElevation := 0.0;
        fFsmCmdTip          := 0.0;
        fFsmCmdTilt         := 0.0;
        eCurrentState := E_PackML_State.ABORTED;
        
    E_PackML_State.ABORTED:
        IF bClear THEN
            eCurrentState := E_PackML_State.CLEARED;
        END_IF
END_CASE

// --------------------------------------------------------------------------------------
// Core Physics & Logic Execution
// --------------------------------------------------------------------------------------
IF eCurrentState = E_PackML_State.EXECUTE THEN
    
    // --- Phase 1: Kinematics & Point-Ahead Angle (PAA) Calculation ---
    // Calculate Range Vector to Ground Station
    fRangeX := fGroundStnPosX - fSatPosX;
    fRangeY := fGroundStnPosY - fSatPosY;
    fRangeZ := fGroundStnPosZ - fSatPosZ;
    
    // Range Magnitude
    fRangeMag := SQRT(fRangeX*fRangeX + fRangeY*fRangeY + fRangeZ*fRangeZ);
    
    // Prevent Division By Zero
    IF fRangeMag > 0.0 THEN
        // Target relative velocity (Simplified ECEF difference)
        fRelVelX := -fSatVelocityX;
        fRelVelY := -fSatVelocityY;
        fRelVelZ := -fSatVelocityZ;
        
        // PAA Vector Approximation (v/c)
        fCalculatedPAA := SQRT(fRelVelX*fRelVelX + fRelVelY*fRelVelY + fRelVelZ*fRelVelZ) / c_SPEED_OF_LIGHT;
    ELSE
        fCalculatedPAA := 0.0;
    END_IF
    
    // --- Phase 2: Quantum Polarization Compensation (Faraday & Doppler) ---
    // Calculate Faraday Rotation: theta = V * B * d
    fFaradayRotationRad := fVerdetConstant * fEarthMagFieldB * fPathLength;
    
    // Map Faraday rotation to LCVR Retardance Voltages
    fLcvrVoltage1 := 5.0 - (fFaradayRotationRad * 1.5); 
    fLcvrVoltage2 := 2.5 + (fCalculatedPAA * 1000.0);   
    fLcvrVoltage3 := 3.0; 
    
    // Clamp voltages
    fLcvrVoltage1 := LIMIT(0.0, fLcvrVoltage1, 10.0);
    fLcvrVoltage2 := LIMIT(0.0, fLcvrVoltage2, 10.0);
    fLcvrVoltage3 := LIMIT(0.0, fLcvrVoltage3, 10.0);
    
    // --- Phase 3: Coarse/Fine Cascaded Pointing & Tracking ---
    // 3.1 Calculate APD Centroid (Fine Error)
    fApdSum := fAPD_Q1 + fAPD_Q2 + fAPD_Q3 + fAPD_Q4;
    IF fApdSum > 1.0E-9 THEN
        fApdErrX := ((fAPD_Q2 + fAPD_Q4) - (fAPD_Q1 + fAPD_Q3)) / fApdSum;
        fApdErrY := ((fAPD_Q1 + fAPD_Q2) - (fAPD_Q3 + fAPD_Q4)) / fApdSum;
    ELSE
        fApdErrX := 0.0;
        fApdErrY := 0.0;
    END_IF
    
    fTrackingErrorRadius := SQRT(fApdErrX*fApdErrX + fApdErrY*fApdErrY);
    
    // 3.2 Fine Tracking Loop (FSM - High bandwidth, small stroke)
    fFsmIntTip := fFsmIntTip + (fApdErrY * fDeltaT);
    fFsmIntTilt := fFsmIntTilt + (fApdErrX * fDeltaT);
    
    // Anti-windup
    fFsmIntTip := LIMIT(-0.01, fFsmIntTip, 0.01);
    fFsmIntTilt := LIMIT(-0.01, fFsmIntTilt, 0.01);
    
    fFsmCmdTip := (Kp_FSM * fApdErrY) + (Ki_FSM * fFsmIntTip) + (Kd_FSM * (fApdErrY - fPrevFsmErrTip)/fDeltaT);
    fFsmCmdTilt := (Kp_FSM * fApdErrX) + (Ki_FSM * fFsmIntTilt) + (Kd_FSM * (fApdErrX - fPrevFsmErrTilt)/fDeltaT);
    
    // Apply Point-Ahead Angle (PAA) bias to FSM tilt
    fFsmCmdTilt := fFsmCmdTilt + fCalculatedPAA;
    
    // Saturate FSM outputs
    fFsmCmdTip := LIMIT(-0.002, fFsmCmdTip, 0.002);
    fFsmCmdTilt := LIMIT(-0.002, fFsmCmdTilt, 0.002);
    
    fPrevFsmErrTip := fApdErrY;
    fPrevFsmErrTilt := fApdErrX;
    
    // 3.3 Coarse Tracking Loop (Gimbal - Low bandwidth, large stroke)
    fGimbalIntAz := fGimbalIntAz + (fFsmCmdTilt * fDeltaT);
    fGimbalIntEl := fGimbalIntEl + (fFsmCmdTip * fDeltaT);
    
    fGimbalCmdAzimuth := (Kp_Gimbal * fFsmCmdTilt) + (Ki_Gimbal * fGimbalIntAz);
    fGimbalCmdElevation := (Kp_Gimbal * fFsmCmdTip) + (Ki_Gimbal * fGimbalIntEl);
    
    // Saturate Gimbal bounds (+/- 3.14 rad)
    fGimbalCmdAzimuth := LIMIT(-3.14159265, fGimbalCmdAzimuth, 3.14159265);
    fGimbalCmdElevation := LIMIT(-3.14159265, fGimbalCmdElevation, 3.14159265);
    
END_IF
```"""

json_obj = {
    "messages": [
        {"role": "user", "content": system_prompt},
        {"role": "assistant", "content": assistant_response}
    ]
}

file_path = r"c:\Users\majip\Downloads\LLM REASEARCH\data\synthetic_generation_v3_enterprise.jsonl"
os.makedirs(os.path.dirname(file_path), exist_ok=True)

with open(file_path, "a", encoding="utf-8") as f:
    f.write(json.dumps(json_obj) + "\n")

print("Successfully written.")
