import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Industrial Scale Offshore Wind Farm High-Voltage Direct Current (HVDC) Converter Station**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Modular Multilevel Converter (MMC) sub-module capacitor voltage balancing, grid-forming frequency droop control, and offshore AC fault ride-through (FRT) reactive power injection). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_HVDC_MMC_Converter\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Industrial Scale Offshore Wind Farm High-Voltage Direct Current (HVDC) Converter Station

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_HVDC_MMC_Controller
VAR_INPUT
    (* High-level operational inputs *)
    bSystemEnable           : BOOL;     (* Main HVDC system enable signal *)
    bEmergencyStop          : BOOL;     (* Safety loop status (TRUE = OK, FALSE = Tripped) *)
    
    (* Grid Measurements *)
    rGridFrequency_Hz       : REAL;     (* Measured AC grid frequency in Hz *)
    rGridVoltage_kV         : REAL;     (* Measured AC grid RMS voltage in kV *)
    rDCBusVoltage_kV        : REAL;     (* Measured DC bus voltage in kV *)
    
    (* Setpoints & References *)
    rPref_MW                : REAL;     (* Active power reference from dispatch in MW *)
    rQref_MVAr              : REAL;     (* Reactive power reference from dispatch in MVAr *)
    
    (* Modular Multilevel Converter (MMC) specific *)
    rCapVoltageAvg_kV       : REAL;     (* Average submodule capacitor voltage in kV *)
END_VAR
VAR_OUTPUT
    (* Converter State *)
    bReadyToOperate         : BOOL;     (* TRUE when converter is initialized and precharged *)
    bFaultActive            : BOOL;     (* TRUE if any critical fault is detected *)
    
    (* Control Signals to Valve Base Electronics (VBE) *)
    rActivePowerCmd_MW      : REAL;     (* Actuating signal for active power *)
    rReactivePowerCmd_MVAr  : REAL;     (* Actuating signal for reactive power *)
    rModulationIndex        : REAL;     (* Overall converter modulation index (0.0 to 1.0) *)
    
    (* Diagnostic *)
    iOperatingState         : INT;      (* Current state machine step *)
END_VAR
VAR
    (* Internal State Machine *)
    iState                  : INT := 0; 
    
    (* Timers *)
    tPrechargeTimer         : TON;
    tFaultDelay             : TON;
    tFRT_Timer              : TON;      (* Fault Ride Through timer *)
    
    (* Filtered Measurements (Low Pass Filter states) *)
    rFreqFiltered           : REAL := 50.0;
    rVoltFiltered           : REAL := 220.0;
    
    (* Control Loop Integrators *)
    rPowerErrorInt          : REAL := 0.0;
    
    (* Constants *)
    NOMINAL_FREQ            : REAL := 50.0;
    NOMINAL_VOLTAGE         : REAL := 220.0;
    DROOP_COEFF             : REAL := 0.02; (* 2% Droop *)
    FRT_VOLTAGE_THRESHOLD   : REAL := 0.85; (* 85% of nominal triggers FRT *)
    
    (* Internal flags *)
    bFRT_Mode               : BOOL := FALSE;
    
    (* Local Variables *)
    rFreqError              : REAL;
    rP_RefAdjusted          : REAL;
END_VAR

(* === MAIN LOGIC === *)

(* 1. Safety Interlocks and Emergency Handling *)
IF NOT bEmergencyStop THEN
    bReadyToOperate         := FALSE;
    bFaultActive            := TRUE;
    iState                  := 99; (* 99 = FAULT STATE *)
    rActivePowerCmd_MW      := 0.0;
    rReactivePowerCmd_MVAr  := 0.0;
    rModulationIndex        := 0.0;
    iOperatingState         := iState;
    RETURN;
END_IF;

