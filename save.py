import json, uuid, os

prompt = """<USER_REQUEST>
You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Next-Gen Subsea Multiphase Booster Pump (MPP)**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., 10,000 HP variable-speed drive water/oil/gas fraction active compensation, helicon-axial impeller thrust bearing dynamic balancing, and hydrate inhibitor subsea chemical injection). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_SubseaMultiphasePump\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Next-Gen Subsea Multiphase Booster Pump (MPP)

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT.
</USER_REQUEST>"""

code = """```iec-st
FUNCTION_BLOCK FB_SubseaMPP_ActiveCompensation
VAR_INPUT
    (* Operational Commands *)
    bSystemEnable           : BOOL;     (* Main Enable for Subsea Multiphase Booster System *)
    bEmergencyStop          : BOOL;     (* Subsea Safety Module OK Signal (Normally High) *)
    bAcknowledgeFault       : BOOL;     (* Topside operator fault acknowledge *)
    
    (* Process Parameters *)
    rSuctionPressure        : REAL;     (* Pump suction pressure [bar] *)
    rDischargePressure      : REAL;     (* Pump discharge pressure [bar] *)
    rProcessFluidTemp       : REAL;     (* Multiphase fluid temperature [deg C] *)
    rGasVolumeFraction      : REAL;     (* GVF input from subsea multiphase meter [%] *)
    rWaterCut               : REAL;     (* Water Cut measurement [%] *)
    
    (* Mechanical Parameters *)
    rMotorSpeedRPM          : REAL;     (* Actual Variable Speed Drive RPM *)
    rVibrationAxial         : REAL;     (* Thrust bearing axial vibration [mm/s] *)
    rVibrationRadial        : REAL;     (* Journal bearing radial vibration [mm/s] *)
    
    (* Chemical Injection *)
    rHydrateInhibitorLevel  : REAL;     (* MEG/Methanol storage tank level [%] *)
END_VAR
VAR_OUTPUT
    (* Operational Status *)
    bReadyToStart           : BOOL;     (* Pump interlocks satisfied, ready to start *)
    bRunning                : BOOL;     (* Pump is running *)
    
    (* Control Outputs *)
    rSpeedReferenceVSD      : REAL;     (* Commanded RPM to the topside VSD *)
    rThrustBalanceValveCmd  : REAL;     (* Helicon-axial balance drum compensation valve [0-100%] *)
    rChemInjectionDoseRate  : REAL;     (* Hydrate inhibitor pump speed reference [L/h] *)
    
    (* Fault & Alarms *)
    bAlarmHighVibration     : BOOL;     (* Vibration exceeds alarm limit *)
    bAlarmLowSuctionPress   : BOOL;     (* Suction pressure critically low *)
    bTrip                   : BOOL;     (* System tripped (safety or operational trip) *)
    iTripCode               : INT;      (* Diagnostics code for trip cause *)
END_VAR
VAR
    (* Internal States and Timers *)
    iState                  : INT := 0; (* 0: INIT, 10: READY, 20: RAMP_UP, 30: RUN, 40: COAST_DOWN, 99: FAULT *)
    tStartupTimer           : TON;
    tCoastDownTimer         : TON;
    tChemDoseTimer          : TON;
    
    (* Internal Calculations *)
    rDifferentialPress      : REAL;
    rDynamicThrustSetp      : REAL;
    rTargetRPM              : REAL;
    rMaxGVF_Limit           : REAL := 85.0; (* Max Gas Volume Fraction allowable [%] *)
    
    (* PID Controllers for dynamic compensation *)
    rKp_Thrust              : REAL := 1.25;
    rKi_Thrust              : REAL := 0.05;
    rIntegralThrust         : REAL := 0.0;
    rErrorThrust            : REAL;
END_VAR

(* === SAFETY & INTERLOCKS === *)
IF NOT bEmergencyStop THEN
    (* Immediate system shutdown *)
    bReadyToStart := FALSE;
    bRunning := FALSE;
    rSpeedReferenceVSD := 0.0;
    rThrustBalanceValveCmd := 100.0; (* Fail-safe open to balance thrust *)
    rChemInjectionDoseRate := 0.0;
    bTrip := TRUE;
    iTripCode := 9999; (* ESD Activated *)
    iState := 99;
    RETURN;
END_IF;

(* Process calculations *)
rDifferentialPress := rDischargePressure - rSuctionPressure;

(* Hydrate Risk Assessment: Increase chemical dose if Temp < 15C and WaterCut > 10% *)
IF rProcessFluidTemp < 15.0 AND rWaterCut > 10.0 THEN
    rChemInjectionDoseRate := 50.0 + (15.0 - rProcessFluidTemp) * 5.0; (* Dynamic dosing curve *)
ELSE
    rChemInjectionDoseRate := 10.0; (* Base maintenance dose *)
END_IF;
IF rHydrateInhibitorLevel < 5.0 THEN
    rChemInjectionDoseRate := 0.0; (* Prevent dry running of injection pump *)
END_IF;

(* Main State Machine *)
CASE iState OF
    0: (* INIT / FAULT RECOVERY *)
        bReadyToStart := FALSE;
        bRunning := FALSE;
        rSpeedReferenceVSD := 0.0;
        
        IF bAcknowledgeFault AND NOT bTrip THEN
            IF rSuctionPressure > 10.0 AND rVibrationAxial < 2.5 THEN
                iState := 10; (* Proceed to READY *)
            END_IF;
        END_IF;
        
        (* Clear Trips if conditions normalize *)
        IF bTrip AND bAcknowledgeFault THEN
            bTrip := FALSE;
            iTripCode := 0;
        END_IF;

    10: (* READY *)
        bReadyToStart := TRUE;
        bAlarmLowSuctionPress := (rSuctionPressure < 12.0);
        
        IF bSystemEnable AND bReadyToStart AND NOT bAlarmLowSuctionPress THEN
            iState := 20;
            tStartupTimer(IN := FALSE);
        END_IF;

    20: (* RAMP_UP *)
        bReadyToStart := FALSE;
        bRunning := TRUE;
        tStartupTimer(IN := TRUE, PT := T#60S);
        
        (* Ramp speed gradually up to minimum flow threshold *)
        rSpeedReferenceVSD := rSpeedReferenceVSD + 5.0;
        IF rSpeedReferenceVSD > 1500.0 THEN
            rSpeedReferenceVSD := 1500.0;
        END_IF;
        
        IF tStartupTimer.Q THEN
            iState := 30;
        END_IF;

    30: (* RUNNING / ACTIVE COMPENSATION *)
        bRunning := TRUE;
        
        (* Multiphase GVF Compensation: Adjust target RPM based on gas fraction *)
        IF rGasVolumeFraction > rMaxGVF_Limit THEN
            (* High gas slug detected: reduce speed to prevent gas lock and impeller cavitation *)
            rTargetRPM := 1800.0 - (rGasVolumeFraction - rMaxGVF_Limit) * 20.0;
        ELSE
            (* Normal liquid/multiphase boosting *)
            rTargetRPM := 3600.0; (* Nominal speed for 10k HP MPP *)
        END_IF;
        
        (* Smooth speed transitions *)
        IF rSpeedReferenceVSD < rTargetRPM THEN
            rSpeedReferenceVSD := rSpeedReferenceVSD + 2.0;
        ELSIF rSpeedReferenceVSD > rTargetRPM THEN
            rSpeedReferenceVSD := rSpeedReferenceVSD - 5.0; (* Faster deceleration for gas slugs *)
        END_IF;
        
        (* Dynamic Thrust Bearing Balancing using Helicon-Axial Valve *)
        (* Target differential pressure is normalized for the thrust drum *)
        rDynamicThrustSetp := (rMotorSpeedRPM / 3600.0) * 45.0; (* Estimated thrust load *)
        rErrorThrust := rDynamicThrustSetp - rDifferentialPress;
        
        rIntegralThrust := rIntegralThrust + (rErrorThrust * rKi_Thrust);
        (* Anti-windup *)
        IF rIntegralThrust > 100.0 THEN rIntegralThrust := 100.0; END_IF;
        IF rIntegralThrust < 0.0 THEN rIntegralThrust := 0.0; END_IF;
        
        rThrustBalanceValveCmd := (rErrorThrust * rKp_Thrust) + rIntegralThrust;
        
        (* Limits for Balance Valve *)
        IF rThrustBalanceValveCmd > 100.0 THEN rThrustBalanceValveCmd := 100.0; END_IF;
        IF rThrustBalanceValveCmd < 10.0 THEN rThrustBalanceValveCmd := 10.0; END_IF;
        
        (* Trip Conditions during run *)
        IF rVibrationAxial > 8.0 OR rVibrationRadial > 8.0 THEN
            bTrip := TRUE;
            iTripCode := 101; (* High Vibration Trip *)
            iState := 40;
        END_IF;
        
        IF NOT bSystemEnable THEN
            iState := 40;
        END_IF;

    40: (* COAST_DOWN *)
        bRunning := FALSE;
        rSpeedReferenceVSD := 0.0;
        rThrustBalanceValveCmd := 100.0; (* Open to relieve pressure during coast down *)
        
        tCoastDownTimer(IN := TRUE, PT := T#120S);
        IF tCoastDownTimer.Q OR rMotorSpeedRPM < 50.0 THEN
            tCoastDownTimer(IN := FALSE);
            iState := 99; (* Enter fault/standby state after stopping *)
            IF NOT bTrip THEN
                iState := 0;
            END_IF;
        END_IF;

    99: (* FAULT HANDLING *)
        bReadyToStart := FALSE;
        bRunning := FALSE;
        rSpeedReferenceVSD := 0.0;
        
        IF bAcknowledgeFault AND rMotorSpeedRPM < 10.0 THEN
            iState := 0;
        END_IF;

END_CASE;

(* Final Alarm Evaluations *)
bAlarmHighVibration := (rVibrationAxial > 5.0 OR rVibrationRadial > 5.0);

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
