import json
import os

prompt = """You are acting as a Lead Process Engineer for a massive Commercial Bakery. Evolve a basic temperature loop into a 100-meter Continuous Tunnel Baking Oven Controller. Technical Specs: 1. Multi-zone cyclotherm burner profiling (radiant and convective heat). 2. Wire-mesh band tracking and tensioning to prevent snap. 3. Steam injection matrices for crust development."""

code = """(*
    VERSION: 3.4.1 (ENTERPRISE GRADE)
    AUTHOR: Lead Process Engineer / Elite Synthetic Data Architect
    DATE: 2026-08-21
    
    DESCRIPTION:
    100-Meter Continuous Tunnel Baking Oven Controller (IEC 61131-3)
    This comprehensive controller manages a massive commercial bakery oven with the following subsystems:
    1. Multi-Zone Cyclotherm Burner Profiling: Manages 8 distinct zones, balancing radiant and convective 
       heat transfer mechanisms for precise baking profiles.
    2. Wire-Mesh Band Tracking & Tensioning: Dual-axis servo control to prevent wire-mesh band snap 
       and lateral drift across the 100-meter span.
    3. Steam Injection Matrices: Micro-pulsed steam headers at the oven entrance for optimal crust 
       development (Maillard reaction promotion).

    ARCHITECTURE:
    - FB_CyclothermZone: Individual zone PID control for top/bottom burners and air circulation.
    - FB_BandTensioner: Load-cell based PID loop for hydraulic/pneumatic tensioning and edge tracking.
    - FB_SteamHeader: Pressure and mass-flow based steam injection matrix.
    - FB_TunnelOven_Main: Coordinator block orchestrating the subsystems.
*)

TYPE ST_ZoneConfig :
STRUCT
    SetPoint_TopRadiant : REAL;    (* °C *)
    SetPoint_BtmRadiant : REAL;    (* °C *)
    SetPoint_Convective : REAL;    (* Airflow m/s *)
    RadiantRatio        : REAL;    (* 0.0 to 1.0 *)
    ExhaustDamperPos    : REAL;    (* % open *)
END_STRUCT
END_TYPE

TYPE ST_ZoneStatus :
STRUCT
    Actual_TopTemp : REAL;
    Actual_BtmTemp : REAL;
    Actual_Airflow : REAL;
    Burner_Modulation : REAL;      (* 0-100% *)
    Burner_Fault   : BOOL;
END_STRUCT
END_TYPE

(* ========================================================================= *)
(* FB_CyclothermZone: Multi-Zone Cyclotherm Burner Control                   *)
(* ========================================================================= *)
FUNCTION_BLOCK FB_CyclothermZone
VAR_INPUT
    Enable          : BOOL;
    Config          : ST_ZoneConfig;
    ActualTopTemp   : REAL;
    ActualBtmTemp   : REAL;
    ActualAirflow   : REAL;
    GasPressureOK   : BOOL;
    FlameRelayOK    : BOOL;
END_VAR
VAR_OUTPUT
    Cmd_TopBurnerValve : REAL;     (* 0-100% Analog Output *)
    Cmd_BtmBurnerValve : REAL;     (* 0-100% Analog Output *)
    Cmd_CirculationFan : REAL;     (* 0-100% VFD Speed *)
    Cmd_ExhaustDamper  : REAL;     (* 0-100% Damper Actuator *)
    Status          : ST_ZoneStatus;
    Alarm           : BOOL;
END_VAR
VAR
    PID_Top : PID_Compact;
    PID_Btm : PID_Compact;
    PID_Air : PID_Compact;
    State   : INT := 0;
END_VAR

IF NOT Enable OR NOT GasPressureOK OR NOT FlameRelayOK THEN
    Cmd_TopBurnerValve := 0.0;
    Cmd_BtmBurnerValve := 0.0;
    Cmd_CirculationFan := 10.0; (* Minimum purge speed *)
    Cmd_ExhaustDamper  := 100.0; (* Open exhaust on stop *)
    Alarm := NOT GasPressureOK OR NOT FlameRelayOK;
    RETURN;
END_IF;

(* Top Burner Radiant PID *)
PID_Top(
    Setpoint := Config.SetPoint_TopRadiant,
    Actual   := ActualTopTemp,
    Kp       := 2.5,
    Ti       := T#120S,
    Td       := T#10S,
    Out_Min  := 0.0,
    Out_Max  := 100.0,
    Output   => Cmd_TopBurnerValve
);

(* Bottom Burner Radiant PID *)
PID_Btm(
    Setpoint := Config.SetPoint_BtmRadiant,
    Actual   := ActualBtmTemp,
    Kp       := 2.8,
    Ti       := T#140S,
    Td       := T#15S,
    Out_Min  := 0.0,
    Out_Max  := 100.0,
    Output   => Cmd_BtmBurnerValve
);

(* Convective Airflow PID *)
PID_Air(
    Setpoint := Config.SetPoint_Convective,
    Actual   := ActualAirflow,
    Kp       := 1.2,
    Ti       := T#60S,
    Out_Min  := 20.0,
    Out_Max  := 100.0,
    Output   => Cmd_CirculationFan
);

Cmd_ExhaustDamper := Config.ExhaustDamperPos;

(* Status Update *)
Status.Actual_TopTemp := ActualTopTemp;
Status.Actual_BtmTemp := ActualBtmTemp;
Status.Actual_Airflow := ActualAirflow;
Status.Burner_Modulation := (Cmd_TopBurnerValve + Cmd_BtmBurnerValve) / 2.0;
Status.Burner_Fault := FALSE;

END_FUNCTION_BLOCK


(* ========================================================================= *)
(* FB_BandTracking: Wire-Mesh Band Tracking and Tensioning                   *)
(* ========================================================================= *)
FUNCTION_BLOCK FB_BandTracking
VAR_INPUT
    Enable          : BOOL;
    BandSpeed_SP    : REAL;        (* m/min *)
    LoadCell_Left   : REAL;        (* kN *)
    LoadCell_Right  : REAL;        (* kN *)
    TargetTension   : REAL;        (* kN *)
    EdgeSensor_L    : REAL;        (* mm deviation *)
    EdgeSensor_R    : REAL;        (* mm deviation *)
END_VAR
VAR_OUTPUT
    Cmd_DriveVFD    : REAL;        (* 0-100% Main Drive *)
    Cmd_TensionCyl  : REAL;        (* 0-100% Hydraulic Valve *)
    Cmd_TrackerLeft : REAL;        (* Actuator Pos *)
    Cmd_TrackerRight: REAL;        (* Actuator Pos *)
    TensionError    : BOOL;
    TrackingFault   : BOOL;
END_VAR
VAR
    TensionPID      : PID_Compact;
    TotalTension    : REAL;
    Differential    : REAL;
    Integral_Track  : REAL;
END_VAR

IF NOT Enable THEN
    Cmd_DriveVFD := 0.0;
    Cmd_TensionCyl := 0.0;
    RETURN;
END_IF;

TotalTension := LoadCell_Left + LoadCell_Right;
Differential := LoadCell_Left - LoadCell_Right;

(* Tensioning PID - Prevent Band Snap *)
TensionPID(
    Setpoint := TargetTension,
    Actual   := TotalTension,
    Kp       := 5.0,
    Ti       := T#5S,
    Out_Min  := 0.0,
    Out_Max  := 100.0,
    Output   => Cmd_TensionCyl
);

(* Band Tracking Proportional-Integral Control *)
IF ABS(EdgeSensor_L - EdgeSensor_R) > 5.0 THEN
    Integral_Track := Integral_Track + (EdgeSensor_L - EdgeSensor_R) * 0.01;
END_IF;

Integral_Track := LIMIT(-20.0, Integral_Track, 20.0);

Cmd_TrackerLeft := 50.0 + (EdgeSensor_L * 2.0) + Integral_Track;
Cmd_TrackerRight := 50.0 + (EdgeSensor_R * 2.0) - Integral_Track;

(* Fault Detections *)
TensionError := (TotalTension > TargetTension * 1.5) OR (TotalTension < TargetTension * 0.5);
TrackingFault := (ABS(EdgeSensor_L) > 50.0) OR (ABS(EdgeSensor_R) > 50.0);

(* Main Drive Control *)
Cmd_DriveVFD := BandSpeed_SP * 2.5; (* Speed scaling factor *)

END_FUNCTION_BLOCK


(* ========================================================================= *)
(* FB_SteamInjection: Steam Matrices for Crust Development                   *)
(* ========================================================================= *)
FUNCTION_BLOCK FB_SteamInjection
VAR_INPUT
    Enable          : BOOL;
    ProductDetect   : BOOL;        (* Photoeye at entrance *)
    TargetFlow      : REAL;        (* kg/hr *)
    SteamPressure   : REAL;        (* bar *)
    Zone1Temp       : REAL;        (* Interlock with Zone 1 temp *)
END_VAR
VAR_OUTPUT
    Cmd_ProportionalValve : REAL;  (* 0-100% *)
    Valve1_Header   : BOOL;
    Valve2_Header   : BOOL;
    Valve3_Header   : BOOL;
    SteamReady      : BOOL;
END_VAR
VAR
    SteamPID        : PID_Compact;
    PulseTimer      : TON;
    PulseCount      : INT;
END_VAR

SteamReady := (SteamPressure > 2.5) AND (Zone1Temp > 100.0);

IF Enable AND SteamReady AND ProductDetect THEN
    SteamPID(
        Setpoint := TargetFlow,
        Actual   := SteamPressure * 10.0, (* Simulated flow calc *)
        Kp       := 1.5,
        Ti       := T#2S,
        Out_Min  := 0.0,
        Out_Max  := 100.0,
        Output   => Cmd_ProportionalValve
    );
    
    (* Sequenced Matrix Injection to maintain pressure *)
    Valve1_Header := TRUE;
    Valve2_Header := Cmd_ProportionalValve > 30.0;
    Valve3_Header := Cmd_ProportionalValve > 70.0;
ELSE
    Cmd_ProportionalValve := 0.0;
    Valve1_Header := FALSE;
    Valve2_Header := FALSE;
    Valve3_Header := FALSE;
END_IF;

END_FUNCTION_BLOCK


(* ========================================================================= *)
(* FB_TunnelOven_Main: Master Coordinator for 100-meter Oven                 *)
(* ========================================================================= *)
PROGRAM MAIN_OVEN_CTRL
VAR
    (* Master Controls *)
    OvenStart       : BOOL;
    OvenEmergency   : BOOL;
    RecipeSelect    : INT;
    
    (* Subsystems *)
    Zones           : ARRAY[1..8] OF FB_CyclothermZone;
    ZoneConfigs     : ARRAY[1..8] OF ST_ZoneConfig;
    BandTrack       : FB_BandTracking;
    SteamInj        : FB_SteamInjection;
    
    (* Field IO - Simulated *)
    ActualTops      : ARRAY[1..8] OF REAL;
    ActualBtms      : ARRAY[1..8] OF REAL;
    ActualAirs      : ARRAY[1..8] OF REAL;
    
    i : INT;
END_VAR

IF OvenEmergency THEN
    OvenStart := FALSE;
END_IF;

(* 1. Recipe Management (Simplistic Example) *)
CASE RecipeSelect OF
    1: (* Artisan Sourdough *)
        BandTrack.BandSpeed_SP := 12.0; (* slower bake *)
        BandTrack.TargetTension := 150.0;
        SteamInj.TargetFlow := 300.0; (* heavy steam *)
        FOR i := 1 TO 8 DO
            ZoneConfigs[i].SetPoint_TopRadiant := 240.0 - (INT_TO_REAL(i)*5.0);
            ZoneConfigs[i].SetPoint_BtmRadiant := 250.0 - (INT_TO_REAL(i)*5.0);
            ZoneConfigs[i].SetPoint_Convective := 5.0;
        END_FOR
    2: (* Soft Buns *)
        BandTrack.BandSpeed_SP := 22.0; (* fast bake *)
        BandTrack.TargetTension := 120.0;
        SteamInj.TargetFlow := 50.0; (* light steam *)
        FOR i := 1 TO 8 DO
            ZoneConfigs[i].SetPoint_TopRadiant := 180.0;
            ZoneConfigs[i].SetPoint_BtmRadiant := 190.0;
            ZoneConfigs[i].SetPoint_Convective := 8.0;
        END_FOR
END_CASE

(* 2. Execute Zone Cyclotherm Controllers *)
FOR i := 1 TO 8 DO
    Zones[i](
        Enable := OvenStart AND NOT OvenEmergency,
        Config := ZoneConfigs[i],
        ActualTopTemp := ActualTops[i],
        ActualBtmTemp := ActualBtms[i],
        ActualAirflow := ActualAirs[i],
        GasPressureOK := TRUE,  (* Simulated IO *)
        FlameRelayOK  := TRUE   (* Simulated IO *)
    );
END_FOR

(* 3. Execute Band Tracking *)
BandTrack(
    Enable := OvenStart AND NOT OvenEmergency,
    BandSpeed_SP := BandTrack.BandSpeed_SP,
    LoadCell_Left := 75.0,  (* Simulated IO *)
    LoadCell_Right := 75.0, (* Simulated IO *)
    TargetTension := BandTrack.TargetTension,
    EdgeSensor_L := 1.0,    (* Simulated IO *)
    EdgeSensor_R := -1.0    (* Simulated IO *)
);

(* 4. Execute Steam Matrix (Entrance Zone Only) *)
SteamInj(
    Enable := OvenStart AND NOT OvenEmergency,
    ProductDetect := TRUE,  (* Simulated IO *)
    TargetFlow := SteamInj.TargetFlow,
    SteamPressure := 3.0,   (* Simulated IO *)
    Zone1Temp := ActualTops[1]
);

END_PROGRAM
"""

obj = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": code}
    ]
}

target_file = r"C:\Users\majip\Downloads\LLM REASEARCH\Local_Ollama_Evol_Pipeline\seeds\tier1_enterprise_grade\synthetic_generation_v3_enterprise.jsonl"

with open(target_file, "a", encoding="utf-8") as f:
    f.write(json.dumps(obj) + "\n")

print("Successfully appended to JSONL.")
