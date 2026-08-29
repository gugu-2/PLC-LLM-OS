import json, uuid, os

iec_code = """```iec-st
FUNCTION_BLOCK FB_EggGradingControl
TITLE = 'Commercial Egg Grading and Sorting Facility Control'
VERSION : '2.1'
AUTHOR : 'Lumina Elite Synthetic Data Architect'

VAR_INPUT
    xEnableSys : BOOL; // System enable command
    xResetFault : BOOL; // Reset system faults
    rConveyorSpeed : REAL; // Multi-lane conveyor speed target (mm/s)
    
    // Acoustic Sensor Inputs (Crack Detection)
    aResonanceFreqs : ARRAY[1..12] OF REAL; // Acoustic resonance frequencies from 12 lanes
    aAcousticAmps : ARRAY[1..12] OF REAL; // Amplitude of the acoustic response
    
    // Vision System Inputs (Candling)
    aVisionBlobs : ARRAY[1..12] OF INT; // Number of dark spots detected by candling vision
    aYolkCentering : ARRAY[1..12] OF REAL; // Yolk centering deviation (mm)
    aVisionReady : ARRAY[1..12] OF BOOL; // Vision system ready trigger
    
    // Load Cell Inputs (Weighing)
    aEggWeights : ARRAY[1..12] OF REAL; // Measured weight (grams)
END_VAR

VAR_OUTPUT
    xSysRunning : BOOL;
    xFaultActive : BOOL;
    iSysState : INT; // 0=IDLE, 1=RUNNING, 2=FAULT
    rActualSpeed : REAL; // Feedback speed
    
    // Rejection and Sorting Outputs
    aRejectCrack : ARRAY[1..12] OF BOOL; // Reject due to shell crack
    aRejectBlood : ARRAY[1..12] OF BOOL; // Reject due to blood spots (candling)
    aSortGrade : ARRAY[1..12] OF INT; // 1=Jumbo, 2=XL, 3=L, 4=M, 5=S, 6=Peewee, 0=Reject
    
    aEjectorTriggers : ARRAY[1..12] OF BOOL; // Synchronization triggers for pneumatic ejectors
END_VAR

VAR
    // Tuning Parameters
    rCrackResonanceLimitHigh : REAL := 4500.0; // Hz
    rCrackResonanceLimitLow : REAL := 3800.0; // Hz
    rBloodSpotThreshold : INT := 3;
    rYolkDeviationLimit : REAL := 5.0; // mm
    
    // State Tracking
    aProcessingStep : ARRAY[1..12] OF INT;
    tSyncTimers : ARRAY[1..12] OF TON;
    tEjectorPulse : ARRAY[1..12] OF TP;
    
    i : INT; // Loop index
    rTempWeight : REAL;
END_VAR

// Control Logic
IF xResetFault THEN
    xFaultActive := FALSE;
    iSysState := 0;
END_IF;

IF NOT xEnableSys THEN
    xSysRunning := FALSE;
    iSysState := 0;
    rActualSpeed := 0.0;
    FOR i := 1 TO 12 DO
        aRejectCrack[i] := FALSE;
        aRejectBlood[i] := FALSE;
        aSortGrade[i] := 0;
        aEjectorTriggers[i] := FALSE;
    END_FOR;
    RETURN;
END_IF;

IF xFaultActive THEN
    xSysRunning := FALSE;
    iSysState := 2;
    rActualSpeed := 0.0;
    RETURN;
END_IF;

// System is running normally
xSysRunning := TRUE;
iSysState := 1;
rActualSpeed := rConveyorSpeed; // Simulated perfect speed tracking

// High-speed multi-lane grading loop
FOR i := 1 TO 12 DO
    
    // 1. Acoustic Crack Detection Resonance Analysis
    IF aResonanceFreqs[i] < rCrackResonanceLimitLow OR aResonanceFreqs[i] > rCrackResonanceLimitHigh THEN
        // Intact eggs resonate within a specific frequency band.
        aRejectCrack[i] := TRUE;
    ELSE
        // Amplitude check for micro-cracks
        IF aAcousticAmps[i] < 10.0 THEN
            aRejectCrack[i] := TRUE;
        ELSE
            aRejectCrack[i] := FALSE;
        END_IF;
    END_IF;
    
    // 2. Candling Vision Rejection Synchronization
    IF aVisionReady[i] THEN
        IF aVisionBlobs[i] >= rBloodSpotThreshold OR aYolkCentering[i] > rYolkDeviationLimit THEN
            aRejectBlood[i] := TRUE;
        ELSE
            aRejectBlood[i] := FALSE;
        END_IF;
    END_IF;
    
    // 3. Weight Grading and Sorting Logic
    rTempWeight := aEggWeights[i];
    
    IF aRejectCrack[i] OR aRejectBlood[i] THEN
        aSortGrade[i] := 0; // Rejected Grade
        
        // Trigger Ejector with sync pulse
        tEjectorPulse[i](IN := TRUE, PT := T#50MS);
        aEjectorTriggers[i] := tEjectorPulse[i].Q;
    ELSE
        // Determine USDA Size Grade based on weight
        IF rTempWeight >= 70.9 THEN
            aSortGrade[i] := 1; // Jumbo
        ELSIF rTempWeight >= 63.8 AND rTempWeight < 70.9 THEN
            aSortGrade[i] := 2; // Extra Large
        ELSIF rTempWeight >= 56.7 AND rTempWeight < 63.8 THEN
            aSortGrade[i] := 3; // Large
        ELSIF rTempWeight >= 49.6 AND rTempWeight < 56.7 THEN
            aSortGrade[i] := 4; // Medium
        ELSIF rTempWeight >= 42.5 AND rTempWeight < 49.6 THEN
            aSortGrade[i] := 5; // Small
        ELSE
            aSortGrade[i] := 6; // Peewee
        END_IF;
        
        // Reset Ejector Pulse
        tEjectorPulse[i](IN := FALSE, PT := T#50MS);
        aEjectorTriggers[i] := FALSE;
    END_IF;
    
END_FOR;

END_FUNCTION_BLOCK
```"""

user_prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Commercial Egg Grading and Sorting Facility.
Task: Invent a highly complex control scenario for this domain (e.g., acoustic crack detection resonance analysis, candling vision rejection synchronization, and high-speed multi-lane grading).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."""

record = {
    "messages": [
        {"role": "user", "content": user_prompt},
        {"role": "assistant", "content": iec_code}
    ]
}

os.makedirs('data/swarm_raw', exist_ok=True)
filename = f'data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json'
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(record, f, indent=2)

with open('data/synthetic_generation_v3_enterprise.jsonl', 'a', encoding='utf-8') as f:
    f.write(json.dumps(record) + '\n')

print(f'Successfully created {filename} and appended to jsonl.')
