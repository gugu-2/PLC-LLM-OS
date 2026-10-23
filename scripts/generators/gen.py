import os, json, uuid

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Next-Gen Micro-LED Display Mass Transfer Fluidic Self-Assembly**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Electro-kinetic fluidic channel vortex shedding, sub-micron die stochastic yield tracking, and high-speed acoustic tweezer array mapping). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_MicroLED_MassTransfer\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Next-Gen Micro-LED Display Mass Transfer Fluidic Self-Assembly

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_MicroLED_Fluidic_SelfAssembly
VAR_INPUT
    (* Core System Enables & Safety *)
    bEnable               : BOOL;   (* System enable signal *)
    bEmergencyStop        : BOOL;   (* Safety relay OK signal - Active High *)
    (* Process Physical Inputs *)
    rFluidicPressure      : REAL;   (* Electro-kinetic fluidic channel pressure in mBar *)
    rAcousticTweezerFreq  : REAL;   (* Acoustic array mapping frequency in MHz *)
    rDieConcentration     : REAL;   (* In-flow sub-micron die suspension concentration (die/mL) *)
    rFluidTemperature     : REAL;   (* Suspension fluid temperature in deg C *)
    bSubstrateReady       : BOOL;   (* Interlock: Target substrate aligned and vacuum locked *)
    rFlowRateFeedback     : REAL;   (* Mass flow meter feedback (uL/min) *)
END_VAR
VAR_OUTPUT
    (* System Status & Controls *)
    bSystemReady          : BOOL;   (* System initialized and ready for assembly *)
    bTransferActive       : BOOL;   (* Fluidic self-assembly mass transfer in progress *)
    rVortexAmplitude      : REAL;   (* Control signal to acoustic vortex generator (um) *)
    rPumpControlSetpt     : REAL;   (* Control signal to precision micro-fluidic pump (uL/min) *)
    (* Analytics & Faults *)
    rCurrentYieldPercent  : REAL;   (* Real-time stochastic yield tracking estimation (%) *)
    bAlarm                : BOOL;   (* Fault alarm output / Critical process deviation *)
    iErrorCode            : INT;    (* Diagnostic error code for HMI *)
END_VAR
VAR
    (* Internal State and Timers *)
    iStep                 : INT := 0; (* Main sequence state machine *)
    tStabilizationTimer   : TON;      (* Fluidic channel stabilization delay *)
    tAssemblyTimer        : TON;      (* Self-assembly duration timer *)
    
    (* Mathematical & Filtering State *)
    rFilteredPressure     : REAL;
    rAlphaPressure        : REAL := 0.05; (* Low pass filter coefficient *)
    rVortexSheddingIntegral: REAL := 0.0;
    
    (* Acoustic Tweezer Control *)
    rResonanceTarget      : REAL := 42.5; (* Nominal resonance for 10um die in MHz *)
    rTweezerPhaseOffset   : REAL;
    
    (* Tracking *)
    iTotalDieProcessed    : DINT := 0;
    iDieSuccessfullyMated : DINT := 0;
END_VAR

(* === MAIN SAFETY & INTERLOCK LOGIC === *)
IF NOT bEmergencyStop THEN
    bSystemReady      := FALSE;
    bTransferActive   := FALSE;
    rVortexAmplitude  := 0.0;
    rPumpControlSetpt := 0.0;
    bAlarm            := TRUE;
    iErrorCode        := 9999; (* E-Stop Active *)
    iStep             := 0;
    RETURN;
END_IF;

(* Fluidic Pressure Signal Filtering (First-Order Low Pass) *)
rFilteredPressure := (rAlphaPressure * rFluidicPressure) + ((1.0 - rAlphaPressure) * rFilteredPressure);

