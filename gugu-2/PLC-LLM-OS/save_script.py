import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: High-Volume Semiconductor Wet Bench Megasonic Cleaning and Chemical Spiking Interlock**

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
   prompt = \"\"\"<copy this exact user prompt here>\"\"\"
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_WetBench_Megasonic\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: High-Volume Semiconductor Wet Bench Megasonic Cleaning and Chemical Spiking Interlock

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_WetBench_Megasonic
VAR_INPUT
    (* Required: at least 4-8 physical inputs with types and comments *)
    bEnable               : BOOL;     (* System master enable signal *)
    bEmergencyStop_OK     : BOOL;     (* Safety relay OK signal (active HIGH for OK state) *)
    rProcessTemp          : REAL;     (* Bath physical measurement in degrees Celsius *)
    rConcentrationH2O2    : REAL;     (* Chemical concentration measurement in wt% *)
    rMegasonicPwrFwd      : REAL;     (* Forward power feedback from RF generator (Watts) *)
    rMegasonicPwrRev      : REAL;     (* Reflected power feedback from RF generator (Watts) *)
    bWaferCarrierPresent  : BOOL;     (* Wafer cassette optical sensor detection *)
END_VAR
VAR_OUTPUT
    (* Required: at least 3-6 outputs with types and comments *)
    bSystemReady          : BOOL;     (* System ready status for SECS/GEM host communication *)
    rControlPowerSp       : REAL;     (* Control signal setpoint to megasonic generator (0-1000W) *)
    rChemSpikeValvePos    : REAL;     (* Analog spiking valve position control (0-100%) *)
    bHeaterInterlock      : BOOL;     (* Hardware interlock relay for quartz inline heater *)
    bAlarm                : BOOL;     (* Fault alarm output to light tower and host *)
    iCurrentState         : INT;      (* State machine diagnostics tracker for HMI display *)
END_VAR
VAR
    (* Internal state variables and timers *)
    iState                : INT := 0;
    tProcessTimer         : TON;
    tSpikeSettleTimer     : TON;
    rConcentrationFiltered: REAL := 0.0;
    rFilterAlpha          : REAL := 0.15;  (* EMA filter coefficient for noise suppression *)
    rReflectedRatio       : REAL := 0.0;
    rPowerRampRate        : REAL := 25.0;  (* Ramp rate in Watts per PLC cycle/second *)
    rTargetPower          : REAL := 850.0; (* Nominal processing megasonic power *)
    rSpikeKp              : REAL := 15.0;  (* Proportional gain for chemical spiking valve *)
    rTargetTemp           : REAL := 65.0;  (* Target process temperature in degrees C *)
    rTargetConc           : REAL := 4.5;   (* Target H2O2 concentration in wt% *)
    bFirstCycle           : BOOL := TRUE;
END_VAR

(* === MAIN LOGIC === *)
(* Initialization and First Cycle Handling *)
IF bFirstCycle THEN
    rConcentrationFiltered := rConcentrationH2O2; (* Initialize filter *)
    bFirstCycle := FALSE;
END_IF;

(* Exponential Moving Average Filter for Chemical Concentration Noise Reduction *)
rConcentrationFiltered := (rFilterAlpha * rConcentrationH2O2) + ((1.0 - rFilterAlpha) * rConcentrationFiltered);

(* VSWR / Reflected Power Calculation for Dry Fire and Transducer Protection *)
IF rMegasonicPwrFwd > 10.0 THEN
    rReflectedRatio := rMegasonicPwrRev / (rMegasonicPwrFwd + 0.01);
ELSE
    rReflectedRatio := 0.0;
END_IF;

(* Multi-layered Safety Interlocks (Overrides all active states) *)
IF NOT bEmergencyStop_OK THEN
    iState := 99; (* Force Fault State: Safety Loop Broken *)
ELSIF rProcessTemp > 85.0 THEN
    iState := 99; (* Force Fault State: Thermal Runaway Detected *)
ELSIF rReflectedRatio > 0.15 AND iState = 40 THEN
    iState := 99; (* Force Fault State: High Reflected Power (Transducer mismatch/dry) *)
