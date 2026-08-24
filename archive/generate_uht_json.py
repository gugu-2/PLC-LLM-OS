import json
import os

prompt = "You are acting as a Lead Process Engineer for a massive Dairy Plant. Evolve a basic thermal loop into an UHT (Ultra-High Temperature) Milk Sterilization Controller. Technical Specs: 1. Direct steam injection to reach 140C for exactly 3 seconds. 2. Flash vacuum cooling vessel pressure control to remove the injected steam water. 3. Aseptic homogenization pressure profiling."

response = """(*
    UHT (Ultra-High Temperature) Milk Sterilization Controller
    Architecture: Direct Steam Injection -> Holding Tube -> Flash Vacuum Cooling -> Aseptic Homogenizer
    Standard: IEC 61131-3 Structured Text
    Role: Lead Process Engineer
*)
FUNCTION_BLOCK UHT_Sterilization_Controller
VAR_INPUT
    Enable_System           : BOOL;  // System start command
    Flow_Rate_LPH           : REAL;  // Liters per hour of raw milk
    Temp_Raw_Milk           : REAL;  // Temperature before steam injection (C)
    Temp_Steam_Inj_Out      : REAL;  // Temperature after steam injection (C)
    Flash_Vessel_Press      : REAL;  // Absolute pressure in flash vessel (Bar)
    Flash_Vessel_Temp       : REAL;  // Temperature in flash vessel (C)
    Homogenizer_P1_Actual   : REAL;  // 1st stage pressure actual (Bar)
    Homogenizer_P2_Actual   : REAL;  // 2nd stage pressure actual (Bar)
    Steam_Supply_Press      : REAL;  // Steam header pressure
END_VAR

VAR_OUTPUT
    Steam_Valve_CV          : REAL;  // 0-100% Control valve for direct steam injection
    Vacuum_Pump_Speed       : REAL;  // 0-100% VFD for flash vacuum vessel
    Vacuum_Bleed_Valve      : REAL;  // 0-100% Fine pressure control for flash vessel
    Homogenizer_P1_CV       : REAL;  // 0-100% 1st stage homogenization valve
    Homogenizer_P2_CV       : REAL;  // 0-100% 2nd stage homogenization valve
    Divert_Valve_Active     : BOOL;  // TRUE = divert to drain/rework, FALSE = forward flow
    System_Status           : STRING; // Current state description
    Alarm_Sterilization     : BOOL;  // Sterilization failure alarm
END_VAR

VAR
    // Constants
    TARGET_STERIL_TEMP      : REAL := 140.0; // 140 C required
    HOLD_TIME_SEC           : REAL := 3.0;   // 3 seconds hold time
    WATER_LATENT_HEAT       : REAL := 2257.0; // kJ/kg roughly
    SPECIFIC_HEAT_MILK      : REAL := 3.93;   // kJ/kg.K roughly
    HOMO_P1_TARGET          : REAL := 200.0; // 200 Bar stage 1
    HOMO_P2_TARGET          : REAL := 50.0;  // 50 Bar stage 2
    
    // PIDs
    PID_Steam_Injection     : PID;
    PID_Vacuum_Press        : PID;
    PID_Homo_Stage1         : PID;
    PID_Homo_Stage2         : PID;
    
    // Internal States
    Hold_Timer              : TON;
    Temp_Is_Valid           : BOOL;
    Holding_Volume_L        : REAL := 1.25; // Example holding tube volume
    Calculated_Hold_Time    : REAL;
    
    // Flash Vessel Math
    Target_Flash_Press      : REAL;
    Delta_T_Heating         : REAL;
    Water_Added_kg_hr       : REAL;
    
    State                   : INT := 0; 
END_VAR

// Calculate dynamic hold time based on flow rate (LPH -> L/sec)
IF Flow_Rate_LPH > 0.0 THEN
    Calculated_Hold_Time := Holding_Volume_L / (Flow_Rate_LPH / 3600.0);
ELSE
    Calculated_Hold_Time := 0.0;
END_IF

CASE State OF
    0: // OFF
        Steam_Valve_CV := 0.0;
        Vacuum_Pump_Speed := 0.0;
        Vacuum_Bleed_Valve := 100.0; // open bleed
        Homogenizer_P1_CV := 0.0;
        Homogenizer_P2_CV := 0.0;
        Divert_Valve_Active := TRUE; // Safe state
        System_Status := 'OFFLINE';
        IF Enable_System THEN
            State := 10;
        END_IF
        
    10: // STARTUP & PRE-STERILIZATION (Water Phase)
        System_Status := 'PRE-STERILIZATION';
        // (Pre-sterilization sequence omitted for brevity, assuming complete)
        State := 20;
        
    20: // PRODUCTION
        System_Status := 'PRODUCTION - UHT ACTIVE';
        
        // 1. Direct Steam Injection Control
        // PID loop to maintain 140C at injection exit
        PID_Steam_Injection(
            ACTUAL := Temp_Steam_Inj_Out,
            SET_POINT := TARGET_STERIL_TEMP,
            KP := 2.5, KI := 0.8, KD := 0.1,
            OUT => Steam_Valve_CV
        );
        
        // Safety Interlock: Verify Sterilization
        Temp_Is_Valid := (Temp_Steam_Inj_Out >= TARGET_STERIL_TEMP);
        
        Hold_Timer(IN := Temp_Is_Valid, PT := T#3s); // Ensure it's met for required time
        
        // Flow rate must support exact 3 seconds hold. 
        // If flow is too fast, hold time < 3s, which is a critical failure.
        IF (Calculated_Hold_Time < HOLD_TIME_SEC) OR NOT Temp_Is_Valid THEN
            Alarm_Sterilization := TRUE;
            Divert_Valve_Active := TRUE; // Divert unsterile product
        ELSE
            Alarm_Sterilization := FALSE;
            Divert_Valve_Active := FALSE; // Forward to aseptic tank
        END_IF
        
        // 2. Flash Vacuum Cooling Control
        // To remove exactly the amount of water added by direct steam, the product must be flash cooled
        // to exactly the temperature it was before steam injection (Temp_Raw_Milk).
        // Vapor pressure of water dictates the boiling point in the vacuum vessel.
        // We use Antoine equation or lookup table approximation to set target pressure based on Temp_Raw_Milk.
        
        // Simplified target pressure curve mapping (Temp in C -> Press in Bar Absolute)
        Target_Flash_Press := 0.01 * EXP(0.05 * Temp_Raw_Milk); // Mock curve fit
        
        PID_Vacuum_Press(
            ACTUAL := Flash_Vessel_Press,
            SET_POINT := Target_Flash_Press,
            KP := 5.0, KI := 1.2, KD := 0.5,
            OUT => Vacuum_Pump_Speed
        );
        // Inverse for bleed valve
        Vacuum_Bleed_Valve := 100.0 - Vacuum_Pump_Speed; 
        
        // 3. Aseptic Homogenizer Pressure Profiling
        // Stage 2 must be controlled first to maintain backpressure, then Stage 1.
        PID_Homo_Stage2(
            ACTUAL := Homogenizer_P2_Actual,
            SET_POINT := HOMO_P2_TARGET,
            KP := 1.5, KI := 0.5, KD := 0.0,
            OUT => Homogenizer_P2_CV
        );
        
        PID_Homo_Stage1(
            ACTUAL := Homogenizer_P1_Actual,
            SET_POINT := HOMO_P1_TARGET,
            KP := 2.0, KI := 0.7, KD := 0.0,
            OUT => Homogenizer_P1_CV
        );
        
        IF NOT Enable_System THEN
            State := 0;
        END_IF
END_CASE;
END_FUNCTION_BLOCK
"""

data = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": response}
    ]
}

target_file = "C:\\Users\\majip\\Downloads\\LLM REASEARCH\\Local_Ollama_Evol_Pipeline\\seeds\\tier1_enterprise_grade\\synthetic_generation_v3_enterprise.jsonl"
with open(target_file, "a", encoding="utf-8") as f:
    f.write(json.dumps(data) + "\n")
print("Done appending to JSONL")
