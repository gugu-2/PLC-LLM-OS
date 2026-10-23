import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Advanced Semiconductor Physical Vapor Deposition (PVD) Magnetron Sputtering**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., High-power impulse magnetron sputtering (HiPIMS) arc suppression, target erosion profile magnetic steering, and argon-nitrogen reactive gas hysteresis loop control). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_PVD_MagnetronSputtering\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Advanced Semiconductor Physical Vapor Deposition (PVD) Magnetron Sputtering

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_PVD_MagnetronSputtering
VAR_INPUT
    (* High-power impulse magnetron sputtering (HiPIMS) process inputs *)
    bSystemEnable       : BOOL;     (* Main PVD system enable signal *)
    bEmergencyStop      : BOOL;     (* Hardwired emergency stop OK signal *)
    rTargetVoltage      : REAL;     (* Feedback target cathode voltage [V] *)
    rCathodeCurrent     : REAL;     (* Feedback target cathode current [A] *)
    rChamberPressure    : REAL;     (* High-vacuum chamber pressure [Torr] *)
    rArgonFlow          : REAL;     (* Argon (sputter gas) mass flow rate [sccm] *)
    rNitrogenFlow       : REAL;     (* Nitrogen (reactive gas) mass flow rate [sccm] *)
    rPowerSetpoint      : REAL;     (* Desired sputtering power setpoint [kW] *)
END_VAR
VAR_OUTPUT
    (* HiPIMS Control Outputs *)
    bSystemReady        : BOOL;     (* System is ready and interlocks clear *)
    rPlasmaPowerCtrl    : REAL;     (* Control signal to the DC/RF power supply (0-10V -> 0-100%) *)
    rArgonValveCmd      : REAL;     (* Control signal for Ar Mass Flow Controller [0-100%] *)
    rNitrogenValveCmd   : REAL;     (* Control signal for N2 Mass Flow Controller [0-100%] *)
    bArcDetected        : BOOL;     (* Arc suppression active signal to generator *)
    bCriticalAlarm      : BOOL;     (* System critical fault, abort process *)
END_VAR
VAR
    (* Internal State and Filtering *)
    iProcessState       : INT := 0;
    rFilteredCurrent    : REAL := 0.0;
    rFilteredVoltage    : REAL := 0.0;
    rCurrentPower       : REAL := 0.0;
    
    (* Timers *)
    tProcessDelay       : TON;
    tArcRecovery        : TON;
    tHysteresisDelay    : TON;
    
    (* Hysteresis & Arc Control *)
    iArcCount           : INT := 0;
    bArcSuppressionActive : BOOL := FALSE;
    rGasRatio           : REAL := 0.0;
    rPowerError         : REAL := 0.0;
    rIntegralTerm       : REAL := 0.0;
    rKp                 : REAL := 2.5;
    rKi                 : REAL := 0.15;
    
    (* Constants *)
    rMaxPressure        : REAL := 1.0E-2; (* Max operating pressure in Torr *)
    rMinPressure        : REAL := 5.0E-7; (* Min base pressure in Torr *)
    rVoltageDropLimit   : REAL := 50.0;   (* Voltage drop threshold for arc detection [V] *)
    rCurrentSpikeLimit  : REAL := 150.0;  (* Current spike threshold for arc [A] *)
END_VAR

