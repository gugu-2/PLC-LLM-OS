import json
import sys

prompt = """You are acting as a Lead Metallurgical Engineer. Evolve a basic motion block into a Continuous Caster Controller for a Steel Mill. Technical Specs: 1. Tundish slide-gate metal level control using eddy-current sensors. 2. Water-cooled copper mold oscillation frequency matrices. 3. Secondary cooling zone water spray tracking based on steel solidification point."""

assistant = """```pascal
(* 
   =================================================================================================
   Lumina Steel Mill - Continuous Caster Controller (CCC)
   =================================================================================================
   Version: 3.0.0
   Standard: IEC 61131-3 Structured Text
   Description:
   Enterprise-grade continuous caster controller module integrating tundish level regulation, 
   copper mold oscillation, and thermodynamic secondary cooling control.

   Technical Specifications Implemented:
   1. Tundish slide-gate metal level control using dual eddy-current sensor feedback and PID loop.
   2. Water-cooled copper mold oscillation frequency matrices based on real-time casting speed.
   3. Secondary cooling zone water spray tracking using dynamic solidification point estimation.
   =================================================================================================
*)

TYPE ST_EddyCurrentSensor :
STRUCT
    LevelRaw           : REAL;   (* Raw mm value *)
    SignalQuality      : REAL;   (* 0.0 to 100.0% *)
    SensorFault        : BOOL;   
    CalibrationOffset  : REAL;
END_STRUCT
END_TYPE

TYPE ST_MoldOscillator :
STRUCT
    FrequencyCmd       : REAL;   (* Hz *)
    StrokeLengthCmd    : REAL;   (* mm *)
    PhaseAngle         : REAL;   (* degrees *)
    DriveEnable        : BOOL;
    DriveFault         : BOOL;
END_STRUCT
END_TYPE

TYPE ST_CoolingZone :
STRUCT
    ZoneID             : INT;
    WaterFlowCmd       : REAL;   (* L/min *)
    AirFlowCmd         : REAL;   (* L/min *)
    SurfaceTemp        : REAL;   (* Deg C *)
    SolidificationFrac : REAL;   (* 0.0 to 1.0 *)
END_STRUCT
END_TYPE

FUNCTION_BLOCK FB_ContinuousCasterController
VAR_INPUT
    EnableCasting           : BOOL;
    CastingSpeedSetpoint    : REAL;   (* m/min *)
    SteelGradeID            : DINT;
    TundishLevelTarget      : REAL;   (* mm *)
    
    Sensor1                 : ST_EddyCurrentSensor;
    Sensor2                 : ST_EddyCurrentSensor;
    
    ActualCastingSpeed      : REAL;   (* m/min *)
    MoldWaterTempIn         : REAL;   (* Deg C *)
    MoldWaterTempOut        : REAL;   (* Deg C *)
END_VAR

VAR_OUTPUT
    SlideGatePositionCmd    : REAL;   (* 0.0 to 100.0% *)
    OscillatorDrive         : ST_MoldOscillator;
    SecondaryCoolingZones   : ARRAY[1..7] OF ST_CoolingZone;
    
    SystemReady             : BOOL;
    TundishLevelAlarm       : BOOL;
    BreakoutWarning         : BOOL;
END_VAR

VAR
    (* Tundish PID Control Variables *)
    LevelError              : REAL;
    LevelErrorPrev          : REAL;
    LevelIntegral           : REAL;
    LevelDerivative         : REAL;
    ActiveLevel             : REAL;
    
    Kp_Level                : REAL := 2.5;
    Ki_Level                : REAL := 0.8;
    Kd_Level                : REAL := 0.15;
    
    (* Oscillation Matrix Params *)
    NegativeStripTimeTarget : REAL := 0.12; (* seconds *)
    LeadFactor              : REAL := 1.2;
    
    (* Secondary Cooling Params *)
    CoolingCurves           : ARRAY[1..5, 1..7] OF REAL; (* [GradeIndex, Zone] Water Flow Base *)
    ThermalConductivity     : REAL;
    SpecificHeat            : REAL;
    Density                 : REAL := 7850.0; (* kg/m3 *)
    LiquidusTemp            : REAL;
    SolidusTemp             : REAL;
    
    TimeStep                : REAL := 0.01; (* 10ms task *)
    i                       : INT;
    GradeIndex              : INT;
    
    (* Local Variables for Calculations *)
    V_cast_sec              : REAL;
    CoolingSpeedMultiplier  : REAL;
    SolidificationTime      : REAL;
    DistanceTravelled       : REAL;
    DeltaT                  : REAL;
    HeatFlux                : REAL;
END_VAR

(* -----------------------------------------------------------------------------
   1. STEEL GRADE INITIALIZATION & THERMAL PROPERTIES
----------------------------------------------------------------------------- *)
CASE SteelGradeID OF
    1008: (* Low Carbon *)
        LiquidusTemp := 1530.0;
        SolidusTemp := 1495.0;
        ThermalConductivity := 35.0;
        SpecificHeat := 650.0;
        GradeIndex := 1;
    1045: (* Medium Carbon *)
        LiquidusTemp := 1495.0;
        SolidusTemp := 1410.0;
        ThermalConductivity := 32.0;
        SpecificHeat := 680.0;
        GradeIndex := 2;
    304: (* Stainless *)
        LiquidusTemp := 1450.0;
        SolidusTemp := 1400.0;
        ThermalConductivity := 16.2;
        SpecificHeat := 500.0;
        GradeIndex := 3;
    ELSE
        (* Default to Safe Low Carbon *)
        LiquidusTemp := 1530.0;
        SolidusTemp := 1495.0;
        ThermalConductivity := 35.0;
        SpecificHeat := 650.0;
        GradeIndex := 1;
END_CASE;

(* Load Base Cooling Flow Matrix (L/min) based on Grade *)
IF EnableCasting THEN
    CoolingCurves[1,1] := 150.0; CoolingCurves[1,2] := 120.0; CoolingCurves[1,3] := 90.0;
    CoolingCurves[1,4] := 70.0;  CoolingCurves[1,5] := 50.0;  CoolingCurves[1,6] := 30.0; CoolingCurves[1,7] := 20.0;
    
    CoolingCurves[2,1] := 130.0; CoolingCurves[2,2] := 100.0; CoolingCurves[2,3] := 80.0;
    CoolingCurves[2,4] := 60.0;  CoolingCurves[2,5] := 40.0;  CoolingCurves[2,6] := 20.0; CoolingCurves[2,7] := 10.0;
    
    (* Replicate for missing indexes safely *)
    FOR i := 3 TO 5 DO
        CoolingCurves[i,1] := 140.0; CoolingCurves[i,2] := 110.0; CoolingCurves[i,3] := 85.0;
        CoolingCurves[i,4] := 65.0;  CoolingCurves[i,5] := 45.0;  CoolingCurves[i,6] := 25.0; CoolingCurves[i,7] := 15.0;
    END_FOR;
END_IF;

(* -----------------------------------------------------------------------------
   2. TUNDISH SLIDE-GATE METAL LEVEL CONTROL (EDDY-CURRENT)
----------------------------------------------------------------------------- *)
(* Sensor Fusion: Average the healthy eddy-current sensors *)
IF NOT Sensor1.SensorFault AND NOT Sensor2.SensorFault AND 
   (Sensor1.SignalQuality > 80.0) AND (Sensor2.SignalQuality > 80.0) THEN
    ActiveLevel := ((Sensor1.LevelRaw + Sensor1.CalibrationOffset) + 
                    (Sensor2.LevelRaw + Sensor2.CalibrationOffset)) / 2.0;
ELSIF NOT Sensor1.SensorFault THEN
    ActiveLevel := Sensor1.LevelRaw + Sensor1.CalibrationOffset;
ELSIF NOT Sensor2.SensorFault THEN
    ActiveLevel := Sensor2.LevelRaw + Sensor2.CalibrationOffset;
ELSE
    ActiveLevel := 0.0;
    TundishLevelAlarm := TRUE;
END_IF;

(* Level PID Loop *)
IF EnableCasting AND NOT TundishLevelAlarm THEN
    LevelError := TundishLevelTarget - ActiveLevel;
    
    (* Anti-windup Integral *)
    IF (SlideGatePositionCmd < 100.0 AND LevelError > 0.0) OR 
       (SlideGatePositionCmd > 0.0 AND LevelError < 0.0) THEN
        LevelIntegral := LevelIntegral + (LevelError * TimeStep);
    END_IF;
    
    LevelDerivative := (LevelError - LevelErrorPrev) / TimeStep;
    
    SlideGatePositionCmd := (Kp_Level * LevelError) + 
                            (Ki_Level * LevelIntegral) + 
                            (Kd_Level * LevelDerivative);
                            
    (* Limit output to 0-100% *)
    IF SlideGatePositionCmd > 100.0 THEN SlideGatePositionCmd := 100.0; END_IF;
    IF SlideGatePositionCmd < 0.0 THEN SlideGatePositionCmd := 0.0; END_IF;
    
    LevelErrorPrev := LevelError;
ELSE
    SlideGatePositionCmd := 0.0;
    LevelIntegral := 0.0;
END_IF;

(* -----------------------------------------------------------------------------
   3. COPPER MOLD OSCILLATION FREQUENCY MATRICES
----------------------------------------------------------------------------- *)
(* 
   Calculates required oscillation frequency (Hz) and stroke (mm) 
   to maintain Negative Strip Time (NST) for the given casting speed.
*)
IF EnableCasting AND ActualCastingSpeed > 0.1 THEN
    V_cast_sec := (ActualCastingSpeed * 1000.0) / 60.0; 
    
    (* Non-sinusoidal oscillation stroke determination based on casting speed *)
    IF ActualCastingSpeed <= 1.0 THEN
        OscillatorDrive.StrokeLengthCmd := 6.0;
    ELSIF ActualCastingSpeed <= 2.0 THEN
        OscillatorDrive.StrokeLengthCmd := 4.5;
    ELSE
        OscillatorDrive.StrokeLengthCmd := 3.0;
    END_IF;
    
    (* 
       Calculate Frequency to maintain Negative Strip Time Target.
       Matrix approximation heuristic:
    *)
    OscillatorDrive.FrequencyCmd := (V_cast_sec * LeadFactor) / (OscillatorDrive.StrokeLengthCmd * 2.0);
    
    (* Bounding limits for hydraulic oscillator *)
    IF OscillatorDrive.FrequencyCmd > 6.0 THEN OscillatorDrive.FrequencyCmd := 6.0; END_IF;
    IF OscillatorDrive.FrequencyCmd < 1.0 THEN OscillatorDrive.FrequencyCmd := 1.0; END_IF;
    
    OscillatorDrive.DriveEnable := TRUE;
ELSE
    OscillatorDrive.DriveEnable := FALSE;
    OscillatorDrive.FrequencyCmd := 0.0;
    OscillatorDrive.StrokeLengthCmd := 0.0;
END_IF;

(* -----------------------------------------------------------------------------
   4. SECONDARY COOLING ZONE WATER SPRAY TRACKING 
----------------------------------------------------------------------------- *)
IF EnableCasting THEN
    (* Speed Multiplier based on nominal 1.0 m/min *)
    CoolingSpeedMultiplier := ActualCastingSpeed / 1.0;
    
    FOR i := 1 TO 7 DO
        SecondaryCoolingZones[i].ZoneID := i;
        
        (* Calculate dynamic water flow based on grade base matrix and actual speed *)
        SecondaryCoolingZones[i].WaterFlowCmd := CoolingCurves[GradeIndex, i] * CoolingSpeedMultiplier;
        
        (* Estimate Solidification Fraction based on Stefan's law approximation 
           D = K * sqrt(t) 
        *)
        DistanceTravelled := INT_TO_REAL(i) * 1.5; (* Assume 1.5m length per zone *)
        SolidificationTime := DistanceTravelled / ActualCastingSpeed; (* min *)
        
        (* Heuristic fraction assignment based on cooling curve *)
        SecondaryCoolingZones[i].SolidificationFrac := SQRT(SolidificationTime) * 0.15 * (1530.0/LiquidusTemp);
        
        IF SecondaryCoolingZones[i].SolidificationFrac >= 1.0 THEN
            SecondaryCoolingZones[i].SolidificationFrac := 1.0;
            (* Reduce water if fully solidified to save energy and prevent cracking *)
            SecondaryCoolingZones[i].WaterFlowCmd := SecondaryCoolingZones[i].WaterFlowCmd * 0.3;
        END_IF;
        
        (* Set Air Flow proportional to Water Flow for mist cooling nozzles *)
        SecondaryCoolingZones[i].AirFlowCmd := SecondaryCoolingZones[i].WaterFlowCmd * 2.5;
    END_FOR;
ELSE
    FOR i := 1 TO 7 DO
        SecondaryCoolingZones[i].WaterFlowCmd := 0.0;
        SecondaryCoolingZones[i].AirFlowCmd := 0.0;
    END_FOR;
END_IF;

(* -----------------------------------------------------------------------------
   5. BREAKOUT WARNING SYSTEM
----------------------------------------------------------------------------- *)
(* Detect anomalous heat transfer in the mold indicative of shell sticking *)
DeltaT := MoldWaterTempOut - MoldWaterTempIn;
HeatFlux := DeltaT * ActualCastingSpeed * 5.0; (* Pseudo heat flux metric *)

IF HeatFlux > 150.0 AND ActualCastingSpeed > 0.5 THEN
    BreakoutWarning := TRUE;
ELSE
    BreakoutWarning := FALSE;
END_IF;

SystemReady := NOT TundishLevelAlarm AND NOT BreakoutWarning AND OscillatorDrive.DriveEnable;

END_FUNCTION_BLOCK
```"""

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": assistant}
    ]
}

with open("data/synthetic_generation_v3_enterprise.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\\n")
