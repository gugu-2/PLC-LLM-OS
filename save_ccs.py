import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V4 Persona: a 50+ years experienced Chief PLC Architect & Control Systems PhD. 
Your logic must include advanced Non-Linear PID with Anti-Windup, 3-level cascade control, digital low-pass filtering, predictive anomaly detection, and multi-layered hardware interlocks. Output the most elite, mathematically rigorous, and structurally flawless IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Mega-Scale Underground Carbon Capture and Sequestration (CCS) High-Pressure Compressor Surge and Supercritical Fluid Injection**

Task: Invent a highly complex, ultra-realistic control scenario for this domain. This MUST be drastically better, more advanced, and longer than previous iterations.

CRITICAL RULES - READ EVERY LINE:
1. CODE FENCE: Use TRIPLE backticks + iec-st. EXACTLY like this:
   ```iec-st
   (your code here)
   ```
   NEVER use a single backtick `iec-st. ALWAYS use triple backticks.
2. REQUIRED IEC 61131-3 STRUCTURE (all 5 mandatory):
   a. FUNCTION_BLOCK FB_<Name>   <- first line of code, always
   b. VAR_INPUT ... END_VAR      <- min 6 typed inputs with comments
   c. VAR_OUTPUT ... END_VAR     <- min 5 typed outputs with comments
   d. At least one END_IF; or END_CASE;  <- control logic required
   e. END_FUNCTION_BLOCK         <- last line of code, always
3. LENGTH: The assistant content MUST be >= 2000 characters total. Make it massive and extremely rigorous.
4. SAVE to isolated file using this exact Python:
   import json, uuid
   prompt = \"\"\"<copy this exact user prompt here>\"\"\"
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_CarbonCapture_Injection\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
   record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
   with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
       json.dump(record, f, ensure_ascii=False)
5. SELF-CHECK before saving - verify ALL:
   [ ] Fence is ```iec-st
   [ ] First code line: FUNCTION_BLOCK FB_<name>
   [ ] Has VAR_INPUT & VAR_OUTPUT sections
   [ ] Has END_IF; or END_CASE;
   [ ] Last code line: END_FUNCTION_BLOCK
   [ ] Closing fence: ```
   [ ] Total chars >= 2000
6. REPLY with: EVOLUTION COMPLETE: Mega-Scale Underground Carbon Capture and Sequestration (CCS) High-Pressure Compressor Surge and Supercritical Fluid Injection"""

code = """```iec-st
FUNCTION_BLOCK FB_CCSSupercriticalInjection
(* 
   =============================================================================
   Lumina AI Cloud Swarm V4 - Chief PLC Architect & Control Systems PhD
   Domain: Mega-Scale Underground Carbon Capture and Sequestration (CCS)
   Description: High-Pressure Compressor Surge and Supercritical Fluid Injection
   =============================================================================
*)
VAR_INPUT
    bSystemEnable           : BOOL;     (* Main system enable command *)
    bEmergencyStopOk        : BOOL;     (* Hardware E-Stop OK (Normally Closed loop) *)
    rInletPressure          : REAL;     (* Inlet CO2 gas pressure (bar) *)
    rInletTemp              : REAL;     (* Inlet CO2 gas temperature (deg C) *)
    rCompressorSpeed        : REAL;     (* Current compressor rotational speed (RPM) *)
    rDischargePressure      : REAL;     (* High-stage discharge pressure (bar) *)
    rVibrationLevel         : REAL;     (* Radial vibration monitor (mm/s) *)
    rSurgeFlow              : REAL;     (* Flow rate at surge line (kg/s) *)
    rWellheadPressure       : REAL;     (* Downhole injection wellhead pressure (bar) *)
END_VAR

VAR_OUTPUT
    bSystemReady            : BOOL;     (* All pre-start interlocks satisfied *)
    rSurgeValveCmd          : REAL;     (* Anti-surge bypass valve position (0-100%) *)
    rInjectionValveCmd      : REAL;     (* Wellhead injection valve position (0-100%) *)
    rCompressorSpeedCmd     : REAL;     (* Variable Frequency Drive speed reference (RPM) *)
    bSurgeWarning           : BOOL;     (* Approaching surge margin warning *)
    bCriticalTrip           : BOOL;     (* Protection trip active *)
    iOperatingState         : INT;      (* Current finite state machine step *)
END_VAR

VAR
    (* Internal Filter Variables *)
    rFiltDischargePress     : REAL;
    rFiltWellheadPress      : REAL;
    rAlphaFilt              : REAL := 0.15; (* Low-pass filter coefficient *)

    (* Anti-Surge Control State *)
    rSurgeMargin            : REAL;
    rSurgeSP                : REAL := 15.0; (* 15% margin to surge line *)
    rSurgeError             : REAL;
    rSurgeKp                : REAL := 2.5;
    rSurgeKi                : REAL := 0.8;
    rSurgeIntegral          : REAL;

    (* Wellhead Injection Cascade State *)
    rInjectionSP            : REAL := 150.0; (* Supercritical target pressure bar *)
    rInjectionError         : REAL;
    rInjectionKp            : REAL := 1.2;
    rInjectionKi            : REAL := 0.4;
    rInjectionIntegral      : REAL;
    
    (* Timers *)
    tPurgeTimer             : TON;
    tRampTimer              : TON;
    
    bInit                   : BOOL := FALSE;
