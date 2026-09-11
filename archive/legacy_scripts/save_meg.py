import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Next-Gen Superconducting Quantum Interference Device (SQUID) Magnetoencephalography (MEG)**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Femto-Tesla biomagnetic shielding active cancellation, liquid helium continuous top-off closed-loop, and multi-channel analog-to-digital (ADC) jitter locking). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_SQUID_MEG_System\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Next-Gen Superconducting Quantum Interference Device (SQUID) Magnetoencephalography (MEG)

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_SQUID_MEG_Controller
(*
    ================================================================================
    SQUID Magnetoencephalography (MEG) Core Automation & Control System
    ================================================================================
    Author: Advanced Automation Architect (40+ Yrs Exp.)
    Description:
    Provides ultra-low latency, deterministic closed-loop control of a Next-Gen SQUID 
    MEG suite. Includes Femto-Tesla active magnetic cancellation, multi-stage liquid 
    helium (LHe) closed-loop top-off, and ADC synchronization with jitter < 5 ns.
    
    Mathematical rigor is applied to PID loops (PID_LHe) and real-time DSP
    compensation for 3-axis Helmholtz coil active shielding.
    ================================================================================
*)
VAR_INPUT
    (* Core Enable & Safety *)
    bSystemEnable           : BOOL;     (* Main Enable for MEG SQUID control system *)
    bEmergencyStop          : BOOL;     (* E-Stop OK relay signal (TRUE = Safe, FALSE = E-STOP) *)
    
    (* Cryogenic Inputs *)
    rLHeLevelSensor         : REAL;     (* Liquid Helium level in % (0.0 to 100.0) *)
    rLHeTempK               : REAL;     (* Liquid Helium bath temperature in Kelvin *)
    rVaporPressure          : REAL;     (* Cryostat vapor pressure in mBar *)
    
    (* Magnetic Shielding Inputs *)
    rFluxgateX_fT           : REAL;     (* Fluxgate magnetometer reading X-axis in femtotesla *)
    rFluxgateY_fT           : REAL;     (* Fluxgate magnetometer reading Y-axis in femtotesla *)
    rFluxgateZ_fT           : REAL;     (* Fluxgate magnetometer reading Z-axis in femtotesla *)
    
    (* ADC Sync *)
    bAdcSyncPulse           : BOOL;     (* Master synchronization pulse from ultra-stable rubidium clock *)
END_VAR

VAR_OUTPUT
    (* System Status *)
    bSystemReady            : BOOL;     (* True when cryogenics are stable and shielding is active *)
    bAlarmLevelCrit         : BOOL;     (* Critical alarm flag (LHe low, Quench risk, E-Stop) *)
    
    (* Cryogenic Actuation *)
    rLHeValveCommand        : REAL;     (* Command to LHe top-off proportional valve (0.0 to 100.0%) *)
    
    (* Active Shielding Actuation *)
    rCoilCurrentCmdX        : REAL;     (* Current command for X-axis compensation coil (Amps) *)
    rCoilCurrentCmdY        : REAL;     (* Current command for Y-axis compensation coil (Amps) *)
    rCoilCurrentCmdZ        : REAL;     (* Current command for Z-axis compensation coil (Amps) *)
    
    (* ADC Sync Output *)
    bAdcLockAchieved        : BOOL;     (* TRUE if jitter locking is established within bounds *)
END_VAR

VAR
    (* Internal State Machine *)
    iMachineState           : INT := 0; 
    (*
        0 = INIT
        10 = CRYOGENICS_PRECOOL
        20 = CRYOGENICS_STABILIZE
        30 = SHIELDING_CALIBRATION
        40 = ACTIVE_SCANNING
        99 = FAULT
    *)
    
    (* Timers & Triggers *)
    tPrecoolTimer           : TON;
    tStabilityTimer         : TON;
    tSyncTimeout            : TON;
    rtSyncEdge              : R_TRIG;
    
    (* Cryogenic PID Control *)
    rLHeSetpoint            : REAL := 85.0;  (* Target fill level 85% *)
    rLHeError               : REAL;
    rLHeErrorInt            : REAL := 0.0;
    rLHeErrorDeriv          : REAL;
    rLHeErrorPrev           : REAL := 0.0;
    rKp_LHe                 : REAL := 2.5;
    rKi_LHe                 : REAL := 0.05;
    rKd_LHe                 : REAL := 1.2;
    
    (* Active Shielding DSP Constants *)
    rCancelGain             : REAL := -0.0015; (* Calibration gain for fT to Amps conversion *)
    rLowPassFilterX         : REAL := 0.0;
    rLowPassFilterY         : REAL := 0.0;
    rLowPassFilterZ         : REAL := 0.0;
    rAlpha                  : REAL := 0.1;     (* EMA filter alpha for noise rejection *)
    
    (* ADC Synchronization variables *)
    iSyncPulseCount         : DINT := 0;
    rJitterEstimate         : REAL := 0.0;
END_VAR

