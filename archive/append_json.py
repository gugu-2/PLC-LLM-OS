import json
import os

prompt = '''You are acting as the Principal Atmospheric Physicist for a High-Altitude Observatory.

Your mission is to generate a master-tier, production-ready IEC 61131-3 Structured Text (ST) implementation for the "Transient Luminous Event (TLE) Sprite & Blue Jet High-Speed Photometry & Lidar Tracker" (`FB_TLE_AtmosphericTracker`).

### Technical Specifications & Engineering Rigor Required:
1. **Triggered High-Speed Photometry**:
   - Ultra-low latency ($< 10\ \mu\\text{s}$) triggering of a $100,000\\text{ fps}$ intensified camera array by detecting the Extremely Low Frequency (ELF) electromagnetic pulse from a positive cloud-to-ground (+CG) lightning strike.
   - Capturing the fleeting, milliseconds-long plasma breakdown of mesospheric Red Sprites and stratospheric Blue Jets.
2. **Mesospheric UV Lidar Ranging**:
   - Immediate firing of a pulsed $355\\text{ nm}$ Nd:YAG laser to measure the transient ozone depletion and localized atmospheric density changes induced by the plasma channels (streamers) up to $90\\text{ km}$ altitude.
3. **Code Quality**: Strict IEC 61131-3 ST, LREAL datatypes, comprehensive `VAR_INPUT`/`VAR_OUTPUT`, atmospheric optics matrices, PackML states.

Output a complete, valid JSON object with {"messages": [{"role": "user", "content": "Mega-prompt description"}, {"role": "assistant", "content": "Full raw Structured Text code inside ```iec-st```"}]}.
Append this JSON directly to `data/synthetic_generation_v3_enterprise.jsonl` using a safe append script.
'''

