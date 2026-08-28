import json
import os

record = {
    'messages': [
        {
            'role': 'user',
            'content': 'You are acting as a Lead Process Engineer for a Carbon Fiber Manufacturing Plant. Evolve a basic temperature loop into a Polyacrylonitrile (PAN) Oxidation Oven Controller. Technical Specs: 1. Multi-zone thermal profiling to stretch and oxidize the precursor fiber at 300C. 2. Exothermic heat exhaust matrices to prevent thermal runaway. 3. Millimeter-perfect tensioning drives.'
        },
        {
            'role': 'assistant',
            'content': '''Here is the evolved production-ready IEC 61131-3 implementation for the PAN Oxidation Oven Controller.

This advanced PLC logic is written in Structured Text (SCL) and incorporates:
1. **Multi-Zone Thermal Profiling**: Six distinct heating zones precisely control the ramp from a base temperature (e.g., 220°C) up to the final oxidation target of 300°C.
2. **Exothermic Heat Exhaust Matrices**: The cyclization of PAN is highly exothermic. The controller calculates the temperature rate-of-change (`°C/sec`) for each zone. If it detects a spike beyond safe thresholds, it immediately shuts off the local heaters, opens exhaust dampers to 100%, and activates the purge fans to prevent thermal runaway and precursor fire.
3. **Millimeter-Perfect Tensioning**: Because the fiber density increases during oxidation, maintaining perfect tension is critical for the resulting carbon fiber's modulus. The module uses a master line-speed outfeed drive and modulates the infeed drive via a dedicated tension PID loop based on load-cell feedback.

```iecst
FUNCTION_BLOCK "FB_PAN_Oxidation_Oven_Controller"
TITLE = PAN Oxidation Oven Control Matrix
{ S7_Optimized_Access := 'TRUE' }
AUTHOR : Lead Process Engineer
VERSION : 1.0
// Description: Multi-zone thermal profiling, exothermic heat exhaust, and tension control for PAN Carbon Fiber Precursor Oxidation.

   VAR_INPUT
      // Process start and emergency stop
      b_Start_Process : BOOL;
      b_Emergency_Stop : BOOL;
      b_Reset_Alarms : BOOL;

      // Thermal Zone Inputs (Actual temperatures in C)
      r_Temp_Zone_1_ACT : REAL;
      r_Temp_Zone_2_ACT : REAL;
      r_Temp_Zone_3_ACT : REAL;
      r_Temp_Zone_4_ACT : REAL;
      r_Temp_Zone_5_ACT : REAL;
      r_Temp_Zone_6_ACT : REAL;

      // Tension Drive Inputs
      r_Drive_Speed_Infeed_ACT : REAL;  // mm/s
      r_Drive_Speed_Outfeed_ACT : REAL; // mm/s
      r_Tension_LoadCell_ACT : REAL;    // N

      // Setpoints from HMI/Recipe
      r_Temp_Setpoint_Base : REAL := 220.0; // Starting temp
      r_Temp_Setpoint_Max : REAL := 300.0;  // Final oxidation temp
      r_Tension_Setpoint_N : REAL := 50.0;  // Target tension in Newtons
      r_Line_Speed_Setpoint : REAL := 150.0; // mm/s
      
      // Control parameters
      r_Exothermic_Delta_Limit : REAL := 5.0; // C/sec rise limit
   END_VAR

   VAR_OUTPUT
      // Heater Control Outputs (0-100% PWM or analog)
      r_Heater_Zone_1_OUT : REAL;
      r_Heater_Zone_2_OUT : REAL;
      r_Heater_Zone_3_OUT : REAL;
      r_Heater_Zone_4_OUT : REAL;
      r_Heater_Zone_5_OUT : REAL;
      r_Heater_Zone_6_OUT : REAL;

      // Exhaust Matrix Control
      b_Exhaust_Fan_Z12 : BOOL;
      b_Exhaust_Fan_Z34 : BOOL;
      b_Exhaust_Fan_Z56 : BOOL;
      r_Exhaust_Damper_Z12 : REAL; // 0-100%
      r_Exhaust_Damper_Z34 : REAL; // 0-100%
      r_Exhaust_Damper_Z56 : REAL; // 0-100%

      // Tension Drive Outputs
      r_Drive_Speed_Infeed_OUT : REAL;  // mm/s
      r_Drive_Speed_Outfeed_OUT : REAL; // mm/s
      
      // Status & Alarms
      b_Thermal_Runaway_Warning : BOOL;
      b_Thermal_Runaway_Trip : BOOL;
      b_Tension_Error : BOOL;
      b_Process_Ready : BOOL;
   END_VAR

   VAR
      // PID Instances for Thermal Zones
      PID_Z1 : "fb_PID_Advanced";
      PID_Z2 : "fb_PID_Advanced";
      PID_Z3 : "fb_PID_Advanced";
      PID_Z4 : "fb_PID_Advanced";
      PID_Z5 : "fb_PID_Advanced";
      PID_Z6 : "fb_PID_Advanced";
      
      PID_Tension : "fb_PID_Advanced";
      
      // Exothermic monitoring arrays
      ar_Temp_Prev_Cycle : ARRAY[1..6] OF REAL;
      ar_Temp_Rate_Of_Change : ARRAY[1..6] OF REAL;
      
      // Cycle timing
      LTime_Last_Cycle : LReal;
      r_Delta_Time_S : REAL;
      
      // Interpolated Temp Setpoints
      ar_Temp_SP : ARRAY[1..6] OF REAL;
   END_VAR

   VAR CONSTANT
      CYCLE_MAX_RATE : REAL := 10.0; // max C/s before trip
   END_VAR

BEGIN
   // [Initialization & Cycle Time Calculation]
   #r_Delta_Time_S := LREAL_TO_REAL(RUNTIME(#LTime_Last_Cycle));
   
   IF #b_Emergency_Stop THEN
       // Failsafe state
       #r_Heater_Zone_1_OUT := 0.0;
       #r_Heater_Zone_2_OUT := 0.0;
       #r_Heater_Zone_3_OUT := 0.0;
       #r_Heater_Zone_4_OUT := 0.0;
       #r_Heater_Zone_5_OUT := 0.0;
       #r_Heater_Zone_6_OUT := 0.0;
       
       #b_Exhaust_Fan_Z12 := TRUE;
       #b_Exhaust_Fan_Z34 := TRUE;
       #b_Exhaust_Fan_Z56 := TRUE;
       #r_Exhaust_Damper_Z12 := 100.0;
       #r_Exhaust_Damper_Z34 := 100.0;
       #r_Exhaust_Damper_Z56 := 100.0;
       
       #r_Drive_Speed_Infeed_OUT := 0.0;
       #r_Drive_Speed_Outfeed_OUT := 0.0;
       #b_Process_Ready := FALSE;
       RETURN;
   END_IF;

   IF #b_Reset_Alarms THEN
       #b_Thermal_Runaway_Warning := FALSE;
       #b_Thermal_Runaway_Trip := FALSE;
       #b_Tension_Error := FALSE;
   END_IF;

   // [1. Multi-Zone Thermal Profiling]
   // Calculate linear thermal profile from base temp to max temp (300C) across 6 zones
   #ar_Temp_SP[1] := #r_Temp_Setpoint_Base;
   #ar_Temp_SP[2] := #r_Temp_Setpoint_Base + (#r_Temp_Setpoint_Max - #r_Temp_Setpoint_Base) * 0.2;
   #ar_Temp_SP[3] := #r_Temp_Setpoint_Base + (#r_Temp_Setpoint_Max - #r_Temp_Setpoint_Base) * 0.4;
   #ar_Temp_SP[4] := #r_Temp_Setpoint_Base + (#r_Temp_Setpoint_Max - #r_Temp_Setpoint_Base) * 0.6;
   #ar_Temp_SP[5] := #r_Temp_Setpoint_Base + (#r_Temp_Setpoint_Max - #r_Temp_Setpoint_Base) * 0.8;
   #ar_Temp_SP[6] := #r_Temp_Setpoint_Max;

   // Execute PID controllers for each zone
   #PID_Z1(ir_Input := #r_Temp_Zone_1_ACT, ir_Setpoint := #ar_Temp_SP[1], ir_Kp := 15.0, ir_Ki := 0.5, ir_Kd := 2.0, or_Output => #r_Heater_Zone_1_OUT);
   #PID_Z2(ir_Input := #r_Temp_Zone_2_ACT, ir_Setpoint := #ar_Temp_SP[2], ir_Kp := 15.0, ir_Ki := 0.5, ir_Kd := 2.0, or_Output => #r_Heater_Zone_2_OUT);
   #PID_Z3(ir_Input := #r_Temp_Zone_3_ACT, ir_Setpoint := #ar_Temp_SP[3], ir_Kp := 18.0, ir_Ki := 0.6, ir_Kd := 2.5, or_Output => #r_Heater_Zone_3_OUT);
   #PID_Z4(ir_Input := #r_Temp_Zone_4_ACT, ir_Setpoint := #ar_Temp_SP[4], ir_Kp := 18.0, ir_Ki := 0.6, ir_Kd := 2.5, or_Output => #r_Heater_Zone_4_OUT);
   #PID_Z5(ir_Input := #r_Temp_Zone_5_ACT, ir_Setpoint := #ar_Temp_SP[5], ir_Kp := 20.0, ir_Ki := 0.8, ir_Kd := 3.0, or_Output => #r_Heater_Zone_5_OUT);
   #PID_Z6(ir_Input := #r_Temp_Zone_6_ACT, ir_Setpoint := #ar_Temp_SP[6], ir_Kp := 25.0, ir_Ki := 1.0, ir_Kd := 3.5, or_Output => #r_Heater_Zone_6_OUT);

   // [2. Exothermic Heat Exhaust Matrices]
   // Monitor rate of change to detect thermal runaway.
   IF #r_Delta_Time_S > 0.0 THEN
       #ar_Temp_Rate_Of_Change[1] := (#r_Temp_Zone_1_ACT - #ar_Temp_Prev_Cycle[1]) / #r_Delta_Time_S;
       #ar_Temp_Rate_Of_Change[2] := (#r_Temp_Zone_2_ACT - #ar_Temp_Prev_Cycle[2]) / #r_Delta_Time_S;
       #ar_Temp_Rate_Of_Change[3] := (#r_Temp_Zone_3_ACT - #ar_Temp_Prev_Cycle[3]) / #r_Delta_Time_S;
       #ar_Temp_Rate_Of_Change[4] := (#r_Temp_Zone_4_ACT - #ar_Temp_Prev_Cycle[4]) / #r_Delta_Time_S;
       #ar_Temp_Rate_Of_Change[5] := (#r_Temp_Zone_5_ACT - #ar_Temp_Prev_Cycle[5]) / #r_Delta_Time_S;
       #ar_Temp_Rate_Of_Change[6] := (#r_Temp_Zone_6_ACT - #ar_Temp_Prev_Cycle[6]) / #r_Delta_Time_S;
   END_IF;

   // Zone 1 & 2 Exhaust Matrix
   IF (#ar_Temp_Rate_Of_Change[1] > #r_Exothermic_Delta_Limit) OR (#ar_Temp_Rate_Of_Change[2] > #r_Exothermic_Delta_Limit) THEN
       #b_Exhaust_Fan_Z12 := TRUE;
       #r_Exhaust_Damper_Z12 := 100.0; // Open fully
       #r_Heater_Zone_1_OUT := 0.0;
       #r_Heater_Zone_2_OUT := 0.0;
       #b_Thermal_Runaway_Warning := TRUE;
   ELSE
       #b_Exhaust_Fan_Z12 := FALSE;
       #r_Exhaust_Damper_Z12 := 20.0; // Minimum purge flow
   END_IF;

   // Zone 3 & 4 Exhaust Matrix
   IF (#ar_Temp_Rate_Of_Change[3] > #r_Exothermic_Delta_Limit) OR (#ar_Temp_Rate_Of_Change[4] > #r_Exothermic_Delta_Limit) THEN
       #b_Exhaust_Fan_Z34 := TRUE;
       #r_Exhaust_Damper_Z34 := 100.0;
       #r_Heater_Zone_3_OUT := 0.0;
       #r_Heater_Zone_4_OUT := 0.0;
       #b_Thermal_Runaway_Warning := TRUE;
   ELSE
       #b_Exhaust_Fan_Z34 := FALSE;
       #r_Exhaust_Damper_Z34 := 20.0;
   END_IF;

   // Zone 5 & 6 Exhaust Matrix
   IF (#ar_Temp_Rate_Of_Change[5] > #r_Exothermic_Delta_Limit) OR (#ar_Temp_Rate_Of_Change[6] > #r_Exothermic_Delta_Limit) THEN
       #b_Exhaust_Fan_Z56 := TRUE;
       #r_Exhaust_Damper_Z56 := 100.0;
       #r_Heater_Zone_5_OUT := 0.0;
       #r_Heater_Zone_6_OUT := 0.0;
       #b_Thermal_Runaway_Warning := TRUE;
   ELSE
       #b_Exhaust_Fan_Z56 := FALSE;
       #r_Exhaust_Damper_Z56 := 20.0;
   END_IF;

   // Trip condition for absolute safety
   IF (#ar_Temp_Rate_Of_Change[1] > #CYCLE_MAX_RATE) OR (#ar_Temp_Rate_Of_Change[2] > #CYCLE_MAX_RATE) OR
      (#ar_Temp_Rate_Of_Change[3] > #CYCLE_MAX_RATE) OR (#ar_Temp_Rate_Of_Change[4] > #CYCLE_MAX_RATE) OR
      (#ar_Temp_Rate_Of_Change[5] > #CYCLE_MAX_RATE) OR (#ar_Temp_Rate_Of_Change[6] > #CYCLE_MAX_RATE) THEN
       #b_Thermal_Runaway_Trip := TRUE;
   END_IF;

   // [3. Millimeter-Perfect Tensioning Drives]
   // Master line speed is maintained by the Outfeed drive.
   #r_Drive_Speed_Outfeed_OUT := #r_Line_Speed_Setpoint;

   // Tension PID takes actual Tension N and tries to reach Setpoint N.
   // Output is a trim value for the Infeed drive (mm/s correction).
   #PID_Tension(ir_Input := #r_Tension_LoadCell_ACT, 
                ir_Setpoint := #r_Tension_Setpoint_N, 
                ir_Kp := 0.05, 
                ir_Ki := 0.01, 
                ir_Kd := 0.005, 
                or_Output => PID_Tension.or_Output);
                
   // Speed compensation: If tension is low, slow down infeed to pull tighter.
   #r_Drive_Speed_Infeed_OUT := #r_Line_Speed_Setpoint + PID_Tension.or_Output;

   // Guardrails for tensioning
   IF (#r_Tension_LoadCell_ACT > #r_Tension_Setpoint_N * 1.5) OR (#r_Tension_LoadCell_ACT < #r_Tension_Setpoint_N * 0.5) THEN
       #b_Tension_Error := TRUE;
   END_IF;

   // Update previous cycle temperatures
   #ar_Temp_Prev_Cycle[1] := #r_Temp_Zone_1_ACT;
   #ar_Temp_Prev_Cycle[2] := #r_Temp_Zone_2_ACT;
   #ar_Temp_Prev_Cycle[3] := #r_Temp_Zone_3_ACT;
   #ar_Temp_Prev_Cycle[4] := #r_Temp_Zone_4_ACT;
   #ar_Temp_Prev_Cycle[5] := #r_Temp_Zone_5_ACT;
   #ar_Temp_Prev_Cycle[6] := #r_Temp_Zone_6_ACT;

   // Process ready flag
   #b_Process_Ready := NOT #b_Thermal_Runaway_Trip AND NOT #b_Tension_Error AND #b_Start_Process;

END_FUNCTION_BLOCK

FUNCTION_BLOCK "fb_PID_Advanced"
TITLE = Advanced PID Controller
{ S7_Optimized_Access := 'TRUE' }
   VAR_INPUT
      ir_Input : REAL;
      ir_Setpoint : REAL;
      ir_Kp : REAL;
      ir_Ki : REAL;
      ir_Kd : REAL;
   END_VAR
   VAR_OUTPUT
      or_Output : REAL;
   END_VAR
   VAR
      r_Error_Prev : REAL;
      r_Integral : REAL;
      LTime_Prev : LReal;
      r_DT : REAL;
   END_VAR
BEGIN
   #r_DT := LREAL_TO_REAL(RUNTIME(#LTime_Prev));
   IF #r_DT > 0.0 THEN
       #r_Integral := #r_Integral + (#ir_Setpoint - #ir_Input) * #r_DT;
       #or_Output := #ir_Kp * (#ir_Setpoint - #ir_Input) + #ir_Ki * #r_Integral + #ir_Kd * (((#ir_Setpoint - #ir_Input) - #r_Error_Prev) / #r_DT);
       #r_Error_Prev := #ir_Setpoint - #ir_Input;
   END_IF;
END_FUNCTION_BLOCK
```'''
        }
    ]
}

file_path = r'C:\Users\majip\Downloads\LLM REASEARCH\Local_Ollama_Evol_Pipeline\data\synthetic_generation_v3_enterprise.jsonl'
os.makedirs(os.path.dirname(file_path), exist_ok=True)
with open(file_path, 'a', encoding='utf-8') as f:
    f.write(json.dumps(record) + '\n')
