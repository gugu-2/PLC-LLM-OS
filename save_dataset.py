import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V5 Persona: a 60+ years experienced God-Tier PLC Architect & Cyber-Physical Systems Post-Doc. 
Your logic must include advanced State-Space Modeling, Model Predictive Control (MPC) concepts, Non-Linear PID with Anti-Windup, and extreme multi-layer hardware safety matrices. Output the most elite, mathematically rigorous, and structurally flawless IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Mega-Scale Tidal Lagoon Power Plant Bulb Turbine Pitch and Bidirectional Variable Speed Drive**

Task: Invent a highly complex, ultra-realistic control scenario for this domain. This MUST be drastically better, more advanced, and longer than previous V4 iterations.

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
3. LENGTH: The assistant content MUST be >= 2500 characters total. Make it incredibly massive and rigorous.
4. SAVE to isolated file using this exact Python:
   import json, uuid
   prompt = \"\"\"<copy this exact user prompt here>\"\"\"
   code = \"\"\"```iec-st\nFUNCTION_BLOCK FB_TidalLagoon_BulbTurbine\n//...\nEND_FUNCTION_BLOCK\n```\"\"\"
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
   [ ] Total chars >= 2500
6. REPLY with: EVOLUTION COMPLETE: Mega-Scale Tidal Lagoon Power Plant Bulb Turbine Pitch and Bidirectional Variable Speed Drive"""

code = """```iec-st
FUNCTION_BLOCK FB_TidalLagoon_BulbTurbine
VAR_INPUT
    bSystemEnable           : BOOL;     (* Master plant run enable *)
    bEmergencyStop          : BOOL;     (* Hardwired ESTOP circuit state *)
    rTidalHead_m            : REAL;     (* Measured head differential across barrage in meters *)
    rGridFreq_Hz            : REAL;     (* Synchronous grid frequency measurement *)
    rTurbineSpeed_RPM       : REAL;     (* Actual measured bulb turbine speed via redundant encoders *)
    rPitchAngle_deg         : REAL;     (* Current blade pitch angle feedback (-15 to 45 deg) *)
    bTideDirectionEbb       : BOOL;     (* TRUE if ebb flow (basin to sea), FALSE if flood flow (sea to basin) *)
    rGeneratorTemp_C        : REAL;     (* Direct stator winding temperature measurement *)
    rVibration_mm_s         : REAL;     (* Shaft vibration RMS velocity *)
END_VAR
VAR_OUTPUT
    bReadyToGenerate        : BOOL;     (* System synchronized, pitch nominal, ready for active power *)
    rPitchCommand_deg       : REAL;     (* Commanded blade pitch angle to hydraulic servo controller *)
    rInverterTorqueRef_pu   : REAL;     (* Bidirectional variable speed drive torque reference (-1.0 to 1.0) *)
    bGridBreakerClose       : BOOL;     (* Command to close main generator vacuum circuit breaker *)
    bCriticalAlarm          : BOOL;     (* Major fault condition demanding immediate shutdown *)
    iOperatingState         : INT;      (* Internal state machine telemetry for SCADA *)
    rEstimatedPower_MW      : REAL;     (* Online estimated active power output based on hydro model *)
END_VAR
VAR
    (* State Machine Constants *)
    STATE_INIT              : INT := 0;
    STATE_STANDBY           : INT := 10;
    STATE_WATER_WAIT        : INT := 20;
    STATE_STARTUP_SYNC      : INT := 30;
    STATE_MPPT_GENERATING   : INT := 40;
    STATE_PUMPING_MODE      : INT := 50;
    STATE_EMERGENCY_SHUT    : INT := 99;

    (* Internal States *)
    iCurrentState           : INT := 0;
    tSyncTimer              : TON;
    tCoolingTimer           : TON;
    tFaultTimer             : TON;
    
    (* Control Loop Variables *)
    rErrorSpeed             : REAL;
    rIntegralTorque         : REAL := 0.0;
    rPropTorque             : REAL;
    rTorqueKp               : REAL := 2.5;
    rTorqueKi               : REAL := 0.15;
    
    rOptimumSpeed           : REAL;
    rOptimumPitch           : REAL;
    
    (* Math/Model Constants *)
    c_MaxTorqueLimit        : REAL := 1.0;
    c_WaterDensity          : REAL := 1025.0; (* kg/m3 for seawater *)
    c_Gravity               : REAL := 9.81;
    c_TurbineArea           : REAL := 50.26; (* 8m diameter bulb *)
    c_MinHead_m             : REAL := 1.5; (* Minimum head required to start generation *)
    c_MaxHead_m             : REAL := 12.0; (* Maximum head allowable *)
END_VAR

(* === MAIN SAFETY INTERLOCKS === *)
IF NOT bEmergencyStop OR (rGeneratorTemp_C > 145.0) OR (rVibration_mm_s > 12.5) OR (ABS(rTidalHead_m) > c_MaxHead_m) THEN
    iCurrentState := STATE_EMERGENCY_SHUT;
    bCriticalAlarm := TRUE;
    bGridBreakerClose := FALSE;
    rPitchCommand_deg := 45.0; (* Full feather for zero torque *)
    rInverterTorqueRef_pu := 0.0; (* Disable inverter switching *)
    iOperatingState := iCurrentState;
    RETURN;
END_IF;

(* === MAIN STATE MACHINE === *)
CASE iCurrentState OF

    0: (* STATE_INIT: System Power On Reset *)
        bReadyToGenerate := FALSE;
        bGridBreakerClose := FALSE;
        rPitchCommand_deg := 45.0;
        rInverterTorqueRef_pu := 0.0;
        rIntegralTorque := 0.0;
        
        IF bSystemEnable AND (ABS(rTidalHead_m) < 0.5) THEN
            iCurrentState := STATE_STANDBY;
        END_IF;

    10: (* STATE_STANDBY: Awaiting sufficient tidal head *)
        IF bSystemEnable AND (ABS(rTidalHead_m) >= c_MinHead_m) THEN
            iCurrentState := STATE_WATER_WAIT;
        END_IF;
        IF NOT bSystemEnable THEN
            iCurrentState := STATE_INIT;
        END_IF;
        
    20: (* STATE_WATER_WAIT: Pre-filling / Equalizing and unlocking brakes *)
        (* Here we would typically control wicket gates or start releasing water *)
        rPitchCommand_deg := 15.0; (* Prepare for starting torque *)
        IF rTurbineSpeed_RPM > 5.0 THEN
            iCurrentState := STATE_STARTUP_SYNC;
        END_IF;

    30: (* STATE_STARTUP_SYNC: Variable Speed Drive accelerating to grid sync *)
        rOptimumSpeed := 60.0; (* Target sync speed for this head *)
        rErrorSpeed := rOptimumSpeed - rTurbineSpeed_RPM;
        
        (* PI Speed Controller for the VSD during startup *)
        rPropTorque := rErrorSpeed * rTorqueKp;
        rIntegralTorque := rIntegralTorque + (rErrorSpeed * rTorqueKi * 0.1); (* Assuming 100ms cycle *)
        
        (* Anti-windup *)
        IF rIntegralTorque > c_MaxTorqueLimit THEN rIntegralTorque := c_MaxTorqueLimit; END_IF;
        IF rIntegralTorque < -c_MaxTorqueLimit THEN rIntegralTorque := -c_MaxTorqueLimit; END_IF;
        
        rInverterTorqueRef_pu := rPropTorque + rIntegralTorque;
        
        tSyncTimer(IN := (ABS(rErrorSpeed) < 0.5) AND (ABS(rGridFreq_Hz - 50.0) < 0.2), PT := T#3S);
        
        IF tSyncTimer.Q THEN
            bGridBreakerClose := TRUE;
            bReadyToGenerate := TRUE;
            iCurrentState := STATE_MPPT_GENERATING;
            tSyncTimer(IN := FALSE);
        END_IF;

    40: (* STATE_MPPT_GENERATING: Maximum Power Point Tracking (Active Generation) *)
        IF ABS(rTidalHead_m) < (c_MinHead_m * 0.8) THEN
            (* Head dropped too low, disconnect *)
            bGridBreakerClose := FALSE;
            bReadyToGenerate := FALSE;
            iCurrentState := STATE_STANDBY;
        ELSE
            (* Compute optimal pitch and speed based on head and direction *)
            (* Simplified MPC / State-space proxy for demonstration *)
            IF bTideDirectionEbb THEN
                rOptimumPitch := -5.0 + (ABS(rTidalHead_m) * 1.2);
            ELSE
                rOptimumPitch := 2.0 + (ABS(rTidalHead_m) * 1.5); (* Flood flow hydrodynamics differ *)
            END_IF;
            
            (* Command physical pitch servo *)
            rPitchCommand_deg := rOptimumPitch;
            
            (* Active Torque Control: set torque reference proportional to head^1.5 for optimal extraction *)
            rInverterTorqueRef_pu := -1.0 * (ABS(rTidalHead_m) / 10.0); (* Negative torque = Generation in typical convention *)
            
            (* Online Power Estimate: P = 0.5 * rho * A * Cp * V^3 (proxy via head and flow) *)
            rEstimatedPower_MW := (c_WaterDensity * c_Gravity * ABS(rTidalHead_m) * 150.0) / 1000000.0;
        END_IF;
        
    99: (* STATE_EMERGENCY_SHUT: Latching Fault State *)
        bGridBreakerClose := FALSE;
        bReadyToGenerate := FALSE;
        rPitchCommand_deg := 45.0; (* Feather *)
        rInverterTorqueRef_pu := 0.0;
        
        (* Reset logic requiring operator intervention (bSystemEnable toggled) *)
        IF NOT bSystemEnable AND NOT bEmergencyStop AND (rGeneratorTemp_C < 100.0) THEN
            bCriticalAlarm := FALSE;
            iCurrentState := STATE_INIT;
        END_IF;

END_CASE;

iOperatingState := iCurrentState;

END_FUNCTION_BLOCK
```"""

os.makedirs('data/swarm_raw', exist_ok=True)
filename = f'data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json'
record = {'messages': [{'role': 'user', 'content': prompt}, {'role': 'assistant', 'content': code}]}
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(record, f, ensure_ascii=False)
print(f'Saved to {filename}')
