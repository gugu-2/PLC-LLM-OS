import os, json, uuid
st_code = """```iec-st
FUNCTION_BLOCK FB_HVDC_VSC_Control
TITLE = 'HVDC VSC MMC Advanced Controller'
VERSION : '2.5'

VAR_INPUT
    Enable : BOOL; // Enable VSC operation
    V_dc_ref : REAL; // DC voltage reference (kV)
    P_ref : REAL; // Active power reference (MW)
    Q_ref : REAL; // Reactive power reference (MVAr)
    V_grid_abc : ARRAY[0..2] OF REAL; // Grid voltages (kV)
    I_grid_abc : ARRAY[0..2] OF REAL; // Grid currents (kA)
    V_dc_meas : REAL; // Measured DC voltage (kV)
    Submodule_V_cap : ARRAY[0..511] OF REAL; // Submodule capacitor voltages
    Submodule_Status : ARRAY[0..511] OF BOOL; // Submodule health status
    Fault_DC_Line : BOOL; // DC line fault detection flag
END_VAR

VAR_OUTPUT
    Switching_Cmds : ARRAY[0..511] OF BOOL; // Submodule switching commands
    V_dc_err : REAL; // DC voltage error
    P_meas : REAL; // Measured active power
    Q_meas : REAL; // Measured reactive power
    System_Ready : BOOL;
    Fault_Blocked : BOOL;
END_VAR

VAR
    // Internal variables for Park/Clarke transformations
    alpha, beta : REAL;
    d, q : REAL;
    theta_pll : REAL;
    sin_theta, cos_theta : REAL;
    
    // PI Controller states
    PI_Vdc_integral : REAL;
    PI_Id_integral : REAL;
    PI_Iq_integral : REAL;
    
    // Decoupling network
    omega : REAL := 314.159; // 50Hz in rad/s
    L_grid : REAL := 0.05; // Grid inductance (H)
    
    // Submodule balancing
    i, j, temp_idx : INT;
    sorted_indices : ARRAY[0..511] OF INT;
    temp_val : REAL;
    cap_voltages_sorted : ARRAY[0..511] OF REAL;
    arm_current_dir : INT; // 1 for charging, -1 for discharging
    num_inserted : INT;
    
    // Fault handling
    block_timer : TIME;
    is_blocked : BOOL := FALSE;
END_VAR

// -- Execution --
IF NOT Enable THEN
    System_Ready := FALSE;
    PI_Vdc_integral := 0.0;
    PI_Id_integral := 0.0;
    PI_Iq_integral := 0.0;
    FOR i := 0 TO 511 DO
        Switching_Cmds[i] := FALSE;
    END_FOR;
    RETURN;
END_IF;

// 1. DC Fault Blocking Sequence
IF Fault_DC_Line THEN
    is_blocked := TRUE;
    Fault_Blocked := TRUE;
    // Block all submodules to clear DC fault
    FOR i := 0 TO 511 DO
        Switching_Cmds[i] := FALSE;
    END_FOR;
    RETURN; // Halt normal control execution
ELSE
    is_blocked := FALSE;
    Fault_Blocked := FALSE;
END_IF;

// 2. Phase-Locked Loop (PLL) - Simplified for brevity
theta_pll := theta_pll + 0.00314;
IF theta_pll > 6.28318 THEN
    theta_pll := theta_pll - 6.28318;
END_IF;
sin_theta := SIN(theta_pll);
cos_theta := COS(theta_pll);

// 3. Active and Reactive Power Calculation & Decoupling
alpha := (2.0/3.0) * (V_grid_abc[0] - 0.5*V_grid_abc[1] - 0.5*V_grid_abc[2]);
beta  := (2.0/3.0) * (0.866025*V_grid_abc[1] - 0.866025*V_grid_abc[2]);

d := alpha * cos_theta + beta * sin_theta;
q := -alpha * sin_theta + beta * cos_theta;

P_meas := 1.5 * (d * I_grid_abc[0] + q * I_grid_abc[1]);
Q_meas := 1.5 * (q * I_grid_abc[0] - d * I_grid_abc[1]);

V_dc_err := V_dc_ref - V_dc_meas;
PI_Vdc_integral := PI_Vdc_integral + (V_dc_err * 0.001);

// 4. MMC Submodule Capacitor Voltage Balancing Algorithm
IF I_grid_abc[0] > 0.0 THEN
    arm_current_dir := 1; 
ELSE
    arm_current_dir := -1; 
END_IF;

FOR i := 0 TO 511 DO
    sorted_indices[i] := i;
    cap_voltages_sorted[i] := Submodule_V_cap[i];
END_FOR;

FOR i := 0 TO 510 DO
    FOR j := 0 TO 510 - i DO
        IF cap_voltages_sorted[j] > cap_voltages_sorted[j+1] THEN
            temp_val := cap_voltages_sorted[j];
            cap_voltages_sorted[j] := cap_voltages_sorted[j+1];
            cap_voltages_sorted[j+1] := temp_val;
            temp_idx := sorted_indices[j];
            sorted_indices[j] := sorted_indices[j+1];
            sorted_indices[j+1] := temp_idx;
        END_IF;
    END_FOR;
END_FOR;

num_inserted := 256;

FOR i := 0 TO 511 DO
    Switching_Cmds[i] := FALSE;
END_FOR;

IF arm_current_dir = 1 THEN
    FOR i := 0 TO (num_inserted - 1) DO
        IF Submodule_Status[sorted_indices[i]] THEN
            Switching_Cmds[sorted_indices[i]] := TRUE;
        END_IF;
    END_FOR;
ELSE
    FOR i := 511 DOWNTO (512 - num_inserted) DO
        IF Submodule_Status[sorted_indices[i]] THEN
            Switching_Cmds[sorted_indices[i]] := TRUE;
        END_IF;
    END_FOR;
END_IF;

System_Ready := TRUE;
END_FUNCTION_BLOCK
```"""

prompt = "You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.\nYour specific domain is: HVDC Voltage Source Converter (VSC) Substation.\nTask: Invent a highly complex control scenario for this domain (e.g., modular multilevel converter (MMC) submodule capacitor voltage balancing, active/reactive power decoupling, and DC fault blocking).\nWrite a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": st_code}]}

os.makedirs("data/swarm_raw", exist_ok=True)
uid = uuid.uuid4().hex[:8]
with open(f"data/swarm_raw/agent_{uid}.json", "w", encoding="utf-8") as f:
    json.dump(record, f)

with open("data/synthetic_generation_v3_enterprise.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\\n")
