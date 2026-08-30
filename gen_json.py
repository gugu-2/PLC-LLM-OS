import json, uuid, os

code = """```iec-st
FUNCTION_BLOCK FB_MeatSlicingPackagingControl
VAR_INPUT
    bEnable : BOOL; // System enable
    bEstop : BOOL; // Emergency stop
    rLogAdvanceSpeed : REAL; // mm/s
    rTargetSliceWeight : REAL; // grams
    iVisionFatRatio : INT; // 0-100%
    iVisionLeanRatio : INT; // 0-100%
    rCurrentLogPosition : REAL; // mm
    rGasPressureO2 : REAL; // bar
    rGasPressureCO2 : REAL; // bar
    bPackagingReady : BOOL;
END_VAR

VAR_OUTPUT
    bSystemReady : BOOL;
    rBladeRPM : REAL; // Target RPM for blade
    rActualLogAdvanceSpeed : REAL;
    bStartCut : BOOL;
    bFlushGas : BOOL;
    bSealPackage : BOOL;
    bRejectSlice : BOOL;
    iErrorCode : INT;
END_VAR

VAR
    rDensityFat : REAL := 0.9; // g/cm3
    rDensityLean : REAL := 1.05; // g/cm3
    rLogDiameter : REAL := 100.0; // mm
    rArea : REAL;
    rEstimatedDensity : REAL;
    rRequiredThickness : REAL; // mm
    rTimePerSlice : REAL; // seconds
    State : INT := 0;
    TimerGas : TON;
    TimerSeal : TON;
    rPrevLogPosition : REAL;
    rCutPosition : REAL;
END_VAR

// Implementation
IF bEstop THEN
    State := 99;
    bSystemReady := FALSE;
    rBladeRPM := 0.0;
    rActualLogAdvanceSpeed := 0.0;
    bStartCut := FALSE;
    bFlushGas := FALSE;
    bSealPackage := FALSE;
    iErrorCode := 100;
    RETURN;
END_IF;

IF NOT bEnable THEN
    State := 0;
    bSystemReady := FALSE;
    rBladeRPM := 0.0;
    rActualLogAdvanceSpeed := 0.0;
    bStartCut := FALSE;
    bFlushGas := FALSE;
    bSealPackage := FALSE;
    RETURN;
END_IF;

bSystemReady := TRUE;

CASE State OF
    0: // Initialization and Calculation
        rArea := 3.14159 * (rLogDiameter / 2.0) * (rLogDiameter / 2.0); // mm2
        rEstimatedDensity := (INT_TO_REAL(iVisionFatRatio) * rDensityFat + INT_TO_REAL(iVisionLeanRatio) * rDensityLean) / 100.0;
        
        // Calculate required thickness for target weight
        // Weight = Volume * Density = Area * Thickness * Density
        // Thickness = Weight / (Area * Density)
        rRequiredThickness := rTargetSliceWeight / (rArea * rEstimatedDensity * 0.001); // 0.001 to convert mm3 to cm3 roughly
        
        // Synchronize Blade RPM to log advance speed
        IF rLogAdvanceSpeed > 0.0 AND rRequiredThickness > 0.0 THEN
            rTimePerSlice := rRequiredThickness / rLogAdvanceSpeed;
            rBladeRPM := 60.0 / rTimePerSlice; // 1 rotation per slice
            rActualLogAdvanceSpeed := rLogAdvanceSpeed;
            rCutPosition := rCurrentLogPosition + rRequiredThickness;
            State := 10;
        ELSE
            iErrorCode := 101; // Invalid speed or thickness
            rBladeRPM := 0.0;
            rActualLogAdvanceSpeed := 0.0;
        END_IF;
        
    10: // Slicing Operation
        IF rCurrentLogPosition >= rCutPosition THEN
            bStartCut := TRUE;
            State := 20;
        ELSE
            bStartCut := FALSE;
        END_IF;
        
    20: // Packaging checks
        IF bPackagingReady THEN
            State := 30;
        ELSE
            iErrorCode := 102; // Waiting for packaging
        END_IF;
        
    30: // MAP Gas Flushing
        bFlushGas := TRUE;
        TimerGas(IN := TRUE, PT := T#2S);
        IF TimerGas.Q THEN
            bFlushGas := FALSE;
            TimerGas(IN := FALSE);
            State := 40;
        END_IF;
        
    40: // Sealing
        bSealPackage := TRUE;
        TimerSeal(IN := TRUE, PT := T#1S);
        IF TimerSeal.Q THEN
            bSealPackage := FALSE;
            TimerSeal(IN := FALSE);
            State := 0; // Ready for next cycle
        END_IF;
        
    99: // Error State
        bStartCut := FALSE;
        bFlushGas := FALSE;
        bSealPackage := FALSE;
        IF NOT bEstop THEN
            State := 0;
            iErrorCode := 0;
        END_IF;
END_CASE;

END_FUNCTION_BLOCK
```"""

prompt = "Invent a highly complex control scenario for High-Speed Automated Meat Slicing & Packaging."

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}

os.makedirs(r"c:\Users\majip\Downloads\LLM REASEARCH\data\swarm_raw", exist_ok=True)
filename = f"c:\\Users\\majip\\Downloads\\LLM REASEARCH\\data\\swarm_raw\\agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)
print(filename)
