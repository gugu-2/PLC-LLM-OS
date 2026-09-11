import json, uuid, os

prompt = """<USER_REQUEST>
You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Advanced Superconducting Maglev (SCMAGLEV) Train Propulsion Inverter**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., 3-phase linear synchronous motor pulse-width modulation, active vehicle-to-guideway heave damping, and sub-cooled liquid helium cryostat quench protection). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_SCMAGLEV_Propulsion\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Advanced Superconducting Maglev (SCMAGLEV) Train Propulsion Inverter

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT.
</USER_REQUEST>"""

code = """```iec-st
FUNCTION_BLOCK FB_SCMAGLEV_Propulsion
VAR_INPUT
    bSystemEnable         : BOOL;      (* Main system enable command from ATC *)
    bEmergencyStop        : BOOL;      (* Hardwired safety loop OK (TRUE = OK) *)
    rSpeedReference       : REAL;      (* Desired vehicle speed in km/h *)
    rActualSpeed          : REAL;      (* Filtered actual speed in km/h from guideway transponders *)
    rHeavePosition        : REAL;      (* Vehicle-to-guideway heave deviation in mm *)
    rCryostatTemp         : REAL;      (* Liquid Helium temperature in Kelvin *)
    rPhaseCurrentU        : REAL;      (* U-phase motor current feedback in Amperes *)
    rPhaseCurrentV        : REAL;      (* V-phase motor current feedback in Amperes *)
    rPhaseCurrentW        : REAL;      (* W-phase motor current feedback in Amperes *)
END_VAR
VAR_OUTPUT
    bInverterReady        : BOOL;      (* Inverter ready to supply tractive effort *)
    rPWM_DutyCycleU       : REAL;      (* U-phase PWM duty cycle command 0.0 - 1.0 *)
    rPWM_DutyCycleV       : REAL;      (* V-phase PWM duty cycle command 0.0 - 1.0 *)
    rPWM_DutyCycleW       : REAL;      (* W-phase PWM duty cycle command 0.0 - 1.0 *)
    bHeaveDampingActive   : BOOL;      (* Active heave damping engagement status *)
    bCryoQuenchAlarm      : BOOL;      (* Superconducting coil quench alarm/trip *)
    iFaultCode            : INT;       (* Diagnostics fault code (0 = Healthy) *)
END_VAR
VAR
    iMainState            : INT := 0;  (* State machine state *)
    rSpeedError           : REAL;      (* Speed loop error *)
    rSpeedIntegral        : REAL;      (* Speed loop integral term *)
    rTorqueCommand        : REAL;      (* Force/Torque command to motor *)
    
    rHeaveErrorLast       : REAL := 0.0;
    rHeaveDeriv           : REAL;
    
    tInverterStartDelay   : TON;
    tQuenchFilterTimer    : TON;
    bQuenchDetected       : BOOL;
    
    rMaxCurrentAllowed    : REAL := 5000.0; (* Amps limit *)
    rMaxTempAllowed       : REAL := 4.5;    (* Kelvin limit for SC coils *)
    
    rKp_Speed             : REAL := 25.4;
    rKi_Speed             : REAL := 5.2;
    rKp_Heave             : REAL := 1.8;
    rKd_Heave             : REAL := 0.45;
END_VAR

(* === MAIN LOGIC === *)

(* Safety and Interlocks: Superconducting Cryostat Quench Protection *)
IF (rCryostatTemp > rMaxTempAllowed) THEN
    tQuenchFilterTimer(IN := TRUE, PT := T#50MS);
    IF tQuenchFilterTimer.Q THEN
        bQuenchDetected := TRUE;
    END_IF;
ELSE
    tQuenchFilterTimer(IN := FALSE);
END_IF;

IF NOT bEmergencyStop OR bQuenchDetected THEN
    bInverterReady      := FALSE;
    rPWM_DutyCycleU     := 0.0;
    rPWM_DutyCycleV     := 0.0;
    rPWM_DutyCycleW     := 0.0;
    bHeaveDampingActive := FALSE;
    bCryoQuenchAlarm    := bQuenchDetected;
    
    IF NOT bEmergencyStop THEN
        iFaultCode := 1001; (* E-STOP Activated *)
    ELSIF bQuenchDetected THEN
        iFaultCode := 2042; (* Magnet Quench Protection Trip *)
    END_IF;
    
    iMainState := 0; (* Force to IDLE *)
    RETURN;
END_IF;

(* Clear faults if system is healthy *)
iFaultCode := 0;
bCryoQuenchAlarm := FALSE;

(* Active Heave Damping Control *)
(* Calculates derivative component for stabilizing vertical oscillations *)
rHeaveDeriv := rHeavePosition - rHeaveErrorLast;
rHeaveErrorLast := rHeavePosition;
IF ABS(rHeavePosition) > 2.0 THEN
    bHeaveDampingActive := TRUE;
ELSE
    bHeaveDampingActive := FALSE;
END_IF;

(* State Machine for Traction Inverter Control *)
CASE iMainState OF
    0: (* SYSTEM IDLE *)
        bInverterReady := FALSE;
        rSpeedIntegral := 0.0;
        rPWM_DutyCycleU := 0.5;
        rPWM_DutyCycleV := 0.5;
        rPWM_DutyCycleW := 0.5;
        
        IF bSystemEnable THEN
            tInverterStartDelay(IN := TRUE, PT := T#2S);
            IF tInverterStartDelay.Q THEN
                tInverterStartDelay(IN := FALSE);
                iMainState := 10;
            END_IF;
        ELSE
            tInverterStartDelay(IN := FALSE);
        END_IF;

    10: (* INVERTER PRE-CHARGE AND SYNCHRONIZATION *)
        (* Simulating synchronization with linear guideway poles *)
        bInverterReady := TRUE;
        IF ABS(rSpeedReference - rActualSpeed) < 5.0 THEN
            iMainState := 20;
        END_IF;
        IF NOT bSystemEnable THEN
            iMainState := 0;
        END_IF;

    20: (* RUNNING - VECTOR PWM GENERATION *)
        (* PI Speed Controller *)
        rSpeedError := rSpeedReference - rActualSpeed;
        rSpeedIntegral := rSpeedIntegral + (rSpeedError * 0.01); (* Assume 10ms task rate *)
        
        (* Anti-windup limit *)
        IF rSpeedIntegral > 1000.0 THEN rSpeedIntegral := 1000.0; END_IF;
        IF rSpeedIntegral < -1000.0 THEN rSpeedIntegral := -1000.0; END_IF;
        
        rTorqueCommand := (rSpeedError * rKp_Speed) + (rSpeedIntegral * rKi_Speed);
        
        (* Active Heave Compensation overlaid on Torque Command *)
        IF bHeaveDampingActive THEN
            rTorqueCommand := rTorqueCommand - (rHeavePosition * rKp_Heave) - (rHeaveDeriv * rKd_Heave);
        END_IF;
        
        (* Basic Phase Output Synthesis (Simplified for Simulation) *)
        rPWM_DutyCycleU := 0.5 + (rTorqueCommand * 0.0001);
        rPWM_DutyCycleV := 0.5 - (rTorqueCommand * 0.00005);
        rPWM_DutyCycleW := 0.5 - (rTorqueCommand * 0.00005);
        
        (* Duty Cycle Clamping *)
        IF rPWM_DutyCycleU > 0.95 THEN rPWM_DutyCycleU := 0.95; END_IF;
        IF rPWM_DutyCycleU < 0.05 THEN rPWM_DutyCycleU := 0.05; END_IF;
        IF rPWM_DutyCycleV > 0.95 THEN rPWM_DutyCycleV := 0.95; END_IF;
        IF rPWM_DutyCycleV < 0.05 THEN rPWM_DutyCycleV := 0.05; END_IF;
        IF rPWM_DutyCycleW > 0.95 THEN rPWM_DutyCycleW := 0.95; END_IF;
        IF rPWM_DutyCycleW < 0.05 THEN rPWM_DutyCycleW := 0.05; END_IF;

        IF NOT bSystemEnable THEN
            iMainState := 0;
        END_IF;
        
    ELSE
        (* FAULT STATE CATCH-ALL *)
        iMainState := 0;
END_CASE;

END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}

os.makedirs("c:/Users/majip/Downloads/LLM REASEARCH/data/swarm_raw", exist_ok=True)
with open(f"c:/Users/majip/Downloads/LLM REASEARCH/data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
