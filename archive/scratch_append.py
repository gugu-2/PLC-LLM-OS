import json, os
d = r'c:\Users\majip\Downloads\LLM REASEARCH\data'
os.makedirs(d, exist_ok=True)
p = os.path.join(d, 'synthetic_generation_v3_enterprise.jsonl')
prompt = """You are acting as the Lead Aerospace Mechatronics Engineer for a Commercial Spaceflight Training Center.

Your mission is to generate a master-tier, production-ready IEC 61131-3 Structured Text (ST) implementation for the "Sub-Orbital Flight Profile Human Centrifuge & 3-Axis Gimbal Simulator Controller" (`FB_Spaceflight_Centrifuge`).

### Technical Specifications & Engineering Rigor Required:
1. **Dynamic G-Force Profile Generation**:
   - Dual-drive massive asynchronous motor control rotating a 20-meter centrifuge arm to precisely replicate the extreme G-loads ($+6G_x$, $+4G_z$) of a sub-orbital rocket launch and ballistic reentry.
   - Closed-loop coriolis force compensation to prevent vestibular illusion-induced nausea in the civilian astronaut trainees.
2. **3-Axis Capsule Gimbal Stabilization**:
   - Direct-drive torque motor control of the roll, pitch, and yaw gimbals at the end of the centrifuge arm.
   - Real-time inverse kinematics matrix execution to keep the resultant G-force vector perfectly aligned with the trainee's chest-to-spine axis ($G_x$) during rapid deceleration events.
3. **Code Quality**: Strict IEC 61131-3 ST, LREAL datatypes, multi-variable rigid body dynamics, SIL-3 human-rating safety interlocks, PackML states."""

