# -*- coding: utf-8 -*-
"""
Full Dataset Generator for FB_Semiconductor_WireBonding_ThermoSonic_Sync
Output: data/swarm_raw/agent_41e92a8c.json
"""
import os, sys, json, re

USER_PROMPT = """You are the Principal Automation Fellow & Cyber-Physical Systems Chair (V7 Max-Persona, 75+ years veteran industrial engineer).
Your mission is to generate a massive, ultra-rigorous, production-ready, fully unrolled IEC 61131-3 Structured Text dataset for heavy commercial manufacturing: Semiconductor Assembly & Advanced IC Packaging.

TARGET DOMAIN:
- Sector: Heavy Commercial Manufacturing - Semiconductor Assembly & Advanced IC Packaging
- System: High-Speed Automatic Thermo-Sonic Ball & Wedge Wire Bonder (35 um ultra-fine pitch, 18 wires/sec, EFO spark generator, piezoelectric ultrasonic transducer resonance tracking, voice-coil bond head force control)
- Function Block Name: FB_Semiconductor_WireBonding_ThermoSonic_Sync
- Target Output File: data/swarm_raw/agent_41e92a8c.json

CYBER-PHYSICAL MATHEMATICAL RIGOR & ARCHITECTURAL MANDATES:
1. Discrete State-Space Model (12 States, 4 Inputs, 6 Outputs):
   - 12 States: Bond head Z-position (um), Z-velocity (um/ms), voice coil current (mA), impact contact force (mN), ultrasonic transducer electrical impedance Z_us (Ohm), horn vibration amplitude (um), Free Air Ball (FAB) diameter (um), heated capillary tip temperature (deg C), leadframe substrate temperature (deg C), wire tail elongation strain (um/mm), wire loop apex height (um), capillary wear factor (dim).
   - 4 Inputs: Voice coil current drive command (mA), Ultrasonic generator power command (W), EFO spark discharge current (mA), Capillary heating element PWM duty cycle (%).
   - 6 Outputs: Measured bond head Z-position (um), Measured contact bond force (mN), Measured ultrasonic transducer impedance (Ohm), Measured ultrasonic vibration amplitude (um), Measured capillary tip temperature (deg C), Measured leadframe temperature (deg C).
   - Fully unrolled matrix update: x_{k+1} = A * x_k + B * u_k, y_k = C * x_k + D * u_k.
   - Discrete steady-state Kalman Filter: x_hat_{k|k} = x_hat_{k|k-1} + L * (y_meas - C * x_hat_{k|k-1}).
2. Model Predictive Control (MPC):
   - Unrolled 10-step horizon Projected Gradient Descent (PGD).
   - Quadratic stage cost: (x - x_ref)^T * Q * (x - x_ref) + u^T * R * u + delta_u^T * S * delta_u.
   - Explicit voice coil force slew rate and ultrasonic power saturation limits.
3. Triple Modular Redundant (TMR) 2oo3 Voting Logic:
   - 4 safety-critical channels: Capillary Z-Axis Optical Linear Encoder (ChA, ChB, ChC), Voice-Coil Piezoelectric Dynamic Impact Force Sensor (ChA, ChB, ChC), Leadframe Heated Vacuum Anvil Pyrometers (ChA, ChB, ChC), Ultrasonic Generator RF Phase/Current Pickoff (ChA, ChB, ChC).
   - Discrepancy timers (10ms), bumpless degradation to 1oo2, and fail-safe capillary retract on dual disagreement.
4. 14-Stage Production FSM:
   - CASE State OF:
     0: IDLE_SAFE_STANDBY
     1: LEADFRAME_INDEXING_VACUUM_CLAMP
     2: DUAL_CAMERA_PR_DIE_ALIGNMENT
     3: HIGH_VOLTAGE_EFO_SPARK_BALL_FORMATION
     4: RAPID_TRAVERSE_Z_SEARCH_TOUCHDOWN
     5: FIRST_BOND_DIE_PAD_THERMOSONIC_SCRUB
     6: CONTROLLED_WIRE_LOOPING_TRAJECTORY
     7: SECOND_BOND_LEAD_WEDGE_STITCH_FORMATION
     8: WIRE_CLAMP_PULL_TAIL_BREAK_OFF
     9: OPTICAL_POST_BOND_WIRE_INTEGRITY_CHECK
     10: LEADFRAME_UNCLAMP_INDEX_STEP
     11: EMERGENCY_CAPILLARY_LIFT_RECOVERY
     12: CALIBRATION_EFO_SPARK_ENERGY_TARE
     13: MANUAL_TEACH_SUPERVISORY_ALIGN
   - Fully detailed transitions, interlocks, timeout fault traps, and diagnostic tracking.
5. ANSI/ISA-18.2 Multi-Tiered Alarm Engine:
   - HH (Trip), H (Warning), L (Low Warning), LL (Low Trip) for all critical physical variables.
   - Configurable hysteresis deadbands, persistence timers, alarm suppression during startup, and bit-packed DWORD alarm registers.
6. 100% Exact Syntax & Parity:
   - Triple backticks with `iec-st`.
   - First line: FUNCTION_BLOCK FB_Semiconductor_WireBonding_ThermoSonic_Sync
   - Last line: END_FUNCTION_BLOCK
   - Every IF has END_IF;, every CASE has END_CASE;, every FOR has END_FOR;.
"""

