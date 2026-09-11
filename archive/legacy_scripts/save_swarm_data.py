import json, uuid
import os

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Industrial Scale High-Volume Water Desalination (SWRO)**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., High-pressure (80 bar) reverse osmosis membrane train, isobaric energy recovery device (ERD) brine mixing, and antiscalant dosing proportional to total dissolved solids (TDS)). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_SWRO_Desalination\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Industrial Scale High-Volume Water Desalination (SWRO)

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_SWRO_Membrane_Train_Control
(* 
   =============================================================================
   Block: FB_SWRO_Membrane_Train_Control
   Description: Advanced control for High-Volume Seawater Reverse Osmosis 
                (SWRO) membrane trains. Includes high-pressure pump (HPP) 
                coordination, isobaric Energy Recovery Device (ERD) control, 
                brine mixing, and flow-proportional antiscalant dosing 
                based on Total Dissolved Solids (TDS).
   Author: Senior Automation Architect
   Version: 1.0.0
   =============================================================================
*)

VAR_INPUT
    bEnableTrain         : BOOL;  (* System enable command from Master SCADA *)
    bEmergencyStop       : BOOL;  (* Safety relay OK signal (FALSE = Trip) *)
    bPermissiveStart     : BOOL;  (* Upstream intake & pretreatment ready *)
    
    rFeedWaterFlow_m3h   : REAL;  (* Feed water flow rate (m^3/h) *)
    rFeedWaterTDS_ppm    : REAL;  (* Feed water Total Dissolved Solids (ppm) *)
    rFeedWaterTemp_C     : REAL;  (* Feed water temperature (Celsius) *)
    
    rHPP_Pressure_bar    : REAL;  (* High Pressure Pump discharge pressure (bar) - Target ~80 bar *)
    rERD_BrinePress_bar  : REAL;  (* ERD brine side pressure (bar) *)
    rPermeateFlow_m3h    : REAL;  (* Permeate (product water) flow rate (m^3/h) *)
    
    rTargetRecoveryPct   : REAL := 45.0; (* Target recovery rate (%) *)
END_VAR

VAR_OUTPUT
    bSystemReady         : BOOL;  (* SWRO train is ready for operation *)
    bTrainRunning        : BOOL;  (* SWRO train is in steady state operation *)
    bAlarmActive         : BOOL;  (* Global alarm output (latching) *)
    
    rHPPSpeedRef_pct     : REAL;  (* HPP VFD speed reference (0-100%) *)
    rDosingPumpRef_mLh   : REAL;  (* Antiscalant dosing pump speed (mL/h) *)
    rERDValvePos_pct     : REAL;  (* ERD booster pump / valve position (0-100%) *)
    
    rCalculatedRecovery  : REAL;  (* Real-time calculated recovery rate (%) *)
END_VAR

VAR
    iState               : INT := 0; (* Internal state machine *)
    
    (* Timers *)
    tStartupDelay        : TON;
    tHPP_RampTimer       : TON;
    tFlushTimer          : TON;
    tFaultTimer          : TON;
    
    (* PID Controllers for Pressure & Flow *)
    stHPP_PID            : PID;
    stERD_PID            : PID;
    
    (* Internal Calculations *)
    rBaseDosingRate      : REAL := 2.5; (* Base dosing rate in mg/L per 35000 ppm TDS *)
    rTDS_Factor          : REAL;
    
    (* Alarms & Faults *)
    bHighPressureTrip    : BOOL;
    bLowFlowTrip         : BOOL;
    bERDFault            : BOOL;
    bUnsafeTemp          : BOOL;
END_VAR

(* === MAIN LOGIC START === *)

