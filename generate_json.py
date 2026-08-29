import json, uuid, os

code = """```iec-st
FUNCTION_BLOCK FB_LFW_Titanium_Forging_Control
TITLE = 'Linear Friction Welding (LFW) Controller - Titanium Forging'
// Handles high-frequency oscillation profiling, hydraulic axial forge load synchronization, 
// and acoustic emission quality monitoring for aerospace-grade titanium components.
VAR_INPUT
    bEnable                 : BOOL; // Enable the LFW process
    bEmergencyStop          : BOOL; // E-Stop condition
    rTargetFrequency        : REAL; // Target oscillation frequency (Hz)
    rTargetAmplitude        : REAL; // Target oscillation amplitude (mm)
    rForgeForce             : REAL; // Target forge force (kN)
    rBurnOffDistance        : REAL; // Target burn-off distance (mm)
    rAcousticEmissionLimit  : REAL; // Maximum allowable acoustic emission threshold
    rHydraulicPressureIn    : REAL; // Actual hydraulic pressure feedback (Bar)
    rActuatorPosFeedback    : REAL; // Linear actuator position feedback (mm)
    rAcousticSensorIn       : REAL; // Acoustic emission sensor input (mV)
    rSpindleVibration       : REAL; // Spindle vibration monitoring (mm/s)
END_VAR

VAR_OUTPUT
    bSystemReady            : BOOL; // System is ready and homed
    bWeldingActive          : BOOL; // Welding process is currently active
    bProcessComplete        : BOOL; // Welding process completed successfully
    bFault                  : BOOL; // Fault condition present
    iFaultCode              : INT;  // Specific fault code
    rCurrentOscillation     : REAL; // Current oscillation output reference
    rCurrentForgeLoad       : REAL; // Current forge load applied (kN)
    rTotalBurnOff           : REAL; // Measured total burn-off (mm)
END_VAR

VAR
    eState                  : INT := 0; // State machine step
    rOscillatorPhase        : REAL := 0.0;
    rInitialPosition        : REAL := 0.0;
    tProcessTimer           : TON;
    tOscillationRampTimer   : TON;
    tForgeTimer             : TON;
    bAcousticFault          : BOOL := FALSE;
    bHydraulicFault         : BOOL := FALSE;
    
    // Constants for PID Force Control
    Kp_Force                : REAL := 2.5;
    Ki_Force                : REAL := 0.5;
    Kd_Force                : REAL := 0.1;
    rForceError             : REAL := 0.0;
    rForceIntegral          : REAL := 0.0;
    rForceDerivative        : REAL := 0.0;
    rLastError              : REAL := 0.0;
END_VAR

// ==============================================================================
// MAIN CONTROL LOGIC
// ==============================================================================

// Fault Monitoring Task (Runs continuously)
IF bEmergencyStop THEN
    eState := 99; // Jump to fault state
    bFault := TRUE;
    iFaultCode := 1000; // E-Stop pressed
ELSIF rAcousticSensorIn > rAcousticEmissionLimit THEN
    eState := 99;
    bFault := TRUE;
    iFaultCode := 1001; // Acoustic emission limit exceeded (Defect detected)
ELSIF rHydraulicPressureIn < 100.0 AND eState > 1 THEN
    eState := 99;
    bFault := TRUE;
    iFaultCode := 1002; // Loss of hydraulic pressure during cycle
END_IF;

// Main State Machine for LFW Process
CASE eState OF
    0: // Initialization & Ready State
        bSystemReady := NOT bFault AND rHydraulicPressureIn > 150.0;
        bWeldingActive := FALSE;
        bProcessComplete := FALSE;
        rCurrentOscillation := 0.0;
        rCurrentForgeLoad := 0.0;
        
        IF bEnable AND bSystemReady THEN
            rInitialPosition := rActuatorPosFeedback;
            eState := 1; // Transition to Contact phase
        END_IF;
        
    1: // Phase 1: Touchdown & Initial Contact
        bWeldingActive := TRUE;
        rCurrentForgeLoad := 5.0; // Apply small contact force
        
        IF ABS(rHydraulicPressureIn - rCurrentForgeLoad) < 1.0 THEN
            tProcessTimer(IN := TRUE, PT := T#500ms);
            IF tProcessTimer.Q THEN
                tProcessTimer(IN := FALSE);
                eState := 2; // Transition to Conditioning/Friction phase
            END_IF;
        END_IF;
        
    2: // Phase 2: Friction & Heating (Oscillation active)
        tOscillationRampTimer(IN := TRUE, PT := T#2s);
        
        // Calculate Ramp Profile for Amplitude
        IF tOscillationRampTimer.ET < T#2s THEN
            rCurrentOscillation := (TIME_TO_REAL(tOscillationRampTimer.ET) / 2000.0) * rTargetAmplitude;
        ELSE
            rCurrentOscillation := rTargetAmplitude;
        END_IF;
        
        // Oscillation Profile generation (Sine wave simulation for driver)
        rOscillatorPhase := rOscillatorPhase + (rTargetFrequency * 360.0 * 0.001); // Assuming 1ms cycle time
        IF rOscillatorPhase >= 360.0 THEN
            rOscillatorPhase := rOscillatorPhase - 360.0;
        END_IF;
        
        // Maintain Friction Force
        rForceError := (rForgeForce * 0.5) - rHydraulicPressureIn; // Friction force is 50% of forge force
        rForceIntegral := rForceIntegral + rForceError;
        rCurrentForgeLoad := (Kp_Force * rForceError) + (Ki_Force * rForceIntegral);
        
        // Monitor Burn-Off
        rTotalBurnOff := rInitialPosition - rActuatorPosFeedback;
        
        IF rTotalBurnOff >= rBurnOffDistance * 0.8 THEN
            // 80% burn-off reached, transition to Forge phase
            tOscillationRampTimer(IN := FALSE);
            eState := 3; 
        END_IF;
        
    3: // Phase 3: Forging (Zero Oscillation, Max Force)
        rCurrentOscillation := 0.0; // Instantly halt oscillation to align parts
        rOscillatorPhase := 0.0;
        
        // Apply Maximum Forge Force
        rCurrentForgeLoad := rForgeForce;
        
        tForgeTimer(IN := TRUE, PT := T#3s); // Hold forge force for 3 seconds
        
        IF tForgeTimer.Q THEN
            tForgeTimer(IN := FALSE);
            eState := 4; // Complete
        END_IF;
        
    4: // Phase 4: Completion and Retract
        bWeldingActive := FALSE;
        rCurrentForgeLoad := 0.0; // Release pressure
        bProcessComplete := TRUE;
        
        IF NOT bEnable THEN
            eState := 0; // Reset state machine
        END_IF;
        
    99: // Fault State
        bWeldingActive := FALSE;
        rCurrentOscillation := 0.0;
        rCurrentForgeLoad := 0.0;
        
        IF NOT bEnable AND NOT bEmergencyStop THEN
            bFault := FALSE;
            iFaultCode := 0;
            eState := 0;
        END_IF;
        
END_CASE;

END_FUNCTION_BLOCK
```"""

prompt = "You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.\nYour specific domain is: Linear Friction Welding (LFW) Machine.\nTask: Invent a highly complex control scenario for this domain (e.g., high-frequency titanium forging oscillation profiling, hydraulic axial forge load synchronization, and acoustic emission quality monitoring).\nWrite a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O.\n\nCRITICAL RULES:\n1. You MUST output the code enclosed in a ```iec-st markdown code fence. DO NOT APOLOGIZE. DO NOT EXPLAIN.\n2. The code must be >= 1500 chars, with FUNCTION_BLOCK and VAR_INPUT/VAR_OUTPUT."

os.makedirs("c:/Users/majip/Downloads/LLM REASEARCH/data/swarm_raw", exist_ok=True)
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
filename = f"c:/Users/majip/Downloads/LLM REASEARCH/data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f)

print("Saved to", filename)
