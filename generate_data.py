import json, uuid, os

prompt = "Invent a highly complex control scenario for this domain (e.g., polyol/isocyanate high-pressure mixing head impingement, blowing agent mass flow, and fall-plate kinematics)."
code = """```iec-st
FUNCTION_BLOCK FB_Slabstock_MixHeadControl
VAR_INPUT
    bEnable                 : BOOL; // Enable the mixing head
    fPolyolSetpoint         : REAL; // kg/min
    fIsocyanateSetpoint     : REAL; // kg/min
    fBlowingAgentSetpoint   : REAL; // kg/min
    fCatalystSetpoint       : REAL; // kg/min
    fMixHeadPressureSP      : REAL; // bar
    
    // Physical IO Feedback
    fPolyolMassFlowFB       : REAL; // kg/min
    fIsocyanateMassFlowFB   : REAL; // kg/min
    fBlowingAgentMassFlowFB : REAL; // kg/min
    fCatalystMassFlowFB     : REAL; // kg/min
    fMixHeadPressureFB      : REAL; // bar
    
    fConveyorSpeed          : REAL; // m/min
    fFallPlateAngle         : REAL; // degrees
    
    bEStop                  : BOOL; 
END_VAR

VAR_OUTPUT
    bMixHeadActive          : BOOL;
    fPolyolValveCmd         : REAL; // 0-100%
    fIsocyanateValveCmd     : REAL; // 0-100%
    fBlowingAgentValveCmd   : REAL; // 0-100%
    fCatalystValveCmd       : REAL; // 0-100%
    
    fFallPlateActuatorCmd   : REAL; // 0-100%
    
    bAlarm                  : BOOL;
    iAlarmCode              : INT;
END_VAR

VAR
    // PID Controllers (simulated structures for ST representation)
    PID_Polyol          : FB_PID_Advanced;
    PID_Isocyanate      : FB_PID_Advanced;
    PID_BlowingAgent    : FB_PID_Advanced;
    PID_Catalyst        : FB_PID_Advanced;
    
    fRatioPolyIso       : REAL;
    fRatioDeviation     : REAL;
    
    TON_MixDelay        : TON;
    TON_AlarmDelay      : TON;
    
    iState              : INT;
    
    // Constants
    MAX_RATIO_ERROR     : REAL := 2.5; // %
END_VAR

// State Machine
CASE iState OF
    0: // IDLE
        bMixHeadActive := FALSE;
        fPolyolValveCmd := 0.0;
        fIsocyanateValveCmd := 0.0;
        fBlowingAgentValveCmd := 0.0;
        fCatalystValveCmd := 0.0;
        fFallPlateActuatorCmd := 0.0;
        bAlarm := FALSE;
        iAlarmCode := 0;
        
        IF bEnable AND NOT bEStop THEN
            iState := 10;
        END_IF
        
    10: // PRE-CIRCULATION
        // Start pumping polyol and iso back to tanks to build pressure
        // ...
        TON_MixDelay(IN:=TRUE, PT:=T#5S);
        IF TON_MixDelay.Q THEN
            TON_MixDelay(IN:=FALSE);
            iState := 20;
        END_IF
        
    20: // INJECTION / MIXING
        bMixHeadActive := TRUE;
        
        // Execute PID loops
        PID_Polyol(
            bEnable := TRUE,
            fSetpoint := fPolyolSetpoint,
            fProcessValue := fPolyolMassFlowFB,
            fKp := 1.2, fKi := 0.5, fKd := 0.1,
            fOutput => fPolyolValveCmd
        );
        
        PID_Isocyanate(
            bEnable := TRUE,
            fSetpoint := fIsocyanateSetpoint,
            fProcessValue := fIsocyanateMassFlowFB,
            fKp := 1.5, fKi := 0.6, fKd := 0.15,
            fOutput => fIsocyanateValveCmd
        );
        
        PID_BlowingAgent(
            bEnable := TRUE,
            fSetpoint := fBlowingAgentSetpoint,
            fProcessValue := fBlowingAgentMassFlowFB,
            fKp := 2.0, fKi := 1.0, fKd := 0.05,
            fOutput => fBlowingAgentValveCmd
        );
        
        PID_Catalyst(
            bEnable := TRUE,
            fSetpoint := fCatalystSetpoint,
            fProcessValue := fCatalystMassFlowFB,
            fKp := 0.8, fKi := 0.2, fKd := 0.0,
            fOutput => fCatalystValveCmd
        );
        
        // Kinematic calculation for fall plate based on conveyor speed and foaming profile
        fFallPlateActuatorCmd := fConveyorSpeed * 2.5 + (fFallPlateAngle * 0.5);
        
        // Ratio monitoring (Polyol to Isocyanate)
        IF fIsocyanateMassFlowFB > 0.1 THEN
            fRatioPolyIso := fPolyolMassFlowFB / fIsocyanateMassFlowFB;
            fRatioDeviation := ABS( (fRatioPolyIso - (fPolyolSetpoint / fIsocyanateSetpoint)) / (fPolyolSetpoint / fIsocyanateSetpoint) ) * 100.0;
            
            IF fRatioDeviation > MAX_RATIO_ERROR THEN
                TON_AlarmDelay(IN:=TRUE, PT:=T#2S);
            ELSE
                TON_AlarmDelay(IN:=FALSE);
            END_IF
        END_IF
        
        IF TON_AlarmDelay.Q THEN
            iAlarmCode := 101; // Ratio error
            iState := 999;
        END_IF
        
        IF NOT bEnable OR bEStop THEN
            iState := 0;
        END_IF
        
    999: // FAULT
        bMixHeadActive := FALSE;
        fPolyolValveCmd := 0.0;
        fIsocyanateValveCmd := 0.0;
        fBlowingAgentValveCmd := 0.0;
        fCatalystValveCmd := 0.0;
        fFallPlateActuatorCmd := 0.0;
        bAlarm := TRUE;
        
        IF NOT bEStop AND NOT bEnable THEN
            iState := 0;
        END_IF
        
END_CASE
END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
os.makedirs("data/swarm_raw", exist_ok=True)
with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
    json.dump(record, f)

os.makedirs("data", exist_ok=True)
with open("data/synthetic_generation_v3_enterprise.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\n")