def generate_header():
    return """FUNCTION_BLOCK FB_Semiconductor_WireBonding_ThermoSonic_Sync
(* ==================================================================================================== *)
(* LUMINA CYBER-PHYSICAL AUTOMATION ARCHITECTURE - V7 MAX-PERSONA (75+ YRS INDUSTRIAL FELLOW EXPERIENCE)   *)
(* DOMAIN: HEAVY COMMERCIAL MANUFACTURING - SEMICONDUCTOR ASSEMBLY & ADVANCED IC PACKAGING             *)
(* SYSTEM: HIGH-SPEED AUTOMATIC THERMO-SONIC BALL & WEDGE WIRE BONDER                                   *)
(*         35 UM ULTRA-FINE PITCH, 18-22 WIRES/SEC, HIGH-VOLTAGE EFO SPARK GENERATOR, PIEZOELECTRIC    *)
(*         ULTRASONIC TRANSDUCER RESONANCE TRACKING, DIRECT-DRIVE VOICE-COIL BOND HEAD FORCE CONTROL    *)
(* STANDARDS COMPLIANCE: SEMI E10 (RAM), SEMI G44 (WIRE BOND PULL/SHEAR), ANSI/ISA-18.2 (ALARMS),        *)
(*                       IEC 61508 SIL-3 (2oo3 TMR SENSOR VOTING), IEEE 1451 SENSOR INTERFACES          *)
(* EXECUTION PROFILE: REAL-TIME SERVO CYCLE TIME Ts = 0.0002 s (5.0 kHz / 200 MICROSECONDS SERVO LOOP)    *)
(* ==================================================================================================== *)
(*
 * CYBER-PHYSICAL FIRST-PRINCIPLES MATHEMATICAL MODELING:
 * 1. HIGH-BANDWIDTH DIRECT-DRIVE VOICE COIL MOTOR (VCM) ELECTROMECHANICS:
 *    Bond head vertical translation (Z-axis) dynamics are governed by Newton-Lorentz second-order balance:
 *      m_head * d2(z)/dt2 + c_viscous * d(z)/dt + k_flexure * z = K_force * i_vc - F_contact(z, z_surface)
 *    where:
 *      m_head    = Bond head moving mass (capillary, horn, transducer, coil) [kg] (~0.125 kg)
 *      c_viscous = Viscous damping coefficient of air-bearing / linear guide [N*s/m] (~2.40 N*s/m)
 *      k_flexure = Flexure suspension parasitic stiffness [N/m] (~45.0 N/m)
 *      K_force   = Voice coil motor force sensitivity constant [N/A] (~14.80 N/A)
 *      i_vc      = Voice coil armature current [A]
 *      F_contact = Dynamic normal contact force between capillary tip and bond pad [N]
 *                  Modeled via nonlinear Hunt-Crossley elastoplastic contact mechanics:
 *                  F_contact = K_contact * delta^p + C_contact * delta^p * d(delta)/dt  (for delta > 0)
 *
 * 2. PIEZOELECTRIC ULTRASONIC TRANSDUCER ELECTRO-ACOUSTIC RESONANCE TRACKING:
 *    The 60 kHz to 138 kHz longitudinal vibration horn is parameterized via Butterworth-Van Dyke (BVD):
 *      Z_us(j*omega) = 1 / ( j*omega*C0 + 1 / ( R_m + j*(omega*L_m - 1/(omega*C_m)) + Z_load ) )
 *    where:
 *      C0     = Transducer static clamped capacitance [nF] (~3.85 nF)
 *      R_m    = Motional resistance reflecting mechanical acoustic loss [Ohm] (~12.5 Ohm)
 *      L_m    = Motional inductance reflecting acoustic horn equivalent mass [mH] (~28.4 mH)
 *      C_m    = Motional capacitance reflecting acoustic horn equivalent compliance [pF] (~98.2 pF)
 *      Z_load = Mechanical acoustic impedance at the bond interface [Ohm]
 *               Z_load = gamma_friction * F_bond + beta_softening * IMC_depth
 *    Resonance tracking PLL phase detector:
 *      Delta_phi = Phase(V_us) - Phase(I_us);  d(omega_us)/dt = - K_pll * sin(Delta_phi)
 *
 * 3. ELECTRONIC FLAME OFF (EFO) TOWNSEND AVALANCHE & FREE AIR BALL (FAB) MELTING:
 *    Negative DC pulsed spark discharge (-1000V to -4200V) between EFO spark rod and wire tail:
 *      E_efo = integral( V_spark(t) * I_spark(t) * dt )  from t_start to t_extinguish
 *    Thermal conservation of molten sphere formation under 95% N2 / 5% H2 shielding gas:
 *      rho_wire * ( Delta_H_fusion + c_p_liquid * (T_melt - T_ambient) ) * V_fab = eta_efo * E_efo
 *      D_fab = [ (6.0 * eta_efo * E_efo) / ( pi * rho_wire * (Delta_H_fusion + c_p * Delta_T) ) ]^(1/3)
 *
 * 4. INTERMETALLIC COMPOUND (IMC) KINETICS & THERMOSONIC DIFFUSION:
 *    Au-Al or Cu-Al solid-state intermetallic growth rate at the scrub interface:
 *      dX_imc / dt = ( k_0 * exp( - Q_activation / (R_gas * T_interface) ) ) / ( 2.0 * X_imc )
 *                    * ( 1.0 + alpha_us * P_ultrasonic * (1.0 - exp(-t / tau_acoustic)) )
 *    Interface temperature under simultaneous heated anvil (T_sub) and friction heating:
 *      T_interface = T_sub + ( T_cap - T_sub ) * eta_cond + ( mu_fric * F_bond * omega_us * A_horn ) / ( 4.0 * J_th * k_th_die )
 *
 * 5. TRIPLE MODULAR REDUNDANCY (2oo3 TMR) SENSOR VOTING WITH 10 MS DISCREPANCY TIMERS:
 *    4 Safety-critical instrumented loops:
 *      Channel 1: Optical Linear Glass Scale Z-Encoder (ChA, ChB, ChC) [um]
 *      Channel 2: Piezoelectric Dynamic Impact Force Transducer (ChA, ChB, ChC) [mN]
 *      Channel 3: Heated Leadframe Vacuum Anvil IR Pyrometers (ChA, ChB, ChC) [deg C]
 *      Channel 4: Ultrasonic Generator RF Phase/Current Pickoff (ChA, ChB, ChC) [deg]
 *    Degradation hierarchy: 2oo3 Median -> 1oo2 Mean -> 1oo1 Direct Advisory -> Fail-Safe Z-Retract.
 *)
"""

