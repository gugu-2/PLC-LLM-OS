import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Commercial High-Rise Elevator Group Dispatching and Regenerative Braking**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_Elevator_GroupControl\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Commercial High-Rise Elevator Group Dispatching and Regenerative Braking

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_ElevatorDispatchAndRegen
VAR_INPUT
    (* System Inputs *)
    bSystemEnable         : BOOL;      (* Main system enable signal *)
    bEmergencyStop        : BOOL;      (* Safety relay OK signal, normally closed (TRUE=OK) *)
    rCarSpeed_m_s         : REAL;      (* Current physical speed of the elevator car in m/s *)
    rCarLoad_kg           : REAL;      (* Current load in the elevator car in kg *)
    rDCBusVoltage_V       : REAL;      (* DC Bus voltage for regenerative braking system in Volts *)
    iCurrentFloor         : INT;       (* Current physical floor location *)
    iTargetFloor          : INT;       (* Desired floor from the dispatching algorithm *)
    bHoistwayClear        : BOOL;      (* Safety interlock from hoistway sensors *)
END_VAR
VAR_OUTPUT
    (* System Outputs *)
    bDriveEnable          : BOOL;      (* Enable signal to the main traction drive *)
    rMotorTorqueCmd       : REAL;      (* Torque command to the traction motor in Nm *)
    bRegenActive          : BOOL;      (* Regenerative braking contactor enable *)
    bSafetyBrakeDeploy    : BOOL;      (* Mechanical safety brake deployment (TRUE = Drop brakes) *)
    bDoorOpenEnable       : BOOL;      (* Enable door operator to open doors *)
    iDispatchState        : INT;       (* Current operating state for SCADA monitoring *)
END_VAR
VAR
    (* Internal State and Timers *)
    iState                : INT := 0;  (* 0=IDLE, 10=ACCEL, 20=CRUISE, 30=DECEL, 40=LEVELING, 50=REGEN, 99=FAULT *)
    tRegenDelay           : TON;       (* Timer for engaging regen contactor safely *)
    tLevelingTimer        : TON;       (* Timer to ensure accurate floor leveling *)
    rSpeedError           : REAL;      (* Error between target speed and current speed *)
    rTargetSpeed          : REAL;      (* Calculated motion profile target speed *)
    rIntegralAccum        : REAL := 0.0;
    
    (* Constants *)
    MAX_SPEED             : REAL := 8.0;   (* 8 m/s for high-rise commercial *)
    MAX_DC_VOLTAGE        : REAL := 750.0; (* 750V DC Bus Limit *)
    OVERSPEED_LIMIT       : REAL := 8.5;
    NOMINAL_LOAD          : REAL := 1500.0;(* 1500 kg max capacity *)
    
    (* Noise Filtering *)
    rSpeedFiltered        : REAL := 0.0;
    ALPHA_FILTER          : REAL := 0.2;   (* Low-pass filter coefficient *)
END_VAR

(* === SAFETY INTERLOCKS AND FAULT HANDLING === *)
IF NOT bEmergencyStop OR NOT bHoistwayClear THEN
    bDriveEnable := FALSE;
    rMotorTorqueCmd := 0.0;
    bRegenActive := FALSE;
    bSafetyBrakeDeploy := TRUE; (* Deploy mechanical brakes instantly *)
    bDoorOpenEnable := FALSE;
    iState := 99; (* FAULT STATE *)
    iDispatchState := iState;
    RETURN;
END_IF;

(* Speed Sensor Noise Filtering (Low-Pass Filter) *)
rSpeedFiltered := (ALPHA_FILTER * rCarSpeed_m_s) + ((1.0 - ALPHA_FILTER) * rSpeedFiltered);

(* Overspeed Protection - Redundant Logic *)
IF rSpeedFiltered > OVERSPEED_LIMIT THEN
    bDriveEnable := FALSE;
    bSafetyBrakeDeploy := TRUE;
    bRegenActive := FALSE;
    iState := 99;
    iDispatchState := iState;
    RETURN;
ELSE
    bSafetyBrakeDeploy := FALSE;
END_IF;

