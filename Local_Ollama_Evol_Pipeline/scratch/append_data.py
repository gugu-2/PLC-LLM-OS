import json
import os

target_file = r"C:\Users\majip\Downloads\LLM REASEARCH\data\evol_instruct_dataset.jsonl"

user_prompt = """Evolve this basic state machine concept into a Geothermal Power Plant Steam Turbine sequencer. 
Implement reinjection well pump synchronization, H2S (Hydrogen Sulfide) gas abatement scrubber control, and turbine overspeed trip logic. 
Include complex state machines, safety interlocks (e.g., e-stops, thermal overloads), hardware abstractions, and flawless comments."""

assistant_response = """Here is a production-ready IEC 61131-3 Structured Text implementation of a Geothermal Power Plant Steam Turbine Sequencer. 

This highly robust function block incorporates a complex state machine for the turbine lifecycle, safety interlocks including overspeed and thermal overload, H2S abatement scrubber control, and reinjection well pump synchronization.

```iecst
(* 
    =============================================================================
    FUNCTION BLOCK: FB_GeothermalTurbineSequencer
    DESCRIPTION:    Advanced Geothermal Power Plant Steam Turbine Sequencer.
                    Manages startup, H2S abatement, grid synchronization, 
                    reinjection pumping, and critical safety interlocks.
    AUTHOR:         Lumina Elite Systems
    VERSION:        2.0.1
    =============================================================================
*)
FUNCTION_BLOCK FB_GeothermalTurbineSequencer
VAR_INPUT
    // Operator Commands
    xCmdStart             : BOOL;   // Operator command to initiate startup sequence
    xCmdStop              : BOOL;   // Operator command to initiate normal shutdown
    xCmdEStop             : BOOL;   // Emergency Stop (TRUE = Active/Trip)
    xResetFaults          : BOOL;   // Reset latched faults

    // Hardware Feedback & Sensors
    rTurbineSpeedRPM      : REAL;   // Current turbine speed in RPM
    rTurbineVibration     : REAL;   // Turbine vibration in mm/s
    rBearingTemp          : REAL;   // Main bearing temperature in °C
    rH2S_Concentration    : REAL;   // H2S gas concentration in ppm
    
    // Subsystem Status
    xScrubberReady        : BOOL;   // H2S scrubber system healthy and ready
    xReinjectionPumpReady : BOOL;   // Reinjection pump VFD ready
    xGridSyncOK           : BOOL;   // Generator is synchronized to the grid
END_VAR

VAR_OUTPUT
    // Actuators & Commands
    xMainSteamValve       : BOOL;   // Open main steam inlet valve
    xH2S_ScrubberPump     : BOOL;   // Command to run H2S abatement pump
    xReinjectionPumpCmd   : BOOL;   // Command to start reinjection pump
    xTripBreaker          : BOOL;   // Command to trip generator breaker
    
    // Status & Diagnostics
    iCurrentState         : INT;    // Active sequence state
    xFaultActive          : BOOL;   // General fault indicator
    sStatusMessage        : STRING[80]; // Human-readable status message
END_VAR

VAR
    // Trip Thresholds (Configurable)
    c_OverspeedLimit      : REAL := 3960.0; // 10% overspeed on 3600 RPM base
    c_VibrationLimit      : REAL := 8.5;    // Max allowable vibration (mm/s)
    c_BearingTempLimit    : REAL := 95.0;   // Max bearing temperature (°C)
    c_H2S_WarningLimit    : REAL := 50.0;   // H2S limit requiring max scrubbing
    
    // Sequence States
    STATE_STANDBY         : INT := 0;
    STATE_PRE_START       : INT := 10;
    STATE_TURBINE_ROLL    : INT := 20;
    STATE_SYNC            : INT := 30;
    STATE_RUNNING         : INT := 40;
    STATE_NORMAL_STOP     : INT := 50;
    STATE_TRIP            : INT := 99;

    // Timers
    fbScrubberWarmupTimer : TON;
    fbValveRampTimer      : TON;
    fbPumpSyncTimer       : TON;
    
    // Internal Fault Latches
    xOverspeedTrip        : BOOL;
    xVibTrip              : BOOL;
    xTempTrip             : BOOL;
    xEStopTrip            : BOOL;
END_VAR

BEGIN
    // =========================================================================
    // 1. SAFETY & CRITICAL INTERLOCKS (EVALUATED FIRST)
    // =========================================================================
    
    // E-Stop Evaluation
    IF xCmdEStop THEN
        xEStopTrip := TRUE;
    END_IF;

    // Overspeed Trip Logic
    IF rTurbineSpeedRPM > c_OverspeedLimit THEN
        xOverspeedTrip := TRUE;
    END_IF;

    // Thermal Overload / Bearing Temp Trip
    IF rBearingTemp > c_BearingTempLimit THEN
        xTempTrip := TRUE;
    END_IF;

    // High Vibration Trip
    IF rTurbineVibration > c_VibrationLimit THEN
        xVibTrip := TRUE;
    END_IF;

    // Fault Aggregation
    xFaultActive := xEStopTrip OR xOverspeedTrip OR xTempTrip OR xVibTrip;

    // Fault Reset Logic (Only if conditions cleared)
    IF xResetFaults AND NOT xCmdEStop THEN
        IF rTurbineSpeedRPM < (c_OverspeedLimit * 0.9) THEN xOverspeedTrip := FALSE; END_IF;
        IF rBearingTemp < (c_BearingTempLimit - 5.0) THEN xTempTrip := FALSE; END_IF;
        IF rTurbineVibration < (c_VibrationLimit - 1.0) THEN xVibTrip := FALSE; END_IF;
        xEStopTrip := FALSE;
    END_IF;

    // Immediate Trip Execution
    IF xFaultActive THEN
        iCurrentState := STATE_TRIP;
    END_IF;


    // =========================================================================
    // 2. MAIN STATE MACHINE
    // =========================================================================
    CASE iCurrentState OF
        
        // ---------------------------------------------------------------------
        STATE_STANDBY: 
            sStatusMessage := 'Standby: Ready to Start';
            xMainSteamValve := FALSE;
            xH2S_ScrubberPump := FALSE;
            xReinjectionPumpCmd := FALSE;
            xTripBreaker := FALSE;
            
            // State Transition
            IF xCmdStart AND NOT xFaultActive THEN
                iCurrentState := STATE_PRE_START;
            END_IF;

        // ---------------------------------------------------------------------
        STATE_PRE_START:
            sStatusMessage := 'Pre-Start: Initiating H2S Scrubber';
            xH2S_ScrubberPump := TRUE; // Start abatement before turbine roll
            
            // Wait for scrubber to be ready (simulated warmup timer)
            fbScrubberWarmupTimer(IN := xScrubberReady, PT := T#5s);
            
            IF fbScrubberWarmupTimer.Q AND NOT xCmdStop THEN
                iCurrentState := STATE_TURBINE_ROLL;
            ELSIF xCmdStop THEN
                iCurrentState := STATE_NORMAL_STOP;
            END_IF;

        // ---------------------------------------------------------------------
        STATE_TURBINE_ROLL:
            sStatusMessage := 'Turbine Roll: Admitting Steam';
            xMainSteamValve := TRUE; // Open steam valve to accelerate
            
            // Transition when approaching synchronous speed
            IF rTurbineSpeedRPM >= 3550.0 THEN
                iCurrentState := STATE_SYNC;
            END_IF;

        // ---------------------------------------------------------------------
        STATE_SYNC:
            sStatusMessage := 'Syncing: Waiting for Grid Synchronization';
            
            // Wait for AVR and synchronizer to match phase and close breaker
            IF xGridSyncOK THEN
                iCurrentState := STATE_RUNNING;
            END_IF;

        // ---------------------------------------------------------------------
        STATE_RUNNING:
            sStatusMessage := 'Running: Starting Reinjection Pumps';
            
            // Once synchronized, start reinjection of geothermal fluid
            fbPumpSyncTimer(IN := xReinjectionPumpReady AND xGridSyncOK, PT := T#3s);
            IF fbPumpSyncTimer.Q THEN
                xReinjectionPumpCmd := TRUE;
            END_IF;
            
            // Dynamic H2S Scrubber Control during run
            // Continuous operation in geothermal plants, boost if concentration rises
            xH2S_ScrubberPump := TRUE; 
            
            // Normal Shutdown request
            IF xCmdStop THEN
                iCurrentState := STATE_NORMAL_STOP;
            END_IF;

        // ---------------------------------------------------------------------
        STATE_NORMAL_STOP:
            sStatusMessage := 'Normal Stop: Unloading and Coasting Down';
            xMainSteamValve := FALSE; // Cut steam
            xTripBreaker := TRUE;     // Disconnect from grid
            
            // Stop reinjection when turbine drops below threshold
            IF rTurbineSpeedRPM < 1000.0 THEN
                xReinjectionPumpCmd := FALSE;
            END_IF;
            
            // Keep scrubber running until speed is 0 to manage tail gas
            IF rTurbineSpeedRPM < 10.0 THEN
                xH2S_ScrubberPump := FALSE;
                xTripBreaker := FALSE; // Reset trip command for next start
                iCurrentState := STATE_STANDBY;
            END_IF;

        // ---------------------------------------------------------------------
        STATE_TRIP:
            sStatusMessage := 'TRIP: Critical Safety Shutdown';
            xMainSteamValve := FALSE;
            xTripBreaker := TRUE;
            xReinjectionPumpCmd := FALSE;
            // Note: Scrubber kept ON during trip to handle vented gas!
            xH2S_ScrubberPump := TRUE; 
            
            IF NOT xFaultActive THEN
                // Faults have been cleared by operator
                xTripBreaker := FALSE;
                iCurrentState := STATE_STANDBY;
            END_IF;

        // ---------------------------------------------------------------------
        ELSE
            // Fallback for undefined states
            iCurrentState := STATE_TRIP;
            
    END_CASE;

    // Reset Timers if not in their respective states
    IF iCurrentState <> STATE_PRE_START THEN
        fbScrubberWarmupTimer(IN := FALSE, PT := T#5s);
    END_IF;
    
    IF iCurrentState <> STATE_RUNNING THEN
        fbPumpSyncTimer(IN := FALSE, PT := T#3s);
    END_IF;

END_FUNCTION_BLOCK
```
"""

msg = {
    "messages": [
        {"role": "user", "content": user_prompt},
        {"role": "assistant", "content": assistant_response}
    ]
}

with open(target_file, "a", encoding="utf-8") as f:
    f.write(json.dumps(msg) + "\n")

print("Successfully appended to dataset.")