(* === MAIN SAFETY AND FILTERING === *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bCriticalAlarm := TRUE;
    rPlasmaPowerCtrl := 0.0;
    rArgonValveCmd := 0.0;
    rNitrogenValveCmd := 0.0;
    bArcDetected := FALSE;
    iProcessState := 0;
    RETURN;
END_IF;

(* First-order low-pass filters for analog signals (Tau = ~10ms at standard scan rate) *)
rFilteredCurrent := (rFilteredCurrent * 0.9) + (rCathodeCurrent * 0.1);
rFilteredVoltage := (rFilteredVoltage * 0.9) + (rTargetVoltage * 0.1);
rCurrentPower := (rFilteredVoltage * rFilteredCurrent) / 1000.0; (* kW *)

(* Arc Detection Logic *)
IF (rCathodeCurrent > rCurrentSpikeLimit) OR (rTargetVoltage < rVoltageDropLimit) THEN
    IF NOT bArcSuppressionActive THEN
        bArcSuppressionActive := TRUE;
        bArcDetected := TRUE;
        iArcCount := iArcCount + 1;
        rPlasmaPowerCtrl := 0.0; (* Instantly cut power to quench arc *)
    END_IF;
END_IF;

tArcRecovery(IN := bArcSuppressionActive, PT := T#50MS);
IF tArcRecovery.Q THEN
    bArcSuppressionActive := FALSE;
    bArcDetected := FALSE;
END_IF;

IF iArcCount > 100 THEN
    bCriticalAlarm := TRUE; (* Too many arcs, inspect target *)
END_IF;

(* === MAIN PROCESS STATE MACHINE === *)
CASE iProcessState OF
    0: (* IDLE - Wait for Enable and Base Vacuum *)
        bSystemReady := FALSE;
        rPlasmaPowerCtrl := 0.0;
        rArgonValveCmd := 0.0;
        rNitrogenValveCmd := 0.0;
        
        IF bSystemEnable AND (rChamberPressure <= rMinPressure) THEN
            iProcessState := 10;
        END_IF;

    10: (* GAS STABILIZATION *)
        rArgonValveCmd := 45.0; (* Baseline Ar flow *)
        rNitrogenValveCmd := 0.0; (* Pure metallic mode start *)
        
        tProcessDelay(IN := TRUE, PT := T#10S);
        IF tProcessDelay.Q THEN
            tProcessDelay(IN := FALSE);
            bSystemReady := TRUE;
            iProcessState := 20;
        END_IF;

    20: (* PLASMA IGNITION *)
        rPlasmaPowerCtrl := 10.0; (* 10% ignition power *)
        IF (rCurrentPower > 0.5) THEN (* Plasma struck *)
            iProcessState := 30;
        END_IF;
        
        IF NOT bSystemEnable THEN iProcessState := 0; END_IF;

    30: (* RAMP & PID POWER CONTROL *)
        IF NOT bArcSuppressionActive THEN
            (* PI Power Control Loop *)
            rPowerError := rPowerSetpoint - rCurrentPower;
            rIntegralTerm := rIntegralTerm + (rPowerError * rKi);
            
            (* Anti-windup *)
            IF rIntegralTerm > 100.0 THEN rIntegralTerm := 100.0; END_IF;
            IF rIntegralTerm < 0.0 THEN rIntegralTerm := 0.0; END_IF;
            
            rPlasmaPowerCtrl := (rPowerError * rKp) + rIntegralTerm;
            
            (* Output clamping *)
            IF rPlasmaPowerCtrl > 100.0 THEN rPlasmaPowerCtrl := 100.0; END_IF;
            IF rPlasmaPowerCtrl < 0.0 THEN rPlasmaPowerCtrl := 0.0; END_IF;
        END_IF;

        (* Reactive Sputtering Hysteresis Loop Control *)
        (* Dynamically adjust Nitrogen flow to stay in transition zone (poisoned vs metallic target) *)
        rGasRatio := rArgonFlow / (rNitrogenFlow + 0.1); 
        IF rFilteredVoltage < 350.0 THEN
            (* Target is getting poisoned, reduce N2 *)
            rNitrogenValveCmd := rNitrogenValveCmd - 0.5;
        ELSIF rFilteredVoltage > 450.0 THEN
            (* Target is fully metallic, increase N2 *)
            rNitrogenValveCmd := rNitrogenValveCmd + 0.5;
        END_IF;
        
        IF rNitrogenValveCmd > 100.0 THEN rNitrogenValveCmd := 100.0; END_IF;
        IF rNitrogenValveCmd < 0.0 THEN rNitrogenValveCmd := 0.0; END_IF;

        IF rChamberPressure > rMaxPressure THEN
            bCriticalAlarm := TRUE;
            iProcessState := 99; (* Abort *)
        END_IF;
        
        IF NOT bSystemEnable THEN 
            iProcessState := 0; 
        END_IF;

    99: (* ABORT STATE *)
        rPlasmaPowerCtrl := 0.0;
        rArgonValveCmd := 0.0;
        rNitrogenValveCmd := 0.0;
        bSystemReady := FALSE;
        IF NOT bSystemEnable AND bEmergencyStop THEN
            bCriticalAlarm := FALSE;
            iArcCount := 0;
            iProcessState := 0;
        END_IF;
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
