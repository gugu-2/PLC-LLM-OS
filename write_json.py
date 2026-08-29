import json, uuid, os
os.makedirs('data/swarm_raw', exist_ok=True)
prompt = "You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.\nYour specific domain is: Subsea Blowout Preventer (BOP) Control Pod.\nTask: Invent a highly complex control scenario for this domain (e.g., acoustic telemetry signal decoding, hydraulic accumulator discharge matrices, and emergency shear ram actuation).\nWrite a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."
code = """```iec-st
FUNCTION_BLOCK FB_SubseaBOP_ControlPod
TITLE = 'Subsea BOP Control Pod - Emergency Disconnect Sequence and Acoustic Telemetry'
VERSION : '1.0'
AUTHOR : 'Lumina Elite Data Architect'

VAR_INPUT
    bEnableSystem         : BOOL; // System Enable
    arrAcousticSignal     : ARRAY[0..15] OF BYTE; // Incoming acoustic telemetry data arrays mapped from hydrophones
    rHydraulicPress_A     : REAL; // Accumulator Bank A Pressure (psi) - Primary hydraulic source
    rHydraulicPress_B     : REAL; // Accumulator Bank B Pressure (psi) - Secondary hydraulic source
    rWellborePressure     : REAL; // Wellbore Pressure (psi) - Annular pressure monitoring
    bManualShearActuate   : BOOL; // Surface command manual override via umbilical
    bDeadmanArm           : BOOL; // Deadman system armed status (loss of comms and hydraulic power)
    bAutoshearArm         : BOOL; // Autoshear system armed status (LMRP disconnect detection)
END_VAR

VAR_OUTPUT
    bBlindShearRamClose   : BOOL; // Command to close Blind Shear Rams (BSR) to seal wellbore
    bCasingShearRamClose  : BOOL; // Command to close Casing Shear Rams (CSR) to cut pipe
    bLMRPDisconnect       : BOOL; // Lower Marine Riser Package (LMRP) disconnect command
    rAccumulatorDischarge : REAL; // Calculated discharge rate required from banks (GPM)
    wStatusWord           : WORD; // Pod Status diagnostic word for telemetry
    bAcousticAck          : BOOL; // Acknowledge signal to surface via acoustic ping
END_VAR

VAR
    // Internal State variables
    eState                : INT := 0; // State machine step tracking
    bValidAcousticCommand : BOOL; // Indicates CRC and payload decoded successfully
    bEmergencyCondition   : BOOL; // Global emergency flag trigger
    rMinRequiredPressure  : REAL := 3000.0; // Minimum psi to successfully actuate shear rams
    rTotalAvailablePress  : REAL; // Sum of Bank A and Bank B
    bPressureCritical     : BOOL; // Flag indicating insufficient hydraulic energy
    
    // Decoded telemetry commands from acoustic matrix
    bCmd_ArmEDS           : BOOL; // Arm Emergency Disconnect Sequence
    bCmd_FireEDS          : BOOL; // Execute Emergency Disconnect Sequence
    bCmd_PingStatus       : BOOL; // Telemetry status request ping
    bCmd_ResetPod         : BOOL; // Reset state machine to idle
    
    iChecksum             : INT; // Running sum for telemetry validation
    i                     : INT; // Loop index
    
    // Timers
    tShearDelay           : TON; // Delay between Casing shear and Blind shear
    tDisconnectDelay      : TON; // Delay before releasing LMRP
END_VAR

// -----------------------------------------------------------------------------
// [0] INITIALIZATION AND SAFETY INTERLOCKS
// -----------------------------------------------------------------------------
IF NOT bEnableSystem THEN
    bBlindShearRamClose := FALSE;
    bCasingShearRamClose := FALSE;
    bLMRPDisconnect := FALSE;
    wStatusWord := 16#0000;
    eState := 0;
    RETURN;
END_IF;

// -----------------------------------------------------------------------------
// [1] ACOUSTIC TELEMETRY DECODING MATRIX
// -----------------------------------------------------------------------------
// The incoming acoustic signal is a 16-byte packet. 
// Bytes 0-13 represent the payload and instruction matrix.
// Bytes 14-15 represent a 16-bit CRC/Checksum.
// Simplifying CRC for logic model: sum of bytes 0-13 MOD 256.

iChecksum := 0;
FOR i := 0 TO 13 DO
    iChecksum := iChecksum + BYTE_TO_INT(arrAcousticSignal[i]);
END_FOR;

IF (iChecksum MOD 256) = BYTE_TO_INT(arrAcousticSignal[14]) THEN
    bValidAcousticCommand := TRUE;
ELSE
    bValidAcousticCommand := FALSE;
    wStatusWord := wStatusWord OR 16#0001; // Set Telemetry Error Bit in status word
END_IF;

IF bValidAcousticCommand THEN
    // Decode specific instruction bits from payload matrix (Bytes 0-3)
    bCmd_ArmEDS     := (arrAcousticSignal[0] = 16#AA);
    bCmd_FireEDS    := (arrAcousticSignal[1] = 16#FF) AND bCmd_ArmEDS;
    bCmd_PingStatus := (arrAcousticSignal[2] = 16#01);
    bCmd_ResetPod   := (arrAcousticSignal[3] = 16#CC);
    
    IF bCmd_PingStatus THEN
        bAcousticAck := TRUE;
    ELSE
        bAcousticAck := FALSE;
    END_IF;
    
    // Handle Remote Reset
    IF bCmd_ResetPod AND eState >= 40 THEN
        eState := 0;
        bBlindShearRamClose := FALSE;
        bCasingShearRamClose := FALSE;
        bLMRPDisconnect := FALSE;
        wStatusWord := 16#0000;
    END_IF;
END_IF;

// -----------------------------------------------------------------------------
// [2] HYDRAULIC ACCUMULATOR DISCHARGE MATRICES
// -----------------------------------------------------------------------------
rTotalAvailablePress := rHydraulicPress_A + rHydraulicPress_B;
bPressureCritical := (rTotalAvailablePress < rMinRequiredPressure);

IF bPressureCritical THEN
    wStatusWord := wStatusWord OR 16#0002; // Low Pressure Alarm Bit
ELSE
    wStatusWord := wStatusWord AND 16#FFFD; // Clear Low Pressure Alarm Bit
END_IF;

// -----------------------------------------------------------------------------
// [3] EMERGENCY CONDITION LOGIC (DEADMAN, AUTOSHEAR, OR COMMANDED)
// -----------------------------------------------------------------------------
// The EDS can be triggered via 3 main pathways:
// 1. Acoustic Telemetry (Surface Command)
// 2. Manual Umbilical Override (Surface Command)
// 3. Deadman System (Loss of communications/power + Blowout pressure profile)

bEmergencyCondition := bCmd_FireEDS OR bManualShearActuate OR 
                       (bDeadmanArm AND bPressureCritical AND (rWellborePressure > 10000.0)) OR
                       bAutoshearArm;

// -----------------------------------------------------------------------------
// [4] EXECUTION STATE MACHINE FOR EMERGENCY SHEAR RAM ACTUATION
// -----------------------------------------------------------------------------
CASE eState OF
    0: // IDLE AND MONITORING
        IF bEmergencyCondition AND NOT bPressureCritical THEN
            eState := 10;
        ELSIF bEmergencyCondition AND bPressureCritical THEN
            wStatusWord := wStatusWord OR 16#0004; // Error: Insufficient energy to fire EDS
        END_IF;
        
    10: // FIRE CASING SHEAR RAMS
        bCasingShearRamClose := TRUE;
        rAccumulatorDischarge := 50.0; // Demand 50 GPM discharge rate from accumulators
        
        // Initiate timer for blind shear delay (e.g., waiting for pipe to be cut and clear)
        tShearDelay(IN := TRUE, PT := T#5s);
        
        IF tShearDelay.Q THEN
            tShearDelay(IN := FALSE); // Reset timer
            eState := 20;
        END_IF;
        
    20: // FIRE BLIND SHEAR RAMS
        bBlindShearRamClose := TRUE;
        rAccumulatorDischarge := 125.0; // Peak demand 125 GPM discharge rate required to seal
        
        // Initiate timer for LMRP disconnect delay
        tDisconnectDelay(IN := TRUE, PT := T#10s);
        
        IF tDisconnectDelay.Q THEN
            tDisconnectDelay(IN := FALSE); // Reset timer
            eState := 30;
        END_IF;
        
    30: // DISCONNECT LOWER MARINE RISER PACKAGE (LMRP)
        bLMRPDisconnect := TRUE;
        wStatusWord := wStatusWord OR 16#8000; // Sequence Complete Bit
        rAccumulatorDischarge := 0.0; // End of high-pressure dynamic demand
        eState := 40;
        
    40: // SEQUENCE COMPLETE LATCH
        // Remain in this state until manually reset via acoustic telemetry or recovery
        // Continually broadcast EDS complete ping on acknowledge channel
        bAcousticAck := TRUE; 
        
    ELSE
        eState := 0; // Fallback to safe idle state on invalid memory
END_CASE;

END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)
print("Saved to", filename)
