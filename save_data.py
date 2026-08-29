import json
import uuid
import os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Multi-Lane Pasta Extrusion Line.
Task: Invent a highly complex control scenario for this domain (e.g., dough hydration rheology loops, bronze die vacuum extrusion pressure, and multi-stage drying humidity curves).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O.

CRITICAL RULES:
1. You MUST output the code enclosed in a ```iec-st markdown code fence. DO NOT APOLOGIZE. DO NOT EXPLAIN.
2. The code must be >= 1500 chars, with FUNCTION_BLOCK and VAR_INPUT/VAR_OUTPUT."""

code = """```iec-st
FUNCTION_BLOCK FB_MultiLanePastaExtrusion
VAR_INPUT
    bEnable                 : BOOL;         // Master enable for the extrusion line
    bEmergencyStop          : BOOL;         // E-Stop condition
    rTargetDoughHydration   : REAL;         // Target dough moisture content (%)
    rFlourFeedRateSP        : REAL;         // Target flour feed rate (kg/h)
    rWaterTempSP            : REAL;         // Target water temperature (deg C)
    rVacuumPressureSP       : REAL;         // Target vacuum in extrusion chamber (mBar)
    rDieTempSP              : REAL;         // Target bronze die temperature (deg C)
    rCuttingSpeedSP         : REAL;         // Target knife cutting speed (Cuts/min)
    rDryingZone1HumiditySP  : REAL;         // Pre-drying stage humidity (%)
    rDryingZone2HumiditySP  : REAL;         // Main drying stage humidity (%)
END_VAR

VAR_OUTPUT
    bSystemReady            : BOOL;         // System is ready for production
    bProductionActive       : BOOL;         // Extrusion is currently active
    rActualHydration        : REAL;         // Measured dough hydration (%)
    rExtrusionPressure      : REAL;         // Actual die head pressure (Bar)
    rActualDieTemp          : REAL;         // Measured die temperature (deg C)
    bHydrationAlarm         : BOOL;         // Hydration out of tolerance
    bVacuumAlarm            : BOOL;         // Vacuum level lost
    bPressureAlarm          : BOOL;         // Extrusion pressure too high
    bDieTempAlarm           : BOOL;         // Die temperature out of bounds
END_VAR

VAR
    // Hydration Control Loop (PID)
    fbHydrationPID          : PID;
    rWaterFlowRate          : REAL;         // Calculated water flow (L/h)
    
    // Extrusion Drive Control
    fbExtruderDrive         : MC_Power;
    fbExtruderVelocity      : MC_MoveVelocity;
    rScrewSpeed             : REAL;         // Extruder screw RPM
    rScrewTorque            : REAL;         // Extruder motor torque (%)
    
    // Vacuum Control Loop (PID)
    fbVacuumPID             : PID;
    rVacuumValveOpen        : REAL;         // Vacuum valve position (%)
    rActualVacuum           : REAL;         // Measured vacuum (mBar)
    
    // Die Temperature Control
    fbDieHeatingPID         : PID;
    rDieHeaterPower         : REAL;         // Die heater PWM duty cycle (%)
    
    // Timers & State Machine
    tonStartDelay           : TON;
    tonHydrationStable      : TON;
    tonPressureCheck        : TON;
    iExtrusionState         : INT;          // State machine step
    
    // Rheology and Physics Simulation Variables
    rDoughViscosity         : REAL;         // Estimated dough viscosity (Pa.s)
    rDieResistance          : REAL;         // Flow resistance of bronze die
END_VAR

// ==============================================================================
// Multi-Lane Pasta Extrusion Line - Core Control Logic
// Handles dough hydration rheology loops, bronze die vacuum extrusion pressure, 
// and multi-stage drying integration.
// ==============================================================================

IF bEmergencyStop THEN
    iExtrusionState := 999; // Error / E-Stop state
END_IF;

IF NOT bEnable AND NOT bEmergencyStop THEN
    iExtrusionState := 0;
    bSystemReady := FALSE;
    bProductionActive := FALSE;
    rWaterFlowRate := 0.0;
    rScrewSpeed := 0.0;
    // Reset Alarms
    bHydrationAlarm := FALSE;
    bVacuumAlarm := FALSE;
    bPressureAlarm := FALSE;
    bDieTempAlarm := FALSE;
    RETURN;
END_IF;

