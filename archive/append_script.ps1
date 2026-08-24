$obj = @{
    messages = @(
        @{
            role = "user"
            content = "You are acting as a Naval Weapons Engineer on a Fast Attack Submarine. Evolve a basic fluid loop into a Torpedo Tube Flood and Equalize Sequencer. Technical Specs: 1. Sea-pressure equalization calculating depth-based hydrostatic pressure to safely flood the tube without compromising the hull. 2. Muzzle door and breech door mechanical interlocks. 3. Water ram impulse launch valve timing."
        },
        @{
            role = "assistant"
            content = "(*
================================================================================
Module: TT_FES_688 (Torpedo Tube Flood and Equalize Sequencer)
Class: SSN Fast Attack Submarine
================================================================================
Description:
  Advanced Torpedo Tube Flood, Equalize, and Launch Sequencer.
  Replaces basic flow control logic with a mission-critical submarine weapons 
  system controller.
  
  Key Capabilities:
  1. Hydrostatic Pressure Equalization: Dynamically calculates ambient sea 
     pressure based on ship's depth (P = rho * g * h) and regulates equalization 
     valves to match internal tube pressure prior to muzzle door operation.
  2. Subsafe Interlocks: Implements rigorous logical interlocks enforcing 
     mutually exclusive breech and muzzle door states to prevent catastrophic 
     flooding (loss of ship).
  3. Water Ram Launch Timing: Precision control of the impulse valve for 
     ejecting the weapon using a high-pressure water ram, optimizing acoustic 
     signature and ejection velocity.
================================================================================
*)
FUNCTION_BLOCK TT_FES_688
VAR_INPUT
    (* Commands *)
    Cmd_Flood           : BOOL;
    Cmd_Equalize        : BOOL;
    Cmd_Open_Muzzle     : BOOL;
    Cmd_Launch          : BOOL;
    Cmd_Drain           : BOOL;
    Cmd_Emergency_Stop  : BOOL;
    
    (* Telemetry *)
    Submarine_Depth_m   : REAL;  (* Current keel depth in meters *)
    Tube_Pressure_Bar   : REAL;  (* Current internal tube pressure in bar *)
    
    (* Interlock Sensors *)
    Breech_Door_Closed  : BOOL;
    Breech_Door_Locked  : BOOL;
    Muzzle_Door_Closed  : BOOL;
    Muzzle_Door_Locked  : BOOL;
    
    Weapon_Loaded       : BOOL;
END_VAR

VAR_OUTPUT
    (* Valve Controls *)
    Flood_Valve_Cmd      : BOOL;
    Equalize_Valve_Cmd   : BOOL;
    Drain_Valve_Cmd      : BOOL;
    Impulse_Valve_Cmd    : BOOL;
    
    (* Door Controls *)
    Muzzle_Door_Open_Cmd : BOOL;
    
    (* Status *)
    State                : INT;
    Ready_To_Fire        : BOOL;
    Target_Sea_Pressure  : REAL;
    Fault_Code           : INT;
END_VAR

VAR CONSTANT
    (* States *)
    ST_IDLE              : INT := 0;
    ST_FLOODING          : INT := 10;
    ST_EQUALIZING        : INT := 20;
    ST_EQUALIZED         : INT := 30;
    ST_MUZZLE_OPENING    : INT := 40;
    ST_READY_TO_FIRE     : INT := 50;
    ST_FIRING            : INT := 60;
    ST_DRAINING          : INT := 70;
    ST_FAULT             : INT := 99;
    
    (* Physics Constants *)
    RHO_SEAWATER         : REAL := 1025.0;  (* Density kg/m^3 *)
    GRAVITY              : REAL := 9.80665; (* Acceleration m/s^2 *)
    P_ATM_BAR            : REAL := 1.01325; (* Surface atmospheric pressure *)
    PA_TO_BAR            : REAL := 0.00001; (* Pascal to Bar conversion *)
    PRESSURE_TOL_BAR     : REAL := 0.25;    (* Allowed delta P for opening muzzle door *)
    
    (* Timing Limits *)
    T_FLOOD_MAX          : TIME := T#45s;
    T_EQUALIZE_MAX       : TIME := T#90s;
    T_IMPULSE_DUR        : TIME := T#1s250ms; (* 1.25s water ram ejection *)
    T_DRAIN_MAX          : TIME := T#120s;
END_VAR

VAR
    Flood_Timer          : TON;
    Equalize_Timer       : TON;
    Launch_Timer         : TON;
    Drain_Timer          : TON;
    
    Pressure_Diff        : REAL;
    Breech_Safe          : BOOL;
    Muzzle_Safe          : BOOL;
END_VAR

(* 1. CRITICAL SUBSAFE INTERLOCKS *)
(* Breech must be fully closed and locked before water can enter the tube *)
Breech_Safe := Breech_Door_Closed AND Breech_Door_Locked;

(* Muzzle can only operate if Breech is safe (prevent straight-through hull breach) *)
Muzzle_Safe := Breech_Safe;

(* Immediate fault on catastrophic interlock failure *)
IF NOT Breech_Safe AND NOT Muzzle_Door_Closed THEN
    Fault_Code := 1; (* CRITICAL: BOTH DOORS OPEN *)
    State := ST_FAULT;
END_IF;

IF Cmd_Emergency_Stop THEN
    Fault_Code := 99; (* Operator Emergency Stop *)
    State := ST_FAULT;
END_IF;

(* 2. HYDROSTATIC CALCULATION *)
(* Calculate ambient ocean pressure at current depth to set equalization target *)
Target_Sea_Pressure := P_ATM_BAR + (RHO_SEAWATER * GRAVITY * Submarine_Depth_m * PA_TO_BAR);
Pressure_Diff := ABS(Target_Sea_Pressure - Tube_Pressure_Bar);

(* 3. STATE MACHINE *)
CASE State OF
    ST_IDLE:
        Flood_Valve_Cmd := FALSE;
        Equalize_Valve_Cmd := FALSE;
        Impulse_Valve_Cmd := FALSE;
        Drain_Valve_Cmd := FALSE;
        Muzzle_Door_Open_Cmd := FALSE;
        Ready_To_Fire := FALSE;
        Fault_Code := 0;
        
        IF Cmd_Flood AND Breech_Safe AND Muzzle_Door_Closed AND Weapon_Loaded THEN
            State := ST_FLOODING;
        ELSIF Cmd_Drain AND Muzzle_Door_Closed THEN
            State := ST_DRAINING;
        END_IF;

    ST_FLOODING:
        Flood_Valve_Cmd := TRUE;
        (* Transition to Equalize manually or automatically if pressure rises slightly *)
        IF Cmd_Equalize OR (Tube_Pressure_Bar > P_ATM_BAR + 1.0) THEN
            Flood_Valve_Cmd := FALSE;
            State := ST_EQUALIZING;
        END_IF;
        
        IF Flood_Timer.Q THEN
            State := ST_FAULT;
            Fault_Code := 2; (* Flood timeout - check valve/strainer *)
        END_IF;

    ST_EQUALIZING:
        Equalize_Valve_Cmd := TRUE;
        
        (* When delta pressure is within tolerance, tube is safe to open to sea *)
        IF Pressure_Diff <= PRESSURE_TOL_BAR THEN
            Equalize_Valve_Cmd := FALSE;
            State := ST_EQUALIZED;
        END_IF;
        
        IF Equalize_Timer.Q THEN
            Equalize_Valve_Cmd := FALSE;
            State := ST_FAULT;
            Fault_Code := 3; (* Equalize timeout - ship depth changing too fast or blocked port *)
        END_IF;

    ST_EQUALIZED:
        IF Cmd_Open_Muzzle AND Muzzle_Safe THEN
            Muzzle_Door_Open_Cmd := TRUE;
            State := ST_MUZZLE_OPENING;
        END_IF;

    ST_MUZZLE_OPENING:
        (* Assuming mechanical limit switch clears Muzzle_Door_Closed when fully open *)
        IF NOT Muzzle_Door_Closed THEN
            State := ST_READY_TO_FIRE;
        END_IF;

    ST_READY_TO_FIRE:
        Ready_To_Fire := TRUE;
        
        IF Cmd_Launch THEN
            Ready_To_Fire := FALSE;
            State := ST_FIRING;
        END_IF;

    ST_FIRING:
        (* Water Ram Impulse Valve control logic *)
        Impulse_Valve_Cmd := TRUE;
        
        IF Launch_Timer.Q THEN
            Impulse_Valve_Cmd := FALSE;
            Muzzle_Door_Open_Cmd := FALSE; (* Auto close muzzle after shot *)
            State := ST_IDLE; (* Wait for close and drain command *)
        END_IF;

    ST_DRAINING:
        Drain_Valve_Cmd := TRUE;
        
        IF Tube_Pressure_Bar <= P_ATM_BAR + 0.1 THEN
            Drain_Valve_Cmd := FALSE;
            State := ST_IDLE;
        END_IF;
        
        IF Drain_Timer.Q THEN
            State := ST_FAULT;
            Fault_Code := 4; (* Drain timeout *)
        END_IF;

    ST_FAULT:
        (* Safe State Enforcement *)
        Flood_Valve_Cmd := FALSE;
        Equalize_Valve_Cmd := FALSE;
        Impulse_Valve_Cmd := FALSE;
        Drain_Valve_Cmd := FALSE;
        Muzzle_Door_Open_Cmd := FALSE;
        Ready_To_Fire := FALSE;
        
        IF NOT Cmd_Emergency_Stop AND Cmd_Drain THEN
            Fault_Code := 0;
            State := ST_IDLE;
        END_IF;

END_CASE;

(* 4. TIMERS *)
Flood_Timer(IN := (State = ST_FLOODING), PT := T_FLOOD_MAX);
Equalize_Timer(IN := (State = ST_EQUALIZING), PT := T_EQUALIZE_MAX);
Launch_Timer(IN := (State = ST_FIRING), PT := T_IMPULSE_DUR);
Drain_Timer(IN := (State = ST_DRAINING), PT := T_DRAIN_MAX);

END_FUNCTION_BLOCK"
        }
    )
}

$json = $obj | ConvertTo-Json -Compress
$json | Out-File -FilePath data\synthetic_generation_v3_enterprise.jsonl -Append -Encoding UTF8
