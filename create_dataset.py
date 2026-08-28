import os
import json
import uuid

# IEC-ST Code
iec_code = r'''```iec-st
FUNCTION_BLOCK FB_STSCrane_AntiSway
TITLE = 'STS Gantry Crane Anti-Sway & Pendulum Mitigation'
// ---------------------------------------------------------------------------
// Description:
// This function block implements a multi-variable non-linear control strategy
// for suppressing the payload sway (pendulum effect) of a Ship-To-Shore (STS) 
// gantry crane. It accounts for trolley dynamics, hoist rope length variations,
// and external wind disturbances.
// ---------------------------------------------------------------------------
VAR_INPUT
    rTrolleyPos_m       : REAL; // Current trolley position [m]
    rTrolleyVel_mps     : REAL; // Current trolley velocity [m/s]
    rHoistLength_m      : REAL; // Current hoist rope length (L) [m]
    rHoistVel_mps       : REAL; // Current hoist velocity (dL/dt) [m/s]
    rSwayAngle_rad      : REAL; // Measured sway angle (theta) [rad]
    rSwayOmega_radps    : REAL; // Measured sway angular velocity [rad/s]
    rWindSpeed_mps      : REAL; // Measured wind speed [m/s]
    rTargetPos_m        : REAL; // Target trolley position [m]
    bEnableControl      : BOOL; // Enable closed-loop anti-sway control
    bEmergencyStop      : BOOL; // Emergency stop active
END_VAR

VAR_OUTPUT
    rTrolleyCmd_mps     : REAL; // Commanded trolley velocity [m/s]
    rTrolleyAccelCmd    : REAL; // Commanded trolley acceleration [m/s^2]
    bSwayWarning        : BOOL; // Sway angle exceeds safety threshold
    bLimitReached       : BOOL; // Actuator limits reached
    bError              : BOOL; // System error
END_VAR

VAR
    // Controller Parameters
    rKp_Pos             : REAL := 2.5;   // Position proportional gain
    rKd_Pos             : REAL := 1.2;   // Position derivative gain
    rKp_Sway            : REAL := -15.0; // Sway proportional gain (Negative feedback)
    rKd_Sway            : REAL := -5.5;  // Sway derivative gain
    rMaxAccel_mps2      : REAL := 0.8;   // Maximum allowed trolley acceleration
    rMaxVel_mps         : REAL := 3.5;   // Maximum allowed trolley velocity
    
    // Physical Constants
    rGravity_mps2       : REAL := 9.81;  // Acceleration due to gravity
    rMaxSafeSway_rad    : REAL := 0.15;  // Safety limit for sway (~8.5 deg)
    
    // Internal State
    rPosError           : REAL;
    rPosControl         : REAL;
    rSwayControl        : REAL;
    rTotalAccelReq      : REAL;
    rWindDisturbance    : REAL;
    
    // Cycle Time (Assuming 10ms task cycle)
    rDeltaT_s           : REAL := 0.01;
END_VAR

// ===========================================================================
// Implementation
// ===========================================================================

// 1. Safety and Enable Checks
IF bEmergencyStop THEN
    rTrolleyCmd_mps := 0.0;
    rTrolleyAccelCmd := 0.0;
    bSwayWarning := FALSE;
    bError := TRUE;
    RETURN;
END_IF;

bError := FALSE;

IF NOT bEnableControl THEN
    // Open loop / Manual mode - output zero commands
    rTrolleyCmd_mps := 0.0;
    rTrolleyAccelCmd := 0.0;
    RETURN;
END_IF;

// 2. Limit Checks & Warnings
IF ABS(rSwayAngle_rad) > rMaxSafeSway_rad THEN
    bSwayWarning := TRUE;
ELSE
    bSwayWarning := FALSE;
END_IF;

// Prevent division by zero for hoist length
IF rHoistLength_m < 0.1 THEN
    rHoistLength_m := 0.1; // Minimum hoist length clamp
END_IF;

// 3. Position Control Loop (PD Controller)
// Calculate trolley position error
rPosError := rTargetPos_m - rTrolleyPos_m;

// Commanded acceleration for position tracking
rPosControl := (rKp_Pos * rPosError) - (rKd_Pos * rTrolleyVel_mps);

// 4. Sway Mitigation Loop (State Feedback)
// The sway dynamics are approximated by: L*Theta'' + 2*L'*Theta' + g*Theta = - X'' + WindDisturbance
// We compensate for sway by modifying the trolley acceleration command.
// We apply state feedback on Theta and Theta'.

// Wind Disturbance Estimation (simplified aerodynamic drag model)
// Force proportional to square of wind speed, normalized to acceleration impact
rWindDisturbance := 0.005 * rWindSpeed_mps * rWindSpeed_mps;
IF rWindSpeed_mps < 0.0 THEN
    rWindDisturbance := -rWindDisturbance;
END_IF;

// Sway control effort
rSwayControl := (rKp_Sway * rSwayAngle_rad) + (rKd_Sway * rSwayOmega_radps);

// Coupling term for hoisting velocity (Coriolis effect damping)
// 2 * dL/dt * dTheta/dt / L
rSwayControl := rSwayControl - (2.0 * rHoistVel_mps * rSwayOmega_radps / rHoistLength_m);

// 5. Aggregate Acceleration Command
// Combine position tracking, sway suppression, and wind rejection
rTotalAccelReq := rPosControl + rSwayControl - rWindDisturbance;

// 6. Actuator Saturation and Rate Limiting
bLimitReached := FALSE;

// Clamp acceleration
IF rTotalAccelReq > rMaxAccel_mps2 THEN
    rTotalAccelReq := rMaxAccel_mps2;
    bLimitReached := TRUE;
ELSIF rTotalAccelReq < -rMaxAccel_mps2 THEN
    rTotalAccelReq := -rMaxAccel_mps2;
    bLimitReached := TRUE;
END_IF;

// Integrate acceleration to get velocity command
rTrolleyCmd_mps := rTrolleyCmd_mps + (rTotalAccelReq * rDeltaT_s);

// Clamp velocity
IF rTrolleyCmd_mps > rMaxVel_mps THEN
    rTrolleyCmd_mps := rMaxVel_mps;
    bLimitReached := TRUE;
ELSIF rTrolleyCmd_mps < -rMaxVel_mps THEN
    rTrolleyCmd_mps := -rMaxVel_mps;
    bLimitReached := TRUE;
END_IF;

// Output the final acceleration command applied (for motor drive feedforward)
rTrolleyAccelCmd := rTotalAccelReq;

END_FUNCTION_BLOCK
```'''

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Automated Container Port.
Task: Invent a highly complex control scenario for this domain (e.g., ship-to-shore gantry crane anti-sway pendulum mitigation).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."""

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": iec_code}
    ]
}

out_dir = r"c:\Users\majip\Downloads\LLM REASEARCH\data\swarm_raw"
os.makedirs(out_dir, exist_ok=True)
filename = os.path.join(out_dir, f"agent_{uuid.uuid4().hex[:8]}.json")

with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)

print(f"Successfully saved to {filename}")
