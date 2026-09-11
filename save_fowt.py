import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Industrial Scale Offshore Floating Wind Turbine (FOWT) Spar Buoy**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., 15MW active blade pitch dynamic thrust mitigation, multi-line mooring tension differential active ballasting, and nacelle yaw gyroscopic stabilization). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_FloatingWindTurbine\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Industrial Scale Offshore Floating Wind Turbine (FOWT) Spar Buoy

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_FOWT_SparBuoy_Control
VAR_INPUT
    (* Required physical inputs with types and comments *)
    bEnableSystem       : BOOL;     (* Main system enable command for the turbine control *)
    bEmergencyStop      : BOOL;     (* Safety relay OK signal; TRUE = system healthy *)
    rWindSpeed          : REAL;     (* Nacelle anemometer measured wind speed (m/s) *)
    rRotorSpeed         : REAL;     (* Generator rotor shaft speed measurement (RPM) *)
    rSparPitchAngle     : REAL;     (* Spar buoy pitch inclination from inclinometer (degrees) *)
    rSparRollAngle      : REAL;     (* Spar buoy roll inclination from inclinometer (degrees) *)
    rMooringTension_A   : REAL;     (* Measured tension on mooring line A (kN) *)
    rMooringTension_B   : REAL;     (* Measured tension on mooring line B (kN) *)
    rMooringTension_C   : REAL;     (* Measured tension on mooring line C (kN) *)
    rWaveHeight         : REAL;     (* Significant wave height from local wave radar (m) *)
END_VAR
VAR_OUTPUT
    (* Required physical outputs with types and comments *)
    bSystemReady        : BOOL;     (* Overall system operational readiness status flag *)
    bCriticalAlarm      : BOOL;     (* Critical fault requiring immediate turbine shutdown *)
    rPitchAngleCmd_A    : REAL;     (* Individual blade pitch command for Blade A (degrees) *)
    rPitchAngleCmd_B    : REAL;     (* Individual blade pitch command for Blade B (degrees) *)
    rPitchAngleCmd_C    : REAL;     (* Individual blade pitch command for Blade C (degrees) *)
    rActiveBallastPump  : REAL;     (* Active ballast pump flow rate command (m3/hr) *)
    rYawRateCmd         : REAL;     (* Nacelle yaw drive rate command for gyroscopic stab (deg/s) *)
END_VAR
VAR
    (* Internal state variables *)
    iControlState       : INT := 0; (* Internal state machine step tracking *)
    tStartupDelay       : TON;      (* Initialization timer for start sequence *)
    tShutdownDelay      : TON;      (* Timer for controlled shutdown sequence *)
    
    (* Filtered signals and intermediate calculations *)
    rFilteredPitch      : REAL := 0.0; (* Low-pass filtered spar pitch angle *)
    rFilteredRoll       : REAL := 0.0; (* Low-pass filtered spar roll angle *)
    rThrustEstimate     : REAL := 0.0; (* Aerodynamic thrust estimation calculation (kN) *)
    
    rTensionDiffAB      : REAL := 0.0; (* Differential tension between lines A and B *)
    rTensionDiffBC      : REAL := 0.0; (* Differential tension between lines B and C *)
    rTensionDiffCA      : REAL := 0.0; (* Differential tension between lines C and A *)
    
    (* PID controller internal state for active ballast control *)
    rBallastError       : REAL := 0.0;
    rBallastIntegral    : REAL := 0.0;
    rBallastKp          : REAL := 2.5;
    rBallastKi          : REAL := 0.15;
END_VAR

