import json, uuid, os

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = "Generate a highly complex control scenario for a Cardboard Folder-Gluer Machine (e.g., trombone section shingling speed profiling, optical glue line detection loops, and squaring kicker tracking)."

st_code = """FUNCTION_BLOCK FB_FolderGluer_AdvancedControl
VAR_INPUT
    bEnable                 : BOOL;                 // Enable overall machine control
    bEmergencyStop          : BOOL;                 // E-Stop status (Active low)
    rMainLineSpeed          : REAL;                 // Main conveyor line speed in m/min
    rTargetShinglePitch     : REAL;                 // Target pitch for shingling in mm
    iOpticalSensorArray     : ARRAY[0..15] OF INT;  // Glue line detection optical sensor array (0-4095)
    bSquaringKickerTrig     : BOOL;                 // Trigger for squaring kicker
    rCartonLength           : REAL;                 // Length of carton in mm
    rCartonWidth            : REAL;                 // Width of carton in mm
    bResetFault             : BOOL;                 // Reset fault command
END_VAR

VAR_OUTPUT
    rTromboneSpeedCmd       : REAL;                 // Speed command for Trombone section (m/min)
    bGlueGunTrigger         : BOOL;                 // Trigger to activate glue gun
    bSquaringKickerActuate  : BOOL;                 // Actuate the squaring kicker cylinder
    bMachineFault           : BOOL;                 // General machine fault indicator
    iFaultCode              : INT;                  // Specific fault code
    rCurrentGlueQuality     : REAL;                 // Computed glue line quality percentage
    bWarningQuality         : BOOL;                 // Warning if glue quality is suboptimal
END_VAR

VAR
    rActualTromboneSpeed    : REAL;
    rCalculatedRatio        : REAL;
    i                       : INT;
    iSensorSum              : DINT;
    rAverageSensorVal       : REAL;
    rGlueThreshold          : REAL := 2500.0;
    rKickerDelayTime        : REAL;
    fbKickerTimer           : TON;
    fbGlueDefectTimer       : TON;
    eState                  : INT := 0; // 0=IDLE, 1=RUN, 2=FAULT
    bGlueDefect             : BOOL;
    rPreviousMainSpeed      : REAL;
    rAccelerationLimit      : REAL := 5.0; // max acceleration m/s^2
END_VAR

// --- E-Stop & Fault Handling ---
IF NOT bEmergencyStop THEN
    eState := 2;
    iFaultCode := 999;
    bMachineFault := TRUE;
    rTromboneSpeedCmd := 0.0;
    bGlueGunTrigger := FALSE;
    bSquaringKickerActuate := FALSE;
    RETURN;
END_IF

IF bResetFault AND eState = 2 THEN
    eState := 0;
    bMachineFault := FALSE;
    iFaultCode := 0;
END_IF

// --- State Machine ---
CASE eState OF
    0: // IDLE
        rTromboneSpeedCmd := 0.0;
        bGlueGunTrigger := FALSE;
        bSquaringKickerActuate := FALSE;
        IF bEnable AND NOT bMachineFault THEN
            eState := 1;
        END_IF
        
    1: // RUN
        IF NOT bEnable THEN
            eState := 0;
        END_IF
        
        // --- Trombone Section Shingling Speed Profiling ---
        // Calculate required ratio for shingling based on carton length and target pitch
        IF rCartonLength > 0.0 AND rTargetShinglePitch > 0.0 THEN
            rCalculatedRatio := rTargetShinglePitch / rCartonLength;
        ELSE
            rCalculatedRatio := 1.0; // 1:1 default to avoid jam
        END_IF
        
        // Command Trombone speed with acceleration limiting
        rActualTromboneSpeed := rMainLineSpeed * rCalculatedRatio;
        
        // Simple rate limiter implementation (pseudo-code logic)
        IF (rActualTromboneSpeed - rTromboneSpeedCmd) > rAccelerationLimit THEN
            rTromboneSpeedCmd := rTromboneSpeedCmd + rAccelerationLimit;
        ELSIF (rTromboneSpeedCmd - rActualTromboneSpeed) > rAccelerationLimit THEN
            rTromboneSpeedCmd := rTromboneSpeedCmd - rAccelerationLimit;
        ELSE
            rTromboneSpeedCmd := rActualTromboneSpeed;
        END_IF

        // --- Optical Glue Line Detection Loops ---
        // Sum optical sensor array to determine glue application presence and quality
        iSensorSum := 0;
        FOR i := 0 TO 15 DO
            iSensorSum := iSensorSum + iOpticalSensorArray[i];
        END_FOR
        
        rAverageSensorVal := DINT_TO_REAL(iSensorSum) / 16.0;
        
        // Normalize quality to percentage (assuming 4095 is max reflection/glue amount)
        rCurrentGlueQuality := (rAverageSensorVal / 4095.0) * 100.0;
        
        IF rAverageSensorVal < rGlueThreshold THEN
            bGlueDefect := TRUE;
        ELSE
            bGlueDefect := FALSE;
        END_IF
        
        // Timer to filter spurious glue defects
        fbGlueDefectTimer(IN := bGlueDefect, PT := T#50MS);
        IF fbGlueDefectTimer.Q THEN
            bWarningQuality := TRUE;
        ELSE
            bWarningQuality := FALSE;
        END_IF
        
        // Simulate glue gun triggering linked to machine speed
        bGlueGunTrigger := (rMainLineSpeed > 10.0) AND NOT bGlueDefect;
        
        // --- Squaring Kicker Tracking ---
        // Delay based on line speed and distance to kicker (assuming 500mm distance)
        IF rMainLineSpeed > 0.0 THEN
            rKickerDelayTime := 500.0 / ((rMainLineSpeed * 1000.0) / 60.0); // seconds
        ELSE
            rKickerDelayTime := 0.0;
        END_IF
        
        fbKickerTimer(IN := bSquaringKickerTrig, PT := REAL_TO_TIME(rKickerDelayTime * 1000.0));
        
        IF fbKickerTimer.Q THEN
            bSquaringKickerActuate := TRUE;
        ELSE
            bSquaringKickerActuate := FALSE;
        END_IF
        
    2: // FAULT
        ;
END_CASE
END_FUNCTION_BLOCK"""

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": "```iec-st\n" + st_code + "\n```"}
    ]
}

file_name = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(file_name, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)

print(file_name)
