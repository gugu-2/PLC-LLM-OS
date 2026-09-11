import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Continuous Hot-Dip Galvanizing Line Zinc Pot Immersion**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., air-knife pressure profile mapping for micro-meter zinc thickness, inductive pot heating cascade loops, and snout atmosphere hydrogen/nitrogen dew point regulation). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_GalvanizingZincPot\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Continuous Hot-Dip Galvanizing Line Zinc Pot Immersion

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_ContinuousHotDipZincPot_ImmersionControl
VAR_INPUT
    (* Core Process Signals *)
    bSystemEnable            : BOOL;     (* System master enable interlock *)
    bEStopActive             : BOOL;     (* Emergency stop circuit OK signal (True = Safe) *)
    rLineSpeed               : REAL;     (* Strip line speed in meters per minute (m/min) *)
    rStripWidth              : REAL;     (* Strip width in millimeters (mm) *)
    rTargetCoatingWt         : REAL;     (* Target zinc coating weight on both sides (g/m2) *)
    
    (* Zinc Pot & Snout Atmosphere Inputs *)
    rZincPotTemp_PV          : REAL;     (* Zinc pot molten metal actual temperature (deg C) *)
    rSnoutDewPoint_PV        : REAL;     (* Snout atmospheric dew point (deg C) *)
    rSnoutH2Concentration    : REAL;     (* Hydrogen concentration in snout (%) *)
    rSnoutN2Concentration    : REAL;     (* Nitrogen concentration in snout (%) *)
    
    (* Inductive Heating Parameters *)
    rInductor1_Power_PV      : REAL;     (* Current power of primary inductor (kW) *)
    rInductor2_Power_PV      : REAL;     (* Current power of secondary inductor (kW) *)
    
    (* Air Knife Inputs *)
    rAirKnifeDistance_PV     : REAL;     (* Air knife lip distance to strip (mm) *)
    rAirKnifePressure_PV     : REAL;     (* Air knife header pressure actual (bar) *)
END_VAR

VAR_OUTPUT
    (* Actuator & Setpoint Controls *)
    bSystemReady             : BOOL;     (* Master system ready permissive *)
    bAlarmCondition          : BOOL;     (* Any active process alarm / interlock trip *)
    rInductor1_Power_SP      : REAL;     (* Calculated primary inductor power setpoint (kW) *)
    rInductor2_Power_SP      : REAL;     (* Calculated secondary inductor power setpoint (kW) *)
    
    (* Atmosphere & Air Knife Regulation Setpoints *)
    rSnoutH2Flow_SP          : REAL;     (* Snout hydrogen mass flow injection rate setpoint (NLPM) *)
    rAirKnifePressure_SP     : REAL;     (* Calculated air knife pressure setpoint (bar) *)
    rAirKnifeDistance_SP     : REAL;     (* Calculated air knife distance setpoint (mm) *)
    
    (* Diagnostic Outputs *)
    iControlState            : INT;      (* Current step in sequence state machine *)
    rCalculatedDross         : REAL;     (* Estimated dross formation rate based on temperature/speed *)
END_VAR

VAR
    (* Internal PID & Tracking State Variables *)
    iState                   : INT := 0; (* Main sequence index *)
    
    (* Timers & Triggers *)
    tStablizationDelay       : TON;
    tSnoutPurgeTimer         : TON;
    tAirKnifeRampUp          : TON;
    
    (* Constants *)
    c_rMaxPotTemp            : REAL := 470.0; (* Maximum allowable zinc pot temp deg C *)
    c_rMinPotTemp            : REAL := 450.0; (* Minimum allowable zinc pot temp deg C *)
    c_rTargetPotTemp         : REAL := 460.0; (* Ideal zinc pot temp for GI coating deg C *)
    
    (* Derived / Mathematical Integrators *)
    rTempError               : REAL;
    rCoatingDeviation        : REAL;
    rP_Gain                  : REAL := 2.5;
    rI_Gain                  : REAL := 0.8;
    rAccumulatedIntegral     : REAL := 0.0;
END_VAR

(* === MAIN SAFETY INTERLOCKS AND SYSTEM INITIALIZATION === *)
IF NOT bEStopActive THEN
    (* Immediate fallback to safe states upon E-Stop *)
    bSystemReady         := FALSE;
    bAlarmCondition      := TRUE;
    rInductor1_Power_SP  := 0.0;
    rInductor2_Power_SP  := 0.0;
    rSnoutH2Flow_SP      := 0.0;
    rAirKnifePressure_SP := 0.5; (* Standby pressure to prevent zinc splashing *)
    rAirKnifeDistance_SP := 50.0; (* Retract position *)
    iControlState        := -1;
    RETURN;