(* === STATE MACHINE FOR MASS TRANSFER === *)
CASE iStep OF
    0: (* IDLE & SYSTEM CHECK *)
        bSystemReady := TRUE;
        bTransferActive := FALSE;
        rVortexAmplitude := 0.0;
        rPumpControlSetpt := 10.0; (* Idle recirculation flow *)
        
        IF bEnable AND bSubstrateReady THEN
            bSystemReady := FALSE;
            iStep := 10;
            bAlarm := FALSE;
            iErrorCode := 0;
        END_IF;

    10: (* FLUIDIC STABILIZATION *)
        (* Ramp up flow to target operation *)
        rPumpControlSetpt := 250.0; (* Operational flow uL/min *)
        
        tStabilizationTimer(IN := TRUE, PT := T#15S);
        
        (* Check pressure bounds *)
        IF rFilteredPressure > 1500.0 THEN
            bAlarm := TRUE;
            iErrorCode := 1001; (* Over-pressure fault *)
            iStep := 900;
        END_IF;

        IF tStabilizationTimer.Q THEN
            tStabilizationTimer(IN := FALSE);
            IF ABS(rFlowRateFeedback - rPumpControlSetpt) < 5.0 THEN
                iStep := 20; (* Stable, proceed to acoustic mapping *)
            END_IF;
        END_IF;

    20: (* ACOUSTIC TWEEZER ARRAY MAPPING & VORTEX SHEDDING *)
        bTransferActive := TRUE;
        
        (* Calculate optimal acoustic vortex amplitude based on resonance feedback *)
        rTweezerPhaseOffset := ABS(rAcousticTweezerFreq - rResonanceTarget);
        rVortexAmplitude := (rDieConcentration * 0.015) + (rTweezerPhaseOffset * 2.5);
        
        (* Bound the amplitude to hardware limits (0.0 to 100.0 um) *)
        IF rVortexAmplitude > 100.0 THEN
            rVortexAmplitude := 100.0;
        ELSIF rVortexAmplitude < 0.0 THEN
            rVortexAmplitude := 0.0;
        END_IF;
        
        (* Simulate Stochastic Yield Accumulation based on Flow & Frequency match *)
        IF (rTweezerPhaseOffset < 0.5) AND (rFilteredPressure > 800.0) THEN
            iTotalDieProcessed := iTotalDieProcessed + 500;
            (* Yield model: higher pressure & exact resonance = ~99.9% yield *)
            iDieSuccessfullyMated := iDieSuccessfullyMated + 499; 
        ELSE
            iTotalDieProcessed := iTotalDieProcessed + 500;
            iDieSuccessfullyMated := iDieSuccessfullyMated + 470; (* Sub-optimal yield *)
        END_IF;
        
        (* Calculate real-time percentage yield *)
        IF iTotalDieProcessed > 0 THEN
            rCurrentYieldPercent := (DINT_TO_REAL(iDieSuccessfullyMated) / DINT_TO_REAL(iTotalDieProcessed)) * 100.0;
        END_IF;

        (* Self-Assembly Duration *)
        tAssemblyTimer(IN := TRUE, PT := T#120S);
        IF tAssemblyTimer.Q THEN
            tAssemblyTimer(IN := FALSE);
            iStep := 30;
        END_IF;
        
        (* Check for system disable request *)
        IF NOT bEnable THEN
            iStep := 30; (* Graceful shutdown *)
        END_IF;

    30: (* SHUTDOWN & COMPLETE *)
        bTransferActive := FALSE;
        rVortexAmplitude := 0.0;
        rPumpControlSetpt := 0.0; (* Stop flow *)
        
        IF rFilteredPressure < 50.0 THEN
            (* Wait for pressure to bleed off before reporting ready *)
            bSystemReady := TRUE;
            iStep := 0; 
        END_IF;

    900: (* FAULT HANDLING *)
        bTransferActive := FALSE;
        rVortexAmplitude := 0.0;
        rPumpControlSetpt := 0.0;
        bAlarm := TRUE;
        
        IF NOT bEnable THEN
            (* Acknowledge fault by dropping enable *)
            bAlarm := FALSE;
            iErrorCode := 0;
            iStep := 0;
        END_IF;
        
END_CASE;

END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
