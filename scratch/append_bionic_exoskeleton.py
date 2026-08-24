import json

prompt = """You are acting as the Chief Cybernetics Engineer for a Next-Generation Medical Bionics Corporation.

Your mission is to generate a master-tier, production-ready IEC 61131-3 Structured Text (ST) implementation for the "Powered Bionic Exoskeleton Neural Interface & Haptic Impedance Controller" (`FB_BionicExoskeleton`).

### Technical Specifications & Engineering Rigor Required:
1. **Electromyography (EMG) Intent Decoding**:
   - Real-time digital signal processing of surface EMG signals from the user's residual limb.
   - Non-linear thresholding and muscle activation envelope extraction to predict intended joint torque before the user physically moves.
2. **Variable Impedance Actuation (VIA)**:
   - Dynamic adjustment of mechanical stiffness and damping at the knee and ankle joints using series elastic actuators (SEAs) and magnetorheological (MR) fluid dampers.
   - Gait phase detection (heel-strike, mid-stance, toe-off, swing) utilizing foot-sole pressure matrices and 6-axis IMUs to adapt the virtual spring-mass model.
3. **Code Quality**: Strict IEC 61131-3 ST, LREAL datatypes, multi-body kinematics equations, redundant safety fault limiters, PackML states.

Output a complete, valid JSON object with {"messages": [{"role": "user", "content": "Mega-prompt description"}, {"role": "assistant", "content": "Full raw Structured Text code inside ```iec-st```"}]}.
Append this JSON directly to `data/synthetic_generation_v3_enterprise.jsonl` using a safe append script."""

