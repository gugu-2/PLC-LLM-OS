import json, uuid, os

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Advanced Semiconductor High-Density Plasma Chemical Vapor Deposition (HDP-CVD)**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Inductively coupled plasma (ICP) multi-zone RF matching network, silane/oxygen precursor stoichiometric ratio closed-loop, and electrostatic chuck (ESC) back-side helium cooling). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_HDP_CVD_Chamber\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Advanced Semiconductor High-Density Plasma Chemical Vapor Deposition (HDP-CVD)

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_HDP_CVD_Chamber
VAR_INPUT
    (* Safety and Enable *)
    bEnable                 : BOOL;     (* System enable signal *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal (Active HIGH = Safe) *)
    
    (* Gas Precursor Feedback *)
    rSiH4FlowFeedback       : REAL;     (* Silane (SiH4) flow feedback in sccm *)
    rO2FlowFeedback         : REAL;     (* Oxygen (O2) flow feedback in sccm *)
    rArFlowFeedback         : REAL;     (* Argon (Ar) flow feedback in sccm *)
    
    (* Chamber Parameters *)
    rChamberPressure        : REAL;     (* Chamber pressure in mTorr *)
    rEscTempBackside        : REAL;     (* Electrostatic Chuck (ESC) backside He temperature in DegC *)
    rEscHePressureFeedback  : REAL;     (* ESC backside Helium pressure in Torr *)
    
    (* RF and Plasma Parameters *)
    rRfForwardPower         : REAL;     (* Forward RF power from generator in Watts *)
    rRfReflectedPower       : REAL;     (* Reflected RF power in Watts *)
    bPlasmaOpticalEmission  : BOOL;     (* Plasma strike confirmation via Optical Emission Spectroscopy *)
END_VAR
VAR_OUTPUT
    (* Status and Alarms *)
    bSystemReady            : BOOL;     (* System ready status *)
    bProcessComplete        : BOOL;     (* Batch / Wafer process complete *)
    bAlarm                  : BOOL;     (* Fault alarm output *)
    iCurrentState           : INT;      (* Current Step in Process Recipe *)
    
    (* Actuator Controls *)
    rSiH4FlowCmd            : REAL;     (* Silane (SiH4) flow command in sccm *)
    rO2FlowCmd              : REAL;     (* Oxygen (O2) flow command in sccm *)
    rArFlowCmd              : REAL;     (* Argon (Ar) flow command in sccm *)
    rRfPowerCmd             : REAL;     (* RF Generator power setpoint in Watts *)
    rEscHePressureCmd       : REAL;     (* ESC backside He pressure control in Torr *)
    bThrottleValveOpen      : BOOL;     (* Roughing throttle valve fully open *)
END_VAR
VAR
    (* Internal State and Timers *)
    iState                  : INT := 0; 
    tStepTimer              : TON;
    tPlasmaTimeout          : TON;
    
    (* Constants and Setpoints *)
    rTargetPressure         : REAL := 5.0;      (* mTorr target for deposition *)
    rStoichRatio            : REAL := 1.8;      (* O2:SiH4 stoichiometric ratio *)
    rTargetSiH4             : REAL := 150.0;    (* sccm *)
    rMaxReflectedPower      : REAL := 50.0;     (* Watts maximum reflected acceptable *)
    rTargetRFPower          : REAL := 2500.0;   (* Watts for dense plasma strike *)
    
    (* Error Codes *)
    iErrorCode              : INT := 0;
END_VAR

(* === MAIN LOGIC AND SAFETY INTERLOCKS === *)
IF NOT bEmergencyStop THEN
    (* Immediate Safe State Enforcement *)
    bSystemReady        := FALSE;
    bAlarm              := TRUE;
    iErrorCode          := 999; (* E-STOP Active *)
    
    (* Zero all energy and precursor outputs *)
    rSiH4FlowCmd        := 0.0;
    rO2FlowCmd          := 0.0;
    rArFlowCmd          := 0.0;
    rRfPowerCmd         := 0.0;
    rEscHePressureCmd   := 0.0;
    bThrottleValveOpen  := TRUE; (* Open to high vacuum pump *)
    
    iState := 0;
    RETURN;
END_IF;