END_IF;

CASE iState OF
    0: (* IDLE - Await start conditions *)
        bSystemReady := FALSE;
        bAlarm := FALSE;
        bHeaterInterlock := FALSE;
        rControlPowerSp := 0.0;
        rChemSpikeValvePos := 0.0;
        tProcessTimer(IN := FALSE);
        tSpikeSettleTimer(IN := FALSE);
        
        IF bEnable AND bWaferCarrierPresent AND bEmergencyStop_OK THEN
            iState := 10;
        END_IF;

    10: (* HEATER ENABLE & THERMAL STABILIZATION *)
        bHeaterInterlock := TRUE; (* Permit external PID heater loop *)
        IF rProcessTemp >= (rTargetTemp - 1.5) AND rProcessTemp <= (rTargetTemp + 1.5) THEN
            iState := 20;
        END_IF;
        
    20: (* CHEMICAL SPIKING (PROPORTIONAL CONTROL ALGORITHM) *)
        IF rConcentrationFiltered < (rTargetConc - 0.1) THEN
            rChemSpikeValvePos := (rTargetConc - rConcentrationFiltered) * rSpikeKp;
            (* Saturate Analog Valve Output *)
            IF rChemSpikeValvePos > 100.0 THEN
                rChemSpikeValvePos := 100.0;
            ELSIF rChemSpikeValvePos < 0.0 THEN
                rChemSpikeValvePos := 0.0;
            END_IF;
            tSpikeSettleTimer(IN := FALSE);
        ELSE
            rChemSpikeValvePos := 0.0; (* Close spiking valve *)
            tSpikeSettleTimer(IN := TRUE, PT := T#10S); (* Allow concentration to settle *)
            IF tSpikeSettleTimer.Q THEN
                iState := 30;
            END_IF;
        END_IF;
        
    30: (* MEGASONIC POWER CONTROLLED RAMP-UP *)
        rControlPowerSp := rControlPowerSp + rPowerRampRate;
        IF rControlPowerSp >= rTargetPower THEN
            rControlPowerSp := rTargetPower;
            tProcessTimer(IN := FALSE); (* Reset Timer *)
            iState := 40;
        END_IF;
        
    40: (* MEGASONIC PROCESS HOLD AND MONITORING *)
        bSystemReady := TRUE; (* Indicate to host that active processing is occurring *)
        rControlPowerSp := rTargetPower;
        tProcessTimer(IN := TRUE, PT := T#300S); (* 5 Minute Acoustic Cleaning Process *)
        
        IF tProcessTimer.Q THEN
            tProcessTimer(IN := FALSE);
            iState := 50;
        END_IF;
        
    50: (* MEGASONIC POWER RAMP-DOWN *)
        bSystemReady := FALSE;
        rControlPowerSp := rControlPowerSp - (rPowerRampRate * 2.0); (* Fast ramp down *)
        IF rControlPowerSp <= 0.0 THEN
            rControlPowerSp := 0.0;
            iState := 60;
        END_IF;
        
    60: (* PROCESS COMPLETE AND WAFER UNLOAD WAIT *)
        bHeaterInterlock := FALSE; (* Secure heater *)
        IF NOT bWaferCarrierPresent THEN
            iState := 0; (* Cassette removed, return to idle *)
        END_IF;
        
    99: (* CRITICAL FAULT HANDLING *)
        bSystemReady := FALSE;
        bAlarm := TRUE;
        rControlPowerSp := 0.0; (* Immediate RF shutdown *)
        rChemSpikeValvePos := 0.0; (* Isolate chemical supply *)
        bHeaterInterlock := FALSE; (* Immediate heater shutdown *)
        tProcessTimer(IN := FALSE);
        tSpikeSettleTimer(IN := FALSE);
        
        (* Latch fault until master enable is toggled low while safety is OK *)
        IF bEmergencyStop_OK AND NOT bEnable THEN
            iState := 0;
        END_IF;

END_CASE;

(* Output internal state for external SECS/GEM host reporting *)
iCurrentState := iState;

END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
