import os, json, uuid
os.makedirs("data/swarm_raw", exist_ok=True)
prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Advanced Metrology Atomic Force Microscope (AFM) Piezo Actuator**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Sub-nanometer piezoelectric Z-axis extension tunneling current feedback, thermal drift active compensation, and high-frequency XY raster scan trajectory generation). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_AFM_PiezoActuator\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Advanced Metrology Atomic Force Microscope (AFM) Piezo Actuator

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_AFM_PiezoActuator_NanoControl
(* 
   ========================================================================
   Advanced Metrology Atomic Force Microscope (AFM) Piezo Actuator
   Sub-nanometer Z-axis extension tunneling current feedback, 
   thermal drift active compensation, and high-frequency XY raster scan
   ========================================================================
*)
VAR_INPUT
    bEnableSystem          : BOOL;     (* System master enable *)
    bEmergencyStop         : BOOL;     (* Safety interlock / limit switch OK *)
    rTunnelingCurrent      : LREAL;    (* Measured tunneling current (pA) *)
    rTargetCurrentSetpoint : LREAL;    (* Target tunneling current setpoint (pA) *)
    rAmbientTemperature    : LREAL;    (* Measured ambient temperature for drift comp (deg C) *)
    rRasterScanRate        : LREAL;    (* XY raster scan speed (Hz) *)
    rRasterScanSizeX       : LREAL;    (* X-axis scan dimension (nm) *)
    rRasterScanSizeY       : LREAL;    (* Y-axis scan dimension (nm) *)
END_VAR
VAR_OUTPUT
    bSystemReady           : BOOL;     (* Control loop stabilized and ready *)
    rPiezoDriveZ           : LREAL;    (* Z-axis piezo drive voltage (V) *)
    rPiezoDriveX           : LREAL;    (* X-axis piezo drive voltage (V) *)
    rPiezoDriveY           : LREAL;    (* Y-axis piezo drive voltage (V) *)
    bScanActive            : BOOL;     (* XY raster scan in progress *)
    bTrackingErrorAlarm    : BOOL;     (* Z-axis tracking error exceeds tolerance limit *)
END_VAR
VAR
    iState                 : INT := 0; (* Internal state machine *)
    rCurrentError          : LREAL;    (* Tunneling current error *)
    rIntegralTerm          : LREAL := 0.0;
    rProportionalTerm      : LREAL := 0.0;
    rDerivativeTerm        : LREAL := 0.0;
    rPrevCurrentError      : LREAL := 0.0;
    
    (* PID tuning parameters for Sub-nanometer Z-axis extension *)
    rKp                    : LREAL := 0.005;
    rKi                    : LREAL := 0.015;
    rKd                    : LREAL := 0.0001;
    
    (* Thermal Drift Compensation *)
    rBaseTemp              : LREAL := 22.0; (* Reference temp in deg C *)
    rThermalCoeff          : LREAL := 0.045; (* nm/degC drift *)
    rThermalOffsetZ        : LREAL := 0.0;
    
    (* Raster Scan Variables *)
    rScanPhaseX            : LREAL := 0.0;
    rScanPhaseY            : LREAL := 0.0;
    rVoltageFactor         : LREAL := 0.1; (* V/nm piezo constant *)
    
    tCycleTimer            : TON;
    tSampleTime            : TIME := T#1MS;
    rSampleTimeSec         : LREAL := 0.001;
END_VAR

(* === MAIN LOGIC === *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bScanActive := FALSE;
    bTrackingErrorAlarm := TRUE;
    rPiezoDriveZ := 0.0;
    rPiezoDriveX := 0.0;
    rPiezoDriveY := 0.0;
    iState := 0;
    RETURN;
END_IF;

(* Active Thermal Drift Compensation *)
rThermalOffsetZ := (rAmbientTemperature - rBaseTemp) * rThermalCoeff;

CASE iState OF
    0: (* INIT / IDLE *)
        bSystemReady := FALSE;
        bScanActive := FALSE;
        bTrackingErrorAlarm := FALSE;
        rIntegralTerm := 0.0;
        rPiezoDriveZ := 0.0;
        
        IF bEnableSystem THEN
            iState := 10;
        END_IF;

    10: (* APPROACH AND ENGAGE (Z-Axis PID) *)
        rCurrentError := rTargetCurrentSetpoint - rTunnelingCurrent;
        rProportionalTerm := rKp * rCurrentError;
        rIntegralTerm := rIntegralTerm + (rKi * rCurrentError * rSampleTimeSec);
        rDerivativeTerm := rKd * (rCurrentError - rPrevCurrentError) / rSampleTimeSec;
        rPrevCurrentError := rCurrentError;
        
        (* Calculate Drive Z with thermal compensation *)
        rPiezoDriveZ := rProportionalTerm + rIntegralTerm + rDerivativeTerm + rThermalOffsetZ;
        
        (* Saturate Piezo Z Drive Voltage limits [-150V to +150V] *)
        IF rPiezoDriveZ > 150.0 THEN
            rPiezoDriveZ := 150.0;
        ELSIF rPiezoDriveZ < -150.0 THEN
            rPiezoDriveZ := -150.0;
        END_IF;
        
        (* Check if locked / converged *)
        IF ABS(rCurrentError) < 0.1 THEN
            bSystemReady := TRUE;
            iState := 20;
        ELSE
            bSystemReady := FALSE;
        END_IF;
        
        IF ABS(rCurrentError) > 5.0 THEN
            bTrackingErrorAlarm := TRUE;
        ELSE
            bTrackingErrorAlarm := FALSE;
        END_IF;
        
    20: (* RASTER SCAN ACTIVE *)
        bScanActive := TRUE;
        
        (* Maintain Z-feedback *)
        rCurrentError := rTargetCurrentSetpoint - rTunnelingCurrent;
        rIntegralTerm := rIntegralTerm + (rKi * rCurrentError * rSampleTimeSec);
        rPiezoDriveZ := (rKp * rCurrentError) + rIntegralTerm + rThermalOffsetZ;
        
        (* Generate XY Trajectories *)
        rScanPhaseX := rScanPhaseX + (rRasterScanRate * rSampleTimeSec);
        IF rScanPhaseX > 1.0 THEN
            rScanPhaseX := 0.0;
            rScanPhaseY := rScanPhaseY + (1.0 / (rRasterScanSizeY + 1.0));
            IF rScanPhaseY > 1.0 THEN
                rScanPhaseY := 0.0;
            END_IF;
        END_IF;
        
        (* Triangle wave for X, Ramp for Y *)
        IF rScanPhaseX < 0.5 THEN
            rPiezoDriveX := (rScanPhaseX * 2.0) * rRasterScanSizeX * rVoltageFactor;
        ELSE
            rPiezoDriveX := (2.0 - (rScanPhaseX * 2.0)) * rRasterScanSizeX * rVoltageFactor;
        END_IF;
        
        rPiezoDriveY := rScanPhaseY * rRasterScanSizeY * rVoltageFactor;
        
        IF NOT bEnableSystem THEN
            iState := 0;
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
```"""
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
