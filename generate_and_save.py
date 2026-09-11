import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Industrial Scale Closed-Cycle Gas Turbine (CCGT) Heat Recovery Steam Generator (HRSG)**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Triple-pressure cascading attemperation spray, drum level shrink-swell compensation, and pinch-point mass flow balancing). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_CCGT_HRSG\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Industrial Scale Closed-Cycle Gas Turbine (CCGT) Heat Recovery Steam Generator (HRSG)

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_HRSG_DrumLevel_AttemperationControl
(*
    Complex HRSG Drum Level and Attemperation Control System
    Implements shrink-swell compensation, triple-pressure mass flow balancing,
    and cascaded temperature spray control for CCGT plants.
*)
VAR_INPUT
    bEnable                 : BOOL;     (* System Enable Signal - Watchdog verified *)
    bEmergencyTrip          : BOOL;     (* Safety Relay Status (SIL3) - Active Low Trip *)
    rGasTurbineExhaustTemp  : REAL;     (* Exhaust gas temperature from GT [deg C] *)
    rGasTurbineExhaustFlow  : REAL;     (* Exhaust gas mass flow rate from GT [kg/s] *)
    rDrumLevelActual        : REAL;     (* HP Drum Level actual reading [mm] *)
    rDrumPressureActual     : REAL;     (* HP Drum Pressure actual reading [bar] *)
    rFeedwaterFlow          : REAL;     (* Feedwater flow rate to HP drum [kg/s] *)
    rSteamFlow              : REAL;     (* Steam flow rate out of HP drum [kg/s] *)
    rAttempOutletTemp       : REAL;     (* Temperature after desuperheater [deg C] *)
    rAttempSetpoint         : REAL;     (* Setpoint for final steam temperature [deg C] *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;     (* System is initialized and ready for control *)
    bTripAlarm              : BOOL;     (* System trip / alarm active *)
    rFeedwaterValveDemand   : REAL;     (* Feedwater control valve demand [0.0 - 100.0 %] *)
    rAttempValveDemand      : REAL;     (* Spray water attemperation valve demand [0.0 - 100.0 %] *)
    iOperatingState         : INT;      (* Current internal state machine step *)
    rCalculatedPinchPoint   : REAL;     (* Estimated pinch point temperature difference [K] *)
END_VAR
VAR
    (* Internal Variables & State *)
    iState                  : INT := 0; 
    tUpdateTimer            : TON;
    tSafetyTimer            : TON;
    rDrumLevelError         : REAL;
    rDrumLevelIntegral      : REAL := 0.0;
    rMassFlowBalance        : REAL;
    rShrinkSwellComp        : REAL;
    rPressureDerivative     : REAL;
    rLastDrumPressure       : REAL := 0.0;
    rAttempError            : REAL;
    rAttempIntegral         : REAL := 0.0;
    
    (* Filter Constants and PID Gains *)
    rKp_Drum                : REAL := 2.5;
    rKi_Drum                : REAL := 0.05;
    rKp_Attemp              : REAL := 1.8;
    rKi_Attemp              : REAL := 0.02;
    rDt                     : REAL := 0.1; (* 100ms cycle time assumption *)
END_VAR

(* === MAIN SAFETY INTERLOCKS === *)
IF NOT bEmergencyTrip THEN
    bSystemReady := FALSE;
    bTripAlarm := TRUE;
    rFeedwaterValveDemand := 0.0;
    rAttempValveDemand := 0.0;
    iOperatingState := 999; (* TRIPPED *)
    RETURN;
END_IF;

(* Evaluate pinch point approximation based on GT exhaust flow and temp *)
rCalculatedPinchPoint := (rGasTurbineExhaustTemp - 200.0) / (1.0 + rGasTurbineExhaustFlow * 0.001);

(* Pressure derivative calculation for shrink-swell compensation *)
rPressureDerivative := (rDrumPressureActual - rLastDrumPressure) / rDt;
rLastDrumPressure := rDrumPressureActual;

CASE iState OF
    0: (* IDLE & INITIALIZATION *)
        bSystemReady := FALSE;
        bTripAlarm := FALSE;
        rFeedwaterValveDemand := 0.0;
        rAttempValveDemand := 0.0;
        IF bEnable THEN
            tSafetyTimer(IN := TRUE, PT := T#2S);
            IF tSafetyTimer.Q THEN
                tSafetyTimer(IN := FALSE);
                iState := 10;
            END_IF;
        ELSE
            tSafetyTimer(IN := FALSE);
        END_IF;

    10: (* WARM-UP & PRE-CHECK *)
        bSystemReady := TRUE;
        bTripAlarm := FALSE;
        (* Minimum feedwater flow during warmup *)
        rFeedwaterValveDemand := 15.0; 
        IF rDrumPressureActual > 10.0 THEN
            iState := 20;
        END_IF;
        IF NOT bEnable THEN
            iState := 0;
        END_IF;

    20: (* NORMAL OPERATION - THREE-ELEMENT DRUM LEVEL CONTROL + ATTEMPERATION *)
        bSystemReady := TRUE;
        
        (* 1. Mass Flow Balance (Feedforward) *)
        rMassFlowBalance := rSteamFlow - rFeedwaterFlow;
        
        (* 2. Shrink-Swell Compensation based on pressure derivative *)
        rShrinkSwellComp := rPressureDerivative * 5.0; 
        
        (* 3. Drum Level Error (Feedback) *)
        rDrumLevelError := 0.0 - rDrumLevelActual; (* Assuming 0.0 is the setpoint mm *)
        rDrumLevelIntegral := rDrumLevelIntegral + (rDrumLevelError * rDt);
        
        (* Calculate Final Feedwater Demand *)
        rFeedwaterValveDemand := (rMassFlowBalance * 0.5) + 
                                 (rDrumLevelError * rKp_Drum) + 
                                 (rDrumLevelIntegral * rKi_Drum) + 
                                 rShrinkSwellComp;
                                 
        (* Clamp Feedwater Demand *)
        IF rFeedwaterValveDemand > 100.0 THEN
            rFeedwaterValveDemand := 100.0;
        ELSIF rFeedwaterValveDemand < 0.0 THEN
            rFeedwaterValveDemand := 0.0;
        END_IF;
        
        (* Attemperation Cascade Control *)
        rAttempError := rAttempSetpoint - rAttempOutletTemp;
        rAttempIntegral := rAttempIntegral + (rAttempError * rDt);
        
        rAttempValveDemand := (rAttempError * rKp_Attemp) + (rAttempIntegral * rKi_Attemp);
        
        (* Clamp Attemperation Demand *)
        IF rAttempValveDemand > 100.0 THEN
            rAttempValveDemand := 100.0;
        ELSIF rAttempValveDemand < 0.0 THEN
            rAttempValveDemand := 0.0;
        END_IF;
        
        IF NOT bEnable THEN
            iState := 0;
        END_IF;

    999: (* TRIPPED STATE WAITING FOR RESET *)
        bTripAlarm := TRUE;
        rFeedwaterValveDemand := 0.0;
        rAttempValveDemand := 0.0;
        IF bEmergencyTrip AND NOT bEnable THEN
            iState := 0; (* Reset sequence requires Enable to go LOW first *)
        END_IF;
        
    ELSE
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
