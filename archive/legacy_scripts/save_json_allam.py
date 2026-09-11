import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Utility-Scale Supercritical CO2 (sCO2) Allam Cycle Power Plant**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., 300-bar sCO2 turbomachinery thrust bearing active magnetic levitation, recuperator heat exchanger thermal stress gradient limiting, and oxy-combustor stoichiometric ratio tracking). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_AllamsCO2Power\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Utility-Scale Supercritical CO2 (sCO2) Allam Cycle Power Plant

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_AllamsCO2PowerControl
VAR_INPUT
    bEnable : BOOL; (* System enable signal *)
    bEmergencyStop : BOOL; (* Emergency stop (active low) *)
    rSCO2_Pressure : REAL; (* sCO2 pressure in bar *)
    rSCO2_TempInlet : REAL; (* sCO2 turbine inlet temp in degC *)
    rOxyFuelRatio : REAL; (* Stoichiometric ratio of oxygen to fuel *)
    rRotorAxialDisplacement : REAL; (* Turbine rotor axial displacement in mm *)
END_VAR
VAR_OUTPUT
    bSystemReady : BOOL; (* Plant ready for load *)
    bTripCommand : BOOL; (* Master trip command to plant systems *)
    rMagneticBearingCurrent : REAL; (* Control signal to active magnetic thrust bearing (Amps) *)
    rRecuperatorBypassValve : REAL; (* Bypass valve command (%) to limit thermal stress *)
    rCombustorOxyValve : REAL; (* Oxidizer valve command (%) for stoichiometry tracking *)
END_VAR
VAR
    iState : INT := 0;
    tStartDelay : TON;
    tRampTimer : TON;
    rStressGradient : REAL := 0.0;
    rLastTempInlet : REAL := 0.0;
    rTempDelta : REAL := 0.0;
    rPID_Integral : REAL := 0.0;
    rPID_Error : REAL := 0.0;
END_VAR
VAR CONSTANT
    MAX_TEMP_GRADIENT : REAL := 15.0; (* degC/sec limit *)
    NOMINAL_OXY_RATIO : REAL := 1.05; (* Target ratio *)
    TRIP_PRESSURE_LIMIT : REAL := 320.0; (* bar *)
    TRIP_DISPLACEMENT_LIMIT : REAL := 0.5; (* mm *)
END_VAR

(* === MAIN LOGIC === *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bTripCommand := TRUE;
    rMagneticBearingCurrent := 0.0;
    rRecuperatorBypassValve := 100.0; (* Full bypass on trip *)
    rCombustorOxyValve := 0.0;
    iState := 0;
    RETURN;
END_IF;

(* Continuous Safety Checks *)
IF rSCO2_Pressure > TRIP_PRESSURE_LIMIT OR ABS(rRotorAxialDisplacement) > TRIP_DISPLACEMENT_LIMIT THEN
    bTripCommand := TRUE;
    iState := 99; (* Trip state *)
END_IF;

(* Magnetic Bearing Control (PD Controller for axial displacement) *)
(* Very simplified approximation of a 300-bar thrust bearing levitation controller *)
rMagneticBearingCurrent := rRotorAxialDisplacement * 50.0 + (rRotorAxialDisplacement - rPID_Error) * 10.0;
rPID_Error := rRotorAxialDisplacement;

(* Thermal Stress Gradient Limiting on Recuperator *)
rTempDelta := rSCO2_TempInlet - rLastTempInlet;
rLastTempInlet := rSCO2_TempInlet;

IF ABS(rTempDelta) > MAX_TEMP_GRADIENT THEN
    (* Modulate bypass valve to protect recuperator from thermal shock *)
    rRecuperatorBypassValve := MIN(100.0, rRecuperatorBypassValve + (ABS(rTempDelta) - MAX_TEMP_GRADIENT) * 2.0);
ELSE
    rRecuperatorBypassValve := MAX(0.0, rRecuperatorBypassValve - 0.5);
END_IF;

(* Main State Machine *)
CASE iState OF
    0: (* IDLE *)
        bTripCommand := FALSE;
        bSystemReady := FALSE;
        rCombustorOxyValve := 0.0;
        IF bEnable THEN
            tStartDelay(IN := TRUE, PT := T#10S);
            IF tStartDelay.Q THEN
                tStartDelay(IN := FALSE);
                iState := 10;
            END_IF;
        ELSE
            tStartDelay(IN := FALSE);
        END_IF;

    10: (* PURGE AND IGNITION PREP *)
        (* Maintain minimum oxygen flow for purge *)
        rCombustorOxyValve := 15.0; 
        tRampTimer(IN := TRUE, PT := T#30S);
        IF tRampTimer.Q THEN
            tRampTimer(IN := FALSE);
            iState := 20;
        END_IF;

    20: (* NORMAL OPERATION (Stoichiometric Control) *)
        bSystemReady := TRUE;
        (* PI Controller for Oxy-Combustor Ratio Tracking *)
        rPID_Integral := rPID_Integral + (NOMINAL_OXY_RATIO - rOxyFuelRatio) * 0.1;
        rCombustorOxyValve := 50.0 + (NOMINAL_OXY_RATIO - rOxyFuelRatio) * 20.0 + rPID_Integral;
        
        (* Clamp outputs *)
        IF rCombustorOxyValve > 100.0 THEN
            rCombustorOxyValve := 100.0;
        ELSIF rCombustorOxyValve < 15.0 THEN
            rCombustorOxyValve := 15.0;
        END_IF;

        IF NOT bEnable THEN
            iState := 30; (* Shutdown sequence *)
        END_IF;

    30: (* SHUTDOWN *)
        bSystemReady := FALSE;
        rCombustorOxyValve := MAX(0.0, rCombustorOxyValve - 5.0);
        IF rCombustorOxyValve = 0.0 THEN
            iState := 0;
        END_IF;

    99: (* TRIP LATCH *)
        bSystemReady := FALSE;
        bTripCommand := TRUE;
        (* Wait for operator reset which would re-toggle EmergencyStop/Enable in external logic *)

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
