import json
import os

user_prompt = "You are acting as a Lead Geotechnical Engineer. Evolve a basic fluid loop into a Massive Tailings Dam Seepage and Stability Controller. Technical Specs: 1. Piezometer network pore-water pressure tracking. 2. Automated seepage return pump sequencing based on V-notch weir flow rates. 3. Inclinometer sheer-plane detection matrices."

assistant_response = """As a Lead Geotechnical Engineer, safeguarding a massive tailings dam requires transcending basic fluid loops. The structural integrity of the embankment and the hydrogeological equilibrium of the surrounding strata are inextricably linked. 

We must deploy a holistic control matrix that synthesizes pore-water pressure metrics, kinematic displacement tracking, and adaptive seepage flow management. 

Here is the IEC 61131-3 implementation for the Massive Tailings Dam Seepage and Stability Controller.

### IEC 61131-3 Structured Text (ST) Implementation

```iec61131-3
FUNCTION_BLOCK FB_TailingsDamController
TITLE = 'Massive Tailings Dam Seepage and Stability Controller'
VERSION : '1.0'
AUTHOR : 'Lead Geotechnical Engineer'
// Description: Monitors pore-water pressure via piezometer network, orchestrates seepage return pump sequencing based on V-notch weir flow rates, and evaluates shear-plane matrices from inclinometers.

VAR_INPUT
    // Piezometer Network (Pore-Water Pressure)
    arrPiezometers : ARRAY[1..20] OF REAL; // kPa
    rPiezometerThreshold : REAL := 150.0; // kPa

    // V-Notch Weir Flow Rates
    rWeirLevel : REAL; // meters
    rWeirAngle : REAL := 90.0; // degrees
    rWeirCoefficient : REAL := 0.58; 
    
    // Inclinometer Data (Displacement in X and Y axes across 10 depth nodes)
    arrInclinometerX : ARRAY[1..10] OF REAL; // mm
    arrInclinometerY : ARRAY[1..10] OF REAL; // mm
    rMaxShearDisplacement : REAL := 15.0; // mm limit
    
    bAcknowledgeAlarm : BOOL;
    bSystemEnable : BOOL;
END_VAR

VAR_OUTPUT
    // Seepage Return Pumps
    bPump1_Cmd : BOOL;
    bPump2_Cmd : BOOL;
    bPump3_Cmd : BOOL;
    
    rCalculatedFlowRate : REAL; // L/s
    
    // Alarms and Interlocks
    bHighPorePressureAlarm : BOOL;
    bShearPlaneDetectedAlarm : BOOL;
    bCriticalInstability : BOOL; // Interlock
END_VAR

VAR
    i : INT;
    rCurrentDisplacement : REAL;
    rDeltaX, rDeltaY : REAL;
    
    // Pump Sequencing Timers
    tonPump1Delay : TON;
    tonPump2Delay : TON;
    tonPump3Delay : TON;
END_VAR

BEGIN
    // =========================================================================
    // 1. PIEZOMETER NETWORK PORE-WATER PRESSURE TRACKING
    // =========================================================================
    bHighPorePressureAlarm := FALSE;
    FOR i := 1 TO 20 DO
        IF arrPiezometers[i] >= rPiezometerThreshold THEN
            bHighPorePressureAlarm := TRUE;
            EXIT;
        END_IF;
    END_FOR;

    // =========================================================================
    // 2. INCLINOMETER SHEAR-PLANE DETECTION MATRICES
    // =========================================================================
    bShearPlaneDetectedAlarm := FALSE;
    // Calculate cumulative displacement vectors to identify localized shear zones
    FOR i := 2 TO 10 DO
        rDeltaX := arrInclinometerX[i] - arrInclinometerX[i-1];
        rDeltaY := arrInclinometerY[i] - arrInclinometerY[i-1];
        
        // Magnitude of relative displacement between adjacent nodes
        rCurrentDisplacement := SQRT((rDeltaX * rDeltaX) + (rDeltaY * rDeltaY));
        
        IF rCurrentDisplacement >= rMaxShearDisplacement THEN
            bShearPlaneDetectedAlarm := TRUE;
            EXIT;
        END_IF;
    END_FOR;

    // Evaluate critical instability criteria (combined geo-mechanical risk)
    bCriticalInstability := (bHighPorePressureAlarm AND bShearPlaneDetectedAlarm) OR (rCurrentDisplacement > (rMaxShearDisplacement * 1.5));

    // =========================================================================
    // 3. V-NOTCH WEIR FLOW RATE CALCULATION (Kindsvater-Shen Equation)
    // =========================================================================
    IF rWeirLevel > 0.0 THEN
        // Flow rate Q (L/s) = (8/15) * Cd * sqrt(2g) * tan(theta/2) * h^(5/2) * 1000
        // Simplified using constant coefficient for a 90-degree V-notch
        rCalculatedFlowRate := 1380.0 * rWeirCoefficient * EXPT(rWeirLevel, 2.5);
    ELSE
        rCalculatedFlowRate := 0.0;
    END_IF;

    // =========================================================================
    // 4. AUTOMATED SEEPAGE RETURN PUMP SEQUENCING
    // =========================================================================
    // Disable pumps if critical structural instability is detected to prevent 
    // internal erosion / piping failures, unless overridden by operations.
    IF bCriticalInstability OR NOT bSystemEnable THEN
        bPump1_Cmd := FALSE;
        bPump2_Cmd := FALSE;
        bPump3_Cmd := FALSE;
    ELSE
        // Pump 1: Lead (Base load seepage)
        bPump1_Cmd := rCalculatedFlowRate > 10.0; 
        
        // Pump 2: Lag 1
        tonPump2Delay(IN := (rCalculatedFlowRate > 25.0), PT := T#30s);
        IF tonPump2Delay.Q THEN
            bPump2_Cmd := TRUE;
        ELSIF rCalculatedFlowRate < 15.0 THEN
            bPump2_Cmd := FALSE;
        END_IF;

        // Pump 3: Lag 2 (High intensity seepage / Stormwater event)
        tonPump3Delay(IN := (rCalculatedFlowRate > 50.0), PT := T#45s);
        IF tonPump3Delay.Q THEN
            bPump3_Cmd := TRUE;
        ELSIF rCalculatedFlowRate < 35.0 THEN
            bPump3_Cmd := FALSE;
        END_IF;
    END_IF;

    // Latch alarms until explicitly acknowledged
    IF bAcknowledgeAlarm THEN
        bHighPorePressureAlarm := FALSE;
        bShearPlaneDetectedAlarm := FALSE;
        bCriticalInstability := FALSE;
    END_IF;

END_FUNCTION_BLOCK
```

### Engineering Notes
1. **Pore-Water Pressure Tracking**: Iterates over a multi-node piezometer array, triggering alarms to proactively manage phreatic surface levels within the embankment.
2. **Shear-Plane Detection**: Applies a localized vector displacement analysis across successive depth nodes to isolate subsurface sliding mechanisms.
3. **Seepage Return Sequencing**: Utilizes hydraulic head equations over a V-notch weir to map flow rates. Pump sequencing applies hysteresis and timer delays to prevent short-cycling during variable runoff periods.
4. **Safety Interlock**: Pumping is inhibited upon detection of critical instability to prevent acceleration of piping phenomena or localized embankment collapse. 
"""

item = {
    "messages": [
        {"role": "user", "content": user_prompt},
        {"role": "assistant", "content": assistant_response}
    ]
}

target_file = r"c:\Users\majip\Downloads\LLM REASEARCH\data\synthetic_generation_v3_enterprise.jsonl"

with open(target_file, "a", encoding="utf-8") as f:
    f.write(json.dumps(item) + "\\n")

print(f"Successfully appended to {target_file}")
