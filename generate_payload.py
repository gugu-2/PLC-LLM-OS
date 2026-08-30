import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Battery Tab Ultrasonic Welding.
Task: Invent a highly complex control scenario for this domain (e.g., sonotrode acoustic amplitude resonance profiling, anvil clamping force servo control, and contact resistance weld verification).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O.
"""

code = """```iec-st
FUNCTION_BLOCK FB_UltrasonicWeldingControl
VAR_INPUT
    bStartWeld          : BOOL;  // Initiate welding cycle
    bEmergencyStop      : BOOL;  // Emergency stop condition
    rTargetForce_N      : REAL;  // Target anvil clamping force in Newtons
    rWeldAmplitude_um   : REAL;  // Target ultrasonic amplitude in micrometers
    tWeldTime           : TIME;  // Duration of ultrasonic energy application
    tHoldTime           : TIME;  // Cooling/holding time post-weld
    rMaxResonanceError  : REAL;  // Maximum allowed deviation in acoustic resonance
    rMaxContactRes_mOhm : REAL;  // Maximum permissible post-weld contact resistance
END_VAR

VAR_OUTPUT
    bWeldComplete       : BOOL;  // Weld cycle finished successfully
    bWeldFailed         : BOOL;  // Weld cycle failed
    sFailureReason      : STRING(255); // Description of failure
    rFinalForce_N       : REAL;  // Achieved clamping force
    rFinalRes_mOhm      : REAL;  // Measured contact resistance
END_VAR

VAR
    // Physical I/O Mappings (Simulated via VAR)
    rActualForce_N       AT %IW100 : REAL;  // Load cell feedback
    rAcousticFreq_Hz     AT %IW102 : REAL;  // Sonotrode frequency feedback
    rAcousticAmp_um      AT %IW104 : REAL;  // Sonotrode amplitude feedback
    rMeasuredRes_mOhm    AT %IW106 : REAL;  // Post-weld micro-ohmmeter reading
    
    bServoEnable         AT %QX10.0 : BOOL; // Enable clamping servo
    rServoForceCmd       AT %QW110 : REAL;  // Command to clamping servo
    bGeneratorEnable     AT %QX10.1 : BOOL; // Enable ultrasonic generator
    rGeneratorAmpCmd     AT %QW112 : REAL;  // Amplitude command to generator
    bMeasureRes          AT %QX10.2 : BOOL; // Trigger resistance measurement
    
    // Internal State Machine
    eState : (
        STATE_IDLE,
        STATE_CLAMPING,
        STATE_RESONANCE_PROFILING,
        STATE_WELDING,
        STATE_HOLDING,
        STATE_VERIFICATION,
        STATE_RETRACTING,
        STATE_ERROR
    );
    
    WeldTimer : TON;
    HoldTimer : TON;
    ClampTimer : TON;
    
    rFreqDeviation : REAL;
    rTargetFreq_Hz : REAL := 20000.0; // Nominal 20kHz
END_VAR

// State Machine Execution
IF bEmergencyStop THEN
    bServoEnable := FALSE;
    bGeneratorEnable := FALSE;
    rServoForceCmd := 0.0;
    rGeneratorAmpCmd := 0.0;
    eState := STATE_ERROR;
    sFailureReason := 'Emergency Stop Triggered';
END_IF;

CASE eState OF
    STATE_IDLE:
        bWeldComplete := FALSE;
        bWeldFailed := FALSE;
        sFailureReason := '';
        bServoEnable := FALSE;
        bGeneratorEnable := FALSE;
        bMeasureRes := FALSE;
        
        IF bStartWeld AND NOT bEmergencyStop THEN
            bServoEnable := TRUE;
            rServoForceCmd := rTargetForce_N;
            ClampTimer(IN:=FALSE);
            eState := STATE_CLAMPING;
        END_IF;
        
    STATE_CLAMPING:
        ClampTimer(IN:=TRUE, PT:=T#2S);
        // Closed-loop check for target force
        IF ABS(rActualForce_N - rTargetForce_N) < (rTargetForce_N * 0.05) THEN
            eState := STATE_RESONANCE_PROFILING;
        ELSIF ClampTimer.Q THEN
            eState := STATE_ERROR;
            sFailureReason := 'Clamping timeout - target force not reached';
        END_IF;
        
    STATE_RESONANCE_PROFILING:
        // Briefly enable generator at low amplitude to check resonance
        bGeneratorEnable := TRUE;
        rGeneratorAmpCmd := rWeldAmplitude_um * 0.1; // 10% amplitude for profiling
        
        rFreqDeviation := ABS(rAcousticFreq_Hz - rTargetFreq_Hz);
        IF rFreqDeviation > rMaxResonanceError THEN
            bGeneratorEnable := FALSE;
            eState := STATE_ERROR;
            sFailureReason := 'Acoustic resonance deviation exceeds tolerance';
        ELSE
            WeldTimer(IN:=FALSE);
            eState := STATE_WELDING;
        END_IF;
        
    STATE_WELDING:
        bGeneratorEnable := TRUE;
        rGeneratorAmpCmd := rWeldAmplitude_um;
        WeldTimer(IN:=TRUE, PT:=tWeldTime);
        
        IF WeldTimer.Q THEN
            bGeneratorEnable := FALSE;
            rGeneratorAmpCmd := 0.0;
            HoldTimer(IN:=FALSE);
            eState := STATE_HOLDING;
        END_IF;
        
        // Monitor clamping force dynamically during phase transition
        IF ABS(rActualForce_N - rTargetForce_N) > (rTargetForce_N * 0.1) THEN
            bGeneratorEnable := FALSE;
            eState := STATE_ERROR;
            sFailureReason := 'Force tracking error during weld phase';
        END_IF;
        
    STATE_HOLDING:
        // Hold force to allow melt cooling and consolidation
        HoldTimer(IN:=TRUE, PT:=tHoldTime);
        IF HoldTimer.Q THEN
            bMeasureRes := TRUE;
            eState := STATE_VERIFICATION;
        END_IF;
        
    STATE_VERIFICATION:
        // Await contact resistance measurement stabilization
        // In a real application, we might use a small delay here
        rFinalRes_mOhm := rMeasuredRes_mOhm;
        bMeasureRes := FALSE;
        
        IF rFinalRes_mOhm > rMaxContactRes_mOhm THEN
            eState := STATE_ERROR;
            sFailureReason := 'Contact resistance exceeds maximum threshold';
        ELSE
            rServoForceCmd := 0.0; // Release clamp
            eState := STATE_RETRACTING;
        END_IF;
        
    STATE_RETRACTING:
        // Wait for anvil to retract
        IF rActualForce_N < 5.0 THEN
            bServoEnable := FALSE;
            rFinalForce_N := rActualForce_N;
            bWeldComplete := TRUE;
            eState := STATE_IDLE;
        END_IF;
        
    STATE_ERROR:
        bWeldFailed := TRUE;
        bServoEnable := FALSE;
        bGeneratorEnable := FALSE;
        bMeasureRes := FALSE;
        IF NOT bStartWeld THEN
            eState := STATE_IDLE;
        END_IF;
        
END_CASE;
END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}

os.makedirs("data/swarm_raw", exist_ok=True)
with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)