def generate_var_input():
    return """VAR_INPUT
    (* === MASTER SYSTEM CONTROL & SAFETY INTERLOCKS === *)
    b_Enable_System : BOOL; (* Master system run enable command *)
    b_Safety_Interlock_OK : BOOL; (* Hardware safety enclosure interlock loop closed and verified *)
    b_EFO_Gas_Shroud_Flow_OK : BOOL; (* Forming gas (95% N2 / 5% H2) flow pressure switch OK *)
    b_Reset_Alarms : BOOL; (* Alarm manual reset and fault acknowledgement button *)
    b_Start_Auto_Cycle : BOOL; (* Automatic high-speed bonding cycle start command *)
    b_Stop_Cycle_End : BOOL; (* Cycle stop at current leadframe completion *)
    b_Manual_Jog_Z_Up : BOOL; (* Manual supervisory jog Z-axis up command *)
    b_Manual_Jog_Z_Down : BOOL; (* Manual supervisory jog Z-axis down command *)

    (* === INSTRUMENTATION CHANNEL 1: CAPILLARY Z-AXIS OPTICAL ENCODERS [um] === *)
    r_Enc_Z_Position_ChA_um : REAL; (* [um] Optical linear glass scale Z position Channel A *)
    r_Enc_Z_Position_ChB_um : REAL; (* [um] Optical linear glass scale Z position Channel B *)
    r_Enc_Z_Position_ChC_um : REAL; (* [um] Optical linear glass scale Z position Channel C *)

    (* === INSTRUMENTATION CHANNEL 2: PIEZOELECTRIC IMPACT FORCE TRANSDUCERS [mN] === *)
    r_Force_Sensor_ChA_mN : REAL; (* [mN] Voice-coil piezoelectric dynamic impact force Channel A *)
    r_Force_Sensor_ChB_mN : REAL; (* [mN] Voice-coil piezoelectric dynamic impact force Channel B *)
    r_Force_Sensor_ChC_mN : REAL; (* [mN] Voice-coil piezoelectric dynamic impact force Channel C *)

    (* === INSTRUMENTATION CHANNEL 3: HEATED VACUUM ANVIL PYROMETERS [deg C] === *)
    r_Pyrometer_Temp_ChA_degC : REAL; (* [deg C] Leadframe heated vacuum anvil optical pyrometer Channel A *)
    r_Pyrometer_Temp_ChB_degC : REAL; (* [deg C] Leadframe heated vacuum anvil optical pyrometer Channel B *)
    r_Pyrometer_Temp_ChC_degC : REAL; (* [deg C] Leadframe heated vacuum anvil optical pyrometer Channel C *)

    (* === INSTRUMENTATION CHANNEL 4: ULTRASONIC GENERATOR RF PHASE PICKOFF [deg] === *)
    r_US_Phase_ChA_deg : REAL; (* [deg] Ultrasonic RF voltage-to-current phase angle Channel A *)
    r_US_Phase_ChB_deg : REAL; (* [deg] Ultrasonic RF voltage-to-current phase angle Channel B *)
    r_US_Phase_ChC_deg : REAL; (* [deg] Ultrasonic RF voltage-to-current phase angle Channel C *)

    (* === ANCILLARY PROCESS TRANSDUCERS & SENSORS === *)
    r_Leadframe_Vacuum_Pressure_Bar : REAL; (* [bar] Leadframe anvil vacuum clamping differential pressure *)
    r_US_Transducer_Current_mA : REAL; (* [mA] Ultrasonic piezoelectric transducer primary current *)
    r_US_Transducer_Voltage_V : REAL; (* [V] Ultrasonic piezoelectric transducer primary voltage *)
    r_Capillary_Temp_Sensor_degC : REAL; (* [deg C] Ceramic capillary heated tip RTD thermocouple *)
    r_EFO_Spark_Discharge_V : REAL; (* [V] Electronic Flame Off capacitor discharge spark voltage *)
    r_EFO_Spark_Current_mA : REAL; (* [mA] Electronic Flame Off plasma gap discharge current *)
    r_Wire_Spool_Tension_mN : REAL; (* [mN] Gold/copper wire feed spool motorized tension sensor *)
    r_Vision_Die_Pad_X_Offset_um : REAL; (* [um] Pattern recognition camera die bond pad X misregistration *)
    r_Vision_Die_Pad_Y_Offset_um : REAL; (* [um] Pattern recognition camera die bond pad Y misregistration *)
    r_Vision_Lead_Finger_X_Offset_um : REAL; (* [um] Pattern recognition camera leadframe finger X offset *)
    r_Vision_Lead_Finger_Y_Offset_um : REAL; (* [um] Pattern recognition camera leadframe finger Y offset *)
    r_Cycle_Time_Delta_Sec : REAL; (* [s] Real-time execution task cycle time Ts (default 0.000200 s = 5.0 kHz) *)

    (* === RECIPE PARAMETERS & TARGET SETPOINTS === *)
    r_Recipe_Bond_Force_Die_mN : REAL; (* [mN] Recipe setpoint: 1st bond die pad normal contact force *)
    r_Recipe_US_Power_Die_W : REAL; (* [W] Recipe setpoint: 1st bond ultrasonic scrub RF power *)
    r_Recipe_Bond_Time_Die_ms : REAL; (* [ms] Recipe setpoint: 1st bond ultrasonic scrub dwell duration *)
    r_Recipe_Bond_Force_Lead_mN : REAL; (* [mN] Recipe setpoint: 2nd bond lead stitch normal contact force *)
    r_Recipe_US_Power_Lead_W : REAL; (* [W] Recipe setpoint: 2nd bond lead stitch ultrasonic RF power *)
    r_Recipe_Bond_Time_Lead_ms : REAL; (* [ms] Recipe setpoint: 2nd bond lead stitch dwell duration *)
    r_Recipe_Loop_Apex_Height_um : REAL; (* [um] Recipe setpoint: Wire loop trajectory apex elevation *)
    r_Recipe_FAB_Target_Dia_um : REAL; (* [um] Recipe setpoint: Target Free Air Ball molten diameter *)
    r_Recipe_Substrate_Temp_degC : REAL; (* [deg C] Recipe setpoint: Leadframe heated anvil temperature *)
    r_Recipe_Capillary_Temp_degC : REAL; (* [deg C] Recipe setpoint: Ceramic capillary tip temperature *)
END_VAR
"""

