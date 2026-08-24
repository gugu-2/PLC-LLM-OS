import json
import os

message = {
    "messages": [
        {
            "role": "user",
            "content": "You are acting as a Lead Medical Electronics Engineer. Evolve a basic pulse loop into a Biventricular Pacemaker (CRT-P) Controller. Technical Specs: 1. Right and left ventricle independent pacing (Cardiac Resynchronization Therapy). 2. Atrial fibrillation (AF) detection using dynamic thresholding. 3. Magnet-mode reversion interlocks for MRI safety."
        },
        {
            "role": "assistant",
            "content": """Here is the evolved Biventricular Pacemaker (CRT-P) Controller implemented in IEC 61131-3 Structured Text.

```iecst
FUNCTION_BLOCK FB_Biventricular_Pacemaker_CRTP
TITLE = 'Biventricular Pacemaker (CRT-P) Controller'
AUTHOR : 'Lumina'
VERSION : '1.0'

(*
    CRT-P Controller with independent Right/Left Ventricle pacing,
    Dynamic Atrial Fibrillation (AF) detection, and
    Magnet-Mode MRI Safety Interlock.
*)

VAR_INPUT
    xAtrialSense       : BOOL;   // Sensed atrial intrinsic event
    xRVSense           : BOOL;   // Sensed Right Ventricle intrinsic event
    xLVSense           : BOOL;   // Sensed Left Ventricle intrinsic event
    rAtrialAmplitude   : REAL;   // Measured amplitude of atrial signal (mV)
    xMagnetMode        : BOOL;   // Magnet applied (MRI safety mode)
    tBasePacingInterval: TIME := T#850ms;  // ~70 BPM
    tAV_Delay          : TIME := T#150ms;  // Atrioventricular delay
    tVV_Delay          : TIME := T#20ms;   // Interventricular delay (LV after RV)
END_VAR

VAR_OUTPUT
    xAtrialPace        : BOOL;   // Atrial pacing output
    xRVPace            : BOOL;   // Right Ventricle pacing output
    xLVPace            : BOOL;   // Left Ventricle pacing output
    xAF_Detected       : BOOL;   // Atrial Fibrillation detection flag
    xMRI_Safe_Mode     : BOOL;   // Active indication of MRI safe reversion
END_VAR

VAR
    // Timers
    fbBaseTimer        : TON;
    fbAVTimer          : TON;
    fbVVTimer          : TON;
    
    // State machine & logic
    iState             : INT := 0; // 0: Wait A, 1: AV Delay, 2: VV Delay, 3: Refractory
    tRefractoryPeriod  : TIME := T#250ms;
    fbRefractoryTimer  : TON;
    
    // AF Detection (Dynamic Thresholding)
    rDynamicThreshold  : REAL := 1.5; // Initial AF sensitivity threshold (mV)
    aAtrialIntervals   : ARRAY[0..4] OF TIME; // Moving average array
    iIndex             : INT := 0;
    fbIntervalTimer    : TON;
END_VAR

BEGIN
    // ==========================================
    // 1. MAGNET-MODE MRI SAFETY INTERLOCK
    // ==========================================
    xMRI_Safe_Mode := xMagnetMode;
    IF xMRI_Safe_Mode THEN
        // VOO Mode: Asynchronous pacing at fixed base interval, ignore sensing
        fbBaseTimer(IN := NOT fbBaseTimer.Q, PT := tBasePacingInterval);
        IF fbBaseTimer.Q THEN
            xRVPace := TRUE;
            xLVPace := TRUE;
            xAtrialPace := TRUE;
        ELSE
            xRVPace := FALSE;
            xLVPace := FALSE;
            xAtrialPace := FALSE;
        END_IF;
        xAF_Detected := FALSE;
        iState := 0;
        RETURN;
    END_IF;

    // ==========================================
    // 2. ATRIAL FIBRILLATION DYNAMIC DETECTION
    // ==========================================
    // Dynamic Threshold Adjustment based on signal amplitude
    IF rAtrialAmplitude > 0.0 THEN
        // EMA filter for adaptive threshold
        rDynamicThreshold := (rDynamicThreshold * 0.9) + (rAtrialAmplitude * 0.05);
    END_IF;

    fbIntervalTimer(IN := TRUE, PT := T#10s);
    IF xAtrialSense AND (rAtrialAmplitude > rDynamicThreshold) THEN
        // Record interval
        aAtrialIntervals[iIndex] := fbIntervalTimer.ET;
        fbIntervalTimer(IN := FALSE); // Reset
        fbIntervalTimer(IN := TRUE);
        
        iIndex := (iIndex + 1) MOD 5;
        
        // Evaluate AF (Fast irregular rates - simple evaluation for demonstration)
        IF (aAtrialIntervals[0] < T#200ms) AND (aAtrialIntervals[1] < T#200ms) THEN
            xAF_Detected := TRUE;
        ELSE
            xAF_Detected := FALSE;
        END_IF;
    END_IF;

    // ==========================================
    // 3. CRT-P STATE MACHINE (A-RV-LV PACING)
    // ==========================================
    CASE iState OF
        0: // Wait for Atrial Sense or Base Timer
            fbBaseTimer(IN := TRUE, PT := tBasePacingInterval);
            IF xAtrialSense OR fbBaseTimer.Q THEN
                fbBaseTimer(IN := FALSE);
                
                // Mode-switch during AF: Suppress atrial pacing, delay AV
                IF NOT xAtrialSense AND NOT xAF_Detected THEN
                    xAtrialPace := TRUE;
                ELSE
                    xAtrialPace := FALSE;
                END_IF;
                iState := 1; // Move to AV Delay
            END_IF;

        1: // AV Delay Phase
            xAtrialPace := FALSE; // Reset Atrial Pace
            fbAVTimer(IN := TRUE, PT := tAV_Delay);
            IF xRVSense THEN
                fbAVTimer(IN := FALSE);
                iState := 2; // Intrinsic RV sense, move to LV timing
            ELSIF fbAVTimer.Q THEN
                fbAVTimer(IN := FALSE);
                xRVPace := TRUE; // AV delay expired, pace RV
                iState := 2;
            END_IF;

        2: // VV Delay Phase (CRT Synchronization)
            fbVVTimer(IN := TRUE, PT := tVV_Delay);
            IF xLVSense THEN
                fbVVTimer(IN := FALSE);
                xRVPace := FALSE;
                iState := 3; // Intrinsic LV sense
            ELSIF fbVVTimer.Q THEN
                fbVVTimer(IN := FALSE);
                xLVPace := TRUE; // Pace LV
                xRVPace := FALSE; // Reset RV Pace
                iState := 3;
            END_IF;

        3: // Refractory Period
            xLVPace := FALSE; // Reset LV Pace
            fbRefractoryTimer(IN := TRUE, PT := tRefractoryPeriod);
            IF fbRefractoryTimer.Q THEN
                fbRefractoryTimer(IN := FALSE);
                iState := 0; // Return to Wait state
            END_IF;
            
    END_CASE;

END_FUNCTION_BLOCK
```"""
        }
    ]
}

target_file = r"c:\Users\majip\Downloads\LLM REASEARCH\data\synthetic_generation_v3_enterprise.jsonl"
with open(target_file, "a", encoding="utf-8") as f:
    f.write(json.dumps(message) + "\n")
print(f"Successfully appended 1 JSON object to {target_file}")
