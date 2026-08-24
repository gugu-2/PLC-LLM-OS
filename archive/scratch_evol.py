import json
import os

target_file = r"c:\Users\majip\Downloads\LLM REASEARCH\data\evol_instruct_dataset.jsonl"
os.makedirs(os.path.dirname(target_file), exist_ok=True)

prompt = """Evolve a basic temperature loop into a massive Data Center CRAC (Computer Room Air Conditioning) unit controller. Implement hot-aisle/cold-aisle containment pressure balancing, N+1 redundancy failover logic, and PUE (Power Usage Effectiveness) calculation blocks."""

response = """(*
================================================================================
Function Block: CRAC_CONTROLLER
Version: 3.2 (Enterprise Grade)
Description: 
Advanced Computer Room Air Conditioning (CRAC) Unit Controller.
Designed for Tier III/IV Data Centers.

Features:
- Precision Temperature & Humidity Control (PID-based)
- Hot-Aisle/Cold-Aisle Containment Pressure Balancing (VFD Fan Control)
- N+1 Redundancy and Failover Logic for multi-unit clusters
- Real-time PUE (Power Usage Effectiveness) Calculation
- Extensive Safety Interlocks (E-Stop, Fire/Smoke detection, Thermal Overloads, Water Leak)
- State Machine driven (INIT, STANDBY, NORMAL, OVERRIDE, FAULT)

================================================================================
*)
FUNCTION_BLOCK CRAC_CONTROLLER
VAR_INPUT
    // Hardware Abstractions (Sensors)
    ReturnAirTemp       : REAL; // [°C] Return Air Temperature
    SupplyAirTemp       : REAL; // [°C] Supply Air Temperature
    ColdAislePressure   : REAL; // [Pa] Pressure in Cold Aisle
    HotAislePressure    : REAL; // [Pa] Pressure in Hot Aisle
    ReturnAirHumidity   : REAL; // [%RH] Return Air Humidity
    
    // Safety & Interlocks
    E_Stop_Active       : BOOL; // NC contact (TRUE = OK, FALSE = E-STOP)
    FireAlarm_Active    : BOOL; // True = Fire/Smoke detected
    WaterLeak_Detected  : BOOL; // True = Water leak detected under raised floor
    Compressor_Overload : BOOL; // True = Compressor thermal overload
    Fan_Overload        : BOOL; // True = Fan VFD fault / overload
    
    // N+1 Redundancy Signals (Cluster Communication)
    Cluster_Active_Units: INT;  // Number of currently active units in the cluster
    Cluster_Master      : BOOL; // True if this unit is the master
    Failover_Request    : BOOL; // Request from master to start this standby unit
    
    // Power Metering for PUE
    Total_Facility_Power: REAL; // [kW] Total power entering the data center
    IT_Equipment_Power  : REAL; // [kW] Power consumed by IT equipment alone
    CRAC_Power_Draw     : REAL; // [kW] Power drawn by this CRAC unit
    
    // Setpoints
    Temp_Setpoint       : REAL := 22.0; // [°C] Target cold aisle / supply temp
    Pressure_Setpoint   : REAL := 15.0; // [Pa] Differential pressure setpoint
    Humidity_Setpoint   : REAL := 45.0; // [%RH] Target humidity
    
    // User Control
    System_Enable       : BOOL;
    Reset_Faults        : BOOL;
END_VAR

VAR_OUTPUT
    // Actuators
    Compressor_Cmd      : BOOL;  // Command to run the compressor
    ChilledWater_Valve  : REAL;  // [0-100%] Chilled water valve position
    SupplyFan_Speed     : REAL;  // [0-100%] Supply fan VFD speed
    Humidifier_Cmd      : REAL;  // [0-100%] Humidifier capacity
    
    // Status
    Current_State       : INT;   // 0: INIT, 1: STANDBY, 2: NORMAL, 3: FAULT
    Is_Failed           : BOOL;  // Indicates unit has failed
    Available_For_N1    : BOOL;  // Indicates unit is healthy and available as standby
    
    // Analytics
    Current_PUE         : REAL;  // Calculated PUE for the facility
    Cooling_Capacity    : REAL;  // [kW] Estimated cooling being delivered
    
    // Alarms
    Alarm_Code          : WORD;  // Bitfield for active alarms
END_VAR

VAR
    // Internal State Machine
    State               : INT := 0; 
    
    // Timers
    Startup_Delay       : TON;
    Compressor_AntiCycle: TON;
    
    // PID Controllers (Abstracted via standard blocks)
    Temp_PID            : PID_CONTROLLER; 
    Pressure_PID        : PID_CONTROLLER;
    Humidity_PID        : PID_CONTROLLER;
    
    // Internal Variables
    Diff_Pressure       : REAL;
    Safety_OK           : BOOL;
END_VAR

// =============================================================================
// 1. SAFETY & INTERLOCK LOGIC
// =============================================================================
// Evaluate all safety conditions. (E-Stop is fail-safe NC, others are NO)
Safety_OK := E_Stop_Active AND NOT FireAlarm_Active AND NOT WaterLeak_Detected 
             AND NOT Compressor_Overload AND NOT Fan_Overload;

IF NOT Safety_OK THEN
    State := 3; // FAULT STATE
    
    // Set Alarm Bits for Diagnostics
    Alarm_Code.0 := NOT E_Stop_Active;
    Alarm_Code.1 := FireAlarm_Active;
    Alarm_Code.2 := WaterLeak_Detected;
    Alarm_Code.3 := Compressor_Overload;
    Alarm_Code.4 := Fan_Overload;
    
    Is_Failed := TRUE;
    Available_For_N1 := FALSE;
ELSIF Reset_Faults AND Safety_OK THEN
    State := 0; // Return to INIT after reset
    Is_Failed := FALSE;
    Alarm_Code := 0;
END_IF;

// =============================================================================
// 2. STATE MACHINE
// =============================================================================
CASE State OF
    0: // INIT
        Compressor_Cmd := FALSE;
        ChilledWater_Valve := 0.0;
        SupplyFan_Speed := 0.0;
        Humidifier_Cmd := 0.0;
        
        // Wait 10 seconds before transitioning to STANDBY
        Startup_Delay(IN := System_Enable AND Safety_OK, PT := T#10s);
        IF Startup_Delay.Q THEN
            State := 1; 
        END_IF;
        
    1: // STANDBY
        Available_For_N1 := TRUE;
        Compressor_Cmd := FALSE;
        ChilledWater_Valve := 0.0;
        SupplyFan_Speed := 10.0; // Keep fan at minimum to sample air
        
        // Transition to NORMAL if commanded by cluster master or standalone
        IF (Cluster_Master OR Failover_Request) THEN
            State := 2;
        END_IF;
        
        IF NOT System_Enable THEN State := 0; END_IF;

    2: // NORMAL OPERATION
        Available_For_N1 := FALSE;
        
        // ---------------------------------------------------------------------
        // A. Hot-Aisle / Cold-Aisle Containment Pressure Balancing
        // ---------------------------------------------------------------------
        // Maintain positive pressure in the cold aisle relative to the hot aisle
        // to prevent hot air recirculation and optimize cooling efficiency.
        Diff_Pressure := ColdAislePressure - HotAislePressure;
        
        Pressure_PID(
            ProcessVariable := Diff_Pressure,
            Setpoint := Pressure_Setpoint,
            Kp := 1.5, Ki := 0.2, Kd := 0.05,
            OutputMin := 20.0, OutputMax := 100.0, // Minimum fan speed 20%
            ControlOutput => SupplyFan_Speed
        );

        // ---------------------------------------------------------------------
        // B. Temperature Control Loop
        // ---------------------------------------------------------------------
        // Primary cooling via Chilled Water Valve
        Temp_PID(
            ProcessVariable := SupplyAirTemp,
            Setpoint := Temp_Setpoint,
            Kp := 2.0, Ki := 0.5, Kd := 0.1,
            OutputMin := 0.0, OutputMax := 100.0,
            ControlOutput => ChilledWater_Valve
        );
        
        // Secondary cooling via DX Compressor (with Anti-short cycle logic)
        Compressor_AntiCycle(IN := NOT Compressor_Cmd, PT := T#5m);
        IF (SupplyAirTemp > Temp_Setpoint + 2.0) AND Compressor_AntiCycle.Q THEN
            Compressor_Cmd := TRUE;
        ELSIF (SupplyAirTemp < Temp_Setpoint - 1.0) THEN
            Compressor_Cmd := FALSE;
        END_IF;

        // ---------------------------------------------------------------------
        // C. Humidity Control Loop
        // ---------------------------------------------------------------------
        Humidity_PID(
            ProcessVariable := ReturnAirHumidity,
            Setpoint := Humidity_Setpoint,
            Kp := 1.0, Ki := 0.1, Kd := 0.0,
            OutputMin := 0.0, OutputMax := 100.0,
            ControlOutput => Humidifier_Cmd
        );
        
        // Check if failover condition is lifted
        IF NOT Cluster_Master AND NOT Failover_Request THEN
            State := 1; // Return to STANDBY
        END_IF;

    3: // FAULT
        // Safe shutdown of all mechanicals
        Compressor_Cmd := FALSE;
        ChilledWater_Valve := 100.0; // Fail-safe open to allow natural cooling
        SupplyFan_Speed := 0.0;
        Humidifier_Cmd := 0.0;

END_CASE;

Current_State := State;

// =============================================================================
// 3. PUE (Power Usage Effectiveness) CALCULATION
// =============================================================================
// PUE = Total Facility Power / IT Equipment Power
// Ideal PUE is 1.0. A typical modern data center targets < 1.2
IF IT_Equipment_Power > 0.0 THEN
    Current_PUE := Total_Facility_Power / IT_Equipment_Power;
ELSE
    Current_PUE := 0.0; // Prevent division by zero
END_IF;

// Cooling Capacity Estimation (Simplified sensible heat formula)
// Capacity (kW) = Airflow (m3/s) * Air Density * Specific Heat * dT
// Note: SupplyFan_Speed * 0.05 is a mock conversion from % to m3/s for demonstration
Cooling_Capacity := (SupplyFan_Speed * 0.05) * 1.2 * 1.006 * (ReturnAirTemp - SupplyAirTemp);
IF Cooling_Capacity < 0.0 THEN Cooling_Capacity := 0.0; END_IF;

END_FUNCTION_BLOCK
"""

data = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": response}
    ]
}

with open(target_file, "a", encoding="utf-8") as f:
    f.write(json.dumps(data) + "\n")

print("Successfully written to", target_file)
