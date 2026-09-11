import json, uuid, os

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Next-Gen Hyperloop Vacuum Tube Linear Induction Motor**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Magnetic levitation (MagLev) active halbach array suspension, supersonic aerodynamic blockage ratio compensation, and transient high-voltage stator switching). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_Hyperloop_LIM\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Next-Gen Hyperloop Vacuum Tube Linear Induction Motor

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_Hyperloop_LIM_Control
VAR_INPUT
    bEnableSystem      : BOOL;    (* Master enable signal for the entire LIM subsystem *)
    bEmergencyStop     : BOOL;    (* Catastrophic failure loop / Safety Relay OK *)
    rLevitationGap_mm  : REAL;    (* Measured air gap from laser triangulation sensors (mm) *)
    rTubePressure_Pa   : REAL;    (* Vacuum tube internal pressure in Pascals *)
    rPodVelocity_ms    : REAL;    (* Current pod velocity in meters per second *)
    rTargetVelocity_ms : REAL;    (* Reference velocity profile target (m/s) *)
    rStatorTemp_C      : REAL;    (* Stator winding temperature (Celsius) *)
END_VAR
VAR_OUTPUT
    bSystemReady       : BOOL;    (* Indicates LIM controller is armed and ready *)
    bFaultActive       : BOOL;    (* Global fault flag (triggers pod emergency braking) *)
    rThrustCommand_kN  : REAL;    (* Force command sent to LIM inverter in kilo-Newtons *)
    rSuspensionCmd_A   : REAL;    (* Active Halbach array trim coil current (Amps) *)
    iFaultCode         : INT;     (* Active fault diagnostic code *)
END_VAR
VAR
    iState             : INT := 0; (* Internal state machine step *)
    rVelocityError     : REAL;     (* Difference between target and actual velocity *)
    rIntegralSum       : REAL := 0.0; (* PID Integral term accumulation *)
    rPrevError         : REAL := 0.0; (* Previous cycle error for derivative calculation *)
    rDerivative        : REAL;     (* Derivative term *)
    rThrustPID         : REAL;     (* PID output for thrust *)
    rGapError          : REAL;     (* Levitation gap error *)
    tStatorCooling     : TON;      (* Cooling system monitor timer *)
    tFaultDebounce     : TON;      (* Timer to debounce transient sensor spikes *)
    
    (* Constants *)
    Kp_Thrust          : REAL := 15.5;
    Ki_Thrust          : REAL := 2.1;
    Kd_Thrust          : REAL := 0.8;
    dT                 : REAL := 0.001; (* 1ms cycle time *)
    MAX_THRUST         : REAL := 150.0; (* Maximum thrust limit kN *)
    MIN_THRUST         : REAL := -100.0; (* Maximum regenerative braking kN *)
    NOMINAL_GAP        : REAL := 15.0; (* Nominal levitation gap in mm *)
    MAX_TEMP           : REAL := 180.0; (* Max stator temperature Celsius *)
    CRITICAL_VACUUM    : REAL := 500.0; (* Max allowable tube pressure (Pa) *)
END_VAR

(* === MAIN LOGIC === *)
(* Emergency Interlocks *)
IF NOT bEmergencyStop THEN
    iState := 999; (* Transition immediately to FAULT state *)
    iFaultCode := 1001; (* E-STOP Activated *)
END_IF;

IF rStatorTemp_C > MAX_TEMP THEN
    tFaultDebounce(IN := TRUE, PT := T#50MS);
    IF tFaultDebounce.Q THEN
        iState := 999;
        iFaultCode := 1002; (* Stator Overtemperature *)
    END_IF;
ELSE
    tFaultDebounce(IN := FALSE);
END_IF;

IF rTubePressure_Pa > CRITICAL_VACUUM THEN
    iState := 999;
    iFaultCode := 1003; (* Vacuum Loss Detected *)
END_IF;

(* Main State Machine *)
CASE iState OF
    0: (* INIT & DIAGNOSTICS *)
        bSystemReady := FALSE;
        bFaultActive := FALSE;
        rThrustCommand_kN := 0.0;
        rSuspensionCmd_A := 0.0;
        rIntegralSum := 0.0;
        
        IF bEnableSystem AND bEmergencyStop THEN
            iState := 10;
        END_IF;

    10: (* STANDBY & LEVITATION CALIBRATION *)
        (* Maintain magnetic levitation gap before allowing thrust *)
        rGapError := NOMINAL_GAP - rLevitationGap_mm;
        rSuspensionCmd_A := rGapError * 5.0; (* Simple proportional control for suspension trim *)
        
        IF ABS(rGapError) < 0.5 THEN
            bSystemReady := TRUE;
            IF rTargetVelocity_ms > 0.1 THEN
                iState := 20; (* TRANSITION TO PROPULSION *)
            END_IF;
        END_IF;

    20: (* ACTIVE PROPULSION (PID CONTROL) *)
        rVelocityError := rTargetVelocity_ms - rPodVelocity_ms;
        
        (* Anti-windup Integral *)
        IF rThrustPID < MAX_THRUST AND rThrustPID > MIN_THRUST THEN
            rIntegralSum := rIntegralSum + (rVelocityError * dT);
        END_IF;
        
        rDerivative := (rVelocityError - rPrevError) / dT;
        rPrevError := rVelocityError;
        
        (* Calculate PID Thrust *)
        rThrustPID := (Kp_Thrust * rVelocityError) + (Ki_Thrust * rIntegralSum) + (Kd_Thrust * rDerivative);
        
        (* Aerodynamic Blockage Ratio Compensation at Transonic Speeds *)
        IF rPodVelocity_ms > 250.0 THEN
            (* Increase thrust to overcome Kantrowitz limit choking effect *)
            rThrustPID := rThrustPID * (1.0 + ((rPodVelocity_ms - 250.0) * 0.002));
        END_IF;
        
        (* Clamp Output *)
        IF rThrustPID > MAX_THRUST THEN
            rThrustCommand_kN := MAX_THRUST;
        ELSIF rThrustPID < MIN_THRUST THEN
            rThrustCommand_kN := MIN_THRUST;
        ELSE
            rThrustCommand_kN := rThrustPID;
        END_IF;
        
        (* Dynamic Levitation Adjustments based on thrust vectoring *)
        rSuspensionCmd_A := (NOMINAL_GAP - rLevitationGap_mm) * 6.5 - (rThrustCommand_kN * 0.05);

        IF rTargetVelocity_ms < 0.1 AND rPodVelocity_ms < 1.0 THEN
            iState := 10;
        END_IF;
        
        IF NOT bEnableSystem THEN
            iState := 0;
        END_IF;

    999: (* FAULT HANDLING *)
        bSystemReady := FALSE;
        bFaultActive := TRUE;
        rThrustCommand_kN := 0.0; (* Cut thrust *)
        (* Maintain suspension to avoid crash during fault braking if possible *)
        rSuspensionCmd_A := (NOMINAL_GAP - rLevitationGap_mm) * 10.0;
        
        (* Wait for manual reset *)
        IF NOT bEnableSystem AND bEmergencyStop THEN
            iState := 0;
            iFaultCode := 0;
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
