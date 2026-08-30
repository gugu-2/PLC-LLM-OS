import os
import json
import uuid

os.makedirs("data/swarm_raw", exist_ok=True)
os.makedirs("data", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Industrial Bookbinding Perfect Binder.
Task: Invent a highly complex control scenario for this domain (e.g., spine roughing milling depth compensation, hot-melt EVA glue extrusion tracking, and cover nipping pressure profiling).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."""

response = """```iec-st
FUNCTION_BLOCK FB_PerfectBinderControl
VAR_INPUT
    bEnable : BOOL; // Enable binder control
    rBookThickness : REAL; // Measured book block thickness (mm)
    rPaperDensity : REAL; // Paper density factor (gsm)
    rTargetMillingDepth : REAL; // Base target milling depth (mm)
    rActualMillingCurrent : REAL; // Feedback current from milling motor (A)
    rGlueTempEVA : REAL; // Current EVA glue temperature (deg C)
    rLineSpeed : REAL; // Machine speed (books/min)
    bCoverReady : BOOL; // Cover feeder ready signal
END_VAR
VAR_OUTPUT
    rMillingDepthSetPoint : REAL; // Compensated milling depth (mm)
    rGlueExtrusionRate : REAL; // Calculated glue extrusion volume (ml/s)
    rNippingPressure : REAL; // Calculated cover nipping pressure (Bar)
    bSystemReady : BOOL; // System ready to cycle
    bError : BOOL; // General error flag
    iErrorID : INT; // Error code
END_VAR
VAR
    rMillingWearCompensation : REAL := 0.0;
    rBaseExtrusion : REAL;
    rNippingBaseForce : REAL := 150.0; // Base force per mm thickness
    rTempFactor : REAL;
    rSpeedFactor : REAL;
    
    // Timers
    TMR_GlueHeating : TON;
    
    // Constants
    cMaxMillingDepth : REAL := 3.5;
    cMinMillingDepth : REAL := 0.5;
    cOptimumGlueTemp : REAL := 160.0;
    cGlueTempTolerance : REAL := 5.0;
END_VAR

// Reset outputs if disabled
IF NOT bEnable THEN
    rMillingDepthSetPoint := 0.0;
    rGlueExtrusionRate := 0.0;
    rNippingPressure := 0.0;
    bSystemReady := FALSE;
    bError := FALSE;
    iErrorID := 0;
    RETURN;
END_IF;

// 1. Spine Roughing Milling Depth Compensation
// Increase milling depth slightly if motor current is low (implies blade wear or softer paper)
IF rActualMillingCurrent < 4.5 AND rActualMillingCurrent > 1.0 THEN
    rMillingWearCompensation := rMillingWearCompensation + 0.001;
ELSIF rActualMillingCurrent > 6.0 THEN
    rMillingWearCompensation := rMillingWearCompensation - 0.001;
END_IF;

rMillingDepthSetPoint := rTargetMillingDepth + rMillingWearCompensation;

// Clamp milling depth
IF rMillingDepthSetPoint > cMaxMillingDepth THEN
    rMillingDepthSetPoint := cMaxMillingDepth;
ELSIF rMillingDepthSetPoint < cMinMillingDepth THEN
    rMillingDepthSetPoint := cMinMillingDepth;
END_IF;

// 2. Hot-Melt EVA Glue Extrusion Tracking
// Extrusion rate depends on line speed, book thickness, and glue temperature
rSpeedFactor := rLineSpeed / 60.0; // scale to books per sec
rTempFactor := 1.0;

// If temp is low, viscosity is high, push harder
IF rGlueTempEVA < cOptimumGlueTemp THEN
    rTempFactor := 1.1 + ((cOptimumGlueTemp - rGlueTempEVA) * 0.02);
END_IF;

// Base extrusion (ml/s) = thickness * speed * constant
rBaseExtrusion := rBookThickness * rSpeedFactor * 0.85; 
rGlueExtrusionRate := rBaseExtrusion * rTempFactor;

// Check temperature bounds for error
IF ABS(rGlueTempEVA - cOptimumGlueTemp) > cGlueTempTolerance THEN
    // Warning state, not necessarily error, but flag if too cold
    IF rGlueTempEVA < (cOptimumGlueTemp - 15.0) THEN
        bError := TRUE;
        iErrorID := 101; // Glue too cold
    END_IF;
END_IF;

// 3. Cover Nipping Pressure Profiling
// Pressure applied must be proportional to book thickness and paper density
// Thicker books need more baseline force, higher density needs firmer nip
IF bCoverReady THEN
    rNippingPressure := (rNippingBaseForce * rBookThickness * (rPaperDensity / 80.0)) / 100.0; // Scale to Bar
    
    // Safety clamp
    IF rNippingPressure > 8.0 THEN
        rNippingPressure := 8.0; // Max 8 Bar
    ELSIF rNippingPressure < 2.0 THEN
        rNippingPressure := 2.0; // Min 2 Bar
    END_IF;
ELSE
    rNippingPressure := 0.0;
END_IF;

// Evaluate System Ready State
IF NOT bError AND bCoverReady AND (ABS(rGlueTempEVA - cOptimumGlueTemp) <= cGlueTempTolerance) THEN
    bSystemReady := TRUE;
ELSE
    bSystemReady := FALSE;
END_IF;

END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": response}]}

with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
    json.dump(record, f)

with open("data/synthetic_generation_v3_enterprise.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\n")

print("Success")
