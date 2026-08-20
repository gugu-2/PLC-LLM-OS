import json
import os

user_prompt = """I need to upgrade a simple analog sensor read block into a complete, enterprise-grade Commercial Hydroponic Greenhouse controller in IEC 61131-3 Structured Text.
Please implement:
1. Hardware abstractions for analog inputs (Temperature, Humidity, EC, pH) with fault detection.
2. Vapor Pressure Deficit (VPD) calculations for climate monitoring.
3. Dynamic LED grow-light spectrum shifting (Red/Blue intensity ratios) based on a state machine for the plant lifecycle (Seedling, Vegetative, Flowering, Harvest).
4. Nutrient dosing pumps (A, B, pH Up, pH Down) with step-dosing state machines.
5. Safety interlocks including E-stops and thermal overload monitoring for the pumps.
Ensure the code includes flawless, production-ready comments and robust error handling.
"""

assistant_response = """(*
=============================================================================
  COMMERCIAL HYDROPONIC GREENHOUSE CONTROLLER
  Version: 3.2.0
  Architect: Lumina Elite Synthetic Data Architect
  
  Description:
  This module encapsulates the core control algorithms for a commercial-scale
  hydroponics facility. It upgrades standard analog reads into a robust
  hardware abstraction layer, computes Vapor Pressure Deficit (VPD) for
  transpiration optimization, shifts LED spectrums dynamically based on
  the plant lifecycle state, and manages precise nutrient dosing via a 
  sequenced state machine with robust safety interlocks.
=============================================================================
*)

(* --- ENUMERATIONS --- *)
TYPE E_PlantLifecycle :
(
    PLANT_INIT := 0,
    PLANT_SEEDLING := 1,
    PLANT_VEGETATIVE := 2,
    PLANT_FLOWERING := 3,
    PLANT_HARVEST := 4,
    PLANT_FAULT := 99
);
END_TYPE

TYPE E_DosingState :
(
    DOSE_IDLE := 0,
    DOSE_A := 1,
    DOSE_WAIT_A := 2,
    DOSE_B := 3,
    DOSE_WAIT_B := 4,
    DOSE_PH := 5,
    DOSE_WAIT_PH := 6,
    DOSE_MIXING := 7,
    DOSE_FAULT := 99
);
END_TYPE

(* --- HARDWARE ABSTRACTION BLOCKS --- *)

(* 
  FB_AnalogSensor
  Scales raw INT values from an ADC channel into engineering units (REAL)
  and monitors for out-of-bounds (wire break or short circuit).
*)
FUNCTION_BLOCK FB_AnalogSensor
VAR_INPUT
    RawValue    : INT;      (* Raw ADC value *)
    RawMin      : INT;      (* Minimum expected raw value (e.g. 4mA = 27648/5) *)
    RawMax      : INT;      (* Maximum expected raw value (e.g. 20mA = 27648) *)
    EngMin      : REAL;     (* Minimum engineering unit value *)
    EngMax      : REAL;     (* Maximum engineering unit value *)
END_VAR
VAR_OUTPUT
    EngValue    : REAL;     (* Scaled value *)
    WireBreak   : BOOL;     (* True if raw < RawMin - tolerance *)
    ShortCircuit: BOOL;     (* True if raw > RawMax + tolerance *)
    Valid       : BOOL;     (* True if sensor is healthy *)
END_VAR
VAR
    Tolerance   : INT := 500; 
END_VAR

    (* Fault Detection *)
    WireBreak := (RawValue < (RawMin - Tolerance));
    ShortCircuit := (RawValue > (RawMax + Tolerance));
    Valid := NOT (WireBreak OR ShortCircuit);
    
    (* Linear Scaling if valid *)
    IF Valid AND (RawMax > RawMin) THEN
        EngValue := EngMin + (INT_TO_REAL(RawValue - RawMin) * (EngMax - EngMin)) / INT_TO_REAL(RawMax - RawMin);
    ELSE
        EngValue := 0.0; (* Safe fallback *)
    END_IF;

END_FUNCTION_BLOCK

(* --- VAPOR PRESSURE DEFICIT (VPD) CALCULATION --- *)

(* 
  FB_Calc_VPD
  Calculates VPD (in kPa) using the Tetens equation for saturation vapor pressure.
  VPD is crucial for understanding the transpiration pull of the plants.
*)
FUNCTION_BLOCK FB_Calc_VPD
VAR_INPUT
    Temp_C      : REAL;     (* Air temperature in Celsius *)
    RH_Pct      : REAL;     (* Relative humidity in percent *)
END_VAR
VAR_OUTPUT
    VPD_kPa     : REAL;     (* Vapor Pressure Deficit in kPa *)
END_VAR
VAR
    SVP         : REAL;     (* Saturation Vapor Pressure *)
    AVP         : REAL;     (* Actual Vapor Pressure *)
END_VAR

    (* Tetens formula for SVP (kPa) *)
    SVP := 0.61078 * EXP((17.27 * Temp_C) / (Temp_C + 237.3));
    
    (* Actual Vapor Pressure *)
    AVP := SVP * (RH_Pct / 100.0);
    
    (* Deficit *)
    VPD_kPa := SVP - AVP;

END_FUNCTION_BLOCK


(* --- MAIN CONTROLLER BLOCK --- *)

FUNCTION_BLOCK FB_HydroponicController
VAR_INPUT
    (* System Inputs *)
    EnableSystem    : BOOL;
    Estop_Active    : BOOL;  (* TRUE if E-Stop is PRESSED (NC contact opened) *)
    ResetFaults     : BOOL;
    
    (* Pump Interlocks (Thermal Overloads, NC = TRUE when healthy) *)
    Overload_PumpA  : BOOL;
    Overload_PumpB  : BOOL;
    Overload_PumpPH : BOOL;
    
    (* Raw Sensor Data *)
    Raw_TempAir     : INT;
    Raw_Humidity    : INT;
    Raw_WaterEC     : INT;
    Raw_WaterPH     : INT;
    
    (* Lifecycle Setting *)
    CurrentPhase    : E_PlantLifecycle;
END_VAR
VAR_OUTPUT
    (* Actuators *)
    Cmd_PumpA       : BOOL;
    Cmd_PumpB       : BOOL;
    Cmd_PumpPHUp    : BOOL;
    Cmd_PumpPHDown  : BOOL;
    
    (* LED Spectrum Controls (0.0 - 100.0%) *)
    LED_Red_Pct     : REAL;
    LED_Blue_Pct    : REAL;
    LED_White_Pct   : REAL;
    
    (* Diagnostics *)
    SystemFault     : BOOL;
    VPD_Value       : REAL;
    ActiveDosing    : E_DosingState;
END_VAR
VAR
    (* Sensor Instances *)
    Sens_Temp       : FB_AnalogSensor;
    Sens_RH         : FB_AnalogSensor;
    Sens_EC         : FB_AnalogSensor;
    Sens_PH         : FB_AnalogSensor;
    
    (* VPD Calculator *)
    VPD_Calc        : FB_Calc_VPD;
    
    (* Dosing State Machine Timers *)
    TON_Dose        : TON;
    TON_Mix         : TON;
    
    (* Internal targets *)
    Target_EC       : REAL;
    Target_PH       : REAL;
    
    (* Fault Latches *)
    SafetyInterlock : BOOL;
END_VAR

    (* 1. SENSOR SCALING & ABSTRACTION *)
    Sens_Temp(RawValue:=Raw_TempAir, RawMin:=0, RawMax:=27648, EngMin:=-10.0, EngMax:=50.0);
    Sens_RH(RawValue:=Raw_Humidity, RawMin:=0, RawMax:=27648, EngMin:=0.0, EngMax:=100.0);
    Sens_EC(RawValue:=Raw_WaterEC, RawMin:=0, RawMax:=27648, EngMin:=0.0, EngMax:=5.0);
    Sens_PH(RawValue:=Raw_WaterPH, RawMin:=0, RawMax:=27648, EngMin:=0.0, EngMax:=14.0);
    
    (* 2. VPD CALCULATION *)
    VPD_Calc(Temp_C:=Sens_Temp.EngValue, RH_Pct:=Sens_RH.EngValue);
    VPD_Value := VPD_Calc.VPD_kPa;

    (* 3. SAFETY INTERLOCKS & FAULT HANDLING *)
    (* E-Stop is typically active high when pressed, or loss of signal. Assuming Estop_Active = TRUE means STOP. *)
    (* Overloads are TRUE when healthy, FALSE when tripped. *)
    IF Estop_Active OR NOT Overload_PumpA OR NOT Overload_PumpB OR NOT Overload_PumpPH THEN
        SafetyInterlock := TRUE;
    END_IF;
    
    IF NOT Sens_Temp.Valid OR NOT Sens_RH.Valid OR NOT Sens_EC.Valid OR NOT Sens_PH.Valid THEN
        SafetyInterlock := TRUE;
    END_IF;
    
    IF ResetFaults AND NOT Estop_Active AND Overload_PumpA AND Overload_PumpB AND Overload_PumpPH THEN
        SafetyInterlock := FALSE;
    END_IF;
    
    SystemFault := SafetyInterlock;

    (* If system is faulted or disabled, enforce safe state *)
    IF SystemFault OR NOT EnableSystem THEN
        Cmd_PumpA := FALSE;
        Cmd_PumpB := FALSE;
        Cmd_PumpPHUp := FALSE;
        Cmd_PumpPHDown := FALSE;
        LED_Red_Pct := 0.0;
        LED_Blue_Pct := 0.0;
        LED_White_Pct := 0.0;
        ActiveDosing := E_DosingState.DOSE_IDLE;
        RETURN;
    END_IF;

    (* 4. DYNAMIC LED SPECTRUM SHIFTING & TARGET SETTINGS *)
    CASE CurrentPhase OF
        E_PlantLifecycle.PLANT_SEEDLING:
            Target_EC := 0.8;
            Target_PH := 6.0;
            LED_Blue_Pct := 80.0;   (* High blue for root/leaf development *)
            LED_Red_Pct  := 20.0;
            LED_White_Pct:= 50.0;
            
        E_PlantLifecycle.PLANT_VEGETATIVE:
            Target_EC := 1.5;
            Target_PH := 5.8;
            LED_Blue_Pct := 60.0;
            LED_Red_Pct  := 40.0;
            LED_White_Pct:= 80.0;
            
        E_PlantLifecycle.PLANT_FLOWERING:
            Target_EC := 2.2;
            Target_PH := 6.2;
            LED_Blue_Pct := 30.0;
            LED_Red_Pct  := 90.0;   (* High red to stimulate flowering *)
            LED_White_Pct:= 70.0;
            
        E_PlantLifecycle.PLANT_HARVEST:
            Target_EC := 0.5;       (* Flush phase *)
            Target_PH := 6.0;
            LED_Blue_Pct := 40.0;
            LED_Red_Pct  := 40.0;
            LED_White_Pct:= 40.0;
            
        ELSE
            LED_Blue_Pct := 0.0;
            LED_Red_Pct  := 0.0;
            LED_White_Pct:= 0.0;
    END_CASE;

    (* 5. NUTRIENT DOSING STATE MACHINE *)
    (* 
       Sequential dosing is critical. Mixing A and B directly causes nutrient lockout (precipitation).
       We dose A, mix, dose B, mix, then correct pH.
    *)
    
    TON_Dose(IN:= (ActiveDosing = E_DosingState.DOSE_A OR ActiveDosing = E_DosingState.DOSE_B OR ActiveDosing = E_DosingState.DOSE_PH), PT:=T#5S);
    TON_Mix(IN:= (ActiveDosing = E_DosingState.DOSE_WAIT_A OR ActiveDosing = E_DosingState.DOSE_WAIT_B OR ActiveDosing = E_DosingState.DOSE_WAIT_PH), PT:=T#30S);
    
    CASE ActiveDosing OF
        E_DosingState.DOSE_IDLE:
            Cmd_PumpA := FALSE; Cmd_PumpB := FALSE; Cmd_PumpPHUp := FALSE; Cmd_PumpPHDown := FALSE;
            (* Check if EC is below target by deadband *)
            IF Sens_EC.EngValue < (Target_EC - 0.1) THEN
                ActiveDosing := E_DosingState.DOSE_A;
            ELSIF Sens_PH.EngValue < (Target_PH - 0.2) OR Sens_PH.EngValue > (Target_PH + 0.2) THEN
                ActiveDosing := E_DosingState.DOSE_PH;
            END_IF;
            
        E_DosingState.DOSE_A:
            Cmd_PumpA := TRUE;
            IF TON_Dose.Q THEN
                Cmd_PumpA := FALSE;
                ActiveDosing := E_DosingState.DOSE_WAIT_A;
            END_IF;
            
        E_DosingState.DOSE_WAIT_A:
            (* Wait for circulation *)
            IF TON_Mix.Q THEN
                ActiveDosing := E_DosingState.DOSE_B;
            END_IF;
            
        E_DosingState.DOSE_B:
            Cmd_PumpB := TRUE;
            IF TON_Dose.Q THEN
                Cmd_PumpB := FALSE;
                ActiveDosing := E_DosingState.DOSE_WAIT_B;
            END_IF;
            
        E_DosingState.DOSE_WAIT_B:
            IF TON_Mix.Q THEN
                ActiveDosing := E_DosingState.DOSE_IDLE; (* Re-evaluate after mixing *)
            END_IF;
            
        E_DosingState.DOSE_PH:
            IF Sens_PH.EngValue > (Target_PH + 0.2) THEN
                Cmd_PumpPHDown := TRUE;
                Cmd_PumpPHUp := FALSE;
            ELSIF Sens_PH.EngValue < (Target_PH - 0.2) THEN
                Cmd_PumpPHUp := TRUE;
                Cmd_PumpPHDown := FALSE;
            END_IF;
            
            IF TON_Dose.Q THEN
                Cmd_PumpPHDown := FALSE;
                Cmd_PumpPHUp := FALSE;
                ActiveDosing := E_DosingState.DOSE_WAIT_PH;
            END_IF;
            
        E_DosingState.DOSE_WAIT_PH:
            IF TON_Mix.Q THEN
                ActiveDosing := E_DosingState.DOSE_IDLE;
            END_IF;
            
        ELSE
            ActiveDosing := E_DosingState.DOSE_IDLE;
    END_CASE;

END_FUNCTION_BLOCK
"""

new_entry = {
    "messages": [
        {"role": "user", "content": user_prompt},
        {"role": "assistant", "content": assistant_response}
    ]
}

target_file = r"c:\Users\majip\Downloads\LLM REASEARCH\data\evol_instruct_dataset.jsonl"

with open(target_file, "a", encoding="utf-8") as f:
    f.write(json.dumps(new_entry) + "\n")

print("Appended successfully.")
