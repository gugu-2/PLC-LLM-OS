import json, uuid, os

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """<USER_REQUEST>
You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Large-Scale Commercial Hydroponic Vertical Farm Nutrient Film Technique (NFT) pH and EC Balancing**

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
   prompt = "<copy this exact user prompt here>"
   code = "..."
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
6. REPLY with: EVOLUTION COMPLETE: Large-Scale Commercial Hydroponic Vertical Farm Nutrient Film Technique (NFT) pH and EC Balancing

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT.
</USER_REQUEST>"""

code = """```iec-st
FUNCTION_BLOCK FB_NFT_Hydroponics_pH_EC_Master
VAR_INPUT
    (* Critical Safety & System Signals *)
    bEnable             : BOOL;       (* Master enable signal for the dosing skid *)
    bEStop              : BOOL;       (* Hardware safety circuit OK (True = Healthy) *)
    bFlowSwitchActive   : BOOL;       (* Confirmation of flow through the NFT system *)
    rTankLevel          : REAL;       (* Nutrient reservoir level in liters (0.0 to 1000.0) *)
    
    (* Process Variables *)
    rSensor_pH_A        : REAL;       (* Redundant pH Sensor A (0.0 to 14.0) *)
    rSensor_pH_B        : REAL;       (* Redundant pH Sensor B (0.0 to 14.0) *)
    rSensor_EC          : REAL;       (* Electrical Conductivity (mS/cm) *)
    rWaterTemp          : REAL;       (* Nutrient water temperature in deg Celsius *)
    
    (* Targets *)
    rTarget_pH          : REAL := 6.0; (* Optimal pH Setpoint for NFT *)
    rTarget_EC          : REAL := 1.8; (* Optimal EC Setpoint for vegetative growth *)
END_VAR

VAR_OUTPUT
    (* Dosing Actuators (PWM or On/Off via SSRs) *)
    rDoseRate_pH_Up     : REAL;       (* Output 0-100% for pH UP dosing pump *)
    rDoseRate_pH_Down   : REAL;       (* Output 0-100% for pH DOWN dosing pump *)
    rDoseRate_NutrientA : REAL;       (* Output 0-100% for Micro/Macro A pump *)
    rDoseRate_NutrientB : REAL;       (* Output 0-100% for Micro/Macro B pump *)
    
    (* System Status *)
    bSystemReady        : BOOL;       (* Indicates system is actively regulating *)
    bCriticalAlarm      : BOOL;       (* Active if pH/EC bounds exceeded or flow lost *)
    iActiveState        : INT;        (* Current state of the sequence machine *)
END_VAR

VAR
    (* Internal Filtering and Validation *)
    rFiltered_pH        : REAL;       (* Voted and filtered pH reading *)
    rFiltered_EC        : REAL;       (* Temperature-compensated and filtered EC *)
    rDeviation_pH       : REAL;       (* pH deviation between sensors *)
    
    (* PID / Deadband Logic *)
    rError_pH           : REAL;
    rError_EC           : REAL;
    
    (* State Machine *)
    iState              : INT := 0;
    tStateTimer         : TON;
    tDosingInterval     : TON;
    
    (* Limits and Constants *)
    rMaxPhDev           : REAL := 0.5;   (* Max acceptable deviation between pH sensors *)
    rMinTankLevel       : REAL := 150.0; (* Minimum safe tank volume *)
    rKp_pH              : REAL := 15.0;  (* Proportional gain for pH dosing *)
    rKp_EC              : REAL := 25.0;  (* Proportional gain for EC dosing *)
END_VAR

(* === MAIN LOGIC === *)

(* 1. Safety and Interlock Layer *)
IF NOT bEStop OR rTankLevel < rMinTankLevel OR NOT bFlowSwitchActive THEN
    bSystemReady := FALSE;
    bCriticalAlarm := TRUE;
    rDoseRate_pH_Up := 0.0;
    rDoseRate_pH_Down := 0.0;
    rDoseRate_NutrientA := 0.0;
    rDoseRate_NutrientB := 0.0;
    iState := 999; (* Fault State *)
    iActiveState := iState;
    RETURN;
END_IF;

(* 2. Signal Processing & Validation *)
(* Compare redundant pH sensors to detect sensor drift or failure *)
rDeviation_pH := ABS(rSensor_pH_A - rSensor_pH_B);
IF rDeviation_pH > rMaxPhDev THEN
    bCriticalAlarm := TRUE;
    iState := 999;
    RETURN;
ELSE
    bCriticalAlarm := FALSE;
    rFiltered_pH := (rSensor_pH_A + rSensor_pH_B) / 2.0;
END_IF;

(* Basic Temperature Compensation for EC (Approx 2% per deg C deviation from 25C) *)
rFiltered_EC := rSensor_EC / (1.0 + 0.02 * (rWaterTemp - 25.0));

(* 3. State Machine for Dosing Control *)
CASE iState OF
    0: (* INIT / IDLE *)
        bSystemReady := FALSE;
        IF bEnable AND NOT bCriticalAlarm THEN
            tStateTimer(IN := FALSE);
            iState := 10;
        END_IF;
        
    10: (* SETTLING AND MEASURING *)
        bSystemReady := TRUE;
        tStateTimer(IN := TRUE, PT := T#30S);
        IF tStateTimer.Q THEN
            tStateTimer(IN := FALSE);
            (* Determine if Dosing is required. EC takes precedence over pH *)
            rError_EC := rTarget_EC - rFiltered_EC;
            rError_pH := rFiltered_pH - rTarget_pH; (* Positive means pH too high -> need DOWN *)
            
            IF ABS(rError_EC) > 0.1 THEN
                iState := 20; (* EC Dosing *)
            ELSIF ABS(rError_pH) > 0.2 THEN
                iState := 30; (* pH Dosing *)
            END_IF;
        END_IF;
        
    20: (* EC DOSING SEQUENCE *)
        IF rError_EC > 0.0 THEN
            (* Calculate Proportional Dose Rate with Saturation *)
            rDoseRate_NutrientA := rError_EC * rKp_EC;
            rDoseRate_NutrientB := rError_EC * rKp_EC;
            IF rDoseRate_NutrientA > 100.0 THEN rDoseRate_NutrientA := 100.0; END_IF;
            IF rDoseRate_NutrientB > 100.0 THEN rDoseRate_NutrientB := 100.0; END_IF;
        ELSE
            rDoseRate_NutrientA := 0.0;
            rDoseRate_NutrientB := 0.0;
        END_IF;
        
        tDosingInterval(IN := TRUE, PT := T#10S); (* Dose for 10 seconds *)
        IF tDosingInterval.Q THEN
            tDosingInterval(IN := FALSE);
            rDoseRate_NutrientA := 0.0;
            rDoseRate_NutrientB := 0.0;
            iState := 40; (* Mixing Delay *)
        END_IF;
        
    30: (* pH DOSING SEQUENCE *)
        IF rError_pH > 0.0 THEN
            (* pH is high, apply pH DOWN *)
            rDoseRate_pH_Down := rError_pH * rKp_pH;
            IF rDoseRate_pH_Down > 100.0 THEN rDoseRate_pH_Down := 100.0; END_IF;
            rDoseRate_pH_Up := 0.0;
        ELSE
            (* pH is low, apply pH UP *)
            rDoseRate_pH_Up := ABS(rError_pH) * rKp_pH;
            IF rDoseRate_pH_Up > 100.0 THEN rDoseRate_pH_Up := 100.0; END_IF;
            rDoseRate_pH_Down := 0.0;
        END_IF;
        
        tDosingInterval(IN := TRUE, PT := T#5S); (* Dose for 5 seconds *)
        IF tDosingInterval.Q THEN
            tDosingInterval(IN := FALSE);
            rDoseRate_pH_Up := 0.0;
            rDoseRate_pH_Down := 0.0;
            iState := 40; (* Mixing Delay *)
        END_IF;
        
    40: (* MIXING DELAY / RECIRCULATION *)
        (* Allow time for nutrients/pH adjusters to mix through the NFT system *)
        tStateTimer(IN := TRUE, PT := T#2M);
        IF tStateTimer.Q THEN
            tStateTimer(IN := FALSE);
            IF bEnable THEN
                iState := 10;
            ELSE
                iState := 0;
            END_IF;
        END_IF;
        
    999: (* FAULT RECOVERY *)
        bSystemReady := FALSE;
        rDoseRate_pH_Up := 0.0;
        rDoseRate_pH_Down := 0.0;
        rDoseRate_NutrientA := 0.0;
        rDoseRate_NutrientB := 0.0;
        IF bEnable AND NOT bCriticalAlarm THEN
            iState := 0;
        END_IF;
END_CASE;

iActiveState := iState;

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
