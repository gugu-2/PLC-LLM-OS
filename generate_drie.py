import os, json, uuid

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Semiconductor Deep Reactive Ion Etching (DRIE) Bosch Process**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., SF6 isotropic etch / C4F8 fluorocarbon passivation sub-second alternation, chuck electrostatic clamping (ESC) high-voltage pulsing, and inductively coupled plasma (ICP) matching). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_SemiconductorDRIE\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Semiconductor Deep Reactive Ion Etching (DRIE) Bosch Process

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_Bosch_DRIE_Process_Controller
(*
    Advanced Deep Reactive Ion Etching (DRIE) Bosch Process Controller.
    Handles precise sub-second alternation between SF6 etch and C4F8 passivation cycles.
    Includes Electrostatic Chuck (ESC) control and Inductively Coupled Plasma (ICP) RF matching.
    Strict safety and interlock handling for toxic gas MFCs and high voltage RF generators.
*)
VAR_INPUT
    bEnable                 : BOOL;     (* System overall enable signal *)
    bEmergencyStop          : BOOL;     (* Main safety circuit status (TRUE = OK, FALSE = E-STOP) *)
    bVacuumInterlockOK      : BOOL;     (* Vacuum system interlock OK *)
    bChamberCoolingOK       : BOOL;     (* Chiller flow and temperature interlock OK *)
    
    rChamberPressure        : REAL;     (* Current chamber pressure in mTorr *)
    rESCTemperature         : REAL;     (* Electrostatic chuck temperature in degrees C *)
    rReflectedPowerICP      : REAL;     (* ICP coil reflected RF power in Watts *)
    rReflectedPowerBias     : REAL;     (* Wafer bias reflected RF power in Watts *)
    
    iTargetCycles           : INT;      (* Number of Bosch process cycles to execute *)
    tEtchPhaseDuration      : TIME;     (* Duration of the SF6 isotropic etch phase *)
    tPassivationPhaseDuration : TIME;   (* Duration of the C4F8 passivation phase *)
    rTargetESCVVoltage      : REAL;     (* Target ESC clamping voltage in kV *)
END_VAR

VAR_OUTPUT
    bSystemReady            : BOOL;     (* Controller ready for sequence *)
    bProcessActive          : BOOL;     (* High when Bosch process is actively running *)
    bProcessComplete        : BOOL;     (* Pulses high for one scan when target cycles are reached *)
    bAlarm                  : BOOL;     (* Critical alarm output *)
    iAlarmCode              : INT;      (* Diagnostics error code *)
    
    rSetPoint_SF6_MFC       : REAL;     (* Flow setpoint for SF6 Mass Flow Controller in sccm *)
    rSetPoint_C4F8_MFC      : REAL;     (* Flow setpoint for C4F8 Mass Flow Controller in sccm *)
    rSetPoint_ICP_Power     : REAL;     (* Forward power setpoint for ICP RF generator in W *)
    rSetPoint_Bias_Power    : REAL;     (* Forward power setpoint for Bias RF generator in W *)
    rSetPoint_ESC_Voltage   : REAL;     (* Commanded ESC clamping voltage in kV *)
    
    iCurrentCycle           : INT;      (* Current executed cycle count *)
END_VAR

VAR
    iState                  : INT := 0; (* Main state machine variable *)
    tPhaseTimer             : TON;      (* High-resolution timer for sub-second gas switching *)
    tInterlockDebounce      : TON;      (* Timer to debounce transient interlock drops *)
    
    bEtchActive             : BOOL;     (* Internal flag for etch phase *)
    bPassivationActive      : BOOL;     (* Internal flag for passivation phase *)
    
    (* Process Recipe Constants *)
    c_rEtchICP_Power        : REAL := 2500.0;
    c_rEtchBias_Power       : REAL := 150.0;
    c_rEtchSF6_Flow         : REAL := 300.0;
    
    c_rPassivationICP_Power : REAL := 1500.0;
    c_rPassivationBias_Power: REAL := 10.0;
    c_rPassivationC4F8_Flow : REAL := 150.0;
    
    c_rMaxReflectedPower    : REAL := 50.0;  (* Max allowable reflected power before tripping *)
END_VAR

(* === SAFETY & INTERLOCK LOGIC === *)
(* Immediate hardware protection overrides all other states *)
IF NOT bEmergencyStop OR NOT bVacuumInterlockOK OR NOT bChamberCoolingOK THEN
    bSystemReady := FALSE;
    bProcessActive := FALSE;
    bAlarm := TRUE;
    iAlarmCode := 1000; (* E-STOP or Hardware Interlock dropped *)
    
    (* Zero all active outputs immediately *)
    rSetPoint_SF6_MFC := 0.0;
    rSetPoint_C4F8_MFC := 0.0;
    rSetPoint_ICP_Power := 0.0;
    rSetPoint_Bias_Power := 0.0;
    rSetPoint_ESC_Voltage := 0.0;
    iState := 999; (* Enter Fault State *)
    RETURN;
