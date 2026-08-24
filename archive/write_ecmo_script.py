import json

prompt = "Evolve a basic timer into an ECMO (Extracorporeal Membrane Oxygenation) Machine Controller. Technical Specs: 1. Centrifugal blood pump flow rate tracking to prevent hemolysis. 2. Membrane oxygenator sweep gas blending (O2/Air). 3. Ultrasonic micro-bubble air-in-line detection and rapid clamping. Append to synthetic_generation_v3_enterprise.jsonl."

assistant_response = """```iec61131-3
// EVOLVED ECMO CONTROLLER
// Originally a simple TON (Timer on Delay), this module has been heavily evolved into a 
// life-critical ECMO (Extracorporeal Membrane Oxygenation) Machine Controller.
//
// Technical Specs Implemented:
// 1. Centrifugal blood pump flow rate tracking (Hemolysis prevention via speed & pressure limits).
// 2. Membrane oxygenator sweep gas blending (O2/Air).
// 3. Ultrasonic micro-bubble air-in-line detection and rapid clamping.

FUNCTION_BLOCK FB_ECMO_Controller
VAR_INPUT
    bEnable : BOOL; // System master enable
    bReset : BOOL; // Reset alarms
    
    // Blood Pump Parameters (Centrifugal)
    rTargetBloodFlow : REAL; // Target flow in L/min
    rActualBloodFlow : REAL; // Actual measured flow in L/min
    rPumpSpeedRPM : REAL; // Centrifugal pump speed
    
    // Pressures
    rPressurePreMembrane : REAL; // mmHg
    rPressurePostMembrane : REAL; // mmHg
    
    // Sweep Gas Parameters
    rTargetSweepFlow : REAL; // Target sweep gas flow in L/min
    rTargetFiO2 : REAL; // Target fraction of inspired O2 (21.0 to 100.0 %)
    
    // Safety Sensors
    bUltrasonicAirDetect : BOOL; // Ultrasonic micro-bubble detector (TRUE = Air present)
END_VAR

VAR_OUTPUT
    // Actuator Commands
    rPumpSpeedCmd : REAL; // Command to blood pump VFD
    rSweepO2ValveCmd : REAL; // 0.0 to 100.0% open
    rSweepAirValveCmd : REAL; // 0.0 to 100.0% open
    bEmergencyClampCmd : BOOL; // TRUE = Clamp venous/arterial lines
    
    // Status & Alarms
    bSystemRunning : BOOL;
    bAlarmHemolysisRisk : BOOL;
    bAlarmAirInLine : BOOL;
    bAlarmHighDeltaP : BOOL; // High Trans-membrane pressure
END_VAR

VAR
    // Internal Timers & Controllers
    fbStartDelay : TON; // Originally the basic timer, now stages the startup sequence
    fbAirBubbleTimer : TON; // Debounce for micro-bubble (very short, e.g., 10ms)
    fbHemolysisDelay : TON; // Sustained high speed/low flow detection
    
    // PID Controllers for Blending & Pumping
    fbBloodFlowPID : PID;
    
    rMaxSafeRPM : REAL := 4500.0;
    rMaxDeltaP : REAL := 150.0; // Max pressure drop across oxygenator
    
    eState : INT; // 0=INIT, 1=STANDBY, 2=RUNNING, 3=EMERGENCY_STOP
    rO2Fraction : REAL;
    rDeltaP : REAL;
END_VAR

// -----------------------------------------------------------------------------
// 1. Air-In-Line Detection & Rapid Clamping
// -----------------------------------------------------------------------------
// This is the most critical safety loop. Must actuate immediately.
fbAirBubbleTimer(IN := bUltrasonicAirDetect, PT := T#10ms);

IF fbAirBubbleTimer.Q THEN
    bAlarmAirInLine := TRUE;
    bEmergencyClampCmd := TRUE; // RAPID CLAMPING
    eState := 3; // EMERGENCY_STOP
END_IF;

// Alarm Reset
IF bReset THEN
    bAlarmAirInLine := FALSE;
    bAlarmHemolysisRisk := FALSE;
    bAlarmHighDeltaP := FALSE;
    IF NOT bUltrasonicAirDetect THEN
        bEmergencyClampCmd := FALSE;
        eState := 1; // STANDBY
    END_IF;
END_IF;

// -----------------------------------------------------------------------------
// State Machine (Evolved from basic start timer)
// -----------------------------------------------------------------------------
CASE eState OF
    0: // INIT
        rPumpSpeedCmd := 0.0;
        rSweepO2ValveCmd := 0.0;
        rSweepAirValveCmd := 0.0;
        bEmergencyClampCmd := TRUE; // Keep clamped until primed and safe
        IF bEnable THEN
            eState := 1; // STANDBY
        END_IF;
        
    1: // STANDBY
        rPumpSpeedCmd := 0.0;
        bSystemRunning := FALSE;
        fbStartDelay(IN := bEnable, PT := T#2s); // 2 second staging delay
        
        IF fbStartDelay.Q AND NOT bEmergencyClampCmd THEN
            eState := 2; // RUNNING
        END_IF;
        
        IF NOT bEnable THEN
            fbStartDelay(IN := FALSE);
        END_IF;
        
    2: // RUNNING
        bSystemRunning := TRUE;
        
        // ---------------------------------------------------------------------
        // 2. Membrane Oxygenator Sweep Gas Blending (O2/Air)
        // ---------------------------------------------------------------------
        // Simple mass balance blending calculation
        // Total Flow = Air Flow + O2 Flow
        // Air has ~21% O2. Pure O2 has 100% O2.
        // FiO2_target * TotalFlow = 0.21 * AirFlow + 1.0 * O2Flow
        IF rTargetFiO2 < 21.0 THEN 
            rTargetFiO2 := 21.0; 
        ELSIF rTargetFiO2 > 100.0 THEN
            rTargetFiO2 := 100.0;
        END_IF;
        
        // Calculate theoretical required flows based on target proportion
        rO2Fraction := (rTargetFiO2 - 21.0) / 79.0;
        
        // Assuming linear valve characteristic for simplicity, mapped to 0-100%
        rSweepO2ValveCmd := rTargetSweepFlow * rO2Fraction * 10.0; // Scaled to valve capacity
        rSweepAirValveCmd := rTargetSweepFlow * (1.0 - rO2Fraction) * 10.0;
        
        // ---------------------------------------------------------------------
        // 3. Centrifugal Blood Pump Flow Rate Tracking (Hemolysis Prevention)
        // ---------------------------------------------------------------------
        // Using PID to control flow
        fbBloodFlowPID.ACTUAL := rActualBloodFlow;
        fbBloodFlowPID.SET_POINT := rTargetBloodFlow;
        fbBloodFlowPID.KP := 2.5;
        fbBloodFlowPID.TN := T#1s;
        fbBloodFlowPID.TV := T#0ms;
        fbBloodFlowPID(ENABLE := TRUE);
        
        // Output from PID adjusts the RPM command
        rPumpSpeedCmd := fbBloodFlowPID.Y; 
        
        // Safety Limit: Clamp RPM to prevent shearing and hemolysis
        IF rPumpSpeedCmd > rMaxSafeRPM THEN
            rPumpSpeedCmd := rMaxSafeRPM;
        END_IF;
        
        // Trans-membrane pressure monitoring
        rDeltaP := rPressurePreMembrane - rPressurePostMembrane;
        IF rDeltaP > rMaxDeltaP THEN
            bAlarmHighDeltaP := TRUE;
            // Derate pump speed to prevent membrane rupture or excessive hemolysis
            rPumpSpeedCmd := rPumpSpeedCmd * 0.8; 
        END_IF;
        
        // Hemolysis detection heuristic: High RPM but Low Flow suggests cavitation or occlusion
        fbHemolysisDelay(IN := (rPumpSpeedRPM > 3500.0) AND (rActualBloodFlow < 1.0), PT := T#5s);
        IF fbHemolysisDelay.Q THEN
            bAlarmHemolysisRisk := TRUE;
        END_IF;
        
        IF NOT bEnable THEN
            eState := 1; // STANDBY
        END_IF;
        
    3: // EMERGENCY_STOP
        // Everything to safe state
        rPumpSpeedCmd := 0.0;
        bSystemRunning := FALSE;
        // Gas might still flow to keep membrane oxygenated, but for safety, usually baseline
        rSweepO2ValveCmd := 21.0; 
        // Await manual clinician intervention and reset
        
END_CASE;

END_FUNCTION_BLOCK
```"""

new_data = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": assistant_response}
    ]
}

with open("data/synthetic_generation_v3_enterprise.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(new_data) + "\n")
print("Successfully appended ECMO controller data.")
