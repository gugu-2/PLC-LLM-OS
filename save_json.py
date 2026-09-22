import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V5 Persona: a 60+ years experienced God-Tier PLC Architect & Cyber-Physical Systems Post-Doc. 
Your logic must include advanced State-Space Modeling, Model Predictive Control (MPC) concepts, Non-Linear PID with Anti-Windup, and extreme multi-layer hardware safety matrices. Output the most elite, mathematically rigorous, and structurally flawless IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Advanced Semiconductor 300mm Wafer Plasma-Enhanced Chemical Vapor Deposition (PECVD) RF Matching Network and Gas Precursor Flow**

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
   code = \"\"\"```iec-st\nFUNCTION_BLOCK FB_PECVD_RFMatchingNetwork\n//...\nEND_FUNCTION_BLOCK\n```\"\"\"
   record = {\"messages\": [{\"role\": \"user\", \"content\": prompt}, {\"role\": \"assistant\", \"content\": code}]}
   with open(f\"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json\", \"w\", encoding=\"utf-8\") as f:
       json.dump(record, f, ensure_ascii=False)
5. SELF-CHECK before saving - verify ALL:
   [ ] Fence is ```iec-st
   [ ] First code line: FUNCTION_BLOCK FB_<name>
   [ ] Has VAR_INPUT & VAR_OUTPUT sections
   [ ] Has END_IF; or END_CASE;
   [ ] Last code line: END_FUNCTION_BLOCK
   [ ] Closing fence: ```
   [ ] Total chars >= 2500
6. REPLY with: EVOLUTION COMPLETE: Advanced Semiconductor 300mm Wafer Plasma-Enhanced Chemical Vapor Deposition (PECVD) RF Matching Network and Gas Precursor Flow"""

code = """```iec-st
FUNCTION_BLOCK FB_PECVD_AdvancedRFMatch_GasPrecursorControl
TITLE = '300mm PECVD RF Match & MPC Gas Flow Controller'
// ==============================================================================
// AUTHOR: Lumina AI Cloud Swarm - V5 Persona (God-Tier PLC Architect)
// DOMAIN: Advanced Semiconductor 300mm Wafer PECVD
// DESCRIPTION: State-Space Modeling based RF matching network combined with 
// Model Predictive Control (MPC) for precursor gas flow delivery.
// Includes extreme safety matrices, non-linear PID with anti-windup.
// ==============================================================================
VAR_INPUT
    bEnable                 : BOOL;   // System Master Enable
    bEmergencyStop          : BOOL;   // Safety Relay OK Signal (Hardware Interlock)
    rRF_ForwardPower        : REAL;   // Measured Forward RF Power (Watts)
    rRF_ReflectedPower      : REAL;   // Measured Reflected RF Power (Watts)
    rChamberPressure        : REAL;   // Chamber Pressure Measurement (mTorr)
    rPrecursorMassFlow      : REAL;   // Silane/TEOS Precursor Flow (sccm)
    rPlasmaImpedancePhase   : REAL;   // VI Probe Phase Angle (Degrees)
    rPlasmaImpedanceMag     : REAL;   // VI Probe Magnitude (Ohms)
    rWaferTemperature       : REAL;   // Susceptor Temperature (Deg C)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;   // Overall System Ready State
    bPlasmaIgnited          : BOOL;   // Plasma Strike Confirmation
    rTuningMotorCmd         : REAL;   // Command to Vacuum Tuning Capacitor (0-100%)
    rLoadMotorCmd           : REAL;   // Command to Vacuum Load Capacitor (0-100%)
    rMFC_ValveCmd           : REAL;   // Mass Flow Controller Valve Command (0-10V)
    bRFGeneratorEnable      : BOOL;   // Enable signal to 13.56 MHz RF Generator
    bAlarmStatus            : BOOL;   // Global Fault Indicator
    iErrorCode              : INT;    // High-Resolution Diagnostic Error Code
END_VAR
VAR
    // Internal State Machine
    iState                  : INT := 0; // 0=IDLE, 10=PURGE, 20=STRIKE, 30=TUNE, 40=PROCESS, 99=FAULT
    
    // Timers
    tPurgeTimer             : TON;
    tStrikeTimeout          : TON;
    tProcessTimer           : TON;
    
    // RF Tuning Non-Linear PID Parameters
    rTuneKp                 : REAL := 0.25;
    rTuneKi                 : REAL := 0.05;
    rTuneKd                 : REAL := 0.01;
    rTuneError              : REAL;
    rTuneLastError          : REAL;
    rTuneIntegral           : REAL;
    rTuneDerivative         : REAL;
    
    // Gas Precursor MPC Variables (Simplified State-Space)
    rGasTargetFlow          : REAL := 500.0; // sccm target
    rGasFlowError           : REAL;
    rPredictedFlow          : REAL;
    rStateX1                : REAL := 0.0;
    rStateX2                : REAL := 0.0;
    
    // Safety Matrix Flags
    bReflectedPowerHigh     : BOOL;
    bPressureDeviation      : BOOL;
    bThermalRunaway         : BOOL;
    
    // Constants
    rMAX_REFLECTED_POWER    : REAL := 50.0;   // Maximum allowed reflected power (Watts)
    rMAX_PRESSURE           : REAL := 2000.0; // Max allowed pressure (mTorr)
    rMIN_PRESSURE           : REAL := 10.0;   // Min required pressure for strike (mTorr)
    rIMPEDANCE_SETPOINT_MAG : REAL := 50.0;   // Target 50 Ohms match
    rIMPEDANCE_SETPOINT_PHA : REAL := 0.0;    // Target 0 Phase angle
END_VAR

// ==============================================================================
// SAFETY MATRIX & HARDWARE INTERLOCKS (Layer 1)
// ==============================================================================
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bRFGeneratorEnable := FALSE;
    rMFC_ValveCmd := 0.0;
    rTuningMotorCmd := 0.0;
    rLoadMotorCmd := 0.0;
    bPlasmaIgnited := FALSE;
    bAlarmStatus := TRUE;
    iErrorCode := 9999; // Critical Hardware E-Stop
    iState := 99;
    RETURN;
END_IF;

// Advanced Diagnostics & Operational Boundaries (Layer 2)
bReflectedPowerHigh := (rRF_ReflectedPower > rMAX_REFLECTED_POWER);
bPressureDeviation := (rChamberPressure > rMAX_PRESSURE) OR (rChamberPressure < rMIN_PRESSURE);
bThermalRunaway := (rWaferTemperature > 650.0); // Extreme limit for PECVD

IF bReflectedPowerHigh OR bPressureDeviation OR bThermalRunaway THEN
    bRFGeneratorEnable := FALSE;
    bAlarmStatus := TRUE;
    IF bReflectedPowerHigh THEN iErrorCode := 1001; END_IF;
    IF bPressureDeviation THEN iErrorCode := 1002; END_IF;
    IF bThermalRunaway THEN iErrorCode := 1003; END_IF;
    iState := 99; // Transition to FAULT
END_IF;

// ==============================================================================
// ADVANCED STATE-SPACE MACHINE (Layer 3)
// ==============================================================================
CASE iState OF
    0: // IDLE STATE
        bSystemReady := TRUE;
        bAlarmStatus := FALSE;
        iErrorCode := 0;
        bRFGeneratorEnable := FALSE;
        bPlasmaIgnited := FALSE;
        
        // Wait for Master Enable
        IF bEnable THEN
            iState := 10;
            bSystemReady := FALSE; // In transition
        END_IF;

    10: // PURGE & PRECONDITIONING
        // MPC Model Initialization for Gas Delivery
        rStateX1 := 0.0; 
        rStateX2 := 0.0;
        rMFC_ValveCmd := 1.5; // Purge flow base setting
        
        tPurgeTimer(IN := TRUE, PT := T#10S);
        IF tPurgeTimer.Q THEN
            tPurgeTimer(IN := FALSE);
            iState := 20; // Move to Strike
        END_IF;

    20: // PLASMA IGNITION (STRIKE)
        rMFC_ValveCmd := 4.5; // Strike pressure/flow setting
        
        // Set initial capacitor positions for strike condition
        rTuningMotorCmd := 45.0; // 45% based on empirical data
        rLoadMotorCmd := 60.0;   // 60% load
        
        bRFGeneratorEnable := TRUE; // Enable 13.56MHz
        tStrikeTimeout(IN := TRUE, PT := T#2S);
        
        // Strike confirmation based on Impedance collapse & Forward Power jump
        IF (rPlasmaImpedanceMag < 1000.0) AND (rRF_ForwardPower > 50.0) THEN
            bPlasmaIgnited := TRUE;
            tStrikeTimeout(IN := FALSE);
            iState := 30; // Move to Tuning
        ELSIF tStrikeTimeout.Q THEN
            // Strike Failed
            tStrikeTimeout(IN := FALSE);
            bRFGeneratorEnable := FALSE;
            bAlarmStatus := TRUE;
            iErrorCode := 2001; // Plasma Strike Failure
            iState := 99;
        END_IF;

    30: // DYNAMIC RF MATCHING & NON-LINEAR PID
        // Vector calculation based on Smith Chart mechanics (simplified for ST)
        // Error is calculated off the 50 Ohm + 0 Phase ideal point
        rTuneError := rIMPEDANCE_SETPOINT_PHA - rPlasmaImpedancePhase;
        
        // Non-Linear Gain Scheduling based on error magnitude
        IF ABS(rTuneError) > 45.0 THEN
            rTuneKp := 0.8; // Aggressive tuning
        ELSE
            rTuneKp := 0.2; // Fine tuning
        END_IF;

        // PID Anti-Windup Logic
        IF (rTuningMotorCmd < 100.0) AND (rTuningMotorCmd > 0.0) THEN
            rTuneIntegral := rTuneIntegral + (rTuneError * 0.01);
        END_IF;
        
        rTuneDerivative := (rTuneError - rTuneLastError) / 0.01;
        
        // Compute Output Commands for Caps
        rTuningMotorCmd := rTuningMotorCmd + (rTuneKp * rTuneError) + (rTuneKi * rTuneIntegral) + (rTuneKd * rTuneDerivative);
        
        // Limit Bounds
        IF rTuningMotorCmd > 100.0 THEN rTuningMotorCmd := 100.0; END_IF;
        IF rTuningMotorCmd < 0.0 THEN rTuningMotorCmd := 0.0; END_IF;
        
        rTuneLastError := rTuneError;
        
        // Matching Convergence Criteria
        IF (ABS(rTuneError) < 2.0) AND (rRF_ReflectedPower < 5.0) THEN
            iState := 40; // Matched, enter process mode
        END_IF;

    40: // STEADY STATE DEPOSITION (MPC GAS FLOW CONTROL)
        tProcessTimer(IN := TRUE, PT := T#300S); // 5 minute deposition
        
        // Simplified Model Predictive Control step for Mass Flow
        // State Update: x(k+1) = A*x(k) + B*u(k)
        rStateX1 := (0.9 * rStateX1) + (0.1 * rPrecursorMassFlow);
        rStateX2 := (0.8 * rStateX2) + (0.2 * rMFC_ValveCmd);
        
        // Predict future output & calculate control horizon
        rPredictedFlow := (1.5 * rStateX1) - (0.5 * rStateX2);
        rGasFlowError := rGasTargetFlow - rPredictedFlow;
        
        // MPC corrective action (Receding Horizon proxy)
        rMFC_ValveCmd := rMFC_ValveCmd + (0.015 * rGasFlowError);
        
        // Clamp MFC Output
        IF rMFC_ValveCmd > 10.0 THEN rMFC_ValveCmd := 10.0; END_IF;
        IF rMFC_ValveCmd < 0.0 THEN rMFC_ValveCmd := 0.0; END_IF;
        
        // Keep matching network active with low gain
        rTuneKp := 0.05; 
        rTuningMotorCmd := rTuningMotorCmd + (rTuneKp * (rIMPEDANCE_SETPOINT_PHA - rPlasmaImpedancePhase));
        
        IF tProcessTimer.Q THEN
            // Deposition Complete
            tProcessTimer(IN := FALSE);
            iState := 0; // Normal Shutdown
            bEnable := FALSE;
        END_IF;

    99: // SYSTEM FAULT & SAFE SHUTDOWN
        bRFGeneratorEnable := FALSE;
        rMFC_ValveCmd := 0.0;
        bPlasmaIgnited := FALSE;
        bSystemReady := FALSE;
        
        IF NOT bEnable AND NOT bAlarmStatus THEN
            // Fault reset logic
            iState := 0;
        END_IF;
        
END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
