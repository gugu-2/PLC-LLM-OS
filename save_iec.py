import json, uuid, os

prompt = """<USER_REQUEST>
You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Advanced Semiconductor Extreme Ultraviolet (EUV) Wafer Stage**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Magnetic levitation 6-DOF planar motor positioning, nanometer-level laser interferometry dynamic thermal compensation, and vacuum reticle chuck electrostatic clamping). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_EUV_WaferStage\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Advanced Semiconductor Extreme Ultraviolet (EUV) Wafer Stage

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT.
</USER_REQUEST>"""

code = """```iec-st
FUNCTION_BLOCK FB_EUV_WaferStage
VAR_INPUT
    (* Required: at least 4-8 physical inputs with types and comments *)
    bEnable                 : BOOL;     (* System Enable Signal - Safely initializes the levitation *)
    bEmergencyStop          : BOOL;     (* Safety interlock for high voltage and laser shutdown *)
    rLaserInterferometerX   : LREAL;    (* Nanometer-level position feedback X-axis (nm) *)
    rLaserInterferometerY   : LREAL;    (* Nanometer-level position feedback Y-axis (nm) *)
    rLaserInterferometerZ   : LREAL;    (* Nanometer-level position feedback Z-axis (nm) *)
    rReticleVacuumPressure  : REAL;     (* Vacuum pressure for electrostatic chuck (mTorr) *)
    rAmbientTemperature     : REAL;     (* Chamber temperature for thermal compensation (C) *)
    rThermalExpansionCoef   : LREAL;    (* Material specific thermal expansion coefficient *)
END_VAR
VAR_OUTPUT
    (* Required: at least 3-6 outputs with types and comments *)
    bSystemReady            : BOOL;     (* Indicates magnetic levitation and vacuum are stable *)
    rPlanarMotorForceX      : LREAL;    (* Force command to X-axis planar motor coils (N) *)
    rPlanarMotorForceY      : LREAL;    (* Force command to Y-axis planar motor coils (N) *)
    rPlanarMotorForceZ      : LREAL;    (* Force command to Z-axis planar motor coils (N) *)
    bElectrostaticClampOn   : BOOL;     (* Enable electrostatic chuck clamping *)
    bFault                  : BOOL;     (* Global fault indicator *)
    iFaultCode              : INT;      (* Diagnostic fault code *)
END_VAR
VAR
    (* Internal state variables *)
    iState                  : INT := 0; (* Internal state machine *)
    tStartupDelay           : TON;      (* Initialization delay timer *)
    tSettleDelay            : TON;      (* Levitation settling timer *)
    rTargetX                : LREAL := 0.0; (* Trajectory target X *)
    rTargetY                : LREAL := 0.0; (* Trajectory target Y *)
    rTargetZ                : LREAL := 50000.0; (* Levitation height target Z (nm) *)
    
    (* Internal Kinematic State *)
    rErrorX                 : LREAL;
    rErrorY                 : LREAL;
    rErrorZ                 : LREAL;
    
    (* PID Gains *)
    Kp                      : LREAL := 15.0;
    Kd                      : LREAL := 3.5;
    Ki                      : LREAL := 0.1;
    
    rIntegralX              : LREAL := 0.0;
    rIntegralY              : LREAL := 0.0;
    rIntegralZ              : LREAL := 0.0;
    
    (* Thermal Compensation *)
    rThermalOffset          : LREAL := 0.0;
END_VAR

(* === MAIN LOGIC === *)
(* Handle Emergency Stop immediately *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bElectrostaticClampOn := FALSE;
    rPlanarMotorForceX := 0.0;
    rPlanarMotorForceY := 0.0;
    rPlanarMotorForceZ := 0.0;
    bFault := TRUE;
    iFaultCode := 999; (* 999 = E-STOP ACTIVE *)
    iState := 0;
    RETURN;
END_IF;

(* Dynamic Thermal Compensation *)
(* Calculates nanometer shift due to ambient temperature delta from 20.0 C nominal *)
rThermalOffset := (rAmbientTemperature - 20.0) * rThermalExpansionCoef * 1000.0; (* Offset in nm *)

CASE iState OF
    0: (* IDLE & VACUUM CHECK *)
        bSystemReady := FALSE;
        bElectrostaticClampOn := FALSE;
        IF bEnable THEN
            IF rReticleVacuumPressure < 1.0 THEN
                iState := 10; (* Vacuum achieved, proceed to clamp *)
            ELSE
                bFault := TRUE;
                iFaultCode := 101; (* Vacuum too high *)
            END_IF;
        END_IF;

    10: (* ELECTROSTATIC CLAMPING *)
        bElectrostaticClampOn := TRUE;
        tStartupDelay(IN := TRUE, PT := T#2S);
        IF tStartupDelay.Q THEN
            tStartupDelay(IN := FALSE);
            iState := 20; (* Proceed to levitation *)
        END_IF;

    20: (* MAGNETIC LEVITATION INITIALIZATION *)
        (* Gentle Z-axis lift profile *)
        rErrorZ := rTargetZ - rLaserInterferometerZ;
        rIntegralZ := rIntegralZ + rErrorZ;
        rPlanarMotorForceZ := (Kp * rErrorZ) + (Ki * rIntegralZ);
        
        tSettleDelay(IN := TRUE, PT := T#5S);
        IF tSettleDelay.Q THEN
            tSettleDelay(IN := FALSE);
            IF ABS(rErrorZ) < 50.0 THEN (* Settled within 50nm *)
                iState := 30;
            ELSE
                bFault := TRUE;
                iFaultCode := 201; (* Levitation failed to settle *)
                iState := 0;
            END_IF;
        END_IF;

    30: (* ACTIVE 6-DOF POSITIONING *)
        bSystemReady := TRUE;
        bFault := FALSE;
        iFaultCode := 0;
        
        (* X-Axis Control with Thermal Compensation *)
        rErrorX := (rTargetX + rThermalOffset) - rLaserInterferometerX;
        rIntegralX := rIntegralX + rErrorX;
        rPlanarMotorForceX := (Kp * rErrorX) + (Ki * rIntegralX);
        
        (* Y-Axis Control with Thermal Compensation *)
        rErrorY := (rTargetY + rThermalOffset) - rLaserInterferometerY;
        rIntegralY := rIntegralY + rErrorY;
        rPlanarMotorForceY := (Kp * rErrorY) + (Ki * rIntegralY);
        
        (* Z-Axis Maintenance *)
        rErrorZ := rTargetZ - rLaserInterferometerZ;
        rIntegralZ := rIntegralZ + rErrorZ;
        rPlanarMotorForceZ := (Kp * rErrorZ) + (Ki * rIntegralZ);

        (* Check for tracking errors *)
        IF ABS(rErrorX) > 100.0 OR ABS(rErrorY) > 100.0 THEN
            bFault := TRUE;
            iFaultCode := 301; (* Tracking error exceeded *)
            iState := 0; (* Abort to safe state *)
        END_IF;
        
        IF NOT bEnable THEN
            iState := 0;
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
