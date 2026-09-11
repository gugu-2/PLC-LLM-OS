import json, uuid, os

prompt = """<USER_REQUEST>
You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Utility-Scale Oceanic Thermal Energy Conversion (OTEC) Plant**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., 1000m cold water pipe (CWP) upwelling pump cavitation limits, closed-cycle ammonia Rankine turbine cascading, and titanium plate heat exchanger bio-fouling tracking). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_OTEC_EnergyPlant\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Utility-Scale Oceanic Thermal Energy Conversion (OTEC) Plant

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT.
</USER_REQUEST>"""

code = """```iec-st
FUNCTION_BLOCK FB_OTEC_Control_Matrix
VAR_INPUT
    bEnableMaster       : BOOL;     (* System master enable interlock *)
    bEmergencyStop      : BOOL;     (* Hardwired ESTOP circuit status OK *)
    rCWP_SuctionPress   : REAL;     (* Cold Water Pipe (1000m) suction pressure (kPa) *)
    rAmmoniaFlowRate    : REAL;     (* Closed-cycle ammonia mass flow rate (kg/s) *)
    rWarmSeawaterTemp   : REAL;     (* Warm seawater intake temperature (deg C) *)
    rColdSeawaterTemp   : REAL;     (* Deep cold seawater intake temperature (deg C) *)
    rTurbineSpeedRPM    : REAL;     (* Rankine cycle ammonia turbine speed (RPM) *)
    rEvaporatorDP       : REAL;     (* Differential pressure across titanium heat exchanger (kPa) - bio-fouling proxy *)
END_VAR
VAR_OUTPUT
    bSystemReady        : BOOL;     (* Master state ready for full operation *)
    rPumpDriveOutput    : REAL;     (* CWP Upwelling Pump VFD Control Signal (0-100%) *)
    rTurbineGuideVane   : REAL;     (* Ammonia turbine inlet guide vane position (0-100%) *)
    bCavitationAlarm    : BOOL;     (* CWP Pump cavitation threshold breached *)
    bBioFoulingAlert    : BOOL;     (* Titanium plate HX bio-fouling critical limits exceeded *)
    rGrossPowerEst      : REAL;     (* Estimated gross power output (MW) *)
END_VAR
VAR
    iState              : INT := 0; 
    tStartupDelay       : TON;
    tCavitationTimer    : TON;
    rNPSH_Available     : REAL;     (* Net Positive Suction Head Available *)
    rNPSH_Required      : REAL := 12.5; (* Pump specific NPSHr at design point *)
    rVaporPressure      : REAL;     (* Estimated vapor pressure of deep sea water at given temp *)
    rFoulingIndex       : REAL;     (* Calculated fouling thermal resistance index *)
END_VAR

(* === MAIN LOGIC === *)
(* Safety Interlock & ESTOP Check *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bCavitationAlarm := FALSE;
    rPumpDriveOutput := 0.0;
    rTurbineGuideVane := 0.0;
    iState := 0;
    RETURN;
END_IF;

(* Vapor Pressure Calculation (Simplified Antoine equation for seawater approx) *)
rVaporPressure := 0.61121 * EXP((18.678 - (rColdSeawaterTemp / 234.5)) * (rColdSeawaterTemp / (257.14 + rColdSeawaterTemp)));

(* Net Positive Suction Head (NPSH) Monitoring for 1000m CWP Cavitation *)
rNPSH_Available := (rCWP_SuctionPress - rVaporPressure) * 0.10197; (* Convert kPa to meters head roughly *)

IF rNPSH_Available < (rNPSH_Required * 1.1) THEN
    tCavitationTimer(IN := TRUE, PT := T#2S);
    IF tCavitationTimer.Q THEN
        bCavitationAlarm := TRUE;
    END_IF;
ELSE
    tCavitationTimer(IN := FALSE);
    bCavitationAlarm := FALSE;
END_IF;

(* Bio-Fouling Tracking across Titanium Plate Heat Exchangers *)
(* Uses empirical correlation based on differential pressure trend vs nominal flow *)
IF rAmmoniaFlowRate > 10.0 THEN
    rFoulingIndex := rEvaporatorDP / (rAmmoniaFlowRate * rAmmoniaFlowRate) * 100.0;
    IF rFoulingIndex > 0.85 THEN
        bBioFoulingAlert := TRUE;
    ELSE
        bBioFoulingAlert := FALSE;
    END_IF;
ELSE
    rFoulingIndex := 0.0;
END_IF;

(* Advanced Rankine Cycle State Machine *)
CASE iState OF
    0: (* IDLE & PRE-CHECKS *)
        bSystemReady := FALSE;
        rPumpDriveOutput := 0.0;
        rTurbineGuideVane := 0.0;
        IF bEnableMaster AND (rWarmSeawaterTemp > 24.0) AND (rColdSeawaterTemp < 6.0) AND NOT bCavitationAlarm THEN
            tStartupDelay(IN := TRUE, PT := T#10S);
            IF tStartupDelay.Q THEN
                iState := 10;
                tStartupDelay(IN := FALSE);
            END_IF;
        ELSE
            tStartupDelay(IN := FALSE);
        END_IF;

    10: (* CWP RAMP UP *)
        rPumpDriveOutput := rPumpDriveOutput + 0.5; (* Slow ramp rate for 1000m water column inertia *)
        IF rPumpDriveOutput > 45.0 THEN
            iState := 20;
        END_IF;

    20: (* AMMONIA CYCLE INITIATION *)
        bSystemReady := TRUE;
        rTurbineGuideVane := rTurbineGuideVane + 0.1;
        IF rTurbineSpeedRPM > 1800.0 THEN
            iState := 30;
        END_IF;

    30: (* FULL LOAD TRACKING *)
        (* Cascading PID placeholder: modulate pump and vanes to maximize delta-T enthalpy drop *)
        rGrossPowerEst := (rWarmSeawaterTemp - rColdSeawaterTemp) * rAmmoniaFlowRate * 0.042; 
        
        IF bCavitationAlarm THEN
            rPumpDriveOutput := rPumpDriveOutput - 5.0; (* Immediate load shed to preserve CWP pump *)
            iState := 25; (* Enter stabilization state *)
        END_IF;
        
        IF NOT bEnableMaster THEN
            iState := 99;
        END_IF;
        
    25: (* STABILIZATION *)
        IF NOT bCavitationAlarm THEN
            iState := 30;
        END_IF;

    99: (* SHUTDOWN SEQUENCE *)
        rTurbineGuideVane := 0.0;
        rPumpDriveOutput := 0.0;
        iState := 0;

END_CASE;

END_FUNCTION_BLOCK
```"""

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": code}
    ]
}

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
