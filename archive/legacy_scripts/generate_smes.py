import os, json, uuid

prompt = """<USER_REQUEST>
You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Next-Gen Superconducting Magnetic Energy Storage (SMES) Cryostat**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., 4-Kelvin liquid helium thermosyphon circulation, NbTi coil quench detection and ultra-fast energy dump, and IGBT-based active power conditioning interface). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_SMES_Cryostat\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Next-Gen Superconducting Magnetic Energy Storage (SMES) Cryostat

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT.
</USER_REQUEST>"""

code = """```iec-st
FUNCTION_BLOCK FB_SMES_Cryostat_Control
VAR_INPUT
    (* System and Safety Enable Signals *)
    bSystemEnable       : BOOL;     (* Master activation command *)
    bEmergencyStop      : BOOL;     (* True if Safety chain is OK (closed) *)
    
    (* Cryogenic Thermosyphon Variables *)
    rLiquidHeTemp_K     : REAL;     (* Liquid Helium bath temperature [Kelvin] *)
    rCryostatPressure_Pa: REAL;     (* Absolute internal pressure [Pascal] *)
    
    (* Superconducting NbTi Coil Variables *)
    rCoilCurrent_A      : REAL;     (* Measured coil current [Amperes] *)
    rCoilVoltage_V      : REAL;     (* Differential coil voltage [Volts] *)
    rCoilCurrent_dIdt   : REAL;     (* Derivative of current over time [A/s] *)
    
    (* IGBT Power Conditioning Variables *)
    rDCLinkVoltage_V    : REAL;     (* Inverter DC link voltage [Volts] *)
    rGridFrequency_Hz   : REAL;     (* Synchronization grid frequency [Hz] *)
END_VAR
VAR_OUTPUT
    (* Cryogenic Actuators *)
    bHePumpEnable       : BOOL;     (* Circulation pump run command *)
    rCryoValve_PCV      : REAL;     (* Proportional cryo-valve position 0-100% *)
    
    (* Electrical Protection & Actuation *)
    bDumpBreakerCmd     : BOOL;     (* TRUE = Closed (Normal), FALSE = Open (Dump to Resistor) *)
    bQuenchAlarm        : BOOL;     (* Critical Quench Detected Flag *)
    
    (* IGBT Drive Command Outputs *)
    bPowerCondEnable    : BOOL;     (* Activate IGBT switching *)
    rPowerCondDuty      : REAL;     (* IGBT switching duty cycle 0.0 - 1.0 *)
    
    (* State & Diagnostic Outputs *)
    iStateMachine       : INT;      (* Current operating state code *)
    bSystemReady        : BOOL;     (* Indicates system is ready to charge/discharge *)
END_VAR
VAR
    (* Internal Constants *)
    C_QUENCH_VOLT_THRES : REAL := 0.25;    (* Voltage threshold for quench (resistive drop) *)
    C_NOMINAL_INDUCT    : REAL := 15.0;    (* Nominal coil inductance [Henry] *)
    C_MAX_HE_TEMP       : REAL := 4.3;     (* Maximum allowable He temperature [Kelvin] *)
    C_TARGET_HE_TEMP    : REAL := 4.2;     (* Target operating temp [Kelvin] *)
    
    (* Internal Variables *)
    rInductiveVoltage   : REAL;            (* Calculated V = L*(di/dt) *)
    rResistiveVoltage   : REAL;            (* V_diff = V_meas - V_inductive *)
    tQuenchFilter       : TON;             (* Debounce timer for quench detection *)
    tCoolingDelay       : TON;             (* Stabilization timer for cooling *)
    bCriticalFault      : BOOL := FALSE;   (* Latched critical fault *)
END_VAR

(* === MAIN LOGIC EXECUTOR === *)

(* 1. Safety & Critical Protection Interlocks *)
IF NOT bEmergencyStop OR bCriticalFault THEN
    (* Instantaneous fail-safe state enforcement *)
    bDumpBreakerCmd     := FALSE; (* OPEN breaker - dump energy *)
    bPowerCondEnable    := FALSE;
    rPowerCondDuty      := 0.0;
    bHePumpEnable       := TRUE;  (* Keep cooling to mitigate boil-off *)
    rCryoValve_PCV      := 100.0; (* Full open for maximum venting/cooling if fault *)
    iStateMachine       := 99;    (* FAULT STATE *)
    bSystemReady        := FALSE;
    RETURN; (* Halt further logic processing *)
END_IF;

(* 2. Advanced Quench Detection Algorithm *)
(* In a superconducting coil, purely inductive voltage is L*(di/dt). 
   Any excess voltage indicates a resistive zone (quench). *)
rInductiveVoltage := C_NOMINAL_INDUCT * rCoilCurrent_dIdt;
rResistiveVoltage := ABS(rCoilVoltage_V - rInductiveVoltage);

tQuenchFilter(IN := (rResistiveVoltage > C_QUENCH_VOLT_THRES), PT := T#5MS);

IF tQuenchFilter.Q THEN
    bQuenchAlarm    := TRUE;
    bCriticalFault  := TRUE; (* Latch the fault *)
    RETURN; (* Jump to safety state on next scan *)
END_IF;

(* 3. Thermosyphon Cooling Control *)
IF rLiquidHeTemp_K > C_MAX_HE_TEMP THEN
    bHePumpEnable := TRUE;
    rCryoValve_PCV := 100.0;
ELSIF rLiquidHeTemp_K > C_TARGET_HE_TEMP THEN
    bHePumpEnable := TRUE;
    (* Proportional valve control based on temperature error *)
    rCryoValve_PCV := (rLiquidHeTemp_K - C_TARGET_HE_TEMP) * 100.0 / (C_MAX_HE_TEMP - C_TARGET_HE_TEMP);
ELSE
    bHePumpEnable := FALSE;
    rCryoValve_PCV := 10.0; (* Minimum bypass *)
END_IF;

(* 4. State Machine for Normal Operations *)
CASE iStateMachine OF
    0: (* OFF / STANDBY *)
        bDumpBreakerCmd := FALSE; (* Dump resistor inline *)
        bPowerCondEnable := FALSE;
        bSystemReady := FALSE;
        
        IF bSystemEnable AND (rLiquidHeTemp_K <= C_TARGET_HE_TEMP) THEN
            iStateMachine := 10;
        END_IF;

    10: (* INITIALIZING & PRE-COOLING VERIFICATION *)
        tCoolingDelay(IN := TRUE, PT := T#30S);
        IF tCoolingDelay.Q THEN
            tCoolingDelay(IN := FALSE);
            bDumpBreakerCmd := TRUE; (* Close breaker, bypass dump resistor *)
            iStateMachine := 20;
        END_IF;

    20: (* READY TO CHARGE / DISCHARGE *)
        bSystemReady := TRUE;
        bPowerCondEnable := TRUE;
        
        (* Example IGBT DC Link voltage regulation logic *)
        IF rDCLinkVoltage_V < 800.0 THEN
            rPowerCondDuty := 0.65; (* Boost/Charge mode *)
        ELSIF rDCLinkVoltage_V > 850.0 THEN
            rPowerCondDuty := 0.35; (* Buck/Discharge mode *)
        ELSE
            rPowerCondDuty := 0.50; (* Float *)
        END_IF;

        IF NOT bSystemEnable THEN
            iStateMachine := 0;
        END_IF;
        
    99: (* FAULT HANDLING *)
        (* Latched state, requires manual reset logic not shown here for brevity *)
        bSystemReady := FALSE;
END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump({"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}, f, ensure_ascii=False)
print(f"Saved to {filename}")
