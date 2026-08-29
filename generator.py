import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Solar Thermal Molten Salt Storage System.
Task: Invent a highly complex control scenario for this domain (e.g., cold/hot tank level mass balancing, freeze protection heat tracing cascades, and heat exchanger bypass).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O.
"""

st_code = """```iec-st
FUNCTION_BLOCK FB_MoltenSaltStorageManager
TITLE = 'Solar Thermal Molten Salt Storage Mass Balancing and Freeze Protection'
VERSION : '1.0'
AUTHOR : 'Lumina AI Cloud Swarm'

VAR_INPUT
    bSystemEnable : BOOL; // Main system enable
    rHotTankLevel : REAL; // Current hot tank level (%)
    rColdTankLevel : REAL; // Current cold tank level (%)
    rHotTankTemp : REAL; // Hot tank temperature (C)
    rColdTankTemp : REAL; // Cold tank temperature (C)
    rReceiverTemp : REAL; // Receiver outlet temperature (C)
    rTargetHotTemp : REAL; // Target hot temperature for salt (C)
    rAmbientTemp : REAL; // Ambient temperature (C)
    bEmergencyStop : BOOL; // Emergency stop signal
    bGridDemandHigh : BOOL; // High power demand from grid
    bSolarFieldReady : BOOL; // Solar field is focused and ready
END_VAR

VAR_OUTPUT
    bPumpColdToReceiver : BOOL; // Enable cold salt pump to receiver
    rColdPumpSpeed : REAL; // Cold salt pump speed command (0-100%)
    bPumpHotToGenerator : BOOL; // Enable hot salt pump to steam generator
    rHotPumpSpeed : REAL; // Hot salt pump speed command (0-100%)
    bHeatTracingHotPipes : BOOL; // Enable electrical heat tracing on hot piping
    bHeatTracingColdPipes : BOOL; // Enable electrical heat tracing on cold piping
    bReceiverBypassValve : BOOL; // Open receiver bypass (recirculation)
    rSystemStateCode : INT; // Current system state code
    bSystemFault : BOOL; // General fault flag
END_VAR

VAR
    rMassBalanceError : REAL;
    rTempDifferential : REAL;
    tFreezeTimer : TON;
    tBypassTimer : TON;
    bFreezeWarning : BOOL;
    rSaltFreezeTemp : REAL := 220.0; // Salt freezes below this temp (C)
    rSafeMargin : REAL := 20.0; // Safety margin for freeze protection (C)
    bIsCharging : BOOL;
    bIsDischarging : BOOL;
END_VAR

// Implementation Details
IF bEmergencyStop THEN
    bPumpColdToReceiver := FALSE;
    bPumpHotToGenerator := FALSE;
    rColdPumpSpeed := 0.0;
    rHotPumpSpeed := 0.0;
    bReceiverBypassValve := TRUE; // Fail-safe to bypass
    bHeatTracingHotPipes := TRUE; // Keep pipes warm to prevent freezing during e-stop
    bHeatTracingColdPipes := TRUE;
    rSystemStateCode := 999;
    bSystemFault := TRUE;
    RETURN;
END_IF;

IF NOT bSystemEnable THEN
    bPumpColdToReceiver := FALSE;
    bPumpHotToGenerator := FALSE;
    rColdPumpSpeed := 0.0;
    rHotPumpSpeed := 0.0;
    rSystemStateCode := 0; // Off state
    
    // Check freeze protection even when off
    bHeatTracingHotPipes := (rHotTankTemp < (rSaltFreezeTemp + rSafeMargin));
    bHeatTracingColdPipes := (rColdTankTemp < (rSaltFreezeTemp + rSafeMargin));
    RETURN;
END_IF;

// Reset fault if we get here
bSystemFault := FALSE;

// 1. Freeze Protection Logic
bFreezeWarning := (rAmbientTemp < 5.0) OR (rHotTankTemp < (rSaltFreezeTemp + rSafeMargin)) OR (rColdTankTemp < (rSaltFreezeTemp + rSafeMargin));
tFreezeTimer(IN:= bFreezeWarning, PT:= T#30s);

IF tFreezeTimer.Q THEN
    bHeatTracingHotPipes := TRUE;
    bHeatTracingColdPipes := TRUE;
    // If temp drops critically, activate circulation pump to prevent line freezing
    IF rHotTankTemp < (rSaltFreezeTemp + 10.0) THEN
        bPumpHotToGenerator := TRUE;
        rHotPumpSpeed := 15.0; // Low speed circulation
    END_IF;
ELSE
    bHeatTracingHotPipes := FALSE;
    bHeatTracingColdPipes := FALSE;
END_IF;

// 2. Solar Field Charging Logic (Cold -> Receiver -> Hot)
IF bSolarFieldReady AND (rHotTankLevel < 95.0) AND (rColdTankLevel > 5.0) THEN
    bIsCharging := TRUE;
    bPumpColdToReceiver := TRUE;
    
    // PID-like flow control based on receiver outlet temperature
    rTempDifferential := rTargetHotTemp - rReceiverTemp;
    
    IF rTempDifferential > 10.0 THEN
        // Receiver too cold, slow down pump to allow more heating
        rColdPumpSpeed := 30.0;
        bReceiverBypassValve := TRUE; // Recirculate until up to temp
    ELSIF rTempDifferential < -10.0 THEN
        // Receiver too hot, speed up pump
        rColdPumpSpeed := 90.0;
        bReceiverBypassValve := FALSE;
    ELSE
        // Ideal temperature range
        rColdPumpSpeed := 60.0;
        bReceiverBypassValve := FALSE;
    END_IF;
    
    // Delayed bypass closure
    tBypassTimer(IN:= (rTempDifferential <= 10.0), PT:= T#2m);
    IF tBypassTimer.Q THEN
        bReceiverBypassValve := FALSE;
    END_IF;
ELSE
    bIsCharging := FALSE;
    bPumpColdToReceiver := FALSE;
    rColdPumpSpeed := 0.0;
    bReceiverBypassValve := TRUE; // Default to bypass when not actively charging
END_IF;

// 3. Discharge Logic (Hot -> Steam Generator -> Cold)
IF bGridDemandHigh AND (rHotTankLevel > 5.0) THEN
    bIsDischarging := TRUE;
    bPumpHotToGenerator := TRUE;
    rHotPumpSpeed := 85.0; // Max flow for high demand
ELSIF (NOT bGridDemandHigh) AND (rHotTankLevel > 10.0) THEN
    bIsDischarging := TRUE;
    bPumpHotToGenerator := TRUE;
    rHotPumpSpeed := 40.0; // Base load flow
ELSE
    bIsDischarging := FALSE;
    // Don't turn off if freeze protection circulation is active
    IF NOT (tFreezeTimer.Q AND (rHotTankTemp < (rSaltFreezeTemp + 10.0))) THEN
        bPumpHotToGenerator := FALSE;
        rHotPumpSpeed := 0.0;
    END_IF;
END_IF;

// 4. Mass Balancing / Safety Cross-checks
rMassBalanceError := (rHotTankLevel + rColdTankLevel) - 100.0;
IF ABS(rMassBalanceError) > 5.0 THEN
    // Mass loss detected (potential leak or sensor failure)
    bSystemFault := TRUE;
    bPumpColdToReceiver := FALSE;
    bPumpHotToGenerator := FALSE;
    rColdPumpSpeed := 0.0;
    rHotPumpSpeed := 0.0;
    rSystemStateCode := 888; // Leak fault
    RETURN;
END_IF;

// State Assignment
IF bIsCharging AND bIsDischarging THEN
    rSystemStateCode := 3; // Simultaneous charge/discharge
ELSIF bIsCharging THEN
    rSystemStateCode := 1; // Charging only
ELSIF bIsDischarging THEN
    rSystemStateCode := 2; // Discharging only
ELSE
    rSystemStateCode := 4; // Standby
END_IF;

END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": st_code}]}

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f)

print(f"File saved to {filename}")
