import json
import os

prompt = '''You are acting as the Principal Grid Architect for a Smart Energy Consortium.

Your mission is to generate a master-tier, production-ready IEC 61131-3 Structured Text (ST) implementation for the "Superconducting Magnetic Energy Storage (SMES) Grid Stabilizer & Cryocooler Controller" (FB_SMES_GridStabilizer).

### Technical Specifications & Engineering Rigor Required:
1. **Superconducting Coil Energy Transfer**:
   - Bi-directional AC/DC voltage source converter (VSC) regulating the energy transfer ( = 1/2 L I^2$) between a 5000 A superconducting niobium-titanium (NbTi) coil and the AC power grid.
   - Four-quadrant active (P) and reactive (Q) power injection with sub-cycle (< 10 ms) response time to stabilize grid voltage sags and frequency deviations.
2. **Cryogenic Quench & Cooling Matrix**:
   - Liquid Helium bath at 4.2 K with continuous boil-off recondensation via a Gifford-McMahon cryocooler.
   - Resistive voltage tap quench detection triggering a fast DC breaker to shunt the 5000 A current into an external dump resistor before the coil melts.
3. **Code Quality**: Strict IEC 61131-3 ST, LREAL datatypes, redundant SIL-3 safety interlocks, PackML states.

Output a complete, valid JSON object with {"messages": [{"role": "user", "content": "Mega-prompt description"}, {"role": "assistant", "content": "Full raw Structured Text code inside `iec-st`"}]}.
'''