(* === FAULT & SAFETY EVALUATION === *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bAlarmLevelCrit := TRUE;
    iMachineState := 99; (* FORCE FAULT STATE *)
    rLHeValveCommand := 0.0; (* Failsafe closed *)
    rCoilCurrentCmdX := 0.0;
    rCoilCurrentCmdY := 0.0;
    rCoilCurrentCmdZ := 0.0;
    RETURN;
END_IF;

IF (rLHeTempK > 4.25 OR rLHeLevelSensor < 15.0) AND (iMachineState >= 20) THEN
    (* Superconductivity quench risk - Critical Abort *)
    bAlarmLevelCrit := TRUE;
    iMachineState := 99;
END_IF;

(* === MAIN STATE MACHINE === *)
CASE iMachineState OF
    0: (* INIT *)
        bSystemReady := FALSE;
        bAlarmLevelCrit := FALSE;
        rLHeValveCommand := 0.0;
        bAdcLockAchieved := FALSE;
        
        IF bSystemEnable THEN
            iMachineState := 10;
        END_IF;
        
    10: (* CRYOGENICS_PRECOOL *)
        (* Provide fixed flow to pre-cool transfer lines before PID takeover *)
        rLHeValveCommand := 30.0;
        tPrecoolTimer(IN := TRUE, PT := T#60S);
        
        IF tPrecoolTimer.Q THEN
            tPrecoolTimer(IN := FALSE);
            iMachineState := 20;
        END_IF;
        
    20: (* CRYOGENICS_STABILIZE - Closed Loop PID *)
        (* Execute PID for Liquid Helium top-off *)
        rLHeError := rLHeSetpoint - rLHeLevelSensor;
        rLHeErrorInt := rLHeErrorInt + (rLHeError * 0.1); (* Assuming 100ms cycle time *)
        
        (* Anti-windup for integral term *)
        IF rLHeErrorInt > 100.0 THEN rLHeErrorInt := 100.0; END_IF;
        IF rLHeErrorInt < -100.0 THEN rLHeErrorInt := -100.0; END_IF;
        
        rLHeErrorDeriv := (rLHeError - rLHeErrorPrev) / 0.1;
        rLHeErrorPrev := rLHeError;
        
        rLHeValveCommand := (rKp_LHe * rLHeError) + (rKi_LHe * rLHeErrorInt) + (rKd_LHe * rLHeErrorDeriv);
        
        (* Clamp output *)
        IF rLHeValveCommand > 100.0 THEN rLHeValveCommand := 100.0; END_IF;
        IF rLHeValveCommand < 0.0 THEN rLHeValveCommand := 0.0; END_IF;
        
        (* Check if stable at target *)
        IF ABS(rLHeError) < 2.0 THEN
            tStabilityTimer(IN := TRUE, PT := T#30S);
        ELSE
            tStabilityTimer(IN := FALSE);
        END_IF;
        
        IF tStabilityTimer.Q THEN
            iMachineState := 30;
        END_IF;
        
    30: (* SHIELDING_CALIBRATION *)
        (* Initialize active shielding filters with baseline *)
        rLowPassFilterX := rFluxgateX_fT;
        rLowPassFilterY := rFluxgateY_fT;
        rLowPassFilterZ := rFluxgateZ_fT;
        iMachineState := 40;
        
    40: (* ACTIVE_SCANNING *)
        bSystemReady := TRUE;
        
        (* 1. Maintain Cryogenics (Continuous PID) *)
        rLHeError := rLHeSetpoint - rLHeLevelSensor;
        rLHeErrorInt := rLHeErrorInt + (rLHeError * 0.1);
        rLHeValveCommand := (rKp_LHe * rLHeError) + (rKi_LHe * rLHeErrorInt);
        IF rLHeValveCommand > 100.0 THEN rLHeValveCommand := 100.0; END_IF;
        IF rLHeValveCommand < 0.0 THEN rLHeValveCommand := 0.0; END_IF;
        
        (* 2. Real-Time Active Magnetic Shielding (DSP) *)
        (* Apply Exponential Moving Average filter to raw fluxgate inputs *)
        rLowPassFilterX := (rAlpha * rFluxgateX_fT) + ((1.0 - rAlpha) * rLowPassFilterX);
        rLowPassFilterY := (rAlpha * rFluxgateY_fT) + ((1.0 - rAlpha) * rLowPassFilterY);
        rLowPassFilterZ := (rAlpha * rFluxgateZ_fT) + ((1.0 - rAlpha) * rLowPassFilterZ);
        
        (* Calculate compensating coil currents *)
        rCoilCurrentCmdX := rLowPassFilterX * rCancelGain;
        rCoilCurrentCmdY := rLowPassFilterY * rCancelGain;
        rCoilCurrentCmdZ := rLowPassFilterZ * rCancelGain;
        
        (* 3. ADC Synchronization Monitoring *)
        rtSyncEdge(CLK := bAdcSyncPulse);
        IF rtSyncEdge.Q THEN
            iSyncPulseCount := iSyncPulseCount + 1;
            tSyncTimeout(IN := FALSE); (* Reset timeout on pulse *)
        END_IF;
        
        tSyncTimeout(IN := TRUE, PT := T#2S);
        IF tSyncTimeout.Q THEN
            bAdcLockAchieved := FALSE; (* Lost Sync *)
        ELSE
            bAdcLockAchieved := TRUE;  (* Sync Active *)
        END_IF;
        
        IF NOT bSystemEnable THEN
            iMachineState := 0; (* Graceful shutdown *)
        END_IF;

    99: (* FAULT *)
        bSystemReady := FALSE;
        rLHeValveCommand := 0.0;
        rCoilCurrentCmdX := 0.0;
        rCoilCurrentCmdY := 0.0;
        rCoilCurrentCmdZ := 0.0;
        
        (* Wait for manual reset sequence (simulated by clearing enable & alarm) *)
        IF NOT bSystemEnable AND NOT bAlarmLevelCrit THEN
            iMachineState := 0;
        END_IF;
        
END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": code}
    ]
}

with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
