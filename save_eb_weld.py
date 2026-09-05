import os
import json
import uuid

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Commercial Aircraft Jet Engine Electron Beam (EB) Welding Chamber**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., High-vacuum (10^-5 mbar) pump-down cascading sequences, 150kV electron gun beam deflection magnetic lens control, and precise multi-axis CNC seam tracking). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_ElectronBeamWelding\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Commercial Aircraft Jet Engine Electron Beam (EB) Welding Chamber

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_EB_Welding_Chamber
VAR_INPUT
    (* System & Safety Inputs *)
    bEnable               : BOOL;   (* System Master Enable *)
    bEmergencyStop        : BOOL;   (* Hardwired Safety Relay (Normally Closed) *)
    bReset                : BOOL;   (* Fault Reset Pushbutton *)
    
    (* Vacuum System Feedback *)
    rChamberPressure      : REAL;   (* Main chamber vacuum level [mbar] *)
    rGunPressure          : REAL;   (* Electron gun housing vacuum level [mbar] *)
    bRootsPumpRunning     : BOOL;   (* Roots blower status *)
    bTurboPumpRunning     : BOOL;   (* Turbomolecular pump status *)
    
    (* Welding Process Parameters *)
    rTargetHV             : REAL;   (* Desired Accelerating Voltage [kV], typically 150.0 *)
    rTargetBeamCurrent    : REAL;   (* Desired Beam Current [mA] *)
    rFocusLensCurrentReq  : REAL;   (* Target magnetic lens focus current [A] *)
    
    (* CNC Seam Tracking System *)
    rCNC_X_Pos            : REAL;   (* Current X-axis position [mm] *)
    rCNC_Y_Pos            : REAL;   (* Current Y-axis position [mm] *)
    rDeflectionCoilXReq   : REAL;   (* High-frequency X-deflection [mA] *)
    rDeflectionCoilYReq   : REAL;   (* High-frequency Y-deflection [mA] *)
END_VAR

VAR_OUTPUT
    (* System Status *)
    bSystemReady          : BOOL;   (* System is ready for welding *)
    bAlarm                : BOOL;   (* Fault or Interlock tripped *)
    wFaultCode            : WORD;   (* Hexadecimal fault indicator code *)
    
    (* Vacuum Control Commands *)
    bCmdRoughingValve     : BOOL;   (* Open roughing line valve *)
    bCmdHighVacuumValve   : BOOL;   (* Open main high-vacuum gate valve *)
    
    (* Electron Gun Controls *)
    rHighVoltageCtrl      : REAL;   (* Command to HV generator [kV] *)
    rBeamCurrentCtrl      : REAL;   (* Command to filament/grid [mA] *)
    rFocusLensCurrent     : REAL;   (* Command to focusing magnetic lens [A] *)
    rDeflectionCoilX      : REAL;   (* Deflection drive X [mA] *)
    rDeflectionCoilY      : REAL;   (* Deflection drive Y [mA] *)
END_VAR

VAR
    (* Internal State Machine *)
    iState                : INT := 0; 
    
    (* Timers & Triggers *)
    tPumpDownTimer        : TON;
    tHVRampTimer          : TON;
    tStabilizationTimer   : TON;
    rrtResetEdge          : R_TRIG;
    
    (* Internal Registers for Ramping *)
    rCurrentHV            : REAL := 0.0;
    rHVRampRate           : REAL := 2.5; (* kV per scan/timer tick limit *)
    
    (* Constants for Vacuum Interlocks *)
    c_rMaxGunPressure     : REAL := 1.0E-5;  (* 10^-5 mbar required for HV on *)
    c_rMaxChamberPressure : REAL := 5.0E-4;  (* 5x10^-4 mbar for roughing complete *)
END_VAR

(* =========================================================================
   MAIN LOGIC - COMMERCIAL AIRCRAFT JET ENGINE EB WELDING CHAMBER
   ========================================================================= *)

(* Edge Detection for Reset *)
rrtResetEdge(CLK := bReset);
IF rrtResetEdge.Q AND iState = 99 THEN
    wFaultCode := 16#0000;
    bAlarm := FALSE;
    iState := 0;
END_IF;

(* Safety & Interlock Watchdog (Highest Priority) *)
IF NOT bEmergencyStop THEN
    bSystemReady        := FALSE;
    bCmdRoughingValve   := FALSE;
    bCmdHighVacuumValve := FALSE;
    rHighVoltageCtrl    := 0.0;
    rBeamCurrentCtrl    := 0.0;
    rCurrentHV          := 0.0;
    bAlarm              := TRUE;
    wFaultCode          := 16#E570; (* E-STOP Fault Code *)
    iState              := 99;
    RETURN;
END_IF;

