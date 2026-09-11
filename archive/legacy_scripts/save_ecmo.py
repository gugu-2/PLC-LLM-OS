import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Next-Gen Biomedical Extracorporeal Membrane Oxygenation (ECMO) Centrifugal Pump**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Magnetic levitation bearing blood hemolysis minimization, counter-current hollow fiber oxygenator gas mass flow blending, and pulsatile physiologic flow emulation). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_ECMO_CentrifugalPump\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Next-Gen Biomedical Extracorporeal Membrane Oxygenation (ECMO) Centrifugal Pump

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_NextGen_ECMO_MagLev_Pump
(* 
   ========================================================================
   Lumina AI Elite Synth Data - IEC 61131-3 Structured Text
   Domain: Next-Gen Biomedical Extracorporeal Membrane Oxygenation (ECMO) Centrifugal Pump
   Description: Advanced magnetic levitation bearing control, physiologic pulsatile
                flow emulation, and hemolysis mitigation logic for prolonged life support.
   ========================================================================
*)
VAR_INPUT
    bEnableSys              : BOOL;     (* System master enable *)
    bEmergencyStop          : BOOL;     (* Hardware safety relay OK signal *)
    rTargetBloodFlowLPM     : REAL;     (* Target blood flow in L/min *)
    rInletPressure_mmHg     : REAL;     (* Venous return pressure *)
    rOutletPressure_mmHg    : REAL;     (* Arterial infusion pressure *)
    rMagBearingZPos_um      : REAL;     (* Z-axis magnetic bearing position feedback (micrometers) *)
    bEnablePulsatileFlow    : BOOL;     (* Enable physiologic pulsatile mode *)
    rPatientHeartRate_BPM   : REAL;     (* Patient ECG heart rate for synchronous pulsing *)
END_VAR

VAR_OUTPUT
    bSystemReady            : BOOL;     (* System initialized and ready for pump start *)
    rMotorSpeedCmd_RPM      : REAL;     (* Commanded mag-lev motor speed (RPM) *)
    rMagBearingForceCmd_N   : REAL;     (* Z-axis levitation force command (Newtons) *)
    bCavitationAlarm        : BOOL;     (* Inlet pressure drop indicating cavitation *)
    bHemolysisWarning       : BOOL;     (* High shear stress or pressure gradient warning *)
    bCriticalFault          : BOOL;     (* Unrecoverable fault (e.g. bearing failure) *)
END_VAR

VAR
    iState                  : INT := 0; 
    (* State Machine: 
       0=Init/Standby, 10=Levitation Check, 20=Priming, 30=Continuous Run, 40=Pulsatile Run, 99=Fault *)
    
    tStateTimer             : TON;
    rDeltaPressure          : REAL;     (* Pressure gradient across pump *)
    rBaseSpeed_RPM          : REAL;     (* Base calculated speed *)
    
    (* Mag-Lev PID variables *)
    rZPosError              : REAL;
    rZPosKp                 : REAL := 2.5;
    rZPosKi                 : REAL := 0.1;
    rZPosKd                 : REAL := 0.05;
    rZPosIntegral           : REAL := 0.0;
    rZPosPrevError          : REAL := 0.0;
    
    (* Pulsatile calculation *)
    rPulsePhase_rad         : REAL := 0.0;
    rPulseAmplitude_RPM     : REAL := 0.0;
    
    (* Safety thresholds *)
    MAX_SPEED_RPM           : REAL := 5500.0;
    MIN_INLET_PRESS         : REAL := -100.0; (* mmHg *)
    MAX_DP                  : REAL := 450.0;  (* mmHg *)
END_VAR

