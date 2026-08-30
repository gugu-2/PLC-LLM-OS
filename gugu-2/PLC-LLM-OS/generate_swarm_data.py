import json
import uuid
import os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Robotic MIG Welding Cell.
Task: Invent a highly complex control scenario for this domain (e.g., arc voltage/current synergy tracking, Wire Feed Speed (WFS) pulsing, and 6-axis Tool Center Point (TCP) kinematics).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."""

response = """```iec-st
FUNCTION_BLOCK FB_RoboticMIGWeldingCell
VAR_INPUT
    bEnable : BOOL; // Enable welding cell operations
    bStartWeld : BOOL; // Command to start the welding process
    bEmergencyStop : BOOL; // E-Stop input
    fTargetVoltage : REAL; // Target Arc Voltage (V)
    fTargetCurrent : REAL; // Target Arc Current (A)
    fWireFeedSpeed : REAL; // Target Wire Feed Speed (m/min)
    fTCP_X : REAL; // Target Tool Center Point X coordinate (mm)
    fTCP_Y : REAL; // Target Tool Center Point Y coordinate (mm)
    fTCP_Z : REAL; // Target Tool Center Point Z coordinate (mm)
    fTCP_Rx : REAL; // Target Tool Center Point Rx rotation (deg)
    fTCP_Ry : REAL; // Target Tool Center Point Ry rotation (deg)
    fTCP_Rz : REAL; // Target Tool Center Point Rz rotation (deg)
    bPulseModeEn : BOOL; // Enable pulsing for WFS and current
    fPulseFreq : REAL; // Pulse frequency in Hz
    fPulseDutyCycle : REAL; // Pulse duty cycle (0.0 to 1.0)
END_VAR

VAR_OUTPUT
    bReady : BOOL; // Cell is ready for welding
    bWeldingActive : BOOL; // Welding in progress
    bError : BOOL; // Error active
    iErrorCode : INT; // Error code (0 = no error)
    fActualVoltage : REAL; // Measured Arc Voltage (V)
    fActualCurrent : REAL; // Measured Arc Current (A)
    fActualWFS : REAL; // Measured Wire Feed Speed (m/min)
    fActualGasFlow : REAL; // Measured shielding gas flow (l/min)
    bArcEstablished : BOOL; // Arc establishment confirmation
END_VAR

VAR
    iState : INT := 0; // State machine state
    fbTonPreFlow : TON; // Pre-flow gas timer
    fbTonPostFlow : TON; // Post-flow gas timer
    fbTonArcTimeout : TON; // Arc strike timeout timer
    rPulseTimer : REAL := 0.0; // Internal timer for pulsing logic
    bPulseState : BOOL := FALSE; // High/Low state of the pulse
    
    // Internal kinematic vars
    fCurrentTCP_X : REAL := 0.0;
    fCurrentTCP_Y : REAL := 0.0;
    fCurrentTCP_Z : REAL := 0.0;
    
    // Hardware I/O simulated mapping
    q_bGasValve : BOOL;
    q_bWireFeederEnable : BOOL;
    q_bPowerSourceEnable : BOOL;
    
    // Synergic tracking variables
    fVoltageError : REAL;
    fCurrentError : REAL;
    fWFSError : REAL;
END_VAR

// Main State Machine for Robotic MIG Welding Cell
IF bEmergencyStop THEN
    iState := 99; // Error state
    iErrorCode := 1001; // E-Stop pressed
END_IF;

CASE iState OF
    0: // Init & Wait for Enable
        bReady := FALSE;
        bWeldingActive := FALSE;
        bError := FALSE;
        iErrorCode := 0;
        q_bGasValve := FALSE;
        q_bWireFeederEnable := FALSE;
        q_bPowerSourceEnable := FALSE;
        
        IF bEnable AND NOT bEmergencyStop THEN
            iState := 10;
        END_IF;
        
    10: // Ready State
        bReady := TRUE;
        IF bStartWeld THEN
            bReady := FALSE;
            iState := 20;
        END_IF;
        IF NOT bEnable THEN
            iState := 0;
        END_IF;
        
    20: // Pre-flow gas
        q_bGasValve := TRUE;
        fbTonPreFlow(IN:= TRUE, PT:= T#500MS);
        IF fbTonPreFlow.Q THEN
            fbTonPreFlow(IN:= FALSE);
            iState := 30;
        END_IF;
        
    30: // Arc Strike & Synergic Tracking Initialization
        q_bPowerSourceEnable := TRUE;
        q_bWireFeederEnable := TRUE;
        fbTonArcTimeout(IN:= TRUE, PT:= T#2S);
        
        // Simulating arc establishment logic
        IF (fActualCurrent > 10.0) THEN // Threshold for arc detection
            bArcEstablished := TRUE;
            fbTonArcTimeout(IN:= FALSE);
            iState := 40;
            bWeldingActive := TRUE;
        ELSIF fbTonArcTimeout.Q THEN
            fbTonArcTimeout(IN:= FALSE);
            iState := 99;
            iErrorCode := 2001; // Arc strike failed
        END_IF;
        
    40: // Welding & Synergic Tracking & Pulsing Logic
        IF NOT bStartWeld THEN
            iState := 50; // Transition to stop
        END_IF;
        
        // Pulse logic
        IF bPulseModeEn AND (fPulseFreq > 0.0) THEN
            // Simulation of pulse logic calculation
            rPulseTimer := rPulseTimer + 0.01; // Assuming 10ms cycle time
            IF rPulseTimer >= (1.0 / fPulseFreq) THEN
                rPulseTimer := 0.0;
            END_IF;
            
            bPulseState := (rPulseTimer < (fPulseDutyCycle / fPulseFreq));
            
            IF bPulseState THEN
                fActualVoltage := fTargetVoltage * 1.2;
                fActualCurrent := fTargetCurrent * 1.3;
                fActualWFS := fWireFeedSpeed * 1.5;
            ELSE
                fActualVoltage := fTargetVoltage * 0.8;
                fActualCurrent := fTargetCurrent * 0.5;
                fActualWFS := fWireFeedSpeed * 0.5;
            END_IF;
        ELSE
            // Continuous mode synergic tracking
            fActualVoltage := fTargetVoltage;
            fActualCurrent := fTargetCurrent;
            fActualWFS := fWireFeedSpeed;
        END_IF;
        
        // Kinematic interpolation simulation (6-axis TCP)
        // In a real system, inverse kinematics would map TCP to joint angles
        // Here we track the command values smoothly
        fCurrentTCP_X := fCurrentTCP_X + (fTCP_X - fCurrentTCP_X) * 0.1;
        fCurrentTCP_Y := fCurrentTCP_Y + (fTCP_Y - fCurrentTCP_Y) * 0.1;
        fCurrentTCP_Z := fCurrentTCP_Z + (fTCP_Z - fCurrentTCP_Z) * 0.1;
        
    50: // Stop Welding / Burnback
        bWeldingActive := FALSE;
        bArcEstablished := FALSE;
        q_bWireFeederEnable := FALSE;
        q_bPowerSourceEnable := FALSE;
        iState := 60;
        
    60: // Post-flow gas
        fbTonPostFlow(IN:= TRUE, PT:= T#2S);
        IF fbTonPostFlow.Q THEN
            fbTonPostFlow(IN:= FALSE);
            q_bGasValve := FALSE;
            iState := 10;
        END_IF;
        
    99: // Error State
        bReady := FALSE;
        bWeldingActive := FALSE;
        bError := TRUE;
        q_bGasValve := FALSE;
        q_bWireFeederEnable := FALSE;
        q_bPowerSourceEnable := FALSE;
        
        IF NOT bEmergencyStop AND bEnable THEN // Simple reset condition
            bError := FALSE;
            iErrorCode := 0;
            iState := 0;
        END_IF;
        
END_CASE;
END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": response}]}

os.makedirs("data/swarm_raw", exist_ok=True)
with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)
    
os.makedirs("data", exist_ok=True)
with open("data/synthetic_generation_v3_enterprise.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\\n")
