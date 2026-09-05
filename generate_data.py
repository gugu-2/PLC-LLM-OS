import json, uuid, os
prompt = """<USER_REQUEST>
You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Deep-Sea Acoustic Doppler Current Profiler (ADCP) Calibration Tank**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Transducer multi-frequency chirped acoustic generation, anechoic test tank multi-axis robotic carriage synchronization, and phased-array beamforming mapping). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_ADCP_CalibrationTank\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Deep-Sea Acoustic Doppler Current Profiler (ADCP) Calibration Tank

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT.
</USER_REQUEST>"""

code = """```iec-st
FUNCTION_BLOCK FB_ADCP_Calibration_Tank
VAR_INPUT
    (* Required: at least 4-8 physical inputs with types and comments *)
    bSystemEnable           : BOOL;     (* Main system enable interlock *)
    bEstopSafetyRelay       : BOOL;     (* Safety relay OK / E-Stop circuit healthy *)
    rTankTemperature        : REAL;     (* Water temperature in anechoic tank (deg C) *)
    rTankSalinity           : REAL;     (* Water salinity in PSU (Practical Salinity Unit) *)
    rCarriagePosX           : LREAL;    (* Multi-axis carriage X position (meters) *)
    rCarriagePosY           : LREAL;    (* Multi-axis carriage Y position (meters) *)
    rCarriagePosZ           : LREAL;    (* Multi-axis carriage Z position (meters) *)
    rAcousticRefInput       : REAL;     (* Reference hydrophone acoustic pressure input (Pa) *)
END_VAR
VAR_OUTPUT
    (* Required: at least 3-6 outputs with types and comments *)
    bSystemReady            : BOOL;     (* System is initialized and ready for acoustic sweep *)
    bCalibrationActive      : BOOL;     (* Calibration sequence is actively running *)
    rCalculatedSoundSpeed   : REAL;     (* Calculated speed of sound in water (m/s) based on Temp/Salinity *)
    rTxDriveVoltage         : REAL;     (* Output drive voltage for ADCP transducer array (V) *)
    rTxDriveFrequency       : REAL;     (* Output frequency for chirped acoustic generation (Hz) *)
    bErrorFault             : BOOL;     (* General fault or error state *)
    iErrorCode              : INT;      (* Specific fault code for diagnostics *)
END_VAR
VAR
    (* Internal state variables *)
    iSeqState               : INT := 0; 
    tStabilizeTimer         : TON;
    tChirpTimer             : TON;
    
    (* Kinematics and Acoustic variables *)
    rTargetX                : LREAL := 0.0;
    rTargetY                : LREAL := 0.0;
    rTargetZ                : LREAL := -2.5; (* Default submersion depth *)
    rTolerance              : LREAL := 0.005;
    
    rBaseFreq               : REAL := 300000.0; (* 300 kHz base frequency *)
    rFreqSweepBand          : REAL := 25000.0;  (* +/- 25 kHz sweep *)
END_VAR

(* === MAIN LOGIC === *)
(* Immediate safety interlock check *)
IF NOT bEstopSafetyRelay THEN
    bSystemReady := FALSE;
    bCalibrationActive := FALSE;
    bErrorFault := TRUE;
    iErrorCode := 999; (* 999: Emergency Stop Active *)
    rTxDriveVoltage := 0.0;
    rTxDriveFrequency := 0.0;
    RETURN;
END_IF;

(* Clear error if system is disabled normally without estop *)
IF NOT bSystemEnable AND NOT bErrorFault THEN
    iSeqState := 0;
END_IF;

(* Environmental Calculations: Chen-Millero Speed of Sound in Seawater Approx *)
(* Simplified for PLC execution context, typical valid range for calibration tank *)
rCalculatedSoundSpeed := 1449.2 + (4.6 * rTankTemperature) - (0.055 * (rTankTemperature * rTankTemperature)) + (0.00029 * (rTankTemperature * rTankTemperature * rTankTemperature)) + (1.34 - 0.01 * rTankTemperature) * (rTankSalinity - 35.0) + 0.016 * 2.5;

CASE iSeqState OF
    0: (* IDLE & STANDBY *)
        bSystemReady := FALSE;
        bCalibrationActive := FALSE;
        bErrorFault := FALSE;
        iErrorCode := 0;
        rTxDriveVoltage := 0.0;
        
        IF bSystemEnable THEN
            iSeqState := 10; (* Transition to Initialization *)
        END_IF;

    10: (* INITIALIZATION & POSITIONING *)
        (* Wait for multi-axis carriage to reach target center coordinates *)
        IF (ABS(rCarriagePosX - rTargetX) < rTolerance) AND 
           (ABS(rCarriagePosY - rTargetY) < rTolerance) AND 
           (ABS(rCarriagePosZ - rTargetZ) < rTolerance) THEN
            
            tStabilizeTimer(IN := TRUE, PT := T#10S);
            IF tStabilizeTimer.Q THEN
                tStabilizeTimer(IN := FALSE);
                bSystemReady := TRUE;
                iSeqState := 20; (* Ready for Sweep *)
            END_IF;
        ELSE
            tStabilizeTimer(IN := FALSE);
        END_IF;

    20: (* READY FOR CALIBRATION SWEEP *)
        IF bSystemEnable THEN
            bCalibrationActive := TRUE;
            tChirpTimer(IN := TRUE, PT := T#2S);
            iSeqState := 30;
        END_IF;
        
    30: (* CHIRP GENERATION & BEAMFORMING MAPPING *)
        (* Generate a linear frequency chirp *)
        IF tChirpTimer.IN THEN
            (* Scale frequency over the 2-second timer *)
            rTxDriveFrequency := rBaseFreq - rFreqSweepBand + ((rFreqSweepBand * 2.0) * (TIME_TO_REAL(tChirpTimer.ET) / 2000.0));
            rTxDriveVoltage := 48.0; (* 48V Drive for ADCP *)
        END_IF;
        
        IF tChirpTimer.Q THEN
            tChirpTimer(IN := FALSE);
            rTxDriveVoltage := 0.0;
            bCalibrationActive := FALSE;
            iSeqState := 20; (* Return to ready *)
        END_IF;

    ELSE
        (* Invalid state fallback *)
        iSeqState := 0;
        bErrorFault := TRUE;
        iErrorCode := 500; (* State machine fault *)
END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": code}
    ]
}
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
