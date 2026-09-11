import json, uuid, os

prompt = '''You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Utility-Scale Enhanced Geothermal System (EGS)**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., High-pressure hydraulic stimulation micro-seismic event monitoring, supercritical binary cycle isobutane expansion, and non-condensable gas (NCG) extraction). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = """```iec-st\nFUNCTION_BLOCK FB_EGS_GeothermalControl\n//...\nEND_FUNCTION_BLOCK\n```"""
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
6. REPLY with: EVOLUTION COMPLETE: Utility-Scale Enhanced Geothermal System (EGS)

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT.'''

code = '''```iec-st
FUNCTION_BLOCK FB_EGS_StimulationAndBinaryCycle
VAR_INPUT
    (* Required: at least 4-8 physical inputs with types and comments *)
    bEnableSystem          : BOOL;     (* Master enable for the geothermal control system *)
    bEmergencyShutdown     : BOOL;     (* SIS trip signal, normally TRUE (failsafe) *)
    rWellheadPressure      : REAL;     (* Injection wellhead pressure [bar] *)
    rWellheadTemp          : REAL;     (* Production wellhead temperature [deg C] *)
    rMicroSeismicPGA       : REAL;     (* Peak Ground Acceleration from seismic network [g] *)
    rIsobutaneFlowRate     : REAL;     (* Mass flow rate of working fluid (isobutane) [kg/s] *)
    rNCGConcentration      : REAL;     (* Non-condensable gas concentration at separator [%] *)
    bIsobutanePumpReady    : BOOL;     (* Binary cycle feed pump VFD ready status *)
END_VAR
VAR_OUTPUT
    (* Required: at least 3-6 outputs with types and comments *)
    bSystemHealthy         : BOOL;     (* TRUE when no alarms and running nominally *)
    rInjectionValveCmd     : REAL;     (* Command to hydraulic stimulation choke valve [0-100%] *)
    rTurbineGovernorCmd    : REAL;     (* Command to isobutane turbine inlet guide vanes [0-100%] *)
    bNCGVentValveOpen      : BOOL;     (* Solenoid command to NCG atmospheric vent *)
    iSystemState           : INT;      (* Current operational state machine step *)
    bSeismicTripAlarm      : BOOL;     (* Latched alarm for micro-seismic exceedance *)
    rCalculatedEnthalpy    : REAL;     (* Estimated production fluid enthalpy [kJ/kg] *)
END_VAR
VAR
    (* Internal state variables *)
    iState                 : INT := 0; (* Internal state tracker *)
    tStartupDelay          : TON;
    tNCGVentTimer          : TON;
    rPressureError         : REAL;
    rPressureIntegral      : REAL := 0.0;
    rIntegralGain          : REAL := 0.05;
    rProportionalGain      : REAL := 2.5;
    rSeismicThreshold      : REAL := 0.025; (* 0.025g traffic light system red limit *)
    rMaxInjectionPressure  : REAL := 350.0; (* 350 bar max stimulation pressure *)
    bSeismicWarning        : BOOL := FALSE;
END_VAR

(* === MAIN LOGIC === *)
(* 1. Safety and Interlocks *)
IF NOT bEmergencyShutdown THEN
    bSystemHealthy := FALSE;
    rInjectionValveCmd := 0.0;
    rTurbineGovernorCmd := 0.0;
    bNCGVentValveOpen := FALSE;
    iState := 99; (* FAULT STATE *)
    iSystemState := iState;
    RETURN;
END_IF;

(* 2. Micro-seismic monitoring (Traffic Light System) *)
IF rMicroSeismicPGA > rSeismicThreshold THEN
    bSeismicTripAlarm := TRUE;
END_IF;

IF bSeismicTripAlarm THEN
    rInjectionValveCmd := 0.0; (* Hard shut-in on seismic event *)
    iState := 99;
END_IF;

(* 3. Enthalpy Estimation (simplified polynomial for supercritical brine) *)
rCalculatedEnthalpy := (rWellheadTemp * 4.18) + (rWellheadPressure * 0.5);

(* 4. State Machine for Normal Operations *)
CASE iState OF
    0: (* IDLE *)
        bSystemHealthy := TRUE;
        rInjectionValveCmd := 0.0;
        rTurbineGovernorCmd := 0.0;
        bNCGVentValveOpen := FALSE;
        IF bEnableSystem AND NOT bSeismicTripAlarm THEN
            iState := 10;
        END_IF;

    10: (* PRE-STIMULATION PRESSURIZATION *)
        tStartupDelay(IN := TRUE, PT := T#30S);
        rInjectionValveCmd := 10.0; (* 10% crack for line fill *)
        IF tStartupDelay.Q THEN
            tStartupDelay(IN := FALSE);
            iState := 20;
        END_IF;

    20: (* ACTIVE HYDRAULIC STIMULATION / PI CONTROL *)
        rPressureError := rMaxInjectionPressure - rWellheadPressure;
        rPressureIntegral := rPressureIntegral + (rPressureError * 0.1); 
        
        (* Anti-windup *)
        IF rPressureIntegral > 100.0 THEN rPressureIntegral := 100.0; END_IF;
        IF rPressureIntegral < 0.0 THEN rPressureIntegral := 0.0; END_IF;
        
        rInjectionValveCmd := (rPressureError * rProportionalGain) + rPressureIntegral;
        
        IF rInjectionValveCmd > 100.0 THEN rInjectionValveCmd := 100.0; END_IF;
        IF rInjectionValveCmd < 0.0 THEN rInjectionValveCmd := 0.0; END_IF;

        IF rWellheadTemp > 180.0 THEN (* Geothermal breakthrough detected *)
            iState := 30;
        END_IF;

    30: (* BINARY CYCLE TURBINE RAMP *)
        IF bIsobutanePumpReady AND rIsobutaneFlowRate > 15.0 THEN
            rTurbineGovernorCmd := rTurbineGovernorCmd + 0.1; (* Ramp up 0.1% per scan *)
            IF rTurbineGovernorCmd >= 100.0 THEN
                rTurbineGovernorCmd := 100.0;
                iState := 40;
            END_IF;
        END_IF;

    40: (* STEADY STATE GENERATION & NCG MANAGEMENT *)
        IF rNCGConcentration > 2.5 THEN
            bNCGVentValveOpen := TRUE;
            tNCGVentTimer(IN := TRUE, PT := T#15S);
        END_IF;
        
        IF tNCGVentTimer.Q THEN
            bNCGVentValveOpen := FALSE;
            IF rNCGConcentration <= 2.0 THEN
                tNCGVentTimer(IN := FALSE);
            END_IF;
        END_IF;

        IF NOT bEnableSystem THEN
            iState := 0;
        END_IF;
        
    99: (* FAULT HANDLING *)
        bSystemHealthy := FALSE;
        rInjectionValveCmd := 0.0;
        rTurbineGovernorCmd := 0.0;
        IF NOT bSeismicTripAlarm AND bEnableSystem AND bEmergencyShutdown THEN
            iState := 0; (* Reset if conditions clear *)
        END_IF;

END_CASE;

iSystemState := iState;

END_FUNCTION_BLOCK
```'''

record = {
    'messages': [
        {'role': 'user', 'content': prompt},
        {'role': 'assistant', 'content': code}
    ]
}

os.makedirs('data/swarm_raw', exist_ok=True)
filename = f'data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json'
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(record, f, ensure_ascii=False)

print(f'Saved to {filename}')
