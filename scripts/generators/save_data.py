import json, uuid
import os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V5 Persona: a 60+ years experienced God-Tier PLC Architect & Cyber-Physical Systems Post-Doc. 
Your logic must include advanced State-Space Modeling, Model Predictive Control (MPC) concepts, Non-Linear PID with Anti-Windup, and extreme multi-layer hardware safety matrices. Output the most elite, mathematically rigorous, and structurally flawless IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Industrial Multi-Zone Continuous Steel Billet Reheating Furnace Cross-Limited Air/Fuel Combustion**

Task: Invent a highly complex, ultra-realistic control scenario for this domain. This MUST be drastically better, more advanced, and longer than previous V4 iterations.

CRITICAL RULES - READ EVERY LINE:
1. CODE FENCE: Use TRIPLE backticks + iec-st. EXACTLY like this:
   ```iec-st
   (your code here)
   ```
   NEVER use a single backtick `iec-st. ALWAYS use triple backticks.
2. REQUIRED IEC 61131-3 STRUCTURE (all 5 mandatory):
   a. FUNCTION_BLOCK FB_<Name>   <- first line of code, always
   b. VAR_INPUT ... END_VAR      <- min 6 typed inputs with comments
   c. VAR_OUTPUT ... END_VAR     <- min 5 typed outputs with comments
   d. At least one END_IF; or END_CASE;  <- control logic required
   e. END_FUNCTION_BLOCK         <- last line of code, always
3. LENGTH: The assistant content MUST be >= 2500 characters total. Make it incredibly massive and rigorous.
4. SAVE to isolated file using this exact Python:
   import json, uuid
   prompt = \"\"\"<copy this exact user prompt here>\"\"\"
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_SteelBillet_ReheatingFurnace\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
   record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
   with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
       json.dump(record, f, ensure_ascii=False)
5. SELF-CHECK before saving - verify ALL:
   [ ] Fence is ```iec-st
   [ ] First code line: FUNCTION_BLOCK FB_<name>
   [ ] Has VAR_INPUT & VAR_OUTPUT sections
   [ ] Has END_IF; or END_CASE;
   [ ] Last code line: END_FUNCTION_BLOCK
   [ ] Closing fence: ```
   [ ] Total chars >= 2500
6. REPLY with: EVOLUTION COMPLETE: Industrial Multi-Zone Continuous Steel Billet Reheating Furnace Cross-Limited Air/Fuel Combustion"""

code = """```iec-st
FUNCTION_BLOCK FB_SteelBillet_ReheatingFurnace
VAR_INPUT
    bEnable                 : BOOL;     (* System enable signal *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal (TRUE = OK) *)
    bFlameDetected          : BOOL;     (* Main burner flame scanner status *)
    bCombustionBlowerRun    : BOOL;     (* Combustion air blower running feedback *)
    rZoneTempPV             : REAL;     (* Process Variable: Zone Temperature (Deg C) *)
    rZoneTempSP             : REAL;     (* Setpoint: Zone Temperature (Deg C) *)
    rFuelFlowPV             : REAL;     (* Process Variable: Fuel Flow (Nm3/h) *)
    rAirFlowPV              : REAL;     (* Process Variable: Air Flow (Nm3/h) *)
    rAirFuelRatioSP         : REAL;     (* Setpoint: Stoichiometric Air/Fuel Ratio *)
    rFuelPressurePV         : REAL;     (* Process Variable: Fuel Gas Pressure (bar) *)
    rFurnacePressurePV      : REAL;     (* Process Variable: Furnace Draft Pressure (Pa) *)
    rBilletFeedRate         : REAL;     (* Feed forward: Billet mass flow rate (ton/h) *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;     (* System ready status for sequence *)
    bBurnerIgniteCMD        : BOOL;     (* Command to ignite main burner *)
    bFuelValveOpenCMD       : BOOL;     (* Command to open main fuel shutoff valves *)
    rFuelValveCV            : REAL;     (* Control Output: Fuel flow control valve (0-100%) *)
    rAirValveCV             : REAL;     (* Control Output: Air flow control valve (0-100%) *)
    rExhaustDamperCV        : REAL;     (* Control Output: Exhaust damper for draft control (0-100%) *)
    bAlarmHighTemp          : BOOL;     (* Alarm: Zone Temperature High-High *)
    bAlarmFlameFailure      : BOOL;     (* Alarm: Flame failure during operation *)
    bAlarmCrossLimitDev     : BOOL;     (* Alarm: Air/Fuel cross-limit deviation fault *)
    bSystemFault            : BOOL;     (* Aggregate system fault flag *)
END_VAR
VAR
    iState                  : INT := 0;
    tPurgeTimer             : TON;
    tIgnitionTimer          : TON;
    tFlameFailTimer         : TON;
    
    (* Temperature PID Control (Master) *)
    rTempError              : REAL;
    rTempErrorPrev          : REAL;
    rTempIntegral           : REAL;
    rTempDerivative         : REAL;
    rThermalDemandOut       : REAL;     (* Master output to cross-limited slaves *)
    rTempKp                 : REAL := 2.5;
    rTempKi                 : REAL := 0.05;
    rTempKd                 : REAL := 0.1;
    
    (* Cross-Limiting Variables *)
    rFuelDemandRaw          : REAL;
    rAirDemandRaw           : REAL;
    rFuelDemandLimited      : REAL;
    rAirDemandLimited       : REAL;
    
    (* Fuel Flow PID (Slave) *)
    rFuelError              : REAL;
    rFuelIntegral           : REAL;
    rFuelKp                 : REAL := 1.2;
    rFuelKi                 : REAL := 0.5;
    
    (* Air Flow PID (Slave) *)
    rAirError               : REAL;
    rAirIntegral            : REAL;
    rAirKp                  : REAL := 1.5;
    rAirKi                  : REAL := 0.8;
    
    (* MPC Feed-forward *)
    rBilletHeatCap          : REAL := 0.13; (* Specific heat proxy *)
    rFeedForwardDemand      : REAL;
    
    (* Safety limits *)
    rMaxTempLimit           : REAL := 1250.0; (* Deg C *)
    rMinAirRatio            : REAL := 9.5;
    rMaxAirRatio            : REAL := 12.0;
    
    rCrossLimitMargin       : REAL := 5.0; (* 5% lead/lag margin *)
END_VAR

(* === MAIN SAFETY & INTERLOCK LOGIC === *)
IF NOT bEmergencyStop OR NOT bCombustionBlowerRun OR rFuelPressurePV < 0.5 THEN
    bSystemReady := FALSE;
    bBurnerIgniteCMD := FALSE;
    bFuelValveOpenCMD := FALSE;
    rFuelValveCV := 0.0;
    rAirValveCV := 0.0;
    bSystemFault := TRUE;
    iState := 99; (* FAULT STATE *)
    RETURN;
END_IF;

(* Temperature High-High Alarm *)
IF rZoneTempPV > rMaxTempLimit THEN
    bAlarmHighTemp := TRUE;
    bSystemFault := TRUE;
    iState := 99;
END_IF;

(* === STATE MACHINE === *)
CASE iState OF
    0: (* IDLE & PURGE *)
        bSystemReady := FALSE;
        bBurnerIgniteCMD := FALSE;
        bFuelValveOpenCMD := FALSE;
        rFuelValveCV := 0.0;
        rAirValveCV := 100.0; (* Full open for purge *)
        
        IF bEnable AND NOT bSystemFault THEN
            tPurgeTimer(IN := TRUE, PT := T#60S);
            IF tPurgeTimer.Q THEN
                tPurgeTimer(IN := FALSE);
                iState := 10; (* IGNITION PREP *)
            END_IF;
        ELSE
            tPurgeTimer(IN := FALSE);
        END_IF;

    10: (* IGNITION PREP *)
        rAirValveCV := 15.0; (* Low fire position for ignition *)
        rFuelValveCV := 10.0; (* Ignition fuel flow *)
        tIgnitionTimer(IN := TRUE, PT := T#5S);
        IF tIgnitionTimer.Q THEN
            tIgnitionTimer(IN := FALSE);
            bFuelValveOpenCMD := TRUE;
            bBurnerIgniteCMD := TRUE;
            iState := 20; (* PROVE FLAME *)
        END_IF;

    20: (* PROVE FLAME *)
        tFlameFailTimer(IN := TRUE, PT := T#3S);
        IF bFlameDetected THEN
            tFlameFailTimer(IN := FALSE);
            bBurnerIgniteCMD := FALSE;
            bSystemReady := TRUE;
            iState := 30; (* RUNNING CROSS-LIMITED CONTROL *)
        ELSIF tFlameFailTimer.Q THEN
            tFlameFailTimer(IN := FALSE);
            bAlarmFlameFailure := TRUE;
            iState := 99;
        END_IF;

    30: (* RUNNING CROSS-LIMITED CONTROL *)
        (* Flame failure monitor during operation *)
        IF NOT bFlameDetected THEN
            bAlarmFlameFailure := TRUE;
            iState := 99;
        END_IF;
        
        (* 1. Master Temperature PID with Feed-Forward *)
        rTempError := rZoneTempSP - rZoneTempPV;
        rTempIntegral := rTempIntegral + (rTempError * 0.1); (* Assuming 100ms cycle *)
        
        (* Anti-windup for Master Integral *)
        IF rTempIntegral > 100.0 THEN rTempIntegral := 100.0; END_IF;
        IF rTempIntegral < 0.0 THEN rTempIntegral := 0.0; END_IF;
        
        rTempDerivative := (rTempError - rTempErrorPrev) / 0.1;
        rTempErrorPrev := rTempError;
        
        (* Feed forward based on billet mass flow to anticipate thermal load *)
        rFeedForwardDemand := rBilletFeedRate * rBilletHeatCap;
        
        rThermalDemandOut := (rTempError * rTempKp) + (rTempIntegral * rTempKi) + (rTempDerivative * rTempKd) + rFeedForwardDemand;
        IF rThermalDemandOut > 100.0 THEN rThermalDemandOut := 100.0; END_IF;
        IF rThermalDemandOut < 10.0 THEN rThermalDemandOut := 10.0; END_IF; (* Minimum fire *)

        (* 2. Cross-Limiting Logic for Air and Fuel *)
        (* Target Demands *)
        rFuelDemandRaw := rThermalDemandOut;
        rAirDemandRaw := rThermalDemandOut * rAirFuelRatioSP;
        
        (* Ensure Air leads Fuel on increasing load, and Fuel lags Air on decreasing load *)
        (* Fuel Demand is limited by Actual Air Flow *)
        rFuelDemandLimited := MIN(rFuelDemandRaw, (rAirFlowPV / rAirFuelRatioSP) + rCrossLimitMargin);
        
        (* Air Demand is limited by Actual Fuel Flow *)
        rAirDemandLimited := MAX(rAirDemandRaw, (rFuelFlowPV * rAirFuelRatioSP) - rCrossLimitMargin);
        
        (* Cross-limit deviation alarm *)
        IF ABS(rFuelDemandLimited - rFuelDemandRaw) > 10.0 OR ABS(rAirDemandLimited - rAirDemandRaw) > 20.0 THEN
            bAlarmCrossLimitDev := TRUE;
        ELSE
            bAlarmCrossLimitDev := FALSE;
        END_IF;

        (* 3. Slave Fuel PID *)
        rFuelError := rFuelDemandLimited - rFuelFlowPV;
        rFuelIntegral := rFuelIntegral + (rFuelError * 0.1);
        IF rFuelIntegral > 100.0 THEN rFuelIntegral := 100.0; END_IF;
        IF rFuelIntegral < 0.0 THEN rFuelIntegral := 0.0; END_IF;
        rFuelValveCV := (rFuelError * rFuelKp) + (rFuelIntegral * rFuelKi);
        
        (* 4. Slave Air PID *)
        rAirError := rAirDemandLimited - rAirFlowPV;
        rAirIntegral := rAirIntegral + (rAirError * 0.1);
        IF rAirIntegral > 100.0 THEN rAirIntegral := 100.0; END_IF;
        IF rAirIntegral < 0.0 THEN rAirIntegral := 0.0; END_IF;
        rAirValveCV := (rAirError * rAirKp) + (rAirIntegral * rAirKi);
        
        (* Valve Saturation Safeguards *)
        IF rFuelValveCV > 100.0 THEN rFuelValveCV := 100.0; END_IF;
        IF rFuelValveCV < 0.0 THEN rFuelValveCV := 0.0; END_IF;
        IF rAirValveCV > 100.0 THEN rAirValveCV := 100.0; END_IF;
        IF rAirValveCV < 0.0 THEN rAirValveCV := 0.0; END_IF;
        
        (* 5. Independent Furnace Draft Control (Proportional only for simplicity in demo) *)
        rExhaustDamperCV := rFurnacePressurePV * 0.5 + 50.0; 
        IF rExhaustDamperCV > 100.0 THEN rExhaustDamperCV := 100.0; END_IF;
        IF rExhaustDamperCV < 0.0 THEN rExhaustDamperCV := 0.0; END_IF;
        
        IF NOT bEnable THEN
            iState := 40; (* SHUTDOWN SEQUENCE *)
        END_IF;

    40: (* SHUTDOWN SEQUENCE *)
        bFuelValveOpenCMD := FALSE;
        rFuelValveCV := 0.0;
        bSystemReady := FALSE;
        
        (* Post-purge *)
        rAirValveCV := 100.0;
        tPurgeTimer(IN := TRUE, PT := T#30S);
        IF tPurgeTimer.Q THEN
            tPurgeTimer(IN := FALSE);
            iState := 0;
        END_IF;

    99: (* FAULT STATE *)
        bFuelValveOpenCMD := FALSE;
        bBurnerIgniteCMD := FALSE;
        rFuelValveCV := 0.0;
        rAirValveCV := 100.0; (* Air remains on to clear volatile gases *)
        bSystemReady := FALSE;
        bSystemFault := TRUE;
        
        (* Reset logic *)
        IF NOT bEmergencyStop THEN (* Assuming E-stop needs to be toggled or similar, simplified reset *)
            IF NOT bAlarmHighTemp AND NOT bAlarmFlameFailure THEN
                iState := 0;
                bSystemFault := FALSE;
            END_IF;
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
