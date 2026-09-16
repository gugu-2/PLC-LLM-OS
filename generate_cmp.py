import json
import uuid
import os

prompt = """<USER_REQUEST>
You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Industrial-Scale Continuous Slurry Chemical Mechanical Polishing (CMP) Distribution System**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Nanoparticle settling prevention pulse agitation, ultra-low shear diaphragm pump flow stabilization, and specific gravity refractive index tracking). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_CMP_SlurryDistribution\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Industrial-Scale Continuous Slurry Chemical Mechanical Polishing (CMP) Distribution System

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT.
</USER_REQUEST>"""

code = """```iec-st
FUNCTION_BLOCK FB_CMP_SlurryDistribution
VAR_INPUT
    bSystemEnable           : BOOL;     (* Main system enable command *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal, normally high *)
    rMainTankLevel          : REAL;     (* Main tank level measurement in liters (0-5000L) *)
    rPumpFlowRate           : REAL;     (* Flow meter feedback for ultra-low shear diaphragm pump (L/min) *)
    rSlurryDensity          : REAL;     (* Refractive index/specific gravity tracker output (g/cm3) *)
    bFilterDeltaPHigh       : BOOL;     (* Differential pressure switch across polishing filter (TRUE = blocked) *)
    rLoopReturnPressure     : REAL;     (* Backpressure on the return loop (bar) *)
    rAgitatorSpeedFbk       : REAL;     (* Settling prevention pulse agitator speed feedback (RPM) *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;     (* System ready for fab supply *)
    bPumpRunCmd             : BOOL;     (* Ultra-low shear pump run command *)
    rPumpSpeedRef           : REAL;     (* Speed reference to pump VFD (0-100%) *)
    bAgitatorRunCmd         : BOOL;     (* Pulse agitator run command *)
    rAgitatorSpeedRef       : REAL;     (* Speed reference to agitator VFD (0-100%) *)
    bFilterBypassVlv        : BOOL;     (* Filter bypass valve command *)
    bAlarm                  : BOOL;     (* General fault alarm output *)
    iFaultCode              : INT;      (* Specific fault code for HMI (0 = None) *)
END_VAR
VAR
    iState                  : INT := 0; 
    tAgitationPulseTimer    : TON;      (* Timer for pulsed agitation *)
    tAgitationRestTimer     : TON;
    tPumpStartDelay         : TON;      (* Delay before starting main pump to ensure agitation *)
    rFlowError              : REAL;     (* Flow PID error *)
    rFlowIntegral           : REAL := 0.0;
    rFlowKp                 : REAL := 2.5; 
    rFlowKi                 : REAL := 0.5;
    rFlowSetpoint           : REAL := 25.0; (* Desired L/min *)
    bAgitationActive        : BOOL;
    tWatchdog               : TON;
END_VAR

(* === MAIN LOGIC === *)
IF NOT bEmergencyStop THEN
    bSystemReady      := FALSE;
    bPumpRunCmd       := FALSE;
    bAgitatorRunCmd   := FALSE;
    rPumpSpeedRef     := 0.0;
    rAgitatorSpeedRef := 0.0;
    bAlarm            := TRUE;
    iFaultCode        := 99; (* E-Stop Fault *)
    iState            := 0;
    RETURN;
END_IF;

(* Continuous Specific Gravity / Quality Monitor *)
IF rSlurryDensity < 1.05 OR rSlurryDensity > 1.25 THEN
    bAlarm     := TRUE;
    iFaultCode := 10; (* Density out of specification *)
END_IF;

(* Polishing Filter Delta P Monitor *)
IF bFilterDeltaPHigh THEN
    bFilterBypassVlv := TRUE; (* Protect loop flow *)
    bAlarm := TRUE;
    iFaultCode := 20; (* Filter blocked *)
ELSE
    bFilterBypassVlv := FALSE;
END_IF;

(* Main State Machine *)
CASE iState OF
    0: (* IDLE *)
        bSystemReady      := FALSE;
        bPumpRunCmd       := FALSE;
        bAgitatorRunCmd   := FALSE;
        rPumpSpeedRef     := 0.0;
        rAgitatorSpeedRef := 0.0;
        rFlowIntegral     := 0.0; (* Reset PID *)
        
        IF bSystemEnable AND (iFaultCode = 0) THEN
            iState := 10; (* Transition to Pre-Agitation *)
        END_IF;

    10: (* PRE-AGITATION: Resuspend Nanoparticles *)
        bAgitatorRunCmd   := TRUE;
        rAgitatorSpeedRef := 80.0; (* High speed for resuspension *)
        tPumpStartDelay(IN := TRUE, PT := T#30S);
        
        IF tPumpStartDelay.Q THEN
            tPumpStartDelay(IN := FALSE);
            iState := 20; (* Transition to Flow Ramp *)
        END_IF;

    20: (* PUMP RAMP & PULSE AGITATION *)
        (* Start Pump *)
        bPumpRunCmd := TRUE;
        
        (* PI Control for Ultra-low shear diaphragm pump flow stabilization *)
        rFlowError := rFlowSetpoint - rPumpFlowRate;
        rFlowIntegral := rFlowIntegral + (rFlowError * 0.1); (* Assuming 100ms cycle time approx *)
        
        (* Anti-windup *)
        IF rFlowIntegral > 100.0 THEN rFlowIntegral := 100.0; END_IF;
        IF rFlowIntegral < 0.0 THEN rFlowIntegral := 0.0; END_IF;
        
        rPumpSpeedRef := (rFlowKp * rFlowError) + (rFlowKi * rFlowIntegral);
        
        (* Limit Output *)
        IF rPumpSpeedRef > 100.0 THEN rPumpSpeedRef := 100.0; END_IF;
        IF rPumpSpeedRef < 10.0 THEN rPumpSpeedRef := 10.0; END_IF; (* Min speed *)
        
        (* Pulse Agitation Logic to prevent sheer damage but maintain suspension *)
        tAgitationPulseTimer(IN := NOT tAgitationRestTimer.Q, PT := T#10S);
        tAgitationRestTimer(IN := tAgitationPulseTimer.Q, PT := T#20S);
        
        IF tAgitationPulseTimer.IN AND NOT tAgitationPulseTimer.Q THEN
            bAgitatorRunCmd := TRUE;
            rAgitatorSpeedRef := 40.0; (* Gentle pulse *)
        ELSE
            bAgitatorRunCmd := FALSE;
            rAgitatorSpeedRef := 0.0;
        END_IF;
        
        (* System Ready condition *)
        IF (rPumpFlowRate > 24.0 AND rPumpFlowRate < 26.0) AND (rMainTankLevel > 500.0) THEN
            bSystemReady := TRUE;
        ELSE
            bSystemReady := FALSE;
        END_IF;
        
        (* Shutdown condition *)
        IF NOT bSystemEnable THEN
            iState := 30; (* Shutdown sequence *)
        END_IF;
        
    30: (* SHUTDOWN SEQUENCE *)
        bSystemReady := FALSE;
        rPumpSpeedRef := rPumpSpeedRef - 1.0; (* Gentle ramp down *)
        
        IF rPumpSpeedRef <= 0.0 THEN
            bPumpRunCmd := FALSE;
            bAgitatorRunCmd := FALSE;
            iState := 0;
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
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