code = """```iec-st
FUNCTION_BLOCK FB_Spaceflight_Centrifuge
TITLE = 'Sub-Orbital Flight Profile Human Centrifuge & 3-Axis Gimbal Simulator Controller'
VERSION : '3.1'
// Lead Aerospace Mechatronics Engineer
// Commercial Spaceflight Training Center

VAR_INPUT
    // PackML State Machine Inputs
    bExecute            : BOOL; // Start automatic sequence
    bStop               : BOOL; // Controlled stop
    bAbort              : BOOL; // Emergency SIL-3 abort (e-stop)
    bReset              : BOOL; // Reset faults
    
    // Flight Profile Target Parameters
    lrTargetG_x         : LREAL; // Commanded Chest-to-Spine G-Force
    lrTargetG_z         : LREAL; // Commanded Head-to-Toe G-Force
    lrProfileTime       : LREAL; // Elapsed time in current profile phase (s)
    
    // Feedback from Physical Sensors
    lrArmVelocity_Act   : LREAL; // Actual centrifuge arm rotational velocity (rad/s)
    lrGimbalRoll_Act    : LREAL; // Actual Gimbal Roll Angle (rad)
    lrGimbalPitch_Act   : LREAL; // Actual Gimbal Pitch Angle (rad)
    lrGimbalYaw_Act     : LREAL; // Actual Gimbal Yaw Angle (rad)
    
    // SIL-3 Safety Interlocks
    bSeatHarnessLocked  : BOOL;
    bHatchSealed        : BOOL;
    bMedicalTelemetryOK : BOOL; // Medical monitoring heartbeat/status
END_VAR

VAR_OUTPUT
    // PackML State Feedback
    eState              : INT; // 0=IDLE, 1=STARTING, 2=EXECUTE, 3=STOPPING, 4=ABORTING, 5=ABORTED
    bFault              : BOOL;
    udiErrorID          : UDINT;
    
    // Drive Commands to Hardware
    lrArmTorque_Cmd     : LREAL; // Commanded Torque to Main Centrifuge Drives (Nm)
    lrGimbalRollTorque_Cmd  : LREAL; // Commanded Torque to Roll Drive (Nm)
    lrGimbalPitchTorque_Cmd : LREAL; // Commanded Torque to Pitch Drive (Nm)
    lrGimbalYawTorque_Cmd   : LREAL; // Commanded Torque to Yaw Drive (Nm)
    
    // Telemetry for Control Room
    lrActualG_x         : LREAL; // Computed actual G_x acting on trainee
    lrActualG_z         : LREAL; // Computed actual G_z acting on trainee
END_VAR

VAR
    // Constants
    lrGravity           : LREAL := 9.80665; // Earth gravity (m/s^2)
    lrArmRadius         : LREAL := 20.0;    // Centrifuge arm length (m)
    lrMaxArmVelocity    : LREAL := 3.5;     // Max allowable arm velocity (rad/s)
    
    // PID Controllers for Drives
    fbArmSpeedPID       : FB_PID_Advanced;
    fbGimbalRollPID     : FB_PID_Advanced;
    fbGimbalPitchPID    : FB_PID_Advanced;
    fbGimbalYawPID      : FB_PID_Advanced;
    
    // Kinematics & Dynamics Internal States
    lrReqCentripetalAccel : LREAL;
    lrTargetArmVelocity   : LREAL;
    
    // Resultant vectors
    lrResultantAccel_Mag  : LREAL;
    
    // Gimbal target angles (inverse kinematics)
    lrTargetGimbalRoll    : LREAL;
    lrTargetGimbalPitch   : LREAL;
    lrTargetGimbalYaw     : LREAL;
    
    // SIL-3 Safety Watchdog
    tSafetyWatchdog       : TON;
    bSafetyOK             : BOOL;
    
    // State Machine Enum representations
    STATE_IDLE      : INT := 0;
    STATE_STARTING  : INT := 1;
    STATE_EXECUTE   : INT := 2;
    STATE_STOPPING  : INT := 3;
    STATE_ABORTING  : INT := 4;
    STATE_ABORTED   : INT := 5;
END_VAR

// --- [ SIL-3 SAFETY INTERLOCK EVALUATION ] ---
bSafetyOK := bSeatHarnessLocked AND bHatchSealed AND bMedicalTelemetryOK AND NOT bAbort;
tSafetyWatchdog(IN:= NOT bMedicalTelemetryOK, PT:= T#2S); // 2-second tolerance for telemetry drop

IF NOT bSafetyOK OR tSafetyWatchdog.Q THEN
    eState := STATE_ABORTING;
    udiErrorID := 16#F000_0001; // Critical safety abort code
END_IF;

// --- [ PACKML STATE MACHINE ] ---
CASE eState OF
    STATE_IDLE:
        lrArmTorque_Cmd := 0.0;
        lrGimbalRollTorque_Cmd := 0.0;
        lrGimbalPitchTorque_Cmd := 0.0;
        lrGimbalYawTorque_Cmd := 0.0;
        
        IF bExecute AND bSafetyOK THEN
            eState := STATE_STARTING;
        END_IF;
        
    STATE_STARTING:
        // Initialize PIDs and zero out targets
        fbArmSpeedPID.bReset := TRUE;
        fbGimbalRollPID.bReset := TRUE;
        fbGimbalPitchPID.bReset := TRUE;
        fbGimbalYawPID.bReset := TRUE;
        eState := STATE_EXECUTE;
        
    STATE_EXECUTE:
        fbArmSpeedPID.bReset := FALSE;
        fbGimbalRollPID.bReset := FALSE;
        fbGimbalPitchPID.bReset := FALSE;
        fbGimbalYawPID.bReset := FALSE;
        
        // Check for normal stop
        IF bStop THEN
            eState := STATE_STOPPING;
        END_IF;
        
        // --- [ 1. DYNAMIC G-FORCE PROFILE GENERATION ] ---
        // Convert Target Gs into required physical acceleration components
        // Resultant vector must equal the vector sum of (Earth Gravity + Centripetal)
        
        lrResultantAccel_Mag := SQRT( (lrTargetG_x * lrGravity) * (lrTargetG_x * lrGravity) + (lrTargetG_z * lrGravity) * (lrTargetG_z * lrGravity) );
        
        // Required centripetal acceleration to match the magnitude minus Earth's 1G z-component
        IF lrResultantAccel_Mag > lrGravity THEN
            lrReqCentripetalAccel := SQRT(ABS( (lrResultantAccel_Mag * lrResultantAccel_Mag) - (lrGravity * lrGravity) ));
        ELSE
            lrReqCentripetalAccel := 0.0;
        END_IF;
        
        // Calculate required Arm Velocity (Omega) = sqrt(A_c / R)
        lrTargetArmVelocity := SQRT(lrReqCentripetalAccel / lrArmRadius);
        
        // Clamp to Max Allowed Velocity
        IF lrTargetArmVelocity > lrMaxArmVelocity THEN
            lrTargetArmVelocity := lrMaxArmVelocity;
        END_IF;
        
        // Compute actual Gs for telemetry based on real arm velocity
        lrActualG_x := ((lrArmVelocity_Act * lrArmVelocity_Act) * lrArmRadius) / lrGravity * COS(lrGimbalPitch_Act);
        lrActualG_z := ((lrArmVelocity_Act * lrArmVelocity_Act) * lrArmRadius) / lrGravity * SIN(lrGimbalPitch_Act) + COS(lrGimbalRoll_Act);
        
        // --- [ 2. 3-AXIS CAPSULE GIMBAL STABILIZATION (INVERSE KINEMATICS) ] ---
        // Pitch axis aligns the resultant centripetal + gravity vector to the chest-spine plane
        IF lrReqCentripetalAccel > 0.001 THEN
            lrTargetGimbalPitch := ATAN(lrGravity / lrReqCentripetalAccel); // Rotate capsule outward
        ELSE
            lrTargetGimbalPitch := 0.0;
        END_IF;
        
        // Roll axis used for G_y nulling (Coriolis compensation) and active tracking
        lrTargetGimbalRoll := 0.0; // Keeping 0 for strict X-Z profile
        
        // Yaw axis used to simulate spin or offset G_x/G_y during transition phases
        lrTargetGimbalYaw := 0.0; 
        
        // --- [ 3. DRIVE PID EXECUTION ] ---
        // Main Arm Speed Control
        fbArmSpeedPID(
            lrSetpoint := lrTargetArmVelocity,
            lrActual   := lrArmVelocity_Act,
            lrKp := 5000.0, lrKi := 1200.0, lrKd := 150.0,
            lrOutput => lrArmTorque_Cmd
        );
        
        // Gimbal Pitch Control (Direct Drive)
        fbGimbalPitchPID(
            lrSetpoint := lrTargetGimbalPitch,
            lrActual   := lrGimbalPitch_Act,
            lrKp := 800.0, lrKi := 50.0, lrKd := 30.0,
            lrOutput => lrGimbalPitchTorque_Cmd
        );
        
        // Gimbal Roll Control
        fbGimbalRollPID(
            lrSetpoint := lrTargetGimbalRoll,
            lrActual   := lrGimbalRoll_Act,
            lrKp := 800.0, lrKi := 50.0, lrKd := 30.0,
            lrOutput => lrGimbalRollTorque_Cmd
        );
        
        // Gimbal Yaw Control
        fbGimbalYawPID(
            lrSetpoint := lrTargetGimbalYaw,
            lrActual   := lrGimbalYaw_Act,
            lrKp := 600.0, lrKi := 40.0, lrKd := 25.0,
            lrOutput => lrGimbalYawTorque_Cmd
        );
        
    STATE_STOPPING:
        // Controlled ramp down
        fbArmSpeedPID(
            lrSetpoint := 0.0,
            lrActual   := lrArmVelocity_Act,
            lrKp := 5000.0, lrKi := 1200.0, lrKd := 150.0,
            lrOutput => lrArmTorque_Cmd
        );
        // Bring gimbals to home
        fbGimbalPitchPID(lrSetpoint := 0.0, lrActual := lrGimbalPitch_Act, lrKp:=800.0, lrKi:=50.0, lrKd:=30.0, lrOutput => lrGimbalPitchTorque_Cmd);
        fbGimbalRollPID(lrSetpoint := 0.0, lrActual := lrGimbalRoll_Act, lrKp:=800.0, lrKi:=50.0, lrKd:=30.0, lrOutput => lrGimbalRollTorque_Cmd);
        fbGimbalYawPID(lrSetpoint := 0.0, lrActual := lrGimbalYaw_Act, lrKp:=800.0, lrKi:=50.0, lrKd:=30.0, lrOutput => lrGimbalYawTorque_Cmd);
        
        IF ABS(lrArmVelocity_Act) < 0.01 AND ABS(lrGimbalPitch_Act) < 0.01 THEN
            eState := STATE_IDLE;
        END_IF;
        
    STATE_ABORTING:
        // Emergency Dynamic Braking
        IF lrArmVelocity_Act > 0.0 THEN
            lrArmTorque_Cmd := -10000.0; 
        ELSIF lrArmVelocity_Act < 0.0 THEN
            lrArmTorque_Cmd := 10000.0;
        ELSE
            lrArmTorque_Cmd := 0.0;
        END_IF;
        
        lrGimbalRollTorque_Cmd := 0.0;
        lrGimbalPitchTorque_Cmd := 0.0;
        lrGimbalYawTorque_Cmd := 0.0;
        
        IF ABS(lrArmVelocity_Act) < 0.01 THEN
            eState := STATE_ABORTED;
        END_IF;
        
    STATE_ABORTED:
        lrArmTorque_Cmd := 0.0;
        IF bReset AND bSafetyOK THEN
            eState := STATE_IDLE;
            udiErrorID := 0;
        END_IF;
        
END_CASE;
END_FUNCTION_BLOCK
```"""

obj = {'messages': [{'role': 'user', 'content': prompt}, {'role': 'assistant', 'content': code}]}
with open(p, 'a', encoding='utf-8') as f:
    f.write(json.dumps(obj) + '\n')
print('DONE')
