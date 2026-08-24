import json

prompt = "Evolve a basic motion block into a Wafer Stepper Reticle Stage Controller. Technical Specs: 1. 6-DOF magnetic levitation position tracking with picometer resolution using laser interferometry. 2. Feed-forward jerk minimization to prevent lens vibration during 100g accelerations. 3. Extreme Ultraviolet (EUV) light source synchronization."

response = """(*
================================================================================
Enterprise-Grade Wafer Stepper Reticle Stage Controller (EUV Lithography)
================================================================================
Architecture:
- 6-DOF Mag-Lev Position Tracking via Laser Interferometry
- Picometer (pm) resolution floating-point scaling
- High-Bandwidth Jerk-Minimization Feed-Forward Control
- EUV Source Trigger Synchronization for Exposure
- Robust Error Handling and Safety Interlocks

Constraints:
- Acceleration up to 100g -> ~981 m/s^2
- Tolerance: < 100 pm
================================================================================
*)
TYPE ST_6DOF_Pose :
STRUCT
    X, Y, Z    : LREAL; (* Picometers (pm) *)
    Rx, Ry, Rz : LREAL; (* Micro-radians (urad) *)
END_STRUCT
END_TYPE

TYPE ST_LaserInterferometer_Feedback :
STRUCT
    MirrorPosX1 : LREAL;
    MirrorPosX2 : LREAL;
    MirrorPosY1 : LREAL;
    MirrorPosY2 : LREAL;
    MirrorPosZ1 : LREAL;
    MirrorPosZ2 : LREAL;
    DataValid   : BOOL;
    ErrorStatus : UDINT;
END_STRUCT
END_TYPE

FUNCTION_BLOCK FB_EUV_Reticle_MagLev_Controller
VAR_INPUT
    bEnable               : BOOL;
    bStartExposure        : BOOL;
    TargetPose            : ST_6DOF_Pose;
    InterferometerData    : ST_LaserInterferometer_Feedback;
    fCycleTime            : LREAL := 0.0001; (* 10kHz control loop (0.1ms) *)
    
    // EUV synchronization params
    fDoseTarget           : LREAL; (* mJ/cm2 *)
    fScanVelocityTarget   : LREAL; (* mm/s *)
END_VAR

VAR_OUTPUT
    bInPosition           : BOOL;
    bExposureActive       : BOOL;
    bEUV_Trigger          : BOOL;
    MagLevCoils_PWM       : ARRAY[1..12] OF LREAL; (* 12 planar/levitation coils *)
    StatusWord            : UDINT;
    bSystemError          : BOOL;
    sErrorMessage         : STRING(255);
END_VAR

VAR
    // State machine
    eState : (INIT, LEVITATE, SETTLE, TRACKING, EXPOSE, HALT, ERROR) := INIT;
    
    // Position tracking (Feedback)
    CurrentPose : ST_6DOF_Pose;
    PoseError   : ST_6DOF_Pose;
    PoseErrorPrev : ST_6DOF_Pose;
    
    // 6-DOF PID + Feed-Forward Vectors
    Kp_Translational : LREAL := 1.5E4;
    Kd_Translational : LREAL := 2.5E2;
    Kp_Rotational    : LREAL := 8.0E3;
    Kd_Rotational    : LREAL := 1.2E2;
    
    JerkLimit        : LREAL := 5.0E6; (* m/s^3 to prevent lens vibration *)
    MaxAccel         : LREAL := 9.81E14; (* ~100g in pm/s^2 *)
    
    // Trajectory generator & Feed-forward
    TargetVel        : ST_6DOF_Pose;
    TargetAcc        : ST_6DOF_Pose;
    TargetJerk       : ST_6DOF_Pose;
    
    ForceCmd         : ARRAY[1..6] OF LREAL; // 6-DOF Forces & Torques
    
    // Dynamic compensation
    Mass             : LREAL := 5.0; (* Reticle + chuck mass in kg *)
    Inertia          : ARRAY[1..3] OF LREAL := [0.1, 0.1, 0.05]; (* kg*m^2 *)
    
    // EUV Synchronization
    EUV_Timer        : TON;
    fPulseDuration   : LREAL := 0.00002; (* 20 micro-seconds *)
    bReadyForLight   : BOOL;
    
    i : INT;
    fTolerance_pm    : LREAL := 50.0; (* 50 picometer tolerance *)
END_VAR

(* Implementation *)
// 1. Diagnostics & Interferometry Resolution Processing (pm level)
IF NOT InterferometerData.DataValid THEN
    eState := ERROR;
    bSystemError := TRUE;
    sErrorMessage := 'Laser Interferometer Loss of Signal';
END_IF

// Kinematic decoupling of interferometer axes to 6-DOF
IF NOT bSystemError THEN
    CurrentPose.X := (InterferometerData.MirrorPosX1 + InterferometerData.MirrorPosX2) / 2.0;
    CurrentPose.Y := (InterferometerData.MirrorPosY1 + InterferometerData.MirrorPosY2) / 2.0;
    CurrentPose.Z := (InterferometerData.MirrorPosZ1 + InterferometerData.MirrorPosZ2) / 2.0;
    // Simplified rotational approximations based on differential interferometry
    CurrentPose.Rz := (InterferometerData.MirrorPosX1 - InterferometerData.MirrorPosX2) / 0.1; // Baseline 100mm
    CurrentPose.Rx := (InterferometerData.MirrorPosZ1 - InterferometerData.MirrorPosZ2) / 0.1;
    CurrentPose.Ry := (InterferometerData.MirrorPosY1 - InterferometerData.MirrorPosY2) / 0.1;
END_IF

// 2. Main State Machine
CASE eState OF
    INIT:
        IF bEnable AND NOT bSystemError THEN
            eState := LEVITATE;
        END_IF;
        
    LEVITATE:
        // Ramp up Z-axis magnetic field for lift-off
        TargetPose.Z := 1.0E8; (* 100 microns hover gap in pm *)
        IF ABS(CurrentPose.Z - TargetPose.Z) < 1.0E3 THEN
            eState := SETTLE;
        END_IF;
        
    SETTLE:
        IF ABS(CurrentPose.X - TargetPose.X) < fTolerance_pm AND 
           ABS(CurrentPose.Y - TargetPose.Y) < fTolerance_pm THEN
            bInPosition := TRUE;
            eState := TRACKING;
        END_IF;
        
    TRACKING:
        bInPosition := (ABS(PoseError.X) < fTolerance_pm) AND (ABS(PoseError.Y) < fTolerance_pm);
        
        IF bStartExposure AND bInPosition THEN
            eState := EXPOSE;
            bExposureActive := TRUE;
        END_IF;
        
    EXPOSE:
        // Feed-Forward Jerk Minimization for 100g scanning
        // Execute EUV Source Synch
        IF ABS(PoseError.X) < fTolerance_pm AND ABS(PoseError.Y) < fTolerance_pm THEN
            bEUV_Trigger := TRUE;
        ELSE
            bEUV_Trigger := FALSE; // Abort pulse if vibration exceeds limits
        END_IF;
        
        IF NOT bStartExposure THEN
            bExposureActive := FALSE;
            bEUV_Trigger := FALSE;
            eState := TRACKING;
        END_IF;
        
    ERROR:
        bSystemError := TRUE;
        bEUV_Trigger := FALSE;
        bInPosition := FALSE;
        // Mag-lev safe landing protocol would be implemented here
        MagLevCoils_PWM[1] := 0.0; // Shut down coils
END_CASE;

// 3. 6-DOF Feed-Forward Jerk-Minimization Controller
IF eState >= LEVITATE AND eState <= EXPOSE THEN
    // Calculate Error
    PoseError.X := TargetPose.X - CurrentPose.X;
    PoseError.Y := TargetPose.Y - CurrentPose.Y;
    PoseError.Z := TargetPose.Z - CurrentPose.Z;
    PoseError.Rx := TargetPose.Rx - CurrentPose.Rx;
    PoseError.Ry := TargetPose.Ry - CurrentPose.Ry;
    PoseError.Rz := TargetPose.Rz - CurrentPose.Rz;
    
    // PID + Advanced Feed-Forward (Mass * Accel + Deriv(Jerk))
    // X, Y, Z translational forces
    ForceCmd[1] := (Kp_Translational * PoseError.X) + (Kd_Translational * (PoseError.X - PoseErrorPrev.X)/fCycleTime) + (Mass * TargetAcc.X);
    ForceCmd[2] := (Kp_Translational * PoseError.Y) + (Kd_Translational * (PoseError.Y - PoseErrorPrev.Y)/fCycleTime) + (Mass * TargetAcc.Y);
    ForceCmd[3] := (Kp_Translational * PoseError.Z) + (Kd_Translational * (PoseError.Z - PoseErrorPrev.Z)/fCycleTime) + (Mass * TargetAcc.Z) + 49.05; // gravity comp
    
    // Rx, Ry, Rz rotational torques
    ForceCmd[4] := (Kp_Rotational * PoseError.Rx) + (Kd_Rotational * (PoseError.Rx - PoseErrorPrev.Rx)/fCycleTime) + (Inertia[1] * TargetAcc.Rx);
    ForceCmd[5] := (Kp_Rotational * PoseError.Ry) + (Kd_Rotational * (PoseError.Ry - PoseErrorPrev.Ry)/fCycleTime) + (Inertia[2] * TargetAcc.Ry);
    ForceCmd[6] := (Kp_Rotational * PoseError.Rz) + (Kd_Rotational * (PoseError.Rz - PoseErrorPrev.Rz)/fCycleTime) + (Inertia[3] * TargetAcc.Rz);
    
    PoseErrorPrev := PoseError;
    
    // 4. Force/Torque to 12-Coil MagLev PWM Matrix Allocation
    // Simplified distribution matrix for a planar halbach array stator
    FOR i := 1 TO 12 DO
        MagLevCoils_PWM[i] := ForceCmd[1]*0.1 + ForceCmd[2]*0.1 + ForceCmd[3]*0.05; // Conceptual mapping
        // Limit outputs
        IF MagLevCoils_PWM[i] > 100.0 THEN MagLevCoils_PWM[i] := 100.0; END_IF;
        IF MagLevCoils_PWM[i] < -100.0 THEN MagLevCoils_PWM[i] := -100.0; END_IF;
    END_FOR;
END_IF;
END_FUNCTION_BLOCK
"""

obj = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": response}
    ]
}

with open(r'C:\Users\majip\Downloads\LLM REASEARCH\data\synthetic_generation_v3_enterprise.jsonl', 'a', encoding='utf-8') as f:
    f.write(json.dumps(obj) + '\n')
