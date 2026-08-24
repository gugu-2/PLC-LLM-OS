import json
import os

prompt = "Evolve a basic state machine into a massive Orbital Space Launch Pad Sequencer. Implement Liquid Oxygen (LOX) / Liquid Hydrogen (LH2) cryogenic fueling sequences, sparker ignition verification, and T-0 umbilical retraction interlocks."

assistant_response = """This transformation upgrades a basic state machine into a massive, production-grade Orbital Space Launch Pad Sequencer. It introduces complex IEC 61131-3 structures, precise terminal countdown management, robust safety interlocks, and dedicated fault-handling for cryogenic fueling and ignition.

```pascal
TYPE E_LaunchState :
(
    IDLE := 0,
    SYSTEM_DIAGNOSTICS := 10,
    CRYOGENIC_CHILLDOWN := 20,
    PROPELLANT_LOAD_SLOW := 30,
    PROPELLANT_LOAD_FAST := 40,
    PROPELLANT_TOP_OFF := 50,
    TERMINAL_COUNT_AUTO := 60,
    ENGINE_CHILLDOWN := 70,
    SPARKER_IGNITION := 80,
    ENGINE_START_SEQ := 90,
    THRUST_BUILDUP := 100,
    UMBILICAL_RETRACT := 110,
    HOLD_DOWN_RELEASE := 120,
    LIFTOFF := 130,
    ABORT_SAFE := 999
);
END_TYPE

FUNCTION_BLOCK FB_OrbitalLaunchSequencer
TITLE = 'Orbital Launch Pad Sequencer'
VERSION : '3.0'
AUTHOR : 'Lumina'

VAR_INPUT
    bStartSequence : BOOL;            // Initiate auto-sequence (T-Minus start)
    bAbort : BOOL;                    // Master E-Stop / Abort
    bManualOverride : BOOL;           // Override for manual operations
    
    // Hardware Feedback & Sensors
    fLOX_TankLevel : REAL;            // Liquid Oxygen tank level (%)
    fLH2_TankLevel : REAL;            // Liquid Hydrogen tank level (%)
    fLOX_Pressure : REAL;             // LOX line pressure (psi)
    fLH2_Pressure : REAL;             // LH2 line pressure (psi)
    fEngineTemp : REAL;               // Engine bell temperature (K)
    
    bLOX_ChilldownComplete : BOOL;    // Thermal sensor confirmation
    bLH2_ChilldownComplete : BOOL;
    
    bSparkerFeedback1 : BOOL;         // Ignition sparker 1 current feedback
    bSparkerFeedback2 : BOOL;         // Ignition sparker 2 current feedback
    bEngineIgnitionDetect : BOOL;     // Optical / Thermal engine ignition sensor
    fEngineThrust : REAL;             // Thrust measurement (kN)
    
    bUmbilicalRetracted : BOOL;       // T-0 umbilical physical limit switch
    bHoldDownClampsReleased : BOOL;   // Pyrotechnic clamp release feedback
END_VAR

VAR_OUTPUT
    eState : E_LaunchState := IDLE;   // Current sequence state
    
    // Actuators
    bCmd_LOX_Fill_Slow : BOOL;
    bCmd_LOX_Fill_Fast : BOOL;
    bCmd_LH2_Fill_Slow : BOOL;
    bCmd_LH2_Fill_Fast : BOOL;
    bCmd_LOX_Bleed : BOOL;
    bCmd_LH2_Bleed : BOOL;
    bCmd_LOX_Prevalves : BOOL;
    bCmd_LH2_Prevalves : BOOL;
    bCmd_Sparkers : BOOL;
    bCmd_EngineStart : BOOL;
    bCmd_UmbilicalRetract : BOOL;
    bCmd_ReleaseClamps : BOOL;
    bCmd_WaterDeluge : BOOL;          // Sound suppression system
    
    // HMI Status
    bSequenceComplete : BOOL;
    bAborted : BOOL;
    nAbortCode : INT;                 // 0=None, 1=Manual, 2=Thermal, 3=Sensor, 4=Thrust
    fT_MinusTime : REAL := 600.0;     // T-Minus in seconds (Starts at T-10m)
END_VAR

VAR
    fbCountdown : TON;
    fbWatchdog : TON;
    bInternalAbort : BOOL;
    rDeltaT : REAL := 0.1;            // Assuming 100ms cycle time for simulation
END_VAR

BEGIN
    // =========================================================================
    // SAFETY INTERLOCKS & MASTER ABORT EVALUATION
    // =========================================================================
    IF bAbort THEN
        bInternalAbort := TRUE;
        nAbortCode := 1; // Manual Abort
    END_IF;
    
    // Critical Overpressure Check during fueling
    IF (fLOX_Pressure > 120.0 OR fLH2_Pressure > 80.0) AND (eState >= CRYOGENIC_CHILLDOWN AND eState < LIFTOFF) THEN
        bInternalAbort := TRUE;
        nAbortCode := 3; // Sensor/Pressure Fault
    END_IF;
    
    // If an abort is triggered, immediately transition to ABORT_SAFE
    IF bInternalAbort AND eState <> ABORT_SAFE THEN
        eState := ABORT_SAFE;
    END_IF;

    // =========================================================================
    // SEQUENCER STATE MACHINE
    // =========================================================================
    CASE eState OF
    
        IDLE:
            bCmd_LOX_Fill_Slow := FALSE; bCmd_LOX_Fill_Fast := FALSE;
            bCmd_LH2_Fill_Slow := FALSE; bCmd_LH2_Fill_Fast := FALSE;
            bCmd_LOX_Bleed := FALSE; bCmd_LH2_Bleed := FALSE;
            bCmd_LOX_Prevalves := FALSE; bCmd_LH2_Prevalves := FALSE;
            bCmd_Sparkers := FALSE; bCmd_EngineStart := FALSE;
            bCmd_UmbilicalRetract := FALSE; bCmd_ReleaseClamps := FALSE;
            bCmd_WaterDeluge := FALSE;
            bAborted := FALSE;
            nAbortCode := 0;
            
            IF bStartSequence AND NOT bInternalAbort AND NOT bManualOverride THEN
                eState := SYSTEM_DIAGNOSTICS;
                fbWatchdog(IN := FALSE); // Reset watchdog
            END_IF;
            
        SYSTEM_DIAGNOSTICS:
            // Verify sensor sanity before proceeding
            IF fLOX_TankLevel < 5.0 AND fLH2_TankLevel < 5.0 THEN
                eState := CRYOGENIC_CHILLDOWN;
                fbWatchdog(IN := FALSE);
            ELSE
                bInternalAbort := TRUE;
                nAbortCode := 3; // Residual propellants detected
            END_IF;
            
        CRYOGENIC_CHILLDOWN:
            // Command bleed valves open to chill lines
            bCmd_LOX_Bleed := TRUE;
            bCmd_LH2_Bleed := TRUE;
            
            fbWatchdog(IN := TRUE, PT := T#300s); // 5 minute max chilldown
            
            IF bLOX_ChilldownComplete AND bLH2_ChilldownComplete THEN
                bCmd_LOX_Bleed := FALSE;
                bCmd_LH2_Bleed := FALSE;
                eState := PROPELLANT_LOAD_SLOW;
                fbWatchdog(IN := FALSE);
            ELSIF fbWatchdog.Q THEN
                bInternalAbort := TRUE;
                nAbortCode := 2; // Thermal timeout
            END_IF;
            
        PROPELLANT_LOAD_SLOW:
            // Begin initial slow fill to avoid thermal shock
            bCmd_LOX_Fill_Slow := TRUE;
            bCmd_LH2_Fill_Slow := TRUE;
            
            IF fLOX_TankLevel > 15.0 AND fLH2_TankLevel > 15.0 THEN
                eState := PROPELLANT_LOAD_FAST;
            END_IF;
            
        PROPELLANT_LOAD_FAST:
            bCmd_LOX_Fill_Slow := FALSE;
            bCmd_LH2_Fill_Slow := FALSE;
            bCmd_LOX_Fill_Fast := TRUE;
            bCmd_LH2_Fill_Fast := TRUE;
            
            IF fLOX_TankLevel >= 95.0 AND fLH2_TankLevel >= 95.0 THEN
                eState := PROPELLANT_TOP_OFF;
            END_IF;
            
        PROPELLANT_TOP_OFF:
            bCmd_LOX_Fill_Fast := FALSE;
            bCmd_LH2_Fill_Fast := FALSE;
            bCmd_LOX_Fill_Slow := TRUE;
            bCmd_LH2_Fill_Slow := TRUE;
            
            IF fLOX_TankLevel >= 99.5 AND fLH2_TankLevel >= 99.5 THEN
                bCmd_LOX_Fill_Slow := FALSE;
                bCmd_LH2_Fill_Slow := FALSE;
                eState := TERMINAL_COUNT_AUTO;
            END_IF;
            
        TERMINAL_COUNT_AUTO:
            // Enter terminal count - Start Water Deluge Sound Suppression
            bCmd_WaterDeluge := TRUE;
            IF fT_MinusTime <= 15.0 THEN
                eState := ENGINE_CHILLDOWN;
            END_IF;
            
        ENGINE_CHILLDOWN:
            // Open prevalves to allow cryogenic propellants into engine pumps
            bCmd_LOX_Prevalves := TRUE;
            bCmd_LH2_Prevalves := TRUE;
            
            IF fT_MinusTime <= 6.0 THEN
                eState := SPARKER_IGNITION;
                fbWatchdog(IN := FALSE);
            END_IF;
            
        SPARKER_IGNITION:
            bCmd_Sparkers := TRUE;
            fbWatchdog(IN := TRUE, PT := T#2s);
            
            IF bSparkerFeedback1 AND bSparkerFeedback2 THEN
                eState := ENGINE_START_SEQ;
                fbWatchdog(IN := FALSE);
            ELSIF fbWatchdog.Q THEN
                bInternalAbort := TRUE;
                nAbortCode := 3; // Sparker failure
            END_IF;
            
        ENGINE_START_SEQ:
            bCmd_EngineStart := TRUE;
            IF fT_MinusTime <= 3.0 THEN
                eState := THRUST_BUILDUP;
                fbWatchdog(IN := FALSE);
            END_IF;
            
        THRUST_BUILDUP:
            fbWatchdog(IN := TRUE, PT := T#3s);
            IF fEngineThrust >= 8500.0 AND bEngineIgnitionDetect THEN
                eState := UMBILICAL_RETRACT;
                fbWatchdog(IN := FALSE);
            ELSIF fbWatchdog.Q THEN
                bInternalAbort := TRUE;
                nAbortCode := 4; // Low thrust or ignition failure
            END_IF;
            
        UMBILICAL_RETRACT:
            bCmd_UmbilicalRetract := TRUE;
            fbWatchdog(IN := TRUE, PT := T#1s);
            
            IF bUmbilicalRetracted THEN
                eState := HOLD_DOWN_RELEASE;
                fbWatchdog(IN := FALSE);
            ELSIF fbWatchdog.Q THEN
                bInternalAbort := TRUE;
                nAbortCode := 3; // Umbilical hang-up
            END_IF;
            
        HOLD_DOWN_RELEASE:
            IF fT_MinusTime <= 0.0 THEN
                bCmd_ReleaseClamps := TRUE;
                IF bHoldDownClampsReleased THEN
                    eState := LIFTOFF;
                END_IF;
            END_IF;
            
        LIFTOFF:
            bSequenceComplete := TRUE;
            // Pad is clear, shut off pad services
            bCmd_WaterDeluge := FALSE;
            bCmd_Sparkers := FALSE;
            bCmd_LOX_Prevalves := FALSE;
            bCmd_LH2_Prevalves := FALSE;
            
        ABORT_SAFE:
            // Safing sequence
            bAborted := TRUE;
            bCmd_LOX_Fill_Fast := FALSE; bCmd_LH2_Fill_Fast := FALSE;
            bCmd_LOX_Fill_Slow := FALSE; bCmd_LH2_Fill_Slow := FALSE;
            bCmd_Sparkers := FALSE;
            bCmd_EngineStart := FALSE;
            bCmd_ReleaseClamps := FALSE;
            
            // Close prevalves
            bCmd_LOX_Prevalves := FALSE;
            bCmd_LH2_Prevalves := FALSE;
            
            // Keep water deluge on if fire risk, else shut off
            bCmd_WaterDeluge := FALSE;
            
            // Allow manual override to take over for detanking
            IF bManualOverride THEN
                bInternalAbort := FALSE;
                eState := IDLE;
            END_IF;
            
    END_CASE;

    // =========================================================================
    // TERMINAL COUNTDOWN CLOCK MANAGEMENT
    // =========================================================================
    // Countdown decrements from TERMINAL_COUNT_AUTO to HOLD_DOWN_RELEASE
    IF eState >= TERMINAL_COUNT_AUTO AND eState <= HOLD_DOWN_RELEASE AND NOT bInternalAbort THEN
        fbCountdown(IN := NOT fbCountdown.Q, PT := T#100ms);
        IF fbCountdown.Q THEN
            fT_MinusTime := fT_MinusTime - 0.1;
        END_IF;
    END_IF;
    
    // Reset clock if aborted before liftoff
    IF bAborted THEN
        fT_MinusTime := 600.0;
    END_IF;

END_FUNCTION_BLOCK
```"""

payload = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": assistant_response}
    ]
}

target_file = r"C:\Users\majip\Downloads\LLM REASEARCH\data\evol_instruct_dataset.jsonl"
with open(target_file, "a", encoding="utf-8") as f:
    f.write(json.dumps(payload) + "\\n")

print("Successfully appended to dataset.")
