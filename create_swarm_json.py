import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Industrial Pharmaceutical Cleanroom Bioreactor WFI (Water For Injection) Loop Thermal Sanitization and O3 Destruction**

Task: Invent a highly complex, ultra-realistic control scenario for this domain. Make this code EVEN BETTER, MORE ADVANCED, and MORE RIGOROUS than previous iterations. Include extreme edge-case handling, advanced math, and robust fault-tolerance.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_Pharma_WFILoop\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Industrial Pharmaceutical Cleanroom Bioreactor WFI (Water For Injection) Loop Thermal Sanitization and O3 Destruction

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_WFI_ThermalSanitization_O3Destruction
VAR_INPUT
    bEnableAutoMode    : BOOL;  (* System enable signal in Auto Mode *)
    bEmergencyStop_CH1 : BOOL;  (* Safety relay channel 1 OK signal *)
    bEmergencyStop_CH2 : BOOL;  (* Safety relay channel 2 OK signal *)
    rTempSupply        : REAL;  (* Supply temperature (deg C) *)
    rTempReturn        : REAL;  (* Return temperature (deg C) *)
    rO3Concentration   : REAL;  (* Ozone concentration (ppb) *)
    rFlowRate          : REAL;  (* WFI Flow rate (L/min) *)
    bUVLampsOK         : BOOL;  (* UV Destruct lamps operational status *)
END_VAR
VAR_OUTPUT
    bSystemReady       : BOOL;  (* System ready status / Loop in production *)
    rHeaterControlCV   : REAL;  (* Control Valve output for heat exchanger (0-100%) *)
    bO3GeneratorEnable : BOOL;  (* Ozone generator activation signal *)
    bUVLampEnable      : BOOL;  (* UV lamp activation signal *)
    bCriticalAlarm     : BOOL;  (* Critical fault alarm output *)
    iSanitizationStep  : INT;   (* Current step of thermal sanitization sequence *)
END_VAR
VAR
    (* Internal State and Timers *)
    iState             : INT := 0;
    tSanitizationTimer : TON;
    tCooldownTimer     : TON;
    tO3DestructTimer   : TON;
    
    (* Filtered Inputs for Noise Reduction (EMA Filter) *)
    rTempSupplyFilt    : REAL := 20.0;
    rTempReturnFilt    : REAL := 20.0;
    rO3ConcFilt        : REAL := 0.0;
    
    (* Filter constants *)
    alpha_Temp         : REAL := 0.1;
    alpha_O3           : REAL := 0.05;
    
    (* PID Variables for Heater Control *)
    rError             : REAL;
    rIntegral          : REAL := 0.0;
    rDerivative        : REAL;
    rLastError         : REAL := 0.0;
    rKp                : REAL := 2.5;
    rKi                : REAL := 0.15;
    rKd                : REAL := 0.5;
    rTempSetpoint      : REAL := 85.0; (* Sanitization target temp *)
    
    (* Safety/Integrity *)
    bEStopActive       : BOOL;
END_VAR

(* === MAIN LOGIC === *)

(* 1. Safety Interlocks & Redundancy Check *)
bEStopActive := NOT (bEmergencyStop_CH1 AND bEmergencyStop_CH2);
IF bEStopActive OR NOT bUVLampsOK THEN
    bSystemReady := FALSE;
    bCriticalAlarm := TRUE;
    rHeaterControlCV := 0.0;
    bO3GeneratorEnable := FALSE;
    bUVLampEnable := FALSE;
    iState := 999; (* FAULT STATE *)
    RETURN;
END_IF;

(* Clear faults if conditions are met and disabled *)
IF bCriticalAlarm AND NOT bEStopActive AND NOT bEnableAutoMode AND bUVLampsOK THEN
    bCriticalAlarm := FALSE;
    iState := 0;
END_IF;

(* 2. Input Signal Filtering (Exponential Moving Average) *)
rTempSupplyFilt := (alpha_Temp * rTempSupply) + ((1.0 - alpha_Temp) * rTempSupplyFilt);
rTempReturnFilt := (alpha_Temp * rTempReturn) + ((1.0 - alpha_Temp) * rTempReturnFilt);
rO3ConcFilt     := (alpha_O3 * rO3Concentration) + ((1.0 - alpha_O3) * rO3ConcFilt);