CASE iExtrusionState OF
    0: // Initialization & Self-Test
        bSystemReady := FALSE;
        tonStartDelay(IN:=TRUE, PT:=T#3S);
        IF tonStartDelay.Q THEN
            iExtrusionState := 10;
            tonStartDelay(IN:=FALSE);
        END_IF;
        
    10: // Die Pre-heating Phase
        fbDieHeatingPID(
            ACT := rActualDieTemp,
            SET := rDieTempSP,
            SUP := 2.0, TR := 15.0, TD := 2.0, K := 1.8,
            Y => rDieHeaterPower
        );
        // Simulate die heating
        rActualDieTemp := rActualDieTemp + (rDieHeaterPower * 0.01);
        
        IF ABS(rActualDieTemp - rDieTempSP) < 2.0 THEN
            iExtrusionState := 20;
        END_IF;
        
    20: // Vacuum Chamber Evacuation
        fbVacuumPID(
            ACT := rActualVacuum,
            SET := rVacuumPressureSP,
            SUP := 1.0, TR := 5.0, TD := 0.5, K := 2.5,
            Y => rVacuumValveOpen
        );
        // Simulate vacuum drawdown
        rActualVacuum := rActualVacuum - (rVacuumValveOpen * 0.5);
        IF rActualVacuum < 0.0 THEN rActualVacuum := 0.0; END_IF;
        
        IF ABS(rActualVacuum - rVacuumPressureSP) < 50.0 THEN
            bSystemReady := TRUE;
            iExtrusionState := 30;
        END_IF;
        
    30: // Hydration & Dosing Phase
        // Dough rheology calculation based on feed rate and water flow
        rActualHydration := (rWaterFlowRate / (rFlourFeedRateSP + 0.01)) * 100.0;
        
        fbHydrationPID(
            ACT := rActualHydration,
            SET := rTargetDoughHydration,
            SUP := 2.0, TR := 10.0, TD := 1.0, K := 1.2,
            Y => rWaterFlowRate
        );
        
        tonHydrationStable(IN := (ABS(rActualHydration - rTargetDoughHydration) < 1.5), PT := T#5S);
        
        IF tonHydrationStable.Q THEN
            iExtrusionState := 40;
        END_IF;
        
        // Alarm Handling
        bHydrationAlarm := (ABS(rActualHydration - rTargetDoughHydration) > 5.0);
        bVacuumAlarm := (ABS(rActualVacuum - rVacuumPressureSP) > 100.0);
        
    40: // Active Extrusion & Pressure Monitoring
        bProductionActive := TRUE;
        
        // Extrusion screw speed based on flour feed rate
        rScrewSpeed := rFlourFeedRateSP * 0.45;
        
        // Rheology feedback: Calculate viscosity based on hydration and temperature
        rDoughViscosity := 5000.0 / (rActualHydration + 0.1) * (50.0 / (rActualDieTemp + 0.1));
        rDieResistance := 15.5; // Constant for bronze die geometry
        
        // Calculate Extrusion Pressure
        rExtrusionPressure := (rScrewSpeed * rDoughViscosity * rDieResistance) / 1000.0;
        
        tonPressureCheck(IN := (rExtrusionPressure > 120.0), PT := T#2S);
        IF tonPressureCheck.Q THEN
            bPressureAlarm := TRUE;
            iExtrusionState := 999; // Fault state
        END_IF;
        
        // Maintain continuous background loops
        fbDieHeatingPID(ACT := rActualDieTemp, SET := rDieTempSP, Y => rDieHeaterPower);
        fbVacuumPID(ACT := rActualVacuum, SET := rVacuumPressureSP, Y => rVacuumValveOpen);
        fbHydrationPID(ACT := rActualHydration, SET := rTargetDoughHydration, Y => rWaterFlowRate);
        
    999: // Error / Emergency Stop Handling
        bSystemReady := FALSE;
        bProductionActive := FALSE;
        rWaterFlowRate := 0.0;
        rScrewSpeed := 0.0;
        rVacuumValveOpen := 0.0;
        rDieHeaterPower := 0.0;
        
        IF NOT bEmergencyStop AND NOT bPressureAlarm THEN
            iExtrusionState := 0; // Ready for reset
        END_IF;
        
    ELSE
        iExtrusionState := 0;
END_CASE;

END_FUNCTION_BLOCK
```"""

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": code}
    ]
}

swarm_dir = "data/swarm_raw"
os.makedirs(swarm_dir, exist_ok=True)
filename = f"{swarm_dir}/agent_{uuid.uuid4().hex[:8]}.json"

with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f)

v3_file = "data/synthetic_generation_v3_enterprise.jsonl"
with open(v3_file, "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\\n")
