import json
import os

user_prompt = "You are acting as a Lead Geophysics Engineer. Evolve a basic fluid loop into a Massive Geothermal ORC (Organic Rankine Cycle) Controller. Technical Specs: 1. Isopentane working fluid vaporization pressure optimization based on brine temperature. 2. Radial inflow turbine speed and grid synchronization. 3. Air-cooled condenser fan speed arrays to maximize heat rejection in a desert climate."

assistant_response = """```iecst
(*
* SYSTEM: MASSIVE GEOTHERMAL ORC (ORGANIC RANKINE CYCLE) CONTROLLER
* WORKING FLUID: ISOPENTANE
* ENVIRONMENT: DESERT CLIMATE (EXTREME TEMPERATURE SWINGS)
* 
* TECHNICAL SPECIFICATIONS:
* 1. Isopentane vaporization pressure optimization via brine enthalpy tracking.
* 2. Radial inflow turbine governor control and active grid synchronization.
* 3. Air-cooled condenser (ACC) variable frequency drive (VFD) fan arrays for maximum heat rejection.
*
*)

FUNCTION_BLOCK ORC_GEOTHERMAL_CONTROLLER
VAR_INPUT
    // Commands
    Enable_System : BOOL;
    Grid_Sync_Cmd : BOOL;
    Emergency_Stop : BOOL;
    
    // Brine (Geothermal Source)
    Brine_Temp_In_C : REAL; // Celsius
    Brine_Flow_Rate_kg_s : REAL; 
    
    // Isopentane (Working Fluid)
    Iso_Vap_Press_bar : REAL;
    Iso_Vap_Temp_C : REAL;
    
    // Turbine & Grid
    Turbine_Speed_RPM : REAL;
    Grid_Freq_Hz : REAL;
    Grid_Voltage_V : REAL;
    Gen_Voltage_V : REAL;
    Phase_Angle_Diff_deg : REAL; // Difference between grid and generator
    
    // Condenser & Environment
    Ambient_Temp_C : REAL;
    Condenser_Press_bar : REAL;
END_VAR

VAR_OUTPUT
    // Vaporizer Control
    Vap_Feed_Valve_Pos : REAL; // 0.0 to 100.0 %
    
    // Turbine Control
    Turbine_Gov_Valve_Pos : REAL; // 0.0 to 100.0 %
    Sync_Breaker_Close : BOOL;
    
    // Condenser Fan Array (16 Fans for large scale ACC)
    ACC_Fan_Speeds : ARRAY[1..16] OF REAL; // 0.0 to 100.0 % (VFD Reference)
    
    // System Status
    System_State : INT; // 0=OFF, 1=STARTUP, 2=SYNCING, 3=GENERATING, 4=TRIPPED
    Alarm_Word : DWORD;
END_VAR

VAR
    // Internal States
    State : INT := 0;
    
    // PID for Vaporizer Pressure
    Vap_PID_Kp : REAL := 2.5;
    Vap_PID_Ki : REAL := 0.1;
    Vap_PID_Error : REAL;
    Vap_PID_Integral : REAL := 0.0;
    Target_Vap_Press_bar : REAL;
    
    // PID for Turbine Speed
    Gov_PID_Kp : REAL := 1.8;
    Gov_PID_Ki : REAL := 0.5;
    Gov_PID_Error : REAL;
    Gov_PID_Integral : REAL := 0.0;
    Target_RPM : REAL;
    
    // PID for Condenser Pressure
    Cond_PID_Kp : REAL := 5.0;
    Cond_PID_Ki : REAL := 0.2;
    Cond_PID_Error : REAL;
    Cond_PID_Integral : REAL := 0.0;
    Target_Cond_Press_bar : REAL;
    Base_Fan_Speed : REAL;
    
    // Timers & Triggers
    Sync_Timer : TON;
    Cycle_Time : REAL := 0.05; // 50ms execution cycle
    i : INT;
    
    // Constants
    ISO_CRIT_TEMP_C : REAL := 187.2;
    ISO_CRIT_PRESS_BAR : REAL := 33.7;
    SYNC_RPM_TOLERANCE : REAL := 5.0;
    SYNC_PHASE_TOLERANCE : REAL := 3.0; // Degrees
    SYNC_VOLT_TOLERANCE : REAL := 10.0; // Volts
END_VAR

// -----------------------------------------------------------------------------
// 0. EMERGENCY STOP & FAULT HANDLING
// -----------------------------------------------------------------------------
IF Emergency_Stop THEN
    State := 4; // TRIPPED
    Vap_Feed_Valve_Pos := 0.0;
    Turbine_Gov_Valve_Pos := 0.0;
    Sync_Breaker_Close := FALSE;
    FOR i := 1 TO 16 DO
        ACC_Fan_Speeds[i] := 100.0; // Max cooling during trip
    END_FOR;
    Alarm_Word := Alarm_Word OR 16#00000001; // E-Stop Active
    RETURN;
END_IF;

// -----------------------------------------------------------------------------
// 1. ISOPENTANE VAPORIZATION PRESSURE OPTIMIZATION
// -----------------------------------------------------------------------------
// Optimization target based on empirical saturation curve and Brine Temp
// Antoine-like approximation for Isopentane target pressure to maximize enthalpy extraction
// Target = f(Brine_Temp) taking a pinch point of ~10C into account.
IF Brine_Temp_In_C > 80.0 THEN
    Target_Vap_Press_bar := 1.0 + (Brine_Temp_In_C - 80.0) * 0.25; 
    IF Target_Vap_Press_bar > (ISO_CRIT_PRESS_BAR * 0.9) THEN
        Target_Vap_Press_bar := ISO_CRIT_PRESS_BAR * 0.9; // Sub-critical ORC limit
    END_IF;
ELSE
    Target_Vap_Press_bar := 1.0;
END_IF;

// PI Control for Vaporizer Feed Valve
Vap_PID_Error := Target_Vap_Press_bar - Iso_Vap_Press_bar;
Vap_PID_Integral := Vap_PID_Integral + (Vap_PID_Error * Cycle_Time);

// Anti-windup
IF Vap_PID_Integral > 100.0 THEN Vap_PID_Integral := 100.0; END_IF;
IF Vap_PID_Integral < 0.0 THEN Vap_PID_Integral := 0.0; END_IF;

Vap_Feed_Valve_Pos := (Vap_PID_Kp * Vap_PID_Error) + (Vap_PID_Ki * Vap_PID_Integral);
IF Vap_Feed_Valve_Pos > 100.0 THEN Vap_Feed_Valve_Pos := 100.0; END_IF;
IF Vap_Feed_Valve_Pos < 0.0 THEN Vap_Feed_Valve_Pos := 0.0; END_IF;

// -----------------------------------------------------------------------------
// 2. AIR-COOLED CONDENSER FAN ARRAYS (DESERT CLIMATE)
// -----------------------------------------------------------------------------
// Desert climate: Ambient temps can exceed 45C.
// Target condenser pressure floats with ambient to save parasitic fan load,
// but capped to prevent turbine backpressure trips.
Target_Cond_Press_bar := 1.2 + (Ambient_Temp_C * 0.05);
IF Target_Cond_Press_bar > 4.5 THEN Target_Cond_Press_bar := 4.5; END_IF;

Cond_PID_Error := Condenser_Press_bar - Target_Cond_Press_bar;
Cond_PID_Integral := Cond_PID_Integral + (Cond_PID_Error * Cycle_Time);
IF Cond_PID_Integral > 100.0 THEN Cond_PID_Integral := 100.0; END_IF;
IF Cond_PID_Integral < 0.0 THEN Cond_PID_Integral := 0.0; END_IF;

Base_Fan_Speed := (Cond_PID_Kp * Cond_PID_Error) + (Cond_PID_Ki * Cond_PID_Integral);
IF Base_Fan_Speed > 100.0 THEN Base_Fan_Speed := 100.0; END_IF;
IF Base_Fan_Speed < 0.0 THEN Base_Fan_Speed := 0.0; END_IF;

// Distribute load across 16 fans. To prevent mechanical resonance and even out wear,
// we apply minor offsets per bank.
FOR i := 1 TO 16 DO
    // E.g., outer banks run slightly faster for better airflow in desert crosswinds
    IF (i <= 4) OR (i >= 13) THEN
        ACC_Fan_Speeds[i] := Base_Fan_Speed * 1.05;
    ELSE
        ACC_Fan_Speeds[i] := Base_Fan_Speed;
    END_IF;
    // Enforce limits
    IF ACC_Fan_Speeds[i] > 100.0 THEN ACC_Fan_Speeds[i] := 100.0; END_IF;
    IF ACC_Fan_Speeds[i] < 15.0 THEN ACC_Fan_Speeds[i] := 0.0; END_IF; // Min speed to avoid motor overheating
END_FOR;

// -----------------------------------------------------------------------------
// 3. RADIAL INFLOW TURBINE SPEED AND GRID SYNCHRONIZATION
// -----------------------------------------------------------------------------
Target_RPM := Grid_Freq_Hz * 60.0; // Assuming 2-pole generator direct drive (3600 RPM for 60Hz)

CASE State OF
    0: // OFF
        Turbine_Gov_Valve_Pos := 0.0;
        Sync_Breaker_Close := FALSE;
        IF Enable_System THEN State := 1; END_IF;
        
    1: // STARTUP (Rolling the turbine)
        Gov_PID_Error := Target_RPM - Turbine_Speed_RPM;
        Gov_PID_Integral := Gov_PID_Integral + (Gov_PID_Error * Cycle_Time);
        // Limit integral for startup
        IF Gov_PID_Integral > 30.0 THEN Gov_PID_Integral := 30.0; END_IF;
        IF Gov_PID_Integral < 0.0 THEN Gov_PID_Integral := 0.0; END_IF;
        
        Turbine_Gov_Valve_Pos := (Gov_PID_Kp * Gov_PID_Error) + (Gov_PID_Ki * Gov_PID_Integral);
        
        IF (ABS(Gov_PID_Error) < 100.0) AND Grid_Sync_Cmd THEN
            State := 2; // Move to Sync
        END_IF;
        
    2: // SYNCING (Active Grid Synchronization)
        Gov_PID_Error := Target_RPM - Turbine_Speed_RPM;
        
        // Add phase angle compensation to speed error (slip control)
        // If phase is lagging, speed up slightly. If leading, slow down.
        Gov_PID_Error := Gov_PID_Error + (Phase_Angle_Diff_deg * 0.1); 
        
        Gov_PID_Integral := Gov_PID_Integral + (Gov_PID_Error * Cycle_Time);
        Turbine_Gov_Valve_Pos := (Gov_PID_Kp * Gov_PID_Error) + (Gov_PID_Ki * Gov_PID_Integral);
        
        // Sync Check Conditions
        IF (ABS(Target_RPM - Turbine_Speed_RPM) <= SYNC_RPM_TOLERANCE) AND
           (ABS(Phase_Angle_Diff_deg) <= SYNC_PHASE_TOLERANCE) AND
           (ABS(Grid_Voltage_V - Gen_Voltage_V) <= SYNC_VOLT_TOLERANCE) THEN
            
            Sync_Timer(IN := TRUE, PT := T#500ms); // Must be stable for 500ms
            IF Sync_Timer.Q THEN
                Sync_Breaker_Close := TRUE;
                State := 3; // GENERATING
                Sync_Timer(IN := FALSE, PT := T#500ms);
            END_IF;
        ELSE
            Sync_Timer(IN := FALSE, PT := T#500ms);
        END_IF;
        
    3: // GENERATING (Base Load / Droop Control)
        // Once synced, breaker is closed. The grid dictates the speed.
        // Governor valve now controls Load (MW) based on available vaporization pressure.
        // We use a pressure-load droop.
        IF Iso_Vap_Press_bar > (Target_Vap_Press_bar * 0.95) THEN
            Turbine_Gov_Valve_Pos := Turbine_Gov_Valve_Pos + (0.1 * Cycle_Time); // Ramp up load
        ELSIF Iso_Vap_Press_bar < (Target_Vap_Press_bar * 0.90) THEN
            Turbine_Gov_Valve_Pos := Turbine_Gov_Valve_Pos - (0.5 * Cycle_Time); // Unload quickly if pressure drops
        END_IF;
        
        IF NOT Enable_System THEN
            Sync_Breaker_Close := FALSE;
            State := 0; // Shutdown
        END_IF;
        
    4: // TRIPPED
        IF NOT Emergency_Stop AND NOT Enable_System THEN
            Alarm_Word := 0;
            State := 0;
        END_IF;
END_CASE;

System_State := State;
END_FUNCTION_BLOCK
```"""

item = {
    "messages": [
        {"role": "user", "content": user_prompt},
        {"role": "assistant", "content": assistant_response}
    ]
}

path1 = r"C:\Users\majip\Downloads\LLM REASEARCH\Local_Ollama_Evol_Pipeline\data\synthetic_generation_v3_enterprise.jsonl"
path2 = r"C:\Users\majip\Downloads\LLM REASEARCH\data\synthetic_generation_v3_enterprise.jsonl"

for p in [path1, path2]:
    try:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "a", encoding="utf-8") as f:
            f.write(json.dumps(item) + "\\n")
    except Exception as e:
        pass
