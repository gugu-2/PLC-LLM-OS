import json, uuid, os
prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Advanced Semiconductor Extreme Ultraviolet (EUV) Mask Inspection**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Actinic wavelength 13.5nm scatterometry scanning, ultra-high vacuum (UHV) piezoresistive cantilever mapping, and stochastic defect pellicle thermal shielding). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_EUV_MaskInspection\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Advanced Semiconductor Extreme Ultraviolet (EUV) Mask Inspection

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_EUV_MaskInspection_Advanced
VAR_INPUT
    (* Core Enable and Safety Signals *)
    bEnable                 : BOOL;     (* System enable signal for the EUV mask inspection sequence *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal; MUST be TRUE to allow operation *)
    bVacuumInterlockOk      : BOOL;     (* Ultra-high vacuum (UHV) interlock status (TRUE = OK) *)
    
    (* Metrology and Sensor Inputs *)
    rActinicWavelength_nm   : LREAL;    (* Measured actinic wavelength, expected ~13.5 nm *)
    rPiezoCantileverDefl_nm : LREAL;    (* Piezoresistive cantilever deflection for UHV mapping *)
    rPellicleTemp_C         : REAL;     (* Stochastic defect pellicle thermal shielding temperature *)
    rScatterometrySignal    : LREAL;    (* EUV scatterometry scanning reflection intensity *)
    
    (* Positioning and Scan Parameters *)
    rStagePosX_um           : LREAL;    (* Current X-axis mask stage position *)
    rStagePosY_um           : LREAL;    (* Current Y-axis mask stage position *)
    bScanTrigger            : BOOL;     (* Trigger to initiate a local scatterometry scan *)
END_VAR
VAR_OUTPUT
    (* Status and Control Outputs *)
    bSystemReady            : BOOL;     (* TRUE when UHV, thermal, and source are stabilized *)
    bActiveScan             : BOOL;     (* TRUE when actively scanning and collecting scatterometry data *)
    bAlarm                  : BOOL;     (* Fault alarm output (e.g., vacuum loss, thermal excursion) *)
    iErrorCode              : INT;      (* Diagnostics error code (0 = No Error) *)
    
    (* Actuation and Correction *)
    rPiezoDriveV            : REAL;     (* Output voltage to drive the cantilever piezoactuator *)
    rPellicleCoolingFlow    : REAL;     (* Thermal shielding cooling gas flow setpoint (sccm) *)
    rDefectProbability      : REAL;     (* Calculated stochastic defect probability based on scatterometry *)
END_VAR
VAR
    (* Internal State and Timers *)
    iState                  : INT := 0;
    tUHVStabilization       : TON;
    tThermalControlLoop     : TON;
    tScanDwellTimer         : TON;
    
    (* Mathematical and Filtering Variables *)
    rFilteredScatterSignal  : LREAL := 0.0;
    rThermalError           : REAL := 0.0;
    rPrevCantileverDefl     : LREAL := 0.0;
    rDeflDerivative         : LREAL := 0.0;
    
    (* Constants *)
    c_rTargetWavelength     : LREAL := 13.5;
    c_rWavelengthTol        : LREAL := 0.05;
    c_rMaxPellicleTemp      : REAL := 85.0;
    c_rTargetPellicleTemp   : REAL := 22.0;
END_VAR

(* === MAIN LOGIC === *)
(* 1. Safety and Interlock Processing *)
IF NOT bEmergencyStop OR NOT bVacuumInterlockOk THEN
    bSystemReady := FALSE;
    bActiveScan := FALSE;
    bAlarm := TRUE;
    iErrorCode := 1000; (* Critical Safety or Vacuum Interlock Failure *)
    rPiezoDriveV := 0.0;
    rPellicleCoolingFlow := 100.0; (* Maximum cooling on fault *)
    iState := 0;
    RETURN;
END_IF;

