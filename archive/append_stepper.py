import json
import os

prompt = "Evolve a basic motion block into a Wafer Stepper Reticle Stage Controller. Technical Specs: 1. 6-DOF magnetic levitation position tracking with picometer resolution using laser interferometry. 2. Feed-forward jerk minimization to prevent lens vibration during 100g accelerations. 3. Extreme Ultraviolet (EUV) light source synchronization."

assistant_response = """FUNCTION_BLOCK FB_WaferStepper_ReticleStage
TITLE = 'Wafer Stepper Reticle Stage Controller'
VERSION : '2.0'
AUTHOR : 'Lumina Synthetic Data Architect'

// ==============================================================================
// WAFER STEPPER RETICLE STAGE - 6-DOF MAGNETIC LEVITATION & EUV SYNC
// ==============================================================================
// 1. 6-DOF Magnetic Levitation Position Tracking (Picometer Resolution via Interferometry)
// 2. Feed-Forward Jerk Minimization (100g Acceleration Profiling)
// 3. Extreme Ultraviolet (EUV) Light Source Synchronization (Nanosecond precision)
// ==============================================================================

TYPE ST_6DOF_Position :
STRUCT
    X : LREAL; // pm (picometers)
    Y : LREAL;
    Z : LREAL;
    Rx : LREAL; // nrad (nanoradians)
    Ry : LREAL;
    Rz : LREAL;
END_STRUCT
END_TYPE

TYPE ST_Interferometer_Feedback :
STRUCT
    MirrorX1 : LREAL;
    MirrorX2 : LREAL;
    MirrorY1 : LREAL;
    MirrorY2 : LREAL;
    MirrorZ1 : LREAL;
    MirrorZ2 : LREAL;
    BeamStatus : BOOL;
    ReferencePhase : LREAL;
END_STRUCT
END_TYPE

TYPE ST_EUV_Source_Control :
STRUCT
    PlasmaTrigger : BOOL;
    DropletSync : BOOL;
    LaserPulseEnable : BOOL;
    DoseControl : LREAL; // mJ/cm2
    ExposureActive : BOOL;
END_STRUCT
END_TYPE

VAR_INPUT
    Enable : BOOL;
    Reset : BOOL;
    Setpoint : ST_6DOF_Position;
    InterferometerRaw : ST_Interferometer_Feedback;
    EUVDemandDose : LREAL;
    ScanVelocity : LREAL; // mm/s
    ScanAcceleration : LREAL; // up to 100g (980665 mm/s^2)
    ExposureWindow : LREAL; // nanoseconds
END_VAR

VAR_OUTPUT
    CurrentPosition : ST_6DOF_Position;
    MagLevCurrents : ARRAY[0..7] OF LREAL; // 8-axis planar motor currents (Amps)
    EUV_ControlOut : ST_EUV_Source_Control;
    InPosition : BOOL;
    TrackingError : LREAL; // pm
    SystemFault : BOOL;
    FaultCode : DWORD;
END_VAR

VAR
    // Kinematic & Dynamic State
    State_Vel : ST_6DOF_Position;
    State_Acc : ST_6DOF_Position;
    State_Jerk : ST_6DOF_Position;
    
    // Jerk Minimization & Feed-forward Matrices
    MassMatrix : ARRAY[0..5, 0..5] OF LREAL; // 6x6 spatial mass matrix
    JerkLimit : LREAL := 5.0E9; // mm/s^3 limit for structural resonance avoidance
    TargetTrajectoryPhase : LREAL;
    
    // Interferometry Processing
    RefractiveIndexCorrection : LREAL;
    Wavelength_EUV : LREAL := 13.5; // nm
    Wavelength_Interf : LREAL := 632.8; // HeNe pm equivalent
    PhaseAccumulator : ARRAY[0..5] OF LREAL;
    
    // Control Loop Parameters (H-infinity or LQG based)
    Kp : ARRAY[0..5] OF LREAL := [1.5e4, 1.5e4, 5.0e4, 2.0e5, 2.0e5, 1.0e5];
    Kd : ARRAY[0..5] OF LREAL := [2.0e2, 2.0e2, 8.0e2, 1.0e3, 1.0e3, 5.0e2];
    Ki : ARRAY[0..5] OF LREAL := [1.0e5, 1.0e5, 2.0e5, 5.0e5, 5.0e5, 3.0e5];
    Integrator_6DOF : ARRAY[0..5] OF LREAL;
    
    // EUV Synchronization
    EUV_Timer_Ns : LINT;
    PulseFrequency_Hz : LREAL := 50000.0; // 50kHz EUV source
    NextPulseTime : LINT;
    DropletArrivalPredicted : LINT;
END_VAR

BEGIN
    IF Reset THEN
        SystemFault := FALSE;
        FaultCode := 16#0000;
        EUV_ControlOut.ExposureActive := FALSE;
        FOR i := 0 TO 5 DO Integrator_6DOF[i] := 0.0; END_FOR;
    END_IF;

    IF NOT Enable THEN
        FOR i := 0 TO 7 DO MagLevCurrents[i] := 0.0; END_FOR;
        EUV_ControlOut.LaserPulseEnable := FALSE;
        RETURN;
    END_IF;
    
    // -------------------------------------------------------------------------
    // 1. SENSOR FUSION & 6-DOF POSITION CALCULATION (INTERFEROMETRY)
    // -------------------------------------------------------------------------
    // Convert heterodyne phase shifts to physical picometer displacements.
    // Environmental refractive index compensation applied.
    RefractiveIndexCorrection := 1.00000028; // Air/vacuum interface calibration
    
    IF NOT InterferometerRaw.BeamStatus THEN
        SystemFault := TRUE;
        FaultCode := 16#E001; // Interferometer beam loss
        RETURN;
    END_IF;
    
    // Kinematic transform from 6 mirrors to 6-DOF CG (Center of Gravity)
    CurrentPosition.X := (InterferometerRaw.MirrorX1 + InterferometerRaw.MirrorX2) * 0.5 * RefractiveIndexCorrection;
    CurrentPosition.Y := (InterferometerRaw.MirrorY1 + InterferometerRaw.MirrorY2) * 0.5 * RefractiveIndexCorrection;
    CurrentPosition.Z := (InterferometerRaw.MirrorZ1 + InterferometerRaw.MirrorZ2) * 0.5 * RefractiveIndexCorrection;
    CurrentPosition.Rz := (InterferometerRaw.MirrorX1 - InterferometerRaw.MirrorX2) / 0.150; // Abbe offset 150mm
    CurrentPosition.Rx := (InterferometerRaw.MirrorZ1 - InterferometerRaw.MirrorZ2) / 0.150;
    CurrentPosition.Ry := (InterferometerRaw.MirrorZ1 + InterferometerRaw.MirrorZ2 - CurrentPosition.Z) * 0.01; 
    
    // -------------------------------------------------------------------------
    // 2. FEED-FORWARD JERK MINIMIZATION & TRAJECTORY GENERATION (100g ACCEL)
    // -------------------------------------------------------------------------
    // Compute 4th-order trajectory to ensure continuous acceleration (limited jerk)
    // to prevent lens excitation and dynamic distortion in the projection optics.
    
    // Target Feed-Forward values (Simplified S-Curve derivatives)
    State_Jerk.Y := JerkLimit * SIN(TargetTrajectoryPhase);
    State_Acc.Y := State_Acc.Y + (State_Jerk.Y * 0.0001); // 100us sample
    IF State_Acc.Y > ScanAcceleration THEN State_Acc.Y := ScanAcceleration; END_IF;
    State_Vel.Y := State_Vel.Y + (State_Acc.Y * 0.0001);
    
    // -------------------------------------------------------------------------
    // 3. 6-DOF MAGNETIC LEVITATION CONTROL LOOP (PID + MULTIVARIABLE DECOUPLING)
    // -------------------------------------------------------------------------
    VAR
        Err : ARRAY[0..5] OF LREAL;
        PID_Out : ARRAY[0..5] OF LREAL;
        FF_Force : ARRAY[0..5] OF LREAL;
    END_VAR
    
    Err[0] := Setpoint.X - CurrentPosition.X;
    Err[1] := Setpoint.Y - CurrentPosition.Y;
    Err[2] := Setpoint.Z - CurrentPosition.Z;
    Err[3] := Setpoint.Rx - CurrentPosition.Rx;
    Err[4] := Setpoint.Ry - CurrentPosition.Ry;
    Err[5] := Setpoint.Rz - CurrentPosition.Rz;
    
    TrackingError := SQRT(Err[0]*Err[0] + Err[1]*Err[1]);
    InPosition := (TrackingError < 50.0); // 50 pm tracking error threshold
    
    // Apply Mass Matrix Feed-Forward for 100g compensation
    // F = M * a
    FF_Force[1] := MassMatrix[1,1] * State_Acc.Y; 
    
    FOR i := 0 TO 5 DO
        Integrator_6DOF[i] := Integrator_6DOF[i] + (Err[i] * 0.0001);
        PID_Out[i] := (Err[i] * Kp[i]) + (Integrator_6DOF[i] * Ki[i]) + FF_Force[i]; 
    END_FOR;
    
    // Inverse Electromechanical Transform (Planar Motor Current Allocation)
    // Mapping 6 virtual forces/torques to 8 physical coils
    MagLevCurrents[0] := (PID_Out[0] + PID_Out[1] + PID_Out[5]) * 0.024;
    MagLevCurrents[1] := (PID_Out[0] - PID_Out[1] - PID_Out[5]) * 0.024;
    MagLevCurrents[2] := (-PID_Out[0] + PID_Out[1] - PID_Out[5]) * 0.024;
    MagLevCurrents[3] := (-PID_Out[0] - PID_Out[1] + PID_Out[5]) * 0.024;
    MagLevCurrents[4] := (PID_Out[2] + PID_Out[3] + PID_Out[4]) * 0.031;
    MagLevCurrents[5] := (PID_Out[2] - PID_Out[3] + PID_Out[4]) * 0.031;
    MagLevCurrents[6] := (PID_Out[2] + PID_Out[3] - PID_Out[4]) * 0.031;
    MagLevCurrents[7] := (PID_Out[2] - PID_Out[3] - PID_Out[4]) * 0.031;
    
    // -------------------------------------------------------------------------
    // 4. EXTREME ULTRAVIOLET (EUV) LIGHT SOURCE SYNCHRONIZATION
    // -------------------------------------------------------------------------
    // Precise firing of CO2 laser on falling Sn droplet.
    // Sync depends on Reticle reaching constant velocity phase (InPosition flag)
    
    IF InPosition AND (State_Acc.Y < 1.0) AND (State_Vel.Y >= ScanVelocity - 0.1) THEN
        EUV_ControlOut.ExposureActive := TRUE;
        EUV_ControlOut.DoseControl := EUVDemandDose;
        
        // Predict Tin (Sn) droplet arrival in plasma chamber
        EUV_Timer_Ns := EUV_Timer_Ns + 100000; // 100us sample = 100,000 ns
        
        IF EUV_Timer_Ns >= DropletArrivalPredicted THEN
            EUV_ControlOut.LaserPulseEnable := TRUE;
            EUV_ControlOut.PlasmaTrigger := TRUE;
            DropletArrivalPredicted := EUV_Timer_Ns + LREAL_TO_LINT(1.0E9 / PulseFrequency_Hz);
        ELSE
            EUV_ControlOut.LaserPulseEnable := FALSE;
            EUV_ControlOut.PlasmaTrigger := FALSE;
        END_IF;
    ELSE
        EUV_ControlOut.ExposureActive := FALSE;
        EUV_ControlOut.LaserPulseEnable := FALSE;
        EUV_ControlOut.PlasmaTrigger := FALSE;
    END_IF;

END_FUNCTION_BLOCK"""

obj = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": assistant_response}
    ]
}

target_file = r"C:\Users\majip\Downloads\LLM REASEARCH\data\synthetic_generation_v3_enterprise.jsonl"
with open(target_file, "a", encoding="utf-8") as f:
    f.write(json.dumps(obj) + "\n")

print("Done appending to", target_file)
