import json
import os

filepath = r"C:\Users\majip\Downloads\LLM REASEARCH\Local_Ollama_Evol_Pipeline\seeds\tier1_enterprise_grade\synthetic_generation_v3_enterprise.jsonl"

user_prompt = "Write the PLC logic implementation for the 'FRAC_PUMP_AND_BLENDER_CONTROLLER' function block/module. This block must evolve from a basic fluid loop into a Massive Hydraulic Fracturing (Fracking) Blender and Pump Controller. Technical Specs: 1. Proppant (sand) and fracturing fluid mixing ratio cross-control. 2. High-pressure (15,000 PSI) quintuplex pump synchronization. 3. Cavitation detection and automatic flow bypass."

assistant_content = """(*
VERSION 1.0
AUTHOR: Enterprise Geotechnical Systems
DESCRIPTION: Massive Hydraulic Fracturing (Fracking) Blender and Pump Controller.
FEATURES:
1. Proppant and fracturing fluid mixing ratio cross-control (Ratio Control).
2. High-pressure (15,000 PSI) quintuplex pump synchronization (RPM & Phase control).
3. Cavitation detection (based on suction pressure and fluid density drops) and automatic flow bypass.
*)
FUNCTION_BLOCK FRAC_PUMP_AND_BLENDER_CONTROLLER
VAR_INPUT
    Enable : BOOL;                  (* System Enable *)
    Start_Pumping : BOOL;           (* Start Frac Operation *)
    Emergency_Stop : BOOL;          (* E-Stop *)
    
    // Process Setpoints
    Target_Discharge_Pressure : REAL; (* PSI, typically 10,000 - 15,000 *)
    Target_Flow_Rate : REAL;        (* bbl/min *)
    Target_Proppant_Conc : REAL;    (* lbs/gal (PPA) *)
    
    // Blender Sensors
    Clean_Fluid_Flow : REAL;        (* bbl/min *)
    Sand_Auger_Speed : REAL;        (* RPM of proppant delivery auger *)
    Blender_Tub_Level : REAL;       (* % 0-100 *)
    Discharge_Density : REAL;       (* lbs/gal (from densitometer) *)
    
    // Pump Sensors
    Suction_Pressure : REAL;        (* PSI *)
    Discharge_Pressure : REAL;      (* PSI *)
    Pump_RPM : REAL;                (* Current Quintuplex Pump RPM *)
    Plunger_Phases : ARRAY[1..5] OF REAL; (* Degrees 0-360 for 5 plungers *)
    Vibration_Level : REAL;         (* mm/s RMS for cavitation detection *)
END_VAR

VAR_OUTPUT
    // Actuators
    Clean_Fluid_Valve_Cmd : REAL;   (* % open 0-100 *)
    Sand_Auger_Cmd : REAL;          (* RPM Setpoint *)
    Pump_Throttle_Cmd : REAL;       (* 0-100% Throttle *)
    Bypass_Valve_Cmd : BOOL;        (* TRUE = Open Bypass (Recirculate) *)
    
    // Status
    System_State : INT;             (* 0=Off, 1=Priming, 2=Blending, 3=Pumping, 4=Bypass, 99=Fault *)
    Current_Proppant_Conc : REAL;   (* Calculated lbs/gal *)
    Cavitation_Warning : BOOL;      (* Cavitation detected flag *)
    Sync_Error : REAL;              (* Pump phase synchronization error *)
END_VAR

VAR
    // Internal State
    PID_Fluid : PID_CONTROLLER;
    PID_Auger : PID_CONTROLLER;
    PID_Pump : PID_CONTROLLER;
    
    // Timers
    Cavitation_Timer : TON;
    Priming_Timer : TON;
    
    // Internal Calc
    Calculated_Sand_Rate : REAL;
    Target_Sand_Rate : REAL;
    Phase_Spacing : REAL := 72.0; (* 360/5 for Quintuplex *)
    Phase_Variance : REAL;
    i : INT;
    Expected_Phase : REAL;
END_VAR

// 1. Emergency and Basic Interlocks
IF Emergency_Stop THEN
    System_State := 99;
    Clean_Fluid_Valve_Cmd := 0.0;
    Sand_Auger_Cmd := 0.0;
    Pump_Throttle_Cmd := 0.0;
    Bypass_Valve_Cmd := TRUE; // Open bypass to drop pressure instantly
    RETURN;
END_IF;

IF NOT Enable THEN
    System_State := 0;
    Clean_Fluid_Valve_Cmd := 0.0;
    Sand_Auger_Cmd := 0.0;
    Pump_Throttle_Cmd := 0.0;
    Bypass_Valve_Cmd := TRUE;
    RETURN;
END_IF;

// 2. Cavitation Detection (Low suction pressure OR high vibration OR erratic density)
Cavitation_Timer(IN := (Suction_Pressure < 20.0) OR (Vibration_Level > 15.0), PT := T#500MS);
IF Cavitation_Timer.Q THEN
    Cavitation_Warning := TRUE;
    Bypass_Valve_Cmd := TRUE; (* Automatic Flow Bypass *)
    System_State := 4; // Bypass mode
ELSE
    Cavitation_Warning := FALSE;
END_IF;

// 3. State Machine
CASE System_State OF
    0: // Ready
        Bypass_Valve_Cmd := TRUE;
        IF Start_Pumping THEN
            System_State := 1;
        END_IF;

    1: // Priming
        Bypass_Valve_Cmd := TRUE;
        Clean_Fluid_Valve_Cmd := 50.0; // Fill tub
        Pump_Throttle_Cmd := 10.0; // Low idle
        Priming_Timer(IN:=TRUE, PT:=T#10S);
        IF Priming_Timer.Q AND Blender_Tub_Level > 60.0 THEN
            Priming_Timer(IN:=FALSE); // Reset
            System_State := 2;
        END_IF;

    2: // Blending & Pumping
        IF NOT Cavitation_Warning THEN
            Bypass_Valve_Cmd := FALSE;
            
            // --- Feature 1: Proppant and Fluid Mixing Ratio Cross-Control ---
            // The clean fluid rate is controlled to maintain Target Flow Rate
            PID_Fluid(SetPoint := Target_Flow_Rate, ProcessValue := Clean_Fluid_Flow, Kp := 2.5, Ki := 0.5);
            Clean_Fluid_Valve_Cmd := PID_Fluid.Output;
            
            // Cross-control: Target Sand Rate is derived from Actual Clean Fluid Flow * Target Concentration
            Target_Sand_Rate := Clean_Fluid_Flow * Target_Proppant_Conc; // lbs/min
            
            // Auger feedback control based on target sand rate
            Calculated_Sand_Rate := Sand_Auger_Speed * 15.5; // Example constant: 15.5 lbs per RPM
            PID_Auger(SetPoint := Target_Sand_Rate, ProcessValue := Calculated_Sand_Rate, Kp := 1.2, Ki := 0.3);
            Sand_Auger_Cmd := PID_Auger.Output;
            
            Current_Proppant_Conc := Calculated_Sand_Rate / MAX(Clean_Fluid_Flow, 0.1);
            
            // --- Feature 2: High-Pressure Quintuplex Pump Synchronization ---
            // Pump throttle controls discharge pressure
            PID_Pump(SetPoint := Target_Discharge_Pressure, ProcessValue := Discharge_Pressure, Kp := 0.8, Ki := 0.1);
            Pump_Throttle_Cmd := PID_Pump.Output;
            
            // Analyze synchronization of the 5 plungers (Quintuplex)
            // Ideal spacing is 72 degrees apart.
            Phase_Variance := 0.0;
            FOR i := 2 TO 5 DO
                Expected_Phase := Plunger_Phases[1] + (i-1) * Phase_Spacing;
                IF Expected_Phase > 360.0 THEN Expected_Phase := Expected_Phase - 360.0; END_IF;
                Phase_Variance := Phase_Variance + ABS(Plunger_Phases[i] - Expected_Phase);
            END_FOR;
            Sync_Error := Phase_Variance / 4.0;
            
            // If synchronization error is too high (mechanical slippage, valve failure)
            IF Sync_Error > 15.0 THEN
                System_State := 99; // Fault due to pump desync
            END_IF;
            
            // High pressure cutoff
            IF Discharge_Pressure > 15500.0 THEN // Max spec is 15000, 500 buffer
                System_State := 99;
            END_IF;
        END_IF;
        
    4: // Bypass (Cavitation Recovery)
        Clean_Fluid_Valve_Cmd := 100.0; // Flood suction
        Sand_Auger_Cmd := 0.0; // Stop sand
        Pump_Throttle_Cmd := 10.0; // Idle pump
        IF NOT Cavitation_Warning THEN
            System_State := 1; // Go back to priming
        END_IF;
        
    99: // Fault State
        Clean_Fluid_Valve_Cmd := 0.0;
        Sand_Auger_Cmd := 0.0;
        Pump_Throttle_Cmd := 0.0;
        Bypass_Valve_Cmd := TRUE;
        
END_CASE;

END_FUNCTION_BLOCK

(* Dummy PID Controller for completeness *)
FUNCTION_BLOCK PID_CONTROLLER
VAR_INPUT
    SetPoint : REAL;
    ProcessValue : REAL;
    Kp : REAL;
    Ki : REAL;
END_VAR
VAR_OUTPUT
    Output : REAL;
END_VAR
VAR
    Error : REAL;
    Integral : REAL;
END_VAR
    Error := SetPoint - ProcessValue;
    Integral := Integral + Error;
    Output := (Kp * Error) + (Ki * Integral);
    IF Output > 100.0 THEN Output := 100.0; END_IF;
    IF Output < 0.0 THEN Output := 0.0; END_IF;
END_FUNCTION_BLOCK"""

data = {
    "messages": [
        {"role": "user", "content": user_prompt},
        {"role": "assistant", "content": assistant_content}
    ]
}

with open(filepath, "a", encoding="utf-8") as f:
    f.write(json.dumps(data) + "\n")
print("Done")