(* === STATE MACHINE FOR ELEVATOR DISPATCHING & MOTION === *)
CASE iState OF
    0: (* IDLE - Wait at floor *)
        bDriveEnable := FALSE;
        rMotorTorqueCmd := 0.0;
        bRegenActive := FALSE;
        bDoorOpenEnable := TRUE;
        
        IF bSystemEnable AND (iCurrentFloor <> iTargetFloor) THEN
            bDoorOpenEnable := FALSE;
            iState := 10;
        END_IF;

    10: (* ACCEL - Accelerate towards target *)
        bDriveEnable := TRUE;
        rTargetSpeed := MAX_SPEED * 0.5; (* Simplified ramp up *)
        
        (* PID Logic for Torque Command *)
        rSpeedError := rTargetSpeed - rSpeedFiltered;
        rIntegralAccum := rIntegralAccum + (rSpeedError * 0.01);
        rMotorTorqueCmd := (rSpeedError * 50.0) + (rIntegralAccum * 5.0);
        
        IF rSpeedFiltered >= (MAX_SPEED * 0.45) THEN
            iState := 20;
        END_IF;

    20: (* CRUISE - Constant speed *)
        bDriveEnable := TRUE;
        rTargetSpeed := MAX_SPEED;
        
        rSpeedError := rTargetSpeed - rSpeedFiltered;
        rMotorTorqueCmd := (rSpeedError * 40.0) + (rIntegralAccum * 5.0);
        
        (* Evaluate distance to target for deceleration *)
        IF ABS(iTargetFloor - iCurrentFloor) <= 2 THEN
            iState := 30;
        END_IF;

    30: (* DECEL & REGENERATIVE BRAKING DECISION *)
        bDriveEnable := TRUE;
        rTargetSpeed := 1.0; (* Decelerate to leveling speed *)
        
        (* Regenerative Braking Logic: 
           If decel is required AND we have heavy load going down OR light load going up,
           the motor acts as a generator. Engage REGEN if DC Bus is healthy. *)
        IF rDCBusVoltage_V < MAX_DC_VOLTAGE THEN
            tRegenDelay(IN := TRUE, PT := T#100MS);
            IF tRegenDelay.Q THEN
                bRegenActive := TRUE;
                iState := 50; (* Transition to Regen-Assist Decel *)
            END_IF;
        ELSE
            bRegenActive := FALSE;
            (* Dissipate via dynamic braking resistors instead (not mapped to IO here) *)
        END_IF;
        
        rSpeedError := rTargetSpeed - rSpeedFiltered;
        rMotorTorqueCmd := (rSpeedError * 60.0);
        
        IF rSpeedFiltered <= 1.2 THEN
            tRegenDelay(IN := FALSE);
            bRegenActive := FALSE;
            iState := 40;
        END_IF;
        
    40: (* LEVELING - Final approach to floor *)
        bDriveEnable := TRUE;
        rTargetSpeed := 0.1;
        rMotorTorqueCmd := (rTargetSpeed - rSpeedFiltered) * 80.0;
        
        tLevelingTimer(IN := TRUE, PT := T#2S);
        IF iCurrentFloor = iTargetFloor AND tLevelingTimer.Q THEN
            tLevelingTimer(IN := FALSE);
            iState := 0;
        END_IF;

    50: (* REGEN - Regenerative braking state *)
        bDriveEnable := TRUE;
        bRegenActive := TRUE;
        rTargetSpeed := 1.0;
        
        (* Negative torque command to extract energy *)
        rMotorTorqueCmd := -150.0; 
        
        (* Monitor DC Bus - trip out if overvoltage *)
        IF rDCBusVoltage_V >= MAX_DC_VOLTAGE THEN
            bRegenActive := FALSE;
            iState := 30; (* Revert to standard decel *)
        END_IF;
        
        IF rSpeedFiltered <= 1.2 THEN
            bRegenActive := FALSE;
            iState := 40; (* Go to leveling *)
        END_IF;

    99: (* FAULT RECOVERY WAIT *)
        bDriveEnable := FALSE;
        rMotorTorqueCmd := 0.0;
        bRegenActive := FALSE;
        IF bSystemEnable AND bEmergencyStop AND bHoistwayClear AND (rSpeedFiltered = 0.0) THEN
            iState := 0; (* Reset to IDLE if safe *)
        END_IF;
        
END_CASE;

iDispatchState := iState;

END_FUNCTION_BLOCK
```"""

os.makedirs('data/swarm_raw', exist_ok=True)
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
