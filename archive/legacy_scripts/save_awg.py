import json, uuid
import os

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Next-Gen Atmospheric Water Generation (AWG) Desiccant Wheel**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Solar-thermal regeneration enthalpy mapping, ambient psychrometric condensation boundary tracking, and ultra-violet LED purification pulsing). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_AWG_DesiccantWheel\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
   record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
   with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
       json.dump(record, f, ensure_ascii=False)
5. SELF-CHECK before saving - verify ALL:
   [ ] Fence is ```iec-st
   [ ] First code line: FUNCTION_BLOCK FB_<name>
   [ ] Has VAR_INPUT section
   [ ] Has VAR_OUTPUT section
   [ ] Has END_IF; or END_CASE;
   [ ] Last code line: END_FUNCTION_BLOCK
   [ ] Closing fence: ```
   [ ] Total chars >= 1500
6. REPLY with: EVOLUTION COMPLETE: Next-Gen Atmospheric Water Generation (AWG) Desiccant Wheel

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_AWG_DesiccantWheel
VAR_INPUT
    (* System Operation & Safety *)
    bEnable                 : BOOL;     (* System master enable signal *)
    bEmergencyStop          : BOOL;     (* Safety relay OK / E-Stop loop *)
    (* Environmental Sensors *)
    rAmbientTemp            : REAL;     (* Ambient Dry Bulb Temperature [°C] *)
    rAmbientHumidity        : REAL;     (* Ambient Relative Humidity [%] *)
    (* Process Feedback Sensors *)
    rDesiccantSatTemp       : REAL;     (* Desiccant adsorption face temperature [°C] *)
    rSolarThermalRegenTemp  : REAL;     (* Solar thermal array output temperature [°C] *)
    rCondenserLevel         : REAL;     (* Water level in the primary condensation tank [mm] *)
END_VAR
VAR_OUTPUT
    (* Actuator Commands & Status *)
    bSystemReady            : BOOL;     (* System ready and safely operational *)
    rWheelSpeedCmd          : REAL;     (* Desiccant wheel rotational speed [RPM] *)
    rRegenBlowerSpeedCmd    : REAL;     (* Regeneration loop blower speed [%] *)
    bUVPurifierEnable       : BOOL;     (* Ultra-Violet LED purification pulsing enable *)
    rControlOutput          : REAL;     (* Main process control indicator [0-100%] *)
    bAlarm                  : BOOL;     (* Fault alarm output *)
    wAlarmCode              : WORD;     (* Hexadecimal fault code for SCADA integration *)
END_VAR
VAR
    (* Internal State & Timers *)
    iState                  : INT := 0; (* Advanced state machine integer *)
    tPreheatTimer           : TON;      (* Pre-heat sequence timer *)
    tUVPulseTimer           : TON;      (* UV LED pulsing control timer *)
    (* Control Variables *)
    rDewPoint               : REAL;     (* Calculated dew point based on Magnus-Tetens approximation *)
    rEnthalpyDelta          : REAL;     (* Enthalpy difference across the regeneration sector *)
    rPID_Error              : REAL;     (* Proportional error for desiccant wheel tracking *)
    rPID_Integral           : REAL;     (* Integral accumulator for wheel tracking *)
    bRegenActive            : BOOL;     (* Internal flag for active thermal regeneration *)
    
    (* Constants *)
    C_ALPHA                 : REAL := 17.625;
    C_BETA                  : REAL := 243.04;
END_VAR

(* === MAIN AWG DESICCANT WHEEL LOGIC === *)

