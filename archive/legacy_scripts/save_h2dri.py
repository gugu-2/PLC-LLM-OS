import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Utility-Scale Hydrogen Direct Reduced Iron (H2-DRI) Shaft Furnace**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., 100% green hydrogen reduction endothermic profiling, sponge iron metallization rate feed-forward, and top-gas recycling multi-stage compression). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_H2DRI_ShaftFurnace\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Utility-Scale Hydrogen Direct Reduced Iron (H2-DRI) Shaft Furnace

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_H2DRI_ShaftFurnace
VAR_INPUT
    bEnable                 : BOOL;     (* System master enable signal *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal - MUST BE TRUE TO RUN *)
    rH2InjectionRate        : REAL;     (* Hydrogen gas injection flow rate in Nm3/h *)
    rFurnaceTopTemp         : REAL;     (* Furnace top zone temperature in deg C *)
    rFurnaceBottomTemp      : REAL;     (* Furnace cooling zone temperature in deg C *)
    rTopGasPressure         : REAL;     (* Top gas pressure in bar(a) *)
    rOreFeedRate            : REAL;     (* Iron ore pellets feed rate in t/h *)
    rMetallizationTarget    : REAL;     (* Target metallization rate (fraction 0.0-1.0) *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;     (* H2-DRI Shaft Furnace ready for operation *)
    rHeaterPowerCmd         : REAL;     (* Command to H2 pre-heaters 0-100% *)
    rH2FlowValveCmd         : REAL;     (* Hydrogen flow control valve 0-100% *)
    rTopGasRecycleValveCmd  : REAL;     (* Top gas recycle compressor inlet valve 0-100% *)
    rDischargeRateCmd       : REAL;     (* DRI discharge screw speed command 0-100% *)
    bHighTempAlarm          : BOOL;     (* High temperature warning/alarm flag *)
    bLowPressureAlarm       : BOOL;     (* Low pressure warning/alarm flag *)
END_VAR
VAR
    iState                  : INT := 0; (* Internal state machine *)
    tStartupTimer           : TON;      (* Timer for pre-heating and purging *)
    tControlLoopTimer       : TON;      (* Loop time for control calculations *)
    rReductionEnthalpy      : REAL := 98.4; (* Endothermic heat of reaction kJ/mol *)
    rEstimatedMetallization : REAL;     (* Internal observer for metallization *)
    rHeatBalanceError       : REAL;     (* Error in heat balance *)
    rFeedForwardH2          : REAL;
    rTopGasSetpoint         : REAL := 1.5; (* bar(a) target for top gas *)
END_VAR

(* === MAIN LOGIC === *)
(* Emergency and Safety Interlocks *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bHighTempAlarm := FALSE;
    bLowPressureAlarm := FALSE;
    rHeaterPowerCmd := 0.0;
    rH2FlowValveCmd := 0.0;
    rTopGasRecycleValveCmd := 0.0;
    rDischargeRateCmd := 0.0;
    iState := 0;
    RETURN;
END_IF;

(* Alarms Generation *)
IF rFurnaceTopTemp > 1050.0 THEN
    bHighTempAlarm := TRUE;
ELSE
    bHighTempAlarm := FALSE;
END_IF;

IF rTopGasPressure < 1.0 THEN
    bLowPressureAlarm := TRUE;
ELSE
    bLowPressureAlarm := FALSE;
END_IF;

(* Main State Machine *)
CASE iState OF
    0: (* IDLE & PURGING *)
        bSystemReady := FALSE;
        rHeaterPowerCmd := 0.0;
        rH2FlowValveCmd := 10.0; (* Minimum purge flow *)
        rTopGasRecycleValveCmd := 0.0;
        rDischargeRateCmd := 0.0;
        
        IF bEnable AND NOT bHighTempAlarm AND NOT bLowPressureAlarm THEN
            iState := 10;
        END_IF;

    10: (* PRE-HEATING *)
        rHeaterPowerCmd := 50.0; (* Ramp up heaters *)
        rH2FlowValveCmd := 20.0;
        tStartupTimer(IN := TRUE, PT := T#300S);
        
        IF tStartupTimer.Q AND (rFurnaceBottomTemp > 600.0) THEN
            tStartupTimer(IN := FALSE);
            iState := 20;
        END_IF;

    20: (* REDUCTION OPERATION *)
        bSystemReady := TRUE;
        
        (* Feed-forward H2 calculation based on ore feed and metallization target *)
        (* Stoichiometric requirement approximation plus excess factor *)
        rFeedForwardH2 := rOreFeedRate * rMetallizationTarget * 600.0; 
        
        (* PID approximation for H2 Valve based on temp *)
        IF rFurnaceTopTemp < 850.0 THEN
            rH2FlowValveCmd := LIMIT(MN:=20.0, IN:=(rFeedForwardH2 * 1.2), MX:=100.0);
            rHeaterPowerCmd := 90.0;
        ELSE
            rH2FlowValveCmd := LIMIT(MN:=20.0, IN:=rFeedForwardH2, MX:=100.0);
            rHeaterPowerCmd := 70.0;
        END_IF;
        
        (* Top gas recycling pressure control *)
        IF rTopGasPressure > (rTopGasSetpoint + 0.1) THEN
            rTopGasRecycleValveCmd := rTopGasRecycleValveCmd + 1.0;
        ELSIF rTopGasPressure < (rTopGasSetpoint - 0.1) THEN
            rTopGasRecycleValveCmd := rTopGasRecycleValveCmd - 1.0;
        END_IF;
        rTopGasRecycleValveCmd := LIMIT(MN:=0.0, IN:=rTopGasRecycleValveCmd, MX:=100.0);
        
        (* Estimate metallization (dummy physics model) *)
        rEstimatedMetallization := (rFurnaceTopTemp / 1000.0) * (rH2InjectionRate / 10000.0);
        
        (* Control discharge speed based on metallization *)
        IF rEstimatedMetallization >= rMetallizationTarget THEN
            rDischargeRateCmd := LIMIT(MN:=10.0, IN:=(rOreFeedRate * 0.8), MX:=100.0);
        ELSE
            rDischargeRateCmd := LIMIT(MN:=0.0, IN:=(rOreFeedRate * 0.4), MX:=50.0);
        END_IF;
        
        IF NOT bEnable THEN
            iState := 30;
        END_IF;
        
    30: (* COOLDOWN *)
        bSystemReady := FALSE;
        rHeaterPowerCmd := 0.0;
        rH2FlowValveCmd := 10.0; (* Purge *)
        rTopGasRecycleValveCmd := 0.0;
        rDischargeRateCmd := 10.0; (* Empty furnace slowly *)
        
        IF rFurnaceTopTemp < 200.0 THEN
            iState := 0;
        END_IF;

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
with open(os.path.join("C:/Users/majip/Downloads/LLM REASEARCH", filename), "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
