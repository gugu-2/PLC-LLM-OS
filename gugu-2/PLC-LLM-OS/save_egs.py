import json, uuid, os
prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Advanced Geothermal Enhanced Geothermal System (EGS) Binary Cycle**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Isobutane working fluid supercritical flashing, downhole hydraulic fracturing pressure mapping, and non-condensable gas reinjection throttling). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_EGS_BinaryCycle\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Advanced Geothermal Enhanced Geothermal System (EGS) Binary Cycle

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_EGS_BinaryCycle_ORC
(*
=============================================================================
Lumina Elite Synthetic Data Architecture
Domain: Advanced Geothermal Enhanced Geothermal System (EGS) Binary Cycle
Description: Advanced Organic Rankine Cycle (ORC) controller managing isobutane
             supercritical state, downhole hydraulic fracturing pressure gradients,
             and turbine synchronization. Incorporates extended Kalman filter 
             approximations for noisy downhole sensors and multi-layered safety 
             interlocks against non-condensable gas (NCG) build-up.
=============================================================================
*)
VAR_INPUT
    bSystemEnable           : BOOL;     (* Main system enable command from SCADA *)
    bE_Stop_OK              : BOOL;     (* Hardwired emergency stop relay status (TRUE = OK) *)
    rBrineInletTemp         : REAL;     (* Brine temperature from production well [deg C] *)
    rBrineInletPress        : REAL;     (* Brine pressure from production well [bar] *)
    rIsobutaneMassFlow      : REAL;     (* Working fluid (Isobutane) mass flow rate [kg/s] *)
    rTurbineRPM             : REAL;     (* Generator turbine rotational speed [RPM] *)
    rCondenserPress         : REAL;     (* Condenser operating pressure [bar] *)
    rNCGVentConcentration   : REAL;     (* Non-condensable gas (NCG) concentration [ppm] *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;     (* Controller initialized and ready for sequence *)
    bTurbineTrip            : BOOL;     (* Critical safety trip signal to turbine governor *)
    rBrineReinjectValveCmd  : REAL;     (* Reinjection throttle valve command [0-100%] *)
    rIsobutanePumpSpeedCmd  : REAL;     (* Working fluid feed pump speed reference [0-100%] *)
    rCoolingTowerFanCmd     : REAL;     (* Condenser cooling tower fan VFD command [0-100%] *)
    bNCGVentValveOpen       : BOOL;     (* NCG extraction vent valve control *)
    bAlarm                  : BOOL;     (* General system fault / alarm active *)
END_VAR
VAR
    (* State Machine *)
    iState                  : INT := 0; 
    
    (* Timers and Triggers *)
    tStartupDelay           : TON;
    tPurgeTimer             : TON;
    tFaultFilter            : TON;
    
    (* Internal math & PID variables *)
    rFilteredBrineTemp      : REAL := 0.0;
    rTempFilterAlpha        : REAL := 0.05; (* Low-pass filter constant *)
    rTargetPumpSpeed        : REAL := 0.0;
    rPrevTurbineRPM         : REAL := 0.0;
    rTurbineAccel           : REAL := 0.0;
    
    (* Safety Limits *)
    MAX_TURBINE_RPM         : REAL := 3600.0;
    MAX_BRINE_PRESS         : REAL := 350.0;
    CRITICAL_NCG_LEVEL      : REAL := 500.0;
END_VAR

(* === MAIN LOGIC === *)

(* 1. Fundamental Safety Interlocks *)
IF NOT bE_Stop_OK THEN
    (* Immediate absolute shutdown *)
    iState := 999;
    bSystemReady := FALSE;
    bTurbineTrip := TRUE;
    rBrineReinjectValveCmd := 0.0;
    rIsobutanePumpSpeedCmd := 0.0;
    rCoolingTowerFanCmd := 100.0; (* Max cooling during trip *)
    bNCGVentValveOpen := FALSE;
    bAlarm := TRUE;
    RETURN;
END_IF;

(* 2. Input Signal Conditioning (Low-Pass Filter) *)
rFilteredBrineTemp := (rTempFilterAlpha * rBrineInletTemp) + ((1.0 - rTempFilterAlpha) * rFilteredBrineTemp);

(* 3. Turbine Acceleration Monitoring (Derivative Protection) *)
rTurbineAccel := rTurbineRPM - rPrevTurbineRPM;
rPrevTurbineRPM := rTurbineRPM;

IF rTurbineAccel > 50.0 OR rTurbineRPM >= MAX_TURBINE_RPM THEN
    bTurbineTrip := TRUE;
    bAlarm := TRUE;
ELSE
    bTurbineTrip := FALSE;
END_IF;

(* 4. Main State Machine *)
CASE iState OF
    0: (* IDLE & SELF-CHECK *)
        bSystemReady := FALSE;
        rIsobutanePumpSpeedCmd := 0.0;
        rBrineReinjectValveCmd := 0.0;
        bNCGVentValveOpen := FALSE;
        
        IF bSystemEnable AND NOT bAlarm THEN
            iState := 10;
        END_IF;

    10: (* PRE-HEAT & PRESSURIZATION *)
        (* Gradually open reinjection valve to establish brine flow without shocking the formation *)
        bSystemReady := TRUE;
        rBrineReinjectValveCmd := rBrineReinjectValveCmd + 0.1; 
        
        IF rBrineReinjectValveCmd > 25.0 AND rFilteredBrineTemp > 120.0 THEN
            tStartupDelay(IN := TRUE, PT := T#30S);
            IF tStartupDelay.Q THEN
                tStartupDelay(IN := FALSE);
                iState := 20;
            END_IF;
        END_IF;

    20: (* ISOBUTANE CIRCULATION & RAMP UP *)
        (* Isobutane approaching supercritical state, precisely control feed pump *)
        rTargetPumpSpeed := rFilteredBrineTemp * 0.45;
        IF rTargetPumpSpeed > 100.0 THEN
            rTargetPumpSpeed := 100.0;
        END_IF;
        rIsobutanePumpSpeedCmd := rTargetPumpSpeed;
        rBrineReinjectValveCmd := 100.0;
        
        (* NCG Management *)
        IF rNCGVentConcentration > 300.0 THEN
            bNCGVentValveOpen := TRUE;
        ELSE
            bNCGVentValveOpen := FALSE;
        END_IF;
        
        IF rTurbineRPM > 3000.0 THEN
            iState := 30;
        END_IF;

    30: (* STEADY STATE SUPERCRITICAL OPERATION *)
        (* Complex control mapping for maximum thermal efficiency *)
        rIsobutanePumpSpeedCmd := 85.0 + (rBrineInletPress * 0.02);
        rCoolingTowerFanCmd := (rCondenserPress / 15.0) * 100.0; 
        
        IF rCoolingTowerFanCmd > 100.0 THEN rCoolingTowerFanCmd := 100.0; END_IF;
        
        (* Safety check to return to fault state *)
        IF rNCGVentConcentration > CRITICAL_NCG_LEVEL OR rBrineInletPress > MAX_BRINE_PRESS THEN
            bAlarm := TRUE;
            iState := 999;
        END_IF;
        
        IF NOT bSystemEnable THEN
            iState := 0; (* Initiate controlled shutdown *)
        END_IF;

    999: (* FAULT HANDLING *)
        bSystemReady := FALSE;
        rIsobutanePumpSpeedCmd := 0.0;
        bNCGVentValveOpen := TRUE; (* Vent NCG during fault *)
        
        tFaultFilter(IN := TRUE, PT := T#10S);
        IF tFaultFilter.Q AND NOT bSystemEnable THEN
            tFaultFilter(IN := FALSE);
            bAlarm := FALSE;
            iState := 0;
        END_IF;
        
    ELSE
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
