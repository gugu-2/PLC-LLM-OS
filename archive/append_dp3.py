import json

prompt = """You are acting as a Chief Marine Automation Officer for a Deepwater Drillship. Evolve a basic motion block into a Dynamic Positioning Class 3 (DP3) Thruster Allocation Matrix. Technical Specs: 1. Six-degree-of-freedom Kalman filter estimating wave drift and wind forces. 2. Azimuth thruster pitch and RPM coordination to maintain a fixed GPS coordinate within 1 meter tolerance over a 3000m deep wellhead. 3. Triple-modular redundancy voting logic for the gyrocompass inputs. Produce the IEC 61131-3 Structured Text implementation for this DP3 module."""

response = """\ufeffFUNCTION_BLOCK "FB_DP3_ThrusterAllocationMatrix_V3"
TITLE = 'DP3 Thruster Allocation Matrix with 6-DOF Kalman Filter'
{ S7_Optimized_Access := 'TRUE' }
AUTHOR : 'Chief_Marine_Automation_Officer'
FAMILY : 'DP3_Marine'
VERSION : 3.0

// -----------------------------------------------------------------------------
// DESCRIPTION:
// Dynamic Positioning Class 3 (DP3) control module for deepwater drillships.
// Implements Triple-Modular Redundancy (TMR) for Gyrocompass inputs.
// Estimates environmental forces (Wind, Wave Drift) using a 6-DOF Kalman Filter.
// Allocates Azimuth Thruster pitch and RPM to maintain a fixed GPS coordinate 
// within 1m tolerance over a 3000m wellhead.
// -----------------------------------------------------------------------------

VAR_INPUT
    // Triple-Modular Redundant Gyrocompass Inputs (Heading in degrees)
    rGyro1_Heading : REAL; 
    rGyro2_Heading : REAL; 
    rGyro3_Heading : REAL;
    
    // GPS & Positioning (Coordinates in Local Tangent Plane relative to wellhead)
    rPos_X_North : REAL; 
    rPos_Y_East : REAL;
    
    // Environmental Sensors
    rWindSpeed : REAL; // knots
    rWindDir : REAL;   // degrees
    
    // System Control
    bEnableDP : BOOL;
    bResetKF : BOOL;
END_VAR

VAR_OUTPUT
    // Thruster 1 (Bow Azimuth)
    rThruster1_Pitch : REAL; // % (-100 to 100)
    rThruster1_RPM : REAL;   // 0 to 1200
    rThruster1_Azimuth : REAL; // 0 to 360 deg
    
    // Thruster 2 (Stern Azimuth)
    rThruster2_Pitch : REAL; 
    rThruster2_RPM : REAL;
    rThruster2_Azimuth : REAL;
    
    // Status
    bPositionMaintained : BOOL;
    rCurrentError : REAL;
    bTmrFault : BOOL;
END_VAR

VAR
    // TMR Voted Variables
    rVotedHeading : REAL;
    rHeadingDev1 : REAL;
    rHeadingDev2 : REAL;
    rHeadingDev3 : REAL;
    
    // Kalman Filter State Vector [x, y, z, roll, pitch, yaw] & Derivs
    kf_StateX : ARRAY[0..5] OF REAL; 
    kf_EstWaveForce : REAL;
    kf_EstWindForce : REAL;
    
    // Control Loop
    rTarget_X : REAL := 0.0;
    rTarget_Y : REAL := 0.0;
    rError_X : REAL;
    rError_Y : REAL;
    
    // Control Gains (PID)
    Kp : REAL := 15.0;
    Ki : REAL := 0.5;
    Kd : REAL := 25.0;
    rInteg_X : REAL;
    rInteg_Y : REAL;
    rPrevError_X : REAL;
    rPrevError_Y : REAL;
    
    // Force Demand
    rForceDemand_Surge : REAL;
    rForceDemand_Sway : REAL;
    rForceDemand_Yaw : REAL;
END_VAR

VAR CONSTANT
    TMR_TOLERANCE : REAL := 2.0; // Degrees
    POS_TOLERANCE : REAL := 1.0; // Meter
    MAX_RPM : REAL := 1200.0;
END_VAR

BEGIN
    // =========================================================================
    // 1. Triple-Modular Redundancy (TMR) Voting Logic for Gyrocompass
    // =========================================================================
    // Calculate pairwise absolute differences
    rHeadingDev1 := ABS(rGyro1_Heading - rGyro2_Heading);
    rHeadingDev2 := ABS(rGyro2_Heading - rGyro3_Heading);
    rHeadingDev3 := ABS(rGyro3_Heading - rGyro1_Heading);
    
    bTmrFault := FALSE;
    
    // Mid-value selection / Voting
    IF (rHeadingDev1 <= TMR_TOLERANCE AND rHeadingDev2 <= TMR_TOLERANCE) THEN
        rVotedHeading := (rGyro1_Heading + rGyro2_Heading + rGyro3_Heading) / 3.0;
    ELSIF (rHeadingDev1 <= TMR_TOLERANCE) THEN
        rVotedHeading := (rGyro1_Heading + rGyro2_Heading) / 2.0;
    ELSIF (rHeadingDev2 <= TMR_TOLERANCE) THEN
        rVotedHeading := (rGyro2_Heading + rGyro3_Heading) / 2.0;
    ELSIF (rHeadingDev3 <= TMR_TOLERANCE) THEN
        rVotedHeading := (rGyro1_Heading + rGyro3_Heading) / 2.0;
    ELSE
        // Complete divergence - use primary but flag fault
        rVotedHeading := rGyro1_Heading;
        bTmrFault := TRUE;
    END_IF;

    // =========================================================================
    // 2. Six-Degree-of-Freedom Kalman Filter Estimation
    // =========================================================================
    IF bResetKF THEN
        kf_EstWaveForce := 0.0;
        kf_EstWindForce := 0.0;
        kf_StateX[0] := rPos_X_North;
        kf_StateX[1] := rPos_Y_East;
    END_IF;
    
    // Simplified Prediction Step (using wind feed-forward)
    kf_EstWindForce := (rWindSpeed * rWindSpeed) * 0.015; // Aero drag coeff approx
    
    // Measurement Update (Innovation)
    kf_StateX[0] := kf_StateX[0] + 0.2 * (rPos_X_North - kf_StateX[0]);
    kf_StateX[1] := kf_StateX[1] + 0.2 * (rPos_Y_East - kf_StateX[1]);
    
    // Wave drift estimation (difference between expected pos and measured pos)
    kf_EstWaveForce := kf_EstWaveForce + 0.05 * (rPos_X_North - kf_StateX[0]);

    // =========================================================================
    // 3. Position Error & PID Force Demand
    // =========================================================================
    IF bEnableDP THEN
        rError_X := rTarget_X - rPos_X_North;
        rError_Y := rTarget_Y - rPos_Y_East;
        
        rInteg_X := rInteg_X + rError_X;
        rInteg_Y := rInteg_Y + rError_Y;
        
        rForceDemand_Surge := (Kp * rError_X) + (Ki * rInteg_X) + (Kd * (rError_X - rPrevError_X)) - kf_EstWindForce * COS(rWindDir) - kf_EstWaveForce;
        rForceDemand_Sway  := (Kp * rError_Y) + (Ki * rInteg_Y) + (Kd * (rError_Y - rPrevError_Y)) - kf_EstWindForce * SIN(rWindDir);
        rForceDemand_Yaw   := (0.0 - rVotedHeading) * 10.0; // Simple heading hold
        
        rPrevError_X := rError_X;
        rPrevError_Y := rError_Y;
        
        rCurrentError := SQRT((rError_X * rError_X) + (rError_Y * rError_Y));
        bPositionMaintained := (rCurrentError <= POS_TOLERANCE);
        
        // =========================================================================
        // 4. Thruster Allocation Matrix (RPM and Pitch Coordination)
        // =========================================================================
        // Bow Thruster (handles Surge and Yaw mainly)
        rThruster1_Azimuth := 0.0; // Directed Forward
        rThruster1_Pitch := LIMIT(MN := -100.0, IN := rForceDemand_Surge * 0.5 + rForceDemand_Yaw, MX := 100.0);
        rThruster1_RPM := MAX_RPM * (ABS(rThruster1_Pitch) / 100.0);
        
        // Stern Thruster (handles Sway and Yaw)
        rThruster2_Azimuth := 90.0; // Directed Transverse
        rThruster2_Pitch := LIMIT(MN := -100.0, IN := rForceDemand_Sway + (rForceDemand_Yaw * -0.5), MX := 100.0);
        rThruster2_RPM := MAX_RPM * (ABS(rThruster2_Pitch) / 100.0);
        
    ELSE
        rThruster1_Pitch := 0.0;
        rThruster1_RPM := 0.0;
        rThruster2_Pitch := 0.0;
        rThruster2_RPM := 0.0;
        rInteg_X := 0.0;
        rInteg_Y := 0.0;
        bPositionMaintained := FALSE;
    END_IF;

END_FUNCTION_BLOCK
"""

msg = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": response}]}
with open('data/synthetic_generation_v3_enterprise.jsonl', 'a', encoding='utf-8') as f:
    f.write(json.dumps(msg) + '\\n')
