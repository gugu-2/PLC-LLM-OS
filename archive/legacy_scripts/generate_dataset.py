import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Next-Gen Superconducting Maglev Train Cryostat Bogie**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., 8-stage pulse tube cryocooler sequence optimization, electrodynamic suspension (EDS) high-speed gap measurement, and levitation coil quench isolation bypassing). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_Maglev_CryostatBogie\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Next-Gen Superconducting Maglev Train Cryostat Bogie

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_Maglev_CryoBogie_Control
VAR_INPUT
    (* Required: at least 4-8 physical inputs with types and comments *)
    bSystemEnable : BOOL; (* Main power and logic enable for the bogie control system *)
    bEmergencyStop : BOOL; (* Safety loop OK, TRUE means nominal safe state *)
    rHeLvl_Cryostat : REAL; (* Liquid Helium level in cryostat (percentage %) *)
    rTemp_Coil_Front : REAL; (* SCM coil temperature at the front winding (K) *)
    rTemp_Coil_Rear : REAL; (* SCM coil temperature at the rear winding (K) *)
    rLevitationGap_Left : REAL; (* Bogie to guideway gap left side (mm) *)
    rLevitationGap_Right : REAL; (* Bogie to guideway gap right side (mm) *)
    bQuenchDetect_Raw : BOOL; (* Hardware quench detection signal from primary sensors *)
END_VAR
VAR_OUTPUT
    (* Required: at least 3-6 outputs with types and comments *)
    bSystemReady : BOOL; (* System ready status for main train propulsion network *)
    rCryocoolerPower : REAL; (* Compressor power setpoint output (kW) *)
    bQuenchIsolateTrigger : BOOL; (* Trigger to dump internal stored energy to braking resistors *)
    rEDS_CorrectionAmp_Left : REAL; (* Correction current to left suspension coils (A) *)
    rEDS_CorrectionAmp_Right : REAL; (* Correction current to right suspension coils (A) *)
    bAlarm : BOOL; (* Fault alarm output for SCADA reporting *)
END_VAR
VAR
    (* Internal state variables and timers *)
    iState : INT := 0; (* Main execution state machine pointer *)
    tQuenchDebounce : TON; (* Debounce timer for transient quench spikes *)
    tCoolingTimer : TON; (* Max time allowed for cooldown procedures *)
    
    (* Control loop internal variables *)
    rTargetGap : REAL := 12.0; (* Nominal levitation gap setpoint in mm *)
    rGapError_Left : REAL;
    rGapError_Right : REAL;
    rKp_EDS : REAL := 18.25; (* Proportional gain for suspension correction *)
    rKd_EDS : REAL := 4.15; (* Derivative gain for suspension damping *)
    rPrevGapError_Left : REAL := 0.0;
    rPrevGapError_Right : REAL := 0.0;
    rDerivative_Left : REAL;
    rDerivative_Right : REAL;
    rMaxTemp_Coil : REAL;
END_VAR

