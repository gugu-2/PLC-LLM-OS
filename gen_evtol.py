import json
import uuid
import os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Commercial Aviation Electric Vertical Takeoff and Landing (eVTOL) Tilt-Rotor**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., 4-axis distributed electric propulsion (DEP) torque vectoring, transition phase gyroscopic decoupling, and high-voltage (800V) battery thermal runway mitigation). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_eVTOL_TiltRotorControl\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Commercial Aviation Electric Vertical Takeoff and Landing (eVTOL) Tilt-Rotor

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_eVTOL_TiltRotorControl
VAR_INPUT
    (* System and Safety Signals *)
    bEnableSystem : BOOL; (* Main power and logic enable *)
    bEmergencyStop : BOOL; (* Critical safety interlock, true = healthy *)
    
    (* Physical Measurements *)
    rBatteryTemp : REAL; (* 800V HV Battery max cell temperature [°C] *)
    rTiltAngleFbk : REAL; (* Current nacelle tilt angle [deg] (0=Hover, 90=Cruise) *)
    rInverterTemp_1 : REAL; (* Motor 1 inverter temp [°C] *)
    
    (* Pilot / Autonomous Flight Controller Commands *)
    rPitchCmd : REAL; (* Pilot/Auto pitch command [-1.0 to 1.0] *)
    rRollCmd : REAL; (* Pilot/Auto roll command [-1.0 to 1.0] *)
    rYawCmd : REAL; (* Pilot/Auto yaw command [-1.0 to 1.0] *)
    rHeaveCmd : REAL; (* Vertical lift command [0.0 to 1.0] *)
END_VAR
VAR_OUTPUT
    (* System Status Flags *)
    bSystemReady : BOOL; (* Ready for flight operation *)
    bThermalAlarm : BOOL; (* HV Battery or Inverter critical thermal warning *)
    bTransitionActive : BOOL; (* Nacelle transition in progress *)
    
    (* Distributed Electric Propulsion Torque Commands *)
    rMotorTorqueCmd_1 : REAL; (* Torque command to Front-Left Motor [Nm] *)
    rMotorTorqueCmd_2 : REAL; (* Torque command to Front-Right Motor [Nm] *)
    rMotorTorqueCmd_3 : REAL; (* Torque command to Rear-Left Motor [Nm] *)
    rMotorTorqueCmd_4 : REAL; (* Torque command to Rear-Right Motor [Nm] *)
    rTiltActuatorCmd : REAL; (* Actuator command for nacelle tilt [-1.0 to 1.0] *)
END_VAR
VAR
    (* Internal State and Timers *)
    iFlightState : INT := 0; (* 0=Init, 10=Hover, 20=Transition, 30=Cruise, 99=Fault *)
    tThermalRunwayTimer : TON;
    
    (* Aerodynamic & Torque Calculations *)
    rGyroscopicDecouplingFactor : REAL;
    rMaxAllowedTorque : REAL := 1500.0;
    rBaseTorque : REAL;
END_VAR

