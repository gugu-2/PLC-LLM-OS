import json
import uuid
import os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Utility-Scale Solar Inverter Farm.
Task: Invent a highly complex control scenario for this domain (e.g., Maximum Power Point Tracking (MPPT) array voltage sweeping, IGBT active thermal derating, and grid anti-islanding protection).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."""

code = """```iec-st
FUNCTION_BLOCK FB_SolarInverterControl
TITLE = 'Utility-Scale Solar Inverter Farm Control'
// Description: Highly complex control for multi-megawatt solar inverter.
// Includes Perturb & Observe MPPT, IGBT thermal derating, and anti-islanding protection.

VAR_INPUT
    V_DC_Array      : REAL; // DC bus voltage from solar array (V)
    I_DC_Array      : REAL; // DC current from solar array (A)
    V_Grid_L1       : REAL; // Grid voltage L1-N (V)
    V_Grid_L2       : REAL; // Grid voltage L2-N (V)
    V_Grid_L3       : REAL; // Grid voltage L3-N (V)
    Freq_Grid       : REAL; // Grid frequency (Hz)
    Temp_IGBT       : REAL; // Maximum IGBT heatsink temperature (C)
    Irradiance      : REAL; // Solar irradiance (W/m2)
    Enable_Cmd      : BOOL; // Master enable command
    Reset_Fault     : BOOL; // Fault reset command
END_VAR

VAR_OUTPUT
    PWM_Active      : BOOL; // Inverter switching active
    P_Ref           : REAL; // Active power reference (kW)
    Q_Ref           : REAL; // Reactive power reference (kVAR)
    State_Machine   : INT;  // Current control state
    Fault_Code      : DINT; // Active fault code
    Derate_Factor   : REAL; // Active thermal derating factor (0.0 to 1.0)
END_VAR

VAR
    // MPPT Variables
    P_DC_Actual     : REAL;
    P_DC_Prev       : REAL := 0.0;
    V_DC_Prev       : REAL := 0.0;
    MPPT_Step       : REAL := 2.5; // Voltage step for P&O (V)
    MPPT_V_Ref      : REAL := 1000.0;
    MPPT_Direction  : INT := 1;

    // Anti-Islanding Variables
    Grid_Fault_Timer: REAL := 0.0;
    Grid_Fault_Time_Limit : REAL := 0.16; // 160ms trip time for V/f faults
    Is_Grid_Valid   : BOOL := FALSE;
    V_Grid_Avg      : REAL;

    // Thermal Derating Variables
    Temp_Warn_Limit : REAL := 80.0;
    Temp_Trip_Limit : REAL := 95.0;
    Derate_Slope    : REAL := 0.05; // 5% reduction per degree above warning

    // State Machine
    SM_INIT         : INT := 0;
    SM_STANDBY      : INT := 1;
    SM_STARTUP      : INT := 2;
    SM_MPPT         : INT := 3;
    SM_FAULT        : INT := 99;

    // Clock/Timing
    Cycle_Time      : REAL := 0.01; // 10ms execution cycle
END_VAR

// --- Grid Monitoring and Anti-Islanding (IEEE 1547 / UL 1741) ---
V_Grid_Avg := (V_Grid_L1 + V_Grid_L2 + V_Grid_L3) / 3.0;

IF (V_Grid_Avg < 240.0) OR (V_Grid_Avg > 293.0) OR (Freq_Grid < 59.3) OR (Freq_Grid > 60.5) THEN
    Grid_Fault_Timer := Grid_Fault_Timer + Cycle_Time;
    IF Grid_Fault_Timer >= Grid_Fault_Time_Limit THEN
        Is_Grid_Valid := FALSE;
    END_IF;
ELSE
    Grid_Fault_Timer := 0.0;
    Is_Grid_Valid := TRUE;
END_IF;

// --- IGBT Thermal Derating ---
IF Temp_IGBT >= Temp_Trip_Limit THEN
    Derate_Factor := 0.0; // Complete shutdown
ELSIF Temp_IGBT > Temp_Warn_Limit THEN
    Derate_Factor := 1.0 - ((Temp_IGBT - Temp_Warn_Limit) * Derate_Slope);
    IF Derate_Factor < 0.1 THEN
        Derate_Factor := 0.1; // Minimum output before trip
    END_IF;
ELSE
    Derate_Factor := 1.0;
END_IF;

// --- State Machine ---
CASE State_Machine OF
    SM_INIT:
        PWM_Active := FALSE;
        P_Ref := 0.0;
        Q_Ref := 0.0;
        IF Enable_Cmd THEN
            State_Machine := SM_STANDBY;
        END_IF;

    SM_STANDBY:
        PWM_Active := FALSE;
        IF NOT Is_Grid_Valid THEN
            State_Machine := SM_FAULT;
            Fault_Code := 101; // Grid fault
        ELSIF (V_DC_Array > 600.0) AND Is_Grid_Valid THEN
            State_Machine := SM_STARTUP;
        END_IF;

    SM_STARTUP:
        PWM_Active := TRUE;
        // Soft start logic here (ramp up voltage)
        MPPT_V_Ref := V_DC_Array; // Initialize at open-circuit
        State_Machine := SM_MPPT;

    SM_MPPT:
        IF NOT Is_Grid_Valid THEN
            State_Machine := SM_FAULT;
            Fault_Code := 102; // Islanding detected
        ELSIF Temp_IGBT >= Temp_Trip_Limit THEN
            State_Machine := SM_FAULT;
            Fault_Code := 201; // Overtemperature
        ELSE
            // Perturb & Observe Algorithm
            P_DC_Actual := V_DC_Array * I_DC_Array;
            
            IF (P_DC_Actual - P_DC_Prev) > 10.0 THEN // Significant power change
                IF (V_DC_Array - V_DC_Prev) > 0.0 THEN
                    MPPT_Direction := 1;
                ELSE
                    MPPT_Direction := -1;
                END_IF;
            ELSIF (P_DC_Actual - P_DC_Prev) < -10.0 THEN
                IF (V_DC_Array - V_DC_Prev) > 0.0 THEN
                    MPPT_Direction := -1;
                ELSE
                    MPPT_Direction := 1;
                END_IF;
            END_IF;

            MPPT_V_Ref := MPPT_V_Ref + (REAL_TO_INT(MPPT_Direction) * MPPT_Step);
            
            // Limit MPPT range
            IF MPPT_V_Ref > 1200.0 THEN MPPT_V_Ref := 1200.0; END_IF;
            IF MPPT_V_Ref < 500.0 THEN MPPT_V_Ref := 500.0; END_IF;

            P_DC_Prev := P_DC_Actual;
            V_DC_Prev := V_DC_Array;
            
            // Set power reference based on MPPT and Derating
            P_Ref := (P_DC_Actual / 1000.0) * Derate_Factor; 
        END_IF;

    SM_FAULT:
        PWM_Active := FALSE;
        P_Ref := 0.0;
        IF Reset_Fault AND Is_Grid_Valid AND (Temp_IGBT < Temp_Warn_Limit) THEN
            Fault_Code := 0;
            State_Machine := SM_INIT;
        END_IF;
        
    ELSE
        State_Machine := SM_INIT;
END_CASE;
END_FUNCTION_BLOCK
```"""

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": code}
    ]
}

os.makedirs("data/swarm_raw", exist_ok=True)

with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
    json.dump(record, f, indent=4)

with open("data/synthetic_generation_v3_enterprise.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\\n")
