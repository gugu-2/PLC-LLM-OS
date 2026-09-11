import os, json, uuid

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Sugar Centrifuge Refining.
Task: Invent a highly complex control scenario for this domain (e.g., massecuite basket purging RPM profiles, wash water spray timing cascades, and plow scraper positioning).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."""

code = """```iec-st
FUNCTION_BLOCK FB_SugarCentrifugeRefiner
TITLE = 'Sugar Centrifuge Refining Control'
VERSION : '1.0'
AUTHOR  : 'Lumina Swarm'
NAME    : 'SugCent'
FAMILY  : 'Centrifugals'

VAR_INPUT
    bEnable : BOOL; // Enable centrifuge sequence
    bEmergencyStop : BOOL; // E-Stop
    rTargetPurgeRPM : REAL; // Target RPM for purging
    rTargetWashRPM : REAL; // Target RPM for washing
    rTargetDischargeRPM : REAL; // Target RPM for discharging
    rMassecuiteTemp : REAL; // Temperature of incoming massecuite
    bVibrationHigh : BOOL; // High vibration interlock
    rBasketLoadMass : REAL; // Mass in the basket
END_VAR

VAR_OUTPUT
    bMotorRun : BOOL; // Command to drive motor
    rMotorSpeedRef : REAL; // Speed reference to VFD
    bWashWaterValve : BOOL; // Wash water spray valve
    bSteamValve : BOOL; // Steam valve
    bPlowExtend : BOOL; // Extend plow scraper
    bPlowRetract : BOOL; // Retract plow scraper
    iCurrentState : INT; // Current state of state machine
    bCycleComplete : BOOL; // True when sequence finishes
    bFaultActive : BOOL; // System fault
END_VAR

VAR
    TMR_Charge : TON; // Charging timer
    TMR_Purge : TON; // Purging timer
    TMR_Wash : TON; // Washing timer
    TMR_Spin : TON; // Final spin timer
    TMR_PlowDelay : TON; // Plow delay timer
    
    eState : (
        STATE_IDLE,
        STATE_ACCEL_CHARGE,
        STATE_CHARGING,
        STATE_ACCEL_PURGE,
        STATE_PURGING,
        STATE_ACCEL_WASH,
        STATE_WASHING,
        STATE_SPINNING,
        STATE_DECEL_DISCHARGE,
        STATE_PLOWING,
        STATE_STOPPING,
        STATE_FAULT
    ) := STATE_IDLE;
    
    rCurrentRPM : REAL := 0.0;
    bInitialize : BOOL := TRUE;
END_VAR

// Control Logic
IF bEmergencyStop OR bVibrationHigh THEN
    eState := STATE_FAULT;
END_IF;

CASE eState OF
    STATE_IDLE:
        bMotorRun := FALSE;
        rMotorSpeedRef := 0.0;
        bWashWaterValve := FALSE;
        bSteamValve := FALSE;
        bPlowExtend := FALSE;
        bPlowRetract := TRUE;
        bCycleComplete := FALSE;
        
        IF bEnable AND NOT bFaultActive THEN
            eState := STATE_ACCEL_CHARGE;
        END_IF;

    STATE_ACCEL_CHARGE:
        bMotorRun := TRUE;
        rMotorSpeedRef := 200.0; // Charge RPM
        IF rCurrentRPM >= 195.0 THEN
            eState := STATE_CHARGING;
            TMR_Charge(IN := FALSE);
        END_IF;

    STATE_CHARGING:
        // Feed massecuite into basket
        TMR_Charge(IN := TRUE, PT := T#20S);
        IF TMR_Charge.Q OR (rBasketLoadMass > 1500.0) THEN
            eState := STATE_ACCEL_PURGE;
            TMR_Charge(IN := FALSE);
        END_IF;

    STATE_ACCEL_PURGE:
        rMotorSpeedRef := rTargetPurgeRPM;
        IF rCurrentRPM >= (rTargetPurgeRPM - 10.0) THEN
            eState := STATE_PURGING;
            TMR_Purge(IN := FALSE);
        END_IF;

    STATE_PURGING:
        // Separate molasses from crystals
        TMR_Purge(IN := TRUE, PT := T#45S);
        IF TMR_Purge.Q THEN
            eState := STATE_ACCEL_WASH;
            TMR_Purge(IN := FALSE);
        END_IF;

    STATE_ACCEL_WASH:
        rMotorSpeedRef := rTargetWashRPM;
        IF rCurrentRPM >= (rTargetWashRPM - 10.0) THEN
            eState := STATE_WASHING;
            TMR_Wash(IN := FALSE);
        END_IF;

    STATE_WASHING:
        bWashWaterValve := TRUE;
        bSteamValve := TRUE; // Apply steam to clean crystals
        TMR_Wash(IN := TRUE, PT := T#30S);
        IF TMR_Wash.Q THEN
            bWashWaterValve := FALSE;
            bSteamValve := FALSE;
            eState := STATE_SPINNING;
            TMR_Spin(IN := FALSE);
        END_IF;

    STATE_SPINNING:
        rMotorSpeedRef := 1200.0; // Max spin speed
        TMR_Spin(IN := TRUE, PT := T#60S);
        IF TMR_Spin.Q THEN
            eState := STATE_DECEL_DISCHARGE;
            TMR_Spin(IN := FALSE);
        END_IF;

    STATE_DECEL_DISCHARGE:
        rMotorSpeedRef := rTargetDischargeRPM; // e.g., 50 RPM
        IF rCurrentRPM <= (rTargetDischargeRPM + 5.0) THEN
            eState := STATE_PLOWING;
            TMR_PlowDelay(IN := FALSE);
        END_IF;

    STATE_PLOWING:
        bPlowRetract := FALSE;
        bPlowExtend := TRUE;
        TMR_PlowDelay(IN := TRUE, PT := T#15S); // Time to scrape sugar out
        IF TMR_PlowDelay.Q THEN
            bPlowExtend := FALSE;
            bPlowRetract := TRUE;
            eState := STATE_STOPPING;
        END_IF;

    STATE_STOPPING:
        rMotorSpeedRef := 0.0;
        IF rCurrentRPM <= 5.0 THEN
            bMotorRun := FALSE;
            bCycleComplete := TRUE;
            eState := STATE_IDLE;
        END_IF;

    STATE_FAULT:
        bMotorRun := FALSE;
        rMotorSpeedRef := 0.0;
        bWashWaterValve := FALSE;
        bSteamValve := FALSE;
        bPlowExtend := FALSE;
        bPlowRetract := TRUE; // Retract for safety
        bFaultActive := TRUE;
        
        IF NOT bEmergencyStop AND NOT bVibrationHigh AND NOT bEnable THEN
            bFaultActive := FALSE;
            eState := STATE_IDLE;
        END_IF;
END_CASE;

// State tracking for external SCADA
iCurrentState := eState;
END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)

print("JSON generation complete")
