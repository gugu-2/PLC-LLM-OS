import json
import uuid
import os

st_code = """FUNCTION_BLOCK FB_HighSpeedBlisterPackaging
VAR_INPUT
    bEnable          : BOOL;  // Main machine enable flag
    bReset           : BOOL;  // Fault reset pushbutton
    diEncoderTicks   : DINT;  // Master encoder position for camming
    bVisionReject    : BOOL;  // Vision system reject trigger (Camera NG)
    bSealTempReady   : BOOL;  // Ultrasonic sealing temperature within limits
    bSealPressOK     : BOOL;  // Ultrasonic sealing pneumatic pressure OK
    bIndexComplete   : BOOL;  // Servo index completed signal from drive
END_VAR
VAR_OUTPUT
    bServoStart      : BOOL;  // Trigger command to servo index drive
    bUltrasonicSeal  : BOOL;  // Trigger for ultrasonic weld generator
    bRejectPneumatic : BOOL;  // Trigger reject blow-off solenoid valve
    iMachineState    : INT;   // Current state machine step for HMI
    wErrorCode       : WORD;  // Active error code (0 = No Error)
END_VAR
VAR
    // Shift Register for Reject Tracking (64 mechanical stations)
    abRejectShiftReg : ARRAY[0..63] OF BOOL;
    iRejectStationIdx: INT := 12; // Distance from vision camera to reject station in index steps
    
    // Timers for process operations
    fbSealTimer      : TON;
    fbRejectTimer    : TON;
    
    // Edge Detectors
    fbVisionTrig     : R_TRIG;
    fbIndexTrig      : R_TRIG;
    fbEnableTrig     : R_TRIG;
    
    // State Machine Constants
    STATE_INIT       : INT := 0;
    STATE_READY      : INT := 10;
    STATE_INDEXING   : INT := 20;
    STATE_SEALING    : INT := 30;
    STATE_FAULT      : INT := 99;
    
    i               : INT;
END_VAR

// Evaluate input triggers
fbVisionTrig(CLK := bVisionReject);
fbIndexTrig(CLK := bIndexComplete);
fbEnableTrig(CLK := bEnable);

// Main Control State Machine
CASE iMachineState OF
    
    // Initialization State - Reset all variables and outputs
    STATE_INIT:
        bServoStart := FALSE;
        bUltrasonicSeal := FALSE;
        bRejectPneumatic := FALSE;
        wErrorCode := 16#0000;
        
        // Clear out the shift register entirely
        FOR i := 0 TO 63 DO
            abRejectShiftReg[i] := FALSE;
        END_FOR;
        
        // Wait for system enable
        IF fbEnableTrig.Q THEN
            iMachineState := STATE_READY;
        END_IF;
        
    // Ready State - Verify prerequisites before indexing
    STATE_READY:
        IF NOT bEnable THEN
            iMachineState := STATE_INIT;
        ELSIF bSealTempReady AND bSealPressOK THEN
            // Parameters are good, initiate mechanical index
            bServoStart := TRUE;
            iMachineState := STATE_INDEXING;
        ELSE
            // Trigger fault if parameters deviate during operation
            wErrorCode := 16#0001; // Error: Seal parameters not ready
            iMachineState := STATE_FAULT;
        END_IF;
        
    // Indexing State - Wait for servo to complete move
    STATE_INDEXING:
        bServoStart := FALSE; // Remove start command, wait for complete flag
        
        IF fbIndexTrig.Q THEN
            // Index complete, shift the reject tracking register by one position
            // Shift from end to beginning to avoid overwriting
            FOR i := 63 TO 1 BY -1 DO
                abRejectShiftReg[i] := abRejectShiftReg[i-1];
            END_FOR;
            abRejectShiftReg[0] := FALSE; // Clear the entry position for the new blister
            
            // Proceed to processing phase (Sealing and Vision Inspection)
            iMachineState := STATE_SEALING;
        END_IF;
        
    // Sealing and Inspection State - Perform stationary operations
    STATE_SEALING:
        // 1. Trigger ultrasonic sealing profile
        bUltrasonicSeal := TRUE;
        fbSealTimer(IN := bUltrasonicSeal, PT := T#200MS); // 200ms seal dwell time
        
        // 2. Record vision system result during this dwell time
        IF fbVisionTrig.Q THEN
            // Mark current blister at station 0 as rejected
            abRejectShiftReg[0] := TRUE; 
        END_IF;
        
        // 3. Handle Rejection at the physical reject station
        IF abRejectShiftReg[iRejectStationIdx] THEN
            bRejectPneumatic := TRUE; // Activate blow-off solenoid
        ELSE
            bRejectPneumatic := FALSE;
        END_IF;
        
        // Pulse the reject solenoid for 50ms to save compressed air
        fbRejectTimer(IN := bRejectPneumatic, PT := T#50MS);
        IF fbRejectTimer.Q THEN
            bRejectPneumatic := FALSE;
        END_IF;
        
        // 4. Check for process completion
        IF fbSealTimer.Q THEN
            // Sealing complete
            bUltrasonicSeal := FALSE;
            fbSealTimer(IN := FALSE); // Reset timer
            
            // Return to Ready state for the next index cycle
            iMachineState := STATE_READY;
        END_IF;
        
    // Fault Handling State - Safely stop the machine and await reset
    STATE_FAULT:
        bServoStart := FALSE;
        bUltrasonicSeal := FALSE;
        bRejectPneumatic := FALSE;
        
        IF bReset THEN
            wErrorCode := 16#0000;
            iMachineState := STATE_INIT;
        END_IF;
        
END_CASE;
END_FUNCTION_BLOCK"""

prompt = "Generate a highly complex control scenario for High-Speed Pharmaceutical Packaging in IEC 61131-3 Structured Text. It must include blister pack ultrasonic sealing, high-speed machine vision rejection tracking via shift registers, and servo blister indexing."
assistant_msg = f"```iec-st\n{st_code}\n```"

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": assistant_msg}
    ]
}

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f)
print(f"Data saved to {filename}")
