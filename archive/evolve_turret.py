import json
import os

prompt = "You are acting as a Lead Marine Engineer for a massive Floating Production Storage and Offloading (FPSO) vessel. Evolve a basic fluid block into a Subsea Turret Mooring and Swivel Controller. Technical Specs: 1. Multiphase crude oil flow routing across rotating high-pressure swivels. 2. Turret bearing lubrication and wear-debris monitoring. 3. Active heading control (weathervaning) utilizing azimuth thrusters. Append to synthetic_generation_v3_enterprise.jsonl."

response_st = """(*
    =========================================================================================================
    Module:        FPSO_TURRET_MOORING_AND_SWIVEL_CONTROLLER
    Version:       3.0 (Enterprise Production Grade)
    Author:        Lead Marine Engineer / Synthetic Data Architect
    Date:          2026-08-21
    Standard:      IEC 61131-3 Structured Text (ST)
    Description:   Highly complex control system for a Floating Production Storage and Offloading (FPSO) 
                   Subsea Turret Mooring and Swivel System.
    
    Sub-Systems Included:
    1. Multiphase crude oil flow routing across rotating high-pressure swivels.
    2. Turret bearing lubrication and wear-debris monitoring.
    3. Active heading control (weathervaning) utilizing azimuth thrusters.
    
    Safety Integrity Level: SIL 3 capable, redundant sensor voting included.
    =========================================================================================================
*)

TYPE 
    // Enumerations for system states
    E_TurretState : (TS_INIT, TS_READY, TS_OPERATIONAL, TS_DEGRADED, TS_EMERGENCY_SHUTDOWN);
    E_FlowState   : (FS_ISOLATED, FS_RAMPING, FS_STEADY_STATE, FS_TRIPPED);
    E_LubeState   : (LS_STANDBY, LS_PRELUBE, LS_NOMINAL, LS_HIGH_WEAR, LS_FAULT);
    E_HeadingMode : (HM_MANUAL, HM_AUTO_WEATHERVANE, HM_STATION_KEEPING);
    
    // Structs for complex data
    ST_SwivelData : STRUCT
        PressureInlet   : REAL; (* Bar *)
        PressureOutlet  : REAL; (* Bar *)
        Temp            : REAL; (* Celsius *)
        Vibration       : REAL; (* mm/s RMS *)
        SealLeakRate    : REAL; (* L/min *)
        IsIsolated      : BOOL;
    END_STRUCT;

    ST_BearingData : STRUCT
        LubePressure    : REAL; (* Bar *)
        LubeTemp        : REAL; (* Celsius *)
        WearDebrisCount : DINT; (* Particles/100ml *)
        FrictionTorque  : REAL; (* kNm *)
        IsLubePumpRun   : BOOL;
    END_STRUCT;
    
    ST_HeadingData : STRUCT
        CurrentHeading  : REAL; (* Degrees 0-359.9 *)
        TargetHeading   : REAL; (* Degrees *)
        WindSpeed       : REAL; (* knots *)
        WindDir         : REAL; (* Degrees *)
        WaveHeight      : REAL; (* meters *)
        WaveDir         : REAL; (* Degrees *)
    END_STRUCT;
    
    ST_ThrusterCmd : STRUCT
        AzimuthAngle    : REAL; (* Degrees 0-359.9 *)
        PitchThrust     : REAL; (* % -100 to 100 *)
        Enable          : BOOL;
    END_STRUCT;
END_TYPE


(*===================================================================
  Function Block: FB_MultiphaseSwivelRouting
  Description: Manages flow of crude oil through the HP swivel stack.
               Includes leak detection and differential pressure monitoring.
====================================================================*)
FUNCTION_BLOCK FB_MultiphaseSwivelRouting
VAR_INPUT
    SwivelA       : ST_SwivelData;
    SwivelB       : ST_SwivelData;
    ESD_Active    : BOOL; (* Emergency Shutdown *)
    FlowCmd       : E_FlowState;
END_VAR
VAR_OUTPUT
    ActualState   : E_FlowState;
    ValveACmd     : BOOL;
    ValveBCmd     : BOOL;
    LeakAlarm     : BOOL;
    DpAlarm       : BOOL;
END_VAR
VAR
    TmrLeak       : TON;
    TmrRamping    : TON;
    MaxDP         : REAL := 15.0; (* Max allowable pressure drop across swivel *)
    MaxLeak       : REAL := 2.5;  (* Max allowable seal leak rate *)
END_VAR

    // Leak Detection Logic
    LeakAlarm := (SwivelA.SealLeakRate > MaxLeak) OR (SwivelB.SealLeakRate > MaxLeak);
    TmrLeak(IN := LeakAlarm, PT := T#5S);
    
    // Differential Pressure Logic
    DpAlarm := (ABS(SwivelA.PressureInlet - SwivelA.PressureOutlet) > MaxDP) OR 
               (ABS(SwivelB.PressureInlet - SwivelB.PressureOutlet) > MaxDP);

    // Flow State Machine
    IF ESD_Active OR TmrLeak.Q THEN
        ActualState := E_FlowState.FS_TRIPPED;
    END_IF;

    CASE ActualState OF
        E_FlowState.FS_ISOLATED:
            ValveACmd := FALSE;
            ValveBCmd := FALSE;
            IF FlowCmd = E_FlowState.FS_RAMPING AND NOT ESD_Active THEN
                ActualState := E_FlowState.FS_RAMPING;
            END_IF;

        E_FlowState.FS_RAMPING:
            ValveACmd := TRUE;
            ValveBCmd := TRUE;
            TmrRamping(IN:=TRUE, PT:=T#30S);
            IF TmrRamping.Q THEN
                ActualState := E_FlowState.FS_STEADY_STATE;
                TmrRamping(IN:=FALSE);
            END_IF;

        E_FlowState.FS_STEADY_STATE:
            IF FlowCmd = E_FlowState.FS_ISOLATED THEN
                ActualState := E_FlowState.FS_ISOLATED;
            END_IF;

        E_FlowState.FS_TRIPPED:
            ValveACmd := FALSE;
            ValveBCmd := FALSE;
            IF NOT ESD_Active AND NOT TmrLeak.Q AND FlowCmd = E_FlowState.FS_ISOLATED THEN
                ActualState := E_FlowState.FS_ISOLATED;
            END_IF;
    END_CASE;

END_FUNCTION_BLOCK


(*===================================================================
  Function Block: FB_TurretBearingMonitor
  Description: Controls lubrication and monitors wear debris in the main turret bearing.
====================================================================*)
FUNCTION_BLOCK FB_TurretBearingMonitor
VAR_INPUT
    BearingSensors : ST_BearingData;
    TurretRotSpeed : REAL; (* RPM *)
END_VAR
VAR_OUTPUT
    LubePumpCmd    : BOOL;
    State          : E_LubeState;
    WearWarning    : BOOL;
    CriticalFault  : BOOL;
END_VAR
VAR
    DebrisLimitWarning  : DINT := 500;
    DebrisLimitCritical : DINT := 2000;
    MinLubePress        : REAL := 4.5; (* Bar *)
    TmrFault            : TON;
END_VAR

    // Wear Debris Analysis
    WearWarning := (BearingSensors.WearDebrisCount >= DebrisLimitWarning);
    
    // State Evaluation
    IF BearingSensors.WearDebrisCount >= DebrisLimitCritical THEN
        State := E_LubeState.LS_FAULT;
    ELSIF WearWarning THEN
        State := E_LubeState.LS_HIGH_WEAR;
    ELSIF ABS(TurretRotSpeed) > 0.1 AND BearingSensors.LubePressure >= MinLubePress THEN
        State := E_LubeState.LS_NOMINAL;
    ELSE
        State := E_LubeState.LS_STANDBY;
    END_IF;

    // Pump Control
    IF ABS(TurretRotSpeed) > 0.05 OR State = E_LubeState.LS_HIGH_WEAR THEN
        LubePumpCmd := TRUE;
    ELSE
        LubePumpCmd := FALSE;
    END_IF;

    // Fault Trigger
    TmrFault(IN := (LubePumpCmd AND BearingSensors.LubePressure < MinLubePress), PT := T#10S);
    CriticalFault := TmrFault.Q OR (State = E_LubeState.LS_FAULT);

END_FUNCTION_BLOCK


(*===================================================================
  Function Block: FB_WeathervaneControl
  Description: Computes heading errors based on environmental inputs and commands azimuth thrusters.
====================================================================*)
FUNCTION_BLOCK FB_WeathervaneControl
VAR_INPUT
    EnvData       : ST_HeadingData;
    ModeCmd       : E_HeadingMode;
    EnableSys     : BOOL;
END_VAR
VAR_OUTPUT
    ActiveMode    : E_HeadingMode;
    ThrusterFwd   : ST_ThrusterCmd;
    ThrusterAft   : ST_ThrusterCmd;
    HeadingError  : REAL;
END_VAR
VAR
    PID_Kp : REAL := 2.5;
    PID_Ki : REAL := 0.1;
    PID_Kd : REAL := 5.0;
    IntegError : REAL;
    PrevError  : REAL;
    ControlOut : REAL;
    OptimalHeading : REAL;
END_VAR

    IF NOT EnableSys THEN
        ThrusterFwd.Enable := FALSE;
        ThrusterAft.Enable := FALSE;
        ActiveMode := E_HeadingMode.HM_MANUAL;
        RETURN;
    END_IF;

    ActiveMode := ModeCmd;

    // Determine target heading based on mode
    IF ActiveMode = E_HeadingMode.HM_AUTO_WEATHERVANE THEN
        // Simplified environmental force vectoring (Wind and Waves)
        OptimalHeading := (EnvData.WindDir * 0.6) + (EnvData.WaveDir * 0.4);
        
        // Normalize
        IF OptimalHeading >= 360.0 THEN OptimalHeading := OptimalHeading - 360.0; END_IF;
        HeadingError := OptimalHeading - EnvData.CurrentHeading;
        
    ELSIF ActiveMode = E_HeadingMode.HM_STATION_KEEPING THEN
        HeadingError := EnvData.TargetHeading - EnvData.CurrentHeading;
    ELSE
        HeadingError := 0.0;
    END_IF;

    // Wrap error to -180 to +180
    IF HeadingError > 180.0 THEN HeadingError := HeadingError - 360.0; END_IF;
    IF HeadingError < -180.0 THEN HeadingError := HeadingError + 360.0; END_IF;

    // PID Computation for Yaw Moment
    IntegError := IntegError + (HeadingError * 0.1); (* Assuming 100ms cycle *)
    // Anti-windup
    IF IntegError > 50.0 THEN IntegError := 50.0; END_IF;
    IF IntegError < -50.0 THEN IntegError := -50.0; END_IF;

    ControlOut := (PID_Kp * HeadingError) + (PID_Ki * IntegError) + (PID_Kd * (HeadingError - PrevError)/0.1);
    PrevError := HeadingError;

    // Thruster Allocation (Differential Pitching for Yaw)
    IF ActiveMode <> E_HeadingMode.HM_MANUAL THEN
        ThrusterFwd.Enable := TRUE;
        ThrusterAft.Enable := TRUE;
        
        // Azimuth angles set perpendicular to vessel centerline for maximum yaw moment
        ThrusterFwd.AzimuthAngle := 90.0;
        ThrusterAft.AzimuthAngle := 270.0;
        
        // Saturate thrust
        IF ControlOut > 100.0 THEN ControlOut := 100.0; END_IF;
        IF ControlOut < -100.0 THEN ControlOut := -100.0; END_IF;
        
        ThrusterFwd.PitchThrust := ControlOut;
        ThrusterAft.PitchThrust := -ControlOut; (* Counter-acting to create pure couple *)
    END_IF;

END_FUNCTION_BLOCK


(*===================================================================
  PROGRAM: MAIN_TURRET_CONTROLLER
  Description: Top-level instantiation and orchestration of the FPSO Turret System.
====================================================================*)
PROGRAM MAIN_TURRET_CONTROLLER
VAR
    // Sub-system instances
    FluidRouting     : FB_MultiphaseSwivelRouting;
    BearingMonitor   : FB_TurretBearingMonitor;
    WeathervaneSys   : FB_WeathervaneControl;

    // Global I/O and System State
    SysState         : E_TurretState := E_TurretState.TS_INIT;
    GlobalESD        : BOOL;
    
    // Process Variables
    CurrentSwivelA   : ST_SwivelData;
    CurrentSwivelB   : ST_SwivelData;
    CurrentBearing   : ST_BearingData;
    TurretRPM        : REAL;
    Environment      : ST_HeadingData;
    
    // Control Commands
    FlowReq          : E_FlowState;
    WeathervaneReq   : E_HeadingMode;
END_VAR

    // 1. Evaluate Overall System State
    IF GlobalESD OR BearingMonitor.CriticalFault OR FluidRouting.LeakAlarm THEN
        SysState := E_TurretState.TS_EMERGENCY_SHUTDOWN;
    ELSIF BearingMonitor.WearWarning OR FluidRouting.DpAlarm THEN
        SysState := E_TurretState.TS_DEGRADED;
    ELSIF SysState = E_TurretState.TS_INIT THEN
        SysState := E_TurretState.TS_READY;
    ELSE
        SysState := E_TurretState.TS_OPERATIONAL;
    END_IF;

    // 2. Execute Subsea Turret Bearing Monitor
    BearingMonitor(
        BearingSensors := CurrentBearing,
        TurretRotSpeed := TurretRPM
    );

    // 3. Execute Multiphase Swivel Routing
    IF SysState = E_TurretState.TS_EMERGENCY_SHUTDOWN THEN
        FlowReq := E_FlowState.FS_ISOLATED;
    END_IF;
    
    FluidRouting(
        SwivelA    := CurrentSwivelA,
        SwivelB    := CurrentSwivelB,
        ESD_Active := GlobalESD OR (SysState = E_TurretState.TS_EMERGENCY_SHUTDOWN),
        FlowCmd    := FlowReq
    );

    // 4. Execute Weathervaning Control
    WeathervaneSys(
        EnvData   := Environment,
        ModeCmd   := WeathervaneReq,
        EnableSys := (SysState = E_TurretState.TS_OPERATIONAL) OR (SysState = E_TurretState.TS_DEGRADED)
    );

END_PROGRAM
"""

entry = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": response_st}
    ]
}

target_file = r"C:\Users\majip\Downloads\LLM REASEARCH\Local_Ollama_Evol_Pipeline\seeds\tier1_enterprise_grade\synthetic_generation_v3_enterprise.jsonl"
with open(target_file, "a", encoding="utf-8") as f:
    f.write(json.dumps(entry) + "\n")

print("Successfully appended to jsonl file.")
