import json, uuid, os

os.makedirs('data/swarm_raw', exist_ok=True)
os.makedirs('data', exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Pharmaceutical Lyophilizer (Freeze Dryer).
Task: Invent a highly complex control scenario for this domain (e.g., primary sublimation vacuum curves, silicone oil thermal fluid cascades, and condenser chilling limits).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."""

st_code = '''```iec-st
FUNCTION_BLOCK FB_Lyophilizer_Cascade_Control
TITLE = 'Pharmaceutical Freeze Dryer Cascade Control'
// -----------------------------------------------------------------------------
// Author: Lumina AI Swarm
// Domain: Pharmaceutical Lyophilizer (Freeze Dryer)
// Description: Implements highly complex control scenario including:
//              1) Primary sublimation vacuum curves via PI control.
//              2) Silicone oil thermal fluid cascade PID (Shelf Temp -> Fluid Temp).
//              3) Condenser chilling limits and protective interlocks.
// -----------------------------------------------------------------------------

VAR_INPUT
    bEnableSystem : BOOL;                   // Global system enable
    bEmergencyStop : BOOL;                  // E-Stop interlock (NC)
    iActivePhase : INT;                     // 0:Idle, 1:Freeze, 2:Pri.Dry, 3:Sec.Dry, 4:Complete
    rShelfTemp_PV : REAL;                   // Process Value: Shelf Temperature (deg C)
    rThermalFluidTemp_PV : REAL;            // Process Value: Silicone Oil Temperature (deg C)
    rCondenserTemp_PV : REAL;               // Process Value: Condenser Coil Temperature (deg C)
    rChamberPressure_PV : REAL;             // Process Value: Absolute Chamber Pressure (mTorr)
    
    rTargetShelfTemp_SP : REAL;             // Setpoint: Shelf Temperature for current phase
    rTargetPressure_SP : REAL;              // Setpoint: Sublimation Vacuum Pressure (mTorr)
END_VAR

VAR_OUTPUT
    bVacuumPumpCmd : BOOL;                  // Command to start vacuum pump
    rVacuumBleedValveCmd : REAL;            // 0-100% analog command for nitrogen bleed
    bCompressorCmd : BOOL;                  // Command to start refrigeration compressor
    rHeaterPWM_Cmd : REAL;                  // 0-100% PWM command to silicone oil heater
    rCoolingValveCmd : REAL;                // 0-100% analog command to thermal fluid cooling heat exchanger
    bPhaseComplete : BOOL;                  // Signal that recipe phase logic allows transition
    iSystemAlarmCode : DINT;                // Active alarm code (0 = Normal)
END_VAR

VAR
    // Master PI Loop Parameters (Shelf Temperature)
    Kp_Shelf : REAL := 2.75;
    Ki_Shelf : REAL := 0.015;
    rErrorShelf : REAL;
    rIntegralShelf : REAL;
    rCalculatedFluid_SP : REAL;             // Cascaded Setpoint for thermal fluid
    
    // Slave PI Loop Parameters (Thermal Fluid)
    Kp_Fluid : REAL := 5.20;
    Ki_Fluid : REAL := 0.12;
    rErrorFluid : REAL;
    rIntegralFluid : REAL;
    rFluidControlEffort : REAL;
    
    // Vacuum PI Loop Parameters (Chamber Pressure)
    Kp_Press : REAL := 1.50;
    Ki_Press : REAL := 0.025;
    rErrorPress : REAL;
    rIntegralPress : REAL;
    
    // Limits & Interlocks
    bCondenserReady : BOOL;
    rMaxFluidTemp : REAL := 65.0;           // High limit for silicone oil (deg C)
    rMinFluidTemp : REAL := -55.0;          // Low limit for silicone oil (deg C)
    rCondenserLimit : REAL := -45.0;        // Maximum temp before vacuum starts (deg C)
    
    // Timers
    tVacuumStartupDelay : REAL := 0.0;
END_VAR

// =============================================================================
// 1. SAFETY & INTERLOCKS
// =============================================================================
IF bEmergencyStop THEN
    bVacuumPumpCmd := FALSE;
    rVacuumBleedValveCmd := 0.0;
    bCompressorCmd := FALSE;
    rHeaterPWM_Cmd := 0.0;
    rCoolingValveCmd := 0.0;
    iSystemAlarmCode := 999; // Critical E-STOP
    RETURN;
END_IF;

IF NOT bEnableSystem THEN
    bVacuumPumpCmd := FALSE;
    bCompressorCmd := FALSE;
    rHeaterPWM_Cmd := 0.0;
    rCoolingValveCmd := 0.0;
    iSystemAlarmCode := 0;
    RETURN;
END_IF;

// Condenser Interlock (Must be sufficiently chilled to trap vapor)
bCondenserReady := (rCondenserTemp_PV <= rCondenserLimit);
IF iActivePhase >= 1 THEN
    bCompressorCmd := TRUE; // Run compressor during all active recipe phases
ELSE
    bCompressorCmd := FALSE;
END_IF;

// =============================================================================
// 2. PRIMARY SUBLIMATION VACUUM CONTROL
// =============================================================================
IF (iActivePhase = 2 OR iActivePhase = 3) AND bCondenserReady THEN
    bVacuumPumpCmd := TRUE;
    
    // Calculate Error (Setpoint - Process Value)
    rErrorPress := rTargetPressure_SP - rChamberPressure_PV;
    
    // Accumulate Integral with anti-windup clamping
    rIntegralPress := rIntegralPress + rErrorPress;
    IF rIntegralPress > 2000.0 THEN rIntegralPress := 2000.0; END_IF;
    IF rIntegralPress < -2000.0 THEN rIntegralPress := -2000.0; END_IF;
    
    // Calculate Bleed Valve Command
    rVacuumBleedValveCmd := (Kp_Press * rErrorPress) + (Ki_Press * rIntegralPress);
    
    // Output Clamp (0% to 100%)
    IF rVacuumBleedValveCmd > 100.0 THEN rVacuumBleedValveCmd := 100.0; END_IF;
    IF rVacuumBleedValveCmd < 0.0 THEN rVacuumBleedValveCmd := 0.0; END_IF;
ELSE
    bVacuumPumpCmd := FALSE;
    rVacuumBleedValveCmd := 0.0;
    rIntegralPress := 0.0; // Reset integrator when not active
END_IF;

// =============================================================================
// 3. SILICONE OIL THERMAL FLUID CASCADE CONTROL
// =============================================================================
IF iActivePhase >= 1 AND iActivePhase <= 3 THEN
    // MASTER LOOP: Shelf Temperature Control
    rErrorShelf := rTargetShelfTemp_SP - rShelfTemp_PV;
    rIntegralShelf := rIntegralShelf + rErrorShelf;
    
    // Anti-windup for Master Loop
    IF rIntegralShelf > 1000.0 THEN rIntegralShelf := 1000.0; END_IF;
    IF rIntegralShelf < -1000.0 THEN rIntegralShelf := -1000.0; END_IF;
    
    // Cascade Setpoint Calculation
    rCalculatedFluid_SP := rShelfTemp_PV + (Kp_Shelf * rErrorShelf) + (Ki_Shelf * rIntegralShelf);
    
    // Restrict Cascaded Setpoint to Safe Fluid Limits
    IF rCalculatedFluid_SP > rMaxFluidTemp THEN rCalculatedFluid_SP := rMaxFluidTemp; END_IF;
    IF rCalculatedFluid_SP < rMinFluidTemp THEN rCalculatedFluid_SP := rMinFluidTemp; END_IF;
    
    // SLAVE LOOP: Thermal Fluid Temperature Control
    rErrorFluid := rCalculatedFluid_SP - rThermalFluidTemp_PV;
    rIntegralFluid := rIntegralFluid + rErrorFluid;
    
    // Anti-windup for Slave Loop
    IF rIntegralFluid > 500.0 THEN rIntegralFluid := 500.0; END_IF;
    IF rIntegralFluid < -500.0 THEN rIntegralFluid := -500.0; END_IF;
    
    rFluidControlEffort := (Kp_Fluid * rErrorFluid) + (Ki_Fluid * rIntegralFluid);
    
    // Split-Range Output to Heater and Cooler
    IF rFluidControlEffort > 0.0 THEN
        rHeaterPWM_Cmd := rFluidControlEffort;
        rCoolingValveCmd := 0.0;
    ELSE
        rHeaterPWM_Cmd := 0.0;
        rCoolingValveCmd := ABS(rFluidControlEffort);
    END_IF;
    
    // Output Clamp (0% to 100%)
    IF rHeaterPWM_Cmd > 100.0 THEN rHeaterPWM_Cmd := 100.0; END_IF;
    IF rCoolingValveCmd > 100.0 THEN rCoolingValveCmd := 100.0; END_IF;
    
ELSE
    // Reset thermal control if not active
    rHeaterPWM_Cmd := 0.0;
    rCoolingValveCmd := 0.0;
    rIntegralShelf := 0.0;
    rIntegralFluid := 0.0;
END_IF;

// =============================================================================
// 4. ALARMS & DIAGNOSTICS
// =============================================================================
iSystemAlarmCode := 0; // Default healthy state
IF rThermalFluidTemp_PV > (rMaxFluidTemp + 5.0) THEN
    iSystemAlarmCode := 101; // ALM 101: Thermal fluid catastrophic over-temp
    rHeaterPWM_Cmd := 0.0;
ELSIF rCondenserTemp_PV > -30.0 AND iActivePhase = 2 THEN
    iSystemAlarmCode := 102; // ALM 102: Condenser warming during primary drying
END_IF;

// Phase Completion Logic (Simplified)
IF iActivePhase = 4 THEN
    bPhaseComplete := TRUE;
ELSE
    bPhaseComplete := FALSE;
END_IF;

END_FUNCTION_BLOCK
```'''

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": st_code}]}

# Save standalone file
file_uuid = uuid.uuid4().hex[:8]
fname = f"data/swarm_raw/agent_{file_uuid}.json"
with open(fname, 'w', encoding='utf-8') as f:
    json.dump(record, f, indent=2)

# Append to JSONL
with open('data/synthetic_generation_v3_enterprise.jsonl', 'a', encoding='utf-8') as f:
    f.write(json.dumps(record) + '\\n')

print(f"Generated {fname}")
