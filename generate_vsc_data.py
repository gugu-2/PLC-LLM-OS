import os
import json
import uuid

prompt = "You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data. Your specific domain is: HVDC Voltage-Source Converter (VSC). Task: Invent a highly complex control scenario for this domain (e.g., IGBT high-frequency switching matrices, harmonic filtering array sequencing, and DC line fault suppression). Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."

code = """```iec-st
FUNCTION_BLOCK FB_HVDC_VSC_Control
TITLE = 'HVDC Voltage-Source Converter Advanced Control Matrix'
VERSION : '2.1'

(*
=============================================================================
System: HVDC VSC Station
Subsystem: Core Converter Control, Harmonic Filtration, Fault Suppression
Description: Orchestrates IGBT switching sequence, reactive power compensation,
             and DC side fault mitigation through fast active damping.
=============================================================================
*)

VAR_INPUT
    Enable_System          : BOOL;  (* Master Enable *)
    Grid_Voltage_Alpha     : REAL;  (* Alpha component of grid voltage (pu) *)
    Grid_Voltage_Beta      : REAL;  (* Beta component of grid voltage (pu) *)
    DC_Link_Voltage        : REAL;  (* Measured DC Link Voltage (kV) *)
    DC_Link_Voltage_Ref    : REAL;  (* Reference DC Link Voltage (kV) *)
    Active_Power_Ref       : REAL;  (* Active Power Setpoint (MW) *)
    Reactive_Power_Ref     : REAL;  (* Reactive Power Setpoint (MVAR) *)
    Fault_DC_Overcurrent   : BOOL;  (* Hardware trigger for DC overcurrent *)
    Harmonic_Distortion    : REAL;  (* Measured THD on AC side (%) *)
END_VAR

VAR_OUTPUT
    IGBT_Gate_Pulse_U_Top  : BOOL;
    IGBT_Gate_Pulse_U_Bot  : BOOL;
    IGBT_Gate_Pulse_V_Top  : BOOL;
    IGBT_Gate_Pulse_V_Bot  : BOOL;
    IGBT_Gate_Pulse_W_Top  : BOOL;
    IGBT_Gate_Pulse_W_Bot  : BOOL;
    Harmonic_Filter_Enable : ARRAY[1..5] OF BOOL;
    DC_Breaker_Trip        : BOOL;
    System_Ready           : BOOL;
    Error_Code             : INT;
END_VAR

VAR
    PI_Volt_Kp             : REAL := 2.5;
    PI_Volt_Ki             : REAL := 15.0;
    Volt_Error             : REAL;
    Volt_Error_Integ       : REAL;
    
    Id_Ref                 : REAL;
    Iq_Ref                 : REAL;
    Id_Measured            : REAL;
    Iq_Measured            : REAL;
    
    PI_Curr_Kp             : REAL := 1.2;
    PI_Curr_Ki             : REAL := 20.0;
    Id_Error_Integ         : REAL;
    Iq_Error_Integ         : REAL;
    
    Modulation_Index_D     : REAL;
    Modulation_Index_Q     : REAL;
    
    Theta                  : REAL;
    Omega                  : REAL := 314.159; (* 50 Hz nominal *)
    
    Fault_Timer            : TIME;
    State                  : INT := 0; (* 0: OFF, 1: PRECHARGE, 2: RUNNING, 3: FAULT *)
    
    PWM_Carrier            : REAL;
    PWM_Dir                : BOOL := TRUE;
    
    Filter_Index           : INT;
END_VAR

(* Logic Implementation *)
IF NOT Enable_System THEN
    State := 0;
    System_Ready := FALSE;
    DC_Breaker_Trip := FALSE;
    Error_Code := 0;
    Volt_Error_Integ := 0.0;
    Id_Error_Integ := 0.0;
    Iq_Error_Integ := 0.0;
    
    IGBT_Gate_Pulse_U_Top := FALSE;
    IGBT_Gate_Pulse_U_Bot := FALSE;
    IGBT_Gate_Pulse_V_Top := FALSE;
    IGBT_Gate_Pulse_V_Bot := FALSE;
    IGBT_Gate_Pulse_W_Top := FALSE;
    IGBT_Gate_Pulse_W_Bot := FALSE;
    
    FOR Filter_Index := 1 TO 5 DO
        Harmonic_Filter_Enable[Filter_Index] := FALSE;
    END_FOR;
    RETURN;
END_IF;

(* Fault Suppression *)
IF Fault_DC_Overcurrent THEN
    State := 3;
    DC_Breaker_Trip := TRUE;
    System_Ready := FALSE;
    Error_Code := 99; (* Critical DC Fault *)
    IGBT_Gate_Pulse_U_Top := FALSE;
    IGBT_Gate_Pulse_U_Bot := FALSE;
    IGBT_Gate_Pulse_V_Top := FALSE;
    IGBT_Gate_Pulse_V_Bot := FALSE;
    IGBT_Gate_Pulse_W_Top := FALSE;
    IGBT_Gate_Pulse_W_Bot := FALSE;
    RETURN;
END_IF;

(* Phase Locked Loop (PLL) Approximation *)
Theta := Theta + Omega * 0.0001; (* Assume 100us cycle time *)
IF Theta > 6.2831853 THEN
    Theta := Theta - 6.2831853;
END_IF;

(* Outer Control Loop: DC Voltage / Power Control *)
Volt_Error := DC_Link_Voltage_Ref - DC_Link_Voltage;
Volt_Error_Integ := Volt_Error_Integ + (Volt_Error * 0.0001 * PI_Volt_Ki);

(* Limit Integrator *)
IF Volt_Error_Integ > 1000.0 THEN Volt_Error_Integ := 1000.0; END_IF;
IF Volt_Error_Integ < -1000.0 THEN Volt_Error_Integ := -1000.0; END_IF;

Id_Ref := (Volt_Error * PI_Volt_Kp) + Volt_Error_Integ;
Iq_Ref := Reactive_Power_Ref * 0.1; (* Simplified scaling *)

(* Inner Control Loop: Current Control in dq frame *)
Id_Error_Integ := Id_Error_Integ + ((Id_Ref - Id_Measured) * 0.0001 * PI_Curr_Ki);
Iq_Error_Integ := Iq_Error_Integ + ((Iq_Ref - Iq_Measured) * 0.0001 * PI_Curr_Ki);

Modulation_Index_D := ((Id_Ref - Id_Measured) * PI_Curr_Kp) + Id_Error_Integ - (Omega * Iq_Measured * 0.05);
Modulation_Index_Q := ((Iq_Ref - Iq_Measured) * PI_Curr_Kp) + Iq_Error_Integ + (Omega * Id_Measured * 0.05);

(* Harmonic Filter Sequencing Matrix *)
IF Harmonic_Distortion > 5.0 THEN
    Harmonic_Filter_Enable[1] := TRUE; (* 5th harmonic *)
    IF Harmonic_Distortion > 8.0 THEN Harmonic_Filter_Enable[2] := TRUE; END_IF; (* 7th harmonic *)
    IF Harmonic_Distortion > 12.0 THEN Harmonic_Filter_Enable[3] := TRUE; END_IF; (* 11th harmonic *)
ELSE
    Harmonic_Filter_Enable[1] := FALSE;
    Harmonic_Filter_Enable[2] := FALSE;
    Harmonic_Filter_Enable[3] := FALSE;
END_IF;

(* Generate PWM Carrier - Triangle Wave *)
IF PWM_Dir THEN
    PWM_Carrier := PWM_Carrier + 0.05;
    IF PWM_Carrier >= 1.0 THEN PWM_Dir := FALSE; END_IF;
ELSE
    PWM_Carrier := PWM_Carrier - 0.05;
    IF PWM_Carrier <= -1.0 THEN PWM_Dir := TRUE; END_IF;
END_IF;

(* Simplified SVM / Sine-Triangle PWM comparison *)
IF Modulation_Index_D > PWM_Carrier THEN
    IGBT_Gate_Pulse_U_Top := TRUE;
    IGBT_Gate_Pulse_U_Bot := FALSE;
ELSE
    IGBT_Gate_Pulse_U_Top := FALSE;
    IGBT_Gate_Pulse_U_Bot := TRUE;
END_IF;

State := 2;
System_Ready := TRUE;
Error_Code := 0;

END_FUNCTION_BLOCK
```"""

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": code}
    ]
}

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)

print(f"Saved to {filename}")
