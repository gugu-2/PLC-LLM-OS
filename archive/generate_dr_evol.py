import json

prompt = "Evolve a basic temperature block into a Quantum Computing Cryostat Dilution Refrigerator controller. Implement ultra-low temperature (milli-Kelvin) He3/He4 isotope mixture regulation, turbo-molecular vacuum pump sequencing, and superconducting magnet quench detection."
assistant_response = """(*
    VERSION 2.0
    AUTHOR: Synthetic Data Architect
    
    DESCRIPTION:
    Ultra-low temperature (milli-Kelvin) He3/He4 isotope mixture regulation, 
    turbo-molecular vacuum pump sequencing, and superconducting magnet quench detection.
*)
FUNCTION_BLOCK CRYOSTAT_DR_CTRL
VAR_INPUT
    Enable : BOOL; // Main system enable
    E_Stop : BOOL; // Emergency stop, active low
    
    // Hardware Sensors
    T_Still : REAL; // Temperature of Still (K)
    T_MC : REAL;    // Temperature of Mixing Chamber (K)
    T_4K_Stage : REAL; // Temperature of 4K stage (K)
    P_Still : REAL; // Pressure at Still (mbar)
    P_Cond : REAL;  // Condensing pressure (mbar)
    P_OVC : REAL;   // Outer Vacuum Chamber pressure (mbar)
    
    // Magnet Sensors
    Mag_V_Lead : REAL; // Voltage across magnet leads (V)
    Mag_Current : REAL; // Current through magnet (A)
    
    // Pump Feedback
    Turbo_Speed_Hz : REAL; // Turbo pump speed in Hz
    Turbo_Fault : BOOL;    // Turbo pump internal fault
    Forepump_Fault : BOOL; // Forepump overload/fault
END_VAR

VAR_OUTPUT
    // Actuators & Pumps
    Cmd_Turbo_Run : BOOL; 
    Cmd_Forepump_Run : BOOL;
    Cmd_He3_He4_Valve : REAL; // 0-100% Flow control valve
    Cmd_Still_Heater : REAL; // 0-100% Still heater power
    
    // Magnet Protection
    Cmd_Dump_Resistor : BOOL; // Engage dump resistor
    Cmd_Mag_PSU_Trip : BOOL; // Trip Magnet PSU
    
    // Status
    Sys_State : INT; // System State Machine
    Fault_Code : DWORD; // Bitfield of faults
    MC_Temp_mK : REAL; // Mixing chamber temp in mK
END_VAR

VAR
    // State Machine Constants
    STATE_IDLE : INT := 0;
    STATE_PUMPDOWN : INT := 10;
    STATE_COOL_4K : INT := 20;
    STATE_CONDENSING : INT := 30;
    STATE_CIRCULATING : INT := 40;
    STATE_QUENCH : INT := 99;
    STATE_FAULT : INT := 100;
    
    // Timers
    TMR_Pumpdown : TON;
    TMR_Condensing : TON;
    
    // Quench Detection
    Prev_Mag_V : REAL;
    Quench_Threshold_V_s : REAL := 5.0; // V/s
    dV_dt : REAL;
    
    // PID for He3/He4
    PID_Mix_Err : REAL;
    PID_Mix_Integral : REAL;
    
    // Internal Flags
    Sys_Fault : BOOL;
END_VAR

// ==============================================================================
// 1. HARDWARE ABSTRACTION & SCALING
// ==============================================================================
MC_Temp_mK := T_MC * 1000.0; // Convert to mK for precise reporting

// ==============================================================================
// 2. SAFETY INTERLOCKS & FAULT EVALUATION
// ==============================================================================
Fault_Code := 0;
Sys_Fault := FALSE;

// Check E-Stop
IF NOT E_Stop THEN
    Fault_Code.0 := TRUE;
    Sys_Fault := TRUE;
END_IF;

// Check Pump Faults
IF Turbo_Fault THEN
    Fault_Code.1 := TRUE;
    Sys_Fault := TRUE;
END_IF;

IF Forepump_Fault THEN
    Fault_Code.2 := TRUE;
    Sys_Fault := TRUE;
END_IF;

// Vacuum interlock (OVC must be < 1e-4 mbar for operation)
IF P_OVC > 1.0E-4 AND Sys_State > STATE_PUMPDOWN THEN
    Fault_Code.3 := TRUE;
    Sys_Fault := TRUE;
END_IF;

// ==============================================================================
// 3. SUPERCONDUCTING MAGNET QUENCH DETECTION
// ==============================================================================
// Calculate derivative of voltage (assuming fixed 10ms cycle time for simplicity)
dV_dt := (Mag_V_Lead - Prev_Mag_V) * 100.0; 
Prev_Mag_V := Mag_V_Lead;

IF ABS(dV_dt) > Quench_Threshold_V_s AND Mag_Current > 10.0 THEN
    // Quench detected! Rapid energy conversion to heat.
    Fault_Code.4 := TRUE;
    Sys_State := STATE_QUENCH;
END_IF;

// ==============================================================================
// 4. MAIN STATE MACHINE
// ==============================================================================
CASE Sys_State OF
    STATE_IDLE:
        Cmd_Turbo_Run := FALSE;
        Cmd_Forepump_Run := FALSE;
        Cmd_He3_He4_Valve := 0.0;
        Cmd_Still_Heater := 0.0;
        
        IF Enable AND NOT Sys_Fault THEN
            Sys_State := STATE_PUMPDOWN;
        END_IF;
        
    STATE_PUMPDOWN:
        // Sequence: Forepump first, then Turbo
        Cmd_Forepump_Run := TRUE;
        TMR_Pumpdown(IN:=Cmd_Forepump_Run, PT:=T#5M);
        
        IF TMR_Pumpdown.Q THEN
            Cmd_Turbo_Run := TRUE;
        END_IF;
        
        // Wait for OVC pressure to drop and turbo to reach operational speed
        IF P_OVC < 1.0E-4 AND Turbo_Speed_Hz > 800.0 THEN
            Sys_State := STATE_COOL_4K;
        END_IF;
        
    STATE_COOL_4K:
        // Wait for Pre-cooling stage to reach liquid helium temperatures (~4K)
        IF T_4K_Stage < 4.5 THEN
            Sys_State := STATE_CONDENSING;
        END_IF;
        
    STATE_CONDENSING:
        // Inject He3/He4 mixture to condense into the circulation loop
        Cmd_He3_He4_Valve := 100.0; // Full open to condense
        
        IF P_Cond < 50.0 AND T_Still < 1.2 THEN
            Sys_State := STATE_CIRCULATING;
        END_IF;
        
    STATE_CIRCULATING:
        // Closed-loop PID regulation for milli-Kelvin operation
        PID_Mix_Err := 15.0 - MC_Temp_mK; // Target 15mK for qubit coherence
        PID_Mix_Integral := PID_Mix_Integral + (PID_Mix_Err * 0.01);
        
        // Anti-windup
        IF PID_Mix_Integral > 100.0 THEN PID_Mix_Integral := 100.0; END_IF;
        IF PID_Mix_Integral < 0.0 THEN PID_Mix_Integral := 0.0; END_IF;
        
        Cmd_He3_He4_Valve := (PID_Mix_Err * 0.5) + PID_Mix_Integral;
        IF Cmd_He3_He4_Valve > 100.0 THEN Cmd_He3_He4_Valve := 100.0; END_IF;
        IF Cmd_He3_He4_Valve < 0.0 THEN Cmd_He3_He4_Valve := 0.0; END_IF;
        
        // Still heater logic to maintain osmotic pressure gradient
        Cmd_Still_Heater := 10.0; // Base power for circulation (mW)
        
        IF NOT Enable THEN
            Sys_State := STATE_IDLE;
        END_IF;
        
    STATE_QUENCH:
        // EMERGENCY MAGNET DISCHARGE - Triggered by massive resistance increase
        Cmd_Dump_Resistor := TRUE;
        Cmd_Mag_PSU_Trip := TRUE;
        
        // Protect delicate cooling system components from massive heat load explosion
        Cmd_He3_He4_Valve := 0.0;
        Cmd_Still_Heater := 0.0;
        
        IF NOT Enable AND Mag_Current < 1.0 THEN
            Sys_State := STATE_FAULT; // Must be manually reset
        END_IF;
        
    STATE_FAULT:
        // Safe state
        Cmd_Turbo_Run := FALSE;
        Cmd_Forepump_Run := FALSE;
        Cmd_He3_He4_Valve := 0.0;
        Cmd_Still_Heater := 0.0;
        
        IF NOT Sys_Fault AND NOT Enable THEN
            Sys_State := STATE_IDLE;
        END_IF;
        
    ELSE
        Sys_State := STATE_FAULT;
END_CASE;

// ==============================================================================
// 5. GLOBAL FAULT OVERRIDE
// ==============================================================================
IF Sys_Fault AND Sys_State <> STATE_QUENCH THEN
    Sys_State := STATE_FAULT;
END_IF;
END_FUNCTION_BLOCK"""

data = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": assistant_response}
    ]
}

# Write to both locations to be safe
paths = [
    r"C:\Users\majip\Downloads\LLM REASEARCH\Local_Ollama_Evol_Pipeline\data\evol_instruct_dataset.jsonl",
    r"C:\Users\majip\Downloads\LLM REASEARCH\data\evol_instruct_dataset.jsonl"
]

for p in paths:
    try:
        with open(p, "a") as f:
            f.write(json.dumps(data) + "\n")
        print(f"Appended to {p}")
    except Exception as e:
        print(f"Error appending to {p}: {e}")

