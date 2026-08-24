import json
import os

base_prompt = "Write a Beckhoff ST program for an automotive marriage station syncing the chassis overhead conveyor with the engine/drivetrain AGV for precise bolt torquing."
base_code = """```iecst
PROGRAM PRG_MarriageStation
VAR
    bConveyorInPosition : BOOL;
    bAGVInPosition : BOOL;
    bStartMarriage : BOOL;
    bMarriageComplete : BOOL;
    nStep : INT;
    
    // Torque tool interface
    bStartTorquing : BOOL;
    bTorquingDone : BOOL;
    bTorquingError : BOOL;
END_VAR

CASE nStep OF
    0: // Wait for both units
        IF bConveyorInPosition AND bAGVInPosition AND bStartMarriage THEN
            nStep := 10;
        END_IF
    10: // Sync motion
        // AGV is locked to conveyor logically
        bStartTorquing := TRUE;
        nStep := 20;
    20: // Wait for bolting
        IF bTorquingDone THEN
            bStartTorquing := FALSE;
            bMarriageComplete := TRUE;
            nStep := 30;
        ELSIF bTorquingError THEN
            bStartTorquing := FALSE;
            nStep := 99;
        END_IF
    30: // Complete
        bMarriageComplete := FALSE;
        nStep := 0;
    99: // Error state
        bStartTorquing := FALSE;
END_CASE
```"""

mut1_prompt = "Write a Beckhoff ST program for an automotive marriage station syncing the chassis overhead conveyor with the engine/drivetrain AGV for precise bolt torquing. Add a critical sub-system: dynamic vision-based alignment correction that offsets the AGV trajectory based on chassis sway."
mut1_code = """```iecst
PROGRAM PRG_MarriageStation_Vision
VAR
    bConveyorInPosition : BOOL;
    bAGVInPosition : BOOL;
    bStartMarriage : BOOL;
    bMarriageComplete : BOOL;
    nStep : INT;
    
    // Vision alignment
    fChassisSwayOffset : LREAL; // Offset received from vision camera
    fAGVTargetPosition : LREAL;
    fAGVCurrentPosition : LREAL;
    bVisionDataValid : BOOL;
    
    // Torque tool interface
    bStartTorquing : BOOL;
    bTorquingDone : BOOL;
    bTorquingError : BOOL;
END_VAR

CASE nStep OF
    0: // Wait for units
        IF bConveyorInPosition AND bAGVInPosition AND bStartMarriage THEN
            nStep := 5;
        END_IF
    5: // Calculate Vision offset
        IF bVisionDataValid THEN
            fAGVTargetPosition := fAGVCurrentPosition + fChassisSwayOffset;
            nStep := 10;
        END_IF
    10: // Sync motion with dynamic offset
        // Drive AGV to fAGVTargetPosition ...
        bStartTorquing := TRUE;
        nStep := 20;
    20: // Wait for bolting
        IF bTorquingDone THEN
            bStartTorquing := FALSE;
            bMarriageComplete := TRUE;
            nStep := 30;
        ELSIF bTorquingError THEN
            nStep := 99;
        END_IF
    30: 
        bMarriageComplete := FALSE;
        nStep := 0;
    99:
        bStartTorquing := FALSE;
END_CASE
```"""

mut2_prompt = "Write a Beckhoff ST program for an automotive marriage station syncing the chassis overhead conveyor with the engine/drivetrain AGV for precise bolt torquing. Include a dynamic vision-based alignment correction that offsets the AGV trajectory based on chassis sway. Furthermore, implement industrial communication via EtherCAT diagnostics and integrate comprehensive fault diagnostics for the servo drives and sensors."
mut2_code = """```iecst
PROGRAM PRG_MarriageStation_EtherCAT
VAR
    bConveyorInPosition, bAGVInPosition, bStartMarriage, bMarriageComplete : BOOL;
    nStep : INT;
    
    // Vision alignment
    fChassisSwayOffset, fAGVTargetPosition, fAGVCurrentPosition : LREAL;
    bVisionDataValid : BOOL;
    
    // Torque tool
    bStartTorquing, bTorquingDone, bTorquingError : BOOL;
    
    // EtherCAT & Diagnostics
    NetId : T_AmsNetId := '192.168.1.10.1.1';
    fbGetSlaveState : FB_EcGetSlaveState;
    nSlaveState : UINT;
    bEcError, bDriveFaultActive, bSensorFaultActive : BOOL;
    sFaultMsg : STRING;
END_VAR

// Continuous EtherCAT Diagnostic Check
fbGetSlaveState(sNetId:=NetId, nSlaveAddr:=1001, bExecute:=TRUE, state=>nSlaveState);
IF nSlaveState <> 8 THEN // 8 = OP State
    bEcError := TRUE;
    sFaultMsg := 'EtherCAT Slave not in OP';
    nStep := 99;
END_IF

IF bDriveFaultActive OR bSensorFaultActive THEN
    sFaultMsg := 'Drive or Sensor Fault';
    nStep := 99;
END_IF

CASE nStep OF
    0:
        IF bConveyorInPosition AND bAGVInPosition AND bStartMarriage AND NOT bEcError THEN
            nStep := 5;
        END_IF
    5:
        IF bVisionDataValid THEN
            fAGVTargetPosition := fAGVCurrentPosition + fChassisSwayOffset;
            nStep := 10;
        END_IF
    10:
        bStartTorquing := TRUE;
        nStep := 20;
    20:
        IF bTorquingDone THEN
            bStartTorquing := FALSE;
            bMarriageComplete := TRUE;
            nStep := 30;
        ELSIF bTorquingError THEN
            nStep := 99;
        END_IF
    30:
        bMarriageComplete := FALSE;
        nStep := 0;
    99:
        bStartTorquing := FALSE;
END_CASE
```"""