(* === SAFETY & INTERLOCK LOGIC === *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bCriticalFault := TRUE;
    rMotorSpeedCmd_RPM := 0.0;
    rMagBearingForceCmd_N := 0.0;
    iState := 99;
    RETURN;
END_IF;

(* Derived Measurements & Filtering *)
rDeltaPressure := rOutletPressure_mmHg - rInletPressure_mmHg;

(* Cavitation Detection *)
IF rInletPressure_mmHg < MIN_INLET_PRESS THEN
    bCavitationAlarm := TRUE;
ELSE
    bCavitationAlarm := FALSE;
END_IF;

(* Hemolysis / Shear Stress Warning *)
IF rDeltaPressure > MAX_DP OR rMotorSpeedCmd_RPM > 4800.0 THEN
    bHemolysisWarning := TRUE;
ELSE
    bHemolysisWarning := FALSE;
END_IF;

(* Magnetic Bearing Z-axis Levitation PID Control (1kHz execution assumed) *)
rZPosError := 50.0 - rMagBearingZPos_um; (* Target gap 50um *)
rZPosIntegral := rZPosIntegral + rZPosError;
IF rZPosIntegral > 1000.0 THEN rZPosIntegral := 1000.0; END_IF;
IF rZPosIntegral < -1000.0 THEN rZPosIntegral := -1000.0; END_IF;

rMagBearingForceCmd_N := (rZPosKp * rZPosError) + 
                         (rZPosKi * rZPosIntegral) + 
                         (rZPosKd * (rZPosError - rZPosPrevError));
rZPosPrevError := rZPosError;


(* === MAIN STATE MACHINE === *)
CASE iState OF
    0: (* INIT / STANDBY *)
        bSystemReady := TRUE;
        rMotorSpeedCmd_RPM := 0.0;
        
        IF bEnableSys THEN
            bSystemReady := FALSE;
            tStateTimer(IN := FALSE);
            iState := 10;
        END_IF;

    10: (* LEVITATION CHECK *)
        (* Wait for Mag Bearing to stabilize *)
        tStateTimer(IN := TRUE, PT := T#2S);
        IF ABS(rZPosError) < 5.0 AND tStateTimer.Q THEN
            tStateTimer(IN := FALSE);
            iState := 20; (* Proceed to prime *)
        ELSIF tStateTimer.Q THEN
            (* Failed to levitate *)
            bCriticalFault := TRUE;
            iState := 99;
        END_IF;

    20: (* PRIMING *)
        (* Low speed ramp to remove air bubbles *)
        rMotorSpeedCmd_RPM := 1500.0;
        tStateTimer(IN := TRUE, PT := T#10S);
        IF tStateTimer.Q THEN
            tStateTimer(IN := FALSE);
            IF bEnablePulsatileFlow THEN
                iState := 40;
            ELSE
                iState := 30;
            END_IF;
        END_IF;

    30: (* CONTINUOUS RUN *)
        (* Flow control using basic proportional mapping for demo *)
        rBaseSpeed_RPM := 1500.0 + (rTargetBloodFlowLPM * 400.0);
        
        (* Cavitation override *)
        IF bCavitationAlarm THEN
            rBaseSpeed_RPM := rBaseSpeed_RPM * 0.8;
        END_IF;
        
        rMotorSpeedCmd_RPM := rBaseSpeed_RPM;
        
        IF bEnablePulsatileFlow THEN
            iState := 40;
        END_IF;
        IF NOT bEnableSys THEN
            iState := 0;
        END_IF;

    40: (* PULSATILE RUN *)
        rBaseSpeed_RPM := 1500.0 + (rTargetBloodFlowLPM * 400.0);
        
        (* Simulate physiologic pulse synchronous to patient heart rate *)
        rPulseAmplitude_RPM := rBaseSpeed_RPM * 0.25;
        (* Pulse phase integration simplified for PLC scanning *)
        rPulsePhase_rad := rPulsePhase_rad + (rPatientHeartRate_BPM / 60.0 * 2.0 * 3.14159 * 0.01);
        IF rPulsePhase_rad > 6.28318 THEN
            rPulsePhase_rad := rPulsePhase_rad - 6.28318;
        END_IF;
        
        rMotorSpeedCmd_RPM := rBaseSpeed_RPM + (rPulseAmplitude_RPM * SIN(rPulsePhase_rad));
        
        IF NOT bEnablePulsatileFlow THEN
            iState := 30;
        END_IF;
        IF NOT bEnableSys THEN
            iState := 0;
        END_IF;

    99: (* FAULT STATE *)
        rMotorSpeedCmd_RPM := 0.0;
        IF NOT bEmergencyStop THEN
            (* Wait for safety reset *)
            tStateTimer(IN := FALSE);
        ELSIF NOT bEnableSys THEN
            bCriticalFault := FALSE;
            iState := 0;
        END_IF;

END_CASE;

(* Speed Limiter *)
IF rMotorSpeedCmd_RPM > MAX_SPEED_RPM THEN
    rMotorSpeedCmd_RPM := MAX_SPEED_RPM;
END_IF;
IF rMotorSpeedCmd_RPM < 0.0 THEN
    rMotorSpeedCmd_RPM := 0.0;
END_IF;

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
