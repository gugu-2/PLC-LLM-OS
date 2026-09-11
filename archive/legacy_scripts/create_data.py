import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Advanced Semiconductor Extreme Ultraviolet (EUV) Source Vacuum Vessel**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., High-power CO2 laser pre-pulse synchronization, multi-stage turbo-molecular backing pump differential pressure cascading, and tin debris mitigation rotating gas lock). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_EUV_VacuumVessel\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Advanced Semiconductor Extreme Ultraviolet (EUV) Source Vacuum Vessel

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_EUV_Source_VacuumVessel_Controller
VAR_INPUT
    (* Required: at least 4-8 physical inputs with types and comments *)
    bEnable                 : BOOL;     (* System master enable signal from fab host *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal (active HIGH = Safe) *)
    rVesselPressure_mBar    : REAL;     (* Main vacuum vessel pressure from Baratron gauge in mBar *)
    rTurboPumpSpeed_RPM     : REAL;     (* Current turbo molecular pump speed in RPM *)
    rBackingPumpPres_mBar   : REAL;     (* Backing pump differential pressure in mBar *)
    rTinCatcherTemp_C       : REAL;     (* Tin (Sn) debris catcher temperature in deg C *)
    bLaserSyncTrigger       : BOOL;     (* Pre-pulse and main pulse synchronization trigger from CO2 laser *)
END_VAR
VAR_OUTPUT
    (* Required: at least 3-6 outputs with types and comments *)
    bSystemReady            : BOOL;     (* System ready status for EUV generation emission *)
    rTurboPumpSpeedRef      : REAL;     (* Control signal setpoint to main turbo actuator drive *)
    rGasLockFlowCtrl_SCCM   : REAL;     (* Mass flow controller output for H2 gas lock mitigation *)
    bLaserInterlockOk       : BOOL;     (* Laser firing interlock permit (hardware safety gate) *)
    bAlarm                  : BOOL;     (* Fault alarm output to centralized monitoring *)
    iDiagnosticsCode        : INT;      (* Detailed integer code for predictive maintenance *)
END_VAR
VAR
    (* Internal state variables *)
    iState                  : INT := 0; (* Main finite state machine step *)
    iSubState               : INT := 0; (* Background routine sub-state *)
    
    (* Timers for sequence progression and stabilization *)
    tTurboPumpTimer         : TON;      (* Turbo pump ramp sequence timeout watchdog *)
    tVacuumSettleTimer      : TON;      (* High vacuum pressure stabilization dwell timer *)
    tDebrisPurgeTimer       : TOF;      (* Off-delay for tin debris H2 purge mechanism *)
    
    (* Signal processing and filtering variables *)
    rFilteredPressure       : REAL := 1000.0; (* EWMA filtered vessel pressure (mBar) *)
    rAlphaPressure          : REAL := 0.05;   (* EWMA low-pass filter coefficient for pressure gauge noise *)
    
    (* Operational setpoints *)
    rHighVacuumTarget       : REAL := 0.005;  (* Target mBar for plasma ignition *)
    rH2GasLockBaseFlow      : REAL := 15.0;   (* SCCM H2 base flow for debris shielding *)
    rH2GasLockPulseFlow     : REAL := 85.0;   (* SCCM H2 transient flow during laser firing *)
END_VAR

(* === MAIN LOGIC === *)
(* 1. Fast-Response Multi-layered Safety Interlock Evaluation *)
IF NOT bEmergencyStop THEN
    bSystemReady            := FALSE;
    bLaserInterlockOk       := FALSE;
    rTurboPumpSpeedRef      := 0.0;       (* Coast down the turbo safely on loss of E-Stop *)
    rGasLockFlowCtrl_SCCM   := 0.0;       (* Isolate H2 mass flow controller *)
    bAlarm                  := TRUE;
    iDiagnosticsCode        := 999;       (* Code 999: Critical Emergency Stop Activated *)
    iState                  := 0;
    RETURN;
END_IF;

(* 2. Mathematical Filtering: EWMA (Exponentially Weighted Moving Average) for Sensor Noise Mitigation *)
(* Industrial vacuum gauges (e.g. Pirani/Baratron) exhibit high frequency noise near their operational floor *)
rFilteredPressure := (rAlphaPressure * rVesselPressure_mBar) + ((1.0 - rAlphaPressure) * rFilteredPressure);

(* 3. Thermal Protection: Continuous Tin (Sn) Debris Catcher Monitoring *)
(* Extreme heat from the plasma droplet can permanently damage the rotating lock if uncooled *)
IF rTinCatcherTemp_C > 450.0 THEN
    bAlarm := TRUE;
    iDiagnosticsCode := 101; (* Code 101: Tin Catcher Over-temperature Limit Reached *)
    iState := 99; (* Enter FAULT SAFE STATE immediately *)
END_IF;

