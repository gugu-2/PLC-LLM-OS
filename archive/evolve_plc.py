import json

system_prompt = "You are an expert PLC programmer. Evolve the provided logic into a complex, enterprise-grade application."

user_prompt = """Evolve the following basic analog scaling logic block into a complex PID Temperature Control loop with deadband filtering and cascade control for a chemical reactor. Include comprehensive state machines, safety interlocks (e-stops, thermal overloads), hardware abstractions, and flawless comments.

Seed Code:
(* Scale_B translates and scales a byte input to a real output *)
FUNCTION SCALE_B : REAL
VAR_INPUT X, I_LO, I_HI : BYTE; O_LO, O_HI : REAL; END_VAR
IF I_HI = I_LO THEN SCALE_B := O_LO;
ELSE SCALE_B := (O_HI - O_LO) / BYTE_TO_REAL(I_HI - I_LO) * BYTE_TO_REAL(LIMIT(I_LO, X, I_HI)); END_IF
"""

assistant_response = """(*
================================================================================
Function Block: FB_ReactorTempCascadeCtrl
Author: Lumina Elite Synthetic Data Architect
Description: 
Complex cascade PID temperature control loop for a chemical reactor.
Features include:
1. Deadband filtering for analog scaling (hardware abstraction).
2. Cascade Control: Primary (Reactor Temp) sets Secondary (Jacket Temp) setpoint.
3. Advanced State Machine: INIT, HEAT_UP, STEADY_STATE, COOL_DOWN, SAFE_STOP, FAULT.
4. Safety Interlocks: E-Stop, Thermal Overloads, and Coolant Flow monitoring.

Hardware Abstraction Concept:
Raw byte signals from field instruments are filtered through a deadband
and scaled into physical engineering units (Real).
================================================================================
*)

TYPE E_ReactorState :
(
    STATE_INIT := 0,
    STATE_HEAT_UP := 10,
    STATE_STEADY_STATE := 20,
    STATE_COOL_DOWN := 30,
    STATE_SAFE_STOP := 40,
    STATE_FAULT := 99
);
END_TYPE

FUNCTION_BLOCK FB_ReactorTempCascadeCtrl
VAR_INPUT
    // Hardware Abstraction Layer - Raw Inputs
    bRawReactorTemp     : BYTE; // 0-255 mapped to 0.0 - 200.0 C
    bRawJacketTemp      : BYTE; // 0-255 mapped to 0.0 - 150.0 C
    bRawCoolantFlow     : BYTE; // 0-255 mapped to 0.0 - 100.0 L/min

    // Safety Interlocks
    xEmergencyStop      : BOOL; // TRUE = Healthy, FALSE = Tripped
    xThermalOverload    : BOOL; // TRUE = Tripped, FALSE = Healthy

    // Operational Commands
    xCmdStart           : BOOL;
    xCmdStop            : BOOL;
    rPrimarySetpoint    : REAL; // Target Reactor Temperature (C)
    
    // Tuning Parameters
    rDeadband           : REAL := 0.5;
END_VAR

VAR_OUTPUT
    // Hardware Abstraction Layer - Raw Outputs
    rSteamValveCmd      : REAL; // 0.0 - 100.0 %
    rCoolantValveCmd    : REAL; // 0.0 - 100.0 %
    
    // Status
    eCurrentState       : E_ReactorState;
    xAlarmActive        : BOOL;
    sStatusMsg          : STRING(50);
END_VAR

VAR
    // Internal Scaled Values
    rReactorTemp        : REAL;
    rJacketTemp         : REAL;
    rCoolantFlow        : REAL;
    
    // Previous Values for Deadband Filtering
    rPrevReactorTemp    : REAL;
    rPrevJacketTemp     : REAL;

    // PID Controllers (Abstracted standard instances)
    fbPrimaryPID        : FB_StandardPID; // Reactor Temp -> Jacket Temp SP
    fbSecondaryPID      : FB_StandardPID; // Jacket Temp -> Valve Output
    
    rJacketTempSP       : REAL; // Output of primary PID
    rSecondaryOutput    : REAL; // Output of secondary PID (-100% to +100%)

    // Timers
    tonHeatUpTimeout    : TON;
    tonCoolDownDelay    : TON;
    
    // State Tracking
    eNextState          : E_ReactorState;
END_VAR

VAR CONSTANT
    CRIT_TEMP_LIMIT     : REAL := 180.0; // Critical temperature threshold
    MIN_COOLANT_FLOW    : REAL := 10.0;  // Minimum safe flow rate
END_VAR

// ==============================================================================
// 1. HARDWARE ABSTRACTION & DEADBAND FILTERING
// ==============================================================================
// Helper inline scaling logic based on the original SCALE_B concept
rReactorTemp := SCALE_BYTE_TO_REAL(bRawReactorTemp, 0, 255, 0.0, 200.0);
IF ABS(rReactorTemp - rPrevReactorTemp) < rDeadband THEN
    rReactorTemp := rPrevReactorTemp; // Apply deadband
ELSE
    rPrevReactorTemp := rReactorTemp;
END_IF

rJacketTemp := SCALE_BYTE_TO_REAL(bRawJacketTemp, 0, 255, 0.0, 150.0);
IF ABS(rJacketTemp - rPrevJacketTemp) < rDeadband THEN
    rJacketTemp := rPrevJacketTemp;
ELSE
    rPrevJacketTemp := rJacketTemp;
END_IF

rCoolantFlow := SCALE_BYTE_TO_REAL(bRawCoolantFlow, 0, 255, 0.0, 100.0);

// ==============================================================================
// 2. SAFETY INTERLOCKS EVALUATION
// ==============================================================================
IF NOT xEmergencyStop OR xThermalOverload OR (rReactorTemp > CRIT_TEMP_LIMIT) THEN
    eNextState := STATE_FAULT;
    sStatusMsg := 'CRITICAL SAFETY TRIP - E-STOP/OVERLOAD';
END_IF

// ==============================================================================
// 3. MAIN STATE MACHINE
// ==============================================================================
CASE eCurrentState OF

    STATE_INIT:
        rSteamValveCmd   := 0.0;
        rCoolantValveCmd := 100.0; // Fail-safe cooling
        fbPrimaryPID.xReset := TRUE;
        fbSecondaryPID.xReset := TRUE;
        xAlarmActive := FALSE;
        sStatusMsg := 'System Initialized. Awaiting Start.';

        IF xCmdStart AND NOT (eNextState = STATE_FAULT) THEN
            eNextState := STATE_HEAT_UP;
        END_IF

    STATE_HEAT_UP:
        fbPrimaryPID.xReset := FALSE;
        fbSecondaryPID.xReset := FALSE;
        sStatusMsg := 'Heating Up Reactor...';

        // Check if we reached steady state condition
        IF ABS(rReactorTemp - rPrimarySetpoint) <= 2.0 THEN
            eNextState := STATE_STEADY_STATE;
        END_IF
        
        IF xCmdStop THEN eNextState := STATE_COOL_DOWN; END_IF

    STATE_STEADY_STATE:
        sStatusMsg := 'Reactor in Steady State';
        
        IF xCmdStop THEN eNextState := STATE_COOL_DOWN; END_IF
        
        // Monitoring for excessive deviation
        IF ABS(rReactorTemp - rPrimarySetpoint) > 10.0 THEN
            xAlarmActive := TRUE;
            sStatusMsg := 'Warning: Temp Deviation High';
        ELSE
            xAlarmActive := FALSE;
        END_IF

    STATE_COOL_DOWN:
        sStatusMsg := 'Cooling Down Sequence';
        // Override cascade, force cooling
        rJacketTempSP := 20.0; // Safe jacket temperature
        
        // Delay for full cooling before safe stop
        tonCoolDownDelay(IN:=TRUE, PT:=T#5M);
        IF tonCoolDownDelay.Q OR rReactorTemp < 30.0 THEN
            eNextState := STATE_SAFE_STOP;
            tonCoolDownDelay(IN:=FALSE);
        END_IF

    STATE_SAFE_STOP:
        rSteamValveCmd := 0.0;
        rCoolantValveCmd := 0.0;
        fbPrimaryPID.xReset := TRUE;
        fbSecondaryPID.xReset := TRUE;
        sStatusMsg := 'Safe Stop Achieved';
        
        IF NOT xCmdStart THEN
            eNextState := STATE_INIT;
        END_IF

    STATE_FAULT:
        xAlarmActive := TRUE;
        // Fail-safe logic
        rSteamValveCmd := 0.0;
        rCoolantValveCmd := 100.0; // Max cooling immediately
        fbPrimaryPID.xReset := TRUE;
        fbSecondaryPID.xReset := TRUE;
        
        IF xEmergencyStop AND NOT xThermalOverload AND (rReactorTemp < CRIT_TEMP_LIMIT) AND xCmdStop THEN
            eNextState := STATE_INIT; // Reset fault via stop command when safe
            sStatusMsg := 'Fault Cleared. Awaiting Reset.';
        END_IF

END_CASE

// Update state
eCurrentState := eNextState;

// ==============================================================================
// 4. CASCADE PID EXECUTION
// ==============================================================================
// Only active in Heat Up or Steady State
IF (eCurrentState = STATE_HEAT_UP) OR (eCurrentState = STATE_STEADY_STATE) THEN
    
    // Primary Loop: Reactor Temp (PV) -> Jacket Temp Setpoint (CV)
    fbPrimaryPID(
        rPV := rReactorTemp,
        rSP := rPrimarySetpoint,
        rKp := 2.5,
        rKi := 0.1,
        rKd := 0.5,
        rMinOut := 10.0,
        rMaxOut := 140.0,
        rCV => rJacketTempSP
    );

END_IF

// Secondary Loop always active unless reset (follows forced rJacketTempSP in COOL_DOWN)
fbSecondaryPID(
    rPV := rJacketTemp,
    rSP := rJacketTempSP,
    rKp := 5.0,
    rKi := 0.2,
    rKd := 0.0,
    rMinOut := -100.0, // -100% means full cooling
    rMaxOut := 100.0,  // +100% means full heating
    rCV => rSecondaryOutput
);

// Split-range output logic based on secondary loop
IF rSecondaryOutput > 0.0 THEN
    rSteamValveCmd   := rSecondaryOutput;
    rCoolantValveCmd := 0.0;
ELSE
    rSteamValveCmd   := 0.0;
    rCoolantValveCmd := ABS(rSecondaryOutput);
END_IF

// Flow interlock for heating
IF rCoolantFlow < MIN_COOLANT_FLOW AND rCoolantValveCmd > 0.0 THEN
    sStatusMsg := 'Warning: Low Coolant Flow';
    xAlarmActive := TRUE;
END_IF

END_FUNCTION_BLOCK

// Internal Helper Function for Scaling
FUNCTION SCALE_BYTE_TO_REAL : REAL
VAR_INPUT
    X, I_LO, I_HI : BYTE;
    O_LO, O_HI : REAL;
END_VAR
IF I_HI = I_LO THEN 
    SCALE_BYTE_TO_REAL := O_LO;
ELSE 
    SCALE_BYTE_TO_REAL := (O_HI - O_LO) / BYTE_TO_REAL(I_HI - I_LO) * BYTE_TO_REAL(LIMIT(I_LO, X, I_HI)); 
END_IF
END_FUNCTION
"""

msg_obj = {
    "messages": [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
        {"role": "assistant", "content": assistant_response}
    ]
}

with open(r"c:\Users\majip\Downloads\LLM REASEARCH\data\evol_instruct_dataset.jsonl", "a") as f:
    f.write(json.dumps(msg_obj) + "\n")

print("Done appending to JSONL")
