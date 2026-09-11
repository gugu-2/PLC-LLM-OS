import json
import uuid
import os

# Ensure directories exist
os.makedirs('data/swarm_raw', exist_ok=True)
os.makedirs('data', exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Biomass Pelletizing Plant.
Task: Invent a highly complex control scenario for this domain (e.g., wood chip hammer mill load shedding, rotary drum dryer inlet temperature cascades, and pellet press die ring extrusion).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."""

st_code = """```iec-st
FUNCTION_BLOCK FB_BiomassPelletizingPlant
VAR_INPUT
    bStartProcess       : BOOL; // Command to start the pelletizing process
    bStopProcess        : BOOL; // Command to stop the pelletizing process
    bEmergencyStop      : BOOL; // Global emergency stop
    rHammerMillLoad     : REAL; // Current load of the wood chip hammer mill (kW)
    rDryerInletTemp     : REAL; // Current inlet temperature of the rotary drum dryer (Celsius)
    rDryerMoisture      : REAL; // Moisture content measured post-dryer (%)
    rPressDieTemp       : REAL; // Temperature of the pellet press die ring (Celsius)
    rPressMotorCurrent  : REAL; // Current of the pellet press motor (A)
    rSiloLevel          : REAL; // Biomass buffer silo level (%)
END_VAR
VAR_OUTPUT
    bHammerMillRun      : BOOL; // Command to run hammer mill
    rHammerMillFeedRate : REAL; // Feed rate to hammer mill (kg/h)
    bDryerRun           : BOOL; // Command to run rotary drum dryer
    rDryerBurnerPower   : REAL; // Burner power command for dryer (%)
    bPressRun           : BOOL; // Command to run pellet press
    rPressFeedRate      : REAL; // Feed rate to pellet press (kg/h)
    bCoolerRun          : BOOL; // Command to run pellet cooler
    bAlarmState         : BOOL; // General alarm state
    iState              : INT;  // State machine state
END_VAR
VAR
    // Hammer Mill Shedding Parameters
    rMaxMillLoad        : REAL := 250.0; // kW
    rSheddingThreshold  : REAL := 240.0; // kW
    // Dryer Cascade Parameters
    rTargetMoisture     : REAL := 10.0;  // %
    rMaxInletTemp       : REAL := 450.0; // Celsius
    // Press Die Parameters
    rMaxDieTemp         : REAL := 95.0;  // Celsius
    rMaxPressCurrent    : REAL := 300.0; // A
    
    // Internal state variables
    tMillSheddingTimer  : TON;
    tCoolingTimer       : TON;
    tPressOverloadTimer : TON;
END_VAR

// Main State Machine for Biomass Pelletizing Plant
IF bEmergencyStop THEN
    bHammerMillRun := FALSE;
    bDryerRun := FALSE;
    bPressRun := FALSE;
    bCoolerRun := FALSE;
    rHammerMillFeedRate := 0.0;
    rDryerBurnerPower := 0.0;
    rPressFeedRate := 0.0;
    bAlarmState := TRUE;
    iState := 999;
    RETURN;
END_IF;

CASE iState OF
    0: // Idle State
        bHammerMillRun := FALSE;
        bDryerRun := FALSE;
        bPressRun := FALSE;
        bCoolerRun := FALSE;
        IF bStartProcess THEN
            iState := 10;
        END_IF;
        
    10: // Start Dryer and Cooler
        bDryerRun := TRUE;
        bCoolerRun := TRUE;
        rDryerBurnerPower := 20.0; // Pilot/warm-up
        IF rDryerInletTemp > 200.0 THEN
            iState := 20;
        END_IF;
        
    20: // Start Hammer Mill
        bHammerMillRun := TRUE;
        rHammerMillFeedRate := 1000.0; // Initial feed rate
        IF rSiloLevel > 30.0 THEN
            iState := 30;
        END_IF;
        
    30: // Start Pellet Press
        bPressRun := TRUE;
        rPressFeedRate := 500.0;
        iState := 40;
        
    40: // Normal Operation & Complex Control Loops
        // 1. Wood Chip Hammer Mill Load Shedding
        IF rHammerMillLoad > rMaxMillLoad THEN
            rHammerMillFeedRate := rHammerMillFeedRate * 0.5; // Aggressive shedding
            bAlarmState := TRUE;
        ELSIF rHammerMillLoad > rSheddingThreshold THEN
            rHammerMillFeedRate := rHammerMillFeedRate - 50.0; // Gradual shedding
        ELSIF rHammerMillLoad < (rSheddingThreshold - 20.0) AND rSiloLevel < 80.0 THEN
            rHammerMillFeedRate := rHammerMillFeedRate + 10.0; // Recover feed
        END_IF;
        
        // Ensure feed rate bounds
        IF rHammerMillFeedRate > 5000.0 THEN rHammerMillFeedRate := 5000.0; END_IF;
        IF rHammerMillFeedRate < 500.0 THEN rHammerMillFeedRate := 500.0; END_IF;
        
        // 2. Rotary Drum Dryer Inlet Temperature Cascade
        // Master loop: Moisture control
        IF rDryerMoisture > (rTargetMoisture + 1.0) THEN
            rDryerBurnerPower := rDryerBurnerPower + 1.0;
        ELSIF rDryerMoisture < (rTargetMoisture - 1.0) THEN
            rDryerBurnerPower := rDryerBurnerPower - 1.0;
        END_IF;
        
        // Slave loop constraint: Inlet temp max limit
        IF rDryerInletTemp > rMaxInletTemp THEN
            rDryerBurnerPower := rDryerBurnerPower - 5.0; // Force reduction
            bAlarmState := TRUE;
        END_IF;
        
        // Ensure burner bounds
        IF rDryerBurnerPower > 100.0 THEN rDryerBurnerPower := 100.0; END_IF;
        IF rDryerBurnerPower < 20.0 THEN rDryerBurnerPower := 20.0; END_IF;
        
        // 3. Pellet Press Die Ring Extrusion Control
        IF rPressDieTemp > rMaxDieTemp OR rPressMotorCurrent > rMaxPressCurrent THEN
            tPressOverloadTimer(IN:=TRUE, PT:=T#3S);
            IF tPressOverloadTimer.Q THEN
                rPressFeedRate := rPressFeedRate - 100.0; // Shed load to press
                bAlarmState := TRUE;
            END_IF;
        ELSE
            tPressOverloadTimer(IN:=FALSE, PT:=T#3S);
            IF rSiloLevel > 50.0 AND rPressFeedRate < 2000.0 THEN
                rPressFeedRate := rPressFeedRate + 10.0; // Ramp up production
            END_IF;
        END_IF;
        
        // Press bounds
        IF rPressFeedRate < 200.0 THEN rPressFeedRate := 200.0; END_IF;
        IF rPressFeedRate > 3000.0 THEN rPressFeedRate := 3000.0; END_IF;
        
        // Process stop logic
        IF bStopProcess THEN
            iState := 50;
        END_IF;
        
    50: // Shutdown Sequence
        rHammerMillFeedRate := 0.0;
        rPressFeedRate := 0.0;
        tCoolingTimer(IN:=TRUE, PT:=T#60S);
        IF tCoolingTimer.Q THEN
            bHammerMillRun := FALSE;
            bPressRun := FALSE;
            rDryerBurnerPower := 0.0;
            iState := 60;
        END_IF;
        
    60: // Final Shutdown Phase
        tCoolingTimer(IN:=FALSE);
        IF rDryerInletTemp < 80.0 THEN
            bDryerRun := FALSE;
            bCoolerRun := FALSE;
            iState := 0;
        END_IF;
        
    999: // Emergency State
        IF NOT bEmergencyStop THEN
            bAlarmState := FALSE;
            iState := 0; 
        END_IF;
END_CASE;
```"""

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": st_code}
    ]
}

swarm_file = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(swarm_file, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)

with open("data/synthetic_generation_v3_enterprise.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\n")

print(f"Success: Wrote to {swarm_file} and appended to synthetic_generation_v3_enterprise.jsonl")
