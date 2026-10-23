import json, uuid, os
os.makedirs("data/swarm_raw", exist_ok=True)
prompt = "You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.\nYour specific domain is: Offset Lithographic Printing Press.\nTask: Invent a highly complex control scenario for this domain (e.g., ink/water emulsion balance cascading, blanket cylinder squeeze pressure servos, and optical dot gain feedback tracking).\nWrite a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."
code = """```iec-st
FUNCTION_BLOCK FB_LithoPressMasterControl
TITLE = 'Offset Lithographic Printing Press Master Control'
// ---------------------------------------------------------------------------
// Description: Advanced control logic for Offset Lithographic Printing Press.
// Handles ink/water emulsion balance, blanket cylinder squeeze pressure servos,
// and optical dot gain feedback tracking.
// ---------------------------------------------------------------------------

VAR_INPUT
    bEnablePress           : BOOL;      // Press master enable
    rTargetSpeed_m_min     : REAL;      // Target web speed in m/min
    rTargetInkDensity      : REAL;      // Target ink density (0.0 - 2.5 D)
    rTargetWaterDampening  : REAL;      // Target water dampening level (0-100%)
    rTargetSqueezePressure : REAL;      // Target blanket cylinder squeeze (bar)
    rOpticalDotGainAct     : REAL;      // Actual dot gain feedback from optical scanner (%)
    
    // Physical IO Feedbacks
    rActSpeed_m_min        : REAL;      // Actual speed feedback
    rActInkDuctOpening     : REAL;      // Actual ink duct opening (0-100%)
    rActWaterPanRollerSpd  : REAL;      // Actual water pan roller speed (RPM)
    rActSqueezePressure    : REAL;      // Actual squeeze pressure (bar)
    bWebTensionOK          : BOOL;      // Web tension healthy
    bSafetyGuardsClosed    : BOOL;      // Safety guards status
END_VAR

VAR_OUTPUT
    bPressReady            : BOOL;      // Press ready to run
    bRunning               : BOOL;      // Press running
    rCmdInkDuctOpening     : REAL;      // Command for ink duct servo (0-100%)
    rCmdWaterPanRollerSpd  : REAL;      // Command for water pan roller speed (RPM)
    rCmdSqueezePressure    : REAL;      // Command for squeeze pressure proportional valve (bar)
    bAlarm                 : BOOL;      // General Alarm
    iAlarmCode             : INT;       // Specific Alarm code
END_VAR

VAR
    // Internal States
    iState                 : INT := 0;  // State machine step
    
    // PID Controllers
    fbInkWaterPID          : FB_PID;    // Ink-water emulsion PID
    fbSqueezePID           : FB_PID;    // Squeeze pressure PID
    fbDotGainPID           : FB_PID;    // Dot gain compensation PID
    
    // Timers
    tonRampUp              : TON;
    tonSqueezeStabilize    : TON;
    
    // Internal Variables
    rEmulsionRatio         : REAL;
    rDotGainError          : REAL;
    rCompensatedInkCmd     : REAL;
    rCompensatedWaterCmd   : REAL;
END_VAR

// Initialization and Safety Checks
bPressReady := bWebTensionOK AND bSafetyGuardsClosed;

IF NOT bEnablePress OR NOT bPressReady THEN
    iState := 0;
    bRunning := FALSE;
    rCmdInkDuctOpening := 0.0;
    rCmdWaterPanRollerSpd := 0.0;
    rCmdSqueezePressure := 0.0;
    bAlarm := NOT bPressReady;
    IF NOT bWebTensionOK THEN iAlarmCode := 101; END_IF;
    IF NOT bSafetyGuardsClosed THEN iAlarmCode := 102; END_IF;
    RETURN;
END_IF;

bAlarm := FALSE;
iAlarmCode := 0;

// State Machine for Press Startup and Running
CASE iState OF
    0: // Standby, Initialize
        rCmdInkDuctOpening := 0.0;
        rCmdWaterPanRollerSpd := 0.0;
        rCmdSqueezePressure := 0.0;
        tonRampUp(IN:=FALSE);
        IF bEnablePress AND bPressReady THEN
            iState := 10;
        END_IF;
        
    10: // Apply Squeeze Pressure
        rCmdSqueezePressure := rTargetSqueezePressure;
        // Simple P control for squeeze pressure
        rCmdSqueezePressure := rTargetSqueezePressure + (rTargetSqueezePressure - rActSqueezePressure) * 0.5;
        
        tonSqueezeStabilize(IN:=TRUE, PT:=T#3S);
        IF tonSqueezeStabilize.Q THEN
            tonSqueezeStabilize(IN:=FALSE);
            iState := 20;
        END_IF;
        
    20: // Pre-ink and pre-dampen
        rCmdWaterPanRollerSpd := rTargetWaterDampening * 2.0; // Base scaling
        rCmdInkDuctOpening := rTargetInkDensity * 40.0;       // Base scaling
        iState := 30;
        
    30: // Running and active compensation
        bRunning := TRUE;
        
        // Dot gain feedback tracking
        // Ideal dot gain depends on ink density; simple linear model assumed for demo
        rDotGainError := (rTargetInkDensity * 12.0) - rOpticalDotGainAct; 
        
        // Emulsion Balance Calculation (Cascading)
        // High web speed requires higher water speed, but we trim based on dot gain error
        rEmulsionRatio := rActSpeed_m_min / 100.0; 
        
        rCompensatedInkCmd := (rTargetInkDensity * 40.0) + (rDotGainError * 1.5) * rEmulsionRatio;
        rCompensatedWaterCmd := (rTargetWaterDampening * 2.0) * rEmulsionRatio - (rDotGainError * 0.5);
        
        // Limits
        IF rCompensatedInkCmd > 100.0 THEN rCompensatedInkCmd := 100.0; END_IF;
        IF rCompensatedInkCmd < 0.0 THEN rCompensatedInkCmd := 0.0; END_IF;
        
        IF rCompensatedWaterCmd > 500.0 THEN rCompensatedWaterCmd := 500.0; END_IF; // Max 500 RPM
        IF rCompensatedWaterCmd < 0.0 THEN rCompensatedWaterCmd := 0.0; END_IF;
        
        rCmdInkDuctOpening := rCompensatedInkCmd;
        rCmdWaterPanRollerSpd := rCompensatedWaterCmd;
        
        // Dynamic squeeze pressure adjustment based on speed
        IF rActSpeed_m_min > 500.0 THEN
            rCmdSqueezePressure := rTargetSqueezePressure * 1.1; // Increase squeeze at high speeds
        ELSE
            rCmdSqueezePressure := rTargetSqueezePressure;
        END_IF;
        
    ELSE
        iState := 0;
END_CASE;

END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
    json.dump(record, f)
