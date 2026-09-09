import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Next-Gen Utility-Scale Solar Updraft Tower (SUT) Aero-Turbine**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., 1000m chimney thermodynamic draft mapping, multi-megawatt axial turbine variable pitch, and greenhouse canopy diurnal thermal storage). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_SolarUpdraftTower\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Next-Gen Utility-Scale Solar Updraft Tower (SUT) Aero-Turbine

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_SUT_AeroTurbine_MasterControl
(* 
   ================================================================================
   Lumiana AI Cloud Swarm - Elite Synthetic Data Architect
   Domain: Next-Gen Utility-Scale Solar Updraft Tower (SUT) Aero-Turbine
   Description: Advanced 1000m chimney thermodynamic draft mapping, multi-megawatt 
                axial turbine variable pitch, and greenhouse canopy diurnal thermal 
                storage management system.
   ================================================================================
*)
VAR_INPUT
    bSystemEnable            : BOOL;     (* Main system enable interlock *)
    bEmergencyStop           : BOOL;     (* Safety relay OK signal - Active High = Safe *)
    rAmbientTemp             : REAL;     (* Ambient temperature (deg C) *)
    rCanopyTemp              : REAL;     (* Greenhouse canopy avg temp (deg C) *)
    rChimneyDraftVel         : REAL;     (* Measured draft velocity in chimney (m/s) *)
    rGridDemandMW            : REAL;     (* Power demand from the grid dispatcher (MW) *)
    rTurbineSpeedRPM         : REAL;     (* Actual turbine rotor speed (RPM) *)
    rVibrationLevel          : REAL;     (* Turbine bearing vibration (mm/s RMS) *)
END_VAR

VAR_OUTPUT
    bSystemReady             : BOOL;     (* System is primed and ready to generate power *)
    rTurbinePitchAngle       : REAL;     (* Blade pitch angle command to actuator (Degrees) *)
    rGeneratorTorqueSP       : REAL;     (* Generator torque setpoint to inverter (Nm) *)
    rActivePowerMW           : REAL;     (* Calculated active power output (MW) *)
    bAlarmVibration          : BOOL;     (* High vibration critical alarm *)
    bThermalOverload         : BOOL;     (* Canopy / draft temperature safety limit exceeded *)
    iOperatingState          : INT;      (* Current state machine step *)
END_VAR

VAR
    iState                   : INT := 0; 
    tDraftStabilizer         : TON;
    tVibrationDebounce       : TON;
    rCalculatedDeltaT        : REAL;
    rTargetDraftVel          : REAL;
    rPitchControllerKp       : REAL := 2.5;
    rPitchControllerKi       : REAL := 0.15;
    rPitchIntegralError      : REAL := 0.0;
    rSpeedError              : REAL;
    
    (* Constants for 1000m Thermodynamic Draft *)
    c_rMaxCanopyTemp         : REAL := 85.0;  (* Max allowable canopy temp deg C *)
    c_rMaxVibration          : REAL := 12.5;  (* Max vibration trip mm/s *)
    c_rNominalRPM            : REAL := 1500.0;
    c_rMinDraftVel           : REAL := 8.5;   (* Min draft for sync m/s *)
END_VAR

(* === MAIN SAFETY & INTERLOCK LOGIC === *)
IF NOT bEmergencyStop THEN
    bSystemReady       := FALSE;
    rTurbinePitchAngle := 90.0; (* Feather blades completely *)
    rGeneratorTorqueSP := 0.0;
    iOperatingState    := 999;  (* Fault state *)
    RETURN;
END_IF;

