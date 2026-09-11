import os, json, uuid

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Commercial Tunnel Boring Machine (TBM).
Task: Invent a highly complex control scenario for this domain (e.g., Earth Pressure Balance (EPB) thrust cylinder hydraulic synchronization, cutterhead torque monitoring, and muck screw conveyor speed).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."""

iec_st = """FUNCTION_BLOCK FB_TBM_EPB_Control
TITLE = 'Tunnel Boring Machine - Earth Pressure Balance Control'
// -----------------------------------------------------------------------------
// DESCRIPTION:
// Highly complex control scenario for Commercial Tunnel Boring Machine (TBM)
// incorporating Earth Pressure Balance (EPB) thrust cylinder hydraulic 
// synchronization, cutterhead torque monitoring, and muck screw conveyor speed.
// -----------------------------------------------------------------------------
VAR_INPUT
    bEnable                 : BOOL; // Master enable for EPB Control
    rTargetEarthPressure    : REAL; // Target earth pressure [bar]
    rActualEarthPressure    : REAL; // Actual earth pressure at bulkhead [bar]
    rThrustCyl1_Pos         : REAL; // Thrust Cylinder 1 Position [mm]
    rThrustCyl2_Pos         : REAL; // Thrust Cylinder 2 Position [mm]
    rThrustCyl3_Pos         : REAL; // Thrust Cylinder 3 Position [mm]
    rThrustCyl4_Pos         : REAL; // Thrust Cylinder 4 Position [mm]
    rCutterheadSpeed        : REAL; // Actual Cutterhead Speed [RPM]
    rCutterheadTorque       : REAL; // Actual Cutterhead Torque [kNm]
    rMaxAllowableTorque     : REAL; // Maximum allowable torque before interlock [kNm]
    rAdvanceRateSetpt       : REAL; // Desired advance rate [mm/min]
END_VAR

VAR_OUTPUT
    bSystemReady            : BOOL; // System is initialized and ready
    rThrustCyl1_Cmd         : REAL; // Hydraulic valve command Cyl 1 [%]
    rThrustCyl2_Cmd         : REAL; // Hydraulic valve command Cyl 2 [%]
    rThrustCyl3_Cmd         : REAL; // Hydraulic valve command Cyl 3 [%]
    rThrustCyl4_Cmd         : REAL; // Hydraulic valve command Cyl 4 [%]
    rMuckScrewSpeed_Cmd     : REAL; // Muck screw conveyor speed command [RPM]
    bTorqueAlarm            : BOOL; // Cutterhead torque high alarm
    bPressureAlarm          : BOOL; // Earth pressure deviation alarm
    bSyncError              : BOOL; // Thrust cylinder synchronization error
END_VAR

VAR
    // Internal States
    rAveragePos             : REAL; // Average position of all cylinders
    rPosError1              : REAL; // Position error for Cyl 1
    rPosError2              : REAL; // Position error for Cyl 2
    rPosError3              : REAL; // Position error for Cyl 3
    rPosError4              : REAL; // Position error for Cyl 4
    
    // PID Controllers for Sync
    rKp_Sync                : REAL := 2.5;
    rKi_Sync                : REAL := 0.1;
    rIntegral1              : REAL := 0.0;
    rIntegral2              : REAL := 0.0;
    rIntegral3              : REAL := 0.0;
    rIntegral4              : REAL := 0.0;
    
    // EPB Control Variables
    rPressureError          : REAL;
    rKp_EPB                 : REAL := 5.0;
    rBaseScrewSpeed         : REAL := 10.0; // Nominal RPM
    rScrewSpeedAdj          : REAL;
    
    // Timers
    TMR_TorqueAlarm         : TON;
    TMR_SyncAlarm           : TON;
    
    // Limits
    rMaxSyncDev             : REAL := 15.0; // Max allowed deviation [mm]
    rMaxPressureDev         : REAL := 0.5;  // Max allowed pressure deviation [bar]
END_VAR

// =============================================================================
// ALGORITHM START
// =============================================================================

// Check Master Enable
IF NOT bEnable THEN
    rThrustCyl1_Cmd := 0.0;
    rThrustCyl2_Cmd := 0.0;
    rThrustCyl3_Cmd := 0.0;
    rThrustCyl4_Cmd := 0.0;
    rMuckScrewSpeed_Cmd := 0.0;
    bSystemReady := FALSE;
    bTorqueAlarm := FALSE;
    bPressureAlarm := FALSE;
    bSyncError := FALSE;
    RETURN;
END_IF;

bSystemReady := TRUE;