(* === MAIN LOGIC === *)
(* First pass: Handle Emergency Stops and Critical Overrides immediately *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bQuenchIsolateTrigger := TRUE; (* Failsafe state dumps energy out of SCM coils *)
    rCryocoolerPower := 0.0;
    rEDS_CorrectionAmp_Left := 0.0;
    rEDS_CorrectionAmp_Right := 0.0;
    bAlarm := TRUE;
    iState := 999; (* E-Stop active state locking *)
    RETURN;
END_IF;

(* Evaluate the worst-case coil temperature *)
IF rTemp_Coil_Front > rTemp_Coil_Rear THEN
    rMaxTemp_Coil := rTemp_Coil_Front;
ELSE
    rMaxTemp_Coil := rTemp_Coil_Rear;
END_IF;

(* Quench detection filtering - 5 millisecond transient ignore *)
tQuenchDebounce(IN := bQuenchDetect_Raw, PT := T#5MS);

(* If quench is sustained or temperature exceeds absolute critical limits (5.5K) *)
IF tQuenchDebounce.Q OR rMaxTemp_Coil > 5.5 THEN
    bQuenchIsolateTrigger := TRUE; (* Dump current to avoid catastrophic thermal runaway *)
    bAlarm := TRUE;
    iState := 800; (* Jump to quench mitigation sequence *)
END_IF;

(* Main State Machine Execution *)
CASE iState OF
    0: (* IDLE & PRE-CHECK STATE *)
        bSystemReady := FALSE;
        bAlarm := FALSE;
        IF bSystemEnable THEN
            (* Check if cryostat is at nominal operational conditions before initiating EDS *)
            IF rHeLvl_Cryostat > 80.0 AND rMaxTemp_Coil <= 4.2 THEN
                iState := 10; (* Nominal temperature reached, ready for EDS stabilization *)
            ELSE
                iState := 5; (* Switch to active cooling mode to reach setpoints *)
            END_IF;
        END_IF;
        
    5: (* ACTIVE COOLING SEQUENCE *)
        (* Maximize 8-stage pulse tube cryocooler efficiency *)
        rCryocoolerPower := 15.0; (* Max allowable cooling power in kW *)
        tCoolingTimer(IN := TRUE, PT := T#300S); (* Allow up to 5 minutes to reach temp *)
        
        IF rMaxTemp_Coil <= 4.2 AND rHeLvl_Cryostat > 80.0 THEN
            tCoolingTimer(IN := FALSE); (* Reset timer *)
            iState := 10; (* Move to levitation stabilization *)
        ELSIF tCoolingTimer.Q THEN
            (* Failed to reach thermal state within timeout limit *)
            bAlarm := TRUE;
            iState := 900; (* Fault state *)
        END_IF;

    10: (* LEVITATION STABILIZATION (INITIAL ENGAGEMENT) *)
        rCryocoolerPower := 5.0; (* Throttle back to maintenance cooling to reduce vibrations *)
        
        (* Calculate left side dynamics *)
        rGapError_Left := rTargetGap - rLevitationGap_Left;
        rDerivative_Left := rGapError_Left - rPrevGapError_Left;
        rEDS_CorrectionAmp_Left := (rKp_EDS * rGapError_Left) + (rKd_EDS * rDerivative_Left);
        rPrevGapError_Left := rGapError_Left;
        
        (* Calculate right side dynamics *)
        rGapError_Right := rTargetGap - rLevitationGap_Right;
        rDerivative_Right := rGapError_Right - rPrevGapError_Right;
        rEDS_CorrectionAmp_Right := (rKp_EDS * rGapError_Right) + (rKd_EDS * rDerivative_Right);
        rPrevGapError_Right := rGapError_Right;
        
        (* Check if both gaps are within a 0.5mm tolerance band for 1 cycle *)
        IF ABS(rGapError_Left) < 0.5 AND ABS(rGapError_Right) < 0.5 THEN
            bSystemReady := TRUE; (* Flag higher-level system for propulsion start *)
            iState := 20; (* Transition to Steady Levitation mode *)
        END_IF;

    20: (* STEADY HIGH-SPEED LEVITATION TRACKING *)
        (* Continuous closed-loop PID-like regulation for EDS suspension *)
        rGapError_Left := rTargetGap - rLevitationGap_Left;
        rDerivative_Left := rGapError_Left - rPrevGapError_Left;
        rEDS_CorrectionAmp_Left := (rKp_EDS * rGapError_Left) + (rKd_EDS * rDerivative_Left);
        rPrevGapError_Left := rGapError_Left;
        
        rGapError_Right := rTargetGap - rLevitationGap_Right;
        rDerivative_Right := rGapError_Right - rPrevGapError_Right;
        rEDS_CorrectionAmp_Right := (rKp_EDS * rGapError_Right) + (rKd_EDS * rDerivative_Right);
        rPrevGapError_Right := rGapError_Right;
        
        (* Dynamic thermal load compensation for the cryocooler at high velocities *)
        IF rMaxTemp_Coil > 4.4 THEN
            rCryocoolerPower := 10.5; (* Increase power to reject dynamic heat loads *)
        ELSE
            rCryocoolerPower := 5.0; (* Return to steady maintenance baseline *)
        END_IF;
        
        (* Normal shutdown pathway *)
        IF NOT bSystemEnable THEN
            bSystemReady := FALSE;
            iState := 0;
        END_IF;
        
    800: (* QUENCH RECOVERY AND MITIGATION *)
        bSystemReady := FALSE;
        rCryocoolerPower := 18.0; (* Overdrive compressor to purge thermal spike *)
        rEDS_CorrectionAmp_Left := 0.0;
        rEDS_CorrectionAmp_Right := 0.0;
        
        (* Wait for operator to clear fault and temp to normalize under 5.0K safely *)
        IF NOT bQuenchDetect_Raw AND rMaxTemp_Coil < 5.0 AND NOT bSystemEnable THEN
            bQuenchIsolateTrigger := FALSE; (* Safe to close dump switches *)
            bAlarm := FALSE;
            iState := 0;
        END_IF;
        
    900: (* HARDWARE/TIMEOUT ERROR FAULT *)
        bSystemReady := FALSE;
        rCryocoolerPower := 0.0;
        rEDS_CorrectionAmp_Left := 0.0;
        rEDS_CorrectionAmp_Right := 0.0;
        bAlarm := TRUE;
        
        (* Requires reset toggle of bSystemEnable to exit fault *)
        IF NOT bSystemEnable THEN
            iState := 0;
        END_IF;

    999: (* EMERGENCY STOP RECOVERY LATCH *)
        (* Wait here until bEmergencyStop is TRUE again, handled by first rung *)
        IF bSystemEnable THEN
            (* Require operator to disable system before re-enabling *)
            iState := 999; 
        ELSE
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
