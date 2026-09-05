import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Utility-Scale Tidal Stream Generator Subsea Turbine**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., bi-directional yaw blade pitch dynamic vectoring, seawater ingress acoustic monitoring, and synchronous generator grid-tie under severe wave turbulence). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_TidalStreamTurbine\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Utility-Scale Tidal Stream Generator Subsea Turbine

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_TidalStreamTurbine
VAR_INPUT
    (* Required: at least 4-8 physical inputs with types and comments *)
    bEnable         : BOOL;     (* System enable signal *)
    bEmergencyStop  : BOOL;     (* Safety relay OK signal *)
    rProcessVar     : REAL;     (* Physical measurement e.g. temperature in deg C *)
    rTidalFlowVelocity : REAL; (* Tidal current velocity in m/s *)
    rNacelleHeading : REAL; (* Current yaw heading relative to magnetic north in degrees *)
    bSeawaterIngressSensor : BOOL; (* Acoustic seawater ingress monitoring OK signal *)
    rGridFrequency : REAL; (* Synchronous generator grid tie frequency in Hz *)
    rGridVoltage : REAL; (* Grid tie voltage in kV *)
    rRotorRPM : REAL; (* Turbine rotor speed in RPM *)
END_VAR
VAR_OUTPUT
    (* Required: at least 3-6 outputs with types and comments *)
    bSystemReady    : BOOL;     (* System ready status *)
    rControlOutput  : REAL;     (* Control signal to actuator *)
    bAlarm          : BOOL;     (* Fault alarm output *)
    rPitchAngleSetpoint : REAL; (* Dynamic blade pitch angle setpoint in degrees *)
    rYawTorqueDemand : REAL; (* Bi-directional yaw drive torque demand *)
    bGridTieBreakerClose : BOOL; (* Command to close grid-tie breaker *)
    iFaultCode : INT; (* Detailed fault diagnostic code *)
END_VAR
VAR
    (* Internal state variables *)
    iState          : INT := 0;
    tTimer          : TON;
    tGridSyncTimer : TON;
    tStartDelay : TON;
    rFilteredFlow : REAL := 0.0;
    rPitchIntegral : REAL := 0.0;
    rFlowAlpha : REAL := 0.05; (* Low pass filter alpha for flow *)
    bTargetReached : BOOL := FALSE;
END_VAR

(* === MAIN LOGIC === *)
IF NOT bEmergencyStop OR NOT bSeawaterIngressSensor THEN
    bSystemReady := FALSE;
    bGridTieBreakerClose := FALSE;
    bAlarm := TRUE;
    rPitchAngleSetpoint := 90.0; (* Feather blades *)
    rYawTorqueDemand := 0.0;
    iState := 999; (* Fault state *)
    iFaultCode := 16#F001; (* Emergency stop or leak *)
    RETURN;
END_IF;

(* Flow filter *)
rFilteredFlow := rFilteredFlow + rFlowAlpha * (rTidalFlowVelocity - rFilteredFlow);

CASE iState OF
    0: (* IDLE *)
        bSystemReady := TRUE;
        bAlarm := FALSE;
        iFaultCode := 0;
        bGridTieBreakerClose := FALSE;
        rPitchAngleSetpoint := 90.0; (* Feathered *)
        rYawTorqueDemand := 0.0;
        
        IF bEnable AND rFilteredFlow > 1.2 THEN (* Min cut-in speed *)
            iState := 10;
        END_IF;

    10: (* YAW ALIGNMENT *)
        (* Simplified yaw controller seeking 0 flow angle error, assuming heading target is 0 for tide *)
        IF rNacelleHeading > 5.0 THEN
            rYawTorqueDemand := -1500.0;
        ELSIF rNacelleHeading < -5.0 THEN
            rYawTorqueDemand := 1500.0;
        ELSE
            rYawTorqueDemand := 0.0;
            tStartDelay(IN := TRUE, PT := T#10S);
            IF tStartDelay.Q THEN
                tStartDelay(IN := FALSE);
                iState := 20;
            END_IF;
        END_IF;

    20: (* ROTOR ACCELERATION *)
        (* Gradually unfeather blades *)
        rPitchAngleSetpoint := rPitchAngleSetpoint - 0.5;
        IF rPitchAngleSetpoint < 15.0 THEN
            rPitchAngleSetpoint := 15.0;
        END_IF;
        
        (* Check RPM *)
        IF rRotorRPM > 18.0 THEN
            iState := 30;
        END_IF;

    30: (* GRID SYNC AND TIE *)
        (* Maintain speed while waiting for sync *)
        IF rRotorRPM > 20.0 THEN
            rPitchAngleSetpoint := rPitchAngleSetpoint + 0.1;
        ELSIF rRotorRPM < 19.5 THEN
            rPitchAngleSetpoint := rPitchAngleSetpoint - 0.1;
        END_IF;
        
        IF rGridFrequency > 49.8 AND rGridFrequency < 50.2 AND rGridVoltage > 31.0 AND rGridVoltage < 34.0 THEN
            tGridSyncTimer(IN := TRUE, PT := T#5S);
            IF tGridSyncTimer.Q THEN
                bGridTieBreakerClose := TRUE;
                tGridSyncTimer(IN := FALSE);
                iState := 40;
            END_IF;
        ELSE
            tGridSyncTimer(IN := FALSE);
        END_IF;

    40: (* RUNNING / POWER TRACKING *)
        (* Max Power Point Tracking (MPPT) logic placeholder *)
        IF rFilteredFlow > 3.5 THEN (* Rated speed *)
            rPitchAngleSetpoint := 5.0 + (rFilteredFlow - 3.5) * 10.0; (* Pitch to shed power *)
        ELSE
            rPitchAngleSetpoint := 5.0; (* Optimal pitch *)
        END_IF;
        rControlOutput := rFilteredFlow * 1.5;
        
        IF rFilteredFlow < 1.0 OR NOT bEnable THEN
            bGridTieBreakerClose := FALSE;
            iState := 0;
        END_IF;
        
    999: (* FAULT HANDLING *)
        IF bEmergencyStop AND bSeawaterIngressSensor THEN
            IF NOT bEnable THEN (* Require reset toggle *)
                iState := 0;
            END_IF;
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