(* Vacuum Loss Interlock During Operation *)
IF iState >= 30 AND iState < 90 THEN
    IF rGunPressure > (c_rMaxGunPressure * 1.5) OR rChamberPressure > (c_rMaxChamberPressure * 2.0) THEN
        rHighVoltageCtrl := 0.0; (* Immediate HV Cutoff to protect filament *)
        rBeamCurrentCtrl := 0.0;
        wFaultCode := 16#VAC1; (* Vacuum loss fault *)
        iState := 99;
    END_IF;
END_IF;

(* Main State Machine *)
CASE iState OF
    
    0: (* IDLE & SAFE STATE *)
        bSystemReady := FALSE;
        rHighVoltageCtrl := 0.0;
        rBeamCurrentCtrl := 0.0;
        rFocusLensCurrent := 0.0;
        IF bEnable THEN
            iState := 10;
        END_IF;

    10: (* ROUGHING PUMP DOWN SEQUENCE *)
        bCmdRoughingValve := TRUE;
        tPumpDownTimer(IN := TRUE, PT := T#5M);
        
        IF rChamberPressure <= c_rMaxChamberPressure THEN
            tPumpDownTimer(IN := FALSE);
            iState := 20;
        ELSIF tPumpDownTimer.Q THEN
            (* Pump down timeout *)
            wFaultCode := 16#7001; 
            iState := 99;
        END_IF;

    20: (* HIGH VACUUM GUN PUMP DOWN SEQUENCE *)
        bCmdHighVacuumValve := TRUE;
        bCmdRoughingValve := FALSE; (* Handover to Turbo *)
        tPumpDownTimer(IN := TRUE, PT := T#15M);
        
        IF (rGunPressure <= c_rMaxGunPressure) AND bTurboPumpRunning THEN
            tPumpDownTimer(IN := FALSE);
            iState := 30;
        ELSIF tPumpDownTimer.Q THEN
            wFaultCode := 16#7002;
            iState := 99;
        END_IF;

    30: (* HV RAMP GENERATOR (150kV max) *)
        tHVRampTimer(IN := TRUE, PT := T#100MS);
        IF tHVRampTimer.Q THEN
            tHVRampTimer(IN := FALSE);
            IF rCurrentHV < rTargetHV THEN
                rCurrentHV := rCurrentHV + rHVRampRate;
                IF rCurrentHV > rTargetHV THEN
                    rCurrentHV := rTargetHV;
                END_IF;
            ELSIF rCurrentHV > rTargetHV THEN
                rCurrentHV := rCurrentHV - rHVRampRate;
            END_IF;
            
            rHighVoltageCtrl := rCurrentHV;
        END_IF;
        
        IF ABS(rCurrentHV - rTargetHV) < 0.5 THEN
            iState := 40;
        END_IF;

    40: (* LENS FOCUS AND BEAM STABILIZATION *)
        rFocusLensCurrent := rFocusLensCurrentReq;
        tStabilizationTimer(IN := TRUE, PT := T#3S);
        IF tStabilizationTimer.Q THEN
            tStabilizationTimer(IN := FALSE);
            bSystemReady := TRUE;
            iState := 50;
        END_IF;

    50: (* WELDING / ACTIVE BEAM DEFLECTION & CURRENT CONTROL *)
        (* High-Frequency magnetic deflection tracking *)
        rDeflectionCoilX := rDeflectionCoilXReq;
        rDeflectionCoilY := rDeflectionCoilYReq;
        
        (* Closed-loop emission current mapping *)
        rBeamCurrentCtrl := rTargetBeamCurrent;
        
        IF NOT bEnable THEN
            bSystemReady := FALSE;
            rBeamCurrentCtrl := 0.0;
            iState := 60; (* Ramp down *)
        END_IF;
        
    60: (* HV RAMP DOWN *)
        tHVRampTimer(IN := TRUE, PT := T#100MS);
        IF tHVRampTimer.Q THEN
            tHVRampTimer(IN := FALSE);
            rCurrentHV := rCurrentHV - (rHVRampRate * 2.0); (* Faster ramp down *)
            IF rCurrentHV <= 0.0 THEN
                rCurrentHV := 0.0;
                iState := 0;
            END_IF;
            rHighVoltageCtrl := rCurrentHV;
        END_IF;

    99: (* FAULT HANDLING *)
        bAlarm := TRUE;
        bSystemReady := FALSE;
        rHighVoltageCtrl := 0.0;
        rBeamCurrentCtrl := 0.0;
        rFocusLensCurrent := 0.0;
        rDeflectionCoilX := 0.0;
        rDeflectionCoilY := 0.0;
        bCmdRoughingValve := FALSE;
        bCmdHighVacuumValve := FALSE;
        tPumpDownTimer(IN := FALSE);
        tHVRampTimer(IN := FALSE);
        tStabilizationTimer(IN := FALSE);
        (* Wait for Reset via rrtResetEdge *)

END_CASE;

END_FUNCTION_BLOCK
```"""

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
