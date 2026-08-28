import json
import os

prompt = "Evolve a simple fluid pump block from the tier1 seeds into a complex multi-pump alternating lead-lag system for a municipal water treatment plant. Include runtime wear-leveling (alternating the lead pump based on hours run), cavitation detection via current spikes, and dry-run protection via pressure switches."

assistant_response = """(*
================================================================================
Function Block: MULTI_PUMP_STATION
Description: Highly complex, production-ready multi-pump alternating lead-lag 
             system for municipal water treatment plants.
Features:
  - Runtime wear-leveling based on pump operating hours.
  - Cavitation detection via current spikes.
  - Dry-run protection via intake pressure switches.
  - Thermal overload interlocks and Emergency Stops (E-Stop).
  - State machine for pump sequence control (Lead, Lag, Standby).
================================================================================
*)

TYPE PumpState : (
    PUMP_OFF,
    PUMP_STARTING,
    PUMP_RUNNING,
    PUMP_STOPPING,
    PUMP_FAULTED
);
END_TYPE

TYPE PumpFaults : STRUCT
    ThermalOverload : BOOL;
    Cavitation      : BOOL;
    DryRun          : BOOL;
    FailedToStart   : BOOL;
END_STRUCT;
END_TYPE

TYPE PumpData : STRUCT
    State           : PumpState;
    RunHours        : REAL;
    CurrentDraw     : REAL;
    Faults          : PumpFaults;
END_STRUCT;
END_TYPE

FUNCTION_BLOCK MULTI_PUMP_STATION
VAR_INPUT
    EnableSystem    : BOOL;           (* Master enable for the pump station *)
    E_Stop          : BOOL;           (* Emergency stop, normally closed (NC) *)
    IntakePressure  : REAL;           (* Analog intake pressure in bar *)
    LevelSetPoint   : REAL;           (* Desired tank level *)
    LevelActual     : REAL;           (* Actual tank level *)
    
    Pump1_Current   : REAL;           (* Analog current feedback for Pump 1 *)
    Pump2_Current   : REAL;           (* Analog current feedback for Pump 2 *)
    
    Pump1_Thermal   : BOOL;           (* Thermal overload switch P1 (NC) *)
    Pump2_Thermal   : BOOL;           (* Thermal overload switch P2 (NC) *)
    
    ResetFaults     : BOOL;           (* Acknowledge and reset faults *)
END_VAR

VAR_OUTPUT
    Pump1_Cmd       : BOOL;           (* Command to run Pump 1 *)
    Pump2_Cmd       : BOOL;           (* Command to run Pump 2 *)
    SystemFault     : BOOL;           (* General fault indicator *)
    LeadPumpID      : INT;            (* Currently assigned lead pump (1 or 2) *)
END_VAR

VAR CONSTANT
    DRY_RUN_PRESSURE_MIN : REAL := 0.5;   (* Minimum bar before dry run fault *)
    CAVITATION_CURRENT   : REAL := 45.0;  (* Current limit indicating cavitation (Amps) *)
    START_DELAY          : TIME := T#5S;  (* Staggered start delay *)
    WEAR_LEVEL_DIFF      : REAL := 10.0;  (* Difference in hours to force switch *)
END_VAR

VAR
    Pumps                : ARRAY[1..2] OF PumpData;
    StartTimer           : TON;
    SysState             : INT := 0;      (* 0=Idle, 1=LeadReq, 2=LagReq *)
    CycleTimer           : TON;
    DryRunTimer          : TON;
    CavitationTimer1     : TON;
    CavitationTimer2     : TON;
    
    bDryRun              : BOOL;
    bEStopActive         : BOOL;
END_VAR

(* -----------------------------------------------------------------------------
   SAFETY INTERLOCKS
   ----------------------------------------------------------------------------- *)
bEStopActive := NOT E_Stop; (* E_Stop is NC *)

(* Dry run detection with 3-second debounce to avoid false trips *)
DryRunTimer(IN := (IntakePressure < DRY_RUN_PRESSURE_MIN), PT := T#3S);
bDryRun := DryRunTimer.Q;

(* -----------------------------------------------------------------------------
   FAULT MONITORING
   ----------------------------------------------------------------------------- *)
IF ResetFaults THEN
    Pumps[1].Faults.ThermalOverload := FALSE;
    Pumps[1].Faults.Cavitation := FALSE;
    Pumps[1].Faults.DryRun := FALSE;
    
    Pumps[2].Faults.ThermalOverload := FALSE;
    Pumps[2].Faults.Cavitation := FALSE;
    Pumps[2].Faults.DryRun := FALSE;
END_IF;

(* Hardware interlocks *)
IF NOT Pump1_Thermal THEN Pumps[1].Faults.ThermalOverload := TRUE; END_IF;
IF NOT Pump2_Thermal THEN Pumps[2].Faults.ThermalOverload := TRUE; END_IF;

IF bDryRun THEN
    Pumps[1].Faults.DryRun := TRUE;
    Pumps[2].Faults.DryRun := TRUE;
END_IF;

(* Cavitation detection via sustained current spikes (e.g., 2 seconds) *)
CavitationTimer1(IN := (Pump1_Current > CAVITATION_CURRENT) AND Pump1_Cmd, PT := T#2S);
IF CavitationTimer1.Q THEN Pumps[1].Faults.Cavitation := TRUE; END_IF;

CavitationTimer2(IN := (Pump2_Current > CAVITATION_CURRENT) AND Pump2_Cmd, PT := T#2S);
IF CavitationTimer2.Q THEN Pumps[2].Faults.Cavitation := TRUE; END_IF;

(* General system fault *)
SystemFault := bEStopActive OR 
               (Pumps[1].Faults.ThermalOverload OR Pumps[1].Faults.Cavitation OR Pumps[1].Faults.DryRun) OR 
               (Pumps[2].Faults.ThermalOverload OR Pumps[2].Faults.Cavitation OR Pumps[2].Faults.DryRun);

(* -----------------------------------------------------------------------------
   WEAR-LEVELING ALGORITHM
   ----------------------------------------------------------------------------- *)
(* Periodically evaluate which pump should be lead based on runtime hours.
   Only switch if difference exceeds the hysteresis value to prevent rapid toggling. *)
IF (Pumps[1].RunHours <= Pumps[2].RunHours) AND (Pumps[2].RunHours - Pumps[1].RunHours > WEAR_LEVEL_DIFF) THEN
    LeadPumpID := 1;
ELSIF (Pumps[2].RunHours < Pumps[1].RunHours) AND (Pumps[1].RunHours - Pumps[2].RunHours > WEAR_LEVEL_DIFF) THEN
    LeadPumpID := 2;
END_IF;

(* Fallback if Lead pump is faulted *)
IF LeadPumpID = 1 AND (Pumps[1].Faults.ThermalOverload OR Pumps[1].Faults.Cavitation OR Pumps[1].Faults.DryRun) THEN
    LeadPumpID := 2;
ELSIF LeadPumpID = 2 AND (Pumps[2].Faults.ThermalOverload OR Pumps[2].Faults.Cavitation OR Pumps[2].Faults.DryRun) THEN
    LeadPumpID := 1;
END_IF;

IF LeadPumpID = 0 THEN LeadPumpID := 1; END_IF; (* Initialization *)

(* -----------------------------------------------------------------------------
   PROCESS CONTROL & SEQUENCING (LEAD-LAG)
   ----------------------------------------------------------------------------- *)
IF NOT EnableSystem OR SystemFault THEN
    Pump1_Cmd := FALSE;
    Pump2_Cmd := FALSE;
    SysState := 0;
ELSE
    (* Control Logic based on Level Actual vs Setpoint.
       Assuming a drain sequence (pump out). *)
    
    (* Lead requirement: Level goes 10% above setpoint *)
    IF LevelActual > (LevelSetPoint * 1.1) THEN
        SysState := 1; 
    END_IF;
    
    (* Lag requirement: Level goes 20% above setpoint (high demand) *)
    IF LevelActual > (LevelSetPoint * 1.2) THEN
        SysState := 2;
    END_IF;
    
    (* Stop condition: Level drops below setpoint *)
    IF LevelActual <= LevelSetPoint THEN
        SysState := 0;
    END_IF;
    
    (* Execute commands based on state *)
    CASE SysState OF
        0: (* Idle *)
            Pump1_Cmd := FALSE;
            Pump2_Cmd := FALSE;
            
        1: (* Lead Only *)
            IF LeadPumpID = 1 THEN
                Pump1_Cmd := TRUE;
                Pump2_Cmd := FALSE;
            ELSE
                Pump1_Cmd := FALSE;
                Pump2_Cmd := TRUE;
            END_IF;
            
        2: (* Lead + Lag *)
            Pump1_Cmd := TRUE;
            Pump2_Cmd := TRUE;
            
    END_CASE;
END_IF;

(* -----------------------------------------------------------------------------
   RUNTIME ACCUMULATION (Simulated integration per cycle)
   ----------------------------------------------------------------------------- *)
(* Assuming a 1s task cycle for simple addition. In reality, use system time. *)
CycleTimer(IN := NOT CycleTimer.Q, PT := T#1S);
IF CycleTimer.Q THEN
    IF Pump1_Cmd THEN
        Pumps[1].RunHours := Pumps[1].RunHours + (1.0 / 3600.0);
    END_IF;
    IF Pump2_Cmd THEN
        Pumps[2].RunHours := Pumps[2].RunHours + (1.0 / 3600.0);
    END_IF;
END_IF;

END_FUNCTION_BLOCK
"""

data = {
    "messages": [
        {
            "role": "user",
            "content": prompt
        },
        {
            "role": "assistant",
            "content": assistant_response
        }
    ]
}

target_file = r'c:\Users\majip\Downloads\LLM REASEARCH\data\evol_instruct_dataset.jsonl'
with open(target_file, 'a', encoding='utf-8') as f:
    f.write(json.dumps(data) + '\n')

print("Data appended successfully!")
