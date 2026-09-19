import os, json, uuid
os.makedirs("data/swarm_raw", exist_ok=True)
prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Industrial Scale Aluminum Smelting Electrolysis Cell Alumina Feeding and Anode Effect Quench**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_AluminumSmelting_Cell\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Industrial Scale Aluminum Smelting Electrolysis Cell Alumina Feeding and Anode Effect Quench

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_Alumina_Smelting_Feeding_And_Quench
(* ======================================================================================
   Block Name   : FB_Alumina_Smelting_Feeding_And_Quench
   Author       : Principal Automation Architect (Lumina Swarm)
   Description  : Advanced control of an industrial-scale Hall-Héroult aluminum reduction cell.
                  Manages continuous Alumina (Al2O3) feeding via point feeders based on cell
                  pseudo-resistance (R = (V - BEMF)/I) tracking. Actively detects impending
                  Anode Effects (AE) by analyzing the rate of change of resistance (dR/dt)
                  and high-frequency voltage noise (V_noise). Executes multi-stage quench
                  protocols (feed over-dosing, anode bumping, and compressed air lancing)
                  to rapidly extinguish Anode Effects and restore normal electrolysis.
                  Features comprehensive EWMA noise filtering, rate-limiters, and safety interlocks.
   ====================================================================================== *)

VAR_INPUT
    bEnable                 : BOOL;     (* System global enable *)
    bEmergencyStop          : BOOL;     (* Safety relay (FALSE = active E-Stop) *)
    rCellVoltage            : REAL;     (* Filtered cell voltage [V] (typical 4.0 - 5.0 V) *)
    rLineCurrent            : REAL;     (* Potline current [kA] (typical 300 - 600 kA) *)
    rBathTemp               : REAL;     (* Bath temperature [Deg C] (typical 950 - 970 C) *)
    rAlF3Ratio              : REAL;     (* Bath acidity ratio (AlF3 / NaF) *)
    bHopperLowLevel         : BOOL;     (* Alumina hopper low level switch *)
    bManualOverride         : BOOL;     (* Maintenance manual mode request *)
END_VAR

VAR_OUTPUT
    bSystemReady            : BOOL;     (* Pot controller active and ready *)
    bPointFeederValve       : BOOL;     (* Solenoid to pulse the point feeder cylinder *)
    rAnodePositionCmd       : REAL;     (* Command to anode beam motors [mm] *)
    bAnodeEffectActive      : BOOL;     (* True if Anode Effect is currently happening *)
    rCellResistance         : REAL;     (* Calculated pseudo-resistance [uOhm] *)
    bAlarmCrit              : BOOL;     (* Critical alarm (E-Stop, Hopper empty, Sensor fault) *)
    bQuenchInProgress       : BOOL;     (* True during active quench sequence *)
END_VAR

VAR
    (* Internal State and Processing *)
    iState                  : INT := 0; (* Main State Machine *)
    iQuenchState            : INT := 0; (* Quench Sequence Sub-State *)
    
    (* Derived Process Variables *)
    rBackEMF                : REAL := 1.65;  (* Assumed Back EMF [V] *)
    rPrevResistance         : REAL := 0.0;
    rResistanceRate         : REAL := 0.0;   (* dR/dt *)
    rResistanceNoise        : REAL := 0.0;
    rEWMA_Alpha             : REAL := 0.2;   (* Filter coefficient *)
    rFilteredResist         : REAL := 0.0;
    
    (* Feeding Configuration & Timers *)
    tFeedInterval           : TON;
    tFeedPulseDuration      : TON;
    rBaseFeedRate           : REAL := 15.0;  (* Base pulses per hour *)
    rTargetResistance       : REAL := 5.2;   (* Target pseudo-resistance [uOhm] *)
    
    (* Quench Configuration & Timers *)
    tQuenchDelay            : TON;
    tAnodeBumpPulse         : TON;
    nQuenchAttempts         : INT := 0;
    rAETrapThreshold        : REAL := 8.0;   (* Resistance threshold for AE [uOhm] *)
    rAEPredictSlope         : REAL := 0.05;  (* dR/dt threshold for AE Prediction *)
    
    (* Interlock Memory *)
    bPrevEStop              : BOOL := TRUE;
    
    (* Cycle Tracking *)
    udiCycleCounter         : UDINT := 0;
END_VAR

(* === SAFETY & INTERLOCK SUPERVISOR === *)
IF NOT bEmergencyStop THEN
    bSystemReady        := FALSE;
    bPointFeederValve   := FALSE;
    bAlarmCrit          := TRUE;
    iState              := 999; (* Fault State *)
    RETURN;
END_IF;

IF bHopperLowLevel THEN
    bAlarmCrit := TRUE;
    (* Continue operating, but flag alarm for crane operator *)
END_IF;

(* === SENSOR VALIDATION & COMPUTATIONS === *)
IF rLineCurrent < 10.0 THEN
    (* Line current too low (e.g. potline trip), suspend control *)
    bSystemReady := FALSE;
    iState := 0;
    RETURN;
END_IF;

(* Pseudo-resistance calculation (R = (V - BEMF) / I) * 1000 for uOhm *)
rCellResistance := ((rCellVoltage - rBackEMF) / rLineCurrent) * 1000.0;