(* 4. Main Control Finite State Machine *)
CASE iState OF
    0: (* IDLE: Waiting for fab host integration enable *)
        bSystemReady := FALSE;
        bLaserInterlockOk := FALSE;
        rTurboPumpSpeedRef := 0.0;
        
        IF bEnable AND (iDiagnosticsCode = 0 OR iDiagnosticsCode = 999) THEN
            iState := 10;
            iDiagnosticsCode := 0;
            bAlarm := FALSE;
        END_IF;

    10: (* ROUGHING PUMP DOWN: Multi-stage cascade verification *)
        (* Monitor backing pump differential pressure to prevent turbo stalling *)
        IF rBackingPumpPres_mBar < 5.0 THEN
            (* Roughing stage complete, transition to High Vacuum ramp *)
            iState := 20; 
        ELSIF rBackingPumpPres_mBar > 50.0 AND bEnable THEN
            (* Backing pump stalled, differential cascade failure or severe leak *)
            iState := 99;
            iDiagnosticsCode := 201; (* Code 201: Backing Pump Cascade Failure *)
        END_IF;

    20: (* HIGH VACUUM RAMP: Engaging Magnetic Bearing Turbo *)
        (* Ramp up turbo molecular pump to nominal resonance-free speed of 35,000 RPM *)
        rTurboPumpSpeedRef := 35000.0;
        
        (* Watchdog timer for turbo spool-up - prevents thermal runaway of motor windings *)
        tTurboPumpTimer(IN := TRUE, PT := T#300S);
        
        IF tTurboPumpTimer.Q THEN
            (* Timeout before reaching speed *)
            tTurboPumpTimer(IN := FALSE);
            iState := 99;
            iDiagnosticsCode := 202; (* Code 202: Turbo Spool-Up Watchdog Timeout *)
        ELSIF rTurboPumpSpeed_RPM > 34000.0 THEN
            (* Target speed achieved successfully *)
            tTurboPumpTimer(IN := FALSE);
            iState := 30;
        END_IF;

    30: (* STABILIZE PRESSURE & ENGAGE ROTATING GAS LOCK *)
        (* Initiate H2 gas lock dynamic pressure regulation to mitigate tin debris back-flow towards collector mirror *)
        rGasLockFlowCtrl_SCCM := rH2GasLockBaseFlow + ((rHighVacuumTarget - rFilteredPressure) * 500.0);
        
        (* Hardware constraints: Clamp mass flow controller output to physical limits *)
        IF rGasLockFlowCtrl_SCCM > 100.0 THEN
            rGasLockFlowCtrl_SCCM := 100.0;
        ELSIF rGasLockFlowCtrl_SCCM < 5.0 THEN
            rGasLockFlowCtrl_SCCM := 5.0;
        END_IF;

        (* Dwell timer to ensure plasma ignition conditions are completely homogeneous *)
        tVacuumSettleTimer(IN := TRUE, PT := T#60S);
        IF tVacuumSettleTimer.Q AND (rFilteredPressure <= rHighVacuumTarget) THEN
            tVacuumSettleTimer(IN := FALSE);
            iState := 40;
        END_IF;

    40: (* EMISSION READY: CO2 Laser Pre-pulse Synchronization Valid *)
        bSystemReady := TRUE;
        bLaserInterlockOk := TRUE;
        
        (* Transient handling: Dynamic H2 flow control based on laser sync pulse *)
        (* A microsecond pre-pulse vaporizes the Sn droplet, requiring immediate debris suppression *)
        tDebrisPurgeTimer(IN := bLaserSyncTrigger, PT := T#2S); 
        
        IF tDebrisPurgeTimer.Q THEN
            (* Momentary surge of H2 to clear plasma shockwave and metallic particulates *)
            rGasLockFlowCtrl_SCCM := rH2GasLockPulseFlow;
        ELSE
            (* Return to steady-state background mitigation flow *)
            rGasLockFlowCtrl_SCCM := rH2GasLockBaseFlow;
        END_IF;

        (* Supervisory loop checks *)
        IF NOT bEnable THEN
            iState := 0;
        ELSIF rFilteredPressure > (rHighVacuumTarget * 1.75) THEN
            (* Critical loss of vacuum integrity during plasma emission - abort instantly *)
            iState := 99;
            iDiagnosticsCode := 301; (* Code 301: Transient Vacuum Collapse *)
        END_IF;

    99: (* FAULT HANDLING & GRACEFUL DEGRADATION *)
        bSystemReady := FALSE;
        bLaserInterlockOk := FALSE;
        bAlarm := TRUE;
        rGasLockFlowCtrl_SCCM := 0.0;
        
        (* Coast down magnetic bearings gracefully to prevent catastrophic blade collision *)
        rTurboPumpSpeedRef := 0.0;
        
        tTurboPumpTimer(IN := FALSE);
        tVacuumSettleTimer(IN := FALSE);
        
        (* Operator must explicitly toggle enable signal to clear faults after safety inspection *)
        IF NOT bEnable THEN
            iState := 0;
            (* Note: diagnostics code is preserved until transition to State 10 for root-cause analysis *)
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
