import json

data = {
    "messages": [
        {
            "role": "user",
            "content": "You are acting as a Lead Civil Engineer for a Ski Resort. Evolve a basic motion block into an Automated Snowmaking Pump House and Hydrant Controller. Technical Specs: 1. Wet-bulb temperature calculation matrices for marginal freezing conditions. 2. High-pressure water and compressed air mixture ratio control for optimal snow crystal nucleation. 3. Pump station staging to prevent mountain-wide pressure drops. Format the response as a complete IEC 61131-3 Structured Text PLC program."
        },
        {
            "role": "assistant",
            "content": """(*
================================================================================
AUTOMATED SNOWMAKING PUMP HOUSE & HYDRANT CONTROLLER
STANDARD: IEC 61131-3
AUTHOR: Lead Civil & Controls Engineer
DESCRIPTION: 
Advanced control system for ski resort snowmaking. Features:
1. Wet-bulb temperature calculation for marginal freezing optimization.
2. Air/Water ratio control for crystal nucleation.
3. Pump staging logic to maintain mountain-wide pressure stability.
================================================================================
*)

TYPE
    E_PumpState : (PUMP_OFF, PUMP_STARTING, PUMP_RUNNING, PUMP_STOPPING, PUMP_FAULT);
    E_SnowQuality : (DRY_SNOW, MEDIUM_SNOW, WET_SNOW);
    
    ST_EnvData : STRUCT
        DryBulbTemp_C   : REAL; (* Dry bulb temperature in Celsius *)
        RelHumidity     : REAL; (* Relative humidity in % *)
        WindSpeed_mps   : REAL; (* Wind speed in m/s *)
        WetBulbTemp_C   : REAL; (* Calculated Wet-bulb temperature *)
    END_STRUCT;
    
    ST_HydrantData : STRUCT
        HydrantID       : INT;
        IsActive        : BOOL;
        WaterPressure_Bar: REAL;
        AirPressure_Bar  : REAL;
        WaterFlow_LPM    : REAL;
        AirFlow_CFM      : REAL;
        TargetRatio      : REAL;
        CurrentRatio     : REAL;
        ValvePosWater    : REAL; (* 0-100% *)
        ValvePosAir      : REAL; (* 0-100% *)
    END_STRUCT;
    
    ST_PumpData : STRUCT
        PumpID          : INT;
        State           : E_PumpState;
        RunTime_Hrs     : REAL;
        Capacity_LPM    : REAL;
    END_STRUCT;
END_TYPE

(*-----------------------------------------------------------------------------
 FUNCTION: CalculateWetBulb
 DESCRIPTION: Approximates Wet-Bulb temperature using Stull's empirical formula
-----------------------------------------------------------------------------*)
FUNCTION CalculateWetBulb : REAL
VAR_INPUT
    TempC : REAL; (* Dry Bulb Temperature in Celsius *)
    RH    : REAL; (* Relative Humidity 0-100% *)
END_VAR
VAR
    T, RH_val : REAL;
END_VAR

T := TempC;
RH_val := RH;

(* Stull's formula for wet-bulb temperature approximation *)
CalculateWetBulb := T * ATAN(0.151977 * EXPT(RH_val + 8.313659, 0.5)) 
                    + ATAN(T + RH_val) 
                    - ATAN(RH_val - 1.676331) 
                    + 0.00391838 * EXPT(RH_val, 1.5) * ATAN(0.023101 * RH_val) 
                    - 4.686035;
END_FUNCTION

(*-----------------------------------------------------------------------------
 FUNCTION_BLOCK: FB_MixtureControl
 DESCRIPTION: Controls the air/water ratio for optimal snow crystal nucleation
-----------------------------------------------------------------------------*)
FUNCTION_BLOCK FB_MixtureControl
VAR_INPUT
    Enable          : BOOL;
    WetBulbTemp     : REAL;
    TargetQuality   : E_SnowQuality;
    WaterPres_Bar   : REAL;
    AirPres_Bar     : REAL;
END_VAR
VAR_OUTPUT
    WaterValveCmd   : REAL; (* 0-100% *)
    AirValveCmd     : REAL; (* 0-100% *)
    ActualRatio     : REAL;
    NucleationReady : BOOL;
END_VAR
VAR
    IdealRatio      : REAL; (* Air to Water ratio *)
    PID_Water       : REAL; (* Simulated PID output *)
    PID_Air         : REAL; (* Simulated PID output *)
END_VAR

IF Enable THEN
    (* Determine ideal ratio based on wet-bulb temperature and target quality *)
    (* Colder wet-bulb allows higher water content (lower air ratio) *)
    IF WetBulbTemp < -10.0 THEN
        IdealRatio := 5.0; (* Very cold, less air needed *)
    ELSIF WetBulbTemp < -4.0 THEN
        IdealRatio := 15.0; (* Medium cold *)
    ELSIF WetBulbTemp <= -2.0 THEN
        IdealRatio := 35.0; (* Marginal freezing, need high air for cooling/nucleation *)
    ELSE
        IdealRatio := 0.0; (* Too warm to make snow *)
    END_IF;

    (* Adjust based on snow quality request *)
    CASE TargetQuality OF
        DRY_SNOW:  IdealRatio := IdealRatio * 1.5;
        WET_SNOW:  IdealRatio := IdealRatio * 0.8;
    END_CASE;

    IF IdealRatio > 0.0 AND WaterPres_Bar > 10.0 AND AirPres_Bar > 5.0 THEN
        (* Simplified control logic to reach ratio *)
        AirValveCmd := 100.0; (* Typically run air wide open and modulate water *)
        WaterValveCmd := 100.0 / IdealRatio; (* Simplified relationship *)
        ActualRatio := IdealRatio;
        NucleationReady := TRUE;
    ELSE
        AirValveCmd := 0.0;
        WaterValveCmd := 0.0;
        ActualRatio := 0.0;
        NucleationReady := FALSE;
    END_IF;
ELSE
    AirValveCmd := 0.0;
    WaterValveCmd := 0.0;
    ActualRatio := 0.0;
    NucleationReady := FALSE;
END_IF;
END_FUNCTION_BLOCK

(*-----------------------------------------------------------------------------
 FUNCTION_BLOCK: FB_PumpStaging
 DESCRIPTION: Manages pump staging to maintain mountain-wide pressure
-----------------------------------------------------------------------------*)
FUNCTION_BLOCK FB_PumpStaging
VAR_INPUT
    MountainPressure    : REAL; (* Current network pressure in Bar *)
    PressureSetpoint    : REAL; (* Target pressure in Bar *)
    TotalFlowDemand     : REAL; (* Total LPM requested by all hydrants *)
    EnableSystem        : BOOL;
END_VAR
VAR_IN_OUT
    Pumps               : ARRAY[1..5] OF ST_PumpData;
END_VAR
VAR_OUTPUT
    SystemReady         : BOOL;
    ActivePumpCount     : INT;
END_VAR
VAR
    i, j, NextPump      : INT;
    TotalCapacity       : REAL;
    MinRuntime          : REAL;
    PressureDeadband    : REAL := 2.5; (* Bar *)
    StagingDelay        : TIME := T#30s;
    TmrStaging          : TON;
    NeedMorePumps       : BOOL;
    NeedFewerPumps      : BOOL;
END_VAR

ActivePumpCount := 0;
TotalCapacity := 0.0;

FOR i := 1 TO 5 DO
    IF Pumps[i].State = PUMP_RUNNING THEN
        ActivePumpCount := ActivePumpCount + 1;
        TotalCapacity := TotalCapacity + Pumps[i].Capacity_LPM;
    END_IF;
END_FOR;

NeedMorePumps := (MountainPressure < (PressureSetpoint - PressureDeadband)) OR (TotalCapacity < TotalFlowDemand);
NeedFewerPumps := (MountainPressure > (PressureSetpoint + PressureDeadband)) AND (TotalCapacity > (TotalFlowDemand * 1.2));

TmrStaging(IN := (NeedMorePumps OR NeedFewerPumps) AND EnableSystem, PT := StagingDelay);

IF TmrStaging.Q THEN
    IF NeedMorePumps THEN
        (* Find available pump with least runtime *)
        MinRuntime := 999999.0;
        NextPump := 0;
        FOR i := 1 TO 5 DO
            IF Pumps[i].State = PUMP_OFF AND Pumps[i].RunTime_Hrs < MinRuntime THEN
                MinRuntime := Pumps[i].RunTime_Hrs;
                NextPump := i;
            END_IF;
        END_FOR;
        
        IF NextPump > 0 THEN
            Pumps[NextPump].State := PUMP_STARTING;
            Pumps[NextPump].State := PUMP_RUNNING; 
        END_IF;
        
    ELSIF NeedFewerPumps AND ActivePumpCount > 1 THEN
        (* Stop pump with most runtime *)
        MinRuntime := -1.0;
        NextPump := 0;
        FOR i := 1 TO 5 DO
            IF Pumps[i].State = PUMP_RUNNING AND Pumps[i].RunTime_Hrs > MinRuntime THEN
                MinRuntime := Pumps[i].RunTime_Hrs;
                NextPump := i;
            END_IF;
        END_FOR;
        
        IF NextPump > 0 THEN
            Pumps[NextPump].State := PUMP_STOPPING;
            Pumps[NextPump].State := PUMP_OFF;
        END_IF;
    END_IF;
    TmrStaging(IN := FALSE); (* Reset timer *)
END_IF;

SystemReady := MountainPressure >= (PressureSetpoint - PressureDeadband) AND EnableSystem;
END_FUNCTION_BLOCK

(*-----------------------------------------------------------------------------
 PROGRAM: PRG_MainSnowmakingControl
 DESCRIPTION: Master orchestrator for pump house and hydrants
-----------------------------------------------------------------------------*)
PROGRAM PRG_MainSnowmakingControl
VAR
    SystemEnabled       : BOOL := TRUE;
    GlobalEnv           : ST_EnvData;
    MainPressure        : REAL := 15.0; (* Simulated mountain pressure *)
    PressureTarget      : REAL := 25.0; (* 25 Bar target for snowmaking *)
    TotalDemand_LPM     : REAL;
    
    Pumps               : ARRAY[1..5] OF ST_PumpData;
    Hydrants            : ARRAY[1..50] OF ST_HydrantData;
    
    PumpStaging         : FB_PumpStaging;
    MixtureCtrls        : ARRAY[1..50] OF FB_MixtureControl;
    
    i                   : INT;
    SnowMakersActive    : INT;
    GlobalSnowQuality   : E_SnowQuality := MEDIUM_SNOW;
END_VAR

(* 1. Calculate Environmental Conditions *)
GlobalEnv.WetBulbTemp_C := CalculateWetBulb(TempC := GlobalEnv.DryBulbTemp_C, RH := GlobalEnv.RelHumidity);

(* 2. Process Hydrant Requests and Mix Control *)
TotalDemand_LPM := 0.0;
SnowMakersActive := 0;

FOR i := 1 TO 50 DO
    (* Marginal condition check - Only allow snowmaking if wet bulb is below -2.0C *)
    IF GlobalEnv.WetBulbTemp_C <= -2.0 AND SystemEnabled AND Hydrants[i].IsActive THEN
        
        MixtureCtrls[i](
            Enable          := TRUE,
            WetBulbTemp     := GlobalEnv.WetBulbTemp_C,
            TargetQuality   := GlobalSnowQuality,
            WaterPres_Bar   := Hydrants[i].WaterPressure_Bar,
            AirPres_Bar     := Hydrants[i].AirPressure_Bar,
            WaterValveCmd   => Hydrants[i].ValvePosWater,
            AirValveCmd     => Hydrants[i].ValvePosAir,
            ActualRatio     => Hydrants[i].CurrentRatio
        );
        
        IF MixtureCtrls[i].NucleationReady THEN
            TotalDemand_LPM := TotalDemand_LPM + 200.0; (* Nominal flow per hydrant *)
            SnowMakersActive := SnowMakersActive + 1;
        END_IF;
    ELSE
        Hydrants[i].ValvePosWater := 0.0;
        Hydrants[i].ValvePosAir := 0.0;
        MixtureCtrls[i](Enable := FALSE);
    END_IF;
END_FOR;

(* 3. Pump Station Staging to maintain pressure under demand *)
PumpStaging(
    MountainPressure    := MainPressure,
    PressureSetpoint    := PressureTarget,
    TotalFlowDemand     := TotalDemand_LPM,
    EnableSystem        := SystemEnabled,
    Pumps               := Pumps
);

(* Simulated Mountain Pressure Dynamics based on pump capacity vs demand *)
IF PumpStaging.ActivePumpCount > 0 THEN
    MainPressure := MainPressure + 0.5 * INT_TO_REAL(PumpStaging.ActivePumpCount) - (TotalDemand_LPM / 1000.0);
ELSE
    MainPressure := MainPressure - 0.1;
END_IF;

(* Limit pressure limits for safety *)
IF MainPressure > 35.0 THEN MainPressure := 35.0; END_IF;
IF MainPressure < 0.0 THEN MainPressure := 0.0; END_IF;

END_PROGRAM"""
        }
    ]
}

with open(r"C:\Users\majip\Downloads\LLM REASEARCH\data\synthetic_generation_v3_enterprise.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(data) + "\n")
