import json, uuid, os
prompt = """<USER_REQUEST>
You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V4 Persona: a 50+ years experienced Chief PLC Architect & Control Systems PhD. 
Your logic must include advanced Non-Linear PID with Anti-Windup, 3-level cascade control, digital low-pass filtering, predictive anomaly detection, and multi-layered hardware interlocks. Output the most elite, mathematically rigorous, and structurally flawless IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Automated Mega-Scale Vertical Lift Module (VLM) Warehouse Robotics Laser Positioning and Payload Balancing**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_VLM_WarehouseRobotics\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
   record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
   with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
       json.dump(record, f, ensure_ascii=False)
5. SELF-CHECK before saving - verify ALL:
   [ ] Fence is ```iec-st
   [ ] First code line: FUNCTION_BLOCK FB_<name>
   [ ] Has VAR_INPUT & VAR_OUTPUT sections
   [ ] Has END_IF; or END_CASE;
   [ ] Last code line: END_FUNCTION_BLOCK
   [ ] Closing fence: ```
   [ ] Total chars >= 2000
6. REPLY with: EVOLUTION COMPLETE: Automated Mega-Scale Vertical Lift Module (VLM) Warehouse Robotics Laser Positioning and Payload Balancing
</USER_REQUEST>"""

code = """```iec-st
FUNCTION_BLOCK FB_VLM_WarehouseRobotics_LaserPos_PayloadBalancing

VAR_INPUT
    bEnableMaster            : BOOL;     (* System master enable interlock *)
    bEmergencyStop           : BOOL;     (* Safety relay OK signal (Dual Channel) *)
    bMaintenanceMode         : BOOL;     (* Maintenance override active *)
    rLaserPositionZ_mm       : REAL;     (* High-res laser positioning Z-axis feedback [mm] *)
    rLaserPositionX_mm       : REAL;     (* High-res laser positioning X-axis feedback [mm] *)
    rPayloadMass_kg          : REAL;     (* Detected tray payload mass via load cells [kg] *)
    rTrayCenterOfGravityX_mm : REAL;     (* Calculated CoG on X-axis [mm] *)
    rTrayCenterOfGravityY_mm : REAL;     (* Calculated CoG on Y-axis [mm] *)
    rVelocityZ_mm_s          : REAL;     (* Actual velocity Z-axis [mm/s] *)
    rTargetPositionZ_mm      : REAL;     (* Target destination height [mm] *)
END_VAR

VAR_OUTPUT
    bSystemReady             : BOOL;     (* VLM robotics ready for motion *)
    rControlOutputZ_V        : REAL;     (* Servo velocity command Z-axis [-10..+10V] *)
    rControlOutputX_V        : REAL;     (* Servo velocity command X-axis [-10..+10V] *)
    bLoadUnbalancedAlarm     : BOOL;     (* Tray CoG out of bounds or mass limit exceeded *)
    bPositionalDeviationAlarm: BOOL;     (* Laser tracking error anomaly detected *)
    bDriveFaultInterlock     : BOOL;     (* Hardware interlock trip output *)
END_VAR

VAR
    (* Internal State Machine *)
    iState                   : INT := 0; 
    
    (* Anti-Windup Non-Linear PID Z-axis *)
    rErrorZ                  : REAL;
    rIntegralZ               : REAL;
    rDerivativeZ             : REAL;
    rLastErrorZ              : REAL;
    rKp_Z                    : REAL := 2.5;
    rKi_Z                    : REAL := 0.05;
    rKd_Z                    : REAL := 0.12;
    rIntegralLimit           : REAL := 5.0;
    
    (* Cascade Control Variables *)
    rTargetVelocityZ         : REAL;
    rVelocityErrorZ          : REAL;
    rVelIntegralZ            : REAL;
    
    (* Digital Low-Pass Filters *)
    rFilteredMass            : REAL;
    rAlphaMass               : REAL := 0.1; (* 10Hz sampling assumed *)
    rFilteredVelocityZ       : REAL;
    rAlphaVel                : REAL := 0.15;

    (* Payload Balance Envelope *)
    rMaxMassLimit            : REAL := 1500.0; (* 1.5 tons max per tray *)
    rMaxCoGDeviation         : REAL := 250.0;  (* Max allowable CoG shift from center [mm] *)
    
    (* Predictive Anomaly Variables *)
    rPredictedPosZ           : REAL;
    rAnomalyThreshold        : REAL := 15.0; (* mm deviation to trigger trip *)
    
    (* Timers *)
    tStartupDelay            : TON;
    tSafetyWatchdog          : TON;
END_VAR

(* === SYSTEM SAFETY INTERLOCKS AND PRE-CHECKS === *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    rControlOutputZ_V := 0.0;
    rControlOutputX_V := 0.0;
    bDriveFaultInterlock := TRUE;
    iState := 0;
    RETURN;
END_IF;

IF bMaintenanceMode THEN
    (* Slow manual jog handled externally, hold position safely *)
    bSystemReady := FALSE;
    bDriveFaultInterlock := FALSE;
    iState := 0;
    RETURN;
END_IF;

(* Digital Low-Pass Filtering for noisy analog sensors *)
rFilteredMass := (rAlphaMass * rPayloadMass_kg) + ((1.0 - rAlphaMass) * rFilteredMass);
rFilteredVelocityZ := (rAlphaVel * rVelocityZ_mm_s) + ((1.0 - rAlphaVel) * rFilteredVelocityZ);

(* Predictive Anomaly Detection: Z-axis Laser Tracking Error *)
rPredictedPosZ := rLaserPositionZ_mm + (rFilteredVelocityZ * 0.1); (* 100ms lookahead *)
IF ABS(rTargetPositionZ_mm - rPredictedPosZ) > rAnomalyThreshold AND iState = 30 THEN
    (* Position deviation growing beyond expected dynamic envelope *)
    bPositionalDeviationAlarm := TRUE;
END_IF;

(* Payload Balancing and Limit Checking *)
IF rFilteredMass > rMaxMassLimit OR 
   ABS(rTrayCenterOfGravityX_mm) > rMaxCoGDeviation OR 
   ABS(rTrayCenterOfGravityY_mm) > rMaxCoGDeviation THEN
    bLoadUnbalancedAlarm := TRUE;
    bDriveFaultInterlock := TRUE;
    iState := 999; (* FAULT STATE *)
ELSE
    bLoadUnbalancedAlarm := FALSE;
END_IF;


(* === MAIN LOGIC STATE MACHINE === *)
CASE iState OF
    0: (* IDLE & SAFETY CHECK *)
        bSystemReady := FALSE;
        rControlOutputZ_V := 0.0;
        rControlOutputX_V := 0.0;
        IF bEnableMaster AND NOT bDriveFaultInterlock AND bEmergencyStop THEN
            tStartupDelay(IN := TRUE, PT := T#2S);
            IF tStartupDelay.Q THEN
                tStartupDelay(IN := FALSE);
                bSystemReady := TRUE;
                iState := 10;
            END_IF;
        ELSE
            tStartupDelay(IN := FALSE);
        END_IF;

    10: (* READY TO MOVE *)
        bSystemReady := TRUE;
        (* Check if movement required *)
        IF ABS(rTargetPositionZ_mm - rLaserPositionZ_mm) > 1.0 THEN
            (* Initialize Cascade PID variables *)
            rIntegralZ := 0.0;
            rLastErrorZ := 0.0;
            rVelIntegralZ := 0.0;
            iState := 30; (* MOVING *)
        END_IF;
        
        IF NOT bEnableMaster THEN
            iState := 0;
        END_IF;

    30: (* CASCADE POSITION AND VELOCITY CONTROL *)
        (* Outer Loop: Position Control to generate Target Velocity *)
        rErrorZ := rTargetPositionZ_mm - rLaserPositionZ_mm;
        
        (* Non-linear adaptive P-gain based on error magnitude and payload mass *)
        (* Heavier loads require softer acceleration to prevent mast oscillation *)
        rKp_Z := 2.5 * (1.0 - (rFilteredMass / (rMaxMassLimit * 1.5)));
        
        (* Anti-Windup Integration *)
        rIntegralZ := rIntegralZ + rErrorZ * 0.01; (* 10ms cycle time *)
        IF rIntegralZ > rIntegralLimit THEN rIntegralZ := rIntegralLimit; END_IF;
        IF rIntegralZ < -rIntegralLimit THEN rIntegralZ := -rIntegralLimit; END_IF;
        
        rDerivativeZ := (rErrorZ - rLastErrorZ) / 0.01;
        rLastErrorZ := rErrorZ;
        
        rTargetVelocityZ := (rKp_Z * rErrorZ) + (rKi_Z * rIntegralZ) + (rKd_Z * rDerivativeZ);
        
        (* Limit Target Velocity based on mechanical constraints *)
        IF rTargetVelocityZ > 2500.0 THEN rTargetVelocityZ := 2500.0; END_IF;
        IF rTargetVelocityZ < -2500.0 THEN rTargetVelocityZ := -2500.0; END_IF;

        (* Inner Loop: Velocity Control to generate Voltage Command *)
        rVelocityErrorZ := rTargetVelocityZ - rFilteredVelocityZ;
        rVelIntegralZ := rVelIntegralZ + rVelocityErrorZ * 0.01;
        
        (* Clamp velocity integral *)
        IF rVelIntegralZ > 5.0 THEN rVelIntegralZ := 5.0; END_IF;
        IF rVelIntegralZ < -5.0 THEN rVelIntegralZ := -5.0; END_IF;
        
        (* Simplified P-I Inner Loop *)
        rControlOutputZ_V := (0.005 * rVelocityErrorZ) + (0.01 * rVelIntegralZ);
        
        (* Clamp Output to DAC limits *)
        IF rControlOutputZ_V > 10.0 THEN rControlOutputZ_V := 10.0; END_IF;
        IF rControlOutputZ_V < -10.0 THEN rControlOutputZ_V := -10.0; END_IF;

        (* Target Reached? *)
        IF ABS(rErrorZ) <= 1.0 AND ABS(rFilteredVelocityZ) < 5.0 THEN
            iState := 10; (* Back to ready *)
        END_IF;

    999: (* FAULT HANDLING *)
        bSystemReady := FALSE;
        rControlOutputZ_V := 0.0;
        rControlOutputX_V := 0.0;
        (* Require Master Enable cycle to reset *)
        IF NOT bEnableMaster THEN
            bDriveFaultInterlock := FALSE;
            bPositionalDeviationAlarm := FALSE;
            iState := 0;
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
```"""

import os
os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump({"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}, f, ensure_ascii=False)
print(f"Saved to {filename}")
