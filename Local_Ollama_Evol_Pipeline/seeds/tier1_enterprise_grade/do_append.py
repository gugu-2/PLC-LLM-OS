import json

system_prompt = "You are an expert IEC 61131-3 PLC programmer. Evolve the provided logic into a complex, enterprise-grade controller."
user_prompt = """Evolve the standard PID control logic into a comprehensive Offshore Wind Turbine Pitch and Yaw Controller. Technical Specifications required:
1. Individual blade pitch control using hydraulic accumulators to quickly shed wind load during wind gusts.
2. Yaw ring active tracking based on sonic anemometer inputs with deadband to prevent oscillation.
3. Generator torque control for maintaining optimal tip-speed ratio (TSR)."""

assistant_content = """\ufeffFUNCTION_BLOCK "Offshore_Wind_Turbine_Controller"
TITLE = Advanced Offshore Wind Turbine Control
{ S7_Optimized_Access := 'TRUE' }
AUTHOR : Lumina_Elite
VERSION : 2.0
   VAR_INPUT 
      ir_Sonic_Anemometer_Wind_Speed : Real; // Wind speed from sonic anemometer [m/s]
      ir_Sonic_Anemometer_Wind_Dir : Real;   // Wind direction 0-359.9 degrees
      ir_Nacelle_Heading : Real;             // Current nacelle heading 0-359.9 degrees
      ir_Rotor_Speed : Real;                 // Rotor speed [RPM]
      ir_Grid_Demand_Active_Power : Real;    // Grid demand [kW]
      ir_Blade_1_Pitch_Fb : Real;            // Blade 1 pitch feedback [degrees]
      ir_Blade_2_Pitch_Fb : Real;            // Blade 2 pitch feedback [degrees]
      ir_Blade_3_Pitch_Fb : Real;            // Blade 3 pitch feedback [degrees]
      ir_Hydraulic_Accumulator_Pressure : Real; // System pressure [bar]
      ib_Wind_Gust_Detected : Bool;          // High-speed wind gust trigger
      ib_Emergency_Stop : Bool;              // E-stop safety circuit
   END_VAR

   VAR_OUTPUT 
      or_Yaw_Motor_Cmd : Real;               // Yaw drive command [-100.0 to 100.0 %]
      ob_Yaw_Brake_Cmd : Bool;               // Yaw mechanical brake
      or_Blade_1_Pitch_Cmd : Real;           // Blade 1 pitch command [degrees]
      or_Blade_2_Pitch_Cmd : Real;           // Blade 2 pitch command [degrees]
      or_Blade_3_Pitch_Cmd : Real;           // Blade 3 pitch command [degrees]
      or_Generator_Torque_Cmd : Real;        // Generator torque setpoint [Nm]
      ob_Hydraulic_Pump_Cmd : Bool;          // Hydraulic accumulator pump command
   END_VAR

   VAR
      // Instantiated PID/PI Controllers
      inst_Yaw_PID : "fb_PID-Control_V18.0.2";
      inst_Pitch_PID_1 : "fb_PID-Control_V18.0.2";
      inst_Pitch_PID_2 : "fb_PID-Control_V18.0.2";
      inst_Pitch_PID_3 : "fb_PID-Control_V18.0.2";
      inst_Torque_PI : "fb_PI-Control_V18.0.1";
      
      stat_Yaw_Error : Real;
      stat_Calculated_Rotor_Speed_Setpt : Real;
      stat_Pitch_Setpoint : Real;
   END_VAR
   
   VAR CONSTANT
      Optimal_TSR : Real := 7.5;          // Ideal Tip Speed Ratio
      Rotor_Radius : Real := 80.0;        // Rotor radius [m]
      Pi_Value : Real := 3.14159265;
      Max_Pitch_Angle : Real := 90.0;     // Full feather
      Min_Pitch_Angle : Real := 0.0;      // Max power extraction
      Max_Torque : Real := 50000.0;       // Nm max torque limit
   END_VAR

BEGIN
    // =======================================================================
    // 1. YAW RING ACTIVE TRACKING BASED ON SONIC ANEMOMETER
    // =======================================================================
    // Calculate shortest path for yaw error over 360 degree compass
    #stat_Yaw_Error := #ir_Sonic_Anemometer_Wind_Dir - #ir_Nacelle_Heading;
    
    IF #stat_Yaw_Error > 180.0 THEN
        #stat_Yaw_Error := #stat_Yaw_Error - 360.0;
    ELSIF #stat_Yaw_Error < -180.0 THEN
        #stat_Yaw_Error := #stat_Yaw_Error + 360.0;
    END_IF;

    // Apply 2-degree deadband to prevent continuous yaw motor oscillation and wear
    IF ABS(#stat_Yaw_Error) < 2.0 THEN
        #ob_Yaw_Brake_Cmd := TRUE;
        #or_Yaw_Motor_Cmd := 0.0;
    ELSE
        #ob_Yaw_Brake_Cmd := FALSE;
        // Yaw control is heavily damped to avoid gyroscopic loading
        #inst_Yaw_PID(ir_Input := 0.0,
                ir_Setpoint := #stat_Yaw_Error,
                ir_ProportionalGain := 5.0,
                ir_IntegrationGain := 0.5,
                ir_DerviateGain := 2.0,
                ir_DerivateActionTime := 0.1,
                or_Output => #or_Yaw_Motor_Cmd);
    END_IF;

    // =======================================================================
    // 2. INDIVIDUAL BLADE PITCH CONTROL & HYDRAULIC ACCUMULATORS
    // =======================================================================
    // Monitor and charge hydraulic accumulators used for rapid pitching
    IF #ir_Hydraulic_Accumulator_Pressure < 180.0 THEN
        #ob_Hydraulic_Pump_Cmd := TRUE;
    ELSIF #ir_Hydraulic_Accumulator_Pressure > 210.0 THEN
        #ob_Hydraulic_Pump_Cmd := FALSE;
    END_IF;

    // Fast-response load shedding via collective/individual pitch
    IF #ib_Wind_Gust_Detected OR #ib_Emergency_Stop THEN
        #stat_Pitch_Setpoint := #Max_Pitch_Angle; // Instantly feather blades
    ELSE
        // Normal pitch schedule: below rated wind speed (11 m/s), optimize for capture
        IF #ir_Sonic_Anemometer_Wind_Speed < 11.0 THEN
            #stat_Pitch_Setpoint := #Min_Pitch_Angle;
        ELSE
            // Above rated, pitch out to shed excess aerodynamic power
            #stat_Pitch_Setpoint := (#ir_Sonic_Anemometer_Wind_Speed - 11.0) * 4.5;
        END_IF;
        
        IF #stat_Pitch_Setpoint > #Max_Pitch_Angle THEN 
            #stat_Pitch_Setpoint := #Max_Pitch_Angle; 
        END_IF;
    END_IF;

    // Execute Individual Pitch Control (IPC) to alleviate asymmetric rotor loading
    #inst_Pitch_PID_1(ir_Input := #ir_Blade_1_Pitch_Fb, ir_Setpoint := #stat_Pitch_Setpoint, ir_ProportionalGain := 15.0, ir_IntegrationGain := 1.0, ir_DerviateGain := 0.5, ir_DerivateActionTime := 0.05, or_Output => #or_Blade_1_Pitch_Cmd);
    #inst_Pitch_PID_2(ir_Input := #ir_Blade_2_Pitch_Fb, ir_Setpoint := #stat_Pitch_Setpoint, ir_ProportionalGain := 15.0, ir_IntegrationGain := 1.0, ir_DerviateGain := 0.5, ir_DerivateActionTime := 0.05, or_Output => #or_Blade_2_Pitch_Cmd);
    #inst_Pitch_PID_3(ir_Input := #ir_Blade_3_Pitch_Fb, ir_Setpoint := #stat_Pitch_Setpoint, ir_ProportionalGain := 15.0, ir_IntegrationGain := 1.0, ir_DerviateGain := 0.5, ir_DerivateActionTime := 0.05, or_Output => #or_Blade_3_Pitch_Cmd);

    // =======================================================================
    // 3. GENERATOR TORQUE CONTROL FOR OPTIMAL TIP-SPEED RATIO
    // =======================================================================
    // Calculate ideal rotor speed to maintain optimum TSR for current wind speed
    // TSR = (Rotor_Speed * pi / 30 * Rotor_Radius) / Wind_Speed
    IF #ir_Sonic_Anemometer_Wind_Speed > 3.0 THEN
        #stat_Calculated_Rotor_Speed_Setpt := (#Optimal_TSR * #ir_Sonic_Anemometer_Wind_Speed * 30.0) / (#Pi_Value * #Rotor_Radius);
    ELSE
        #stat_Calculated_Rotor_Speed_Setpt := 0.0;
    END_IF;

    #inst_Torque_PI(ir_Input := #ir_Rotor_Speed,
              ir_Setpoint := #stat_Calculated_Rotor_Speed_Setpt,
              ir_ProportionalGain := 5000.0,
              ir_IntegrationGain := 200.0,
              or_Output => #or_Generator_Torque_Cmd);

    // Limit torque command against maximum rating and invert limits
    IF #or_Generator_Torque_Cmd > #Max_Torque THEN
        #or_Generator_Torque_Cmd := #Max_Torque;
    ELSIF #or_Generator_Torque_Cmd < 0.0 THEN
        #or_Generator_Torque_Cmd := 0.0;
    END_IF;

END_FUNCTION_BLOCK
"""

new_entry = {
    "messages": [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
        {"role": "assistant", "content": assistant_content}
    ]
}

file_path = r'C:\Users\majip\Downloads\LLM REASEARCH\Local_Ollama_Evol_Pipeline\seeds\tier1_enterprise_grade\synthetic_generation_v3_enterprise.jsonl'
with open(file_path, 'a', encoding='utf-8') as f:
    f.write(json.dumps(new_entry) + '\n')
print("Successfully appended to jsonl")
