import json
import uuid
import os

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Next-Gen Subsea Hydrothermal Vent Mineral Mining Crawler**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Abyssal track slip traction compensation, hyperbaric hydraulic actuator compensation mapping, and acoustic telemetry bandwidth optimization). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_Subsea_MiningCrawler\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Next-Gen Subsea Hydrothermal Vent Mineral Mining Crawler

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_Subsea_MiningCrawler
VAR_INPUT
    bEnableSystem          : BOOL;     (* Main enable signal from surface control *)
    bEmergencyAscent       : BOOL;     (* Trigger emergency ballast drop and immediate ascent *)
    rDepthPressure         : REAL;     (* Current ambient pressure in Bar, typically > 300 Bar *)
    rTrackSlipPort         : REAL;     (* Slip percentage on port track (0.0 to 100.0) *)
    rTrackSlipStbd         : REAL;     (* Slip percentage on starboard track (0.0 to 100.0) *)
    rPitchAngle            : REAL;     (* Vehicle pitch angle in degrees (-90.0 to +90.0) *)
    rRollAngle             : REAL;     (* Vehicle roll angle in degrees (-90.0 to +90.0) *)
    rHydraulicTemp         : REAL;     (* Temperature of hydraulic fluid in Deg C *)
    rHydraulicPressure     : REAL;     (* System hydraulic pressure in Bar *)
END_VAR
VAR_OUTPUT
    bSystemReady           : BOOL;     (* Crawler is ready for autonomous operations *)
    bCriticalFault         : BOOL;     (* Critical fault requiring immediate abort *)
    rTractionCmdPort       : REAL;     (* Torque command for port track motor (Nm) *)
    rTractionCmdStbd       : REAL;     (* Torque command for starboard track motor (Nm) *)
    rHydraulicValveCmd     : REAL;     (* Compensated hydraulic valve opening (0-100%) *)
    bAcousticBeaconActive  : BOOL;     (* Acoustic emergency telemetry beacon status *)
END_VAR
VAR
    iState                 : INT := 0; (* Internal state machine state *)
    rFilteredPitch         : REAL := 0.0;
    rFilteredRoll          : REAL := 0.0;
    rSlipThreshold         : REAL := 15.0; (* Slip percentage above which traction is reduced *)
    rMaxTraction           : REAL := 5000.0; (* Maximum allowed torque in Nm *)
    
    tHydraulicWarmup       : TON;
    tFaultTimer            : TON;
    tAcousticPing          : TON;
    
    bOverTempFault         : BOOL;
    bHyperbaricFault       : BOOL;
END_VAR

(* === MAIN LOGIC === *)
(* 1. Safety and Interlocks *)
IF bEmergencyAscent THEN
    bCriticalFault := TRUE;
    bSystemReady := FALSE;
    rTractionCmdPort := 0.0;
    rTractionCmdStbd := 0.0;
    bAcousticBeaconActive := TRUE;
    iState := 999;
    RETURN;
END_IF;

(* Continuous sensor filtering (simple exponential moving average for noise rejection) *)
rFilteredPitch := (rFilteredPitch * 0.9) + (rPitchAngle * 0.1);
rFilteredRoll := (rFilteredRoll * 0.9) + (rRollAngle * 0.1);

(* Fault evaluations *)
bOverTempFault := (rHydraulicTemp > 85.0);
bHyperbaricFault := (rDepthPressure > 450.0); (* Rated to 4000m depth, ~400 Bar + margin *)

IF bOverTempFault OR bHyperbaricFault THEN
    tFaultTimer(IN := TRUE, PT := T#2S);
    IF tFaultTimer.Q THEN
        bCriticalFault := TRUE;
        iState := 999; (* Enter fault state *)
    END_IF;
ELSE
    tFaultTimer(IN := FALSE);
END_IF;

(* 2. State Machine *)
CASE iState OF
    0: (* IDLE & WARMUP *)
        bSystemReady := FALSE;
        rTractionCmdPort := 0.0;
        rTractionCmdStbd := 0.0;
        rHydraulicValveCmd := 0.0;
        
        IF bEnableSystem AND NOT bCriticalFault THEN
            (* Wait for hydraulics to stabilize *)
            tHydraulicWarmup(IN := TRUE, PT := T#10S);
            IF tHydraulicWarmup.Q THEN
                tHydraulicWarmup(IN := FALSE);
                iState := 10;
            END_IF;
        ELSE
            tHydraulicWarmup(IN := FALSE);
        END_IF;
        
    10: (* ACTIVE TRACTION CONTROL AND COMPENSATION *)
        bSystemReady := TRUE;
        bCriticalFault := FALSE;
        
        (* Hyperbaric hydraulic actuator compensation mapping based on ambient pressure *)
        (* Nominal valve command scaled by differential pressure constraints *)
        IF rDepthPressure > 100.0 THEN
            rHydraulicValveCmd := 50.0 + (rDepthPressure * 0.05); 
        ELSE
            rHydraulicValveCmd := 50.0;
        END_IF;
        
        (* Abyssal track slip traction compensation *)
        IF rTrackSlipPort > rSlipThreshold THEN
            rTractionCmdPort := rMaxTraction * (1.0 - ((rTrackSlipPort - rSlipThreshold) / 100.0));
        ELSE
            rTractionCmdPort := rMaxTraction;
        END_IF;
        
        IF rTrackSlipStbd > rSlipThreshold THEN
            rTractionCmdStbd := rMaxTraction * (1.0 - ((rTrackSlipStbd - rSlipThreshold) / 100.0));
        ELSE
            rTractionCmdStbd := rMaxTraction;
        END_IF;
        
        (* Attitude adjustments - reduce torque on extreme slopes *)
        IF ABS(rFilteredPitch) > 30.0 OR ABS(rFilteredRoll) > 20.0 THEN
            rTractionCmdPort := rTractionCmdPort * 0.5;
            rTractionCmdStbd := rTractionCmdStbd * 0.5;
        END_IF;
        
        (* Acoustic telemetry bandwidth optimization - ping only on significant attitude changes *)
        tAcousticPing(IN := TRUE, PT := T#5S);
        IF tAcousticPing.Q THEN
            bAcousticBeaconActive := TRUE;
            tAcousticPing(IN := FALSE);
        ELSE
            bAcousticBeaconActive := FALSE;
        END_IF;

        IF NOT bEnableSystem THEN
            iState := 0;
        END_IF;
        
    999: (* FAULT / EMERGENCY STATE *)
        bSystemReady := FALSE;
        rTractionCmdPort := 0.0;
        rTractionCmdStbd := 0.0;
        rHydraulicValveCmd := 0.0;
        
        (* Emergency beacon always active in fault *)
        bAcousticBeaconActive := TRUE;

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
