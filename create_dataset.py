import json, uuid, os

# Ensure directory exists
os.makedirs("data/swarm_raw", exist_ok=True)

prompt = "You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.\nYour specific domain is: Sludge Decanter Centrifuge.\nTask: Invent a highly complex control scenario for this domain (e.g., bowl/scroll differential RPM locking, flocculant polymer volumetric dosing, and solids discharge cake torque detection).\nWrite a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."

code = """FUNCTION_BLOCK FB_DecanterCentrifugeControl
VAR_INPUT
    xEnable : BOOL; // Enable centrifuge sequence
    xEmergencyStop : BOOL; // E-Stop
    rBowlSpeedSp : REAL; // Bowl Speed Setpoint (RPM)
    rScrollDiffSpeedSp : REAL; // Scroll Differential Speed Setpoint (RPM)
    rFlocculantDosingRateSp : REAL; // Polymer dosing rate setpoint (L/h)
    
    // Physical Inputs
    rActualBowlSpeed : REAL; // Actual Bowl Speed from VFD
    rActualScrollSpeed : REAL; // Actual Scroll Speed from VFD
    rTorqueFeedback : REAL; // Cake torque feedback (Nm)
    rInfeedFlowRate : REAL; // Sludge feed flow rate (m3/h)
    xVibrationHighLimit : BOOL; // Vibration switch high
    xBearingTempHigh : BOOL; // Bearing temperature high
END_VAR

VAR_OUTPUT
    xSystemReady : BOOL; // System is ready to start
    xSystemRunning : BOOL; // System is running
    xAlarmActive : BOOL; // Global alarm flag
    
    // Physical Outputs
    rBowlVFDControl : REAL; // Speed reference to Bowl VFD (RPM)
    rScrollVFDControl : REAL; // Speed reference to Scroll VFD (RPM)
    rFlocculantPumpControl : REAL; // Dosing pump control (0-100%)
    xFeedPumpEnable : BOOL; // Enable sludge feed pump
END_VAR

VAR
    iState : INT := 0; // State machine step
    
    // PID Controllers (Simulated representation)
    rTorqueError : REAL;
    rTorqueIntegral : REAL;
    rDifferentialCorrection : REAL;
    
    // Timers
    tonStartDelay : TON;
    tonRampUp : TON;
    tonFeedDelay : TON;
    
    // Internal limits
    rMaxTorqueLimit : REAL := 1500.0; // Nm
    rOptimalTorque : REAL := 800.0; // Nm
    rMaxVibrationTime : TIME := T#2S;
    tonVibrationDelay : TON;
END_VAR

// Alarm checking
IF xEmergencyStop OR xBearingTempHigh THEN
    iState := 99; // Fault state
END_IF

tonVibrationDelay(IN := xVibrationHighLimit, PT := rMaxVibrationTime);
IF tonVibrationDelay.Q THEN
    iState := 99; // Fault state
END_IF

// State Machine
CASE iState OF
    0: // Stop / Ready State
        xSystemReady := TRUE;
        xSystemRunning := FALSE;
        xFeedPumpEnable := FALSE;
        rBowlVFDControl := 0.0;
        rScrollVFDControl := 0.0;
        rFlocculantPumpControl := 0.0;
        
        IF xEnable AND NOT xAlarmActive THEN
            xSystemReady := FALSE;
            iState := 10;
        END_IF
        
    10: // Ramp up Bowl
        xSystemRunning := TRUE;
        rBowlVFDControl := rBowlSpeedSp;
        
        IF ABS(rBowlSpeedSp - rActualBowlSpeed) < 50.0 THEN
            iState := 20;
        END_IF
        
    20: // Start Scroll
        rScrollVFDControl := rActualBowlSpeed - rScrollDiffSpeedSp;
        
        IF ABS(rActualBowlSpeed - rActualScrollSpeed - rScrollDiffSpeedSp) < 5.0 THEN
            iState := 30; // Start Dosing
        END_IF
        
    30: // Start Flocculant
        rFlocculantPumpControl := rFlocculantDosingRateSp / 10.0; // Scale to %
        tonFeedDelay(IN := TRUE, PT := T#10S);
        
        IF tonFeedDelay.Q THEN
            tonFeedDelay(IN := FALSE);
            iState := 40;
        END_IF
        
    40: // Start Sludge Feed
        xFeedPumpEnable := TRUE;
        iState := 50;
        
    50: // Steady State Control - Torque optimization
        // Calculate torque error
        rTorqueError := rTorqueFeedback - rOptimalTorque;
        
        // Simple PI control for differential speed based on torque
        rTorqueIntegral := rTorqueIntegral + (rTorqueError * 0.1);
        rDifferentialCorrection := (rTorqueError * 0.5) + rTorqueIntegral;
        
        // Limit correction
        IF rDifferentialCorrection > 10.0 THEN
            rDifferentialCorrection := 10.0;
        ELSIF rDifferentialCorrection < -10.0 THEN
            rDifferentialCorrection := -10.0;
        END_IF
        
        rScrollVFDControl := rActualBowlSpeed - (rScrollDiffSpeedSp + rDifferentialCorrection);
        
        // Maintain Flocculant based on feed
        rFlocculantPumpControl := (rInfeedFlowRate * 0.5) + (rFlocculantDosingRateSp / 10.0);
        
        // Over-torque protection
        IF rTorqueFeedback > rMaxTorqueLimit THEN
            xFeedPumpEnable := FALSE;
            iState := 60; // Flush state
        END_IF
        
        IF NOT xEnable THEN
            iState := 0; // Shutdown
        END_IF
        
    60: // Flush state
        xFeedPumpEnable := FALSE;
        rFlocculantPumpControl := 0.0;
        rScrollVFDControl := rActualBowlSpeed - (rScrollDiffSpeedSp + 15.0); // Increase diff speed to clear
        
        IF rTorqueFeedback < (rOptimalTorque * 0.5) THEN
            iState := 40; // Resume feed
        END_IF
        
    99: // Fault State
        xAlarmActive := TRUE;
        xSystemRunning := FALSE;
        xFeedPumpEnable := FALSE;
        rBowlVFDControl := 0.0;
        rScrollVFDControl := 0.0;
        rFlocculantPumpControl := 0.0;
        
        IF NOT (xEmergencyStop OR xBearingTempHigh OR tonVibrationDelay.Q) AND NOT xEnable THEN
            xAlarmActive := FALSE;
            iState := 0;
        END_IF
END_CASE
END_FUNCTION_BLOCK"""

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": f"```iec-st\n{code}\n```"}
    ]
}

filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)
print(f"Saved to {filename}")
