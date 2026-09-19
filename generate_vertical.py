import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Automated Commercial Vertical Farming Hydroponic Nutrient Dosing and LED Spectrum Shift**

Task: Invent a highly complex, ultra-realistic control scenario for this domain. Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

CRITICAL RULES - READ EVERY LINE:
1. CODE FENCE: Use TRIPLE backticks + iec-st. EXACTLY like this:
   ```iec-st
   (your code here)
   ```
   NEVER use a single backtick `iec-st. ALWAYS use triple backticks.
2. REQUIRED IEC 61131-3 STRUCTURE (all 5 mandatory):
   a. FUNCTION_BLOCK FB_<Name>   <- first line of code, always
   b. VAR_INPUT ... END_VAR      <- min 4 typed inputs with comments
   c. VAR_OUTPUT ... END_VAR     <- min 3 typed outputs with comments
   d. At least one END_IF; or END_CASE;  <- control logic required
   e. END_FUNCTION_BLOCK         <- last line of code, always
3. LENGTH: The assistant content MUST be >= 1500 characters total.
4. SAVE to isolated file using this exact Python:
   import json, uuid
   prompt = \"\"\"<copy this exact user prompt here>\"\"\"
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_VerticalFarm_Control\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
   record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
   with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
       json.dump(record, f, ensure_ascii=False)
5. SELF-CHECK before saving - verify ALL:
...
6. REPLY with: EVOLUTION COMPLETE: Automated Commercial Vertical Farming Hydroponic Nutrient Dosing and LED Spectrum Shift"""

code = """```iec-st
FUNCTION_BLOCK FB_VerticalFarm_HydroLED_Master
VAR_INPUT
    bSystemEnable         : BOOL;      (* Main start/stop command for the farming zone *)
    bEmergencyStop        : BOOL;      (* Safety relay OK signal (E-STOP loop) *)
    rTankLevel_Liters     : REAL;      (* Hydroponic reservoir level in Liters *)
    rEC_Sensor_mS         : REAL;      (* Electrical Conductivity in mS/cm *)
    rpH_Sensor            : REAL;      (* pH measurement of the nutrient solution *)
    rAirTemp_C            : REAL;      (* Ambient air temperature in degrees Celsius *)
    rLightIntensity_PPFD  : REAL;      (* Measured Photosynthetic Photon Flux Density *)
    bPhotoperiodActive    : BOOL;      (* Current time is within the active light cycle *)
END_VAR
VAR_OUTPUT
    bSystemReady          : BOOL;      (* Indicates all interlocks are met and system is running *)
    rDosePump_A_ml        : REAL;      (* Nutrient Part A dosing pump command (ml/min) *)
    rDosePump_B_ml        : REAL;      (* Nutrient Part B dosing pump command (ml/min) *)
    rDosePump_pH_Down_ml  : REAL;      (* pH Down acid dosing pump command (ml/min) *)
    iLED_Red_PWM          : INT;       (* PWM signal (0-10000) for Red spectrum LEDs *)
    iLED_Blue_PWM         : INT;       (* PWM signal (0-10000) for Blue spectrum LEDs *)
    bAlarm_Critical       : BOOL;      (* Critical fault - system shutdown *)
    bAlarm_Warning        : BOOL;      (* Warning flag - non-critical deviation *)
END_VAR
VAR
    iState                : INT := 0;  (* Master State Machine Index *)
    tDosingTimer          : TON;       (* Mixing and stabilization timer *)
    tSpectrumTransition   : TON;       (* Smooth LED spectrum shift timer *)
    rFiltered_EC          : REAL;      (* Exponential moving average of EC *)
    rFiltered_pH          : REAL;      (* Exponential moving average of pH *)
    
    (* Internal constants for filtering and control *)
    ALPHA_FILTER          : REAL := 0.1;
    EC_SETPOINT           : REAL := 1.8;
    PH_SETPOINT           : REAL := 5.8;
    EC_DEADBAND           : REAL := 0.05;
    PH_DEADBAND           : REAL := 0.1;
END_VAR

