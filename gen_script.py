import json
import uuid
import os

prompt = "Invent a highly complex control scenario for a Semiconductor Photolithography Stepper. Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."

code = """FUNCTION_BLOCK FB_PhotolithographyStepperControl
VAR_INPUT
    bEnable : BOOL; (* Enable system *)
    rTargetX : REAL; (* Target X position in nm *)
    rTargetY : REAL; (* Target Y position in nm *)
    rTargetZ : REAL; (* Target Z position in nm *)
    rTargetDose : REAL; (* Target Excimer Laser Dose mJ/cm2 *)
    
    (* Interferometric feedback *)
    rActualX : REAL; 
    rActualY : REAL;
    rActualZ : REAL;
    
    (* Reticle Alignment *)
    rReticleErrorX : REAL;
    rReticleErrorY : REAL;
    rReticleErrorTheta : REAL;
    
    rCurrentLaserPower : REAL;
END_VAR

VAR_OUTPUT
    bInPosition : BOOL;
    bDoseComplete : BOOL;
    bError : BOOL;
    nErrorCode : INT;
    
    (* Actuator commands *)
    rCmdStageX : REAL;
    rCmdStageY : REAL;
    rCmdStageZ : REAL;
    rCmdReticleX : REAL;
    rCmdReticleY : REAL;
    rCmdReticleTheta : REAL;
    rCmdLaserPulseRate : REAL;
END_VAR

VAR
    (* Internal State *)
    nState : INT := 0;
    
    (* PID Controllers *)
    rErrorX, rErrorY, rErrorZ : REAL;
    rLastErrorX, rLastErrorY, rLastErrorZ : REAL;
    rIntegralX, rIntegralY, rIntegralZ : REAL;
    
    rKpStage : REAL := 0.5;
    rKiStage : REAL := 0.01;
    rKdStage : REAL := 0.1;
    
    rTolerancePos : REAL := 5.0; (* 5 nm *)
    rAccumulatedDose : REAL := 0.0;
    
    rMaxPulseRate : REAL := 4000.0; (* Hz *)
END_VAR

IF NOT bEnable THEN
    nState := 0;
    bInPosition := FALSE;
    bDoseComplete := FALSE;
    bError := FALSE;
    rCmdStageX := 0.0;
    rCmdStageY := 0.0;
    rCmdStageZ := 0.0;
    rCmdLaserPulseRate := 0.0;
    rAccumulatedDose := 0.0;
    RETURN;
END_IF;

CASE nState OF
    0: (* Initialization and Wait for Target *)
        IF rTargetX > 0.0 AND rTargetY > 0.0 THEN
            nState := 10; (* Start positioning *)
            bDoseComplete := FALSE;
            rAccumulatedDose := 0.0;
        END_IF;
        
    10: (* Wafer Stage Nanometer-scale Interferometric Positioning *)
        rErrorX := rTargetX - rActualX;
        rErrorY := rTargetY - rActualY;
        rErrorZ := rTargetZ - rActualZ;
        
        rIntegralX := rIntegralX + rErrorX;
        rIntegralY := rIntegralY + rErrorY;
        rIntegralZ := rIntegralZ + rErrorZ;
        
        rCmdStageX := (rKpStage * rErrorX) + (rKiStage * rIntegralX) + (rKdStage * (rErrorX - rLastErrorX));
        rCmdStageY := (rKpStage * rErrorY) + (rKiStage * rIntegralY) + (rKdStage * (rErrorY - rLastErrorY));
        rCmdStageZ := (rKpStage * rErrorZ) + (rKiStage * rIntegralZ) + (rKdStage * (rErrorZ - rLastErrorZ));
        
        rLastErrorX := rErrorX;
        rLastErrorY := rErrorY;
        rLastErrorZ := rErrorZ;
        
        IF ABS(rErrorX) < rTolerancePos AND ABS(rErrorY) < rTolerancePos AND ABS(rErrorZ) < rTolerancePos THEN
            bInPosition := TRUE;
            nState := 20; (* Reticle alignment error correction *)
        ELSE
            bInPosition := FALSE;
        END_IF;
        
    20: (* Reticle Alignment Error Correction *)
        (* Adjust reticle based on measured errors *)
        rCmdReticleX := -rReticleErrorX * 0.8; (* Proportional correction *)
        rCmdReticleY := -rReticleErrorY * 0.8;
        rCmdReticleTheta := -rReticleErrorTheta * 0.8;
        
        IF ABS(rReticleErrorX) < 1.0 AND ABS(rReticleErrorY) < 1.0 AND ABS(rReticleErrorTheta) < 0.001 THEN
            nState := 30; (* Laser Dose Control *)
        END_IF;
        
    30: (* Excimer Laser Dose Control *)
        IF rAccumulatedDose < rTargetDose THEN
            IF rCurrentLaserPower > 0.0 THEN
                rCmdLaserPulseRate := (rTargetDose - rAccumulatedDose) / rCurrentLaserPower * 1000.0;
                IF rCmdLaserPulseRate > rMaxPulseRate THEN
                    rCmdLaserPulseRate := rMaxPulseRate;
                END_IF;
            ELSE
                bError := TRUE;
                nErrorCode := 101; (* Laser Power Loss *)
                nState := 99;
            END_IF;
            
            rAccumulatedDose := rAccumulatedDose + (rCmdLaserPulseRate * rCurrentLaserPower * 0.001);
        ELSE
            rCmdLaserPulseRate := 0.0;
            bDoseComplete := TRUE;
            nState := 40; (* Step complete *)
        END_IF;
        
    40: (* Complete *)
        IF NOT bEnable THEN
            nState := 0;
        END_IF;
        
    99: (* Error State *)
        rCmdStageX := 0.0;
        rCmdStageY := 0.0;
        rCmdStageZ := 0.0;
        rCmdReticleX := 0.0;
        rCmdReticleY := 0.0;
        rCmdReticleTheta := 0.0;
        rCmdLaserPulseRate := 0.0;
        bInPosition := FALSE;
        bDoseComplete := FALSE;
END_CASE;"""

os.makedirs('data/swarm_raw', exist_ok=True)
record = {
    'messages': [
        {'role': 'user', 'content': prompt},
        {'role': 'assistant', 'content': f'```iec-st\n{code}\n```'}
    ]
}
with open(f'data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json', 'w', encoding='utf-8') as f:
    json.dump(record, f, indent=4)
