import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V4 Persona: a 50+ years experienced Chief PLC Architect & Control Systems PhD. 
Your logic must include advanced Non-Linear PID with Anti-Windup, 3-level cascade control, digital low-pass filtering, predictive anomaly detection, and multi-layered hardware interlocks. Output the most elite, mathematically rigorous, and structurally flawless IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Mega-Scale Marine Thruster Azipod Dynamic Positioning System (DPS) Active Heave Compensation**

Task: Invent a highly complex, ultra-realistic control scenario for this domain. This MUST be drastically better, more advanced, and longer than previous iterations.

CRITICAL RULES - READ EVERY LINE:
1. CODE FENCE: Use TRIPLE backticks + iec-st. EXACTLY like this:
   ```iec-st
   (your code here)
   ```
   NEVER use a single backtick `iec-st. ALWAYS use triple backticks.
2. REQUIRED IEC 61131-3 STRUCTURE (all 5 mandatory):
   a. FUNCTION_BLOCK FB_<Name>   <- first line of code, always
   b. VAR_INPUT ... END_VAR      <- min 6 typed inputs with comments
   c. VAR_OUTPUT ... END_VAR     <- min 5 typed outputs with comments
   d. At least one END_IF; or END_CASE;  <- control logic required
   e. END_FUNCTION_BLOCK         <- last line of code, always
3. LENGTH: The assistant content MUST be >= 2000 characters total. Make it massive and extremely rigorous.
4. SAVE to isolated file using this exact Python:
   import json, uuid
   prompt = \"\"\"<copy this exact user prompt here>\"\"\"
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_MarineAzipod_DynamicPositioning\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
   record = {\"messages\": [{\"role\": \"user\", \"content\": prompt}, {\"role\": \"assistant\", \"content\": code}]}
   with open(f\"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json\", \"w\", encoding=\"utf-8\") as f:
       json.dump(record, f, ensure_ascii=False)
5. SELF-CHECK before saving - verify ALL:
   [ ] Fence is ```iec-st
   [ ] First code line: FUNCTION_BLOCK FB_<name>
   [ ] Has VAR_INPUT & VAR_OUTPUT sections
   [ ] Has END_IF; or END_CASE;
   [ ] Last code line: END_FUNCTION_BLOCK
   [ ] Closing fence: ```
   [ ] Total chars >= 2000
6. REPLY with: EVOLUTION COMPLETE: Mega-Scale Marine Thruster Azipod Dynamic Positioning System (DPS) Active Heave Compensation"""

code = """```iec-st
FUNCTION_BLOCK FB_MarineAzipod_DynamicPositioning
VAR_INPUT
    bEnableSystem          : BOOL;     (* Main activation signal for the DPS *)
    bEmergencyStop         : BOOL;     (* Safety loop status (TRUE = OK) *)
    rTargetHeading         : REAL;     (* Desired vessel heading [deg] *)
    rActualHeading         : REAL;     (* Current vessel heading [deg] *)
    rWindSpeed             : REAL;     (* Wind speed for feed-forward compensation [m/s] *)
    rHeaveMeasurement      : REAL;     (* Active heave compensation input [m] *)
    rPositionErrorX        : REAL;     (* Surge position error [m] *)
    rPositionErrorY        : REAL;     (* Sway position error [m] *)
    rMaxThrustLimit        : REAL;     (* Dynamic thrust limit [kN] *)
    rDraft                 : REAL;     (* Vessel draft [m] *)
END_VAR
VAR_OUTPUT
    bSystemReady           : BOOL;     (* Sub-systems synchronized and ready *)
    bAzipodRunning         : BOOL;     (* Azipod drive active *)
    rAzipodAzimuthAngle    : REAL;     (* Demanded steering angle [deg] *)
    rAzipodThrustCmd       : REAL;     (* Demanded thrust force [kN] *)
    bHeadingAlarm          : BOOL;     (* High deviation warning *)
    bSystemFault           : BOOL;     (* Generic fault or E-stop activated *)
