import json, uuid, os
content = """```iec-st
FUNCTION_BLOCK FB_HydroTurbine_Control
VAR_INPUT
    bStartSeq : BOOL; (* Start sequence command *)
    bStopSeq : BOOL; (* Stop sequence command *)
    bEmergencyStop : BOOL; (* Emergency stop *)
    rGridFreq : REAL; (* Grid frequency in Hz *)
    rGridVoltage : REAL; (* Grid voltage in kV *)
    rGenFreq : REAL; (* Generator frequency in Hz *)
    rGenVoltage : REAL; (* Generator voltage in kV *)
    rWaterHead : REAL; (* Net water head in meters *)
    rFlowRate : REAL; (* Current flow rate m3/s *)
    rLoadSetpoint : REAL; (* Desired MW load *)
END_VAR

VAR_OUTPUT
    rWicketGatePos_SP : REAL; (* Setpoint for wicket gates % *)
    rRunnerBladePos_SP : REAL; (* Setpoint for runner blades % *)
    bSyncBreakerClose : BOOL; (* Command to close sync breaker *)
    bExcitationEnable : BOOL; (* Enable generator excitation *)
    bBrakeApply : BOOL; (* Apply mechanical brakes *)
    iState : INT; (* Current state of sequence *)
    bReadyToSync : BOOL; (* Generator ready to sync *)
    bError : BOOL; (* Fault condition *)
    iErrorCode : INT; (* Error code *)
END_VAR

VAR
    rtStart : R_TRIG;
    rtStop : R_TRIG;
    tSyncTimer : TON;
    tBrakeTimer : TON;
    tWaitTimer : TON;
    
    rSpeedError : REAL;
    rVoltError : REAL;
    rPhaseDiff : REAL; (* Simulated phase difference *)
    
    Kp_Speed : REAL := 2.5;
    Ki_Speed : REAL := 0.5;
    Kp_Volt : REAL := 1.2;
    Ki_Volt : REAL := 0.3;
    
    rSpeedIntegral : REAL := 0.0;
    rVoltIntegral : REAL := 0.0;
    
    rOptimalBladeAngle : REAL;
    rMaxGatePos : REAL := 95.0;
END_VAR

(* Main State Machine *)
rtStart(CLK:= bStartSeq);
rtStop(CLK:= bStopSeq);

IF bEmergencyStop THEN
    iState := 99; (* Emergency state *)
END_IF;

CASE iState OF
    0: (* IDLE *)
        bSyncBreakerClose := FALSE;
        bExcitationEnable := FALSE;
        rWicketGatePos_SP := 0.0;
        rRunnerBladePos_SP := 0.0;
        IF rtStart.Q AND rWaterHead > 10.0 THEN
            bBrakeApply := FALSE;
            iState := 10;
        END_IF;
        
    10: (* PRE-LUBE & AUXILIARIES *)
        tWaitTimer(IN:= TRUE, PT:= T#5S);
        IF tWaitTimer.Q THEN
            tWaitTimer(IN:= FALSE);
            iState := 20;
        END_IF;
        
    20: (* ROLL-OFF & ACCELERATION *)
        (* Open wicket gates slightly to overcome inertia *)
        rWicketGatePos_SP := 15.0;
        rRunnerBladePos_SP := 10.0;
        IF rGenFreq > 5.0 THEN
            iState := 30;
        END_IF;
        
    30: (* SPEED-NO-LOAD CONTROL *)
        rSpeedError := rGridFreq - rGenFreq;
        rSpeedIntegral := rSpeedIntegral + (rSpeedError * 0.1);
        rWicketGatePos_SP := (Kp_Speed * rSpeedError) + (Ki_Speed * rSpeedIntegral) + 20.0;
        
        IF rWicketGatePos_SP > 40.0 THEN
            rWicketGatePos_SP := 40.0;
        END_IF;
        
        IF ABS(rSpeedError) < 0.2 THEN
            tWaitTimer(IN:= TRUE, PT:= T#10S);
            IF tWaitTimer.Q THEN
                tWaitTimer(IN:= FALSE);
                iState := 40;
            END_IF;
        ELSE
            tWaitTimer(IN:= FALSE);
        END_IF;
        
    40: (* EXCITATION AND VOLTAGE MATCHING *)
        bExcitationEnable := TRUE;
        rVoltError := rGridVoltage - rGenVoltage;
        rVoltIntegral := rVoltIntegral + (rVoltError * 0.1);
        
        IF ABS(rVoltError) < 0.5 THEN
            bReadyToSync := TRUE;
            iState := 50;
        END_IF;
        
    50: (* SYNCHRONIZATION *)
        (* Assuming an external synchrocheck relay monitors phase angle *)
        (* Here we simulate closing when conditions are met *)
        tSyncTimer(IN:= bReadyToSync, PT:= T#2S);
        IF tSyncTimer.Q THEN
            bSyncBreakerClose := TRUE;
            iState := 60;
        END_IF;
        
    60: (* LOADED & 3D CAM RELATIONSHIP *)
        (* Calculate optimal runner blade position based on net head and wicket gate position (Cam profile) *)
        rOptimalBladeAngle := (rWicketGatePos_SP * 0.8) + (rWaterHead * 0.1);
        IF rOptimalBladeAngle > 100.0 THEN
            rOptimalBladeAngle := 100.0;
        END_IF;
        rRunnerBladePos_SP := rOptimalBladeAngle;
        
        (* Load control based on Setpoint *)
        rWicketGatePos_SP := (rLoadSetpoint / 100.0) * rMaxGatePos;
        
        IF rtStop.Q THEN
            iState := 70;
        END_IF;
        
    70: (* UNLOADING *)
        rWicketGatePos_SP := rWicketGatePos_SP - 0.5;
        IF rWicketGatePos_SP <= 0.0 THEN
            bSyncBreakerClose := FALSE;
            bExcitationEnable := FALSE;
            iState := 80;
        END_IF;
        
    80: (* BRAKING *)
        IF rGenFreq < 15.0 THEN
            bBrakeApply := TRUE;
        END_IF;
        IF rGenFreq < 0.5 THEN
            bBrakeApply := FALSE;
            iState := 0;
        END_IF;
        
    99: (* EMERGENCY SHUTDOWN *)
        rWicketGatePos_SP := 0.0;
        bSyncBreakerClose := FALSE;
        bExcitationEnable := FALSE;
        IF rGenFreq < 20.0 THEN
            bBrakeApply := TRUE;
        END_IF;
        bError := TRUE;
        iErrorCode := 1001;
        
END_CASE;
END_FUNCTION_BLOCK
```"""

record = {
    'messages': [
        {
            'role': 'user',
            'content': 'You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.\nYour specific domain is: Multi-Megawatt Hydroelectric Turbine.\nTask: Invent a highly complex control scenario for this domain (e.g., Kaplan runner blade pitch adjustment, guide vane wicket gate sequencing, and generator synchronizing).\nWrite a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O.'
        },
        {
            'role': 'assistant',
            'content': content
        }
    ]
}

os.makedirs('data/swarm_raw', exist_ok=True)
filename = f'data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json'
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(record, f)

# System instruction 5: Append this JSON object as a single line to data/synthetic_generation_v3_enterprise.jsonl
os.makedirs('data', exist_ok=True)
with open('data/synthetic_generation_v3_enterprise.jsonl', 'a', encoding='utf-8') as f:
    f.write(json.dumps(record) + '\n')
    
print(filename)
