import json, uuid, os

prompt = '''You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Lunar Base Regolith 3D Printing System.
Task: Invent a highly complex control scenario for this domain (e.g., lunar regolith microwave sintering temperature control and multi-axis print head positioning in vacuum).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O.'''

st_code = '''FUNCTION_BLOCK FB_LunarRegolith3DPrinter
TITLE = 'Lunar Base Regolith Microwave Sintering & 3D Printing Control System'
VERSION : '3.14'

VAR_INPUT
    bEnableSystem       : BOOL;   // Master enable for printing system
    bEmergencyStop      : BOOL;   // E-Stop (Active Low)
    rTargetTemperature  : REAL;   // Target sintering temperature (C)
    rCurrentTemperature : REAL;   // Feedback from IR pyrometer (C)
    rTargetPosX         : REAL;   // Target X position (mm)
    rTargetPosY         : REAL;   // Target Y position (mm)
    rTargetPosZ         : REAL;   // Target Z position (mm)
    rCurrentPosX        : REAL;   // Current X position (mm)
    rCurrentPosY        : REAL;   // Current Y position (mm)
    rCurrentPosZ        : REAL;   // Current Z position (mm)
    rMicrowavePowerMax  : REAL;   // Maximum microwave magnetron power (kW)
    rRegolithFeedRate   : REAL;   // Target regolith mass flow rate (g/s)
    bVacuumValid        : BOOL;   // True if chamber vacuum is within operational limits (<10^-4 Torr)
END_VAR

VAR_OUTPUT
    bSystemReady        : BOOL;   // System initialized and ready
    rMicrowavePowerCmd  : REAL;   // Commanded microwave power (0.0 to rMicrowavePowerMax)
    rAxisSpeedCmdX      : REAL;   // X-axis velocity command (mm/s)
    rAxisSpeedCmdY      : REAL;   // Y-axis velocity command (mm/s)
    rAxisSpeedCmdZ      : REAL;   // Z-axis velocity command (mm/s)
    rAugerSpeedCmd      : REAL;   // Regolith feed auger speed (RPM)
    bHeaterEnable       : BOOL;   // Magnetron enable signal
    bFaultActive        : BOOL;   // System fault flag
    iFaultCode          : INT;    // Specific fault code
END_VAR

VAR
    // PID Controller for Microwave Sintering Temperature
    stTempPID : PID_CONTROLLER;
    rTempKp   : REAL := 2.5;
    rTempKi   : REAL := 0.15;
    rTempKd   : REAL := 1.2;
    rTempIntegral : REAL := 0.0;
    rTempLastError: REAL := 0.0;
    
    // Position Control Parameters (P-control for simplicity in this block)
    rPosKpX   : REAL := 5.0;
    rPosKpY   : REAL := 5.0;
    rPosKpZ   : REAL := 2.5;
    
    // State Machine
    iState    : INT := 0; // 0=Init, 1=Idle, 2=Preheat, 3=Printing, 4=Cooldown, 99=Fault
    
    // Timers
    tonPreheatTimer : TON;
    tonCooldownTimer: TON;
    
    // Internal Flags
    bThermalStable  : BOOL;
    bPositionReached: BOOL;
    rTempError      : REAL;
    rPosXError      : REAL;
    rPosYError      : REAL;
    rPosZError      : REAL;
    rPosTolerance   : REAL := 0.1; // 0.1 mm tolerance
    
    dtLastScanTime  : TIME;
    rDeltaTime      : REAL := 0.01; // 10ms assumed scan time
END_VAR

// --- MAIN CONTROL LOGIC ---

// 1. Safety and Fault Monitoring
IF NOT bEmergencyStop THEN
    iState := 99;
    iFaultCode := 1001; // E-Stop activated
ELSIF NOT bVacuumValid AND (iState > 1 AND iState < 99) THEN
    iState := 99;
    iFaultCode := 1002; // Loss of vacuum during operation
ELSIF rCurrentTemperature > 1800.0 THEN
    iState := 99;
    iFaultCode := 1003; // Over-temperature fault
END_IF;

// 2. State Machine Processing
CASE iState OF
    0: // INIT
        bSystemReady := FALSE;
        bHeaterEnable := FALSE;
        rMicrowavePowerCmd := 0.0;
        rAxisSpeedCmdX := 0.0;
        rAxisSpeedCmdY := 0.0;
        rAxisSpeedCmdZ := 0.0;
        rAugerSpeedCmd := 0.0;
        bFaultActive := FALSE;
        iFaultCode := 0;
        
        IF bVacuumValid AND bEmergencyStop THEN
            iState := 1;
        END_IF;
        
    1: // IDLE
        bSystemReady := TRUE;
        bHeaterEnable := FALSE;
        rMicrowavePowerCmd := 0.0;
        rAugerSpeedCmd := 0.0;
        
        // Hold position
        rAxisSpeedCmdX := 0.0;
        rAxisSpeedCmdY := 0.0;
        rAxisSpeedCmdZ := 0.0;
        
        IF bEnableSystem THEN
            iState := 2; // Transition to preheat
            rTempIntegral := 0.0;
            rTempLastError := 0.0;
        END_IF;
        
    2: // PREHEAT
        bHeaterEnable := TRUE;
        
        // Execute PID for Temperature
        rTempError := rTargetTemperature - rCurrentTemperature;
        rTempIntegral := rTempIntegral + (rTempError * rDeltaTime);
        
        // Anti-windup
        IF rTempIntegral > 1000.0 THEN rTempIntegral := 1000.0; END_IF;
        IF rTempIntegral < -1000.0 THEN rTempIntegral := -1000.0; END_IF;
        
        rMicrowavePowerCmd := (rTempKp * rTempError) + (rTempKi * rTempIntegral) + (rTempKd * (rTempError - rTempLastError) / rDeltaTime);
        rTempLastError := rTempError;
        
        // Limit Output
        IF rMicrowavePowerCmd > rMicrowavePowerMax THEN
            rMicrowavePowerCmd := rMicrowavePowerMax;
        ELSIF rMicrowavePowerCmd < 0.0 THEN
            rMicrowavePowerCmd := 0.0;
        END_IF;
        
        // Check if thermal stability is reached
        IF ABS(rTempError) < 15.0 THEN
            tonPreheatTimer(IN:=TRUE, PT:=T#5s);
            IF tonPreheatTimer.Q THEN
                iState := 3; // Transition to Printing
                tonPreheatTimer(IN:=FALSE);
            END_IF;
        ELSE
            tonPreheatTimer(IN:=FALSE, PT:=T#5s);
        END_IF;
        
    3: // PRINTING
        bHeaterEnable := TRUE;
        
        // Continue Temperature PID
        rTempError := rTargetTemperature - rCurrentTemperature;
        rTempIntegral := rTempIntegral + (rTempError * rDeltaTime);
        rMicrowavePowerCmd := (rTempKp * rTempError) + (rTempKi * rTempIntegral) + (rTempKd * (rTempError - rTempLastError) / rDeltaTime);
        rTempLastError := rTempError;
        
        // Clamp output
        IF rMicrowavePowerCmd > rMicrowavePowerMax THEN rMicrowavePowerCmd := rMicrowavePowerMax; END_IF;
        IF rMicrowavePowerCmd < 0.0 THEN rMicrowavePowerCmd := 0.0; END_IF;
        
        // Position Control (Kinematics for Print Head)
        rPosXError := rTargetPosX - rCurrentPosX;
        rPosYError := rTargetPosY - rCurrentPosY;
        rPosZError := rTargetPosZ - rCurrentPosZ;
        
        rAxisSpeedCmdX := rPosKpX * rPosXError;
        rAxisSpeedCmdY := rPosKpY * rPosYError;
        rAxisSpeedCmdZ := rPosKpZ * rPosZError;
        
        // Speed limits
        IF rAxisSpeedCmdX > 100.0 THEN rAxisSpeedCmdX := 100.0; ELSIF rAxisSpeedCmdX < -100.0 THEN rAxisSpeedCmdX := -100.0; END_IF;
        IF rAxisSpeedCmdY > 100.0 THEN rAxisSpeedCmdY := 100.0; ELSIF rAxisSpeedCmdY < -100.0 THEN rAxisSpeedCmdY := -100.0; END_IF;
        IF rAxisSpeedCmdZ > 50.0  THEN rAxisSpeedCmdZ := 50.0;  ELSIF rAxisSpeedCmdZ < -50.0  THEN rAxisSpeedCmdZ := -50.0;  END_IF;
        
        // Regolith Extrusion Control based on movement speed
        // Feed rate is proportional to XY planar speed to ensure even bead width
        rAugerSpeedCmd := rRegolithFeedRate * ((rAxisSpeedCmdX * rAxisSpeedCmdX) + (rAxisSpeedCmdY * rAxisSpeedCmdY))**0.5 * 0.5;
        IF rAugerSpeedCmd > 500.0 THEN rAugerSpeedCmd := 500.0; END_IF;
        
        IF NOT bEnableSystem THEN
            iState := 4; // Stop printing, enter cooldown
        END_IF;
        
    4: // COOLDOWN
        bHeaterEnable := FALSE;
        rMicrowavePowerCmd := 0.0;
        rAugerSpeedCmd := 0.0;
        
        // Move to safe Z height (e.g. 100mm above current)
        rPosZError := (rCurrentPosZ + 100.0) - rCurrentPosZ;
        rAxisSpeedCmdZ := rPosKpZ * rPosZError;
        
        // Stop XY movement
        rAxisSpeedCmdX := 0.0;
        rAxisSpeedCmdY := 0.0;
        
        IF rCurrentTemperature < 200.0 THEN
            iState := 1; // Return to idle once cool
        END_IF;
        
    99: // FAULT STATE
        bSystemReady := FALSE;
        bFaultActive := TRUE;
        bHeaterEnable := FALSE;
        rMicrowavePowerCmd := 0.0;
        rAxisSpeedCmdX := 0.0;
        rAxisSpeedCmdY := 0.0;
        rAxisSpeedCmdZ := 0.0;
        rAugerSpeedCmd := 0.0;
        
        // Fault reset logic
        IF NOT bEnableSystem AND bEmergencyStop AND bVacuumValid THEN
            iState := 0; // Reset system when enable is toggled low and conditions are safe
        END_IF;
        
END_CASE;

END_FUNCTION_BLOCK'''

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": f"```iec-st\n{st_code}\n```"}]}
os.makedirs('data/swarm_raw', exist_ok=True)
filename = f'data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json'
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(record, f, indent=2)
print(f'Saved to {filename}')