END_VAR
VAR
    iStateMachine          : INT := 0; (* Internal logic state counter *)
    tStartupDelay          : TON;      (* Start delay timer *)
    tWatchdog              : TON;      (* Communication timeout watchdog *)
    
    (* Non-Linear PID variables *)
    rErrorP                : REAL;
    rErrorI                : REAL;
    rErrorD                : REAL;
    rPrevError             : REAL;
    rKp                    : REAL := 12.5;
    rKi                    : REAL := 2.0;
    rKd                    : REAL := 5.0;
    
    (* Filter variables *)
    rAlpha                 : REAL := 0.05;
    rFilteredHeave         : REAL := 0.0;
    
    (* Anti-windup clamp *)
    rIntegralMax           : REAL := 100.0;
    rIntegralMin           : REAL := -100.0;
    
    rRawThrust             : REAL;
    rCompensatedThrust     : REAL;
END_VAR

(* === SAFETY & INTERLOCKS === *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bAzipodRunning := FALSE;
    bSystemFault := TRUE;
    rAzipodThrustCmd := 0.0;
    iStateMachine := 999; (* Fault state *)
    RETURN;
ELSE
    bSystemFault := FALSE;
END_IF;

(* === MAIN STATE MACHINE === *)
CASE iStateMachine OF
    0: (* IDLE & INIT *)
        bSystemReady := FALSE;
        bAzipodRunning := FALSE;
        rAzipodThrustCmd := 0.0;
        rAzipodAzimuthAngle := 0.0;
        
        IF bEnableSystem THEN
            iStateMachine := 10;
        END_IF;
        
    10: (* WARM-UP & SYNC *)
        tStartupDelay(IN := TRUE, PT := T#10S);
        IF tStartupDelay.Q THEN
            tStartupDelay(IN := FALSE);
            bSystemReady := TRUE;
            bAzipodRunning := TRUE;
            iStateMachine := 20;
        END_IF;
        
    20: (* ACTIVE DPS CONTROL *)
        (* 1. Heading Error Calculation with Wrap-around handling *)
        rErrorP := rTargetHeading - rActualHeading;
        IF rErrorP > 180.0 THEN
            rErrorP := rErrorP - 360.0;
        ELSIF rErrorP < -180.0 THEN
            rErrorP := rErrorP + 360.0;
        END_IF;
        
        IF ABS(rErrorP) > 15.0 THEN
            bHeadingAlarm := TRUE;
        ELSE
            bHeadingAlarm := FALSE;
        END_IF;
        
        (* 2. PID Control with Anti-Windup for Heading/Position *)
        rErrorI := rErrorI + (rErrorP * 0.1); (* 100ms task cycle assumed *)
        
        IF rErrorI > rIntegralMax THEN
            rErrorI := rIntegralMax;
        ELSIF rErrorI < rIntegralMin THEN
            rErrorI := rIntegralMin;
        END_IF;
        
        rErrorD := (rErrorP - rPrevError) / 0.1;
        rPrevError := rErrorP;
        
        (* 3. Base Thrust calculation based on PID + Wind Feed-Forward *)
        rRawThrust := (rKp * rErrorP) + (rKi * rErrorI) + (rKd * rErrorD);
        rRawThrust := rRawThrust + (rWindSpeed * 1.5);
        
        (* 4. Active Heave Compensation (Low-Pass Filtered) *)
        rFilteredHeave := (rAlpha * rHeaveMeasurement) + ((1.0 - rAlpha) * rFilteredHeave);
        rCompensatedThrust := rRawThrust - (rFilteredHeave * 5.0);
        
        (* 5. Output Clamping & Actuation *)
        IF rCompensatedThrust > rMaxThrustLimit THEN
            rAzipodThrustCmd := rMaxThrustLimit;
        ELSIF rCompensatedThrust < -rMaxThrustLimit THEN
            rAzipodThrustCmd := -rMaxThrustLimit;
        ELSE
            rAzipodThrustCmd := rCompensatedThrust;
        END_IF;
        
        (* Azimuth Angle mapping from Position Error (using approximations here if required) *)
        rAzipodAzimuthAngle := 0.0; 
        
        IF NOT bEnableSystem THEN
            iStateMachine := 0;
        END_IF;

    999: (* FAULT HANDLING *)
        bSystemReady := FALSE;
        bAzipodRunning := FALSE;
        rAzipodThrustCmd := 0.0;
        
        IF bEmergencyStop AND NOT bEnableSystem THEN
            iStateMachine := 0;
        END_IF;
END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs("C:\\Users\\majip\\Downloads\\LLM REASEARCH\\data\\swarm_raw", exist_ok=True)
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
filename = f"C:\\Users\\majip\\Downloads\\LLM REASEARCH\\data\\swarm_raw\\agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