def generate_var_output():
    return """VAR_OUTPUT
    (* === ACTUATOR COMMANDS & SERVO SETPOINTS === *)
    r_VoiceCoil_Current_Cmd_mA : REAL; (* [mA] Voice-coil motor armature drive current command *)
    r_Ultrasonic_Power_Cmd_W : REAL; (* [W] Ultrasonic RF generator power output command *)
    r_Ultrasonic_Freq_Cmd_kHz : REAL; (* [kHz] Ultrasonic generator tracked resonance frequency command *)
    r_EFO_Discharge_Trigger_kV : REAL; (* [kV] Electronic Flame Off negative spark ignition command *)
    r_Capillary_Heater_PWM_pct : REAL; (* [%] Capillary tip ceramic heating element PWM command *)
    b_Wire_Clamp_Actuate : BOOL; (* Wire clamp motorized solenoid: TRUE=Grip, FALSE=Open *)
    b_Leadframe_Index_Advance : BOOL; (* Leadframe indexing walking-beam stepper trigger pulse *)
    b_Leadframe_Vacuum_Solenoid : BOOL; (* Leadframe anvil vacuum clamp solenoid valve drive *)

    (* === FINITE STATE MACHINE & EXECUTION STATUS === *)
    w_FSM_Current_State : INT; (* Current production FSM state ID (0 to 13) *)
    w_FSM_Sub_State : INT; (* Current active sub-state (0=Entry, 1=Execute, 2=Verify, 3=Exit) *)

    (* === ANSI/ISA-18.2 ALARM & STATUS REGISTERS === *)
    dw_Alarms_Trip_HH : DWORD; (* Bit-packed ISA-18.2 Critical High-High trip alarms *)
    dw_Alarms_Warning_H : DWORD; (* Bit-packed ISA-18.2 Warning High advisory alarms *)
    dw_Alarms_Warning_L : DWORD; (* Bit-packed ISA-18.2 Warning Low advisory alarms *)
    dw_Alarms_Trip_LL : DWORD; (* Bit-packed ISA-18.2 Critical Low-Low trip alarms *)
    dw_Device_Status_Word : DWORD; (* Bit-packed device operational status word *)
    dw_Safety_Interlock_Word : DWORD; (* Bit-packed SIL-3 safety interlock status register *)

    (* === KALMAN FILTER ESTIMATED CYBER-PHYSICAL STATES === *)
    r_Est_Bond_Head_Z_um : REAL; (* [um] Kalman estimated bond head capillary Z-position *)
    r_Est_Bond_Head_Vz_um_ms : REAL; (* [um/ms] Kalman estimated bond head vertical velocity *)
    r_Est_Bond_Force_mN : REAL; (* [mN] Kalman estimated bond pad normal contact force *)
    r_Est_US_Impedance_Ohm : REAL; (* [Ohm] Kalman estimated ultrasonic transducer electrical impedance *)
    r_Est_Horn_Amplitude_um : REAL; (* [um] Kalman estimated horn tip longitudinal vibration amplitude *)
    r_Est_FAB_Diameter_um : REAL; (* [um] Kalman estimated Free Air Ball diameter *)
    r_Est_Capillary_Temp_degC : REAL; (* [deg C] Kalman estimated heated capillary tip temperature *)
    r_Est_Substrate_Temp_degC : REAL; (* [deg C] Kalman estimated leadframe substrate temperature *)
    r_Est_Wire_Tail_Strain_pct : REAL; (* [%] Kalman estimated wire tail elongation strain *)
    r_Est_Loop_Apex_Height_um : REAL; (* [um] Kalman estimated wire loop apex trajectory height *)
    r_Est_Capillary_Wear_Factor : REAL; (* Dimensionless capillary ceramic tip abrasive wear factor *)

    (* === PRODUCTION DIAGNOSTICS & METRICS === *)
    r_Wires_Per_Second_Instant : REAL; (* [wires/sec] Instantaneous wire bonding throughput rate *)
    udi_Total_Wires_Bonded : UDINT; (* Total cumulative bonded wires counter *)
    b_Master_Trip : BOOL; (* Master safety trip summary flag *)
    b_Master_Warning : BOOL; (* Master operational warning summary flag *)
    b_FailSafe_Retract_Active : BOOL; (* Fail-safe high-speed capillary lift active *)
END_VAR
"""

print("Header, VAR_INPUT, VAR_OUTPUT defined.")

