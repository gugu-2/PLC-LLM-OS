import json
import uuid
import os

code = """FUNCTION_BLOCK FB_JacquardLoomControl_Extreme
// ==============================================================================
// Domain: Jacquard Loom Weaving Control System
// Description: Electronic jacquard harness servo shedding, rapier weft 
// insertion synchronization, and warp beam let-off tension cascades.
// Complexity: High
// Deterministic Execution: Yes
// ==============================================================================
VAR_INPUT
    bStart_Weaving : BOOL; // Main start command from HMI
    bStop_Weaving : BOOL; // Main stop command from HMI
    bEmergency_Stop : BOOL; // Emergency stop from safety relay
    rTarget_Speed_PPM : REAL; // Target loom speed in Picks Per Minute
    
    // Shedding (Electronic Jacquard) Inputs
    wPattern_Data : ARRAY[0..1023] OF WORD; // Current pick pattern data buffer
    bPattern_Buffer_Ready : BOOL; // Indicates pattern data is loaded and verified
    bShed_Limit_Switch_Top : BOOL;
    bShed_Limit_Switch_Bottom : BOOL;
    
    // Rapier Insertion Inputs
    bRapier_Left_Home : BOOL; // Proximity sensor left rapier
    bRapier_Right_Home : BOOL; // Proximity sensor right rapier
    rWeft_Tension_Feedback : REAL; // Feedback from weft tension sensor (cN)
    bWeft_Break_Sensor : BOOL; // Optical weft break detector
    
    // Warp Let-off Inputs
    rWarp_Tension_Sensor_Left : REAL; // Left load cell (N)
    rWarp_Tension_Sensor_Right : REAL; // Right load cell (N)
    rBeam_Diameter_Sensor : REAL; // Laser sensor for beam diameter (mm)
END_VAR

VAR_OUTPUT
    bSystem_Ready : BOOL; // System initialized and ready
    bFault_Active : BOOL; // Global fault indicator
    iFault_Code : INT; // Error code for HMI
    rActual_Speed_PPM : REAL; // Actual calculated machine speed
    
    // Shedding Outputs
    bShed_Open_Cmd : BOOL; // Command to open the shed
    bShed_Close_Cmd : BOOL; // Command to close the shed
    wJacquard_Command_Word : WORD; // Data out to Jacquard controller
    
    // Rapier Outputs
    bFire_Left_Rapier_Servo : BOOL;
    bFire_Right_Rapier_Servo : BOOL;
    
    // Let-off Outputs
    rLetOff_Servo_Speed_Cmd : REAL; // Speed command to warp beam servo drive (RPM)
    bLetOff_Brake_Release : BOOL; // Release mechanical brake
END_VAR

VAR
    // Internal State Machine
    iMain_State : INT := 0; // 0:Init, 1:Ready, 2:StartDelay, 3:Running, 4:Stopping, 5:Fault
    
    // Timers
    tShedding_Timeout : TON;
    tRapier_Timeout : TON;
    tStop_Ramp_Timer : TON;
    
    // Let-off PID Controller Variables
    rAvg_Warp_Tension : REAL;
    rTension_Error : REAL;
    rTension_Setpoint : REAL := 1200.0; // N
    rKp_LetOff : REAL := 0.75;
    rKi_LetOff : REAL := 0.25;
    rKd_LetOff : REAL := 0.05;
    rLetOff_Integral : REAL := 0.0;
    rLetOff_Derivative : REAL := 0.0;
    rLetOff_Prev_Error : REAL := 0.0;
    
    // Master Virtual Axis and Cycle Tracking
    rMaster_Angle_Deg : REAL := 0.0; // 0.0 to 359.9 degrees
    bPick_Complete : BOOL;
    rScan_Time_ms : REAL := 1.0; // Assuming 1ms task cycle time
END_VAR

// ==============================================================================
// 1. MAIN STATE MACHINE
// ==============================================================================
CASE iMain_State OF
    0: // Initialization
        bSystem_Ready := FALSE;
        bFault_Active := FALSE;
        iFault_Code := 0;
        bLetOff_Brake_Release := FALSE;
        rMaster_Angle_Deg := 0.0;
        // Verify sensors
        IF bRapier_Left_Home AND bRapier_Right_Home THEN
            iMain_State := 1;
        END_IF
        
    1: // Ready
        bSystem_Ready := TRUE;
        IF bStart_Weaving AND NOT bEmergency_Stop THEN
            iMain_State := 2; // Move to start sequence
            bSystem_Ready := FALSE;
        END_IF
        
    2: // Start Delay & Pre-tension
        bLetOff_Brake_Release := TRUE;
        // Wait for pattern buffer
        IF bPattern_Buffer_Ready THEN
            iMain_State := 3;
        END_IF
        
    3: // Running (Weaving Cycle)
        IF bStop_Weaving THEN
            iMain_State := 4;
        END_IF
        IF bEmergency_Stop OR bWeft_Break_Sensor THEN
            iMain_State := 5;
            iFault_Code := 101; // E-Stop or Weft Break
        END_IF
        
        // --- 1.1 Master Virtual Axis ---
        // Calculate degrees per scan based on Target PPM (1 pick = 360 deg)
        // (PPM / 60) = Picks per second. * 360 = Degrees per second.
        // * (rScan_Time_ms / 1000) = Degrees per scan
        rMaster_Angle_Deg := rMaster_Angle_Deg + (rTarget_Speed_PPM / 60.0 * 360.0 * (rScan_Time_ms / 1000.0));
        
        IF rMaster_Angle_Deg >= 360.0 THEN
            rMaster_Angle_Deg := rMaster_Angle_Deg - 360.0;
            bPick_Complete := TRUE;
        ELSE
            bPick_Complete := FALSE;
        END_IF
        
        // --- 1.2 Electronic Jacquard Shedding Synchronization ---
        // Shed opens at 300 degrees and stays open until 60 degrees of next cycle
        IF (rMaster_Angle_Deg >= 300.0) OR (rMaster_Angle_Deg < 60.0) THEN
            bShed_Open_Cmd := TRUE;
            bShed_Close_Cmd := FALSE;
            wJacquard_Command_Word := wPattern_Data[0]; // Output pattern
        ELSE
            bShed_Open_Cmd := FALSE;
            bShed_Close_Cmd := TRUE;
            wJacquard_Command_Word := 16#0000;
        END_IF
        
        // --- 1.3 Rapier Weft Insertion Synchronization ---
        // Fire left rapier (giver) at 70 degrees
        IF rMaster_Angle_Deg >= 70.0 AND rMaster_Angle_Deg <= 175.0 THEN
            bFire_Left_Rapier_Servo := TRUE;
        ELSE
            bFire_Left_Rapier_Servo := FALSE;
        END_IF
        
        // Fire right rapier (taker) at 170 degrees for handover
        IF rMaster_Angle_Deg >= 170.0 AND rMaster_Angle_Deg <= 280.0 THEN
            bFire_Right_Rapier_Servo := TRUE;
        ELSE
            bFire_Right_Rapier_Servo := FALSE;
        END_IF
        
        // Fault check: Rapier collision prevention
        IF (bFire_Left_Rapier_Servo AND bFire_Right_Rapier_Servo) AND rMaster_Angle_Deg > 185.0 THEN
            iMain_State := 5; // Fault
            iFault_Code := 201; // Rapier synchronization fault
        END_IF
        
        // --- 1.4 Warp Beam Let-off Tension Cascade (PID) ---
        rAvg_Warp_Tension := (rWarp_Tension_Sensor_Left + rWarp_Tension_Sensor_Right) / 2.0;
        rTension_Error := rTension_Setpoint - rAvg_Warp_Tension;
        
        // Integral with Anti-windup
        IF (rLetOff_Integral < 2000.0) AND (rLetOff_Integral > -2000.0) THEN
            rLetOff_Integral := rLetOff_Integral + (rTension_Error * (rScan_Time_ms / 1000.0));
        END_IF
        
        // Derivative
        rLetOff_Derivative := (rTension_Error - rLetOff_Prev_Error) / (rScan_Time_ms / 1000.0);
        rLetOff_Prev_Error := rTension_Error;
        
        // PID Output Calculation
        rLetOff_Servo_Speed_Cmd := (rTension_Error * rKp_LetOff) + (rLetOff_Integral * rKi_LetOff) + (rLetOff_Derivative * rKd_LetOff);
        
        // Feedforward & Diameter Compensation
        // Smaller beam diameter requires higher RPM to maintain linear speed
        IF rBeam_Diameter_Sensor > 50.0 THEN
            rLetOff_Servo_Speed_Cmd := rLetOff_Servo_Speed_Cmd * (800.0 / rBeam_Diameter_Sensor);
        END_IF
        
        rActual_Speed_PPM := rTarget_Speed_PPM; // In a real system, calculate from encoder
        
    4: // Stopping Ramp
        rActual_Speed_PPM := 0.0;
        bFire_Left_Rapier_Servo := FALSE;
        bFire_Right_Rapier_Servo := FALSE;
        bLetOff_Brake_Release := FALSE;
        rLetOff_Servo_Speed_Cmd := 0.0;
        iMain_State := 1;
        
    5: // Fault State
        bFault_Active := TRUE;
        rActual_Speed_PPM := 0.0;
        bFire_Left_Rapier_Servo := FALSE;
        bFire_Right_Rapier_Servo := FALSE;
        bShed_Open_Cmd := FALSE;
        bShed_Close_Cmd := FALSE;
        rLetOff_Servo_Speed_Cmd := 0.0;
        bLetOff_Brake_Release := FALSE;
        
        // Fault Reset Logic
        IF NOT bEmergency_Stop AND NOT bWeft_Break_Sensor THEN
            IF bStart_Weaving THEN // Use start button to reset faults
                iMain_State := 0;
            END_IF
        END_IF
END_CASE
END_FUNCTION_BLOCK
"""

prompt = "You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.\\nYour specific domain is: Jacquard Loom.\\nTask: Invent a highly complex control scenario for this domain (e.g., electronic jacquard harness servo shedding, rapier weft insertion synchronization, and warp beam let-off tension cascades).\\nWrite a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O.\\n\\nCRITICAL RULES:\\n1. You MUST output the code enclosed in a ```iec-st markdown code fence. DO NOT APOLOGIZE. DO NOT EXPLAIN.\\n2. The code must be >= 1500 chars, with FUNCTION_BLOCK and VAR_INPUT/VAR_OUTPUT.\\n3. You MUST save your JSON payload to a uniquely named file in the swarm directory using python."

content = f"```iec-st\n{code}\n```"

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": content}
    ]
}

os.makedirs(r"c:\Users\majip\Downloads\LLM REASEARCH\data\swarm_raw", exist_ok=True)
filename = f"c:\\Users\\majip\\Downloads\\LLM REASEARCH\\data\\swarm_raw\\agent_{uuid.uuid4().hex[:8]}.json"

with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)

print(f"Success: {filename}")
