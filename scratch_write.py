import json

user_prompt = """You are acting as a Lead Aviation Integrator at a major international airport (e.g., Denver or Dubai). Evolve a basic array block into a massive ICS (Individual Carrier System) Baggage Handling routing matrix.

Technical Specifications required in the ST code:
1. RFID (Radio Frequency Identification) read/write tracking at 10 meters per second.
2. High-speed diverter paddle actuation using predictive encoder-based timing windows.
3. Early Baggage Storage (EBS) automated crane sequencing for holding layover luggage.
4. Anti-gridlock cascading stop logic if a downstream TSA explosive detection scanner faults."""

assistant_response = """Here is the evolved IEC 61131-3 Structured Text (ST) implementation for the massive ICS Baggage Handling routing matrix. This code introduces high-speed tracking arrays, precision diverter paddle timing based on encoder pulses, EBS automated crane integration, and a rigorous cascading stop algorithm to prevent gridlock.

```iecst
FUNCTION_BLOCK "FB_ICS_RoutingMatrix_Master"
TITLE = 'Massive ICS Baggage Handling Matrix'
AUTHOR : 'Lumina Elite Synthetics'
VERSION : '5.0'

// -----------------------------------------------------------------------------
// TECHNICAL SPECIFICATIONS
// 1. RFID read/write tracking at 10 meters per second.
// 2. High-speed diverter paddle actuation using predictive encoder-based timing.
// 3. Early Baggage Storage (EBS) automated crane sequencing.
// 4. Anti-gridlock cascading stop logic for TSA scanner faults.
// -----------------------------------------------------------------------------

TYPE "UDT_BaggageCarrier" :
    STRUCT
        BagID : STRING[32];           // IATA 10-digit license plate or RFID tag
        Occupied : BOOL;              // Carrier physical presence
        EnterPosPulses : UDINT;       // Encoder pulse count at read point
        DestCode : INT;               // 1=Flight, 2=TSA EDS, 3=EBS
        IsLayover : BOOL;             // True if flight is > 3 hours away
        RequiresScreening : BOOL;     // True if TSA flag is raised
    END_STRUCT;
END_TYPE

VAR_INPUT
    EnableSystem : BOOL; 
    
    // Encoder Feedback for 10 m/s predictive tracking
    MasterEncoderPulses : UDINT;
    
    // High-speed RFID Interfaces (Zones 1 to 10)
    RfidTriggers : ARRAY[1..10] OF BOOL;
    RfidDataRead : ARRAY[1..10] OF STRING[32];
    
    // Downstream TSA Scanner
    TsaScannerFault : BOOL;          // Scanner critical error
    
    // EBS Crane System
    EbsCraneReady : BOOL;
    EbsCranePosAck : BOOL;
END_VAR

VAR_OUTPUT
    // Actuators and Conveyor Drives
    DiverterPaddles : ARRAY[1..10] OF BOOL; // High-speed pneumatic diverters
    ConveyorRunCmd : ARRAY[1..20] OF BOOL;  // Zone drive run commands
    
    // RFID Write Interfaces
    RfidWriteReq : ARRAY[1..10] OF BOOL;
    RfidDataWrite : ARRAY[1..10] OF STRING[32];
    
    // EBS Crane
    EbsCraneMoveCmd : BOOL;
    EbsTargetLane : INT;
    
    // System Alarms
    SystemGridlockAlarm : BOOL;
END_VAR

VAR
    // The Massive ICS Routing Matrix
    CarrierMatrix : ARRAY[1..50, 1..10] OF "UDT_BaggageCarrier";
    
    // Diverter Timing Variables
    DiverterOffsetPulses : UDINT := 5000; // Distance to diverter
    DiverterWindowPulses : UDINT := 50;   // Actuation window length
    PredictedWinStart : UDINT;
    PredictedWinEnd : UDINT;
    
    // Loop iterators
    ZoneIdx : INT;
    CarrierIdx : INT;
    
    // Anti-Gridlock Cascade
    CascadeStop : ARRAY[1..20] OF BOOL;
    
    // EBS State Machine
    EbsState : INT;
END_VAR

BEGIN
    IF NOT EnableSystem THEN
        SystemGridlockAlarm := FALSE;
        EbsCraneMoveCmd := FALSE;
        FOR ZoneIdx := 1 TO 20 DO ConveyorRunCmd[ZoneIdx] := FALSE; END_FOR;
        RETURN;
    END_IF;

    // =========================================================================
    // 1. ANTI-GRIDLOCK CASCADING STOP LOGIC
    // =========================================================================
    // If the downstream TSA Explosive Detection System faults, we must cascade
    // a stop backward through the ICS to prevent carrier collisions.
    IF TsaScannerFault THEN
        SystemGridlockAlarm := TRUE;
        CascadeStop[20] := TRUE; // Immediate stop on the entry to scanner
        // Cascade backwards from zone 19 down to 1
        FOR ZoneIdx := 19 TO 1 BY -1 DO
            CascadeStop[ZoneIdx] := CascadeStop[ZoneIdx+1]; 
        END_FOR;
    ELSE
        SystemGridlockAlarm := FALSE;
        FOR ZoneIdx := 1 TO 20 DO
            CascadeStop[ZoneIdx] := FALSE;
        END_FOR;
    END_IF;

    FOR ZoneIdx := 1 TO 20 DO
        ConveyorRunCmd[ZoneIdx] := NOT CascadeStop[ZoneIdx];
    END_FOR;

    // =========================================================================
    // 2. 10 M/S RFID READ/WRITE TRACKING 
    // =========================================================================
    // Process high-speed triggers.
    FOR CarrierIdx := 1 TO 10 DO
        IF RfidTriggers[CarrierIdx] THEN
            // Register baggage into the matrix
            CarrierMatrix[1, CarrierIdx].BagID := RfidDataRead[CarrierIdx];
            CarrierMatrix[1, CarrierIdx].Occupied := TRUE;
            CarrierMatrix[1, CarrierIdx].EnterPosPulses := MasterEncoderPulses;
            
            // Dynamic Routing Assignment
            IF LEFT(RfidDataRead[CarrierIdx], 3) = 'TSA' THEN
                CarrierMatrix[1, CarrierIdx].DestCode := 2; 
                CarrierMatrix[1, CarrierIdx].IsLayover := FALSE;
            ELSIF LEFT(RfidDataRead[CarrierIdx], 3) = 'EBS' THEN
                CarrierMatrix[1, CarrierIdx].DestCode := 3; 
                CarrierMatrix[1, CarrierIdx].IsLayover := TRUE;
            ELSE
                CarrierMatrix[1, CarrierIdx].DestCode := 1; 
            END_IF;
            
            // Write tracking acknowledge to the RFID tag
            RfidDataWrite[CarrierIdx] := CONCAT(RfidDataRead[CarrierIdx], '_TRK');
            RfidWriteReq[CarrierIdx] := TRUE;
        ELSE
            RfidWriteReq[CarrierIdx] := FALSE;
        END_IF;
    END_FOR;

    // =========================================================================
    // 3. HIGH-SPEED PREDICTIVE DIVERTER PADDLE ACTUATION
    // =========================================================================
    // Calculate precise window based on master encoder pulses for TSA routing.
    FOR CarrierIdx := 1 TO 10 DO
        IF CarrierMatrix[1, CarrierIdx].Occupied AND (CarrierMatrix[1, CarrierIdx].DestCode = 2) THEN
            PredictedWinStart := CarrierMatrix[1, CarrierIdx].EnterPosPulses + DiverterOffsetPulses;
            PredictedWinEnd := PredictedWinStart + DiverterWindowPulses;
            
            // Actuate paddle precisely within the encoder window
            IF (MasterEncoderPulses >= PredictedWinStart) AND (MasterEncoderPulses <= PredictedWinEnd) THEN
                DiverterPaddles[CarrierIdx] := TRUE;
                // Clear matrix entry once bag is diverted
                CarrierMatrix[1, CarrierIdx].Occupied := FALSE;
            ELSIF MasterEncoderPulses > PredictedWinEnd THEN
                DiverterPaddles[CarrierIdx] := FALSE;
            END_IF;
        ELSE
            DiverterPaddles[CarrierIdx] := FALSE;
        END_IF;
    END_FOR;

    // =========================================================================
    // 4. EBS (EARLY BAGGAGE STORAGE) AUTOMATED CRANE SEQUENCING
    // =========================================================================
    // Handshake sequence for moving layover luggage into automated storage.
    CASE EbsState OF
        0: // Idle - Wait for layover bag at Crane Pickup (Assume Carrier 1 is pick position)
            IF CarrierMatrix[1, 1].Occupied AND CarrierMatrix[1, 1].IsLayover AND EbsCraneReady THEN
                EbsTargetLane := 42; // Example dynamic rack assignment
                EbsCraneMoveCmd := TRUE;
                EbsState := 1;
            END_IF;
            
        1: // Wait for crane to acknowledge target position reached
            IF EbsCranePosAck THEN
                EbsCraneMoveCmd := FALSE;
                CarrierMatrix[1, 1].Occupied := FALSE; // Bag removed from ICS
                EbsState := 2;
            END_IF;
            
        2: // Return to Idle once crane drops the ack
            IF NOT EbsCranePosAck THEN
                EbsState := 0;
            END_IF;
    END_CASE;

END_FUNCTION_BLOCK
```"""

record = {
    "messages": [
        {"role": "user", "content": user_prompt},
        {"role": "assistant", "content": assistant_response}
    ]
}

with open("C:\\Users\\majip\\Downloads\\LLM REASEARCH\\data\\evol_instruct_dataset.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\\n")

print("JSON successfully appended.")
