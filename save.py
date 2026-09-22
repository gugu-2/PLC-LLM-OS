import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V5 Persona: a 60+ years experienced God-Tier PLC Architect & Cyber-Physical Systems Post-Doc. 
Your logic must include advanced State-Space Modeling, Model Predictive Control (MPC) concepts, Non-Linear PID with Anti-Windup, and extreme multi-layer hardware safety matrices. Output the most elite, mathematically rigorous, and structurally flawless IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Advanced High-Temperature Superconducting (HTS) Maglev Train Levitation Gap and Linear Motor Sync**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_HTSMaglev_Levitation\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Advanced High-Temperature Superconducting (HTS) Maglev Train Levitation Gap and Linear Motor Sync"""

code = """```iec-st
FUNCTION_BLOCK FB_HTSMaglev_Levitation_LinearMotor_Sync
VAR_INPUT
    (* Main Interlocks & References *)
    bSystemEnable           : BOOL;     (* Main safety interlock and system start signal *)
    bEmergencyStop          : BOOL;     (* Hardware E-stop, active low, SIL-4 compliant *)
    rLevitationGapTarget    : REAL;     (* Target levitation gap in mm (e.g., 10.0 to 15.0 mm) *)
    rTrainVelocityRef       : REAL;     (* Reference track velocity profile in km/h *)
    
    (* Actual Sensor Measurements *)
    rLevitationGapActual    : REAL;     (* Measured gap from high-speed laser/eddy current sensors in mm *)
    rTrainVelocityAct       : REAL;     (* Actual velocity from linear sync motor sensors in km/h *)
    rTrainAccelerationAct   : REAL;     (* IMU derived instantaneous acceleration in m/s^2 *)
    rHTSTempFront           : REAL;     (* Superconducting coil temperature front bogie (K) *)
    rHTSTempRear            : REAL;     (* Superconducting coil temperature rear bogie (K) *)
    rCryoPressure           : REAL;     (* Cryocooler LN2/LHe operating pressure in bar *)
    rMagneticFluxDensity    : REAL;     (* Measured magnetic flux density in the air gap (Tesla) *)
END_VAR

VAR_OUTPUT
    (* Status and Control Commands *)
    bSystemReady            : BOOL;     (* Maglev system is fully operational and suspended *)
    rLevitationControlSignal: REAL;     (* Excitation current command to levitation coils (A) *)
    rMotorThrustCommand     : REAL;     (* Thrust force command to linear synchronous motor (kN) *)
    
    (* Diagnostic and Safety Status *)
    bThermalWarning         : BOOL;     (* HTS coil approaching critical temperature limit *)
    bFluxQuenchWarning      : BOOL;     (* Risk of magnetic flux quench detected *)
    bSafetyTrip             : BOOL;     (* Critical fault active, system coasting down or e-braking *)
    iOperatingState         : INT;      (* Internal state machine broadcast for supervisory HMI *)
END_VAR

VAR
    (* Internal State Machine Variables *)
    iState                  : INT := 0;
    tInitTimer              : TON;
    tCoolingTimer           : TON;
    
    (* Non-Linear PID Variables for Levitation (State-Space Feedback Equivalent) *)
    rLevError               : REAL;
    rLevErrorPrev           : REAL;
    rLevErrorIntegral       : REAL;
    rLevErrorDerivative     : REAL;
    
    (* Adaptive Control Parameters *)
    rKp_Adaptive            : REAL := 125.5;
    rKi_Adaptive            : REAL := 45.2;
    rKd_Adaptive            : REAL := 80.1;
    rIntegralMaxLimit       : REAL := 500.0;
    
    (* Linear Motor Sync MPC-like variables *)
    rVelocityError          : REAL;
    rThrustFeedforward      : REAL;
    rDragCompensation       : REAL;
    rAeroCoefficient        : REAL := 0.0052; (* Derived from wind tunnel testing *)
    
    (* Constants and Operational Limits *)
    HTS_TEMP_CRITICAL       : REAL := 77.0;  (* Liquid Nitrogen boiling point ~ 77K *)
    HTS_TEMP_WARNING        : REAL := 72.0;
    CRYO_PRESSURE_MIN       : REAL := 2.5;   (* bar *)
    MAX_EXCITATION_CURRENT  : REAL := 1200.0;(* Amperes per coil group *)
    MAX_THRUST_KN           : REAL := 850.0; (* Maximum permissible thrust (kN) *)
    FLUX_QUENCH_LIMIT       : REAL := 1.8;   (* Tesla threshold for early warning *)
    CYCLE_TIME              : REAL := 0.005; (* 5ms high-speed execution cycle *)
END_VAR

(* === MAIN SAFETY INTERLOCKS & EXTREME HARDWARE SAFETY MATRIX === *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bSafetyTrip := TRUE;
    rLevitationControlSignal := 0.0;
    rMotorThrustCommand := 0.0;
    iState := 999; (* EMERGENCY SCRAM STATE *)
    iOperatingState := iState;
    RETURN;
END_IF;

(* Multi-layer Thermal and Magnetic Protection Logic *)
IF (rHTSTempFront > HTS_TEMP_CRITICAL) OR (rHTSTempRear > HTS_TEMP_CRITICAL) THEN
    bSafetyTrip := TRUE;
    bThermalWarning := TRUE;
    iState := 999;
ELSIF (rHTSTempFront > HTS_TEMP_WARNING) OR (rHTSTempRear > HTS_TEMP_WARNING) THEN
    bThermalWarning := TRUE;
ELSE
    bThermalWarning := FALSE;
END_IF;

(* Flux Quench Protection *)
IF rMagneticFluxDensity > FLUX_QUENCH_LIMIT THEN
    bFluxQuenchWarning := TRUE;
    IF rMagneticFluxDensity > (FLUX_QUENCH_LIMIT * 1.1) THEN
        bSafetyTrip := TRUE;
        iState := 999;
    END_IF;
ELSE
    bFluxQuenchWarning := FALSE;
END_IF;

(* === MAIN STATE MACHINE FOR ADVANCED HTS MAGLEV CONTROL === *)
CASE iState OF
    0: (* IDLE & DIAGNOSTICS: Wait for supervisory control to initialize *)
        bSystemReady := FALSE;
        rLevitationControlSignal := 0.0;
        rMotorThrustCommand := 0.0;
        bSafetyTrip := FALSE;
        rLevErrorIntegral := 0.0;
        
        IF bSystemEnable AND (NOT bSafetyTrip) THEN
            iState := 10; (* Transition to PRE-COOLING & FLUX PINNING CHECK *)
        END_IF;

    10: (* PRE-COOLING VERIFICATION: Ensure cryogenic stability *)
        (* Wait for cryogenic systems to stabilize pressure and temperature margins *)
        tCoolingTimer(IN := TRUE, PT := T#15S);
        IF tCoolingTimer.Q THEN
            IF rCryoPressure > CRYO_PRESSURE_MIN AND (NOT bThermalWarning) THEN
                tCoolingTimer(IN := FALSE);
                iState := 20; (* Transition to INITIATE LEVITATION *)
            ELSE
                iState := 999; (* FAIL TO COOL - Cryogenic fault *)
            END_IF;
        END_IF;

    20: (* INITIATE LEVITATION / GAP RAMP UP *)
        (* Apply non-linear PID with anti-windup for the highly unstable maglev gap dynamics *)
        rLevError := rLevitationGapTarget - rLevitationGapActual;
        
        (* Integrator with Anti-Windup bounds to prevent saturation lock *)
        rLevErrorIntegral := rLevErrorIntegral + (rLevError * CYCLE_TIME);
        IF rLevErrorIntegral > rIntegralMaxLimit THEN
            rLevErrorIntegral := rIntegralMaxLimit;
        ELSIF rLevErrorIntegral < -rIntegralMaxLimit THEN
            rLevErrorIntegral := -rIntegralMaxLimit;
        END_IF;
        
        rLevErrorDerivative := (rLevError - rLevErrorPrev) / CYCLE_TIME;
        
        (* Calculate dynamic gain scaling based on gap proximity (Non-linear element) *)
        IF rLevitationGapActual < (rLevitationGapTarget * 0.5) THEN
            rKp_Adaptive := 150.0;
        ELSE
            rKp_Adaptive := 125.5;
        END_IF;
        
        rLevitationControlSignal := (rKp_Adaptive * rLevError) + (rKi_Adaptive * rLevErrorIntegral) + (rKd_Adaptive * rLevErrorDerivative);
        
        (* Current limiter saturation constraint *)
        IF rLevitationControlSignal > MAX_EXCITATION_CURRENT THEN
            rLevitationControlSignal := MAX_EXCITATION_CURRENT;
        ELSIF rLevitationControlSignal < 0.0 THEN
            rLevitationControlSignal := 0.0;
        END_IF;
        
        rLevErrorPrev := rLevError;
        
        (* Verify if levitation gap is within steady-state tolerance (e.g., +/- 0.5 mm) for continuous duration *)
        IF ABS(rLevError) < 0.5 THEN
            tInitTimer(IN := TRUE, PT := T#3S);
            IF tInitTimer.Q THEN
                tInitTimer(IN := FALSE);
                bSystemReady := TRUE;
                iState := 30; (* Transition to MOTOR SYNC & PROPULSION *)
            END_IF;
        ELSE
            tInitTimer(IN := FALSE);
        END_IF;

    30: (* MOTOR SYNC & PROPULSION - MPC INSPIRED TRAJECTORY CONTROL *)
        (* 1. Maintain active levitation control constantly *)
        rLevError := rLevitationGapTarget - rLevitationGapActual;
        rLevErrorIntegral := rLevErrorIntegral + (rLevError * CYCLE_TIME);
        IF rLevErrorIntegral > rIntegralMaxLimit THEN rLevErrorIntegral := rIntegralMaxLimit; END_IF;
        IF rLevErrorIntegral < -rIntegralMaxLimit THEN rLevErrorIntegral := -rIntegralMaxLimit; END_IF;
        
        rLevErrorDerivative := (rLevError - rLevErrorPrev) / CYCLE_TIME;
        rLevitationControlSignal := (rKp_Adaptive * rLevError) + (rKi_Adaptive * rLevErrorIntegral) + (rKd_Adaptive * rLevErrorDerivative);
        IF rLevitationControlSignal > MAX_EXCITATION_CURRENT THEN rLevitationControlSignal := MAX_EXCITATION_CURRENT; END_IF;
        IF rLevitationControlSignal < 0.0 THEN rLevitationControlSignal := 0.0; END_IF;
        rLevErrorPrev := rLevError;

        (* 2. Calculate Linear Motor Thrust with Feedforward Velocity Vectoring *)
        rVelocityError := rTrainVelocityRef - rTrainVelocityAct;
        
        (* Feedforward term modeling aerodynamic drag at high speeds (Drag is proportional to V^2) *)
        rDragCompensation := rAeroCoefficient * rTrainVelocityAct * rTrainVelocityAct;
        
        (* Basic Model Predictive Control logic: Project thrust required to zero velocity error *)
        rThrustFeedforward := rDragCompensation + (25.5 * rVelocityError) + (10.0 * rTrainAccelerationAct);
        
        rMotorThrustCommand := rThrustFeedforward;
        
        (* Enforce Motor Operational Constraints *)
        IF rMotorThrustCommand > MAX_THRUST_KN THEN
            rMotorThrustCommand := MAX_THRUST_KN;
        ELSIF rMotorThrustCommand < -MAX_THRUST_KN THEN
            rMotorThrustCommand := -MAX_THRUST_KN; (* Regenerative electro-dynamic braking regime *)
        END_IF;
        
        (* Graceful degradation trigger *)
        IF NOT bSystemEnable THEN
            iState := 40; (* Transition to CONTROLLED SHUTDOWN *)
        END_IF;

    40: (* CONTROLLED SHUTDOWN: Safe desync and landing *)
        bSystemReady := FALSE;
        rMotorThrustCommand := 0.0; (* Disable propulsion abruptly, rely on friction/aerodynamics or distinct braking subsystem *)
        
        (* Gradually decay levitation excitation current to softly drop the train onto landing skids *)
        rLevitationControlSignal := rLevitationControlSignal * 0.998; 
        IF rLevitationControlSignal < 15.0 THEN
            rLevitationControlSignal := 0.0;
            iState := 0; (* Return to IDLE *)
        END_IF;
        
    999: (* FAULT STATE / EMERGENCY SCRAM *)
        bSystemReady := FALSE;
        rMotorThrustCommand := -MAX_THRUST_KN; (* Apply max regenerative braking torque if possible, else 0 *)
        
        (* Rapidly quench the magnetic field if thermal limits breached, else standard fast decay *)
        IF bThermalWarning THEN
            rLevitationControlSignal := 0.0; (* Hard drop to protect coils from catastrophic quench explosion *)
        ELSE
            rLevitationControlSignal := rLevitationControlSignal * 0.90; (* Fast decay landing *)
        END_IF;
        
        IF (NOT bThermalWarning) AND (bEmergencyStop) AND (NOT bSystemEnable) AND (ABS(rTrainVelocityAct) < 1.0) THEN
            iState := 0; (* Reset only when at standstill and hardware E-Stop is physically cleared *)
        END_IF;

END_CASE;

(* Broadcast internal state for diagnostics / SCADA telemetry *)
iOperatingState := iState;

END_FUNCTION_BLOCK
```"""

import os
os.makedirs("data/swarm_raw", exist_ok=True)
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
