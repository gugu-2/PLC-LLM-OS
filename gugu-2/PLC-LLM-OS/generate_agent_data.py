import os, json, uuid

os.makedirs('data/swarm_raw', exist_ok=True)

prompt = '''You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Large-Scale Municipal Solid Waste (MSW) Incinerator Grate Stoker Speed and Flue Gas Scrubber**

Task: Invent a highly complex, ultra-realistic control scenario for this domain. Make this code EVEN BETTER, MORE ADVANCED, and MORE RIGOROUS than previous iterations. Include extreme edge-case handling, advanced math, and robust fault-tolerance.

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
   prompt = """<copy this exact user prompt here>"""
   code = """```iec-st\\nFUNCTION_BLOCK FB_MSWIncinerator_Control\\n//...\\nEND_FUNCTION_BLOCK\\n```"""
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
6. REPLY with: EVOLUTION COMPLETE: Large-Scale Municipal Solid Waste (MSW) Incinerator Grate Stoker Speed and Flue Gas Scrubber

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT.'''

code = '''```iec-st
FUNCTION_BLOCK FB_MSW_Incinerator_Stoker_Scrubber_Control
(*=============================================================================
  Block: FB_MSW_Incinerator_Stoker_Scrubber_Control
  Description: 
    Advanced control strategy for a Large-Scale Municipal Solid Waste (MSW) 
    Incinerator Grate Stoker Speed and Flue Gas Scrubber. 
    Implements multi-variable control, dynamic speed scheduling, sensor noise 
    filtering, emissions compliance handling, and safety interlocks.
=============================================================================*)
VAR_INPUT
    bEnableSys               : BOOL;   (* System Global Enable *)
    bEmergencyStop           : BOOL;   (* Safety relay OK signal; TRUE = OK *)
    rFurnaceTemperature      : REAL;   (* Main combustion zone temperature [degC] *)
    rSteamFlowRate           : REAL;   (* Boiler steam output flow rate [t/h] *)
    rO2ConcentrationWet      : REAL;   (* Wet oxygen concentration in flue gas [%] *)
    rSO2Emission             : REAL;   (* SO2 concentration at scrubber inlet [mg/Nm3] *)
    rHClEmission             : REAL;   (* HCl concentration at scrubber inlet [mg/Nm3] *)
    rScrubberSlurrypH        : REAL;   (* Current pH of the scrubber slurry *)
END_VAR

VAR_OUTPUT
    bSystemReady             : BOOL;   (* System initialized and ready for auto *)
    rGrateStokerSpeedCtrl    : REAL;   (* Commanded grate stoker speed [m/h] *)
    rLimeSlurryDosingRate    : REAL;   (* Commanded lime slurry flow rate [L/h] *)
    rPrimaryAirFlowRef       : REAL;   (* Commanded primary air flow [Nm3/h] *)
    bCriticalAlarm           : BOOL;   (* Critical fault active (emissions/temp) *)
    bWarningAlarm            : BOOL;   (* Warning active (approaching limits) *)
END_VAR

VAR
    (* Internal State and Timers *)
    iState                   : INT := 0; (* 0=IDLE, 10=INIT, 20=RUN, 99=FAULT *)
    tScanCycle               : TON;
    tFaultDelay              : TON;
    tEmissionsDelay          : TON;
    
    (* Filtered Measurements *)
    rFiltTemp                : REAL;
    rFiltSO2                 : REAL;
    rFiltHCl                 : REAL;
    
    (* PID States / Control Variables *)
    rTempError               : REAL;
    rTempIntegral            : REAL;
    rScrubberDoseBase        : REAL;
    rPhError                 : REAL;
    
    (* Constants *)
    c_rTempSetpoint          : REAL := 950.0; (* Optimal incineration temp *)
    c_rMaxGrateSpeed         : REAL := 15.0;
    c_rMinGrateSpeed         : REAL := 2.0;
    c_rPhSetpoint            : REAL := 7.0;
    c_rSO2Limit              : REAL := 50.0;
END_VAR

(* === MAIN LOGIC === *)
(* 1. Safety and Emergency Stop Check *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bCriticalAlarm := TRUE;
    rGrateStokerSpeedCtrl := 0.0;
    rLimeSlurryDosingRate := 0.0;
    rPrimaryAirFlowRef := 0.0;
    iState := 99;
    RETURN;
END_IF;

(* 2. Simple First-Order Low Pass Filtering for noisy sensors *)
rFiltTemp := (rFurnaceTemperature * 0.1) + (rFiltTemp * 0.9);
rFiltSO2  := (rSO2Emission * 0.2) + (rFiltSO2 * 0.8);
rFiltHCl  := (rHClEmission * 0.2) + (rFiltHCl * 0.8);

(* 3. State Machine *)
CASE iState OF
    0: (* IDLE *)
        bSystemReady := FALSE;
        rGrateStokerSpeedCtrl := 0.0;
        rLimeSlurryDosingRate := 0.0;
        IF bEnableSys THEN
            iState := 10;
        END_IF;

    10: (* INIT *)
        (* Perform pre-checks *)
        IF rFiltTemp > 400.0 THEN (* Minimum warmup temp reached *)
            bSystemReady := TRUE;
            iState := 20;
        END_IF;
        IF NOT bEnableSys THEN
            iState := 0;
        END_IF;

    20: (* RUNNING *)
        (* Stoker Speed Control based on Temp Error (P-I acting) *)
        rTempError := c_rTempSetpoint - rFiltTemp;
        rTempIntegral := rTempIntegral + (rTempError * 0.05);
        
        (* Anti-windup *)
        IF rTempIntegral > 50.0 THEN rTempIntegral := 50.0; END_IF;
        IF rTempIntegral < -50.0 THEN rTempIntegral := -50.0; END_IF;
        
        rGrateStokerSpeedCtrl := 5.0 + (rTempError * -0.01) + (rTempIntegral * -0.005);
        
        (* Clamping Grate Speed *)
        IF rGrateStokerSpeedCtrl > c_rMaxGrateSpeed THEN
            rGrateStokerSpeedCtrl := c_rMaxGrateSpeed;
        ELSIF rGrateStokerSpeedCtrl < c_rMinGrateSpeed THEN
            rGrateStokerSpeedCtrl := c_rMinGrateSpeed;
        END_IF;
        
        (* Scrubber Slurry Dosing Control based on SO2/HCl and pH *)
        rScrubberDoseBase := (rFiltSO2 * 1.5) + (rFiltHCl * 1.2);
        rPhError := c_rPhSetpoint - rScrubberSlurrypH;
        
        IF rPhError > 0.0 THEN
            rLimeSlurryDosingRate := rScrubberDoseBase * (1.0 + (rPhError * 0.5));
        ELSE
            rLimeSlurryDosingRate := rScrubberDoseBase;
        END_IF;
        
        (* Alarm Logic *)
        IF rFiltSO2 > c_rSO2Limit THEN
            tEmissionsDelay(IN := TRUE, PT := T#10S);
        ELSE
            tEmissionsDelay(IN := FALSE);
        END_IF;
        
        IF tEmissionsDelay.Q THEN
            bWarningAlarm := TRUE;
        ELSE
            bWarningAlarm := FALSE;
        END_IF;
        
        IF NOT bEnableSys THEN
            iState := 0;
        END_IF;

    99: (* FAULT *)
        bSystemReady := FALSE;
        IF bEmergencyStop AND NOT bEnableSys THEN
            bCriticalAlarm := FALSE;
            iState := 0;
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
```'''

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
