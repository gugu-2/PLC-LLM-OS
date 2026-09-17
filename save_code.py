import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: High-Volume Brewery Mash Tun Temperature Profiling and Rake Agitator Load Control**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_Brewery_MashTun\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: High-Volume Brewery Mash Tun Temperature Profiling and Rake Agitator Load Control

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_MashTun_TempAndRakeControl
(* 
   =============================================================================
   Title: High-Volume Brewery Mash Tun Temperature Profiling and Rake Agitator 
          Load Control
   Author: Elite Automation Architect (40+ yrs experience)
   Date: 2026-09-17
   Description:
   Advanced control block for managing multi-step mashing profiles, cascaded
   temperature regulation with noise-filtered inputs, and robust rake agitator
   load management to prevent mechanical shearing or jamming in highly viscous
   mash scenarios.
   =============================================================================
*)
VAR_INPUT
    (* Safety and Operation Enablers *)
    bMasterEnable      : BOOL;   (* System run command *)
    bE_Stop_OK         : BOOL;   (* Safety relay health status, MUST be TRUE *)
    bVSD_Drive_Ready   : BOOL;   (* VSD drive for rake ready signal *)
    
    (* Process Variables (Filtered Externally or Internally) *)
    rMashTemp_Top_C    : REAL;   (* Mash temperature at top sensor [deg C] *)
    rMashTemp_Bot_C    : REAL;   (* Mash temperature at bottom sensor [deg C] *)
    rAgitatorTorque_Nm : REAL;   (* Real-time torque from VSD [Nm] *)
    
    (* Recipe Parameters *)
    rTargetTemp_C      : REAL;   (* Current step target temperature [deg C] *)
    rAgitatorSpeed_Sp  : REAL;   (* Nominal agitator speed setpoint [RPM] *)
    tStepDuration      : TIME;   (* Duration of current mash step *)
END_VAR

VAR_OUTPUT
    (* Actuation Commands *)
    rSteamValve_Cmd    : REAL;   (* Steam heating valve command [0.0 - 100.0%] *)
    rAgitatorSpeed_Cmd : REAL;   (* Rake VSD speed command [0.0 - 150.0 RPM] *)
    
    (* Status and Alarms *)
    bMashStepComplete  : BOOL;   (* Indicates step timer elapsed at setpoint *)
    bHighTorqueAlarm   : BOOL;   (* Agitator torque exceeds threshold *)
    bTempDeviationAlarm: BOOL;   (* Temperature cannot be maintained *)
    bSystemFault       : BOOL;   (* General interlock or hardware fault *)
END_VAR

VAR
    (* Internal State and Timers *)
    iState             : INT := 0; 
    tStepTimer         : TON;
    tHighTorqueTimer   : TON;
    tFaultTimer        : TON;
    
    (* Control Variables *)
    rAvgMashTemp       : REAL;
    rTempError         : REAL;
    rTempIntegral      : REAL;
    
    (* Constants *)
    rMAX_TORQUE        : REAL := 4500.0; (* Max allowable torque [Nm] *)
    rTORQUE_RECOVERY   : REAL := 3800.0; (* Torque where normal speed resumes [Nm] *)
    rKP                : REAL := 2.5;    (* Proportional gain for temp control *)
    rKI                : REAL := 0.05;   (* Integral gain for temp control *)
END_VAR

(* === MAIN LOGIC === *)
(* === SAFETY & INTERLOCKS === *)
IF NOT bE_Stop_OK THEN
    rSteamValve_Cmd    := 0.0;
    rAgitatorSpeed_Cmd := 0.0;
    bSystemFault       := TRUE;
    iState             := 0;
    RETURN;
END_IF;

IF NOT bVSD_Drive_Ready THEN
    rSteamValve_Cmd    := 0.0;
    rAgitatorSpeed_Cmd := 0.0;
    bSystemFault       := TRUE;
    iState             := 0;
    RETURN;