mut3_prompt = "Write a Beckhoff ST program for an automotive marriage station syncing the chassis overhead conveyor with the engine/drivetrain AGV for precise bolt torquing, including dynamic vision-based alignment correction, EtherCAT diagnostics, and comprehensive fault diagnostics. Additionally, implement IEC 62443 cybersecurity checks (e.g., verifying secure PLC-to-SCADA communication certificates), a failover mechanism in case of primary PLC failure, and structured SCADA integration using OPC UA."
mut3_code = """```iecst
PROGRAM PRG_MarriageStation_Secure
VAR
    bConveyorInPosition, bAGVInPosition, bStartMarriage, bMarriageComplete : BOOL;
    nStep : INT;
    fChassisSwayOffset, fAGVTargetPosition, fAGVCurrentPosition : LREAL;
    bVisionDataValid : BOOL;
    bStartTorquing, bTorquingDone, bTorquingError : BOOL;
    
    // EtherCAT Diagnostics
    bEcError, bDriveFaultActive, bSensorFaultActive : BOOL;
    
    // IEC 62443 Cybersecurity & SCADA (OPC UA)
    {attribute 'OPC.UA.DA' := '1'}
    stScadaData : ST_ScadaMarriageData;
    bSecureCertValid : BOOL; // Updated via secure key exchange block
    bOpcuALinkActive : BOOL;
    
    // Redundancy / Failover
    bPrimaryPLCActive : BOOL := TRUE;
    bSecondaryHeartbeatOk : BOOL;
    bInitiateFailover : BOOL;
END_VAR

// Cybersecurity and Failover Checks
IF NOT bSecureCertValid OR NOT bOpcuALinkActive THEN
    stScadaData.sStatus := 'SECURITY LOCKDOWN';
    nStep := 100;
END_IF

IF NOT bSecondaryHeartbeatOk AND NOT bPrimaryPLCActive THEN
    bInitiateFailover := TRUE; // Signal secondary to take master
END_IF

CASE nStep OF
    0:
        stScadaData.sStatus := 'WAITING';
        IF bConveyorInPosition AND bAGVInPosition AND bStartMarriage AND NOT bEcError AND bPrimaryPLCActive THEN
            nStep := 5;
        END_IF
    5:
        IF bVisionDataValid THEN
            fAGVTargetPosition := fAGVCurrentPosition + fChassisSwayOffset;
            stScadaData.fCurrentOffset := fChassisSwayOffset;
            nStep := 10;
        END_IF
    10:
        stScadaData.sStatus := 'TORQUING';
        bStartTorquing := TRUE;
        nStep := 20;
    20:
        IF bTorquingDone THEN
            bStartTorquing := FALSE;
            bMarriageComplete := TRUE;
            stScadaData.sStatus := 'COMPLETE';
            nStep := 30;
        ELSIF bTorquingError THEN
            nStep := 99;
        END_IF
    30:
        bMarriageComplete := FALSE;
        nStep := 0;
    99:
        stScadaData.sStatus := 'PROCESS FAULT';
        bStartTorquing := FALSE;
    100:
        // Security/SCADA fault state
        bStartTorquing := FALSE;
END_CASE
```"""

