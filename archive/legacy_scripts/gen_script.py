import json, uuid, os

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Next-Gen Heavy-Duty Hydrogen Fuel Cell Mining Truck Powertrain**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., 2MW PEM fuel cell stack air compressor surge mapping, ultra-capacitor transient load leveling, and liquid cooling loop two-phase boiling suppression). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_FuelCellMiningTruck\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Next-Gen Heavy-Duty Hydrogen Fuel Cell Mining Truck Powertrain

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_FuelCellPowertrainCoord
TITLE = 'Next-Gen Heavy-Duty H2 Fuel Cell Mining Truck Powertrain Coordinator'
// -----------------------------------------------------------------------------
// Description:
// Coordinates a 2MW PEM fuel cell stack, ultra-capacitor transient leveling,
// and liquid cooling two-phase boiling suppression for extreme load profiles
// in a heavy-duty mining truck.
// -----------------------------------------------------------------------------

VAR_INPUT
    (* Mandatory inputs *)
    bSystemEnable           : BOOL;     (* System master enable signal *)
    bEmergencyStop          : BOOL;     (* Safety circuit healthy signal *)
    rTorqueRequest_Nm       : REAL;     (* Operator/Autonomous drive torque request *)
    rFC_StackVoltage_V      : REAL;     (* Real-time fuel cell stack voltage (V) *)
    rFC_StackCurrent_A      : REAL;     (* Real-time fuel cell stack current (A) *)
    rUC_StateOfCharge_Pct   : REAL;     (* Ultra-capacitor SoC (0.0 - 100.0%) *)
    rCoolantTempOut_C       : REAL;     (* Stack coolant outlet temperature (C) *)
    rCompressorSpeed_RPM    : REAL;     (* Air compressor actual speed *)
END_VAR

VAR_OUTPUT
    (* Mandatory outputs *)
    bPowertrainReady        : BOOL;     (* Powertrain ready for traction *)
    rFC_PowerDemand_kW      : REAL;     (* Commanded power to fuel cell DC/DC *)
    rUC_PowerDemand_kW      : REAL;     (* Commanded power to UC DC/DC (positive=discharge) *)
    rCoolantPumpCmd_Pct     : REAL;     (* Coolant pump speed command (0-100%) *)
    rCompressorCmd_RPM      : REAL;     (* Air compressor speed command *)
    bCriticalAlarm          : BOOL;     (* System fault / derate active *)
END_VAR

VAR
    (* Internal State Machine *)
    iOpState                : INT := 0; (* 0:Off, 10:Init, 20:Precharge, 30:Run, 99:Fault *)
    
    (* Timers & Filters *)
    tInitDelay              : TON;
    tFaultDelay             : TON;
    rFilteredTorqueReq      : REAL;
    
    (* Thermodynamic / Surge Limits *)
    rMaxStackPower_kW       : REAL := 2000.0;
    rStackThermalLimit_C    : REAL := 85.0;
    rSurgeMargin            : REAL := 1.15;
    
    (* Calculated Values *)
    rTractionPowerReq_kW    : REAL;
    rAvailableUCPower_kW    : REAL;
    rThermalDerateFactor    : REAL;
    
    (* Constants *)
    c_MotorSpeed_RPM        : REAL := 1500.0; (* Assuming nominal speed for power calc simplify *)
END_VAR

(* === MAIN LOGIC === *)

(* Safety and Enable Interlocks *)
IF NOT bEmergencyStop THEN
    iOpState := 99; // Force fault state
    bPowertrainReady := FALSE;
    rFC_PowerDemand_kW := 0.0;
    rUC_PowerDemand_kW := 0.0;
    rCoolantPumpCmd_Pct := 100.0; // Max cooling on trip
    bCriticalAlarm := TRUE;
    RETURN;
END_IF;

(* Thermal Derating Calculation *)
IF rCoolantTempOut_C > rStackThermalLimit_C THEN
    rThermalDerateFactor := MAX(0.0, 1.0 - ((rCoolantTempOut_C - rStackThermalLimit_C) * 0.1));
    bCriticalAlarm := TRUE;
ELSE
    rThermalDerateFactor := 1.0;
    bCriticalAlarm := FALSE;
END_IF;

(* Transient Load Leveling (Ultra-Capacitor Logic) *)
// Simple low-pass filter on torque request to simulate vehicle inertia decoupling
rFilteredTorqueReq := rFilteredTorqueReq + 0.05 * (rTorqueRequest_Nm - rFilteredTorqueReq);

// Calculate total requested traction power (P = T * w)
rTractionPowerReq_kW := (rTorqueRequest_Nm * c_MotorSpeed_RPM * 0.10472) / 1000.0;

(* State Machine *)
CASE iOpState OF
    0: (* OFF / STANDBY *)
        bPowertrainReady := FALSE;
        rFC_PowerDemand_kW := 0.0;
        rUC_PowerDemand_kW := 0.0;
        rCompressorCmd_RPM := 1000.0; // Idle speed
        IF bSystemEnable THEN
            iOpState := 10;
        END_IF;

    10: (* INITIALIZATION & PURGE *)
        // Run compressor to purge stack
        rCompressorCmd_RPM := 15000.0; 
        rCoolantPumpCmd_Pct := 20.0;
        
        tInitDelay(IN := TRUE, PT := T#10S);
        IF tInitDelay.Q THEN
            tInitDelay(IN := FALSE);
            iOpState := 20;
        END_IF;

    20: (* PRECHARGE & VOLTAGE STABILIZATION *)
        // Wait for Stack voltage to build
        IF rFC_StackVoltage_V > 600.0 THEN
            iOpState := 30;
        END_IF;

    30: (* NORMAL RUN *)
        bPowertrainReady := TRUE;
        
        // Split power demand between FC (Base load) and UC (Transient)
        // Fuel cell provides the filtered (slow moving) power
        rFC_PowerDemand_kW := MIN((rFilteredTorqueReq * c_MotorSpeed_RPM * 0.10472) / 1000.0, rMaxStackPower_kW * rThermalDerateFactor);
        
        // UC provides the transient delta, limited by its SoC
        IF rUC_StateOfCharge_Pct > 20.0 THEN
            rUC_PowerDemand_kW := rTractionPowerReq_kW - rFC_PowerDemand_kW;
        ELSE
            // Force charge if too low
            rUC_PowerDemand_kW := -200.0; 
            rFC_PowerDemand_kW := rFC_PowerDemand_kW + 200.0; // FC must supply traction + charging
        END_IF;
        
        // Compressor map scheduling (Surge protection proxy)
        rCompressorCmd_RPM := MAX(15000.0, rFC_PowerDemand_kW * 25.0 * rSurgeMargin);
        
        // Two-phase boiling suppression (Aggressive cooling curve)
        rCoolantPumpCmd_Pct := MIN(100.0, 20.0 + (rFC_PowerDemand_kW / 20.0) + (MAX(0.0, rCoolantTempOut_C - 70.0) * 5.0));

        // Disable handling
        IF NOT bSystemEnable THEN
            iOpState := 0;
        END_IF;

    99: (* FAULT HANDLING *)
        // Wait for reset condition
        IF bEmergencyStop AND NOT bSystemEnable THEN
            iOpState := 0;
            bCriticalAlarm := FALSE;
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

filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
