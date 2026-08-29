import os, json, uuid

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: High-Speed Web Envelope Converting Machine.
Task: Invent a highly complex control scenario for this domain (e.g., window patch film zero-speed splicing, cold glue extrusion volumetric tracking, and rotary flap folding pneumatics).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."""

iec_st_code = """```iec-st
FUNCTION_BLOCK FB_EnvelopeConverting_WebMaster
TITLE = 'High-Speed Web Envelope Converting Machine Control'
// Handles zero-speed splicing, cold glue volumetric tracking, and rotary flap folding

VAR_INPUT
    bEnable : BOOL; // System enable
    rLineSpeed_m_min : REAL; // Current main line speed in m/min
    bSpliceRequest : BOOL; // Request to initiate zero-speed splice
    rFilmDiameter_mm : REAL; // Current unwinding film roll diameter
    rGlueTargetVol_ml_m : REAL; // Target glue volume per meter
    bFlapFoldSyncPhase : BOOL; // Trigger signal for rotary flap folding
END_VAR

VAR_OUTPUT
    bSpliceActive : BOOL; // Splice sequence in progress
    rAccumulatorPos_mm : REAL; // Position of the film accumulator
    rGluePumpSpeed_rpm : REAL; // Commanded glue pump speed
    bFlapFoldValve1 : BOOL; // Pneumatic valve 1 for flap fold
    bFlapFoldValve2 : BOOL; // Pneumatic valve 2 for flap fold
    bError : BOOL;
    iErrorCode : INT;
END_VAR

VAR
    // Splice State Machine
    iSpliceState : INT := 0;
    rFilmAccel_m_s2 : REAL := 2.5; // Max film acceleration
    tSpliceTimer : TON;
    rAccumulatorDraw_m : REAL;

    // Glue Tracking
    rEncoderPulses_per_m : REAL := 10000.0;
    rPumpDisplacement_ml_rev : REAL := 15.0;
    
    // Flap Folding
    tFoldValve1Duration : TON;
    tFoldValve2Duration : TON;
    bPrevFoldSyncPhase : BOOL;
END_VAR

// ---------------------------------------------------------
// 1. Zero-Speed Splicing Logic
// ---------------------------------------------------------
// The accumulator pays out film while the unwind spindle stops for the splice
IF bEnable THEN
    CASE iSpliceState OF
        0: // Idle
            bSpliceActive := FALSE;
            IF bSpliceRequest AND rFilmDiameter_mm < 250.0 THEN
                iSpliceState := 10;
                bSpliceActive := TRUE;
            END_IF;
            
        10: // Decelerate Unwind, Accumulator takes over
            // Simulate accumulator filling/drawing
            rAccumulatorDraw_m := rAccumulatorDraw_m + (rLineSpeed_m_min / 60.0) * 0.01; // 10ms cycle
            IF rAccumulatorDraw_m > 10.0 THEN // Max capacity 10m
                iErrorCode := 1001; // Accumulator overflow
                bError := TRUE;
            END_IF;
            tSpliceTimer(IN:=TRUE, PT:=T#2S);
            IF tSpliceTimer.Q THEN
                iSpliceState := 20;
                tSpliceTimer(IN:=FALSE);
            END_IF;
            
        20: // Perform Splice (Firing knives, pressing tape)
            tSpliceTimer(IN:=TRUE, PT:=T#500MS);
            IF tSpliceTimer.Q THEN
                iSpliceState := 30;
                tSpliceTimer(IN:=FALSE);
            END_IF;
            
        30: // Accelerate new roll, refill accumulator
            rAccumulatorDraw_m := rAccumulatorDraw_m - (rLineSpeed_m_min / 60.0) * 0.02; // Refill twice as fast
            IF rAccumulatorDraw_m <= 0.0 THEN
                rAccumulatorDraw_m := 0.0;
                iSpliceState := 0;
            END_IF;
    END_CASE;
    rAccumulatorPos_mm := rAccumulatorDraw_m * 1000.0;
    
// ---------------------------------------------------------
// 2. Cold Glue Extrusion Volumetric Tracking
// ---------------------------------------------------------
// Calculates the required pump speed (RPM) to maintain consistent ml/m at current line speed
    IF rLineSpeed_m_min > 5.0 THEN
        // (m/min) * (ml/m) = ml/min
        // (ml/min) / (ml/rev) = rev/min (RPM)
        rGluePumpSpeed_rpm := (rLineSpeed_m_min * rGlueTargetVol_ml_m) / rPumpDisplacement_ml_rev;
    ELSE
        rGluePumpSpeed_rpm := 0.0; // Standby
    END_IF;

// ---------------------------------------------------------
// 3. Rotary Flap Folding Pneumatics
// ---------------------------------------------------------
// Trigger high-speed pneumatic valves based on machine phase pulse
    IF bFlapFoldSyncPhase AND NOT bPrevFoldSyncPhase THEN
        bFlapFoldValve1 := TRUE;
        bFlapFoldValve2 := FALSE;
    END_IF;
    
    // Timing logic for valve deactivation
    tFoldValve1Duration(IN:=bFlapFoldValve1, PT:=T#15MS);
    IF tFoldValve1Duration.Q THEN
        bFlapFoldValve1 := FALSE;
        bFlapFoldValve2 := TRUE; // Sequential fold
    END_IF;
    
    tFoldValve2Duration(IN:=bFlapFoldValve2, PT:=T#20MS);
    IF tFoldValve2Duration.Q THEN
        bFlapFoldValve2 := FALSE;
    END_IF;
    
    bPrevFoldSyncPhase := bFlapFoldSyncPhase;
ELSE
    // System disabled, reset outputs
    bSpliceActive := FALSE;
    rAccumulatorPos_mm := 0.0;
    rGluePumpSpeed_rpm := 0.0;
    bFlapFoldValve1 := FALSE;
    bFlapFoldValve2 := FALSE;
    iSpliceState := 0;
    tSpliceTimer(IN:=FALSE);
    tFoldValve1Duration(IN:=FALSE);
    tFoldValve2Duration(IN:=FALSE);
END_IF;
END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": iec_st_code}]}

os.makedirs("data/swarm_raw", exist_ok=True)
with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)
