import json, uuid

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: AS/RS Cold Store System.
Task: Invent a highly complex control scenario for this domain (e.g., mast anti-sway positioning, shuttle regenerative braking, and deep-lane satellite pallet handshakes).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."""

code = """```iec-st
FUNCTION_BLOCK FB_ASRS_ColdStore_Control
TITLE = 'AS/RS Cold Store System Control'
// Highly complex control scenario for mast anti-sway positioning, shuttle regenerative braking, and deep-lane satellite pallet handshakes.

VAR_INPUT
    xEnable : BOOL; // System enable
    xEmergencyStop : BOOL; // E-Stop active (NC)
    xStartSeq : BOOL; // Start automatic sequence
    rTargetPos_X : REAL; // Target X position (Mast)
    rTargetPos_Y : REAL; // Target Y position (Hoist)
    rTargetPos_Z : REAL; // Target Z position (Forks)
    rCurrentPos_X : REAL; // Current X position (Laser)
    rCurrentPos_Y : REAL; // Current Y position (Encoder)
    xShuttleAtHome : BOOL; // Shuttle in home position
    xPalletDetected : BOOL; // Pallet present sensor
    rShuttleVelocity : REAL; // Current shuttle velocity
    rDC_Bus_Voltage : REAL; // DC Bus voltage for regen monitoring
    xSatelliteDocked : BOOL; // Satellite successfully docked
    xSatelliteFault : BOOL; // Satellite communication fault
END_VAR

VAR_OUTPUT
    xReady : BOOL; // System ready for operations
    xMoving : BOOL; // Axis currently in motion
    rCmdSpeed_X : REAL; // Command speed X axis
    rCmdSpeed_Y : REAL; // Command speed Y axis
    rCmdTorque_Shuttle : REAL; // Shuttle torque command
    xEngageRegenBrake : BOOL; // Enable regenerative braking resistor
    xSatellite_Cmd_Deploy : BOOL; // Command satellite to deploy
    xSatellite_Cmd_Retrieve : BOOL; // Command satellite to retrieve
    iState : INT; // State machine state
    xError : BOOL; // Global error flag
    iErrorCode : INT; // Error code ID
END_VAR

VAR
    // Anti-Sway Control Variables
    rSwayAngle : REAL; // Estimated mast sway angle
    rSwayVelocity : REAL; // Estimated mast sway velocity
    rKp_Sway : REAL := 2.5; // Proportional gain for anti-sway
    rKd_Sway : REAL := 0.8; // Derivative gain for anti-sway
    rPendulumLength : REAL := 15.0; // Effective pendulum length in meters
    rGravity : REAL := 9.81; // Gravity constant
    
    // Regenerative Braking Variables
    rBrakingTorqueLimit : REAL := -150.0; // Max regenerative torque (Nm)
    rMax_DC_Voltage : REAL := 750.0; // Max allowed DC bus voltage (V)
    rNominal_DC_Voltage : REAL := 600.0; // Nominal DC bus voltage (V)
    
    // Handshake Variables
    tSatelliteTimeout : TON; // Timeout for satellite operations
    
    // Internal States
    xInitComplete : BOOL := FALSE;
    iSeqStep : INT := 0;
END_VAR

// ==============================================================================
// INIT & SAFETY CHECKS
// ==============================================================================
IF NOT xEmergencyStop THEN
    xReady := FALSE;
    xMoving := FALSE;
    rCmdSpeed_X := 0.0;
    rCmdSpeed_Y := 0.0;
    rCmdTorque_Shuttle := 0.0;
    xEngageRegenBrake := FALSE;
    xSatellite_Cmd_Deploy := FALSE;
    xSatellite_Cmd_Retrieve := FALSE;
    xError := TRUE;
    iErrorCode := 1000; // E-Stop
    iState := 0;
    RETURN;
END_IF;

IF NOT xEnable THEN
    xReady := FALSE;
    rCmdSpeed_X := 0.0;
    rCmdSpeed_Y := 0.0;
    iState := 0;
    RETURN;
END_IF;

xReady := TRUE;
xError := FALSE;
iErrorCode := 0;

// ==============================================================================
// MAIN STATE MACHINE
// ==============================================================================
CASE iState OF
    0: // IDLE
        IF xStartSeq THEN
            iState := 10;
        END_IF;
        
    10: // MAST ANTI-SWAY POSITIONING (X-AXIS)
        // Calculate basic position error
        VAR
            rPosError_X : REAL;
            rBaseCmdSpeed_X : REAL;
            rSwayCorrection : REAL;
        END_VAR
        
        rPosError_X := rTargetPos_X - rCurrentPos_X;
        rBaseCmdSpeed_X := rPosError_X * 1.5; // P-control for position
        
        // Anti-sway pendulum model (simplified)
        // Natural frequency omega = sqrt(g / L)
        // Correction = Kp * SwayAngle + Kd * SwayVelocity
        rSwayCorrection := (rKp_Sway * rSwayAngle) + (rKd_Sway * rSwayVelocity);
        
        // Combine base command with sway correction
        rCmdSpeed_X := rBaseCmdSpeed_X - rSwayCorrection;
        
        // Speed limits
        IF rCmdSpeed_X > 3.0 THEN rCmdSpeed_X := 3.0; END_IF;
        IF rCmdSpeed_X < -3.0 THEN rCmdSpeed_X := -3.0; END_IF;
        
        xMoving := TRUE;
        
        // Check if target reached within tolerance
        IF ABS(rPosError_X) < 0.05 AND ABS(rSwayAngle) < 0.01 THEN
            rCmdSpeed_X := 0.0;
            iState := 20;
        END_IF;

    20: // HOIST POSITIONING (Y-AXIS)
        VAR
            rPosError_Y : REAL;
        END_VAR
        rPosError_Y := rTargetPos_Y - rCurrentPos_Y;
        rCmdSpeed_Y := rPosError_Y * 2.0;
        
        IF ABS(rPosError_Y) < 0.05 THEN
            rCmdSpeed_Y := 0.0;
            iState := 30;
        END_IF;
        
    30: // SHUTTLE REGENERATIVE BRAKING & APPROACH
        // Calculate required torque to decelerate shuttle
        IF rShuttleVelocity > 0.1 THEN
            // Applying negative torque to brake
            rCmdTorque_Shuttle := rBrakingTorqueLimit * (rShuttleVelocity / 2.0);
            
            // Monitor DC Bus for regen overvoltage
            IF rDC_Bus_Voltage > rMax_DC_Voltage THEN
                xEngageRegenBrake := TRUE; // Burn excess energy in resistor
            ELSE
                xEngageRegenBrake := FALSE;
            END_IF;
        ELSE
            rCmdTorque_Shuttle := 0.0;
            xEngageRegenBrake := FALSE;
            IF xShuttleAtHome THEN
                iState := 40;
            END_IF;
        END_IF;
        
    40: // DEEP-LANE SATELLITE HANDSHAKE - DEPLOY
        IF xSatelliteDocked AND NOT xSatelliteFault THEN
            xSatellite_Cmd_Deploy := TRUE;
            tSatelliteTimeout(IN := TRUE, PT := T#15S);
            
            IF xPalletDetected THEN
                xSatellite_Cmd_Deploy := FALSE;
                tSatelliteTimeout(IN := FALSE, PT := T#15S);
                iState := 50;
            ELSIF tSatelliteTimeout.Q THEN
                xError := TRUE;
                iErrorCode := 2001; // Deploy timeout
                iState := 999;
            END_IF;
        ELSE
            xError := TRUE;
            iErrorCode := 2000; // Satellite not ready or fault
            iState := 999;
        END_IF;
        
    50: // DEEP-LANE SATELLITE HANDSHAKE - RETRIEVE
        xSatellite_Cmd_Retrieve := TRUE;
        tSatelliteTimeout(IN := TRUE, PT := T#15S);
        
        IF xSatelliteDocked THEN
            xSatellite_Cmd_Retrieve := FALSE;
            tSatelliteTimeout(IN := FALSE, PT := T#15S);
            xMoving := FALSE;
            iState := 100; // Sequence Complete
        ELSIF tSatelliteTimeout.Q THEN
            xError := TRUE;
            iErrorCode := 2002; // Retrieve timeout
            iState := 999;
        END_IF;
        
    100: // SEQUENCE COMPLETE
        xMoving := FALSE;
        IF NOT xStartSeq THEN
            iState := 0; // Reset state machine
        END_IF;
        
    999: // ERROR STATE
        xMoving := FALSE;
        rCmdSpeed_X := 0.0;
        rCmdSpeed_Y := 0.0;
        rCmdTorque_Shuttle := 0.0;
        xSatellite_Cmd_Deploy := FALSE;
        xSatellite_Cmd_Retrieve := FALSE;
        // Require manual reset via xEnable toggle
        
END_CASE;
END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
    json.dump(record, f)
print("Done")