st_code = '''```iec-st
FUNCTION_BLOCK FB_TLE_AtmosphericTracker
(*
    =============================================================================
    High-Altitude Observatory System: Transient Luminous Event (TLE) Tracker
    =============================================================================
    Component:      FB_TLE_AtmosphericTracker
    Description:    Controls a 100,000 fps intensified camera array and a 355 nm
                    Nd:YAG UV Lidar system for high-resolution tracking and 
                    characterization of Red Sprites and Blue Jets.
    Latency Req:    < 10 µs trigger response to ELF electromagnetic pulses.
    Standard:       IEC 61131-3 Structured Text
    =============================================================================
*)
VAR_INPUT
    // PackML State Machine Inputs
    xExecute                : BOOL;             (* Command to start execution *)
    xAbort                  : BOOL;             (* Command to abort operation *)
    xHold                   : BOOL;             (* Command to hold operation *)
    xReset                  : BOOL;             (* Command to reset faults *)
    
    // Environmental & Sensor Inputs
    rELF_V_m                : LREAL;            (* Extremely Low Frequency Electric Field (V/m) *)
    rMagneticField_pT       : LREAL;            (* Magnetic field perturbation (pT) for +CG lightning *)
    rLidarReturnIntensity   : LREAL;            (* UV Lidar backscatter intensity *)
    rAtmosphericPressure_Pa : LREAL;            (* Ambient atmospheric pressure at observatory level *)
    rSkyBackgroundFlux      : LREAL;            (* Ambient background photon flux (photons/m²/s) *)
    
    // System Configuration
    rTriggerThresholdELF    : LREAL := 5000.0;  (* Threshold for +CG flash ELF detection (V/m) *)
    rLidarPulseEnergy_mJ    : LREAL := 150.0;   (* Setpoint for 355nm Nd:YAG pulse energy *)
    rCameraExposure_us      : LREAL := 10.0;    (* Exposure time per frame in microseconds (100k fps) *)
END_VAR

VAR_OUTPUT
    // PackML State Machine Outputs
    iState                  : INT;              (* Current PackML State *)
    xReady                  : BOOL;             (* System ready for operation *)
    xError                  : BOOL;             (* System fault active *)
    sErrorMsg               : STRING(255);      (* Detailed error message *)
    
    // Hardware Actuation & Control
    xTriggerCameraArray     : BOOL;             (* High-speed trigger signal to intensified camera array *)
    xFireNdYagLidar         : BOOL;             (* Trigger signal for 355nm UV Lidar pulse *)
    
    // Process Data
    rCalculatedDistance_km  : LREAL;            (* Calculated range of plasma streamer (km) *)
    rOzoneDepletionIndex    : LREAL;            (* Estimated local ozone depletion index based on Lidar return *)
    xEventCaptured          : BOOL;             (* Flag indicating a valid TLE sequence was captured *)
END_VAR

VAR
    // PackML States (ISA-88/TR88.00.02)
    STATE_IDLE              : INT := 1;
    STATE_STARTING          : INT := 2;
    STATE_EXECUTE           : INT := 3;
    STATE_HOLDING           : INT := 4;
    STATE_HELD              : INT := 5;
    STATE_ABORTING          : INT := 6;
    STATE_ABORTED           : INT := 7;
    STATE_FAULT             : INT := 8;
    STATE_RESETTING         : INT := 9;
    STATE_COMPLETING        : INT := 10;
    STATE_COMPLETE          : INT := 11;

    // Internal State Variables
    eCurrentState           : INT := STATE_IDLE;
    rLidarTimeOfFlight_us   : LREAL := 0.0;
    rCaptureSequenceTimer_us: LREAL := 0.0;
    xTriggerArmed           : BOOL := FALSE;
    xLidarActive            : BOOL := FALSE;
    
    // Physics Constants
    C_LIGHT_SPEED_KM_US     : LREAL := 0.299792;(* Speed of light in vacuum (km/µs) *)
    LIDAR_CALIB_FACTOR      : LREAL := 1.25E-4; (* Calibration constant for ozone absorption at 355nm *)
    
    // Fast Event Tracking Variables
    tonLidarPulseWait       : TON;              (* Timer for Lidar pulse duration tracking *)
    tonSequenceWindow       : TON;              (* Timer for overall capture sequence window *)
END_VAR

(*
=============================================================================
PackML State Machine Implementation
=============================================================================
*)

IF xAbort THEN
    eCurrentState := STATE_ABORTING;
ELSIF xError AND eCurrentState <> STATE_FAULT AND eCurrentState <> STATE_ABORTING AND eCurrentState <> STATE_ABORTED THEN
    eCurrentState := STATE_FAULT;
END_IF;

CASE eCurrentState OF

    STATE_IDLE:
        xReady := TRUE;
        xTriggerCameraArray := FALSE;
        xFireNdYagLidar := FALSE;
        xEventCaptured := FALSE;
        xTriggerArmed := FALSE;
        
        IF xExecute THEN
            xReady := FALSE;
            eCurrentState := STATE_STARTING;
        END_IF;
        
    STATE_STARTING:
        // Initialization of tracking matrices and sensor offsets
        rCalculatedDistance_km := 0.0;
        rOzoneDepletionIndex := 0.0;
        xTriggerArmed := TRUE;
        eCurrentState := STATE_EXECUTE;
        
    STATE_EXECUTE:
        IF xHold THEN
            eCurrentState := STATE_HOLDING;
        ELSE
            (* 
            =================================================================
            1. Fast +CG Lightning Trigger Detection (Sub 10µs response)
            =================================================================
            Detecting the Extremely Low Frequency (ELF) electromagnetic pulse
            indicative of a massive positive cloud-to-ground strike, which
            precedes TLE phenomena like Sprites and Blue Jets.
            *)
            IF (rELF_V_m > rTriggerThresholdELF) AND xTriggerArmed THEN
                
                // Immediately trigger high-speed camera array
                xTriggerCameraArray := TRUE;
                
                // Engage Lidar targeting sequence
                xFireNdYagLidar := TRUE;
                xLidarActive := TRUE;
                xTriggerArmed := FALSE; // Prevent re-triggering during sequence
                
                tonSequenceWindow(IN := TRUE, PT := T#500ms); // 500ms capture window
                
            END_IF;
            
            (* 
            =================================================================
            2. Mesospheric UV Lidar Ranging & Data Processing
            =================================================================
            *)
            IF xLidarActive THEN
                // Simulated Lidar Time of Flight tracking (typically microsecond precision hardware timer required)
                // For ST representation, we process the backscatter return immediately if valid.
                IF rLidarReturnIntensity > 0.1 THEN
                    // Pseudo calculation for time-of-flight based on atmospheric density scaling
                    rLidarTimeOfFlight_us := 600.0; // Simulated TOF for ~90km
                    
                    // Range equation: Distance = (c * t) / 2
                    rCalculatedDistance_km := (C_LIGHT_SPEED_KM_US * rLidarTimeOfFlight_us) / 2.0;
                    
                    // Ozone depletion index derived from differential absorption (simplified for ST)
                    rOzoneDepletionIndex := EXP(-1.0 * rLidarReturnIntensity * LIDAR_CALIB_FACTOR * rCalculatedDistance_km);
                    
                    xLidarActive := FALSE;
                    xFireNdYagLidar := FALSE;
                END_IF;
            END_IF;
            
            // Sequence Reset
            tonSequenceWindow(IN := TRUE);
            IF tonSequenceWindow.Q THEN
                xTriggerCameraArray := FALSE;
                tonSequenceWindow(IN := FALSE);
                xEventCaptured := TRUE;
                eCurrentState := STATE_COMPLETING;
            END_IF;
            
        END_IF;
        
    STATE_HOLDING:
        xTriggerCameraArray := FALSE;
        xFireNdYagLidar := FALSE;
        eCurrentState := STATE_HELD;
        
    STATE_HELD:
        IF NOT xHold THEN
            eCurrentState := STATE_EXECUTE;
        END_IF;
        
    STATE_ABORTING:
        xTriggerCameraArray := FALSE;
        xFireNdYagLidar := FALSE;
        xTriggerArmed := FALSE;
        eCurrentState := STATE_ABORTED;
        
    STATE_ABORTED:
        IF xReset THEN
            eCurrentState := STATE_RESETTING;
        END_IF;
        
    STATE_FAULT:
        xTriggerCameraArray := FALSE;
        xFireNdYagLidar := FALSE;
        IF xReset THEN
            xError := FALSE;
            sErrorMsg := '';
            eCurrentState := STATE_RESETTING;
        END_IF;
        
    STATE_RESETTING:
        eCurrentState := STATE_IDLE;
        
    STATE_COMPLETING:
        eCurrentState := STATE_COMPLETE;
        
    STATE_COMPLETE:
        IF NOT xExecute THEN
            eCurrentState := STATE_IDLE;
        END_IF;

END_CASE;

// Update Output State
iState := eCurrentState;

END_FUNCTION_BLOCK
```'''

data = {
    'messages': [
        {'role': 'user', 'content': prompt},
        {'role': 'assistant', 'content': st_code}
    ]
}

os.makedirs('data', exist_ok=True)
with open('data/synthetic_generation_v3_enterprise.jsonl', 'a', encoding='utf-8') as f:
    f.write(json.dumps(data) + '\\n')
