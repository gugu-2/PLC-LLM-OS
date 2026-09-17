import json, uuid, os

prompt = """<USER_REQUEST>
You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Large-Scale Desalination Multi-Stage Flash Distillation (MSF) Brine Heater Control**

Task: Invent a highly complex, ultra-realistic control scenario for this domain. Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_MSF_BrineHeater\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
   record = {\"messages\": [{\"role\": \"user\", \"content\": prompt}, {\"role\": \"assistant\", \"content\": code}]}
   with open(f\"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json\", \"w\", encoding=\"utf-8\") as f:
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
6. REPLY with: EVOLUTION COMPLETE: Large-Scale Desalination Multi-Stage Flash Distillation (MSF) Brine Heater Control

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT.
</USER_REQUEST>"""

code = """```iec-st
FUNCTION_BLOCK FB_MSF_BrineHeater
VAR_INPUT
    (* Physical Inputs from Field Instruments *)
    bEnable            : BOOL;     (* System master enable command *)
    bEmergencyStop     : BOOL;     (* Safety loop status (TRUE = Healthy, FALSE = Trip) *)
    rBrineInletTemp    : REAL;     (* Temperature of brine entering heater [deg C] *)
    rBrineOutletTemp   : REAL;     (* Top Brine Temperature (TBT) exiting heater [deg C] *)
    rSteamPressure     : REAL;     (* Supply steam pressure to heater [bar] *)
    rBrineFlowRate     : REAL;     (* Recirculating brine flow rate [m3/h] *)
    rTBTSetpoint       : REAL;     (* Desired Top Brine Temperature [deg C] *)
    rMaxSteamPress     : REAL := 3.5; (* Safety limit for steam pressure [bar] *)
END_VAR
VAR_OUTPUT
    (* Physical Outputs to Actuators and SCADA *)
    bSystemReady       : BOOL;     (* Controller initialized and healthy *)
    rSteamValveCmd     : REAL;     (* Command to steam control valve [0-100%] *)
    bHeaterTrip        : BOOL;     (* Interlock active - heater tripped *)
    bTempAlarm         : BOOL;     (* High temperature or deviation alarm *)
    bLowFlowAlarm      : BOOL;     (* Brine flow is critically low *)
END_VAR
VAR
    (* Internal State and Filtering *)
    iState             : INT := 0; (* State machine step index *)
    rFilteredTBT       : REAL;     (* EMA filtered brine outlet temperature *)
    rFilterAlpha       : REAL := 0.1; (* Exponential Moving Average coefficient *)
    
    (* PID Control Variables *)
    rError             : REAL;     (* Control error (Setpoint - Actual) *)
    rLastError         : REAL;     (* Previous cycle error for derivative calculation *)
    rIntegral          : REAL := 0.0; (* Integral accumulator *)
    rDerivative        : REAL;     (* Derivative term *)
    rKp                : REAL := 2.5; (* Proportional gain *)
    rKi                : REAL := 0.05; (* Integral gain *)
    rKd                : REAL := 1.2; (* Derivative gain *)
    rFeedForward       : REAL;     (* Flow-based feed-forward term *)
    
    (* Timers and Safety *)
    tWarmupTimer       : TON;      (* Timer for gradual steam introduction *)
    tTripDelay         : TON;      (* Delay timer to prevent nuisance trips *)
    rMaxTBT_Limit      : REAL := 120.0; (* Absolute maximum Top Brine Temperature limit *)
    rMinFlow_Limit     : REAL := 1500.0; (* Minimum required flow [m3/h] before steam admitted *)
END_VAR

(* === MAIN LOGIC === *)

(* 1. Safety Interlocks & E-Stop *)
IF NOT bEmergencyStop OR (rSteamPressure > rMaxSteamPress) THEN
    bHeaterTrip := TRUE;
    bSystemReady := FALSE;
    rSteamValveCmd := 0.0;
    iState := 0; (* Force to IDLE / FAULT state *)
    rIntegral := 0.0; (* Reset PID integral to prevent windup *)
    RETURN;
END_IF;

(* 2. Signal Processing (EMA Filter for noisy TBT sensor) *)
rFilteredTBT := (rFilterAlpha * rBrineOutletTemp) + ((1.0 - rFilterAlpha) * rFilteredTBT);

(* 3. Alarm Generation *)
bTempAlarm := (rFilteredTBT > (rTBTSetpoint + 5.0)) OR (rFilteredTBT > rMaxTBT_Limit);
bLowFlowAlarm := (rBrineFlowRate < rMinFlow_Limit);

(* 4. State Machine for Heater Operation *)
CASE iState OF
    0: (* IDLE & SAFETY CHECK *)
        rSteamValveCmd := 0.0;
        bSystemReady := TRUE;
        bHeaterTrip := FALSE;
        rIntegral := 0.0;
        tWarmupTimer(IN := FALSE);
        
        IF bEnable AND NOT bLowFlowAlarm THEN
            iState := 10; (* Transition to Pre-Check *)
        END_IF;

    10: (* WARM-UP (GRADUAL HEATING) *)
        (* Open valve slightly to avoid thermal shock to heat exchanger tubes *)
        rSteamValveCmd := 15.0; 
        tWarmupTimer(IN := TRUE, PT := T#5M);
        
        IF tWarmupTimer.Q THEN
            tWarmupTimer(IN := FALSE);
            iState := 20; (* Transition to Auto Control *)
        END_IF;
        
        (* Abort warm-up if enable drops or flow stops *)
        IF NOT bEnable OR bLowFlowAlarm THEN
            iState := 0;
        END_IF;

    20: (* PID CONTROL MODE *)
        (* Calculate Error *)
        rError := rTBTSetpoint - rFilteredTBT;
        
        (* Anti-windup for Integral term *)
        IF (rSteamValveCmd < 100.0 AND rSteamValveCmd > 0.0) OR 
           (rSteamValveCmd >= 100.0 AND rError < 0.0) OR 
           (rSteamValveCmd <= 0.0 AND rError > 0.0) THEN
            rIntegral := rIntegral + (rError * rKi);
        END_IF;
        
        (* Derivative term *)
        rDerivative := (rError - rLastError) * rKd;
        rLastError := rError;
        
        (* Feed-forward based on Brine Flow Rate to anticipate thermal load changes *)
        (* Nominal load assumption: baseline steam valve opening scales with flow *)
        rFeedForward := (rBrineFlowRate / 10000.0) * 10.0; 
        
        (* Final PID Equation *)
        rSteamValveCmd := (rError * rKp) + rIntegral + rDerivative + rFeedForward;
        
        (* Actuator limits saturation (0 to 100%) *)
        IF rSteamValveCmd > 100.0 THEN
            rSteamValveCmd := 100.0;
        ELSIF rSteamValveCmd < 0.0 THEN
            rSteamValveCmd := 0.0;
        END_IF;
        
        (* Return to idle if master enable removed *)
        IF NOT bEnable OR bLowFlowAlarm THEN
            iState := 0;
        END_IF;

    ELSE
        (* Failsafe default *)
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
