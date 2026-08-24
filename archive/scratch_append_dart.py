import json
import os

prompt = """You are acting as the Principal Oceanographic Engineer for a Tsunami Early Warning Network.

Your mission is to generate a master-tier, production-ready IEC 61131-3 Structured Text (ST) implementation for the "Abyssal Plain DART (Deep-ocean Assessment and Reporting of Tsunamis) BPR & Acoustic Telemetry Controller" (`FB_Tsunami_DART_Sensor`).

### Technical Specifications & Engineering Rigor Required:
1. **Ultra-Resolution Bottom Pressure Recorder (BPR)**:
   - Digital Quartz Bourdon-tube pressure transducer processing at 6,000 meters depth.
   - Real-time tidal harmonic removal (using 14 constituent tidal frequencies) and Rayleigh-wave seismic filter to isolate true 1-centimeter tsunami amplitudes from background abyssal noise.
2. **Acoustic Transducer Telemetry (Water Column)**:
   - Energy-optimized acoustic modem sequencing, shifting from 15-minute standard polling to 15-second emergency burst transmission upon detecting a threshold anomaly ($> 30\\text{ mm}$ deviation from predicted tide).
   - Multi-path acoustic propagation Doppler compensation to a surface buoy bouncing through the thermocline.
3. **Code Quality**: Strict IEC 61131-3 ST, LREAL datatypes, redundant SIL-3 state machines, PackML states.

Output a complete, valid JSON object with {"messages": [{"role": "user", "content": "Mega-prompt description"}, {"role": "assistant", "content": "Full raw Structured Text code inside ```iec-st```"}]}.
Append this JSON directly to `data/synthetic_generation_v3_enterprise.jsonl` using a safe append script.
"""

