import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Autonomous Stratospheric Balloon Payload Gondola Thermal Management**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Diurnal extreme temperature swing compensation (-70C to +40C), ammonia loop capillary pumped heat pipe routing, and avionics freeze-protection louver actuations). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_StratosphericBalloon_Thermal\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
   record = {\"messages\": [{\"role\": \"user\", \"content\": prompt}, {\"role\": \"assistant\", \"content\": code}]}
   with open(f\"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json\", \"w\", encoding=\"utf-8\") as f:
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
6. REPLY with: EVOLUTION COMPLETE: Autonomous Stratospheric Balloon Payload Gondola Thermal Management

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_StratoBalloon_Thermal_Mgmt
VAR_INPUT
    bEnable                 : BOOL;     (* System master enable signal *)
    bEmergencyStop          : BOOL;     (* Hardware E-stop or critical fault *)
    rAvionicsTemp_C         : REAL;     (* Gondola internal avionics temp [-80 to +80] *)
    rAmbientTemp_C          : REAL;     (* Stratospheric ambient temp [-90 to +50] *)
    rAmmoniaLoopPress_Bar   : REAL;     (* Capillary pumped heat pipe pressure *)
    rSolarIrradiance_W_m2   : REAL;     (* External solar radiation input *)
    bOverrideManual         : BOOL;     (* Manual ground control override *)
    rOverrideLouverPos      : REAL;     (* Commanded override louver position 0-100% *)
END_VAR
VAR_OUTPUT
    bSystemHealthy          : BOOL;     (* Thermal management system nominal *)
    rLouverPosition_Pct     : REAL;     (* Active thermal louver position 0-100% *)
    rHeaterPower_Pct        : REAL;     (* Survival heater PWM duty cycle 0-100% *)
    bAmmoniaValveOpen       : BOOL;     (* Capillary heat pipe circulation valve *)
    bCriticalAlarm          : BOOL;     (* Fault condition requiring payload safing *)
END_VAR
VAR
    iControlState           : INT := 0; 
    tCycleTimer             : TON;
    tFaultTimer             : TON;
    rFilteredAvionicsTemp   : REAL := 20.0;
    rFilteredAmbientTemp    : REAL := 20.0;
    rTempError              : REAL;
    rProportional           : REAL;
    rIntegral               : REAL := 0.0;
    rDerivative             : REAL;
    rLastTempError          : REAL := 0.0;
    rKp                     : REAL := 5.5;
    rKi                     : REAL := 0.12;
    rKd                     : REAL := 15.0;
    rPID_Output             : REAL;
    ALPHA_FILTER            : REAL := 0.05; (* Low-pass filter constant *)
END_VAR

(* === SENSOR NOISE FILTERING === *)
(* Applying exponential moving average to filter sensor noise in stratospheric environment *)
rFilteredAvionicsTemp := (ALPHA_FILTER * rAvionicsTemp_C) + ((1.0 - ALPHA_FILTER) * rFilteredAvionicsTemp);
rFilteredAmbientTemp  := (ALPHA_FILTER * rAmbientTemp_C) + ((1.0 - ALPHA_FILTER) * rFilteredAmbientTemp);

(* === MULTI-LAYERED SAFETY INTERLOCKS === *)
IF NOT bEnable OR bEmergencyStop OR (rAmmoniaLoopPress_Bar > 45.0) THEN
    (* FAIL-SAFE MODE: Protect avionics from freeze and overpressure *)
    bSystemHealthy := FALSE;
    bCriticalAlarm := TRUE;
    iControlState := 99;
    bAmmoniaValveOpen := TRUE; (* Relieve pressure / allow max passive cooling *)
    rLouverPosition_Pct := 0.0; (* Close louvers to retain remaining heat if in deep cold *)
    rHeaterPower_Pct := 0.0;
    RETURN;
END_IF;

bCriticalAlarm := FALSE;

(* === MAIN STATE MACHINE === *)
CASE iControlState OF
    0: (* INIT AND SYSTEM CHECK *)
        bSystemHealthy := FALSE;
        rLouverPosition_Pct := 0.0;
        rHeaterPower_Pct := 0.0;
        bAmmoniaValveOpen := FALSE;
        rIntegral := 0.0; (* Reset PID integral *)
        
        IF bEnable AND (rAmmoniaLoopPress_Bar < 40.0) THEN
            iControlState := 10;
        END_IF;

    10: (* DIURNAL EXTREME TEMPERATURE COMPENSATION *)
        bSystemHealthy := TRUE;
        
        (* Calculate PID Error (Target Avionics Temp is +15.0C) *)
        rTempError := 15.0 - rFilteredAvionicsTemp;
        
        (* Advanced PID Calculation *)
        rProportional := rKp * rTempError;
        rIntegral := rIntegral + (rKi * rTempError);
        
        (* Anti-windup protection for Integral *)
        IF rIntegral > 100.0 THEN rIntegral := 100.0; END_IF;
        IF rIntegral < -100.0 THEN rIntegral := -100.0; END_IF;
        
        rDerivative := rKd * (rTempError - rLastTempError);
        rLastTempError := rTempError;
        
        rPID_Output := rProportional + rIntegral + rDerivative;
        
        (* Mode Splitter based on Ambient and Solar Irradiance *)
        IF rFilteredAvionicsTemp < 5.0 THEN
            (* CRITICAL COLD: Deep space / eclipse phase -70C *)
            rLouverPosition_Pct := 0.0; (* Completely closed *)
            bAmmoniaValveOpen := FALSE; (* Stop heat rejection to radiator *)
            
            (* Custom LIMIT function equivalent *)
            IF rPID_Output < 0.0 THEN rHeaterPower_Pct := 0.0;
            ELSIF rPID_Output > 100.0 THEN rHeaterPower_Pct := 100.0;
            ELSE rHeaterPower_Pct := rPID_Output; END_IF;
            
        ELSIF rFilteredAvionicsTemp > 35.0 THEN
            (* EXCESS HEAT: Direct sun albedo + avionics max load *)
            IF -rPID_Output < 0.0 THEN rLouverPosition_Pct := 0.0;
            ELSIF -rPID_Output > 100.0 THEN rLouverPosition_Pct := 100.0;
            ELSE rLouverPosition_Pct := -rPID_Output; END_IF;
            
            bAmmoniaValveOpen := TRUE; (* Start capillary pumped loop *)
            rHeaterPower_Pct := 0.0;
        ELSE
            (* NOMINAL REGULATION PHASE *)
            IF -rPID_Output < 0.0 THEN rLouverPosition_Pct := 0.0;
            ELSIF -rPID_Output > 100.0 THEN rLouverPosition_Pct := 100.0;
            ELSE rLouverPosition_Pct := -rPID_Output; END_IF;
            
            bAmmoniaValveOpen := (rFilteredAmbientTemp > -10.0) AND (rLouverPosition_Pct > 50.0);
            
            IF rPID_Output < 0.0 THEN rHeaterPower_Pct := 0.0;
            ELSIF rPID_Output > 100.0 THEN rHeaterPower_Pct := 100.0;
            ELSE rHeaterPower_Pct := rPID_Output; END_IF;
            
        END_IF;
        
        (* Overrides for manual ground commands *)
        IF bOverrideManual THEN
            rLouverPosition_Pct := rOverrideLouverPos;
        END_IF;

    99: (* FAIL-SAFE LOCKOUT LATCH *)
        (* Requires full reset of bEnable to clear *)
        IF NOT bEmergencyStop AND NOT bEnable THEN
            iControlState := 0;
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
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