code = '''`iec-st
(*
================================================================================
Superconducting Magnetic Energy Storage (SMES) Grid Stabilizer & Cryocooler Controller
================================================================================
Author: Principal Grid Architect
Standard: IEC 61131-3 Structured Text (ST)
Safety: SIL-3 Redundant Interlocks
Protocol: PackML State Machine
================================================================================
*)

TYPE E_PackML_State :
(
    PML_UNDEFINED := 0,
    PML_CLEARED := 1,
    PML_STARTING := 2,
    PML_IDLE := 3,
    PML_SUSPENDED := 4,
    PML_EXECUTE := 5,
    PML_STOPPING := 6,
    PML_ABORTING := 7,
    PML_ABORTED := 8,
    PML_HOLDING := 9,
    PML_HELD := 10
);
END_TYPE

TYPE ST_Grid_Measurements :
STRUCT
    Voltage_A : LREAL; (* AC Voltage Phase A (V) *)
    Voltage_B : LREAL; (* AC Voltage Phase B (V) *)
    Voltage_C : LREAL; (* AC Voltage Phase C (V) *)
    Frequency : LREAL; (* Grid Frequency (Hz) *)
    I_Grid_A  : LREAL; (* Grid Current Phase A (A) *)
    I_Grid_B  : LREAL; (* Grid Current Phase B (A) *)
    I_Grid_C  : LREAL; (* Grid Current Phase C (A) *)
END_STRUCT
END_TYPE

TYPE ST_SMES_Sensors :
STRUCT
    Coil_Current  : LREAL; (* SMES Coil Current (A) *)
    dIdt_Coil     : LREAL; (* Derivative of Current (A/s) *)
    Voltage_Tap_1 : LREAL; (* Diff Voltage across half coil 1 (V) *)
    Voltage_Tap_2 : LREAL; (* Diff Voltage across half coil 2 (V) *)
    LHe_Level     : LREAL; (* Liquid Helium Level (%) *)
    LHe_Temp      : LREAL; (* Liquid Helium Bath Temperature (K) *)
    VSC_DC_Bus    : LREAL; (* DC Bus Voltage (V) *)
END_STRUCT
END_TYPE

FUNCTION_BLOCK FB_SMES_GridStabilizer
VAR_INPUT
    Enable            : BOOL;  (* System Enable Command *)
    Emergency_Stop    : BOOL;  (* Hardware E-Stop (NC) *)
    Grid_Data         : ST_Grid_Measurements;
    SMES_Data         : ST_SMES_Sensors;
    Cmd_P_Ref         : LREAL; (* Active Power Reference (W) *)
    Cmd_Q_Ref         : LREAL; (* Reactive Power Reference (VAR) *)
END_VAR

VAR_OUTPUT
    Current_State        : E_PackML_State;
    VSC_PWM_A            : LREAL; (* Duty cycle -1.0 to 1.0 *)
    VSC_PWM_B            : LREAL;
    VSC_PWM_C            : LREAL;
    DC_Breaker_Close     : BOOL;  (* TRUE = Breaker closed, coil online *)
    Dump_Resistor_Switch : BOOL;  (* TRUE = Switch closed, dump energy *)
    Cryocooler_Speed_Ref : LREAL; (* Compressor RPM *)
    Alarm_Quench         : BOOL;  (* Quench fault indicator *)
    Energy_Stored        : LREAL; (* Stored Energy (Joules) *)
END_VAR

VAR
    (* SMES Physical Constants *)
    L_COIL         : LREAL := 2.5;     (* Total Inductance (Henries) *)
    I_MAX          : LREAL := 5000.0;  (* Maximum Coil Current (A) *)
    T_CRIT         : LREAL := 5.2;     (* Critical Temp of NbTi (K) *)
    V_QUENCH_THRES : LREAL := 0.050;   (* 50mV Resistive Voltage Threshold *)
    NOMINAL_FREQ   : LREAL := 60.0;    (* Grid Hz *)
    DC_BUS_NOMINAL : LREAL := 1500.0;  (* VSC DC Bus Nominal (V) *)
    
    (* State Management *)
    State          : E_PackML_State := PML_ABORTED;
    Init_Done      : BOOL := FALSE;
    
    (* Execution Timing *)
    dT             : LREAL := 0.001; (* 1ms Task cycle *)
    
    (* Quench Detection Matrix *)
    U_Inductive_1  : LREAL;
    U_Inductive_2  : LREAL;
    U_Resistive_1  : LREAL;
    U_Resistive_2  : LREAL;
    Quench_Detected: BOOL;
    
    (* Cryocooler Gifford-McMahon PI Controller *)
    Temp_Setpoint  : LREAL := 4.2;
    Err_Temp       : LREAL;
    Temp_Integral  : LREAL;
    Kp_Cryo        : LREAL := 250.0;
    Ki_Cryo        : LREAL := 10.0;
    
    (* Grid Synchronization (PLL/dq0 Transformation) *)
    Grid_Theta     : LREAL;
    Grid_Omega     : LREAL;
    V_alpha, V_beta: LREAL;
    I_alpha, I_beta: LREAL;
    Vd, Vq         : LREAL;
    Id, Iq         : LREAL;
    
    (* VSC Four-Quadrant Decoupled Control *)
    Id_Ref, Iq_Ref : LREAL;
    Id_Err, Iq_Err : LREAL;
    Id_Int, Iq_Int : LREAL;
    Kp_VSC         : LREAL := 0.05;
    Ki_VSC         : LREAL := 2.5;
    Vd_Cmd, Vq_Cmd : LREAL;
    V_alpha_Cmd, V_beta_Cmd : LREAL;
    
    (* Interlocks *)
    SIL3_Hardware_OK : BOOL;
    SIL3_Software_OK : BOOL;
    SIL3_Trip        : BOOL;
END_VAR

(* ---------------------------------------------------------
   1. STORED ENERGY CALCULATION (E = 1/2 L I^2)
--------------------------------------------------------- *)
Energy_Stored := 0.5 * L_COIL * (SMES_Data.Coil_Current * SMES_Data.Coil_Current);

(* ---------------------------------------------------------
   2. REDUNDANT SIL-3 QUENCH DETECTION (Voltage Tap Method)
   L1 = L2 = L_COIL / 2
   U_tap = L*(di/dt) + R*I
   U_res = U_tap - L*(di/dt)
--------------------------------------------------------- *)
U_Inductive_1 := (L_COIL / 2.0) * SMES_Data.dIdt_Coil;
U_Inductive_2 := (L_COIL / 2.0) * SMES_Data.dIdt_Coil;

U_Resistive_1 := ABS(SMES_Data.Voltage_Tap_1 - U_Inductive_1);
U_Resistive_2 := ABS(SMES_Data.Voltage_Tap_2 - U_Inductive_2);

IF (U_Resistive_1 > V_QUENCH_THRES) OR (U_Resistive_2 > V_QUENCH_THRES) THEN
    Quench_Detected := TRUE;
    Alarm_Quench    := TRUE;
END_IF;

(* ---------------------------------------------------------
   3. SAFETY INTERLOCK MATRIX
--------------------------------------------------------- *)
SIL3_Hardware_OK := Emergency_Stop; (* NC circuit *)
SIL3_Software_OK := (SMES_Data.Coil_Current <= I_MAX) AND 
                    (SMES_Data.LHe_Temp < T_CRIT) AND 
                    NOT Quench_Detected;

SIL3_Trip := NOT (SIL3_Hardware_OK AND SIL3_Software_OK);

(* ---------------------------------------------------------
   4. PACKML STATE MACHINE LOGIC
--------------------------------------------------------- *)
CASE State OF
    PML_UNDEFINED, PML_CLEARED:
        IF SIL3_Trip THEN
            State := PML_ABORTING;
        ELSIF Enable THEN
            State := PML_STARTING;
        END_IF;
        
    PML_STARTING:
        (* Charge DC Bus and cool down coil *)
        IF NOT SIL3_Trip AND (SMES_Data.LHe_Temp <= 4.25) AND (SMES_Data.VSC_DC_Bus >= DC_BUS_NOMINAL * 0.95) THEN
            State := PML_IDLE;
        ELSIF SIL3_Trip THEN
            State := PML_ABORTING;
        END_IF;
        
    PML_IDLE:
        DC_Breaker_Close := TRUE;
        Dump_Resistor_Switch := FALSE;
        IF Enable AND (Cmd_P_Ref <> 0.0 OR Cmd_Q_Ref <> 0.0) THEN
            State := PML_EXECUTE;
        ELSIF SIL3_Trip THEN
            State := PML_ABORTING;
        ELSIF NOT Enable THEN
            State := PML_STOPPING;
        END_IF;
        
    PML_EXECUTE:
        IF SIL3_Trip THEN
            State := PML_ABORTING;
        ELSIF (Cmd_P_Ref = 0.0 AND Cmd_Q_Ref = 0.0) THEN
            State := PML_IDLE;
        ELSIF NOT Enable THEN
            State := PML_STOPPING;
        END_IF;
        
    PML_STOPPING:
        DC_Breaker_Close := FALSE;
        IF (SMES_Data.Coil_Current < 10.0) THEN
            State := PML_CLEARED;
        END_IF;
        
    PML_ABORTING:
        (* FAST DISCHARGE DUE TO QUENCH OR FAULT *)
        DC_Breaker_Close     := FALSE; 
        Dump_Resistor_Switch := TRUE; (* Shunt current to external resistor *)
        Id_Ref := 0.0;
        Iq_Ref := 0.0;
        IF (SMES_Data.Coil_Current < 1.0) THEN
            State := PML_ABORTED;
        END_IF;
        
    PML_ABORTED:
        DC_Breaker_Close     := FALSE;
        Dump_Resistor_Switch := FALSE; (* Safe to open dump switch *)
        IF Emergency_Stop AND NOT Quench_Detected THEN
            State := PML_CLEARED; (* Reset only if quench is cleared and estop pulled *)
        END_IF;
END_CASE;

Current_State := State;

(* ---------------------------------------------------------
   5. CRYOGENIC GIFFORD-MCMAHON PI CONTROLLER
--------------------------------------------------------- *)
Err_Temp := SMES_Data.LHe_Temp - Temp_Setpoint;
IF State <> PML_ABORTED THEN
    Temp_Integral := Temp_Integral + (Err_Temp * dT);
    (* Anti-windup *)
    IF Temp_Integral > 100.0 THEN Temp_Integral := 100.0; END_IF;
    IF Temp_Integral < -50.0 THEN Temp_Integral := -50.0; END_IF;
    
    Cryocooler_Speed_Ref := (Kp_Cryo * Err_Temp) + (Ki_Cryo * Temp_Integral);
    
    IF Cryocooler_Speed_Ref > 1500.0 THEN Cryocooler_Speed_Ref := 1500.0; END_IF;
    IF Cryocooler_Speed_Ref < 300.0 THEN Cryocooler_Speed_Ref := 300.0; END_IF;
ELSE
    Cryocooler_Speed_Ref := 0.0;
END_IF;

(* ---------------------------------------------------------
   6. GRID VSC FOUR-QUADRANT CONTROL (Sub-cycle response)
--------------------------------------------------------- *)
IF (State = PML_EXECUTE) THEN
    (* Simulated PLL (Phase Locked Loop) integration *)
    Grid_Omega := 2.0 * 3.14159265359 * Grid_Data.Frequency;
    Grid_Theta := Grid_Theta + (Grid_Omega * dT);
    IF Grid_Theta >= 2.0 * 3.14159265359 THEN
        Grid_Theta := Grid_Theta - 2.0 * 3.14159265359;
    END_IF;
    
    (* Clarke Transform (abc to alpha-beta) *)
    V_alpha := (2.0/3.0) * (Grid_Data.Voltage_A - 0.5*Grid_Data.Voltage_B - 0.5*Grid_Data.Voltage_C);
    V_beta  := (2.0/3.0) * (0.8660254*Grid_Data.Voltage_B - 0.8660254*Grid_Data.Voltage_C);
    
    I_alpha := (2.0/3.0) * (Grid_Data.I_Grid_A - 0.5*Grid_Data.I_Grid_B - 0.5*Grid_Data.I_Grid_C);
    I_beta  := (2.0/3.0) * (0.8660254*Grid_Data.I_Grid_B - 0.8660254*Grid_Data.I_Grid_C);
    
    (* Park Transform (alpha-beta to d-q) *)
    Vd := V_alpha * COS(Grid_Theta) + V_beta * SIN(Grid_Theta);
    Vq := -V_alpha * SIN(Grid_Theta) + V_beta * COS(Grid_Theta);
    
    Id := I_alpha * COS(Grid_Theta) + I_beta * SIN(Grid_Theta);
    Iq := -I_alpha * SIN(Grid_Theta) + I_beta * COS(Grid_Theta);
    
    (* PQ Decoupled Reference Calculation (Id -> P, Iq -> Q) 
       Assuming Vq approx 0 under PLL lock:
       P = 3/2 * Vd * Id  => Id_Ref = P_Ref / (1.5 * Vd)
       Q = -3/2 * Vd * Iq => Iq_Ref = -Q_Ref / (1.5 * Vd) 
    *)
    IF Vd > 10.0 THEN
        Id_Ref := Cmd_P_Ref / (1.5 * Vd);
        Iq_Ref := -Cmd_Q_Ref / (1.5 * Vd);
    ELSE
        Id_Ref := 0.0;
        Iq_Ref := 0.0;
    END_IF;
    
    (* Current PI Controllers *)
    Id_Err := Id_Ref - Id;
    Iq_Err := Iq_Ref - Iq;
    
    Id_Int := Id_Int + (Id_Err * dT);
    Iq_Int := Iq_Int + (Iq_Err * dT);
    
    (* PI output with decoupling feed-forward *)
    Vd_Cmd := (Kp_VSC * Id_Err) + (Ki_VSC * Id_Int) - (Grid_Omega * L_COIL * Iq) + Vd;
    Vq_Cmd := (Kp_VSC * Iq_Err) + (Ki_VSC * Iq_Int) + (Grid_Omega * L_COIL * Id) + Vq;
    
    (* Inverse Park Transform *)
    V_alpha_Cmd := Vd_Cmd * COS(Grid_Theta) - Vq_Cmd * SIN(Grid_Theta);
    V_beta_Cmd  := Vd_Cmd * SIN(Grid_Theta) + Vq_Cmd * COS(Grid_Theta);
    
    (* Inverse Clarke Transform to PWM Duty Cycles (-1 to 1) *)
    VSC_PWM_A := V_alpha_Cmd / SMES_Data.VSC_DC_Bus;
    VSC_PWM_B := (-0.5 * V_alpha_Cmd + 0.8660254 * V_beta_Cmd) / SMES_Data.VSC_DC_Bus;
    VSC_PWM_C := (-0.5 * V_alpha_Cmd - 0.8660254 * V_beta_Cmd) / SMES_Data.VSC_DC_Bus;
    
    (* PWM Saturation *)
    IF VSC_PWM_A > 1.0 THEN VSC_PWM_A := 1.0; ELSIF VSC_PWM_A < -1.0 THEN VSC_PWM_A := -1.0; END_IF;
    IF VSC_PWM_B > 1.0 THEN VSC_PWM_B := 1.0; ELSIF VSC_PWM_B < -1.0 THEN VSC_PWM_B := -1.0; END_IF;
    IF VSC_PWM_C > 1.0 THEN VSC_PWM_C := 1.0; ELSIF VSC_PWM_C < -1.0 THEN VSC_PWM_C := -1.0; END_IF;
ELSE
    VSC_PWM_A := 0.0;
    VSC_PWM_B := 0.0;
    VSC_PWM_C := 0.0;
    Id_Int    := 0.0;
    Iq_Int    := 0.0;
END_IF;

END_FUNCTION_BLOCK
`'''

doc = {
    "messages": [
        {
            "role": "user",
            "content": prompt
        },
        {
            "role": "assistant",
            "content": code
        }
    ]
}

target_file = r"C:\Users\majip\Downloads\LLM REASEARCH\Local_Ollama_Evol_Pipeline\seeds\tier1_enterprise_grade\synthetic_generation_v3_enterprise.jsonl"
with open(target_file, "a", encoding="utf-8") as f:
    f.write(json.dumps(doc) + "\\n")
