import json

user_prompt = """You are acting as a Lead Process Engineer for an Oil Sands Upgrader. Evolve a basic temperature control loop into a highly complex, production-ready Fluid Catalytic Cracking (FCC) Unit Controller in IEC 61131-3 Structured Text.

The system must handle:
1. Catalyst circulation rate control using riser temperature feedback.
2. Regenerator vessel superficial gas velocity tracking and combustion air optimization.
3. Wet gas compressor anti-surge matrices and capacity control.
4. Comprehensive interlock and constraint handling for reactor-regenerator differential pressure.

Provide the complete, enterprise-grade Structured Text implementation including data types, function blocks, and detailed engineering comments."""

assistant_response = """```iecst
(*
================================================================================
FCC_UNIT_CONTROLLER - Fluid Catalytic Cracking Unit Advanced Control System
================================================================================
Lead Process Engineer: [Synthetic Identity]
Facility: Oil Sands Upgrader, Secondary Conversion
Version: 4.2.0 - Enterprise Edition
================================================================================
DESCRIPTION:
Advanced regulatory and constraint controller for an FCC unit. This system 
supervises the thermal balance between the reactor and regenerator, manages 
fluidization regimes, and protects the wet gas compressor (WGC) against surge.

Key Sub-Systems:
1. Riser Temperature Control via Catalyst Circulation (Slide Valve Positioning)
2. Regenerator Superficial Gas Velocity (SGV) and Combustion Air Control
3. Wet Gas Compressor (WGC) Anti-Surge Matrices
4. Reactor-Regenerator Differential Pressure (dP) Constraint Management
================================================================================
*)

TYPE FCC_PROCESS_VARS :
STRUCT
    // Reactor/Riser Variables
    Riser_Top_Temp       : REAL; // [°C] Riser termination temperature
    Reactor_Pressure     : REAL; // [kPag] Reactor overhead pressure
    Feed_Rate            : REAL; // [m3/h] Fresh feed + recycle
    Feed_Preheat_Temp    : REAL; // [°C] Feed temperature
    
    // Regenerator Variables
    Regen_Dense_Temp     : REAL; // [°C] Dense bed temperature
    Regen_Dilute_Temp    : REAL; // [°C] Dilute phase / cyclone temp
    Regen_Pressure       : REAL; // [kPag] Regenerator pressure
    Combustion_Air_Flow  : REAL; // [Nm3/h] Main air blower discharge
    Flue_Gas_O2          : REAL; // [% vol] Excess oxygen in flue gas
    
    // Catalyst Circulation
    Regen_Cat_Slide_Pos  : REAL; // [%] Regenerated catalyst slide valve position
    Spent_Cat_Slide_Pos  : REAL; // [%] Spent catalyst slide valve position
    Rx_Rg_Diff_Press     : REAL; // [kPa] Reactor to Regenerator dP
    
    // Wet Gas Compressor (WGC)
    WGC_Suction_Press    : REAL; // [kPag] WGC suction pressure
    WGC_Discharge_Press  : REAL; // [kPag] WGC discharge pressure
    WGC_Flow             : REAL; // [Nm3/h] WGC actual flow
    WGC_RPM              : REAL; // [RPM] Compressor speed
END_STRUCT;
END_TYPE

TYPE FCC_SETPOINTS :
STRUCT
    Riser_Temp_SP        : REAL; // [°C] Target riser temperature
    Regen_Temp_Max       : REAL; // [°C] Maximum dense bed temp
    SGV_Target           : REAL; // [m/s] Superficial Gas Velocity target
    WGC_Suction_Press_SP : REAL; // [kPag] Wet gas suction target
    Min_Diff_Press       : REAL; // [kPa] Minimum allowable Rx-Rg dP (flow reversal protection)
END_STRUCT;
END_TYPE

TYPE WGC_SURGE_MATRIX :
STRUCT
    Poly_A               : REAL; // Surge line polynomial coefficient A
    Poly_B               : REAL; // Surge line polynomial coefficient B
    Poly_C               : REAL; // Surge line polynomial coefficient C
    Surge_Margin         : REAL; // [%] Safety margin from surge line
    Recycle_Valve_Pos    : REAL; // [%] Anti-surge recycle valve position
END_STRUCT;
END_TYPE

//-----------------------------------------------------------------------------
// FUNCTION BLOCK: FCC_CATALYST_CIRCULATION
// Regulates slide valve to maintain riser temperature while honoring dP constraints
//-----------------------------------------------------------------------------
FUNCTION_BLOCK FCC_CATALYST_CIRCULATION
VAR_INPUT
    Riser_Temp      : REAL;
    Riser_Temp_SP   : REAL;
    Rx_Rg_dP        : REAL;
    Min_dP          : REAL;
    Enable          : BOOL;
    Kp, Ti, Td      : REAL;
END_VAR
VAR_OUTPUT
    Regen_Slide_Val : REAL; // 0-100%
    dP_Override     : BOOL;
END_VAR
VAR
    Error           : REAL;
    Integral        : REAL;
    Derivative      : REAL;
    Prev_Error      : REAL;
    CV_Temp         : REAL;
    dP_Error        : REAL;
    dP_Gain         : REAL := 5.0; // Aggressive override gain
END_VAR

IF NOT Enable THEN
    Integral := 0.0;
    Regen_Slide_Val := 0.0;
    RETURN;
END_IF;

// 1. Primary Temperature Control (PID)
Error := Riser_Temp_SP - Riser_Temp;
Integral := Integral + (Error * Ti);
Integral := LIMIT(0.0, Integral, 100.0); // Anti-windup
Derivative := (Error - Prev_Error) * Td;
Prev_Error := Error;

CV_Temp := (Kp * Error) + Integral + Derivative;
CV_Temp := LIMIT(0.0, CV_Temp, 100.0);

// 2. Differential Pressure Constraint (Flow Reversal Protection)
// If dP drops near the minimum safe limit, override the temperature controller
// to close the slide valve and restore pressure differential.
IF Rx_Rg_dP < (Min_dP + 7.0) THEN
    dP_Error := (Min_dP + 7.0) - Rx_Rg_dP;
    // Reduce valve opening proportionally to the dP violation
    CV_Temp := CV_Temp - (dP_Error * dP_Gain);
    dP_Override := TRUE;
ELSE
    dP_Override := FALSE;
END_IF;

Regen_Slide_Val := LIMIT(5.0, CV_Temp, 95.0); // Hard mechanical limits
END_FUNCTION_BLOCK

//-----------------------------------------------------------------------------
// FUNCTION BLOCK: FCC_REGEN_SGV_CONTROL
// Calculates and tracks Superficial Gas Velocity (SGV) to maintain proper fluidization
//-----------------------------------------------------------------------------
FUNCTION_BLOCK FCC_REGEN_SGV_CONTROL
VAR_INPUT
    Air_Flow        : REAL; // [Nm3/h]
    Regen_Temp      : REAL; // [°C]
    Regen_Press     : REAL; // [kPag]
    Regen_Diameter  : REAL; // [m]
    Target_SGV      : REAL; // [m/s]
END_VAR
VAR_OUTPUT
    Current_SGV     : REAL; // [m/s]
    SGV_Deviation   : REAL; // [m/s]
    Air_Flow_Req    : REAL; // [Nm3/h] Suggested air flow to meet SGV
    Fluidization_OK : BOOL;
END_VAR
VAR
    Cross_Sectional_Area : REAL;
    Actual_Vol_Flow      : REAL;
    Gas_Constant         : REAL := 8.314;
    Std_Temp             : REAL := 273.15; // [K]
    Std_Press            : REAL := 101.325; // [kPa]
    Abs_Regen_Temp       : REAL; // [K]
    Abs_Regen_Press      : REAL; // [kPa]
END_VAR

// Area = pi * (d/2)^2
Cross_Sectional_Area := 3.14159 * (Regen_Diameter / 2.0) * (Regen_Diameter / 2.0);

Abs_Regen_Temp := Regen_Temp + Std_Temp;
Abs_Regen_Press := Regen_Press + Std_Press;

// Convert Standard Flow (Nm3/h) to Actual Flow (m3/s) based on Ideal Gas Law
// P1*V1/T1 = P2*V2/T2  => V2 = V1 * (P1/P2) * (T2/T1)
Actual_Vol_Flow := (Air_Flow / 3600.0) * (Std_Press / Abs_Regen_Press) * (Abs_Regen_Temp / Std_Temp);

// Calculate SGV = Actual Flow / Area
Current_SGV := Actual_Vol_Flow / Cross_Sectional_Area;

SGV_Deviation := Target_SGV - Current_SGV;

// Calculate required air flow to meet Target SGV
Air_Flow_Req := (Target_SGV * Cross_Sectional_Area * 3600.0) * (Abs_Regen_Press / Std_Press) * (Std_Temp / Abs_Regen_Temp);

// Validate fluidization regime (typically 0.7 to 1.2 m/s for bubbling/turbulent beds)
Fluidization_OK := (Current_SGV >= 0.6) AND (Current_SGV <= 1.5);
END_FUNCTION_BLOCK

//-----------------------------------------------------------------------------
// FUNCTION BLOCK: WGC_ANTI_SURGE
// Evaluates compressor operating point against surge curve
//-----------------------------------------------------------------------------
FUNCTION_BLOCK WGC_ANTI_SURGE
VAR_INPUT
    Suction_Press   : REAL;
    Discharge_Press : REAL;
    Vol_Flow        : REAL;
    Matrix          : WGC_SURGE_MATRIX;
END_VAR
VAR_OUTPUT
    Compression_Ratio: REAL;
    Surge_Flow_Lim   : REAL;
    Dist_To_Surge    : REAL;
    Recycle_Vlv_Cmd  : REAL; // 0-100%
END_VAR
VAR
    Abs_Suction   : REAL;
    Abs_Discharge : REAL;
    Control_Line  : REAL;
    Error         : REAL;
    Kp            : REAL := 2.5;
END_VAR

Abs_Suction := Suction_Press + 101.325;
Abs_Discharge := Discharge_Press + 101.325;

IF Abs_Suction > 0.0 THEN
    Compression_Ratio := Abs_Discharge / Abs_Suction;
ELSE
    Compression_Ratio := 1.0;
END_IF;

// Surge flow limit based on empirical polynomial: Q_surge = A*Rc^2 + B*Rc + C
Surge_Flow_Lim := (Matrix.Poly_A * (Compression_Ratio * Compression_Ratio)) + 
                  (Matrix.Poly_B * Compression_Ratio) + 
                  Matrix.Matrix.Poly_C;

// Add safety margin to create the control line
Control_Line := Surge_Flow_Lim * (1.0 + (Matrix.Surge_Margin / 100.0));

Dist_To_Surge := Vol_Flow - Surge_Flow_Lim;

// Proportional-only anti-surge recycle calculation (simplified)
IF Vol_Flow < Control_Line THEN
    Error := Control_Line - Vol_Flow;
    Recycle_Vlv_Cmd := Error * Kp;
    Recycle_Vlv_Cmd := LIMIT(0.0, Recycle_Vlv_Cmd, 100.0);
ELSE
    Recycle_Vlv_Cmd := 0.0;
END_IF;

END_FUNCTION_BLOCK

//-----------------------------------------------------------------------------
// MAIN PROGRAM: FCC_MAIN_SUPERVISOR
//-----------------------------------------------------------------------------
PROGRAM FCC_MAIN_SUPERVISOR
VAR
    PVs             : FCC_PROCESS_VARS;
    SPs             : FCC_SETPOINTS;
    WGC_Surge       : WGC_SURGE_MATRIX;
    
    Cat_Circ_Ctrl   : FCC_CATALYST_CIRCULATION;
    Regen_SGV_Ctrl  : FCC_REGEN_SGV_CONTROL;
    WGC_AS_Ctrl     : WGC_ANTI_SURGE;
    
    // Global Status
    Unit_Trip       : BOOL;
    Alarms          : DWORD;
END_VAR

// 1. Initialize Matrices and Constraints
WGC_Surge.Poly_A := 5.2;
WGC_Surge.Poly_B := 120.4;
WGC_Surge.Poly_C := 850.0;
WGC_Surge.Surge_Margin := 10.0; // 10% safety margin

// 2. Execute Catalyst Circulation Control (Riser Temp -> Slide Valve)
PVs.Rx_Rg_Diff_Press := PVs.Reactor_Pressure - PVs.Regen_Pressure;

Cat_Circ_Ctrl(
    Riser_Temp      := PVs.Riser_Top_Temp,
    Riser_Temp_SP   := SPs.Riser_Temp_SP,
    Rx_Rg_dP        := PVs.Rx_Rg_Diff_Press,
    Min_dP          := SPs.Min_Diff_Press,
    Enable          := NOT Unit_Trip,
    Kp              := 1.2,
    Ti              := 0.5,
    Td              := 0.1
);
PVs.Regen_Cat_Slide_Pos := Cat_Circ_Ctrl.Regen_Slide_Val;

// 3. Execute Regenerator Fluidization Control
Regen_SGV_Ctrl(
    Air_Flow        := PVs.Combustion_Air_Flow,
    Regen_Temp      := PVs.Regen_Dense_Temp,
    Regen_Press     := PVs.Regen_Pressure,
    Regen_Diameter  := 8.5, // 8.5 meters vessel diameter
    Target_SGV      := SPs.SGV_Target
);

// 4. Execute Wet Gas Compressor Anti-Surge
WGC_AS_Ctrl(
    Suction_Press   := PVs.WGC_Suction_Press,
    Discharge_Press := PVs.WGC_Discharge_Press,
    Vol_Flow        := PVs.WGC_Flow,
    Matrix          := WGC_Surge
);
WGC_Surge.Recycle_Valve_Pos := WGC_AS_Ctrl.Recycle_Vlv_Cmd;

// 5. Interlocks & Alarms
IF NOT Regen_SGV_Ctrl.Fluidization_OK THEN
    Alarms.0 := TRUE; // Loss of fluidization alarm
END_IF;

IF Cat_Circ_Ctrl.dP_Override THEN
    Alarms.1 := TRUE; // Slide valve overridden by low dP constraint
END_IF;

IF PVs.Rx_Rg_Diff_Press < (SPs.Min_Diff_Press - 2.0) THEN
    Unit_Trip := TRUE; // Hard trip on critical flow reversal risk
END_IF;

END_PROGRAM
```"""

with open(r'C:\Users\majip\Downloads\LLM REASEARCH\Local_Ollama_Evol_Pipeline\seeds\tier1_enterprise_grade\synthetic_generation_v3_enterprise.jsonl', 'a', encoding='utf-8') as f:
    f.write(json.dumps({"messages": [{"role": "user", "content": user_prompt}, {"role": "assistant", "content": assistant_response}]}) + '\n')