(* 2. Pellicle Thermal Shielding Control (Proportional Control) *)
rThermalError := rPellicleTemp_C - c_rTargetPellicleTemp;
IF rPellicleTemp_C > c_rMaxPellicleTemp THEN
    bAlarm := TRUE;
    iErrorCode := 2000; (* Pellicle Thermal Excursion *)
    rPellicleCoolingFlow := 100.0;
    iState := 0; (* Abort operations *)
ELSE
    (* Simple P-controller for cooling gas flow *)
    IF rThermalError > 0.0 THEN
        rPellicleCoolingFlow := LIMIT(10.0, rThermalError * 2.5, 100.0);
    ELSE
        rPellicleCoolingFlow := 10.0; (* Idle minimum flow *)
    END_IF;
END_IF;

(* 3. Main State Machine for Inspection Sequence *)
CASE iState OF
    0: (* IDLE & INITIALIZATION *)
        bSystemReady := FALSE;
        bActiveScan := FALSE;
        rPiezoDriveV := 0.0;
        
        IF bEnable AND (iErrorCode = 0 OR iErrorCode = 1000) THEN
            iErrorCode := 0;
            bAlarm := FALSE;
            iState := 10;
        END_IF;

    10: (* UHV AND SOURCE STABILIZATION *)
        (* Wait for vacuum and wavelength stabilization *)
        tUHVStabilization(IN := TRUE, PT := T#10S);
        
        IF tUHVStabilization.Q THEN
            IF ABS(rActinicWavelength_nm - c_rTargetWavelength) < c_rWavelengthTol THEN
                tUHVStabilization(IN := FALSE);
                bSystemReady := TRUE;
                iState := 20;
            ELSE
                bAlarm := TRUE;
                iErrorCode := 3000; (* Source Wavelength out of tolerance *)
                tUHVStabilization(IN := FALSE);
                iState := 0;
            END_IF;
        END_IF;

    20: (* READY FOR INSPECTION *)
        bSystemReady := TRUE;
        IF bScanTrigger AND bEnable THEN
            bActiveScan := TRUE;
            rFilteredScatterSignal := rScatterometrySignal; (* Initialize filter *)
            rPrevCantileverDefl := rPiezoCantileverDefl_nm;
            iState := 30;
        END_IF;
        
        IF NOT bEnable THEN
            iState := 0;
        END_IF;

    30: (* ACTIVE SCATTEROMETRY & CANTILEVER MAPPING SCAN *)
        (* Low-pass filter for the actinic 13.5nm scatterometry signal *)
        rFilteredScatterSignal := (rFilteredScatterSignal * 0.8) + (rScatterometrySignal * 0.2);
        
        (* Calculate deflection derivative for dynamic topography estimation *)
        rDeflDerivative := rPiezoCantileverDefl_nm - rPrevCantileverDefl;
        rPrevCantileverDefl := rPiezoCantileverDefl_nm;
        
        (* Adjust Piezo Drive Voltage based on deflection to maintain constant force (Closed Loop) *)
        rPiezoDriveV := LIMIT(-10.0, rPiezoDriveV - LREAL_TO_REAL(rPiezoCantileverDefl_nm * 0.05 + rDeflDerivative * 0.01), 10.0);
        
        (* Stochastic defect probability estimation based on local scatter loss *)
        IF rFilteredScatterSignal < 0.5 THEN
            rDefectProbability := LREAL_TO_REAL((0.5 - rFilteredScatterSignal) * 200.0);
        ELSE
            rDefectProbability := 0.0;
        END_IF;
        
        (* Dwell timer for localized scanning step *)
        tScanDwellTimer(IN := TRUE, PT := T#250MS);
        IF tScanDwellTimer.Q THEN
            tScanDwellTimer(IN := FALSE);
            bActiveScan := FALSE;
            iState := 20; (* Return to ready, waiting for next trigger/position *)
        END_IF;
        
        (* Abort scan if enable is lost *)
        IF NOT bEnable THEN
            tScanDwellTimer(IN := FALSE);
            bActiveScan := FALSE;
            iState := 0;
        END_IF;

    ELSE
        (* Failsafe state *)
        iState := 0;
END_CASE;

END_FUNCTION_BLOCK
```"""
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
