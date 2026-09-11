import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Advanced Semiconductor Rapid Thermal Processing (RTP) Chamber**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., 10,000-Watt halogen lamp multi-zone pyrometric feedback, 100°C/sec transient wafer ramping, and inert gas cross-flow boundary layer stabilization). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

CRITICAL RULES - READ EVERY LINE:
1. CODE FENCE: Use TRIPLE backticks + iec-st. EXACTLY like this:
   `iec-st
   (your code here)
   `
   NEVER use a single backtick iec-st. ALWAYS use triple backticks.
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
   code = \"\"\"`iec-st\\nFUNCTION_BLOCK FB_RTP_Chamber\\n//...\\nEND_FUNCTION_BLOCK\\n`\"\"\"
   record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
   with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
       json.dump(record, f, ensure_ascii=False)
5. SELF-CHECK before saving - verify ALL:
   [ ] Fence is `iec-st
   [ ] First code line: FUNCTION_BLOCK FB_<name>
   [ ] Has VAR_INPUT section
   [ ] Has VAR_OUTPUT section
   [ ] Has END_IF; or END_CASE;
   [ ] Last code line: END_FUNCTION_BLOCK
   [ ] Closing fence: `
   [ ] Total chars >= 1500
6. REPLY with: EVOLUTION COMPLETE: Advanced Semiconductor Rapid Thermal Processing (RTP) Chamber

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """`iec-st
FUNCTION_BLOCK FB_RTP_Chamber_AdvancedControl
(* ==============================================================================
   Block:      FB_RTP_Chamber_AdvancedControl
   Author:     Lumina Elite Automation Architect
   Date:       2026-09-11
   Version:    V4.0 (Mission-Critical)
   Desc:       Multi-Zone Rapid Thermal Processing (RTP) Control with 
               Pyrometric Feedback, 100°C/s Transient Ramp, and Inert Gas Cross-Flow.
               Includes advanced noise filtering (EMA), PID scheduling, and Safety.
   ============================================================================== *)

VAR_INPUT
    bEnable                 : BOOL;     (* System enable & safety OK interlock *)
    bEmergencyStop          : BOOL;     (* Hardware E-Stop (Active Low) *)
    bStartRecipe            : BOOL;     (* Trigger for RTP thermal cycle *)
    rWaferTempPyr1          : REAL;     (* Pyrometer 1 reading (Center Zone) [°C] *)
    rWaferTempPyr2          : REAL;     (* Pyrometer 2 reading (Edge Zone) [°C] *)
    rWaferTempPyr3          : REAL;     (* Pyrometer 3 reading (Guard Zone) [°C] *)
    rChamberPressure        : REAL;     (* RTP Chamber pressure [mTorr] *)
    rPurgeGasFlow           : REAL;     (* Inert gas cross-flow measurement [SLM] *)
    rCoolantFlow            : REAL;     (* Quartz window cooling flow [L/min] *)
    rSetPointTarget         : REAL;     (* Final recipe target temperature [°C] *)
    rRampRate               : REAL;     (* Target ramp rate [°C/s] *)
END_VAR

VAR_OUTPUT
    bSystemReady            : BOOL;     (* System initialized and safe for recipe *)
    bRecipeActive           : BOOL;     (* Thermal cycle currently in progress *)
    bRecipeComplete         : BOOL;     (* Thermal cycle successfully finished *)
    rLampPowerCenter        : REAL;     (* Commanded 10kW Halogen array % - Center *)
    rLampPowerEdge          : REAL;     (* Commanded 10kW Halogen array % - Edge *)
    rLampPowerGuard         : REAL;     (* Commanded 10kW Halogen array % - Guard *)
    rGasValveCmd            : REAL;     (* Mass Flow Controller valve output 0-100% *)
    bChamberAlarm           : BOOL;     (* General fault indicator *)
    iErrorCode              : INT;      (* Diagnostics: 0=OK, >0=Fault Code *)
END_VAR

VAR
    (* Internal State Machine *)
    iState                  : INT := 0; 
    
    (* Filtered Sensors (Exponential Moving Average) *)
    rFiltWaferTempC         : REAL;
    rFiltWaferTempE         : REAL;
    rFiltWaferTempG         : REAL;
    
    (* Kinematics & Profiles *)
    rCurrentSetPoint        : REAL;
    tCycleTimer             : TON;
    tFaultTimer             : TON;
    rRampStep               : REAL;
    
    (* PID Controllers for 3 Zones (Simplified integration representation) *)
    rErrCenter, rErrEdge, rErrGuard : REAL;
    rIntegralC, rIntegralE, rIntegralG : REAL;
    
    (* Constants *)
    c_rAlphaFilter          : REAL := 0.2; (* EMA Filter coefficient *)
    c_rMaxTempDelta         : REAL := 25.0; (* Max allowable center-edge delta [°C] *)
    c_rMaxPower             : REAL := 100.0;
    c_rMinPressure          : REAL := 15.0; (* Minimum operational vacuum [mTorr] *)
    c_rMinCoolantFlow       : REAL := 8.5;  (* Coolant flow threshold [L/min] *)
    c_rSampleTime           : REAL := 0.01; (* 10ms execution cycle *)
    
    (* PID Gains *)
    Kp : REAL := 0.85;
    Ki : REAL := 0.12;
END_VAR

(* === MAIN SAFETY & INTERLOCKS === *)
IF NOT bEmergencyStop OR NOT bEnable THEN
    bSystemReady := FALSE;
    bRecipeActive := FALSE;
    bChamberAlarm := TRUE;
    iErrorCode := 101; (* Safety Interlock Tripped *)
    
    (* Immediate Lamp Shutdown *)
    rLampPowerCenter := 0.0;
    rLampPowerEdge   := 0.0;
    rLampPowerGuard  := 0.0;
    rGasValveCmd     := 100.0; (* Full purge on fault *)
    iState := 0;
    RETURN;
END_IF;

(* === SENSOR NOISE FILTERING (EMA) === *)
rFiltWaferTempC := (c_rAlphaFilter * rWaferTempPyr1) + ((1.0 - c_rAlphaFilter) * rFiltWaferTempC);
rFiltWaferTempE := (c_rAlphaFilter * rWaferTempPyr2) + ((1.0 - c_rAlphaFilter) * rFiltWaferTempE);
rFiltWaferTempG := (c_rAlphaFilter * rWaferTempPyr3) + ((1.0 - c_rAlphaFilter) * rFiltWaferTempG);

(* Process Fault Diagnostics *)
IF rChamberPressure < c_rMinPressure THEN
    bChamberAlarm := TRUE;
    iErrorCode := 201; (* Vacuum loss *)
    iState := 999;
END_IF;

IF rCoolantFlow < c_rMinCoolantFlow THEN
    bChamberAlarm := TRUE;
    iErrorCode := 202; (* Coolant loss *)
    iState := 999;
END_IF;

IF ABS(rFiltWaferTempC - rFiltWaferTempE) > c_rMaxTempDelta THEN
    bChamberAlarm := TRUE;
    iErrorCode := 301; (* Thermal Gradient Violation - Risk of slip/dislocation *)
    iState := 999;
END_IF;

(* === RTP STATE MACHINE === *)
CASE iState OF
    0: (* SYSTEM IDLE / INITIALIZATION *)
        bSystemReady := TRUE;
        bRecipeActive := FALSE;
        bRecipeComplete := FALSE;
        bChamberAlarm := FALSE;
        iErrorCode := 0;
        
        rLampPowerCenter := 0.0;
        rLampPowerEdge   := 0.0;
        rLampPowerGuard  := 0.0;
        
        (* Maintain baseline inert gas flow boundary layer *)
        rGasValveCmd := 25.0; 
        
        rCurrentSetPoint := 20.0; (* Ambient *)
        
        IF bStartRecipe AND bSystemReady THEN
            iState := 10;
        END_IF;

    10: (* RECIPE START & PRE-PURGE *)
        bSystemReady := FALSE;
        bRecipeActive := TRUE;
        rGasValveCmd := 85.0; (* High cross-flow to clear oxygen/moisture *)
        
        tCycleTimer(IN := TRUE, PT := T#5S);
        IF tCycleTimer.Q THEN
            tCycleTimer(IN := FALSE);
            rGasValveCmd := 40.0; (* Steady processing flow *)
            iState := 20;
        END_IF;

    20: (* DYNAMIC RAMPING (100 C/s Target) *)
        (* Calculate Ramp Step per 10ms execution cycle *)
        rRampStep := rRampRate * c_rSampleTime;
        rCurrentSetPoint := rCurrentSetPoint + rRampStep;
        
        IF rCurrentSetPoint >= rSetPointTarget THEN
            rCurrentSetPoint := rSetPointTarget;
            iState := 30;
        END_IF;
        
        (* Simple PID execution (P+I) for each zone *)
        rErrCenter := rCurrentSetPoint - rFiltWaferTempC;
        rIntegralC := rIntegralC + (rErrCenter * c_rSampleTime);
        rLampPowerCenter := (Kp * rErrCenter) + (Ki * rIntegralC);
        
        rErrEdge := rCurrentSetPoint - rFiltWaferTempE;
        rIntegralE := rIntegralE + (rErrEdge * c_rSampleTime);
        rLampPowerEdge := (Kp * rErrEdge) + (Ki * rIntegralE);
        
        rErrGuard := rCurrentSetPoint - rFiltWaferTempG;
        rIntegralG := rIntegralG + (rErrGuard * c_rSampleTime);
        rLampPowerGuard := (Kp * rErrGuard) + (Ki * rIntegralG);
        
        (* Saturate Outputs *)
        IF rLampPowerCenter > c_rMaxPower THEN rLampPowerCenter := c_rMaxPower; END_IF;
        IF rLampPowerEdge > c_rMaxPower THEN rLampPowerEdge := c_rMaxPower; END_IF;
        IF rLampPowerGuard > c_rMaxPower THEN rLampPowerGuard := c_rMaxPower; END_IF;
        IF rLampPowerCenter < 0.0 THEN rLampPowerCenter := 0.0; END_IF;
        IF rLampPowerEdge < 0.0 THEN rLampPowerEdge := 0.0; END_IF;
        IF rLampPowerGuard < 0.0 THEN rLampPowerGuard := 0.0; END_IF;

    30: (* SOAK / STEADY STATE *)
        tCycleTimer(IN := TRUE, PT := T#10S); (* Typical ultra-short soak *)
        
        (* Continue PID to maintain temp *)
        rErrCenter := rSetPointTarget - rFiltWaferTempC;
        rIntegralC := rIntegralC + (rErrCenter * c_rSampleTime);
        rLampPowerCenter := (Kp * rErrCenter) + (Ki * rIntegralC);
        
        rErrEdge := rSetPointTarget - rFiltWaferTempE;
        rIntegralE := rIntegralE + (rErrEdge * c_rSampleTime);
        rLampPowerEdge := (Kp * rErrEdge) + (Ki * rIntegralE);
        
        rErrGuard := rSetPointTarget - rFiltWaferTempG;
        rIntegralG := rIntegralG + (rErrGuard * c_rSampleTime);
        rLampPowerGuard := (Kp * rErrGuard) + (Ki * rIntegralG);
        
        IF tCycleTimer.Q THEN
            tCycleTimer(IN := FALSE);
            iState := 40;
        END_IF;

    40: (* CONTROLLED COOL DOWN *)
        rLampPowerCenter := 0.0;
        rLampPowerEdge   := 0.0;
        rLampPowerGuard  := 0.0;
        rGasValveCmd     := 100.0; (* Max cross-flow to aid convective cooling *)
        
        IF rFiltWaferTempC < 50.0 AND rFiltWaferTempE < 50.0 THEN
            bRecipeComplete := TRUE;
            bRecipeActive := FALSE;
            IF NOT bStartRecipe THEN
                iState := 0;
            END_IF;
        END_IF;

    999: (* FAULT HANDLING *)
        rLampPowerCenter := 0.0;
        rLampPowerEdge   := 0.0;
        rLampPowerGuard  := 0.0;
        bRecipeActive := FALSE;
        rGasValveCmd := 100.0; (* Fail-safe purge *)
        
        IF NOT bStartRecipe AND bEnable AND bEmergencyStop THEN
            (* Wait for operator reset *)
            IF rFiltWaferTempC < 100.0 THEN
                iState := 0;
            END_IF;
        END_IF;
END_CASE;

END_FUNCTION_BLOCK
``"""

import os
os.makedirs("data/swarm_raw", exist_ok=True)
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(filename)
