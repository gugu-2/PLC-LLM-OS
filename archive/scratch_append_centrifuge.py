import json
import os

target_file = r"c:\Users\majip\Downloads\LLM REASEARCH\data\synthetic_generation_v3_enterprise.jsonl"

user_prompt = """You are acting as a Lead Bioprocess Engineer for a major Pharmaceutical company. Evolve a basic motor block into a massive Continuous Blood Plasma Fractionation Centrifuge. Technical Specs: 1. 20,000 RPM magnetic bearing levitation stabilization. 2. Harmonic resonance avoidance during spin-up. 3. Cryogenic chilling jackets to keep plasma proteins from denaturing."""

assistant_response = """```iecst
(* 
   ================================================================================
   ENTERPRISE GRADE IEC 61131-3 CONTINUOUS BLOOD PLASMA FRACTIONATION CENTRIFUGE 
   ================================================================================
   Module: FB_PlasmaFractionationCentrifuge
   Description: 
       Controls a high-speed continuous blood plasma fractionation centrifuge.
       Features:
       - 20,000 RPM high-speed control loop.
       - Magnetic Bearing Levitation Stabilization.
       - Harmonic Resonance Avoidance Profile during spin-up sequence.
       - Cryogenic Chilling Jackets Control to maintain protein integrity.
       - Advanced Alarming, Interlocks, and State Machine.
*)

TYPE E_CentrifugeState :
(
    STATE_IDLE := 0,
    STATE_INITIALIZE_CHILLING := 10,
    STATE_LEVITATION_START := 20,
    STATE_LEVITATION_STABILIZED := 30,
    STATE_SPIN_UP_PRE_RESONANCE := 40,
    STATE_RESONANCE_TRANSITION := 50,
    STATE_SPIN_UP_POST_RESONANCE := 60,
    STATE_FRACTIONATION_RUNNING := 70,
    STATE_SPIN_DOWN := 80,
    STATE_EMERGENCY_COASTDOWN := 90,
    STATE_FAULT := 99
);
END_TYPE

TYPE ST_MagBearingSensors :
STRUCT
    fGapX1 : REAL; // mm
    fGapY1 : REAL; // mm
    fGapX2 : REAL; // mm
    fGapY2 : REAL; // mm
    fRotorVibration : REAL; // mm/s
END_STRUCT
END_TYPE

TYPE ST_MagBearingControl :
STRUCT
    fDriveX1 : REAL; // Current command A
    fDriveY1 : REAL; // Current command A
    fDriveX2 : REAL; // Current command A
    fDriveY2 : REAL; // Current command A
    bLevitationActive : BOOL;
END_STRUCT
END_TYPE

TYPE ST_CryoSensors :
STRUCT
    fTempInlet : REAL;  // Deg C
    fTempOutlet : REAL; // Deg C
    fJacketTemp : REAL; // Deg C
    fPlasmaTemp : REAL; // Deg C
END_STRUCT
END_TYPE

FUNCTION_BLOCK FB_PlasmaFractionationCentrifuge
VAR_INPUT
    bStart_Sequence : BOOL;
    bStop_Sequence : BOOL;
    bEmergencyStop : BOOL;
    bAckFault : BOOL;
    
    // Setpoints
    fTargetRPM : REAL := 20000.0;
    fTargetTemp : REAL := -4.0; // Denaturation threshold protection (typically -2 to -5 for plasma cryo)
    
    // Critical Resonance Bands
    fResonanceLowerLimit : REAL := 8000.0;
    fResonanceUpperLimit : REAL := 12000.0;
    fResonanceTransitionAccel : REAL := 500.0; // RPM/s (Aggressive push through resonance)
    
    // Process Inputs
    stMagBearingSensors : ST_MagBearingSensors;
    stCryoSensors : ST_CryoSensors;
    fCurrentRPM : REAL;
    fMotorTorque : REAL;
END_VAR

VAR_OUTPUT
    eState : E_CentrifugeState;
    fMotorSpeedSetpoint : REAL;
    fCryoValveCmd : REAL; // 0-100%
    stMagBearingCmd : ST_MagBearingControl;
    bFeedValveEnable : BOOL;
    bSystemReady : BOOL;
    bError : BOOL;
    nErrorID : DINT;
    sStatusMessage : STRING(255);
END_VAR

VAR
    // PID Instances (Pseudo representation for IEC implementation)
    PID_Cryo : FB_PID_Controller; // Standard PID loop
    PID_MagBearingX1 : FB_PID_Controller;
    PID_MagBearingY1 : FB_PID_Controller;
    PID_MagBearingX2 : FB_PID_Controller;
    PID_MagBearingY2 : FB_PID_Controller;
    
    fCurrentRampRate : REAL;
    tStateTimer : TON;
    fNominalRampRate : REAL := 50.0; // RPM/s
    
    // Internal Flags
    bLevitationStable : BOOL;
    bCryoStable : BOOL;
    bResonancePassed : BOOL;
END_VAR

// ==========================================
// CONTROL LOGIC
// ==========================================
// 1. EMERGENCY & FAULT HANDLING
IF bEmergencyStop THEN
    eState := E_CentrifugeState.STATE_EMERGENCY_COASTDOWN;
    bError := TRUE;
    nErrorID := 9999;
    sStatusMessage := 'CRITICAL: EMERGENCY STOP ACTIVATED. COASTING DOWN.';
END_IF

IF bError AND bAckFault AND NOT bEmergencyStop THEN
    bError := FALSE;
    nErrorID := 0;
    eState := E_CentrifugeState.STATE_IDLE;
END_IF

// 2. CRYO CHILLING CONTROL LOOP
PID_Cryo(
    rSetpoint := fTargetTemp,
    rProcessValue := stCryoSensors.fPlasmaTemp,
    rKp := 2.5, rTi := 15.0, rTd := 0.0,
    rOutMin := 0.0, rOutMax := 100.0
);
fCryoValveCmd := PID_Cryo.rOutput;

IF ABS(stCryoSensors.fPlasmaTemp - fTargetTemp) < 0.5 THEN
    bCryoStable := TRUE;
ELSE
    bCryoStable := FALSE;
END_IF

// 3. MAGNETIC BEARING LEVITATION STABILIZATION LOOP
// Active magnetic bearing control to keep rotor centered at 0.0 mm offset
PID_MagBearingX1(rSetpoint := 0.0, rProcessValue := stMagBearingSensors.fGapX1, rKp := 500.0, rTd := 2.0);
PID_MagBearingY1(rSetpoint := 0.0, rProcessValue := stMagBearingSensors.fGapY1, rKp := 500.0, rTd := 2.0);
PID_MagBearingX2(rSetpoint := 0.0, rProcessValue := stMagBearingSensors.fGapX2, rKp := 500.0, rTd := 2.0);
PID_MagBearingY2(rSetpoint := 0.0, rProcessValue := stMagBearingSensors.fGapY2, rKp := 500.0, rTd := 2.0);

IF eState >= E_CentrifugeState.STATE_LEVITATION_START THEN
    stMagBearingCmd.bLevitationActive := TRUE;
    stMagBearingCmd.fDriveX1 := PID_MagBearingX1.rOutput;
    stMagBearingCmd.fDriveY1 := PID_MagBearingY1.rOutput;
    stMagBearingCmd.fDriveX2 := PID_MagBearingX2.rOutput;
    stMagBearingCmd.fDriveY2 := PID_MagBearingY2.rOutput;
    
    // Check Levitation Stability
    IF (ABS(stMagBearingSensors.fGapX1) < 0.05) AND (ABS(stMagBearingSensors.fGapY1) < 0.05) THEN
        bLevitationStable := TRUE;
    ELSE
        bLevitationStable := FALSE;
    END_IF
ELSE
    stMagBearingCmd.bLevitationActive := FALSE;
    stMagBearingCmd.fDriveX1 := 0.0;
    stMagBearingCmd.fDriveY1 := 0.0;
    stMagBearingCmd.fDriveX2 := 0.0;
    stMagBearingCmd.fDriveY2 := 0.0;
    bLevitationStable := FALSE;
END_IF

// Vibration monitoring
IF stMagBearingSensors.fRotorVibration > 15.0 THEN // mm/s trip limit
    bError := TRUE;
    nErrorID := 1001; // Vibration Trip
    sStatusMessage := 'FAULT: Rotor Vibration Exceeded Limits.';
    eState := E_CentrifugeState.STATE_FAULT;
END_IF


// 4. MAIN CENTRIFUGE STATE MACHINE
CASE eState OF
    E_CentrifugeState.STATE_IDLE:
        fMotorSpeedSetpoint := 0.0;
        bFeedValveEnable := FALSE;
        sStatusMessage := 'Idle. Ready for Sequence.';
        
        IF bStart_Sequence AND NOT bError THEN
            eState := E_CentrifugeState.STATE_INITIALIZE_CHILLING;
        END_IF
        
    E_CentrifugeState.STATE_INITIALIZE_CHILLING:
        sStatusMessage := 'Pre-chilling vessel to cryogenic setpoint...';
        IF bCryoStable THEN
            eState := E_CentrifugeState.STATE_LEVITATION_START;
        END_IF
        
    E_CentrifugeState.STATE_LEVITATION_START:
        sStatusMessage := 'Activating Magnetic Bearings...';
        tStateTimer(IN := TRUE, PT := T#5S);
        IF bLevitationStable AND tStateTimer.Q THEN
            tStateTimer(IN := FALSE);
            eState := E_CentrifugeState.STATE_LEVITATION_STABILIZED;
        END_IF
        
    E_CentrifugeState.STATE_LEVITATION_STABILIZED:
        sStatusMessage := 'Levitation Stabilized. Commencing Spin-Up.';
        eState := E_CentrifugeState.STATE_SPIN_UP_PRE_RESONANCE;
        
    E_CentrifugeState.STATE_SPIN_UP_PRE_RESONANCE:
        fMotorSpeedSetpoint := fMotorSpeedSetpoint + (fNominalRampRate * 0.1); // Assuming 100ms cycle
        
        IF fMotorSpeedSetpoint >= (fResonanceLowerLimit - 500.0) THEN
            eState := E_CentrifugeState.STATE_RESONANCE_TRANSITION;
            sStatusMessage := 'Approaching Critical Resonance. Accelerating.';
        END_IF
        
    E_CentrifugeState.STATE_RESONANCE_TRANSITION:
        // HARMONIC RESONANCE AVOIDANCE
        // Aggressive acceleration to blast through the critical harmonic resonance band
        fMotorSpeedSetpoint := fMotorSpeedSetpoint + (fResonanceTransitionAccel * 0.1); 
        
        IF fMotorSpeedSetpoint > fResonanceUpperLimit THEN
            eState := E_CentrifugeState.STATE_SPIN_UP_POST_RESONANCE;
            sStatusMessage := 'Resonance Band Cleared. Resuming Nominal Ramp.';
        END_IF
        
    E_CentrifugeState.STATE_SPIN_UP_POST_RESONANCE:
        fMotorSpeedSetpoint := fMotorSpeedSetpoint + (fNominalRampRate * 0.1);
        
        IF fMotorSpeedSetpoint >= fTargetRPM THEN
            fMotorSpeedSetpoint := fTargetRPM;
            eState := E_CentrifugeState.STATE_FRACTIONATION_RUNNING;
        END_IF
        
    E_CentrifugeState.STATE_FRACTIONATION_RUNNING:
        fMotorSpeedSetpoint := fTargetRPM;
        bFeedValveEnable := TRUE; // Enable blood plasma feed only at full 20k RPM
        sStatusMessage := 'Running: Continuous Fractionation Active (20k RPM).';
        bSystemReady := TRUE;
        
        IF stCryoSensors.fPlasmaTemp > (fTargetTemp + 2.0) THEN
            // Protein Denaturation Risk Warning!
            sStatusMessage := 'WARNING: Plasma temperature deviation detected. Adjusting Cryo.';
        END_IF
        
        IF bStop_Sequence THEN
            bFeedValveEnable := FALSE;
            bSystemReady := FALSE;
            eState := E_CentrifugeState.STATE_SPIN_DOWN;
        END_IF
        
    E_CentrifugeState.STATE_SPIN_DOWN:
        sStatusMessage := 'Spin Down Sequence...';
        // Need to clear resonance on the way down as well, but for simplicity, standard decel
        fMotorSpeedSetpoint := fMotorSpeedSetpoint - (fNominalRampRate * 0.1);
        
        IF fMotorSpeedSetpoint <= 0.0 THEN
            fMotorSpeedSetpoint := 0.0;
            eState := E_CentrifugeState.STATE_IDLE;
        END_IF
        
    E_CentrifugeState.STATE_EMERGENCY_COASTDOWN:
        bFeedValveEnable := FALSE;
        fMotorSpeedSetpoint := 0.0; // Remove drive power, allow coasting on mag bearings
        stMagBearingCmd.bLevitationActive := TRUE; // Must keep levitation active until 0 RPM!
        IF fCurrentRPM < 10.0 THEN
            eState := E_CentrifugeState.STATE_FAULT;
        END_IF
        
    E_CentrifugeState.STATE_FAULT:
        fMotorSpeedSetpoint := 0.0;
        bFeedValveEnable := FALSE;
        stMagBearingCmd.bLevitationActive := FALSE; // Drop rotor to backup catcher bearings
        
END_CASE

END_FUNCTION_BLOCK
```"""

new_entry = {
    "messages": [
        {"role": "user", "content": user_prompt},
        {"role": "assistant", "content": assistant_response}
    ]
}

with open(target_file, "a", encoding="utf-8") as f:
    f.write(json.dumps(new_entry) + "\\n")

print("Appended successfully.")