(* 1. Safety & Interlocks *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bTrainRunning := FALSE;
    bAlarmActive := TRUE;
    rHPPSpeedRef_pct := 0.0;
    rDosingPumpRef_mLh := 0.0;
    rERDValvePos_pct := 0.0;
    iState := 999; (* Transition to Emergency Fault State *)
    RETURN;
END_IF;

(* Evaluate Trips *)
bHighPressureTrip := (rHPP_Pressure_bar > 85.0);
bLowFlowTrip := (rFeedWaterFlow_m3h < 10.0) AND bTrainRunning;
bUnsafeTemp := (rFeedWaterTemp_C < 5.0) OR (rFeedWaterTemp_C > 45.0);

IF bHighPressureTrip OR bLowFlowTrip OR bUnsafeTemp THEN
    bAlarmActive := TRUE;
    IF iState < 900 THEN
        iState := 900; (* Controlled Shutdown State *)
    END_IF;
END_IF;

(* 2. Real-time Calculations *)
IF rFeedWaterFlow_m3h > 0.1 THEN
    rCalculatedRecovery := (rPermeateFlow_m3h / rFeedWaterFlow_m3h) * 100.0;
ELSE
    rCalculatedRecovery := 0.0;
END_IF;

(* Dosing Calculation: Proportional to Flow and TDS *)
rTDS_Factor := rFeedWaterTDS_ppm / 35000.0;
IF rTDS_Factor < 0.5 THEN rTDS_Factor := 0.5; END_IF;

rDosingPumpRef_mLh := rFeedWaterFlow_m3h * rBaseDosingRate * rTDS_Factor;

(* 3. Main State Machine *)
CASE iState OF
    0: (* IDLE & STANDBY *)
        bSystemReady := bPermissiveStart AND NOT bAlarmActive;
        bTrainRunning := FALSE;
        rHPPSpeedRef_pct := 0.0;
        rERDValvePos_pct := 0.0;
        
        IF bSystemReady AND bEnableTrain THEN
            iState := 10;
        END_IF;

    10: (* PRE-START / FLUSHING *)
        (* Open feed valves and allow low pressure flow *)
        tFlushTimer(IN := TRUE, PT := T#30S);
        IF tFlushTimer.Q THEN
            tFlushTimer(IN := FALSE);
            iState := 20;
        END_IF;

    20: (* HPP RAMP UP *)
        (* Gradually ramp up high pressure pump to overcome osmotic pressure *)
        tHPP_RampTimer(IN := TRUE, PT := T#60S);
        rHPPSpeedRef_pct := 30.0 + (70.0 * (TIME_TO_REAL(tHPP_RampTimer.ET) / TIME_TO_REAL(T#60S)));
        
        IF tHPP_RampTimer.Q THEN
            tHPP_RampTimer(IN := FALSE);
            iState := 30;
        END_IF;

    30: (* STEADY STATE CONTROL *)
        bTrainRunning := TRUE;
        
        (* Cascade control for HPP based on permeate flow & recovery *)
        stHPP_PID(
            ACTUAL := rCalculatedRecovery,
            SET_POINT := rTargetRecoveryPct,
            KP := 1.2,
            TN := 5.0,
            TV := 0.0
        );
        rHPPSpeedRef_pct := stHPP_PID.Y;
        
        (* ERD balancing: Ensure brine pressure doesn't exceed HPP pressure *)
        stERD_PID(
            ACTUAL := rERD_BrinePress_bar,
            SET_POINT := rHPP_Pressure_bar - 2.0, (* 2 bar differential *)
            KP := 0.8,
            TN := 3.0
        );
        rERDValvePos_pct := stERD_PID.Y;

        IF NOT bEnableTrain THEN
            iState := 900;
        END_IF;

    900: (* CONTROLLED SHUTDOWN *)
        bTrainRunning := FALSE;
        rHPPSpeedRef_pct := rHPPSpeedRef_pct - 1.0; (* Ramp down *)
        IF rHPPSpeedRef_pct <= 0.0 THEN
            rHPPSpeedRef_pct := 0.0;
            iState := 0;
        END_IF;

    999: (* EMERGENCY FAULT *)
        bTrainRunning := FALSE;
        rHPPSpeedRef_pct := 0.0;
        rERDValvePos_pct := 0.0;
        rDosingPumpRef_mLh := 0.0;
        
        IF NOT bEmergencyStop THEN
            (* Wait for safety reset *)
        ELSE
            IF NOT bAlarmActive THEN
                iState := 0;
            END_IF;
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}

with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print("Saved.")