END_IF;

(* === MAIN SEQUENCE STATE MACHINE === *)
CASE iState OF
    0: (* SYSTEM IDLE / STANDBY *)
        bSystemReady := FALSE;
        rInductor1_Power_SP := 50.0; (* Maintenance holding heat *)
        rInductor2_Power_SP := 50.0;
        
        IF bSystemEnable THEN
            iState := 10;
        END_IF;

    10: (* SNOUT ATMOSPHERE PURGE & CONDITIONING *)
        bSystemReady := FALSE;
        (* Regulate Dew Point to < -40C for surface cleanliness before immersion *)
        IF rSnoutDewPoint_PV > -40.0 THEN
            rSnoutH2Flow_SP := 15.0; (* High flow purge *)
        ELSE
            rSnoutH2Flow_SP := 5.0;  (* Maintenance flow *)
        END_IF;
        
        tSnoutPurgeTimer(IN := TRUE, PT := T#15S);
        IF tSnoutPurgeTimer.Q THEN
            tSnoutPurgeTimer(IN := FALSE);
            iState := 20;
        END_IF;

    20: (* INDUCTIVE HEATING CASCADE & POT THERMAL STABILIZATION *)
        (* PI Control for Pot Temperature *)
        rTempError := c_rTargetPotTemp - rZincPotTemp_PV;
        rAccumulatedIntegral := rAccumulatedIntegral + (rTempError * 0.1);
        
        (* Anti-windup limit on integral action *)
        IF rAccumulatedIntegral > 100.0 THEN
            rAccumulatedIntegral := 100.0;
        ELSIF rAccumulatedIntegral < -100.0 THEN
            rAccumulatedIntegral := -100.0;
        END_IF;
        
        (* Output mapping for inductors - splitting load equally *)
        rInductor1_Power_SP := (rTempError * rP_Gain) + (rAccumulatedIntegral * rI_Gain);
        rInductor2_Power_SP := rInductor1_Power_SP;
        
        (* Clamp outputs *)
        IF rInductor1_Power_SP > 250.0 THEN rInductor1_Power_SP := 250.0; END_IF;
        IF rInductor1_Power_SP < 20.0 THEN rInductor1_Power_SP := 20.0; END_IF;
        IF rInductor2_Power_SP > 250.0 THEN rInductor2_Power_SP := 250.0; END_IF;
        IF rInductor2_Power_SP < 20.0 THEN rInductor2_Power_SP := 20.0; END_IF;
        
        IF rZincPotTemp_PV >= c_rMinPotTemp AND rZincPotTemp_PV <= c_rMaxPotTemp THEN
            tStablizationDelay(IN := TRUE, PT := T#5S);
            IF tStablizationDelay.Q THEN
                tStablizationDelay(IN := FALSE);
                iState := 30;
            END_IF;
        ELSE
            tStablizationDelay(IN := FALSE);
        END_IF;

    30: (* AIR KNIFE PROFILE MAPPING & RUNNING OPERATION *)
        bSystemReady := TRUE;
        bAlarmCondition := FALSE;
        
        (* Air knife pressure calculation based on line speed, target coating weight, and a non-linear aerodynamic coefficient *)
        (* Theoretical model: Pressure varies with square of speed and inversely with distance & target weight *)
        IF rLineSpeed > 0.0 AND rTargetCoatingWt > 0.0 THEN
            rAirKnifePressure_SP := (rLineSpeed * rLineSpeed * 0.00015) / (rTargetCoatingWt * 0.05);
            
            (* Calculate optimal distance: closer for lighter coats, further for heavier coats to avoid turbulence *)
            rAirKnifeDistance_SP := 8.0 + (rTargetCoatingWt * 0.012);
        ELSE
            rAirKnifePressure_SP := 0.2;
            rAirKnifeDistance_SP := 20.0;
        END_IF;
        
        (* Clamp limits for aerodynamic stability *)
        IF rAirKnifePressure_SP > 5.0 THEN rAirKnifePressure_SP := 5.0; END_IF;
        IF rAirKnifeDistance_SP < 5.0 THEN rAirKnifeDistance_SP := 5.0; END_IF;
        IF rAirKnifeDistance_SP > 30.0 THEN rAirKnifeDistance_SP := 30.0; END_IF;
        
        (* Dross formation calculation estimation for predictive maintenance *)
        rCalculatedDross := (rZincPotTemp_PV - c_rTargetPotTemp) * 0.5 + (rLineSpeed * 0.01);
        
        IF NOT bSystemEnable THEN
            iState := 0;
        END_IF;

END_CASE;

(* Update state output for HMI mapping *)
iControlState := iState;

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