(* === MAIN LOGIC === *)
(* Safety Interlocks & Hardware Check *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    rMotorTorqueCmd_1 := 0.0;
    rMotorTorqueCmd_2 := 0.0;
    rMotorTorqueCmd_3 := 0.0;
    rMotorTorqueCmd_4 := 0.0;
    rTiltActuatorCmd := 0.0;
    iFlightState := 99;
    RETURN;
END_IF;

(* High Voltage (800V) Battery Thermal Runaway Mitigation *)
(* Hysteresis and timing applied to prevent nuisance trips while ensuring aircraft safety *)
tThermalRunwayTimer(IN := (rBatteryTemp > 85.0), PT := T#2S);
IF tThermalRunwayTimer.Q THEN
    bThermalAlarm := TRUE;
    rMaxAllowedTorque := 500.0; (* Severe derating - Emergency landing mode *)
ELSIF rBatteryTemp > 75.0 OR rInverterTemp_1 > 90.0 THEN
    bThermalAlarm := TRUE;
    rMaxAllowedTorque := 1000.0; (* Moderate derating to stabilize thermal buildup *)
ELSE
    bThermalAlarm := FALSE;
    rMaxAllowedTorque := 1500.0; (* Normal flight envelope *)
END_IF;

(* Gyroscopic Decoupling Matrix Calculation for Transition Phase *)
(* During tilt, the heavy nacelle rotors induce strong gyroscopic precession forces which must be countered *)
rGyroscopicDecouplingFactor := rTiltAngleFbk * 0.01111; (* Normalized 0.0 to 1.0 for 0 to 90 degrees *)

(* Finite State Machine for eVTOL Flight Phase Control *)
CASE iFlightState OF
    0: (* INIT PHASE *)
        bTransitionActive := FALSE;
        IF bEnableSystem AND NOT bThermalAlarm THEN
            iFlightState := 10;
            bSystemReady := TRUE;
        END_IF;
        
    10: (* HOVER PHASE - VTOL Operation *)
        (* 4-axis DEP Torque Vectoring purely based on Heave, Pitch, Roll, Yaw differential thrust *)
        rBaseTorque := rHeaveCmd * rMaxAllowedTorque;
        rMotorTorqueCmd_1 := rBaseTorque + (rPitchCmd * 100.0) + (rRollCmd * 100.0) + (rYawCmd * 50.0);
        rMotorTorqueCmd_2 := rBaseTorque + (rPitchCmd * 100.0) - (rRollCmd * 100.0) - (rYawCmd * 50.0);
        rMotorTorqueCmd_3 := rBaseTorque - (rPitchCmd * 100.0) + (rRollCmd * 100.0) - (rYawCmd * 50.0);
        rMotorTorqueCmd_4 := rBaseTorque - (rPitchCmd * 100.0) - (rRollCmd * 100.0) + (rYawCmd * 50.0);
        
        (* Check criteria for entering forward flight transition *)
        IF rTiltAngleFbk > 5.0 THEN
            iFlightState := 20;
            bTransitionActive := TRUE;
        END_IF;
        
    20: (* TRANSITION PHASE - Complex Gyroscopic & Aerodynamic Blending *)
        (* Blended aerodynamic and direct thrust control - Wing lift begins to support aircraft weight *)
        rBaseTorque := rHeaveCmd * rMaxAllowedTorque * (1.0 - (rGyroscopicDecouplingFactor * 0.5));
        
        (* Apply gyroscopic decoupling torque offsets dynamically as tilt progresses *)
        rMotorTorqueCmd_1 := rBaseTorque + (rPitchCmd * 80.0) + (rYawCmd * 50.0 * rGyroscopicDecouplingFactor);
        rMotorTorqueCmd_2 := rBaseTorque + (rPitchCmd * 80.0) - (rYawCmd * 50.0 * rGyroscopicDecouplingFactor);
        rMotorTorqueCmd_3 := rBaseTorque - (rPitchCmd * 40.0) + (rRollCmd * 80.0);
        rMotorTorqueCmd_4 := rBaseTorque - (rPitchCmd * 40.0) - (rRollCmd * 80.0);
        
        IF rTiltAngleFbk >= 85.0 THEN
            iFlightState := 30;
            bTransitionActive := FALSE;
        END_IF;
        
    30: (* CRUISE PHASE - Forward Wing-Borne Flight *)
        (* Lift generated by wings, front motors provide forward thrust, rear rotors stowed *)
        rMotorTorqueCmd_1 := rHeaveCmd * rMaxAllowedTorque; 
        rMotorTorqueCmd_2 := rHeaveCmd * rMaxAllowedTorque;
        rMotorTorqueCmd_3 := 0.0; (* Rear rotors aerodynamic braking / feathered *)
        rMotorTorqueCmd_4 := 0.0;
        
        IF rTiltAngleFbk < 85.0 THEN
            iFlightState := 20;
            bTransitionActive := TRUE;
        END_IF;
        
    99: (* FAULT / DEGRADED MODE *)
        bSystemReady := FALSE;
        bTransitionActive := FALSE;
        rMotorTorqueCmd_1 := 0.0;
        rMotorTorqueCmd_2 := 0.0;
        rMotorTorqueCmd_3 := 0.0;
        rMotorTorqueCmd_4 := 0.0;
        IF NOT bEnableSystem THEN
            iFlightState := 0;
        END_IF;
        
END_CASE;

(* Actuator Limits Enforcer - Prevent Over-Torque Commands to Inverters *)
IF rMotorTorqueCmd_1 > rMaxAllowedTorque THEN rMotorTorqueCmd_1 := rMaxAllowedTorque; END_IF;
IF rMotorTorqueCmd_1 < 0.0 THEN rMotorTorqueCmd_1 := 0.0; END_IF;

IF rMotorTorqueCmd_2 > rMaxAllowedTorque THEN rMotorTorqueCmd_2 := rMaxAllowedTorque; END_IF;
IF rMotorTorqueCmd_2 < 0.0 THEN rMotorTorqueCmd_2 := 0.0; END_IF;

IF rMotorTorqueCmd_3 > rMaxAllowedTorque THEN rMotorTorqueCmd_3 := rMaxAllowedTorque; END_IF;
IF rMotorTorqueCmd_3 < 0.0 THEN rMotorTorqueCmd_3 := 0.0; END_IF;

IF rMotorTorqueCmd_4 > rMaxAllowedTorque THEN rMotorTorqueCmd_4 := rMaxAllowedTorque; END_IF;
IF rMotorTorqueCmd_4 < 0.0 THEN rMotorTorqueCmd_4 := 0.0; END_IF;

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