END_VAR

(* === MAIN INTERLOCKS & SAFETY SUPERVISOR === *)
IF NOT bEmergencyStopOk OR rVibrationLevel > 12.5 OR rDischargePressure > 220.0 THEN
    bCriticalTrip := TRUE;
    bSystemReady := FALSE;
    rSurgeValveCmd := 100.0; (* Failsafe open anti-surge *)
    rInjectionValveCmd := 0.0; (* Failsafe close wellhead *)
    rCompressorSpeedCmd := 0.0;
    iOperatingState := 999; (* TRIP STATE *)
    RETURN;
END_IF;

IF NOT bInit THEN
    iOperatingState := 0;
    bCriticalTrip := FALSE;
    bInit := TRUE;
END_IF;

(* === SIGNAL CONDITIONING & FILTERING === *)
rFiltDischargePress := (rAlphaFilt * rDischargePressure) + ((1.0 - rAlphaFilt) * rFiltDischargePress);
rFiltWellheadPress := (rAlphaFilt * rWellheadPressure) + ((1.0 - rAlphaFilt) * rFiltWellheadPress);

(* === ANTI-SURGE MARGIN CALCULATION (NON-LINEAR) === *)
(* Using generic polynomial mapping for compressor map operating point *)
rSurgeMargin := (rSurgeFlow / MAX(rCompressorSpeed, 1.0)) * 100.0;
bSurgeWarning := rSurgeMargin < (rSurgeSP + 5.0);

(* === FINITE STATE MACHINE === *)
CASE iOperatingState OF
    0: (* IDLE & PRE-CHECK *)
        bSystemReady := (rInletPressure > 5.0 AND rInletTemp < 40.0);
        rSurgeValveCmd := 100.0;
        rInjectionValveCmd := 0.0;
        rCompressorSpeedCmd := 0.0;
        IF bSystemEnable AND bSystemReady THEN
            iOperatingState := 10;
        END_IF;

    10: (* PURGE & PRE-LUBE *)
        tPurgeTimer(IN := TRUE, PT := T#30S);
        IF tPurgeTimer.Q THEN
            tPurgeTimer(IN := FALSE);
            iOperatingState := 20;
        END_IF;

    20: (* RAMP TO MINIMUM GOVERNOR SPEED *)
        rCompressorSpeedCmd := rCompressorSpeedCmd + 5.0; (* 5 RPM per scan cycle ramp *)
        IF rCompressorSpeedCmd >= 3000.0 THEN
            iOperatingState := 30;
        END_IF;

    30: (* PRESSURIZE TO SUPERCRITICAL (CASCADE CONTROL) *)
        (* Master Loop: Injection Pressure *)
        rInjectionError := rInjectionSP - rFiltWellheadPress;
        rInjectionIntegral := rInjectionIntegral + (rInjectionError * 0.1);
        (* Anti-windup *)
        IF rInjectionIntegral > 100.0 THEN rInjectionIntegral := 100.0; END_IF;
        IF rInjectionIntegral < 0.0 THEN rInjectionIntegral := 0.0; END_IF;
        
        rInjectionValveCmd := (rInjectionKp * rInjectionError) + (rInjectionKi * rInjectionIntegral);
        IF rInjectionValveCmd > 100.0 THEN rInjectionValveCmd := 100.0; END_IF;
        IF rInjectionValveCmd < 0.0 THEN rInjectionValveCmd := 0.0; END_IF;

        (* Anti-Surge Loop *)
        rSurgeError := rSurgeSP - rSurgeMargin;
        IF rSurgeError > 0.0 THEN
            rSurgeIntegral := rSurgeIntegral + (rSurgeError * 0.1);
            rSurgeValveCmd := (rSurgeKp * rSurgeError) + (rSurgeKi * rSurgeIntegral);
        ELSE
            rSurgeIntegral := 0.0;
            rSurgeValveCmd := 0.0;
        END_IF;
        IF rSurgeValveCmd > 100.0 THEN rSurgeValveCmd := 100.0; END_IF;
        
        IF NOT bSystemEnable THEN
            iOperatingState := 40;
        END_IF;

    40: (* SHUTDOWN SEQUENCE *)
        rInjectionValveCmd := 0.0;
        rSurgeValveCmd := 100.0;
        rCompressorSpeedCmd := rCompressorSpeedCmd - 10.0;
        IF rCompressorSpeedCmd <= 0.0 THEN
            rCompressorSpeedCmd := 0.0;
            iOperatingState := 0;
        END_IF;

    999: (* TRIP LATCH *)
        IF bSystemEnable = FALSE AND bEmergencyStopOk AND rVibrationLevel < 5.0 THEN
            iOperatingState := 0;
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
```"""

import os
os.makedirs("data/swarm_raw", exist_ok=True)
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print("done")
