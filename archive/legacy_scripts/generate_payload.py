import json, uuid
import os

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Automated Gigafactory EV Battery Pack Laser Welding Gantry**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Galvanometric mirror 3D weld seam tracking, continuous wave (CW) fiber laser optical back-reflection isolation, and argon shielding gas laminar flow mapping). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_EV_LaserWeldingGantry\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Automated Gigafactory EV Battery Pack Laser Welding Gantry

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_EV_LaserWeldingGantry
(* ====================================================================================
   Module:        FB_EV_LaserWeldingGantry
   Author:        Lumina Elite Synthetic Data Architect (40+ Yr Automation Veteran)
   Description:   Advanced Galvanometric 3D Seam Tracking & Continuous Wave (CW) 
                  Fiber Laser Control for EV Battery Pack Assembly. Integrates
                  optical back-reflection isolation and laminar argon flow mapping.
   Version:       3.14.159 - Production Validated
   ==================================================================================== *)
VAR_INPUT
    (* System & Safety Inputs *)
    bEnableSystem         : BOOL;     (* System master enable signal from Main PLC *)
    bEmergencyStop        : BOOL;     (* Safety relay OK / E-Stop loop closed (1=Safe) *)
    bResetAlarms          : BOOL;     (* Operator alarm reset push button *)
    
    (* Laser Processing Parameters *)
    rLaserPowerCmd        : REAL;     (* Commanded CW laser power in kW (Range: 0.0 to 8.0 kW) *)
    rSeamTrackTargetX     : REAL;     (* Galvo X-axis position target in mm (Absolute) *)
    rSeamTrackTargetY     : REAL;     (* Galvo Y-axis position target in mm (Absolute) *)
    rSeamTrackTargetZ     : REAL;     (* Galvo Z-axis focal depth in mm (Absolute) *)
    rWeldSpeedCmd         : REAL;     (* Welding trajectory speed in mm/s *)
    
    (* Shielding & Optical Sensors *)
    rArgonFlowRate        : REAL;     (* Shielding gas flow rate setpoint in L/min *)
    bBackReflectionHigh   : BOOL;     (* Optical isolator back-reflection alarm from laser source *)
    bPlasmaPlumeDetect    : BOOL;     (* Weld pool plasma emission detector for seam tracking loop *)
END_VAR

VAR_OUTPUT
    (* System Status *)
    bSystemReady          : BOOL;     (* Gantry and Laser system ready for emission phase *)
    bLaserEmission        : BOOL;     (* Active laser emission indicator (Hardware interlocked) *)
    bArgonFlowOK          : BOOL;     (* Laminar argon flow mapped and verified within tolerances *)
    bTrackingActive       : BOOL;     (* Real-time 3D galvanometric tracking is active *)
    
    (* Telemetry *)
    rLaserPowerActual     : REAL;     (* Actual measured laser power delivered to workpiece in kW *)
    rCurrentGalvoX        : REAL;     (* Real-time X position feedback (mm) *)
    rCurrentGalvoY        : REAL;     (* Real-time Y position feedback (mm) *)
    rCurrentGalvoZ        : REAL;     (* Real-time Z position feedback (mm) *)
    
    (* Alarms & Diagnostics *)
    bAlarm                : BOOL;     (* General fault or safety interlock broken *)
    wErrorCode            : WORD;     (* Detailed error code for HMI diagnostics *)
END_VAR

VAR
    (* Internal State & Timers *)
    iState                : INT := 0;      (* Main execution state machine step index *)
    tGasPreFlow           : TON;           (* Purge delay timer before laser emission *)
    tWeldTimer            : TON;           (* Maximum weld duration timeout *)
    tGasPostFlow          : TON;           (* Shielding pool cooling timer post-weld *)
    
    (* Control Loop Variables *)
    rPositionError        : REAL := 0.0;   (* Dynamic tracking error for PID *)
    rIntegrator           : REAL := 0.0;   (* Integral accumulator for depth control *)
    rKp                   : REAL := 1.25;  (* Proportional gain for galvo tracking *)
    rKi                   : REAL := 0.05;  (* Integral gain for depth stability *)
    bOpticalLockout       : BOOL := FALSE; (* Latch for catastrophic optical damage prevention *)
END_VAR

(* === CRITICAL SAFETY INTERLOCKS === *)
IF NOT bEmergencyStop THEN
    bSystemReady      := FALSE;
    bLaserEmission    := FALSE;
    bTrackingActive   := FALSE;
    bAlarm            := TRUE;
    wErrorCode        := 16#F001; (* F001: Critical E-Stop Loop Open *)
    iState            := 999;     (* Jump to fatal error state *)
    rLaserPowerActual := 0.0;
    RETURN;
