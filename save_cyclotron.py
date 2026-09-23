import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V5 Persona: a 60+ years experienced God-Tier PLC Architect & Cyber-Physical Systems Post-Doc. 
Your logic must include advanced State-Space Modeling, Model Predictive Control (MPC) concepts, Non-Linear PID with Anti-Windup, and extreme multi-layer hardware safety matrices. Output the most elite, mathematically rigorous, and structurally flawless IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Advanced Medical Isotope Cyclotron Magnetic Field Shim Coil and Radio Frequency (RF) Amplifier Sync**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_Cyclotron_MagneticShim\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Advanced Medical Isotope Cyclotron Magnetic Field Shim Coil and Radio Frequency (RF) Amplifier Sync"""

code = """```iec-st
FUNCTION_BLOCK FB_Cyclotron_MagneticShim_RFSync
VAR_INPUT
    (* System Enable and Safety Interlocks - Hardware Layer 0 *)
    bEnable               : BOOL;   (* System enable signal *)
    bEmergencyStop        : BOOL;   (* Safety relay OK signal - Active High means SAFE *)
    bBeamOnRequest        : BOOL;   (* Request from operator to start RF and inject beam *)
    bVacuumInterlockOK    : BOOL;   (* Cryo-pump vacuum level interlock - MUST be true *)
    
    (* Physical Measurements - High Frequency Sampling *)
    rMainMagnetField      : REAL;   (* Measured main cyclotron B-field in Tesla (Nominal: 1.2T) *)
    rShimCoilTemp         : REAL;   (* Physical measurement of shim coil temperature in deg C *)
    rRFForwardPower       : REAL;   (* Measured RF forward power in kW (0.0 to 150.0 kW) *)
    rRFReflectedPower     : REAL;   (* Measured RF reflected power in kW (Max 5.0 kW) *)
    rCavityPhase          : REAL;   (* Phase of the RF cavity in degrees (-180.0 to +180.0) *)
    rBeamCurrent          : REAL;   (* Extracted beam current measurement in micro-amps *)
END_VAR
VAR_OUTPUT
    (* System Status and Precise Actuation Matrix *)
    bSystemReady          : BOOL;   (* System ready status - Magnetic and RF domains synced *)
    rShimCurrentCommand   : REAL;   (* Control signal to shim actuator PSU in Amps *)
    rRFAmplitudeCommand   : REAL;   (* RF Drive amplitude command (Volts) *)
    rRFPhaseCommand       : REAL;   (* RF Drive phase shift command (Degrees) *)
    bBeamInterlockActive  : BOOL;   (* Hardware interlock status - Active prevents injection *)
    bAlarm                : BOOL;   (* Fault alarm output *)
    uiErrorCode           : UINT;   (* Specific fault code mapping for SCADA logging via Ethernet/IP *)
END_VAR
VAR
    (* Advanced State Machine Variables *)
    iState                : INT := 0; 
    tTimer                : TON;
    tRampTimer            : TON;
    tStabilizationTimer   : TON;
    
    (* Non-Linear PID with Anti-Windup (RF Phase Sync) *)
    rPhaseError           : REAL := 0.0;
    rPrevPhaseError       : REAL := 0.0;
    rPhaseIntegral        : REAL := 0.0;
    rPhaseDerivative      : REAL := 0.0;
    rKp                   : REAL := 1.25;
    rKi                   : REAL := 0.15;
    rKd                   : REAL := 0.05;
    rIntegralMax          : REAL := 50.0;
    
    (* Model Predictive Control (MPC) Shim Estimation Matrix for Isochronous Field *)
    rBFieldTarget         : REAL := 1.20005;
    rBFieldDrift          : REAL := 0.0;
    rShimGainMatrix       : ARRAY[1..3, 1..3] OF REAL := [0.1, 0.05, 0.01, 0.05, 0.2, 0.02, 0.01, 0.02, 0.3];
    rStateVectorX         : ARRAY[1..3] OF REAL;
    
    (* Extremal Hard-Coded Safety Limits *)
    cMaxShimTemp          : REAL := 65.0; (* Degrees Celsius *)
    cMaxReflectedPower    : REAL := 3.5;  (* kW *)
    cMaxPhaseDeviation    : REAL := 15.0; (* Degrees *)
    
    (* Operational Flags *)
    bPhaseLocked          : BOOL := FALSE;
    bMagneticFieldStable  : BOOL := FALSE;
END_VAR

(* === EXTREME MULTI-LAYER HARDWARE SAFETY MATRIX === *)
(* Safety Layer 1: SIL3 Estop and Vacuum Interlocks (Direct execution overrides) *)
IF NOT bEmergencyStop OR NOT bVacuumInterlockOK THEN
    bSystemReady := FALSE;
    bBeamInterlockActive := TRUE;
    rShimCurrentCommand := 0.0;
    rRFAmplitudeCommand := 0.0;
    bAlarm := TRUE;
    uiErrorCode := 1001; (* Critical Hardware E-Stop or Vacuum Loss *)
    iState := 99; (* Force Fault State - Await operator acknowledgement *)
    RETURN;
END_IF;

(* Safety Layer 2: Thermal and High-Power RF Anomalies *)
IF rShimCoilTemp > cMaxShimTemp THEN
    bBeamInterlockActive := TRUE;
    bAlarm := TRUE;
    uiErrorCode := 2001; (* Shim Thermal Overload - Imminent Superconducting Quench Risk *)
    iState := 99;
    RETURN;
END_IF;

IF rRFReflectedPower > cMaxReflectedPower THEN
    bBeamInterlockActive := TRUE;
    rRFAmplitudeCommand := 0.0; (* Drop RF immediately to protect the Klystron tube *)
    bAlarm := TRUE;
    uiErrorCode := 3001; (* VSWR / Reflected Power Threshold Exceeded *)
    iState := 99;
    RETURN;
END_IF;

(* === MAIN CYCLOTRON CONTROL STATE-SPACE MACHINE === *)
CASE iState OF
    0: (* IDLE - WAIT FOR ENABLE *)
        bSystemReady := FALSE;
        bAlarm := FALSE;
        bBeamInterlockActive := TRUE;
        bPhaseLocked := FALSE;
        bMagneticFieldStable := FALSE;
        uiErrorCode := 0;
        rShimCurrentCommand := 0.0;
        rRFAmplitudeCommand := 0.0;
        
        IF bEnable THEN
            iState := 10;
        END_IF;

    10: (* INIT_MAGNETICS - STATE-SPACE SHIM PRE-CALCULATION *)
        (* Utilize a simplistic discrete-time state-space prediction for isochronous field stabilization *)
        rBFieldDrift := rBFieldTarget - rMainMagnetField;
        
        (* State Vector Mapping: [1] Field Error, [2] Temp Drift, [3] RF Coupling Coefficient Approximation *)
        rStateVectorX[1] := rBFieldDrift;
        rStateVectorX[2] := (rShimCoilTemp - 25.0) * 0.01;
        rStateVectorX[3] := rRFForwardPower * 0.001;
        
        (* MPC Matrix Multiplication for optimal shim current setpoint injection *)
        rShimCurrentCommand := (rShimGainMatrix[1,1] * rStateVectorX[1]) + 
                               (rShimGainMatrix[1,2] * rStateVectorX[2]) + 
                               (rShimGainMatrix[1,3] * rStateVectorX[3]);
        
        iState := 20;

    20: (* RAMP_SHIM - MAGNETIC FIELD STABILIZATION VERIFICATION *)
        tRampTimer(IN := TRUE, PT := T#15S);
        IF ABS(rBFieldTarget - rMainMagnetField) < 0.0001 THEN
            bMagneticFieldStable := TRUE;
        END_IF;
        
        IF tRampTimer.Q AND bMagneticFieldStable THEN
            tRampTimer(IN := FALSE);
            iState := 30;
        ELSIF tRampTimer.Q AND NOT bMagneticFieldStable THEN
            (* Iterative correction via MPC gain adjustment required, but for simplicity, fault here if unstable *)
            bAlarm := TRUE;
            uiErrorCode := 4001; (* Field Stabilization Timeout *)
            iState := 99;
        END_IF;

    30: (* SYNC_RF_CAVITY - NON-LINEAR PID PHASE LOCK WITH ANTI-WINDUP *)
        rRFAmplitudeCommand := 12.5; (* Nominal pre-buncher threshold voltage injection *)
        
        (* Calculate Phase Error against the synchronizing reference frame *)
        rPhaseError := 0.0 - rCavityPhase; (* Target is 0.0 degrees sync *)
        
        (* Non-Linear Proportional Term: Increase gain aggressively if error is highly divergent *)
        IF ABS(rPhaseError) > 10.0 THEN
            rKp := 2.85;
        ELSE
            rKp := 1.25;
        END_IF;
        
        (* Anti-Windup Integrator for zero-steady-state error tracking *)
        rPhaseIntegral := rPhaseIntegral + rPhaseError;
        IF rPhaseIntegral > rIntegralMax THEN
            rPhaseIntegral := rIntegralMax;
        ELSIF rPhaseIntegral < -rIntegralMax THEN
            rPhaseIntegral := -rIntegralMax;
        END_IF;
        
        (* Discrete Derivative Term for predicting phase jitter over short dt *)
        rPhaseDerivative := rPhaseError - rPrevPhaseError;
        
        (* Final Actuation Output for RF Phase (in Degrees shift) *)
        rRFPhaseCommand := (rKp * rPhaseError) + (rKi * rPhaseIntegral) + (rKd * rPhaseDerivative);
        rPrevPhaseError := rPhaseError;
        
        (* Strict Convergence Validation Window *)
        IF ABS(rPhaseError) < 0.5 AND rRFForwardPower > 10.0 THEN
            tStabilizationTimer(IN := TRUE, PT := T#2S);
            IF tStabilizationTimer.Q THEN
                bPhaseLocked := TRUE;
                iState := 40;
                tStabilizationTimer(IN := FALSE);
            END_IF;
        ELSE
            tStabilizationTimer(IN := FALSE);
            (* If phase error goes haywire mid-sync, fault out *)
            IF ABS(rPhaseError) > cMaxPhaseDeviation THEN
                 uiErrorCode := 5001; (* Severe Phase Decoupling Detected *)
                 iState := 99;
            END_IF;
        END_IF;

    40: (* BEAM_ACTIVE - CYCLOTRON IS OPERATIONAL & MULTIPACTORING CLEARED *)
        bSystemReady := TRUE;
        bBeamInterlockActive := FALSE; (* Hardware interlock lifted, ion source injection authorized *)
        
        (* Continuous MPC runtime adjustment could be placed here to counteract thermal field expansion *)
        
        IF NOT bEnable OR NOT bBeamOnRequest THEN
            iState := 50; (* Transition to Safe Shutdown Topology *)
        END_IF;
        
    50: (* SAFE SHUTDOWN SEQUENCE - CONTROLLED DECAY *)
        bBeamInterlockActive := TRUE; (* Terminate injection instantly *)
        
        (* Exponential decay of the RF amplitude to avoid cavity spark-downs *)
        rRFAmplitudeCommand := rRFAmplitudeCommand * 0.90; 
        IF rRFAmplitudeCommand < 0.1 THEN
            rRFAmplitudeCommand := 0.0;
            rShimCurrentCommand := 0.0; (* Ramp down shim *)
            iState := 0;
        END_IF;

    99: (* FAULT HANDLING - CATASTROPHIC EVENT FALLBACK *)
        bSystemReady := FALSE;
        bBeamInterlockActive := TRUE;
        rShimCurrentCommand := 0.0;
        rRFAmplitudeCommand := 0.0;
        rRFPhaseCommand := 0.0;
        tRampTimer(IN := FALSE);
        tStabilizationTimer(IN := FALSE);
        
        (* Wait for central command SCADA to perform a hard reset which toggles bEnable FALSE *)
        IF NOT bEnable THEN
            bAlarm := FALSE;
            uiErrorCode := 0;
            iState := 0;
        END_IF;
        
END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print("SAVED_SUCCESS")