def generate_var_internal():
    lines = ["VAR", "    (* === MODEL PARAMETER MATRICES INITIALIZATION FLAG === *)", "    b_Model_Initialized : BOOL := FALSE;"]
    
    # State-space matrices
    lines.append("\n    (* === DISCRETE STATE TRANSITION MATRIX A [12x12] === *)")
    for i in range(1, 13):
        for j in range(1, 13):
            lines.append(f"    r_A_{i}_{j} : REAL := 0.0;")
            
    lines.append("\n    (* === DISCRETE INPUT COUPLING MATRIX B [12x4] === *)")
    for i in range(1, 13):
        for j in range(1, 5):
            lines.append(f"    r_B_{i}_{j} : REAL := 0.0;")
            
    lines.append("\n    (* === DISCRETE OUTPUT OBSERVATION MATRIX C [6x12] === *)")
    for i in range(1, 7):
        for j in range(1, 13):
            lines.append(f"    r_C_{i}_{j} : REAL := 0.0;")
            
    lines.append("\n    (* === DISCRETE DIRECT FEEDTHROUGH MATRIX D [6x4] === *)")
    for i in range(1, 7):
        for j in range(1, 5):
            lines.append(f"    r_D_{i}_{j} : REAL := 0.0;")
            
    lines.append("\n    (* === DISCRETE STEADY-STATE KALMAN FILTER GAIN MATRIX L [12x6] === *)")
    for i in range(1, 13):
        for j in range(1, 7):
            lines.append(f"    r_L_{i}_{j} : REAL := 0.0;")

    # State vectors
    lines.append("\n    (* === STATE ESTIMATES, PREDICTIONS, INNOVATIONS & REFERENCES === *)")
    for i in range(1, 13):
        lines.append(f"    r_x_hat_{i} : REAL := 0.0;")
        lines.append(f"    r_x_pred_{i} : REAL := 0.0;")
        lines.append(f"    r_x_ref_{i} : REAL := 0.0;")
    for i in range(1, 7):
        lines.append(f"    r_y_est_{i} : REAL := 0.0;")
        lines.append(f"    r_y_innov_{i} : REAL := 0.0;")
        lines.append(f"    r_y_meas_{i} : REAL := 0.0;")

    # MPC weights and parameters
    lines.append("\n    (* === MODEL PREDICTIVE CONTROL (MPC) COST WEIGHTS & LIMITS === *)")
    for i in range(1, 13):
        lines.append(f"    r_Q_{i} : REAL := 1.0;")
        lines.append(f"    r_P_{i} : REAL := 10.0;")
    for j in range(1, 5):
        lines.append(f"    r_R_{j} : REAL := 0.1;")
        lines.append(f"    r_S_{j} : REAL := 0.5;")
        lines.append(f"    r_u_min_{j} : REAL := -1000.0;")
        lines.append(f"    r_u_max_{j} : REAL := 1000.0;")
        lines.append(f"    r_du_max_{j} : REAL := 100.0;")
        lines.append(f"    r_u_cmd_{j} : REAL := 0.0;")
        lines.append(f"    r_u_prev_{j} : REAL := 0.0;")
    lines.append("    r_alpha_pgd : REAL := 0.0050;")
    lines.append("    r_J_terminal : REAL := 0.0;")

    # MPC 10-step horizon variables
    lines.append("\n    (* === MPC UNROLLED 10-STEP PREDICTION HORIZON VARIABLES === *)")
    for h in range(1, 11):
        lines.append(f"    (* --- Horizon Step {h} --- *)")
        lines.append(f"    r_J_stage_{h} : REAL := 0.0;")
        for i in range(1, 13):
            lines.append(f"    r_x_h{h}_{i} : REAL := 0.0;")
            lines.append(f"    r_lambda_h{h}_{i} : REAL := 0.0;")
            lines.append(f"    r_e_h{h}_{i} : REAL := 0.0;")
        for m in range(1, 5):
            lines.append(f"    r_u_h{h}_{m} : REAL := 0.0;")
            lines.append(f"    r_grad_h{h}_{m} : REAL := 0.0;")

    # TMR 2oo3 Voting variables
    lines.append("\n    (* === 4-CHANNEL 2oo3 TMR SENSOR VOTING VARIABLES === *)")
    channel_names = [
        "1_Enc_Z",
        "2_Force",
        "3_Pyrometer",
        "4_US_Phase"
    ]
    for ch_idx, ch_name in enumerate(channel_names, 1):
        lines.append(f"    (* Channel {ch_idx}: {ch_name} *)")
        lines.append(f"    r_voted_{ch_idx} : REAL := 0.0;")
        lines.append(f"    r_last_voted_{ch_idx} : REAL := 0.0;")
        lines.append(f"    r_diff_AB_{ch_idx} : REAL := 0.0;")
        lines.append(f"    r_diff_BC_{ch_idx} : REAL := 0.0;")
        lines.append(f"    r_diff_CA_{ch_idx} : REAL := 0.0;")
        lines.append(f"    r_timer_AB_{ch_idx} : REAL := 0.0;")
        lines.append(f"    r_timer_BC_{ch_idx} : REAL := 0.0;")
        lines.append(f"    r_timer_CA_{ch_idx} : REAL := 0.0;")
        lines.append(f"    b_fault_AB_{ch_idx} : BOOL := FALSE;")
        lines.append(f"    b_fault_BC_{ch_idx} : BOOL := FALSE;")
        lines.append(f"    b_fault_CA_{ch_idx} : BOOL := FALSE;")
        lines.append(f"    b_chA_healthy_{ch_idx} : BOOL := TRUE;")
        lines.append(f"    b_chB_healthy_{ch_idx} : BOOL := TRUE;")
        lines.append(f"    b_chC_healthy_{ch_idx} : BOOL := TRUE;")
        lines.append(f"    i_healthy_count_{ch_idx} : INT := 3;")
        lines.append(f"    i_degrade_mode_{ch_idx} : INT := 3;")
        lines.append(f"    r_thresh_{ch_idx} : REAL := 1.0;")
        lines.append(f"    r_max_slew_{ch_idx} : REAL := 10000.0;")

    # FSM variables
    lines.append("\n    (* === 14-STAGE PRODUCTION FINITE STATE MACHINE VARIABLES === *)")
    lines.append("    r_State_Timer : REAL := 0.0;")
    lines.append("    r_Sub_State_Timer : REAL := 0.0;")
    lines.append("    r_Stage_Timeout_Limit : REAL := 2.0;")
    lines.append("    r_Wire_Cycle_Timer : REAL := 0.0;")
    lines.append("    b_Cell_Fault_Trip : BOOL := FALSE;")
    lines.append("    b_Stage_Fault_Aborted : BOOL := FALSE;")
    lines.append("    r_Traj_s_tau : REAL := 0.0;")
    lines.append("    r_Traj_ds_tau : REAL := 0.0;")
    lines.append("    r_Traj_tau : REAL := 0.0;")
    lines.append("    r_Traj_Z_Start : REAL := 0.0;")
    lines.append("    r_Traj_Z_Target : REAL := 0.0;")
    lines.append("    r_Traj_Duration : REAL := 0.020;")
    lines.append("    r_Loop_X_Kink : REAL := -15.0;")
    lines.append("    r_Loop_Z_Kink : REAL := 25.0;")
    lines.append("    r_Loop_Apex_Z : REAL := 180.0;")
    lines.append("    r_Loop_Lead_X : REAL := 1250.0;")
    lines.append("    r_Loop_Lead_Y : REAL := 450.0;")
    lines.append("    r_Loop_Lead_Z : REAL := 0.0;")
    lines.append("    r_EFO_Energy_mJ : REAL := 0.0;")
    lines.append("    r_EFO_Time_Elapsed_us : REAL := 0.0;")
    lines.append("    b_EFO_Discharging : BOOL := FALSE;")
    lines.append("    r_Scrub_Osc_Freq_Hz : REAL := 120.0;")
    lines.append("    r_Scrub_Osc_Amp_um : REAL := 1.20;")
    lines.append("    r_Scrub_Elapsed_ms : REAL := 0.0;")
    lines.append("    r_IMC_Thickness_nm : REAL := 1.0;")
    lines.append("    r_Stitch_Squash_Ratio : REAL := 1.0;")
    lines.append("    r_Stitch_Elapsed_ms : REAL := 0.0;")
    lines.append("    r_Tail_Break_Force_Peak_mN : REAL := 0.0;")
    lines.append("    r_Tail_Length_Actual_um : REAL := 180.0;")
    lines.append("    r_Vision_Die_Angle_deg : REAL := 0.0;")
    lines.append("    r_Vision_Score_pct : REAL := 99.5;")
    lines.append("    udi_Wires_Passed_PR : UDINT := 0;")
    lines.append("    udi_Wires_Failed_PR : UDINT := 0;")
    lines.append("    r_Wire_Bond_Pitch_Actual_um : REAL := 35.0;")
    lines.append("    r_Tracked_US_Freq_kHz : REAL := 128.50;")
    lines.append("    r_US_Impedance_Mag_Ohm : REAL := 15.0;")
    lines.append("    r_US_Phase_Rad : REAL := 0.0;")
    lines.append("    r_US_Conductance_G : REAL := 0.065;")
    lines.append("    r_US_Susceptance_B : REAL := 0.0;")

    # ISA-18.2 Alarms
    lines.append("\n    (* === ANSI/ISA-18.2 MULTI-TIERED ALARM ENGINE VARIABLES === *)")
    alarm_vars = [
        "Z_Position_Error",
        "Bond_Contact_Force",
        "US_Impedance",
        "US_Horn_Amplitude",
        "Capillary_Temperature",
        "Substrate_Temperature",
        "EFO_Spark_Energy",
        "FAB_Diameter_Error",
        "Wire_Spool_Tension",
        "Capillary_Wear_Index"
    ]
    for idx, name in enumerate(alarm_vars, 1):
        lines.append(f"    (* Alarm Variable {idx}: {name} *)")
        lines.append(f"    r_Monitored_Val_{idx} : REAL := 0.0;")
        lines.append(f"    r_SP_HH_{idx} : REAL := 100.0;")
        lines.append(f"    r_SP_H_{idx} : REAL := 80.0;")
        lines.append(f"    r_SP_L_{idx} : REAL := 20.0;")
        lines.append(f"    r_SP_LL_{idx} : REAL := 10.0;")
        lines.append(f"    r_Hyst_{idx} : REAL := 2.0;")
        lines.append(f"    r_Timer_HH_{idx} : REAL := 0.0;")
        lines.append(f"    r_Timer_H_{idx} : REAL := 0.0;")
        lines.append(f"    r_Timer_L_{idx} : REAL := 0.0;")
        lines.append(f"    r_Timer_LL_{idx} : REAL := 0.0;")
        lines.append(f"    b_Alarm_HH_{idx} : BOOL := FALSE;")
        lines.append(f"    b_Alarm_H_{idx} : BOOL := FALSE;")
        lines.append(f"    b_Alarm_L_{idx} : BOOL := FALSE;")
        lines.append(f"    b_Alarm_LL_{idx} : BOOL := FALSE;")

    lines.append("END_VAR\n")
    return "\n".join(lines)