END_IF;

(* Back-Reflection Hardware Protection (10 microsecond response requirement simulated) *)
IF bBackReflectionHigh AND bLaserEmission THEN
    bSystemReady      := FALSE;
    bLaserEmission    := FALSE;
    bAlarm            := TRUE;
    bOpticalLockout   := TRUE;
    wErrorCode        := 16#E002; (* E002: Catastrophic Optical Back-Reflection Threshold Exceeded! *)
    iState            := 999;
    RETURN;
END_IF;

(* === RESET LOGIC === *)
IF bResetAlarms AND NOT bOpticalLockout THEN
    bAlarm := FALSE;
    wErrorCode := 16#0000;
    IF iState = 999 THEN
        iState := 0;
    END_IF;
END_IF;

(* === STATE MACHINE EXECUTOR === *)
CASE iState OF
    0: (* ST_IDLE: Wait for master enable *)
        bSystemReady      := TRUE;
        bLaserEmission    := FALSE;
        bTrackingActive   := FALSE;
        rLaserPowerActual := 0.0;
        tGasPreFlow(IN := FALSE);
        tWeldTimer(IN := FALSE);
        tGasPostFlow(IN := FALSE);
        
        IF bEnableSystem AND NOT bAlarm THEN
            bSystemReady := FALSE;
            iState := 10;
        END_IF;

    10: (* ST_POSITIONING_AND_PREFLOW: Move to start and establish laminar argon shield *)
        (* PID loop simulation for Z-axis seam depth tracking *)
        rPositionError := rSeamTrackTargetZ - rCurrentGalvoZ;
        rIntegrator := rIntegrator + (rPositionError * rKi);
        rCurrentGalvoZ := rCurrentGalvoZ + (rPositionError * rKp) + rIntegrator;
        
        (* X/Y fast traverse *)
        rCurrentGalvoX := rSeamTrackTargetX;
        rCurrentGalvoY := rSeamTrackTargetY;
        bTrackingActive := TRUE;

        (* Verify argon laminar flow map bounds *)
        IF rArgonFlowRate >= 18.5 AND rArgonFlowRate <= 22.0 THEN
            bArgonFlowOK := TRUE;
            tGasPreFlow(IN := TRUE, PT := T#2500MS);
        ELSE
            bArgonFlowOK := FALSE;
            tGasPreFlow(IN := FALSE);
        END_IF;

        IF tGasPreFlow.Q AND bArgonFlowOK AND (ABS(rPositionError) < 0.05) THEN
            tGasPreFlow(IN := FALSE);
            iState := 20;
        END_IF;

    20: (* ST_WELD_EMISSION: Active laser operation with plasma feedback *)
        bLaserEmission := TRUE;
        (* Modulate power slightly based on plasma plume stability *)
        IF bPlasmaPlumeDetect THEN
            rLaserPowerActual := rLaserPowerCmd * 0.99; (* Stable pool, minimal scatter loss *)
        ELSE
            rLaserPowerActual := rLaserPowerCmd * 1.05; (* Push power to penetrate oxidation layer *)
        END_IF;
        
        tWeldTimer(IN := TRUE, PT := T#3500MS); (* Max seam duration per pulse/segment *)
        
        (* Check for premature system disable *)
        IF NOT bEnableSystem THEN
            tWeldTimer(IN := FALSE);
            iState := 30;
        END_IF;

        IF tWeldTimer.Q THEN
            tWeldTimer(IN := FALSE);
            iState := 30;
        END_IF;

    30: (* ST_POSTFLOW: Laser off, cool weld pool with argon to prevent oxidation *)
        bLaserEmission    := FALSE;
        rLaserPowerActual := 0.0;
        bTrackingActive   := FALSE;
        
        tGasPostFlow(IN := TRUE, PT := T#5S);
        IF tGasPostFlow.Q THEN
            tGasPostFlow(IN := FALSE);
            iState := 0; (* Cycle complete, return to idle *)
        END_IF;

    999: (* ST_ERROR_TRAP: System halted, awaiting operator intervention *)
        bLaserEmission    := FALSE;
        bTrackingActive   := FALSE;
        bSystemReady      := FALSE;
        rLaserPowerActual := 0.0;
        tGasPreFlow(IN := FALSE);
        tWeldTimer(IN := FALSE);
        tGasPostFlow(IN := FALSE);
        
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
