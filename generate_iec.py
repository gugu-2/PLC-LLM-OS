import os
import json
import uuid

os.makedirs('data/swarm_raw', exist_ok=True)

st_code = """```iec-st
FUNCTION_BLOCK FB_Diaper_Web_Master_Control
TITLE = 'High-Speed Diaper Web Converting & SAP Dosing Master Control'
// 
// This function block orchestrates the complex web handling,
// ultrasonic bonding, SAP dosing, and rotary die cutting for
// high-speed diaper manufacturing lines.
//

VAR_INPUT
    bEnableLine           : BOOL;  // Main line enable
    rMasterVelocity       : REAL;  // Master line speed in m/s
    rTensionSetpoint      : REAL;  // Web tension setpoint in N
    rActualTension        : REAL;  // Actual web tension feedback in N
    rSAPTargetDosing      : REAL;  // Target SAP dosing in g/pad
    rSAPActualFlow        : REAL;  // Actual SAP flow rate in g/s
    bUltrasonicReady      : BOOL;  // Ultrasonic generator ready status
    rBondingPressure      : REAL;  // Required bonding pressure in Bar
    bRotaryDieHome        : BOOL;  // Rotary die cutter home position sensor
    rProductLength        : REAL;  // Diaper product length in mm
END_VAR

VAR_OUTPUT
    bLineRunning          : BOOL;  // Line is actively running
    bError                : BOOL;  // General error flag
    iErrorCode            : INT;   // Error code for diagnostics
    rTensionCtrlOut       : REAL;  // Speed trim for tension control (%)
    rSAPDosingSpeedOut    : REAL;  // Speed reference for SAP screw feeder (RPM)
    bUltrasonicEnable     : BOOL;  // Enable ultrasonic bonding
    rBondingPressureOut   : REAL;  // Output to proportional valve for bonding pressure
    rRotaryDiePhaseTrim   : REAL;  // Phase correction for rotary die cutter (degrees)
    bCutterEngage         : BOOL;  // Engage die cutter
END_VAR

VAR
    // State Machine
    iState                : INT := 0; 
    
    // PID for Tension Control
    rTensionError         : REAL;
    rTensionIntegral      : REAL;
    rTensionDerivative    : REAL;
    rTensionLastError     : REAL;
    Kp_Tension            : REAL := 1.5;
    Ki_Tension            : REAL := 0.2;
    Kd_Tension            : REAL := 0.05;
    
    // SAP Dosing Control
    rSAPError             : REAL;
    rSAPIntegral          : REAL;
    Kp_SAP                : REAL := 2.0;
    Ki_SAP                : REAL := 0.5;
    rSAPFeedForward       : REAL;
    
    // Rotary Die Registration
    rVirtualMasterPos     : REAL;  // Virtual master position in mm
    rCutPosition          : REAL;  // Calculated cut position
    rPhaseError           : REAL;
    Kp_Phase              : REAL := 0.1;
    
    // Timers & Filters
    TMR_StartDelay        : TON;
    TMR_BondingDwell      : TON;
    rFilteredVelocity     : REAL;
END_VAR

// ==============================================================================
// 1. STATE MACHINE FOR LINE CONTROL
// ==============================================================================
CASE iState OF
    0: // STOPPED
        bLineRunning := FALSE;
        bUltrasonicEnable := FALSE;
        bCutterEngage := FALSE;
        rTensionCtrlOut := 0.0;
        rSAPDosingSpeedOut := 0.0;
        
        IF bEnableLine THEN
            iState := 10;
            TMR_StartDelay(IN := FALSE);
        END_IF;
        
    10: // STARTING UP - TENSION ESTABLISHMENT
        TMR_StartDelay(IN := TRUE, PT := T#2S);
        
        // Tension PID calculation
        rTensionError := rTensionSetpoint - rActualTension;
        rTensionIntegral := rTensionIntegral + (rTensionError * 0.01); // 10ms task
        rTensionDerivative := (rTensionError - rTensionLastError) / 0.01;
        rTensionCtrlOut := (Kp_Tension * rTensionError) + (Ki_Tension * rTensionIntegral) + (Kd_Tension * rTensionDerivative);
        rTensionLastError := rTensionError;
        
        // Limit tension control authority during startup
        IF rTensionCtrlOut > 10.0 THEN rTensionCtrlOut := 10.0; END_IF;
        IF rTensionCtrlOut < -10.0 THEN rTensionCtrlOut := -10.0; END_IF;
        
        IF TMR_StartDelay.Q THEN
            iState := 20;
        END_IF;
        
        IF NOT bEnableLine THEN iState := 0; END_IF;

    20: // RUNNING - FULL PRODUCTION
        bLineRunning := TRUE;
        bCutterEngage := TRUE;
        
        // --- TENSION CONTROL ---
        rTensionError := rTensionSetpoint - rActualTension;
        // Anti-windup
        IF (rTensionCtrlOut < 100.0 AND rTensionCtrlOut > -100.0) THEN
            rTensionIntegral := rTensionIntegral + (rTensionError * 0.01);
        END_IF;
        rTensionDerivative := (rTensionError - rTensionLastError) / 0.01;
        rTensionCtrlOut := (Kp_Tension * rTensionError) + (Ki_Tension * rTensionIntegral) + (Kd_Tension * rTensionDerivative);
        rTensionLastError := rTensionError;
        
        // --- SAP DOSING CONTROL (Feedforward + PI) ---
        // Feedforward based on master line speed and target g/pad
        // Assumes conversion factor from m/s and g/pad to screw RPM
        rSAPFeedForward := rMasterVelocity * rSAPTargetDosing * 15.0; 
        
        rSAPError := (rMasterVelocity * rSAPTargetDosing * 1000.0 / rProductLength) - rSAPActualFlow;
        rSAPIntegral := rSAPIntegral + (rSAPError * 0.01);
        rSAPDosingSpeedOut := rSAPFeedForward + (Kp_SAP * rSAPError) + (Ki_SAP * rSAPIntegral);
        
        // Max limit on dosing
        IF rSAPDosingSpeedOut > 3000.0 THEN rSAPDosingSpeedOut := 3000.0; END_IF;
        IF rSAPDosingSpeedOut < 0.0 THEN rSAPDosingSpeedOut := 0.0; END_IF;
        
        // --- ULTRASONIC BONDING CONTROL ---
        IF bUltrasonicReady AND (rMasterVelocity > 0.5) THEN
            bUltrasonicEnable := TRUE;
            // Modulate pressure based on speed (higher speed = slightly higher pressure)
            rBondingPressureOut := rBondingPressure + (rMasterVelocity * 0.2);
            IF rBondingPressureOut > 8.0 THEN rBondingPressureOut := 8.0; END_IF; // Max 8 bar
        ELSE
            bUltrasonicEnable := FALSE;
            rBondingPressureOut := 0.0;
        END_IF;
        
        // --- ROTARY DIE REGISTRATION ---
        // Update virtual master position integration
        rVirtualMasterPos := rVirtualMasterPos + (rMasterVelocity * 1000.0 * 0.01); // mm per 10ms
        IF rVirtualMasterPos >= rProductLength THEN
            rVirtualMasterPos := rVirtualMasterPos - rProductLength;
        END_IF;
        
        // Simple phase correction when die is home
        IF bRotaryDieHome THEN
            // Die should be home at 0 position of the product length
            rPhaseError := 0.0 - rVirtualMasterPos;
            // Shortest path calculation
            IF rPhaseError > (rProductLength / 2.0) THEN
                rPhaseError := rPhaseError - rProductLength;
            ELSIF rPhaseError < -(rProductLength / 2.0) THEN
                rPhaseError := rPhaseError + rProductLength;
            END_IF;
            
            // Convert linear error to rotary phase trim (assume 360 deg = 1 product length)
            rRotaryDiePhaseTrim := (rPhaseError / rProductLength) * 360.0 * Kp_Phase;
        ELSE
            rRotaryDiePhaseTrim := 0.0;
        END_IF;
        
        IF NOT bEnableLine THEN iState := 30; END_IF;
        
        // Error monitoring
        IF ABS(rTensionError) > (rTensionSetpoint * 0.5) THEN
            iState := 99; // Error state
            iErrorCode := 101; // Tension out of bounds
        END_IF;
        
    30: // STOPPING
        bLineRunning := FALSE;
        bCutterEngage := FALSE;
        bUltrasonicEnable := FALSE;
        rSAPDosingSpeedOut := 0.0;
        
        IF rMasterVelocity < 0.1 THEN
            iState := 0;
        END_IF;
        
    99: // ERROR STATE
        bLineRunning := FALSE;
        bError := TRUE;
        bUltrasonicEnable := FALSE;
        bCutterEngage := FALSE;
        rTensionCtrlOut := 0.0;
        rSAPDosingSpeedOut := 0.0;
        rBondingPressureOut := 0.0;
        
        IF NOT bEnableLine THEN
            bError := FALSE;
            iErrorCode := 0;
            iState := 0;
        END_IF;
        
END_CASE;
END_FUNCTION_BLOCK
```"""

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: High-Speed Diaper Manufacturing / Web Converting.
Task: Invent a highly complex control scenario for this domain (e.g., non-woven material ultrasonic bonding, Super Absorbent Polymer (SAP) dosing cascades, and rotary die cutting registration).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O.

CRITICAL RULES:
1. You MUST output the code enclosed in a ```iec-st markdown code fence. DO NOT APOLOGIZE. DO NOT EXPLAIN.
2. The code must be >= 1500 chars, with FUNCTION_BLOCK and VAR_INPUT/VAR_OUTPUT."""

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": st_code}
    ]
}

filepath = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filepath, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)

print(f"Success. File written to: {os.path.abspath(filepath)}")