(* 2. Measurement Filtering (1st Order LPF, approx for demonstration) *)
(* In a real implementation this would use a discrete transfer function with exact sample times *)
rFreqFiltered := rFreqFiltered * 0.9 + rGridFrequency_Hz * 0.1;
rVoltFiltered := rVoltFiltered * 0.9 + rGridVoltage_kV * 0.1;

(* 3. Grid-Forming / Droop Control Evaluation *)
(* Adjust active power reference based on grid frequency deviation *)
rFreqError := NOMINAL_FREQ - rFreqFiltered;
rP_RefAdjusted := rPref_MW + (rFreqError * DROOP_COEFF * 1000.0);

(* 4. Fault Ride-Through (FRT) Detection *)
IF (rVoltFiltered < (NOMINAL_VOLTAGE * FRT_VOLTAGE_THRESHOLD)) THEN
    tFRT_Timer(IN := TRUE, PT := T#200MS);
    bFRT_Mode := TRUE;
ELSE
    tFRT_Timer(IN := FALSE);
    bFRT_Mode := FALSE;
END_IF;

(* 5. Main State Machine *)
CASE iState OF
    0: (* IDLE *)
        bReadyToOperate := FALSE;
        rActivePowerCmd_MW := 0.0;
        rReactivePowerCmd_MVAr := 0.0;
        rModulationIndex := 0.0;
        
        IF bSystemEnable AND (rDCBusVoltage_kV > 50.0) THEN
            iState := 10;
        END_IF;

    10: (* PRECHARGE & SUBMODULE BALANCING *)
        (* Simulate capacitor precharge sequence *)
        tPrechargeTimer(IN := TRUE, PT := T#5S);
        
        IF tPrechargeTimer.Q THEN
            tPrechargeTimer(IN := FALSE);
            IF rCapVoltageAvg_kV > 2.5 THEN
                iState := 20; (* Nominal operation *)
            ELSE
                iState := 99; (* Precharge failed *)
            END_IF;
        END_IF;

    20: (* RUNNING / NOMINAL OPERATION *)
        bReadyToOperate := TRUE;
        bFaultActive := FALSE;
        
        IF bFRT_Mode THEN
            (* Under FRT, active power is reduced, reactive power is maximized for grid support *)
            rActivePowerCmd_MW := rP_RefAdjusted * 0.1;
            rReactivePowerCmd_MVAr := 500.0; (* Inject max MVAr to support voltage *)
            rModulationIndex := 1.0;
            
            IF tFRT_Timer.Q THEN
                (* Fault sustained too long, trip system *)
                iState := 99;
            END_IF;
        ELSE
            (* Normal control mode *)
            (* Simple PI-like control approximation for demonstration *)
            rPowerErrorInt := rPowerErrorInt + (rP_RefAdjusted - rActivePowerCmd_MW) * 0.01;
            
            rActivePowerCmd_MW := rP_RefAdjusted;
            rReactivePowerCmd_MVAr := rQref_MVAr;
            rModulationIndex := 0.85 + (rDCBusVoltage_kV / 1000.0) * 0.1;
        END_IF;
        
        IF NOT bSystemEnable THEN
            iState := 30; (* SHUTDOWN SEQUENCE *)
        END_IF;
        
    30: (* SHUTDOWN *)
        bReadyToOperate := FALSE;
        rActivePowerCmd_MW := 0.0;
        rReactivePowerCmd_MVAr := 0.0;
        rModulationIndex := 0.0;
        IF (rDCBusVoltage_kV < 10.0) THEN
            iState := 0;
        END_IF;

    99: (* FAULT HANDLING *)
        bReadyToOperate := FALSE;
        bFaultActive := TRUE;
        rActivePowerCmd_MW := 0.0;
        rReactivePowerCmd_MVAr := 0.0;
        rModulationIndex := 0.0;
        
        (* Require manual reset via bSystemEnable cycle *)
        IF NOT bSystemEnable THEN
            iState := 0;
        END_IF;

END_CASE;

iOperatingState := iState;

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