(* === MAIN LOGIC === *)
(* 1. Safety Interlocks & Emergency Handling *)
IF NOT bEmergencyStop THEN
    bSystemReady         := FALSE;
    bAlarm_Critical      := TRUE;
    rDosePump_A_ml       := 0.0;
    rDosePump_B_ml       := 0.0;
    rDosePump_pH_Down_ml := 0.0;
    iLED_Red_PWM         := 0;
    iLED_Blue_PWM        := 0;
    iState               := 99; (* Fault state *)
    RETURN;
END_IF;

(* 2. Signal Processing (EMA Filtering) *)
rFiltered_EC := (ALPHA_FILTER * rEC_Sensor_mS) + ((1.0 - ALPHA_FILTER) * rFiltered_EC);
rFiltered_pH := (ALPHA_FILTER * rpH_Sensor) + ((1.0 - ALPHA_FILTER) * rFiltered_pH);

(* 3. Reservoir Level Check *)
IF rTankLevel_Liters < 50.0 THEN
    bAlarm_Critical := TRUE;
    iState := 99; (* Dry run protection *)
END_IF;

(* 4. Main State Machine *)
CASE iState OF
    0: (* IDLE *)
        bSystemReady := FALSE;
        IF bSystemEnable AND NOT bAlarm_Critical THEN
            bAlarm_Warning := FALSE;
            iState := 10;
        END_IF;

    10: (* LIGHTING & ENVIRONMENT CONTROL *)
        bSystemReady := TRUE;
        
        (* Adjust LED spectrum based on photoperiod and temperature *)
        IF bPhotoperiodActive THEN
            (* Shift spectrum to cooler light if air temp is high to reduce plant stress *)
            IF rAirTemp_C > 28.0 THEN
                iLED_Red_PWM  := 6000;
                iLED_Blue_PWM := 9000;
            ELSE
                iLED_Red_PWM  := 8500;
                iLED_Blue_PWM := 5000;
            END_IF;
        ELSE
            iLED_Red_PWM  := 0;
            iLED_Blue_PWM := 0;
        END_IF;
        
        iState := 20;

    20: (* NUTRIENT DOSING EVALUATION *)
        IF rFiltered_EC < (EC_SETPOINT - EC_DEADBAND) THEN
            (* Need to add nutrients *)
            rDosePump_A_ml := 5.0; (* Base dose *)
            rDosePump_B_ml := 5.0;
            tDosingTimer(IN := FALSE); (* Reset timer *)
            iState := 30;
        ELSIF rFiltered_pH > (PH_SETPOINT + PH_DEADBAND) THEN
            (* Need to lower pH *)
            rDosePump_pH_Down_ml := 2.0;
            tDosingTimer(IN := FALSE);
            iState := 30;
        ELSE
            (* In deadband *)
            rDosePump_A_ml := 0.0;
            rDosePump_B_ml := 0.0;
            rDosePump_pH_Down_ml := 0.0;
            iState := 10; (* Loop back to lighting control *)
        END_IF;
        
    30: (* DOSING MIXING AND STABILIZATION *)
        (* Run mixing for 60 seconds before re-evaluating *)
        rDosePump_A_ml := 0.0; (* Stop pumps while mixing *)
        rDosePump_B_ml := 0.0;
        rDosePump_pH_Down_ml := 0.0;
        
        tDosingTimer(IN := TRUE, PT := T#60S);
        IF tDosingTimer.Q THEN
            tDosingTimer(IN := FALSE);
            iState := 10; (* Re-evaluate everything *)
        END_IF;
        
    99: (* FAULT STATE *)
        bSystemReady := FALSE;
        rDosePump_A_ml := 0.0;
        rDosePump_B_ml := 0.0;
        rDosePump_pH_Down_ml := 0.0;
        iLED_Red_PWM := 0;
        iLED_Blue_PWM := 0;
        
        IF NOT bEmergencyStop THEN
            (* Waiting for safety reset *)
        ELSIF NOT bSystemEnable THEN
            (* Reset fault via disable *)
            bAlarm_Critical := FALSE;
            iState := 0;
        END_IF;
END_CASE;

END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
