import os, json, uuid

os.makedirs('data/swarm_raw', exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Next-Gen Heavy-Duty Electric Mining Haul Truck Pantograph Substation**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., 3kV DC catenary on-the-fly robotic arm engagement, active arc flash quench filtering, and regenerative downhill dynamic braking chopper modulation). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_MiningTruckPantograph\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Next-Gen Heavy-Duty Electric Mining Haul Truck Pantograph Substation

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_MiningTruckPantographSubstation
VAR_INPUT
    (* System & Safety Constraints *)
    bEnable             : BOOL;     (* System enable signal *)
    bEmergencyStop      : BOOL;     (* Safety relay OK signal, normally high *)
    bLineVoltageOK      : BOOL;     (* Catenary 3kV DC verification relay *)
    
    (* Vehicle Dynamics & Sensors *)
    rTruckVelocityKmh   : REAL;     (* Truck velocity in km/h *)
    rDownhillGrade      : REAL;     (* Road gradient % (positive = downhill) *)
    rPantographForceN   : REAL;     (* Contact force on the pantograph head in Newtons *)
    
    (* Vision & Positioning *)
    bGpsAlignmentOK     : BOOL;     (* Ultra-Wideband & RTK-GPS catenary alignment confirm *)
    bArcFlashDetected   : BOOL;     (* Optical arc flash sensor input *)
END_VAR
VAR_OUTPUT
    (* System Status *)
    bSystemReady        : BOOL;     (* System ready status for main VFD drives *)
    bAlarm              : BOOL;     (* Fault alarm output *)
    
    (* Pantograph Actuation *)
    bPantographDeploy   : BOOL;     (* Command to raise pantograph to catenary *)
    bArcQuenchActive    : BOOL;     (* Active arc flash quench filter relay engagement *)
    
    (* Power Modulation *)
    rChopperDutyCycle   : REAL;     (* Regenerative braking chopper modulation 0.0-100.0% *)
    rTargetContactForce : REAL;     (* Dynamic target upward contact force setpoint *)
END_VAR
VAR
    (* Internal State & Timers *)
    iState              : INT := 0;
    tDeployTimer        : TON;
    tArcQuenchTimer     : TON;
    tAlignDebounce      : TON;
    
    (* Filtering & Math *)
    rFilteredForce      : REAL := 0.0;
    rForceError         : REAL := 0.0;
    
    (* Constants *)
    MAX_SPEED_KMH       : REAL := 60.0;
    MIN_SPEED_KMH       : REAL := 5.0;
    NOMINAL_FORCE_N     : REAL := 150.0;
END_VAR

(* === MAIN LOGIC === *)

(* 1. Safety Interlock Evaluation *)
IF NOT bEmergencyStop OR NOT bLineVoltageOK THEN
    bSystemReady := FALSE;
    bPantographDeploy := FALSE;
    rChopperDutyCycle := 0.0;
    bArcQuenchActive := FALSE;
    bAlarm := TRUE;
    iState := 99; (* Force fault state *)
    RETURN;
END_IF;

(* 2. Contact Force Low-Pass Filter (First Order) *)
(* Mathematically rigorous filtering of pantograph contact pressure *)
rFilteredForce := rFilteredForce + 0.25 * (rPantographForceN - rFilteredForce);

(* 3. Complex State Machine Execution *)
CASE iState OF
    0: (* IDLE & SAFETY CHECK *)
        bSystemReady := FALSE;
        bAlarm := FALSE;
        bPantographDeploy := FALSE;
        rChopperDutyCycle := 0.0;
        
        IF bEnable AND bEmergencyStop THEN
            iState := 10;
        END_IF;
        
    10: (* ALIGNMENT & SPEED VALIDATION *)
        tAlignDebounce(IN := bGpsAlignmentOK, PT := T#2S);
        
        IF tAlignDebounce.Q AND (rTruckVelocityKmh > MIN_SPEED_KMH) AND (rTruckVelocityKmh < MAX_SPEED_KMH) THEN
            iState := 20; (* Proceed to dynamic deployment *)
        ELSIF NOT bEnable THEN
            iState := 0;
        END_IF;
        
    20: (* PANTOGRAPH ENGAGEMENT (ON-THE-FLY) *)
        bPantographDeploy := TRUE;
        tDeployTimer(IN := TRUE, PT := T#5S);
        
        (* Calculate dynamic target upward force based on aerodynamics (speed factor) *)
        rTargetContactForce := NOMINAL_FORCE_N + (rTruckVelocityKmh * 0.45);
        
        IF tDeployTimer.Q AND (rFilteredForce > (NOMINAL_FORCE_N * 0.8)) THEN
            tDeployTimer(IN := FALSE);
            bSystemReady := TRUE;
            iState := 30;
        ELSIF tDeployTimer.Q AND (rFilteredForce <= (NOMINAL_FORCE_N * 0.8)) THEN
            (* Failed to engage catenary wire within threshold time *)
            bAlarm := TRUE;
            iState := 99; 
        END_IF;
        
    30: (* ACTIVE TROLLEY MODE & DYNAMIC REGEN BRAKING CHOPPER MODULATION *)
        rForceError := rTargetContactForce - rFilteredForce;
        
        (* Regenerative braking chopper modulation based on downhill grade and kinetic energy *)
        IF rDownhillGrade > 2.0 THEN
            (* Aggressive chopper modulation for heavy downhill regen (0 to 100%) *)
            rChopperDutyCycle := LIMIT(0.0, (rDownhillGrade - 2.0) * 12.5, 100.0);
        ELSE
            rChopperDutyCycle := 0.0;
        END_IF;
        
        (* Active Arc flash detection during active transit & heavy regen *)
        IF bArcFlashDetected OR (rFilteredForce < 20.0 AND rChopperDutyCycle > 15.0) THEN
            iState := 40;
        END_IF;
        
        IF NOT bEnable OR NOT bGpsAlignmentOK THEN
            iState := 0; (* Detach from Catenary *)
        END_IF;
        
    40: (* ACTIVE ARC FLASH QUENCHING FILTERING *)
        bArcQuenchActive := TRUE;
        rChopperDutyCycle := 0.0; (* Instantly cut regen current to quench arc *)
        
        tArcQuenchTimer(IN := TRUE, PT := T#500MS);
        
        IF tArcQuenchTimer.Q THEN
            tArcQuenchTimer(IN := FALSE);
            bArcQuenchActive := FALSE;
            IF rFilteredForce > (NOMINAL_FORCE_N * 0.6) THEN
                iState := 30; (* Arc successfully quenched, physical contact re-established *)
            ELSE
                iState := 0; (* Lost contact entirely, retract safely *)
            END_IF;
        END_IF;
        
    99: (* FAULT HANDLING & LOCKOUT *)
        bPantographDeploy := FALSE;
        rChopperDutyCycle := 0.0;
        bArcQuenchActive := FALSE;
        bSystemReady := FALSE;
        
        IF NOT bEmergencyStop THEN
            (* Wait for E-Stop clear or system disable cycle to reset fault *)
            IF NOT bEnable THEN
                iState := 0;
            END_IF;
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

filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