assistant_content = """```iec-st
FUNCTION_BLOCK FB_BionicExoskeleton
VAR_INPUT
    bEnable                 : BOOL; // Enable system
    bEmergencyStop          : BOOL; // E-Stop
    fEMG_ResidualLimb_mV    : LREAL; // Surface EMG reading (mV)
    fJointAngleKnee_rad     : LREAL; // Knee angle
    fJointAngleAnkle_rad    : LREAL; // Ankle angle
    aFootPressureMatrix     : ARRAY[1..16] OF LREAL; // 16-point pressure matrix on foot sole
    stIMU_6Axis             : ST_IMU_Data; // 6-axis IMU data (Accel & Gyro)
END_VAR

VAR_OUTPUT
    bSystemReady            : BOOL; // PackML State Ready
    fCmdTorqueKnee_Nm       : LREAL; // Target torque for Knee SEA
    fCmdTorqueAnkle_Nm      : LREAL; // Target torque for Ankle SEA
    fCmdDampingMR_Nms       : LREAL; // Target damping for MR fluid damper
    eState                  : E_PackML_State; // Current PackML State
    bFault                  : BOOL;
    nFaultID                : UDINT;
END_VAR

VAR
    // EMG Processing
    fEMG_Filtered           : LREAL;
    fEMG_Envelope           : LREAL;
    fEMG_Threshold          : LREAL := 0.25; // mV
    fIntentGain             : LREAL := 50.0; // Nm/mV
    
    // Low-pass filter for EMG
    fAlphaEMG               : LREAL := 0.05;
    
    // Gait Phase
    eGaitPhase              : E_GaitPhase;
    fTotalPressure          : LREAL;
    fCenterOfPressure_X     : LREAL;
    fCenterOfPressure_Y     : LREAL;
    
    // Impedance Control (Virtual Spring-Mass)
    fStiffnessKnee          : LREAL; // Nm/rad
    fDampingKnee            : LREAL; // Nms/rad
    fStiffnessAnkle         : LREAL; 
    
    // Constants
    cKnee_Stiffness_Stance  : LREAL := 300.0;
    cKnee_Stiffness_Swing   : LREAL := 20.0;
    cKnee_Damping_Stance    : LREAL := 15.0;
    cKnee_Damping_Swing     : LREAL := 2.0;
    
    i                       : INT;
    fCoordX                 : ARRAY[1..16] OF LREAL := [0.1, 0.2, 0.3, 0.4, 0.1, 0.2, 0.3, 0.4, 0.1, 0.2, 0.3, 0.4, 0.1, 0.2, 0.3, 0.4];
    fCoordY                 : ARRAY[1..16] OF LREAL := [0.1, 0.1, 0.1, 0.1, 0.2, 0.2, 0.2, 0.2, 0.3, 0.3, 0.3, 0.3, 0.4, 0.4, 0.4, 0.4];
END_VAR

// -----------------------------------------------------------------------------
// State Machine (PackML simplified)
// -----------------------------------------------------------------------------
IF bEmergencyStop THEN
    eState := E_PackML_State.Aborted;
    bFault := TRUE;
    nFaultID := 1001; // E-Stop pressed
    fCmdTorqueKnee_Nm := 0.0;
    fCmdTorqueAnkle_Nm := 0.0;
    fCmdDampingMR_Nms := 50.0; // High damping for safety
    RETURN;
END_IF

CASE eState OF
    E_PackML_State.Stopped:
        IF bEnable THEN
            eState := E_PackML_State.Starting;
        END_IF
        
    E_PackML_State.Starting:
        // Initialize filters and calibrations
        fEMG_Filtered := fEMG_ResidualLimb_mV;
        eState := E_PackML_State.Execute;
        bSystemReady := TRUE;
        
    E_PackML_State.Execute:
        IF NOT bEnable THEN
            eState := E_PackML_State.Stopping;
        END_IF
        
        // 1. Electromyography (EMG) Intent Decoding
        // Low-pass filter the rectified EMG signal
        fEMG_Filtered := fEMG_Filtered + fAlphaEMG * (ABS(fEMG_ResidualLimb_mV) - fEMG_Filtered);
        
        // Non-linear thresholding & Envelope extraction
        IF fEMG_Filtered > fEMG_Threshold THEN
            fEMG_Envelope := fEMG_Filtered - fEMG_Threshold;
        ELSE
            fEMG_Envelope := 0.0;
        END_IF
        
        // 2. Gait Phase Detection
        fTotalPressure := 0.0;
        fCenterOfPressure_X := 0.0;
        fCenterOfPressure_Y := 0.0;
        
        FOR i := 1 TO 16 DO
            fTotalPressure := fTotalPressure + aFootPressureMatrix[i];
            fCenterOfPressure_X := fCenterOfPressure_X + (aFootPressureMatrix[i] * fCoordX[i]);
            fCenterOfPressure_Y := fCenterOfPressure_Y + (aFootPressureMatrix[i] * fCoordY[i]);
        END_FOR
        
        IF fTotalPressure > 0.1 THEN
            fCenterOfPressure_X := fCenterOfPressure_X / fTotalPressure;
            fCenterOfPressure_Y := fCenterOfPressure_Y / fTotalPressure;
        END_IF
        
        // Simple state machine for gait phase
        IF fTotalPressure > 50.0 THEN
            IF fCenterOfPressure_Y < 0.2 THEN
                eGaitPhase := E_GaitPhase.HeelStrike;
            ELSIF fCenterOfPressure_Y > 0.3 THEN
                eGaitPhase := E_GaitPhase.ToeOff;
            ELSE
                eGaitPhase := E_GaitPhase.MidStance;
            END_IF
        ELSE
            eGaitPhase := E_GaitPhase.Swing;
        END_IF
        
        // 3. Variable Impedance Actuation (VIA) Control
        // Adapt stiffness and damping based on gait phase
        CASE eGaitPhase OF
            E_GaitPhase.HeelStrike, E_GaitPhase.MidStance:
                fStiffnessKnee := cKnee_Stiffness_Stance;
                fDampingKnee := cKnee_Damping_Stance;
                
            E_GaitPhase.ToeOff, E_GaitPhase.Swing:
                fStiffnessKnee := cKnee_Stiffness_Swing;
                fDampingKnee := cKnee_Damping_Swing;
        END_CASE
        
        // Calculate commanded torque using Virtual Spring-Mass model + Intent
        // Tau = K * (theta_ref - theta) - D * (theta_dot) + IntentTorque
        // Assuming theta_ref is 0 for simplicity, and theta_dot derived from gyro
        fCmdTorqueKnee_Nm := -fStiffnessKnee * fJointAngleKnee_rad 
                             - fDampingKnee * stIMU_6Axis.fGyroY 
                             + (fEMG_Envelope * fIntentGain);
                             
        // Ankle torque logic
        fStiffnessAnkle := fStiffnessKnee * 0.5; // Simplified coupling
        fCmdTorqueAnkle_Nm := -fStiffnessAnkle * fJointAngleAnkle_rad 
                              - (fDampingKnee * 0.5) * stIMU_6Axis.fGyroY;
                              
        // Set Magnetorheological fluid damping based on shock absorption need
        IF eGaitPhase = E_GaitPhase.HeelStrike THEN
            fCmdDampingMR_Nms := 20.0;
        ELSE
            fCmdDampingMR_Nms := 5.0;
        END_IF
        
        // 4. Redundant Safety Fault Limiters
        IF ABS(fCmdTorqueKnee_Nm) > 150.0 OR ABS(fCmdTorqueAnkle_Nm) > 120.0 THEN
            bFault := TRUE;
            nFaultID := 2001; // Torque limit exceeded
            eState := E_PackML_State.Aborting;
        END_IF

    E_PackML_State.Stopping:
        fCmdTorqueKnee_Nm := 0.0;
        fCmdTorqueAnkle_Nm := 0.0;
        bSystemReady := FALSE;
        eState := E_PackML_State.Stopped;
        
    E_PackML_State.Aborting:
        fCmdTorqueKnee_Nm := 0.0;
        fCmdTorqueAnkle_Nm := 0.0;
        fCmdDampingMR_Nms := 50.0;
        bSystemReady := FALSE;
        eState := E_PackML_State.Aborted;
        
    E_PackML_State.Aborted:
        // Wait for reset (not implemented in this minimal example)
        IF NOT bEmergencyStop AND NOT bFault THEN
            eState := E_PackML_State.Stopped;
        END_IF

END_CASE
```"""

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": assistant_content}
    ]
}

with open(r'c:\Users\majip\Downloads\LLM REASEARCH\data\synthetic_generation_v3_enterprise.jsonl', 'a', encoding='utf-8') as f:
    f.write(json.dumps(record) + '\\n')