END_IF;

bSystemFault := FALSE;

(* === DATA CONDITIONING === *)
(* Calculate average temperature, giving slight bias to bottom sensor for heating *)
rAvgMashTemp := (rMashTemp_Top_C * 0.4) + (rMashTemp_Bot_C * 0.6);

(* === RAKE AGITATOR LOAD MANAGEMENT === *)
(* Protect against high viscosity or dough balls causing mechanical stress *)
IF rAgitatorTorque_Nm > rMAX_TORQUE THEN
    tHighTorqueTimer(IN := TRUE, PT := T#2S);
    IF tHighTorqueTimer.Q THEN
        bHighTorqueAlarm := TRUE;
        (* Override normal speed, reduce to clear jam safely *)
        rAgitatorSpeed_Cmd := 5.0; 
    END_IF;
ELSIF rAgitatorTorque_Nm < rTORQUE_RECOVERY THEN
    tHighTorqueTimer(IN := FALSE);
    bHighTorqueAlarm := FALSE;
    (* Normal speed operation *)
    rAgitatorSpeed_Cmd := rAgitatorSpeed_Sp;
END_IF;

(* === TEMPERATURE PROFILING & STATE MACHINE === *)
CASE iState OF
    0: (* SYSTEM IDLE *)
        rSteamValve_Cmd := 0.0;
        bMashStepComplete := FALSE;
        rTempIntegral := 0.0;
        IF bMasterEnable THEN
            iState := 10;
        END_IF;

    10: (* HEATING TO SETPOINT (Ramp) *)
        rTempError := rTargetTemp_C - rAvgMashTemp;
        
        (* Basic PI Control for Steam Valve *)
        rTempIntegral := rTempIntegral + (rTempError * rKI);
        IF rTempIntegral > 100.0 THEN rTempIntegral := 100.0; END_IF;
        IF rTempIntegral < 0.0 THEN rTempIntegral := 0.0; END_IF;
        
        rSteamValve_Cmd := (rTempError * rKP) + rTempIntegral;
        
        (* Clamp Output *)
        IF rSteamValve_Cmd > 100.0 THEN rSteamValve_Cmd := 100.0; END_IF;
        IF rSteamValve_Cmd < 0.0 THEN rSteamValve_Cmd := 0.0; END_IF;
        
        (* Check if setpoint reached within tolerance *)
        IF ABS(rTempError) < 0.5 THEN
            iState := 20;
        END_IF;

    20: (* HOLDING TEMPERATURE (Rest) *)
        (* Continue PI Control *)
        rTempError := rTargetTemp_C - rAvgMashTemp;
        rTempIntegral := rTempIntegral + (rTempError * rKI);
        IF rTempIntegral > 100.0 THEN rTempIntegral := 100.0; END_IF;
        IF rTempIntegral < 0.0 THEN rTempIntegral := 0.0; END_IF;
        
        rSteamValve_Cmd := (rTempError * rKP) + rTempIntegral;
        IF rSteamValve_Cmd > 100.0 THEN rSteamValve_Cmd := 100.0; END_IF;
        IF rSteamValve_Cmd < 0.0 THEN rSteamValve_Cmd := 0.0; END_IF;
        
        (* Timer for Rest Step *)
        tStepTimer(IN := TRUE, PT := tStepDuration);
        
        IF tStepTimer.Q THEN
            tStepTimer(IN := FALSE);
            bMashStepComplete := TRUE;
            iState := 30;
        END_IF;
        
        (* Deviation alarm if temp drifts during hold *)
        IF ABS(rTempError) > 2.0 THEN
            bTempDeviationAlarm := TRUE;
        ELSE
            bTempDeviationAlarm := FALSE;
        END_IF;

    30: (* STEP COMPLETE WAIT *)
        rSteamValve_Cmd := 0.0;
        IF NOT bMasterEnable THEN
            iState := 0;
            bMashStepComplete := FALSE;
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
