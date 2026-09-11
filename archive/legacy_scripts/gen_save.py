import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Semiconductor Ion Beam Etching (IBE) Defect Mitigation**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Kaufman ion source grid voltage synchronization, argon beam neutralization via thermionic emission, and high-vacuum cryopump regeneration cascading). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_IonBeamEtching\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Semiconductor Ion Beam Etching (IBE) Defect Mitigation

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_IonBeamEtching
VAR_INPUT
    (* Required: at least 4-8 physical inputs with types and comments *)
    bEnable                 : BOOL;     (* System enable signal for IBE *)
    bEmergencyStop          : BOOL;     (* Safety interlock / Emergency Stop OK signal *)
    rBeamVoltage            : REAL;     (* Kaufman source grid beam voltage feedback (kV) *)
    rArgonFlowRate          : REAL;     (* Process argon gas flow rate (sccm) *)
    bCryopumpReady          : BOOL;     (* High-vacuum cryopump nominal state *)
    rChamberPressure        : REAL;     (* Main chamber pressure (Torr) *)
    rNeutralizerCurrent     : REAL;     (* Thermionic emission neutralizer current (mA) *)
    bBeamOnRequest          : BOOL;     (* Request from host to ignite beam *)
END_VAR
VAR_OUTPUT
    (* Required: at least 3-6 outputs with types and comments *)
    bSystemReady            : BOOL;     (* System ready status for etching *)
    rBeamVoltageSP          : REAL;     (* Beam voltage setpoint command (kV) *)
    rArgonFlowSP            : REAL;     (* Argon mass flow controller setpoint (sccm) *)
    bBeamActive             : BOOL;     (* Beam is ignited and stable *)
    bRegenRequired          : BOOL;     (* Cryopump regeneration cascade required *)
    bAlarm                  : BOOL;     (* General fault or interlock tripped *)
    iFaultCode              : INT;      (* Diagnostics: 0=OK, 1=EStop, 2=Vacuum, 3=Ignition *)
END_VAR
VAR
    (* Internal state variables *)
    iState                  : INT := 0; 
    tIgnitionDelay          : TON;
    tStabilization          : TON;
    tNeutralizerCheck       : TON;
    rTargetPressure         : REAL := 5.0E-4; (* Target striking pressure *)
    bInterlockOK            : BOOL;
    rKp_Volt                : REAL := 0.45;
    rKi_Volt                : REAL := 0.05;
    rVoltError              : REAL;
    rVoltIntegral           : REAL;
END_VAR

(* === MAIN LOGIC === *)
(* Safety and Interlock Check *)
bInterlockOK := bEmergencyStop AND bCryopumpReady AND (rChamberPressure < 1.0E-3);

IF NOT bInterlockOK THEN
    bSystemReady := FALSE;
    bBeamActive := FALSE;
    bAlarm := TRUE;
    rBeamVoltageSP := 0.0;
    rArgonFlowSP := 0.0;
    iState := 99; (* Fault State *)
    
    IF NOT bEmergencyStop THEN
        iFaultCode := 1;
    ELSIF NOT bCryopumpReady THEN
        iFaultCode := 2;
        bRegenRequired := TRUE;
    ELSE
        iFaultCode := 2; (* Vacuum issue *)
    END_IF;
    
    RETURN;
END_IF;

bAlarm := FALSE;
iFaultCode := 0;
bRegenRequired := FALSE;

CASE iState OF
    0: (* IDLE AND INITIALIZATION *)
        bSystemReady := TRUE;
        bBeamActive := FALSE;
        rBeamVoltageSP := 0.0;
        rArgonFlowSP := 0.0;
        IF bEnable AND bBeamOnRequest THEN
            bSystemReady := FALSE;
            iState := 10;
        END_IF;

    10: (* GAS FLOW INITIATION *)
        (* Establish target striking pressure using Argon flow *)
        rArgonFlowSP := 15.5; (* Pre-strike flow *)
        IF rChamberPressure > (rTargetPressure * 0.9) AND rChamberPressure < (rTargetPressure * 1.1) THEN
            tIgnitionDelay(IN := TRUE, PT := T#2S);
            IF tIgnitionDelay.Q THEN
                tIgnitionDelay(IN := FALSE);
                iState := 20;
            END_IF;
        ELSE
            tIgnitionDelay(IN := FALSE);
        END_IF;

    20: (* BEAM IGNITION & NEUTRALIZER START *)
        rBeamVoltageSP := 1.2; (* kV for ignition *)
        IF rBeamVoltage > 1.0 AND rNeutralizerCurrent > 50.0 THEN
            iState := 30;
        END_IF;
        (* Timeout logic could be added here *)

    30: (* RAMP & STABILIZATION *)
        (* Simple PI loop simulation for Beam Voltage Control *)
        rVoltError := 2.5 - rBeamVoltage; (* 2.5 kV is the operation target *)
        rVoltIntegral := rVoltIntegral + (rVoltError * 0.1);
        rBeamVoltageSP := 2.5 + (rVoltError * rKp_Volt) + (rVoltIntegral * rKi_Volt);
        
        tStabilization(IN := TRUE, PT := T#5S);
        IF tStabilization.Q THEN
            tStabilization(IN := FALSE);
            iState := 40;
        END_IF;

    40: (* BEAM ACTIVE / PROCESSING *)
        bBeamActive := TRUE;
        
        (* Continuously monitor neutralizer to prevent surface charging defects *)
        tNeutralizerCheck(IN := (rNeutralizerCurrent < 40.0), PT := T#500MS);
        IF tNeutralizerCheck.Q THEN
            iState := 99; (* Drop to fault if neutralization fails *)
            iFaultCode := 3;
        END_IF;

        IF NOT bEnable OR NOT bBeamOnRequest THEN
            iState := 50;
        END_IF;

    50: (* SHUTDOWN SEQUENCE *)
        bBeamActive := FALSE;
        rBeamVoltageSP := 0.0;
        rArgonFlowSP := 0.0;
        iState := 0;

    99: (* FAULT HANDLING *)
        bSystemReady := FALSE;
        bBeamActive := FALSE;
        rBeamVoltageSP := 0.0;
        rArgonFlowSP := 0.0;
        IF bInterlockOK AND NOT bEnable THEN
            iState := 0; (* Reset fault on disable *)
        END_IF;
        
END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs(r"c:\Users\majip\Downloads\LLM REASEARCH\data\swarm_raw", exist_ok=True)
record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": code}
    ]
}

filename = rf"c:\Users\majip\Downloads\LLM REASEARCH\data\swarm_raw\agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