(* 3. State Machine for Sanitization and Production *)
CASE iState OF
    0: (* IDLE / STANDBY *)
        bSystemReady := FALSE;
        rHeaterControlCV := 0.0;
        bO3GeneratorEnable := FALSE;
        bUVLampEnable := FALSE;
        iSanitizationStep := 0;
        
        IF bEnableAutoMode THEN
            iState := 10; (* Start Production with O3 *)
        END_IF;

    10: (* PRODUCTION WITH O3 MAINTENANCE *)
        bSystemReady := TRUE;
        iSanitizationStep := 1;
        
        (* Maintain low-level O3 for sanitization at ambient *)
        IF rO3ConcFilt < 20.0 THEN
            bO3GeneratorEnable := TRUE;
        ELSIF rO3ConcFilt > 30.0 THEN
            bO3GeneratorEnable := FALSE;
        END_IF;
        
        (* Destruct O3 before point of use via UV *)
        bUVLampEnable := TRUE;
        
        (* Transition to Thermal Sanitization if requested or scheduled *)
        IF rTempSetpoint > 80.0 AND rTempSupply > 50.0 THEN
            iState := 20; (* Prepare Thermal San *)
            bSystemReady := FALSE;
        END_IF;
        
    20: (* PREPARE THERMAL SANITIZATION *)
        bO3GeneratorEnable := FALSE; (* Stop O3 during thermal *)
        bUVLampEnable := TRUE;       (* Keep UV on to kill residual O3 *)
        iSanitizationStep := 2;
        
        tO3DestructTimer(IN := TRUE, PT := T#5M);
        
        (* Wait for O3 to deplete and UV timer *)
        IF tO3DestructTimer.Q AND rO3ConcFilt < 5.0 THEN
            tO3DestructTimer(IN := FALSE);
            iState := 30; (* Heating Phase *)
        END_IF;
        
    30: (* HEATING PHASE (PID Control) *)
        iSanitizationStep := 3;
        
        (* Calculate PID *)
        rError := rTempSetpoint - rTempSupplyFilt;
        rIntegral := rIntegral + (rError * 0.1); (* Assuming 100ms task rate *)
        (* Anti-windup *)
        IF rIntegral > 100.0 THEN rIntegral := 100.0; END_IF;
        IF rIntegral < 0.0 THEN rIntegral := 0.0; END_IF;
        
        rDerivative := (rError - rLastError) / 0.1;
        rHeaterControlCV := (rKp * rError) + (rKi * rIntegral) + (rKd * rDerivative);
        
        (* Clamp Output *)
        IF rHeaterControlCV > 100.0 THEN rHeaterControlCV := 100.0; END_IF;
        IF rHeaterControlCV < 0.0 THEN rHeaterControlCV := 0.0; END_IF;
        
        rLastError := rError;
        
        (* Check if return temp has reached sanitization temp *)
        IF rTempReturnFilt >= 80.0 THEN
            iState := 40; (* Holding Phase *)
        END_IF;
        
    40: (* HOLDING PHASE *)
        iSanitizationStep := 4;
        
        (* Continue PID to maintain temp *)
        rError := rTempSetpoint - rTempSupplyFilt;
        rIntegral := rIntegral + (rError * 0.1);
        rDerivative := (rError - rLastError) / 0.1;
        rHeaterControlCV := (rKp * rError) + (rKi * rIntegral) + (rKd * rDerivative);
        
        IF rHeaterControlCV > 100.0 THEN rHeaterControlCV := 100.0; END_IF;
        IF rHeaterControlCV < 0.0 THEN rHeaterControlCV := 0.0; END_IF;
        rLastError := rError;
        
        tSanitizationTimer(IN := TRUE, PT := T#60M); (* 60 mins at >80C *)
        
        (* If temp drops below threshold, reset timer *)
        IF rTempReturnFilt < 79.0 THEN
            tSanitizationTimer(IN := FALSE);
        END_IF;
        
        IF tSanitizationTimer.Q THEN
            tSanitizationTimer(IN := FALSE);
            iState := 50; (* Cooldown *)
        END_IF;
        
    50: (* COOLDOWN PHASE *)
        iSanitizationStep := 5;
        rHeaterControlCV := 0.0; (* Turn off heater *)
        
        (* Wait for temps to return to ambient *)
        IF rTempReturnFilt < 25.0 THEN
            iState := 0; (* Back to idle *)
        END_IF;
        
    999: (* FAULT STATE *)
        bSystemReady := FALSE;
        rHeaterControlCV := 0.0;
        bO3GeneratorEnable := FALSE;
        bUVLampEnable := FALSE;
        
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
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
