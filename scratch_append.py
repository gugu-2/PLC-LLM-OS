import json
import os

plc_code = """(*
    VERSION 1.0
    TITLE: Heavy Mining Cone Crusher Sequencer
    DESCRIPTION: 
    Advanced sequencer for a Heavy Mining Cone Crusher. 
    Manages lubrication systems, tramp iron relief valve interlocks, 
    bowl float monitoring, and oil viscosity/temperature safety checks 
    prior to permitting main drive motor engagement.
*)

FUNCTION_BLOCK CONE_CRUSHER_DRIVE_SEQ
VAR_INPUT
    (* Commands *)
    cmd_Start             : BOOL; (* Start sequence command *)
    cmd_Stop              : BOOL; (* Normal stop command *)
    cmd_Reset             : BOOL; (* Fault reset command *)
    
    (* Safety & E-Stop *)
    E_Stop_OK             : BOOL; (* Emergency stop circuit (TRUE = Safe, FALSE = E-Stop) *)
    Motor_Thermal_OK      : BOOL; (* Main motor thermal overload (TRUE = Safe) *)
    
    (* Process Variables *)
    Oil_Temp_C            : REAL; (* Lube oil temperature in Celsius *)
    Oil_Viscosity_cSt     : REAL; (* Lube oil kinematic viscosity *)
    Crusher_Vibration_mm  : REAL; (* Bearing vibration levels *)
    
    (* Interlocks & Hardware Status *)
    fbk_Lube_Pump_Run     : BOOL; (* Lube pump contactor feedback *)
    Lube_Pressure_OK      : BOOL; (* Lube system pressure switch *)
    Bowl_Float_OK         : BOOL; (* Crusher bowl float / mechanical gap OK *)
    Tramp_Relief_Valve_OK : BOOL; (* Tramp iron relief valve is closed/pressurized *)
    fbk_Main_Motor_Run    : BOOL; (* Main crusher motor contactor feedback *)
END_VAR

VAR_INPUT CONSTANT
    (* Configurable Limits *)
    MIN_OIL_TEMP          : REAL := 25.0;  (* Minimum temp for safe viscosity *)
    MAX_OIL_TEMP          : REAL := 65.0;  (* Maximum safe operating temp *)
    MAX_VISCOSITY         : REAL := 150.0; (* Max cold viscosity in cSt *)
    MAX_VIBRATION         : REAL := 12.5;  (* Max permissible vibration mm/s *)
    
    (* Timers *)
    T_LUBE_PRE_START      : TIME := T#30S; (* Required lube time before start *)
    T_DRIVE_SPINUP        : TIME := T#15S; (* Allowed time for main motor spin-up *)
END_VAR

VAR_OUTPUT
    cmd_Lube_Pump         : BOOL;  (* Output to lube pump contactor *)
    cmd_Main_Motor        : BOOL;  (* Output to main drive contactor *)
    
    System_Ready          : BOOL;  (* Ready for feed *)
    Alarm_Active          : BOOL;  (* General alarm/fault active *)
    Active_State          : INT;   (* Current step in sequence *)
    State_String          : STRING[50]; (* Human-readable state *)
END_VAR

VAR
    (* Internal State Machine *)
    state                 : INT := 0;
    
    (* Timers *)
    tmr_LubePreStart      : TON;
    tmr_DriveSpinup       : TON;
    
    (* Edge Detection *)
    edge_Start            : R_TRIG;
    edge_Reset            : R_TRIG;
    
    (* Internal Flags *)
    bFault_Lube           : BOOL;
    bFault_Interlocks     : BOOL;
    bFault_Motor          : BOOL;
    bFault_Safety         : BOOL;
END_VAR

(* Edge Detections *)
edge_Start(CLK := cmd_Start);
edge_Reset(CLK := cmd_Reset);

(* Fault Reset Logic *)
IF edge_Reset.Q THEN
    bFault_Lube := FALSE;
    bFault_Interlocks := FALSE;
    bFault_Motor := FALSE;
    bFault_Safety := FALSE;
    IF state = 99 THEN
        state := 0; (* Reset to STOPPED state *)
    END_IF;
END_IF;

(* Continuous Safety Monitoring (Highest Priority) *)
IF NOT E_Stop_OK OR NOT Motor_Thermal_OK THEN
    bFault_Safety := TRUE;
    state := 99;
END_IF;

IF Crusher_Vibration_mm > MAX_VIBRATION AND state >= 40 THEN
    bFault_Motor := TRUE;
    state := 99;
END_IF;

(* State Machine Execution *)
CASE state OF
    0: (* INIT / STOPPED *)
        State_String := 'STOPPED / READY TO SEQUENCE';
        cmd_Lube_Pump := FALSE;
        cmd_Main_Motor := FALSE;
        System_Ready := FALSE;
        
        IF edge_Start.Q AND NOT bFault_Safety THEN
            state := 10;
        END_IF;
        
    10: (* STARTING LUBE SYSTEM *)
        State_String := 'STARTING LUBE PUMP';
        cmd_Lube_Pump := TRUE;
        
        (* Verify Lube conditions are met *)
        IF fbk_Lube_Pump_Run AND Lube_Pressure_OK THEN
            state := 20;
        END_IF;
        
        (* Add timeout logic if needed... *)
        
    20: (* VERIFYING OIL CONDITION & LUBRICATING *)
        State_String := 'PRE-LUBRICATION & CONDITIONING';
        
        IF (Oil_Temp_C < MIN_OIL_TEMP) OR (Oil_Temp_C > MAX_OIL_TEMP) OR (Oil_Viscosity_cSt > MAX_VISCOSITY) THEN
            (* Wait for heaters/coolers to condition the oil. 
               In a real system, this might trigger a heater. *)
            tmr_LubePreStart.IN := FALSE;
        ELSE
            (* Oil is good, run pre-start timer *)
            tmr_LubePreStart.IN := TRUE;
        END_IF;
        
        IF tmr_LubePreStart.Q THEN
            tmr_LubePreStart.IN := FALSE;
            state := 30;
        END_IF;
        
    30: (* CRITICAL INTERLOCKS CHECK *)
        State_String := 'CHECKING BOWL FLOAT & TRAMP IRON';
        
        IF NOT Bowl_Float_OK OR NOT Tramp_Relief_Valve_OK THEN
            bFault_Interlocks := TRUE;
            state := 99;
        ELSE
            state := 40;
        END_IF;
        
    40: (* STARTING MAIN MOTOR *)
        State_String := 'STARTING MAIN DRIVE MOTOR';
        cmd_Main_Motor := TRUE;
        tmr_DriveSpinup.IN := TRUE;
        
        IF fbk_Main_Motor_Run THEN
            tmr_DriveSpinup.IN := FALSE;
            state := 50;
        ELSIF tmr_DriveSpinup.Q AND NOT fbk_Main_Motor_Run THEN
            (* Failed to spin up *)
            tmr_DriveSpinup.IN := FALSE;
            bFault_Motor := TRUE;
            state := 99;
        END_IF;
        
    50: (* RUNNING & CRUSHING *)
        State_String := 'RUNNING - READY FOR FEED';
        System_Ready := TRUE;
        
        (* Monitor active running faults *)
        IF NOT Lube_Pressure_OK THEN
            bFault_Lube := TRUE;
            state := 99;
        ELSIF NOT Bowl_Float_OK OR NOT Tramp_Relief_Valve_OK THEN
            bFault_Interlocks := TRUE;
            state := 99;
        ELSIF NOT fbk_Main_Motor_Run THEN
            bFault_Motor := TRUE;
            state := 99;
        END_IF;
        
        (* Normal Stop *)
        IF cmd_Stop THEN
            System_Ready := FALSE;
            state := 60;
        END_IF;
        
    60: (* SHUTDOWN SEQUENCE *)
        State_String := 'STOPPING MAIN MOTOR';
        cmd_Main_Motor := FALSE;
        (* Optional: Keep lube pump running for cool down *)
        (* Here we just drop out to 0 immediately for simplicity *)
        IF NOT fbk_Main_Motor_Run THEN
            state := 0;
        END_IF;
        
    99: (* FAULT STATE *)
        State_String := 'FAULT ACTIVE - DRIVE SECURED';
        System_Ready := FALSE;
        cmd_Main_Motor := FALSE;
        cmd_Lube_Pump := FALSE; (* Depending on fault, you might want lube to stay on, but safe default is off *)
        tmr_LubePreStart.IN := FALSE;
        tmr_DriveSpinup.IN := FALSE;
        Alarm_Active := TRUE;
        
        (* Clear alarm output when faults cleared, state handled by reset *)
        IF NOT bFault_Lube AND NOT bFault_Interlocks AND NOT bFault_Motor AND NOT bFault_Safety THEN
            Alarm_Active := FALSE;
        END_IF;
        
    ELSE
        state := 0;
END_CASE;

(* Execute Timers *)
tmr_LubePreStart(PT := T_LUBE_PRE_START);
tmr_DriveSpinup(PT := T_DRIVE_SPINUP);

(* Maintain output states just to be safe *)
Active_State := state;
"""

payload = {
    "messages": [
        {
            "role": "user",
            "content": "Write the PLC logic implementation for a Heavy Mining Cone Crusher lubrication and drive sequencer function block. It should implement tramp iron relief valve interlocks, bowl float monitoring, and oil viscosity/temperature safety checks before permitting the main motor start."
        },
        {
            "role": "assistant",
            "content": plc_code
        }
    ]
}

with open(r"c:\\Users\\majip\\Downloads\\LLM REASEARCH\\data\\evol_instruct_dataset.jsonl", "a") as f:
    f.write(json.dumps(payload) + "\\n")