// -----------------------------------------------------------------------------
// 1. Cutterhead Torque Monitoring
// -----------------------------------------------------------------------------
TMR_TorqueAlarm(IN := (rCutterheadTorque > rMaxAllowableTorque), PT := T#3S);
IF TMR_TorqueAlarm.Q THEN
    bTorqueAlarm := TRUE;
ELSE
    bTorqueAlarm := FALSE;
END_IF;

// If torque is too high, reduce advance rate dynamically
VAR
    rDynamicAdvanceRate : REAL;
END_VAR

IF bTorqueAlarm THEN
    rDynamicAdvanceRate := rAdvanceRateSetpt * 0.5; // Reduce advance rate by 50%
ELSE
    rDynamicAdvanceRate := rAdvanceRateSetpt;
END_IF;

// -----------------------------------------------------------------------------
// 2. Thrust Cylinder Hydraulic Synchronization
// -----------------------------------------------------------------------------
// Calculate average position
rAveragePos := (rThrustCyl1_Pos + rThrustCyl2_Pos + rThrustCyl3_Pos + rThrustCyl4_Pos) / 4.0;

// Calculate position errors relative to average
rPosError1 := rAveragePos - rThrustCyl1_Pos;
rPosError2 := rAveragePos - rThrustCyl2_Pos;
rPosError3 := rAveragePos - rThrustCyl3_Pos;
rPosError4 := rAveragePos - rThrustCyl4_Pos;

// Check for synchronization error
TMR_SyncAlarm(
    IN := (ABS(rPosError1) > rMaxSyncDev) OR 
          (ABS(rPosError2) > rMaxSyncDev) OR 
          (ABS(rPosError3) > rMaxSyncDev) OR 
          (ABS(rPosError4) > rMaxSyncDev), 
    PT := T#2S
);
bSyncError := TMR_SyncAlarm.Q;

// Calculate PI control for each cylinder
// Prevent windup when sync error is active
IF NOT bSyncError THEN
    rIntegral1 := rIntegral1 + (rPosError1 * rKi_Sync);
    rIntegral2 := rIntegral2 + (rPosError2 * rKi_Sync);
    rIntegral3 := rIntegral3 + (rPosError3 * rKi_Sync);
    rIntegral4 := rIntegral4 + (rPosError4 * rKi_Sync);
END_IF;

// Base command derived from dynamic advance rate (scaled to percentage)
VAR
    rBaseThrustCmd : REAL;
END_VAR
rBaseThrustCmd := rDynamicAdvanceRate * 2.0; // simplified scaling factor

rThrustCyl1_Cmd := rBaseThrustCmd + (rPosError1 * rKp_Sync) + rIntegral1;
rThrustCyl2_Cmd := rBaseThrustCmd + (rPosError2 * rKp_Sync) + rIntegral2;
rThrustCyl3_Cmd := rBaseThrustCmd + (rPosError3 * rKp_Sync) + rIntegral3;
rThrustCyl4_Cmd := rBaseThrustCmd + (rPosError4 * rKp_Sync) + rIntegral4;

// Clamp outputs to 0.0 - 100.0%
rThrustCyl1_Cmd := LIMIT(0.0, rThrustCyl1_Cmd, 100.0);
rThrustCyl2_Cmd := LIMIT(0.0, rThrustCyl2_Cmd, 100.0);
rThrustCyl3_Cmd := LIMIT(0.0, rThrustCyl3_Cmd, 100.0);
rThrustCyl4_Cmd := LIMIT(0.0, rThrustCyl4_Cmd, 100.0);

// -----------------------------------------------------------------------------
// 3. Earth Pressure Balance (EPB) via Muck Screw Conveyor
// -----------------------------------------------------------------------------
// Calculate pressure error
rPressureError := rActualEarthPressure - rTargetEarthPressure;

// Check for pressure alarm
IF ABS(rPressureError) > rMaxPressureDev THEN
    bPressureAlarm := TRUE;
ELSE
    bPressureAlarm := FALSE;
END_IF;

// Adjust muck screw speed to maintain earth pressure
rScrewSpeedAdj := rPressureError * rKp_EPB;

rMuckScrewSpeed_Cmd := rBaseScrewSpeed + rScrewSpeedAdj;

// Clamp muck screw speed 0.0 - 50.0 RPM
rMuckScrewSpeed_Cmd := LIMIT(0.0, rMuckScrewSpeed_Cmd, 50.0);

// Safety override: Stop muck screw if synchronization is lost or severe torque alarm
IF bSyncError THEN
    rMuckScrewSpeed_Cmd := 0.0;
END_IF;

END_FUNCTION_BLOCK"""

content = f"```iec-st\n{iec_st}\n```"
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": content}]}

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=4)
print(f"Saved to {filename}")
