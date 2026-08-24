import json
import os

data = {
    "messages": [
        {
            "role": "user",
            "content": "You are acting as a Lead Plasma Control Engineer at a global Nuclear Fusion research facility (e.g., ITER). Evolve a basic PID block into a Tokamak Plasma Magnetic Confinement Controller.\n\nTechnical Specifications required in the ST code:\n1. Poloidal and Toroidal magnetic field coil synchronization using superconducting niobium-tin electromagnets to shape a 150-million-degree plasma torus.\n2. Plasma Disruption Mitigation System (DMS): if magneto-hydrodynamic (MHD) instabilities indicate an impending plasma collapse, instantly trigger high-pressure shattered pellet injection (argon/neon) to quench the plasma and protect the divertor tiles.\n3. Neutral beam injector (NBI) interlocks to prevent firing if the plasma density is too low, which would cause the beam to burn a hole through the inner vacuum vessel wall."
        },
        {
            "role": "assistant",
            "content": """Here is the IEC 61131-3 Structured Text implementation for the Tokamak Plasma Magnetic Confinement Controller, integrating superconducting coil synchronization, DMS, and NBI interlocks.

```iecst
(*
======================================================================================
TOKAMAK PLASMA MAGNETIC CONFINEMENT & DISRUPTION MITIGATION CONTROLLER
======================================================================================
Facility: Advanced Fusion Research Center (AFRC)
Component: IEC 61131-3 Superconducting Coil & Heating Interlock System
Version: 4.12.0 (Enterprise-Grade Mission Critical)
Author: Lead Plasma Control Engineer
======================================================================================
*)

TYPE Superconducting_Coil_State :
    STRUCT
        Current_kA          : REAL; (* kiloAmperes *)
        Temperature_K       : REAL; (* Kelvin *)
        Quench_Detect       : BOOL; (* Superconducting quench detected *)
        Cooling_Flow_kg_s   : REAL; (* Helium coolant flow rate *)
    END_STRUCT;
END_TYPE

TYPE Plasma_Diagnostics :
    STRUCT
        Density_m3          : REAL; (* e-/m^3 *)
        Temperature_keV     : REAL; (* kilo-electron volts *)
        Plasma_Current_MA   : REAL; (* MegaAmperes *)
        MHD_Instability_Idx : REAL; (* 0.0 to 1.0 (1.0 = Critical Tearing Mode) *)
        Vertical_Displ_m    : REAL; (* Vertical displacement from magnetic axis *)
    END_STRUCT;
END_TYPE

TYPE DMS_Subsystem :
    STRUCT
        Argon_Pressure_MPa  : REAL;
        Neon_Pressure_MPa   : REAL;
        Valve_Armed         : BOOL;
        Injection_Triggered : BOOL;
    END_STRUCT;
END_TYPE

FUNCTION_BLOCK FB_Tokamak_Confinement_Controller
VAR_INPUT
    Enable_System           : BOOL;
    
    (* Diagnostics *)
    Sensor_Plasma           : Plasma_Diagnostics;
    Sensor_Poloidal_Coils   : ARRAY[1..6] OF Superconducting_Coil_State;
    Sensor_Toroidal_Coils   : ARRAY[1..18] OF Superconducting_Coil_State;
    
    (* Setpoints *)
    SP_Plasma_Density       : REAL := 1.0E20; (* Nominal Density e-/m^3 *)
    SP_Toroidal_Field_T     : REAL := 5.3;    (* Tesla *)
    
    (* Interlock Thresholds *)
    Min_Density_NBI         : REAL := 0.3E20; (* Minimum density for NBI firing *)
    Max_MHD_Threshold       : REAL := 0.85;   (* Instability trigger threshold *)
    Quench_Temp_Limit_K     : REAL := 5.5;    (* Nb3Sn max operating temp before quench *)
END_VAR

VAR_OUTPUT
    (* Actuators *)
    Cmd_Poloidal_Voltage    : ARRAY[1..6] OF REAL; (* kV to PF coils *)
    Cmd_Toroidal_Voltage    : ARRAY[1..18] OF REAL;(* kV to TF coils *)
    
    (* Interlocks & Mitigation *)
    Permit_NBI_Firing       : BOOL;
    DMS_Status              : DMS_Subsystem;
    Fast_Coil_Discharge     : BOOL;
    
    (* Alarms *)
    Alarm_Disruption_Imminent : BOOL;
    Alarm_Coil_Quench         : BOOL;
    System_Healthy            : BOOL;
END_VAR

VAR
    (* Internal Controllers *)
    PID_Toroidal_Field      : FB_PID_Advanced;
    PID_Poloidal_Shape      : ARRAY[1..6] OF FB_PID_Advanced;
    
    i                       : INT;
    Total_TF_Current        : REAL;
    Calculated_TF_Field     : REAL;
    
    State_Machine           : INT := 0; 
    (* 0: Standby, 1: Ramp-up, 2: Flat-top, 3: Soft-Shutdown, 99: Disruption *)
END_VAR

(* -------------------------------------------------------------------------
   1. SUPERCONDUCTING COIL SYNCHRONIZATION (TOROIDAL & POLOIDAL)
   ------------------------------------------------------------------------- *)
System_Healthy := Enable_System;
Alarm_Coil_Quench := FALSE;

(* Check coil health (Nb3Sn Superconductors) *)
FOR i := 1 TO 18 DO
    IF Sensor_Toroidal_Coils[i].Temperature_K > Quench_Temp_Limit_K OR Sensor_Toroidal_Coils[i].Quench_Detect THEN
        Alarm_Coil_Quench := TRUE;
        System_Healthy := FALSE;
    END_IF;
END_FOR;

FOR i := 1 TO 6 DO
    IF Sensor_Poloidal_Coils[i].Temperature_K > Quench_Temp_Limit_K OR Sensor_Poloidal_Coils[i].Quench_Detect THEN
        Alarm_Coil_Quench := TRUE;
        System_Healthy := FALSE;
    END_IF;
END_FOR;

(* Calculate approximate Toroidal Field based on current (Ampere's Law simplified) *)
Total_TF_Current := 0.0;
FOR i := 1 TO 18 DO
    Total_TF_Current := Total_TF_Current + Sensor_Toroidal_Coils[i].Current_kA;
END_FOR;
Calculated_TF_Field := (Total_TF_Current * 1000.0) * 0.0001; (* Conversion factor for geometry *)

(* TF Coil Synchronization Control *)
PID_Toroidal_Field(
    Enable := System_Healthy,
    Setpoint := SP_Toroidal_Field_T,
    ProcessValue := Calculated_TF_Field,
    Kp := 4.5, Ki := 1.2, Kd := 0.1
);

FOR i := 1 TO 18 DO
    (* Distribute voltage command equally amongst TF coils *)
    Cmd_Toroidal_Voltage[i] := PID_Toroidal_Field.ControlOutput / 18.0;
END_FOR;

(* PF Coil Shaping Control (Synchronization with Vertical Displacement) *)
FOR i := 1 TO 6 DO
    PID_Poloidal_Shape[i](
        Enable := System_Healthy,
        Setpoint := 0.0, (* Aiming for zero vertical displacement error *)
        ProcessValue := Sensor_Plasma.Vertical_Displ_m,
        Kp := 12.0, Ki := 2.5, Kd := 8.0 (* High derivative for fast vertical stability *)
    );
    (* Shape specific multipliers for upper vs lower PF coils *)
    IF i <= 3 THEN
        Cmd_Poloidal_Voltage[i] := PID_Poloidal_Shape[i].ControlOutput * 1.5;
    ELSE
        Cmd_Poloidal_Voltage[i] := -PID_Poloidal_Shape[i].ControlOutput * 1.5;
    END_IF;
END_FOR;

(* -------------------------------------------------------------------------
   2. DISRUPTION MITIGATION SYSTEM (DMS)
   ------------------------------------------------------------------------- *)
(* Monitor Magneto-Hydrodynamic (MHD) instabilities (e.g., Neoclassical Tearing Modes) *)
IF Sensor_Plasma.MHD_Instability_Idx >= Max_MHD_Threshold THEN
    Alarm_Disruption_Imminent := TRUE;
    
    (* TRIGGER DMS INSTANTLY *)
    DMS_Status.Injection_Triggered := TRUE;
    DMS_Status.Valve_Armed := FALSE; 
    
    (* Initiate fast discharge of superconducting coils to prevent inductive arcing *)
    Fast_Coil_Discharge := TRUE;
    
    (* Enter disruption state *)
    State_Machine := 99;
    System_Healthy := FALSE;
    
    (* Force coil voltages to zero (dump resistors take over) *)
    FOR i := 1 TO 18 DO Cmd_Toroidal_Voltage[i] := 0.0; END_FOR;
    FOR i := 1 TO 6 DO Cmd_Poloidal_Voltage[i] := 0.0; END_FOR;
ELSE
    Alarm_Disruption_Imminent := FALSE;
    Fast_Coil_Discharge := FALSE;
    DMS_Status.Injection_Triggered := FALSE;
    
    IF System_Healthy THEN
        DMS_Status.Valve_Armed := TRUE; (* Ensure shatter valves are primed *)
    END_IF;
END_IF;

(* Quench detection also triggers fast discharge *)
IF Alarm_Coil_Quench THEN
    Fast_Coil_Discharge := TRUE;
    State_Machine := 99;
END_IF;

(* -------------------------------------------------------------------------
   3. NEUTRAL BEAM INJECTOR (NBI) INTERLOCKS
   ------------------------------------------------------------------------- *)
(* 
   Prevent NBI firing if plasma density is too low.
   High energy neutral beams can "shine through" low density plasma
   and melt the beryllium/tungsten armor on the inner vessel wall.
*)
IF (Sensor_Plasma.Density_m3 >= Min_Density_NBI) AND System_Healthy AND NOT Alarm_Disruption_Imminent THEN
    Permit_NBI_Firing := TRUE;
ELSE
    Permit_NBI_Firing := FALSE;
END_IF;

END_FUNCTION_BLOCK
```

### Design Rationale:
1. **Poloidal and Toroidal Synchronization**: Implements arrays of 18 TF coils and 6 PF coils simulating the geometry of a complex Tokamak. It calculates collective fields and actively trims errors using synchronized high-speed PID blocks for stable vertical control and field confinement. Nb3Sn thermal monitoring serves as a quench protection check before authorizing synchronization.
2. **Disruption Mitigation System (DMS)**: Constant cyclic evaluation of the `MHD_Instability_Idx`. Exceeding the disruption threshold (e.g., `0.85`) completely overrides standard procedures, disarms safety interlocks, and fires the `DMS_Status.Injection_Triggered` (shattered pellet injection) boolean while fast-dumping coil energy.
3. **NBI Interlocks (Shine-Through Protection)**: Implements `Permit_NBI_Firing` evaluating `Sensor_Plasma.Density_m3`. If the density falls beneath `Min_Density_NBI` (e.g., `0.3E20` e/m³), the heating beams are disabled to protect the innermost beryllium wall armor.
"""
        }
    ]
}

os.makedirs('data', exist_ok=True)
with open('data/synthetic_generation_v3_enterprise.jsonl', 'a') as f:
    f.write(json.dumps(data) + '\n')
