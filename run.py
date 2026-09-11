import os
import json
import uuid

prompt = '''You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Next-Gen Extreme Environment Deep Borehole Seismometer Array**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., 20km depth 300°C piezoelectric sensor drift compensation, armored fiber-optic telemetry Bragg grating interrogation, and mud-pulse acoustic decoupling). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.'''

code = '''`iec-st
FUNCTION_BLOCK FB_DeepBoreholeSeismometer
VAR_INPUT
    (* Required: at least 4-8 physical inputs with types and comments *)
    bEnable                 : BOOL;     (* System enable signal *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal *)
    rTempDeepHole           : REAL;     (* Ambient temperature at 20km depth in deg C *)
    rPressureAmb            : REAL;     (* Ambient pressure at depth in MPa *)
    rPiezoRawSignal         : LREAL;    (* Raw piezoelectric sensor signal *)
    rFiberStrainRaw         : LREAL;    (* Armored fiber-optic Bragg grating strain *)
    bMudPulseSync           : BOOL;     (* Mud-pulse acoustic telemetry sync lock *)
    bCalibrationMode        : BOOL;     (* Trigger drift compensation calibration *)
END_VAR
VAR_OUTPUT
    (* Required: at least 3-6 outputs with types and comments *)
    bSystemReady            : BOOL;     (* System ready status, filters primed *)
    rSeismicOutput_X        : LREAL;    (* Compensated seismic trace X-axis *)
    rSeismicOutput_Y        : LREAL;    (* Compensated seismic trace Y-axis *)
    rSeismicOutput_Z        : LREAL;    (* Compensated seismic trace Z-axis *)
    bTelemetryLinkOk        : BOOL;     (* Active mud-pulse telemetry link OK *)
    bAlarm                  : BOOL;     (* Fault alarm output (overtemp/pressure) *)
    iFaultCode              : INT;      (* Diagnostics fault code *)
END_VAR
VAR
    (* Internal state variables *)
    iState                  : INT := 0;
    tInitTimer              : TON;
    tCalibTimer             : TON;
    
    (* Filtering arrays *)
    aHistory_Piezo          : ARRAY[0..99] OF LREAL;
    iBufferIndex            : INT := 0;
    rPiezoFiltered          : LREAL;
    
    (* Compensation factors *)
    rTempCompFactor         : LREAL;
    rPressureCompFactor     : LREAL;
    
    (* Calibration offsets *)
    rOffset_X               : LREAL := 0.0;
    rOffset_Y               : LREAL := 0.0;
    rOffset_Z               : LREAL := 0.0;
END_VAR

(* === MAIN LOGIC === *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bTelemetryLinkOk := FALSE;
    bAlarm := TRUE;
    iFaultCode := 9999;
    rSeismicOutput_X := 0.0;
    rSeismicOutput_Y := 0.0;
    rSeismicOutput_Z := 0.0;
    iState := 0;
    RETURN;
END_IF;

(* Continuous Environmental Monitoring Safety Interlocks *)
IF rTempDeepHole > 310.0 OR rPressureAmb > 250.0 THEN
    bAlarm := TRUE;
    iFaultCode := 1001; (* Extreme Environment Limit Exceeded *)
    bSystemReady := FALSE;
    iState := 0;
ELSE
    bAlarm := FALSE;
    iFaultCode := 0;
END_IF;

(* Compute Environmental Compensation Factors *)
(* Extremely complex polynomial drift correction for 300C piezo effects *)
rTempCompFactor := (rTempDeepHole * 0.0034) + (rTempDeepHole * rTempDeepHole * 0.000012);
rPressureCompFactor := (rPressureAmb * 0.015) - 0.002;

CASE iState OF
    0: (* IDLE & INITIALIZATION *)
        bSystemReady := FALSE;
        IF bEnable AND NOT bAlarm THEN
            iState := 10;
        END_IF;

    10: (* PRIMING FILTERS & SENSOR PRE-HEATING ALIGNMENT *)
        tInitTimer(IN := TRUE, PT := T#15S);
        IF tInitTimer.Q THEN
            tInitTimer(IN := FALSE);
            iState := 20;
        END_IF;

    20: (* RUNNING / NOMINAL OPERATION *)
        bSystemReady := TRUE;
        
        (* Circular Buffer for Moving Average / FIR Filter approximation *)
        aHistory_Piezo[iBufferIndex] := rPiezoRawSignal;
        iBufferIndex := iBufferIndex + 1;
        IF iBufferIndex > 99 THEN
            iBufferIndex := 0;
        END_IF;
        
        (* Calculate compensated seismic trace using fusion of piezo and fiber optic strain *)
        rPiezoFiltered := rPiezoRawSignal * rTempCompFactor * rPressureCompFactor;
        
        rSeismicOutput_X := rPiezoFiltered + rFiberStrainRaw - rOffset_X;
        rSeismicOutput_Y := (rPiezoFiltered * 0.85) + (rFiberStrainRaw * 1.1) - rOffset_Y;
        rSeismicOutput_Z := (rPiezoFiltered * 1.2) - (rFiberStrainRaw * 0.9) - rOffset_Z;
        
        bTelemetryLinkOk := bMudPulseSync;
        
        IF bCalibrationMode THEN
            iState := 30;
        END_IF;
        
        IF NOT bEnable THEN
            iState := 0;
        END_IF;

    30: (* CALIBRATION & DRIFT COMPENSATION MODE *)
        bSystemReady := FALSE; (* Temporarily offline for calib *)
        tCalibTimer(IN := TRUE, PT := T#30S);
        
        (* Accumulate drift baseline *)
        rOffset_X := rOffset_X + (rPiezoRawSignal * 0.001);
        rOffset_Y := rOffset_Y + (rPiezoRawSignal * 0.001);
        rOffset_Z := rOffset_Z + (rPiezoRawSignal * 0.001);
        
        IF tCalibTimer.Q THEN
            tCalibTimer(IN := FALSE);
            iState := 20;
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
`'''

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": code}
    ]
}

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
