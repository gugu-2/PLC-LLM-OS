import json, uuid, os

os.makedirs("data/swarm_raw", exist_ok=True)
os.makedirs("data", exist_ok=True)

prompt = "You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.\nYour specific domain is: High-Speed Automated People Mover (APM).\nTask: Invent a highly complex control scenario for this domain (e.g., guideway switching interlocks, station platform screen door synchronization, and CBTC communication handoffs).\nWrite a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."

code = """```iec-st
FUNCTION_BLOCK FB_APM_Guideway_Control
VAR_INPUT
    bStart_Sequence : BOOL; // Start train sequence
    bTrain_At_Station : BOOL; // Train presence detected
    bDoors_Closed_Train : BOOL; // Train doors fully closed
    bDoors_Closed_Platform : BOOL; // Platform screen doors closed
    rTrain_Speed : REAL; // Current train speed in m/s
    bGuideway_Switch_Lock : BOOL; // Lock signal from guideway switch
    bCBTC_Comm_OK : BOOL; // Communication status with CBTC
    rDistance_To_Next_Zone : REAL; // Distance to the next control zone
    bEmergency_Stop : BOOL; // Emergency stop request
    bPower_Rail_Active : BOOL; // Traction power status
END_VAR

VAR_OUTPUT
    bAllow_Departure : BOOL; // Signal to allow train departure
    bOpen_Platform_Doors : BOOL; // Command to open platform doors
    bOpen_Train_Doors : BOOL; // Command to open train doors
    bEngage_Traction : BOOL; // Command to engage traction motors
    rTarget_Speed : REAL; // Target speed command to CBTC
    bTrigger_E_Brake : BOOL; // Command to engage emergency brake
    bSwitch_Req : BOOL; // Request guideway switch operation
    iSystem_State : INT; // Current state of the APM controller
    bAlarm_Comm_Loss : BOOL; // Alarm for CBTC communication loss
    bAlarm_Door_Sync : BOOL; // Alarm for door synchronization failure
END_VAR

VAR
    Tmr_Door_Sync : TON;
    Tmr_Comm_Loss : TON;
    Tmr_Departure_Delay : TON;
    bState_Init : BOOL := TRUE;
    iState : INT := 0; 
    // 0: Init, 1: Arriving, 2: Docked, 3: Doors Open, 4: Boarding Complete, 5: Departing, 99: Fault
    bDoor_Opening_Seq : BOOL;
    bDeparture_Seq : BOOL;
END_VAR

// -----------------------------------------------------------------------------
// TIMER LOGIC
// -----------------------------------------------------------------------------
Tmr_Door_Sync(IN := bDoor_Opening_Seq AND NOT (bDoors_Closed_Train AND bDoors_Closed_Platform), PT := T#5S);
Tmr_Comm_Loss(IN := NOT bCBTC_Comm_OK, PT := T#1S);
Tmr_Departure_Delay(IN := bDeparture_Seq, PT := T#3S);

// -----------------------------------------------------------------------------
// EMERGENCY AND FAULT MONITORING
// -----------------------------------------------------------------------------
IF bEmergency_Stop THEN
    bTrigger_E_Brake := TRUE;
    bAllow_Departure := FALSE;
    bEngage_Traction := FALSE;
    rTarget_Speed := 0.0;
    iState := 99;
ELSIF Tmr_Comm_Loss.Q THEN
    bAlarm_Comm_Loss := TRUE;
    bTrigger_E_Brake := TRUE;
    bAllow_Departure := FALSE;
    rTarget_Speed := 0.0;
    iState := 99;
END_IF;

// -----------------------------------------------------------------------------
// MAIN STATE MACHINE
// -----------------------------------------------------------------------------
CASE iState OF
    0: // Initialization
        bAllow_Departure := FALSE;
        bOpen_Platform_Doors := FALSE;
        bOpen_Train_Doors := FALSE;
        bEngage_Traction := FALSE;
        rTarget_Speed := 0.0;
        IF bCBTC_Comm_OK AND bPower_Rail_Active AND NOT bEmergency_Stop THEN
            iState := 1;
        END_IF;

    1: // Arriving
        IF bTrain_At_Station AND (rTrain_Speed < 0.1) THEN
            rTarget_Speed := 0.0;
            bEngage_Traction := FALSE;
            iState := 2; // Transition to Docked
        ELSE
            rTarget_Speed := 15.0; // Approach speed
            bEngage_Traction := TRUE;
        END_IF;

    2: // Docked
        IF bTrain_At_Station AND (rTrain_Speed = 0.0) THEN
            bDoor_Opening_Seq := TRUE;
            bOpen_Platform_Doors := TRUE;
            bOpen_Train_Doors := TRUE;
            IF NOT bDoors_Closed_Train AND NOT bDoors_Closed_Platform THEN
                bDoor_Opening_Seq := FALSE;
                iState := 3;
            ELSIF Tmr_Door_Sync.Q THEN
                bAlarm_Door_Sync := TRUE;
                iState := 99; // Fault due to door failure
            END_IF;
        END_IF;

    3: // Doors Open / Boarding
        IF bStart_Sequence THEN
            bOpen_Platform_Doors := FALSE;
            bOpen_Train_Doors := FALSE;
            IF bDoors_Closed_Train AND bDoors_Closed_Platform THEN
                iState := 4;
            END_IF;
        END_IF;

    4: // Boarding Complete, Awaiting Guideway
        IF bGuideway_Switch_Lock AND (rDistance_To_Next_Zone > 500.0) THEN
            bDeparture_Seq := TRUE;
            IF Tmr_Departure_Delay.Q THEN
                bDeparture_Seq := FALSE;
                bAllow_Departure := TRUE;
                iState := 5;
            END_IF;
        ELSE
            bSwitch_Req := TRUE; // Request switch ahead
        END_IF;
        
    5: // Departing
        bAllow_Departure := TRUE;
        bEngage_Traction := TRUE;
        rTarget_Speed := 25.0; // Nominal cruising speed
        
        IF NOT bTrain_At_Station THEN
            // Train has left the station
            bAllow_Departure := FALSE;
            iState := 1; // Reset to arriving for next station/zone block
        END_IF;

    99: // Fault State
        bEngage_Traction := FALSE;
        bAllow_Departure := FALSE;
        rTarget_Speed := 0.0;
        bOpen_Platform_Doors := FALSE;
        bOpen_Train_Doors := FALSE;
        
        // Requires manual reset or remote command to clear
        IF bCBTC_Comm_OK AND NOT bEmergency_Stop AND NOT bAlarm_Door_Sync THEN
            iState := 0; // Attempt auto-recovery to init
            bTrigger_E_Brake := FALSE;
            bAlarm_Comm_Loss := FALSE;
        END_IF;
        
END_CASE;

// State Output
iSystem_State := iState;

END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}

with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
    json.dump(record, f)

with open("data/synthetic_generation_v3_enterprise.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\\n")
