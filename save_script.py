import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Semiconductor Extreme Ultraviolet (EUV) Droplet Generator**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., 50kHz molten tin droplet laser-plasma targeting synchronization, high-vacuum droplet catcher temperature stabilization, and optical debris mitigation buffer gas control). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_EUV_DropletGenerator\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Semiconductor Extreme Ultraviolet (EUV) Droplet Generator

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_EUV_DropletGenerator
VAR_INPUT
    (* High-frequency trigger and synchronization *)
    bSystemEnable       : BOOL;     (* Main system enable for EUV droplet generation *)
    bSafetyInterlockOK  : BOOL;     (* High-vacuum and laser safety interlock status *)
    rTinMeltTempActual  : REAL;     (* Actual temperature of molten tin reservoir [deg C] *)
    rDropletFreqCmd     : REAL;     (* Commanded droplet frequency, typically 50.0 kHz *)
    rChamberVacuumActual: REAL;     (* Actual vacuum pressure in the source chamber [mbar] *)
    rBufferGasFlowActual: REAL;     (* Optical debris mitigation buffer gas flow rate [slm] *)
    rLaserTargetSyncPos : REAL;     (* Real-time laser targeting synchronization position error [um] *)
    bLaserPlasmaReady   : BOOL;     (* Laser plasma source readiness indicator *)
END_VAR
VAR_OUTPUT
    (* Droplet and system control outputs *)
    bSystemReady        : BOOL;     (* Droplet generator is stable and ready for laser pulsing *)
    rPiezoDriveVolts    : REAL;     (* Piezoelectric actuator drive voltage [V] for droplet formation *)
    rTinHeaterPower     : REAL;     (* Commanded power to the tin reservoir heater [0.0 - 100.0 %] *)
    rCatcherTempSetpt   : REAL;     (* Setpoint for the droplet catcher stabilization [deg C] *)
    bDropletSyncValid   : BOOL;     (* Valid droplet targeting synchronization achieved *)
    bCriticalAlarm      : BOOL;     (* Critical fault requiring immediate shutdown *)
    iDiagnosticsState   : INT;      (* Current operational state for diagnostics *)
END_VAR
VAR
    (* Internal State and Timers *)
    iState              : INT := 0; (* 0: Init, 10: Heating, 20: Vacuum stabilization, 30: Droplet Generation, 40: Target Sync, 99: Fault *)
    tHeaterTimer        : TON;
    tStabilityTimer     : TON;
    
    (* Internal Control Variables *)
    rTinMeltTempSetpt   : REAL := 240.0; (* Ideal melting temp for Sn *)
    rVacuumLimit        : REAL := 1.0E-5; (* Maximum allowable pressure for EUV *)
    rPiezoNominalAmp    : REAL := 120.0; (* Nominal piezo drive amplitude *)
    
    (* PI Controller States *)
    rHeaterIntegral     : REAL := 0.0;
    rHeaterError        : REAL := 0.0;
    rSyncIntegral       : REAL := 0.0;
    rSyncError          : REAL := 0.0;
END_VAR

(* === SAFETY AND INTERLOCKS === *)
IF NOT bSafetyInterlockOK OR rChamberVacuumActual > 1.0E-3 THEN
    bSystemReady := FALSE;
    bDropletSyncValid := FALSE;
    bCriticalAlarm := TRUE;
    rPiezoDriveVolts := 0.0;
    rTinHeaterPower := 0.0;
    iState := 99; (* Enter fault state *)
    RETURN;
END_IF;

(* === MAIN STATE MACHINE === *)
CASE iState OF
    0: (* INIT *)
        bSystemReady := FALSE;
        bDropletSyncValid := FALSE;
        bCriticalAlarm := FALSE;
        rPiezoDriveVolts := 0.0;
        IF bSystemEnable THEN
            iState := 10;
        END_IF;
        
    10: (* HEATING TIN RESERVOIR *)
        (* Simple PI Controller for Tin Heater *)
        rHeaterError := rTinMeltTempSetpt - rTinMeltTempActual;
        rHeaterIntegral := rHeaterIntegral + (rHeaterError * 0.01); (* Assuming 10ms cycle time *)
        (* Limit Integral Windup *)
        IF rHeaterIntegral > 100.0 THEN rHeaterIntegral := 100.0; END_IF;
        IF rHeaterIntegral < 0.0 THEN rHeaterIntegral := 0.0; END_IF;
        
        rTinHeaterPower := (rHeaterError * 5.0) + rHeaterIntegral;
        IF rTinHeaterPower > 100.0 THEN rTinHeaterPower := 100.0; END_IF;
        IF rTinHeaterPower < 0.0 THEN rTinHeaterPower := 0.0; END_IF;
        
        IF ABS(rHeaterError) < 1.5 THEN
            tHeaterTimer(IN := TRUE, PT := T#10S);
            IF tHeaterTimer.Q THEN
                tHeaterTimer(IN := FALSE);
                iState := 20;
            END_IF;
        ELSE
            tHeaterTimer(IN := FALSE);
        END_IF;

    20: (* VACUUM AND BUFFER GAS STABILIZATION *)
        rCatcherTempSetpt := 150.0; (* Maintain catcher above tin melting point *)
        IF (rChamberVacuumActual < rVacuumLimit) AND (rBufferGasFlowActual > 50.0) THEN
            tStabilityTimer(IN := TRUE, PT := T#5S);
            IF tStabilityTimer.Q THEN
                tStabilityTimer(IN := FALSE);
                iState := 30;
            END_IF;
        ELSE
            tStabilityTimer(IN := FALSE);
        END_IF;
        
    30: (* DROPLET GENERATION INITIATION *)
        (* Activate piezo with voltage proportional to commanded frequency *)
        rPiezoDriveVolts := rPiezoNominalAmp + ( (rDropletFreqCmd - 50.0) * 2.5 );
        IF bLaserPlasmaReady THEN
            iState := 40;
        END_IF;
        
    40: (* LASER TARGET SYNCHRONIZATION *)
        (* Fine-tune piezo drive based on laser sync error *)
        rSyncError := 0.0 - rLaserTargetSyncPos; (* Target position error is zero *)
        rSyncIntegral := rSyncIntegral + (rSyncError * 0.005);
        (* Limit Sync Integral Windup *)
        IF rSyncIntegral > 10.0 THEN rSyncIntegral := 10.0; END_IF;
        IF rSyncIntegral < -10.0 THEN rSyncIntegral := -10.0; END_IF;
        
        (* Apply correction to piezo voltage *)
        rPiezoDriveVolts := rPiezoDriveVolts + (rSyncError * 0.5) + rSyncIntegral;
        
        IF ABS(rSyncError) < 0.5 THEN
            bDropletSyncValid := TRUE;
            bSystemReady := TRUE;
        ELSE
            bDropletSyncValid := FALSE;
        END_IF;
        
        IF NOT bSystemEnable THEN
            iState := 0;
        END_IF;
        
    99: (* FAULT STATE *)
        (* Reset logic requires disable then enable *)
        IF NOT bSystemEnable THEN
            bCriticalAlarm := FALSE;
            iState := 0;
        END_IF;
        
END_CASE;

iDiagnosticsState := iState;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
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