(* Continuous Reflected Power Monitoring (RF Matching Network Health) *)
IF iState >= 40 AND iState <= 50 THEN
    IF rRfReflectedPower > rMaxReflectedPower THEN
        bAlarm := TRUE;
        iErrorCode := 101; (* High Reflected RF Power - Match Network Failure *)
        iState := 99; (* Jump to Fault State *)
    END_IF;
END_IF;

(* Continuous ESC Cooling Monitor *)
IF rEscTempBackside > 65.0 THEN
    bAlarm := TRUE;
    iErrorCode := 102; (* ESC Over-temperature Warning *)
    iState := 99;
END_IF;

CASE iState OF
    0: (* IDLE *)
        bSystemReady := TRUE;
        bProcessComplete := FALSE;
        bAlarm := FALSE;
        iErrorCode := 0;
        
        rSiH4FlowCmd := 0.0;
        rO2FlowCmd := 0.0;
        rArFlowCmd := 0.0;
        rRfPowerCmd := 0.0;
        
        IF bEnable THEN
            bSystemReady := FALSE;
            iState := 10;
        END_IF;

    10: (* PUMP DOWN *)
        bThrottleValveOpen := TRUE;
        rEscHePressureCmd := 8.0; (* Pre-charge ESC backside He *)
        
        IF rChamberPressure < 1.0 THEN (* Base pressure reached *)
            iState := 20;
        END_IF;

    20: (* GAS STABILIZATION *)
        bThrottleValveOpen := FALSE;
        (* Introduce Argon for Plasma Strike and Precursors *)
        rArFlowCmd := 200.0;
        rSiH4FlowCmd := rTargetSiH4;
        rO2FlowCmd := rTargetSiH4 * rStoichRatio; (* Closed-loop stoichiometric setpoint *)
        
        tStepTimer(IN := TRUE, PT := T#10S);
        
        (* Verify flows are within 5% of target before proceeding *)
        IF tStepTimer.Q THEN
            tStepTimer(IN := FALSE);
            IF ABS(rSiH4FlowFeedback - rSiH4FlowCmd) < (0.05 * rSiH4FlowCmd) AND
               ABS(rO2FlowFeedback - rO2FlowCmd) < (0.05 * rO2FlowCmd) THEN
                iState := 30;
            ELSE
                bAlarm := TRUE;
                iErrorCode := 201; (* MFC Flow Stabilization Timeout *)
                iState := 99;
            END_IF;
        END_IF;

    30: (* PLASMA STRIKE *)
        rRfPowerCmd := rTargetRFPower;
        
        tPlasmaTimeout(IN := TRUE, PT := T#3S);
        
        IF bPlasmaOpticalEmission THEN
            tPlasmaTimeout(IN := FALSE);
            iState := 40;
        ELSIF tPlasmaTimeout.Q THEN
            tPlasmaTimeout(IN := FALSE);
            bAlarm := TRUE;
            iErrorCode := 301; (* Plasma Strike Failure *)
            iState := 99;
        END_IF;

    40: (* HDP-CVD DEPOSITION *)
        (* Closed loop RF regulation could be implemented here *)
        tStepTimer(IN := TRUE, PT := T#60S); (* 60 second deposition recipe *)
        
        IF tStepTimer.Q THEN
            tStepTimer(IN := FALSE);
            iState := 50;
        END_IF;

    50: (* RF OFF & GAS FLUSH *)
        rRfPowerCmd := 0.0;
        rSiH4FlowCmd := 0.0;
        rO2FlowCmd := 0.0;
        rArFlowCmd := 500.0; (* High Argon purge *)
        
        tStepTimer(IN := TRUE, PT := T#15S);
        IF tStepTimer.Q THEN
            tStepTimer(IN := FALSE);
            iState := 60;
        END_IF;

    60: (* COMPLETE *)
        rArFlowCmd := 0.0;
        bThrottleValveOpen := TRUE;
        bProcessComplete := TRUE;
        
        IF NOT bEnable THEN
            iState := 0;
        END_IF;

    99: (* FAULT HANDLING *)
        rRfPowerCmd := 0.0;
        rSiH4FlowCmd := 0.0;
        rO2FlowCmd := 0.0;
        rArFlowCmd := 0.0;
        bThrottleValveOpen := TRUE;
        
        IF NOT bEnable AND NOT bEmergencyStop THEN
            iState := 0; (* Reset sequence *)
        END_IF;

END_CASE;

iCurrentState := iState;

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
