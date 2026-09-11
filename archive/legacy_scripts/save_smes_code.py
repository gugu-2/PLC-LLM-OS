import json, uuid, os

os.makedirs('data/swarm_raw', exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Advanced Superconducting Magnetic Energy Storage (SMES)**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Niobium-titanium coil 4.2K helium bath thermal stabilization, mega-ampere bidirectional DC-DC chopper modulation, and grid-tie sub-cycle fault ride-through injection). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_SMES_EnergyStorage\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Advanced Superconducting Magnetic Energy Storage (SMES)

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_SMES_CoilController
TITLE = 'Advanced Superconducting Magnetic Energy Storage Controller'
(*
    Author: Lumina AI Cloud Swarm (40-year veteran)
    Description: 
    High-fidelity control for Niobium-titanium coil at 4.2K helium bath.
    Handles thermal stabilization, mega-ampere bidirectional DC-DC chopper 
    modulation, and grid-tie sub-cycle fault ride-through injection.
*)

VAR_INPUT
    bEnableSystem       : BOOL;     (* System master enable signal *)
    bEmergencyStop      : BOOL;     (* Safety relay OK signal (True = Healthy) *)
    rHeBathTemp         : REAL;     (* Helium bath temperature in Kelvin *)
    rCoilCurrent        : REAL;     (* Current flowing through the SMES coil in kA *)
    rGridVoltage        : REAL;     (* Grid voltage measurement in kV *)
    rPowerDemand        : REAL;     (* Requested power injection/absorption in MW *)
    bGridFaultDetect    : BOOL;     (* Sub-cycle grid fault detection flag *)
END_VAR

VAR_OUTPUT
    bSystemReady        : BOOL;     (* SMES is charged, thermally stable, and ready *)
    rChopperDutyCycle   : REAL;     (* Bidirectional DC-DC chopper duty cycle (0.0 to 1.0) *)
    bQuenchAlarm        : BOOL;     (* Superconductivity loss (Quench) imminent alarm *)
    bCryoCoolerRun      : BOOL;     (* Cryocooler compressor activation command *)
    iStateStatus        : INT;      (* Current internal state machine status code *)
    rPowerInjected      : REAL;     (* Actual power being injected to the grid in MW *)
END_VAR

VAR
    iState              : INT := 0; (* Internal state machine variable *)
    rMaxTempLimit       : REAL := 4.8; (* Quench temperature threshold in K *)
    rMinTempLimit       : REAL := 4.2; (* Nominal operating temperature in K *)
    tFaultTimer         : TON;      (* Timer for fault ride-through duration *)
    tCoolingTimer       : TON;      (* Timer for cryocooler minimum run time *)
    rEnergyStored       : REAL;     (* Calculated stored energy in MJ *)
    rTargetCurrent      : REAL;     (* Target coil current based on demand *)
    rErrorCurrent       : REAL;     (* PI controller error *)
    rKp                 : REAL := 0.05; (* PI proportional gain *)
    rKi                 : REAL := 0.01; (* PI integral gain *)
    rIntegral           : REAL := 0.0;  (* PI integral sum *)
END_VAR

(* === MAIN LOGIC === *)

