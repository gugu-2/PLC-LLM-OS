import json, uuid, os

prompt = """<USER_REQUEST>
You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Next-Gen Hypersonic Scramjet Wind Tunnel Heater**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., 4000°K arc jet plasma arc stabilization, continuous Mach-7 blow-down pressure regulation, and copper nozzle active water cooling nucleate boiling prevention). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_HypersonicWindTunnel\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Next-Gen Hypersonic Scramjet Wind Tunnel Heater

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT.
</USER_REQUEST>"""

code = """```iec-st
FUNCTION_BLOCK FB_ScramjetWindTunnelHeater
VAR_INPUT
    (* Required physical inputs *)
    bEnable                 : BOOL;     (* System master enable signal *)
    bEmergencyStop          : BOOL;     (* Master Safety relay OK signal - active high *)
    rArcVoltageFeedback     : REAL;     (* Arc jet voltage measurement (V) *)
    rArcCurrentFeedback     : REAL;     (* Arc jet current measurement (A) *)
    rPlenumPressure         : REAL;     (* Blow-down plenum pressure (MPa) *)
    rNozzleCoolantTempOut   : REAL;     (* Coolant water temperature out of nozzle (deg C) *)
    rNozzleCoolantFlow      : REAL;     (* Coolant water flow rate (kg/s) *)
    rTargetMachNumber       : REAL;     (* Commanded Mach number (M = 4.0 to 10.0) *)
END_VAR
VAR_OUTPUT
    (* Required physical outputs *)
    bSystemReady            : BOOL;     (* Wind tunnel ready for blow-down sequence *)
    rArcPowerCommand        : REAL;     (* Commanded arc power setpoint (MW) *)
    rMainThrottleValveCmd   : REAL;     (* Blow-down main throttle valve position (%) *)
    rCoolantPumpSpeedCmd    : REAL;     (* Coolant pump VFD speed command (%) *)
    bAlarm                  : BOOL;     (* General fault alarm output *)
    bPlasmaStabilized       : BOOL;     (* Indicates plasma arc is stable at 4000K *)
END_VAR
VAR
    (* Internal State Variables *)
    iState                  : INT := 0;
    tStabilizationTimer     : TON;
    tBlowdownTimer          : TON;
    
    (* Control Parameters *)
    rCalculatedPlasmaTemp   : REAL;     (* Estimated plasma temperature (K) *)
    rRequiredStagPressure   : REAL;     (* Required stagnation pressure for Mach Target (MPa) *)
    rHeatFluxEstimate       : REAL;     (* Estimated heat flux at throat (MW/m^2) *)
    
    (* Constants *)
    c_rGamma                : REAL := 1.4; (* Specific heat ratio for air *)
    c_rMaxCoolantTemp       : REAL := 180.0; (* Nucleate boiling threshold at 2MPa (deg C) *)
END_VAR

(* === MAIN LOGIC === *)
(* Master Safety Interlock *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bAlarm := TRUE;
    rArcPowerCommand := 0.0;
    rMainThrottleValveCmd := 0.0;
    rCoolantPumpSpeedCmd := 100.0; (* Max cooling during trip *)
    bPlasmaStabilized := FALSE;
    iState := 999; (* Error state *)
    RETURN;
END_IF;

(* Nucleate Boiling Prevention (Active Water Cooling) *)
rHeatFluxEstimate := rArcVoltageFeedback * rArcCurrentFeedback / 1000000.0; (* MW *)
IF (rNozzleCoolantTempOut > c_rMaxCoolantTemp) OR (rNozzleCoolantFlow < 10.0) THEN
    bAlarm := TRUE;
    (* Increase pump speed to prevent boiling damage to copper nozzle *)
    rCoolantPumpSpeedCmd := 100.0; 
ELSE
    (* Modulate coolant pump based on heat flux *)
    rCoolantPumpSpeedCmd := 40.0 + (rHeatFluxEstimate * 2.0); 
    IF rCoolantPumpSpeedCmd > 100.0 THEN
        rCoolantPumpSpeedCmd := 100.0;
    END_IF;
END_IF;

(* Plasma Arc Jet Stabilization (4000K Target) *)
rCalculatedPlasmaTemp := (rArcVoltageFeedback * rArcCurrentFeedback) * 0.005 + 300.0;

CASE iState OF
    0: (* IDLE - Wait for Enable *)
        bSystemReady := TRUE;
        bPlasmaStabilized := FALSE;
        rArcPowerCommand := 0.0;
        rMainThrottleValveCmd := 0.0;
        IF bEnable THEN
            iState := 10;
        END_IF;

    10: (* IGNITION & STABILIZATION *)
        bSystemReady := FALSE;
        rArcPowerCommand := 25.0; (* Initial strike power *)
        
        IF rCalculatedPlasmaTemp > 3800.0 AND rCalculatedPlasmaTemp < 4200.0 THEN
            tStabilizationTimer(IN := TRUE, PT := T#2S);
            IF tStabilizationTimer.Q THEN
                bPlasmaStabilized := TRUE;
                tStabilizationTimer(IN := FALSE);
                iState := 20;
            END_IF;
        ELSE
            tStabilizationTimer(IN := FALSE);
        END_IF;

    20: (* MACH-7 BLOW-DOWN PRESSURE REGULATION *)
        (* Calculate required stagnation pressure for the target Mach number *)
        rRequiredStagPressure := 0.1 * ((1.0 + ((c_rGamma - 1.0)/2.0) * rTargetMachNumber * rTargetMachNumber) ** (c_rGamma / (c_rGamma - 1.0)));
        
        (* Proportional control of main throttle valve *)
        rMainThrottleValveCmd := (rRequiredStagPressure - rPlenumPressure) * 5.0 + 50.0;
        
        (* Clamp valve command *)
        IF rMainThrottleValveCmd > 100.0 THEN
            rMainThrottleValveCmd := 100.0;
        ELSIF rMainThrottleValveCmd < 0.0 THEN
            rMainThrottleValveCmd := 0.0;
        END_IF;
        
        tBlowdownTimer(IN := TRUE, PT := T#30S); (* Max run duration *)
        IF tBlowdownTimer.Q OR NOT bEnable THEN
            tBlowdownTimer(IN := FALSE);
            iState := 30;
        END_IF;

    30: (* SHUTDOWN SEQUENCE *)
        bPlasmaStabilized := FALSE;
        rArcPowerCommand := 0.0;
        rMainThrottleValveCmd := 0.0;
        (* Keep cooling on until temperature drops *)
        IF rNozzleCoolantTempOut < 50.0 THEN
            iState := 0;
        END_IF;
        
    999: (* FAULT HANDLING *)
        IF bEmergencyStop THEN (* Reset logic if E-Stop is cleared and enable toggled *)
            IF NOT bEnable THEN
                bAlarm := FALSE;
                iState := 0;
            END_IF;
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
