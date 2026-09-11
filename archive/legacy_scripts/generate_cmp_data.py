import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Chemical Mechanical Polishing (CMP) of Semiconductor Wafers.
Task: Invent a highly complex control scenario for this domain (e.g., polishing pad conditioning downward force, slurry flow rate profiling, and multi-zone wafer carrier rotation).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O.
"""

content = """```iec-st
FUNCTION_BLOCK FB_CMP_ProcessController
TITLE = 'CMP Semiconductor Wafer Advanced Control'
VERSION : '1.0'

VAR_INPUT
    bStartProcess : BOOL; // Start the CMP process
    bEmergencyStop : BOOL; // Emergency stop the entire system
    rTargetRemovalRate : REAL; // Target wafer removal rate (Angstroms/min)
    rWaferThicknessInit : REAL; // Initial thickness measurement
    rCarrierSpeedRPM : REAL; // Wafer carrier rotation speed (RPM)
    rPlatenSpeedRPM : REAL; // Platen rotation speed (RPM)
    rSlurryFlowSetpoint : REAL; // Slurry flow setpoint (ml/min)
    rPadConditionerForce : REAL; // Pad conditioner downward force (N)
    aZonePressures : ARRAY[1..5] OF REAL; // Zone pressures for carrier head
END_VAR

VAR_OUTPUT
    bProcessActive : BOOL; // Process is currently running
    bProcessComplete : BOOL; // Process finished successfully
    bFaultActive : BOOL; // System fault detected
    rCurrentRemovalRate : REAL; // Estimated current removal rate
    rEstimatedThickness : REAL; // Estimated current thickness
    iCurrentStep : INT; // Current process step ID
    sStatusMessage : STRING[50]; // Status message
    
    // Actuator outputs
    rOutCarrierSpeed : REAL; // Command to Carrier VFD
    rOutPlatenSpeed : REAL; // Command to Platen VFD
    rOutSlurryFlow : REAL; // Command to Slurry Pump
    aOutZonePressures : ARRAY[1..5] OF REAL; // Commands to Zone Pressure Regulators
END_VAR

VAR
    rtStartEdge : R_TRIG;
    iState : INT := 0; // State machine variable
    tStepTimer : TON;
    rProcessTime : REAL := 0.0;
    rIntegratedRemoval : REAL := 0.0;
    i : INT;
END_VAR

// Edge detection for start
rtStartEdge(CLK := bStartProcess);

IF bEmergencyStop THEN
    iState := 99; // Fault state
END_IF;

// Main State Machine
CASE iState OF
    0: // Idle State
        bProcessActive := FALSE;
        bProcessComplete := FALSE;
        bFaultActive := FALSE;
        rOutCarrierSpeed := 0.0;
        rOutPlatenSpeed := 0.0;
        rOutSlurryFlow := 0.0;
        sStatusMessage := 'Idle. Ready to start.';
        FOR i := 1 TO 5 DO
            aOutZonePressures[i] := 0.0;
        END_FOR;
        
        IF rtStartEdge.Q THEN
            iState := 10;
            rIntegratedRemoval := 0.0;
            rEstimatedThickness := rWaferThicknessInit;
        END_IF;
        
    10: // Slurry Priming and Pad Conditioning
        bProcessActive := TRUE;
        sStatusMessage := 'Priming Slurry and Conditioning';
        rOutSlurryFlow := rSlurryFlowSetpoint * 1.5; // Flush
        rOutPlatenSpeed := rPlatenSpeedRPM * 0.5;
        tStepTimer(IN := TRUE, PT := T#15S);
        
        IF tStepTimer.Q THEN
            tStepTimer(IN := FALSE);
            iState := 20;
        END_IF;
        
    20: // Main Polishing
        sStatusMessage := 'Main Polishing Active';
        rOutCarrierSpeed := rCarrierSpeedRPM;
        rOutPlatenSpeed := rPlatenSpeedRPM;
        rOutSlurryFlow := rSlurryFlowSetpoint;
        
        // Multi-zone pressure distribution simulation
        FOR i := 1 TO 5 DO
            aOutZonePressures[i] := aZonePressures[i];
        END_FOR;
        
        // Preston's Equation simulation (Removal Rate = K_p * Pressure * Velocity)
        rCurrentRemovalRate := 0.005 * rCarrierSpeedRPM * aZonePressures[3]; 
        rIntegratedRemoval := rIntegratedRemoval + (rCurrentRemovalRate / 60.0);
        rEstimatedThickness := rWaferThicknessInit - rIntegratedRemoval;
        
        IF rEstimatedThickness <= (rWaferThicknessInit - rTargetRemovalRate) THEN
             iState := 30;
        END_IF;
        
    30: // Ramp Down and Cleaning
        sStatusMessage := 'Ramp Down / Clean';
        rOutCarrierSpeed := rCarrierSpeedRPM * 0.2;
        rOutPlatenSpeed := rPlatenSpeedRPM * 0.2;
        rOutSlurryFlow := 0.0;
        FOR i := 1 TO 5 DO
            aOutZonePressures[i] := 0.0;
        END_FOR;
        tStepTimer(IN := TRUE, PT := T#10S);
        
        IF tStepTimer.Q THEN
            tStepTimer(IN := FALSE);
            iState := 40;
        END_IF;
        
    40: // Process Complete
        bProcessActive := FALSE;
        bProcessComplete := TRUE;
        sStatusMessage := 'Process Complete';
        rOutCarrierSpeed := 0.0;
        rOutPlatenSpeed := 0.0;
        
        IF NOT bStartProcess THEN
            iState := 0; // Reset
        END_IF;
        
    99: // Fault state
        bProcessActive := FALSE;
        bFaultActive := TRUE;
        sStatusMessage := 'EMERGENCY STOP / FAULT';
        rOutCarrierSpeed := 0.0;
        rOutPlatenSpeed := 0.0;
        rOutSlurryFlow := 0.0;
        FOR i := 1 TO 5 DO
            aOutZonePressures[i] := 0.0;
        END_FOR;
        
        IF NOT bEmergencyStop AND NOT bStartProcess THEN
            iState := 0; // Requires reset
        END_IF;
END_CASE;

iCurrentStep := iState;

END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": content}]}
os.makedirs("C:/Users/majip/Downloads/LLM REASEARCH/data/swarm_raw", exist_ok=True)
with open(f"C:/Users/majip/Downloads/LLM REASEARCH/data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
    json.dump(record, f)

with open("C:/Users/majip/Downloads/LLM REASEARCH/data/synthetic_generation_v3_enterprise.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\n")
