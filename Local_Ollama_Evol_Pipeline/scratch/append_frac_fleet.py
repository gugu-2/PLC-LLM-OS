import json
import os

user_content = """You are acting as a Principal Petroleum Engineer for a top-tier Oil Services company (e.g., Halliburton). Evolve a basic pressure loop into a Multi-Pump Hydraulic Fracturing (Fracking) Fleet Controller.

Technical Specifications required in the ST code:
1. Fleet-wide harmonic torque synchronization across 20 massive diesel-driven triplex pumps running at 10,000 PSI to prevent resonant frequency vibration from destroying the manifold.
2. Proppant (sand) concentration blending control: dynamically adjust the dry-sand augers based on real-time radioactive densitometer readings in the slurry blender.
3. Cavitation detection algorithms using localized vibration spectral analysis (FFT) on each individual pump fluid end."""

assistant_content = """This is an enterprise-grade Multi-Pump Hydraulic Fracturing Fleet Controller implemented in IEC 61131-3 Structured Text. Operating a 20-pump fleet at 10,000 PSI involves extreme mechanical forces. If the cyclic torque pulsations of the 20 massive triplex pumps synchronize, they can cause a catastrophic resonant vibration that tears apart the high-pressure manifold (the "missile"). 

To mitigate this, this controller employs an active phase-shifting algorithm. It assigns a target crank angle offset to each pump relative to a master pump (e.g., 360 degrees / 20 pumps = 18 degrees phase shift per pump) to ensure destructive interference of pressure waves.

Additionally, it features a nuclear densitometer integration for dynamic proppant blending and FFT-based cavitation detection at the pump fluid ends.

### ST Implementation

```iecst
(* 
    Frac Fleet Controller - Tier 1 Enterprise Grade
    Architecture: IEC 61131-3 Structured Text (ST)
    System: Multi-Pump Hydraulic Fracturing Control
*)

TYPE UDT_Pump_Vibration_FFT :
STRUCT
    FundamentalFreq_Hz : REAL;
    Harmonic1_Magnitude : REAL;
    Harmonic2_Magnitude : REAL;
    HighFreqNoise_Cavitation : REAL; (* Spectral energy > 2kHz indicating cavitation *)
END_STRUCT
END_TYPE

TYPE UDT_TriplexPump :
STRUCT
    Active : BOOL;
    Pressure_PSI : REAL;
    RPM : REAL;
    Torque_NM : REAL;
    CrankAngle_Deg : REAL; (* High-speed encoder feedback *)
    Vibration : UDT_Pump_Vibration_FFT;
    SpeedCmd_RPM : REAL;
    Cavitation_Alarm : BOOL;
END_STRUCT
END_TYPE

PROGRAM PRG_FracFleetController
VAR CONSTANT
    MAX_PUMPS : INT := 20;
    TARGET_PRESSURE_PSI : REAL := 10000.0;
    CAVITATION_THRESHOLD : REAL := 85.5; 
    PHASE_SHIFT_DEG : REAL := 360.0 / 20.0; (* 18 degrees between each pump to avoid resonance *)
END_VAR

VAR
    FracPumps : ARRAY[1..MAX_PUMPS] OF UDT_TriplexPump;
    
    (* Manifold Pressure Control *)
    ManifoldPressure_PSI : REAL;
    PressureError : REAL;
    BaseSpeedCommand_RPM : REAL;
    Kp_Press : REAL := 0.05;
    Ki_Press : REAL := 0.01;
    PressIntegral : REAL;
    
    (* Harmonic Synchronization *)
    MasterAngle_Deg : REAL;
    AngleError : REAL;
    PhaseCorrection : REAL;
    Kp_Phase : REAL := 0.5;
    
    (* Proppant Blending Control *)
    TargetDensity_PPA : REAL := 4.0; (* Pounds of Proppant per Gallon *)
    RadioactiveDensitometer_Raw : REAL; 
    SlurryDensity_PPA : REAL; 
    AugerSpeedCmd_RPM : REAL;
    BlendError : REAL;
    Kp_Blend : REAL := 1.2;
    Ki_Blend : REAL := 0.3;
    BlendIntegral : REAL;
    
    i : INT;
END_VAR

(* ---------------------------------------------------------
   1. Fleet-Wide Pressure Control (Master Loop) 
   --------------------------------------------------------- *)
PressureError := TARGET_PRESSURE_PSI - ManifoldPressure_PSI;
PressIntegral := PressIntegral + (PressureError * 0.1); (* Assumes 100ms Task *)
BaseSpeedCommand_RPM := (Kp_Press * PressureError) + (Ki_Press * PressIntegral);

IF BaseSpeedCommand_RPM > 2100.0 THEN BaseSpeedCommand_RPM := 2100.0; END_IF;
IF BaseSpeedCommand_RPM < 0.0 THEN BaseSpeedCommand_RPM := 0.0; END_IF;

(* Establish Master Angle from the first active pump *)
FOR i := 1 TO MAX_PUMPS DO
    IF FracPumps[i].Active THEN
        MasterAngle_Deg := FracPumps[i].CrankAngle_Deg;
        EXIT;
    END_IF;
END_FOR;

(* ---------------------------------------------------------
   2. Anti-Resonance Sync & 3. Cavitation Detection
   --------------------------------------------------------- *)
FOR i := 1 TO MAX_PUMPS DO
    IF FracPumps[i].Active THEN
        
        (* Evaluate Fluid End Vibration FFT for Cavitation *)
        IF FracPumps[i].Vibration.HighFreqNoise_Cavitation > CAVITATION_THRESHOLD THEN
            FracPumps[i].Cavitation_Alarm := TRUE;
            (* De-rate pump speed to suppress cavitation and protect the fluid end *)
            FracPumps[i].SpeedCmd_RPM := BaseSpeedCommand_RPM * 0.7; 
        ELSE
            FracPumps[i].Cavitation_Alarm := FALSE;
            
            (* Harmonic Torque Synchronization (Active Phase Shifting) *)
            (* Target phase angle = Master Angle + (18 degrees * Pump Index) *)
            AngleError := (MasterAngle_Deg + (INT_TO_REAL(i - 1) * PHASE_SHIFT_DEG)) - FracPumps[i].CrankAngle_Deg;
            
            (* Normalize angle error between -180 and 180 degrees *)
            WHILE AngleError > 180.0 DO AngleError := AngleError - 360.0; END_WHILE;
            WHILE AngleError < -180.0 DO AngleError := AngleError + 360.0; END_WHILE;
            
            PhaseCorrection := AngleError * Kp_Phase;
            
            (* Superimpose phase correction on top of the base pressure demand *)
            FracPumps[i].SpeedCmd_RPM := BaseSpeedCommand_RPM + PhaseCorrection;
        END_IF;
    ELSE
        FracPumps[i].SpeedCmd_RPM := 0.0;
    END_IF;
END_FOR;

(* ---------------------------------------------------------
   4. Proppant Concentration Blending Control
   --------------------------------------------------------- *)
(* Scale the raw output from the radioactive densitometer to PPA *)
SlurryDensity_PPA := (RadioactiveDensitometer_Raw * 1.05) - 8.34; (* 8.34 = clean water weight *)

BlendError := TargetDensity_PPA - SlurryDensity_PPA;
BlendIntegral := BlendIntegral + (BlendError * 0.1);

(* PI Control for Dry-Sand Augers feeding the tub *)
AugerSpeedCmd_RPM := (Kp_Blend * BlendError) + (Ki_Blend * BlendIntegral);

IF AugerSpeedCmd_RPM > 100.0 THEN AugerSpeedCmd_RPM := 100.0; END_IF;
IF AugerSpeedCmd_RPM < 0.0 THEN AugerSpeedCmd_RPM := 0.0; END_IF;

END_PROGRAM
```"""

record = {
    "messages": [
        {"role": "user", "content": user_content},
        {"role": "assistant", "content": assistant_content}
    ]
}

file_path = r'C:\Users\majip\Downloads\LLM REASEARCH\Local_Ollama_Evol_Pipeline\data\synthetic_generation_v3_enterprise.jsonl'

with open(file_path, 'a') as f:
    f.write(json.dumps(record) + '\n')