(* 1. Safety Interlocks & Fallback Control *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bAlarm := TRUE;
    wAlarmCode := 16#FFFF; (* E-STOP Fault *)
    rWheelSpeedCmd := 0.0;
    rRegenBlowerSpeedCmd := 0.0;
    bUVPurifierEnable := FALSE;
    rControlOutput := 0.0;
    iState := 999; (* FAULT STATE *)
    RETURN;
END_IF;

(* 2. Psychrometric Boundary Tracking (Dewpoint Approx) *)
(* Using Magnus formula to evaluate atmospheric moisture availability *)
IF rAmbientHumidity > 0.0 AND rAmbientTemp > -20.0 THEN
    rDewPoint := C_BETA * ((C_ALPHA * rAmbientTemp) / (C_BETA + rAmbientTemp) + LN(rAmbientHumidity/100.0)) / 
                 (C_ALPHA - ((C_ALPHA * rAmbientTemp) / (C_BETA + rAmbientTemp) + LN(rAmbientHumidity/100.0)));
ELSE
    rDewPoint := -50.0; (* Invalid reading fallback *)
END_IF;

(* 3. State Machine Operation *)
CASE iState OF
    0: (* IDLE *)
        bSystemReady := TRUE;
        bAlarm := FALSE;
        wAlarmCode := 16#0000;
        IF bEnable AND rDewPoint > 5.0 THEN
            (* Only begin if moisture content is sufficient *)
            iState := 10;
        END_IF;

    10: (* SOLAR THERMAL PREHEAT *)
        bSystemReady := TRUE;
        rRegenBlowerSpeedCmd := 25.0; (* Low speed for initial heating loop *)
        tPreheatTimer(IN := TRUE, PT := T#30S);
        
        IF tPreheatTimer.Q AND (rSolarThermalRegenTemp > 65.0) THEN
            tPreheatTimer(IN := FALSE);
            iState := 20;
        ELSIF tPreheatTimer.Q THEN
            (* Thermal capacity too low *)
            tPreheatTimer(IN := FALSE);
            wAlarmCode := 16#0001; (* Low Solar Temp *)
            iState := 0; 
        END_IF;

    20: (* ADSORPTION & REGENERATION RUNNING *)
        bSystemReady := TRUE;
        
        (* Calculate pseudo-enthalpy delta across wheel *)
        rEnthalpyDelta := (rSolarThermalRegenTemp - rDesiccantSatTemp) * 1.05; 
        
        (* PID Tracking for Wheel Speed (simplified PI loop) *)
        rPID_Error := (rDewPoint * 2.0) - rDesiccantSatTemp;
        rPID_Integral := rPID_Integral + (rPID_Error * 0.01);
        IF rPID_Integral > 50.0 THEN rPID_Integral := 50.0; END_IF;
        IF rPID_Integral < 0.0 THEN rPID_Integral := 0.0; END_IF;
        
        rWheelSpeedCmd := (rPID_Error * 0.5) + (rPID_Integral * 0.1);
        
        (* Clamp Wheel Speed *)
        IF rWheelSpeedCmd > 10.0 THEN
            rWheelSpeedCmd := 10.0;
        ELSIF rWheelSpeedCmd < 0.5 THEN
            rWheelSpeedCmd := 0.5;
        END_IF;

        rRegenBlowerSpeedCmd := 85.0; (* High flow for max extraction *)
        rControlOutput := rWheelSpeedCmd / 10.0 * 100.0;
        
        (* UV Purification Pulsing for condensation tank *)
        tUVPulseTimer(IN := NOT tUVPulseTimer.Q, PT := T#2S);
        IF tUVPulseTimer.ET > T#1S THEN
            bUVPurifierEnable := TRUE;
        ELSE
            bUVPurifierEnable := FALSE;
        END_IF;
        
        IF NOT bEnable THEN
            iState := 30;
        END_IF;

    30: (* COOLDOWN / PURGE *)
        bSystemReady := TRUE;
        rWheelSpeedCmd := 1.0;
        rRegenBlowerSpeedCmd := 50.0;
        bUVPurifierEnable := FALSE;
        
        IF rDesiccantSatTemp < 35.0 THEN
            iState := 0;
        END_IF;
        
    999: (* FAULT HANDLING *)
        bSystemReady := FALSE;
        bAlarm := TRUE;
        rWheelSpeedCmd := 0.0;
        rRegenBlowerSpeedCmd := 0.0;
        bUVPurifierEnable := FALSE;
        IF bEnable = FALSE AND bEmergencyStop THEN
            iState := 0; (* Reset sequence *)
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
```"""

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": code}
    ]
}

filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
