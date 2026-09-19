import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Automated Warehouse High-Density Automated Storage and Retrieval System (ASRS) Shuttle Anti-Collision**

Task: Invent a highly complex, ultra-realistic control scenario for this domain. Make this code EVEN BETTER, MORE ADVANCED, and MORE RIGOROUS than previous iterations. Include extreme edge-case handling, advanced math, and robust fault-tolerance.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_ASRS_ShuttleCollision\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Automated Warehouse High-Density Automated Storage and Retrieval System (ASRS) Shuttle Anti-Collision

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_ASRS_ShuttleCollision_Advanced
VAR_INPUT
    bEnable                 : BOOL;     (* System enable signal *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal - MUST be TRUE for operation *)
    rShuttleVelocity        : REAL;     (* Current velocity of the shuttle in m/s *)
    rDistanceToObstacle     : REAL;     (* Laser rangefinder distance to nearest obstacle in front in meters *)
    rDistanceToTrailing     : REAL;     (* Laser rangefinder distance to trailing shuttle behind in meters *)
    rPayloadMass            : REAL;     (* Current mass of the payload on the shuttle in kg *)
    bLaserSensorOk          : BOOL;     (* Laser rangefinder health status *)
    bCommLinkOk             : BOOL;     (* V2V (Vehicle-to-Vehicle) communication link status *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;     (* System ready status *)
    rSpeedLimit             : REAL;     (* Safe speed limit to send to drive control in m/s *)
    bEmergencyBrake         : BOOL;     (* Immediate emergency braking request *)
    bWarningAlarm           : BOOL;     (* Collision warning alarm output *)
    iFaultCode              : INT;      (* Diagnostics fault code (0=OK) *)
END_VAR
VAR
    iState                  : INT := 0; (* State machine state *)
    tSensorTimeout          : TON;      (* Timeout for sensor failure *)
    rSafeStoppingDistance   : REAL;     (* Calculated safe stopping distance in m *)
    rKineticEnergy          : REAL;     (* Current kinetic energy calculation *)
    rDecelerationRate       : REAL := 2.5; (* Configured emergency deceleration rate in m/s^2 *)
    rReactionTime           : REAL := 0.2; (* System reaction time in seconds *)
    rSafetyMargin           : REAL := 1.5; (* Safety margin distance in meters *)
END_VAR

(* === MAIN LOGIC === *)
(* 1. Safety & Interlock Checks *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bEmergencyBrake := TRUE;
    rSpeedLimit := 0.0;
    bWarningAlarm := TRUE;
    iFaultCode := 999; (* Critical E-Stop *)
    iState := 0;
    RETURN;
END_IF;

IF NOT bLaserSensorOk OR NOT bCommLinkOk THEN
    (* Sensor or Comm failure - trigger timer to allow transient dropouts, else fault *)
    tSensorTimeout(IN := TRUE, PT := T#500MS);
    IF tSensorTimeout.Q THEN
        bSystemReady := FALSE;
        bEmergencyBrake := TRUE;
        rSpeedLimit := 0.0;
        bWarningAlarm := TRUE;
        iFaultCode := 101; (* Sensor or Comm failure *)
        iState := 0;
        RETURN;
    END_IF;
ELSE
    tSensorTimeout(IN := FALSE);
END_IF;

(* 2. Physics & Safety Calculations *)
(* Kinematic equation: v^2 = u^2 + 2as -> s = v^2 / (2a) *)
(* Add reaction time distance: s_reaction = v * t *)
rSafeStoppingDistance := (rShuttleVelocity * rShuttleVelocity) / (2.0 * rDecelerationRate) + 
                         (rShuttleVelocity * rReactionTime) + 
                         rSafetyMargin;

(* Adjust deceleration requirements based on Payload Mass to ensure brakes can handle it *)
rKineticEnergy := 0.5 * rPayloadMass * (rShuttleVelocity * rShuttleVelocity);
IF rKineticEnergy > 50000.0 THEN
    (* Extremely heavy or fast - increase safety margin dynamically *)
    rSafeStoppingDistance := rSafeStoppingDistance * 1.25;
END_IF;

(* 3. State Machine for Anti-Collision Control *)
CASE iState OF
    0: (* IDLE / FAULT RECOVERY *)
        bSystemReady := FALSE;
        rSpeedLimit := 0.0;
        bEmergencyBrake := TRUE;
        IF bEnable AND bEmergencyStop AND bLaserSensorOk AND bCommLinkOk THEN
            iFaultCode := 0;
            bEmergencyBrake := FALSE;
            bWarningAlarm := FALSE;
            iState := 10; (* Transition to RUNNING *)
        END_IF;

    10: (* RUNNING - NORMAL OPERATION *)
        bSystemReady := TRUE;
        
        (* Evaluate Forward Collision Risk *)
        IF rDistanceToObstacle <= rSafeStoppingDistance THEN
            iState := 20; (* Collision imminent - engage braking *)
        ELSIF rDistanceToObstacle <= (rSafeStoppingDistance * 1.5) THEN
            (* Warning zone - reduce speed proportionally *)
            bWarningAlarm := TRUE;
            rSpeedLimit := rShuttleVelocity * 0.5;
        ELSE
            (* Safe operation *)
            bWarningAlarm := FALSE;
            rSpeedLimit := 5.0; (* Max nominal speed *)
        END_IF;
        
        (* Evaluate Trailing Collision Risk (if another shuttle is too close behind) *)
        IF rDistanceToTrailing < rSafetyMargin THEN
            (* Cannot brake suddenly if someone is right behind us, unless we have to *)
            (* This is an advanced swarm logic scenario. For now, issue warning *)
            bWarningAlarm := TRUE;
        END_IF;

    20: (* EMERGENCY BRAKING *)
        bSystemReady := FALSE;
        bEmergencyBrake := TRUE;
        rSpeedLimit := 0.0;
        bWarningAlarm := TRUE;
        iFaultCode := 50; (* Collision avoidance engaged *)
        
        (* Stay in braking state until vehicle completely stops and obstacle clears *)
        IF (rShuttleVelocity <= 0.01) AND (rDistanceToObstacle > rSafeStoppingDistance) THEN
            IF NOT bEnable THEN
                iState := 0; (* Require toggle of enable to reset *)
            END_IF;
        END_IF;

    ELSE
        (* Invalid state trap *)
        iState := 0;
        
END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs('data/swarm_raw', exist_ok=True)
record = {'messages': [{'role': 'user', 'content': prompt}, {'role': 'assistant', 'content': code}]}
filename = f'data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json'
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(record, f, ensure_ascii=False)
print(f'Saved to {filename}')