mut4_prompt = "Write a Beckhoff ST program for an automotive marriage station syncing the chassis overhead conveyor with the engine/drivetrain AGV for precise bolt torquing. The system must include vision-based alignment, EtherCAT diagnostics, fault handling, IEC 62443 cybersecurity checks, failover mechanisms, and OPC UA SCADA integration. Finally, add advanced adversarial conditions: sensor drift detection algorithms for the AGV encoders, hardware-in-the-loop (HIL) digital twin synchronization checks, and an automated self-test routine that triggers before every marriage sequence."
mut4_code = """```iecst
PROGRAM PRG_MarriageStation_Adversarial
VAR
    bConveyorInPosition, bAGVInPosition, bStartMarriage, bMarriageComplete : BOOL;
    nStep : INT;
    fChassisSwayOffset, fAGVTargetPosition, fAGVCurrentPosition : LREAL;
    bVisionDataValid : BOOL;
    bStartTorquing, bTorquingDone, bTorquingError : BOOL;
    
    // Security & Comm
    bSecureCertValid, bOpcuALinkActive, bEcError : BOOL;
    bPrimaryPLCActive : BOOL := TRUE;
    
    // Adversarial: Sensor Drift
    fAGVEncoderPrimary, fAGVEncoderSecondary : LREAL;
    fDriftTolerance : LREAL := 0.05; // mm
    bSensorDriftDetected : BOOL;
    
    // Adversarial: HIL Digital Twin
    bHIL_SyncActive : BOOL;
    fHIL_SimulatedPos : LREAL;
    fHIL_Tolerance : LREAL := 1.0; // mm
    bHIL_DeviationFault : BOOL;
    
    // Adversarial: Self-Test
    bSelfTestRunning, bSelfTestPassed : BOOL;
    nTestStep : INT;
END_VAR

// Advanced Diagnostics Processing
IF ABS(fAGVEncoderPrimary - fAGVEncoderSecondary) > fDriftTolerance THEN
    bSensorDriftDetected := TRUE;
    nStep := 99;
END_IF

IF bHIL_SyncActive AND ABS(fAGVCurrentPosition - fHIL_SimulatedPos) > fHIL_Tolerance THEN
    bHIL_DeviationFault := TRUE;
    nStep := 99;
END_IF

CASE nStep OF
    0: // Idle
        IF bStartMarriage AND bSecureCertValid AND NOT bEcError THEN
            bSelfTestRunning := TRUE;
            bSelfTestPassed := FALSE;
            nTestStep := 1;
            nStep := 2; // Go to self-test
        END_IF
    
    2: // Automated Self-Test Routine
        CASE nTestStep OF
            1: // Check comms & bounds
                IF bOpcuALinkActive AND NOT bSensorDriftDetected THEN
                    nTestStep := 2;
                ELSE
                    nStep := 99;
                END_IF
            2: // Check torquing tool interlocks
                IF NOT bTorquingError THEN
                    bSelfTestPassed := TRUE;
                    bSelfTestRunning := FALSE;
                    nStep := 5;
                END_IF
        END_CASE

    5: // Wait for physical position
        IF bSelfTestPassed AND bConveyorInPosition AND bAGVInPosition THEN
            nStep := 10;
        END_IF
        
    10: // Vision Alignment
        IF bVisionDataValid THEN
            fAGVTargetPosition := fAGVCurrentPosition + fChassisSwayOffset;
            nStep := 20;
        END_IF
        
    20: // Sync and Torque
        bStartTorquing := TRUE;
        nStep := 30;
        
    30: // Wait for completion
        IF bTorquingDone THEN
            bStartTorquing := FALSE;
            bMarriageComplete := TRUE;
            nStep := 40;
        ELSIF bTorquingError OR bHIL_DeviationFault THEN
            nStep := 99;
        END_IF
        
    40: // Reset
        bMarriageComplete := FALSE;
        nStep := 0;
        
    99: // Global Fault State
        bStartTorquing := FALSE;
        bSelfTestRunning := FALSE;
END_CASE
```"""

def create_msg(prompt, code):
    return {
        "messages": [
            {"role": "system", "content": "You are a helpful industrial automation programming assistant."},
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": code}
        ]
    }

data = [
    create_msg(base_prompt, base_code),
    create_msg(mut1_prompt, mut1_code),
    create_msg(mut2_prompt, mut2_code),
    create_msg(mut3_prompt, mut3_code),
    create_msg(mut4_prompt, mut4_code)
]

out_dir = r"C:\Users\majip\Downloads\LLM REASEARCH\data\swarm_outputs"
os.makedirs(out_dir, exist_ok=True)

out_file = os.path.join(out_dir, "seed_144.jsonl")
with open(out_file, "w", encoding="utf-8") as f:
    for item in data:
        f.write(json.dumps(item) + "\\n")
