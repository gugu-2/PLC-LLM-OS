import json, uuid, os

os.makedirs("data/swarm_raw", exist_ok=True)

code = """```iec-st
FUNCTION_BLOCK FB_ExtrusionBlowMolding
VAR_INPUT
    bEnable : BOOL;
    bStartCycle : BOOL;
    bEmergencyStop : BOOL;
    
    // Parison Control
    rActualExtruderSpeed : REAL; // RPM
    rAccumulatorPosition : REAL; // mm
    arThicknessProfileSetpoints : ARRAY[0..99] OF REAL; // 0-100%
    
    // Clamp Control
    rActualClampPosition : REAL; // mm
    rTargetClampTonnage : REAL; // kN
    rActualClampForce : REAL; // kN
    
    // Blow Pin Control
    rActualBlowPressure : REAL; // bar
    rTargetBlowPressure1 : REAL; // bar (Pre-blow)
    rTargetBlowPressure2 : REAL; // bar (Main-blow)
END_VAR

VAR_OUTPUT
    bMachineReady : BOOL;
    bCycleActive : BOOL;
    bAlarmActive : BOOL;
    iAlarmCode : INT;
    
    // Parison Control
    rServoValveCommand : REAL; // 0-100%
    
    // Clamp Control
    rClampServoVelocityCmd : REAL; // mm/s
    rClampServoTorqueCmd : REAL; // Nm
    
    // Blow Pin
    rProportionalAirValveCmd : REAL; // 0-100%
END_VAR

VAR
    // State machine
    eState : (INIT, IDLE, EXTRUDE_PARISON, CLAMP_CLOSE, BLOW_PIN_INSERT, PRE_BLOW, MAIN_BLOW, EXHAUST, CLAMP_OPEN, EJECT, FAULT);
    
    // Parison profile calculation
    iCurrentProfileIndex : INT;
    rInterpolatedThickness : REAL;
    rTotalAccumulatorStroke : REAL := 250.0; // mm
    rAccumulatorStrokePerPoint : REAL;
    
    // Timers
    tPreBlowTimer : TON;
    tMainBlowTimer : TON;
    tExhaustTimer : TON;
    
    // PID for Blow Pressure
    fbBlowPressurePID : PID;
    
    // Clamp control variables
    rClampPositionError : REAL;
    rClampForceError : REAL;
    
END_VAR

// Implementation
IF bEmergencyStop THEN
    eState := FAULT;
    iAlarmCode := 999;
END_IF;

CASE eState OF
    INIT:
        bMachineReady := FALSE;
        bCycleActive := FALSE;
        bAlarmActive := FALSE;
        rServoValveCommand := 0.0;
        rClampServoVelocityCmd := 0.0;
        rClampServoTorqueCmd := 0.0;
        rProportionalAirValveCmd := 0.0;
        rAccumulatorStrokePerPoint := rTotalAccumulatorStroke / 100.0;
        IF bEnable THEN
            eState := IDLE;
            bMachineReady := TRUE;
        END_IF;
        
    IDLE:
        bMachineReady := TRUE;
        bCycleActive := FALSE;
        IF bStartCycle AND NOT bAlarmActive THEN
            eState := EXTRUDE_PARISON;
            bCycleActive := TRUE;
        END_IF;
        
    EXTRUDE_PARISON:
        // Calculate parison wall thickness profiling based on accumulator position
        iCurrentProfileIndex := REAL_TO_INT((rTotalAccumulatorStroke - rAccumulatorPosition) / rAccumulatorStrokePerPoint);
        
        IF iCurrentProfileIndex < 0 THEN iCurrentProfileIndex := 0; END_IF;
        IF iCurrentProfileIndex > 99 THEN iCurrentProfileIndex := 99; END_IF;
        
        rInterpolatedThickness := arThicknessProfileSetpoints[iCurrentProfileIndex];
        
        // Output to servo valve (WDS - Wall Thickness Distribution System)
        rServoValveCommand := rInterpolatedThickness;
        
        IF rAccumulatorPosition <= 5.0 THEN // End of extrusion
            eState := CLAMP_CLOSE;
        END_IF;
        
    CLAMP_CLOSE:
        rClampPositionError := 0.0 - rActualClampPosition; // Target is 0.0 mm (fully closed)
        
        IF rActualClampPosition > 10.0 THEN
            // Velocity control mode
            rClampServoVelocityCmd := LIMIT(MN := -200.0, IN := rClampPositionError * 5.0, MX := 200.0);
            rClampServoTorqueCmd := 100.0; // Limit torque during velocity phase
        ELSE
            // Tonnage buildup (Force control mode)
            rClampServoVelocityCmd := 5.0; // Slow speed during lock
            rClampForceError := rTargetClampTonnage - rActualClampForce;
            
            // PI control for tonnage
            rClampServoTorqueCmd := rClampServoTorqueCmd + (rClampForceError * 0.1);
            rClampServoTorqueCmd := LIMIT(MN := 0.0, IN := rClampServoTorqueCmd, MX := 500.0);
            
            IF ABS(rClampForceError) < (rTargetClampTonnage * 0.02) THEN // Within 2% of target
                eState := BLOW_PIN_INSERT;
            END_IF;
        END_IF;
        
    BLOW_PIN_INSERT:
        // Assume mechanical insert completes in fixed time or position
        tPreBlowTimer(IN := TRUE, PT := T#500MS);
        IF tPreBlowTimer.Q THEN
            tPreBlowTimer(IN := FALSE);
            eState := PRE_BLOW;
        END_IF;
        
    PRE_BLOW:
        fbBlowPressurePID(
            ACT := rActualBlowPressure,
            SET := rTargetBlowPressure1,
            SUP := 0.0,
            OFS := 0.0,
            M_I := TRUE,
            MAN_IN := 0.0,
            KP := 2.5,
            TR := 0.5,
            TD := 0.0,
            CYCLE := 0.01 // Assuming 10ms cycle
        );
        rProportionalAirValveCmd := fbBlowPressurePID.Y;
        
        tMainBlowTimer(IN := TRUE, PT := T#1500MS);
        IF tMainBlowTimer.Q THEN
            tMainBlowTimer(IN := FALSE);
            eState := MAIN_BLOW;
        END_IF;
        
    MAIN_BLOW:
        fbBlowPressurePID(
            ACT := rActualBlowPressure,
            SET := rTargetBlowPressure2,
            SUP := 0.0,
            OFS := 0.0,
            M_I := TRUE,
            MAN_IN := 0.0,
            KP := 2.5,
            TR := 0.5,
            TD := 0.0,
            CYCLE := 0.01 
        );
        rProportionalAirValveCmd := fbBlowPressurePID.Y;
        
        tExhaustTimer(IN := TRUE, PT := T#3000MS); // Cure time
        IF tExhaustTimer.Q THEN
            tExhaustTimer(IN := FALSE);
            rProportionalAirValveCmd := 0.0;
            eState := EXHAUST;
        END_IF;
        
    EXHAUST:
        rProportionalAirValveCmd := 0.0;
        IF rActualBlowPressure < 1.0 THEN
            eState := CLAMP_OPEN;
        END_IF;
        
    CLAMP_OPEN:
        rClampPositionError := 500.0 - rActualClampPosition; // Target is 500.0 mm (fully open)
        rClampServoVelocityCmd := LIMIT(MN := -200.0, IN := rClampPositionError * 5.0, MX := 200.0);
        rClampServoTorqueCmd := 100.0;
        
        IF rActualClampPosition >= 495.0 THEN
            eState := EJECT;
        END_IF;
        
    EJECT:
        // Ejection logic
        eState := IDLE;
        
    FAULT:
        bAlarmActive := TRUE;
        bMachineReady := FALSE;
        rServoValveCommand := 0.0;
        rClampServoVelocityCmd := 0.0;
        rClampServoTorqueCmd := 0.0;
        rProportionalAirValveCmd := 0.0;
        IF NOT bEmergencyStop THEN
            eState := INIT;
        END_IF;
END_CASE;
```"""

record = {
    "messages": [
        {"role": "user", "content": "Write a highly complex control scenario for an Extrusion Blow Molding Machine in Structured Text (ST). Ensure it includes parison wall thickness profiling, toggle clamp tonnage servo locking, and blow pin proportional air control."},
        {"role": "assistant", "content": code}
    ]
}

filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)

print(f"File saved to {filename}")