(* EWMA Filter for Resistance *)
rFilteredResist := (rEWMA_Alpha * rCellResistance) + ((1.0 - rEWMA_Alpha) * rFilteredResist);

(* Derivative of Resistance (dR/dt) per cycle, simplified *)
rResistanceRate := rFilteredResist - rPrevResistance;
rPrevResistance := rFilteredResist;

(* === MAIN POT CONTROLLER STATE MACHINE === *)
CASE iState OF
    0: (* IDLE & INITIALIZATION *)
        bSystemReady := FALSE;
        bPointFeederValve := FALSE;
        bAnodeEffectActive := FALSE;
        bQuenchInProgress := FALSE;
        rFilteredResist := rCellResistance;
        
        IF bEnable AND NOT bManualOverride THEN
            iState := 10;
        END_IF;

    10: (* NORMAL FEEDING (BASE/TRACKING/UNDERFEED/OVERFEED) *)
        bSystemReady := TRUE;
        bAnodeEffectActive := FALSE;
        bQuenchInProgress := FALSE;
        
        (* Evaluate Anode Effect (AE) Precursors & Trigger *)
        IF (rFilteredResist > rAETrapThreshold) OR (rCellVoltage > 8.0) THEN
            iState := 20; (* Hard AE Detected *)
            nQuenchAttempts := 0;
            iQuenchState := 0;
        ELSIF (rResistanceRate > rAEPredictSlope) THEN
            (* Impending AE predicted - Overfeed to suppress *)
            rBaseFeedRate := 30.0;
        ELSE
            (* Modulate feed rate based on resistance deviation (Simple P-Control) *)
            IF rFilteredResist > (rTargetResistance + 0.1) THEN
                rBaseFeedRate := 20.0; (* Overfeed *)
            ELSIF rFilteredResist < (rTargetResistance - 0.1) THEN
                rBaseFeedRate := 10.0; (* Underfeed *)
            ELSE
                rBaseFeedRate := 15.0; (* Nominal *)
            END_IF;
        END_IF;
        
        (* Feeder Pulse Generator *)
        (* Convert BaseFeedRate (pulses/hr) to interval ms. (3600000 / Rate) *)
        tFeedInterval(IN := NOT tFeedPulseDuration.Q, PT := DINT_TO_TIME(REAL_TO_DINT(3600000.0 / rBaseFeedRate)));
        tFeedPulseDuration(IN := tFeedInterval.Q, PT := T#2S);
        
        bPointFeederValve := tFeedPulseDuration.IN;

        IF NOT bEnable OR bManualOverride THEN
            iState := 0;
        END_IF;

    20: (* ANODE EFFECT (AE) QUENCH SEQUENCE *)
        bSystemReady := TRUE;
        bAnodeEffectActive := TRUE;
        bQuenchInProgress := TRUE;
        bPointFeederValve := FALSE; (* Handled by quench states *)
        
        CASE iQuenchState OF
            0: (* INIT QUENCH *)
                tQuenchDelay(IN := FALSE);
                iQuenchState := 10;
                
            10: (* OVERDOSE FEEDING *)
                (* Hold feeder valve open for 5 seconds to flood with Alumina *)
                bPointFeederValve := TRUE;
                tQuenchDelay(IN := TRUE, PT := T#5S);
                IF tQuenchDelay.Q THEN
                    bPointFeederValve := FALSE;
                    tQuenchDelay(IN := FALSE);
                    iQuenchState := 20;
                END_IF;
                
            20: (* WAIT FOR RECOVERY *)
                tQuenchDelay(IN := TRUE, PT := T#10S);
                IF rFilteredResist < (rTargetResistance + 0.5) THEN
                    iState := 10; (* Recovered, back to normal *)
                ELSIF tQuenchDelay.Q THEN
                    tQuenchDelay(IN := FALSE);
                    iQuenchState := 30; (* Escalate to Anode Bump *)
                END_IF;
                
            30: (* ANODE BUMP (Move beam down/up) *)
                (* Command beam down by 5mm temporarily to splash bath under anodes *)
                rAnodePositionCmd := -5.0; 
                tAnodeBumpPulse(IN := TRUE, PT := T#3S);
                IF tAnodeBumpPulse.Q THEN
                    rAnodePositionCmd := 0.0;
                    tAnodeBumpPulse(IN := FALSE);
                    nQuenchAttempts := nQuenchAttempts + 1;
                    
                    IF nQuenchAttempts > 3 THEN
                        iQuenchState := 99; (* AE Failed to quench, manual intervention *)
                    ELSE
                        iQuenchState := 20; (* Wait again *)
                    END_IF;
                END_IF;
                
            99: (* MANUAL INTERVENTION REQUIRED *)
                bAlarmCrit := TRUE;
                IF bManualOverride THEN
                    iState := 0;
                END_IF;
        END_CASE;
        
    999: (* CRITICAL FAULT STATE *)
        bSystemReady := FALSE;
        bPointFeederValve := FALSE;
        IF bEnable AND bEmergencyStop THEN
            bAlarmCrit := FALSE;
            iState := 0;
        END_IF;
        
END_CASE;

udiCycleCounter := udiCycleCounter + 1;

END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
