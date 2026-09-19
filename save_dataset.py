import json, uuid

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Automated Superconducting Magnetic Energy Storage (SMES) Cryocooler Flow and Quench Detection**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_SMES_CryoControl\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Automated Superconducting Magnetic Energy Storage (SMES) Cryocooler Flow and Quench Detection

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_SMES_CryoControl
VAR_INPUT
    bSystemEnable           : BOOL;     (* Main system enable command *)
    bEmergencyStop          : BOOL;     (* Hardware E-stop relay status (Active Low) *)
    rCoilTempK              : REAL;     (* Superconducting coil temperature in Kelvin *)
    rCoolantFlowRate        : REAL;     (* Helium flow rate in L/min *)
    rCoilVoltage            : REAL;     (* Voltage across SMES coil, used for quench detection *)
    rCoilCurrent            : REAL;     (* Current through SMES coil in Amperes *)
    rHeliumPressure         : REAL;     (* Cryostat helium pressure in Bar *)
    rAmbientTempC           : REAL;     (* Ambient room temperature in Celsius *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;     (* True when cryocooler is running and coil is at target temp *)
    rFlowControlValve       : REAL;     (* 0-100% control signal to proportional helium flow valve *)
    bQuenchDetected         : BOOL;     (* Critical flag indicating a quench event is occurring *)
    bDumpEnergyCmd          : BOOL;     (* Command to fast-discharge energy to dump resistors *)
    bAlarmHighTemp          : BOOL;     (* Warning alarm for coil temperature approaching critical T_c *)
    iOperatingState         : INT;      (* Current state of the SMES thermal management system *)
END_VAR
VAR
    (* Internal State Variables *)
    iState                  : INT := 0; (* 0=IDLE, 10=PRE_COOL, 20=STEADY_STATE, 99=QUENCH_FAULT *)
    
    (* Timers and Filters *)
    tPrecoolTimer           : TON;
    tQuenchConfirmTimer     : TON;
    
    (* Filtered Measurements *)
    rFiltCoilTemp           : REAL;
    rFiltCoilVoltage        : REAL;
    rFiltFlowRate           : REAL;
    
    (* Constants *)
    T_CRITICAL_K            : REAL := 4.2;  (* Critical temperature for Niobium-Titanium in Liquid Helium *)
    V_QUENCH_THRESH         : REAL := 0.05; (* Voltage threshold for quench detection (resistive zone formation) *)
    FLOW_TARGET_LPM         : REAL := 15.0;
    
    (* PID Variables for Flow Control *)
    rErrorFlow              : REAL;
    rIntegralFlow           : REAL;
    rDerivativeFlow         : REAL;
    rLastErrorFlow          : REAL;
    Kp                      : REAL := 2.5;
    Ki                      : REAL := 0.1;
    Kd                      : REAL := 0.05;
    rDt                     : REAL := 0.01; (* 10ms cycle time *)
END_VAR

(* === MAIN LOGIC === *)

(* 1. Safety and Hardware Interlocks *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bQuenchDetected := FALSE;
    bDumpEnergyCmd := TRUE; (* Fail-safe: discharge energy if E-Stop is hit *)
    rFlowControlValve := 100.0; (* Open valve fully to flood cryostat *)
    iOperatingState := -1;
    RETURN;
END_IF;

(* 2. Sensor Noise Filtering (Exponential Moving Average) *)
rFiltCoilTemp := (rCoilTempK * 0.1) + (rFiltCoilTemp * 0.9);
rFiltCoilVoltage := (rCoilVoltage * 0.2) + (rFiltCoilVoltage * 0.8);
rFiltFlowRate := (rCoolantFlowRate * 0.15) + (rFiltFlowRate * 0.85);

(* 3. Quench Detection Logic (Resistive Voltage + Temp Rise) *)
IF (ABS(rFiltCoilVoltage) > V_QUENCH_THRESH) AND (rFiltCoilTemp > (T_CRITICAL_K - 0.5)) THEN
    tQuenchConfirmTimer(IN := TRUE, PT := T#50MS);
ELSE
    tQuenchConfirmTimer(IN := FALSE, PT := T#50MS);
END_IF;

IF tQuenchConfirmTimer.Q THEN
    bQuenchDetected := TRUE;
    iState := 99; (* Transition to fault state immediately *)
END_IF;

(* 4. State Machine for Thermal Management *)
CASE iState OF
    0: (* IDLE *)
        bSystemReady := FALSE;
        rFlowControlValve := 0.0;
        bDumpEnergyCmd := FALSE;
        IF bSystemEnable THEN
            iState := 10;
        END_IF;

    10: (* PRE_COOLING *)
        bSystemReady := FALSE;
        (* Aggressive cooling during pre-cool phase *)
        rFlowControlValve := 80.0;
        
        IF rFiltCoilTemp <= T_CRITICAL_K THEN
            tPrecoolTimer(IN := TRUE, PT := T#10S);
            IF tPrecoolTimer.Q THEN
                tPrecoolTimer(IN := FALSE);
                iState := 20;
            END_IF;
        ELSE
            tPrecoolTimer(IN := FALSE);
        END_IF;

    20: (* STEADY_STATE_OPERATION *)
        bSystemReady := TRUE;
        
        (* Advanced PID Flow Control to maintain exact target flow rate *)
        rErrorFlow := FLOW_TARGET_LPM - rFiltFlowRate;
        rIntegralFlow := rIntegralFlow + (rErrorFlow * rDt);
        rDerivativeFlow := (rErrorFlow - rLastErrorFlow) / rDt;
        
        rFlowControlValve := (Kp * rErrorFlow) + (Ki * rIntegralFlow) + (Kd * rDerivativeFlow);
        
        (* Anti-windup and clamping *)
        IF rFlowControlValve > 100.0 THEN
            rFlowControlValve := 100.0;
            rIntegralFlow := rIntegralFlow - (rErrorFlow * rDt);
        ELSIF rFlowControlValve < 10.0 THEN
            rFlowControlValve := 10.0;
        END_IF;
        
        rLastErrorFlow := rErrorFlow;
        
        (* Thermal Warning *)
        IF rFiltCoilTemp > (T_CRITICAL_K - 0.2) THEN
            bAlarmHighTemp := TRUE;
            rFlowControlValve := 100.0; (* Over-ride PID, max cooling *)
        ELSE
            bAlarmHighTemp := FALSE;
        END_IF;
        
        IF NOT bSystemEnable THEN
            iState := 0;
        END_IF;

    99: (* QUENCH_FAULT - Critical Protection Sequence *)
        bSystemReady := FALSE;
        bDumpEnergyCmd := TRUE;     (* Divert massive current to dump resistors *)
        rFlowControlValve := 100.0; (* Maximum helium flow to mitigate thermal runaway *)
        
        (* Latch fault until manual reset / power cycle *)

END_CASE;

iOperatingState := iState;

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
