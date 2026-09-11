import json, uuid, os

prompt = "Invent a highly complex control scenario for Cryogenic Energy Storage (Liquid Air). Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."

code = """
FUNCTION_BLOCK FB_LAES_Liquefaction_Control
TITLE = 'Cryogenic Liquid Air Energy Storage Control'
VERSION : '1.0'
AUTHOR : 'Lumina AI'

VAR_INPUT
    bStart_Liquefaction      : BOOL; // Command to start the liquefaction process
    bEmergency_Stop          : BOOL; // E-Stop, overrides all
    rInletAir_Flow           : REAL; // kg/s
    rInletAir_Temp           : REAL; // K
    rCompStage1_Press        : REAL; // bar
    rCompStage2_Press        : REAL; // bar
    rCompStage3_Press        : REAL; // bar
    rColdBox_Temp            : REAL; // K
    rExpansionTurbine_Speed  : REAL; // RPM
    rCryoTank_Level          : REAL; // %
    rCryoTank_Temp           : REAL; // K
    rCryoTank_Press          : REAL; // bar
    rBoilOff_FlowRate        : REAL; // kg/s
END_VAR

VAR_OUTPUT
    bCompStage1_Run          : BOOL;
    bCompStage2_Run          : BOOL;
    bCompStage3_Run          : BOOL;
    rCompStage1_VFD          : REAL; // 0-100%
    rCompStage2_VFD          : REAL; // 0-100%
    rCompStage3_VFD          : REAL; // 0-100%
    bExpansionTurbine_Run    : BOOL;
    rExpansionTurbine_VIGV   : REAL; // Variable Inlet Guide Vanes 0-100%
    bCryoValve_Inlet_Open    : BOOL;
    bCryoValve_BoilOff_Open  : BOOL;
    rColdBox_CoolingFlow     : REAL; // kg/s
    wSystem_State            : WORD; // 0=Off, 1=Purge, 2=Cooling, 3=Liquefaction, 4=Standby, 99=Fault
    bAlarm                   : BOOL;
    sAlarm_Message           : STRING[80];
END_VAR

VAR
    T_Stage1_Delay           : TON;
    T_Stage2_Delay           : TON;
    T_Stage3_Delay           : TON;
    PID_ColdBox              : PID; // Internal PID for cold box temperature
    PID_TankPress            : PID; // Internal PID for tank pressure management
    rTarget_ColdBoxTemp      : REAL := 80.0; // Target temp in K (approx -193 C)
    rTarget_TankPress        : REAL := 5.0;  // Target storage pressure in bar
    bFault_OverPress         : BOOL;
    bFault_CompSurge         : BOOL;
    bFault_TurbineOverspeed  : BOOL;
    iState                   : INT := 0; 
END_VAR

// Logic Implementation
IF bEmergency_Stop THEN
    // Immediate safe shutdown
    bCompStage1_Run := FALSE;
    bCompStage2_Run := FALSE;
    bCompStage3_Run := FALSE;
    rCompStage1_VFD := 0.0;
    rCompStage2_VFD := 0.0;
    rCompStage3_VFD := 0.0;
    bExpansionTurbine_Run := FALSE;
    rExpansionTurbine_VIGV := 0.0;
    bCryoValve_Inlet_Open := FALSE;
    bCryoValve_BoilOff_Open := TRUE; // Vent boil-off to prevent overpressure
    wSystem_State := 99;
    bAlarm := TRUE;
    sAlarm_Message := 'EMERGENCY STOP ACTIVATED';
    RETURN;
END_IF;

// Fault Detection
bFault_OverPress := (rCryoTank_Press > 10.0);
bFault_CompSurge := (rCompStage1_Press < 1.0 AND rCompStage1_VFD > 50.0);
bFault_TurbineOverspeed := (rExpansionTurbine_Speed > 36000.0);

IF bFault_OverPress OR bFault_CompSurge OR bFault_TurbineOverspeed THEN
    wSystem_State := 99;
    bAlarm := TRUE;
    IF bFault_OverPress THEN sAlarm_Message := 'TANK OVERPRESSURE'; END_IF;
    IF bFault_CompSurge THEN sAlarm_Message := 'COMPRESSOR SURGE DETECTED'; END_IF;
    IF bFault_TurbineOverspeed THEN sAlarm_Message := 'TURBINE OVERSPEED'; END_IF;
    
    // Controlled shutdown
    rCompStage1_VFD := rCompStage1_VFD - 10.0;
    IF rCompStage1_VFD <= 0.0 THEN bCompStage1_Run := FALSE; rCompStage1_VFD := 0.0; END_IF;
    bCryoValve_BoilOff_Open := TRUE;
    RETURN;
END_IF;

// Normal Operations State Machine
CASE iState OF
    0: // OFF
        wSystem_State := 0;
        IF bStart_Liquefaction AND rCryoTank_Level < 95.0 THEN
            iState := 1;
        END_IF;

    1: // PURGE
        wSystem_State := 1;
        bCompStage1_Run := TRUE;
        rCompStage1_VFD := 20.0; // Low speed for purge
        T_Stage1_Delay(IN:=TRUE, PT:=T#5M);
        IF T_Stage1_Delay.Q THEN
            T_Stage1_Delay(IN:=FALSE);
            iState := 2;
        END_IF;

    2: // COOLING
        wSystem_State := 2;
        rCompStage1_VFD := 50.0;
        bCompStage2_Run := TRUE;
        rCompStage2_VFD := 40.0;
        
        bExpansionTurbine_Run := TRUE;
        rExpansionTurbine_VIGV := 30.0;
        
        PID_ColdBox(
            EN := TRUE,
            SP := rTarget_ColdBoxTemp,
            PV := rColdBox_Temp,
            KP := 2.5, KI := 0.5, KD := 0.1,
            CV => rColdBox_CoolingFlow
        );
        
        IF rColdBox_Temp <= (rTarget_ColdBoxTemp + 5.0) THEN
            iState := 3;
        END_IF;

    3: // LIQUEFACTION
        wSystem_State := 3;
        bCompStage3_Run := TRUE;
        rCompStage3_VFD := 80.0;
        rCompStage1_VFD := 90.0;
        rCompStage2_VFD := 85.0;
        rExpansionTurbine_VIGV := 75.0;
        bCryoValve_Inlet_Open := TRUE;
        
        // Continuous Temperature Control
        PID_ColdBox(
            EN := TRUE, SP := rTarget_ColdBoxTemp, PV := rColdBox_Temp,
            CV => rColdBox_CoolingFlow
        );
        
        // Boil-off management
        PID_TankPress(
            EN := TRUE, SP := rTarget_TankPress, PV := rCryoTank_Press,
            KP := 1.0, KI := 0.2, KD := 0.05
        );
        
        IF PID_TankPress.CV > 50.0 THEN
            bCryoValve_BoilOff_Open := TRUE;
        ELSE
            bCryoValve_BoilOff_Open := FALSE;
        END_IF;
        
        IF NOT bStart_Liquefaction OR rCryoTank_Level >= 98.0 THEN
            iState := 4; // Go to Standby
        END_IF;

    4: // STANDBY
        wSystem_State := 4;
        bCompStage1_Run := FALSE;
        bCompStage2_Run := FALSE;
        bCompStage3_Run := FALSE;
        rCompStage1_VFD := 0.0;
        rCompStage2_VFD := 0.0;
        rCompStage3_VFD := 0.0;
        bExpansionTurbine_Run := FALSE;
        bCryoValve_Inlet_Open := FALSE;
        
        // Maintain tank pressure only
        IF rCryoTank_Press > rTarget_TankPress + 1.0 THEN
            bCryoValve_BoilOff_Open := TRUE;
        ELSE
            bCryoValve_BoilOff_Open := FALSE;
        END_IF;
        
        IF bStart_Liquefaction AND rCryoTank_Level < 90.0 THEN
            iState := 1;
        END_IF;
END_CASE;
END_FUNCTION_BLOCK
"""

assistant_content = f"```iec-st\\n{code}\\n```"

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": assistant_content}
    ]
}

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)

os.makedirs("data", exist_ok=True)
with open("data/synthetic_generation_v3_enterprise.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\\n")

print(f"Created file {filename} and appended to synthetic_generation_v3_enterprise.jsonl")
