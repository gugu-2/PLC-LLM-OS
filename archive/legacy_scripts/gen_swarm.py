import json, uuid, os

prompt = "You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.\nYour specific domain is: Semiconductor Photolithography Stepper.\nTask: Invent a highly complex control scenario for this domain (e.g., wafer stage interferometry tracking, excimer laser dose control, and reticle alignment optics).\nWrite a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."

code = """```iec-st
FUNCTION_BLOCK FB_PhotolithographyStepperControl
(*
    Semiconductor Photolithography Stepper Control System
    Handles Wafer Stage Interferometry Tracking, Excimer Laser Dose Control, and Reticle Alignment Optics.
    Sub-nanometer precision requires high-speed deterministic execution.
*)
VAR_INPUT
    bEnable                 : BOOL;   (* System Enable *)
    bStartExposure          : BOOL;   (* Trigger Exposure Sequence *)
    fTargetPosX_nm          : LREAL;  (* Target X Position in nanometers *)
    fTargetPosY_nm          : LREAL;  (* Target Y Position in nanometers *)
    fTargetDose_mJ          : LREAL;  (* Target UV Dose in mJ/cm^2 *)
    
    (* Interferometer Feedback *)
    fActualPosX_nm          : LREAL;
    fActualPosY_nm          : LREAL;
    fLaserIntensity_mW      : LREAL;  (* Current laser intensity from sensor *)
    
    (* Reticle Alignment *)
    fReticleErrorX_nm       : LREAL;
    fReticleErrorY_nm       : LREAL;
    fReticleErrorTheta_urad : LREAL;
END_VAR

VAR_OUTPUT
    bSystemReady            : BOOL;
    bExposureActive         : BOOL;
    bExposureComplete       : BOOL;
    bError                  : BOOL;
    nErrorCode              : INT;
    
    (* Actuator Commands *)
    fCmdVelocityX_m_s       : LREAL;
    fCmdVelocityY_m_s       : LREAL;
    bLaserTrigger           : BOOL;
    fLaserAttenuator        : LREAL;  (* 0.0 to 100.0 % *)
    
    (* Reticle Stage Commands *)
    fCmdReticleX_nm         : LREAL;
    fCmdReticleY_nm         : LREAL;
    fCmdReticleTheta_urad   : LREAL;
END_VAR

VAR
    eState                  : (INIT, ALIGN_RETICLE, MOVE_STAGE, SETTLE, EXPOSE, POST_EXPOSE, ERROR);
    fAccumulatedDose_mJ     : LREAL;
    tExposureTimer          : TON;
    fStageErrorX            : LREAL;
    fStageErrorY            : LREAL;
    
    (* PID Controllers for Stage *)
    fKp_Stage               : LREAL := 0.05;
    fKd_Stage               : LREAL := 0.001;
    fPrevErrorX             : LREAL;
    fPrevErrorY             : LREAL;
    
    (* Laser Control *)
    fNominalPulse_mJ        : LREAL := 5.0;
    nPulseCount             : DINT;
    nRequiredPulses         : DINT;
END_VAR

(* Implementation *)
IF NOT bEnable THEN
    eState := INIT;
    bSystemReady := FALSE;
    bExposureActive := FALSE;
    bExposureComplete := FALSE;
    bError := FALSE;
    nErrorCode := 0;
    fCmdVelocityX_m_s := 0.0;
    fCmdVelocityY_m_s := 0.0;
    bLaserTrigger := FALSE;
    RETURN;
END_IF;

CASE eState OF
    INIT:
        bSystemReady := TRUE;
        bExposureComplete := FALSE;
        IF bStartExposure THEN
            bSystemReady := FALSE;
            bExposureActive := TRUE;
            eState := ALIGN_RETICLE;
        END_IF;
        
    ALIGN_RETICLE:
        (* Reticle Alignment Loop - PI Control for nanometer positioning *)
        fCmdReticleX_nm := fCmdReticleX_nm + (fReticleErrorX_nm * 0.1);
        fCmdReticleY_nm := fCmdReticleY_nm + (fReticleErrorY_nm * 0.1);
        fCmdReticleTheta_urad := fCmdReticleTheta_urad + (fReticleErrorTheta_urad * 0.05);
        
        IF ABS(fReticleErrorX_nm) < 2.0 AND ABS(fReticleErrorY_nm) < 2.0 AND ABS(fReticleErrorTheta_urad) < 1.0 THEN
            eState := MOVE_STAGE;
        END_IF;
        
    MOVE_STAGE:
        (* Wafer Stage Interferometry Tracking - PD Control *)
        fStageErrorX := fTargetPosX_nm - fActualPosX_nm;
        fStageErrorY := fTargetPosY_nm - fActualPosY_nm;
        
        fCmdVelocityX_m_s := (fStageErrorX * fKp_Stage) + ((fStageErrorX - fPrevErrorX) * fKd_Stage);
        fCmdVelocityY_m_s := (fStageErrorY * fKp_Stage) + ((fStageErrorY - fPrevErrorY) * fKd_Stage);
        
        fPrevErrorX := fStageErrorX;
        fPrevErrorY := fStageErrorY;
        
        (* Velocity limit clamp *)
        IF fCmdVelocityX_m_s > 0.5 THEN fCmdVelocityX_m_s := 0.5; END_IF;
        IF fCmdVelocityX_m_s < -0.5 THEN fCmdVelocityX_m_s := -0.5; END_IF;
        IF fCmdVelocityY_m_s > 0.5 THEN fCmdVelocityY_m_s := 0.5; END_IF;
        IF fCmdVelocityY_m_s < -0.5 THEN fCmdVelocityY_m_s := -0.5; END_IF;
        
        IF ABS(fStageErrorX) < 1.5 AND ABS(fStageErrorY) < 1.5 THEN
            eState := SETTLE;
            fCmdVelocityX_m_s := 0.0;
            fCmdVelocityY_m_s := 0.0;
        END_IF;
        
    SETTLE:
        (* Allow mechanical vibrations to dampen *)
        tExposureTimer(IN:=TRUE, PT:=T#50MS);
        IF tExposureTimer.Q THEN
            tExposureTimer(IN:=FALSE);
            fAccumulatedDose_mJ := 0.0;
            nPulseCount := 0;
            nRequiredPulses := REAL_TO_DINT(fTargetDose_mJ / fNominalPulse_mJ);
            eState := EXPOSE;
        END_IF;
        
    EXPOSE:
        (* Excimer Laser Dose Control *)
        IF fAccumulatedDose_mJ < fTargetDose_mJ AND nPulseCount < nRequiredPulses THEN
            bLaserTrigger := TRUE;
            fAccumulatedDose_mJ := fAccumulatedDose_mJ + fNominalPulse_mJ; (* In reality, integrated from sensor *)
            nPulseCount := nPulseCount + 1;
        ELSE
            bLaserTrigger := FALSE;
            bExposureComplete := TRUE;
            bExposureActive := FALSE;
            eState := POST_EXPOSE;
        END_IF;
        
    POST_EXPOSE:
        IF NOT bStartExposure THEN
            eState := INIT;
        END_IF;
        
    ERROR:
        bError := TRUE;
        bLaserTrigger := FALSE;
        fCmdVelocityX_m_s := 0.0;
        fCmdVelocityY_m_s := 0.0;
        IF NOT bEnable THEN
            eState := INIT;
        END_IF;
        
END_CASE;
END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)