(* === MAIN LOGIC === *)
(* Master Safety Interlock Check *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bCriticalAlarm := TRUE;
    
    (* Feather blades fully for aerodynamic braking *)
    rPitchAngleCmd_A := 90.0; 
    rPitchAngleCmd_B := 90.0;
    rPitchAngleCmd_C := 90.0;
    
    (* Halt all dynamic stabilization systems *)
    rActiveBallastPump := 0.0;
    rYawRateCmd := 0.0;
    
    (* Reset state machine *)
    iControlState := 0;
    RETURN;
END_IF;

(* Continuous Signal Filtering (First-order discrete low-pass filter) *)
rFilteredPitch := (rFilteredPitch * 0.95) + (rSparPitchAngle * 0.05);
rFilteredRoll  := (rFilteredRoll * 0.95) + (rSparRollAngle * 0.05);

(* Continuous Mooring Tension Differential Calculation *)
rTensionDiffAB := rMooringTension_A - rMooringTension_B;
rTensionDiffBC := rMooringTension_B - rMooringTension_C;
rTensionDiffCA := rMooringTension_C - rMooringTension_A;

(* Main Control State Machine *)
CASE iControlState OF
    0: (* IDLE / INITIALIZATION *)
        bSystemReady := FALSE;
        bCriticalAlarm := FALSE;
        
        (* Maintain blades feathered while idle *)
        rPitchAngleCmd_A := 90.0; 
        rPitchAngleCmd_B := 90.0;
        rPitchAngleCmd_C := 90.0;
        
        (* Wait for operator enable and safe environmental conditions *)
        IF bEnableSystem AND (rWindSpeed > 3.0) AND (rWindSpeed < 25.0) AND (rWaveHeight < 8.0) THEN
            iControlState := 10;
        END_IF;

    10: (* STARTUP SEQUENCE *)
        tStartupDelay(IN := TRUE, PT := T#15S);
        IF tStartupDelay.Q THEN
            tStartupDelay(IN := FALSE);
            bSystemReady := TRUE;
            iControlState := 20;
        END_IF;

    20: (* ACTIVE DYNAMIC THRUST & BALLAST MITIGATION RUNNING *)
        
        (* 1. Aerodynamic Thrust Mitigation via Blade Pitch *)
        (* Simple thrust estimation based on rotor swept area and wind speed squared *)
        rThrustEstimate := rWindSpeed * rWindSpeed * 0.5 * 1.225 * 3.14159 * (120.0 * 120.0) / 1000.0; 
        
        IF rThrustEstimate > 1500.0 THEN
            (* Excessive thrust detected: pitch out blades proportionally to shed load *)
            rPitchAngleCmd_A := (rThrustEstimate - 1500.0) * 0.01 + (rFilteredPitch * 0.5);
        ELSE
            (* Below rated thrust: maintain optimal aerodynamic power extraction pitch *)
            rPitchAngleCmd_A := 0.0; 
        END_IF;
        
        (* Implement individual pitch control (IPC) to counteract cyclic wave loading *)
        rPitchAngleCmd_B := rPitchAngleCmd_A + (rFilteredRoll * 0.2);
        rPitchAngleCmd_C := rPitchAngleCmd_A - (rFilteredRoll * 0.2);

        (* 2. Active Ballasting based on mooring tension differential *)
        (* Objective: Minimize tension differential to keep platform balanced *)
        rBallastError := rTensionDiffAB * 1.5; 
        
        (* Update Integrator with anti-windup clamping *)
        rBallastIntegral := rBallastIntegral + (rBallastError * 0.01); 
        IF rBallastIntegral > 100.0 THEN 
            rBallastIntegral := 100.0; 
        END_IF;
        IF rBallastIntegral < -100.0 THEN 
            rBallastIntegral := -100.0; 
        END_IF;
        
        (* Compute PI control action for the ballast pump *)
        rActiveBallastPump := (rBallastError * rBallastKp) + (rBallastIntegral * rBallastKi);
        
        (* 3. Gyroscopic Stabilization via Yaw Drive *)
        (* Utilize nacelle yaw inertia to provide counter-roll damping *)
        rYawRateCmd := rFilteredRoll * (-0.1); 

        (* Extreme conditions and fault check during operation *)
        IF (rFilteredPitch > 12.0) OR (rFilteredRoll > 12.0) OR (rWindSpeed >= 25.0) THEN
            iControlState := 99; (* Transition to fault/storm survival mode *)
        END_IF;

        (* Check for operator disable command *)
        IF NOT bEnableSystem THEN
            iControlState := 0;
        END_IF;
        
    99: (* STORM SURVIVAL / FAULT MODE *)
        bSystemReady := FALSE;
        bCriticalAlarm := TRUE;
        
        (* Lock system into safe survival state *)
        rPitchAngleCmd_A := 90.0; 
        rPitchAngleCmd_B := 90.0;
        rPitchAngleCmd_C := 90.0;
        
        rActiveBallastPump := 0.0;
        rYawRateCmd := 0.0;
        
        (* Operator must cycle the enable signal to acknowledge and reset *)
        IF NOT bEnableSystem THEN
            iControlState := 0;
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

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
