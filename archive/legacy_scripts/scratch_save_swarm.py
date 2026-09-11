import json, uuid, os

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Deep-Space Optical Communication Laser Downlink Gimbal**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., 10-microradian piezo fast steering mirror (FSM) jitter cancellation, photon-counting avalanche photodiode phase tracking, and atmospheric turbulence adaptive optics wavefront correction). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

CRITICAL RULES - READ EVERY LINE:
1. CODE FENCE: Use TRIPLE backticks + iec-st. EXACTLY like this:
   ```iec-st
   (your code here)
   ```
   NEVER use a single backtick `iec-st. ALWAYS use triple backticks.
2. REQUIRED IEC 61131-3 STRUCTURE (all 5 mandatory):
   a. FUNCTION_BLOCK FB_<Name>   <- first line of code, always
   b. VAR_INPUT ... END_VAR      <- min 4 typed inputs with comments
   c. VAR_OUTPUT ... END_VAR     <- min 3 typed outputs with comments
   d. At least one END_IF; or END_CASE;  <- control logic required
   e. END_FUNCTION_BLOCK         <- last line of code, always
3. LENGTH: The assistant content MUST be >= 1500 characters total.
4. SAVE to isolated file using this exact Python:
   import json, uuid
   prompt = \"\"\"<copy this exact user prompt here>\"\"\"
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_OpticalCommsGimbal\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
   record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
   with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
       json.dump(record, f, ensure_ascii=False)
5. SELF-CHECK before saving - verify ALL:
   [ ] Fence is ```iec-st
   [ ] First code line: FUNCTION_BLOCK FB_<name>
   [ ] Has VAR_INPUT section
   [ ] Has VAR_OUTPUT section
   [ ] Has END_IF; or END_CASE;
   [ ] Last code line: END_FUNCTION_BLOCK
   [ ] Closing fence: ```
   [ ] Total chars >= 1500
6. REPLY with: EVOLUTION COMPLETE: Deep-Space Optical Communication Laser Downlink Gimbal

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_DeepSpaceOptCommsGimbal
(*
    =========================================================================
    FB Name       : FB_DeepSpaceOptCommsGimbal
    Description   : Advanced Fast Steering Mirror (FSM) and Adaptive Optics (AO)
                    wavefront correction for deep-space laser downlink.
                    Implements 10-urad jitter cancellation and photon-counting
                    avalanche photodiode (APD) phase tracking.
    Author        : Lumina AI Cloud Swarm
    Version       : 1.0.0
    =========================================================================
*)
VAR_INPUT
    bEnable                 : BOOL;   (* System enable signal / start tracking *)
    bEmergencyStop          : BOOL;   (* Safety interlock / Emergency Stop (Active High means OK) *)
    rAPD_PhaseError_rad     : LREAL;  (* Phase error from photon-counting APD array [radians] *)
    rWavefrontError_rms     : LREAL;  (* RMS wavefront error from Shack-Hartmann sensor [nm] *)
    rMacroAzimuth_urad      : LREAL;  (* Macro gimbal azimuth feedback [microradians] *)
    rMacroElevation_urad    : LREAL;  (* Macro gimbal elevation feedback [microradians] *)
END_VAR

VAR_OUTPUT
    bSystemReady            : BOOL;   (* System initialized, calibrated, and ready *)
    bTrackingActive         : BOOL;   (* Locked on and actively tracking *)
    bAlarm                  : BOOL;   (* Tracking loss or fault condition detected *)
    rFsmAzimuthDrive_V      : LREAL;  (* FSM Piezo Azimuth Drive Command [Volts] *)
    rFsmElevationDrive_V    : LREAL;  (* FSM Piezo Elevation Drive Command [Volts] *)
    rDeformableMirrorStroke : LREAL;  (* Actuator global stroke for wavefront correction [nm] *)
END_VAR

VAR
    iState                  : INT := 0;      (* Internal State Machine variable *)
    tLockTimer              : TON;           (* Timer for phase lock validation *)
    tFaultDelay             : TON;           (* Timer for transient fault rejection *)
    
    (* Internal PID variables for Jitter Cancellation (10-urad goal) *)
    rKp_FSM                 : LREAL := 0.15;
    rKi_FSM                 : LREAL := 0.05;
    rKd_FSM                 : LREAL := 0.005;
    rIntegralAzimuth        : LREAL := 0.0;
    rIntegralElevation      : LREAL := 0.0;
    rLastErrorAzimuth       : LREAL := 0.0;
    rLastErrorElevation     : LREAL := 0.0;
    
    (* Filter Constants *)
    rAlpha                  : LREAL := 0.85; (* First-order low-pass filter coefficient *)
    rFilteredPhaseError     : LREAL := 0.0;
END_VAR

(* === MAIN LOGIC === *)
(* 1. Safety and Hardware Interlock Processing *)
IF NOT bEmergencyStop THEN
    (* Immediate shutdown on E-Stop / Safety loop open *)
    bSystemReady            := FALSE;
    bTrackingActive         := FALSE;
    bAlarm                  := TRUE;
    iState                  := 999; (* Fault State *)
    rFsmAzimuthDrive_V      := 0.0;
    rFsmElevationDrive_V    := 0.0;
    rDeformableMirrorStroke := 0.0;
    RETURN;
END_IF;

(* 2. Adaptive Optics Wavefront Correction (Continuous background task) *)
(* Converts SH-sensor RMS error into raw stroke for Deformable Mirror (DM) array *)
IF bEnable AND iState >= 20 THEN
    rDeformableMirrorStroke := rWavefrontError_rms * 1.05; (* Simplified adaptive gain matrix logic *)
    
    (* Cap stroke to physical DM limits *)
    IF rDeformableMirrorStroke > 5000.0 THEN
        rDeformableMirrorStroke := 5000.0;
    ELSIF rDeformableMirrorStroke < -5000.0 THEN
        rDeformableMirrorStroke := -5000.0;
    END_IF;
ELSE
    rDeformableMirrorStroke := 0.0;
END_IF;

(* 3. Gimbal Control State Machine *)
CASE iState OF
    0: (* IDLE & INITIALIZATION *)
        bSystemReady := TRUE;
        bTrackingActive := FALSE;
        bAlarm := FALSE;
        
        rIntegralAzimuth := 0.0;
        rIntegralElevation := 0.0;
        
        IF bEnable THEN
            iState := 10;
        END_IF;

    10: (* MACRO ACQUISITION *)
        (* Await macro positioning to get within Fast Steering Mirror capture range *)
        bSystemReady := TRUE;
        bTrackingActive := FALSE;
        
        IF ABS(rMacroAzimuth_urad) < 500.0 AND ABS(rMacroElevation_urad) < 500.0 THEN
            (* Target is within FSM optical field of view *)
            iState := 20;
        END_IF;
        
        IF NOT bEnable THEN
            iState := 0;
        END_IF;

    20: (* PHASE LOCKING & FSM JITTER CANCELLATION *)
        bSystemReady := TRUE;
        bTrackingActive := TRUE;
        
        (* Low-pass filter the photon-counting APD array phase error *)
        rFilteredPhaseError := (rAlpha * rFilteredPhaseError) + ((1.0 - rAlpha) * rAPD_PhaseError_rad);
        
        (* Evaluate Phase lock threshold for tracking stability (e.g., 0.1 rad tolerance) *)
        tLockTimer(IN := ABS(rFilteredPhaseError) < 0.1, PT := T#2S);
        
        (* If phase lock is lost for an extended period, transition to fault/reacquisition *)
        tFaultDelay(IN := ABS(rFilteredPhaseError) > 0.5, PT := T#1S);
        IF tFaultDelay.Q THEN
            tFaultDelay(IN := FALSE);
            bTrackingActive := FALSE;
            iState := 30;
        END_IF;
        
        (* FSM Jitter Cancellation PID loop (simplified representation)
           Normally this runs at 10+ kHz. This computes the corrective control voltage. *)
        rIntegralAzimuth := rIntegralAzimuth + (rFilteredPhaseError * rKi_FSM);
        rFsmAzimuthDrive_V := (rFilteredPhaseError * rKp_FSM) + rIntegralAzimuth + ((rFilteredPhaseError - rLastErrorAzimuth) * rKd_FSM);
        rLastErrorAzimuth := rFilteredPhaseError;
        
        (* Clamp outputs to DAC range limits +/- 10 Volts *)
        IF rFsmAzimuthDrive_V > 10.0 THEN
            rFsmAzimuthDrive_V := 10.0;
        ELSIF rFsmAzimuthDrive_V < -10.0 THEN
            rFsmAzimuthDrive_V := -10.0;
        END_IF;
        
        IF NOT bEnable THEN
            iState := 0;
        END_IF;
        
    30: (* LOSS OF SIGNAL RECOVERY *)
        bSystemReady := TRUE;
        bTrackingActive := FALSE;
        bAlarm := TRUE;
        
        (* Soft-reset FSM integrator *)
        rIntegralAzimuth := rIntegralAzimuth * 0.95;
        rFsmAzimuthDrive_V := 0.0;
        rFsmElevationDrive_V := 0.0;
        
        (* Attempt to reacquire once macro pointing is stabilized *)
        IF ABS(rMacroAzimuth_urad) < 200.0 AND ABS(rMacroElevation_urad) < 200.0 AND bEnable THEN
            bAlarm := FALSE;
            iState := 10;
        END_IF;
        
        IF NOT bEnable THEN
            iState := 0;
        END_IF;
        
    999: (* HARD FAULT STATE *)
        bSystemReady := FALSE;
        bTrackingActive := FALSE;
        bAlarm := TRUE;
        
        (* Wait for operator reset (bEnable toggle + E-Stop cleared) *)
        IF NOT bEnable AND bEmergencyStop THEN
            iState := 0;
        END_IF;
        
END_CASE;

END_FUNCTION_BLOCK
```"""

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": code}
    ]
}

filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
