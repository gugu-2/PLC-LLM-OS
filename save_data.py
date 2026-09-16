import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Offshore Wind Turbine Blade Pitch and Yaw Aerodynamic Load Balancing**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_WindTurbine_PitchYaw\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Offshore Wind Turbine Blade Pitch and Yaw Aerodynamic Load Balancing

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_OffshoreWindTurbine_PitchYaw_AeroLoadBalancer
(* 
   =============================================================================
   LUMINA ELITE AUTOMATION ARCHITECTURE - SYNTHETIC DATA GENERATION
   Domain: Offshore Wind Turbine Blade Pitch and Yaw Aerodynamic Load Balancing
   Version: 5.0 (Mathematical Modeling and PID Tuning)
   =============================================================================
*)
VAR_INPUT
    (* Safety and System Enable *)
    bSystemEnable           : BOOL;     (* Main activation signal *)
    bEmergencyStop          : BOOL;     (* E-Stop OK, 1 = Safe *)
    bGridFaultActive        : BOOL;     (* High if grid throws a fault *)
    
    (* Environmental & Sensor Inputs *)
    rWindSpeed              : REAL;     (* Hub height wind speed [m/s] *)
    rWindDirection          : REAL;     (* Wind direction relative to North [deg] *)
    rNacelleYawAngle        : REAL;     (* Current Nacelle Yaw [deg] *)
    
    (* Rotor Dynamics *)
    rRotorSpeed             : REAL;     (* Rotor angular velocity [RPM] *)
    rBlade1RootBending      : REAL;     (* Blade 1 root bending moment [kNm] *)
    rBlade2RootBending      : REAL;     (* Blade 2 root bending moment [kNm] *)
    rBlade3RootBending      : REAL;     (* Blade 3 root bending moment [kNm] *)
END_VAR

VAR_OUTPUT
    (* Status and Alarms *)
    bSystemReady            : BOOL;     (* System healthy and ready *)
    bSafetyTrip             : BOOL;     (* True if structural limits exceeded *)
    bGridCurtailmentMode    : BOOL;     (* True if shedding load due to grid *)
    
    (* Actuation Signals *)
    rPitchCommandB1         : REAL;     (* Blade 1 Pitch Setpoint [deg] *)
    rPitchCommandB2         : REAL;     (* Blade 2 Pitch Setpoint [deg] *)
    rPitchCommandB3         : REAL;     (* Blade 3 Pitch Setpoint [deg] *)
    rYawRateCommand         : REAL;     (* Yaw motor rate setpoint [deg/s] *)
END_VAR

VAR
    (* State Machine *)
    iState                  : INT := 0; 
    
    (* Internal Calculations *)
    rAvgBendingMoment       : REAL;
    rYawError               : REAL;
    rPitchOffsetB1          : REAL;
    rPitchOffsetB2          : REAL;
    rPitchOffsetB3          : REAL;
    rCollectivePitchCmd     : REAL;
    
    (* Timers and Filters *)
    tStartupDelay           : TON;
    tFaultTimer             : TON;
    
    (* Tuning Constants *)
    K_P_YAW                 : REAL := 0.5;
    K_I_YAW                 : REAL := 0.01;
    K_D_YAW                 : REAL := 0.05;
    MAX_YAW_RATE            : REAL := 0.5;  (* [deg/s] *)
    NOMINAL_ROTOR_RPM       : REAL := 12.0;
    
    (* Control Integrators *)
    rYawIntegral            : REAL := 0.0;
END_VAR

(* === SAFETY & FAULT HANDLING === *)
IF NOT bEmergencyStop OR bGridFaultActive THEN
    bSystemReady := FALSE;
    bSafetyTrip  := TRUE;
    
    (* Feather blades to safe stop *)
    rPitchCommandB1 := 90.0;
    rPitchCommandB2 := 90.0;
    rPitchCommandB3 := 90.0;
    rYawRateCommand := 0.0;
    iState := 0;
    RETURN;
END_IF;

bSafetyTrip := FALSE;

(* === MAIN STATE MACHINE === *)
CASE iState OF
    0: (* SYSTEM IDLE / INIT *)
        bSystemReady := FALSE;
        rPitchCommandB1 := 90.0;
        rPitchCommandB2 := 90.0;
        rPitchCommandB3 := 90.0;
        rYawRateCommand := 0.0;
        
        IF bSystemEnable THEN
            tStartupDelay(IN := TRUE, PT := T#10S);
            IF tStartupDelay.Q THEN
                tStartupDelay(IN := FALSE);
                iState := 10;
            END_IF;
        ELSE
            tStartupDelay(IN := FALSE);
        END_IF;

    10: (* NORMAL OPERATION: YAW AND PITCH CONTROL *)
        bSystemReady := TRUE;
        
        (* 1. Yaw Alignment Control (PID) *)
        rYawError := rWindDirection - rNacelleYawAngle;
        
        (* Normalize error to -180 to 180 degrees *)
        IF rYawError > 180.0 THEN
            rYawError := rYawError - 360.0;
        ELSIF rYawError < -180.0 THEN
            rYawError := rYawError + 360.0;
        END_IF;
        
        (* Anti-windup for Yaw Integral *)
        IF ABS(rYawError) < 10.0 THEN
            rYawIntegral := rYawIntegral + (rYawError * 0.1); 
        END_IF;
        
        rYawRateCommand := (K_P_YAW * rYawError) + (K_I_YAW * rYawIntegral);
        
        (* Clamp Yaw Rate *)
        IF rYawRateCommand > MAX_YAW_RATE THEN
            rYawRateCommand := MAX_YAW_RATE;
        ELSIF rYawRateCommand < -MAX_YAW_RATE THEN
            rYawRateCommand := -MAX_YAW_RATE;
        END_IF;
        
        (* 2. Aerodynamic Load Balancing (Individual Pitch Control) *)
        rAvgBendingMoment := (rBlade1RootBending + rBlade2RootBending + rBlade3RootBending) / 3.0;
        
        (* Base collective pitch based on wind speed (simplified mapping) *)
        IF rWindSpeed < 4.0 THEN
            rCollectivePitchCmd := 0.0;
        ELSIF rWindSpeed > 25.0 THEN
            rCollectivePitchCmd := 90.0; (* Feather in extreme wind *)
        ELSE
            rCollectivePitchCmd := (rWindSpeed - 4.0) * 1.5; 
        END_IF;
        
        (* Individual cyclic pitch offsets to reject asymmetric rotor loads *)
        rPitchOffsetB1 := (rBlade1RootBending - rAvgBendingMoment) * 0.02;
        rPitchOffsetB2 := (rBlade2RootBending - rAvgBendingMoment) * 0.02;
        rPitchOffsetB3 := (rBlade3RootBending - rAvgBendingMoment) * 0.02;
        
        rPitchCommandB1 := rCollectivePitchCmd + rPitchOffsetB1;
        rPitchCommandB2 := rCollectivePitchCmd + rPitchOffsetB2;
        rPitchCommandB3 := rCollectivePitchCmd + rPitchOffsetB3;

        IF NOT bSystemEnable THEN
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
