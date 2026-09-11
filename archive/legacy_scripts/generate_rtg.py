import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Rubber-Tired Gantry (RTG) Crane.
Task: Invent a highly complex control scenario for this domain (e.g., container sway anti-pendulation math, diesel-electric hybrid load sharing, and laser spreader positioning).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."""

code = """```iec-st
FUNCTION_BLOCK FB_RTG_Crane_Control
VAR_INPUT
    bEnable : BOOL;
    fHoistPosition : REAL; // meters
    fTrolleyPosition : REAL; // meters
    fTrolleySpeed : REAL; // m/s
    fGantrySpeed : REAL; // m/s
    fWindSpeed : REAL; // m/s
    fLaserDistance1 : REAL; // mm
    fLaserDistance2 : REAL; // mm
    fLaserDistance3 : REAL; // mm
    fLaserDistance4 : REAL; // mm
    fDieselRPM : REAL;
    fGridVoltage : REAL;
    fGridPowerAvailable : REAL; // kW
    fBatterySOC : REAL; // 0-100%
    fLoadWeight : REAL; // kg
    fTargetTrolleyPos : REAL;
    fTargetHoistPos : REAL;
END_VAR
VAR_OUTPUT
    fTrolleyAccelCmd : REAL;
    fHoistSpeedCmd : REAL;
    fDieselThrottleCmd : REAL;
    fBatteryPowerCmd : REAL;
    fSpreaderSkewCmd : REAL;
    fSpreaderTrimCmd : REAL;
    fSpreaderListCmd : REAL;
    bAlarmSway : BOOL;
    bAlarmPower : BOOL;
END_VAR
VAR
    // Sway control variables
    fPendulumLength : REAL;
    fNaturalFrequency : REAL;
    fSwayAngle : REAL;
    fSwayVelocity : REAL;
    fDampingFactor : REAL := 0.15;
    fTrolleyForce : REAL;
    
    // Spreader Positioning
    fDeltaX : REAL;
    fDeltaY : REAL;
    fDeltaZ : REAL;
    
    // Power Management
    fTotalPowerDemand : REAL;
    fDieselOptimalPower : REAL := 350.0; // kW
    fMaxBatteryDischarge : REAL := 500.0; // kW
    
    // State machine
    nState : INT;
    
    // Timers
    tUpdate : TON;
END_VAR

// Implementation
tUpdate(IN := TRUE, PT := T#10MS);
IF tUpdate.Q THEN
    tUpdate(IN := FALSE);
    
    IF NOT bEnable THEN
        fTrolleyAccelCmd := 0.0;
        fHoistSpeedCmd := 0.0;
        fDieselThrottleCmd := 0.0;
        fBatteryPowerCmd := 0.0;
        RETURN;
    END_IF;

    // 1. Anti-Pendulation (Sway) Math
    // Length of pendulum is essentially hoist position (cable length)
    fPendulumLength := MAX(fHoistPosition, 1.0); 
    // Natural frequency omega = sqrt(g / L)
    fNaturalFrequency := SQRT(9.81 / fPendulumLength);
    
    // Simplified observer for sway angle based on trolley acceleration and wind
    fSwayVelocity := fSwayVelocity - (fNaturalFrequency * fNaturalFrequency * fSwayAngle + 2.0 * fDampingFactor * fNaturalFrequency * fSwayVelocity - (fWindSpeed * 0.01)) * 0.01;
    fSwayAngle := fSwayAngle + fSwayVelocity * 0.01;
    
    // Sway compensation logic
    IF ABS(fSwayAngle) > 0.1 THEN
        bAlarmSway := TRUE;
    ELSE
        bAlarmSway := FALSE;
    END_IF;
    
    // Calculate Trolley Acceleration Command to counter sway while moving to target
    fTrolleyAccelCmd := (fTargetTrolleyPos - fTrolleyPosition) * 0.5 - fTrolleySpeed * 0.2 + (fSwayAngle * 9.81);
    
    // Limit acceleration
    IF fTrolleyAccelCmd > 1.5 THEN fTrolleyAccelCmd := 1.5; END_IF;
    IF fTrolleyAccelCmd < -1.5 THEN fTrolleyAccelCmd := -1.5; END_IF;

    // 2. Laser Spreader Positioning (Micro-motions)
    // Laser sensors at 4 corners of spreader
    fSpreaderSkewCmd := (fLaserDistance1 - fLaserDistance2 + fLaserDistance3 - fLaserDistance4) * 0.001;
    fSpreaderTrimCmd := (fLaserDistance1 + fLaserDistance2 - fLaserDistance3 - fLaserDistance4) * 0.001;
    fSpreaderListCmd := (fLaserDistance1 - fLaserDistance2 - fLaserDistance3 + fLaserDistance4) * 0.001;
    
    // 3. Diesel-Electric Hybrid Load Sharing
    // Calculate total power demand based on load, hoist speed cmd, trolley acceleration
    fHoistSpeedCmd := (fTargetHoistPos - fHoistPosition) * 0.5;
    fTotalPowerDemand := (fLoadWeight * 9.81 * fHoistSpeedCmd / 1000.0) + (fLoadWeight * ABS(fTrolleyAccelCmd) * fTrolleySpeed / 1000.0);
    
    IF fTotalPowerDemand > fGridPowerAvailable THEN
        // Need supplemental power from diesel and battery
        fTotalPowerDemand := fTotalPowerDemand - fGridPowerAvailable;
        
        IF fBatterySOC > 20.0 THEN
            // Use battery up to its max discharge rate
            IF fTotalPowerDemand > fMaxBatteryDischarge THEN
                fBatteryPowerCmd := fMaxBatteryDischarge;
                fTotalPowerDemand := fTotalPowerDemand - fMaxBatteryDischarge;
            ELSE
                fBatteryPowerCmd := fTotalPowerDemand;
                fTotalPowerDemand := 0.0;
            END_IF;
        ELSE
            fBatteryPowerCmd := 0.0;
        END_IF;
        
        // Remaining demand goes to diesel engine
        IF fTotalPowerDemand > 0.0 THEN
            fDieselThrottleCmd := fTotalPowerDemand / fDieselOptimalPower * 100.0;
            IF fDieselThrottleCmd > 100.0 THEN fDieselThrottleCmd := 100.0; END_IF;
        ELSE
            // Idle diesel if battery handles it, but keep running if SOC is dropping
            IF fBatterySOC < 40.0 THEN
                fDieselThrottleCmd := 50.0; // Charge battery
                fBatteryPowerCmd := -200.0; // Negative means charging
            ELSE
                fDieselThrottleCmd := 10.0; // Idle
            END_IF;
        END_IF;
    ELSE
        // Regenerative braking or excess grid power can charge battery
        IF fTotalPowerDemand < -50.0 AND fBatterySOC < 95.0 THEN
            fBatteryPowerCmd := fTotalPowerDemand; // Charge
        ELSE
            fBatteryPowerCmd := 0.0;
        END_IF;
        fDieselThrottleCmd := 0.0; // Engine off or idle
    END_IF;
    
    // Alarm on power deficiency
    IF fTotalPowerDemand > fDieselOptimalPower THEN
        bAlarmPower := TRUE;
    ELSE
        bAlarmPower := FALSE;
    END_IF;

END_IF;
END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f)
print(f"Saved to {filename}")
