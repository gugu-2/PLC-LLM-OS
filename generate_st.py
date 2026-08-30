import json
import uuid
import os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Utility-Scale Synchronous Condenser.
Task: Invent a highly complex control scenario for this domain (e.g., stator hydrogen cooling cascades, Automatic Voltage Regulator (AVR) reactive power excitation limits, and flywheel kinetic inertia mapping).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."""

st_code = """```iec-st
FUNCTION_BLOCK FB_SyncCondenser_MasterControl
TITLE = 'Utility-Scale Synchronous Condenser Master Controller'
VERSION : '2.1'
AUTHOR : 'Lumina Elite Data Architect'

VAR_INPUT
    Enable : BOOL; // System Master Enable
    Grid_Voltage_pu : REAL; // Grid voltage in per-unit (0.0 to 1.2)
    Grid_Frequency_Hz : REAL; // Grid frequency in Hz
    ActivePower_MW : REAL; // Active power in MW (losses)
    ReactivePower_MVAR : REAL; // Reactive power in MVAR
    
    // Hydrogen Cooling System
    H2_Pressure_kPa : REAL; // Hydrogen pressure in kPa
    H2_Purity_Pct : REAL; // Hydrogen purity percentage
    Stator_Temp_C : REAL; // Stator winding temperature
    CoolingWater_Flow_Lps : REAL; // Primary cooling water flow
    
    // Flywheel & Inertia
    Rotor_Speed_RPM : REAL; // Current rotor speed
    Vibration_mm_s : REAL; // Shaft vibration level
    
    // AVR & Excitation
    Excitation_Current_A : REAL; // Field current
    Exciter_Temp_C : REAL; // Exciter temperature
    AVR_Setpoint_pu : REAL; // AVR voltage setpoint
END_VAR

VAR_OUTPUT
    System_Ready : BOOL;
    System_Fault : BOOL;
    
    // AVR Control
    Excitation_Target_A : REAL; // Calculated field current target
    AVR_OEL_Active : BOOL; // Over-Excitation Limit active
    AVR_UEL_Active : BOOL; // Under-Excitation Limit active
    
    // Cooling Control
    H2_Makeup_Valve_Open : BOOL; // Hydrogen makeup valve
    Water_Pump_Speed_Pct : REAL; // Cooling water pump VFD command
    
    // Diagnostics
    Inertial_Response_MWs : REAL; // Calculated kinetic energy available
    Fault_Code : INT;
END_VAR

VAR
    // Internal States
    State_Machine : INT; // 0=Off, 1=Startup, 2=Sync, 3=Run, 4=Fault
    Timer_Startup : TON;
    Timer_Cooling : TON;
    
    // AVR Constants
    K_p_AVR : REAL := 2.5;
    K_i_AVR : REAL := 0.5;
    Error_Int : REAL; // Integral accumulator
    OEL_Threshold_A : REAL := 3500.0;
    UEL_Threshold_A : REAL := -1200.0;
    
    // Cooling Constants
    H2_Min_Pressure : REAL := 300.0; // kPa
    H2_Min_Purity : REAL := 95.0; // %
    Stator_Max_Temp : REAL := 120.0; // C
    
    // Inertia Constants
    J_Flywheel : REAL := 45000.0; // kg*m^2
    Omega_Nominal : REAL := 377.0; // rad/s for 60Hz
END_VAR

// ====================================================================
// SYNCHRONOUS CONDENSER CONTROL LOGIC
// ====================================================================

// Fault Detection
System_Fault := FALSE;
Fault_Code := 0;

IF H2_Purity_Pct < H2_Min_Purity THEN
    System_Fault := TRUE;
    Fault_Code := 101; // Hydrogen purity critical
END_IF;

IF Stator_Temp_C > Stator_Max_Temp THEN
    System_Fault := TRUE;
    Fault_Code := 102; // Stator over-temperature
END_IF;

IF Vibration_mm_s > 15.0 THEN
    System_Fault := TRUE;
    Fault_Code := 103; // High vibration
END_IF;

// Hydrogen Cooling Cascade
IF H2_Pressure_kPa < H2_Min_Pressure AND NOT System_Fault THEN
    H2_Makeup_Valve_Open := TRUE;
ELSE
    H2_Makeup_Valve_Open := FALSE;
END_IF;

// Dynamic Cooling Water Control based on Stator Temperature
IF Stator_Temp_C > 80.0 THEN
    Water_Pump_Speed_Pct := 50.0 + (Stator_Temp_C - 80.0) * 1.25;
    IF Water_Pump_Speed_Pct > 100.0 THEN Water_Pump_Speed_Pct := 100.0; END_IF;
ELSE
    Water_Pump_Speed_Pct := 30.0; // Base cooling flow
END_IF;

// Flywheel Kinetic Inertia Mapping
// KE = 0.5 * J * w^2
Inertial_Response_MWs := 0.5 * J_Flywheel * (Rotor_Speed_RPM * 0.104719755) * (Rotor_Speed_RPM * 0.104719755) / 1000000.0;

// Automatic Voltage Regulator (AVR) with Limits
IF Enable AND NOT System_Fault THEN
    System_Ready := TRUE;
    
    // PI Control for Voltage
    VAR
        V_Error : REAL;
        P_Term : REAL;
    END_VAR
    
    V_Error := AVR_Setpoint_pu - Grid_Voltage_pu;
    P_Term := K_p_AVR * V_Error;
    Error_Int := Error_Int + (K_i_AVR * V_Error * 0.1); // Assuming 100ms task cycle
    
    Excitation_Target_A := P_Term + Error_Int;
    
    // Over-Excitation Limit (OEL)
    IF Excitation_Target_A > OEL_Threshold_A THEN
        Excitation_Target_A := OEL_Threshold_A;
        AVR_OEL_Active := TRUE;
        // Anti-windup
        Error_Int := Error_Int - (K_i_AVR * V_Error * 0.1);
    ELSE
        AVR_OEL_Active := FALSE;
    END_IF;
    
    // Under-Excitation Limit (UEL)
    IF Excitation_Target_A < UEL_Threshold_A THEN
        Excitation_Target_A := UEL_Threshold_A;
        AVR_UEL_Active := TRUE;
        // Anti-windup
        Error_Int := Error_Int - (K_i_AVR * V_Error * 0.1);
    ELSE
        AVR_UEL_Active := FALSE;
    END_IF;

ELSE
    System_Ready := FALSE;
    Excitation_Target_A := 0.0;
    Error_Int := 0.0;
    AVR_OEL_Active := FALSE;
    AVR_UEL_Active := FALSE;
    Water_Pump_Speed_Pct := 0.0;
    H2_Makeup_Valve_Open := FALSE;
END_IF;

END_FUNCTION_BLOCK
```"""

record = {'messages': [{'role': 'user', 'content': prompt}, {'role': 'assistant', 'content': st_code}]}

os.makedirs('data/swarm_raw', exist_ok=True)
os.makedirs('data', exist_ok=True)

agent_id = uuid.uuid4().hex[:8]
filename = f'data/swarm_raw/agent_{agent_id}.json'

with open(filename, 'w', encoding='utf-8') as f:
    json.dump(record, f)

with open('data/synthetic_generation_v3_enterprise.jsonl', 'a', encoding='utf-8') as f:
    f.write(json.dumps(record) + '\\n')
    
print('Success')
