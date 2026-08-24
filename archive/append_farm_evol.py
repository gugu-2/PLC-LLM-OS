import json

data = {
    "messages": [
        {
            "role": "user",
            "content": "You are acting as a Lead Agricultural Engineer for an automated Vertical Farm. Evolve a basic light block into a Hyperspectral LED and Hydroponic Dosing Controller. Technical Specs: 1. Multi-channel LED PWM dimming based on crop circadian rhythms. 2. EC (Electrical Conductivity) and pH feedback dosing loops for macro/micro nutrients. 3. HVAC vapor-pressure deficit (VPD) regulation. Provide the complete IEC 61131-3 Structured Text (ST) implementation."
        },
        {
            "role": "assistant",
            "content": """(* 
    TITLE: Hyperspectral LED and Hydroponic Dosing Controller
    VERSION: 3.2.0 (Enterprise Vertical Farm Core)
    AUTHOR: Lead Agricultural Engineer
    DATE: 2026-08-21
*)

TYPE ST_CropCircadianProfile :
STRUCT
    Phase_Dawn_Start : TIME_OF_DAY;
    Phase_Day_Start  : TIME_OF_DAY;
    Phase_Dusk_Start : TIME_OF_DAY;
    Phase_Night_Start: TIME_OF_DAY;
    
    Target_Red_PWM   : ARRAY[0..3] OF REAL; (* 0: Dawn, 1: Day, 2: Dusk, 3: Night *)
    Target_Blue_PWM  : ARRAY[0..3] OF REAL;
    Target_Green_PWM : ARRAY[0..3] OF REAL;
    Target_UV_PWM    : ARRAY[0..3] OF REAL;
    Target_IR_PWM    : ARRAY[0..3] OF REAL;
END_STRUCT
END_TYPE

TYPE ST_HydroponicSensors :
STRUCT
    WaterTemp_C : REAL;
    EC_mS_cm    : REAL;
    pH_Value    : REAL;
    DO_mg_L     : REAL; (* Dissolved Oxygen *)
    FlowRate_Lpm: REAL;
END_STRUCT
END_TYPE

TYPE ST_HVACSensors :
STRUCT
    AirTemp_C   : REAL;
    RelHumidity : REAL;
    CO2_ppm     : REAL;
END_STRUCT
END_TYPE

TYPE ST_DosingActuators :
STRUCT
    Pump_Macro_A_PWM : REAL;
    Pump_Macro_B_PWM : REAL;
    Pump_Micro_PWM   : REAL;
    Pump_pH_Up_PWM   : REAL;
    Pump_pH_Down_PWM : REAL;
END_STRUCT
END_TYPE

TYPE ST_LEDActuators :
STRUCT
    Ch_Red_PWM   : REAL;
    Ch_Blue_PWM  : REAL;
    Ch_Green_PWM : REAL;
    Ch_UV_PWM    : REAL;
    Ch_IR_PWM    : REAL;
END_STRUCT
END_TYPE

TYPE ST_HVACActuators :
STRUCT
    CoolingValve_Pct : REAL;
    HeatingValve_Pct : REAL;
    Humidifier_PWM   : REAL;
    Dehumidifier_PWM : REAL;
    FanSpeed_Pct     : REAL;
END_STRUCT
END_TYPE

FUNCTION_BLOCK FB_VPD_Calculator
VAR_INPUT
    AirTemp_C : REAL;
    RelHumidity : REAL;
END_VAR
VAR_OUTPUT
    VPD_kPa : REAL;
END_VAR
VAR
    SVP : REAL; (* Saturation Vapor Pressure *)
    AVP : REAL; (* Actual Vapor Pressure *)
END_VAR
(* Calculate VPD using Tetens Equation *)
SVP := 0.61078 * EXP((17.27 * AirTemp_C) / (AirTemp_C + 237.3));
AVP := SVP * (RelHumidity / 100.0);
VPD_kPa := SVP - AVP;
END_FUNCTION_BLOCK

FUNCTION_BLOCK FB_PID_Advanced
VAR_INPUT
    Enable : BOOL;
    Setpoint : REAL;
    ProcessValue : REAL;
    Kp : REAL;
    Ki : REAL;
    Kd : REAL;
    CycleTime_s : REAL;
    MinOut : REAL;
    MaxOut : REAL;
END_VAR
VAR_OUTPUT
    Output : REAL;
END_VAR
VAR
    Error : REAL;
    LastError : REAL;
    Integral : REAL;
    Derivative : REAL;
END_VAR
IF NOT Enable THEN
    Output := 0.0;
    Integral := 0.0;
    LastError := ProcessValue;
    RETURN;
END_IF;

Error := Setpoint - ProcessValue;
Integral := Integral + (Error * CycleTime_s);
(* Anti-windup *)
IF Integral > (MaxOut / Ki) THEN Integral := (MaxOut / Ki); END_IF;
IF Integral < (MinOut / Ki) THEN Integral := (MinOut / Ki); END_IF;

Derivative := (Error - LastError) / CycleTime_s;
Output := (Kp * Error) + (Ki * Integral) + (Kd * Derivative);

IF Output > MaxOut THEN Output := MaxOut; END_IF;
IF Output < MinOut THEN Output := MinOut; END_IF;

LastError := Error;
END_FUNCTION_BLOCK

FUNCTION_BLOCK FB_Circadian_LED_Control
VAR_INPUT
    CurrentTime : TIME_OF_DAY;
    Profile : ST_CropCircadianProfile;
    Enable : BOOL;
END_VAR
VAR_OUTPUT
    LED_Out : ST_LEDActuators;
    CurrentPhase : INT; (* 0: Dawn, 1: Day, 2: Dusk, 3: Night *)
END_VAR
VAR
    InterpolationFactor : REAL;
END_VAR

IF NOT Enable THEN
    LED_Out.Ch_Red_PWM := 0.0;
    LED_Out.Ch_Blue_PWM := 0.0;
    LED_Out.Ch_Green_PWM := 0.0;
    LED_Out.Ch_UV_PWM := 0.0;
    LED_Out.Ch_IR_PWM := 0.0;
    RETURN;
END_IF;

(* Determine Current Phase *)
IF CurrentTime >= Profile.Phase_Dawn_Start AND CurrentTime < Profile.Phase_Day_Start THEN
    CurrentPhase := 0;
ELSIF CurrentTime >= Profile.Phase_Day_Start AND CurrentTime < Profile.Phase_Dusk_Start THEN
    CurrentPhase := 1;
ELSIF CurrentTime >= Profile.Phase_Dusk_Start AND CurrentTime < Profile.Phase_Night_Start THEN
    CurrentPhase := 2;
ELSE
    CurrentPhase := 3;
END_IF;

(* Basic step assignment - production version would include linear interpolation over time between phases *)
LED_Out.Ch_Red_PWM   := Profile.Target_Red_PWM[CurrentPhase];
LED_Out.Ch_Blue_PWM  := Profile.Target_Blue_PWM[CurrentPhase];
LED_Out.Ch_Green_PWM := Profile.Target_Green_PWM[CurrentPhase];
LED_Out.Ch_UV_PWM    := Profile.Target_UV_PWM[CurrentPhase];
LED_Out.Ch_IR_PWM    := Profile.Target_IR_PWM[CurrentPhase];

END_FUNCTION_BLOCK

FUNCTION_BLOCK FB_VerticalFarm_Controller
VAR_INPUT
    EnableSystem        : BOOL;
    CurrentTime         : TIME_OF_DAY;
    CycleTime_s         : REAL := 0.1;
    
    CropProfile         : ST_CropCircadianProfile;
    Target_EC           : REAL := 2.0; (* mS/cm *)
    Target_pH           : REAL := 5.8;
    Target_VPD          : REAL := 1.0; (* kPa *)
    
    HydroSensors        : ST_HydroponicSensors;
    HVACSensors         : ST_HVACSensors;
END_VAR
VAR_OUTPUT
    DosingCmd           : ST_DosingActuators;
    LEDCmd              : ST_LEDActuators;
    HVACCmd             : ST_HVACActuators;
    Current_VPD         : REAL;
    SystemFault         : BOOL;
END_VAR
VAR
    inst_LEDControl     : FB_Circadian_LED_Control;
    inst_VPDCalc        : FB_VPD_Calculator;
    
    pid_EC              : FB_PID_Advanced;
    pid_pH              : FB_PID_Advanced;
    pid_VPD             : FB_PID_Advanced;
END_VAR

(* 1. Multi-channel LED PWM dimming based on crop circadian rhythms *)
inst_LEDControl(
    CurrentTime := CurrentTime,
    Profile     := CropProfile,
    Enable      := EnableSystem,
    LED_Out     => LEDCmd
);

(* 2. EC and pH feedback dosing loops for macro/micro nutrients *)
pid_EC(
    Enable := EnableSystem AND HydroSensors.FlowRate_Lpm > 5.0, (* Only dose if flowing *)
    Setpoint := Target_EC,
    ProcessValue := HydroSensors.EC_mS_cm,
    Kp := 10.0, Ki := 0.5, Kd := 1.0,
    CycleTime_s := CycleTime_s,
    MinOut := 0.0, MaxOut := 100.0
);
(* Distribute EC demand across Macro A, Macro B, and Micro *)
DosingCmd.Pump_Macro_A_PWM := pid_EC.Output * 0.45;
DosingCmd.Pump_Macro_B_PWM := pid_EC.Output * 0.45;
DosingCmd.Pump_Micro_PWM   := pid_EC.Output * 0.10;

pid_pH(
    Enable := EnableSystem AND HydroSensors.FlowRate_Lpm > 5.0,
    Setpoint := Target_pH,
    ProcessValue := HydroSensors.pH_Value,
    Kp := 5.0, Ki := 0.2, Kd := 0.5,
    CycleTime_s := CycleTime_s,
    MinOut := -100.0, MaxOut := 100.0
);
(* Split pH control: Negative output -> pH Down, Positive output -> pH Up *)
IF pid_pH.Output < 0.0 THEN
    DosingCmd.Pump_pH_Down_PWM := ABS(pid_pH.Output);
    DosingCmd.Pump_pH_Up_PWM := 0.0;
ELSE
    DosingCmd.Pump_pH_Down_PWM := 0.0;
    DosingCmd.Pump_pH_Up_PWM := pid_pH.Output;
END_IF;

(* 3. HVAC vapor-pressure deficit (VPD) regulation *)
inst_VPDCalc(
    AirTemp_C := HVACSensors.AirTemp_C,
    RelHumidity := HVACSensors.RelHumidity,
    VPD_kPa => Current_VPD
);

pid_VPD(
    Enable := EnableSystem,
    Setpoint := Target_VPD,
    ProcessValue := Current_VPD,
    Kp := 20.0, Ki := 1.5, Kd := 2.0,
    CycleTime_s := CycleTime_s,
    MinOut := -100.0, MaxOut := 100.0
);

(* If VPD is too high (too dry/hot), increase humidity/cooling (negative error) *)
(* If VPD is too low (too wet/cold), decrease humidity/increase heating (positive error) *)
IF pid_VPD.Output > 0.0 THEN
    HVACCmd.Dehumidifier_PWM := pid_VPD.Output;
    HVACCmd.Humidifier_PWM := 0.0;
ELSE
    HVACCmd.Humidifier_PWM := ABS(pid_VPD.Output);
    HVACCmd.Dehumidifier_PWM := 0.0;
END_IF;

(* Basic safety interlocks *)
SystemFault := (HydroSensors.pH_Value < 4.0 OR HydroSensors.pH_Value > 8.0) OR 
               (HydroSensors.EC_mS_cm > 5.0) OR
               (HydroSensors.WaterTemp_C > 30.0);
               
IF SystemFault THEN
    DosingCmd.Pump_Macro_A_PWM := 0.0;
    DosingCmd.Pump_Macro_B_PWM := 0.0;
    DosingCmd.Pump_Micro_PWM := 0.0;
    DosingCmd.Pump_pH_Up_PWM := 0.0;
    DosingCmd.Pump_pH_Down_PWM := 0.0;
END_IF;

END_FUNCTION_BLOCK
"""
        }
    ]
}

filepath = 'c:/Users/majip/Downloads/LLM REASEARCH/Local_Ollama_Evol_Pipeline/seeds/tier1_enterprise_grade/synthetic_generation_v3_enterprise.jsonl'
with open(filepath, 'a', encoding='utf-8') as f:
    f.write(json.dumps(data) + '\\n')
print("Successfully appended to jsonl")
