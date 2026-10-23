import json, uuid, os

st_code = """```iec-st
FUNCTION_BLOCK FB_BOP_AcousticControl
VAR_INPUT
    bEnableAcousticRx : BOOL; (* Enable acoustic receiver *)
    nAcousticSignalStrength : INT; (* Signal strength from subsea modem (dB) *)
    bRxDataReady : BOOL; (* Data packet received *)
    nRxCmdCode : WORD; (* Command code from surface *)
    nRxChecksum : WORD; (* Received checksum *)
    fAccumulatorPressure_psi : REAL; (* Current hydraulic accumulator pressure *)
    fAmbientHydrostatic_psi : REAL; (* Ambient hydrostatic pressure at depth *)
    bManualOverride : BOOL;
END_VAR
VAR_OUTPUT
    bAcousticTxEnable : BOOL; (* Enable acoustic transmitter to reply *)
    nTxStatusCode : WORD; (* Status code to send to surface *)
    bBlindShearRamActuate : BOOL; (* Fire Blind Shear Ram (BSR) *)
    bPipeRamActuate : BOOL; (* Fire Pipe Ram *)
    bAccumulatorChargeCmd : BOOL; (* Command to charge accumulators *)
    nSystemFaultCode : WORD;
    bCommunicationHealthy : BOOL;
END_VAR
VAR
    eState : INT; (* 0:IDLE, 1:DECODING, 2:VALIDATION, 3:EXECUTION, 4:REPLY, 5:FAULT *)
    nCalculatedChecksum : WORD;
    fDifferentialPressure : REAL;
    tCommandTimeout : TON;
    tReplyDelay : TON;
    nRetryCount : INT;
    bValidCmd : BOOL;
    
    (* Constants for Acoustic Telemetry *)
    c_CMD_FIRE_BSR : WORD := 16#A1B2;
    c_CMD_FIRE_PIPE : WORD := 16#C3D4;
    c_CMD_STATUS_REQ : WORD := 16#E5F6;
    c_MIN_SIG_STRENGTH : INT := -85; (* Minimum dBm for reliable comms *)
    c_MIN_DIFF_PRESSURE : REAL := 3000.0; (* Minimum differential pressure in psi to actuate *)
END_VAR

(* Calculate Differential Pressure *)
fDifferentialPressure := fAccumulatorPressure_psi - fAmbientHydrostatic_psi;

(* Timeout for acoustic sequence *)
tCommandTimeout(IN := (eState <> 0), PT := T#30s);
IF tCommandTimeout.Q THEN
    eState := 5;
    nSystemFaultCode := 16#F001; (* Timeout fault *)
END_IF;

(* Main State Machine *)
CASE eState OF
    0:
        bAcousticTxEnable := FALSE;
        bBlindShearRamActuate := FALSE;
        bPipeRamActuate := FALSE;
        bCommunicationHealthy := (nAcousticSignalStrength >= c_MIN_SIG_STRENGTH);
        
        IF bEnableAcousticRx AND bRxDataReady AND bCommunicationHealthy THEN
            eState := 1;
        END_IF;
        
    1:
        (* Simplified Checksum Calculation (XOR with fixed key for example) *)
        nCalculatedChecksum := nRxCmdCode XOR 16#55AA;
        
        IF nCalculatedChecksum = nRxChecksum THEN
            eState := 2;
        ELSE
            nSystemFaultCode := 16#F002; (* Checksum Error *)
            eState := 4; 
        END_IF;
        
    2:
        bValidCmd := FALSE;
        IF (nRxCmdCode = c_CMD_FIRE_BSR) OR (nRxCmdCode = c_CMD_FIRE_PIPE) OR (nRxCmdCode = c_CMD_STATUS_REQ) THEN
            (* Check Hydraulic Interlocks before actuation *)
            IF (nRxCmdCode = c_CMD_FIRE_BSR) OR (nRxCmdCode = c_CMD_FIRE_PIPE) THEN
                IF fDifferentialPressure >= c_MIN_DIFF_PRESSURE THEN
                    bValidCmd := TRUE;
                ELSE
                    nSystemFaultCode := 16#F003; (* Insufficient Hydraulic Pressure *)
                END_IF;
            ELSE
                bValidCmd := TRUE; (* Status request always valid *)
            END_IF;
        ELSE
            nSystemFaultCode := 16#F004; (* Invalid Command Code *)
        END_IF;
        
        IF bValidCmd THEN
            eState := 3;
        ELSE
            eState := 4;
        END_IF;
        
    3:
        IF nRxCmdCode = c_CMD_FIRE_BSR THEN
            bBlindShearRamActuate := TRUE;
            nTxStatusCode := 16#0011; (* BSR Actuated *)
        ELSIF nRxCmdCode = c_CMD_FIRE_PIPE THEN
            bPipeRamActuate := TRUE;
            nTxStatusCode := 16#0022; (* Pipe Ram Actuated *)
        ELSIF nRxCmdCode = c_CMD_STATUS_REQ THEN
            nTxStatusCode := 16#00FF; (* Status OK *)
        END_IF;
        
        eState := 4;
        
    4:
        tReplyDelay(IN := TRUE, PT := T#2s); (* Delay before transmitting reply to avoid multi-path interference *)
        IF tReplyDelay.Q THEN
            bAcousticTxEnable := TRUE;
            tReplyDelay(IN := FALSE); (* Reset timer *)
            eState := 0;
        END_IF;
        
    5:
        bCommunicationHealthy := FALSE;
        IF bManualOverride THEN
            nSystemFaultCode := 16#0000;
            eState := 0;
        END_IF;
END_CASE;

(* Hydraulic Accumulator Management *)
IF fDifferentialPressure < (c_MIN_DIFF_PRESSURE + 500.0) THEN
    bAccumulatorChargeCmd := TRUE;
ELSE
    bAccumulatorChargeCmd := FALSE;
END_IF;

END_FUNCTION_BLOCK
```"""

user_prompt = "You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data. Your specific domain is: Subsea Blowout Preventer (BOP) Acoustic Control."
record = {"messages": [{"role": "user", "content": user_prompt}, {"role": "assistant", "content": st_code}]}

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f)

os.makedirs("data", exist_ok=True)
with open("data/synthetic_generation_v3_enterprise.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\n")