END_IF;

(* Monitor Reflected Power - Trip if too high (plasma un-matched or extinguished) *)
IF (rReflectedPowerICP > c_rMaxReflectedPower) OR (rReflectedPowerBias > c_rMaxReflectedPower) THEN
    IF bProcessActive THEN
        bAlarm := TRUE;
        iAlarmCode := 1001; (* RF Match Failure *)
        iState := 999;
    END_IF;
END_IF;


(* === MAIN BOSCH PROCESS STATE MACHINE === *)
CASE iState OF

    0: (* INIT & IDLE *)
        bSystemReady := TRUE;
        bProcessActive := FALSE;
        bProcessComplete := FALSE;
        bAlarm := FALSE;
        iAlarmCode := 0;
        iCurrentCycle := 0;
        
        (* Safing outputs *)
        rSetPoint_SF6_MFC := 0.0;
        rSetPoint_C4F8_MFC := 0.0;
        rSetPoint_ICP_Power := 0.0;
        rSetPoint_Bias_Power := 0.0;
        rSetPoint_ESC_Voltage := 0.0;
        
        IF bEnable AND NOT bAlarm THEN
            bSystemReady := FALSE;
            iState := 10;
        END_IF;

    10: (* WAFER CLAMPING (ESC ENGAGE) *)
        rSetPoint_ESC_Voltage := rTargetESCVVoltage;
        bProcessActive := TRUE;
        
        (* Delay to allow chuck voltage to stabilize and helium backside cooling to establish *)
        tPhaseTimer(IN := TRUE, PT := T#2S);
        IF tPhaseTimer.Q THEN
            tPhaseTimer(IN := FALSE);
            iState := 20;
        END_IF;

    20: (* PASSIVATION PHASE (C4F8 Polymer Deposition) *)
        bEtchActive := FALSE;
        bPassivationActive := TRUE;
        
        rSetPoint_SF6_MFC := 0.0;
        rSetPoint_C4F8_MFC := c_rPassivationC4F8_Flow;
        rSetPoint_ICP_Power := c_rPassivationICP_Power;
        rSetPoint_Bias_Power := c_rPassivationBias_Power;
        
        tPhaseTimer(IN := TRUE, PT := tPassivationPhaseDuration);
        IF tPhaseTimer.Q THEN
            tPhaseTimer(IN := FALSE);
            iState := 30;
        END_IF;

    30: (* ETCH PHASE (SF6 Isotropic Silicon Etch) *)
        bEtchActive := TRUE;
        bPassivationActive := FALSE;
        
        rSetPoint_C4F8_MFC := 0.0;
        rSetPoint_SF6_MFC := c_rEtchSF6_Flow;
        rSetPoint_ICP_Power := c_rEtchICP_Power;
        rSetPoint_Bias_Power := c_rEtchBias_Power;
        
        tPhaseTimer(IN := TRUE, PT := tEtchPhaseDuration);
        IF tPhaseTimer.Q THEN
            tPhaseTimer(IN := FALSE);
            iCurrentCycle := iCurrentCycle + 1;
            
            IF iCurrentCycle >= iTargetCycles THEN
                iState := 40; (* Process complete *)
            ELSE
                iState := 20; (* Loop back to Passivation *)
            END_IF;
        END_IF;

    40: (* PROCESS COMPLETE SHUTDOWN *)
        (* Extinguish Plasma and shut gas *)
        rSetPoint_SF6_MFC := 0.0;
        rSetPoint_C4F8_MFC := 0.0;
        rSetPoint_ICP_Power := 0.0;
        rSetPoint_Bias_Power := 0.0;
        
        tPhaseTimer(IN := TRUE, PT := T#1S);
        IF tPhaseTimer.Q THEN
            tPhaseTimer(IN := FALSE);
            iState := 50;
        END_IF;

    50: (* DECLAMP WAFER *)
        rSetPoint_ESC_Voltage := 0.0;
        
        tPhaseTimer(IN := TRUE, PT := T#1S);
        IF tPhaseTimer.Q THEN
            tPhaseTimer(IN := FALSE);
            bProcessActive := FALSE;
            bProcessComplete := TRUE;
            iState := 60;
        END_IF;
        
    60: (* WAIT FOR DISABLE *)
        IF NOT bEnable THEN
            bProcessComplete := FALSE;
            iState := 0;
        END_IF;

    999: (* FAULT HANDLING *)
        bProcessActive := FALSE;
        rSetPoint_SF6_MFC := 0.0;
        rSetPoint_C4F8_MFC := 0.0;
        rSetPoint_ICP_Power := 0.0;
        rSetPoint_Bias_Power := 0.0;
        rSetPoint_ESC_Voltage := 0.0;
        
        IF NOT bEnable AND bEmergencyStop AND bVacuumInterlockOK AND bChamberCoolingOK THEN
            (* Wait for operator to clear enable to acknowledge fault *)
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

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
