import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Industrial Scale Offshore Wind Farm High-Voltage Direct Current (HVDC) Converter Platform**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Modular multilevel converter (MMC) sub-module capacitor balancing, onshore-offshore AC-DC voltage source conversion (VSC), and subsea cable fault ride-through). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_HVDC_OffshoreConverter\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Industrial Scale Offshore Wind Farm High-Voltage Direct Current (HVDC) Converter Platform

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_HVDC_OffshoreConverter
(*
    Modular Multilevel Converter (MMC) Sub-module Capacitor Balancing, 
    Onshore-Offshore AC-DC Voltage Source Conversion (VSC), 
    and Subsea Cable Fault Ride-Through (FRT).
*)
VAR_INPUT
    bEnable                 : BOOL;     (* System enable signal from SCADA *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal (E-Stop) *)
    rGridVoltageAC          : REAL;     (* Offshore AC grid voltage measurement (kV) *)
    rGridFreqAC             : REAL;     (* Offshore AC grid frequency (Hz) *)
    rDCLinkVoltage          : REAL;     (* HVDC link voltage measurement (kV) *)
    rActivePowerRef         : REAL;     (* Active power reference from grid operator (MW) *)
    rReactivePowerRef       : REAL;     (* Reactive power reference from grid operator (MVAR) *)
    aSubModuleCapVolts      : ARRAY[1..100] OF REAL; (* Array of sub-module capacitor voltages *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;     (* System ready and stable status *)
    rIGBTFiringAngle        : REAL;     (* Firing angle control signal for MMC valves *)
    bAlarm                  : BOOL;     (* Fault alarm output to SCADA *)
    bFaultRideThroughActive : BOOL;     (* Indicates FRT mode is currently engaged *)
    rDCLinkVoltageControl   : REAL;     (* Controlled DC link voltage reference (kV) *)
    iActiveSubModules       : INT;      (* Number of currently inserted sub-modules *)
END_VAR
VAR
    iState                  : INT := 0; (* Internal state machine variable *)
    tTimer                  : TON;      (* General purpose timer *)
    tFRTTimer               : TON;      (* Fault Ride-Through timer *)
    i                       : INT;      (* Loop index for capacitor balancing *)
    rAvgCapVoltage          : REAL;     (* Average capacitor voltage calculation *)
    rSumCapVoltage          : REAL;
    rVoltageError           : REAL;     (* AC grid voltage error for FRT detection *)
    bGridFaultDetected      : BOOL;
    rFRTThreshold           : REAL := 0.85; (* 85% of nominal voltage triggers FRT *)
    rNominalACVoltage       : REAL := 66.0; (* 66 kV nominal AC voltage *)
END_VAR

(* === MAIN LOGIC === *)
(* Safety Interlock *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bAlarm := TRUE;
    rIGBTFiringAngle := 0.0;
    iActiveSubModules := 0;
    bFaultRideThroughActive := FALSE;
    RETURN;
END_IF;

(* Grid Fault Detection for Fault Ride-Through (FRT) *)
rVoltageError := rGridVoltageAC / rNominalACVoltage;
IF rVoltageError < rFRTThreshold AND iState > 10 THEN
    bGridFaultDetected := TRUE;
ELSE
    bGridFaultDetected := FALSE;
END_IF;

CASE iState OF
    0: (* IDLE *)
        bSystemReady := FALSE;
        bFaultRideThroughActive := FALSE;
        rIGBTFiringAngle := 0.0;
        iActiveSubModules := 0;
        IF bEnable THEN
            iState := 10;
        END_IF;

    10: (* PRE-CHARGE MMC SUB-MODULES *)
        (* Simulate pre-charge sequence *)
        tTimer(IN := TRUE, PT := T#10S);
        IF tTimer.Q THEN
            tTimer(IN := FALSE);
            iState := 20;
        END_IF;

    20: (* RUNNING - NORMAL OPERATION *)
        bSystemReady := TRUE;
        bAlarm := FALSE;
        
        (* Calculate Average Capacitor Voltage for Balancing Logic *)
        rSumCapVoltage := 0.0;
        FOR i := 1 TO 100 DO
            rSumCapVoltage := rSumCapVoltage + aSubModuleCapVolts[i];
        END_FOR;
        rAvgCapVoltage := rSumCapVoltage / 100.0;

        (* VSC active and reactive power control calculations (simplified) *)
        rDCLinkVoltageControl := (rActivePowerRef * 1.05) + rDCLinkVoltage;
        
        (* Basic MMC sorting and insertion algorithm approximation *)
        IF rAvgCapVoltage > 0.0 THEN
            iActiveSubModules := REAL_TO_INT(rDCLinkVoltageControl / (rAvgCapVoltage * 2.0));
        ELSE
            iActiveSubModules := 0;
        END_IF;

        (* Cap limits *)
        IF iActiveSubModules > 100 THEN iActiveSubModules := 100; END_IF;
        IF iActiveSubModules < 0 THEN iActiveSubModules := 0; END_IF;

        (* Modulation index derived firing angle *)
        rIGBTFiringAngle := rReactivePowerRef * 0.01 + 30.0;

        IF bGridFaultDetected THEN
            iState := 30; (* Jump to FRT *)
        END_IF;

        IF NOT bEnable THEN
            iState := 0;
        END_IF;

    30: (* FAULT RIDE-THROUGH (FRT) MODE *)
        bFaultRideThroughActive := TRUE;
        bSystemReady := FALSE; (* System is unstable during fault *)
        
        (* Inject reactive current to support grid voltage (Q-Priority) *)
        rIGBTFiringAngle := 90.0; 
        
        tFRTTimer(IN := TRUE, PT := T#2S); (* LVRT capability up to 2 seconds *)
        
        IF NOT bGridFaultDetected THEN
            (* Grid recovered before FRT timer expired *)
            tFRTTimer(IN := FALSE);
            bFaultRideThroughActive := FALSE;
            iState := 20; (* Return to normal operation *)
        ELSIF tFRTTimer.Q THEN
            (* Fault persisted longer than capability, trip converter *)
            tFRTTimer(IN := FALSE);
            bAlarm := TRUE;
            iState := 40;
        END_IF;

    40: (* TRIP / FAULTED *)
        bSystemReady := FALSE;
        bFaultRideThroughActive := FALSE;
        rIGBTFiringAngle := 0.0;
        iActiveSubModules := 0;
        
        (* Require disable to reset fault *)
        IF NOT bEnable THEN
            bAlarm := FALSE;
            iState := 0;
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
