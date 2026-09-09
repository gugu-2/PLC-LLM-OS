import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Semiconductor Extreme Ultraviolet (EUV) Laser-Produced Plasma (LPP) Collector Mirror**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., High-temperature tin debris mitigation gas flow (H2) modeling, spectral purity filter (SPF) thermal distortion tracking, and picosecond laser targeting synchronization). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_EUV_LPP_CollectorMirror\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Semiconductor Extreme Ultraviolet (EUV) Laser-Produced Plasma (LPP) Collector Mirror

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st\nFUNCTION_BLOCK FB_EUV_LPP_CollectorMirror\nVAR_INPUT\n    (* System operation signals *)\n    bEnable                 : BOOL;     (* Enable collector mirror control system *)\n    bEmergencyStop          : BOOL;     (* Safety interlock / Emergency stop signal (active low) *)\n    \n    (* Process measurements *)\n    rMirrorTempDegC         : REAL;     (* Current collector mirror surface temperature [deg C] *)\n    rH2GasFlowTarget        : REAL;     (* Target Hydrogen gas flow for tin debris mitigation [slpm] *)\n    diTinDebrisCount        : DINT;     (* Real-time tin ion (Sn++) count measured by plasma diagnostic *)\n    bLaserSyncTrigger       : BOOL;     (* Picosecond CO2 laser firing synchronization pulse *)\nEND_VAR\nVAR_OUTPUT\n    (* System Status *)\n    bSystemReady            : BOOL;     (* EUV collector system is ready for plasma generation *)\n    bThermalAlarm           : BOOL;     (* Thermal distortion or overheating alarm *)\n    bMitigationFault        : BOOL;     (* Debris mitigation system failure *)\n    \n    (* Actuator Commands *)\n    rH2ValveControl         : REAL;     (* Command signal to H2 mass flow controller [0.0 - 100.0 %] *)\n    rCoolerPowerCommand     : REAL;     (* Thermal control loop cooling power [0.0 - 100.0 %] *)\n    bSyncAcknowledge        : BOOL;     (* Acknowledge laser pulse readiness *)\nEND_VAR\nVAR\n    (* Internal state and timers *)\n    iState                  : INT := 0; \n    tStartupDelay           : TON;\n    tPurgeTimer             : TON;\n    \n    (* PID and thermal modeling variables *)\n    rTempError              : REAL;\n    rTempIntegral           : REAL := 0.0;\n    rTempDerivative         : REAL := 0.0;\n    rLastTemp               : REAL := 25.0;\n    \n    (* Kinematic/Process constants *)\n    c_rTempSetpoint         : REAL := 150.0; (* Optimal mirror temp to keep Sn liquid but not damage coating *)\n    c_rKp                   : REAL := 2.5;\n    c_rKi                   : REAL := 0.15;\n    c_rKd                   : REAL := 0.5;\n    \n    (* Mitigation metrics *)\n    rRequiredFlow           : REAL;\nEND_VAR\n\n(* === MAIN LOGIC === *)\n(* Safety Interlock Evaluation *)\nIF NOT bEmergencyStop THEN\n    bSystemReady := FALSE;\n    bThermalAlarm := TRUE;\n    bMitigationFault := TRUE;\n    rH2ValveControl := 0.0;\n    rCoolerPowerCommand := 0.0;\n    bSyncAcknowledge := FALSE;\n    iState := 0; (* Force to IDLE / FAULT state *)\n    RETURN;\nEND_IF;\n\n(* Thermal Control - PID Loop (Executed every cycle) *)\nrTempError := rMirrorTempDegC - c_rTempSetpoint;\nrTempIntegral := rTempIntegral + (rTempError * 0.01); (* Assuming 10ms cycle time *)\nrTempDerivative := (rMirrorTempDegC - rLastTemp) / 0.01;\nrLastTemp := rMirrorTempDegC;\n\n(* Calculate cooling effort *)\nrCoolerPowerCommand := (c_rKp * rTempError) + (c_rKi * rTempIntegral) + (c_rKd * rTempDerivative);\n\n(* Clamp output to valid percentage range *)\nIF rCoolerPowerCommand > 100.0 THEN\n    rCoolerPowerCommand := 100.0;\nELSIF rCoolerPowerCommand < 0.0 THEN\n    rCoolerPowerCommand := 0.0;\nEND_IF;\n\n(* Thermal Alarm threshold *)\nIF rMirrorTempDegC > 180.0 OR rMirrorTempDegC < 120.0 THEN\n    bThermalAlarm := TRUE;\nELSE\n    bThermalAlarm := FALSE;\nEND_IF;\n\n(* Main State Machine *)\nCASE iState OF\n    0: (* IDLE & INITIALIZATION *)\n        bSystemReady := FALSE;\n        rH2ValveControl := 0.0;\n        bSyncAcknowledge := FALSE;\n        \n        IF bEnable AND NOT bThermalAlarm THEN\n            iState := 10;\n        END_IF;\n        \n    10: (* PRE-PURGE H2 SYSTEM *)\n        (* Ramp up H2 flow to baseline for tin mitigation before firing *)\n        rH2ValveControl := 50.0; (* 50% flow for purge *)\n        tPurgeTimer(IN := TRUE, PT := T#15S);\n        \n        IF tPurgeTimer.Q THEN\n            tPurgeTimer(IN := FALSE);\n            iState := 20;\n        END_IF;\n        \n    20: (* ACTIVE RUNNING / TARGETING *)\n        bSystemReady := TRUE;\n        \n        (* Dynamic H2 flow based on target and real-time tin debris *)\n        (* Increase flow proportionally if heavy debris count detected *)\n        rRequiredFlow := rH2GasFlowTarget + (DINT_TO_REAL(diTinDebrisCount) * 0.001);\n        \n        IF rRequiredFlow > 100.0 THEN\n            rH2ValveControl := 100.0;\n        ELSE\n            rH2ValveControl := rRequiredFlow;\n        END_IF;\n        \n        (* Laser synchronization *)\n        IF bLaserSyncTrigger THEN\n            bSyncAcknowledge := TRUE;\n            (* Log or process shot statistics here... *)\n        ELSE\n            bSyncAcknowledge := FALSE;\n        END_IF;\n        \n        (* Fault conditions check *)\n        IF diTinDebrisCount > 50000 THEN\n            bMitigationFault := TRUE;\n            iState := 30; (* Go to fault cooldown *)\n        END_IF;\n        \n        IF NOT bEnable THEN\n            iState := 0;\n        END_IF;\n        \n    30: (* FAULT HANDLING & COOLDOWN *)\n        bSystemReady := FALSE;\n        rH2ValveControl := 100.0; (* Max flow to clear heavy debris *)\n        \n        tStartupDelay(IN := TRUE, PT := T#30S);\n        IF tStartupDelay.Q THEN\n            tStartupDelay(IN := FALSE);\n            bMitigationFault := FALSE;\n            IF NOT bEnable THEN\n                iState := 0;\n            END_IF;\n        END_IF;\n        \nEND_CASE;\nEND_FUNCTION_BLOCK\n```"""

os.makedirs(r"c:\Users\majip\Downloads\LLM REASEARCH\data\swarm_raw", exist_ok=True)
filename = f"c:\\Users\\majip\\Downloads\\LLM REASEARCH\\data\\swarm_raw\\agent_{uuid.uuid4().hex[:8]}.json"
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