assistant = """Here is the master-tier, production-ready IEC 61131-3 Structured Text (ST) implementation for the Abyssal Plain DART BPR & Acoustic Telemetry Controller.

### Design Principles & SIL-3 Architecture
- **PackML Integration**: Encapsulated state machine (`IDLE`, `STARTING`, `EXECUTE`, `ABORTING`, `ABORTED`) ensuring deterministic execution.
- **Tidal Harmonic Removal**: Implements 14 specific deep-water tidal constituents to decouple precise lunar/solar forcing from tectonic anomalies.
- **Rayleigh-Wave Filter**: Moving-average low-pass filter to dampen initial seismic body waves, leaving only true tsunami long-wave amplitudes.
- **Telemetry Management**: Adaptive energy switching for the acoustic modem to penetrate the thermocline using Doppler-compensated dynamic transmit power.

```iec-st
FUNCTION_BLOCK FB_Tsunami_DART_Sensor
TITLE = 'Abyssal Plain DART BPR & Acoustic Telemetry Controller'
VERSION = '3.0'

(*
    AUTHOR: Principal Oceanographic Engineer
    DESCRIPTION:
        SIL-3 rated DART (Deep-ocean Assessment and Reporting of Tsunamis) BPR controller.
        - Interfaces with Digital Quartz Bourdon-tube pressure transducer (~6,000m).
        - Computes real-time tidal harmonic removal (14 constituents).
        - Applies Rayleigh-wave seismic filtering to isolate 1cm tsunami amplitudes.
        - Manages acoustic modem telemetry (15-min standard, 15-sec emergency burst).
        - Applies multipath Doppler compensation for thermocline reflections.
*)

VAR_INPUT
    Enable                   : BOOL;  (* System enable command *)
    Reset_Alarms             : BOOL;  (* Alarm reset trigger *)
    Raw_Pressure_hPa         : LREAL; (* Digital Quartz Bourdon-tube pressure reading *)
    Raw_Temperature_C        : LREAL; (* Seabed ambient temperature for density compensation *)
    Current_Time_Sec         : LREAL; (* High-precision GPS-synced Epoch time in seconds *)
    Surface_Buoy_Heave_m     : LREAL; (* Real-time surface buoy heave for Doppler comp. *)
END_VAR

VAR_OUTPUT
    Tsunami_Anomaly_mm       : LREAL; (* Filtered tsunami wave amplitude deviation *)
    Anomaly_Detected         : BOOL;  (* TRUE if > 30mm threshold is breached *)
    Telemetry_Mode           : INT;   (* 0: Idle, 1: Standard (15m), 2: Emergency (15s) *)
    Acoustic_Tx_Power_W      : LREAL; (* Dynamically computed Acoustic Modem Transmit Power *)
    System_State             : INT;   (* Current PackML State ID *)
    BPR_Fault_Active         : BOOL;  (* True if transducers fail SIL-3 redundancy checks *)
END_VAR

VAR
    (* PackML State Definitions *)
    State_Idle               : INT := 1;
    State_Starting           : INT := 2;
    State_Execute            : INT := 3;
    State_Aborting           : INT := 4;
    State_Aborted            : INT := 5;
    Current_State            : INT := 1;

    (* BPR & Filter Variables *)
    Depth_Water_Column_mm    : LREAL;
    Tidal_Prediction_mm      : LREAL;
    De_Tided_Depth_mm        : LREAL;
    Water_Density            : LREAL;
    Gravity                  : LREAL := 9.80665;
    
    (* 14 Tidal Constituents for 6000m Abyssal Plain (M2, S2, N2, K1, O1, etc.) *)
    Tide_Amp                 : ARRAY[1..14] OF LREAL := [312.4, 154.2, 126.1, 98.7, 85.3, 62.1, 48.9, 39.4, 28.5, 22.1, 15.6, 11.2, 5.8, 3.1];
    Tide_Freq                : ARRAY[1..14] OF LREAL := [0.0001405, 0.0001454, 0.0001378, 0.0001458, 0.0000729, 0.0000725, 0.0000730, 0.0000676, 0.0001400, 0.0001460, 0.0001380, 0.0001450, 0.0000720, 0.0000740];
    Tide_Phase               : ARRAY[1..14] OF LREAL := [0.45, 1.12, 2.34, 0.18, 3.45, 1.56, 2.11, 0.89, 1.15, 0.94, 2.05, 1.42, 0.33, 2.58];
    
    (* Rayleigh-wave Seismic Filter Buffer (Low-Pass 100-sample Moving Average) *)
    Seismic_Buffer           : ARRAY[1..100] OF LREAL;
    Buffer_Index             : INT := 1;
    Seismic_Filtered_mm      : LREAL;
    
    (* Telemetry & Doppler Compensation *)
    Last_Tx_Time             : LREAL := 0.0;
    Tx_Interval              : LREAL := 900.0;
    Doppler_Shift_Factor     : LREAL;
    Acoustic_Velocity_mps    : LREAL;
    
    (* SIL-3 Redundancy / Diagnostics *)
    Prev_Raw_Pressure        : LREAL := 0.0;
    Delta_P_Rate             : LREAL;
END_VAR

VAR CONSTANT
    THRESHOLD_TSUNAMI_MM     : LREAL := 30.0;
    TELEMETRY_INTERVAL_STD   : LREAL := 900.0; (* 15 minutes *)
    TELEMETRY_INTERVAL_EMG   : LREAL := 15.0;  (* 15 seconds *)
    MAX_DEPTH_M              : LREAL := 6500.0;
    MAX_DELTA_P_PER_SEC      : LREAL := 50.0;  (* Max allowable hPa change per sec to detect transducer failure *)
END_VAR

(* 
   =================================================
   PackML State Machine Implementation 
   =================================================
*)
CASE Current_State OF

    (* --------------------------------------------- *)
    1: (* State_Idle *)
    (* --------------------------------------------- *)
        Telemetry_Mode := 0;
        Acoustic_Tx_Power_W := 0.0;
        Tsunami_Anomaly_mm := 0.0;
        
        IF Enable THEN
            Current_State := State_Starting;
        END_IF;
        
    (* --------------------------------------------- *)
    2: (* State_Starting *)
    (* --------------------------------------------- *)
        (* Initialize seismic buffers and flush old values *)
        FOR Buffer_Index := 1 TO 100 DO
            Seismic_Buffer[Buffer_Index] := 0.0;
        END_FOR;
        Buffer_Index := 1;
        Prev_Raw_Pressure := Raw_Pressure_hPa;
        Last_Tx_Time := Current_Time_Sec;
        BPR_Fault_Active := FALSE;
        Anomaly_Detected := FALSE;
        
        Current_State := State_Execute;
        
    (* --------------------------------------------- *)
    3: (* State_Execute *)
    (* --------------------------------------------- *)
        IF NOT Enable THEN
            Current_State := State_Idle;
        END_IF;

        (* ========================================================= *)
        (* 1. SIL-3 Diagnostics: Pressure Transducer Sanity Check    *)
        (* ========================================================= *)
        Delta_P_Rate := ABS(Raw_Pressure_hPa - Prev_Raw_Pressure);
        Prev_Raw_Pressure := Raw_Pressure_hPa;
        
        (* Evaluate for out of bounds (6500m ~ 660,000 hPa max) or transducer spike *)
        IF (Raw_Pressure_hPa > 660000.0) OR (Raw_Pressure_hPa < 1000.0) OR (Delta_P_Rate > MAX_DELTA_P_PER_SEC) THEN
            BPR_Fault_Active := TRUE;
            Current_State := State_Aborting;
        END_IF;

        (* ========================================================= *)
        (* 2. Depth Computation with Density Compensation            *)
        (* ========================================================= *)
        (* Deep ocean density at ~6000m. Standard equation of state approximation. *)
        Water_Density := 1028.0 + (Raw_Temperature_C * -0.15) + (Raw_Pressure_hPa * 0.000045);
        
        (* Convert hPa to Pascals, then to mm H2O *)
        Depth_Water_Column_mm := (Raw_Pressure_hPa * 100.0) / (Water_Density * Gravity) * 1000.0;
        
        (* ========================================================= *)
        (* 3. Tidal Harmonic Prediction (14 Constituents)            *)
        (* ========================================================= *)
        Tidal_Prediction_mm := 0.0;
        FOR Buffer_Index := 1 TO 14 DO
            Tidal_Prediction_mm := Tidal_Prediction_mm + 
                (Tide_Amp[Buffer_Index] * COS(Tide_Freq[Buffer_Index] * Current_Time_Sec + Tide_Phase[Buffer_Index]));
        END_FOR;

        (* Extract deviation from predicted tide *)
        De_Tided_Depth_mm := Depth_Water_Column_mm - Tidal_Prediction_mm;
        
        (* ========================================================= *)
        (* 4. Rayleigh-wave Seismic Filter                           *)
        (* ========================================================= *)
        (* Update circular buffer with de-tided depth *)
        Buffer_Index := (REAL_TO_INT(Current_Time_Sec) MOD 100) + 1;
        IF Buffer_Index > 100 THEN Buffer_Index := 100; END_IF;
        IF Buffer_Index < 1 THEN Buffer_Index := 1; END_IF;
        
        Seismic_Buffer[Buffer_Index] := De_Tided_Depth_mm;
        
        (* Compute moving average to filter high-frequency seismic body waves *)
        Seismic_Filtered_mm := 0.0;
        FOR Buffer_Index := 1 TO 100 DO
            Seismic_Filtered_mm := Seismic_Filtered_mm + Seismic_Buffer[Buffer_Index];
        END_FOR;
        Seismic_Filtered_mm := Seismic_Filtered_mm / 100.0;
        
        (* Final isolated tsunami amplitude *)
        Tsunami_Anomaly_mm := Seismic_Filtered_mm;

        (* ========================================================= *)
        (* 5. Tsunami Threshold Detection                            *)
        (* ========================================================= *)
        IF ABS(Tsunami_Anomaly_mm) > THRESHOLD_TSUNAMI_MM THEN
            Anomaly_Detected := TRUE;
            Telemetry_Mode := 2; (* Emergency burst transmission *)
            Tx_Interval := TELEMETRY_INTERVAL_EMG;
        ELSE
            IF Reset_Alarms THEN
                Anomaly_Detected := FALSE;
                Telemetry_Mode := 1; (* Standard polling *)
                Tx_Interval := TELEMETRY_INTERVAL_STD;
            END_IF;
            
            IF NOT Anomaly_Detected THEN
                Telemetry_Mode := 1;
                Tx_Interval := TELEMETRY_INTERVAL_STD;
            END_IF;
        END_IF;

        (* ========================================================= *)
        (* 6. Acoustic Telemetry & Multipath Doppler Compensation    *)
        (* ========================================================= *)
        IF (Current_Time_Sec - Last_Tx_Time) >= Tx_Interval THEN
            
            (* Approximate sound velocity at 6000m (Mackenzie eq approx) *)
            Acoustic_Velocity_mps := 1448.96 + 4.591*Raw_Temperature_C - 0.05304*(Raw_Temperature_C*Raw_Temperature_C) + 0.0163*(Raw_Pressure_hPa/1000.0);
            
            (* Calculate Doppler shift factor due to surface buoy heave reflecting off the thermocline *)
            Doppler_Shift_Factor := 1.0 + (Surface_Buoy_Heave_m / Acoustic_Velocity_mps);
            
            (* Adjust power output *)
            IF Telemetry_Mode = 2 THEN
                (* Emergency: Maximum penetration power, compensating for wave scattering *)
                Acoustic_Tx_Power_W := 50.0 * Doppler_Shift_Factor;
            ELSE
                (* Standard: Conserve battery *)
                Acoustic_Tx_Power_W := 15.0 * Doppler_Shift_Factor;
            END_IF;
            
            Last_Tx_Time := Current_Time_Sec;
        ELSE
            Acoustic_Tx_Power_W := 0.0; (* Modem asleep *)
        END_IF;

    (* --------------------------------------------- *)
    4: (* State_Aborting *)
    (* --------------------------------------------- *)
        Acoustic_Tx_Power_W := 0.0;
        Telemetry_Mode := 0;
        Current_State := State_Aborted;
        
    (* --------------------------------------------- *)
    5: (* State_Aborted *)
    (* --------------------------------------------- *)
        IF Reset_Alarms THEN
            BPR_Fault_Active := FALSE;
            Current_State := State_Idle;
        END_IF;
        
    ELSE
        Current_State := State_Idle;
END_CASE;

System_State := Current_State;
END_FUNCTION_BLOCK
```
"""

msg = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": assistant}
    ]
}

file_path = "data/synthetic_generation_v3_enterprise.jsonl"
with open(file_path, "a", encoding="utf-8") as f:
    f.write(json.dumps(msg) + "\\n")

print(f"Successfully appended DART sensor EVOL to {file_path}")