(* Vibration Monitoring with Debounce *)
tVibrationDebounce(IN := (rVibrationLevel > c_rMaxVibration), PT := T#2S);
IF tVibrationDebounce.Q THEN
    bAlarmVibration    := TRUE;
    iState             := 999; (* Force fault trip *)
END_IF;

(* Thermal Overload Check *)
IF rCanopyTemp > c_rMaxCanopyTemp THEN
    bThermalOverload := TRUE;
    (* We don't trip immediately, but we might throttle pitch to reduce flow and thus draft heat transfer if needed, or open vents *)
ELSE
    bThermalOverload := FALSE;
END_IF;

(* Thermodynamic calculations *)
rCalculatedDeltaT := rCanopyTemp - rAmbientTemp;

(* === MAIN STATE MACHINE === *)
CASE iState OF
    0: (* IDLE / STANDBY *)
        bSystemReady       := TRUE;
        rTurbinePitchAngle := 90.0;
        rGeneratorTorqueSP := 0.0;
        iOperatingState    := 0;
        
        IF bSystemEnable AND NOT bAlarmVibration THEN
            iState := 10;
        END_IF;

    10: (* PRIMING DRAFT - Waiting for aerodynamic stability *)
        iOperatingState := 10;
        (* Pitch blades to allow free-wheeling draft build-up *)
        rTurbinePitchAngle := 45.0; 
        
        tDraftStabilizer(IN := (rChimneyDraftVel >= c_rMinDraftVel), PT := T#30S);
        IF tDraftStabilizer.Q THEN
            tDraftStabilizer(IN := FALSE);
            iState := 20;
        END_IF;
        
        IF NOT bSystemEnable THEN
            tDraftStabilizer(IN := FALSE);
            iState := 0;
        END_IF;

    20: (* RAMP TO SYNCHRONOUS SPEED *)
        iOperatingState := 20;
        
        (* Simple PI control for RPM tracking *)
        rSpeedError := c_rNominalRPM - rTurbineSpeedRPM;
        rPitchIntegralError := rPitchIntegralError + (rSpeedError * 0.1); (* Assuming 100ms cycle *)
        
        (* Anti-windup *)
        IF rPitchIntegralError > 50.0 THEN rPitchIntegralError := 50.0; END_IF;
        IF rPitchIntegralError < -50.0 THEN rPitchIntegralError := -50.0; END_IF;
        
        (* Calculate pitch angle - less pitch = more torque from wind *)
        rTurbinePitchAngle := 45.0 - (rPitchControllerKp * rSpeedError + rPitchControllerKi * rPitchIntegralError);
        
        (* Bound pitch angle *)
        IF rTurbinePitchAngle < 0.0 THEN rTurbinePitchAngle := 0.0; END_IF;
        IF rTurbinePitchAngle > 90.0 THEN rTurbinePitchAngle := 90.0; END_IF;
        
        (* Check if synchronous speed reached *)
        IF ABS(rSpeedError) < 10.0 THEN
            iState := 30;
        END_IF;

    30: (* MPPT / ACTIVE POWER GENERATION *)
        iOperatingState := 30;
        
        (* Map grid demand to torque setpoint given current RPM and draft limit *)
        (* P(MW) = T(kNm) * w(rad/s) -> T = P / w *)
        IF rTurbineSpeedRPM > 0.0 THEN
            rGeneratorTorqueSP := (rGridDemandMW * 1000.0) / (rTurbineSpeedRPM * 0.104719755); 
        ELSE
            rGeneratorTorqueSP := 0.0;
        END_IF;
        
        (* Maintain optimum aerodynamic efficiency via pitch control *)
        (* Here pitch targets a specific tip-speed ratio, simplified for this block *)
        rTurbinePitchAngle := 15.0 + (rCalculatedDeltaT * 0.05); 
        
        rActivePowerMW := rGeneratorTorqueSP * (rTurbineSpeedRPM * 0.104719755) / 1000.0;

        IF NOT bSystemEnable THEN
            iState := 40; (* Go to normal stop *)
        END_IF;
        
    40: (* NORMAL STOP *)
        iOperatingState := 40;
        rGeneratorTorqueSP := 0.0;
        rTurbinePitchAngle := 90.0; (* Feather blades *)
        rActivePowerMW := 0.0;
        
        IF rTurbineSpeedRPM < 50.0 THEN
            iState := 0;
        END_IF;

    999: (* FAULT TRIPPED *)
        iOperatingState := 999;
        bSystemReady := FALSE;
        rTurbinePitchAngle := 90.0;
        rGeneratorTorqueSP := 0.0;
        
        IF bSystemEnable = FALSE AND bEmergencyStop = TRUE AND bAlarmVibration = FALSE THEN
            iState := 0; (* Reset fault if enable toggled and E-Stop OK *)
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

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
