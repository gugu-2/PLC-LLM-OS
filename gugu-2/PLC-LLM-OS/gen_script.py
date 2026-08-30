import json
import uuid
import os

# Create directory
os.makedirs('data/swarm_raw', exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Offshore Wind Turbine Jack-up Vessel.
Task: Invent a highly complex control scenario for this domain (e.g., dynamic positioning thruster azimuth control, leg jacking rack-and-pinion synchronization, and crane active heave compensation).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."""

code = """```iec-st
FUNCTION_BLOCK FB_JackUpVessel_MasterControl
// ==============================================================================
// Offshore Wind Turbine Jack-up Vessel Master Control System
// Subsystems:
// 1. Dynamic Positioning (DP) Thruster Azimuth Control
// 2. Leg Jacking Rack-and-Pinion Synchronization (4 Legs)
// 3. Crane Active Heave Compensation (AHC)
// ==============================================================================

VAR_INPUT
    bEnableSystem          : BOOL;  // Main system enable
    bEmergencyStop         : BOOL;  // Global E-stop

    // DP System Inputs
    fWindSpeed             : REAL;  // Current wind speed [m/s]
    fWindDir               : REAL;  // Current wind direction [deg]
    fVesselHeading         : REAL;  // Current vessel heading [deg]
    fTargetHeading         : REAL;  // Desired vessel heading [deg]
    fPositionErrorX        : REAL;  // Position error X [m]
    fPositionErrorY        : REAL;  // Position error Y [m]

    // Jacking System Inputs
    fLeg1Load              : REAL;  // Load on Leg 1 [kN]
    fLeg2Load              : REAL;  // Load on Leg 2 [kN]
    fLeg3Load              : REAL;  // Load on Leg 3 [kN]
    fLeg4Load              : REAL;  // Load on Leg 4 [kN]
    fLeg1Pos               : REAL;  // Position of Leg 1 [m]
    fLeg2Pos               : REAL;  // Position of Leg 2 [m]
    fLeg3Pos               : REAL;  // Position of Leg 3 [m]
    fLeg4Pos               : REAL;  // Position of Leg 4 [m]
    fTargetDraft           : REAL;  // Target vessel draft/height [m]
    bInitiateJacking       : BOOL;  // Start jacking sequence

    // Crane AHC Inputs
    fWaveHeaveAmplt        : REAL;  // Measured wave heave amplitude [m]
    fWaveHeavePeriod       : REAL;  // Measured wave heave period [s]
    fCranePayloadPos       : REAL;  // Current payload vertical position [m]
    fCraneTargetPos        : REAL;  // Desired payload vertical position [m]
END_VAR

VAR_OUTPUT
    bSystemReady           : BOOL;  // System is ready
    bAlarmState            : BOOL;  // Global alarm flag

    // DP Thruster Outputs
    fThruster1AzimuthCmd   : REAL;  // Thruster 1 angle [deg]
    fThruster1PitchCmd     : REAL;  // Thruster 1 pitch/thrust [%]
    fThruster2AzimuthCmd   : REAL;  // Thruster 2 angle [deg]
    fThruster2PitchCmd     : REAL;  // Thruster 2 pitch/thrust [%]
    fThruster3AzimuthCmd   : REAL;  // Thruster 3 angle [deg]
    fThruster3PitchCmd     : REAL;  // Thruster 3 pitch/thrust [%]

    // Jacking Outputs
    fLeg1SpeedCmd          : REAL;  // Leg 1 jacking speed command [mm/s]
    fLeg2SpeedCmd          : REAL;  // Leg 2 jacking speed command [mm/s]
    fLeg3SpeedCmd          : REAL;  // Leg 3 jacking speed command [mm/s]
    fLeg4SpeedCmd          : REAL;  // Leg 4 jacking speed command [mm/s]
    bJackingComplete       : BOOL;  // Jacking sequence done

    // Crane AHC Outputs
    fWinchSpeedCmd         : REAL;  // Winch speed command [m/s]
    bAHCActive             : BOOL;  // AHC is active and locked
END_VAR

VAR
    // Internal States
    eState                 : INT := 0; // 0=Init, 1=Transit/DP, 2=Jacking, 3=Operations/AHC
    
    // DP Control Variables
    fKp_DP                 : REAL := 1.5;
    fKi_DP                 : REAL := 0.1;
    fKd_DP                 : REAL := 0.5;
    fHeadingError          : REAL;
    fIntegralErrorX        : REAL;
    fIntegralErrorY        : REAL;
    
    // Jacking Sync Variables
    fAvgLegPos             : REAL;
    fMaxLegPosDiff         : REAL;
    fPosTolerance          : REAL := 0.05; // 50mm max deviation
    fNominalJackSpeed      : REAL := 10.0; // 10mm/s
    fSyncGain              : REAL := 2.0;

    // Crane AHC Variables
    fAHC_Kp                : REAL := 2.5;
    fAHC_Derivative        : REAL;
    fPrevHeaveAmplt        : REAL;
    fPayloadError          : REAL;
END_VAR

// ==============================================================================
// IMPLEMENTATION
// ==============================================================================

IF bEmergencyStop THEN
    // Reset all commands to safe state
    fThruster1PitchCmd := 0.0;
    fThruster2PitchCmd := 0.0;
    fThruster3PitchCmd := 0.0;
    fLeg1SpeedCmd := 0.0;
    fLeg2SpeedCmd := 0.0;
    fLeg3SpeedCmd := 0.0;
    fLeg4SpeedCmd := 0.0;
    fWinchSpeedCmd := 0.0;
    bSystemReady := FALSE;
    bAlarmState := TRUE;
    RETURN;
END_IF;

bAlarmState := FALSE;
bSystemReady := bEnableSystem;

IF NOT bEnableSystem THEN
    RETURN;
END_IF;

// Determine Operating Mode
IF bInitiateJacking AND eState <> 2 THEN
    eState := 2; // Transition to Jacking
ELSIF bJackingComplete AND eState = 2 THEN
    eState := 3; // Transition to Operations (Crane AHC active)
ELSIF NOT bInitiateJacking AND eState = 0 THEN
    eState := 1; // Default to DP Transit
END_IF;

CASE eState OF
    1: // ================== DYNAMIC POSITIONING MODE ==================
        // Calculate Heading Error
        fHeadingError := fTargetHeading - fVesselHeading;
        IF fHeadingError > 180.0 THEN fHeadingError := fHeadingError - 360.0; END_IF;
        IF fHeadingError < -180.0 THEN fHeadingError := fHeadingError + 360.0; END_IF;
        
        // Simple PID for DP (X, Y, Yaw translation to thrust)
        // Thruster 1 (Bow)
        fThruster1AzimuthCmd := 90.0; // Bow thruster fixed lateral
        fThruster1PitchCmd := (fHeadingError * fKp_DP) + (fPositionErrorY * 0.5);
        
        // Thruster 2 & 3 (Aft Port/Starboard)
        fThruster2AzimuthCmd := 0.0;
        fThruster2PitchCmd := (fPositionErrorX * fKp_DP) - (fHeadingError * 0.2);
        
        fThruster3AzimuthCmd := 0.0;
        fThruster3PitchCmd := (fPositionErrorX * fKp_DP) + (fHeadingError * 0.2);
        
        // Anti-windup and limits
        IF fThruster1PitchCmd > 100.0 THEN fThruster1PitchCmd := 100.0; END_IF;
        IF fThruster1PitchCmd < -100.0 THEN fThruster1PitchCmd := -100.0; END_IF;

    2: // ================== LEG JACKING SYNCHRONIZATION ==================
        // Stop DP thrusters during jacking
        fThruster1PitchCmd := 0.0;
        fThruster2PitchCmd := 0.0;
        fThruster3PitchCmd := 0.0;

        fAvgLegPos := (fLeg1Pos + fLeg2Pos + fLeg3Pos + fLeg4Pos) / 4.0;
        
        // Check for max deviation
        fMaxLegPosDiff := MAX(ABS(fLeg1Pos - fAvgLegPos), ABS(fLeg2Pos - fAvgLegPos));
        fMaxLegPosDiff := MAX(fMaxLegPosDiff, ABS(fLeg3Pos - fAvgLegPos));
        fMaxLegPosDiff := MAX(fMaxLegPosDiff, ABS(fLeg4Pos - fAvgLegPos));
        
        IF fMaxLegPosDiff > (fPosTolerance * 2.0) THEN
            // Synchronization error - halt jacking
            fLeg1SpeedCmd := 0.0;
            fLeg2SpeedCmd := 0.0;
            fLeg3SpeedCmd := 0.0;
            fLeg4SpeedCmd := 0.0;
            bAlarmState := TRUE;
        ELSE
            // Apply synchronized speed commands
            IF fAvgLegPos < fTargetDraft THEN
                fLeg1SpeedCmd := fNominalJackSpeed + (fAvgLegPos - fLeg1Pos) * fSyncGain;
                fLeg2SpeedCmd := fNominalJackSpeed + (fAvgLegPos - fLeg2Pos) * fSyncGain;
                fLeg3SpeedCmd := fNominalJackSpeed + (fAvgLegPos - fLeg3Pos) * fSyncGain;
                fLeg4SpeedCmd := fNominalJackSpeed + (fAvgLegPos - fLeg4Pos) * fSyncGain;
            ELSE
                // Target reached
                fLeg1SpeedCmd := 0.0;
                fLeg2SpeedCmd := 0.0;
                fLeg3SpeedCmd := 0.0;
                fLeg4SpeedCmd := 0.0;
                bJackingComplete := TRUE;
            END_IF;
        END_IF;

    3: // ================== CRANE ACTIVE HEAVE COMPENSATION ==================
        // Vessel is jacked up, but boom might still experience relative dynamics if transferring to a floating vessel.
        // Assuming AHC compensates for relative motion of the supply vessel (fWaveHeaveAmplt).
        
        bAHCActive := TRUE;
        
        // Calculate payload position error
        fPayloadError := fCraneTargetPos - fCranePayloadPos;
        
        // Derivative of wave heave (predictive velocity compensation)
        fAHC_Derivative := (fWaveHeaveAmplt - fPrevHeaveAmplt) / 0.1; // Assuming 100ms cycle
        fPrevHeaveAmplt := fWaveHeaveAmplt;
        
        // Winch speed combines PID for payload positioning and feedforward for heave cancellation
        fWinchSpeedCmd := (fPayloadError * fAHC_Kp) - fAHC_Derivative;
        
        // Speed limits
        IF fWinchSpeedCmd > 5.0 THEN fWinchSpeedCmd := 5.0; END_IF;
        IF fWinchSpeedCmd < -5.0 THEN fWinchSpeedCmd := -5.0; END_IF;
        
END_CASE;
END_FUNCTION_BLOCK
```"""

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": code}
    ]
}

file_name = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(file_name, "w", encoding="utf-8") as f:
    json.dump(record, f)

print(f"Success: {file_name}")