(* Safety and Interlocks *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bQuenchAlarm := TRUE;
    rChopperDutyCycle := 0.0;
    bCryoCoolerRun := TRUE; (* Max cooling during E-Stop *)
    iState := 99; (* Fault state *)
    iStateStatus := iState;
    RETURN;
END_IF;

(* Thermal Management & Quench Protection *)
IF rHeBathTemp > rMaxTempLimit THEN
    bQuenchAlarm := TRUE;
    bSystemReady := FALSE;
    (* Force rapid discharge to dump resistor if temperature critical *)
    rChopperDutyCycle := -1.0; 
    iState := 98; (* Quench mitigation state *)
ELSE
    bQuenchAlarm := FALSE;
END_IF;

(* Cryocooler Hysteresis Control *)
IF rHeBathTemp > (rMinTempLimit + 0.2) THEN
    bCryoCoolerRun := TRUE;
ELSIF rHeBathTemp <= rMinTempLimit THEN
    bCryoCoolerRun := FALSE;
END_IF;

(* Main State Machine *)
CASE iState OF
    0: (* IDLE & INITIALIZATION *)
        bSystemReady := FALSE;
        rChopperDutyCycle := 0.0;
        rPowerInjected := 0.0;
        IF bEnableSystem AND NOT bQuenchAlarm THEN
            iState := 10;
        END_IF;

    10: (* CHARGING & STABILIZATION *)
        (* Simple ramp up of coil current to baseline standby value *)
        rTargetCurrent := 50.0; (* 50 kA standby current *)
        rErrorCurrent := rTargetCurrent - rCoilCurrent;
        rIntegral := rIntegral + (rErrorCurrent * 0.01);
        rChopperDutyCycle := (rKp * rErrorCurrent) + (rKi * rIntegral);
        
        (* Clamp duty cycle *)
        IF rChopperDutyCycle > 0.8 THEN rChopperDutyCycle := 0.8; END_IF;
        IF rChopperDutyCycle < 0.0 THEN rChopperDutyCycle := 0.0; END_IF;

        IF (rCoilCurrent >= (rTargetCurrent * 0.95)) AND (rHeBathTemp <= rMaxTempLimit) THEN
            iState := 20;
        END_IF;

    20: (* STANDBY / READY *)
        bSystemReady := TRUE;
        rChopperDutyCycle := 0.0; (* Maintain current, minimal chopper switching *)
        rPowerInjected := 0.0;
        
        IF bGridFaultDetect THEN
            iState := 30;
        ELSIF rPowerDemand <> 0.0 THEN
            iState := 40;
        END_IF;
        
        IF NOT bEnableSystem THEN
            iState := 50; (* Ramp down *)
        END_IF;

    30: (* GRID FAULT RIDE-THROUGH (SUB-CYCLE INJECTION) *)
        bSystemReady := FALSE;
        tFaultTimer(IN := TRUE, PT := T#200MS); (* Max ride-through duration *)
        
        (* Inject max power to support grid voltage dip *)
        rChopperDutyCycle := 1.0; 
        rPowerInjected := rCoilCurrent * rGridVoltage * 0.9; (* Approximation *)
        
        IF tFaultTimer.Q OR NOT bGridFaultDetect THEN
            tFaultTimer(IN := FALSE);
            iState := 20; (* Return to standby after fault clears or timer expires *)
        END_IF;

    40: (* ACTIVE MODULATION (POWER DEMAND) *)
        (* Bidirectional power flow based on demand *)
        IF rPowerDemand > 0.0 THEN
            (* Discharging to grid *)
            rChopperDutyCycle := 0.5 + (rPowerDemand * 0.01);
        ELSE
            (* Charging from grid *)
            rChopperDutyCycle := -0.5 + (rPowerDemand * 0.01);
        END_IF;
        
        (* Clamp limits *)
        IF rChopperDutyCycle > 1.0 THEN rChopperDutyCycle := 1.0; END_IF;
        IF rChopperDutyCycle < -1.0 THEN rChopperDutyCycle := -1.0; END_IF;
        
        rPowerInjected := rPowerDemand;
        
        IF rPowerDemand = 0.0 THEN
            iState := 20;
        END_IF;

    50: (* RAMP DOWN / DISCHARGE *)
        bSystemReady := FALSE;
        rChopperDutyCycle := -0.5; (* Regenerative braking into grid or dump *)
        IF rCoilCurrent <= 0.1 THEN
            rChopperDutyCycle := 0.0;
            iState := 0;
        END_IF;

    98: (* QUENCH MITIGATION *)
        bSystemReady := FALSE;
        rChopperDutyCycle := -1.0; (* Max discharge *)
        (* Wait for operator reset *)
        
    99: (* EMERGENCY STOP *)
        (* Wait for E-Stop clear *)
        IF bEmergencyStop THEN
            iState := 0;
        END_IF;

END_CASE;

iStateStatus := iState;

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
