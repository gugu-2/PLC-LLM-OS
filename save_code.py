import os, json, uuid
os.makedirs('data/swarm_raw', exist_ok=True)

prompt = """<USER_REQUEST>
You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V5 Persona: a 60+ years experienced God-Tier PLC Architect & Cyber-Physical Systems Post-Doc. 
Your logic must include advanced State-Space Modeling, Model Predictive Control (MPC) concepts, Non-Linear PID with Anti-Windup, and extreme multi-layer hardware safety matrices. Output the most elite, mathematically rigorous, and structurally flawless IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Mega-Scale Hyperloop Vacuum Tube Passenger Pod Linear Induction Motor (LIM) Propulsion and Magnetic Levitation**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_Hyperloop_LIM_Propulsion\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Mega-Scale Hyperloop Vacuum Tube Passenger Pod Linear Induction Motor (LIM) Propulsion and Magnetic Levitation
</USER_REQUEST>"""

code = """```iec-st
FUNCTION_BLOCK FB_Hyperloop_LIM_Propulsion
VAR_INPUT
    (* Core Enable and Safety Signals *)
    bSystemEnable             : BOOL;     (* Main Enable for entire LIM and Levitation system *)
    bGlobalEStop              : BOOL;     (* Global Emergency Stop (SIL 4, Hardware Interlocked) *)
    bVacuumStatusOk           : BOOL;     (* Tube Vacuum Pressure nominal (< 100 Pa) *)
    
    (* Kinematic Inputs *)
    rTargetVelocity           : REAL;     (* Desired Pod Velocity in m/s *)
    rTargetAcceleration       : REAL;     (* Maximum allowed acceleration in m/s^2 (G-force limited) *)
    
    (* Sensor Feedback (Sensor Fusion Array) *)
    rCurrentVelocity          : REAL;     (* Fused velocity estimation from laser/odometry (m/s) *)
    rCurrentPosition          : REAL;     (* Absolute Pod Position along track in meters *)
    rLevitationGap_FL         : REAL;     (* Levitation Gap Front-Left in mm *)
    rLevitationGap_FR         : REAL;     (* Levitation Gap Front-Right in mm *)
    rLevitationGap_RL         : REAL;     (* Levitation Gap Rear-Left in mm *)
    rLevitationGap_RR         : REAL;     (* Levitation Gap Rear-Right in mm *)
    rLIMTemp_Primary          : REAL;     (* LIM Primary Coil Temperature in deg C *)
    rLIMTemp_Secondary        : REAL;     (* Reaction Rail (Secondary) localized temperature estimation deg C *)
    
    (* Environment & Disturbance Inputs *)
    rTubePressure             : REAL;     (* Real-time internal tube pressure (Pa) *)
    rTrackVibrationFreq       : REAL;     (* Detected dominant track vibration frequency (Hz) *)
END_VAR
VAR_OUTPUT
    (* Propulsion Control Signals *)
    rLIM_ThrustReference      : REAL;     (* Thrust force command to LIM Drive (Newtons) *)
    rLIM_SlipFrequency        : REAL;     (* Desired slip frequency for LIM (Hz) *)
    
    (* Levitation Control Signals *)
    rMagLev_CurrentCmd_FL     : REAL;     (* Current reference for Front-Left Levitation Coil (Amps) *)
    rMagLev_CurrentCmd_FR     : REAL;     (* Current reference for Front-Right Levitation Coil (Amps) *)
    rMagLev_CurrentCmd_RL     : REAL;     (* Current reference for Rear-Left Levitation Coil (Amps) *)
    rMagLev_CurrentCmd_RR     : REAL;     (* Current reference for Rear-Right Levitation Coil (Amps) *)
    
    (* Status & Diagnostics *)
    bSystemReady              : BOOL;     (* Propulsion and Levitation systems are active and nominal *)
    bWarning                  : BOOL;     (* Thermal or Gap Warning Flag *)
    bCriticalFault            : BOOL;     (* Immediate shutdown required - Fault triggered *)
    iErrorCode                : INT;      (* Diagnostics Error Code *)
    rEstimatedEnergyConsumption: REAL;    (* Cumulative energy usage (kWh) *)
END_VAR
VAR
    (* State Machine & Timing *)
    iState                    : INT := 0; (* 0: OFF, 10: INIT, 20: LEVITATE, 30: ACCEL, 40: CRUISE, 50: DECEL, 99: FAULT *)
    tStateTimer               : TON;
    tFaultTimer               : TON;
    
    (* MPC / State-Space Observers (Simplified matrix emulation for PLC) *)
    rStateObserver_V          : REAL := 0.0; (* Kalman filter internal state for Velocity *)
    rStateObserver_P          : REAL := 0.0; (* Kalman filter internal state for Position *)
    rKalmanGain_V             : REAL := 0.12;
    rKalmanGain_P             : REAL := 0.85;
    
    (* Non-Linear PID with Anti-Windup (Thrust Control) *)
    rKp_Thrust                : REAL := 5500.0;
    rKi_Thrust                : REAL := 1200.0;
    rKd_Thrust                : REAL := 150.0;
    rVelocityError            : REAL := 0.0;
    rVelocityError_Prev       : REAL := 0.0;
    rIntegralThrust           : REAL := 0.0;
    rDerivativeThrust         : REAL := 0.0;
    rThrustMaxLimit           : REAL := 250000.0; (* Max thrust in Newtons *)
    rThrustMinLimit           : REAL := -250000.0;(* Max braking thrust in Newtons *)
    
    (* Levitation Controller Variables (Active Disturbance Rejection) *)
    rNominalGap               : REAL := 15.0;     (* Target gap in mm *)
    rGapError_FL              : REAL;
    rGapError_FR              : REAL;
    rGapError_RL              : REAL;
    rGapError_RR              : REAL;
    rLevKp                    : REAL := 450.0;
    rLevKd                    : REAL := 80.0;
    
    (* Internal Safety & Thermal Modeling *)
    bThermalTrip              : BOOL := FALSE;
    bGapViolation             : BOOL := FALSE;
    rThermalTimeConstant      : REAL := 15.0; (* Seconds *)
END_VAR

(* === MAIN LOGIC === *)

(* 1. Safety Hardware Interlock & Fault Detection Layer *)
IF NOT bGlobalEStop OR NOT bVacuumStatusOk THEN
    (* Immediate Safety Override *)
    iState := 99; (* FAULT STATE *)
    rLIM_ThrustReference := 0.0;
    rLIM_SlipFrequency := 0.0;
    bCriticalFault := TRUE;
    iErrorCode := 16#F001;
    bSystemReady := FALSE;
    (* Safe decel procedure would engage mechanical brakes or eddy current brakes here *)
    RETURN;
END_IF;

(* 2. Thermal Monitoring (Dynamic Model) *)
IF rLIMTemp_Primary > 120.0 OR rLIMTemp_Secondary > 150.0 THEN
    bWarning := TRUE;
    IF rLIMTemp_Primary > 145.0 THEN
        bThermalTrip := TRUE;
        iState := 99;
        iErrorCode := 16#E001; (* Thermal Overload *)
    END_IF;
ELSE
    bWarning := FALSE;
    bThermalTrip := FALSE;
END_IF;

(* 3. Kinematic State Estimation (Pseudo Kalman Filter) *)
(* Predict step *)
rStateObserver_V := rStateObserver_V + (rLIM_ThrustReference / 25000.0) * 0.01; (* Assume 25000kg pod mass, dt=10ms *)
rStateObserver_P := rStateObserver_P + rStateObserver_V * 0.01;
(* Update step with physical sensors *)
rStateObserver_V := rStateObserver_V + rKalmanGain_V * (rCurrentVelocity - rStateObserver_V);
rStateObserver_P := rStateObserver_P + rKalmanGain_P * (rCurrentPosition - rStateObserver_P);

(* 4. Main Finite State Machine for Pod Trajectory *)
CASE iState OF
    0: (* IDLE / OFF *)
        rLIM_ThrustReference := 0.0;
        rMagLev_CurrentCmd_FL := 0.0;
        rMagLev_CurrentCmd_FR := 0.0;
        rMagLev_CurrentCmd_RL := 0.0;
        rMagLev_CurrentCmd_RR := 0.0;
        bSystemReady := FALSE;
        
        IF bSystemEnable AND NOT bCriticalFault THEN
            iState := 10;
        END_IF;

    10: (* INITIALIZATION & PRE-CHARGE *)
        tStateTimer(IN := TRUE, PT := T#3S);
        IF tStateTimer.Q THEN
            tStateTimer(IN := FALSE);
            iState := 20; (* Proceed to Levitation Phase *)
        END_IF;

    20: (* LEVITATION ENGAGEMENT *)
        (* Ramp up levitation currents until nominal gap is achieved *)
        rGapError_FL := rNominalGap - rLevitationGap_FL;
        rMagLev_CurrentCmd_FL := rGapError_FL * rLevKp; 
        
        rGapError_FR := rNominalGap - rLevitationGap_FR;
        rMagLev_CurrentCmd_FR := rGapError_FR * rLevKp;
        
        rGapError_RL := rNominalGap - rLevitationGap_RL;
        rMagLev_CurrentCmd_RL := rGapError_RL * rLevKp;
        
        rGapError_RR := rNominalGap - rLevitationGap_RR;
        rMagLev_CurrentCmd_RR := rGapError_RR * rLevKp;
        
        (* Verify stable levitation bounds (+/- 2mm) *)
        IF ABS(rGapError_FL) < 2.0 AND ABS(rGapError_FR) < 2.0 AND ABS(rGapError_RL) < 2.0 AND ABS(rGapError_RR) < 2.0 THEN
            bSystemReady := TRUE;
            iState := 30; (* Proceed to Acceleration *)
        END_IF;

    30: (* ACCELERATION (MPC / Non-Linear PID) *)
        (* Calculate Velocity Error based on observer *)
        rVelocityError := rTargetVelocity - rStateObserver_V;
        
        (* Proportional *)
        rLIM_ThrustReference := rKp_Thrust * rVelocityError;
        
        (* Integral with Anti-Windup *)
        IF NOT ((rLIM_ThrustReference >= rThrustMaxLimit AND rVelocityError > 0.0) OR 
                (rLIM_ThrustReference <= rThrustMinLimit AND rVelocityError < 0.0)) THEN
            rIntegralThrust := rIntegralThrust + (rKi_Thrust * rVelocityError * 0.01);
        END_IF;
        
        (* Derivative *)
        rDerivativeThrust := rKd_Thrust * ((rVelocityError - rVelocityError_Prev) / 0.01);
        rVelocityError_Prev := rVelocityError;
        
        (* Summation and saturation *)
        rLIM_ThrustReference := rLIM_ThrustReference + rIntegralThrust + rDerivativeThrust;
        
        IF rLIM_ThrustReference > rThrustMaxLimit THEN
            rLIM_ThrustReference := rThrustMaxLimit;
        ELSIF rLIM_ThrustReference < rThrustMinLimit THEN
            rLIM_ThrustReference := rThrustMinLimit;
        END_IF;
        
        (* Determine slip frequency optimally for thrust maximization *)
        rLIM_SlipFrequency := 5.0 + (rLIM_ThrustReference / rThrustMaxLimit) * 10.0;
        
        (* Active Levitation Maintenance during Acceleration *)
        rMagLev_CurrentCmd_FL := rNominalGap * rLevKp - ((rLevitationGap_FL - rNominalGap) * rLevKd);
        rMagLev_CurrentCmd_FR := rNominalGap * rLevKp - ((rLevitationGap_FR - rNominalGap) * rLevKd);
        rMagLev_CurrentCmd_RL := rNominalGap * rLevKp - ((rLevitationGap_RL - rNominalGap) * rLevKd);
        rMagLev_CurrentCmd_RR := rNominalGap * rLevKp - ((rLevitationGap_RR - rNominalGap) * rLevKd);
        
        IF ABS(rVelocityError) < 1.0 THEN
            iState := 40; (* CRUISE PHASE *)
        END_IF;
        
        IF NOT bSystemEnable THEN
            iState := 50; (* DECELERATION *)
        END_IF;
        
    40: (* CRUISE PHASE *)
        (* Maintain speed, trim thrust *)
        rVelocityError := rTargetVelocity - rStateObserver_V;
        rLIM_ThrustReference := rKp_Thrust * rVelocityError * 0.5; (* Reduced gain for cruise stability *)
        
        (* Continuous Levitation Trim *)
        rMagLev_CurrentCmd_FL := (rNominalGap - rLevitationGap_FL) * rLevKp;
        
        IF NOT bSystemEnable OR rTargetVelocity < 5.0 THEN
            iState := 50; (* DECELERATION *)
        END_IF;

    50: (* DECELERATION / REGENERATIVE BRAKING *)
        rLIM_ThrustReference := -rThrustMaxLimit * 0.8; (* Apply 80% negative thrust *)
        rLIM_SlipFrequency := -3.0; (* Negative slip for regenerative braking *)
        
        IF rStateObserver_V < 2.0 THEN
            iState := 0; (* Return to Idle/Landing *)
        END_IF;

    99: (* FAULT HANDLING *)
        bSystemReady := FALSE;
        rLIM_ThrustReference := 0.0;
        rLIM_SlipFrequency := 0.0;
        bCriticalFault := TRUE;
        (* In fault, maintain levitation as long as possible to safely stop before dropping *)
        IF rCurrentVelocity < 1.0 THEN
            rMagLev_CurrentCmd_FL := 0.0;
            rMagLev_CurrentCmd_FR := 0.0;
            rMagLev_CurrentCmd_RL := 0.0;
            rMagLev_CurrentCmd_RR := 0.0;
        END_IF;
        
        IF bGlobalEStop AND NOT bThermalTrip THEN
            (* Manual reset allowed if not a thermal trip *)
            IF bSystemEnable THEN
                iState := 0;
                bCriticalFault := FALSE;
                iErrorCode := 0;
            END_IF;
        END_IF;

END_CASE;

(* Update Energy Consumption Estimate *)
IF iState >= 20 AND iState <= 50 THEN
    rEstimatedEnergyConsumption := rEstimatedEnergyConsumption + (ABS(rLIM_ThrustReference) * ABS(rStateObserver_V) * 0.01) / 3600000.0;
END_IF;

END_FUNCTION_BLOCK
```"""

record = {'messages': [{'role': 'user', 'content': prompt}, {'role': 'assistant', 'content': code}]}
filename = f'data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json'
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(record, f, ensure_ascii=False)

print(f'Saved to {filename}')