print("generate_var_internal defined.")

def generate_phase_1():
    lines = [
        "(* ==================================================================================================== *)",
        "(* PHASE 1: 4-CHANNEL 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING ARCHITECTURE                   *)",
        "(* IEC 61508 SIL-3 SAFETY & HIGH-AVAILABILITY SENSOR SUBSYSTEM                                           *)",
        "(* 4 INDEPENDENT SENSORY INSTRUMENTATION LOOPS:                                                         *)",
        "(*   CHANNEL 1: CAPILLARY Z-AXIS OPTICAL LINEAR ENCODERS [um]                                           *)",
        "(*   CHANNEL 2: VOICE-COIL PIEZOELECTRIC DYNAMIC IMPACT FORCE SENSORS [mN]                              *)",
        "(*   CHANNEL 3: HEATED VACUUM ANVIL PYROMETERS [deg C]                                                  *)",
        "(*   CHANNEL 4: ULTRASONIC GENERATOR RF PHASE PICKOFF TRANSDUCERS [deg]                                 *)",
        "(* FEATURES:                                                                                            *)",
        "(*   - Continuous Pairwise Discrepancy Monitoring (|A-B|, |B-C|, |C-A| vs Delta Threshold)              *)
        "(*   - 10 Millisecond Debounce Persistence Anti-Nuisance Filter Integration                             *)
        "(*   - 4-Tier Bumpless Degradation Hierarchy: 2oo3 Median -> 1oo2 Mean -> 1oo1 Direct -> Fail-Safe Trip *)
        "(* ==================================================================================================== *)"
    ]
    
    channels = [
        (1, "CAPILLARY Z-AXIS OPTICAL ENCODERS", "r_Enc_Z_Position_ChA_um", "r_Enc_Z_Position_ChB_um", "r_Enc_Z_Position_ChC_um", 1.50, 250000.0, "r_Enc_Z_Voted_um"),
        (2, "VOICE-COIL DYNAMIC IMPACT FORCE SENSORS", "r_Force_Sensor_ChA_mN", "r_Force_Sensor_ChB_mN", "r_Force_Sensor_ChC_mN", 15.00, 500000.0, "r_Force_Voted_mN"),
        (3, "HEATED VACUUM ANVIL PYROMETERS", "r_Pyrometer_Temp_ChA_degC", "r_Pyrometer_Temp_ChB_degC", "r_Pyrometer_Temp_ChC_degC", 4.00, 500.0, "r_Temp_Voted_degC"),
        (4, "ULTRASONIC GENERATOR RF PHASE PICKOFF", "r_US_Phase_ChA_deg", "r_US_Phase_ChB_deg", "r_US_Phase_ChC_deg", 3.50, 10000.0, "r_US_Phase_Voted_deg")
    ]
    
    for ch_idx, ch_name, sig_a, sig_b, sig_c, thresh, max_slew, out_var in channels:
        lines.append(f"\n(* ---------------------------------------------------------------------------------------------------- *)")
        lines.append(f"(* CHANNEL {ch_idx}: {ch_name} *)")
        lines.append(f"(* ---------------------------------------------------------------------------------------------------- *)")
        lines.append(f"r_thresh_{ch_idx} := {thresh:.2f};")
        lines.append(f"r_max_slew_{ch_idx} := {max_slew:.1f};")
        lines.append(f"r_diff_AB_{ch_idx} := ABS({sig_a} - {sig_b});")
        lines.append(f"r_diff_BC_{ch_idx} := ABS({sig_b} - {sig_c});")
        lines.append(f"r_diff_CA_{ch_idx} := ABS({sig_c} - {sig_a});")
        
        # Debounce timer A-B
        lines.append(f"IF r_diff_AB_{ch_idx} > r_thresh_{ch_idx} THEN")
        lines.append(f"    r_timer_AB_{ch_idx} := r_timer_AB_{ch_idx} + r_Cycle_Time_Delta_Sec;")
        lines.append(f"ELSE")
        lines.append(f"    IF r_timer_AB_{ch_idx} > (r_Cycle_Time_Delta_Sec * 2.0) THEN")
        lines.append(f"        r_timer_AB_{ch_idx} := r_timer_AB_{ch_idx} - (r_Cycle_Time_Delta_Sec * 2.0);")
        lines.append(f"    ELSE")
        lines.append(f"        r_timer_AB_{ch_idx} := 0.0;")
        lines.append(f"    END_IF;")
        lines.append(f"END_IF;")
        
        # Debounce timer B-C
        lines.append(f"IF r_diff_BC_{ch_idx} > r_thresh_{ch_idx} THEN")
        lines.append(f"    r_timer_BC_{ch_idx} := r_timer_BC_{ch_idx} + r_Cycle_Time_Delta_Sec;")
        lines.append(f"ELSE")
        lines.append(f"    IF r_timer_BC_{ch_idx} > (r_Cycle_Time_Delta_Sec * 2.0) THEN")
        lines.append(f"        r_timer_BC_{ch_idx} := r_timer_BC_{ch_idx} - (r_Cycle_Time_Delta_Sec * 2.0);")
        lines.append(f"    ELSE")
        lines.append(f"        r_timer_BC_{ch_idx} := 0.0;")
        lines.append(f"    END_IF;")
        lines.append(f"END_IF;")
        
        # Debounce timer C-A
        lines.append(f"IF r_diff_CA_{ch_idx} > r_thresh_{ch_idx} THEN")
        lines.append(f"    r_timer_CA_{ch_idx} := r_timer_CA_{ch_idx} + r_Cycle_Time_Delta_Sec;")
        lines.append(f"ELSE")
        lines.append(f"    IF r_timer_CA_{ch_idx} > (r_Cycle_Time_Delta_Sec * 2.0) THEN")
        lines.append(f"        r_timer_CA_{ch_idx} := r_timer_CA_{ch_idx} - (r_Cycle_Time_Delta_Sec * 2.0);")
        lines.append(f"    ELSE")
        lines.append(f"        r_timer_CA_{ch_idx} := 0.0;")
        lines.append(f"    END_IF;")
        lines.append(f"END_IF;")
        
        # Discrepancy flags (10 ms debounce threshold)
        lines.append(f"b_fault_AB_{ch_idx} := (r_timer_AB_{ch_idx} >= 0.0100);")
        lines.append(f"b_fault_BC_{ch_idx} := (r_timer_BC_{ch_idx} >= 0.0100);")
        lines.append(f"b_fault_CA_{ch_idx} := (r_timer_CA_{ch_idx} >= 0.0100);")
        
        # Healthy channel isolation
        lines.append(f"b_chA_healthy_{ch_idx} := NOT (b_fault_AB_{ch_idx} AND b_fault_CA_{ch_idx});")
        lines.append(f"b_chB_healthy_{ch_idx} := NOT (b_fault_AB_{ch_idx} AND b_fault_BC_{ch_idx});")
        lines.append(f"b_chC_healthy_{ch_idx} := NOT (b_fault_BC_{ch_idx} AND b_fault_CA_{ch_idx});")
        
        lines.append(f"i_healthy_count_{ch_idx} := BOOL_TO_INT(b_chA_healthy_{ch_idx}) + BOOL_TO_INT(b_chB_healthy_{ch_idx}) + BOOL_TO_INT(b_chC_healthy_{ch_idx});")
        
        # Voting hierarchy
        lines.append(f"IF i_healthy_count_{ch_idx} = 3 THEN")
        lines.append(f"    (* Mode 3: Full 2oo3 TMR Median Voting *)")
        lines.append(f"    i_degrade_mode_{ch_idx} := 3;")
        lines.append(f"    IF (({sig_a} >= {sig_b}) AND ({sig_a} <= {sig_c})) OR (({sig_a} <= {sig_b}) AND ({sig_a} >= {sig_c})) THEN")
        lines.append(f"        r_voted_{ch_idx} := {sig_a};")
        lines.append(f"    ELSIF (({sig_b} >= {sig_a}) AND ({sig_b} <= {sig_c})) OR (({sig_b} <= {sig_a}) AND ({sig_b} >= {sig_c})) THEN")
        lines.append(f"        r_voted_{ch_idx} := {sig_b};")
        lines.append(f"    ELSE")
        lines.append(f"        r_voted_{ch_idx} := {sig_c};")
        lines.append(f"    END_IF;")
        lines.append(f"ELSIF i_healthy_count_{ch_idx} = 2 THEN")
        lines.append(f"    (* Mode 2: 1oo2 Degraded Arithmetic Mean Averaging *)")
        lines.append(f"    i_degrade_mode_{ch_idx} := 2;")
        lines.append(f"    IF b_chA_healthy_{ch_idx} AND b_chB_healthy_{ch_idx} THEN")
        lines.append(f"        r_voted_{ch_idx} := ({sig_a} + {sig_b}) * 0.50;")
        lines.append(f"    ELSIF b_chB_healthy_{ch_idx} AND b_chC_healthy_{ch_idx} THEN")
        lines.append(f"        r_voted_{ch_idx} := ({sig_b} + {sig_c}) * 0.50;")
        lines.append(f"    ELSE")
        lines.append(f"        r_voted_{ch_idx} := ({sig_a} + {sig_c}) * 0.50;")
        lines.append(f"    END_IF;")
        lines.append(f"ELSIF i_healthy_count_{ch_idx} = 1 THEN")
        lines.append(f"    (* Mode 1: 1oo1 Single-Channel Direct Fallback with Process Advisory *)")
        lines.append(f"    i_degrade_mode_{ch_idx} := 1;")
        lines.append(f"    IF b_chA_healthy_{ch_idx} THEN")
        lines.append(f"        r_voted_{ch_idx} := {sig_a};")
        lines.append(f"    ELSIF b_chB_healthy_{ch_idx} THEN")
        lines.append(f"        r_voted_{ch_idx} := {sig_b};")
        lines.append(f"    ELSE")
        lines.append(f"        r_voted_{ch_idx} := {sig_c};")
        lines.append(f"    END_IF;")
        lines.append(f"ELSE")
        lines.append(f"    (* Mode 0: Dual/Triple Disagreement Fail-Safe Total Sensor Trip *)")
        lines.append(f"    i_degrade_mode_{ch_idx} := 0;")
        lines.append(f"    r_voted_{ch_idx} := r_last_voted_{ch_idx};")
        lines.append(f"    b_Cell_Fault_Trip := TRUE;")
        lines.append(f"    b_FailSafe_Retract_Active := TRUE;")
        lines.append(f"END_IF;")
        
        # Slew rate limitation and last voted store
        lines.append(f"IF ABS(r_voted_{ch_idx} - r_last_voted_{ch_idx}) > (r_max_slew_{ch_idx} * r_Cycle_Time_Delta_Sec) THEN")
        lines.append(f"    IF r_voted_{ch_idx} > r_last_voted_{ch_idx} THEN")
        lines.append(f"        r_voted_{ch_idx} := r_last_voted_{ch_idx} + (r_max_slew_{ch_idx} * r_Cycle_Time_Delta_Sec);")
        lines.append(f"    ELSE")
        lines.append(f"        r_voted_{ch_idx} := r_last_voted_{ch_idx} - (r_max_slew_{ch_idx} * r_Cycle_Time_Delta_Sec);")
        lines.append(f"    END_IF;")
        lines.append(f"END_IF;")
        lines.append(f"r_last_voted_{ch_idx} := r_voted_{ch_idx};")
        lines.append(f"{out_var} := r_voted_{ch_idx};")

    return "\n".join(lines)

print("generate_phase_1 defined.")
